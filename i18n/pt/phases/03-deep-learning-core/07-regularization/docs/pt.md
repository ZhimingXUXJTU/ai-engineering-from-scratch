# Regularização .

> O seu modelo tem 99% de dados de treinamento e 60% de dados de teste.

> **【中文解读】**O modelo de treinamento é 99% mas o teste é apenas 60% é "scorrer" em vez de "aprender"                                                                                                                                                                                                                                                 

**Type:** Build
**Languages:** Python
**Prerequisites:** Lesson 03.06 (Optimizers)
**Time:** ~75 minutes

## Objetivos de aprendizagem

- Implementar o abandono com escala invertida, declínio de peso L2, normalização de lote, normalização de camada e RMSNorm a partir do zero
- Medir a lacuna de precisão dos testes de trem e diagnosticar o sobreajuste utilizando experimentos de regularização
- Explique por que os transformadores usam a LayerNorm em vez da BatchNorm e por que os LLM modernos preferem a RMSNorm
- Aplicar a combinação correta de técnicas de regularização com base na gravidade do sobreajuste

> **【中文解读】**Este capítulo tem como objetivo entender por que o Transformer usa LayerNorm e não o BatchNorm, bem como por que o Llama/Mistral usa RMSNorm.

## O problema é o problema da introdução

Uma rede neural com parâmetros suficientes pode memorizar qualquer conjunto de dados. Isto não é hipotético - Zhang et al. (2017) provou isso treinando redes padrão na ImageNet com rótulos aleatórios. As redes alcançaram perda de treinamento quase zero em atribuições de rótulos completamente aleatórias. Eles memorizaram um milhão de pares aleatórios de entrada e saída sem padrão para aprender. Perda de treinamento foi perfeita. A precisão do teste foi zero.

> Uma rede neural com parâmetros suficientes pode lembrar qualquer conjunto de dados. Isto não é uma hipótese. Zhang 等人 (2017) provou isso através de um treinamento de padrões de etiquetas aleatórias na ImageNet. A rede alcançou quase zero perdas de treinamento na distribuição de etiquetas completamente aleatórias. Eles se lembram de um milhão de pessoas sem regras de ingressos-sais aleatórios em comparação com a perda de treinamento.

Este é o problema de sobre-ajustamento, e piora à medida que os modelos ficam maiores. GPT-3 tem 175 bilhões de parâmetros. O conjunto de treinamento tem cerca de 500 bilhões de tokens. Com tantos parâmetros, o modelo tem capacidade suficiente para memorizar pedaços significativos dos dados de treinamento verbalmente. Sem regularização, ele apenas regurgitará exemplos de treinamento em vez de aprender padrões generalizáveis.

> É um problema de adaptação, com o modelo se tornando maior e pior. O GPT-3 tem 1750 bilhões de parâmetros. O treinamento acumula cerca de 5000 bilhões de tokens.

A diferença entre o desempenho do treinamento e o desempenho dos testes é a diferença de sobre-ajustamento. Cada técnica desta aula ataca essa lacuna de um ângulo diferente. A interrupção obriga a rede a não depender de nenhum neurônio. A perda de peso impede que qualquer peso se torne muito grande. A normalização de lote suaviza o cenário de perdas para que o optimizador encontre mínimos mais planos e mais generalizáveis. A normalização de camadas faz a mesma coisa, mas funciona onde a normalização de lote falha (pequenas parcelas, sequências de comprimento variável). A RMSNorm faz isso 10% mais rápido, soltando o cálculo médio. Cada técnica é simples. Juntos, são a diferença entre um modelo que memoriza e um que generaliza.

> A diferença entre o desempenho de treinamento e o desempenho de teste é a diferença de super-adaptation. Cada tipo de tecnologia desta aula ataca essa diferença de diferentes ângulos. O depósito de redes forçadas não depende de nenhum neurônio. A redução de peso impede o aumento de peso de qualquer peso. A redução de peso é muito simples. A redução de massa e o aumento de massa e o aumento de massa e o aumento de massa e o aumento de massa e o aumento de massa e o aumento de massa.

> **【中文解读】**Modelo parametros mais, mais fácil de adaptar. GPT-3 tem 1750 bilhões de parametros,5 bilhões de tokens  não está normalizado, ele só vai memorizar treinamento dados  Cada forma de normalização do meio de ataque de diferentes ângulos                                                                                                                                                                                                                                                                                                                                                                                                                                                              

> **【拓展：大模型的正则化策略】**GPT-4 e Llama 3 são muito simples: AdamW 权重衰减 (wd=0.01) + Dropout (p=0.1) + RMSNorm。 não é necessário técnicas de regularização complexas。

## O conceito central.

### O Espectro de Super-Fitamento é um sistema de transmissão.

Cada modelo fica em algum lugar no espectro, desde o sub-ajustamento (demasiado simples para capturar o padrão) até o sobreajustamento (tão complexo que capta ruído).

> Cada modelo está em uma posição na cadeia de espectro de desadaptado (extremamente simples e incompreensível) a ultraadaptado (extremamente complexo para capturar ruído).

```mermaid
graph LR
    Under["Underfitting<br/>Train: 60%<br/>Test: 58%<br/>Model too simple"] --> Good["Good Fit<br/>Train: 95%<br/>Test: 92%<br/>Generalizes well"]
    Good --> Over["Overfitting<br/>Train: 99.9%<br/>Test: 65%<br/>Memorized noise"]

    Dropout["Dropout"] -->|"Pushes left"| Over
    WD["Weight Decay"] -->|"Pushes left"| Over
    BN["BatchNorm"] -->|"Pushes left"| Over
    Aug["Data Augmentation"] -->|"Pushes left"| Over
```

### Deixar de lado.

A técnica de regularização mais simples com a interpretação mais elegante.

> A técnica de normalização mais simples e mais elegante é explicada. Durante o treino, a probabilidade de que a saída de cada neurônio seja de zero é definida.

```
output = activation(z) * mask    where mask[i] ~ Bernoulli(1 - p)
```

Com p = 0,5, metade dos neurônios são centrais em cada passagem para a frente. A rede deve aprender representações redundantes porque não pode prever quais neurônios estarão disponíveis. Isso impede a co-adaptação - neurônios aprendendo a confiar em outros neurônios específicos estarem presentes.

> Quando p = 0,5 , metade dos neurônios são colocados em zero por cada transmissão anterior. A rede deve aprender a expressão redundante, pois não pode prever quais neurônios são usáveis. Isso impede a co-adaptação de neurônios dependentes da existência de outros neurônios específicos.

A interpretação do conjunto: uma rede com N neurônios e desligamento cria 2^N sub-redes possíveis (cada combinação das quais os neurônios estão ligados ou desligados). O treinamento com abandono, aproximadamente, treina simultaneamente todas as sub-rede 2^N, cada uma em mini-partidas diferentes. No momento do teste, utiliza todos os neurônios (sem interrupção) e escala as saídas em (1 - p) para corresponder ao valor esperado durante o treino. Isto é equivalente a uma média das previsões de 2^N sub-rede -- um conjunto maciço de um único modelo.

> 集成解释: uma rede com N 个神经元和中断的网络创建 2^N 个可能的子网络(神经元开关或关的每种组合) ⋅ usando dropout 训练大约同时训练所有2^N 个子网络,每个在不同的迷你上――测试时,你使用所有神经元(无中断)并按 (1 - p) 缩放输出与匹配值训练期间的期望――这等于对2^N 个子网络的预测平均取 单个模型实现大规模集成──

Na prática, a escalação é aplicada durante o treinamento em vez de testes (abandonamento invertido):

```
During training:  output = activation(z) * mask / (1 - p)
During testing:   output = activation(z)   (no change needed)
```

Isto é mais limpo porque o código de teste não precisa saber sobre o abandono.

> É melhor, porque o código de teste não precisa saber a existência de abandono.

Taxas de defeito: p = 0,1 para transformadores, p = 0,5 para MLPs, p = 0,2 a 0,3 para CNNs.

> 默认比率:Transformer 用 p = 0,1,MLP 用 p = 0,5,CNN 用 p = 0,2-0,3── dropout 越高 = 正则化越强 = 欠拟合风险越大──

> **【拓展：Dropout 在 BERT 和 GPT 中的不同用法】**BERT utiliza Dropout p=0.1                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    

### Desconto de peso (L2 regularização) 权重减减 (L2 正则化)

Adicionar a magnitude quadrada de todos os pesos à perda:

> A expansão quadrada do peso da propriedade aumentará para a perda:

```
total_loss = task_loss + (lambda / 2) * sum(w_i^2)
```

O gradiente do termo regularização é lambda * w. Isso significa que a cada passo, cada peso é reduzido para zero por uma fração proporcional à sua magnitude. pesos grandes são penalizados mais. O modelo é empurrado para soluções onde nenhum peso único domina.

> O gradiente de regularização é lambda * w. Isto significa que em cada passo, cada peso é reduzido a zero em proporção à sua amplitude em proporção à sua amplitude.

Por que isso ajuda a generalização: os modelos super ajustados tendem a ter grandes pesos que amplificam o ruído nos dados de treinamento.

> Por que isso ajuda a generalizar: modelos super-adaptados geralmente têm muito peso, aumentam o ruído dos dados de treinamento.

O hiperparâmetro lambda controla a resistência.

> lambda 超参数控制强度──valor típico:

- 0,01 para AdamW em transformadores
  Tradução do idioma: 0.01 Usado para Transformer 上的 AdamW
- 1e-4 para SGD nas emissoras de televisão
  Tradução do inglês:
- 0,1 para os modelos com grande sobreajuste
  0.1 Usar modelos gravemente sobreadaptados

Como discutido na lição 06: a perda de peso e a regularização de L2 são equivalentes em SGD mas não em Adam.

> Como se pode ver no capítulo 6, o peso decrece e L2 se torna normal no SGD, mas não é igual no Adam.

### Normalização de lote.

Normalize a saída de cada camada através do mini-batch antes de passá-lo para a próxima camada.

> Em que cada camada de saída seja transferida para a camada inferior, a mini-partida será reintegrada.

Para um mini-parcelamento de ativas em alguma camada:

>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              

```
mu = (1/B) * sum(x_i)           (batch mean)
sigma^2 = (1/B) * sum((x_i - mu)^2)   (batch variance)
x_hat = (x_i - mu) / sqrt(sigma^2 + eps)   (normalize)
y = gamma * x_hat + beta        (scale and shift)
```

Gamma e beta são parâmetros aprendíveis que permitem que a rede desface a normalização se isso for otimizado. sem eles, você estaria forçando a saída de cada camada a ser de variação de unidade zero-media, o que pode não ser o que a rede quer.

> Gamma 和 beta é um parâmetro que pode ser aprendido, se o melhor for, pode fazer a retirada da rede se tornar uma unificação. Sem eles, você forçará cada nível de saída a ser de divisão de unidades de valor médio zero, isso não é o que a rede quer.

**Training vs inference split:**Durante o treino, mu e sigma provêm do mini-batch atual. Durante a inferência, você usa médias correntes acumuladas durante o treino (média móvel exponencial com impulso = 0,1, ou seja, 90% antigo + 10% novo).

> **训练与推理的区别：**訓練時,mu 和 sigma 来自当前ミニ-batch──推理時,使用訓練期間累积的运行平均值(指数移动平均,动量 = 0.1,即90% 旧值 + 10% 新值)──

Por que o BatchNorm funciona ainda é debatido. O artigo original alegou que reduz "a mudança de covariados interna" (a distribuição de entradas de camadas mudando à medida que as camadas anteriores atualizam). Santurkar et al. (2018) mostrou que esta explicação é errada. A razão real é que o BatchNorm torna o cenário de perdas mais suave. Os gradientes são mais preditivos, as constantes de Lipschitz são menores, e o optimizador pode dar passos maiores com segurança. É por isso que o BatchNorm permite que você use taxas de aprendizagem mais altas e converja mais rápido.

> BatchNorm por que é válido ainda há controvérsia. O artigo original afirma que reduz a "deformação de variação interna" (deformação de mudanças de configuração) (Santurkar et al. (2018)).

BatchNorm tem uma limitação fundamental: depende das estatísticas de lote. Com o tamanho do lote 1, a média e a variância são sem sentido. Com lotes pequenos (< 32), as estatísticas são barulhentas e prejudicam o desempenho. Isso importa para tarefas como detecção de objetos (onde a memória limita o tamanho do lote) e modelagem de linguagem (onde os comprimentos de sequência variam).

> BatchNet tem uma limitação fundamental: depende da quantidade de dados. Tamanho do lote é de 1 时, valor médio e diferença de tamanho não significam nada.

> **【中文解读】**As limitações fundamentais do BatchNorm: dependem da quantidade de dados. Batch_size=1 时平均值差无意义; batch_size<32 时统计量噪声太大──这就是Transformer 用 LayerNorm 的原因语言模型批小、序列长度不一──

### Normalização de camadas .

Normalização em todas as características em vez de em todo o lote.

> 跨特征维度归化, não跨批量── para uma única amostra:

```
mu = (1/D) * sum(x_j)           (feature mean)
sigma^2 = (1/D) * sum((x_j - mu)^2)   (feature variance)
x_hat = (x_j - mu) / sqrt(sigma^2 + eps)
y = gamma * x_hat + beta
```

D é a dimensão da característica. Cada amostra é normalizada de forma independente - sem dependência do tamanho do lote. É por isso que os transformadores usam LayerNorm em vez de BatchNorm. As sequências têm comprimentos variáveis, os tamanhos do lote são muitas vezes pequenos (ou 1 durante a geração), e o cálculo é idêntico entre treinamento e inferência.

> D é a dimensão da característica. Cada amostra é independente de sua dimensão. Não depende da massa. É por isso que o transformador usa a LayerNorm e não a BatchNorm.

O LayerNorm em transformadores é aplicado após cada bloco de autoatentação e cada bloco de alimentação (Post-LN), ou antes deles (Pre-LN, que é mais estável para o treinamento).

> LayerNorm do transformador  aplicado a cada bloco de atenção e cada bloco anterior  Depois  Post-LN), ou antes  Pre-LN, treinamento mais estável) 

### RMSNorm .

LayerNorm sem a subtração média. Proposto por Zhang & Sennrich (2019).

> LayerNorm 去掉均值减法── por Zhang & Sennrich (2019) 提出──

```
rms = sqrt((1/D) * sum(x_j^2))
y = gamma * x / rms
```

Não há medias de cálculo, não há parâmetros beta. A observação: a recentração (subtração média) no LayerNorm contribui muito pouco para o desempenho do modelo, mas custa computação.

> É assim. Não há valor médio calculado, não há beta parâmetros. Observe:LayerNorm's residency in LayerNorm (Reduction in average value) contribui muito pouco para o desempenho do modelo, mas o consumo calculado.

LLaMA, LLaMA 2, LLaMA 3, Mistral e a maioria dos LLM modernos usam RMSNorm em vez de LayerNorm. Na escala de bilhões de parâmetros e trilhões de tokens, essa economia de 10% é significativa.

> LLaMA、LLaMA 2、LLaMA 3、Mistral 和大多数现代 LLM使用RMSNorm而不是LayerNorm── em escala de bilhões de parâmetros e de vários bilhões de tokens, a economia de 10% é significativa──

> **【拓展：RMSNorm 为什么能省 10%】**LayerNorm  calcular o valor médio e o diferencial de duas etapas, RMSNorm  saltar o valor médio apenas para RMS。 em Llama 3 405B(126 层) em cima, cada passo de treinamento é de 252 RMSNorm ️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️

### Normalismo Comparação                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         

### Normalismo Comparação                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         

```mermaid
graph TD
    subgraph "Batch Normalization"
        BN_D["Normalize across BATCH<br/>for each feature"]
        BN_S["Batch: [x1, x2, x3, x4]<br/>Feature 1: normalize [x1f1, x2f1, x3f1, x4f1]"]
        BN_P["Needs batch > 32<br/>Different train vs eval<br/>Used in CNNs"]
    end
    subgraph "Layer Normalization"
        LN_D["Normalize across FEATURES<br/>for each sample"]
        LN_S["Sample x1: normalize [f1, f2, f3, f4]"]
        LN_P["Batch-independent<br/>Same train vs eval<br/>Used in Transformers"]
    end
    subgraph "RMS Normalization"
        RN_D["Like LayerNorm<br/>but skip mean subtraction"]
        RN_S["Just divide by RMS<br/>No centering"]
        RN_P["10% faster than LayerNorm<br/>Same accuracy<br/>Used in LLaMA, Mistral"]
    end
```

### Aumentar dados como regularização

Não é uma modificação de modelo, mas uma modificação de dados.

> Não é modificação do modelo, mas modificação do dados.

- Imagens: colheita aleatória, virada, rotação, nervosismo de cor, corte
  Tradução do inglês: image:随机剪转转转转转转转色 动 遮
- Texto: substituição de sinônimos, tradução de volta, exclusão aleatória
  中文翻译:文本:同义词替换、回译、随机删除
- Áudio: tempo de estiramento, mudança de tom, adição de ruído
  Chinese: 音频: 時間拉伸、音调偏移、添加噪音

O efeito é idêntico à regularização: aumenta o tamanho efetivo do conjunto de treinamento, tornando mais difícil para o modelo memorizar exemplos específicos. Um modelo que só vê cada imagem uma vez em sua forma original pode memorizá-la. Um modelo que vê 50 versões aumentadas de cada imagem é forçado a aprender a estrutura invariante.

> O efeito é o mesmo que a normalização: ele aumenta a tamanho válido do conjunto de treinamento, tornando o modelo mais difícil de lembrar de um padrão específico.

### Parar cedo. Parar cedo.

O regulador mais simples: parar de treinar quando a perda de validação começa a aumentar. O modelo ainda não está sobresponsado naquele ponto. Na prática, você acompanha a perda de validação em cada época, salva o melhor modelo e continua treinando para uma janela de "paciência" (normalmente 5-20 épocas). Se a perda de validação não melhora dentro da janela de paciência, você para e carrega o melhor modelo salvo.

> O método mais simples de regularização é: quando a perda de testes começa a aumentar, pare de treinar. Neste momento o modelo ainda não está preparado. Na prática, você em cada época acompanha a perda de testes, conserva o melhor modelo, e continua a treinar uma janela de "paciência" (normalmente 5-20 épocas) ⋅ Se a perda de testes na janela de testes não melhora, pare de carregar o melhor modelo de conservação.

> **【拓展：Early Stopping 在大模型中的实践】**GPT 和 Llama 等大模型通常不使用早期停止训练在固定代币 数后结束──但在微调阶段 (como LoRA fine-tuning),早期停止 非常重要,因为小数据集上容易过拟合──HuggingFace 的教练默认使用早期停止(耐心=3),监控 eval_loss──

### Quando aplicar o que ?

```mermaid
flowchart TD
    Gap{"Train-test<br/>accuracy gap?"} -->|"> 10%"| Heavy["Heavy regularization"]
    Gap -->|"5-10%"| Medium["Moderate regularization"]
    Gap -->|"< 5%"| Light["Light regularization"]

    Heavy --> D5["Dropout p=0.3-0.5"]
    Heavy --> WD2["Weight decay 0.01-0.1"]
    Heavy --> Aug["Aggressive data augmentation"]
    Heavy --> ES["Early stopping"]

    Medium --> D3["Dropout p=0.1-0.2"]
    Medium --> WD1["Weight decay 0.001-0.01"]
    Medium --> Norm["BatchNorm or LayerNorm"]

    Light --> D1["Dropout p=0.05-0.1"]
    Light --> WD0["Weight decay 1e-4"]
```

## Construí-lo e realizei-o.
```figure
l2-regularization
```

## Construí-lo

> **【中文解读】**A seguinte é a seguinte: a partir de zero implementar cinco tipos de regulamentação técnica.

### Passo 1: Desistência (Modo de treinamento e Eval)

> Primeiro passo:Dropout 实现──关键是逆转 training时按概率 p 置零,剩余值除以 (1-p) 保持期望不变;推理时直接通过──这样推理代码不需要知道的存在──倒退也需要应用相同的面具(除以 (1-p))──

```python
import random
import math


class Dropout:
    def __init__(self, p=0.5):
        self.p = p
        self.training = True
        self.mask = None

    def forward(self, x):
        if not self.training:
            return list(x)
        self.mask = []
        output = []
        for val in x:
            if random.random() < self.p:
                self.mask.append(0)
                output.append(0.0)
            else:
                self.mask.append(1)
                output.append(val / (1 - self.p))
        return output

    def backward(self, grad_output):
        grads = []
        for g, m in zip(grad_output, self.mask):
            if m == 0:
                grads.append(0.0)
            else:
                grads.append(g / (1 - self.p))
        return grads
```

### Passo 2: L2 Decaimento de peso.

> Segundo passo: L2 L2 L2 L2 L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L L

```python
def l2_regularization(weights, lambda_reg):
    penalty = 0.0
    for w in weights:
        penalty += w * w
    return lambda_reg * 0.5 * penalty

def l2_gradient(weights, lambda_reg):
    return [lambda_reg * w for w in weights]
```

### Passo 3: Normalização de lote.

> O primeiro passo é a implementação de um padrão de bateria de dados de um grupo de dados.

```python
class BatchNorm:
    def __init__(self, num_features, momentum=0.1, eps=1e-5):
        self.gamma = [1.0] * num_features
        self.beta = [0.0] * num_features
        self.eps = eps
        self.momentum = momentum
        self.running_mean = [0.0] * num_features
        self.running_var = [1.0] * num_features
        self.training = True
        self.num_features = num_features

    def forward(self, batch):
        batch_size = len(batch)
        if self.training:
            mean = [0.0] * self.num_features
            for sample in batch:
                for j in range(self.num_features):
                    mean[j] += sample[j]
            mean = [m / batch_size for m in mean]

            var = [0.0] * self.num_features
            for sample in batch:
                for j in range(self.num_features):
                    var[j] += (sample[j] - mean[j]) ** 2
            var = [v / batch_size for v in var]

            for j in range(self.num_features):
                self.running_mean[j] = (1 - self.momentum) * self.running_mean[j] + self.momentum * mean[j]
                self.running_var[j] = (1 - self.momentum) * self.running_var[j] + self.momentum * var[j]
        else:
            mean = list(self.running_mean)
            var = list(self.running_var)

        self.x_hat = []
        output = []
        for sample in batch:
            normalized = []
            out_sample = []
            for j in range(self.num_features):
                x_h = (sample[j] - mean[j]) / math.sqrt(var[j] + self.eps)
                normalized.append(x_h)
                out_sample.append(self.gamma[j] * x_h + self.beta[j])
            self.x_hat.append(normalized)
            output.append(out_sample)
        return output
```

### Passo 4: Normalização de camadas.

```python
class LayerNorm:
    def __init__(self, num_features, eps=1e-5):
        self.gamma = [1.0] * num_features
        self.beta = [0.0] * num_features
        self.eps = eps
        self.num_features = num_features

    def forward(self, x):
        mean = sum(x) / len(x)
        var = sum((xi - mean) ** 2 for xi in x) / len(x)

        self.x_hat = []
        output = []
        for j in range(self.num_features):
            x_h = (x[j] - mean) / math.sqrt(var + self.eps)
            self.x_hat.append(x_h)
            output.append(self.gamma[j] * x_h + self.beta[j])
        return output
```

### Passo 5: RMSNorm. Passo 5: Reunificação de raízes.

> 第五步:RMSNorm é a versão simplificada de LayerNorm  apenas calcula RMS(quadratic roots), não reduzir o valor médio, não há beta;;LLaMA、Mistral etc. LLM moderno todos usam RMSNorm ∼10% de aceleração parece não ser muito, mas em mil milhões de tokens ∞ treinamento equivale a economizar milhares de GPU 小时──

```python
class RMSNorm:
    def __init__(self, num_features, eps=1e-6):
        self.gamma = [1.0] * num_features
        self.eps = eps
        self.num_features = num_features

    def forward(self, x):
        rms = math.sqrt(sum(xi * xi for xi in x) / len(x) + self.eps)
        output = []
        for j in range(self.num_features):
            output.append(self.gamma[j] * x[j] / rms)
        return output
```

### Passo 6: Treinamento com e sem regularização.

> Segundo, a redução da taxa de aceleração de um grupo de dados em forma circular pode ser de aproximadamente 50% (ou mais), mas a redução da taxa de aceleração de um grupo de dados pode ser de aproximadamente 65% (ou menos).

```python
def sigmoid(x):
    x = max(-500, min(500, x))
    return 1.0 / (1.0 + math.exp(-x))


def make_circle_data(n=200, seed=42):
    random.seed(seed)
    data = []
    for _ in range(n):
        x = random.uniform(-2, 2)
        y = random.uniform(-2, 2)
        label = 1.0 if x * x + y * y < 1.5 else 0.0
        data.append(([x, y], label))
    return data


class RegularizedNetwork:
    def __init__(self, hidden_size=16, lr=0.05, dropout_p=0.0, weight_decay=0.0):
        random.seed(0)
        self.hidden_size = hidden_size
        self.lr = lr
        self.dropout_p = dropout_p
        self.weight_decay = weight_decay
        self.dropout = Dropout(p=dropout_p) if dropout_p > 0 else None

        self.w1 = [[random.gauss(0, 0.5) for _ in range(2)] for _ in range(hidden_size)]
        self.b1 = [0.0] * hidden_size
        self.w2 = [random.gauss(0, 0.5) for _ in range(hidden_size)]
        self.b2 = 0.0

    def forward(self, x, training=True):
        self.x = x
        self.z1 = []
        self.h = []
        for i in range(self.hidden_size):
            z = self.w1[i][0] * x[0] + self.w1[i][1] * x[1] + self.b1[i]
            self.z1.append(z)
            self.h.append(max(0.0, z))

        if self.dropout and training:
            self.dropout.training = True
            self.h = self.dropout.forward(self.h)
        elif self.dropout:
            self.dropout.training = False
            self.h = self.dropout.forward(self.h)

        self.z2 = sum(self.w2[i] * self.h[i] for i in range(self.hidden_size)) + self.b2
        self.out = sigmoid(self.z2)
        return self.out

    def backward(self, target):
        eps = 1e-15
        p = max(eps, min(1 - eps, self.out))
        d_loss = -(target / p) + (1 - target) / (1 - p)
        d_sigmoid = self.out * (1 - self.out)
        d_out = d_loss * d_sigmoid

        for i in range(self.hidden_size):
            d_relu = 1.0 if self.z1[i] > 0 else 0.0
            d_h = d_out * self.w2[i] * d_relu
            self.w2[i] -= self.lr * (d_out * self.h[i] + self.weight_decay * self.w2[i])
            for j in range(2):
                self.w1[i][j] -= self.lr * (d_h * self.x[j] + self.weight_decay * self.w1[i][j])
            self.b1[i] -= self.lr * d_h
        self.b2 -= self.lr * d_out

    def evaluate(self, data):
        correct = 0
        total_loss = 0.0
        for x, y in data:
            pred = self.forward(x, training=False)
            eps = 1e-15
            p = max(eps, min(1 - eps, pred))
            total_loss += -(y * math.log(p) + (1 - y) * math.log(1 - p))
            if (pred >= 0.5) == (y >= 0.5):
                correct += 1
        return total_loss / len(data), correct / len(data) * 100

    def train_model(self, train_data, test_data, epochs=300):
        history = []
        for epoch in range(epochs):
            total_loss = 0.0
            correct = 0
            for x, y in train_data:
                pred = self.forward(x, training=True)
                self.backward(y)
                eps = 1e-15
                p = max(eps, min(1 - eps, pred))
                total_loss += -(y * math.log(p) + (1 - y) * math.log(1 - p))
                if (pred >= 0.5) == (y >= 0.5):
                    correct += 1
            train_loss = total_loss / len(train_data)
            train_acc = correct / len(train_data) * 100
            test_loss, test_acc = self.evaluate(test_data)
            history.append((train_loss, train_acc, test_loss, test_acc))
            if epoch % 75 == 0 or epoch == epochs - 1:
                gap = train_acc - test_acc
                print(f"    Epoch {epoch:3d}: train_acc={train_acc:.1f}%, test_acc={test_acc:.1f}%, gap={gap:.1f}%")
        return history
```

## Use-o com o framework implementado.

> **【中文解读】**PyTorch 中使用正则化关键:model.train()/model.eval() 切换 Dropout 和 BatchNorm 的行为──在Transformer 中,LayerNorm + Dropout p=0.1 是标配──忘记模型.eval() 是最常见的深度学习 bug 之一──

PyTorch fornece toda a normalização e regularização como módulos:

> PyTorch vai fornecer todas as funções de regularização e regularização como módulo:

```python
import torch
import torch.nn as nn

model = nn.Sequential(
    nn.Linear(784, 256),
    nn.BatchNorm1d(256),
    nn.ReLU(),
    nn.Dropout(0.3),
    nn.Linear(256, 128),
    nn.BatchNorm1d(128),
    nn.ReLU(),
    nn.Dropout(0.3),
    nn.Linear(128, 10),
)

model.train()
out_train = model(torch.randn(32, 784))

model.eval()
out_test = model(torch.randn(1, 784))
```

O `model.train()`- Não .`model.eval()`O toggle é crítico. Ele desliga/desliga o desligamento e diz ao BatchNorm para usar estatísticas de lote versus estatísticas de execução.`model.eval()`A precisão do teste fluctará aleatoriamente porque o abandono ainda está ativo e o BatchNorm está usando estatísticas mini-batch.

> `model.train()`- Não .`model.eval()`切换至关重要──它开关 dropout 并告诉BatchNorm  使用批量统计量还是运行统计量──推理前忘记 `model.eval()`É um dos bugs mais comuns no aprendizado em profundidade. A taxa de verificação de seus testes vai variar, porque o abandono ainda está ativo.

Para transformadores, o padrão é diferente:

> 对于Transformer,模式不同:

```python
class TransformerBlock(nn.Module):
    def __init__(self, d_model=512, nhead=8, dropout=0.1):
        super().__init__()
        self.attention = nn.MultiheadAttention(d_model, nhead, dropout=dropout)
        self.norm1 = nn.LayerNorm(d_model)
        self.ff = nn.Sequential(
            nn.Linear(d_model, d_model * 4),
            nn.GELU(),
            nn.Linear(d_model * 4, d_model),
            nn.Dropout(dropout),
        )
        self.norm2 = nn.LayerNorm(d_model)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        attended, _ = self.attention(x, x, x)
        x = self.norm1(x + self.dropout(attended))
        x = self.norm2(x + self.ff(x))
        return x
```

LayerNorm, não BatchNorm. Desistência p=0.1, não p=0.5.

> Use LayerNorm, não BatchNorm.

## Envia-o . Produto .

Esta lição produz:
- `outputs/prompt-regularization-advisor.md`-- um aviso que diagnostica o excesso de conexão e recomenda a estratégia de regularização certa

> 本课产出:`outputs/prompt-regularization-advisor.md`- um diagnóstico de transmissão e recomendação de estratégias de correção

## Exercícios.

1. Implementar o abandono espacial para dados 2D: em vez de deixar cair neurônios individuais, deixe cair canais inteiros de recursos. Simula isso tratando grupos de recursos consecutivos como canais e deixando cair grupos inteiros. Compare a lacuna de teste de trem com o abandono padrão no conjunto de dados do círculo com hidden_size=32.

2. Implementar o suavizamento de rótulos da lição 05 combinado com o abandono desta lição. Treinar com quatro configurações: nenhuma, apenas abandono, apenas suavizamento de rótulos, ambos. Meter a lacuna de precisão final do teste de trem para cada uma. Qual combinação dá a menor lacuna?

3. Adicione uma camada BatchNorm entre a camada oculta e a ativação na sua rede de conjunto de dados circular. Treine com e sem BatchNorm a taxas de aprendizagem 0,01, 0,05, e 0.1.

4. Implementar paragem precoce: acompanhar a perda de teste em cada época, economizar os melhores pesos e parar se a perda de teste não tiver melhorado por 20 épocas. Execute a rede regularizada por 1000 épocas. Relate qual época teve a melhor precisão de teste e quantas épocas de computação você economizou.

5. Compare LayerNorm vs RMSNorm em uma rede de 4 camadas (não apenas 2). Iniciar ambos com os mesmos pesos. Treinar por 200 épocas e comparar precisão final, velocidade de treinamento (tempo por época) e magnitudes de gradiente na primeira camada. Verifique que RMSNorm é mais rápido com a mesma precisão.

## Termos-chave .

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Overfitting | "Model memorized the data" | When a model's training performance significantly exceeds its test performance, indicating it learned noise rather than signal |
| Regularization | "Preventing overfitting" | Any technique that constrains model complexity to improve generalization: dropout, weight decay, normalization, augmentation |
| Dropout | "Random neuron deletion" | Zeroing random neurons during training with probability p, forcing redundant representations; equivalent to training an ensemble |
| Weight decay | "L2 penalty" | Shrinking all weights toward zero by subtracting lambda * w at each step; penalizes complexity through weight magnitude |
| Batch normalization | "Normalize per batch" | Normalizing layer outputs across the batch dimension using batch statistics during training and running averages during inference |
| Layer normalization | "Normalize per sample" | Normalizing across features within each sample; batch-independent, used in transformers where batch size varies |
| RMSNorm | "LayerNorm without the mean" | Root mean square normalization; drops the mean subtraction from LayerNorm for 10% speedup with equal accuracy |
| Early stopping | "Stop before overfit" | Halting training when validation loss stops improving; the simplest regularizer, often used alongside others |
| Data augmentation | "More data from less" | Transforming training inputs (flip, crop, noise) to increase effective dataset size and force invariance learning |
| Generalization gap | "Train-test split" | The difference between training and test performance; regularization aims to minimize this gap |

## Mais leitura 延伸阅读

- Srivastava et al., "Dropout: Uma maneira simples de evitar redes neurais de sobreajuste" (2014) -- o papel original de abandono com a interpretação do conjunto e extensas experiências
  Srivastava 等人,Dropout: um método simples para prevenir a transcorrência da rede neurológica(2014)Original drop-out 论文, contendo explicação e experiências em grande quantidade
- Ioffe & Szegedy, "Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift" (2015) -- apresentou BatchNorm e seu procedimento de treinamento, um dos trabalhos de aprendizagem profunda mais citados
  Ioffe & Szegedy, 批归归一化:通过减少内部协变量偏移加速深度网络训练(2015) 引入BatchNorm 及其训练过程,深度学习中最引用的论文之一
- Zhang & Sennrich, "Root Mean Square Layer Normalization" (2019) -- mostrou que o RMSNorm corresponde à precisão do LayerNorm com computação reduzida; adotado pela LLaMA e Mistral
  Zhang & Sennrich,                                                                                                                                                                                                                                                            
- Zhang et al., "Compreender Deep Learning Requere Re-Pensar Generalização" (2017) - o documento histórico que mostra que as redes neurais podem memorizar rótulos aleatórios, desafiando as visões tradicionais da generalização
  Zhang 等人, compreender profundidade de aprendizagem precisa repensar a generalização(2017)里程碑论文,证明神经网络可以记忆随机标签,挑战传统泛化观点
