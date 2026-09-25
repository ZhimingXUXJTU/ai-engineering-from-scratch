# Red Team Tooling  Garak, Guarda Llama, Guarda Pyrit  Llama Guarda  ferramentas Garak Pyrit

> Três ferramentas de produção enquadram a pilha de equipa vermelha de 2026. Llama Guard (Meta)  um classificador Llama-3.1-8B ajustado em 14 categorias de perigo de MLCommons; o 2025 Llama Guard 4 é um classificador multimodais nativo 12B podado a partir de Llama 4 Scout. Garak (NVIDIA)  Scanner de vulnerabilidade LLM de código aberto com sondas estáticas, dinâmicas e adaptativas para alucinações, vazamento de dados, injeção rápida, toxicidade e jailbreaks. PyRIT (Microsoft)  campanhas red-team multi-turn com Crescendo, TAP e cadeias de conversores personalizadas para exploração profunda. Llama Guard 3 é documentado no Meta "Llama 3 Herd of Models" (arXiv:2407.21783); Llama Guard 3-1B-INT4 em arXiv:2411.17713; Arquitetura da sonda de Garak em github.com/NVIDIA/garak. Estas ferramentas são a interface de produção 2026 entre a investigação da equipa vermelha (Lessões 12-15) e a implantação (Lessões 17+).

> **【中文解读】**Este capítulo apresenta métodos de avaliação de segurança sistematizados, com ataques automatizados para descobrir falhas de AI  sistemas. Três ferramentas de produção definem a tecnologia da equipe vermelha em 2026: Lama Guard (Meta) Llama-3.1-8B 分类器微调到14 MLCommons 危险类别;Garak (NVIDIA) 开源 LLM 漏洞扫描机,含静态、动态和自适应探针;PyRIT (Microsoft) 多轮红队活动,含 Crescendo、TAP 和自定义转换链;;

> **【拓展：2026 红队技术栈 → 生产配置】**标准配置:Llama Guard 放在模型两侧(输入+输出),Garak 每晚运行回归测试,PyRIT Used for pre-release campaign。Prompt-Guard-86M é o Meta de menor porte de entrada, com Llama Guard 配合使用──TrustyAI irá Garak e Llama Stack shields 集成进行端到端评估──

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, tool-architecture simulator and Llama Guard-style classifier mock) | **语言:** Python（标准库，工具架构模拟器和 Llama Guard 风格分类器模拟）
**Prerequisites:** Phase 18 · 12-15 (jailbreaks and IPI) | **前置知识:** Phase 18 · 12-15 (越狱和 IPI)
**Time:** ~75 minutes | **时间:** ~75 分钟

> - Não .**【前置】**学本节前请先掌握:Fase 18·12-15(越狱+IPI 全套) ⋅2026 红队工具三件套──
> - Não .**【类比】**红队工具 = "AI 安全的透透测试套件"――Llama Guard(Meta) = 输入输出分类器(14 危险类别, similar à Fase 15·18);Garak(NVIDIA) = 漏洞扫描器(静态+动态+自适应探针,覆盖幻觉/数据泄漏/越狱);PyRIT(Microsoft) = 多轮深度攻击编排(Crescendo/TAP/自定义链)。三件套是研究(12-15) 和部署(17+) 之间的工程界面──

## Objetivos de aprendizagem

- Descreva a posição do Llama Guard 3/4 na pilha de segurança: classificador de entrada, classificador de saída ou ambos.

> Descrição de Llama Guard 3/4 在安全技术中的位置:输入分类器、输出分类器或两者兼有──

- Cite as 14 categorias de perigo MLCommons e indique uma que não seja óbvia (abuso de interpretadores de código).

> 列出 14  MLCommons 危险类别,并说明一个不明显的类别 () 

- Descreva a arquitetura da sonda de Garak: sondas, detectores, arneses.

> 描述 Garak's探针架构:探针、检测器、线束──

- Descreva a estrutura da campanha de turnos múltiplos do PyRIT e como ela se compõe com as sondas Garak.

> Descrição da estrutura de atividades do PyRIT e de como se relaciona com o Garak 探针组合──

## O problema é o problema .

As lições 12-15 apresentam a superfície de ataque. As implementações de produção precisam de avaliação repetível e escalável. Três ferramentas dominam 2026: Llama Guard (o classificador de defesa), Garak (o escaneador), PyRIT (o orquestador de campanha). Cada uma visa uma camada diferente do ciclo de vida da equipe vermelha.

> Lições 12-15  mostraram a face de ataque. A produção de operações precisa de avaliação reprodutiva.

## O conceito .

> **【中文解读】**Llama Guard 3 é Llama-3.1-8B 模型微调到 MLCommons AILuminate 14 类别的输入/输出分类,支持 8种语言。Llama Guard 3-1B-INT4 é quantificada边缘变体(440MB, CPU móvel 约30 tokens/s)。Llama Guard 4(4月2025 年) é 12B 原生多模态分类器, de Llama 4 Scout 剪枝, substituindo os anteriores 8B 文本和 11B 视觉分类器。

### Guarda de lama (Meta)

Llama Guard 3 é um modelo Llama-3.1-8B ajustado para classificação de entrada/saída em relação às categorias MLCommons AILuminate 14:
- Crimes violentos, crimes não violentos, relacionados com o sexo, CSAM, difamação
- Conselhos especializados, privacidade, IP, armas indiscriminadas, ódio
- Suicídio/auto-harmagem, conteúdo sexual, eleições, abuso de interpretadores de código

> Llama Guard 3 é um modelo Llama-3.1-8B, dirigido para MLCommons AILuminate 14 个类别进行输入/输出分类微调――支持 8种语言――

Suporta 8 idiomas. Uso: coloca antes do LLM (moderação de entrada), após o LLM (moderação de saída), ou ambos. Os dois usos geram distribuições de treinamento diferentes.

> Uso: colocar LLM 之前(输入审核) 之后(输出审核) 或两者兼有──Llama Guard 3 作为单一模型处理两者──

Llama Guard 3-1B-INT4 (arXiv:2411.17713, 440MB, ~ 30 tokens / s em CPU móvel) é a variante de borda quantizada.

> Llama Guard 3-1B-INT4 é um grande número de chips.

Llama Guard 4 (abril 2025) é 12B, nativo multimodal, podado a partir de Llama 4 Scout.

> Llama Guard 4(2025 年 4 月) é um aparelho de divisão original de 12B, de Llama 4 Scout 剪枝, substituindo os anteriores 8B 文本和 11B 视觉分类器──

> **【拓展：Garak 架构 → 探针/检测器/线束】**Garak's three-tiered architecture: probe幻觉、数据泄露、提示注入、毒性、越狱的攻击生成器,分为静态固定提示)、动态生成提示)、自适应响应目标输出);检测器针对预期失败模式评分输出;线束管理探针-检测器对,运行活动,生成报告――基于层评分(TBSA) substituir二元通过/失败模型可以在探针上通过同一级度级 3但失败级 5

### Garak (NVIDIA)

Scanner de vulnerabilidade de código aberto.
- **Probes.**Geradores de ataque para alucinação, vazamento de dados, injeção rápida, toxicidade, jailbreaks. estático (invite fixo), dinâmico (invite gerado), adaptativo (responde à saída alvo).
- **Detectors.**Resultados de pontuação em relação aos modos de falha esperados  tóxicos, vazados, jailbroken.
- **Harnesses.**Gerenciar pares de sondas-detectores, executar campanhas, gerar relatórios.

> 开源漏洞扫描机.架构:探针. 探针. 探针. 探针. 探针. 探针. 探针. 探针. 探针. 探针. 探针. 探针.

TrustyAI integra Garak com os escudos Llama-Stack (Clasificador de entrada Prompt-Guard-86M, Classificador de saída Llama-Guard-3-8B) para avaliação de alvos protegidos de ponta a ponta. A pontuação baseada em níveis (TBSA) substitui o pass/falha binário.

> TrustyAI irá Garak e Llama Stack Shields  integrar para realizar avaliação de fim a fim.

### PyRIT (Microsoft)

Python Risk Identification Toolkit, campanhas red-team multiples.
- **Converters.**Transformar um semente de resposta parafrase, codificar, traduzir, jogar papéis.
- **Orchestrators.**Executa a campanha: Crescendo (escalação), TAP (branqueamento), RedTeaming (loop personalizado).
- **Scoring.**Licenciatura em Direito como juiz ou classificador como juiz.

> PyRIT é Python 风险识别工具包──多轮红队活动──核心组件:转换器:转换种子提示) 编排器:运行活动: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分:                                                                                                                                                                                                                                        

O PyRIT é o primo mais pesado de Garak. Garak executa milhares de sondas de uma única volta; o PyRIT executa campanhas profundas de várias voltas projetadas para quebrar modos de falha específicos.

> O PyRIT é um programa de pesos de Garak. Garak opera milhares de sondas de uma única rota.

### A pilha

Coloque a guarda Llama em ambos os lados do modelo. Execute Garak todas as noites para regressão. Execute PyRIT para campanhas pré-lançamento. Esta é a configuração padrão de 2026 para a maioria das implantações de produção.

> Na modalidade, ambos os lados são colocados a Guarda Llama.

> **【中文解读】**评估陷:评判身份所有三工具都可以使用LLM 评判,评判校准驱动报告的ASR(Lesson 12),必须指定评判;探针过时Garak 探针随着模型修复和老化,自适应探针(PAIR 式)比静态探针老化更慢;Llama Guard 在良性内容上的误报率早期版本过标记政治和LGBTQ+ 内容,v3/v4 校准有改善但未按部署校准;;

### Empregos de avaliação

- **Judge identity.**As três ferramentas podem usar um juiz de LLM; os drives de calibração dos juízes relataram ASRs (Lessão 12). Especifique o juiz ao lado da ferramenta.
- **Probe staleness.**Garak envelhece as sondas quando os modelos são apertados contra elas.
- **Llama Guard FPR on benign content.**As primeiras versões da Guarda Llama exibiram conteúdo político e LGBTQ +; as calibrações da Guarda Llama 3/4 foram melhoradas, mas não calibradas por implantação.

### Onde isto encaixa na Fase 18

Lições 12-15 são as famílias de ataque. Lição 16 é a ferramenta de produção. Lição 17 (WMDP) é a avaliação de capacidade de duplo uso. Lição 18 é os quadros de segurança de fronteira que envolvem essas ferramentas em uma estrutura política.

> Lições 12-15 é ataque familiar. Lição 16 é ferramenta de produção. Lição 17 é avaliação de capacidade de uso duplo. Lição 18 é encomendar essas ferramentas em uma estrutura de segurança de vanguarda na estrutura de políticas.

> **【拓展：PyRIT → 多轮深度利用】**PyRIT(Microsoft) é o pesador de Garak. Garak opera milhares de pilhas de solo, PyRIT opera com o objetivo de quebrar um determinado modelo de falha de atividades de profundidade múltipla.

## Usa-o. Usa-o.
```figure
al-guard-stack
```

## Usá-lo

`code/main.py`Construi um classificador de estilo brinquedo Llama Guard (palavra-chave + características semânticas em 14 categorias), um arnes Garak brinquedo (loop de detector de sonda), e uma cadeia de conversor de várias voltas de estilo PyRIT.

> `code/main.py`Construiu brinquedo Llama Guard 风格分类器、 brinquedo Garak 线束和 PyRIT 风格多轮转换链── você pode comparar três ferramentas e observar diferentes características de cobertura──

## Envia-o .

Esta lição produz`outputs/skill-red-team-stack.md`- Uma descrição da implantação indica quais das três ferramentas são adequadas, o que deve ser configurado em cada uma delas e qual é a cadência de regressão a executar.

> 本课产 出 `outputs/skill-red-team-stack.md` Descrição da determinação da implementação, nomear quais dos três instrumentos são adequados, cada um dos quais é equipado e qual é o ritmo de regresso.

## Exercícios.

1. Corra .`code/main.py`Comparar a taxa de detecção do classificador de estilo Llama-Guard em ataques de uma única volta versus vários.

2. Implementar uma nova sonda Garak: um pedido prejudicial codificado base64.

3. Extender a cadeia de conversores de estilo PyRIT com um conversor "traduzir para francês, depois parafrasear".

4. Leia a lista de categorias de perigo do Llama Guard 3. Identifique duas categorias em que os dados de treinamento produziriam, de forma realista, taxas altas de falsos positivos sobre conteúdo legítimo para desenvolvedores.

5. Comparar os princípios de design do Garak e do PyRIT.

## Termos-chave .

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| Llama Guard | "the classifier" | Fine-tuned Llama-3.1-8B/4-12B safety classifier with 14 hazard categories |
| Garak | "the scanner" | NVIDIA open-source vulnerability scanner; probes, detectors, harnesses |
| PyRIT | "the campaign tool" | Microsoft multi-turn red-team orchestrator; converters, orchestrators, scoring |
| Prompt-Guard | "the small classifier" | Meta's 86M prompt-injection classifier, paired with Llama Guard |
| TBSA | "tier-based scoring" | Garak's tier-based pass/fail replacing binary outcomes |
| Converter chain | "paraphrase + encode + ..." | PyRIT composition primitive for building multi-step attacks |
| MLCommons hazard categories | "the 14 taxonomies" | Industry-standard taxonomy Llama Guard targets |

## Mais leitura 延伸阅读

- [Meta — Llama Guard 3 (in Llama 3 Herd paper, arXiv:2407.21783)](https://arxiv.org/abs/2407.21783) o classificador 8B
- [Meta — Llama Guard 3-1B-INT4 (arXiv:2411.17713)](https://arxiv.org/abs/2411.17713) Classificador de dispositivos móveis quantizados
- [NVIDIA Garak — GitHub](https://github.com/NVIDIA/garak) o repo do scanner e a documentação
- [Microsoft PyRIT — GitHub](https://github.com/Azure/PyRIT) o conjunto de ferramentas da campanha
