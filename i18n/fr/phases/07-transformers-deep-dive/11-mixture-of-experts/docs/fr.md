# Le modèle d'experts (MoE)

> Un transformateur dense 70B active tous les paramètres pour chaque jeton. Un MoE 671B active seulement 37B par jeton et le bat sur chaque référence.

> **【中文解读】**MoE est seulement activé par des spécialistes du réseau qui traitent chaque jeton, augmentant considérablement le nombre de paramètres sans augmenter la quantité de calcul.

**Type:** Hands-on | **类型:** 动手
**Language:**Je suis un Python .**语言:**Python
**Prerequisites:** Phase 7 · 05 (Full Transformer), Phase 7 · 07 (GPT) | **前置知识:** Phase 7 · 05 (Full Transformer), Phase 7 · 07 (GPT)
**Time:** ~45 minutes | **时间:** ~45 分钟

## Le problème , l' introduction du problème

Les FLOP d'un transformateur dense sont à l'inférence égaux au nombre de paramètres (deux fois pour le passage à l'avant).

> 密 推理时的FLOPs等于其参数(前向传播乘以2);;扩大密模型意味着每个代币都必须支付全部代价;; Dès 2024, le modèle de l'avant-garde a rencontré un calcul: il doit devenir plus intelligent, il doit augmenter en nombre de FLOPs par token;;

Le mélange d'experts rompt ce lien.`E`experts indépendants + un routeur qui choisit `k`Parmi les paramètres de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de la valeur de cette valeur de cette valeur de cette valeur de cette valeur de cette valeur de cette valeur de cette valeur de cette valeur de cette valeur,`E × FFN_size`. Paramètres actifs par jeton = `k × FFN_size`. Configuration typique pour 2026: `E=256`- Je suis là .`k=8`- Balances de stockage avec`E`, calculer des échelles avec `k`- Je suis désolé .

> Le modèle spécialisé mixte a rompu ce lien.`E`个独立专家 + 一个路由器, chaque jeton 选择 `k`个专家──总参数 = `E × FFN_size`◊ Le nombre de paramètres actifs de chaque symbole = `k × FFN_size`❖ Conception typique pour l'année 2026:`E=256`- Je suis là.`k=8`◊ stockage avec`E`扩展,计算随 `k`- Je suis en train de me lancer.

La frontière 2026 est presque entièrement MoE: DeepSeek-V3 (671B total / 37B actif), Mixtral 8×22B, Qwen2.5-MoE, Llama 4, Kimi K2, gpt-oss.

> La première ligne de 2026 est presque entièrement MoE:DeepSeek-V3(671B 总参数 / 37B 活跃) 、Mixtral 8×22B、Qwen2.5-MoE、Llama 4、Kimi K2、gpt-oss──

> **【中文解读】**MoE 打破了"参数 = 计算量"等式──每个FFN 层被替换为E 个独立专家 + 路由器,每个代币只激活 k 个专家──总参数随着E 增长,但每个代币的计算量只随着E 增长──典型配置E=256, k=8,存储随着E 缩缩,计算随着k 缩缩──这是2020年代最重要的扩展思路──

> **【拓展：DeepSeek-V3 的 MoE 创新】**DeepSeek-V3 possède 671B  Paramètres généraux mais chaque jeton n'active que 37B par 256 experts en route + 1 expert en partage pour réaliser. Il introduit également une stratégie d'équilibre de charge sans perte de support, évitant les problèmes de rupture des routes traditionnelles du MoE.

## Le concept de base.

![MoE layer: router selects k of E experts per token](../assets/moe.svg)

### Le swap FFN

Bloc de transformateur dense:

> 密 Les blocs de transformateur:

```
h = x + attn(norm(x))
h = h + FFN(norm(h))
```

Bloc de la moée:

```
h = x + attn(norm(x))
scores = router(norm(h))              # (N_tokens, E)
top_k = argmax_k(scores)              # pick k of E per token
h = h + sum_{e in top_k}(
        gate(scores[e]) * Expert_e(norm(h))
    )
```

Chaque expert est un FFN indépendant (typiquement SwiGLU). le routeur est une seule couche linéaire. chaque jeton choisit son propre`k`les experts et obtient un mélange fermé de leurs résultats.

> Chaque spécialiste est un FFN indépendant (habituellement SwiGLU) ⋅ le routeur est un niveau monothérique ⋅ chaque jeton                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          `k`个专家, obtenir leurs sorties et leur mélange contrôlé.

### Le problème de l'équilibre de la charge

Si le routeur passe 90% des jetons par l'expert 3, les autres experts meurent de faim.

> Si le routeur distribue 90% des jetons aux experts 3, d'autres experts seront " affamés "

1. **Auxiliary load-balancing loss**(Switch Transformer, Mixtral). Ajouter une pénalité proportionnelle à la variance dans l'utilisation des experts. Fonctionne, mais ajoute un hyperparamètre et un deuxième signal de gradient.
   Le mot grec traduit par " le mot grec "**辅助负载均衡损失**(Switch Transformer、Mixtral) ∼ Ajout avec des spécialistes utilisent une différence de proportion de punition── efficace, mais augmenté superparamètres et deuxième degré de signal──
2. **Expert capacity + token dropping**(début de la mise en place).`C × N/E`Les jetons de débordement sautent la couche.
   Le mot grec traduit par " le mot grec "**专家容量 + token 丢弃**(Mécanisme de démarrage) ◊ chaque spécialiste le plus traité `C × N/E`个标志;溢出的标志 跳过这个层――损害质量――
3. **Auxiliary-loss-free balancing**(DeepSeek-V3). Ajouter un biais appris par expert qui change la sélection top-k du routeur.
   Le mot grec traduit par " le mot grec "**辅助损失无关均衡**(DeepSeek-V3)── Ajouter une formation à chaque spécialiste, modifier le choix du routeur, modifier le choix du routeur.

Approche de DeepSeek-V3: après chaque étape de formation, chaque expert vérifie si son utilisation est supérieure ou inférieure à l'objectif.`±γ`. Utilisation de sélection `scores + bias`Les probabilités d' expertise utilisées pour le dépistage sont les premières`scores`Découpe le routage de l'expression.

> Méthode de recherche approfondie-V3: après chaque étape de formation, chaque spécialiste vérifie si son utilisation est plus ou moins élevée que l'objectif.`±γ` choisir usage `scores + bias` Le taux de risque des spécialistes utilisés est inchangé.`scores`将路由与表达解──

### Des experts partagés

DeepSeek-V2/V3 divise également les experts en *shared* et *routed*. Chaque jeton passe par tous les experts partagés. Les experts partagés sont choisis par le biais de top-k. Les experts partagés capturent les connaissances communes; les experts partagés se spécialisent. V3 exécute 1 expert partagé plus le top-8 des 256 partagés.

> DeepSeek-V2/V3 divisera également les spécialistes en deux catégories: * partage* et * parcours*. Chaque jeton est divisé en deux catégories:

### Des experts en grains fins

MoE classique (GShard, Switch): chaque expert est aussi large qu'un FFN complet. `E`est petite (864), `k`est petite (12).

> 经典 MoE(GShard、Switch): chaque spécialiste avec FFN complet`E`较小(8-64),`k`Je suis un peu plus jeune que toi.

MoE moderne à grains fins (DeepSeek-V3, Qwen-MoE): chaque expert est plus étroit (1/8 FFN de taille). `E`est grand (256+), `k`Les paramètres totaux sont les mêmes, mais les combinaisons évoluent beaucoup plus rapidement. `C(256, 8) = 400 trillion`La qualité augmente, la latence reste stable.

> 现代细粒度 MoE(DeepSeek-V3、Qwen-MoE): chaque spécialiste est plus étroit(1/8 FFN`E`较大(256+),`k`Même plus grand (8, +) ⋅ ensemble de composants est le même, mais le groupe de composants augmente plus rapidement.`C(256, 8) = 400 万亿`种可能的"专家"组合──质量提升,延迟不变──

> **【拓展：MoE 的路由崩塌问题】**Le défi central de l'entraînement MoE est le roulement de l'écrasement du routeur. Le routeur peut distribuer la majeure partie des jetons à une minorité d'experts, ce qui entraîne l'absence d'entraînement des autres spécialistes.

### Le profil des coûts

Par jeton, par couche:

> Chaque jeton, chaque couche:

| Config | Active params / token | Total params |
|--------|-----------------------|--------------|
| 配置 | 每个 token 活跃参数 | 总参数量 |
| Mixtral 8×22B | ~39B | 141B |
| Llama 3 70B (dense) | 70B | 70B |
| DeepSeek-V3 | 37B | 671B |
| Kimi K2 (MoE) | ~32B | 1T |

DeepSeek-V3 bat Llama 3 70B (dense) sur presque tous les indicateurs de référence en faisant **fewer active FLOPs per token**Plus de paramètres = plus de connaissances. Plus de FLOPs actifs = plus de calcul par jeton.

> DeepSeek-V3 a battu Llama 3 70B dans presque tous les tests de base, en même temps.**每个 token 的活跃 FLOPs 更少**△Plus de paramètres = 更多知识──更多活跃 FLOPs = Chaque jeton 更多计算──MoE 将两者解──

### Le problème: la mémoire

Tous les experts vivent sur GPU, quel que soit le type de GPU. Un modèle 671B nécessite ~ 1,3 To de VRAM pour les poids fp16.

> Tous les experts, qu'ils soient activés ou non, sont installés sur le GPU. Un modèle 671B nécessite environ 1,3 To de fp16 de puissance de mise à jour.

> **【中文解读】**Le poids central de MoE: avec le calcul du changement de mémoire. Le DeepSeek-V3 atteint des performances de plus de 70B avec un paramètre actif de 37B, mais nécessite 1,3TB de stockage de données.

> **【拓展：细粒度专家 vs 粗粒度专家】**传统 MoE(Switch Transformer) utilise une petite quantité de grands spécialistes(E=8-64)。现代细粒度 MoE(DeepSeek-V3) utilise une grande quantité de petits spécialistes(E=256+), chaque spécialiste ne possède que 1/8 de la FFN 宽度──组合数 C(256,8) 约为40000000000种,远超粗粒度的组合空间──质量提升显著,延迟基本不变──

## Construisez-le et mettez-le en œuvre.
```figure
expert-routing
```

## Faites-le

Regardez !`code/main.py`- une couche compacte de MoE en stdlib pur avec:

> 参见 `code/main.py` Une couche de la mise en œuvre de la norme pure, comprenant:

- `n_experts=8`Des experts en SWIGU (un linéaire par exemplaire)
  Le mot grec traduit par " le mot grec "`n_experts=8`个类 SwiGLU 专家( chaque une ligne de couche, pour démonstration)
- en route de haut-k=2
  Le premier est le premier.
- poids de fermeture normalisé à la hauteur de la douceur maximale
  Le poids du poids est contrôlé
- équilibrage sans perte auxiliaire par biais de biais par expert
  En français, par exemple, le décalage de l'équilibre est un problème de santé.

### Étape 1: le routeur

```python
def route(hidden, W_router, top_k, bias):
    scores = [sum(h * w for h, w in zip(hidden, W_router[e])) for e in range(len(W_router))]
    biased = [s + b for s, b in zip(scores, bias)]
    top_idx = sorted(range(len(biased)), key=lambda i: -biased[i])[:top_k]
    # softmax over ORIGINAL scores of the chosen experts
    chosen = [scores[i] for i in top_idx]
    m = max(chosen)
    exps = [math.exp(c - m) for c in chosen]
    s = sum(exps)
    gates = [e / s for e in exps]
    return top_idx, gates
```

Le biais affecte la sélection, pas le poids de la porte. C'est le truc DeepSeek-V3  bias corrige le déséquilibre de charge sans diriger les prédictions du modèle.

> 偏置影响选择,不影响门控制权重―― voilà la technique de DeepSeek-V3 偏置纠正负载不平衡, mais non pré pré prédiction du modèle―

### Étape 2: exécuter 100 jetons à travers le routeur

Suivre quelle fréquence les experts tirent. Sans le biais, l'utilisation est biaisée.`-γ`pour les experts surutilisés `+γ`Les utilisations sont généralement moins fréquentes (en fonction de la fréquence de l'utilisation), et l'utilisation converge à une distribution uniforme sur quelques itérations.

> Suivez les spécialistes qui ont été activés plusieurs fois. Pas de décalage, le nombre d'utilisations est différent.`-γ`, utilisation insuffisante des spécialistes `+γ`), la consommation est répandue de façon moyenne à plusieurs générations.

### Étape 3: Comparation du nombre de paramètres

Imprimez l'équivalent dense d'une configuration MoE. DeepSeek-V3-forme: 256 routi + 1 partagé, 8 actif, d_model = 7168. Le nombre total de paramètres est impressionnant. Le nombre actif est un septième d'un Llama dense 3 70B.

> 印印 MOE 配置的"密等价"──DeepSeek-V3 形状:256 个路由 + 1 个共享,8 个活跃,d_model=7168──总参数令人惊叹──活跃参数数只有密 Llama 3 70B 的七分之一──

## Utilisez-le avec le cadre de réalisation

Chargement de la face:

> Elle est en train de se faire avaler.

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
model = AutoModelForCausalLM.from_pretrained("mistralai/Mixtral-8x22B-v0.1")
```

2026 production d'inférence: vLLM prend en charge le routage MoE natively. SGLang a le plus rapide parallèle expert-path.

> 2026 年生产推理:vLLM 原生支持 MoE 路由──SGLang 拥有最快的专家并行路径──两者都自动处理顶级选择和专家并行──

**When to pick MoE:**
- Vous voulez une qualité de pointe à un coût inférieur par jeton.
  Vous voulez obtenir une qualité de l'avant-garde ?
- Vous disposez de l'infrastructure VRAM / expert parallèle.
  Vous avez suffisamment de ressources / spécialistes et infrastructures.
- Votre charge de travail est lourde en tokens (chat, code) et non lourde en contexte (longs documents).
  Le travail que vous faites est un symbole de type 密集型(聊天、代码) plutôt que de type 密集型 (长文档)

**When NOT to pick MoE:**
- Déploiement de bord  vous payez le stockage complet pour tout FLOP actif.
  Le gouvernement a décidé de mettre fin à la crise de l'Afrique du Sud.
- L'expertise en routage  pour un utilisateur unique critique de la latence ajoute des frais généraux.
  Le service de l'utilisateur unique est un service spécialisé dans la vente de services.
- Les modèles de petite taille (<7B)  L'avantage de qualité du MoE ne se dégage qu'au-dessus d'un seuil de calcul (~6B paramètres actifs).
  Le nombre de modèles de MoE est de 6B (environ 6B) et il n'existe que 6B.

## Envoyez-le . Produit .

Regardez !`outputs/skill-moe-configurator.md`. La compétence choisit E, k et la mise en page partagée par des experts pour un nouveau budget de paramètre du MoE, des jetons de formation et des objectifs de déploiement.

> 参见 `outputs/skill-moe-configurator.md` Cette compétence ∞ en fonction du budget paramétrique ∞ en train de travailler ∞ en fonction des objectifs de déploiement, ∞ en vue de la nouvelle MoE ∞ en sélectionnant E、k 和 en partage des spécialités ∞

## Les exercices

1. **Easy.**On court .`code/main.py`Regardez comment la mise à jour de biais sans perte auxiliaire équivaut à l'utilisation des experts sur 50 itérations.
   Le mot " l' économie " est traduit par " l' économie ".`code/main.py`◊ Observer l'utilisation de l'équilibre entre les 50 générations
2. **Medium.**Remplacez le routeur apprenant par un routeur basé sur le hachage (déterministique, pas d'apprentissage). Comparer la qualité et l'équilibre. Pourquoi le routeur apprenant est-il meilleur?
   Le modèle de formation est un modèle de formation de formation de formation de formation.
3. **Hard.**Implémenter le "routage parallèle de déploiement" (truc DeepSeek-V3.2): enregistrer ce que les experts tirent lors de l'inférence, forcer le même routage lors du calcul des gradients. Mesurer l'effet sur une configuration de politique de jeu-gradient.
   Le système de calcul de la taille de l'instrument est basé sur la méthode de calcul de la taille de l'instrument.

## Les termes clés

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Expert | "One FFN among many" | An independent feed-forward network; parameters dedicated to a sparse slice of the FFN computation. |
| 专家 | "众多 FFN 之一" | 独立的前馈网络；专用于 FFN 计算的稀疏切片的参数。 |
| Router | "The gate" | A tiny linear layer that scores each token against each expert; top-k selection. |
| 路由器 | "门控" | 一个小线性层，对每个 token 与每个专家打分；top-k 选择。 |
| Top-k routing | "k active experts per token" | Each token's FFN computation goes through exactly k experts, weighted by gate. |
| Top-k 路由 | "每个 token 激活 k 个专家" | 每个 token 的 FFN 计算经过恰好 k 个专家，按门控加权。 |
| Auxiliary loss | "Load-balance penalty" | Extra loss term that penalizes skewed expert usage. |
| 辅助损失 | "负载均衡惩罚" | 惩罚专家使用不均衡的额外损失项。 |
| Auxiliary-loss-free | "DeepSeek-V3's trick" | Balance via per-expert bias on the router's selection only; no extra gradient. |
| 辅助损失无关 | "DeepSeek-V3 的技巧" | 仅通过路由器选择上的逐专家偏置实现均衡；无额外梯度。 |
| Shared expert | "Always on" | Extra expert through which every token passes; captures common knowledge. |
| 共享专家 | "始终开启" | 每个 token 都通过的额外专家；捕获通用知识。 |
| Expert parallelism | "Shard by expert" | Distribute different experts to different GPUs; route tokens across the network. |
| 专家并行 | "按专家分片" | 将不同专家分配到不同 GPU；通过网络路由 token。 |
| Sparsity | "Active params < total params" | The ratio `k × expert_size / (E × expert_size)`; 37/671 ≈ 5.5% for DeepSeek-V3. |
| 稀疏性 | "活跃参数 < 总参数" | 比率 `k × expert_size / (E × expert_size)`；DeepSeek-V3 为 37/671 ≈ 5.5%。 |

## Encore une lecture

- [Shazeer et al. (2017). Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer](https://arxiv.org/abs/1701.06538)- L'idée.
  Le premier article de MoE
- [Fedus, Zoph, Shazeer (2022). Switch Transformer: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity](https://arxiv.org/abs/2101.03961)- Le Switch, le MoE classique.
  Le changement de mode est un changement de mode.
- [Jiang et al. (2024). Mixtral of Experts](https://arxiv.org/abs/2401.04088) Mixtral 8×7B.
  Le mélange 8×7B
- [DeepSeek-AI (2024). DeepSeek-V3 Technical Report](https://arxiv.org/abs/2412.19437) MLA + MoE sans perte auxiliaire + MTP.
  Le rapport technique, MLA + 辅助损失无关 MoE + MTP──
- [Wang et al. (2024). Auxiliary-Loss-Free Load Balancing Strategy for Mixture-of-Experts](https://arxiv.org/abs/2408.15664) le papier d'équilibrage basé sur les biais.
  Traduction anglaise: Équilibre stratégique de la mise en place
- [Dai et al. (2024). DeepSeekMoE: Towards Ultimate Expert Specialization in Mixture-of-Experts Language Models](https://arxiv.org/abs/2401.06066) le spécialiste de la division de l'utilisation du routeur de cette leçon.
  Le thème de la recherche est "Professionnellement".
- [Kim et al. (2022). DeepSpeed-MoE: Advancing Mixture-of-Experts Inference and Training](https://arxiv.org/abs/2201.05596) document d'expert commun original.
  Le thème de la rédaction de l'article est "Préparation de l'équipe de rédaction de l'article".
