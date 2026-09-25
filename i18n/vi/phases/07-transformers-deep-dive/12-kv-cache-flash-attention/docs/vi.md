# KV Cache, Flash Attention & Inference Optimization  KV Cache  Flash Attention và Optimization

> Trình luyện là song song và liên kết với FLOP. Thuyết định là liên kết với bộ nhớ.

> **【中文解读】**KV Cache 缓存已计算的钥匙/值 避免重复计算,是 LLM 推理加速的核心──Flash Attention 优化显存访问模式,减少显存使用──

**Type:** Hands-on | **类型:** 动手
**Language:**Python**语言:**Python
**Prerequisites:** Phase 7 · 02 (Self-Attention), Phase 7 · 05 (Full Transformer), Phase 7 · 07 (GPT) | **前置知识:** Phase 7 · 02 (Self-Attention), Phase 7 · 05 (Full Transformer), Phase 7 · 07 (GPT)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Vấn đề  vấn đề giới thiệu

Một máy giải mã tự động thâm nhập ngu ngốc có thể làm được `O(N²)`làm việc để tạo ra `N`token: ở mỗi bước nó tính lại sự chú ý trên tiền đề đầy đủ. Đối với một phản ứng 4K-token là 16M các hoạt động chú ý, hầu hết chúng là dư thừa. Mỗi trạng thái ẩn của một tiền đề token là xác định khi được tính toán.

> Một máy tự giải mã đơn giản`N`个 token 需要 `O(N²)`Ưu điểm: Mỗi bước đều có thể tính toán lại sự chú ý hoàn chỉnh. Đối với phản ứng của token 4K, đó là 16M lần hoạt động chú ý, phần lớn trong đó là dư thừa.

Ngoài ra, sự chú ý tự động di chuyển rất nhiều dữ liệu. Sự chú ý tiêu chuẩn hiện thực hóa một matrix điểm số N×N, đầu ra mềm dẻo N×d, đầu ra cuối cùng N×d đọc và viết quá nhiều cho HBM. Đối với N≥2K, sự chú ý bị ràng buộc trong bộ nhớ trước khi nó trở thành FLOP. Các hạt nhân chú ý cổ điển sử dụng GPU hiện đại ít hơn 410×.

> Ngoài ra, sự chú ý tự nó phải di chuyển một lượng lớn dữ liệu. Sự chú ý tiêu chuẩn sẽ tạo ra N×N phân số矩阵, N×d softmax, output, N×d, ultimate output, cho HBM.

Hai cách tối ưu hóa, cả hai từ Dao et al., đã đẩy suy luận biên giới từ "nước từ" sang "nhanh":

> 两个优化 ((都来自道人) sẽ đi từ "慢"推向"快":

1. **KV cache.**lưu trữ các vector K và V của mỗi token tiền tố. sự chú ý của mỗi token mới là một truy vấn so với các khóa được lưu trữ trong cache.`O(N²)`đến`O(N)`mỗi bước thế hệ.
   Trung ngữ翻译:**KV 缓存。**存储 mỗi token trước K và V 向量── mỗi token mới chú ý đến một lần truy vấn vào khóa lưu trữ── đưa ra ý kiến từ từng bước.`O(N²)`降低到 `O(N)`
2. **Flash Attention.**Đặt máy tính chú ý để các n×N matrix đầy đủ không bao giờ chạm vào HBM. Tất cả các softmax + matmul xảy ra trong SRAM. 24× tốc độ đồng hồ tường trên A100; 510× trên H100 với FP8.
   Trung ngữ翻译:**Flash Attention。**Để tập trung vào việc tính toán các khối, làm cho N×N 矩阵 hoàn chỉnh không bao giờ được ghi vào HBM。 tất cả các softmax + 矩阵乘法 đều được hoàn thành trong SRAM。A100 lên 2-4 lần tăng tốc;H100 lên FP8 có thể đạt đến 5-10 lần。

Đến năm 2026, cả hai đều phổ biến. Mỗi đống suy luận sản xuất (vLLM, TensorRT-LLM, SGLang, llama.cpp) giả định chúng.

> Đến năm 2026, cả hai đều đã phổ biến. Mỗi sản xuất đề xuất (vLLM、TensorRT-LLM、SGLang、llama.cpp) đều giả định sử dụng chúng.

> **【中文解读】**推理优化两大核心技术:KV Cache 存储已计算的钥匙/值向量,避免重复计算,将每步推理从O(N^2) 降至O(N);Flash Attention 通过分块计算避免N×N矩阵写入HBM,完成所有计算在SRAM,速度提升2-10倍――

## Khái niệm cốt lõi

![KV cache growth and Flash Attention tiling](../assets/kv-cache-flash-attn.svg)

### KV cache toán học

Mỗi lớp giải mã, mỗi token, mỗi đầu:

> Mỗi lớp giải mã, mỗi token, mỗi đầu:

```
bytes_per_token_per_layer = 2 * d_head * dtype_size
                          ^
                          K and V
```

Đối với mô hình 7B với 32 lớp, 32 đầu, d_head=128, fp16:

> Đối với 7B 模型(32 层、32 头、d_head=128、fp16):

```
per token per layer = 2 * 128 * 2 = 512 bytes
per token (32 layers) = 16 KB
per 32K context = 512 MB
```

> **【拓展：GQA 对 KV 缓存的影响】**GQA(Grouped-Query Attention) sẽ giảm đầu KV từ n_heads  giảm xuống n_kv_heads, trực tiếp等比例缩小 KV 缓存. Ví dụ: 64 查询头 / 8 KV 配置 của Llama 3 70B, sẽ KV 缓存压缩 8 lần. Trong 128K 上下文中, điều này giảm từ khoảng 4 GB  giảm xuống 0.5 GB KV 缓存, là quan trọng tối ưu hóa của suy nghĩ trên 下文.

Đối với Llama 3 70B (80 lớp, d_head=128, GQA với 8 đầu KV):

> Đối với Llama 3 70B ((80 层、d_head=128、GQA 8 个 KV 头):

```
per token per layer = 2 * 8 * 128 * 2 = 4096 bytes (4 KB)
per 32K context = 10.4 GB
```

Đó là lý do tại sao Llama 3 70B ở 128K cần hầu hết 40 GB A100 chỉ cho bộ nhớ cache KV ở kích thước batch 1.

> Đây là 10 GB vì sao Llama 3 70B trong 128K 上下文 下仅 KV 缓存(lượng lô 1) cần phần lớn 40 GB A100 显存――

**GQA is the KV-cache win.**MHA với 64 đầu sẽ là 32 GB. MLA nén hơn nữa.

> **GQA 是 KV 缓存的胜利。**64 đầu MHA  cần 32 GB. MLA  áp suất hơn nữa.
Nhổ kích thước và xem kích thước cache di chuyển. Nhấn chiều dài chuỗi hoặc hàng lên và xem nó thổi nhanh như thế nào qua một GPU duy nhất:

```figure
kv-cache-sizer
```

### Flash Attention  thủ thuật làm gạch

Sự chú ý tiêu chuẩn:

> 标准注意力:

```
S = Q @ K^T          (HBM read, N×N, HBM write)
P = softmax(S)       (HBM read, HBM write)
O = P @ V            (HBM read, HBM write)
```

Ba chuyến đi về và về của HBM. trên H100, băng thông HBM là 3 TB / s; SRAM là 30 TB / s. Mỗi chuyến đi của HBM là một sự chậm lại nhân tố 10 so với giữ mọi thứ trên chip.

> Trong H100 trên, HBM 带宽 là 3 TB/s; SRAM là 30 TB/s.

Lưu ý:

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

Một chuyến HBM mỗi tấm.`O(N²)`đến`O(N)`. Pass ngược tính lại một số giá trị từ pass phía trước thay vì lưu trữ chúng  một bộ nhớ khác giành chiến thắng.

> Mỗi tấm một lần HBM truy cập ⋅ tổng lưu trữ chiếm dụng từ `O(N²)`降到 `O(N)`反向传播 从前向传播中重新计算某些值而不是存储它们另一个内存优势

**Numerical trick.**Tăng tốc độ hoạt động của softmax`(max, sum)`Phân tích không phải là một cách gần gũi  Flash Attention tính toán đầu ra bit giống hệt với sự chú ý tiêu chuẩn (modulo fp16 không liên quan).

> **数值技巧。**运行时 softmax 跨 tile 维护 `(max, sum)`Đối với, đảm bảo kết quả kết hợp là chính xác. Không gần như.

> **【中文解读】**Kỹ năng cốt lõi của Flash Attention:将注意力计算分块(tiling), hoàn thành softmax 和矩阵乘法 trong GPU của SRAM, tránh viết n×N của trung bình矩阵 vào slowspeed HBM。 kỹ năng số lượng quan trọng là "运行时软max"跨tile 维护 (max, sum) 对, đảm bảo kết quả cuối cùng phù hợp hoàn toàn với tiêu chuẩn chú ý toán học, không gần gũi。

> **【拓展：vLLM 的 PagedAttention】**PagedAttention(vLLM) sẽ tổ chức KV 缓存 thành "页" cố định, giống như "hình" ảo của hệ điều hành. Điều này đã loại bỏ vấn đề các mảnh vỡ trong bộ nhớ, giúp nhiều yêu cầu được chia sẻ GPU hiệu quả cao.

**Version evolution:**

| Version | Year | Key change | Speedup on reference hardware |
|---------|------|-----------|-------------------------------|
| 版本 | 年份 | 关键变化 | 参考硬件上的加速 |
| Flash 1 | 2022 | Tiled SRAM kernel | 2× on A100 |
| Flash 2 | 2023 | Better parallelism, causal-first ordering | 3× on A100 |
| Flash 3 | 2024 | Hopper asynchrony, FP8 | 1.5–2× on H100 (~740 TFLOPs FP16) |
| Flash 4 | 2026 | Blackwell 5-stage pipeline, software exp2 | Inference-first (forward only initially) |

Flash 4 chỉ được tiến hành khi ra mắt. Đào tạo vẫn sử dụng Flash 3. GQA và varlen hỗ trợ cho Flash 4 đang chờ đợi (trung năm 2026).

> Flash 4 发布时仅支持前向传播;;训练仍使用 Flash 3;; GQA 和变长支持待定(2026年中)。

### Việc giải mã giả định  chiến thắng độ trễ khác

Mô hình rẻ tiền đề xuất N token. Mô hình lớn xác minh tất cả N song song. Nếu xác minh chấp nhận k token, bạn đã trả 1 thẻ chuyển tiếp mô hình lớn cho k thế hệ.

> 廉价模型提出N 个代币――大模型并行验证所有N 个―― Nếu验证 chấp nhận k 个代币, bạn sẽ sử dụng một mô hình lớn để truyền bá được k 个生成――代码和散文的典型 k=3-5――

2026 không phát hành:
- **EAGLE 2 / Medusa.**Bộ trưởng dự thảo tích hợp chia sẻ trạng thái ẩn của người xác minh. 23x tăng tốc mà không mất chất lượng.
  Trung ngữ翻译:**EAGLE 2 / Medusa。**集成草案头, chia sẻ trạng thái ẩn của chứng minh.
- **Speculative decoding with draft model.**2×4 tăng tốc trên phần cứng tiêu dùng.
  Trung ngữ翻译:**带草案模型的推测解码。**消费级硬件上 2-4 倍加速──
- **Lookahead decoding.**- Không cần mô hình dự thảo, nhưng miễn phí.
  Trung ngữ翻译:**前瞻解码。**Jacobi 代;不需要草案模型──小众但免费──

### Lượng hàng liên tục

Kết luận đợt cổ điển: chờ đợi chuỗi chậm nhất kết thúc, sau đó bắt đầu một đợt mới.

> 经典批量推理: chờ đợi quá trình chậm nhất hoàn thành, sau đó bắt đầu một loạt mới.

Lưu lượng liên tục (lưu lượng đầu tiên tại Orca, bây giờ tại vLLM, TensorRT-LLM, SGLang): trao đổi các yêu cầu mới vào lô ngay khi các yêu cầu cũ kết thúc.

> 连续批处理(首次在Orca中发布,现在在vLLM、TensorRT-LLM、SGLang 中): 旧请求完成后立即将新请求换入批次――典型聊天工作负载的吞吐量提升 5-10 倍――

### PagedAttention  KV cache như bộ nhớ ảo

Tính năng tiêu đề của vLLM. KV cache được phân bổ trong 16 khối mã thông báo; một bảng trang lập bản đồ vị trí logic cho các khối vật lý. Cho phép bạn chia sẻ KV trên các mẫu song song (hướng tìm kiếm, lấy mẫu song song), tiền đề hot-swap cho lưu trữ nhanh chóng, và bộ nhớ phân mảnh.

> Các tính năng cốt lõi của vLLM: KV 缓存 được phân phối bằng 16 token block; trang bảng sẽ hiển thị vị trí logic vào khối vật lý.

## Hãy xây dựng nó.
```figure
flash-attention-memory
```

## Hãy xây dựng nó

Nhìn xem`code/main.py`Chúng tôi thực hiện:

> 参见 `code/main.py`❖ Chúng tôi thực hiện:

1. Một kẻ ngây thơ .`O(N²)`decoder tăng trưởng.
   Trung ngữ翻译:一个朴素的`O(N²)`增量解码器──
2. A `O(N)`KV-cache decoder.
   Trung ngữ翻译:一个 `O(N)`KV 缓存解码器。
3. Một Softmax được làm bằng gạch mô phỏng thuật toán chạy tối đa của Flash Attention.
   Trung文翻译:一个模拟 Flash Attention 运行时最大值的分块软max──

### Bước 1: KV cache

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

Rất đơn giản: tiếp tục tăng trưởng các vector per token K, V trong các danh sách per layer, per head.

> 简单: trong danh sách từng cấp ‧ từng đầu tiếp tục thêm mỗi token của K、V 向量。

### Bước 2: Softmax được làm phay

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

Khả năng phát ra bit giống nhau với `softmax(qK) V`trong một lần chụp, nhưng bất cứ lúc nào bộ làm việc là một `tile × d_head`khối, không phải toàn bộ `N × d_head`- Tôi không biết.

> Với một lần `softmax(qK) V`Mỗi lần xuất phát giống nhau, nhưng bất cứ lúc nào tập hợp chỉ là`tile × d_head`块, chứ không hoàn chỉnh `N × d_head`

### Bước 3: So sánh mã hóa ngây thơ so với mã hóa được lưu trữ trong caching trên thế hệ 100 token

- Lưu ý các hoạt động chú ý.`O(N²)`= 5050. `O(N)`Mã in cả hai.

> 计算注意力操作次数──朴素:`O(N²)`= 5050──缓存:`O(N)`= 100¬代码会打印两者¬

## Hãy sử dụng nó để thực hiện

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

sản xuất vLLM:

> VLLM 生产部署:

```bash
pip install vllm
vllm serve meta-llama/Llama-3.1-70B-Instruct \
    --tensor-parallel-size 4 \
    --max-model-len 32768 \
    --enable-prefix-caching \
    --kv-cache-dtype fp8
```

Caching tiền đề trên các yêu cầu là một chiến thắng lớn 2026  cùng một hệ thống nhắc, vài lần chụp ví dụ, hoặc tài liệu ngữ cảnh dài sử dụng lại KV trên các cuộc gọi. Đối với tải trọng công việc của đại lý với nhắc lại các yêu cầu công cụ, Caching tiền đề thường là tăng thông qua 5x.

> 跨请求的前缓存是2026年重大胜利相同系统提示、少样本示例或长上下文文档在调用间重复使用 KV── đối với các tác nhân tải trọng của các提示重复工具提示, dự trữ trước thường mang lại 5 lần tăng dung lượng──

## Chuyển nó đi.

Nhìn xem`outputs/skill-inference-optimizer.md`. Khả năng chọn sự thực hiện chú ý, chiến lược cache KV, định lượng và giải mã suy đoán cho việc triển khai suy luận mới.

> 参见 `outputs/skill-inference-optimizer.md` Kỹ năng này cho các bộ phận mới của Bộ Cứu chọn tập trung vào việc thực hiện KV  Chiến lược dự trữ, định lượng và tính toán giải mã

## Tập luyện bài tập

1. **Easy.**Đi chạy`code/main.py`- Đảm bảo các máy giải mã ngây thơ và được lưu trữ trong cache tạo ra cùng một đầu ra; lưu ý sự khác biệt trong số op.
   Trung ngữ翻译:运行 `code/main.py`❖ xác nhận đơn giản và bộ nhớ giải mã tạo ra cùng một đầu ra; chú ý đến số lần hoạt động khác nhau.
2. **Medium.**Thực hiện bộ nhớ cache tiền tố: với một prompt P và một số hoàn thành, chạy một lần đi trước trên P để lấp đầy bộ nhớ cache KV, sau đó nhánh cho mỗi hoàn thành.
   Trung文翻译:实现前缓存:给定提示 P 和多个补充,对P 运行一次前向传播填充 KV 缓存,然后每个补充分支――测量与每次重新编码 P 相比的速度提升――
3. **Hard.**Thực hiện một đồ chơi PagedAttention: KV cache trong các khối 16 token cố định với một danh sách miễn phí. Khi một chuỗi kết thúc, trả lại các khối của nó cho hồ bơi. Mô phỏng 1.000 kết thúc trò chuyện với chiều dài khác nhau. So sánh phân mảnh bộ nhớ so với phân bổ liền kề.
   Trung文翻译:实现玩具版 PagedAttention:KV 缓存使用固定 16 token 块加空列表。序列完成时归归块。模拟 1,000 个变长聊天补全──比较与连续分配的内存碎片化差异──

## Từ khóa  Từ khóa nhanh chóng

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

## Xem thêm 延伸阅读

- [Dao et al. (2022). FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness](https://arxiv.org/abs/2205.14135) Flash 1.
  Trung文翻译:Flash Attention 1 论文。
- [Dao (2023). FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning](https://arxiv.org/abs/2307.08691) Flash 2.
  Trung文翻译:Flash Attention 2 论文。
- [Shah et al. (2024). FlashAttention-3: Fast and Accurate Attention with Asynchrony and Low-precision](https://arxiv.org/abs/2407.08608) Flash 3.
  Trung文翻译:Flash Attention 3 论文。
- [FlashAttention-4 release notes (Dao-AILab, 2026)](https://github.com/Dao-AILab/flash-attention) Blackwell 5 giai đoạn đường ống và trò chơi phần mềm-exp2; đọc repo README cho các cảnh báo phóng chỉ đi trước bài học này đề cập.
  Trung文翻译:Flash Attention 4 发布说明;Blackwell 5 阶段管道和软件 exp2 技巧。
- [Kwon et al. (2023). Efficient Memory Management for Large Language Model Serving with PagedAttention](https://arxiv.org/abs/2309.06180) giấy vLLM.
  中文翻译:vLLM PagedAttention 论文。
- [Leviathan et al. (2023). Fast Inference from Transformers via Speculative Decoding](https://arxiv.org/abs/2211.17192) Tự giải mã thông số.
  Trung ngữ翻译:推测解码论文。
- [Li et al. (2024). EAGLE: Speculative Sampling Requires Rethinking Feature Uncertainty](https://arxiv.org/abs/2401.15077) Bài báo EAGLE-1/2 cho phương pháp tiếp cận dự thảo tích hợp bài học đề cập.
  Trung ngữ翻译:EAGLE-1/2 论文,集成草案方法──
- [Cai et al. (2024). Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads](https://arxiv.org/abs/2401.10774) phương pháp Medusa được tham khảo cùng với Eagle.
  Trung ngữ翻译:Medusa 论文,多解码头方法──
- [vLLM docs — PagedAttention](https://docs.vllm.ai/en/latest/design/kernel/paged_attention.html) canonical deep dive trên 16 token block và trang-table thiết kế.
  Trung文翻译:vLLM PagedAttention 文档,16 token 块和页表设计的深入解析──
