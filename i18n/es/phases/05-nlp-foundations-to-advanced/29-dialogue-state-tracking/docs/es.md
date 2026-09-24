# El estado del diálogo.

> "Quiero un restaurante barato en el norte... en realidad hacer moderado... y añadir italiano". Tres vueltas, tres actualizaciones estatales.
> "我要北边一家便宜的餐厅......改成中等价位......加意大利菜──" Tres rondas de conversación, tres veces de actualización de estado──DST 保持槽位-值字典同步,让预订成功──

> **【中文解读】**Seguir el diálogo en el estado de cambio (en el contexto de la conversación), asegurar la concordancia de las conversaciones en varias ramas.

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 17 (Chatbots), Phase 5 · 07 (POS & Parsing) | **前置知识:** Phase 5 · 17（聊天机器人），Phase 5 · 07（POS 与解析）
**Time:** ~45 minutes | **时间:** ~45 分钟

## El problema es la introducción del problema

Si se equivoca una sola ranura, el sistema reserva el restaurante equivocado, carga la tarjeta equivocada o marca la fecha equivocada.

> Una trayectoria de trabajo, sistema de trabajo, de trabajo, de trabajo, de trabajo, de trabajo, de trabajo, de trabajo, de trabajo, de trabajo, de trabajo, de trabajo, de trabajo, de trabajo, de trabajo, de trabajo, de trabajo, de trabajo, de trabajo, de trabajo, de trabajo, de trabajo, de trabajo, de trabajo, de trabajo, de trabajo, de trabajo, de trabajo, de trabajo, de trabajo, de trabajo, de trabajo, de trabajo, de trabajo, de trabajo, de trabajo, de trabajo, de trabajo, de trabajo, de trabajo, de trabajo, de trabajo, de trabajo, de trabajo, de trabajo, de trabajo, de trabajo, de trabajo, de trabajo, de trabajo, de trabajo, de trabajo, de trabajo, de trabajo, de trabajo, de trabajo, de trabajo, de trabajo, de trabajo, de trabajo, de trabajo, de trabajo, de trabajo, de trabajo, de trabajo, de trabajo, de trabajo, de trabajo, de trabajo, de trabajo, de trabajo, de trabajo, de trabajo, de trabajo, de trabajo, de trabajo, de trabajo, de trabajo, de trabajo, de trabajo, de trabajo, de trabajo, de trabajo, de trabajo, de trabajo, de trabajo, etc.

> **【中文解读】**La pregunta planteada en este capítulo es: ¿cómo entender y aplicar correctamente esta técnica en el proyecto real?

Por qué todavía importa en 2026 a pesar de los LLM: los LLM manejan el estado simple implícitamente, pero fallan en actualizaciones complejas de múltiples ranuras, cascadas de corrección ("espera, haz que sea el 7 no el 8 y cambie el tiempo a las 3 pm"), y estado persistente a lo largo de sesiones largas.

> Por qué 2026 año sigue siendo importante: LLM 隐式处理简单状态但在复杂多槽更新、纠正级联("等等等,改成7号不是8号,时间改成下午3点") y长会话的持久状态失败;;

## El concepto central.

> **【中文解读】**Este artículo presenta la base de los conceptos y teorías centrales.

**Dialogue state.**Un conjunto de pares (flip, valor) que captura lo que el sistema sabe sobre el objetivo del usuario en cada turno. Ejemplo: {cucina: italiano, precio: moderado, área: norte}.

> **对话状态。**Cada vez más, el usuario puede tener una experiencia en el mundo de la música.

**State update.**A cada turno, actualice el estado basado en la nueva declaración del usuario. Tres operaciones: establecer, actualizar, borrar.

> **状态更新。**Cada ronda de conversación según el nuevo estado de usuario.

**Belief state.**Distribución de probabilidades sobre posibles valores de ranura. Útil cuando el usuario es ambiguo ("un restaurante" → cocina=Ninguna, pero la creencia muestra italiano=0.3, chino=0.2, ...).

> **信念状态。**Puede ser que el número de personas que utilizan el servicio sea de menor importancia.

> **【拓展：大语言模型的工程实践】**Desde el GPT hasta el ChatGPT, el campo de la NLP ha experimentado un cambio de paradigma.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) es la arquitectura más popular de la aplicación de IA en las empresas actuales.
```figure
n5-slot-tracker
```

## Construye el mismo

> **【拓展：NLP 的多语言挑战】**En todo el mundo hay más de 7000 idiomas, pero los estudios de PNL se centran principalmente en inglés y en una minoría de idiomas.

## Construye y realiza.

> **【中文解读】**Este capítulo pasa por el código desde el núcleo de algoritmos de implementación de cero.

### Paso 1: rastreador de estado de valor de ranura

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

### Paso 2: Actualización del estado basado en el LLM

```python
def llm_state_update(dialogue_history, current_state, llm):
    prompt = f"""Given the dialogue history and current state, extract slot updates.

Current state: {current_state}
Dialogue: {dialogue_history[-1]}

Output JSON of updated slots."""
    return llm(prompt)
```

> **【中文解读】**Este capítulo muestra cómo utilizar un marco maduro para aplicar rápidamente esta tecnología.

> **【拓展：Prompt Engineering 与 LLM 应用】**La ingeniería rápida se ha convertido en la habilidad central de los ingenieros de PNL.

## Usalo con el marco de ejecución

> **【中文解读】**Este apartado se centra en cómo el modelo se desplegará en productos disponibles.

- **Rule-based DST.**Rellenar la ranura con regex + extracción de entidades. Rápido, predecible. / 基于规则的 DST──正则 + 实体提取──快速、可预测──
- **Neural DST.**Entrenamiento en MultiWOZ o conjunto de datos similar. Mejor generalización. / 神经 DST──在 MultiWOZ 上训练──更好泛化──
- **LLM-based DST.**Promover el LLM para extraer actualizaciones estatales.
- **Hybrid.**LLM para extracción + base de reglas para validación. Recomendación de producción. / 混合。LLM 提取 + 规则验证。生产推──

## Envíe el producto .

Salvo como`outputs/skill-dst-builder.md`¿Qué es esto ?

> 保存为                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `outputs/skill-dst-builder.md`¿Qué es esto ?

```markdown
Given a task-oriented dialogue system, design DST.
1. Slots to track.
2. State update method (rule, neural, LLM).
3. Confirmation and correction handling.
```

## Los ejercicios.

1. **Easy.**Construir un sistema de reserva de restaurantes basado en reglas. / **简单。**Por lo tanto, el sistema de reserva de restaurantes se construye en base a las normas de DST.
2. **Medium.**Añadir extracción de estado basada en LLM. Comparar con la base de reglas. / **中等。**添加基于LLM de estado提取──
3. **Hard.**Evaluar el DST en MultiWOZ. Informar la exactitud de los objetivos conjuntos. / **困难。**En MultiWOZ 上 evaluar el DST

## Términos clave .

| Term / 术语 | What it means / 含义 |
|------|-----------------------|
| Dialogue state（对话状态） | Current (slot, value) pairs. / 当前槽位-值对。 |
| Slot filling（槽位填充） | Extracting values for predefined slots. / 为预定义槽位提取值。 |
| Belief state（信念状态） | Probability distribution over slot values. / 槽位值的概率分布。 |
| MultiWOZ | Multi-domain dialogue dataset. / 多领域对话数据集。 |

## Más Leer más Leer más

- [MultiWOZ](https://arxiv.org/abs/1810.00278) conjunto de datos estándar de DST. / 标准 DST 数据集──
- [TRADE](https://arxiv.org/abs/1810.00278) rastreador de estado de diálogo transferible. / 可迁移对话状态跟踪器──
- [SimpleTOD](https://arxiv.org/abs/2005.00796) simple DST de extremo a extremo. / 简单端到端 DST──
