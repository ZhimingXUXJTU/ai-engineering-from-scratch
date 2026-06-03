class Vector:
    """向量类 —— AI 中一切数据的数学表示。
    【中文注释】一个词用768维向量表示(词嵌入)，一张图片用百万维向量表示(像素)，
    一个用户用偏好向量表示。向量就是 AI 的"通用语言"。"""

    def __init__(self, components):
        self.components = list(components)
        self.dim = len(self.components)

    def __add__(self, other):
        # 向量加法：对应分量相加。几何意义 = 两个力合成的平行四边形法则。
        return Vector([a + b for a, b in zip(self.components, other.components)])

    def __sub__(self, other):
        # 向量减法：从 other 指向 self 的箭头。
        return Vector([a - b for a, b in zip(self.components, other.components)])

    def __mul__(self, scalar):
        # 标量乘法：缩放向量长度，方向不变。[1,2]*3 = [3,6]
        return Vector([x * scalar for x in self.components])

    def dot(self, other):
        """点积 —— AI 中最核心的数学操作。
        【拓展】点积衡量两个向量的"对齐程度"：
          > 0 表示方向相似（正相关），= 0 表示垂直（无关），< 0 表示方向相反。
        在 Transformer 中，Attention 分数 = Q·K^T（Query 和 Key 的点积），
        这决定了模型"关注"输入中的哪个部分。RAG 检索、推荐系统的核心也是点积。"""
        return sum(a * b for a, b in zip(self.components, other.components))

    def magnitude(self):
        # 模长（向量长度）= 勾股定理的推广：|v| = √(v₁² + v₂² + ... + vₙ²)
        return sum(x**2 for x in self.components) ** 0.5

    def normalize(self):
        """归一化：缩放到长度1，方向不变。
        【拓展】归一化后，点积 = 余弦相似度，不受向量长度干扰。
        Word2Vec、BERT 计算语义相似度时，都先归一化再做点积。"""
        mag = self.magnitude()
        return Vector([x / mag for x in self.components])

    def cosine_similarity(self, other):
        """余弦相似度 cos(θ) = (a·b)/(|a|×|b|)，值域[-1,1]。
        【拓展】这是 NLP 衡量"两个词/句子语义有多像"的标准方法。
        cos=1 方向完全一致，cos=0 完全无关，cos=-1 方向完全相反。
        比"欧氏距离"更好的原因：它只看方向不看长度——
        "我喜欢编程"和"我超级喜欢编程"语义相同，只是程度不同，余弦相似度会很高。"""
        return self.dot(other) / (self.magnitude() * other.magnitude())

    def angle_between(self, other):
        # 两向量的夹角（度），用反余弦函数计算。
        import math
        cos_theta = self.cosine_similarity(other)
        cos_theta = max(-1.0, min(1.0, cos_theta))  # 防止浮点误差超出[-1,1]
        return math.degrees(math.acos(cos_theta))

    def project_onto(self, other):
        """将 self 投影到 other 方向上——即 self 在 other 方向上的"影子"。
        【拓展】公式 proj_b(a) = (a·b / b·b) × b
        残差 = a - proj，残差与 b 垂直（点积=0）。
        应用：(1) 线性回归最小二乘法本质就是投影；(2) PCA 降维把数据投影到主成分方向；
        (3) Transformer 中 Query 投影到 Key 的空间计算相关性。"""
        scalar = self.dot(other) / other.dot(other)
        return Vector([scalar * x for x in other.components])

    def __repr__(self):
        return f"Vector({self.components})"


def is_independent(vectors):
    """判断一组向量是否线性无关——用高斯消元算矩阵的秩。
    【拓展】线性无关 = 没有任何一个向量能被其他向量"凑出来"。
    反例：[1,0], [0,1], [2,1] 中第三个 = 2×第一个 + 第二个，所以这组线性相关。
    在机器学习中：如果两个特征完全线性相关（如房价按美元和按人民币计），
    模型无法区分它们的贡献，权重会变得不稳定。这就是"多重共线性"问题。"""
    n = len(vectors)
    if n == 0:
        return True
    dim = vectors[0].dim
    rows = [v.components[:] for v in vectors]
    rank = 0
    # 高斯消元：逐列找主元，化为行最简形
    for col in range(dim):
        pivot = None
        for row in range(rank, len(rows)):
            if abs(rows[row][col]) > 1e-10:
                pivot = row
                break
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        scale = rows[rank][col]
        rows[rank] = [x / scale for x in rows[rank]]
        for row in range(len(rows)):
            if row != rank and abs(rows[row][col]) > 1e-10:
                factor = rows[row][col]
                rows[row] = [rows[row][j] - factor * rows[rank][j] for j in range(dim)]
        rank += 1
    return rank == n  # 秩 = 向量个数 → 无关


def gram_schmidt(vectors):
    """Gram-Schmidt 正交化：把任意向量组变成互相垂直、长度为1的标准正交基。
    【拓展】算法直觉：每个新向量先减去在已有方向上的"重合部分"（投影），
    只保留全新的方向，然后归一化。
    这就是 QR 分解的原理。QR 分解是数值线性代数的基石——
    解方程组、计算特征值、最小二乘回归都依赖它。"""
    orthonormal = []
    for v in vectors:
        w = v
        for u in orthonormal:
            proj = w.project_onto(u)  # 减去在已有基方向上的投影
            w = w - proj              # 只保留"新的方向"
        if w.magnitude() < 1e-10:     # 向量接近零 = 线性相关，跳过
            continue
        orthonormal.append(w.normalize())
    return orthonormal


class Matrix:
    """矩阵类 —— 矩阵就是一个"变换规则"，把一个向量变成另一个向量。
    【拓展】神经网络的一层 = output = W × input + bias。
    W 就是权重矩阵，矩阵乘法就是整个深度学习的计算核心。
    矩阵可以旋转、缩放、投影向量——这些变换的组合就是模型的"学习"。"""

    def __init__(self, rows):
        self.rows = [list(row) for row in rows]
        self.shape = (len(self.rows), len(self.rows[0]))

    def __matmul__(self, other):
        """矩阵乘法（@运算符）—— 神经网络的核心计算。
        【拓展】矩阵×向量：把高维输入映射到低维（或升维）输出。
        例：3维输入 → [2×3权重矩阵] → 2维输出，这就是网络的一层。
        矩阵×矩阵：两个变换的串联（先做后一个，再做前一个）。"""
        if isinstance(other, Vector):
            return Vector([
                sum(self.rows[i][j] * other.components[j] for j in range(self.shape[1]))
                for i in range(self.shape[0])
            ])
        rows = []
        for i in range(self.shape[0]):
            row = []
            for j in range(other.shape[1]):
                row.append(sum(
                    self.rows[i][k] * other.rows[k][j]
                    for k in range(self.shape[1])
                ))
            rows.append(row)
        return Matrix(rows)

    def transpose(self):
        """转置：行列互换。第i行变第i列。
        【拓展】Attention 中 scores = Q @ K.T（Key 矩阵要转置）。
        线性回归的解析解：w = (X.T @ X)^{-1} @ X.T @ y，到处都有转置。"""
        return Matrix([
            [self.rows[j][i] for j in range(self.shape[0])]
            for i in range(self.shape[1])
        ])

    def rank(self):
        """矩阵的秩 = 线性无关的列（或行）的数量。
        【拓展】秩的直觉：矩阵真正包含的"独立信息"有多少维。
        · 满秩(rank=min(行,列))：信息完整，方程有唯一解
        · 低秩：有冗余信息，方程解不唯一
        · LoRA 微调的关键洞察：大模型的权重更新通常是"低秩"的——
          4096×4096 的更新可以近似为 4096×16 和 16×4096 两个小矩阵，
          参数从 1600万降到 13万（减少 99%），训练成本大幅降低。
          这就是"秩"在 AI 中最惊艳的应用。"""
        rows = [row[:] for row in self.rows]
        m, n = self.shape
        r = 0
        for col in range(n):
            pivot = None
            for row in range(r, m):
                if abs(rows[row][col]) > 1e-10:
                    pivot = row
                    break
            if pivot is None:
                continue
            rows[r], rows[pivot] = rows[pivot], rows[r]
            scale = rows[r][col]
            rows[r] = [x / scale for x in rows[r]]
            for row in range(m):
                if row != r and abs(rows[row][col]) > 1e-10:
                    factor = rows[row][col]
                    rows[row] = [rows[row][j] - factor * rows[r][j] for j in range(n)]
            r += 1
        return r

    def __repr__(self):
        return f"Matrix({self.rows})"


if __name__ == "__main__":
    # === 向量基本运算 ===
    print("=== Vectors ===")
    a = Vector([1, 2, 3])
    b = Vector([4, 5, 6])
    print(f"a = {a}")
    print(f"b = {b}")
    print(f"a + b = {a + b}")          # 向量加法
    print(f"a - b = {a - b}")          # 向量减法
    print(f"a * 3 = {a * 3}")          # 标量乘法
    print(f"a · b = {a.dot(b)}")       # 点积=32，正值说明方向相似
    print(f"|a| = {a.magnitude():.4f}")  # 模长
    print(f"â (normalized) = {a.normalize()}")  # 归一化（单位向量）
    print(f"cosine_similarity(a, b) = {a.cosine_similarity(b):.4f}")  # 余弦相似度≈0.97

    # === 矩阵变换：旋转 ===
    print("\n=== Matrices ===")
    rotation_90 = Matrix([[0, -1], [1, 0]])  # 逆时针旋转90°的变换矩阵
    point = Vector([3, 1])
    rotated = rotation_90 @ point
    print(f"Rotate {point} by 90° → {rotated}")

    # === 向量夹角 ===
    print("\n=== Angle Between Vectors ===")
    v1 = Vector([1, 0])   # x轴方向
    v2 = Vector([0, 1])   # y轴方向
    v3 = Vector([1, 1])   # 45°方向
    print(f"Angle between {v1} and {v2}: {v1.angle_between(v2):.1f} degrees")  # 90°垂直
    print(f"Angle between {v1} and {v3}: {v1.angle_between(v3):.1f} degrees")  # 45°
    print(f"Angle between {v1} and {v1}: {v1.angle_between(v1):.1f} degrees")  # 0°同向

    # === 向量投影 ===
    print("\n=== Projection ===")
    a = Vector([3, 4])
    b = Vector([1, 0])    # x轴方向
    proj = a.project_onto(b)    # a在x轴上的投影 = [3,0]
    residual = a - proj         # 残差 = [0,4]，与x轴垂直
    print(f"a = {a}")
    print(f"b = {b}")
    print(f"proj_b(a) = {proj}")
    print(f"residual = {residual}")
    print(f"residual dot b = {residual.dot(b):.6f}")  # ≈0，验证垂直

    # === 线性相关性 ===
    print("\n=== Linear Independence ===")
    e1 = Vector([1, 0, 0])
    e2 = Vector([0, 1, 0])
    e3 = Vector([0, 0, 1])
    dep = Vector([2, 1, 0])  # = 2×e1 + e2，与e1,e2线性相关
    print(f"{{e1, e2, e3}} independent: {is_independent([e1, e2, e3])}")     # True
    print(f"{{e1, e2, 2*e1+e2}} independent: {is_independent([e1, e2, dep])}")  # False

    # === Gram-Schmidt 正交化 ===
    print("\n=== Gram-Schmidt Orthogonalization ===")
    u1 = Vector([1, 1, 0])
    u2 = Vector([1, 0, 1])
    u3 = Vector([0, 1, 1])
    basis = gram_schmidt([u1, u2, u3])
    for i, vec in enumerate(basis):
        print(f"u{i+1} = {vec}")
    print(f"u1 dot u2 = {basis[0].dot(basis[1]):.6f}")  # ≈0，互相垂直
    print(f"u1 dot u3 = {basis[0].dot(basis[2]):.6f}")  # ≈0
    print(f"u2 dot u3 = {basis[1].dot(basis[2]):.6f}")  # ≈0
    for i, vec in enumerate(basis):
        print(f"|u{i+1}| = {vec.magnitude():.6f}")  # ≈1，长度都是1

    # === 矩阵的秩 ===
    print("\n=== Matrix Rank ===")
    full_rank = Matrix([[1, 0], [0, 1]])          # 单位矩阵，秩=2（满秩）
    rank_deficient = Matrix([[1, 2], [2, 4]])      # 第2行=2×第1行，秩=1（低秩）
    rectangular = Matrix([[1, 0, 0], [0, 1, 0]])   # 2×3矩阵，秩=2
    print(f"Identity 2x2 rank: {full_rank.rank()}")
    print(f"[[1,2],[2,4]] rank: {rank_deficient.rank()}")
    print(f"[[1,0,0],[0,1,0]] rank: {rectangular.rank()}")

    # === 模拟神经网络的一层 ===
    print("\n=== Neural Network Layer (Matrix x Vector) ===")
    import random
    random.seed(42)
    weights = Matrix([[random.gauss(0, 0.1) for _ in range(3)] for _ in range(2)])
    input_vec = Vector([1.0, 0.5, -0.3])
    output = weights @ input_vec  # 矩阵×向量 = 神经网络一层的完整计算
    print(f"Input (3D):  {input_vec}")
    print(f"Output (2D): {output}")
    print("^ This is literally what a neural network layer does.")
