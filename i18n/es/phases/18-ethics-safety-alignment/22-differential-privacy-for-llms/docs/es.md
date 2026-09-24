# Diferencia de privacidad para LLM 差分隐私 LLM

> DP-SGD sigue siendo la actualización estándar de gradientes inyectados por ruido  proporcionan garantías formales (epsilon, delta). El gasto general en computación, memoria y utilidad es sustancial; el ajuste fino de DP eficiente en parámetros (LoRA + DP-SGD) es la configuración común de 2025 (ACM 2025). Dos cuerpos de evidencia en tensión: la inferencia de membresía basada en canarios (Duan et al., 2024) informa de un éxito limitado contra los modelos de lenguaje; la extracción de datos de capacitación (Carlini et al., 2021; Nasr et al., 2025) recupera una memorización literal sustancial. Resolución (arXiv:2503.06808, marzo 2025): la brecha es en lo que se mide  canarios insertados vs "más extractables" datos. Los nuevos diseños de canarios permiten una MIA basada en pérdidas sin modelos de sombra y dan lugar a la primera auditoría de DP no trivial de un LLM capacitado en datos reales con garantías realistas de DP. Alternativas: PMixED (arXiv:2403.15638)  predicción privada en el tiempo de inferencia a través de una mezcla de expertos en las distribuciones de tokens siguientes; generación de datos sintéticos DP (Google Research 2024). Ataque emergente: Inversión de la privacidad diferencial a través de la retroalimentación de LLM  fuga de puntaje de confianza.

> **【中文解读】**Este capítulo presenta la diferencia de privacidad de LLM en el método matemático de protección de la privacidad de datos de los usuarios en el entrenamiento y la reflexión.

> **【拓展：MIA vs 训练数据提取 → 衡量差距】**Las dos evidencias de la línea de formación de 2024-2025 años Zhang力: 金丝雀 MIA(Duan 等人 2024) Report on Language Model's Success Limited; train数据提取(Carlini 2021, Nasr 等人 2025) Recuperar un gran número de memorias por letra.

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, DP-SGD noise-injection and ε-δ accountant demonstration) | **语言:** Python（标准库，DP-SGD 噪声注入和 ε-δ 计数器演示）
**Prerequisites:** Phase 01 · 09 (information theory), Phase 10 · 01 (large-model training) | **前置知识:** Phase 01 · 09 (信息论), Phase 10 · 01 (大模型训练)
**Time:** ~60 minutes | **时间:** ~60 分钟

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 01·09(信息论)、Fase 10·01(大模型训练)。DP-SGD = 标准 DP 训练方法,(ε,δ) 保证。
> ¿ Qué es esto ?**【类比】**DP = "data hidden身衣"──DP-SGD en la escala de inyección de ruido, un solo ejemplo no afecta a la formación completa→ Formalización matemática prueba no puede ser de un modelo de la información en el entrenamiento conjunto──代价:计算/内存/效用都明显下降──LoRA+DP-SGD es 2025 实用配置(
> 🤔 困境: MIA 攻击失败 vs 训练数据提取成功差别在测什么(插入 vs 最易提取) ・・・2025.3 新金雀设计首次对真数据 LLM做非凡 DP 审计──

## Objetivos de aprendizaje

- Definir la privacidad diferencial (epsilon, delta) y indicar la receta DP-SGD.
- Explica la tensión de 2024-2025: el MIA canario vs extracción de datos de entrenamiento dan imágenes diferentes.
- Describa el PMixED y por qué la predicción privada del tiempo de inferencia es una alternativa a la formación en DP.
- Describa la Inversión Diferencial de la Privacidad mediante el ataque de retroalimentación de LLM.

> 定义 (epsilon, delta) -差分隐私并说明 DP-SGD 方法──解释 2024-2025 年张力:金丝雀 MIA vs 训练数据提取给出不同图景──描述 PMixED 及为什么推理时私有预测是 DP 训练的替代──描述通过LLM 反的差分隐私逆转攻击──

## El problema es el problema .

Los LLM memorizan. Carlini et al. 2021 mostraron que los modelos de lenguaje de producción reproducen texto de entrenamiento literal a pedido. DP es la defensa formal: entrenar para que la salida sea probada insensible a cualquier ejemplo de entrenamiento. Las pruebas 2024-2025 muestran que DP-SGD es necesario pero los valores ε desplegados pueden no coincidir con el modelo de amenaza.

> LLM 会记忆──Carlini 等人 2021 años de demostración de producción de lenguaje modelo puede ser aplicado a la demanda replicado por palabra entrenamiento texto──DP es formalización defensa: entrenamiento hace que el resultado de cualquier un solo entrenamiento muestra insensível──2024-2025 años de evidencia muestra DP-SGD es necesario pero el ε 值可能的部署与威胁模型不匹配──

## El concepto.

> **【中文解读】**(epsilon, delta) -差分隐私定义:随机算法 M 是 (epsilon, delta) -DP 的, si para cualquier dos fases de diferencia en un ejemplo de datos y cualquier evento S:P(M(D) en S) <= e^epsilon * P(M(D') en S) + delta。

### (ε, δ) - privacidad diferencial

Un algoritmo aleatorio M es (ε, δ) -DP si para cualquier dos conjuntos de datos que difieren en un ejemplo y cualquier evento S:
P(M(D) en S) <= e^ε * P(M(D') en S) + δ.

> 随机算法 M 是 (ε, δ) -DP 的, si para cualquier dos fases diferencias de un ejemplo de datos y cualquier evento S:P(M(D) en S) <= e^ε * P(M(D') en S) + δ。

Interpretación: la distribución de salida es lo suficientemente cercana (parametrizada por ε) para que la contribución de un solo individuo no pueda inferirse confiablemente, excepto con probabilidad δ.

> 解释:输出分布足够接近 (由 ε 参数化)), ninguna contribución de un individuo puede ser deducida confiablemente, excepto la probabilidad δ──

### DPS-SGD

Abadi et al. 2016. La receta estándar:
1. Muestre un mini lote.
2. Calcule los gradientes por ejemplo.
3. Clip cada gradiente por ejemplo a un umbral C.
4. Sumar los gradientes recortados y agregar el ruido gaussiano con std σ * C.
5. Utilice la suma ruidosa para actualizar los parámetros.

> DP-SGD 标准方法:1. 采样小批次──2. 计算逐例梯度──3. 剪切每梯度到值 C──4. 求和剪切后的梯度并添加高的噪音──5.

El coste de la privacidad es rastreado por un contador (contador de Moments, contador de Rényi DP). Los valores ε reportados en la literatura de LLM varían ampliamente según el modelo de amenaza, la sensibilidad de los datos y el objetivo de utilidad; no hay un estándar universal "seguro" ε. Los ejemplos publicados abarcan aproximadamente ε ≈ 110 en algunos entornos de formación LLM, pero estos son ilustrativos  no se recomiendan los valores predeterminados. La reducción de ε generalmente requiere más ruido y puede aumentar la pérdida de utilidad.

> Costos de privacidad por el seguimiento de contadores                                                                                                                                                                                                                                                        

### LoRA + DP-SGD

El DP-SGD completo de un modelo fronterizo es prohibitivo. LoRA (Hu et al. 2022) limita las actualizaciones de gradiente a un pequeño adaptador, reduciendo el almacenamiento de gradiente por ejemplo. LoRA + DP-SGD es la configuración común de 2025. Las garantías DP se aplican al adaptador; el modelo base se mantiene fijo.

> Total DP-SGD  entrenamiento costos del modelo de primera línea son demasiado altos. LoRA  limitación de la escala actualizada a los pequeños adaptadores, reducción de la escala de almacenamiento de cada caso. LoRA + DP-SGD es la configuración habitual de 2025:

### La tensión de 2024-2025

Dos líneas de evidencia:

> 两条证据线:

- **Canary MIA (Duan et al. 2024).**Insertar canarios únicos en los datos de entrenamiento, medir si un atacante de la inferencia de membresía puede identificarlos.
- **Training-data extraction (Carlini 2021, Nasr et al. 2025).**El modelo se puede utilizar para determinar si el texto se recupera de forma literal de la formación.

> ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞

Resolución de marzo de 2025 (arXiv:2503.06808): las dos medidas diferentes cosas. MIA pregunta "¿es el ejemplo e en D?" en los canarios insertados.

> Resolución de marzo de 2025: dos medidas diferentes. La MIA pregunta "¿exemplo e está en D?", pregunta "¿qué puedo recuperar de D?"

Nuevos diseños de canarios. MIA basado en pérdidas sin modelos de sombra. Primera auditoría no trivial de DP de un LLM sobre datos reales con garantías realistas de DP.

> MIA basada en pérdidas del modelo de no sombra, por primera vez en la auditoría de DP extraordinaria de un LLM con un DP real garantizado en datos reales.

> **【拓展：PMixED → 推理时隐私】**PMixED(arXiv:2403.15638) proporciona una hipótesis: en el siguiente token, los expertos de la distribución mezclan, cada experto ve un fragmento de datos de entrenamiento, aglutinan un aumento de ruido para lograr DP.

### Alternativas a la formación en DP

- **PMixED (arXiv:2403.15638).**Previsión privada en el momento de la inferencia. mezcla de expertos en las distribuciones de tokens siguientes; cada experto ve un fragmento de datos de entrenamiento; agregación añade ruido para DP. Evitar el entrenamiento DP por completo.
- **DP synthetic data generation (Google Research 2024).**LoRA-fine-tune con DP-SGD, muestra de datos sintéticos, entrenar un clasificador en aguas posteriores sobre los datos sintéticos.

Ambos evitan el coste de utilidad de la formación completa de DP a costa de un modelo de amenaza diferente.

> **【中文解读】**差分隐私逆转攻击(2025): utilizar DP 训练模型的置信分数作为预言机重新识别个体──即使输出不泄露,置信分布也可能泄露──防御:不暴露置信度,或在暴露前截断/量化──这是 (epsilon, delta) -DP 训练之外的额外要求──

### Reversión diferencial de la privacidad a través de la retroalimentación del MLL

El ataque de 2025 emergente. Utilice los puntajes de confianza de un modelo entrenado en DP como un oráculo para volver a identificar a los individuos. Incluso cuando las salidas no se filtran, las distribuciones de confianza pueden.

> 2025 新兴攻击: utilizar el modelo de entrenamiento DP 训练模型的置信分数作为预言机重新识别个体──即使输出不泄露,置信分布也可能泄露──

La defensa: no exponer confidencias, o truncar / cuantificar antes de la exposición.

> 防御:不露置信度,或在露前截断/量化──这是 (ε, δ) DP 训练之外的额外要求──

### Donde esto encaja en la Fase 18

Las lecciones 20-21 son sesgos/justicia. La lección 22 es privacidad. La lección 23 es procedencia a través de marcas de agua. La lección 27 abarca la capa regulatoria de procedencia de datos.

> Lecciones 20-21 es prejuicio/justo. Lección 22 es privacidad. Lección 23 es fuente de agua.

> **【拓展：DP-SGD 的实际开销 → LoRA 解决方案】**El modelo de formación de DP-SGD se aplica a la configuración de los adaptadores, el modelo básico se mantiene fijo. Esto es un balance de ingeniería entre la utilidad y la privacidad.

## Usalo.
```figure
an-dp-clip-noise
```

## Usalo

`code/main.py`simula DP-SGD en un conjunto de datos de clasificación binaria de juguetes. Puede analizar el multiplicador de ruido σ y la norma de recorte C y rastrear el presupuesto (ε, δ) y el costo de precisión. Un "ataque canario" inserta un ejemplo de entrenamiento único y mide si una prueba de pérdida de registro puede detectarlo antes y después de DP.

> `code/main.py`En el juego de datos de segunda clase, se puede analizar el número de ruidos multiplicado σ y el número de cortes C, seguir (ε, δ)  presupuesto y el costo de precisión.

## Envíalo .

Esta lección produce`outputs/skill-dp-audit.md`. Dado que una declaración de DP sobre un modelo de lenguaje se implementa, audita: los valores (ε, δ), el contable utilizado, el protocolo de evaluación de la MIA y si se han evaluado los vectores de exposición a la confianza.

> 本课产 出  `outputs/skill-dp-audit.md` Declaración de DP en el modelo de lenguaje establecido, auditoría: ε, δ) √ valor, uso de contadores, MIA  evaluación de acuerdo y si se ha evaluado la confianza en la exposición a la radiación

## Los ejercicios.

1. - ¿ Qué ?`code/main.py`. Especie σ en {0,5, 1.0, 2.0} y informe el trade-off de precisión (ε, δ).

2. Se realizará una inserción de canarios y una prueba de pérdida de registro.

3. En el caso de las empresas que se encuentran en el mercado de servicios, el riesgo de que se produzcan problemas de salud y de salud es el de que se produzcan problemas de salud.

4. Diseñar una implementación utilizando PMixED (arXiv:2403.15638) que funcione completamente en el momento de la inferencia. ¿Cuál es el modelo de amenaza que PMixED aborda que DP-SGD no?

5. Esbozar la inversión de DP a través del ataque de retroalimentación de LLM. Diseñar una contramedida que limite la fuga de puntaje de confianza y estimar el costo de su despliegue.

## Términos clave .

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| DP | "(ε, δ)-differential privacy" | Formal privacy: output distribution close under neighbouring-dataset change |
| DP-SGD | "noise-injected SGD" | Gradient clipping + Gaussian noise addition; standard DP training |
| LoRA + DP-SGD | "efficient private fine-tune" | DP-SGD on low-rank adapters; standard 2025 configuration |
| MIA | "membership inference" | Attack that determines whether an example was in training data |
| Canary | "inserted watermark example" | Unique training example used to measure DP leakage |
| PMixED | "private inference mixture" | Inference-time DP via mixture-of-experts on next-token distributions |
| DP Reversal | "confidence leakage attack" | Attack that uses a model's confidence as an oracle for re-identification |

## Más Leer más Leer más

- [Abadi et al. — DP-SGD (arXiv:1607.00133)](https://arxiv.org/abs/1607.00133) el algoritmo de formación estándar de DP
- [Carlini et al. — Extracting Training Data (arXiv:2012.07805)](https://arxiv.org/abs/2012.07805) el papel de extracción canónica
- [Duan et al. — Canary MIA on LLMs (arXiv:2402.07841, 2024)](https://arxiv.org/abs/2402.07841) MIA de éxito limitado
- [Kowalczyk et al. — Auditing DP for LLMs (arXiv:2503.06808, March 2025)](https://arxiv.org/abs/2503.06808) Resolución de la tensión
- [PMixED (arXiv:2403.15638)](https://arxiv.org/abs/2403.15638) Previsión privada del tiempo de inferencia
