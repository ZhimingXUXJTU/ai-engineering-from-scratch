# Kırmızı Takım Araçları  Garak, Llama Gardiyan, Pyrit  Llama Gardiyan 工具 Garak Pyrit

> 2026'da üç üretim aracı kırmızı takım yığınına çerçeveye girer. Llama Guard (Meta)  Llama-3.1-8B sınıflandırıcısı, 14 MLCommons tehlike kategorisi üzerinde ince ayarlanmıştır; 2025 Llama Guard 4 Llama 4 Scout'tan kesilmiş bir 12B doğuştan multimodal sınıflandırıcıdır. Garak (NVIDIA)  Halüsinasyon, veri sızıntısı, hızlı enjeksiyon, toksisite ve jailbreaks için statik, dinamik ve uyarlayıcı araştırmalarla açık kaynaklı LLM hassaslık tarayıcısı. PyRIT (Microsoft)  Crescendo, TAP ve derin sömürü için özel dönüştürücü zincirleri ile çok yönlü kırmızı takım kampanyaları. Llama Guard 3 Meta'nın "Llama 3 Herd of Models" (arXiv:2407.21783); Llama Guard 3-1B-INT4 arXiv:2411.17713; Garak'ın github.com/NVIDIA/garak'daki sondarchitektüründe belgelendirilir. Bu araçlar, 2026 yılındaki kırmızı ekip araştırmaları (Deneyim 12-15), ve dağıtım (Deneyim 17+) arasındaki üretim arayüzüdür.

> **【中文解读】**Bu bölüm, Red Team Testing  Sistemleşmiş güvenlik değerlendirme yöntemi, otomatik saldırı kullanarak AI  sistem hatalarını keşfetmek için üç üretim aracı tanımladı 2026 yıl  Red Team Teknolojisi :Llama Guard  Meta) Llama-3.1-8B 分类器微调到14  MLCommons 危险类;Garak  NVIDIA) 开源 LLM 漏洞扫描器,含静态、动态和自适应探针;PyRIT Microsoft) 多轮红队活动,含 Crescendo、TAP 和自定义转换链;;

> **【拓展：2026 红队技术栈 → 生产配置】**标准配置:Llama Guard 放在模型两侧(输入+输出),Garak 每晚运行回归测试,PyRIT,预发布活动 हेतु उपयोग किया गया──Prompt-Guard-86M Meta'nın hafif bir sınıflı giriş sınıfı, Llama Guard ile birlikte kullanılmıştır──TrustyAI, Garak ve Llama Stack kalkanlarını 集成 olarak uçtan uçe değerlendirir──

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, tool-architecture simulator and Llama Guard-style classifier mock) | **语言:** Python（标准库，工具架构模拟器和 Llama Guard 风格分类器模拟）
**Prerequisites:** Phase 18 · 12-15 (jailbreaks and IPI) | **前置知识:** Phase 18 · 12-15 (越狱和 IPI)
**Time:** ~75 minutes | **时间:** ~75 分钟

>  **【前置】**学本节前请先掌握:Phase 18·12-15(越狱+IPI 全套) ⋅2026 红队工具三件套──
>  **【类比】**红队工具 = "AI 安全的透透测试套件"――Llama Guard(Meta) = 输入输出分类器(14 危险类别,类似Phase 15·18);Garak(NVIDIA) = 漏洞扫描器(静态+动态+自适应探针,覆盖幻觉/数据泄漏/越狱);PyRIT(Microsoft) = 多轮深度攻击编排(Crescendo/TAP/自定义链) ・・・三件套是研究(12-15) 和部署(17+) 之间的工程界面──

## Öğrenme hedefleri

- Güvenlik yığınında Llama Guard 3/4'ün konumunu açıklayın: giriş sınıflandırıcısı, çıkış sınıflandırıcısı veya her ikisi de.

> 描述 Llama Guard 3/4 在安全技术中的位置:输入分类器、输出分类器或两者兼有──

- MLCommons'un 14 tehlike kategorisini ve açık olmayan bir risk kategorisini (Kod Anlatıcısı İstifadesi) belirtin.

> 列出 14  MLCommons 危险类,并说明一个不明类 (不明类) 编码解释器滥用)

- Garak'ın sondası mimarisini anlat: sondlar, dedektörler, harneleri.

> 描述 Garak'ın探针架构:探针、检测器、线束──

- PyRIT'in çok dönüşlü kampanya yapısını ve Garak araştırmaları ile nasıl birleştirildiğini açıklayın.

> 描述 PyRIT'in多轮活动结构 ve Garak 探针组合──

## Sorun . Sorun .

Ders 12-15 saldırı yüzeyini sunar. Üretim dağıtımları tekrarlanabilir, ölçeklenebilir değerlendirme gerektirir. 2026 yılında üç araç hakim olur: Llama Guard (savunma sınıflandırıcısı), Garak (skaner), PyRIT (kampanyası orkestrasyonu). Her biri kırmızı takım yaşam döngüsünün farklı bir katmanını hedef alır.

> Ders 12-15  saldırı yüzünü gösterdi.

## Konsep kavramı.

> **【中文解读】**Llama Guard 3 is Llama-3.1-8B 模型微调到 MLCommons AILuminate 14 类别的输入/输出分类,支持 8种语言。Llama Guard 3-1B-INT4 is量化边缘变体(440MB,移动 CPU 约30 token/s)。Llama Guard 4(2025年 4月) is 12B 原生多模态分类器, Llama 4 Scout 剪枝, 8B 文本和 11B 视觉分类器,

### Llama Gardiyanı (Meta)

Llama Guard 3, MLCommons AILuminate 14 kategorisi üzerinde giriş/çıkan sınıflandırması için ince ayarlanmış Llama-3.1-8B modeli:
- Şiddetli suçlar, şiddetli olmayan suçlar, cinsel ilişki, CSAM, hakaret
- Uzman tavsiye, gizlilik, IP, ayrımcılıktan uzak silahlar, nefret
- İntihar/kendine zarar vermek, cinsel içerik, seçimler, kod yorumcularının kötüye kullanımı

> Llama Guard 3 Llama-3.1-8B 模型, MLCommons AILuminate için 14 个类别进行输入/输出分类微调――支持 8种语言――

8 dil destekler. Kullanım: LLM'den önce (girin moderasyonu), LLM'den sonra (çıkan moderasyonu) veya her ikisinden sonra yerleştir.

> kullanma biçimi: LLM 之前(输入审核) 之后(输出审核) 或两者兼有──Llama Guard 3 作为单一模型处理两者──

Llama Guard 3-1B-INT4 (arXiv:2411.17713, 440MB, mobil CPU'da ~ 30 token/s) kuantüze edge varianıdır.

> Llama Guard 3-1B-INT4 ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅                                                                                                                                                                                                                                                               

Llama Guard 4 (April 2025) 12B, doğuştan multimodal, Llama 4 Scout'tan kesilmiştir.

> Llama Gardiyası 4(2025 yıl 4 月) 12B orijinal model biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biçim biç

> **【拓展：Garak 架构 → 探针/检测器/线束】**Garak'ın üç katlı yapı: kontrol cihazı: kontrol cihazı: kontrol cihazı: kontrol cihazı: kontrol cihazı: kontrol cihazı: kontrol cihazı: kontrol cihazı: kontrol cihazı: kontrol cihazı: kontrol cihazı: kontrol cihazı: kontrol cihazı: kontrol cihazı: kontrol cihazı: kontrol cihazı: kontrol cihazı: kontrol cihazı: kontrol cihazı: kontrol cihazı: kontrol cihazı: kontrol cihazı: kontrol cihazı: kontrol cihazı: kontrol cihazı: kontrol cihazı: kontrol cihazı: kontrol cihazı: kontrol cihazı: kontrol cihazı: kontrol cihazı: kontrol cihazı: kontrol cihazı: kontrol cihazı: kontrol cihazı: kontrol cihazı: kontrol cihazı: kontrol cihazı: kontrol cihazı: kontrol cihazı: kontrol cihazı: kontrol cihazı: kontrol cihazı: kontrol cihazı: kontrol cihazı: kontrol cihazı: kontrol cihazı: kontrol cihazı: kontrol cihazı: kontrol cihazı: kontrol cihazı: kontrol cihazı: kontrol cihazı: kontrol cihazı: kontrol cihazı: kontrol cihazı: kontrol cihazı: kontrol cihazı: kontrol cihazı: kontrol cihazı: kontrol cihazı: kontrol cihazı: kontrol eden kişi: kontrol eden kişi: kontrol eden kişi: kontrol eden kişi: kontrol eden kişi: kontrol eden kişi: kontrol eden kişi:

### Garak (NVIDIA)

Açık kaynaklı güvenlik açığı tarayıcısı.
- **Probes.**Halüsinasyon, veri sızması, hızlı enjeksiyon, toksisite, jailbreak için saldırı jeneratörleri.
- **Detectors.**Beklenen başarısızlık modlarına karşı puanlama sonuçları  toksik, sızmış, hapsedilmiş.
- **Harnesses.**Sonda-detektor çiftlerini yönet, kampanyalar yürüt, raporlar oluştur.

> 开源漏洞扫描器.架构:探针(幻觉、数据泄露、提示注入、毒性、越狱的攻击生成器) 检测器 (Anadolu Başarısızlık Mode评分输出) 线束(管理探针-检测器对,运行活动,生成报告)

TrustyAI, Garak'ı Llama-Stack kalkanlarıyla (Prompt-Guard-86M giriş sınıflandırıcısı, Llama-Guard-3-8B çıkış sınıflandırıcısı) en-to-end kalkanlı hedef değerlendirmesi için entegre eder. Dönem tabanlı puanlama (TBSA) ikili geçiş / başarısızlığı değiştirir.

> TrustyAI Garak ve Llama Stack kalkanlarını 集ım sonucu sonucu değerlendirecek.

### PyRIT (Microsoft)

Python Risk Identification Toolkit. Çok yönlü kırmızı takım kampanyaları.
- **Converters.**Bir tohum sorguyu dönüştürün  parafrase, kodlama, çevirme, rol oynatma.
- **Orchestrators.**Kampanyayı yürüt: Crescendo (eskalasiyon), TAP (branching), RedTeaming (sözlü döngü).
- **Scoring.**Yargıç olarak veya yargıç olarak sınıflandırıcı olarak.

> PyRIT Python 风险识别工具包──多轮红队活动──核心组件:转换器:转换种子提示) 编排器:运行活动: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分: 评分:                                                                                                                                                                                                                                                                 

PyRIT, Garak'ın ağır kuzeni. Garak binlerce tek dönüşlü sondayı yürütür; PyRIT, belirli başarısızlık modlarını kırmak için tasarlanmış derin çok dönüşlü kampanyaları yürütür.

> PyRIT Garak'ın ağırlık seviyesindeki bir göstergesidir. Garak binlerce tek turlu birer damla yürütüyor.

### - Yığın.

Llama Guard'ı modelin her iki tarafına koyun. Geri dönüş için Garak'ı gece çalıştırın. Ön yayın kampanyaları için PyRIT çalıştırın. Bu 2026'da çoğu üretim dağıtımında varsayılan yapılandırma.

> Modelin iki tarafında Llama Guard yerleştirilmiştir. Garak dönüş testleri için her gece çalışmaktadır.

> **【中文解读】**评估陷:评判身份 tüm üç araç, LLM 评判,评判校准驱动报告的ASR (ASR) ), belirlenmesi gereken 评判;探针过时Garak 探针随着模型修复和老化,自适应探针 (PAIR) 静态探针老化较慢;Llama Guard 在良性内容上的误报率早期版本过标政治和LGBTQ+ 内容,v3/v4 校准有改善但未部署校准;;

### Değerlendirme tuzağı

- **Judge identity.**Üç alet de bir LLM yargıçı kullanabilir; yargıç kalibrasyon sürücüleri ASR'leri (Denevi 12) rapor etti.
- **Probe staleness.**Garak araştırmacıları modellerin karşısında yapıştırıldığında yaşlanır. Adaptif araştırmacılar (PAIR şeklinde) statik araştırmacılardan daha yavaş yaşlanır.
- **Llama Guard FPR on benign content.**Erken Llama Guard sürümleri, aşırı derecede politik ve LGBTQ+ içeriği vardı; Llama Guard 3/4 kalibrasyonları geliştirildi ancak dağıtım başına kalibrlenmedi.

### Bu 18 fazaya uygun.

Ders 12-15 saldırı aileleri. Ders 16 üretim araçları. Ders 17 (WMDP) çift kullanım kabiliyetinin değerlendirilmesidir. Ders 18 bu araçları bir politika yapısına sarılan sınır güvenlik çerçeveleri.

> Ders 12-15 saldırı ailesidir. Ders 16 üretim araçlarıdır. Ders 17 ikili kullanım kabiliyetinin değerlendirilmesidir. Ders 18 bu araçları politika yapısında ön kenar güvenlik çerçevesinde paketlemektedir.

> **【拓展：PyRIT → 多轮深度利用】**PyRIT (Microsoft) Garak'ın ağırlıklı bir performans göstermektedir. Garak binlerce tek döngülik birer çubuk yürütüyor.

## Kullanın Kullanın
```figure
al-guard-stack
```

## Kullan

`code/main.py`Oyuncak bir Llama Guard tarzı sınıflandırıcı ( anahtar kelime + 14 kategoride semantik özellikler), oyuncak bir Garak harnes (sonde-detektor döngüsü) ve PyRIT tarzı çok dönüştürücü zincir inşa eder.

> `code/main.py` Oyuncaklar Llama Guard 风格分类器、 oyuncaklar Garak 线束和 PyRIT 风格多轮转换链──

## Gönderin.

Bu ders bize çok yararlı .`outputs/skill-red-team-stack.md`- Uygulama tanımını göz önünde bulundurarak, üç araçtan hangisinin uygun olduğunu, her birinde neyi yapılandırması ve hangi gerileme kadenci çalıştırılması gerektiğini belirler.

> 本课产 出 `outputs/skill-red-team-stack.md` Verilmiş bir görevli olarak, üç araçtan hangisinin uygun olduğunu, her birinin nasıl ve nasıl bir şekilde geri dönüşeceğini tanımlamak.

## Egzersizler.

1. Çık .`code/main.py`Llama-Guard tarzı sınıflandırıcısının tek dönüşlü ve çok dönüşlü saldırılarda algılama oranını karşılaştırın.

2. Yeni bir Garak sondeyi uygulayın: base64 kodlanmış zararlı bir taleb.

3. PyRIT tarzı dönüştürücü zincirini "Fransızca çevir, sonra parafrase" dönüştürücü ile uzatın.

4. Llama Guard 3'ün tehlike kategorileri listesini okuyun. Eğitim verilerinin gerçekçi bir şekilde yasal geliştiriciler içerikleri üzerinde yüksek yanlış pozitif oranlar ürettiği iki kategorinin belirlenmesi.

5. Garak ve PyRIT'in tasarım ilkelerini karşılaştırın.

## Anahtar Terimler

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| Llama Guard | "the classifier" | Fine-tuned Llama-3.1-8B/4-12B safety classifier with 14 hazard categories |
| Garak | "the scanner" | NVIDIA open-source vulnerability scanner; probes, detectors, harnesses |
| PyRIT | "the campaign tool" | Microsoft multi-turn red-team orchestrator; converters, orchestrators, scoring |
| Prompt-Guard | "the small classifier" | Meta's 86M prompt-injection classifier, paired with Llama Guard |
| TBSA | "tier-based scoring" | Garak's tier-based pass/fail replacing binary outcomes |
| Converter chain | "paraphrase + encode + ..." | PyRIT composition primitive for building multi-step attacks |
| MLCommons hazard categories | "the 14 taxonomies" | Industry-standard taxonomy Llama Guard targets |

## Daha fazla okumak

- [Meta — Llama Guard 3 (in Llama 3 Herd paper, arXiv:2407.21783)](https://arxiv.org/abs/2407.21783) 8B sınıflandırıcısı
- [Meta — Llama Guard 3-1B-INT4 (arXiv:2411.17713)](https://arxiv.org/abs/2411.17713) Kvantistik mobil sınıflandırıcı
- [NVIDIA Garak — GitHub](https://github.com/NVIDIA/garak) tarayıcı repo ve belgeleri
- [Microsoft PyRIT — GitHub](https://github.com/Azure/PyRIT) kampanya araçları
