# Configuração de GPU e nuvem

> O treinamento com CPU é bom para aprender.
> Usar CPU para treinar não há problemas, mas o treinamento real requer GPU.

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 0, Lesson 01 | **前置知识:** Phase 0, 第 01 课
**Time:** ~45 minutes | **时间:** ~45 分钟

## Objetivos de aprendizagem

- Verifique a disponibilidade local da GPU usando `nvidia-smi`e a API CUDA da PyTorch
  Tradução:`nvidia-smi`和 PyTorch's CUDA API 验证本地 GPU 是否可用
- Configure o Google Colab com uma GPU T4 para experimentos gratuitos baseados em nuvem
  Configurar a GPU T4 do Google Colab, fazer experiência gratuita no cloud
- Marque a multiplicação de matriz de referência na CPU vs GPU e mede a aceleração
  Tradução do inglês para PC: CPU e GPU
- Estima o modelo maior que se encaixa no seu VRAM usando a regra fp16 do polegar
  Tradução do inglês: using fp16 experience law estimate your apparent storage能装下的最大模型

> **【中文解读】**
> Este capítulo ensina-lhe como configurar GPU aceleração. Em AI, GPU é o hardware chave do modelo de treinamento. Ele pode reduzir o tempo de treinamento de algumas horas para alguns minutos.

## O problema .

A maioria das aulas nas fases 1-3 funciona bem na CPU. Mas uma vez que você começa a treinar CNNs, transformadores ou LLMs (fasas 4+), você precisa de aceleração da GPU. Uma corrida de treinamento que leva 8 horas na CPU leva 10 minutos na GPU.

> A maior parte dos cursos de fases 1-3 funciona bem na CPU. Mas uma vez que começa a treinar CNN, Transformer ou LLM, é necessário GPU acelerado.

Você tem três opções: GPU local, GPU em nuvem ou Google Colab (gratuito).

> Você tem três opções: GPU local, GPU de terminal ou Google Colab (WEB

> **【中文解读】**
> O curso da fase 1-3 está no CPU, mas a partir da fase 4 começa a funcionar.

## O conceito central.

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
> A GPU possui milhares de núcleos, que são bons para executar um grande número de simples cálculos. A formação da rede neural é, em sua essência, um grande número de cálculos de matrizes, de modo que a GPU pode fornecer dezenas a cem vezes mais aceleração.
```figure
s0-gpu-dispatch
```

## Construí-lo

## Construí-lo.

> **【中文解读】**Os seguintes fornecem três tipos de GPUs:

### Opção 1: GPU local NVIDIA real NVIDIA GPU

Verifique se tem um .

> Verifique se tem GPU local:

```bash
nvidia-smi  # 查看 GPU 状态和驱动信息
```

Instalar PyTorch com CUDA:

> Instalação de apoio à CUDA

```python
import torch

print(f"CUDA available: {torch.cuda.is_available()}")  # 检查 CUDA 是否可用
print(f"CUDA version: {torch.version.cuda}")  # CUDA 版本号
if torch.cuda.is_available():
    print(f"GPU: {torch.cuda.get_device_name(0)}")  # GPU 型号
    print(f"Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")  # 显存大小
```

### Opção 2: Google Colab Google Colab (GPU gratuito)

1. Vai para o[colab.research.google.com](https://colab.research.google.com)
2. Tempo de execução > Mudança de tipo de tempo de execução > T4 GPU # 运行时 > 更改运行时类型 > 选择 T4 GPU
3. Corra .`!nvidia-smi`para verificar # 验证 GPU

Faça o upload dos cadernos deste curso diretamente para o Colab.

> A partir de agora, o programa será transmitido ao Colab.

### Opção 3: GPU em nuvem

Para Lambda Labs, RunPod ou Vast.ai:

> Utilizado em Lambda Labs ≈ RunPod ou Vast.ai:

```bash
ssh user@your-gpu-instance

pip install torch torchvision torchaudio
python -c "import torch; print(torch.cuda.get_device_name(0))"
```

### Não há GPU? Não há problema.

> **【拓展：显存估算经验公式】**fp16 下每个参数占 2 字节──7B 参数模型(如Llama 2 7B) requer cerca de 14GB 显存──加上优化器状态(Adam 需要 2 倍参数额外显存),训练 7B 模型实际需要约 40-50GB 显存(一张A100 80GB 可以跑)──推理则只需要约 14GB──这就是为什么`device = "cuda" if available else "cpu"`Este código é em todo o ar em engenharia de IA.

A maioria das aulas funciona com CPU. Aqueles que precisam de GPU dirão isso e incluirão links Colab.

> A maior parte dos cursos está no CPU e pode ser executado.

```python
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")  # 自动选择 GPU 或 CPU
print(f"Using: {device}")
```

## Construir: GPU vs CPU benchmark . GPU vs CPU 基准测试

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
> O código acima compara a CPU e a GPU com a diferença de velocidade na matriz multiplicada. A matriz multiplicada é o cálculo mais central do treinamento de redes neurais, o efeito de aceleração da GPU determina diretamente a eficiência do treinamento.

## Exercícios.

1. Execute o benchmark acima e compare CPU vs GPU vezes
   运行 上面基准测试, em relação à velocidade do CPU e GPU
2. Se você não tem uma GPU, execute no Google Colab e compare
   Se não houver GPU local, no Google Colab
3. Verifique a quantidade de memória de GPU que você tem e estimar o maior modelo que você pode caber (regra geral: 2 bytes por parâmetro para fp16)
   检查你的GPU 显存大小,估算能装下的最大模型(experience法则:fp16 下每个参数占 2 字节)

## Termos-chave .

> **【拓展：2026 年 GPU 市场参考】**A inteligência artificial 训练的主流 GPU:RTX 4090(24GB,~$1600，个人学习首选）、A100（80GB，云端约 $2/h)、H100(80GB,云端约$3/h,训练大模型首选)。Google Colab 免费版提供 T4(16GB),足足足足跑完本课程大部分实验──

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
