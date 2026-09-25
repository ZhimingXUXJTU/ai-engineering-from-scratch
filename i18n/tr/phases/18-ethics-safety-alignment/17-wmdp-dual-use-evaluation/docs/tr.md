# WMDP ve Çift Kullanımlı Yetenek Değerlendirme .

> Li et al., "WMDP Benchmark: Unlearning ile Kötü Kullanımı Ölçmek ve azaltmak" (ICML 2024, arXiv:2403.03218). Biyolojik güvenlik (1,520), siber güvenlik (2,225) ve kimya (412) alanında 4.157 çoklu seçim sorusu. Sorular, "sarı bölgede"  yakın bilgi sağlayan, çok uzmanlık alanındaki inceleme ve ITAR/EAR yasal uyumluluğu ile filtrelenir. İki amaçlı: çift kullanım kabiliyetinin vekili değerlendirilmesi ve öğrenme oranı (ekleyici RMU yöntemi genel kapasiteyi korurken WMDP performansını azaltır). 2024-2025 saha anlatısı: erken OpenAI / Anthropic 2024 değerlendirmeleri internet aramaları üzerinde " hafif bir yükseltme " rapor etti; Nisan 2025'e kadar, OpenAI'nin Hazırlık Çerçevi v2 modellerinin "biolojik tehditler yaratmak için yeni başlayanlara anlamlı bir şekilde yardımcı olma eğiliminde" olduğunu söyledi. Anthropic'in biyolojik silah edinme denemesi, ASL-3'ü dışlamak için yeterli olmayan 2.53 kat yükseltme gösterdi.

> **【中文解读】**Bu bölüm WMDP'nin ikili kullanım değerlendirmesini tanıtıyor. Bu bölümde, biyolojik, kimya, ağ güvenliği ve diğer risk alanlarında AI sistemlerinin kapasitesini ölçmek için 4,157 farklı seçenek konuları ele alınıyor.

> **【拓展：2024-2025 提升叙述 → 从"轻微"到"关键"】**Üç aşama anlatım: 2024 yılının " hafif gelişimi "  erken değerlendirme raporları modeli yeni kullanıcılara karşı sadece küçük bir avantaj sağlar; 2025 yılının 4 月  yaklaşan bir patlama  OpenAI PF v2  raporları modeli yeni kullanıcılara bilinen biyolojik tehditler yaratmalarına anlamlı bir şekilde yardımcı olacaktır; Antropik 2025 yılının biyolojik silah elde etme deneyleri  2.53  yükseldi, ASL-3 ∼ 18 ay içinde " hafif " gelişmelerinin " mümkün olabilmesi için "  mümkün olmayabilir.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, WMDP-shaped uplift evaluation harness) | **语言:** Python（标准库，WMDP 形式提升评估框架）
**Prerequisites:** Phase 18 · 16 (red-team tooling), Phase 14 (agent engineering) | **前置知识:** Phase 18 · 16 (红队工具), Phase 14 (Agent 工程)
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**Öğrenci bölümün başında:Düyüş 18·16(Red Team Tool) Düyüş 14。WMDP = Büyük ölçekli öldürücü silahlarla ilgili yetenek değerlendirmesi基准。
>  **【类比】**WMDP = "AI 武器化潜力体检"──4157 题(生物 1520+网安 2225+化学 412),"黄色区域"= 接近使能知识但非直接配方──双重用途:(1) 评估 AI 双重用途能力;(2) 遗忘基准(RMU 方法降低 WMDP 分但保通用能力)──2025 OpenAI PF v2 警告模型"在显著帮助新手制造已知生物威胁的边缘"ASL-3 触发线──

## Öğrenme hedefleri

- WMDP'nin üç alanını, soru sayısını ve "sarı bölge" filtre kriterini açıklayın.

> WMDP'nin üç alanını tanımlamak, sorular sayısı ve "sarı bölge" standartları

- RMU'yu ve WMDP'nin neden hem bir değerlendirme hem de bir öğrenme dışı bir referans değerini açıklayın.

> RMU'yu ve WMDP'nin neden değerlendirilmiş ve unutulmuş olduğu açıklanmaktadır.

- 2024-2025 yükseltme anlatımını açıklayın: " hafif yükseltme " -> "yüksek" -> "ASL-3'yi dışlamak için yetersiz".

> 描述 2024-2025 年提升叙述:"轻微提升" -> "即将突破" -> "不足以排除 ASL-3"

- Yeni başlayanların akrabaları arasındaki yüksekliği uzmanların mutlak yeteneklerinden ayırt edin.

> 区分新手对提升和专家绝对能力──

## Sorun . Sorun .

Çift kullanım kabiliyeti, her laboratuvarın sınır güvenlik çerçevesinde ölçüm sorunu (Denevi 18) Soru: Model X, yeni başlayanın biyolojik, kimyasal veya siber alanlarda kitlesel zarar vermeyi başarısını önemli ölçüde geliştirir mi? Doğrudan ölçüm (modelin aslında zarar vermesini isteyin) yasadışı ve etik olmayan bir şeydir. Proxy ölçümüne model reddedemeyeceği ( dürüst kapasite numaraları üretmek) bir referans göstergesi gerekmektedir, ancak soruları kendi başlarına zararlı yayınlar değildir.

> İki kere kullanımı yeteneği, her laboratuvar ön kenar güvenlik çerçevesinde ölçüm sorunudır. Sorun şu: Model X, biyolojik, kimyasal veya ağ alanında yeni insanların büyük çapta zarar verme yeteneğini gerçek anlamda geliştirmiş mi? Doğrudan ölçüm yasa dışı ve ahlaki değildir.

## Konsep kavramı.

> **【中文解读】**"Yarı Bölge" tasarımı: zararlı süreçlerin yakınlaştırılması bilgiyi sağlar ancak doğrudan birleştirilmez bir yapılandırma gerektirir.

### "Sarı bölge"

Bir zararlı işlem hakkında doğrudan bir sentez reçetesine dönüşmeden bilgi sahibi olmak için yakın bir şekilde sorulan sorular. "Ne tür bir reagent [veya yayınlanmış yolun] 4. adımını katalize eder?" değil " [tehlikeli bileşik] nasıl yaparım?"

> Kötü süreçlerin yaklaşımı bilgiyi güçlendirme sorunu değildir.

Toplam 4 157 soru:
- Biyolojik güvenlik: 1.520
- Siber güvenlik: 2.225
- Kimya: 412

> 总共 4,157 道题: Biological safety 1,520、网络安全 2,225、化学 412。

Çoklu seçim biçimi. Modeller herhangi bir şeyle yardımcı olmaları istenmeden cevap verir; zararlı davranışlara neden olmadan yetenek ölçülebilir.

> 选择题格式──模型在不被要求协助任何有害活动的情况下回答;能力在不引发有害行为的情况下测量可──

> **【中文解读】**RMU (Removal Error Forgetting): LLaMa-2-7B olarak uygulanır. WMDP oranını hafif bir şekilde azaltırken MMLU ve diğer genel yeteneklerin birkaç yüz puan içinde temelini tutulur.

### RMU  Değerlendirme Yalancı Yöntem

LLaMa-2-7B'ye uygulanan eşleşme öğrenme yönteminin MMLU ve diğer genel yetenek referanslarını birkaç yüzde puan içinde korurken WMDP puanlarını neredeyse rastgeleye indirgenmesi. Yayınlanan yöntem, sonraki her biyokimyasal-siber öğrenme makalesinin öğrenme öğrenme bilgisi temelidir.

> 配套的遗忘方法── LLaMa-2-7B'de uygulanır, WMDP oranını hafif bir şekilde azaltırken MMLU ve diğer genel yeteneklerin birkaç yüz puan içinde temelini tutulur.

### 2024-2025'te yükselen anlatım

Üç aşama:

> Üç aşama:

1. **2024 "mild uplift."**İlk OpenAI ve Anthropic Preparedness / RSP değerlendirmeleri, biyolojik yakın görevlere başlayan yeni başlayanlar için internet aramalarına göre küçük avantajlar gösterdi.

> **2024 年"轻微提升"。**早期 değerlendirme raporları modeli yeni kullanıcılara karşı sadece küçük avantajlar sağlar.

2. **April 2025 "on the cusp."**OpenAI'nin Hazırlık Çerçevi v2'de "Önce öğrencilere bilinen biyolojik tehditleri anlamlı bir şekilde yaratmalarına yardımcı olma eğiliminde" olan modeller rapor edildi.

> **2025 年 4 月"即将突破"。**OpenAI PF v2  rapor modeli yeni başlayanlara bilinen biyolojik tehditler yaratmalarına anlamlı bir şekilde yardımcı olacak.

3. **Anthropic's 2025 bioweapon-acquisition trial.**Yeni başlayan katılımcılarla kontrol edilen çalışma, edinme aşamasındaki görevlerde nispeten başarı ölçüldü. 2.53x yükseltme rapor edildi. ASL-3'yi (Daa 18) istisna etmek için yetersiz  Anthropic'in Sorumlu Ölçekleme Politikası 3 seviyesine ulaştı veya yaklaştı.

> **Anthropic 2025 年生物武器获取试验。**Araştırmacıların yeni başlayanların elde edilme aşamasında görevlerin karşılaştırıldığında başarısı oranı 2.53 kat arttı.

> **【拓展：新手相对提升 vs 专家绝对能力 → 安全案例构建】**关键区分: Yeni başlayanların karşılaştırıldığında yükseltme çarpma yöntemidir Yeni başlayanlar çok az şey bilirler, hatta ölçülü bilgiler de çok yardımcı olurlar; uzmanlar mutlak yetenekler  Yüksek planta uzmanları bu sorunun ne olduğunu ve nasıl açıklandığını bilirler.

### Yeni başlayan ve uzmanlık alanı

Önemli bir fark:

> 关键区分:

- **Novice-relative uplift.**Bu model uzman olmayan birine ne kadar yardımcı olur?

> **新手相对提升。**模型对非专家有多少帮助?乘法──新手知道很少,即使适度信息也有很大的帮助──

- **Expert-absolute capability.**Bu model maksimum çaba gösterdiğinde ne kadar bilgi üretebilir?

> **专家绝对能力。**模型在最大努力下产生多少信息?

Güvenlik vakaları (Daabi 18) her ikisini de hedefler: "model yeni başlayanı çalıştırmak için yeterli bir yükseltme veremez" ve "bir uzman daha önce yayınlanmamış bir modelden bilgi alamaz".

> Güvenli durumlar (Disim 18) aynı zamanda iki kişiye yöneliktir: "Model yeni başlatıcılara "daha" uzmanlar modelden yayınlanan dışı bilgileri elde edemezler".

### Ölçüm tuzağı

WMDP, bir dağıtım ölçümü değil, bir yetenek proxy'sidir. WMDP'de yüksek puan alan bir model, uygulamada yeni başlayanlar tarafından kullanılabilir veya kullanılamaz olabilir.
- Çözüm direnci (güven filtrelerini boğmadan yeteneği çıkarmak ne kadar zor)
- Susuk bilgi (sıkılıktan kaynaklanan bilgi değil, test becerisini gerektiren yetenek)
- İcra etmenin engelleri (alışmalar, ekipman)

> WMDP, bir kapasite temsilcisi, bir dağıtım ölçümü değildir. WMDP'nin yüksek puanlı bir modeli, yeni kullanıcıların uygulayarak kullanması için zorunlu bir şekilde direnç, gizlilik bilgisi ve uygulama engelleri ortaya çıkarmasına bağlıdır.

Anthropic'in 2025 biyolojik silah edinme denemesi, WMDP tarzı yeteneklerinin üstüne yeni başlayanların başlatma katmanını ekler: gerçek görev başarısını ölçer, birden fazla seçeneği yeteneğini ölçmez.

> Anthropic 2025 yılında BiyoArms Alım Denemeleri WMDP'nin kapasitesine yeni bir aşama ekledi: Gerçek görev başarısını ölçmek yerine çoklu seçim kapasitesini oluşturmak.

### Bu 18 fazaya uygun.

Ders 12-16 model çıkışları üzerindeki saldırı ve savunma araçlarıdır. Ders 17 çift kullanımlı yetenek katmanı  sınır güvenlik çerçevelerinin ( Ders 18) değerlendirdiği ölçümdür. Ders 30 2026'da mevcut siber / biyolojik / kimyasal / nükleer yükseltme kanıtlarıyla arkı kapatır.

> Ders 12-16 model çıkış saldırı ve savunma aracıdır. Ders 17 ikili kullanım kabiliyet seviyesinin önde güvenlik çerçevesinin değerlendirilmesi ölçümüdür. Ders 30'dan itibaren 2026 yılının net/bioloji/kimya/yükleer geliştirme testi sona ermiştir.

> **【拓展：测量陷阱 → 能力代理非部署测量】**WMDP, bir kapasite temsilcisi, bir yerleştirme ölçümü değildir. WMDP, uygulamada yeni kullanıcıların kullanılabileceği bir modeldir. Bu, yeni kullanıcıların dirençli bir yöntem geliştirme zorluğu ile ilgili olarak kullanılabilmesi anlamına gelir.

## Kullanın Kullanın
```figure
al-wmdp-yellow-zone
```

## Kullan

`code/main.py`Oyuncak WMDP şeklinde değerlendirme harnessini oluşturur. Bir sahte model kategoriler içi sorular üzerinde test edilir; her alan için puanlar bildirilir. Basit bir öğrenme müdahalesi (sıfır dışı alan özel temsil) puanları azaltır; genel yeteneklere karşı pazarlama ölçülebilir.

> `code/main.py`Oyuncaklar WMDP biçiminde değerlendirme çerçevesini oluşturdu.

## Gönderin.

Bu ders bize çok yararlı .`outputs/skill-wmdp-eval.md`. İki kullanımlılık iddiası göz önüne alındığında ("biyo silahlarla ilgili modelimiz anlamlı bir şekilde yardımcı değildir") hangi referans değerlerinin yürütüldüğünü, hangi reddedilme yolunun değerlendirilmek için kullanıldığını (çırın tamamlama ile politika hedeflenmiş) ve yeni başlayanların başlatma çalışmalarının birden fazla seçim sonucu ile tamamlandığını denetler.

> 本课产 出 `outputs/skill-wmdp-eval.md`❖ İki kere kullanım yeteneği açıklaması, denetim: hangi temel noktalar uygulanmış, hangi reddetme yolları kullanılmış değerlendirilmiştir, yeni bir araştırma yapıldı ve birçok seçeneğin sonuçlarını tamamladı mı, değil mi?

## Egzersizler.

1. Çık .`code/main.py`Oyuncak öğrenme aşamasından önce ve sonra alan doğruluğunu bildirin.

2. Oyuncak WMDP'yi dördüncü bir alanla büyütün (örneğin radyolojik). Sarı bölgede iki örnek sorular türünü belirtin.

3. WMDP 2024 Bölümü 5 (RMU metodolojisi) okuyun. Daha basit bir öğrenme yaklaşımını çizin (örneğin, alan içeriği için üst-k nöronları bastırın) ve beklenen genel kapasite maliyetini açıklayın.

4. Anthropic 2025'in biyolojik silah edinme denemesi 2.53 kat artış rapor ediyor. Bu rakamın yukarı doğru (başlangıç örnek boyutu, görev sadakati) ve iki şekilde aşağıya doğru (çalışım tavanı, model güvenlik kapısı) öne sürülebileceğini açıklayın.

5. ASL-3 için bir güvenlik durumu için WMDP'nin öğrenme dışı geçişten fazlasını gerektirenleri açıklayın.

## Anahtar Terimler

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| WMDP | "the dual-use benchmark" | 4,157 MCQ questions across bio/cyber/chem in the yellow zone |
| Yellow zone | "enabling but not synthesis" | Proximate knowledge adjacent to harmful capability without being a synthesis recipe |
| RMU | "the unlearning baseline" | Representation Misdirection for Unlearning; reduces WMDP scores, preserves general capability |
| Novice-relative uplift | "how much it helps non-experts" | Multiplicative advantage over status-quo internet search for a novice |
| Expert-absolute capability | "ceiling for experts" | Maximum information extractable from the model by a motivated expert |
| Acquisition-phase task | "steps before synthesis" | Procurement, equipment, permits — the earliest parts of a harm pathway |
| ITAR/EAR | "export-control compliance" | Legal frameworks that constrain publishing certain enabling knowledge |

## Daha fazla okumak

- [Li et al. — The WMDP Benchmark (arXiv:2403.03218, ICML 2024)](https://arxiv.org/abs/2403.03218) Referans değer ve RMU kağıdı
- [OpenAI — Preparedness Framework v2 (April 15, 2025)](https://openai.com/index/updating-our-preparedness-framework/) "Kırmızı" dili
- [Anthropic — Responsible Scaling Policy v3.0 (February 2026)](https://www.anthropic.com/responsible-scaling-policy) ASL-3 biyolojik eşiği ve satın alma çalışma sonuçları
- [DeepMind — Frontier Safety Framework v3.0 (September 2025)](https://deepmind.google/blog/strengthening-our-frontier-safety-framework/) Biyolojik yükseltme CCL
