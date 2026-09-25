# FIPA-ACL ve Konuşma Yasası Mirası

> MCP'den önce, A2A'dan önce, FIPA-ACL vardı. 2000 yılında Akıllı Fiziksel Ajanlar için IEEE Vakfı, yirmi performatif, iki içerik dili ve bir dizi etkileşim protokolü ile bir ajan iletişim dili onayladı  sözleşme net, abonelik/bilgi, talep-ne zaman. Endüstriye düştü çünkü ontoloji genel masrafları web için çok ağırydı, ancak çoklu ajan sistemlerinin LLM canlanımı resmi semantik olmadan sessizce aynı fikirleri yeniden uyguluyor: JSON sözleşmeleri performatifler için, doğal dil ontolojiler için yer almaktadır. Bu ders, FIPA-ACL'yi ciddiye alır, böylece 2026 protokolü kararlarının hangi yenilikleri yeniden icat ettiğini ve bugünkü dalgaların 2000'lerde çözülen sorunları yeniden keşfetmeye çalıştığını görebilirsiniz.

> **【中文解读】**Bu dersde FIPA-ACL   遗产多 系统通信协议的历史标准与现代发展──2000 yılına ait 20 adet yapısal davranışlar (performatifler) 、内容语言和交互协议, tam olarak 2026 yılındaki MCP/A2A/ACP'ler yeniden geliştirmekte olan bir şey: JSON 契约替换施事行为,自然语言替换本体──

> **【拓展：FIPA ACL 遗产→具体应用】**FIPA ACL (Inteligent Physical Agents Foundation for Agent Communication Language) 1990-2000 yılları arasında bir grup ajanın iletişim standartlarıdır. FIPA  organizası 2013 yılında dağıldı ancak temel düşüncesi ise, modern bir grup ajanın iletişim protokolünü hâlâ etkiliyor.

>  **【前置】**Öğrenci: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sınıf: Sını

>  **【类比】**FIPA-ACL = "AI 界的拉丁语"──2000 yılın standartları,2026 yılın protokolü(MCP/A2A) büyük miktarda fikirlerini sürdürmek──区别:FIPA 用形式化本体(重)、现代协议用 JSON+自然语言(轻)──学历史的价值:避免重复覆FIPA 因为"本体太重"而死,现代协议要保持轻量──

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib) | **语言:** Python（标准库）
**Prerequisites:** Phase 16 · 01 (Why Multi-Agent) | **前置知识:** Phase 16 · 01（为什么需要多 Agent）
**Time:** ~60 minutes | **时间:** 约 60 分钟

## Sorunlar sorunun giriş

> **【中文解读】**2026 yılının ajan 协议 görünüşe yüzlerce insan tarafından yayılmış,实则大多在重走一条二十年前的决策树:言语行为理论(话语即行动)→ KQML 线协议 → FIPA-ACL 标准化 → 因本体太重而被Web 技术淘汰──本节给出判断框架:看新协议时,先问它应对FIPA 决策树上的哪个节点──

2026 ajan-protokolu manzarası yoğun: araçlar için MCP, ajanlar için A2A, kurumsal denetim için ACP, merkezi olmayan güven için ANP, doğal dil içerikleri için NLIP, CA-MCP ve iki düzine araştırma önerisi.

> 2026 yılının ajan anlaşması alanı oldukça sıcak: MCP araçlara, A2A'ya, Agent'e, ACP'ye, işletme denetimine, ANP'ye, güvenin merkezileştirilmesine, NLIP'ye, doğal dil içeriğine ve CA-MCP'ye ve yirmi araştırma önerisine göre. Her bir kural kendini temel olarak iddia eder.

Dürüst bir şekilde, çoğu, 20 yıllık bir karar ağacını yeniden keşfediyor. Austin (1962) ve Searle (1969) 'dan konuşma-işleyiş teorisi bize "sözler eylemlerdir". KQML (1993) bunu bir tel protokolüne dönüştürdü. FIPA-ACL (takatlenmiş 2000), referans standartlaştırmasını üretti: yirmi performatif, içerik dilleri SL0/SL1, sözleşme ağı ve abone-bilgi için etkileşim protokolleri. JADE ve JACK Java referans platformlarıydı. 2010 civarında çabalar sönmüştü çünkü ontoloji üst ücreti çok ağırydı ve web kazanıyordu.

> 诚实的看法是, bunların çoğu, yirmi yıl önce çok spesifik bir karar ağacını yeniden keşfediyor. Austin 1962 ve Searle 1969'daki sözcük davranış teorisi bize "话语即行动"  KQML 1993) ile bağlantı protokolü olarak çevrildi. FIPA-ACL 2000 yılında onaylandı) referans standartlaşımı oluşturdu:

MCP'ye baktığınızda`tools/call`Bu nedenle, A2A'nın görev yaşam döngüsü veya CA-MCP'nin paylaşılan bağlam depoları, FIPA kararlarının daha yumuşak ve JSON'a özgü bir yeniden dönüşümünü görüyor.

> MCP'yi incelediğinde`tools/call`、A2A'nın görev yaşam döngüsü veya CA-MCP'nin paylaşımında aşağıdaki deposu sırasında, FIPA  kararlarının daha yumuşak ve JSON'dan gelen bir özetini görürsünüz. Bu mirasın size iki şeyi anlattığını anlamak: hangi yeni "inova"lar aslında yeniden ortaya çıkarıldı, ve yeni kurallar eski başarısızlık modellerini yeniden keşfedeceklerini öğrenmek için.

## Konsept merkezi konsept

> **【中文解读】**Bu bölümde, "FIFA-ACL" adlı bir programın yayımlanması ve yayımlanması hakkında bilgi edinip, bu programın başlatılması için, "FIFA-ACL" adlı bir programın yayımlanması ve yayımlanması için, "FIFA-ACL" adlı bir programın yayımlanması ve yayımlanması için, "FIFA-ACL" adlı bir programın yayımlanması ve yayımlanması için, "FIFA-ACL" adlı bir programın yayımlanması ve yayımlanması için, "FIFA-ACL" adlı bir programın yayımlanması için, "FIFA-ACL" adlı bir programın yayımlanması için, "FIFA-ACL" adlı bir programın yayımlanması için, "FIFA-ACL" adlı bir programın yayımlanması için, "FIFA-ACL" adlı bir programın yayımlanması için, "FIFA-ACL" adlı bir programın yayımlanması için, "FIFA-ACL" adlı bir programın yayımlandı.

### Konuşma aktları, tek bir paragraf

> **【中文解读】**Bir bölüm konuşma açık teori kök: bazı cümleler dünyayı tanımlamakta değil, dünyayı değiştirmekte. Searle bunları beş sınıflara ayırır; KQML bu felsefe kavramını uygulamaya kolaydırılabilir bir programlı bir bağlama olarak değiştirir; FIPA-ACL                                                                                                                                                                                                                                                                                                                                                                                                                                                              

Austin bazı cümlelerin dünyayı tanımlamadığını fark etti  değiştirirler. "Vadiyorum". "İsteyim". "Bilgiliyim". "Bu performanssal ifadelerdi". Searle beş kategorisi resmileştirdi: asertif, yönetici, komisyon, ifadeci, açıklayıcı. KQML (Finin et al., 1993) bunu yazılım ajanları için işlevsel hale getirdi: bir mesaj performatif (hareketi) artı içeriğe (hareketin ne hakkında olduğu) sahiptir. FIPA-ACL KQML'in boşluklarını temizledi ve yirmi kadar performatif standartlaştırdı.

> Austin bazı cümleleri dünyayı değiştirmek için tanımlamadığını belirtti. "My promise. " "My request. " "I declare. " Searle bunları beş kategoriye şekillendirdi: "Fromance. "

### FIPA'nın yirmi performatifleri ( kısmi liste)

| Performative | Intent |
|---|---|
| `inform` | "I tell you P is true" |
| `request` | "I ask you to do X" |
| `query-if` | "Is P true?" |
| `query-ref` | "What is the value of X?" |
| `propose` | "I propose we do X" |
| `accept-proposal` | "I accept the proposal" |
| `reject-proposal` | "I reject the proposal" |
| `agree` | "I agree to do X" |
| `refuse` | "I refuse to do X" |
| `confirm` | "I confirm P is true" |
| `disconfirm` | "I deny P" |
| `not-understood` | "Your message did not parse" |
| `cancel` | "Cancel the ongoing X" |
| `cfp` | "Call for proposals on X" |
| `subscribe` | "Notify me when X changes" |
| `failure` | "I tried X and failed" |

Tam listesi var .`fipa00037.pdf`Bu konunun bir kısmını akılda tutmak değil, bunların her biri bir LLM protokolüyle aynıdır.

> 完整列表在 `fipa00037.pdf`(FIPA ACL 消息结构) 中── öncelik hafıza üzerinde değil, her birimizin LLM 协议ı ile sonuçta yeniden eklenmiş olan orijinal dil üzerinde.

### Kanonik FIPA-ACL mesajı

> **【中文解读】**Sınıfı sadece yedi tane.`content`- Ne? - Hayır.`conversation-id`和 `reply-with`Modern değişim sistemleri sürekli yeniden keşfedilen şeyler; bunlar olmadan çoklu değişim yapamazlar.

```
(inform
  :sender       agent1@platform
  :receiver     agent2@platform
  :content      "((price IBM 83))"
  :language     SL0
  :ontology     finance
  :protocol     fipa-request
  :conversation-id   conv-42
  :reply-with   msg-17
)
```

Protokol zarfını taşıyan yedi alan; bir alan (`content`Diğer alanlar, her tekrar deneme, ipleme ve ontolojiyi JSON protokolüne eklediğinizde tam olarak yeniden icat ettiğiniz şeydir.

> 七个字段承载协议信封;一个字段(`content`) yüklenme geçerli yüklenme. Geri kalan kısımlar, her seferinde yeniden deneme, 线程和本体加上 JSON 协议上重新发明的.

### İki eski platform

**JADE**(Java Agent DEvelopment framework, 19992020s) en çok kullanılan FIPA uyumlu çalıştırma süresiydi. Ajanlar bir temel sınıfı genişletti, ACL mesajları değiştirdi, konteynerler içinde çalıştı ve "hareketi" kullanarak koordinat etti.

> **JADE**(Java Agent 开发框架, 1999-2020 年代) en sık kullanılan FIPA 兼容运行时――Agent 继承基类,交换 ACL 消息,在容器内运行,并使用"行为"进行协调――交互协议库附带合同网、订阅-通知、请求-当和提议-接受――

**JACK**(Agent Oriented Software, ticari) FIPA mesajlarının üstesinden gelen BDI (İman-İstelik-İstelik) mantıklamasını vurguladı.

> **JACK**(Agent Oriented Software, Commercial Products) FİPA 消息之上 BDI yapılması üzerinde vurgu

Web stack çoklu ajan kullanım durumlarını yediğinde her ikisi de düştü. MCP ve A2A 2026'daki çalıştırma zamanındaki "konteynerler"dir.

> Bir kere Web 技术吞了多代理用例, ikisi de çöktü. MCP 和 A2A 2026 yılının "容器" olarak kullanılır.

### FIPA'nın neden kaybolduğunu

- **Ontology overhead.**FIPA , analiz için ortak bir ontoloji gerektirdi .`content`Ontolojiler konusunda anlaşmak yıllarca süren standart süreçtir.
  Çeviri:**本体开销。**FIPA                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            `content`                                                                                                                                                                                                                                                              
- **Formal semantics nobody used.**SL (Semantik Dil) sıkı gerçek koşulları verdi, ancak çoğu üretim sistemi serbest biçim içerik kullanıyordu ve formallığı görmezden gelmişti.
  Çeviri:**没人用的形式语义。**SL (语义语言) ciddi gerçek değer koşulları sağladı, ancak çoğu üretim sistemi özgür biçim içerikleri kullanıyor ve biçimçiliği göz ardı ediyor.
- **Tooling lock-in.**JADE sadece Java'da, Jack ise ticari bir programdı.
  Çeviri:**工具锁定。**JADE 仅支持Java;JACK 是商业的──多语言团队绕过了两者──
- **The internet won the stack.**REST, sonra JSON-RPC, sonra gRPC ACL'nin taşıma yerini aldı.
  Çeviri:**互联网赢得了技术栈。**REST, sonra JSON-RPC, sonra gRPC ACL'nin aktarımını değiştirdi.

### LLM yeniden canlandırılması FIPA-lite

> **【中文解读】**FIPA'yı`request`Ülkemiz`tools/call`Ve çıkış: Aynı bir şifrenin içinde, farklı dil biçimleri, ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ 

FIPA'yı karşılaştırın `request`Bir MCP'ye`tools/call`- ...

> FIPA'yı`request`MCP ile`tools/call` karşılaştırma yapın:

```
(request                                {
  :sender  agent1                         "jsonrpc": "2.0",
  :receiver tool-server                   "method":  "tools/call",
  :content "(lookup stock IBM)"           "params":  {"name":"lookup_stock",
  :ontology finance                                   "arguments":{"symbol":"IBM"}},
  :conversation-id c42                    "id": 42
)                                        }
```

Aynı zarf, farklı sözcük. Her ikisi de taşıyor: kim, kim, niyet, payload, ilişki kimliği.

> Aynı şifreler, farklı dil biçimleri. İkisi de taşıyor: kim, kime, niyet, yükleme, bağlantı kimliği.

Liu et al. tarafından 2025 tarihli araştırması ("A Survey of Agent Interoperability Protocols: MCP, ACP, A2A, ANP", arXiv:2505.02279) bu soyunu açıkça gösterir: MCP araç kullanımı konuşma eylemlerine, A2A ajan-teke konuşma eylemlerine, ACP denetim iz konuşma eylemlerine, ANP merkezi olmayan kimlik uzantılarına karşılık gelir. Yeni özellikler JSON sentaksisi ve gevşek semantik ile ACL'in soyuncusu.

> Liu 等人 2025 yılındaki genel tarihleri: "Agent 互操作性协议综述:MCP, ACP, A2A, ANP",arXiv:2505.02279) açıkça belirtti:MCP konuşma davranışına yönelik araç kullanımı, A2A konuşma davranışına yönelik ajan, ACP konuşma davranışına yönelik denetim tarzı, ANP konuşma merkezli kimlik genişlemesine yönelik yeni düzenlemeler, JSON 语法和更松散的语义──

### Açıkça belirtilen,

> **【中文解读】**权衡要明说:FIPA 给形式语义(可证明) 规范施事行为目录(不用重辩) 带正确性保证的交互协议模式;现代规范给 JSON 原生载荷、自然语言内容、Web 传输、能力发现──交换的就是"更松散的意图语义换更容易实现"──

**What FIPA gave you and modern specs drop:**

> **FIPA 给你的而现代规范丢弃的：**

- Formal semantik  kanıtlayabilirsiniz `inform`göndericinin içeriğe inandığını gösterir.
  Çeviri: formasi语义 sen kanıtlayabilirsin`inform`Gönderenin bu içeriğe inanması anlamına geliyor.
- Bir performatif kataloğu  tekrar tartışmak zorunda değilsiniz "eğer bir `cancel`"
  Çin Çeviri: "Bizim İçin Bir Tartışma Olmamalı"`cancel`"Hem?"
- On yıllardır etkileşim-protokola kalıpları  sözleşme-net, abone-bilgi, öner- Kabul  bilinen doğruluk özellikleri ile.
  Çinçe çevirisi: On yılın birliğindeki iletişim anlaşması modeli 合同网、订阅-通知、提议-接受具有已知的正确性属性──

**What modern specs give you and FIPA did not:**

> **现代规范给你的而 FIPA 没有的：**

- JSON-devde gelen payloadlar, her modern araçla uyumludur.
  Çinçe Çevirimiçi: Çinçe Çeviri
- LLM'lerin el kodlanmış ontoloji olmadan yorumlayabileceği doğal dil içerikleri.
  Çin Çeviri:LLM, doğal dil içeriğini el yapımı kodlama yapısı olmadan açıklayabilir.
- Web-stack taşımacılığı (HTTP, SSE, WebSocket).
  ÇXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
- Canlı MCP üzerinden yetenek keşfi `server/discover`A2A Ajan Kartları.
  Çeviri: MCP`server/discover`A2A Ajan Kartı  İhtiyaçlı Bulma

Daha kolay uygulanmak için gevşek niyet semantikası.

> Daha kolay gerçekleşmek için daha rahat bir şekilde gerçekleşmek için daha kolay gerçekleşmek için daha kolay gerçekleşmek için daha kolay gerçekleşmek için daha kolay gerçekleşmek için daha kolay gerçekleşmek için daha kolay gerçekleşmek için daha kolay gerçekleşmek için daha kolay gerçekleşmek için daha kolay gerçekleşmek için daha kolay gerçekleşmek için daha kolay gerçekleşmek için daha kolay gerçekleşmek için daha kolay gerçekleşmek için daha kolay gerçekleşmek için daha kolay gerçekleşmek için daha kolay gerçekleşmek için daha kolay gerçekleşmek için daha kolay gerçekleşmek için daha kolay gerçekleşmek için daha kolay gerçekleşmek için daha kolay gerçekleşmek için daha kolay gerçekleşmek için daha kolay gerçekleşmek için daha kolay gerçekleşmek için daha kolay gerçekleşmek için daha kolay gerçekleşmek için daha kolay gerçekleşmek için daha kolay.

### Portlamaya değer etkileşim protokolleri

> **【中文解读】**FIPA 约15 交互协议里,三个值搬入 LLM 多 Agent 系统:合同网,应应任务市场模式,应Fase 16·16 协商) 订阅/通知 ((每个事件总线) 请求-当(持久工作流引擎的延迟任务,应Fase 16·22) 它们都能干净映射到现代消息队列、HTTP + 轮询或SSE 流──

FIPA 15 etkileşim protokolü gönderdi.

> FIPA yaklaşık 15 iletişim anlaşması yayınladı. Bunlardan üçü LLM'nin çoklu ajan sisteminde uzatılmalıdır:

1. **Contract Net Protocol (CNP).**Yöneticilerle ilgili sorunlar `cfp`(yardım çağrısı); teklif verenler cevap verirken `propose`Bu, görev pazarının kanonik örneğidir (16 · 16 müzakere aşaması).
   Çeviri:**合同网协议 (CNP)。**管理者发布  yöneticisi`cfp`(征求提案);投标者用 `propose`响应;管理者接受/拒绝──这是典型任务市场模式(Phase 16 · 16 协商)
2. **Subscribe/Notify.**Abone gönderir `subscribe`; yayıncı gönderir `inform`Bu 2026'da her etkinlik otobüsü.
   Çeviri:**订阅/通知。**订阅者发送 `subscribe`; Publisher in tema değişimi saat gönderme `inform`2026 yılındaki her olayın bir parçası bu.
3. **Request-When.**"Y koşulları geçerli olduğunda X yapın". Ön koşullarla gecikmiş eylem. 2026 analog, dayanıklı çalışma akışı motorlarında gecikmiş görevlerdir (Fase 16 · 22 Üretim ölçeklemesi).
   Çeviri:**请求-当。**"Y 成立时执行 X──"带前置条件的延迟动作──2026 yılının benzerleri ise sürekli çalışma akım motorundaki geçici görevlerdir.

Her haritada modern mesaj kuyrukları, HTTP + anketleri veya SSE akışı bulunur.

> Her biri modern haber sıralarına açıkça görüntülenebilir, HTTP + 轮询 veya SSE 流.

### Ontolojiyi bırakırken ne kırılır?

> **【中文解读】**Bedenimi kaybetme bedeli**语义漂移**İki ajan aynı kelime için çok farklı kavramlar vardır, kabul eden yanlış anlaşılmamış bir hareketle, schema 验证器抓不住──FIPA'nın kendiliğinden talep ettiği gibi bu tür haberleri çözünce reddeder──缓解三件套:`content`Üstlerine JSON Şemaı, tip kimyasal parçalar, A2A'lar, açık bir şekilde yapılmış yapıların yapısı.

Ortak bir ontoloji olmadan, ajanlar doğal dil içeriklerinden anlam çıkarırlar.**semantic drift**: iki ajan aynı kelimeyi kullanır (`"customer"`) ince farklı kavramlar için, alıcının ajanı yanlış yorum üzerine hareket eder, hiçbir schema validator onu yakalamaz. FIPA'nın ontoloji talebi mesajı analiz zamanında reddetmiş olurdu.

> 没有共享本体,Agent 从自然语言内容中推断含义──记录在案的2026年失败模式是**语义漂移**İki ajan aynı kelime için:)`"customer"`) farklı kavramlar vardır, alıcı Ajan yanlış anlama eylemlerine dayanır, hiçbir model denetleyicisi onu yakalayamaz.

Tam ontoloji olmadan azaltmalar:

> İçtenlikle tamamen kullanılmayan hafifleme önlemleri:

- JSON Şeması `content` teldeki yapısal hataları reddeder.
  Çeviri:`content`JSON Şema kullanmak  传输层拒绝结构性错误
- Tipli eserler (A2A)  yanlış modaliteyi reddeder.
  Çinçe Çevirimi:类型化工件 A2A) 拒绝错误的模态。
- Kapakta açık performatif , içerik doğal dil olduğunda bile niyetini belirgin hale getirir.
  Çine dilinde de belirgin bir işlev yapılır.

### 2026 özellikleri, konuşma-işlev mirası ile haritası

| Modern spec | FIPA analog | What it keeps | What it drops |
|---|---|---|---|
| MCP `tools/call` | `request` | explicit intent, correlation id | formal semantics, ontology |
| MCP `resources/read` | `query-ref` | explicit intent, correlation id | formal semantics |
| A2A Task lifecycle | contract-net + request-when | async lifecycle, state transitions | formal completeness guarantees |
| A2A streaming events | subscribe/notify | async push | typed-predicate subscription |
| CA-MCP shared context | blackboard (Hayes-Roth 1985) | multi-writer shared memory | logical consistency model |
| NLIP | natural-language content | LLM-native | schema |

Tabloyu yukarıdan aşağıya okuyarak, örneği şöyle: yapısal ilkelliği koruyun, formallığı bırakın, LLM'lerin belirsizliği ele almasına izin verin.

> Şekil: Yapısal dil, biçimselliği bırak, LLM'yi düzeltmek için.

> **【中文解读】**Bir cümlede toplam tüm tablo:2026 规范保留的是结构性原语(显式意图、关联 id、异步生命周期),丢弃的是形式主义(形式语义、本体、逻辑一致性), LLM'nin açıklama yeteneği ile doldurmaktadır歧义──

```figure
sw-contract-net
```

## Yapın.

> **【中文解读】**Örneğin kod, bir FIPA-ACL 翻訳器:把五条 MCP/A2A 风格消息编码为 FIPA-ACL 再解码回来,并跑一个"一个管理者 + 三个投标者"的玩具合同网协商──输出并排展示同一消息的2026 JSON 形态和FIPA-ACL 形态与一些协议原语在往返中存活,只有语法不同──

`code/main.py`MCP / A2A mesaj şeklinin aynı yedi alanı nasıl azaltdığını gösterir.

> `code/main.py`实现一个纯标准库的FIPA-ACL 翻译器──它编解标准 ACL 信封,并展示每个 MCP / A2A 消息形状如何简化为相同的七段──演示内容:

- Beş MCP ve A2A biçimindeki mesajı FIPA-ACL olarak kodlar.
  Çinçe Çevirisi:将五个 MCP 风格和 A2A 风格的消息编码为 FIPA-ACL。
- FIPA-ACL'yi modern eşdeğeri olarak dekode eder.
  Çinçe Çevirisi:将 FIPA-ACL 解码回现代等效形式──
- Oyuncak çalıştırma Sözleşmesi Bir yöneticiden üç teklifci arasında net pazarlama`cfp`- Evet .`propose`- Evet .`accept-proposal`- Evet .`reject-proposal`- Evet .
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`cfp`- Evet.`propose`- Evet.`accept-proposal`- Evet.`reject-proposal`Bir yöneticiler ve üç teklif verenler arasında bir oyuncak anlaşması yürütülmektedir.

Çık:

```
python3 code/main.py
```

Çıktı, her modern mesajı hem 2026 JSON formunda hem de FIPA-ACL formunda, ardından bir sözleşme ağ teklifinin bir geri dönüş yolu gösterir. Aynı protokol ilkesi geri dönüş yolu hayatta kalır; sadece sentezi farklıdır.

> 输出是一个并排追踪,显示每条现代消息的 2026 JSON 形式和FIPA-ACL 形式,然后是合同网投标标标的往返──同协议原语在往返中存活;只有语法不同──

## Çerçeveyi kullanın.

`outputs/skill-fipa-mapper.md`Bu, bir ajan-protokolu özelliklerini okuyan ve FIPA-ACL haritasını üreten bir beceri.`inform`JSON sözcükleri ile mi?"

> `outputs/skill-fipa-mapper.md`Bu yeni protokolü kullanmadan önce kullanmak için cevap vermek için: "Bu gerçekten yeni bir şey, ya da JSON 语法 ile.`inform`"Bunu nasıl yapabilirim?"

## İndirin . Ürünler .

> **【中文解读】**Bu beş soruya önce cevap vererek, bir sonraki aşamada bir daha bir daha daha daha daha daha daha daha daha daha fazla bilgi verelim.

FIPA-ACL'i geri getirmeyin.

> FIPA-ACL'i geri getirmeyin.

- Her mesajın ilk amacı nedir?
  Çinçe Çevirimi: her haberin anlamı nedir?
- İstek- yanıt ve iptal için bir ilişki kimliği var mı?
  Çinçe Çevirimi: istek-response ve kaldırma için kullanılacak bağlantı kimliği var mı?
- Açık bir içerik dili var mı (JSON-RPC, düz metin, yapılandırılmış yazılı eser)?
  Çinçe Çevirimi Çevirisi: JSON-RPC 純文本 構造化类型工件)
- Etkinlik protokolleri birinci sınıf mı yoksa yeni bir sözleşme sistemi mi var?
  Çinçe Çevirisi:交互协议 is equal citizen, or are you starting to re-implement contract net?
- İki ajan içeriğin anlamı hakkında anlaşmazlıklarda (semantik sürükleme) ne olur?
  Çinçe Çevirim: İçerik anlamı hakkında ayrılığa düşen iki ajan olduğunda ne olur?

Bu beş soruyu, yeni bir protokol için üretime göndermeden önce belgeleyin.

> Yeni bir anlaşma yapmadan önce, bu beş sorunu kaydet.

## Egzersizler.

1. Çık .`code/main.py`.Geri-geri kodlama gözlemleyin. FIPA performatifinin hangi ile karşılık geldiğini belirleyin `tools/call`- Evet .`resources/read`, ve A2A görev oluşturma.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`code/main.py` gözlemleme                                                                                                                                                                                                                                                                                                                                                        `tools/call`- Evet.`resources/read`A2A 任务创建――
2. Sözleşme ağı gösterisini bir  ile uzatın`cancel`Bu, yöneticinin görevleri orta teklif sırasında geri çekmesine izin veren performatif.`cancel`Tekrar denemeyi çözmek için değil mi?
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`cancel`Şirketin başvuruda bulunan yöneticilerin görevlerini geri alabilmesi için yapılan açıklamalar.`cancel`Tekrar deneme ile çözülemez olan bir sorun mu?
3. FIPA ACL Mesaj Yapısı (http://www.fipa.org/specs/fipa00037/Bu dersde ele alınmayan bir performatif seçin ve modern JSON-RPC analogunu açıklayın.
   Çeviri: FIPA ACL 消息结构http://www.fipa.org/specs/fipa00037/）第4.1-4.3 节──选择本课未涵盖的一个施事行为并描述其现代 JSON-RPC 类比──
4. Liu et al., arXiv:2505.02279. MCP, A2A, ACP, ANP'lerin her biri için, FIPA'nın sürdürdüğü ve bıraktıkları performatif ailelerini listelenin.
   Çinli İngilizce çevirisi:阅读 ?? 等人,arXiv:2505.02279── MCP、A2A、ACP、ANP içindeki her biri için, onları korumak ve terk etmek için FIPA 施事行为族を列挙します。
5.  için en az bir JSON-Skeması tasarlayın`content`bir alanı `request`Bu şema size doğal dilin yapmadığı neyi verir ve maliyeti ne kadar?
   Çin Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Ç Çeviri Çeviri Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç`request`施事行为  İşler`content`字段设计一个最小的JSON-Schema――这个模式给你提供纯自然语言没有什么,价格是什么?

## Anahtar Şartlar .

| Term | What people say | What it actually means | 中文术语 |
|------|----------------|------------------------|----------|
| Speech act | "An utterance that does something" | Austin/Searle: utterances as actions. The theoretical parent of ACL. | 言语行为 |
| FIPA | "That old XML thing" | IEEE Foundation for Intelligent Physical Agents. Standardized ACL in 2000. | FIPA 基金会 |
| ACL | "Agent Communication Language" | FIPA's envelope format: performative + content + metadata. | Agent 通信语言 |
| Performative | "The verb" | The intent class of a message: `inform`, `request`, `propose`, `cfp`, etc. | 施事行为 |
| KQML | "FIPA's predecessor" | Knowledge Query and Manipulation Language (1993). Simpler, narrower. | KQML |
| Ontology | "Shared vocabulary" | A formal definition of the concepts the content language talks about. | 本体 |
| SL0 / SL1 | "FIPA content languages" | Semantic Language levels 0 and 1 — the formal content language family. | SL 内容语言 |
| Contract Net | "Task market" | Manager issues cfp; bidders propose; manager accepts. The canonical interaction protocol. | 合同网 |
| Interaction protocol | "Pattern of messages" | A sequence of performatives with known correctness: request-when, subscribe-notify, etc. | 交互协议 |

## Daha fazla okumak

- [Liu et al. — A Survey of Agent Interoperability Protocols: MCP, ACP, A2A, ANP](https://arxiv.org/html/2505.02279v1) Modern özellikleri FIPA mirası ile bağlayan 2025 Kanonik Anket
  中文翻译:Liu 等人Agent 互操作性协议综述,连接现代规范与FIPA 遗产的权威 2025 综述
- [FIPA ACL Message Structure Specification (fipa00037)](http://www.fipa.org/specs/fipa00037/) Ratifik edilmiş 2000 zarfı biçimi
  Çin dilinde:FIPA ACL 消息结构规范2000年批准的信封格式
- [FIPA Communicative Act Library Specification (fipa00037)](http://www.fipa.org/specs/fipa00037/) Tam performans kataloğu
  Çinçe Çevirimi:FIPA 通信行为库规范完整的施事行为目录
- [MCP specification 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28) mevcut devletsiz araç kullanımı eşdeğeri `request`- Ne ?`query-ref`
  Çeviri:MCP 2026-07-28 规范`request`- Ne ?`query-ref`                                                                                                                                                                                                                                                              
- [A2A specification](https://a2a-protocol.org/latest/specification/) Modern ajan-e eşdeğerlik sözleşme-net ve abone-bilgi
  Çinçe Çevirimi:A2A 规范合同网和订阅-通知的现代代理对等效
