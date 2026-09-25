# Dialeto de estado de rastreamento .

> "Quero um restaurante barato no norte... que seja moderado... e adicione italiano". Três turnos, três atualizações de estado.
> "我要北边一家便宜的餐厅......改成中等价位......加意菜──" 三轮对话,三次状态更新──DST 保持槽位-值字典同步,让预订成功──

> **【中文解读】**Seguir o diálogo em mudança de estado (s)

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 17 (Chatbots), Phase 5 · 07 (POS & Parsing) | **前置知识:** Phase 5 · 17（聊天机器人），Phase 5 · 07（POS 与解析）
**Time:** ~45 minutes | **时间:** ~45 分钟

## O problema é o problema da introdução

Se você errar em um único slot, o sistema reserva o restaurante errado, carrega o cartão errado ou agenda a data errada.

> Uma sala de conversa é fazer com que os dispositivos se sintam como uma consulta de banco de dados ou como uma diferença de diálogo.

> **【中文解读】**A questão que se coloca neste capítulo é: como entender e aplicar esta técnica na prática da construção.

Por que ainda importa em 2026 apesar dos LLM: LLM lidam com o estado simples implicitamente, mas falham em atualizações complexas de várias slots, cascadas de correção ("esperar, torná-lo o 7o não o 8o, e mude a hora para as 15h"), e estado persistente em sessões longas.

> O LM 隐式处理简单状态但在复杂多槽更新、纠正级联("等等等,改成7号不是8号,时间改成下午3点") e长会话的持久状态失败──显然 DST 仍然是任务导向系统的生产答案──

## O conceito central.

> **【中文解读】**Este artigo apresenta os conceitos e as bases da teoria.

**Dialogue state.**Um conjunto de pares (fratura, valor) que capta o que o sistema sabe sobre o objetivo do usuário em cada turno.

> **对话状态。**Cada round dialog中一组 (槽位, 值) 对,捕获系统对用户目标的理解──例如:{cuisine: Italian, price: moderate, area: north}──

**State update.**Em cada turno, atualize o estado com base na nova expressão do usuário.

> **状态更新。**Cada rodada de diálogo de acordo com o novo status do usuário.

**Belief state.**Distribuição de probabilidade sobre possíveis valores de slots. Útil quando o usuário é ambíguo ("um restaurante" → culinária = Nenhuma, mas a crença mostra italiano = 0,3, chinês = 0,2, ...).

> **信念状态。**Pode ser que o número de pessoas que estão em situação de pobreza seja muito maior.

> **【拓展：大语言模型的工程实践】**O GPT foi transformado em um campo de discussão.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) é a estrutura mais popular de aplicação de IA em empresas atuais.
```figure
n5-slot-tracker
```

## Construí-lo

> **【拓展：NLP 的多语言挑战】**No mundo há mais de 7000 idiomas, mas os estudos de PNL se concentram principalmente em inglês e em uma minoria de línguas.

## Construí-lo e realizei-o.

> **【中文解读】**Este é o capítulo do código do zero implementar o algoritmo central.

### Passo 1: rastreador de estado de valor de slot

```python
class DialogueStateTracker:
    def __init__(self, slots):
        self.state = {slot: None for slot in slots}
        self.history = []

    def update(self, slot_values):
        for slot, value in slot_values.items():
            if slot in self.state:
                self.state[slot] = value
        self.history.append(dict(self.state))

    def get_missing_slots(self):
        return [s for s, v in self.state.items() if v is None]

    def is_complete(self):
        return all(v is not None for v in self.state.values())


tracker = DialogueStateTracker(["cuisine", "price", "area", "party_size"])
tracker.update({"cuisine": "Italian", "area": "north"})
print(tracker.get_missing_slots())  # ['price', 'party_size']
print(tracker.is_complete())  # False
```

### Passo 2: Atualização do estado baseada no Mestrado em Direitos Jurídicos

```python
def llm_state_update(dialogue_history, current_state, llm):
    prompt = f"""Given the dialogue history and current state, extract slot updates.

Current state: {current_state}
Dialogue: {dialogue_history[-1]}

Output JSON of updated slots."""
    return llm(prompt)
```

> **【中文解读】**Este capítulo mostra como usar um quadro de desenvolvimento rápido para aplicar esta tecnologia.

> **【拓展：Prompt Engineering 与 LLM 应用】**A Engenharia Prometida tornou-se a habilidade central de engenheiros de PNL.

## Use-o com o framework implementado.

> **【中文解读】**Este capítulo trata-se de como o modelo será implementado para produtos disponíveis.

- **Rule-based DST.**Preenchimento de slot com regex + extrusão de entidade. Rapido, previsível. / 基于规则的 DST──正则 + 实体提取──快速、可预测──
- **Neural DST.**Treinar em MultiWOZ ou conjunto de dados semelhantes. Melhor generalização. / 神经 DST──在 MultiWOZ 上訓練──更好泛化──
- **LLM-based DST.**Promover o LLM para extrair atualizações do estado.
- **Hybrid.**LLM para extração + regra baseada para validação. recomendação de produção. / 混合。LLM 提取 + 规则验证。生产推──

## Envia-o . Produto .

Salva como`outputs/skill-dst-builder.md`- Não .

> 保存为 `outputs/skill-dst-builder.md`- Não .

```markdown
Given a task-oriented dialogue system, design DST.
1. Slots to track.
2. State update method (rule, neural, LLM).
3. Confirmation and correction handling.
```

## Exercícios.

1. **Easy.**Construir um sistema de reserva de restaurantes baseado em regras.**简单。**Pormenor, o sistema de preenchimento de restaurantes é construído com base nas regras do DST.
2. **Medium.**Adicionar extração de estado baseada em LLM. Comparar com baseada em regras. / **中等。**添加基于 LLM 状态提取──
3. **Hard.**Avaliação do DST no MultiWOZ. Relata a precisão do objectivo comum. / **困难。**Em MultiWOZ 上 avalia DST

## Termos-chave .

| Term / 术语 | What it means / 含义 |
|------|-----------------------|
| Dialogue state（对话状态） | Current (slot, value) pairs. / 当前槽位-值对。 |
| Slot filling（槽位填充） | Extracting values for predefined slots. / 为预定义槽位提取值。 |
| Belief state（信念状态） | Probability distribution over slot values. / 槽位值的概率分布。 |
| MultiWOZ | Multi-domain dialogue dataset. / 多领域对话数据集。 |

## Mais leitura 延伸阅读

- [MultiWOZ](https://arxiv.org/abs/1810.00278) conjunto de dados padrão DST. / 标准 DST 数据集──
- [TRADE](https://arxiv.org/abs/1810.00278) transferivel de diálogo estado de rastreamento. / 可迁移对话状态跟踪器──
- [SimpleTOD](https://arxiv.org/abs/2005.00796) simples DST de ponta a ponta. / 简单端到端 DST──
