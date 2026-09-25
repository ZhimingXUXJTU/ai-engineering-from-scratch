# Yapılandırılmış Çıktımlar ve kısıtlı çözme

> JSON için LLM'den isteyin. Çoğu zaman JSON alın. Üretimde, "çoğu" sorundur. Sınırlama yapmadan önce logitleri düzenleyerek kısıtlı dekodlama "çoğu"yı "her zaman"a dönüştürür.
> 让LLM 输出 JSON──大多数时候能得到 JSON──在生产中,"大多数"就是问题──约束解码通过在采样前编辑逻辑将"大多数" 变成"总是"──

> **【中文解读】**LLM'nin JSON、SQL gibi yapılandırılmış verileri çıkarmasını sağlayın.

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 19 (Subword Tokenization) | **前置知识:** Phase 5 · 19（子词分词）
**Time:** ~60 minutes | **时间:** ~60 分钟

## Sorunlar. Sorunlar.

Özgür form jenerasyonu bir sözleşme değildir. Bu bir öneridir. JSON için sorarsanız, bir JSON şeklinde bir dizilme alırsınız.

> Özgür biçim oluşturmak bir anlaşma değil, bir önerimdir. JSON'u istedin, bir birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle birimle yap yapma yapma yapma yapma yapma yapma yapma yapma yapma yapma yapma yapma yapma yapma yapma yapma yapma yapma yapma yapma yapma yapma yapma yapma yapma yapma yapma yapma yapma yapma yapma yapma yapma yapma yapma yapma yapma yapma yapma yapma yapma yapma yapma yapma yapma yapma yapma yapma yapma yapma yapma yapma yapma yapma yapma yapma yapma yapma yapma yapma yapma yapma yapma yapma yapma yapma yapma yapma yapma yapma yapma yapma yapma yapma yapma yap

> **【中文解读】**Bu bölümde sorulan soru şu: Bu tekniği pratik projede nasıl doğru bir şekilde anlayabilir ve uygulayabilirsiniz.

2026'da üç katman var.

> 2026 yılında üç katlı bir çözüm var.

1. **Prompting.**İyice sor. "JSON nesnesini geri getir". Zamanın %85-95'inde çalışır. Kısayol vakalarında, uzun çıkışlarda ve karşıt girişlerde başarısız olur. / **提示。**İyi iyi istek. JSON'u sadece nesneye geri göndermek için kullanılır.
2. **Constrained decoding.**Maske geçersiz bir sonraki belirti logitleri her nesil adım böylece çıkış her zaman bir şema (JSON şema, regex, bağlamsız dilbilgisi) uyar. %100 çalışır. ~ 10-30% gecikme overhead maliyetleri. / **约束解码。**Her üretim aşamasında, bir sonraki token logitinin etkinsizliğine engel olmak, çıkışı her zaman modelle uyumlu hale getirmek için %100 etkinlik gösterir.
3. **Tool/function calling.**Modelin yerel araç çağrı arayüzü üzerinden yapılandırılmış çıkış. Model bir JSON nesnesini doğrudan metin olarak değil, yayınlar. En iyi gecikme, en iyi güvenilirlik, ancak model-özel. / **工具/函数调用。**通过模型原生工具调用接口的结构化输出──最佳延迟,最佳可靠性,但模型特定──

## Konsepten bir şey.

> **【中文解读】**Bu bölümde temel kavramlar ve teoriler hakkında konuşuluyor. Bu kavramları öğrenmek, sonradan gerçekleştirilme önemi, aynı zamanda, görüşmeler ve mühendislik uygulamalarında yüksek sıklıkta yapılan incelemelerin bilgi noktasıdır.

**Logit masking.**Modeldeki tüm yenilikler, yenilikçi bir sistemle birlikte, yenilikçi bir sistemle birlikte, yenilikçi bir sistemle birlikte, yenilikçi bir sistemle birlikte, yenilikçi bir sistemle birlikte, yenilikçi bir sistemle birlikte, yenilikçi bir sistemle birlikte, yenilikçi bir sistemle birlikte, yenilikçi bir sistemle birlikte, yenilikçi bir sistemle birlikte, yenilikçi bir sistemle birlikte, yenilikçi bir sistemle birlikte, yenilikçi bir sistemle birlikte, yenilikçi bir sistemle birlikte, yenilikçi bir sistemle birlikte, yenilikçi bir sistemle birlikte, yenilikçi bir sistemle birlikte, yenilikçi bir sistemle birlikte, yenilikçi bir sistemle birlikte, yenilikçi bir sistemle birlikte, yenilikçi bir sistemle birlikte, yenilikçi bir sistemle birlikte, yenilikçi bir sistemle, yenilikçi bir sistemle, yenilikçi bir sistemle, yenilikçi bir sistemle, yenilikçi bir sistemle, yenilikçi bir sistemle, yenilikçi bir sistemle, yenilikçi bir sistemle, yenilikçi bir sistemle, yenilikçi, yenilikçi, yenilikçi, yenilikçilikçi, yenilikçilikçi, yenilikçilikçi, yenilikçilikçi, yenilikçilik, yenilik, yenilikçilik, yenilik, yenilikçilik, yenilik, yenilik, yenilik, yenilik, yenilik, yenilik, yenilik, yenilik, yenilik, yenilik, yenilik, yenilik, yenilik, yenilik, yenilik, yenilik, yenilik, yenilik, yenilik, yenilik, yenilik, yenilik, yenilik, yenilik, yenilik, yenilik, yenilik, yenilik, yenilik, yenilik, yenilik, yenilik, yenilik, yenilik, yenilik, yenilik, yenilik, yenilik, yenilik, yenilik, yenilik, yenilik, yenilik, yenilik, yenilik, yenilik, yenilik, yenilik, yenilik, yenilik, yenilik, yenilik, yenilik, yenilik, yenilik, yenilik, yenilik, yenilik, yenilik, yenilik, yenilik, yenilik, yenilik, yenilik, yenilik, yenilik, yenilik, yenilik, yenilik

> **Logit 屏蔽。**Her bir oluşturma aşamasında, model kelimeler üzerinde olasılık dağılımını oluşturur.

**JSON schema constraints.**JSON çıkışı için kısıtlama uygulanır: açılış bağlamaları kapatma bağlamalarına eşittir, anahtarlar satırlara alıntılanır, değerler açıklanan türlerine eşittir, gerekli alanlar mevcuttur, şema dışında ek alanlar yoktur. Bu bağlamsız bir dilbilgisi kısıtlamasıdır, artan-artan hesaplanır.

> **JSON 模式约束。**JSON 输出 için, 约束强制:开闭括号匹配、键是带引号字符串、值匹配声明类型、必填字段存在、无模式外额外字段──

> **【拓展：大语言模型的工程实践】**GPT'den ChatGPT'e kadar, NLP alanında "her görev bir model eğitimi" ile "her görevyi çözmek için bir model" biçiminin değişiminden geçti.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) şu anki işletme AI 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用  应用 应用 应用    应用     应用   应用        应用    应用       应用          应用        应用      应用          应用                                                                                                       

> **【拓展：NLP 的多语言挑战】**Küresel olarak 7000'den fazla dil vardır, ancak NLP çalışmaları çoğunlukla İngilizce ve az sayıda dil üzerinde yoğunlaşmaktadır.

## Yapın.
```figure
constrained-decoder
```

## Yapın

> **【中文解读】**Bu bölüm kodla sıfırdan gerçekleştirilen çekirdek algoritmasıdır. Bu "sıfırdan" yöntem çerçevenin arkasındaki prensipleri anlama yardımcı olur.

### Adım 1: Basit bir logit maskeli

```python
import json
import re


def mask_logits(logits, valid_token_ids):
    """Set invalid token logits to -inf."""
    mask = torch.full_like(logits, float('-inf'))
    mask[valid_token_ids] = logits[valid_token_ids]
    return mask
```

Temel anlayış: her aşamada, sadece bir alt set simgeler geçerlidir. Bu alt setin verimli olarak hesaplanması mühendislik zorunluluğudur.

> 核心洞察:在每步中,只有符号子集是有效的──高效计算该子集是工程挑战──

### Adım 2: JSON şemaları oluşturma sırasında onaylanmaktadır

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

### Adım 3: LM Format Enforcer kullanmak

```python
from lmformatenforcer import JsonSchemaParser, generate_enforced

parser = JsonSchemaParser(schema)
# Use with any Hugging Face model's generate method
# result = generate_enforced(model, tokenizer, parser, prompt)
```

> **【中文解读】**Bu bölüm, bu teknolojiyi nasıl hızlı bir şekilde uygulayacağımızı gösterir.

> **【拓展：Prompt Engineering 与 LLM 应用】**Hızlı Mühendislik NLP mühendislerinin temel beceri haline geldi. Zero-shot'tan birkaç-shot'a, Chain-of-Thought'tan ReAct'e kadar, farklı fikir stratejileri farklı durumlarda uygulanmaktadır.

## Çerçeveyi kullanın.

> **【中文解读】**Bu bölümde modellerin kullanılabilir ürünler için nasıl dağıtılacağı üzerinde yoğunlaşmaktadır.

2026 üretim seçenekleri:

> 2026 yılındaki üretim seçeneği:

| Approach / 方案 | Reliability / 可靠性 | Latency cost / 延迟成本 | Best for / 最适合 |
|---------|------------|-------------|---------|
| Prompting / 提示 | ~85-95% / 约 85-95% | None / 无 | Prototypes, non-critical paths / 原型、非关键路径 |
| Constrained decoding / 约束解码 | 100% / 100% | +10-30% / 加 10-30% | Production APIs / 生产 API |
| Tool calling / 工具调用 | ~99.9% / 约 99.9% | Lowest / 最低 | Model-native workflows / 模型原生工作流 |

## İndirin . Ürünler .

- Kaydet .`outputs/prompt-structured-output.md`- ...

> 保存为 `outputs/prompt-structured-output.md`- ...

```markdown
Given an LLM output that must be structured (JSON, SQL, etc.), pick the right approach and implement it.
1. Schema definition. JSON Schema, regex, or grammar.
2. Enforcement method. Prompting, constrained decoding, or tool calling.
3. Fallback plan. What happens when the output still fails validation.
```

> **【中文解读】**练习题按照易/中级/难三度递进;;建议至少完成中级题,Hard级适合深入研究或面试准备;;

## Egzersizler.

1. **Easy.**Sadece çabuk bir JSON çıkarıcı oluşturun. 100 LLM çağrısında başarıyı ölçün. / **简单。**构建纯提示的 JSON 提取器──测量100次 LLM 调用成功率──
2. **Medium.**Logit maske kullanılarak basit bir JSON şeması için kısıtlı dekodlama uygulayın. / **中等。**Logit 屏蔽为简单 JSON 模式实现约束解码.
3. **Hard.**Yükleme iş yükünü gerektiren kısıtlı çözme ile araç karşılaştırın. Gecikme, güvenilirlik ve maliyet rapor edin. / **困难。**Üretim çalışma yükü ile araç kullanımı karşılaştırmak. Rapor gecikmesi, güvenilirlik ve maliyet.

> **【中文解读】**术语表中的"İnsanların ne dediği" vs "Gerçekten ne anlama geldiği" 区分日常口语和精确技术含义──在团队协作中,统一术语定义可以避免大量沟通误解──

## Anahtar Şartlar .

| Term / 术语 | What people say / 人们常说的 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| Constrained decoding（约束解码） | Force valid output / 强制有效输出 | Mask invalid logits at each step. / 每步屏蔽无效 logits。 |
| Logit masking（Logit 屏蔽） | Block bad tokens / 阻止坏 token | Set invalid token logits to -inf before softmax. / softmax 前将无效 token logits 设为 -inf。 |
| JSON Schema | JSON validation rules / JSON 验证规则 | Declarative schema for validating JSON structure and types. / 验证 JSON 结构和类型的声明式模式。 |
| Tool calling（工具调用） | Function calling / 函数调用 | Model emits structured arguments directly via native interface. / 模型通过原生接口直接发出结构化参数。 |

> **【中文解读】**延伸阅读, derinlemesine öğrenme için yüksek kaliteli kaynaklar sağladı. Bu makaleler ve dersler, derinlemesine anlama ihtiyacı olan okuyuculara uygun olarak bu alanın klasik referanslarıdır.

## Daha fazla okumak

- [LM Format Enforcer](https://github.com/noamgat/lm-format-enforcer) üretim kısıtlı kodlama kütüphanesi. / 生产级约束解码库。
- [Outlines](https://github.com/dottxt-ai/outlines) regex/JSON/CFG ile yapılandırılmış jenerasyon. / 带 regex/JSON/CFG 的结构化生成──
- [JSON Schema specification](https://json-schema.org/)JSON doğrulama standardı.
