# Les outils de l'équipe rouge  Garak, garde de llama, Pyrit  

> Trois outils de production encadrent la pile de l'équipe rouge de 2026. Llama Guard (Meta)  un classifiateur Llama-3.1-8B ajusté sur 14 catégories de danger MLCommons; le 2025 Llama Guard 4 est un classifiateur multimodale natif 12B taillé à partir de Llama 4 Scout. Garak (NVIDIA)  Scanner de vulnérabilité LLM open source avec des sondes statiques, dynamiques et adaptives pour les hallucinations, la fuite de données, l'injection rapide, la toxicité et les jailbreaks. PyRIT (Microsoft)  Campaignes multi-tournées de l'équipe rouge avec Crescendo, TAP et chaînes de convertisseurs personnalisées pour une exploitation profonde. Llama Guard 3 est documenté dans le "Llama 3 Herd of Models" de Meta (arXiv:2407.21783); Llama Guard 3-1B-INT4 dans arXiv:2411.17713; l'architecture de sonde de Garak dans github.com/NVIDIA/garak. Ces outils sont l'interface de production 2026 entre la recherche en équipe rouge (lesçons 12-15) et le déploiement (lession 17+).

> **【中文解读】**Ce chapitre présente les méthodes d'évaluation de la sécurité du système de contrôle des équipes rouges, utilisant des attaques automatisées pour détecter les lacunes de l'IA  système. Trois outils de production définissent la technologie de la équipe rouge en 2026: Llama Guard (Meta)  Llama-3.1-8B 分类器微调到14 MLCommons 危险类别;Garak(NVIDIA) 开源 LLM 漏洞扫描机,含静态、动态和自适应探针;PyRIT (Microsoft) 多轮红队活动,含 Crescendo、TAP 和自定义转换链──

> **【拓展：2026 红队技术栈 → 生产配置】**标准配置:Llama Guard 放在模型两侧(输入+输出),Garak 每晚运行回归测试,PyRIT 用于预发布活动。Prompt-Guard-86M est Meta's lightweight class输入分类器,与Llama Guard 配合使用。TrustyAI va Garak 及Llama Stack shields 集成进行端到端评估。

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, tool-architecture simulator and Llama Guard-style classifier mock) | **语言:** Python（标准库，工具架构模拟器和 Llama Guard 风格分类器模拟）
**Prerequisites:** Phase 18 · 12-15 (jailbreaks and IPI) | **前置知识:** Phase 18 · 12-15 (越狱和 IPI)
**Time:** ~75 minutes | **时间:** ~75 分钟

>  **【前置】**Je vous invite à maîtriser la phase 18·12-15 (Veterfäng+IPI)
>  **【类比】**红队工具 = "AI 安全的透测试套件"――Llama Guard(Meta) = 输入输出分类器(14 危险类别, similaire à la phase 15·18);Garak(NVIDIA) = 漏洞扫描器(静态+动态+自适应探针,覆盖幻觉/数据泄漏/越狱);PyRIT(Microsoft) = 多轮深度攻击编排(Crescendo/TAP/自定义链)。三件套是研究(12-15)和部署(17+) entre les interfaces ingénières

## Objectifs d'apprentissage

- Décrire la position de Llama Guard 3/4 dans la pile de sécurité: classifiant d'entrée, de sortie ou les deux.

> 描述 Llama Guard 3/4 在安全技术中的位置:输入分类器、输出分类器或两者兼有──

- Nombre des 14 catégories de risques MLCommons et indiquez une catégorie non évidente (abus par interprète de code).

> 列出 14  MLCommons 危险类别,并说明一个不明显的类别 ({{common_code_explanator_code_explanator_code_explanator_code_explanator_code_code_explanator_code_code_explanator_code_code_explanator_code_code_explanator_code_code_code_code_code_explanator_code_code_code_code_code_code_explanator_code_code_code_code_code_code_code_code_code_code_code_code_code_code_code_code_code_code_code_code_code_code_code_code_code_code_code_code_code_code_code_code_code_code_code_code_code_code_code_code_code_code_code_code_code_code_code_code_code_code_code_code_code_code_code_code_code_code_code_code_code_code_code_code_code_code_code_code_code_code_code_code_code_code_code_code_code_code_code_code_code_code_code_code_code_code_code_code_code_code_code_code_code_code_code_code_code___________________________________________________________________________________________________________________________________________________________________________________________________________

- Décrivez l'architecture de la sonde de Garak: sondes, détecteurs, harnais.

> 描述 Garak's探针架构:探针、检测器、线束──

- Décrivez la structure de la campagne multi-tours du PyRIT et comment il se compose avec les sondes Garak.

> Décrire la structure des activités en plusieurs cycles du PyRIT et comment elles sont associées à Garak 探针组合──

## Le problème .

Les leçons 12-15 présentent la surface d'attaque. Les déploiements de production nécessitent une évaluation répétée et évolutive. Trois outils dominent 2026: Llama Guard (le classifiateur de défense), Garak (le scanner), PyRIT (l'orchestrateur de campagne). Chacun cible une couche différente du cycle de vie de l'équipe rouge.

> Les leçons 12-15  ont montré les attaques. La production de déploiements nécessite une évaluation récurrente.

## Le concept.

> **【中文解读】**Llama Guard 3 est Llama-3.1-8B 模型微调到 MLCommons AILuminate 14 类别的输入/输出分类,支持 8种语言。Llama Guard 3-1B-INT4 est la taille de la CPU 约30 tokens/s)。Llama Guard 4(4月2025年) est le 12B 原生多模态分类器, de Llama 4 Scout 剪枝, remplaçant les précédents 8B 文本和 11B 视觉分类器。

### Garde des Llama (Meta)

Llama Guard 3 est un modèle Llama-3.1-8B ajusté pour la classification des entrées et sorties sur les catégories MLCommons AILuminate 14:
- Délits violents, crimes non violents, liés au sexe, CSAM, diffamation
- Conseils spécialisés, vie privée, IP, armes indiscriminées, haine
- Suicide/automutilation, contenu sexuel, élections, abus d'interprète de code

> Llama Guard 3 est un modèle de Llama-3.1-8B, destiné aux MLCommons AILuminate 14 个类别进行输入/输出分类微调――支持 8种语言――

Il prend en charge 8 langues. Utilisation: place avant le LLM (modération d'entrée), après le LLM (modération de sortie), ou les deux. Les deux utilisations génèrent des distributions de formation différentes.

> Utilisation: mettre LLM 之前(输入审核) 之后(输出审核) 或两者兼有──Llama Guard 3 作为单一模型处理两者──

Llama Guard 3-1B-INT4 (arXiv:2411.17713, 440 Mo, ~ 30 jetons / s sur le processeur mobile) est la variante de bord quantifiée.

> Llama Guard 3-1B-INT4 est une plateforme de traitement de la CPU mobile de 440 Mo environ 30 jetons/s.

Llama Guard 4 (avril 2025) est un 12B, natif multimodal, taillé à partir de Llama 4 Scout. Il remplace les prédécesseurs de texte 8B et de vision 11B par un classifiateur qui ingère du texte + des images.

> Llama Guard 4 (Llama Guard 4 (Llama Guard 4)) est un classifiant de type 12B, qui a remplacé les précédents 8B et 11B.

> **【拓展：Garak 架构 → 探针/检测器/线束】**La structure de Garak est en trois niveaux: sonde 幻觉、数据泄露、提示注入、毒性、越狱的攻击生成器,分为静态(固定提示)、动态(生成提示)、自适应(响应目标输出); testeur针对预期失败模式评分输出;线束管理探针-检测器对,运行活动,生成报告――基于层评分(TBSA)

### Garak (NVIDIA)

Scanner de vulnérabilité open source.
- **Probes.**Générateurs d'attaque pour les hallucinations, fuites de données, injection rapide, toxicité, jailbreak. statiques (invitations fixes), dynamiques (invitations générées), adaptifs (répondait à la sortie cible).
- **Detectors.**Résultats par rapport aux modes de défaillance attendus  Toxiques, fuites, jailbroken.
- **Harnesses.**Gérer les paires de sondes détecteurs, exécuter des campagnes, générer des rapports.

> 开源漏洞扫描机.架构:探针. ️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️

TrustyAI intègre Garak avec les boucliers Llama-Stack (classificateur d'entrée Prompt-Guard-86M, classificateur de sortie Llama-Guard-3-8B) pour l'évaluation de la cible protégée de bout en bout.

> TrustyAI va intégrer les boucliers Garak et Llama Stack pour évaluer le niveau de la série.

### Le projet de loi

Python Toolkit pour l'identification des risques. Campaignes multi-tournées de l'équipe rouge.
- **Converters.**Transformer une requête de semence  paraphrase, coder, traduire, jouer de rôle.
- **Orchestrators.**Exécuter la campagne: Crescendo (escalade), TAP (branchage), RedTeaming (cycle personnalisé).
- **Scoring.**L'examen de la loi en tant que juge ou le classement en tant que juge.

> PyRIT est un outil Python 风险识别工具包──多轮红队活动──核心组件:转换器:转换种子提示) 编排器:运行活动:评分:LLM:

PyRIT est le cousin le plus lourd de Garak. Garak exploite des milliers de sondes à tour unique; PyRIT exploite des campagnes à tour multiple profondes conçues pour briser des modes de défaillance spécifiques.

> PyRIT est un programme de poids de Garak. Garak exploite des milliers de spots à tour unique.

### La pile

Mettez la garde de llama des deux côtés du modèle. Exécutez Garak tous les soirs pour la régression. Exécutez PyRIT pour les campagnes de pré-édition. C'est la configuration par défaut de 2026 pour la plupart des déploiements de production.

> Le modèle est placé sur les deux côtés de la Garde des Llama. Chaque soir, le Garak retourne à la recherche.

> **【中文解读】**评估陷:评判身份 Tous les trois outils peuvent être utilisés pour évaluer le MLL 评判,评判校准驱动报告 ASR(Lesson 12), il faut spécifier le jugement;探针过时Garak 探针随着模型修复和老化,自适应探针(PAIR 式)比静态探针老化慢;Llama Guard 在良性内容上的误报率早期版本过标记政治和LGBTQ+内容,v3/v4 校准有改善但未部署校准;;

### Les pièges d'évaluation

- **Judge identity.**Les trois outils peuvent utiliser un juge LLM; les disques de calibration du juge ont rapporté des ASR (leçon 12).
- **Probe staleness.**Les sondes Garak vieillissent à mesure que les modèles sont collés contre elles.
- **Llama Guard FPR on benign content.**Les premières versions de la Garde Llama ont sur-classifié le contenu politique et LGBTQ +; les calibrations de la Garde Llama 3/4 sont améliorées mais pas calibrées par déploiement.

### Là où cela s'inscrit dans la phase 18

Les leçons 12-15 sont les familles d'attaques. La leçon 16 est l'outillage de production. La leçon 17 (WMDP) est l'évaluation de la capacité à double usage. La leçon 18 est les cadres de sécurité frontaliers qui enveloppent ces outils dans une structure politique.

> Les leçons 12-15 sont des attaques familiales. La leçon 16 est des outils de production. La leçon 17 est une évaluation des capacités à double usage. La leçon 18 est de mettre ces outils en place dans le cadre de sécurité de la première ligne de la structure politique.

> **【拓展：PyRIT → 多轮深度利用】**PyRIT (Microsoft) est un système de gestion de poids de Garak. Garak exploite des milliers de pousses à tour unique, PyRIT exploite des activités à grande profondeur de plusieurs cycles de défaites spécifiques. Son cœur est la chaîne de transformateurs.

## Utilisez-le.
```figure
al-guard-stack
```

## Utilisez-le

`code/main.py`Il construit un classifiateur de type jouet Llama Guard (mot clé + fonctionnalités sémantiques sur 14 catégories), un harnais Garak jouet (boucle de détecteur de sonde) et une chaîne de convertisseur multi-tours de type PyRIT.

> `code/main.py`Construit un jouet Llama Guard 风格分类器、 jouet Garak 线束和 PyRIT 风格多轮转换链── vous pouvez utiliser trois outils et observer différentes caractéristiques de couverture──

## Envoyez-le en ligne .

Cette leçon produit `outputs/skill-red-team-stack.md`- En raison de la description du déploiement, il indique quels sont les trois outils appropriés, quels sont les outils à configurer et quelle cadence de régression à exécuter.

> 本课产 出 `outputs/skill-red-team-stack.md` Définir la description, nommer les trois outils qui sont adaptés, chaque disposition quoi, et quel est le rythme de retour.

## Les exercices

1. On court .`code/main.py`Comparer le taux de détection du classifiateur de type Llama-Guard sur les attaques à tour unique et à tour multiple.

2. Implémenter une nouvelle sonde Garak: une demande nuisible codée en base 64. Mesurer sa détection par le classifiateur de style Llama-Guard.

3. Étendre la chaîne de convertisseurs de style PyRIT avec un convertisseur "traducer en français, puis paraphraser".

4. Lisez la liste des catégories de danger de Llama Guard 3. Identifiez deux catégories où les données de formation produiraient réellement des taux de faux positifs élevés sur le contenu légitime des développeurs.

5. Comparer les principes de conception de Garak et PyRIT.

## Les termes clés

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| Llama Guard | "the classifier" | Fine-tuned Llama-3.1-8B/4-12B safety classifier with 14 hazard categories |
| Garak | "the scanner" | NVIDIA open-source vulnerability scanner; probes, detectors, harnesses |
| PyRIT | "the campaign tool" | Microsoft multi-turn red-team orchestrator; converters, orchestrators, scoring |
| Prompt-Guard | "the small classifier" | Meta's 86M prompt-injection classifier, paired with Llama Guard |
| TBSA | "tier-based scoring" | Garak's tier-based pass/fail replacing binary outcomes |
| Converter chain | "paraphrase + encode + ..." | PyRIT composition primitive for building multi-step attacks |
| MLCommons hazard categories | "the 14 taxonomies" | Industry-standard taxonomy Llama Guard targets |

## Encore une lecture

- [Meta — Llama Guard 3 (in Llama 3 Herd paper, arXiv:2407.21783)](https://arxiv.org/abs/2407.21783) le classifiant 8B
- [Meta — Llama Guard 3-1B-INT4 (arXiv:2411.17713)](https://arxiv.org/abs/2411.17713) classifiateur mobile quantifié
- [NVIDIA Garak — GitHub](https://github.com/NVIDIA/garak) le référentiel et la documentation du scanner
- [Microsoft PyRIT — GitHub](https://github.com/Azure/PyRIT) le kit d'outils de campagne
