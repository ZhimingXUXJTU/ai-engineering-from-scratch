# La négociation et la négociation

> Les agents négocient des ressources, des prix, des affectations de tâches et des conditions. L'ensemble de référence de 2026 est clair: NegotiationArena (arXiv:2402.05863) montre que les LLM peuvent améliorer les paiements de ~20% via la manipulation de la personnalité ("désespoir"); " Mesurer les capacités de négociation " (arXiv:2402.15813) montre que l'acheteur est plus difficile que le vendeur et que l'échelle ne les aide pas  leur**OG-Narrator**(Générateur d'offres déterministes + narrator de LLM) a poussé le taux de négociation de 26,67% à 88,88%; la grande compétition de négociation autonome (arXiv:2503.06416) a mené environ 180 000 négociations et a constaté que**chain-of-thought-concealing**Les agents gagnent en cachant le raisonnement des homologues; Bhattacharya et coll. 2025 sur les métriques du projet de négociation de Harvard classé Llama-3 le plus efficace, Claude-3 le plus agressif, GPT-4 le plus juste. Cette leçon met en œuvre le protocole de réseau de contrat (l'ancêtre de la FIPA, leçon 02), câble un acheteur / vendeur de style LLM, exécute une décomposition de style OG-Narrateur et mesure comment le taux de transaction change avec chaque choix structurel.

> **【中文解读】**Ce chapitre présente les stratégies de négociation et de négociation entre les agents dans la répartition des ressources et la répartition des tâches.

> **【拓展：negotiation bargaining→具体应用】**协商和讨价还价是多代理 资源分配的核心机制――三种协商策略:(1) 合作型Agent 追求整体利益最大化;(2) 竞争型Agent 追求自身利益最大化;(3) 混合型兼顾个体和整体── Dans l'économie 代理, les négociations sont généralement menées par la mise en œuvre d'un protocole de proposition-réponse structuré, semblable à un protocole de réseau de contrats(Contract Net Protocol) ⋅


**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib) | **语言:** Python（标准库）
**Prerequisites:** Phase 16 · 02 (FIPA-ACL Heritage), Phase 16 · 09 (Parallel Swarm Networks) | **前置知识:** Phase 16 · 02（FIPA-ACL 遗产），Phase 16 · 09（并行群体网络）

>  **【前置】**Les résultats de la recherche ont été obtenus en vue de la réalisation de la première phase du projet.
>  **【类比】**L'agent 协商 = "二手市场砍价"―LLM 通过 persona 操纵(装穷)能多 20%;隐藏推理过程的 Agent 赢对手看不到你的底线──OG-Narrator 把协商拆为"确定性提议生成"+"LLM 叙述",deal rate 26%→89%──模型差异:Llama-3 最有效、Claude-3 强势、GPT-4公平 最选即模型选风格──
**Time:** ~75 minutes | **时间:** ~75 分钟

## ♪ Problème ♪ Introduction du problème ♪

Les deux agents doivent s'entendre sur un prix. Laissant à eux-mêmes des indications purement linguistiques, les LLM 2024-2026 concluront des transactions à des taux étonnamment bas (~ 27% sur des offres strictement paramétrisées dans arXiv:2402.15813).

> 两个代理 需要就价格达成. 在纯语言提示下,2024-2026年 LLM 成交率惊地低在 arXiv:2402.15813紧密参数化议议价中约27%) 规模化不能解决:GPT-4在议价结构上不比GPT-3.5好;它只是在议价上*语言*上更好

Le problème principal est que les LLM confondent deux emplois  décider de l'offre et de raconter l'offre. OG-Narrateur les a séparés: un générateur d'offres déterministe compute les mouvements numériques; le LLM ne raconte que. Le taux de transaction augmente à ~89%.

> Le problème fondamental est que le LLM a combiné deux tâches: décider des offres et des offres de commentaires.

Ce qui reflète une conclusion classique multi-agent: découpler le mécanisme de la couche de communication gagne. Le protocole de réseau de contrat (FIPA, 1996; Smith, 1980) est le mécanisme de référence du marché des tâches.

> Ceci reflète un classique multi-agent découverte: le mécanisme et la communication est le moyen de la victoire.

## Concept Le concept central

### Réseau de contrat, en un seul paragraphe

Le protocole de 1980 de Smith sur le réseau des contrats: a **manager**diffuse une **call for proposals (cfp)**- le président .**bidders**répondez avec **propose**messages contenant leurs offres; le gestionnaire choisit un gagnant et envoie **accept-proposal**au gagnant et **reject-proposal**Le gagnant fait le travail.**refuse**L' FIPA a codifié cette proposition comme:`fipa-contract-net`protocole d'interaction.

> Accord de contrat de Smith 1980:**管理者**广播**提案请求（cfp）**Le dépôt de la commission**投标人**Réponse contenant son prix**提案**消息; gestionnaire choisi le gagnant并向获胜者发送**接受提案**, à l' élu**拒绝提案**❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖**拒绝**(投标人拒绝提案)  La FIPA a adopté une politique de réduction des coûts de la participation des entreprises dans le secteur de l'énergie`fipa-contract-net`- Je suis en train de parler.

### Pourquoi OG-Narrateur gagne

"Mesurer les capacités de négociation des modèles linguistiques" (arXiv:2402.15813) a observé que:

> "Méager la capacité de la langue modèle de la capacité de la langue" (ArXiv:2402.15813) observe:

- Les LLM enfreignent souvent les règles de négociation (offre à des prix absurdes, ignorez les ZOPA de l'autre partie).
  L'économie de marché est une société de commerce qui a une politique de concurrence et de commerce.
- Ils s'ancrent mal (acceptent de mauvaises offres d'abord; contre-offres à des montants symboliques plutôt que stratégiques).
  Le prix de la première tour est un prix de retour symbolique et non stratégique.
- Les modèles plus grands rendent le langage plus plausible avec une erreur stratégique similaire.
  Les grandes méthodes peuvent produire des langages plus raisonnables, mais des erreurs de stratégie similaires existent.

La décomposition du narrateur:

```
           ┌──────────────────┐        ┌──────────────────┐
  state  → │ offer generator  │ price → │  LLM narrator    │ → message
           │  (deterministic) │        │  (writes the     │
           │                  │        │   human-style    │
           └──────────────────┘        │   accompaniment) │
                                       └──────────────────┘
```

Le générateur d'offres est une stratégie de négociation classique: un modèle de négociation de Rubinstein, une stratégie de Zeuthen ou un simple coup de tête sur le prix.

Le taux de transaction augmente parce que:
- Les prix restent dans la zone de négociation.
- Les ancres sont stratégiques, pas émotionnelles.
- Le LLM fait ce qu'il est bon à faire: écrire.

> Le taux de change augmente parce que:
> - Le prix reste dans la zone de prix.
> - 点是战略性的, mais pas émotionnelles.
> - LLM faire ce qu'il y a de bon: écrire.

### Les résultats de négociationArena

Le rapport de référence canonique est fourni par arXiv:2402.05863.

> Le rapport de l'OMS a été publié en décembre.

- Les LLM peuvent améliorer les paiements de ~20% en adoptant des personas ("Je suis désespérément prêt à vendre ce vendredi")  La manipulation de la personnalité est une véritable tactique.
  L'utilisation de la personnalité peut augmenter les bénéfices d'environ 20% (en chinois: "I急需在本周五前卖掉这个")
- Les agents équitables/coopératifs sont exploités par ceux qui sont opposés; la défense exige une contre-position explicite.
  En français, le terme "agent équitable" signifie "agent opposé à l'action".
- Les couples symétriques convergent à des résultats inéquitables sur environ 40% des scénarios de référence.
  En français, les résultats obtenus sont inéquitables sur une base de 40% environ.

Ce n'est pas "les LLM sont de mauvais négociateurs". C'est "les LLM négocient trop comme les humains, y compris les parties exploitables".

> Ce n'est pas "LLM est un mauvais négociateur" mais "le mode de négociation de LLM est trop humain, y compris les parties utilisables".

### Le cauchemar de la chaîne de pensée

Le Grand Concours de négociation autonome (arXiv:2503.06416) a mené environ 180 000 négociations sur de nombreuses stratégies de LLM. Les gagnants ont caché leur raisonnement à leurs homologues:

> Le concours de consultation autonome à grande échelle (ArXiv:2503.06416) a été mené sur 180.000 consultations sur de nombreuses stratégies de LLM.

- Si un agent imprime "Je vais seulement à$75; my reservation price is $70" dans un scratchpad visible au public, l'adversaire le lit.
  Si l'agent va "je ne vais qu'arriver"$75；我的保留价是 $70" imprimé sur le plan public, à lire à la main.
- Les gagnants calculent la stratégie en privé; le canal de sortie ne contient que l'offre et le minimum de narration requis.
  Traduction anglaise: 获胜者私下计算策略;输出通道只包含报价和最低限度的叙述──

Il s'agit d'un écho de 2026 de la théorie classique du jeu (Aumann 1976 sur la rationalité et l'information): révéler votre valorisation privée coûte la rémunération. LLM ne l'intuition et heureusement taper leurs réserves dans des traces de raisonnement qui deviennent visibles à l'autre.

> C'est le classique blog de l'Aumann 1976  Sobre Raciology y Information) dans le 2026 Réponse: révéler les pertes de bénéfices de l'évaluation privée.

Résumé de l'ingénierie: séparer le contexte privé du scratchpad du contexte public.

> 工程要点:将私人草稿本上下文与公开消息上下文分离── ceci n'est pas facultatif──

### Bhattacharya et coll. 2025  classement des modèles

Sur les mesures du projet de négociation de Harvard (négociation en principe, respect de la BATNA, réciprocité des intérêts):

> Dans le cadre de la politique de coopération, les pays de l'UE ont adopté des mesures de coopération en matière de coopération et de coopération.

- **Llama-3**était le plus efficace pour négocier des offres (taux de transaction + remboursement).
  Le mot grec traduit par " le mot grec "**Llama-3**Le taux de conversion + de bénéfices est le plus efficace dans le domaine de l'échange.
- **Claude-3**Il a été le négociateur le plus agressif (ancres élevés, concessions tardives).
  Le mot grec traduit par " le mot grec "**Claude-3**C'est le plus agressif des négociateurs.
- **GPT-4**était le plus équitable (moins de variance de rémunération entre les couples).
  Le mot grec traduit par " le mot grec "**GPT-4**Le taux de change est le plus bas.

Il s'agit d'un instantané de 2025. Le point n'est pas lequel modèle gagne en avril 2026  c'est que les différents modèles de base ont des styles de négociation persistants.

> C'est le rappel de l'année 2025: le point de vue n'est pas sur le modèle qui remportera le 4 avril 2026, mais sur le modèle de base qui aura une forme de négociation durable.

### Allocation des tâches par contrat net + LLM

La réutilisation moderne du réseau de contrat pour les LLM multi-agents:

> 合同网在现代 LLM 多 Agent 中中重用:

1. L'agent directeur décompose une tâche en unités.
   Le directeur de l'entreprise va décomposer les tâches en unités.
2. Les émissions `cfp`avec une description des tâches aux agents des travailleurs.
   Le rôle de l'agent dans la gestion des tâches`cfp`Il y a une autre.
3. Chaque travailleur retourne une offre: `(price, eta, confidence)`où le prix pourrait être des jetons, des unités de calcul ou des dollars.
   Chaque travailleur retourne à un prix:`(price, eta, confidence)`Le prix peut être un symbole, calculé en unités ou en dollars.
4. Le gestionnaire choisit les gagnants (singles ou multiples, selon la tâche) et les prix.
   Le gouvernement a décidé de créer un gouvernement qui ne serait pas le seul gouvernement à pouvoir faire le choix de la région.
5. Les travailleurs rejetés sont libres de faire des offres pour d'autres tâches.
   Le travail est rejeté.

Cette échelle dépasse bien 100 travailleurs parce que la coordination est de diffusion et de réponse, pas de chat synchrone.

> Il peut être très bien étendu à plus de 100 employés, car le coordonnage est un mode de diffusion-réponse, et non un mode de conversation.

### L'entreprise de gestion des droits de propriété intellectuelle et des parties prenantes

NeurIPS 2024 (https://proceedings.neurips.cc/paper_files/paper/2024/file/984dd3db213db2d1454a163b65b84d08-Paper-Datasets_and_Benchmarks_Track.pdf) introduit des jeux scortables multipartis avec **secret scores**et **minimum-acceptance thresholds**. Chaque partie prenante possède des services publics privés; le LLM doit les déduire des messages. C'est la généralisation de la négociation bipartite à la formation de coalitions de N-partis.

> NeurIPS 2024 a été introduit avec**秘密分数**和**最低接受阈值**Les différents types de travail sont utilisés dans les entreprises et les entreprises, et les entreprises et les entreprises sont utilisées dans les entreprises.

### La règle de la narration contre le mécanisme

Dans tous les critères de référence de négociation de 2024 à 2026, la règle d'ingénierie constante est la suivante:

> Laissez le LLM raconter, ne laissez pas le LLM calculer l'offre.

> 让LLM 叙述──不要让LLM 计算报价──

Si l'offre doit être un nombre (prix, ETA, quantité), générez-la déterministiquement à partir de l'état de négociation et faites en sorte que le LLM produise le cadrage.

> Si le prix est numérique, il doit être calculé à partir du niveau de négociation, il doit être généré en fonction de la situation de négociation, il doit être créé un cadre.

## Construisez-le en main
```figure
a5-og-narrator
```

## Faites-le

`code/main.py`les implémentations:

- `ContractNetManager`- Je suis là .`ContractNetTask`- Je suis là .`Bid` gestionnaire + soumissionnaires, diffusion de la télévision, collecte de propositions, récompense.
  Le mot grec traduit par " le mot grec "`ContractNetManager`- Je suis là.`ContractNetTask`- Je suis là.`Bid` 管理者 + 投标人,广播 cfp,收集提案,授标──
- `og_narrator_bargain(state, rng)` Acheteur OG-Narrateur: concession déterministe de style Zeuthen vers le milieu.
  Le mot grec traduit par " le mot grec "`og_narrator_bargain` OG-Narrateur 买方:确定性 Zeuthen 风格向中间点让步──
- `seller_response(state, rng)` politique déterministe de contre-offre du vendeur (la vérité structurelle de base pour les deux styles).
  Le mot grec traduit par " le mot grec "`seller_response` 确定性卖方回价策略 (··················································································································································································································································································································································································································································································································
- `naive_llm_bargain(state, rng)` simulation d'une négociation entièrement LLM: choisit des prix avec une forte variance, souvent en dehors de la ZOPA.
  Le mot grec traduit par " le mot grec "`naive_llm_bargain` 模拟全 LLM 议价者:以高方差选价,经常超出 ZOPA。
- Mesure: taux de transaction sur 1000 essais avec prix de réservation frais échantillonnés par essais.
  Le taux de conversion de 1000 fois de l'essai, le taux de conservation de chaque tentative.

Je vais courir .

```
python3 code/main.py
```

Les résultats attendus: taux de transaction naïf-LLM ~65-75%; taux de transaction OG-Narrateur ~85-95%; l'écart de 15-25 points est l'avantage structurel de décomposer la génération d'offres de la narration.

> 预期输出:朴素 LLM 成交率约65-75%;OG-Narrator 成交率约85-95%;15-25 个百分点的差距是将报价生成与叙述解的结构优势──加上一个三个投标者和一个任务的合同网任务市场分配示例──

## Utilisez-le.

`outputs/skill-bargainer-designer.md`Il conçoit un protocole de négociation: qui génère des offres (déterministique ou LLM), qui raconte, comment les scratchpads privés se séparent des messages publics et comment le taux de transaction est surveillé.

> `outputs/skill-bargainer-designer.md`设计一个议价协议:谁生成报价 (qui génère des offres) 确定性 (qui génère des offres) ou LLM (qui décrit des propositions), qui décrit comment le projet privé a été séparé de la public information et comment surveiller le taux de conversion (qui est le taux de conversion).

## Envoyez-le en ligne .

Liste de contrôle des négociations de production:

- **Separate scratchpad.**L'État privé n'atteint jamais le contexte de l'autre.
  Le mot grec traduit par " le mot grec "**分离草稿本。**L'état privé ne parviendra jamais à la hauteur du défendeur.
- **Deterministic offer generation.**Prix, quantités, dates d'arrivée: calculer, ne pas demander.
  Le mot grec traduit par " le mot grec "**确定性报价生成。**价格、数量、ETA: calcul, ne pas vous faire remarquer
- **Validate all incoming offers**rejeter les offres hors ZOPA à la limite du protocole.
  Le mot grec traduit par " le mot grec "**验证所有传入报价**Selon le modèle, la limite de l'accord refuse les offres extérieures de ZOPA.
- **Bound rounds.**3 à 5 coups maximum; escalade à la médiation en cas d'impasse.
  Le mot grec traduit par " le mot grec "**限制轮次。**Le maximum de 3 à 5 roues;
- **Measure deal rate and payoff variance**Une baisse du taux d'opération est un symptôme  souvent une dérive rapide ou une attaque par contrepartie.
  Le mot grec traduit par " le mot grec "**持续测量成交率和收益方差。**Le taux de conversion est généralement un symptôme de déménagement ou d'attaque de la part de l'autre.
- **Log all rejected proposals**Pour les gestionnaires de réseau de contrats, les soumissionnaires perdants doivent comprendre pourquoi.
  Le mot grec traduit par " le mot grec "**记录所有被拒绝的提案**及确定性理由── Pour les gestionnaires de réseau de contrats, les candidats à l'élection doivent comprendre les raisons──

## Les exercices

1. On court .`code/main.py`Confirme que OG-Narrateur est plus que naïf-LLM sur le taux de transaction.
   Le mot " l' économie " est traduit par " l' économie ".`code/main.py`❖ Confirmer OG-Narrateur en taux de réussite supérieur à un LLM simple ― combien de avantages ?
2. Mise en œuvre **persona-based payoff improvement**L'acheteur adopte un personnage " désespéré d'acheter cette semaine " dans le récit seulement, offre générateur inchangé.
   Le récit de la prophétie**基于人格的收益改进**(arXiv:2402.05863)  le consommateur adopte uniquement dans le récit le personnage "本周急需购" , le prix générateur ne change pas.
3. Implémentation de la chaîne de pensée **concealment**: maintenir une chaîne de scratchpad privée qui n'est pas transmise à la contrepartie.
   Le récit de la création**隐藏**Il est également question de la rédaction de la lettre de l'auteur:
4. Lorsque toutes les offres dépassent la réserve, comment le gestionnaire décide-t-il entre le prix le plus bas et le prix le plus élevé?
   Le contrat est étendu à N 投标人拍卖带保留价. Lorsque toutes les soumissions dépassent le prix de réservation, comment le gestionnaire choisit-il entre le prix le plus bas et la qualité la plus élevée ?
5. Lisez Bhattacharya et collègues 2025 sur les métriques du projet de négociation de Harvard. Implémenter deux négociateurs avec des styles différents (agressif contre juste). Mesurer la variance de rémunération sous des paires symétriques et asymétriques.
   Le thème de la négociation de l'Afghanistan avec le gouvernement de l'Afghanistan est le développement d'un projet de loi qui vise à améliorer la qualité des relations entre les pays.

## Les termes clés

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Contract Net / 合同网 | "Task market" / "任务市场" | Smith 1980, FIPA 1996. cfp + propose + accept/reject. The canonical task-market. / Smith 1980, FIPA 1996。cfp + propose + accept/reject。规范的任务市场。 |
| ZOPA / 可能协议区 | "Zone of possible agreement" / "可能协议区域" | Overlap between buyer's max and seller's min. Offers outside it cannot close. / 买方最大值和卖方最小值的重叠。超出此范围的报价无法成交。 |
| BATNA / 最佳替代方案 | "Best alternative to a negotiated agreement" / "谈判协议的最佳替代方案" | Your fallback if this deal fails. Sets your reservation price. / 如果交易失败的后备方案。设定你的保留价。 |
| OG-Narrator / OG-叙述者 | "Offer generator + narrator" / "报价生成器 + 叙述者" | Decomposition: deterministic offer, LLM narration. / 分解：确定性报价，LLM 叙述。 |
| Zeuthen strategy / Zeuthen 策略 | "Risk-minimizing concession" / "风险最小化让步" | Classical offer-generator that concedes based on risk limits. / 基于风险限制让步的经典报价生成器。 |
| Rubinstein bargaining / Rubinstein 议价 | "Alternating-offer equilibrium" / "交替报价均衡" | Game-theoretic model for infinite-horizon bargaining with discounting. / 带折现的无限期议价博弈论模型。 |
| CoT concealment / CoT 隐藏 | "Hide your reasoning" / "隐藏推理" | Winners in arXiv:2503.06416 kept private scratchpads; public channel shows offer only. / arXiv:2503.06416 的获胜者保持私人草稿本；公开通道只显示报价。 |
| Persona manipulation / 人格操纵 | "Emotional posturing" / "情绪姿态" | arXiv:2402.05863: ~20% payoff gain from desperation/urgency personas. / arXiv:2402.05863：绝望/紧迫人格带来约 20% 的收益增益。 |

## Encore une lecture

- [NegotiationArena](https://arxiv.org/abs/2402.05863) l'indice de référence; constatations sur la manipulation et l'exploitation de la personne
- [Measuring Bargaining Abilities of Language Models](https://arxiv.org/abs/2402.15813) OG-Narrateur et le résultat de l'acheteur-plus dur que le vendeur
- [Large-Scale Autonomous Negotiation Competition](https://arxiv.org/abs/2503.06416) ~ 180 000 négociations; la dissimulation de la chaîne de pensée gagne
- [LLM-Stakeholders Interactive Negotiation (NeurIPS 2024)](https://proceedings.neurips.cc/paper_files/paper/2024/file/984dd3db213db2d1454a163b65b84d08-Paper-Datasets_and_Benchmarks_Track.pdf) Jeux scortables multi-partis avec des utilitaires secrets
- [Smith 1980 — The Contract Net Protocol](https://ieeexplore.ieee.org/document/1675516) le mécanisme classique, IEEE Transactions sur ordinateur
