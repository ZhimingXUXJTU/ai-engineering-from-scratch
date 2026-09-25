# Sự chú ý nhiều đầu
# Nhiều chú ý

> Một đầu chú ý học một mối quan hệ một lần, tám đầu học tám đầu tự do, lấy nhiều hơn.

> Một chú ý đầu tiên để học một mối quan hệ.

> **【中文解读】**Nhiều đầu tập trung để mô hình tập trung vào các loại khác nhau của mối quan hệ: ngữ法、语义、位置等──GPT-3 có 96 đầu tập trung vào các lĩnh vực khác nhau.

**Type:** Build | **类型:** 动手
**Language:**Python**语言:**Python
**Prerequisites:** Phase 7 · 02 (Self-Attention from Scratch) | **前置知识:** 阶段 7 · 02（从零实现自注意力）
**Time:** ~75 minutes | **时间:** ~75 分钟

## Vấn đề  vấn đề giới thiệu

Một đầu tự chú ý đơn lẻ tính toán một matrix chú ý. Matrix đó nắm bắt một loại mối quan hệ  thường là một mối quan hệ giảm thiểu tổn thất trên bất kỳ tín hiệu đào tạo nào. Nếu dữ liệu của bạn có sự đồng thuận đối tượng-tên, tham chiếu đồng, bài phát biểu dài và phân đoạn ngữ pháp tất cả được dính vào nhau, một đầu đơn lẻ bôi chúng thành một phân phối tối đa mềm duy nhất và mất một nửa tín hiệu.

> 单个自注意头计算一个注意矩阵――这个矩阵捕获一种关系通常是最小化训练信号损失的那种关系――如果你的数据中的主题一致,共指消解,长程语篇和句法分块纠在一起,单个头会模糊它们成单个软max 分布,丢失半信号――

Sự cố từ bài báo Vaswani năm 2017: chạy một số chức năng chú ý song song, mỗi chức năng có dự đoán Q, K, V của riêng mình, và kết nối các đầu ra.`d_model / n_heads`- Tỷ lệ tổng số vẫn không thay đổi.

> 2017 修复方案:并行运行多个注意力函数, mỗi người có Q、K、V 投影, rồi拼接输出──每个头在维度为`d_model / n_heads`                                                                                                                                                                                                                                                              

Sự chú ý đa đầu là mặc định của mọi bộ biến đổi trong 2026 tàu. Vấn đề duy nhất là về * bao nhiêu đầu và liệu các phím và giá trị có chia sẻ dự đoán (Thăm tâm nhóm, Thăm tâm đa câu hỏi, Thăm tâm trần trần đa đầu).

> Nhiều đầu tập trung là định dạng mặc định của mỗi Transformer năm 2026。 tranh luận duy nhất là về * bao nhiêu* đầu và liệu các khóa và giá trị có chia sẻ dự án không?

> **【中文解读】**Một đầu tập trung chỉ có thể học một mô hình quan hệ, nhưng trong ngôn ngữ tự nhiên có nhiều loại quan hệ.

## Khái niệm cốt lõi

![Multi-head attention splits, attends, concatenates](../assets/multi-head-attention.svg)

**Split.**Nhận đi`X`hình dạng`(N, d_model)`. Dự án đến Q, K, V mỗi hình dạng `(N, d_model)`- Tái tạo lại`(N, n_heads, d_head)`nơi `d_head = d_model / n_heads`- Chuyển vào`(n_heads, N, d_head)`- Tôi không biết.

> **拆分。**取形为 `(N, d_model)`của `X`◊投影到形状各为 `(N, d_model)`của Q、K、V──重塑为`(N, n_heads, d_head)`, trong số đó `d_head = d_model / n_heads`                                                                                                                                                                                                                                                              `(n_heads, N, d_head)`

**Attend in parallel.**Điệu suất điểm-đánh giá trong mỗi đầu.`(N, d_head)`Các đầu hoạt động trên các vùng phụ khác nhau của việc nhúng và không bao giờ nói chuyện trong quá trình tính toán sự chú ý.

> **并行计算注意力。**Trong mỗi đầu trong hành trình thu hẹp tập trung tập trung.`(N, d_head)`头在嵌入的不同子空间上操作,在注意计算本身期间互不通信──

**Concatenate and project.**Lầu đầu quay lại `(N, d_model)`và nhân bằng một matrix đầu ra học `W_o`hình dạng`(d_model, d_model)`- `W_o`là nơi mà đầu người được pha trộn.

> **拼接并投影。**Sẽ được lắp ráp lại`(N, d_model)`Và nhân bằng các mô hình đầu ra của học tập`W_o`, hình dạng`(d_model, d_model)``W_o`Đó là nơi có thể trộn lẫn.

**Why it works.**Mỗi đầu có thể chuyên môn mà không cạnh tranh với các đầu khác về ngân sách đại diện. Các nghiên cứu thăm dò từ năm 20192024 cho thấy các vai trò đầu khác nhau: đầu vị trí, đầu tham gia vào mã thông báo trước đó, đầu sao chép, đầu thực thể có tên, đầu cảm ứng (được đặt nền tảng cho việc học trong bối cảnh).

> **为什么有效。**Mỗi đầu có thể được chuyên dụng mà không tranh giành với các đầu khác để thể hiện ngân sách. Nghiên cứu tìm kiếm năm 2019-2024 cho thấy các vai trò đầu khác nhau: vị trí đầu; quan tâm đến đầu đầu của một token trước đó; sao chép đầu; đặt tên vật thể đầu; đầu đầu đầu; nó là cơ sở của học văn học trên và dưới).

> **【中文解读】**三步走:Split(拆分到多个子空间)→ tham dự(每个头独立做注意力)→ Concat+Project(拼接并通过W_o 混合)。关键洞察: mỗi头在不同子空间中独立工作,不争夺表示资源──实验表明不同头确实学会了不同的"职责"──

> **【拓展：GQA 在 Llama 3 中的实际应用】**Llama 3 70B sử dụng 64 đầu truy vấn nhưng chỉ có 8 đầu KV, sẽ KV 缓存 bị nén gấp 8 lần.

**The 2026 lineage of variations:**

> **2026 年的变体谱系：**

| Variant | Q heads / Q 头数 | K/V heads / K/V 头数 | Used by / 使用者 |
|---------|---------|-----------|---------|
| Multi-head (MHA) / 多头 | N | N | GPT-2, BERT, T5 |
| Multi-query (MQA) / 多查询 | N | 1 | PaLM, Falcon |
| Grouped-query (GQA) / 分组查询 | N | G (e.g. N/8) | Llama 2 70B, Llama 3+, Qwen 2+, Mistral |
| Multi-head latent (MLA) / 多头潜在 | N | compressed to low-rank / 压缩为低秩 | DeepSeek-V2, V3 |

GQA là mặc định hiện đại bởi vì nó cắt giảm bộ nhớ cache KV bằng một nhân tố của `N/G`MLA đi xa hơn bằng cách nén K/V vào một không gian ẩn, sau đó chiếu lại vào thời gian tính toán  chi phí FLOPs, tiết kiệm nhiều bộ nhớ hơn.

> GQA là lựa chọn tiêu chuẩn hiện đại, vì nó sẽ làm giảm KV 缓存内存 `N/G`倍, đồng thời giữ chất lượng gần như hoàn chỉnh. MLA 通过将 K/V 压缩到隐藏空间进一步,然后在计算时投影回来,节省更多内存.

## Hãy xây dựng nó.
```figure
multihead-split
```

## Hãy xây dựng nó

### Bước 1: tách đầu khỏi sự chú ý đơn đầu mà chúng ta đã có. Bước 1: tách đầu khỏi sự chú ý đơn đầu.

Hãy lấy `SelfAttention`từ Bài học 02 và lấn nó bằng một cặp chia/concat.`code/main.py`cho một thực hiện numpy; logic là:

> 取第 02 课的 `SelfAttention`, dùng để chia tách /拼接 để đóng gói nó.`code/main.py`中的 numpy 实现; logic如下:

```python
def split_heads(X, n_heads):
    n, d = X.shape
    d_head = d // n_heads
    return X.reshape(n, n_heads, d_head).transpose(1, 0, 2)  # (heads, n, d_head)

def combine_heads(H):
    h, n, d_head = H.shape
    return H.transpose(1, 0, 2).reshape(n, h * d_head)
```

Một hình dạng lại và một chuyển thể. Không vòng lặp. Đây chính xác là những gì PyTorch làm dưới`nn.MultiheadAttention`- Tôi không biết.

> Một lần tái tạo và một lần chuyển đổi. Không có vòng lặp.`nn.MultiheadAttention`Những gì tầng dưới làm.

> **【中文解读】** `split_heads`和 `combine_heads`只是重塑+转换操作,无需循环――这就是GPU上高效的多头注意的原因它本质上就是批量矩阵乘法――

### Bước 2: Điệu suất điểm-đánh giá chú ý mỗi đầu

Mỗi đầu đều có một mảnh của riêng mình của Q, K, V. Sự chú ý trở thành một bộ đống:

> Mỗi đầu nhận được các mảnh Q、K、V của riêng mình.

```python
def mha_forward(X, W_q, W_k, W_v, W_o, n_heads):
    Q = X @ W_q
    K = X @ W_k
    V = X @ W_v
    Qh = split_heads(Q, n_heads)         # (heads, n, d_head)
    Kh = split_heads(K, n_heads)
    Vh = split_heads(V, n_heads)
    scores = Qh @ Kh.transpose(0, 2, 1) / np.sqrt(Qh.shape[-1])
    weights = softmax(scores, axis=-1)
    out = weights @ Vh                    # (heads, n, d_head)
    concat = combine_heads(out)
    return concat @ W_o, weights
```

Trên thiết bị thực`Qh @ Kh.transpose(...)`là một `bmm`GPU nhìn thấy một bộ hình dạng đơn lẻ`(heads, N, d_head) × (heads, d_head, N) -> (heads, N, N)`Thêm đầu là miễn phí.

> Trên thực tế,`Qh @ Kh.transpose(...)`Một lần `bmm`GPU nhìn thấy là hình dạng`(heads, N, d_head) × (heads, d_head, N) -> (heads, N, N)`Đơn vị số lượng khối lượng:

### Bước 3: Nhóm-Query Attention biến thể .

Chỉ có các dự báo khóa và giá trị thay đổi.`n_heads`nhóm; K và V nhận `n_kv_heads < n_heads`nhóm và được lặp lại để phù hợp với:

> Chỉ có sự thay đổi của các dự án quan trọng và giá trị.`n_heads`个组; K 和 V có `n_kv_heads < n_heads`个组,并被重复以匹配:

```python
def gqa_project(X, W, n_kv_heads, n_heads):
    kv = split_heads(X @ W, n_kv_heads)       # (kv_heads, n, d_head)
    repeat = n_heads // n_kv_heads
    return np.repeat(kv, repeat, axis=0)      # (n_heads, n, d_head)
```

Theo kết luận , điều này tiết kiệm được trí nhớ bởi vì chỉ có`n_kv_heads`Các bản sao sống trong cache KV, không `n_heads`Llama 3 70B sử dụng 64 đầu truy vấn với 8 đầu KV  một bộ thu nhỏ cache 8x.

> Trong thời gian suy nghĩ, nó tiết kiệm được bộ nhớ, bởi vì chỉ có `n_kv_heads`份副本 tồn tại trong KV 缓存, thay vì `n_heads`份──Llama 3 70B Sử dụng 64 đầu truy vấn và 8 đầu KV 8 倍 giảm lưu trữ

> **【拓展：MQA/GQA 在推理中的内存节约】**KV 缓存的大小与 KV 头数成正比──Llama 3 70B sử dụng 64 查询头, nhưng chỉ có 8 头 KV, sẽ KV 缓存压缩 8 lần── đối với 128K 上下文, điều này có nghĩa là tiết kiệm số GB 显存── đây là một cải tiến quan trọng của lý luận GQA 几乎 không mất chất lượng, nhưng giảm đáng kể chi phí lý luận──

### Bước 4: Hãy thử nghiệm những gì mỗi đầu đã học. Bước 4: Tìm hiểu những gì mỗi đầu đã học.

Đọc MHA trên một câu ngắn với 4 đầu.`(N, N)`bạn sẽ thấy các đầu khác nhau chọn ra cấu trúc khác nhau ngay cả với sự khởi tạo ngẫu nhiên đó là một phần tín hiệu, một phần chu trình đối xứng quay trong các tiểu không gian.

> Trong câu ngắn, sử dụng 4 đầu chạy MHA.`(N, N)`Bạn sẽ thấy ngay cả khi sử dụng tự động khởi tạo, các đầu khác nhau cũng sẽ chọn ra các cấu trúc khác nhau.

## Hãy sử dụng nó để thực hiện

Trong PyTorch, phiên bản một dòng:

> PyTorch 中,一行版本:

```python
import torch.nn as nn

mha = nn.MultiheadAttention(embed_dim=512, num_heads=8, batch_first=True)
```

GQA từ PyTorch 2.5+:

> GQA(PyTorch 2.5+):

```python
from torch.nn.functional import scaled_dot_product_attention

# scaled_dot_product_attention auto-dispatches Flash Attention on CUDA.
# For GQA, pass Q of shape (B, n_heads, N, d_head) and K,V of shape
# (B, n_kv_heads, N, d_head). PyTorch handles the repeat.
out = scaled_dot_product_attention(q, k, v, is_causal=True, enable_gqa=True)
```

**How many heads?**Quy tắc ngón tay từ các mô hình sản xuất vào năm 2026:

> **多少个头？**Luật kinh nghiệm sản xuất mô hình năm 2026:

| Model size / 模型大小 | d_model | n_heads | d_head |
|------------|---------|---------|--------|
| Small (~125M) / 小型 | 768 | 12 | 64 |
| Base (~350M) / 基础 | 1024 | 16 | 64 |
| Large (~1B) / 大型 | 2048 | 16 | 128 |
| Frontier (~70B) / 前沿 | 8192 | 64 | 128 |

`d_head`Hầu như luôn luôn hạ cánh ở 64 hoặc 128. Đó là đơn vị của một đầu có thể "xem".`sqrt(d_head)`; đi trên 256 và bạn sẽ mất lợi ích "nhiều chuyên gia nhỏ".

> `d_head`几乎总是64或128――它是一个头能"看"多少的量单位――低于32时,头开始与缩小因子`sqrt(d_head)`冲突; hơn 256 时, bạn đã mất đi những lợi ích của "những chuyên gia nhỏ"

## Chuyển nó đi.

Nhìn xem`outputs/skill-mha-configurator.md`. Kỹ năng này khuyến cáo số lượng đầu, số lượng đầu kv và chiến lược chiếu cho một biến thể mới với ngân sách tham số, chiều dài chuỗi và mục tiêu triển khai.

> 参见 `outputs/skill-mha-configurator.md` Kỹ năng này cho Transformer mới  đề xuất số lượng đầu  KV  số lượng đầu và chiến lược dự án, cho các tham số ngân sách  bước tiến và mục tiêu triển khai 

## Tập luyện bài tập

1. **Easy / 简单。**Hãy lấy MHA từ `code/main.py`và thay đổi`n_heads`từ 1 đến 16 với `d_model=64`- Làm việc này có thể giúp đỡ, làm cho cao điểm, hoặc làm tổn thương?
   取 `code/main.py`Trung  MHA, trong `d_model=64`Trong trường hợp cố định sẽ`n_heads`Từ 1 đổi thành 16 ⋅ trong một nhiệm vụ sao chép tổng hợp vẽ lỗ hổng mô hình đơn tầng nhỏ ⋅ nhiều hơn có ích ⋅ đạt được thời gian nền tảng có hại?

2. **Medium / 中等。**Thực hiện MQA (một đầu KV được chia sẻ trên tất cả các đầu truy vấn). đo số lượng số parameter giảm so với MHA đầy đủ. Xét số lượng KV-thủ nhớ nhỏ gọn ở suy luận cho N = 2048.
   实现 MQA(一个 KV 头在所有查询头间共享) ――测量与完整MHA相比参数下降多少──计算在 N=2048的推理时 KV 缓存大小缩减多少──

3. **Hard / 困难。**Thực hiện một phiên bản nhỏ của Multi-head Latent Attention: nén K, V đến một cấp độ`r`- Lưu trữ trong cache KV, giải nén vào thời điểm chú ý.`r`bộ nhớ cache vượt qua dưới 1/8 của MHA đầy đủ trong khi chất lượng vẫn trong vòng 1 bit của việc xác thực ppl?
   实现迷你版的多头潜伏注意:将 K,V 压缩为秩 `r`Trong KV 缓存 trong KV 缓存 trong KV 缓存, trong tập trung tính toán`r`Giá trị giảm lưu trữ trong bộ nhớ giảm xuống còn 1/8 của MHA hoàn chỉnh dưới đây, đồng thời chất lượng giữ trong 1 bit của sự bối rối kiểm tra?

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say / 人们怎么说 | What it actually means / 实际含义 |
|------|------------------------------|----------------------------------|
| Head / 头 | "A single attention circuit" / "一个注意力电路" | One Q/K/V projection of dimension `d_head = d_model / n_heads` with its own attention matrix. 维度为 `d_head = d_model / n_heads` 的一个 Q/K/V 投影，有自己的注意力矩阵。 |
| d_head | "Head dimension" / "头维度" | Per-head hidden width; almost always 64 or 128 in production. 每个头的隐藏宽度；生产中几乎总是 64 或 128。 |
| Split / combine / 拆分/合并 | "Reshape tricks" / "reshape 技巧" | `(N, d_model) ↔ (n_heads, N, d_head)` reshape+transpose around attention. 围绕注意力的 `(N, d_model) ↔ (n_heads, N, d_head)` reshape+transpose。 |
| W_o | "Output projection" / "输出投影" | `(d_model, d_model)` matrix applied after concatenating heads; where heads mix. 拼接头后应用的 `(d_model, d_model)` 矩阵；头混合的地方。 |
| MQA | "One KV head" / "一个 KV 头" | Multi-Query Attention: single shared K/V projection. Smallest KV cache, some quality loss. 多查询注意力：单个共享的 K/V 投影。最小 KV 缓存，有一些质量损失。 |
| GQA | "The default since Llama 2" / "Llama 2 之后的默认" | Grouped-Query Attention with `n_kv_heads < n_heads`; repeats to match Q. 分组查询注意力，`n_kv_heads < n_heads`；重复以匹配 Q。 |
| MLA | "DeepSeek's trick" / "DeepSeek 的技巧" | Multi-head Latent Attention: K,V compressed to low-rank latent, decompressed at attend time. 多头潜在注意力：K,V 压缩为低秩隐向量，在注意力计算时解压。 |
| Induction head / 归纳头 | "The circuit behind in-context learning" / "上下文学习背后的电路" | A pair of heads that detect previous occurrences and copy what followed them. 一对检测先前出现模式并复制后续内容的头。 |

## Xem thêm 延伸阅读

- [Vaswani et al. (2017). Attention Is All You Need §3.2.2](https://arxiv.org/abs/1706.03762) mô hình đầu đa đầu ban đầu.
  Vaswani 等人(2017)  原始多头规范──

- [Shazeer (2019). Fast Transformer Decoding: One Write-Head is All You Need](https://arxiv.org/abs/1911.02150) giấy tờ MQA.
  Shazeer(2019)  MQA 论文。

- [Ainslie et al. (2023). GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints](https://arxiv.org/abs/2305.13245) cách chuyển đổi MHA thành GQA sau khi đào tạo.
  Ainslie 等人(2023)  训练后如何将 MHA 转换为 GQA。

- [DeepSeek-AI (2024). DeepSeek-V2 Technical Report](https://arxiv.org/abs/2405.04434) MLA và tại sao nó đánh bại MHA / GQA trên bộ nhớ cache.
  DeepSeek-AI(2024)  MLA 及为何在缓存内存上击败 MHA/GQA。

- [Olsson et al. (2022). In-context Learning and Induction Heads](https://transformer-circuits.pub/2022/in-context-learning-and-induction-heads/index.html) nhìn cơ học về những gì đầu thực sự làm.
  Olsson 等人(2022)  phân tích cơ chế về các chức năng thực tế.

> **【拓展：Induction Heads 与上下文学习】**Nghiên cứu của Anthropic phát hiện ra, Transformer's up-down literature learning ability (tự học trong ngữ cảnh) chủ yếu được thực hiện bởi một loại tập trung được gọi là "đầu induktion" .
