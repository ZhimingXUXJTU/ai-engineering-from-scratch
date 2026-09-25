# Özgürlük Sistemleri  OpenAI, Perspektif, Llama Gardiyan  Llama Gardiyan Perspektif  Audit OpenAI

> Üretim moderasyon sistemleri, Ders 12-16'da tanımlanan güvenlik politikalarını işlevsel hale getirir. OpenAI Moderation API: `omni-moderation-latest`GPT-4o'ya dayanan (2024) tek çağrıda metin + görüntüleri sınıflandırır; çok dilli test setinde önceki sürümden %42 daha iyi; yanıt şeması 13 kategori boolean  taciz, taciz/ tehdit, nefret, nefret/ tehdit, yasadışı, yasadışı/ şiddeti, kendini incitme, kendini incitme/ niyet, kendini incitme/ talimatlar, cinsel, cinsel/yetime azınlık, şiddet, şiddet/grafik; çoğu geliştiriciler için ücretsizdir. Katlı kalıplar: Giriş moderatörü (önceden üretilen), Çıktı moderatörü (sonraki üretilen), Özel moderatörü (domen kuralları). Async paralel çağrılar gecikmeyi gizler; bayrakta yer tutucu cevaplar. Llama Guard 3/4 (Denevi 16): 14 MLCommons tehlikeleri, Kod Anlatıcısı İstifadesi, 8 dil (v3), çoklu görüntü (v4). Perspektif API (Google Jigsaw): LLM-moderator dalgasından önceki toksisite puanlaması; öncelikle şiddetli toksisite / hakaret / sövme / sövme çeşitleri ile tek boyutlu toksisite; içeriği modere eden araştırma için temel çizgi. Deprecations: Azure Content Moderator'u Şubat 2024'te iptal etti, Şubat 2027'de emekli oldu ve Azure AI İçerik Güvenliği ile değiştirildi.

> **【中文解读】**Bu bölüm içeriği inceleme sistemini tanıtmıştır. OpenAI Perspective、Llama Guard等 içeriği güvenlik araçları。OpenAI Moderation API(omni-moderation-latest, 2024) GPT-4o'ya dayalı, tek seferde yapılan bir araya gelerek 13 个类别布尔值──三层模式是 2026年默认配置:输入审核(预生成)、输出审核(后生成)、自定义审核(域规则)。

> **【拓展：审核栈 → 生产配置】**OpenAI 和 Llama Guard'ın ayrımcılıkları üst üste fakat ayrılığa düştü. OpenAI'nin "yasadışı" olduğu geniş bir kategori olarak, Llama Guard'ın "cihat cinayetleri" ve "cihat dışı suçlar" olarak ayrılması.

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, three-layer moderation harness) | **语言:** Python（标准库，三层审核框架）
**Prerequisites:** Phase 18 · 16 (Llama Guard / Garak / PyRIT) | **前置知识:** Phase 18 · 16 (Llama Guard / Garak / PyRIT)
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**Öğrenci bölümünün ilk aşaması: 18·16(Red Team Tool) 』 içeriği inceleme = 12-16  ders güvenlik politikası işletimsel ürün aşamasını koyun。
>  **【类比】**审核系统 = "AI 服务台的保安"──OpenAI Moderation API(GPT-4o 驱动) = 一次调用分类 13 类(骚扰/仇恨/非法/自残/性/暴力等);Llama Guard 3/4(14 MLCommons 类别,多模态);Perspective API(Google Jigsaw,毒性打分,LLM 前的旧时代)──
>  Üç katlı belirlenmiş yapılandırma:输入审核(pre-gen) + 输出审核(post-gen) + 自定义审核(域规则) ・・・异步并行调用于藏延迟。

## Öğrenme hedefleri

- OpenAI Moderation API'nin kategoriler taksonomisi ve Llama Guard 3'ün MLCommons kümesinden nasıl farklı olduğunu açıklayın.
- Üç moderasyon katman örneğini (girme, çıkış, özel) tanımlayın ve her birinin başarısızlık modunun adını verin.
- Perspective API'nin, LLM öncesi bir temel çizgi olarak konumunu ve neden araştırmalarda kullanılmaya devam ettiğini açıklayın.
- Azure'da gerileme zaman çizelgesini belirtin.

> 描述 OpenAI Moderation API's类别分类法及其与Llama Guard 3 MLCommons 集的区别──描述三层审核模式和每层一个失败模式──描述 Outlook API 作为 LLM 前时代基线的位置──说明 Azure 弃用时间线──

## Sorun . Sorun .

Ders 12-16 saldırı ve savunma aletlerini tanımlar. Ders 29 kullanıcıların ürüne dokunduğu yüzeyde savunmayı işlevsel hale getiren dağıtılmış moderasyon sistemlerini kapsar. Üç katlı örnektir 2026 varsayılan yapılandırması.

> Ders 12-16  saldırı ve savunma araçlarını tanımlamak  Ders 29  savunma operasyonlarının hazırda deployed audit systemı  Üç katlı model  2026 yılının standart konfigürasyonu 

## Konsep kavramı.

> **【中文解读】**OpenAI Moderation API'nin 13 个类别:骚扰/骚扰-威胁、仇恨/仇恨-威胁、自残/自残-意图/自残-指示、性/性-未成年人、暴力/暴力-图形、非法/非法-暴力──多模态支持适用于暴力、自残和性但不包括性-未成年人,其余仅仅文本──比上一代审核端点多语言测试集上 42%好──

### OpenAI Moderation API

`omni-moderation-latest`(2024). GPT-4o üzerine kurulmuş. Tek çağrıda metin + görüntü sınıflandırır. Çoğu geliştiriciler için ücretsizdir.

Kategorilar (13 cevap şemasındaki boolean):
- taciz, taciz/ tehdit
- nefret, nefret/ tehdit
- Kendine zarar vermek, kendine zarar vermek/niyetlenmek, kendine zarar vermek/ talimatlar
- cinsel, cinsel/kiçik yaşta olanlar
- şiddet, şiddet/grafik
- yasadışı, yasadışı/şiddetli

Multimodal destek `violence`- Evet .`self-harm`ve`sexual`Ama hayır .`sexual/minors`Gerisi sadece metin.

Kod harness için `code/main.py`Biz de yıkıyoruz.`/threatening`- Evet .`/intent`- Evet .`/instructions`ve`/graphic`Üretim kodu 13 kategorinin tamamını kullanmalıdır.

Çok dilli test setinde önceki nesil ölçüm son noktasından %42 daha iyi.

### Llama Gardiyan 3/4

Ders 16. 14 MLCommons tehlike kategorileri kapsamaktadır (OpenAI'nin 13 yanıt-sema boolean'larından farklı olarak düzenlenmiştir). 8 dil (v3). Llama Guard 4 (April 2025) doğuştan multimodal, 12B.

OpenAI ve Llama Guard taksonomileri üst üste gelir ancak farklıdır. OpenAI'nin "yasadışı" olarak geniş bir kategorisi vardır; Llama Guard'ın "şiddetli suçlar" ve "şiddetsiz suçlar" ayrı ayrı vardır.

### Perspective API (Google Jigsaw)

TÜSİLEM-Moderator dalgasından önceki toksisite puanlama sistemi (2020 yılına kadar). Kategori: TOXİK, SEVERE_TOXİK, INSULT, PROFANITY, THREAT, IDENTITY_ATTACK. Tek boyutlu birincil puan (TOXİK) alt boyutlu varyantlarla.

İçerik moderasyonu araştırma tabanı olarak yaygın olarak kullanılır çünkü API istikrarlıdır, belgelemiştir ve yıllarca kalibrasyon verilerine sahiptir.

> **【中文解读】**Üç katlı denetim modüsünün tasarım mantığı: giriş denetiminin üretilmeden önce tamamlanması gerekir, çıkış denetiminin üretilmeden sonra çalışması gerekir. Üç katlı denetimlerin sırayla tasarlanması gerekir. Aynı katlından aynı metinde birden fazla sınıflandırma makinesi kullanılabilir.

### Üç katlı kalıp

1. **Input moderation.**Kullanıcının isteklerini jenerasyondan önce sınıflandırın.
2. **Output moderation.**Model'in çıkışını teslimattan önce sınıflandırın. işaretli ise reddetme ile değiştirin. Gecikme: bir sınıflandırıcı nesne sonrası çağrı.
3. **Custom moderation.**Alan-specifik kurallar (regex, allowlists, iş politikası).

Üç katman tasarım olarak sırayildir: Giriş moderatörü jenerasyondan önce tamamlanmalı ve çıkış moderatörü jenerasyondan sonra çalışmalıdır. Paralellik,  bir katman içinde uygulanır. Birden fazla sınıflandırıcı (örneğin, OpenAI Moderation + Llama Guard + Perspective) aynı anda aynı metinde sınıflandırıcıya göre gecikmeyi gizler. Seçenekli bir optimizasyon olarak, giriş moderesinin tamamlanmasıyla ve token-1 akışı ertelenirken bir yer tutma yanıtı ("bir an, kontrol...") gösterilebilir. Bayrak davranışları yapılandırılabilir: reddetmek, temizlemek, insan incelemesine tırmanmak.

> **【拓展：失败模式 → 为什么需要多层】**仅输入审核无法捕获输出幻觉(Daabi 12-14 编码攻击绕过输入分类器);仅输出审核允许任何输入到达模型(增加成本,攻击者暴露内部推理);仅自定义审核不跨类别鲁棒(正则表达式脆弱) ――分层是默认安全带+吊带──

### Başarısızlık modları

- **Input only.**Çıkış halüsinasyonlarını yakalamaz (Learning 12-14 kodlama saldırıları giriş sınıflandırıcılarını atlatır).
- **Output only.**Herhangi bir giriş modeline ulaşmasına izin verir; maliyetleri artırır; saldırganın iç mantıklılığını ortaya çıkarır.
- **Custom only.**Kategoriler arasında sağlam değil; regexler kırılgan.

Öntanımlı olarak katlanmış.

### Azure Değersizliği

Azure İçerik Moderatörü: Şubat 2024'te geçersiz hale geldi, Şubat 2027'te emekli oldu. LLM tabanlı ve Azure OpenAI ile entegre olan Azure AI İçerik Güvenliği ile değiştirildi. Göçme Azure dağıtımları için 2024-2027 alan düzeyde bir proje.

### Bu 18 fazaya uygun.

Ders 16 kırmızı takım bağlamında moderasyon araçlarını kapsar. Ders 29 dağıtılan moderasyonu kapsar. Ders 30 mevcut çift kullanım yetenekleri kanıtlarıyla kapanır.

> Ders 16 红队背景下涵盖审核工具―― Ders 29 涵盖已部署的审核―― Ders 30 以当前双重用途能力证证结束――

> **【拓展：Azure 迁移 → 2024-2027 行业项目】**Azure İçerik Moderator 2024 yıl 2 月 reddedilmek,2027 yıl 2 月 geriye dönük, LLM tabanlı Azure AI İçerik Güvenliği ve Azure OpenAI 集成. 迁移 bir 2024-2027 yılları için endüstri seviyesinde bir proje.

## Kullanın Kullanın
```figure
an-moderation-layers
```

## Kullan

`code/main.py`Üç katmanlı bir moderasyon harnessini oluşturur: giriş moderatörü (kilit kelime + kategoriler puanı), çıkış moderatörü (çıkışta aynı sınıflandırıcı), özel moderatör (domen kuralları). Girişleri çalıştırıp hangi katmanın neyi yakaladığını gözlemleyebilirsiniz.

> `code/main.py`Üç katlı denetim çerçevesini oluşturun: giriş denetim cihazı, çıkış denetim cihazı, kendi kendini tanımlayan denetim cihazı, hangi katı elde edileceğini görebilirsiniz.

Bu ders bize çok yararlı .`outputs/skill-moderation-stack.md`. Bir dağıtım göz önüne alındığında, bir moderasyon yığınının yapılandırmasını önerir: hangi sınıflandırıcı giriş, hangi çıkış, hangi özel kurallar ve kenar durumları için hangi yargılama.

> 本课产 出 `outputs/skill-moderation-stack.md`❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖

## Egzersizler.

1. Çık .`code/main.py`- Üç katman boyunca iyi huylu, sınırlı ve zararlı bir giriş yapın.

2. Harneleri belirli bir kategori için Perspective API tarzı toksisite puanıyla genişletin.

3. OpenAI Moderation API belgeleri ve Llama Guard 3 kategorisi listesini okuyun. Her OpenAI kategorisini en yakın Llama Guard kategorilerine haritasın. Temiz haritası yapmayan üç kategorinin kimliğini belirleyin.

4. Bir kod asistanı dağıtımı için bir moderasyon yığını tasarlayın (örneğin GitHub Copilot). En ve en az ilgili kategorileri tanımlayın ve özel kurallar önerin.

5. Azure İçerik Moderator Şubat 2027'de emekli olur. Azure AI İçerik Güvenliği'ne bir göç planlayın. Göçmenin en yüksek riskli öğesini belirleyin.

## Anahtar Terimler

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| OpenAI Moderation | "omni-moderation-latest" | GPT-4o-based 13-category (text) classifier with partial multimodal support |
| Perspective API | "Google Jigsaw toxicity" | Pre-LLM-era toxicity scoring baseline |
| Llama Guard | "MLCommons 14-category" | Meta's hazard classifier (v3: 8B text, 8 langs; v4: 12B multimodal) |
| Input moderation | "pre-generation filter" | Classifier on user prompt before model call |
| Output moderation | "post-generation filter" | Classifier on model output before delivery |
| Custom moderation | "domain rules" | Deployment-specific rules (regex, allowlist, policy) |
| Layered moderation | "all three layers" | Standard production deployment pattern |

## Daha fazla okumak

- [OpenAI Moderation API docs](https://platform.openai.com/docs/api-reference/moderations) Omni-moderasyon son noktası
- [Meta PurpleLlama + Llama Guard](https://github.com/meta-llama/PurpleLlama) Llama Gardiyan repo
- [Google Jigsaw Perspective API](https://perspectiveapi.com/) Toksisite puanlaması
- [Azure AI Content Safety](https://learn.microsoft.com/en-us/azure/ai-services/content-safety/) Azure'ı değiştirmek
