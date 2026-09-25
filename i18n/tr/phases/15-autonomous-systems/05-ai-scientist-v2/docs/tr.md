# AI Bilimci v2  Atölyel-Deneli Otonom Araştırma  AI Bilimci v2  Çalışmaları seviyesinde kendiliğinden araştırma

> Sakana'nın AI Bilimcisi v2 (Yamada et al., arXiv:2504.08066) tam araştırma döngüsünü yürütüyor: hipotez, kod, deneyler, rakamlar, yazma, gönderme. Bu, ICLR 2025 atölyesinde bir kağıt geçiş eşcinsel incelemesine sahip olan ilk sistemdir. Bağımsız değerlendirme (Beel et al.) deneylerin %42'si kodlama hatalarından başarısız olduğunu ve literatür incelemesi sıklıkla kurulmuş kavramları yeni olarak yanlış etiketlediğini buldu. Sakana'nın doktorları kod tabanının LLM yazılı kodunu uyguladığını ve Docker izolasyonunu önerdiğini uyarıyor. Bu resmin her iki yarısı da önemli.

> **【中文解读】**Sakana'nın AI Bilimcisi v2(Yamada 等人,arXiv:2504.08066) tam bir araştırma döngüsünü yürütüyor: varsayım, kodlama, deney, grafik, yazma, gönderme. ICLR 2025 工作坊 eş eş inceleme sistemleri üzerinden ilk ortaya çıkan çalışma sistemidir.

> **【拓展：开放式研究的代价】**AlphaEvolve ve DGM'de "makine kontrol edilebilir değerlendirme cihazı" var.  birim testi veya基准. Araştırma yoktur: makale, birim testi değil, muayenetçi tarafından değerlendirilmiştir. Bu, kapalı bir çerçeveyi daha zorlaştırır, ancak değer de daha yüksektir.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, research-loop state-machine toy) | **语言:** Python（标准库，研究循环状态机玩具）
**Prerequisites:** Phase 15 · 03 (AlphaEvolve), Phase 15 · 04 (DGM) | **前置知识:** Phase 15 · 03（AlphaEvolve），Phase 15 · 04（DGM）
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**Öğrenci bölümünün önüne geçerek:Fase 15·03-04(AlphaEvolve/DGM)、Fase 14·30+(工作台 Agent 实践)、学术论文写作基础──AI Bilimci = 开放式研究任务,评估器是"同行评审"(弱信号),所以安全模型完全不同──
>  **【类比】**AI Scientist = "AI 博士生"──AlphaEvolve/DGM = 工程师(评估器=单元测试,强信号);AI Scientist = 博士生(评估器=审稿人,弱信号)──同样跑实验-评估-代循环,但弱信号评估让 Agent 容易欺骗自己42% 的实验代码有错,文献综述把已知概念当新发现──修复:(1) Docker 隔离(必须执行 LLM 代码沙箱化);(2) 人类复核(披露 AI 生成);(3) 强信号检查(如复现性测试) 

## Sorunlar. Sorunlar.

Araştırma, açık bir görevdir.

> Araştırma açık bir görev.

AlphaEvolve'in algoritmik arama veya DGM'in referans sınırlı kendi kendine değiştirmesinden farklı olarak, bir araştırma sonucu makine kontrol edilebilir doğruluk kriterine sahip değildir. Bir makale birim testleri değil, inceleyiciler tarafından değerlendirilir. Bu da döngüyü kapatmayı zorlaştırır  ve kapatıldığında daha değerli olur, çünkü araştırma karmaşık ilerlemenin yaşadığı yerdir.

> AlphaEvolve'un algoritma arama veya DGM'in temel kurallarına göre, çalışma sonuçları, inceleme makinesi tarafından kontrol edilebilir doğruluk standartları ile farklıdır.

AI Bilimci v1 (Sakana, 2024) insan tarafından yazılan şablonlardan başlayarak döngüyü kapattı. LLM, sabit bir heykel içinde deneyler yaptı. AI Scientist v2 (Yamada et al., 2025) görme dili modeli eleştirisi döngüsü ile ajanistik ağaç arama kullanılarak şablon gereksinimini kaldırır. Sistem fikirler üretiyor, deneyler uyguluyor, rakamlar üretir, bir makale yazıyor ve eleştirmen geri bildirimlerini tekrarlıyor.

> AI Bilimci v1(Sakana,2024) insan yazılı modelden geçerek kapanış döngüsüne başladı.LLM sabit bir yazı çerçevesinde doldurma deneyimi.

> **【中文解读】**AI Scientist v2 (Sakana, 2025) 运行完整的研究循环:假设,编码,实验,图表,论文撰写和提交―― ICLR 2025 工作坊同行评审系统通过的第一种有生成论文系统――但独立评估发现 42% 实验因编码错误失败,文献综述经常将已建立的概念标记为新──两面都是事实──

Eşcinsel değerlendirme hükümü: bir v2 üretilen makale ICLR 2025 atölyesinde kabul edildi (açıklama ile). Bağımsız değerlendirme hükümü: sistem güvenilir olmaktan çok uzak. Her ikisi de doğru.

> 同行评审结论:一篇 v2 生成的论文被ICLR 2025 工作坊接受(附带披露) ・独立评估结论:系统远非可靠──两者都是事实──

## Konsepten bir şey.

### Mimarlık, mimarlık.

1. **Idea generation.**LLM, bir konu ve önceki literatür üzerinde koşullanmış araştırma fikirlerini önerir. v1 şablonları kullanır; v2 bir hipotez alanı üzerinde ajantik arama kullanır.
   Çeviri:**想法生成。**LLM  teme ve önceki yayınlara dayalı araştırma fikirleri önermektedir.
2. **Novelty check.**Bir edebiyat kurtarma adım fikri yayınlanmış olup olmadığını kontrol eder. Bu Beel et al's değerlendirmesinin yanlış etiketleme bulduğu adımdır  sıklıkla yenilik olarak sınıflandırılan kurulmuş yöntemler.
   Çeviri:**新颖性检查。**文献检查步骤思想是否已发表.                                                                                                                                                                                                                                                         
3. **Experiment plan.**Ajan bir deneysel protokol hazırlıyor ve kod yazıyor.
   Çeviri:**实验计划。**Agent 起草实验协议并编写代码──
4. **Execution.**Beel et al'ın ölçümlerinde, bu aşamada yapılan deneylerin %42'si kodlama hatalarından dolayı başarısız oldu.
   Çeviri:**执行。**代码在沙箱中运行──失败反到重试循环── Beel ve diğer insanların ölçümlerinde, %42'si bu aşamada kodlama hatası nedeniyle başarısız oldu.
5. **Figure generation.**Görüş dil modelinde oluşturulan rakamları okuyor ve açıklık için yeniden yazıyor.
   Çeviri:**图表生成。**视觉语言模型读取生成图表并为清晰性重写它们──这是 v2 的关键技术添加──
6. **Writeup.**LLM bir makale hazırlar, iç bir inceleyicilerle tekrarlar.
   Çeviri:**撰写。**LLM 起草论文,与内部审稿人代──
7. **Optional: submission.**Kağıt bir yere teslim edilir.
   Çeviri:**可选：提交。**论文提交到会议──

### Atölyenin kabul sonucu ne anlama geliyor?

Bir v2 üretilen makale ICLR 2025 atölyesinde bir eşeğince incelemeyi geçti. Yazarlar makaleyi program komitesine açıkladı. Kabul bir veri noktasıdır; sistemin " Araştırma yapıyor " diyerek iddia etmek için bir lisans değildir.

> Bir v2 生成的论文在ICLR 2025 工作坊通过同行评审――作者向程序委员会披露论文的来源――接受是一个数据点;不是声称系统的"做研究"的许可――

Önemli bağlam: atölye makaleleri ana konferans makaleleri ile karşılaştırıldığında daha düşük bir bardır. Eşcinsel inceleme gürültülüdür; verilen bir günde gönderilenlerin küçük bir kısmı kabul edilir. Bir başarı bir konsept kanıtıdır, güvenilirlik iddiası değildir. Nature 2026 makalesi son-son döngüyü belgelendirir ve kendisi insan araştırmacıları tarafından birlikte yazılmıştır; "sistem bir Nature makalesi yazmadı".

> 重要背景:工作坊论文的门低于主会议论文──同行评审有噪音;任何一天都有一小部分提交被接受──一次成功是概念证明,不是可靠性声明──自然 2026 论文记录端到端循环,本身由人类研究人员共同撰写;不是"系统写了一篇自然论文"──

### Bağımsız değerlendirmenin bulduğu sonuçlar

Beel et al. (arXiv:2502.14297) bir dış değerlendirme yaptı.

> Beel 等人 ((arXiv:2502.14297) 运行了外部评估──标题性发现:

- **Experiment failures.**Deneyimlerin %42'si kodlama hataları (kötü ithalatlar, şekil eşleşme eksikliği, tanımlanamayan değişkenler) nedeniyle başarısız oldu.
  Çeviri:**实验失败。**%42'si deneylerin birçoğunun kodlama hatası başarısız oldu.
- **Novelty mislabeling.**Edebiyat-içinde bulma adımları sıklıkla kurulmuş kavramları yeni olarak işaretler. Bu, halüsinasyonun araştırma eşdeğeri.
  Çeviri:**新颖性错误标记。**文献检索步骤频繁 文献检索步骤频繁 文献检索步骤频繁 文献检索步骤频繁将已建立的概念标记为新────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
- **Presentation-quality gap.**Görme dili figür eleştirisi, temel deneysel zayıflıkları gizleyen yayın derecesi görseller üretti.
  Çeviri:**呈现质量差距。**视觉语言图表评审产生出版级视觉效果, gömüyor alt seviye deney zayıflıklarını.

Son bulgu bu aşamada önemli bir bulgu: ikna edici araştırma yapmadan ikna edici sonuçlar üreten bir sistem, açıkça başarısız olan bir sistemden daha tehlikeli, daha güvenli değil.

> Son bulgu bu aşamada önemli bir noktaya sahiptir. İnanılmaz bir çıkış üreten ama inanılmaz bir şekilde çalışılmayan sistemler, açıkça başarısız olan sistemlerden daha tehlikeli ve daha güvenli değildir.

Değerlendirme, rakamlara kadar değil, temel iddialara ulaşmalıdır.

> 评估, tabloda durmak yerine alt kat açıklamalara değinmek gerekir.

### Kum kutusu kaçış endişesi.

Sakana'nın kendi depoları README uyarıyor:

> Sakana  kendi depo README 警告:

> LLM'den kaynaklanan kodları uygulayan bu yazılımın doğası nedeniyle, güvenliğini garanti edemeyiz. Tehlikeli paketlerin, kontrolsüz web erişiminin ve istenmeyen süreçlerin doğuşu riskleri vardır.

> Bu yazılım LLM'nin gelişim kodunu gerçekleştirdiği için, güvenlik garanti edilemiyor.

Bu, doğrulanmamış bir alanda özerkliğin işletim şeklidir. LLM kod yazar; kod çalışır; kod işlemin yapmasına izin verilen her şeyi yapabilir. Dosya sistemi, ağ ve işlem eylemlerini zor sınırlayan kum kutusu olmadan, herhangi bir kendi kendini yönlendiren araştırma ajanı verileri sızdırır, hesapları yakır veya kendini yeniden yazabilir.

> Bu, kanıtlanmamış alanlarda kendiliğinden işletim biçimidir. LLM  write code; code run; code can do process allowed anything. Hard limit file system, network and process operation sandığı yoktur.

AlphaEvolve'in kum kutu hikayesi, değerlendirici sıkı olduğu için daha kolaydır. AI Scientist v2'nin döngüsü açık sonlu hedeflerle açık sonlu kod çalıştırır. Bu nedenle sistemden ayrılmadan önce daha güçlü bir izolasyon (Docker minimum; seccomp / gVisor tercih edilir) ve her gönderimin manuel bir incelemesine ihtiyaç duyar.

> AlphaEvolve'in sandığı anlatımı daha kolay, çünkü değerlendirme cihazı sıkı. AI Scientist v2'in döngüsü açık hedeflerle açık kod kullanıyor. İşte bu yüzden daha güçlü bir ayrım gerektirir.

### V2'nin sınırda olduğu yerde.

| System | Target | Output kind | Evaluator | Known failure |
|---|---|---|---|---|
| 系统 | 目标 | 输出类型 | 评估器 | 已知失败 |
| AlphaEvolve | algorithms | code | unit + benchmark | bounded by evaluator rigor |
| AlphaEvolve | 算法 | 代码 | 单元 + 基准 | 受评估器严谨性约束 |
| DGM | agent scaffolding | code | SWE-bench | reward hacking |
| DGM | Agent 脚手架 | 代码 | SWE-bench | 奖励篡改 |
| AI Scientist v2 | research papers | text + code + figures | peer review (weak) | experiment failures, mislabeling, polish masking weakness |
| AI Scientist v2 | 研究论文 | 文本 + 代码 + 图表 | 同行评审（弱） | 实验失败、错误标记、修饰掩盖弱点 |

V2 üçün en zayıf otomatik değerlendirici, en geniş çıkış yüzeyi ve kamu eserlerine en kısa yolu vardır.

> v2 Üçün en zayıf otomatik değerlendirme cihazına sahip olmak, en geniş çıkış yüzüne ve en kısa açık ürün yoluna sahip olmak.

İşlem kontrolleri (sandbox, inceleme, açıklama) güvenlik işlerinin büyük kısmını yapıyor.

> 操作控制 (Sah箱, inceleme, açıklama) güvenlik işinin büyük kısmını üstlendi.

## Çerçeveyi kullanın.
```figure
mx-research-loop
```

## Kullan

`code/main.py`v2 döngüsünü bir durum makinesi olarak simüle eder: fikir → yenilik kontrol → deney → figür → yazma → inceleme → kabul-veya tekrarlama. Her durum Beel et al. bulgularından alınan yapılandırılabilir bir başarısızlık olasılığına sahiptir. Simülatörü N döngüsleri için çalıştırın ve sayın:

> `code/main.py`将 v2 循环模拟为状态机:想法 → 新性检查 → 实验 → 图表 → 撰写 → 审稿 → 接受或代―― her durumda Beel 等人 tarafından elde edilen 提取的可配置失败概率──运行模拟器 N 个循环并计数:

- Ne kadar fikirler teslim olur.
  Çeviri: Ne kadar fikir gönderilene kadar.
- Kaç tane yazının inceleme kağıdındaki kritik bir deney hatası olabilir.
  Çinçe Çevirisi: ne kadar gönderilmiş olacak?
- Yeniden deneme bütçeleri kalite karşı verim ile nasıl değişir.
  Çinçe çevirisi: 重试预算 nasıl kalite ile üretim arasında bir tartışma yapar.

## İndirin . Ürünler .

`outputs/skill-ai-scientist-sandbox-review.md`Araştırma döngüsü ajanı tarafından sandbox'dan çıkmadan önce üretilen her şey için iki kapı bir inceleme kontrol listesi.

> `outputs/skill-ai-scientist-sandbox-review.md`Bu nedenle, bu ürünlerin tümü, bir ürün olarak kullanılmaktadır.

## Egzersizler.

1. Çık .`code/main.py`Bu, bir "temiz" kağıt üreten bir döngü çalışmasının hangi bölümüdür?
   Çeviri:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          `code/main.py` Çekil çalışmaların "çık" çalışmaların ne kadar oranında oluştuğunu?

2. Defaultlar zaten Beel et al. ' nin % 42 / 25% ' si kullanıyor .`--experiment-failure 0.20 --novelty-mislabel 0.10`Sonra da `--experiment-failure 0.60 --novelty-mislabel 0.40`- Peki iki koşuk arasında nasıl bir parçanın değişmesi olur?
   Çeviri: %42 / %25`--experiment-failure 0.20 --novelty-mislabel 0.10`Çıkıp koş, sonra kullan.`--experiment-failure 0.60 --novelty-mislabel 0.40`◊ İki sefer arasında yapılan değişikliklerin ama eksiklerin oranı nasıl değişir?

3. Sakana'nın AI Scientist v2 repo README'sini sandbox gereksinimleri üzerine okuyun.
   Çinçe Çevirimi:Sakana AI Bilimci v2  deposu README 关于沙箱要求──命名你会为多日自主运行添加的两项额外限制(除Docker 外)。

4. Beel et al. bölüm 4'ü okuyun.
   Çin dilinde:Beli  et al. 4. bölüm, mevcut kalite farkı hakkında.

5. Araştırma ajanlarının sonuçları için "doktor her makaleyi okuyor"dan daha iyi ölçülecek bir insan inceleme protokolü önerin.
   Çinçe Çevirimi: için araştırma Agent 输出提议比"博士读每篇论文"扩展更好的人工审查协议──识别瓶并根据此设计──

## Anahtar Şartlar .

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| AI Scientist v1 | "Sakana's templated research agent" | Filled experiments into a fixed scaffold |
| AI Scientist v1 | "Sakana 的模板研究 Agent" | 在固定脚手架中填充实验 |
| AI Scientist v2 | "Template-free research agent" | Agentic tree search with VLM figure critique |
| AI Scientist v2 | "无模板研究 Agent" | 带有 VLM 图表评审的 Agent 式树搜索 |
| Agentic tree search | "Branching research agent" | Expands multiple experiment plans in parallel; prunes by internal critic |
| Agent 式树搜索 | "分支研究 Agent" | 并行展开多个实验计划；由内部评论者修剪 |
| Vision-language critique | "VLM polish on figures" | Multimodal model reads figures and rewrites them for clarity |
| 视觉语言评审 | "VLM 修饰图表" | 多模态模型读取图表并为清晰性重写 |
| Literature retrieval | "Novelty check" | Searches prior work to confirm idea novelty — documented to mislabel |
| 文献检索 | "新颖性检查" | 搜索先前工作以确认想法新颖性——文档记录会错误标记 |
| Polish masking | "Pretty paper, broken research" | Presentation quality exceeds experimental quality; hides weaknesses |
| 修饰掩盖 | "漂亮论文，破碎研究" | 呈现质量超过实验质量；隐藏弱点 |
| Sandbox escape | "LLM code breaks out" | Agent-executed code does things the loop designer did not intend |
| 沙箱逃逸 | "LLM 代码逃逸" | Agent 执行的代码做循环设计者未预期的事 |

## Daha fazla okumak

- [Yamada et al. (2025). The AI Scientist-v2](https://arxiv.org/abs/2504.08066)Kağıt.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri
- [Sakana blog on the Nature 2026 publication](https://sakana.ai/ai-scientist-nature/) Tıpkı bir eşeğen değerlendirme bağlamı ile tedarikçi özet.
  Çin dilinde:厂商摘要,含同行评审背景──
- [Beel et al. (2025). Independent evaluation of The AI Scientist](https://arxiv.org/abs/2502.14297) Dış değerlendirme numaraları.
  Çevreci değerlendirme sayısı
- [Sakana AI Scientist v1 paper](https://arxiv.org/abs/2408.06292) Şablonlu öncü.
  Çinçe Çevirim:模板化前身──
- [Anthropic — Measuring AI agent autonomy](https://www.anthropic.com/research/measuring-agent-autonomy) Açık araştırma ajanlarının daha geniş bir çerçevesinde.
  Çinçe Çevirisi: Açık Araştırma Ajanın Daha Geniş Çerçeği
