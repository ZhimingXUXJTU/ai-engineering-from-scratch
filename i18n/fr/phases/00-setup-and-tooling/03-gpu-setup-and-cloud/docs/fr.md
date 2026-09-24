# Configuration de GPU et Cloud

> L'entraînement sur le processeur est bon pour apprendre.
> Avec le CPU, on apprend à apprendre.

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 0, Lesson 01 | **前置知识:** Phase 0, 第 01 课
**Time:** ~45 minutes | **时间:** ~45 分钟

## Objectifs d'apprentissage

- Vérifiez la disponibilité du GPU local en utilisant `nvidia-smi`et l'API CUDA de PyTorch
  Le mot " usage " est traduit par " usage "`nvidia-smi`Et le CPU de PyTorch est testé en utilisant des GPU
- Configurer Google Colab avec un GPU T4 pour des expériences basées sur le cloud gratuites
  Configurer le GPU T4 de Google Colab, faire une expérience gratuite sur le cloud
- Indiquez la multiplication de la matrice de référence sur le processeur par rapport au processeur graphique et mesurez la vitesse
  Traduction anglaise: à la CPU et à la GPU
- Évaluer le modèle le plus grand qui s'adapte à votre VRAM en utilisant la règle de pouce fp16
  Le modèle de l'expérience est le plus grand modèle de votre stockage.

> **【中文解读】**
> Ce chapitre vous apprend à configurer la GPU pour accélérer. Dans l'IA, la GPU est le matériel clé du modèle de formation. Il peut réduire le temps de formation de quelques heures à quelques minutes.

## Le problème .

La plupart des cours des phases 1-3 fonctionnent bien sur le processeur. Mais une fois que vous commencez à former des CNN, des transformateurs ou des LLM (phases 4+), vous avez besoin d'accélération de la GPU.

> La plupart des cours de la phase 1-3 sont bien fonctionnés sur le CPU. Mais une fois que vous avez commencé à entraîner CNN, Transformer ou LLM, la phase 4+), vous avez besoin de GPU accéléré.

Vous avez trois options: GPU local, GPU cloud ou Google Colab (gratuit).

> Vous avez trois choix: GPU local, GPU de terminal ou Google Colab (en anglais)

> **【中文解读】**
> Les cours de la phase 1-3 sont en cours de fonctionnement au niveau du CPU. Mais à partir de la phase 4 (CNN, Transformer, LLM), sans GPU, ils seront ralentis jusqu'à inacceptables.

## Le concept de base.

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
> La GPU possède des milliers de cœurs, et est capable de faire de nombreux calculs simples. La GPU peut donc fournir des dizaines à des centaines de fois plus d'accélération.
```figure
s0-gpu-dispatch
```

## Faites-le

## Construisez-le à la main.

> **【中文解读】**Vous trouverez ci-dessous trois types de GPU:

### Option 1: GPU NVIDIA local

Vérifiez si vous en avez un:

> Check si vous avez un GPU:

```bash
nvidia-smi  # 查看 GPU 状态和驱动信息
```

Installez PyTorch avec CUDA:

> Montage de la commande de la commande de la commande de la commande de la commande de la commande de la commande de la commande de la commande de la commande de la commande de la commande de la commande de la commande de la commande de la commande de la commande de la commande de la commande de la commande de la commande de la commande de la commande de la commande de la commande de la commande de la commande de la commande de la commande de commande de la commande de commande de la commande de commande de commande de la commande de commande de commande de commande de commande de commande de la commande de commande de commande de commande de commande de commande de commande de commande de commande de commande de commande de commande de commande de commande de commande de commande de commande de commande de commande de commande de commande de commande de commande de commande de commande de commande de commande de commande de commande de commande de commande de commande de commande de commande de commande de commande de commande de commande de commande de commande de commande de commande de commande de commande de commande de commande de commande de commande de commande de commande

```python
import torch

print(f"CUDA available: {torch.cuda.is_available()}")  # 检查 CUDA 是否可用
print(f"CUDA version: {torch.version.cuda}")  # CUDA 版本号
if torch.cuda.is_available():
    print(f"GPU: {torch.cuda.get_device_name(0)}")  # GPU 型号
    print(f"Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")  # 显存大小
```

### Option 2: Google Colab 谷歌 Colab 免费GPU)

1. Allez à la[colab.research.google.com](https://colab.research.google.com)
2. Temps d'exécution > Modifier le type d'exécution > T4 GPU # 运行时 > 更改运行时类型 > 选择 T4 GPU
3. On court .`!nvidia-smi`pour vérifier si la GPU est disponible

Téléchargez les carnets de ce cours directement à Colab.

> Le livre de notes de ce cours sera transmis directement à Colab.

### Option 3: GPU en nuage

Pour Lambda Labs, RunPod ou Vast.ai:

> Utilisé par Lambda Labs ≈ RunPod ou Vast.ai:

```bash
ssh user@your-gpu-instance

pip install torch torchvision torchaudio
python -c "import torch; print(torch.cuda.get_device_name(0))"
```

### Je suis pas en train de faire une vidéo.

> **【拓展：显存估算经验公式】**Le modèle de paramètres de l'application est de 2 caractères. Il a besoin d'environ 14 Go de stockage.`device = "cuda" if available else "cpu"`Ce code est partout visible dans l'IA.

La plupart des leçons fonctionnent sur le processeur. Ceux qui ont besoin de GPU diront ainsi et incluront des liens Colab.

> La plupart des cours sont en CPU et peuvent fonctionner.

```python
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")  # 自动选择 GPU 或 CPU
print(f"Using: {device}")
```

## Le GPU contre le CPU est un test de base.

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
> Le code ci-dessus est le plus central de l'entraînement du réseau nerveux, l'effet d'accélération du GPU détermine directement l'efficacité de l'entraînement.

## Les exercices

1. Exécutez le point de référence ci-dessus et comparer les temps de CPU vs GPU
   运行上基准测试, par rapport à la vitesse du CPU et du GPU
2. Si vous n'avez pas de GPU, exécutez-le sur Google Colab et comparez
   Si vous n'avez pas de GPU, vous pouvez utiliser Google Colab
3. Vérifiez combien de mémoire GPU vous avez et estimez le plus grand modèle que vous pouvez adapter (règle générale: 2 octets par paramètre pour fp16)
   检查你的GPU 显存大小,estimate能装下的最大模型(l'expérience

## Les termes clés

> **【拓展：2026 年 GPU 市场参考】**La GPU est de 4090 [24 Go,~]$1600，个人学习首选）、A100（80GB，云端约 $2/h)、H100(80GB,云端约$3/h,训练大模型首选)。Google Colab 免费版提供 T4(16GB),足足足足跑完本课程大部分实验──

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
