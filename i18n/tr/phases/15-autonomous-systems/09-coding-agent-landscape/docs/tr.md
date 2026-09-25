# Özerk Kodlama Ajanı Landscape (2026)

> SWE-bench Verified, üç yıl içinde% 4'ten% 80,9'a yükseldi. Aynı Claude Sonnet 4.5 SWE-agent v1 üzerinde 43.2% ve Cline otonom üzerinde 59.8% puan aldı. OpenHands (eski OpenDevin) MIT lisanslı en aktif platformdur ve CodeAct döngüsü, JSON araç çağrıları yerine doğrudan bir kum kutusunda Python eylemlerini gerçekleştirir. Başlık sayıları bir metodolojik sorun saklar: SWE-bench Verified görevlerinin 500'inden 161'si sadece 12 satır değişikliğine ihtiyaç duyar ve SWE-bench Pro (10+ satır görevleri) aynı sınır modelleri için 2359%'a sahiptir.

> **【中文解读】**SWE-bench Verified, üç yıl içinde %4'ten %80.9'a yükseldi. Aynı Claude Sonnet 4.5'in SWE-agent v1'de %43.2'e yükseldi. Cline otonom olarak %59.8'e yükseldi. Model etrafındaki yazı makineleri şimdi ve modelin kendisi kadar önemlidir. OpenHands(previous OpenDevin) en aktif MIT lisans platformu, CodeAct döngüsü doğrudan sandıkta Python hareketlerini yerine JSON 工具调用 olarak gerçekleştirir.

> **【拓展：脚手架 > 模型】**2022-2026 yıllarındaki eğilimi, kodlama ajanının yeteneklerinin yükseltilmesinin üç karmaşık kaynağı olduğunu göstermektedir: daha iyi bir temel model, daha iyi bir脚手架 ((CodeAct、反思、验证器循环) 、 daha iyi bir temel (CodeAct、反思、验证器循环) 、 daha iyi bir temel (CodeAct、反思、验证器循环) 、 daha iyi bir temel (CodeAct、反思、验证器循环) 、 daha iyi bir temel (CodeAct、反思、验证器循环) 、 daha iyi bir temel (CodeAct、反思、验证器循环) 、 daha iyi bir temel (CodeAct,反思、验证器循环) 、 daha iyi bir temel (CodeAct,反思、反噪) 、 daha iyi bir temel (CodeAct, ̊CodeAct, ̊CodeAct, ̊CodeAct, ̊CodeAct, ̊CodeAct, ̊CodeAct, ̊CodeAct, ̊CodeAct, ̊CodeAct, ̊CodeAct, ̊CodeAct, ̊CodeAct, ̊CodeAct, ̊C, ̊C, ̊CodeAct, ̊C, ̊C, ̊C, ̊C, ̊C, ̊C, ̊C, ̊C, ̊C, ̊C, ̊C, ̊C, ̊C, ̊d, ̊d, ̊d, ̊C, ̊, ̊, ̊, ̊, ̊, ̊, ̊, ̊, ̊, ̊, ̊, ̊, ̊, ̊, ̊, ̊, ̊, ̊, ̊, ̊, ̊, ̊, ̊, ̊, ̊, ̊, ̊, ̊, ̊, ̊, ̊, ̊, ̊, ̊, ̊, ̊, ̊, ̊, ̊, ̊, ̊

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, CodeAct vs JSON tool-call comparison) | **语言:** Python（标准库，CodeAct vs JSON 工具调用对比）
**Prerequisites:** Phase 14 · 07 (Tool use), Phase 15 · 01 (Long-horizon agents) | **前置知识:** Phase 14 · 07（工具使用），Phase 15 · 01（长程 Agent）
**Time:** ~45 minutes | **时间:** ~45 分钟

>  **【前置】**学本节前 Lütfen önce öğrenin:Fase 14·07(工具调用) 、Fase 14·30+(工作台 Agent 实践) 、Fase 15·01(长程 Agent) 。本节是 2026年编码 Agent 全景图选型必读。
>  **【类比】**选编码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代码 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 代 
> ️ **【易错点】**SWE-bench Verified 分数选 Agent = 被基准骗了──500 个任务里 161 个只需要1-2 行修改(容易),看 SWE-bench Pro(10+ 行真实任务) 分数才有参考价值──修复:选 Agent 前用自己代码库的真实问题 测试,而不是看营销基准──

## Sorunlar. Sorunlar.

> **【中文解读】**编码 景观 is 2025-2026 yılları en hızlı değişen AI 应用领域lerden biri. Ana oyunculara Claude Code,Cursor,GitHub Copilot,Devin,Windsurf vb. dahil.

> **【拓展：coding agent landscape】**2026年编码 代理的竞争格局:(1) Claude CodeAnthropic'in kendi kendine kodlama ajanı, tüm geliştirme, Git 操作和终端命令执行'ı destekler;(2) Cursor VS Code'un AI editörüne dayanan, insanların işbirliğini vurgular;(3) DevinCognition AI'in kendi kendine kodlama ajanı, bağımsız olarak geliştirme görevlerini tamamlayabilir;(4) Windsurf(原 Codeium) AI 優先 IDE──SWE-bench 上的表现是主要竞争指标;;

Doğru soru şu: işime uyan bir görev dağılımında, üretimdeki asfaltla, sonundan sonuna kadar hangi güvenilirliğe sahip olacağım?

> "En iyi kodlama ajanı" yanlış bir soru. Gerçek soru şu: İşime uygun görev dağılımında, üretim sırasında çalışacağım bir yazı levhası kullanarak, ne kadar güvenilir olabileceğim?

2022 ile 2026 yılları arasında alan, asfaltlama  kurtarma katmanı, planlayıcısı, kum kutusu, düzenleme-temizleme döngüsü, geri bildirim biçimi  yük taşıyan olduğunu öğrendi. Claude Sonnet 4.5 SWE-agent v1 üzerinde SWE-benç Verified üzerinde %43,2 puan aldı; aynı model Cline'in otonom asfaltında %59,8 puan aldı. 16.6 mutlak fark noktaları, aynı ağırlıklar. Temel model bir bileşen; döngü üründür.

> 2022-2026 yılları arasında, alanlar arasında yazılımcılık, programcılık, sandık, edit-verification döngüsü, karşısındaki biçim ve yükümlülüktür.

> **【中文解读】**Bu bölümde AI Ajanının temel kavramı ve gerçekleştirme yöntemleri ele alınıyor. Ajan, çevreyi gözlemleyebilen, kararlar verebilen, eylemleri gerçekleştiren ve hedefleri gerçekleştirene kadar döngülenebilen LLM tarafından yönlendirilmiş bir otonom sistemdir.

Yanlısı sorun, referans derecesi doymuşluğunun geri dönüşleri gizlemesidir.

> 伴奏問題是基准和隐藏回归──

SWE-bench Verified, doymuş gibi yakın ve kolay görev kuyruğu (161'i 500 görevin içinde ≤2 satır gerektirir) en yüksek puanları çıkarır. Gerçek dünya kalitesi daha iyi SWE-bench Pro gibi dağıtımlarda ölçülür (10+ satır değişikliği), aynı liderlerin hala 2359%'da oturduğu yerlerde.

> SWE-benç Verified 接近和,简单任务尾部(500 个任务中 161 个需要 ≤2 行) 拉高顶级分数──现实世界质量在SWE-bench Pro(10+ 行变更)等分布上测量更好,同领先者仍然只有23-59%──

## Konsepten bir şey.

### SWE-benç, bir paragraf SWE-benç bir bölüm

SWE-bench (Jimenez ve diğerleri) gerçek GitHub sorunlarını temel gerçeklik patchleriyle alır ve bir ajanı test paketini geçiren bir patch üretmesini ister. SWE-bench Verified (OpenAI, 2024) belirsiz ve kırık görevleri kaldırılan insan kuralı 500 görev alt kümesidir. SWE-bench Pro, 10+ değişim çizgisi gerektiren daha zor halefi  görevlerdir.

> SWE-bench(Jimenez 等人) Get real fixin of real GitHub issue, requiring Agent 产生使测试套件通过补丁──SWE-bench Verified(OpenAI,2024) is an artificial策划ing 500 任务子集, deblblbl and损坏的任务──SWE-bench Pro is easier of successor需 10+ 行变更任务,当前前沿 Agent 在 23-59%──

### 2022 → 2026 eğri aslında ne gösteriyor.

- **2022**: %4'lik araştırma modelleri çiğ SWE-benç üzerinde.
  Çeviri:**2022**:研究模型在原始 SWE-bench 上约 4%──
- **2024**: GPT-4 + Devin tarzı asfaltlama %14; SWE-ağentme %12
  Çeviri:**2024**:GPT-4 + Devin 式脚手架約 14%;SWE-agent 约 12%──
- **2025**: Claude 3.5/3.7 Aider ve SWE ajanı içindeki Sonet 40~55% aralığına doğru ilerler.
  Çeviri:**2025**Sonet: Klavüde 3.5/3.7 Aider ve SWE-Agent İçin 40-55%                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
- **2026**Claude Sonnet 4.5 ve SWE-bencinde 70~80%+'de sınır rekabetçileri Verified.
  Çeviri:**2026**Claude Sonnet 4.5 &amp; Frontonter rekabetçi SWE-bençinde Verified Up 70-80% +──Epoch AI'nın sıralaması gerçek zaman takip────

İndirme üç bileşik kaynaktan geldi: daha iyi temel modeller, daha iyi asfaltlama (CodeAct, yansıma, doğrulayıcı döngüler) ve daha iyi referanslar (Tahqiqatlı gürültü çıkarma).

> 斜率来自三个复合源:更好的基础模型、更好的脚手架(CodeAct、反思、验证器循环) 更多的基准(Verified 去除噪音)

### CodeAct vs JSON araç çağrıları .

OpenHands (All-Hands-AI, arXiv:2407.16741, eski OpenDevin) belirli bir mimari bahis yaptı: bir host tarafından dekode edilen ve uygulanan JSON araç çağrılarını yayımlayan modelin yerine, model Python kodu yayar ve Jupyter tarzı bir çekirdeği onu kum kutuunda çalıştırabilir. Ajan dosyaları, zincir araçlarını döngüye alabilir ve bir eylem içinde kendi istisnalarını yakalayabilir.

> OpenHands(All-Hands-AI,arXiv:2407.16741,前 OpenDevin) belirli bir yapı altında 注: model artık ev sahibi tarafından executed JSON 工具调用 tarafından gönderilmez, ancak Python 代码, Jupyter tarafından 风格内核在沙箱中运行──Agent bir hareket içinde döngül dosya、链式工具、捕获自身异常──

- İşbirliği:

> 权衡:

- **JSON tool calls**: her eylem bir dönüştür; denetleme kolay; kısıtlı kompozisyon; varsayılan olarak güvenli çünkü her çağrı açık bir onaylayıcıdan geçer.
  Çeviri:**JSON 工具调用**Her seferinde açık bir denetleme aracı üzerinden yapılan bir arama için:
- **CodeAct**: bir eylem tüm bir program olabilir; kompozisyonal; sert bir kum kutusu gerektirir (OpenHands Docker izolasyonunu kullanır); başarısızlık modları kum kutusu çalıştırma süresi izin veren her şeyi içerir.
  Çeviri:**CodeAct**Bir hareket tüm süreci oluşturabilir; birleştirilmelidir; bir sandık kullanmak gerekir; bir başarısızlık modeli, sandık çalışmasını içerir.

Her iki mimarlık da üretimde. CodeAct açık platformlarda (OpenHands, smolagents) baskındır. JSON araç çağrıları, icracıyı sağlayan sağlayıcı kontrol ettiği yönetilen hizmetlerde (Anthropic Managed Agents, OpenAI Asistanları) baskın kalır.

> 两种架构都在生产中.CodeAct 在开放平台(OpenHands、smolagents) 主导.

### 2026 manzarasında asfaltlar.

| Scaffold | License | Execution model | Notable property |
|---|---|---|---|
| 脚手架 | 许可 | 执行模型 | 显著属性 |
| OpenHands (OpenDevin) | MIT | CodeAct in Docker | Most active open platform; event-stream replayable |
| OpenHands（OpenDevin） | MIT | Docker 中 CodeAct | 最活跃开放平台；事件流可重放 |
| SWE-agent | MIT | Agent-Computer Interface (ACI) | First end-to-end SWE-bench scaffold |
| SWE-agent | MIT | Agent-计算机接口（ACI） | 首个端到端 SWE-bench 脚手架 |
| Aider | Apache-2 | edit-via-diff in local repo | Minimal scaffold, strong regression stability |
| Aider | Apache-2 | 本地仓库 edit-via-diff | 最小脚手架，强回归稳定性 |
| Cline | Apache-2 | VS Code agent with tool policy | Highest-scoring open scaffold on Sonnet 4.5 |
| Cline | Apache-2 | 带工具策略的 VS Code Agent | Sonnet 4.5 上得分最高的开放脚手架 |
| Devin (Cognition) | Proprietary | Managed VM + planner | First "AI software engineer" product category |
| Devin（Cognition） | 专有 | 管理 VM + 规划器 | 首个"AI 软件工程师"产品类别 |
| Claude Code | Proprietary | Permission modes + routines | Lesson 10 covers the agent loop in detail |
| Claude Code | 专有 | 权限模式 + 例程 | 第 10 课详细介绍 Agent 循环 |

### Neden asfaltlar hakim? Neden asfaltlar hakim?

Bir kodlama koşusu uzun ufuklu bir yoldur (Dene 1) Merdivenler boyunca güvenilirlik bileşikleri.

> 编码运行是长程轨迹 (第 1 课) ◊ güvenilirlik跨步骤复合――脚手架买入分数的三个地方:

1. **Retrieval**SWE-Agent'in ACI, OpenHands'in dosya indeksleri ve Aider'in repo haritası hepsinin saldırısı.
   Çeviri:**检索**Bu konuda bir açıklama yaparak, bu konuda bir açıklama yaparak, bu konuda bir açıklama yaparak, bu konuda bir açıklama yaparak, bu konuda bir açıklama yaparak, bu konuda bir açıklama yaparak, bu konuda bir açıklama yaparak, bu konuda bir açıklama yaparak, bu konuda bir açıklama yaparak, bu konuda bir açıklama yaparak, bu konuda bir açıklama yaparak, bu konuda bir açıklama yaparak, bu konuda bir açıklama yaparak, bu konuda bir açıklama yaparak, bu konuda bir açıklama yaparak, bu konuda bir açıklama yaparak, bu konuda bir açıklama yaparak, bu konuda bir açıklama yaparak, bu konuda bir açıklama yaparak, bu konuda bir açıklama yaparak, bu konuda bir açıklama yaparak, bu konuda bir açıklama yaparak, bu konuda bir açıklama yaparak, bu konuda bir açıklama yaparak, bu konuda bir açıklama yaparak, bu konuda bir açıklama yaparak, bu konuda bir açıklama yaparak, bu konuda bir açıklama yaparak, bu konuda bir açıklama yaparak, bu konuda bir bir açıklama yaparak, bu konuda bir bir bir düzenlemde bir düzenlemde,
2. **Verifier loop**SWE-benç üzerinde 10+ puan delta ile testler yapılır, yığın izlerini okur ve tekrar denenilir.
   Çeviri:**验证器循环**SWE-bençinde tekrar çalışmak: 10+ nokta artışı
3. **Failure containment**Bu nedenle, bir verifiyeci döngüsü ile ve olmadan aynı model iki farklı ürüne benziyor.
   Çeviri:**失败遏制**Bu nedenle, bir ürün için bir vericilik sistemi kullanılır.

### Benchmark doymuşluğu ve gerçek dağılım.

OpenHands yazarları ve Epoch AI hem SWE-bench Verified'in kolay bir kuyruğu olduğunu belirtti: 500 görevden 161'i sadece 12 değişim çizgisi gerektirir. Yüksek puanlar kısmen bu kuyruğun etkisiyle hareket eder. SWE-bench Pro 10+ çizgi değişimlerine sınırlandırır ve sınır sistemleri için bile 2359% aralığında puanlar verir. Üretim dağılımınız neredeyse kesinlikle Verified'e göre Pro'ya daha yakındır.

> OpenHands yazarı ve Epoch AI tarafından belirtilen SWE-bench Verified 有简单尾部:500 个任务中 161 个 个只需要1-2 行变更──高分部分由该尾部驱动──SWE-bench Pro 限制10+ 行变更,即使前沿系统也返回23-59% 范围──你的生产分布几乎肯定更接近Pro而非 Verified──

Bir ajan seçimi için etkisi: kendi hata arka arkadasının Pro'ya benzer bir alt kümesini çalıştırın. Önemli olan puan, gönderdiğiniz görevlerin temsilcisi olan puanıdır.

> 选择 Agent 的含义: kendi hata 积压上运行 Pro 类子集── önemli分数 is representing your posting task──

## Çerçeveyi kullanın.
```figure
a5-scaffold-delta
```

## Kullan

`code/main.py`sabit bir mini görev dağılımında iki oyuncak ajanı asfaltı karşılaştırılır:

> `code/main.py`Düzgün Mini görev dağılımında iki oyuncak ajanı karşılaştır:

1. A.**JSON tool-call**Bir turda bir hareket yapan bir heykel.
   Çeviri:**JSON 工具调用**Bir de her seferinde bir hareket.
2. A.**CodeAct**Bir harekete küçük bir Python fragmanı gönderebilecek bir heykel.
   Çeviri:**CodeAct**Kılavuz, her hareket küçük Python kod parçaları çıkarabilir.

Her ikisi de bir "model" (deterministik kurallar) kullanır, bu nedenle karşılaştırma asfaltı model kalitesinden ayırır.

> 两者使用存根"模型" (birbirliği kuralları)                                                                                                                                                                                                                                                       

## İndirin . Ürünler .

`outputs/skill-scaffold-audit.md`kabul edilmeden önce önerilen kodlama ajanı asfaltını denetlemenize yardımcı olur: geri alım kalitesi, doğrulayıcı varlığı, kum kutu izolesi ve referans değerinden dağıtım için uygunluk.

> `outputs/skill-scaffold-audit.md`助你在采用前审计提议编码 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编辑 编

## Egzersizler.

1. Çık .`code/main.py`Her bir asfalt aynı görev setinde kaç dönüş yapar?
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`code/main.py`❖ Aynı görev kitlesinde her bir komut için kaç tane tur var?

2. OpenHands kağıdı okuyun (arXiv:2407.16741). Kağıt CodeAct'in karmaşık görevlerde JSON aracı çağrılarını yendiğini iddia ediyor. Kağıtın kabul ettiği bir başarısızlık modunu tanımlayın ve bu modun üretimde ne zaman baskın olacağı konusunda bir cümle yazın.
   Çinçe çevirisi: oku OpenHands 论文(arXiv:2407.16741)。论文论证 CodeAct 在复杂任务上胜胜 JSON 工具调用。识别论文承认一个失败模式并写一句该模式在生产中何时主导。

3. İki dosya boyunca 10+ değişim satırı gerektiren bir hata arka arkadan bir görev seçin. (a) JSON araç çağrıları ve (b) CodeAct altında bir sınır modeli için uçtan sona başarı olasılığını tahmin edin. Boşluğu haklı çıkarın.
   Çinçe çevirisi: Your bug 积压中中选一个需要跨两文件 10+ 行变更的任务──估算前沿模型在 (a) JSON 工具调用和 (b) CodeAct 下的端到端成功概率──论证差距──

4. SWE-bench Verified'de 161 tek dosya, 12 satırlı görev var. Onları dışlayan bir puan oluşturun.
   Çinçe Çevirim:SWE-benç Verified 161 个单文件 1-2 行任务──构建排除它们的分数──排行榜如何重排?

5. "SWE-bench Verified" (OpenAI) başlatmayı okuyun.
   Çine dilinde yapılan yorum: "SWE-bench Verified" ("SWE-bench Verified") başlatılması, "OpenAI")

## Anahtar Şartlar .

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| SWE-bench | "Coding benchmark" | Real GitHub issues with ground-truth patches and test suites |
| SWE-bench | "编码基准" | 带真实补丁和测试套件的真实 GitHub issue |
| SWE-bench Verified | "Cleaned subset" | 500 human-curated tasks, easier-tail present |
| SWE-bench Verified | "清理的子集" | 500 个手工策划任务，存在简单尾部 |
| SWE-bench Pro | "Harder subset" | 10+ line changes; frontier sits at 23–59% |
| SWE-bench Pro | "更难的子集" | 10+ 行变更；前沿在 23-59% |
| CodeAct | "Code-as-action" | Agent emits Python; Jupyter-style kernel executes in sandbox |
| CodeAct | "代码即动作" | Agent 发出 Python；Jupyter 风格内核在沙箱执行 |
| JSON tool call | "Function calling" | Each action is a structured JSON payload validated before execution |
| JSON 工具调用 | "函数调用" | 每动作是执行前验证的结构化 JSON 负载 |
| Scaffold | "Agent framework" | Retrieval + planner + executor + verifier loop around the base model |
| 脚手架 | "Agent 框架" | 围绕基础模型的检索 + 规划器 + 执行器 + 验证器循环 |
| ACI (Agent-Computer Interface) | "SWE-agent's format" | Command set designed for LLM ergonomics, not human shells |
| ACI（Agent-计算机接口） | "SWE-agent 格式" | 为 LLM 人体工程学设计的命令集，非人类 shell |
| Verifier loop | "Test-and-retry" | Run tests, read output, revise patch; biggest non-model reliability gain |
| 验证器循环 | "测试并重试" | 运行测试、读输出、修订补丁；最大非模型可靠性增益 |

## Daha fazla okumak

- [Jimenez et al. — SWE-bench](https://www.swebench.com/) orijinal referans değer ve metodoloji.
  Çinçe Çevirisi:原始基准和方法論。
- [OpenAI — Introducing SWE-bench Verified](https://openai.com/index/introducing-swe-bench-verified/) kurate alt kümenin nasıl inşa edildiği.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri
- [Wang et al. — OpenHands: An Open Platform for AI Software Developers](https://arxiv.org/abs/2407.16741) CodeAct mimarisi ve olay akışı tasarımı.
  Çevre:CodeAct 架构和事件流设计
- [Epoch AI — SWE-bench leaderboard](https://epoch.ai/benchmarks)- Canlı izlenen notlar.
  Çin Çeviri:实时跟踪分数──
- [Anthropic — Measuring agent autonomy](https://www.anthropic.com/research/measuring-agent-autonomy) uzun uzayda kodlama ajanı güvenilirliği çerçevesini oluşturmak.
  Çinçe Çevirisi:长程编码 Agent 可靠性框架──
