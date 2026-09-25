# Apontação de hiperparâmetros
# 超参数调优


> Os hiperparâmetros são os botões que se giram antes do início do treino.

> Superparâmetros é o treinamento para começar a girar.

**Type:** Build | **类型：** 构建
**Language:**O Python .**语言：**Python
**Prerequisites:** Phase 2, Lesson 11 (Ensemble Methods) | **前置知识：** Phase 2 第 11 课（集成方法）
**Time:** ~90 minutes | **时间：** 约 90 分钟

## Objetivos de aprendizagem

- Implementar a pesquisa em rede, pesquisa aleatória e otimização Bayesiana a partir do zero e comparar a eficiência da amostra
  A partir de zero realização de pesquisa em rede, pesquisa automática e optimização de base, comparar a eficiência de amostragem delas
- Explique por que a pesquisa aleatória supera a pesquisa em rede quando a maioria dos hiperparâmetros tem uma dimensionalidade eficaz baixa
   Explicar por que pesquisa automática na maioria dos superparâmetros válido Dimensão baixa quando melhor que pesquisa em rede
- Construir um loop de otimização Bayesian usando um modelo substitutivo e função de aquisição para guiar a pesquisa
  Utilize modelos de agência e funções de captação construção de um ciclo de optimização para guiar a pesquisa
- Desenhar uma estratégia de sintonização de hiperparâmetros que evite o excesso de encaixe do conjunto de validação através de uma validação cruzada adequada
   Desenho através de um conveniente intervalo de verificação evitar o excesso de requisitos para o conjunto de verificação


> **【中文解读】**
> 超参数 é um modelo de treinamento que é definido antes de ser executado. Não pode ser aplicado em dados.

> **【拓展：超参数调优在大模型训练中的重要性】**
> O treinamento do GPT-4 envolve dezenas de superparâmetros (regularidade de taxa de aprendizagem, tamanho de lote, perda de peso, taxa de queda, etc.), cada treinamento completo custa cerca de US$ 1 bilhão, impossível de usar pesquisa em rede.

## O problema é o problema da introdução

O seu modelo de aumento de gradiente tem uma taxa de aprendizagem, número de árvores, profundidade máxima, min amostras por folha, sub-muestra proporção e coluna proporção de amostras. Isso é seis hiperparâmetros. Se cada um tem 5 valores razoáveis, a grade tem 5 ^ 6 = 15.625 combinações. Treinamento cada leva 10 segundos. Isso é 43 horas de computação para testá-los todos.

> Seu modelo de escala de elevação tem a taxa de aprendizagem, o número de árvores, a maior profundidade, o número de amostras mínimas de pontos de folha, a taxa de sub-tempagem e a taxa de colheita.

A pesquisa de rede é a abordagem óbvia e a pior em escala. A pesquisa aleatória faz melhor com menos computação. A otimização bayesiana faz ainda melhor aprendendo com avaliações passadas. Sabendo qual estratégia usar e quais hiperparâmetros realmente importam, economiza dias de tempo de GPU desperdiçado.

> A pesquisa em rede é o método mais evidente, mas também o pior em grande escala. A pesquisa de menor quantidade é melhor feita com menos cálculos.

> **【中文解读】**
> 超参数调优的核心矛盾:搜索空间大但每次评估成本高――网格搜索穷举所有组合,成本指数增长;随机搜索随机采样,在同样的预算下探索更多区域;贝叶斯优化概率模型(高斯过程) 预测哪些区域可能更好,智能地选择下一个评估点――

## O conceito central.

### Parâmetros vs. Hiperparâmetros

Os parâmetros são aprendidos durante o treinamento (pesos, preconceitos, limiares divididos).

> 参数在训练中学习(权重、偏置、分离值) ――超参数在训练开始前设定,控制学习如何发生──

| Hyperparameter | What it controls | Typical range |
|---------------|-----------------|---------------|
| Learning rate | Step size per update | 0.001 to 1.0 |
| Number of trees/epochs | How long to train | 10 to 10,000 |
| Max depth | Model complexity | 1 to 30 |
| Regularization (lambda) | Overfitting prevention | 0.0001 to 100 |
| Batch size | Gradient estimation noise | 16 to 512 |
| Dropout rate | Fraction of neurons dropped | 0.0 to 0.5 |

| 超参数 | 控制什么 | 典型范围 |
|--------|---------|---------|
| 学习率 | 每次更新的步长 | 0.001 到 1.0 |
| 树的数量/epoch 数 | 训练多久 | 10 到 10,000 |
| 最大深度 | 模型复杂度 | 1 到 30 |
| 正则化 (lambda) | 防止过拟合 | 0.0001 到 100 |
| 批量大小 | 梯度估计噪声 | 16 到 512 |
| Dropout 率 | 丢弃的神经元比例 | 0.0 到 0.5 |

### Pesquisa da Gradeira

A pesquisa de rede avalia cada combinação de valores especificados. É exaustiva e fácil de entender, mas escala exponencialmente com o número de hiperparâmetros.

> 网格搜索评估指定值的每个组合── é extremamente fácil de entender, mas aumenta com o aumento dos índices de quantidade de superparâmetros──

```
Grid for 2 hyperparameters:

  learning_rate: [0.01, 0.1, 1.0]
  max_depth:     [3, 5, 7]

  Evaluations: 3 x 3 = 9 combinations

  (0.01, 3)  (0.01, 5)  (0.01, 7)
  (0.1,  3)  (0.1,  5)  (0.1,  7)
  (1.0,  3)  (1.0,  5)  (1.0,  7)
```

A pesquisa de rede tem uma falha fundamental: se um hiperparâmetro importa e o outro não, a maioria das avaliações é desperdiçada.

> A pesquisa em redes tem uma falha fundamental: se um parâmetro é importante e outro não é importante, a maioria das avaliações é desperdiçada.

### Pesquisa aleatória

Pesquisas aleatórias de amostras de hiperparâmetros de distribuições em vez de uma grade. Com o mesmo orçamento de 9 avaliações, você obtém 9 valores únicos de cada hiperparâmetro.

> Quando você pesquisa a partir de uma distribuição, você obtém 9 valores únicos de cada superparâmetro.

```mermaid
flowchart LR
    subgraph Grid Search
        G1[3 unique learning rates]
        G2[3 unique max depths]
        G3[9 total evaluations]
    end

    subgraph Random Search
        R1[9 unique learning rates]
        R2[9 unique max depths]
        R3[9 total evaluations]
    end
```

Por que o acaso bate à grade (Bergstra & Bengio, 2012):

> Por que fazer isso?

- A maioria dos hiperparâmetros tem baixa dimensionalidade eficaz. Apenas 1-2 de 6 hiperparâmetros geralmente importam para um determinado problema.
  A maioria dos superparâmetros tem uma dimensão válida baixa. De seis, normalmente, apenas 1-2 são importantes para um determinado problema.
- Avaliações de resíduos de busca em rede em dimensões não importantes.
  网格搜索在不重要维度上浪费评估──
- A pesquisa aleatória cobre as dimensões importantes mais densamente para o mesmo orçamento.
  As vezes, as pesquisas cobrem dimensões importantes em um orçamento mais intenso.
- Em 60 ensaios aleatórios, você tem 95% de chances de encontrar um ponto dentro de 5% do ótimo (se existe um no espaço de busca).
  Em 60 vezes de teste random, você tem 95% de probabilidade de encontrar o melhor valor de 5% e dentro se existem os melhores pontos no espaço de pesquisa)

### Optimização Bayesiana

A pesquisa aleatória ignora os resultados. Não aprende que as altas taxas de aprendizagem causam divergências ou que a profundidade 3 supera consistentemente a profundidade 10.

> 随机搜索忽略结果──它不会学到高学习率导致散散或深度 3 总是优于深度 10──贝叶斯优化利用过去的评估来决定下一步搜索哪里──

```mermaid
flowchart TD
    A[Define search space] --> B[Evaluate initial random points]
    B --> C[Fit surrogate model to results]
    C --> D[Use acquisition function to pick next point]
    D --> E[Evaluate the model at that point]
    E --> F{Budget exhausted?}
    F -->|No| C
    F -->|Yes| G[Return best hyperparameters found]
```

Os dois componentes fundamentais:

**Surrogate model:**Um modelo barato para avaliar (geralmente um processo gaussiano) que aproxima a função objetiva cara. Ele dá uma previsão e uma estimativa de incerteza em qualquer ponto do espaço de pesquisa.

> **代理模型：**Um modelo de avaliação barata (normalmente processo de alta), uma função de objetivo quase cara, fornece uma estimativa de previsão e incerteza em qualquer ponto do espaço de pesquisa.

**Acquisition function:**Decide onde avaliar a seguir, equilibrando a exploração (busca perto de pontos bons conhecidos) e a exploração (busca onde há grande incerteza).

> **采集函数：**通过平衡开发 (Beliw Development) 搜索已知好点附近) 和探索 (Beliw Development) 搜索不确定性高的区域) 来决定下一步评估哪里──常见选择:

- **Expected Improvement (EI):**Quanto melhoramento em relação ao melhor atual esperamos neste ponto?
  **期望改进 (EI)：**Neste ponto, o que esperamos de melhor resultado do que o atual?
- **Upper Confidence Bound (UCB):**Previsão mais um múltiplo de incerteza.
  **上置信界 (UCB)：**预测加上不确定性的倍数──更高的 UCB significa que há uma perspectiva ou não explorada──
- **Probability of Improvement (PI):**Qual é a probabilidade de este ponto bater o melhor atual?
  **改进概率 (PI)：**Qual é a probabilidade de um resultado melhor do que o anterior?

A otimização bayesiana normalmente encontra melhores hiperparâmetros do que a pesquisa aleatória com 2-5 vezes menos avaliações.

> Otimizar o desempenho geralmente usa 2-5 vezes menos de tempo para encontrar melhores superparâmetros do que pesquisar acessível.

> **【中文解读】**
> 贝叶斯优化是最智能调整方法――核心组件:代理模型(通常使用高斯过程拟合目标函数) 和采集函数(平衡"探索未知区域"和"利用已知好区域")――每次评估后更新代理模型,采集函数决定下一个评估点――相比随机搜索,贝叶斯优化使用2-5倍较少的评估次数就能找到更好的超值参数,对于高训费的模型有特殊价值――

> **【拓展：Optuna——自动化超参数调优的工业标准】**
> Optuna é um framework de optimização de superparâmetros desenvolvido pela Rede Preferida do Japão, amplamente utilizado em projetos industriais e de competição. Ele suporta a optimização de base de dados (TPE) 采样器 (剪枝) 剪枝 (剪枝) 自動停止不前景的试验) 分布式搜索. O DeepMind AlphaGo e Google's Vizier também usam técnicas similares de optimização de base de dados para melhorar os seus próprios sistemas.

### Parar cedo

Não é necessário que todas as corridas de treinamento terminem. Se uma configuração é claramente ruim após 10 épocas, pare-a e continue.

> Não é necessário que cada treino seja concluído. Se uma configuração não for boa depois de 10 épocas, basta parar e continuar a próxima.

Estratégias:
- **Patience-based:**Suspende se a perda de validação não tiver melhorado durante N épocas consecutivas
  **基于耐心：**Se a perda de testes continuar N 个 époque  não melhorar stop
- **Median pruning:**Parar se o resultado intermediário do ensaio for pior do que a média dos ensaios concluídos no mesmo passo
  **中位数剪枝：**Se o resultado intermediário do teste estiver em comparação com o passo que foi concluído, o diferencial de média do teste ficará parado.
- **Hyperband:**Asignar pequenos orçamentos para muitas configurações, e depois aumentar progressivamente o orçamento para os melhores
  **Hyperband：**Dê-se um orçamento pequeno a muitas dotações, e depois aumentar gradualmente o orçamento das melhores dotações

A banda-mãe é particularmente eficaz. Inicia 81 configurações com 1 época cada, mantém o terceiro maior, dá-lhes 3 épocas, mantém o terceiro maior, etc. Isso encontra boas configurações 10 a 50 vezes mais rápido do que avaliar todas as configurações para o orçamento completo.

> A banda de hiperligação é especialmente eficaz. Compreende 81 configurações em cada uma das épocas, retendo-as em três épocas, retendo-as em três, e assim fazendo-se uma avaliação do orçamento completo, encontrando uma boa configuração de 10 a 50 vezes.

### Programadores de Taxas de Aprendizagem

A taxa de aprendizagem é quase sempre o hiperparâmetro mais importante.

> A taxa de aprendizagem é quase sempre a superparâmetro mais importante.

| Scheduler | Formula | When to use |
|-----------|---------|-------------|
| Step decay | Multiply by 0.1 every N epochs | Classic CNN training |
| Cosine annealing | lr * 0.5 * (1 + cos(pi * t / T)) | Modern default |
| Warmup + decay | Linear increase then cosine decay | Transformers |
| One-cycle | Increase then decrease over one cycle | Fast convergence |
| Reduce on plateau | Reduce by factor when metric stalls | Safe default |

| 调度器 | 公式 | 何时使用 |
|--------|------|---------|
| 阶梯衰减 | 每 N 个 epoch 乘以 0.1 | 经典 CNN 训练 |
| 余弦退火 | lr * 0.5 * (1 + cos(pi * t / T)) | 现代默认 |
| 预热+衰减 | 线性增加后余弦衰减 | Transformer |
| 单周期 | 一个周期内先增后减 | 快速收敛 |
| 平台期衰减 | 指标停滞时按因子减小 | 安全默认 |

### Importância do hiperparâmetro

Não todos os hiperparâmetros importam igualmente. A pesquisa em florestas aleatórias (Probst et al., 2019) e aumento de gradientes mostra padrões consistentes:

> Não são todos os superparâmetros igualmente importantes.

**High importance:**
- Taxa de aprendizagem (sempre sintonizar primeiro)
  學习率 (始终首先调优)
- Número de estimadores/épocas (utilizar paragem precoce em vez de sintonização)
  估计器数量 / epoch 数 (previamente substituído por调优)
- Força de regularização
  Força de regularização

**Medium importance:**
- Profundeza máxima / número de camadas
  Maxima profundidade / Número de níveis
- Minas amostras por folha / decadência de peso
  叶节点最小样本数 / 权重衰减
- Relação de submuestras
  Taxa de desempenho

**Low importance:**
- Características máximas (para florestas aleatórias)
  Maximum Features Number (máximo número de caracteres)
- Escolha de função de ativação específica
  具体激活函数选择
- Dimensão do lote (dentro de um intervalo razoável)
  批量大小(在合理范围内)

Primeiro sintonize as importantes, deixe o resto em padrão.

> Primeiro, é importante, o resto é importante.

### Estratégia prática

```mermaid
flowchart TD
    A[Start with defaults] --> B[Coarse random search: 20-50 trials]
    B --> C[Identify important hyperparameters]
    C --> D[Fine random or Bayesian search: 50-100 trials in narrowed space]
    D --> E[Final model with best hyperparameters]
    E --> F[Retrain on full training data]
```

O fluxo de trabalho concreto:

> 具体工作流:

1. **Start with library defaults.**São escolhidos por profissionais experientes e muitas vezes são 80% do caminho até lá.
   **从库默认值开始。**Eles são escolhidos por profissionais experientes, geralmente já atingindo 80% do efeito.
2. **Coarse random search.**Largos intervalos, 20 a 50 testes, usar paradas iniciais para matar corridas ruins rapidamente.
   **粗粒度随机搜索。**宽范围,20-50 次试点──用早停快速终止差的运行──
3. **Analyze results.**Quais hiperparametros correlacionam com o desempenho?
   **分析结果。** quais são os superparâmetros relacionados com a performance?
4. **Fine search.**Optimização Bayesiana ou busca aleatória focada no espaço estreito. 50-100 ensaios.
   **精细搜索。**Em espaço reduzido, utilizem otimizar o foco ou concentrar-se em busca.
5. **Retrain on all training data**com os melhores hiperparâmetros encontrados.
   Usando o melhor superparâmetro encontrado**所有训练数据上重新训练**- Não.

### Integração de validação cruzada

A sintonização de hiperparâmetros em uma única divisão de validação é arriscada. Os melhores hiperparâmetros podem se encaixar na dobra de validação específica.

> Em um único teste dividido, há risco de que o melhor superparâmetro seja adequado a um teste específico.

- **Outer loop**(avaliação): divide os dados em treino+val e teste.
  **外循环**(Avaliar):将数据分为训练+验证和测试―― relatório não tem desempenho parcial――
- **Inner loop**(tuning): divide o tren+val em tren e val. Encontre os melhores hiperparâmetros.
  **内循环**(调优):将训练+验证分为训练和验证―― encontrar o melhor super参数――

```mermaid
flowchart TD
    D[Full Dataset] --> O1[Outer Fold 1: Test]
    D --> O2[Outer Fold 2: Test]
    D --> O3[Outer Fold 3: Test]
    D --> O4[Outer Fold 4: Test]
    D --> O5[Outer Fold 5: Test]

    O1 --> I1[Inner 5-fold CV on remaining data]
    I1 --> T1[Best hyperparams for fold 1]
    T1 --> E1[Evaluate on outer test fold 1]

    O2 --> I2[Inner 5-fold CV on remaining data]
    I2 --> T2[Best hyperparams for fold 2]
    T2 --> E2[Evaluate on outer test fold 2]
```

Cada dobra externa encontra os seus melhores hiperparâmetros de forma independente.

> Cada extrado encontra independentemente o seu próprio melhor superparâmetro.

Com sklearn:

```python
from sklearn.model_selection import cross_val_score, GridSearchCV
from sklearn.ensemble import GradientBoostingRegressor

inner_cv = GridSearchCV(
    GradientBoostingRegressor(),
    param_grid={
        "learning_rate": [0.01, 0.05, 0.1],
        "max_depth": [2, 3, 5],
        "n_estimators": [50, 100, 200],
    },
    cv=5,
    scoring="neg_mean_squared_error",
)

outer_scores = cross_val_score(
    inner_cv, X, y, cv=5, scoring="neg_mean_squared_error"
)

print(f"Nested CV MSE: {-outer_scores.mean():.4f} +/- {outer_scores.std():.4f}")
```

Esta é cara (5 pistas externas x 5 pistas internas x 27 pontos de grade = 675 pontos de rede) mas dá-lhe uma estimativa de desempenho confiável.

> É muito caro ((5 extensões x 5 extensões x 27 pontos de rede = 675 vezes modelo adequado), mas dá-lhe uma estimativa de desempenho confiável.

### Dicas Práticas

**Start with the learning rate.**É sempre o hiperparâmetro mais importante para métodos baseados em gradientes. Uma taxa de aprendizagem ruim torna tudo o mais irrelevante.

> **从学习率开始。**Para o método baseado em gradientes, ele sempre foi o superparâmetro mais importante. Uma taxa de aprendizagem ruim deixa tudo mais desnecessário. Primeiro, fixar os outros superparâmetros no valor padrão, primeiro, a taxa de aprendizagem.

**Use log-uniform distributions for learning rate and regularization.**A diferença entre 0,001 e 0,01 é tão importante quanto a diferença entre 0,1 e 1,0.

> **对学习率和正则化使用对数均匀分布。**A diferença entre 0,001 e 0,01 e entre 0,1 e 1,0 é igualmente importante.

**Use early stopping instead of tuning n_estimators.**Para a estimativa e redes neurais, definir n_estimatores ou épocas elevadas e deixar que a parada precoce decida quando parar.

> **用早停代替调优 n_estimators。**Para a elevação e a rede neuronal, vai n_estimatores ou época num set alto, deixe-se precocemente decidir quando parar.

**Budget allocation.**Gaste 60% do teu orçamento de sintonia nos dois mais importantes hiperparâmetros. Gaste os 40% restantes em tudo o mais. Os dois primeiros são responsáveis pela maior parte da variação de desempenho.

> **预算分配。**O 60% do orçamento será ajustado e será gasto nos dois principais superparâmetros. O restante 40% será gasto em todos os outros parâmetros.

**Scale matters.**Nunca procure tamanho de lote em uma escala de log (16, 32, 64 são boas). Sempre procure taxa de aprendizagem em uma escala de log. Compare a distribuição da busca com como o hiperparâmetro afeta o modelo.

> **尺度很重要。**永遠不要在数量尺度上搜索批量大小 ((16、32、64 就行) 〜始终在数量尺度上搜索学习率── buscará uma distribuição que se ajuste ao modelo de influência dos superparâmetros──

| Model Type | Top Hyperparameters | Recommended Search | Budget |
|-----------|--------------------|--------------------|--------|
| Random Forest | n_estimators, max_depth, min_samples_leaf | Random search, 50 trials | Low (fast training) |
| Gradient Boosting | learning_rate, n_estimators, max_depth | Bayesian, 100 trials + early stopping | Medium |
| Neural Network | learning_rate, weight_decay, batch_size | Bayesian or random, 100+ trials | High (slow training) |
| SVM | C, gamma (RBF kernel) | Grid on log scale, 25-50 trials | Low (2 params) |
| Lasso/Ridge | alpha | 1D search on log scale, 20 trials | Very low |
| XGBoost | learning_rate, max_depth, subsample, colsample | Bayesian, 100-200 trials + early stopping | Medium |

**When in doubt:**Pesquisa aleatória com 2x o número de hiperparâmetros como ensaios (por exemplo, 6 hiperparâmetros = 12+ ensaios mínimos). Você ficará surpreso com a frequência com que a pesquisa aleatória com 50 ensaios supera a pesquisa de grade cuidadosamente projetada.

> **拿不准时：**随机搜索, o número de testes é 2 vezes maior do que o número de superparâmetros (como 6 超参数 = pelo menos 12 vezes) ⋅ Você ficará surpreso com 50 vezes de testes随机搜索多经常击败精心设计的网格搜索──

## Construí-lo e realizei-o.

> **【中文解读】**
> A partir de zero, a busca em rede e a optimização de Bayes, e usando o mesmo conjunto de dados, a eficiência e o efeito dos três comparados. A busca em rede e todos os componentes.

> **【拓展：Hyperband 和 ASHA——大规模超参数搜索的加速器】**
> O conceito central do algoritmo de hiperbande (em inglês: Hyperband) é uma versão diferente da hiperbande, utilizada pela Microsoft, em NNI e Ray Tune. Durante o treinamento de LLM, um treinamento completo pode exigir US$ 100 milhões, o Hyperband pode reduzir o custo de pesquisa 10 a 50 vezes.
```figure
k-fold-cv
```

## Construí-lo

### Passo 1: Pesquisa da Grade desde o zero

O código está em `code/tuning.py`Implementa a busca em rede, a busca aleatória e um simples optimizador bayesiano a partir do zero.

> `code/tuning.py`O código central realizou a pesquisa de rede a partir de zero, pesquisa automática e simples optimizadores de bacias.

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

### Passo 2: Pesquisa aleatória a partir do zero

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

### Passo 3: Optimização Bayesiana (Simplificada)

A ideia principal: ajustar um processo gaussiano a pares observados (hiperparâmetro, pontuação), em seguida, usar uma função de aquisição para decidir onde procurar a seguir.

> 核心思想:将高斯过程拟合到观察到的 (超参数,分数) 对, então usar a função de captação para decidir o próximo passo de onde.

```python
class SimpleBayesianOptimizer:
    def __init__(self, search_space, n_initial=5):
        self.search_space = search_space
        self.n_initial = n_initial
        self.X_observed = []
        self.y_observed = []

    def _kernel(self, x1, x2, length_scale=1.0):
        dists = np.sum((x1[:, None, :] - x2[None, :, :]) ** 2, axis=2)
        return np.exp(-0.5 * dists / length_scale ** 2)

    def _fit_gp(self, X_new):
        X_obs = np.array(self.X_observed)
        y_obs = np.array(self.y_observed)
        y_mean = y_obs.mean()
        y_centered = y_obs - y_mean

        K = self._kernel(X_obs, X_obs) + 1e-4 * np.eye(len(X_obs))
        K_star = self._kernel(X_new, X_obs)

        L = np.linalg.cholesky(K)
        alpha = np.linalg.solve(L.T, np.linalg.solve(L, y_centered))
        mu = K_star @ alpha + y_mean

        v = np.linalg.solve(L, K_star.T)
        var = 1.0 - np.sum(v ** 2, axis=0)
        var = np.maximum(var, 1e-6)

        return mu, var

    def _expected_improvement(self, mu, var, best_y):
        sigma = np.sqrt(var)
        z = (mu - best_y) / (sigma + 1e-10)
        ei = sigma * (z * norm_cdf(z) + norm_pdf(z))
        return ei

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

O GP surrogado dá duas coisas em cada ponto candidato: uma pontuação prevista (mu) e uma incerteza (var). A Melhoria Esperada equilibra estas: favorece pontos onde o modelo prevê pontuações altas OR onde a incerteza é alta. No início, a maioria dos pontos tem alta incerteza para que o optimizador explore. Mais tarde, foca-se na região mais promissora.

> GP 代理在每个候选点给出两样东西:预测分数(mu) 和不确定性(var) ・期望改善平衡.

### Passo 4: Compare todos os métodos

Execute os três métodos no mesmo objetivo sintético e compare. Esta comparação usa um envolvente simplificado que chama cada optimizador com uma função objetiva direta (sem treinamento de modelo), de modo que a API difere das implementações baseadas em modelos acima:

> Em comparação, todos os três métodos são executados no mesmo objetivo de composição. Este comparativo usa um embalagem simplificado, usando diretamente a função de objetivo para convocar cada optimizador, portanto, a API é diferente da implementação baseada no modelo acima:

```python
def synthetic_objective(params):
    lr = params["learning_rate"]
    depth = params["max_depth"]
    return -(np.log10(lr) + 2) ** 2 - (depth - 4) ** 2 + 10

param_grid = {
    "learning_rate": [0.001, 0.01, 0.1, 1.0],
    "max_depth": [2, 3, 4, 5, 6, 7, 8],
}

grid_best = None
grid_score = -float("inf")
grid_history = []
for combo in itertools.product(*param_grid.values()):
    params = dict(zip(param_grid.keys(), combo))
    score = synthetic_objective(params)
    grid_history.append((params, score))
    if score > grid_score:
        grid_score = score
        grid_best = params

param_dist = {
    "learning_rate": ("log_float", 0.001, 1.0),
    "max_depth": ("int", 2, 8),
}

rand_best = None
rand_score = -float("inf")
rand_history = []
rng = np.random.RandomState(42)
for _ in range(28):
    params = {k: sample(v, rng) for k, v in param_dist.items()}
    score = synthetic_objective(params)
    rand_history.append((params, score))
    if score > rand_score:
        rand_score = score
        rand_best = params

optimizer = SimpleBayesianOptimizer(param_dist, n_initial=5)
bayes_history = []
for _ in range(28):
    params = optimizer.suggest()
    score = synthetic_objective(params)
    optimizer.observe(params, score)
    bayes_history.append((params, score))
bayes_score = max(s for _, s in bayes_history)

print(f"{'Method':<20} {'Best Score':>12} {'Evaluations':>12}")
print("-" * 50)
print(f"{'Grid Search':<20} {grid_score:>12.4f} {len(grid_history):>12}")
print(f"{'Random Search':<20} {rand_score:>12.4f} {len(rand_history):>12}")
print(f"{'Bayesian Opt':<20} {bayes_score:>12.4f} {len(bayes_history):>12}")
```

Com o mesmo orçamento, a otimização bayesiana geralmente encontra a melhor pontuação mais rápida porque não desperdiça avaliações em regiões claramente ruins. A pesquisa aleatória cobre mais terreno do que a pesquisa em grade. A pesquisa em grade só ganha quando você tem muito poucos hiperparâmetros e pode se dar ao luxo de ser exaustivo.

> Sob o mesmo orçamento, a optimização de Beyaz geralmente encontra o melhor resultado mais rápido, pois não avalia o desperdício regional de diferença evidente.

## Use-o com o framework implementado.

### Optuna em prática

Optuna é a biblioteca recomendada para ajustar os hiperparâmetros graves.

> Optuna é uma série de recomendações de alta definição.

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

print(f"Best params: {study.best_params}")
print(f"Best MSE: {study.best_value:.4f}")
```

Características-chave da Optuna:
- `suggest_float(..., log=True)`Para os parâmetros mais procurados na escala de registro (taxa de aprendizagem, regularização)
- `suggest_int`para parâmetros inteiros
- `suggest_categorical`para escolhas discretas
- MedianPruner integrado para parar precocemente maus testes
- `study.trials_dataframe()`para análise

### Optuna com poda

A poda parava testes pouco promissores cedo, economizando grande computação.

> 剪枝及早停止无前景的试验,节省大量计算──以下是模式:

```python
import optuna
from sklearn.model_selection import cross_val_score

def objective(trial):
    params = {
        "learning_rate": trial.suggest_float("lr", 1e-4, 0.5, log=True),
        "max_depth": trial.suggest_int("max_depth", 2, 10),
        "n_estimators": trial.suggest_int("n_estimators", 50, 500),
        "subsample": trial.suggest_float("subsample", 0.5, 1.0),
    }

    model = GradientBoostingRegressor(**params)
    scores = cross_val_score(model, X_train, y_train, cv=3,
                             scoring="neg_mean_squared_error")
    mean_score = -scores.mean()

    trial.report(mean_score, step=0)
    if trial.should_prune():
        raise optuna.TrialPruned()

    return mean_score

pruner = optuna.pruners.MedianPruner(n_startup_trials=10, n_warmup_steps=5)
study = optuna.create_study(direction="minimize", pruner=pruner)
study.optimize(objective, n_trials=200)
```

O `MedianPruner`O processo de corte requer a chamada de um grupo de estudos de medianação.`trial.report()`Para comunicar as métricas intermediárias e `trial.should_prune()`A Comissão deve verificar se o processo deve ser interrompido.`n_startup_trials=10`A redução da quantidade de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados

> `MedianPruner`O valor médio do teste é igual ao valor médio do teste que foi concluído.`trial.report()` relatório indicador intermediário,`trial.should_prune()`检查是否应停止──`n_startup_trials=10` assegure que pelo menos 10 experiências sejam completas antes de a secção de produção ser efetuada.

### - Sim. - Sim. - Sim.

Para experimentos rápidos, sklearn fornece `GridSearchCV`- Não .`RandomizedSearchCV`, e `HalvingRandomSearchCV`- Não .

> 对于快速实验,sklearn 提供 `GridSearchCV`- Não.`RandomizedSearchCV`和 `HalvingRandomSearchCV`- Não .

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
print(f"Best params: {search.best_params_}")
print(f"Best CV MSE: {-search.best_score_:.4f}")
```

Utilização`loguniform`A partir da aprendizagem para a taxa de aprendizagem e regularização.`randint`para hiperparâmetros inteiros.`n_jobs=-1`A bandeira é paralela a todos os núcleos da CPU.

> Para a taxa de aprendizagem e a normalização do uso da aprendizagem`loguniform`◊ para o número total `randint`- Não.`n_jobs=-1`标志跨所有CPU 核心并行──

### Erros comuns na sintonização de hiperparâmetros

**Data leakage through preprocessing.**Se inserir um escalador no conjunto de dados completo antes da validação cruzada, as informações do pliegue de validação vazam para o treinamento.`Pipeline`Assim, só se encaixa na colcha de treinamento.

> **通过预处理的数据泄漏。**Se estiveres em um envelope de dados em formato de envelope, a informação da envelope de envelope será divulgada até ao treino.`Pipeline`- Não, não. - Não, não.

**Overfitting to the validation set.**Usar a validação cruzada em ninhos para estimativas finais de desempenho, ou manter um conjunto de testes separado que você nunca toca durante o sintonização.

> **对验证集过拟合。**运行数千次试验实际上是在验证集上训练―― usando嵌套交叉验证进行最终性能估算,或保留一个调优时永远不碰的独立试验集――

**Searching too narrow a range.**Se o seu melhor valor estiver no limite do seu espaço de pesquisa, você não pesquisou amplamente o suficiente. O valor ideal pode estar fora do seu alcance. Verifique sempre se os melhores parâmetros estão nas bordas.

> **搜索范围太窄。**Se o melhor valor estiver na borda do espaço de busca, você vai procurar pouco. O melhor valor pode estar fora do alcance.

**Ignoring interaction effects.**A taxa de aprendizagem e o número de estimadores interagem fortemente para aumentar a taxa de aprendizagem.

> **忽略交互效应。**A taxa de aprendizagem e o número de estimadores estão a aumentar.

**Not using early stopping for iterative models.**Para aumentar o gradiente e redes neurais, definir n_estimatores ou épocas para um valor alto e usar parada precoce.

> **不对迭代模型使用早停。**Para a escalada e a rede neuronal, os números de tempo são utilizados como um "precursor" ou "precursor".

## Exercícios.

1. Exerça pesquisa em rede e pesquisa aleatória com o mesmo orçamento total (por exemplo, 50 avaliações). Comparar as melhores pontuações encontradas. Exerça o experimento 10 vezes com sementes diferentes. Com que frequência a pesquisa aleatória ganha?
   1. Em comparação com os melhores resultados encontrados, com diferentes sementes, 10 vezes, com diferentes sementes, quantas vezes ganhou?

2. Implementar a banda hiper desde zero. Comece com 81 configurações, cada uma treinada por 1 época. Mantenha os 1/3 superiores em cada rodada e triplica seu orçamento. Compare computação total (suma de todas as épocas em todas as configurações) para executar 81 configurações para o orçamento completo.
   2. Desde zero a realização da hiperbanda. Iniciação de 81 configurações, cada treinamento 1 época.

3. Adicionar um cronograma de taxa de aprendizagem (annelamento de cosina) à implementação de gradientes a partir da lição 11.
   3. Em 11o curso, a elevação do nível de aprendizagem é mais fácil de alcançar.

4. Use Optuna para ajustar um RandomForestClassifier em um conjunto de dados real (por exemplo, o conjunto de dados sobre o cancro da mama de sklearn). Use `optuna.visualization.plot_param_importances(study)`Para ver quais hiperparametros são mais importantes.
   4. Usar Optuna em verdadeiros dados (RandomForestClassifier, Usar)`optuna.visualization.plot_param_importances(study)`Olha quais são os superparâmetros mais importantes.

5. Implementar uma função de aquisição simples (Melhoramento Esperado) e demonstrar exploração versus exploração.
   5.  realizar uma simples função de captação (expectativa de melhoria), demonstrar exploração versus desenvolvimento, desenhar o valor médio e a incerteza do modelo de agência, demonstrar a EI 选择在哪里评估,

> **【中文解读】**
> A taxa de aprendizagem é quase sempre a superparâmetro mais importante. A estratégia de regulação é mais eficaz do que a taxa de aprendizagem fixa: Warmup (de 0 线性增加到目标值) + Cosine Decay (Cosine Decay) 余弦退火下降) é a classificação do treinamento do transformador.

## Termos-chave .

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Hyperparameter | "A setting you choose" | A value set before training that controls the learning process, not learned from data |
| Grid search | "Try every combination" | Exhaustive search over a specified parameter grid. Exponential cost. |
| Random search | "Just sample randomly" | Sample hyperparameters from distributions. Covers important dimensions better than grid search. |
| Bayesian optimization | "Smart search" | Uses a surrogate model of the objective to decide where to evaluate next, balancing exploration and exploitation |
| Surrogate model | "A cheap approximation" | A model (usually Gaussian process) that approximates the expensive objective function from observed evaluations |
| Acquisition function | "Where to look next" | Scores candidate points by balancing expected improvement with uncertainty. EI and UCB are common choices. |
| Early stopping | "Stop wasting time" | Terminate training early when validation performance stops improving |
| Hyperband | "Tournament bracket for configs" | Adaptive resource allocation: start many configs with small budgets, keep the best and increase their budgets |
| Learning rate scheduler | "Change lr during training" | A function that adjusts the learning rate over the course of training for better convergence |

## Mais leitura 延伸阅读

- [Bergstra & Bengio: Random Search for Hyper-Parameter Optimization (2012)](https://jmlr.org/papers/v13/bergstra12a.html)- O jornal que mostrou a grade de batimentos aleatórios
  [Bergstra & Bengio: Random Search for Hyper-Parameter Optimization (2012)](https://jmlr.org/papers/v13/bergstra12a.html)- prova de que o seu trabalho é superior ao de um trabalho
- [Snoek et al., Practical Bayesian Optimization of Machine Learning Algorithms (2012)](https://arxiv.org/abs/1206.2944)-- Optimização Bayesiana para ML
  [Snoek et al., Practical Bayesian Optimization of Machine Learning Algorithms (2012)](https://arxiv.org/abs/1206.2944)- Melhoria do nível de qualidade
- [Li et al., Hyperband: A Novel Bandit-Based Approach (2018)](https://jmlr.org/papers/v18/16-558.html)- o papel de banda hiper
  [Li et al., Hyperband (2018)](https://jmlr.org/papers/v18/16-558.html)- Hiperbanda 论文
- [Optuna: A Next-generation Hyperparameter Optimization Framework](https://arxiv.org/abs/1907.10902)- O jornal Optuna
  [Optuna](https://arxiv.org/abs/1907.10902)- Optuna 论文
- [Probst et al., Tunability: Importance of Hyperparameters (2019)](https://jmlr.org/papers/v20/18-444.html)-- quais os hiperparâmetros importam
  [Probst et al., Tunability (2019)](https://jmlr.org/papers/v20/18-444.html)- 哪些超参数重要
