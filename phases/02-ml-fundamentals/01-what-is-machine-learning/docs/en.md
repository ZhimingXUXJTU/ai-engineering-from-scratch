# What Is Machine Learning | 什么是机器学习

> Machine learning is teaching computers to find patterns in data instead of writing rules by hand.

**Type:** Learn
**Languages:** Python
**Prerequisites:** Phase 1 (Math Foundations)
**Time:** ~45 minutes

## Learning Objectives | 学习目标

- Explain the difference between supervised, unsupervised, and reinforcement learning and identify which type applies to a given problem
- Implement a nearest centroid classifier from scratch and evaluate it against a random baseline
- Distinguish between classification and regression tasks and select the appropriate loss function for each
- Evaluate whether a given business problem is suitable for ML or better solved with deterministic rules


> **【中文解读】**
> 机器学习是让计算机从数据中自动学习规律，而不是靠人工编写规则。监督学习（有标签）、无监督学习（无标签）、强化学习（奖惩信号）是三大范式。对应 sklearn 中的各类 estimator。

> **【拓展：机器学习范式的产业应用】**
> GPT-4 使用自监督学习（预测下一个 token）在约 13 万亿 token 上训练；BERT 使用掩码语言建模在 Wikipedia + BookCorpus 上预训练；AlphaGo 使用强化学习通过自我对弈超越人类围棋冠军。这三种范式在真实 AI 系统中常常组合使用——ChatGPT 先自监督预训练，再用 RLHF（人类反馈强化学习）对齐。

## The Problem | 问题引入

You want to build a spam filter. The traditional approach: sit down and write hundreds of rules. "If the email contains 'FREE MONEY', mark it spam. If it has more than 3 exclamation marks, mark it spam." You spend weeks writing rules. Then spammers change their wording. Your rules break. You write more rules. The cycle never ends.

Machine learning flips this. Instead of writing rules, you give the computer thousands of labeled emails ("spam" or "not spam") and let it figure out the rules on its own. The computer finds patterns you never would have thought of. When spammers change tactics, you retrain on new data instead of rewriting code.

This shift from "programming rules" to "learning from data" is the core of machine learning. Every recommendation engine, voice assistant, self-driving car, and language model works this way.

> **【中文解读】**
> 传统编程是"人写规则，机器执行"；机器学习是"人给数据，机器自己发现规则"。以垃圾邮件过滤器为例：传统方法需要手动维护数百条规则，而 ML 方法只需提供大量标注邮件，模型自动学习判别模式。当垃圾邮件策略变化时，只需重新训练而非重写代码。

> **【拓展：垃圾邮件过滤的演进】**
> Gmail 的垃圾邮件过滤器每天处理约 3 亿封邮件，准确率超过 99.9%。早期使用规则引擎（如 SpamAssassin），后来转向 ML（朴素贝叶斯 → 集成方法 → 深度学习）。现代系统结合 TF-IDF 特征、n-gram 模型和神经网络，在毫秒级完成分类。

## The Concept | 核心概念

### Learning From Data, Not Rules

Traditional programming and machine learning solve problems in opposite directions.

```mermaid
flowchart LR
    subgraph Traditional["Traditional Programming"]
        direction LR
        R[Rules] --> P1[Program]
        D1[Data] --> P1
        P1 --> O1[Output]
    end

    subgraph ML["Machine Learning"]
        direction LR
        D2[Data] --> P2[Learning Algorithm]
        O2[Expected Output] --> P2
        P2 --> M[Model / Rules]
    end
```

Traditional programming: you write the rules. The program applies them to data to produce output.

Machine learning: you provide data and expected outputs. The algorithm discovers the rules.

The "model" that comes out of training IS the rules, encoded as numbers (weights, parameters). It generalizes from examples it has seen to make predictions on data it has never seen.

> **【中文解读】**
> 传统编程 vs 机器学习的本质区别：传统编程输入"规则+数据"得到"输出"；机器学习输入"数据+期望输出"得到"模型（规则）"。模型本质上就是用数字编码的规则（权重和参数），它能对从未见过的新数据做出预测。这就是"泛化"——AI 系统最核心的能力。

### The Three Types of Machine Learning

```mermaid
flowchart TD
    ML[Machine Learning] --> SL[Supervised Learning]
    ML --> UL[Unsupervised Learning]
    ML --> RL[Reinforcement Learning]

    SL --> C[Classification]
    SL --> R[Regression]

    UL --> CL[Clustering]
    UL --> DR[Dimensionality Reduction]

    RL --> PO[Policy Optimization]
    RL --> VL[Value Learning]
```

**Supervised Learning**: You have input-output pairs. The model learns to map inputs to outputs.
- "Here are 10,000 photos labeled cat or dog. Learn to tell them apart."
- "Here are house features and prices. Learn to predict the price."

**Unsupervised Learning**: You have inputs only. No labels. The model finds structure on its own.
- "Here are 10,000 customer purchase histories. Find natural groupings."
- "Here are 1,000 dimensional data points. Reduce to 2 dimensions while keeping structure."

**Reinforcement Learning**: An agent takes actions in an environment and receives rewards or penalties. It learns a strategy (policy) to maximize total reward.
- "Play this game. +1 for winning, -1 for losing. Figure out a strategy."
- "Control this robot arm. +1 for picking up the object, -0.01 for each second wasted."

Most of what you will build in practice uses supervised learning. Unsupervised learning is common for preprocessing and exploration. Reinforcement learning powers game AI, robotics, and RLHF for language models.

> **【拓展：三种范式在真实系统中的分工】**
> Netflix 推荐系统同时使用三种范式：协同过滤（无监督聚类用户群体）、监督学习（预测用户对电影的评分 1-5 星）、强化学习（A/B 测试选择最优推荐策略）。Tesla Autopilot 使用监督学习（目标检测）+ 强化学习（路径规划）。Stable Diffusion 的训练涉及自监督（图像-文本对比学习 CLIP）+ 监督微调。

### Beyond the Big Three

The three categories above are clean, but real-world ML often blurs the lines.

**Semi-supervised learning** uses a small set of labeled data and a large set of unlabeled data. You might have 100 labeled medical images and 100,000 unlabeled ones. Techniques include:

- **Label propagation:** Build a graph connecting similar data points. Labels spread from labeled nodes to unlabeled neighbors through the graph.
- **Pseudo-labeling:** Train a model on the labeled data, use it to predict labels for unlabeled data, then retrain on everything. The model bootstraps its own training set.
- **Consistency regularization:** The model should give the same prediction for an input and a slightly perturbed version of that input. This works even without labels.

**Self-supervised learning** creates supervision from the data itself. No human labels needed at all. The model creates its own prediction task from the structure of the data.

- **Masked language modeling (BERT):** Hide 15% of words in a sentence, train the model to predict the missing words. The "labels" come from the original text.
- **Contrastive learning (SimCLR):** Take an image, create two augmented versions. Train the model to recognize they came from the same image while distinguishing them from augmented versions of other images.
- **Next-token prediction (GPT):** Predict the next word given all previous words. Every text document becomes a training example.

> **【拓展：自监督学习如何驱动大模型革命】**
> GPT-4 的训练数据约 13 万亿 token，如果靠人工标注根本不可能。自监督学习让模型从数据自身结构中创建训练信号：BERT 遮盖 15% 的词让模型预测，GPT 预测下一个 token，SimCLR 通过数据增强学习视觉表征。这使得训练数据规模从百万级跃升到万亿级，是大模型成功的关键技术。

These are not separate categories from the big three. They are strategies that combine supervised and unsupervised ideas. Self-supervised learning is technically supervised (the model predicts something), but the labels are generated automatically, not by humans.

### Classification vs Regression

These are the two main supervised learning tasks.

| Aspect | Classification | Regression |
|--------|---------------|------------|
| Output | Discrete categories | Continuous numbers |
| Example | "Is this email spam?" | "What will the house price be?" |
| Output space | {cat, dog, bird} | Any real number |
| Loss function | Cross-entropy, accuracy | Mean squared error, MAE |
| Decision | Boundaries between classes | A curve that fits the data |

Classification answers "which category?" Regression answers "how much?"

Some problems can be framed either way. Predicting if a stock goes up or down is classification. Predicting the exact price is regression.

> **【中文解读】**
> 分类和回归是监督学习的两大基本任务。分类预测离散类别（如"垃圾邮件/正常邮件"），回归预测连续数值（如"房价 250 万"）。关键区别在于输出空间：分类的输出是有限的类别集合，回归的输出是任意实数。选择哪种取决于业务需求——有时同一个问题可以用两种方式建模。

### The ML Workflow

Every machine learning project follows the same pipeline, regardless of the algorithm.

```mermaid
flowchart LR
    A[Collect Data] --> B[Clean & Explore]
    B --> C[Feature Engineering]
    C --> D[Split Data]
    D --> E[Train Model]
    E --> F[Evaluate]
    F -->|Not good enough| C
    F -->|Good enough| G[Deploy]
    G --> H[Monitor]
    H -->|Performance drops| A
```

**Collect Data**: Gather raw data. More data is almost always better, but quality matters more than quantity.

**Clean & Explore**: Handle missing values, remove duplicates, visualize distributions, spot anomalies. This step often takes 60-80% of total project time.

**Feature Engineering**: Transform raw data into features the model can use. Turn dates into day-of-week. Normalize numerical columns. Encode categorical variables. Good features matter more than fancy algorithms.

**Split Data**: Divide into training, validation, and test sets. The model trains on training data, you tune hyperparameters on validation data, and you report final performance on test data.

**Train Model**: Feed training data into an algorithm. The algorithm adjusts internal parameters to minimize a loss function.

**Evaluate**: Measure performance on validation/test data. If performance is not acceptable, go back and try different features, algorithms, or hyperparameters.

**Deploy**: Put the model into production where it makes predictions on new data.

**Monitor**: Track performance over time. Data distributions change (data drift), and models degrade. When performance drops, retrain.

### Training, Validation, and Test Splits

This is the most important concept beginners get wrong. You must evaluate your model on data it has never seen during training. Otherwise you are measuring memorization, not learning.

```mermaid
flowchart LR
    subgraph Dataset["Full Dataset (100%)"]
        direction LR
        TR["Training Set (70%)"]
        VA["Validation Set (15%)"]
        TE["Test Set (15%)"]
    end

    TR -->|Train model| M[Model]
    M -->|Tune hyperparameters| VA
    VA -->|Final evaluation| TE
```

| Split | Purpose | When used | Typical size |
|-------|---------|-----------|-------------|
| Training | Model learns from this data | During training | 60-80% |
| Validation | Tune hyperparameters, compare models | After each training run | 10-20% |
| Test | Final unbiased performance estimate | Once, at the very end | 10-20% |

The test set is sacred. You look at it exactly once. If you keep adjusting your model based on test performance, you are effectively training on the test set and your reported numbers are meaningless.

> **【中文解读】**
> 数据划分是 ML 中最容易犯的错误之一。训练集用于学习参数，验证集用于调节超参数和选择模型，测试集只用于最终评估。如果反复在测试集上调优，就等于"偷看答案"，模型性能评估完全失效。对于小数据集，使用 k 折交叉验证可以更可靠地评估性能。

For small datasets, use k-fold cross-validation: split data into k parts, train on k-1 parts, validate on the remaining part, rotate, and average results.

### Overfitting vs Underfitting

```mermaid
flowchart LR
    subgraph UF["Underfitting"]
        U1["Model too simple"]
        U2["High bias"]
        U3["Misses patterns"]
    end

    subgraph GF["Good Fit"]
        G1["Right complexity"]
        G2["Balanced"]
        G3["Generalizes well"]
    end

    subgraph OF["Overfitting"]
        O1["Model too complex"]
        O2["High variance"]
        O3["Memorizes noise"]
    end

    UF -->|Increase complexity| GF
    GF -->|Too much complexity| OF
```

**Underfitting**: The model is too simple to capture the patterns in the data. A straight line trying to fit a curved relationship. Training error is high. Test error is high.

**Overfitting**: The model is too complex and memorizes the training data, including its noise. A wiggly curve that passes through every training point but fails on new data. Training error is low. Test error is high.

**Good fit**: The model captures real patterns without memorizing noise. Training error and test error are both reasonably low.

> **【中文解读】**
> 欠拟合 = 模型太简单，连训练数据中的规律都没学到；过拟合 = 模型太复杂，把训练数据中的噪声都记住了，遇到新数据就"露馅"。好的模型在训练集和测试集上都表现良好。判断标准：如果训练准确率远高于验证准确率，就是过拟合的典型信号。

Signs of overfitting:
- Training accuracy is much higher than validation accuracy
- The model performs well on training data but poorly on new data
- Adding more training data improves performance (the model was memorizing, not learning)

Fixes for overfitting:
- Get more training data
- Reduce model complexity (fewer parameters, simpler architecture)
- Regularization (add a penalty for large weights)
- Dropout (randomly zero out neurons during training)
- Early stopping (stop training when validation error starts increasing)

Fixes for underfitting:
- Use a more complex model
- Add more features
- Reduce regularization
- Train longer

### The Bias-Variance Tradeoff

This is the mathematical framework behind overfitting and underfitting.

**Bias**: Error from wrong assumptions in the model. A linear model has high bias when the true relationship is nonlinear. High bias leads to underfitting.

**Variance**: Error from sensitivity to small fluctuations in the training data. A model with high variance gives very different predictions when trained on different subsets of data. High variance leads to overfitting.

| Model complexity | Bias | Variance | Result |
|-----------------|------|----------|--------|
| Too low (linear model for curved data) | High | Low | Underfitting |
| Just right | Medium | Medium | Good generalization |
| Too high (degree-20 polynomial for 10 points) | Low | High | Overfitting |

Total error = Bias^2 + Variance + Irreducible noise

You cannot reduce irreducible noise (it is randomness in the data itself). You want to find the sweet spot where bias^2 + variance is minimized.

### No Free Lunch Theorem

There is no single algorithm that works best for every problem. An algorithm that performs well on one class of problems will perform poorly on another. This is why data scientists try multiple algorithms and compare results.

> **【拓展：没有免费午餐定理的实践意义】**
> 这个定理告诉我们： Kaggle 竞赛冠军几乎从不只用一种算法，而是用集成方法（XGBoost + LightGBM + 神经网络）融合多个模型。在实际项目中，通常先用多种算法做基线对比（逻辑回归、随机森林、SVM、XGBoost），再选最优的深入调优。AutoML 工具（如 Google Vertex AI、H2O.ai）正是自动化了这个"试多种算法"的过程。

In practice, the choice depends on:
- How much data you have
- How many features there are
- Whether the relationship is linear or nonlinear
- Whether you need interpretability
- How much compute you can afford

### When NOT to Use Machine Learning

ML is powerful but not always the right tool. Before reaching for a model, ask whether you actually need one.

**Do not use ML when:**

- **Rules are simple and well-defined.** Tax calculation, sorting algorithms, unit conversions. If you can write the logic in a few if-statements, a model adds complexity for no benefit.
- **You have no data or very little data.** ML needs examples to learn from. With 10 data points, you cannot train anything meaningful. Collect data first.
- **The cost of being wrong is catastrophic and you need guaranteed correctness.** Medical dosage calculation, nuclear reactor control, cryptographic verification. ML models are probabilistic. They will sometimes be wrong. If "sometimes wrong" is unacceptable, use deterministic methods.
- **A lookup table or heuristic solves the problem.** If a simple threshold or table covers 99% of cases, adding ML increases maintenance cost without meaningful improvement.
- **You cannot explain the decision and explainability is required.** Regulated industries (lending, insurance, criminal justice) sometimes require that every decision be fully explainable. Some ML models are interpretable (linear regression, small decision trees). Most are not.
- **The problem changes faster than you can retrain.** If the rules change daily and retraining takes a week, the model is always stale.

Use this decision flowchart:

```mermaid
flowchart TD
    A["Do you have data?"] -->|No| B["Collect data first or use rules"]
    A -->|Yes| C["Can you write the rules explicitly?"]
    C -->|"Yes, and they are simple"| D["Use rules. Skip ML."]
    C -->|"No, or they are too complex"| E["Is the cost of errors acceptable?"]
    E -->|"No, need guaranteed correctness"| F["Use deterministic methods"]
    E -->|Yes| G["Do you need explainability?"]
    G -->|"Yes, strictly"| H["Use interpretable models only"]
    G -->|"No, or partially"| I["Use ML"]
    I --> J["Do you have enough labeled data?"]
    J -->|Yes| K["Supervised learning"]
    J -->|"Some labels"| L["Semi-supervised learning"]
    J -->|"No labels"| M["Unsupervised or self-supervised"]
```

## Build It | 动手实现

The code in `code/ml_intro.py` implements a nearest centroid classifier from scratch, the simplest possible ML algorithm. It demonstrates the core idea: learn from data, then predict on new data.

> **【中文解读】**
> 最近质心分类器是最简单的 ML 算法：训练时计算每个类别的中心点（均值），预测时将新样本分配给最近的中心。虽然简单，但它完整展示了 ML 的核心流程：fit（从数据学习）→ predict（对新数据预测）→ evaluate（与基线对比）。这个三步模式在从逻辑回归到 Transformer 的所有算法中都是一样的。

### Step 1: Nearest Centroid Classifier from Scratch

The nearest centroid classifier computes the center (mean) of each class in the training data. To predict, it assigns each new point to the class whose center is closest.

```python
class NearestCentroid:
    def fit(self, X, y):
        self.classes = np.unique(y)  # 获取所有唯一类别标签
        self.centroids = np.array([
            X[y == c].mean(axis=0) for c in self.classes  # 计算每个类别的质心（均值向量）
        ])

    def predict(self, X):
        distances = np.array([
            np.sqrt(((X - c) ** 2).sum(axis=1))  # 计算每个样本到各质心的欧氏距离
            for c in self.centroids
        ])
        return self.classes[distances.argmin(axis=0)]  # 返回距离最近的质心对应的类别
```

That is the entire algorithm. Fit computes two means. Predict computes distances. No gradient descent, no iteration, no hyperparameters.

### Step 2: Train on Synthetic Data

We generate a 2D classification dataset with two classes that overlap slightly. The centroid classifier draws a linear decision boundary between the class centers.

```python
rng = np.random.RandomState(42)  # 设置随机种子以保证可复现
X_class0 = rng.randn(100, 2) + np.array([1.0, 1.0])  # 类别 0 的数据：中心在 (1,1) 附近
X_class1 = rng.randn(100, 2) + np.array([-1.0, -1.0])  # 类别 1 的数据：中心在 (-1,-1) 附近
X = np.vstack([X_class0, X_class1])  # 合并所有特征数据
y = np.array([0] * 100 + [1] * 100)  # 创建对应的标签数组
```

### Step 3: Compare Against a Baseline

Every ML model should be compared against a trivial baseline. Here, the baseline predicts a random class. If your ML model does not beat random guessing, something is wrong.

```python
baseline_preds = rng.choice([0, 1], size=len(y_test))  # 随机猜测作为基线
baseline_acc = np.mean(baseline_preds == y_test)  # 计算基线准确率
```

The centroid classifier should get around 90%+ accuracy on this clean dataset. Random baseline gets around 50%.

### Why This Matters

The nearest centroid classifier is trivially simple. It has no hyperparameters, no iteration, no gradient descent. Yet it captures the fundamental ML pattern:

1. **Learn** a representation from training data (the centroids)
2. **Predict** on new data using that representation (nearest distance)
3. **Evaluate** against a baseline (random guessing)

Every ML algorithm, from logistic regression to transformers, follows this same three-step pattern. The representation gets more complex, but the workflow stays the same.

### Step 4: What the Centroid Classifier Cannot Do

The nearest centroid classifier assumes each class forms a single blob. It draws linear decision boundaries. It fails when:

- Classes have multiple clusters (e.g., the digit "1" can be written in several different ways)
- The decision boundary is nonlinear (e.g., one class wraps around another)
- Features have very different scales (distance is dominated by the largest-scale feature)

These limitations motivate every other algorithm you will learn. K-nearest neighbors handles multiple clusters. Decision trees handle nonlinear boundaries. Feature scaling fixes the scale problem. Each lesson builds on the limitations of the previous one.

## Use It | 用框架实现

sklearn provides `NearestCentroid` and synthetic data generators:

```python
from sklearn.neighbors import NearestCentroid
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

# 生成 500 个样本、2 个特征的合成分类数据集
X, y = make_classification(
    n_samples=500, n_features=2, n_redundant=0,
    n_clusters_per_class=1, random_state=42
)
# 按 70/30 比例划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

# 创建最近质心分类器并训练
clf = NearestCentroid()
clf.fit(X_train, y_train)
# 在测试集上评估准确率
print(f"Accuracy: {clf.score(X_test, y_test):.3f}")
```

## Ship It | 产出物

This lesson produces `outputs/prompt-ml-problem-framer.md` -- a prompt that turns vague business problems into concrete ML tasks. Give it a problem description ("we want to reduce churn" or "predict demand for next quarter") and it identifies the learning type, defines the prediction target, lists candidate features, picks a success metric, establishes a baseline, and flags pitfalls like data leakage or class imbalance. Use it at the start of any ML project to avoid building the wrong thing.

## Key Terms | 术语速查表

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Model | "The AI" | A mathematical function with learnable parameters that maps inputs to outputs |
| Training | "Teaching the AI" | Running an optimization algorithm to adjust model parameters so predictions match known outputs |
| Feature | "An input column" | A measurable property of the data that the model uses to make predictions |
| Label | "The answer" | The known output for a training example, used to compute the error signal |
| Hyperparameter | "A setting you tweak" | A parameter set before training that controls the learning process (learning rate, number of layers) |
| Loss function | "How wrong the model is" | A function that measures the gap between predicted and actual outputs, which training tries to minimize |
| Overfitting | "It memorized the test" | The model learned training-specific noise instead of general patterns, so it fails on new data |
| Underfitting | "It didn't learn anything" | The model is too simple to capture the real patterns in the data |
| Generalization | "It works on new data" | The model's ability to make accurate predictions on data it was not trained on |
| Cross-validation | "Testing on different chunks" | Repeatedly splitting data into train/test folds and averaging results, giving a more robust performance estimate |
| Regularization | "Keeping weights small" | Adding a penalty term to the loss function that discourages overly complex models |
| Data drift | "The world changed" | The statistical distribution of incoming data shifts over time, degrading model performance |

## Exercises | 练习题

1. Take any dataset (e.g., Iris, Titanic). Split it 70/15/15 into train/validation/test. Explain why you should not tune hyperparameters on the test set.
2. List three real-world problems. For each one, identify whether it is classification, regression, or clustering, and whether it is supervised or unsupervised.
3. A model gets 99% accuracy on training data but 60% on test data. Diagnose the problem and list three things you would try to fix it.

## Further Reading | 延伸阅读

- [An Introduction to Statistical Learning](https://www.statlearning.com/) - free textbook covering all classical ML methods with practical examples
- [Google's Machine Learning Crash Course](https://developers.google.com/machine-learning/crash-course) - concise visual introduction to ML concepts
- [Scikit-learn User Guide](https://scikit-learn.org/stable/user_guide.html) - the practical reference for implementing ML in Python
