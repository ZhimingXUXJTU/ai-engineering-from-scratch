# Diyaloğu takip etme durumu

> "Şimalde ucuz bir restoran istiyorum... aslında onu moderat yapıp İtalyanca ekle". Üç dönüş, üç devlet güncelleme.
> "我要北边一家便宜的餐厅......改成中等价位......加意菜──" 三轮对话,三次状态更新──DST 保持槽位-值字典同步,让预订成功──

> **【中文解读】**Sohbetlerdeki durum değişimleri, çok sayıda sohbetin uyumlu olmasını sağlamak.

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 17 (Chatbots), Phase 5 · 07 (POS & Parsing) | **前置知识:** Phase 5 · 17（聊天机器人），Phase 5 · 07（POS 与解析）
**Time:** ~45 minutes | **时间:** ~45 分钟

## Sorunlar. Sorunlar.

Bir slot yanlış olursa sistem yanlış restoranı kaydeder, yanlış kartı ücretlendirir veya yanlış tarihte programlanır. DST, bir veritabanı sorgu gibi hisseden bir chatbot ile bir sohbet gibi hisseden bir chatbot arasındaki fark.

> Bir slot sitesi yanlış yapılır, sistem bir yanlış yemek odası, bir yanlış yemek odası veya bir yanlış günlüğü vardır.

> **【中文解读】**Bu bölümde sorulan soru şu: Bu tekniği nasıl gerçek tasarımda doğru şekilde anlayabilir ve uygulayabilirsiniz.

LLM'lere rağmen neden 2026'da hâlâ önemli: LLM'ler basit durumu içeren bir şekilde ele alır, ancak karmaşık çoklu yuva güncellemelerinde başarısız olurlar, düzeltme kaskadları ("bırak, 7.'yi 8.'ye değil, saatini 3'ye değiştirin"), ve uzun seanslar boyunca sürekli durum. Açık DST hala görev odaklı sistemler için üretim cevabıdır.

> 2026 yıl neden hâlâ önemli:LLM 隐式处理简单状态但在复杂多槽更新、纠正级联("等等等,改成7号不是8号,时间改成下午3点")

## Konsepten bir şey.

> **【中文解读】**本節介绍核心概念和理论基础──

**Dialogue state.**Sistemin her dönüşte kullanıcı hedefi hakkında bildiklerini yakalayan (slot, değer) çiftler kümesi. Örnek: {mutfağı: İtalyan, fiyat: ortalama, alan: kuzey}.

> **对话状态。**Her zamanki bir grup konuşma (槽位, 值) için, captur system对用户目标的理解──例如:{kuhinji: İtalyan, fiyat: ortalama, alan: kuzey}──

**State update.**Her seferinde, yeni kullanıcı ifadesine göre durumu güncelleyin.

> **状态更新。**Her konuşma yeni kullanıcı konuşması yeni durumlara göre gerçekleşir.

**Belief state.**Muhtemelen slot değerleri üzerinde olasılık dağılımı. Kullanıcı belirsiz olduğunda yararlıdır ("bir restoran" → mutfak = Hiçbir, ancak inanç İtalyanca = 0,3, Çinli = 0,2, ...).

> **信念状态。**Belki de bu bir çeşit bir yemektir.

> **【拓展：大语言模型的工程实践】**GPT'den ChatGPT'ye kadar, NLP'de değişim biçimi yaşandı.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG)   检索增强生成 (RAG)  RAG)   检索增强生成 (RAG) 检索增强生成 (RAG) 检索增强生成 (RAG) RAG) 检索增强生成 (RAG) 检索增强生成 (RAG) 检索增强生成 (RAG) 检索增强生成 (RAG) 检索增强生成 (RAG) 检索增强生成 (RAG) 检索增强生成) 检索增强生成 (RAG) 检索增强生成 (RAG) 检测增强生成) 检测增强生成 (RAG) 检测增强生成) 检测增强的架构 (RAG) 检测) 检测增强的架构
```figure
n5-slot-tracker
```

## Yapın

> **【拓展：NLP 的多语言挑战】**Dünya çapında 7000'den fazla dil vardır, ancak NLP çalışmaları çoğunlukla İngilizce ve birkaç dil üzerinde yoğunlaşmaktadır.

## Yapın.

> **【中文解读】**Bu bölüm kodla birlikte, çekirdek algoritmasını da tamamlıyor.

### Adım 1: Çatış değerleri durum izleyicisi

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

### Adım 2: LLM'ye dayalı devlet güncelleştirmesi

```python
def llm_state_update(dialogue_history, current_state, llm):
    prompt = f"""Given the dialogue history and current state, extract slot updates.

Current state: {current_state}
Dialogue: {dialogue_history[-1]}

Output JSON of updated slots."""
    return llm(prompt)
```

> **【中文解读】**Bu bölüm, bu teknolojiyi nasıl hızlı bir şekilde uygulayacağımızı gösterir.

> **【拓展：Prompt Engineering 与 LLM 应用】**Hızlı Mühendislik NLP mühendislerinin temel beceri haline geldi.

## Çerçeveyi kullanın.

> **【中文解读】**Bu bölümde modellerin kullanılabilir ürünler için nasıl deploye edileceği üzerinde yoğunlaşmaktadır.

- **Rule-based DST.**Regex + entite çıkarımı ile slot doldurma. Hızlı, öngörülebilir. /  基于规则的DST──正则 + 实体提取──快速、可预测──
- **Neural DST.**Eğitim MultiWOZ veya benzer veri kümesi. Daha iyi genelleştirme.
- **LLM-based DST.**Yüksek Lisans Yüksek Lisansı'nı, devlet güncellemelerini çıkarmak için teşvik et.
- **Hybrid.**Çekim için LLM + doğrulama için kural tabanlı. Üretim tavsiyesi. / 混合。LLM 提取 + 规则验证。生产推──

## İndirin . Ürünler .

- Kaydet .`outputs/skill-dst-builder.md`- ...

> 保存为 `outputs/skill-dst-builder.md`- ...

```markdown
Given a task-oriented dialogue system, design DST.
1. Slots to track.
2. State update method (rule, neural, LLM).
3. Confirmation and correction handling.
```

## Egzersizler.

1. **Easy.**Restoran rezervasyonu için kurallara dayalı bir DST oluşturun. / **简单。**Çevreye yapılan düzenlemeler için düzenlemeler yapılır.
2. **Medium.**LLM tabanlı devlet çıkarımı ekleyin. Kurallara dayalı karşılaştırın. / **中等。**添加基于LLM的状态提取──
3. **Hard.**MultiWOZ'da DST değerlendirme yapın. Ortak hedef doğruluğunu bildirin. / **困难。**Bu yüzden, çok sayıda kişiye karşı bir tutum geliştirmek için çok şey yapıyoruz.

## Anahtar Şartlar .

| Term / 术语 | What it means / 含义 |
|------|-----------------------|
| Dialogue state（对话状态） | Current (slot, value) pairs. / 当前槽位-值对。 |
| Slot filling（槽位填充） | Extracting values for predefined slots. / 为预定义槽位提取值。 |
| Belief state（信念状态） | Probability distribution over slot values. / 槽位值的概率分布。 |
| MultiWOZ | Multi-domain dialogue dataset. / 多领域对话数据集。 |

## Daha fazla okumak

- [MultiWOZ](https://arxiv.org/abs/1810.00278) standart DST veri kümesi. / 标准 DST 数据集。
- [TRADE](https://arxiv.org/abs/1810.00278) aktarılabilir iletişim durum takipçisi. / 可迁移对话状态跟踪器──
- [SimpleTOD](https://arxiv.org/abs/2005.00796) basit uçtan son DST. / 简单端到端 DST──
