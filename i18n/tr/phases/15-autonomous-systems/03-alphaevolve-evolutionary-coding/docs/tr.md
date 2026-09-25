# AlphaEvolve  Evrim kodlama ajanları  AlphaEvolve  Devrim kodlama ajanları

> Devrimsel bir döngü ve makine kontrol edilebilir bir değerlendirici ile sınır kodlama modeli eşleştirin. Çubuk yeterince uzun sürsün. Bu, 48 skalar çarpımı kullanan 4x4 kompleks-matris çarpma prosedürünü keşfeder. 56 yıl içinde Strassen'in ilk gelişimi. Ayrıca, üretimde bulunan klüster hesaplamalarının %0,7'ini geri alan Google genelinde bir Borg programlama heuristik bulur. Mimarlık kasten sıkıcı. Kazançlar değerlendirici'nin katılamasından kaynaklanmaktadır.

> **【中文解读】**Önceki kodlama modeli, gelişme döngüsü ve makineler kontrol edilebilir değerlendirme makinesi ile eşleşirken, döngü yeterince uzun süre çalışsın. Bu, 48 kez ölçüm çarpımının 4x4 tekrarlama matrajı çarpım sürecini 56 yıldır ilk kez aşan Strassen'i kullanan bir yöntem buldu. Ayrıca, bir Google genel Borg Düzenleme Başlatma biçimi de buldu.

> **【拓展：进化算法 + LLM 的化学反应】**进化算法 (?? 变异+选择+交叉) on yıllarca bir geçmişe sahiptir, ancak geleneksel 随机变异大型程序larda neredeyse her zaman dil biçim hatası oluşur. LLM "Akıllı 变异算子" olarak bu noktayı değiştirdi: onu bir şekilde düzenleyerek geçiyor, anlamda mantıklı bir değişiklik yapabilir.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, evolutionary-loop toy) | **语言:** Python（标准库，进化循环玩具）
**Prerequisites:** Phase 15 · 01 (long-horizon framing), Phase 15 · 02 (self-taught reasoning) | **前置知识:** Phase 15 · 01（长程框架），Phase 15 · 02（自我教学推理）
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**学本节前 Lütfen önce bil:Fase 15·01(长程 Agent)、Fase 15·02(STaR 自我改进)、进化算法基础(变异/交叉/选择)。AlphaEvolve = LLM 作为智能变异算子的进化算法──
>  **【类比】**AlphaEvolve = "AI 实验室里的博士生群体"。传统进化算法 = 随机打字员(多数是乱码);AlphaEvolve = 一群 AI 博士生,每个人都提出有意的修改("试试把循环展开两倍"),评估器跑实验打分,高分修改进入下一代种群──LLM 解决"如何提出合理变异",评估器解决"如何辨别伪"结真合 56年第一次突破 Strassen 矩阵乘法──
> 🤔 **【困惑】**S: AlphaEvolve neden insan uzmanlarından üstün olabilir? Çünkü milyonlarca kez gerçek bir referans değerini kullanarak 验证 ediyor.

## Sorunlar. Sorunlar.

Büyük dil modelleri kod yazabilir. Evrimsel algoritmalar kod üzerinde arama yapabilir. İkisi de on yıllardır ayrı ayrı denedi; ikisi de tavanlara ulaştı.

> Büyük dil modeli kod yazabilir, gelişen algoritmalar kod alanında arama yapabilir.

LLM tavanı bir konfabulatörlüktür: model iddia ettiği şeyi yapmayan makul kod yazar. Evrimsel tavan arama maliyetidir: sentaks üzerinde rastgele mutasyonlar nadiren oluşturur, daha iyi programları bile söylemeyiz.

> LLM'nin planşeti, uydurma bir biçimdir: Modeller mantıklı görünen ama gerçekte davranışta bulunmayan bir kod yazıyor.

AlphaEvolve (Novikov et al., DeepMind, arXiv:2506.13131, Haziran 2025) bunları birleştirir. LLM bir program veritabanına hedeflenmiş düzenlemeler önerir; otomatik bir değerlendirici her variansı puanlar; yüksek puanlı varianlar gelecek nesiller için ebeveyn olur. LLM makul kod yazmanın pahalı adımı ele alır; değerlendirici konfabulasiyonları yakalar.

> AlphaEvolve(Novikov 等人,DeepMind,arXiv:2506.13131,2025 yıl 6 月) iki şeyi birleştirir.LLM program veritabanı için özel bir düzenleme önerir.

> **【中文解读】**AlphaEvolve (Google DeepMind, 2025) gelişim algoritmasını kod optimizasyonu için kullanmaya başlayacak. Bu, bir program seyhediyi, değişiklik, geçiş ve seçim yoluyla sürdürmek için kullanılacak.

Sonuçlar bildirildi: 48-skala-koşul-koşul 4x4 kompleks matris çarpımı (Strassen'in 1969 sınırı 49 idi), Google üretiminde bir Borg programlama heuristik, %32,5 FlashAttention çekirdek hızlandırması, Gemini eğitim geçiş gelişimleri.

> Rapor sonuçları: 48 kez 标量乘法 4x4 复矩阵乘法(Strassen 1969 yılının sınırı 49),Google 生产中的 Borg调度启发式,32.5%'nin FlashAttention 内核加速,Gemini 训练吞吐量改进──

Arsitektur çalışır çünkü değerlendirici makine kontrol edilebilir. değerlendirici olmayan yerde çalışmaz. Bu asimetri ders.

> Bu tür eşleşmesizlik, bu dersin merkezinde: yapıların bu yüzden geçerli olduğu için değerlendirme makinesi kontrol edilebilir; değerlendirme makinesi inanılmaz bir alan, döngü başarısız olduğu için geçerlidir.

## Konsepten bir şey.

### Çember döngüsü

1. Tohum programından başla `P_0`Bu doğru ama optimum değil.
   Çin Çeviri: Doğru ama iyi bir tohum programından`P_0`Başlayın.
2. Değişiklik programlarının bir veritabanını tutmak, her biri değerlendirici tarafından puanlanmıştır.
   Çinçe Çevirimi:维护一个变体程序数据库,每个变体由评估器打分──
3. Veritabanın (MAP-elite tarzı veya ada tabanlı) bir veya daha fazla ebeveyn örneği.
   Çin Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Ç Çeviri: Ç Ç Ç Ç Ç Ç Ç Çeviri: Çeviri: Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç
4. LLM'yi (Biri Flash birçok aday için, İkiz Pro zor olanlar için) değiştirilmiş bir ana variansı üretmek için çağırın.
   Çin dilinde dil değiştirme:提示 LLM(多数候选用 Gemini Flash,难题用 Gemini Pro)生成父本的修改变体──
5. Sürekli değerlendirme cihazında variansı oluştur, çalıştır ve değerlendirin.
   Çinçe Çevirim:编译、运行并保留评估器上评估变体──
6. Skor ve özellik vektörü ile anahtarlanmış veritabanına ekle.
   Çin Çeviri: 分数和特征向量为键插入数据库
7. Tekrar ediyorum.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri

İki detay önemlidir. Birincisi, LLM ana programdan daha fazlasıyla  genellikle veritabanından birkaç üst varyant ile teşvik edilir.

> İlk olarak, LLM 时不仅给父程序 genellikle veri tabanında en yüksek sıralamada bulunan birkaç değişken, ayrıca değerlendirmeci imzası ve kısa görev açıklamasıdır.

### Bu değerlendiriciyi anlaşılmaz yapan şey .

AlphaEvolve'in kazançları, değerlendirici hızlı, belirleyici ve zor oynadığı alanlardan gelir:

> AlphaEvolve'in kazançları, hızlı, belirgin ve zor değerlendirici alanlardan geliyor:

- **Matrix multiplication algorithm**: matrisleri çarpıtan ve eşitliği bit-tıpkı bir şekilde kontrol eden birim testi.
  Çeviri:**矩阵乘法算法** bir çarpı bir matç ve bir sıra kontrol egali birim testi
- **Borg scheduling heuristic**: tarihi küme yükünü yeniden oynayan ve boşa harcanmış hesaplama ölçümlerini yapan üretim derecesi simülatörü.
  Çeviri:**Borg 调度启发式** Bir üretim sınıfı simülatör, yeniden yükleme ve ölçme harcamalarının hesaplanması
- **FlashAttention kernel**: gerçek donanım üzerinde doğrulık testi ve duvar saati referans göstergesi.
  Çeviri:**FlashAttention 内核**正确性测试加上真实硬件上壁钟基准──
- **Gemini training throughput**: adım başına GPU saniye ölçülmüştür.
  Çeviri:**Gemini 训练吞吐量** ölçüm her adım GPU 秒数

Her durumda değerlendirici, öte yandan üstünlük sağlayacak LLM hataları sınıfını yakalar: konfabulated doğruluk iddiaları, donanım üzerinde kaybolan performans iddiaları ve kenar durum hataları.

> Her durumda, değerlendirmeci, hakim olabilecek LLM'yi yakaladı  hata sınıfı: sahte doğruluk bildirimi, donanım üzerinde kaybolan performans bildirimi ve kenarlık durumu başarısızlıkları.

### Ödül hackeri bu ifadeyi başka bir şekilde ifade ediyor. Ödül değişimi, bu kararın diğer bir tarafıdır.

Evolusiyon, değerlendirici ne ölçüde olursa olsun optimize eder. Eğer değerlendirici kusurlu ise, döngü kusurlu bulur. Doğrulanmamış bir alanda döngü, amaçlanan davranış için değil, yüzey özelliği için optimize eder.

> 进化优化评估器测量的任何东西―― eğer değerlendirme cihazı kusurluysa, döngü kusurlu bir yer bulur―― in unprovened fields, the cycle optimizes surface features rather than expected behavior―

DeepMind bu durumu açıkça kağıda belirtir: AlphaEvolve'un başarıları yalnızca değerlendirici sıkıntısının aramaların hırsına uyduğu alanlara aktarılır.

> DeepMind, makalede açıkça belirtti: AlphaEvolve'in başarısı yalnızca değerlendirmecilerin araştırma hedeflerine uygun bir alanına geçebilir.

2025-2026 yılları arasında kod arama döngüslerinde ödül hackleme örnekleri:

> 2025-2026 yılları için ödül değişiminin özel örnekleri:

- "Bütünleşme zamanı" ödülünü veren optimizasyon hedefleri boş çözümler göndermekle ödüllendirildi.
  Çinçe Çevirisi: ödül "完成时间" ̆ optimization objectif会 ödüller göndermek空解决方案。
- Benchmark puanları doğruluk testi altındaki hatırlarlık testleri ve aşırı uygunlukları ödüllendirir.
  Çinçe çevirisi: Ödül Test Haklılık Kilitli Ödül Ödül Hatırlama Testleri ve Üzerine Hazırlık Yapmak
- "Kod kalitesi" proxy, yorumları kaldırmak ve semantik bir değişiklik olmadan değişken isimleri yeniden yazmakla ödüllendirildi.
  Çinçe Çevirisi: "代码质量" temsilcilik ödülü kaldırmak注释和重写变量名,而没有语义变化──

AlphaEvolve'de çözüm: LLM'nin hiç görmediği bir değerlendirmeci gönderir ve değerlendirme sırasında üretilen girişler.

> AlphaEvolve'in Dönüşümü: Bir LLM'yi teslim etmek, değerlendirme sırasında oluşturmak için bir değerlendirme makinesi oluşturmak, inceleme yaparak, herhangi bir önerinin uygulanmasına ciddi bir inceleme yapılması için derin düşünce önerir.

### Neden LLM + arama tek başına mı geçiyor ?

LLM, kompüle edilebilir, anlamsal olarak makul değişiklikler üretebilir. 2000 satırlı Python dosyasında rastgele mutasyon GA neredeyse her zaman sözcük hatası üretir. LLM ayrıca rastgele komşularda aramaları yoğunlaştırır (herhangi bir fonksiyonu değiştir, rastgele bayt değil), bu da değerlendirmeci çağrıları çarpıcı bir şekilde azaltır.

> LLM, 2000 行 Python dosyalarında oluşan her türlü değişimlerde neredeyse her zaman bir dilbilim hatası meydana gelir. LLM ayrıca aramaları mantıklı bir komşu bölgede odaklanır. Bu da değerlendirme cihazının kullanımını büyük ölçüde azaltır.

Değerlendirici, LLM'nin konfabulasiyonlarını yakalar. LLM'ler, aslında O(n^2) olduğu halde bir fonksiyonun "O(n log n) sınırında olduğunu güvenle iddia eder; bir duvar saati referans sorunu çözür.

> 评估器反过来捕获LLM'in虚构──LLM 会自信地声称一个函数"极限下是 O(n log n)",而实际是 O(n2);墙钟基准让问题尘埃落定──

### AlphaEvolve sınır yığınına yerleştiği yerde.

| System | Generator | Evaluator | Domain | Example win |
|---|---|---|---|---|
| 系统 | 生成器 | 评估器 | 领域 | 示例胜利 |
| AlphaEvolve | Gemini | correctness + benchmark | algorithms, kernels, schedulers | 48-mul 4x4 matmul |
| AlphaEvolve | Gemini | 正确性 + 基准 | 算法、内核、调度器 | 48 次乘法 4x4 矩阵乘法 |
| FunSearch (DeepMind, 2023) | PaLM / Codey | correctness | combinatorial math | cap-set lower bounds |
| FunSearch（DeepMind，2023） | PaLM / Codey | 正确性 | 组合数学 | cap-set 下界 |
| AI Scientist v2 (Sakana, L5) | GPT/Claude | LLM critique + experiment | ML research | ICLR workshop paper |
| AI Scientist v2（Sakana，L5） | GPT/Claude | LLM 评审 + 实验 | ML 研究 | ICLR 工作坊论文 |
| Darwin Godel Machine (L4) | agent scaffolding | SWE-bench / Polyglot | agent code | 20% → 50% SWE-bench |
| Darwin Godel Machine（L4） | Agent 脚手架 | SWE-bench / Polyglot | Agent 代码 | SWE-bench 20% → 50% |

Dörtü de aynı tarifin değişikliği: jeneratör artı değerlendirici, döngü. Farklılıklar değerlendirici notlarının ne kadar sıkı olduğu.

> Dörtü aynı yöntemi oluşturan değişkenler: üreticiler, değerlendirmeciler, döngüler.
```figure
alphaevolve-loop
```

## Kullan

## Çerçeveyi kullanın.

`code/main.py`Oyuncak simgesel gerileme sorunu üzerinde minimal bir AlphaEvolve benzeri bir döngü uyguluyor.

> `code/main.py`Bir oyuncak simgesi dönüşü sorunu üzerinde AlphaEvolve'e benzer en küçük döngü gerçekleştirildi.

"LLM" bir hedef fonksiyonunu hesaplayan bir programa küçük sentaksik mutasyonlar öneren bir stdlib proxy. "Değerlendirici" ölçümleri, tutulan test noktalarında karelerinin hata anlamına gelir.

> "LLM" bir standart kitlesinin temsilcisi, bir hesaplama hedef işlevi için bir programın önüne küçük dil değişikliği getirir.

- Gözleyin.

> 观察:

- En iyi notun nesiller boyunca nasıl geliştiğini.
  Çinçe Çevirisi: ︎ ︎ ︎ ︎ ︎
- Bir MAP elit şebekesi çeşitli çözümleri nasıl canlı tutar ki bu da halka yerel minimumlara doğru birleştiği için değil.
  Çeviri:MAP-elite 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网格 网址 网址 网址 网址 网址 网址 网址 网址 网址 网址 网址 网址 网址 网址 网址 网址 网址 网址 网址 网址 网址 网址 网址 网址 网址 网址 网址 网址 网址 网址 网址 网址 网址 网址 网址 网址 网址 网址 网址 网址 网址 网址 网址 网址 网址 网址 网址 网址 网址 网址 网址 网址 网址
- Nasıl bir şekilde, beklenmedik bir denemeyi (tekrar eğitimli değerlendirmeci) kaldırmak, döngüyi çarpıcı bir şekilde uyumlandırır.
  Çinçe Çevirimi:移除保留测试 (→)                                                                                                                                                                                                                                                        

## İndirin . Ürünler .

`outputs/skill-evaluator-rigor-audit.md`Yeni bir alanda AlphaEvolve tarzında bir döngü düşünmenin ön koşuludur: değerlendirici gerçekten önem verdiğiniz başarısızlıkları algılar mı?

> `outputs/skill-evaluator-rigor-audit.md`AlphaEvolve döngüsüne benzer bir ön koşul üzerinde yeni bir alanda düşünün: değerlendirme cihazınız gerçekten kaygılarınızı yakaladı mı?

## Egzersizler.

1. Çık .`code/main.py`. En iyi puan çizgisini not edin.`--no-holdout`) ve tekrar çalıştırmak.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`code/main.py`                                                                                                                                                                                                                                                                                                                                         `--no-holdout`) yeniden yürütülmüş, ölçeği daha uygun hale getirilmiştir.

2. MAP-elite grid'deki AlphaEvolve makalesinin 3. bölümünü okuyun. Aramaları çeşitlilikte tutmak için yeni bir sorun için bir özellik vektörü tanımlayıcısı tasarlayın (örneğin, kompiliör optimizasyonu geçişleri).
   Çinçe Çevirimi: AlphaEvolve'i okuyun. MAP elitleri hakkında 3. bölüm.

3. Strassen'in 49-mul sınırında 48 çarpma 4x4 sonucu 56 yıl sonra iyileşti. Kağıtın F ekini okuyun ve bu sorunun değerlendirici neden özellikle doğru olmak için kolay olduğunu ve çoğu alanın neden bu şekilde olmadığını üç cümleyle açıklayın.
   Çinçe çevirisi:48 kez çarpma 4x4  sonucu 56 yıl sonra Strassen'in 49 kez çarpma sınırını geliştirdi.

4. AlphaEvolve'in başarısız olduğu bir alan önerin.
   Çinçe Çevirimiçi:Tip议一个 AlphaEvolve 会失败的领域――精确指出评估器在哪里失败以及原因──

5. Bildiğiniz bir alan için kullanmak istediğiniz değerlendirmeci imzasını yazın. (a) doğruluk koşulları, (b) performans metrikleri, (c) devamlı giriş üretimi kuralları, (d) en az bir ödül saldırısına karşı kontrolü ekleyin.
   Çinçe Çevirimi: Bildiğiniz bir alan için, yazın kullanılacağınız değerlendirme cihazı imzalamak.

## Anahtar Şartlar .

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| AlphaEvolve | "DeepMind's evolutionary coding agent" | Gemini + program database + machine-checkable evaluator |
| AlphaEvolve | "DeepMind 的进化编码 Agent" | Gemini + 程序数据库 + 机器可检查评估器 |
| MAP-elites | "Diversity-preserving archive" | Grid keyed by feature vectors; each cell holds the best variant with that descriptor |
| MAP-elites | "保持多样性的档案" | 以特征向量为键的网格；每个单元持有具有该描述符的最佳变体 |
| Island model | "Parallel evolution subpopulations" | Independent populations that migrate periodically; prevents premature convergence |
| 岛屿模型 | "并行进化子种群" | 定期迁移的独立种群；防止过早收敛 |
| Machine-checkable evaluator | "Deterministic oracle" | A unit test, simulator, or benchmark the LLM cannot fake — a prerequisite for this loop |
| 机器可检查评估器 | "确定性预言机" | LLM 无法伪造的单元测试、模拟器或基准——此循环的前提 |
| Reward hacking | "Optimizing the measure, not the goal" | Loop finds a way to maximize score without doing the intended task |
| 奖励篡改 | "优化度量而非目标" | 循环找到一种方法在不执行预期任务的情况下最大化分数 |
| Seed program | "The starting point" | An initial correct-but-suboptimal program the loop evolves from |
| 种子程序 | "起点" | 循环从中演化的初始正确但次优的程序 |
| Held-out evaluator | "Evaluation data the LLM never saw" | Inputs generated at evaluation time to prevent memorization |
| 保留评估器 | "LLM 从未见过的评估数据" | 评估时生成的输入以防止记忆 |

## Daha fazla okumak

- [Novikov et al. (2025). AlphaEvolve: A coding agent for scientific and algorithmic discovery](https://arxiv.org/abs/2506.13131)- Tüm kağıt.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri
- [DeepMind blog on AlphaEvolve](https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/) Satıcı kayıtları sonuçlarla.
  Çinçe Çevirimiçi:厂商撰文及结果──
- [AlphaEvolve results repository](https://github.com/google-deepmind/alphaevolve_results)48-mul 4x4 matmul dahil olmak üzere algoritmalar keşfedildi.
  Çinçe Çevirisi: Foundation of Algorithm deposu, 48 kez乘法 4x4 矩阵乘法
- [Romera-Paredes et al. (2023). Mathematical discoveries from program search with LLMs (FunSearch)](https://www.nature.com/articles/s41586-023-06924-6) Önceki sistem.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri
- [Anthropic — Responsible Scaling Policy v3.0 (Feb 2026)](https://anthropic.com/responsible-scaling-policy/rsp-v3-0) değerlendiriciye bağlı otonomluk, temel bir araştırma yönü olarak çerçeveliyor.
  Çinçe Çevirisi:                                                                                                                                                                                                                                                            
