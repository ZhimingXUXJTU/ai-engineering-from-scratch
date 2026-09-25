# Cơ chế chú ý  Sự đột phá  Cơ chế chú ý  Sự đột phá cốt lõi của Transformer

> Bộ giải mã ngừng nhìn vào một bản tóm tắt nén và bắt đầu nhìn vào toàn bộ nguồn.
> 解码器 không còn nhìn vào bản tóm tắt, bắt đầu nhìn vào toàn bộ nguồn.

> **【中文解读】**Hệ thống chú ý để mô hình quan tâm đến các phần liên quan của nhập.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 09 (Sequence-to-Sequence Models) | **前置知识:** Phase 5 · 09（序列到序列模型）
**Time:** ~45 minutes | **时间:** ~45 分钟

## Vấn đề  vấn đề giới thiệu

Bài học 09 kết thúc với một sự thất bại đo lường. Một bộ mã hóa-bẻ khóa GRU được đào tạo trên một nhiệm vụ sao chép đồ chơi đi từ độ chính xác 89% ở độ dài 5 đến gần như xác suất ở độ dài 80. Lý do là cấu trúc, không phải là lỗi đào tạo: mỗi bit thông tin mà bộ mã hóa thu thập phải phù hợp với một trạng thái ẩn kích thước cố định, và bộ mã hóa không bao giờ thấy bất cứ điều gì khác.

> Chương 09  Học kết thúc với một thất bại có thể đo lường. GRU mã hóa giải mã được đào tạo trong nhiệm vụ sao chép đồ chơi có độ dài 5 giờ 89%  tỉ lệ chính xác, gần như theo thời gian trong độ dài 80 giờ.

Bahdanau, Cho và Bengio đã công bố một sửa chữa ba dòng vào năm 2014. Thay vì chỉ cho máy giải mã trạng thái giải mã cuối cùng, hãy giữ cho từng máy giải mã trạng thái.`i`"Đây là thời điểm của chúng ta".

> Bahdanau、Cho 和 Bengio đã xuất bản một bản trong năm 2014: Không chỉ cho máy giải mã tình trạng máy giải mã cuối cùng, mà còn giữ lại tình trạng máy giải mã mỗi bước, tính toán tình trạng máy giải mã tăng thêm quyền trung bình, quyền trọng cho biết "Khóa máy bây giờ cần nhiều hơn xem vị trí máy giải mã .`i`"Điều này tăng quyền trung bình là trên xuống văn bản, nó thay đổi trong mỗi bước giải mã.

Đó là ý tưởng. Transformers mở rộng nó. Sự chú ý tự tính áp dụng nó cho một chuỗi đơn lẻ. Sự chú ý đa đầu chạy nó song song. Nhưng phiên bản 2014 đã phá vỡ nút thắt, và một khi bạn có nó, tâm điểm của các transformer là kỹ thuật, không phải khái niệm.

> Đó là toàn bộ ý tưởng. Transformer đã mở rộng nó. Phong tâm sẽ áp dụng nó cho một chuỗi đơn.

## Khái niệm cốt lõi

> **【中文解读】**Bài viết này giới thiệu các khái niệm và lý thuyết cốt lõi.

![Bahdanau attention: decoder queries all encoder states](../assets/attention.svg)

Ở mỗi bước giải mã `t`- Có thể là:

> Trong mỗi bước giải mã`t`- Có thể là:

1. Sử dụng trạng thái ẩn của máy giải mã trước đó `s_{t-1}`như một **query**- Tôi không biết.
2. Đánh giá nó so với mọi trạng thái ẩn của mã hóa`h_1, ..., h_T`Một scalar cho mỗi vị trí mã hóa.
3. Tối đa điểm để có được trọng lượng chú ý `α_{t,1}, ..., α_{t,T}`số đó là 1.
4. Vêctơ ngữ cảnh `c_t = Σ α_{t,i} * h_i`- Tỷ lệ trung bình trọng lượng của các trạng thái mã hóa.
5. Decoder lấy `c_t`cộng với token đầu ra trước, tạo ra token tiếp theo.
   1. 使用前一个解码器                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        `s_{t-1}`作为**查询（Query）**
   2. Để nó ẩn với mỗi bộ lập trình`h_1, ..., h_T`打分── mỗi bộ lập trình vị trí một tiêu chuẩn──
   3. Để phân số làm mềm tối đa  nhận được trọng lượng chú ý `α_{t,1}, ..., α_{t,T}`, tổng cộng là 1
   4. 上下文向量 `c_t = Σ α_{t,i} * h_i`❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖
   5. 解码器取 `c_t`Thêm vào một token đầu ra, tạo ra một token tiếp theo.

Đường trung bình trọng lượng là điểm. Khi máy giải mã cần dịch "Je" thành "I", nó cân nặng trạng thái mã hóa trên "Je" cao và các loại khác thấp. Khi nó cần "không", nó cân nặng "pas" cao.

> 加权平均是关键──当解码器需要将 "Je" 翻译为 "I" 时,它对 "Je" 上的编码器状态权重高,其他低──当需要"not" 时,它对 "pas" 权重高──上下文向量在每步重塑──

> **【拓展：大语言模型的工程实践】**Từ GPT đến ChatGPT, NLP đã trải qua sự chuyển đổi từ "mỗi nhiệm vụ đào tạo một mô hình" đến "một mô hình giải quyết tất cả các nhiệm vụ". Trong công trình thực tế, việc triển khai LLM cần phải xem xét các vấn đề như: giới hạn token, trì hoãn, chi phí, kiểm tra an toàn, và các vấn đề khác.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) là cấu trúc phổ biến nhất trong ứng dụng AI của doanh nghiệp hiện tại: sẽ truy vấn người dùng trước tiên truy vấn các đoạn tài liệu liên quan, tiếp tục truy vấn kết quả như trên dưới đây cho LLM 生成答案──

> **【拓展：NLP 的多语言挑战】**Trên toàn cầu có hơn 7000 ngôn ngữ, nhưng nghiên cứu về NLP tập trung chủ yếu vào tiếng Anh và một số ít ngôn ngữ.

## hình dạng (làm gì cắn mọi người) 形状

Đây là nơi mọi sự thực hiện sự chú ý đều sai lần đầu tiên.

> Đó là nơi mà mọi người tập trung vào việc thực hiện lần đầu tiên.

| Thing / 对象 | Shape / 形状 | Notes / 说明 |
|-------|-------|-------|
| Encoder hidden states `H` / 编码器隐藏状态 `H` | `(T_enc, d_h)` | If BiLSTM, `d_h = 2 * d_hidden` / 如果是 BiLSTM，`d_h = 2 * d_hidden` |
| Decoder hidden state `s_{t-1}` / 解码器隐藏状态 | `(d_s,)` | One vector / 一个向量 |
| Attention score `e_{t,i}` / 注意力分数 | scalar / 标量 | One per encoder position / 每个编码器位置一个 |
| Attention weight `α_{t,i}` / 注意力权重 | scalar / 标量 | After softmax over all `i` / 对所有 `i` 做 softmax 后 |
| Context vector `c_t` / 上下文向量 | `(d_h,)` | Same shape as an encoder state / 与编码器状态相同形状 |

**Bahdanau (additive) score.** `e_{t,i} = v_α^T * tanh(W_a * s_{t-1} + U_a * h_i)`- Tôi không biết.

> **Bahdanau（加性）分数。** `e_{t,i} = v_α^T * tanh(W_a * s_{t-1} + U_a * h_i)`

- `s_{t-1}`có hình dạng`(d_s,)`- `h_i`có hình dạng`(d_h,)`- Tôi không biết.
- `W_a`có hình dạng`(d_attn, d_s)`- `U_a`có hình dạng`(d_attn, d_h)`- Tôi không biết.
- Số lượng của chúng bên trong tanh có hình dạng`(d_attn,)`- Tôi không biết.
- `v_α`có hình dạng`(d_attn,)`. sản phẩm bên trong với `v_α`- Nó sụp đổ thành một con đường.**This is what `v_α` does.**Nó không phải là phép thuật, mà là sự chiếu biến một vector ánh sáng ánh sáng thành một điểm số scalar.
  - `s_{t-1}`hình dạng`(d_s,)`- Tôi không biết.`h_i`hình dạng`(d_h,)`
  - `W_a`hình dạng`(d_attn, d_s)``U_a`hình dạng`(d_attn, d_h)`
  - tanh 内部的和形状为 `(d_attn,)`
  - `v_α`hình dạng`(d_attn,)`❖ với `v_α`n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n n**这就是 `v_α` 的作用。**Nó không phải là phép thuật. Nó là một sự chiếu của trọng lượng chiều kích và khối lượng để mô tả số lượng.

**Luong (multiplicative) score.**Ba biến thể:

> **Luong（乘性）分数。**3 biến thể:

- `dot``e_{t,i} = s_t^T * h_i`- Cần`d_s == d_h`- Cấm nếu mã hóa của bạn là hai chiều.
  `dot`- Có thể là:`e_{t,i} = s_t^T * h_i`❖ yêu cầu`d_s == d_h`硬约束 Nếu bộ lập trình là hai chiều thì nhảy qua
- `general``e_{t,i} = s_t^T * W * h_i`với `W`hình dạng`(d_s, d_h)`- Giảm giới hạn độ mờ bằng nhau.
  `general`- Có thể là:`e_{t,i} = s_t^T * W * h_i`- Tôi không biết.`W`hình dạng`(d_s, d_h)`❖ Di chuyển等维约束──
- `concat`: chủ yếu là hình thức Bahdanau. hiếm khi được sử dụng vì hai hình thức đầu tiên rẻ hơn.
  `concat`Bản chất là Bahdanau 形式──由于前两种更便宜,很少使用──

**One Bahdanau / Luong gotcha worth naming.**Bahdanau sử dụng `s_{t-1}`(các trạng thái decoder * trước khi * tạo ra từ hiện tại). Luong sử dụng `s_t`(the state *after*). khi trộn chúng lại tạo ra gradient sai lầm rất khó để gỡ lỗi. chọn một giấy và bám vào quy tắc của nó.

> **一个值得注意的 Bahdanau / Luong 陷阱。**Bahdanau 使用 `s_{t-1}`(生成当前词*之前*的解码器状态) ――Long 使用 `s_t`(** sau* của trạng thái) ――混 chúng sẽ tạo ra rất khó để điều chỉnh các tỉ lệ sai lầm nhỏ gọn―― chọn một bài luận并坚持约定――

## Hãy xây dựng nó.

> **【中文解读】**本节通过代码实现核心算法从零――这种" từ đầu"的方式能帮助理解框架背后的原理,遇到问题时不会被黑盒困住――
```figure
attention-heatmap
```

## Hãy xây dựng nó

### Bước 1: sự chú ý phụ gia (Bahdanau)

```python
import numpy as np


def additive_attention(decoder_state, encoder_states, W_a, U_a, v_a):
    projected_dec = W_a @ decoder_state
    projected_enc = encoder_states @ U_a.T
    combined = np.tanh(projected_enc + projected_dec)
    scores = combined @ v_a
    weights = softmax(scores)
    context = weights @ encoder_states
    return context, weights


def softmax(x):
    x = x - np.max(x)
    e = np.exp(x)
    return e / e.sum()
```

Hãy kiểm tra hình dạng của bạn với bảng trên. `encoder_states`có hình dạng`(T_enc, d_h)`- `projected_enc`có hình dạng`(T_enc, d_attn)`- `projected_dec`có hình dạng`(d_attn,)`và phát sóng. `combined`có hình dạng`(T_enc, d_attn)`- `scores`có hình dạng`(T_enc,)`- `weights`có hình dạng`(T_enc,)`- `context`có hình dạng`(d_h,)`- Đưa đi.

> Để kiểm tra hình dạng của bạn trên đây.`encoder_states`hình dạng`(T_enc, d_h)``projected_enc`hình dạng`(T_enc, d_attn)``projected_dec`hình dạng`(d_attn,)`Và phát sóng.`combined`hình dạng`(T_enc, d_attn)``scores`hình dạng`(T_enc,)``weights`hình dạng`(T_enc,)``context`hình dạng`(d_h,)` đã quyết định rồi.

### Bước 2: Luong dot và chung

```python
def dot_attention(decoder_state, encoder_states):
    scores = encoder_states @ decoder_state
    weights = softmax(scores)
    return weights @ encoder_states, weights


def general_attention(decoder_state, encoder_states, W):
    projected = W.T @ decoder_state
    scores = encoder_states @ projected
    weights = softmax(scores)
    return weights @ encoder_states, weights
```

3 dòng mỗi, đó là lý do tại sao tờ giấy của Luong xuất hiện, chính xác như hầu hết các nhiệm vụ, ít mã hơn nhiều.

> Mỗi bộ. Đó là ý nghĩa của bài luận Luong.

### Bước 3: ví dụ số được làm việc

Với ba trạng thái mã hóa (khoảng "cat", "sat", "mat") và trạng thái mã hóa phù hợp nhất với thứ nhất, sự phân phối sự chú ý tập trung vào vị trí 0. Nếu trạng thái mã hóa thay đổi để phù hợp với thứ cuối cùng, sự chú ý chuyển sang vị trí 2.

> 给定三个编码器状态 ((大致是"cat"、"sat"、"mat") và một với thứ nhất nhất phù hợp với thứ nhất giải mã器状态, tập trung sự chú ý phân bố ở vị trí 0。 Nếu giải mã器 trạng thái di chuyển đến với cuối cùng phù hợp, sự chú ý di chuyển đến vị trí 2。

```python
H = np.array([
    [1.0, 0.0, 0.2],
    [0.5, 0.5, 0.1],
    [0.1, 0.9, 0.3],
])

s_close_to_cat = np.array([0.9, 0.1, 0.2])
ctx, w = dot_attention(s_close_to_cat, H)
print("weights:", w.round(3))
```

```
weights: [0.464 0.305 0.231]
```

Lần đầu tiên thắng. sau đó di chuyển trạng thái decoder gần hơn đến trạng thái encoder thứ ba và xem trọng lượng chuyển đổi. Đó là nó.

> Đầu tiên, hãy chuyển trạng thái của máy tính giải mã sang trạng thái của máy tính lập trình thứ ba, để quan sát quyền lực thay đổi.

### Bước 4: tại sao đây là cây cầu dẫn đến các bộ biến đổi

Dịch ngôn ngữ trên thành Q/K/V:

> 将上面的语言翻译为:

- **Query**= trạng thái decoder `s_{t-1}`
  **查询（Query）**= 解码器 trạng thái `s_{t-1}`
- **Key**= các trạng thái mã hóa (tại điểm gì chúng ta đánh giá)
  **键（Key）**= 编码器 trạng thái(我们用来打分的对象)
- **Value**= các trạng thái mã hóa (tổng số và trọng lượng)
  **值（Value）**= 编码器 trạng thái(我们用来加权和的对象)

Trong sự chú ý cổ điển, chìa khóa và giá trị là cùng một thứ. Sự chú ý tự phân biệt chúng: bạn có thể truy vấn một chuỗi chống lại chính nó, với các dự đoán học được khác nhau cho K và V. Sự chú ý đa đầu chạy nó song song với các dự đoán học được khác nhau. Các bộ biến chuyển xếp chồng toàn bộ giai đoạn nhiều lần và thả RNN.

> Trong chú ý cổ điển, trọng điểm và giá trị là cùng một thứ. Chú ý sẽ phân chia chúng: bạn có thể sử dụng các chuỗi học khác nhau để tìm kiếm một dự án như K và V.

Các toán học giống nhau, hình dạng giống nhau, sự nhảy vọt giáo dục từ sự chú ý Bahdanau đến sự chú ý sản phẩm điểm quy mô chủ yếu là ghi chú.

> Hình dạng của nó giống nhau. Từ Bahdanau chú ý đến tập trung điểm tập trung chú ý, nhảy học chủ yếu là biểu tượng.

> **【中文解读】**Bài này sẽ trình bày cách sử dụng một khung đã phát triển như PyTorch, HuggingFace, và các khác.

> **【拓展：Prompt Engineering 与 LLM 应用】**Kỹ thuật nhanh chóng đã trở thành kỹ năng cốt lõi của các kỹ sư NLP. Từ Zero-shot đến Few-shot, từ Chain-of-Thought đến ReAct, các chiến lược khác nhau áp dụng cho các tình huống khác nhau. Trong các dự án thực tế, thiết kế của System提示(System Prompt) ảnh hưởng trực tiếp đến sự ổn định và chất lượng sản xuất của ứng dụng LLM.

## Hãy sử dụng nó để thực hiện

PyTorch và TensorFlow sẽ đưa sự chú ý trực tiếp.

> PyTorch và TensorFlow  trực tiếp cung cấp sự chú ý.

```python
import torch
import torch.nn as nn

mha = nn.MultiheadAttention(embed_dim=128, num_heads=8, batch_first=True)
query = torch.randn(2, 5, 128)
key = torch.randn(2, 10, 128)
value = torch.randn(2, 10, 128)

output, weights = mha(query, key, value)
print(output.shape, weights.shape)
```

```
torch.Size([2, 5, 128]) torch.Size([2, 5, 10]
```

Đó là một lớp chú ý biến đổi. Nhóm truy vấn 5 vị trí, khóa/định giá 10 vị trí, mỗi vị trí có 128 chiều, 8 đầu.`output`là các truy vấn mới tăng cường ngữ cảnh. `weights`là các 5x10 trục trọng mà bạn có thể hình dung.

> Đây là một biến thể chú ý cấp độ. Tìm kiếm 5 vị trí, khóa/đánh giá 10 vị trí, mỗi 128 维,8 头.`output`Là một câu hỏi mới trên.`weights`Đó là 5x10 của một đối số, bạn có thể nhìn thấy.

### Khi sự chú ý cổ điển vẫn quan trọng

- Lập trình đơn, đơn lớp, dựa trên RNN làm cho mọi khái niệm trở nên rõ ràng.
  Giáo dục: Một đầu, một tầng, dựa trên phiên bản RNN để mọi khái niệm được nhìn thấy.
- Các nhiệm vụ theo trình trên thiết bị khi các bộ biến không phù hợp.
  Transformer 放不下设备端序列任务。
- Bất kỳ bài báo nào từ năm 2014 đến 2017 bạn sẽ đọc sai nó mà không biết sự kiện của Bahdanau.
  Bất kỳ bài luận nào trong năm 2014-2017 không hiểu về Bahdanau
- Phân tích sắp xếp tinh tế trong MT. Năng lượng chú ý thô là một công cụ giải thích ngay cả trên các mô hình biến thể, và đọc chúng đòi hỏi phải biết chúng là gì.
  机器翻译中的细粒度对齐分析──原始注意力权重甚至在变压器模型上也是可解释性工具,阅读它们需要知道它们是什么──

### Cái bẫy chú ý trọng lượng như giải thích

Các trọng lượng chú ý trông có thể diễn giải được. Chúng là trọng lượng tổng hợp với một người qua các vị trí; bạn có thể vẽ chúng; cao có nghĩa là "để nhìn vào điều này".

> chú ý trọng lực nhìn có thể giải thích. Chúng là trọng lực của 1 và 1 trong các vị trí khác nhau; bạn có thể vẽ chúng; cao có nghĩa là " nhìn vào nó" (see this).

Chúng không thể diễn giải được như chúng trông thấy. Jain và Wallace (2019) cho thấy rằng phân phối sự chú ý có thể được thay đổi và thay thế bằng các thay thế tùy ý mà không thay đổi dự đoán mô hình cho một số nhiệm vụ.

> Chúng không giống như trông có thể giải thích. Jane và Wallace (2019) cho thấy rằng phân bố tập trung có thể được thay thế và thay thế cho bất kỳ thay thế nào, không thay đổi mô hình dự đoán của một số nhiệm vụ.

> **【中文解读】**Phần này tập trung vào cách phân phối mô hình như một sản phẩm có thể sử dụng.

## Chuyển nó đi.

Cứ như `outputs/prompt-attention-shapes.md`- Có thể là:

> 保存为 `outputs/prompt-attention-shapes.md`- Có thể là:

```markdown
---
name: attention-shapes
description: Debug shape bugs in attention implementations.
phase: 5
lesson: 10
---

Given a broken attention implementation, you identify the shape mismatch. Output:

1. Which matrix has the wrong shape. Name the tensor.
2. What its shape should be, derived from (d_s, d_h, d_attn, T_enc, T_dec, batch_size).
3. One-line fix. Transpose, reshape, or project.
4. A test to catch regressions. Typically: assert `output.shape == (batch, T_dec, d_h)` and `weights.shape == (batch, T_dec, T_enc)` and `weights.sum(dim=-1) close to 1`.

Refuse to recommend fixes that silently broadcast. Broadcast-hiding bugs surface later as silent accuracy degradation, the worst kind of attention bug.

For Bahdanau confusion, insist the decoder input is `s_{t-1}` (pre-step state). For Luong, `s_t` (post-step state). For dot-product, flag dimension mismatch between query and key as the most common first-time error.
```

> **【中文解读】**练题按照 Easy/Medium/Hard 三个难度递进;;建议至少完成 级别的题目, 级别适合深入研究或面试准备;;

## Tập luyện bài tập

1. **Easy.**Thực hiện`softmax`che giấu để mã hóa mã thông báo trong mã hóa nhận được trọng lượng chú ý bằng không.
   **简单。**实现 `softmax`掩码, để tập trung vào các mã hóa để làm cho các mã hóa được tải lên.
2. **Medium.**Thêm nhiều đầu chú ý đến Luong `general`hình dạng. chia.`d_h`vào`n_heads`nhóm, chạy sự chú ý mỗi đầu, kết nối.
   **中等。**Vì Luong `general`hình thức thêm nhiều chú ý.`d_h`chia chia cho`n_heads`组, mỗi đầu运行注意力,拼接,拼接, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验证, 验
3. **Hard.**Trén một bộ mã hóa-chế lập GRU với sự chú ý Bahdanau vào nhiệm vụ sao chép đồ chơi từ bài học 09. Độ chính xác của bản vẽ so với chiều dài chuỗi. So sánh với đường cơ sở không chú ý. Bạn nên thấy khoảng cách mở rộng khi chiều dài tăng lên, xác nhận sự chú ý nâng nút thắt.
   **困难。**Trong bài tập thứ 9  tập luyện nhiệm vụ sao chép đồ chơi với Bahdanau chú ý GRU 编码器- giải mã器。 vẽ tỉ lệ chính xác so với độ dài chuỗi。 so sánh với không chú ý cơ sở线。 bạn nên thấy khoảng cách tăng và mở rộng theo chiều dài, xác nhận chú ý đã giải phóng chai。

> **【中文解读】**Trong 术语表中的"Những gì mọi người nói" vs "Những gì nó thực sự có nghĩa" 区分日常口语和精确技术含义── 在团队协作中,统一术语定义可以避免大量沟通误解──

## Từ khóa  Từ khóa nhanh chóng

| Term / 术语 | What people say / 人们常说的 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| Attention（注意力） | Looking at things / 看东西 | Weighted average of a value sequence, weights computed from a query-key similarity. / 值序列的加权平均，权重从查询-键相似度计算。 |
| Query, Key, Value（查询、键、值） | QKV | Three projections: Q asks, K is what to match, V is what to return. / 三个投影：Q 询问，K 是要匹配的，V 是要返回的。 |
| Additive attention（加性注意力） | Bahdanau | Feed-forward score: `v^T tanh(W q + U k)`. / 前馈分数：`v^T tanh(W q + U k)`。 |
| Multiplicative attention（乘性注意力） | Luong dot / general | Score is `q^T k` or `q^T W k`. Cheaper, same accuracy on most tasks. / 分数是 `q^T k` 或 `q^T W k`。更便宜，大多数任务上相同准确率。 |
| Alignment matrix（对齐矩阵） | The pretty picture / 那张漂亮的图 | Attention weights as a `(T_dec, T_enc)` grid. Read it to see what the model attended to. / 注意力权重作为 `(T_dec, T_enc)` 网格。阅读它看模型关注了什么。 |

> **【中文解读】**延伸阅读 cung cấp các nguồn chất lượng cao cho việc học sâu. Những bài báo và giảng dạy này là tài liệu tham khảo cổ điển trong lĩnh vực này, phù hợp với những người đọc cần hiểu sâu hơn.

## Xem thêm 延伸阅读

- [Bahdanau, Cho, Bengio (2014). Neural Machine Translation by Jointly Learning to Align and Translate](https://arxiv.org/abs/1409.0473)- Thư báo.
- [Luong, Pham, Manning (2015). Effective Approaches to Attention-based Neural Machine Translation](https://arxiv.org/abs/1508.04025) ba biến thể điểm số và so sánh của chúng. / 三种分数变体及其比较──
- [Jain and Wallace (2019). Attention is not Explanation](https://arxiv.org/abs/1902.10186) cảnh báo về khả năng giải thích. / 可解释性警示──
- [Dive into Deep Learning — Bahdanau Attention](https://d2l.ai/chapter_attention-mechanisms-and-transformers/bahdanau-attention.html) chạy qua với PyTorch. / 带 PyTorch 的可运行演练──
