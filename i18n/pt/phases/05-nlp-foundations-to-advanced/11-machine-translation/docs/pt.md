# Tradução automática Tradução automática

> A tradução é a tarefa que pagou pela pesquisa de PNL durante trinta anos e continua a pagar agora.
> 翻译是为NLP研究买单三十年的任务,现在仍在继续──

> **【中文解读】**Desde统计机器翻译到神经机器翻译──现代用变压器──

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 10 (Attention Mechanism), Phase 5 · 04 (GloVe, FastText, Subword) | **前置知识:** Phase 5 · 10 (Attention Mechanism), Phase 5 · 04 (GloVe, FastText, Subword)
**Time:** ~75 minutes | **时间:** ~75 minutes


## O problema é o problema da introdução

Um modelo lê uma frase em uma língua e produz uma frase em outra. O comprimento varia. A ordem das palavras varia. Algumas palavras-fonte mapeam para múltiplas palavras-alvo e vice-versa. Idiomas recusam o mapeamento de um a um. "Eu te sinto saudável" em francês é "tu me manques"  literalmente "você me está faltando". Nenhum alinhamento de nível de palavras sobrevive a isso.
> 模型读取一语言的句子并产生另一语言的句子──长度不同──词序不同──一些源词映射到多个目标词,反之亦然──习语拒绝对一映射── "Eu sinto falta de você" é um termo francês que significa "tu me manques"  字面意思是"tu me as falta para mim"──没有词级对齐能经受受受此──

> **【中文解读】**A questão que se coloca neste capítulo é: como entender e aplicar esta tecnologia de forma correta na engenharia real.


A tradução automática é a tarefa que forçou a PNL a inventar codificadores-decodificadores, atenção, transformadores e, eventualmente, todo o paradigma LLM. Cada passo adiante chegou porque a qualidade da tradução era mensurável e a lacuna entre humano e máquina era teimosa.
> A tradução por máquina é a obrigação da PNL a desenvolver um codificador-descodificador, um transformador e, finalmente, a tarefa do modelo LLM. Cada passo é feito por causa da qualidade da tradução, que pode ser medida e que a diferença entre humanos e máquinas é constante.

Esta aula salta a aula de história e ensina o pipeline de trabalho de 2026: codificador-decodificador multilingue pré-treinado (NLLB-200 ou mBART), tokenização de subpalavras, pesquisa de feixe, avaliação BLEU e chrF, e o punhado de modos de falha que ainda enviam para a produção sem ser capturados.
> O estudo foi realizado em um estudo de estudos de ciências da biologia, que mostrou que a produção de dados em um determinado país é uma das principais causas de desenvolvimento de dados.

## O conceito central.

> **【中文解读】**Este capítulo apresenta os conceitos e teorias fundamentais.


![MT pipeline: tokenize → encode → decode with attention → detokenize](../assets/mt-pipeline.svg)
> ![MT 流水线：分词 → 编码 → 带注意力的解码 → 去分词](../assets/mt-pipeline.svg)

O MT moderno é um transformador encoder-decoder treinado em texto paralelo. O encoder lê a fonte em sua tokenization de linguagem. O decoder gera o alvo, uma subpalavra por vez, usando a saída do encoder através da atenção cruzada (leção 10).
> O MT moderno é um transformer treinado em textos comuns. O transformer é um transcriador. O transcriador é um transcriador. O transcriador é um transcriador. O transcriador é um transcriador.

Três opções operacionais impulsionam a qualidade do MT no mundo real.
> Três operações de transporte em todo o mundo

- **Tokenizer.**SentencePiece BPE treinado em um corpo de línguas mistas.
- **Model size.**NLLB-200 600M destilado cabe em um laptop. NLLB-200 3.3B é o padrão de produção publicado. 54.5B é o limite máximo de pesquisa.
- **Decoding.**Largura do feixe 4-5 para conteúdo geral. Penaltia de comprimento para evitar saída muito curta. Decodificação limitada quando você precisa de consistência terminológica.
> - **分词器。**O programa de formação em linguagem misturada é um dos principais programas de ensino de língua inglesa.
- **模型大小。**NLLB-200 蒸 600M 适合笔记本。NLLB-200 3.3B é já publicado produção默认。54.5B é研究天花板。
- **解码。**Gênero: Gênero: Gênero: Gênero: Gênero: Gênero: Gênero: Gênero: Gênero: Gênero: Gênero: Gênero: Gênero: Gênero: Gênero: Gênero: Gênero: Gênero: Gênero: Gênero: Gênero: Gênero: Gênero: Gênero: Gênero: Gênero: Gênero: Gênero: Gênero: Gênero: Gênero: Gênero: Gênero: Gênero: Gênero: Gênero: Gênero: Gênero: Gênero: Gênero: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên: Gên

> **【中文解读】**Este é um método de "desde zero" que ajuda a entender o princípio da estrutura, não é um problema que se encontra em uma caixa negra.

> **【拓展：大语言模型的工程实践】**De GPT a ChatGPT, o campo do NLP passou por uma transição de paradigma de "cada tarefa treinar um modelo" para "um modelo resolver todas as tarefas".

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) é a estrutura mais popular de aplicações de IA em empresas: fazer uma consulta de usuário antes de fazer uma consulta de documentos relacionados, e reapreciar o resultado da consulta como resposta de produção para o LLM.

> **【拓展：NLP 的多语言挑战】**No mundo todo, há mais de 7000 idiomas, mas os estudos de PNL se concentram principalmente em inglês e outras línguas.


## Construí-lo e realizei-o.
```figure
seq2seq-alignment
```

## Construí-lo

### Passo 1: chamada de MT pré-treinada
> Três coisas são importantes.`src_lang`Diga-me qual é o seu significado.`forced_bos_token_id`告诉解码器生成哪种语言── ambas são técnicas especiais da NLLB; mBART 和 M2M-100

```python
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

model_id = "facebook/nllb-200-distilled-600M"
tok = AutoTokenizer.from_pretrained(model_id, src_lang="eng_Latn")
model = AutoModelForSeq2SeqLM.from_pretrained(model_id)

src = "The cats are running."
inputs = tok(src, return_tensors="pt")

out = model.generate(
    **inputs,
    forced_bos_token_id=tok.convert_tokens_to_ids("fra_Latn"),
    num_beams=5,
    length_penalty=1.0,
    max_new_tokens=64,
)
print(tok.batch_decode(out, skip_special_tokens=True)[0])
```

```text
Les chats courent.
```

Três coisas importam aqui.`src_lang`diz ao tokenizer qual script e segmentação aplicar. `forced_bos_token_id`O M2M-100 e o mBART usam suas próprias convenções e não são intercambiáveis.
> BLEU 测出与参考之间的 n-gram 重叠──四种参考 n-gram 大小(1-4), 精确率几何平均,对过短输出的简洁惩罚──分数在 [0, 100]──常用但难解读:30 BLEU é "可用";40 é "好";50 é "出色";1 BLEU 以内差异是噪声──

### Passo 2: BLEU e chrF
> A sua capacidade de produção é de cerca de R$ 5 milhões.

BLEU mede sobreposição de n-gram entre saída e referência. Quatro tamanhos de n-gram de referência (1-4), média geométrica de precisões, penalidade de brevidade para saída muito curta. A pontuação é em [0, 100]. Comumente usado. Frustrante para interpretar: 30 BLEU é "utiliável"; 40 é "bom"; 50 é "excepcional"; diferenças abaixo de 1 BLEU são ruído.
> 始终使用 `sacrebleu`                                                                                                                                                                                                                                                              

A chrF mede a pontuação F de nível de caracteres. Mais sensível a linguagens morfologicamente ricas onde a subcontagem BLEU coincide.
> 现代 MT 评估使用三个互补的标标族―― pelo menos duas publicações――

```python
import sacrebleu

hypotheses = ["Les chats courent."]
references = [["Les chats courent."]]

bleu = sacrebleu.corpus_bleu(hypotheses, references)
chrf = sacrebleu.corpus_chrf(hypotheses, references)
print(f"BLEU: {bleu.score:.1f}  chrF: {chrf.score:.1f}")
```

Sempre usar`sacrebleu`A normalização da tokenização, para que as pontuações sejam comparáveis em todos os papéis, é a forma como os valores de referência enganosos acontecem.
> - **启发式**(BLEU、chrF)──快速、基于参考、可解释、对释义不敏感──用于遗留比较和归归检测──
- **学习型**(COMET、BLEURT、BERTScore) ⋅ Modelo de neurônios treinados em julgamento humano; comparação tradução com origem e semelhança de significado de referência ⋅ COMET Desde 2023 anos, está associado ao MT, é a produção preferencial de qualidade importante de 2026 anos ⋅
- **LLM 评委**(sem referência)  Proposição: grande modelo em flu性、充分性、语调和文化适当性  GPT-4 评委在评分标准设计良好时与人类一致性约80%──用于没有参考的开放内容──

### A hierarquia de avaliação de três níveis (2026)
> 2026 `sacrebleu`Utilizado em BLEU e chrF,`unbabel-comet`Utilizado para COMET, LLM Utilizado para sinais finais voltados para humanos.

A avaliação MT moderna usa três famílias métricas complementares.
> 无参考指标(COMET-QE、BLEURT-QE、LLM 评委) Deixe-te avaliar a tradução sem referência, isto é muito importante para não existir referência tradução

- **Heuristic**Rapido, baseado em referências, interpretável, insensível à paráfrase.
- **Learned**(COMET, BLEURT, BERTScore). Modelos neurais formados em julgamento humano; comparação semântica da semelhança da tradução com a fonte e a referência. COMET tem a maior associação com a investigação MT desde 2023 e é o padrão de produção de 2026 quando a qualidade importa.
- **LLM-as-judge**(sem referência). Promover um modelo grande para avaliar traduções em termos de fluência, adequação, tom, adequação cultural. GPT-4-as-judge corresponde ao acordo humano em ~80% do tempo em que a rubrica é bem concebida.
> 80% do tempo pode fluir, o restante 20% vai ficar sem sucesso.

- A pilha prática de 2026:`sacrebleu`para BLEU e chrF, `unbabel-comet`Para o COMET, e um LLM solicitado para o sinal final de cara humana, calibre cada métrica em relação a 50-100 exemplos etiquetados por humanos antes de confiar nos dados de produção.
> - **幻觉。**模型发明源中没有的内容──在不熟的领域词汇中常见──症状:输出流但声称源没有陈述的事实──缓解: sobre a restrição do termo do domínio, sobre o conteúdo sob controle revisão artificial, sobre o controle de saída de entrada muito mais anormal──
- **偏离目标语言生成。**模型翻译成错误的语言――NLLB 在罕见语言对上出奇地容易出错――缓解:验证 `forced_bos_token_id`Não sempre usou linguagem de identificação de modelos de verificação de saída.
- **术语漂移。**"Inscrever" em "document 1" se transforma em "s'inscreir", em "document 2" se transforma em "creer un compte"── para a interface 文本和面向用户的字符串,一致性比原始质量更重要──缓解:词汇表约束解码或后编辑字典──
- **语体不匹配。**Para o conteúdo do cliente, isso geralmente é errado. Caution: Se o modelo é suportado, use o token do idioma como um suporte, ou em apenas um pequeno modelo no idioma oficial.
- **短输入长度爆炸。**非常短的输入句子经常产生过长的翻译,因为长度惩罚在约5源代币下面急剧下降──缓解:

As métricas sem referência (COMET-QE, BLEURT-QE, LLM-as-judge) permitem avaliar traduções sem referência, o que é importante para pares de línguas de cauda longa onde não existem traduções de referência.
> O modelo de pre-treinamento é de talento. O programa não é complexo:

### Passo 3: que falhas na produção
>  milhares de amostras de alta qualidade vencem centenas de milhares de milhares de amostras de rede de ruído                                                                                                                                                                                                                                                

O tubo de trabalho acima traduzirá fluentemente 80% do tempo e falhará silenciosamente os restantes 20%.

- **Hallucination.**O modelo invente conteúdo que não estava na fonte. Comum no vocabulário de domínio desconhecido. Sintoma: saída é fluente, mas afirma fatos que a fonte não declarou. Mitigation: decodificação limitada em termos de domínio, revisão humana de conteúdo regulamentado, monitoramento de saída muito mais tempo do que entrada.
- **Off-target generation.**O modelo traduz para a língua errada. A NLLB é surpreendentemente propensa a isso em pares de línguas raros.`forced_bos_token_id`e sempre decodificar com uma verificação de modelo de ID de língua na saída.
- **Terminology drift.**"Registrar" torna-se "s'inscrire" no documento 1 e "creer un compte" no documento 2. Para o texto da interface e as cadeias de uso, a consistência é mais importante do que a qualidade bruta.
- **Formality mismatch.**O modelo escolhe qual for a forma mais comum no treinamento. Para conteúdo voltado para o cliente, isso geralmente é errado. Mitigation: prefixo rápido com um token de formalidade se o modelo o suporta, ou ajustar um pequeno modelo em corpora-somente formais.
- **Length explosion on short input.**Frases de entrada muito curtas geralmente produzem traduções longas demais porque a penalidade de comprimento cai de um penhasco abaixo de ~ 5 tokens de fonte.

### Passo 4: ajuste fino para um domínio

Os modelos pré-treinados são generalistas. A tradução legal, médica ou de diálogo de jogos beneficia de forma mensurável de ajustes finos em dados paralelos de domínio.

```python
from transformers import Trainer, TrainingArguments
from datasets import Dataset

pairs = [
    {"src": "The defendant pleaded guilty.", "tgt": "L'accusé a plaidé coupable."},
]

ds = Dataset.from_list(pairs)


def preprocess(ex):
    return tok(
        ex["src"],
        text_target=ex["tgt"],
        truncation=True,
        max_length=128,
        padding="max_length",
    )


ds = ds.map(preprocess, remove_columns=["src", "tgt"])

args = TrainingArguments(output_dir="out", per_device_train_batch_size=4, num_train_epochs=3, learning_rate=3e-5)
Trainer(model=model, args=args, train_dataset=ds).train()
```

> **【中文解读】**Este capítulo mostra como usar um framework maduro (como PyTorch、HuggingFace etc) rápida aplicação desta tecnologia.


A qualidade dos dados de formação é a maior alavanca de produção.


> **【拓展：Prompt Engineering 与 LLM 应用】**A Engenharia Prometida tornou-se a habilidade central dos engenheiros de PNL. De zero-shot a poucos-shot, de cadeia de pensamento a reação, diferentes estratégias de orientação são aplicadas a diferentes cenários.

## Use-o com o framework implementado.

A pilha de produção de 2026 para MT:
> MT 生产技术:

| Use case | Recommended starting point |
|---------|---------------------------|
| Any-to-any, 200 languages | `facebook/nllb-200-distilled-600M` (laptop) or `nllb-200-3.3B` (production) |
| English-centric, high quality, 50 languages | `facebook/mbart-large-50-many-to-many-mmt` |
| Short runs, cheap inference, English-French/German/Spanish | Helsinki-NLP / Marian models |
| Latency-critical browser-side | ONNX-quantized Marian (~50 MB) |
| Maximum quality, willing to pay | GPT-4 / Claude / Gemini with translation prompts |
> ♪ Use a cena ♪ Recomenda-se a começar ♪
|---------|---------|
| 任意到任意，200 种语言 | `facebook/nllb-200-distilled-600M`（笔记本）或 `nllb-200-3.3B`（生产） |
| 以英语为中心，高质量，50 种语言 | `facebook/mbart-large-50-many-to-many-mmt` |
| 短任务，廉价推理，英语-法语/德语/西班牙语 | Helsinki-NLP / Marian 模型 |
| 延迟敏感的浏览器端 | ONNX 量化的 Marian（约 50 MB） |
| 最高质量，愿意付费 | GPT-4 / Claude / Gemini 配合翻译提示 |

Os LLM agora superam os modelos especializados de MT em vários pares de idiomas a partir de 2026, particularmente no conteúdo idiomático e longo contexto. A troca é o custo por token e a latência. Escolha um LLM quando o comprimento do contexto, a consistência estilística ou a adaptação de domínio através de questões mais importantes do que o throughput.
> 截至2026年,LLM em várias línguas já ultrapassou os modelos MT especializados, especialmente no seu conteúdo e na sua duração.

> **【中文解读】**Este capítulo se concentra em como o modelo será implantado como produto disponível. De modelo original a nível de produção, os sistemas precisam considerar várias dimensões de otimização de desempenho, tratamento de erros, controle, etc.


## Envia-o . Produto .

Salva como`outputs/skill-mt-evaluator.md`- Não .
> 保存为 `outputs/skill-mt-evaluator.md`- Não .

```markdown
---
name: mt-evaluator
description: Evaluate a machine translation output for shipping.
version: 1.0.0
phase: 5
lesson: 11
tags: [nlp, translation, evaluation]
---

Given a source text and a candidate translation, output:

1. Automatic score estimate. BLEU and chrF ranges you would expect. State whether a reference is available.
2. Five-point human-verifiable check list: (a) content preservation (no hallucinations), (b) correct language, (c) register / formality match, (d) terminology consistency with glossary if provided, (e) no truncation or length explosion.
3. One domain-specific issue to probe. E.g., for legal: named entities and statute citations. For medical: drug names and dosages. For UI: placeholder variables `{name}`.
4. Confidence flag. "Ship" / "Ship with review" / "Do not ship". Tie to the severity of issues found in step 2.

> **【中文解读】** 练习题按照 Easy/Medium/Hard 三个难度递进。建议至少完成 Medium 级别的题目，Hard 级别适合深入研究或面试准备。


Refuse to ship a translation without a language-ID check on output. Refuse to evaluate without a reference unless the user explicitly opts in to reference-free scoring (COMET-QE, BLEURT-QE). Flag any content over 1000 tokens as likely needing chunked translation.
```

## Exercícios.

1. **Easy.**Traduza um parágrafo de 5 frases em inglês para o francês e de volta para o inglês usando `nllb-200-distilled-600M`- Medir o quão perto a viagem de ida e volta é do original.
2. **Medium.**Implementar uma verificação de identificação de língua nas saídas de tradução usando `fasttext lid.176`ou `langdetect`Integrar-se na chamada MT para que as gerações fora do alvo sejam capturadas antes de retornarem.
3. **Hard.**- A música é perfeita .`nllb-200-distilled-600M`A medida de BLEU em um conjunto de duração antes e depois de ajuste fino.
> 1. **简单。**Utilização `nllb-200-distilled-600M`将 5 句英语段落翻译成法语再翻回英语──测量往返与原文接近程度── você deve ver a palavra reservada mas com a palavra漂移──
2. **中等。**Utilização `fasttext lid.176`Ou `langdetect`实现翻译输出的语言识别检查──集成到MT调用中,在返回前捕获偏离目标语言的生成──
3. **困难。**Na sua escolha 5000 para o conteúdo do campo`nllb-200-distilled-600M`◊ Método de análise de dados em bloco de dados em bloco de dados em bloco de dados em bloco de dados em bloco de dados em bloco de dados em bloco de dados em bloco de dados em bloco de dados em bloco de dados em bloco de dados em bloco de dados em bloco de dados em bloco de dados em bloco de dados em bloco de dados em bloco de dados em bloco de dados em bloco de dados em bloco de dados em bloco de dados em bloco de dados em bloco de dados em bloco de dados em bloco de dados em bloco de dados em bloco de dados em bloco de dados em bloco de dados em bloco de dados em bloco de dados em bloco de dados em bloco de dados em bloco de dados em bloco de dados em bloco de dados em bloco de dados em bloco de dados em bloco de dados em bloco de dados em bloco de dados em bloco de dados em bloco de dados em bloco de dados em bloco de dados em bloco de dados em bloco de dados em bloco de dados em bloco de dados em bloco de dados em bloco de dados em bloco de dados em bloco de dados em bloco de dados em bloco de dados em bloco de dados em bloco de dados em bloco de dados em bloco de dados em bloco de dados em bloco de dados em bloco de dados em bloco de dados em bloco de bloco de dados.

> **【中文解读】**No 术语表中的"O que as pessoas dizem" vs "O que realmente significa" 区分日常口语和精确技术含义── em equipe,统一术语定义可以避免大量沟通误解──


## Termos-chave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| BLEU | Translation score | N-gram precision with brevity penalty. [0, 100]. |
| chrF | Character F-score | Character-level F-score. More sensitive for morphologically rich languages. |
| NMT | Neural MT | Transformer encoder-decoder trained on parallel text. The 2017+ default. |
| NLLB | No Language Left Behind | Meta's 200-language MT model family. |
| Constrained decoding | Controlled output | Force specific tokens or n-grams to appear / not appear in the output. |
| Hallucination | Invented content | Model output that is not supported by the source. |
> # O termo # Que as pessoas dizem # # O significado real #
|------|-----------|---------|
| BLEU | 翻译分数 | 带简洁惩罚的 n-gram 精确率。[0, 100]。 |
| chrF | 字符 F 分数 | 字符级 F 分数。对形态丰富语言更敏感。 |
| NMT | 神经机器翻译 | 在平行文本上训练的 Transformer 编码器-解码器。2017+ 的默认。 |
| NLLB | No Language Left Behind | Meta 的 200 语言 MT 模型系列。 |
| 约束解码 | 控制输出 | 强制特定 token 或 n-gram 出现/不出现在输出中。 |
| 幻觉 | 发明内容 | 模型输出中不被源支持的内容。 |

> **【中文解读】**延伸阅读 fornece recursos de alta qualidade para a aprendizagem profunda.


## Mais leitura 延伸阅读

- [Costa-jussà et al. (2022). No Language Left Behind: Scaling Human-Centered Machine Translation](https://arxiv.org/abs/2207.04672)O artigo da NLLB.
- [Post (2018). A Call for Clarity in Reporting BLEU Scores](https://aclanthology.org/W18-6319/)Porquê ?`sacrebleu`é a única forma correta de comunicar o BLEU.
- [Popović (2015). chrF: character n-gram F-score for automatic MT evaluation](https://aclanthology.org/W15-3049/)- o papel de chrF.
- [Hugging Face MT guide](https://huggingface.co/docs/transformers/tasks/translation) A prática de ajuste fino.
> - [Costa-jussà et al. (2022). No Language Left Behind: Scaling Human-Centered Machine Translation](https://arxiv.org/abs/2207.04672) NLLB 论文──
- [Post (2018). A Call for Clarity in Reporting BLEU Scores](https://aclanthology.org/W18-6319/)Porquê ?`sacrebleu`É a única forma correta de relatar o BLEU.
- [Popović (2015). chrF: character n-gram F-score for automatic MT evaluation](https://aclanthology.org/W15-3049/) chrF 论文──
- [Hugging Face MT guide](https://huggingface.co/docs/transformers/tasks/translation) 实用微调演练──
