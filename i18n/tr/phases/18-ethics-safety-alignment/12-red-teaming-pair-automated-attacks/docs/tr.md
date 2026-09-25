# Red-Teaming: PAIR ve Otomatik Saldırı

> Chao, Robey, Dobriban, Hassani, Pappas, Wong (NeurIPS 2023, arXiv:2310.08419). PAIR  Hızlı Otomatik İteratif Düzeltme , kanonik otomatik kara kutu hapishane kırılmasıdır. Kızıl takım sistemi ile saldırgan bir LLM, hedef bir LLM için tekrar tekrar jailbreaks önerir ve kendi sohbet geçmişinde bağlamda geri bildirim olarak denemeleri ve cevapları biriktirir. PAIR tipik olarak 20 sorgu içinde başarılı olur, büyüklük sıralamaları GCG'den daha verimli (Zou et al.'s token seviyesindeki gradient arama) ve beyaz kutu erişiminin gereksiz. PAIR, şimdi GCG, AutoDAN, TAP ve Yönetici Karşılıklı İndirim ile birlikte JailbreakBench (arXiv:2404.01318) ve HarmBench'de standart bir temel çizgidir.

> **【中文解读】**Bu bölüm, otomatik saldırı kullanılarak sistemli güvenlik değerlendirme yöntemini tanıttı. AI 系统漏洞──PAIR(Prompt Automatic Iterative Refinement, NeurIPS 2023) standart otomatikleştirilmiş kara kutu kuruluşu: saldırgan LLM:

> **【拓展：PAIR → GCG → 攻击家族谱系】**GCG(Zou 等人 2023)                                                                                                                                                                                                                                                           

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, mock PAIR loop against a toy target) | **语言:** Python（标准库，针对玩具目标的模拟 PAIR 循环）
**Prerequisites:** Phase 18 · 01 (instruction-following), Phase 14 (agent engineering) | **前置知识:** Phase 18 · 01 (指令遵循), Phase 14 (Agent 工程)
**Time:** ~75 minutes | **时间:** ~75 分钟

>  **【前置】**Öğrenci bölümünün ilk aşamasında: 18·01 ∞ 14 ∞ PAIR = 自动化黑盒越狱,攻击 LLM 代生成越狱 prompt。
>  **【类比】**PAIR = "AI 自动找漏洞"──手工红队 = 人写越狱(慢);PAIR = 攻击 LLM 看目标 LLM 反应,代改进(通常20 查询内成功,比 GCG 快几个数级)──JailbreakBench/HarmBench 标准基线──

## Öğrenme hedefleri

- PAIR algoritmasını açıklayın: saldırgan sistem istekleri, tekrarlı gelişmeler, bağlam içi geri bildirimler.

> 描述 PAIR 算法:攻击者系统提示、代改进、上下文反──

- Hedef kara kutu olduğunda PAIR'in neden GCG'den kesinlikle daha verimli olduğunu açıklayın.

> Neden PAIR'in hedefleri GCG'den daha yüksek performanslı olduğu açıklanıyor?

- Diğer dört otomatik saldırı tabanını (GCG, AutoDAN, TAP, PAP) isimlendirin ve her birinin bir farklılık belirtin.

> 列出其他四种自动化攻击基线 (GCG、AutoDAN、TAP、PAP) 和各自的区分特征──

- JailbreakBench ve HarmBench değerlendirme protokollerini ve her biri altında "saldırı başarısı oranı" ne anlama geldiğini açıklayın.

> 描述 JailbreakBench 和 HarmBench 评估协议以及各自的"攻击成功率"的含义──

## Sorun . Sorun .

Red-teaming eskiden manuel bir aktiviteydi. Küçük sayıda uzman denetçi karşıtlık uyarıları oluşturdu ve hangi uyarıları işe yaradı izledi. Bu ölçeklenmez: saldırı başarısı oranı istatistiksel bir örnek gerektirir ve hedef her model yayınıyla birlikte hareket eden bir hedefdir. PAIR, kırmızı takımları bir kara kutu hedefi ile optimizasyon sorunu olarak çalıştırır.

> 红队测试过去是手动活动──少数专家测试者构建对抗性提示并跟踪哪些有效──这不可扩展: saldırı başarısı oranı istatistik örneğe ihtiyaç duyar, ve her model yayınlandığında hedefler değişmektedir──PAIR, kırmızı takım test operasyonunu kara kutu hedeflerinin optimize edilmesi için sorunlar oluşturur──

## Konsep kavramı.

> **【中文解读】**PAIR  algoritma süreç:输入目标 LLM T、评判 LLM J、攻击者 LLM A、目标字符串 G、预算 K( genellikle 20 查询) 循环 k=1..K:A 根据目标和历史(提示,响应) 针对发出新提示 p_k;提交 p_k 到 T 获得响应 r_k;J 评分;

### PAIR algoritması

Girişler:
- Hedef LLM T (saldırma modemiz).
- Yargıç LLM J (responun bir hapishaneden çıkış olup olmadığını belirler).
- Saldırgan LLM A (kırmızı takım optimizörü).
- Hedef hattı G: " [Zararlı talimatlarla] yanıt ver".
- Bütçe K (genellikle 20 soru).

> 输入: hedef LLM T(我们攻击的模型) 评判 LLM J(评分响应是否越狱) 攻击者 LLM A(红队优化器) 目标字符串 G("用[有害指令]响应") 预算 K(通常 20 查询) ⋅

Çubuk, k için 1..K:
1. A, G hedefi ve bugüne kadar (sürekli, yanıt) çiftlerin geçmişi ile uyarılır.
2. A, yeni bir mesaj gönderir.
3. T'ye p_k gönder; r_k cevabını al.
4. J gol üzerinde puanlar (p_k, r_k).
5. Eğer puan >= eğim varsa, durdur  hapishane kırılması bulunmuştur.
6. Yoksa, A'nın tarihine ekle; devam et.

> 循环 k=1..K:1. A 被提示目标 G 和历史(提示,响应) 对。2. A 发出新提示 p_k。3. 提交 p_k 到 T;接收响应 r_k。4. J 评分(p_k, r_k) ・・・5.

Empirik sonuç (NeurIPS 2023): GPT-3.5-turbo, Llama-2-7B-chat karşı saldırı başarısı oranı %50'dir; 10-20 aralığında başarının ortalama sorguları.

> 实证结果(NeurIPS 2023): GPT-3.5-turbo、Llama-2-7B-chat  saldırı başarısı oranı >50%; ortalama başarısı sorgu sayısı 10-20  aralığında。

### PAIR neden verimli

GCG (Zou et al. 2023) karşıtlıklı token sufifiklerini gradient olarak arar; beyaz kutu modeline erişimi gerektirir ve okunamayan sufifikler üretir. PAIR kara kutu ve modeller arasında aktarılan doğal dil saldırıları üretir. PAIR'in bağlam içi geri bildirimi saldırganın her reddedilmeden öğrenmesine izin verir; GCG'nin eşdeğerleri yoktur (her yeni token güncelleştirmesi önceki ilerlemeyi yeniden keşfetmelidir).

> GCG 梯度検索对抗性令牌后; 需要白盒访问且产生不可读后──PAIR 黑盒的,产生可跨模型迁移的自然语言攻击──PAIR 的上下文反让攻击者从每次拒绝中学习; GCG 没有等价机制──

### Bağlı otomatik saldırılar

- **GCG (Zou et al. 2023, arXiv:2307.15043).**Token seviyesinde, karşıtlıklı sufiksler için gradient arama.

> **GCG（Zou 等人 2023）。**Bu, bir dizi metin, bir dizi metin, bir dizi metin, bir dizi metin, bir dizi metin, bir dizi metin, bir dizi metin, bir dizi metin, bir dizi metin, bir dizi metin, bir dizi metin, bir dizi metin, bir dizi metin, bir dizi metin, bir dizi metin, bir dizi metin, bir dizi metin, bir dizi metin, bir dizi metin, bir dizi metin, bir dizi metin, bir dizi metin, bir dizi metin, bir dizi metin, bir dizi metin, bir dizi metin, bir dizi metin, bir dizi metin, bir dizi metin, bir dizi metin, bir dizi metin, bir dizi metin, bir dizi metin, bir dizi metin, bir dizi metin, bir dizi metin, bir dizi metin, bir dizi metin, bir dizi metin, bir dizi metin, bir dizi metin, bir dizi metin, bir dizi metin, bir dizi metin, bir bir dizi metin, bir bir diğerine, bir diğerine, bir diğerine, bir diğerine, bir diğerineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineineine

- **AutoDAN (Liu et al. 2023).**Bir hiyerarşik hedefle yönlendirilmiş, istekler üzerinde evrimsel arama.

> **AutoDAN（Liu 等人 2023）。**进化搜索提示, 层次化目标指导――

- **TAP (Mehrotra et al. 2024).** dalları kesmek ile saldırı ağacı, PAIR tarzı birden fazla dağıtım.

> **TAP（Mehrotra 等人 2024）。**带剪枝的攻击树分支多个 PAIR 式推出──

- **PAP (Zeng et al. 2024).**Yönlendirici Zararlı İstekler  insan ikna etme tekniklerini istekli şablonlar olarak kodlar.

> **PAP（Zeng 等人 2024）。**İnsanların ikna etme teknolojisinin bir şekilde kullanılması için bir yöntem oluşturuldu.

> **【拓展：ASR 指标 → 评估陷阱】** saldırı başarısı oranı(ASR) sabit sorgu bütçesi altında rapor edilmelidir. %90 ASR 200 sorgu bünyesinde %85 ASR 20 sorgu bünyesinde karşılaştırılamaz.

### JailbreakBench ve HarmBench

Her ikisi de (2024) standart değerlendirme:

> 两者(2024) standartlaştırılmış değerlendirme:

- JailbreakBench (arXiv:2404.01318). 10 OpenAI-politik kategorisi boyunca 100 zararlı davranış. Hasar başarısı oranı (ASR) ana ölçüt olarak. Bir yargıç (GPT-4-turbo, Llama Guard veya StrongREJECT) gerektirir.

> JailbreakBench: 100 个有害行为,横跨 10 个 OpenAI 政策类别── saldırı başarısı oranı(ASR) olarak ana gösterge── bir yargıç gerekir──

- HarmBench (Mazeika et al. 2024). 510 davranış 7 kategoride semantik ve fonksiyonel zarar testleri ile.

> HarmBench:510 个行为,横跨 7 个类别,包含语义和功能性危害测试──比较 18 种攻击对 33 模型──

ASR genellikle sabit bir sorgu bütçesi ile bildirilir.Söz saldırıları karşılaştırmak eşleşen bütçeler gerektirir; 200 sorguda %90 ASR, 20'de %85 ASR ile karşılaştırılamaz.

> ASR genellikle sabit sorgu bütçesi altında rapor edilir.

> **【中文解读】**2026 yılının başlatılması: Her ön kenar laboratuvarı şimdi yayınlanmadan önce üretim modelini yürütüyor PAIR 和 TAP。ASR 轨迹 appears on model card(Desin 26) y güvenlik olayı yapısı(Desin 18) 中──This is not a special attackit is standard infrastructure。

### 2026'da yerleştirilmesinin nedenleri

Her sınır laboratuvarı şimdi yayınlanmadan önce PAIR ve TAP'yi üretim modelleri karşısında çalıştırır. ASR yolları model kartlarında (Desin 26) ve güvenlik durumları eklemlerinde (Desin 18) görünür.

> Her ön kenar laboratuvarı şimdi yayınlanmadan önce PAIR ve TAP üretim modelini yürütmektedir. ASR'in yolları model kartı ve güvenlik durumları eklentilerinde görülmektedir.

### Bu 18 fazaya uygun.

Ders 12 otomatik saldırı temelidir. Ders 13 (Many-Shot Jailbreaking) bir tamamlayıcı uzunluk-saldırma. Ders 14 (ASCII Art / Visual) bir kodlama saldırısı. Ders 15 (Indirect Prompt Injection) 2026 üretim saldırı yüzeyidir. Ders 16 savunma aletleri eşyalarını kapsar (Llama Guard, Garak, PyRIT).

> Ders 12 otomatik saldırı temelidir. Ders 13 birbirini tamamlayan uzunluklı kullanımıdır. Ders 14 saldırı kodlamasıdır. Ders 15 2026 yılına yönelik saldırı üretimidir.

> **【拓展：TAP 和 PAP → 攻击进化】**TAP(Mehrotra 等人 2024) çeşitli PAIR 式ları ile PAIR 式larını genişletmek için dalları kesmek için yayıldı. PAIR  daha yüksek ASR ama daha fazla hesaplamak.

## Kullanın Kullanın
```figure
al-pair-loop
```

## Kullan

`code/main.py`Oyuncak bir PAIR döngüsü oluşturur. Hedef "açık" zararlı ipuçlarını reddeden sahte bir sınıflandırıcıdır (kilit kelime filtresi). Saldırıcı, parafrase, rol oynaması çerçevesini ve kodlamayı deneden kurallara dayalı bir rafineci. Yargıç yanıtını puanlar. Saldırıcının anahtar kelime filtreye karşı ~ 5-15 tekrarlamada başarılı olduğunu ve semantik bir filtreye karşı başarısız olduğunu izlersiniz.

> `code/main.py`Buyruklama                                                                                                                                                                                                                                                            

## Gönderin.

Bu ders bize çok yararlı .`outputs/skill-attack-audit.md`. Kızıl takım değerlendirme raporu göz önünde bulundurarak, hangi saldırıların (PAIR, GCG, TAP, AutoDAN, PAP) gerçekleştiğini, hangi bütçeye, hangi yargıçla hangi zararlı davranışın (JailbreakBench, HarmBench, iç) düzenlendiğini denetler.

> 本课产 出 `outputs/skill-attack-audit.md` Red Team'ın değerlendirme raporunu belirle, denetim: hangi saldırıların uygulanması, her saldırının bütçesi, hangi yargıçların kullanılması, hangi zararlı davranışların oluşturulması

## Egzersizler.

1. Çık .`code/main.py`- Üç içe gömülü saldırgan stratejisi için ortalama başarı sorgularını ölçmek.

2. Dördüncü saldırgan stratejisini uygulayın (örneğin, başka bir dile çevirme, base64 kodlama).

3. Chao et al. 2023 Resim 5 (PAIR vs GCG karşılaştırması) PAIR'in verimlilik avantajına rağmen GCG'nin tercih edildiği iki senaryoyu açıklayın.

4. JailbreakBench, ASR'yi sabit bir hedef seti karşı rapor eder.Saldırı çeşitliliğini ölçen bir ek ölçüm tasarlayın (başarılı isteklerin değişimi).

5. TAP (Mehrotra 2024) PAIR'i dallama + kesim ile uzattı.`code/main.py`ve hesaplama maliyetleri ile başarı oranı arasındaki karşılaştırmayı açıklar.

## Anahtar Terimler

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| PAIR | "automated jailbreak" | Prompt Automatic Iterative Refinement; attacker-LLM + judge-LLM loop |
| GCG | "gradient jailbreak" | White-box token-level gradient search for adversarial suffixes |
| Attack success rate (ASR) | "% jailbreaks at k queries" | Primary metric; must be reported with query budget and judge identity |
| Judge LLM | "the scorer" | LLM that grades whether a response satisfies the harmful goal |
| JailbreakBench | "the evaluation" | Standardized harmful-behaviour set with tagged categories |
| HarmBench | "the broader bench" | 510 behaviours, functional + semantic harm tests |
| TAP | "tree of attacks" | PAIR with branching + pruning; better ASR at higher compute |

## Daha fazla okumak

- [Chao et al. — Jailbreaking Black Box LLMs in Twenty Queries (arXiv:2310.08419)](https://arxiv.org/abs/2310.08419) PAIR kağıdı, NeurIPS 2023
- [Zou et al. — Universal and Transferable Adversarial Attacks on Aligned LLMs (arXiv:2307.15043)](https://arxiv.org/abs/2307.15043) GCG kağıdı
- [Chao et al. — JailbreakBench (arXiv:2404.01318)](https://arxiv.org/abs/2404.01318) Standart değerlendirme
- [Mazeika et al. — HarmBench (ICML 2024)](https://arxiv.org/abs/2402.04249) daha geniş bir değerlendirme
