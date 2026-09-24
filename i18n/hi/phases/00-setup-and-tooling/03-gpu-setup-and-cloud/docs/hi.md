# GPU सेटअप और क्लाउड

> सीपीयू पर प्रशिक्षण सीखने के लिए ठीक है। वास्तविक के लिए प्रशिक्षण एक GPU की जरूरत है।
> सीपीयू के साथ सीखने के लिए प्रशिक्षण नहीं है, लेकिन वास्तविक प्रशिक्षण के लिए GPU की आवश्यकता है।

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 0, Lesson 01 | **前置知识:** Phase 0, 第 01 课
**Time:** ~45 minutes | **时间:** ~45 分钟

## सीखने के लक्ष्य

- स्थानीय GPU उपलब्धता का सत्यापन `nvidia-smi`और PyTorch के CUDA API
  中文翻译: उपयोग `nvidia-smi`和 PyTorch का CUDA API 验证本地 GPU
- मुफ्त क्लाउड आधारित प्रयोगों के लिए T4 GPU के साथ Google Colab को कॉन्फ़िगर करें
  中文翻译: Google Colab के T4 GPU को कॉन्फ़िगर करें, मुफ्त क्लाउड-इन प्रयोग करें
- CPU बनाम GPU पर बेंचमार्क मैट्रिक्स गुणन और गति को मापें
  चीनी अनुवादः सीपीयू और जीपीयू के रैंक गुणांक के लिए आधार परीक्षण, माप त्वरण अनुपात
- अपने VRAM में फिट बैठता है कि सबसे बड़ा मॉडल का अनुमान लगाने के लिए fp16 अंगूठे के नियम का उपयोग
  中文翻译: fp16 प्रयोग विधि के साथ अपने प्रकट भंडारण क्षमता के तहत सबसे बड़ा मॉडल का अनुमान

> **【中文解读】**
> इस अध्याय में आपको सिखाया गया है कि GPU को कैसे कॉन्फ़िगर किया जाए। AI में, GPU प्रशिक्षण मॉडल का मुख्य हार्डवेयर है। यह प्रशिक्षण समय को कुछ घंटों से कुछ मिनटों तक कम कर सकता है।

## समस्या का वर्णन

सीपीयू पर 8 घंटे का प्रशिक्षण 10 मिनट का होता है, लेकिन सीएनएन, ट्रांसफार्मर या एलएलएम (चरण 4+) को प्रशिक्षित करने के बाद आपको जीपीयू त्वरण की आवश्यकता होती है।

> 阶段 1-3 के अधिकांश पाठ्यक्रम CPU पर अच्छी तरह से चल रहे हैं। लेकिन एक बार प्रशिक्षण शुरू करने के बाद CNN, ट्रांसफार्मर या LLM (चरण 4+), GPU को गति देने की आवश्यकता है।

आपके पास तीन विकल्प हैंः स्थानीय जीपीयू, क्लाउड जीपीयू, या गूगल कोलब (मुफ्त) ।

> आप तीन प्रकार के विकल्प हैंः本地 GPU、云端 GPU या Google Colab(免费)

> **【中文解读】**
> 阶段 1-3 के पाठ्यक्रम CPU पर चल सकते हैं। लेकिन से चरण 4 开始(CNN、Transformer、LLM), बिना GPU के धीमा हो जाएगा अप्राप्य हो जाएगा।

## अवधारणा का मूल अवधारणा

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
> GPU के पास हजारों कोर हैं, जो बड़ी संख्या में सरल गणना करने में सक्षम हैं।
```figure
s0-gpu-dispatch
```

## इसे बनाओ

## इसे बनाओ।

> **【中文解读】**नीचे तीन प्रकार के GPU 方案 प्रदान किए जाते हैंः本地 NVIDIA 显卡(免费但需要硬件) 谷歌 Colab(免费云 GPU) 云 GPU 租(按小时付费) ;; आपके शर्तों के अनुसार एक प्रकार का चयन करें即可──

### विकल्प 1: स्थानीय NVIDIA GPU

जाँचें कि क्या आपके पास एक हैः

>  जाँच करें कि क्या आप एक वास्तविक GPU है:

```bash
nvidia-smi  # 查看 GPU 状态和驱动信息
```

CUDA के साथ PyTorch स्थापित करें:

> स्थापना समर्थित CUDA का PyTorch:

```python
import torch

print(f"CUDA available: {torch.cuda.is_available()}")  # 检查 CUDA 是否可用
print(f"CUDA version: {torch.version.cuda}")  # CUDA 版本号
if torch.cuda.is_available():
    print(f"GPU: {torch.cuda.get_device_name(0)}")  # GPU 型号
    print(f"Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")  # 显存大小
```

### विकल्प 2: गूगल कोलाब

1. जाओ [colab.research.google.com](https://colab.research.google.com)
2. रनटाइम > रनटाइम प्रकार बदलें > T4 GPU # 运行时 > 更改运行时类型 > 选择 T4 GPU
3. दौड़ें`!nvidia-smi`सत्यापित करने के लिए # 验证 जीपीयू है या नहीं

इस कोर्स से नोटबुक सीधे कोलाब में अपलोड करें।

> इस पाठ्यक्रम की नोटबुक को सीधे कोलब में अपलोड करें।

### विकल्प 3: क्लाउड GPU

लैम्ब्डा लैब्स, रनपॉड या वास्ट.एआई के लिएः

> लैम्ब्डा लैब्स ऱनपॉड या वास्ट.एआई के लिए प्रयोग किया जाता हैः

```bash
ssh user@your-gpu-instance

pip install torch torchvision torchaudio
python -c "import torch; print(torch.cuda.get_device_name(0))"
```

### कोई GPU नहीं? कोई समस्या नहीं. कोई GPU नहीं? कोई संबंध नहीं.

> **【拓展：显存估算经验公式】**fp16 下 प्रत्येक पैरामीटर 2 字节──7B 参数模型(Llama 2 7B की तरह) लगभग 14GB 显存──加上优化器状态(Adam 需要 2 倍参数额外显存), प्रशिक्षण 7B 模型实际需要约 40-50GB 显存(一张A100 80GB 可以运行)──推理则只需要约14GB──这就是为什么`device = "cuda" if available else "cpu"`यह कोड एआई  इंजीनियरिंग में हर जगह दिखाई देता है।

अधिकांश पाठ CPU पर काम करते हैं. जिन लोगों को GPU की जरूरत है वे ऐसा कहेंगे और Colab लिंक शामिल करेंगे.

> अधिकांश पाठ्यक्रम CPU पर चल सकते हैं।

```python
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")  # 自动选择 GPU 或 CPU
print(f"Using: {device}")
```

## इसे बनाएंः GPU बनाम CPU बेंचमार्क

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
> उपरोक्त कोड CPU और GPU के मुकाबले रैखिक गुणांक पर गति अंतर है। रैखिक गुणांक तंत्रिका नेटवर्क प्रशिक्षण में सबसे केंद्रीय ऑपरेशन है।

## अभ्यास विषय

1. ऊपर बेंचमार्क चलाएं और सीपीयू बनाम जीपीयू समय की तुलना करें
   运行 ऊपर की基准测试, CPU और GPU की गति के मुकाबले
2. यदि आपके पास एक GPU नहीं है, तो इसे Google Colab पर चलाएं और तुलना करें
   यदि कोई स्थानीय GPU नहीं है, तो Google Colab में ऊपर चलाने और तुलना
3. जांचें कि आपके पास कितनी GPU मेमोरी है और अनुमान लगाएं कि आप सबसे बड़ा मॉडल फिट कर सकते हैं (आंगूठे का नियमः fp16 के लिए प्रति पैरामीटर 2 बाइट्स)
   检查你的GPU 显存大小,估算能装下最大模型(अनुभव विधि:fp16 下每个参数占 2 字节)

## Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key

> **【拓展：2026 年 GPU 市场参考】**एआई  प्रशिक्षण मुख्य प्रवाह GPU:RTX 4090(24GB,~$1600，个人学习首选）、A100（80GB，云端约 $2/घंटे)、H100(80GB,云端约$3/घंटे,训练大模型首选)。Google Colab 免费版提供 T4(16GB),足足足足跑完本课程大部分实验──

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
