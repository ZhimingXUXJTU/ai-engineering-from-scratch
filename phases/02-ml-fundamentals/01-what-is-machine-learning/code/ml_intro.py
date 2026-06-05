"""
机器学习基础概念演示：最近质心分类器从零实现。
AI 对应: sklearn 的 NearestCentroid 估计器，本课展示了 sklearn 的核心使用模式 (fit/predict/score)。
ML 核心流程: 数据生成 → 训练 (fit) → 预测 (predict) → 评估 (evaluate) → 与基线对比。
"""
import numpy as np


class NearestCentroid:
    """
    最近质心分类器：最简单的 ML 算法之一。
    训练时计算每个类别的质心（均值向量），预测时将样本分配给最近的质心。
    虽然简单，但完整展示了 fit → predict → evaluate 的 ML 核心流程。
    """

    def __init__(self):
        # 初始化类别标签和质心
        self.classes = None
        self.centroids = None

    def fit(self, X, y):
        """
        从训练数据中学习每个类别的质心。
        参数:
            X: 特征矩阵，形状 (n_samples, n_features)
            y: 标签数组，形状 (n_samples,)
        """
        self.classes = np.unique(y)  # 获取所有唯一类别标签
        self.centroids = np.array([
            X[y == c].mean(axis=0) for c in self.classes  # 计算每个类别的质心（均值向量）
        ])

    def predict(self, X):
        """
        将新样本分配给最近的质心对应的类别。
        参数:
            X: 待预测的特征矩阵
        返回:
            预测的类别标签数组
        """
        distances = np.array([
            np.sqrt(((X - c) ** 2).sum(axis=1))  # 计算每个样本到各质心的欧氏距离
            for c in self.centroids
        ])
        return self.classes[distances.argmin(axis=0)]  # 返回距离最近的质心对应的类别

    def score(self, X, y):
        """
        计算在给定数据上的准确率。
        参数:
            X: 特征矩阵
            y: 真实标签
        返回:
            准确率 (0~1 之间的浮点数)
        """
        return np.mean(self.predict(X) == y)


def generate_classification_data(n_per_class=100, n_features=2, separation=2.0, seed=42):
    """
    生成用于分类的合成数据集。
    两个类别分别以 (separation/2) 和 (-separation/2) 为中心，呈高斯分布。
    参数:
        n_per_class: 每个类别的样本数
        n_features: 特征维度
        separation: 两类中心之间的距离（越大越容易分类）
        seed: 随机种子，保证可复现
    返回:
        X: 特征矩阵, y: 标签数组
    """
    rng = np.random.RandomState(seed)
    center_0 = np.ones(n_features) * (separation / 2)  # 类别 0 的中心点
    center_1 = np.ones(n_features) * (-separation / 2)  # 类别 1 的中心点
    X_class0 = rng.randn(n_per_class, n_features) + center_0  # 围绕中心 0 生成高斯数据
    X_class1 = rng.randn(n_per_class, n_features) + center_1  # 围绕中心 1 生成高斯数据
    X = np.vstack([X_class0, X_class1])  # 合并两个类别的数据
    y = np.array([0] * n_per_class + [1] * n_per_class)  # 创建标签
    shuffle_idx = rng.permutation(len(y))  # 随机打乱顺序
    return X[shuffle_idx], y[shuffle_idx]


def train_test_split(X, y, test_fraction=0.3, seed=42):
    """
    将数据集划分为训练集和测试集。
    参数:
        X: 特征矩阵
        y: 标签数组
        test_fraction: 测试集比例（默认 0.3）
        seed: 随机种子
    返回:
        X_train, X_test, y_train, y_test
    """
    rng = np.random.RandomState(seed)
    n = len(y)
    idx = rng.permutation(n)  # 随机打乱索引
    split = int(n * (1 - test_fraction))  # 计算训练集大小
    return X[idx[:split]], X[idx[split:]], y[idx[:split]], y[idx[split:]]


def random_baseline(y_train, y_test, seed=42):
    """
    随机基线：按照训练集中各类别的比例随机猜测。
    ML 模型至少要超越这个基线才有意义。
    参数:
        y_train: 训练集标签（用于估计类别分布）
        y_test: 测试集标签
        seed: 随机种子
    返回:
        随机猜测的准确率
    """
    rng = np.random.RandomState(seed)
    classes, counts = np.unique(y_train, return_counts=True)
    probs = counts / counts.sum()  # 计算各类别的概率
    preds = rng.choice(classes, size=len(y_test), p=probs)  # 按概率随机抽样
    return np.mean(preds == y_test)


def majority_baseline(y_train, y_test):
    """
    多数类基线：永远预测训练集中最常见的类别。
    在类别不平衡的场景下，这个基线非常重要。
    参数:
        y_train: 训练集标签
        y_test: 测试集标签
    返回:
        多数类预测的准确率
    """
    values, counts = np.unique(y_train, return_counts=True)
    majority_class = values[np.argmax(counts)]  # 找到出现次数最多的类别
    preds = np.full(len(y_test), majority_class)  # 所有样本都预测为多数类
    return np.mean(preds == y_test)


def demo_nearest_centroid():
    """
    演示 1: 最近质心分类器的基本使用。
    生成合成数据 → 训练模型 → 与随机基线和多数类基线对比。
    """
    print("=" * 60)
    print("NEAREST CENTROID CLASSIFIER FROM SCRATCH")
    print("从零实现最近质心分类器")
    print("=" * 60)
    print()

    # 生成 300 个样本的 2D 分类数据，两类中心距离为 2.0
    X, y = generate_classification_data(n_per_class=150, separation=2.0)
    X_train, X_test, y_train, y_test = train_test_split(X, y)

    print(f"Dataset: {len(y)} samples, {X.shape[1]} features, 2 classes")
    print(f"数据集: {len(y)} 个样本, {X.shape[1]} 个特征, 2 个类别")
    print(f"Train: {len(y_train)} samples, Test: {len(y_test)} samples")
    print(f"训练集: {len(y_train)} 个样本, 测试集: {len(y_test)} 个样本")
    print()

    # 训练最近质心分类器
    clf = NearestCentroid()
    clf.fit(X_train, y_train)

    # 在训练集和测试集上评估
    train_acc = clf.score(X_train, y_train)
    test_acc = clf.score(X_test, y_test)

    print(f"Centroids / 质心:")
    for i, c in enumerate(clf.classes):
        print(f"  Class {c}: [{clf.centroids[i][0]:.3f}, {clf.centroids[i][1]:.3f}]")
    print()

    print(f"{'Method':<25} {'Train Acc':>10} {'Test Acc':>10}")
    print(f"{'方法':<25} {'训练准确率':>10} {'测试准确率':>10}")
    print("-" * 50)
    print(f"{'Nearest Centroid':<25} {train_acc:>10.3f} {test_acc:>10.3f}")

    # 与随机基线对比
    rand_acc = random_baseline(y_train, y_test)
    print(f"{'Random Baseline':<25} {'--':>10} {rand_acc:>10.3f}")

    # 与多数类基线对比
    maj_acc = majority_baseline(y_train, y_test)
    print(f"{'Majority Baseline':<25} {'--':>10} {maj_acc:>10.3f}")

    print()
    improvement_over_random = (test_acc - rand_acc) / rand_acc * 100
    print(f"Nearest Centroid beats random baseline by {improvement_over_random:.1f}%")
    print(f"最近质心分类器比随机基线高 {improvement_over_random:.1f}%")


def demo_varying_difficulty():
    """
    演示 2: 类别分离度对准确率的影响。
    分离度越大，两类越容易区分，准确率越高。
    """
    print()
    print("=" * 60)
    print("EFFECT OF CLASS SEPARATION ON ACCURACY")
    print("类别分离度对准确率的影响")
    print("=" * 60)
    print()

    separations = [0.5, 1.0, 1.5, 2.0, 3.0, 5.0]

    print(f"{'Separation':>12} {'Train Acc':>10} {'Test Acc':>10} {'Random':>10}")
    print(f"{'分离度':>12} {'训练准确率':>10} {'测试准确率':>10} {'随机基线':>10}")
    print("-" * 50)

    for sep in separations:
        X, y = generate_classification_data(n_per_class=150, separation=sep)
        X_train, X_test, y_train, y_test = train_test_split(X, y)

        clf = NearestCentroid()
        clf.fit(X_train, y_train)

        train_acc = clf.score(X_train, y_train)
        test_acc = clf.score(X_test, y_test)
        rand_acc = random_baseline(y_train, y_test)

        print(f"{sep:>12.1f} {train_acc:>10.3f} {test_acc:>10.3f} {rand_acc:>10.3f}")

    print()
    print("Small separation: classes overlap heavily, accuracy drops.")
    print("分离度小: 类别严重重叠，准确率下降。")
    print("Large separation: classes are far apart, even this simple model excels.")
    print("分离度大: 类别相距很远，即使这个简单模型也表现出色。")


def demo_higher_dimensions():
    """
    演示 3: 在更高维度空间中的表现。
    对于高斯分布数据，更多特征可以使质心更加区分明显。
    但在真实数据中要注意"维度灾难"问题。
    """
    print()
    print("=" * 60)
    print("NEAREST CENTROID IN HIGHER DIMENSIONS")
    print("高维空间中的最近质心分类器")
    print("=" * 60)
    print()

    dimensions = [2, 5, 10, 20, 50]

    print(f"{'Features':>10} {'Test Acc':>10}")
    print(f"{'特征数':>10} {'测试准确率':>10}")
    print("-" * 25)

    for d in dimensions:
        X, y = generate_classification_data(n_per_class=200, n_features=d, separation=2.0)
        X_train, X_test, y_train, y_test = train_test_split(X, y)

        clf = NearestCentroid()
        clf.fit(X_train, y_train)
        test_acc = clf.score(X_test, y_test)

        print(f"{d:>10d} {test_acc:>10.3f}")

    print()
    print("With Gaussian data and fixed separation, more dimensions help.")
    print("对于高斯数据且固定分离度，更多特征有助于分类。")
    print("The centroids become more distinct in higher-dimensional space.")
    print("质心在高维空间中变得更加可区分。")
    print("Real data behaves differently -- the curse of dimensionality kicks in")
    print("when many features are noise.")
    print("真实数据则不同——当很多特征是噪声时，维度灾难就会出现。")


def demo_multiclass():
    """
    演示 4: 多分类（3 类）最近质心分类器。
    将三个类别的中心分布在等边三角形的三个顶点上。
    """
    print()
    print("=" * 60)
    print("MULTICLASS NEAREST CENTROID (3 CLASSES)")
    print("多分类最近质心分类器（3 个类别）")
    print("=" * 60)
    print()

    rng = np.random.RandomState(42)
    n_per_class = 100
    # 三个类别的中心呈等边三角形分布
    centers = np.array([[2, 0], [-1, 1.7], [-1, -1.7]])
    X_parts = [rng.randn(n_per_class, 2) * 0.8 + c for c in centers]
    X = np.vstack(X_parts)
    y = np.array([0] * n_per_class + [1] * n_per_class + [2] * n_per_class)

    # 随机打乱数据
    shuffle_idx = rng.permutation(len(y))
    X, y = X[shuffle_idx], y[shuffle_idx]

    X_train, X_test, y_train, y_test = train_test_split(X, y)

    clf = NearestCentroid()
    clf.fit(X_train, y_train)

    print(f"3-class problem: {len(y)} samples")
    print(f"3 分类问题: {len(y)} 个样本")
    print(f"Centroids / 质心:")
    for i, c in enumerate(clf.classes):
        print(f"  Class {c}: [{clf.centroids[i][0]:.3f}, {clf.centroids[i][1]:.3f}]")
    print()
    print(f"Test accuracy: {clf.score(X_test, y_test):.3f}")
    print(f"测试准确率: {clf.score(X_test, y_test):.3f}")
    print(f"Random baseline (1/3): {random_baseline(y_train, y_test):.3f}")
    print(f"随机基线 (1/3): {random_baseline(y_train, y_test):.3f}")


if __name__ == "__main__":
    demo_nearest_centroid()
    demo_varying_difficulty()
    demo_higher_dimensions()
    demo_multiclass()
    print()
    print("All ML intro demos complete.")
    print("所有 ML 入门演示完成。")
