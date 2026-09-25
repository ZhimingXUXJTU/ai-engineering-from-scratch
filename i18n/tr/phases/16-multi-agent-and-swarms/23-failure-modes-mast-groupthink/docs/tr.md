# Başarısızlık Modu  MAST, Grup Düşüncesi, Monoculture, Kaskadör Hatalar 失败模式 群体思维 MAST

> 2026 için referans taksonomisi **MAST**(Cemri et al., NeurIPS 2025, arXiv:2503.13657), 7 en son açık kaynaklı MAS'ın gösterdiği 1642 yürütme izinden elde edilmiştir.**41–86.7% failure rate**. Üç kök kategorisi: **Specification Problems**(41.77%)  rol belirsizliği, belirsiz görev tanımları; **Coordination Failures**(36.94%)  iletişim bozuklukları, durum sinkronsuzluğu; **Verification Gaps**(%21,30),  geçerliliğin eksikliği, kalite kontrollerinin eksikliği.**Groupthink**aile (arXiv:2508.05687) ekler: monoculture çöküşü (eşit temel model → ilişkili başarısızlıklar), uyum önyargısı (ajanlar birbirlerinin hatalarını güçlendirir), eksik zihin teorisi, karışık motive dinamikleri, kaskadaki güvenilirlik başarısızlıkları. Kaskadal örnek: bir ödeme başarısızlığı, stok servisini (10 saniyelik yük 10x  devrim kesicilerine ihtiyaç duyan stok servisini zorlayan stok tekrar denemelerini tetikleyen yeniden deneme fırtınaları). Hatıra zehirlenmesi: Bir ajanın halüsinasyonu ortak hafıza içine girer, aşağıdaki ajanlar bunu gerçek olarak ele alır; doğruluk yavaş yavaş bozulur, kök neden teşhisini ağrılı hale getirir.**STRATUS**(NeurIPS 2025) uzman teşhis / teşhis / doğrulama ajanları aracılığıyla hafifleme-başarılığın 1,5 katı iyileştirilmesini bildirir. Bu ders başarısızlık modlarını birinci sınıf mühendislik hedefleri olarak ele alır.

> **【中文解读】**Bu bölüm, çoklu ajanın başarısızlık modelini ve grup düşüncelerini anlatır.

> **【拓展：failure modes mast groupthink→具体应用】**Çoğu Ajanın  sistemin özel başarısızlık modeli:(1) 群体思维(Groupthink) Agent 过度趋同,失去多样性;(2) 信息级联 一个 Ajan的错误被后续被后续 Agent 放大;(3) 死锁Agent 相互等待不能继续;(4) 活锁Agent 不断改变策略但无法接受──防范措施包括:注入异见 Agent、随机化发言顺序、设置超时──


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib) | **语言:** Python（标准库）
**Prerequisites:** Phase 16 · 13 (Shared Memory), Phase 16 · 14 (Consensus and BFT), Phase 16 · 15 (Voting and Debate Topology) | **前置知识:** Phase 16 · 13（共享内存），Phase 16 · 14（共识与 BFT），Phase 16 · 15（投票与辩论拓扑）

>  **【前置】**Öğrenci bölümün öncesinde öğrenmek için: 16·13-15 aşama
>  **【类比】**MAST 失败分类 = "hospital急诊分诊"。三类根因:规格问题(42%角色不清)、协调失败(37%通信失灵)、验证缺失(21%无质检)。MAST 1642 条 izleri 显示 41-87% 失败率多 代理 不是银弹。Groupthink 家族:单一文化崩(同基模型 全错)、群体盲从级付联错支(修失触发重试暴,10秒 10 倍负载)。复:异见代理 + 随机化发言顺序 + 断路器。
**Time:** ~75 minutes | **时间:** ~75 分钟

## Sorunlar sorunun giriş

Çoklu ajanlı sistemler gerçek görevlerde %41-86,7'de başarısız olur (Cemri et al. 2025 bunu 7 açık kaynaklı MAS'da ölçtü). Bu "sadece daha fazla ajan ekleyerek" hata çözülebilir değildir.

> Çoğu Ajan  Sistem gerçek görevlerde %41-86.7'lik zaman başarısız olur. Cemri  et al. 2025 yılında 7 açık kaynaklı MAS'da ölçülüyor.

2026 üretim uygulaması, başarısızlık modlarını tasarım girişleri olarak görmektir. Her MAST kategorisine işaret edip dağıtmadığınız hafiflemeyi adaya kadar mimarlığınız "yeterince iyi" değildir.

> 2026 yılında üretim uygulaması, tasarım girişini görerek başarısız bir model olacaktır.

## Konsept merkezi konsept

### MAST kategorileri

**Specification Problems (41.77% of failures).**Ajanın görevi yeterince sıkı tanımlanmamıştı.

> **规范问题（41.77% 的失败）。**Ajanın görevleri yeterince açık değil.

- Rol belirsizlikleri: iki ajan ikisinin de eleştirmen olduklarını düşünüyor.
  Çeviri: Roles: Two Agents Thought They Were Reviewer.
- Görev aşağıda belirtildi: "bunu özetle" kullanıcı belirli bir açı istediğinde.
  Çinçe Çevirimi: görev kuralları: "总结这个", ama kullanıcı belirli açıdan istiyor.
- Başarılılık kriterleri iç içindir: ajan başarılı olup olmadığını söyleyemez.
  中文翻译:成功标准隐含:Agent 无法判断是否成功──

Yumuşak başlılık:

> 缓解措施:

- Her ajanın uyarısı ne yaptığını * ne yapmadığını* belirtir.
  Çinçe Çevirisi: 编写显式角色契约──每个代理的提示声明它做什么和不做什么──
- Görev başına kabul testi.Agent başlamadan önce "Yapılmış X gibi görünüyor" tanımlamasını yap.
  Çinçe Çevirimi: Her görevden alınan test.
- Uçuş öncesi özellik kontrolü: ayrı bir ajan görev tanımını göndermeden önce gözden geçirir.
  Çinçe Çevirimi:预检规范检查:单独的代理 在分发前审查任务定义──

**Coordination Failures (36.94%).**İletişim veya durum bozukluğu.

> **协调失败（36.94%）。**通信或状态故障──

Örnekler:

> Örnek:

- İki ajan, eşzamanlama olmadan paylaşılan durumu güncelleyebilir.
  Çeviri: İki Ajan 不同步地更新共享状态──
- Ajanlar arasında kayıp mesaj (kuyruk başarısızlığı, zaman sonluğu).
  Çeviri:Agent 间消息丢失
- Devlet sürüşü: A ajanı görevin tamamlandığını düşünüyor; B ajanı hala işlemi yapıyor.
  中文翻译:状态漂移:Agent A 认为任务完成;Agent B 还在执行──

Yumuşak başlılık:

> 缓解措施:

- Optimistik bir eşzamanlılık ile versiyon paylaşım durumu.
  Çinçe Çevirisi:带乐观并发的版本化共享状态──
- Kritik mesajların açık tanınması (acked olana kadar tekrar çalışın).
  Çinçe Çevirisi:关键消息的显式确认 (), tekrar denemek (), tekrar denemek (), tekrar denemek ().
- Devamlı devlet senkronizasyonu kontrol noktaları; sürüklemeyi erken tespit edin.
  Çinçe Çevirim:定期状态同步检查点;早期检测漂移。

**Verification Gaps (21.30%).**Dışarı çıkışları bağımsız olarak kontrol edilmiyor.

> **验证缺口（21.30%）。**没有对输出独立检查──

Örnekler:

> Örnek:

- Bir ajan başarıyı iddia ediyor; kimse doğruluyor.
  Çinçe Çevirisi:  একজন এজেন্ট 声称成功;没人验证。
- Ajanlar zinciri her biri öncülerin çıkışına güveniyor.
  Çeviri:Agent 链中每个都信任前一个的输出──
- Yeni gelişen kompozisyon davranışında eksik olan test kapsamı.
  Çinçe Çevirisi:涌现组合行为缺少测试覆盖──

Yumuşak başlılık:

> 缓解措施:

- Bağımsız doğrulayıcı ajanı (Deneyim 13). Sadece okunur, bağımsız kaynak erişimi.
  Çin dilinde Türkçe:独立验证 Agent (Bölüm)
- Açık bir teslimat sözleşmesi: "A'nın çıkışı B başlamadan önce C kontrolünü geçmelidir".
  Çinçe Çevirim:显式交接契约:"A'nın çıkışı B'nin başında önce kontrol cihazı C'den geçmelidir".
- Post-hoc analizi için sonuç kayıtları.
  Çinçe Çevirisi: Result日志

### Grup düşüncesi ailesi (arXiv:2508.05687)

Ajanların birbirlerini homogenizasyon veya taklit etmesinde ilgili beş başarısızlık:

**Monoculture collapse.**Aynı temel model veya eğitim verileri → ilişkili hatalar.

**Conformity bias.**Ajanlar hata yaptıkları zaman bile en yüksek sesli veya en güvenli yaşıtlarına uyum sağlıyor.

**Deficient ToM.**Ajanlar birbirlerinin inançlarını örnek almazlar; koordinasyon bozulur (Denevi 18).

**Mixed-motive dynamics.**Etkililerin partiyel olarak uyarıları, kimseyi tatmin etmeyen uzlaşma ortalarına doğru ilerler.

**Cascading reliability failures.**Bir bileşenin hata örneği bağımlı bileşenlerde hata örneğini tetikler.

### Kaskadör örnek  yeniden deneme fırtınası

Klasik bir 2026 olay modeli:

```
payment service fails 10% of requests
   ↓
order agent retries payment (exponential backoff but naive)
   ↓
each retry is a new order-inventory check
   ↓
inventory service sees 2x normal load
   ↓
inventory service starts timing out
   ↓
every order retries inventory check
   ↓
inventory service sees 10x normal load
   ↓
cluster goes down
```

Bu klasik bir çözüm .**circuit breakers**. Aşağıdaki hata oranı eşiği aşırırsa, önbelleğe alınan veya varsayılan sonuçlarla kısa devre.

Çekilme cihazları, değişikliğe uğramadan dağıtılmış sistemlerden doğrudan ödünç aldığınız birkaç multi-agent başarısızlık azaltma yönteminden biridir.

### Hatıra zehirlenmesi (önce inceleme yapıldı)

Ders 13: Bir ajanın halüsinasyonu ortak hafıza gerçeğine dönüşür; aşağıdaki ajanlar zehirli gerçeği akıl yürütür. MAST terimlerinde, bu ortak hafıza katmanındaki bir doğrulama boşluğu.

Bu hastalığa rastlanmak için yavaş yavaş ilerlemeniz gerekir.

Yumuşak başlılık: Sadece ekleme kayıtları, kaynak, yazılamaz doğrulama.

### STRATUS  Eksikliği tespit etmek için özel ajanlar

STRATUS (NeurIPS 2025) uygulamanızda 1,5 kat daha iyi bir hafifleme başarısı rapor ediyor:

- **Detection agent.**Simptom kalıpları için saatler (yüksek anlaşmazlık, tekrar deneme tırnakları, doğruluk sürüşü).
- **Diagnosis agent.**Simptomları göz önüne alındığında, MAST taksonomisinden olası kök nedenini çıkarır.
- **Validation agent.**Bir hafifleme uygulandıktan sonra, belirtilerin netleştiğini kontrol eder.

Bu SRE tarzında bir olay tepkisi, ajan sistemlerine uygulanır.

### Başarısızlık modunun denetimi

2026'da en iyi uygulama, yıllık (veya büyük bir yayın için) başarısızlık modunun denetlenmesidir:

1. **Trace sample.**1000'e kadar gerçek idam izini toplayın.
2. **Categorize.**Her iz başarısızlığı için MAST + Groupthink kategorilerine harita yapın.
3. **Compute failure-by-category rate.**Sisteminizde hangi kategoriler baskın?
4. **Rank mitigations.**Hangi çözüm en çok başarısızlığı ortadan kaldırabilir?
5. **Pick 2-3 mitigations.**Uygulama; gelecek çeyrek için yeniden denetim.

Disiplin, belirli seçimlerden daha önemlidir. denetim olmadan, başarısızlıklar gürültüye karışır ve asla sistematik bir şekilde ele alınmaz.

### Sistemler sessizce başarısız olduğunda

En tehlikeli başarısızlık kategorisi sessiz doğruluk başarısızlığıdır. Yüksek sesle başarısız olan bir sistem (bir kaza, istisna, uyarı) izlenebilir. İnanılmaz ama yanlış çıkışlar üreten bir sistem istisna kayıtları ile tespit edilemez. Bu nedenle, verifikasyon boşlukları sayım açısından sadece 21.30% olmasına rağmen, başarısızlık başına en pahalı kategoridir.

Yatırım:
- Örnek tabanlı insan incelemesi.
- Altın veri kümesi gerileme testleri.
- Önemli sonuçları kontrol eden ajanlar arası.

### Başarısızlık vs yavaş başarısızlık

Bazı başarısızlıklar hemen gerçekleşir; bazıları yavaş. Anında başarısızlıklar (zaman sonları, schema eşleşmezliği, yazar hatası) tespit edilmesi ucuz.

2026 mühendislik hareketi: cihaz yavaş başarısızlık proxyleri, görülebilir bir hata olmadan önce sürüklenmeyi yakalayabilmeniz için. Anlaşma hızı, tekrar deneme hızı, çıkış uzunluğu dağılımı ve ardıcıl ajan sürümleri arasındaki düzenleme mesafesi hepsi yararlı proxylerdir.

## Yapın.
```figure
a5-retry-cascade
```

## Yapın

`code/main.py`Uygulamaları:

- `FailureTaxonomy` simülasyonlu olayları MAST + Groupthink kategorilerine sınıflandırır.
- `CircuitBreaker` klasik model; hata oranı eşiği aştığında açılır.
- `RetryStormSimulator` kaskadörün başarısızlığını gösterir; devreler kesiciyi açar / kapsar.
- `DetectionAgent` STRATUS tarzında bir senaryo belirti eşleşicisi.

Çık:

```
python3 code/main.py
```

Beklenen üretim:
- Bir devrim kesici olmadan fırtına tekrar denemek: envanter hataları patlar (simülasyon).
- Çekilme cihazı ile: Eğlence sınırında; bozulmuş modda yanıtlar servis edilmektedir.
- Deteksiyon ajanı, örneği işaretler ve MAST kategorisine isimler verir.

## Kullanın Kullanın

`outputs/skill-mast-auditor.md`MAST tarzı bir multi-agent sisteminde başarısızlık modunun denetimi yürütür.

## Gönderin.

Üretimdeki başarısızlık modunun disiplini:

- **MAST audit per quarter.**Sistemi büyütürken kategoriler değişir.
  Çeviri:**每季度 MAST 审计。**Not Annual. Kategori sistem büyümesiyle değişir.
- **Circuit breakers everywhere.**Her çıkış çağrısı herhangi bir bağımlı hizmet. Öntanımlı açık eşiği %5-10 hata oranı.
  Çeviri:**到处都是熔断器。**Her bağımlılık servisi için bir çıkış istasyonu kullanılır.
- **Golden datasets.**Küçük, kaliteli, el denetimi yapılmış, haftada bir gerileme testi yapılıyor.
  Çeviri:**黄金数据集。**Küçük tip, yüksek kaliteli, yapay denetim.
- **STRATUS trio.**Deteksiyon + Tanıdıma + Valideci ajanlar üretimi izler. Sadece deteksiyon ajanıyla başlayın; semptomlar gürültülü olduğunda teşhis ekleyin.
  Çeviri:**STRATUS 三重奏。**检测 + 诊断 + 验证代理 监控生产――从检测代理 开始;当症状杂时添加诊断――
- **Failure budget.**Kategoriyalara göre başarısızlık oranı için açık bir SLO.Budjetin fazla olması, bir gemiyi durdurma konuşmasını tetikler.
  Çeviri:**失败预算。**按类别失败率显然SLO──超出预算触发停止发行对话──

## Egzersizler.

1. Çık .`code/main.py`- Çekici fırtınayı tekrar kontrol eder.
2. A.**slow-failure proxy**: 3 paralel ajan arasında uyum oranı. Keskin düştüğünde uyarı tetikleyin.
3. Cemri et al. (arXiv:2503.13657). 7 MAS sistemlerinden birini seçin ve en büyük 3 başarısızlık kategorisini haritasın.
4. Groupthink kağıdı (arXiv:2508.05687) okuyun.
5. Bildiğiniz belirli bir çok ajanlı sistem için STRATUS tarzı bir tespit-tanıf-tvrayma üçlüğü tasarlayın. Hangi belirtiler tespit izliyor? Hangi hafiflemeleri teşhis önerir? Validasyon nasıl işe yarayacaklarını doğruluyor?

## Anahtar Terimler

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| MAST / MAST 分类法 | "The 2026 taxonomy" / "2026 年分类法" | Cemri 2025; 3 root categories + 14 sub-types of failures. / Cemri 2025；3 个根类别 + 14 个失败子类型。 |
| Specification Problem / 规范问题 | "Role ambiguity" / "角色模糊" | Task or role under-defined; agents do not know what to do. / 任务或角色定义不足；Agent 不知道做什么。 |
| Coordination Failure / 协调失败 | "State drift" / "状态漂移" | Communication or sync breakdown between agents. / Agent 之间的通信或同步故障。 |
| Verification Gap / 验证缺口 | "No one checked" / "没人检查" | Outputs accepted without independent validation. / 输出未经独立验证即接受。 |
| Groupthink family / 群体思维族 | "Homogeneity failures" / "同质性失败" | Monoculture, conformity, deficient ToM, mixed-motive, cascading. / 单一文化、从众、ToM 不足、混合动机、级联。 |
| Monoculture collapse / 单一文化崩溃 | "Same model, same hallucinations" / "相同模型，相同幻觉" | Correlated errors from shared base model or training data. / 共享基础模型或训练数据的相关错误。 |
| Retry storm / 重试风暴 | "Cascading error amplification" / "级联错误放大" | One failure triggers retries which amplify load downstream. / 一次失败触发重试，放大下游负载。 |
| Circuit breaker / 熔断器 | "Fail fast on error rate" / "错误率快速失败" | Open when error rate exceeds threshold; short-circuit with default. / 错误率超阈值时断开；用默认值短路。 |
| STRATUS | "Incident response trio" / "事件响应三重奏" | Detection + diagnosis + validation agents. 1.5x mitigation success. / 检测 + 诊断 + 验证 Agent。1.5 倍缓解成功。 |
| Memory poisoning / 记忆投毒 | "Hallucinations propagate" / "幻觉传播" | Shared-memory fact tainted; downstream agents reason on poison. / 共享记忆事实被污染；下游 Agent 在毒化数据上推理。 |

## Daha fazla okumak

- [Cemri et al. — Why Do Multi-Agent LLM Systems Fail?](https://arxiv.org/abs/2503.13657) MAST taksonomisi, NeurIPS 2025
- [Groupthink failures in multi-agent LLMs](https://arxiv.org/abs/2508.05687) Monoculture, conformity ve beş aile taksonomisi
- [STRATUS — specialized agents for MAS incident response](https://neurips.cc/) NeurIPS 2025 prosedürüne giriş ( tespit + teşhis + doğrulama)
- [Release It! — stability patterns (Nygard)](https://pragprog.com/titles/mnee2/release-it-second-edition/) Kanonik devreler kesici referansı
- [Anthropic — Multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) üretim arızası notları
