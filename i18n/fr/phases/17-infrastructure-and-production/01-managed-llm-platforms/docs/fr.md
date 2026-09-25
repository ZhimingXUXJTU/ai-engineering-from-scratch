# Plateformes de gestion de la LLM  Bedrock, Vertex AI, Azure OpenAI 

> Trois hypercalers, trois stratégies distinctes. AWS Bedrock est un marché modèle  Claude, Llama, Titan, Stabilité, Cohere derrière une API. Azure OpenAI est un partenariat exclusif OpenAI plus des unités de débit fournies (PTU) pour une capacité dédiée. Vertex AI est le premier Gemini avec la meilleure histoire multimodal et long-context. En 2026, l'analyse artificielle mesure Azure OpenAI à ~ 50 ms en moyenne et Bedrock à ~ 75 ms sur les équivalents Llama 3.1 405B  Les PTU expliquent le fossé parce que la capacité dédiée bat partagée sur demande. La règle de décision n'est pas "qui est le plus rapide" mais "qui catalogue de modèle et FinOps surface correspond à mon produit". Cette leçon vous apprend à choisir avec les compromis écrits, pas les vibrations.

> **【中文解读】**Ce chapitre présente les types et les comparaisons des modèles de services fournis par Google et autres.

>  **【前置】**學本節前 請先掌握:Phase 11 (LLM Engineering) 全部你已經會使用OpenAI/Anthropic API 调模型;Phase 13 (Tools & Protocols) 理解 MCP等协议──本节讲生产部署选哪个云不是技术问题,是商业+合规+技术综合决策──

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy cost-and-latency comparator) | **语言:** Python（标准库，成本-延迟比较器）
**Prerequisites:** Phase 11 (LLM Engineering), Phase 13 (Tools & Protocols) | **前置知识:** Phase 11（LLM 工程）, Phase 13（工具与协议）
**Time:** ~60 minutes | **时间:** ~60 分钟

## Objectifs d'apprentissage

- Nombrez les trois stratégies de plateforme (marché vs exclusive vs Gémeaux-première) et correspondrez chacune à un cas d'utilisation du produit.

>  **【类比】**Le programme de formation en médecine est un programme de formation en médecine.**AWS Bedrock**= 美食广场(((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((**Azure OpenAI**= 米其林餐厅(OpenAI 独家合作,PTU 专属容量,延迟最低 ~50ms,但贵且绑定OpenAI);(3) **Vertex AI**= Sujet: Résultats du projet de loi sur les produits alimentaires (en anglais et en français)

> ️ **【易错点】**托管平台选型的 3 个坑: ) **只看标价**Bedrock 上 Claude 比 Anthropic 直连贵15-20% (云税),但合规和统一计值钱;做 TCO (总拥有成本)而非单价比较――(2) **忽略数据驻留** Les données des utilisateurs européens doivent rester en Europe, choisir Azure EU 区域 ou Bedrock eu-central-1; la transmission de données transfrontalière est contraire au RGPD。(3) **没做厂商锁定评估** utiliser OpenAI PTU 后想换 Bedrock 转写SDK 和 prompt 格式; utiliser LiteLLM 等抽象层降低锁风险──
  Le modèle de production de produits est le modèle de production de produits.
- Expliquez ce que les unités de débit fournies (PTU) vous achètent dans Azure OpenAI et pourquoi Bedrock à la demande lit généralement environ 25 ms plus lentement à l'échelle 405B.
  Expliquer ce que l'unité de déploiement de masse de l'Azure OpenAI (PTU) a apporté, ainsi que pourquoi la déploiement de masse de Bedrock à une échelle de 405B est généralement lent d'environ 25ms.
- Décrire la surface d'attribution FinOps pour chaque plateforme (profiles d'inference d'application Bedrock vs Vertex projet par équipe vs champs d'action Azure + réservations PTU).
  Le projet de conception de l'application est un projet de conception de l'application de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de conception de concep
- Écrivez une politique de "double fournisseur minimum" et expliquez pourquoi le verrouillage d'un seul fournisseur est une erreur coûteuse en 2026.
  Le système de "double fournisseurs minimum" est un système de logement de deux fournisseurs.

## Le problème , l' introduction du problème

Vous avez choisi Claude 3.7 Sonnet pour votre produit. Vous devez maintenant le servir. Vous pouvez appeler l'API Anthropic directement, ou vous pouvez l'appeler via AWS Bedrock, ou vous pouvez passer par un gateway. L'API directe est la plus simple; Bedrock ajoute BAAs, points de fin VPC, IAM et attribut CloudWatch. Le gateway ajoute failover, facturation unifiée et limites de tarifs entre les fournisseurs.

> Vous avez choisi le produit Claude 3.7 Sonnet. Vous devez le déployer. Vous pouvez utiliser directement l'API Anthropic, ou vous pouvez utiliser AWS Bedrock.

La question la plus profonde est le catalogue. Si vous avez besoin de Claude et Llama et Gémeaux dans le même produit, vous ne pouvez pas les acheter tous à partir d'un seul endroit à moins que ce lieu soit Bedrock plus Vertex plus Azure OpenAI simultanément. Les hyperscalers ne sont pas interchangeables  ils ont chacun fait un pari différent sur qui possède la couche modèle.

> Si vous avez besoin de Claude, Llama et Gémeaux dans le même produit, vous ne pouvez pas acheter tous les modèles à partir d'un seul endroit, sauf en utilisant simultanément Bedrock + Vertex + Azure OpenAI.

Cette leçon trace les trois paris, l'écart de latence, l'écart de FinOps et le risque de verrouillage.

> Ce cours trace trois différences de retard, de fin d'opération et de mise en place de la stratégie.

> **【中文解读】**选择 LLM 后, "在哪里部署" est une décision de niveau infrastructure.  Directement utiliser API 最简单, mais manque de contrôle de niveau d'entreprise;                                                                                                                                                                                                                                           

> **【拓展：LLM 部署模式】**Le modèle de déploiement de services de LLM de 2024 à 2026 a connu des développements allant de l'" API directe " à la " cloud platform托管 " à la " IA " .

## Le concept de base.

> **【中文解读】**La stratégie de la plateforme de LLM de 三大云厂商 est nettement différente: AWS Bedrock est un " modèle集市 ", un regroupement de plusieurs fournisseurs; Azure OpenAI est un " exclusive cooperation ", un " exclusive cooperation ", un " exclusive collaboration " pour OpenAI 模型; Vertex AI est un " gémein  priorité ", un point de vente à la fois sur la base de la capacité de production et de diffusion multimédia.

> **【拓展：全球 LLM 云平台格局】**En dehors de trois grands hyperscaler, en 2026, il y a encore des choses à prévoir: Cloudflare Workers AI(random推理) ✓ Ensemble AI(Open Source Model推理平台, $0.18/M de jetons pour Llama 3.1 70B) ✓ Grroq(LPU 推理引擎,TTFT < 20ms) ✓ Cerebras(CS-3 wafer-scale 推理,2000+ de jetons/s) ✓

### Trois stratégies

**AWS Bedrock**La société a été créée par le groupe de sociétés de recherche et de recherche de l'industrie du marketing.

> **AWS Bedrock** 模型集市──Claude(Anthropic)、Llama(Meta)、Titan(AWS 自有)、Stabilité(图像)、Cohere(嵌入)、Mistral, ainsi que l'image et le module de l'imagerie──un API、un IAM 界面、un CloudWatch 导出──Bedrock 注是客户想要可选择性而不是单一模型──

**Azure OpenAI** le partenariat exclusif. Vous obtenez GPT-4 / 4o / 5 / o-série, DALL·E, Whisper et fine-tuning des modèles OpenAI dans les centres de données Azure. Aucun modèle non OpenAI dans le catalogue "Azure OpenAI Service"  ceux qui vont à Azure AI Foundry (produit séparé).

> **Azure OpenAI** 独家合作──你在Azure 数据中心获得 GPT-4/4o/5/o 系列、DALL·E、Whisper 和 OpenAI 模型微调──"Azure OpenAI Service" 目录中没有非 OpenAI 模型那些在Azure AI Foundry(独立产品) 中──Azure 注是OpenAI 保持前沿地位和客户想要对此关系的企业级控制──

**Vertex AI** Gémeaux d'abord, tout le reste en deuxième. Gémeaux 1.5 / 2.0 / 2.5 Flash et Pro, plus Model Garden (troisième partie).

> **Vertex AI** Gémeaux  priorités,其他其次── Gémeaux 1.5/2.0/2.5 Flash 和 Pro,加上 Model Garden(第三方)──Vertex 注是多模态长上下文1M 代币的 Gémeaux 上文是差异化因素──

### L'écart de latence à l'échelle

L'analyse artificielle présente des critères de référence continus. Sur les déploiements Llama 3.1 405B équivalents (partagés à la demande), la latence médiane du premier jeton Azure OpenAI est d'environ 50 ms; Bedrock est d'environ 75 ms. L'écart n'est pas une défaillance AWS  c'est une différence de modèle de capacité. Azure vend des PTU (Unités de débit fournies), qui réservent la capacité de la GPU à votre locataire. L'équivalent de Bedrock (Provisioned Throughput) existe mais commence à environ 21 $/heure par unité, et la plupart des clients restent sur le partage sur demande.

> L'analyse artificielle 运行持续基准测试。在等效的Llama 3.1 405B 部署) 共享按量) 上,Azure OpenAI 中位首代代币 延迟约50ms;Bedrock 约75ms。差距不是AWS 问题而是容量模型差异。Azure 销售PTU(预置吞吐量单位),为您租户预留GPU 容量。Bedrock 等效功能存在但起价约$21/户小时/按量模式,大多数客户使用共享量模式。

La capacité partagée sur demande est en concurrence avec le trafic de chaque autre client. La capacité dédiée n'est pas. Si votre SLA de produit est TTFT < 100 ms à P99, vous achetez soit des PTU sur Azure, achetez Bedrock Provisioned Throughput, ou acceptez la variance par défaut.

> 按量共享容量与所有其他客户的流量竞争 GPU资源──专用容量不会──如果你的产品 SLA是 P99 TTFT < 100ms,你要么在Azure 购买PTU,要么购买Bedrock Provisioned Throughput,要么接受默认方差──

> **【中文解读】**La différence de retard est essentielle à la différence de "modèle de capacité". Dans le déploiement de masse partagée, votre demande est en concurrence avec la concurrence de tous les autres clients.

### Économie du débit fourni

Azure PTUs: un bloc réservé de calcul d'inférence. Jusqu'à ~ 70% d'épargne par rapport à la demande pour les charges de travail prévisibles. Coûts fixes par heure indépendamment du trafic  vous payez pour la réservation même lorsque vous êtes en activité. Le break-even est généralement d'environ 40-60% d'utilisation soutenue.

> Azure PTU: pré-reserve des blocs de calcul. Pour une charge de travail prévisible, les économies de charge de travail peuvent atteindre environ 70%.

Travail fourni par le lit: $21-$50 par heure selon le modèle et la région. mathématiques similaires  break-even est environ la moitié de l'utilisation maximale.

> Résultats fournis par Bedrock: 每小时 $21-$50, dépend du modèle et de la région. Les modèles économiques similaires représentent environ la moitié du taux d'utilisation de la valeur maximale.

La capacité fournie par Vertex est vendue par SKU Gemini; les prix varient selon le modèle et la région et sont moins publiquement annoncés.

> Vertex  préposition de la capacité selon Gemini SKU  vente; prix par modèle et région, public information moins:.

### Surface FinOps  le différenciateur réel

**Bedrock Application Inference Profiles**Les données de référence sont les plus propres du marché.`team`- Je suis là .`product`- Je suis là .`feature`; parcourir toutes les invocations de modèle à travers elle; CloudWatch décompose le coût par profil sans traitement post-processé.

> **Bedrock Application Inference Profiles**C'est le programme de coût attribué le plus clair du marché.`team`- Je suis là.`product`- Je suis là.`feature` Marquer le fichier de configuration; par le biais de celui-ci, tous les modèles sont modifiés; CloudWatch  sans traitement ultérieur, décomposable en fonction du coût du fichier de configuration.

**Vertex**Vous modélisez chaque équipe comme un projet GCP, mettez des étiquettes sur chaque ressource, et utilisez BigQuery Billing Export + DataStudio pour les roulements. Plus de travail, mais BigQuery vous donne un SQL arbitraire sur les données de coûts.

> **Vertex**归因是项目-per-team加无处不在标签――你将每个团队建模为一个GCP项目,放置标签在每个资源上,使用BigQuery Billing Export + DataStudio 进行汇总――工作量更大,但BigQuery 允许你对成本数据执行任意SQL――

**Azure**Les tags sont hérités des groupes de ressources, pas des demandes, donc l'attribution par demande nécessite des métriques personnalisées d'Application Insights ou une passerelle qui imprime les en-têtes.

> **Azure**En fonction de la participation/réseau de rôle du domaine de la marque, PTU  réservé comme un objet de coût de premier ordre.

Le schéma: Bedrock est le plus propre natif, Vertex est le plus flexible via BigQuery, Azure est le plus opaque à moins que vous n'ayez un instrument.

> 总结:Bedrock 原生最清晰,Vertex 通过 BigQuery 最灵活,Azure 除非自行埋点否则最不透明──

> **【中文解读】**FinOps (en anglais FinOps) est la plus faible quantité de l'infrastructure LLM. Les profils d'inference d'application de Bedrock sont actuellement les plus précis de l'origine générée en fonction du coût de répartition de la mise en œuvre.

> **【拓展：LLM FinOps 实践】**企业 LLM  spending in 2025 year grew average 300% (Flexera 2025 云状态报告) 常见 FinOps 策略包括: 1) 按代币 消耗设置团队预算告警; 2) 使用缓存层(Semantic Cache) 减少重复调调用约30-40%; 3) 模型路由简单任务用小模型、复杂任务用大模型,可节省50%+ 成本; 4) 批量API在非实时场景可降低50% 价格;;

### Le risque de blocage est de 2026

L'engagement d'un hypercalculateur était bien quand un modèle dominait. En 2026, la frontière bouge mensuellement  Claude 3.7 un trimestre, Gemini 2.5 le trimestre suivant, GPT-5 le trimestre suivant.

> Lorsqu'un modèle est dominé, un seul cloud peut aussi s'engager. Le modèle avant-goût de 2026 est en évolution.

Les équipes de travail adoptent le modèle suivant: deux fournisseurs minimum pour tout appel de LLM critique pour le produit. Bedrock plus Azure OpenAI est la paire commune  Claude d'un, GPT de l'autre, défaillance entre eux, même passerelle. L'augmentation des coûts est négligeable car les routes de passerelle sont optimales; l'augmentation de la disponibilité pendant les pannes (comme l'incident d'Azure OpenAI de janvier 2025, l'arrêt AWS us-east-1) est décisif.

> Modèle d'adoption du groupe de travail: tout produit clé LLM 调用双供应商最低策略。Bedrock + Azure OpenAI est la combinaison la plus couranteun fournit Claude, l'autre fournit GPT, via le même réseau connecté effectuer un décalage de transfert。 le coût augmente négligeable, car le réseau connecté est le meilleur; la disponibilité améliorée pendant la période机期 (en tant qu'Azure OpenAI en janvier 2025  AWS us-east-1 机) est décisive︎

> **【中文解读】**Le risque majeur d'infrastructure de 2026 est le verrouillage des fournisseurs. Le modèle avant-coût est en cours de remplacement chaque trimestre. Q1 avec Claude 3.7, Q2 avec Gemini 2.5, Q3 avec GPT-5. Le verrouillage d'une seule plate-forme signifie une capacité avant-coût de plus de 2/3 de la capacité. La meilleure pratique est la stratégie "double fournisseur minimum": Bedrock + Azure OpenAI est le plus courant, via un réseau de connexion, le coût augmente négligeable, mais la disponibilité augmente nettement en cas de défaillance.

> **【拓展：云厂商宕机事件】**En janvier 2025, Azure OpenAI a connu des pannes globales de plusieurs heures, affectant tous les clients d'entreprise ChatGPT de Azure. Cette même année, AWS us-east-1 a également connu des pannes graves. La stratégie de plusieurs fournisseurs a démontré sa valeur dans ces événements: lors d'un temps, le réseau se transforme automatiquement en flux vers un autre, réalisant un décalage de détection.

### Résidence des données, BAA et industries réglementées

Bedrock: BAA dans la plupart des régions; points d'extrémité VPC; barreaux.
Azure OpenAI: HIPAA, SOC 2, ISO 27001; résidence des données de l'UE; la réglementation par défaut de l'entreprise.
Vertex: HIPAA, GDPR, résidence des données par région; la pile de conformité de Google Cloud.

> La plupart des régions offrent des BAA; VPC 端点;防护──常见金融科技默认选择──
> Azure OpenAI:HIPAA、SOC 2、ISO 27001; données de l'UE;
> Vertex:HIPAA, RGPD, conformément aux données régionales; Google Cloud's compliance──

Les différences sont les politiques de conservation des données, la façon dont les journaux sont gérés et si la surveillance des abus lit votre trafic (option par défaut sur la plupart; opt-out disponible pour les entreprises).

> Les différences sont les stratégies de conservation des données, la manière de traiter les journaux et la surveillance de la mauvaise utilisation de votre trafic.

### Les chiffres que vous devriez vous rappeler

- TTFT médian d'Azure OpenAI sur les équivalents Llama 3.1 405B: ~50 ms (avec PTU).
  Le modèle de fonctionnement de l'application est basé sur le modèle de fonctionnement de l'application.
- TTFT médiane de la couche à la demande: ~75 ms.
  Le temps de réaction de la chaîne de télévision est de 75 ms.
- Travail fourni par le lit: $21-$50/h par unité.
  Le nombre de couches est de 7 à 7$21-$50/小时──
- Régulation de la PTU Azure: utilisation soutenue de 40 à 60%.
  Le taux d'utilisation continue de la PTU est de 40 à 60%
- Économies de PTU par rapport à la demande à haute utilisation: jusqu'à 70%.
  Le PTU en moyenne économise jusqu'à 70% en termes de taux d'utilisation élevé.

## Utilisez-le avec le cadre de réalisation
```figure
i4-platform-lanes
```

## Utilisez-le

`code/main.py`Il compare les trois plateformes sur une charge de travail synthétique  il modélise l'économie sur demande contre PTU, la variance TTFT et la fidélité de l'attribution des coûts.

> `code/main.py`Comparer les trois plateformes sur lesquelles la PTU est basée sur la production de modèles et la PTU est plus grande que la PTU.

> **【中文解读】**实践部分通过模拟工作负载对比三大平台──关键指标包括:TTFT(首代币延迟)、吞吐量、每百万代币 成本──通过调整利用率参数,可以直观看PTU在什么负载水平下比按量计费更划算──

## Envoyez-le . Produit .

Cette leçon produit `outputs/skill-managed-platform-picker.md`. Compte tenu du profil de la charge de travail (modèles nécessaires, TTFT SLA, volume quotidien, exigences de conformité), il recommande une plateforme primaire, un plan de réaction et un plan d'instrumentation FinOps.

> 本课产 出 `outputs/skill-managed-platform-picker.md` donner un certain nombre de fichiers de configuration de travail (en anglais seulement), il propose des plateformes principales, des plateformes de sélection et des programmes de fin d'options.

> **【拓展：生产环境平台选型 Checklist】**Le programme de gestion de la production et du traitement de l'environnement (LLC) est un programme de gestion de la production et de la gestion de l'environnement (LLC) qui vise à améliorer la qualité de l'emploi et à améliorer la qualité de l'emploi.

## Les exercices

1. On court .`code/main.py`À quelle utilisation durable Azure PTU surpasse la demande pour un modèle de classe 70B ?
   Le mot " l' économie " est traduit par " l' économie ".`code/main.py` Comparer les coûts de production de la plateforme à la moyenne de 40 à 60% de la publicité avec les coûts de production de la plateforme à la moyenne de 70 B.
2. Votre produit a besoin de Claude 3.7 Sonnet et GPT-4o. Concevez un déploiement de deux fournisseurs qui va à quel hypercaler, quel gateway est devant, quelle est la politique de défaillance ?
   Le produit de votre entreprise nécessite Claude 3.7 Sonnet 和 GPT-4o.
3. Un client de soins de santé réglementé a besoin de BAAs, de résidence de données US-East et de TTFT sous 100ms P99 .
   Un client de soins de santé sous surveillance a besoin de BAAs, de données de séjour et de P99 TTFT < 100ms.
4. Vous découvrez que votre facture de Bedrock a augmenté 4 fois ce mois-ci sans changement de trafic.
   Vous avez trouvé le nombre de pages de Bedrock 4 fois plus élevé que le nombre de pages de Bedrock.
5. Pour une charge de travail Claude de 100 millions de jetons par mois, qui est moins chère  API anthropique directe, Bedrock à la demande ou Bedrock Provisioned Throughput ?
   Pour le compte de 100 millions de jetons/mois de Claude 工作负载, lequel est le plus rentable 直接Anthropic API、Bedrock 按量还是Bedrock Provisioned Throughput?

## Les termes clés

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|------------------------|----------|
| Bedrock | "AWS LLM service" | Model marketplace across Claude, Llama, Titan, Mistral, Cohere | AWS 的 LLM 模型集市平台 |
| Azure OpenAI | "Azure's ChatGPT" | Exclusive OpenAI models in Azure datacenters with enterprise controls | Azure 独家托管 OpenAI 模型的企业服务 |
| Vertex AI | "Google's LLM" | Gemini-first platform with Model Garden for third-party models | Google 的 Gemini 优先 AI 平台 |
| PTU | "dedicated capacity" | Provisioned Throughput Unit — reserved inference GPUs, priced per hour | 预置吞吐量单位——独占推理 GPU 容量 |
| Application Inference Profile | "Bedrock tagging" | Per-product cost/usage profile with tags, CloudWatch-native | Bedrock 按产品归因的推理配置文件 |
| Model Garden | "Vertex catalog" | Vertex AI's third-party model section, separate from Gemini | Vertex AI 第三方模型目录 |
| Two-provider minimum | "LLM redundancy" | Policy of running every critical LLM path across ≥2 hyperscalers | 双供应商最低策略——关键 LLM 调用跨 2+ 云商 |
| BAA | "HIPAA paperwork" | Business Associate Agreement; required for PHI; provided by all three | 业务关联协议——HIPAA 合规必需 |
| Abuse monitoring | "the log watcher" | Provider-side safety scan on prompts/outputs; opt-out in enterprise | 平台侧的 prompt/输出安全扫描 |

## Encore une lecture

- [AWS Bedrock Pricing](https://aws.amazon.com/bedrock/pricing/) carte de taux d'autorisation et tarification de la capacité de production fournie.
- [Azure OpenAI Service Pricing](https://azure.microsoft.com/en-us/pricing/details/azure-openai/) Économie et cartes de taux de PTU.
- [Vertex AI Generative AI Pricing](https://cloud.google.com/vertex-ai/generative-ai/pricing) Les niveaux Gémeaux et les suppléments du modèle jardin.
- [Artificial Analysis LLM Leaderboard](https://artificialanalysis.ai/) des indicateurs de référence de latence et de débit continus entre les fournisseurs.
- [The AI Journal — AWS Bedrock vs Azure OpenAI CTO Guide 2026](https://theaijournal.co/2026/03/aws-bedrock-vs-azure-openai/) cadre de décision de l'entreprise.
- [Finout — Bedrock vs Vertex vs Azure FinOps](https://www.finout.io/blog/bedrock-vs.-vertex-vs.-azure-cognitive-a-finops-comparison-for-ai-spend) mécanique d'attribution côte à côte.
