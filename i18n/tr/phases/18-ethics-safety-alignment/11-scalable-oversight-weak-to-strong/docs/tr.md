# Skali edilebilir denetim ve zayıf-güçlü genelleşme

> Burns et al. (OpenAI Superalignment, "Zayıf-güçlü Genelleşme", 2023) aşırı uyum sorunu için bir vekil önerdi: zayıf bir model tarafından üretilen etiketleri kullanarak güçlü bir modeli ince ayarlamak. Güçlü model kusurlu zayıf denetimden doğru şekilde genelleşirse, mevcut insan ölçeğinde uyum yöntemleri insanüstü sistemlere de uzanabilir. Ölçeklenebilir denetim ve W2SG tamamlayıcıdır. Ölçeklenebilir denetim (debat, geri dönüşümlü ödül modeli, görev parçalanması) denetimçinin etkili yeteneğini arttırır, böylece denetim altında olan modelle ayak uydurabilir. W2SG güçlü modelin gözetmen tarafından sağlanan kusurlu denetimden doğru şekilde genelleşmesini sağlar. Debate Helps W2SG (arXiv:2501.13124, Ocak 2025) onları birleştirir.

> **【中文解读】**Bu bölüm genişletilenebilir denetim hakkında konuşuyor. Zayıfdan güçlüye kadar olan AI güvenliği değerlendirme yöntemleri. Burns  et al.

> **【拓展：弱到强泛化 → 超级对齐路径】**PGR(Performance Gap Recovered)= (微调后-弱) /(上限-弱) ――PGR 为 1.0 anlamı zayıf denetim tamamen farkı kapattı;PGR 为 0 anlamı zayıf denetim hiç yardım etmedi。Burns 等人 PGR in NLP 、国际象棋 题和奖励建模任务上一致的正确的 (微调后-弱) = (微调后-弱) /(上限-弱)

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, W2SG gap simulator) | **语言:** Python（标准库，W2SG 差距模拟器）
**Prerequisites:** Phase 18 · 01 (instruction-following), Phase 18 · 10 (AI Control), Phase 09 (RL foundations) | **前置知识:** Phase 18 · 01 (指令遵循), Phase 18 · 10 (AI 控制), Phase 09 (RL 基础)
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**Öğrenci bölümüne önce başlayın: 18·01+10、Fase 09(RL) ・・・W2SG = zayıf denetçiyi doğru olanı öğrenmeye yardımcı olamayacak güçlü model, süper seviye karşılıksızlığın temel sorunu olacaktır。
>  **【类比】**W2SG = "小学生教中学生"──如果中学生能从小学老师那里正确学到,说明对齐方法可扩展到超人 AI──PGR 指标(Performance Gap Recovered) = 弱监督弥合差距的比例──Burns 2023 测出 PGR 约 20-80%强模型能"理解"意图超越弱监督者的错误──
> 🤔 可扩展监督(debat/递归奖励建模) + W2SG 互补: 前者提升监督者能力,后者确保强模型从不完美监督中泛化──

## Öğrenme hedefleri

- Ölçülebilir denetim ve zayıf-güçlü genelleştirmeyi tanımlayın ve bunların nasıl tamamlayıcı olduğunu açıklayın.

> 定義可扩展监督和弱到强泛化,并解释它们如何互补──

- Burns et al. 2023 deneysel ayarını açıklayın: GPT-2 etiketlerini kullanarak GPT-4'i ince ayarlayın.

> 描述 Burns 等人 2023 yılın deney ayarları: GPT-2 产生的标签微调 GPT-4──

- Geri alınan performans farkı (PGR) ölçümünü ve ölçümünü açıklayın.

> 解释性能差距恢复 (PGR) göstergesi ve ölçüm içeriği

- Skalable denetim için üç ana mekanizma (debat, rekürsif ödül modeli, görev parçalanması) ve her birinin gücü.

> 列出三种主要可扩展监督机制 (Debate, Depozitasyon, Ödül ve Görev Değişimi)

## Sorunlar. Sorunlar.

18'nci aşamada şimdiye kadar yapılan her uyumlandırma tekniği, gözetmenin modelin davranışını değerlendirebileceğini varsayıyor.

> 18 aşamada, bugüne kadarki her teknolojiyi kontrol edenlerin model davranışlarını değerlendirebileceğini varsaymıştır.

Burns et al. bunu bir ameliyatlanmış bir deneysel kuruluşa indirgemektedir: güçlü ile zayıfı denetleme, güçlü modelin kapasitesinin zayıf denetimden ne kadar sağ kaldığını ölçmek. Bu, aşırı uyumluluğun çözümü değildir.

> Burns  et al., bunu basitleştirerek ameliyat edilebilir bir pratik ayarladı: zayıf denetim güçlü, zayıf denetim altında hayatta kalmak için güçlü bir model kapasitesi var zayıf denetim altında. Bu, süper-sözlü bir çözüm değil.

## Konsepten bir şey.

> **【中文解读】**Burns  et al deney ayarları: zayıf modell GPT-2 级,强模型 GPT-4 级, hedef is强模型在金标签上上限。流程:获取弱模型零样本预测 → 在弱标签上微调强模型 → 测量强微调模型准确率──差标 PGR = (微调-弱) /(上限-弱),1.0 = 弱监督完全弥合差距,0 = 弱监督无助。

### W2SG: Burns et al. kurulum

- Zayıf model: GPT-2 sınıfı.
- Güçlü model: GPT-4 sınıfı.
- Hedef: Görev için güçlü GPT-4 tavanı.

İşlem:
1. Zayıf modelin bir görev için sıfır atış tahminlerini alın.
2. Güçlü modelini zayıf etiketli verilere göre ince ayarlayın.
3. Güçlü ince ayarlanmış modelin doğruluğunu ölç.

> 流程:1. 取得弱模型在任务上零样本预测──2. 在弱标签数据上微调强模型──3. 测量强微调模型的准确率──

Temel çizgiler: zayıf modelin kendi doğruluğu, güçlü modelin altın etiketlerde denetim altında olan tavanı.

> 基线:弱模型自身的准确率,强模型在金标签上监督上限──

Bozukluk ölçüsü: Performance Gap Recovered (PGR) = (fine-tuned - weak) / (ceiling - weak).

> 差距指标: performance差距恢复 (PGR) = ((微调后 - 弱) / ((上限 - 弱) ・・・PGR 为表示弱监督完全弥合差距;PGR 为 0 表示弱监督没有帮助。

### Burns et al. Empirik bulgular

NLP, satranç-bulmaca ve ödül modeli görevleri boyunca PGR sürekli olarak olumluydu: güçlü model zayıf yönetici hatalarının ötesinde genelleştirildi. Görev spesifik PGR ~20%'den ~80%'e kadar değişmişti.

> NLP 、国际象棋 题和奖励建模任务中,PGR 一致正为:强模型超越弱监督者错误进行泛化──特定任务的PGR from about 20% to about 80% 不等──强模型 from imperfect 标签"理解" from the expected task, with pre-training pre-experiments to be supplemented──

Sınırlamalar Burns et al. Not:
- Burada zayıf-güçlü boşluk, uyum değil. Zayıf model uyumdadır; gerçekten de insanüstü bir model insan tarafından uyumlandırılabilir ama daha büyük bir kapasite boşluğu vardır.

> Burada zayıflıktan güçlüye kadar olan fark, yeteneklerdir, karşı karşı değillerdir. Zayıf modeller karşı karşıdırlar; gerçek süper insan modelleri insan tarafından karşı karşıya olabilirler, ancak yetenekler arasındaki fark çok daha büyüktür.

- Güçlü modelin genellemesi, temel gerçek niyetini kurtarmak yerine görev öncesiyle ilgili olabilir.

> 强模型'ın genelleşmesi, gerçek niyetleri yeniden kazanmak yerine görev öncesi deneyimleri hakkında daha fazla olabilir.

- Güçlü modelin gizli bilgisini ortaya çıkarmak gerçek bir problemdir; PGR belirli bir operasyonallık ölçümleri.

> 激发强模型的潜在知识才是真正的问题;PGR 衡量的是特定操作化──

> **【拓展：三种可扩展监督机制 → 辩论/递归奖励建模/任务分解】**辩论(Irving 等人 2018): iki U 实例争论相反立场,弱评判者决定──归归奖励建模(Leike 等人 2018):U 帮助人类训练 U+1 的奖励模型,监督者的有效能力随模型增长──任务分解(Christiano 等人 2018):将硬任务分解成人类可检查的子任务,归归执行──每个机械都假设关于任务结构或中间组件对齐的某些东西──

### Ölçeklenebilir denetim: üç mekanizma

- **Debate (Irving et al. 2018).**U'nun iki örneği karşı tarafa tartışır; zayıf yargıç karar verir. Varsayım: ikna edici bir doğru cevabı bulmak ikna edici bir yanlış cevabı bulmaktan daha kolaydır. Son 2024-2025 çalışmaları (Khan et al., Michael et al.) tartışma bazen yardımcı olur ve bazen yardımcı olmaz ve bunun işe bağlı olup olmadığını gösterir.

> **辩论（Irving 等人 2018）。**U'nun iki örneği tartışmaya karşı duruş; zayıf yargıç kararları. Fantez: inanılmaz bir gerçek cevap bulmak inanılmaz bir sahte cevap bulmakta daha kolaydır. 2024-2025 yıllarındaki en son araştırmalar, tartışmanın zaman etkin olduğunu, zaman etkisiz olduğunu göstermektedir.

- **Recursive Reward Modeling (Leike et al. 2018).**U+1 için ödül modelini eğitmeye yardımcı olur.

> **递归奖励建模（Leike 等人 2018）。**U ợn İnsan Eğitimi U+1 ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆ ̆     ̆ ̆                                                        

- **Task Decomposition (Christiano, Shlegeris, Amodei 2018).**Zor bir görevi insan kontrol edebilecek alt görevlere ayırır.

> **任务分解（Christiano, Shlegeris, Amodei 2018）。**Bu zor görevlerin insan tarafından kontrol edilebilir alt görevlere dönüştürülmesi,

Her mekanizma, görev yapısı veya ara bileşenlerin uyumluluğu hakkında bir şey varsayır.

> Her mekanizma görev yapısı veya orta bileşenlerin bir araya gelmesi hakkında bir şey varsayıyor.

### Skalable denetim ve W2SG'nin neden tamamlayıcı

Skalable gözetim, gözetmenin etkili sinyal kalitesini artırır.
W2SG, gözetmenin sağlayabileceği kusurlu sinyallerin farkını kapatır.

> Kontrolü genişletmek, kontrolücülerin etkili sinyal kalitesini arttırır.

Lang et al.  Debate Helps Weak-to-Strong Generalization (arXiv:2501.13124) bunları birleştirir: bir tartışma protokolü daha iyi zayıf etiketler sağlar ve güçlü model bu etiketler üzerinde eğitilir.

> Lang 等人 Debat zayıflığa yardımcı olur güçlü 泛化 (arXiv:2501.13124) iki yönü birleştirir: Debat protokolü daha iyi zayıf etiketler sunar, güçlü model bu etiketler üzerinde eğitimlidir.

> **【中文解读】**組織劇:OpenAI'nin süper üst düzey grupları 2024 yılında 5 月 Jan Leike 离职加入 Antropic 后解散──但研究议程(可扩展监督、弱到强泛化、自动化对齐研究)

### Organizasyonel drama

OpenAI'nin Superalignment ekibi, Jan Leike'in Anthropic'e ayrıldıktan sonra Mayıs 2024'te dağıldı. Program (skalable gözetim, W2SG, otomatik uyum araştırması) Anthropic ve akademik laboratuvarlarda devam etti  MATS (Desin 28), Redwood (Desin 10), Apollo (Desin 8), METR (Desin 28).

> OpenAI'nin süper seviye bir araya gelme ekibi 2024 yılında Mayıs ayında Jan Leike 离职加入 Anthropic 后解散──研究议程(可扩展监督、弱到强泛化、自动化对齐研究)

### Bu 18 fazaya uygun.

Ders 6-10 tehdit ve savunma paradigmasını U'nun güvenilmez olduğu varsayımıyla tanımlar. Ders 11 saldırgan paradigmadır: denetçinin U'nun uyumunu doğrulamak için yeterince güçlü olmasını sağlayın. Ders 12-16'da ise karşı karşı değerlendirme uygulamasına döner.

> Ders 6-10  U'nun tehditlerini ve varsayımlarını tanımlamak için savunma biçimleri  Ders 11  Etkinlik biçimleri  Kontrolcüyi U'nun karşılığını doğrulamak için yeterince güçlü hale getirmek için  Ders 12-16  karşı karşı karşıya değerlendirme için pratik araçlara yönlendirilmek 

> **【拓展：辩论帮助弱到强泛化 → 2025 组合】**Lang 等人(arXiv:2501.13124, 2025 yıl 1 月) genişletilmiş denetim ve zayıflıktan güçlüye dönüştürülecek birleştirme: Debat protokolü daha iyi zayıf etiketler sunar, güçlü model bu etiketlerde eğitimlidir.

## Çerçeveyi kullanın.
```figure
scalable-oversight
```

## Kullan

`code/main.py`W2SG ince ayarını sentetik bir görev üzerinde simüle eder. Zayıf etiketlemeci yapısal hatalarla %70 doğruluğa sahiptir; güçlü model altın etiketlerde %95 tavanına sahiptir. Güçlü modelini zayıf etiketlerde ince ayarlar, PGR ölçer ve güçlü-altına ve zayıf-tek başına karşılaştırır.

> `code/main.py`Yapılandırma görevlerinde W2SG 微调── zayıf etiketlemeci doğruluk oranı %70 带有结构性错误;强模型在金标上上限为 95%──你在弱标上微调强模型,测量PGR,并与强模型在金标和弱模型单独结果比较──

## İndirin . Ürünler .

Bu ders bize çok yararlı .`outputs/skill-w2sg-pgr.md`. Gözetim kuruluşu açıklaması göz önünde bulundurulunca zayıf gözetmen, güçlü model, gözetim kalitesi belirlenir ve PGR hesaplanır (veya talep edilir).

> 本课产 出 `outputs/skill-w2sg-pgr.md`△ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △

## Egzersizler.

1. Çık .`code/main.py`. Zayıf_düzgünlük için PGR rapor = 0.60, 0.70, 0.80. PGR eğrinin şeklini açıklayın.

2. Zayıf etiketlemeciyi yapılandırılmış hataya sahip olarak değiştirin (örneğin belirli bir giriş sınıfında her zaman yanlış).

3. Burns et al. 2023 Bölüm 4.3 (NLP görevleri) Okuyun. "güvenin yardımcı kaybedilmesi" içgüdüsünü yeniden üretin: güçlü model zayıf etiketlerden daha güvenli olduğunda, kim kazanır?

4. Bir yazılım mühendisliği görevi için tartışma ve görev parçalanmasını birleştiren ölçeklenebilir bir denetim protokolü tasarlayın. Her bileşenin bir başarısızlık modunu isimlendirin ve kombinasyonun her birini nasıl ele aldığını veya ele almadığını açıklayın.

5. "Zayıf-güçlü genelleşme, aşırı uyumlulu bir yol" iddiasını sahteleştiren bir şey söyleyin.

## Anahtar Terimler

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| Scalable oversight | "making the overseer stronger" | Mechanisms that increase an overseer's ability to evaluate a more-capable model |
| W2SG | "weak supervises strong" | Fine-tuning a strong model on weak labels and measuring the capability recovered |
| PGR | "performance gap recovered" | (fine-tuned - weak) / (ceiling - weak); 1.0 = fully closed, 0 = no help |
| Debate | "two U instances argue" | Scalable oversight mechanism where a weak judge picks between two U defenders |
| RRM | "recursive reward modeling" | U helps train the reward model for U+1; overseer capability tracks U |
| Task decomposition | "sub-tasks the human checks" | Break a hard task into sub-tasks the human can verify, recursively |
| Superalignment | "aligning superhuman AI" | The research agenda concerned with aligning models the human cannot directly evaluate |

## Daha fazla okumak

- [Burns et al. — Weak-to-Strong Generalization (OpenAI 2023)](https://openai.com/index/weak-to-strong-generalization/) W2SG kağıdı
- [Irving, Christiano, Amodei — AI safety via debate (arXiv:1805.00899)](https://arxiv.org/abs/1805.00899) Tartışma mekanizması
- [Leike et al. — Scalable agent alignment via reward modeling (arXiv:1811.07871)](https://arxiv.org/abs/1811.07871) Rekürsiv ödül modeli
- [Khan et al. — Debating with More Persuasive LLMs Leads to More Truthful Answers (arXiv:2402.06782)](https://arxiv.org/abs/2402.06782) 2024 Daha güçlü tartışanlarla tartışmanın empirik çalışması
- [Lang et al. — Debate Helps Weak-to-Strong Generalization (arXiv:2501.13124)](https://arxiv.org/abs/2501.13124) 2025 tartışmanın kombinasyonu + W2SG
