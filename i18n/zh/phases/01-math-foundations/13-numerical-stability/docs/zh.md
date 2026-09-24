# 数字稳定性

> 浮点是一个漏洞的抽象,它会在训练中咬你,你不会看到它.
> 浮点数是漏水的抽象. 它会在训练中咬你一口,而你不会看到它到来.

**Type:** Build | **类型:** 动手
**Language:**子**语言:**字符串
**Prerequisites:** Phase 1, Lessons 01-04 | **前置知识:** Phase 1, Lessons 01-04
**Time:** ~120 minutes | **时间:** ~120 分钟

## 学习目标

- 通过最大减法技巧实现数值稳定的软max和日志总和-exp
  使用最大值减小技巧实现数值稳定软max 和日志总和exp
- 在浮点计算中确定过度流量,低流量和灾难性取消
  识别浮点计算中的溢溢和灾难性抵消
- 通过中心化有限差异对数值梯度进行分析梯度验证
  用中心有限差分验证解析梯度
- 解释为什么bfloat16是训练中偏好的,以及损失缩小如何防止梯度下流
  解释为什么Bfloat16比Bfloat16更适合训练,以及如何防止降水降低

> **【中文解读】**
> 浮点数是漏水的抽象──训练 3 小时后损失 变 NaN是最常见的崩──本章实现数值稳定的软max(减最大值技巧),解释为什么bfloat16比float16更适合训练──混合精度训练中使用损失缩小 防止小梯度下溢──

## 问题 问题引入

> **【中文解读】**三种典型数值稳定性灾难: 1) 训练 3 小时后损失 变化 NaN某步计算溢出; 2) 精度比论文差 2% 浮16的累积舍入误差吃掉准确率; 3) 自写交叉 大逻辑时返回inf软max 溢出. 这些都是浮点数量的"漏水抽象",每个种类都有标准的修复技巧.

您添加一个印表表. 记录在9000步骤上是好的.`inf`通过9 002 步骤,每个梯度是`nan`训练已经结束了.
> 你加了一个印记. 记录在第9,000步恢复正常.`inf`到了第九百零二步,所有的梯度都是`nan`训练已经死了.

您的模型已经完成,但精度比纸质要求差了2%.您检查了一切. 建筑匹配. 超参数匹配. 数据匹配. 问题是纸质使用 float32 而您使用 float16 没有正确的扩展. 32 位积累的圆形错误食了您的精度.
> 或:模型训练完成,但精度比论文差 2%――你检查了一切――结构匹配,超参数匹配,数据匹配――问题是论文使用 float32,你使用 float16 但没有正确的缩放――

它们可以在小的日志上运行. 当日志超过100时,它会返回.`inf`软max过了,因为`exp(100)`任何ML框架都用两行技巧来处理这个.你不知道这个技巧存在.
> 或:你从头实现交叉损失──小登录时正常──当登录时超过100回归时`inf`,因为,因为.`exp(100)`超过了 float32 的表示范围.

编号稳定不是一个理论问题.这是成功和沉默失败的训练运行之间的区别.你将对每一个严重的 ML 错误进行调试,最终会变成浮动点.
> 数值稳定性不是理论问题――它是训练成功与沉默失败之间的区别――你调试的每一个严重的 ML 错误最终都归结为浮点数――

## 概念的核心概念

> **【拓展：Softmax 的数值稳定技巧是面试必考题】**原始软max:`softmax(x) = exp(x) / sum(exp(x))`解法:减去最大值`softmax(x) = exp(x - max(x)) / sum(exp(x - max(x)))`结果不变,但数值稳定.`F.cross_entropy`内部使用日志软度最大而非分开计算,就是这个原因.

### 计算机如何存储实数?

计算机以IEEE 754标准的浮点值存储实数.浮点有三个部分:一个标志位,一个指数和一个 mantissa (含义和).
> 计算机根据IEEE 754标准将实数存储为浮点值――浮点数有三部分:符号位、指数和尾数――

```
Float32 layout (32 bits total):
[1 sign] [8 exponent] [23 mantissa]

Value = (-1)^sign * 2^(exponent - 127) * 1.mantissa
```

分数决定了精度 (有多少个重要数字). 指数决定了范围 (一个数字可以多大或小).
> 尾数决定精度 ((多少有效数字),指数决定范围 ((数字可以多大或多小) 👇

```
Format     Bits   Exponent  Mantissa  Decimal digits  Range (approx)
float64    64     11        52        ~15-16          +/- 1.8e308
float32    32     8         23        ~7-8            +/- 3.4e38
float16    16     5         10        ~3-4            +/- 65,504
bfloat16   16     8         7         ~2-3            +/- 3.4e38
```

float32给你准确度约7个十位数. float16给你大约3个数字. bfloat16是谷歌对 float16的范围问题的答案--与 float32相同的8位指数,但只有7位 mantissa.
> 浮动32 给你约7位进制精度──浮动16 约3位──bfloat16 是谷歌对浮动16 范围问题的答案 与浮动32 相等的8位指数,但只有7位尾数──训练神经网络时范围比精度更重要,所以浮动16 通常更优良──

### 为什么0.1加 0.2!=0.3?为什么0.1加 0.2!=0.3?

在二进制浮点中,0.1号是不能完全表示的.在基 2,它是重复的分数. Float32将这个分数缩小到23位的 mantissa.
> 0.1 在二进制浮点中不能精确表示──它是循环小数──浮点32将其切断为23位尾数──

```
In Python:
>>> 0.1 + 0.2
0.30000000000000004

>>> 0.1 + 0.2 == 0.3
False
```

这对 ML 很重要,因为: (1) 损失比较`if loss < threshold`它们可以给出错误的答案. (2) 积累许多小值从真实数量中偏离. (3) 如果比较浮动的数量与`==`解决方案:永远不要比较浮动机`==`使用`abs(a - b) < epsilon`或`math.isclose()`现在,我们要去.
> 这对 ML 很重要: 1) 损失比较可能出错.`==`试验和测试会失败.`==`比较浮点数量.

### 灾难性抵消

当你减去两个几乎相同的浮点数, 显著数字取消,
> 当你减小两个近似相等浮点数时,有效数字抵消, 噪音被提升为前导数字.

```
a = 1.0000001    (stored as 1.00000011920929 in float32)
b = 1.0000000    (stored as 1.00000000000000 in float32)

True difference:  0.0000001
Computed:         0.00000011920929

Relative error: 19.2%
```

解决方案:重新安排公式以避免减小大,几乎相同的数量.
> 修复:重新排列公式以避免相减大近似相等数量.

### 过流和下流 溢出和下流

过度流动发生在一个结果太大,不能表现出来时.
> 溢出是结果太大不能表示,下溢是结果太小.

```
Float32 boundaries:
  Maximum:  3.4028235e+38
  Overflow:  anything > 3.4e38 becomes inf
  Underflow: anything < 1.4e-45 becomes 0.0

exp(88.7)  = 3.40e+38   (barely fits in float32)
exp(89.0)  = inf         (overflow)
```

在ML中,`exp()`在软max,sigmoid和概率计算中出现. `log()`它们在交叉化,日志概率和KL分离中出现.
> 在ML中,`exp()`现在软max,sigmoid和概率计算中.`log()`现在交叉、对数似然和 KL 散度中

### 记账总和出口技巧

计算`log(sum(exp(x_i)))`技巧是从数值中减去最大值.
> 直接计算`log(sum(exp(x_i)))`技巧:在指数化之前减去最大值.

```
log(sum(exp(x_i))) = max(x) + log(sum(exp(x_i - max(x))))
```

为什么这有效:减去后`max(x)`它们的最大指数是`exp(0) = 1`总数至少是1个,所以总数至少是1个,`log(1) = 0`没有下流到`-inf`现在,我们可以.
> 为什么有效:减去`max(x)`后,最大指数是`exp(0) = 1`△不可能溢出──至少一个为1,所以和至少为1,`log(1) = 0`不可能下溢到`-inf`,我知道.

这种技巧在ML中出现了:软max正常化,交叉缩损失,日记概率总和,高西人混合,变化推理.
> 这种技巧在ML中无处不在:软max 归结,交叉损失,对数概率求和高斯混合,变分推断.

### 为什么软max需要最大减法技巧

如果没有这个技巧, [100, 101, 102] 的逻辑会导致溢出.
> 没有技巧时,引发溢出. 有技巧时,减去最大的 (x) = 102.

```
exp(100 - 102) = exp(-2) = 0.135
exp(101 - 102) = exp(-1) = 0.368
exp(102 - 102) = exp(0)  = 1.000
sum = 1.503

softmax = [0.090, 0.245, 0.665]
```

计算是安全的,这不是优化,这是准确的要求.
> 概率完全相同. 计算安全. 这不是优化,而是正确的必要条件.

### 检测和预防

`nan`其他`inf`通过计算传播病毒.`nan`在梯度更新中,重量增加了`nan`后续的输出`nan`训练在一个步骤内就死了.
> `nan`和 `inf`通过计算病毒式传播.`nan`使权重变为`nan`让后续所有输出变为`nan`练步就死了.

如何?`nan`显示:`0.0 / 0.0`现在`inf - inf`现在`inf * 0`现在`sqrt()`负值`log()`预防: 门输入`exp()`增加epsilon到分号,使用稳定实现,梯度剪切.
> `nan`如何出现:`0.0/0.0`,我知道.`inf-inf`,我知道.`inf*0`≠负数的`sqrt()`≠负数的`log()`预防:限制`exp()`输入、给分母加epsilon、使用稳定实现、梯度剪切──

### 数字级别检查

分析梯度 (从后延伸) 可能存在错误. 数字梯度检查通过计算有限差异的梯度来验证它们.
> 解析梯度 (来自反向传播) 可能有错误.

```
df/dx ~= (f(x + h) - f(x - h)) / (2h)
```

基本规则: relative_error < 1e-7:完美; < 1e-5:可接受; > 1e-3:有什么不对; > 1:完全错误.
> 经验法则:相对误差 < 1e-7:完美;< 1e-5:可接受;> 1e-3:有问题;> 1:完全错误──

### 混合精度训练

现代GPU具有子芯,可以比float32计算2-8倍的矩阵乘法.
> 现代GPU 有度核心,浮16矩阵乘法比浮32快 2-8倍――混合精度训练利用这一点――

```
1. Maintain float32 master copy of weights
2. Forward pass in float16 (fast)
3. Compute loss in float32 (prevents overflow)
4. Backward pass in float16 (fast)
5. Scale gradients to float32
6. Update float32 master weights
```

浮动16下流的解决方案是损失缩小:乘以大规模因素的损失,倒流计算更大的梯度,在更新权重之前按尺度划分.
> 变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变量变化变量变量变量变化变量变量变量变量变量变量变量变量变化变量变量变量变量变量变变量变量变量变变量变量变

### 球16对球16:为什么球16 胜出训练

16具有更高精度 (10 mantissa 位),但范围有限 (最高65,504). bfloat16具有更少的精度,但与 float32 (最高3.4e38) 的范围相同.
> 精度更高 (最大~65,504) ◎bfloat16 精度较低但范围与 float32 相同 (最大~3.4e38) ◎训练时范围更重要──

### 渐进的剪裁

爆炸梯度发生在梯度增长指数.两种剪辑:按值剪辑 (按每个元素粘贴) 和按标准剪辑 (按整个向量尺度,使其标准不超过门).按标准剪辑保持梯度方向.这是什么`torch.nn.utils.clip_grad_norm_()`没有.
> 梯度爆炸发生在梯度指数增长时――两种剪裁:按值剪裁 (限制每个元素) 和按范数剪裁 (缩小整个向量使范数不超过值)――按范数剪裁保留梯度方向――

典型值:`max_norm=1.0`对于变压器`max_norm=0.5`对于RL,`max_norm=5.0`对于更简单的网络.
> 典型值:变压器 用`max_norm=1.0`没有什么.`max_norm=0.5`简单网络使用`max_norm=5.0`,我知道.

### 常见的ML数值错误

**Bug: Loss is NaN after a few epochs.**原因: 位太大,软max过度流动. 解决:使用稳定的软max,降低学习速度,增加梯度剪辑.
> **Bug: 几个 epoch 后 loss 变 NaN。**原因:logits 太大,软max 溢出──修复:使用稳定软max,降低学习率,添加梯度剪剪──

**Bug: Validation accuracy is lower by 1-3%.**原因:不需要适当的损失扩展,混合精度. 修正:启用动态损失扩展,或切换到bfloat16.
> **Bug: 验证精度低 1-3%。**原因:混合精度没有正确的损失缩放.

**Bug: `exp()` returns `inf` in loss computation.**修复:使用`torch.nn.functional.log_softmax()`内部实现了总数计算.
> **Bug: 损失计算中 `exp()` 返回 `inf`。**修复:使用`torch.nn.functional.log_softmax()`,我知道.

## 建立它,实现它.

### 演示浮点精度限制.
**Bug: Validation accuracy is lower than expected by 1-3%.**
原因:不需要适当的损失扩展, 渐进的下流将默默地消除小更新.
修复:启用动态损失扩展,或切换到bfloat16.

**Bug: Gradient norms are 0.0 for some layers.**
原因:死于RLU神经元 (所有输入都是负),或浮16下流.
修复:使用LeakyReLU或GELU,使用梯度扩展,检查重量初始化.

**Bug: Model works on one GPU but gives different results on another.**
原因:非确定性浮点积累顺序.GPU平行减小在不同硬件上的不同顺序中总和,而浮点加算是不相关的.
解决问题:接受小差异 (1e-6),或设定`torch.use_deterministic_algorithms(True)`接受速度罚款.

**Bug: `exp()` returns `inf` in loss computation.**
原因:原材料被转移到`exp()`没有最大减法技巧.
修复:使用`torch.nn.functional.log_softmax()`内部实现了总数计算.

**Bug: Training diverges after switching from float32 to float16.**
原因: float16不能代表6e-8以下的梯度大小或超过65,504的激活.
修复:使用混合精度与损失扩展 (AMP) 或使用bfloat16代替.

```figure
logsumexp-stability
```

## 建立它

### 步骤1:展示浮点精度限制

```python
print("=== Floating Point Precision ===")
print(f"0.1 + 0.2 = {0.1 + 0.2}")
print(f"0.1 + 0.2 == 0.3? {0.1 + 0.2 == 0.3}")
print(f"Difference: {(0.1 + 0.2) - 0.3:.2e}")
```

### 实现简单和稳定的软max

```python
import math

def softmax_naive(logits):
    exps = [math.exp(z) for z in logits]
    total = sum(exps)
    return [e / total for e in exps]

def softmax_stable(logits):
    max_logit = max(logits)
    exps = [math.exp(z - max_logit) for z in logits]
    total = sum(exps)
    return [e / total for e in exps]

safe_logits = [2.0, 1.0, 0.1]
print(f"Naive:  {softmax_naive(safe_logits)}")
print(f"Stable: {softmax_stable(safe_logits)}")

dangerous_logits = [100.0, 101.0, 102.0]
print(f"Stable: {softmax_stable(dangerous_logits)}")
# softmax_naive(dangerous_logits) would return [nan, nan, nan]
```

### 实现稳定的日志总和解释

```python
def logsumexp_stable(values):
    c = max(values)
    return c + math.log(sum(math.exp(v - c) for v in values))
```

### 实现稳定的交叉

```python
def cross_entropy_stable(true_class, logits):
    max_logit = max(logits)
    shifted = [z - max_logit for z in logits]
    log_sum_exp = math.log(sum(math.exp(s) for s in shifted))
    log_prob = shifted[true_class] - log_sum_exp
    return -log_prob
```

### 步骤5: 梯度检查

```python
def numerical_gradient(f, x, h=1e-5):
    grad = []
    for i in range(len(x)):
        x_plus = x[:]
        x_minus = x[:]
        x_plus[i] += h
        x_minus[i] -= h
        grad.append((f(x_plus) - f(x_minus)) / (2 * h))
    return grad

def check_gradient(analytical, numerical, tolerance=1e-5):
    for i, (a, n) in enumerate(zip(analytical, numerical)):
        denom = max(abs(a), abs(n), 1e-8)
        rel_error = abs(a - n) / denom
        status = "OK" if rel_error < tolerance else "FAIL"
        print(f"  param {i}: analytical={a:.8f} numerical={n:.8f} "
              f"rel_error={rel_error:.2e} [{status}]")
```

## 用它实现框架

看到`code/numerical.py`对于所有证明的边缘情况的完整实施.
> 完整实现见`code/numerical.py`,我知道.

```python
# 梯度裁剪
def clip_by_norm(gradients, max_norm):
    total_norm = math.sqrt(sum(g**2 for g in gradients))
    if total_norm > max_norm:
        scale = max_norm / total_norm
        return [g * scale for g in gradients]
    return gradients

# NaN/Inf 检测
def check_tensor(name, values):
    has_nan = any(math.isnan(v) for v in values)
    has_inf = any(math.isinf(v) for v in values)
    if has_nan or has_inf:
        print(f"WARNING {name}: nan={has_nan} inf={has_inf}")
        return False
    return True
```

## 运送它.

这一课产生了:
> 本课程产出:

- `code/numerical.py`具有稳定的软max,日志总和exp,交叉透,梯度检查和混合精度模拟
  包含稳定软max,log-sum-exp,交叉,梯度检查和混合精度模拟
- `outputs/prompt-numerical-debugger.md`对于培训中诊断NAN/Inf和数值问题
  用于诊断训练中 NaN/Inf 和数值问题

## 练习题

1. **Catastrophic cancellation.**通过简单公式计算[1000000.0, 1000001.0, 1000002.0]的差异`E[x^2] - E[x]^2`然后使用韦尔福德的在线算法计算它.
   **灾难性抵消。**用简单公式和威尔福德算法计算 [1000000.0, 1000001.0, 1000002.0] 的方差,比较误差──

2. **Precision hunt.**找到最小的正值 float32 `x`这样.`1.0 + x == 1.0`检查是否符合`numpy.finfo(numpy.float32).eps`现在,我们要去.
   **精度搜索。**找到使`1.0 + x == 1.0`最小正值的浮动32 值.

3. **Log-sum-exp edge cases.**测试你的`logsumexp_stable`函数: (a) 所有值均等, (b) 一个值比其余值大得多, (c) 所有值非常负 (-1000).
   **Log-sum-exp 边界情况。**测试稳定日记总和exp 在极端输入下表现

4. **Gradient checking a neural network layer.**实现单一线性层`y = Wx + b`检查3×2重量矩阵的正确性.
   **梯度检查神经网络层。**实现单层线性层并验证正确性.

5. **Loss scaling experiment.**模拟训练使用浮动16:测量梯度的哪个部分变为零. 然后应用损失规模和测量再次.
   **损失缩放实验。**模拟浮动16 训练,测量梯度变为零的比例,然后应用损失缩放再测量――

## 关键词 快速查找表

| Term / 术语 | What people say | What it actually means / 实际含义 |
|------|----------------|----------------------|
| IEEE 754 | "The float standard" | International standard defining binary floating point formats. / 定义二进制浮点格式的国际标准。 |
| Machine epsilon / 机器精度 | "The precision limit" | The smallest value e such that 1.0 + e != 1.0. For float32, ~1.19e-7. / 使 1.0 + e != 1.0 的最小值。float32 约 1.19e-7。 |
| Catastrophic cancellation / 灾难性抵消 | "Precision loss from subtraction" | Significant digits cancel when subtracting nearly equal numbers. / 相减近似相等数时有效数字抵消。 |
| Overflow / 溢出 | "Number too big" | A result exceeds the maximum representable value and becomes inf. / 结果超过最大可表示值变为 inf。 |
| Underflow / 下溢 | "Number too small" | A result is closer to zero than the smallest representable positive number. / 结果比最小可表示正数更接近零。 |
| Log-sum-exp trick / Log-sum-exp 技巧 | "Subtract the max first" | Computing log(sum(exp(x))) by factoring out exp(max(x)). / 通过提取 exp(max(x)) 计算 log(sum(exp(x)))。 |
| Stable softmax / 稳定 softmax | "Softmax that does not explode" | Subtracting max(logits) before exponentiating. / 指数化前减去最大 logit。 |
| Gradient checking / 梯度检查 | "Verify your backprop" | Comparing analytical vs numerical gradients to catch bugs. / 比较解析和数值梯度以捕获 bug。 |
| Mixed precision / 混合精度 | "Float16 forward, float32 backward" | Using lower-precision for speed, higher-precision for accuracy. / 低精度加速，高精度保准确。 |
| Loss scaling / 损失缩放 | "Prevent gradient underflow" | Multiplying loss by a large constant to keep gradients in float16 range. / 将损失乘以大常数使梯度保持在 float16 范围内。 |
| bfloat16 | "Brain floating point" | Google's 16-bit format with 8 exponent bits. Preferred for training. / Google 的 16 位格式，8 位指数。训练首选。 |
| Gradient clipping / 梯度裁剪 | "Cap the gradient norm" | Scaling the gradient vector so its norm does not exceed a threshold. / 缩放梯度向量使范数不超过阈值。 |
| NaN | "Not a Number" | Special float value from undefined operations. Propagates through all arithmetic. / 未定义操作的特殊浮点值。通过所有算术传播。 |
| Inf | "Infinity" | Special float value from overflow or division by zero. / 溢出或除零产生的特殊浮点值。 |
| Numerical gradient / 数值梯度 | "Brute force derivative" | Approximating a derivative by evaluating f(x+h) and f(x-h). / 通过求 f(x+h) 和 f(x-h) 近似导数。 |

## 继续阅读 继续阅读

- [What Every Computer Scientist Should Know About Floating-Point Arithmetic (Goldberg 1991)](https://docs.oracle.com/cd/E19957-01/806-3568/ncg_goldberg.html)--最终引用
  浮点算术权威参考
- [Mixed Precision Training (Micikevicius et al., 2018)](https://arxiv.org/abs/1710.03740)关于损失扩展的NVIDIA论文
  美国国家经济发展部
- [AMP: Automatic Mixed Precision (PyTorch docs)](https://pytorch.org/docs/stable/amp.html)-- 实际指南
  混合精度实践指南
- [bfloat16 format (Google Cloud TPU docs)](https://cloud.google.com/tpu/docs/bfloat16)-- 为什么谷歌选择了这个格式
  谷歌选择bfloat16 的原因
- [Kahan Summation (Wikipedia)](https://en.wikipedia.org/wiki/Kahan_summation_algorithm)-- 减少圆形错误的算法
  减少进差的卡汉求和算法
