# Mã hóa vị trí  Sinusoidal, RoPE, ALiBi
# 位置编码  正弦、RoPE、ALiBi

> Sự chú ý là không thay đổi. "Căn nuôi ngồi trên thảm" và "mát trên mèo trên tàu" tạo ra cùng một đầu ra mà không có tín hiệu vị trí. Ba thuật toán sửa chữa nó  mỗi một cược khác nhau về điều gì " vị trí " có nghĩa là.

> 注意力是排列不变的. "Căn khốn ngồi trên thảm" 和 "Căn khốn ngồi trên thảm" 在没有位置信号时产生相同输出.

> **【中文解读】**Transformer 没有位置信息,需要手动注入──RoPE là phương pháp sử dụng Llama, ALiBi 支持外推到更长序列──

**Type:** Build | **类型:** 动手
**Language:**Python**语言:**Python
**Prerequisites:** Phase 7 · 02 (Self-Attention), Phase 7 · 03 (Multi-Head Attention) | **前置知识:** 阶段 7 · 02（自注意力），阶段 7 · 03（多头注意力）
**Time:** ~45 minutes | **时间:** ~45 分钟

## Vấn đề  vấn đề giới thiệu

Sự chú ý của sản phẩm điểm quy mô là mù thứ tự.`softmax(Q K^T / √d) V`được tính từ sự tương đồng cặp.`X`Không có gì trong sự chú ý quan tâm về vị trí.

> 缩放点积注意力是顺序无关的──注意力矩阵 `softmax(Q K^T / √d) V`Từ thành lập đối với tính toán tương tự đến.`X`Trong đó, các hành trình, các hành trình ra ngoài cũng bị rối loạn như vậy.

Đó không phải là một lỗi trong một mô hình túi từ. Đối với ngôn ngữ, mã, âm thanh, video  bất cứ điều gì mà thứ tự mang ý nghĩa  nó là chết người.

> Trong mô hình từ, đây không phải là lỗi. Nhưng đối với ngôn ngữ, mã, âm thanh, video, bất kỳ thứ tự nào mang ý nghĩa của nó là chết người.

Trình sửa là để đưa vị trí vào các nội dung bằng cách nào đó.

> Phương pháp sửa chữa là một cách nào đó sẽ được đặt vào.

1. **Absolute sinusoidal**(Vaswani 2017). Thêm `sin/cos`Đơn giản, không thể học được, không thể phân tích tốt hơn các chiều dài được đào tạo.
   **绝对正弦编码**(Vaswani 2017):`sin/cos`+ đến được nhúng trên. đơn giản. Không cần học.

2. **RoPE — Rotary Position Embeddings**(Su 2021). Chuyển các vector Q và K theo một góc tương xứng với vị trí. Mã hóa vị trí * tương đối * trực tiếp trong sản phẩm chấm.
   **RoPE — 旋转位置嵌入**(Su 2021) ・按与位置成正比的角度旋转 Q 和 K 向量──直接在点积中编码*相对*位置──2026年占主导地位──

3. **ALiBi — Attention with Linear Biases**(Bấm vào năm 2022). Trượt các nhúng hoàn toàn; thêm một hình phạt tuyến tính mỗi đầu cho điểm chú ý dựa trên khoảng cách.
   **ALiBi — 带线性偏置的注意力**(Báo chí 2022):  hoàn toàn nhảy qua nhúng; tùy thuộc vào khoảng cách để chú ý phần tử thêm mỗi đầu của hình phạt: 

Tính đến năm 2026, hầu hết các mô hình mở biên giới đều sử dụng RoPE: Llama 2/3/4, Qwen 2/3, Mistral, Mixtral, DeepSeek-V3, Kimi. Một số mô hình ngữ cảnh dài sử dụng ALiBi hoặc các biến thể hiện đại của nó.

> 截至 2026年, cơ bản mỗi mô hình mở nguồn phía trước đều sử dụng RoPE:Llama 2/3/4、Qwen 2/3、Mistral、Mixtral、DeepSeek-V3、Kimi。

> **【中文解读】**Bản thân sự chú ý là thứ tự không thay đổi, sự xuất hiện chỉ là đối với sự rối loạn.

## Khái niệm cốt lõi

![Sinusoidal absolute vs RoPE rotations vs ALiBi distance bias](../assets/positional-encoding.svg)

### - Tự nhiên. - Tự nhiên.

Lập trước một matrix cố định `PE`hình dạng`(max_len, d_model)`- Có thể là:

> 预计算一个固定矩阵 `PE`, hình dạng`(max_len, d_model)`- Có thể là:

```
PE[pos, 2i]   = sin(pos / 10000^(2i / d_model))
PE[pos, 2i+1] = cos(pos / 10000^(2i / d_model))
```

Vậy thì`X' = X + PE[:N]`Mỗi chiều là một hình âm ở tần số khác nhau. mô hình học cách đọc vị trí từ mô hình pha.`max_len`: không có gì cho mô hình biết điều gì xảy ra ở vị trí 2048 khi nó chỉ thấy vị trí 02047.

> Rồi trong chú ý trước`X' = X + PE[:N]`◊ mỗi chiều là một dòng dây có tần suất khác nhau.`max_len` ngoài thất bại: mô hình chỉ nhìn thấy vị trí 0-2047 时, không có gì nói cho nó biết vị trí 2048 sẽ xảy ra gì 

### RoPE quay vị trí nhập

Chuyển các vector Q và K (không phải nhúng).`(2i, 2i+1)`- Có thể là:

> 旋转 Q 和 K 向量(không được đặt) ⋅ đối với một đối với kích thước `(2i, 2i+1)`- Có thể là:

```
[q'_2i    ]   [ cos(pos·θ_i)  -sin(pos·θ_i) ] [q_2i   ]
[q'_2i+1  ] = [ sin(pos·θ_i)   cos(pos·θ_i) ] [q_2i+1 ]

θ_i = base^(-2i / d_head),  base = 10000 by default
```

Lấy cùng một xoay vào các phím với vị trí `pos_k`. sản phẩm điểm `q'_m · k'_n`trở thành một chức năng của `(m - n)`Chỉ riêng mình.**the attention score depends only on the relative distance**Mặc dù quay được khóa khỏi vị trí tuyệt đối.

> Đối với vị trí ứng dụng chính`pos_k`                                                                                                                                                                                                                                                              `q'_m · k'_n` biến thành chỉ `(m - n)`của hàm:**注意力分数只取决于相对距离**Ngay cả khi quay được dựa trên vị trí tuyệt đối...

> **【中文解读】**Điểm đặc biệt của RoPE: Mặc dù góc quay dựa trên vị trí tuyệt đối, nhưng điểm tích của Q·K chỉ phụ thuộc vào khoảng cách tương đối (m-n) ―― điều này có nghĩa là mô hình tự nhiên học đã có mối quan hệ vị trí tương đối―― điều chỉnh cơ sở 参数 cũng có thể thực hiện dài trên dưới dưới ngoài, Llama 3 chính là thông qua cách này từ 8K  mở rộng lên 128K 上 下文。

> **【拓展：RoPE 在 Llama 3 中的长上下文扩展】**Llama 3 通过 YaRN(Một phương pháp khác của RoPE mở rộngN) sẽ mở rộng từ 8K lên 128K.

Lợi ích của RoPE: `base`Llama 3 mở rộng từ 8K đến 128K theo cách này.

> 扩展 RoPE:`base`Llama 3 là như thế từ 8K  mở rộng đến 128K 上下文的。

### ALiBi ơi, hãy chú ý đến sự chuyển hướng về đường dây.

Trượt qua thủ thuật nhúng vào.

> 跳过嵌入技巧──直接偏置注意力分数:

```
attn_score[i, j] = (q_i · k_j) / √d  -  m_h · |i - j|
```

Ở đâu `m_h`là một đường ngốc cụ thể cho đầu (ví dụ `1 / 2^(8·h/H)`Các token gần hơn được tăng cường; các token xa bị phạt. Không có chi phí thời gian đào tạo.

> Trong số đó `m_h`là một tỷ lệ nghiêng cụ thể của đầu`1 / 2^(8·h/H)`(■)                                                                                                                                                                                                                                                              

### Những gì để chọn vào năm 2026

| Variant / 变体 | Extrapolation / 外推能力 | Training cost / 训练成本 | Used by / 使用者 |
|---------|---------------|---------------|---------|
| Absolute sinusoidal / 绝对正弦编码 | poor / 差 | free / 免费 | original transformer, early BERT |
| Learned absolute / 学习式绝对编码 | none / 无 | tiny / 微小 | GPT-2, GPT-3 |
| RoPE | good with scaling / 良好（带缩放） | free / 免费 | Llama 2/3/4, Qwen 2/3, Mistral, DeepSeek-V3, Kimi |
| RoPE + YaRN | excellent / 优秀 | fine-tune stage / 微调阶段 | Qwen2-1M, Llama 3.1 128K |
| ALiBi | excellent / 优秀 | free / 免费 | BLOOM, MPT, Baichuan |

RoPE thắng vì nó thu hút sự chú ý mà không thay đổi kiến trúc, mã hóa vị trí tương đối, và nó `base`siêu tham số cung cấp một nút sạch cho điều chỉnh tinh tế trong bối cảnh dài.

> RoPE 胜出 là vì nó không cần phải thay đổi cấu trúc, nó có thể đưa vào sự chú ý, lập trình đối với vị trí, và nó`base`超参数长上下文微调提供了清晰调节旋──

> **【中文解读】**Sự lựa chọn của định vị năm 2026 rất rõ ràng: dự án mới mặc định RoPE── nó không thay đổi cấu trúc, định vị so với vị trí, và thông qua cơ sở các tham số cung cấp một đường rõ ràng của长上下文微调── chỉ có ở cực extreme ngoài trường hợp.

> **【拓展：位置编码对长上下文 RAG 的影响】**Trong hệ thống RAG, định vị mã hóa ảnh hưởng trực tiếp đến khả năng xử lý tài liệu dài. RoPE + YaRN 让 Llama 3 能 xử lý các token 128K trên, có nghĩa là có thể xử lý một lần khoảng 300 trang tài liệu.
```figure
rope-explorer
```

## Hãy xây dựng nó

## Hãy xây dựng nó.

### Bước 1: Mã hóa hình âm đạo. Bước 1: mã hóa dây chân chính.

Nhìn xem`code/main.py`Một tính toán 4 dòng:

> 参见 `code/main.py`△4 行计算:

```python
def sinusoidal(N, d):
    pe = [[0.0] * d for _ in range(N)]
    for pos in range(N):
        for i in range(d // 2):
            theta = pos / (10000 ** (2 * i / d))
            pe[pos][2 * i]     = math.sin(theta)
            pe[pos][2 * i + 1] = math.cos(theta)
    return pe
```

Thêm vào các matrix nhúng trước lớp chú ý đầu tiên.

> Trước khi tập trung vào lớp đầu tiên, nó sẽ được thêm vào các mô hình.

### Bước 2: RoPE được áp dụng cho Q, K. Bước 2: RoPE sẽ được áp dụng cho Q.K.

RoPE hoạt động tại chỗ trên Q và K. Đối với mỗi cặp bóng tối:

> RoPE đối với Q và K hoạt động nguyên bản.

```python
def apply_rope(x, pos, base=10000):
    d = len(x)
    out = list(x)
    for i in range(d // 2):
        theta = pos / (base ** (2 * i / d))
        c, s = math.cos(theta), math.sin(theta)
        a, b = x[2 * i], x[2 * i + 1]
        out[2 * i]     = a * c - b * s
        out[2 * i + 1] = a * s + b * c
    return out
```

Quan trọng: áp dụng cùng một hàm cho Q tại vị trí `m`và K ở vị trí `n`Sản phẩm của họ có thể nhận được một`cos((m-n)·θ_i)`chú ý học được vị trí tương đối miễn phí.

> 关键: đối với vị trí `m`của Q và vị trí `n`K  ứng dụng cùng một hàm.`cos((m-n)·θ_i)`Vì con ơi, chú ý miễn phí học được vị trí tương đối.

> **【中文解读】**Trọng tâm thực hiện của RoPE: đối với mỗi đối số kích thước (2i, 2i+1) của Q và K làm vị trí liên quan đến xoay quanh.

### Bước 3: ALiBi nghiêng và thiên vị  bước 3: ALiBi  độ nghiêng và thiên vị

```python
def alibi_bias(n_heads, seq_len):
    # slope_h = 2 ** (-8 * h / n_heads) for h = 1..n_heads
    slopes = [2 ** (-8 * (h + 1) / n_heads) for h in range(n_heads)]
    bias = []
    for m in slopes:
        row = [[-m * abs(i - j) for j in range(seq_len)] for i in range(seq_len)]
        bias.append(row)
    return bias  # add to attention scores before softmax
```

Thêm `bias[h]`đến `(seq_len, seq_len)`điểm chú ý của đầu `h`, sau đó là Softmax.

> sẽ`bias[h]`Chuyện này`h`của `(seq_len, seq_len)`chú ý, rồi mềm tối đa.

### Bước 4: Kiểm tra thuộc tính tương đối khoảng cách của RoPE . Bước 4: Kiểm tra thuộc tính tương đối khoảng cách của RoPE

Chọn hai vector ngẫu nhiên `a, b`- Chuyển đi`(pos_a, pos_b)`Rồi rồi.`(pos_a + k, pos_b + k)`. Cả hai sản phẩm điểm phải phù hợp trong sai lầm điểm nổi. Cất lượng đó là toàn bộ điểm của RoPE  nó không thay đổi đối với sự bù đắp tuyệt đối, chỉ có khoảng cách tương đối quan trọng.

>  chọn hai tùy biến `a, b` `(pos_a, pos_b)`旋转──然后用 `(pos_a + k, pos_b + k)`Chuyển: hai điểm trong vòng tròn điểm phải phù hợp.

> **【拓展：位置编码的历史演进】**Từ Vaswani(2017) của mã mã âm đạo tuyệt đối, đến GPT-2/3 của learning mode position embedded, tiếp tục đến RoPE(2021) và ALiBi(2022), mã vị trí đã trải qua sự chuyển đổi từ " vị trí tuyệt đối " đến " vị trí tương đối " . Thành công của RoPE là nó không thay đổi cấu trúc chú ý, trực tiếp trong Q / K quay trong mã hóa tương đối vị trí, đồng thời cung cấp một con đường rõ ràng của việc mở rộng văn bản trên dài.

## Hãy sử dụng nó để thực hiện

PyTorch 2.5+ tàu RoPE tiện ích trong `torch.nn.functional`Hầu hết mã sản xuất sử dụng`flash_attn`hoặc `xformers`nơi RoPE được áp dụng bên trong hạt nhân chú ý.

> PyTorch 2.5+`torch.nn.functional`中内置了 RoPE 工具──大多数生产代码使用 `flash_attn`Hoặc`xformers`, trong đó RoPE trong tập trung trong nội tâm ứng dụng.

```python
from transformers import AutoModel
model = AutoModel.from_pretrained("meta-llama/Llama-3.2-3B")
# model.config.rope_scaling → {"type": "yarn", "factor": 32.0, "original_max_position_embeddings": 8192}
```

**Long-context tricks in 2026:**

> **2026 年的长上下文技巧：**

- **NTK-aware interpolation.**Tái quy mô `base`đến`base * (scale_factor)^(d/(d-2))`khi mở rộng từ 4K đến 16K+.
  **NTK-aware 插值。**Khi từ 4K  mở rộng đến 16K + 时,将 `base`重新缩放为 `base * (scale_factor)^(d/(d-2))`
- **YaRN.**Sự phân tích thông minh hơn để bảo vệ sự chú ý vào các bối cảnh dài. Llama 3.1 128K sử dụng nó.
  **YaRN。**Hơn nữa, tăng thêm năng lượng, giữ lại sự chú ý trên văn bản dưới đây.
- **LongRoPE.**Phương pháp 2024 của Microsoft sử dụng tìm kiếm tiến hóa để chọn các yếu tố trên quy mô kích thước. Phi-3-Long sử dụng nó.
  **LongRoPE。**Microsoft 2024 năm phương pháp, sử dụng tiến hóa tìm kiếm chọn cho mỗi kích thước nhân nhân rộng.
- **Position interpolation + fine-tuning.**Chỉ cần thu hẹp vị trí bằng nhân rộng và điều chỉnh tốt cho token 15B.
  **位置插值 + 微调。**Chỉ cần theo quy mô mở rộng và giảm vị trí và điều chỉnh 1-5B token.

## Chuyển nó đi.

Nhìn xem`outputs/skill-positional-encoding-picker.md`. Kỹ năng chọn một chiến lược mã hóa cho một mô hình mới do chiều dài bối cảnh mục tiêu, nhu cầu phân tích và ngân sách đào tạo.

> 参见 `outputs/skill-positional-encoding-picker.md` Kỹ năng này cho mô hình mới chọn chiến lược lập trình, cho mục tiêu định trên văn bản dài hạn, nhu cầu và ngân sách đào tạo.

## Tập luyện bài tập

1. **Easy / 简单。**Đặt đường chân lưng `PE`Matrix như là một bản đồ nhiệt cho `max_len=512, d=128`- Đảm nhận mô hình "những dải mở rộng hơn khi chỉ số kích thước tăng lên".
   将正弦 `PE`矩阵绘制为`max_len=512, d=128`                                                                                                                                                                                                                                                              

2. **Medium / 中等。**Thực hiện quy mô RoPE có ý thức NTK. Tập một LM nhỏ trên các chuỗi dài 256, sau đó thử nghiệm trên dài 1024 với và không quy mô. đo độ phức tạp.
   实现 NTK-aware RoPE 缩放―― tập luyện một LM nhỏ trên chuỗi 256 độ dài, sau đó trong tình huống có缩放 và không缩放, thử nghiệm độ dài 1024― đo độ bối rối――

3. **Hard / 困难。**Thực hiện ALiBi và RoPE trong cùng một mô-đun chú ý. Trình chuyển đổi 4 lớp trên một nhiệm vụ sao chép với chuỗi dài 512. Phân tích đến 2048 tại thời điểm thử nghiệm. So sánh sự suy giảm.
   Trong cùng một mô-đun tập trung thực hiện ALiBi và RoPE. Trong nhiệm vụ sao chép của chuỗi độ dài 512 tập luyện một Transformer 4 tầng. Trong thời gian thử nghiệm được đưa ra vào năm 2048.

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say / 人们怎么说 | What it actually means / 实际含义 |
|------|------------------------------|----------------------------------|
| Positional encoding / 位置编码 | "Tells attention about order" / "告诉注意力顺序" | Any signal added to embeddings or attention that encodes position. 添加到嵌入或注意力中编码位置的任何信号。 |
| Sinusoidal / 正弦编码 | "The original one" / "原始的那种" | `sin/cos` at geometric frequencies added to embeddings; doesn't extrapolate. 以几何频率加到嵌入上的 `sin/cos`；不能外推。 |
| RoPE | "Rotary embeddings" / "旋转嵌入" | Rotate Q, K by position-dependent angle; dot product encodes relative distance. 按位置相关角度旋转 Q、K；点积编码相对距离。 |
| ALiBi | "Linear bias trick" / "线性偏置技巧" | Add `-m·|i-j|` to attention scores; no embedding needed, great extrapolation. 向注意力分数添加 `-m·|i-j|`；无需嵌入，出色的外推。 |
| base | "RoPE's knob" / "RoPE 的旋钮" | The frequency scaler in RoPE; increase to extend context at inference. RoPE 中的频率缩放器；增大以在推理时扩展上下文。 |
| NTK-aware | "A RoPE scaling trick" / "RoPE 缩放技巧" | Rescale `base` so high-frequency dims aren't squeezed when context expands. 重新缩放 `base` 使高频维度在上下文扩展时不被挤压。 |
| YaRN | "The fancy one" / "高级的那种" | Per-dimension interpolation+extrapolation that preserves attention entropy. 保留注意力熵的每维度插值+外推。 |
| Extrapolation / 外推 | "Works beyond trained length" / "超过训练长度还能用" | Can the position scheme serve correct output past `max_len` seen in training? 位置方案能否在训练中见过的 `max_len` 之后提供正确的输出？ |

## Xem thêm 延伸阅读

- [Vaswani et al. (2017). Attention Is All You Need §3.5](https://arxiv.org/abs/1706.03762) hình âm đạo gốc.
  Vaswani 等人(2017)  原始正弦编码──

- [Su et al. (2021). RoFormer: Enhanced Transformer with Rotary Position Embedding](https://arxiv.org/abs/2104.09864) Bảng giấy RoPE.
  Su 等人(2021)  RoPE 论文。

- [Press, Smith, Lewis (2021). Train Short, Test Long: Attention with Linear Biases Enables Input Length Extrapolation](https://arxiv.org/abs/2108.12409) ALiBi.
  Báo chí, Smith, Lewis...

- [Peng et al. (2023). YaRN: Efficient Context Window Extension of Large Language Models](https://arxiv.org/abs/2309.00071) hiện đại nhất RoPE quy mô.
  Peng 等人(2023)  最先进的 RoPE 缩放──

- [Chen et al. (2023). Extending Context Window of Large Language Models via Positional Interpolation](https://arxiv.org/abs/2306.15595) Llama 2 của Meta.
  Chen 等人(2023)  Meta của Llama 2 长上下文论文。

- [Ding et al. (2024). LongRoPE: Extending LLM Context Window Beyond 2 Million Tokens](https://arxiv.org/abs/2402.13753) phương pháp Microsoft được Phi-3-Long sử dụng.
  Ding 等人(2024)  Microsoft's method, được Phi-3-Long sử dụng。

- [HuggingFace Transformers — `modeling_rope_utils.py`](https://github.com/huggingface/transformers/blob/main/src/transformers/modeling_rope_utils.py) Thực hiện cấp sản xuất của mỗi chương trình quy mô RoPE.
  HuggingFace Transformers  所有 RoPE 缩放方案的生产级实现──
