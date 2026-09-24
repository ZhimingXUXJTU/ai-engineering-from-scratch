# إعدادات الجيبو و السحابة

> التدريب على المعالجة المركزية جيد للتعلم التدريب الحقيقي يحتاج إلى GPU
> لا يوجد مشكلة في التعلم باستخدام CPU ولكن التدريب الحقيقي يتطلب GPU

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 0, Lesson 01 | **前置知识:** Phase 0, 第 01 课
**Time:** ~45 minutes | **时间:** ~45 分钟

## أهداف التعلم

- التحقق من توافر GPU المحلي باستخدام `nvidia-smi`و API CUDA من PyTorch
  中文翻译: استخدام `nvidia-smi`و بايتورش's CUDA API 验证本地 GPU 是否可用
- قم بتهيئة Google Colab مع GPU T4 للتجارب المستندة إلى السحابة مجانا
  中文翻译: إعداد Google Colab T4 GPU، إجراء تجربة مجانية على النظام التشغيلي
- قم بتحديد مضاعفة المصفوفة المرجعية على CPU مقابل GPU وقياس السرعة
  ترجمة باللغة الصينية: قياس المعدلات المحددة للسي سي و GPU
- تقدير أكبر نموذج يناسب في VRAM الخاص بك باستخدام قاعدة fp16 الإبهام
  中文翻译: باستخدام fp16  تجربة قانون تقييم الخاص بك الحفاظ على قدر أكبر من النماذج تحت

> **【中文解读】**
> هذا الفصل يعلمك كيفية تثبيت GPU تسريع. في الذكاء الاصطناعي، GPU هو الأجهزة الرئيسية لموديل التدريب. يمكن أن تقلل وقت التدريب من بضعة ساعات إلى بضعة دقائق.

## المشكلة

معظم الدروس في المراحل 1-3 تعمل بشكل جيد على المعالجة المركزية. ولكن بمجرد البدء في تدريب سي إن إن، المحولات، أو LLM (المراحل 4+) ، تحتاج إلى تسريع GPU. تشغيل التدريب الذي يستغرق 8 ساعات على المعالجة المركزية يستغرق 10 دقائق على GPU.

> معظم الدورات في المرحلة 1-3 تعمل بشكل جيد على جهاز التشغيل المركزي. ولكن بمجرد بدء تدريب CNN Transformer أو LLM مرة 4+) ، تحتاج إلى GPU تسريع.

لديك ثلاثة خيارات: GPU محلية، GPU سحرية، أو Google Colab (مجانية).

> لديك ثلاثة خيارات: GPU المحلي أو GPU النظام الأساسي أو Google Colab

> **【中文解读】**
> 阶段 1-3 课程在CPU上就能跑──但从阶段 4 开始(CNN、Transformer、LLM),没有GPU会慢到无法接受──CPU上 8 小时的训练,GPU上只需 10 分钟──

## المفهوم الأساسي

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
> تمتلك GPU آلاف النواة، وتتميز بتنفيذ الكثير من الحسابات البسيطة مثل الموجات المتعددة.
```figure
s0-gpu-dispatch
```

## بناءها

## بناءه بيد بناءه

> **【中文解读】**ويكمن في ثلاثة أنواع من برامج الجيبو:本地 NVIDIA 显卡(免费但需要硬件) 谷歌 Colab(免费云 GPU) 云 GPU 租(按小时付费) ;; حسب شروطك اختيار طريقة即可──

### الخيار الأول: GPU NVIDIA المحلية

تحقق من وجودك

> تحقق من وجود GPU محلية

```bash
nvidia-smi  # 查看 GPU 状态和驱动信息
```

قم بتثبيت PyTorch مع CUDA:

> تنصيب دعم كودا بيتورش:

```python
import torch

print(f"CUDA available: {torch.cuda.is_available()}")  # 检查 CUDA 是否可用
print(f"CUDA version: {torch.version.cuda}")  # CUDA 版本号
if torch.cuda.is_available():
    print(f"GPU: {torch.cuda.get_device_name(0)}")  # GPU 型号
    print(f"Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")  # 显存大小
```

### الخيار الثاني: Google Colab 谷歌 Colab

1. إذهب إلى[colab.research.google.com](https://colab.research.google.com)
2. وقت تشغيل > تغيير نوع وقت تشغيل > T4 GPU # 运行时 > 更改运行时类型 > 选择 T4 GPU
3. أركض`!nvidia-smi`للتحقق من # 验证 GPU 是否可用

قم بتحميل الملاحظات من هذه الدورة مباشرة إلى (كولاب)

> سوف نكتب المذكرة من هذا الدور مباشرة على موقع Colab

### الخيار الثالث: GPU السحاب

لـ Lambda Labs، RunPod، أو Vast.ai:

> تستخدم في مختبرات لامبدا

```bash
ssh user@your-gpu-instance

pip install torch torchvision torchaudio
python -c "import torch; print(torch.cuda.get_device_name(0))"
```

### لا يوجد جيبو؟ لا مشكلة. لا يوجد جيبو؟ لا علاقة.

> **【拓展：显存估算经验公式】**fp16 下每个参数占 2 字节──7B 参数模型(如Llama 2 7B) تحتاج إلى حوالي 14GB 显存──加上优化器状态(Adam 需要 2 倍参数额外显存),训练 7B 模型实际需要约 40-50GB 显存(一张A100 80GB 可以跑)──推理则只需要约 14GB──这就是为什么`device = "cuda" if available else "cpu"`هذا الكود يمكن رؤيته في كل مكان في مجال التصميم الذكوي

معظم الدروس تعمل على المعالجة المركزية. أولئك الذين يحتاجون إلى GPU سوف يقول ذلك وتشمل روابط Colab.

> معظم الدورات على CPU على التشغيل.

```python
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")  # 自动选择 GPU 或 CPU
print(f"Using: {device}")
```

## بناءه: GPU مقابل CPU مقياس

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
> الاختلافات السريعة في المطار المتعدد في المعدل المستخدمة في البرمجيات المستخدمة في التدريبات العصبية والتي تعتبر أساسية في التدريبات على شبكة العصبية، ويتحكم تأثير تسريع المعدل بشكل مباشر في كفاءة التدريب.

## تمارين التدريب

1. قم بتشغيل المعيار المرجعي أعلاه ومقارنة CPU مقابل GPU
   运行 基准测试, مقابل سرعة CPU و GPU
2. إذا لم يكن لديك جهاز GPU، تشغيله على Google Colab ومقارنة
   إذا لم يكن هناك GPU محلي، في Google Colab على تشغيل ومقارنة
3. تحقق من كمية ذاكرة GPU لديك وتقدير أكبر نموذج يمكنك إطلاقا (قاعدة الإبهام: 2 بايت لكل مبرمير ل fp16)
   检查你的GPU 显存大小,估算能装下的最大模型( تجربة قواعد:fp16 下每个参数占 2 字节)

## شروط رئيسية

> **【拓展：2026 年 GPU 市场参考】**الذكاء الاصطناعي 訓練的主流 GPU:RTX 4090(24GB،~$1600，个人学习首选）、A100（80GB，云端约 $2/ساعة)、H100(80GB،云端约$3/ساعة، training大模型首选)。Google Colab 免费版提供 T4(16GB),足足足跑完本课程大部分实验──

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
