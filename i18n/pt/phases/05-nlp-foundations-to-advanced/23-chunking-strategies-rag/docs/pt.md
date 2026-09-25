# Estratégias de fragmentação para RAG

> A configuração de fragmentação influencia a qualidade da recuperação tanto quanto a escolha do modelo de incorporação (Vectara NAACL 2025).
> O impacto da configuração de blocos na qualidade de pesquisa é tão grande quanto a seleção de modelos de inserção.

> **【中文解读】**RAG 系统中,文档如何切分成块直接影响检索效果──

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 22 (Embedding Models), Phase 5 · 14 (IR & Search) | **前置知识:** Phase 5 · 22（嵌入模型），Phase 5 · 14（信息检索）
**Time:** ~60 minutes | **时间:** ~60 分钟

## O problema é o problema da introdução

A solução não é "comprar um melhor modelo de incorporação". A solução é fazer o pedaço corretamente. O artigo NAACL 2025 de Vectara mostrou que a estratégia de integração explica tanto a variação na qualidade de recuperação quanto a escolha de incorporação.

> O método de modificação não é "comprar um melhor modelo de inserção"― o método de modificação é o mesmo que o bloco de inserção― o artigo NAACL 2025 de Vectara mostra que a estratégia de inserção explica as diferenças de qualidade de pesquisa da mesma forma que a seleção de inserção―

> **【中文解读】**O ponto de partida é: como entender e aplicar esta técnica na prática de projeto.

Os benchmarks de fevereiro de 2026 mostram resultados surpreendentes: o chunking naívo de tamanho fixo com 100 tokens e 20 tokens superpondo a maioria das estratégias de chunking "inteligentes" em RAG de propósito geral.

> O teste de base de 2 de Fevereiro de 2026 mostrou resultados surpreendentes: simplesmente fixado grande pedaço de blocos ((100 tokens adicionados a 20 tokens sobrepostos) derrotou a maioria das estratégias de blocos inteligentes no General RAG.

## O conceito central.

> **【中文解读】**Este capítulo apresenta os conceitos e teorias fundamentais.

**Fixed-size chunking.**Dividir o texto em blocos de N-tokens com sobreposição opcional.

> **固定大小分块。**O texto é dividido em blocos de N tokens, selecionáveis.

**Sentence-level chunking.**Divida em limites de frases. Cada pedaço = uma ou mais frases. Boa para perguntas frequentes e recuperação de respostas curtas.

> **句子级分块。**Em parágrafos de limite de divisão. Cada bloco = um ou mais parágrafos.

**Semantic chunking.**Embed sentenças, agrupar sentenças consecutivas com inserções semelhantes em pedaços.

> **语义分块。**嵌入句子, será embutida similar连续句子分组为块── em texto narrativo melhor, calcular mais lentamente──

**Recursive character chunking.**Dividido por parágrafo, depois por frase, depois por caráter.

> **递归字符分块。**按段落分割,然后按句,然后按字符──LangChain 的默认──Good通用启发式──

> **【拓展：大语言模型的工程实践】**De GPT a ChatGPT, o campo de NLP passou por uma transição de "cada tarefa treinar um modelo" para "um modelo resolver todas as tarefas".

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) é a estrutura mais popular de aplicação de IA em empresas atuais.

> **【拓展：NLP 的多语言挑战】**No mundo há mais de 7000 idiomas, mas os estudos de PNL se concentram principalmente em inglês e em uma minoria de línguas.
```figure
n5-chunk-cuts
```

## Construí-lo

## Construí-lo e realizei-o.

> **【中文解读】**Este é o capítulo do código do zero implementar o algoritmo central.

### Passo 1: despejo de tamanho fixo com sobreposição

```python
def fixed_chunk(text, chunk_size=100, overlap=20):
    tokens = text.split()
    chunks = []
    for i in range(0, len(tokens), chunk_size - overlap):
        chunks.append(" ".join(tokens[i:i + chunk_size]))
    return chunks
```

### Passo 2: fragmentação semântica

```python
from sentence_transformers import SentenceTransformer
import numpy as np

def semantic_chunk(text, model_name="sentence-transformers/all-MiniLM-L6-v2", threshold=0.5):
    model = SentenceTransformer(model_name)
    sentences = text.split(". ")
    embeddings = model.encode(sentences, normalize_embeddings=True)
    chunks = [sentences[0]]
    for i in range(1, len(sentences)):
        sim = np.dot(embeddings[i], embeddings[i-1])
        if sim < threshold:
            chunks.append(sentences[i])
        else:
            chunks[-1] += ". " + sentences[i]
    return chunks
```

> **【中文解读】**Este capítulo mostra como usar um quadro de desenvolvimento rápido para aplicar esta tecnologia.

> **【拓展：Prompt Engineering 与 LLM 应用】**A Engenharia Prometida tornou-se a habilidade central de engenheiros de PNL.

## Use-o com o framework implementado.

> **【中文解读】**Este capítulo trata-se de como o modelo será implementado para produtos disponíveis.

| Strategy / 策略 | Chunk size / 块大小 | Best for / 最适合 |
|---------|---------|---------|
| Fixed / 固定 | 100-500 tokens | General purpose / 通用 |
| Sentence / 句子 | 1-3 sentences | FAQ, short answers / FAQ、短答案 |
| Semantic / 语义 | Variable / 可变 | Narrative, long docs / 叙述、长文档 |
| Recursive / 递归 | 500-1500 chars | LangChain default / LangChain 默认 |

## Envia-o . Produto .

Salva como`outputs/skill-chunking-picker.md`- Não .

> 保存为 `outputs/skill-chunking-picker.md`- Não .

```markdown
Given document type and retrieval task, pick chunking strategy and parameters.
1. Chunking method (fixed, sentence, semantic, recursive).
2. Chunk size and overlap.
3. Evaluation metric (retrieval recall@k, answer quality).
```

## Exercícios.

1. **Easy.**Implementar a despejo de tamanho fixo com sobreposição.**简单。**实现固定大小分块──测量检索质量──
2. **Medium.**Comparar o parcelação fixa vs semântica em um conjunto de dados narrativo. / **中等。**Em ensaios de dados, comparação fixa vs.
3. **Hard.**Construir um pipeline de fragmentação óptima que adapte o tamanho da peça por tipo de documento. / **困难。**Construção de arquivos tipo auto-adaptação blocos de grandeza de best分块流水线。

## Termos-chave .

| Term / 术语 | What it means / 含义 |
|------|-----------------------|
| Chunking（分块） | Splitting documents into retrievable units. / 将文档分割为可检索单元。 |
| Overlap（重叠） | Shared tokens between adjacent chunks. / 相邻块之间的共享 token。 |
| Semantic chunking（语义分块） | Group sentences by embedding similarity. / 按嵌入相似度分组句子。 |

## Mais leitura 延伸阅读

- [Vectara NAACL 2025 chunking study](https://vectara.com/blog/breaking-the-ice-chunking-strategies-for-rag) comparativo de fragmentos. / 分块基准。
- [LangChain text splitters](https://python.langchain.com/docs/modules/data_connection/document_transformers/) implementações em pedaços. / 分块实现。
