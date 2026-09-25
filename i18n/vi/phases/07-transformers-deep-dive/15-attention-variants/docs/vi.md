# Sự chú ý Variants  cửa sổ trượt, Sparse, khác biệt  Sự chú ý biến đổi  cửa sổ trượt 稀疏 差分注意

> Tất cả sự chú ý là một vòng tròn. Mỗi token nhìn thấy mỗi token, và bộ nhớ trả giá. Bốn biến thể xoay hình dạng của vòng tròn và phục hồi một nửa chi phí.

> **【中文解读】**标准注意力 O(n^2) 复杂度太贵;;滑动窗口注意力(Mistral) 稀疏注意力、差分注意力是降低复杂度的方法──

**Type:** Hands-on | **类型:** 动手
**Language:**Python**语言:**Python
**Prerequisites:** Phase 7 · 02 (Self-Attention), Phase 7 · 03 (Multi-Head), Phase 7 · 12 (KV Cache / Flash Attention) | **前置知识:** Phase 7 · 02 (Self-Attention), Phase 7 · 03 (Multi-Head), Phase 7 · 12 (KV Cache / Flash Attention)
**Time:** ~60 minutes | **时间:** ~60 分钟

## Vấn đề  vấn đề giới thiệu

Chi phí chăm sóc đầy đủ `O(N²)`trí nhớ và`O(N²)`tính toán theo chiều dài chuỗi. Đối với một Llama 3 70B 128K-context là 16 tỷ lần chú ý mỗi lớp, nhân 80 lớp.`O(N²)`Memory kích hoạt nhưng không thay đổi chi phí toán học  mỗi token vẫn phục vụ cho mỗi token khác.

> Tất cả sự chú ý là về bộ nhớ và tính toán chi phí trên chiều dài của chuỗi.`O(N²)`❖ Đối với 128K 上下文 ◦ Llama 3 70B, đó là mỗi tầng 160 tỷ chú ý, nhân lên 80 tầng.`O(N²)` mỗi token  vẫn quan tâm đến mỗi token khác 

Ba lớp biến thể thay đổi topology của bản thân ma trận chú ý:

> Ba loại biến thể đã thay đổi cấu trúc của tập thể chú ý:

1. **Sliding window attention (SWA).**Mỗi token sẽ được xem xét bởi một cửa sổ hàng xóm, không phải là tiền tố đầy đủ.`O(N · W)`nơi `W`Gemma 2/3, Mistral 7B, Phi-3-Long.
   Trung ngữ翻译:**滑动窗口注意力 (SWA)。**Mỗi token chỉ tập trung vào khu vực lân cận của cửa sổ cố định, chứ không phải toàn bộ trước ──内存和计算降至 `O(N · W)`, trong số đó `W`Đó là cửa sổ lớn. Gemma 2/3 Mistral 7B.
2. **Sparse / block attention.**Chỉ có các cặp được chọn `(i, j)`Đánh giá số điểm, phần còn lại bị buộc phải giảm trọng lượng. Longformer, BigBird, OpenAI thâm hụt.
   Trung ngữ翻译:**稀疏/块注意力。**Chỉ có một lựa chọn`(i, j)`Đối với được đánh giá; phần còn lại bị ép buộc phải làm 0 trọng lượng.
3. **Differential attention.**Xét hai bản đồ chú ý với các dự đoán Q / K riêng biệt, trừ một từ một. Tử "trọn trọng tâm" làm chảy máu trọng lượng vào vài token đầu tiên. DIFF Transformer của Microsoft (2024).
   Trung ngữ翻译:**差分注意力。**Sử dụng Q/K độc lập 投影计算两个注意力图,将一个从另一个减去――消除将权重汇聚到前几代币的"注意力汇聚"现象――Microsoft's DIFF Transformer(2024)。

Các mô hình biên giới 2026 thường trộn lẫn chúng: hầu hết các lớp là SWA-1024, mỗi thứ năm là toàn cầu toàn bộ chú ý, và một số ít là các đầu khác biệt làm sạch lấy lại.

> 它们 có thể tồn tại chung. Một mô hình tiền tuyến năm 2026 thường sử dụng hỗn hợp: hầu hết các tầng là SWA-1024, mỗi tầng là toàn bộ tập trung, một số ít là phân biệt phân biệt phân biệt trong việc kiểm tra.

> **【中文解读】**三种降低注意力复杂度的方法:(1) 滑窗口(SWA) 只关注局部邻域,O(N*W) 复杂度;(2) 稀疏/块注意力只计算选的代号对;(3) 差分注意力两组 Q/K 注意力相减,消除"注意力汇聚"现象──2026年模型通常混合使用这些变体──

## Khái niệm cốt lõi

### Chú ý cửa sổ trượt (SWA)

Mỗi truy vấn ở vị trí `i`chỉ tham gia vào các vị trí trong `[i - W, i]`(SWA nguyên nhân) hoặc `[i - W/2, i + W/2]`(trong hai hướng) Các token bên ngoài cửa sổ nhận được`-inf`trong số số điểm.

> 位置 `i`Tất cả các truy vấn chỉ liên quan`[i - W, i]`(因果 SWA) hoặc `[i - W/2, i + W/2]`(双向) vị trí trong phạm vi.`-inf`

```
full causal:           sliding window (W=4):
positions 0-7          positions 0-7, W=4
    0 1 2 3 4 5 6 7        0 1 2 3 4 5 6 7
0 | x                0 |  x
1 | x x              1 |  x x
2 | x x x            2 |  x x x
3 | x x x x          3 |  x x x x
4 | x x x x x        4 |    x x x x
5 | x x x x x x      5 |      x x x x
6 | x x x x x x x    6 |        x x x x
7 | x x x x x x x x  7 |          x x x x
```

Vì `N = 8192`và `W = 1024`, các số điểm tử liệu có 1024 × 8192 không bằng 0 hàng trong kỳ vọng  một giảm 8 ×.

>  Đối với `N = 8192`和 `W = 1024`, số lượng mô hình dự kiến có 1024 × 8192 个非零行 giảm 8 lần.

**KV cache shrinks with SWA.**Chỉ là cuối cùng thôi`W`Các token của K và V cần phải được giữ cho mỗi lớp. Đối với cấu hình Gemma-3-ish (1024 cửa sổ, ngữ cảnh 128K), bộ nhớ cache KV giảm 128x.

> **KV 缓存随 SWA 缩小。**Mỗi tầng chỉ cần giữ lại K và V của cuối cùng `W`个 token── đối với các loại Gemma-3 配置(1024 窗口,128K 上下文),KV 缓存 giảm 128 倍──

**Quality cost.**Các bộ chuyển đổi chỉ có SWA gặp khó khăn với việc lấy lại tầm xa. Giải pháp: để lại các lớp SWA với các lớp tập trung đầy đủ. Gemma 3 sử dụng 5:1 SWA: toàn cầu. Mistral 7B sử dụng một đống SWA nguyên nhân nơi thông tin "thường chảy về phía trước" thông qua các cửa sổ chồng chéo  mỗi lớp mở rộng lĩnh vực tiếp nhận hiệu quả bằng 5`W`, và sau đó`L`các lớp mà mô hình có thể tham dự `L × W`Đồ tín hiệu trở lại.

> **质量代价。**纯 SWA Transformer 在长距离检索上表现不佳──修复方案:将 SWA层与全注意层交换使用──Gemma 3 使用 5:1 的 SWA:全局比例──Mistral 7B 使用因果 SWA 堆,信息通过重叠窗口"向前流动"每层将有效感受野扩展`W`- Tôi không biết.`L`Lớp sau mô hình có thể được truy cập lại`L × W`个 token.

### Sự chú ý thâm hụt / ngăn chặn

Chọn một `N × N`Mô hình thắt lưng trước thời gian.

> 预先选择 `N × N`                                                                                                                                                                                                                                                              

- **Local + strided (OpenAI sparse transformer).**Hãy chờ đợi người cuối cùng`W`token cộng với mỗi `stride`-Thiết hiệu trước đó.`O(N · sqrt(N))`tính toán.
  Trung ngữ翻译:**局部 + 步进（OpenAI 稀疏 Transformer）。**关注最后 `W`个 token 加上之前每隔 `stride`个 token.`O(N · sqrt(N))`                                                                                                                                                                                                                                                              
- **Longformer / BigBird.**Cửa sổ địa phương + một bộ nhỏ các token toàn cầu (ví dụ `[CLS]`) được tham gia bởi tất cả mọi người và được tham gia bởi tất cả mọi người + liên kết ngẫu nhiên.
  Trung ngữ翻译:**Longformer / BigBird。**局部窗口 + 少量全局 token(如 `[CLS]`(với tất cả các token 双向关注 + 随机稀疏连接―― thí nghiệm cho thấy trên cùng chất lượng trên tiếp theo mở rộng 2 lần――
- **Native Sparse Attention (DeepSeek, 2025).**Tìm hiểu những khối nào của `(Q, K)`- Vấn đề, bỏ qua các khối không ở cấp độ hạt nhân.
  Trung ngữ翻译:**原生稀疏注意力（DeepSeek，2025）。**Học những gì `(Q, K)`块重要; trong内核级别跳过零块──与 FlashAttention 兼容──

Sparse Attention là một câu chuyện kỹ thuật hạt nhân. toán học đơn giản (mátrix điểm số); chiến thắng đến từ không bao giờ tải các mục 0 vào SRAM. FlashAttention-3 và 2026 FlexAttention API làm cho các mẫu hiếm tùy chỉnh hạng nhất trong PyTorch.

> 稀疏注意力 là một câu chuyện trong ngành công nghiệp hạt nhân.

> **【拓展：滑动窗口的信息传递机制】**滑窗注意力看似只能捕获局部信息,但通过多层堆叠,信息可以"透透"到更远的位置. L层注意力,有效感受野为L×W. Ví dụ: W=1024、L=32 mô hình có hiệu lực感受野为32K token. Mistral 7B đã tận dụng tính năng này trong việc giữ O(N*W) 计算复杂性同时实现长上下文建模――

### Sự chú ý khác biệt (DIFF Transformer, 2024)

Sự chú ý thường xuyên có một vấn đề "thủy bỏ sự chú ý": softmax buộc mỗi hàng cộng lên 1, vì vậy các token không muốn tham gia vào bất cứ điều gì cụ thể sẽ bị đẩy vào khối lượng đầu tiên (hoặc vài đầu tiên).

> 标准注意力有"注意力汇聚"问题:softmax 强制每行总和为 1,所以不想关注任何特定内容的代币会重量倾倒到第一个代币 (或前几个) ;;

Sự chú ý khác biệt khắc phục điều này bằng cách tính toán **two**Bản đồ chú ý và trừ:

> 差分注意力通过计算**两个**chú ý:

```
A1 = softmax(Q1 K1^T / √d)
A2 = softmax(Q2 K2^T / √d)
DiffAttn = (A1 - λ · A2) V
```

nơi `λ`là một scalar được học (thường là 0.50.8). A1 nắm bắt trọng lượng nội dung thực; A2 nắm bắt trục. Phục trừ hủy trục, phân bổ trọng lượng cho các token liên quan.

> Trong số đó `λ`là một tập trung tập trung (khác định là 0.5-0.8): A1  nắm bắt trọng lượng nội dung thực sự; A2  nắm bắt tập trung; A2  giảm tập trung, sẽ phân bổ trọng lượng lại cho các token liên quan.

Kết quả được báo cáo (Microsoft 2024): 510% độ bối rối thấp hơn, bối cảnh hiệu quả dài hơn 1,52x với cùng độ dài được đào tạo, lấy lại kim cương trong đống cỏ sắc hơn.

> 报告结果(Microsoft 2024):困惑度降低 5-10%,同训长度下有效上下文长度增加1.5-2倍,针-in-haystack 检索更精确──

> **【中文解读】**差分注意力创新之处: tiêu chuẩn chú ý vì softmax 归结导致"注意力汇聚" (trong tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung

> **【拓展：Gemma 3 的混合注意力策略】**Google Gemma 3 sử dụng tỷ lệ chi tiết của cửa sổ trượt với toàn bộ sự chú ý  mỗi 5 tầng chi tiết toàn bộ sự chú ý  sau đó là 1 tầng chi tiết toàn bộ sự chú ý . Đây cũng duy trì khả năng xây dựng trên toàn bộ các tầng cung cấp kết nối từ xa), cũng giảm đáng kể chi phí tính toán .

### So sánh khác nhau

| Variant | Compute | KV cache | Quality vs full | Production use |
|---------|---------|----------|-----------------|----------------|
| 变体 | 计算量 | KV 缓存 | 相对全注意力的质量 | 生产使用 |
| Full attention | O(N²) | O(N) per layer | baseline | every model's default layer |
| 全注意力 | O(N²) | 每层 O(N) | 基线 | 每个模型的默认层 |
| SWA (window 1024) | O(N·W) | O(W) per layer | -0.1 ppl, good with global layers | Gemma 2/3, Phi-3-Long |
| 滑动窗口 (窗口 1024) | O(N·W) | 每层 O(W) | -0.1 ppl，配合全局层效果好 | Gemma 2/3, Phi-3-Long |
| Local + strided sparse | O(N·√N) | mixed | similar to SWA | OpenAI sparse transformer, Longformer |
| 局部+步进稀疏 | O(N·√N) | 混合 | 类似 SWA | OpenAI 稀疏 Transformer, Longformer |
| BigBird (local + global + random) | O(N) approx | mixed | matches full at 2× context | early long-context BERT |
| BigBird (局部+全局+随机) | O(N) 近似 | 混合 | 2 倍上下文下匹配全注意力 | 早期长上下文 BERT |
| Native Sparse (DeepSeek-V3.2) | O(N · active fraction) | O(N) | within 0.05 ppl | DeepSeek-V3.2, 2025 |
| 原生稀疏 (DeepSeek-V3.2) | O(N · 活跃比例) | O(N) | 0.05 ppl 以内 | DeepSeek-V3.2, 2025 |
| Differential | O(2·N²) | O(2N) | -5 to -10% ppl | DIFF Transformer, early 2026 models |
| 差分 | O(2·N²) | O(2N) | 困惑度降低 5-10% | DIFF Transformer, 2026 早期模型 |

## Hãy xây dựng nó.
```figure
gqa-kv-sharing
```

## Hãy xây dựng nó

Nhìn xem`code/main.py`Chúng tôi thực hiện một so sánh mặt nạ nhân quả cho thấy toàn bộ, SWA, địa phương + bước, và sự chú ý khác biệt bên cạnh nhau trên một chuỗi đồ chơi.

> 参见 `code/main.py` Chúng tôi thực hiện một máy so sánh ẩn kết quả, trình bày toàn bộ sự chú ý, SWA, địa phương, bước tiến và sự phân biệt sự chú ý trên chuỗi đồ chơi

### Bước 1: mặt nạ nguyên nhân đầy đủ (tầm cơ sở)

```python
def causal_mask(n):
    return [[0.0 if j <= i else float("-inf") for j in range(n)] for i in range(n)]
```

Hình cơ bản từ Bài học 07. Ba giác; trọng lượng không trên đường vạch.

> 第07 课的基线──下三角;对角线上权重为零──

### Bước 2: mặt nạ nhân quả cửa sổ trượt

```python
def swa_mask(n, window):
    M = [[float("-inf")] * n for _ in range(n)]
    for i in range(n):
        lo = max(0, i - window + 1)
        for j in range(lo, i + 1):
            M[i][j] = 0.0
    return M
```

Một tham số  `window`- Vì `window >= n`, bạn phục hồi sự chú ý nguyên nhân đầy đủ.`window = 1`, mỗi token chỉ phục vụ cho chính mình.

> Một số liệu`window``window >= n`时, phục hồi cho toàn因果注意力.`window = 1`时, mỗi token chỉ quan tâm đến bản thân mình.

### Bước 3: mặt nạ nhỏ bé địa phương + bước

```python
def strided_mask(n, window, stride):
    M = [[float("-inf")] * n for _ in range(n)]
    for i in range(n):
        lo = max(0, i - window + 1)
        for j in range(lo, i + 1):
            M[i][j] = 0.0
        for j in range(0, i + 1, stride):
            M[i][j] = 0.0
    return M
```

Chiếc cửa sổ địa phương dày đặc cộng với mọi thứ`stride`-th token trở lại vào đầu chuỗi. trường nhận phát triển trong log bước với thêm lớp.

> Chiếc cửa sổ của bộ phận mật độ tăng lên từ chuỗi mở đầu mỗi phần`stride`个 token── cảm giác 野随层数以对数步长增长──

### Bước 4: sự chú ý khác biệt

```python
def diff_attention(Q1, K1, Q2, K2, V, lam):
    A1 = softmax_causal(Q1 @ K1.T / sqrt_d)
    A2 = softmax_causal(Q2 @ K2.T / sqrt_d)
    return (A1 - lam * A2) @ V
```

Trong mã, chúng tôi so sánh bản đồ nhiệt độ tập trung-thấm của đơn so với phân biệt và xem bộ rửa sáp sụp đổ.

> 两次注意力计算, sử dụng các hệ số hỗn hợp được học để giảm. Trong mã, chúng ta so sánh tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung

### Bước 5: KV cache kích thước

Bác kích thước cache trên mỗi lớp ở `N = 131072`cho mỗi biến thể. SWA và biến thể hiếm giảm 10100x. Differential đôi. Biết toán bộ nhớ của bạn một cách ý thức.

> 打印 `N = 131072`Khi mỗi biến thể của mỗi tầng lưu trữ lớn. SWA và biến thể hiếm giảm 10-100 lần.

## Hãy sử dụng nó để thực hiện

Các mô hình sản xuất năm 2026:

> 2026 năm sản xuất mô hình:

```python
from transformers import AutoModelForCausalLM
# Gemma 3 mixes SWA (window=1024) and global layers at 5:1.
model = AutoModelForCausalLM.from_pretrained("google/gemma-3-27b-it")
# print(model.config.sliding_window, model.config.layer_types)
```

FlexAttention trong PyTorch 2.5+ chấp nhận chức năng mặt nạ:

> PyTorch 2.5+ 中的 FlexAttention  chấp nhận ẩn码 hàm:

```python
from torch.nn.attention.flex_attention import flex_attention, create_block_mask

def swa_pattern(b, h, q_idx, kv_idx):
    return (q_idx - kv_idx < 1024) & (q_idx >= kv_idx)

mask = create_block_mask(swa_pattern, B=batch, H=heads, Q_LEN=n, KV_LEN=n)
out = flex_attention(q, k, v, block_mask=mask)
```

Điều này biên soạn thành một hạt nhân Triton tùy chỉnh. Trong 10% tốc độ FlashAttention-3 cho các mẫu phổ biến, và chức năng mặt nạ là một Python có thể gọi.

> Đây sẽ được dịch thành tự định nghĩa Triton 内核. Đối với mô hình thường, tốc độ là 10% trong FlashAttention-3, và hàm ẩn là một đối tượng có thể điều chỉnh Python.

**When to pick each:**

> **何时选择每种变体：**

- **Pure full attention** mỗi lớp lên đến ~ 16K ngữ cảnh, hoặc khi chất lượng thu hồi là tối ưu.
  Trung ngữ翻译:**纯全注意力** Mỗi tầng đều sử dụng đến khoảng 16K trên văn bản dưới đây, hoặc kiểm tra chất lượng quan trọng cảnh.
- **SWA + global mix** ngữ cảnh dài (> 32K), tập luyện và suy luận có liên quan đến bộ nhớ.
  Trung ngữ翻译:**SWA + 全局混合** 长上下文(>32K), đào tạo và suy nghĩ được ghi nhớ约束──32K trên của 2026 năm默认配置──
- **Sparse block attention** hạt nhân tùy chỉnh, mô hình tùy chỉnh. Được dành riêng cho tải trọng công việc chuyên dụng (khám, âm thanh).
  Trung ngữ翻译:**稀疏块注意力** 自定义内核,自定义模式──专用于特殊工作负载(检索、音频)──
- **Differential attention** bất kỳ khối lượng công việc nào mà sự ô nhiễm nước lặn tập trung gây đau (RAG trong bối cảnh dài, kim trong đống cỏ).
  Trung ngữ翻译:**差分注意力** 注意力汇聚污染有害的任何工作负载(长上下文 RAG、针-in-haystack)

## Chuyển nó đi.

Nhìn xem`outputs/skill-attention-variant-picker.md`. Khả năng chọn một topology chú ý cho một mô hình mới do chiều dài bối cảnh mục tiêu, yêu cầu thu hồi và hồ sơ tính toán đào tạo / suy luận.

> 参见 `outputs/skill-attention-variant-picker.md` Kỹ năng này 根据目标上下文长度,检查需求和训练/推理计算配置,为新模型选择注意力拓──

## Tập luyện bài tập

1. **Easy.**Đi chạy`code/main.py`- Kiểm tra SWA tại `window=4`- Đánh giá tất cả ngoài 4 token cuối cùng mỗi hàng.`window=n`tái tạo sự chú ý nguyên nhân đầy đủ theo bit-tương tự.
   Trung ngữ翻译:运行 `code/main.py`❖ 验证`window=4`SWA sẽ đặt tất cả nội dung bên ngoài 4 token cuối cùng mỗi lần.`window=n`能逐位复现全因果注意力──
2. **Medium.**Thực hiện SWA nguyên nhân với `window=1024`Đọc 1000 bước trên Tinyshakespeare, giảm giá trị giảm giá bằng cách giảm sự chú ý?
   Trung文翻译: 实现在第07课毕业项目 上`window=1024`Trong một cuộc tập luyện nhỏ, tập luyện 1.000 bước.
3. **Hard.**Thực hiện một hỗn hợp lớp 5:1 kiểu Gemma-3 (5 SWA, 1 toàn cầu) trong mô hình đá cuối. So sánh chất lượng mất mát, bộ nhớ và sản xuất so với đường cơ sở SWA thuần khiết và đường cơ sở toàn cầu thuần khiết ở các tham số phù hợp.
   Trong mô hình dự án毕业实现类 Gemma-3 của 5:1 层混合 ((5 层 SWA、1 层全局) ⋅ 在匹配参数下与纯SWA 和纯全局基线比较损失、内存和生成质量。
4. **Hard.**Thực hiện sự chú ý khác biệt với một người học `λ`mỗi người. đào tạo về một nhiệm vụ lấy lại tổng hợp (một kim, 2.000 máy phân tâm). đo độ chính xác lấy lại so với một đường cơ sở chú ý duy nhất ở các tham số phù hợp.
   Trung ngữ翻译:实现每个头有学习 `λ`Sự khác biệt về độ tập trung. Trong nhiệm vụ kiểm tra tổng hợp (một con nồi, 2.000 个干扰项) tập luyện.

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Sliding window attention (SWA) | "Local attention" | Each query attends to its last `W` tokens; KV cache shrinks to `O(W)`. |
| 滑动窗口注意力 (SWA) | "局部注意力" | 每个查询关注其最后 `W` 个 token；KV 缓存缩小到 `O(W)`。 |
| Effective receptive field | "How far back the model sees" | In an `L`-layer SWA stack with window `W`, up to `L × W` tokens. |
| 有效感受野 | "模型能看多远" | 在 `L` 层 SWA 堆栈中，窗口 `W`，最多 `L × W` 个 token。 |
| Longformer / BigBird | "Local + global + random" | Sparse patterns with a few always-attending global tokens; early long-context approach. |
| Longformer / BigBird | "局部+全局+随机" | 带少量始终关注的全局 token 的稀疏模式；早期长上下文方案。 |
| Native Sparse Attention | "DeepSeek's kernel trick" | Learn block-level sparsity; skip zero blocks at the kernel level while keeping quality. |
| 原生稀疏注意力 | "DeepSeek 的内核技巧" | 学习块级稀疏性；在内核级别跳过零块同时保持质量。 |
| Differential attention | "Two maps, one subtracts" | DIFF Transformer: subtract a learned `λ` times a second attention map from the first to cancel attention sinks. |
| 差分注意力 | "两个图，一个相减" | DIFF Transformer：用第一个注意力图减去学习 `λ` 倍的第二个注意力图，消除注意力汇聚。 |
| Attention sink | "Weight bleeds to token 0" | Softmax normalization forces rows to sum to 1; uninformative queries dump weight on position 0. |
| 注意力汇聚 | "权重流向 token 0" | Softmax 归一化迫使每行总和为 1；无信息查询将权重倾倒到位置 0。 |
| FlexAttention | "Mask-as-Python" | PyTorch 2.5+ API that compiles arbitrary mask functions into FlashAttention-shape kernels. |
| FlexAttention | "掩码即 Python" | PyTorch 2.5+ API，将任意掩码函数编译为 FlashAttention 形式的内核。 |
| Layer type mix | "5:1 SWA-to-global" | Interleave sparse and full attention layers in a stack to keep quality at lower memory. |
| 层类型混合 | "5:1 SWA 与全局" | 在堆栈中交替使用稀疏和全注意力层，以较低内存保持质量。 |

## Xem thêm 延伸阅读

- [Beltagy, Peters, Cohan (2020). Longformer: The Long-Document Transformer](https://arxiv.org/abs/2004.05150) giấy cửa sổ trượt theo quy luật + giấy mã thông báo toàn cầu.
  Trung ngữ翻译:Longformer 论文,经典的滑动窗口 + 全局代号方案──
- [Zaheer et al. (2020). Big Bird: Transformers for Longer Sequences](https://arxiv.org/abs/2007.14062) địa phương + toàn cầu + ngẫu nhiên.
  Trung ngữ翻译:BigBird 论文,局部 + 全局 + 随机模式。
- [Child et al. (2019). Generating Long Sequences with Sparse Transformers](https://arxiv.org/abs/1904.10509) Mô hình địa phương + bước của OpenAI.
  Trung ngữ翻译:OpenAI 稀疏 Transformer 论文,局部+步进模式。
- [Gemma Team (2024). Gemma 2: Improving Open Language Models at a Practical Size](https://arxiv.org/abs/2408.00118) sự pha trộn 1:1 SWA: toàn cầu.
  中文翻译:Gemma 2 论文,1:1 SWA 与全局混合──
- [Gemma Team (2025). Gemma 3 technical report](https://arxiv.org/abs/2503.19786) sự kết hợp 5:1 với window=1024 đó là sách giáo khoa mặc định.
  Trung văn翻译:Gemma 3 技术报告,5:1 混合,窗口=1024,现已成为教科书默认。
- [Ye et al. (2024). Differential Transformer](https://arxiv.org/abs/2410.05258) Bảng biến đổi DIFF.
  Trung文翻译:DIFF Transformer 论文。
- [Yuan et al. (2025). Native Sparse Attention](https://arxiv.org/abs/2502.11089) Sự chú ý về sự thâm hụt của DeepSeek-V3.2
  Trung ngữ翻译:DeepSeek-V3.2 的原生稀疏注意力论文──
- [PyTorch — FlexAttention blog and docs](https://pytorch.org/blog/flexattention/) Khán giả API cho mô hình mặt nạ như có thể gọi trong Use It.
  Trung文翻译:PyTorch FlexAttention 文档,掩码即可调用模式的 API 参考──
