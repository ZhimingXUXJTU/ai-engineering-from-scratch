# Ưu điểm giải mã  Dự thảo, xác minh, lặp lại  Ưu điểm giải mã  Ưu điểm 验证、重复

> Autoregressive decoding là hàng loạt. Mỗi token chờ đợi cho token trước đó. Spekulative decoding phá vỡ chuỗi: một mô hình rẻ tiền che chở N token, mô hình đắt tiền xác minh tất cả N trong một lần đi trước. Khi dự thảo đúng, bạn đã trả một tiền lớn cho N thế hệ.

> **【中文解读】**Sử dụng mô hình nhỏ nhanh tạo mã thông báo ứng cử, mô hình lớn xác nhận khối lượng.

**Type:** Hands-on | **类型:** 动手
**Language:**Python**语言:**Python
**Prerequisites:** Phase 7 · 07 (GPT Causal LM), Phase 7 · 12 (KV Cache & Flash Attention) | **前置知识:** Phase 7 · 07 (GPT Causal LM), Phase 7 · 12 (KV Cache & Flash Attention)
**Time:** ~60 minutes | **时间:** ~60 分钟

## Vấn đề  vấn đề giới thiệu

Một mẫu 70B LLM lấy một token mất ~ 30 ms trên một H100. Một mô hình dự thảo 3B mất ~ 3 ms. Nếu chúng ta để dự thảo 3B 5 token trước, sau đó chạy 70B * một lần * để xác minh tất cả 5, tổng là `5×3 + 30 = 45 ms`cho tối đa 5 token được chấp nhận  so với `5×30 = 150 ms`Đó là mức độ giải mã đầu cơ đầy đủ: trao đổi một lượng nhỏ bộ nhớ GPU bổ sung (chương trình dự thảo) cho độ trễ giải mã thấp hơn 24x.

> Một 70B LLM  lấy một token trong H100 lên cần khoảng 30 ms。 một 3B 草案 mô hình cần khoảng 3 ms。 Nếu chúng ta cho 3B 提前 tạo ra 5 token, sau đó chạy 70B * một lần* xác nhận tất cả 5 个,总时间为 `5×3 + 30 = 45 ms`Tối đa nhận được 5 token được chấp nhận và cần phải phát triển trực tiếp`5×30 = 150 ms` Đó là toàn bộ điểm bán của các mã: sử dụng một số lượng nhỏ GPU trong lưu trữ

Trù này phải bảo vệ phân phối. Tiêu chuẩn lấy mẫu dự đoán, được đưa ra bởi Leviathan et al. (2023) và bởi Chen et al. đồng thời, đảm bảo rằng chuỗi đầu ra là **identically distributed**Không có sự thỏa hiệp về chất lượng, chỉ nhanh hơn.

> Kỹ thuật này phải giữ được sự phân bố không thay đổi.**完全相同**Không mất chất lượng. Chỉ nhanh hơn.

Bốn gia đình của các cặp kiểm tra dự thảo thống trị suy luận 2026:

> 4 loại thiết bị kiểm chứng dự thảo chiếm ưu thế trong năm 2026:

1. **Vanilla speculative (Leviathan 2023).**Mô hình dự thảo riêng biệt (ví dụ: Llama 3 1B) + xác minh (ví dụ: Llama 3 70B).
   Trung ngữ翻译:**朴素推测（Leviathan 2023）。**独立的草案模型(如 Llama 3 1B) + 验证器(如 Llama 3 70B) 👇
2. **Medusa (Cai 2024).**Nhiều đầu giải mã trên xác minh dự đoán vị trí `t+1..t+k`Không có mô hình dự thảo riêng biệt.
   Trung ngữ翻译:**Medusa（Cai 2024）。**Nhiều giải pháp trên máy kiểm tra và vị trí dự đoán`t+1..t+k`Không cần mô hình bản thảo độc lập
3. **EAGLE family (Li 2024, 2025).**Dự thảo nhẹ sử dụng lại các trạng thái ẩn của người xác minh; tỷ lệ chấp nhận gần hơn so với vanilla; 34× điển hình.
   Trung ngữ翻译:**EAGLE 系列（Li 2024, 2025）。**复用验证器隐藏状态的轻量草案; 接受率比简单方案更高;典型加速3-4倍──
4. **Lookahead decoding (Fu 2024).**- Không cần mô hình dự thảo, tự đoán, không phụ thuộc.
   Trung ngữ翻译:**前瞻解码（Fu 2024）。**Jacobi 代;完全不需要草案模型──自推测──小众但无依赖──

Mỗi sản xuất kết luận xếp chồng vào năm 2026 tàu dự đoán giải mã mặc định. vLLM, TensorRT-LLM, SGLang, và llama.cpp tất cả hỗ trợ ít nhất vanilla + EAGLE-2.

> Mỗi năm 2026 mỗi sản xuất được đưa ra đều được đưa ra theo ý định.

> **【中文解读】**推测解码的核心洞察:自归生成是串行瓶──用小模型(3B)快速生成 N 个候选代币,大模型(70B) một lần前向传播验证所有 N 个──总时间从 N×30ms 降至 5×3+30=45ms,加速 2-4 倍──关键:推测采样保证输出分布与大模型完全一致,无质量损失──

> **【拓展：EAGLE 与 Medusa 的自推测策略】**EAGLE(2024) Sử dụng trạng thái ẩn của mô hình lớn để tạo ra bản thảo, tỷ lệ chấp nhận cao hơn mô hình nhỏ độc lập, tăng tốc điển hình 3-4 lần.

## Khái niệm cốt lõi

### Các thuật toán cốt lõi

Với một người xác minh `M_q`và một bản thảo rẻ hơn `M_p`- Có thể là:

> 给定验证器 `M_q`Và rẻ hơn mô hình dự thảo `M_p`- Có thể là:

1. Để `x_1..x_k`là tiền tố đã được giải mã.
   中文翻译:设 `x_1..x_k`Vì đã giải mã trước 🏼
2. **Draft**: sử dụng `M_p`để tự lập lập đề xuất `d_{k+1}, d_{k+2}, ..., d_{k+N}`với dự thảo xác suất `p_1..p_N`- Tôi không biết.
   Trung ngữ翻译:**草案**:用 `M_p`自归地 đề xuất`d_{k+1}, d_{k+2}, ..., d_{k+N}`,附带草案概率 `p_1..p_N`
3. **Verify in parallel**: chạy `M_q`Một lần nữa `x_1..x_k, d_{k+1}, ..., d_{k+N}`, nhận xác minh xác suất `q_1..q_{N+1}`cho các vị trí `k+1..k+N+1`- Tôi không biết.
   Trung ngữ翻译:**并行验证**: đối với `x_1..x_k, d_{k+1}, ..., d_{k+N}`运行 một lần `M_q`, lấy vị trí `k+1..k+N+1`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `q_1..q_{N+1}`
4. **Accept/reject each draft token left to right**: cho mỗi `i`, chấp nhận với khả năng`min(1, q_i(d_i) / p_i(d_i))`- Tôi không biết.
   Trung ngữ翻译:**从左到右接受/拒绝每个草案 token**: đối với mỗi người`i`, theo tỷ lệ`min(1, q_i(d_i) / p_i(d_i))`接受──
5. Khi bị từ chối lần đầu tiên tại vị trí `j`: mẫu `t_j`từ phân phối "bỏ còn" `(q_j - p_j)_+`Tất cả các bản thảo sau đó`j`được loại bỏ.
   Trung ngữ翻译: 在位置 `j`首次被拒绝时: Từ phân bố "残差"`(q_j - p_j)_+`归一化后采样 `t_j``j`Sau đó tất cả các dự án đã bị bỏ rơi.
6. Về việc chấp nhận tất cả`N`: mẫu một token thêm `t_{N+1}`từ `q_{N+1}`(tương hiệu tiền thưởng miễn phí).
   中文翻译:当所有 `N`个都被接受时: từ `q_{N+1}`采样一个额外的标志 `t_{N+1}`(tín hiệu thưởng miễn phí)

Trù phân phối dư là cái nhìn toán học giữ cho sản phẩm được phân phối chính xác như thể `M_q`đã lấy mẫu từ đầu.

> Các kỹ thuật phân phối khác biệt là giữ phân phối xuất và`M_q`Từ đầu, hình thức toán học hoàn toàn giống nhau.

### Điều gì quyết định tốc độ

Để `α`= tỷ lệ chấp nhận dự kiến cho mỗi dự án token.`c`= tỷ lệ chi phí dự thảo đối với kiểm tra viên.

> 设 `α`= Tỷ lệ chấp nhận dự kiến của mỗi mã dự thảo.`c`= Chi phí dự thảo với chứng minh:

- Thế hệ ngây thơ sẽ gọi 1 mẫu lớn cho mỗi token.
  Trung文翻译:朴素生成每个代币调用一次大模型──
- Tiêu chuẩn cho 1 cuộc gọi lớn mỗi tháng`(1 - α^{N+1}) / (1 - α) ≈ 1/(1-α)`token khi `α`cao.
  Trung ngữ翻译:推测解码在 `α`较高时, mỗi `(1 - α^{N+1}) / (1 - α) ≈ 1/(1-α)`个 token 调用一次大模型──

Quy tắc điển hình của thằng bé`α = 0.75`và `N = 5`: 3 lần ít hơn các cuộc gọi lớn mô hình. chi phí dự thảo là 5 lần rẻ. Tổng đồng hồ tường giảm ~ 2,5 lần.

> `α = 0.75`和 `N = 5`时的典型经验法则: 模型调用减少 3 倍. 草案成本是 5 倍便宜.

> **【中文解读】**加速效果取决于接受率 alpha──当 alpha=0.75、草案长度 N=5 时,大约3倍减少大模型调用──残差分布(残差分布) là một yếu tố quan trọng trong phân bố (q-p) + phân bố trong phân bố, đảm bảo kết quả cuối cùng phù hợp với phân bố trực tiếp của mô hình lớn──

**α depends on:**

> **α 取决于：**

- Đề án tương ứng tốt với xác minh.
  Trung ngữ翻译:草案对验证器的近似程度──同系列/同训练数据显著提升 α──
- Chiến lược giải mã: dự thảo tham lam chống lại xác minh tham lam: cao α. Tiêu chuẩn lấy mẫu: khó để phù hợp; chấp nhận giảm.
  Trung ngữ翻译:解码策略──贪心草案对贪心验证器:高 α──温度采样:更难匹配;接受率下降──
- Loại nhiệm vụ: Mã và kết quả cấu trúc chấp nhận nhiều hơn (đáng dự đoán); viết sáng tạo dạng tự do chấp nhận ít hơn.
  Trung ngữ翻译:任务类型──代码和结构化输出接受更多(可预测);自由形式创意写作接受更少──

### Medusa  Dự thảo không có mô hình dự thảo

Medusa thay thế mô hình dự thảo bằng các đầu đầu ra ngoài thêm trên xác minh.`t`- Có thể là:

> Medusa sử dụng trên máy kiểm tra thêm đầu tư thay thế mô hình.`t`- Có thể là:

```
shared trunk → hidden h_t
    ├── head_0: predict token at t+1  (standard LM head)
    ├── head_1: predict token at t+2
    ├── head_2: predict token at t+3
    ├── head_3: predict token at t+4
```

Mỗi đầu phát ra logits của riêng mình. Khi suy luận bạn lấy mẫu từ mỗi đầu để có được một chuỗi ứng cử viên, sau đó xác minh bằng một lần đi trước bằng cách sử dụng một kế hoạch chú ý cây xem xét tất cả các tiếp tục ứng cử viên cùng một lúc.

> Mỗi đầu xuất bản logits của riêng mình. Khi đưa ra ý kiến, mỗi đầu lấy một chuỗi ứng cử viên, sau đó sử dụng một chương trình chú ý để truyền tải một lần, đồng thời xem xét tất cả các ứng cử viên.

Lợi thế: không có mô hình thứ hai. Khối thấu: thêm các tham số có thể đào tạo; cần một giai đoạn điều chỉnh tinh tế được giám sát (~ 1B token); tỷ lệ chấp nhận thấp hơn một chút so với loại vanilla đầu cơ với một bản thảo tốt.

> 优点:无需第二模型──缺点:增加可训练参数;需要监督微调阶段(约1B token); 接受率比好的草案模型的朴素推测略低──

> **【拓展：推测解码在 vLLM 中的实现】**vLLM là khung lý luận LLM phổ biến nhất năm 2026, nguyên sinh hỗ trợ việc phân tích phân tích. Nó sử dụng tiếp tục xử lý hàng loạt (continuous batching) + PagedAttention + 推测解码的组合优化. Trong triển khai sản xuất, việc phân tích phân tích thường mang lại 2-3 lần giảm chậm, đối với các tình huống trò chuyện.

### Eagle  mô tả tốt hơn bằng cách tái sử dụng các trạng thái ẩn

EAGLE-1/2/3 (Li et al., 20242025) làm cho mô hình dự thảo trở thành một biến thể nhỏ (thường là 1 lớp) hấp thụ các trạng thái ẩn lớp cuối cùng của người xác minh. Bởi vì dự thảo thấy đại diện tính năng của người xác minh, dự đoán của nó tương quan chặt chẽ với phân phối đầu ra của người xác minh. Tỷ lệ chấp nhận tăng từ ~ 0.6 (vanilla) lên 0.85+.

> EAGLE-1/2/3 ((Li 等人,2024-2025) sẽ mô hình dự thảo được làm thành một biến thể nhỏ (((thường là 1 tầng), tình trạng ẩn của tầng cuối cùng của máy kiểm chứng hấp thụ.

EAGLE-3 (2025) đã thêm tìm kiếm cây trên các tiếp tục ứng cử viên. vLLM và SGLang tàu EAGLE-2/3 như là con đường thông số mặc định cho Llama 3/4 và Qwen 3.

> EAGLE-3(2025) đã thêm vào các tìm kiếm cây trong ứng cử tiếp tục.

### Vũ vẹ KV

Các nguồn cấp dữ liệu xác minh `N`dự thảo mã thông báo vào xác minh trong một lần đi trước. Điều này mở rộng bộ nhớ cache KV của xác minh bởi `N`Nếu một số bản thảo bị từ chối, bạn phải xoay bộ nhớ cache trở lại chiều dài tiền tố được chấp nhận.

> 验证在一次前向传播中将 `N`个草案 token 输入验证器── đây sẽ là KV của验证器 缓存扩展 `N`个条目── Nếu một số dự thảo bị từ chối, bạn phải sẽ lưu trữ trở lại vòng dài trước đã được chấp nhận──

Các thực hiện sản xuất (vLLM's `--speculative-model`- Thử xử lý với các bộ đệm KV.

> 生产实现(vLLM của `--speculative-model`、TensorRT-LLM của LookaheadDecoder) sử dụng tạm thời KV 缓冲区 xử lý vấn đề này──先写入,接受时提交──概念上不难,但实现上比较繁──

## Hãy xây dựng nó.
```figure
draft-verify-tokens
```

## Hãy xây dựng nó

Nhìn xem`code/main.py`Chúng tôi thực hiện thuật toán lấy mẫu đầu cơ cốt lõi (phases of rejection + residual distribution) với:

> 参见 `code/main.py`△ Chúng tôi sử dụng các bộ phận sau để thực hiện các thuật toán chính thức:

- Một "chương trình lớn" là một xác định-softmax trên một phân phối mã hóa bằng tay (vì vậy chúng ta có thể xác minh toán học chấp nhận phân tích).
  Trung ngữ翻译:一个"大模型", là một định tính mềm trên phân bố mã hóa (手动编码分布上的确定性 softmax) để phân tích các chứng nghiệm (验证接受数学) ⋅
- Một "mô hình bản thảo" là một sự xáo trộn của mô hình lớn.
  Trung ngữ翻译:一个"草案模型", là phiên bản rối loạn của mô hình lớn.
- Một vòng chấp nhận / từ chối tạo ra phân phối biên tương tự như lấy mẫu trực tiếp.
  Trung ngữ翻译: một chu kỳ chấp nhận/ từ chối, tạo ra phân bố cùng một cạnh tranh với mẫu trực tiếp.

### Bước 1: Bước từ chối

```python
def accept_or_reject(q_prob, p_prob, draft_token, u):
    ratio = q_prob / p_prob if p_prob > 0 else float("inf")
    return u < min(1.0, ratio)
```

`u`là một số ngẫu nhiên đồng nhất. `q_prob`là xác định xác suất của người xác minh cho token được soạn thảo. `p_prob`Lý thuyết Leviathan là quyết định Bernoulli này, tiếp theo là lấy mẫu từ phần còn lại khi từ chối, bảo tồn phân bố xác minh chính xác.

> `u`là trung bình với số lượng.`q_prob` xác nhận đối với dự án token`p_prob`Ưu điểm của mô hình dự thảo. Ưu điểm Leviathan cho thấy, quyết định này cộng với việc từ chối các mẫu dư thừa, có thể đảm bảo sự phân bố của các nhà chứng nhận.

### Bước 2: phân phối dư

```python
def residual_dist(q, p):
    raw = [max(0.0, qi - pi) for qi, pi in zip(q, p)]
    s = sum(raw)
    return [r / s for r in raw]
```

Giảm `p`từ `q`- Nhìn vào các yếu tố, clamp các giá trị âm xuống 0, tái bình thường hóa.

> 个元素 từ `q`减去 `p`, sẽ cắt giá trị âm thành 0, tái归结.

### Bước 3: một bước đầu cơ

```python
def spec_step(prefix, q_model, p_model, N, rng):
    drafts = []
    p_probs = []
    ctx = list(prefix)
    for _ in range(N):
        p_dist = p_model(ctx)
        d = sample(p_dist, rng)
        drafts.append(d)
        p_probs.append(p_dist[d])
        ctx.append(d)

    q_dists = [q_model(prefix + drafts[:i]) for i in range(N + 1)]

    for i, d in enumerate(drafts):
        u = rng.random()
        q_prob = q_dists[i][d]
        p_prob = p_probs[i]
        if u < min(1.0, q_prob / p_prob if p_prob > 0 else float("inf")):
            prefix = prefix + [d]
        else:
            res = residual_dist(q_dists[i], p_model(prefix))
            prefix = prefix + [sample(res, rng)]
            return prefix
    prefix = prefix + [sample(q_dists[N], rng)]
    return prefix
```

Năm chấp nhận → một tiền thưởng → sáu token được sản xuất trong một thẻ xác minh.

> 五个被接受 → 一个奖励 → 一次验证器通行产生六个代币──

### Bước 4: đo lường tỷ lệ chấp nhận

Thực hiện 10.000 bước đầu cơ ở các cấp độ chất lượng dự thảo khác nhau. tỷ lệ chấp nhận bản đồ so với sự khác biệt KL giữa phân phối dự thảo và xác minh. Bạn nên thấy một mối quan hệ đơn tần sạch.

> Trong các dự thảo khác nhau trên cấp độ chất lượng chạy 10.000 lần đề xuất bước.

### Bước 5: kiểm tra sự tương đương phân phối

Theo kinh nghiệm: histogram của các token được tạo ra bởi vòng đầu cơ nên phù hợp với histogram được tạo ra bằng cách lấy mẫu trực tiếp từ người xác minh. Đây là định lý Leviathan trong thực tế. Một thử nghiệm chi-quad xác nhận trong sai lầm lấy mẫu.

> 经验上: 推测循环产生的符号直方图应与直接从验证器采采样直方图匹配――这是实践中的Leviathan定理――卡方检验在采样错误范围内确认――

## Hãy sử dụng nó để thực hiện

Sản xuất:

> 生产部署:

```bash
# vLLM with EAGLE
vllm serve meta-llama/Llama-3.1-70B-Instruct \
    --speculative-model /models/llama-3.1-eagle-70b \
    --speculative-draft-tensor-parallel-size 1 \
    --num-speculative-tokens 5

# vLLM with vanilla draft model
vllm serve meta-llama/Llama-3.1-70B-Instruct \
    --speculative-model meta-llama/Llama-3.2-1B-Instruct \
    --num-speculative-tokens 5
```

TensorRT-LLM có con đường Medusa nhanh nhất từ giữa năm 2026. `faster-whisper`bao trùm mã hóa giả định cho Whisper-large với một bản thảo nhỏ.

> TensorRT-LLM sẽ có đường Medusa nhanh nhất trong giai đoạn giữa năm 2026:`faster-whisper`Để nói chuyện với người khác, hãy dùng mô hình sơ đồ nhỏ.

**Picking a draft:**

> **选择草案策略：**

| Strategy | When to pick | Speedup |
|----------|--------------|---------|
| 策略 | 何时选择 | 加速比 |
| Vanilla draft (1B/3B Llama family) | Fast prototype, no training | 1.8–2.3× |
| 朴素草案（1B/3B Llama 系列） | 快速原型，无需训练 | 1.8–2.3× |
| Medusa heads | You can fine-tune the verifier | 2–3× |
| Medusa 头 | 可以微调验证器 | 2–3× |
| EAGLE-2 / 3 | Production, max speed | 3–4× |
| EAGLE-2 / 3 | 生产环境，最大速度 | 3–4× |
| Lookahead | No draft, no training, no extra params | 1.3–1.6× |
| 前瞻 | 无草案，无训练，无额外参数 | 1.3–1.6× |

**When NOT to spec-decode:**

> **何时不使用推测解码：**

- Tạo ra 1-5 token, tổng chi phí thống trị.
  Trung文翻译:1-5 token 的单序列生成──开销占主导──
- Tiêu chuẩn mẫu sáng tạo / nhiệt độ cao (α giảm).
  Trung文翻译:高度创意/高温采样(α 下降)
- Việc triển khai bị hạn chế trong bộ nhớ (chương trình dự thảo thêm VRAM).
  Trung文翻译:内存受限的部署(草案模型增加显存)

## Chuyển nó đi.

Nhìn xem`outputs/skill-spec-decode-picker.md`Kỹ năng chọn một chiến lược giải mã phỏng đoán (vanilla / Medusa / EAGLE / lookahead) và điều chỉnh các tham số (N, nhiệt độ dự thảo) cho khối lượng công việc suy luận mới.

> 参见 `outputs/skill-spec-decode-picker.md`△ Đây là một kỹ năng cho các công việc mới ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎

## Tập luyện bài tập

1. **Easy.**Đi chạy`code/main.py`. xác nhận phân phối mã thông báo đầu cơ phù hợp với phân phối mẫu trực tiếp của người xác minh trên 50.000 mã thông báo trong chi-quad p > 0,05.
   Trung ngữ翻译:运行 `code/main.py`❖ xác nhận trên 50.000 token, token đề xuất phân phối với chứng thực trực tiếp được phân phối trên các bài kiểm tra p > 0.05 trong phù hợp ❖
2. **Medium.**Tốc độ nhanh hóa (tốc hiệu cho mô hình lớn tiến) như một hàm của `N`cho `α = 0.5, 0.7, 0.85`- Định vị tối ưu `N`cho mỗi α. (Công báo: dự kiến token cho mỗi cuộc gọi xác minh = `(1 - α^{N+1}) / (1 - α)`.)
   Trung ngữ翻译:绘制 `α = 0.5, 0.7, 0.85`时加速比( mỗi lần lớn mô hình tiến lên của biểu tượng số) với `N`Quan hệ: xác định lợi thế của mỗi α`N`△  提示: mỗi lần thử nghiệm调用预期 token 数 = `(1 - α^{N+1}) / (1 - α)`◊)
3. **Hard.**Thực hiện một Medusa nhỏ: lấy GPT đá cuối từ Bài học 14, thêm 3 đầu LM bổ sung dự đoán các vị trí t + 2, t + 3, t + 4. Tập luyện trên Tinyshakespeare với một mất nhiều đầu chung. So sánh tỷ lệ chấp nhận so với một bản thảo vanilla được tạo bằng cách cắt giảm mô hình tương tự.
   Trung ngữ翻译:实现一个小型Medusa:取第14 课的GPT毕业项目,添加 3 额外的LM 头预测位置 t+2、t+3、t+4──用联合多头损失在小小小的培训──比较与截断相同模型得到的简单草案的接受率──
4. **Hard.**Thực hiện rollback: bắt đầu với một dự trữ dự trữ KV tiền đề 10 token, cấp dữ liệu 5 dự thảo token, mô phỏng từ chối ở vị trí 3. Kiểm tra đọc cache của bạn phù hợp với " dự thảo + 2 dự thảo được chấp nhận đầu tiên" ở lần lặp tiếp theo.
   Trung文翻译:实现回滚: từ 10 token 的前 KV 缓存开始,输入 5 个草案代币,模拟位置 3 的拒绝――验证你的缓存读取在下次代时正确匹配"前 + 前 2 个已接受草案"――

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Draft model | "The cheap one" | A smaller model that proposes candidate tokens; usually 10–50× cheaper than the verifier. |
| 草案模型 | "便宜的那个" | 提出候选 token 的较小模型；通常比验证器便宜 10-50 倍。 |
| Verifier | "The big one" | The target model whose distribution we preserve; runs once per speculative step. |
| 验证器 | "大的那个" | 我们要保持其分布的目标模型；每次推测步骤运行一次。 |
| Acceptance rate (α) | "How often the draft is right" | Per-token probability that the verifier accepts the draft. 0.7–0.9 typical. |
| 接受率 (α) | "草案正确的频率" | 验证器接受草案的每 token 概率。典型值 0.7-0.9。 |
| Residual distribution | "The rejection fallback" | `(q - p)_+` normalized; sampling from this on rejection preserves the verifier's distribution. |
| 残差分布 | "拒绝时的后备方案" | `(q - p)_+` 归一化；拒绝时从中采样保持验证器的分布。 |
| Bonus token | "The free one" | When all N drafts accepted, sample one more from the verifier's next-step distribution. |
| 奖励 token | "免费的那个" | 当所有 N 个草案被接受时，从验证器的下一步分布中多采样一个。 |
| Medusa | "Draft-less speculative" | Multiple LM heads on the verifier predict positions t+1..t+k in parallel. |
| Medusa | "无草案推测" | 验证器上的多个 LM 头并行预测位置 t+1..t+k。 |
| EAGLE | "Hidden-state draft" | Tiny transformer draft conditioned on the verifier's last-layer hidden states. |
| EAGLE | "隐藏状态草案" | 以验证器最后一层隐藏状态为条件的小型 Transformer 草案。 |
| Lookahead decoding | "Jacobi iteration" | Self-speculation using a fixed-point iteration; no draft model. |
| 前瞻解码 | "Jacobi 迭代" | 使用不动点迭代的自推测；无需草案模型。 |
| Tree attention | "Verify many candidates at once" | Branching verification that considers several draft continuations simultaneously. |
| 树注意力 | "同时验证多个候选" | 同时考虑多个草案续写的分支验证。 |
| KV rollback | "Undo rejected drafts" | Scratch KV buffer; commit on acceptance, discard on reject. |
| KV 回滚 | "撤销被拒绝的草案" | 临时 KV 缓冲区；接受时提交，拒绝时丢弃。 |

## Xem thêm 延伸阅读

- [Leviathan, Kalman, Matias (2023). Fast Inference from Transformers via Speculative Decoding](https://arxiv.org/abs/2211.17192) thuật toán cốt lõi và định lý tương đương.
  Trung ngữ翻译:推测解码的核心算法和等价定理论文──
- [Chen et al. (2023). Accelerating Large Language Model Decoding with Speculative Sampling](https://arxiv.org/abs/2302.01318) giới thiệu đồng thời; minh chứng từ chối Bernoulli sạch.
  Trung ngữ翻译:同时期发表的推测采样论文;清晰的伯努利拒绝证明──
- [Cai et al. (2024). Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads](https://arxiv.org/abs/2401.10774) Bức giấy Medusa; kiểm tra sự chú ý của cây.
  Trung文翻译:Medusa 论文;树注意力验证。
- [Li et al. (2024). EAGLE: Speculative Sampling Requires Rethinking Feature Uncertainty](https://arxiv.org/abs/2401.15077) EAGLE-1; dự thảo có điều kiện ẩn trong nhà nước.
  Trung文翻译:EAGLE-1 论文;隐藏状态条件草案。
- [Li et al. (2024). EAGLE-2: Faster Inference of Language Models with Dynamic Draft Trees](https://arxiv.org/abs/2406.16858) Eagle-2; độ sâu động của cây.
  Trung文翻译:EAGLE-2 论文;动态树深度。
- [Li et al. (2025). EAGLE-3: Scaling up Inference Acceleration of Large Language Models via Training-Time Test](https://arxiv.org/abs/2503.01840) Eagle-3.
  Trung文翻译:EGLE-3 论文。
- [Fu et al. (2024). Break the Sequential Dependency of LLM Inference Using Lookahead Decoding](https://arxiv.org/abs/2402.02057) Nhìn thẳng vào phía trước, không có kế hoạch tiếp cận.
  Trung ngữ翻译:前解码论文,无草案方案──
- [vLLM docs — Speculative Decoding](https://docs.vllm.ai/en/latest/features/spec_decode.html) tham chiếu sản xuất theo quy định của luật pháp với tất cả bốn chiến lược được kết nối.
  Trung文翻译:vLLM 推测解码文档,四种策略的生产参考──
- [SafeAILab / EAGLE reference implementation](https://github.com/SafeAILab/EAGLE) mã tham chiếu cho EAGLE-1/2/3.
  Trung文翻译:EGLE-1/2/3 参考实现代码──
