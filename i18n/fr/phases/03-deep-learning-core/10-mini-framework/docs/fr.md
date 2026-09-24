# Construisez votre propre mini-cadre

> Vous avez construit des neurones, des couches, des réseaux, des backprops, des activations, des fonctions de perte, des optimisateurs, des régularisations, des initialités et des calendriers LR. Tout comme des pièces distinctes.

> **【中文解读】**Pour comprendre le cadre complet de tous les cours, il faut comprendre le concept de l'ensemble des cours: moteur automatique, type d'optimisation, système de régulation, cycle de formation.

**Type:** Build
**Languages:** Python
**Prerequisites:** All of Phase 03 (Lessons 01-09)
**Time:** ~120 minutes

## Objectifs d'apprentissage

- Construire un cadre complet d'apprentissage profond (~ 500 lignes) avec Module, Linear, ReLU, Sigmoid, Dropout, BatchNorm, Sequential, fonctions de perte, optimisateurs et DataLoader
- Expliquer l'abstraction du module (avant, arrière, paramètres) et pourquoi le changement de mode train/éval est nécessaire
- Le câblage de tous les composants dans une boucle de formation de travail qui entraîne un réseau de 4 couches sur la classification de cercle
- Mapez chaque composant de votre framework à son équivalent PyTorch (nn.Module, nn.Sequential, optim.Adam, DataLoader)

> **【中文解读】**Le chapitre 3 de la phase 3 est un chapitre intégré. Après avoir terminé, vous comprendrez vraiment ce qui se passe derrière PyTorch.

## Le problème , l' introduction du problème

Vous avez dix leçons de blocs de construction dispersés sur des fichiers séparés.`Value`Une classe ici, une boucle d'entraînement là, une initialisation du poids dans un autre fichier, des horaires de taux d'apprentissage dans un autre.

> Vous avez 10 modèles de construction dispersés dans différents fichiers.`Value`类, il y a un cycle de formation, un autre document est l'initialisation du poids, un autre est la régulation du taux d'apprentissage. Pour former un réseau, vous devez copier des cinq ou six cours différents.

C'est ce que résolvent les frameworks.`nn.Module`- Je suis là .`nn.Sequential`- Je suis là .`optim.Adam`- Je suis là .`DataLoader`, et un schéma de boucle d'entraînement qui les lie ensemble.`keras.Layer`- Je suis là .`keras.Sequential`- Je suis là .`keras.optimizers.Adam`Ce ne sont pas des choses magiques, mais des modèles organisationnels qui permettent de définir, d'entraîner et d'évaluer les réseaux sans réinventer les plomberie à chaque fois.

> C'est le problème que le PyTorch vous a résolu.`nn.Module`- Je suis là.`nn.Sequential`- Je suis là.`optim.Adam`- Je suis là.`DataLoader`Et les lier ensemble dans un cycle d'entraînement.`keras.Layer`- Je suis là.`keras.Sequential`- Je suis là.`keras.optimizers.Adam` Ce ne sont pas des mages Elles sont des modèles d'organisation, vous permettant de définir, d'entraîner et d'évaluer le réseau sans avoir à réinventer chaque fois les tuyaux

Vous allez construire la même chose dans environ 500 lignes de Python. Pas de numpy. Pas de dépendances externes. Un cadre qui peut définir n'importe quel réseau de flux, l'entraîner avec SGD ou Adam, batch les données, appliquer la normalisation de dérapagement et de batch, utiliser n'importe quelle activation, et planifier le taux d'apprentissage.

> Vous utiliserez environ 500 pages Python pour construire la même chose. Pas besoin de numpy. Pas besoin de dépendance externe. Vous pouvez définir n'importe quel réseau.

Quand vous aurez terminé, vous comprendrez exactement ce qui se passe quand vous écrivez.`model = nn.Sequential(...)`Vous comprendrez pourquoi.`model.train()`et `model.eval()`Vous comprendrez pourquoi.`optimizer.zero_grad()`Vous allez tout comprendre, parce que vous l'avez construit.

> Après, tu comprendras parfaitement ce que je vais écrire en PyTorch.`model = nn.Sequential(...)`Tu sais pourquoi ?`model.train()`et `model.eval()`Tu comprendras pourquoi.`optimizer.zero_grad()`C'est un seul usage. Tu comprendras tout ça, parce que tu l'as construit toi-même.

> **【中文解读】**框架的核心价值:把散落的组件统一到一个接口下――Module est la base de toutLinear、ReLU、Dropout、BatchNorm 都是Module──Sequentielle est le mode de assemblage一堆Module 串起还是一个模块──

> **【拓展：PyTorch 框架的设计哲学】**Le design central de PyTorch ne comporte que 5 concepts: Tensor (Data) 、nn.Module (Model) 、autograd (Automatic) 、Optimizer (Optimizer) 、Optimiser (Optimiser) 、DataLoader (DataLoader) 、DataLoader (DataLoader) ‒ mais c'est ce que ces 5 concepts permettent de former le GPT-4 ‒ Stable Diffusion ‒ AlphaFold et autres modèles.

## Le concept de base.

### Le module d'abstraction le module d' abstraction

Chaque couche de PyTorch hérite de `nn.Module`Un module a trois responsabilités:

> PyTorch en Chine est une entreprise de production de chacune des deux catégories.`nn.Module`◊ Un module a trois responsabilités:

1. **forward()**-- calculer la sortie des entrées données
   **forward()**-- 给定输入计算输出
2. **parameters()**- retourner tous les poids entraînés
   **parameters()**--                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
3. **backward()**-- gradients de calcul (traités par autograd en PyTorch, explicite dans la nôtre)
   **backward()**-- 计算梯度(PyTorch 中由自动化 处理, notre cadre dans lequel il est nécessaire de réaliser clairement)

Une couche linéaire est un module. Une activation ReLU est un module. Une couche de dérapagement est un module. Une couche de normalisation de lot est un module. Ils ont tous la même interface.

> La couche linéaire est un module. La réLU 激活 est un module. La couche déroulante est un module. La couche normale est un module. Elles ont les mêmes interfaces.

### Un conteneur séquentiel

`nn.Sequential`Les modules de chaîne. Passage vers l'avant: données de flux à travers le module 1, puis le module 2, puis le module 3. Passage vers l'arrière: inverser la chaîne. Le conteneur lui-même est un module - il a des paramètres devant(), et vers l'arrière().

> `nn.Sequential`Pour le module, il est nécessaire de créer un module qui est en phase avec le module.

> **【拓展：真实框架的额外功能】**Votre framework miniature couvre le concept central de PyTorch, mais le vrai framework est aussi: 1) Autograd Automatic Mic分(pas besoin de réécrire à la main); 2) GPU  Support(CUDA 内存管理和内核调度); 3) 分布式训练(DDP、FSDP、DeepSpeed); 4) 混合精度训练(AMP); 4) 模型序列化(state_dict + save/load) ・PyTorch's code library exceeds 100 000 lines, mais le cœur abstrait est encore à votre disposition pour réaliser ces 5 个.

### Mode d'entraînement et d'évaluation

La normalisation des lots utilise des statistiques de lots pendant l'entraînement mais des moyennes de course pendant l'évaluation.`train()`et `eval()`Les méthodes de commutation de ce comportement.`training`Le drapeau.

> Le décalage de l'entraînement est un processus de mise à zéro, mais l'évaluation est entièrement réalisée.`train()`et `eval()`Chaque module a un seul.`training`Le signe.

### Optimisateur

L'optimisateur met à jour les paramètres en utilisant leurs gradients.`param -= lr * grad`Adam: maintient des estimations de dynamique et de variance, puis les mises à jour. L'optimisateur ne connaît pas l'architecture du réseau - il ne voit qu'une liste plane de paramètres et leurs gradients.

> 优化器用梯度更新参数──SGD:`param -= lr * grad`Adam: maintenance动量和方差估算后再更新──优化器不知道网络架构它只看一个平面的参数列表和它们的梯度──

### Le chargeur de données

Le batch est important pour deux raisons: d'abord, vous ne pouvez pas installer l'ensemble des données dans la mémoire pour de grands problèmes. Deuxièmement, la baisse du gradient mini-batch fournit un bruit qui aide à échapper aux minima locaux. Le DataLoader divise les données en lots et mélange optionnellement entre les époques.

> Les données de la série sont en grande partie décomposées dans le volume de données.

> **【拓展：DataLoader 在大模型训练中的演进】**Le DataLoader de PyTorch est un seul appareil. Le Big Model Training nécessite un DataLoader distribué. (1) Le WebDataset est utilisé pour un flux de données de niveau TB.

### La structure du cadre

```mermaid
graph TD
    subgraph "Modules"
        Linear["Linear<br/>W*x + b"]
        ReLU["ReLU<br/>max(0, x)"]
        Sigmoid["Sigmoid<br/>1/(1+e^-x)"]
        Dropout["Dropout<br/>random zero mask"]
        BatchNorm["BatchNorm<br/>normalize activations"]
    end

    subgraph "Containers"
        Sequential["Sequential<br/>chains modules"]
    end

    subgraph "Loss Functions"
        MSE["MSELoss<br/>(pred - target)^2"]
        BCE["BCELoss<br/>binary cross-entropy"]
    end

    subgraph "Optimizers"
        SGD["SGD<br/>param -= lr * grad"]
        Adam["Adam<br/>adaptive moments"]
    end

    subgraph "Data"
        DataLoader["DataLoader<br/>batching + shuffle"]
    end

    Sequential --> |"contains"| Linear
    Sequential --> |"contains"| ReLU
    Sequential --> |"forward/backward"| MSE
    SGD --> |"updates"| Sequential
    DataLoader --> |"feeds"| Sequential
```

### La boucle d'entraînement

```mermaid
sequenceDiagram
    participant DL as DataLoader
    participant M as Model
    participant L as Loss
    participant O as Optimizer

    loop Each Epoch
        DL->>M: batch of inputs
        M->>M: forward pass (layer by layer)
        M->>L: predictions
        L->>L: compute loss
        L->>M: backward pass (gradients)
        M->>O: parameters + gradients
        O->>M: updated parameters
        O->>O: zero gradients
    end
```

### Je suis un homme qui a des problèmes avec les modules.

```mermaid
classDiagram
    class Module {
        +forward(x)
        +backward(grad)
        +parameters()
        +train()
        +eval()
    }

    class Linear {
        -weights
        -biases
        +forward(x)
        +backward(grad)
    }

    class ReLU {
        +forward(x)
        +backward(grad)
    }

    class Sequential {
        -modules[]
        +forward(x)
        +backward(grad)
        +parameters()
    }

    Module <|-- Linear
    Module <|-- ReLU
    Module <|-- Sequential
    Sequential *-- Module
```

## Construisez-le et mettez-le en œuvre.

> **【中文解读】**Vous trouverez ci-dessous chaque composant de la structure de construction:Module 基类 → Ligne → 激活函数 → Dropout → BatchNorm → Sequentielle 容器 → 损失函数 → 优化器 → DataLoader → 完整训练循环──
```figure
gradient-clipping
```

## Faites-le

### Étape 1: Module de base de classe

L'interface abstraite que chaque couche implemente.

> Chaque couche de réalisation est une interface abstraite.

```python
class Module:
    def __init__(self):
        self.training = True

    def forward(self, x):
        raise NotImplementedError

    def backward(self, grad):
        raise NotImplementedError

    def parameters(self):
        return []

    def train(self):
        self.training = True

    def eval(self):
        self.training = False
```

### Étape 2: Couche linéaire

Le bloc de construction fondamental. stocke les poids et les biais, calcule Wx + b vers l'avant et les gradients de poids / entrée vers l'arrière.

> 基本构建块── stockage权重和偏置,前向计算 Wx + b,反向计算权重/输入梯度──

> L' épaisseur est PyTorch`nn.Linear`Pour chaque neurone de sortie, calculer`sum(W[i][j] * x[j]) + b[i]`◊ Le taux de gravité de l'équipement est`grad[i] * input[j]`, le degré d'entrée est `grad[i] * W[i][j]`◊ attention à la fan_in 维度初始化用 Kaiming(`std = sqrt(2/fan_in)`), adapté à la réaction.

```python
import math
import random


class Linear(Module):
    def __init__(self, fan_in, fan_out):
        super().__init__()
        std = math.sqrt(2.0 / fan_in)
        self.weights = [[random.gauss(0, std) for _ in range(fan_in)] for _ in range(fan_out)]
        self.biases = [0.0] * fan_out
        self.weight_grads = [[0.0] * fan_in for _ in range(fan_out)]
        self.bias_grads = [0.0] * fan_out
        self.fan_in = fan_in
        self.fan_out = fan_out
        self.input = None

    def forward(self, x):
        self.input = x
        output = []
        for i in range(self.fan_out):
            val = self.biases[i]
            for j in range(self.fan_in):
                val += self.weights[i][j] * x[j]
            output.append(val)
        return output

    def backward(self, grad):
        input_grad = [0.0] * self.fan_in
        for i in range(self.fan_out):
            self.bias_grads[i] += grad[i]
            for j in range(self.fan_in):
                self.weight_grads[i][j] += grad[i] * self.input[j]
                input_grad[j] += grad[i] * self.weights[i][j]
        return input_grad

    def parameters(self):
        params = []
        for i in range(self.fan_out):
            for j in range(self.fan_in):
                params.append((self.weights, i, j, self.weight_grads))
            params.append((self.biases, i, None, self.bias_grads))
        return params
```

### Étape 3: Modules d'activation.

ReLU, Sigmoid et Tanh en tant que modules, chacun cache ce dont il a besoin pour le passage arrière.

> ReLU、Sigmoid 和 Tanh 作为模块──每个缓存反向传播所需的信息──

```python
class ReLU(Module):
    def __init__(self):
        super().__init__()
        self.mask = None

    def forward(self, x):
        self.mask = [1.0 if v > 0 else 0.0 for v in x]
        return [max(0.0, v) for v in x]

    def backward(self, grad):
        return [g * m for g, m in zip(grad, self.mask)]


class Sigmoid(Module):
    def __init__(self):
        super().__init__()
        self.output = None

    def forward(self, x):
        self.output = []
        for v in x:
            v = max(-500, min(500, v))
            self.output.append(1.0 / (1.0 + math.exp(-v)))
        return self.output

    def backward(self, grad):
        return [g * o * (1 - o) for g, o in zip(grad, self.output)]


class Tanh(Module):
    def __init__(self):
        super().__init__()
        self.output = None

    def forward(self, x):
        self.output = [math.tanh(v) for v in x]
        return self.output

    def backward(self, grad):
        return [g * (1 - o * o) for g, o in zip(grad, self.output)]
```

### Étape 4: Module de déconnexion

Il est possible de faire des étalons de 1 à 1 p. Les valeurs attendues restent les mêmes.

> 訓練時随机将元素置零──按 1/(1-p) 缩放剩余元素,使期望值不变──评估时不做任何操作──

```python
class Dropout(Module):
    def __init__(self, p=0.5):
        super().__init__()
        self.p = p
        self.mask = None

    def forward(self, x):
        if not self.training:
            return x
        self.mask = [0.0 if random.random() < self.p else 1.0 / (1 - self.p) for _ in x]
        return [v * m for v, m in zip(x, self.mask)]

    def backward(self, grad):
        if self.mask is None:
            return grad
        return [g * m for g, m in zip(grad, self.mask)]
```

### Étape 5: Module de sérieNorm

Normalise les activations à zéro moyenne et variance unitaire par fonctionnalité sur le lot. Maintient des statistiques en cours d'exécution pour le mode d'évaluation.

> La valeur active sera regroupée en valeurs zéro moyennes et en unités de différence entre les lots.

```python
class BatchNorm(Module):
    def __init__(self, size, momentum=0.1, eps=1e-5):
        super().__init__()
        self.size = size
        self.gamma = [1.0] * size
        self.beta = [0.0] * size
        self.gamma_grads = [0.0] * size
        self.beta_grads = [0.0] * size
        self.running_mean = [0.0] * size
        self.running_var = [1.0] * size
        self.momentum = momentum
        self.eps = eps
        self.x_norm = None
        self.std_inv = None
        self.batch_input = None

    def forward_batch(self, batch):
        batch_size = len(batch)
        output_batch = []

        if self.training:
            mean = [0.0] * self.size
            for sample in batch:
                for j in range(self.size):
                    mean[j] += sample[j]
            mean = [m / batch_size for m in mean]

            var = [0.0] * self.size
            for sample in batch:
                for j in range(self.size):
                    var[j] += (sample[j] - mean[j]) ** 2
            var = [v / batch_size for v in var]

            self.std_inv = [1.0 / math.sqrt(v + self.eps) for v in var]

            self.x_norm = []
            self.batch_input = batch
            for sample in batch:
                normed = [(sample[j] - mean[j]) * self.std_inv[j] for j in range(self.size)]
                self.x_norm.append(normed)
                output = [self.gamma[j] * normed[j] + self.beta[j] for j in range(self.size)]
                output_batch.append(output)

            for j in range(self.size):
                self.running_mean[j] = (1 - self.momentum) * self.running_mean[j] + self.momentum * mean[j]
                self.running_var[j] = (1 - self.momentum) * self.running_var[j] + self.momentum * var[j]
        else:
            std_inv = [1.0 / math.sqrt(v + self.eps) for v in self.running_var]
            for sample in batch:
                normed = [(sample[j] - self.running_mean[j]) * std_inv[j] for j in range(self.size)]
                output = [self.gamma[j] * normed[j] + self.beta[j] for j in range(self.size)]
                output_batch.append(output)

        return output_batch

    def forward(self, x):
        result = self.forward_batch([x])
        return result[0]

    def backward(self, grad):
        if self.x_norm is None:
            return grad
        for j in range(self.size):
            self.gamma_grads[j] += self.x_norm[0][j] * grad[j]
            self.beta_grads[j] += grad[j]
        return [grad[j] * self.gamma[j] * self.std_inv[j] for j in range(self.size)]

    def parameters(self):
        params = []
        for j in range(self.size):
            params.append((self.gamma, j, None, self.gamma_grads))
            params.append((self.beta, j, None, self.beta_grads))
        return params
```

### Étape 6: Contenant séquentiel

Les chaînes sont des modules, avant va de gauche à droite, arrière va de droite à gauche.

> 串联模块──前向从左到右,反向从右到左──

> Le contenant séquentiel pour réaliser le mode de composition est lui-même un module, mais il maintient un module en interne.`train()`et `eval()`递归调用每个子模块──`parameters()`C'est le PyTorch.`nn.Sequential`La réalisation centrale de la

```python
class Sequential(Module):
    def __init__(self, *modules):
        super().__init__()
        self.modules = list(modules)

    def forward(self, x):
        for module in self.modules:
            x = module.forward(x)
        return x

    def backward(self, grad):
        for module in reversed(self.modules):
            grad = module.backward(grad)
        return grad

    def parameters(self):
        params = []
        for module in self.modules:
            params.extend(module.parameters())
        return params

    def train(self):
        self.training = True
        for module in self.modules:
            module.train()

    def eval(self):
        self.training = False
        for module in self.modules:
            module.eval()
```

### Étape 7: Perte de fonction

MSE et entropies croisées binaires. Chacun renvoie la valeur de perte et fournit un arrière qui renvoie le gradient.

> MSE 和二元交叉──每回损失值,并提供回升梯度的逆转──) 方法──

> La fonction de perte est le point de départ du cycle de formation  contre direction de propagation du degré de perte de fonction de départ                                                                                                                                                                                                                                                `2 * (pred - target) / n`Le degré de l'établissement de l'Etat est de`(-target/p + (1-target)/(1-p)) / n`注意 BCE 中要使用eps 裁剪防止 log ((0) 

```python
class MSELoss:
    def __call__(self, predicted, target):
        self.predicted = predicted
        self.target = target
        n = len(predicted)
        self.loss = sum((p - t) ** 2 for p, t in zip(predicted, target)) / n
        return self.loss

    def backward(self):
        n = len(self.predicted)
        return [2 * (p - t) / n for p, t in zip(self.predicted, self.target)]


class BCELoss:
    def __call__(self, predicted, target):
        self.predicted = predicted
        self.target = target
        eps = 1e-7
        n = len(predicted)
        self.loss = 0
        for p, t in zip(predicted, target):
            p = max(eps, min(1 - eps, p))
            self.loss += -(t * math.log(p) + (1 - t) * math.log(1 - p))
        self.loss /= n
        return self.loss

    def backward(self):
        eps = 1e-7
        n = len(self.predicted)
        grads = []
        for p, t in zip(self.predicted, self.target):
            p = max(eps, min(1 - eps, p))
            grads.append((-t / p + (1 - t) / (1 - p)) / n)
        return grads
```

### Étape 8: SGD et Adam Optimisers

Les deux prennent une liste de paramètres et mettent à jour les poids en utilisant des gradients.

> 两者都接收参数列表,使用梯度更新权重──

> SGD 简单:参数 -= apprentissage × 梯度。Adam 维护一阶矩 m 和二阶矩 v,加上偏差修正(前几步梯度估计有偏差), effet sur la majorité des tâches est meilleur que SGD。AdamW 在Adam 基础加解权重衰减──参数列表中的每个元素是 (容器, i, j, 梯度容器) 四组,j=None元表示偏置(一维)。

```python
class SGD:
    def __init__(self, parameters, lr=0.01):
        self.params = parameters
        self.lr = lr

    def step(self):
        for container, i, j, grad_container in self.params:
            if j is not None:
                container[i][j] -= self.lr * grad_container[i][j]
            else:
                container[i] -= self.lr * grad_container[i]

    def zero_grad(self):
        for container, i, j, grad_container in self.params:
            if j is not None:
                grad_container[i][j] = 0.0
            else:
                grad_container[i] = 0.0


class Adam:
    def __init__(self, parameters, lr=0.001, beta1=0.9, beta2=0.999, eps=1e-8):
        self.params = parameters
        self.lr = lr
        self.beta1 = beta1
        self.beta2 = beta2
        self.eps = eps
        self.t = 0
        self.m = [0.0] * len(parameters)
        self.v = [0.0] * len(parameters)

    def step(self):
        self.t += 1
        for idx, (container, i, j, grad_container) in enumerate(self.params):
            if j is not None:
                g = grad_container[i][j]
            else:
                g = grad_container[i]

            self.m[idx] = self.beta1 * self.m[idx] + (1 - self.beta1) * g
            self.v[idx] = self.beta2 * self.v[idx] + (1 - self.beta2) * g * g

            m_hat = self.m[idx] / (1 - self.beta1 ** self.t)
            v_hat = self.v[idx] / (1 - self.beta2 ** self.t)

            update = self.lr * m_hat / (math.sqrt(v_hat) + self.eps)

            if j is not None:
                container[i][j] -= update
            else:
                container[i] -= update

    def zero_grad(self):
        for container, i, j, grad_container in self.params:
            if j is not None:
                grad_container[i][j] = 0.0
            else:
                grad_container[i] = 0.0
```

### Étape 9: DataLoader

Divise les données en lots, mélange optionnellement chaque époque.

> Les données seront divisées en lots, à choisir à chaque époque.

```python
class DataLoader:
    def __init__(self, data, batch_size=32, shuffle=True):
        self.data = data
        self.batch_size = batch_size
        self.shuffle = shuffle

    def __iter__(self):
        indices = list(range(len(self.data)))
        if self.shuffle:
            random.shuffle(indices)
        for start in range(0, len(indices), self.batch_size):
            batch_indices = indices[start:start + self.batch_size]
            batch = [self.data[i] for i in batch_indices]
            inputs = [item[0] for item in batch]
            targets = [item[1] for item in batch]
            yield inputs, targets

    def __len__(self):
        return (len(self.data) + self.batch_size - 1) // self.batch_size
```

### Étape 10: Formez un réseau à 4 couches sur la classification en cercle.

Définir un modèle, choisir une perte, choisir un optimisateur, faire le cycle d'entraînement.

> Pour le classement des résultats, il est nécessaire de définir le modèle, de choisir la fonction de perte, de choisir l'optimisateur, de faire fonctionner le cycle de formation.

> 训练循环的标准模式: chaque époque 遍历所有批次,每个批次 中:(1) zéro_grade 清零梯度;(2) forward 前向计算预测;(3) 计算损失;(4) backwards 反向传播梯度;(5) optimizer.step() 更新参数。圆形分类任务:点是 (x, y),标签是 x2+y2<1.5 → 1,否则 0。

```python
def make_circle_data(n=500, seed=42):
    random.seed(seed)
    data = []
    for _ in range(n):
        x = random.uniform(-2, 2)
        y = random.uniform(-2, 2)
        label = 1.0 if x * x + y * y < 1.5 else 0.0
        data.append(([x, y], [label]))
    return data


def train():
    random.seed(42)

    model = Sequential(
        Linear(2, 16),
        ReLU(),
        Linear(16, 16),
        ReLU(),
        Linear(16, 8),
        ReLU(),
        Linear(8, 1),
        Sigmoid(),
    )

    criterion = BCELoss()
    optimizer = Adam(model.parameters(), lr=0.01)

    data = make_circle_data(500)
    split = int(len(data) * 0.8)
    train_data = data[:split]
    test_data = data[split:]

    loader = DataLoader(train_data, batch_size=16, shuffle=True)

    model.train()

    for epoch in range(100):
        total_loss = 0
        total_correct = 0
        total_samples = 0

        for batch_inputs, batch_targets in loader:
            batch_loss = 0
            for x, t in zip(batch_inputs, batch_targets):
                pred = model.forward(x)
                loss = criterion(pred, t)
                batch_loss += loss

                optimizer.zero_grad()
                grad = criterion.backward()
                model.backward(grad)
                optimizer.step()

                predicted_class = 1.0 if pred[0] >= 0.5 else 0.0
                if predicted_class == t[0]:
                    total_correct += 1
                total_samples += 1

            total_loss += batch_loss

        avg_loss = total_loss / total_samples
        accuracy = total_correct / total_samples * 100

        if epoch % 10 == 0 or epoch == 99:
            print(f"Epoch {epoch:3d} | Loss: {avg_loss:.6f} | Train Accuracy: {accuracy:.1f}%")

    model.eval()
    correct = 0
    for x, t in test_data:
        pred = model.forward(x)
        predicted_class = 1.0 if pred[0] >= 0.5 else 0.0
        if predicted_class == t[0]:
            correct += 1
    test_accuracy = correct / len(test_data) * 100
    print(f"\nTest Accuracy: {test_accuracy:.1f}% ({correct}/{len(test_data)})")

    return model, test_accuracy
```

## Utilisez-le avec le cadre de réalisation

> **【中文解读】**La structure de PyTorch et votre petit cadre de computation est parfaitement cohérente: Sequentiel, Linier, RéLU, Sigmoïde, BCELoss, Adam, zéro degré, arrière, pas, train, évolution. La seule différence est que PyTorch utilise un degré automatique de calcul autogradé, mais vous devez écrire à la main en arrière.

Voici l'équivalent PyTorch de ce que vous venez de construire:

> Voici la mise en œuvre de PyTorch, le cadre que vous venez de construire:

> PyTorch de `nn.Sequential`- Je suis là.`nn.Linear`- Je suis là.`nn.ReLU`- Je suis là.`nn.Sigmoid`- Je suis là.`nn.BCELoss`- Je suis là.`torch.optim.Adam`La plus grande différence avec votre miniature cadre est PyTorch avec autograde automatique calcul gradient (vous n'avez pas besoin de réécrire à la main en arrière), et prend en charge GPU et et la précision mixte. Mais le modèle mental est tout à fait le même.

```python
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset

model = nn.Sequential(
    nn.Linear(2, 16),
    nn.ReLU(),
    nn.Linear(16, 16),
    nn.ReLU(),
    nn.Linear(16, 8),
    nn.ReLU(),
    nn.Linear(8, 1),
    nn.Sigmoid(),
)

criterion = nn.BCELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

for epoch in range(100):
    model.train()
    for inputs, targets in dataloader:
        optimizer.zero_grad()
        predictions = model(inputs)
        loss = criterion(predictions, targets)
        loss.backward()
        optimizer.step()

    model.eval()
    with torch.no_grad():
        test_predictions = model(test_inputs)
```

La structure est identique.`Sequential`- Je suis là .`Linear`- Je suis là .`ReLU`- Je suis là .`Sigmoid`- Je suis là .`BCELoss`- Je suis là .`Adam`- Je suis là .`zero_grad`- Je suis là .`backward`- Je suis là .`step`- Je suis là .`train`- Je suis là .`eval`Chaque concept est cartographié un à un. La différence est que PyTorch gère automatiquement l'autograd (pas besoin d'implémenter à l'envers) dans chaque module, fonctionne sur GPU et a été optimisé pendant des années.

> La structure est entièrement la même.`Sequential`- Je suis là.`Linear`- Je suis là.`ReLU`- Je suis là.`Sigmoid`- Je suis là.`BCELoss`- Je suis là.`Adam`- Je suis là.`zero_grad`- Je suis là.`backward`- Je suis là.`step`- Je suis là.`train`- Je suis là.`eval` Chaque concept est automatisé par PyTorch, mais il n'est pas nécessaire de le réaliser en arrière dans chaque module.

Maintenant, quand vous voyez le code PyTorch, vous savez exactement ce qui se passe à chaque ligne.

> Maintenant, quand vous voyez le code PyTorch, vous savez vraiment ce qui s'est passé dans chaque ligne.

## Envoyez-le . Produit .

Cette leçon donne:
- `outputs/prompt-framework-architect.md`-- une commande pour concevoir des architectures de réseaux neuronaux à l'aide d'abstractions de cadres

> Le programme de formation`outputs/prompt-framework-architect.md`- un usage de cadre abstrait conception de conception de réseaux de conception

> Cette suggestion va guider le LLM en fonction des caractéristiques de tâches (input dimension, output type, quantité de données) recommandant une structure réseau adaptée à chaque niveau, avec quel type de neurones, avec quel type d'activation, avec quel type de défaillance et d'optimisation.

## Les exercices

1. Ajouter un `SoftmaxCrossEntropyLoss`Softmax les prédictions, calculer la perte d'entropie croisée, et gérer le passage arrière combiné.

   1. 添加 `SoftmaxCrossEntropyLoss`类用于多类──对预测做软max,计算交叉损失,处理组合反向传播──在 3类螺旋数据集上测试──

2. Implémenter la planification du taux d'apprentissage dans l'optimisateur: ajouter un `set_lr()`Le système de calcul de la fréquence de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échantillon de l'échon de l'échantillon de l'échon de l'échon de l'échon de l'échon de l'échon de l'échon de l'échon de l'échon de l'échon de l'échon de l'échon de l'échon de l'échon de l'échon de l'échon de l'échon de l'échon de l'échon de l'échon de l'échon de l'échon de l'échon de l'échon de l'échon de l'échon de l'échon de l'échon de l'échon de l'échon de l'éch

   2. Dans les appareils d'optimisation, le taux d'apprentissage est réduit:`set_lr()`方法, connecté à la 9e classe de la régularisation des résidus ⋅ avec le réchauffement + l'entraînement des résidus ⋅ avec un rééquilibre constant LR

3. Ajouter un `save()`et `load()`La méthode de séquence qui sérialise tous les poids dans un fichier JSON et les charge à nouveau.

   3. 给 Sequentiel `save()`et `load()`方法, mettre tous les droits de séquence dans JSON 文件并加载回来──验证加载的模型产生和原模型相同的预测──

4. Appliquer une régulation de la perte de poids (L2) dans l'optimisateur Adam.`weight_decay`Paramètre qui réduit les poids vers zéro à chaque étape.

   4. Dans Adam 优化器实现权重衰减 (L2) 正则化 (L2) 添加`weight_decay`参数, chaque étape de la contraction du poids vers le zéro.

5. Remplacez la boucle d'entraînement par échantillon par une accumulation appropriée de gradients mini-partie: accumulez des gradients sur tous les échantillons d'un lot, puis divisez-les par la taille du lot et faites une étape d'optimisation. Mesurez si cela change la vitesse de convergence.

   5. Utilisez le bon mini-batch de gradience cumulée en remplacement de chaque cycle de formation: accumulez tous les gradients de l'échantillon dans un lot, puis déduisez-les en lots de taille, faites une fois l'optimisation progressive.

## Les termes clés

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Module | "A layer" | The base abstraction in a framework -- anything with forward(), backward(), and parameters() |
| Sequential | "Stack layers in order" | A container that chains modules, applying them in sequence for forward and reverse for backward |
| Forward pass | "Run the network" | Computing the output by passing input through each module in order |
| Backward pass | "Compute gradients" | Propagating the loss gradient through each module in reverse to compute parameter gradients |
| Parameters | "The trainable weights" | All values in the network that the optimizer can update -- weights and biases |
| Optimizer | "The thing that updates weights" | An algorithm that uses gradients to update parameters, implementing SGD, Adam, or other rules |
| DataLoader | "The thing that feeds data" | An iterator that splits a dataset into batches, optionally shuffling between epochs |
| Training mode | "model.train()" | A flag that enables stochastic behavior like dropout and batch normalization with batch stats |
| Evaluation mode | "model.eval()" | A flag that disables dropout and uses running statistics for batch normalization |
| Zero grad | "Clear the gradients" | Resetting all parameter gradients to zero before computing the next batch's gradients |

| 术语 | 俗称 | 实际含义 |
|------|------|---------|
| Module / 模块 | "一层" | 框架中的基础抽象——任何有 forward()、backward()、parameters() 的对象 |
| Sequential / 顺序容器 | "按顺序叠层" | 一个把模块串联起来的容器，前向按顺序、反向按逆序 |
| Forward pass / 前向传播 | "跑网络" | 把输入依次通过每个模块计算输出 |
| Backward pass / 反向传播 | "算梯度" | 把损失梯度反向通过每个模块计算参数梯度 |
| Parameters / 参数 | "可训练权重" | 网络中优化器能更新的所有值——权重和偏置 |
| Optimizer / 优化器 | "更新权重的东西" | 用梯度更新参数的算法，实现 SGD、Adam 或其他规则 |
| DataLoader / 数据加载器 | "喂数据的东西" | 把数据集切成批次的迭代器，可选地在 epoch 间打乱 |
| Training mode / 训练模式 | "model.train()" | 启用 Dropout、BN 用 batch 统计等随机行为的标志 |
| Evaluation mode / 评估模式 | "model.eval()" | 关闭 Dropout、BN 用运行统计量的标志 |
| Zero grad / 清零梯度 | "清掉梯度" | 在计算下一批梯度前把所有参数梯度重置为零 |

## Encore une lecture

- Paszke et coll., "PyTorch: un style impératif, haute performance de la bibliothèque d'apprentissage profond" (2019) -- le document décrivant les décisions de conception de PyTorch
  Paszke 等人,PyTorch: un style de haute performance en profondeur de formation(2019) description PyTorch  design decision
- Chollet, "Deep Learning with Python, Second Edition" (2021) -- Chapitre 3 couvre les internes de Keras avec la même abstraction de module/couche
  Chollet,Python profondeur de formation 2ème édition (2021) 3ème chapitreUtilisation du même module/couche de résumé de lecture Keras  intérieur mécanisme
- Johnson, "Tiny-DNN" (https://github.com/tiny-dnn/tiny-dnn) -- un cadre d'apprentissage en profondeur C++ uniquement en en-tête pour comprendre les internes du cadre
  Johnson,Tiny-DNN un pur titre de document C++ Framework d'apprentissage profond, utilisé pour comprendre le mécanisme interne du cadre
