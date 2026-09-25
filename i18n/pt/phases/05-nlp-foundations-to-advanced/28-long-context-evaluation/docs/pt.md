# Avaliação de longo contexto  NIAH, RULER, LongBench, MRCR 长上下文评估  NIAH、RULER

> Gemini 3 Pro anuncia 10 milhões de tokens de contexto. Em 1 milhão de tokens, o MRCR de 8 agulhas cai para 26,3%. Publicado ≠ utilizável. Avaliação de longo contexto diz a capacidade real do modelo que você está enviando.
> O Gemini 3 Pro 宣称10M token 上下文──在1M token 时,8-needle MRCR 降至26.3%──宣称的 ≠可用──长上下文评估告诉你你正在部署模型的实际能力──

> **【中文解读】** avaliação do Mestrado em Direito em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Praça em Pra

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 27 (LLM Evaluation) | **前置知识:** Phase 5 · 27（LLM 评估）
**Time:** ~45 minutes | **时间:** ~45 分钟

## O problema é o problema da introdução

Esta é a diferença de capacidade de contexto de 2026. As folhas de especificações dizem 1M tokens. Os indicadores de referência dizem: em tokens 100K, a precisão de recuperação cai 15-40%. Em 500K, cai 40-70%. O modelo não "vede" tudo na janela de contexto igualmente.

> É a diferença de capacidade de carga de 2026 ano. O modelo não está na janela de carga de 100K.

> **【中文解读】**A questão que se coloca neste capítulo é: como entender e aplicar esta técnica na prática da construção.

A avaliação de longo contexto mede estes eixos: precisão de recuperação em várias profundidades, raciocínio multi-hop entre documentos e agregação sobre informações distribuídas.

> 长上下文评估测量这些轴: diversidade de profundidade de procura precision rate, multidisciplinaridade de documentos, assim como a concentração de informações distribuídas.

## O conceito central.

> **【中文解读】**Este artigo apresenta os conceitos e as bases da teoria.

**NIAH (Needle in a Haystack).**Insira um fato específico em um documento longo em várias posições. Peça ao modelo para recuperá-lo. Medidas: o modelo pode encontrar uma agulha na profundidade X em um monte de feno de tokens Y?

> **NIAH（大海捞针）。**Em cada posição do arquivo longueiro, inserir fatos específicos.

**RULER.**Extende a NIAH com tarefas de agulhas múltiplas, distância variável e agregação.

> **RULER。**扩展 NIAH 添加多针、可变距离和聚合任务──更全面──

**LongBench.**Tarefas de contexto longo do mundo real: resumo, QA, recuperação, código. Mais representativas do que benchmarks sintéticos.

> **LongBench。**O que é o que é um "computador" de um computador?

**MRCR (Multi-hop Reasoning over Context).**Raciocínio que requer a conexão de informações entre vários documentos.

> **MRCR（上下文多跳推理）。**需要跨多文档连接信息的推理──最难的长上下文测试──

> **【拓展：大语言模型的工程实践】**O GPT foi transformado em um campo de discussão.
```figure
gx-niah-decay
```

## Construí-lo

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) é a estrutura mais popular de aplicação de IA em empresas atuais.

> **【拓展：NLP 的多语言挑战】**No mundo há mais de 7000 idiomas, mas os estudos de PNL se concentram principalmente em inglês e em uma minoria de línguas.

## Construí-lo e realizei-o.

> **【中文解读】**Este é o capítulo do código do zero implementar o algoritmo central.

### Passo 1: teste simples de NIAH

```python
def needle_in_haystack(model, context_length, needle, needle_position):
    """Insert needle at position in a long document and test retrieval."""
    haystack = generate_irrelevant_text(context_length)
    full_text = haystack[:needle_position] + f"\n{needle}\n" + haystack[needle_position:]
    question = f"What is the secret fact hidden in the text?"
    response = model(full_text + "\n\n" + question)
    return needle.lower() in response.lower()
```

> **【中文解读】**Este capítulo mostra como usar um quadro de desenvolvimento rápido para aplicar esta tecnologia.

> **【拓展：Prompt Engineering 与 LLM 应用】**A Engenharia Prometida tornou-se a habilidade central de engenheiros de PNL.

## Use-o com o framework implementado.

> **【中文解读】**Este capítulo trata-se de como o modelo será implementado para produtos disponíveis.

| Benchmark / 基准 | Type / 类型 | Measures / 测量 |
|---------|------|---------|
| NIAH | Synthetic / 合成 | Single-fact retrieval at depth. / 深度单事实检索。 |
| RULER | Synthetic / 合成 | Multi-needle + aggregation. / 多针 + 聚合。 |
| LongBench | Real / 真实 | Practical long-context tasks. / 实用长上下文任务。 |
| MRCR | Synthetic / 合成 | Multi-hop reasoning. / 多跳推理。 |

## Envia-o . Produto .

Salva como`outputs/skill-long-context-eval.md`- Não .

> 保存为 `outputs/skill-long-context-eval.md`- Não .

```markdown
Given a model claiming long-context support, verify actual performance.
1. Context length to test.
2. Benchmarks to run (NIAH, RULER, LongBench).
3. Minimum acceptable accuracy at target length.
```

## Exercícios.

1. **Easy.**Execute NIAH em um modelo com tokens de 10K e 50K.**简单。**Em 10K e 50K tokens,
2. **Medium.**Construir um teste com várias agulhas, medir a recuperação de 5 fatos num contexto de 100K. / **中等。**构建多针测试──
3. **Hard.**Comparar 3 modelos no LongBench.**困难。**Em LongBench 上比较 3 个模型──

## Termos-chave .

| Term / 术语 | What it means / 含义 |
|------|-----------------------|
| NIAH（大海捞针） | Insert fact in long text, test retrieval. / 在长文本中插入事实，测试检索。 |
| Context window（上下文窗口） | Maximum input length a model can process. / 模型能处理的最大输入长度。 |
| Multi-hop reasoning（多跳推理） | Connect info across multiple documents. / 跨文档连接信息。 |

## Mais leitura 延伸阅读

- [NIAH original](https://arxiv.org/abs/2404.05460)- A agulha num palheiro.
- [RULER](https://arxiv.org/abs/2404.02372) referência de longo contexto alargada. / 扩展长上下文基准──
- [LongBench](https://arxiv.org/abs/2308.14508) tarefas de contexto longo do mundo real.
