# 功能工程和选择
# 工程与选择的特征


> 一个好功能值一千个数据点.

> 一个好特征.

**Type:** Build | **类型：** 构建
**Languages:** Python
**Prerequisites:** Phase 1 (Statistics for ML, Linear Algebra), Phase 2 Lessons 1-7 | **前置知识：** Phase 1（统计学、线性代数），Phase 2 第 1-7 课
**Time:** ~90 minutes | **时间：** 约 90 分钟

## 学习目标

- 实施数值转换 (标准化,最小最大规模化,日志转换,结) 并解释每一个转换的适当时
  实现数值变化(标准化、Min-Max 缩放、对数量变换、分箱) 并解释各自的适用场景
- 建立一个热点,标签和目标编码的类别特征,并确定目标编码中的数据泄漏风险
  构建独创编码"",标签编码和目标编码,识别目标编码的数据泄漏风险
- 从零开始构建TF-IDF向量表,并解释为什么它超过文本分类的原始字数
  从零构建 TF-IDF到量化器,解释为什么它优于原始词频计数
- 应用基于过器的特征选择 (变异门,相关性,相互信息) 减少维度性
  基于过的特征选择 (方差值,相关性,互信息) 降低维度


> **【中文解读】**
> 特征工程是将原始数据转化为模型能理解的特征.这是ML中最耗时的步骤.标准化,编码,交叉特征,多项式特征都是常用的技巧.

> **【拓展：特征工程 vs 深度学习的自动特征学习】**
> 深度学习的核心优势是自动学习特征(CNN自动提取图像特征、变化器自动提取文本特征),但在表格数据处理工艺特征工程仍然至关重要.

## 问题 问题引入

你有数据集,你选择一个算法,你训练它.结果是中等的.你试着一个更精彩的算法.仍然是中等的.你花了一个星期调整超参数.边缘改进.

> 你有一个数据集. 你选择了一个算法. 你训练它. 结果平平. 你试图更花哨的算法.

然后有人将原始数据转化为更好的功能, 一个简单的物流回归比你的调节的梯度增强组件更好.

> 然后有人把原始数据转换为更好的特征,一个简单的逻辑回归打败了你调整的梯度升级集成.

在经典的ML中,数据的表示比算法的选择更重要.一个"平方录像"和"卧室数量"的房价模型将比一个"地址作为原始字符串"的模型更重要,无论学习者多么复杂.算法只能根据你给出的东西工作.

> 在经典ML中,数据表示比算法更重要.一个使用"面积"和"卧室数"的房价模型会打败"地址原始字符串"的模型,无论学习器多么复杂.算法只能处理给你的东西.

功能工程是将原始数据转化为模型更容易找到的表现.功能选择是抛弃没有添加信号的噪音特性的过程.它们一起是经典 ML 中最大的杆活动.

> 特征工程是将原始数据转换为使模式更容易被模型发现的表示过程.特征选择是放弃的过程.

> **【中文解读】**
> "数据和特征决定了ML的上限,模型和算法只是接近这个上限. "好的特征可以让简单模型打败复杂模型.

## 概念的核心概念

### 功能管道

```mermaid
flowchart LR
    A[Raw Data] --> B[Handle Missing Values]
    B --> C[Numerical Transforms]
    B --> D[Categorical Encoding]
    B --> E[Text Features]
    C --> F[Feature Interactions]
    D --> F
    E --> F
    F --> G[Feature Selection]
    G --> H[Model-Ready Data]
```

### 数字特征

基本的数字很少是模型准备的.

> 原始数字很少能直接用于模型.

**Scaling:**设置功能在相同的范围,以使距离基于的算法 (K-Means, KNN, SVM) 对待所有功能均等.最小最大扩展地图到 [0, 1].标准化 (z-score) 地图到 mean=0, std=1.

> **缩放：**将特征放到相同范围,使基于距离算法的 K-Means、KNN、SVM) 等待所有特征──Min-Max 缩放映射到 [0, 1]──标准化(z-score)映射到平均值=0、标准差=1──

**Log transform:**压缩了右倾分布 (收入,人口,字数). 转化了乘法关系为加值关系.

> **对数变换：**压缩右偏分布 收入、人口、词频) △将乘法关系变为加法关系.

**Binning:**转换连续值为类别. 当特征与目标之间的关系非线性,但步骤式 (例如年龄组) 时有用.

> **分箱：**将连续值转换为类型. 当特征与目标的关系不线性,但在阶梯式中有用.

**Polynomial features:**允许线性模型以更多的特性来捕捉非线性关系.

> **多项式特征：**创建x^2、x^3、x1*x2项――让线性模型以更多特征为代价捕捉非线性关系――

### 类别特征

模型需要数字,类别需要编码.

> 模型需要数字.类别需要编码.

**One-hot encoding:**创建一个对每个类别的二进制列. "色 = 红/蓝/绿"变成三个列: is_red, is_blue, is_green.适用于低cardinality功能,但在许多类别中爆炸.

> **独热编码：**为每类创建一个二进制列――"颜色 = 红/蓝/绿" 变成三列:is_red、is_blue、is_green。对低基数的特征效果好,但类别多时会爆炸──

**Label encoding:**绘制每个类别的整数:红=0,蓝=1,绿=2. 引入错误的排序 (模型可能认为绿 >蓝 >红). 仅适用于基于树的模型,分为单个值.

> **标签编码：**将每个类别映射到整数:红=0、蓝=1、绿=2──引入虚假排序模型可能认为绿 >蓝 >红) 只适合单个值分化的树模型──

**Target encoding:**强大但危险:高数据泄漏风险.只需基于训练数据计算,应应用于测试数据.

> **目标编码：**必须仅在训练数据上计算并应用到测试数据中.

### 文字的特征

**Count vectorizer:**计算每一个词在文档中出现在多少次. "猫坐在床上"变成 {the: 2, cat: 1, sat: 1, on: 1, mat: 1}.

> **词频向量化：**计算每个词在文档中出现的次数――"猫坐在床上" 变成 {the: 2, cat: 1, sat: 1, on: 1, mat: 1}──

**TF-IDF:**频率-反文档频率. 根据文档中的独特性,重量词. "the"等常见词变得较低. 罕见的,独特的词变得更重.

> **TF-IDF：**词频-逆文档频率──按词在文档中的唯一性加权──常见词如"the"获得低权重──稀有、有区别的词获得高权重──

```
TF(word, doc) = count(word in doc) / total words in doc
IDF(word) = log(total docs / docs containing word)
TF-IDF = TF * IDF
```

### 缺失的价值观

实际数据有漏洞.

> 实际数据有空洞.

- **Drop rows:**只有缺失数据是罕见的,随机的
  **删除行：**只有缺失数据很少,随时
- **Mean/median imputation:**简单,保持分布形状 (中位数更坚固到异常)
  **均值/中位数填充：**简单,保持分布形状 (中位数对异常值更鲁棒)
- **Mode imputation:**对于类别特征
  **众数填充：**用于类型特征
- **Indicator column:**在计算之前添加一个二进制列"was_this_missing".数据缺失的事实本身可以是信息性的
  **指示列：**填充前添加二进制列"是_这是_缺失"――数据缺失本身可能是信息性
- **Forward/backward fill:**时间序列数据
  **前向/后向填充：**用时间序列数据

### 功能互动

有时,这种关系是结合中的.单独的"身高"和"体重"比"BMI =体重/身高^2"更少的预测性.

> 有时关系在组合中――"身高"和"体重"单独不如"BMI = 体重 / 身高^2"有预测力――特征交互会增加空间特征,因此使用领域知识选择正确的组合――

### 功能选择

没有相关的功能会增加噪音,增加训练时间,并可能导致过度适应.

> 更多特征不一定更好. 无关特征增加噪音. 增加训练时间并可能导致过适应.

**Filter methods (pre-model):**
- 相关性:消除高度相互相关的特征 (冗余)
  相关性:移除高度相关的特征 (冗余)
- 互通信息:衡量知道特征的程度,减少了对目标的不确定性
  互信息:衡量知道一个特征可以减少目标多少不确定性
- 变异门:删除几乎不变的功能
  方差值:移除几乎不变的特征

**Wrapper methods (model-based):**
- L1规律化 (Lasso):将无关性的特征权重达到完全零
  :将无关特征权重驱动到恰好为零
- 复发性功能消除:训练,删除最不重要的功能,重复
  递归特征消除:训练,移除最不重要的特征,重复

**Why selection matters:**具有10个好功能的模型通常会超过具有10个好功能和90个噪音的模型.噪音的功能使模型有机会过度适应不通用的训练数据模式.

> **为什么选择很重要：**一个具有10个好特征的模型通常胜过了10个好特征加上90个噪音特征的模型――噪音特征给了模型在训练数据中过于适合不通用的模式的机会――

## 建立它,实现它.

> **【中文解读】**
> 从零实现常见特征变化:标准化(零平均值单位差) ‧ 微-最大归结化(缩小到0-1) ‧ 对数量变化(处理长尾分布) ‧ 分箱(连续值离散化) ‧ 每种变化适用于不同场景对数量变化适合收入等右偏分分布,标准化适合 KNN/SVM等距离敏感算法──
```figure
feature-scaling
```

## 建立它

### 步骤1:从零开始进行数值转换

```python
import math


def min_max_scale(values):
    min_val = min(values)
    max_val = max(values)
    if max_val == min_val:
        return [0.0] * len(values)
    return [(v - min_val) / (max_val - min_val) for v in values]


def standardize(values):
    n = len(values)
    mean = sum(values) / n
    variance = sum((v - mean) ** 2 for v in values) / n
    std = math.sqrt(variance) if variance > 0 else 1.0
    return [(v - mean) / std for v in values]


def log_transform(values):
    return [math.log(v + 1) for v in values]


def bin_values(values, n_bins=5):
    min_val = min(values)
    max_val = max(values)
    bin_width = (max_val - min_val) / n_bins
    if bin_width == 0:
        return [0] * len(values)
    result = []
    for v in values:
        bin_idx = int((v - min_val) / bin_width)
        bin_idx = min(bin_idx, n_bins - 1)
        result.append(bin_idx)
    return result


def polynomial_features(row, degree=2):
    n = len(row)
    result = list(row)
    if degree >= 2:
        for i in range(n):
            result.append(row[i] ** 2)
        for i in range(n):
            for j in range(i + 1, n):
                result.append(row[i] * row[j])
    return result
```

### 步骤2:从零开始编码类别

```python
def one_hot_encode(values):
    categories = sorted(set(values))
    cat_to_idx = {cat: i for i, cat in enumerate(categories)}
    n_cats = len(categories)

    encoded = []
    for v in values:
        row = [0] * n_cats
        row[cat_to_idx[v]] = 1
        encoded.append(row)

    return encoded, categories


def label_encode(values):
    categories = sorted(set(values))
    cat_to_int = {cat: i for i, cat in enumerate(categories)}
    return [cat_to_int[v] for v in values], cat_to_int


def target_encode(feature_values, target_values, smoothing=10):
    global_mean = sum(target_values) / len(target_values)

    category_stats = {}
    for feat, target in zip(feature_values, target_values):
        if feat not in category_stats:
            category_stats[feat] = {"sum": 0.0, "count": 0}
        category_stats[feat]["sum"] += target
        category_stats[feat]["count"] += 1

    encoding = {}
    for cat, stats in category_stats.items():
        cat_mean = stats["sum"] / stats["count"]
        weight = stats["count"] / (stats["count"] + smoothing)
        encoding[cat] = weight * cat_mean + (1 - weight) * global_mean

    return [encoding[v] for v in feature_values], encoding
```

### 步骤3:从零开始的文字功能

> 第三步:文本特征──词频向量(CountVectorizer) 统计每一个词在文档中出现的次数;TF-IDF 在词频基础上乘以逆文档频率,降低常见词权重、提升稀有词权重──学习的`TfidfVectorizer`是这个实现的生产版.

```python
def count_vectorize(documents):
    vocab = {}
    idx = 0
    for doc in documents:
        for word in doc.lower().split():
            if word not in vocab:
                vocab[word] = idx
                idx += 1

    vectors = []
    for doc in documents:
        vec = [0] * len(vocab)
        for word in doc.lower().split():
            vec[vocab[word]] += 1
        vectors.append(vec)

    return vectors, vocab


def tfidf(documents):
    n_docs = len(documents)

    vocab = {}
    idx = 0
    for doc in documents:
        for word in doc.lower().split():
            if word not in vocab:
                vocab[word] = idx
                idx += 1

    doc_freq = {}
    for doc in documents:
        seen = set()
        for word in doc.lower().split():
            if word not in seen:
                doc_freq[word] = doc_freq.get(word, 0) + 1
                seen.add(word)

    vectors = []
    for doc in documents:
        words = doc.lower().split()
        word_count = len(words)
        tf_map = {}
        for word in words:
            tf_map[word] = tf_map.get(word, 0) + 1

        vec = [0.0] * len(vocab)
        for word, count in tf_map.items():
            tf = count / word_count
            idf = math.log(n_docs / doc_freq[word])
            vec[vocab[word]] = tf * idf
        vectors.append(vec)

    return vectors, vocab
```

### 步骤4:从零开始错失的值归因

> 第四步:缺失值填充.平均值填充对正态分布数据合适,中位数对异常值鲁棒,众多用于类特征.关键技巧:加缺失指示列"这个值是否缺失"本身可能是预测性信号.

```python
def impute_mean(values):
    present = [v for v in values if v is not None]
    if not present:
        return [0.0] * len(values), 0.0
    mean = sum(present) / len(present)
    return [v if v is not None else mean for v in values], mean


def impute_median(values):
    present = sorted(v for v in values if v is not None)
    if not present:
        return [0.0] * len(values), 0.0
    n = len(present)
    if n % 2 == 0:
        median = (present[n // 2 - 1] + present[n // 2]) / 2
    else:
        median = present[n // 2]
    return [v if v is not None else median for v in values], median


def impute_mode(values):
    present = [v for v in values if v is not None]
    if not present:
        return values, None
    counts = {}
    for v in present:
        counts[v] = counts.get(v, 0) + 1
    mode = max(counts, key=counts.get)
    return [v if v is not None else mode for v in values], mode


def add_missing_indicator(values):
    return [0 if v is not None else 1 for v in values]
```

### 步骤5:从零开始选择功能

> 第五步:特征选择. 皮尔逊相关系数衡量线性关系. -1到 +1);互信息能捕获非线性关系,更全面但需要分离.`SelectKBest`,我知道.`VarianceThreshold`是这些方法的生产封装.

```python
def correlation(x, y):
    n = len(x)
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    cov = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / n
    std_x = math.sqrt(sum((xi - mean_x) ** 2 for xi in x) / n)
    std_y = math.sqrt(sum((yi - mean_y) ** 2 for yi in y) / n)
    if std_x == 0 or std_y == 0:
        return 0.0
    return cov / (std_x * std_y)


def mutual_information(feature, target, n_bins=10):
    feat_min = min(feature)
    feat_max = max(feature)
    bin_width = (feat_max - feat_min) / n_bins if feat_max != feat_min else 1.0
    feat_binned = [
        min(int((f - feat_min) / bin_width), n_bins - 1) for f in feature
    ]

    n = len(feature)
    target_classes = sorted(set(target))

    feat_bins = sorted(set(feat_binned))
    p_feat = {}
    for b in feat_bins:
        p_feat[b] = feat_binned.count(b) / n

    p_target = {}
    for t in target_classes:
        p_target[t] = target.count(t) / n

    mi = 0.0
    for b in feat_bins:
        for t in target_classes:
            joint_count = sum(
                1 for fb, tv in zip(feat_binned, target) if fb == b and tv == t
            )
            p_joint = joint_count / n
            if p_joint > 0:
                mi += p_joint * math.log(p_joint / (p_feat[b] * p_target[t]))

    return mi


def variance_threshold(features, threshold=0.01):
    n_features = len(features[0])
    n_samples = len(features)
    selected = []

    for j in range(n_features):
        col = [features[i][j] for i in range(n_samples)]
        mean = sum(col) / n_samples
        var = sum((v - mean) ** 2 for v in col) / n_samples
        if var >= threshold:
            selected.append(j)

    return selected


def remove_correlated(features, threshold=0.9):
    n_features = len(features[0])
    n_samples = len(features)

    to_remove = set()
    for i in range(n_features):
        if i in to_remove:
            continue
        col_i = [features[r][i] for r in range(n_samples)]
        for j in range(i + 1, n_features):
            if j in to_remove:
                continue
            col_j = [features[r][j] for r in range(n_samples)]
            corr = abs(correlation(col_i, col_j))
            if corr >= threshold:
                to_remove.add(j)

    return [i for i in range(n_features) if i not in to_remove]
```

### 步骤 6: 完整的管道和演示

```python
import random


def make_housing_data(n=200, seed=42):
    random.seed(seed)
    data = []
    for _ in range(n):
        sqft = random.uniform(500, 5000)
        bedrooms = random.choice([1, 2, 3, 4, 5])
        age = random.uniform(0, 50)
        neighborhood = random.choice(["downtown", "suburbs", "rural"])
        has_pool = random.choice([True, False])

        sqft_with_missing = sqft if random.random() > 0.05 else None
        age_with_missing = age if random.random() > 0.08 else None

        price = (
            50 * sqft
            + 20000 * bedrooms
            - 1000 * age
            + (50000 if neighborhood == "downtown" else 10000 if neighborhood == "suburbs" else 0)
            + (15000 if has_pool else 0)
            + random.gauss(0, 20000)
        )

        data.append({
            "sqft": sqft_with_missing,
            "bedrooms": bedrooms,
            "age": age_with_missing,
            "neighborhood": neighborhood,
            "has_pool": has_pool,
            "price": price,
        })
    return data


if __name__ == "__main__":
    data = make_housing_data(200)

    print("=== Raw Data Sample ===")
    for row in data[:3]:
        print(f"  {row}")

    sqft_raw = [d["sqft"] for d in data]
    age_raw = [d["age"] for d in data]
    prices = [d["price"] for d in data]

    print("\n=== Missing Value Handling ===")
    sqft_missing = sum(1 for v in sqft_raw if v is None)
    age_missing = sum(1 for v in age_raw if v is None)
    print(f"  sqft missing: {sqft_missing}/{len(sqft_raw)}")
    print(f"  age missing: {age_missing}/{len(age_raw)}")

    sqft_indicator = add_missing_indicator(sqft_raw)
    age_indicator = add_missing_indicator(age_raw)
    sqft_imputed, sqft_fill = impute_median(sqft_raw)
    age_imputed, age_fill = impute_mean(age_raw)
    print(f"  sqft filled with median: {sqft_fill:.0f}")
    print(f"  age filled with mean: {age_fill:.1f}")

    print("\n=== Numerical Transforms ===")
    sqft_scaled = standardize(sqft_imputed)
    age_scaled = min_max_scale(age_imputed)
    sqft_log = log_transform(sqft_imputed)
    age_binned = bin_values(age_imputed, n_bins=5)
    print(f"  sqft standardized: mean={sum(sqft_scaled)/len(sqft_scaled):.4f}, std={math.sqrt(sum(v**2 for v in sqft_scaled)/len(sqft_scaled)):.4f}")
    print(f"  age min-max: [{min(age_scaled):.2f}, {max(age_scaled):.2f}]")
    print(f"  age bins: {sorted(set(age_binned))}")

    print("\n=== Categorical Encoding ===")
    neighborhoods = [d["neighborhood"] for d in data]

    ohe, ohe_cats = one_hot_encode(neighborhoods)
    print(f"  One-hot categories: {ohe_cats}")
    print(f"  Sample encoding: {neighborhoods[0]} -> {ohe[0]}")

    le, le_map = label_encode(neighborhoods)
    print(f"  Label encoding map: {le_map}")

    te, te_map = target_encode(neighborhoods, prices, smoothing=10)
    print(f"  Target encoding: {({k: round(v) for k, v in te_map.items()})}")

    print("\n=== Text Features ===")
    descriptions = [
        "large modern house with pool",
        "small cozy cottage near downtown",
        "spacious family home with large yard",
        "modern apartment downtown with view",
        "rustic cabin in rural area",
    ]
    cv, cv_vocab = count_vectorize(descriptions)
    print(f"  Vocabulary size: {len(cv_vocab)}")
    print(f"  Doc 0 non-zero features: {sum(1 for v in cv[0] if v > 0)}")

    tf, tf_vocab = tfidf(descriptions)
    print(f"  TF-IDF vocabulary size: {len(tf_vocab)}")
    top_words = sorted(tf_vocab.keys(), key=lambda w: tf[0][tf_vocab[w]], reverse=True)[:3]
    print(f"  Doc 0 top TF-IDF words: {top_words}")

    print("\n=== Polynomial Features ===")
    sample_row = [sqft_scaled[0], age_scaled[0]]
    poly = polynomial_features(sample_row, degree=2)
    print(f"  Input: {[round(v, 4) for v in sample_row]}")
    print(f"  Polynomial: {[round(v, 4) for v in poly]}")
    print(f"  Features: [x1, x2, x1^2, x2^2, x1*x2]")

    print("\n=== Feature Selection ===")
    feature_matrix = [
        [sqft_scaled[i], age_scaled[i], float(sqft_indicator[i]), float(age_indicator[i])]
        + ohe[i]
        for i in range(len(data))
    ]

    print(f"  Total features: {len(feature_matrix[0])}")

    surviving_var = variance_threshold(feature_matrix, threshold=0.01)
    print(f"  After variance threshold (0.01): {len(surviving_var)} features kept")

    surviving_corr = remove_correlated(feature_matrix, threshold=0.9)
    print(f"  After correlation filter (0.9): {len(surviving_corr)} features kept")

    binary_prices = [1 if p > sum(prices) / len(prices) else 0 for p in prices]
    print("\n  Mutual information with target:")
    feature_names = ["sqft", "age", "sqft_missing", "age_missing"] + [f"neigh_{c}" for c in ohe_cats]
    for j in range(len(feature_matrix[0])):
        col = [feature_matrix[i][j] for i in range(len(feature_matrix))]
        mi = mutual_information(col, binary_prices, n_bins=10)
        print(f"    {feature_names[j]}: MI={mi:.4f}")

    print("\n  Correlation with price:")
    for j in range(len(feature_matrix[0])):
        col = [feature_matrix[i][j] for i in range(len(feature_matrix))]
        corr = correlation(col, prices)
        print(f"    {feature_names[j]}: r={corr:.4f}")
```

## 用它实现框架

> **【拓展：sklearn Pipeline 的工业级实践】**
> 结算的ColumnTransformer + Pipeline是特征工程的最佳实践:将数值特征和类型特征分别处理,组合成一个端到端的流水线――这确保了训练集和测试集使用完全相同的变化,避免了数据泄露――在 Kaggle 竞争和工业项目中,Pipeline是标准的做法它让代码可复制、可部署、可维护――

通过使用 scikit-learn,这些转换是可组合的管道:

> 通过简单学习,这些变化可组合为管线:

```python
from sklearn.preprocessing import StandardScaler, OneHotEncoder, PolynomialFeatures  # 预处理变换器
from sklearn.impute import SimpleImputer  # 缺失值填充
from sklearn.feature_extraction.text import TfidfVectorizer  # 文本 TF-IDF 向量化
from sklearn.feature_selection import mutual_info_classif, VarianceThreshold  # 特征选择
from sklearn.compose import ColumnTransformer  # 按列分组处理
from sklearn.pipeline import Pipeline  # 构建端到端流水线

numeric_pipe = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler()),
])

categorical_pipe = Pipeline([
    ("encoder", OneHotEncoder(sparse_output=False)),
])

preprocessor = ColumnTransformer([
    ("num", numeric_pipe, ["sqft", "age"]),
    ("cat", categorical_pipe, ["neighborhood"]),
])
```

图书馆版本增加了边缘处理,稀疏的矩阵支持和管道组合,但数学是相同的.

> 从零版本准确显示每个变化内部发生了什么.库版本增加了边界情况处理,稀疏矩阵支持和管线组合,但数学原理是相同的.

## 运送它.

这一课产生了:
- `outputs/prompt-feature-engineer.md`- 系统地从原始数据中进行工程的提示

> 本课产出:
> - `outputs/prompt-feature-engineer.md`- 一个从原始数据系统化工程特征的提示词

> **【拓展：自动化特征工程——Featuretools 和 AutoML】**
> 功能工具是一个开源自动化特征工程库,可以自动从关系型数据中生成数千个特征 (聚合,时间差,交叉特征等).

> **【中文解读】**
> TF-IDF (字频逆文档频率) 是文本特征工程的经典方法:TF 衡量文档中的词频率,IDF 衡量词在所有文档中的稀少程度.常见词:如"的"、"是")IDF 低,特征词:如"量子"",区块链")IDF 高――TF-IDF 虽然简单,但在文本分类中至今仍然有效的基线特征.

## 练习题

1. 加入强大的规模化 (使用中位数和四分之一间范围而不是平均和标准偏差) 数字变化.将其与极端异常值的数据的标准规模化进行比较.
   1. 在数值变换中增加缩,使用中位数和四位数距离代替平均值和标准差) 缩与标准缩放比较.
2. 实现单独的目标编码:对于每个行,计算目标平均值,排除该行的目标值. 展示如何减少过度适应与天真的目标编码相比.
   2. 实现留一法目标编码:对每行,计算排除该行自身目标值的目标平均值.
3. 建立一个自动化特征选择管道,结合变异门,相关性过和相互信息排名.将其应用到住房数据集,并将模型性能 (使用简单的线性回归) 与所有特征和选定的特征进行比较.
   3. 构建自动化特征选择管线,结合方差值,相关性过和互信息排序. 应用到住房数据集,比较使用所有特征和选择特征的模型性能.

## 关键词 快速查找表

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Feature engineering | "Making new columns" | Transforming raw data into representations that expose patterns to the model |
| Standardization | "Making it normal" | Subtracting the mean and dividing by standard deviation so the feature has mean=0 and std=1 |
| One-hot encoding | "Making dummy variables" | Creating one binary column per category, where exactly one column is 1 for each row |
| Target encoding | "Using the answer to encode" | Replacing each category with the average target value for that category, with smoothing to prevent overfitting |
| TF-IDF | "Fancy word counts" | Term Frequency times Inverse Document Frequency: words weighted by how distinctive they are across the corpus |
| Imputation | "Filling in blanks" | Replacing missing values with estimated values (mean, median, mode, or model-predicted) |
| Feature selection | "Throwing out bad columns" | Removing features that add noise or redundancy, keeping only those with signal about the target |
| Mutual information | "How much one thing tells you about another" | A measure of the reduction in uncertainty about variable Y gained by observing variable X |
| Data leakage | "Accidentally cheating" | Using information during training that would not be available at prediction time, giving falsely optimistic results |

## 继续阅读 继续阅读

- [Feature Engineering and Selection (Max Kuhn & Kjell Johnson)](http://www.feat.engineering/)- 免费的网上书,涵盖了整个功能工程领域
  [Feature Engineering and Selection (Max Kuhn & Kjell Johnson)](http://www.feat.engineering/)- 涵盖工程全景的免费在线书籍
- [scikit-learn Preprocessing Guide](https://scikit-learn.org/stable/modules/preprocessing.html)- 对于所有标准转换的实用参考
  [scikit-learn 预处理指南](https://scikit-learn.org/stable/modules/preprocessing.html)- 所有标准变化的实用参考
- [Target Encoding Done Right (Micci-Barreca, 2001)](https://dl.acm.org/doi/10.1145/507533.507538)- 目标编码的原始文件
  [Target Encoding Done Right (Micci-Barreca, 2001)](https://dl.acm.org/doi/10.1145/507533.507538)- 带平滑的目标编码原始论文
