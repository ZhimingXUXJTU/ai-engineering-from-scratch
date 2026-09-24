# Enlace y desambiguación de entidades

> NER encontró "Paris". La entidad que vincula decide: París, Francia? Paris Hilton? Paris, Texas? Paris (el príncipe troyano)?
> En el caso de los Estados Unidos, el gobierno de la República Popular del Congo (DRC) ha adoptado una política de libre comercio y de libre comercio.

> **【中文解读】**La información de la NER se encuentra en la base de datos de la NER.

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 06 (NER), Phase 5 · 22 (Embedding Models) | **前置知识:** Phase 5 · 06（NER），Phase 5 · 22（嵌入模型）
**Time:** ~45 minutes | **时间:** ~45 分钟

## El problema es la introducción del problema

El enlace de entidades (EL) resuelve cada mención a una entrada única en una base de conocimientos (Wikidata, Wikipedia, GeoNames).

> 实体链接(EL) va a resolver cada uno de los nombres en la base de datos de Wikipedia, los nombres geográficos, los nombres geográficos y los datos de la Wikipedia.

> **【中文解读】**La pregunta planteada en este capítulo es: ¿cómo entender y aplicar correctamente esta técnica en el proyecto real?

## El concepto central.

> **【中文解读】**Este artículo presenta la base de los conceptos y teorías centrales.

**Candidate generation.**Dado que "Jordan", ¿qué entradas de KB coinciden? Utilice la coincidencia de cadenas, resolución redirigida y precedentes de popularidad.

> **候选生成。**给定 "Jordania", ¿qué conocimientos de la base de datos se ajustan?

**Disambiguation.**Clasificar candidatos por similitud de contexto. Bi-encoder para la velocidad, cross-encoder para la precisión. Contexto = texto circundante + descripción de entidad desde KB.

> **消歧。**按上下文相似度排名候选──双编码器用于速度,交叉编码器用于准确率──上下文 = 周围文本 + 知识库中的实体描述──

> **【拓展：大语言模型的工程实践】**Desde el GPT hasta el ChatGPT, el campo de la NLP ha experimentado un cambio de paradigma.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) es la arquitectura más popular de la aplicación de IA en las empresas actuales.

> **【拓展：NLP 的多语言挑战】**En todo el mundo hay más de 7000 idiomas, pero los estudios de PNL se centran principalmente en inglés y en una minoría de idiomas.

## Construye y realiza.

> **【中文解读】**Este capítulo pasa por el código desde el núcleo de algoritmos de implementación de cero.
```figure
gx-entity-linking
```

## Construye el mismo

### Paso 1: crear un índice de alias desde redirecciones de Wikipedia

```python
alias_to_entities = {
    "jordan": ["Q41421 (Michael Jordan)", "Q810 (Jordan, country)", "Q254110 (Michael B. Jordan)"],
    "paris":  ["Q90 (Paris, France)", "Q663094 (Paris, Texas)", "Q55411 (Paris Hilton)"],
    "apple":  ["Q312 (Apple Inc.)", "Q89 (apple, fruit)"],
}
```

Los datos de alias de Wikipedia: ~ 18M (alias, entidad) pares. Descargar desde los vertederos de Wikidata. Almacenar como índice invertido.

### Paso 2: Desambiguación basada en el contexto

```python
def entity_link(mention, context, kb_lookup, embed_model):
    candidates = kb_lookup.get(mention.lower(), [])
    if not candidates:
        return None
    ctx_emb = embed_model.encode([context])
    scores = []
    for cand in candidates:
        cand_emb = embed_model.encode([cand["description"]])
        scores.append((cand, float(np.dot(ctx_emb[0], cand_emb[0]))))
    return max(scores, key=lambda x: x[1])[0]
```

> **【中文解读】**Este capítulo muestra cómo utilizar un marco maduro para aplicar rápidamente esta tecnología.

> **【拓展：Prompt Engineering 与 LLM 应用】**La ingeniería rápida se ha convertido en la habilidad central de los ingenieros de PNL.

## Usalo con el marco de ejecución

> **【中文解读】**Este apartado se centra en cómo el modelo se desplegará en productos disponibles.

- **OpenTapioca.**EL ligero para Wikidata. / OpenTapioca。Wikidata 轻量 EL。
- **REL (Radboud Entity Linker).**Wikipedia de última generación EL. / REL。先进 Wikipedia EL。
- **GENRE.**Autoregresividad enlazando por Facebook. / GENRE。Facebook 自回归实体链接。
- **LLM prompting.**Pida al LLM que sea desambiguo.

## Envíe el producto .

Salvo como`outputs/skill-entity-linker.md`¿Qué es esto ?

> 保存为                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `outputs/skill-entity-linker.md`¿Qué es esto ?

```markdown
Given mentions from NER, link them to a knowledge base.
1. KB choice (Wikidata, Wikipedia, custom).
2. Candidate generation strategy.
3. Disambiguation method (embedding similarity, cross-encoder, LLM).
```

## Los ejercicios.

1. **Easy.**Construir un generador de candidatos basado en Wikipedia. / **简单。**构建基于维基百科的候选生成器──
2. **Medium.**Implementar desambiguación de bi-encoder y evaluar en un conjunto de pruebas. / **中等。**实现双编码器消歧──
3. **Hard.**Comparar EL basado en LLM con EL neuronal en un conjunto de datos multilingüe. / **困难。**En el conjunto de datos de varios idiomas, comparación entre LLM EL vs.

## Términos clave .

| Term / 术语 | What it means / 含义 |
|------|-----------------------|
| Entity linking（实体链接） | Map mentions to KB entries. / 将指称映射到知识库条目。 |
| Disambiguation（消歧） | Pick the correct entity among candidates. / 在候选中选择正确实体。 |
| Candidate generation（候选生成） | Retrieve possible KB matches for a mention. / 为指称检索可能的知识库匹配。 |

## Más Leer más Leer más

- [Wu et al. (2020). Scalable Zero-shot Entity Linking](https://arxiv.org/abs/1910.02854)/ 可扩展零样本实体链接──
- [De Cao et al. (2020). GENRE](https://arxiv.org/abs/1912.01572)/ 自回归实体链接──
