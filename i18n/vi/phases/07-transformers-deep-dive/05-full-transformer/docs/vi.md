# Bộ biến đổi đầy đủ  Encoder + Decoder
# 完整 Transformer  编码器 + 解码器

> Sự chú ý là ngôi sao. Mọi thứ khác, những dư thừa, bình thường hóa, chuyển tiếp, sự chú ý qua nhau, là những cái bàn phế để bạn xếp nó sâu.

> chú ý là phần chủ yếu. Tất cả những thứ khác, kết nối còn lại, kết hợp, kết nối mạng, giao thông, đều để bạn có thể xếp chồng lên một cái bàn tay sâu hơn.

> **【中文解读】**Hãy tự chú ý, đa đầu, FFN, dư thừa, LayerNorm 组装 thành một bộ biến thể hoàn chỉnh.

**Type:** Build | **类型:** 动手
**Language:**Python**语言:**Python
**Prerequisites:** Phase 7 · 02 (Self-Attention), Phase 7 · 03 (Multi-Head Attention), Phase 7 · 04 (Positional Encoding) | **前置知识:** 阶段 7 · 02（自注意力），阶段 7 · 03（多头注意力），阶段 7 · 04（位置编码）
**Time:** ~75 minutes | **时间:** ~75 分钟

## Vấn đề  vấn đề giới thiệu

Một lớp chú ý đơn là một bộ thu hoạch tính năng, không phải là mô hình. Một matmul mỗi lớp không đủ dung lượng cho ngôn ngữ. Bạn cần độ sâu  và độ sâu phá vỡ mà không cần ống nước đúng.

> Một tầng chú ý là một loại máy tính, không phải là mô hình. Mỗi tầng có một khối lượng không đủ.

Báo Vaswani năm 2017 đã đóng gói sáu quyết định thiết kế biến một lớp chú ý thành một khối xếp chồng. Mỗi biến thể kể từ khi  chỉ có mã hóa (BERT), chỉ có mã hóa (GPT), chỉ có mã hóa (T5)  thừa kế cùng một bộ xương. Năm 2026 các khối đã được tinh chỉnh (RMSNorm, SwiGLU, pre-norm, RoPE) nhưng bộ xương là giống nhau.

> Năm 2017 Vaswani 论文打包了六个设计决策,将一个注意层变成可堆叠的块──此后每个变压器纯编码器(BERT) 、纯解码器(GPT) 、编码器-解码器(T5) 都继承了相同的骨架──2026年,这些块已经优化了(RMSNorm、SwiGLU、前归化、RoPE),但骨架完全相同──

Bài học này là bộ xương. Bài học tiếp theo chuyên về nó  06 cho các mã hóa, 07 cho các mã hóa, 08 cho mã hóa-các mã hóa.

> Bài viết này là cơ cấu. Bài tiếp theo là chuyên về nó.

> **【中文解读】**单个注意层只是一个特征提取器,不是完整模型――2017年论文将六个设计决策包装成可堆积的块:嵌入+位置编码、自注意力、FFN、残差连接、层归化、交叉注意力――所有后续变体 变体BERT、GPT、T5都继承相同的骨架――

## Khái niệm cốt lõi

![Encoder and decoder block internals, wired](../assets/full-transformer.svg)

### 6 bộ phận.

1. **Embedding + positional signal.**Địa chỉ → vector. Vị trí được tiêm qua RoPE (công nghệ hiện đại) hoặc sinusoidal (classic).
   **嵌入 + 位置信号。**Địa chỉ → 向量── thông qua RoPE(现代) hoặc正弦编码(经典) 注入位置──

2. **Self-attention.**Mỗi vị trí đều được bảo vệ bởi các máy giải mã.
   **自注意力。**Mỗi vị trí quan sát tất cả các vị trí khác.

3. **Feed-forward network (FFN).**MLP hai lớp theo vị trí: `W_2 · activation(W_1 · x)`Tỷ lệ mở rộng 4x theo mặc định.
   **前馈网络 (FFN)。**位置级两层 MLP:`W_2 · activation(W_1 · x)`◊默认扩展比 4×──

4. **Residual connection.** `x + sublayer(x)`Không có nó, gradient biến mất sau khoảng 6 lớp.
   **残差连接。** `x + sublayer(x)`Không có cái này, thang ở khoảng 6 tầng rồi biến mất.

5. **Layer normalization.** `LayerNorm`hoặc `RMSNorm`(công nghệ hiện đại) ổn định dòng lưu lượng dư thừa.
   **层归一化。** `LayerNorm`Hoặc`RMSNorm`(现代) 稳定残差流

6. **Cross-attention (decoder only).**Các truy vấn đến từ bộ giải mã, các khóa và giá trị từ đầu ra bộ giải mã.
   **交叉注意力（仅解码器）。**查询 từ giải mã, khóa và giá trị từ coder xuất.

### Khóa mã hóa (được sử dụng bởi BERT, T5 mã hóa) 编码器块
Xem một vector chảy qua một khối: sự chú ý trộn lẫn qua các vị trí, dư sẽ mang nó về phía trước, FFN biến đổi nó, và chuẩn giữ cho dòng chảy ổn định.

```figure
transformer-block
```

### Bloc mã hóa (được sử dụng bởi BERT, mã hóa T5)

```
x → LN → MHA(self) → + → LN → FFN → + → out
                     ^              ^
                     |              |
                     └── residual ──┘
```

Mã hóa là hai chiều, không che giấu, mọi vị trí đều thấy mọi vị trí.

> 编码器 là hai chiều. Không có ẩn chứa.

### Bloc decoder (được sử dụng bởi GPT, T5 decoder)

```
x → LN → MHA(masked self) → + → LN → MHA(cross to encoder) → + → LN → FFN → + → out
```

Các bộ giải mã có ba lớp phụ mỗi khối. trung tâm  sự chú ý chéo  là nơi duy nhất thông tin chảy từ bộ giải mã đến bộ giải mã. Trong một kiến trúc chỉ có trình giải mã (GPT), sự chú ý chéo bị bỏ qua và bạn chỉ có sự chú ý tự ẩn + FFN.

> Trong mỗi khối có ba tầng. Trong giữa đó, sự chú ý giao thông là nơi duy nhất thông tin từ bộ xử lý đến bộ xử lý. Trong cấu trúc của GPT, sự chú ý giao thông bị bỏ qua, bạn chỉ cần ẩn chứa sự chú ý tự + FFN.

### Trước chuẩn vs hậu chuẩn .

Bức giấy gốc: `x + sublayer(LN(x))`vs `LN(x + sublayer(x))`. Sau chuẩn bị mất đi sự ủng hộ vào khoảng năm 2019  việc đào tạo sâu hơn mà không cần được ấm áp cẩn thận.`LN`* trước * lớp phụ) là mặc định 2026: Llama, Qwen, GPT-3+, Mistral tất cả sử dụng nó.

> 原始论文:`x + sublayer(LN(x))`vs `LN(x + sublayer(x))`◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊`LN`Trong tầng lớp* trước*) là 2026 năm của默认:Llama、Qwen、GPT-3+、Mistral 都 sử dụng nó。

### 2026 là một khối được hiện đại hóa.

| Component / 组件 | 2017 | 2026 |
|-----------|------|------|
| Normalization / 归一化 | LayerNorm | RMSNorm |
| FFN activation / FFN 激活函数 | ReLU | SwiGLU |
| FFN expansion / FFN 扩展比 | 4× | 2.6×（SwiGLU 使用三个矩阵，总参数匹配） |
| Position / 位置编码 | Sinusoidal absolute / 绝对正弦 | RoPE |
| Attention / 注意力 | Full MHA | GQA (or MLA) |
| Bias terms / 偏置项 | Yes / 有 | No / 无 |

RMSNorm giảm trung tâm trung bình của LayerNorm (một lần trừ ít hơn), giúp tiết kiệm tính toán và là thực nghiệm ít nhất ổn định.`Swish(W1 x) ⊙ W3 x`) luôn vượt trội hơn ReLU/GELU FFN bằng ~ 0,5 điểm trong các bài báo Llama, PaLM và Qwen.

> RMSNorm đã loại bỏ trung tâm hóa trung bình của LayerNorm (một lần giảm), tiết kiệm lượng tính toán, kinh nghiệm ít nhất ổn định như vậy.`Swish(W1 x) ⊙ W3 x`) trong Llama、PaLM 和 Qwen 论文中一致地比 ReLU/GELU FFN 好约0.5 个困惑度点──

> **【中文解读】**2026 năm của现代 Transformer 块与 2017 năm gốc相比:LayerNorm→RMSNorm,ReLU→SwiGLU,后归一化→前归一化,绝对位置编码→RoPE,全多头注意力→GQA。 Mỗi phần cải tiến đều tiến bộ, nhưng kết hợp lại đã cải thiện đáng kể sự ổn định và chất lượng mô hình của bài tập。

> **【拓展：为什么 Decoder-only 成为主流】**Mặc dù cấu trúc mã hóa giải mã có ưu thế tự nhiên trong các nhiệm vụ như dịch, nhưng mô hình chỉ có Decoder (GPT、Llama) có thể sử dụng cùng một cấu trúc để xử lý và tạo ra nhiệm vụ, đào tạo mục tiêu và mở rộng đã được Chinchilla 定律验证. Đây chính là lý do tại sao hầu hết các mô hình lớn trước đây trong năm 2024-2026 được chọn Decoder-only.

### Số lượng tham số.

Một khối với `d_model = d`và mở rộng FFN `r`- Có thể là:

>  Đối với một `d_model = d`且FFN 扩展比为 `r`Các khối:

- MHA: `4 · d²`(Q, K, V, O dự đoán)
  MHA:`4 · d²`(Q、K、V、O 投影)
- FFN (SwiGLU): `3 · d · (r · d)`≈ ≈`3rd²`
  FFN(SwiGLU):`3 · d · (r · d)`≈ ≈`3rd²`
- Các tiêu chuẩn: không đáng kể
  归一化:可忽略

> **【拓展：参数计数与模型规模的实际意义】**Các tham số của biến thể chủ yếu tập trung vào tập trung vào tập trung vào các dự án ((4d^2) và FFN(khoảng 8d^2 cho SwiGLU) 中。Llama 3 8B Mỗi tầng khoảng 1.5B 参数,32 tầng cộng với khoảng 7B cộng với các lớp nhúng và đầu ra.

## Hãy xây dựng nó.

### Bước 1: Các khối xây dựng Bước 1: xây dựng mô-đun

Sử dụng cái nhỏ `Matrix`lớp từ Bài học 03 (được sao chép vào tệp này để độc lập):

> Sử dụng thứ 03 课中的微型 `Matrix`类( đã sao chép đến tài liệu này để giữ độc lập):

- `layer_norm(x, eps=1e-5)` trừ trung bình, chia bằng std.
  `layer_norm(x, eps=1e-5)` 减去平均值,除以标准差──
- `rms_norm(x, eps=1e-6)` chia bằng RMS. Không trừ trung bình.
  `rms_norm(x, eps=1e-6)` trừ RMS──不减平均值──
- `gelu(x)`và `silu(x) * W3 x`(SwiGLU).
  `gelu(x)`和 `silu(x) * W3 x`(SwiGLU) ✿
- `ffn_swiglu(x, W1, W2, W3)`- Tôi không biết.
- `encoder_block(x, params)`và `decoder_block(x, enc_out, params)`- Tôi không biết.

### Bước 2: Cụm một bộ mã hóa 2 tầng và một bộ giải mã 2 tầng. Bước 2: Kết nối bộ mã hóa 2 tầng và bộ giải mã 2 tầng.

Đặt chúng lên, chuyển đầu ra mã hóa vào mỗi bộ giải mã, thêm LN cuối cùng trước khi dự đoán đầu ra.

> 堆叠它们──将编码器输出传入每个解码器交叉注意力──在输出投影前添加最终 LN──

```python
def encode(tokens, params):
    x = embed(tokens, params.emb) + sinusoidal(len(tokens), params.d)
    for block in params.encoder_blocks:
        x = encoder_block(x, block)
    return x

def decode(target_tokens, encoder_out, params):
    x = embed(target_tokens, params.emb) + sinusoidal(len(target_tokens), params.d)
    for block in params.decoder_blocks:
        x = decoder_block(x, encoder_out, block)
    return x
```

### Bước 3: Đi trước trên một ví dụ đồ chơi . Bước 3: Đi trước để truyền trên ví dụ đồ chơi .

Đưa nguồn 6 token và mục tiêu 5 token qua.`(5, vocab)`Không có đào tạo, bài học này là về kiến trúc, không phải về sự mất mát.

> 输入 6 token 源和 5 token 目标──验证输出形状是 `(5, vocab)`❖ không tập luyện ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖

### Bước 4: Thay đổi thành RMSNorm + SwiGLU

Thay thế LayerNorm và ReLU-FFN bằng RMSNorm và SwiGLU. xác nhận hình dạng vẫn phù hợp. Đây là hiện đại hóa 2026 với một thay thế chức năng.

> Sử dụng RMSNorm 和 SwiGLU  thay thế LayerNorm 和 ReLU-FFN。 xác nhận hình dạng vẫn phù hợp── đây là thông qua một lần thay thế hàm thực hiện 2026 năm hiện đại hóa──

## Hãy sử dụng nó để thực hiện

Các thực hiện tham chiếu PyTorch/TF: `nn.TransformerEncoderLayer`- `nn.TransformerDecoderLayer`Nhưng hầu hết mã sản xuất 2026 đều có khối riêng vì:

> PyTorch/TF 参考实现:`nn.TransformerEncoderLayer``nn.TransformerDecoderLayer`Nhưng hầu hết các sản phẩm sản xuất năm 2026 tự xây dựng, vì:

- Flash Attention được gọi vào trong sự chú ý, không phải qua `nn.MultiheadAttention`- Tôi không biết.
  Flash Attention trong tập trung tập trung, không qua `nn.MultiheadAttention`
- GQA / MLA không có trong tham chiếu stdlib.
  GQA / MLA không trong tài liệu tham khảo tiêu chuẩn.
- RoPE, RMSNorm, SwiGLU không phải là các mặc định PyTorch.
  RoPE、RMSNorm、SwiGLU không phải là định giá của PyTorch。

**Encoder vs decoder vs encoder-decoder — when to pick:**

> **编码器 vs 解码器 vs 编码器-解码器——何时选择：**

| Need / 需求 | Pick / 选择 | Example / 示例 |
|------|------|---------|
| Classification, embeddings, QA over text / 分类、嵌入、文本 QA | Encoder-only / 纯编码器 | BERT, DeBERTa, ModernBERT |
| Text generation, chat, code, reasoning / 文本生成、聊天、代码、推理 | Decoder-only / 纯解码器 | GPT, Llama, Claude, Qwen |
| Structured input → structured output (translation, summarization) / 结构化转换 | Encoder-decoder / 编码器-解码器 | T5, BART, Whisper |

> **【中文解读】**三种架构的选择:Encoder-only(BERT)适合分类和嵌入;Decoder-only(GPT/Llama)适合生成和通用任务;Encoder-Decoder(T5/BART)适合有明确的"源序列"结构化转换任务──2026年的主流选择是Decoder-only,因为它的扩展性最好,训练最简洁──

> **【拓展：SwiGLU 为何优于 ReLU】**SwiGLU(Swish-Gated Linear Unit) thông qua cơ chế kiểm soát cửa để làm cho khả năng biểu hiện của FFN mạnh hơn. Các thí nghiệm của các mô hình như Llama, PaLM, Qwen cho thấy SwiGLU so với ReLU/GELU trong sự bối rối xây dựng ngôn ngữ thấp hơn khoảng 0,5 điểm. Mặc dù nó cần ba khối trọng lực thay vì hai, số tham số tăng 50%), nhưng thường thông qua sẽ mở rộng tỷ lệ từ 4x xuống còn 2.6x để bù đắp.

## Chuyển nó đi.

Nhìn xem`outputs/skill-transformer-block-reviewer.md`. Khả năng xem xét việc triển khai khối biến thể mới đối với các mặc định 2026 và đánh dấu các phần thiếu (pre-norm, RoPE, RMSNorm, GQA, FFN tỷ lệ mở rộng).

> 参见 `outputs/skill-transformer-block-reviewer.md` Kỹ năng này theo thiết lập mặc định năm 2026 kiểm tra các khối Transformer mới thực hiện,并 đánh dấu phần thiếu hụt.

## Tập luyện bài tập

1. **Easy / 简单。**Đếm các tham số trong block encoder của bạn ở `d_model=512, n_heads=8, ffn_expansion=4, swiglu=True`. Thiết lập bằng cách thực hiện khối và sử dụng `sum(p.numel() for p in block.parameters())`- Tôi không biết.
   计算 `d_model=512, n_heads=8, ffn_expansion=4, swiglu=True`时 encoder_block 的参数──通过实现块并使用 `sum(p.numel() for p in block.parameters())`验证。

2. **Medium / 中等。**Chuyển từ post-norm sang pre-norm. khởi động cả hai và đo chuẩn kích hoạt sau 12 lớp xếp chồng vào vào ngẫu nhiên.
   Từ chuyển đổi sau tập hợp thành tập hợp trước tập hợp. Từ tập hợp sau tập hợp thành tập hợp trước tập hợp.

3. **Hard / 困难。**Thực hiện một bộ mã hóa-chế lập 4 lớp trên một nhiệm vụ sao chép đồ chơi (cói `x`Trở 100 bước. báo cáo mất mát. Thay đổi trong RMSNorm + SwiGLU + RoPE  mất mát giảm?
   Trong việc làm việc làm việc`x`(b) thực hiện 4 tầng lập trình- giải trình máy.                                                                                                                                                                                                                                                        

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say / 人们怎么说 | What it actually means / 实际含义 |
|------|------------------------------|----------------------------------|
| Block / 块 | "One transformer layer" / "一个 Transformer 层" | Stack of norm + attention + norm + FFN, wrapped in residual connections. 归一化 + 注意力 + 归一化 + FFN 的堆叠，包裹在残差连接中。 |
| Residual / 残差连接 | "Skip connection" / "跳跃连接" | `x + f(x)` output; enables gradient flow through deep stacks. `x + f(x)` 输出；使梯度流能穿过深层堆叠。 |
| Pre-norm / 前归一化 | "Normalize before, not after" / "先归一化，不是后归一化" | Modern: `x + sublayer(LN(x))`. Trains deeper without warmup gymnastics. 现代：`x + sublayer(LN(x))`。无需预热技巧即可训练更深的网络。 |
| RMSNorm | "LayerNorm without the mean" / "没有均值的 LayerNorm" | Divide by RMS; one less op, same empirical stability. 除以 RMS；少一次操作，经验上同样稳定。 |
| SwiGLU | "The FFN everyone switched to" / "大家都换成的 FFN" | `Swish(W1 x) ⊙ W3 x → W2`. Beats ReLU/GELU on LM ppl. 在 LM 困惑度上击败 ReLU/GELU。 |
| Cross-attention / 交叉注意力 | "How the decoder sees the encoder" / "解码器如何看到编码器" | MHA with Q from decoder, K/V from encoder outputs. MHA 的 Q 来自解码器，K/V 来自编码器输出。 |
| FFN expansion / FFN 扩展比 | "How wide the middle MLP is" / "中间 MLP 有多宽" | Ratio of hidden-size to d_model, usually 4 or 2.6 (SwiGLU). 隐藏大小与 d_model 的比率，通常为 4 或 2.6（SwiGLU）。 |
| Bias-free / 无偏置 | "Drop the +b terms" / "去掉 +b 项" | Modern stacks omit biases in linear layers; slight ppl improvement, smaller model. 现代堆栈在线性层中省略偏置；轻微的困惑度改善，更小的模型。 |

## Xem thêm 延伸阅读

- [Vaswani et al. (2017). Attention Is All You Need](https://arxiv.org/abs/1706.03762) đặc điểm khối ban đầu.
  Vaswani 等人(2017)  原始块规范。

- [Xiong et al. (2020). On Layer Normalization in the Transformer Architecture](https://arxiv.org/abs/2002.04745) tại sao tiền chuẩn đánh bại hậu chuẩn sâu sắc.
  Xiong 等人(2020)  Tại sao trước khi tái hợp ở cấp độ sâu hơn sau khi tái hợp.

- [Zhang, Sennrich (2019). Root Mean Square Layer Normalization](https://arxiv.org/abs/1910.07467) RMSNorm.

- [Shazeer (2020). GLU Variants Improve Transformer](https://arxiv.org/abs/2002.05202) tờ SwiGLU.
  Shazeer(2020)  SwiGLU 论文。

- [HuggingFace `modeling_llama.py`](https://github.com/huggingface/transformers/blob/main/src/transformers/models/llama/modeling_llama.py) khối chỉ có decoder canonical 2026
  Nhấp mặt `modeling_llama.py` 2026                                                                                                                                                                                                                                                             
