# GPU Setup & Cloud  GPU Setup với nền tảng đám mây

> Trình luyện trên CPU là tốt cho việc học. Trình luyện cho thực tế cần một GPU.
> Sử dụng CPU để học không có vấn đề... nhưng thực sự cần GPU...

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 0, Lesson 01 | **前置知识:** Phase 0, 第 01 课
**Time:** ~45 minutes | **时间:** ~45 分钟

## Mục tiêu học tập

- Kiểm tra khả năng GPU địa phương bằng cách sử dụng `nvidia-smi`và API CUDA của PyTorch
  中文翻译:使用 `nvidia-smi`和 PyTorch của CUDA API 验证本地 GPU có sẵn không
- Cấu hình Google Colab với GPU T4 cho các thí nghiệm dựa trên đám mây miễn phí
  Trung ngữ翻译: cấu hình Google Colab của T4 GPU, thực hiện miễn phí cloud端实验
- Đánh giá nhân số matrix trên CPU vs GPU và đo tốc độ tăng tốc
  Trung ngữ翻译: tiến hành thử nghiệm cơ bản, đo lường tăng tốc tỷ lệ
- Đếm mô hình lớn nhất phù hợp với VRAM của bạn bằng cách sử dụng quy tắc ngón tay fp16
  Trung ngữ翻译: dùng fp16 经验法则估算你的显存能装下的最大模型

> **【中文解读】**
> Trong AI, GPU là phần cứng quan trọng của mô hình đào tạo. Nó có thể làm giảm thời gian đào tạo từ vài giờ xuống vài phút. Không có GPU địa phương cũng có thể sử dụng miễn phí Google Colab.

## Vấn đề  vấn đề mô tả

Hầu hết các bài học trong giai đoạn 1-3 chạy tốt trên CPU. Nhưng một khi bạn bắt đầu đào tạo CNN, biến đổi, hoặc LLM (phase 4+), bạn cần tăng tốc GPU. Một cuộc đào tạo kéo dài 8 giờ trên CPU mất 10 phút trên GPU.

> Phần lớn các khóa học của giai đoạn 1-3 hoạt động tốt trên CPU. Nhưng một khi bắt đầu đào tạo CNN, Transformer hoặc LLM, giai đoạn 4+), bạn cần GPU tăng tốc.

Bạn có ba tùy chọn: GPU địa phương, GPU đám mây, hoặc Google Colab (không).

> Bạn có 3 lựa chọn: bản địa GPU,云端 GPU hoặc Google Colab (tài liệu miễn phí)

> **【中文解读】**
> Các khóa học của giai đoạn 1-3 trên CPU có thể chạy. Nhưng từ giai đoạn 4 bắt đầu, không có GPU sẽ chậm đến không thể chấp nhận.

## Khái niệm cốt lõi

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
> GPU có hàng ngàn lõi, giỏi và thực hiện rất nhiều tính toán đơn giản như矩阵乘法.
```figure
s0-gpu-dispatch
```

## Hãy xây dựng nó

## Hãy xây dựng nó.

> **【中文解读】**Sau đây cung cấp ba loại GPU: 本地 NVIDIA 显卡(免费但需要硬件) 谷歌 Colab(免费云 GPU) 云 GPU 租(按小时付费) ;; tùy thuộc vào điều kiện của bạn chọn một loại即可──

### Tùy chọn 1: NVIDIA GPU địa phương

Hãy kiểm tra xem có có gì không.

> 检查你是否有本地GPU:

```bash
nvidia-smi  # 查看 GPU 状态和驱动信息
```

Lắp đặt PyTorch với CUDA:

> Ưu tiên của CUDA:

```python
import torch

print(f"CUDA available: {torch.cuda.is_available()}")  # 检查 CUDA 是否可用
print(f"CUDA version: {torch.version.cuda}")  # CUDA 版本号
if torch.cuda.is_available():
    print(f"GPU: {torch.cuda.get_device_name(0)}")  # GPU 型号
    print(f"Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")  # 显存大小
```

### Tùy chọn 2: Google Colab 谷歌 Colab 免费 GPU)

1. Đi đi[colab.research.google.com](https://colab.research.google.com)
2. Thời gian chạy > Thay đổi loại thời gian chạy > T4 GPU # 运行时 > 更改运行时类型 > 选择 T4 GPU
3. Đi chạy`!nvidia-smi`để xác minh # 验证 GPU là không có sẵn

Lên lên sổ ghi chép từ khóa học này trực tiếp đến Colab.

> Đăng sổ ghi chép của khóa học này trực tiếp lên để Colab.

### Tùy chọn 3: GPU đám mây

Đối với Lambda Labs, RunPod hoặc Vast.ai:

> Sử dụng cho Lambda Labs  RunPod hoặc Vast.ai:

```bash
ssh user@your-gpu-instance

pip install torch torchvision torchaudio
python -c "import torch; print(torch.cuda.get_device_name(0))"
```

### Không có GPU? Không có vấn đề.

> **【拓展：显存估算经验公式】**Fp16 下 mỗi参数 chiếm 2 字节──7B 参数模型(如Llama 2 7B) cần khoảng 14GB 显存──加上优化器状态(Adam 需要 2倍参数额外显存),训练 7B 模型实际需要约 40-50GB 显存(一张A100 80GB 可以跑)──推理则只需要约14GB──这就是为什么`device = "cuda" if available else "cpu"`Đây là một trong những công nghệ AI.

Hầu hết các bài học đều hoạt động trên CPU. Những người cần GPU sẽ nói như vậy và bao gồm các liên kết Colab.

> Phần lớn các khóa học trên CPU là có thể chạy.

```python
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")  # 自动选择 GPU 或 CPU
print(f"Using: {device}")
```

## Build It: GPU vs CPU benchmark  GPU vs CPU 基准测试

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
> Các mã trên đối với CPU và GPU trên các mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình:

## Tập luyện bài tập

1. Động cơ chuẩn ở trên và so sánh thời gian CPU vs GPU
   运行 trên cơ sở kiểm tra, so với tốc độ CPU và GPU
2. Nếu bạn không có GPU, chạy nó trên Google Colab và so sánh
   Nếu không có GPU địa phương, trên Google Colab hoạt động và đối với
3. Kiểm tra lượng bộ nhớ GPU bạn có và ước tính mô hình lớn nhất bạn có thể phù hợp (quyền ngón tay: 2 byte cho mỗi tham số cho fp16)
   检查你的GPU 显存大小,估算能装下的最大模型(经验法则:fp16 下每个参数占 2 字节)

## Từ khóa  Keyword

> **【拓展：2026 年 GPU 市场参考】**AI 训练 主流 GPU:RTX 4090(24GB,~$1600，个人学习首选）、A100（80GB，云端约 $2/h)、H100(80GB,云端约$3/h,训练大模型首选)。Google Colab 免费版提供 T4(16GB),足够跑完本课程大部分实验──

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
