# Grup sohbet ve konuşmacı seçimi 群聊 选择 发言人

> Paylaşılan konuşma orkestrasyonu, bir konuşmaya N ajanları yerleştirir; bir seçme fonksiyonu (LLM, yuvarlak-robin veya özel) sonraki konuşmayı seçer. Bu gelişen çoklu ajan konuşmasının arşetipi. Ajanlar statik bir grafikte rollerini bilmiyorlar, sadece paylaşılmış havuza tepki veriyorlar. AutoGen GroupChat ve AG2 GroupChat referans uygulamalardır: AutoGen v0.2'nin GroupChat semantikası AG2 çatalında korunmuştur; AutoGen v0.4 olay yönlendirici bir oyuncu modeli olarak yeniden yazdı. Microsoft, AutoGen'i 2026 Şubat'ta bakım moduna koydu ve Semantic Kernel ile Microsoft Agent Framework'e (RC Şubat 2026) birleştirdi. GroupChat primitif hem AG2 hem de Microsoft Agent Framework'ta hayatta kalır  bir kez öğrenin, her yerde kullanın.

> **【中文解读】**Bu bölümden konuşmacıların seçimi hakkında konuşuluyor.

> **【拓展：group chat speaker selection→具体应用】**群聊发言人选择是多代理 讨论中的关键问题谁发言、什么时候发言、发言多久──三种主要策略:(1) 轮流制按固定顺序发言;(2) 相关性制最相关的代理发言;(3) 仲裁制一个专门协调者决定谁发言──AutoGen's GroupChat LLM'yi aracı olarak kullanmak──


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 16 · 04 (Primitive Model) | **前置知识:** Phase 16 · 04 (Primitive Model)
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**学本节前 Lütfen önce ele alın:Fase 16·04(原语模型)、AutoGen 基础──群聊 = N 个 Agent 共享一个对话池,发言人选择决定谁说话──
>  **【类比】**群聊发言人选择 = "konference主持人"──轮流制 = 圆桌按序;相关性制 = 谁懂谁说;仲裁制 = 主持人指定──AutoGen GroupChat LLM ile birlikte 主持人当高成本但灵活──2026 Dikkat:AutoGen 已被微软合并并到微软代理框架,AG2 是社区叉,两者保留 GroupChat 原语──

## Sorunlar sorunun giriş

Statik grafikler (LangGraph) iş akışı bilinirken harika. Gerçek sohbetler statik değildir: bazen kodlayıcı eleştirmeni, bazen araştırmacıyı, bazen yazarı sorar. Her olası teslimatın sert kodlanması bir kenar patlaması yaratır. * Ajanların ortak bir havuza tepki göstermesini istersin*, bir fonksiyon sonra kimin konuştuğunu belirler.

> 静态图(LangGraph) 工作流已知时很好──真实对话不是静态:有时编码器问审阅者,有时问研究员,有时问写作者──硬编码每可能的交接会产生边爆炸──你想要*Agent对共享池做反应*,某函数决定谁下发言──

Kenar patlama sorunu gerçek: tüm olası el uzatmalarla birlikte 5 ajanlı bir sistem 25 yönlü kenarlara sahiptir. Altı bir ajan ekleyin ve 36.

> 边爆问题是真实的:带所有可能交接的5 代理系统有25条有向边――加上第六代理就有36条――图方法不能扩展到现有的对话;你需要池――

İşte AutoGen GroupChat'ın yaptığı da bu.

> İşte bu, AutoGen GroupChat'ın yaptığı şey.

## Konsept merkezi konsept

### Şekil

```
              ┌─── shared pool ────┐
              │   m1  m2  m3  ...  │
              └─────────┬──────────┘
                        │ (everyone reads all)
      ┌───────┬─────────┼─────────┬───────┐
      ▼       ▼         ▼         ▼       ▼
    Agent A  Agent B  Agent C  Agent D  Selector
                                           │
                                           ▼
                                  "next speaker = C"
```

Her ajan her mesajı görür, sonra kim konuşacak seçmek için her dönüşte bir seçer fonksiyonu çağrılır.

> Her ajan, her haber görüyor. Seçer fonksiyonunu kullanıyor.

Grup Çat'ın güçlü ve zayıf yönleri de tam şeffaflık havuzudur. Güç: Herhangi bir ajan, herkesin söylediği her şeye tepki verebilir. Zayıflık: 20 turdan sonra, her ajansın bağlamı büyük, pahalı ve incelenmiştir. Yumuşatma: proje hedefleri (dersi 15) veya erken sona erdirilmektedir.

> 完全透明池既是Grouppchat'in优点也是弱点. 优点: herhangi bir ajanın herhangi bir kişiye söylediği herhangi bir şeye tepki verebileceği 弱点:20 轮后,每一个代理的上下文巨大、昂贵且稀释──缓解措施:为每一个代理 投影范围视图(15th lesson) 或提前终止──

### Üç seçen tatlı

**Round-robin.**Sıkılıklı bir döngü. Deterministik. Skalaları lineer olarak N'de ama bağlamı görmezden  bir kodlayıcı, konu yasal inceleme olduğunda bile dönüş alır.

> **轮询。**固定循环──确定性── N 线性扩展但忽略上下文 Even the topic is legal review,编码器 can also obtain the right to speak──

**LLM-selected.**Son bir havuz okuyan ve en iyi bir sonraki konuşmayı geri veren bir LLM çağrısı. Kontext farkında ama yavaş: her dönüşte bir LLM çağrısı eklenir. AutoGen'in varsayılan.

> **LLM 选择。**调用 LLM 读取近期池并返回最佳下文发言人──上下文感知但慢: her turda bir kez artırılmak LLM 调用──AutoGen'in默认选择──

**Custom.**Python fonksiyonu istediğiniz mantıkla. Tipik: Fallback kuralları ile LLM seçilen (örneğin, "her zaman doğrulayıcıya kodlayıcıyı takip et").

> **自定义。**Bir Python  işlevi, istediğiniz herhangi bir mantığı kullanın.

### Konuşulabilir Ajan API

```
agent = ConversableAgent(
    name="coder",
    system_message="You write Python.",
    llm_config={...},
)
chat = GroupChat(agents=[coder, reviewer, tester], messages=[])
manager = GroupChatManager(groupchat=chat, llm_config={...})
```

`GroupChatManager`Bir ajan bir tur tamamladığında, yöneticisi seçeneği arar ve bu da bir sonraki ajanı geri gönderir.

> `GroupChatManager`持有选择器──当 Agent 完成一轮时,管理者调用选择器,返回下一个 Agent──循环继续直到终止条件──

Seçim fonksiyonu GroupChat'in kalbidir. Değiştir, orkestrasyon tarzını değiştir. Dört-robin seçicisi = belirleyici. LLM seçicisi = uyarlayıcı. Özel seçicisi = kodladığınız kurallar. Aynı ilkeler, farklı orkestrasyon.

> Seçimci fonksiyonu GroupChat'ın merkezi olarak kullanılır.

### Sonlandırma

Üç ortak desen:

> Üç adet:

- **Max rounds.**Toplam dönüşlerde sert kapak.
  Çeviri:**最大轮数。**总轮数的硬上限──
- **"TERMINATE" token.**Ajanlar bir nöbetçi mesajı gönderebilir. Müdür ortaya çıktığında durur.
  Çeviri:**"TERMINATE" 标记。**Ajan görevli mesaj gönderebilir, yöneticisi ortaya çıkınca durur.
- **Goal-reached check.**Her dönüşü hafif bir doğrulayıcı çalışır ve konuşmayı bitirdiğinde durdurur.
  Çeviri:**目标达成检查。**轻量级验证者每轮运行和完成时停止聊天──

### AutoGen -> AG2 bölünmesi ve Microsoft Agent Framework birleşmesi
### Soy: çatallar ve birleşmeler

2025'in başında Microsoft, AutoGen'in (v0.4) etkinlik odaklı bir oyuncu modeli etrafında büyük bir yeniden yazmaya başladı. Toplum, ilk kullanıcıların entegre ettiği API'yi koruyarak AutoGen v0.2'nin GroupChat semantikasını AG2 olarak kırdı.

> 2025 yılının başlarında, Microsoft, AutoGen (v0.4) için olay yönlendirici aktör model etrafında büyük bir yeniden yazma yapmaya başladı.

Şarj gerekli oldu çünkü v0.4 temel yollarla geriye doğru uyumluluğu kırdı. AG2 orijinalini korudu.`GroupChat`- Evet .`ConversableAgent`ve`GroupChatManager`API istikrarlıken, v0.4 yeni olay yönlendirici ilk yaratıklar sunar.

> Bölüm gereklidir, çünkü v0.4 temel olarak arka uyumluluğu bozar.`GroupChat`- Evet.`ConversableAgent`和 `GroupChatManager`API 稳定, v0.4  yeni olayların sürüşü için kullanılır.

Şubat 2026'da Microsoft, AutoGen'in bakım moduna geçeceğini, etkinlik odaklı aktör modelinin **Microsoft Agent Framework**GroupChat konsepti her iki pistte de hayatta kalır; uygulama detayları farklıdır. AG2 v0.2 uyumlu kod için tercih edilen yukarı kaynaktır.

> 2026 yıl 2 月, Microsoft AutoGen'i 维护模式,事件驱动 actor 模型合并到 **Microsoft Agent Framework**Grup Çat kavramı iki yörede hayatta kalıyor; gerçekleştirmek ayrıntıları farklıyor.

Ders: API yüzey çerçevelerden daha uzun sürer. 2024'te AutoGen v0.2'nin GroupChat API'ye karşı yazılan kod, 2026'da AG2 üzerinden değişmeden çalışır. Çerçeveler çürürüyor; primitivler ( paylaşılan havuz + seçiciler) yapmazlar. Primitivler üzerine bahis edin.

> Öğrenim:API 表面比框架持久──2024 yıl için AutoGen v0.2 GroupChat API 编写的代码在 2026 yıl boyunca AG2 仍然不变运行──框架变化;原语(共享池 + 选择器) 不变──押注原语──

### GroupChat uygun olduğunda

- **Emergent conversations.**Her olası sonraki hoparlörü önceden kablolamak istemezsin.
  Çeviri:**涌现对话。**Önceden her bir konuşmacıyla bağlantı kurmak istemiyorsun.
- **Role-mixing tasks.**Kodlayıcı araştırmacıdan, araştırmacı arşivciden, arşivci de kodlayıcıdan geri istiyor.
  Çeviri:**角色混合任务。**编码器问研究员,研究员问档案员,档案员反问编码器──流程不是DAG──
- **Exploratory problem-solving.**"Brainstorm toplantısı" düşün, "montaj hattı" değil.
  Çeviri:**探索性问题解决。**"Tüm bir dizi" yerine "Tüm bir dizi" düşünün.

### Başarısız olduğunda

- **Strict determinism.**LLM seçicisi aynı sürede, farklı çalışmalar, farklı konuşmacılar olabilir.
  Çeviri:**严格确定性。**LLM 选择器可能不一致──相同提示,不同运行,不同下一个发言者──
- **Sycophancy cascades.**Ajanlar en güvenle konuştuğu kişiye geri dönüyorlar.
  Çeviri:**谄媚级联。**Ajan en güvenli konuşmacıya boyun eğmiştir.
- **Context bloat.**Her ajan her mesajı okuyor; 10 dönüşten sonra bağlam büyüktür. Görünümleri kapsamlamak için projeksiyonları kullanın (Deneyim 15).
  Çeviri:**上下文膨胀。**Her Ajan, her haber okuyor.
- **Hot speakers.**Bir temsilci konuşmada egemenlik kazanır çünkü seçiciler kendi uzmanlıklarını tercih eder.
  Çeviri:**热发言者。**Bir ajan, eleştiriciyi kendi uzmanlığına yönlendirerek konuşmayı yönlendirir.

### Grup sohbetleri ve yöneticisi

Aynı ilkeller, farklı varsayımlar:

> Aynı orijinal, farklı bir anlamda:

- Gözetmen: Bir ajan planlar yapar, diğerleri yürütür. Seçimci "planlayıcıya ne yapması gerektiğini sor".
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri
- Grup sohbetleri: tüm ajanlar eşcinsidir; seçicisi paylaşılan havuz üzerinde bir fonksiyondur.
  Çin dilinde:群聊:所有 Agent 是对等的;选择器 是共享池上的函数──

Her ikisi de Ders 04'ten dört ilksel kullanıyor. Grup sohbetleri standart olarak LLM seçtiği orkestrasyon ve tam bir havuz paylaşım durumuna kadar.

> 两者都使用课04的四个原语──群聊默认使用LLM 选择的编排和全池共享状态──

Gözetmen ve grup sohbetleri arasında seçim çoğunlukla *plani kimin elinde tuttuğu* ile ilgilidir. Gözetmen: bir ajan planın sahibi ve delegeler. Grup sohbet: plan iç içindir, konuşmadan ortaya çıkar. Birincisi daha kontrol edilebilir; ikincisi daha esnekdir.

> 監督者と群談 arasındaki seçim, öncelikle plan sahibi olanlar hakkındadır.

## Yapın.
```figure
swarm-speaker
```

## Yapın

`code/main.py`Bu programın ilk başından itibaren, üç ajan (kodlayıcı, yorumcu, yöneticisi), grup ve LLM seçilen çeşitleri ve bir sonlandırma ile birlikte, bir`TERMINATE`- Bir işaret.

> `code/main.py`Standartlar Kütüphanesi'nden başlayan bir Grup Çatı, üç Ajan, bir düzenleyici, bir gözcü, bir yöneticisi, bir sorgu ve bir LLM  seçim değişikliği, ve`TERMINATE`标记上终止──

Demo, iki varians için konuşma transkripti ve seçicinin karar izini basar.

> 演示印交谈记录以及两种变体的选择器决策追踪──

## Çerçeveyi kullanın.

`outputs/skill-groupchat-selector.md`belirli bir görev için GroupChat seçeneğini yapılandırır  round-robin vs LLM-seçilmiş vs özel, ve seçeneğin hangi girişlerini (son mesajlar, ajan uzmanlıkları, dönüş sayıları) kullanmak için.

> `outputs/skill-groupchat-selector.md`Görev belirleme konumu Grup Çat  seçme cihazı  sorgu vs. LLM  seçme vs. kendini tanımlamak, ayrıca ne kullanmak  seçme cihazı 输入(最近消息、Agent 专长、轮次计数) 。

## İndirin . Ürünler .

Kontrol listesini:

> 检查清单:

- **Max rounds cap.**Her zaman. Tipik görevler için 10-20.
  Çeviri:**最大轮数上限。**总是使用──典型任务 10-20──
- **Speaker-balance metric.**İzleme aracı başına döner; dengesizlik bir eşiği aşırırken uyar.
  Çeviri:**发言者平衡指标。**Her ajanın sırasındaki dengesizlik, bir polis tarafından belirlenmiş bir değerden daha fazla.
- **Termination token.** `TERMINATE`veya özel bir doğrulama ajanı.
  Çeviri:**终止标记。** `TERMINATE`Ya da özel bir verifiyeci ajanı.
- **Projection or scoped memory.**~ 10 mesajdan sonra, bağlam şişmesini önlemek için her ajanı sadece bir kapsamlı görüntülemeyi düşünün.
  Çeviri:**投影或范围内存。**10 haberden sonra, her ajanın aşağıdaki yükselişin önlenmesi için sadece bir görüntü alanını düşünün.
- **Selector logging.**LLM seçilen variantlar için, seçicinin girişini ve seçimini kayıt edin. Aksi takdirde debugging imkansızdır.
  Çeviri:**选择器日志。**LLM için 选择变体,记录选择器的输入和选择──否则调试不可能──

## Egzersizler.

1. Çık .`code/main.py`- Round-robin ve LLM seçilmişleri arasındaki konuşmayı karşılaştırın.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`code/main.py`◊LLC  seçme altında konuşma ◊ Her türlü modelde hangi ajanın yönlendirici olduğu?
2. Seçicide "Agent başına maksimum konuşma" kuralını ekleyin.
   Çinçe Çevirim: Çekim Aracında Ekle "Her Ajan En Büyük Söz Sayısı" Kuralı.
3. Hedefine ulaşmış bir sonlama uygulayın: değerlendirici "tamklı" olarak döndüğünde durun.
   Çinçe Çevirimi Çevirisi: Çözümcü'nin "önlenmesi" için geri dönmesi durduruldu.
4. GroupChat'te AutoGen sabit belgeleri okuyun.`GroupChatManager`- Evet .
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`GroupChatManager`Uygulama:
5. AG2 repo'sını okuyun ve GroupChat'ın v0.2'sini v0.4 olay yönlendirici sürümüne karşılaştırın. v0.4 hangi spesifik özellikleri (sürüm, hata toleransı, komposabilite) ekler?
   Çin dilinde:阅读 AG2 仓库并比较其 v0.2 GroupChat 与 v0.4 事件驱动版本──v0.4 添加了什么具体属性(吞吐量、容错、可组合性)?

## Anahtar Şartlar .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| GroupChat / 群聊 | "Agents in one chat room" / "一个聊天室中的 Agent" | Shared message pool + selector function. AutoGen / AG2 primitive. / 共享消息池 + 选择器函数。AutoGen / AG2 原语。 |
| Speaker selection / 发言者选择 | "Who talks next" / "谁下一个说话" | The function that picks the next agent. Round-robin, LLM-selected, or custom. / 选择下一个 Agent 的函数。轮询、LLM 选择或自定义。 |
| GroupChatManager / 群聊管理者 | "The meeting host" / "会议主持人" | AutoGen component that owns the selector and loops over turns. / 拥有选择器并循环轮次的 AutoGen 组件。 |
| ConversableAgent / 可对话 Agent | "The base agent" / "基础 Agent" | AutoGen base class; an agent that can send and receive messages. / AutoGen 基类；可以发送和接收消息的 Agent。 |
| Termination token / 终止标记 | "The 'stop' word" / "停止词" | Sentinel string (usually `TERMINATE`) that ends the chat. / 结束聊天的哨兵字符串（通常是 `TERMINATE`）。 |
| Hot speaker / 热发言者 | "One agent dominates" / "一个 Agent 主导" | Failure mode where the selector keeps picking the same agent. / 选择器持续选择同一 Agent 的失败模式。 |
| Context bloat / 上下文膨胀 | "Pool grows unbounded" / "池无限增长" | Each agent reads every prior message; context grows with turns. / 每个 Agent 读取每条先前消息；上下文随轮次增长。 |
| Projection / 投影 | "Scoped view" / "范围视图" | Role-specific view into the shared pool to prevent context bloat. / 角色特定的共享池视图以防止上下文膨胀。 |

## Daha fazla okumak

- [AutoGen group chat docs](https://microsoft.github.io/autogen/stable/user-guide/core-user-guide/design-patterns/group-chat.html) Referans uygulanması
  中文翻译:AutoGen 群聊文档  参考实现
- [AG2 repo](https://github.com/ag2ai/ag2) topluluk AutoGen v0.2 devamı
  中文翻译:AG2 仓库  社区 AutoGen v0.2 延续
- [Microsoft Agent Framework docs](https://microsoft.github.io/agent-framework/) birleşmiş halefi, RC Şubat 2026
  中文翻译:Microsoft Agent Framework 文档  合并后的继任者,2026 年 2 月 RC
- [Microsoft Agent Framework docs](https://learn.microsoft.com/en-us/agent-framework/) birleşmiş halefi, RC Şubat 2026
- [AutoGen v0.4 release notes](https://microsoft.github.io/autogen/stable/) olaylara dayalı aktör modelinin yeniden yazılması
  中文翻译:AutoGen v0.4 发布说明  事件驱动 actor 模型重写详情
