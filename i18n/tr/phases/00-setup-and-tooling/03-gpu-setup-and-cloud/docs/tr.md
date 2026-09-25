# GPU Kurulum ve Bulut

> CPU'da eğitim öğrenmek için iyidir.
> CPU'yu kullanmak için eğitim görüyorum.

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 0, Lesson 01 | **前置知识:** Phase 0, 第 01 课
**Time:** ~45 minutes | **时间:** ~45 分钟

## Öğrenme hedefleri

- Yerel GPU kullanımı doğrulanması `nvidia-smi`Ve PyTorch'in CUDA API'si
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`nvidia-smi`和 PyTorch'ın CUDA API 验证本地 GPU
- Google Colab'ı ücretsiz bulut tabanlı deneyler için T4 GPU ile yapılandır
  Çin Çeviri: Google Colab'ın T4 GPU'sını yapılandır, ücretsiz cloud端 deneyimi yap
- CPU vs GPU'da standart matris çarpımı göster ve hızlandırmayı ölç
  Çinçe çevirisi: CPU ve GPU'nun matron çarpımına göre test yapılır, ölçüm hızlandırılması oranı
- VRAM'a en büyük modelin fp16 basamak kuralını kullanarak uygun olduğunu tahmin edin
  Çinçe Çevirimi: fp16  deney kuralıyla gösterilen kaydının en büyük modelini değerlendir

> **【中文解读】**
> Bu bölüm size GPU hızlandırma nasıl ayarlanacağını öğretiyor. AI'de, GPU, eğitim modelinin anahtar bir donanımıdır.

## Sorunları anlatın.

1-3 aşamada yapılan derslerin çoğu CPU'da iyi çalışır. Ancak CNN'ler, transformatörler veya LLM'ler (vazesi 4+) eğitime başladıktan sonra, GPU hızlandırmasına ihtiyacınız var. CPU'da 8 saat süren bir eğitim süreci GPU'da 10 dakika sürer.

> 阶段 1-3 derslerinin çoğu CPU üzerinde iyi çalışıyor. Ancak CNN  Transformer veya LLM ️ 阶段 4+) eğitimi başladıktan sonra GPU hızlandırılması gerekir. CPU'da 8 saatlik eğitim, GPU'da sadece 10 dakika gerekir.

Üç seçenekiniz var: yerel GPU, bulut GPU veya Google Colab (ücretsiz).

> Üç seçenek var: kendi GPU'ları, Google'ın Google'ı veya Google'ın Google'ı.

> **【中文解读】**
> 阶段 1-3 dersleri CPU üzerinde çalışacak. Ama 4'cü aşamada başlamak için, GPU olmadan yavaşlamak için kabul edilemez olacaktır.

## Konsepten bir şey.

```
Your options:

1. Local NVIDIA GPU          # 本地 NVIDIA 显卡
   Cost: $0 (you already have it)  # 免费（已有硬件）
   Setup: Install CUDA + cuDNN
   Best for: Regular use, large datasets  # 适合：日常使用、大数据集

2. Google Colab (free tier)  # 免费 Colab
   Cost: $0
   Setup: None               # 无需安装
   Best for: Quick experiments, no GPU at home  # 适合：快速实验、家里没有 GPU

3. Cloud GPU (Lambda, RunPod, Vast.ai)  # 云端 GPU 租赁
   Cost: $0.20-2.00/hr       # 按小时计费
   Setup: SSH + install
   Best for: Serious training, large models  # 适合：正式训练、大模型
```

> **【拓展：GPU 为什么适合 AI？】**
> GPU'nun binlerce çekirdeği vardır, çok sayıda basit hesaplama yapmayı başarır.
```figure
s0-gpu-dispatch
```

## Yapın

## Yapın.

> **【中文解读】**Aşağıda üç çeşit GPU 方案 sunuluyor:本地 NVIDIA 显卡(免费但需要硬件)、Google Colab(免费云 GPU)、云 GPU 租(按小时付费)。

### Seçenek 1: Yerel NVIDIA GPU

Bir tane var mı diye kontrol et.

> - Yerel GPU'lar olup olmadığını kontrol et.

```bash
nvidia-smi  # 查看 GPU 状态和驱动信息
```

PyTorch' i CUDA ile yükle:

> CUDA'nın PyTorch'i installed:

```python
import torch

print(f"CUDA available: {torch.cuda.is_available()}")  # 检查 CUDA 是否可用
print(f"CUDA version: {torch.version.cuda}")  # CUDA 版本号
if torch.cuda.is_available():
    print(f"GPU: {torch.cuda.get_device_name(0)}")  # GPU 型号
    print(f"Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")  # 显存大小
```

### Seçenek 2: Google Colab

1. Git .[colab.research.google.com](https://colab.research.google.com)
2. Çalışma Zamanı > Çalışma Zamanı Tipi > T4 GPU # 运行时 > 更改运行时类型 > 选择 T4 GPU
3. Çık .`!nvidia-smi`# 验证 GPU kullanılabilir mi olduğunu kontrol etmek için

Bu kursdan defterleri doğrudan Colab'a yükle.

> Bu ders defterini direkt olarak Colab'a aktarmak.

### Seçenek 3: Bulut GPU

Lambda Labs, RunPod veya Vast.ai için:

> Lambda Labs  RunPod veya Vast.ai için kullanılıyor:

```bash
ssh user@your-gpu-instance

pip install torch torchvision torchaudio
python -c "import torch; print(torch.cuda.get_device_name(0))"
```

### - Hiçbir GPU yok.

> **【拓展：显存估算经验公式】**fp16 下每个参数占 2 字节──7B 参数模型(Llama 2 7B gibi) yaklaşık 14GB 显存──加上优化器状态(Adam 需要 2 倍参数额外显存),训练 7B 模型实际需要约 40-50GB 显存(一张A100 80GB 可以运行)──推理则只需要约 14GB──这就是为什么`device = "cuda" if available else "cpu"`Bu kod AI'de her yerde görülüyor.

Çoğu ders CPU'da çalışır. GPU'ya ihtiyaç duyanlar da öyle söyler ve Colab bağlantıları içerir.

> Çoğu ders CPU'da çalıştırılabilir.

```python
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")  # 自动选择 GPU 或 CPU
print(f"Using: {device}")
```

## Yap: GPU vs CPU referansı . GPU vs CPU 基准测试

```python
import torch
import time

size = 5000

a_cpu = torch.randn(size, size)  # 生成随机矩阵 A
b_cpu = torch.randn(size, size)  # 生成随机矩阵 B

start = time.time()
c_cpu = a_cpu @ b_cpu  # CPU 矩阵乘法
cpu_time = time.time() - start
print(f"CPU: {cpu_time:.3f}s")

if torch.cuda.is_available():
    a_gpu = a_cpu.to("cuda")  # 将矩阵移到 GPU
    b_gpu = b_cpu.to("cuda")

    torch.cuda.synchronize()  # 等待 GPU 完成所有操作
    start = time.time()
    c_gpu = a_gpu @ b_gpu  # GPU 矩阵乘法
    torch.cuda.synchronize()  # 同步，确保计时准确
    gpu_time = time.time() - start
    print(f"GPU: {gpu_time:.3f}s")
    print(f"Speedup: {cpu_time / gpu_time:.0f}x")  # 加速倍数
```

> **【中文解读】**
> Yukarıdaki kod CPU ve GPU'yla karşılaştırıldığında, matron çarpma hızındaki farklar için geçerlidir. Matron çarpma, sinir ağları eğitimi en temel işlemdir.

## Egzersizler.

1. Yukarıdaki referans değerini çalıştırın ve CPU vs GPU sürelerini karşılaştırın
   运行上基准测试, CPU ve GPU hızına karşı
2. Eğer bir GPU'unuz yoksa, Google Colab'da çalıştırın ve karşılaştırın
   Eğer yerel GPU yoksa, Google Colab'da çalıştırılır ve karşılaştırılır
3. Ne kadar GPU belleği olduğunuzu kontrol edin ve yerleştirilebilecek en büyük modelin tahmin edilmesini sağlayın (barmak kuralı: fp16 için parametresi başına 2 byte)
   检查你的GPU 显存大小,估算能装下的最大模型(体验法则:fp16 下每个参数占2 字节)

## Anahtar Terimler

> **【拓展：2026 年 GPU 市场参考】**AI 訓練的主流 GPU:RTX 4090(24GB,~$1600，个人学习首选）、A100（80GB，云端约 $2/h)、H100(80GB,云端約$3/h, training大模型首选) ・・・Google Colab 免费版提供 T4(16GB),足足足跑完本课程大部分实验──

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| CUDA | "GPU programming" | NVIDIA's parallel computing platform that lets you run code on the GPU |
| VRAM | "GPU memory" | Video RAM on the GPU, separate from system RAM. Limits model size. |
| fp16 | "Half precision" | 16-bit floating point, uses half the memory of fp32 with minimal accuracy loss |
| Tensor Core | "Fast matrix hardware" | Specialized GPU cores for matrix multiplication, 4-8x faster than regular cores |

| 术语 | 俗称 | 实际含义 |
|------|------|---------|
| CUDA | "GPU 编程" | NVIDIA 的并行计算平台，让你能在 GPU 上运行代码 |
| VRAM | "显存" | GPU 上的视频内存，独立于系统内存，决定了能跑多大的模型 |
| fp16 | "半精度" | 16 位浮点数，占用 fp32 一半的内存，精度损失极小 |
| Tensor Core | "快速矩阵硬件" | GPU 上专门做矩阵乘法的核心，比普通核心快 4-8 倍 |
