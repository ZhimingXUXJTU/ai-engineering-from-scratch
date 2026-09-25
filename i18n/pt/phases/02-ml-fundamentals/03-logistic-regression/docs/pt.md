# Regressão logística
# 逻辑回归


> A regressão logística dobra uma linha reta em uma curva S para responder a perguntas de sim ou não com probabilidades.

> 逻辑回归将直线成 S 形曲线, use概率 responder não é um problema.

**Type:** Build | **类型：** 构建
**Languages:** Python
**Prerequisites:** Phase 2 Lesson 1-2 (What Is ML, Linear Regression) | **前置知识：** Phase 2 第 1-2 课（什么是机器学习、线性回归）
**Time:** ~90 minutes | **时间：** 约 90 分钟

## Objetivos de aprendizagem

- Implementar regressão logística a partir do zero usando a função sigmoide e a perda binária de entropia cruzada
  Desde zero realizando logical regresso, dominar a função Sigmoid e a perda de
- Computação e interpretação de precisão, recall, pontuação F1 e matriz de confusão para classificação binária
  計算并解释精确率 (Preciso) 召回率 (Rememem)  F1 分数和混矩阵
- Explicar por que a MSE não consegue classificar e por que a entropia binária transversal produz uma superfície de custos convexa
   explica por que o erro médio (MSE) não é adequado para tarefas de classe, e por que o binário pode gerar um custo de curvatura
- Construir um modelo de regressão softmax para classificação multi-classe e avaliar as compensações de ajuste de limiar
  Construir Softmax regresso modelo realizar mais classes,并评估值调优的权衡


> **【中文解读】**
> 逻辑归归是二分类的基石使用Sigmoid 函数将线性输出映射到 [0,1] 的概率──虽然称为归归,但它是分类器──sklearn 中的物流回归──信用卡欺诈检查──疾病诊断都可用逻辑归归──

> **【拓展：逻辑回归在工业界的广泛应用】**
> O sistema de previsão de taxas de cliques de anúncios no Facebook foi baseado em regresso lógico (compatível com GBMT); CTR de anúncios de pesquisa do Google (previsão de longo prazo) foi também usado em regresso lógico (mais tarde, elevando para aprendizagem profunda).

## O problema é o problema da introdução

Você quer prever se um tumor é maligno ou benigno, dado seu tamanho. Você tenta regressão linear. Ele produz números como 0,3 ou 1,7 ou -0,5. O que significam? 1,7 é "muito maligno"? -0,5 é "muito benigno"? Regressão linear produz números ilimitados. Classificação precisa de probabilidades limitadas entre 0 e 1, e uma decisão clara: sim ou não.

> Você quer dizer que, de acordo com a grandeza do tumor, é mau ou mau. Você tenta usar o regresso linear. Ele produz 0.3 ou 1.7 ou -0.5 números como este.

A regressão logística resolve isso. Ele toma a mesma combinação linear (wx + b) e passa-a através da função sigmoide, que esmagam qualquer número na faixa (0, 1). A saída é uma probabilidade. Você define um limiar (geralmente 0,5) e toma uma decisão.

> 逻辑归归解决了这个问题──它取同样线性组合 (wx + b),通过Sigmoid 函数将任意数字压缩到 (0, 1) 范围内──输出是一个概率──你设定一个值(通常0.5) 通过Sigmoid 函数将任意数字压缩到 (0, 1) 范围内──输出是一个概率──你设定一个值──通常0.5) 通过Sigmoid 函数将任意数字压缩到 (0, 1) 范围内──输出是一个概率──你设定一个值──通常0.5) 通过Sigmoid 函数将任意数字压缩到 (0, 1) 范围内──输出是一个概率──你设定一个值──你设定一个值──通常0.5) 通过Sigmoid 函数将任意数字压缩到 (0, 1) 范围内──输出一个概率──你设定一个值──你设定一个值──通常0.5) 通过

Este é um dos algoritmos mais utilizados na prática. Apesar de seu nome, a regressão logística é um algoritmo de classificação, não um algoritmo de regressão. O nome vem da função logística (sigmoide) que usa.

> É um dos algoritmos mais amplamente utilizados na prática. Apesar de haver "regressão" em seu nome, o regressão lógica é um algoritmo de classe, não um regressão.

> **【中文解读】**
> A rotação linear não pode ser usada diretamente para a divisão: sua saída é a probabilidade entre 0 e 1 ∞ até +∞), enquanto a divisão precisa de probabilidade entre 0 e 1 ∞.

## O conceito central.

### Por que a regressão linear falha em classificação

Imagine prever a passagem/falha (1/0) com base nas horas de estudo.

> 想象根据学习时间预测通过/不通过(1/0)。线性归归拟合一根直线穿过数据:

```
hours:  1   2   3   4   5   6   7   8   9   10
actual: 0   0   0   0   1   1   1   1   1   1
```

Um ajuste linear pode produzir previsões como -0,2 na hora 1 e 1,3 na hora 10. Estes valores não são probabilidades. Eles vão abaixo de 0 e acima de 1.

> 线性拟合可能在 1 小时内产生 -0.2预测,在 10 小时内产生 1.3预测── esses valores não são probabilidades── eles são inferiores a 0 ou superiores a 1── pior ainda, singles abnormal values (seus 50 horas) vão arrastar toda a linha, alterando a previsão dos proprietários──

A classificação requer uma função que:
- Valores de saída entre 0 e 1 (probabilidades)
  输出 0 到 1  之间的值(概率)
- Cria uma transição acentuada (um limite de decisão)
  创建急剧过渡 (o que é um drama de guerra)
- Não é distorcida por valores fora do limite
  Não é distante da fronteira

> 分类 precisa de uma função, é:

### A função sigmoide

A função sigmoide faz exatamente isto:

> A função sigmoide 函数恰好 fez isso:

```
sigmoid(z) = 1 / (1 + e^(-z))
```

Propriedades:
- Quando z é grande e positivo, sigmoid(z) aproxima-se de 1
  Quando z é grande número, sigmoid(z) 趋近于1
- Quando z é grande e negativo, sigmoid(z) aproxima-se de 0
  Quando z é grande número negativo, sigmoid(z) 趋近于0
- Quando z = 0, sigmoid(z) = 0,5
  Quando z = 0 时,sigmoid(z) = 0,5
- A saída é sempre entre 0 e 1
  输出始终在0和1 之间
- A função é suave e diferenciável em todos os lugares
  Função está em plano

A derivada tem uma forma conveniente: sigmoid'(z) = sigmoid(z) * (1 - sigmoid(z)). Isso torna a computação de gradientes eficiente.

> 导数 tem uma forma fácil:sigmoid'(z) = sigmoid(z) * (1 - sigmoid(z))。 Isso torna a gradiência de cálculo muito alta eficiência。

### Regressão logística = Modelo linear + Sigmoide

O modelo calcula z = wx + b (o mesmo que a regressão linear), e aplica sigmoide:

> 模型计算 z = wx + b(与线性归归相同), então aplicar Sigmoid:

```mermaid
flowchart LR
    X[Input features x] --> L["Linear: z = wx + b"]
    L --> S["Sigmoid: p = 1/(1+e^-z)"]
    S --> D{"p >= 0.5?"}
    D -->|Yes| P[Predict 1]
    D -->|No| N[Predict 0]
```

A saída p é interpretada como P ((y=1\x), a probabilidade de que a entrada pertença à classe 1. O limite de decisão é onde wx + b = 0, o que faz a saída sigmoide exatamente 0,5.

> 输出 p é explicado como P  y = 1  x), isto é, a probabilidade de entrada pertencer a classe 1                                                                                                                                                                                                                                                

### Perda de entropia cruzada binária

Não se pode usar MSE para regressão logística. O MSE com um sigmoide cria uma superfície de custos não convexa com muitos mínimos locais.

> Você não pode voltar a usar MSE;. MSE                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   

```
Loss = -(1/n) * sum(y * log(p) + (1-y) * log(1-p))
```

Por que isto funciona:
- Quando y=1 e p é próximo de 1: log(1) = 0, então a perda é próxima de 0 (correto, baixo custo)
  Quando y = 1 e p 接近 1 时:log(1) = 0, perda perto de 0(正确,低代价)
- Quando y=1 e p está perto de 0: log(0) se aproxima do infinito negativo, então a perda é enorme (erro, alto custo)
  Quando y = 1 e p                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
- Quando y=0 e p está perto de 0: log(1) = 0, então a perda está perto de 0 (correto, baixo custo)
  Quando y = 0 e p                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
- Quando y=0 e p está perto de 1: log(0) se aproxima do infinito negativo, então a perda é enorme (erro, alto custo)
  Quando y = 0 e p 接近 1 时:log(0) 趋向负无穷,损失极大(错误,高代价)

Esta função de perda é convexa para regressão logística, garantindo um único mínimo global.

> Esta função de perda para regresso lógico é uma função de contagem, garantindo que há um único valor mínimo integral.

> **【中文解读】**
> Por que não pode classificar a MSE? Porque a MSE + Sigmoid irá produzir perdas não convexões de função curva, existem muitos valores mínimos locais, gradiente de baixa possível de cará-se.

> **【拓展：交叉熵损失在深度学习中的核心地位】**
> 交叉损失 não é apenas usado para regressão lógica, é a função de perda de sinalização de todas as categorias de redes neurais. GPT é um modelo de linguagem que é essencialmente um símbolo de suavidade.

### Descenso gradual para a Regressão Logística

Os gradientes para a entropia binária cruzada com sigmoide têm uma forma limpa:

> O gradiente de um sistema de divisão de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisões de divisas de divisões de divisões de divisões de divisões de divisões de divisões de divisas de divisas de divisas de divisas de divisas de divisas de divisas de divisas de divisas de divisas de divisas de divisas de divisas de divisas de divisas de divisas de divisas de divisas de divisas de divisas de divisas de divisas de divisas de divisas de divisas de divisas de divisas de divisas de divisas de divisas de divisas de divisas de divisas de divisas de divisas de divisas de divisas

```
dL/dw = (1/n) * sum((p - y) * x)
dL/db = (1/n) * sum(p - y)
```

Estes parecem idênticos aos gradientes de regressão linear. A diferença é que p = sigmoid(wx + b) em vez de p = wx + b. O sigmoid introduz a não linearidade, mas a regra de atualização do gradiente permanece a mesma.

> Estes parecem ser completamente iguais à gradiência de regresso linear. A diferença é que p = sigmoid (wx + b) e não p = wx + b. A sigmoid (sigmoid) introduziu a não-linearidade, mas a gradiência de atualização mantém-se constante.

> **【中文解读】**
> 逻辑归归的梯度公式与线性归归惊人地相似:`dL/dw = (1/n) * sum((p-y)*x)`◊ A única diferença é p = sigmoide(wx+b) e não p = wx+b。 É porque a combinação de sigmoide 和交叉 em matemática "刚好" cancelou os complexos, tornando a forma gradiente muito simples🏼 Esta excelente natureza matemática também se aplica a softmax + 交叉🏼

```mermaid
flowchart TD
    A[Initialize w=0, b=0] --> B[Forward pass: z = wx+b, p = sigmoid z]
    B --> C[Compute loss: binary cross-entropy]
    C --> D["Compute gradients: dw = (1/n) * sum((p-y)*x)"]
    D --> E[Update: w = w - lr*dw, b = b - lr*db]
    E --> F{Converged?}
    F -->|No| B
    F -->|Yes| G[Model trained]
```

### O limite da decisão

Para uma entrada 2D (dois elementos), o limite de decisão é a linha em que:

> Para 2D 输入 (dos traços), a fronteira de decisão é a seguinte:

```
w1*x1 + w2*x2 + b = 0
```

Os pontos de um lado são classificados como 1, os pontos do outro lado como 0. A regressão logística sempre produz um limite de decisão linear. Se você precisar de um limite curvo, adicione características polinômias ou use um modelo não linear.

> Um lado dos pontos é classificado em 1, o outro é classificado em 0;; a regresso lógico sempre produz limites de decisão linear;; se for necessário um limite de curvatura, você deve adicionar mais características, ou usar um modelo não linear;;

### Classificação de classes múltiplas com Softmax

A regressão logística binária lida com duas classes. Para as classes k, use a função softmax:

> Para o tratamento de dois tipos de regresso lógico, use a função Softmax:

```
softmax(z_i) = e^(z_i) / sum(e^(z_j) for all j)
```

Cada classe tem seu próprio vetor de peso. O modelo calcula uma pontuação z_i para cada classe, em seguida, softmax converte as pontuações em probabilidades que somam a 1.

> Cada classe tem seu próprio peso-vivo. O modelo calcula um fração z_i para cada classe, e então o Softmax transformará o fração em probabilidade de 1 e total.

A função de perda torna-se entropia cruzada categórica:

> 损失函数变为分类交叉:

```
Loss = -(1/n) * sum(sum(y_k * log(p_k)))
```

onde y_k é 1 para a classe verdadeira e 0 para todas as outras (coding one-hot).

> Entre eles, um é para o real (ou um é para o real)

### Metricas de avaliação

Para um conjunto de dados com 95% negativo e 5% positivo, um modelo que sempre prevê negativo obtém 95% de precisão, mas é inútil.

> Para um conjunto de dados de 95% de casos negativos, 5% de casos positivos, um modelo de sempre previsão de casos negativos obtém 95% de precisão, mas não serve de nada.

**Confusion Matrix**- Não .

> **混淆矩阵**- Não .

| | Predicted Positive | Predicted Negative |
|---|---|---|
| Actually Positive | True Positive (TP) | False Negative (FN) |
| Actually Negative | False Positive (FP) | True Negative (TN) |

| | 预测为正 | 预测为负 |
|---|---|---|
| 实际为正 | 真正例 (TP) | 假负例 (FN) |
| 实际为负 | 假正例 (FP) | 真负例 (TN) |

**Precision**De todos os positivos previstos, quantos são realmente positivos?
```
Precision = TP / (TP + FP)
```

> **精确率**Entre todas as previsões, há quantas reais?

**Recall**(Sensibilidade): De todos os positivos reais, quantos capturamos?
```
Recall = TP / (TP + FN)
```

> **召回率**(Lígitividade): De todas as amostras reais, nós encontramos o quanto?

**F1 Score**Intervalo de precisão e de recall: equilibra ambas as métricas.
```
F1 = 2 * (Precision * Recall) / (Precision + Recall)
```

> **F1 分数**A taxa de precisão e a taxa de recomposição de um produto são:

Quando priorizar:
- **Precision**: quando os falsos positivos são caros (filtro de spam, não quer bloquear e-mails legítimos)
  **精确率**Quando o preço é alto (tradução: quando o preço é alto)
- **Recall**: quando os falsos negativos são caros (exame de detecção do cancro, não se quer perder um tumor)
  **召回率**Quando você está com o câncer, não quero perder o câncer.
- **F1**Quando você precisa de uma única métrica equilibrada
  **F1**Quando é necessário um indicador de equilíbrio

>  prioritariamente considerar quais são os indicadores:

> **【中文解读】**
> A classificação não pode ser apenas uma avaliação da taxa de precisão. Em casos de desequilíbrio na categoria, como a análise de fraude, apenas 0,1% de casos, a taxa de precisão total é de 99,9% mas não tem valor. A taxa de precisão é uma questão de atenção para o "previsão de que há algo realmente correto", a taxa de recuperação é uma questão de atenção para o "realmente correto que há algo encontrado". F1 é a média de ambos.

> **【拓展：评估指标在真实系统中的选择】**
> Preferência de exame de páginas de lixo em busca no Google Preferência de exame de páginas de lixo em busca no Google Preferência de exame de páginas de lixo em busca no Google Preferência de exame de páginas de lixo em busca de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imagens de imag
```figure
logistic-sigmoid
```

## Construí-lo

### Passo 1: Função Sigmoid e geração de dados

```python
import random
import math

def sigmoid(z):
    z = max(-500, min(500, z))  # 裁剪防止数值溢出
    return 1.0 / (1.0 + math.exp(-z))  # Sigmoid 函数：将任意实数映射到 (0,1)


random.seed(42)
N = 200
X = []
y = []

# 生成类别 0 的数据：中心在 (2,2)
for _ in range(N // 2):
    X.append([random.gauss(2, 1), random.gauss(2, 1)])
    y.append(0)

# 生成类别 1 的数据：中心在 (5,5)
for _ in range(N // 2):
    X.append([random.gauss(5, 1), random.gauss(5, 1)])
    y.append(1)

combined = list(zip(X, y))
random.shuffle(combined)
X, y = zip(*combined)
X = list(X)
y = list(y)

print(f"Generated {N} samples (2 classes, 2 features)")
print(f"Class 0 center: (2, 2), Class 1 center: (5, 5)")
print(f"First 5 samples:")
for i in range(5):
    print(f"  Features: [{X[i][0]:.2f}, {X[i][1]:.2f}], Label: {y[i]}")
```

### Passo 2: Regressão logística a partir do zero

```python
class LogisticRegression:
    def __init__(self, n_features, learning_rate=0.01):
        self.weights = [0.0] * n_features  # 权重初始化为 0
        self.bias = 0.0  # 偏置初始化为 0
        self.lr = learning_rate  # 学习率
        self.loss_history = []  # 记录训练损失

    def predict_proba(self, x):
        z = sum(w * xi for w, xi in zip(self.weights, x)) + self.bias  # 线性组合 z = wx + b
        return sigmoid(z)  # 通过 Sigmoid 得到概率

    def predict(self, x, threshold=0.5):
        return 1 if self.predict_proba(x) >= threshold else 0  # 概率 >= 阈值则预测为 1

    def compute_loss(self, X, y):
        n = len(y)
        total = 0.0
        for i in range(n):
            p = self.predict_proba(X[i])
            p = max(1e-15, min(1 - 1e-15, p))  # 裁剪防止 log(0)
            # 二元交叉熵损失
            total += y[i] * math.log(p) + (1 - y[i]) * math.log(1 - p)
        return -total / n  # 取负号得到正值损失

    def fit(self, X, y, epochs=1000, print_every=200):
        n = len(y)
        n_features = len(X[0])
        for epoch in range(epochs):
            dw = [0.0] * n_features
            db = 0.0
            for i in range(n):
                p = self.predict_proba(X[i])
                error = p - y[i]  # 预测概率 - 真实标签
                for j in range(n_features):
                    dw[j] += error * X[i][j]  # 累积权重梯度
                db += error  # 累积偏置梯度
            # 梯度下降更新参数
            for j in range(n_features):
                self.weights[j] -= self.lr * (dw[j] / n)
            self.bias -= self.lr * (db / n)
            loss = self.compute_loss(X, y)
            self.loss_history.append(loss)
            if epoch % print_every == 0:
                print(f"  Epoch {epoch:4d} | Loss: {loss:.4f} | w: [{self.weights[0]:.3f}, {self.weights[1]:.3f}] | b: {self.bias:.3f}")
        return self

    def accuracy(self, X, y):
        correct = sum(1 for i in range(len(y)) if self.predict(X[i]) == y[i])
        return correct / len(y)


split = int(0.8 * N)
X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]

print("\n=== Training Logistic Regression ===")
model = LogisticRegression(n_features=2, learning_rate=0.1)
model.fit(X_train, y_train, epochs=1000, print_every=200)

print(f"\nTrain accuracy: {model.accuracy(X_train, y_train):.4f}")
print(f"Test accuracy:  {model.accuracy(X_test, y_test):.4f}")
print(f"Weights: [{model.weights[0]:.4f}, {model.weights[1]:.4f}]")
print(f"Bias: {model.bias:.4f}")
```

### Passo 3: Matriz de confusão e métricas a partir do zero

```python
class ClassificationMetrics:
    def __init__(self, y_true, y_pred):
        # 统计混淆矩阵四个值
        self.tp = sum(1 for t, p in zip(y_true, y_pred) if t == 1 and p == 1)  # 真正例
        self.tn = sum(1 for t, p in zip(y_true, y_pred) if t == 0 and p == 0)  # 真负例
        self.fp = sum(1 for t, p in zip(y_true, y_pred) if t == 0 and p == 1)  # 假正例
        self.fn = sum(1 for t, p in zip(y_true, y_pred) if t == 1 and p == 0)  # 假负例

    def accuracy(self):
        total = self.tp + self.tn + self.fp + self.fn
        return (self.tp + self.tn) / total if total > 0 else 0

    def precision(self):
        denom = self.tp + self.fp
        return self.tp / denom if denom > 0 else 0

    def recall(self):
        denom = self.tp + self.fn
        return self.tp / denom if denom > 0 else 0

    def f1(self):
        p = self.precision()
        r = self.recall()
        return 2 * p * r / (p + r) if (p + r) > 0 else 0

    def print_confusion_matrix(self):
        print(f"\n  Confusion Matrix:")
        print(f"                  Predicted")
        print(f"                  Pos   Neg")
        print(f"  Actual Pos     {self.tp:4d}  {self.fn:4d}")
        print(f"  Actual Neg     {self.fp:4d}  {self.tn:4d}")

    def print_report(self):
        self.print_confusion_matrix()
        print(f"\n  Accuracy:  {self.accuracy():.4f}")
        print(f"  Precision: {self.precision():.4f}")
        print(f"  Recall:    {self.recall():.4f}")
        print(f"  F1 Score:  {self.f1():.4f}")


y_pred_test = [model.predict(x) for x in X_test]
print("\n=== Classification Report (Test Set) ===")
metrics = ClassificationMetrics(y_test, y_pred_test)
metrics.print_report()
```

### Passo 4: Análise de limites de decisão

```python
print("\n=== Decision Boundary ===")
w1, w2 = model.weights
b = model.bias
print(f"Decision boundary: {w1:.4f}*x1 + {w2:.4f}*x2 + {b:.4f} = 0")
if abs(w2) > 1e-10:
    print(f"Solved for x2:     x2 = {-w1/w2:.4f}*x1 + {-b/w2:.4f}")

print("\nSample predictions near the boundary:")
test_points = [
    [3.0, 3.0],
    [3.5, 3.5],
    [4.0, 4.0],
    [2.5, 2.5],
    [5.0, 5.0],
]
for point in test_points:
    prob = model.predict_proba(point)
    pred = model.predict(point)
    print(f"  [{point[0]}, {point[1]}] -> prob={prob:.4f}, class={pred}")
```

### Passo 5: Multi-classe com softmax

```python
class SoftmaxRegression:
    def __init__(self, n_features, n_classes, learning_rate=0.01):
        self.n_features = n_features
        self.n_classes = n_classes
        self.lr = learning_rate
        self.weights = [[0.0] * n_features for _ in range(n_classes)]
        self.biases = [0.0] * n_classes

    def softmax(self, scores):
        max_score = max(scores)
        exp_scores = [math.exp(s - max_score) for s in scores]
        total = sum(exp_scores)
        return [e / total for e in exp_scores]

    def predict_proba(self, x):
        scores = [
            sum(self.weights[k][j] * x[j] for j in range(self.n_features)) + self.biases[k]
            for k in range(self.n_classes)
        ]
        return self.softmax(scores)

    def predict(self, x):
        probs = self.predict_proba(x)
        return probs.index(max(probs))

    def fit(self, X, y, epochs=1000, print_every=200):
        n = len(y)
        for epoch in range(epochs):
            grad_w = [[0.0] * self.n_features for _ in range(self.n_classes)]
            grad_b = [0.0] * self.n_classes
            total_loss = 0.0
            for i in range(n):
                probs = self.predict_proba(X[i])
                for k in range(self.n_classes):
                    target = 1.0 if y[i] == k else 0.0
                    error = probs[k] - target
                    for j in range(self.n_features):
                        grad_w[k][j] += error * X[i][j]
                    grad_b[k] += error
                true_prob = max(probs[y[i]], 1e-15)
                total_loss -= math.log(true_prob)
            for k in range(self.n_classes):
                for j in range(self.n_features):
                    self.weights[k][j] -= self.lr * (grad_w[k][j] / n)
                self.biases[k] -= self.lr * (grad_b[k] / n)
            if epoch % print_every == 0:
                print(f"  Epoch {epoch:4d} | Loss: {total_loss / n:.4f}")
        return self

    def accuracy(self, X, y):
        correct = sum(1 for i in range(len(y)) if self.predict(X[i]) == y[i])
        return correct / len(y)


random.seed(42)
X_3class = []
y_3class = []

centers = [(1, 1), (5, 1), (3, 5)]
for label, (cx, cy) in enumerate(centers):
    for _ in range(50):
        X_3class.append([random.gauss(cx, 0.8), random.gauss(cy, 0.8)])
        y_3class.append(label)

combined = list(zip(X_3class, y_3class))
random.shuffle(combined)
X_3class, y_3class = zip(*combined)
X_3class = list(X_3class)
y_3class = list(y_3class)

split_3 = int(0.8 * len(X_3class))
X_train_3 = X_3class[:split_3]
y_train_3 = y_3class[:split_3]
X_test_3 = X_3class[split_3:]
y_test_3 = y_3class[split_3:]

print("\n=== Multi-class Softmax Regression (3 classes) ===")
softmax_model = SoftmaxRegression(n_features=2, n_classes=3, learning_rate=0.1)
softmax_model.fit(X_train_3, y_train_3, epochs=1000, print_every=200)
print(f"\nTrain accuracy: {softmax_model.accuracy(X_train_3, y_train_3):.4f}")
print(f"Test accuracy:  {softmax_model.accuracy(X_test_3, y_test_3):.4f}")

print("\nSample predictions:")
for i in range(5):
    probs = softmax_model.predict_proba(X_test_3[i])
    pred = softmax_model.predict(X_test_3[i])
    print(f"  True: {y_test_3[i]}, Predicted: {pred}, Probs: [{', '.join(f'{p:.3f}' for p in probs)}]")
```

### Passo 6: Ajuste de limiar

```python
print("\n=== Threshold Tuning ===")
print("Default threshold: 0.5. Adjusting the threshold trades precision for recall.\n")

thresholds = [0.3, 0.4, 0.5, 0.6, 0.7]
print(f"{'Threshold':>10} {'Accuracy':>10} {'Precision':>10} {'Recall':>10} {'F1':>10}")
print("-" * 52)

for t in thresholds:
    y_pred_t = [1 if model.predict_proba(x) >= t else 0 for x in X_test]
    m = ClassificationMetrics(y_test, y_pred_t)
    print(f"{t:>10.1f} {m.accuracy():>10.4f} {m.precision():>10.4f} {m.recall():>10.4f} {m.f1():>10.4f}")
```

## Use-o com o framework implementado.

Agora, a mesma coisa com o aprendizado de escobilha.

> Agora, com um pouco de aprendizagem, podemos fazer o mesmo.

```python
from sklearn.linear_model import LogisticRegression as SklearnLR
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import numpy as np

np.random.seed(42)
X_0 = np.random.randn(100, 2) + [2, 2]
X_1 = np.random.randn(100, 2) + [5, 5]
X_sk = np.vstack([X_0, X_1])
y_sk = np.array([0] * 100 + [1] * 100)

X_tr, X_te, y_tr, y_te = train_test_split(X_sk, y_sk, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_tr_sc = scaler.fit_transform(X_tr)
X_te_sc = scaler.transform(X_te)

lr = SklearnLR()
lr.fit(X_tr_sc, y_tr)
y_pred = lr.predict(X_te_sc)

print("=== Scikit-learn Logistic Regression ===")
print(f"Accuracy:  {accuracy_score(y_te, y_pred):.4f}")
print(f"Precision: {precision_score(y_te, y_pred):.4f}")
print(f"Recall:    {recall_score(y_te, y_pred):.4f}")
print(f"F1:        {f1_score(y_te, y_pred):.4f}")
print(f"\nConfusion Matrix:\n{confusion_matrix(y_te, y_pred)}")
print(f"\nClassification Report:\n{classification_report(y_te, y_pred)}")
```

A sua implementação do zero produz o mesmo limite de decisão e métricas. Scikit-learn adiciona opções de resolvedores (liblinear, lbfgs, saga), regularização automática, estratégias de várias classes (one-vs-rest, multinomia), e otimizações de estabilidade numérica.

> Sua realização a partir de zero produzir a mesma fronteira e indicador de decisão.

## Envia-o . Produto .

Esta lição produz:
- `code/logistic_regression.py`- regressão logística a partir do zero com métricas

> 本课产出:
> - `code/logistic_regression.py`- Indicadores de regresso lógico e de avaliação de realização a partir de zero

## Exercícios.

1. Gerar um conjunto de dados que NÃO é linearmente separável (por exemplo, dois círculos concêntricos). Treinar regressão logística e observar sua falha. Depois adicionar características polinômias (x1^2, x2^2, x1*x2) e treinar novamente. Mostrar que a precisão melhora.
   1. - Eu sei.**非**线性可分的数据集 (→ "trenagem de lógica"): (→ "trenagem de lógica")
2. Implementar uma matriz de confusão multi-classe para o modelo softmax de 3 classes. Computação por classe de precisão e recall. Qual classe é mais difícil de classificar?
   2. Por 3 classes Softmax  Modelo de implementação de uma maioria de classes de matrizes de contagem ∙ Calcula a precisão e a taxa de convocação de cada classe ∙ Qual é a classe mais difícil de classificar?
3. Construir uma curva ROC a partir do zero. Para 100 valores de limiar de 0 a 1, calcular a taxa positiva verdadeira e a taxa positiva falsa. Calcular a AUC (área abaixo da curva) usando a regra trapezoidal.
   3. Desde zero construção ROC 曲线── para 100 值, entre 0 a 1 , calcular real例率 e falso例率── utilizando o gradiente de cálculo AUC曲线下面积 () 

## Termos-chave .

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Logistic regression | "Regression for classification" | A linear model followed by a sigmoid function that outputs class probabilities |
| Sigmoid function | "The S-curve" | The function 1/(1+e^(-z)) that maps any real number to the range (0, 1) |
| Binary cross-entropy | "Log loss" | The loss function -[y*log(p) + (1-y)*log(1-p)] that penalizes confident wrong predictions severely |
| Decision boundary | "The dividing line" | The surface where the model's output probability equals 0.5, separating predicted classes |
| Softmax | "Multi-class sigmoid" | A function that converts a vector of scores into probabilities that sum to 1 |
| Precision | "How many selected are relevant" | TP / (TP + FP), the fraction of positive predictions that are actually positive |
| Recall | "How many relevant are selected" | TP / (TP + FN), the fraction of actual positives that the model correctly identifies |
| F1 score | "Balanced accuracy" | The harmonic mean of precision and recall: 2*P*R / (P+R) |
| Confusion matrix | "The error breakdown" | A table showing TP, TN, FP, FN counts for each class pair |
| Threshold | "The cutoff" | The probability value above which the model predicts class 1 (default 0.5, tunable) |
| One-hot encoding | "Binary columns for categories" | Representing class k as a vector of zeros with a 1 at position k |
| Categorical cross-entropy | "Multi-class log loss" | The extension of binary cross-entropy to k classes using one-hot encoded labels |
