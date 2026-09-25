# O Fourier Transform.

> Cada sinal é uma soma de ondas sinusais.
> Cada sinal é um sinal de um sinal de um sinal.

**Type:** Build | **类型:** 动手
**Language:**O Python .**语言:**Python
**Prerequisites:** Phase 1, Lessons 01-04, 19 (complex numbers) | **前置知识:** Phase 1, 第 01-04 课、第 19 课（复数）
**Time:** ~90 minutes | **时间:** ~90 分钟

## Objetivos de aprendizagem

- Implementar o DFT a partir do zero e verificá-lo contra o O(N log N) Cooley-Tukey FFT
  Desde zero a realização de DFT e não com O(N log N) de Cooley-Tukey FFT 验证
- Interpreta os coeficientes de frequência: extrair amplitude, fase e espectro de potência de um sinal
  解释频率系数:从信号中提取幅度、相位和功率谱(O Espectro de Potência)
- Aplicar o teorema de convolução para realizar convolução através da multiplicação FFT
   aplicando o processo de determinação através da FFT 乘法执行卷积
- Conectar a decomposição de frequência de Fourier para transformar codificadores posicionais e camadas de convolução CNN
  A partir de agora, a rede de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de


> **【中文解读】**
> Qualquer sinal pode ser dividido em um sinal de freqüência. O processamento de freqüência pode ser dividido em um sinal de freqüência.

## O problema é o problema da introdução

Uma gravação de áudio é uma sequência de medições de pressão ao longo do tempo. Um preço de ação é uma sequência de valores ao longo de dias. Uma imagem é uma grade de intensidades de pixels sobre o espaço. Todos estes são dados no domínio do tempo (ou domínio do espaço). Você vê valores mudando em algum índice.

> 音频录制是随时变化的压力测量序列――股票价格是随天数变化的值序列――图像是空间上像素强度的网格――这些都是时域 (或空域) 的数据――你看到的是某索引上变化的值――

Mas muitos padrões são invisíveis no domínio do tempo. Este sinal de áudio é um tom puro ou um acorde? Este preço das ações tem um ciclo semanal? Esta imagem tem uma textura repetitiva? Estas perguntas são sobre o conteúdo de frequência, e o domínio do tempo o oculta.

> Mas muitos padrões são invisíveis no tempo. Este sinal de som é puro ou sincronizado?

A transformação de Fourier converte dados do domínio do tempo para o domínio da frequência. Ele pega um sinal e o decompõe em ondas sinusais de diferentes frequências. Cada onda sinusa tem uma amplitude (quão forte é) e uma fase (onde começa).

> 里叶变换将数据从时域转换到频域――它收取一个信号并将其分解成不同频率的正弦波――每个正弦波有幅度(有多强) 和相位(从哪里开始)―里叶变换告诉你两者──

Isto é importante para a ML porque o pensamento do domínio de frequência aparece em todos os lugares. As redes neurais convolucionais executam convolução, que é multiplicação no domínio de frequência. Os codificadores posicionais transformadores usam a decomposição de frequência para representar a posição. Os modelos de áudio (reconhecimento de fala, geração de música) operam em espectrogramas - representações de frequência do som. Os modelos de séries temporais procuram padrões periódicos. Entender a transformação de Fourier dá-lhe o vocabulário para trabalhar com todos estes.

> Isto é importante para o ML, porque o frequência de pensamento não está presente. O volume de execução da rede de neurônios é multiplicado.

## O conceito central.

> **【中文解读】**
> 里叶变换的核心思想: qualquer sinal pode ser dividido em diferentes frequências de ossinos de onda e de.DFT Colocar o sinal de tempo em frequência frequência  cada frequência diz-lhe "esta frequência tem muita energia"― isto é como o espelho que divide a luz branca em rainho: o tempo em que o domínio vê é um sinal misturado, o frequência em que o campo vê os componentes―

> **【拓展：FFT 的计算影响力】**
> O FFT é considerado um dos algoritmos de valores numéricos mais importantes do século XX. Gauss descobriu a estratégia de divisão em 1805, mas Cooley-Tukey em seu trabalho de 1965 apenas fez com que o FFT fosse amplamente aplicado. Hoje em dia, cada vez que o 4G / LTE 通话、 cada张 JPEG 照片、 cada canção de MP3 foi processada por FFT.

### A definição de DFT

Dadas as amostras N x[0], x[1], ..., x[N-1], a Transforma de Fourier Discreta produz N coeficientes de frequência X[0], X[1], ..., X[N-1]:

> 给定 N 个样本 x[0], x[1], ..., x[N-1],离散里叶变换产生 N 个频率系数 X[0], X[1], ..., X[N-1]:

```
X[k] = sum_{n=0}^{N-1} x[n] * e^(-2*pi*i*k*n/N)

for k = 0, 1, ..., N-1
```

Cada X [k] é um número complexo. Sua magnitude. X [k] que lhe diz a amplitude da frequência k. Seu ângulo de fase ((X [k]) diz-lhe o offset de fase dessa frequência.

> Cada X[k] é o número de vezes.

A principal ideia:`e^(-2*pi*i*k*n/N)`O DFT calcula a correlação entre o sinal e cada uma das frequências de espaço igual N. Se o sinal contém energia na frequência k, a correlação é grande.

> 关键洞察:`e^(-2*pi*i*k*n/N)`É a frequência para a quantidade de rotação de k.

### O que significa cada coeficiente

**X[0]: the DC component.**Esta é a soma de todas as amostras -- proporcional à média. Representa a constante (frequência zero) de compensação do sinal.

> **X[0]：直流分量（DC Component）。**É a proporção total de todas as amostras e o valor médio em proporção.

```
X[0] = sum_{n=0}^{N-1} x[n] * e^0 = sum of all samples
```

**X[k] for 1 <= k <= N/2: positive frequencies.**X[k] representa os ciclos de frequência k por amostras N. A frequência mais alta k significa frequência mais alta (oscillação mais rápida).

> **X[k]（1 <= k <= N/2）：正频率。**X[k] 代表每 N 个样本中 k 个周期的频率──k 越大频率越高(振荡越快)──

**X[N/2]: the Nyquist frequency.**A maior frequência que podemos representar com amostras N. acima disso, obtemos aliasing -- frequências altas mascaradas como baixas.

> **X[N/2]：Nyquist 频率。**Utilize N 个样本能表示的最高频率──超过此频率会产生混叠高频伪装成低频──

**X[k] for N/2 < k < N: negative frequencies.**Para sinais de valor real, X[N-k] = conj(X[k]). As frequências negativas são imagens espelhadas das positivas. É por isso que a informação útil está nos primeiros coeficientes N/2 + 1.

> **X[k]（N/2 < k < N）：负频率。**对于实值信号,X[N-k] = conj(X[k])。负频率是正频率的镜像──这就是为什么有用信息在前N/2 + 1 系数中──

### DFT inverso

O DFT inverso reconstitui o sinal original a partir dos seus coeficientes de frequência:

```
x[n] = (1/N) * sum_{k=0}^{N-1} X[k] * e^(2*pi*i*k*n/N)

for n = 0, 1, ..., N-1
```

As únicas diferenças do DFT para frente: o sinal no exponente é positivo (não negativo), e há um fator de normalização 1/N.

> Com a direita DFT, a única diferença é que o símbolo da função é positivo (non negativo), e que tem um factor de redução de 1/N.

O DFT inverso é uma reconstrução perfeita. Não há informação perdida. Você pode ir de domínio de tempo para domínio de frequência e de volta sem qualquer erro. O DFT é uma mudança de base - ele reexprime a mesma informação em um sistema de coordenadas diferente.

> Ao contrário, o DFT é uma reconstrução perfeita. Não há perda de informação. Você pode voltar de um domínio temporal para outro, sem qualquer erro.

### A FFT: a acelerar

O DFT definido acima é O ((N^2): para cada um dos coeficientes de saída N, você soma sobre amostras de entrada N. Para N = 1 milhão, isto é 10^12 operações.

> Para N = 100.000.000, é 10^12 vezes de cálculo.

A Transforma de Fourier Rápida (FFT) calcula o mesmo resultado em O  N log N. Para N = 1 milhão, isso é cerca de 20 milhões de operações em vez de um trilhão.

> 快速里叶变换(FFT) com O(N log N) 计算相同的结果──对于N = 100 万,大约是2000 万次运算而不是10亿次──这就是使频率分析变得可行的原因──

> **【中文解读】**
> A quantidade de cálculo do DFT é O(N^2), mas o FFT 通过分治策略把它降至O(N log N) ⋅对于N=100.000信号,DFT 需要万亿次运算,FFT 需要约2000.000次加速5万倍!秘是把信号按奇偶下标分成两半,递归计算后再使用"旋转因子"合并──这要求信号长度是2的──

O algoritmo Cooley-Tukey (o FFT mais comum) funciona dividindo e conquistando:

> Cooley-Tukey 算法 (FFT) ️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️

1. Dividir o sinal em amostras indexadas e paradas.
   A partir de agora, o sistema de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de
2. Calcule o DFT de cada metade de forma recorrente.
   递归计算每一半的DFT──
3. Combinar as duas DFTs de meia dimensão usando "fatores de dupla" e^(-2*pi*i*k/N).
   Utilize "旋转因子" (twiddle factor) e^(-2*pi*i*k/N) 合并两个半尺寸的DFT──

```
X[k] = E[k] + e^(-2*pi*i*k/N) * O[k]          for k = 0, ..., N/2 - 1
X[k + N/2] = E[k] - e^(-2*pi*i*k/N) * O[k]    for k = 0, ..., N/2 - 1

where E = DFT of even-indexed samples
      O = DFT of odd-indexed samples
```

A simetria significa que cada nível de recursão faz O(N) funcionar, e há níveis log2(N).

> 对称性 significa cada nível de regresso fazer O (N) 工作,共有 log2 (N) 层――总计:O (N) log N)。

```mermaid
graph TD
    subgraph "8-point FFT (Cooley-Tukey)"
        X["x[0..7]<br/>8 samples"] -->|"split even/odd"| E["Even: x[0,2,4,6]"]
        X -->|"split even/odd"| O["Odd: x[1,3,5,7]"]
        E -->|"4-pt FFT"| EK["E[0..3]"]
        O -->|"4-pt FFT"| OK["O[0..3]"]
        EK -->|"combine with twiddle factors"| XK["X[0..7]"]
        OK -->|"combine with twiddle factors"| XK
    end
    subgraph "Complexity"
        C1["DFT: O(N^2) = 64 multiplications"]
        C2["FFT: O(N log N) = 24 multiplications"]
    end
```

O FFT exige que o comprimento do sinal seja de 2 potências. Na prática, os sinais são empurrados a zero para a próxima potência de 2.

### Análise espectral

O **power spectrum**É X [k]^2 - a magnitude quadrada de cada coeficiente de frequência.

O **phase spectrum**é ângulo ((X[k]) -- o offset de fase de cada frequência. Para a maioria das tarefas de análise, você se importa com o espectro de potência e ignora a fase.

```
Power at frequency k:  P[k] = |X[k]|^2 = X[k].real^2 + X[k].imag^2
Phase at frequency k:  phi[k] = atan2(X[k].imag, X[k].real)
```

### Resolução de frequência

A resolução de frequência do DFT depende do número de amostras N e da taxa de amostragem fs.

```
Frequency of bin k:      f_k = k * fs / N
Frequency resolution:    delta_f = fs / N
Maximum frequency:       f_max = fs / 2  (Nyquist)
```

Para resolver duas frequências próximas, é preciso mais amostras. Para capturar frequências altas, é preciso uma taxa de amostragem mais alta.

### O teorema da convolução

Este é um dos resultados mais importantes no processamento de sinais e diretamente relevante para as emissoras de televisão.

> Este é um dos resultados mais importantes no processamento de sinais, diretamente relacionado à CNN.

**Convolution in the time domain equals pointwise multiplication in the frequency domain.**

> **时域中的卷积等于频域中的逐点相乘。**

```
x * h = IFFT(FFT(x) . FFT(h))

where * is convolution and . is element-wise multiplication
```

Por que isso importa:

- A convolução direta de dois sinais de comprimento N e M realiza operações O(N*M).
  两个长度为 N 和 M 的信号直接卷积需要 O(N*M) 次运算──
- A convolução baseada em FFT toma O(N log N): transforma ambos, multiplica, transforma de volta.
  Baseada em FFT, o volume requer O  N log N: 变换两个信号、相乘、逆变换。
- Para núcleos grandes, a convolução FFT é dramaticamente mais rápida.
  Para o grande volume, o FFT 卷积快得多──
- É exatamente o que acontece nas camadas convolucionais com grandes campos receptivos.
  É o que acontece na área de volume com grande sensação.

> **【拓展：卷积定理在 CNN 中的实际应用】**
>                                                                                                                                                                                                                                                               

Nota: o DFT calcula a convulsão circular (o sinal envolve-se). Para a convulsão linear (sem envolvimento), pad zero ambos os sinais para comprimento N + M - 1 antes da computação.

> Nota:DFT  calcular é ciclo de volumes (→ M + M - 1) ⋅

```mermaid
graph LR
    subgraph "Time Domain"
        TA["Signal x[n]"] -->|"convolve (slow: O(NM))"| TC["Output y[n]"]
        TB["Filter h[n]"] -->|"convolve"| TC
    end
    subgraph "Frequency Domain"
        FA["FFT(x)"] -->|"multiply (fast: O(N))"| FC["FFT(x) * FFT(h)"]
        FB["FFT(h)"] -->|"multiply"| FC
        FC -->|"IFFT"| FD["y[n]"]
    end
    TA -.->|"FFT"| FA
    TB -.->|"FFT"| FB
    FD -.->|"same result"| TC
```

### Janela

O DFT assume que o sinal é periódico - trata as amostras N como um período de um sinal infinitamente repetitivo. Se o sinal não começar e terminar no mesmo valor, isso cria uma descontinuidade na fronteira, que aparece como conteúdo de alta frequência falso.

> DFT 假设信号是周期的它将N个样本视为无限重复信号的一个周期――如果信号不存在相同的值处开始和结束,边界处会产生不连续性,表现为虚假的高频内容――这称为频谱泄漏(Spectral Leakage) ――

A janela reduz a fuga diminuindo o sinal para zero em ambas as extremidades antes de calcular o DFT.

> 窗函数 (window) 通过在计算 DFT 之前将信号两端逐渐衰减到零来减少泄漏──

Janela comum:

| Window | Shape | Main lobe width | Side lobe level | Use case |
|--------|-------|----------------|-----------------|----------|
| Rectangular | Flat (no window) | Narrowest | Highest (-13 dB) | When signal is exactly periodic in N samples |
| Hann | Raised cosine | Moderate | Low (-31 dB) | General purpose spectral analysis |
| Hamming | Modified cosine | Moderate | Lower (-42 dB) | Audio processing, speech analysis |
| Blackman | Triple cosine | Wide | Very low (-58 dB) | When side lobe suppression is critical |

```
Hann window:    w[n] = 0.5 * (1 - cos(2*pi*n / (N-1)))
Hamming window: w[n] = 0.54 - 0.46 * cos(2*pi*n / (N-1))
```

Aplicar a janela multiplicando-a por elemento com o sinal antes do DFT: `X = DFT(x * w)`- Não .

### Propriedades DFT

| Property | Time Domain | Frequency Domain |
|----------|-------------|-----------------|
| Linearity | a*x + b*y | a*X + b*Y |
| Time shift | x[n - k] | X[f] * e^(-2*pi*i*f*k/N) |
| Frequency shift | x[n] * e^(2*pi*i*f0*n/N) | X[f - f0] |
| Convolution | x * h | X * H (pointwise) |
| Multiplication | x * h (pointwise) | X * H (circular convolution, scaled by 1/N) |
| Parseval's theorem | sum \|x[n]\|^2 | (1/N) * sum \|X[k]\|^2 |
| Conjugate symmetry (real input) | x[n] real | X[k] = conj(X[N-k]) |

O teorema de Parseval diz que a energia total é a mesma em ambos os domínios.

> Parseval 定理说明 两个域中的总能量相同.

### Conexão a codificações posicionais

O Transformer original usa codificações posicionais sinusoidais:

```
PE(pos, 2i)   = sin(pos / 10000^(2i/d_model))
PE(pos, 2i+1) = cos(pos / 10000^(2i/d_model))
```

Cada par de dimensões (2i, 2i+1) oscila em uma frequência diferente. As frequências são espaçadas geométricamente de alta (dimensão 0,1) para baixa (última dimensão). Isso dá a cada posição um padrão único em todas as bandas de frequência - semelhante à forma como os coeficientes de Fourier identificam um sinal de forma única.

> Cada dimensão (2i, 2i+1) tem diferentes frequências de oscilação. A frequência de alta (dimensão 0,1) a baixa (dimensão final) apresenta vários intervalos.

As principais propriedades que isto fornece:

- **Uniqueness:**Não há duas posições com a mesma codificação.
  **唯一性：**Não há duas posições com o mesmo código.
- **Bounded values:**O pecado e o cos estão sempre em [-1, 1].
  **有界值：**Sin 和 cos 始终在 [-1, 1] 中──
- **Relative position:**A codificação da posição p+k pode ser expressa como uma função linear da codificação na posição p. O modelo pode aprender a atender a posições relativas.
  **相对位置：**位置 p+k 编码可以表示为位置 p 编码的线性函数──模型可以学习关注相对位置──

### Conexão com as CNNs

Uma camada de convolução aplica um filtro aprendido (núcleo) à entrada deslizando-o através do sinal ou imagem.

> 卷积层通过在信号或图像上滑学习的波器 (卷积核) é aplicado à entrada.

Pelo teorema da convolução, isto é equivalente a:
1. FFT a entrada
   FFT 输入
2. FFT o núcleo
   FFT 卷积核
3. Multiplicar no domínio de frequência
   Em frequência
4. Se o resultado for
   IFFT  resultados

As implementações padrão da CNN usam convolução direta (mais rápida para pequenos kernels 3x3). Mas para kernels grandes ou convolução global, as abordagens baseadas em FFT são significativamente mais rápidas. Algumas arquiteturas (como FNet) substituem a atenção inteiramente por FFT, alcançando precisão competitiva com O(N log N) em vez de complexidade O(N^2).

> 标准 CNN 实现使用直接卷积 (小的3x3卷积核更快) ⋅但对于大卷积核或全局卷积,基于FFT的方法显著更快──一些架构 (如 FNet) 完全使用FFT 替代注意力,以O(N log N) 而非O(N^2) 的复杂性达到竞争精度──

### Espectogramas e a Transforma Fourier de Curto Tempo

Um único FFT dá-lhe o conteúdo de frequência de todo o sinal, mas não lhe diz nada sobre quando essas frequências ocorrem.

> 单次 FFT 给你整个信号的频率内容,但不告诉你这些频率在什么时候出现──信号频率随时间增加的信号) 和和弦频率同时出现) pode ter a mesma amplitude谱──

A Transformação de Fourier de Tempo Curto (STFT) resolve isso computação de FFTs em janelas sobrepostas do sinal. O resultado é um espectrograma: uma representação 2D com tempo em um eixo e frequência no outro. A intensidade em cada ponto mostra a energia na frequência naquele momento.

> 短时里叶变换(STFT) através da calculação de FFT na janela de sobreposição do sinal para resolver este problema. O resultado é o gráfico de freqüência: uma em tempo para um eixo, a frequência para outro eixo.

```
STFT procedure:
1. Choose a window size (e.g., 1024 samples)
2. Choose a hop size (e.g., 256 samples -- 75% overlap)
3. For each window position:
   a. Extract the windowed segment
   b. Apply a Hann/Hamming window
   c. Compute FFT
   d. Store the magnitude spectrum as one column of the spectrogram
```

Os espectrogramas são a representação padrão de entrada para modelos de áudio ML. Os modelos de reconhecimento de fala (Whisper, DeepSpeech) operam em espectrogramas mel - espectrogramas com frequências mapeadas na escala mel, que melhor se encaixa na percepção de pitch humana.

> 频谱图是音频 ML 模型的标准输入表示──语音识别模型──Whisper、DeepSpeech) operação 频率映射到梅尔刻度的频谱图, melhor se adequar ao som humano.

> **【中文解读】**
>  Single FFT só pode ver a componente de frequência de todo o sinal, mas não sabe cada frequência em "quando" aparece.短时里叶变换STFT) através da janela de esboço resolveu este problema: fazer FFT por separado em cada segmento da janela, obter três dimensões de tempo-frequência-energia.

### Aliasing

Se um sinal contém frequências acima de fs/2 (a frequência de Nyquist), a amostragem a taxa fs criará cópias alias. Um sinal de 90 Hz amostragado a 100 Hz parece idêntico a um sinal de 10 Hz. Não há forma de distinguir-los das amostras sozinhas.

> Se o sinal contém uma frequência superior a fs/2 (frequência de Nyquist), a taxa de fs 采样会产生混混副――90 Hz 信号以 100 Hz 采样看起来与 10 Hz 信号相同――仅从样本无法区分它们――

```
Example:
  True signal: 90 Hz sine wave
  Sampling rate: 100 Hz
  Apparent frequency: 100 - 90 = 10 Hz

  The samples from the 90 Hz signal at 100 Hz sampling rate
  are identical to the samples from a 10 Hz signal.
  No amount of math can recover the original 90 Hz.
```

É por isso que os conversores analógicos para digitais incluem filtros anti-aliasing que removem as frequências acima de Nyquist antes da amostragem.

> É por isso que os transformadores de módulos contêm os transmissores de ondas anti-confusação, que são removidos com frequência superior à de Nyquist antes da tomada de amostras.

### A colcha zero não aumenta a resolução

Um equívoco comum: empolgar um sinal antes de FFT melhora a resolução de frequência. Não. O empolgar zero interpola entre os recipientes de frequência existentes, dando-lhe um espectro mais liso. Mas não pode revelar detalhes de frequência que não estavam presentes nas amostras originais.

> 常见误解: antes de FFT 补零可以提高频率分辨率──实际上不能──补零在现有频率bin 之间插值,给你一个更平滑的频谱外观──但它不能揭露原始样本中不存在的频率细节──

A resolução de frequência verdadeira depende apenas do tempo de observação T = N / fs. Para resolver duas frequências separadas por delta_f, você precisa de pelo menos T = 1 / delta_f segundos de dados. Nenhuma quantidade de empate zero altera esse limite fundamental.

> A resolução da frequência real depende apenas do tempo de observação T = N / fs──para distinguir as duas frequências de delta_f, pelo menos precisa de dados de T = 1 / delta_f 秒──para mais adição também não é possível alterar esta limitação básica──

> **【拓展：频谱图在语音 AI 中的标准地位】**
> O modelo OpenAI Whisper irá transformar o som em log-Mel 频谱图后输入编码器──Mel 刻度模拟人耳对频率的感知(低频区分更细)──Whisper utiliza 80 个 Mel 波器组、25ms 窗口、10ms 步长──一段 30 秒的音频产生约3000 x 80 的频谱图阵──Google WaveNet、Meta's EnCodec também são utilizados para expressão de características intermédia──

## Construí-lo e realizei-o.
```figure
fourier-synthesis
```

## Construí-lo

### Passo 1: DFT a partir do zero

O O ((N^2) DFT segue directamente da definição.

```python
import math

class Complex:
    ...

def dft(x):
    N = len(x)
    result = []
    for k in range(N):
        total = Complex(0, 0)
        for n in range(N):
            angle = -2 * math.pi * k * n / N
            w = Complex(math.cos(angle), math.sin(angle))
            xn = x[n] if isinstance(x[n], Complex) else Complex(x[n])
            total = total + xn * w
        result.append(total)
    return result
```

### Passo 2: DFT inverso

A mesma estrutura, exponente positivo, dividido por N.

```python
def idft(X):
    N = len(X)
    result = []
    for n in range(N):
        total = Complex(0, 0)
        for k in range(N):
            angle = 2 * math.pi * k * n / N
            w = Complex(math.cos(angle), math.sin(angle))
            total = total + X[k] * w
        result.append(Complex(total.real / N, total.imag / N))
    return result
```

### Passo 3: FFT (Cooley-Tukey)

O FFT recorrente requer poder de 2 comprimento. Dividido em par e ímpar, recorrente, combinar com fatores de torcida.

```python
def fft(x):
    N = len(x)
    if N <= 1:                                      # 基础情况：长度 1 的 DFT 就是自身
        return [x[0] if isinstance(x[0], Complex) else Complex(x[0])]
    if N % 2 != 0:                                  # 非偶数长度，回退到普通 DFT
        return dft(x)

    even = fft([x[i] for i in range(0, N, 2)])     # 递归：偶数下标子序列
    odd = fft([x[i] for i in range(1, N, 2)])      # 递归：奇数下标子序列

    result = [Complex(0)] * N
    for k in range(N // 2):
        angle = -2 * math.pi * k / N                # 旋转因子角度
        twiddle = Complex(math.cos(angle), math.sin(angle))  # 旋转因子 e^(-2piik/N)
        t = twiddle * odd[k]                        # 蝶形运算：旋转后的奇数部分
        result[k] = even[k] + t                    # 前半：E[k] + twiddle * O[k]
        result[k + N // 2] = even[k] - t           # 后半：E[k] - twiddle * O[k]
    return result
```

### Passo 4: Auxiliares de análise espectral

```python
def power_spectrum(X):
    return [xk.real ** 2 + xk.imag ** 2 for xk in X]

def convolve_fft(x, h):
    N = len(x) + len(h) - 1                         # 线性卷积的输出长度
    padded_N = 1
    while padded_N < N:
        padded_N *= 2                                # 补零到 2 的幂次

    x_padded = x + [0.0] * (padded_N - len(x))      # 补零避免循环卷积混叠
    h_padded = h + [0.0] * (padded_N - len(h))

    X = fft(x_padded)                               # 信号 FFT
    H = fft(h_padded)                               # 滤波器 FFT

    Y = [xk * hk for xk, hk in zip(X, H)]          # 频域逐点相乘（卷积定理）

    y = idft(Y)                                     # 逆 FFT 回到时域
    return [y[n].real for n in range(N)]
```

## Use-o com o framework implementado.

Para o trabalho real, use o FFT da numpy, que é apoiado por bibliotecas C altamente otimizadas.

```python
import numpy as np

signal = np.sin(2 * np.pi * 5 * np.arange(256) / 256)
spectrum = np.fft.fft(signal)
freqs = np.fft.fftfreq(256, d=1/256)

power = np.abs(spectrum) ** 2

positive_freqs = freqs[:len(freqs)//2]
positive_power = power[:len(power)//2]
```

Para análise espectral mais avançada e para análise de janelas:

```python
from scipy.signal import windows, stft

window = windows.hann(256)
windowed = signal * window
spectrum = np.fft.fft(windowed)
```

Para convulsão:

```python
from scipy.signal import fftconvolve

result = fftconvolve(signal, kernel, mode='full')
```

Para os espectrogramas:

```python
from scipy.signal import stft

frequencies, times, Zxx = stft(signal, fs=sample_rate, nperseg=256)
spectrogram = np.abs(Zxx) ** 2
```

A matriz do espectrograma tem forma (n_frequências, n_time_frames). Cada coluna é o espectro de potência em uma janela de tempo.

> 频谱图矩阵形状是 (n_frequências, n_time_frames) ⋅ cada linha é um tempo de janela ⋅ é o seu modo de entrada ⋅

## Envia-o . Produto .

Corra .`code/fourier.py`para gerar `outputs/prompt-spectral-analyzer.md`- Não .

> 运行 `code/fourier.py` 生成`outputs/prompt-spectral-analyzer.md`(频谱分析器提示词)

## Exercícios.

1. **Pure tone identification.**Crie um sinal com uma única onda sinusal em uma freqüência desconhecida (entre 1 e 50 Hz), amostragem a 128 Hz por 1 segundo. Use o seu DFT para identificar a frequência. Verifique as correspondências da resposta. Agora adicione ruído gaussiano com desvio padrão 0,5 e repita. Como o ruído afeta o espectro?

2. **FFT vs DFT verification.**Gerar um sinal aleatório de comprimento 64. Calcule tanto DFT (O(N^2)) quanto FFT. Verifique se todos os coeficientes correspondem a dentro de 1e-10. Tempo ambas as funções em sinais de comprimento 256, 512, 1024, e 2048.

3. **Convolution theorem proof by example.**Crie o sinal x = [1, 2, 3, 4, 0, 0, 0, 0] e filtre h = [1, 1, 1, 0, 0, 0, 0, 0]. Calcule sua convolução circular diretamente (loop aninhado). Em seguida, compute-o através de FFT (transformação, multiplicação, transformação inversa). Verifique a correspondência dos resultados. Agora, faça a convolução linear com pad zero apropriadamente.

4. **Windowing effects.**Crie um sinal que seja a soma de duas ondas sinusais a 10 Hz e 12 Hz (muito perto). Mostre a 128 Hz por 1 segundo. Calcule o espectro de potência sem janela, janela Hann e janela Hamming. Qual janela torna mais fácil distinguir os dois picos? Por quê?

5. **Positional encoding analysis.**Gerar as codificações posicionais sinusoidais para d_model = 128 e max_pos = 512. Para cada par de posições (p1, p2), calcular o produto de pontos de suas codificações. Mostrar que o produto de pontos depende apenas de p1 - p2, não das posições absolutas. O que acontece com o produto de pontos à medida que a distância aumenta?

## Termos-chave .

| Term | What it means |
|------|---------------|
| DFT (Discrete Fourier Transform) | Converts N time-domain samples into N frequency-domain coefficients. Each coefficient is the correlation with a complex sinusoid at that frequency |
| FFT (Fast Fourier Transform) | An O(N log N) algorithm to compute the DFT. The Cooley-Tukey algorithm splits even/odd indices recursively |
| Inverse DFT | Reconstructs the time-domain signal from frequency coefficients. Same formula as DFT with flipped exponent sign and 1/N scaling |
| Frequency bin | Each index k in the DFT output represents frequency k*fs/N Hz. The "bin" is the discrete frequency slot |
| DC component | X[0], the zero-frequency coefficient. Proportional to the signal mean |
| Nyquist frequency | fs/2, the maximum frequency representable at sampling rate fs. Frequencies above this alias |
| Power spectrum | \|X[k]\|^2, the squared magnitude of each frequency coefficient. Shows energy distribution across frequencies |
| Phase spectrum | angle(X[k]), the phase offset of each frequency component. Often ignored in analysis |
| Spectral leakage | Spurious frequency content caused by treating a non-periodic signal as periodic. Reduced by windowing |
| Window function | A tapering function (Hann, Hamming, Blackman) applied before DFT to reduce spectral leakage |
| Twiddle factor | The complex exponential e^(-2*pi*i*k/N) used to combine sub-DFTs in the FFT butterfly computation |
| Convolution theorem | Convolution in time domain equals pointwise multiplication in frequency domain. Fundamental to signal processing and CNNs |
| Circular convolution | Convolution where the signal wraps around. This is what the DFT naturally computes |
| Linear convolution | Standard convolution without wraparound. Achieved by zero-padding before DFT |
| Parseval's theorem | Total energy is preserved through the Fourier transform. sum \|x[n]\|^2 = (1/N) sum \|X[k]\|^2 |
| Aliasing | When frequencies above Nyquist appear as lower frequencies due to insufficient sampling rate |

> 术语速查:DFT(离散里叶变换)、FFT(快速里叶变换 O(N log N))、Inversos DFT(逆 DFT)、Frequency bin (频率槽) 、DC componente(直流分量 X[0])、Nyquist freqüência(奈奎斯特频率 fs/2)、Power spectrum(功率谱X[k]2)、Phase spectrum(相位谱)、Spectral leakage(频谱泄漏)、Window function function function function function (Funkção de janela/Hamming)、Twiddle factor (Twiddle factor) ]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]

## Mais leitura 延伸阅读

- [Cooley & Tukey: An Algorithm for the Machine Calculation of Complex Fourier Series (1965)](https://www.ams.org/journals/mcom/1965-19-090/S0025-5718-1965-0178586-1/)- o papel original da FFT que mudou a computação
- [3Blue1Brown: But what is the Fourier Transform?](https://www.youtube.com/watch?v=spUNpyF58BY)- a melhor introdução visual às transformações de Fourier
- [Lee-Thorp et al.: FNet: Mixing Tokens with Fourier Transforms (2021)](https://arxiv.org/abs/2105.03824)- substitui a auto-atenção pela FFT nos transformadores
- [Smith: The Scientist and Engineer's Guide to Digital Signal Processing](http://www.dspguide.com/)- livro de texto online gratuito que abrange em profundidade a FFT, a análise das janelas e os espectros
- [Vaswani et al.: Attention Is All You Need (2017)](https://arxiv.org/abs/1706.03762)- codificadores posicionais sinusoidais derivados da decomposição de frequência de Fourier
- [Radford et al.: Whisper (2022)](https://arxiv.org/abs/2212.04356)- reconhecimento de voz utilizando espectrogramas mel como representação de entrada
