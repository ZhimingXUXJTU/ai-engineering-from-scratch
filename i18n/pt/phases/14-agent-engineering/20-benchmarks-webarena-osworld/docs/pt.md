# Benchmarks: WebArena e OSWorld

> WebArena testa a capacidade de agente web em quatro aplicativos auto-hospedados. OSWorld testa a capacidade de agente de desktop em Ubuntu, Windows, macOS. No lançamento (20232024) ambos mostraram uma grande lacuna entre os melhores agentes da classe e os humanos. A lacuna está se reduzindo; os modos de falha não mudaram.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 19 (SWE-bench, GAIA) | **前置知识:** 见原文
**Time:** ~60 minutes | **时间:** 见原文

## Objetivos de aprendizagem

- Descreva os quatro aplicativos auto-hospedados da WebArena e por que a avaliação baseada na execução é importante.
- Explique por que o OSWorld usa capturas de tela reais do sistema operacional em vez de APIs de acessibilidade.
- Nomear os dois principais modos de falha do OSWorld: conectividade de interface gráfica e conhecimento operacional.
- Resumir o que os OSWorld-G e os OSWorld-Human adicionam ao índice de referência base.

## O problema é o problema da introdução

Os agentes generalistas podem chamar ferramentas. Eles podem dirigir um navegador em 20 cliques para concluir um checkout de compras? Eles podem configurar uma caixa Linux usando apenas teclado e mouse? Estas são as perguntas que WebArena e OSWorld respondem.

> O agente geral pode utilizar ferramentas. Mas eles podem mover o navegador para completar 20 cliques para completar a compra de contas? Eles podem configurar apenas com teclado e mouse uma máquina Linux?


> **【中文解读】**WebArena e OSWorld  avaliação de Agente em real ambiente de cálculo capacidade de operação.

> **{【拓展：WebArena (CMU, 2023) 创建了真实的 Web 环境（电商、论坛、GitLab），A...】}**WebArena (CMU, 2023) 创建了真实的 Web 环境(电商、论坛、GitLab),Agent 需要像人类一样浏览和操作。2026年 SOTA 约 35% taxa de sucesso,人类约 80%。OSWorld (HKU, 2024) 提供真实的 Ubuntu/Windows/macOS 桌面环境,Agent 需要操作 GUI 完成任务。

> - Não .**【前置】**建议先过:Phase 14·19 (SWE-bench/GAIA) 本节是其姐妹篇,专门评估"GUI 操作"能力;以及Phase 14·21 (Computer Use Agents) 本节是评估那些 Agent 的"考试题"──理解GUI 操作和工具调用区别──GUI 是像素+点击,工具调用是API+JSON) 本节是关键──

## O conceito central.

### WebArena (Zhou et al., ICLR 2024)

- 812 tarefas de longo horizonte em quatro aplicativos web auto-hospedados: um site de compras, um fórum, uma ferramenta de desenvolvimento como o GitLab, um CMS empresarial.
- Além de utilidades: mapa, calculadora, scratchpad.
- A avaliação é baseada na execução através de APIs de ginásio  foi a ordem colocada, foi o problema encerrado, foi a página do CMS atualizada?
- Na liberação: melhor agente GPT-4 atingiu 14,41% de sucesso contra humano 78,24%.

O enquadramento auto-hosted importa  o índice de referência não é escorregadio porque os aplicativos-alvo são fixados e reprodutíveis.

> O quadro de autogestão é importante para que a base de aplicação seja fixa e reproduzível e não seja instável.

> - Não .**【类比】**WebArena e OSWorld são diferentes de "simulação de condução" e "real carros": WebArena é simulação de condução quatro aplicações de páginas web fixas (e-commerce, fórum etc.), ambiente totalmente controlado e replicável, como o padronização do local de condução; OSWorld é real carros na estrada  real Ubuntu/Windows/macOS  sistemas, cada versão da UI pode ser diferente, também pode ser lançado em janelas, cartões, anúncios.**关键**O WebArena 测 é "Agente 能不能使用Web", OSWorld 测 é "Agente 能不能使用电脑"后者难一个量级──

> WebArena 和 OSWorld é um ambiente de avaliação de um agente usando computadores.

### Extensões

- **VisualWebArena** tarefas baseadas em elementos visuais, onde o sucesso depende da interpretação das imagens (câmpanhas de tela como observações de primeira classe).
- **TheAgentCompany**(Dec 2024)  adiciona terminal + codificação; mais como um ambiente de trabalho remoto real.

### OSWorld (Xie et al., NeurIPS 2024)

- 369 tarefas reais de computador em Ubuntu, Windows, macOS.
- Controle de teclado e mouse de forma livre de aplicações reais.
- 1920×1080 capturas de tela como observação.
- No momento da liberação: melhor modelo 12,24% vs humano 72,36%.

### Modos de falha primária

1. **GUI grounding.**Mapeamento de pixel → elemento. Os modelos lutam para localizar os elementos da interface de forma confiável em 1920×1080.
2. **Operational knowledge.**Qual menu tem a configuração, qual atalho de teclado, qual painel de preferências.

> ️ **【易错点】**Use DOM ou API de acessibilidade  run OSWorld e depois relata "高分"―**后果**O propósito do design é testar**视觉 grounding**(Mapping of Element), usando DOM API assim como contornar o desafio central.**一行修复**: em OSWorld 上 só pode usar screenshot-as-input de agente, caso não é "en OSWorld 上评估"― se quiser testar um agente baseado em DOM, use WebArena ou Mind2Web―

### Seguimento

- **OSWorld-G**564 amostras de terra + Jedi treinamento conjunto.
- **OSWorld-Human**- trajetórias de acção do ouro seleccionadas manualmente.

### Por que isto importa

Claude uso de computadores, OpenAI CUA, Gemini 2.5 Uso de computadores (Lessão 21) todos treinam em cargas de trabalho moldadas pela WebArena e OSWorld.

> Claude 计算机使用、OpenAI CUA、Gemini 2.5 计算机使用(第 21 课) todos estão em WebArena 和 OSWorld 塑造 塑造 工作负载上训练──基准是目标;生产模型是交付的答案──

> WebArena 和 OSWorld é um ambiente de avaliação de um agente usando computadores.

### Onde a análise comparativa vai mal

- **Screenshot-only evals.**O OSWorld é guiado por captura de tela; avaliar um agente que usa DOM ou APIs de acessibilidade no OSWorld perde o desafio de aterrissagem.
- **Ignoring trajectory length.**A pontuação apenas de taxa de sucesso perde a ineficiência de 1,4-2,7x nas superfícies OSWorld-Human.
- **Stale self-hosted apps.**Os aplicativos da WebArena pin versões específicas; atualização sem re-curatização quebra comparabilidade.

> 🤔 **【困惑】**A: Não pode ser usado agora? A: Não pode ser usado agora? A: Não pode ser usado agora?**针对性优化**de: fixas várias páginas web 清晰的任务流、人回路底──Claude Code 在 WebArena 上可能也低分,但它在IDE这种结构化环境里可以使用──**结论**A base de teste é "capacidade superior", "produção usada" especializada, ambas não podem ser trocadas diretamente.

> **仅截图评估。**O OSWorld é um projeto de análise; o OSWorld é um projeto de avaliação que utiliza DOM ou API sem obstáculos.
> **忽略轨迹长度。**                                                                                                                                                                                                                                                              
> **过时的自托管应用。**A aplicação da WebArena fixa uma versão específica; não reorganiza a sua atualização para destruir a sua compatibilidade.

## Construí-lo e realizei-o.
```figure
ae-agent-human-gap
```

## Construí-lo

`code/main.py`Implementa um arnes de agentes de web de brinquedo:

> `code/main.py`实现 um brinquedo Agente Web 测试工具:

> WebArena 和 OSWorld é um ambiente de avaliação de um agente usando computadores.

- Uma máquina de estado "aplicativo de compras" mínima: list_items, add_to_cart, checkout.
- Tráetoras de ouro para 3 tarefas.
- Um agente com guião que tenta cada tarefa.
- Avaliação baseada na execução (controle de estado) e métrica de eficiência de trajetória (pasos versus ouro).

- É o que é ?

```
python3 code/main.py
```

Resultado: taxa de sucesso por tarefa e eficiência de trajetória, que refletem a metodologia da OSWorld-Human.

> 输出: taxa de sucesso e eficiência de rotação de cada missão, refletindo o método OSWorld-Human.

> WebArena 和 OSWorld é um ambiente de avaliação de um agente usando computadores.

## Use-o com o framework implementado.

- **WebArena Verified**auto-hostado num cluster interno para avaliação contínua.
- **OSWorld**numa frota de máquinas virtuais para agentes de desktop.
- **Computer-use agents**(Lessão 21) Claude, OpenAI CUA, Gemini, todos treinados para carregar tarefas como esta.
- **Your own product flows** capturar trajetórias de ouro para as suas 20 principais tarefas; executar agentes contra eles semanalmente.

## Envia-o . Produto .

`outputs/skill-web-desktop-harness.md`Construirá um arsenal de agentes web/desktop com métricas de avaliação e eficiência de trajetória baseadas em execução.

> `outputs/skill-web-desktop-harness.md`Construir um instrumento de teste de Agente Web/descrevista, com um indicador de avaliação e de eficiência de tráfego baseado na execução.

> WebArena 和 OSWorld é um ambiente de avaliação de um agente usando computadores.

## Exercícios.

1. Estende o arame de brinquedo com um segundo aplicativo (um fórum). Escreva 3 tarefas mais trajetórias de ouro.
  Tradução do inglês para tradução do inglês:
2. Adicione o relatório de eficiência de trajetória por tarefa.
  Tradução do inglês para tradução do inglês:
3. Implementar uma ferramenta "distractor" que a trajetória do ouro nunca usa.
  Tradução do inglês para tradução do inglês:
4. Como separaria as falhas de aterragem das falhas de planeamento nas suas próprias avaliações?
  Tradução do inglês para tradução do inglês:
5. Leia os aplicativos do WebArena README. O que se rompe quando você atualiza uma das versões de aplicativos fixadas?
  Tradução do inglês para tradução do inglês:

## Termos-chave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| WebArena | "Web agent benchmark" | 812 tasks across 4 self-hosted apps; gym-style evaluation |  |
| VisualWebArena | "Visual WebArena" | Visually grounded WebArena; screenshots are observations |  |
| OSWorld | "Desktop agent benchmark" | 369 tasks on real Ubuntu/Windows/macOS |  |
| GUI grounding | "Pixel-to-element mapping" | Model localizing UI elements in 1920x1080 |  |
| Operational knowledge | "OS know-how" | Which menu, which shortcut, which preference pane |  |
| OSWorld-G | "Grounding suite" | 564 grounding-only samples + training set |  |
| OSWorld-Human | "Gold trajectories" | Manual expert action sequences to measure efficiency |  |
| Trajectory efficiency | "Steps over gold" | Agent step count divided by human minimum |  |

## Mais leitura 延伸阅读

- [Zhou et al., WebArena (arXiv:2307.13854)](https://arxiv.org/abs/2307.13854) Referência web de quatro aplicações
  Tradução do português:
- [Xie et al., OSWorld (arXiv:2404.07972)](https://arxiv.org/abs/2404.07972) Referência de desktop cross-OS
  Tradução do português:
- [Anthropic, Introducing computer use](https://www.anthropic.com/news/3-5-models-and-computer-use) Capacidade de referência de Claude
  Tradução do português:
- [OpenAI, Computer-Using Agent](https://openai.com/index/computer-using-agent/) Números OSWorld e WebArena
  Tradução do português:
