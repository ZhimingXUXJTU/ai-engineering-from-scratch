# Doğal Dil İfade  Metin Değişimi  Doğal Dil İfade  文本含

> "t h içerir" anlamı, t'nin insan okuma sonucu olarak h doğru olduğu anlamına gelir. NLI, içerme / çelişki / tarafsızlık öngörme görevi.
> "t 含 h" anlamı insan okuyucularının sonucu h 为真──NLI is预测含/矛盾/中性的任务──表面无聊,生产中承重──

> **【中文解读】**NLI 判断两个句子之间逻辑关系:含、矛盾、中性──

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 05 (Sentiment Analysis), Phase 5 · 10 (Attention) | **前置知识:** Phase 5 · 05（情感分析），Phase 5 · 10（注意力机制）
**Time:** ~45 minutes | **时间:** ~45 分钟

## Sorunlar. Sorunlar.

Bir chatbot oluşturdun. "Evet" cevabını verdi. "Evet"in kanıtlarla desteklendiğini nereden biliyorsun? 10.000 haber makalesini konuya göre sınıflandırmalısın. 50 etiketli örneğin var. NLI'ye dönüştürüyorsun: "bu makale {topik}"  bağlantı veya çelişki hakkında? Yaratılan bir özetin kaynağa sadık olup olmadığını kontrol etmelisin.

> Bu makaleyi NLI'ye çevirmek için "Bu makale {topik} hakkında mı yoksa çelişki içerir mi?

> **【中文解读】**Bu bölümde sorulan soru şu: Bu tekniği pratik projede nasıl doğru bir şekilde anlayabilir ve uygulayabilirsiniz.

Bu üç sorun da doğal dil çıkarımına dönüşür. NLI, gerçek kontrolünü, sıfır atış sınıflandırmasını, özetleme değerlendirilmesini ve geri alma doğrulamalarını destekleyen omurgası görevidir.

> Bu üç sorun doğal dil düşüncesine dayanır. NLI, temel görevleri olan gerçek inceleme, sıfır örnek sınıflandırma, özet değerlendirmesi ve inceleme çalışmalarıdır.

## Konsepten bir şey.

> **【中文解读】**Bu bölümde temel kavramlar ve teoriler hakkında konuşuluyor. Bu kavramları öğrenmek, sonradan gerçekleştirilme önemi, aynı zamanda, görüşmeler ve mühendislik uygulamalarında yüksek sıklıkta yapılan incelemelerin bilgi noktasıdır.

**The task.**Önbellek verildiğinde `t`ve hipotezi.`h`, ilişkilerini şu türlerden biri olarak sınıflandırır: Etkinlik (t h anlamına gelir), Çelişki (t h'ye çelişki gösterir), Tarafsız (hem de değildir).

> **任务。**给定前提 `t`和假设 `h`,将它们的关系分类为: 含含含 h) 矛盾矛盾t 矛盾 h) 、中性都不是) ∼三分类

**Cross-encoder approach.**T ve h'yi bir transformatörle besleyip sınıflandırır.

> **交叉编码器方法。**拼接 t 和 h,通过 Transformer,分类──用于准确率关键的应用──慢因为每对运行完整模型──

**Bi-encoder approach.**T ve h'yi ayrı ayrı kodlayın, yerleşimleri (kozin benzerliği) karşılaştırın.

> **双编码器方法。**分别编码 t 和 h,比较嵌入 (余弦相似度) ⋅检索快但不太准确──

> **【拓展：大语言模型的工程实践】**GPT'den ChatGPT'e kadar, NLP alanında "her görev bir model eğitimi" ile "her görevyi çözmek için bir model" biçiminin değişiminden geçti.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) şu anki işletme AI 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用  应用 应用 应用    应用     应用   应用        应用    应用       应用          应用        应用      应用          应用                                                                                                       
```figure
nli-router
```

## Yapın

> **【拓展：NLP 的多语言挑战】**Küresel olarak 7000'den fazla dil vardır, ancak NLP çalışmaları çoğunlukla İngilizce ve az sayıda dil üzerinde yoğunlaşmaktadır.

## Yapın.

> **【中文解读】**Bu bölüm kodla sıfırdan gerçekleştirilen çekirdek algoritmasıdır. Bu "sıfırdan" yöntem çerçevenin arkasındaki prensipleri anlama yardımcı olur.

### Adım 1: NLI üzerinden sıfır atış sınıflandırması

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

tok = AutoTokenizer.from_pretrained("roberta-large-mnli")
model = AutoModelForSequenceClassification.from_pretrained("roberta-large-mnli")

def nli_classify(premise, hypothesis):
    inputs = tok(premise, hypothesis, return_tensors="pt", truncation=True)
    with torch.no_grad():
        logits = model(**inputs).logits[0]
    # 0=contradiction, 1=neutral, 2=entailment
    probs = torch.softmax(logits, dim=-1)
    labels = ["contradiction", "neutral", "entailment"]
    return {labels[i]: probs[i].item() for i in range(3)}

print(nli_classify("A man is playing guitar.", "Someone is making music."))
```

> **【中文解读】**Bu bölüm, bu teknolojiyi nasıl hızlı bir şekilde uygulayacağımızı gösterir.

> **【拓展：Prompt Engineering 与 LLM 应用】**Hızlı Mühendislik NLP mühendislerinin temel beceri haline geldi. Zero-shot'tan birkaç-shot'a, Chain-of-Thought'tan ReAct'e kadar, farklı fikir stratejileri farklı durumlarda uygulanmaktadır.

## Çerçeveyi kullanın.

> **【中文解读】**Bu bölümde modellerin kullanılabilir ürünler için nasıl dağıtılacağı üzerinde yoğunlaşmaktadır.

Üretim NLI yığın:

> 生产 NLP 技术:

- **Zero-shot classification:**NLI modelleri (DeBERTa-v3-large-mnli). / 零样本分类:NLI 模型。
- **Fact verification:**İddia karşıtı kanıtlar üzerine çapraz kodlayıcı NLI. / 事实验证:交叉编码器 NLI。
- **Summary faithfulness:**Her özet cümlesini kaynağa göre kontrol edin. / 摘要忠实度:检查每个摘要句子与源。
- **RAG grounding:**Çıkarılan bağlamı doğrulayın cevabı destekler. / RAG 定:验证检索上下文支持答案──

## İndirin . Ürünler .

- Kaydet .`outputs/skill-nli-applications.md`- ...

> 保存为 `outputs/skill-nli-applications.md`- ...

```markdown
Given a production need (fact-checking, zero-shot classification, summary evaluation), design the NLI pipeline.
1. Model choice. Cross-encoder (accuracy) or bi-encoder (speed).
2. Input format. Premise-hypothesis pairs.
3. Evaluation. Accuracy on labeled NLI datasets.
```

> **【中文解读】**练习题按照易/中级/难三度递进;;建议至少完成中级题;;

## Egzersizler.

1. **Easy.**Kullanım`roberta-large-mnli`20 cümle ile sıfır atışlı konu sınıflandırması için. / **简单。**Kullanım`roberta-large-mnli`20 cümle için yapım biçimleri
2. **Medium.**NLI kullanarak bir özet sadakat kontrolörü oluşturun. CNN/DailyMail'de değerlendirin. / **中等。**NLI'yi kullanmak için bir fidyelik kontrol cihazı oluşturmak için.
3. **Hard.**RAG yanıt doğrulama için çapraz kodlayıcı ile iki kodlayıcı NLI karşılaştırın.**困难。**Raporlama hızı ve doğruluk oranı ağırlığı için RAG                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               

## Anahtar Şartlar .

| Term / 术语 | What people say / 人们常说的 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| NLI（自然语言推理） | Entailment task / 蕴含任务 | Classify premise-hypothesis pairs as entailment/contradiction/neutral. / 将前提-假设对分类为蕴含/矛盾/中性。 |
| Cross-encoder（交叉编码器） | Joint encoding / 联合编码 | Encode both texts together through the full model. / 通过完整模型联合编码两个文本。 |
| Bi-encoder（双编码器） | Separate encoding / 分离编码 | Encode each text independently, compare embeddings. / 独立编码每个文本，比较嵌入。 |

## Daha fazla okumak

- [Bowman et al. (2015). SNLI](https://nlp.stanford.edu/pubs/snli_paper.pdf)Stanford NLI veri kümesi.
- [He et al. (2021). DeBERTa v3](https://arxiv.org/abs/2111.09543) En son NLI modeli. / 先进 NLI 模型。
