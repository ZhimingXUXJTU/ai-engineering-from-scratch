# Traduction automatique

> La traduction est la tâche qui a payé la recherche en PNL pendant trente ans et continue de payer maintenant.
> La traduction est une tâche qui a duré trois décennies et qui continue à être réalisée.

> **【中文解读】**De la statistique à la machine à écrire.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 10 (Attention Mechanism), Phase 5 · 04 (GloVe, FastText, Subword) | **前置知识:** Phase 5 · 10 (Attention Mechanism), Phase 5 · 04 (GloVe, FastText, Subword)
**Time:** ~75 minutes | **时间:** ~75 minutes


## Le problème , l' introduction du problème

Un modèle lit une phrase dans une langue et produit une phrase dans une autre. La longueur varie. L'ordre des mots varie. Certains mots source cartographient plusieurs mots cibles et vice versa. Les idiomes refusent de cartographier un à un. "Je te manque" en français est "tu me manques"  littéralement "je te manque". Aucun alignement au niveau des mots ne survit à cela.
> 模型读取一语言的句子并产生另一语言的句子──长度不同──词序不同──一些源词映射到多个目标词,反之亦然──习语拒绝对一映射──"Je te manque" est un mot français qui signifie "tu me manques"  字面意思是"tu me manque"──没有词级对齐能经受住这个──

> **【中文解读】**La question posée dans ce chapitre est la suivante: comment comprendre et appliquer correctement cette technique dans la conception pratique. Comprendre le contexte de la question aide à saisir les principaux facteurs de décision concernant le type de technologie. Dans les systèmes d'IA réels, le type de technique erroné coûte souvent plus cher que le coût de la mise en œuvre de détails.


La traduction automatique est la tâche qui a forcé la PNL à inventer des décodeurs, des attention, des transformateurs et finalement l'ensemble du paradigme de la LLM. Chaque pas en avant est arrivé parce que la qualité de la traduction était mesurable et que l'écart entre humain et machine était têtu.
> La traduction automatique est l'impulsion de la PNL à inventer un codeur-décodeur, un attentionne, un transformateur et finalement l'ensemble du modèle de la LM. Chaque étape est réalisée à cause de la qualité de la traduction mesurable et de la différence entre l'homme et la machine.

Cette leçon passe à côté de la leçon d'histoire et enseigne le pipeline de travail de 2026: un codeur-décodeur multilingue prétrainé (NLLB-200 ou mBART), la tokenization de sous-words, la recherche de faisceaux, l'évaluation BLEU et chrF, et la poignée de modes d'échec qui sont toujours en production.
> Le programme de formation de l'équipe de formation de formation professionnelle de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de formation professionnelle de formation professionnelle de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de l'équipe de formation professionnelle de l'équipe de formation professionnelle de l'équipe de la formation professionnelle de la formation professionnelle de l'équipe de la formation de la formation professionnelle de l'équipe de la formation de la formation professionnelle de la formation professionnelle de l'équipe de la formation professionnelle de la formation professionnelle de la formation professionnelle de l'équipe de la formation de la formation professionnelle de l'équipe de la formation de la formation de la formation professionnelle de la formation professionnelle de la formation professionnelle de la formation professionnelle de la formation professionnelle de la formation de la formation de la formation de la formation professionnelle de la formation de la formation professionnelle de la formation professionnelle de la formation

## Le concept de base.

> **【中文解读】**Le présent article présente les concepts et les bases théoriques de base. La connaissance de ces concepts est la prémisse de la réalisation de la réalisation de la réalisation, mais aussi le point de connaissance de l'interview et de la pratique de l'ingénierie.


![MT pipeline: tokenize → encode → decode with attention → detokenize](../assets/mt-pipeline.svg)
> ![MT 流水线：分词 → 编码 → 带注意力的解码 → 去分词](../assets/mt-pipeline.svg)

Le décodeur génère la cible, un sous-mot à la fois, en utilisant la sortie du codeur via l'attention croisée (leçon 10). Le décodeur utilise la recherche de faisceau pour éviter le piège du décodeur avide. La sortie est détocénisée, détrouquée et notée contre une référence.
> Le MT moderne est un transformateur de texte en forme de texte ordinaire. Il est un transformateur de texte en forme de texte. Il est un transformateur de texte en forme de texte. Il est un transformateur de texte en forme de texte. Il est un transformateur de texte en forme de texte. Il est un transformateur de texte en forme de texte. Il est un transformateur de texte en forme de texte. Il est un transformateur de texte en forme de texte. Il est un transformateur de texte en forme de texte. Il est un transformateur de texte en forme de texte. Il est un transformateur de texte en forme de texte. Il est un transformateur de texte en forme de texte. Il est un transformateur de texte en forme de texte. Il est un transformateur de texte en forme de texte. Il est un transformateur de texte en forme de texte. Il est un transformateur de texte en forme de texte. Il est un transformateur de texte en forme de texte. Il est un transformateur de texte en forme de texte.

Trois choix opérationnels sont à l'origine de la qualité MT du monde réel.
> 3 ⇒ La qualité de l'équipement

- **Tokenizer.**Le vocabulaire partagé entre les langues est ce qui permet de créer des paires de nulles coups dans le NLLB.
- **Model size.**NLLB-200 600M distillé s'adapte à un ordinateur portable. NLLB-200 3.3B est le plafond de production publié.
- **Decoding.**La largeur du faisceau est de 4 à 5 pour le contenu général. La longueur est de la peine pour éviter une sortie trop courte. Le décoding est restreint lorsque vous avez besoin de cohérence terminologique.
> - **分词器。**Le code de la langue est le code de la langue.
- **模型大小。**NLLB-200 蒸 600M 适合笔记本。NLLB-200 3.3B est déjà publié en production默认。54.5B est étude de plancher。
- **解码。**Généralement, le contenu est de taille 4 à 5 et la longueur du texte est de taille 5 à 5 et la longueur du texte est de taille 5 à 5 et la longueur du texte est de taille 5 à 5 et la longueur du texte est de taille 5 à 5 et la longueur du texte est de taille 5 à 5 et la longueur du texte est de taille 5 à 5 et la longueur du texte est de taille 5 à 5 et la longueur du texte est de taille 5 à 5 et la longueur du texte est de taille 5 à 5 et la longueur du texte est de taille 5 à 5 et la longueur du texte est de taille 5 à 5 et la longueur du texte est de taille 5 à 5 et la longueur du texte est de taille 5 à 5 et la longueur de 5 à 5 à 6 à 6 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 en 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 en 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 en 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à 7 à

> **【中文解读】**Cette méthode "de zéro" peut aider à comprendre le principe derrière le cadre, en cas de problème, ne sera pas bloqué dans une boîte noire.

> **【拓展：大语言模型的工程实践】**De GPT à ChatGPT, le domaine de l'NLP a connu un changement de paradigme, passant de " chaque tâche entraîne un modèle " à " un modèle résoudre toutes les tâches ".

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) est l'architecture la plus populaire de l'application de l'IA dans les entreprises actuelles: la première requête utilisateur est la requête de documents relatifs à la requête, puis la seconde requête est effectuée en tant que réponse à la requête de résolution de la requête de résolution.

> **【拓展：NLP 的多语言挑战】**Dans le monde entier, il existe plus de 7000 langues, mais les études de PNL se concentrent principalement sur l'anglais et les minorités linguistiques.


## Construisez-le et mettez-le en œuvre.
```figure
seq2seq-alignment
```

## Faites-le

### Étape 1: appel MT prétrainé
> Trois choses sont importantes.`src_lang`告诉分词器使用哪种文字和分割──`forced_bos_token_id`告诉解码器生成哪种语言──两者都是 les compétences particulières de la NLLB; mBART 和 M2M-100 使用各自的约定,不可互换──

```python
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

model_id = "facebook/nllb-200-distilled-600M"
tok = AutoTokenizer.from_pretrained(model_id, src_lang="eng_Latn")
model = AutoModelForSeq2SeqLM.from_pretrained(model_id)

src = "The cats are running."
inputs = tok(src, return_tensors="pt")

out = model.generate(
    **inputs,
    forced_bos_token_id=tok.convert_tokens_to_ids("fra_Latn"),
    num_beams=5,
    length_penalty=1.0,
    max_new_tokens=64,
)
print(tok.batch_decode(out, skip_special_tokens=True)[0])
```

```text
Les chats courent.
```

Trois choses comptent ici.`src_lang`indique au tokeniser quel script et quelle segmentation appliquer. `forced_bos_token_id`Le décodeur indique quel langage générer. Les deux sont des astuces spécifiques à la NLLB; mBART et M2M-100 utilisent leurs propres conventions et ne sont pas interchangeables.
> BLEU 测量输出与参考之间的 n-gram 重叠──四种参考 n-gram 大小(1-4), précision ratio de几何平均,对过短输出的简洁惩罚──分数在 [0, 100]──常用但难解读:30 BLEU est "可用";40 est "好";50 est "出色";1 BLEU etesinomiale différence est bruit──

### Étape 2: BLEU et chrF
> chrF  mesure des caractères de classe F  分数。 à BLEU 低估匹配的形态丰富语言更敏感──通常与BLEU一起报告──

BLEU mesure la superposition n-gramme entre la sortie et la référence. Quatre tailles de référence n-gramme (1-4), moyenne géométrique des précisions, peine de breveté pour la sortie trop courte. Le score est en [0, 100].
> 始终使用 `sacrebleu`                                                                                                                                                                                                                                                              

chrF mesure le score F au niveau des caractères. Plus sensible aux langages riches en morphologie où le sous-compte BLEU correspond.
> 现代 MT 评估使用三个互补的指标族──至少使用两个发布──

```python
import sacrebleu

hypotheses = ["Les chats courent."]
references = [["Les chats courent."]]

bleu = sacrebleu.corpus_bleu(hypotheses, references)
chrf = sacrebleu.corpus_chrf(hypotheses, references)
print(f"BLEU: {bleu.score:.1f}  chrF: {chrf.score:.1f}")
```

Toujours utiliser `sacrebleu`Il normalise la marquage afin que les scores soient comparables sur tous les papiers.
> - **启发式**(BLEU、chrF)── rapid­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­­
- **学习型**(COMET、BLEURT、BERTScore) ⋅ Modèle de neurones entraînés sur le jugement humain; comparaison traduction avec source et référence de la similitude de la signification ⋅ COMET depuis 2023 ans associé au MT, est la production standard de choix de qualité importante de 2026 ⋅
- **LLM 评委**(non-référentiel)                                                                                                                                                                                                                                                           

### La hiérarchie d'évaluation à trois niveaux (2026)
> 2026:`sacrebleu`Pour le bleu et le chrF,`unbabel-comet`Il est utilisé pour COMET, LLM est utilisé pour les signaux finaux à l'homme.

L'évaluation moderne de la MT utilise trois familles métriques complémentaires.
> 无参考指标(COMET-QE、BLEURT-QE、LLM 评委) vous faire évaluer la traduction sans référence, c'est très important pour

- **Heuristic**Rapide, basé sur la référence, interprétable, insensible à la paraphrase.
- **Learned**(COMET, BLEURT, BERTScore). Modèles neuronaux formés sur le jugement humain; comparer la similitude sémantique de la traduction à la source et à la référence. COMET a la plus grande association avec la recherche sur les MT depuis 2023 et est le défaut de production de 2026 où la qualité compte.
- **LLM-as-judge**(sans référence). Promouvoir un grand modèle pour évaluer les traductions en termes de fluidité, d'adéquation, de ton, d'adéquation culturelle. GPT-4-as-judge correspond à l'accord humain dans ~80% des cas où la rubrique est bien conçue. Utilisation pour le contenu ouvert où aucune référence n'existe.
> 80% du temps peut être passé, les 20% restants sont ratés.

La pile pratique de 2026: `sacrebleu`pour les BLEU et les chrF, `unbabel-comet`Pour les données de production, il est nécessaire de calibrer chaque métrique en fonction de 50 à 100 exemples étiquetés par l'homme.
> - **幻觉。**模型发明源中没有的内容──在不熟悉的领域词汇中常见──症状:输出流但声称源没有陈述的事实──缓解:对领域术语的约束解码,对受监管的内容的人工审查,监管输出比输入长得多的异常──
- **偏离目标语言生成。**模型翻译成错误的语言――NLLB 在罕见语言对上出奇地容易出错――缓解:验证 `forced_bos_token_id`Il n'a pas toujours utilisé le langage de reconnaissance de modèle.
- **术语漂移。**"Sign up" dans le document 1 devient "s'inscrire", dans le document 2 devient "créer un compte"── pour les utilisateurs de l'interface utilisateur 文本和面向用户的字符串, la cohérence est plus importante que la qualité initiale──缓解:词汇表约束解码或后编辑字典──
- **语体不匹配。**Pour le contenu de la clientèle, il est généralement erroné.
- **短输入长度爆炸。**非常短的输入句子经常产生过长的翻译,因为长度惩罚在约5个源代币下面急剧下降──缓解:

Les mesures sans référence (COMET-QE, BLEURT-QE, LLM-as-judge) vous permettent d'évaluer les traductions sans référence, ce qui est important pour les paires de langues à longue queue où les traductions de référence n'existent pas.
> Le modèle de formation préalable est le généralisme. Le programme n'est pas complexe:

### Étape 3: les pannes de production
>  plusieurs milliers de échantillons de haute qualité ont surpassé les centaines de millions de réseaux de prise de son.  Qualité des données de formation est la plus grande production 杆.

Le pipeline de travail ci-dessus traduira fluidement 80% du temps et échouera silencieusement les 20% restants.

- **Hallucination.**Le modèle invente un contenu qui n'était pas dans la source. C'est courant dans le vocabulaire de domaine inconnu. Symptom: la sortie est fluide mais affirme des faits que la source n'a pas déclarés. Atténuation: décoding restreint sur les termes de domaine, examen humain sur le contenu réglementé, suivi de la sortie beaucoup plus longtemps que l'entrée.
- **Off-target generation.**Le modèle traduit dans la mauvaise langue. La NLLB est étonnamment encline à cela sur des paires de langues rares.`forced_bos_token_id`et toujours décoder avec un modèle de langue-ID de vérification de la sortie.
- **Terminology drift.**"Sign up" devient "s'inscrire" dans le document 1 et "creer un compte" dans le document 2. Pour le texte de l'interface utilisateur et les chaînes d'utilisation, la cohérence est plus importante que la qualité brute.
- **Formality mismatch.**Le modèle choisit la forme la plus courante dans la formation. Pour le contenu axé sur le client, c'est généralement faux.
- **Length explosion on short input.**Les phrases d'entrée très courtes produisent souvent des traductions trop longues car la peine de longueur tombe d'un raclée inférieure à ~ 5 jetons source.

### Étape 4: réglage de domaine

Les modèles prétraînés sont généraux. La traduction juridique, médicale ou de dialogue de jeu bénéficie de manière mesurable d'une mise en forme fine sur les données parallèles de domaine.

```python
from transformers import Trainer, TrainingArguments
from datasets import Dataset

pairs = [
    {"src": "The defendant pleaded guilty.", "tgt": "L'accusé a plaidé coupable."},
]

ds = Dataset.from_list(pairs)


def preprocess(ex):
    return tok(
        ex["src"],
        text_target=ex["tgt"],
        truncation=True,
        max_length=128,
        padding="max_length",
    )


ds = ds.map(preprocess, remove_columns=["src", "tgt"])

args = TrainingArguments(output_dir="out", per_device_train_batch_size=4, num_train_epochs=3, learning_rate=3e-5)
Trainer(model=model, args=args, train_dataset=ds).train()
```

> **【中文解读】**Dans ce chapitre, nous allons montrer comment utiliser un cadre mature (comme PyTorch, HuggingFace, etc.) pour appliquer rapidement cette technique.


Quelques milliers d'exemples parallèles de haute qualité dépassent quelques centaines de milliers de ceux qui sont grattés sur le net.


> **【拓展：Prompt Engineering 与 LLM 应用】**L'ingénierie rapide est devenue la compétence centrale des ingénieurs en PNL. De la série Zero-shot à la série Few-shot, de la chaîne de pensée à la réaction, différentes stratégies de suggestion s'appliquent à différents scénarios.

## Utilisez-le avec le cadre de réalisation

La pile de production 2026 pour MT:
> MT 生产技术 de l'année 2026:

| Use case | Recommended starting point |
|---------|---------------------------|
| Any-to-any, 200 languages | `facebook/nllb-200-distilled-600M` (laptop) or `nllb-200-3.3B` (production) |
| English-centric, high quality, 50 languages | `facebook/mbart-large-50-many-to-many-mmt` |
| Short runs, cheap inference, English-French/German/Spanish | Helsinki-NLP / Marian models |
| Latency-critical browser-side | ONNX-quantized Marian (~50 MB) |
| Maximum quality, willing to pay | GPT-4 / Claude / Gemini with translation prompts |
> Je vous recommande de commencer.
|---------|---------|
| 任意到任意，200 种语言 | `facebook/nllb-200-distilled-600M`（笔记本）或 `nllb-200-3.3B`（生产） |
| 以英语为中心，高质量，50 种语言 | `facebook/mbart-large-50-many-to-many-mmt` |
| 短任务，廉价推理，英语-法语/德语/西班牙语 | Helsinki-NLP / Marian 模型 |
| 延迟敏感的浏览器端 | ONNX 量化的 Marian（约 50 MB） |
| 最高质量，愿意付费 | GPT-4 / Claude / Gemini 配合翻译提示 |

Les LLM dépassent désormais les modèles spécialisés MT sur plusieurs paires de langues à partir de 2026, en particulier sur le contenu idiomatique et le long contexte.
> Jusqu'en 2026, le programme de maîtrise en langage multilingue dépasse les modèles de maîtrise en langage spécialisé, en particulier en matière de langage et de langage.

> **【中文解读】**Cette section se concentre sur la façon de déployer le modèle en tant que produit disponible. De l'original au système de production, il faut considérer plusieurs dimensions de l'optimisation des performances, du traitement des erreurs, du contrôle, etc.


## Envoyez-le . Produit .

- Je ne sais pas .`outputs/skill-mt-evaluator.md`- Le numéro de la liste:
> 保存为 `outputs/skill-mt-evaluator.md`- Le numéro de la liste:

```markdown
---
name: mt-evaluator
description: Evaluate a machine translation output for shipping.
version: 1.0.0
phase: 5
lesson: 11
tags: [nlp, translation, evaluation]
---

Given a source text and a candidate translation, output:

1. Automatic score estimate. BLEU and chrF ranges you would expect. State whether a reference is available.
2. Five-point human-verifiable check list: (a) content preservation (no hallucinations), (b) correct language, (c) register / formality match, (d) terminology consistency with glossary if provided, (e) no truncation or length explosion.
3. One domain-specific issue to probe. E.g., for legal: named entities and statute citations. For medical: drug names and dosages. For UI: placeholder variables `{name}`.
4. Confidence flag. "Ship" / "Ship with review" / "Do not ship". Tie to the severity of issues found in step 2.

> **【中文解读】** 练习题按照 Easy/Medium/Hard 三个难度递进。建议至少完成 Medium 级别的题目，Hard 级别适合深入研究或面试准备。


Refuse to ship a translation without a language-ID check on output. Refuse to evaluate without a reference unless the user explicitly opts in to reference-free scoring (COMET-QE, BLEURT-QE). Flag any content over 1000 tokens as likely needing chunked translation.
```

## Les exercices

1. **Easy.**Traduction d' un paragraphe en français de 5 phrases en anglais et retour en anglais en utilisant `nllb-200-distilled-600M`Mesurer la proximité du retour vers l'original. Vous devriez voir la préservation sémantique avec la dérive de choix de mots.
2. **Medium.**Implémenter une vérification de l' identifiant de langue sur les sorties de traduction en utilisant `fasttext lid.176`ou `langdetect`Intégrer dans l'appel MT afin que les générations hors cible soient capturées avant de revenir.
3. **Hard.**- Je suis bien .`nllb-200-distilled-600M`Sur un corpus de domaine de votre choix de 5 000 paires, mesurez BLEU sur un ensemble de temps avant et après l'ajustement.
> 1. **简单。**Utilisation `nllb-200-distilled-600M`Pour la première fois, le mot "références" est utilisé pour désigner les mots "références".
2. **中等。**Utilisation `fasttext lid.176`Ou `langdetect`实现翻译输出的语言识别检查──集成到MT调用中,在返回前捕获偏离目标语言的生成──
3. **困难。**5000 pour le matériel de la région`nllb-200-distilled-600M`◊ mesure des modifications de la mise en page de la publication de la publication de l'article BLEU.

> **【中文解读】**Dans le tableau des termes, la définition du terme "ce que les gens disent" et "ce qu'il signifie réellement" est différenciée entre le langage quotidien et la signification technique précise.


## Les termes clés

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| BLEU | Translation score | N-gram precision with brevity penalty. [0, 100]. |
| chrF | Character F-score | Character-level F-score. More sensitive for morphologically rich languages. |
| NMT | Neural MT | Transformer encoder-decoder trained on parallel text. The 2017+ default. |
| NLLB | No Language Left Behind | Meta's 200-language MT model family. |
| Constrained decoding | Controlled output | Force specific tokens or n-grams to appear / not appear in the output. |
| Hallucination | Invented content | Model output that is not supported by the source. |
> ♪ Les termes que les gens disent souvent ♪ ♪ Le sens réel ♪
|------|-----------|---------|
| BLEU | 翻译分数 | 带简洁惩罚的 n-gram 精确率。[0, 100]。 |
| chrF | 字符 F 分数 | 字符级 F 分数。对形态丰富语言更敏感。 |
| NMT | 神经机器翻译 | 在平行文本上训练的 Transformer 编码器-解码器。2017+ 的默认。 |
| NLLB | No Language Left Behind | Meta 的 200 语言 MT 模型系列。 |
| 约束解码 | 控制输出 | 强制特定 token 或 n-gram 出现/不出现在输出中。 |
| 幻觉 | 发明内容 | 模型输出中不被源支持的内容。 |

> **【中文解读】**延伸阅读 fournit des ressources de haute qualité pour l'apprentissage en profondeur. Ces articles et cours sont des références classiques dans ce domaine, adaptés aux lecteurs qui ont besoin d'une compréhension approfondie.


## Encore une lecture

- [Costa-jussà et al. (2022). No Language Left Behind: Scaling Human-Centered Machine Translation](https://arxiv.org/abs/2207.04672) le document de la NLLB.
- [Post (2018). A Call for Clarity in Reporting BLEU Scores](https://aclanthology.org/W18-6319/)Pourquoi ?`sacrebleu`est la seule façon correcte de signaler BLEU.
- [Popović (2015). chrF: character n-gram F-score for automatic MT evaluation](https://aclanthology.org/W15-3049/) le papier chrF.
- [Hugging Face MT guide](https://huggingface.co/docs/transformers/tasks/translation) réglage pratique de la marche.
> - [Costa-jussà et al. (2022). No Language Left Behind: Scaling Human-Centered Machine Translation](https://arxiv.org/abs/2207.04672) NLLB 论文。
- [Post (2018). A Call for Clarity in Reporting BLEU Scores](https://aclanthology.org/W18-6319/)Pourquoi ?`sacrebleu`C'est la seule façon correcte de signaler BLEU.
- [Popović (2015). chrF: character n-gram F-score for automatic MT evaluation](https://aclanthology.org/W15-3049/) chrF 论文。
- [Hugging Face MT guide](https://huggingface.co/docs/transformers/tasks/translation) 实用微调演练──
