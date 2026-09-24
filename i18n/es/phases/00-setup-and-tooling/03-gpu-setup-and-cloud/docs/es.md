# Configuración de GPU y nube

> El entrenamiento en CPU es bueno para aprender.
> Usando CPU entrenamiento para aprender no hay problemas  Pero el entrenamiento real requiere GPU

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 0, Lesson 01 | **前置知识:** Phase 0, 第 01 课
**Time:** ~45 minutes | **时间:** ~45 分钟

## Objetivos de aprendizaje

- Verifique la disponibilidad de GPU local utilizando `nvidia-smi`y la API CUDA de PyTorch
  En inglés:`nvidia-smi`Y PyTorch de CUDA API 验证本地 GPU ¿Y si está disponible
- Configurar Google Colab con una GPU T4 para experimentos gratuitos basados en la nube
  Configurar la GPU T4 de Google Colab, realizar experiencias gratuitas en el cloud
- Indique la multiplicación de matriz de referencia en CPU vs GPU y mide la aceleración
  Traducción:La CPU y la GPU se multiplican en base a la medida de la velocidad.
- Estima el modelo más grande que se ajusta a su VRAM usando la regla de pulgar fp16
  Con fp16 experience law estimar tu mayor modelo bajo el cuadro de almacenamiento

> **【中文解读】**
> Este capítulo te enseña cómo configurar GPU acelerado. En AI, GPU es el hardware clave del modelo de entrenamiento. Puede reducir el tiempo de entrenamiento de unas horas a unos minutos.

## El problema es describir el problema

La mayoría de las clases en las fases 1-3 funcionan bien en CPU. Pero una vez que comienzas a entrenar CNNs, transformadores o LLM (fase 4+), necesitas aceleración de GPU. Una carrera de entrenamiento que dura 8 horas en CPU toma 10 minutos en GPU.

> La mayor parte de los cursos de la fase 1-3 se ejecutan bien en la CPU. Pero una vez que empiecen a entrenar CNN, Transformer o LLM, la fase 4+), se necesita GPU acelerado.

Tienes tres opciones: GPU local, GPU en la nube o Google Colab (gratuito).

> Usted tiene tres opciones: GPU local, GPU de terminal o Google Colab (免费)

> **【中文解读】**
> El curso de las fases 1-3 está en la CPU, pero desde la fase 4 se inicia con la CPU, sin GPU, se retrasa hasta que no se puede aceptar.

## El concepto central.

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
> La GPU tiene miles de núcleos, es bueno para ejecutar un gran número de simples cálculos. La formación de la red neuronal es en esencia la operación de matrices de cantidades, por lo que la GPU puede proporcionar decenas o cientos de veces más de aceleración.
```figure
s0-gpu-dispatch
```

## Construye el mismo

## Construye con la mano.

> **【中文解读】**Se ofrecen tres tipos de GPUs: NVIDIA 显卡 (en inglés) 免费但需要硬件) 谷歌 Colab (en inglés) 免费云 GPU (en inglés) 云 GPU 租 (en inglés) 按小时付费) ⋅ según sus condiciones, elija una manera de hacerlo.

### Opción 1: GPU NVIDIA local real NVIDIA GPU

Compruebe si tiene uno:

> Cheque si tienes GPU local:

```bash
nvidia-smi  # 查看 GPU 状态和驱动信息
```

Instalar PyTorch con CUDA:

> Instalar el PyTorch de CUDA:

```python
import torch

print(f"CUDA available: {torch.cuda.is_available()}")  # 检查 CUDA 是否可用
print(f"CUDA version: {torch.version.cuda}")  # CUDA 版本号
if torch.cuda.is_available():
    print(f"GPU: {torch.cuda.get_device_name(0)}")  # GPU 型号
    print(f"Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")  # 显存大小
```

### Opción 2: Google Colab 谷歌 Colab 免费GPU)

1. ¡ Vamos ![colab.research.google.com](https://colab.research.google.com)
2. Tiempo de ejecución > Cambia el tipo de tiempo de ejecución > T4 GPU # 运行时 > 更改运行时类型 > 选择 T4 GPU
3. - ¿ Qué ?`!nvidia-smi`para verificar # 验证 GPU si es o no disponible

Cargue los cuadernos de este curso directamente a Colab.

> El libro de notas de este curso se transmite directamente a Colab.

### Opción 3: GPU en la nube

Para Lambda Labs, RunPod o Vast.ai:

> Utilizado en Lambda Labs  RunPod o Vast.ai:

```bash
ssh user@your-gpu-instance

pip install torch torchvision torchaudio
python -c "import torch; print(torch.cuda.get_device_name(0))"
```

### No hay GPU? No hay problema.

> **【拓展：显存估算经验公式】**fp16 下每参数占 2 字节──7B 参数模型(如Llama 2 7B) necesita alrededor de 14GB 显存──加上优化器状态(Adam 需要 2 倍参数额外显存), entrenamiento 7B 模型实际需要约 40-50GB 显存(一张A100 80GB 可以跑)──推理则只需要约14GB──这就是为什么`device = "cuda" if available else "cpu"`Este código es ubicuo en la ingeniería de IA.

La mayoría de las clases funcionan en CPU. Los que necesitan GPU dirán eso e incluirán enlaces Colab.

> La mayor parte de los cursos se ejecutan en la CPU.

```python
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")  # 自动选择 GPU 或 CPU
print(f"Using: {device}")
```

## Construirlo: GPU vs CPU referencia . GPU vs CPU 基准测试

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
> El código anterior se compara con la diferencia de velocidad de CPU y GPU en la matriz multiplicada. La matriz multiplicada es el cálculo más central de la formación de redes neuronales, el efecto de aceleración de la GPU determina directamente la eficiencia de la formación.

## Los ejercicios.

1. Ejecutar el índice de referencia de arriba y comparar CPU vs GPU veces
   运行 上的基准测试, en comparación con la velocidad de CPU y GPU
2. Si no tienes una GPU, ejecuta en Google Colab y compara
   Si no hay GPU local, en Google Colab arriba funcionará y se comparará
3. Compruebe la cantidad de memoria de GPU que tiene y estima el modelo más grande que pueda caber (regla de pulgar: 2 bytes por parámetro para fp16)
   检查你的GPU 显存大小,估算能装下的最大模型(experience法则:fp16 下每个参数占 2 字节)

## Términos clave .

> **【拓展：2026 年 GPU 市场参考】**La inteligencia artificial  entrenamiento de la GPU: RTX 4090(24GB,~$1600，个人学习首选）、A100（80GB，云端约 $2/h)、H100(80GB,云端约$3/hr,训练大模型首选)。Google Colab 免费版提供 T4(16GB),足够跑完本课程大部分实验──

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
