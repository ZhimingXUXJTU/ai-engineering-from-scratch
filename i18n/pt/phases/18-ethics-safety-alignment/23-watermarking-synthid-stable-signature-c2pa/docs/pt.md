# Marcação de água  SynthID, assinatura estável, C2PA 稳定签名 水印 SynthID C2PA

> Três tecnologias estruturam 2026 proveniência de conteúdo gerado por IA. SynthID (Google DeepMind)  marcação de água de imagem lançada em agosto de 2023, texto + vídeo maio 2024 (Gemini + Veo), texto de código aberto outubro de 2024 através do Responsible GenAI Toolkit, detector multimédia unificado novembro 2025 ao lado do Gemini 3 Pro. A marcação de água de texto ajusta as probabilidades de amostragem do token seguinte de forma imperceptível; as marcas de água de imagem/vídeo sobrevivem à compressão, corte, filtros, alterações na taxa de quadros. Estabilidade da assinatura (Fernandez et al., ICCV 2023, arXiv:2303.15435)  sintonização do decodificador de difusão latente para que cada saída contenha uma mensagem fixa; imagens cortadas (10% do conteúdo) geradas detectadas > 90% no FPR<1e-6. Seguimento "A assinatura estável é instável" (arXiv:2405.07145, maio 2024)  ajuste fino remove a marca de água enquanto preserva a qualidade. C2PA  padrão de metadados criptográficamente assinado, com evidência de adulteração (C2PA 2.2 Explicador 2025). A marcação de águas e a C2PA são complementares: os metadados podem ser desligados, mas têm origem mais rica; as marcas de águas persistem através da transcodificação, mas transportam menos informação.

> **【中文解读】**Este capítulo apresenta a tecnologia de impressão de água da AI SynthID、C2PA 等 identificando a AI produzir conteúdo métodos。SynthID(Google DeepMind) ajustar next-token 采样概率使生成包含更多"绿色"令牌不可察知但可检测──Stable Signature 微调潜在扩散解码器使每个输出包含固定二进制消息──C2PA é uma assinatura criptográfica、改的元数据标准──

> **【拓展：水印 → Deepfake 检测】**A água imprensa é um caminho tecnológico central do Deepfake 检测的核心技术路径. A tecnologia de transmissão do SynthID é um sistema de leitura de sinais de texto, imagens, áudio e vídeo.

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, token-watermark embed + detect) | **语言:** Python（标准库，token 水印嵌入 + 检测）
**Prerequisites:** Phase 10 · 04 (sampling), Phase 01 · 09 (information theory) | **前置知识:** Phase 10 · 04 (采样), Phase 01 · 09 (信息论)
**Time:** ~75 minutes | **时间:** ~75 分钟

> - Não .**【前置】**學本节前请先掌握:Fase 10·04(采样) 、Fase 01·09(信息论) ∼三大水印技术 + 内容追溯标准。
> - Não .**【类比】**水印 = "AI 内容の隐形身份证"──SynthID(Google) = 调整次要代码 采样偏好"绿色"代码,不可察知但可检测;Stable Signature = 微调解码器让每张图都含固定二进制消息(剪裁 10% 仍 >90% 检出);C2PA = 加密签名元数据──互补:元数据可剥但信息丰富;水抗印转码但信息少──
> ️ "Signature stable 不稳定"2024.5:

## Objetivos de aprendizagem

- Descreva a marcação de água a nível de token (estilo de texto SynthID) e o mecanismo pelo qual é detectável.
- Descreva a assinatura estável e o ataque de remoção de 2024 que a quebrou.
- O papel do C2PA estatal e por que é complementar ao marcado de água.
- Descreva as principais limitações: sinal específico do modelo, robustez sob parafrase e ataques que preservam o significado (arXiv:2508.20228).

> 描述令牌级水印(SynthID-text 风格) e seu mecanismo de detecção── descrição da assinatura estável 和 2024 anos destruindo seu ataque de remoção── explicação do papel do C2PA e por que ele é complementado com o sistema de água── descrição de limitações fundamentais: modelo específico sinal、释义下鲁棒性和意义保持攻击──

## O problema é o problema .

2023-2024 viu deepfakes e conteúdo gerado pela IA entrar em contextos políticos e de consumo em escala. A marcação de água é o sinal de proveniência técnica proposto: marque gerações no momento da criação, detecta-as mais tarde. 2025 evidência: nenhuma marcação de água é incondicionalmente robusta, mas em camadas com metadados C2PA a combinação fornece uma história de proveniência utilizável.

> 2023-2024 de profundidade falsificação e produção de conteúdo de IA em grande escala para o cenário político e de consumo.

## O conceito .

> **【中文解读】**文本水印机(Kirchenbauer 等人 2023, by Google 产品化): cada passo de código vai começar K 个令牌哈希产生词汇表的伪随机"绿色"和"红色"分区,向绿色logits 添加 delta 偏置采样――生成包含比随机更多的绿色令牌――检测:重新哈希每个前,计数生成中的绿色令牌,计算 z 分数――水印文本 z > 0,人类文本 z ~ 0。

### Marcação de água do texto (estilo de texto SynthID)

O mecanismo de Kirchenbauer et al. 2023, produzido pelo Google:

1. Em cada passo de decodificação, hash os tokens K anteriores para produzir uma partição pseudorandomática do vocabulário em conjuntos "verde" e "vermelho".
2. Amostragem de bias em direção ao conjunto verde adicionando δ aos logitos verdes.
3. A geração contém mais tokens verdes do que o acaso produziria.

Detecção: repete cada prefixo, conte os tokens verdes na geração, compute uma pontuação z. A pontuação z é >0 para texto marcado por água, ~0 para texto humano.

Propriedades:
- Imperceptível para os leitores (δ é suficientemente pequeno para que a perda de qualidade seja menor).
- Detectável com acesso à função de partição de vocabulário.
- Não é robusto para parafrasear. Reescrever o texto destrói o sinal.

SynthID-text é de código aberto em outubro de 2024 através do Google Responsible GenAI Toolkit.

> **【中文解读】**Estabilidade de assinatura (((Fernandez 等人, ICCV 2023)) Micro调潜在扩散解码器使每个生成图像包含固定二进制消息──剪切到原始内容10%的图像在 FPR<1e-6 下检测率 >90%──但2024 年 5 月"Stability Signature is Unstable"证明微调解码器可以在保持图像质量同时移除水印对抗性生成后微调成本低──

### Assinatura estável (imagem)

Fernandez et al. ICCV 2023. Fine-tune o decodificador de difusão latente para que cada imagem gerada contenha uma mensagem binária fixa incorporada na representação latente. A detecção é decodificada do latente com um decodificador neural.

> Estabilidade de assinatura 微调潜在扩散解码器 permite que cada imagem gerada contenha um sistema de informação fixa.

Maio de 2024 "Signature stable is unstable" (arXiv:2405.07145): ajuste fino do decodificador remove a marca de água enquanto preserva a qualidade da imagem.

> 2024 5 月 "Signature stable is unstable" prova que o micro-moduleador pode manter a qualidade da imagem ao mesmo tempo em que remove o micro-module.

### Detetor unificado SynthID (novembro 2025)

Junto com o Gemini 3 Pro: um detector multimédia que lê sinais SynthID de texto, imagem, áudio e vídeo em uma API. Unifica a pilha de proveniência do Google.

> 伴随 Gemini 3 Pro: um transmodelo tester, pode ser lido em texto, imagem, áudio e vídeo 信号──统一 Google Source技术──

> **【拓展：C2PA + 水印互补 → EU AI Act Article 50】**C2PA 和水印互补:元数据可剥离但携带丰富来源链;水印通过转码持久但只携带少量比特──Google集集成在搜索、广告和"关于此图片"中两者──EU AI Act Artigo 50 de transparência código requer que a AI produzir etiquetas de conteúdo ((incluindo Deepfake), isto é necessário Lição 23 Layer de supervisão da tecnologia de água-impressão──

### C2PA

Coalizão para a Providencia e Authenticidade do Conteúdo. Padrão de metadados criptográficamente assinado com evidência de adulteração. C2PA 2.2 Explicador (2025).

> C2PA é uma signatura de criptografia, padrão de dados de segurança e segurança.

Complementar à marcação de água:
- Os metadados podem ser despojados; as marcas de água não podem (fácilmente).
- Os metadados são ricos (cadena de proveniência completa); as marcas de água transportam bits.
- C2PA depende da adoção da plataforma; marcas de água incorporadas automaticamente.

> Compartilhar dados com dados em formato de código aberto, mas com um conteúdo muito rico;

O Google integra tanto na Pesquisa, anúncios e "Acerca desta imagem".

> O Google em busca e publicidade e "Acerca desta imagem"

> **【拓展：水印局限性 → 模型特定信号问题】**关键局限性:SynthID 水印仅来自启用SynthID的模型──"无SynthID 信号"不等于真实性证明未启用SynthID的模型生成的任何内容都不会有水印──此外,arXiv:2508.20228(2025) demonstrou o significado de manter o ataque pode simultaneamente destruir o texto de um código de código e várias formas de imagem de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de

### Limitações

- **Model-specific.**A geração de um modelo sem SynthID não é marcada por água, portanto, "nenhum sinal SynthID" não é prova de autenticidade.
- **Paraphrase.**As marcas de água do texto não sobrevivem à paráfrase que preserva o significado.
- **Transformation attacks.**arXiv:2508.20228 (2025) mostra ataques de preservação de significado que destroem marcas de água de texto e muitas marcas de água de imagem.
- **Fine-tune removal.**Por "Signature stable is unstable", o ajuste fino de pós-geração remove as marcas de água embutidas.

### Lei da UE sobre IA Artigo 50

Código de Transparência para a rotulagem de conteúdos gerados por IA (primeiro projecto de Dezembro de 2025, segundo projecto de Março de 2026, previsto final de Junho de 2026 para o [European Commission status page](https://digital-strategy.ec.europa.eu/en/policies/code-practice-ai-generated-content)O código permanece em redação a partir de abril de 2026 e o cronograma está sujeito a alterações. A camada regulatória que requer a camada técnica.

### Onde isto encaixa na Fase 18

As lições 22-23 são sobre o que o modelo emite (dados privados, sinal de proveniência). A lição 27 abrange a governança de dados de formação. A lição 24 é o quadro regulamentar que exige essas medidas técnicas.

> Lições 22-23  Sobre modelos de dados (private data 源信号)  Lição 27 涵盖训练数据管理 ・ Lição 24 要求这些技术措施的监管框架──

## Usa-o. Usa-o.
```figure
an-watermark-greenlist
```

## Usá-lo

`code/main.py`O sistema de detecção de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de

> `code/main.py`构建玩具文本水印──令牌是整数 0.N-1;水印采样偏向哈希定义的绿色集──检测器计算绿色令牌 z 分数── você pode observar 1000 令牌生成的检测、释义破坏信号以及人类文本上的误报率──

## Envia-o .

Esta lição produz`outputs/skill-provenance-audit.md`- Tendo em conta uma implantação de conteúdos com uma alegação de proveniência, verifica: o mecanismo de marca de água (se houver), a cadeia de assinatura C2PA (se houver), a robustez adversária de cada um deles e a cobertura por modalidade.

> 本课产 出 `outputs/skill-provenance-audit.md` Definição de fontes de declarações de conteúdo, auditoria: mecanismo de impressão de água, C2PA, cadeia de assinaturas, respectivas oposições à robustez e cobertura de cada modelo.

## Exercícios.

1. Corra .`code/main.py`. Relatar os resultados z para a geração de 1000 tokens com marca de água versus texto escrito por humanos. Identificar a taxa de falsos positivos no limiar de confiança de 95%.

2. Implementar um ataque parafrase que substitua 30% dos tokens por sinônimos.

3. Leia Kirchenbauer et al. 2023 Secção 6 sobre robustez. Por que as marcas de água de texto falham sob parafrase, mas as marcas de água de imagem sobrevivem ao corte?

4. Desenhar uma implementação que use SynthID-text + C2PA metadados. Descrever a cadeia de proveniência que um consumidor vê. Identificar um modo de falha de cada componente.

5. O resultado de 2024 "Signature estável é instável" mostra que o ajuste fino remove a marca de água da imagem.

## Termos-chave .

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| SynthID | "Google's watermark" | Cross-modal provenance signal; text, image, audio, video |
| Token watermark | "Kirchenbauer-style" | Biased-sampling text watermark detectable via green-token z-score |
| Stable Signature | "image watermark" | Fine-tuned-decoder watermark; ICCV 2023 |
| C2PA | "the metadata standard" | Cryptographically signed tamper-evident provenance metadata |
| Paraphrase robustness | "does rewording break it" | Text watermark property; currently limited |
| Fine-tune removal | "adversarial unwatermark" | Attack that removes image watermark via decoder fine-tuning |
| Cross-modal detector | "unified SynthID" | November 2025 unified API across modalities |

## Mais leitura 延伸阅读

- [Kirchenbauer et al. — A Watermark for Large Language Models (ICML 2023, arXiv:2301.10226)](https://arxiv.org/abs/2301.10226) o mecanismo de marca de água de tokens
- [Fernandez et al. — Stable Signature (ICCV 2023, arXiv:2303.15435)](https://arxiv.org/abs/2303.15435) papel de marca de água de imagem
- ["Stable Signature is Unstable" (arXiv:2405.07145)](https://arxiv.org/abs/2405.07145) o ataque de remoção
- [Google DeepMind — SynthID](https://deepmind.google/models/synthid/) a marca de água transmodal
- [C2PA 2.2 Explainer (2025)](https://c2pa.org/specifications/specifications/2.2/explainer/Explainer.html) Padrão de metadados
