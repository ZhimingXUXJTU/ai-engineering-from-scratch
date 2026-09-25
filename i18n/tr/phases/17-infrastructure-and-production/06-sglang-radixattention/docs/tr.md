# SGLang ve RadixKartesi Ağır İş yükleri için dikkat
# Önbellek Servisleri  RadixAtention ve KV Reuse

> KV önbelleğini bir kök ağacında saklanan birinci sınıf, tekrar kullanılabilir bir kaynak olarak ele alın ve programlama değişiklikleri onunla birlikte yapın: FCFS (birincil gelen, ilk hizmet verilen) yerine vLLM programları olarak, bir önbelleğe uyan bir planlamacı daha uzun paylaşılmış önlüklerle yapılan istekleri öncelikli hale getirir  etkili bir derinlik-birincil kök geçiş böylece sıcak dallar HBM'de oturuyor kalır. SGLang, bu fikri destekleyen motor. ShareGPT gibi 1K istekleri ile Llama 3.1 8B'de, SGLang ~ 16.200 tok/s'e ~ 12.500 vLLM'ye ulaşır, %29 bir kenar. Önceden ağır RAG iş yüklerinde avantaj 6.4x'e ulaşır. Ses klonlama şeklinde iş yükleri üzerinde cache trafiği oranı %86 arttı. 2026 yılında xAI, LinkedIn, Cursor, Oracle, GCP, Azure, AWS'de 400.000+ GPU'da dağıtıldı. 6.4x numarası, ön işaret siparişleri tutarlı olmadığı zaman buharlaşır.

> **【中文解读】**Bu bölüm SGLang ve RadixAttention'ı tanıttı.
**Type:** Learn
**Languages:** Python (stdlib, toy radix-tree cache + cache-aware scheduler)
**Prerequisites:** Phase 17 · 04 (Serving Engine Internals), Phase 14 (Agentic RAG)
**Time:** ~75 minutes


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy radix-tree cache + cache-aware scheduler) | **语言:** Python（标准库，radix tree 缓存 + 缓存感知调度器模拟）
**Prerequisites:** Phase 17 · 04 (vLLM Serving Internals), Phase 14 (Agentic RAG) | **前置知识:** Phase 17 · 04（vLLM 服务内部）, Phase 14（Agentic RAG）

>  **【前置】**学本节前 請先掌握:Phase 17·04(vLLM) 、Phase 14(Agentic RAG) ・・・SGLang Radiks ağacı kullan 復用 KV cache比 vLLM FCFS 更智能的调度。
>  **【类比】**SGLang RadixAttention = "gütüphanelerden hatırlama"──vLLM = 每次重新查目录;SGLang = 热门前(系统提示+RAG bağlamı)存 radix tree 复用──Llama 3.1 8B 在 ShareGPT 上比 vLLM 快 29%;RAG 工作负载快 6.4 倍;语音克隆场景缓存命中 86%──2026 部署在40万+ GPU(xAI、LinkedIn、Cursor)──关键:前必须稳定排序才有效────
**Time:** ~75 minutes | **时间:** ~75 分钟

## Öğrenme hedefleri

- Diyar Radix Dikkat: bir radix ağacında önlüklerin nasıl depolandığı ve KV bloklarının aynı dalda kökleşmiş diziler arasında nasıl paylaşıldığı.
  Çinçe Çevirim: Çizim Radiks Dikkat:前 nasıl in radix ağacı 中存储,KV 块 nasıl in同分支的序列间共享──
- Önbellek farkında olan programlama ve neden FCFS'in ağır trafik için yanlış olduğunu açıklayın.
  Çinçe çevirisi: Kaşınma algılama düzenini açıklamak ve neden FCFS'in önde gelen yoğun akışın yanlış olduğunu açıklamak.
- Önbellek-cache hit hızı ve hızlı uzunluk dağılımını vererek bir iş yükü için beklenen hızlandırmayı hesaplayın.
  Çinçe çevirisi: given determination 缓存命中率和快速 长度分布,计算工作负载的预期加速──
- 6.4x sayısını gerçekleştirecek bir hızlandırma disiplini adını verin.
  Çinçe Çevirisi:                                                                                                                                                                                                                                                            

## Sorunlar. Sorunlar.

> **【中文解读】**传统推理服务将每个请求的提示视为不透明即使5000个RAG 请求共享相同2000代币 系统提示,vLLM也将执行5000次完整的预填――RadixAttention 通过将代币序列存储在radix tree 中解决这个问题: 新请求沿树匹配已有前,只需预填 新增的后部分──挑战在调度FCFS先来先服务) 破坏前局部性,需要缓存意识调度器优先服务共享前的请求──

> **【拓展：前缀共享在 Agent 场景的价值】**Agent 工作负载天然具有前共享特征:系统提示、工具 schema、少数shot示例、对话历史跨请求重复──Cursor(AI 代码编辑器) 2026 yılında Rapor Agent 调用中系统提示 + 工具定义占即时的80% , yalnızca kullanıcı sorgu bölümünün farklılıkları vardır.

Klasik servis, her talebin istekini açık olmayan bir şekilde değerlendirir. 5.000 RAG istekinin hepsi aynı 2.000 token sistem istekinin yanı sıra aynı kurtarma preamblesinden başladığında bile, vLLM, 2.000 token önlüğünü 5.000 kez doldurur. GPU aynı işi tekrar yapar.

> 经典服务将每请求的快速 视为不透明的──即使5000个RAG请求都以相同的2000个代币 系统提示加相同检索前开始,vLLM也会预填充那2,000个代币前 5,000次──GPU 重复做同样的工作──

Gözetim: agentic ve RAG iş yüklerinde istekler neredeyse her zaman uzun önlükleri paylaşır. Sistem istekleri, araç şemeleri, birkaç çekim örneği, çekim başlıkları, sohbet geçmişi  tüm istekler boyunca tekrarlanır. Eğer KV önlükleri için bir kez sakladığınız ve tekrar kullandığınızda, tekrar doldurmazsınız.

> 观察:Agent 和 RAG 工作负载中的提示 几乎总是共享长前──系统提示、工具方案、少数shot示例、检索头、对话历史都在请求间重复── Eğer bir kez önce KV 缓存并复用,就不需要再预填──

RadixAttention tam olarak bunu yapar. Tokenler bir radix ağacında indekslenir; her düğüm kökten yolundaki token dizisi için KV bloklarına sahiptir. Yeni bir talep ağacı yürür: token eşleşen herhangi bir düğüm, nodun KV bloklarını tekrar kullanır. Ön doldurma maliyeti tam isteklenme değil, "yeni" sufiksine orantılı hale gelir.

> RadixAttention 正正是这样做──Token 在 radix tree 中索引; her nodet root to this pathway's token 序列's KV 块──新请求遍历树: herhangi bir token 匹配的节点复用该节点的 KV 块──预填成本与"新"后成正比,而不是完整的提示──

İki istek 2000 tokenlik bir önbölü paylaşırsa ve üçüncü bir de aynı önbölü sadece 200 token paylaşırsa, uzun paylaşılmış iki istekleri birlikte hizmet etmek istersiniz, böylece uzun önbölü HBM'de kalır. FCFS tersini yapar  ilk gelen herkese hizmet eder, potansiyel olarak sıcak dalı sonraki uzun önbölü istek başlamadan önce çıkarır.

> Çaban düzenlemede bulunmaktadır. İki istek paylaşılansa, ikinci ise 200 paylaşılansa, ikinci ise HBM'de paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan paylaşılan

## Konsepten bir şey.

### KV indeksi olarak kök ağacı

> **【中文解读】**Radiks ağacı (Radix tree) SGLang'ın çekirdek veri yapısıdır. Her bir noktada bir token vardır. KV bloklarının aralığı ve karşılığı. Yeni bir giriş istekleri.

Bir radiks ağacı (kompakt trie) simge dizilerini saklar. Her düğüm bir simge aralığına sahiptir ve bu aralık için hesaplanan KV blokları vardır. Çocuklar bir veya daha fazla simge dizisini uzatırlar.

> Radix ağacı(紧前树) depolama token 序列── her node sahip bir token 范围和为该范围计算的 KV 块──子节点扩展序列 一或多个 token──

```
root
 |- "You are a helpful assistant..."  (2,000 tokens, 124 KV blocks)
      |- "Context: <doc A>..."        (500 tokens, 31 blocks)
           |- "Question: Alice..."    (80 tokens, 5 blocks)
           |- "Question: Bob..."      (95 tokens, 6 blocks)
      |- "Context: <doc B>..."        (520 tokens, 33 blocks)
```

Yeni bir istek sistem istekleri + "Kontext: <doc A>" + "Question: Carol" ile gelir. Programlayıcı: sistem önbellekleri eşleşir (124 blok yeniden kullanılır), doc-A dal eşleşir (31 blok yeniden kullanılır), sonra sadece "Question: Carol" için yeni bloklar tahsis eder (4 blok). Ön doldurma maliyeti: 4 blok yeni jetonlar. Ağaç olmadan: 160 blok. ~40x ön doldurma tasarruf.

> Bir yeni istek sistemle birlikte bir ipucu + "Kontext: <doc A>" + "Question: Carol" 进入──调度器遍历:系统前匹配(复用124块),doc-A 分支匹配(复用31块), sonra sadece "Question: Carol" 分配新块(4块)──预填成本:4块新代币──没有树:160块──预填节省约40倍──

### Kaynaklı programlama

> **【中文解读】**缓存 algılama düzenlemesinin iki anahtar stratejisi: 1) derin öncelikli ayarlama  öncelikli hizmet ile mevcut işletme topluluğu paylaşım bölümü çağrısı, HBM'de sürekli olarak sıcak nokta bölümü tutmak; 2) bölük seviyesinde LRU 淘汰 tüm bölük bölümü olarak seçilme  en az kullanılan yapraklardan başlamak), tek bir blok yerine.

Eğer bu arşiv çalışmıyorsa, Radix ağacı desteklenen tekrar kullanımı anlamsızdır.

> Eğer kayıt sürekli hareket ederse, kök ağacının 支持的复用无意义―― iki anahtar strateji:

1. **Depth-first dispatch**Sıradan bir sonraki talebi seçerken, geçerli çalıştırma seti ile aynı dalda kökleşmiş istekleri tercih edin. Bu sıcak dalı sabit tutar.
   Çeviri:**深度优先调度**❖ Bir dizi arasından bir sonraki talebi seçerken, öncelikli seçim mevcut çalışma kümesi ile bir bölümün talebi ile yapılmalıdır.
2. **LRU at branch level, not block level**. Bireysel bloklar yerine tüm dalları (en kısa kullanılan yapraklardan başlayarak) çıkarın, böylece önbelleğin şekli radix şekliyle eşleşir.
   Çeviri:**分支级 LRU**❖ tüm bölgeleri en az kullanılan yapraklardan çıkarmak, tek bir parça yerine, kayıp şeklini kök şekliyle uyumlu hale getirmek.

FCFS her ikisini de ihlal eder. 2000 token paylaşım talebi 50 token paylaşım talebi arkasında kalır.

> FCFS 违反两者──一共享2000代币请求排在共享50代币请求后,然后2000代币分支被淘汰以接受50代币请求──

### Hatırlamalısınız.

- Llama 3.1 8B, H100, ShareGPT 1K istekleri: SGLang ~ 16,200 tok/s vs vLLM ~ 12,500 (~ 29% kenar).
  Çeviri:Llama 3.1 8B,H100,ShareGPT 1K prompt:SGLang 约 16,200 tok/s vs vLLM 约 12,500(约 29% 优势)
- Önceden ağır RAG (aynı sistem + aynı belge, farklı soru): SGLang'da 6.4x'e kadar.
  Çine Çevirimi:前密集 RAG(相同系统 + 相同文档,不同问题):SGLang 上最高 6.4 倍。
- Ses klonlama iş yükleri: 86,4% önbellek-cache hit oranı.
  Çinçe Çevirisi:语音克隆工作负载:86.4% 前缓存命中中率──
- SGLang müşterilerinde üretim oranları: hızlı disiplinlere bağlı olarak %50-99'dur.
  Çin dilinde:SGLang 客户的生产命中率:50-99%, 排序纪律──
- 2026'da 400.000+ GPU'da dağıtıldı.
  Çinçe Çevirisi:26 yıl deployment on 400,000+ GPU 上。

### Sipariş aldı.

> **【中文解读】**6.4x hızlılık, uyumlu bir önerme biçiminin sıralanmasına bağlıdır.`[system, tools, context, history, question]`Bazen yapım yapıyorlar .`[system, context, tools, history, question]`,radix tree  cannot find shared                                                                                                                                                                                                                                                           

> **【拓展：SGLang 在生产中的采用】**SGLang 2026 yılında 400.000'den fazla GPU'da dağıtıldı. Kullanıcılar arasında xAI(Grok)、LinkedIn、Cursor、Oracle, ve GCP/Azure/AWS'in yönetim hizmetleri bulunmaktadır.

6.4x numarası, sürekli bir istek şablon siparişine dayanır.`[system, tools, context, history, question]`Bazı isteklerde ve`[system, context, tools, history, question]`Bir insan için ortak bir önlük gibi görünen şey, kök ağacının iki farklı sırasıdır.

> 6.4x sayı, uyumlu bir istek üzerine kuruluyor. Eğer müşteriniz belirli bir istek içinde yapılandırılmışsa`[system, tools, context, history, question]`, diğer istekler arasında yapılandırma`[system, context, tools, history, question]`, ağaç ortaklıkta bulunamıyor. İnsanlara göre ortaklıkta görünüyordu.

Mühendislik Lever: Cevap şablonunuz bir önbelleğe açılır. Düzenlemeyi düzeltin. Değişmez olan her şeyi (sistem, araçlar, şemalar) önce koyun. Ardından geri alım bağlamını koyun. Kullanıcı sorusunu sonuna koyun. Dinamik içeriği önlükte bırakmayın.

> 工程师的杆:你的提示 模板是缓存键──固定顺序──将所有不可变内容(系统、工具、方案) 放最前──检索上下文放中间──用户问题放最后──不要在可缓存前中交错动态内容──

Araştırmadan gerçek bir durum: Kaynağabilir önlükten dinamik içeriği taşımak bir değişiklikte bir dağıtımın %7'ten %74'e kadar kaynağa ulaşma oranını aldı.

> Araştırmalarda gerçek örnek: Hareketli içerik kaydedilebilir kaydetme önüne taşınırken, bir seferinde yerleştirilen kaydetme kaydetme oranı %7'ten %74'e yükseldi.

### RadixAttention'ın kazanıp kaybettiği yer

> **【拓展：RadixAttention vs Prefix Caching 性能对比】**SGLang ve vLLM'nin önde gelen depolama performansı karşılaştırması: Llama 3.1 8B H100'de, genel ShareGPT 工作负载 içinde SGLang 达到 ~16,200 tok/s vs vLLM ~12,500 tok/s(29% 优势);重度前重复使用 RAG 工作负载中优势可达 6.4x;语音克隆工作负载缓存命中率 86% ⋅ ama vLLM 2026 yılında da ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön ön

Kazanç:
- RAG (aynı bir alıntı önbellek, farklı soru).
  Çeviri:Rag (Rag)
- Ajanlar (aynı araç şemeleri, farklı sorgular).
  Çeviri:Agent (Agent)
- Uzun sistem mesajıyla sohbet edin.
  Çin Çeviri: Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Ç Çanakkale Ç Ç Çanakkale Ç Ç Ç Çanakkale Ç Ç Ç Ç Ç Çanakkale Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Çanak Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç
- Tekrarlanan preambulları olan ses/görüş iş yükleri.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri

Kayıplar (vLLM seviyesindeki geçiş seviyesine geri döner):
- Tek çekim generasyonu, benzersiz isteklerle (kod tamamlanması, sistem isteksiz açık sohbet).
  Çinçe Çevirimiçi:独立 prompt 的单次生成
- Dinamik istekler, her istek için eşsiz içeriği önbellek içine bırakır.
  Çinçe Çevirimi: Her istek bir kez daha kaydedilebilir.

### Neden bu sadece çekirdek sorunu değil, bir programlayıcı sorunu

KV yeniden kullanımı bir çekirdek hilesi olarak uygulayabilirsiniz. SGLang'ın anlayışı, tekrar kullanımı yalnızca programcı sıcak dalın oturucuunu tutursa ödenecektir. Saf bir "daha kullanılabilirse yeniden kullan" politikası, önbelleği karışık yük altında hızlandıracak. Radiks ağacı indeksi programcısı çekirdek hilesini% 29 üretim kenarına çeviren şeydir.

> KV'yi nükleer teknikler için kullanmak için kullanılabilmektedir. SGLang'ın anlayışı nükleer tekniklerin sadece nükleer cihazlarda kalıcı kalıcılık için kullanılabilmesi için kullanılabilmektedir.

### VLLM ile etkileşim

İki sistem de sıkı bir rekabetçi değildir.`--enable-prefix-caching`SGLang'ın tüm yığını radix-birincidir; vLLM onu aşıladı. Önceden yeniden kullanımı ile egemen olan iş yükleri için, SGLang varsayılan olarak kalır.

> 两个系统不是严格竞争者──2026年 vLLM 添加了前缓存(`--enable-prefix-caching`) ve缓存感知路由器 (Rust 实现的 vLLM Router) 差距缩小而未完全消失SGLang'ın tümü 是radix-first 设计;vLLM 是嫁接上去的──对于前复用主导工作负载,SGLang 仍然是默认选择──对于没有强前模式的通用服务,vLLM 仍然相当或更好──

## Çerçeveyi kullanın.
```figure
roofline
```

## Kullan

`code/main.py`Oyuncak bir radix-tree KV önbelleği ek olarak iki politika ile bir programlayıcı: FCFS ve önbelleği farkındadır. Her ikisinden de aynı iş yükünü çalışır, önbelleği önbelleği isabet oranı ve özet delta raporları.

> `code/main.py`实现一个模拟基根树 KV 缓存加两个策略调度器:FCFS 和缓存感知──用两者运行相同工作负载,报告前缓存命中率和吞吐量差异──然后运行"乱序排序"工作负载显示 6.4x 崩──

## İndirin . Ürünler .

> **【拓展：前缀缓存策略选择】**2026 yıl öncesinde 缓存 üç aşama vardır: 1) 应用级语义缓存(Phase 17·14) 调用中文学历前用嵌入相似度匹配历史响应,命中率 10-70%;(2) 服务端前缓存(SGLang RadixAttention / vLLM önbelleği önbelleği önbelleği) 重用 KV Cache,10x 延迟降低;(3) 跨节点缓存路由(Phase 17·11)  通过缓存-aware router 将请求路由由请求路由到持有前的副本──三者可叠加:语义缓存 → 避免 LLM 调用 端端前缓存避免重复预填 → 跨节点路由避免请求配──

Bu ders bize çok yararlı .`outputs/skill-radix-scheduler-advisor.md`. İş yükünün bir açıklaması (sürekli şablon şekli, geri alım örneği, eş zamanlı kiracı sayısı) verildiğinde, SGLang'ın kabul edilmesi için bir sürekli sipariş reçetesini ve bir git/götürme reçetesini üretir.

> 本课产 出 `outputs/skill-radix-scheduler-advisor.md`△ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △                                                      

## Egzersizler.

1. Çık .`code/main.py`. Aynı iş yükü üzerinde FCFS ve cache-conscious'i karşılaştırın.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`code/main.py`◊ Aynı iş yükü üzerinde FCFS ile depolama algısını karşılaştırmak. Fark neyden  prefill save, decode save, or queue delay?
2. Çalışma yükünü değiştir , böylece istekler rastgele dönüştürülür .`[system, tools, context]`- Tekrar çalış.
   Çeviri: Modifié工作负载使 prompt 随机排列  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`[system, tools, context]`- Ne oldu? - Neden?
3. Llama 3.1 8B'de bir radix dalı olarak 2.000 tokenlik bir sistem istekçiyi tutmanın HBM maliyetini hesaplayın. Önceden yeniden kullanılmadan 16 dizi bir parti maliyetine karşılaştırın.
   Çin Çeviri:计算在 Llama 3.1 8B 上保持 2,000 token 系统提示作为一个基因 分支常驻的HBM 成本──与无前复用16序列批次成本比较──
4. SGLang RadixAttention makalesini okuyun. Üç cümle ile açıklayın, neden ağaç şeklinde LRU'nun çıkarılması, ağır yük altında blok şeklinde LRU'yu yener.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri Çeviri Çeviri: Çeviri Çeviri: Çeviri Çeviri: Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Ç Ç Ç Ç Ç Ç Ç Çeviri Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç
5. Bir müşteri sadece %8'lik bir önbelleğe rastlanan oranı rapor ediyor.
   Çin dilinde: Client report sadece %8 缓存命中率── diyor üç olası neden ve her bir teşhis yöntemini──

## Anahtar Şartlar .

| Term / 术语 | What people say / 通俗说法 | What it actually means / 实际含义 |
|------|----------------|------------------------|
| RadixAttention | "the SGLang thing" / "SGLang 的那个" | KV cache indexed as a radix tree so shared prefixes reuse blocks / KV 缓存以 radix tree 索引，共享前缀复用块 |
| Radix tree | "compact trie" / "紧凑前缀树" | Tree where each node owns a token range and its KV blocks / 每个节点拥有 token 范围和 KV 块的树 |
| Cache-aware scheduler | "hot-branch-first" / "热分支优先" | Scheduler that prefers requests sharing the resident branch / 优先服务共享常驻分支请求的调度器 |
| Prefix-cache hit rate | "how much of your prompt was free" / "prompt 多少是免费的" | Fraction of prompt tokens served from reused KV blocks / 从复用 KV 块服务的 prompt token 比例 |
| FCFS | "first-come first-served" / "先来先服务" | Default scheduling that breaks prefix locality / 破坏前缀局部性的默认调度 |
| Branch-level LRU | "evict the leaf" / "淘汰叶子" | Eviction policy matched to radix shape / 匹配 radix 形状的淘汰策略 |
| Prompt template ordering | "the cache key" / "缓存键" | The prompt's component order determines what the tree can share / prompt 组件顺序决定树能共享什么 |
| System prompt pinning | "resident prefix" / "常驻前缀" | Keep the immutable system portion pinned to avoid eviction thrash / 保持不可变系统部分固定避免淘汰抖动 |

## Daha fazla okumak

- [SGLang GitHub](https://github.com/sgl-project/sglang) kaynak ve belgeler.
- [SGLang documentation](https://sgl-project.github.io/) Radixİzdenme ve programlama detayları.
- [SGLang paper — Efficiently Programming Large Language Models (arXiv:2312.07104)](https://arxiv.org/abs/2312.07104) tasarım referansı.
- [LMSYS blog — SGLang with RadixAttention](https://www.lmsys.org/blog/2024-01-17-sglang/) Referans sayıları ve programcı mantıklılığı.
- [vLLM — Prefix Caching](https://docs.vllm.ai/en/latest/features/prefix_caching.html) vLLM'nin kendi radikal uygulaması, karşılaştırma için.
