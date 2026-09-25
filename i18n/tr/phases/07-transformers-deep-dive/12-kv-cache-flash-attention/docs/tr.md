# KV Kaş, Flash Dikkat ve İfrat Optimizasyonı

> Eğitim paralel ve FLOP bağlıdır. İferense seri ve hafıza bağlıdır. Farklı şişek boynuzları, farklı numaralar.

> **【中文解读】**KV Cache 缓存已计算的钥匙/值 避免重复计算,是LLM 推理加速的核心──Flash Attention 优化显存访问模式,减少显存使用──

**Type:** Hands-on | **类型:** 动手
**Language:**Python .**语言:**Python
**Prerequisites:** Phase 7 · 02 (Self-Attention), Phase 7 · 05 (Full Transformer), Phase 7 · 07 (GPT) | **前置知识:** Phase 7 · 02 (Self-Attention), Phase 7 · 05 (Full Transformer), Phase 7 · 07 (GPT)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Sorunlar. Sorunlar.

Saf bir otomatik gerileme dekodörü yapar .`O(N²)`üretmek için çalışmak `N`Tokens: her adımda dikkatini tam önbellek üzerinde yeniden hesaplar. 16M dikkat işlemleri olan 4K-token yanıt için, çoğu fazladan. Bir önbellek tokeninin her gizli durumu hesaplandığında belirlenir.

> Bir basit kendi kendine çözücü üreticisi .`N`个标志 需要 `O(N²)`4K token'in tepkisi, 16M kez dikkat işlemidir, bunların çoğu boştur. Bir kez hesaplanırsa kesinlik, yeni token'ın sorguları ve önceki depolamaların tüm anahtarları ve değerlerine dikkat etmelisiniz.

Bu nedenle, dikkat, bir çok veriyi hareket ettirir. Standart dikkat N×N puan matrisi, N×d softmax çıkışı, N×d son çıkışı  çok fazla okuma ve HBM'ye yazma yapar. N≥2K için, dikkat FLOP-a bağlı olmadan önce hafıza bağlanır. Klasik dikkat çekirdekleri modern GPU'ları 410×'ya az kullanır.

> Ayrıca, dikkat kendisi çok fazla veri taşımak gerekir. Standart dikkat N×N bölü sayı矩阵、N×d softmax 输出、N×d 最终输出 HBM'ye kadar çok sayıda okuma süresi vardır.

Dao et al'dan gelen iki optimizasyon, sınır çıkarımını "yavaş"tan "hızlı"a doğru harekete geçirdi:

> 两个优化 ((都来自道 等人) 将前沿推理从"慢"推向"快":

1. **KV cache.**Her ön işaret simgesinin K ve V vektörlerini saklayın. Her yeni simgenin dikkatini önbelleğe alınan anahtarlara karşı bir sorgu oluşturur.`O(N²)`- ...`O(N)`Bir nesil adım başına.
   Çeviri:**KV 缓存。**存储每个前代币的K 和 V 向量──每个新代币的注意是缓存键的一个查询──推理从每步`O(N²)`降低到 `O(N)`- Evet.
2. **Flash Attention.**Dikkat hesaplamalarını çizin böylece tam N×N matrisi asla HBM'ye ulaşmaz. Tüm softmax + matmul SRAM'da gerçekleşir. A100'de 24× duvar saati hızlandırması; FP8 ile H100'de 510×.
   Çeviri:**Flash Attention。**A100'in yukarısı 2-4 倍 hızlandırma; H100'in yukarısı FP8'in yukarısı 5-10 倍 hızlandırma.

2026 yılına kadar her iki üretim sonuç kümesi (vLLM, TensorRT-LLM, SGLang, llama.cpp) onları varsayır.

> 2026 yılına kadar, her iki ürün de yaygınlaşmıştır. Her üretim önerisi, Flash Dikkatini etkinleştirmeyi kabul eder.

> **【中文解读】**推理优化两大核心技术:KV Cache 存储已计算的钥匙/值向量,避免重复计算,将每步推理从O(N^2) 降至O(N);Flash Attention 通过分块计算避免 N×N矩阵写入HBM,在SRAM中完成所有计算,速度提升 2-10倍――

## Konsepten bir şey.

![KV cache growth and Flash Attention tiling](../assets/kv-cache-flash-attn.svg)

### KV önbelleği matematik

Dekodör katmanı, token başına:

> Her kodlama aşaması, her token, her baş:

```
bytes_per_token_per_layer = 2 * d_head * dtype_size
                          ^
                          K and V
```

32 katmanlı, 32 başlı, d_head=128, fp16 bir 7B modeli için:

> 对于 7B 模型(32 层、32 头、d_head=128、fp16):

```
per token per layer = 2 * 128 * 2 = 512 bytes
per token (32 layers) = 16 KB
per 32K context = 512 MB
```

> **【拓展：GQA 对 KV 缓存的影响】**GQA(Grouped-Query Attention) KV 头 from n_heads  reduced to n_kv_heads, directly等 proportion shorten小 KV 缓存。 örneğin Llama 3 70B'nin 64 查询头 / 8 KV 头配置, KV 缓存 压缩 8 倍── 128K 上下文中, bu da yaklaşık 4 GB 降至 0.5 GB KV 缓存, 长上下文推理的关键优化──

Llama 3 70B için (80 katman, d_head=128, GQA 8 KV başlı):

> Llama 3 için 70B ((80 层、d_head=128、GQA 8 个 KV 头):

```
per token per layer = 2 * 8 * 128 * 2 = 4096 bytes (4 KB)
per 32K context = 10.4 GB
```

Bu 10 GB'lık bir durum için Llama 3 70B'nin 128K bağlamında sadece KV önbelleği için 40 GB A100'in çoğu gerekir.

> Bu 10 GB bu yüzden Llama 3 70B 128K 上下文 下 缓存 KV 缓存(batch size 1) büyük kısmını 40 GB A100 显存所需します。

**GQA is the KV-cache win.**64 başlı MHA 32 GB'dır. MLA daha da sıkıştırır.

> **GQA 是 KV 缓存的胜利。**64 başlı MHA 32 GB'ye ihtiyaç duyar.
Boyutları sürükle ve önbelleğin boyutunun hareketini izle.

```figure
kv-cache-sizer
```

### Akşam dikkat  kapaklama hilesi

Standart dikkat:

> 标准注意力:

```
S = Q @ K^T          (HBM read, N×N, HBM write)
P = softmax(S)       (HBM read, HBM write)
O = P @ V            (HBM read, HBM write)
```

HBM'de 3 TB/s bant genişliği, SRAM'da 30 TB/s. Her HBM seferinde 10 oranında yavaşlama var.

> Üç kez HBM 往返── H100 üzerinde, HBM 带宽ı 3 TB/s; SRAM 30 TB/s── Her seferinde HBM  ziyaretinden sonra tüm verileri 10 kat daha yavaş tutmak için bir film üzerinde bulunur.

Akıllı Dikkat:

```
for each block of Q (tile size ~128 × 128):
    load Q_tile into SRAM
    for each block of K, V:
        load K_tile, V_tile into SRAM
        compute S_tile = Q_tile @ K_tile^T     (SRAM)
        running softmax aggregation             (SRAM)
        accumulate into O_tile                  (SRAM)
    write O_tile to HBM
```

Bir HBM seferı tek tek tekerlek.`O(N²)`- ...`O(N)`Geri geçiş, ileri geçişten bazı değerleri yeniden hesaplar ve onları saklar.

> Her bir kapak bir HBM ziyaretı...`O(N²)`降到 `O(N)`❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖

**Numerical trick.**Softmax çalışmasını sürdürüyor `(max, sum)`Flash dikkat, bit-tıpkı standart dikkat için çıkış hesaplar (modulo fp16 ilişkisizliği).

> **数值技巧。**运行时 softmax 跨 tile 维护 `(max, sum)`FP16 dışında, FP16'ın aynı çıkışını hesaplamak için, FP16'ın aynı çıkışını yaparak, FP16'ın aynı çıkışın aynı çıkışını yaparak, FP16'ın aynı çıkışın aynı çıkışını yaparak, FP16'ın aynı çıkışın aynı çıkışını yaparak, FP16'ın aynı çıkışın aynı çıkışını yaparak, FP16'ın aynı çıkışın aynı çıkışını yaparak, FP16'ın aynı çıkışın aynı çıkışını yaparak, FP16'ın aynı çıkışın aynı çıkışın aynı çıkışını yaparak, FP16'ın aynı çıkışın aynı çıkışın aynı çıkışın aynı çıkışın aynı çıkışına çıkışını yaparak, FP16'ın aynı çıkışın.

> **【中文解读】**Flash Dikkatinin temel teknikleri: dikkatini hesaplamak, GPU'nun hızlı SRAM'da yumuşak maksimum ve矩阵乘法'yı tamamlamak, N×N'in orta矩阵'ını yavaş hız HBM'ye yazmaktan kaçınmak.

> **【拓展：vLLM 的 PagedAttention】**PagedAttention(vLLM) KV 缓存'nı sabit büyüklükte "sayfa" olarak organize edecek, işletim sistemine benzer sanal内存. Bu da内存 parçaları problemini ortadan kaldıracak, çok sayıda并发请求'nin GPU 显存'yu yüksek verimli paylaşmasına yardımcı olacak.

**Version evolution:**

| Version | Year | Key change | Speedup on reference hardware |
|---------|------|-----------|-------------------------------|
| 版本 | 年份 | 关键变化 | 参考硬件上的加速 |
| Flash 1 | 2022 | Tiled SRAM kernel | 2× on A100 |
| Flash 2 | 2023 | Better parallelism, causal-first ordering | 3× on A100 |
| Flash 3 | 2024 | Hopper asynchrony, FP8 | 1.5–2× on H100 (~740 TFLOPs FP16) |
| Flash 4 | 2026 | Blackwell 5-stage pipeline, software exp2 | Inference-first (forward only initially) |

Flash 4 sadece fırlatma sırasında ilerleme kaydetmektedir. Eğitim hala Flash 3 kullanır. GQA ve varlen desteği Flash 4 için beklenmektedir (2026 ortalarında).

> Flash 4  yayınlama sırasında sadece destek önde yayılmak için.

### Spekülatör çözme  diğer gecikme kazan

Ucuz model N simgeler önerir. Büyük model tüm N'leri paralel olarak doğruluyor. Eğer doğrulama k simgeler kabul ederse, k nesiller için 1 büyük model ileri geçiş ödediğiniz. Tipik k = 35 kod ve prozda.

> 廉价模型提出 N 个代币――大模型并行验证所有 N 个―― eğer验证 k 个代币 kabul ederse, bir kez büyük modelle ileriye doğru yayılmakla k 个生成――代码和散文的典型 k=3-5―― elde edersiniz.

2026'da geçersiz olanlar:
- **EAGLE 2 / Medusa.**Verifikatörün gizli durumlarını paylaşan entegre taslak başlıkları. Kalite kaybı olmadan 2  3  hızlandırma.
  Çeviri:**EAGLE 2 / Medusa。**集成草案头,共享验证器的隐藏状态──2-3 倍加速,质量损失──
- **Speculative decoding with draft model.**İsteğe bağlı donanımlarda 2×4 hızlanma.
  Çeviri:**带草案模型的推测解码。**İsteğe bağlı olarak, bu durumun daha da artması için,
- **Lookahead decoding.**Jacobi iterasyonu, bir taslak modeli gerekmiyor.
  Çeviri:**前瞻解码。**Jacobi 代;不需要草案模型──小众但免费──

### Sürekli serileme

Klasik seri sonucu: en yavaş dizinin bitmesini bekle, sonra yeni bir seri başlat. Kısa cevaplar erken bitince GPU'yı harcıyor.

> Klasik toplama düşüncesi: en yavaş sırayı bekle, sonra yeni toplamalara başla.

Sürekli serileme (İlk olarak Orca'da, şimdi vLLM, TensorRT-LLM, SGLang'da gönderilmiştir): Eski istekler bittikten sonra yeni istekleri partiye değiştirin.

> 连续批处理(首次在Orca中发布,现在在vLLM、TensorRT-LLM、SGLang 中): Eski talep tamamlandıktan sonra hemen yeni talep değişime girdi.

### PagedAttention  KV önbelleği sanal bellek olarak

vLLM'nin başlık özelliği. KV önbelleği 16 token bloklarına ayrılır; bir sayfa tablosu mantıksal konumları fiziksel bloklara haritası yapar. KV'yi paralel örnekler (şekil arama, paralel örnekleme), hızlı önbelleğe sıcak değişim önlükleri ve defragman belleği arasında paylaşabilir.

> vLLM'nin temel özellikleri: KV 缓存 16 token blok dağıtımıyla; sayfa tablosu logik konumunu fiziki bloklara haritalama yapar.

## Yapın.
```figure
flash-attention-memory
```

## Yapın

Bakın .`code/main.py`Bu uygulamayı uyguluyoruz:

> 参见 `code/main.py`❖ Biz gerçekleştirmek:

1. Saf bir adam .`O(N²)`Gelişmiş dekodör.
   Çeviri: Bir sıradan`O(N²)`增量解码器──
2. A.`O(N)`KV-cached dekodör.
   Çeviri: Bir`O(N)`KV 缓存解码器──
3. Flash Attention'ın çalıştırma maksimum algoritmasını simüle eden bir softmax.
   Çinçe Çevirim: 运行时最大值的分块软max──

### Adım 1: KV önbelleği

```python
class KVCache:
    def __init__(self, n_layers, n_heads, d_head):
        self.K = [[[] for _ in range(n_heads)] for _ in range(n_layers)]
        self.V = [[[] for _ in range(n_heads)] for _ in range(n_layers)]

    def append(self, layer, head, k, v):
        self.K[layer][head].append(k)
        self.V[layer][head].append(v)

    def read(self, layer, head):
        return self.K[layer][head], self.V[layer][head]
```

Basit: her token için K ve V vektörlerini katmanlık, başlık listesinde büyütmeye devam edin.

> 简单: K、V 向量的 K、V 向量的每代币的逐层、逐头的列表中持续增加

### Adım 2: Plaklı softmax

```python
def tiled_softmax_dot(q, K, V, tile=4):
    """Flash-attention-style softmax(qK^T)V with running max/sum."""
    m = float("-inf")
    s = 0.0
    out = [0.0] * len(V[0])
    for start in range(0, len(K), tile):
        k_block = K[start:start + tile]
        v_block = V[start:start + tile]
        scores = [sum(qi * ki for qi, ki in zip(q, k)) for k in k_block]
        new_m = max(m, *scores)
        exp_old = math.exp(m - new_m) if m != float("-inf") else 0.0
        exp_new = [math.exp(sc - new_m) for sc in scores]
        s = s * exp_old + sum(exp_new)
        for j in range(len(out)):
            out[j] = out[j] * exp_old + sum(e * v[j] for e, v in zip(exp_new, v_block))
        m = new_m
    return [o / s for o in out]
```

Bit-iynet çıkış `softmax(qK) V`Bir çekimde, ama her zaman çalışma seti bir `tile × d_head`- Blok, tam değil.`N × d_head`- Evet .

> Bir kerelik`softmax(qK) V`Aynı çıkış, ama her zaman iş birliği sadece.`tile × d_head`-Büyük, tamamlanmamış.`N × d_head`- Evet.

### Adım 3: 100 token neslinde saf ve önbelleğe alınan kodlama ile karşılaştırın

Dikkat operasyonlarını say.`O(N²)`= 5050 .`O(N)`Kodu her ikisini de basıyor.

> 計算注意力操作次数──朴素:`O(N²)`= 5050──缓存:`O(N)`= 100¬代码会打印两者¬

## Çerçeveyi kullanın.

```python
# HuggingFace transformers auto-enables KV cache on decoder-only generate().
from transformers import AutoModelForCausalLM
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.2-3B",
    attn_implementation="flash_attention_2",  # use FA3 if Hopper
    torch_dtype="bfloat16",
)
# generate() uses KV cache automatically
```

VLLM üretimi:

> VLLM 生产部署:

```bash
pip install vllm
vllm serve meta-llama/Llama-3.1-70B-Instruct \
    --tensor-parallel-size 4 \
    --max-model-len 32768 \
    --enable-prefix-caching \
    --kv-cache-dtype fp8
```

Önbellek önbelleği istekler arasında büyük bir 2026 kazanç  aynı sistem prompt, birkaç atış örnekleri veya uzun bağlam belgesini tekrar kullanır KV aramalar arasında. Tekrarlanan araç istekleri ile ajan iş yükleri için önbellek önbelleği rutin olarak 5× throughput kazançtır.

> 跨请求的前缓存是2026 yılının büyük başarıları 相同的系统提示、少样本示例或长上下文文档在调用间重复使用 KV──

## İndirin . Ürünler .

Bakın .`outputs/skill-inference-optimizer.md`. Yetenek yeni bir sonucu uygulaması için dikkat uygulaması, KV önbelleği stratejisi, kuantitasyon ve spekülatör çözümü seçer.

> 参见 `outputs/skill-inference-optimizer.md`Bu beceriler yeni bir önerme ve önerme departmanı için dikkat çekiminin gerçekleşmesi için kullanılır.

## Egzersizler.

1. **Easy.**Çık .`code/main.py`- Naif ve önbelleğe alınmış dekodörlerin aynı çıkış ürettiğini onaylayın; op-count farkını not edin.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`code/main.py`❖ Kontrol edilmesi için basit ve kayda çözücü aynı çıkış üretir; dikkat işlem sayısı farkı。
2. **Medium.**Önbellek önbelleği önbelleği uygulaması: bir istek P ve birkaç tamamlama verildiğinde, KV önbelleğini doldurmak için P üzerinde bir ileri geçiş çalıştırın, sonra tamamlama başına dal.
   Çinçe çevirisi: 实现前缓存:给定提示 P 和多个补充,对 P 运行一次前向传播填充 KV 缓存,然后每个补充分支――测量与每次重编码 P 相比的速度提升――
3. **Hard.**Bir oyuncak uygulamak PagedAttention: KV önbelleği sabit 16 jeton bloklarında serbest liste ile. Bir dizi tamamlandığında, bloklarını havuza geri gönderin. Çeşitli uzunluklarla 1.000 sohbet tamamlamasını simüle edin. Hatırlama parçalanması vs. bitişik tahsis karşılaştırın.
   Çinçe Çevirimi:实现玩具版 PagedAttention:KV 缓存固定16 token 块加空列表。序列完成时归归块。模拟 1,000 个变长聊天补全──比较连续分配的内存碎片化差异──

## Anahtar Şartlar .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| KV cache | "The trick that makes decoding fast" | Stored K and V from every prefix token; new queries attend to them instead of recomputing. |
| KV 缓存 | "让解码变快的技巧" | 存储每个前缀 token 的 K 和 V；新查询对它们做注意力而非重新计算。 |
| HBM | "GPU main memory" | High Bandwidth Memory; 80 GB on H100, 192 GB on B200. ~3 TB/s bandwidth. |
| HBM | "GPU 主内存" | 高带宽内存；H100 上 80 GB，B200 上 192 GB。约 3 TB/s 带宽。 |
| SRAM | "On-chip memory" | Per-SM fast memory, ~256 KB per SM on H100. ~30 TB/s bandwidth. |
| SRAM | "片上内存" | 每 SM 的快速内存，H100 上每 SM 约 256 KB。约 30 TB/s 带宽。 |
| Flash Attention | "Tiled attention kernel" | Computes attention without materializing N×N in HBM. |
| Flash Attention | "分块注意力内核" | 不在 HBM 中生成 N×N 矩阵即完成注意力计算。 |
| Continuous batching | "No-wait batching" | Swap finished sequences out, new ones in, without draining the batch. |
| 连续批处理 | "无等待批处理" | 完成的序列换出，新的换入，无需排空批次。 |
| PagedAttention | "vLLM's headline" | KV cache allocated in fixed blocks with a page table; eliminates fragmentation. |
| PagedAttention | "vLLM 的核心特性" | KV 缓存以固定块分配加页表；消除碎片化。 |
| Prefix caching | "Reuse long prompts" | Cache KV for a shared prefix across requests; major cost cut for agents. |
| 前缀缓存 | "复用长提示" | 跨请求缓存共享前缀的 KV；代理场景大幅降低成本。 |
| Speculative decoding | "Draft + verify" | Cheap draft model proposes tokens; big model verifies k in one pass. |
| 推测解码 | "草案 + 验证" | 廉价草案模型提出 token；大模型一次验证 k 个。 |

## Daha fazla okumak

- [Dao et al. (2022). FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness](https://arxiv.org/abs/2205.14135) Flash 1.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri
- [Dao (2023). FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning](https://arxiv.org/abs/2307.08691) Flash 2.
  Çeviri:Flash Dikkat 2
- [Shah et al. (2024). FlashAttention-3: Fast and Accurate Attention with Asynchrony and Low-precision](https://arxiv.org/abs/2407.08608) Flash 3.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri
- [FlashAttention-4 release notes (Dao-AILab, 2026)](https://github.com/Dao-AILab/flash-attention) Blackwell 5 aşamalı boru hattı ve yazılım-exp2 hilesi; bu derste bahsedilen sadece ileriye atılma uyarıları için repo README'yi okuyun.
  Çeviri:Flash Attention 4  yayımlama açıklaması; Blackwell 5 阶段管道和软件 exp2 技巧。
- [Kwon et al. (2023). Efficient Memory Management for Large Language Model Serving with PagedAttention](https://arxiv.org/abs/2309.06180)- VLLM kağıdı.
  Çeviri:VLLM Sayfalar Dikkat
- [Leviathan et al. (2023). Fast Inference from Transformers via Speculative Decoding](https://arxiv.org/abs/2211.17192) Spec kodlaması.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri
- [Li et al. (2024). EAGLE: Speculative Sampling Requires Rethinking Feature Uncertainty](https://arxiv.org/abs/2401.15077) Örgütlerdeki bütünleşmiş taslak yaklaşımı için EAGLE-1/2 makalesi.
  Çeviri:Çeviri-1/2 论文,集成草案方法──
- [Cai et al. (2024). Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads](https://arxiv.org/abs/2401.10774) Medusa yaklaşımı, Eagle ile birlikte referans edildi.
  Çeviri: Medusa 论文,多解码头方法──
- [vLLM docs — PagedAttention](https://docs.vllm.ai/en/latest/design/kernel/paged_attention.html) 16 token blok ve sayfa tablo tasarımı üzerinde kanonik derin dalış.
  中文翻译:vLLM PagedAttention 文档,16 token 块和页表设计的深入解析──
