# vLLM Servis İçsel: Sayfa Dikkat, Sürekli Batching, parçalanmış Prefill
# Servis Motor İçleri  PagedAtention, Sürekli Batching, parçalanmış Prefill

> Modern servis motorlarının üretimi üç komplo etkisiyle yapılır, tek bir numara değil. PagedAttention her zaman açık. Sürekli serileme, yeni istekleri çözme iterasyonları arasında aktif seriye enjekte eder. Parça dolandırıcılık parçaları uzun ipuçları böylece kodlama tokenleri asla açlıktan ölmez. Üçünü de açarsanız, bir H100 SXM5'de Llama 3.3 70B FP8'in 128 eşzamanlı 'de 2.200-2.400 tok/s'i harekete geçiriyor. Bu ders, vLLM'nin programlayıcı ve dikkat çekirdeğini okuyor  üç tekniğin referans motorunu  bir düzeyde çizim yapabileceğiniz bir seviyede ve bir oyuncak sürekli batcher ile sona erer `code/main.py`Programlar vLLM'nin yaptığı gibi önceden doldurulur ve çözülür.

> **【中文解读】**vLLM 2026 yılında baskın konum üç karmaşık optimizasyon temelinde:PagedAttention(分页注意力)始终开启;连续批处理在解码代间注入新请求;分块预填片长提示以防止解码 代币饥饿──三者全开时,Llama 3.3 70B FP8 在单卡 H100 上以 128 并发达2,200-2,400 tok/s比朴素 PyTorch 循环快 3-4 倍──

> **【拓展：vLLM → LLM 推理服务标准】**vLLM 2026 yılının en popüler açık kaynaklı LLM 推理服务引擎です。PagedAttention 借借操作系统的虚拟内存分页思想管理 KV Cache, parçacık oranını% 4 altında kontrol edecektir。

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy continuous batching scheduler) | **语言:** Python（标准库，连续批处理调度器模拟）
**Prerequisites:** Phase 17 · 01 (Model Serving), Phase 11 (LLM Engineering) | **前置知识:** Phase 17 · 01（模型服务）, Phase 11（LLM 工程）
**Time:** ~75 minutes | **时间:** ~75 分钟

>  **【前置】**Önemli bir şekilde, bu süreçte, yeni bir sistem oluşturmak için, yeni bir sistem oluşturmak için, yeni bir sistem oluşturmak için, yeni bir sistem oluşturmak için, yeni bir sistem oluşturmak için, yeni bir sistem oluşturmak için, yeni bir sistem oluşturmak için, yeni bir sistem oluşturmak için, yeni bir sistem oluşturmak için, yeni bir sistem oluşturmak için, yeni bir sistem oluşturmak için, yeni bir sistem oluşturmak için, yeni bir sistem oluşturmak için, yeni bir sistem oluşturmak için, yeni bir sistem oluşturmak için, yeni bir sistem oluşturmak için, yeni bir sistem oluşturmak için, yeni bir sistem oluşturmak için, yeni bir sistem oluşturmak için, yeni bir sistem oluşturmak için, yeni bir sistem oluşturmak için, yeni bir sistem oluşturmak için, yeni bir sistem oluşturmak için, yeni bir sistem oluşturmak için, yeni bir sistem oluşturmak için, yeni bir sistem oluşturmak için, yeni bir sistem oluşturmak için, yeni bir sistem oluşturmak için, yeni bir sistem oluşturmak için, yeni bir sistem oluşturmak için, yeni bir sistem oluşturmak için, yeni bir sistem oluşturmak için, yeni bir sistem oluşturmak için, yeni bir sistem oluşturmak için, yeni bir sistem oluşturmak için, yeni bir sistem oluşturmak için, yeni bir sistem oluşturmak için, yeni bir sistem oluşturmak için, yeni bir sistem ve geliştirmek için, yeni bir sistem oluşturmak için, yeni bir sistem oluşturmak için, yeni bir sistem ve geliştirmek için,
>  **【类比】**vLLM 三件套 = "高效餐厅厨房"。PagedAttention = 分块管理 KV cache(像操作系统虚拟内存分页,碎片率 < 4%);Continuous Batching = 动态拼单(新请求随时插入运行批);Chunked Prefill = 切长快速(长输切片避免阻塞解码)。Llama 3.3 70B FP8 H100 上 128 并发达 2200-2400 tok/s,比朴素实现快 3-4 ⋅倍

## Öğrenme hedefleri

- PagedAttention'u KV önbelleği tahsiscisi olarak açıklayın: bloklar, blok tabloları ve neden parçalanma üretim yükünde% 4'ten düşük kalır.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri Çeviri: Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Ç Ç Ç Ç Ç Ç Çeviri Çeviri Ç Ç Ç Çeviri Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç
- İterasyon düzeyinde sürekli serileme diyalogu: bitmiş dizilerin seriyi nasıl terk ettiğini ve yeni dizilerin boşaltılmadan nasıl birleştiğini gösterir.
  Çinçe Çevirimiçi: 代级别绘制连续批处理:完成的序列如何离开批次,新序列如何加入而无需清空──
- Bir cümlede parçalanmış prefill'i tanımlayın ve hangi gecikme metrikini koruduğunu belirtin (söyleme: TTFT kuyruk, geçiş anlamına gelmez).
  Çinçe Çevirimiçi: using a sentence describe分块预填充,并说出它保护哪个延迟指标
- 2026 vLLM v0.18.0'un adını verin. Tüm optimizasyonları bir anda sağlayan takımları ısırır.
  Çinçe Çevirisi:  2026 yıl vLLM v0.18.0 中同时启用所有优化团队会遇到问题──

## Sorunlar. Sorunlar.

> **【中文解读】**朴素 PyTorch 服务循环一次处理一个请求――静态批处理将所有请求填充至最长序列,浪费 GPU资源并让快请求等待慢请求――vLLM 通过三个核心优化解决这个问题:PagedAttention(KV Cache 碎片率从60-80% 降至4% 以下) 连续批处理(在解码代间动态加入新请求) 分块预填充(将长提示切片以防止解码饥饿) 

Saf bir PyTorch servis döngüsü bir seferde bir istek çalışır: tokenize, prefill, EOS'a kadar dekode, geri. Bir kullanıcı için bu işe yarıyor. Yüzde, sabırlı insanların bir kuyrukları. Açıkça görülen düzeltme  statik parti  her talebi penceredeki en uzun çağrısına, her dekodunu en uzun beklenen çıkışa kapatır ve tüm partiyi en yavaş dizide durdurur. Hiç kullanmadığın dolgu için para ödüyorsun ve hızlı talepler yavaş talepler için bekliyor.

> 朴素 PyTorch 服务循环一次处理一个请求:分词、预填充、解码直到EOS、返回──一个用户时这行通──一百用户时,这就是一排耐心等待的人──显然修复静态批处理将每个请求填充到窗口中最长的提示,将每个解码填充到最长的预期输出,整个批次等待最慢的序列──你为未曾使用的填充单,快速请求等待缓慢请求──

VLLM üç sorunu bir anda çözer. PagedAttention, KV önbelleğinin parçalanmasını, klasik bir arada tahsis edilme gibi GPU belleğinin %60-80'ini tüketmekten alıkoyar. Sürekli serileme, isteklerin her dekodlama iterasyonu arasında bir araya gelmesine ve partiyi terk etmesine izin verir, bu nedenle parti her zaman gerçek işle dolu olur. Parça dolandırıcılığı, 32k işaretli bir işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli işaretli olarak bölgeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeyeye

> vLLM bir kez çözmek üç sorunu. PayedAttention PagedAttention PageedAttention PageedAttention PageedAttention PageedAttention PageedAttention PageedAttention PageedAttention PageedAttention PageedAttention PageedAttention PageedAttention PageedAttention PageedAttention PageedAttention PageedAttention PageedAttention PageedAttention PageedAttention PageedAttention PageedAttention PageedAttention PageedAttention PageedAttention PageedAttention PageedAttention PageedAttention PageedAttention PageedAttention PageedAttention PageedAttention PageedAttention PageedAttention PageedAttention PageedAttention PageedAttention PageedAttention PageedAttention PageedAttention PageedAttention PageedAttention PageedAttention PageedAttention PageedAttention PageedAttention PageedAttention PageedAttention PageedAttention PageedAttention Pageed Attention Pageed Attention Pageed Attention Pageed Attention Pageed Attention Pageed Attention Pageed Attention Pageed Attention Pageed Attention Pageed Attention Pageed Attention Pageed Attention Pageed Attention Pageed attention Pageed attention Pageed attention Pageed attention Pageed to Each Pageed to Work Pageed attention Pageed to Work Pageed to Work P

2026 üretim standartı üçü de çalıştırılmış. Her birinin ne yaptığını anlamalısınız çünkü başarısızlık modları tümüyle planlamacıda, modelde değil.

> 2026 yılında üretim öntanımlı ayarları üçtür. Her birimizin ne yapacağını bilmen gerekir. Çünkü sorunlar model üzerinde değil, düzenleyicide.

## Konsepten bir şey.

### PagedAttention sanal bellek sistemi olarak

> **【中文解读】**PagedAttention 借借鉴操作系统虚拟内存分页思想管理 KV Cache。 geleneksel olarak her diziye en fazla uzunlukta dağıtım yapılmaktadır.`--gpu-memory-utilization`(默认 0.9) kontrol KV Cache kullanılabilir HBM örneğin

> **【拓展：KV Cache 内存管理演进】**KV Cache 内存管理 üç nesil gelişimi yaşamıştır: 1) 连续预分配简单但浪费60-80%内存; 2) PagedAttention(vLLM 2023) 分页管理,碎片率 <4%,成为行业标准; 3) RadixAttention(SGLang 2024) 前共享场景下进一步优化,通过 radix tree 索引实现跨请求的 KV 复用――70B 模型 128 并发的生产负载下,PagedAttention 相比连续分配可节省50-70% GPU'nın内存――

KV önbelleği .`num_layers × 2 × num_heads × head_dim × seq_len × bytes_per_element`Llama 3.3 70B için 8192 token, yani BF16'da yaklaşık 1.25 GB bir dizi. Eğer her talebe 8192 slot önceden rezervasyon yaparsanız ancak ortalama talebe sadece 1500 token kullanırsanız, rezervasyon yaptığınız HBM'nin yaklaşık %82'ini harcıyorsunuz. Klasik parti bu harcamaları öder.

> Her bir dizi KV'nin büyüklüğü büyüklüğünde .`num_layers × 2 × num_heads × head_dim × seq_len × bytes_per_element`❖ Llama 3.3 70B ⋅ BF16 ⋅ BF16 ⋅ BF16 ⋅ BF16 ⋅ BF16 ⋅ BF16 ⋅ BF16 ⋅ BF16 ⋅ BF16 ⋅ BF16 ⋅ BF16 ⋅ BF16 ⋅ BF16 ⋅ BF16 ⋅ BF16 ⋅ BF16 ⋅ BF16 ⋅ BF16 ⋅ BF16 ⋅ BF16 ⋅ BF16 ⋅ BF16 ⋅ BF16 ⋅ BF16 ⋅ BF16 ⋅ BF16 ⋅ BF16 ⋅ BF16 ⋅ BF16 ⋅ BF16 ⋅ BF16 ⋅ BF16 ⋅ BF16 ⋅ BF16 ⋅ BF16 ⋅ BF16 ⋅ BF16 ⋅ BF16 ⋅ BF16 ⋅ BF16 ⋅ BF16 ⋅ BF16 ⋅ BF6 ⋅ BF6 ⋅ BF2 ⋅ BF ⋅ BF ⋅ BF ⋅ BF ⋅ BF ⋅ BF ⋅ BF ⋅ BF ⋅ BF ⋅ BF ⋅ BF ⋅ BF ⋅ BF ⋅ BF ⋅ BF ⋅ BF ⋅ BF ⋅ BF ⋅ BF                                                                                                     

PagedAttention, bu fikri OS sanal bellekinden ödünç alır. KV önbelleği dizi başına bitişik değildir. Sıkı boyutlu bloklara (öntemli 16 token) tahsis edilir. Her dizi, mantıklı token konumlarını fiziksel blok kimliklerine harcayacak bir blok tablosuna sahiptir. Bir dizi tahsis edilen blokların ötesinde büyüdüğünde, bir blok daha eklenir. Bitirdiğinde, blokları havuza geri döner.

> PagedAttention 借借借操作系统虚拟内存的思想──KV 缓存不是每个序列连续的──它以固定大小的块──默认16代币) 分布──每个序列有一个块表,将逻辑代币 位置映射到物理块 ID──当序列增长超过已分配块时,添加一个新块──完成后,块回归池──

Fragmentasyon %60-80%'den (klasik) %4'ten (PagedAttention) aşağıya düşüyor.`--gpu-memory-utilization`(devay 0.9), vLLM'ye yükleme ağırlıkları ve etkinleştirmelerinden sonra KV blokları için ne kadar HBM rezervasyonu yapması gerektiğini söyler.

> 碎片率 60-80% 经典) aşağı aşağı 4% 👍🏻PagedAttention)。you don't need with tag to enable PagedAttention`--gpu-memory-utilization`(默认 0.9), vLLM'ye yükleme yüklemesi ve aktivasyon sonrasında KV blokları için HBM'yi bırakmalarını söyle.

### Sürekli iterasyon düzeyinde serileme

> **【中文解读】**连续批处理在每个解码步骤之间做出接受/释放决策──每个代:(1) 移除已完成的序列;;(EOS veya max_tokens);(2) 检查等队列,如果有空 KV 块则接受新序列;(3) RUNNING listedeki tüm序列ler için bir kez前向传播──批次大小不定,不同输出位置的序列共享一次融合前向计算──2026 vLLM V1 调度器的核心不变量是:调度器解码每个代运一次,而不是每一个请求运一次──

Eski "dinamik parti" bir parti doldurmak için bir pencereyi (deyelim 10 ms) bekledi, sonra her dizisi bitene kadar önceden doldur + dekode + dekode + dekode çalıştı.

> 旧的"动态批处理" bir pencerenin doldurulmasını bekler, sonra her bir dizide bitene kadar prefill + decode + decode + decode çalışır.

Her dekodlama aşamasında sürekli seri çalışması yürütülür.`RUNNING`listesi. her iterasyonda:

> 连续批处理在每个解码步骤之间操作――将运行中的序列集合称为 `RUNNING`列表──每次代:

1. Herhangi bir sırada .`RUNNING`EOS'u vurmak veya max_tokens kaldırılır.
   Çeviri:`RUNNING`EOS veya max_tokens'in herhangi bir sırası kaldırıldı.
2. Programlayıcı bekleme sırasına bakıyor. Eğer ücretsiz KV blokları varsa, yeni diziler kabul eder (öncelme veya yeniden başlatılır).
   Çinçe Çevirimiçi:调度器查看等待队列──如果有空 KV 块,它接纳新序列(预填充或恢复)──
3. Ön geçit şimdi ne varsa üzerinde geçer .`RUNNING`, her sekvense yeni bir token gönderir.
   Çeviri:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          `RUNNING`İçinde olan her şey yürür, her bir bölüm yeni bir token gönderir.

İsteğe bağlı olarak, bir seri seri olarak, bir seri olarak, bir seri olarak, bir seri olarak, bir seri olarak, bir seri olarak, bir seri olarak, bir seri olarak, bir seri olarak, bir seri olarak, bir seri olarak, bir seri olarak, bir seri olarak, bir seri olarak, bir seri olarak, bir seri olarak, bir seri olarak, bir seri olarak, bir seri olarak, bir seri olarak, bir seri olarak, bir seri olarak, bir seri olarak, bir seri olarak, bir seri olarak, bir seri olarak, bir seri olarak, bir seri olarak, bir seri olarak, bir seri olarak, bir seri olarak, bir seri olarak, bir seri olarak, bir seri olarak, bir seri olarak, bir seri olarak, bir seri olarak, bir seri olarak, bir seri olarak, bir seri olarak, bir seri olarak, bir seri olarak, bir seri olarak, bir seri olarak, bir seri olarak, bir seri olarak, bir seri olarak, bir seri olarak, bir seri olarak, 2026 vLLM olarak, bir dizi olarak, bir dizi olarak, bir dizi olarak, bir dizi olarak, bir dizi olarak, bir dizi olarak, bir dizi olarak, bir dizi olarak, bir dizi olarak, bir dizi olarak, bir olarak, bir olarak, bir olarak,`V1 scheduler`Anahtar değişmezliği: programlayıcı, her dekodlama iterasyonunda bir kez çalıştırılır, istek için değil.

> 批次大小 批次大小 批次大小 批次大小 批次大小 批次大小 批次大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大小大`V1 scheduler`△关键不变量:调度器每个解码代运行一次,而不是每个请求运行一次──

### Parçalama prefill TTFT kuyruğunu korur

> **【中文解读】**Bölüm önceden doldurma, diğer sıra çözme sorunu çözmüştür. 70B modelinde 32K token'un önünü 800 ms'lik bir saf önceden doldurma işlemine ihtiyaç duyulur. Diğer tüm sıraların çözme tokenleri bekliyor. Bölüm önceden doldurma, sabit büyüklükteki blokların çözmesini sağlar. Her blok arasındaki düzenleyici diğer sıraların çözmesini ilerletebilir.

> **【拓展：vLLM 生产部署最佳实践】**2026 yılında VLLM 生产部署'ın anahtar yapılandırması şunları içerir:`--gpu-memory-utilization 0.9`预留 90% HBM 给 KV Cache;(2) `--max-model-len` Gerçek ihtiyaç ayarlarına göre öntanımlı olarak değil, en büyük değer; 3) %s ön doldurucu öntanımlı olarak açılır ama bazı tahminlerle çözülür;`--enable-prefix-caching`RAG/Agent'in durumunda, tekrar tekrar ön doldurma oranı büyük ölçüde azalıyor.

Prefill hesaplama bağlıdır. Llama 3.3 70B'de 32k-token istek bir H100'de ~800 ms saf prefill alır. Prefill çalışırken, seri bekleyen diğer her dizi için tokenleri çözün. Bir servis döngüsünde, bir uzun istek için ilk token gecikmesi (TTFT) onlarca diğer kullanıcı için inter-token gecikme (ITL) blip olur.

> 预充是计算密集型的──Llama 3.3 70B 上一个32K 代币提示在单卡 H100 上需要约800ms 的纯预充──预充运行时,批次中所有其他序列的解码代币都在等待──服务循环中,一个长提示的首个代币延迟(TTFT) birkaç diğer kullanıcı 代币 间延迟(ITL) 毛刺──

Çüklü prefill, sabit boyutlu parçalara bölünür (devay 512 token) ve her parçayı bir birim olarak programlar. Çükler arasında programlayıcı dekod dizilerini bir token ile ileriye atabilir. Yayınlanan referanslarda çok daha düşük dekod zaman jitter için küçük mutlak prefill latency hit (bir parça başına birkaç ms) değiştirirsiniz.

> Bölümler arasında, düzenleyici bir token çözümü sırasını ilerletebilir. Bir blok için birkaç millimetr saniyelik bir süreliğine daha düşük çözümü süresi için değiştirilir. P99 ITL'nin karıştırma yükü yaklaşık 50 ms'den 15 ms'e düşer.

### Üç defalarca etkileşime giren

Tüm üç özellik birbirini kabul eder. PagedAttention programcıya ticaret için ince tohumlu bir KV kaynağı verir. Sürekli serileme bu ince tohumlu kaynağa ihtiyaç duyar, bu nedenle yeni bir dizini kabul etmek küresel bir yeniden düzenleme zorlamaz.`RUNNING`list  bu bir programcı politika daha, ayrı bir sistem değil.

> Üç özellik birbirine bağımlılık.PagedAttention olarak düzenleyici, küçük parçacıklı KV kaynaklarını düzenleyici olarak sağladı.`RUNNING`Listede yapılan kararlar, bağımsız bir sistem değil, başka bir düzenleme stratejisi.

Her bayrağı bilmenize gerek yok.Sedülerin neyi optimize ettiğini bilmelisiniz: KV blok bütçesine uygun, parçalara ayırılmış prefill slicing'e tabi.

> Her bir işareti bilmen gerekmiyor.

### 2026 v0.18.0'u aldın.

> **【中文解读】**vLLM v0.18.0 中 aynı anda etkinleştirilmiyor `--enable-chunked-prefill`和 taslak modeli 推测解码`--speculative-model`)。 Tek istisna V1 调度器daki N-gram GPU 推测解码──not read release notation on opening all optimization mark team will encounter running errors when starting, not software degradation── eğer 推测解码'ın kazancı değerinin açılması blok önceden doldurulması halinde ise,2026 yılının doğru cevabı genellikle EAGLE-3 ve taslak model değil──

vLLM v0.18.0' da birleştiremezsiniz `--enable-chunked-prefill`(Draf model spekülasyonsal çözme ile)`--speculative-model`) Belli bir istisna, V1 programcıda N-gram GPU spekülatör çözümüdür. Sergi notlarını okumadan her bayrağı açan takımlar, başlatma sırasında bir çalıştırma hatası elde eder, yumuşak bir gerileme değil. Eğer spekülatör kazancınız parçalanmış prefill için etkinleştirmeye değerse, seçeneği tekrar gözden geçirin  2026'da doğru cevap genellikle parçalanmış prefill olmadan EAGLE-3'dir, bir taslak model değil ve toplanmayan parçalanmış prefill.

> VLLM v0.18.0'da, aynı anda çalıştırılamazsın.`--enable-chunked-prefill`和 taslak modeli 推测解码`--speculative-model`)。 Dosya kayıtlarının istisnaları V1 调度器 içindeki N-gram GPU 推测解码。 not read Yayın açıklaması tüm işarelerin açılışında çalıştırılmasında bir hata yerine bir soft性退化­ye rastlanan bir ekip tarafından açılmasında bulunmaktadır。 Eğer 推测解码'ın kazancı açılmalıdırsa blok önceden doldurulmalıdır, yeniden gözden geçirilmesi seçimi2026 yılının doğru cevabı genellikle EAGLE-3 ve tasarımı değil model olacaktır。

### Hatırlamalısın numaralar

- Llama 3.3 70B FP8, H100 SXM5, 128 eşzamanlı, üçü de: 2.200-2.400 tok/s.
  Latin Translation:Llama 3.3 70B FP8,H100 SXM5,128 并发,三个优化全开:2,200-2,400 tok/s
- Aynı model, varsayılan vLLM (çıkılmış ön doldurma yok): ~1,800 tok/s.
  Çine dilinde:同模型,默认 vLLM(无分块预填充): yaklaşık 1.800 tok/s。
- Aynı model, saf PyTorch ileri döngüsü: ~600 tok/s.
  Çeviri: 600 tok/s
- KV parçalanması atıkları: %4
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri Çeviri: Çeviri: Çeviri: Çeviri: Çeviri Çeviri: Çeviri Çeviri: Çeviri Ç Ç Ç Çeviri Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç
- Karışık yük altında P99 ITL: ~ 15 ms parçalı prefill ile, ~ 50 ms olmadan.
  Çine Çeviri: HİKK yükleme altında P99 ITL:有分块预填充约15ms,无约50ms──

### Programcı nasıl görünüyor?

```
while True:
    finished = [s for s in RUNNING if s.is_done()]
    for s in finished: release_blocks(s); RUNNING.remove(s)

    while WAITING and have_free_blocks_for(WAITING[0]):
        s = WAITING.pop(0)
        allocate_initial_blocks(s)
        RUNNING.append(s)

    # schedule prefill chunks + decode in one batch
    batch = []
    for s in RUNNING:
        if s.in_prefill:
            batch.append(next_prefill_chunk(s))   # e.g. 512 tokens
        else:
            batch.append(decode_one_token(s))     # 1 token

    run_forward(batch)                            # one fused GPU call
```

`code/main.py`Stdlib Python'da sahte token sayıları ve sahte ileri gecikme ile aynı döngüdür.

> `code/main.py`Bu döngünün saf standart kütüphanesi Python'u gerçekleştirir, sahte token sayımı ve sahte ön-gecikme ile.

## Çerçeveyi kullanın.
```figure
tensor-parallel
```

## Kullan

`code/main.py`vLLM tarzı bir programcı simüle eder.

> `code/main.py`模拟一个带有可切换功能的 vLLM 风格调度器──运行

- `NAIVE`Mod: Tek seferde bir talep, serileme yapılmıyor.
  Çeviri:`NAIVE`模式: bir kere bir istek, hiçbir miktarda işlem yapılmamıştır.
- `STATIC`Mod: bekleme ve bekleme, klasik parti.
  Çeviri:`STATIC`模式: doldurma ve bekleme, klasik toplama işlemleri
- `CONTINUOUS`Mod: İterasyon düzeyinde kabul ve serbest bırakma.
  Çeviri:`CONTINUOUS`模式: 代级的接收和释放──
- `CONTINUOUS + CHUNKED`Mod: Decode ile birbirine karışmış prefill parçalar.
  Çeviri:`CONTINUOUS + CHUNKED`模式:预填充切片与解码交错──

Çıktı toplam geçiş (virtual saniyede tokenler), TTFT ortalaması ve P99 ITL gösterir.`CONTINUOUS + CHUNKED`sıra karışık trafikte baskın olmalıdır.

> 输出显示总吞吐量(每虚拟秒令子 数) 、TTFT 均值和 P99 ITL。`CONTINUOUS + CHUNKED`Yapılan karışık akımlar arasında en büyük oranı

## İndirin . Ürünler .

> **【拓展：LLM 推理引擎对比】**2026 yılında ana açık kaynak LLM 推理引擎包括:vLLM(通用生产默认,PagedAttention+连续批处理)、SGLang(前共享优化,RadixAttention)、TensorRT-LLM(NVIDIA 专属,Blackwell 上吞吐最高)、llama.cpp(CPU/边缘,GGUF 格式)。选择取取于硬件(CPU/GPU/Hopper/Blackwell)、工作负载(通用聊天/Agent/RAG) 和合规要求自(托管/云托管)。vLLM 约60% 根据生产部署额的部署((2026 AI 基础设施调查)。

Bu ders bize çok yararlı .`outputs/skill-vllm-scheduler-reader.md`. Bir servis yapılandırmasını (batch boyutu, KV bellek kullanımı, parçalanmış prefill boyutu, spekülatör yapılandırması) göz önüne alındığında, üç standarttan hangisinin şişek boynuzlu olduğunu ve hangi ayarlanacağını belirleyen bir planlamacı teşhisini üretir.

> 本课产 出 `outputs/skill-vllm-scheduler-reader.md`△ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △                                                                                  

## Egzersizler.

1. Çık .`code/main.py`- Ben de .`STATIC`- ...`CONTINUOUS` Prefill verimliliği, dekode verimliliği veya kuyruğu gecikmeliliği ile birlikte, geçiş boşluğu nereden geliyor?
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`code/main.py`◊                                                                                                                                                                                                                                                              `STATIC`和 `CONTINUOUS`◊ Yüklenme farkı hangi yönlerden  Prefill efficiency, decode efficiency veya final delay?
2. Eklemek için oyuncak programlayıcısını değiştir `--max-num-batched-tokens`Llama 3.3 70B FP8 çalışan bir H100 için doğru değer nedir? (İpucu: KV blok boyutunun ve serbest blokların sayısının, ham HBM değil, fonksiyonu.)
   Çeviri: Modifikasi: Modifikasi: Modifikasi: Modifikasi: Modifikasi: Modifikasi: Modifikasi: Modifikasi: Modifikasi: Modifikasi: Modifikasi: Modifikasi: Modifikasi: Modifikasi: Modifikasi: Modifikasi: Modifikasi: Modifikasi: Modifikasi: Modifikasi: Modifikasi: Modification: Modification: Modification: Modification: Modification: Modification: Modification: Modification: Modification: Modification: Modification: Modification: Modification: Modification: Modification: Modification: Modification: Modification: Modification: Modification: Modification: Modification: Modification: Modification: Modification: Modification: Modification: Modification: Modification: Modification: Modification: Modification: Modification: Modification: Modification: Modification: Modification: Modification: Modification: Modification: Modification: Modification: Modification: Modification: Modification: Modification: Modification: Modified by Modification: Modification: Modification: Modified by Modification: Modification: Modified by Modification: Modified by Modification: Modified by Modification: Modified by Modification: Modified by Modification: Modified by Modified by Modification: Modified by Modified by Modified by Modification: Modified by Modified by Modified by Modification: Modified by Modified by Modified by Modified by Modified by Modification: Modified by Modified by Modified by Modified by Modified by Modified by Modified by Modified by Modified by Modified by Modified by Modified by Modified by Modified by Modified by Modified by Modified by Modified by Modified by Modified by Modified by Modified by Modified by Modified by Modified by Modified by Modified by Modified by Modified by Modified by Modified by Modified by Modified by Modified by Modified by Modified by Modified by Modified by Modified by Modified by Modified by Modified by Modified by Modified by Modified by Modified by Modified by Modified by Modified by Modified by Modified by Modified by Modified by Modified by Modified by Modified by Modified by Modified by Modified by Modified by Modified by Modified by Modified by Modified by Modified by Modified by Modified`--max-num-batched-tokens`△H100 运行 Llama 3.3 70B FP8'in gerçek değeri nedir?
3. VLLM v0.18.0'un açıklama notlarını tekrar okuyun. Hangi bayrak kombinasyonları karşılıklı dışı?
   Çin dilinde: [değiştirilmiştir]
4. KV önbelleği parçalanma atıklarını, ortalama 1.500 çıkış tokeni, std 600 tokeni ile 1000 talebinin izini hesaplayın, a) talep başına 8192 maksimum, b) 16 token bloklu PagedAttention altında.
   Çin dilinde:计算 1,000 个请求的 KV 缓存碎片浪费(平均值 1,500 输出代币,标准差 600),在 (a) 最大 8192 的连续每请求分配和 (b) 16 代币块的 PagedAttention 下。
5. Bir paragrafda, parçalanmış prefill'in neden P99 ITL'ye yardımcı olduğunu, ancak özelleştirilmiş olarak üretimi yapmadığını açıklayın.
   Çinçe Çevirimi: bir bölümle açıklayın neden P99 ITL'de bir parça prefill yardım etti ancak sadece toplama oranını yükseltmedi.

## Anahtar Şartlar .

| Term / 术语 | What people say / 通俗说法 | What it actually means / 实际含义 |
|------|----------------|------------------------|
| PagedAttention | "the KV trick" / "KV 技巧" | Fixed-size block allocator for KV cache; fragmentation <4% / KV 缓存的固定大小块分配器；碎片率 <4% |
| Block table | "the page table" / "页表" | Per-sequence map from logical token position to physical KV block / 每序列的逻辑 token 位置到物理 KV 块的映射 |
| Continuous batching | "dynamic batching, but right" / "正确的动态批处理" | Admit/release decisions made every decode iteration / 每个解码迭代做出接纳/释放决策 |
| Chunked prefill | "prefill splitting" / "预填充切片" | Break long prefill into 512-token slices interleaved with decode / 将长预填充切为 512 token 片段与解码交错 |
| TTFT | "first token time" / "首 token 时间" | Prefill + queue + network; dominated by prefill at long prompts / 预填充+队列+网络；长提示时由预填充主导 |
| ITL | "inter-token latency" / "token 间延迟" | Time between consecutive decode tokens; dominated by batch size / 连续解码 token 之间的时间；由批次大小主导 |
| Goodput | "throughput that meets SLO" / "满足 SLO 的吞吐量" | Tokens/sec where every request still hit TTFT and ITL targets / 每秒 token 数，每个请求仍满足 TTFT 和 ITL 目标 |
| V1 scheduler | "the new scheduler" / "新调度器" | vLLM's 2026 scheduler; N-gram spec decode is the chunked-prefill-compatible path / vLLM 2026 调度器；N-gram 推测解码与分块预填充兼容 |
| `--gpu-memory-utilization` | "the memory knob" / "内存旋钮" | Fraction of HBM reserved for KV blocks after weights and activations / 加载权重和激活后为 KV 块预留的 HBM 比例 |

## Daha fazla okumak

- [vLLM documentation — Speculative Decoding](https://docs.vllm.ai/en/latest/features/spec_decode/) parçalı prefill ve spekülatör dekodlama uyumluluğu hakkında resmi kaynak.
- [vLLM Release Notes (NVIDIA)](https://docs.nvidia.com/deeplearning/frameworks/vllm-release-notes/index.html) 2026'da yayın cadence ve sürüm spesifik davranış.
- [vLLM Blog — PagedAttention](https://blog.vllm.ai/2023/06/20/vllm.html) hala tahsisci hakkında nasıl düşünüleceğini belirleyen orijinal yazısı.
- [PagedAttention paper (arXiv:2309.06180)](https://arxiv.org/abs/2309.06180) parçalanma analizi ve programlayıcı tasarımı.
- [Aleksa Gordic — Inside vLLM](https://www.aleksagordic.com/blog/vllm) V1 programlayıcısı, alev grafikleriyle ayrıntılı bir şekilde yürüyüşe devam ediyor.
