# Neden Multi-Agent?

> Bir ajan duvara çarptı, akıllı hareket daha büyük bir ajan değil, daha fazla ajan.

> **【中文解读】**Bu bölüm, neden çoklu ajanın ihtiyaç duyduğunu, rol karışıklığı ve bir dizi sorununu ve çoklu ajanın bu sorunları nasıl çözmek için bölük iş birliği yoluyla çözdüğünü anlatıyor.

> **【拓展：why multi agent→具体应用】**单代理在处理复杂任务时面临三个瓶:(1) 上下文溢出所有信息塞进一个窗口,重要被淹没;(2) 角色混乱 一个代理 扮演多角色导致提示词冲突;(3) 串行执行工具调用只能排队――多代理 通过分工协作解决这些问题――Antropic研究表明,多代理系统在BrowseComp 基准上多代理系统 升 90.2%,80% 方仅由代币使用解释量而差──

>  **【前置】**Öğrenci bölümüne başlayın:Dava 14(Agent Mühendisliği) tamamı, özellikle Fase 14·01(Agent Loop) ve Fase 14·28(Orkestrasyon Şablonları)。本节 cevap "çı时候多 Agent kullanmak"简单回答:单 Agent + 工具不够时。Antropik 经验法则:任务需要 > 50 工具调用、或 > 1 个角色(如研究员 + 写手)、或并行能省时间,才考虑多 Agent。

>  **【类比】**单 Agent vs 多 Agent = 全能管家 vs 专业团队──全能管家──单 Agent) 能干所有事但每件事都不精:上午做饭、下午修车、晚上辅导作业,每样都半吊子──专业团队──多 Agent:厨师专做饭、机修工专修车、家教专辅导,每个人精一行──代价:协调成本(Agent 间通信) 和复杂性增加简单任务单 Agent 更划算──

**Type:** Learn | **类型:** 学习
**Languages:** TypeScript | **语言:** TypeScript
**Prerequisites:** Phase 14 (Agent Engineering) | **前置知识:** Phase 14 (Agent 工程)
**Time:** ~60 minutes | **时间:** ~60 分钟

## Öğrenme hedefleri

- Tek ajanlı tavanı belirleyin (koneks aşırılığı, karışık uzmanlık, sıralı şişek boynuz) ve birden fazla ajanlılığa bölünmenin doğru hareket olduğunu açıklayın
  Çinçe Çevirimi: Identification Single Agent 上限(上下文溢出、专业能力混合、串行瓶),并解释何时分分多代理 是正确的选择
- Orkestralama desenlerini karşılaştırın (pipeline, paralel fan-out, yönetici, hiyerarşik) ve verilen görev yapısı için doğru olanı seçin
  Çinçe çevirisi: ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎
- Açık rol sınırları, paylaşılan durum ve iletişim sözleşmesi ile çoklu ajanlı bir sistem tasarlayın
  Çinçe Çevirisi: Çevre sınırları, ortak durum ve iletişim anlaşması belirgin bir rolü olan bir çok ajanı oluşturma  sistem
- Çoklu ajan karmaşıklığının (kenaklık, maliyet, hata işleminde zorluk) karşılaştırmalarını tek ajan basitliği ile analiz edin
  Çinçe çevirisi: analiz çok Ajan 复杂性(延迟、成本、调试难度) ve tek Ajan 简单性 arasındaki tartışma

## Sorunlar. Sorunlar.

14. aşamada tek bir ajan oluşturdun. İşliyor. Dosyaları okuyabilir, komutları çalıştırır, API'leri arayabilir ve sonuçları düşünüyor. Sonra gerçek bir kod tabanına yönlendiriyorsun: 200 dosya, üç dil, altyapıya bağlı testler ve kod yazmadan önce dış API'leri araştırmak için bir gereksinim.

> 14. aşamada tek bir ajan oluşturursunuz. İyi çalışır, dosyaları okuyabilir, işlemi düzenleyebilir, API'yi kullanır ve sonuçları düşünerek yönlendirebilirsiniz. Sonra onu gerçek bir kod kütlesine yönlendireceksiniz: 200 dosya, üç dil, altyapıya bağlılık testi ve öncelikle dış API'yi yeniden yazma talepleri üzerinde çalışmanız gerekir.

Demo ajanları ve üretim ajanları arasındaki boşluk "bir dosya, bir dil, bir araç" ve "çok dosya, birçok dil, bağımlılıkları olan birçok araç" arasındaki boşluktur.

> 演示 Ajan ve üretim Ajan arasındaki fark "bir dosya, bir dil, bir araç" ve "birçok dosya, bir çok dil, bir çok bağımlı araç" arasındaki farkdır.

Bu yüzden, bu iş, bir ajanın yapabileceği işten fazlasını yapar. Bu iş, bir ajanın yapabileceği işten fazlasını yapar. Bu iş, bir ajanın yapabileceği işten fazlasını yapar. Bu iş, bir ajanın yapabileceği işten fazlasını yapar. Bu iş, bir ajanın yapabileceği işten fazlasını yapar. Bu iş, bir ajanın yapabileceği işten fazlasını yapar. Bu iş, bir ajanın yapabildiği işten sonra, bir ajanın yapabildiği işten sonra, bu işten sonra, bu işten sonra, bu işten sonra, bu işten sonra, bu işten sonra, bu işten sonra, bu işten sonra, bu işten sonra, bu işten sonra, bu işten sonra, bu işten sonra, bu işten sonra, bu işten sonra, bu işten sonra, bu işten sonra, bu işten sonra, bu işten sonra, bu işten sonra, bu işten sonra, bu işten sonra, bu işten sonra, bu işten sonra, bu işten sonra, bu işten sonra, bu işten sonra, bu işten sonra, bu işten sonra, bu işten sonra, bu işten sonra, bu işten sonra, bu işten sonra, bu işten sonra, bu işten sonra, bu işten sonra, bu işten sonra, bu işten sonra, bu işten sonra, bu işten sonra, bu işten sonra, bu işten sonra, bu işten sonra, bu, bu işten sonra, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bir işten, bu, bu, bu, bir işten, bu, bu, bir işten, bu, bu, bu, bir işten, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bir şey, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, için, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, için, bu, bu, bu, bu, bu, bu, bu, bu, için, bu, bu, bu, bu, bu, bu, bu, bu, bu, bu, için, bu, bu, bu, bu, bu, bu, bu

> Ajan 崩了── LLM 愚蠢的原因ではなく, görevleri tek Ajan 循环能处理の範囲を超えているため──上下文窓はファイル内容が満載──Ajan 忘了40回工具调用前読みの内容──Ajan 忘了40回工具调用前読みの内容──Ajan 忘了 40回工具调用前読みの内容──Ajan 忘了 40回工具调用前読みの内容──Ajan 忘了 40回工具调用前読みの内容──Ajan 忘了 40回工具调用前読みの内容──Ajan 忘了 40回 忘了 40 回 忘了 忘了 忘了 忘了 忘了 忘了 忘了 忘了 忘了 忘了 忘了 忘了 忘了 忘了 忘了 忘了 忘了 忘了 忘了 忘了 忘了 忘了 忘了 忘了 忘了 忘了 忘了 忘了 忘了 忘了 忘了 忘了 忘了 忘了 忘了 忘了 忘了 忘了 忘了 忘了 忘了 忘了 忘了 忘了 忘了 忘了 忘了 忘了 忘了 忘了 忘了 忘了 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 忘 

Bu tek ajanlı tavan. Bir görev için her zaman vurulur.

> Bu tek bir ajanın sınırları. Her görevde aşağıdaki şartlar vardır.

Sınır yapısal, algoritmik değil. Daha iyi bir LLM tavanı geciktirir ama çıkarmaz. 1M-token bağlam penceresi 200k bir  kadar kesinlikle doldurulur. Sadece daha fazla dosya alır.

> Yukarı sınır yapısal, algoritmik değil. Daha iyi LLM 延迟上限但不移除它──1M token 上下文窗口像200k 一样确定地填满只是需要更多文件──

- **More context than fits in one window**- 50 dosya okuyarak 200 bin tokeni geçiyor
  Çeviri:**超出一个窗口容量的上下文**50 dosya , 200 bin tokenden fazla olacak .
- **Different expertise at different stages**- araştırma kod üretiminden farklı bir teşvik gerektirir
  Çeviri:**不同阶段需要不同的专业知识** Araştırma kod üretmek ile farklı öneriler oluşturmak gerekir
- **Work that can happen in parallel**- ...sadece aynı anda okuyabilirseniz neden üç dosyayı sıradan okuyun?
  Çeviri:**可以并行执行的工作**  Üç dosyayı aynı anda okuyabilirsek neden sırayla okuyabilirsek?

## Konsepten bir şey.

### Tek Ajanlı Tavan

Tek bir ajan bir döngü, bir bağlam penceresi, bir sistem uyarısı.

> Tek Ajan bir döngüdür, bir aşağıdaki pencerede bir sistem ipucu.

```
┌─────────────────────────────────────────┐
│            SINGLE AGENT                 │
│                                         │
│  ┌───────────────────────────────────┐  │
│  │         Context Window            │  │
│  │                                   │  │
│  │  research notes                   │  │
│  │  + code files                     │  │
│  │  + test output                    │  │
│  │  + review feedback                │  │
│  │  + API docs                       │  │
│  │  + ...                            │  │
│  │                                   │  │
│  │  ██████████████████████ FULL ███  │  │
│  └───────────────────────────────────┘  │
│                                         │
│  One system prompt tries to cover       │
│  research + coding + review + testing   │
│                                         │
│  Result: mediocre at everything         │
└─────────────────────────────────────────┘
```

Tek sistem uyarısı temel nedendir. Araştırma, kodlama, inceleme ve test için talimatlar vermek zorunda. Her talimat diğerlerini hafifletir.

> 单系统提示是根本原因――它必须同时为研究,编码,审核和测试提供指令――每条指令稀释其他――Agent 最终在所有事上"还行",在任何事上都不优秀――

Üç şey kırılır:

> Üç sorun çöküşe yol açacaktır:

1. **Context saturation**30. turda ajan 150 bin token dosya içeriği, komut çıkışı ve önceki akıl yürütme tüketti.
   Çeviri:**上下文饱和** 工具結果不断堆积──30'cu turuna kadar,Agent 已消耗了150k token 文件内容、命令输出和前推理──5th轮的关键细节丢失──

2. **Role confusion**- "Sen bir araştırmacı, kodlayıcı, inceleyicisin ve testçi" diyen bir sistem uyarısı yarı araştırma yapan, yarı kodlayan ve incelemeyi asla bitirmeyen bir ajan üretir.
   Çeviri:**角色混乱** "Sen araştırmacı, programcı, denetçi ve denetçi" yazısı sistem önerisi yarı inceleme, yarı kodlama, sonsuza dek tamamlanmamış inceleme ajanı oluşturur.

3. **Sequential bottleneck**- ajan A dosyasını okuyor, sonra B dosyasını, sonra C dosyasını.
   Çeviri:**串行瓶颈** Agent 读取文件 A,然后文件 B,然后文件 C──三次串行 LLM 调用──三次串行工具执行──没有并行性──

Tek ajan, her adımda uzman olmak istenen bir genelisttir.

> Tek Ajanın her adımda uzman olma isteği vardır. Bir çok Ajanın ayrılması, her Ajanın bir konuda uzman olma isteği vardır.

### Çok Ajanlı Çözüm

Her ajanın bir görevi, bir bağlam penceresi ve bu göreve uygun bir sistem uyarısı yapın:

> 拆分工作──给每一个代理一个任务、一个上下文窗口和一个系统提示:

Bu, LLM ajanlarına uygulanan "sorun ayrımı"dır. Her ajanın istekleri daha kısa ve daha odaklıdır. Her ajanın bağlam penceresi sadece ihtiyaç duyduğu şeyi tutar. Her ajan bağımsız olarak test edilebilir ve geliştirilebilir. Orkestratör kompozisyonu ele alıyor.

> Bu, LLM Ajanının "kesinlik noktaları ayırılması" için uygulanmaktadır. Her Ajanın ipucu daha kısa ve daha odaklanmıştır.

```
┌──────────────────────────────────────────────────────────┐
│                    ORCHESTRATOR                          │
│                                                          │
│  "Build a REST API for user management"                  │
│                                                          │
│         ┌──────────┬──────────┬──────────┐               │
│         │          │          │          │               │
│         ▼          ▼          ▼          ▼               │
│   ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │
│   │RESEARCHER│ │  CODER   │ │ REVIEWER │ │  TESTER  │  │
│   │          │ │          │ │          │ │          │  │
│   │ Reads    │ │ Writes   │ │ Checks   │ │ Runs     │  │
│   │ docs,    │ │ code     │ │ code     │ │ tests,   │  │
│   │ finds    │ │ based on │ │ quality, │ │ reports  │  │
│   │ patterns │ │ research │ │ finds    │ │ results  │  │
│   │          │ │ + spec   │ │ bugs     │ │          │  │
│   └─────┬────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘  │
│         │           │            │             │         │
│         └───────────┴────────────┴─────────────┘         │
│                          │                               │
│                     Merge results                        │
└──────────────────────────────────────────────────────────┘
```

Her ajanın:
- odaklanmış bir sistem sorgulaması ("Kodu inceleyicisiniz. Tek işiniz hata bulmak. ")
  Çinçe Çevirimiçi: bir odaklı sistem gösterişi ((("You are a code reader。Your only task is to find bug。")
- Kendi bağlam penceresi (diğer ajanların çalışmaları tarafından kirlenmemiş)
  Çeviri: kendi üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst üst
- Açık bir giriş/çıktı sözleşmesi ( Araştırma notları alır, çıkış kodu alır)
  Çinçe Çevirim:清晰的输入/输出契约(接收研究笔记,输出代码)

Orkestratör ajanı sadece yüksek düzeyde görevi ve nasıl devredileceğini anlamalıdır. Her alt görevi nasıl yapacağını bilmesi gerekmez. Her uzman ajanın sadece kendi dar işini bilmesi gerekir.

> 编排 代理 应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应对应

### Bunu Yapacak Gerçek Sistemler

**Claude Code subagents**- Claude Code bir subagen doğururken .`Task`Bu, bir çocuk ajanı oluşturur ve bir görev belirlenir. Ebeveyn bağlamını temiz tutar. Çocuk odaklı bir iş yapar ve bir özet gönderir.

> **Claude Code 子 Agent** 当 Claude Code 使用 `Task`Doğumcu Ajan 时, sınırlı bir boyutlu bir çocuk Ajanı oluşturur.

Bu model viral çünkü oluşturur: bir alt-altı öz özürlü alt-altı üretebilir. Karmaşık kod tabanlı görevlerde üç seviye derinlik yaygın; bunun ötesinde, hata işlemleri ağrılı hale gelir.

> Bu tür bir yöntem viral olarak yayılır çünkü birleştirilebilir: Çocuk Ajan kendi Çocuk Ajanını oluşturabilir.

**Devin**- planlayıcı ajanı, kodlayıcı ajanı ve tarayıcı ajanı çalıştırır. Planlayıcı işi adımlara ayırır. kodlayıcı kod yazar. tarayıcı belgeleri araştırır. Her birinin ayrı bağlamı vardır.

> **Devin** 运行一个规划代理一个编码代理 和一个浏览器代理――规划器将工作分解成步骤――编码器编写代码――浏览器研究文档――每个都有独立的上下文――

Devin'in mimarisi derslik denetleyicisi örneğidir: küresel plana sahip olan bir planlamacı, parçaları gerçekleştiren birden fazla uzman işçi. Tarayıcı ajanı ilginçtir  bu kendisinde tarayıcı araçları olan bir alt-agent, kodlayıcı bağlamından izole edilmiştir.

> Devin'in yapı, bir kursu gibi bir denetçi modeli: bir bütünsel planı olan planlayıcısı, bir çok parça gerçekleştiren uzman işçi; bir tarayıcı ajanı.

**Multi-agent coding teams (SWE-bench)**- SWE-benç'teki en iyi performanslı sistemler, kod tabanını okuyan bir araştırmacı, düzeltmeyi tasarlayan bir planlayıcı ve uygulayan bir kodleyiciden yararlanır.

> **多 Agent 编码团队 (SWE-bench)** SWE-benç'te en iyi performans gösteren sistem bir kod kütüphanesi araştırmacısı, bir tasarım düzeltme programı planlayıcısı ve bir düzeltme gerçekleştiren kodlayıcı kullanıyor.

2026 SWE-benç liderlik tablosu, çoklu ajan sistemleri tarafından baskınlaştırılmıştır. Şablon: kod tabanı anlayışı için büyük bir bağlamı olan bir araştırmacı, düzeltme tasarımı için odaklı bir istekle planlayan bir planlayıcı, uygulamak için sıkı yazılama gereksinimleri olan bir kodlayıcı. Her rol ihtiyaç duyduğu istekle sonuçlanır.

> 2026 SWE-bench  sıralama  çoklu ajan  sistem yönetiyor 模式:带大上下文的研究员用于代码库理解、带焦点提示的规划器用于修复设计、带严格类型要求的编码器用于实现──每个角色获得它需要的提示──

**ChatGPT Deep Research**- her biri farklı açılardan araştırma yapan, paralel olarak birden fazla arama ajanı üretir, sonra sonuçları sentezler.

> **ChatGPT Deep Research** ve birden fazla arama ajanı üretmek için, her bir farklı açıdan araştırmak, sonra sonuçları birleştirmek için.

### Spektrum

Çoklu ajan ikili değil, bir spektrum:

> Do Agent Not in Two.

Spektrum çerçevesinin önemli olduğu için çoğu üretim sistemi hiçbir aşırılıkta değildir. Claude Code, alt alt (bir seviye derinlik) kullanır. Devin küçük bir ekibi kullanır. Gerçek araştırma sistemleri 5-50 ajan kullanır. Spektrdeki doğru nokta görev karmaşıklığına bağlıdır.

> 光谱 çerçeve önemlidir, çünkü çoğu üretim sistemi bir uçta değildir.

```
SIMPLE ──────────────────────────────────────────── COMPLEX

 Single        Sub-         Pipeline      Team         Swarm
 Agent         agents

 ┌───┐       ┌───┐        ┌───┐───┐    ┌───┐───┐    ┌─┐┌─┐┌─┐
 │ A │       │ A │        │ A │ B │    │ A │ B │    │ ││ ││ │
 └───┘       └─┬─┘        └───┘─┬─┘    └─┬─┘─┬─┘    └┬┘└┬┘└┬┘
               │                │        │   │       ┌┴──┴──┴┐
             ┌─┴─┐          ┌───┘───┐    │   │       │shared │
             │ a │          │ C │ D │  ┌─┴───┴─┐    │ state │
             └───┘          └───┘───┘  │  msg   │    └───────┘
                                       │  bus   │
 1 loop      Parent +      Stage by    │       │    N peers,
 1 context   child tasks   stage       └───────┘    emergent
                                       Explicit      behavior
                                       roles
```

**Single agent**- Bir döngü, bir uyarı.

> **单 Agent** Bir döngü, bir ipucu, basit bir göreve uygun.

**Subagents**- bir ebeveyn çocuklarını odaklı alt görevler için doğurur. ebeveyn planı korur. çocuklar rapor verir. Claude Code böyle yapar.

> **子 Agent** Baba Ajanı 聚焦的子任务生成子 Ajanı 父 Ajanı 维护计划 子 Ajan 汇报结果  İşte Claude Code'un uygulaması budur

**Pipeline**- ajanlar sırayla çalışırlar. A ajanın çıkışı A ajanın girişine dönüşür.

> **流水线** Ajan 顺序运行──Ajan A'nın输出成为 B A'nın输入──适合分阶段的工作流:研究 -> 编码 -> 审阅 -> 测试──

**Team**- ajanlar ortak mesaj otobüsü ile paralel olarak çalışırlar. her birinin bir rolü vardır. bir orkeströr koordinatör.

> **团队** Agent 通過共享消息总线并行运行──各有角色──编排器协调──适应需要同时使用不同技能的场景──

**Swarm**- ortak durumlu çok sayıda aynı veya neredeyse aynı ajan. sabit orkeströr yok. ajanlar sıradan iş alırlar. yüksek performanslı paralel görevler için iyi.

> **群体**                                                                                                                                                                                                                                                              

### Dört Çok Ajanlı Örnek

#### Şekil 1: Pipeline

```
Input ──▶ Agent A ──▶ Agent B ──▶ Agent C ──▶ Output
          (research)  (code)      (review)
```

Her ajan verileri dönüştürür ve öne aktarır.

> Her ajan veriyi aktarır ve sonraki bir ajanı gönderir.

Her aşamada net bir giriş/çıktı varken kullanın ve aşamalar doğal olarak sırayildir. Araştırma → kod → inceleme → test kanonik örnektir.

> kullanma durumu: her aşamada net bir giriş/çıxış ve aşamada doğal bir sırayla yürütülmektedir.

#### Şekil 2: Fan Out / Fan In

```
                ┌──▶ Agent A ──┐
                │              │
Input ──▶ Split ├──▶ Agent B ──├──▶ Merge ──▶ Output
                │              │
                └──▶ Agent C ──┘
```

Paralel ajanlar arasında çalışmayı bölün, sonra sonuçları birleştir.

> İşleri paralel çalışan Ajanlara dağıtacak ve sonuçları birlikte birlikte birlikte dağıtacak.

İşler birbirinden bağımsız parçalara ayrıldığında kullanın (örneğin 5 farklı kaynağı arayın, 10 belgeyi özetleyin).

> Uygulamayı kullanın: görevler açıkça ayrılabilir bağımsız bölümlere ayrılır.

#### Model 3: Orkestratör-işçi

```
                    ┌──────────┐
                    │  Orch.   │
                    └──┬───┬───┘
                  task │   │ task
                 ┌─────┘   └─────┐
                 ▼               ▼
           ┌──────────┐   ┌──────────┐
           │ Worker A │   │ Worker B │
           └──────────┘   └──────────┘
```

Akıllı orkeströr ne yapacağını belirler, işçilere görevlendirir ve sonuçları sentezler.

> Zeki düzenleyici ne yapmayı karar verir, görevlendirmek için çalıştırır,并综合结果── düzenleyici kendisi bir çalıştırma aracı üreten bir ajanıdır──

İşleme ne zaman kullanılır: görev o kadar karmaşık ki ne yapılması gerektiğine karar vermek kendi başına zor bir problemdir.

> İşleme alanı: Görev yeterince karmaşık, ne yapılması gerektiği konusunda karar vermek zor bir sorun.

#### Dörtüncü örnek: Arkadaşlar

```
         ┌───┐ ◄──── msg ────▶ ┌───┐
         │ A │                  │ B │
         └─┬─┘                  └─┬─┘
           │                      │
      msg  │    ┌───────────┐     │ msg
           └───▶│  Shared   │◄────┘
                │  State    │
           ┌───▶│  / Queue  │◄────┐
           │    └───────────┘     │
      msg  │                      │ msg
         ┌─┴─┐                  ┌─┴─┐
         │ C │ ◄──── msg ────▶ │ D │
         └───┘                  └───┘
```

Merkez orkeströrü yok, ajanlar birbiriyle iletişim kurar, kararlar etkileşimden kaynaklanır, hataları düzeltmek daha zor ama birçok ajan için ölçeklendirilir.

> 没有中央编排器──Agent 之间点对点通信──决策从交互中涌现──更难调试,但可以扩展到许多Agent──

Bir çok eşdeğer ajanın aynı işi (kaçırma, sınıflandırma) ölçekte yaptığında kullanın.

> Use scene: Numaralardaki benzerler Büyük çapta benzer işler yaparlar.

### Çoklu Ajanlar Ne Zaman Kullanılmamalı

Multi-agent karmaşıklığı artırır. ajanlar arasındaki her mesaj potansiyel bir başarısızlık noktasıdır. Debug "bir konuşmayı oku"dan "beş ajan arasındaki mesajları izlemek"e kadar gider.

> Birçok ajan  karmaşıklık artmıştır. Ajanlar arasındaki her haber potansiyel bir sorun noktasıdır.

**Stay single-agent when:**
- Görev bir bağlam penceresine (iş verisi tokenlerinin ~ 100k altında) uymaktadır.
  Çinçe Çevirimi: görev uygundur bir üst aşağı penceresi (şirket verileri yaklaşık 100k tokenden fazla değil)
- Farklı aşamalarda farklı sistem isteklerine ihtiyacınız yok .
  Çin Çeviri: farklı aşamalar farklı sistem önerilerine ihtiyaç duymaz
- İletişim yeteri kadar hızlı .
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri
- Görev yeterince basit ki bölmek değerden daha fazla genel maliyet ekler.
  Çin Çeviri: Görev yeterince basit, ayrılma, giderlerin artırılması, değerinden fazla olması

**The complexity cost:**
- Her ajan sınırı bir kayblı sıkıştırma adımıdır: A ajanının tüm bağlamı A ajan için bir mesaj olarak özetlenir
  Çin Çeviri: Her Ajanın Sınırı Dolu Durum: Ajanın B Ajanın Haberleri
- Koordinasyon mantığı (kim ne yapar, ne zaman, hangi sırada) kendi hata kaynağıdır
  Çeviri: koordinasyon logika (kim ne yapıyor, ne zaman ne yapıyor, neyi yaparak) kendiliğinden bir hata kaynağıdır.
- Gecikme artışları: N ajanlar N seri LLM çağrıları minimum anlamına gelir, ileri geri konuşmaları gerekiyorsa daha fazla
  Çinçe Çevirimi:延迟增加:N 个代理 调用, if need to come back dialog则更多
- Maliyet katılaştırıcıları: her ajan jetonları bağımsız olarak yakar
  Çinçe Çevirim: Cost倍增:每个 Agent 独立消耗代币

Basamak kural: Bir görev 20'den az araç çağrısı alır ve 100k tokene uyarsa, tek ajanlı tutun.

> 経験法: Eğer bir görev sadece 20 kez araç kullanılması gerekiyorsa ve 100k token için uygun ise, tek bir ajan tutun.

## Yapın.
```figure
swarm-messages
```

## Yapın

### Adım 1: Aşırı yüklü tek bir ajan

Burada her şeyi yapmaya çalışan tek bir ajan var. Bu büyük bir sistem sorgulaması ve bir bağlam penceresi araştırma, kod ve incelemeleri tutan:

> Bu, her şeyi yapmaya çalışan tek bir ajan. Büyük bir sistemli bir ipucu ve bir çalışma, kod ve inceleme kapsamı olan aşağıdaki penceresi var:

```typescript
type AgentResult = {
  content: string;
  tokensUsed: number;
  toolCalls: number;
};

async function singleAgentApproach(task: string): Promise<AgentResult> {
  const systemPrompt = `You are a full-stack developer. You must:
1. Research the requirements
2. Write the code
3. Review the code for bugs
4. Write tests
Do ALL of these in a single conversation.`;

  const contextWindow: string[] = [];
  let totalTokens = 0;
  let totalToolCalls = 0;

  const research = await fakeLLMCall(systemPrompt, `Research: ${task}`);
  contextWindow.push(research.output);
  totalTokens += research.tokens;
  totalToolCalls += research.calls;

  const code = await fakeLLMCall(
    systemPrompt,
    `Given this research:\n${contextWindow.join("\n")}\n\nNow write code for: ${task}`
  );
  contextWindow.push(code.output);
  totalTokens += code.tokens;
  totalToolCalls += code.calls;

  const review = await fakeLLMCall(
    systemPrompt,
    `Given all previous context:\n${contextWindow.join("\n")}\n\nReview the code.`
  );
  contextWindow.push(review.output);
  totalTokens += review.tokens;
  totalToolCalls += review.calls;

  return {
    content: contextWindow.join("\n---\n"),
    tokensUsed: totalTokens,
    toolCalls: totalToolCalls,
  };
}
```

Bu yaklaşımdaki sorunlar:
- Konekst penceresi her aşamada büyüyor. Değerlendirme aşamasında araştırma notları ve kod ve önceden akıl yürütme içerir.
  Çinçe Çevirisi: 上下文 penceresi her aşamada büyüyor.
- Sistem uyarısı geneldir. Her aşama için ayarlanamaz.
  Çinçe Çevirimiçi: sistem提示是通用──不能为每个阶段调优──
- Hiçbir şey paralel olarak yürümüyor.
  Çeviri: 沒有并行执行──

Tek ajan döngüsü, LLM'yi her dönüşte çok farklı bilişsel görevler ( araştırma vs. kodlama vs. inceleme) arasında bağlam değiştirmeye zorlar.

> 单代理 循环迫使 LLM 每轮在非常不同的认知任务(研究 vs 编码 vs 审阅)之间切换上下文──每次切换都损质──

### İkinci Adım: Uzman Ajanlar

Şimdi paylaşıp her ajan bir iş alır:

> Şimdi onu dağıtın. Her ajan bir görev alıyor.

```typescript
type SpecialistAgent = {
  name: string;
  systemPrompt: string;
  run: (input: string) => Promise<AgentResult>;
};

function createSpecialist(name: string, systemPrompt: string): SpecialistAgent {
  return {
    name,
    systemPrompt,
    run: async (input: string) => {
      const result = await fakeLLMCall(systemPrompt, input);
      return {
        content: result.output,
        tokensUsed: result.tokens,
        toolCalls: result.calls,
      };
    },
  };
}

const researcher = createSpecialist(
  "researcher",
  "You are a technical researcher. Read documentation, find patterns, and summarize findings. Output only the facts needed for implementation."
);

const coder = createSpecialist(
  "coder",
  "You are a senior TypeScript developer. Given requirements and research notes, write clean, tested code. Nothing else."
);

const reviewer = createSpecialist(
  "reviewer",
  "You are a code reviewer. Find bugs, security issues, and logic errors. Be specific. Cite line numbers."
);
```

Her uzmanın odaklı bir ipucu vardır. Her biri sadece ihtiyaç duyduğu girişlerle temiz bir bağlam penceresi alır.

> Her uzmanın bir odak noktası vardır. Her biri temiz bir üst-üst-üst penceresi elde eder.

Araştırmacıların istekleri okuma ve özetleme için optimize edilmiştir. Kodlayıcıların istekleri temiz kod yazmak için optimize edilmiştir. Değerlendirici istekleri hatalar bulmak için optimize edilmiştir. Hiçbir tek istek üçü de yapmaya çalışmaz.

> Araştırmacıların önerileri okuma ve genel sonuç optimizasyonu üzerine. Editörlerin önerileri temiz kod optimizasyonu üzerine.

### Üçüncü Adım: Mesajlar Göndererek Birlikte İşlem Yapın

Uzmanlara açık mesajla haber verin:

> 通過顯示消息傳递将专家连接起来:

```typescript
type AgentMessage = {
  from: string;
  to: string;
  content: string;
  timestamp: number;
};

async function multiAgentApproach(task: string): Promise<AgentResult> {
  const messages: AgentMessage[] = [];
  let totalTokens = 0;
  let totalToolCalls = 0;

  const researchResult = await researcher.run(task);
  messages.push({
    from: "researcher",
    to: "coder",
    content: researchResult.content,
    timestamp: Date.now(),
  });
  totalTokens += researchResult.tokensUsed;
  totalToolCalls += researchResult.toolCalls;

  const coderInput = messages
    .filter((m) => m.to === "coder")
    .map((m) => `[From ${m.from}]: ${m.content}`)
    .join("\n");

  const codeResult = await coder.run(coderInput);
  messages.push({
    from: "coder",
    to: "reviewer",
    content: codeResult.content,
    timestamp: Date.now(),
  });
  totalTokens += codeResult.tokensUsed;
  totalToolCalls += codeResult.toolCalls;

  const reviewerInput = messages
    .filter((m) => m.to === "reviewer")
    .map((m) => `[From ${m.from}]: ${m.content}`)
    .join("\n");

  const reviewResult = await reviewer.run(reviewerInput);
  messages.push({
    from: "reviewer",
    to: "orchestrator",
    content: reviewResult.content,
    timestamp: Date.now(),
  });
  totalTokens += reviewResult.tokensUsed;
  totalToolCalls += reviewResult.toolCalls;

  return {
    content: messages.map((m) => `[${m.from} -> ${m.to}]: ${m.content}`).join("\n\n"),
    tokensUsed: totalTokens,
    toolCalls: totalToolCalls,
  };
}
```

Her ajan sadece kendisine gönderilen mesajları alır.Kontext kirliliği yoktur. Araştırmacıların 50 bin belge okuyuşu asla değerlendirici'nin bağlamına girmez.

> Her ajan sadece kendi mesajını alır. Hiç bir yazılı kirlenme yok. Araştırmacıların aldığı 50 bin numaralar, bir de bir kez daha incilenicinin yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı yazılı

Bu, temel kazanç: bilgi izolasyonu. Her ajanın bağlam penceresi kendi görevine adanmıştır. Bir ajanın 200k token bütçesi diğer ajanların sıfır işlerine harcanmaz.

> Bu, çekirdek avantajıdır: Bilgi ayrımı. Her Ajan'ın üst-üstüne çıkan penceresi kendi görevlerine odaklanır.

### Dördüncü adım: karşılaştır

```typescript
async function compare() {
  const task = "Build a rate limiter middleware for an Express.js API";

  console.log("=== Single Agent ===");
  const single = await singleAgentApproach(task);
  console.log(`Tokens: ${single.tokensUsed}`);
  console.log(`Tool calls: ${single.toolCalls}`);

  console.log("\n=== Multi-Agent ===");
  const multi = await multiAgentApproach(task);
  console.log(`Tokens: ${multi.tokensUsed}`);
  console.log(`Tool calls: ${multi.toolCalls}`);
}
```

Çoklu ajan sürümü daha fazla toplam token kullanır (üç ajan, üç ayrı LLM çağrısı), ancak her ajanın bağlamı temiz kalır.

> Çoğu Ajan  versiyon kullanmak daha fazla toplam token(3 Ajan, üç bağımsız LLM 调用), ama her Ajan'ın üst aşağıdaki yazısı temiz kalmak için.

İşin anlamı açık: daha fazla token harcamak, daha iyi bir çıkış elde etmek.

> 权衡很清晰:花更多令牌,获得更好的输出――任务难时值――对"总结这一段"不值――

## Çerçeveyi kullanın.

Bu ders, ne zaman çoklu ajanlık yapılması gerektiği konusunda tekrar kullanılabilir bir ipucu üretir.`outputs/prompt-multi-agent-decision.md`- Evet .

> Bu ders, ne zaman çoklu ajan kullanılacağını belirlemek için kullanılabilir bir ipucu ortaya çıkardı.`outputs/prompt-multi-agent-decision.md`- Evet.

Bu sorular, dört teşhis sorusunda yer alır: (1) görev 100k'den fazla iş bağlamına ihtiyaç duyar mı? (2) farklı aşamalarda farklı uzmanlığa ihtiyaç duyar mı? (3) paralel iş var mı? (4) karmaşıklık genel maliyetlere değer mi?

> Bu soru dört teşhis sorusunu soruyor: 1) görev 100k'den fazla token gerektiriyor mu? 2) farklı aşamalarda farklı uzmanlık bilgileri gerekmektedir mi? 3) eşleşebilir iş var mı? 4) karmaşıklık satılmaya değer mi?

## Egzersizler.

1. Dördüncü bir uzman ekleyin: kodlayıcıdan kod alan ve inceleyiciden geri bildirimleri inceleyen ve ardından testler yazan bir "tester" ajanı
   Çinçe Çevirim: Ekle dördüncü uzman: bir "testermen" Ajan, kod ve denetleyicinin karşılığını alır, sonra test yazır
2. Tüzükleyi değiştirin böylece inceleyiciler bir inceleme döngüsü için kodlayıcıya geri bildirim gönderebilir (maksimum 2 tur)
   Çinçe Çevirimi: Modify流水线, böylece okuyucuya karşı gönderilen tekrar kodlayıcıya düzenleme döngüsü yapabilmesi için 2 轮)
3. Düzsel boru hattını bir fan-out'a dönüştürün: araştırmacıyı ve "gereklilik analizatörü" ajanını paralel olarak çalıştırın, sonra kodlamacıya geçmeden önce çıkışlarını birleştirin
   Çinçe çevirisi:将顺序流水线转换为扇出:并行运行研究员和"需求分析师"代理,然后合并它们的输出再传递给编码器

## Anahtar Şartlar .

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Swarm / 群体 | "A hive mind of AI agents" / "AI Agent 的蜂巢思维" | A set of peer agents with shared state and no fixed leader. Behavior emerges from local interactions. / 一组具有共享状态且无固定领导者的对等 Agent。行为从局部交互中涌现。 |
| Orchestrator / 编排器 | "The boss agent" / "老板 Agent" | An agent whose tools include spawning and managing other agents. It plans and delegates but may not do the actual work. / 一个工具包括生成和管理其他 Agent 的 Agent。它规划和委派，但可能不做实际工作。 |
| Coordinator / 协调器 | "The traffic cop" / "交通警察" | A non-agent component (often just code, not an LLM) that routes messages between agents based on rules. / 一个非 Agent 组件（通常只是代码，不是 LLM），根据规则在 Agent 之间路由消息。 |
| Consensus / 共识 | "The agents agree" / "Agent 们达成一致" | A protocol where multiple agents must reach agreement before proceeding. Used when conflicting outputs need resolution. / 多个 Agent 在继续之前必须达成一致的协议。用于需要解决冲突输出的情况。 |
| Emergent behavior / 涌现行为 | "The agents figured it out themselves" / "Agent 自己想出来的" | System-level patterns that arise from agent interactions but were not explicitly programmed. Can be useful or harmful. / 从 Agent 交互中产生但未被明确编程的系统级模式。可能有用也可能有害。 |
| Fan-out / fan-in / 扇出/扇入 | "Map-reduce for agents" / "Agent 的 Map-reduce" | Splitting a task across parallel agents (fan-out), then combining their results (fan-in). / 将任务分配给并行 Agent（扇出），然后合并它们的结果（扇入）。 |
| Message passing / 消息传递 | "Agents talk to each other" / "Agent 之间互相交谈" | The communication mechanism between agents: structured data sent from one agent to another, replacing shared context windows. / Agent 之间的通信机制：从一个 Agent 发送到另一个 Agent 的结构化数据，替代共享上下文窗口。 |

## Daha fazla okumak

- [The Landscape of Emerging AI Agent Architectures](https://arxiv.org/abs/2409.02977)- çoklu ajanlı modellerin araştırılması
  Çinçe Çevirim: 新兴 AI Ajanı 架构概览  多 Ajan 模式综述
- [AutoGen: Enabling Next-Gen LLM Applications](https://arxiv.org/abs/2308.08155)- Microsoft'un çok ajanlı konuşma çerçevesini
  Çinçe Çevirimi:AutoGen:赋能下一代 LLM 应用  微软的多代理对话框架
- [Claude Code subagents documentation](https://docs.anthropic.com/en/docs/claude-code)- Claude Code'un görevle nasıl temsil ettiği
  中文翻译:Claude Code 子 Agent 文档  Claude Code 如何使用任务委派
- [CrewAI documentation](https://docs.crewai.com/)- Rol tabanlı çoklu ajan çerçevesini
  Çeviri:CrewAI 文档  基于角色的多代理 框架
