# L' art et la visualisation de la prison

> Jiang, Xu, Niu, Xiang, Ramasubramanian, Li, Poovendran, "ArtPrompt: Attaques de jailbreak basées sur l'art ASCII contre les LLM alignées" (ACL 2024, arXiv:2402.11753). Masquer les jetons pertinents pour la sécurité dans une demande nuisible, les remplacer par des rendus ASCII-art des mêmes lettres, et envoyer l'invitation masquée. GPT-3.5, GPT-4, Gémeaux, Claude, Llama-2 ne parviennent pas à reconnaître les jetons ASCII-art. L'attaque contourne les PPL (filtres de perplexité), les défenses paraphrasiques et la rétokénisation. Related: le ViTC benchmark mesure la reconnaissance des requêtes visuelles non sémantiques; StructuralSleight généralise aux structures non communes codées par texte (arbres, graphiques, JSON nichés) comme une famille d'attaques de codage.

> **【中文解读】**Le présenté est basé sur l'article suivant: "Le projet de loi sur la sécurité des systèmes de contrôle de la sécurité des systèmes de contrôle de sécurité des systèmes de contrôle de sécurité des systèmes de contrôle de sécurité des systèmes de contrôle de sécurité des systèmes de contrôle de sécurité des systèmes de contrôle de sécurité des systèmes de contrôle de sécurité des systèmes de contrôle de sécurité des systèmes de contrôle de sécurité des systèmes de contrôle de sécurité des systèmes de contrôle de sécurité des systèmes de contrôle de sécurité des systèmes de contrôle de sécurité des systèmes de contrôle de sécurité des systèmes de contrôle de sécurité des systèmes de contrôle de sécurité des systèmes de sécurité des systèmes de contrôle de sécurité des systèmes de contrôle de sécurité des systèmes de sécurité des systèmes de contrôle de sécurité des systèmes de sécurité des systèmes de contrôle de sécurité des systèmes de sécurité des systèmes de contrôle de sécurité des systèmes de contrôle de sécurité des systèmes de sécurité des systèmes de contrôle de sécurité des systèmes de sécurité des systèmes de contrôle de sécurité des systèmes de sécurité des systèmes de sécurité des systèmes de contrôle de sécurité des systèmes de sécurité des systèmes de sécurité des systèmes de sécurité des systèmes de sécurité des systèmes de surveillance des systèmes de sécurité des systèmes de sécurité des systèmes de sécurité de sécurité des systèmes de sécurité de sécurité des systèmes de sécurité de sécurité de sécurité des systèmes de sécurité de sécurité de sécurité des systèmes de sécurité de sécurité de sécurité de sécurité de sécurité des systèmes de sécurité de sécurité de sécurité de sécurité de sécurité de sécurité des systèmes de sécurité de sécurité de sécurité de sécurité de sécurité de sécurité de sécurité de sécurité de sécurité des systèmes de sécurité de sécurité de sécurité de sécurité de sécurité de sécurité de sécurité de sécurité de sécurité de sécurité de sécurité de sécurité des systèmes de sécurité de sécurité de sécurité de sécurité de sécurité de sécurité de sécurité à la sécurité à la sécurité des systèmes de sécurité de sécurité à la sécurité des systèmes de sécurité à la sécurité des systèmes de sécurité à la sécurité des systèmes de sécurité à la sécurité à la sécurité des systèmes de sécurité à la sécurité des systèmes de sécurité à la sécurité à la sécurité des systèmes de sécurité à sécurité à sécurité des systèmes de sécurité à sécurité à sécurité des systèmes de sécurité à sécurité à sécurité à sécurité à sécurité à sécurité des systèmes de sécurité à sécurité à sécurité à sécurité à sécurité à sécurité à sécurité à sécurité à sécurité à sécurité des systèmes de sécurité à sécurité à sécurité à sécurité à sécurité à sécurité à sécurité à sécurité à sécurité à sécurité à sécurité à sécurité à sécurité à sécurité à sécurité à sécurité à sécurité à sécurité à sécurité à sécurité à sécurité à sécurité à sécurité à

> **【拓展：ArtPrompt → 编码攻击家族】**标准防御 (困惑度过、释义、重新分词) est totalement échoué dans ArtPrompt, car la sécurité de l'appareil est en train de fonctionner à un niveau de commandes/signification, tandis que ArtPrompt est en train de fonctionner à un niveau de reconnaissance visuelle.

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, ArtPrompt token-masking harness) | **语言:** Python（标准库，ArtPrompt token 掩码框架）
**Prerequisites:** Phase 18 · 12 (PAIR), Phase 18 · 13 (MSJ) | **前置知识:** Phase 18 · 12 (PAIR), Phase 18 · 13 (MSJ)
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**Pour les autres, il est nécessaire de se préparer à la mise en œuvre de la méthode de rédaction de l'article.
>  **【类比】**ASCII 越狱 = "隐形墨水"。安全过器看无害的标点网格,模型视觉理解为一个词。ArtPrompt ACL 2024:GPT-4/Gemini/Claude/Llama-2 全失败,>75% 攻击成功率──绕过PPL 过、改写、重代币 化防御──结构性变种(StructuralSleight) étendu à树/图/嵌套 JSON所有非语义视觉提示都是攻击面──

## Objectifs d'apprentissage

- Décrivez l'attaque ArtPrompt: étape d'identification par mot, substitution ASCII-art, dernière requête masquée.

> 描述 ArtPrompt 攻击:词识别步骤、ASCII 艺术替换、最终伪装提示──

- Expliquez pourquoi les défenses standard (PPL, Paraphrase, Retokenization) échouent sur ArtPrompt.

> 解释为什么标准防御(困惑度过、释义、重新分词)

- Définir le TIC et décrire ce qu'il mesure.

> définir ViTC并描述其量量内容──

- Décrire StructuralSleight comme une généralisation des structures encodées par texte inhabituelles arbitraires.

> 描述 StructuralSleight 作为对任意罕见文本编码结构的推广──

## Le problème .

Les attaques par paraphrase et jeu de rôle (leçon 12) et par long contexte (leçon 13) fonctionnent sur le modèle au niveau du texte. ArtPrompt fonctionne au niveau de la reconnaissance: le modèle ne paralyse pas le jeton interdit. Il paralyse une image rendue en caractères. Le filtre de sécurité voit une ponctuation inoffensive. Le modèle voit un mot.

> 通过释义和角色扮演(Léction 12) 和长上下文(Léction 13) Les attaques sont effectuées sur un modèle de niveau texte。ArtPrompt dans l'opération de niveau de reconnaissance: le modèle ne résoud pas les commandes interdites, mais les résoud à l'aide d'une image de caractère🏼

## Le concept.

> **【中文解读】**ArtPrompt 两步攻击的细节:第一步给定有害请求,使用LLM 识别安全相关词(如"炸弹"在"如何做炸弹"中);第二步将每个识别的词换成其ASCII 艺术染(7x5或7x7 字符块形成字母形状) ;; le modèle reçoit des signes et des vues de net格, assez puissant pour pouvoir reconnaître des mots; sécurité过器只看到网格;;

### ArtPrompt, deux étapes

Étape 1. Identification des mots. En cas de demande nuisible, l'attaquant utilise un LLM pour identifier les mots pertinents pour la sécurité (par exemple, " bombe " dans " comment faire une bombe "). 

Étape 2. Génération de la mise en évidence masquée. Remplacez chaque mot identifié par son rendu ASCII-art (un bloc de caractères 7x5 ou 7x7 formant la forme de la lettre). Le modèle reçoit une grille de ponctuation et d'espaces que un modèle suffisamment capable peut reconnaître comme le mot; un filtre de sécurité ne voit que la grille.

Résultat: GPT-4, Gémeaux, Claude, Llama-2, GPT-3.5 échouent tous.

> Résultat: GPT-4、Gemini、Claude、Llama-2、GPT-3.5 全部失败── le taux de réussite des attaques sur le groupe de base dépasse 75%──

> **【拓展：防御失败 → 多层安全启示】**困惑度过器失败是因为合法结构化输入也得分高;释义失败是因为释义 LLM 常保留或重建 ASCII 艺术;重新分词失败是因为识别是视觉的而不是令牌级的──安全必须泛化到模型能解析的所有结构化表示

### Pourquoi les défenses standard échouent

- **PPL (perplexity filter).**L'art ASCII a une grande perplexité  mais tout nouveau input le fait aussi.

> **困惑度过滤。**ASCII 艺术有高困惑度但所有新输入也是如此──阻止ArtPrompt的值选择也阻止了合法的结构化输入──

- **Paraphrase.**La paraphrase du prompt détruit l'art ASCII. En pratique, les LLM de paraphrase préservent ou reconstruisent souvent l'art.

> **释义。**释义提示会破坏 ASCII 艺术── en fait, la mise en œuvre de la loi de droit 常常保留或重建艺术──

- **Retokenization.**La division des jetons différemment ne change pas le fait que la vision du modèle reconnaît les formes de lettres.

> **重新分词。**Les différents éléments de la carte de départ ne changent pas le modèle de la vue en reconnaissant la forme des lettres.

Le problème sous-jacent est que les filtres de sécurité sont au niveau des symboles ou de la sémantique; ArtPrompt fonctionne au niveau de la reconnaissance visuelle.

> Le problème fondamental est la sécurité des filtres dans les commandes ou les opérations de niveau de langage; ArtPrompt dans les opérations de niveau de reconnaissance visuelle.

> **【中文解读】**ViTC 基准:ArtPrompt's efficacité et capacité de modèle à lire des textes visuels liés ViTC 准确率越高,ArtPrompt 越有效。这是一个能力-安全权衡:提升模型的多模态理解能力会同时增加编码攻击的脆弱性──视觉 LLM(GPT-5.2, Gemini 3 Pro, Claude Opus 4.5, Grok 4.1) a étendu les attaques face à face  ArtPrompt 式攻击实际图像的 ASCII 艺术更强──

### Indice de référence ViTC

Reconnaissance des instructions visuelles non sémantiques. Mesure la capacité du modèle à lire ASCII-art, wingdings et autres contenus visuels non textes-sémantiques. L'efficacité d'ArtPrompt est corrélée à la précision de ViTC: plus le modèle lit le texte visuel, mieux ArtPrompt travaille dessus.

> La capacité de lecture de l'art et de l'art est une mesure de la qualité de l'art.

### StructuralSleight

Généralise ArtPrompt: Structures encodées par texte (UTES) peu communes. arbres, graphiques, JSON nichés, CSV-in-JSON, blocs de code de style différent. Si une structure est rare dans la formation des données de sécurité mais parseable par le modèle, elle peut cacher du contenu nocif.

> 推广 ArtPrompt: rare textbook codification structure(UTES) ―― tree、图、嵌套 JSON、 JSON CSV、diff 风格代码块── Si une structure est rare mais que le modèle peut être résolu dans les données de sécurité, elle peut cacher du contenu nocif──

L'implication de la défense: la sécurité doit être généralisée sur les représentations structurées que le modèle peut analyser.

> La sécurité doit être généralisée à tous les aspects structurels du modèle.

### Analogue de la modalité d'image

Les LLM visuels (GPT-5.2, Gemini 3 Pro, Claude Opus 4.5, Grok 4.1) étendent la surface d'attaque. Les attaques de style ArtPrompt avec des images réelles sont plus fortes que les analogues ASCII-art car les encoders d'image produisent un signal plus riche.

> Le M.L.L.V. a étendu les attaques. L'utilisation d'images réelles en ArtPrompt est plus forte que l'ASCII, car le codeur d'images génère plus de signaux.

### Là où cela s'inscrit dans la phase 18

Les leçons 12-14 décrivent trois vecteurs d'attaque orthogonales: raffinement itératif (PAIR), longueur de contexte (MSJ) et codage (ArtPrompt/StructuralSleight).

> Les leçons 12-14  décrire trois attaques positives                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                

> **【拓展：视觉 LLM → 攻击面扩展】**视觉 LLM(GPT-5.2, Gemini 3 Pro, Claude Opus 4.5, Grok 4.1) a étendu l'attaque face à face.

## Utilisez-le.
```figure
al-ascii-cloak
```

## Utilisez-le

`code/main.py`Vous pouvez masquer des mots spécifiques dans une requête nuisible avec des glyphes ASCII-art, vérifier que la chaîne masquée passe un filtre de mots clés et (en option) décoder la chaîne masquée en utilisant un simple reconnaisseur.

> `code/main.py`Construire un jouet ArtPrompt。 vous pouvez utiliser ASCII 艺术字形伪装有害查询中的特定词,验证伪装字符串通过关键词过,并(可选地) en utilisant un simple identifiateur解码。

## Envoyez-le en ligne .

Cette leçon produit `outputs/skill-encoding-audit.md`. Compte tenu d'un rapport de défense contre les jailbreak, il énumère les familles d'attaques de codage couvertes (art ASCII, base64, leet-speak, homoglyphe UTF-8, UTES) et la couche de défense qui capture chacune.

> 本课产 出 `outputs/skill-encoding-audit.md` Définir les rapports de défense de la prison, les couvertures de code d'attaque de la famille et de chaque couche de défense de la réponse.

## Les exercices

1. On court .`code/main.py`- Vérifiez que la chaîne masquée passe par un simple filtre de mots clés.

2. Implémenter un deuxième codage: base64 pour le même mot cible. Comparer le taux de contournement du filtre avec ArtPrompt et la difficulté de récupération.

3. Lisez Jiang et coll. 2024 Section 4.3 (résultats de cinq modèles). Proposez une raison pour laquelle la résistance à ArtPrompt de Claude est supérieure à celle de Gémeaux sur le même critère de référence.

4. Conçuez une défense de pré-génération qui détecte les régions en forme d'art ASCII dans le prompt. Mesurez le taux de faux positifs sur le code légitime, les tables et la notation mathématique.

5. StructuralSleight énumère 10 structures de codage.

## Les termes clés

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| ArtPrompt | "the ASCII-art attack" | Two-step jailbreak that masks safety words with ASCII-art renderings |
| Cloaking | "hide the word" | Replace a forbidden token with a visual representation the model reads but the filter does not |
| UTES | "uncommon structure" | Uncommon Text-Encoded Structure — tree, graph, nested JSON, etc. used to smuggle content |
| ViTC | "visual-text capability" | Benchmark for model's ability to read non-semantic visual encoding |
| Perplexity filter | "PPL defense" | Reject prompts with high perplexity; fails because legitimate structured input also scores high |
| Retokenization | "tokenizer shift defense" | Pre-process the prompt with a different tokenizer; fails because recognition is visual |
| Homoglyph | "lookalike characters" | Unicode characters that look identical to Latin letters; bypass substring checks |

## Encore une lecture

- [Jiang et al. — ArtPrompt (ACL 2024, arXiv:2402.11753)](https://arxiv.org/abs/2402.11753) le papier de jailbreak ASCII-art
- [Li et al. — StructuralSleight (arXiv:2406.08754)](https://arxiv.org/abs/2406.08754) Généralisation des UTES
- [Chao et al. — PAIR (Lesson 12, arXiv:2310.08419)](https://arxiv.org/abs/2310.08419) attaque itérative complémentaire
- [Anil et al. — Many-shot Jailbreaking (Lesson 13)](https://www.anthropic.com/research/many-shot-jailbreaking) attaque de longueur complémentaire
