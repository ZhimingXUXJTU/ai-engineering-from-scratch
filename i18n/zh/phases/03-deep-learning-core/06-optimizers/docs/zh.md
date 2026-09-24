# 优化器

> 渐进式下降告诉你哪个方向移动. 它没有说多少距离或速度. SGD 是一个 компас.亚当是GPS与交通数据.

> **【中文解读】**梯度下降告诉你方向,但不说步幅和速度――SGD 像指南针只知道方向――亚当 像带实时路况的GPS根据历史信息调整策略――本章从零实现 SGD → 动力 →亚当 → 亚当W,理解每一步的优化直觉――

**Type:** Build
**Languages:** Python
**Prerequisites:** Lesson 03.05 (Loss Functions)
**Time:** ~75 minutes

## 学习目标

- 在Python中从零开始实现SGD,SGD与动力,亚当和亚当W优化器
- 解释亚当的偏见纠正如何补偿早期训练阶段零初始化时刻估计
- 证明为什么AdamW在同一任务上具有L2规律化,比Adam产生更好的概括性
- 选择适合转换器,CNN,GAN和细调的优化器和默认超参数

## 问题 问题引入

你计算了梯度.你知道重量#4,721应该减少0.003减少损失.但0.003在哪个单位?通过什么?

> 你计算了梯度――你知道权重#4,721 应该减少0.003来减少损失――但0.003是什么单位?按什么比例缩小?在步骤1和步骤1000上应该移动相同的量吗?

基梯度下降对每一步的每个参数都应用相同的学习速度:w = w - lr *梯度. 这造成了三种问题,使得训练神经网络在实践中很痛苦.

> 基本梯度在每个步骤上降低了对每个参数应用相同的学习率:w = w - lr *梯度.

首先,振荡. 失败的景观很少像一个滑. 这更像是一个长而狭窄的谷. 梯度指向谷 (向),而不是沿谷 (浅向). 渐进的下降反弹前后穿越狭窄的维度,同时在有用的维度上取得微小的进展. 你已经看到了:损失比高原快速下降,不是因为模型合,而是因为它正在振荡.

> 首先,振荡――损失曲面很少像平滑的碗――它更像一个长而窄的山谷――梯度指向山谷的横向方向),而不是纵向方向――梯度下降在狭维度上跳跳,而在有用的方向上进展小小――

另一方面,所有参数的学习速度都是错误的.有些重量需要大规模更新 (它们处于早期的,不适合的阶段).其他需要小规模的更新 (它们接近最佳值).一个适合前者学习率破坏后者,反之亦然.

> 其次,所有参数共享一个学习率是错误的.有些权力需要大更新.

第三,车点.在高层次,损失景观有广的平面区域,梯度接近零. 瓦尼拉 SGD 爬行这些在梯度的速度,实际上是零. 模型看起来卡住了. 它不是卡住的 - - 它在一个平面区域,另一边有有用的下降.

> 第三,点――在高层面,损失曲面有大片平面区域,梯度接近零――原始 SGD 以梯度 (实际上为零) 的速度爬行通过这些区域――模型看起来卡住了――它没有卡住它在平面区域,另一边有有用的下降――但 SGD 没有机制来突破――

亚当解决了所有三个问题. 它保持每参数的两个运行平均值 - - 平均梯度 (momentum,处理振荡) 和平均二次梯度 (适应速度,处理不同的尺度). 结合前几步的偏差纠正,它给你一个优化器,它可以解决80%的默认超参数问题. 这一课将它从头开始,所以你会明白,

> 亚当解决了所有三个问题. 它为每个参数维护两个运行平均值平均值梯度 (动量,处理振荡) 和平均梯度 (自适应速度,处理不同规模) 结合前几步的偏差修正,它提供了一个单一的优化器,适用于默认超参数的80%问题. 本课程从零构建它,让你准确地理解它在另外20%的问题上何时以及为什么失败.

> **【中文解读】**原始 SGD 有三个问题:振荡 (振荡) 谷中来跳动) 单一学习率 (单一学习率) 不适合所有参数 (不适合所有参数) 无法穿越平坦区域 (梯度接近零就卡住) 亚当 同时解决这三个问题:动量抑制振荡 (动量抑制振荡),自适应学习率 (自适应学习率) 适合不同参数 (不同参数),偏差修正加速初期收收──

## 概念的核心概念

### 随着梯度下降,

计算一个小批量上的梯度,然后朝着相反的方向行进.

> 最简单的优化器――在小批量上计算梯度,然后向相反方向走一步――

```
w = w - lr * gradient    # 最简单的参数更新公式
```

位式意味着你使用一个随机的子集 (迷你批量) 数据来估计梯度,而不是整个数据集.这个噪音实际上是有用的 - 它帮助逃避严峻的局部最小值.

> "随机"意味着你使用随机集群的数据量来估计梯度,而不是整个数据集.

学习率是唯一的. 太高:损失差异.太低:训练需要永远.最佳的价值取决于架构,数据,批量大小和训练的当前阶段. 在现代网络上,凡尼拉 SGD 的典型价值在0.01~0.1之间.

> 学习率是唯一的旋转――太高:损失发散――太低:训练永远不完美――最优的价值取决于训练的构建,数据,批量大小和当前阶段――对于现代网络上的原始SGD,典型的价值范围为0.01~0.1――但即使在单次训练运行中,理想的学习率也在变化――

### 动力动力

滚球下坡比喻过度使用,但确切.

> 滚滚山坡的比喻过度使用,但很准确. 与仅按梯度步进不同,你保持一个累积过去梯度的速度.

```
m_t = beta * m_{t-1} + gradient    # 速度 = 衰减 × 历史速度 + 当前梯度
w = w - lr * m_t                    # 沿速度方向更新
```

贝塔 (通常是0.9) 控制了要保存多少历史记录. 贝塔 =0.9,动力大致是最后10个梯度 (1 / (1 -0.9) =10的平均值.

> 贝塔 (通常为0.9) 控制保留多少历史──当贝塔 =0.9时,动量大约是最近10个梯度的平均值.

由于这种方法可以调整振荡,在同一方向指向的梯度积累.反向方向的梯度取消.在那个狭窄的谷中,"横"组件翻转每一步,减温."沿"组件保持一致,得到放大.结果是在有用方向上平稳加速.

> 为什么这能修复振荡:指向相同方向的梯度累积――转向的梯度相互抵消――在那个狭窄谷中,横向的分量每步翻转符号被抑制――"纵向"分量保持一致并被放大――结果是有用方向的平滑加速――

实际数字:在一个不良条件的损失景观上,SGD单独可能需要10,000步.在动力 (beta=0.9) 的SGD通常需要3,000-5,000步.

> 具体数字:在差异的损失曲面上,单独的 SGD 可能需要1万步.带动量 (beta=0.9) 的 SGD 在相同的问题上通常需要3万至5万步.

> **【拓展：SGD + Momentum 的 resurgence】**虽然亚当是默认选择,但2023年的论文显示SGD+时机在特定任务上仍然有优势.

### 们的子就在子里.

实际上有效的第一个每参数适应性学习率方法. 希顿在Coursera讲座中提出 (从未正式发表).

> 第一个真正有效的每参数自适应学习率方法――顿在课程中提出了 (从未正式发表)

```
s_t = beta * s_{t-1} + (1 - beta) * gradient^2
w = w - lr * gradient / (sqrt(s_t) + epsilon)
```

随着一个小的学习率,一个小的学习率 (s_t) 能够分为一个小的学习率.

> 追踪平方梯度的运行平均――梯度持续大的参数被一个大数除了(有效学习率更小) ――梯度小的参数被一个小数除了(有效学习率更大) ――

这解决了"所有参数的学习速度"的问题. 一个已经获得了大规模更新的重量可能接近目标 - - 减速. 一个已经获得了小规模更新的重量可能不够训练 - - 加速.

> 这解决了"所有参数共享一个学习率"的问题. 一个已经获得大更新权重可能接近目标.

子 (通常是1e-8) 在没有更新参数时,防止零分.

> 子 (通常是1e-8) 防止参数未更新时除以零.

### 亚当:动量 +自适应学习率

亚当将这两个想法结合在一起,每参数保持两个指数动平均值:

> 亚当结合了两种思想. 它为每个参数维护两个指数的移动平均值:

```
m_t = beta1 * m_{t-1} + (1 - beta1) * gradient        (first moment: mean)        # 一阶矩：梯度均值
v_t = beta2 * v_{t-1} + (1 - beta2) * gradient^2       (second moment: variance)   # 二阶矩：梯度方差
```

**Bias correction**基本的解释是最少的细节.在步骤1时,m_1= (1 - beta1) *梯度.在beta1=0.9时,这是0.1 *梯度--太小了10倍.移动平均值还没有升温.偏差纠正补偿:

> **偏差修正**是大多数解释跳过的关键细节──第 1 步,m_1 = (1 - beta1) *梯度──当beta1 = 0.9 时,是 0.1 *梯度小了十倍──移动平均还没"热身"完──偏差修正做补偿:

```
m_hat = m_t / (1 - beta1^t)
v_hat = v_t / (1 - beta2^t)
```

在步骤1 (beta1 = 0.9):m_hat =m_1 / (1 - 0.9) =m_1 / 0.1 =实际梯度.在步骤100: (1 - 0.9^100) 约为1.0,因此纠正消失.偏差纠正对第10步很重要,在50后是无关紧要的.

> 第1步beta1 = 0.9 时:m_hat = m_1 / (1 - 0.9) = m_1 / 0.1 = 实际梯度. 第100步:(1 - 0.9^100) 大约等于 1.0,修正消失──偏差修正对前 ~10 步重要,~50 步后无关紧要──

更新:

> 更新公式:

```
w = w - lr * m_hat / (sqrt(v_hat) + epsilon)
```

亚当默认:lr=0.001,beta1=0.9,beta2=0.999,epsilon=1e-8.这些默认解决80%的问题.如果没有,先更改lr.然后beta2.几乎从来没有更改beta1或epsilon.

> 亚当默认值:lr = 0.001,beta1 = 0.9,beta2 = 0.999,epsilon = 1e-8──这些默认值适用于80%的问题──不适用时,先调 lr,再调 beta2──几乎不需要改变beta1或epsilon──

> **【拓展：Adam 的局限性】**虽然亚当是最常用的优化器,但它并不完美: 1) 在某些凸状问题上收不像SGD; 2)亚当的泛化性有时比SGD差; 3)亚当的内存开销是SGD的2-3倍;

### 减肥是正确的

在尼拉 SGD 中,这相当于体重衰减 (减去每一步的体重中的 lambda * w).在亚当中,这种等效性断裂.

> 在原始 SGD 中,这等于权重减小,在亚当中,这等于权重减小.

洛希洛夫和哈特的见解:当你把L2加到损失中,然后亚当处理梯度时,适应性学习率也会扩大调节术语. 具有较大的梯度差异的参数得到较少的调节.具有较小的变异的参数得到更多.这不是你想要的 - - 你想要的调节是不论梯度统计数据如何.

> 洛希洛夫和哈特的洞察:当你将L2加到损失中,然后亚当处理梯度时,自适应学习率也会缩小正则化项.

在亚当更新后,亚当W直接将重量衰减应用于重量:

```
w = w - lr * m_hat / (sqrt(v_hat) + epsilon) - lr * lambda * w    # Adam 更新 + 解耦权重衰减
```

减肥率 (lr * lambda * w) 不由亚当的适应因子缩小.每个参数都得到相同的比例缩小.

这似乎是一个小细节.它不是.亚当W几乎在每一个任务上都与亚当+L2规律化相比更好的解决方案相近.它是 PyTorch 中的默认优化器,用于训练变压器,扩散模型和大多数现代建筑.BERT,GPT,LLaMA,稳定扩散--所有这些都是使用亚当W训练的.

> **【中文解读】**亚当W的关键改进:权重衰减不经过亚当的自适应缩放,直接作用于参数――BERT、GPT、Llama、稳定分散 都用亚当W 训练──默认参数:lr=3e-4,重量_衰减=0.01──

> **【拓展：LoRA 微调中的 AdamW】**用LoRA 微调 LLM 时,通常使用AdamW(lr=2e-5~1e-4,重量_衰减=0.01)。LoRA 只训练低排序分解矩阵 A 和 B,AdamW的权重衰减帮助控制这些新增参数的幅度。

### 学习率:最重要的超参数

```mermaid
graph TD
    LR["Learning Rate"] --> TooHigh["Too high (lr > 0.01)"]
    LR --> JustRight["Just right"]
    LR --> TooLow["Too low (lr < 0.00001)"]

    TooHigh --> Diverge["Loss explodes<br/>NaN weights<br/>Training crashes"]
    JustRight --> Converge["Loss decreases steadily<br/>Reaches good minimum<br/>Generalizes well"]
    TooLow --> Stall["Loss decreases slowly<br/>Gets stuck in suboptimal minimum<br/>Wastes compute"]

    JustRight --> Schedule["Usually needs scheduling"]
    Schedule --> Warmup["Warmup: ramp from 0 to max<br/>First 1-10% of training"]
    Schedule --> Decay["Decay: reduce over time<br/>Cosine or linear"]
```

学习速度的变化比任何建筑决定都重要.

> 如果只调整一个超参数,调学习率――学习率的变化比任何架构决策都重要――常见默认值:

- 清算量: lr = 0.01 至 0.1
  总体数:lr=0.01到0.1
- 亚当/亚当W: lr = 1e-4到 3e-4
  亚当/亚当W:lr=1e-4到3e-4
- 精细调节预训练的模型:lr = 1e-5至 5e-5
  微调预训练模型:lr = 1e-5 到 5e-5
- 学习速度升温:在第一步的1-10%上线性坡道
  学习率升温:前1-10% 步数内线性升温

### 优化器对优化器比较

```mermaid
flowchart LR
    subgraph "Optimization Path"
        SGD_P["SGD<br/>Oscillates across valley<br/>Slow but finds flat minima"]
        Mom_P["SGD + Momentum<br/>Smoother path<br/>3x faster than SGD"]
        Adam_P["Adam<br/>Adapts per-parameter<br/>Fast convergence"]
        AdamW_P["AdamW<br/>Adam + proper decay<br/>Best generalization"]
    end
    SGD_P --> Mom_P --> Adam_P --> AdamW_P
```

### 当每个优化器赢得时

```mermaid
flowchart TD
    Task["What are you training?"] --> Type{"Model type?"}

    Type -->|"Transformer / LLM"| AdamW["AdamW<br/>lr=1e-4, wd=0.01-0.1"]
    Type -->|"CNN / ResNet"| SGD_M["SGD + Momentum<br/>lr=0.1, momentum=0.9"]
    Type -->|"GAN"| Adam2["Adam<br/>lr=2e-4, beta1=0.5"]
    Type -->|"Fine-tuning"| AdamW2["AdamW<br/>lr=2e-5, wd=0.01"]
    Type -->|"Don't know yet"| Default["Start with AdamW<br/>lr=3e-4, wd=0.01"]
```

> **【拓展：深度学习中优化器的演进】**从2012年亚历克斯网的SGD+Momentum到2014年亚当提出,再到2017年亚当W的诞生优化器的发展让训练从"需要数周调调"变成"默认参数就能跑"――Llama 3 405B的训练使用亚当W,峰值 lr=3e-4,在16384块H100 GPU上训练了30.8M GPU 小时――

## 建立它,实现它.

> **【中文解读】**下面从零实现四种优化器:SGD → SGD+Momentum → AdamW──每个都在前一个基础上增加一个关键机制──注意亚当的偏差修正和亚当W的解权重减──这是面试常考的知识点──
```figure
optimizer-trajectory
```

## 建立它

### 步骤1: 瓦尼拉酸盐.

> 原始 SGD:参数直接减去学习率乘梯度――简单但容易振荡――

```python
class SGD:
    def __init__(self, lr=0.01):
        self.lr = lr

    def step(self, params, grads):
        for i in range(len(params)):
            params[i] -= self.lr * grads[i]
```

### 步骤2:SGD与动力第二步:带动量SGD

> 时刻:引入速度变量,累积历史梯度――指向一致方向的梯度相互叠加,振荡方向相互抵消――

```python
class SGDMomentum:
    def __init__(self, lr=0.01, beta=0.9):
        self.lr = lr
        self.beta = beta
        self.velocities = None

    def step(self, params, grads):
        if self.velocities is None:
            self.velocities = [0.0] * len(params)
        for i in range(len(params)):
            self.velocities[i] = self.beta * self.velocities[i] + grads[i]
            params[i] -= self.lr * self.velocities[i]
```

### 步骤3:亚当.

> 亚当:维护一阶矩 m) 和二阶矩 v) 梯度方差),加上偏差修正──80%的问题用默认参数就能跑──

```python
import math

class Adam:
    def __init__(self, lr=0.001, beta1=0.9, beta2=0.999, epsilon=1e-8):
        self.lr = lr
        self.beta1 = beta1
        self.beta2 = beta2
        self.epsilon = epsilon
        self.m = None
        self.v = None
        self.t = 0

    def step(self, params, grads):
        if self.m is None:
            self.m = [0.0] * len(params)
            self.v = [0.0] * len(params)

        self.t += 1

        for i in range(len(params)):
            self.m[i] = self.beta1 * self.m[i] + (1 - self.beta1) * grads[i]
            self.v[i] = self.beta2 * self.v[i] + (1 - self.beta2) * grads[i] ** 2

            m_hat = self.m[i] / (1 - self.beta1 ** self.t)
            v_hat = self.v[i] / (1 - self.beta2 ** self.t)

            params[i] -= self.lr * m_hat / (math.sqrt(v_hat) + self.epsilon)
```

### 亚当W.第四步:亚当W优化器

> 根据亚当的基础,将权重减轻从梯度中解直接对参数本身做减弱,不过 m 和 v 的缩放.

```python
class AdamW:
    def __init__(self, lr=0.001, beta1=0.9, beta2=0.999, epsilon=1e-8, weight_decay=0.01):
        self.lr = lr
        self.beta1 = beta1
        self.beta2 = beta2
        self.epsilon = epsilon
        self.weight_decay = weight_decay
        self.m = None
        self.v = None
        self.t = 0

    def step(self, params, grads):
        if self.m is None:
            self.m = [0.0] * len(params)
            self.v = [0.0] * len(params)

        self.t += 1

        for i in range(len(params)):
            self.m[i] = self.beta1 * self.m[i] + (1 - self.beta1) * grads[i]
            self.v[i] = self.beta2 * self.v[i] + (1 - self.beta2) * grads[i] ** 2

            m_hat = self.m[i] / (1 - self.beta1 ** self.t)
            v_hat = self.v[i] / (1 - self.beta2 ** self.t)

            params[i] -= self.lr * m_hat / (math.sqrt(v_hat) + self.epsilon)
            params[i] -= self.lr * self.weight_decay * params[i]
```

### 训练比较第五步:训练对比

训练从05课开始的圆数据集上使用四个优化器.

> 用第五课的圆形数据集训练与四种优化器相比,同一个双层网络的收获速度.

```python
import random

def sigmoid(x):
    x = max(-500, min(500, x))
    return 1.0 / (1.0 + math.exp(-x))

def make_circle_data(n=200, seed=42):
    random.seed(seed)
    data = []
    for _ in range(n):
        x = random.uniform(-2, 2)
        y = random.uniform(-2, 2)
        label = 1.0 if x * x + y * y < 1.5 else 0.0
        data.append(([x, y], label))
    return data


class OptimizerTestNetwork:
    def __init__(self, optimizer, hidden_size=8):
        random.seed(0)
        self.hidden_size = hidden_size
        self.optimizer = optimizer

        self.w1 = [[random.gauss(0, 0.5) for _ in range(2)] for _ in range(hidden_size)]
        self.b1 = [0.0] * hidden_size
        self.w2 = [random.gauss(0, 0.5) for _ in range(hidden_size)]
        self.b2 = 0.0

    def get_params(self):
        params = []
        for row in self.w1:
            params.extend(row)
        params.extend(self.b1)
        params.extend(self.w2)
        params.append(self.b2)
        return params

    def set_params(self, params):
        idx = 0
        for i in range(self.hidden_size):
            for j in range(2):
                self.w1[i][j] = params[idx]
                idx += 1
        for i in range(self.hidden_size):
            self.b1[i] = params[idx]
            idx += 1
        for i in range(self.hidden_size):
            self.w2[i] = params[idx]
            idx += 1
        self.b2 = params[idx]

    def forward(self, x):
        self.x = x
        self.z1 = []
        self.h = []
        for i in range(self.hidden_size):
            z = self.w1[i][0] * x[0] + self.w1[i][1] * x[1] + self.b1[i]
            self.z1.append(z)
            self.h.append(max(0.0, z))

        self.z2 = sum(self.w2[i] * self.h[i] for i in range(self.hidden_size)) + self.b2
        self.out = sigmoid(self.z2)
        return self.out

    def compute_grads(self, target):
        eps = 1e-15
        p = max(eps, min(1 - eps, self.out))
        d_loss = -(target / p) + (1 - target) / (1 - p)
        d_sigmoid = self.out * (1 - self.out)
        d_out = d_loss * d_sigmoid

        grads = [0.0] * (self.hidden_size * 2 + self.hidden_size + self.hidden_size + 1)
        idx = 0
        for i in range(self.hidden_size):
            d_relu = 1.0 if self.z1[i] > 0 else 0.0
            d_h = d_out * self.w2[i] * d_relu
            grads[idx] = d_h * self.x[0]
            grads[idx + 1] = d_h * self.x[1]
            idx += 2

        for i in range(self.hidden_size):
            d_relu = 1.0 if self.z1[i] > 0 else 0.0
            grads[idx] = d_out * self.w2[i] * d_relu
            idx += 1

        for i in range(self.hidden_size):
            grads[idx] = d_out * self.h[i]
            idx += 1

        grads[idx] = d_out
        return grads

    def train(self, data, epochs=300):
        losses = []
        for epoch in range(epochs):
            total_loss = 0.0
            correct = 0
            for x, y in data:
                pred = self.forward(x)
                grads = self.compute_grads(y)
                params = self.get_params()
                self.optimizer.step(params, grads)
                self.set_params(params)

                eps = 1e-15
                p = max(eps, min(1 - eps, pred))
                total_loss += -(y * math.log(p) + (1 - y) * math.log(1 - p))
                if (pred >= 0.5) == (y >= 0.5):
                    correct += 1
            avg_loss = total_loss / len(data)
            accuracy = correct / len(data) * 100
            losses.append((avg_loss, accuracy))
            if epoch % 75 == 0 or epoch == epochs - 1:
                print(f"    Epoch {epoch:3d}: loss={avg_loss:.4f}, accuracy={accuracy:.1f}%")
        return losses
```

> **【拓展：GPT 训练中的优化器选择】**培训时的一个常见技巧:对嵌入层和输出层使用不同的学习率. 在 PyTorch 中通过参数组实现:`optimizer = AdamW([{'params': base_params}, {'params': head_params, 'lr': lr*0.1}])`,我知道.

## 用它实现框架

> **【中文解读】**火中的训练循环模式:零_级 → 前进 → 损失 → 后退 → 剪辑 → 步骤 → 时间表――这个顺序不能搞错――CNN 用 SGD+ 时刻(lr=0.1),变压器 用 AdamW(lr=1e-4)。

 PyTorch 优化器处理参数组,梯度剪辑和学习速度规划:

```python
import torch
import torch.optim as optim

model = torch.nn.Sequential(
    torch.nn.Linear(784, 256),
    torch.nn.ReLU(),
    torch.nn.Linear(256, 10),
)

optimizer = optim.AdamW(model.parameters(), lr=3e-4, weight_decay=0.01)

scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=100)

for epoch in range(100):
    optimizer.zero_grad()
    output = model(torch.randn(32, 784))
    loss = torch.nn.functional.cross_entropy(output, torch.randint(0, 10, (32,)))
    loss.backward()
    torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
    optimizer.step()
    scheduler.step()
```

模式总是:零_级,前进,损失,后退, (剪辑),步骤, (时间表).记住这个顺序.错误 (例如,在优化器.步骤之前调用时间表.步骤()) 是微妙的错误的常见来源.

对于CNN,许多实践者仍然更喜欢SGD+动力 (lr=0.1,动力=0.9,重量_衰减=1e-4) 具有步骤或共数时间表.SGD发现更平坦的最小值,这些通常更好地概括.对于变压器和LLM来说,AdamW+共数衰减是普遍的默认.不要没有测量原因而战.

## 运送它.

这一课产生了:
- `outputs/prompt-optimizer-selector.md`-- 选择任何架构的最佳优化器和学习率的决定提示

## 练习题

1. 运行Nesterov动力,计算在"看头"位置 (w - lr * beta * v) 转移的梯度,而不是当前位置.
   > **练习 1：**实现Nesterov 动量 (在"前"位置计算梯度),对标准动量的收速度.

2. 实施学习速度升温时间表:在训练步骤的前10%中从0到max_lr的线性坡路,然后降低到0.与亚当+加热相比亚当没有加热的训练.测量圆数据集中达到90%的准确度需要多少时代.
   > **练习 2：**实现升温+宇宙衰变 学习率调度,对有/没有升温达到90%的准确率的轮数――

3. 追踪亚当训练期间每个参数的有效学习率.有效率是lr * m_hat / (sqrt(v_hat) + eps).在10 ,50和200步后绘制有效率的分布.所有参数都以相同的速度更新吗?
   > **练习 3：**追踪亚当 训练中各参数有效学习率,观察不同参数更新速度差异.

4. 执行梯度剪辑 (按全球标准剪辑).设置最高梯度标准为1.0.使用高学习率 (lr=0.01为亚当) 进行剪辑和没有剪辑训练.计算几次跑步分离 (损失到NaN) 进行10个随机种子或没有剪辑.
   > **练习 4：**实现梯度剪裁,统计有/无剪裁时高学习率下训练发散比例

5. 在一个大型权重网络上比较亚当与亚当W. 启动所有权重以随机值为 [-5, 5] (比正常大得多). 训练200个时代,体重_衰减=0.1. 绘制L2权重标准对两个优化器的训练.亚当W应该显示更快的体重缩小.
   > **练习 5：**在大初级权重下对亚当和亚当W,观察权重减减效差异.

## 关键词 关键词

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Learning rate | "Step size" | The scalar multiplier on the gradient update; the single most impactful hyperparameter in training |
| SGD | "Basic gradient descent" | Stochastic gradient descent: update weights by subtracting lr * gradient, computed on a mini-batch |
| Momentum | "Rolling ball analogy" | Exponential moving average of past gradients; dampens oscillation and accelerates consistent directions |
| RMSProp | "Adaptive learning rate" | Divides each parameter's gradient by the running RMS of its recent gradients; equalizes learning rates |
| Adam | "The default optimizer" | Combines momentum (first moment) and RMSProp (second moment) with bias correction for the initial steps |
| AdamW | "Adam done right" | Adam with decoupled weight decay; applies regularization directly to weights rather than through the gradient |
| Bias correction | "Warmup for running averages" | Dividing by (1 - beta^t) to compensate for the zero-initialization of Adam's moment estimates |
| Weight decay | "Shrink the weights" | Subtracting a fraction of the weight value at each step; a regularizer that penalizes large weights |
| Learning rate schedule | "Changing lr over time" | A function that adjusts the learning rate during training; warmup + cosine decay is the modern default |
| Gradient clipping | "Capping the gradient norm" | Scaling down the gradient vector when its norm exceeds a threshold; prevents exploding gradient updates |

| 术语 | 通俗说法 | 实际含义 |
|------|---------|---------|
| 学习率 (Learning rate) | "步长" | 梯度更新的标量乘数；训练中影响最大的超参数 |
| SGD | "基础梯度下降" | 随机梯度下降：用小批量梯度更新 w -= lr * grad |
| 动量 (Momentum) | "滚球的类比" | 历史梯度的指数移动平均；抑制振荡、加速一致方向 |
| RMSProp | "自适应学习率" | 除以梯度平方的移动平均根；均衡各参数学习速度 |
| Adam | "默认优化器" | 动量 + RMSProp + 偏差修正的统一优化器 |
| AdamW | "正确的 Adam" | Adam + 解耦权重衰减；直接对参数施加正则化 |
| 偏差修正 (Bias correction) | "运行平均的热身" | 除以 (1-beta^t) 补偿 Adam 矩估计的零初始化偏差 |
| 权重衰减 (Weight decay) | "缩小权重" | 每步减去权重的一小部分；惩罚大权重的正则化手段 |
| 学习率调度 (LR schedule) | "随时间改变 lr" | 训练中调整学习率的函数；warmup + cosine decay 是现代标配 |
| 梯度裁剪 (Gradient clipping) | "限制梯度范数" | 梯度范数超限时缩小梯度；防止梯度爆炸 |

## 继续阅读 继续阅读

- Kingma & Ba, "亚当:一种方法来实现斯托哈斯主义优化" (2014) -- 原始的亚当论文与融合分析和偏差纠正衍生
- 洛希洛夫和哈特, "脱节体重衰减规范化" (2017) -- 证明L2规范化和体重衰减在亚当中并非等同,并提出亚当W
- 史密斯,"训练神经网络周期性学习率" (2017) -- 引入了LR范围测试和周期性时间表,
- 鲁德, "渐进下降优化算法的概述" (2016) - - 优化器变体中最好的单一调查,有明确的比较和直觉
