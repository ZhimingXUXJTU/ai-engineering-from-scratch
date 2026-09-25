# Embedding Models  O 2026 Deep Dive  Embedding Models  Depth Resolution

> Word2Vec deu-lhe um vetor por palavra. Modelos modernos de incorporação dão-lhe um vetor por passagem, translingual, com vistas raras, densas e multi-vetor, dimensionadas para se adequarem ao seu índice. Escolha errado e o seu RAG recupera a coisa errada.
> Word2Vec  dá-lhe cada palavra um êmetro. Modelo moderno de inserção dá-lhe cada fragmento um êmetro, translanguagem, tem rara, intensa e multi-êmetro, grande para sua indicação.

> **【中文解读】**O modelo embuxado é o núcleo da pesquisa RAG e de linguagem.

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 03 (Word Embeddings), Phase 5 · 14 (IR & Search) | **前置知识:** Phase 5 · 03（词嵌入），Phase 5 · 14（信息检索）
**Time:** ~60 minutes | **时间:** ~60 分钟

## O problema é o problema da introdução

Escolher um incorporador em 2026 significa escolher entre cinco eixos: denso vs. espesso vs. multi-vector, monolingüe vs. multilingüe, tamanho do modelo, objetivo de treinamento e se ele se encaixa nas restrições de dimensão do seu banco de dados de vetores.

> 2026 Seleção de emplacamento significa que você deve escolher em cinco eixos: 密 vs 稀疏 vs 多向量、单语 vs 多语言、模型大小、训练目标、以及是否适合您的向量数据库尺寸约束──

> **【中文解读】**O ponto de partida é: como entender e aplicar esta técnica na prática de projeto.

## O conceito central.

> **【中文解读】**Este capítulo apresenta os conceitos e teorias fundamentais.

**Dense embeddings.**Vector único de tamanho fixo por texto (por exemplo, 768-dim de MiniLM). Rapido para comparação, bem comprimido, padrão em bancos de dados de vetores.

> **稠密嵌入。**Cada texto tem um grande volume fixo (como o MiniLM) 维 768 ⋅ Comparar rápido, comprimido, com base em dados de volume.

**Sparse embeddings.**Um peso por termo vocabulário (como um TF-IDF aprendido). SPLADE, BM25. Bom para consultas pesadas em palavras-chave.

> **稀疏嵌入。**Cada palavra expressa um peso especial (如学习的TF-IDF) ⋅SPLADE、BM25──适合关键词密集的查询──

**Multi-vector / ColBERT.**Um vetor por token, pontuação de interação tardia, índice mais preciso mas maior.

> **多向量 / ColBERT。**Cada token, um , um 延迟交互评分.

> **【拓展：大语言模型的工程实践】**De GPT a ChatGPT, o campo de NLP passou por uma transição de "cada tarefa treinar um modelo" para "um modelo resolver todas as tarefas".

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) é a estrutura mais popular de aplicação de IA em empresas atuais.

> **【拓展：NLP 的多语言挑战】**No mundo há mais de 7000 idiomas, mas os estudos de PNL se concentram principalmente em inglês e em uma minoria de línguas.

## Construí-lo e realizei-o.

> **【中文解读】**Este é o capítulo do código do zero implementar o algoritmo central.
```figure
gx-matryoshka
```

## Construí-lo

### Passo 1: comparação de modelos de incorporação

```python
from sentence_transformers import SentenceTransformer
import numpy as np

models = {
    "MiniLM": "sentence-transformers/all-MiniLM-L6-v2",
    "multilingual": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
}

query = "What is attention in transformers?"
docs = ["Self-attention computes weighted sums of values.", "The cat sat on the mat."]

for name, model_id in models.items():
    model = SentenceTransformer(model_id)
    q_emb = model.encode([query], normalize_embeddings=True)
    d_embs = model.encode(docs, normalize_embeddings=True)
    sims = (d_embs @ q_emb.T).flatten()
    print(f"{name}: {list(zip(docs, sims.round(3)))}")
```

> **【中文解读】**Este capítulo mostra como usar um quadro de desenvolvimento rápido para aplicar esta tecnologia.

> **【拓展：Prompt Engineering 与 LLM 应用】**A Engenharia Prometida tornou-se a habilidade central de engenheiros de PNL.

## Use-o com o framework implementado.

> **【中文解读】**Este capítulo trata-se de como o modelo será implementado para produtos disponíveis.

| Model / 模型 | Dim / 维度 | Best for / 最适合 |
|------|------|---------|
| all-MiniLM-L6-v2 | 384 | English, speed / 英语，速度 |
| paraphrase-multilingual-MiniLM-L12-v2 | 384 | Multilingual / 多语言 |
| BGE-large-en-v1.5 | 1024 | English accuracy / 英语准确率 |

## Envia-o . Produto .

Salva como`outputs/skill-embedding-picker.md`- Não .

> 保存为 `outputs/skill-embedding-picker.md`- Não .

```markdown
Given requirements (language, accuracy, latency, index size), pick the right embedding model.
1. Dense vs sparse vs multi-vector.
2. Model checkpoint.
3. Dimension and index budget.
```

## Exercícios.

1. **Easy.**Comparar MiniLM vs BGE numa tarefa de recuperação de 100 consultas. / **简单。**Em 100 tarefas de pesquisa comparar MiniLM vs BGE
2. **Medium.**Construir uma recuperação híbrida densa + espársia. / **中等。**Construção mistura + rare疏检索
3. **Hard.**Aponta um modelo de incorporação em pares específicos de domínio. / **困难。**Em áreas específicas para os modelos de inserção de micro-modelos.

## Termos-chave .

| Term / 术语 | What it means / 含义 |
|------|-----------------------|
| Dense embedding（稠密嵌入） | Fixed-size vector per text. / 固定大小向量。 |
| Sparse embedding（稀疏嵌入） | One weight per vocab term. / 每个词表项一个权重。 |
| ColBERT / multi-vector | One vector per token, late interaction. / 每个 token 一个向量。 |
| Hybrid search（混合搜索） | Combine dense + sparse retrieval scores. / 结合稠密+稀疏检索。 |

## Mais leitura 延伸阅读

- [MTEB Leaderboard](https://huggingface.co/spaces/mteb/leaderboard) embebedamento de referências. / 嵌入模型基准──
- [SPLADE](https://arxiv.org/abs/2109.10086) Embedings pouco aprendidos. / 稀疏学习嵌入──
- [ColBERT](https://arxiv.org/abs/2004.12832) Retorno tardío de interação. / 延迟交互检索。
