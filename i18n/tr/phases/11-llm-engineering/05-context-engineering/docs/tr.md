# Kontext Engineering: Windows, Budjetler, Hatıra ve İndirme.

> Çabuk mühendislik bir alt kümedir. Konteks mühendisliği tüm oyundur. Çabuk bir dizilme, bir dizilme. Konteks, modelin penceresine giren her şeydir: sistem talimatları, alınan belgeler, araç tanımları, konuşma tarihi, birkaç çekim örneği ve çabuk bir şey. 2026'daki en iyi AI mühendisleri bağlam mühendisleri. Ne girer, ne kalır ve hangi sırada karar verirler.

> **【中文解读】**提示工程只是上下文工程的子集──上下文工程管理模型窗口中的一切内容系统指令、检查文档、工具定义、对话历史等──2026 yılının en iyi AI 工程师就是上下文工程师──

> **【拓展：上下文工程→Claude生态】**Claude'un MCP protokolü, temel olarak, birleştirilmiş protokol yönetim modeli yoluyla aşağıdaki yazılımların standartlarının gerçekleştirilmesidir.

>  **【前置】**Önemli bir şekilde, bu konuda bilgi sahibi olmak için, 1. aşamada, 1. aşamada, 1. aşamada, 1. aşamada, 1. aşamada, 2. aşamada, 2. aşamada, 2. aşamada, 2. aşamada, 2. aşamada, 2. aşamada, 2. aşamada, 2. aşamada, 2. aşamada, 2. aşamada, 2. aşamada, 2. aşamada, 2. aşamada, 2. aşamada, 2. aşamada, 2. aşamada, 2. aşamada, 2. aşamada, 2. aşamada, 2. aşamada, 2. aşamada, 2. aşamada, 2. aşamada, 2. aşamada, 2. aşamada, 2. aşamada, 3. aşamada, 3. aşamada, 3. aşamada, 3. aşamada, 3. aşamada, 3. aşamada, 3. aşamada, 3. aşamada, 3. aşamada, 3. aşamada, 3. aşamada, 3. aşamada, 3. aşamada, 3. aşamada, 3. aşamada, 3. aşamada, 3. aşamada, 3. aşamada, 3. aşamada, 3. aşamada, 3. aşamada, 3. aşamada, 3. aşamada, 3. aşamada, 3. aşamada, 3. aşamada, 3. aşamada, 3. aşamada, 3. aşamada, 3. aşamada, 3. aşamada, 3. aşamada, 3. aşamada, 3. aşamada, 3. aşamada, 3. aşamada, 3. aşamada, 3. aşamada, 3. aşamada, 3. aşamada, 3. aşamada, 3. aşamada, 3. aşamada, 3. aşamada, 3. aşamada, 3. aşamada, 3. aşamada, 3. aşada.

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 10 (LLMs from Scratch), Phase 11 Lesson 01-02 | **前置知识:** Phase 10（从零理解 LLM）、Phase 11 Lesson 01-02
**Time:** ~90 minutes | **时间:** ~90 分钟
**Related:**Faza 11 · 15 (Hızlı Kayıtlama)  önbelleğe dostu düzen bağlam mühendisliği bir uzantı. 5 · 28 (Uzun bağlam değerlendirme) NIAH / RULER ile orta kayıp ölçmek için. **相关:**EY 11 · 15(提示缓存) 缓存友好布局是上下文工程的延伸──5 · 28(长上下文评估)介绍 NIAH/RULER 测量"中间丢失"──

## Öğrenme hedefleri

- Tüm bağlam penceresi bileşenleri (sistem istekleri, araçlar, geçmiş, alınan belgeler, jenerasyon başlık alanı) için token bütçelerini hesaplayın
  跨所有上下文窗口组件(系统提示、工具、历史、检索文档、生成余量) hesaplama belirti 预算
- Konekst pencere yönetim stratejilerini uygulayın: konuşma geçmişi için kısaltma, özetleme ve kaydırma penceresi
  实现上下文 pencereleri yönetim stratejisi: kesintisi, özetleri, kaydırma pencereleri yönetim sohbet tarihi
- Modelin en alakalı bilgilere olan dikkatini artırmak için öncelik ver ve bağlam bileşenlerini sıralayın
   öncelikli sıralama üzerine aşağıdaki metin bileşenleri, en ilgili bilgilere odaklanma modelini en iyi şekilde artırmak
- Sorgu türüne ve mevcut pencerenin alanına göre belirtiler dinamik olarak tahsis eden bir bağlam asembleri oluştur
   Yapım sorgu türüne ve kullanılabilir pencereler için alan hareketli dağıtım tokeni

> **【中文解读】**Bu dersin amacı: Çabuk Mühendislik, Sistemleşme Yönetimi Üzerine Modelle Giriş Üzerine Tüm Bilgiler.


## Sorunlar. Sorunlar.

Claude Opus 4.7'de 200K token penceresi (1M beta versiyonunda). GPT-5'de 400K. Gemini 3 Pro'da 2M. Llama 4'de 10M. Bu rakamlar doldurulana kadar muazzam görünüyor.

> Claude Opus 4.7'de 200K token var  Window(beta  sürümü 1M) ・・・GPT-5'de 400K ・・・Gemini 3 Pro'da 2M ・・・ Bu rakamlar doldurana kadar çok büyük görünüyor ・・・

İşte bir kodlama asistanı için gerçek bir ayrıntı. Sistem sorgulaması: 500 token. 50 araç için araç tanımları: 8.000 token. Alınan belge: 4.000 token. Konuşma tarihi (10 dönüş): 6.000 token. Güncel kullanıcı sorusu: 200 token. Gelişim bütçesi (maksimum çıkış): 4.000 token. Toplam: 22.700 token. Bu 128K penceresinin sadece 18%'idir.

> Bu bir programlama asistanının gerçek çözümüdür. Sistem Önerisi: 500 token──50 个工具定义: 8,000 token──检索文档: 4,000 token──对话历史(10轮): 6,000 token──当前查询:200 token──生成预算: 4,000 token──总计: 22,700 token──

>  **【类比】**上下文窗口像书桌桌面200K token 听起来很大,但放上"教科书(系统提示) "+"参考书(恢复文件) "+"草稿纸(tarih) "+"计算器(工具) "就快满了──**Lost in the Middle**现象像寻找东西: Kitap masasındaki şeyler dolu olduğunda, en kolay göz ardı edilen, orta yığının  you will only pay attention to the table's opening ( yakın yığın) ve sonu (hand margin)  Revive:把关键信息放最前或最后,中间放丢的内容──

> ️ **【易错点】**上下文管理的 3 个坑:(1) **历史无限增长**对话越长历史 越大,最终撞窗口;修复:用总结(每 N 轮缩成摘要) 或滑窗((只保留近 K 轮 + 第一轮) 』2) **工具定义重复发送** Her seferinde调用都把 50 个工具方案 全发一遍;修复:用快速缓存(Phase 11·15),Claude / OpenAI 都支持,省 90% cost──(3) **检索文档全塞**50 parça geri çağır  Full塞 prompt 模型迷失;修复:top-5 高质量块 + çapraz kodlayıcı 重排──

Ama dikkat bağlam uzunluğu ile lineer olarak ölçeklenmez. 128K bağlam belirtileri olan bir model, most transformörlerinde kare dikkat maliyetini (O(n^2) ödüyor, ancak çoğu üretim modeli verimli dikkat varianlarını kullanıyor. Daha da önemlisi, çekim doğruluğu azalıyor. "Haystack'taki İğne" testi, modellerin uzun bağlamların ortasında yerleştirilen bilgileri bulmakta zorlandığını göstermektedir. Liu ve diğerleri tarafından yapılan araştırma. (2023) LLM'lerin uzun bağlamların başlangıcında ve sonunda neredeyse mükemmel bir doğrulukla bilgi almadığını gösterdi, ancak doğruluk ortalama konuma yerleştirilen bilgiler için (koneksten oluşan pozisyonların 40-70%'i) %10-20 oranında düştü. Bu "ortalarda kaybolan" etki modelden model değişir ancak tüm mevcut mimarlıkları etkiler.

> Ancak dikkat aşağıdaki uzunluk linear genişlemeyi sürdürmez. Daha da önemlisi, arama doğruluk oranı düşüyor. "大海捞针" testi, modelin uzunluğa aşağıdaki orta konumdaki bilgiyi bulmakta zor olduğunu göstermektedir.

Pratik ders: 200K token kullanmak 200K token kullanmanın etkili olduğu anlamına gelmez. Dikkatle düzenlenen 10K token bağlamı genellikle atılan 100K token bağlamını üstlenir. Kontext mühendisliği bağlam penceresi içinde sinyal-gürültü oranını en üst düzeye çıkarma disiplini.

> 实际教训:有200K代币可用并不意味着使用200K代币是有效的──精心策划的10K代币上下文通常优于倾倒的100K代币上下文──上下文工程在上下文窗户内最大化信噪比的学科──

Pencereye koyduğunuz her token daha fazla ilgili bilgi taşıyabilecek bir token'ı değiştirir. Her anlamsız araç tanımlaması, her eski konuşma dönüşü, soruya cevap vermeyen her alınan metin parçası -- her biri, modelin görevi biraz daha kötü hale getiriyor.

> Pencerede yerleştirdiğiniz her bir simge daha fazla ilgili bilgi taşıyabilecek bir simgeyi oluşturuyor. Her bir bağlantısız araç tanımlaması, her geçen konuşma döngüsü, her bir cevap vermeyen sorunun kontrolü metin blokları.

## Konsepten bir şey.

> **【中文解读】**Kontext Mühendisliği) sadece hızlı yazmak değil, sistemli yönetim için bir model oluşturmak için aşağıdaki pencerede tüm bilgileri: kontrol sonuçları, sohbet tarihi, araç çıkışı, sistem talimatları vb.

> **【拓展：上下文窗口的有效利用】**GPT-4o 128K token vardır 上下文窗口, ancak araştırmalar modelin orta konumdaki bilgiye dikkatini düşürdüğünü göstermektedir.


### Konekst Penceresi Kıt Bir Kaynak

Konekst penceresini disk değil RAM olarak düşünün. Hızlı ve doğrudan erişilebilir, ama sınırlı. Her şeyi yerleştiremezsiniz. Seçmelisiniz.

> Yukarıdaki pencereleri disk değil RAM olarak düşün.

```mermaid
graph TD
    subgraph Window["Context Window (128K tokens)"]
        direction TB
        S["System Prompt\n~500 tokens"] --> T["Tool Definitions\n~2K-8K tokens"]
        T --> R["Retrieved Context\n~2K-10K tokens"]
        R --> H["Conversation History\n~2K-20K tokens"]
        H --> F["Few-shot Examples\n~1K-3K tokens"]
        F --> Q["User Query\n~100-500 tokens"]
        Q --> G["Generation Budget\n~2K-8K tokens"]
    end

    style S fill:#1a1a2e,stroke:#e94560,color:#fff
    style T fill:#1a1a2e,stroke:#0f3460,color:#fff
    style R fill:#1a1a2e,stroke:#ffa500,color:#fff
    style H fill:#1a1a2e,stroke:#51cf66,color:#fff
    style F fill:#1a1a2e,stroke:#9b59b6,color:#fff
    style Q fill:#1a1a2e,stroke:#e94560,color:#fff
    style G fill:#1a1a2e,stroke:#0f3460,color:#fff
```

Her bileşen boşluk için rekabet eder. Daha fazla araç tanımını eklemek sohbet geçmişi için daha az yer demektir. Daha fazla alınan bağlam eklemek birkaç çekim örneği için daha az yer demektir. Kontext mühendisliği, bu bütçeyi görev performansını en üst düzeye çıkarmak için tahsis etme sanatıdır.

> Her bir bileşen için daha fazla araç tanımlaması, daha az sohbet tarihi alanı anlamına gelir.

### Ortada Kaybolmuş

En önemli empirici bulgu bağlam mühendisliği. Modeller bağlamın başlangıcında ve sonunda bilgiyi daha iyi karşılar. Ortadaki bilgi daha düşük dikkat puanları alır ve daha fazla ihmal edilme olasılığı vardır.

> Yukarıdaki yazılımlarda en önemli pratik bulgular vardır. Modeller, yukarıdaki yazının başlangıcı ve sonundaki bilgilere daha iyi dikkat eder. Orta konumdaki bilgiler daha düşük dikkat oranına sahip olur, daha kolay göz ardı edilir.

Liu et al. (2023) bunu sistematik olarak test ettiler. 20 farklı pozisyonda ilgili bir belgeyi 20 irelevant belge arasında yerleştirdiler ve cevap doğruluğunu ölçtüler. İlgili belge ilk veya son olduğunda, doğruluk 85-90% idi. Ortadayken (20'nin 10 pozisyonu), doğruluk 60-70%'ye düştü.

> Liu 等人(2023) sistematik olarak bu fenomeni test ettiler. ilgili dosyaları 20 个不相关文档中不同位置,测量答案准确率──20 个中位位置,准确率下降至 60-70%──

Bu doğrudan mühendislik etkileri vardır:

> Bu doğrudan bir teknik anlamı vardır:

- En önemli bilgileri öncelikle verin (sistem süresi, kritik talimatlar)
  En önemli bilgiyi en önde koymak (system提示、关键指令)
- Geçerli soruyu ve en ilgili bağlamı sonuna koy (son zamanlarda önyargı yardımcı olur)
  Son olarak, son olarak, son olarak, son olarak, son olarak, son olarak, son olarak, son olarak, son olarak, son olarak, son olarak, son olarak, son olarak, son olarak, son olarak, son olarak, son olarak, son olarak, son olarak, son olarak, son olarak, son olarak, son olarak, son olarak, son olarak, son olarak, son olarak, son olarak, son olarak, son olarak, son olarak, son olarak, son olarak, son olarak, son olarak, son olarak, son olarak, son olarak, son olarak, son olarak, son olarak, son olarak, son olarak, son olarak, son olarak, son olarak, son olarak, son olarak, son olarak, son olarak, son olarak, son olarak, son olarak, son olarak, son olarak, son olarak, son olarak, son olarak, son olarak, son olarak, son olarak, son olarak, son olarak, son olarak, son olarak, son olarak, son olarak, son olarak,
- Konektsin ortasını en düşük öncelik alanı olarak değerlendirin
  Aşağıdaki orta bölgeyi en düşük öncelik alanı olarak görme
- Eğer orta tarafta bilgi eklemek istiyorsanız, son tarafta anahtar noktayı tekrarlayın.
  Eğer bir şey yapman gerekiyorsa, sonunda tekrar et.

```mermaid
graph LR
    subgraph Attention["Attention Distribution Across Context"]
        direction LR
        P1["Position 0-20%\nHIGH attention\n(system prompt)"]
        P2["Position 20-40%\nMODERATE"]
        P3["Position 40-70%\nLOW attention\n(lost in middle)"]
        P4["Position 70-90%\nMODERATE"]
        P5["Position 90-100%\nHIGH attention\n(current query)"]
    end

    style P1 fill:#51cf66,color:#000
    style P2 fill:#ffa500,color:#000
    style P3 fill:#ff6b6b,color:#fff
    style P4 fill:#ffa500,color:#000
    style P5 fill:#51cf66,color:#000
```

### Bağlantı bileşenleri

**System prompt**Claude Code, araç tanımlamaları ve davranış talimatları dahil olmak üzere sistem prompt'u için yaklaşık 6.000 token kullanır.

> **系统提示**: Setting persona、约束和行为规则──放最前面且跨轮次保持不变──Claude Code's system提示大约6,000 token,包含工具定义和行为指令──保持紧──系统提示中每个词在每次 API调用中重复──

**Tool definitions**Bu, bir iletişim kurmadan önce her bir işaretin 50-200 simgesini ekler. Dinamik araç seçimi - sadece mevcut sorguya ilişkin araçları dahil ederek - bu oranı %60-80 oranında azaltabilir.

> **工具定义**Her bir araç 50-200 simgelidir. Bu sayı, konuşma başlamadan önce kullanılmış 7.500 simge anlamına gelir.

**Retrieved context**Vectör veritabanından belgeler, arama sonuçları, dosya içeriği. Arama kalitesi doğrudan yanıt kalitesini belirler. Kötü bir arama hiçbir arama olmaktan daha kötüdür - pencereleri gürültüyle doldurur ve aktif olarak modelin yanıltıcı hale getiriyor.

> **检索上下文**Bu, bir dizi sorguya cevap vermenin en iyi yolu olduğunu gösterir.

**Conversation history**Bu, bir kullanıcı tarafından gönderilen bir mesajın ve yardımcı yanıtının öncesinde gerçekleşen bir mesajdır. Konuşma uzunluğu ile lineer olarak büyür.

> **对话历史**Tüm önceki kullanıcı mesajları ve yardımcı cevapları. %50 konuşma, %200'lik bir konuşma. %100'lik bir konuşma. %100'lik bir konuşma. %100'lik bir konuşma. %100'lik bir konuşma. %100'lik bir konuşma. %100'lik bir konuşma. %100'lik bir konuşma. %100'lik bir konuşma. %100'lik bir konuşma. %100'lik bir konuşma. %100'lik bir konuşma. %100'lik bir konuşma. %100'lik bir konuşma. %100'lik bir konuşma. %100'lik bir konuşma. %100'lik bir konuşma. %100'lik bir konuşma. %100'lik bir konuşma. %100'lik bir konuşma. %100'lik bir konuşma. %100'lik bir konuşma. %100'lik bir konuşma. %100'lik bir konuşma. %100'lik bir konuşma. %100'lik bir konuşma. %100'lik bir konuşma. %100'lik bir konuşma. %100'lik %100'lik bir konuşma. %100'lik %100'lik %100'lik %100'lik %100'lik %100'lik %100'lik %%%%%%%%%%'lik %%'lik %%'lik %%'lik %%'lik %%'lik %%'lik %%'lik %%'lik %%'lik %%'lik %%'lik %%'lik %'lik %'lik %'lik %'lik %'lik %'lik %'lik %'lik %'lik %'lik %'lik %'lik %'lik %'lik %'lik %'lik %'lik %'lik %'lik %'lik %'lik %'lik %'lik %'lik %'lik %'lik %'lik %'lik %'lik %'lik %'lik %'lik %'lik %'lik %'lik %'lik %'lik %'lik %'lik %'lik %'lik %'lik %'lik %'lik %'lik %'lik %'lik %'lik %'lik %'lik %'lik %'lik %'lik %'lik %'lik %'lik %'lik

**Few-shot examples**Bu nedenle, bu örnekler, bir dizi yönlendirme simgesinin içeriği ve çıkışını gösterir.

> **少样本示例**Gösterme: İsteyen davranışların giriş/çıktılarına karşı: 2-3 dikkatli seçilen örnekler genellikle binlerce tokenin emirlerini daha fazla çıkış kalitesini yükseltebilir.

**Generation budget**Modelin cevaplaması için rezerve edilen tokens. Kapasite penceresini doldurursanız, modelin cevap vermesi için yer yoktur.

> **生成预算**Modelle Response Reserve Tokens: Modelle Response Reserve Tokens: Modelle Response Reserve Tokens: Modelle Response Reserve Tokens: Modelle Reserve Tokens: Modelle Response Reserve Tokens: Modelle Reserve Tokens: Modelle Reserve Tokens: Modelle Response Reserve Tokens: Modelle Reserve Tokens: Modelle Reserve Tokens: Modelle Reserve Tokens: Modelle Reserve Tokens: Modelle Reserve Tokens: Modelle Reserve Tokens: Modelle Reserve Tokens: Modelle Reserve Tokens: Modelle Reserve Tokens: Modelle Reserve Tokens: Modelle Reserve Tokens: Modelle Reserve Tokens: Modelle Reserve Tokens: Modelle Reserve Tokens: Modelle Reserve Tokens: Modelle Reserve Tokens: Modelle Reserve Tokens: Modelle Reserve Tokens: Modelle Reserve Tokens: Modelle Reserve Tokens: Modelle Reserve Tokens: Modelle Reserve Tokens: Modelle Reserve Tokens: Modelle Reserve Tokens: Modelle Reserve Tokens: Modelle Reserve Tokens: Modelle Reserve Tokens: Modelle Reserve Tokens: Modelle Reserve Tokens: Modelle Reserve Tokens: Modelle Reserve Tokens: Modelle Reserve Tokens: Modelle Reserve Tokens: Modelle Reserve Tokens: Modelle Reserve Tokens: Modelle Reserve Tokens: Modelle Reserve Tokens: Modelle Reserve Tokens: Modelle Reserve Tokens: Modelle Reserve Tokens: Modelle Reserve Tokens: Modelle Reserve Tokens: Modelle Reserve Tokens: Models are used to generate to generate

### Konekst Sıkıştırma Stratejileri

**History summarization**Bu, "X'yi tartıştık, Y'yi karar verdik ve kullanıcı Z'yi istiyor" diyerek 100 tokenin yerine 2000 tokenin alınan 10 dönüşü değiştirir. Tarih bir eşiği aşırınca özetleme çalıştırın (örneğin, 5.000 token).

> **历史摘要**Bu nedenle, bu konudaki tüm değerler, "X" ile tartıştık, "Y" ile karar verdik, kullanıcı "Z" ile 100 token kullanmak istiyor.

**Relevance filtering**: her alınmış belgeyi mevcut sorguya göre değerlendirerek bir eşiğin altında bırakın. 10 parça alınır ama sadece 3 parça önemlidirse, diğerleri atın. 7. Ortalama 10'dan çok önemli olan 3 parça daha iyi.

> **相关性过滤**Bu nedenle, bu bilgiyi kullanmak için, bu bilgiyi kullanmak için, bu bilgiyi kullanmak için, bu bilgiyi kullanmak için kullanın.

**Tool pruning**Bu nedenle, bir kod sorusu için programlama araçları gerekmez. Bir programlama sorusu için dosya sistemleri araçları gerekmez. Bu, araç tanımlarını 8.000 tokenden 1.000'e düşürebilir.

> **工具裁剪**: 分类用户查询意图, yalnızca bu意图相关的工具包含──代码问题不需要日历工具──日程安排问题不需要文件系统工具──

**Recursive summarization**Bu nedenle, bir makaleyi oluşturmak için, bir makaleyi oluşturmak için, bir makaleyi oluşturmak için, bir makaleyi oluşturmak için, bir makaleyi oluşturmak için, bir makaleyi oluşturmak için, bir makaleyi oluşturmak için, bir makaleyi oluşturmak için, bir makaleyi oluşturmak için, bir makaleyi oluşturmak için, bir makaleyi oluşturmak için, bir makaleyi oluşturmak için, bir makaleyi oluşturmak için, bir makaleyi oluşturmak için, bir makaleyi oluşturmak için, bir makaleyi oluşturmak için, bir makaleyi oluşturmak için, bir makale oluşturmak için, bir makale oluşturmak için, bir makale oluşturmak için, bir makale oluşturmak için, bir makale oluşturmak için, bir makale oluşturmak için, bir makale oluşturmak için, bir makale oluşturmak için, bir makale oluşturmak için, bir makale oluşturmak için, bir makale oluşturmak için, bir makale oluşturmak için, bir makale oluşturmak için, bir makaleyi oluşturmak için, bir makaleyi oluşturmak için, bir makale, bir makaleyi oluşturmak için, bir makale, bir makale oluşturmak için, bir makale, bir makale oluşturmak için, bir makale, bir makale, bir makale oluşturmak için, bir makale, bir makale oluşturmak için, bir makale, bir makale, bir makale, bir makale, bir makale, bir makale, bir makale, bir makale, bir makale, bir makale, bir makale, bir makale, bir makale, bir makale, bir makale, bir makale, bir makale, bir makale, bir makale, bir makale, bir makale, bir makale, bir makale, bir makale, bir makale, bir makale, bir makale, bir makale, bir makale, bir makale, bir makale, bir makale, bir makale, bir makale, bir makale, bir makale, bir makale, bir makale, bir makale, bir makale, bir makale, bir makale, bir makale, bir makale, bir makale, bir makale, bir makale, bir makale, bir makale, bir makale, bir makale,

> **递归摘要**İlk bölüm, son kısım, son kısım, son kısım, son kısım, son kısım, son kısım, son kısım, son kısım, son kısım, son kısım, son kısım, son kısım, son kısım, son kısım, son kısım, son kısım, son kısım, son kısım, son kısım, son kısım, son kısım, son kısım, son kısım, son kısım, son kısım, son kısım, son kısım, son kısım, son kısım, son kısım, son kısım, son kısım, son kısım, son kısım, son kısım, son kısım, son kısım, son kısım, son kısım, son kısım, son kısım, son kısım, son kısım, son kısım, son kısım, son kısım, son kısım, son kısım, son kısım, son kısım, son kısım, son kısım, son kısım, son kısım, son kısım, son kısım, son kısım, son kısım, önemli noktalar,

### Hatırlama Sistemleri

Kontext mühendisliği üç zaman ufukuna uzanıyor.

> Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ünün Ün Ünün Ünün Ünün Ünün Ün Ünün Ünün Ünün Ünün Ünün Ünün Ün Ünün Ünün Ünün Ü Ü Ünün Ü Ü Ü Ü Ünün Ü Ü Ü Ü Ünün Ünün Ü Ü Ü Ü Ü Ünün

**Short-term memory**Bu, bir iletişim kuruluşu oluşturur.

> **短期记忆**:当前对话──直接存储在上下文窗中──随着每轮增长──通过摘要和截断管理──

**Long-term memory**"Kullanıcı TypeScript'i tercih eder". "Projen PostgreSQL kullanır". Bir veritabanında depolanır, oturum başlaması sırasında alınır. Claude Code bunu CLAUDE.md dosyalarında saklar. ChatGPT bunu bellek özelliğinde saklar.

> **长期记忆**:跨对话持久的事实和偏好──"user preference TypeScript──""项目用 PostgreSQL──"database内存,会话开始时检索──Claude Code 存在 CLAUDE.md 文件中──ChatGPT 存在其内存 功能中──

**Episodic memory**: ilgili olabilecek özel geçmiş etkileşimleri. "Geçen Salı, Auth modülünde benzer bir sorunu debugg ettik".

> **情景记忆**Bu nedenle, bu konularda, "bkz. "bu konularda, "bu konularda, "bu konularda, "bu konularda, "bu konularda, "bu konularda, "bu konularda, "bu konularda, "bu konularda, "bu konularda, "bu konularda, "bu konularda, "bu konularda, "bu konularda, "bu konularda, "bu konularda, "bu konularda, "bu konularda, "bu konularda, "bu konularda, "bu konularda, "bu konularda, "bu konularda, "bu konularda, "bu konularda, "bu konularda, "bu konularda, "bu konularda, "bu konularda, "bular" ve "bular" da "bular" da "bu konularda "bular" olarak adlandırılır.

```mermaid
graph TD
    subgraph Memory["Memory Architecture"]
        direction TB
        STM["Short-term Memory\n(current conversation)\nDirect in context window"]
        LTM["Long-term Memory\n(facts, preferences)\nDB -> retrieved on session start"]
        EM["Episodic Memory\n(past interactions)\nEmbeddings -> retrieved on similarity"]
    end

    Q["Current Query"] --> STM
    Q --> LTM
    Q --> EM

    STM --> CW["Context Window"]
    LTM --> CW
    EM --> CW

    style STM fill:#1a1a2e,stroke:#51cf66,color:#fff
    style LTM fill:#1a1a2e,stroke:#0f3460,color:#fff
    style EM fill:#1a1a2e,stroke:#e94560,color:#fff
    style CW fill:#1a1a2e,stroke:#ffa500,color:#fff
```

### Dinamik Konekst Meclisi

Anahtar anlayış: farklı sorguların farklı bağlamlara ihtiyacı vardır. Bir statik sistem prompt + statik araçlar + statik geçmiş harcama olur. En iyi sistemler her sorguya dinamik olarak bağlam oluşturur.

> 关键洞察:不同查询需要不同上下文──静态系统提示 + 静态工具 + 静态历史是浪费──最好的系统按查询动态组装上下文──

1. Sorgu niyetini sınıflandır
   Sorgulama İstihbaratı
2. İlgili araçları seçin (bütün araçlar değil)
   选择相关工具(不是全部工具)
3. İlgili belgeler (sıkı bir set değil)
   检索相关文档(不是固定集合)
4. Önemli tarih dönümleri dahil edin (bütün tarih değil)
   包含相关历史轮次(不是全部历史)
5. Görev türüne uyan birkaç çekim örneğini ekle
   Görev türüne uygun küçük örnek örnekleri eklenir
6. Her şeyi önemle sıralayın: önce kritik, sonra önemli, ortada seçeneği.
   按重要性排序:关键在前、重要在后、可选在中间

Bu, iyi bir AI uygulamasını harika bir uygulamadan ayıran şeydir.

> Bu, iyi bir AI uygulaması ve üstün bir AI uygulaması arasındaki farkın anahtarıdır.

## Yapın.
```figure
lost-in-the-middle
```

## Yapın

### Adım 1: İşaret Sayıcı

Ölçemeyeceğiniz şeyi bütçe edemezsiniz. Basit bir token sayıcısı oluşturun (beyaz alan bölümü kullanarak yaklaşım, çünkü tam sayım tokenizer'e bağlıdır).

> Yetersiz bir şey için bütçe yapamazsınız. (Büyük bir simge hesaplayıcıyı inşa edin.)

```python
import json
import numpy as np
from collections import OrderedDict

def count_tokens(text):
    if not text:
        return 0
    return int(len(text.split()) * 1.3)

def count_tokens_json(obj):
    return count_tokens(json.dumps(obj))
```

### Adım 2: Bağlantı bütçe yöneticisi

Bir bütçe yöneticisi her bileşenin kaç tane tokeni kullandığını takip eder ve sınırları uyguluyor.

> 核心抽象──预算管理器 追踪每个组件使用多少代币 并强限制制──

```python
class ContextBudget:
    def __init__(self, max_tokens=128000, generation_reserve=4000):
        self.max_tokens = max_tokens
        self.generation_reserve = generation_reserve
        self.available = max_tokens - generation_reserve
        self.allocations = OrderedDict()

    def allocate(self, component, content, max_tokens=None):
        tokens = count_tokens(content)
        if max_tokens and tokens > max_tokens:
            words = content.split()
            target_words = int(max_tokens / 1.3)
            content = " ".join(words[:target_words])
            tokens = count_tokens(content)

        used = sum(self.allocations.values())
        if used + tokens > self.available:
            allowed = self.available - used
            if allowed <= 0:
                return None, 0
            words = content.split()
            target_words = int(allowed / 1.3)
            content = " ".join(words[:target_words])
            tokens = count_tokens(content)

        self.allocations[component] = tokens
        return content, tokens

    def remaining(self):
        used = sum(self.allocations.values())
        return self.available - used

    def utilization(self):
        used = sum(self.allocations.values())
        return used / self.max_tokens

    def report(self):
        total_used = sum(self.allocations.values())
        lines = []
        lines.append(f"Context Budget Report ({self.max_tokens:,} token window)")
        lines.append("-" * 50)
        for component, tokens in self.allocations.items():
            pct = tokens / self.max_tokens * 100
            bar = "#" * int(pct / 2)
            lines.append(f"  {component:<25} {tokens:>6} tokens ({pct:>5.1f}%) {bar}")
        lines.append("-" * 50)
        lines.append(f"  {'Used':<25} {total_used:>6} tokens ({total_used/self.max_tokens*100:.1f}%)")
        lines.append(f"  {'Generation reserve':<25} {self.generation_reserve:>6} tokens")
        lines.append(f"  {'Remaining':<25} {self.remaining():>6} tokens")
        return "\n".join(lines)
```

### Adım 3: Ortalık Kayıp Düzenleme

Yeniden düzenleme stratejisini uygulayın: en önemli konular önce ve sonuncu, en az önemli konular orta.

> 实现重排策略:最重要项目放最前和最后,最不重要项目放中──

```python
def reorder_lost_in_middle(items, scores):
    paired = sorted(zip(scores, items), reverse=True)
    sorted_items = [item for _, item in paired]

    if len(sorted_items) <= 2:
        return sorted_items

    first_half = sorted_items[::2]
    second_half = sorted_items[1::2]
    second_half.reverse()

    return first_half + second_half

def score_relevance(query, documents):
    query_words = set(query.lower().split())
    scores = []
    for doc in documents:
        doc_words = set(doc.lower().split())
        if not query_words:
            scores.append(0.0)
            continue
        overlap = len(query_words & doc_words) / len(query_words)
        scores.append(round(overlap, 3))
    return scores
```

### Adım 4: Konuşma Tarihi Kompresörü

Eski konuşmayı özetleyerek, para kazanmak için bir devreye dönüşüyor.

> 总结旧对话轮次以收藏标志 预算。

```python
class ConversationManager:
    def __init__(self, max_history_tokens=5000):
        self.turns = []
        self.summaries = []
        self.max_history_tokens = max_history_tokens

    def add_turn(self, role, content):
        self.turns.append({"role": role, "content": content})
        self._compress_if_needed()

    def _compress_if_needed(self):
        total = sum(count_tokens(t["content"]) for t in self.turns)
        if total <= self.max_history_tokens:
            return

        while total > self.max_history_tokens and len(self.turns) > 4:
            old_turns = self.turns[:2]
            summary = self._summarize_turns(old_turns)
            self.summaries.append(summary)
            self.turns = self.turns[2:]
            total = sum(count_tokens(t["content"]) for t in self.turns)

    def _summarize_turns(self, turns):
        parts = []
        for t in turns:
            content = t["content"]
            if len(content) > 100:
                content = content[:100] + "..."
            parts.append(f"{t['role']}: {content}")
        return "Previous: " + " | ".join(parts)

    def get_context(self):
        parts = []
        if self.summaries:
            parts.append("[Conversation Summary]")
            for s in self.summaries:
                parts.append(s)
        parts.append("[Recent Conversation]")
        for t in self.turns:
            parts.append(f"{t['role']}: {t['content']}")
        return "\n".join(parts)

    def token_count(self):
        return count_tokens(self.get_context())
```

### Adım 5: Dinamik Araç Seçicisi

Sadece mevcut sorguya ilişkin araçları ekleyin.

> Sadece mevcut sorgu ile ilgili araçları içerir.

```python
TOOL_REGISTRY = {
    "read_file": {
        "description": "Read contents of a file",
        "tokens": 120,
        "categories": ["code", "files"],
    },
    "write_file": {
        "description": "Write content to a file",
        "tokens": 150,
        "categories": ["code", "files"],
    },
    "search_code": {
        "description": "Search for patterns in codebase",
        "tokens": 130,
        "categories": ["code"],
    },
    "run_command": {
        "description": "Execute a shell command",
        "tokens": 140,
        "categories": ["code", "system"],
    },
    "create_calendar_event": {
        "description": "Create a new calendar event",
        "tokens": 180,
        "categories": ["calendar"],
    },
    "list_emails": {
        "description": "List recent emails",
        "tokens": 160,
        "categories": ["email"],
    },
    "send_email": {
        "description": "Send an email message",
        "tokens": 200,
        "categories": ["email"],
    },
    "web_search": {
        "description": "Search the web for information",
        "tokens": 140,
        "categories": ["research"],
    },
    "query_database": {
        "description": "Run a SQL query on the database",
        "tokens": 170,
        "categories": ["code", "data"],
    },
    "generate_chart": {
        "description": "Generate a chart from data",
        "tokens": 190,
        "categories": ["data", "visualization"],
    },
}

def classify_intent(query):
    query_lower = query.lower()

    intent_keywords = {
        "code": ["code", "function", "bug", "error", "file", "implement", "refactor", "debug", "test"],
        "calendar": ["meeting", "schedule", "calendar", "appointment", "event"],
        "email": ["email", "mail", "send", "inbox", "message"],
        "research": ["search", "find", "what is", "how does", "explain", "look up"],
        "data": ["data", "query", "database", "chart", "graph", "analytics", "sql"],
    }

    scores = {}
    for intent, keywords in intent_keywords.items():
        score = sum(1 for kw in keywords if kw in query_lower)
        if score > 0:
            scores[intent] = score

    if not scores:
        return ["code"]

    max_score = max(scores.values())
    return [intent for intent, score in scores.items() if score >= max_score * 0.5]

def select_tools(query, token_budget=2000):
    intents = classify_intent(query)
    relevant = {}
    total_tokens = 0

    for name, tool in TOOL_REGISTRY.items():
        if any(cat in intents for cat in tool["categories"]):
            if total_tokens + tool["tokens"] <= token_budget:
                relevant[name] = tool
                total_tokens += tool["tokens"]

    return relevant, total_tokens
```

### Adım 6: Tam Konekst Meclis Boru hattı

Bir soruyu vererek, optimum bağlamı dinamik bir şekilde birleştirin.

> Her şeyi topla. Soru sor.

```python
class ContextEngine:
    def __init__(self, max_tokens=128000, generation_reserve=4000):
        self.budget = ContextBudget(max_tokens, generation_reserve)
        self.conversation = ConversationManager(max_history_tokens=5000)
        self.system_prompt = (
            "You are a helpful AI assistant. You have access to tools for "
            "code editing, file management, web search, and data analysis. "
            "Use the appropriate tools for each task. Be concise and accurate."
        )
        self.knowledge_base = [
            "Python 3.12 introduced type parameter syntax for generic classes using bracket notation.",
            "The project uses PostgreSQL 16 with pgvector for embedding storage.",
            "Authentication is handled by Supabase Auth with JWT tokens.",
            "The frontend is built with Next.js 15 using the App Router.",
            "API rate limits are set to 100 requests per minute per user.",
            "The deployment pipeline uses GitHub Actions with Docker multi-stage builds.",
            "Test coverage must be above 80% for all new modules.",
            "The codebase follows the repository pattern for data access.",
        ]

    def assemble(self, query):
        self.budget = ContextBudget(self.budget.max_tokens, self.budget.generation_reserve)

        system_content, _ = self.budget.allocate("system_prompt", self.system_prompt, max_tokens=1000)

        tools, tool_tokens = select_tools(query, token_budget=2000)
        tool_text = json.dumps(list(tools.keys()))
        tool_content, _ = self.budget.allocate("tools", tool_text, max_tokens=2000)

        relevance = score_relevance(query, self.knowledge_base)
        threshold = 0.1
        relevant_docs = [
            doc for doc, score in zip(self.knowledge_base, relevance)
            if score >= threshold
        ]

        if relevant_docs:
            doc_scores = [s for s in relevance if s >= threshold]
            reordered = reorder_lost_in_middle(relevant_docs, doc_scores)
            doc_text = "\n".join(reordered)
            doc_content, _ = self.budget.allocate("retrieved_context", doc_text, max_tokens=3000)

        history_text = self.conversation.get_context()
        if history_text.strip():
            history_content, _ = self.budget.allocate("conversation_history", history_text, max_tokens=5000)

        query_content, _ = self.budget.allocate("user_query", query, max_tokens=500)

        return self.budget

    def chat(self, query):
        self.conversation.add_turn("user", query)
        budget = self.assemble(query)
        response = f"[Response to: {query[:50]}...]"
        self.conversation.add_turn("assistant", response)
        return budget


def run_demo():
    print("=" * 60)
    print("  Context Engineering Pipeline Demo")
    print("=" * 60)

    engine = ContextEngine(max_tokens=128000, generation_reserve=4000)

    print("\n--- Query 1: Code task ---")
    budget = engine.chat("Fix the bug in the authentication module where JWT tokens expire too early")
    print(budget.report())

    print("\n--- Query 2: Research task ---")
    budget = engine.chat("What is the best approach for implementing vector search in PostgreSQL?")
    print(budget.report())

    print("\n--- Query 3: After conversation history builds up ---")
    for i in range(8):
        engine.conversation.add_turn("user", f"Follow-up question number {i+1} about the implementation details of the system")
        engine.conversation.add_turn("assistant", f"Here is the response to follow-up {i+1} with technical details about the architecture")

    budget = engine.chat("Now implement the changes we discussed")
    print(budget.report())

    print("\n--- Tool Selection Examples ---")
    test_queries = [
        "Fix the bug in auth.py",
        "Schedule a meeting with the team for Tuesday",
        "Show me the database query performance stats",
        "Search for best practices on error handling",
    ]

    for q in test_queries:
        tools, tokens = select_tools(q)
        intents = classify_intent(q)
        print(f"\n  Query: {q}")
        print(f"  Intents: {intents}")
        print(f"  Tools: {list(tools.keys())} ({tokens} tokens)")

    print("\n--- Lost-in-the-Middle Reordering ---")
    docs = ["Doc A (most relevant)", "Doc B (somewhat relevant)", "Doc C (least relevant)",
            "Doc D (relevant)", "Doc E (moderately relevant)"]
    scores = [0.95, 0.60, 0.20, 0.80, 0.50]
    reordered = reorder_lost_in_middle(docs, scores)
    print(f"  Original order: {docs}")
    print(f"  Scores:         {scores}")
    print(f"  Reordered:      {reordered}")
    print(f"  (Most relevant at start and end, least relevant in middle)")
```

## Çerçeveyi kullanın.

### Harness Yönetilen Koneks

Claude Code, katmanlı bir yaklaşım ile bağlamı yönetir. Sistem prompt'unda davranış kuralları ve araç tanımları (~ 6K jetonları) bulunur. Bir dosyayı açtığınızda, içeriği bağlam olarak enjekte edilir. Aradığınızda, sonuçlar eklenir. Eski konuşma dönümleri özetlenir. CLAUDE.md, oturuluklar boyunca devam eden uzun vadeli bellek sağlar.

> Claude Code kullanılarak farklı yöntemi yönetim üzerinde aşağı yukarı. Sistem önerileri içerir davranış kuralları ve araç tanımlamaları.

Ana mühendislik kararı: Claude Code tüm kod tabanınızı bağlamda atmaz. İsteğe bağlı dosyaları geri alır. Bu pratikte bağlam mühendisliği.

> Key Engineering Decision:Claude Code Not Putting the Whole Code Library into the following. Bu, aşağıdaki yazılardaki uygulamaların bir parçasıdır.

### Cursor'un Dinamik Konekst yüklemesi
### Dinamik Konekst yükleme

Cursor tüm kod tabanınızı yerleşimlere indexe eder. Bir sorgu yazdığınızda, vektör benzerliği kullanarak en ilgili dosyaları ve kod bloklarını geri alır. Sadece bu parçalar bağlam penceresine girer. 500K satırlı bir kod tabanı en ilgili 5-10 kod bloğuna sıkıştırılır.

> Cursor tüm kod kutubu indeksini yerleştirir. Giriş sorgularında, en ilgili dosyaları ve kod bloklarını ve en ilgili kod bloklarını ve en çok ilgili kod kutularını ve en çok ilgili kod kutularını bulmaya çalışır.

Bu bir örnektir: her şeyi yerleştir, talep üzerine geri alın, sadece önemli olanları ekleyin.

> İşte bu şekilde: her şeyi, gerekçeye göre, sadece önemli olanı içerir.

### ChatGPT hafızası
### Uzun vadeli hafıza yardımcıları

ChatGPT, kullanıcı tercihlerini ve gerçekleri uzun süreli hafıza olarak kaydediyor. Her konuşma başlatıldığında ilgili hatıralar alınır ve sistem uyarısına dahil edilir. "Kullanıcı Python'ı tercih eder" 5 token maliyetini alır, ancak konuşmalar boyunca tekrarlanan talimatların yüzlerce tokenini kaydeder.

> ChatGPT, kullanıcı tercihlerini ve gerçeklerini uzun süreli hafıza olarak depolar. Her konuşma başladığında, ilgili hafızalar kontrol edilir ve sistem önerilerinde yer alır.

### RAG Konekts Mühendisliği

Retrieval-Augmented Generation, bağlam mühendisliği resmileştirilmiştir. Bilgiyi modelin ağırlıklarına (öğrenme) veya sistem uyarısına (statik bağlam) doldurmak yerine, sorgu zamanında ilgili belgeler alıyorsunuz ve bağlam penceresine enjekte ediyorsunuz. RAG'in tüm hattı - parçalanma, yerleştirme, çekim, yeniden sıralama - bir sorunu çözmek için var: doğru bilgileri bağlam penceresine koymak.

> 检索增强生成是上下文工程的形式化──不把知识塞进模型权重 (重量) 训练) 或系统提示 (系统提示) ),而在查询时检索相关文档并注入上下文窗口──整个RAG管线分块、嵌入、检索、重排存在就是为了解决一个问题:把正确信息放入上下文窗口──

## İndirin . Ürünler .

Bu ders bize çok yararlı .`outputs/prompt-context-optimizer.md`-- bir bağlam birimliği stratejisini denetleyen ve optimize etme önerisi veren tekrar kullanılabilir bir istatistik. Sistem istatistiklerini, araç sayısını, ortalama tarih uzunluğunu ve geri alma stratejisini besle ve token atıklarını belirle ve geliştirmeler önerir.

> 本课产 出 `outputs/prompt-context-optimizer.md`                                                                                                                                                                                                                                                              

Ayrıca üretir `outputs/skill-context-engineering.md`-- görev türüne, bağlam penceresinin boyutuna ve gecikme bütçesine göre bağlam birimleri borularını tasarlamak için bir karar çerçevesini.

> Aynı zamanda üretim `outputs/skill-context-engineering.md` Görev türüne dayanan, üst ve aşağıdaki çerçeve büyüklüğü ve gecikme bütçe tasarımı üst ve aşağıdaki çerçeve yapılandırma hattı karar çerçevesidir.

## Egzersizler.

1. ContextBudget sınıfına "token waste detector" ekleyin.Budjetin %30'undan fazla kullanan bileşenleri işaretlemeli ve her bileşen türüne özel sıkıştırma stratejilerini önermelidir (tarihi özetlemek, kesme araçları, belgeleri yeniden sıralamak).
   Bu nedenle, bu programın başlıklı bir programı oluşturmak için, bu programın başlıklı bir programı oluşturmak ve bu programın başlıklı bir programı oluşturmak için gerekli düzenlemeleri yapılması gerekmektedir.

2. Arayan bağlam için semantik deduplasyon uygulayın. Eğer iki alınmış belge %80'den fazla benzerse (söz üst üstelik veya gömülmelerinin cosine benzerliği ile), sadece daha yüksek puan alan bir belgeyi tutun. Bu belge bütçesinin ne kadar geri kazanıldığını ölçün.
   实现检索上下文的语义去重──若两个检索文档超过80%相似之分重叠或嵌入余弦相似度), yalnızca daha yüksek 分数保留──测量

3. "Sonuç tekrarlama" aracı oluşturun. Bir konuşma transkripti verildiğinde, onu ContextEngine üzerinden tekrar oynatın ve bütçe tahsisinin nasıl değişeceğini görselleştirin. Zamanla bileşen başına token kullanımını çizin. Sunuç sıkıştırılmaya başladığı sırayı tanımlayın.
   Bu nedenle, bu programın bir sonraki bölümünü oluşturmak için, bir sonraki bölümünü oluşturmak için, bir sonraki bölümünü oluşturmak için, bir sonraki bölümünü oluşturmak için, bir sonraki bölümünü oluşturmak için, bir sonraki bölümünü oluşturmak için, bir sonraki bölümünü oluşturmak için, bir sonraki bölümünü oluşturmak için, bir sonraki bölümünü oluşturmak için, bir sonraki bölümünü oluşturmak için, bir sonraki bölümünü oluşturmak için, bir sonraki bölümünü oluşturmak için, bir sonraki bölümünü oluşturmak için, bir sonraki bölümünü oluşturmak için, bir sonraki bölümünü oluşturmak için, bir sonraki bölümünü oluşturmak için, bir sonraki bölümünü oluşturmak için, bir sonraki bölümünü oluşturmak için, bir sonraki bölümünü oluşturmak için, bir sonraki bölümünü oluşturmak için, bir sonraki bölümünü oluşturmak için, bir sonraki bölümünü oluşturmak için, bir sonraki bölümünü oluşturmak için, bir sonraki bölümünü oluşturmak için, bir sonraki bölümünü oluşturmak için, bir sonraki bölümünü oluşturmak için, bir sonraki bölümünü oluşturmak için, bir sonraki bölümünü oluşturmak için, bir sonraki bölümünü oluşturmak için, bir diğer bölümünü oluşturmak için, bir bölümünü oluşturmak için, bir bölümünü oluşturmak için, bir bölümünü oluşturmak için, bir bölümünü oluşturmak için, bir bölümünü oluşturmak için, bir bölümünü oluşturmak için, bir bölümünü oluşturmak için, bir bölümünü oluşturmak için, bir bölümünü oluşturmak için,

4. Önceliklere dayalı bir araç seçicisi uygulayın. İkili ekle/ekle yerine, her bir araçla mevcut soruya bir bağlayıcılık puanı tahsis edin. Araç bütçesi bitene kadar aşağıdaki bağlayıcılık sırasıyla araçları ekleyin. Ödev performansını 5, 10, 20 ve 50 araçla karşılaştırın.
   Bu, bir araçın 5,10,2050 araç zamanındaki görev performansını oluşturur.

5. Çok strateji bağlamlı bir kompresör oluşturun. Üç kompresyon stratejisini uygulayın (kısaltma, özetleme, anahtar cümlelerin çıkarılması) ve 20 belge üzerinde bir referans çizin. Kompresyon oranı ve bilgi saklama arasındaki karıştırmayı ölçün (kompresyon versiyonunda hala sorunun cevabı var mı?).
   构建多策略上下文压缩机. 实现三种压缩策略. 截断,摘要,关键句提取) 基准测试. 基准测试. 基准测试. 基准测试. 基准测试. 基准测试. 基准测试. 基准测试. 基准测试. 基准测试. 基准测试. 基准测试. 基准测试. 基准测试. 基准测试. 基准测试. 基准测试. 基准测试. 基准测试. 基准测试. 基准测试. 基准测试. 基准测试. 基准测试. 基准测试. 基准测试. 基准测试. 基准测试. 基准测试. 基准测试. 基准测试. 基准测试. 基准测试. 基准测试. 基准测试. 基准测试. 基准测试. 基准测试. 

## Anahtar Şartlar .

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|----------------------|---------|
| Context window | "How much the model can read" | The maximum number of tokens (input + output) the model processes in a single forward pass -- 400K for GPT-5, 200K (1M beta) for Claude Opus 4.7, 2M for Gemini 3 Pro | 上下文窗口：模型单次前向传播处理的最大 token 数（输入+输出）|
| Context engineering | "Advanced prompt engineering" | The discipline of deciding what goes into the context window, in what order, and at what priority -- encompasses retrieval, compression, tool selection, and memory management | 上下文工程：决定什么进入上下文窗口、什么顺序、什么优先级的学科——包含检索、压缩、工具选择、记忆管理 |
| Lost-in-the-middle | "Models forget stuff in the middle" | Empirical finding that LLMs attend better to the beginning and end of context, with 10-20% accuracy drop for information placed in the middle | 中间丢失：LLM 对上下文开头和结尾注意力更好的实证发现；中间位置准确率下降 10-20% |
| Token budget | "How many tokens you have left" | An explicit allocation of context window capacity across components (system prompt, tools, history, retrieval, generation) with per-component limits | token 预算：跨组件的上下文窗口容量显式分配（系统提示、工具、历史、检索、生成）带每组件限制 |
| Dynamic context | "Loading stuff on the fly" | Assembling the context window differently for each query based on intent classification, relevant tool selection, and retrieval results | 动态上下文：基于意图分类、相关工具选择和检索结果，为每个查询不同地组装上下文窗口 |
| History summarization | "Compressing the conversation" | Replacing verbatim old conversation turns with a concise summary, reducing token cost while preserving key information | 历史摘要：用简洁摘要替代逐字旧对话轮次，减少 token 成本同时保留关键信息 |
| Tool pruning | "Only including relevant tools" | Classifying query intent and only including tool definitions that match, reducing tool token cost by 60-80% | 工具裁剪：分类查询意图只包含匹配的工具定义，减少工具 token 成本 60-80% |
| Long-term memory | "Remembering across sessions" | Facts and preferences stored in a database and retrieved at session start -- CLAUDE.md, ChatGPT Memory, and similar systems | 长期记忆：跨会话存储在数据库并在会话开始时检索的事实和偏好——CLAUDE.md、ChatGPT Memory 等 |
| Episodic memory | "Remembering specific past events" | Past interactions stored as embeddings and retrieved when the current query is similar to a past conversation | 情景记忆：作为嵌入存储的过去交互，当前查询相似时检索 |
| Generation budget | "Room for the answer" | Tokens reserved for the model's output -- if the context fills the window completely, the model has no room to respond | 生成预算：为模型输出保留的 token——若上下文填满窗口，模型没有空间响应 |

## Daha fazla okumak

- [Liu et al., 2023 -- "Lost in the Middle: How Language Models Use Long Contexts"](https://arxiv.org/abs/2307.03172)-- pozisyon bağımlılığı üzerine yapılan kesin çalışma, modellerin uzun bağlamlar ortasında bilgiyle mücadele ettiğini göstermektedir.
  Liu 等, "Lost in the Middle" (Yoklanmak Ortalama)  Position Related Attention'ın otoriterlik araştırması, modelin uzun üzerinde aşağıdaki ortamdaki bilgiyi işlemekte zor olduğunu göstermektedir.
- [Anthropic's Contextual Retrieval blog post](https://www.anthropic.com/news/contextual-retrieval)-- Anthropic'in bağlamdan haberdar parçaları nasıl bulduğunu, bu da %49'a düşmüş bir geri alım başarısızlığı
  Antropik 上下文检索博客Antropik  nasıl işleyeceğiniz aşağıdaki hissedecek blokların araması, aramanın başarısızlığı %49 oranında azalır
- [Simon Willison's "Context Engineering"](https://simonwillison.net/2025/Jun/27/context-engineering/)- ...diplinin adını veren ve onu hızlı mühendislikten ayıran blog yazısı
  Simon Willison'un "Kontext Mühendisliği" adlı bölümünü, öneriler mühendisliği ile ayırt edilemez.
- [LangChain documentation on RAG](https://python.langchain.com/docs/tutorials/rag/)-- Çıkarma artıran jenerasyonun bağlam mühendisliği örneği olarak pratik uygulanması
  LangChain RAG 文档 , aşama aşamasında kullanılan bir çalışma modunun pratik gerçekleşmesi olarak arşiv güçlendirme üretimi yapacaktır
- [Greg Kamradt's Needle in a Haystack test](https://github.com/gkamradt/LLMTest_NeedleInAHaystack)-- tüm büyük modellerde konumlara bağlı olarak alınma başarısızlıklarını ortaya koyan referans değer
  Greg Kamradt'in büyük denizde bir tıklama testi tüm başlıca modellerin konumları ortaya çıkardı
- [Pope et al., "Efficiently Scaling Transformer Inference" (2022)](https://arxiv.org/abs/2211.05102)-- bağlam uzunluğu hafıza ve gecikme sürüşünü neden değiştirir ve KV önbelleği, MQA ve GQA bütçe hesaplamasını nasıl değiştirir.
  Pope等, "Effificiently Scaling Transformer Inference" (Effificiently Scaling Transformer Inference) 为何上下文长度驱动内存和延迟,以及 KV cache、MQA、GQA 如何改变预算计算──
- [Agrawal et al., "SARATHI: Efficient LLM Inference by Piggybacking Decodes with Chunked Prefills" (2023)](https://arxiv.org/abs/2308.16369)-- TTFT'de uzun çağrıları pahalı yapan iki sonucu aşamaları, TPOT'de ucuz olan; bağlam içeren pazarlamaların arkasındaki temel gerçek.
  Agrawal 等, "SARATHI" (Yaratılı)                                                                                                                                                                                                                                                        
- [Ainslie et al., "GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints" (EMNLP 2023)](https://arxiv.org/abs/2305.13245)-- üretim dekodörlerinde kalite kaybı olmadan KV hafızasını 8x kesen gruplanmış sorgu dikkat kağıdı.
  Ainslie 等, "GQA" ((EMNLP 2023) 分组查询注意力论文, in production decoder will KV in storage reduced 8 times and no quality loss;;
