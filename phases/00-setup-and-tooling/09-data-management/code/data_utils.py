"""
数据管理工具 — 数据集加载、流式处理、格式转换、拆分和模型缓存。
核心概念: Hugging Face datasets 库的使用、数据格式对比、可复现的数据拆分。
AI 对应: 数据管理是 ML 管线的第一步，本工具覆盖了数据加载到拆分的完整流程。
"""
import os
import sys
import json
import hashlib
from pathlib import Path

try:
    from datasets import load_dataset, Dataset
except ImportError:
    print("Install the datasets library: pip install datasets")  # 安装 datasets 库
    sys.exit(1)

try:
    from huggingface_hub import hf_hub_download
except ImportError:
    print("Install huggingface_hub: pip install huggingface_hub")  # 安装 HF Hub 库
    sys.exit(1)


CACHE_DIR = Path.home() / ".cache" / "huggingface" / "datasets"  # HF 数据集缓存目录


def load_and_inspect(dataset_name: str, config: str = None, split: str = "train"):
    """加载并检查数据集的基本信息（行数、列名、特征类型、首条数据）。"""
    kwargs = {"path": dataset_name}
    if config:
        kwargs["name"] = config
    if split:
        kwargs["split"] = split

    ds = load_dataset(**kwargs)  # 从 HF Hub 加载数据集
    print(f"Dataset: {dataset_name}")
    print(f"  Split: {split}")
    print(f"  Rows: {len(ds)}")
    print(f"  Columns: {ds.column_names}")
    print(f"  Features: {ds.features}")
    print(f"  First row: {ds[0]}")
    return ds


def stream_dataset(dataset_name: str, config: str = None, max_rows: int = 5):
    """流式加载数据集——逐行读取，不下载完整文件，适合超大数据集。"""
    kwargs = {"path": dataset_name, "split": "train", "streaming": True}  # streaming=True 启用流式模式
    if config:
        kwargs["name"] = config

    ds = load_dataset(**kwargs)
    rows = []
    for i, example in enumerate(ds):
        rows.append(example)
        if i >= max_rows - 1:
            break

    print(f"Streamed {len(rows)} rows from {dataset_name}")
    return rows


def convert_format(ds, output_dir: str, name: str):
    """将数据集转换为 CSV、JSON、Parquet 三种格式，并对比文件大小。"""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    csv_path = output_path / f"{name}.csv"
    json_path = output_path / f"{name}.json"
    parquet_path = output_path / f"{name}.parquet"

    ds.to_csv(str(csv_path))  # 转换为 CSV
    ds.to_json(str(json_path))  # 转换为 JSON
    ds.to_parquet(str(parquet_path))  # 转换为 Parquet（推荐格式）

    csv_size = csv_path.stat().st_size
    json_size = json_path.stat().st_size
    parquet_size = parquet_path.stat().st_size

    print(f"Format comparison for {name}:")
    print(f"  CSV:     {csv_size:>10,} bytes")
    print(f"  JSON:    {json_size:>10,} bytes")
    print(f"  Parquet: {parquet_size:>10,} bytes")
    print(f"  Parquet is {csv_size / parquet_size:.1f}x smaller than CSV")  # Parquet 压缩率

    return {"csv": csv_path, "json": json_path, "parquet": parquet_path}


def make_splits(ds, train_ratio: float = 0.8, val_ratio: float = 0.1, seed: int = 42):
    """将数据集拆分为训练/验证/测试三部分，使用固定种子确保可复现。"""
    test_ratio = 1.0 - train_ratio - val_ratio
    assert test_ratio > 0, "train_ratio + val_ratio must be less than 1.0"

    test_size = val_ratio + test_ratio
    split1 = ds.train_test_split(test_size=test_size, seed=seed)  # 第一次拆分：训练 vs (验证+测试)
    train_ds = split1["train"]

    val_fraction = val_ratio / test_size
    split2 = split1["test"].train_test_split(test_size=(1.0 - val_fraction), seed=seed)  # 第二次拆分：验证 vs 测试
    val_ds = split2["train"]
    test_ds = split2["test"]

    total = len(train_ds) + len(val_ds) + len(test_ds)
    print(f"Splits (seed={seed}):")  # 使用固定种子保证每次拆分结果一致
    print(f"  Train: {len(train_ds):>6} ({len(train_ds)/total:.1%})")
    print(f"  Val:   {len(val_ds):>6} ({len(val_ds)/total:.1%})")
    print(f"  Test:  {len(test_ds):>6} ({len(test_ds)/total:.1%})")

    return {"train": train_ds, "val": val_ds, "test": test_ds}


def download_model_file(repo_id: str, filename: str):
    """从 Hugging Face Hub 下载模型文件并缓存到本地。"""
    path = hf_hub_download(repo_id=repo_id, filename=filename)  # 自动缓存到 ~/.cache/huggingface/
    size = Path(path).stat().st_size
    print(f"Downloaded {filename} from {repo_id}")
    print(f"  Path: {path}")
    print(f"  Size: {size:,} bytes")
    return path


def cache_summary():
    """统计 Hugging Face 缓存目录的文件数和总大小。"""
    cache_path = CACHE_DIR
    if not cache_path.exists():
        print("No HF cache found yet.")  # 尚未缓存任何数据集
        return

    total_size = 0
    file_count = 0
    for f in cache_path.rglob("*"):
        if f.is_file():
            total_size += f.stat().st_size
            file_count += 1

    print(f"HF Dataset Cache: {cache_path}")
    print(f"  Files: {file_count}")
    print(f"  Total size: {total_size / (1024 * 1024):.1f} MB")


def load_from_parquet(path: str):
    """从 Parquet 文件加载数据集（推荐格式，速度快体积小）。"""
    ds = Dataset.from_parquet(path)
    print(f"Loaded {len(ds)} rows from {path}")
    return ds


def load_from_csv(path: str):
    """从 CSV 文件加载数据集。"""
    ds = Dataset.from_csv(path)
    print(f"Loaded {len(ds)} rows from {path}")
    return ds


def load_from_json(path: str):
    """从 JSON 文件加载数据集。"""
    ds = Dataset.from_json(path)
    print(f"Loaded {len(ds)} rows from {path}")
    return ds


def fingerprint(ds, num_rows: int = 100):
    """生成数据集的指纹（SHA-256 哈希），用于验证数据一致性。"""
    sample = ds.select(range(min(num_rows, len(ds))))
    content = json.dumps([row for row in sample], default=str).encode()
    digest = hashlib.sha256(content).hexdigest()[:16]  # 取前 16 位作为指纹
    print(f"Dataset fingerprint (first {num_rows} rows): {digest}")
    return digest


if __name__ == "__main__":
    print("=" * 60)
    print("Data Management Utility")  # 数据管理工具
    print("=" * 60)

    print("\n--- 1. Load and inspect a dataset ---")  # 1. 加载并检查数据集
    ds = load_and_inspect("rotten_tomatoes", split="train")

    print("\n--- 2. Stream a dataset ---")  # 2. 流式加载数据集
    rows = stream_dataset("rotten_tomatoes", max_rows=3)
    for row in rows:
        print(f"  {row['text'][:80]}...")

    print("\n--- 3. Convert formats ---")  # 3. 格式转换
    small_ds = ds.select(range(500))
    paths = convert_format(small_ds, "/tmp/data_utils_demo", "rotten_tomatoes_sample")

    print("\n--- 4. Create train/val/test splits ---")  # 4. 创建训练/验证/测试拆分
    splits = make_splits(small_ds, train_ratio=0.8, val_ratio=0.1, seed=42)

    print("\n--- 5. Reload from Parquet ---")  # 5. 从 Parquet 重新加载
    reloaded = load_from_parquet(str(paths["parquet"]))
    print(f"  Columns: {reloaded.column_names}")

    print("\n--- 6. Download a model file ---")  # 6. 下载模型文件
    download_model_file("sentence-transformers/all-MiniLM-L6-v2", "config.json")

    print("\n--- 7. Dataset fingerprint ---")  # 7. 数据集指纹
    fingerprint(ds)

    print("\n--- 8. Cache summary ---")  # 8. 缓存统计
    cache_summary()

    print("\n" + "=" * 60)
    print("All checks passed. Your data pipeline is ready.")  # 数据管线就绪
    print("=" * 60)
