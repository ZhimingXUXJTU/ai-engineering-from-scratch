# Evaluación  FID, CLIP Score, Preferencia humana   evaluación indicador  FID  CLIP Score y preferencias humanas

> Cada tabla de clasificación de modelos generacionales cita el FID, el puntaje CLIP y una tasa de ganancias de una arena de preferencia humana. Cada número tiene un modo de fracaso que un investigador determinado puede jugar. Si no conoces los modos de fracaso, no puedes saber una mejora real de una carrera de juego.

> **【中文解读】**Cada uno de los modelos de generación en la clasificación se refiere a FID (Fréchet Inception Distance) ∙ CLIP Score 和人类偏好胜率── cada uno de los indicadores tiene una falla que puede ser borrada── no se entiende estas faltas, no se puede distinguir entre mejoras reales y la falta de la lista──

> **【拓展：FID 的局限性】**FID mide la distancia de distribución entre la imagen generada y la imagen real, pero puede ser optimizada (como la selección de imágenes).

**Type:** Build / 构建型 | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 8 · 01 (Taxonomy / 分类), Phase 2 · 04 (Evaluation Metrics / 评估指标) | **前置知识:** 阶段 8 · 01（分类），阶段 2 · 04（评估指标）
**Time:** ~45 minutes | **预计用时:** ~45 分钟

## El problema es la introducción del problema

Un modelo generativo se juzga por *la calidad de la muestra* y *la adhesión de los condicionamientos*. Ninguno de ellos tiene una medida de forma cerrada. Su modelo tiene que renderizar 10.000 imágenes; algo tiene que asignarles números; usted tiene que confiar en los números a través de las familias de modelos, a través de resoluciones, a través de arquitecturas. Tres métricas sobrevivieron al guante 2014-2026.

> El modelo de producción tiene que tener 10000 imágenes; tiene que tener algo que darles un hueco. Tres indicadores han pasado el examen 2014-2026.

- **FID (Fréchet Inception Distance).**La distancia entre dos distribuciones  reales y generadas  en el espacio de características de una red de inicio.
  **FID。**Verdad y generación distribuidos en Inception 网络特征空间中的距离──越低越好──
- **CLIP score.**Cosiña similaridad entre la incorporación de imagen CLIP de una imagen generada y la incorporación de texto CLIP de un prompt.
  **CLIP Score。**Clip de imágenes y texto de texto de la Clip 嵌入余弦相似度──越高越好──
- **Human preference.**Ponte dos modelos cara a cara en el mismo prompt, que los humanos (o un modelo de clase GPT-4) elijan el mejor, agregado a una puntuación Elo.
  **人类偏好。**Dos modelos de cabeza contra cabeza, humanos o GPT-4 级模型选择更好,聚合为 Elo 分数──

También verá: IS (puntuación de inicio, en gran parte retirado), KID, CMMD, ImageReward, PickScore, HPSv2, MJHQ-30k. Cada uno corrige por un fallo del anterior.

> También verás: IS(Ya está en marcha) ✓ Kid、CMMD、ImageReward、PickScore、HPSv2 etc.

> **【中文解读】**Los tres principales indicadores de evaluación de modelos de producción: 1) FID en el espacio de características de la red de inicio para medir la distancia entre la distribución de generación y la distribución real, cada vez más baja; 2) CLIP Score para generar imágenes y la concordancia de la definición de texto de los textos, cada vez más alta; 3) Prefierancia de la gente para dos modelos en comparación con la selección mejor, agrupados en Elo por un número de partes.

> **【拓展：生成模型评估的"刷榜"问题】**FID puede ser optimizado a través de la selección de la generación de alta porción de muestras, ajuste de la creación de la capa de características del modelo o de la adaptación a la distribución de referencia. CLIP Score también tiene un parámetro. CLIP modelo es más sensible a ciertos conceptos.

## El concepto central.

![FID, CLIP, and preference: three axes, different failure modes](../assets/evaluation.svg)

### La calidad de la muestra es de la calidad de la muestra.

Heusel et al. (2017).

> Heusel 等人(2017)。步骤:

1. Extraer las características de Inception-v3 (2048-D) para N imágenes reales y N generadas.
   Por lo tanto, el proyecto de investigación de la Universidad de San Francisco (UFSA) se ha desarrollado para ayudar a los estudiantes a desarrollar sus capacidades de aprendizaje.
2. Encaja un gaussiano en cada piscina: media de cálculo `μ_r, μ_g`y la covarianza `Σ_r, Σ_g`¿ Qué ?
   Para cada grupo de valores:`μ_r, μ_g`Y la diferencia`Σ_r, Σ_g`¿Qué es eso?
3. FID = `||μ_r - μ_g||² + Tr(Σ_r + Σ_g - 2 · (Σ_r · Σ_g)^0.5)`¿ Qué ?
   FID = `||μ_r - μ_g||² + Tr(Σ_r + Σ_g - 2 · (Σ_r · Σ_g)^0.5)`¿Qué es eso?

Interpretación: distancia de Fréchet entre dos Gaussianos multivariados en el espacio de características.

> 解读:Trategy space                                                                                                                                                                                                                                                           

Modo de falla:

> 失败模式:

- **Biased on small N.**FID es el cuadrado medio sobre la distribución de características  pequeña N subestima la covarianza, da falsamente bajo FID. Siempre use N ≥ 10,000.
  FID es el error medio de la distribución de características, FID es el error medio de la distribución, FID es el menor de los valores de la distribución, FID es el menor de los valores de la distribución.
- **Inception-dependent.**Inception-v3 fue entrenado en ImageNet. Los dominios lejos de ImageNet (cara, arte, imágenes de texto) producen FID sin sentido.
  De acuerdo con Inception:Inception-v3 en ImageNet 上训练──远离 ImageNet's domain ([[人脸]],艺术、文字图像]]) se producirá FID (FID) sin sentido── utilizar en el dominio específico de los trajes de extracción──
- **Gaming.**El sobreajuste al previo de inicio da un bajo FID sin mejoría de la calidad visual.
  刷分: para la Inception pre-tested fue diseñado para dar bajo FID pero la calidad de la visión no mejoró.

### Punto de CLIP  Seguimiento inmediato  Punto de CLIP  Seguimiento inmediato

Radford et al. (2021). Para una imagen generada + prompt:

> Radford 等人(2021)。

```
clip_score = cos_sim( CLIP_image(x_gen), CLIP_text(prompt) )
```

Medio en 30k imágenes generadas → una escala comparable entre modelos.

> Se puede comparar una imagen de 30k 张 generando una media → una cantidad de muestras entre modelos.

Modo de falla:

> 失败模式:

- **CLIP's own blind spots.**CLIP tiene un razonamiento de composición débil ("un cubo rojo en una esfera azul" a menudo falla).
  CLIP  propia cego: CLIP 组合推理能力弱 (la capacidad de pensar es débil) ⋅ "red colored cubo on blue ball body" (el cubo en rojo en el globo azul) ⋅ menudo falla) ⋅ modelo puede clasificarse en la clasificación superior de CLIP Score por primera vez pero en realidad no sigue realmente un complejo prompt。
- **Short prompt bias.**Las instrucciones cortas tienen más coincidencias de imágenes CLIP en la naturaleza. Las instrucciones más largas tienen puntuaciones CLIP más bajas mecánicamente.
  短 prompt 偏差:短 prompt 在野外有更多 CLIP-image 匹配──长 prompt 在 CLIP Score 上机械性地更低──
- **Prompt gaming.**Incluir "alta calidad, 4k, obra maestra" en el prompt infla la puntuación CLIP sin mejorar la vinculación de imagen-texto.
  Enstant 刷分: 在 prompt 中加入 "alta calidad, 4k, obra maestra" 能升高 CLIP Score而不改善图文绑定──

CMMD (Jayasumana et al., 2024) corrige algunas de estas características: utiliza características CLIP en lugar de Inception, discrepancia máxima media en lugar de Fréchet. Mejor en la detección de diferencias sutiles de calidad.

> CMMD(Jayasumana 等人 2024) corrigió algunos de los problemas: utilizar CLIP características en lugar de inicio, utilizar MMD(máxima media de valor diferencial) en lugar de distancia.

### Prefierencia humana  la verdad de la tierra  Prefierencia de la gente  Valor real de la tierra

Seleccione un conjunto de instrucciones. Generar con el modelo A y el modelo B. Muestre pares a los humanos (o un juez LLM fuerte).

> 選一批提示──用模型 A 和模型 B 生成──把成对结果展示给人类 (或强 LLM 评判)──把胜场聚聚为 Elo 或 Bradley-Terry 分数──基准:

- **PartiPrompts (Google)**: 1.600 diferentes instrucciones, 12 categorías.
  **PartiPrompts（Google）**:1600 个多样化提示,12 个类别──
- **HPSv2**: 107k anotaciones humanas, ampliamente utilizadas como proxy automatizado.
  **HPSv2**10.70.000 artículos de etiquetas humanas, ampliamente utilizados como agentes automáticos.
- **ImageReward**: 137k pares de preferencias de imágenes instantáneas, con licencia MIT.
  **ImageReward**13,7 mil por favor de imágenes de inmediato, MIT.
- **PickScore**: entrenados en preferencias de Pick-a-Pic 2.6M.
  **PickScore**En el Pick-a-Pic 260 millones de personas se han entrenado.
- **Chatbot-Arena-style image arenas**¿ Qué es esto ?https://imagearena.ai/y otros.
  **Chatbot-Arena 风格的图像竞技场**¿Qué es esto ?https://imagearena.ai/Y así.

Modo de falla:

> 失败模式:

- **Judge variance.**Los no expertos tienen preferencias diferentes a las expertas.
  评判者方差: los no expertos y los expertos tienen preferencias diferentes.
- **Prompt distribution.**Las instrucciones de cereza favorecen a una familia.
  Pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, pronto, para que será, pronto, para que será, para que será pronto, para que será pronto, para que será pronto, para que será pronto, para que será pronto, para que será pronto, para su vez vez vez vez vez que será, para ser ...
- **LLM-judge reward hacking.**El juez de GPT-4 se engaña con resultados bonitos pero equivocados.
  LLM 评判被刷分:GPT-4 评判会被"好看但错"的输出欺骗──与人类三角验证──

## Usar juntos

Un informe de evaluación de la producción debe incluir:

> Un informe de evaluación de la producción debe incluir:

1. FID en muestras de 10 a 30 mil en comparación con una distribución real prolongada (calidad de la muestra).
   En 10-30k muestras en comparación de dejar de distribuirse real de la FID ((muestra de calidad) 👇
2. Punto CLIP / CMMD en las mismas muestras frente a sus indicaciones (adherencia).
   Como en el caso de los países de la UE, el nivel de la población en el país es el nivel de la población de la UE.
3. Taxa de ganancias en una arena ciega frente al modelo anterior (preferencia general).
   Con un modelo anterior en el campo de juego de la opinión ciega
4. Análisis de modo de falla: 50 salidas muestranadas al azar, marcadas por problemas conocidos (anatomía de la mano, renderización de texto, recuento de objetos consistente).
   失败模式分析:随机采样 50 输出,标记已知问题(手部解剖、文字染、对象计数一致性)

Cualquier métrica es una mentira. Tres métricas corroboradoras + revisión cualitativa son una afirmación.

>  cualquier indice único es mentira  Tres indices mutuamente evidentes                                                                                                                                                                                                                                                      

## Construye y realiza.
```figure
gx-fid-distributions
```

## Construye el mismo

`code/main.py`Implementa la agregación de FID, CLIP-score-like, y Elo en "vectores de características" sintéticos (usamos vectores 4D como alternativos para las características de Inception).

> `code/main.py`En sintesis "trademarks" para lograr FID, CLIP Score y Elo 聚合 (), usamos 4 维向量 en lugar de "trademarks de inicio").

- El cálculo de FID en un pequeño N y en un grande N  el sesgo.
  Pequeño N y grande N 上 de FID  calcular 偏差──
- "Colocación CLIP" como similitud cosina entre las pools de características.
  Como característica de la similitud entre los cuerpos
- Regla de actualización de Elo de un flujo de preferencias sintéticas.
  Desde la composición de preferencias de Elo 更新规则──

### Paso 1: FID en cuatro líneas.

```python
def fid(real_features, gen_features):
    mu_r, cov_r = mean_and_cov(real_features)
    mu_g, cov_g = mean_and_cov(gen_features)
    mean_diff = sum((a - b) ** 2 for a, b in zip(mu_r, mu_g))
    trace_term = trace(cov_r) + trace(cov_g) - 2 * sqrt_cov_product(cov_r, cov_g)
    return mean_diff + trace_term
```

> Cuatro líneas FID: diferencia entre el promedio de cálculo de las características reales y generales y el promedio de cálculo de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia entre la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia de la diferencia entre la diferencia de la

### Paso 2: Similaridad cosínica en estilo CLIP.

```python
def clip_like(image_feat, text_feat):
    dot = sum(a * b for a, b in zip(image_feat, text_feat))
    norm = math.sqrt(dot_self(image_feat) * dot_self(text_feat))
    return dot / max(norm, 1e-8)
```

> CLIP 风格余弦相似度: punto积除以两个向量范数乘积,加epsilon 防止除零──

### Paso 3: Elogregación de Elo

```python
def elo_update(r_a, r_b, winner, k=32):
    expected_a = 1 / (1 + 10 ** ((r_b - r_a) / 400))
    actual_a = 1.0 if winner == "a" else 0.0
    r_a_new = r_a + k * (actual_a - expected_a)
    r_b_new = r_b - k * (actual_a - expected_a)
    return r_a_new, r_b_new
```

> Elo 更新: Basado en la expectativa de ganancia y el resultado real, K=32 es el estándar de juego internacional.

## Enlaces.

- **FID at N=1000.**La heurística es poco confiable bajo N=10k. Los documentos que informan de bajo N FID están jugando.
  N=1000 时的FID:在N<10k 时不可靠──报告低 N FID 的论文在刷分──
- **Comparing FID across resolutions.**El tamaño de 299×299 de Inception cambia la distribución de características.
  跨分辨率比较 FID:Inception's 299×299 缩放会改变特征分布──只在匹配分辨率下比较──
- **Reporting one seed.**Ejecutar 3 semillas como mínimo.
  Sólo reportar una semilla: al menos 3 semillas han sido ejecutadas.
- **CLIP score inflation via negative prompts.**Algunos conductos aumentan el CLIP al montar demasiado el aviso.
  通过负向快速 抬高 CLIP Score:有些流水线通过过拟合快速 抬高 CLIP──检查视觉和──
- **Elo bias from prompt overlap.**Si ambos modelos vieron un punto de referencia durante el entrenamiento, Elo no tiene sentido.
  El tiempo de trabajo de los dos modelos se ha convertido en un tiempo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de trabajo de
- **Human eval paid-crowd skew.**Los anotadores MTurk prolíficos son más jóvenes / amigables con la tecnología.
  工评付费众包偏差:Prolific、MTurk 标注者偏年轻 / 偏技术友好──混合招募的艺术/设计专家──

## Usalo con el marco de ejecución

Protocolo de evaluación de la producción en 2026:

> Acuerdo de evaluación de la producción de 2026:

| Pillar / 支柱 | Minimum / 最低要求 | Recommended / 推荐 |
|--------|---------|-------------|
| Sample quality / 样本质量 | FID on 10k vs held-out real | + CMMD on 5k + FID on subset per category |
| Prompt adherence / Prompt 遵循 | CLIP score on 30k | + HPSv2 + ImageReward + VQA-style question answering |
| Preference / 偏好 | 200 blinded pairs vs baseline | + 2000 paired human + LLM-judge + Chatbot Arena |
| Failure analysis / 失败分析 | 50 hand-flagged | 500 hand-flagged + automated safety classifier |

Los cuatro pilares en un informe = reclamo.

> Cuatro pilares llenos de un solo mensaje.

## Envíe el producto .

Salva .`outputs/skill-eval-report.md`. Skill toma un nuevo punto de control de modelo + línea de base y produce un plan de evaluación completo: tamaños de muestra, métricas, sondas de modo de falla, criterios de firma.

> 保存为                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `outputs/skill-eval-report.md` Esta habilidad recibe un nuevo punto de control de modelo + 基线, y produce un plan de evaluación completo: muestra de muestras, indicadores, modelos de fracaso, búsquedas, signos, estándares.

## Los ejercicios.

1. **Easy.**- ¿ Qué ?`code/main.py`. Comparar el FID en N=100 vs N=1000 en las mismas distribuciones sintéticas.
2. **Medium.**Implementar CMMD a partir de características sintéticas de estilo CLIP (ver Jayasumana et al., 2024 para la fórmula). Comparar la sensibilidad a las diferencias de calidad con FID.
3. **Hard.**Replicar la configuración HPSv2: tomar 1000 pares de imágenes de un subconjunto de Pick-a-Pic, ajustar a un pequeño puntero basado en CLIP en las preferencias, y medir su conformidad con un conjunto prolongado.

## Términos clave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| FID | "Fréchet Inception Distance" | Fréchet distance of Gaussian fits to real vs gen Inception features. |
| CLIP score | "Text-image similarity" | Cosine similarity between CLIP image and text embeddings. |
| CMMD | "FID's replacement" | CLIP-feature MMD; less biased, no Gaussian assumption. |
| IS | "Inception score" | Exp KL(p(y|x) || p(y)); correlates poorly on modern models, retired. |
| HPSv2 / ImageReward / PickScore | "Learned preference proxies" | Small models trained on human preferences; used as automatic judges. |
| Elo | "Chess rating" | Bradley-Terry aggregation of pairwise wins. |
| PartiPrompts | "The benchmark prompt set" | 1,600 Google-curated prompts across 12 categories. |
| FD-DINO | "Self-sup replacement" | FD using DINOv2 features; better for out-of-ImageNet domains. |

## Nota de producción: la evaluación es una carga de trabajo de inferencia demasiado.

Para una base SDXL de 50 pasos en 10242 en un solo L4, es decir ~11 horas de inferencia de una sola solicitud. Los presupuestos de evaluación son reales, y el marco es exactamente el escenario de inferencia fuera de línea (máxima rendimiento, ignora TTFT):

- **Batch hard, forget latency.**Evaluación fuera de línea = lotes estáticos en el tamaño más grande que se adapte a la memoria. `pipe(...).images`con`num_images_per_prompt=8`en un H100 de 80 GB funciona 4-6 veces más rápido que el reloj de pared de una sola solicitud.
- **Cache the real features.**La extracción de la función de inicio (FID) o CLIP (CLIP-score, CMMD) sobre el conjunto de referencia real se ejecuta *once*, almacenada como una`.npz`No recompite por evaluación.

Para las puertas de CI / regresión: ejecuta la puntuación FID + CLIP en un subconjunto de 500 muestras por PR (~ 30 min); ejecuta la puntuación completa 10k FID + HPSv2 + Elo por noche.

## Más Leer más Leer más

- [Heusel et al. (2017). GANs Trained by a Two Time-Scale Update Rule Converge to a Local Nash Equilibrium (FID)](https://arxiv.org/abs/1706.08500) Papel de la FID.
- [Jayasumana et al. (2024). Rethinking FID: Towards a Better Evaluation Metric for Image Generation (CMMD)](https://arxiv.org/abs/2401.09603) CMMD.
- [Radford et al. (2021). Learning Transferable Visual Models from Natural Language Supervision (CLIP)](https://arxiv.org/abs/2103.00020) CLIP.
- [Wu et al. (2023). HPSv2: A Comprehensive Human Preference Score](https://arxiv.org/abs/2306.09341) HPSv2.
- [Xu et al. (2023). ImageReward: Learning and Evaluating Human Preferences for Text-to-Image Generation](https://arxiv.org/abs/2304.05977) ImageReward.
- [Yu et al. (2023). Scaling Autoregressive Models for Content-Rich Text-to-Image Generation (Parti + PartiPrompts)](https://arxiv.org/abs/2206.10789) PartiPrompts.
- [Stein et al. (2023). Exposing flaws of generative model evaluation metrics](https://arxiv.org/abs/2306.04675) Encuesta de modo de falla.
