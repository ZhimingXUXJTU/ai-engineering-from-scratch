# Zihn Teorisi ve Çözüm Koordinasyonu

> Li et al. (arXiv:2310.10701) ortak bir metin oyun sergisinde LLM ajanlarının **emergent high-order Theory of Mind**(ToM)  bir üçüncü ajanın inançları hakkında başka bir ajanın ne düşündüğünü düşünmek  ancak bağlam yönetimi ve halüsinasyon nedeniyle uzun vadede planlamayı başarısız etmek. Riedl (arXiv:2510.05174) bir popülasyonda daha yüksek sıralama sinerjisi ölçtü ve buldu ki **only**ToM-prompt koşulı kimlik bağlantılı farklılık ve hedef odaklı tamamlayıcılık üretir; düşük kapasiteli LLM'ler sadece sahte ortaya çıkış gösterir. Yani, koordinasyon ortaya çıkışı, serbest değil, derhal koşullu ve model bağımlıdır. Bu ders, minimal bir ToM-a karşı bilinçli ajan uyguluyor, ToM'nin teşvik edilmesiyle ve olmadan işbirliği görevini yürütüyor ve Riedl 2025 protokolüne karşı koordinasyon delta ölçüyor.

> **【中文解读】**Bu bölümde, akıl teorisi koordinasyonunun ajanı anlama ve öngörme diğer ajanın niyetinin koordinasyon mekanizması hakkında bilgi edindiler.

> **【拓展：theory of mind coordination→具体应用】**心の理論 (心智理論) (Akıl Teorisi) başkalarının psikolojik durumlarını anlama ve tahmin etme yeteneğidir. 複数の Ajan システムの中で, 心の理論を持つ Ajan 能更好地協調 它知道其他 Ajan 知道什么、想要什么、会做什么──2025-2026 yıllarındaki araştırmalar, diğer Ajanların niyetlerinin koordinasyon verimliliğini önemli ölçüde artırabileceğini, ancak aynı zamanda hesaplama maliyetlerini de artırabileceğini göstermektedir.


**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib) | **语言:** Python（标准库）
**Prerequisites:** Phase 16 · 07 (Society of Mind and Debate), Phase 16 · 17 (Generative Agents) | **前置知识:** Phase 16 · 07（心智社会与辩论），Phase 16 · 17（生成式 Agent）

>  **【前置】**Öğrenci: Önemli bir konu. Önemli bir konu.
>  **【类比】**ToM = "Agent'in ortak fikri"──无 ToM Agent = 自言自话;有 ToM Agent = 站在对方角度思考" o, bu şeyi biliyor mu?高阶 ToM = 嵌套推理?
**Time:** ~75 minutes | **时间:** ~75 分钟

## Sorunlar sorunun giriş

Çoklu ajan koordinasyonu genellikle büyülü görünüyor: ajanlar iş gücü bölüşür, birbirlerini öngörür, boşaltmayı önler. Genellikle bu "gelen" bir an önce mühendisliği eseri  birisi ajanlara "koordinasyon" yapmaları için söyledi.

> Çoğu ajan  koordine genellikle çok garip görünüyor: ajan bölünmüş, birbirini öngörmüş, eksikliği önlemiş. Genellikle bu tür "gelenekler" bir proje ürünüdür.

Riedl'in 2025 bulguları daha sıkıdır: kontrol edilen koşullarda, koordinasyon sadece ajanların hakkında düşünmeye teşvik edildiğinde ortaya çıkar **other agents' minds**(ToM). ToM uyarısı olmadan, güçlü modeller bile istatistik kontrollerden geçmeyen koordinasyon kalıplarını gösterir. Bu üretim için önemlidir: ekipler, hız bağımlı ve kırılgan "çok ajan koordinasyonu" özelliklerini gönderir.

> Riedl 2025'in bulguları daha sıkı: kontrol altında, koordinasyon sadece ajan tarafından önerilmektedir**其他 Agent 的心理**(ToM) zamanında ortaya çıkıyor. ToM 提示 yok, güçlü modeller bile statistik kontrol altında mevcut olmayan koordinasyon modeli göstermektedir.

Bu ders ToM'ye belirli bir yetenek olarak bakıyor (inanışlar hakkında düşünme), minimal bir ToM-a karşı farkında bir ajan oluşturur ve gerçek koordinasyonun neye benzediğini vs. hızlı giyinmenin neye benzediğini ölçüyor.

> Bu ders, ToM'yi belirli bir yetenek olarak görecek, inanç hakkında inançlar üzerinde düşünerek, en küçük ToM'yi algılama ajanını oluşturarak, gerçek koordinasyon ve öneriler arasında farkı ölçerek.

## Konsept merkezi konsept

### ToM'in anlamı

Gelişme psikolojisi: 3 yaşındaki bir çocuk, herkesin iç dünyası onlarınkiyle eşleşir diye düşünüyor. 5 yaşındaki bir çocuk başkalarının farklı inançlara sahip olduğunu anlıyor. 7 yaşındaki bir çocuk inançlar hakkında inançlar hakkında nedenler ("topun fincanın altında olduğunu düşünüyorum") düşünüyor. Bunlar zeroth, birinci ve ikinci sıradaki ToM.

> 发展心理学:3 岁的孩子认为任何人的内心世界与自己相同――5 岁的孩子理解他人有不同的信仰――7 岁的孩子推理关于信仰的信念――"O, topun kafenin altında olduğunu düşünüyorum"――这些是零阶段,一阶段和二阶段 ToM──

LLM ajanları için ToM, haritasını:

> LLM Ajanı için:

- **Zeroth-order:**Ajan sadece kendi gözlemlerine dayanarak hareket eder.
  Çeviri:**零阶：**Başkalarının modeli yok. Ajan sadece kendi gözlemlerine göre hareket eder.
- **First-order:**"Alice X'e inanıyor".
  Çeviri:**一阶：**Ajanın diğer Ajanların inançlarına bir örneği var.
- **Second-order:**"Alice Bob'un X'e inandığına inanıyor".
  Çeviri:**二阶：**Ajan, Alice, Bob'u, X'i, inanıyor.

Li ve diğerleri 2023'te ilk ve ikinci sıradaki ToM'nin kooperatif oyunlarda LLM ajanlarında ortaya çıktığını ancak uzun ufaklık ve güvenilir olmayan iletişim ile düştüğünü buldular.

> Li 等人 2023 yılında ilk ve ikinci aşamada ortak oyunlarda LLM ajanı ortaya çıkmış, ancak uzun süreli ve güvenilir olmayan iletişimde geri dönüşmüştür.

### Sally-Anne testi, kısaca

Bir 1985 sahte inanç testi: Sally bir mermer kuruşuna A koyup ayrılır. Anne onu kuruşuna B'ye taşır.

> 1985 yılının yanlış inanç test: Sally Balge Bear'ı Basket A'da, Leave.Anne Balge Bear'ı Basket B'ye taşıdı. Sally Geri dönüp nerede bulur?

GPT-4 dönemindeki LLM'ler açıkça ortaya koyduğunda Sally-Anne tarzı testlerini geçiyor. Hikaye uzun olduğunda, sahne birkaç kez değişirken veya soru dolaylı olarak ifade edildiğinde başarısız olurlar.

> GPT-4 时代的LLM 在直接提问时通过Sally-Anne 风格测试──当叙述长,场景多次变化或问题间接表达时失败──这是2026年生产LLM 中 ToM 的实际状态──

### Riedl'in koordinasyon ölçümü

Riedl (arXiv:2510.05174) nüfus ölçeğinde bir test inşa etti: N ajanlar, işbirliği amacı, değişken acil koşullar.

> Riedl(arXiv:2510.05174) oluşturmuş grup ölçeği test:N 个 Agent,合作目标,可变提示条件──测量:

1. **Identity-linked differentiation.**Ajanlar zamanla sabit rol ayrımları geliştiriyor mu?
   Çeviri:**身份关联分化。**Ajanın zamanla gelişmesi için bir rol ayırt ediliyor mu?
2. **Goal-directed complementarity.**Ajanların eylemleri birbirlerini (farklı alt görevler) ikili değil tamamlıyor mu?
   Çeviri:**目标导向互补性。**Ajanın davranışları tekrarlanmamış bir şekilde tamamlanmalı mıydı?
3. **Higher-order synergy.**Bir grupun hiçbir alt kümenin başaramadığı bir şeyi elde edip etmediğinin istatistiksel bir ölçüsü.
   Çeviri:**高阶协同。**群体是否达到任何子集都无法达到的统计量量──

Sonuç: sadece ToM istek koşulunda üç metrik de başlangıç hattından yukarı sinyal üretir. ToM isteksiz, ölçüler orta kapasiteli modeller için şansın yakınında kalır. Büyük modeller açık ToM isteksiz bir koordinasyonu gösterir, ancak etki açık isteksiz olmaktan daha küçüktür.

> Sonuç: Sadece ToM 提示 koşullarında, üç gösterge sadece temel çizgiden yüksek sinyal üretir. ToM 提示 olmadan, orta yetenek modelinin göstergesi herhangi bir seviyede ︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-︎-

### Koordinasyon yanılsısı

İstatistik kontroller olmadan, gösterilerdeki "özel koordinasyon" genellikle:

> 没有统计控制,演示中的"涌现协调" genellikle şunları yansıtır:

- Koordinasyonda pişirilen hızlı mühendislik (sistem uyarıları "birlikte çalışın" diyor).
  Çinçe Çevirimiçi:嵌入协调的提示工程(系统提示说"一起工作")
- Gözlemci tarafsızlığı (bunu beklediğimiz kalıpları görüyoruz).
  Çinçe Çevirimiçi: observer偏差 (),
- Başarılı koşular için post-hoc seçimi.
  Çöntem: Başarılılık, başarının ardından seçim.

Ölçülebilir sinyal olmadan "daha gelişmiş koordinasyon" pazarlanan üretim sistemleri pazarlama olarak değerlendirilmelidir.

> 没有可测量信号就宣传"涌现协调"in üretim sistemi, satış olarak görülmelidir.

### En az bir ToM-bilgili ajan.

Yapı:

```
agent state:
  own_beliefs:    {facts the agent believes}
  other_models:   {other_agent_id -> {beliefs_the_agent_attributes_to_them}}
  actions_last_N: [history of others' actions]

observation update:
  - update own_beliefs from direct observation
  - update other_models[agent_id] from their action + prior beliefs

action selection:
  - enumerate candidate actions
  - for each, predict what each other agent will do next given their modeled beliefs
  - pick action that maximizes joint outcome under those predictions
```

- Evet .`other_models`Birinci sırada ToM sadece bir seviyeyi korur.`other_models[i][other_models_of_j]`- Bence Ajan J'nin inandığını düşünüyorum.

### Neden uzun uzayda acı çekiyor?

Li et al. belge: bağlam sınırları ajanların kime ait olduğunu unutmalarına neden olur. Halüsinasyon diğer ajan modelleri için yanlış inançlar ekler. Her ikisi de zamanla karmaşan "X'yi sandım" hataları üretir.

Raporda belgelenmiş hafiflemeler ve 2024-2026 yıllarındaki takipler:

- **Explicit ToM state in the prompt.**Yapılandırılmış format: `{agent_id: belief_list}`Kimlik-için bağını korumak için geri almayı zorlar.
- **Shorter reasoning chains.**Her seferinde daha az ToM güncellemesi bileşik halüsinasyonları azaltır.
- **External ToM store.**Modelli LLM bağlamının dışında tutun; her turda sadece ilgili parçalar enjekte edin.

### ToM'nin üretiminde başarısız olduğu durumlarda

- **Adversarial settings.**İyi ToM'li ajanlar manipüle edilmesi daha kolaydır (senden model olduklarını modelleyebilir, sonra da sömürülebilirsin).
- **Heterogeneous teams.**Modeller farklı olduğunda, bir rakip için çalışan ToM modeli genelleştirmez.
- **Ground-truth-dependent tasks.**ToM inançlarla ilgilidir; eğer doğruluk gerçeklere bağlıysa, ToM dikkat dağıtıcı olabilir.

### Gerçekten ölçülebilecekleri koordinasyon

Takımın koordinasyonu, hemen giyinmek yerine gerçek olduğunu gösteren üç pratik sinyal:

1. **Complementarity over time.**Bir çok dönüşlü görevde, ajanların eylemleri ayrı alt görevleri kapsar mı?
2. **Anticipation.**T+1'deki A ajanının eylemleri doğru olan T+2'deki B'nin eylemleri hakkında bir tahminden mi bağlı?
3. **Correction.**A, T'de B'nin inancını yanlış anladığında, A, T+2'de doğru mu?

Bunlar kayıtlı bir çok ajan sisteminde ölçülebilir. "Koordinasyon" anlatısının içsel versiyonudur.

## Yapın.
```figure
sw-theory-of-mind
```

## Yapın

`code/main.py`Uygulamaları:

- `ToMAgent` kendi inançlarını ve diğer ajan inanç modellerini takip eder.
  Çeviri:`ToMAgent`Kendi inançlarını ve diğer ajanların inanç modellerini takip et.
- Bir işbirliği görevi: üç ajan üç kutudan üç token toplamalıdır; her kutu bir token tutabilir.
  Çinçe Çevirisi:合作任务:三个代理 必须从三个盒中收集三个代币;每个盒只能放一个代币――Agent 不能通信;它们从彼此的行为推断意图――
- İki yapılandırma: `zeroth_order`(ToM yok) ve `first_order`(Bir düzeyde inanç modeli ile ToM).
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`zeroth_order`(Barsı)`first_order`(带一层信念模型的 ToM)
- 200 randomisasyonlu çalışmanın ölçümü: tamamlama oranı, çoğaltma oranı (iki ajan aynı kutuyu hedef alan), ortalama dönüş tamamlanmaya kadar.
  Çinçe Çevirimi:200 次随机试验的测量:完成率、重复率(iki ajan 准同一个盒) 、平均完成轮次。

Çık:

```
python3 code/main.py
```

Beklenen çıkış: sıfır sıra ajanları %35 oranında çabaları ikiye katlar ve 10 dönüşte denemelerin %60'ını tamamlar.

> 预期输出:零阶级代理以约35%的比例重复工作和10轮内完成约60%的试验──一阶级TM代理以约5%的比例重复并完成约95%──差异就是可测量的协调效果──

## Kullanın Kullanın

`outputs/skill-tom-auditor.md`Bir çok ajanlı sistemin "daha gelişmiş koordinasyon" iddiasını denetleyen bir beceri.

> `outputs/skill-tom-auditor.md`Bu, bir kontrol örgütü ile karşılaştırıldığında, bir kontrol örgütü ile karşılaştırıldığında, bir kontrol örgütü ile karşılaştırıldığında, bir kontrol örgütü ile karşılaştırıldığında, bir kontrol örgütü ile karşılaştırıldığında, bir kontrol örgütü ile karşılaştırıldığında, bir kontrol örgütü ile karşılaştırıldığında, bir kontrol örgütü ile karşılaştırıldığında, bir kontrol örgütü ile karşılaştırıldığında, bir kontrol örgütü ile karşılaştırıldığında, bir kontrol örgütü ile karşılaştırıldığında, bir kontrol örgütü ile karşılaştırıldığında, bir kontrol örgütü ile karşılaştırıldığında, bir kontrol örgütü ile karşılaştırıldığında, birleştirildiğinde, birleştirildiğinde, birleştirildiğinde, birleştirildiğinde, birleştirildiğinde, birleştirildiğinde, birleştirildiğinde, birleştirildiğinde, birleştirildiğinde, birleştirildiğinde, birleştirildiğinde, birleştirildiğinde, birleştirildiğinde, birleştirildiğinde, birleştirildiğinde,

## Gönderin.

Koordinasyon taleplerinin kontrol listesini:

- **Control condition.**Koordinasyon sorusu olmadan sisteminizin bir versiyonu.
  Çeviri:**对照条件。**没有协调提示的系统版本──两者都测量──
- **Statistical test.**Sistem ve kontrol arasındaki fark önemli mi ?`p < 0.05`- Metriklerinize göre mi?
  Çeviri:**统计测试。** Sistem ve                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `p < 0.05`- Görkemli mi?
- **Complementarity measure.**Zamanla hareket-karşılaşma, sadece son başarı değil.
  Çeviri:**互补性测量。**Zamanla hareketler, sadece sonuçta başarılı değil.
- **Failure-case log.**Ajanlar yanlış koordinasyon yaparken, ToM eyaleti nasıl görünür?
  Çeviri:**失败案例日志。**Ajan başarısız olduğunda, durumun nasıl olurdu?
- **Model-capacity disclosure.**Eğer daha küçük modellerde etkisi kaybolursa, söyle.
  Çeviri:**模型能力披露。**Eğer daha küçük bir modelde sonuçlar kaybolursa, bunu açıklayın.

## Egzersizler.

1. Çık .`code/main.py`İlk sıralama ToM'nin kopyalama oranını 7 kat azaltmasını onaylayın. 5 ajan ve 5 kutuya kadar ölçeklendirdiğinizde boşluk devam ediyor mu?
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`code/main.py`❖ Bir aşamada tekrar oranının 7 katı düşeceğini doğrula. 5 Ajan ve 5 kutu zaman farkı hâlâ var mı?
2. İkinci sıradaki ToM uygulaması (Agent A, B'nin C'ye ne düşündüğünü modellemektedir).
   Çinçe Çevirimi: A A A A A A B C'nin düşüncelerini gerçekleştirmek için.
3. Bir **hallucination**Bu, birinci sıradaki performansı ne kadar düşürüyor?
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri**幻觉**Bu bir aşama performansını ne kadar düşürecek?
4. Li et al. (arXiv:2310.10701). "Uzun ufuk degradasyonu" bulgularını yeniden üretin: dönüşler 10'dan 30'a kadar arttıkça, ilk sıra ToM performansınız nasıl değişiyor?
   Çine dilinde: Li 等人 ([[arXiv:2310.10701) ]]: Repeat "长期退化" keşif:当轮次10 增长到30 时,你的一阶 ToM 性能如何变化?
5. Riedl 2025 (arXiv:2510.05174) okuyun. Simülasyon günlüğünüzde yüksek sıralama sinerji istatistiklerini uygulayın.
   Çin Çeviri: Ridel 2025: arXiv: 2510.05174)

## Anahtar Terimler

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Theory of Mind / 心智理论 | "Understanding others' minds" / "理解他人的心理" | The capacity to model another agent's beliefs. Graded by order (0, 1, 2+). / 建模另一个 Agent 信念的能力。按阶次分级（0, 1, 2+）。 |
| Sally-Anne test / Sally-Anne 测试 | "The false-belief test" / "错误信念测试" | 1985 developmental psychology; LLMs pass plain versions, fail complex ones. / 1985 年发展心理学；LLM 通过简单版本，复杂版本失败。 |
| First-order ToM / 一阶 ToM | "A believes X" / "A 相信 X" | Modeling one other's beliefs about facts. / 建模另一个关于事实的信念。 |
| Second-order ToM / 二阶 ToM | "A believes B believes X" / "A 相信 B 相信 X" | Recursive modeling one level deeper. / 递归建模更深一层。 |
| Identity-linked differentiation / 身份关联分化 | "Stable roles over time" / "稳定的角色" | Riedl's metric: roles persist, not random. / Riedl 的指标：角色持续而非随机。 |
| Goal-directed complementarity / 目标导向互补性 | "Disjoint actions" / "不交动作" | Agents target different subtasks, not the same one. / Agent 瞄准不同子任务，不是同一个。 |
| Higher-order synergy / 高阶协同 | "Group exceeds any subset" / "群体超越任何子集" | Riedl's statistical measure for real coordination. / Riedl 对真正协调的统计度量。 |
| Coordination illusion / 协调幻觉 | "It looks coordinated" / "看起来协调" | Prompt-dressed appearance of coordination without measurable signal. / 没有可测量信号的提示装饰的协调外观。 |

## Daha fazla okumak

- [Li et al. — Theory of Mind for Multi-Agent Collaboration via Large Language Models](https://arxiv.org/abs/2310.10701) Kooperatif oyunlarda yeni gelişen ToM; uzun uzayda başarısızlık modları
- [Riedl — Emergent Coordination in Multi-Agent Language Models](https://arxiv.org/abs/2510.05174) Popülasyon ölçeğinde ölçüm; ToM uyarı yük taşıma koşuludur
- [Premack & Woodruff — Does the chimpanzee have a theory of mind?](https://www.cambridge.org/core/journals/behavioral-and-brain-sciences/article/does-the-chimpanzee-have-a-theory-of-mind/1E96B02CD9850E69AF20F81FA7EB3595) ToM kavramının 1978'deki kökeni
- [Baron-Cohen, Leslie, Frith — Does the autistic child have a theory of mind?](https://doi.org/10.1016/0010-0277(85)90022-8)  Sally-Anne makalesi (1985)
