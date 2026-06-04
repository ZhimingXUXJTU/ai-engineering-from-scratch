# 调试神经网络

> 网络编译了、运行了、输出了数字——但数字是错的，没有报错信息。欢迎来到最难的调试——没有错误信息的调试。

**类型：** 实践
**语言：** Python、PyTorch
**前置知识：** Phase 03 第 01-10 课（特别是反向传播、损失函数、优化器）
**预计时间：** ~90 分钟

## 学习目标

- 使用系统化调试策略诊断常见神经网络故障（NaN 损失、平坦损失曲线、过拟合、振荡）
- 应用"过拟合单 batch"技术验证模型架构和训练循环正确
- 检查梯度幅度、激活分布和权重范数，识别梯度消失/爆炸问题
- 构建涵盖数据管道、模型架构、损失函数、优化器和学习率问题的调试清单

## 问题引入

传统软件坏了会崩溃。空指针抛异常。类型不匹配在编译时失败。

神经网络不会给你这种奢侈。一个坏掉的神经网络运行到完成，打印损失值，输出预测。损失可能在下降。预测可能看起来合理。但模型在悄悄地错——学习捷径、记忆噪声、或收敛到无用的局部极小值。Google 研究人员估计 60-70% 的 ML 调试时间花在"静默"bug 上——不产生错误但降低模型质量。

最常见的三个坑：忘记 zero_grad()、维度转置错误、学习率差 10 倍。

## 核心概念

### 调试心态

黄金法则：**从最简单的情况开始，每次只加一个组件，独立验证每个组件。**

### 症状 1：Loss 不下降

最常见的问题。训练循环运行，epoch 过去，损失保持平坦或剧烈振荡。

- **学习率错误**——太高：振荡或跳到 NaN。太低：下降极慢。
- **死亡 ReLU**——如果 ReLU 神经元接收到大负输入，输出 0，梯度 0，永远不再激活。
- **梯度消失**——sigmoid/tanh 网络中梯度逐层指数缩小。
- **梯度爆炸**——梯度逐层指数增长。损失跳到 NaN。

### 症状 2：Loss 下降但模型不好

- **过拟合**——训练准确率 99% 但测试 55%。加 dropout、权重衰减、更多数据。
- **数据泄漏**——测试数据泄漏到训练中。准确率异常地高。
- **标签错误**——大多数真实数据集中 5-10% 的标签是错的。

### 症状 3：NaN 或 Inf

- **学习率太高**——梯度更新过大，权重爆炸。
- **log(0)**——交叉熵计算 `log(p)`，如果 p=0 则爆炸。加 epsilon。
- **除以零**——BatchNorm 除以标准差，常数批次 std=0。
- **数值溢出**——大激活值输入 `exp()` 产生 Inf。减去最大值再指数化。

### 技术 1：梯度检查

将解析梯度（反向传播）与数值梯度（有限差分）比较。如果 `rel_diff < 1e-5`：正确。如果 `rel_diff > 1e-3`：几乎肯定是 bug。

### 技术 2：激活统计

监控每层训练时激活的均值和标准差。

| 健康指标 | 均值 | 标准差 | 诊断 |
|---------|------|--------|------|
| 健康 | ~0 | ~1 | 网络正常学习 |
| 饱和 | >>0 或 <<0 | ~0 | 激活卡在极端值 |
| 死亡 | 0 | 0 | 神经元全部为零 |
| 爆炸 | >>10 | >>10 | 激活无界增长 |

### 技术 3：过拟合单 batch 测试

深度学习中最重要的调试技术。取一个小 batch（8-32 样本），训练 100+ 次迭代。损失应接近零，训练准确率应达 100%。如果不能，你的模型或训练循环有根本性 bug——不要继续完整训练。

### 技术 4：学习率搜索器

从一个极小的 lr（1e-7）到一个极大的 lr（10）扫描一个 epoch，记录损失。最优学习率大约是损失开始最快下降处的 10 倍以下。

### 常见 PyTorch 错误

| 错误 | 症状 | 修复 |
|-----|------|------|
| 忘记 `optimizer.zero_grad()` | 梯度跨批量累积，损失振荡 | 在 `loss.backward()` 前添加 |
| 忘记 `model.eval()` | 测试准确率在不同运行间波动 | 添加 `model.eval()` 和 `torch.no_grad()` |
| 错误的张量形状 | 静默广播产生错误结果 | 调试时在每个操作后打印形状 |
| CPU/GPU 不匹配 | `RuntimeError: expected CUDA tensor` | 对模型和数据都用 `.to(device)` |
| 不分离张量 | 计算图永远增长，OOM | 使用 `.detach()` 或 `with torch.no_grad()` |
| 数据未归一化 | 损失卡在随机水平 | 将输入归一化为 mean=0, std=1 |

### 调试总表

| 症状 | 可能原因 | 首先尝试 |
|------|---------|---------|
| 损失卡在 -log(1/num_classes) | 模型预测均匀分布 | 检查数据管道 |
| 几步后 NaN | 学习率太高 | 降低 10 倍 |
| 立即 NaN | log(0) 或除以零 | 添加 epsilon |
| 损失剧烈振荡 | lr 太高或批量太小 | 降低 lr，增大批量 |
| 训练高测试低 | 过拟合 | 加 dropout、权重衰减 |
| 梯度全零 | 死亡 ReLU 或分离的计算图 | 换 LeakyReLU |

## 动手实现

### NetworkDebugger 类

```python
class NetworkDebugger:
    def __init__(self, model):
        self.model = model
        self.activation_stats = {}
        self.gradient_stats = {}
        self.loss_history = []
        self.hooks = []
        self._register_hooks()

    def _register_hooks(self):
        for name, module in self.model.named_modules():
            if isinstance(module, (nn.Linear, nn.Conv2d, nn.ReLU)):
                hook = module.register_forward_hook(self._make_activation_hook(name))
                self.hooks.append(hook)
                hook = module.register_full_backward_hook(self._make_gradient_hook(name))
                self.hooks.append(hook)

    def check_loss_health(self):
        if any(math.isnan(v) for v in self.loss_history[-10:]):
            return "NAN_OR_INF"
        if self.loss_history[-1] >= self.loss_history[0] * 0.99:
            return "NOT_DECREASING"
        return "HEALTHY"
```

### 过拟合单 batch 测试

```python
def overfit_one_batch(model, x_batch, y_batch, criterion, lr=0.01, steps=200):
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    model.train()
    for step in range(steps):
        optimizer.zero_grad()
        output = model(x_batch)
        loss = criterion(output, y_batch)
        loss.backward()
        optimizer.step()
    return loss.item() < 0.1  # 通过：损失 < 0.1
```

### 学习率搜索器

从 1e-7 到 10 指数增长 lr，记录损失，找到最优 lr。

## 用框架实现

```python
# PyTorch 内置调试
with torch.autograd.detect_anomaly():
    output = model(input_tensor)
    loss = criterion(output, target)
    loss.backward()

for name, param in model.named_parameters():
    if param.grad is not None:
        print(f"{name}: grad_mean={param.grad.abs().mean():.2e}")
```

生产环境用 Weights & Biases (wandb) 或 TensorBoard 实时监控。

### 调试清单（完整训练前）

1. 运行过拟合单 batch 测试。如果失败，停止。
2. 打印模型摘要——验证参数量合理。
3. 用随机数据跑一次前向传播——检查输出形状。
4. 训练 5 个 epoch——验证损失下降。
5. 检查激活统计——无死亡层、无爆炸。
6. 检查梯度流——无消失、无爆炸。
7. 验证数据管道——打印 5 个随机样本及标签。

## 练习题

1. 添加梯度爆炸检测器，自动建议梯度裁剪值。
2. 构建死亡神经元复活器：识别死亡 ReLU 神经元并用 Kaiming 重新初始化。
3. 实现带绘图的学习率搜索器，找到 ResNet-18 在 CIFAR-10 上的最优 lr。
4. 创建数据管道验证器：检查重复样本、标签不平衡、归一化、NaN 值。
5. 在迷你框架中引入一个隐蔽 bug，用梯度检查定位。

## 术语速查表

| 术语 | 通俗说法 | 实际含义 |
|------|---------|---------|
| 静默 bug | "能跑但结果差" | 不产生错误但降低模型质量的 bug |
| 死亡 ReLU | "神经元死了" | 输入永远为负的 ReLU 神经元，输出和梯度永远为零 |
| 梯度消失 | "前面几层不学了" | 梯度逐层指数缩小 |
| 梯度爆炸 | "Loss 变 NaN" | 梯度逐层指数增长 |
| 梯度检查 (Gradient checking) | "验证反向传播正确" | 对比解析梯度和数值梯度 |
| 过拟合单 batch | "最重要的调试测试" | 在单个小 batch 上训练验证模型能学习 |
| 学习率搜索器 (LR finder) | "扫一遍找最佳 lr" | 指数增长 lr 找到损失开始发散的点 |
| 数据泄漏 | "测试数据漏到训练里" | 测试集信息污染训练 |

## 延伸阅读

- Smith, "Cyclical Learning Rates for Training Neural Networks" (2017) —— 学习率范围测试
- Northcutt et al., "Pervasive Label Errors in Test Sets" (2021) —— 主要基准测试中 3-6% 标签错误
- Zhang et al., "Understanding Deep Learning Requires Rethinking Generalization" (2017) —— 神经网络可以记忆随机标签
