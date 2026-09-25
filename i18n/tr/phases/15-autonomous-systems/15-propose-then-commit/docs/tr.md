# İnsan-da-da-da: Teklif-den sonra-yönlendirmek

> HITL konusunda 2026 yılındaki konsensüs spesifiktir. Bu "evlat soruyor, kullanıcı onay tıklıyor". değildir. Bu önerilen-sonra-yüzdür: önerilen eylem idempotency anahtarı ile dayanıklı bir depoya devam eder; niyet, veri soy, dokunan izinler, patlama radyüsü ve geri dönüş planı ile bir inceleyicinin önüne çıkarılır; sadece olumlu onaylandıktan sonra yapılır; yan etkinin gerçekleştiğini doğrultmak için uygulandıktan sonra doğrulanır. LangGraph'in `interrupt()`Ayrıca PostgreSQL kontrol noktası, Microsoft Agent Framework'ın `RequestInfoEvent`, ve Cloudflare'ın `waitForApproval()`Bu yöntemin en iyi yöntemleri ise, aynı şekil ile uygulanmasıdır. Kanonik başarısızlık modunda kauçuk damgası onaylaması bulunur: "Onurlandır?" üzerinde inceleme yapmadan tıklanır. Belli bir hafifleme açık bir kontrol listesi ile meydan okuma ve yanıtlama yapılır.

> **【中文解读】**2026 yıl HITL 共识是具体的──不是"Agent 问, user点击 Approve"──是提出-then-commit:提议动作以等键持久化至持久存储;审查员 presented意图、数据谱系、触及权、爆炸半径、回滚计划; sadece正面确认后提交;执行后验证确认副作用实际发生── LangGraph 的`interrupt()`Google'ın Microsoft Agent Framework'i oluşturan bir program.`RequestInfoEvent`Cloudflare'ın`waitForApproval()`Bu nedenle, bu durumun bir sonraki aşamasında, bir diğer sorunla karşı karşıya kalmak için, bir diğer sorunla karşı karşıya kalmak için, bir diğer sorunla karşı karşıya kalmak için, bir diğer sorunla karşı karşı karşıya kalmak için, bir diğer sorunla karşı karşı karşıya kalmak için, bir diğer sorunla karşı karşı karşıya kalmak için, bir diğer sorunla karşı karşı karşıya kalmak için, bir diğer sorunla karşı karşı karşıya kalmak için, bir diğer sorunla karşı karşı karşıya kalmak için, bir diğer sorunla karşı karşı karşıya kalmak için, bir diğer sorunla karşı karşı karşıya kalmak için, bir diğer sorunla karşı karşı karşıya kalmak için, bir başka sorunla karşı karşı karşıya kalmak için, bir başka bir sorunla karşı karşı karşıya kalmak için, bir çözüm olarak, bir çözüm olarak, bir çözüm olarak, bir çözüm olarak, bir çözüm olarak, bir çözüm olarak, bir çözüm olarak, bir çözüm olarak, bir çözüm olarak, bir çözüm olarak, bir çözüm olarak, bir çözüm olarak, bir çözüm olarak, bir çözüm olarak, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde,

> **【拓展：四个状态机步骤】**Önerilen-sonra-tümleşme yapılması Agent 产生动作,以等键持久化带意图/数据谱系/触及权限/爆炸半径/回滚计划;(2) 呈现审查者(人类,非 Agent 自审) 所有元数据;(3) 提交正面确认,动作执行;(4) 验证执行后回读副作用确认──这是数据库`RETURNING`- Ne? - Hayır.`PutObject`后 `GetObject`、Stripe/AWS API 等键模式在代理 审批上复用──

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, propose-then-commit state machine with idempotency) | **语言:** Python（标准库，带幂等的提议-提交状态机）
**Prerequisites:** Phase 15 · 12 (Durable execution), Phase 15 · 14 (Tripwires) | **前置知识:** Phase 15 · 12（持久执行），Phase 15 · 14（触发器）
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**学本节前 Lütfen önce bil:Fase 15·12(Durable Execution) Fase 15·14(Kill Switches) Fase 14·15(HITL Agent 模式)  本节是HITL'in工程化标准四步状态机。
>  **【类比】**Önerilen-sonra-Komit = "Banking大额转账审批"──普通 LLM 调用 = 即时转账(错了找客服);Önerilen-sonra-Komit = 提交转账申请(含收款人、金额、用途、回滚预案)→ 审查员看元数据 → 批准 → 执行 → 验证到账──每一步都不能省──这是人类计算机使用、Claude Code Plan Mode、Stripe API 等的键统一模式──
> ️ **【易错点】**"Tamam mı?" 弹窗被用户惯性点"是" → 皮章失效──修复:(1) 多选清单(每个动作独立确认);(2) 强制延迟(3秒倒计时);(3) 关键动作双确认(输入金额数字);(4) 显示"爆炸半径"(影响 N 个文件、M 个用户) ・・・

## Sorunlar. Sorunlar.

> **【中文解读】**Önceden önerilen ve sonra yapılan değişiklikler için öncelik verilmesi gerekir. Bu, bir insan veya sistem için bir önceki kontrol ve düzeltme fırsatı sağlayan bir 'düşünme' ve 'eğlenme' biçimidir.

> **【拓展：propose then commit】**Ön önerilen sonrası gönderme modeli, 2026 yılındaki kodlama ajanının standart güvenlik uygulamasıdır. Klavü Kodı 默认使用这种模式生成修改建议并等待用户确认. Git'in PR/MR mekanizması da bu modelin uygulanmasıdır.

Bir ajan bir eylem yapar. Kullanıcı karar vermek zorunda: onaylamak veya onaylamamak.

> Agent, eylem yapmalı. Kullanıcı, onaylanmalı veya onaylanmamalı.

Eğer karar yapılandırılmışsa, yavaş ama güvenilirdir. Mühendislik sorusu, yapılandırılmış bir incelemeyi en az direniş yoluyla nasıl yapacağımızdır.

> Eğer karar yapılandırılmışsa, yavaş ama güvenilirdir. Mühendislik sorusu yapılandırılmış incelemeyi en az engelleyici bir yol haline getirmektir.

2023 çağının HITL örneği eşzamanlı bir istekti: "Ajent Y  onaylı vücut ile X'ye e-posta göndermek istiyor mu?" Kullanıcı onayla tıklıyor. Herkes sistemin güvenli olduğunu düşünüyor.

> 2023 时代 HITL 模式是同步提示:"Agent göndermek için X,正文 Y批准?" kullanıcı tıklayın onaylıyor. Herkes hisseder sistem güvenliği.

> **【中文解读】**Bu bölümde AI Ajanının temel kavramı ve gerçekleştirme yöntemleri ele alınıyor. Ajan, çevreyi gözlemleyebilen, kararlar verebilen, eylemleri gerçekleştiren ve hedefleri gerçekleştirene kadar döngülenebilen LLM tarafından yönlendirilmiş bir otonom sistemdir.

2026 modeli  öner-sonra yapım  HITL'yi dayanıklı bir altyapıya taşıyor, yapılandırılmış metadatalar ekliyor ve pozitif yapım gerektiriyor.

> 2026 model propose-then-commit will HITL  transfer to持久基板上,附加结构化元数据,要求正面提交──

Her yönetilen ajan SDK bir sürüm gönderir: LangGraph `interrupt()`, Microsoft Agent Framework `RequestInfoEvent`, Cloudflare `waitForApproval()`API isimleri farklıdır, şekli değil.

> Her bir sorumlu ajan SDK`interrupt()`Microsoft Agent Framework`RequestInfoEvent`Cloudflare`waitForApproval()`△API 名称不同;形态不。

## Konsepten bir şey.

### O zaman teklif-eğitim devleti makinesi.

1. **Propose.**Agent, önerilen bir eylem üretir. Sürdürülebilir bir depoya (PostgreSQL, Redis, Durable Object) devam eder.
   Çeviri:**提议。**Agent 产生提议动作──持久化到持久存储(PostgreSQL、Redis、Durable Object)──包括:
   - Niyet (ajan neden bunu yapıyor)
     Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri
   - Veriler soyundan (bu önermeye hangi kaynak yol açtı)
     Çinçe Çevirimiçi:数据谱系
   - dokunan izinler (ne alanlar / dosyalar / son noktalar)
     Çinçe Çevirimiçi:触及的权限 (哪些范围/文件/端点)
   - patlama radyüsü (en kötü durum nedir)
     Çinçe Çevirisi: Explosion halfway (En kötü durum nedir)
   - Geri dönüş planı (eğer yapılmışsa, nasıl geri çeviriyoruz)
     Çönüştürme planı (Roll Plan)
   - İdepotans anahtarı (tekrar bir önerme; yeniden gönderme aynı kayıtları gönderir)
     Çeviri: 等键 (→ Çeviri: 等键)
2. **Surface.**Eleştirmen, teklifi tüm metadata ile görüyor. Eleştirmen bir insandır (öntemsel eleştiren değil).
   Çeviri:**呈现。**审查者看到带所有元数据的提议──审查者是个人──不是代理自审──
3. **Commit.**- İstihbarat onaylandı.
   Çeviri:**提交。**Doğrudan onaylanmak.
4. **Verify.**İptal sonrasında yan etki tekrar okunuyor ve onaylanıyor. Eğer doğrulama adımı başarısız olursa, sistem bilinen kötü bir durumdadır ve uyarı etkinleştirir.
   Çeviri:**验证。**执行后副作用被回读确认──如果验证步骤失败,系统处于已知坏状态并启动警报── 执行后副作用被回读确认──如果验证步骤失败,系统处于已知坏状态并启动警报──

### İdempotency anahtarı.

İdempotency anahtarı olmadan geçici bir başarısızlıktan sonra yeniden deneme onaylanmış bir eylemin iki katına çıkabilir.

> 没有等键,瞬态失败后的重试可能双倍执行已批准动作──

Konkrete bir örnek: kullanıcı "A'dan B'ye 100 dolar aktar"a onay verir. Ağ blipleri. İş akışı tekrar dener. Kullanıcı bir kez onaylamış ancak aktarım iki kez yürütülür. İdempotency anahtarı onayı tek, benzersiz bir yan etkiye bağlar; ikinci yürütme bir işlemizdir.

> 具体例:用户批准"A 转 $100到B"――网络闪断――工作流重试――用户批准一次但转账执行两次――等键将批准绑定到单一唯一副作用;第二次执行是无-op――

Bu aynı idempotency örneği Stripe ve AWS API'ler kullanır. Ajan onayları için tekrar kullanmak Microsoft Ajan Çerçeve belgeleri açıkça belirtilmiştir.

> Bu Stripe ve AWS API kullanımı aynı  modeldir. Microsoft Agent Framework'ı kullanmak için kullanılır.

### Süreklilik: neden onaylar süreçten daha uzun sürer ?

Onaylama bekleme odası, ajanın sahip olmadığı bir durum parçasıdır. İş akışı durur (Denevi 12). Onaylama geldiğinde, iş akışı tam olarak o noktadan yeniden başlar. Bu nedenle LangGraph çiftleşir `interrupt()`PostgreSQL kontrol noktası ile ve sadece hafıza durumu değil  bir onay iki gün sonra hala iş akışı sağlam bulur.

> 批准等候室是 Agent 不拥有一片状态──工作流暂停──第 12 课)──批准到来时,工作流从该精确点恢复──这就是为什么LangGraph将`interrupt()`PostgreSQL'in kontrol noktası sadece kayda konumu değil, iki gün sonra onaylanmıştır.

### Kağız damgası onayları ve meydan okuma ve yanıt azaltma.

HITL için varsayılan kullanıcı arayüzü ("Onaylayın" / "Refut" düğmeleri) gerçek bir inceleme olmadan hızlı onaylar üretir. Belli hafifleme: Onaylayın düğmesi etkinleştirilmeden önce belirli sorulara olumlu cevaplar gerektiren bir meydan okuma ve yanıt kontrol listesi.

> HITL 默认 UI("Tamam"/"Redeg" 按)产生快速批准无真实审查──已记录缓解:在 批准按启动前要求对特定问题正面回答的挑战-响应清单──具体形状:

- "Bu ne kaynakla ilgili olduğunu anlıyor musun?"
  Çinçe Çevirimi: "You了解这触及什么资源吗? [ ]"
- "Patlama radyüsünün kabul edilebilir olduğunu doğruladın mı?"
  Çin Çeviri: "You验证了爆炸半径可接受吗?"
- "Bu başarısız olursa geri dönüş planınız var mı?
  Çinçe Çevirim: "If Fail Do You Have a Backroll Plan?

Bu, birincil olarak bir işverenin bir diğer işverenin yaptığı bir çalışma olarak görülür. Bu çalışma, birincil olarak bir işlev olarak kullanılır.

> Bu, bir işçi tarafından onaylanmış bir sistem olarak kullanılır. Bu, bir işçi tarafından onaylanmış bir sistem olarak kullanılır.

### Sonuç olarak neyin önemli olduğu neyin sonuçları neyin önemli olduğu

Her eylemde önerilen ve sonra yapılan bir şey gerekmez.

> Bu, her hareket için bir teklif ve bir karar vermeye gereklidir.

- **Consequential actions**(her zaman HITL): geri dönüşü olmayan yazılar, finansal işlemler, dışa giden iletişim, üretim veritabanı değişiklikleri, yıkıcı dosya sistemleri operasyonları.
  Çeviri:**后果性动作**(总 HITL):不可逆写、金融交易、外发通信、生产数据库变更、破坏性文件系统操作──
- **Reversible actions**(bazen HITL): yerel dosyalara düzenlemeler, aşamalama-env değişiklikleri, net bir geri dönüş ile geri dönüşlü yazılar.
  Çeviri:**可逆动作**(Sometimes HITL):本地文件编辑、舞台化 环境变更、带清晰回滚的可逆写──
- **Reads and inspections**(never HITL): bir dosyayı okumak, kaynakları listelenmek, sadece okuma API'yi arama.
  Çeviri:**读和检查**(從不HITL):读文件、列资源、调用只读API。

### İşten sonra doğrulama.

"Commit ran" " yan etkisi oldu" ile aynı değildir. Ağ partisyonu ve yarış koşulları, arka uç devam etmeden başarılı olduğunu düşünen bir iş akışı oluşturabilir. Verify adımı, onaylama için commit edildikten sonra hedef kaynağı yeniden okuyor. Bu, veri tabanı işlemleri ile aynı kalıptır `RETURNING`Sözleşmeler veya AWS `GetObject`Sonra .`PutObject`- Evet .

> "Soruşturma işlemi" "Kısayollar meydana gelmiştir" gibi değildir.`RETURNING`Sözcükler ve veri tabanı`PutObject`后 `GetObject`AWS'in benzer bir modülü.

### AB AI Yasası Madde 14.

14. madde, AB'deki yüksek riskli Yapay zeka sistemleri için etkili insan denetimi zorunluyor. "Etkili" dekoratif değildir. Yönetim dili özellikle kauçuk damga desenlerini dışlıyor.

> Bölüm 14 条 Zorla AB Yüksek Riskli AI  Sisteminin geçerli insan denetimi 有效 dekoratif değildir  监管语言明确排除皮章模式──带挑战-响应的提案-then-commit is in Microsoft Agent Governance Toolkit 合规文档中通过第 14 条审查的形态──

## Çerçeveyi kullanın.
```figure
mx-propose-then-commit
```

## Kullan

`code/main.py`Stdlib Python'da bir önerme-sonra-yaptırma durum makinesi uyguluyor. Durable store bir JSON dosyası. Idempotency anahtarı bir hash (thread_id, action_signature) dir. Sürücü üç vaka simüle eder: temiz onay akışı, geçici başarısızlıktan sonra yeniden deneme (iki kat çalıştırılamaz) ve bir kağız damgası varsayılan karşı bir meydan okuma ve yanıt akışı.

> `code/main.py`Python standart kütüphanesi 实现 propose-then-commit 状态机──持久存储是 JSON 文件──等键是 (thread_id, action_signature) 的哈希──驱动器模拟三例:干净批准流、瞬态失败后重试(必须不双执行)

## İndirin . Ürünler .

`outputs/skill-hitl-design.md`önerilen HITL iş akışını gözden geçirir. Bu durumda, metadata eksikliği, idempotency, verifikasyon veya meydan okuma ve yanıt katmanları için önerilen ve işlenilen biçim ve işaretler.

> `outputs/skill-hitl-design.md`审查提议 HITL 工作流的提案-然后-commit 形态并标记缺失的元数据、等、验证或挑战-响应层──

## Egzersizler.

1. Çık .`code/main.py`- Onaylanmış bir önerinin yeniden deneme süresi, dayanıklı kayıt kullanıldığını ve tekrar yürütülmediğini onaylayın.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`code/main.py`❖ onaylanmış önerinin tekrar kullanımı onaylanmıştır.

2. Teklif kayıtlarını bir  ile uzatmak`rollback`Verification adımının başarısız olduğu bir işlem simülasyonu yapın.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`rollback`字段扩展提议记录──模拟验证步骤失败的执行──展示回滚自动触发──

3. Microsoft Agent Framework'ı okuyun `RequestInfoEvent`Bir metadata alanı belirleyin. API'de oyuncak motoru eksik olduğunu belirtir.
   Çeviri: Microsoft Agent Framework'ı okuyun`RequestInfoEvent`文档──识别 API 包含而玩具引擎缺失的一个元数据字段──添加它并解释它防止什么──

4. Bir belirli eylem için bir meydan okuma ve yanıt kontrol listesini oluşturun (örneğin "ağcı bir Twitter hesabına gönderin").
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri Çeviri: Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Ç Ç Çeviri Çeviri Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç

5. "Tamamlayın" diye bir çağrılı sorunun yeterli olabileceği bir durum seçin (kalıcı bir depo gerekmez). Nedenini açıklayın ve kabul ettiğiniz risk sınıfını isimlendirin.
   Çinçe Çevirimi: seçme bir eşzamanlı "Onla" ipucu.

## Anahtar Şartlar .

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| Propose-then-commit | "Two-phase approval" | Persisted proposal + positive commit + verify |
| Propose-then-commit | "两阶段批准" | 持久提议 + 正面提交 + 验证 |
| Idempotency key | "Retry-safe token" | Unique per proposal; second execution no-ops |
| 幂等键 | "重试安全 token" | 每提议唯一；第二次执行 no-op |
| Data lineage | "Where it came from" | The specific source content that led to the proposal |
| 数据谱系 | "它从哪来" | 导致提议的特定源内容 |
| Blast radius | "Worst case" | Scope of effect if the action goes wrong |
| 爆炸半径 | "最坏情况" | 动作出错时的影响范围 |
| Rubber-stamp | "Fast approval" | "Approve" clicked without genuine review |
| 橡皮章 | "快速批准" | 无真实审查地点击"Approve" |
| Challenge-and-response | "Forcing checklist" | Reviewer must positively acknowledge specific questions |
| 挑战-响应 | "强制清单" | 审查者必须正面确认特定问题 |
| RequestInfoEvent | "MS Agent Framework primitive" | Durable HITL request with structured metadata |
| RequestInfoEvent | "MS Agent Framework 原语" | 带结构化元数据的持久 HITL 请求 |
| `interrupt()` / `waitForApproval()` | "Framework primitives" | LangGraph / Cloudflare equivalents of the same shape |
| `interrupt()` / `waitForApproval()` | "框架原语" | 相同形态的 LangGraph / Cloudflare 等价物 |

## Daha fazla okumak

- [Microsoft Agent Framework — Human in the loop](https://learn.microsoft.com/en-us/agent-framework/workflows/human-in-the-loop) `RequestInfoEvent`, kalıcı onaylar.
  Çeviri:`RequestInfoEvent`Uzun süre onaylanmıştır.
- [Cloudflare Agents — Human in the loop](https://developers.cloudflare.com/agents/concepts/human-in-the-loop/) `waitForApproval()`Ve Kalıcı Nesneler.
  Çeviri:`waitForApproval()`和 Dayanıklı Nesneler
- [Anthropic — Measuring agent autonomy in practice](https://www.anthropic.com/research/measuring-agent-autonomy) HITL uzun vadede riskin azaltılması olarak.
  Çeviri: HITL 作为长程风险缓解.
- [EU AI Act — Article 14: Human oversight](https://artificialintelligenceact.eu/article/14/) Yüksek riskli sistemler için düzenleyici bir temel.
  Çinçe Çevirisi:高风险系统的监管基线──
- [Anthropic — Claude's Constitution (January 2026)](https://www.anthropic.com/news/claudes-constitution) denetim ile ilgili anayasa çerçevesini oluşturmak.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri
