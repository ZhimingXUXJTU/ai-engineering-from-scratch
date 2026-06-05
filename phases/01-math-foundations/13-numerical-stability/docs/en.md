# Numerical Stability | 数值稳定性

> Floating point is a leaky abstraction. It will bite you during training, and you will not see it coming.
> 浮点数是漏水的抽象。它会在训练中咬你一口，而你不会看到它到来。

**Type:** Build | **类型:** 动手
**Language:** Python | **语言:** Python
**Prerequisites:** Phase 1, Lessons 01-04 | **前置知识:** Phase 1, Lessons 01-04
**Time:** ~120 minutes | **时间:** ~120 分钟

## Learning Objectives | 学习目标

- Implement numerically stable softmax and log-sum-exp using the max-subtraction trick
  用减最大值技巧实现数值稳定的 softmax 和 log-sum-exp
- Identify overflow, underflow, and catastrophic cancellation in floating-point computations
  识别浮点计算中的溢出、下溢和灾难性抵消
- Verify analytical gradients against numerical gradients using centered finite differences
  用中心有限差分验证解析梯度
- Explain why bfloat16 is preferred over float16 for training and how loss scaling prevents gradient underflow
  解释为什么 bfloat16 比 float16 更适合训练，以及损失缩放如何防止梯度下溢

> **【中文解读】**
> 浮点数是漏水的抽象。训练 3 小时后 loss 变 NaN 是最常见的崩溃。本章实现数值稳定的 Softmax（减最大值技巧），解释为什么 bfloat16 比 float16 更适合训练。混合精度训练中用 loss scaling 防止小梯度下溢。

## The Problem | 问题引入

> **【中文解读】** 三种典型的数值稳定性灾难：(1) 训练 3 小时后 loss 变 NaN——某步计算溢出了；(2) 精度比论文差 2%——float16 的累积舍入误差吃掉了准确率；(3) 自己写的交叉熵在大 logits 时返回 inf——softmax 溢出。这些都是浮点数的"漏水抽象"，每种都有标准的修复技巧。

You add a print statement. The logits are fine at step 9,000. At step 9,001 they are `inf`. By step 9,002 every gradient is `nan` and training is dead.
> 你加了一条 print。logits 在第 9,000 步还正常。第 9,001 步变成了 `inf`。到第 9,002 步所有梯度都是 `nan`，训练已经死了。

Or: your model trains to completion but accuracy is 2% worse than the paper claims. You check everything. Architecture matches. Hyperparameters match. Data matches. The problem is that the paper used float32 and you used float16 without the right scaling. Thirty-two bits of accumulated rounding error quietly ate your accuracy.
> 或者：模型训练完成但精度比论文差 2%。你检查了一切。架构匹配、超参数匹配、数据匹配。问题是论文用了 float32，你用了 float16 但没有正确的缩放。

Or: you implement cross-entropy loss from scratch. It works on small logits. When logits exceed 100, it returns `inf`. The softmax overflowed because `exp(100)` is larger than float32 can represent. Every ML framework handles this with a two-line trick. You did not know the trick existed.
> 或者：你从头实现交叉熵损失。小 logits 时正常。当 logits 超过 100 时返回 `inf`。softmax 溢出了，因为 `exp(100)` 超过了 float32 的表示范围。

Numerical stability is not a theoretical concern. It is the difference between a training run that succeeds and one that silently fails. Every serious ML bug you will debug eventually comes down to floating point.
> 数值稳定性不是理论问题。它是训练成功与静默失败之间的区别。你调试的每个严重 ML bug 最终都归结到浮点数。

## The Concept | 核心概念

> **【拓展：Softmax 的数值稳定技巧是面试必考题】** 原始 Softmax：`softmax(x) = exp(x) / sum(exp(x))`，当 x 中有大值时 exp 溢出。解法：减去最大值 `softmax(x) = exp(x - max(x)) / sum(exp(x - max(x)))`，数学结果不变但数值稳定。PyTorch 的 `F.cross_entropy` 内部使用 log-softmax 而非分开计算，就是这个原因。

### IEEE 754: How Computers Store Real Numbers | IEEE 754：计算机如何存储实数

Computers store real numbers as floating point values following the IEEE 754 standard. A float has three parts: a sign bit, an exponent, and a mantissa (significand).
> 计算机按照 IEEE 754 标准将实数存储为浮点值。浮点数有三部分：符号位、指数和尾数。

```
Float32 layout (32 bits total):
[1 sign] [8 exponent] [23 mantissa]

Value = (-1)^sign * 2^(exponent - 127) * 1.mantissa
```

The mantissa determines precision (how many significant digits). The exponent determines range (how large or small a number can be).
> 尾数决定精度（多少有效数字），指数决定范围（数字可以多大或多小）。

```
Format     Bits   Exponent  Mantissa  Decimal digits  Range (approx)
float64    64     11        52        ~15-16          +/- 1.8e308
float32    32     8         23        ~7-8            +/- 3.4e38
float16    16     5         10        ~3-4            +/- 65,504
bfloat16   16     8         7         ~2-3            +/- 3.4e38
```

float32 gives you about 7 decimal digits of precision. float16 gives you about 3 digits. bfloat16 is Google's answer to float16's range problem -- same 8-bit exponent as float32 but only 7 mantissa bits. For training neural networks, range matters more than precision, so bfloat16 usually wins.
> float32 给你约 7 位十进制精度。float16 约 3 位。bfloat16 是 Google 对 float16 范围问题的回答——与 float32 相同的 8 位指数但只有 7 位尾数。训练神经网络时范围比精度更重要，所以 bfloat16 通常更优。

### Why 0.1 + 0.2 != 0.3 | 为什么 0.1 + 0.2 != 0.3

The number 0.1 cannot be represented exactly in binary floating point. In base 2, it is a repeating fraction. Float32 truncates this to 23 bits of mantissa.
> 0.1 在二进制浮点中无法精确表示。它是循环小数。float32 将其截断为 23 位尾数。

```
In Python:
>>> 0.1 + 0.2
0.30000000000000004

>>> 0.1 + 0.2 == 0.3
False
```

This matters for ML because: (1) Loss comparisons like `if loss < threshold` can give wrong answers. (2) Accumulating many small values drifts from the true sum. (3) Checksums and reproducibility tests fail if you compare floats with `==`. The fix: never compare floats with `==`. Use `abs(a - b) < epsilon` or `math.isclose()`.
> 这对 ML 很重要：(1) 损失比较可能出错。(2) 累积许多小值会偏离真实和。(3) 用 `==` 比较浮点数的校验和测试会失败。修复：永远不要用 `==` 比较浮点数。

### Catastrophic Cancellation | 灾难性抵消

When you subtract two nearly equal floating point numbers, the significant digits cancel and you are left with rounding noise promoted to leading digits.
> 当你相减两个近似相等的浮点数时，有效数字抵消，舍入噪声被提升为前导数字。

```
a = 1.0000001    (stored as 1.00000011920929 in float32)
b = 1.0000000    (stored as 1.00000000000000 in float32)

True difference:  0.0000001
Computed:         0.00000011920929

Relative error: 19.2%
```

The fix: rearrange formulas to avoid subtracting large, nearly equal numbers. For variance, use the Welford algorithm or center the data first.
> 修复：重新排列公式以避免相减大型近似相等的数。计算方差时用 Welford 算法或先中心化数据。

### Overflow and Underflow | 溢出与下溢

Overflow happens when a result is too large to represent. Underflow happens when it is too small.
> 溢出是结果太大无法表示，下溢是结果太小。

```
Float32 boundaries:
  Maximum:  3.4028235e+38
  Overflow:  anything > 3.4e38 becomes inf
  Underflow: anything < 1.4e-45 becomes 0.0

exp(88.7)  = 3.40e+38   (barely fits in float32)
exp(89.0)  = inf         (overflow)
```

In ML, `exp()` appears in softmax, sigmoid, and probability computations. `log()` appears in cross-entropy, log-likelihoods, and KL divergence.
> 在 ML 中，`exp()` 出现在 softmax、sigmoid 和概率计算中。`log()` 出现在交叉熵、对数似然和 KL 散度中。

### The Log-Sum-Exp Trick | Log-Sum-Exp 技巧

Computing `log(sum(exp(x_i)))` directly is numerically dangerous. The trick: subtract the maximum value before exponentiating.
> 直接计算 `log(sum(exp(x_i)))` 数值危险。技巧：在指数化之前减去最大值。

```
log(sum(exp(x_i))) = max(x) + log(sum(exp(x_i - max(x))))
```

Why this works: after subtracting `max(x)`, the largest exponent is `exp(0) = 1`. No overflow is possible. At least one term in the sum is 1, so the sum is at least 1, and `log(1) = 0`. No underflow to `-inf` is possible.
> 为什么有效：减去 `max(x)` 后，最大指数是 `exp(0) = 1`。不可能溢出。至少一项为 1，所以和至少为 1，`log(1) = 0`。不可能下溢到 `-inf`。

This trick appears everywhere in ML: softmax normalization, cross-entropy loss, log-probability summation, mixture of Gaussians, variational inference.
> 这个技巧在 ML 中无处不在：softmax 归一化、交叉熵损失、对数概率求和、高斯混合、变分推断。

### Why Softmax Needs the Max-Subtraction Trick | 为什么 Softmax 需要减最大值技巧

Without the trick, logits of [100, 101, 102] cause overflow. With the trick, subtract max(x) = 102:
> 没有技巧时，logits [100, 101, 102] 导致溢出。有技巧时，减去 max(x) = 102：

```
exp(100 - 102) = exp(-2) = 0.135
exp(101 - 102) = exp(-1) = 0.368
exp(102 - 102) = exp(0)  = 1.000
sum = 1.503

softmax = [0.090, 0.245, 0.665]
```

The probabilities are identical. The computation is safe. This is not an optimization. It is a requirement for correctness.
> 概率完全相同。计算安全。这不是优化，而是正确性的必要条件。

### NaN and Inf: Detection and Prevention | NaN 和 Inf：检测与预防

`nan` and `inf` propagate virally through computation. One `nan` in a gradient update makes the weight `nan`, which makes every subsequent output `nan`. Training is dead within one step.
> `nan` 和 `inf` 通过计算病毒式传播。梯度更新中的一个 `nan` 使权重变为 `nan`，使后续所有输出变为 `nan`。训练一步就死了。

How `nan` appears: `0.0 / 0.0`, `inf - inf`, `inf * 0`, `sqrt()` of negative, `log()` of negative. Prevention: clamp inputs to `exp()`, add epsilon to denominators, use stable implementations, gradient clipping.
> `nan` 如何出现：`0.0/0.0`、`inf-inf`、`inf*0`、负数的 `sqrt()`、负数的 `log()`。预防：限制 `exp()` 输入、给分母加 epsilon、使用稳定实现、梯度裁剪。

### Numerical Gradient Checking | 数值梯度检查

Analytical gradients (from backpropagation) can have bugs. Numerical gradient checking verifies them by computing gradients with finite differences.
> 解析梯度（来自反向传播）可能有 bug。数值梯度检查通过有限差分计算梯度来验证。

```
df/dx ~= (f(x + h) - f(x - h)) / (2h)
```

Rules of thumb: relative_error < 1e-7: perfect; < 1e-5: acceptable; > 1e-3: something is wrong; > 1: completely wrong.
> 经验法则：相对误差 < 1e-7：完美；< 1e-5：可接受；> 1e-3：有问题；> 1：完全错误。

### Mixed Precision Training | 混合精度训练

Modern GPUs have Tensor Cores that compute float16 matrix multiplications 2-8x faster than float32. Mixed precision training exploits this.
> 现代 GPU 有 Tensor Core，float16 矩阵乘法比 float32 快 2-8 倍。混合精度训练利用这一点。

```
1. Maintain float32 master copy of weights
2. Forward pass in float16 (fast)
3. Compute loss in float32 (prevents overflow)
4. Backward pass in float16 (fast)
5. Scale gradients to float32
6. Update float32 master weights
```

The fix for float16 underflow is loss scaling: multiply loss by a large scale factor, backward pass computes larger gradients, divide by scale before updating weights.
> float16 下溢的修复是损失缩放：将损失乘以大缩放因子，反向传播计算更大的梯度，更新权重前除以缩放因子。

### bfloat16 vs float16: Why bfloat16 Wins for Training | bfloat16 vs float16：为什么 bfloat16 在训练中胜出

float16 has more precision (10 mantissa bits) but limited range (max ~65,504). bfloat16 has less precision but the same range as float32 (max ~3.4e38). For training, range matters more. bfloat16 is preferred for training. float16 is preferred for inference.
> float16 精度更高（10 位尾数）但范围有限（最大 ~65,504）。bfloat16 精度较低但范围与 float32 相同（最大 ~3.4e38）。训练时范围更重要。

### Gradient Clipping | 梯度裁剪

Exploding gradients happen when gradients grow exponentially. Two types of clipping: clip by value (clamp each element) and clip by norm (scale entire vector so its norm does not exceed a threshold). Clip by norm preserves gradient direction. This is what `torch.nn.utils.clip_grad_norm_()` does.
> 梯度爆炸发生在梯度指数增长时。两种裁剪：按值裁剪（限制每个元素）和按范数裁剪（缩放整个向量使范数不超过阈值）。按范数裁剪保留梯度方向。

Typical values: `max_norm=1.0` for transformers, `max_norm=0.5` for RL, `max_norm=5.0` for simpler networks.
> 典型值：Transformer 用 `max_norm=1.0`，RL 用 `max_norm=0.5`，简单网络用 `max_norm=5.0`。

### Common ML Numerical Bugs | 常见 ML 数值 Bug

**Bug: Loss is NaN after a few epochs.** Cause: logits too large, softmax overflowed. Fix: use stable softmax, reduce learning rate, add gradient clipping.
> **Bug: 几个 epoch 后 loss 变 NaN。** 原因：logits 太大，softmax 溢出。修复：使用稳定 softmax，降低学习率，添加梯度裁剪。

**Bug: Validation accuracy is lower by 1-3%.** Cause: mixed precision without proper loss scaling. Fix: enable dynamic loss scaling, or switch to bfloat16.
> **Bug: 验证精度低 1-3%。** 原因：混合精度没有正确的损失缩放。修复：启用动态损失缩放，或切换到 bfloat16。

**Bug: `exp()` returns `inf` in loss computation.** Fix: use `torch.nn.functional.log_softmax()` which implements log-sum-exp internally.
> **Bug: 损失计算中 `exp()` 返回 `inf`。** 修复：使用 `torch.nn.functional.log_softmax()`。

## Build It | 动手实现

### Step 1: Demonstrate floating point precision limits | 第1步：演示浮点精度限制

```python
print("=== Floating Point Precision ===")
print(f"0.1 + 0.2 = {0.1 + 0.2}")
print(f"0.1 + 0.2 == 0.3? {0.1 + 0.2 == 0.3}")
print(f"Difference: {(0.1 + 0.2) - 0.3:.2e}")
```

### Step 2: Implement naive vs stable softmax | 第2步：实现朴素与稳定 softmax

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

### Step 3: Implement stable log-sum-exp | 第3步：实现稳定的 log-sum-exp

```python
def logsumexp_stable(values):
    c = max(values)
    return c + math.log(sum(math.exp(v - c) for v in values))
```

### Step 4: Implement stable cross-entropy | 第4步：实现稳定的交叉熵

```python
def cross_entropy_stable(true_class, logits):
    max_logit = max(logits)
    shifted = [z - max_logit for z in logits]
    log_sum_exp = math.log(sum(math.exp(s) for s in shifted))
    log_prob = shifted[true_class] - log_sum_exp
    return -log_prob
```

### Step 5: Gradient checking | 第5步：梯度检查

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

## Use It | 用框架实现

See `code/numerical.py` for complete implementations with all edge cases demonstrated.
> 完整实现见 `code/numerical.py`。

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

## Ship It | 产出物

This lesson produces:
> 本课程产出：

- `code/numerical.py` with stable softmax, log-sum-exp, cross-entropy, gradient checking, and mixed precision simulation
  包含稳定 softmax、log-sum-exp、交叉熵、梯度检查和混合精度模拟
- `outputs/prompt-numerical-debugger.md` for diagnosing NaN/Inf and numerical issues in training
  用于诊断训练中 NaN/Inf 和数值问题

## Exercises | 练习题

1. **Catastrophic cancellation.** Compute the variance of [1000000.0, 1000001.0, 1000002.0] using the naive formula `E[x^2] - E[x]^2` in float32. Then compute it using Welford's online algorithm. Compare the errors against the true variance (0.6667).
   **灾难性抵消。** 用朴素公式和 Welford 算法计算 [1000000.0, 1000001.0, 1000002.0] 的方差，比较误差。

2. **Precision hunt.** Find the smallest positive float32 value `x` such that `1.0 + x == 1.0`. Verify it matches `numpy.finfo(numpy.float32).eps`.
   **精度搜索。** 找到使 `1.0 + x == 1.0` 的最小正 float32 值。

3. **Log-sum-exp edge cases.** Test your `logsumexp_stable` function with: (a) all values equal, (b) one value much larger than the rest, (c) all values very negative (-1000).
   **Log-sum-exp 边界情况。** 测试稳定 log-sum-exp 在极端输入下的表现。

4. **Gradient checking a neural network layer.** Implement a single linear layer `y = Wx + b` and verify correctness for a 3x2 weight matrix.
   **梯度检查神经网络层。** 实现单层线性层并验证正确性。

5. **Loss scaling experiment.** Simulate training with float16: measure what fraction of gradients become zero. Then apply loss scaling and measure again.
   **损失缩放实验。** 模拟 float16 训练，测量梯度变为零的比例，然后应用损失缩放再测量。

## Key Terms | 术语速查表

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

## Further Reading | 延伸阅读

- [What Every Computer Scientist Should Know About Floating-Point Arithmetic (Goldberg 1991)](https://docs.oracle.com/cd/E19957-01/806-3568/ncg_goldberg.html) -- the definitive reference
  浮点算术权威参考
- [Mixed Precision Training (Micikevicius et al., 2018)](https://arxiv.org/abs/1710.03740) -- the NVIDIA paper on loss scaling
  NVIDIA 损失缩放论文
- [AMP: Automatic Mixed Precision (PyTorch docs)](https://pytorch.org/docs/stable/amp.html) -- practical guide
  PyTorch 混合精度实践指南
- [bfloat16 format (Google Cloud TPU docs)](https://cloud.google.com/tpu/docs/bfloat16) -- why Google chose this format
  Google 选择 bfloat16 的原因
- [Kahan Summation (Wikipedia)](https://en.wikipedia.org/wiki/Kahan_summation_algorithm) -- algorithm for reducing rounding error
  减少舍入误差的 Kahan 求和算法
