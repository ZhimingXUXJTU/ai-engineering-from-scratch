# Avaliação de LLM  RAGAS, DeepEval, G-Eval  LLM  avaliação  RAGAS DeepEval

> A correspondência exata e a F1 não têm equivalência semântica. A revisão humana não é escalavel. LLM-as-judge é a resposta de produção  com calibração suficiente para confiar no número.
> 精确匹配和 F1 捕捉不到语义等价――exame artificial não pode ser expandido―LLM 作为评审是生产答案经过足够校准可以信任这个数字―

> **【中文解读】** avaliar a qualidade do LLM, incluindo os efeitos do RAG  Ragas  DeepEval  G-Eval 

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 23 (Chunking), Phase 5 · 14 (IR & Search) | **前置知识:** Phase 5 · 23（分块），Phase 5 · 14（信息检索）
**Time:** ~60 minutes | **时间:** ~60 分钟

## O problema é o problema da introdução

O sistema RAG responde: "29 de junho de 2007". A resposta de referência diz: "29 de junho de 2007". A correspondência exata diz errado. A BLEU diz parcial. Um humano diz certo. Você precisa de uma métrica que concorda com os humanos, escalas para milhares de saídas, e custa menos do que a anotação humana.

> Seu RAG 系统回答:"29 de junho de 2007"."" 参考答案是:"29 de junho de 2007"."" 精确匹配说错了。BLEU 说部分对──人类说正确──你需要一个与人类一致的量度,可扩展到数千输出,且成本低于人工标注──

> **【中文解读】**A questão que se coloca neste capítulo é: como entender e aplicar esta técnica na prática da construção.

Agora multiplica por 10.000 casos de teste. Multiplica novamente por cada atualização do modelo que você quer enviar. Avaliação humana não é escalado. Você precisa de métricas automatizadas que se correlacionam com o julgamento humano em r ≥ 0,85.

> Agora, multiplica-se em 10.000 casos de teste. Recompõe-se em cada modelo que você deseja publicar. Avaliação artificial não pode ser expandida.

## O conceito central.

> **【中文解读】**Este artigo apresenta os conceitos e as bases da teoria.

2026 tem três estruturas que possuem este problema.

> Em 2026 existem três quadros que regem este problema:

**RAGAS.**Avaliação RAG. Avaliação de recuperação + geração em conjunto. Métricas: fidelidade, relevância da resposta, precisão do contexto, recall de contexto.

> **RAGAS。**RAG  avaliação── avaliação conjunta procura e produção── indicador: fidelidade、 resposta 関連性、 上下文精确率、 上下文召回率──RAG 评估标准──

**DeepEval.**Estrutura de teste unitário para resultados de Mestrado em Direito Superior. Metricas: relevância da resposta, fidelidade, viés, toxicidade.

> **DeepEval。**O Mestrado em Matemática (LLM) 输出单元测试框架──指标:答案相关性、忠诚度、偏见、毒性──与 pytest 集成──
```figure
n5-judge-gauge
```

## Construí-lo

**G-Eval.**Cadeia de pensamento que incita a gerar critérios de avaliação, depois pontuação de resultados.

> **G-Eval。**Usar o pensamento para gerar critérios de avaliação, depois avaliar e emitir.

> **【拓展：大语言模型的工程实践】**O GPT foi transformado em um campo de discussão.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) é a estrutura mais popular de aplicação de IA em empresas atuais.

> **【拓展：NLP 的多语言挑战】**No mundo há mais de 7000 idiomas, mas os estudos de PNL se concentram principalmente em inglês e em uma minoria de línguas.

## Construí-lo e realizei-o.

> **【中文解读】**Este é o capítulo do código do zero implementar o algoritmo central.

```python
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision

# Evaluate RAG pipeline
results = evaluate(
    dataset=rag_dataset,
    metrics=[faithfulness, answer_relevancy, context_precision],
    llm=judge_llm,
    embeddings=embed_model,
)
print(results)
```

```python
from deepeval import assert_test
from deepeval.metrics import FaithfulnessMetric

metric = FaithfulnessMetric(threshold=0.7, model="gpt-4")
assert_test(test_case, [metric])
```

> **【中文解读】**Este capítulo mostra como usar um quadro de desenvolvimento rápido para aplicar esta tecnologia.

> **【拓展：Prompt Engineering 与 LLM 应用】**A Engenharia Prometida tornou-se a habilidade central de engenheiros de PNL.

## Use-o com o framework implementado.

> **【中文解读】**Este capítulo trata-se de como o modelo será implementado para produtos disponíveis.

| Framework / 框架 | Focus / 重点 | Best for / 最适合 |
|---------|--------|---------|
| RAGAS | RAG evaluation / RAG 评估 | Retrieval + generation / 检索 + 生成 |
| DeepEval | Unit testing / 单元测试 | CI/CD integration / CI/CD 集成 |
| G-Eval | Research / 研究 | Custom metrics / 自定义指标 |

## Envia-o . Produto .

Salva como`outputs/skill-llm-eval.md`- Não .

> 保存为 `outputs/skill-llm-eval.md`- Não .

```markdown
Given an LLM application (chatbot, RAG, agent), design evaluation pipeline.
1. Framework (RAGAS, DeepEval, G-Eval).
2. Metrics to track.
3. Calibration against human labels.
```

## Exercícios.

1. **Easy.**Avaliação de um simples gasoduto RAG com RAGAS. / **简单。**Utilize RAGAS  avaliação simples RAG 流水线──
2. **Medium.**Construir uma suite de testes DeepEval para um chatbot.**中等。**Por causa do seu trabalho, ele foi um dos principais autores do projeto.
3. **Hard.**Calibra o LLM como juiz contra 200 rótulos humanos.**困难。**Utilizando 200 个人类标签校准 LLM 评审――报告相关性――

## Termos-chave .

| Term / 术语 | What it means / 含义 |
|------|-----------------------|
| RAGAS | RAG evaluation framework. / RAG 评估框架。 |
| Faithfulness（忠实度） | Answer is supported by context. / 答案有上下文支持。 |
| LLM-as-judge | LLM evaluates other LLM outputs. / LLM 评估其他 LLM 输出。 |

## Mais leitura 延伸阅读

- [RAGAS](https://docs.ragas.io/) Marco de avaliação do RAG. / RAG  avaliação quadro。
- [DeepEval](https://docs.confident-ai.com/) Testes de unidade de LLM. / LLM 单元测试。
- [G-Eval](https://arxiv.org/abs/2303.16634) avaliação de cadeia de pensamento. / 思维链评估。
