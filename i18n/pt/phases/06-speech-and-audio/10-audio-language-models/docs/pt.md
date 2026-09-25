# Modelos de áudio-língua  Qwen2.5 Omni, Áudio Flamingo, GPT-4o Áudio 音频语言模型

> 2026 modelos de áudio-língua raciocinam sobre fala + som ambiental + música. Qwen2.5-Omni-7B combina GPT-4o Audio no MMAU-Pro. Audio Flamingo Next bate Gemini 2.5 Pro no LongAudioBench. A diferença entre aberta e fechada é essencialmente fechada  exceto em tarefas de áudio múltipla, onde todos são quase aleatórios.

> **【中文解读】**O modelo de linguagem de rádio de 2026 pode ser entendido como um sistema de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio de rádio

> **【拓展：音频大模型的新时代】**O modelo de linguagem de rádio vai expandir a capacidade de pensamento do LLM para o campo de rádio, capaz de simultaneamente compreender o conteúdo do idioma, identificar o ambiente, som, análise da estrutura musical.

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 04 (ASR), Phase 12 · 03 (Vision-Language Models), Phase 7 · 10 (Audio Transformers) | **前置知识:** 阶段 6 · 04（ASR），阶段 12 · 03（视觉语言模型），阶段 7 · 10（音频 Transformer）
**Time:** ~45 minutes | **预计用时:** ~45 分钟

## O problema é o problema da introdução

Você tem 5 segundos de áudio: ladrões de cães, alguém grita "para!", depois silêncio.

> Você tem 5 segundos de voz: cão grita, alguém grita "pare!", então é silencioso.

> **【中文解读】**A questão que se coloca neste capítulo é: como entender e aplicar esta tecnologia de forma correta na engenharia real.

- **Transcription.**"O que foi dito?"  Território da ASR.
  **转录。**"Dizei o quê?"
- **Semantic reasoning.**"A pessoa está em perigo?"  requer compreensão conjunta do ladrão + grito + silêncio.
  **语义推理。**"Este homem é perigoso?"
- **Music reasoning.**"Que instrumentos tocam a melodia?"
  **音乐推理。**"Que instrumento toca melodia?"
- **Long-audio retrieval.**"Em que lugar nesta palestra de 90 minutos o instrutor explicou a descida de gradientes?"
  **长音频检索。**"Neste discurso de 90 minutos, onde o professor explicou a queda do gradiente?"

Um único modelo que responde a todos estes com um único pedido é um **audio-language model**(LALM / ALM). Separado da ASR pura: LALM produz respostas em forma livre em língua natural, não apenas transcrições.

> Com um único sugestão, responder a todas estas perguntas é um único modelo.**音频语言模型**(LALM / ALM) 区别于纯 ASR:LALM 生成自由形式的自然语言答案, não apenas é um texto transcrito

## O conceito central.

> **【中文解读】**Este capítulo apresenta os conceitos e teorias fundamentais.


![Audio-language model: audio encoder + projector + LLM decoder](../assets/alm-architecture.svg)

### O modelo de três componentes

Cada 2026 LALM tem o mesmo esqueleto:

> ### 3 componentes

> Em 2026 cada LAM tem a mesma estrutura:

1. **Audio encoder.**Encoder de sussurros · BEATs · CLAP · WavLM · ou um encoder personalizado por modelo.
   **音频编码器。**Whisper 编码器 · BEATs · CLAP · WavLM · 或每个模型的自定义编码器──
2. **Projector.**O áudio-encoder de ponte linear ou MLP funciona no espaço de incorporação de tokens do LLM.
   **投影器。**A rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede de rede
3. **LLM.**Llama / Qwen / Gemma baseado em decodificador. Toma texto entrelaçado + tokens de áudio; gera texto.
   **LLM。**Baseado em Llama / Qwen / Gemma 的解码器──接收交织的文本 + 音频代币;生成文本──

Formação:

> 訓練:

- **Stage 1.**Encoder de congelação + LLM; projétor de trem apenas em dados de ASR / legendas.
  **阶段 1。**结编码器 + LLM; apenas em ASR/标注数据上训练投影器──
- **Stage 2.**A sintonia completa / LoRA para as tarefas de áudio que seguem instruções (QA, raciocínio, compreensão musical).
  **阶段 2。**Em instrução seguir a tarefa de som (QA、推理、音乐理解) para realizar o total de parametros / LoRA 微调──
- **Stage 3 (optional).**A voz-in / voz-out adiciona um decodificador de voz. Qwen2.5-Omni e AF3-Chat fazem isso.
  **阶段 3（可选）。**语音入/语音出添加语音解码器──Qwen2.5-Omni 和 AF3-Chat 实现了这一点──

### Mapa modelo de 2026

> ### Mapa de modelos de 2026

| Model | Backbone | Audio encoder | Output modality | Access |
|-------|----------|---------------|-----------------|--------|
| Qwen2.5-Omni-7B | Qwen2.5-7B | Custom + Whisper | text + speech | Apache-2.0 |
| Qwen3-Omni | Qwen3 | Custom | text + speech | Apache-2.0 |
| Audio Flamingo 3 | Qwen2 | AF-CLAP | text | NVIDIA non-commercial |
| Audio Flamingo Next | Qwen2 | AF-CLAP v2 | text | NVIDIA non-commercial |
| SALMONN | Vicuna | Whisper + BEATs | text | Apache-2.0 |
| LTU / LTU-AS | Llama | CAV-MAE | text | Apache-2.0 |
| GAMA | Llama | AST + Q-Former | text | Apache-2.0 |
| Gemini 2.5 Flash/Pro (closed) | Gemini | proprietary | text + speech | API |
| GPT-4o Audio (closed) | GPT-4o | proprietary | text + speech | API |

| 模型 | 骨干 | 音频编码器 | 输出模态 | 访问方式 |
|------|------|-----------|---------|---------|
| Qwen2.5-Omni-7B | Qwen2.5-7B | 自定义 + Whisper | 文本+语音 | Apache-2.0 |
| Qwen3-Omni | Qwen3 | 自定义 | 文本+语音 | Apache-2.0 |
| Audio Flamingo 3 | Qwen2 | AF-CLAP | 文本 | NVIDIA 非商业 |
| Audio Flamingo Next | Qwen2 | AF-CLAP v2 | 文本 | NVIDIA 非商业 |
| SALMONN | Vicuna | Whisper + BEATs | 文本 | Apache-2.0 |
| LTU / LTU-AS | Llama | CAV-MAE | 文本 | Apache-2.0 |
| GAMA | Llama | AST + Q-Former | 文本 | Apache-2.0 |
| Gemini 2.5 Flash/Pro（闭源） | Gemini | 专有 | 文本+语音 | API |
| GPT-4o Audio（闭源） | GPT-4o | 专有 | 文本+语音 | API |

### Verificação de realidade de referência (2026)

**MMAU-Pro.**1800 pares de QA que cobrem fala / som / música / mixado.

| Model | Overall | Speech | Sound | Music | Multi-audio |
|-------|---------|--------|-------|-------|-------------|
| Gemini 2.5 Pro | ~60% | 73.4% | 51.9% | 64.9% | ~22% |
| Gemini 2.5 Flash | ~57% | 73.4% | 50.5% | 64.9% | 21.2% |
| GPT-4o Audio | 52.5% | — | — | — | 26.5% |
| Qwen2.5-Omni-7B | 52.2% | 57.4% | 47.6% | 61.5% | ~20% |
| Audio Flamingo 3 | ~54% | — | — | — | — |
| Audio Flamingo Next | SOTA on LongAudioBench | — | — | — | — |

O **multi-audio column is damning for everyone.**A chance aleatória em 4 opções múltiplas = 25%; a maioria dos modelos pontua em torno disso.

> **多音频列对所有人都是致命的。**4 選 1 多選題的随机概率 = 25%; a maioria dos modelos obtém resultados por perto.

### Onde os LALM são úteis em 2026

- **Compliance audit of call-center recordings.**"O agente mencionou a divulgação necessária?"
  **合规审计通话录音。**"Customer é que tem a declaração de responsabilidade necessária?"
- **Accessibility.**Descreva eventos sonoros para usuários surdos (não apenas transcrição).
  **无障碍。**Por ouvir o usuário descrever o som do evento.
- **Content moderation.**Detectar linguagem violenta + tom ameaçador + contexto de fundo.
  **内容审核。**检测暴力语言 + 威胁语气 + 背景上下文──
- **Podcast / meeting chaptering.**Resumo semântico, não apenas as viradas do orador.
  **播客/会议章节化。**语义摘要, não apenas falar
- **Music catalog analysis.**"Encontre todas as faixas com uma mudança de chave da secção B".
  **音乐目录分析。**"Find out all B 段有转调曲目──"

### Quando não são (ainda) úteis

- Teoria da música de grãos finos (abaixo do nível de acordes).
  精细音乐理论(和弦级别以下) 』
- Raciocínio atribuído pelo orador em longas conversas (grados passados 10 minutos).
  长对话中的说话人归因推理 (também não há mais de 10 minutos de conversa)
- Comparar com áudio múltipla (22-26% é apenas acima do aleatório).
  O número de pessoas que estão em situação de risco é de 22 a 26%.
- Raciocínio de streaming em tempo real (a maioria são inferências de lote offline).
  实时流式推理 (a maioria é de lote de linha)

> **【中文解读】**Este é um método de "desde zero" que ajuda a entender o princípio da estrutura, não é um problema que se encontra em uma caixa negra.

> **【拓展：语音 AI 的产品化】**A tecnologia de voz enfrenta desafios únicos na produção: diferentes sons, ruídos de contexto, remoção de chamadas, conversas de pessoas, etc. Os produtos de Siri, Alexa, Pequeno Amor e outros são empregados em grande quantidade de engenharia para resolver esses "problemas de longo prazo".

> **【拓展：多语言语音技术】**As características do som de uma língua mundial são enormes: a alta densidade de voz de uma língua (como o chinês) é de baixa capacidade, a falta de dados de treinamento em linguagem.




## Construí-lo e realizei-o.
```figure
v4-alm-tokens
```

## Construí-lo

### Passo 1: consulta Qwen2.5-Omni

```python
from transformers import AutoModelForCausalLM, AutoProcessor

processor = AutoProcessor.from_pretrained("Qwen/Qwen2.5-Omni-7B")
model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-Omni-7B", torch_dtype="auto")

audio, sr = load_wav("clip.wav", sr=16000)
messages = [{
    "role": "user",
    "content": [
        {"type": "audio", "audio": audio},
        {"type": "text", "text": "What sounds do you hear, and what's happening?"},
    ],
}]
inputs = processor.apply_chat_template(messages, tokenize=True, return_tensors="pt")
output = model.generate(**inputs, max_new_tokens=200)
print(processor.decode(output[0], skip_special_tokens=True))
```

### Passo 2: padrão do projetor

```python
import torch.nn as nn

class AudioProjector(nn.Module):
    def __init__(self, audio_dim=1280, llm_dim=4096):
        super().__init__()
        self.down = nn.Linear(audio_dim, llm_dim)
        self.act = nn.GELU()
        self.up = nn.Linear(llm_dim, llm_dim)

    def forward(self, audio_features):
        return self.up(self.act(self.down(audio_features)))
```

É isso. O projetor é geralmente de 1-3 camadas lineares. Treinar-o em pares ASR (audio → transcrição) é a tarefa de pretexto de estágio 1.

### Passo 3: análise comparativa MMAU / LongAudioBench

```python
from datasets import load_dataset
mmau = load_dataset("MMAU/MMAU-Pro")

correct = 0
for item in mmau["test"]:
    answer = call_model(item["audio"], item["question"], item["choices"])
    if answer == item["correct_choice"]:
        correct += 1
print(f"Accuracy: {correct / len(mmau['test']):.3f}")
```

> **【中文解读】**Este capítulo mostra como usar um framework maduro (como PyTorch、HuggingFace etc) rápida aplicação desta tecnologia.


Relacione por categoria (discurso / som / música / multi-audio) separadamente.




> **【拓展：语音与情感计算】**语音 não apenas transmite informações escritas, mas também carrega um rico sinal emocional (语调、语速、音高变化) ◦情感语音识别 (语调、语速、音高变化) ◦情感语音识别 (语音识别, speech emotion recognition, SER) tem uma ampla aplicação em áreas como o controle de qualidade de clientes, a monitorização de saúde mental, a educação inteligente e outras.

## Use-o com o framework implementado.

| Task | 2026 pick |
|------|-----------|
| Free-form audio QA (open) | Qwen2.5-Omni-7B |
| Best open on long audio | Audio Flamingo Next |
| Best closed | Gemini 2.5 Pro |
| Voice-in / voice-out agent | Qwen2.5-Omni or GPT-4o Audio |
| Music reasoning | Audio Flamingo 3 or 2 (music-specialized AF-CLAP) |
| Call-center audit | Gemini 2.5 Pro via API, with RAG over your policy docs |

| 任务 | 2026 年选择 |
|------|-----------|
| 自由格式音频 QA（开源） | Qwen2.5-Omni-7B |
| 最佳开源长音频 | Audio Flamingo Next |
| 最佳闭源 | Gemini 2.5 Pro |
| 语音入/语音出智能体 | Qwen2.5-Omni 或 GPT-4o Audio |
| 音乐推理 | Audio Flamingo 3 或 2（音乐专用 AF-CLAP） |
| 呼叫中心审计 | Gemini 2.5 Pro via API，配合策略文档 RAG |



## Encurralagens

> 常见陷

- **Over-trust on multi-audio.**Se a sua tarefa precisa de "qual clip tem X", o desempenho aleatório é real.
  **过度信任多音频。**Se a sua missão precisa de "qual é o número X", o desempenho horizontal é real.
- **Long-audio degradation.**Após 10 minutos, a atribuição de alto-falantes da maioria dos modelos se rompe.
  **长音频退化。**超过 10 分钟, maioria dos modelos de discurso 归因失效──先做日志化(第 6 课),再总结──
- **Hallucinations on silence.**O mesmo problema do Whisper herdado pelos LALM que usam o codificador Whisper.
  **静音上的幻觉。**O problema é o mesmo que o problema do Whisper ︎.
- **Benchmark cherry-picking.**Postes de blog de vendedores destacam categorias de melhor caso.
  **基准挑挑拣拣。**供应商博客文章突出最佳类别──自运行 MMAU-Pro 多音频子集──

> **【中文解读】**Este capítulo se concentra em como o modelo será implantado como produto disponível. De modelo original a nível de produção, os sistemas precisam considerar várias dimensões de otimização de desempenho, tratamento de erros, controle, etc.


## Envia-o . Produto .

Salva como`outputs/skill-alm-picker.md`. Selecione LALM + subconjunto de referência + modalidade de saída (texto vs fala) para uma determinada tarefa de compreensão de áudio.

> 保存为 `outputs/skill-alm-picker.md`◊ For given audio频理解任务选择 LALM + 基准子集 + 输出模态(文本 vs 语音) ◊

## Exercícios.

1. **Easy.**Corra .`code/main.py`para ver um padrão de projetor de brinquedo + roteamento LALM falso de (audio-embed, tokens de texto) → tokens de saída.
   **简单。**运行 `code/main.py`查看玩具投影器模式 + 假 LALM 路由(音频嵌入,文本代币)→ 输出代币──
2. **Medium.**Ponha o Qwen2.5 Omni-7B em 100 pontos de fala do MMAU-Pro.
   **中等。**Em 100 MMAU-Pro 语音项上评分 Qwen2.5-Omni-7B──与论文报告的数字比较──
3. **Hard.**Construa uma linha de base de captura de áudio mínima: BEATs encoder + projétor de 2 camadas + congelado Llama-3.2-1B. Ajuste perfeitamente apenas o projétor em AudioCaps. Compare com SALMONN em Clotho-AQA.
   **困难。**构建最小音频标注基线:BEATs 编码器 + 2 层投影器 + 结 Llama-3.2-1B──仅在AudioCaps 上微调投影器──在Clotho-AQA 上与SALMONN比较──

> **【中文解读】**No 术语表中的"O que as pessoas dizem" vs "O que realmente significa" 区分日常口语和精确技术含义── em equipe,统一术语定义可以避免大量沟通误解──


## Termos-chave .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| LALM | Audio ChatGPT | Audio encoder + projector + LLM decoder. |
| Projector | Adapter | Small MLP mapping audio features into LLM embedding space. |
| MMAU | The benchmark | 10k audio-QA pairs across speech, sound, music. |
| MMAU-Pro | Harder MMAU | 1800 multi-audio / reasoning-heavy questions. |
| LongAudioBench | Long-form eval | Multi-minute clips with semantic queries. |
| Voice-in / voice-out | Speech-native | Model ingests speech and emits speech without text detour. |

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| LALM | 音频 ChatGPT | 音频编码器 + 投影器 + LLM 解码器。 |
| 投影器 | 适配器 | 将音频特征映射到 LLM 嵌入空间的小型 MLP。 |
| MMAU | 那个基准 | 跨语音、声音、音乐的 1 万音频-QA 对。 |
| MMAU-Pro | 更难的 MMAU | 1800 个多音频/重推理问题。 |
| LongAudioBench | 长音频评估 | 带语义查询的多分钟片段。 |
| 语音入/语音出 | 原生语音 | 模型直接接收和输出语音，不经文本。 |

> **【中文解读】**延伸阅读 fornece recursos de alta qualidade para a aprendizagem profunda.


## Mais leitura 延伸阅读

- [Chu et al. (2024). Qwen2-Audio](https://arxiv.org/abs/2407.10759)Arquitetura de referência.
  Chu 等 (2024). Qwen2-Audio参考架构──
- [Alibaba (2025). Qwen2.5-Omni](https://huggingface.co/Qwen/Qwen2.5-Omni-7B)- O discurso-em-discurso.
  Alibaba (2025). Qwen2.5-Omni语音入语音出。
- [NVIDIA (2025). Audio Flamingo 3](https://arxiv.org/abs/2507.08128)O líder de áudio aberto.
  NVIDIA (2025). Áudio Flamingo 3开源长音频领先者──
- [NVIDIA (2026). Audio Flamingo Next](https://arxiv.org/abs/2604.10905) LongAudioBench SOTA.
  NVIDIA (2026). Áudio Flamingo PróximoLongAudioBench SOTA──
- [Tang et al. (2023). SALMONN](https://arxiv.org/abs/2310.13289)Pioneiro de duplo codificador.
  Tang 等 (2023). SALMONN双编码器先驱──
- [MMAU-Pro leaderboard](https://mmaubenchmark.github.io/) classificação ao vivo de 2026.
  MMAU-Pro 排行榜2026 年实时排名──

> **【中文解读】**延伸阅读 forneceu recursos de alta qualidade para a aprendizagem profunda, incluindo artigos, tutoriais e ferramentas.

