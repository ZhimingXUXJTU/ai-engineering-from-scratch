# Zihn Topluluğu ve Çok Ajan Tartışmaları .

> Minsky'nin 1986'daki önemi  zeka uzmanların bir toplumu  her on yılda yeniden keşfedilmektedir. 2023'te Du et al. onu bir somut algoritma haline getirdi: birden fazla LLM örneği cevaplar önerir, birbirlerinin cevaplarını okuyor, eleştirir ve güncelleir. N tur boyunca sıfır çekim CoT'yi yenen bir fikir birliği üzerine toplanır ve altı akıl ve gerçeklik görevleri üzerinde düşünme. İki bulgu önemlidir: her ikisi de **multiple agents**ve **multiple rounds**Toplum tek ajanlı bir monologtan, çok yönlü bir değişim tek atışla oy kullanmaktan daha iyidir.

> **【中文解读】**Bu bölümde, Marvin Minsky'nin "Akılcılık ve Sosyal Devamı" teorisinin çoklu ajanlar sistemindeki uygulanması ele alınıyor.

> **【拓展：society of mind debate→具体应用】**Marvin Minsky'nin 心智社会 (心智社会) (1986) fikri, zekiliği birçok basit zekilik ile işbirliği ürünü olarak ortaya koydu. Bu düşünce, 2026 yılında çoklu ajanlar 辩论 sisteminde  çoklu ajanlar  farklı açılardan tartışılan sorulara ulaşmak için daha iyi sonuçlar elde etmek için yapılan bir araştırma, 3-5 ajanların tartışmasının en iyi etkisini gösterdi.


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 16 · 04 (Primitive Model) | **前置知识:** Phase 16 · 04 (Primitive Model)
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**学本节前请先掌握:Phase 16·04(原语模型)、Phase 13·01-03(CoT 推理)。Minsky 心智社会理論 + LLM 辩论算法。
>  **【类比】**Çoğu Agent 辩论 = "学术同行评审"。单 Agent = 一个作者写论文(容易自但片面);多 Agent 辩论 = 多位审稿人 + 作者多轮回应,最终共识更稳健。Du et al. 2023 证明:多 Agent + 多轮独立贡献提升不是简单加法,是协同效应──3-5 个 Agent 最优(多多多了反而成一团)。

## Sorunlar sorunun giriş

Kendi kendine tutarlılık  bir modelin birçok kez örnek alın ve çoğunlukla yanıt alın  en ucuz mantık geliştirme.

> Özüm uyumluluk  bir model için çok defa örnekleme ve çoğunlukla cevap alınması  ekleyebileceğiniz en ucuz düşünce geliştirme ıdır.

Doymuşluk ilişkili hatalardan kaynaklanır: aynı model aynı şekilde başarısız olma eğilimindedir. Her örnek aynı kör noktayı paylaşırsa daha fazla örnek almak işe yaramaz. Tartışma, anlaşmazlıklarla yüzleşmek için ajanları zorlayarak ilişkiyi kırar.

> 和来自相关错误:相同模型倾向于以同方式失败──如果每个样本共享相同盲点,更多样本没有帮助──辩论通过强迫代理 面对分歧打破相关性──

Tartışma doymayı bozar. Bir modelden N bağımsız örneklerin yerine, N ajanlar birbirlerinin mantıklarını okuyor ve gözden geçiriyor. Örnekler arasındaki ilişki düşüyor ( artık id değiller), ve id oylamalarının güvenle yanlış olduğu bir şekilde doğru olan bir dönüş noktası genellikle doğru olur.

> Debat 和──'ı kırıyor. Bir modelden N 个独立样本 elde etmemek, N 个代理ı birbirinin düşüncelerini okumaya ve değiştirmeye çalışmak yerine 个代理ı 阅读彼此的推理和修改──样本之间的相关性下降了(它们不再独立和分布的),收点通常正确,而独立与分布的投票则在自信地犯错──

Bu ilişki mekanizmadır.Agentler diğer ajanların mantıklarını gördüğünde, ya pozisyonlarını savunmak ya da güncelleştirmek için onlarla uğraşmaktan başka bir şey yapamazlar.Bu zorla uğraşmak, hiçbir miktarda örnekleme yapamayacağı bilgiyi üretir.

> Bu mekanizma ilişkin olarak, ajan diğer ajanların önerilerini gördüğünde, kendi konumunu savunmak veya yenilemek için katılmak zorunda kalır. Bu zorunlu katılım herhangi bir sayıda bağımsız ve dağılımlı bilgi üretmek için hiçbir şekilde üretilemez.

## Konsept merkezi konsept

### Du et al. 2023 algoritması

ArXiv:2305.14325 (ICML 2024):

> ArXiv:2305.14325 (ICML 2024)'den:

Algoritm kasıtlı olarak basit: özel roller, yargıçlar, moderatörler yok. Her ajan simetriktir. Tek asimetri, önce kimin konuştuğunun sırasıdır ve hatta bu da birden fazla turda yıkayarak gider.

> Algoritme basit: özel rol yok, yargıç yok, yöneticisi yok. Her ajanın birbiriyle karşılaştırılması gerekir.

1. N ajanların her biri soruya ilk bir cevap verir.
   Çin Çeviri:Agentler, kendi başlarına ortaya çıkan sorulara ilk cevaplar verir.
2. Ronde r = 2..R için: her ajan diğer ajanların r-1'li grup cevaplarını gösterir ve "buları göz önünde bulundurarak, güncellenmiş cevapınızı verin" sorulur.
   Çin Çeviri: için第 r = 2..R 轮: Her ajan diğer ajanı görse 第 r-1 轮'ın yanıtını ve " bunları düşün, yeni yanıtını ver" soruldu.
3. R turlarından sonra, son cevapları çoğunlukla oylayın.
   Çinçe Çevirisi:R 轮后, son cevap için çoğunlukla oy kullanılmıştır.

MMLU, GSM8K, biyografiler, MATH ve gerçeklik referansları üzerine yapılan kağıt testleri.

> 论文在 MMLU、GSM8K、传记、MATH 和事实性基准上测试──辩论持续优于CoT 和自我反思──

Benchmark Suite hem mantıklama (MATH, GSM8K  doğru cevaplarla sorunlar) hem de gerçeklik (biografi  Wikipedia'ya karşı kontrol edilebilir iddialar) kapsamaktadır.

> 基准套件涵盖推理(MATH、GSM8K有可验证正确答案问题) 和事实性(传记可对照维基百科 检查的声明) ⋅事实性增益是标题结果:辩论是减少事实性问题幻觉的已知最便宜方法──

### İki bağımsız düğüm

Aynı kağıttan alınan ifadeler:

> Aynı bir makale için:

- **Agent count alone**Bir turda, N'nin çoğunluğu oy kullanır.
  Çeviri:**仅 Agent 数量**(1 ronde,N'in çoğunluğu oy verdi) Büyük çoğunluk görevleri tek Ajan'dan iyidir, ama platform'a ulaşır.
- **Round count alone**(Önce düşüncelerini gören 1 ajan)  refleksiyonun bilinen zayıflığını zor yardımcı olur.
  Çeviri:**仅轮数**(1 ajan kendi öncesinden bir düşünceyi görüyor) neredeyse hiç yardımcı olmadı. Bu düşüncenin bilinen bir zayıflığı.
- **Both together**Çoklu ajanlar arasındaki çoklu değişim kazancı artırır.
  Çeviri:**两者结合** büyük bir artış oluştu.  Birçok Ajan arasındaki çoklu değişim kazançlara yol açtı.

### Neden işe yarıyor?

İki mekanizma:

> İki mekanizma:

İki mekanizma bileşiktir: anlaşmazlığa maruz kalmak yeni bilgi sağlar; korellemeden yapılan hatalar yeni bilgilerin yanlış cevaplara ortalama olarak değerlendirilmesini engeller.

> 两个机制复合:暴露于分歧提供新信息;去相关错误防止新信息被平均到错误答案中;;单独任一比两者结合弱;;

1. **Exposure to disagreement.**Bir ajan başka bir ajanın akıl zincirini farklı bir sonuca çıkarırken, ya haklı çıkarmak ya da güncellemek zorunda kalır. Her iki durumda da, yuvarlak r + 1 için bağlam yuvarlak r'den daha zengindir.
   Çeviri:**暴露于分歧。**Bir Ajan başka bir Ajanı gördüğünde farklı sonuçlara sahip bir düşünce zinciri vardır, bu da ya kanıtlamak ya da yenilemek gerekir.
2. **Correlated error reduction.**Kendi kendine tutarlılık, tüm örnekler aynı modelden gelir, bu nedenle hatalar  güvenle yanlış bir cevap olarak ortalama ilişkilendirir. Farklı modeller veya farklı tohumlar ilişkilendirmeyi bozar. Farklı * tartışılmış görüşler* daha da ilişkilendirmeyi bozar.
   Çeviri:**相关错误减少。**Kendiliğinden uyum içinde, tüm örnekler aynı modelden gelir, bu yüzden yanlış ilişkilendirilmiş  ortalama bir güvence yanlış cevap elde edilir  farklı model veya farklı tür ilişkilendirilebilir  farklı* tartışmalar görüşleri* daha fazla ilişkilendirilebilir 

### Çeşitli tartışma

A-HMAD ve ilgili takipler farklı ajanlar için *farklı temel modeller* kullanır. Llama + Claude + GPT tartışması, monokultur çöküşünü azaltır (Denevi 26) çünkü bir model ailesinin ilişkili hataları diğerleri tarafından paylaşılamıyor.

> A-HMAD 和相关后续工作为不同 Agent 使用*不同的基础模型*──Llama + Claude + GPT 辩论减少了单一文化崩(Lesson 26),因为一个模型族的相关错误不被其他模型族共享────

Hata-decorrelation argümanı klasik ML'deki ansambl yöntemlerinin arkasındaki aynıdır: çeşitli modeller farklı şekilde başarısız olur, bu nedenle oylama daha güvenilirdir.

> 错误去相关论点与经典 ML 中集成方法背后的相同:多样化模型以不同方式失败,因此投票更可靠──问题是多样性昂贵(三份API 账单而不是一) 且收益在 3-4模型族后快速和──

Yanlış taraf: bir tartışmalara katılan zayıf bir model, konsensüzi yanlış cevabına doğru sürükleyebilir (bakın "Çılgınlık yapmalı mıyız?", arXiv:2311.17371).

> 缺点: bir tartışmaya katılan zayıf model, kendi yanlış cevaplarına doğru çekilip çekilebilir.

Heterogen tartışma özgür çeşitlilik değildir. Zayıf bir model (değil ki, 7B parametresi Llama) güçlü bir modelden (GPT-4) daha fazla oy alabilir, eğer güçlü model zayıf modelin güvenli yanlış cevaplarına karşı çok agresif bir şekilde güncelleyebilir. Katılımcı modellerin kalibrini yapın.

> 异构辩论不是免费多样性──弱模型(如 7B 参数 Llama) 可以否决强模型(GPT-4), eğer强模型过激进地向弱模型的自信错答案更新──校准哪些模型参与──

### NLSOM  129-Agent uzantısı

Zhuge et al. ("Doğal Dil Temelindeki Zihn Toplumlarında Zihn Fırtınaları", arXiv:2305.17066) bu fikri 129 üye topluma kadar ölçeklendirdi. Sonuç: uzmanlık ve kendi kendini organize etmek ölçekle ortaya çıkıyor ve sistem görsel soru cevaplama gibi görevlerde tek ajanı üstlenmektedir.

> Zhuge 等人 ((("Based on Natural Language的心智社会中的思维风暴",arXiv:2305.17066) bu fikri 129 成员社会に拡大する. Sonuç: uzmanlaşım ve kendi kendini organize etmek, sistemlerde görsel soru ve cevaplar gibi görevlerde tek bir Ajanın üstünlüğünü kazanmak.

Skalalama sonucu çarpıcıdır: ~ 50 ajanın ardından, bireysel roller, kendilerine söylenmeden uzmanlaşmaya başlar. Bazıları " araştırmacılar, " bazıları " eleştirmenler, " bazıları " sentezciler " olur. " Bu yeni ortaya çıkan rol ayrımı  insan organizasyonlarında görülen aynı fenomen, şimdi LLM toplumlarında gerçekleşmektedir.

> 扩展结果引人注目: Yaklaşık 50 ajanın ardından, bireysel roller, bilinmeyen durumlarda uzmanlaşmaya başladı. Bazıları "dahasçılar"、 diğerleri "tanıkcılar"、 diğerleri "kompleksörler" olarak çevrildi.

### Başarısızlık modları

- **Sycophancy cascade.**Tüm ajanlar en güvenli olan ajanı tercih eder. Tartışma en yüksek sesle çöker. Karşılıklı roller için teşvik ("bir ajan karşı pozisyonu tartışmalıdır") yardımcı olur.
  Çeviri:**谄媚级联。**Bütün Ajan 屈服于听起来最自信的代理──辩论崩为最大声音──对抗角色的提示──"Bir Ajan 必须论证反方立场") yardımcı olmak──
- **Topic drift.**Birçok tur boyunca tartışmalar orijinal sorudan uzaklaşır.
  Çeviri:**主题漂移。**Douroule Debate Orijinal Sorunlardan Ayrılıklı Olmak: Her Runde Yeniden Sorunlara Uçuş
- **Compute blowup.**N ajanlar x R turlar = N*R LLM çağrıları, her biri büyüyor bağlamı ile. 5 ajan, 5 tur tartışma büyüyor bağlamda 25 çağrıdır. Her soru için maliyet tek bir CoT çağrısı 10 katı aşabilmektedir.
  Çeviri:**计算爆炸。**N 个代理 x R 轮 = N*R 次 LLM 调用,每次的上下文都在增长──5 个代理、5 轮的辩论是25 次调用,上下文不断增长──每问题成本可能超过单次 CoT 调用的10倍──

## Yapın.
```figure
multi-agent-debate
```

## Yapın

`code/main.py`Her ajanın farklı (muhtemelen yanlış) bir cevapla başladığı bir matematik sorusu üzerinde 3 ajan x 3 tur tartışmaları yürütür. Ajanlar  her "daha" yazılarla komşuların cevaplarının ortalama bir yazılı güvenle ağırlıklandırıldığını göstererek yazılıdır.

> `code/main.py`Bir matematik sorusunda çalışmak 3 Agent x 3 Round Debat, her Agent farklı bir                                                                                                                                                                                                                                                      

Demo iki önemli etkeni gösteriyor:

> Gösterim iki önemli etkiye sahip:

- Tek bir değişim, ajanları doğru cevaba yaklaştırır.
  Çinçe Çevirisi: 单轮交流将 代理 移向正确答案──
- İkinci turdan sonraki ek turlarda düşen getiri gösterir (Du et al. plato ile eşleşir).
  Çinçe Çevirisi: İkinci turun fazladan tur sayısı gelir düşüşünü gösterir.

Çık:

```
python3 code/main.py
```

## Çerçeveyi kullanın.

`outputs/skill-debate-configurator.md`Yeni bir görev için bir tartışma ayarlar: ajan sayısı, tur sayısı, heterogenlik (eşit model vs karışık), rol atama (simetrik vs. tek karşıtlık).

> `outputs/skill-debate-configurator.md`Yeni görev konumu tartışması:Agent 数量、轮数、异构性(同样模型 vs 混合)、角色分配(对称 vs 一个对抗者) ・・・

## İndirin . Ürünler .

Eğer tartışmaya devam ederseniz:

> Eğer dep署辩论系统:

- **Cap rounds at 3.**Du et al. 3 tur kazancın çoğunu yakalar.
  Çeviri:**将轮数限制在 3。**Du 等人, üç turun büyük kısmını kazanç olarak elde ettiğini göstermiştir.
- **Cap agents at 5.**5'in ötesinde bağlam ve maliyet baskısı vardır.
  Çeviri:**将 Agent 限制在 5。**超過 5 條,上下文膨胀和成本占主导──
- **Heterogeneous by default.**Havuzda en az iki farklı model var.
  Çeviri:**默认异构。**Havuzda en az iki farklı temel model vardır.
- **Adversarial slot.**Bir ajan yine de anlaşmazlığa düştü.
  Çeviri:**对抗角色。**Bir ajanı nasıl olursa olsun karşıya getirir.
- **Log every round.**Ortalama atışları gizleyen tartışma sistemleri debugging veya denetim yapılamaz.
  Çeviri:**记录每轮。**Gizli orta sıralardaki tartışmalar sistemi, denetlenemez veya denetlenemez.

## Egzersizler.

1. Çık .`code/main.py`Bu da bir diğer yöntemi oluşturur.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`code/main.py`Ardından da 5 olarak ayarlanacak ve gelirlerin azalmasını göreceğiz.
2. Dördüncü bir ajan ekleyin, karşıtlıklı bir rol oynar: her zaman mevcut çoğunlukla aynı fikirde olmaz.
   Çinçe Çevirisi: Ekle dördüncü bir karşılaşmacı var:总是与当前多数不同意.
3. Bir turda anlaşma puanı (çoğunlukla verilen cevapta ajanların bölümü) ne zaman 1.0'a ulaşır ve bu "sağ"a eşdeğer mi?
   Çinçe Çevirimiçi: çizim (印刷) Birlik (一致性分数) (Running) (Running) (Running) (Running) (Running) (Running) (Running) (Running) (Running) (Running) (Running) (Running) (Running) (Running) (Running) (Running) (Running) (Running) (Running) (Running) (Running) (Running) (Running) (Running) (Running) (Running) (Running) (Running) (Running) (Running) (Running) (Running) (Running) (Running) (Running) (Running) (Running) (Running) (Running) (Running) (Running) (Running) (Running) (Running) (Running) (Running) (Running) (Running) (Running) (Running) (Running) (Running) (Running) (Running) (Running) (Running) (Running) (Running) (R)) (Running) (Running) (Running) (Running) (R) (R)) (Running) (R) (R) (R)) (R) (R) (R)) (R) (R) (R)) (R))
4. Bölüm 4'ün ablationlarını okuyun. "Agent-only" vs. "Rounds-only" vs. "bütün" sonuçlarını bu kodla tekrarlayın.
   Çinçe Çevirimi: Du 等人第 4 节消融实验──使用此代码复现"仅代理"vs"仅轮数"vs"两者结合"的结果──
5. "Çılgınlık yapmalı mıyız?" (arXiv:2311.17371) ve "doğru-robin" 'den öte iki tartışma varianını listede.
   Çinçe Çevirimi Çevirisi: "Biz çıldırmaya mi gidelim?" ([[arXiv: 2311.17371) ]]

## Anahtar Şartlar .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Society of Mind / 心智社会 | "Minsky's idea" / "Minsky 的想法" | Intelligence as interacting specialists; 1986 framing now operationalized via LLM debate. / 智能作为交互的专家；1986 年的框架现在通过 LLM 辩论实现。 |
| Multi-agent debate / 多 Agent 辩论 | "Agents argue" / "Agent 争论" | N agents propose, critique each other, revise over R rounds, majority-vote. / N 个 Agent 提议、批评彼此、在 R 轮中修改、多数投票。 |
| Consensus / 共识 | "They agree" / "他们一致" | Not epistemic truth — just fraction-on-majority-answer. Can be confidently wrong. / 不是认识论真理——只是多数答案上的比例。可能自信地犯错。 |
| Rounds / 轮次 | "Exchange steps" / "交换步骤" | One round = each agent reads the others and updates once. / 一轮 = 每个 Agent 阅读其他 Agent 并更新一次。 |
| Heterogeneous debate / 异构辩论 | "Mix model families" / "混合模型族" | Using different base models to decorrelate errors. / 使用不同的基础模型来去相关错误。 |
| Sycophancy cascade / 谄媚级联 | "Everyone agrees with the loud one" / "每个人都同意最大声的" | Debate failure where agents defer to the most confident agent regardless of correctness. / 辩论失败，Agent 不顾正确性屈从于最自信的 Agent。 |
| NLSOM | "129-agent society" / "129 Agent 社会" | Natural-language society of mind; Zhuge et al.'s scaled version. / 自然语言心智社会；Zhuge 等人的扩展版本。 |
| Correlated error / 相关错误 | "Same model, same bug" / "相同模型，相同 bug" | Why self-consistency saturates; debate across different views decorrelates. / 自我一致性为什么饱和；不同观点的辩论去相关。 |

## Daha fazla okumak

- [Du et al. — Improving Factuality and Reasoning in Language Models through Multiagent Debate](https://arxiv.org/abs/2305.14325) İpucu kağıdı, ICML 2024
  Çinçe Çevirimi:Du 等人  通过多 Agent 辩论改进语言模型的事实性和推理  参考论文, ICML 2024
- [Zhuge et al. — Mindstorms in Natural Language-Based Societies of Mind](https://arxiv.org/abs/2305.17066) 129-ajan NLSOM
  Çeviri: Zhuge 等人   基于自然语言的心智社会中的思维风暴  129 NLSOM ajanı
- [Should we be going MAD? A Look at Multi-Agent Debate Strategies for LLMs](https://arxiv.org/abs/2311.17371) Referans değerleri tartışma çeşitleri
  Çinçe Çevirimi: Biz MAD ğa doğru gitmeli miyiz?
- [Debate project page](https://composable-models.github.io/llm_debate/) Du et al. ' nin kodu, demoları ve ablation detayları
  Çinçe Çevirimi:辩论项目页面  Du 等人的代码、演示和消融细节
