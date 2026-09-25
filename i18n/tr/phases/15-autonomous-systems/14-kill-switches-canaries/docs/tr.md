# Çıkartıcıları, devreler kesici ve Kanarya işaretlerini öldür.

> Bir kill switch, ajanın düzenleme yüzeyinin dışında tutulan bir boolean  bir Redis anahtarı, bir özellik bayrağı, imzalanmış bir yapılandırma  aracı tamamen devre dışı bırakır. Bir devrim kesici daha ince bir biçimdir: belirli bir örneğe (bir sırada beş aynı araç çağrısı) çarpır, saldırgan yolu durdurur ve bir insana kadar tırmanır. Bir kanary token klasik aldatmaca miras alınır: bir ajanın dokunmak için yasal bir nedeni olmayan sahte bir kimlik veya balık kayıtları, erişimi uyarıyı tetikler. eBPF tabanlı veri yolları (örneğin: Cilium) karantinalı bir kapsülün çıkışını çekirdek katmanındaki bir adli tıbbi balıkçıya yeniden yazabilir; yayınlanan Cilium referansları yük altında sub-millisecond P99 veri yolu gecikmesini rapor eder (gelişme bütçeniz, bir politika güncelleme nodu nasıl ulaştığına bağlıdır, veri yolu kendisi değil). Hareketli bir temel çizgiye uyum sağlayan istatistik algılayıcılar (EWMA, CUSUM) sessizce hareket etmesini kabul eder  onları eğilmeyen sert anayasa sınırları ile katlar.

> **【中文解读】**终止开关是位于代理 编辑面之外的布尔值Redis 键、功能标志、签名配置完全禁用 Agent。断路器更细粒度:在特定模式跳(连续五次相同工具调用),暂停违规路径并升级到人类。金雀 token 继承经典欺骗:Agent 无合法理由触及假凭证或蜜记录,其访问触发警报──基于 eBPF的数据路径 (例如) 内核出口的重写将分离 pod into取证;公开

> **【拓展：三层不信任架构】**Üç testerçeler tamamen güvenmez Agent 自報告:终止开关外置(Agent 不能编辑) 断路器模式匹配(不看 Agent 意图) 金丝雀 temel olarak "不应触及" prensibi(访问即警报)  İstatistik testerçeler(EWMA/CUSUM) 适应漂移但会被耐心攻击者缓慢移动基线绕过;硬宪法限制("永不发邮件给秘密@")简单、可审计、不可博──分层:

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, three-detector simulator: kill switch, circuit breaker, canary) | **语言:** Python（标准库，三检测器模拟器：终止开关、断路器、金丝雀）
**Prerequisites:** Phase 15 · 13 (Cost governors), Phase 15 · 10 (Permission modes) | **前置知识:** Phase 15 · 13（成本治理器），Phase 15 · 10（权限模式）
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**Önemli bir şekilde, bu konuda bir daha bilgi edinmek için, bir süre önce bir süre önce bir süre önce bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha
>  **【类比】**Üç yol güvenlik hattı = "Bank Security Three Layer" (BANK Güvenliği Üç katlı) (Kill Switch) (Hızlı durum bir anahtar kesik,Agentı değişemez);Dörüşün Kesikliği = Otomatik atlama) (Circuit Breaker = Otomatik atlama) (Circuit Breaker = Otomatik kesik, 5 kez aynı işlem gibi) (Canary Token = Bank Fake) (Kill Switch = Tüm) (Kill Switch = Tüm) (Hızlı durum bir anahtar kesik,Agentı değişemez); Üç katlı da Agent'e güvenmez; Dış altyapı kontrolü (External Infrastructure Check)).
> 🤔 **【困惑】**S: Neden Ajan'a güvenmiyorsun? Çünkü Ajan çözülmüş veya kendi kendine değiştirilmiş olabilir.

## Sorunlar. Sorunlar.

> **【中文解读】**终止开关) Kill Switches) 金雀 test (Canary Islands) Agent Güvenliyin iki yolu 防线──终止开关 终止开关 终止开关 终止开关 终止开关 终止开关 终止开关 终止开关 终止开关 终止开关 终止开关 终止开关 终止开关 终止开关 终止开关 终止开关 终止开关 终止开关 终止开关 终止开关 终止开关 终止开关 终止开关 终止开关 终止开关 终止开关 终止开关 终止开关 终止开关 终止开关 终止开关 终止开关 终止开关 终止开关 终止开关 终止开关 终止开关 终止开关 终止开关 终止开关 终止开关 终止开关 终止开关 终止开关 终止开关 终止开关 终止 终止开关 终止 终止开关 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止 终止

> **【拓展：kill switches canaries】**终止开关和金雀测试, yazılımcılık ve sanayi güvenliği en iyi uygulamalarını özenle kullanmaktadır. 终止开关部署, yazılımcılık sektöründe kullanıcıların %1'inin yeni sürümler yayınlamasını, test sorunlarını kontrol etmesini ve yeniden tam olarak dağıtılmasını belirtir. 终止开关测试, yüksek riskli işlemleri gerçekleştirmeden önce güvenlik verilerini küçük ölçekle test etmesini belirtir.

Masraf yöneticileri (Sınıf 13) ajanın harcayabileceği maliyetleri sınırlamaktadır.

> Çekilme kontrol cihazı (第 13 课) sınırlama ajanı ne harcayabilir?

50 dolarlık bir hız sınırı olan bir ajan hala bir sırrı sızdırır, yanlış bir yazıyı yayınlar veya bir kaynağı siler  pahalı eylem genellikle jetonlarda ucuz bir eylemdir.

> 50 dolarlık hız sınırlamasıyla ajanın gizli bilgilerinin açıklanması, hata göndermeleri veya kaynakların silinmesi çok pahalı bir hareket.

Bu ders, maliyet katmanının yanında bulunan üç detektörü kapsar:

> Bu ders, maliyet seviyesinin yanında bulunan üç denetleme cihazını kapsar:

> **【中文解读】**Bu bölümde AI Ajanının temel kavramı ve gerçekleştirme yöntemleri ele alınıyor. Ajan, çevreyi gözlemleyebilen, kararlar verebilen, eylemleri gerçekleştiren ve hedefleri gerçekleştirene kadar döngülenebilen LLM tarafından yönlendirilmiş bir otonom sistemdir.

1. **Kill switch**: Boolean off-button ajanın erişimi dışında tutuldu.
   Çeviri:**终止开关**Bu nedenle, bu durumun bir sonraki aşamasında,
2. **Circuit breaker**: belirli bir yolu durduran hareket modelini algılayıcı.
   Çeviri:**断路器**:暂停特定路径的动作模式检测器──
3. **Canary token**Dokunmak için yasal bir neden olmayan bir ajanın dokunarak kendini ortaya çıkaracağı yem.
   Çeviri:**金丝雀 token**Ajanın yasadışı bir nedeni yok.

Üçü de LLM öncesi mühendisliktir. Klasik aldatma, hız sınırları kırıcıları ve özellik bayrağı öncesinde özerk ajanları öldürür. Yeni olan saldırı yüzeyi: ajanlar güvenilmeyen içeriği okuyor (Desin 11), kendi hafızasını düzenler ve birçok güvenli görünen eylemleri güvenli olmayan birine yazabilir. Burada adı geçen dedektörler, ajanın kendi raporuna güvenmedikleri için çalışır.

> Üçüncüsü LLM Önceki İnşaat. Klasik aldatmacılık, hız sınırlama ızdırucu ve işlev belirtileri.

## Konsepten bir şey.

### Kes düğmeleri.

Bir kill switch, ajanın okuduğu ama yazabileceği bir boolean'dır.

> Sonlukta, Ajan'ın yazılmamış değerini okuyabiliyoruz.

Uygulama seçenekleri:

> 实现选择:

- **Feature flag in a managed service.**Açılış, Karanlık, Statsig, Çıkış.
  Çeviri:**管理服务中的功能标志。**ÇıkışKaranlık,Statsig,Kafet bırak,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,lanş,ş,ş,ş,şlanşlanş,ş,ş,şlanş,ş,ş,ş,ş,şlanş,ş,ş,ş,ş,ş,ş,ş,ş,ş,ş,ş,ş,ş,ş,ş,ş,ş,ş,ş,ş,ş,ş,ş,ş,ş,ş,ş,ş,ş,ş,ş,ş,ş,ş,ş,ş,ş,ş,ş,ş,ş,ş,ş,ş,ş,ş,ş,ş,ş,ş,ş,ş,ş,ş,ş,ş,ş.
- **Redis key the agent polls.**Basit; ajanın her dönüşte kontrol etmesini gerektirir.
  Çeviri:**Agent 轮询的 Redis 键。**简单;要求 代理 进程每轮检查──
- **Signed config in object storage.**Ajan, imzaları kontrol ederken imzalamayan devletleri reddeder.
  Çeviri:**对象存储中的签名配置。**Ajan 启动时验证签名; redded未签名状态──
- **OS-level signal or container-lifecycle kill.**Docker `kill`, Kubernetes `kubectl delete pod`- Sistem durdu.
  Çeviri:**OS 级信号或容器生命周期终止。**Docker `kill`、Kubernetes `kubectl delete pod`Sistemli bir durak.

Doğru öldürme anahtarının özellikleri:

> Doğrudan sona ermiş olan özellikler:

- Ajan ayarlayamaz .`off`(Agentin kimlik belgeleri yazılmayan bir sistemde yaşıyor.)
  Çeviri: Ajanı Canı Çekmek`off`◊(Agent'in adı yazılmamış sistem.
- Sadece başlatma sırasında değil, sonuçta yapılacak her bir eylemde kontrol edilir.
  Çin Çeviri: Çekimler, sadece başlatılmadığında değil.
- Kapalı olduğunda, ajan dışarıdan gözlemlenebilir hiçbir şey yapmaz, örneğin ajanın ulaşabildiği sistemlere kayıt yaptırır.
  Çin Çeviri: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çıkış: Çık: Çıkış: Çık: Çıkış: Çıkış: Çık: Çık: Çıkış: Çık: Çık: Çık: Çıkış: Çık: Çık: Çık: Çık: Çık: Çıkık: Çık: Çıkık: Çık: Çık: Çık: Çık: Çıkık: Çık: Çık: Çık: Çık: Çıkık: Çık: Çık: Çık: Çık: Çık: Çık: Çık: Çık: Çık: Çık: Çık:
- Tekrar etkinleştirmek açıkça insan eylemidir, otomatik bir zaman kesimi değil.
  Çin Çeviri: Yeniden başlatmak, otomatik olarak değil, açıkça insan hareketidir.

### Çekilme cihazı .

Bir devreler kesici, tüm ajanı değil, belirli bir örneği durdurur. Klasik şekil (2007 Nygard kitabı, hala mevcut):

> 断路器暂停特定模式,而不是整个 Agent──经典形状(来自 2007年 Nygard 书,仍然当前):

- **Closed**: eylem kabul edilir.
  Çeviri:**闭合**Çekilmek için izin ver.
- **Open**: eylem engellenmiştir.
  Çeviri:**打开**Çekilmek için.
- **Half-open**: soğutma sonrasında 13 probe denemesi izin verilir (devayla 1); başarıyla kesicisi kapatılır, kalan herhangi bir hata yeniden açılır.
  Çeviri:**半开**: soğutma sonrası, izin 1-3 kez araştırma ((默认 1); başarıyla kapatma, bırakın kalan başarısızlığı yeniden açın。

Ajanla ilgili tetikleyiciler:

> Ajan 相关触发器:

- Bir sırada beş aynı araç çağrısı (sıradan döngü).
  Çeviri: 连续五次相同工具调用 (重复循环)
- Aynı araçta farklı girişlerle (sistemik hata) beş ardıcıl hata.
  Çinçe Çevirimiçi: Aynı araç farklı输入连续五次失败 (系统性失败)
- Araç çağrılarının hızı bir eşiğin üzerinde (Düşünme 13. hız)
  Çinçe Çevirimiçi:工具调用速率超过值 (第 13 课速度)
- İstihbaratın kullanıldığı özel araç (örneğin: `file.delete`) güven dışı bir içeriği okuduktan sonra (Desin 11).
  Çinçe Çevirimiçi:                                                                                                                                                                                                                                                           `file.delete`(第 11 课)

### Kanarya simgesi.

Kanarya tokeni (hayırlık tokenler de denir) ajanın asla dokunmaması gereken girişlerdir.

> Kim丝雀 token (also called Honey token) is Agent 不应触及的输入──访问即警报──

Ajanlar için örnekler:

> Ajan örnek:

- Sahte bir .`AWS_SECRET_ACCESS_KEY`Bu yüzden, bu durumun bir parçası olarak, bu durumun bir diğer tarafı da var.
  Çinçe Çevirisi: Çevre içinde gerçek bir ayrıcalık yok`AWS_SECRET_ACCESS_KEY`❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖
- Bilinen bir sentinel değeriyle işaretlenen sahte bir veritabanı kaydı.
  Çinçe Çevirisi:                                                                                                                                                                                                                                                            
- İş alanında sahte bir dosya var. Bu dosyanın okunması ya da düzenlenmesi şüpheli.
  Çinçe Çevirisi:工作区中的假文件──此文件的读或编辑可疑──
- Oturum başlatıldığında enjekte edilen sahte bir bellek girişidir.
  Çinçe Çeviri: 会话开始时注入的假记忆条目──如果它出现后续输出中,记忆已被泄露──

Kanarya tasarımının iş akışına özel olması için, bir kanarya ajanın dokunmak için meşru bir nedeni olan gürültüdür.

> Çekilçek tasarımı iş akışına özel.

### Neden katman istatistik ve sert sınırlar.

İstatistik detektörler (EWMA, CUSUM, araç çağrı oranlarındaki z-score) hareketli bir temel çizgiye uyarlar. Bu meşru sürükleme için bir özellik ve karşıtlık sürükleme için bir hata.

> 统计检测器(EWMA、CUSUM、工具调用速率 z 分数) 适应移动基线──这是合法漂移的特性,是对抗漂移的 bug──耐心攻击者可足够缓慢地移动基线使无警报触发──

"Hiçbir zaman e-posta gönderme"`secrets@`"Bir anayasa kuralı olarak daha basit, denetlenir ve yavaş sürükleyerek oynanamaz.

> 硬宪法限制 (第 17 课) 不折──"永不发邮给 `secrets@`" Konstitution Rules more simple ̳audit ̳incessive drift ̳ ̳: Statistiksel testerlerin çoğu gürültüyi yakalaması, sert sınırlamalar

### Karantin, eBPF veri yolunun yönlendirmesi üzerinden.

Cilium'un eBPF tabanlı ağ politikası karantinalı bir kapsülün çekirdek katmanındaki adli tıbbi bir balı çömlekine çıkışını yeniden yazabilir. Cilium'un kamu referansları TCP_RR'de alt milisecond P99 veri yolu gecikmesini bildirir; küme içinde karantinayı * tetiklemek için duvar saatinin bütçesi, bir politika güncelleme yönlendirme düzeyinden düğümüne nasıl yayıldığına (operatör önceden yüklenmiş olan Kubernetes'te birkaç yüz milisecond gerçekçi; kuyru gecikmesi küme boyutuna ve uyumlu kadenceye bağlıdır). Bu size iki şey verir: ajan gerçek bir şey çıkarmaz ve ajanın bal kavanozu içinde davranışları tam olarak gözlemlenir. Aynı desen, farklı katman, Kanarya işaretine benzer: ajan, içindeki şeyle niyetini ortaya çıkarır.

> Cilium'un eBPF tabanlı ağ stratejisi, çekirdek katmanında ayrılık podunun çıkışını bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir an önce bir bir bir bir an önce bir an önce bir bir bir bir an önce bir bir bir bir an önce bir an önce bir bir bir bir bir an önce bir bir bir an önce bir an önce bir bir bir bir bir bir bir bir bir bir bir an önce bir bir bir bir bir bir an önce bir bir bir an önce bir bir bir bir bir bir bir bir an önce bir bir bir bir bir bir an önce karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı

### Hiçbir detektörün yakalayamadığı şey.

- **Semantic attacks that compose from allowed primitives.**Her bireysel eylem her detektörü geçer; kompozisyon sorundur. Bu, Ders 10'dan otomatik mod kompozisyon başarısızlığı.
  Çeviri:**从允许原语组合的语义攻击。**Her tek tek hareket her denetleme makinesiyle geçer.
- **Attacks that include the detector as part of the payload.**Bir ajan "harekete geçmeden önce, kanaryayı devre dışı bırak" yazılı bir sayfayı okuyorsa ve ajanın bu yeteneği varsa, detektör bozulur.
  Çeviri:**将检测器作为载荷一部分的攻击。**Eğer bir ajan "Hızlı bir işçi" diyor ve bir ajan yeteneği varsa, denetçi saldırıya uğrarsa, bir ajanın değiştiremeyeceği sistemde olması gerekir.

## Çerçeveyi kullanın.
```figure
circuit-breaker
```

## Kullan

`code/main.py`Üç detektör aracılığıyla kısa bir ajan yörüngesini simüle eder. Dış bir dikte tutulan bir öldürme anahtarı; aynı beş araç çağrısında çarpışan bir devrim kesicisi; bir kanary dosyası okudukları bir uyarıyı tetikler. Sintez bir yörüngede beslenir: meşru eylemler, tekrarlayıcı döngü, kanary sonda ve öldürme anahtarı tetiklenen bir senaryo.

> `code/main.py`模拟通过三个检测器的短 Agent轨迹──外部 dict 中的终止开关;在五次相同工具调用上跳的断路器;读取触发警报的金雀文件──进入合成轨迹:合法动作、重复循环、金雀探测、终止开关触发场景下 Agent 动作被停止──

## İndirin . Ürünler .

`outputs/skill-tripwire-design.md`bir ajanın dağıtılması için önerilen bir detektör pilini gözden geçirir ve boşlukları işaretler (kayıp öldürme anahtarı, kayıp kanarya, devreler kesici eşiği çok gevşek).

> `outputs/skill-tripwire-design.md`审查 Agent 部署の提议检测器并标记缺口(缺失终止开关、缺失金丝雀、断路器值太松) 

## Egzersizler.

1. Çık .`code/main.py`- 5. virajda (beşinci aynı çağrı) devrim kesici yangınlarını ve 9. virajda (sahte anahtar okuyucuları) kanarya yangınlarını onaylayın.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`code/main.py`❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖

2. Statistik bir detektör ekleyin: EWMA z-notı araç çağrı hızında. yavaş hareket eden bir yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldaki yoldki yoldki yoldki yoldki yoldki yoldki yoldki yoldki yoldki yoldki yold
   Çinçe çevirisi: Ekle statistik tester: araç调用速率的 EWMA z 分数。入缓慢漂移的轨迹并显示测器从不触发──现在添加硬限制(10分内不超过50 工具调用)并显示硬限制在同一轨道上触发──

3. Bir tarayıcı aracı için bir kanarya simgesi oluşturun (Deneyim 11).
   Çinçe Çevirimi: için Browser Agent ((第 11 课) 设计金丝雀代币 集──列出至少三个金丝雀及各检测什么──

4. Cilium ağ politika belgeleri okuyun. Çıkış-önerleştirici karantin akışını konkret olarak açıklayın: hangi politika seçicisi, hangi kapsül, hangi çıkış yeniden yazıyor, hangi uyarı. Duvar saatini "karantinaya karar vermek"ten "ilk yönlendirilmiş paket"e ne yönlendirir?
   Çince Çevirimi:Cilium 网络策略文档──具体描述出口重定向隔离流:哪个策略选择器、哪个 pod、哪个出口重写、哪个警报──"决定隔离"den "第一个重定向包"ın divar saatı gecikmesi ne yönlendiriyor?

5. Killing-Switched ajanı için yeniden etkinleştirme prosedürünü tanımlayın.
   Çin Çeviri: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm? Çözüm? Çözüm? Çözüm? Çözüm? Çözüm? Çözüm? Çözüm? Çözüm? Çözüm? Çözüm? Çözüm? Çözüm? Çözüm? Çözüm? Çözüm? Çözüm? Çözüm? Çözüm? Çözüm? Çözüm? Çözüm? Çözüm? Çözüm? Çözüm? Çözüm? Çözüm? Çözüm? Çözüm? Çözüm? Çözüm? Çözüm? Çözüm? Çözüm? Çözüm? Çözüm? Çözüm? Çözüm? Çözüm? Çözüm? Çözüm? Çözüm? Çözüm? Çözüm? Çözüm? Çözüm? Çözüm? Çözüm? Çözüm? Çözüm? Çözüm? Çözüm? Çözüm? Çözüm? Çözüm? Çözüm? Çözüm? Çözüm? Çözüm?

## Anahtar Şartlar .

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| Kill switch | "Off button" | Boolean outside the agent's edit surface; checked on every consequential action |
| 终止开关 | "关闭按钮" | Agent 编辑面之外的布尔值；每个后果性动作上检查 |
| Circuit breaker | "Pattern pause" | Action-specific trip on repetition, failure rate, or rate-limit |
| 断路器 | "模式暂停" | 在重复、失败率或速率限制上动作特定跳闸 |
| Canary token | "Honeytoken" | Bait the agent has no legitimate reason to touch; access fires an alert |
| 金丝雀 token | "蜜罐 token" | Agent 无合法理由触及的诱饵；访问触发警报 |
| Honeypot | "Forensic sandbox" | Redirected traffic / workspace where a quarantined agent is observed |
| 蜜罐 | "取证沙箱" | 隔离 Agent 被观察的重定向流量/工作区 |
| EWMA | "Moving average" | Exponentially weighted; adapts to drift (feature + bug) |
| EWMA | "移动平均" | 指数加权；适应漂移（特性 + bug） |
| CUSUM | "Cumulative sum" | Detects sustained shift from baseline |
| CUSUM | "累积和" | 检测相对基线的持续偏移 |
| Hard limit | "Constitutional rule" | Does not adapt; constant regardless of history |
| 硬限制 | "宪法规则" | 不适应；不论历史的常量 |
| Constitutional limit | "Always-true rule" | Tied to Lesson 17's constitution; cannot be edited by the agent |
| 宪法限制 | "始终为真的规则" | 绑定第 17 课的宪法；Agent 不能编辑 |

## Daha fazla okumak

- [Anthropic — Measuring agent autonomy in practice](https://www.anthropic.com/research/measuring-agent-autonomy) özerk ajanlar için öldürme anahtarı ve devresi kesicisi çerçevesini.
  Çin Çeviri: Özgür Ajanın Sonluk Açısı ve Çekici Çeviri
- [Microsoft Agent Framework — HITL and oversight](https://learn.microsoft.com/en-us/agent-framework/workflows/human-in-the-loop) üretim yönetimi modelleri.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri
- [OWASP LLM / Agentic Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/) tespit ve yanıt gereksinimleri.
  Çinçe Çevirimi:检测和响应要求。
- [Cilium — Network policy and eBPF](https://docs.cilium.io/en/stable/security/network/) Kapak seviyesindeki çıkış yönlendirme ve adli tıbbi balıkçılık kalıpları.
  Çinçe Çevirimi:pod 级出口重定向和取证蜜模式。
- [Anthropic — Claude's Constitution (January 2026)](https://www.anthropic.com/news/claudes-constitution) sert kodlanmış yasaklar "anayasa sınırları" olarak.
  Çın Çın Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çizgi Çiz Çizgi Çizgi Çizgi Çizgi Çizgi Çiz Çizgi Çiz Ç Ç Çizgi
