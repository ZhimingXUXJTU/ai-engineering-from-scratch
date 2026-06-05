# Decision Trees and Random Forests
# 决策树与随机森林


> A decision tree is just a flowchart. But a forest of them is one of the most powerful tools in ML.

> 一棵决策树就是一张流程图。但一片由它们组成的森林，是机器学习中最强大的工具之一。

**Type:** Build | **类型：** 构建
**Language:** Python | **语言：** Python
**Prerequisites:** Phase 1 (Lessons 09 Information Theory, 06 Probability) | **前置知识：** Phase 1（第 9 课信息论、第 6 课概率论）
**Time:** ~90 minutes | **时间：** 约 90 分钟

## Learning Objectives | 学习目标

- Implement Gini impurity, entropy, and information gain calculations to find optimal decision tree splits
  实现 Gini 不纯度、熵和信息增益计算，找到最优决策树分裂点
- Build a decision tree classifier from scratch with pre-pruning controls (max depth, min samples)
  从零构建带有预剪枝控制（最大深度、最小样本数）的决策树分类器
- Construct a random forest using bootstrap sampling and feature randomization, and explain why it reduces variance
  使用 Bootstrap 采样和特征随机化构建随机森林，并解释它为什么能降低方差
- Compare MDI feature importance with permutation importance and identify when MDI is biased
  比较 MDI 特征重要性和置换重要性，识别 MDI 的偏差问题


> **【中文解读】**
> 决策树通过 if-else 规则分割数据，随机森林是多个决策树的投票组合。sklearn 中最常用的模型之一。金融风控、医疗诊断中随机森林是基线模型。

> **【拓展：树模型在 Kaggle 和工业界的主导地位】**
> 在 Kaggle 结构化数据竞赛中，约 70% 的获胜方案使用梯度提升树（XGBoost/LightGBM/CatBoost）。在金融领域，信用评分（FICO 分数）广泛使用决策树变体；银行反欺诈系统常用随机森林作为基线；医疗诊断中，随机森林用于预测再入院风险。树模型能自动处理混合类型特征且可解释，这是神经网络难以做到的。

## The Problem | 问题引入

You have tabular data. Rows are samples, columns are features, and there is a target column you want to predict. You could throw a neural network at it. But for tabular data, tree-based models (decision trees, random forests, gradient boosted trees) consistently outperform deep learning. Kaggle competitions on structured data are dominated by XGBoost and LightGBM, not transformers.

> 你有表格数据。行是样本，列是特征，还有一个你想预测的目标列。你可以用神经网络来处理。但对于表格数据，树模型（决策树、随机森林、梯度提升树）始终优于深度学习。Kaggle 的结构化数据竞赛被 XGBoost 和 LightGBM 主导，而不是 Transformer。

Why? Trees handle mixed feature types (numeric and categorical) without preprocessing. They handle nonlinear relationships without feature engineering. They are interpretable: you can look at the tree and see exactly why a prediction was made. And random forests, which average many trees, are highly resistant to overfitting on moderate-sized datasets.

> 为什么？树模型无需预处理就能处理混合特征类型（数值和类别）。无需特征工程就能处理非线性关系。它们可解释：你可以查看树并确切了解为什么做出某个预测。而随机森林通过平均许多树，对中等规模数据集的过拟合有很强的抵抗力。

This lesson builds decision trees from scratch using recursive splitting, then builds a random forest on top. You will implement the math behind split criteria (Gini impurity, entropy, information gain) and understand why an ensemble of weak learners becomes a strong one.

> 本课从零使用递归分裂构建决策树，然后在之上构建随机森林。你将实现分裂标准背后的数学（Gini 不纯度、熵、信息增益），并理解为什么一组弱学习器能变成强学习器。

> **【中文解读】**
> 对于表格型数据（行是样本，列是特征），树模型通常优于深度学习。原因：树模型原生支持混合类型特征、自动发现非线性关系、训练速度快、结果可解释。随机森林通过集成多个"弱学习器"（单棵决策树）成为"强学习器"，是 ML 最实用的算法之一。

## The Concept | 核心概念

### What a decision tree does

A decision tree partitions the feature space into rectangular regions by asking a sequence of yes/no questions.

> 决策树通过一系列是非问题将特征空间划分为矩形区域。

```mermaid
graph TD
    A["Age < 30?"] -->|Yes| B["Income > 50k?"]
    A -->|No| C["Credit Score > 700?"]
    B -->|Yes| D["Approve"]
    B -->|No| E["Deny"]
    C -->|Yes| F["Approve"]
    C -->|No| G["Deny"]
```

Each internal node tests a feature against a threshold. Each leaf node makes a prediction. To classify a new data point, you start at the root and follow the branches until you reach a leaf.

> 每个内部节点将一个特征与阈值进行比较。每个叶节点做出预测。要分类一个新数据点，从根节点开始沿着分支走直到到达叶节点。

The tree is built top-down by choosing, at each node, the feature and threshold that best separate the data. "Best" is defined by a split criterion.

> 树自顶向下构建，在每个节点选择最能分离数据的特征和阈值。"最好"由分裂标准定义。

### Split criteria: measuring impurity

At each node, we have a set of samples. We want to split them so that the resulting child nodes are as "pure" as possible, meaning each child contains mostly one class.

> 在每个节点，我们有一组样本。我们想要分裂它们使子节点尽可能"纯净"，即每个子节点主要包含一个类别。

**Gini impurity** measures the probability that a randomly chosen sample would be misclassified if it were labeled according to the class distribution at that node.

> **Gini 不纯度**衡量一个随机选择的样本如果按该节点的类别分布标记，被错误分类的概率。

```
Gini(S) = 1 - sum(p_k^2)

where p_k is the proportion of class k in set S.
```

For a pure node (all one class), Gini = 0. For a binary split with 50/50 classes, Gini = 0.5. Lower is better.

> 对于纯节点（全是一个类别），Gini = 0。对于 50/50 的二元分裂，Gini = 0.5。越低越好。

```
Example: 6 cats, 4 dogs

Gini = 1 - (0.6^2 + 0.4^2) = 1 - (0.36 + 0.16) = 0.48
```

**Entropy** measures the information content (disorder) in a node. Covered in Phase 1 Lesson 09.

> **熵**衡量节点中的信息内容（混乱度）。在 Phase 1 第 9 课中已讨论。

```
Entropy(S) = -sum(p_k * log2(p_k))
```

For a pure node, entropy = 0. For a 50/50 binary split, entropy = 1.0. Lower is better.

> 对于纯节点，熵 = 0。对于 50/50 的二元分裂，熵 = 1.0。越低越好。

```
Example: 6 cats, 4 dogs

Entropy = -(0.6 * log2(0.6) + 0.4 * log2(0.4))
        = -(0.6 * -0.737 + 0.4 * -1.322)
        = 0.442 + 0.529
        = 0.971 bits
```

**Information gain** is the reduction in impurity (entropy or Gini) after a split.

> **信息增益**是分裂后不纯度（熵或 Gini）的减少量。

```
IG(S, feature, threshold) = Impurity(S) - weighted_avg(Impurity(S_left), Impurity(S_right))

where the weights are the proportions of samples in each child.
```

The greedy algorithm at each node: try every feature and every possible threshold. Pick the (feature, threshold) pair that maximizes information gain.

> 每个节点的贪心算法：尝试每个特征和每个可能的阈值。选择使信息增益最大的（特征，阈值）对。

> **【中文解读】**
> 分裂标准衡量节点的"不纯度"。Gini 不纯度 = 随机分类的错误概率；熵 = 信息论中的不确定性度量。信息增益 = 分裂前不纯度 - 分裂后加权不纯度。贪心算法在每个节点选择信息增益最大的（特征, 阈值）对进行分裂。虽然贪心不保证全局最优（找最优树是 NP-hard），但实践中效果很好。

### How splitting works

For a dataset with n features and m samples at the current node:

> 对于有 n 个特征和 m 个样本的当前节点：

1. For each feature j (j = 1 to n):
   对于每个特征 j（j = 1 到 n）：
   - Sort the samples by feature j
     按特征 j 对样本排序
   - Try every midpoint between consecutive distinct values as a threshold
     尝试每对相邻不同值的中点作为阈值
   - Compute the information gain for each threshold
     计算每个阈值的信息增益
2. Select the feature and threshold with the highest information gain
   选择信息增益最高的特征和阈值
3. Split the data into left (feature <= threshold) and right (feature > threshold)
   将数据分裂为左（特征 <= 阈值）和右（特征 > 阈值）
4. Recurse on each child
   对每个子节点递归

This greedy approach does not guarantee the globally optimal tree. Finding the optimal tree is NP-hard. But greedy splitting works well in practice.

> 这种贪心方法不保证全局最优的树。找到最优树是 NP-hard 的。但贪心分裂在实践中效果很好。

### Stopping conditions

Without stopping conditions, the tree grows until every leaf is pure (one sample per leaf). This perfectly memorizes the training data and generalizes terribly.

> 没有停止条件，树会一直生长直到每个叶节点都是纯的（每个叶节点一个样本）。这完美记忆了训练数据但泛化能力极差。

**Pre-pruning** stops the tree before it fully grows:
- Maximum depth: stop splitting when the tree reaches a set depth
  最大深度：当树达到设定深度时停止分裂
- Minimum samples per leaf: stop if a node has fewer than k samples
  每叶最小样本数：如果节点少于 k 个样本则停止
- Minimum information gain: stop if the best split improves impurity by less than a threshold
  最小信息增益：如果最佳分裂改善不纯度低于阈值则停止
- Maximum leaf nodes: limit the total number of leaves
  最大叶节点数：限制叶节点的总数

**Post-pruning** grows the full tree, then trims it back:
- Cost-complexity pruning (used by scikit-learn): adds a penalty proportional to the number of leaves. Increase the penalty to get smaller trees
  代价复杂度剪枝（scikit-learn 使用）：添加与叶节点数成正比的惩罚。增加惩罚得到更小的树
- Reduced error pruning: remove a subtree if the validation error does not increase
  减误差剪枝：如果验证误差不增加，则移除子树

Pre-pruning is simpler and faster. Post-pruning often produces better trees because it does not prematurely stop splits that might lead to useful further splits.

> 预剪枝更简单更快。后剪枝通常产生更好的树，因为它不会过早停止可能带来有用后续分裂的节点。

### Decision trees for regression

For regression, the leaf prediction is the mean of the target values in that leaf. The split criterion changes too:

> 对于回归，叶节点的预测是该叶中目标值的均值。分裂标准也改变了：

**Variance reduction** replaces information gain:

> **方差减少**替代了信息增益：

```
VR(S, feature, threshold) = Var(S) - weighted_avg(Var(S_left), Var(S_right))
```

Pick the split that reduces variance the most. The tree partitions the input space into regions, and predicts a constant (the mean) in each region.

> 选择方差减少最多的分裂。树将输入空间划分为区域，在每个区域预测一个常数（均值）。

### Random forests: the power of ensembles

A single decision tree is high variance. Small changes in the data can produce completely different trees. Random forests fix this by averaging many trees.

> 单棵决策树具有高方差。数据的微小变化会产生完全不同的树。随机森林通过平均许多树来解决这个问题。

```mermaid
graph TD
    D["Training Data"] --> B1["Bootstrap Sample 1"]
    D --> B2["Bootstrap Sample 2"]
    D --> B3["Bootstrap Sample 3"]
    D --> BN["Bootstrap Sample N"]
    B1 --> T1["Tree 1<br>(random feature subset)"]
    B2 --> T2["Tree 2<br>(random feature subset)"]
    B3 --> T3["Tree 3<br>(random feature subset)"]
    BN --> TN["Tree N<br>(random feature subset)"]
    T1 --> V["Aggregate Predictions<br>(majority vote or average)"]
    T2 --> V
    T3 --> V
    TN --> V
```

Two sources of randomness make the trees diverse:

> 两种随机性来源使树变得多样化：

**Bagging (bootstrap aggregating):** Each tree is trained on a bootstrap sample, a random sample with replacement from the training data. About 63% of the original samples appear in each bootstrap (the rest are out-of-bag samples that can be used for validation).

> **Bagging（Bootstrap 聚合）**：每棵树在 Bootstrap 样本上训练，即从训练数据中有放回抽样的随机样本。约 63% 的原始样本出现在每个 Bootstrap 中（其余是袋外样本，可用于验证）。

**Feature randomization:** At each split, only a random subset of features is considered. For classification, the default is sqrt(n_features). For regression, n_features/3. This prevents all trees from splitting on the same dominant feature.

> **特征随机化**：在每次分裂时，只考虑随机子集的特征。分类默认 sqrt(n_features)，回归默认 n_features/3。这防止所有树在同一个主导特征上分裂。

The key insight: averaging many decorrelated trees reduces variance without increasing bias. Each individual tree may be mediocre. The ensemble is strong.

> 核心洞察：平均许多去相关的树可以降低方差而不增加偏差。每棵单独的树可能平庸，但集成是强大的。

> **【中文解读】**
> 随机森林的两个核心随机化机制：(1) Bagging——每棵树用有放回抽样（约 63% 的原始样本）训练；(2) 特征随机化——每次分裂只考虑随机子集的特征（分类任务默认 √n 个）。这两个机制使树之间足够"不同"，取平均后大幅降低方差，同时不增加偏差。这就是"三个臭皮匠顶个诸葛亮"的数学证明。

> **【拓展：随机森林 vs 梯度提升树】**
> 随机森林是并行训练（各树独立），适合快速原型开发，几乎不需调参。梯度提升树（XGBoost/LightGBM/CatBoost）是串行训练（每棵树纠正前一棵的错误），精度通常更高但更容易过拟合。在 Kaggle 竞赛中，XGBoost 出现在约 60% 的获奖方案中。实际项目中常用策略：先用随机森林做基线，再用 XGBoost 追求极致性能。

### Feature importance

Random forests naturally provide feature importance scores. The most common method:

> 随机森林天然提供特征重要性分数。最常见的方法：

**Mean Decrease in Impurity (MDI):** For each feature, sum the total reduction in impurity across all trees and all nodes where that feature is used. Features that produce bigger impurity reductions at earlier splits are more important.

> **平均不纯度减少（MDI）**：对每个特征，在所有使用该特征的树和节点上求和不纯度的总减少量。在更早的分裂中产生更大不纯度减少的特征更重要。

```
importance(feature_j) = sum over all nodes where feature_j is used:
    (n_samples_at_node / n_total_samples) * impurity_decrease
```

This is fast (computed during training) but biased toward high-cardinality features and features with many possible split points.

> 这很快（训练时计算）但偏向高基数特征和有许多可能分裂点的特征。

**Permutation importance** is the alternative: shuffle one feature's values and measure how much the model's accuracy drops. More reliable but slower.

> **置换重要性**是替代方案：打乱一个特征的值，测量模型准确率下降多少。更可靠但更慢。

> **【拓展：特征重要性的陷阱】**
> MDI 特征重要性有两个已知偏差：(1) 高基数特征（如用户 ID）会被高估重要性，因为有更多分裂点可选；(2) 相关特征之间会分摊重要性，使每个看起来都不那么重要。Permutation importance 更可靠，但计算成本更高。在金融风控中，这种偏差可能导致错误的特征选择，进而影响模型公平性。

### When trees beat neural networks

Trees and forests dominate neural networks on tabular data. Several reasons:

> 树和森林在表格数据上优于神经网络。原因如下：

| Factor | Trees | Neural networks |
|--------|-------|----------------|
| Mixed types (numeric + categorical) | Native support | Need encoding |
| Small datasets (< 10k rows) | Work well | Overfit |
| Feature interactions | Found by splitting | Need architecture design |
| Interpretability | Full transparency | Black box |
| Training time | Minutes | Hours |
| Hyperparameter sensitivity | Low | High |

| 因素 | 树模型 | 神经网络 |
|------|-------|---------|
| 混合类型（数值 + 类别） | 原生支持 | 需要编码 |
| 小数据集（< 1 万行） | 表现良好 | 容易过拟合 |
| 特征交互 | 通过分裂自动发现 | 需要架构设计 |
| 可解释性 | 完全透明 | 黑盒 |
| 训练时间 | 分钟级 | 小时级 |
| 超参数敏感度 | 低 | 高 |

Neural networks win when the data has spatial or sequential structure (images, text, audio). For flat tables of features, trees are the default.

> 当数据具有空间或序列结构（图像、文本、音频）时，神经网络更胜一筹。对于扁平的特征表格，树模型是默认选择。

## Build It | 动手实现

### Step 1: Gini impurity and entropy

Build both split criteria from scratch and verify they agree on which splits are good.

> 从零构建两种分裂标准，验证它们在哪些分裂好这一点上达成一致。

```python
import math

def gini_impurity(labels):
    n = len(labels)
    if n == 0:
        return 0.0
    counts = {}
    for label in labels:
        counts[label] = counts.get(label, 0) + 1  # 统计每个类别的出现次数
    # Gini = 1 - sum(p_k^2)，衡量节点的不纯度
    return 1.0 - sum((c / n) ** 2 for c in counts.values())

def entropy(labels):
    n = len(labels)
    if n == 0:
        return 0.0
    counts = {}
    for label in labels:
        counts[label] = counts.get(label, 0) + 1
    # Entropy = -sum(p_k * log2(p_k))，信息论中的不确定性度量
    return -sum(
        (c / n) * math.log2(c / n) for c in counts.values() if c > 0
    )
```

### Step 2: Find the best split

Try every feature and every threshold. Return the one with the highest information gain.

> 尝试每个特征和每个阈值。返回信息增益最高的那个。

```python
def information_gain(parent_labels, left_labels, right_labels, criterion="gini"):
    measure = gini_impurity if criterion == "gini" else entropy  # 选择不纯度度量
    n = len(parent_labels)
    n_left = len(left_labels)
    n_right = len(right_labels)
    if n_left == 0 or n_right == 0:
        return 0.0  # 空节点无法产生信息增益
    parent_impurity = measure(parent_labels)  # 父节点不纯度
    # 子节点加权不纯度
    child_impurity = (
        (n_left / n) * measure(left_labels) +
        (n_right / n) * measure(right_labels)
    )
    # 信息增益 = 父节点不纯度 - 子节点加权不纯度
    return parent_impurity - child_impurity
```

### Step 3: Build the DecisionTree class

Recursive splitting, prediction, and feature importance tracking.

> 递归分裂、预测和特征重要性追踪。

```python
class DecisionTree:
    def __init__(self, max_depth=None, min_samples_split=2,
                 min_samples_leaf=1, criterion="gini",
                 max_features=None):
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.min_samples_leaf = min_samples_leaf
        self.criterion = criterion
        self.max_features = max_features
        self.tree = None
        self.feature_importances_ = None

    def fit(self, X, y):
        self.n_features = len(X[0])
        self.feature_importances_ = [0.0] * self.n_features
        self.n_samples = len(X)
        self.tree = self._build(X, y, depth=0)
        total = sum(self.feature_importances_)
        if total > 0:
            self.feature_importances_ = [
                fi / total for fi in self.feature_importances_
            ]

    def predict(self, X):
        return [self._predict_one(x, self.tree) for x in X]
```

### Step 4: Build the RandomForest class

Bootstrap sampling, feature randomization, and majority voting.

> Bootstrap 采样、特征随机化和多数投票。

```python
class RandomForest:
    def __init__(self, n_trees=100, max_depth=None,
                 min_samples_split=2, max_features="sqrt",
                 criterion="gini"):
        self.n_trees = n_trees
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.max_features = max_features
        self.criterion = criterion
        self.trees = []

    def fit(self, X, y):
        n = len(X)
        for _ in range(self.n_trees):
            indices = [random.randint(0, n - 1) for _ in range(n)]
            X_boot = [X[i] for i in indices]
            y_boot = [y[i] for i in indices]
            tree = DecisionTree(
                max_depth=self.max_depth,
                min_samples_split=self.min_samples_split,
                max_features=self.max_features,
                criterion=self.criterion,
            )
            tree.fit(X_boot, y_boot)
            self.trees.append(tree)

    def predict(self, X):
        all_preds = [tree.predict(X) for tree in self.trees]
        predictions = []
        for i in range(len(X)):
            votes = {}
            for preds in all_preds:
                v = preds[i]
                votes[v] = votes.get(v, 0) + 1
            predictions.append(max(votes, key=votes.get))
        return predictions
```

See `code/trees.py` for the complete implementation with all helper methods.

> 完整实现（含所有辅助方法）见 `code/trees.py`。

## Use It | 用框架实现

> **【中文解读】**
> sklearn 的随机森林只需三行代码：创建分类器 → fit → score。但在实践中需要注意：n_estimators（树的数量）通常 100-500 就足够，随机森林几乎不会因为树太多而过拟合；max_features 控制每次分裂考虑的特征数，默认 √n 是经验最优值。对于更高性能，使用 XGBoost 或 LightGBM。

With scikit-learn, training a random forest is three lines:

> 使用 scikit-learn，训练随机森林只需三行代码：

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

X, y = load_iris(return_X_y=True)  # 加载鸢尾花数据集
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)  # 划分训练/测试集

rf = RandomForestClassifier(n_estimators=100, random_state=42)  # 100 棵树的随机森林
rf.fit(X_train, y_train)  # 训练
print(f"Accuracy: {rf.score(X_test, y_test):.4f}")  # 评估准确率
print(f"Feature importances: {rf.feature_importances_}")
```

In practice, gradient boosted trees (XGBoost, LightGBM, CatBoost) are often stronger than random forests because they build trees sequentially, with each tree correcting the errors of the previous ones. But random forests are harder to misconfigure and require almost no hyperparameter tuning.

> 在实践中，梯度提升树（XGBoost、LightGBM、CatBoost）通常比随机森林更强，因为它们顺序构建树，每棵树纠正前一棵的错误。但随机森林更难配置错，几乎不需要超参数调优。

## Ship It | 产出物

This lesson produces `outputs/prompt-tree-interpreter.md` -- a prompt that interprets decision tree splits for business stakeholders. Feed it a trained tree's structure (depth, features, split thresholds, accuracy) and it translates the model into plain-language rules, ranks feature importance, flags overfitting or leakage, and recommends next steps. Use it any time you need to explain a tree-based model to someone who does not read code.

> 本课产出 `outputs/prompt-tree-interpreter.md`——一个为业务相关方解释决策树分裂的提示词。输入训练好的树结构（深度、特征、分裂阈值、准确率），它会将模型翻译成自然语言规则、排列特征重要性、标记过拟合或泄漏、推荐下一步。当你需要向不看代码的人解释树模型时使用它。

> **【中文解读】**
> 树模型最大的优势之一是可解释性——可以清楚看到每个决策路径。这个产出物是一个 prompt 模板，将训练好的决策树结构翻译成业务人员能理解的自然语言规则。在金融风控中，这种可解释性是监管合规的必要条件——银行必须能解释为什么拒绝了一笔贷款申请。

## Exercises | 练习题

1. Train a single decision tree on a 2D dataset with 3 classes. Manually trace the splits and draw the rectangular decision boundaries. Compare the boundaries at max_depth=2 vs max_depth=10.
   1. 在 3 类 2D 数据集上训练单棵决策树。手动追踪分裂并绘制矩形决策边界。比较 max_depth=2 和 max_depth=10 的边界。

2. Implement variance reduction splitting for regression trees. Generate y = sin(x) + noise for 200 points and fit your regression tree. Plot the tree's piecewise-constant predictions against the true curve.
   2. 实现回归树的方差减少分裂。为 200 个点生成 y = sin(x) + noise，拟合回归树。绘制树的分段常数预测与真实曲线。

3. Build a random forest with 1, 5, 10, 50, and 200 trees. Plot training accuracy and test accuracy vs number of trees. Observe that test accuracy plateaus but does not decrease (forests resist overfitting).
   3. 分别用 1、5、10、50 和 200 棵树构建随机森林。绘制训练准确率和测试准确率随树数量的变化。观察测试准确率趋于平稳但不会下降（森林抗过拟合）。

4. Compare Gini impurity vs entropy as split criteria on 5 different datasets. Measure accuracy and tree depth. In most cases, they produce nearly identical results. Explain why.
   4. 在 5 个不同数据集上比较 Gini 不纯度和熵作为分裂标准。测量准确率和树深度。大多数情况下它们产生几乎相同的结果。解释原因。

5. Implement permutation importance. Compare it with MDI importance on a dataset where one feature is random noise but has high cardinality. MDI will rank the noise feature highly. Permutation importance will not.
   5. 实现置换重要性。在一个包含随机噪声但高基数特征的数据集上，将其与 MDI 重要性比较。MDI 会将噪声特征排在前列。置换重要性不会。

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Decision tree | "A flowchart for predictions" | A model that partitions feature space into rectangular regions by learning a sequence of if/else splits |
| Gini impurity | "How mixed the node is" | Probability of misclassifying a random sample at a node. 0 = pure, 0.5 = maximum impurity for binary |
| Entropy | "The disorder in a node" | Information content at a node. 0 = pure, 1.0 = maximum uncertainty for binary. From information theory |
| Information gain | "How good a split is" | Reduction in impurity after a split. The greedy criterion for choosing splits |
| Pre-pruning | "Stop the tree early" | Stopping tree growth early by setting max depth, min samples, or min gain thresholds |
| Post-pruning | "Trim the tree after" | Growing the full tree, then removing subtrees that do not improve validation performance |
| Bagging | "Train on random subsets" | Bootstrap aggregating. Train each model on a different random sample with replacement |
| Random forest | "A bunch of trees" | Ensemble of decision trees, each trained on a bootstrap sample with random feature subsets at each split |
| Feature importance (MDI) | "Which features matter" | Total impurity decrease contributed by each feature, summed across all trees and nodes |
| Permutation importance | "Shuffle and check" | Accuracy drop when a feature's values are randomly shuffled. More reliable than MDI for noisy features |
| Variance reduction | "The regression version of info gain" | The regression tree analogue of information gain. Picks the split that reduces target variance the most |
| Bootstrap sample | "Random sample with repeats" | A random sample drawn with replacement from the original dataset. Same size, but with duplicates |

## Further Reading | 延伸阅读

- [Breiman: Random Forests (2001)](https://link.springer.com/article/10.1023/A:1010933404324) - the original random forest paper
  [Breiman: Random Forests (2001)](https://link.springer.com/article/10.1023/A:1010933404324) - 随机森林原始论文
- [Grinsztajn et al.: Why do tree-based models still outperform deep learning on tabular data? (2022)](https://arxiv.org/abs/2207.08815) - rigorous comparison of trees vs neural networks on tabular tasks
  [Grinsztajn et al.: Why do tree-based models still outperform deep learning on tabular data? (2022)](https://arxiv.org/abs/2207.08815) - 树模型与神经网络在表格数据上的严格比较
- [scikit-learn Decision Trees documentation](https://scikit-learn.org/stable/modules/tree.html) - practical guide with visualization tools
  [scikit-learn 决策树文档](https://scikit-learn.org/stable/modules/tree.html) - 实用指南及可视化工具
- [XGBoost: A Scalable Tree Boosting System (Chen & Guestrin, 2016)](https://arxiv.org/abs/1603.02754) - the gradient boosting paper that dominates Kaggle
  [XGBoost: A Scalable Tree Boosting System (Chen & Guestrin, 2016)](https://arxiv.org/abs/1603.02754) - 统治 Kaggle 的梯度提升论文
