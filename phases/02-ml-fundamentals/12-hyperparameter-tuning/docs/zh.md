# 超参数调优

> 超参数是训练开始前你拧的旋钮。拧好了，平庸模型变优秀。

**类型：** 构建
**语言：** Python
**前置知识：** Phase 2 第 11 课（集成方法）
**时长：** 约 90 分钟

## 学习目标

- 从零实现网格搜索、随机搜索和贝叶斯优化，比较它们的样本效率
- 解释为什么随机搜索在大多数超参数有效维度低时优于网格搜索
- 使用代理模型和采集函数构建贝叶斯优化循环来引导搜索
- 设计通过适当交叉验证避免对验证集过拟合的超参数调优策略

## 问题引入

你的梯度提升模型有学习率、树的数量、最大深度、叶节点最小样本数、子采样比例和列采样比例。那是 6 个超参数。如果每个有 5 个合理值，网格有 5^6 = 15,625 个组合。每次训练需要 10 秒。那就是 43 小时的计算来全部尝试。

网格搜索是显而易见的方法，但在规模上是最差的。随机搜索用更少的计算做得更好。贝叶斯优化通过从过去的评估中学习做得更好。知道用哪种策略，以及哪些超参数真正重要，能节省数天浪费的 GPU 时间。

## 核心概念

### 参数 vs 超参数

参数在训练期间学习（权重、偏置、分裂阈值）。超参数在训练开始前设定，控制学习如何发生。

| 超参数 | 控制什么 | 典型范围 |
|-------|---------|---------|
| 学习率 | 每次更新的步长 | 0.001 到 1.0 |
| 树的数量/Epoch | 训练多久 | 10 到 10,000 |
| 最大深度 | 模型复杂度 | 1 到 30 |
| 正则化 (lambda) | 防止过拟合 | 0.0001 到 100 |
| 批量大小 | 梯度估计噪声 | 16 到 512 |
| Dropout 率 | 丢弃的神经元比例 | 0.0 到 0.5 |

### 网格搜索

网格搜索评估指定值的每个组合。它穷举且容易理解，但随超参数数量指数增长。

网格搜索有一个根本缺陷：如果一个超参数重要另一个不重要，大部分评估浪费了。9 次评估只得到重要参数的 3 个唯一值。

### 随机搜索

随机搜索从分布中采样超参数而非网格。在同样的 9 次评估预算下，你得到每个超参数的 9 个唯一值。

为什么随机优于网格（Bergstra & Bengio, 2012）：

- 大多数超参数有效维度低。6 个超参数中通常只有 1-2 个重要
- 网格搜索在不重要的维度上浪费评估
- 随机搜索在同样的预算下更密集地覆盖重要维度
- 在 60 次随机试验中，你有 95% 的机会找到距离最优 5% 以内的点

### 贝叶斯优化

随机搜索忽略结果。它不会学到高学习率导致发散或深度 3 始终优于深度 10。贝叶斯优化使用过去的评估来决定下一步搜索哪里。

两个关键组件：

**代理模型 (Surrogate Model)：** 一个廉价评估的模型（通常是高斯过程）近似昂贵的目标函数。它在搜索空间中任何点都给出预测和不确定性估计。

**采集函数 (Acquisition Function)：** 通过平衡开发（在已知好点附近搜索）和探索（在不确定性高的地方搜索）来决定下一步评估哪里。常见选择：

- **期望改进 (EI)：** 在这个点上预期比当前最好改善多少？
- **置信上界 (UCB)：** 预测加不确定性的倍数。更高的 UCB 意味着有希望或未探索。
- **改进概率 (PI)：** 这个点超过当前最好的概率？

贝叶斯优化通常比随机搜索用 2-5 倍少的评估找到更好的超参数。拟合代理模型的开销与训练实际模型相比可以忽略。

### 早停

不是每次训练都需要完成。如果一个配置在 10 个 epoch 后明显不好，停止它继续下一个。

策略：
- **基于耐心值：** 如果验证损失连续 N 个 epoch 没改善就停止
- **中位数剪枝：** 如果试验的中间结果比同一阶段已完成试验的中位数差就停止
- **Hyperband：** 给许多配置分配小预算，然后逐步给最好的增加预算

Hyperband 特别有效：启动 81 个配置各 1 个 epoch，保留前 1/3，给它们 3 个 epoch，保留前 1/3，以此类推。这比全预算评估所有配置快 10-50 倍找到好配置。

### 学习率调度

学习率几乎总是最重要的超参数。调度器在训练期间调整它而非保持固定。

| 调度器 | 公式 | 何时使用 |
|-------|------|---------|
| 步进衰减 | 每 N 个 epoch 乘以 0.1 | 经典 CNN 训练 |
| 余弦退火 | lr * 0.5 * (1 + cos(pi * t / T)) | 现代默认 |
| 预热+衰减 | 线性增加然后余弦衰减 | Transformer |
| 单周期 | 在一个周期内先增后减 | 快速收敛 |
| 平台期时降低 | 指标停滞时乘以一个因子 | 安全默认 |

### 超参数重要性

不是所有超参数同等重要。对随机森林和梯度提升的研究显示一致的模式：

**高重要性：**
- 学习率（始终最先调优）
- 估计器数量/Epoch（用早停代替调优）
- 正则化强度

**中等重要性：**
- 最大深度/层数
- 叶节点最小样本/权重衰减
- 子采样比例

**低重要性：**
- 最大特征数（随机森林）
- 具体激活函数选择
- 批量大小（在合理范围内）

先调重要的，其余保持默认。

### 实用策略

具体工作流：

1. **从库默认值开始。** 它们由经验丰富的从业者选择，通常已经 80% 好了。
2. **粗略随机搜索。** 宽范围，20-50 次试验。用早停快速杀死差的运行。
3. **分析结果。** 哪些超参数与性能相关？缩小搜索空间。
4. **精细搜索。** 在缩小的空间中贝叶斯优化或聚焦随机搜索。50-100 次试验。
5. **在所有训练数据上重训** 用找到的最佳超参数。

### 交叉验证集成

在单个验证分割上调优超参数有风险。最佳超参数可能过拟合到特定验证折。嵌套交叉验证通过两个循环解决这个问题：

- **外循环**（评估）：将数据分为训练+验证和测试。报告无偏性能。
- **内循环**（调优）：将训练+验证分为训练和验证。找到最佳超参数。

每个外折独立找到自己的最佳超参数。外分数是无偏的泛化性能估计。

这很昂贵（5 个外折 x 5 个内折 x 27 个网格点 = 675 次模型拟合），但给你可信赖的性能估计。在论文中报告最终结果或决策风险高时使用。

### 实用技巧

**从学习率开始。** 它对基于梯度的方法总是最重要的超参数。糟糕的学习率让其他一切无关紧要。先固定其他超参数在默认值，先扫学习率。

**对学习率和正则化使用对数均匀分布。** 0.001 和 0.01 之间的差异与 0.1 和 1.0 之间的差异一样重要。线性搜索在大端浪费预算。

**用早停代替调优 n_estimators。** 对于提升和神经网络，设高 n_estimators 或 epochs，让早停决定何时停止。这从搜索中移除了一个超参数。

**预算分配。** 将 60% 的调优预算花在前 2 个最重要的超参数上。剩余 40% 给其他所有。前 2 个占了大部分性能变化。

**搜索尺度重要。** 绝不在对数尺度上搜索批量大小（16、32、64 就好）。始终在对数尺度上搜索学习率。让搜索分布匹配超参数如何影响模型。

## 动手实现

`code/tuning.py` 中的代码从零实现网格搜索、随机搜索和简化贝叶斯优化器。

### 步骤 1：从零实现网格搜索

```python
def grid_search(model_fn, param_grid, X_train, y_train, X_val, y_val):
    keys = list(param_grid.keys())
    values = list(param_grid.values())
    best_score = -float("inf")
    best_params = None
    n_evals = 0

    for combo in itertools.product(*values):
        params = dict(zip(keys, combo))
        model = model_fn(**params)
        model.fit(X_train, y_train)
        score = evaluate(model, X_val, y_val)
        n_evals += 1

        if score > best_score:
            best_score = score
            best_params = params

    return best_params, best_score, n_evals
```

### 步骤 2：从零实现随机搜索

```python
def random_search(model_fn, param_distributions, X_train, y_train,
                  X_val, y_val, n_iter=50, seed=42):
    rng = np.random.RandomState(seed)
    best_score = -float("inf")
    best_params = None

    for _ in range(n_iter):
        params = {k: sample(v, rng) for k, v in param_distributions.items()}
        model = model_fn(**params)
        model.fit(X_train, y_train)
        score = evaluate(model, X_val, y_val)

        if score > best_score:
            best_score = score
            best_params = params

    return best_params, best_score, n_iter
```

### 步骤 3：简化贝叶斯优化

核心思想：用高斯过程拟合观测到的（超参数，分数）对，然后用采集函数决定下一步看哪里。

```python
class SimpleBayesianOptimizer:
    def __init__(self, search_space, n_initial=5):
        self.search_space = search_space
        self.n_initial = n_initial
        self.X_observed = []
        self.y_observed = []

    def suggest(self):
        if len(self.X_observed) < self.n_initial:
            return sample_random(self.search_space)

        candidates = [sample_random(self.search_space) for _ in range(500)]
        X_cand = np.array([to_vector(c) for c in candidates])
        mu, var = self._fit_gp(X_cand)
        ei = self._expected_improvement(mu, var, max(self.y_observed))
        return candidates[np.argmax(ei)]

    def observe(self, params, score):
        self.X_observed.append(to_vector(params))
        self.y_observed.append(score)
```

GP 代理在每个候选点给出两样东西：预测分数 (mu) 和不确定性 (var)。期望改进平衡两者：它偏爱模型预测高分的点或不确定性高的点。早期，大多数点不确定性高所以优化器探索。后期，它聚焦于最有希望的区域。

### 步骤 4：比较所有方法

在同一个合成目标上运行三种方法并比较。详见 `code/tuning.py`。

## 用框架实现

### Optuna 实践

Optuna 是严肃超参数调优的推荐库。它支持剪枝、分布式搜索和可视化。

```python
import optuna

def objective(trial):
    lr = trial.suggest_float("learning_rate", 1e-4, 1e-1, log=True)
    n_est = trial.suggest_int("n_estimators", 50, 500)
    max_depth = trial.suggest_int("max_depth", 2, 10)

    model = GradientBoostingRegressor(
        learning_rate=lr,
        n_estimators=n_est,
        max_depth=max_depth,
    )
    model.fit(X_train, y_train)
    return mean_squared_error(y_val, model.predict(X_val))

study = optuna.create_study(direction="minimize")
study.optimize(objective, n_trials=100)

print(f"最佳参数: {study.best_params}")
print(f"最佳 MSE: {study.best_value:.4f}")
```

关键 Optuna 特性：
- `suggest_float(..., log=True)` 用于最好在对数尺度上搜索的参数（学习率、正则化）
- `suggest_int` 用于整数参数
- `suggest_categorical` 用于离散选择
- 内置 MedianPruner 用于早停差的试验
- `study.trials_dataframe()` 用于分析

### sklearn 内置调优器

对于快速实验，sklearn 提供 `GridSearchCV`、`RandomizedSearchCV` 和 `HalvingRandomSearchCV`：

```python
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import loguniform, randint

param_dist = {
    "learning_rate": loguniform(1e-4, 0.5),
    "max_depth": randint(2, 10),
    "n_estimators": randint(50, 500),
}

search = RandomizedSearchCV(
    GradientBoostingRegressor(),
    param_dist,
    n_iter=100,
    cv=5,
    scoring="neg_mean_squared_error",
    random_state=42,
    n_jobs=-1,
)
search.fit(X_train, y_train)
print(f"最佳参数: {search.best_params_}")
print(f"最佳 CV MSE: {-search.best_score_:.4f}")
```

## 练习题

1. 在相同的总预算下（如 50 次评估）运行网格搜索和随机搜索。比较找到的最佳分数。用不同种子运行 10 次。随机搜索赢多少次？

2. 从零实现 Hyperband。启动 81 个配置，各训练 1 个 epoch。每轮保留前 1/3 并三倍其预算。比较总计算量（所有配置的所有 epoch 之和）与全预算运行 81 个配置。

3. 在第 11 课的梯度提升实现中添加学习率调度器（余弦退火）。与固定学习率比较有帮助吗？

4. 用 Optuna 在真实数据集（如 sklearn 的乳腺癌数据集）上调优 RandomForestClassifier。用 `optuna.visualization.plot_param_importances(study)` 看哪些超参数最重要。

5. 实现一个简单的采集函数（期望改进），展示探索 vs 开发。绘制代理模型的均值和不确定性，展示 EI 选择在哪里评估。

## 术语速查表

| 术语 | 实际含义 |
|------|---------|
| 超参数 (Hyperparameter) | 训练前设定的值，控制学习过程，不从数据中学习 |
| 网格搜索 (Grid Search) | 在指定参数网格上穷举搜索。指数成本。 |
| 随机搜索 (Random Search) | 从分布中采样超参数。比网格搜索更好地覆盖重要维度。 |
| 贝叶斯优化 (Bayesian Optimization) | 使用目标的代理模型决定下一步评估哪里，平衡探索和开发 |
| 代理模型 (Surrogate Model) | 近似昂贵目标函数的模型（通常高斯过程） |
| 采集函数 (Acquisition Function) | 通过平衡期望改进和不确定性对候选点评分。EI 和 UCB 是常用选择。 |
| 早停 (Early Stopping) | 验证性能停止改善时提前终止训练 |
| Hyperband | 自适应资源分配：以小预算启动多配置，保留最好的并增加预算 |
| 学习率调度器 (LR Scheduler) | 在训练过程中调整学习率的函数 |

## 延伸阅读

- [Bergstra & Bengio: Random Search for Hyper-Parameter Optimization (2012)](https://jmlr.org/papers/v13/bergstra12a.html) - 证明随机优于网格的论文
- [Snoek et al., Practical Bayesian Optimization of Machine Learning Algorithms (2012)](https://arxiv.org/abs/1206.2944) - ML 的贝叶斯优化
- [Li et al., Hyperband (2018)](https://jmlr.org/papers/v18/16-558.html) - Hyperband 论文
- [Optuna](https://arxiv.org/abs/1907.10902) - Optuna 论文
- [Probst et al., Tunability (2019)](https://jmlr.org/papers/v20/18-444.html) - 哪些超参数重要
