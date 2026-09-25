# GPT  Mô hình hóa ngôn ngữ nguyên nhân  GPT  因果语言模型

> BERT nhìn cả hai bên. GPT chỉ nhìn thấy quá khứ. Mặt nạ tam giác là dòng mã đơn nhất trong AI hiện đại.

> **【中文解读】**GPT là một bộ chuyển đổi chỉ có Decoder, sử dụng ιν果掩码 () để ngăn chặn nhìn thấy các biểu tượng tương lai.

**Type:** Hands-on | **类型:** 动手
**Language:**Python**语言:**Python
**Prerequisites:** Phase 7 · 02 (Self-Attention), Phase 7 · 05 (Full Transformer), Phase 7 · 06 (BERT) | **前置知识:** Phase 7 · 02 (Self-Attention), Phase 7 · 05 (Full Transformer), Phase 7 · 06 (BERT)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Vấn đề  vấn đề giới thiệu

Một mô hình ngôn ngữ trả lời một câu hỏi: cho phép đầu tiên `t-1`token, phân phối xác suất trên token là gì `t`Đào tạo vào tín hiệu đó  dự đoán mã thông báo tiếp theo  và bạn có được một mô hình có thể tạo ra văn bản tùy ý một mã thông báo một lần.

> 语言模型回答一个问题:给定前 `t-1`个 token, thứ nhất`t`Trong tín hiệu này 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预

Để đào tạo nó từ đầu đến cuối trên một chuỗi toàn bộ song song, bạn cần dự đoán của mỗi vị trí chỉ phụ thuộc vào vị trí trước đó. Nếu không mô hình lừa dối tầm thường bằng cách nhìn vào câu trả lời.

> Để thực hiện các bài tập trên cùng một chuỗi, bạn cần dự đoán từng vị trí chỉ phụ thuộc vào vị trí trước đó. Nếu không, mô hình sẽ nhìn thấy câu trả lời trực tiếp, "bảo quy" để hoàn thành nhiệm vụ.

Mặt nạ nguyên nhân làm điều này. Đó là một matrix ba giác trên đơn`-inf`các giá trị được thêm vào điểm chú ý trước softmax. Sau softmax, các vị trí đó trở thành 0. Mỗi vị trí chỉ có thể tham gia vào chính nó và các vị trí trước đó. Và bởi vì bạn áp dụng nó một lần cho toàn bộ chuỗi, bạn nhận được N tương đồng dự đoán token tiếp theo trong một chuyển tiếp về phía trước.

> Vì vậy, nó là một hình ảnh của một góc trên.`-inf`值), tăng lên softmax  trước khi chú ý phần tử trên. softmax 后, những vị trí này thay đổi thành 0. Mỗi vị trí chỉ có thể chú ý đến chính nó và vị trí trước đó.

GPT-1 (2018), GPT-2 (2019), GPT-3 (2020), GPT-4 (2023), GPT-5 (2024), Claude, Llama, Qwen, Mistral, DeepSeek, Kimi  tất cả chúng đều là các bộ chuyển đổi nguyên nhân chỉ có mã hóa với cùng một vòng lặp cốt lõi. Chỉ lớn hơn, dữ liệu tốt hơn và RLHF tốt hơn.
GPT-1 (2018), GPT-2 (2019), GPT-3 (2020), GPT-4 (2023), GPT-5 (2025), Claude, Llama, Qwen, Mistral, DeepSeek, Kimi  tất cả đều là các bộ chuyển đổi nguyên nhân chỉ có mã hóa với cùng một vòng lặp cốt lõi. Điều phân biệt chúng là chất lượng dữ liệu, quy mô và tinh tế kiến trúc, và sau đào tạo (SFT, RLHF, DPO và những người kế nhiệm của chúng).

> GPT-1(2018)、GPT-2(2019)、GPT-3(2020)、GPT-4(2023)、GPT-5(2024)、Claude、Llama、Qwen、Mistral、DeepSeek、Kimi它们都是解码器专用因果变压器,核心循环相同──只是更大、数据更好、RLHF 更好──

> **【中文解读】**因果掩码 là một dòng mã quan trọng nhất trong AI hiện đại. Một trên三角矩阵 (n-inf 值), tăng lên số lượng chú ý, thông qua softmax 后 được ẩn định vị trí biến thành 0. Mỗi vị trí chỉ có thể tập trung vào bản thân và các token trước đó.

## Khái niệm cốt lõi

![Causal mask creates a triangular attention matrix](../assets/causal-attention.svg)

### Mặt nạ

Với một chuỗi dài `N`, xây dựng một `N × N`Matrix:

> 给定长度为 `N`      `N × N`矩阵:

```
M[i, j] = 0       if j <= i
M[i, j] = -inf    if j > i
```

Thêm `M`cho điểm chú ý nguyên chất trước softmax. `exp(-inf) = 0`, vì vậy các vị trí che giấu đóng góp trọng lượng không. mỗi hàng của ma trận chú ý là phân phối xác suất trên các vị trí trước đó chỉ.

> sẽ`M`Tăng lên điểm tập trung đầu tiên trước đó.`exp(-inf) = 0`, vì vậy trọng lượng của vị trí được che giấu là 0, mỗi dòng của tập hợp chú ý chỉ là phân bố xác suất ở vị trí trước.

Chi phí thực hiện: 1 `torch.tril()`Tiếng gọi, thời gian tính toán: nanoseconds, tác động trên trường: mọi thứ.

> 实现成本: 一行 `torch.tril()`调用――计算时间:纳秒级―― ảnh hưởng đến toàn bộ lĩnh vực:改变了一切――
### Từ đâu được hình tam giác

Mặt nạ thường được trình bày như một vá được gắn vào sự chú ý. Tiến dẫn theo hướng khác và nó không còn bí ẩn: sự chú ý là sự tinh tế thứ ba của một trung bình tiền tố, và tam giác là ranh giới vòng lặp của trung bình đó, được viết như một matrix.

**Stage 1 — prefix average.**Kết luận nguyên nhân ngu ngốc nhất của một chuỗi: vị trí`i`trở thành trung bình của các vị trí `0…i`Như một vòng lặp, đó là`out[i] = X[:i+1].mean(0)`- cùng một tính toán là một số tử liệu nhân. lấy một số tử liệu ba góc dưới của một, chia mỗi hàng bằng số lượng của nó, nhân:

```python
import numpy as np

A = np.tril(np.ones((n, n)))
A = A / A.sum(axis=1, keepdims=True)
out = A @ X
```

Đường `i`của `A`là `[1/(i+1), …, 1/(i+1), 0, …, 0]`Những con số 0 trên đường viền là nguyên nhân. Không có gì về tương lai được che giấu; tương lai không bao giờ là tổng.

**Stage 2 — learned weights.**Một trung bình đồng nhất xử lý mọi token trước đây như là tương đương. Thay thế những người với một số điểm học được .`S`. Bây giờ các hàng không còn cộng với một bằng cách xây dựng, vì vậy bình thường hóa mỗi hàng bằng Softmax thay vì chia bằng số. Softmax không bao giờ đưa ra một số không chính xác, điều này phá vỡ tính nhân quả  trừ khi điểm số trong tương lai đi vào như `-inf`, bởi vì`exp(-inf) = 0`- Có thể là:

```python
def softmax(x, axis):
    e = np.exp(x - np.max(x, axis=axis, keepdims=True))
    return e / e.sum(axis=axis, keepdims=True)

S = S + np.triu(np.full((n, n), -np.inf), k=1)
A = softmax(S, axis=1)
out = A @ X
```

cùng một tam giác, cùng một matrix hàng-stochastic, cùng một matmul.`-inf`mask không phải là một máy móc mới. Nó là các mục 0 giai đoạn 1, được dịch thành lĩnh vực đầu vào của softmax.

**Stage 3 — content-dependent weights.**Trong giai đoạn 2, `S`được cố định sau khi tập luyện: vị trí 7 luôn cân nặng vị trí 3 giống nhau, bất kể các token nói. Hãy để điểm số phụ thuộc vào các token chính: `S = Q @ K.T / sqrt(d_k)`Không có gì khác thay đổi.

Ba giai đoạn, một không biến đổi: một chuỗi hàng-stochastic ba góc thấp gấp đôi chuỗi. trung bình thống nhất, học được trọng lượng tĩnh, trọng lượng phụ thuộc vào nội dung.

```figure
mask-derivation
```

### Việc đào tạo song song, suy luận hàng loạt

Việc đào tạo: chuyển tiếp toàn bộ`(N, d_model)`Dòng một lần, tính toán N mất tích entropy chéo (một trong mỗi vị trí), tổng, backprop. song song dọc theo chuỗi. Đây là lý do tại sao các quy mô đào tạo GPT  bạn xử lý 1M token trong một lô trong một GPU vượt qua.

> 训练: đối với toàn bộ `(N, d_model)`序列 làm một lần trước và tiếp tục, tính toán N 个交叉损失( mỗi vị trí một), tìm kiếm和,反向传播──沿序列并行──这就是GPT 训练可扩展的原因一次GPU 通行就能处理批量中的 1M 个代币──

Thuyết định: bạn tạo ra token theo token.`[t1, t2, t3]`, đi`t4`- Thức ăn`[t1, t2, t3, t4]`, đi`t5`- Thức ăn`[t1, t2, t3, t4, t5]`, đi`t6`KV cache (Dạy 12) lưu các trạng thái ẩn của `t1…tn`Vì vậy bạn không tính lại chúng mỗi bước. nhưng độ sâu hàng loạt tại suy luận = bước đầu ra. Đó là thuế tự rút và tại sao việc giải mã là nút nút kẹt độ của mỗi LLM.

> 推理: từng token 生成──输入 `[t1, t2, t3]`, nhận được`t4`❖ nhập khẩu`[t1, t2, t3, t4]`, nhận được`t5`❖ nhập khẩu`[t1, t2, t3, t4, t5]`, nhận được`t6`;;KV 缓存;;第 12 课) lưu giữ `t1…tn`Trong tình trạng ẩn, tránh mỗi bước lặp lại tính toán. Nhưng khi đưa ra ý kiến, chiều sâu của chuỗi = 输出长度.

### Lối mất  chuyển đổi từng người

Đồ tín hiệu được đưa ra `[t1, t2, t3, t4]`- Có thể là:

> 给定 token `[t1, t2, t3, t4]`- Có thể là:

- Nhập: `[t1, t2, t3]`
  Trung ngữ翻译:输入:`[t1, t2, t3]`
- Mục tiêu: `[t2, t3, t4]`
  Trung ngữ翻译:目标:`[t2, t3, t4]`

Đối với mọi vị trí `i`, tính toán`-log P(target_i | inputs[:i+1])`Đây là sự chuyển động của toàn bộ chuỗi.

> Đối với mỗi vị trí`i`,计算 `-log P(target_i | inputs[:i+1])`求和── đây là đường giao của toàn bộ chuỗi──

Mỗi bộ biến đổi LM mà bạn đã nghe nói về tàu trên mất mát này.

> Bạn đã nghe nói mỗi mô hình ngôn ngữ biến đổi đều có trong sự mất mát này.

> **【拓展：Teacher Forcing 与暴露偏差】**GPT trenage sử dụng giáo viên buộc mỗi bước输入真实前一个代币而非模型自己的预测──这导致"暴露偏差"(曝光偏差): training时模型从未见过自己的错输出,推理时却必须从自己的输出继续产生──Tổ hoạch lấy mẫu 和 RLHF là hai phương pháp giải quyết vấn đề này──

### Chiến lược giải mã

Sau khi đào tạo, lựa chọn lấy mẫu quan trọng hơn mọi người nghĩ.

> Sau khi hoàn thành bài tập, việc lựa chọn các chiến lược mẫu quan trọng hơn những gì người ta tưởng tượng.

| Method | What it does | When to use |
|--------|--------------|-------------|
| 方法 | 功能 | 适用场景 |
| Greedy | Argmax every step | Deterministic tasks, code completion |
| 贪心 | 每步取最大值 | 确定性任务、代码补全 |
| Temperature | Divide logits by T, sample | Creative tasks, higher T = more diversity |
| 温度 | 将 logits 除以 T 后采样 | 创意任务，T 越高多样性越大 |
| Top-k | Sample from top-k tokens only | Kills low-probability tails |
| Top-k | 只从概率最高的 k 个 token 采样 | 消除低概率尾部 |
| Top-p (nucleus) | Sample from smallest set with cumulative prob ≥ p | 2020+ default; adapts to distribution shape |
| Top-p（核采样） | 从累积概率 ≥ p 的最小集合中采样 | 2020+ 默认策略；自适应分布形状 |
| Min-p | Keep tokens with `p > min_p * max_p` | 2024+; better at rejecting long tails than top-p |
| Min-p | 保留 `p > min_p * max_p` 的 token | 2024+；比 top-p 更好地拒绝长尾 |
| Speculative decoding | Draft model proposes N tokens, big model verifies | 2–3× latency reduction at same quality |
| 推测解码 | 草案模型提出 N 个 token，大模型验证 | 相同质量下延迟降低 2-3 倍 |

Năm 2026, nhiệt độ min-p + 0,7 là một mặc định hợp lý cho các mô hình trọng lượng mở.

> Năm 2026, nhiệt độ min-p + 0,7 là một định dạng hợp lý của mô hình nguồn mở.

> **【中文解读】**解码策略的选择直接影响生成质量──贪心搜索(argmax) phù hợp với nhiệm vụ xác định, nhiệt độ theo kiểu tăng đa dạng,top-p/min-p 截断低概率尾部──2026 年的推默认:min-p + nhiệt độ 0.7,比传统的top-p 能更好地处理分布的度变化──

> **【拓展：从 GPT-2 到 GPT-4 的规模跳跃】**GPT-2(1.5B 参数)→ GPT-3(175B)→ GPT-4( ước tính 1.8T MoE) trong bước nhảy vọt quy mô, thay đổi cấu trúc rất nhỏ, nhưng cải tiến dữ liệu và phương pháp đào tạo rất lớn.

### Điều gì khiến "giết chế GPT" hoạt động

1. **Decoder-only.**Không có bộ mã hóa trên đầu. Một lần lưu ý + FFN cho mỗi lớp.
   Trung ngữ翻译:**解码器专用。**Không có máy lập trình nào. Mỗi tầng một lần tập trung.
2. **Scaling.**124M → 1.5B → 175B → nghìn tỷ. Luật quy mô Chinchilla (Dạy học 13) cho bạn biết cách chi tiêu tính toán.
   Trung ngữ翻译:**规模扩展。**Từ 124M đến 1.5B đến 175B trở lại thành hàng triệu số.
3. **In-context learning.**Tạo ra khoảng 6B13B. Mô hình có thể theo dõi một vài ví dụ chụp mà không cần điều chỉnh tinh tế.
   Trung ngữ翻译:**上下文学习。**约在 6B-13B 参数时涌现――模型无需微调就能遵循少样本示例――
4. **RLHF.**Sau khi đào tạo về sở thích của con người chuyển đổi văn bản nguyên liệu được đào tạo trước thành trợ lý trò chuyện.
   Trung ngữ翻译:**RLHF。**Trong khi được thực hiện theo sở thích của con người, văn bản dự kiến đầu tiên sẽ được chuyển thành trợ lý đối thoại.
5. **Pre-norm + RoPE + SwiGLU.**Đào tạo ổn định ở quy mô.
   Trung ngữ翻译:**Pre-norm + RoPE + SwiGLU。**Tập luyện ổn định quy mô lớn.

Kiến trúc cốt lõi không thay đổi nhiều kể từ GPT-2. Mọi thứ thú vị đã xảy ra trong dữ liệu, quy mô và sau đào tạo.

> Kể từ GPT-2, cấu trúc cốt lõi không thay đổi lớn. Tất cả những điều thú vị đều xảy ra trong dữ liệu, quy mô và các phương pháp đào tạo sau đó.

> **【中文解读】**Các yếu tố thành công của GPT:Décoder-only 架构的简洁性,规模扩展 (đơn 124M đến hàng triệu参数) 上下文学习能力 (khoảng 6B参数 bắt đầu nổi lên) RLHF 后训练 (将预训文文转化为对话助手) 及现代块设计 (Pre-norm + RoPE + SwiGLU) 核心架构自 GPT-2以来不变大,创新主要在数据,规模和后训练中.

> **【拓展：自回归生成的推理瓶颈】**Sự nghịch lý cốt lõi của GPT: đào tạo khi và đi tính toán toàn bộ chuỗi (高效), việc đưa ra ra ra ra ra ra ra phải từng mã số 生成 (串行) ・KV 缓存 (缓存) (Lớp 12) và việc đưa ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra ra

## Hãy xây dựng nó.
```figure
causal-mask
```

## Hãy xây dựng nó

### Bước 1: mặt nạ nguyên nhân

Nhìn xem`code/main.py`Một dòng:

> 参见 `code/main.py`一行代码:

```python
def causal_mask(n):
    return [[0.0 if j <= i else float("-inf") for j in range(n)] for i in range(n)]
```

Thêm vào điểm chú ý trước khi Softmax.

> Để tăng nó lên điểm tập trung trước đó của Softmax. Đó là toàn bộ cơ chế.

### Bước 2: mô hình GPT 2 lớp

Lắp lên hai khối decoder (đánh giá tự chú ý + FFN, không có sự chú ý chéo). Thêm một mã hóa token, mã hóa vị trí và unembedding (được gắn với mã hóa token  một thủ thuật tiêu chuẩn kể từ GPT-2).

> 堆叠两个解码器块(掩码自注意力 + FFN,无交叉注意力) ・・・添加代币 嵌入、位置编码和反嵌入(与代币 嵌入矩阵绑定GPT-2 以来的标准技巧) ・・・

### Bước 3: dự đoán mã thông báo tiếp theo, kết thúc đến kết thúc

Trên một từ ngữ đồ chơi 20 token, tạo logits ở mọi vị trí. tính toán mất tích entropy chéo so với mục tiêu chuyển đổi theo một. Không gradient  đây là kiểm tra trí tuệ vượt qua về phía trước.

> Trong 20 biểu tượng của biểu tượng, trên mỗi vị trí tạo ra logits.

### Bước 4: lấy mẫu

Thực hiện tham lam, nhiệt độ, top-k, top-p, min-p. chạy mỗi trên một prompt cố định và so sánh đầu ra.

> 实现贪心、温度、top-k、top-p、min-p 采样──在固定提示上分别运行并比较输出──一个采样函数只需要10 行代码──

## Hãy sử dụng nó để thực hiện

PyTorch, 2026 ngôn ngữ:

> PyTorch,2026 năm sử dụng quen thuộc:

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.2-3B-Instruct")
tok = AutoTokenizer.from_pretrained("meta-llama/Llama-3.2-3B-Instruct")

prompt = "Attention is all you need because"
inputs = tok(prompt, return_tensors="pt")
out = model.generate(
    **inputs,
    max_new_tokens=64,
    temperature=0.7,
    top_p=0.9,
    do_sample=True,
)
print(tok.decode(out[0]))
```

Dưới cái nắp,`generate()`chạy chuyển tiếp về phía trước, kéo các logit vị trí cuối cùng, lấy mẫu mã thông báo tiếp theo, thêm nó và lặp lại. Mỗi đống suy luận LLM sản xuất (vLLM, TensorRT-LLM, llama.cpp, Ollama, MLX) thực hiện cùng một vòng lặp với tối ưu hóa nặng  prefill batch, batching liên tục, KV cache paging, giải mã suy đoán.

> Ở tầng dưới,`generate()`运行前向传播,取出最后位置的logits,采样下一个代币,添加到序列中,重复──每个生产 LLM 推理(vLLM、TensorRT-LLM、llama.cpp、Ollama、MLX) đều sử dụng rất nhiều tối ưu hóa để thực hiện cùng một vòng lặp批量预填、连续批处理、KV 缓存分页、推测解码──

**GPT vs BERT, one line each:**GPT dự đoán `P(x_t | x_{<t})`BERT dự đoán`P(x_masked | x_unmasked)`. Khối thối quyết định liệu mô hình có thể tạo ra.

> **GPT 与 BERT 各一句话：**GPT 预测 `P(x_t | x_{<t})`│BERT 预测 │`P(x_masked | x_unmasked)` Lệch hàm quyết định liệu mô hình có thể tạo ra 

## Chuyển nó đi.

Nhìn xem`outputs/skill-sampling-tuner.md`. Kỹ năng chọn các tham số lấy mẫu cho một nhiệm vụ thế hệ mới và đánh dấu khi cần thiết giải mã xác định.

> 参见 `outputs/skill-sampling-tuner.md` Kỹ năng này cho các nhiệm vụ tạo ra mới chọn các tham số,并 đánh dấu khi cần xác định tính giải mã.

## Tập luyện bài tập

1. **Easy.**Đi chạy`code/main.py`và xác minh các hình tử liệu chú ý nguyên nhân là ba góc dưới sau softmax.
   Trung ngữ翻译:运行 `code/main.py`, xác định nguyên nhân tập trung tập trung trong softmax 后是下三角的──抽查:
2. **Medium.**Thực hiện tìm kiếm chùm để có chiều rộng 4. So sánh sự bối rối của chùm-4 so với tham lam trên 10 lời nhắc ngắn.
   Trong 10 câu ngắn gọn trên so sánh câu hỏi tìm kiếm và tìm kiếm tham lam. Câu hỏi tìm kiếm nhất định tốt hơn?
3. **Hard.**Thực hiện giải mã phỏng đoán: sử dụng mô hình 2 tầng nhỏ như bản thảo và mô hình 6 tầng như xác minh. đo tốc độ đồng hồ tường trên 100 hoàn thành chiều dài 64.
   Trung ngữ翻译:实现推测解码: dùng 2层小模型作为草案模型,6层模型作为验证器── 在 100 个长度为 64 的补充上测量实际加速比──确认输出与验证器的贪心解码一致──

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Causal mask | "The triangle" | Upper-triangular `-inf` matrix added to attention scores so position `i` only sees positions `≤ i`. |
| 因果掩码 | "三角矩阵" | 加到注意力分数上的上三角 `-inf` 矩阵，使位置 `i` 只能看到位置 `≤ i`。 |
| Next-token prediction | "The loss" | Cross-entropy of the model's distribution against the true next token at every position. |
| 下一个 token 预测 | "损失函数" | 模型分布与每个位置真实下一个 token 之间的交叉熵。 |
| Autoregressive | "Generate one at a time" | Feed output back as input; parallelism only during training, not during generation. |
| 自回归 | "逐个生成" | 将输出反馈为输入；仅在训练时并行，生成时不并行。 |
| Logits | "Pre-softmax scores" | Raw output of the LM head before softmax; sampling happens on these. |
| Logits | "softmax 前的分数" | LM 头在 softmax 之前的原始输出；采样基于这些值。 |
| Temperature | "Creativity knob" | Divide logits by T; T→0 = greedy, T→∞ = uniform. |
| 温度 | "创造力旋钮" | 将 logits 除以 T；T→0 为贪心，T→∞ 为均匀分布。 |
| Top-p | "Nucleus sampling" | Truncate distribution to smallest set summing to ≥p; sample from what remains. |
| Top-p | "核采样" | 将分布截断为累积概率 ≥ p 的最小集合；从剩余部分采样。 |
| Min-p | "Better than top-p" | Keep tokens where `p ≥ min_p × max_p`; adapts cutoff to sharpness of distribution. |
| Min-p | "比 top-p 更好" | 保留 `p ≥ min_p × max_p` 的 token；根据分布锐度自适应调整截断。 |
| Speculative decoding | "Draft + verify" | Cheap model proposes N tokens; big model verifies in parallel. |
| 推测解码 | "草案+验证" | 廉价模型提出 N 个 token；大模型并行验证。 |
| Teacher forcing | "Training trick" | During training, feed the true previous token, not the model's prediction. Standard for every seq2seq LM. |
| Teacher forcing | "训练技巧" | 训练时输入真实的前一个 token，而非模型的预测。所有 seq2seq 语言模型的标准做法。 |

## Xem thêm 延伸阅读

- [Radford et al. (2018). Improving Language Understanding by Generative Pre-Training](https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf) GPT-1.
  Trung ngữ翻译:GPT-1 论文。
- [Radford et al. (2019). Language Models are Unsupervised Multitask Learners](https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf) GPT-2.
  Trung ngữ翻译:GPT-2 论文。
- [Brown et al. (2020). Language Models are Few-Shot Learners](https://arxiv.org/abs/2005.14165) GPT-3 và học tập trong bối cảnh.
  Trung ngữ翻译:GPT-3 和上下文学习论文──
- [Leviathan, Kalman, Matias (2023). Fast Inference from Transformers via Speculative Decoding](https://arxiv.org/abs/2211.17192) giấy giải mã kỹ thuật.
  Trung ngữ翻译:推测解码论文。
- [HuggingFace `modeling_llama.py`](https://github.com/huggingface/transformers/blob/main/src/transformers/models/llama/modeling_llama.py) mã tham chiếu nguyên nhân-LM.
  Trung文翻译:HuggingFace Llama 因果语言模型参考代码──
