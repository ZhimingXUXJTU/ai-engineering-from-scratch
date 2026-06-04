# 集成方法

> 一组弱学习器，正确组合后，就变成强学习器。这不是比喻，这是定理。

**类型：** 构建
**语言：** Python
**前置知识：** Phase 2 第 10 课（偏差-方差权衡）
**时长：** 约 120 分钟

## 学习目标

- 从零实现 AdaBoost 和梯度提升，解释 Boosting 如何串行减少偏差
- 构建 Bagging 集成，展示平均不相关模型如何在不增加偏差的情况下减少方差
- 比较 Bagging、Boosting 和 Stacking 各自针对的误差分量
- 评估集成多样性，解释为什么多数投票准确率随更多独立弱学习器而提高

## 问题引入

单棵决策树训练快、易解释，但会过拟合。单个线性模型在复杂边界上欠拟合。你可以花几天工程化完美的模型架构。或者你可以组合一堆不完美的模型，得到比任何单独一个都更好的结果。

集成方法做的就是这件事。它们是赢得 Kaggle 表格数据竞赛最可靠的技术，驱动着大多数生产 ML 系统，并生动展示了偏差-方差权衡。Bagging 减少方差。Boosting 减少偏差。Stacking 学习在不同输入上该信任哪个模型。

## 核心概念

### 为什么集成有效

假设你有 N 个独立分类器，每个准确率 p > 0.5。多数投票的准确率：

```
P(多数正确) = sum over k > N/2 of C(N,k) * p^k * (1-p)^(N-k)
```

对于 21 个各 60% 准确率的分类器，多数投票准确率约 74%。101 个分类器时升至 84%。当模型犯不同的错误时，错误互相抵消。

关键要求是**多样性**。如果所有模型犯相同的错误，组合它们毫无帮助。集成通过以下方式产生多样性：

- 不同的训练子集（Bagging）
- 不同的特征子集（随机森林）
- 串行错误纠正（Boosting）
- 不同的模型族（Stacking）

### Bagging（Bootstrap Aggregating）

Bagging 通过在每个 Bootstrap 样本上训练每个模型来创造多样性。一个 Bootstrap 样本是从原始数据中有放回抽样得到的，大小与原始数据相同。约 63.2% 的唯一样本出现在每个 Bootstrap 中。剩余的 36.8%（袋外样本）提供了免费的验证集。

Bagging 减少方差而不怎么增加偏差。每棵单独的树对其 Bootstrap 样本过拟合，但过拟合因树而异，所以平均后噪声被抵消。

**随机森林**是 Bagging 加上一个额外手法：每次分裂时只考虑随机子集的特征。这迫使树之间更多样化。典型的候选特征数对分类是 `sqrt(n_features)`，对回归是 `n_features / 3`。

### Boosting（串行错误纠正）

Boosting 串行训练模型。每个新模型关注前面模型犯错的样本。

Boosting 减少偏差。每个新模型纠正集成到目前为止的系统性错误。最终预测是所有模型的加权和，更好的模型获得更高权重。

权衡：如果运行太多轮，Boosting 会过拟合，因为它持续拟合困难样本，其中一些可能是噪声。

### AdaBoost

AdaBoost（自适应提升）是第一个实用的 Boosting 算法。它适用于任何基础学习器，通常用决策树桩（深度 1 的树）。

算法：

```
1. 初始化样本权重：w_i = 1/N

2. 对 t = 1 到 T:
   a. 在加权数据上训练弱学习器 h_t
   b. 计算加权错误率：
      err_t = sum(w_i * I(h_t(x_i) != y_i)) / sum(w_i)
   c. 计算模型权重：
      alpha_t = 0.5 * ln((1 - err_t) / err_t)
   d. 更新样本权重：
      w_i = w_i * exp(-alpha_t * y_i * h_t(x_i))
   e. 归一化权重使总和为 1

3. 最终预测：H(x) = sign(sum(alpha_t * h_t(x)))
```

错误率低的模型获得更高的 alpha。被误分类的样本获得更高的权重，使下一个模型更关注它们。

### 梯度提升

梯度提升将 Boosting 推广到任意损失函数。它不是重新加权样本，而是让每个新模型拟合当前集成的残差（损失的负梯度）。

```
1. 初始化：F_0(x) = argmin_c sum(L(y_i, c))

2. 对 t = 1 到 T:
   a. 计算伪残差：
      r_i = -dL(y_i, F_{t-1}(x_i)) / dF_{t-1}(x_i)
   b. 对残差 r_i 拟合一棵树 h_t
   c. 找最优步长：
      gamma_t = argmin_gamma sum(L(y_i, F_{t-1}(x_i) + gamma * h_t(x_i)))
   d. 更新：
      F_t(x) = F_{t-1}(x) + learning_rate * gamma_t * h_t(x)

3. 最终预测：F_T(x)
```

对于平方误差损失，伪残差就是实际残差：`r_i = y_i - F_{t-1}(x_i)`。每棵树字面上就在拟合之前集成的错误。

学习率（收缩）控制每棵树的贡献。更小的学习率需要更多树但泛化更好。典型值：0.01 到 0.3。

### XGBoost：为什么它统治表格数据

XGBoost（eXtreme Gradient Boosting）是带工程优化的梯度提升，使其快速、准确、抗过拟合：

- **正则化目标：** 叶子权重上的 L1 和 L2 惩罚防止单棵树过于自信
- **二阶近似：** 同时使用损失的一阶和二阶导数，给出更好的分裂决策
- **稀疏感知分裂：** 原生处理缺失值，在每个分裂点学习缺失数据的最佳方向
- **列子采样：** 像随机森林一样在每次分裂时采样特征以增加多样性
- **加权分位数草图：** 高效地在分布式数据上找连续特征的分裂点

对于表格数据，XGBoost（及其后继者 LightGBM）始终优于神经网络。如果你的数据适合放入行列的表格中，从梯度提升开始。

### Stacking（元学习）

Stacking 使用多个基础模型的预测作为元学习器的特征。

元学习器学习对哪些输入该信任哪个基础模型。如果随机森林在某些区域更好，SVM 在其他区域更好，元学习器会学会相应地路由。

为避免数据泄漏，基础模型预测必须通过训练集上的交叉验证生成。你绝不能在相同数据上训练基础模型并生成元特征。

### 投票

最简单的集成。直接组合预测。

- **硬投票：** 对类别标签多数投票。
- **软投票：** 平均预测概率，选平均概率最高的类别。通常更好，因为它使用了置信度信息。

## 动手实现

### 步骤 1：决策树桩（基础学习器）

```python
class DecisionStump:
    def __init__(self):
        self.feature_idx = None
        self.threshold = None
        self.polarity = 1
        self.alpha = None

    def fit(self, X, y, weights):
        n_samples, n_features = X.shape
        best_error = float("inf")

        for f in range(n_features):
            thresholds = np.unique(X[:, f])
            for thresh in thresholds:
                for polarity in [1, -1]:
                    pred = np.ones(n_samples)
                    pred[polarity * X[:, f] < polarity * thresh] = -1
                    error = np.sum(weights[pred != y])
                    if error < best_error:
                        best_error = error
                        self.feature_idx = f
                        self.threshold = thresh
                        self.polarity = polarity

    def predict(self, X):
        n = X.shape[0]
        pred = np.ones(n)
        idx = self.polarity * X[:, self.feature_idx] < self.polarity * self.threshold
        pred[idx] = -1
        return pred
```

### 步骤 2：从零实现 AdaBoost

```python
class AdaBoostScratch:
    def __init__(self, n_estimators=50):
        self.n_estimators = n_estimators
        self.stumps = []
        self.alphas = []

    def fit(self, X, y):
        n = X.shape[0]
        weights = np.full(n, 1 / n)

        for _ in range(self.n_estimators):
            stump = DecisionStump()
            stump.fit(X, y, weights)
            pred = stump.predict(X)

            err = np.sum(weights[pred != y])
            err = np.clip(err, 1e-10, 1 - 1e-10)

            alpha = 0.5 * np.log((1 - err) / err)
            weights *= np.exp(-alpha * y * pred)
            weights /= weights.sum()

            stump.alpha = alpha
            self.stumps.append(stump)
            self.alphas.append(alpha)

    def predict(self, X):
        total = sum(a * s.predict(X) for a, s in zip(self.alphas, self.stumps))
        return np.sign(total)
```

### 步骤 3：从零实现梯度提升

```python
class GradientBoostingScratch:
    def __init__(self, n_estimators=100, learning_rate=0.1, max_depth=3):
        self.n_estimators = n_estimators
        self.lr = learning_rate
        self.max_depth = max_depth
        self.trees = []
        self.initial_pred = None

    def fit(self, X, y):
        self.initial_pred = np.mean(y)
        current_pred = np.full(len(y), self.initial_pred)

        for _ in range(self.n_estimators):
            residuals = y - current_pred
            tree = SimpleRegressionTree(max_depth=self.max_depth)
            tree.fit(X, residuals)
            update = tree.predict(X)
            current_pred += self.lr * update
            self.trees.append(tree)

    def predict(self, X):
        pred = np.full(X.shape[0], self.initial_pred)
        for tree in self.trees:
            pred += self.lr * tree.predict(X)
        return pred
```

完整实现和比较见 `code/ensembles.py`。

## 用框架实现

### 何时用哪种方法

| 方法 | 减少 | 适合 | 注意 |
|------|------|------|------|
| Bagging / 随机森林 | 方差 | 噪声数据，多特征 | 不帮助偏差 |
| AdaBoost | 偏差 | 干净数据，简单基础学习器 | 对离群值和噪声敏感 |
| 梯度提升 | 偏差 | 表格数据，竞赛 | 训练慢，不调参容易过拟合 |
| XGBoost / LightGBM | 两者 | 生产表格 ML | 超参数多 |
| Stacking | 两者 | 追求最后 1-2% 准确率 | 复杂，元学习器有过拟合风险 |
| 投票 | 方差 | 快速组合多样化模型 | 只在模型多样化时有效 |

### 表格数据的生产栈

对于大多数表格预测问题，尝试顺序：

1. **LightGBM 或 XGBoost**，使用默认参数
2. 调优 n_estimators、learning_rate、max_depth、min_child_weight
3. 如果需要最后 0.5%，构建 3-5 个多样化模型的 Stacking 集成
4. 始终使用交叉验证

表格数据上的神经网络几乎总是比梯度提升差。TabNet、NODE 等架构偶尔能匹敌但很少打败调好的 XGBoost。

## 产出物

本课产出 `outputs/prompt-ensemble-selector.md` 和 `outputs/skill-ensemble-builder.md`。

## 练习题

1. 修改 AdaBoost 实现在每轮后追踪训练准确率。绘制准确率 vs 估计器数量。何时收敛？

2. 从零实现随机森林：在回归树上添加随机特征子采样。训练 100 棵树，`max_features=sqrt(n_features)`，平均预测。比较方差减少与单棵树。

3. 在梯度提升实现中添加早停：每轮后追踪验证损失，连续 10 轮没改善就停止。实际需要多少棵树？

4. 构建三个基础模型（逻辑回归、决策树、KNN）和一个逻辑回归元学习器的 Stacking 集成。用 5 折交叉验证生成元特征。与每个基础模型单独比较。

5. 在同一数据集上用默认参数运行 XGBoost。与从零实现的梯度提升比较准确率。计时两者。速度差异有多大？

## 术语速查表

| 术语 | 实际含义 |
|------|---------|
| Bagging | Bootstrap 聚合：在 Bootstrap 样本上训练模型，平均预测以减少方差 |
| Boosting | 串行训练模型，每个纠正集成到目前为止的错误，以减少偏差 |
| AdaBoost | 通过样本权重更新进行 Boosting；被误分类的点在下一次获得更高权重 |
| 梯度提升 | 通过让每个新模型拟合损失函数的负梯度来进行 Boosting |
| XGBoost | 带正则化、二阶优化和系统级加速的梯度提升 |
| Stacking | 将基础模型的预测作为元学习器的输入特征 |
| 随机森林 | 对决策树做 Bagging，在每次分裂时添加随机特征子采样以增加多样性 |
| 集成多样性 | 模型的错误必须不相关，集成才能优于单个模型 |
| 袋外误差 | 未被 Bootstrap 抽中的样本（约 36.8%）作为免费验证集 |

## 延伸阅读

- [Schapire & Freund: Boosting: Foundations and Algorithms](https://mitpress.mit.edu/9780262526036/) - AdaBoost 创始人的著作
- [Friedman: Greedy Function Approximation: A Gradient Boosting Machine (2001)](https://statweb.stanford.edu/~jhf/ftp/trebst.pdf) - 梯度提升原始论文
- [Chen & Guestrin: XGBoost (2016)](https://arxiv.org/abs/1603.02754) - XGBoost 论文
- [Wolpert: Stacked Generalization (1992)](https://www.sciencedirect.com/science/article/abs/pii/S0893608005800231) - Stacking 原始论文
- [scikit-learn 集成方法](https://scikit-learn.org/stable/modules/ensemble.html) - 实用参考
