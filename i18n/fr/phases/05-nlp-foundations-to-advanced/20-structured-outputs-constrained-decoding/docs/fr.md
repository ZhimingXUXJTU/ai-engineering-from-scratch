# Les sorties structurées et le décoding restreint

> Demandez à un LLM pour JSON. Obtenez JSON la plupart du temps. Dans la production, "la plupart" est le problème. Le décoding restreint se transforme en "la plupart" en "tous les temps" en éditant les logits avant le prélèvement.
> 让LLM 输出 JSON──大多数时候能得到 JSON──在生产中,"大多数"就是问题──约束解码通过在采样前编辑逻辑将"大多数"变成"总是"──

> **【中文解读】**让LLM 输出结构化数据如JSON、SQL──

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 19 (Subword Tokenization) | **前置知识:** Phase 5 · 19（子词分词）
**Time:** ~60 minutes | **时间:** ~60 分钟

## Le problème , l' introduction du problème

La génération de formulaires libres n'est pas un contrat. C'est une suggestion. Vous demandez JSON, vous obtenez une chaîne en forme de JSON avec une virgule arrière, un backtick supplémentaire ou une clé nommée en allemand. Chaque parseur en aval se brise. Vous demandez une requête SQL, vous en obtenez une avec un nom de colonne halluciné.

> La libéralisation de format n'est pas un accord, c'est une suggestion. Vous demandez JSON, obtenez un avec un bout de commentaire.

> **【中文解读】**La question posée dans ce chapitre est la suivante: comment comprendre et appliquer correctement cette technique dans la conception pratique. Comprendre le contexte de la question aide à saisir les principaux facteurs de décision concernant le type de technologie. Dans les systèmes d'IA réels, le type de technique erroné coûte souvent plus cher que le coût de la mise en œuvre de détails.

Trois couches existent en 2026.

> En 2026, il existe trois niveaux de solution:

1. **Prompting.**Demandez gentiment. "Retournez seulement l'objet JSON". Fonctionne environ 85 à 95% du temps. Échoue sur les cas de bord, les sorties longues et les entrées adversitaires. / **提示。**Bon bon demande. "Retourner uniquement JSON aux objets".
2. **Constrained decoding.**Masquer les logits de jetons suivants invalides à chaque étape de génération afin que la sortie soit toujours conforme à un schéma (schéma JSON, regex, grammaire sans contexte). Fonctionne 100%.**约束解码。**Dans chaque étape de production, les logits de jetons suivants sont bloqués, ce qui permet à la sortie de toujours être conforme au modèle.
3. **Tool/function calling.**Exécution structurée via l'interface d'appel d'outil natif du modèle. Le modèle émet un objet JSON directement, pas sous forme de texte.**工具/函数调用。**通过模型原生工具调用接口的结构化输出──最佳延迟,最佳可靠性,但模型特定──

## Le concept de base.

> **【中文解读】**Le présent article présente les concepts et les bases théoriques de base. La connaissance de ces concepts est la prémisse de la réalisation de la réalisation de la réalisation, mais aussi le point de connaissance de l'interview et de la pratique de l'ingénierie.

**Logit masking.**Le modèle produit une distribution de probabilité sur le vocabulaire à chaque étape de la génération. Le décoding restreint calcule l'ensemble des jetons suivants valides (donné le schéma et ce qui a été généré jusqu'à présent) et fixe toutes les autres logites à -inf avant softmax.

> **Logit 屏蔽。**Dans chaque étape de génération, le modèle produit une probabilité de distribution sur le tableau de mots.

**JSON schema constraints.**Pour la sortie JSON, la contrainte s'impose: les braces d'ouverture correspondent aux braces de fermeture, les touches sont citées comme des chaînes, les valeurs correspondent à leurs types déclarés, les champs requis sont présents, aucun champ supplémentaire au-delà du schéma.

> **JSON 模式约束。**Pour les sorties JSON, le lien est obligatoire: open closed parentheses matching, key is with eting numbers strings, value matching declaration type, must fill, existent, have a mode, have a mode, have a mode, have a mode, have a mode, have a mode, have a mode, have a mode, have a mode, have a mode, have a mode, have a mode, have a mode, have a mode, have a mode, have a mode, have a mode, have a mode, have a mode, have a mode, have a mode, have a mode, have a mode, have a mode, have a mode, have a mode, have a mode, have a mode, have a mode, have a mode, have a mode, have a mode, have a mode, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have, have

> **【拓展：大语言模型的工程实践】**De GPT à ChatGPT, le domaine de l'NLP a connu un changement de paradigme, passant de " chaque tâche entraîne un modèle " à " un modèle résoudre toutes les tâches ".

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) est l'architecture la plus populaire de l'application de l'IA dans les entreprises actuelles: la première requête utilisateur est la requête de documents relatifs à la requête, puis la seconde requête est effectuée en tant que réponse à la requête de résolution de la requête de résolution.

> **【拓展：NLP 的多语言挑战】**Dans le monde entier, il existe plus de 7000 langues, mais les études de PNL se concentrent principalement sur l'anglais et les minorités linguistiques.

## Construisez-le et mettez-le en œuvre.
```figure
constrained-decoder
```

## Faites-le

> **【中文解读】**Cette méthode "de zéro" peut aider à comprendre le principe derrière le cadre, en cas de problème, ne sera pas bloqué dans une boîte noire.

### Étape 1: masquage simple de la logite

```python
import json
import re


def mask_logits(logits, valid_token_ids):
    """Set invalid token logits to -inf."""
    mask = torch.full_like(logits, float('-inf'))
    mask[valid_token_ids] = logits[valid_token_ids]
    return mask
```

Le concept principal: à chaque étape, seul un sous-ensemble de jetons est valide.

> 核心洞察: dans chaque étape, seul le token 子集是有效的──高效计算该子集是工程挑战──

### Étape 2: Validation du schéma JSON pendant la génération

```python
import jsonschema

schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "integer", "minimum": 0},
    },
    "required": ["name", "age"],
}

def validate_json_output(text, schema):
    try:
        data = json.loads(text)
        jsonschema.validate(data, schema)
        return True, data
    except (json.JSONDecodeError, jsonschema.ValidationError) as e:
        return False, str(e)
```

### Étape 3: en utilisant l' exécuter le format LM

```python
from lmformatenforcer import JsonSchemaParser, generate_enforced

parser = JsonSchemaParser(schema)
# Use with any Hugging Face model's generate method
# result = generate_enforced(model, tokenizer, parser, prompt)
```

> **【中文解读】**Ce chapitre montre comment mettre en œuvre rapidement cette technique dans un cadre mature.

> **【拓展：Prompt Engineering 与 LLM 应用】**L'ingénierie rapide est devenue la compétence centrale des ingénieurs en PNL. De la série Zero-shot à la série Few-shot, de la chaîne de pensée à la réaction, différentes stratégies de suggestion s'appliquent à différents scénarios.

## Utilisez-le avec le cadre de réalisation

> **【中文解读】**Cette section se concentre sur la façon de déployer le modèle en tant que produit disponible. De l'original au système de production, il faut considérer plusieurs dimensions de l'optimisation des performances, du traitement des erreurs, du contrôle, etc.

Les options de production de 2026:

> Les projets de production pour l'année 2026:

| Approach / 方案 | Reliability / 可靠性 | Latency cost / 延迟成本 | Best for / 最适合 |
|---------|------------|-------------|---------|
| Prompting / 提示 | ~85-95% / 约 85-95% | None / 无 | Prototypes, non-critical paths / 原型、非关键路径 |
| Constrained decoding / 约束解码 | 100% / 100% | +10-30% / 加 10-30% | Production APIs / 生产 API |
| Tool calling / 工具调用 | ~99.9% / 约 99.9% | Lowest / 最低 | Model-native workflows / 模型原生工作流 |

## Envoyez-le . Produit .

- Je ne sais pas .`outputs/prompt-structured-output.md`- Le numéro de la liste:

> 保存为 `outputs/prompt-structured-output.md`- Le numéro de la liste:

```markdown
Given an LLM output that must be structured (JSON, SQL, etc.), pick the right approach and implement it.
1. Schema definition. JSON Schema, regex, or grammar.
2. Enforcement method. Prompting, constrained decoding, or tool calling.
3. Fallback plan. What happens when the output still fails validation.
```

> **【中文解读】** Exercices de base selon Easy/Medium/Hard 三个难度递进──建议至少完成  级别的题目,  级别适合深入研究或面试准备──

## Les exercices

1. **Easy.**Construisez un extracteur JSON instantané et mesurez le taux de réussite sur 100 appels LLM. / **简单。**构建纯提示的 JSON 提取器──测量 100次 LLM 调用成功率──
2. **Medium.**Implémenter le décoding restreint pour un schéma JSON simple en utilisant le masquage logit. / **中等。**Utiliser le logiciel de protection pour réaliser le code JSON simple.
3. **Hard.**Comparer le décoding restreint par rapport à l'outil qui nécessite une charge de travail de production.**困难。**Comparer le décompte et l'utilisation des outils sur la charge de production.

> **【中文解读】**Dans le tableau des termes, la définition du terme "ce que les gens disent" et "ce qu'il signifie réellement" est différenciée entre le langage quotidien et la signification technique précise.

## Les termes clés

| Term / 术语 | What people say / 人们常说的 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| Constrained decoding（约束解码） | Force valid output / 强制有效输出 | Mask invalid logits at each step. / 每步屏蔽无效 logits。 |
| Logit masking（Logit 屏蔽） | Block bad tokens / 阻止坏 token | Set invalid token logits to -inf before softmax. / softmax 前将无效 token logits 设为 -inf。 |
| JSON Schema | JSON validation rules / JSON 验证规则 | Declarative schema for validating JSON structure and types. / 验证 JSON 结构和类型的声明式模式。 |
| Tool calling（工具调用） | Function calling / 函数调用 | Model emits structured arguments directly via native interface. / 模型通过原生接口直接发出结构化参数。 |

> **【中文解读】**延伸阅读 fournit des ressources de haute qualité pour l'apprentissage en profondeur. Ces articles et cours sont des références classiques dans ce domaine, adaptés aux lecteurs qui ont besoin d'une compréhension approfondie.

## Encore une lecture

- [LM Format Enforcer](https://github.com/noamgat/lm-format-enforcer) la production est limitée à la bibliothèque de décoding. / 生产级约束解码库。
- [Outlines](https://github.com/dottxt-ai/outlines) génération structurée avec regex/JSON/CFG. / 带 regex/JSON/CFG 的结构化生成──
- [JSON Schema specification](https://json-schema.org/) la norme de validation JSON. / JSON 验证标准。
