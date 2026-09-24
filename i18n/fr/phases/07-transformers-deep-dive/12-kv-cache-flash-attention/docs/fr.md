# KV cache, attention flash et optimisation de l'inférence

> L'entraînement est parallèle et lié à FLOP. L'inférence est sérielle et liée à la mémoire.

> **【中文解读】**KV Cache 缓存已计算的关键/值 避免重复计算,是LLM 推理加速的核心──Flash Attention 优化显存访问模式,减少显存使用──

**Type:** Hands-on | **类型:** 动手
**Language:**Je suis un Python .**语言:**Python
**Prerequisites:** Phase 7 · 02 (Self-Attention), Phase 7 · 05 (Full Transformer), Phase 7 · 07 (GPT) | **前置知识:** Phase 7 · 02 (Self-Attention), Phase 7 · 05 (Full Transformer), Phase 7 · 07 (GPT)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Le problème , l' introduction du problème

Un décodeur autorégressif naïf le fait .`O(N²)`travail à générer `N`Les jetons: à chaque étape, il recompte l'attention sur le préfixe complet. Pour une réponse à jetons 4K qui est 16M opérations d'attention, la plupart d'entre eux redondants. Chaque état caché d'un jeton préfixe est déterministe une fois calculé  vous avez seulement besoin d'exécuter la requête du nouveau jeton contre les clés cachées et les valeurs de tout avant.

> Un générateur de code simple.`N`个 token 需要 `O(N²)`Pour la réponse au jeton 4K, c'est une opération de 16M de temps de attention, la plupart d'entre elles étant redondantes.

En plus de cela, l'attention elle-même déplace beaucoup de données. L'attention standard matérialise une matrice de score N×N, une sortie de softmax N×d, une sortie finale N×d  trop de lecture et d'écriture à HBM. Pour N≥2K, l'attention devient liée à la mémoire avant de devenir liée à FLOP.

> En outre, l'attention elle-même doit déplacer une grande quantité de données. L'attention standard génère N×N de la matrice de fractionnement, N×d de la douceur max 输出, N×d de la sortie finale, lorsque le nombre de fois de lecture de HBM est trop élevé.

Deux optimisations, toutes deux de Dao et coll., ont poussé l'inférence de frontière de "lente" à "rapide":

> Les deux améliorations (tuto proviennent de Dao et d'autres) vont être de "l'avant-garde" à "l'avant-garde":

1. **KV cache.**Enregistrer les vecteurs K et V de chaque jeton préfixe.`O(N²)`à `O(N)`par étape de génération.
   Le mot grec traduit par " le mot grec "**KV 缓存。**存储每前代币的K 和 V 向量──每新代币的注意是对缓存键的一个查询──推理从每步`O(N²)`降低到 `O(N)`Il y a une autre.
2. **Flash Attention.**Le calcul de l'attention est calculé de telle sorte que la matrice N×N complète ne touche jamais le HBM. Tout le softmax + matmul se produit dans le SRAM. 24× accélération de l'horloge murale sur A100; 510× sur H100 avec FP8.
   Le mot grec traduit par " le mot grec "**Flash Attention。**Pour calculer l'attention par bloc, faire de la N×N 矩阵 parfaite ne jamais écrire dans HBM。 tous les softmax + 矩阵乘法都在SRAM完成。A100 上 2-4 倍加速;H100 上 FP8 可达 5-10 倍。

D'ici 2026, les deux sont universels. Chaque pile d'inférence de production (vLLM, TensorRT-LLM, SGLang, llama.cpp) les assume.

> D'ici 2026, les deux sont déjà largement utilisés. Chaque modèle de production est censé utiliser Flash Attention.

> **【中文解读】**推理优化两大核心技术:KV Cache 存储已计算的钥匙/值向量,避免重复计算,将每步推理从O(N^2) 降至O(N);Flash Attention 通过分块计算避免N×N矩阵写入HBM,完成所有计算在SRAM,速度提升2-10倍――

## Le concept de base.

![KV cache growth and Flash Attention tiling](../assets/kv-cache-flash-attn.svg)

### Mathématiques de cache KV

Par couche de décodeur, par jeton, par tête:

> Chaque couche de code, chaque jeton, chaque tête:

```
bytes_per_token_per_layer = 2 * d_head * dtype_size
                          ^
                          K and V
```

Pour un modèle 7B avec 32 couches, 32 têtes, d_tête=128, fp16:

> Pour le modèle 7B: 32 niveaux, 32 têtes, 128 têtes, fp16):

```
per token per layer = 2 * 128 * 2 = 512 bytes
per token (32 layers) = 16 KB
per 32K context = 512 MB
```

> **【拓展：GQA 对 KV 缓存的影响】**GQA(Grouped-Query Attention) réduira le KV de n_heads à n_kv_heads, directement égal proportion réduit KV 缓存。 par exemple 64 查询头 / 8 KV 头配置, réduira le KV 缓存 8 fois── en 128K 上下文中, ce qui signifie qu'il est passé d'environ 4 GB à 0,5 GB de KV 缓存, est une optimisation clé de la logique de la longue sous-titre──

Pour Llama 3 70B (80 couches, d_head=128, GQA avec 8 têtes KV):

> Pour les Llama 3 70B ((80 层、d_head=128、GQA 8 个 KV 头):

```
per token per layer = 2 * 8 * 128 * 2 = 4096 bytes (4 KB)
per 32K context = 10.4 GB
```

Ce 10 Go est la raison pour laquelle Llama 3 70B dans le contexte 128K a besoin de la plupart d'un 40 GB A100 juste pour le cache KV à la taille de lot 1.

> C'est pourquoi le Llama 3 70B en 128K est disponible en KV seulement.

**GQA is the KV-cache win.**MHA avec 64 têtes serait 32 Go. MLA comprimés encore plus.

> **GQA 是 KV 缓存的胜利。**64 têtes de MHA  nécessitent 32 GB.
Tirez les dimensions et regardez le déplacement de la taille du cache. Poussez la longueur de la séquence ou le lot vers le haut et voyez à quelle vitesse il souffle au-delà d'un seul GPU:

```figure
kv-cache-sizer
```

### Attention à la lumière

Attention à la norme:

> 标准注意力:

```
S = Q @ K^T          (HBM read, N×N, HBM write)
P = softmax(S)       (HBM read, HBM write)
O = P @ V            (HBM read, HBM write)
```

Trois voyages aller-retour HBM. Sur H100, la bande passante HBM est de 3 TB/s; SRAM est de 30 TB/s. Chaque voyage HBM est un facteur de ralentissement de 10 par rapport à garder tout sur la puce.

> Trois fois HBM 往返── On H100, HBM 带宽是3 TB/s; SRAM est de 30 TB/s── chaque fois HBM 访问比在片保持所有数据慢10倍──

Attention à la lumière:

```
for each block of Q (tile size ~128 × 128):
    load Q_tile into SRAM
    for each block of K, V:
        load K_tile, V_tile into SRAM
        compute S_tile = Q_tile @ K_tile^T     (SRAM)
        running softmax aggregation             (SRAM)
        accumulate into O_tile                  (SRAM)
    write O_tile to HBM
```

Un HBM par carrelage, une trace de mémoire totale en baisse.`O(N²)`à `O(N)`. Pass arrière recompte certaines valeurs de la passe avant au lieu de les stocker  une autre mémoire gagne.

> Chaque carreaux, une visite de la HBM, une visite de la HBM.`O(N²)`- Je ne sais pas .`O(N)` Contrast-directionnellement, il est possible de recalculer certaines valeurs au lieu de les stocker un autre avantage de l'inventaire

**Numerical trick.**La durée de fonctionnement de la softmax est maintenue `(max, sum)`L'attention flash compute une sortie identique à l'attention standard (modulo fp16 non-associativité).

> **数值技巧。**运行时 softmax 跨天 ?? 维护 `(max, sum)`Pour assurer que la réintégration finale est précise.

> **【中文解读】**Les techniques clés de l'attention flash: calculer l'attention par bloc (tiling), effectuer le softmax et la matrice multiplication dans le SRAM rapide du GPU, éviter d'écrire la matrice moyenne de N×N dans le slowspeed HBM. Les techniques clés de la valeur numérique sont "softmax en fonctionnement" à travers la carreaux 维护 (max, somme) pour, s'assurer que le résultat final est parfaitement conforme aux mathématiques standards de l'attention, pas approximatif.

> **【拓展：vLLM 的 PagedAttention】**PagedAttention(vLLM) organisera KV 缓存 pour un "page" fixe de taille, similaire à l'inventaire de l'exploitation. Ceci élimine le problème des fragments de cache, permettant à plusieurs demandes de partage de GPU 显存.

**Version evolution:**

| Version | Year | Key change | Speedup on reference hardware |
|---------|------|-----------|-------------------------------|
| 版本 | 年份 | 关键变化 | 参考硬件上的加速 |
| Flash 1 | 2022 | Tiled SRAM kernel | 2× on A100 |
| Flash 2 | 2023 | Better parallelism, causal-first ordering | 3× on A100 |
| Flash 3 | 2024 | Hopper asynchrony, FP8 | 1.5–2× on H100 (~740 TFLOPs FP16) |
| Flash 4 | 2026 | Blackwell 5-stage pipeline, software exp2 | Inference-first (forward only initially) |

Flash 4 est seulement avancé au lancement. L'entraînement utilise encore Flash 3.

> Flash 4 发布时仅支持前向传播;; entraînement encore en utilisant Flash 3;; GQA 和变长支持待定(2026年中)。

### Décodage spéculatif  l'autre gain de latence

Le modèle bon marché propose N-tokens. Le modèle grand vérifie tous les N en parallèle. Si la vérification accepte k-tokens, vous avez payé 1 large-model avant pour k générations.

> 廉价模型提出 N 个代币――大模型并行验证所有 N 个――如果验证接受 k 个代币,你用一次大模型前向传播获得 k 个生成――代码和散文的典型 k=3-5――

2026 défauts:
- **EAGLE 2 / Medusa.**Des capteurs de projet intégrés qui partagent les états cachés du vérificateur. 23x accélération sans perte de qualité.
  Le mot grec traduit par " le mot grec "**EAGLE 2 / Medusa。**集成草案头,共享验证器的隐藏状态──2-3 倍加速,无质量损失──
- **Speculative decoding with draft model.**2×4 fois plus rapide sur le matériel de consommation.
  Le mot grec traduit par " le mot grec "**带草案模型的推测解码。**2 à 4 fois plus d'accélération sur les appareils de consommation.
- **Lookahead decoding.**Je ne veux pas de modèle de projet, niche mais gratuite.
  Le mot grec traduit par " le mot grec "**前瞻解码。**Je ne veux pas de projet.

### Partage continu

Inference classique par lots: attendre que la séquence la plus lente se termine, puis commencer un nouveau lot.

> 经典批量推理: attendre la séquence la plus lente pour terminer, puis commencer la nouvelle séquence.

Batchage continu (d'abord expédié en Orca, maintenant en vLLM, TensorRT-LLM, SGLang): échangez de nouvelles demandes dans le lot dès que les anciennes sont terminées.

> 连续批处理(首次在Orca中发布,现在在vLLM、TensorRT-LLM、SGLang 中):

### PagedAttention  KV cache comme mémoire virtuelle

La fonctionnalité principale de vLLM. Le cache KV est alloué en blocs de 16 jetons; une table de page cartographique les positions logiques des blocs physiques. Vous pouvez partager KV sur des échantillons parallèles (recherche de faisceaux, prélèvement parallèle), préfixes de swap chaud pour le caching rapide et la mémoire de défragmentation. Amélioration de débit 4x par rapport à l'allocation contiguë naïve.

> Les caractéristiques de base de vLLM sont: KV 缓存 distribué en 16 blocs de jetons; page table sera la position logique de la carte de la carte de données à partir de blocs physiques.

## Construisez-le et mettez-le en œuvre.
```figure
flash-attention-memory
```

## Faites-le

Regardez !`code/main.py`Nous mettons en œuvre:

> 参见 `code/main.py`❖ Nous réalisons:

1. Une naïve .`O(N²)`décodeur incrémentiel.
   Un simple et simple.`O(N²)`- Je suis en train de faire une petite histoire.
2. Une .`O(N)`Décoder en cache KV.
   Un de ces mots`O(N)`KV 缓存解码器──
3. Une softmax en carreaux qui simule l'algorithme de fonctionnement maximal de Flash Attention.
   Une comparaison avec Flash Attention 运行时最大值的分块软max──

### Étape 1: cache KV

```python
class KVCache:
    def __init__(self, n_layers, n_heads, d_head):
        self.K = [[[] for _ in range(n_heads)] for _ in range(n_layers)]
        self.V = [[[] for _ in range(n_heads)] for _ in range(n_layers)]

    def append(self, layer, head, k, v):
        self.K[layer][head].append(k)
        self.V[layer][head].append(v)

    def read(self, layer, head):
        return self.K[layer][head], self.V[layer][head]
```

Simple: continuez à augmenter les vecteurs K et V par jeton dans les listes de couches et de têtes.

> 简单: continue à ajouter chaque jeton de K、V 向量─ dans la liste de chaque rangement

### Étape 2: softmax en carreaux

```python
def tiled_softmax_dot(q, K, V, tile=4):
    """Flash-attention-style softmax(qK^T)V with running max/sum."""
    m = float("-inf")
    s = 0.0
    out = [0.0] * len(V[0])
    for start in range(0, len(K), tile):
        k_block = K[start:start + tile]
        v_block = V[start:start + tile]
        scores = [sum(qi * ki for qi, ki in zip(q, k)) for k in k_block]
        new_m = max(m, *scores)
        exp_old = math.exp(m - new_m) if m != float("-inf") else 0.0
        exp_new = [math.exp(sc - new_m) for sc in scores]
        s = s * exp_old + sum(exp_new)
        for j in range(len(out)):
            out[j] = out[j] * exp_old + sum(e * v[j] for e, v in zip(exp_new, v_block))
        m = new_m
    return [o / s for o in out]
```

Sortie par bits identiques à `softmax(qK) V`dans un seul coup, mais à tout moment le jeu de travail est un `tile × d_head`Le bloc, pas le plein.`N × d_head`- Je suis désolé .

> Avec une seule fois`softmax(qK) V`Les mêmes sorties, mais à tout moment, les mêmes résultats.`tile × d_head`块, et non complet `N × d_head`Il y a une autre.

### Étape 3: comparer le décoding naïf et le décoding en cache sur la génération de 100 jetons

On compte les opérations d'attention.`O(N²)`- 5050 en caisse:`O(N)`Le code imprime les deux.

> 計算注意力操作次数──朴素:`O(N²)`= 5050──缓存:`O(N)`= 100... et je vais imprimer les deux...

## Utilisez-le avec le cadre de réalisation

```python
# HuggingFace transformers auto-enables KV cache on decoder-only generate().
from transformers import AutoModelForCausalLM
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.2-3B",
    attn_implementation="flash_attention_2",  # use FA3 if Hopper
    torch_dtype="bfloat16",
)
# generate() uses KV cache automatically
```

Production de VLLM:

> VLLM 生产部署:

```bash
pip install vllm
vllm serve meta-llama/Llama-3.1-70B-Instruct \
    --tensor-parallel-size 4 \
    --max-model-len 32768 \
    --enable-prefix-caching \
    --kv-cache-dtype fp8
```

Le préfixe de mise en cache entre les demandes est un gros gain 2026  le même système de mise en cache, quelques exemples de tir ou un document de contexte long réutilise KV entre les appels. Pour les charges de travail d'agent avec des demandes d'outils répétées, la mise en cache de préfixe est habituellement 5x gain de débit.

> Le cache de pré-exemplaires de requêtes est le plus grand gain du même système de pré-exemplaires de 2026 ̇ peu de exemples ou de longue liste de documents en cours de réutilisation entre KV ̇ pour les prélèvements de travail de pré-exemplaires de pré-exemplaires de pré-exemplaires de KV ̇, le cache de pré-exemplaires de pré-exemplaires de 2026 entraîne généralement une augmentation de 5 fois de la capacité de débit ̇

## Envoyez-le . Produit .

Regardez !`outputs/skill-inference-optimizer.md`. La compétence choisit la mise en œuvre de l'attention, la stratégie de cache KV, la quantification et le décoding spéculatif pour un nouveau déploiement d'inférence.

> 参见 `outputs/skill-inference-optimizer.md` Cette compétence est mise en œuvre par le nouveau ministère de la Sélection de l'attention à la réalisation de la stratégie de mise en cache de la CV, de la quantification et de la détection des programmes de détection de données.

## Les exercices

1. **Easy.**On court .`code/main.py`- Confirmer que les décodeurs naïfs et cachés produisent la même sortie; noter la différence de calcul optique.
   Le mot " l' économie " est traduit par " l' économie ".`code/main.py` Confirmer que les codes simples et de cache produisent la même sortie;
2. **Medium.**Implémentation de la mise en cache de préfixe: compte tenu d'un prompt P et de plusieurs compléments, exécutez un passage avant sur P pour remplir le cache KV, puis branchez par complément. Mesurer la vitesse par rapport au re-encodage P pour chacun.
   Pour réaliser le pré缓存: donner une indication P 和多个补充, pour P 运行一次前向传播填充 KV 缓存, puis chaque补充分支──测量与每次重编码 P 相比的速度提升──
3. **Hard.**Mise en œuvre d'un jouet PagedAttention: KV cache dans des blocs fixes de 16 jetons avec une liste libre. Une fois une séquence terminée, retournez ses blocs à la piscine. Simuler 1000 chats terminés avec des longueurs variables. Comparer la fragmentation de mémoire par rapport à l'allocation contiguë.
   L'équipe de gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion de la gestion

## Les termes clés

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| KV cache | "The trick that makes decoding fast" | Stored K and V from every prefix token; new queries attend to them instead of recomputing. |
| KV 缓存 | "让解码变快的技巧" | 存储每个前缀 token 的 K 和 V；新查询对它们做注意力而非重新计算。 |
| HBM | "GPU main memory" | High Bandwidth Memory; 80 GB on H100, 192 GB on B200. ~3 TB/s bandwidth. |
| HBM | "GPU 主内存" | 高带宽内存；H100 上 80 GB，B200 上 192 GB。约 3 TB/s 带宽。 |
| SRAM | "On-chip memory" | Per-SM fast memory, ~256 KB per SM on H100. ~30 TB/s bandwidth. |
| SRAM | "片上内存" | 每 SM 的快速内存，H100 上每 SM 约 256 KB。约 30 TB/s 带宽。 |
| Flash Attention | "Tiled attention kernel" | Computes attention without materializing N×N in HBM. |
| Flash Attention | "分块注意力内核" | 不在 HBM 中生成 N×N 矩阵即完成注意力计算。 |
| Continuous batching | "No-wait batching" | Swap finished sequences out, new ones in, without draining the batch. |
| 连续批处理 | "无等待批处理" | 完成的序列换出，新的换入，无需排空批次。 |
| PagedAttention | "vLLM's headline" | KV cache allocated in fixed blocks with a page table; eliminates fragmentation. |
| PagedAttention | "vLLM 的核心特性" | KV 缓存以固定块分配加页表；消除碎片化。 |
| Prefix caching | "Reuse long prompts" | Cache KV for a shared prefix across requests; major cost cut for agents. |
| 前缀缓存 | "复用长提示" | 跨请求缓存共享前缀的 KV；代理场景大幅降低成本。 |
| Speculative decoding | "Draft + verify" | Cheap draft model proposes tokens; big model verifies k in one pass. |
| 推测解码 | "草案 + 验证" | 廉价草案模型提出 token；大模型一次验证 k 个。 |

## Encore une lecture

- [Dao et al. (2022). FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness](https://arxiv.org/abs/2205.14135)- Flash 1
  Le mot "Flash Attention" est traduit par "Flash Attention".
- [Dao (2023). FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning](https://arxiv.org/abs/2307.08691)- Flash 2.
  Le mot "Flash Attention 2" est traduit par "Flash Attention".
- [Shah et al. (2024). FlashAttention-3: Fast and Accurate Attention with Asynchrony and Low-precision](https://arxiv.org/abs/2407.08608)- Flash 3.
  Le mot "Flash Attention" est traduit par "Flash Attention".
- [FlashAttention-4 release notes (Dao-AILab, 2026)](https://github.com/Dao-AILab/flash-attention) Le pipeline de 5 étapes Blackwell et le truc logiciel-exp2; lisez le repo README pour les avertissements de lancement à l'avant-garde mentionnés dans cette leçon.
  Le projet de loi de la Commission européenne sur les droits de l'homme (CEP) est en cours de mise en œuvre.
- [Kwon et al. (2023). Efficient Memory Management for Large Language Model Serving with PagedAttention](https://arxiv.org/abs/2309.06180) papier VLLM.
  Le texte de l'article est écrit en français.
- [Leviathan et al. (2023). Fast Inference from Transformers via Speculative Decoding](https://arxiv.org/abs/2211.17192) Décodage des spécifications.
  Le thème de la rédaction de la Bible est:
- [Li et al. (2024). EAGLE: Speculative Sampling Requires Rethinking Feature Uncertainty](https://arxiv.org/abs/2401.15077) Le document EAGLE-1/2 pour l'approche intégrée de projet que cite la leçon.
  Le texte de l'article est le texte de la première partie de la série.
- [Cai et al. (2024). Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads](https://arxiv.org/abs/2401.10774) l'approche Medusa référencée aux côtés de l'Eagle.
  Le thème de la méduse est "Médusa" (Médusa), "Médusa" (Médusa), "Médusa" (Médusa), "Médusa"), "Médusa" (Médusa), "Médusa", "Médusa" (Médusa), "Médusa" (Médusa), "Médusa" (Médusa), "Médusa" (Médusa), "Médusa" (Médusa), "Médusa" (Médusa), "Médusa" (Médusa), "Médusa" (Médusa), "Médusa) " (Médusa) " (Médusa) " (Médusa) " (Médusa) " (Médusa) " (Médusa) " (Médusa) " (Médusa) " (Médusa) " (Médusa) " (Médusa) " (Médusa) " (Médusa) " (Médusa) " (Médusa) " (Médusa) " (Médusa) " (Médusa) " (Médusa) " (Médusa) " (en)
- [vLLM docs — PagedAttention](https://docs.vllm.ai/en/latest/design/kernel/paged_attention.html) la plongée canonique profonde sur le bloc de 16 jetons et la conception de table de page.
  Le code de la page est le code de la page.
