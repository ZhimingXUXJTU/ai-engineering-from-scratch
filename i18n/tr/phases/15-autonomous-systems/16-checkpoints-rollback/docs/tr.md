# Kontrol noktaları ve geri dönüş.

> Her grafik-devlet geçişi devam ediyor. Bir işçi kaza yaparsa, kira sözleşmesi geçerli olur ve son kontrol noktasında başka bir işçi onu alır. Cloudflare Durable Objects saatler veya haftalar boyunca durumunu korur. Teklif-sonra-tümlenme (Disim 15) her eylem için bir gerileme planı tanımlar. Eylem sonrası doğrulama döngüyü kapatır. AB AI Yasası'nın 14. maddesi yüksek riskli sistemler için etkili insan denetimini zorunlu kılıyor  bu, pratikte kontrol noktalarının sorgulanabilir olması, geri dönüşlerin prova edilmesi ve denetim yolunun bir dağıtımdan geçmesi gerektiği anlamına geliyor. Keskin bir başarısızlık modusu: İdempotency anahtarları ve ön koşul kontrolleri olmadan geçici bir başarısızlıktan sonra yeniden deneme, zaten onaylanmış bir eylemin iki katına çıkabilir. İşten sonra doğrulama onu yakalar.

> **【中文解读】**Her bir grafik durumu dönüşüm sürimleşme, çalışan  çöküntüde kiralama süresi, diğer çalışan yeni kontrol noktası alıyor  Cloudflare Durable Objects 跨数小时或数周持有状态;; Önerilen-den sonra-verilen;; 15 课) her hareketi tanımlayan geri dönüş planı için  Hareketi sonrası denetim kapalı döngü.

> **【拓展：幂等+前置条件+验证+回滚四件套】**仅等不够:考虑"当余额 > $1000 时从 A 转 $100 B'ye kadar onaylı hareketler. Başlatılmaktadır. Başlatılmaktadır. Başlatılmaktadır. Başlatılmaktadır. Başlatılmaktadır.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, checkpoint and rollback state machine) | **语言:** Python（标准库，检查点和回滚状态机）
**Prerequisites:** Phase 15 · 12 (Durable execution), Phase 15 · 15 (Propose-then-commit) | **前置知识:** Phase 15 · 12（持久执行），Phase 15 · 15（propose-then-commit）
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetleme: Özetlemelemeleme: Özetlemelemelemeleme: Özetlemelemeleme
>  **【类比】**检查点回滚 = "games的档案与读档"──检查点 = 自动档(每次一关存一次);回滚 = 读档(这关打错了回到上一关)──后果性动作四件套 = 等键(防止重启双重执行) + 前置条件(重启后世界状态仍符合预期) + 动作后验证(确认真实副作用发生) + 失败回滚(恢复到动作前)──
> ️ **【易错点】**Tekrar başlatma süreci, diğer süreçler tarafından değiştirilmiştir.

## Sorunlar. Sorunlar.

> **【中文解读】**Kontrol noktası ve dönüşüm mekanizması, Ajanın, işlem sürecinde durumunu kaydetmesini, hatalı zamanın önceki iyi duruma geri dönmesini sağlar. Bu, veritabanı iş ve Git'in sürüm kontrolüne benzer. Kontrol noktası anahtar noktalar tutmaktadır.

> **【拓展：checkpoints rollback】**检查点-回滚是可靠的代理 系统的基础设施――实现选择:(1) 文件系统级使用 Git 或快照保存文件状态;(2) 数据库级使用事务保证数据一致性;(3) 应用级Agent自我管理检查点((如LangGraph) ――关键权衡是检查点粒度太细会增加开销,太粗会丢失更多工作──

Sürekli uygulanma (Deneyim 12) bir kaza ajanı yeniden başlatabilir hale getirir.

> 持久执行 (第 12 课) 使崩 Agent 可恢复──Propose-then-commit (İş önerme) 第 15 课) 使批准动作可审计──

Bu ders onlara katılır: onaylanmış bir eylem kısmen yürürlüğe girdiğinde, çöktüğünde ve tekrar başladığında ne olur?

> Bu ders bunlarla bağlantılı: Ratification Motion Section Execution  Crash  Restore sırasında ne olur?

Gerçek sistemler bunu farklı şekilde gösterir:

> Gerçek sistem bağlantısı farklı:

> **【中文解读】**Bu bölümde AI Ajanının temel kavramı ve gerçekleştirme yöntemleri ele alınıyor. Ajan, çevreyi gözlemleyebilen, kararlar verebilen, eylemleri gerçekleştiren ve hedefleri gerçekleştirene kadar döngülenebilen LLM tarafından yönlendirilmiş bir otonom sistemdir.

- **LangGraph**PostgreSQL'e yapılan her grafik durumu geçişini kontrol noktaları kontrol eder. İşçi çöktüğünde, kira sözleşmesi serbest bırakılır ve bir diğer işçi en son kontrol noktasında yeniden başlar. İş akışları duraklama yapar.`interrupt()`, ki bu da devam ediyor.
  Çeviri:**LangGraph**Bu durumdan sonra, her bir işçi, bir işçiye bir işçi bırakmak için bir işçiye bir işçiye bir işçiye bir işçiye bir işçiye bir işçiye bir işçiye bir işçiye bir işçiye bir işçiye bir işçiye bir işçiye bir işçiye bir işçiye bir işçiye bir işçiye bir işçiye bir işçiye bir işçiye bir işçiye bir işçiye bir işçiye bir işçiye bir işçiye bir işçiye bir işçiye bir işçiye bir işçiye bir işçiye bir işçiye bir işçiye dönüştürmek için bir işçiye dönüştürmek için bir işçiye dönüştürmek için bir işçiye dönüştürmek için bir işçiye dönüştürmek için bir işçiye dönüştürmek için bir işçiye dönüştürmek için bir işçiye dönüştürmek için bir işçiye dönüştürmek için bir işçiye dönüştürmek için bir işçiye dönüştürmek için bir işçiye dönüştürmek için bir işçiye dönüştür.`interrupt()`Ünce durur, kendi kendine devam eder.
- **Cloudflare Durable Objects**Saatler veya haftalar boyunca anahtar durumunu tutun. Bilgisayarı onaylanmış eylem için depolama ile birlikte yerleştirin.
  Çeviri:**Cloudflare Durable Objects**跨数小时或数周持有每键状态──将计算与批准动作的存储同址──
- **Microsoft Agent Framework**Açıklamalar`Checkpoint`iş akışı API'sinde primitifler; tekrarlama artı idempotency tekrar denemeleri kapsar.
  Çeviri:**Microsoft Agent Framework**Çalışmalar akış API'sinde ortaya çıkış`Checkpoint`Çıktı. Çıktı.

Her durumda, gerçekten işe yarayan kombinasyon: idempotency anahtarı + ön koşul kontrolü + eylem sonrası doğrulama + doğrulama başarısızlığı üzerine geri dönüştürülmesidir.

> Her durumda gerçekçi etkili bir yapılandırma: 等键 + 前置条件检查 + 动作后验证 + 验证失败时回滚──

## Konsepten bir şey.

### Her geçiş devam ediyor. Her dönüşüm kalıcılaşıyor.

Grafik-devlet geçimi, iş akışını bir isimli devletteki diğerine taşıyan herhangi bir adımdır. Saçma uygulamalar sadece belirli görev noktalarında kalır; üretim uygulamalar her geçişte kalır. Maliyet (bazı ekstra yazılar) güvenilirlik kazancı ile görece küçüktür (replay herhangi bir yerde yer alır, kiralama kurtarımı doğru olur).

> 图状态转换是将工作流从一个命名状态转移到另一个命名状态的任何步骤──简单实现只在特定提交点持久化;生产实现持久化每转换──成本几次额外写) 对于可靠性收益(重放落在任何地方、租约恢复精确) 小──

### Kiralama yeniden kazanım

Bir işçi kaza olduğunda, iş akışı kaybolmaz; kiralama (bu işçinin bu çalışmayı gerçekleştirdiğini kısa süredir iddia eden) sadece sona erer. Bir başka işçi en son kontrol noktasını alır ve yeniden başlar. Kiralama mekanizması üretim sistemlerinin uçuşta çalışmalarını kaybetmeden süren yerleşimlerde hayatta kalmasına izin verir.

> işçi 崩时工作流不丢失;租约(Bu işçi bu işlevi gerçekleştirmekte) sadece geçici açıklama.

### İdempotency ve ön koşullar.

Sadece idempotency yeterli değildir.$100 from A to B when balance > $1000. " İş akışı yapılır, çalıştırma ortasında çöker ve devam eder. Eğer idempotency anahtarı kontrol edilirse ve çalıştırma devam ederse, transfer bir kez çalışır (tam). Ancak çökme ve devam arasında A'nın bakiyesinin farklı bir iş akışı aracılığıyla 500 dolara düştüğünü düşünün. Idempotency kontrolü hala geçer; ön koşul değil. Ön koşul kontrolü olmadan, bir ödemek göndeririz.

> 仅等不够――考虑: 工作流被批准"当余额 > $1000 时从 A 转 $100 B'¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬

Her sonuçlı eylem her iki şeye de ihtiyaç duyar:

> Her sonucun iki yönü vardır:

- **Idempotency key**: ikili işlenmeyi önler.
  Çeviri:**幂等键**: iki katı gerçekleştirmeyi önlemek
- **Precondition check**: devletin hala onaylananlara uygun olduğunu doğruluyor.
  Çeviri:**前置条件检查**• onay durumunun onayla aynı olması

### İşten sonra doğrulama.

"Yalnızca 200'e geri döndürülmüş" doğrulama değildir. Gerçek doğrulama hedefi yeniden okuyor ve yan etkisi gerçekte meydana geldiğini doğruluyor.

> "工具返回 200" değil test edilmiştir.

- Veritabanı güncelleştir: `UPDATE ... RETURNING *`Sonra geri gönderilen satır eşleşmelerinin istenen durumunu belirtir.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`UPDATE ... RETURNING *`Sonra da geri dönüp beklenmiş durumuna uyum sağlayacağını söyledi.
- E-posta gönderme: gönderilen mesaj kimliği için gönderilen klasörü kontrol edin.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri
- Dosya yazma: dosyayı tekrar oku ve hash et.
  Çin Çeviri: PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, PDF, da da da da da da da da da da da da da da da da da da da da da da da da da da da da da da da da da da
- API çağrısı: takip `GET`hedef kaynağı.
  Çeviri: API 调用:对目标资源的后续`GET`- Evet.

Eğer doğrulama başarısız olursa, iş akışı bilinen kötü bir durumdadır.

> 验证失败时工作流已知坏状态──回滚启动──

### Geri dönüş planları . Geri dönüş planları .

Teklif sonra görev (Desin 15) her sonuçta bir geri dönüş planı vardır.

> Önerilen-sonra-yürüttük (第 15 课) 中每个后果性动作带回滚计划──类型:

- **In-band rollback**: yan etkisini doğrudan tersine çevir (`DELETE`Sonra .`INSERT`- Evet .`Send-correction-email`gönderildikten sonra).
  Çeviri:**带内回滚**: doğrudan karşı karşı yan etkileri`INSERT`后 `DELETE`、发送后发送更正邮件) ⋅
- **Compensating transaction**: orijinalini (standart SAGA modelini) nötralize eden yeni bir eylem.
  Çeviri:**补偿事务**Bu nedenle, bu durumun bir sonraki döneminde de, bir sonraki döneminde de, bir sonraki döneminde de, bir sonraki dönemlerde de, bir sonraki dönemlerde de, bir sonraki dönemlerde de, bir sonraki dönemlerde de, bir sonraki dönemlerde de, bir sonraki dönemlerde de, bir sonraki dönemlerde de, bir sonraki dönemlerde de, bir sonraki dönemlerde de, bir sonraki dönemlerde de, bir sonraki dönemlerde de, bir sonraki dönemlerde de, bir sonraki dönemlerde de, bir sonraki dönemlerde de, bir sonraki dönemlerde de, bir sonraki dönemlerde de, bir sonraki dönemlerde de, bir sonraki dönemlerde de, bir sonraki dönemlerde, bir başka bir dönemlerde, bir başka bir dönemlerde, bir dönemlerde, bir dönemlerde, bir dönemlerde, bir dönem, bir dönem, bir dönem, bir dönem, bir dönem, bir dönem, bir dönem, bir dönem, bir dönem, bir dönem, bir dönem, bir dönem, bir dönem, bir dönem, bir dönem, bir dönem, bir dönem, bir dönem, bir dönem, bir dönem, bir dönem, bir dönem, bir dönem, bir dönem, bir dönem, bir dönem, bir dönem, bir dönem, bir dönem, bir dönem, bir dönem, bir dönem, bir dönem, bir dönem, bir dönem, bir dönem, bir dönem, bir dönem, bir dönem, bir dönem, bir dönem, bir dönem, bir dönem, bir dönem, bir dönem, bir dönem, bir dönem, bir dönem, bir dönem, bir dönem, bir döner, bir döner, bir döner, bir döneme, bir döneme, bir döneme, bir döneme, bir döneme, bir döneme, bir döneme, bir döneme, bir döneme, bir döneme, bir döneme, bir döneme, bir döneme, bir döneme, bir döneme, bir döneme, bir döneme, bir döneme, bir döneme, bir döneme, bir döneme, bir döneme, bir döneme, bir döneme, bir döneme, bir döneme, bir döneme, bir döneme, bir döneme, bir döneme, bir döneme, bir döneme, bir döneme, bir döneme, bir döneme, bir döneme, bir döneme, bir döneme, bir döneme, bir döneme, bir döneme, bir döneme, bir döneme, bir döneme, bir döneme, bir döneme, bir döneme
- **Out-of-band rollback**İnsanı uyar, iş akışını durdur, kötü durumu araştırmaya bırak.
  Çeviri:**带外回滚**İnsanları uyarmak, çalışma akışını durdurmak, araştırmak için kötü bir durum bırakmak.

Bu konuda bir değişiklik yapılması gerekmektedir. "Bu durumu geri çeviremeyiz" ("bu durumu geri çeviremeyiz") öneride belirtilmelidir.

> No-op 回滚("我们不能撤销此") ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒  ⇒ ⇒ ⇒  ⇒ ⇒ ⇒    ⇒ ⇒ ⇒    ⇒      ⇒        ⇒                                                                                                                                                                                   

### AB AI Yasası Madde 14 İşletme Okunuşu

Madde 14 yüksek riskli sistemler için "verimli insan denetimi" gerektirir.

> 第 14 条要求高风险系统的有效人类监督"──运营术语中,实现者读为:

- Kontrol noktaları bir denetçi tarafından sorulabilir.
  Çinçe Çevirim: Çekşemek noktası
- Rollback'ler prova edilir (en az bir kez sonundan sona test edilir).
  Çinçe Çevirim: 回滚演练
- Denetim izleri bir dağıtımdan geçiyor (checkpoint backend geçici değildir).
  Çinçe Çevirimiçi: 审计追踪跨部署存活(检查点后端非临时)
- Başarısız doğrulamalar uyarılır, sessiz olarak kaydedilmez.
  Çinçe Çevirimiçi:失败验证被警报而非静默记录──

Verify + rollback yolu olmadan görev sırasında çökmüş, yan etkeni yeniden başlatan ve tamamlayan bir iş akışı, Madde 14 testi boyunca hayatta kalmaz.

> 提交中崩、恢复、无验证+回滚路完成副作用工作流不通过第 14 条测试──

### Keskin başarısızlık modusu: iki kat idareci

Bu alanda en yaygın üretim olayı: Eylem onaylandı, commit başlandı, geri döndü 200, çalışma akışı durmadan çöktü, devam etti ve tekrar yürütüldü.

> Bu alanda en yaygın üretim kazaları:动作批准、提交开始、返回 200、工作流在持久化状态前崩、恢复并重新执行──

1. Hareket onaylandı, idempotency key k.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri
2. Başlatma, yürütme, 200'e geri dönüş.
   Çeviri: başlatmak, yürütmek, geri dönmek
3. İş akışı "altınlık" durumunu sürdürmeden önce çöküyor.
   Çinçe Çevirimiçi:工作流在持久化 "已提交"状态前崩──
4. İş akışı devam eder; "önlendirildi ama commit edilmedi" görür; yeniden yürütülür.
   Çin Çeviri:工作流恢复; see "批准但未提交";重新执行──
5. Yan etkisi iki kez ateş eder.
   Çinçe Çevirisi: Yanlışı 触发两次.

Yumuşatma: yürütmeden önce "uçuşta" bir niyeti sürdürün, idempotency anahtarıyla yürütün, sonra "yürüttük" işaretini sadece eylem sonrası doğrulama başarısız olduğunda işaretleyin. Eylem ateşleri ve durum yazısı başarısız olursa, doğrulama ve (gerekirse) yeniden ateş etmeyi biliyorsunuz. Eğer durum yazısı başarılı olursa ve eylem başarısız olursa, kurtarma yolu üzerinden tam olarak bir kez doğrulayıp ateş edersiniz.

> 缓解:执行前持久化"in-flight"意图, 等键で执行, 只有在动作后验证成功后标记"已提交"──如动作触发而状态写失败,你知道要验证(如必要) 重触发──如状态写成功而动作失败,你验证并通过恢复路径精确触发一次──

## Çerçeveyi kullanın.
```figure
checkpoint-replay
```

## Kullan

`code/main.py`Sürücü dört senaryoyu simüle eder: temiz çalışmak, kaza sonrası yeniden denemek (idempotency catch), ön koşul başarısızlığı (iş akışı ateşlemeden düşürülür), başarısızlığı doğrulayın (rollback fire).

> `code/main.py`实现带等、前置条件、验证和回滚的检查点工作流──驱动器模拟四场景:干净运行、崩后重试(等捕获)、前置条件失败(工作流停止不触发)、验证失败(回滚触发)。

## İndirin . Ürünler .

`outputs/skill-rollback-rehearsal.md`önerilen bir iş akışı için bir geri dönüş prova testi tasarlar ve denetim yolunun devamlılığı için kontrol noktasının arka planını denetler.

> `outputs/skill-rollback-rehearsal.md`Önerilen çalışma akışı tasarımı geri dönüşü, deneme ve denetim kontrol noktasının son taraftan denetim takip süresi.

## Egzersizler.

1. Çık .`code/main.py`Dört senaryoyu kontrol edin, kaza sırasında olayda, tekrar denemeler sırasında bir kez ateş açıldığını doğrulayın.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`code/main.py`❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖  ❖ ❖ ❖    ❖                                                                                          

2. "İlk önce işlendiği gibi işaretle, sonra yap" örneğini değiştirin, böylece durum hareketi sonrasında ateşler yazır. Çarpışma senaryosunu tekrarlayın. Ne kadar ikili hareketi ateşlediğini ölçün.
   Çinçe Çevirimi: Modify "先标记完成再做" mode使状态写在动作后触发──重跑崩场景──测量多少重动作触发──

3. Özel bir üretim eyleminin (örneğin "Slack kanalına gönderme") bir geri dönüş planı tasarlayın.
   Çinçe Çevirimiçi: "Slack 频道" için özel bir üretim hareketi için.

4. Bildiğiniz bir iş akışı alın. Her durum geçimini belirleyin. Her birini dayanıklılık gereksinimleri ile işaretleyin (durdurmak / devam etmemek). Şu anda devam etmemekte olduğunuzları sayın.
   Çinçe çevirisi: Get a You Know Job flow。识别每个状态转换──标记各的持久性要求(持久化/不持久化)──计数你当前不持久化的──

5. Tekrar tekrarlı geri dönüş testi: gerçek bir iş akışı çalıştırmak, bozulmak ve geri dönüş yolunun ateşini doğrulayan bir uçtan sona test tasarlayın.
   Çinçe Çevirim:演练回滚测试:设计端到端测试运行真实工作流、崩、确认回滚路径触发──测试断言什么?

## Anahtar Şartlar .

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| Checkpoint | "Save point" | Every graph-state transition persists to a durable store |
| 检查点 | "保存点" | 每个图状态转换持久化到持久存储 |
| Lease | "Worker claim" | Short-lived claim that a worker is executing a run; expires on crash |
| 租约 | "Worker 声明" | worker 正在执行运行的短暂声明；崩溃时过期 |
| Precondition | "State gate" | Assertion that the state is still consistent with the approved action |
| 前置条件 | "状态门" | 状态仍与批准动作一致的断言 |
| Post-action verify | "Re-read check" | Confirm the side effect actually happened in the target system |
| 动作后验证 | "回读检查" | 确认副作用在目标系统中实际发生 |
| In-band rollback | "Direct undo" | Reverse the side effect with the inverse operation |
| 带内回滚 | "直接撤销" | 用逆操作反转副作用 |
| Compensating transaction | "SAGA undo" | A new action that neutralizes the original |
| 补偿事务 | "SAGA 撤销" | 抵消原始动作的新动作 |
| Mark-as-done-first | "Status write order" | Persist the committed status before returning from commit |
| 先标记完成 | "状态写顺序" | 从提交返回前持久化已提交状态 |
| Article 14 | "EU AI Act human oversight" | Operational: queryable checkpoints, rehearsed rollbacks, auditable trail |
| 第 14 条 | "EU AI 法案人类监督" | 运营：可查询检查点、演练回滚、可审计追踪 |

## Daha fazla okumak

- [Microsoft Agent Framework — Checkpointing and HITL](https://learn.microsoft.com/en-us/agent-framework/workflows/human-in-the-loop) Kontrol noktaları ve kiralama geri kazanımı.
  Çinçe Çevirisi:检查点原语和租约恢复。
- [Cloudflare Agents — Human in the loop](https://developers.cloudflare.com/agents/concepts/human-in-the-loop/) Durumlu nesneler bir devlet altyapısı olarak.
  中文翻译:Durable Objects 作为状态基板──
- [EU AI Act — Article 14: Human oversight](https://artificialintelligenceact.eu/article/14/) düzenleyici başlangıç.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri
- [Anthropic — Measuring agent autonomy in practice](https://www.anthropic.com/research/measuring-agent-autonomy) Uzun vadede iş akışları için güvenilirlik çerçevesini oluşturmak.
  Çinçe Çevirisi:长程工作流的可靠性框架──
- [Anthropic — Claude Code Agent SDK: agent loop](https://code.claude.com/docs/en/agent-sdk/agent-loop) Claude Code Routines için iş akışı şekli.
  Çeviri:Cloyd Code Routines'ın çalışma akışı biçimi
