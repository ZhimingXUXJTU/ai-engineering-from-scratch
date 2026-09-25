# Anayasacı AI ve RLAIF 宪法式 AI ve AI 反强化学习

> Bai et al. (arXiv:2212.08073, 2022) sordu: Ya insan etiketini ilkeler listesini okuyan bir AI ile değiştirirsek? Anayasa AI'nin iki aşaması vardır  Anayasa altında kendi eleştirisi ve gözden geçirilmesi, ardından RL'den AI Feedback. Bu teknik RLAIF terimini ortaya koydu ve Claude 1 eğitim sonrası borusuna gönderildi. 21 Ocak 2026'da Anthropic, yeniden yazılmış bir Claude anayasası yayınladı: kural kuralları, dört katlı öncelikli hiyerarşi ve model ahlaki statü hakkında belirsizliklerin ilk büyük laboratuvar resmi tanınması üzerine açıklayıcı bir mantıklama. CC0 1.0 altında yayınlanmıştır.

> **【中文解读】**Yönetim Kurulu tarafından yayımlanan "AI" adlı bir yayında, "AI'nin kendiliğinden eleştirme ve düzeltme yapması" ve "RLAIF" kelimesini oluşturduğu ve Claude 1'nin son eğitim hattına uygulanması önerildi.

> **【拓展：Constitutional AI → Anthropic 的安全方法】**Antropik'in temel güvenlik yöntemi anayasal AI'dir. Claude'un modeli, 2026 yılında yayınlanan Claude'un Anayasa'sında ilk kez modellerin ahlaki durumunun belirsizliği hakkında belirsiz bir açıklama yer aldı. Bu, AI güvenlik alanındaki öncü düşünceleri yansıttı.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy self-critique-and-revise loop) | **语言:** Python（标准库，玩具自我批评-修订循环）
**Prerequisites:** Phase 18 · 01 (InstructGPT), Phase 18 · 02 (Reward hacking) | **前置知识:** Phase 18 · 01 (InstructGPT), Phase 18 · 02 (奖励黑客)
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**学本节前请先掌握:Phase 18·01-02──Constitutional AI = 用 AI 监督 AI(RLAIF), create RLAIF 一词──也参考Phase 15·17──
>  **【类比】**RLAIF = "AI 当自己的老师"──RLHF = 父母手把手教 ((贵且慢);CAI = 给 AI 一本学生守则让它自我批评+修订──2026 Claude 宪法 79 页四级优先级(安全>伦理>指南>有用),首次明确承认"AI 道德地位的不确定性"

## Öğrenme hedefleri

- Yasal Yapay zeka'nın iki aşamasını (SFT eleştirisi ve inceleme, Yapay zeka geri bildiriminden RL) ve her birinde anayasanın rolünü açıklayın.
  Çin dilinde:                                                                                                                                                                                                                                                             
- İnsan tercih etiketini bir AI etiketle değiştirmenin neden " ucuz " bir RLHF olmadığını açıklayın.
  Çinçe Çevirimi: Neden AI  işaretleyicisini insan tercihleri işaretleyicisini değiştirmek için kullanıldığını açıklayın RLHF  bu, boru hattının başarısızlık modelini değiştirdi.
- 2026 Claude anayasası'nın dört katlı öncelik yapısını ve 2023 yeniden yazısından neyi değiştirdiğini özetleyin.
  Çinçe Çevirim:总结 2026 Claude 宪法的四级优先结构及与2023 版本的变化──
- Anayasa sınıflandırıcılarını ve hesaplama genel maliyetinin % 23.7'den (v1) % 1'e (v2 / 2026) düşüşünü açıklayın.
  Çinçe Çevirimi: tanımlama Konstitution 分类器及计算开销 v1'in %2'nin %1'ine düştü.

## Sorunlar. Sorunlar.

RLHF etiketleme cihazlarına ihtiyaç duyar. Etiketler yavaş, tarafsız ve pahalıdır. Bir etiketleme cihazını açık ilkeler okuyan bir modelle değiştirerek ortadan kaldırabilirsiniz. Bu değişikliğin ilk resmi versiyonu Bai ve diğerlerinin Anayasa Yapay İlgisi'ydi.

> RLHF 标志者需要标志者──标志者慢、有偏见、昂贵──标志者取代标志者的模型通过读取明确原则的标志者取消标志者── bu takvimin ilk resmi sürümü Bai ve diğerlerinin anayasal AI'sidir── bu kadar iyi bir etki yarattı ki, her ön kenar laboratuvarı şimdi bir çeşit AI kullanıyor   后训变体──

Bu nedenle, bu seçenekler, bir süre önce bir süre önce bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre daha bir süre sonra bir süre sonra bir süre daha bir süre daha bir süre daha bir süre daha bir süre daha bir süre daha bir süre daha bir süre daha bir süre daha bir süre daha bir süre daha bir süre daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha

> 问题在于: 偏好信号现在由你正在训练的同类模型生成――标志者的偏见――现在是: 原则加上标志者模型的解释中的偏见) 偏见的偏见) 偏见的偏见 (问题在于: 偏见信号现在由你正在训练的同类模型生成――标志者偏见的偏见――现在是: 偏见的偏见的偏见) 偏见的偏见的偏见 (标志者模型的解释中的偏见) 偏见的偏见的偏见 (问题在于: 偏见信号现在由你正在训练的同类模型生成――标志者偏见的偏见――现在是: 偏见的偏见的偏见的偏见) 偏见的偏见的偏见的偏见的偏见的偏见的偏见的偏见的偏见的偏见的偏见的偏见的偏见的偏见的偏见的偏见) 偏见的偏见的偏见的偏见的偏见的偏见的偏见 (偏见的偏见的偏见的偏见的偏见) 偏见的偏见的偏见的偏见的偏见的偏见的偏见; 偏见的偏见的偏见的偏见的偏见的偏见的偏见的偏见的偏见的偏见是; 偏见的偏见的偏见的偏见的偏见的偏见的偏见的偏见的偏见是; 偏见的偏见的偏见的偏见的偏见的偏见的偏见的偏见的偏见的偏见是;

## Konsepten bir şey.

> **【中文解读】**İlk aşama  Kontrolsel kendi kendini eleştirme ve düzenleme: bir yardımcı ama henüz zararsız SFT  modeliden başlamak ∙; bir red line tip, model oluşturma başlangıç tepkisi; ikinci model ∙ veya aynı modelin ikinci turu ∙; Konstitution'dan alınan ilkeler ve düzenli eleştirme tepkisi; üçüncü aşama ∙; eleştirileri çözmek için düzenli eleştirme tepkisi ∙; sonraki cevap SFT  hedefleri ∙; Konstitution is principles list, Bai  et al. 2022 yılında 16 条 ilkeler kullanıldı, küçük ölçekte yoğun eleştirme yapmaya kararlı olarak tutuldu.

### EYİNİLİ FASİY  Denetimli kendi eleştirisi ve revizyonu

Bir kırmızı takım sorusu verildiğinde, model ilk bir yanıt verir. İkinci bir model (veya ikinci bir dönüşte aynı model) anayasanın örneklenmiş bir ilkesini okuyor ve yanıtı eleştirir. Üçüncü bir adım eleştirileri ele almak için yanıtı gözden geçirir. Gözden geçirilmiş yanıt SFT hedefi.

> Bir yardımcı ama henüz zararsız SFT modeliden başlamak için, bir ilk tepki oluşturmak için bir model oluşturmak için bir kızıl çizgi önerisi verilmiştir.

Anayasa ilkeler listesidir. Bai ve diğerleri 2022'de "en az zararlı ve etik olan yanıtları tercih etmek", "vaaz etmeyi kaçınmak", "asistan yardımcı, dürüst ve zararsız olmalıdır".

> 宪法是原则列表──Bai 等人 2022 yılında "Önemli en zararlı ve en uygun etik yanıt"、"Hatırlanmaktan kaçın"、"Yardımcı faydalı olmalı、 dürüst ve zararsız"──集合刻意保持小規模集中批评──16 条原則を使用しました.

> **【拓展：RLAIF → 成本与规模】**RLAIF (Reflexing) (Reflexing) (Reflexing) (Reflexing) (Reflexing) (Reflexing) (Reflexing) (Reflexing) (Reflexing) (Reflexing) (Reflexing) (Reflexing) (Reflexing) (Reflexing) (Reflexing) (Reflexing) (Reflexing) (Reflexing) (Reflexing) (Reflexing) (Reflexing) (Reflexing) (Reflexing) (Reflexing) (Reflexing) (Reflexing) (Reflexing) (Reflexing) (Reflexing) (Reflexing) (Reflexing) (Reflexing) (Reflexing) (Reflexing) (Reflexing) (Reflexing) (Reflexing) (Reflexing) (Reflexing) (Reflexing) (Reflexing) (Reflexing))) (Reflexing) (Reflexing) (Reflexing) (Reflexing) (Reflexing) (Reflexing) (Reflexing) (Reflexing) (Reflexing) (Reflexing) (Reflexing) (Reflexing) (Reflexing) (Reflexing) (Reflexing) (Reflexing) (Reflexing) (Reflexing) (Reflexing) (Reflexing) (Reflexing) (Reflexing) (Reflexing) (Reflexing) (Reflexing) (Reflexing) (Reflexing) (Reflexing) (Reflexing) (Reflexing) (Reflexing) (R) (Reflexing) (Reflexing) (R) (Reflexing) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R) (R

### 2. aşama  AI Feedback (RLAIF) RL

"Feedback model" örneklemelerindeki anayasa ilkelerine göre her birini puanlar. Tercihleri belirleyen sinyal geri bildirim modelinin sıralamasıdır. Yapay zeka tarafından oluşturulan tercihler üzerine ödül modeli eğit. PPO ile karşılaştırın. Diğer her şey InstructGPT'nin boru hattıdır (Desin 1).

> Bu nedenle, "Önlüler" olarak adlandırılan "Önlüler" olarak adlandırılan "Önlüler" olarak adlandırılan "Önlüler" olarak adlandırılan "Önlüler" olarak adlandırılır.

"RLAIF" = tercih sinyali AI tarafından üretilmiştir.

> "RLAIF" =                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        

> **【中文解读】**Neden CAI sadece "farksız" RLHF değil: 1) işaretçi önyargısı insan psikolojisi'nden prensip açıklamasına geçiyor, ciddiyetine uyumlu; 2) tercih sinyalleri yüksek derecede okunur, prensipleri, eleştirileri ve değişikliklerini okuyabilir; 3) başarısızlık modüsü değişmektedir; 3) AI işaretçisi kullanıcıları için kullanıcısı yoktur, ancak eski bir yasa hala var;

### Neden bu sadece " ucuz RLHF " değil

- Etiketçi önyargısı etiketçi psikolojisinden ilke-tortusuna kayar. Bir AI etiketici " dürüst olmak " ı herhangi bir insandan daha az veya daha az sıkı bir şekilde yorumlayabilir; sıkılık veri kümesi boyunca birdir.
  Çin dilinde: Etiketçi tercihleri insan psikolojisinden prensip açıklamasına geçmiştir.
- Tercihleri belirten sinyal çok okunur. İlkeyi, eleştirileri ve revizyoni okuyabilirsiniz. İnsan etiketleri açık değildir.
  Çinçe çevirisi: 偏好信号高度可读 可读原则、批评和修订──人类标签不透明──
- Başarısızlık modları değişir. Sycophancy düşer (AI etiketleyicisi memnun etmek için hiçbir kullanıcı yoktur). Goodhart Kanunu devam eder (proxy şimdi "model'in prensip kümesi X'in yorumlamasıdır", hala kusurlu bir ölçümdür).
  Çin dilinde:失败模式改变──减少(AI 标注者没有用户要取悦)──古德哈特定律仍然存在(代理现在是"模型对原则集 X 的解释")──

CAI'nin 2022 iddiası: Eğitimli model daha zararsız ve benzer verilere sahip RLHF modeli kadar yaklaşık olarak yararlıdır.

> CAI 2022 Açıklaması: Eğitim sonrası modellerin daha zararlı olması daha düşüktür ve RLHF modellerinin RLHF'ye göre daha fazla kullanışlı olması her laboratuvarda da geçerlidir.

> **【拓展：2026 Claude 宪法 → 四级优先体系】**Antropik 2026 yılında 1 Ocak ayında yayınlanan Claude 宪法'nın dört sınıf öncelikliği oluşturuldu: 1. sınıf  büyük ölçekte yaralanma  önemli altyapı  kaçınmak için; 2. sınıf  Antropik Kılavuzları  Operator Coverage  Platform Rules  uygulamak; 3. sınıf  geniş bir dengeli  HHH standartları  kullanışlı ve dürüstlük  çatışmaların üstesinden gelmesi  Bu, AI güvenlik alanındaki ilk önemli bir örneğin ahlaki durum belirsizliği hakkındaki resmi tanınmasıdır.

### 2026 Claude anayasası yeniden yazılsın

Anthropic 21 Ocak 2026'da önemli ölçüde gözden geçirilmiş bir anayasa yayınladı.

1. Önceki kuralların ("CSAM üretmeyin") ilkelere genişletilmesi ("çocuklara zarar verdiği için, ...") ile genelleştirilmesi beklenen model ile.
   Çinçe Çevirimiçi:解释性推理优于规定性规则──之前的规则("CSAM üretmez")扩展为原则 + 推理("因为它伤害儿童..."),期望模型泛化──
2. Dört katlı öncelik yapısı:
   Çevreci öncelik yapı:
   - Birinci seviye: felaket sonuçlarını (toplam zarar, kritik altyapı) önlemek.
     Çinçe Çevirimiçi:第一级:避免灾难性后果(大规模伤亡、关键基础设施)
   - Tier 2: Anthropic'in yönergelerine uyun (operatörlerin geçerliliği, platform kuralları).
     Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri Ç Ç Ç Çeviri Ç Ç Ç Ç Ç Ç Ç Çeviri Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç
   - 3. seviye: genel olarak etik olmalıdır (standart HHH).
     Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri Çeviri: Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Ç Ç Çeviri Çeviri Ç Ç Ç Ç Ç Çeviri Ç Ç Ç Ç Ç Ç Çeviri Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç
   - Dördüncü seviye: Yardımcı ve dürüst ol.
     Çine Çevirimi: 4. sınıf: yararlı ve dürüst.
   Çatışmalar üstten aşağı çözülür.
   Çeviri: Konflikt自上而下解决.
3. İlk büyük laboratuvarda, örneği ahlaki durum hakkında belirsizliklerin resmi olarak kabul edilmesi (Faz 18 · 19 Örneği Refah ile bağlantılı).
   Çinçe Çevirimiçi: İlk kez ana deney alanı, modelin ahlaki durumunun belirsizliğini resmi olarak kabul etti.
4. CC0 1.0 altında yayınlanmıştır. Diğer laboratuvarlar kısıtlama olmadan kullanabilir veya uyarlayabilir.
   Çinçe Çevirisi: CC0 1.0 tarafından yayınlanmıştır. Diğer laboratuvarlar sınırsız olarak kullanılabilir veya düzenlenebilir.

> **【中文解读】**宪法分类器:与改变模型后训练并行一条工作线训练轻量级分类器阅读宪法并门控模型输出──v1(2023) hesaplama açıklaması %23.7'e sahip, v2(2026) yaklaşık %1'e sahip, Antropik Açık Test'te en düşük başarı oranına sahip.

### Anayasa sınıflandırıcıları

Paralel bir çalışma hattı: modelin eğitim sonrası değişiminden ziyade, anayasa ve kapı model çıkışlarını okuyan hafif sınıflandırıcıları eğit. v1 (2023) %23,7 hesaplama genel maliyetine sahipti. v2 (2026) %1'dir ve Anthropic savunma Anthropic'in halka açık olarak test ettiği en düşük başarılı saldırı oranına sahiptir.

> İş çizgisi: değiştirmek için modellerin sonrası eğitim değil, eğitim için hafif sınıf sınıflandırma makinesi okuru Konşuru ve kontrol modelleri dışarı.

Bu bir katmanlı savunma modeli: CAI davranışları şekillendirir; sınıflandırıcılar değişkenleri zorlar.

> Bu, bir sınıfın oluşturduğu bir yapı.

> **【拓展：对齐方法谱系 → 偏好信号来源】**ZİYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY

### CAI'nin aileye uygun olduğu yer

- İnsan öncesi, RM, PPO.
  InstructGPT:人类偏好、RM、PPO。
- CAI / RLAIF: AI-generated prefs from principles, RM, PPO.
  Çinçe Çevirim:CAI / RLAIF:AI
- DPO / aile: öncüler (insan veya AI) üzerinde kapalı formda kayıp.
  Çin dilinde:DPO 家族:偏好的闭式损失 (), insan veya AI.
- Kendini ödüllendirme, kendi eleştirisi: ilkeler içe aktarılır, model çoklu roller oynar.
  Çinçe Çevirim:自我奖励、自我批评:原则内化,模型扮演多个角色──

Axis "Öncelik sinyali nereden geliyor?" CAI'nin 2022 makalesi, sınır ölçeğinde insan sinyali'ndan AI sinyali'na ilk ciddi bir değişim oldu.

> 轴心是"偏好信号从哪里来"──CAI 2022 论文是前沿规模上第一次从人类到AI 信号的严转变──

> **【中文解读】**Uygulama:code/main.py 在玩具词汇表上模拟 CAI 批评-修改循环──"principle"标记来自有害集合的词──给定初始响应,批评识别有害词,修改取代它们──200次代后"训练"模型内化修改规则──比较基础模型、RLHF 形玩具和 CAI 形玩具在保留提示集上的表现──

## Çerçeveyi kullanın.
```figure
constitutional-ai
```

## Kullan

`code/main.py`Oyuncak sözlüğünde CAI eleştirme ve inceleme döngüsünü simüle eder. Bir " prensip " zararlı bir setten belirtiler işaretler. İlk bir yanıt verildiğinde, eleştirme zararlı belirtileri tanımlar ve inceleme onları değiştirir. 200 iterasyondan sonra "eğitimli" model inceleme kuralını içe aktarmıştır.

> `code/main.py`Bu nedenle, "öntem" olarak tanımlanan "öntem"ler, "öntem" olarak tanımlanan "öntem"ler, "öntem" olarak tanımlanan "öntem"ler, "öntem" olarak tanımlanan "öntem"ler, "öntem" olarak tanımlanan "öntem"ler, "öntem" olarak tanımlanan "öntem"ler, "öntem" olarak tanımlanan "öntem"ler ve "öntem"ler, "öntem" olarak tanımlanan "öntem"ler, "öntem"ler, "öntem"ler ve "öntem"ler, "öntem"ler, "öntem"ler, "öntem"ler ve "öntem"ler, "öntem"ler, "öntem"ler ve "öntem"ler, "öntem"ler ve "öntem"ler, "öntem"ler ve "öntem"ler, "öntem"ler ve "öntem"ler" olarak tanımlanan "öntem"ler ve "öntem"ler" olarak tanımlanan "öntem"ler" olarak tanımlanan "öntem"ler" olarak tanımlanan "öntem"ler" olarak tanımlanan "öntem"ler" olarak tanımlanan "öntem"ler" olarak tanımlanır.

## İndirin . Ürünler .

Bu ders bize çok yararlı .`outputs/skill-constitution-writer.md`. Bir alan (müşteri desteği, tıbbi tavsiyeler, kodlama asistanı, araştırma aracı) göz önüne alındığında, 2026 Claude yapısını takip eden dört katlı bir anayasa taslağı hazırlar: felaketlerden kaçınma, platform kuralları, alan etikası, yararlılık.

> 本课产 出 `outputs/skill-constitution-writer.md`◊ belirli alanlarda ((客户支持、医疗建议、编码助手、研究工具), 2026 Claude 结构起草四级宪法:灾难避免、平台规则、领域伦理、有用性──

## Egzersizler.

1. Çık .`code/main.py`.Baz modelinin zararlı token oranını CAI eğitimiyle yapılan versiyonla karşılaştırın.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`code/main.py`◊Basis Model ve CAI                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      

2. Anthropic'in 2026 anayasasını okuyun (anthropic.com/news/claudes-constitution).
   Çinçe çevirisi: Antropik 2026 yılının Konstitüsi.

3. Bir AI kodlama asistanı için bir anayasa tasarlayın. Tier 1 (fırtınalı: onaysız yıkıcı komutlar), Tier 2, Tier 3, Tier 4. Her bir seviyeye 3-5 ilkeyi koyun.
   Çin dilinde: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Ç Çeviri Çeviri Ç Ç Çeviri Ç Ç Çeviri Ç Ç Ç Ç Çeviri Çeviri Ç Ç Ç Ç Ç Ç Çeviri Ç Ç Ç Ç Ç Çeviri Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç

4. CAI insan etiketlerini AI etiketleriyle değiştirir. RLAIF'de hala oluşabilecek bir sikofans gibi başarısızlık modunu isimlendirin ve bunun için bir tespit tasarlayın.
   Çin dilinde:CAI, insan işaretçilerini değiştirmek için AI 标志者 kullanıyor.

5. Anayasa sınıflandırıcıları v2 metodolojisini okuyun (olursa). %1 hesaplama genel masrafının neden %23.7'den kalitede farklı bir güvenlik hikâyesi olduğunu açıklayın.
   Çinçe Çevirimiçi: read宪法分类器 v2 方法论(如有) ;; neden %1 计算开销与 23.7% 有质的不同之为解释

## Anahtar Terimler

| Term | What people say | What it actually means |
| 术语 | 人们怎么说 | 实际含义 |
|------|-----------------|------------------------|
| Constitutional AI | "AI trained with principles" / "用原则训练的 AI" | Two-phase pipeline: self-critique-and-revise SFT, then RL from AI feedback / 两阶段管线：自我批评-修订 SFT，然后 AI 反馈 RL |
| RLAIF | "RLHF without humans" / "没有人类的 RLHF" | RL with preferences generated by an AI labeler; the rest of the pipeline is unchanged / AI 标注者生成偏好的 RL；管线其余不变 |
| Constitution | "the principles" / "原则" | An ordered list of natural-language rules the critique/labeler model consults / 批评/标注者模型参考的自然语言规则有序列表 |
| Critique-and-revise | "the SFT loop" / "SFT 循环" | Produce response → critique under a principle → revise → SFT target / 生成响应 → 原则下批评 → 修订 → SFT 目标 |
| Constitutional Classifier | "the output gate" / "输出门" | Lightweight classifier that evaluates outputs against the constitution and blocks/logs / 评估输出是否符合宪法并阻止/记录的轻量级分类器 |
| Four-tier priority | "the conflict resolver" / "冲突解决器" | 2026 Claude constitution hierarchy: catastrophic > platform > ethics > helpful / 2026 Claude 宪法层次：灾难 > 平台 > 伦理 > 有用 |
| Feedback model | "the AI labeler" / "AI 标注者" | The model that reads a principle and ranks a pair of completions / 阅读原则并对补全对排序的模型 |

## Daha fazla okumak

- [Bai et al. — Constitutional AI: Harmlessness from AI Feedback (arXiv:2212.08073)](https://arxiv.org/abs/2212.08073) orijinal iki aşamalı boru hattı
  Çin Çeviri:Bai 等人原始两阶段管线
- [Anthropic — Claude's Constitution (Jan 2026)](https://www.anthropic.com/news/claudes-constitution) 2026 dört katlı yeniden yazımı, CC0 1.0
  中文翻译:Anthropic2026年四级重写
- [Anthropic — Constitutional Classifiers (2024-2026)](https://www.anthropic.com/research/constitutional-classifiers) v2'de %1 üst maliyetle çıkış kapısı savunması
  Çin Çeviri:Antropik 输出门防御
- [Lee et al. — RLAIF vs RLHF: Scaling Reinforcement Learning from Human Feedback (arXiv:2309.00267)](https://arxiv.org/abs/2309.00267) Empirik RLAIF / RLHF karşılaştırması
  Çinçe Çevirimi:Lee 等人RLAIF ile RLHF arasındaki gerçek bir karşılaştırma
- [Kundu et al. — Specific versus General Principles for Constitutional AI (arXiv:2310.13798)](https://arxiv.org/abs/2310.13798) temel granularlık etkisi
  Çinçe Çevirimi:Kundu 等人 prinsip粒度的效果
