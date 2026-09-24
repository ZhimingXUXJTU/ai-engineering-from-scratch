# Clasificación de imágenes

> Un clasificador es una función de píxeles a una distribución de probabilidades en clases.

> **【中文解读】**La imagen es una función de distribución de la probabilidad de la imagen a la clase en esencia. La función de la distribución de la imagen a la clase en esencia es la función de la distribución de la imagen a la clase en la que se encuentra la imagen.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 2 Lesson 09 (Model Evaluation), Phase 3 Lesson 10 (Mini Framework), Phase 4 Lesson 03 (CNNs) | **前置知识:** Phase 2 Lesson 09（模型评估），Phase 3 Lesson 10（迷你框架），Phase 4 Lesson 03（CNN）
**Time:** ~75 minutes | **时间:** ~75 分钟

## Objetivos de aprendizaje

- Construir una línea de clasificación de imágenes de extremo a extremo en el CIFAR-10: conjunto de datos, ampliación, modelo, ciclo de formación, evaluación
- Explicar el papel de cada componente (cargador de datos, pérdida, optimizador, programador, aumento) y predecir cómo se manifiesta la ruptura de cualquiera de ellos en la curva de pérdida
- Implementar mezcla, recorte y suavizamiento de etiquetas desde cero y justificar cuándo cada uno vale la pena añadir
- Leer una matriz de confusión y una tabla de precisión/recall por clase para diagnosticar fallas en los conjuntos de datos y modelos más allá de la precisión agregada

> **【中文解读】**El objetivo de aprendizaje enumera las capacidades centrales que debe dominarse después de completar la clase.


## El problema es la introducción del problema

Cada tarea de visión que se realiza se reduce a la clasificación de imágenes en algún nivel. La detección clasifica regiones. La segmentación clasifica píxeles. La recuperación se clasifica por similitud con los centros de clase.

> Cada misión visual entregada se reduce en cierta medida a la clasificación de imágenes. Se clasifica en la clasificación de regiones. Se clasifica en la clasificación de similitud de los centros de clasificación. Se clasifica en el ciclo de datos, en la estrategia de refuerzo, en la función de pérdida. Se evalúa la transferencia a la técnica de cada otra tarea en esta etapa.

> **【中文解读】**Todas las tareas visuales de implementación real pueden en esencia ser reducidas a categorías de imágenes: la prueba de objetivos es "a la categoría de la región", la división de significado es "a la categoría de la imagen", la búsqueda de imágenes es "a la clasificación de similitud según el centro de la categoría"......

La mayoría de los errores de clasificación no están en el modelo. Viven en la línea de la normalización: una normalización rota, un conjunto de capacitación sin cambios, un aumento que distorsiona las etiquetas, una división de validación contaminada por datos de capacitación, una tasa de aprendizaje que discrepa silenciosamente después de la época 30. Una CNN que alcanzara el 93% en CIFAR-10 con una configuración correcta normalmente obtiene un 70-75% con una rotura, y la curva de pérdida parece plausible todo el tiempo.

> La mayoría de los segmentos de bugs no están en el modelo. Se encuentran en la línea de flujo: errores de regeneración, no perturbados, aumento de etiquetas torcidas, verificación de contaminación de datos entrenados, tasa de aprendizaje en la fase de 30  post-silencia de difusión. Una configuración correcta puede alcanzar el 93% de CNN en CIFAR-10, normalmente sólo 70-75% bajo la configuración errónea, y la curva de pérdida parece ser muy razonable.

Esta lección conecta toda la tubería a mano para que cada pieza sea inspectable.`torchvision.datasets`que podría ocultar un insecto.

> Esta clase se realiza con la mano de construir toda la línea de flujo, para que cada parte sea inspectable.`torchvision.datasets`Todo lo que pueda ocultar un insecto.

> **【中文解读】**La mayoría de los segmentos de errores no están en el modelo en sí, sino en la línea de flujo: la regeneración ha cometido errores, el entrenamiento ha hecho desorden, ha destruido los etiquetas, ha contaminado los datos, ha diseminado la tasa de aprendizaje. La configuración correcta puede alcanzar el 93% del modelo, la configuración errónea puede alcanzar el 70-75%, y la pérdida de curvas parece ser normal.

## El concepto central.

### El sistema de clasificación

```mermaid
flowchart LR
    A["Dataset<br/>(images + labels)"] --> B["Augment<br/>(random transforms)"]
    B --> C["Normalise<br/>(mean/std)"]
    C --> D["DataLoader<br/>(batch + shuffle)"]
    D --> E["Model<br/>(CNN)"]
    E --> F["Logits<br/>(N, C)"]
    F --> G["Cross-entropy loss"]
    F --> H["Argmax<br/>at eval"]
    G --> I["Backward"]
    I --> J["Optimizer step"]
    J --> K["Scheduler step"]
    K --> E

    style A fill:#dbeafe,stroke:#2563eb
    style E fill:#fef3c7,stroke:#d97706
    style G fill:#fecaca,stroke:#dc2626
    style H fill:#dcfce7,stroke:#16a34a
```

Cada línea en este bucle es donde un insecto puede vivir.`model(x).softmax()`antes de que la pérdida calcule silenciosamente el gradiente equivocado.

> Cada línea de este ciclo es un error posible en el lugar donde existe.`model(x).softmax()`La ciudad se calculaba en silencio el grado de error.

> **【中文解读】**流水线中每一行都可能藏有 bug──交叉接收是原始logits(未经 softmax 的值), si primero se hace softmax 再传入损失 函数,梯度计算就完全错了但不会报错── Las ampliaciones se aplican solo a las entradas, no a las etiquetas  excepto para la mezcla, que mezcla ambas. `optimizer.zero_grad()`El error de aprendizaje se reduce a una velocidad de aprendizaje muy inestable, y cada uno de estos errores aplanan la curva de aprendizaje sin lanzar un error.

### Entropia cruzada, logits y softmax

Un clasificador produce `C`Los números por imagen llamados logits. Aplicando softmax los convierte en una distribución de probabilidades:

> Se producen imágenes por cada uno`C`个数字, llamados logits. 个数字, llamados logits. 个数字, llamados logits. 个数字, llamados logits. 个数字, llamados logits. 个数字, llamados logits. 个数字, llamados logits. 个数字, llamados logits. 个数字, llamados logits. 个数字, llamados logits. 个数字, llamados logits. 个数字, llamados logits. 个数字, llamados logits. 个数字, llamados logits. 个数字, llamados logits. 个数字, llamados logits. 个数字, llamados logits. 个数字, llamados logits. 个数字, llamados logits. 个数字, llamados logits. 个数字, llamados logits. 个数字, 个数字, 个数字, 个数字, 个数字, 个数, 个个个个个, 个个个, 个个个, 个个个, 个个个, 个个个, 个个, 个个, 个个, 个, 个, 个, 个, 个, 个, 个, 个, 个, 个, 个, 个, 个, 个, 个, 个, 个, 个, 个, 个, 个, 个, 个, 个, 个, 个, 个, 个, 个, 个, 个, 个, 个, 个, 个, 个, 个, 个, 个, 个, 个, 个, 个, 个, 个, 个, 个, 个, 个, 个, 个, 个, 个, 个, 个, 个, 个, 个, 个, 个, 个, 个, 个, 个, 个, 个, 个, 个, 个, 个, 个, 个, 个, 个, 个, 个, 个, 个, 个, 个, 个, 个, 个, 个, 

```
softmax(z)_i = exp(z_i) / sum_j exp(z_j)
```

La entropía cruzada mide la probabilidad de registro negativo de la clase correcta:

> 交叉衡正确类别的负对数概率:

```
CE(z, y) = -log( softmax(z)_y )
        = -z_y + log( sum_j exp(z_j) )
```

La forma de la mano derecha es la estable numéricamente (log-sum-exp).`nn.CrossEntropyLoss`La aplicación de softmax por primera vez es casi siempre un error  se calcula log(softmax(softmax(z))), una cantidad sin sentido.

> La forma de derecha es el número de valores estable (log-sum-exp)`nn.CrossEntropyLoss`En una operación se fusiona softmax + NLL, directamente recibiendo logits originales.

> **【中文解读】**PyTorch de `nn.CrossEntropyLoss`内部已经融合了软max + 负对数似然, directamente传入原始逻辑 即可──. Si primero se modifica softmax de nuevo con la mano, equivale a hacer dos softmax, gradiente calcular completamente error──.

### Por qué funciona el aumento

Una CNN tiene un sesgo inductivo para la traducción (de la distribución de peso) pero no tiene una invarianza incorporada a los cultivos, voltapés, nerviosismo de color o oclusión. La única manera de enseñarle esas invariencias es mostrándole píxeles que las ejercen.

> CNN tiene una inclinación de la distribución de la distribución de peso, pero no tiene ninguna variación interna en el corte, el cambio de color o la ocultación. El único método para enseñar a estos cambios es mostrar su forma de reflejar las imágenes.

> **【拓展：数据增强与模型泛化】**En los entrenamientos de modelos clásicos como ResNet, EfficientNet, los buenos y malos de las estrategias de aumento afectan directamente a la tasa de precisión del 3-5%. Google RandAugment y AutoAugment utilizan métodos de búsqueda para seleccionar automáticamente la mejor combinación de mejoras, ya ha sido ampliamente probado en ImageNet.

```
Original crop:  "dog facing left"
Flip:           "dog facing right"       <- same label, different pixels
Rotate(+15):    "dog, slight tilt"
Colour jitter:  "dog in warmer light"
RandomErasing:  "dog with patch missing"
```

La regla: el aumento debe conservar la etiqueta. El corte y la rotación en un dígito pueden convertir "6" en "9"; para ese conjunto de datos se utilizan rangos de rotación más pequeños y se escogen aumentos que respetan las invariencias específicas de dígitos.

> 规则:增强必须保持标签不变―― para el número realizar un oculto y la rotación puede convertir "6"  into "9"; para ese conjunto de datos, usted utiliza un rango de rotación más pequeño, y elige respetar el número específico invariable增强――

### Mezcla y corte

El aumento ordinario transforma los píxeles pero mantiene las etiquetas unincorporadas. **Mixup**y **cutmix**rompe eso interpolar los dos.

> Normalmente aumenta el cambio de imagen pero mantiene el etiquetado para un solo calor.**Mixup**Y **cutmix** Por medio de los dos realizarse el intercambio de valores rompió este punto.

```
Mixup:
  lambda ~ Beta(a, a)
  x = lambda * x_i + (1 - lambda) * x_j
  y = lambda * y_i + (1 - lambda) * y_j

Cutmix:
  paste a random rectangle of x_j into x_i
  y = area-weighted mix of y_i and y_j
```

Por qué ayuda: el modelo deja de memorizar objetivos espinosos y aprende a interpolar entre clases. La pérdida de entrenamiento aumenta, la precisión de las pruebas aumenta. Es la mejor actualización de robustez única más barata para cualquier clasificador.

> Por qué es útil: el modelo para parar de recordar punta de punta de un objetivo caliente, el aprendizaje entre clases de valores.

> **【拓展：Mixup 在大模型中的应用】**La idea de la mezcla se ha extendido al ámbito de la PNL para la inserción de textos para la mezcla de valores. En el entrenamiento de LLM, como ChatGPT, la tecnología de etiquetado y etiquetado de etiquetas también se usa ampliamente, ayudando a los modelos a generar una probabilidad de salida más calificada, reduciendo la excesividad de confianza.

### Limpiación de etiquetas

Un primo de la confusión.`[0, 0, 1, 0, 0]`, tren contra`[eps/C, eps/C, 1-eps, eps/C, eps/C]`para un pequeño `eps`El modelo de la producción de logits arbitrariamente afilados y mejora la calibración a casi ningún costo.`nn.CrossEntropyLoss(label_smoothing=0.1)`desde PyTorch 1.10.

> Mezcla de los próximos.`[0, 0, 1, 0, 0]` hacer entrenamiento, sino usar `[eps/C, eps/C, 1-eps, eps/C, eps/C]`, entre ellos `eps`En el caso de la torcha 1.10 se ha puesto en marcha un sistema de control de la velocidad de la torsión.`nn.CrossEntropyLoss(label_smoothing=0.1)`En el medio.

### Evaluamiento más allá de la precisión

La precisión agregada oculta el desequilibrio. Un clasificador binario de 90-10 que siempre predice la clase mayoritaria obtiene un puntaje del 90%.

>                                                                                                                                                                                                                                                               

- **Per-class accuracy** un número por clase; inmediatamente aparece las categorías con menos resultados.
  Por ejemplo, el número de personas que han estado en el país en el año pasado se ha reducido a un número de personas que han estado en el país en el año pasado.
- **Confusion matrix** C x C cuya fila i col j = el recuento de la clase verdadera i predicho como clase j; la diagonal es correcta, las diagonales fuera de la línea son donde vive el modelo.
  Traducción:混矩阵C x C 网格,行 i 列 j = 真实类别 i 被预测为类别 j 的计数;对角线是正确的,非对角线是你的模型出错的地方──
- **Top-1 / Top-5** si la clase correcta está en las predicciones de 1 o 5 principales; Top-5 importa para ImageNet porque clases como "Norwich terrier" vs "Norfolk terrier" son genuinamente ambigüas.
  El Top-5 para ImageNet es muy importante, ya que este tipo de categorías es realmente muy similar al "Norwich Terrier" vs. "Norfolk Terrier".
- **Calibration (ECE)**¿Se obtiene la predicción de confianza de 0,8 el 80% de las veces? las redes modernas son sistemáticamente demasiado seguras; fija con la escala de temperatura o el suavización de las etiquetas.
  China 翻译:校准(ECE) 0.8 置信度的预测 80% 的时间是对的吗?

> **【拓展：工业部署中的视觉系统】**En la implementación industrial real, los modelos de visión necesitan considerar la posibilidad de retraso, el tamaño del modelo, la adaptación de los dispositivos de borde, etc. TensorRT, ONNX Runtime, OpenVINO son herramientas de aceleración de la teoría de uso habitual.


## Construye y realiza.

> **【中文解读】**Este capítulo a través del código de la implementación de algoritmos centrales de cero. Este método "desde cero" puede ayudar a entender el principio detrás del marco, no se encuentra en la caja negra cuando se encuentran problemas.

```figure
receptive-field
```

## Construye el mismo

### Paso 1: Un conjunto de datos sintéticos deterministas

CIFAR-10 vive en disco. Para hacer que esta lección sea reproducible y rápida construimos un conjunto de datos sintéticos que se parecen a imágenes CIFAR  32x32 RGB con estructura específica de clase que el modelo debe aprender.

> CIFAR-10  existía en el disco. Para hacer que esta clase fuera replicable y rápida, construimos un conjunto de datos sintético que pareciera a CIFAR con un modelo que debe aprender de una estructura específica de 32x32 RGB  imágenes.

```python
import numpy as np
import torch
from torch.utils.data import Dataset


def synthetic_cifar(num_per_class=1000, num_classes=10, seed=0):
    rng = np.random.default_rng(seed)
    X = []
    Y = []
    for c in range(num_classes):
        centre = rng.uniform(0, 1, (3,))
        freq = 2 + c
        for _ in range(num_per_class):
            yy, xx = np.meshgrid(np.linspace(0, 1, 32), np.linspace(0, 1, 32), indexing="ij")
            r = np.sin(xx * freq) * 0.5 + centre[0]
            g = np.cos(yy * freq) * 0.5 + centre[1]
            b = (xx + yy) * 0.5 * centre[2]
            img = np.stack([r, g, b], axis=-1)
            img += rng.normal(0, 0.08, img.shape)
            img = np.clip(img, 0, 1)
            X.append(img.astype(np.float32))
            Y.append(c)
    X = np.stack(X)
    Y = np.array(Y)
    idx = rng.permutation(len(X))
    return X[idx], Y[idx]


class ArrayDataset(Dataset):
    def __init__(self, X, Y, transform=None):
        self.X = X
        self.Y = Y
        self.transform = transform

    def __len__(self):
        return len(self.X)

    def __getitem__(self, i):
        img = self.X[i]
        if self.transform is not None:
            img = self.transform(img)
        img = torch.from_numpy(img).permute(2, 0, 1)
        return img, int(self.Y[i])
```

Cada clase obtiene su propia paleta de colores y patrón de frecuencia, más ruido gaussiano para obligar al modelo a aprender la señal en lugar de memorizar píxeles. Diez clases, mil imágenes cada una, permutadas.

> Cada categoría tiene su propio patrón de regulación y frecuencia, además de ruido alto para obligar a los modelos a aprender señales y no imágenes de memoria.

### Paso 2: Normalización y ampliación

Los dos transforman que cada línea de visión tiene.

> Cada línea de flujo de imágenes tiene dos cambios.

```python
def standardize(mean, std):
    mean = np.array(mean, dtype=np.float32)
    std = np.array(std, dtype=np.float32)
    def _fn(img):
        return (img - mean) / std
    return _fn


def random_hflip(p=0.5):
    def _fn(img):
        if np.random.random() < p:
            return img[:, ::-1, :].copy()
        return img
    return _fn


def random_crop(pad=4):
    def _fn(img):
        h, w = img.shape[:2]
        padded = np.pad(img, ((pad, pad), (pad, pad), (0, 0)), mode="reflect")
        y = np.random.randint(0, 2 * pad)
        x = np.random.randint(0, 2 * pad)
        return padded[y:y + h, x:x + w, :]
    return _fn


def compose(*fns):
    def _fn(img):
        for fn in fns:
            img = fn(img)
        return img
    return _fn
```

Reflejado-pad antes de cosecha, no cero-pad, porque las fronteras negras son una señal que el modelo aprendería a ignorar de una manera inútil.

> Corte antes de usar reflejo llenado y no llenado, ya que el borde negro es un mensaje que el modelo se ignora de manera inútil

### Paso 3: Mezcla

Mezcla dos imágenes y dos etiquetas dentro del paso de entrenamiento. Implementado como un lote de transformación para que viva junto al pase hacia adelante en lugar de dentro del conjunto de datos.

> En el entrenamiento, se mezclan dos imágenes y dos etiquetas. Como un cambio de masa, se encuentra junto a la transmisión de la información y no dentro de la base de datos.

```python
def mixup_batch(x, y, num_classes, alpha=0.2):
    if alpha <= 0:
        return x, torch.nn.functional.one_hot(y, num_classes).float()
    lam = float(np.random.beta(alpha, alpha))
    idx = torch.randperm(x.size(0), device=x.device)
    x_mixed = lam * x + (1 - lam) * x[idx]
    y_onehot = torch.nn.functional.one_hot(y, num_classes).float()
    y_mixed = lam * y_onehot + (1 - lam) * y_onehot[idx]
    return x_mixed, y_mixed


def soft_cross_entropy(logits, soft_targets):
    log_probs = torch.log_softmax(logits, dim=-1)
    return -(soft_targets * log_probs).sum(dim=-1).mean()
```

`soft_cross_entropy`Se reduce a la habitual un-hot caso cuando el objetivo es exactamente un-hot.

> `soft_cross_entropy`Es un paso de la distribución de etiquetas de software. Cuando el objetivo es un solo calor, se descompone en la situación habitual de un solo calor.

### Paso 4: El ciclo de entrenamiento

La receta completa: un paso por los datos, gradientes una vez por lote, cronista paso una vez por época.

> Programa completo: se realiza una vez en toda la información, cada lote calcula una escala, cada época se modifica una vez en la tasa de aprendizaje.

```python
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torch.optim import SGD
from torch.optim.lr_scheduler import CosineAnnealingLR

def train_one_epoch(model, loader, optimizer, device, num_classes, use_mixup=True):
    model.train()
    total, correct, loss_sum = 0, 0, 0.0
    for x, y in loader:
        x, y = x.to(device), y.to(device)
        if use_mixup:
            x_m, y_soft = mixup_batch(x, y, num_classes)
            logits = model(x_m)
            loss = soft_cross_entropy(logits, y_soft)
        else:
            logits = model(x)
            loss = nn.functional.cross_entropy(logits, y, label_smoothing=0.1)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        loss_sum += loss.item() * x.size(0)
        total += x.size(0)
        # Training accuracy vs the un-mixed labels `y` is only an approximation
        # when mixup is on (the model saw soft targets, not y). Treat it as a
        # rough progress signal; rely on val accuracy for real performance.
        with torch.no_grad():
            pred = logits.argmax(dim=-1)
            correct += (pred == y).sum().item()
    return loss_sum / total, correct / total


@torch.no_grad()
def evaluate(model, loader, device, num_classes):
    model.eval()
    total, correct = 0, 0
    loss_sum = 0.0
    cm = torch.zeros(num_classes, num_classes, dtype=torch.long)
    for x, y in loader:
        x, y = x.to(device), y.to(device)
        logits = model(x)
        loss = nn.functional.cross_entropy(logits, y)
        pred = logits.argmax(dim=-1)
        for t, p in zip(y.cpu(), pred.cpu()):
            cm[t, p] += 1
        loss_sum += loss.item() * x.size(0)
        total += x.size(0)
        correct += (pred == y).sum().item()
    return loss_sum / total, correct / total, cm
```

Cinco invariantes que comprueba cada vez que escribe un ciclo de entrenamiento:

> Cada ciclo de entrenamiento de escritura, cinco variables de la inspección:

1. `model.train()`antes de la formación, `model.eval()`Antes de la evaluación  se desprende del comportamiento normal y de los lotes.
2. `.zero_grad()`antes de`.backward()`¿ Qué ?
3. `.item()`Cuando se acumulan métricas para que nada mantiene vivo el gráfico de cálculo.
4. `@torch.no_grad()`Durante la evaluación  ahorra memoria y tiempo, previene accidentes sutiles.
5. Argmax contra los logits crudos, no softmax  el mismo resultado, una operación menos.

### Paso 5: Ponlo juntos

Utilice el `TinyResNet`de la lección anterior, entrenar por algunas épocas, evaluar.

> Uso de la primera clase `TinyResNet`, entrenar varias épocas, evaluar:.

```python
from main import synthetic_cifar, ArrayDataset
from main import standardize, random_hflip, random_crop, compose
from main import mixup_batch, soft_cross_entropy
from main import train_one_epoch, evaluate
# TinyResNet comes from the previous lesson (03-cnns-lenet-to-resnet).
# Adjust the import path to wherever you stored the previous lesson's code.
from cnns_lenet_to_resnet import TinyResNet  # example placeholder

X, Y = synthetic_cifar(num_per_class=500)
split = int(0.9 * len(X))
X_train, Y_train = X[:split], Y[:split]
X_val, Y_val = X[split:], Y[split:]

mean = [0.5, 0.5, 0.5]
std = [0.25, 0.25, 0.25]
train_tf = compose(random_hflip(), random_crop(pad=4), standardize(mean, std))
eval_tf = standardize(mean, std)

train_ds = ArrayDataset(X_train, Y_train, transform=train_tf)
val_ds = ArrayDataset(X_val, Y_val, transform=eval_tf)

train_loader = DataLoader(train_ds, batch_size=128, shuffle=True, num_workers=0)
val_loader = DataLoader(val_ds, batch_size=256, shuffle=False, num_workers=0)

device = "cuda" if torch.cuda.is_available() else "cpu"
model = TinyResNet(num_classes=10).to(device)
optimizer = SGD(model.parameters(), lr=0.1, momentum=0.9, weight_decay=5e-4, nesterov=True)
scheduler = CosineAnnealingLR(optimizer, T_max=10)

for epoch in range(10):
    tr_loss, tr_acc = train_one_epoch(model, train_loader, optimizer, device, 10, use_mixup=True)
    va_loss, va_acc, _ = evaluate(model, val_loader, device, 10)
    scheduler.step()
    print(f"epoch {epoch:2d}  lr {scheduler.get_last_lr()[0]:.4f}  "
          f"train {tr_loss:.3f}/{tr_acc:.3f}  val {va_loss:.3f}/{va_acc:.3f}")
```

En el conjunto de datos sintético, esto llega a una precisión de validación casi perfecta dentro de cinco épocas, que es el punto: la tubería es correcta, el modelo puede aprender lo que es aprendizaje.

> En el conjunto de datos sintetizados, en cinco épocas se puede alcanzar una tasa de precisión de verificación casi perfecta, es el punto: el flujo de agua es correcto, el modelo puede aprender algo que se puede aprender.

### Paso 6: Lea la matriz de confusión

La precisión por sí sola nunca te dice dónde está fallando el modelo.

> La precisión individual nunca te dirá en qué modelo fallarás.

```python
def print_confusion(cm, labels=None):
    c = cm.shape[0]
    labels = labels or [str(i) for i in range(c)]
    print(f"{'':>6}" + "".join(f"{l:>5}" for l in labels))
    for i in range(c):
        row = cm[i].tolist()
        print(f"{labels[i]:>6}" + "".join(f"{v:>5}" for v in row))
    print()
    tp = cm.diag().float()
    fp = cm.sum(dim=0).float() - tp
    fn = cm.sum(dim=1).float() - tp
    prec = tp / (tp + fp).clamp_min(1)
    rec = tp / (tp + fn).clamp_min(1)
    f1 = 2 * prec * rec / (prec + rec).clamp_min(1e-9)
    for i in range(c):
        print(f"{labels[i]:>6}  prec {prec[i]:.3f}  rec {rec[i]:.3f}  f1 {f1[i]:.3f}")

_, _, cm = evaluate(model, val_loader, device, 10)
print_confusion(cm)
```

Las filas son clases verdaderas, las columnas son predicciones. Un grupo de recuentos fuera de diagonales entre las clases 3 y 5 significa que el modelo confunde esas dos y le da un punto de partida para la recopilación de datos dirigidos o un aumento específico de la clase.

> El conjunto de las clases real, la clase es predicción. La agrupación de las no-contradictaciones entre las clases 3 y 5 significa que el modelo mezcla estas dos clases y proporciona un punto de partida para la recopilación de datos específicos o la mejora de las clases.



## Usalo con el marco de ejecución

> **【中文解读】**Este capítulo muestra cómo utilizar un marco maduro (como PyTorch、HuggingFace, etc.) para aplicar rápidamente esta tecnología. En los proyectos reales, se realiza con prioridad el uso de un marco experimentado, se pueden reducir errores y mejorar la eficiencia de desarrollo.


`torchvision`En el caso de un CIFAR-10 real, la línea completa es de cuatro líneas más un bucle de entrenamiento.

> `torchview`Para el verdadero CIFAR-10, el flujo completo es cuatro líneas de código, además de un ciclo de entrenamiento.

```python
from torchvision.datasets import CIFAR10
from torchvision.transforms import Compose, RandomCrop, RandomHorizontalFlip, ToTensor, Normalize

mean = (0.4914, 0.4822, 0.4465)
std = (0.2470, 0.2435, 0.2616)
train_tf = Compose([
    RandomCrop(32, padding=4, padding_mode="reflect"),
    RandomHorizontalFlip(),
    ToTensor(),
    Normalize(mean, std),
])
eval_tf = Compose([ToTensor(), Normalize(mean, std)])

train_ds = CIFAR10(root="./data", train=True,  download=True, transform=train_tf)
val_ds   = CIFAR10(root="./data", train=False, download=True, transform=eval_tf)
```

Dos cosas que hay que notar: la media/std es **dataset-specific** computado en el conjunto de capacitación CIFAR-10, no ImageNet  y el reflejo pad es la política de cultivo por defecto de la comunidad.

> 两点注意事项: promedio de valor/standard差是**数据集特定的** Calculado en el CIFAR-10  entrenamiento conjunto, en lugar de ImageNet  Reflexion Filled es la estrategia de corte de la comunidad por defecto.  Aquí copia de la pegada ImageNet  estadística causará una tasa de precisión de aproximadamente 1% de fuga, hasta que se descubra un modelo de análisis humano.


> **【拓展：数据标注与质量】**视觉任务的效果高度依赖标签数据质量──标签工作室、CVAT es la principal herramienta de marcado──在工业场景中,主动学习(Active Learning) puede reducir el costo de marcado: modelo a un requerimiento de muestras indeterminadas, marcación automática de muestras de determinación──

## Envíe el producto .

> **【中文解读】**Este capítulo se centra en cómo se puede implementar el modelo como producto disponible. Desde el modelo original hasta el sistema de producción, se deben considerar múltiples dimensiones de optimización de rendimiento, tratamiento de errores, control, etc.


Esta lección produce:

- `outputs/prompt-classifier-pipeline-auditor.md` una solicitud que revisa un guión de entrenamiento para las cinco invariantes anteriores y pone de manifiesto la primera violación.
- `outputs/skill-classification-diagnostics.md` una habilidad que, dada una matriz de confusión y una lista de nombres de clases, resume los fallos por clase y propone la solución única más impactante.

> **【中文解读】**Practice los temas de fácil/medio/duro  3 difficulty to pass in  Recomenda al menos completar los temas de grado medio  Grado duro  para la preparación de la entrevista


## Los ejercicios.

1. **(Easy | 简单)**Explique por qué la pérdida de tren con mezcla es mayor pero la precisión de la val es similar o mejor.
   Se dividen con / sin mezcla  entrenamiento 5 épocas, dibujo de entrenamiento y prueba de pérdida  curva, explica por qué la pérdida de entrenamiento de mezcla es más alta pero la tasa de precisión de prueba no es diferente¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬

2. **(Medium | 中等)**Implemente Cutout  cero un cuadrado aleatorio de 8x8 en cada imagen de entrenamiento  y ejecute una ablación vs no aumento, hflip+crop, hflip+crop+cutout, hflip+crop+mixup.
   实现 Cutout (con frecuencia oculta en 8x8 区域),对无增强,翻转+剪剪,翻转+剪+剪+Cutout,翻转+剪+剪+Mixup 四种方案做消融实验,报告验证准确率──

3. **(Hard | 困难)**Construir una línea de CIFAR-100 (100 clases, el mismo tamaño de entrada) y reproducir un entrenamiento ResNet-34 ejecutado con una precisión de menos del 1% de la publicada.
   搭建 CIFAR-100 流水线(100 类),复现 ResNet-34 训练结果到与公开准确率相差 1% 以内──进阶:搜索三种学习率和两种权重衰减,记录到CSV,生成混矩阵中最容易混的类别对──

## Términos clave .

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|----------------------|---------|
| Logits | "Raw outputs" | The pre-softmax vector of C numbers per image; cross-entropy expects these, not softmaxed values | Logits：softmax 之前的原始输出向量，交叉熵直接接收它 |
| Cross-entropy | "The loss" | Negative log-probability of the correct class; combines log-softmax and NLL in one stable op | 交叉熵：正确类别的负对数概率，融合了 log-softmax 和 NLL |
| DataLoader | "The batcher" | Wraps a dataset with shuffling, batching, and (optional) multi-worker loading; gets blamed for half of training bugs | 数据加载器：封装数据集的打乱、分批、多进程加载 |
| Augmentation | "Random transforms" | Any pixel-level transform at training time that preserves the label; teaches invariances the CNN does not have natively | 数据增强：训练时保持标签不变的像素级变换，教会模型 CNN 天生不具备的不变性 |
| Mixup / Cutmix | "Mix two images" | Blend both inputs and labels so the classifier learns smooth interpolations instead of hard boundaries | Mixup/Cutmix：混合两张图像及其标签，让分类器学习平滑插值 |
| Label smoothing | "Softer targets" | Replace one-hot with (1-eps, eps/(C-1), ...); improves calibration and slightly boosts accuracy | 标签平滑：用软标签替代 one-hot，改善概率校准 |
| Top-k accuracy | "Top-5" | The correct class is in the k highest-probability predictions; used on datasets with genuinely ambiguous classes | Top-k 准确率：正确类别在前 k 个预测中即算对 |
| Confusion matrix | "Where errors live" | C x C table where entry (i, j) counts images of true class i predicted as j; diagonal is right, off-diagonal tells you what to fix | 混淆矩阵：C×C 表格，对角线是正确预测，非对角线揭示混淆的类别对 |

> **【中文解读】**延伸阅读 proporciona un alto nivel de recursos para el aprendizaje profundo. Estos artículos y cursos son los referentes clásicos en el campo, adecuados para los lectores que necesitan una comprensión profunda.


## Más Leer más Leer más

- [CS231n: Training Neural Networks](https://cs231n.github.io/neural-networks-3/) todavía el recorrido más claro de la línea de formación en una sola página
- [Bag of Tricks for Image Classification (He et al., 2019)](https://arxiv.org/abs/1812.01187) cada pequeño truco que juntos añade 3-4% a la precisión de ResNet en ImageNet
- [mixup: Beyond Empirical Risk Minimization (Zhang et al., 2017)](https://arxiv.org/abs/1710.09412) el original de la mezcla de documentos; tres páginas de teoría más experimentos convincentes
- [Why temperature scaling matters (Guo et al., 2017)](https://arxiv.org/abs/1706.04599) el papel que demostró que las redes modernas están calibradas erróneamente y se fijó con un parámetro escalar
