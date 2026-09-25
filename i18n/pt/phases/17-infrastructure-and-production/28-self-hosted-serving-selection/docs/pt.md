# Seleção de Servidores Autogestados  llama.cpp, Ollama, TGI, vLLM, SGLang ‬ 自托管 选择 服务 SGLang vLLM
# Seleção de serviço auto-hosted  Motor de correspondência para hardware e escala

> A seleção do motor é uma função de hardware, escala e ecossistema  não uma leitura de classificação. Quatro motores dominam a inferência auto-hostada em 2026: llama.cpp, Ollama, vLLM, SGLang, com TGI atrasado no modo de manutenção. **llama.cpp**é mais rápido em CPU  mais amplo suporte de modelo, controle total sobre quantização e threading. **Ollama**é a instalação de comando único de dev-laptop, ~ 15-30% mais lenta do que llama.cpp (serialização Go + CGo + HTTP), 3x diferença de throughput sob carga prod-like. **TGI entered maintenance mode December 11, 2025** apenas corrigem bugs, ~ 10% mais lento do que o vLLM, mas historicamente a observabilidade e a integração do ecossistema HF são superiores.**vLLM**é o padrão de produção de finalidade geral  v0.15.1 (fevereiro 2026) adiciona PyTorch 2.10, RTX Blackwell SM120, otimização H200. **SGLang**é o especialista em multi-turn / prefixo agencial pesado  400.000+ GPUs em produção (xAI, LinkedIn, Cursor, Oracle, GCP, Azure, AWS). Constraensões de hardware: CPU-first → llama.cpp. AMD / não NVIDIA → vLLM é o caminho mais forte-apoiado (TRT-LLM é bloqueado por NVIDIA). 2026 padrão de canalização: dev = Ollama, estagização = llama.cpp, prod = vLLM ou SGLang. Os motores assumem diferentes formatos de peso  GGUF para a família llama.cpp, HF safetensores para os motores GPU  para que uma conversão de formato possa ficar entre as etapas.

> **【中文解读】**Este capítulo apresenta a comparação e a seleção de sistemas de gestão automática.


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, engine-decision tree walker) | **语言:** Python
**Prerequisites:** All Phase 17 lessons covering engines (04, 06, 07, 09, 18) | **前置知识:** All Phase 17 lessons covering engines (04, 06, 07, 09, 18)

> - Não .**【前置】**Este é o capítulo 17 do curso de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia de Engenharia.
> - Não .**【类比】**Autotúbal motor = "AI 服务器品牌"―llama.cpp = CPU 王者(最广模型支持、量化全控制);Ollama = 笔记本一键安装(比 llama.cpp 慢 15-30%);TGI 已进入维护模式(2025.12.11) 修改 bug,新项目别选;vLLM = 通用生产默认(v0.15.1+ PyTorch 2.10+Blackwell);SGLang = Agente 多轮+前万密集专家(40+ GPU 在 xAI/LinkedIn/Cursor) ⋅
> 🤔 **【困惑】**P: 我的场景该选哪个? CPU-only→llama.cpp;AMD/非 NVIDIA→vLLM(TRT-LLM 锁 NVIDIA);Agente 多轮→SGLang;通用→vLLM。2026 流水线:dev=Ollama、staging=llama.cpp、prod=vLLM/SGLang,全用 GGUF/HF 权重一致。
**Time:** ~45 minutes | **时间:** ~45 minutes

## Objetivos de aprendizagem

- Escolha um motor dado hardware (CPU / AMD / NVIDIA Hopper / Blackwell), escala (1 usuário / 100 / 10,000), e carga de trabalho (chat geral / agente / longo contexto).
  Tradução do inglês para tradução livre: given determined hardware (CPU/AMD/NVIDIA Hopper/Blackwell)
- Cite o status de modo de manutenção TGI 2026 (11 de dezembro de 2025) e por que ele desvia novos projetos para vLLM ou SGLang.
  Chinese:  维护模式状态 (título original)  维护模式状态 (título original)   维护模式状态 (título original)                                                                                                                                                                                                                                           
- Descrever o gasoduto de desenvolvimento/estagem/produtor utilizando os mesmos pesos GGUF ou HF em toda a direcção.
  Tradução em inglês: description of the use of the same GGUF or HF during the entire life cycle 权重的开发/预发布/生产流水线──
- Explique por que "apenas o CPU" força llama.cpp e "AMD" exclui o TRT-LLM.
  Tradução do idioma: explica por que "só CPU" forçou o uso de llama.cpp enquanto "AMD" excluiu TRT-LLM。

## O problema é o problema da introdução

> **【中文解读】**A seleção do motor de cálculo depende de três dimensões: hardware (CPU / AMD / NVIDIA Hopper / Blackwell)  tamanho ((1 usuário / 100 / 10,000)  trabalho de carga ((通用聊天 / Agent / 长上下文)  2025 ano 12 月 11 日 HuggingFace TGI 进入维护模式 ((só bug fix), o que torna o novo projeto deve ser concebido para longe do TGI, virar para vLLM ou SGLang.
- Descrever o processo de desenvolvimento/estagem/produtor, incluindo onde uma conversão de formato GGUF em safetensores se situa entre as fases.
- Explique por que "CPU-first" aponta para llama.cpp e "AMD" exclui TRT-LLM.

> **【拓展：2026 年推理引擎选择决策】**2026 年推理引擎的硬件优先决策树:(1) CPU-only → llama.cpp(唯一有竞争力的选项);(2) AMD GPU → vLLM(ROCm 支持),TRT-LLM 不支持 AMD;(3) NVIDIA Hopper → vLLM 或 SGLang 或 TRT-LLM(三选一);(4) NVIDIA Blackwell → TRT-LLM 吞吐最高;(5) Apple Silicon → llama.cpp(Metal 后端) △ 尺寸决策:1 用户→Ollama,10-100→LLM 单,100-10K→LLM produção-stack 或 SangGL,10K+→production-stack + 分离式 + LMC。

A sua equipe inicia um novo projeto de LLM auto-anfitrião. Um engenheiro diz Ollama, outro diz vLLM, um terceiro diz "o TGI não funciona fora da caixa?" Todos os três são adequados para diferentes contextos. Nenhum é adequado para todos.

Em 2026, a árvore de escolha importa: hardware primeiro, escala segunda, carga de trabalho terceira. E um evento específico de 2025  TGI entrando no modo de manutenção 11 de dezembro  altera o padrão para novos projetos.

## O conceito central.

### Os cinco motores

| Engine | Best for | Notes |
|--------|----------|-------|
| **llama.cpp** | CPU / edge / minimal deps / widest model support | Fastest on CPU, full control |
| **Ollama** | Dev laptops, single user, one-command install | 15-30% slower than llama.cpp; 3x prod throughput gap |
| **TGI** | HF ecosystem, regulated industries | **Maintenance mode Dec 11, 2025** |
| **vLLM** | General-purpose production, 100+ users | Broad production default; v0.15.1 Feb 2026 |
| **SGLang** | Agentic multi-turn, prefix-heavy workloads | 400,000+ GPUs in production |

### Decisão de primeira aplicação

**CPU-first**→ llama.cpp. Ollama também funciona, mas é mais lento. Nenhum outro motor é competitivo na CPU.

**AMD GPU**→ vLLM é o caminho mais forte suportado (suporte AMD ROCm). SGLang também funciona. TRT-LLM é bloqueado pela NVIDIA, então está fora.

**NVIDIA Hopper (H100 / H200)**→ VLLM ou SGLang ou TRT-LLM.

**NVIDIA Blackwell (B200 / GB200)**→ TRT-LLM é o líder de transmissão (Fase 17 · 07). vLLM e SGLang seguem-no de perto.

**Apple Silicon (M-series)**Ollama envolve isto.

### Decisão de segunda escala

**1 user / local dev**Um comando, primeiro sinal em segundos.

**10-100 users / small team**→ VLLM single-GPU.

**100-10k users / production**→ VLLM produção-pilha (fase 17 · 18) ou SGLang.

**10k+ users / enterprise**→ VLLM produção-pilha + desagregada (Fase 17 · 17) + LMCache (Fase 17 · 18).

### Terceira decisão sobre a carga de trabalho

**General chat / Q&A**→ VLLM ganha em padrão amplo.

**Agentic multi-turn (tools, planning, memory)**→ A RadixAttention (Fase 17 · 06) de SGLang é a dominante.

**RAG with heavy prefix reuse**→ SGLang.

**Code generation**→ VLLM bem; SGLang um pouco melhor no cache.

**Long context (128K+)**→ VLLM + preenchimento em pedaços; SGLang + KV em camadas.

### A armadilha de manutenção TGI

> **【中文解读】**TGI 陷:HuggingFace TGI entrou em 2025 em 12 de janeiro de 11 dias em um modelo de manutenção  apenas bug fix, deixou de ter funcionalidades atualizadas。 na história TGI tem o topo de observabilidade e HF  生态集積(模型卡、安全工具), original吞吐略低于vLLM(cerca de 10%)。 Para o novo projeto de 2026 ano, deve ser assumido que o TGI 部署 pode continuar a funcionar, mas deve ser planejado para mudar.

> **【拓展：工作负载驱动的引擎选择】**工作负载维度驱动引擎选择:(1) 通用聊天/问答 → vLLM(广泛默认);(2) Agente 多轮对话(工具、规划、记忆)→ SGLang RadixAttention 主导;(3) RAG 重前复用 → SGLang;(4) 代码生成 → vLLM 足够,SGLang 缓存略好;(5) 长上下文(128K+)→ vLLM + 分块预填充,SGLang + 分层 KV──Ollama 适合开发但不是生产共享服务的理想选择Go HTTP 序列化增加开销并发管理比 vLLM 简单、Openmetry 支持滞后──

Hugging Face TGI entrou em modo de manutenção em 11 de dezembro de 2025  apenas corrigem bugs para o futuro. Historicamente: observabilidade de nível superior, melhor integração do ecossistema HF (modelo de cartões, ferramentas de segurança), ligeiramente atrás do vLLM em throughput bruto.

Para novos projetos em 2026: desvio por defeito da TGI. As implementações existentes de TGI podem continuar, mas devem eventualmente migrar.

### O padrão de oleoduto

Dev (Ollama) → stage (llama.cpp) → prod (vLLM). Os motores assumem diferentes formatos de peso  GGUF para a família llama.cpp, HF safetensores para os motores GPU  para que uma conversão de formato possa estar entre as fases. Os engenheiros iteram rapidamente em laptops; espetáculos de fase quantizam a produção; prod é o alvo de serviço.

### Aviso Ollama

Ollama é ótimo para dev. Não é ótimo para produção compartilhada: serialização HTTP Go adiciona gastos, gerenciamento de concurência é mais simples do que vLLM, OpenTelemetry suporta lags. Use Ollama onde brilha  um usuário, um comando  e mudar para vLLM para compartilhado.

### Auto-hosted vs. gerenciado é uma decisão separada

Fase 17 · 01 (hiperscalers gerenciados), · 02 (platformas de inferência) cobertura gerenciada. Esta lição assume que você já decidiu auto-host. Razões para auto-host: residência de dados, ajuste personalizado, total custo de propriedade em escala, modelo de domínio não disponível no hospedado.

### Números que você deve lembrar

- Modo de manutenção TGI: 11 de dezembro de 2025.
- VLLM v0.15.1: Fevereiro 2026; PyTorch 2.10; suporte Blackwell SM120.
- Impressão de produção SGLang: 400.000+ GPUs.
- O diferencial de transmissão Ollama vs llama.cpp: 15-30% mais lento; 3x abaixo da carga de prod.

## Use-o com o framework implementado.
```figure
data-parallel
```

## Usá-lo

`code/main.py`é um caminhador de árvore de decisão: dado hardware + escala + carga de trabalho, escolhe um motor e explica o porquê.

> `code/main.py`é um caminhador de árvore de decisão: dado hardware + escala + carga de trabalho, escolhe um motor e explica o porquê.

## Envia-o . Produto .

> **【拓展：自托管 vs 托管的决策】**O sistema de gestão e gestão de dados não pode deixar a organização; o sistema de gestão de dados não pode deixar a organização; o sistema de gestão de dados não pode deixar a organização; o sistema de gestão de dados não pode deixar a organização; o sistema de gestão de dados não pode deixar a organização; o sistema de gestão de dados não pode deixar a organização; o sistema de gestão de dados não pode deixar a organização; o sistema de gestão de dados não pode deixar a organização; o sistema de gestão de dados não pode deixar a organização; o sistema de gestão de dados não pode deixar a organização; o sistema de gestão de dados não pode deixar a organização; o sistema de gestão de dados não pode deixar a organização; o sistema de gestão de dados não pode deixar a organização; o sistema de gestão de dados não pode deixar a organização; o sistema de gestão de dados não pode deixar a organização; o sistema de gestão de dados não pode deixar a organização; o sistema de gestão de dados não pode deixar a organização; o sistema de gestão de dados não pode deixar a organização; o sistema de gestão de dados não pode ser controlado; o sistema de gestão de dados não pode ser controlado; o sistema de gestão de dados não pode ser controlado; o sistema de gestão de dados não pode ser controlado; o sistema de gestão de dados é controlado; o sistema de gestão de dados é controlado é controlado por um sistema de dados é controlado por um sistema de dados é controlado por um sistema de dados é controlado por um sistema de dados.

Esta lição produz`outputs/skill-engine-picker.md`Com restrições, escolhe um motor e escreve o plano de migração.

> 本课产 出 `outputs/skill-engine-picker.md`Com restrições, escolhe um motor e escreve o plano de migração.

## Exercícios.

1. Corra .`code/main.py`O resultado coincide com a sua intuição?
   Tradução do inglês:`code/main.py` A produção está em conformidade com o esperado?
2. O teu infra é 12 H100s e 8 MI300X AMD.
   Sua infraestrutura é de 12 blocos H100 e 8 blocos MI300X AMD.
3. Uma equipa quer usar o TGI em 2026 porque "é o que sabemos".
   Tradução do inglês para o inglês: a teoria de um grupo de pessoas em 2026
4. Ollama dev para vLLM prod: quais são as mudanças na quantização, configuração e observabilidade?
   Ollama  desenvolvido até vLLM 生产: quantização, configuração e observação
5. Produto RAG com comprimento de prefixo P99 8K e alta reutilização entre os inquilinos.

## Termos-chave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| llama.cpp | "the CPU one" | Widest model support, fastest on CPU |
| Ollama | "the laptop one" | One-command install, dev-grade throughput |
| TGI | "HF's serving" | Maintenance mode since Dec 2025 |
| vLLM | "the default" | Broad production baseline 2026 |
| SGLang | "the agentic one" | Prefix-heavy, RadixAttention |
| TRT-LLM | "NVIDIA-locked" | Blackwell throughput leader, NVIDIA only |
| GGUF | "llama.cpp format" | Bundled K-quant variants |
| Production-stack | "vLLM K8s" | Phase 17 · 18 reference deployment |
| Pipeline pattern | "dev→stage→prod" | Ollama → llama.cpp → vLLM; weight formats differ per engine |

## Mais leitura 延伸阅读

- [AI Made Tools — vLLM vs Ollama vs llama.cpp vs TGI 2026](https://www.aimadetools.com/blog/vllm-vs-ollama-vs-llamacpp-vs-tgi/)
- [Morph — llama.cpp vs Ollama 2026](https://www.morphllm.com/comparisons/llama-cpp-vs-ollama)
- [n1n.ai — Comprehensive LLM Inference Engine Comparison](https://explore.n1n.ai/blog/llm-inference-engine-comparison-vllm-tgi-tensorrt-sglang-2026-03-13)
- [PremAI — 10 Best vLLM Alternatives 2026](https://blog.premai.io/10-best-vllm-alternatives-for-llm-inference-in-production-2026/)
- [TGI maintenance announcement](https://github.com/huggingface/text-generation-inference)- Notas de liberação.
- [vLLM v0.15.1 release notes](https://github.com/vllm-project/vllm/releases)
