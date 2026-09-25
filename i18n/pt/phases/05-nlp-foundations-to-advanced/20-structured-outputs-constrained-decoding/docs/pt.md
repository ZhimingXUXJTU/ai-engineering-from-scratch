# Output estruturado e decodificação restrita

> Peça um LLM para JSON. Obtenha JSON a maior parte do tempo. Na produção, "a maioria" é o problema. A decodificação restrita transforma "a maioria" em "sempre" editando os logits antes da amostragem.
> 让LLM 输出 JSON──大多数时候能得到 JSON──在生产中,"大多数"就是问题──约束解码通过在采样前编辑逻辑将"大多数" 变成"总是"──

> **【中文解读】**让LLM 输出结构化数据如JSON、SQL──

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 19 (Subword Tokenization) | **前置知识:** Phase 5 · 19（子词分词）
**Time:** ~60 minutes | **时间:** ~60 分钟

## O problema é o problema da introdução

A geração de formulário livre não é um contrato. É uma sugestão. Você pede JSON, você recebe uma cadeia em forma de JSON com uma vírgula atrás, um backtick extra ou uma chave com nome em alemão. Cada parser downstream quebra. Você pede uma consulta SQL, você recebe uma com um nome de coluna alucinado. Na produção, essas falhas não são bugs  são incidentes.

> O gerador de formato livre não é um acordo, é uma recomendação. Você requer JSON, obtém um com o fim de um número, ou um número de erros de código em alemão.

> **【中文解读】**A questão que se coloca neste capítulo é: como entender e aplicar esta tecnologia de forma correta na engenharia real.

Existem três camadas em 2026.

> Em 2026 existem três níveis de solução:

1. **Prompting.**Pergunte bem. "Retorna apenas o objeto JSON". Funciona entre 85 e 95% do tempo. Falha em casos de borda, saídas longas e entradas adversárias. / **提示。**Boa solicitação. "Tornar apenas JSON para objetos". Cerca de 85-95% do tempo válido.
2. **Constrained decoding.**Mascarar logits inválidos de tokens próximos em cada etapa de geração para que a saída sempre esteja em conformidade com um esquema (esquema JSON, regex, gramática livre de contexto). Funciona 100%.**约束解码。**Em cada fase de geração, bloqueia o próximo logite de token, fazendo com que o output sempre esteja em conformidade com o modelo.
3. **Tool/function calling.**Output estruturado através da interface de chamada de ferramenta nativa do modelo. O modelo emite um objeto JSON diretamente, não como texto. Melhor latência, melhor confiabilidade, mas modelo-específico. / **工具/函数调用。**通过模型原生工具调用接口的结构化输出──最佳延迟,最佳可靠性,但模型特定──

## O conceito central.

> **【中文解读】**Este capítulo apresenta os conceitos e teorias fundamentais.

**Logit masking.**A decodificação restringida calcula o conjunto de tokens válidos próximos (dado o esquema e o que foi gerado até agora) e define todos os outros logits para -inf antes de softmax.

> **Logit 屏蔽。**Em cada fase de geração, o modelo em um formulário gerará uma probabilidade de distribuição.

**JSON schema constraints.**Para a saída JSON, a restrição é aplicada: os braços de abertura correspondem aos braços de fechamento, as chaves são citadas como strings, os valores correspondem aos tipos declarados, os campos necessários estão presentes, não há campos extras além do esquema. Esta é uma restrição gramática livre de contexto, calculada incrementalmente.

> **JSON 模式约束。** Para JSON 输出,约束强制:开闭括号匹配、键是带引号字符串、值匹配声明类型、必填字段存在、无模式外额外字段── é um 下文无关语法约束,增量计算──

> **【拓展：大语言模型的工程实践】**De GPT a ChatGPT, o campo do NLP passou por uma transição de paradigma de "cada tarefa treinar um modelo" para "um modelo resolver todas as tarefas".

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) é a estrutura mais popular de aplicações de IA em empresas: fazer uma consulta de usuário antes de fazer uma consulta de documentos relacionados, e reapreciar o resultado da consulta como resposta de produção para o LLM.

> **【拓展：NLP 的多语言挑战】**No mundo todo, há mais de 7000 idiomas, mas os estudos de PNL se concentram principalmente em inglês e outras línguas.

## Construí-lo e realizei-o.
```figure
constrained-decoder
```

## Construí-lo

> **【中文解读】**Este é um método de "desde zero" que ajuda a entender o princípio da estrutura, não é um problema que se encontra em uma caixa negra.

### Passo 1: mascaramento simples de logit

```python
import json
import re


def mask_logits(logits, valid_token_ids):
    """Set invalid token logits to -inf."""
    mask = torch.full_like(logits, float('-inf'))
    mask[valid_token_ids] = logits[valid_token_ids]
    return mask
```

A ideia principal: em cada etapa, apenas um subconjunto de tokens é válido.

> 核心洞察: em cada passo, apenas token 子集是有效的──高效计算该子集是工程挑战──

### Passo 2: Validação de esquema JSON durante a geração

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

### Passo 3: usando o Formativo de Formatação LM

```python
from lmformatenforcer import JsonSchemaParser, generate_enforced

parser = JsonSchemaParser(schema)
# Use with any Hugging Face model's generate method
# result = generate_enforced(model, tokenizer, parser, prompt)
```

> **【中文解读】**Este capítulo mostra como aplicar rapidamente esta tecnologia em um quadro de experiência.

> **【拓展：Prompt Engineering 与 LLM 应用】**A Engenharia Prometida tornou-se a habilidade central dos engenheiros de PNL. De zero-shot a poucos-shot, de cadeia de pensamento a reação, diferentes estratégias de orientação são aplicadas a diferentes cenários.

## Use-o com o framework implementado.

> **【中文解读】**Este capítulo se concentra em como o modelo será implantado como produto disponível. De modelo original a nível de produção, os sistemas precisam considerar várias dimensões de otimização de desempenho, tratamento de erros, controle, etc.

As opções de produção para 2026:

> O projeto de produção para 2026:

| Approach / 方案 | Reliability / 可靠性 | Latency cost / 延迟成本 | Best for / 最适合 |
|---------|------------|-------------|---------|
| Prompting / 提示 | ~85-95% / 约 85-95% | None / 无 | Prototypes, non-critical paths / 原型、非关键路径 |
| Constrained decoding / 约束解码 | 100% / 100% | +10-30% / 加 10-30% | Production APIs / 生产 API |
| Tool calling / 工具调用 | ~99.9% / 约 99.9% | Lowest / 最低 | Model-native workflows / 模型原生工作流 |

## Envia-o . Produto .

Salva como`outputs/prompt-structured-output.md`- Não .

> 保存为 `outputs/prompt-structured-output.md`- Não .

```markdown
Given an LLM output that must be structured (JSON, SQL, etc.), pick the right approach and implement it.
1. Schema definition. JSON Schema, regex, or grammar.
2. Enforcement method. Prompting, constrained decoding, or tool calling.
3. Fallback plan. What happens when the output still fails validation.
```

> **【中文解读】**Practicação de temas de fácil/médio/difícil  3o dificuldade de passagem  Recomendação de completar pelo menos Praça de nível médio Classe difícil  Adaptação a pesquisa profunda ou preparação para o encontro 

## Exercícios.

1. **Easy.**Construa um extrator JSON de ponta-só. Meter a taxa de sucesso em 100 chamadas de LLM. / **简单。**构建纯提示的 JSON 提取器──测量 100 次 LLM 调用成功率──
2. **Medium.**Implementar decodificação restrita para um esquema JSON simples usando logit masking. / **中等。**Utilize logit 屏蔽为简单 JSON 模式实现约束解码──
3. **Hard.**Comparar decodificação restrita versus ferramenta que exige uma carga de trabalho de produção. Relatar latência, confiabilidade e custo. / **困难。**Comparar a redução de volume de produção com a redução de volume de produção.

> **【中文解读】**No 术语表中的"O que as pessoas dizem" vs "O que realmente significa" 区分日常口语和精确技术含义── em equipe,统一术语定义可以避免大量沟通误解──

## Termos-chave .

| Term / 术语 | What people say / 人们常说的 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| Constrained decoding（约束解码） | Force valid output / 强制有效输出 | Mask invalid logits at each step. / 每步屏蔽无效 logits。 |
| Logit masking（Logit 屏蔽） | Block bad tokens / 阻止坏 token | Set invalid token logits to -inf before softmax. / softmax 前将无效 token logits 设为 -inf。 |
| JSON Schema | JSON validation rules / JSON 验证规则 | Declarative schema for validating JSON structure and types. / 验证 JSON 结构和类型的声明式模式。 |
| Tool calling（工具调用） | Function calling / 函数调用 | Model emits structured arguments directly via native interface. / 模型通过原生接口直接发出结构化参数。 |

> **【中文解读】**延伸阅读 fornece recursos de alta qualidade para a aprendizagem profunda.

## Mais leitura 延伸阅读

- [LM Format Enforcer](https://github.com/noamgat/lm-format-enforcer) produção limitada de decodificação biblioteca. / 生产级约束解码库。
- [Outlines](https://github.com/dottxt-ai/outlines) geração estruturada com regex/JSON/CFG. / 带 regex/JSON/CFG 的结构化生成──
- [JSON Schema specification](https://json-schema.org/) o padrão para validação JSON. / JSON 验证标准。
