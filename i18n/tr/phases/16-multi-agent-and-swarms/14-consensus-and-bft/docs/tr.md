# Konsens ve Bizans Sorun Toleransı Ajanlar için

> Klasik dağıtılmış sistemler BFT, stokastik LLM'lere ulaşıyor. 2025-2026 yıllarında üç araştırma yönü ortaya çıktı: **CP-WBFT**(arXiv:2511.10400) her oyı bir güven sorgulaması ile tartar.**DecentLLMs**(arXiv:2507.14928) paralel işçi önerileri ve geometrik-medyen birleştirme ile lidersiz kalıyor. **WBFT**(arXiv:2505.05103) ağırlıklı oylama ile Hiyerarşik Yapı Gruplama'yı birleştirerek Core ve Edge düğümlerini ayırır. "AI Ajanları Anlaşabilir mi?" (arXiv:2603.01213)'nin dürüst bir empiriyel sonucu, bugün ölçekli anlaşmanın bile kırılgan olmasıdır. BFT gereklidir ama yeterli değildir. Bu ders minimal bir BFT protokolü oluşturur, üç ajan-spesifik saldırıyı enjekte eder (Bizans yalanı, sikofant uyumluluk, ilişkili hata monoculture) ve her konsensüs varianti nasıl başa çıktığını ölçer.

> **【中文解读】**Bu bölüm, bir anlaşma ve bir işçiyi yanlış davranışlarda bulunurken nasıl anlaşılır olduğunu anlatır.

> **【拓展：consensus and bft→具体应用】**拜占庭容错 (BFT) 多代理 系统中的应用:当部分 Agent可能故障或被攻击时,如何确保系统整体正确? klasik BFT 算法 (PBFT) 需要3f+1 个节点容忍 f 个故障节点―― LLM Agent 上下文中,'故障' 可是幻觉、注入或拒绝执行──实践中使用多数投票作为简化 BFT──


**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib) | **语言:** Python（标准库）
**Prerequisites:** Phase 16 · 07 (Society of Mind and Debate), Phase 16 · 13 (Shared Memory) | **前置知识:** Phase 16 · 07（心智社会与辩论），Phase 16 · 13（共享内存）

>  **【前置】**Öğrenci bölümünün ilk aşamasında:Devam 16·07 (debat)  16·13 (共享内存)  dağıdılı sistem BFT (PBFT)  Raft (LLM) 
>  **【类比】**BFT = "Juride oy verildi ama içinde bir hata yapılmalı"。 klasik BFT =  toleran 1/3 节点说谎(PBFT 3f+1);LLM 版 = 加权投票(按置信度) + 几何中位数聚合 + 层级聚类。三类攻击:拜占庭说谎、附和、相关错误(同一基模型 全错)。结论:BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: BFT: B) BFT: BFT: BFT: BFT: BFT: BFT: B) BFT: BFT
**Time:** ~75 minutes | **时间:** ~75 分钟

## Sorunlar sorunun giriş

N LLM ajanları var. Her biri bir cevap üretir. Onlar aynı fikirde değiller. Çoğu oy yanlış bir tanesini seçer çünkü iki ajan ilişkili (eşit temel model, aynı eğitim verileri, aynı başarısızlık modları).

> Sizde N'LLM Ajanı var, her biri bir cevap üretir. Bunlar aynı değildir. Çoğu oy yanlış cevapları seçti, çünkü iki Ajan ilgili. Aynı temel model, aynı eğitim verileri, aynı başarısızlık modeli.

Şimdi bir aldatıcı ajan ekleyin: kasıtlı olarak yalan söylüyor. veya bir sikofant ajan: son konuşanla aynı fikirde. klasik BFT'de, Bizans düğümlerinin bir bölümü olduğu varsayımıdır.`f < n/3`2026'da gerçek şu ki, LLM düğümleri dürüst olsalar bile, modeller arasında ilişkili ve birbirlerinin çıkışları tarafından etkilenen stohastiktir.

> Şimdi bir aldatıcı ajanı kabul et: Bu bir yalan. Ya da bir yalancı ajanı kabul et: Son konuşmacı fikrine.`f < n/3`Ve istekli davranmak.2026 yılının gerçekliği, LLM 节点 bile dürüstlük de rastlantı, örneğin, birbirinden etkilenmek ve üretilenlerdir.

Klasik BFT (PBFT, 1999) yanlış değildir  eksiktir. İstisnasız bit-flipping ile ilgilenir. "Üç dürüst ajan eğitim verilerini paylaştığı için bir halüsinasyon paylaşıyor".

> Klasik BFT(PBFT, 1999)并非错它是不完整的──它处理任意的位翻转──但它不处理"三个诚实代理"因为共享训练数据产生相同幻觉"──本课程来自PBFT的基础,叠加三个2025-2026年改进──

## Konsept merkezi konsept

### Klasik BFT'nin size verdiği

Pratik Bizans Suç Tahammülü (Castro & Liskov, OSDI 1999)`f < n/3`Bizans düğümleri. Protokol üç aşama (hazırlama, hazırlama, görev) ve iki primitif ( imzalama mesajları, kworum sertifikaları) sahiptir.`n >= 3f + 1`Dürüst veya kötü niyetli düğümler.

> 实用拜占庭容错(Castro & Liskov, OSDI 1999) tolerance `f < n/3`个拜占庭节点──协议有三个阶段 (预备,准备,提交) 和两个原语 (签名消息,仲裁证书)`n >= 3f + 1`个诚意或恶意节点之间就单一价值达成一致.

Garantiler güçlüdür ama şu varsayımları var:

> Bu garantiler çok güçlü ama varsayım:

1. **Independent faults.**Bizanslılar koordinasyon yapmaz.
   Çeviri:**独立故障。**拜占庭节点不协调──
2. **Honest nodes are truly honest.**Dürüst çıkışların doğruluğu bir sorun değil; protokol sadece anlaşmazlıkları düzeltir.
   Çeviri:**诚实节点真正诚实。**诚实输出正确性问题;协议只处理分歧──
3. **The question has a ground-truth answer.**Yanlış bir gerçekle ilgili bir fikir birliği hala bir fikir birliği.
   Çeviri:**问题有标准答案。**Hataların farkında olmak hâlâ farkındadır.

LLM ajanları üçünü de ihlal eder. Aynı temel modelde çalışan iki ajan hata paylaşıyor. "Dürüst" bir LLM hala halüsinasyonlar yapar. ve belirsiz sorularda, "gerçek" ajanların karar verdiği şey dış bir oracle yok.

> LLM Ajanı  üç varsayımı ihlal etti                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                

### Üç LLM özel saldırısı

**Byzantine lie.**Bir ajan kasten yanlış bir cevap verir.`f < n/3`- Evet .

> **拜占庭撒谎。**Bir ajan yanlış bir cevap vermeye çalışıyor.`f < n/3`Klasik BFT'ler işlenebilir.

**Sycophantic conformity.**Bir ajan oy vermeden önce diğerlerinin cevaplarını okuyor ve son konuşan kişiyle uyumlu. Kötü olmayan, ama en yüksek sesle ilişkili.

> **谄媚从众。**Bir Ajan oylama öncesi diğer Ajanın cevabını okuyarak son konuşanla aynı fikirde kalır.

**Correlated-error monoculture.**Üç ajan aynı temel modelde. Aynı yanlış cevabı halüsinasyonlar. Çoğu yanlıştır. Klasik BFT yardım etmez çünkü üçü de " dürüstçe " aynı fikirde.

> **相关错误单一文化。**Üç Ajan ortak bir temel model oluşturur. Aynı yanlış anlamalar ortaya çıkar. Çoğu yanlışlıklardır.

### 2025-2026 Cevapları

**CP-WBFT**(arXiv:2511.10400)  Güvenle Denetlenmiş Ağırlaştırılmış BFT. Her seçmen cevabına bir güven sorgulamasını bağlar (kendine bildirilen bir olasılık veya ayrı bir kalibrasyon modeli öngörü). Oy tartıları güvenle ölçeyor. Tam grafiklerde +85.71% BFT iyileşmesi bildirildi.

> **CP-WBFT**(arXiv:2511.10400)  güvence araştırması artırma hakkı BFT。 her oy veren kendi cevabına bir güvence araştırması eklemiş olur.

**DecentLLMs**(arXiv:2507.14928)  Lidersiz. İşçi ajanları paralel olarak önerir, değerlendirici ajanlar önerileri puanlar, son cevap puanlanmış pozisyonların geometrik ortalamasıdır.`f < n/2`. Benzans yalanı ve ilişkili hatalar için hafifleme (geometrik ortalama dış değerlere dayanıklıdır ve model önyargılı ortalama değil yoğun kümelere doğru çekilir).

> **DecentLLMs**(arXiv:2507.14928) Lidersiz  İşçi Ajanı ve önerileri, değerlendirme Ajanı için program değerlendirmesi, son cevap değerlendirme konumunun hangi sırada olduğunu `f < n/2`时稳健.                                                                                                                                                                                                                                                             

**WBFT**(arXiv:2505.05103)  Yerarşik Yapı Klusterleme ile ağırlanan BFT. Oy ağırlıkları yanıt kalitesi ile birlikte tarihten öğrenilen bir güven puanı ile atılır. Kluster ajanları Core ve Edge'e; Core ajanları önce konsensüse ulaşmalıdır, Edge ajanları takip eder.

> **WBFT**(arXiv:2505.05103) 带层次结构聚类的加权 BFT;; oy hakkı, cevap kalitesi ile birlikte tarihsel öğrenimden gelen inanç oranlarının dağılımı; 将代理聚类为核心和边缘; 核心代理 必须先达成共识,边缘代理跟随;; 针对可扩展性的缓解措施 (Central共识小而快) 部分针对单一文化的缓解 (Central can choose diversity) ;;

### Empirik: "İS ajanları kabul edebilir mi?" (arXiv:2603.01213)

Kağıt, çok sayıda sınır modeli arasında skalar anlaşmayı ölçer (LLM ajanları tek bir sayısal değer üzerinde anlaşırlar).

> Bu makale, çok sayıda ön kenar model üzerinde standart tutarlılığını ölçtü.

- Hiç bir rakip olmamasına rağmen, LLM ajanları birçok referans değerinde %30'dan fazla oranlarda ölçekli sorular konusunda anlaşmazlık yaşıyor.
  Çinçe Çevirisi: Haksız bile, LLM Ajanı, birçok temel testlerde, standart sorunlarının %30'dan fazla anlaşmazlık oranı vardır.
- Yalancı bir karakter edinen tek bir ajan, karışım ajanları konsensusunu dürüst bir başlangıç çizgisinden %40'dan fazla çıkarabilir.
  Çinçe Çevirimi: Hileci kişilik bir tek ajanı kullanarak karıştırabilir Agent ortak bilgi ve dürüstlik için 40 个百分点以上.
- Anlaşmazlık oranları model çeşitliliği ile ilişkili  heterogen gruplar homogen gruplardan daha fazla anlaşmazlıkta (iyi: ilişkili olmayan hatalar), ancak aynı zamanda daha yavaş hareket etmektedir (kötü: daha uzun anlaşma süresi).
  Çinçe Çevirimiçi:不一致率与模型多样性相关异构集成比同构集成不一致更多(好:不相关错误),但漂移更慢(坏:更长的一致达成时间) ⋅

BFT, çıkışları uyumlandırmak için bir makine sağlar, ancak uyumlu çıkışın doğru olup olmadığını söylemez.

> Sonuç:BFT                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          

### Ana protokol, çıkarıldı

LLM temsilcileri için en az BFT turları:

```
1. task arrives; each agent i produces answer a_i
2. each agent attaches confidence probe c_i in [0, 1]
3. aggregator collects (a_i, c_i) from all n agents
4. aggregator groups by semantic cluster (equivalent answers)
5. aggregator computes weight for each cluster C:
     w(C) = sum_{i in C} c_i
6. winner = cluster with max weight, if max > threshold * sum(c_i)
   else: retry or escalate
7. minority clusters logged with provenance for post-hoc audit
```

Semantik gruplama adımı LLM-specifik dönüştürülür. İki cevap "kağıt raporları 4.2%" ve "4.2% iyileşme" aynı gruplama.

> 语义聚类步骤是LLM'in özel yenilikleri. İki cevap: "4.2%" ve "4.2%'in iyileştirilmesi" aynıdır.

### Sınır ayarlama

- Evet .`threshold`Bu, bir diğer yöntemi de gösterir. Bu, bir diğer yöntemi de gösterir.`n=5-7`Daha küçükleri için daha yüksek.`n`Bir eşiğin altında, insan veya başka bir ajan grubuna tırman.

> `threshold`参数决定何时接受、何时重试──太低:接受弱多数──太高:永远不接受任何东西── deneyim kapsamı:`n=5-7`个 Agent 时为0.5-0.67,较小的 `n`时更高. 低于 值. 时更高. 低于 值. 时更高. 低于 值. 时更高. 低于 值. 时更高. 低于 值. 低于 值. 时更高. 低于 值. 低于 值. 低于 值. 低于 值. 低于 时更高. 低于 低于 低于 值.

### Anlaşmanın yardımı olmazsa

- **Ambiguous questions.**Eğer sorunun temel bir gerçeği yoksa, konsensus bir fikirdir.
  Çeviri:**模糊问题。**Eğer bir sorun standart bir cevapsızsa, fikir bir fikirdir.
- **Compound questions.**"Kodu yaz ve açıkla"  iki cevap.
  Çeviri:**复合问题。**"编写代码并解释"两个答案──分别独立投票──
- **Adversarial multi-round.**Eğer ajanlar önceki turları gözlemleyebilir ve taklit edebilirlerse (Du 2023 tartışması), gerçekten bağımsız olarak birbirleriyle anlaşmaya başlarlar.
  Çeviri:**对抗性多轮。**Eğer ajanın gözlemleyebileceği bir süre önce birkaç kez konuştukları gibi, onlar birbirlerine karşı bir görüşe sahip olurlar.

## Yapın.
```figure
swarm-consensus-wave
```

## Yapın

`code/main.py`Uygulamaları:

- `AgentVoter` ( yanıt, güven) ile ilgili bir politika.
  Çeviri:`AgentVoter` 带有(答案,置信度) 带有((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((
- `MajorityVote` klasik çoğulluk.
  Çeviri:`MajorityVote` 经典多数投票──
- `CPWBFT` semantik gruplama ile güven ağırlığıyla oylama.
  Çeviri:`CPWBFT` 带语义聚类的信度加权投票──
- `DecentLLMs` puanlanmış öneriler üzerinde geometrik-medyen birleştirme.
  Çeviri:`DecentLLMs` 评分 提案上的几何中位数聚聚──
- `Scenario` her birleştiricisi üç saldırı kalıbı altında çalışır.
  Çeviri:`Scenario`                                                                                                                                                                                                                                                              

Uygulama şekilleri:

> 实现的攻击模式:

1. `byzantine`Bir ajan yüksek güvenle yalan söylüyor.
   Çeviri:`byzantine`Bir ajanı yalan söylemeye ikna ediyorsun.
2. `sycophancy`Bir ajan ilk gördüğü cevabı eşleşen güvenle kopyalar.
   Çeviri:`sycophancy`Bir ajan, gördüğü ilk cevabı kopyalayıp, inançlı bir şekilde uyguluyor.
3. `monoculture`: üç temsilci orta derecede güvenle yanlış bir cevap (tümleşen hata) paylaşır.
   Çeviri:`monoculture`Üç ajan ortak bir hata cevaplı, bir yanıltıcı, bir güven içinde,

Çık:

```
python3 code/main.py
```

Beklenen çıkış: bir tablo (saldırı, toplayıcı) -> son cevap, doğru cevap belirtildi. Plurality monoculture durumunu başarısız. CPWBFT'nin güven ağırlığı sikofansayı azaltır. DecentLLMs'in geometrik-medyanı monoculture nüfusun yarısından daha az olduğu zaman dürüst kümelere doğru çekilir.

> 预期输出:一张(攻击,聚合器) -> 最终答案的表格,正确答案高亮显示──多数投票在单一文化案中失败──CPWBFT'in güven artışı 缓解了──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

## Kullanın Kullanın

`outputs/skill-consensus-designer.md`Çoklu ajanlar için bir konsensus protokolü tasarlıyor: gruplama yöntemi, ağırlıklandırma, eğim ve alt eğim döngüleri için tırmanma politikası.

> `outputs/skill-consensus-designer.md`Bir çok ajan 集合设计共识协议:聚类方法、权重、值,以及低于值轮次的升级策略──

## Gönderin.

Bir konsensüse sahip olmak için herhangi bir mekanizma göndermeden önce:

- **Attack-test with at least the three patterns**Protokolünüz, sessizce değil, öngörülebilir bir şekilde başarısız olmalı.
  Çeviri:**至少用上述三种模式进行攻击测试。**Senin anlaşmanın başarısız olması beklenir, sessizce başarısız olmamak değil.
- **Log every minority cluster**Azınlık grupları, ilişkili hatalar için erken uyarı sisteminiz.
  Çeviri:**记录每个少数派簇**及其来源──少数派是你相关错误的早期预警系统──
- **Enforce bounded rounds.**"Bir anlaşmaya varana kadar tartışmaya devam etmemek"  bu da bir şımarıklık ödülünü verir.
  Çeviri:**强制限制轮次。**"Bunu kabul etene kadar tartışmaya devam etmeyin".
- **Separate agreement from correctness.**Konsens çıkışı bir doğrulayıcıya gider; doğrulayıcı ansambldan bağımsızdır.
  Çeviri:**分离一致性和正确性。**共识输出交给验证器;验证器集合den bağımsızdır.
- **Monitor the agreement rate.**Keskin bir yükseliş uyum kayıpları anlamına gelir; keskin bir düşüş model sürüklenmesi anlamına gelir.
  Çeviri:**监控一致率。**Aksi hızla yükselmesi, çoğunluğun ayrılığı anlamına gelir; aksi hızla düşmesi, model kaydırmasını anlamına gelir.

## Egzersizler.

1. Çık .`code/main.py`. Pluraliğin onaylanması monokultüre saldırıya başarısız olur ancak CPWBFT monokultüre güveninin 0.7'den aşağı olduğu zaman kısmen hafifletiyor.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`code/main.py`❖ Tek kültür saldırısında oyların çoğunluğu başarısız olduğunu doğruladı, ancak tek kültür güveninin 0.7'den düşük olduğu zaman CPWBFT  kısmının sorunları hafifletti.
2. Dördüncü saldırı kalıbını ekle:**silent abstention** bir temsilci cevap vermeyi reddeder ("Bilmiyorum").
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri**静默弃权**                                                                                                                                                                                                                                                              
3. İpuç kanonikleştirmesinden semantik gruplamaları yerleştirme-benzemeye değiştirin (herhangi bir açık kaynaklı yerleştirme modeli kullanın).
   Çinçe çevirisi:将语义聚类从字符串规范化换为嵌入相似度 (嵌入式化) 攻击会发生什么?
4. CP-WBFT (arXiv:2511.10400) okuyun. Güvenli-sonde kalibrasyon adımını uygulayın (her bir ajanın kendi kendine bildirilen güvenini ayrı bir kalibrasyon modeli kontrol eder). Monoculture senaryosunda doğruluk kazanımını ölçün.
   Çinçe çevirisi: CP-WBFT (arXiv: 2511.10400) ◊ gerçekleştirmek inandırıcılık araştırma kurgu adımları ◊ tek başına kurgu modeli kontrol her ajanın kendi kendine inanç) ◊ ölçüm tek tek kültür sahnesinde doğruluk oranı artmak ◊
5. "AI Ajanları Anlaşabilir mi?" (arXiv:2603.01213) okuyun. Basitleştirilmiş bir skalar anlaşma deneyini yeniden üretin: üç ajan, bir skalar soru, aldatıcı kişi sorusu. CPWBFT veya DecentLLMs yakalar mı?
   Çin dilinde: "AI Ajanı 能达成一致吗?" ("AI Ajanı 能达成一致吗?")

## Anahtar Terimler

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| BFT / 拜占庭容错 | "Byzantine fault tolerance" / "拜占庭容错" | Castro-Liskov 1999 protocol for consensus with `f < n/3` arbitrary faults. / Castro-Liskov 1999 协议，容忍 `f < n/3` 个任意故障节点的共识。 |
| Byzantine / 拜占庭 | "Any bad behavior" / "任何不良行为" | A node that can lie, drop messages, fail silently — anything but crash safely. / 可以撒谎、丢弃消息、静默失败的节点——除了安全崩溃外的任何行为。 |
| Confidence probe / 置信度探测 | "How sure are you?" / "你有多确定？" | Self-reported or calibrator-predicted probability attached to a vote. / 附加在投票上的自报或校准器预测的概率。 |
| Semantic clustering / 语义聚类 | "Same answer, different words" / "相同答案，不同措辞" | Grouping equivalent answers before counting votes. / 在计票前将等价答案分组。 |
| Geometric median / 几何中位数 | "Robust center" / "稳健中心" | The point minimizing sum of distances to sample points. Robust to outliers, unlike the mean. / 最小化到样本点距离之和的点。对异常值稳健，与均值不同。 |
| Monoculture / 单一文化 | "Same model, same failures" / "相同模型，相同失败" | Correlated errors when agents share training data or base model. / Agent 共享训练数据或基础模型时的相关错误。 |
| Sycophantic conformity / 谄媚从众 | "Agreeing with the loud voice" / "附和最大声的声音" | An agent's vote biases toward whoever spoke first/loudest. / Agent 的投票偏向最先/最大声发言的人。 |
| Core/Edge / 核心/边缘 | "Hierarchical BFT" / "层次化 BFT" | WBFT split: small Core consensus first, Edge nodes follow. Bounds latency. / WBFT 分割：小核心先达成共识，边缘节点跟随。限制延迟。 |

## Daha fazla okumak

- [Castro & Liskov — Practical Byzantine Fault Tolerance (OSDI 1999)](https://pmg.csail.mit.edu/papers/osdi99.pdf) Temel
- [CP-WBFT — Confidence-Probe Weighted BFT](https://arxiv.org/abs/2511.10400) Güvenle oy ağırlığı
- [DecentLLMs — leaderless multi-agent consensus](https://arxiv.org/abs/2507.14928) Geometri-medyen birleştirme
- [WBFT — Weighted BFT with Hierarchical Structure Clustering](https://arxiv.org/abs/2505.05103) Sınırlı gecikme için çekirdek/kırık bölünmesi
- [Can AI Agents Agree?](https://arxiv.org/abs/2603.01213) Skala anlaşması kırılganlığı ve aldatıcı kişi saldırısı
