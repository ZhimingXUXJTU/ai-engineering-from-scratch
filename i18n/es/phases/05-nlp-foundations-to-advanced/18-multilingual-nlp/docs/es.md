# PNL multilingüe

> Un modelo, más de 100 idiomas, cero datos de capacitación para la mayoría de ellos. La transferencia translingüística es el milagro práctico de la década de 2020.
> Un modelo, 100+ idiomas, la mayoría de idiomas, es un fenómeno práctico de los años 2020.

> **【中文解读】**Más idiomas BERT, XLM-R etc.

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 04 (GloVe, FastText, Subword), Phase 5 · 11 (Machine Translation) | **前置知识:** Phase 5 · 04（GloVe、FastText、子词），Phase 5 · 11（机器翻译）
**Time:** ~45 minutes | **时间:** ~45 分钟

## El problema es la introducción del problema

El inglés tiene miles de millones de ejemplos etiquetados. El urdu tiene miles. El maithili casi no tiene ninguno. Cualquier sistema práctico de NLP que sirva a un público global tiene que trabajar en la larga cola de idiomas donde no existen datos de capacitación específicos de tareas.

> Inglés tiene miles de millones de ejemplos de marcas. En Urdu hay miles. En Maitili casi no hay. En cualquier servicio, los usuarios globales de NLP tienen que trabajar en un sistema de entrenamiento de tareas específico en un idioma que no existe.

> **【中文解读】**La pregunta planteada en este capítulo es: ¿cómo entender y aplicar correctamente esta tecnología en la ingeniería real? Comprender el contexto de la cuestión ayuda a comprender los puntos clave de decisión del tipo de selección técnica. En los sistemas de IA reales, el tipo de selección técnica errónea suele ser más alto que el costo de error de la realización de detalles.

Los modelos multilingües resuelven esto entrenando a un modelo en muchos idiomas simultáneamente. La representación compartida permite que el modelo transfiera las habilidades aprendidas en lenguas de alto recurso a las de bajo recurso. Al ajustar el modelo en el análisis de sentimiento inglés, produce sorprendentemente buenas predicciones de sentimiento en urdu fuera de la caja. Eso es transferencia interlingual de tiro cero, y ha remodelado la forma en que la PNL se transmite al mundo.

> El modelo multilingüe se ha formado en muchos idiomas para resolver este problema. El modelo de aprendizaje de alto recurso se ha transferido a un lenguaje de bajo recurso. En el análisis de emociones en inglés, el modelo de micro-modo genera una sorprendente buena predicción de emociones para el idioma urdu.

Esta lección menciona los compromisos, los modelos canónicos y la única decisión que hace que los equipos nuevos a la labor multilingüe: elegir un idioma fuente para la transferencia.

> Este curso se llama el modelo clásico y la decisión del equipo de trabajo de nuevos idiomas:

## El concepto central.

> **【中文解读】**Este capítulo presenta los conceptos y teorías básicos. La comprensión de estos conceptos es el prerrequisito de la realización posterior de la actividad, y también el conocimiento de los puntos de alta frecuencia de la entrevista y la práctica de la ingeniería.

![Cross-lingual transfer via shared multilingual embedding space](../assets/multilingual.svg)

**Shared vocabulary.**Los modelos multilingües utilizan un tokenizador SentencePiece o WordPiece entrenado en texto de todos los idiomas objetivo. El vocabulario es compartido: la misma unidad de subpalabra representa el mismo morfema en todos los idiomas relacionados. `anti-`en inglés e italiano obtiene la misma señal.

> **共享词表。**Muchos modelos de lenguaje utilizan en todos los textos de la lengua objetivo entrenados SentencePiece o WordPiece 分词器──词表是共享的: identica sublevación unidad en los idiomas relacionados representa la misma语素──英语和意大利语的`anti-`Obtener el mismo token.

**Shared representation.**Un transformador preentrenado en el modelado de lenguaje enmascarado en muchos idiomas aprende que oraciones semánticamente similares en diferentes idiomas producen estados ocultos similares. mBERT, XLM-R y NLLB todos lo muestran.

> **共享表示。**En muchos idiomas, el transformer aprendió que las oraciones similares en diferentes idiomas se producen en estado oculto similar. MBERT, XLM-R y NLLB han demostrado esto.

**Zero-shot transfer.**La etiqueta de la lengua de destino no es necesaria. Los resultados son fuertes para idiomas tipológicamente relacionados y más débiles para los distantes.

> **零样本迁移。**En un idioma (usualmente en inglés) los datos de etiquetas se encuentran en un modelo de modelado.

**Few-shot fine-tuning.**Añadir 100-500 ejemplos etiquetados en el idioma objetivo. La precisión salta al 95-98% de la línea de base en inglés en las tareas de clasificación. Esta es la palanca más rentable en la PNL multilingüe.

> **少样本微调。**En el idioma objetivo se añaden 100-500 muestras de etiquetado. En la clasificación de tareas, la tasa de precisión se eleva al 95-98% de la línea de base del inglés.

> **【拓展：大语言模型的工程实践】**Desde GPT hasta ChatGPT, el campo de NLP ha experimentado un cambio de paradigma de "cada tarea entrenar un modelo" a "un modelo resolver todas las tareas". En el proyecto real, la implementación de LLM necesita considerar los problemas de token 限制,延迟,成本, seguridad etc.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) es la estructura más popular de las aplicaciones de IA de las empresas actuales: la consulta de usuarios primero se consulta los documentos relacionados, luego se vuelve a buscar los resultados como respuesta a la pregunta de LLM.

> **【拓展：NLP 的多语言挑战】**En todo el mundo hay más de 7000 idiomas, pero los estudios de PNL se centran principalmente en inglés y en una minoría de idiomas.

## Los modelos .

| Model / 模型 | Year / 年份 | Coverage / 覆盖 | Notes / 说明 |
|-------|------|----------|-------|
| mBERT | 2018 | 104 languages / 104 种语言 | Trained on Wikipedia. First practical multilingual LM. Weak on low-resource. / 在 Wikipedia 上训练。首个实用多语言 LM。低资源语言较弱。 |
| XLM-R | 2019 | 100 languages / 100 种语言 | Trained on CommonCrawl. Sets the cross-lingual baseline. / 在 CommonCrawl 上训练。设定跨语言基线。 |
| XLM-V | 2023 | 100 languages / 100 种语言 | XLM-R with 1M-token vocabulary. Better on low-resource. / XLM-R 配 1M token 词表。低资源更好。 |
| mT5 | 2020 | 101 languages / 101 种语言 | T5 architecture for multilingual generation. / T5 架构用于多语言生成。 |
| NLLB-200 | 2022 | 200 languages / 200 种语言 | Meta's translation model; includes 55 low-resource languages. / Meta 翻译模型；含 55 种低资源语言。 |
| BLOOM | 2022 | 46 languages + 13 programming / 46 种语言 + 13 种编程语言 | Open 176B LLM trained multilingually. / 开源 176B 多语言 LLM。 |
| Aya-23 | 2024 | 23 languages / 23 种语言 | Cohere's multilingual LLM. Strong on Arabic, Hindi, Swahili. / Cohere 多语言 LLM。阿拉伯语、印地语、斯瓦希里语强。 |

Seleccionar por caso de uso. La clasificación funciona bien con la base XLM-R como el predeterminado razonable. Las tareas de generación requieren mT5 o NLLB dependiendo de la traducción vs generación abierta. Los pares de trabajo de estilo LLM con Aya-23 o Claude utilizando una solicitud multilingüe explícita.

> 按用例选择──分类任务以 XLM-R-base 作为合理默认──生成任务根据翻译vs开放生成选择 mT5 或 NLLB──LLM 风格工作配合 Aya-23 或 Claude 使用显式多语言提示──

## La decisión del idioma fuente (2026 investigación) 源语言决策

La mayoría de los equipos usan por defecto el inglés como fuente de ajuste fino.

> La mayoría de los equipos de la comunidad internacional de la lengua inglesa como un medio de comunicación.

La similitud lingüística predice la calidad de transferencia mejor que el tamaño del cuerpo crudo. Para los objetivos eslavos, el alemán o el ruso a menudo vencen al inglés.**qWALS**La métrica de similitud (2026, basada en las características del Atlas Mundial de Estructuras Lingüísticas) cuantifica esto. **LANGRANK**(Lin et al., ACL 2019) es un método separado y anterior que clasifica a los idiomas fuente candidatos a partir de una combinación de similitud lingüística, tamaño del cuerpo y relación genética.

> 语言相似性比原始语料大小更好地预测迁移质量──对于斯拉夫语目标,德语或俄语通常胜英语──对于印度语目标,印度语通常胜英语──**qWALS**La comparación de la sexualidad se ha ampliado en 2026.**LANGRANK**(Lin 等, ACL 2019) de la similaridad lingüística, el lenguaje de la lengua, el lenguaje de la lengua, el lenguaje de la lengua, el lenguaje de la lengua, el lenguaje de la lengua, el lenguaje de la lengua, el lenguaje de la lengua, el lenguaje de la lengua, el lenguaje de la lengua, el lenguaje de la lengua, el lenguaje de la lengua, el lenguaje de la lengua, el lenguaje de la lengua, el lenguaje de la lengua, el lenguaje de la lengua, el lenguaje de la lengua, el lenguaje de la lengua, el lenguaje de la lengua, el lenguaje de la lengua, el lenguaje de la lengua, el lenguaje de la lengua, el lenguaje de la lengua, el lenguaje de la lengua, el lenguaje de la lengua, el lenguaje de la lengua, el lenguaje de la lengua, el lenguaje de la lengua, el lenguaje de la lengua, el lengua y el lenguaje de la lengua, el lengua, el lenguaje de la lengua, etc.

Regla práctica: si tu idioma objetivo tiene un tipo de parente de alto recurso, intenta ajustarlo primero, y luego compártale con el inglés.

>  Reglas prácticas: si tu idioma objetivo tiene un tipo de lenguaje de alto recurso, primero intenta la moderación en ese idioma, y luego compara con el inglés.

## Construye y realiza.

> **【中文解读】**Este capítulo a través del código de la implementación de algoritmos centrales de cero. Este método "desde cero" puede ayudar a entender el principio detrás del marco, no se encuentra en la caja negra cuando se encuentran problemas.
```figure
n5-crosslingual-bridge
```

## Construye el mismo

### Paso 1: Clasificación interlingüística de vuelo cero

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

tok = AutoTokenizer.from_pretrained("joeddav/xlm-roberta-large-xnli")
model = AutoModelForSequenceClassification.from_pretrained("joeddav/xlm-roberta-large-xnli")


def classify(text, candidate_labels, hypothesis_template="This text is about {}."):
    scores = {}
    for label in candidate_labels:
        hypothesis = hypothesis_template.format(label)
        inputs = tok(text, hypothesis, return_tensors="pt", truncation=True)
        with torch.no_grad():
            logits = model(**inputs).logits[0]
        entail_score = torch.softmax(logits, dim=-1)[2].item()
        scores[label] = entail_score
    return dict(sorted(scores.items(), key=lambda x: -x[1]))


print(classify("I love this product!", ["positive", "negative", "neutral"]))
print(classify("मुझे यह उत्पाद पसंद है!", ["positive", "negative", "neutral"]))
print(classify("J'adore ce produit !", ["positive", "negative", "neutral"]))
```

Un modelo, tres idiomas, la misma API. XLM-R entrenado en NLI transferen datos bien a la clasificación a través del truco de implicación.

> Un modelo, tres idiomas, la misma API.

### Paso 2: espacio de incorporación multilingüe

```python
from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

pairs = [
    ("The cat is sleeping.", "Le chat dort."),
    ("The cat is sleeping.", "El gato está durmiendo."),
    ("The cat is sleeping.", "Die Katze schläft."),
    ("The cat is sleeping.", "The dog is barking."),
]

for eng, other in pairs:
    emb_eng = model.encode([eng], normalize_embeddings=True)[0]
    emb_other = model.encode([other], normalize_embeddings=True)[0]
    sim = float(np.dot(emb_eng, emb_other))
    print(f"  {eng!r} <-> {other!r}: cos={sim:.3f}")
```

Las traducciones se acercan en el espacio de incorporación. Una oración en inglés diferente se ubica más lejos. Esto es lo que hace que la recuperación, agrupamiento y similitud interlingual funcionen.

> 翻译在嵌入空间中距离很近. Diferentes idiomas en inglés se encuentran más lejos. Esta es la base de la búsqueda, la concentración y la similitud de los trabajos.

### Paso 3: Estrategia de ajuste fino de pocos disparos

```python
from transformers import TrainingArguments, Trainer
from datasets import Dataset


def few_shot_finetune(base_model, base_tokenizer, examples):
    ds = Dataset.from_list(examples)

    def tokenize_fn(ex):
        out = base_tokenizer(ex["text"], truncation=True, max_length=128)
        out["labels"] = ex["label"]
        return out

    ds = ds.map(tokenize_fn)
    args = TrainingArguments(
        output_dir="out",
        per_device_train_batch_size=8,
        num_train_epochs=5,
        learning_rate=2e-5,
        save_strategy="no",
    )
    trainer = Trainer(model=base_model, args=args, train_dataset=ds)
    trainer.train()
    return base_model
```

Para 100-500 ejemplos de idiomas objetivo, `num_train_epochs=5`y `learning_rate=2e-5`Las tasas de aprendizaje más altas causan que la alineación multilingüe colapse y obtienes un modelo solo en inglés.

>  para 100-500 个目标语言样本,`num_train_epochs=5`Y `learning_rate=2e-5`Es un valor de seguridad. Una tasa de aprendizaje más alta conducirá a la colisión de varios idiomas, obtendrás un modelo limitado al inglés.

> **【拓展：Prompt Engineering 与 LLM 应用】**La ingeniería rápida se ha convertido en la habilidad central de los ingenieros de PNL. Desde la Cero-Shot hasta la Few-Shot, desde la Cadena de Pensamiento hasta la Reacción, diferentes estrategias de sugerencias se aplican a diferentes escenarios.

## Una evaluación que realmente funciona.

- **Per-language accuracy on held-out sets.**No agregado, el agregado esconde la cola larga.
  **每种语言在留出集上的准确率。**No me reúnan. Me reúnen.
- **Benchmark against monolingual baseline.**Para los idiomas con suficientes datos, un modelo monolingüe entrenado desde cero a veces supera al multilingüe.
  **与单语基线比较。**Para un idioma con suficiente datos, el modelo de un solo idioma de entrenamiento a veces supera el modelo de varios idiomas.
- **Entity-level tests.**Las entidades denominadas en el idioma objetivo. Los modelos multilingües a menudo tienen una débil tokenización para escrituras lejos del latín.
  **实体级测试。**目標言語中的命名实体──多语言模型对远离拉丁文的书写的分词通常较弱──
- **Cross-lingual consistency.**El mismo significado en dos idiomas debería producir la misma predicción.
  **跨语言一致性。**两种语言中相同含义应产生相同预测――测量差距―― debe tener el mismo significado en dos idiomas.

> **【中文解读】**Este capítulo muestra cómo utilizar un marco maduro (como PyTorch、HuggingFace, etc.) para aplicar rápidamente esta tecnología. En los proyectos reales, se realiza con prioridad el uso de un marco experimentado, se pueden reducir errores y mejorar la eficiencia de desarrollo.

## Usalo con el marco de ejecución

La pila de 2026:

> Tecnología de 2026:

| Task / 任务 | Recommended / 推荐 |
|-----|-------------|
| Classification, 100 languages / 分类，100 种语言 | XLM-R-base (~270M) fine-tuned / 微调 |
| Zero-shot text classification / 零样本文本分类 | `joeddav/xlm-roberta-large-xnli` |
| Multilingual sentence embeddings / 多语言句子嵌入 | `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` |
| Translation, 200 languages / 翻译，200 种语言 | `facebook/nllb-200-distilled-600M` |
| Generative multilingual / 生成式多语言 | Claude, GPT-4, Aya-23, mT5-XXL |
| Low-resource language NLP / 低资源语言 NLP | XLM-V or domain-specific fine-tune / XLM-V 或领域微调 |

Siempre presupuestemos para ajustar el idioma objetivo si el rendimiento es importante.

> Si el rendimiento es importante, siempre se debe a un presupuesto de la lengua de destino.

### El impuesto a la tokenización.

Los modelos multilingües comparten un tokenizer en todos sus idiomas. Ese vocabulario se entrena en un corpus dominado por inglés, francés, español, chino, alemán. Para cualquier lengua fuera del conjunto dominante, tres impuestos se componen silenciosamente:

> El modelo de muchos idiomas es un lenguaje que se utiliza en el lenguaje de todos los idiomas.

- **Fertility tax.**Un texto de lenguaje de bajo recurso se tokeniza en mucho más tokens por palabra que en inglés. Una oración en hindi puede necesitar 3-5 veces los tokens de una oración en inglés equivalente.
  **繁殖税。**低资源语言文本每词分词成英语比很多的代币―― un indio语句可能需要等价英语句的3-5 veces más de代币――
- **Variant recovery tax.**Cada error de tipografía, variante diacrítica, desajuste de normalización de Unicode o variación de caso se convierte en una secuencia no relacionada de inicio en frío en el espacio de incorporación.
  **变体恢复税。**Cada error de redacción, cambio de símbolo, cambio de código, unificación, desajuste o cambio de escritura se convierte en una secuencia de inicio en frío en el espacio de inserción.
- **Capacity spillover tax.**Los impuestos 1 y 2 consumen posiciones de contexto, profundidad de capa y dimensiones de incrustación. Lo que queda para el razonamiento real es sistemáticamente menor.
  **容量溢出税。**税 1 和 2 消耗上下文位置、层深度和嵌入维度──留给实际推理的系统性地更小──

El síntoma práctico: su modelo se prepara normalmente en hindi, la curva de pérdida se ve correcta, la perplejidad de evaluación se ve razonable y los resultados de producción son sutilmente incorrectos. **You cannot data-scale your way out of a broken tokenizer.**

> 实际症状:模型在印地语上训练正常,损失曲线正确,评估困惑度合理, pero producción输出微妙地出错――**你无法通过数据扩展来修复损坏的分词器。**

Mitigations: elegir un tokenizer con buena cobertura para su lenguaje objetivo; verificar la fertilidad de tokenización en el texto objetivo retenido; utilizar fallback a nivel de byte para scripts de verdadera cola larga.

> 缓解措施: seleccionar un buen分词器 para el idioma objetivo; la tasa de reproducción de los textos objetivos que se hayan dejado; el regreso al nivel de los escritos escritos escritos en el actual lang尾书写.

> **【中文解读】**Este capítulo se centra en cómo se puede implementar el modelo como producto disponible. Desde el modelo original hasta el sistema de producción, se deben considerar múltiples dimensiones de optimización de rendimiento, tratamiento de errores, control, etc.

## Envíe el producto .

Salvo como`outputs/skill-multilingual-picker.md`¿Qué es esto ?

> 保存为                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `outputs/skill-multilingual-picker.md`¿Qué es esto ?

```markdown
---
name: multilingual-picker
description: Pick source language, target model, and evaluation plan for a multilingual NLP task.
version: 1.0.0
phase: 5
lesson: 18
tags: [nlp, multilingual, cross-lingual]
---

Given requirements (target languages, task type, available labeled data per language), output:

1. Source language for fine-tuning. Default English; check LANGRANK or qWALS if target language has a typologically close high-resource language.
2. Base model. XLM-R (classification), mT5 (generation), NLLB (translation), Aya-23 (generative LLM).
3. Few-shot budget. Start with 100-500 target-language examples if available.
4. Evaluation plan. Per-language accuracy, cross-lingual consistency, entity-level F1 on non-Latin scripts.

Refuse to ship a multilingual model without per-language evaluation. Flag scripts with low tokenization coverage as needing byte-fallback.
```

> **【中文解读】**Practice los temas de fácil/medio/duro  3 difficulty to pass in  Recomenda al menos completar los temas de grado medio  Grado duro  para la preparación de la entrevista

## Los ejercicios.

1. **Easy.**Ejecutar la línea de clasificación de disparos cero en 10 frases por idioma en inglés, francés, hindi y árabe.
   **简单。**En inglés, francés, hindi y árabe, el número de ejecuciones es de 10 por ciento.
2. **Medium.**Usar`paraphrase-multilingual-MiniLM-L12-v2`Para obtener información sobre los datos de los usuarios, se debe utilizar el código de acceso de los usuarios para crear un retriever interlingual sobre un pequeño corpus de idiomas mixtos.
   **中等。**构建跨语言检索器──用英语查询,检索任何语言的文档──测量回忆@5──
3. **Hard.**Comparar el ajuste de fuente inglesa y fuente hindi para una tarea de clasificación hindi. Reporte qué fuente produce una mejor precisión hindi. Esta es la tesis LANGRANK en miniatura.
   **困难。**Comparar las fuentes de inglés e indio con los efectos de las tareas de clasificación de idiomas indios.

> **【中文解读】**En el lenguaje de los términos "Lo que la gente dice" vs "Lo que realmente significa" se distingue entre el lenguaje diario y la definición técnica de significado.

## Términos clave .

| Term / 术语 | What people say / 人们常说的 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| Multilingual model（多语言模型） | One model, many languages / 一个模型多种语言 | Shared vocabulary and parameters across languages. / 跨语言共享词表和参数。 |
| Cross-lingual transfer（跨语言迁移） | Train on one, run on another / 训练一种，运行另一种 | Fine-tune on source, evaluate on target without target labels. / 在源语言微调，在目标语言评估。 |
| Zero-shot（零样本） | No target labels / 无目标标签 | Transfer without target-language fine-tuning. / 无目标语言微调的迁移。 |
| Few-shot（少样本） | Small target labels / 少量目标标签 | 100-500 target-language examples for fine-tuning. / 100-500 个目标语言样本。 |
| mBERT | First multilingual LM / 首个多语言 LM | 104-language BERT on Wikipedia. / 104 语言 BERT。 |
| XLM-R | Cross-lingual baseline / 跨语言基线 | 100-language RoBERTa on CommonCrawl. / 100 语言 RoBERTa。 |
| NLLB | 200-language MT / 200 语言 MT | No Language Left Behind. 55 low-resource languages. / 不让任何语言掉队。55 种低资源语言。 |

> **【中文解读】**延伸阅读 proporciona un alto nivel de recursos para el aprendizaje profundo. Estos artículos y cursos son los referentes clásicos en el campo, adecuados para los lectores que necesitan una comprensión profunda.

## Más Leer más Leer más

- [Conneau et al. (2019). XLM-R](https://arxiv.org/abs/1911.02116) el documento XLM-R. / XLM-R 论文。
- [Pires et al. (2019). How Multilingual is Multilingual BERT?](https://arxiv.org/abs/1906.01502) el análisis de transferencias translinguísticas.
- [Costa-jussà et al. (2022). No Language Left Behind](https://arxiv.org/abs/2207.04672) NLLB-200. / NLLB-200 论文。
- [Üstün et al. (2024). Aya Model](https://arxiv.org/abs/2402.07827) LLM multilingüe de Cohere.
- [Language Similarity Predicts Cross-Lingual Transfer (2026)](https://www.mdpi.com/2504-4990/8/3/65) QWALS / LANGRANK. / QWALS / LANGRANK 源语言论文。
