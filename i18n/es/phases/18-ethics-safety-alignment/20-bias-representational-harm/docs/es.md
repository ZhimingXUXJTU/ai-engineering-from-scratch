# Prejuicios y daños representativos en LLM

> Gallegos, Rossi, Barrow, Tanjim, Kim, Dernoncourt, Yu, Zhang, Ahmed (Lingüística computacional 2024, arXiv:2309.00770). Encuesta de base de 2024 que distingue los daños representativos (estereotipos, borrado) de los daños asignacionales (distribución desigual de recursos) y categorizando las métricas de evaluación como basadas en la incorporación, basadas en la probabilidad o basadas en el texto generado. 2024-2025 empírico: An et al. (PNAS Nexus, marzo 2025) mide el sesgo de género x raza intersectorial en GPT-3.5 Turbo, GPT-4o, Gemini 1.5 Flash, Claude 3.5 Sonnet, Llama 3-70B en evaluación automática de currículum para 20 trabajos de nivel de entrada. El objetivo de la evaluación de la equidad de las identidades intersectoriales es garantizar la transparencia de las identidades intersectoriales. Yu & Ananiadou 2025 identifican las neuronas de género en las capas de MLP; Ahsan & Wallace 2025 utilizan SAEs para revelar el sesgo racial clínico; Zhou et al. 2024 (UniBias) manipula las cabezas de atención para desviar. Meta-crítica (arXiv:2508.11067): La literatura de 10 años se centra desproporcionadamente en el sesgo binario de género.

> **【中文解读】**Este capítulo presenta la fuente de prejuicios y la distribución de recursos en sistemas de IA. Gallegos  etcétera  Linguística Computacional 2024) distingue entre la distribución de recursos y la distribución de los recursos, y evaluará la clasificación de indicadores en base a la inserción, la probabilidad y la generación de textos.

> **【拓展：交叉偏见 → 真实世界影响】**Un 等人(PNAS Nexus, 2025 年 3 月) midió GPT-3.5 Turbo、GPT-4o、Gemini 1.5 Flash、Claude 3.5 Sonnet、Llama 3-70B en 20 个入门级职位自动简历评估中的交叉性别×种族偏见──GPT-4o 在简历评分中对黑人女性的惩罚对黑人男性和白人女性的分别更严重单轴评估无法捕捉这种效应──

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, toy embedding-based bias probe) | **语言:** Python（标准库，玩具嵌入偏见探针）
**Prerequisites:** Phase 05 (word embeddings), Phase 18 · 01 (instruction following) | **前置知识:** Phase 05 (词嵌入), Phase 18 · 01 (指令遵循)
**Time:** ~60 minutes | **时间:** ~60 分钟

> ¿ Qué es esto ?**【前置】**Estudiar en el campo de la educación y la educación en la educación y la educación en la educación.
> ¿ Qué es esto ?**【类比】**偏见 = "AI tiene ojos de color"── proviene de datos de entrenamiento(social history bias) + 训练目标──评估三方法:嵌入空间(向量几何) + 概率(logits 差) + 生成文本(输出统计)──2025 Un PNAS Nexus:GPT/Claude/Gemini/Llama en la evaluación de la historia tiene un交叉性别×种族偏见──Yu 2025 en MLP 定位"性别神经元",Ahsan 2025 Used SAE 揭示临床种族偏见──

## Objetivos de aprendizaje

- Definir el daño representativo vs asignación y dar un ejemplo de cada uno en una implementación de LLM.

>  define las lesiones representativas y las lesiones distributivas, y cada uno de ellos en un ejemplo de la implementación del MLL:

- Nombre de las tres categorías de evaluación-metríca de Gallegos et al. 2024 y describir una métrica de cada una.

> 列出 Gallegos 等人 de 2024 tres indicadores de evaluación,并描述每类中的一个指标――

- Describa la intersección y por qué la medición de equidad basada en la incertidumbre de WinoIdentity aborda las lagunas en la evaluación de sesgos de un solo eje.

>  Describir la交叉性 y por qué la medición equitativa basada en la incertidumbre de WinoIdentity resolvió la falta de evaluación de prejuicios unilaterales

- Describa dos enfoques de interpretación mecánica del sesgo (neuronas de género, características de SAE, manipulación de la cabeza de atención).

> 描述两种偏见的机制可解释性方法 (Mécanismo de las dos clases de prejuicios puede explicarse de forma explicativa).

## El problema es el problema .

Las lecciones anteriores abarcan el daño deliberado (infracciones de cárcel, esquemas) y la gobernanza de la seguridad. El sesgo es el daño que surge sin intención  de la formación de las distribuciones de datos, de la elaboración rápida, de las opciones de diseño acumuladas.

>  los cursos anteriores abarcan las lesiones intencionales (越狱,策略) y la gestión de la seguridad los prejuicios son los daños sin intención provienen de la distribución de datos de entrenamiento, los marcos de sugerencias, la selección de diseño acumulado.

## El concepto.

### Representativo vs asignación

- **Representational harm.**Estereotipos, borrado, retratos degradantes. Un LLM que representa a las enfermeras como exclusivamente femeninas está produciendo daño representativo.
- **Allocational harm.**Un LLM que califica sistemáticamente más bajo los currículos de los solicitantes negros produce daños asignacionales.

> **代表性伤害：**刻板印象、抹除、低性描绘──**分配性伤害：**Resultados de la materia desigual. Los dos modelos diferentes pueden ser "representativos sin prejuicios", pero "distributivos con prejuicios".

Un modelo puede ser "representativamente imparcial" (produce retratos diversos) mientras que es "partido alocativamente" (hace recomendaciones desiguales).

> 评估需要同时测量两者──

> **【中文解读】**Tres tipos de indicadores de evaluación: enmembración de la base (WEB                                                                                                                                                                                                                                                       

### El objetivo de la evaluación es mejorar la calidad de la información y la calidad de la información.

- **Embedding-based.**Pruebas de tipo WEAT en embeddings anteriores a RLHF. Mide las asociaciones estadísticas entre términos de identidad y términos de atributos.
- **Probability-based.**Log-probabilidad de los estereotipos que confirman contra estereotipos que violan los resultados.
- **Generated-text-based.**Medición de tareas posteriores en el texto generado. Scoring de currículum, escritura de recomendaciones, diálogo. Más ecológicamente válido; más difícil de reproducir.

> **嵌入基础：**El tiempo de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de la prueba de prueba de prueba de la prueba de la prueba de la prueba de prueba de la prueba de la prueba de la prueba de la prueba de prueba de la prueba de la prueba de la prueba de prueba de prueba de prueba de la prueba de prueba de prueba de la prueba de la prueba de prueba de la prueba de prueba de prueba de la prueba de prueba de prueba de prueba de prueba de**概率基础：**刻板印象确认 vs 违反补全的对数似然比比──**生成文本基础：**Método de tarea, la mayor eficiencia pero más difícil de realizar.

### Intersección

La evaluación de la discriminación sobre "género" pierde el sesgo que solo dispara en pares (género, raza). Un estudio de 2025 y otros encontró que GPT-4o penaliza a las mujeres negras en los currículos que obtienen más puntos que los hombres negros y más que las mujeres blancas por separado.

> La evaluación de los prejuicios sobre el "género" se ha olvidado de los prejuicios sobre el género, la raza, etc. En el estudio de la GPT-4o se ha encontrado que la discriminación entre hombres y mujeres blancas en la mujer negra es más grave que en la evaluación de la historia.

WinoIdentity (COLM 2025) introduce la equidad intersectorial basada en la incertidumbre. mide si la incertidumbre del modelo sobre los resultados difiere entre los tuples de identidad intersectorial  no solo la predicción de puntos. Esto capta casos en los que el modelo es igualmente incorrecto entre los grupos pero más incierto para algunos, lo que produce un comportamiento de asignación a la baja diferente.

> WinoIdentity  introducción basada en la incertidumbre de la tasa de evaluación de la tasa de identidad.

> **【拓展：机制可解释性 → 偏见干预新路径】**El mecanismo explicable del trabajo de 2024-2025 abrió el camino a la intervención del mecanismo: genero neuronas (Yu & Ananiadou 2025)  MLP neuronas específicas relacionadas con el comportamiento específico de género, desintegrando estos neuronas con un costo limitado de capacidad para reducir la diferencia de género; clínico racial prejuicio SAE  Ahsan & Wallace 2025)  Rarura de los rasgos de codificación característicos se desglosarán en dimensiones explicables; UniBias  Zhou  et al. 2024)  Atención a la operación de realizar un modelo de desvío de prejuicio 

### Enfoques mecánicos

El trabajo de interpretación 2024-2025 abre el sesgo a la intervención mecanicista:

- **Gender neurons (Yu & Ananiadou 2025).**Las neuronas MLP específicas se correlacionan con comportamientos específicos de género.
- **Clinical racial bias via SAEs (Ahsan & Wallace 2025).**Las características de autoencoder Sparse descomponen la representación interna en dimensiones interpretables; las características relacionadas con la raza pueden ser identificadas y suprimidas.
- **UniBias (Zhou et al. 2024).**La manipulación de la cabeza de atención para desacelerar con disparos cero. Las cabezas específicas amplifican la sensibilidad de la clase de identidad; el cero o el nuevo peso de estas cabezas reduce el sesgo sin ajuste fino.

> El mecanismo explicable del trabajo de 2024-2025 abrió el camino a la intervención del mecanismo de prejuicios: genero neurales  eliminación de estos neuronas con un costo limitado de capacidad para reducir la diferencia de género; prejuicio étnico clínico SAE  identificación y inhibición de rasas relacionadas características; UniBias  atención de la operación para lograr el zero de muestras de prejuicios.

> **【中文解读】**元評論(arXiv:2508.11067, 2025): 10 años de literatura recalcuando encontró que el campo se centra desproporcionadamente en el prejuicio de género de dos dimensiones.

### La meta-crítica

La revisión de la literatura de 10 años (arXiv:2508.11067, 2025) encuentra que el campo se centra desproporcionadamente en el sesgo binario de género. Otros ejes  discapacidad, religión, estatus migratorio, identidad multilingüe  reciben mucha menos atención. La meta-crítica argumenta que el enfoque estrecho puede dañar a los grupos marginados por negligencia: un modelo bien desviado sobre el género binario puede ser muy sesgado en dimensiones que nadie ha verificado.

> 10 años de literatura recueve que este campo se centra desproporcionadamente en los prejuicios de género de las dos clases.

### Donde esto encaja en la Fase 18

Las lecciones 20-21 cubren formalmente el sesgo y la equidad. La lección 22 abarca la privacidad. La lección 23 abarca el marcado de agua. Estas son las capas de daño al usuario que complementan la capa anterior de engaño / seguridad.

> Lecciones 20-21 Forma cover bias and fairness. Lección 22 cover privacy. Lección 23 cover waterprint.

> **【拓展：交叉性 → WinoIdentity 基准】**WinoIdentity(COLM 2025, arXiv:2508.07111) introduce la evaluación de la equidad de la relación entre grupos basado en la incertidumbre.

## Usalo.
```figure
an-bias-two-harms
```

## Usalo

`code/main.py`construye una sonda de sesgo basada en la incorporación de juguetes: mide la distancia al estilo WEAT entre los términos de identidad y los términos de atributos en una simple incorporación de cooccurrencia.

> `code/main.py`Construyó un instrumento de juego: Métido de la distancia entre los términos de identidad y los términos de la propiedad.

## Envíalo .

Esta lección produce`outputs/skill-bias-eval.md`. Dado un modelo de tarjeta o una afirmación de equidad, audita la evaluación en las tres categorías métricas (embedding, probabilidad, generated-text), la cobertura de intersectionalidad y el mecanismo de cualquier intervención de desactivación.

> 本课产 出  `outputs/skill-bias-eval.md` una declaración de equidad, evaluación de los indicadores de auditoría, cobertura y mecanismo de intervención de carácter parcial.

## Los ejercicios.

1. - ¿ Qué ?`code/main.py`• Informar de los resultados de sesgo de tipo WEAT antes y después del paso de desaceleración.

2. Extenda la sonda con una prueba intersectorial: (género, raza) x (carrera, familia).

3. En el caso de los Estados miembros, el número de casos de discriminación de género en el sistema de evaluación de género de un solo eje no se puede calcular.

4. Yu & Ananiadou 2025 identifican las neuronas de género. Esbozan un experimento de falsificación que distinguiría "estas neuronas causan sesgo de género" de "estas neuronas se correlacionan con el sesgo de género".

5. La meta-crítica argumenta que el campo se centra demasiado estrechamente en el género binario.

## Términos clave .

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| Representational harm | "stereotypes / erasure" | Biased portrayal of a group |
| Allocational harm | "unequal decisions" | Biased material outcome for a group |
| WEAT | "the embedding test" | Word Embedding Association Test; co-occurrence-based bias probe |
| Intersectionality | "combined identity effects" | Bias that emerges at the intersection of multiple identity axes |
| Gender neurons | "MLP bias neurons" | Specific neurons whose activations correlate with gender-specific behaviour |
| SAE feature | "interpretable dimension" | Sparse-autoencoder-identified feature; useful for mechanistic bias analysis |
| UniBias | "attention-head debiasing" | Zero-shot debiasing by reweighting attention heads |

## Más Leer más Leer más

- [Gallegos et al. — Bias and Fairness in LLMs: A Survey (arXiv:2309.00770, Computational Linguistics 2024)](https://arxiv.org/abs/2309.00770) Encuesta canónica
- [An et al. — Intersectional resume-evaluation bias (PNAS Nexus, March 2025)](https://academic.oup.com/pnasnexus/article/4/3/pgaf089/8111343) Estudio interseccionario de cinco modelos
- [WinoIdentity — uncertainty-based intersectional fairness (arXiv:2508.07111, COLM 2025)](https://arxiv.org/abs/2508.07111) Nuevo índice de referencia
- [UniBias — attention-head manipulation (Zhou et al. 2024, ACL)](https://arxiv.org/abs/2405.20612) Descarga de tiro cero
