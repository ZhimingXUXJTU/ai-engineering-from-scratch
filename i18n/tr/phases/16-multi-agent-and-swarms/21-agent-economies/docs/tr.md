# Agent Ekonomi, Token teşvikleri, itibar.

> Uzun vadede otonom ajanlar (METR'nin 1 ila 8 saatlik çalışma eğri) ekonomik ajanlığa ihtiyaç duyar.**5-layer stack**Bu:**DePIN**(fiziksel hesaplama) → **Identity**(W3C DID + itibar sermayesi) → **Cognition**(RAG + MCP) → **Settlement**(Hesaba çekimi) → **Governance**Üretim ajanları teşvik eden ağlar **Bittensor**(TAO alt ağları görev-sözlü modelleri ödüllendirir), **Fetch.ai / ASI Alliance**(ASI-1 Mini LLM + FET token) ve **Gonka**Akademik çalışma: AAMAS 2025'in merkezi olmayan LaMAS kullanımları **Shapley-value credit attribution**Google Research "Büyük dil modelleri için mekanizma tasarımı" önerisini yapar.**token auctions**Bu ders, minimal bir ajan pazarı oluşturur, bir çok ajan boru hattına Shapley değerli kredi atributunu uyguluyor ve ikinci fiyatlı bir token müzayedesi yürütüyor. Böylece oyun teorisi makinesi somut bir şekilde yer alır.

> **【中文解读】**Bu bölümde, Agent ekonom多 Agent sistemindeki kaynaklar değişim 定价和市场机制ı hakkında bilgi edindiler.

> **【拓展：agent economies→具体应用】**Agent  ekonomi araştırması çok Agent  sistemdeki kaynak dağılımı ve teşvik mekanizması  çekirdek kavramı:(1) 代币 ekonomi  Agent kullanır 代币 ödeme hizmetleri;(2)  nüfuz sistemi  Agent'in hizmet kalitesi seçilme olasılığını etkiler;(3)  satış mekanizması  Resurslar  teklif dağıtımıyla 😇 OpenAI'nin x402  ödeme anlaşması ve MCP'nin kapsamı  Model  Agent  ekonomisinin ilk gerçekleşmesi 😇


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib) | **语言:** Python（标准库）
**Prerequisites:** Phase 16 · 16 (Negotiation and Bargaining), Phase 16 · 09 (Parallel Swarm Networks) | **前置知识:** Phase 16 · 16（协商与讨价还价），Phase 16 · 09（并行群体网络）

>  **【前置】**Öğrenci bölümünün ilk aşaması: 16·16(parlaşmak) 、16·09 √ Swarm) 、 mekan tasarım temeli √ Shapeley 価値、拍卖 teori)  Ajan 經濟 = 多 Ajan 系统的市场层──
>  **【类比】**Agent 經濟 = "AI 自由市場"──5 層:DePIN(算力) + 身份(DID+声誉) + 认知(RAG+MCP) + 结算(账户抽象) + 治理(Agentic DAO)。Bittensor 子网奖励专门模型,Fetch.ai kullanarak ASI-1 Mini + FET token,Gonka kullanarak transformator PoW 把算力导向生产任务──学术:Shapley 给多 Agent 公平分、二价 拍卖防操纵──
**Time:** ~75 minutes | **时间:** ~75 分钟

## Sorunlar sorunun giriş

Çoklu ajan sistemleri, ajanlar birlikte değer ürettiklerinde karmaşık hale gelir ama bireysel olarak ödüllendirilmelidir. Klasik mekanizmalar  eşit bölünme, son katılımcı-her şeyi alır  haksız veya oyun oynanabilir. Shapley değerleri üzerinden koalisyon tabanlı ödüller inşaat açısından adil ama hesaplamak pahalıdır. 2025-2026 literatürü yararlı yaklaşımları teşvik ediyor: Shapley örneği, monoton birleştirme müzayedeleri ve onaylanmış katkılardan kaynaklanan zincir üzerindeki itibar.

> Birçok ajan  sistemleri ajan  birlikte değer üretir ama ayrı ödüller gerektirir karmaşıklaşır. Klasik mekanizmalar 平分、 son katılımcıların tümü  haksız veya manipüle edilebilir.

Kredi atributundan öte, alan gerçek ekonomik ajanlara dönüştü: Bittensor TAO madencilik hesaplamalarını alt ağ-sözlü modeller için ince ayarlamalar için ödüllendirir, Fetch.ai/ASI ASI-1 Mini LLM kullanımını FET jetonlarıyla ödüllendirir, Gonka üretken AI görevlerine dönüştürücü iş kanıtı yeniden dağıtır.

> 超越信用归因, bu alan gerçek ekonomik ajanlara yöneldi:Bittensor TAO 奖励挖掘计算来微调子网特定模型,Fetch.ai/ASI FET token kullanmak 奖励 ASI-1 Mini LLM kullanmak,Gonka dönüştürmek 工作量证明 再分配到生产性 AI 任务──自主交易的代理今已存在;问题是如何对齐激励──

Bu ders ajan ekonomileri belirli bir sorun ailesi olarak ele alıyor  kredi atributu, mekanizma tasarımı ve itibar  ve her birini en az matematikle inşa ediyor, böylece fikirler kalır.

> Bu ders, Agent ekonomik'i belirli bir sorunun, kredi özelliğinin, mekanizma tasarımının ve itibarının, her birinin en az matematik yapılandırılması ile gerçek anlamda anlaşılmasını sağlayacak şekilde görecektir.

## Konsept merkezi konsept

### Beş katmanlı ajan-ekonomik yığın

1. **DePIN (physical compute).**GPU, depolama, bant genişliği kiralayan merkezi olmayan alt altyapı, Bittensor alt ağları, Render ağı, Akash.
   Çeviri:**DePIN（物理计算）。**租 GPU、存储、带宽的去中心化基础设施──Bittensor 子网、Render Network、Akash──非代理 专用;Agent 使用它──
2. **Identity.**W3C Merkezi tanımlayıcıları (DID) her ajanı herhangi bir platformdan bağımsız olarak kalıcı bir kimlik sağlar. İsimlilik DID'ye gelir. Agent Ağ Protokolü (ANP) keşif katmanı olarak DID'yi kullanır.
   Çeviri:**身份。**W3C 去中心化标识符(DID) her Ajan'a bir platformdan bağımsız kalıcı ID'yi vermiştir.
3. **Cognition.**Ajanın akıl yürütme döngüsü: LLM + RAG + MCP. Diğer aşamalar da bu şekilde oluşur.
   Çeviri:**认知。**Ajanın düşünce döngüsü:LLM + RAG + MCP. Bu diğer aşama yapılandırma.
4. **Settlement.**Hesap soyutlama (ERC-4337) ajanların ETH'i tutmadan kendi bakiyelerinden gaz ödemelerini sağlar.
   Çeviri:**结算。**口座抽象(ERC-4337) Ajanın kendi bakiyinden gaz ödemesini sağlarken ETH'i tutmak zorunda değildir. Ajanın hizmetlerini ödemesi, birbirine ödemesi veya hesap ödemesi gerekir.
5. **Governance.**Ajantik DAO: İnsanların * ve * ajanların protokola yapılan değişiklikler hakkında oy verdiği yönetim yapıları, oy verme gücü itibarla bağlıdır.
   Çeviri:**治理。**Agent DAO: İnsan* ve* Agent, oy verme hakkı ve itibarı bağlanarak, oylama yapısını değiştirmek için yapılan anlaşmaya bağlıdır.

Her üretim sistemi beşini kullanmaz. Bittensor 1, 2, kısmen 3, kısmen 4, hiçbirini kullanmaz. OpenAI ajanları 3. dışında hiçbirini kullanmaz.

### Bittensor, Fetch.ai, Gonka  ne çalışıyor

**Bittensor (TAO).**Alt ağlar, özel görevlerdir (dilli modellerleme, görüntü oluşturma, tahminler). Madenciler model çıkışlarını gönderir. Validatörler onları sıralar; pay ağırlıklı puanlama TAO ödüllerini dağıtır. Her alt ağın kendi değerlendirme vardır. Ekonomik ders: görev spesifik çıkış kalitesi için ödeme, kullanılan hesaplama değil.

**Fetch.ai / ASI Alliance.**ASI-1 Mini LLM Fetch.ai'nin ağında çalışır; kullanıcılar sonuç çıkarmak için FET tokenlerini ödüyor.

**Gonka.**Transformer proof-of-work: "iş" bir transformatörün ileri geçişleri. Minerler doğru çıkışları (öğretim verilerinden) bildikleri çıkarım görevlerini çalıştırarak kazanırlar.

Üçü de Nisan 2026 itibariyle üretim derecesindedir. Ödeme dağılımları farklıdır. Bittensor alt ağ onaylayıcılarına göre kaliteli ödüller verir; Ödeme yapan kullanıcılar tarafından ölçülen Fetch ödülleri kullanımı; Gonka ödülleri doğrulanabilir sonuç çalışmaları.

### Shapley değeri kredi atributı

Üç ajan bir görev için işbirliği yapıyor.

Shapley değeri: dört aksiomu (verimlilik, simetri, doğrusallık, sıfır) karşılayan eşsiz kredi tahsisidir.`i`- ...

```
shapley(i) = (1/N!) * sum over all orderings O of (v(S_i_O ∪ {i}) - v(S_i_O))
```

nerede`S_i_O`önce ajanların bir dizi `i`Düzenleyici olarak `O`. Pratikte: tüm permutasyonları sayın, her permutasyonda her ajanın sınırlı katkılarını kaydetin, ortalama.

N=3 ajanları için 6 permutasyon vardır. N=10, 3.6M  için, pratikte saymak yerine örneği örnektir.

### Toplantı için ikinci fiyat açık artırması

Google Research ("Büyük dil modelleri için mekanizma tasarımı") LLM ürünlerini toplamak için ikinci fiyatlı token müzayedelerini önerir. Kurulum: N ajan her biri bir tamamlama önerisi; seçilmek için her birinin özel bir değeri vardır. Satışçı en yüksek değerli teklifi seçer ve *ekincisi* en yüksek değerini öder. Monoton birleştirme altında (değer hangi teklif seçildiğine bağlıdır, kaç teklif edildiğine değil), bu doğru  ajanlar gerçek değerlerini teklif ediyor.

LLM sistemleri için bu neden önemlidir: tamamlama görevlerini farklı fiyatlarla birden fazla ajanlara dışa tıraş edebilirsiniz; açık artırma en iyiyi seçer + adil ödeme yapar ve ajanların yanlış rapor vermeye teşvikleri yoktur.

### İsimlik sermayesi

DID'ye bağlı bir itibar puanı onaylanmış katkılardan biriktirilmiştir.

```
rep(i, t+1) = alpha * rep(i, t) + (1 - alpha) * contribution_quality(i, t)
```

Çürüme faktörü ile`alpha`1. Ünlü:

- Yol kararları için okumak ucuz ("çık işleri yüksek replik ajanlarına gönder").
- DID'ye bağlı olarak zamanla biriktirilen (türklenmesi pahalı).
- Kısaltılabilir: doğrulama başarısız olan katkıları çıkar.

### AAMAS 2025 merkezi olmayan LAMAS

LaMAS önerisi (AAMAS 2025): DID kimliği, Shapley değeri kredi atributasyonu ve basit bir açıklama mekanizmasını birleştirir. Ana iddia: kredi atributasyonu aşamasını merkezileştirmek sistemi denetlenebilir ve tek nokta manipülasyonuna bağışık hale getirir.

### Ekonomik çöküşleri

- **Price oracle manipulation.**Kredi fonksiyonu oynanabilirse, ajanlar oynayacak.
- **Sybil attacks.**Bir operatör kendi katkılarını arttırmak için N sahte ajanları devreye sokar. DID'ler yavaş ama bunu durdurmaz; ün kazandırması ise bu kadar büyük bir zarardan ibarettir.
- **Verification cost.**Kredi tahsis edilmesi sadece doğrulayıcı kadar adildir. Eğer doğrulama ucuzsa (küçük LLM), oyun oynanabilir; eğer pahalısa (insan paneli), sistem ölçeklenmez.
- **Regulatory overhang.**Agent ekonomileri finansal düzenleme ile kesişmektedir. Bittensor, Fetch ve Gonka, 2026 yılından itibaren bazı yargı bölgelerinde yasal gri bölgelerde faaliyet göstermektedir.

### Agent ekonomileri anlamlı olduğunda

- **Open networks with heterogeneous operators.**Tek bir ekip tüm ajanları kontrol edemez.
- **Verifiable outputs.**Doğrulama olmadan kredi atributı bir tahmin.
- **Long-horizon workflows.**Tek seferlik görevler itibar birikimiyle yararlanmaz.
- **Tokenized payments are legally viable**Yurtdışınızdaki.

Kapalı kurumsal sistemlerde, ekonomi daha basit tahsislere yer verir (menyerler işyi atarlar, ölçümler içindir).

## Yapın.
```figure
swarm-auction
```

## Yapın

`code/main.py`Uygulamaları:

- `shapley(value_fn, agents)` küçük N için sayımla Shapley'nin tam hesaplaması.
- `second_price_auction(bids)` doğru bir mekanizma; kazanan ikinci en yüksek ödemeyi yapar.
- `Reputation` Eksponansiyel çöküş ve kesimlerle DID- bağlanmış bir ün.
- Demo 1: üç ajan işbirliği yaparak, Shapley'in tam olarak krediyi gösterdi.
- Demo 2: Beş ajan bir görev boşluğu için teklif; ikinci ödül açık artırması kazananı + ödemeyi seçer.
- Demo 3: 100 adet heterogen temsilci olan ajanlara görev verimi; rep ağırlıklı yönlendirme rastgele çarpıyor.

Çık:

```
python3 code/main.py
```

Beklenen çıkış: Her ajan için Shapley değerleri; açıklama sonucu doğru teklif dengesini gösterir; tekrar ağırlanan yönlendirme, ısınmadan sonra rastgele karşı 10-20% kalite kazancı gösterir.

## Kullanın Kullanın

`outputs/skill-economy-designer.md`Asgari bir ajan ekonomisini tasarlıyor: kimlik katmanının seçimi, kredi tahsis mekanizması, ödeme mekanizması, itibar kuralları.

## Gönderin.

2026'da bir ajan ekonomisi yönetmek:

- **Start with reputation, not tokens.**Ünlü bir ün geliştirmek ucuz ve tek başına değerlidir; tokenler yasal ve ekonomik karmaşıklığa katkıda bulunur.
  Çeviri:**从声誉开始，不是 token。**¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥¥
- **Verify before you reward.**Kendiliğinden bildirilen kalite, sybil oyunları kazanır.
  Çeviri:**先验证再奖励。**Hiç kredi dağıtmayın.
- **Shapley-sample, not Shapley-exact.**Örnek 100-1000 sipariş; tam sayım ölçeklenmez.
  Çeviri:**Shapley 采样，而非 Shapley 精确。**采样 100-1000 个排序;精确枚举不可扩展──
- **Cap decay factor and floor reputation.**Sınırsız çürümüşlük meşru katkıda bulunanları siler; çok yavaş çürümüşlük ödülleri eski yüksek rep ajanları.
  Çeviri:**限制衰减因子和最低声誉。**无界衰减抹抹合法贡献者; 太慢的衰减奖过时的高声誉代理──
- **Audit mechanisms adversarially.**Her mekanizmanın bir oyun teorisi vardır; saldırganları değil, delikleri bulmak istiyorsunuz.
  Çeviri:**对抗性审计机制。**开放网络前运行红队场景──每个机制都有博论;你想找到漏洞,而不是攻击者──

## Egzersizler.

1. Çık .`code/main.py`Shapley değerlerinin toplam değerine (verimlilik aksiyomı) doğrulamasını onaylayın. Değer fonksiyonunu değiştirin; Shapley tahsisleri beklenen yönde değişir mi?
2. Shapley *sampling* uygulaması (Monte Carlo'nun K sıralamaları üzerinde). K'nin yaklaşım doğruluğuna nasıl etkisi olur?
3. Satışa kadar koalisyon oluşturma adımını uygulayın: ajanlar takımlara birleşip bir birim olarak teklif verebilir. Hangi koalisyonlar oluşur?
4. Google Araştırma mekanizma tasarımını okuyun. Eğer ihlal edilirse doğruluğu kırırsa bir varsayım tanımlayın. LLM ortamında bu başarısızlık modunun nasıl görüneceği?
5. AAMAS 2025 merkezi olmayan LaMAS makalesini okuyun. Sintez bir görevde Shapley'nin 10 ajanın üzerinde adımını uygulayın. Tam hesaplama ne kadar sürer? 100 çekim ile örnekleme ne kadar yakındır?

## Anahtar Terimler

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| DePIN / 去中心化物理基础设施 | "Decentralized physical infrastructure" / "去中心化物理基础设施" | Token-incentivized compute/storage/bandwidth. Bittensor, Akash, Render. / Token 激励的计算/存储/带宽。Bittensor、Akash、Render。 |
| DID / 去中心化标识符 | "Decentralized identifier" / "去中心化标识符" | W3C spec for portable IDs. Agent reputation binds to DID, not to a platform. / W3C 便携 ID 规范。Agent 声誉绑定到 DID，而非平台。 |
| ERC-4337 / 账户抽象 | "Account abstraction" / "账户抽象" | Contract accounts that can sponsor gas, enabling agent payments. / 可以赞助 gas 的合约账户，使 Agent 支付成为可能。 |
| Shapley value / Shapley 值 | "Fair credit attribution" / "公平信用归因" | Unique allocation satisfying efficiency, symmetry, linearity, null. / 满足效率、对称、线性、零贡献者的唯一分配。 |
| Second-price auction / 二价拍卖 | "Vickrey auction" / "Vickrey 拍卖" | Truthful mechanism: winner pays second-highest bid. Monotone aggregation compatible. / 诚实机制：获胜者支付第二高出价。兼容单调聚合。 |
| Reputation capital / 声誉资本 | "Accumulated quality score" / "累积质量分数" | DID-bound score from confirmed contributions; decays over time. / DID 绑定的来自确认贡献的分数；随时间衰减。 |
| Agentic DAO / Agent DAO | "Agents + humans govern" / "Agent + 人类治理" | DAO with agent voters as first-class, voting power tied to reputation. / Agent 投票者作为一等公民的 DAO，投票权与声誉绑定。 |
| TAO / FET / GPU credits / Token 面额 | "Token denominations" / "Token 面额" | Bittensor TAO, Fetch.ai FET, various DePIN tokens. / Bittensor TAO、Fetch.ai FET、各种 DePIN token。 |

## Daha fazla okumak

- [The Agent Economy](https://arxiv.org/abs/2602.14219) 5 katmanlı ajan-ekonomik yığının 2026 tarihli araştırması
- [Google Research — Mechanism design for large language models](https://research.google/blog/mechanism-design-for-large-language-models/) Monoton birleştirme ile simgesel açık artırmalar
- [AAMAS 2025 — decentralized LaMAS](https://www.ifaamas.org/Proceedings/aamas2025/pdfs/p2896.pdf) Shapley değeri kredi atributı
- [Bittensor TAO documentation](https://docs.bittensor.com/) Alt ağ yapısı ve ödül dağılımı
- [Fetch.ai / ASI Alliance](https://fetch.ai/) ASI-1 Mini LLM ve FET token
- [W3C Decentralized Identifiers (DIDs) spec](https://www.w3.org/TR/did-core/) Kimlik Temel
