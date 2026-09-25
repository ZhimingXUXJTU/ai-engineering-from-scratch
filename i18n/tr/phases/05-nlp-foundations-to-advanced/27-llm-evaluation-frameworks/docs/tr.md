# LLM Değerlendirme  RAGAS, DeepEval, G-Eval  LLM  değerlendirme  RAGAS  DeepEval

> Tam eşleşme ve F1 semantik eşdeğerliği eksik. İnsan inceleme ölçeklenmez. LLM-as-judge, sayıya güvenmek için yeterli kalibrasyonla  üretim cevabıdır.
> 精确匹配和 F1 捕捉不到语义等价──人工审查不可扩展──LLM 作为评审是生产答案经过足够的校准可以信任这个数字──

> **【中文解读】**评估 LLM 生成质量, RAG 效果, RAGAS, DeepEval, G-Eval,

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 23 (Chunking), Phase 5 · 14 (IR & Search) | **前置知识:** Phase 5 · 23（分块），Phase 5 · 14（信息检索）
**Time:** ~60 minutes | **时间:** ~60 分钟

## Sorunlar. Sorunlar.

RAG sisteminiz cevap verir: "29 Haziran 2007". İpucu cevabı şöyle diyor: "29 Haziran 2007". Tam eşleşme yanlış diyor. BLEU kısmi diyor. Bir insan doğru diyor. İnsanlarla uyumlu bir ölçümün olması gerekir, binlerce çıkışa kadar ölçebilir ve insan notlarından daha az maliyetlidir.

> Senin RAG 系统 cevap:"29 Haziran 2007"."" 参考答案是:"29 Haziran 2007。" 精确匹配说错了。BLEU 说部分对──人类说正确──你需要一个与人类一致的量度,可扩展到数千输出,且成本低于人工标签──

> **【中文解读】**Bu bölümde sorulan soru şu: Bu tekniği nasıl gerçek tasarımda doğru şekilde anlayabilir ve uygulayabilirsiniz.

Şimdi 10.000 test vakaları ile çarpın. Göndermek istediğiniz her model güncelleme ile tekrar çarpın. İnsan değerlendirme ölçeklenmez. R ≥ 0.85'te insan yargısına ilişkin otomatik ölçümlere ihtiyacınız var.

> Şimdi 10.000 test kullanımı örneği ile tekrar tekrar, yayınlamak istediğiniz her modelde yenilik yapın. Yapay değerlendirme genişletmez.

## Konsepten bir şey.

> **【中文解读】**本節介绍核心概念和理论基础──

2026'da bu sorunun üç çerçevesine sahip.

> 2026 yılında bu sorunu yönlendirecek üç çerçeve vardır.

**RAGAS.**RAG Değerlendirme. Geri alınma + jenerasyonı birlikte değerlendirir. Ölçümler: sadakat, cevapların uygunluğu, bağlam doğruluğu, bağlam geri çağırma. RAG değerlendirme standardı.

> **RAGAS。**RAG 評価──联合评估检索和生成──指标:忠诚度、答案相关性、上下文精确率、上下文召回率──RAG 评估标准──

**DeepEval.**LLM sonuçları için birim testi çerçevesine.

> **DeepEval。**LLM 输出单元测试框架──标志:答案相关性、忠诚度、偏见、毒性──与 pytest 集成──
```figure
n5-judge-gauge
```

## Yapın

**G-Eval.**Düşünce zinciri değerlendirme kriterleri oluşturmak için uyarıyor, sonra sonuçları puanlamak için. Araştırma derecesi. İnsan yargısına en yüksek korelasyon.

> **G-Eval。**Düşünce ve öneriler ile değerlendirme standartları oluşturmak, sonra değerlendirmeler çıkarmak.

> **【拓展：大语言模型的工程实践】**GPT'den ChatGPT'ye kadar, NLP'de değişim biçimi yaşandı.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG)   检索增强生成 (RAG)  RAG)   检索增强生成 (RAG) 检索增强生成 (RAG) 检索增强生成 (RAG) RAG) 检索增强生成 (RAG) 检索增强生成 (RAG) 检索增强生成 (RAG) 检索增强生成 (RAG) 检索增强生成 (RAG) 检索增强生成 (RAG) 检索增强生成) 检索增强生成 (RAG) 检索增强生成 (RAG) 检测增强生成) 检测增强生成 (RAG) 检测增强生成) 检测增强的架构 (RAG) 检测) 检测增强的架构

> **【拓展：NLP 的多语言挑战】**Dünya çapında 7000'den fazla dil vardır, ancak NLP çalışmaları çoğunlukla İngilizce ve birkaç dil üzerinde yoğunlaşmaktadır.

## Yapın.

> **【中文解读】**Bu bölüm kodla birlikte, çekirdek algoritmasını da tamamlıyor.

```python
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision

# Evaluate RAG pipeline
results = evaluate(
    dataset=rag_dataset,
    metrics=[faithfulness, answer_relevancy, context_precision],
    llm=judge_llm,
    embeddings=embed_model,
)
print(results)
```

```python
from deepeval import assert_test
from deepeval.metrics import FaithfulnessMetric

metric = FaithfulnessMetric(threshold=0.7, model="gpt-4")
assert_test(test_case, [metric])
```

> **【中文解读】**Bu bölüm, bu teknolojiyi nasıl hızlı bir şekilde uygulayacağımızı gösterir.

> **【拓展：Prompt Engineering 与 LLM 应用】**Hızlı Mühendislik NLP mühendislerinin temel beceri haline geldi.

## Çerçeveyi kullanın.

> **【中文解读】**Bu bölümde modellerin kullanılabilir ürünler için nasıl deploye edileceği üzerinde yoğunlaşmaktadır.

| Framework / 框架 | Focus / 重点 | Best for / 最适合 |
|---------|--------|---------|
| RAGAS | RAG evaluation / RAG 评估 | Retrieval + generation / 检索 + 生成 |
| DeepEval | Unit testing / 单元测试 | CI/CD integration / CI/CD 集成 |
| G-Eval | Research / 研究 | Custom metrics / 自定义指标 |

## İndirin . Ürünler .

- Kaydet .`outputs/skill-llm-eval.md`- ...

> 保存为 `outputs/skill-llm-eval.md`- ...

```markdown
Given an LLM application (chatbot, RAG, agent), design evaluation pipeline.
1. Framework (RAGAS, DeepEval, G-Eval).
2. Metrics to track.
3. Calibration against human labels.
```

## Egzersizler.

1. **Easy.**RAGAS ile basit bir RAG boru hattını değerlendir. / **简单。**RAGAS kullanın 评估简单 RAG 流水线──
2. **Medium.**Bir chatbot için DeepEval test süiti yapın.**中等。**Çatacaklar için DeepEval'i oluşturmak için test süsü­tü­
3. **Hard.**200 insan etiketi ile yargıç olarak LLM'yi kalibre et.**困难。**200 个人类标签校准 LLM 评审――报告相关性――

## Anahtar Şartlar .

| Term / 术语 | What it means / 含义 |
|------|-----------------------|
| RAGAS | RAG evaluation framework. / RAG 评估框架。 |
| Faithfulness（忠实度） | Answer is supported by context. / 答案有上下文支持。 |
| LLM-as-judge | LLM evaluates other LLM outputs. / LLM 评估其他 LLM 输出。 |

## Daha fazla okumak

- [RAGAS](https://docs.ragas.io/) RAG değerlendirme çerçevesini. / RAG 评估框架──
- [DeepEval](https://docs.confident-ai.com/) LLM birim testi. / LLM 单元测试。
- [G-Eval](https://arxiv.org/abs/2303.16634) düşünce zinciri değerlendirme. / 思维链评估。
