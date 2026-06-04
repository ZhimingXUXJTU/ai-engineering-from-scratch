# ML 管线

> 模型不是产品，管线才是。管线是从原始数据到部署预测的一切，每一步都必须可复现。

**类型：** 构建
**语言：** Python
**前置知识：** Phase 2 第 12 课（超参数调优）
**时长：** 约 120 分钟

## 学习目标

- 从零构建 ML 管线，将填充、缩放、编码和模型训练链接为单个可复现对象
- 识别数据泄漏场景，解释管线如何通过只在训练数据上拟合变换器来防止泄漏
- 构建 ColumnTransformer，对数值和类别特征应用不同预处理
- 实现管线序列化，展示同一拟合管线在训练和生产中产生相同结果

## 问题引入

你有一个 notebook，加载数据、用中位数填充缺失值、缩放特征、训练模型、打印准确率。能用。你发布了。

一个月后，有人重训模型得到不同结果。中位数是在包含测试数据的全量数据上计算的（数据泄漏）。缩放参数没有保存，推理时使用了不同的统计量。特征工程代码在训练和服务之间复制粘贴，副本已经分叉。一个类别列在生产中出现了一个编码器从未见过的新值。

这些不是假设，它们是 ML 系统在生产中最常见的失败原因。管线通过将每个变换步骤打包为一个有序、可复现的对象来解决所有问题。

## 核心概念

### 什么是管线

管线是一个有序的数据变换序列，后跟一个模型。每个步骤将上一步的输出作为输入。整个管线在训练数据上拟合一次。推理时，同一个拟合管线变换新数据并产生预测。

管线保证：
- 变换只在训练数据上拟合（无泄漏）
- 推理时应用相同的变换
- 整个对象可以序列化并作为一个制品部署
- 交叉验证按折应用管线，防止微妙的泄漏

### 数据泄漏：静默杀手

数据泄漏在测试集或未来数据的信息污染训练时发生。管线防止最常见的形式。

**泄漏（错误）：** 在划分前对全量数据 fit scaler。
**正确：** 先划分，只在训练集上 fit scaler。

有了管线，你不需要考虑这些。管线自动处理。

### sklearn Pipeline

sklearn 的 `Pipeline` 链接变换器和估计器。它暴露 `.fit()`、`.predict()` 和 `.score()`，按顺序应用所有步骤。

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("model", LogisticRegression()),
])

pipe.fit(X_train, y_train)
predictions = pipe.predict(X_test)
```

当你调用 `pipe.fit(X_train, y_train)` 时：
1. Scaler 对 X_train 调用 `fit_transform`
2. Model 对缩放后的 X_train 调用 `fit`

当你调用 `pipe.predict(X_test)` 时：
1. Scaler 对 X_test 调用 `transform`（不是 fit_transform）
2. Model 对缩放后的 X_test 调用 `predict`

Scaler 在拟合时从未见过测试数据。这就是全部意义。

### ColumnTransformer：不同列不同管线

真实数据集有数值列和类别列需要不同预处理。`ColumnTransformer` 处理这个。

```python
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer

numeric_pipe = Pipeline([
    ("impute", SimpleImputer(strategy="median")),
    ("scale", StandardScaler()),
])

categorical_pipe = Pipeline([
    ("impute", SimpleImputer(strategy="most_frequent")),
    ("encode", OneHotEncoder(handle_unknown="ignore")),
])

preprocessor = ColumnTransformer([
    ("num", numeric_pipe, ["age", "income", "score"]),
    ("cat", categorical_pipe, ["city", "gender", "plan"]),
])

full_pipeline = Pipeline([
    ("preprocess", preprocessor),
    ("model", GradientBoostingClassifier()),
])
```

OneHotEncoder 中的 `handle_unknown="ignore"` 对生产至关重要。当出现新类别时，它产生零向量而不是崩溃。

### 实验追踪

管线使训练可复现，但你还需要追踪跨实验发生了什么：哪些超参数被使用、哪个数据集版本、指标是什么、运行的是什么代码。

**MLflow** 是最常见的开源方案：

```python
import mlflow

with mlflow.start_run():
    mlflow.log_param("max_depth", 5)
    mlflow.log_param("n_estimators", 100)
    mlflow.log_param("learning_rate", 0.1)

    pipe.fit(X_train, y_train)
    accuracy = pipe.score(X_test, y_test)

    mlflow.log_metric("accuracy", accuracy)
    mlflow.sklearn.log_model(pipe, "model")
```

### 模型版本管理

实验追踪后，你需要管理模型版本。哪个在生产？哪个在预发布？哪个是上周的？

MLflow 的模型注册中心提供版本追踪、阶段转换（预发布、生产、归档）、审批工作流和即时回滚。

### 从 Notebook 到生产管线

典型进展：

1. **Notebook 探索**：快速实验、可视化、特征想法
2. **提取函数**：将预处理、特征工程、评估移到模块
3. **构建管线**：将变换链接为 sklearn Pipeline 或自定义类
4. **配置管理**：将所有超参数移到 YAML/JSON 配置
5. **实验追踪**：添加 MLflow 或 wandb 日志
6. **数据验证**：训练前检查模式、分布和缺失值模式
7. **测试**：变换器单元测试、完整管线集成测试
8. **部署**：序列化管线，包装为 API（FastAPI、Flask），容器化

### 常见管线错误

| 错误 | 为什么不好 | 修复 |
|------|----------|------|
| 分割前在全量数据上 fit | 数据泄漏 | 使用 Pipeline 配合 cross_val_score |
| 管线外做特征工程 | 训练和服务的变换不同 | 把所有变换放进 Pipeline |
| 不处理未知类别 | 生产中新值导致崩溃 | OneHotEncoder(handle_unknown="ignore") |
| 硬编码列名 | 模式变化时崩溃 | 使用配置中的列名列表 |
| 无数据验证 | 坏数据上静默错误预测 | 预测前添加模式检查 |
| 训练/服务偏差 | 模型在生产中看到不同特征 | 训练和服务用同一个 Pipeline 对象 |

## 动手实现

### 步骤 1：自定义变换器

```python
class CustomTransformer:
    def __init__(self):
        self.means = None
        self.stds = None

    def fit(self, X):
        self.means = np.mean(X, axis=0)
        self.stds = np.std(X, axis=0)
        self.stds[self.stds == 0] = 1.0
        return self

    def transform(self, X):
        return (X - self.means) / self.stds

    def fit_transform(self, X):
        return self.fit(X).transform(X)
```

### 步骤 2：从零实现 Pipeline

```python
class PipelineFromScratch:
    def __init__(self, steps):
        self.steps = steps

    def fit(self, X, y=None):
        X_current = X.copy()
        for name, step in self.steps[:-1]:
            X_current = step.fit_transform(X_current)
        name, model = self.steps[-1]
        model.fit(X_current, y)
        return self

    def predict(self, X):
        X_current = X.copy()
        for name, step in self.steps[:-1]:
            X_current = step.transform(X_current)
        name, model = self.steps[-1]
        return model.predict(X_current)
```

### 步骤 3：带管线的交叉验证

代码展示带管线的交叉验证如何防止数据泄漏：scaler 在每折的训练数据上分别 fit。

### 步骤 4：sklearn 完整生产管线

完整的管线包含 `ColumnTransformer`、多个预处理路径和一个模型，配合正确的交叉验证和实验日志训练。

详见 `code/pipeline.py`。

## 产出物

本课产出：
- `outputs/prompt-ml-pipeline.md` -- 构建和调试 ML 管线的技能文档
- `code/pipeline.py` -- 从零到 sklearn 的完整管线

## 练习题

1. 构建处理 3 个数值列和 2 个类别列的数据集的管线。用 `ColumnTransformer` 对数值列应用中位数填充+缩放，对类别列应用众数填充+独热编码。用 5 折交叉验证训练。

2. 故意引入数据泄漏：在划分前对全量数据 fit scaler。比较泄漏的交叉验证分数和管线的交叉验证分数。差异多大？

3. 用 `joblib.dump` 序列化你的管线。在另一个脚本中加载并运行预测。验证预测完全相同。

4. 在管线中添加一个自定义变换器，为最重要的两个数值列创建多项式特征（degree 2）。它应该放在管线的什么位置？

5. 为管线设置 MLflow 追踪。用不同超参数运行 5 个实验。用 MLflow UI（`mlflow ui`）比较运行并挑选最佳模型。

## 术语速查表

| 术语 | 实际含义 |
|------|---------|
| 管线 (Pipeline) | 有序的已拟合变换器和模型的序列，作为一个单元应用以防止泄漏 |
| 数据泄漏 (Data Leakage) | 使用训练集之外的信息构建模型，夸大性能估计 |
| ColumnTransformer | 对不同列子集应用不同管线并合并结果 |
| 实验追踪 (Experiment Tracking) | 记录每次训练运行的参数、指标、制品和代码版本 |
| MLflow | 实验追踪、模型注册和部署的开源平台 |
| DVC | 大数据文件的版本控制系统，在 git 中存储哈希，数据在远程存储 |
| 模型注册中心 (Model Registry) | 追踪模型版本并带有阶段标签（预发布、生产、归档）的系统 |
| 训练/服务偏差 | 训练和推理期间数据处理方式的差异，导致静默错误 |
| 可复现性 | 从相同代码、数据和配置获得相同结果的能力 |

## 延伸阅读

- [scikit-learn Pipeline 文档](https://scikit-learn.org/stable/modules/compose.html) - 官方管线参考
- [MLflow 文档](https://mlflow.org/docs/latest/index.html) - 实验追踪和模型注册
- [DVC 文档](https://dvc.org/doc) - 数据版本管理
- [Sculley et al., Hidden Technical Debt in ML Systems (2015)](https://papers.nips.cc/paper/2015/hash/86df7dcfd896fcaf2674f757a2463eba-Abstract.html) - ML 系统复杂性的奠基论文
- [Google ML Best Practices](https://developers.google.com/machine-learning/guides/rules-of-ml) - 实用生产 ML 建议
