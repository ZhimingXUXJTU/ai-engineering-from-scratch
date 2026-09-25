# Uzun bağlam değerlendirmesi  NIAH, RULER, LongBench, MRCR 长上下文评估  NIAH、RULER

> Gemini 3 Pro 10M bağlamlı token reklam eder. 1M tokenlerde, 8 iğne MRCR 26,3%'e düşer. Reklamlanmış ≠ kullanılabilir. Uzun bağlam değerlendirmesi gönderdiğiniz modelin gerçek kapasitesini söyler.
> Gemini 3 Pro 宣称10M token 上下文──在1M token 时,8-针 MRCR 降至26.3%──宣称的 ≠可用──长上下文评估告诉你你正在部署的模型的实际能力──

> **【中文解读】**评估 LLM 在长上下文窗户中的实际表现──

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 27 (LLM Evaluation) | **前置知识:** Phase 5 · 27（LLM 评估）
**Time:** ~45 minutes | **时间:** ~45 分钟

## Sorunlar. Sorunlar.

Bu 2026 bağlam-yetenek boşluğu. Özellik sayfaları 1M jeton diyor. Benchmarks diyor: 100K jetonlarda, geri alma doğruluğu 15-40% düşüyor. 500K'da, 40-70% düşüyor.

> Bu 2026 yılındaki üst aşağı yazılım kapasitesi farkıdır. 1M tokenı belirtiyor.

> **【中文解读】**Bu bölümde sorulan soru şu: Bu tekniği nasıl gerçek tasarımda doğru şekilde anlayabilir ve uygulayabilirsiniz.

Uzun bağlam değerlendirme bu ekseleri ölçer: çeşitli derinliklerde çekim doğruluğu, belgeler arasında çoktan akıl yürütme ve dağıtılan bilgi üzerinde toplama.

> 长上下文评估测量这些轴:各种深度检查准确率,跨文档多跳推理以及分布信息聚合物――

## Konsepten bir şey.

> **【中文解读】**本節介绍核心概念和理论基础──

**NIAH (Needle in a Haystack).**Bir uzun belgeye belirli bir gerçek yerleştirin. Modelin onu almak için isteyin. Ölçümler: model Y-token çiy yığınında derinlikteki bir iğne bulabilir mi?

> **NIAH（大海捞针）。**Yapılan bir analiz için, Y simgesinin çimenli bir çimenli bir çimenle ilgili bir araştırma yapın.

**RULER.**NIAH'yi çok iğneli, değişken mesafeli ve toplama görevleriyle genişletiyor.

> **RULER。**扩展 NIAH 添加多针、可变距离和聚合任务──更全面──

**LongBench.**Gerçek dünyadaki uzun bağlamlı görevler: özetleme, sorgulama, çekim, kod.

> **LongBench。**Gerçekte, bu konuyu daha fazla bilgi için ele alalım.

**MRCR (Multi-hop Reasoning over Context).**Bu mantık çok sayıda belge arasında bilgi bağlamasını gerektirir.

> **MRCR（上下文多跳推理）。**需要跨多文档连接信息的推理──最难的长上下文测试──

> **【拓展：大语言模型的工程实践】**GPT'den ChatGPT'ye kadar, NLP'de değişim biçimi yaşandı.
```figure
gx-niah-decay
```

## Yapın

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG)   检索增强生成 (RAG)  RAG)   检索增强生成 (RAG) 检索增强生成 (RAG) 检索增强生成 (RAG) RAG) 检索增强生成 (RAG) 检索增强生成 (RAG) 检索增强生成 (RAG) 检索增强生成 (RAG) 检索增强生成 (RAG) 检索增强生成 (RAG) 检索增强生成) 检索增强生成 (RAG) 检索增强生成 (RAG) 检测增强生成) 检测增强生成 (RAG) 检测增强生成) 检测增强的架构 (RAG) 检测) 检测增强的架构

> **【拓展：NLP 的多语言挑战】**Dünya çapında 7000'den fazla dil vardır, ancak NLP çalışmaları çoğunlukla İngilizce ve birkaç dil üzerinde yoğunlaşmaktadır.

## Yapın.

> **【中文解读】**Bu bölüm kodla birlikte, çekirdek algoritmasını da tamamlıyor.

### Adım 1: Basit NIAH testi

```python
def needle_in_haystack(model, context_length, needle, needle_position):
    """Insert needle at position in a long document and test retrieval."""
    haystack = generate_irrelevant_text(context_length)
    full_text = haystack[:needle_position] + f"\n{needle}\n" + haystack[needle_position:]
    question = f"What is the secret fact hidden in the text?"
    response = model(full_text + "\n\n" + question)
    return needle.lower() in response.lower()
```

> **【中文解读】**Bu bölüm, bu teknolojiyi nasıl hızlı bir şekilde uygulayacağımızı gösterir.

> **【拓展：Prompt Engineering 与 LLM 应用】**Hızlı Mühendislik NLP mühendislerinin temel beceri haline geldi.

## Çerçeveyi kullanın.

> **【中文解读】**Bu bölümde modellerin kullanılabilir ürünler için nasıl deploye edileceği üzerinde yoğunlaşmaktadır.

| Benchmark / 基准 | Type / 类型 | Measures / 测量 |
|---------|------|---------|
| NIAH | Synthetic / 合成 | Single-fact retrieval at depth. / 深度单事实检索。 |
| RULER | Synthetic / 合成 | Multi-needle + aggregation. / 多针 + 聚合。 |
| LongBench | Real / 真实 | Practical long-context tasks. / 实用长上下文任务。 |
| MRCR | Synthetic / 合成 | Multi-hop reasoning. / 多跳推理。 |

## İndirin . Ürünler .

- Kaydet .`outputs/skill-long-context-eval.md`- ...

> 保存为 `outputs/skill-long-context-eval.md`- ...

```markdown
Given a model claiming long-context support, verify actual performance.
1. Context length to test.
2. Benchmarks to run (NIAH, RULER, LongBench).
3. Minimum acceptable accuracy at target length.
```

## Egzersizler.

1. **Easy.**NIAH'i 10K ve 50K tokenlerle çalıştır.**简单。**10K ve 50K token'ı kullanıyorum.
2. **Medium.**Çoklu iğneli bir test yapın. 100K bağlamında 5 gerçekin alınmasını ölçün. / **中等。**构建多针测试──
3. **Hard.**LongBench'de 3 model karşılaştırın.**困难。**LongBench'e göre, bu bir model.

## Anahtar Şartlar .

| Term / 术语 | What it means / 含义 |
|------|-----------------------|
| NIAH（大海捞针） | Insert fact in long text, test retrieval. / 在长文本中插入事实，测试检索。 |
| Context window（上下文窗口） | Maximum input length a model can process. / 模型能处理的最大输入长度。 |
| Multi-hop reasoning（多跳推理） | Connect info across multiple documents. / 跨文档连接信息。 |

## Daha fazla okumak

- [NIAH original](https://arxiv.org/abs/2404.05460)Haystağındaki İğne.
- [RULER](https://arxiv.org/abs/2404.02372) genişletilmiş uzun bağlamlı referans. / 扩展长上下文基准。
- [LongBench](https://arxiv.org/abs/2308.14508) gerçek dünya uzun bağlamlı görevler. / 真实长上下文任务。
