# Números complexos para IA.

> A raiz quadrada de -1 não é imaginária, é a chave para rotações, frequências e metade do processamento de sinais.
> A raiz quadrada de -1 não é "fals" e é a chave para o campo de rotação, frequência e meio de processamento de sinais.

**Type:** Learn | **类型:** 学习
**Language:**O Python .**语言:**Python
**Prerequisites:** Phase 1, Lessons 01-04 (linear algebra, calculus) | **前置知识:** Phase 1, 第 01-04 课（线性代数、微积分）
**Time:** ~60 minutes | **时间:** ~60 分钟

## Objetivos de aprendizagem

- Realizar aritmética complexa (aditar, multiplicar, dividir, conjugar) em forma retangular e polar
  执行复数运算(加、乘、除、共), incluindo forma de坐标直角和极坐标
- Aplicar a fórmula de Euler para converter entre exponenciais complexos e funções trigonometricas
   aplicação                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
- Implementar a Transforma Fourier Discreta usando raízes complexas de unidade
  Utilize unit root implement separation 里叶变换 (DFT)
- Explicar como as rotações complexas são a base das codificações posicionais RoPE e sinusoidais em transformadores
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               


> **【中文解读】**
> 虚数 i é a chave para a rotação e frequência. RoPE 位置编码 (RPG) do transformador (LMA) é a chave para a rotação e frequência.

## O problema é o problema da introdução

Abres um artigo sobre as transformações de Fourier e há`i`Olham para os codificadores de posição do transformador e veem`sin`E ...`cos`As partes reais e imaginárias de exponenciais complexos.

> Tu abriste um artigo sobre mudanças de humor, por toda parte.`i`── você vê Transformer  localização                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     `sin`和 `cos` são partes reais e partes falsas do índice de repetição.

Os números complexos parecem abstratos. Um sistema de números construído na raiz quadrada de -1 parece um truque matemático. Mas não é um truque. É a linguagem natural das rotações e oscilações. Sempre que algo gira, vibra ou oscila, os números complexos são a ferramenta certa.

> O número é um número abstrato. É construído em raiz quadrada de -1 e parece ser um jogo matemático. Mas não é um jogo. É uma linguagem natural de rotação e oscilação.

Sem entender números complexos, você não pode entender a Transformação de Fourier Discreta. Você não pode entender a FFT. Você não pode entender como RoPE (Rotary Position Embedding) funciona em modelos de linguagem modernos. Você não pode entender por que codificações posicionais sinusoidais no papel original Transformer usam as frequências que fazem.

> Não entendo o número de vezes, você não consegue entender o número de vezes, não consegue entender o número de vezes, não consegue entender o número de vezes, não consegue entender o número de vezes, não consegue entender o número de vezes, não consegue entender o número de vezes, não consegue entender o número de vezes, não consegue entender o número de vezes, não consegue entender o número de vezes, não consegue entender o número de vezes, não consegue entender o número de vezes, não consegue entender o número de vezes, não consegue entender o número de vezes, não consegue entender o número de vezes, não consegue entender o número de vezes, não consegue entender o número de vezes, não consegue entender o número de vezes, não consegue entender o número de vezes, não consegue entender o número de vezes, não consegue entender o número de vezes, não consegue entender o número de vezes, não consegue entender o número de vezes, não consegue entender o número de vezes, não consegue entender o número de vezes, não consegue entender o número de vezes, não consegue entender o número de vezes, não consegue entender o número de vezes, não consegue entender o número de vezes, não consegue usar o número de vezes.

Esta lição construi aritmética complexa a partir do zero, liga-a à geometria e mostra-lhe exatamente onde os números complexos aparecem na aprendizagem de máquina.

> Esta aula foi desenvolvida a partir de zero construção de quadros de cálculo, ligando-os à geometria, e exatamente mostrando a posição do quadros em aprendizado de máquina.

## O conceito central.

> **【中文解读】**
> 复数的核心洞察:i 不是"虚"的, é uma operação de rotação de 90 graus.

> **【拓展：复数在 AI 中的实际应用规模】**
> A série LLaMA do OpenAI GPT-4、Meta de LLaMA  usou RoPE(Rotary Position Embedding), em essência é repetida rotação。 cada atenção sobre a posição codificação execução repetida乘法。 para LLaMA-2-70B(80 个注意力头,序列长度 4096), cada passo de raciocínio executar milhões de vezes repetidas rotações。音频 AI 领域(como OpenAI Whisper) depende de FFT(快速里叶变换), todos os cálculos são concluídos em repetidas áreas。

### O que é um número complexo?

Um número complexo tem duas partes: uma parte real e uma parte imaginária.

> 复数有两部分:实部 (Real Part) 和虚部 (虚部)

```
z = a + bi

where:
  a is the real part
  b is the imaginary part
  i is the imaginary unit, defined by i^2 = -1
```

É isso. Você estende a linha de números em um plano. Os números reais sentam-se em um eixo. Os números imaginários sentam-se no outro. Cada número complexo é um ponto neste plano.

> É assim. Você expande o eixo numérico em uma superfície.

### Aritmética complexa

**Addition.**Adicione as partes reais juntas, adicione as partes imaginárias juntas.

> **加法。**- Não, não, não.

```
(a + bi) + (c + di) = (a + c) + (b + d)i

Example: (3 + 2i) + (1 + 4i) = 4 + 6i
```

**Multiplication.**Use a lei distributiva e lembre-se de que i^2 = -1.

> **乘法。**Utilize distribuição, lembre-se de i^2 = -1──

```
(a + bi)(c + di) = ac + adi + bci + bdi^2
                 = ac + adi + bci - bd
                 = (ac - bd) + (ad + bc)i

Example: (3 + 2i)(1 + 4i) = 3 + 12i + 2i + 8i^2
                            = 3 + 14i - 8
                            = -5 + 14i
```

**Conjugate.**Vire o sinal da parte imaginária.

> **共轭（Conjugate）。**翻转虚部的符号──

```
conjugate of (a + bi) = a - bi
```

O produto de um número complexo e seu conjugado é sempre real:

> O número multiplicado e o número multiplicado são números reais:

```
(a + bi)(a - bi) = a^2 + b^2
```

**Division.**Multiplicar o numerador e o denominador pelo conjugado do denominador.

> **除法。**分子和分母同时乘以分母的共──

```
(a + bi) / (c + di) = (a + bi)(c - di) / (c^2 + d^2)
```

Isso elimina a parte imaginária do denominador, dando-lhe um número complexo limpo.

> Isso elimina o divisor de divisão, obtendo um número de vezes mais puro.

### O plano complexo

O plano complexo mapeia cada número complexo para um ponto 2D. O eixo horizontal é o eixo real, o eixo vertical é o eixo imaginário.

> 复平面将每个复数映射为2D点──水平轴是实轴,垂直轴是虚轴──

```
z = 3 + 2i  corresponds to the point (3, 2)
z = -1 + 0i corresponds to the point (-1, 0) on the real axis
z = 0 + 4i  corresponds to the point (0, 4) on the imaginary axis
```

Um número complexo é simultaneamente um ponto e um vetor da origem. Esta interpretação dupla é o que torna os números complexos úteis para a geometria.

> O número duplo é um ponto e um volume de origem do ponto de partida.

### Forma polar

Qualquer ponto no plano pode ser descrito pela sua distância da origem e o seu ângulo do eixo real positivo.

> Qualquer ponto na superfície pode ser descrito a partir de um ângulo de distância do ponto de origem e do eixo real.

```
z = r * (cos(theta) + i*sin(theta))

where:
  r = |z| = sqrt(a^2 + b^2)     (magnitude, or modulus)
  theta = atan2(b, a)             (phase, or argument)
```

A forma retangular (a + bi) é boa para adição. A forma polar (r, theta) é boa para multiplicação.

> 直角坐标形式 (a + bi) 适合加法。极坐标形式 (r, theta) 适合乘法。

**Multiplication in polar form.**Multiplicar as magnitudes, adicionar os ângulos.

> **极坐标形式的乘法。**- Não, não.

```
z1 = r1 * e^(i*theta1)
z2 = r2 * e^(i*theta2)

z1 * z2 = (r1 * r2) * e^(i*(theta1 + theta2))
```

É por isso que os números complexos são perfeitos para rotações. Multiplicar por um número complexo com magnitude 1 é uma rotação pura.

> É por isso que o número de múltiplas é perfeitamente adequado à rotação.

### A fórmula de Euler

A ponte entre exponenciais complexos e trigonometria:

> O ponto de partida entre o índice de repunto e o triângulo:

```
e^(i*theta) = cos(theta) + i*sin(theta)
```

Esta é a fórmula mais importante nesta lição.

> É a fórmula mais importante do curso.

```
e^(i*pi) = cos(pi) + i*sin(pi) = -1 + 0i = -1

Therefore: e^(i*pi) + 1 = 0
```

Cinco constantes fundamentais (e, i, pi, 1, 0) ligadas em uma equação.

> 五个基本常数 ((e、i、pi、1、0) 统一在一个方程中──

### Por que a fórmula de Euler é importante para ML

A fórmula de Euler diz que`e^(i*theta)`A rotação total é a rotação total é a rotação total é a rotação total é a rotação total é a rotação total é a rotação total é a rotação total é a rotação total é a rotação total é a rotação total é a rotação total é a rotação total é a rotação total é a rotação total é a rotação total é a rotação total é a rotação total é a rotação total é a rotação total é a rotação total é a rotação total é a rotação total é a rotação total é a rotação total é a rotação total é a rotação total é a rotação total é a rotação total é a rotação total é a rotação total é a rotação total é a rotação total é a rotação total é a rotação total é a rotação total é a rotação total é a rotação total é a rotação total é a rotação total é a rotação total é a rotação total.

> 欧拉公式说 `e^(i*theta)`随着thea 变化描绘单位圆――theta = 0 时在 (1, 0)──theta = pi/2 时在 (0, 1)──theta = pi 时在 (-1, 0)──theta = 3*pi/2 时在 (0, -1)──完整旋转是thea = 2*pi。

Isto significa que os exponenciais complexos são rotações.

> Isto significa que o índice de repetição é a rotação. A rotação está presente no processamento de sinais e no ML.

> **【中文解读】**
> 欧拉公式 e^(i*theta) = cos(theta) + i*sin(theta) é a fórmula mais importante do curso.

### Conexão a rotações 2D

Multiplicando o número complexo (x + yi) por e^(i*theta) gira o ponto (x, y) por ângulo theta em torno da origem.

> 将复数 (x + yi) 乘以 e^(i*theta) 将点 (x, y) 绕原点旋转角 theta。

```
Rotation via complex multiplication:
  (x + yi) * (cos(theta) + i*sin(theta))
  = (x*cos(theta) - y*sin(theta)) + (x*sin(theta) + y*cos(theta))i

Rotation via matrix multiplication:
  [cos(theta)  -sin(theta)] [x]   [x*cos(theta) - y*sin(theta)]
  [sin(theta)   cos(theta)] [y] = [x*sin(theta) + y*cos(theta)]
```

Eles produzem resultados idênticos. Multiplicação complexa é rotação 2D. A matriz de rotação é apenas multiplicação complexa escrita em notação de matriz.

> Eles produzem resultados completamente iguais. O número multiplicado é 2D.

```mermaid
graph TD
    subgraph "Complex Multiplication = 2D Rotation"
        A["z = x + yi<br/>Point (x, y)"] -->|"multiply by e^(i*theta)"| B["z' = z * e^(i*theta)<br/>Point rotated by theta"]
    end
    subgraph "Equivalent Matrix Form"
        C["vector [x, y]"] -->|"multiply by rotation matrix"| D["[x cos theta - y sin theta,<br/> x sin theta + y cos theta]"]
    end
    B -.->|"same result"| D
```

### Fámeros e sinais rotativos

Um complexo exponencial e^(i*omega*t) é um ponto que gira em torno do círculo unitário em frequência angular omega.

> 复指数 e^(i*omega*t) é um ponto de rotação em torno de uma unidade de frequência de um círculo.

A parte real deste ponto de rotação é cosm * omega * t. A parte imaginária é sin * omega * t. Um sinal sinusoidal é a sombra de um número complexo rotativo.

> Esse movimento é um movimento de movimento que se torna um movimento de movimento.

```
e^(i*omega*t) = cos(omega*t) + i*sin(omega*t)

Real part:      cos(omega*t)    -- a cosine wave
Imaginary part: sin(omega*t)    -- a sine wave
```

Esta é a representação do fator. Em vez de rastrear uma onda sinusal movida, você rastreia uma seta que gira suavemente. As mudanças de fase se tornam offsets de ângulo. As mudanças de amplitude se tornam mudanças de magnitude. A adição de sinais se torna adição de vetores.

> É o que o fator faz: não precisa de rastrear a onda de cordas de um movimento, mas sim de rastrear a arco de rotação plana.

### Raízes da unidade

As raízes N-a da unidade são N pontos igualmente espaçados no círculo unitário:

> N 次单位根(Róis da Unidade) é um círculo de unidades e de N 个点 distribuídos entre si:

```
w_k = e^(2*pi*i*k/N)    for k = 0, 1, 2, ..., N-1
```

Para N = 4, as raízes são: 1, i, -1, -i (os quatro pontos da bússola).
Para N = 8, você obtém os quatro pontos da bússola mais os quatro diagonais.

As raízes da unidade são a base da Transforma de Fourier Discreta.

> A unidade-raiz é a base da separação entre os níveis de variação.

> **【中文解读】**
> 单位根是N 个等等间距分布在单位圆上的点――它们的两个奇特性:(1) Cada modelo é de um modo, é de um modo;(2) Tudo se suma de um modo, é de um modo, é de um modo, é de um modo, é de um modo, é de um modo, é de um modo, é de um modo, é de um modo, é de um modo, é de um modo, é de um modo, é de um modo, é de um modo, é de um modo, é de um modo, é de um modo, é de um modo, é de um modo, é de um modo, é de um modo, é de um modo, é de um modo, é de um modo, é de um modo, é de um modo, é de um modo, é de um modo, é de um modo, é de um modo, é de um modo, é de um modo, é de um modo, de um modo, de um modo, de um modo, de um modo, de um modo, de um modo, de um modo, de um modo, de um modo, de um modo, de um modo, de um, de um, de um, de um, de um, de um, de um, de um, de um, ou de um, de um, de um, de um, de um, de um, ou de um, de um, de um, de um, ou de um, de um, ou de um, de um, de um, ou de outro, de um, ou de outro, ou de outro, de, ou de, ou de, ou de outro, ou de, ou de outro, ou de, ou de, ou de outro, ou de, ou de, ou de, ou de, ou de, ou de, ou de, ou de, ou de, ou de, de, ou de, ou de, ou de, ou de, ou de, ou de, ou de, ou de, ou de, ou de, de, ou de, ou de, ou de, ou de, ou de, ou de, ou de, ou de, ou de, ou de, ou de, ou de, ou de, ou de, ou de, ou de, ou de, ou de, ou de, ou de, ou de, ou de, ou de, ou de, ou de

### Conexão ao DFT

A Transforma Fourier Discreta de um sinal x[0], x[1], ..., x[N-1] é:

> 信号 x[0], x[1], ..., x[N-1] 的离散里叶变换为:

```
X[k] = sum_{n=0}^{N-1} x[n] * e^(-2*pi*i*k*n/N)
```

Cada X[k] mede o quanto o sinal correlaciona com a raiz k-th da unidade - um sinusoide complexo na frequência k. O DFT quebra um sinal em N fases rotativas e diz-lhe a amplitude e fase de cada uma.

> Cada X[k] mede o sinal de correlação com a primeira k 个单位根频率为 k 的复正弦波──DFT irá dividir o sinal em N 个旋转相量, dizendo-lhe a amplitude e o lugar de cada fase──

### Porque não sou imaginário

A palavra "imaginária" é um acidente histórico. Descartes usou-a de forma desrespeitosa. Mas i não é mais imaginário do que os números negativos eram quando as pessoas os rejeitaram pela primeira vez. Os números negativos respondem "o que subtraímos de 5 de 3 para obter?" A unidade imaginária responde "o que você quadrada para obter -1?"

> A expressão "虚" é um caso histórico. Descartes usou-a para se tornar uma "favorita". Mas não é comparado ao número negativo inicialmente rejeitado.

Mais útil: i é um operador de rotação de 90 graus. Multiplicar um número real por i uma vez, você gira 90 graus para o eixo imaginário. Multiplicar por i novamente (i^2), você gira mais 90 graus - agora você está apontando na direção real negativa. É por isso que i^2 = -1. Não é misterioso. É uma meia-volta construída a partir de duas quartas-volta.

> Mais útil entender:i é um cálculo de rotação de 90 graus. O número real será multiplicado por i uma vez, você girará 90 graus até o虚轴.

É por isso que os números complexos estão em toda a engenharia. Qualquer coisa que gira - ondas eletromagnéticas, estados quânticos, oscilações de sinal, codificações posicionais - é naturalmente descrita por números complexos.

> É por isso que o número duplo não está presente na engenharia. Qualquer coisa que gira é descrita naturalmente por números duplos.

### Exponenciais complexos vs funções trigonometricas

Antes da fórmula de Euler, os engenheiros escreveram sinais como A*cos(omega*t + phi) - amplitude A, frequência omega, fase phi. Isso funciona, mas torna a aritmética dolorosa. Adicionar dois cosinos com fases diferentes requer identidades trigonômétricas.

> Antes da fórmula, o engenheiro escreverá o sinal em A*cos(omega*t + phi) 幅度 A、 frequência omega、相位 phi。 Isso é possível, mas fazer o cálculo é doloroso。相加两个不同相位的余弦需要三角恒等式。

Com exponenciais complexos, o mesmo sinal é A*e^(i*(omega*t + phi)). Adicionar dois sinais é apenas adicionar dois números complexos. Multiplicar (modular) é apenas multiplicar magnitudes e adicionar ângulos. As mudanças de fase se tornam adições de ângulo.

> Utilize duplo índice, similar signal is A*e^(i*(omega*t + phi))。 dois sinais相加就是二复数相加──相乘(调制)就是模相乘、角相加──相位偏移变成角加法──频率偏移变成乘相量──

O campo inteiro de processamento de sinais mudou para notação exponencial complexa porque a matemática é mais limpa. O "sinal real" é sempre apenas a parte real da representação complexa. A parte imaginária é levada junto como contabilidade, fazendo com que toda a álgebra funcione naturalmente.

> Todo o campo de processamento de sinais se move para o índice de representação, porque matemática é mais simples.

> **【拓展：复数在量子计算中的角色】**
> Base de cálculo quântico态是复数向量── estado de um qubbit é alfa  0> + beta    1>, em que alpha^2 + beta  2 = 1,alpha 和 beta 都是复数──量子门是复数矩阵── Google's Sycamore 量子芯片 量子芯片 拥有53 量子比特,其状态向量 拥有2^53 复数分──量子机器学习(QML) opera diretamente no复数空间──

### Conexão a transformadores

**Sinusoidal positional encodings**(papel original de transformador):

```
PE(pos, 2i) = sin(pos / 10000^(2i/d))
PE(pos, 2i+1) = cos(pos / 10000^(2i/d))
```

Os pares de pecados e cos são as partes reais e imaginárias de exponenciais complexos em diferentes frequências. Cada frequência fornece uma "resolução" diferente para a posição de codificação. As frequências baixas mudam lentamente (posição grosseira). As frequências altas mudam rapidamente (posição fina). Juntas dão a cada posição uma impressão digital de frequência única.

> Sin 和 cos 对是不同频率复指数的实部和虚部── cada frequência é codificada para uma posição fornecendo diferentes "resoluções"── baixa frequência variação lenta (粗粒度位置)──高频变化快速 (细粒度位置)── eles juntos fornecem uma única frequência para cada posição──

**RoPE (Rotary Position Embedding)**A atenção é calculada usando esses vetores rotativos, tornando o modelo sensível à posição relativa através da multiplicação complexa.

> **RoPE（旋转位置编码）**Mais adiante. É evidente que a consulta e a chave vão ser multiplicadas por uma massa de rotação múltipla.

> **【拓展：RoPE 在 LLaMA 和 GPT-NeoX 中的实现】**
> RoPE vai fazer uma consulta e um comando de rotação de um fator de rotação que varia de ângulo a posição. Para um modelo de dimensão d = 4096 ∞, a duração da sequência é L = 4096, RoPE executará L^2/2 vezes a multiplicidade de números por par (q, k). Em comparação com o código de posição absoluta, a vantagem do RoPE é que a posição em relação ao fator de rotação depende apenas da diferença de posição, o que naturalmente suporta o "output" ∞.

| Operation | Algebraic Form | Geometric Meaning |
|-----------|---------------|-------------------|
| Addition | (a+c) + (b+d)i | Vector addition in the plane |
| Multiplication | (ac-bd) + (ad+bc)i | Rotate and scale |
| Conjugate | a - bi | Reflect over real axis |
| Magnitude | sqrt(a^2 + b^2) | Distance from origin |
| Phase | atan2(b, a) | Angle from positive real axis |
| Division | multiply by conjugate | Reverse rotation and rescale |
| Power | r^n * e^(i*n*theta) | Rotate n times, scale by r^n |

```mermaid
graph LR
    subgraph "Unit Circle"
        direction TB
        U1["e^(i*0) = 1"] -.-> U2["e^(i*pi/2) = i"]
        U2 -.-> U3["e^(i*pi) = -1"]
        U3 -.-> U4["e^(i*3pi/2) = -i"]
        U4 -.-> U1
    end
    subgraph "Applications"
        A1["Euler's formula:<br/>e^(i*theta) = cos + i*sin"]
        A2["DFT uses roots of unity:<br/>e^(2*pi*i*k/N)"]
        A3["RoPE uses rotation:<br/>q * e^(i*m*theta)"]
    end
    U1 --> A1
    U1 --> A2
    U1 --> A3
```

## Construí-lo e realizei-o.
```figure
roots-of-unity
```

## Construí-lo

### Passo 1: Classe complexa

Construir uma classe de números complexos que suporta a aritmética, magnitude, fase e conversão entre formas retangulares e polares.

> Construir um grupo de números, apoiar o cálculo de operações 模、相位, bem como a transformação entre o坐标直角 e o坐标极.

```python
import math

class Complex:
    def __init__(self, real, imag=0.0):
        self.real = real
        self.imag = imag

    def __add__(self, other):
        return Complex(self.real + other.real, self.imag + other.imag)

    def __mul__(self, other):
        r = self.real * other.real - self.imag * other.imag  # 实部：(ac - bd)
        i = self.real * other.imag + self.imag * other.real  # 虚部：(ad + bc)
        return Complex(r, i)

    def __truediv__(self, other):
        denom = other.real ** 2 + other.imag ** 2            # 分母：c^2 + d^2
        r = (self.real * other.real + self.imag * other.imag) / denom  # 乘以共轭后的实部
        i = (self.imag * other.real - self.real * other.imag) / denom  # 乘以共轭后的虚部
        return Complex(r, i)

    def magnitude(self):
        return math.sqrt(self.real ** 2 + self.imag ** 2)

    def phase(self):
        return math.atan2(self.imag, self.real)

    def conjugate(self):
        return Complex(self.real, -self.imag)
```

### Passo 2: Conversão polar e fórmula de Euler

```python
def to_polar(z):
    return z.magnitude(), z.phase()

def from_polar(r, theta):
    return Complex(r * math.cos(theta), r * math.sin(theta))

def euler(theta):
    return Complex(math.cos(theta), math.sin(theta))
```

Verificar: `euler(theta).magnitude()`Deve ser sempre 1.0. `euler(0)`deve dar (1, 0). `euler(pi)`deve dar (-1, 0).

> 验证:`euler(theta).magnitude()`应始终为 1.0。`euler(0)`应给出 (1, 0)`euler(pi)`应给出 (-1, 0)

### Passo 3: rotação

Rotar um ponto (x, y) por ângulo theta é uma multiplicação complexa:

> 将点 (x, y) 旋转角度 theta 只有一次复数乘法:

```python
point = Complex(3, 4)
rotated = point * euler(math.pi / 4)
```

A magnitude permanece a mesma, só o ângulo muda.

> 模保持不变──只有角度改变──

### Passo 4: DFT da aritmética complexa

```python
def dft(signal):
    N = len(signal)                               # 信号长度
    result = []
    for k in range(N):
        total = Complex(0, 0)
        for n in range(N):
            angle = -2 * math.pi * k * n / N      # 第 k 个单位根的角度
            total = total + Complex(signal[n], 0) * euler(angle)  # 累加：信号与旋转相量的相关
        result.append(total)
    return result
```

Esta é a O(N^2) DFT. Cada saída X[k] é a soma das amostras de sinal multiplicadas por raízes de unidade.

> É o DFT de O(N^2) ⋅ cada saída X[k] ⋅ é sinal de exemplo multiplicado por unidade de raiz ⋅

### Passo 5: DFT inverso

O DFT inverso reconstrui o sinal original a partir de seu espectro. As únicas mudanças do DFT para a frente: inverte o sinal no exponente e divide por N.

> 逆 DFT 从频谱重建原始信号──与正向 DFT唯一区别:翻转指数符号并除以 N──

```python
def idft(spectrum):
    N = len(spectrum)
    result = []
    for n in range(N):
        total = Complex(0, 0)
        for k in range(N):
            angle = 2 * math.pi * k * n / N
            total = total + spectrum[k] * euler(angle)
        result.append(Complex(total.real / N, total.imag / N))
    return result
```

Aplique DFT, depois IDFT, e você retorna o sinal original à precisão da máquina.

> Isto lhe dá uma reconstrução perfeita. Aplique DFT, reaplique IDFT, você recupera o sinal original com precisão de máquina.

### Passo 6: Raízes da unidade

```python
def roots_of_unity(N):
    return [euler(2 * math.pi * k / N) for k in range(N)]
```

Verificar duas propriedades:
- Cada raiz tem magnitude exatamente 1.
  Cada raiz é de um.
- A soma de todas as raízes N é zero (eles são anulados por simetria).
  Propriedade N 个根之和为零(对称性导致相消)

Estas propriedades são o que torna o DFT invertível. As raízes da unidade formam uma base ortogonais para o domínio de frequência.

> Estes caracteres tornam a DFT contrária.

## Use-o com o framework implementado.

Python tem suporte integrado a números complexos.`j`representa a unidade imaginária.

> Python 内置复数支持──字面量 `j`Expressão de números de unidades.

```python
z = 3 + 2j
w = 1 + 4j

print(z + w)
print(z * w)
print(abs(z))

import cmath
print(cmath.phase(z))
print(cmath.exp(1j * cmath.pi))
```

Para matrizes, numpy lida com números complexos nativamente:

> Para o número, não há número original de processos:

```python
import numpy as np

z = np.array([1+2j, 3+4j, 5+6j])
print(np.abs(z))
print(np.angle(z))
print(np.conj(z))
print(np.real(z))
print(np.imag(z))

signal = np.sin(2 * np.pi * 5 * np.linspace(0, 1, 128))
spectrum = np.fft.fft(signal)
freqs = np.fft.fftfreq(128, d=1/128)
```

## Envia-o . Produto .

Corra .`code/complex_numbers.py`para gerar `outputs/skill-complex-arithmetic.md`- Não .

> 运行 `code/complex_numbers.py` 生成`outputs/skill-complex-arithmetic.md`(复数运算技能文档)

## Exercícios.

1. **Complex arithmetic by hand.**Calcule (2 + 3i) * (4 - i) e verifique com o código. Então, calcule (5 + 2i) / (1 - 3i). Desenhe ambos os resultados no plano complexo e verifique se a multiplicação girou e escalaram o primeiro número.

2. **Rotation sequence.**Comece com o ponto (1, 0). Multiplica por e^(i*pi/6) doze vezes. Verifique se você volta a (1, 0) após 12 multiplicações. Imprima as coordenadas em cada passo e confirme que eles rastream um regular de 12 gons.

3. **DFT of a known signal.**Crie um sinal que seja a soma dos sin ((2 * pi * 3 * t) e 0,5 * sin ((2 * pi * 7 * t) amostragados em 32 pontos. Exerça o seu DFT. Verifique se o espectro de magnitude tem picos em frequências 3 e 7, com o pico em 7 sendo metade da altura do pico em 3.

4. **Roots of unity visualization.**Calcule as 8a raízes da unidade. Verifique se somam a zero. Verifique se multiplicar qualquer raiz pela raiz primitiva e^(2*pi*i/8) dá a próxima raiz.

5. **Rotation matrix equivalence.**Para 10 ângulos aleatórios e 10 pontos aleatórios, verifique se a multiplicação complexa dá o mesmo resultado que a multiplicação de matriz-vector com a matriz de rotação 2x2.

## Termos-chave .

| Term | What it means |
|------|---------------|
| Complex number | A number a + bi where a is the real part, b is the imaginary part, and i^2 = -1 |
| Imaginary unit | The number i, defined by i^2 = -1. Not imaginary in the philosophical sense -- it is a rotation operator |
| Complex plane | The 2D plane where the x-axis is real and the y-axis is imaginary. Also called the Argand plane |
| Magnitude (modulus) | The distance from the origin: sqrt(a^2 + b^2). Written as \|z\| |
| Phase (argument) | The angle from the positive real axis: atan2(b, a). Written as arg(z) |
| Conjugate | The mirror image across the real axis: conjugate of a + bi is a - bi |
| Polar form | Expressing z as r * e^(i*theta) instead of a + bi. Makes multiplication easy |
| Euler's formula | e^(i*theta) = cos(theta) + i*sin(theta). Connects exponentials to trigonometry |
| Phasor | A rotating complex number e^(i*omega*t) representing a sinusoidal signal |
| Roots of unity | The N complex numbers e^(2*pi*i*k/N) for k = 0 to N-1. N equally spaced points on the unit circle |
| DFT | Discrete Fourier Transform. Decomposes a signal into complex sinusoidal components using roots of unity |
| RoPE | Rotary Position Embedding. Uses complex multiplication to encode relative position in transformer attention |

> 术语速查:número complexo(复数 a+bi)、Unidade imaginária(虚数单位 i,旋转算子)、 plano complexo(复平面)、Magnitudo/módulo(模 √(a2+b2))、Fase/argumento(相位 atan2(b,a))、Conjugate(共 a-bi)、Polar forma(极坐标 r·e^(iθ、)) 欧拉公式 e^(iθ)=θ+i·sinθ)、Phasor(旋转相量)、Redes da unidade N 个均分单位圆的点)、DFT散离里叶变换)、Rocos 转位置编码,L(Laos 模型使用)

## Mais leitura 延伸阅读

- [Visual Introduction to Euler's Formula](https://betterexplained.com/articles/intuitive-understanding-of-eulers-formula/)- construi intuição geométrica sem notação pesada
- [Su et al.: RoFormer (2021)](https://arxiv.org/abs/2104.09864)- o papel que introduz a rotativa de posições de inserção com rotações complexas
- [Vaswani et al.: Attention Is All You Need (2017)](https://arxiv.org/abs/1706.03762)- o papel transformador original com codificações posicionais sinusoidais
- [3Blue1Brown: Euler's formula with introductory group theory](https://www.youtube.com/watch?v=mvmuCPvRoWQ)- explicação visual do porquê de e^(i*pi) = -1
- [Needham: Visual Complex Analysis](https://global.oup.com/academic/product/visual-complex-analysis-9780198534464)- o melhor tratamento visual de números complexos, cheio de conhecimentos geométricos
- [Strang: Introduction to Linear Algebra, Ch. 10](https://math.mit.edu/~gs/linearalgebra/)- números complexos no contexto da álgebra linear e dos valores próprios
