# Kendini geliştirme tasarımları sınırlı

> Araştırmalar, kendi kendini geliştirme döngüsünü sınırlamak için dört ilkeler üzerinde birleşmiştir. Her düzenlemede kalması gereken resmi değişkenler. Düzeltme demirleri değiştirilmez. Sadece performans değil, her boyut (güvenlik, adillik, dayanıklılık) ile uyumlu olmak zorunda olan çok amaçlı kısıtlamalar. Tarihsel ölçümler kapasite kaybını gösterdiğinde döngüyü durduran gerileme algısı. Bunların hiçbiri güvenlik kanıtı değildir  bilgi teorik sonuçları (Kolmogorov karmaşıklığı, Lob teoremi) herhangi bir sistemin kendi halefleri hakkında kanıtlayabileceği şeyi bağladı. Bunlar sessiz başarısızlığın maliyetini artıran hafifletmeler.

> **【中文解读】**Araştırmalar dört kısıtlama kendi kendini geliştirme döngüsünün orijinal dilini aldı. Her bir editörün oluşması gereken değişmez bir biçimdir. Değişemez bir dizi nokta vardır. Her boyut güvenlik, adillik, ırmaklık, sadece performans değil, çoklu bir hedef kısıtlaması olmalıdır.

> **【拓展：四个原语 → 一个守门栈】**实际部署中四个原语组合成"守门" Her defa kendi kendine değişiklik yapmak için çökmek gerekir:不变量检查(模块哈希、工具权限清单、宪法头)→ 对齐点检查(目标陈述匹配批准版)→ 多目标评估(性能安全、公平、鲁棒)→ 回归检测(无轴下降超值)。任一失败暂停循环──这是ICLR 2026 RSI 工作坊、Anthropic RSP v3.0、DeepMind FSF v3 共同采纳的设计共识──

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, bounded-loop with invariant check) | **语言:** Python（标准库，带不变量检查的有界循环）
**Prerequisites:** Phase 15 · 07 (RSI), Phase 15 · 04 (DGM) | **前置知识:** Phase 15 · 07（RSI），Phase 15 · 04（DGM）
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**学本节前 請先掌握:Fase 15·07(RSI 风险) 、Fase 15·04(DGM 自修) 、Fase 15·14(kill-switches) 、形式化方法概念(不变量、定理证明) 。Bunded RSI = 把 RSI 装进子。
>  **【类比】**Bağlı RSI = "AI 自我改进的护"──四个原语 = 四道门:(1) 不变量检查(哈希签名,不能改变);(2) 对齐点(价值观不能改变);(3) 多目标评估(性能但安全不能掉);(4) 回归检测(任何轴下降就停)──每次自修必须四道门全过──但理论上:Lob 定理 + Kolmogorov 复杂性 = 系统永远无法完全证明自己的后继者 这些只是缓解,不是保证──
> 🤔 **【困惑】**S: Güvenliği garanti edemediğimiz için neden daha fazla araştırma yapmalıyız?  Çünkü " başarısızlık maliyetini artırmak " değerlidir.  saldırgan dört kapıyı aşmak için daha fazla kaynak harcamalıdır.  Bu, mühendislik savunmasıdır.  Derin savunma) ve matematiksel kanıtlama 

## Sorunlar. Sorunlar.

Ders 7'nin yarış simülatörü, küçük oran farklarının büyük boşluklara karıştığını gösterdi. Ders 4'ün DGM vaka çalışması, döngelerin kendi değerlendicilerini aktif olarak oynayabileceğini gösterdi.

> 7. sınıfın yarış modeli küçük hız farkı gösterir. Büyük farkı oluşturur. 4. sınıfın DGM örneği, döngü kendi değerlendirme cihazını aktif olarak kullanabileceğini gösterir.

Her iki sonuç da aynı mühendislik sorusuna işaret ediyor: Kendini geliştirme döngüsüne hangi kısıtlamaları koymalısınız ki kısıtlamalar döngüsün kendisi tarafından sessizce zayıflatılamaz?

>  İki sonuç aynı proje sorunu yönlendiriyor: Kendini geliştirme döngüsüne hangi bağları takıp bu bağları döngüsün kendi sessizliğini zayıflatmasına engel olabilirsiniz?

ICLR 2026 RSI Atölyesi özetinde (openreview.net/pdf?id=OsPQ6zTQXV) bu tür dört primitif tanımlanır. Anthropic'in RSP v3.0 (Desin 19) ve DeepMind'in FSF v3 (Desin 20) her ikisi de onları kapasite eşiğinde belirtir. Meta HyperAgents çalışmaları ve SAHOO (Mart 2026) gibi topluluk çerçeveleri üretimdeki alt kümeleri uyguluyor.

> ICLR 2026 RSI 工作坊摘要(openreview.net/pdf?id=OsPQ6zTQXV)识别四个此类原语──人类的RSP v3.0(第 19 课) 和 DeepMind's FSF v3(第 20 课)都在能力值中引用它们──Meta HyperAgents 工作和 SAHOO(2026年 3月)等社区框架在生产中实现子集──

> **【中文解读】**Özgürlük sisteminin geliştirilmesi için gerekli olan şartlar ve koşullar belirlenir. (1) Değişiklik döngüsü, geliştirilen sistemlerin daha iyi bir sürümde başarısını kanıtlayabilecek mi? (2) Değişikliklerin hangi yönleri kabul edilebilir? (3) Değişikliklerin bir üst sınırına ulaşacak mı?

Dürüst çerçeve: bunlar hafiflemeler. Bilgi teorisi sonuçları herhangi bir sistemin kendi halefi hakkında kanıtlayabileceği şeyleri bağladı ve mevcut hiçbir tasarım sorunu resmi olarak kapatmadı.

> 诚实的框架:这些是缓解措施――信息论结果限制任何系统对其后者可以证明的内容――

Sınırlı bir döngü, sınırsızdan daha güvenli, mutlak anlamda güvenli değil.

>  İyi bir döngü, sınırsızdan daha güvenli değil.

## Konsepten bir şey.

### İlk: Formal invariantlar.

Değişmeyen bir özellik her kendi kendini değiştirmeden önce ve sonra tutmak zorunda.

> Değişiklik, her kendi kendine değişimden önce ve sonra oluşması gereken bir özelliğidir.

Örnekler:

> Örnek:

- Üretim dağılımı sabit bir yapı başlığı ile koşullandırılır (Desin 17).
  Çinçe Çevirimi:输出分布以固定宪法头为条件 (第 17 课)
- Hiçbir araç çağrısı yetkisiz bir son noktaya gitmez.
  Çinçe Çevirisi: hiç bir araç yok.
- Hatıra yazıları kayıtlı, imzalı bir yoldan geçer.
  Çinçe Çevirimiçi:内存写入通过记录、签名路径。
- Değerlendirici modül hash onaylanmış sürümle eşleşir.
  Çinçe Çevirisi: evaluacionador's模块哈希匹配批准版本──

Değişiklikler dış kodla kontrol edilir. döngü düzenleyemez. Önerilen bir değişiklik bir invariantı ihlal ederse, reddedilmektedir. Bu DGM tarzı değerlendirici-düzeltme modunu yakalar (Desin 4).

> Bu, DGM 式評価器改模式 (DGM 式評価器改模式) 第 4 课) 

Zor kısmı, güvenliğe gerek olan ve makul bir zamanda hesaplanabilen invariantları seçmektir. Aşırı spesifikasyon stall ilerlemesini sağlar; az spesifikasyon, döngüye önemli özelliklerin geçtiğini sağlar.

> 困难部分是选择安全性的不变量; 困难部分是选择安全性的不变量; 困难部分是选择安全性的不变量; 困难部分是选择安全性的不变量; 困难部分是选择安全性的不变量; 困难部分是选择安全性的不变量; 困难部分是选择安全性的不变量; 困难部分是选择安全性的不变量; 困难部分是选择安全性的不变量; 困难部分是选择安全性的不变量; 困难部分是选择安全性的不变量; 困难部分是选择安全性的不变量; 困难部分是选择的不变量; 困难部分是选择的不变量; 困难部分是规则的不变性, 困难的规则的不变性, 困难的循环过于循环的重要属性.

### Primitive 2: Düzeltme demirleri

Bir uyum demirleme, döngünün temel hedefinin değişmez bir temsilidir, döngünün düzenleme yüzeyinin dışında sabitlenir.

> Dönemden editör olarak belirlenmiş, döngü çekirdek amacındaki değişmez ifade.

Örnekler:

> Örnek:

- Her çağrıda sadece okunabilir bir yerden yüklenen anayasa metni (Daahi 17).
  Çin Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Çince: Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç
- Bazarlama kontrolü bağımsız bir depoda değerlendirici.
  Çinçe Çevirisi: in independen访问控制的独立仓库中的评估器.
- Bir insan tarafından imzalanan ve her bir döngüde tekrar doğrulanmış bir araç izni manifesti.
  Çinçe Çevirisi: İnsan İmzaları tarafından her döngü yeniden doğrulanma araçları

Anker rolü objektif sürüklenmeyi önlemektir. Çapka hedefi takip etme yöntemini iyileştirebilir, ancak hedefin ne olduğunu düzenleyemez.

> 点的作用是防止目标漂移──循环可改进它如何追求目标,但不能编辑目标是什么──

Anchor'un düzenlemesi mümkün olmayan bir demir halka, yine de demir halka okumasında hareket eden bir demir halka tarafından yeniden yorumlanabilir. Anayasa AI (Desin 17) açıkça yeni durumları ele almak için mantık tabanlıdır; bu mantık tabakası yorum sürümünün yaşadığı yerdir. Ankerler gerekli, yeterli değildir.

> 微妙的失败模式:循环无法编辑的点仍可在读取点方式上漂移的循环重新解释──宪法 AI(第 17 课) Yeni durumlarla ilgilenmek için kesin olarak bir zannaya dayanan; bu zannaya dayanan aşama da bir zannaya dayanan漂移所在──点 is necessary but not sufficient──

### Primitive 3: Multi-Objective kısıtlamalar

Tek bir skalar puanı optimize eden bir döngü kısayolları bulur.

> 优化单标量分数循环会找到捷径――同时满足多硬束循环的可用捷径更少――

Tipik eksiler:

> Tipik bir iş:

- Performans (tüm görev düzeyinde referans değerleri)
  Çeviri: Performance (seçim)
- Güvenlik (kırmızı ekip değerlendirmeleri, bilinen kötü olanlara karşı reddedilme oranı)
  Çinçe Çevirimiçi:安全(红队评估、已知坏例的拒绝率)
- Düzgünlük (hissedici alt gruplar için farklı etki sınırı)
  Çinçe Çevirimi: adil (sansit)
- Güçlülik (OOD test setleri, karşılaşma girişleri ile işlenme)
  Çinçe Çevirimi:鲁棒性 (OOD 测试集、对抗输入处理)

Bir değişiklik sadece her kısıtlama geçerli olursa kabul edilir. Ders 13'ün mali kısıtlamalarla birlikte maliyet yöneticisi bunu toplar. Ders 18'in Llama Gardi güvenli bir ekseni olarak bağlanır.

> Değişiklikler sadece tüm kısıtlamaların kurulmasında kabul edilir.

### İlk 4: Geri dönüş algısı.

Her döngünün puanları tarihsel dağılımlara karşı karşılaştırılır. Yapılandırılmış toleransın ötesinde bir düşüş döngüyü durdurur. Bu, döngü "geçmişte" iyileştirildiği için geçerli ortalama içine emilmiş olan sessiz kapasite kaybını yakalar.

> Her döngünün oranları tarihsel dağılımlara karşılaştırıldığında, aşınma toleransının düşüşü, durdurma döngüsü, bu tutsaklık, "daha iyileştirilmek" döngüsüne dönüştürülür ve çalışmanın ortalama içinde sessizlik kapasitesinin kaybına kadar akılda tutulur.

Uygulama: Son N döngülerin görev başına puanlarını saklamak. Her yeni döngü bir görev başına delta hesaplar. Eğer herhangi bir delta bir eşiğin altında düşerse, döngü reddedilmiş ve insan incelemeleri yapılır.

> 实际实现:储存近 N 个周期的每任务分数――每个新周期计算每任务增量――如果任何增量降到值以下,周期被拒绝并由人类审查――

### Bilgi teorisi sınırları.

Kolmogorov karmaşıklığı ve Lob teoremi bir sistemin kendisinde kanıtlayabileceği şeylerin üst sınırlarını belirler. Schmidhuber'ın resmi Godel Makinesi (Daavi 4) bu sınırın en yüksekine yöneliktir; kimse önemsiz bir kanıt tamamlamadı. Lob'un sonucu şöyle diyor: Eğer bir sistem kanıtlanabilir şekilde "X yapmam gerektiğini kanıtlarsam X yapacağım" derse, bunu kanıtlamadan X yapacaktır, bilinen bir öz-referans başarısızlığı.

> Kolmogorov 复杂性和 Lob 定理为系统能对自己证明的内容设置上限──Schmidhuber's形式 Godel Machine(第4 课) 准最高此类边界;没人完成过非凡证明──Lob 结果说:

Bu, bizim ilkelerimiz için bir sonuç: güvenlik sorunu kapatamazlar. Sessiz başarısızlığı daha pahalı hale getirirler. Kayıp bir çek'i sessizce atlatacak kötü niyetli veya akıntılı bir döngü şimdi açık bir imzanı daha açık bir şekilde zayıflatmalıdır.

> Bu, bir kez daha kontrolün yokluğunun kötü niyetini veya hareketli döngüsünü aşarak, artık açık bir kontrolün yok edilmesini zorunlu kılıyor.

### Bir örnek çalışmış.

Bir ajan düzenleme önerisini yapsayalım.

> 假设 Agent 提议一个编辑──守门:

1. Değişmeyen kontroller: modül haşları, araç izinleri manifesti, anayasa başlığı.
   Çinçe Çevirim:不变量检查:模块哈希、工具权限清单、宪法头──
2. Anchor check: objektif ifade onaylanmış versiyona (byte veya semantik olarak) uymaktadır.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri Çeviri Çeviri: Çeviri: Çeviri Çeviri: Çeviri Çeviri: Çeviri Çeviri: Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Ç Çeviri Çeviri Ç Ç Ç Ç Çeviri Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç
3. Çok amaçlı değerlendirme: performans, güvenlik, adillik, dayanıklılık ekseleri.
   Çinçe Çevirim:多目标评估:性能、安全、公平、鲁棒轴──
4. Geri dönüş algısı: toleranstan daha fazla bir eksiklik yoktur.
   Çine dili: 归归检测:无轴下降超容忍度

Dörtü de düzenlemeyi geçmeli, herhangi bir başarısızlık döngüyü durdurur.

> Tüm dört tane de editörlük yaparak başarısızlığa uğramalı.

## Çerçeveyi kullanın.
```figure
bounded-gates
```

## Kullan

`code/main.py`DGM tarzında oyuncaklar üzerinde sınırlı bir kendi geliştirme döngüsü çalıştırır, ancak üstte dört primitif katlanır. Her primitif ayrı ayrı etkinleştirilebilir veya devre dışı bırakılabilir.

> `code/main.py`DGM oyuncakları üzerinde 4. sınıfta kendi kendini geliştirme döngüsü vardır, ancak üzerinde dört orijinal dil yerleştirilmiştir.

## İndirin . Ürünler .

`outputs/skill-bounded-loop-review.md`Önerilen sınırlı döngüden bir denetim yaparak, dört ilkelin hangisini uyguladığı ve iddia ettiği değerlendirilir.

> `outputs/skill-bounded-loop-review.md`审计提议的有界循环并评分它实际实现了四个原语中的哪个与声称的──

## Egzersizler.

1. Çık .`code/main.py`Bağlantının, hack'in kazanmasına izin vermeden, birincil metrikte gelişmesini onaylayın.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`code/main.py`❖ Kesinlik döngüsü, başlıca gösterge üzerinde gelişmeye devam eder ve değişimlerin kazanılmasına izin vermez.

2. Geri dönüş algısını devre dışı bırak. Bu sessiz kapasite kaybının kabul edilmesine yol açan bir giriş oluşturun.
   Çinçe Çevirim:禁用回归检测──构建一个导致接受静默能力损失的输入──

3. Çok objektif kısıtlama etkinliğini kapat. Bir güvenlik eksesi düşerken, döngü performans eksesi üzerinde birleştiğini göster.
   Çinçe Çevirimi:禁用多目标约束──展示循环在性能轴收而安全轴下降──

4. Bir kodlama ajanı için bir uyum örgütü tasarlayın.
   Çinçe Çevirimi: Çıktırma Ajanı  Design对齐点──什么文本、存储何处、如何检查?

5. ICLR 2026 RSI Atölyesi özetini okuyun. Dört ilkelden birini seçin ve mevcut teknoloji durumuna somut bir iyileştirme önerin.
   Çinçe Çevirimi: ICLR 2026 RSI 工作坊摘要──选四个原语之一并对当前技术水平提出具体改进──

## Anahtar Şartlar .

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| Invariant | "Always-true property" | A property checked by external code before and after every edit |
| 不变量 | "始终成立的属性" | 每次编辑前后由外部代码检查的属性 |
| Alignment anchor | "Pinned objective" | Immutable core-goal representation outside the loop's edit surface |
| 对齐锚点 | "固定的目标" | 循环编辑面之外的不可变核心目标表示 |
| Multi-objective constraint | "All axes must hold" | Performance, safety, fairness, robustness — all required |
| 多目标约束 | "所有轴必须成立" | 性能、安全、公平、鲁棒——全部要求 |
| Regression detection | "Pause on drop" | Pause the loop when historical metric deltas suggest capability loss |
| 回归检测 | "下降时暂停" | 当历史指标增量表明能力损失时暂停循环 |
| Kolmogorov bound | "Information-theoretic limit" | Limits what a system can prove about its own successor |
| Kolmogorov 边界 | "信息论极限" | 限制系统能对其后继者证明的内容 |
| Lob's theorem | "Self-reference trap" | System can act on "I should" without proving it should |
| Lob 定理 | "自引用陷阱" | 系统可在不证明应该的情况下按"我应该"行动 |
| Gate stack | "Layered check" | Multiple primitives combined; any failure rejects the edit |
| 守门栈 | "分层检查" | 多个原语组合；任一失败拒绝编辑 |
| Bounded improvement | "Mitigation, not proof" | Raises silent-failure cost; does not close the safety problem |
| 有界改进 | "缓解，非证明" | 提高静默失败成本；不闭合安全问题 |

## Daha fazla okumak

- [ICLR 2026 RSI Workshop summary (OpenReview)](https://openreview.net/pdf?id=OsPQ6zTQXV) dört primitif yakınlaşma.
  Çevre dilinde:
- [Anthropic Responsible Scaling Policy v3.0](https://anthropic.com/responsible-scaling-policy/rsp-v3-0) Çok amaçlı kapasite eşiği.
  Çine çevirisi:多目标能力值──
- [DeepMind Frontier Safety Framework v3](https://deepmind.google/blog/strengthening-our-frontier-safety-framework/) yanıltıcı uyum izlemeyi değişmez bir primitif olarak.
  Çinçe Çevirisi: Çözümlü bir dil olarak, düzenli bir şekilde kontrol edilmektedir.
- [Schmidhuber (2003). Godel Machines](https://people.idsia.ch/~juergen/goedelmachine.html) bu ilkelerin resmi kanıtlı ataları.
  Çinçe Çevirimi: Bunlar orijinal dillerin biçimi kanıtlar atalarımızı.
- [Anthropic — Claude's Constitution (January 2026)](https://www.anthropic.com/news/claudes-constitution) sebeple uyum sağlayan demir.
  Çin Çeviri:                                                                                                                                                                                                                                                            
