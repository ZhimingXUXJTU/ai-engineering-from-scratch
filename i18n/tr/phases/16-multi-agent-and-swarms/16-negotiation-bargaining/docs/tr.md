# # Ve anlaşma ve anlaşma #

> Agentler kaynakları, fiyatları, görev tahsislerini ve şartları müzakere eder. 2026 referans göstergesi açık: müzakere alanı (arXiv:2402.05863) LLM'lerin kişi manipülasyonu ("ümitsizlik" yoluyla ödemeyi %20'lik bir artış sağlayabileceğini gösterir; "Bordaj yeteneklerini ölçmek" (arXiv:2402.15813) alıcıyı satandan daha zor olduğunu ve ölçekleri  onlara yardımcı olmadığını gösterir.**OG-Narrator**(deterministik teklif üreticisi + LLM anlatıcısı) anlaşma oranını 26.67%'den 88.88%'ye yükseltti; Büyük ölçekli özerk müzakere yarışması (arXiv:2503.06416) yaklaşık 180k müzakere gerçekleştirdi ve buldu ki**chain-of-thought-concealing**Bhattacharya et al. 2025 Harvard müzakere projesi ölçümleri üzerinde Llama-3 en etkili, Claude-3 agresif, GPT-4 en adil sıralanmış. Bu ders Sözleşme Net Protokolü (FIPA ataları, Ders 02), LLM tarzı bir alıcı / satıcı tel, OG-Narrator tarzı bir parçalanma yürütür ve her yapısal seçimle nasıl anlaşma oranı değişir ölçüyor.

> **【中文解读】**Bu bölüm, kaynak dağılımında ve görev dağılımında danışmanlık ve pazarlık stratejilerini tanımlar.

> **【拓展：negotiation bargaining→具体应用】**协商和讨价还价, çoklu ajanın kaynak dağıtımının temel mekanizmasıdır.


**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib) | **语言:** Python（标准库）
**Prerequisites:** Phase 16 · 02 (FIPA-ACL Heritage), Phase 16 · 09 (Parallel Swarm Networks) | **前置知识:** Phase 16 · 02（FIPA-ACL 遗产），Phase 16 · 09（并行群体网络）

>  **【前置】**Öte yandan, bu süre içinde, bir süre önce, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir sürece, bir sürece, bir sürece, bir sürece, bir sürececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececece
>  **【类比】**Agent 协商 = "二手市场砍价"──LLM 通过 persona 操纵(装穷)能多 20%;隐藏推理过程的 Agent 赢对手看不到你的底线──OG-Narrator 把协商拆为"确定性提议生成"+"LLM 叙述",deal rate 26%→89%──模型差异:Llama-3 最有效、Claude-3 强势、GPT-4公平 最选即选模型选风格──
**Time:** ~75 minutes | **时间:** ~75 分钟

## Sorunlar sorunun giriş

İki ajan bir fiyat konusunda anlaşmak zorunda. saf dil istekleriyle kendileri için bırakılan 2024-2026 LLM'ler şaşırtıcı derecede düşük oranlarda (ArXiv'de sıkı parametreli pazarlıklarda ~27%) anlaşmalar kapatır.

> İki Ajanın fiyat anlaşması gerekiyor. 2024-2026 yılları için LLM'nin gelişim oranı şaşırtıcı derecede düşük. Arxiv:2402.15813'ün yoğun parametre fiyatı arasında %27 civarında.

LLM'lerin iki işi birleştirmesidir  teklif karar vermesi ve teklif anlatması. OG-Narrator bunları ayırmıştır: bir belirleyici teklif jeneratörü sayısal hareketleri hesaplar; LLM sadece anlatır.

> 根本问题是LLM 混了两个任务决定报价和叙述报价――OG-Narrator 将两者分离:确定性报价生成器计算数字变动;LLM 仅负责叙述――成交率跃升至约89%――

Bu, klasik bir çok ajan bulguyu yansıtır: mekanizmayı iletişim katmanından ayırmak kazanır. Sözleşme Ağ Protokolü (FIPA, 1996; Smith, 1980) referans görev piyasası mekanizmasıdır.

> Bu, klasik bir çok ajanın ortaya çıkışını yansıtır: 将机机制与通信层解是胜之道.

## Konsept merkezi konsept

### Sözleşme Net, bir paragraf

Smith'in 1980'deki Sözleşme Net Protokolü:**manager**yayımlar a **call for proposals (cfp)**- ...**bidders**Cevap ver .**propose**tekliflerini içeren mesajlar; yöneticisi bir kazananı seçip gönderir **accept-proposal**Kazananın ve**reject-proposal**Kazanan işi yapar.**refuse**FIPA bunu şöyle kodlaştırdı:`fipa-contract-net`etkileşim protokolü.

> Smith 1980 yılında:**管理者**广播**提案请求（cfp）**- ...**投标人**回复 içerir fiyat**提案**消息; administrator seçen kazananı并向获胜者发送**接受提案**,向落选者发送**拒绝提案**❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖**拒绝**(投标人拒绝提案) FIPA将其编码为`fipa-contract-net`交互协议。

### Neden OG-Narrator kazanıyor?

"Dil Modellerinin Tartışma Yeteneğini Ölçmek" (arXiv:2402.15813) şunları belirtti:

> "衡量语言模型的议价能力" (arXiv:2402.15813) şunları gözlemliyor:

- LLM'ler genellikle pazarlık kurallarını çiğnerler (makasız fiyatlara teklif, karşı tarafın ZOPA'sını görmezden gel).
  Çinçe Çevirimiçi:LLM  sık sık karşıya gelir kurallarını 
- Kötü şekilde demirlenirler (kötü ilk teklifleri kabul ederler; stratejik değil sembolik miktarlarda karşı teklifler).
  Çin dilinde: 定效差 (定效差)                                                                                                                                                                                                                                                        
- Büyük modeller benzer stratejik hatalarla daha makul bir dil oluşturur.
  Çinçe çevirisi: Sadece ölçeklendirme ile bu sorunları çözemez. Daha büyük modeller daha mantıklı bir dil üretir, ancak benzer stratejik hatalar vardır.

OG-Narrator'ın parçalanması:

```
           ┌──────────────────┐        ┌──────────────────┐
  state  → │ offer generator  │ price → │  LLM narrator    │ → message
           │  (deterministic) │        │  (writes the     │
           │                  │        │   human-style    │
           └──────────────────┘        │   accompaniment) │
                                       └──────────────────┘
```

Teklif üreticisi klasik bir müzakereler stratejisi: Rubinstein pazarlama modeli, Zeuthen stratejisi veya basit bir fiyat karşılığı. LLM anlatır. Mesaj belirleyici fiyatı ve doğal dil çerçevesini içerir.

İşletme oranı artıyor çünkü:
- Fiyatlar pazarlık bölgesinde kalır.
- Anchorlar stratejik, duygusal değil.
- Yüksek Lisans, iyi olan şeyi yapar: yazmayı.

> Çıkacak oranı artıyor çünkü:
> - 价格保持在议价区间内──
> - 点是战略性的,而非情绪化──
> - LLM Yapmayı İyi Yapmak:

### Aren'de yapılan görüşmeler

ArXiv:2402.05863 kanonik referans değerini sunar.

> ArXiv:2402.05863  provided规范基准──

- LLM'ler, personaları benimseyerek ödemeyi %20'e iyileştirebilir ("Cüman günü bu satmayı umutsuzluğa düşüyorum")  persona manipülasyonu gerçek bir taktiktir.
  Çin Çeviri:LLM, insanlık kullanılarak gelirlerin %20'i artmasına yardımcı olur.
- Adaletli/kooperatif ajanlar, karşı taraflı kişiler tarafından sömürülür; savunma açıkça karşı duruş gerektirir.
  Çinçe Çevirimiçi: adil/ kooperatif ajanı, karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı
- Simetrik çiftleşmeler, referans senaryolarının yaklaşık %40'ında eşitsiz sonuçlara doğru yaklaşıyor.
  Çinçe Çevirisi: karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı

Bu "LLM'ler kötü müzakereci" değil. "LLM'ler, sömürülebilir kısımları da dahil olmak üzere, insanlar gibi çok fazla müzakere ediyor".

> Bu "LLM kötü müzakereler" değil, "LLM'nin müzakerelerinin insan gibi olduğu, kullanılabilir kısımları da dahil" anlamına gelmez.

### Düşünce zinciri gizlenmesi

Büyük ölçekli özerk müzakere yarışması (arXiv:2503.06416) birçok LLM stratejisi boyunca yaklaşık 180 bin müzakere gerçekleştirdi.

> Büyük çaplı kendi kendine müzakere yarışması ((arXiv:2503.06416) birçok LLM stratejisi üzerinde yaklaşık 180.000 kez müzakere edildi.

- Eğer bir ajan "Ben sadece gideceğim" yazdırırsa$75; my reservation price is $70"'lik bir çizik çubuğuna, karşısının okuduğu.
  Eğer ajanı "ben sadece çıkardım"$75；我的保留价是 $70'lik baskı açık görünen bir taslakta, ele alın.
- Kazananlar stratejiyi özel olarak hesaplar; çıkış kanalı sadece teklif ve minimum gereksinimli anlatımı içerir.
  Çinçe çevirisi: 获胜者私下计算策略;输出通道只包含报价和最低限度的叙述──

Bu, klasik oyun teorisinin 2026'daki yankısıdır (Aumann 1976 akılcılık ve bilgi üzerine): özel değerlendirme maliyetlerini ödemenizi ortaya çıkarmak. LLM'ler bunu sezgisel olarak fark etmez ve mutlulukla karşılığı için görünür hale gelen mantık izlerinde özürlerini yazırlar.

> Bu klasik bir blog teorisiydi. Aumann 1976                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   

Mühendislik götürme: özel-scrappad bağlamını kamu mesaj bağlamından ayırmak.

> 工程要点:将私人草稿本上下文与公开消息上下文分离──これは可選──

### Bhattacharya et al. 2025  model sıralamaları

Harvard müzakere projesi ölçümleri (elçipe müzakere, BATNA saygısı, çıkar karşılıklılığı):

> Bu nedenle, bu konudaki en önemli konularda, bu konularda, bir araya gelmek ve bir araya gelmek için, bir araya gelmek gerekir.

- **Llama-3**En etkili olan pazarlık (işleme oranı + ödeme) oldu.
  Çeviri:**Llama-3**Aralık ayında yapılan anlaşmaların en etkili sonuçları:
- **Claude-3**En agresif müzakerelerden biriydi (yüksek demir, geç uzlaşma).
  Çeviri:**Claude-3**En saldırgan konuşmacı.
- **GPT-4**en adil (parlamalar arasındaki ödeme farkında en küçük fark)
  Çeviri:**GPT-4**En az eşitlik (sadece en az)

Bu 2025 anında bir anlık fotoğraf. Konu Nisan 2026'da hangi model kazanacağı değil.  farklı temel modellerin sürekli müzakere tarzları olmasıdır. Heterogene ensembler (Düşünme 15) bunu çeşitlilik kaynağı olarak içerir.

> Bu 2025 yılındaki hızlı bir resimler. Temel, 2026'da hangi model başarılı olacak değil, farklı bir temel modelin kalıcı bir müzakereler biçimi olacak.

### Sözleşme Net + LLM üzerinden görev dağılımı

LLM çoklu ajan için Contract Net'in modern yeniden kullanımı:

> 合同网在现代 LLM 多 Agent 中中重用:

1. Yönetim ajanı bir görevi birimlere ayırır.
   Çeviri: Manager Agent görevleri birimlere bölmek üzere
2. Yayınlar `cfp`İşçi ajanlarına görev tanımı ile.
   Çinçe Çevirisi:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       `cfp`- Evet.
3. Her işçi bir teklif gönderir: `(price, eta, confidence)`Fiyatı token, hesap ünitesi veya dolar olabilir.
   Çinçe Çevirimi: her işçi bir teklif geri döndü:`(price, eta, confidence)`, fiyatı simge ̇ hesap birimi veya dolar olabilir.
4. Yöneticiler kazananları (işlerine bağlı olarak tek veya birden fazla) ve ödülleri seçer.
   Çinçe çevirisi: administratorı seçen kazananı (单个或多个,取决于任务)并授标──
5. reddedilen işçiler başka görevlere teklif verebilirler.
   Çinçe Çevirisi:被拒绝工作者可以竞标其他任务──

Bu, 100 işçinin üzerinde uzanır çünkü koordinasyon yayın ve cevaplama, senkroni sohbet değil.

> Bu, 100'den fazla işçiye genişletebilir, çünkü koordinasyon, bir iletişim-response modudur, aynı zamanda sohbet değil.

### LLM-Stakeholders Interactive Negotiation

NeurIPS 2024 (https://proceedings.neurips.cc/paper_files/paper/2024/file/984dd3db213db2d1454a163b65b84d08-Paper-Datasets_and_Benchmarks_Track.pdf) çoklu oyunculuk oyunlarını **secret scores**ve **minimum-acceptance thresholds**. Her paydaşın özel hizmetleri vardır; LLM bunları mesajlardan çıkarmalıdır. Bu, iki taraflı pazarlamanın N-partiya koalisyon oluşumuna genelleştirilmesidir.

> NeurIPS 2024  başlatıldı**秘密分数**和**最低接受阈值**Bu, farklı yapılandırılmış işçi kapasitesi olan üretim görev pazarına uygulanmaktadır.

### Hikaye-mexanizm kuralı

2024-2026 müzakerelerinin tüm referans kriterleri boyunca, tutarlı mühendislik kuralı:

> LLM'nin teklifini hesaplamasına izin vermeyin.

> 让LLM 叙述──不要让LLM 计算报价──

Teklif bir sayı ( fiyat, ETA, miktar) olması gerekiyorsa, onu müzakere durumundan belirleyici olarak oluşturun ve LLM'nin çerçevelemeyi üretmesini sağlayın. Teklif bir teklif yapısı (iş parçalanması, rol atama) olması gerekiyorsa, LLM'nin onu hazırlamasına izin verin, ancak göndermeden önce bir şema ve zorluk kontrolüne göre onaylayın.

> Eğer teklif gerekirse, dijital bir şekilde üretilmelidir, ancak bir süre önce gönderilmelidir.

## Yapın.
```figure
a5-og-narrator
```

## Yapın

`code/main.py`Uygulamaları:

- `ContractNetManager`- Evet .`ContractNetTask`- Evet .`Bid` yöneticiler + teklif verenler, yayın cfp, teklif toplama, ödül.
  Çeviri:`ContractNetManager`- Evet.`ContractNetTask`- Evet.`Bid` 管理者 + 投标人,广播 cfp,收集提案,授标──
- `og_narrator_bargain(state, rng)` OG-Narrator alıcı: Deterministik Zeuthen tarzı orta noktaya doğru koncession.
  Çeviri:`og_narrator_bargain` OG-Narrator 买方:确定性 Zeuthen 风格向中间点让步──
- `seller_response(state, rng)` Deterministik satıcı karşı teklif politikası (ereki stil için yapısal temel gerçeklik).
  Çeviri:`seller_response` 确定性卖方回价策略 (BİÇİNİŞİK)
- `naive_llm_bargain(state, rng)` tüm LLM pazarlamacılarını simüle eder: genellikle ZOPA dışında yüksek farklı fiyatlar seçer.
  Çeviri:`naive_llm_bargain` 模拟全 LLM 议价者:以高方差选价,经常超出 ZOPA。
- Ölçüm: 1000 deneme üzerinde işlem oranı, test başına örnek alınan taze rezervasyon fiyatları ile.
  Çinçe Çevirimi: ölçüm: 1000 kez deneme, her deneme yeniden alınması

Çık:

```
python3 code/main.py
```

Beklenen çıkış: naif-LLM anlaşma oranı ~65-75%; OG-Narrator anlaşma oranı ~85-95%; 15-25 puan farkı anlatmadan teklif neslini parçalanmanın yapısal avantajıdır.

> 预期输出:朴素 LLM 成交率约65-75%;OG-Narrator 成交率约85-95%;15-25 个百分点差是将报价生成与叙述解的结构优势──加上一个三个投标者和一个任务的合同网任务市场分配示例──

## Kullanın Kullanın

`outputs/skill-bargainer-designer.md`Bir pazarlama protokolü tasarlıyor: kim teklifler üretir (deterministik veya LLM), kim anlatır, özel kırıntı çubuğunun kamu mesajlarından nasıl ayrıldığı ve pazarlama oranının nasıl izlendiği.

> `outputs/skill-bargainer-designer.md`设计一个议价协议:谁生成报价 (),谁叙述,谁叙述,谁草稿本如何与公开消息分离以及如何监控成交率──

## Gönderin.

Üretim pazarlık kontrol listesini:

- **Separate scratchpad.**Özel devlet asla karşı tarafın bağlamına ulaşmaz.
  Çeviri:**分离草稿本。**Özel durum asla karşıya gelmez. Bu anlaşılmaz.
- **Deterministic offer generation.**Fiyatlar, miktarlar, ETA'lar: hesaplayın, istek vermeyin.
  Çeviri:**确定性报价生成。**价格、数量、ETA:计算, don't提示──
- **Validate all incoming offers**Protokol sınırında,ZOPA'dan çıkmış teklifleri reddet.
  Çeviri:**验证所有传入报价**根据模式──在协议边界拒绝 ZOPA 外的报价──
- **Bound rounds.**3-5 mermi maksimum; duraklama durumunda aracıya yüksel.
  Çeviri:**限制轮次。**Maksimum 3-5 tur; ölmüş zaman yükseltilmiş.
- **Measure deal rate and payoff variance**Düşen bir anlaşma oranı bir semptomdur  genellikle hızlı bir sürüş veya karşı taraflı bir saldırı.
  Çeviri:**持续测量成交率和收益方差。**Düşen dönüşüm oranı genellikle bir gösterge veya saldırı olarak belirtilir.
- **Log all rejected proposals**Sözleşme ağları yöneticileri için, kaybeden teklif verenlerin nedenini anlaması gerekir.
  Çeviri:**记录所有被拒绝的提案**及确定性理由── Kontrat ve İnternet Yöneticisi için,落选投标人 nedenleri anlamalıdır──

## Egzersizler.

1. Çık .`code/main.py`OG-Narrator'un anlaşma oranında naif bir LLM'den daha iyi olduğunu doğrulayın.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`code/main.py`❖ OG-Narrator'ın başarıyla başarılı olması için daha iyi bir LLM'den daha iyi olduğunu belirleyin.
2. Uygulama**persona-based payoff improvement**Satın almacı sadece anlatımda "Bu hafta satın almak için umutsuz" karakterini benimseyerek, değişmeyen bir jeneratör sunuyor.
   Çeviri: gerçekleştirmek**基于人格的收益改进**(arXiv:2402.05863)  Satın almacıları sadece anlatımda "本周急需購買" kişiliğini kullanıyor, fiyat üreticisi değişmiyor.
3. Düşünce zincirini uygula **concealment**Bu nedenle, bir kişiye ait olan bir şey, bir kişiye ait olan bir şey değil, bir kişiye ait olan bir şey.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri**隐藏**Bu yüzden, bu konuda bir şey yapmamalıyız.
4. Tasarruf fiyatı rezervi olan N-biyer açık artırmasına kadar uzatın. Tüm teklifler rezervi aşırınca, yöneticiler en düşük fiyat ile en yüksek kalitede arasında nasıl karar verirler? Hangi ödül kuralını seçersiniz ve neden?
   Çinçe çevirisi: N 投标人拍卖将合同网扩展以保留价格为 N 投标人拍卖. Bütün teklifler, tutulma fiyatından fazla olduğunda, yöneticiler en düşük fiyat ile en yüksek kalite arasında nasıl seçim yapabilirler?
5. Bhattacharya et al. 2025'i Harvard müzakere projesi ölçümleri üzerine okuyun. Farklı stiller (agresif vs adil) ile iki pazarlamacı uygulayın.
   Çin dilinde:Bhattacharya  et al. 2025 yılındaki Harvard görüşmesi hedefleri üzerine makale.

## Anahtar Terimler

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Contract Net / 合同网 | "Task market" / "任务市场" | Smith 1980, FIPA 1996. cfp + propose + accept/reject. The canonical task-market. / Smith 1980, FIPA 1996。cfp + propose + accept/reject。规范的任务市场。 |
| ZOPA / 可能协议区 | "Zone of possible agreement" / "可能协议区域" | Overlap between buyer's max and seller's min. Offers outside it cannot close. / 买方最大值和卖方最小值的重叠。超出此范围的报价无法成交。 |
| BATNA / 最佳替代方案 | "Best alternative to a negotiated agreement" / "谈判协议的最佳替代方案" | Your fallback if this deal fails. Sets your reservation price. / 如果交易失败的后备方案。设定你的保留价。 |
| OG-Narrator / OG-叙述者 | "Offer generator + narrator" / "报价生成器 + 叙述者" | Decomposition: deterministic offer, LLM narration. / 分解：确定性报价，LLM 叙述。 |
| Zeuthen strategy / Zeuthen 策略 | "Risk-minimizing concession" / "风险最小化让步" | Classical offer-generator that concedes based on risk limits. / 基于风险限制让步的经典报价生成器。 |
| Rubinstein bargaining / Rubinstein 议价 | "Alternating-offer equilibrium" / "交替报价均衡" | Game-theoretic model for infinite-horizon bargaining with discounting. / 带折现的无限期议价博弈论模型。 |
| CoT concealment / CoT 隐藏 | "Hide your reasoning" / "隐藏推理" | Winners in arXiv:2503.06416 kept private scratchpads; public channel shows offer only. / arXiv:2503.06416 的获胜者保持私人草稿本；公开通道只显示报价。 |
| Persona manipulation / 人格操纵 | "Emotional posturing" / "情绪姿态" | arXiv:2402.05863: ~20% payoff gain from desperation/urgency personas. / arXiv:2402.05863：绝望/紧迫人格带来约 20% 的收益增益。 |

## Daha fazla okumak

- [NegotiationArena](https://arxiv.org/abs/2402.05863) referans değer; kişi manipülasyonu ve sömürü bulguları
- [Measuring Bargaining Abilities of Language Models](https://arxiv.org/abs/2402.15813) OG-Narrator ve alıcı-satıcı-kısıtlayıcı sonucu
- [Large-Scale Autonomous Negotiation Competition](https://arxiv.org/abs/2503.06416) ~ 180k müzakereler; düşünce zinciri gizleme kazanır
- [LLM-Stakeholders Interactive Negotiation (NeurIPS 2024)](https://proceedings.neurips.cc/paper_files/paper/2024/file/984dd3db213db2d1454a163b65b84d08-Paper-Datasets_and_Benchmarks_Track.pdf)Gizli araçlarla çoklu oyunculuk oyunları
- [Smith 1980 — The Contract Net Protocol](https://ieeexplore.ieee.org/document/1675516) Klasik mekanizma, IEEE işlemleri bilgisayarlar
