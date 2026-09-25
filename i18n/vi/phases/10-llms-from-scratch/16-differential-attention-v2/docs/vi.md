# Sự khác biệt chú ý (V2) 差分注意力 (V2)

> Sự chú ý Softmax phân tán một số lượng nhỏ xác suất trên mỗi token không phù hợp. Hơn 100k token mà tiếng ồn cộng lên và nhấn chìm tín hiệu. Differential Transformer (Ye et al., ICLR 2025) sửa chữa nó bằng cách tính toán sự chú ý như là sự khác biệt của hai softmax, trừ được sàn tiếng ồn chung. DIFF V2 (Microsoft, tháng 1 năm 2026) là bản viết lại sản xuất: phù hợp với độ trễ giải mã với Transformer dòng cơ sở, không có lõi tùy chỉnh, tương thích với FlashAttention. Bài học này là từ đầu đến cuối V1, với một trò chơi thực hiện của hoạt động khác biệt bạn có thể chạy trong stdlib Python.

> **【中文解读】**Softmax chú ý đến mỗi token không phù hợp phân chia tỷ lệ có thể xảy ra, trong dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng dòng

> **【拓展：长上下文优化】**Sự chú ý phân biệt là một trong những hướng quan trọng trong việc tối ưu hóa LLM. Trong cửa sổ trên của 100K + token, vấn đề "tránh chú ý hiếm" của tiêu chuẩn chú ý ngày càng nghiêm trọng, sự chú ý phân biệt cung cấp một giải pháp không hy sinh tốc độ.

>  **【前置】**Học本节前请先掌握:Phase 07·01-05(Self-Attention 基础);softmax 函数。本节是注意力变体之一,对应Phase 07·15。
>  **【类比】**标准 Softmax = 大合唱里听不清独唱;; tiếng ồn từ tất cả các hướng truyền đến) 差分注意力 = 双耳降噪耳机两个麦克风(两个软max) 录录相同声音,相减消掉背景噪音(共享噪音基底),独唱清晰浮现;;对长上下文特别有效:100K token 时背景"声"被消除──

**Type:** Build
**Languages:** Python (stdlib)
**Prerequisites:** Phase 7 · 02 (self-attention), Phase 7 · 15 (attention variants), Phase 10 · 14 (architecture walkthrough)
**Time:** ~60 minutes

## Mục tiêu học tập

- Hãy nói chính xác tại sao sự chú ý softmax có một sàn tiếng ồn và tại sao nó tăng lên theo chiều dài của ngữ cảnh.
   Cần xác định softmax chú ý tại sao có âm thanh, và tại sao nó tăng theo chiều dài của văn bản
- Thuộc dẫn công thức chú ý khác biệt và giải thích tại sao việc trừ hủy thành phần tiếng ồn chung trong khi bảo tồn tín hiệu.
  推导差分注意力公式, giải thích tại sao giảm法 có thể loại bỏ chia sẻ âm thanh và giữ lại tín hiệu
- Đi theo sự khác biệt V1-V2: những gì trở nên nhanh hơn, những gì trở nên đơn giản hơn, những gì trở nên ổn định hơn, và tại sao mỗi thay đổi là cần thiết cho việc đào tạo trước sản xuất.
  Sự khác biệt giữa V1 và V2: những gì đã thay đổi nhanh chóng, đơn giản hóa, ổn định, và tại sao mỗi sửa đổi cho đào tạo dự kiến sản xuất là cần thiết
- Thực hiện sự chú ý khác biệt từ đầu trong Python tinh khiết và xác minh bằng chứng về tính chất hủy tiếng ồn trên một truy vấn tín hiệu cộng tiếng ồn tổng hợp.
  Sử dụng Python tinh khiết từ không thực hiện sự phân biệt sự chú ý, trong việc thử nghiệm các tính năng loại bỏ tiếng ồn trên các tín hiệu tổng hợp

## Vấn đề  vấn đề giới thiệu

Sự chú ý softmax tiêu chuẩn có tính chất toán học biến thành một cơn đau đầu hoạt động trên quy mô.`q`, trọng lượng chú ý là `softmax(qK^T / sqrt(d))`. Softmax không bao giờ có thể tạo ra những con số không chính xác  mỗi token không phù hợp có một số khối lượng tích cực. khối lượng dư thừa đó là tiếng ồn, và nó cân bằng với chiều dài ngữ cảnh. Tại các token 128k, ngay cả khi mỗi token không phù hợp chỉ có 0,001% xác suất, 127.999 trong số chúng kết hợp đóng góp khoảng 12% tổng cộng. Mô hình phải học cách định tuyến xung quanh một tầng tiếng ồn phát triển với ngữ cảnh.

> 标准 softmax chú ý có một đặc tính toán học, trên quy mô trở thành một cái đầu trên hoạt động.`q`, chú ý quyền trọng là `softmax(qK^T / sqrt(d))`❖ Softmax 永远不能产生精确零 每个不匹配的代币都获得了一些正质量──那个残余质量是噪音,并且随着下文长度增加── 在128k代币时,即使每一个不匹配的代币只获得0.001%的概率,127,999代币加起来贡献了约12%.

Về cơ bản, điều này xuất hiện như sự can thiệp của đầu chú ý: các trích dẫn ảo giác trong RAG trong bối cảnh dài, thất bại trong giữa trong các nhiệm vụ lấy lại 100k token, và sự suy giảm độ chính xác tinh tế trên các tiêu chuẩn kim cương trong đống cỏ sau 32k. Bức giấy biến đổi khác biệt (arXiv:2410.05258, ICLR 2025) đo khoảng cách: DIFF Transformers đạt độ bối rối thấp hơn, độ chính xác ngữ cảnh dài cao hơn và ít ảo giác hơn so với các đường cơ sở cùng kích thước.

> Trong kinh nghiệm, biểu hiện này là sự cố trong quá trình nghiên cứu của các công cụ phân tích và phân tích của các công cụ phân tích và phân tích.

DIFF V1 có ba vấn đề khiến nó không được đi đường ống dẫn trước khi đào tạo biên giới. Kho lưu trữ giá trị của nó phải được tải hai lần mỗi bước giải mã, nó yêu cầu các lõi CUDA tùy chỉnh phá vỡ khả năng tương thích FlashAttention, và đầu RMSNorm của nó gây mất ổn định đào tạo dài ở quy mô 70B-plus. DIFF V2 (blog Microsoft unilm, 20 tháng 1 năm 2026) đã sửa chữa cả ba. Bài học này đi bộ cả hai phiên bản, xây dựng trình điều khiển khác biệt, và đánh giá hủy tiếng ồn trên câu hỏi đồ chơi.

## Khái niệm cốt lõi

> **【中文解读】**差分注意力 (trong phương pháp phân biệt sự chú ý) bằng cách tính toán hai giá trị khác biệt của softmax độc lập để loại bỏ tiếng ồn tập trung, để mô hình tập trung nhiều hơn vào thông tin liên quan thực sự.

> **【拓展：注意力机制的演进】**Từ tiêu chuẩn Multi-Head Attention → GQA(分组查询注意力,Llama 2/3 使用)→ MLA(多头潜在注意力,DeepSeek-V2/V3 使用,将KV-cache 压缩到低维潜在空间)→差分注意力──MLA将DeepSeek-V3的KV-cache 压缩约10倍,是推理效率的关键创新──


### Lầu tiếng ồn của softmax

Để hỏi `q`và chìa khóa`K = [k_1, ..., k_N]`, trọng lượng chú ý là:

```
w_i = exp(q . k_i / sqrt(d)) / sum_j exp(q . k_j / sqrt(d))
```

Không .`w_i`là không.`k_i`hoàn toàn không liên quan đến `q`, điểm số `q . k_i`không phải là 0  nó dao động xung quanh 0 với sự biến động `||q||^2 / d`Sau khi softmax bình thường hóa, mỗi token không liên quan vẫn đóng góp.`O(1/N)`Tổng đóng góp của các token không liên quan là `O((N-1)/N) = O(1)`Không phải một lượng nhỏ.

Những gì mô hình muốn là một cái gì đó giống như một top-k cứng: trọng lượng cao trên các token phù hợp, trọng lượng gần bằng không ở mọi nơi khác. Softmax quá mịn để làm điều đó trực tiếp.

### Ý tưởng khác biệt

Chia các dự đoán Q và K của mỗi đầu thành hai: Q = (Q_1, Q_2) và K = (K_1, K_2).

```
A_1 = softmax(Q_1 K_1^T / sqrt(d))
A_2 = softmax(Q_2 K_2^T / sqrt(d))
```

Tạo ra:

```
DiffAttn = (A_1 - lambda * A_2) V
```

Việc trừ bỏ bất kỳ phân phối tiếng ồn nào mà hai bản đồ chia sẻ. Nếu cả hai bản đồ có trọng lượng tương tự trên các token không liên quan 127k (mà họ sẽ, khi khởi đầu ngẫu nhiên), thì chúng sẽ hủy bỏ. tín hiệu  trọng lượng đỉnh trên vài token thực sự liên quan  chỉ hủy bỏ nếu nó xuất hiện trong cả hai bản đồ với cùng một cường độ, điều mà nó sẽ không làm khi mô hình được đào tạo.

`lambda`là một tính toán có thể học được cho mỗi người, được định nghĩa như `lambda = exp(lambda_q1 dot lambda_k1) - exp(lambda_q2 dot lambda_k2) + lambda_init`Nó có thể tiêu cực.`lambda_init`mặc định để một số tích cực nhỏ như 0.8.

### Tại sao điều này phù hợp với đầu phím tiếng ồn

Hãy nghĩ đến hai chiếc microphone ồn ào ghi lại cùng một giọng nói. Cả hai đều lấy loa cộng với tiếng ồn nền tương quan. Khi trừ một từ nhau thì tiếng ồn chia sẻ sẽ giảm đi.`lambda`học được sự cân bằng này.

### V1 vs V2: sự khác biệt

V1 giữ số lượng tham số bằng với đường dẫn cơ bản Transformer. Để có được hai truy vấn mỗi đầu nó làm giảm một nửa chiều kích đầu. Điều đó chi phí đầu biểu hiện và  hơn đau đớn  giảm một nửa giá trị cache mỗi đầu. Decode phải tải giá trị cache hai lần mỗi bước (một lần mỗi chi nhánh softmax). Kết quả: decode chậm hơn đường dẫn cơ bản mặc dù số lượng tham số phù hợp.

V2 tăng gấp đôi số đầu truy vấn và giữ cho các đầu KV tương tự (mượn các tham số từ dự đoán lên). chiều kích đầu vẫn giống như đường cơ sở. Sau khi trừ, chiều kích bổ sung được dự đoán xuống để phù hợp với dự đoán O_W của đường cơ sở Transformer. Ba điều xảy ra cùng một lúc:

1. Tốc độ giải mã phù hợp với đường cơ sở (KV cache được tải một lần).
2. FlashAttention chạy không thay đổi (không có lõi tùy chỉnh).
3. Tăng cường toán học khi giải mã tăng lên (cần tính toán nhiều hơn cho mỗi byte tải từ HBM).

V2 cũng loại bỏ RMSNorm mỗi đầu mà V1 sử dụng để ổn định việc trừ. Ở thang trước đào tạo lớp 70B, RMSNorm gây bất ổn cho đào tạo muộn. V2 thay thế nó bằng một kế hoạch khởi tạo đơn giản hơn giúp đào tạo ổn định mà không cần mô-đun bổ sung.

### Khi nào để đạt được nó

| Workload | Benefit |
|----------|---------|
| Long-context RAG (64k+) | Cleaner attention maps, fewer hallucinated citations |
| Needle-in-haystack benchmarks | Substantial accuracy lift past 32k |
| Multi-document QA | Less cross-document interference |
| Code completion at 8k | Marginal, not worth the architecture change |
| Short chat (< 4k) | Essentially indistinguishable from baseline |

Giá trị tăng lên theo chiều dài ngữ cảnh. ở 4k token sàn tiếng ồn đủ nhỏ để sự chú ý tiêu chuẩn là tốt. ở 128k nó làm tổn thương bạn.

### Làm thế nào nó xếp chồng với các nút 2026 khác

| Feature | Compatible with DIFF V2? |
|---------|------------------------|
| GQA | Yes (V2 increases Q heads, not KV heads) |
| MLA (DeepSeek) | Yes in principle, no published paper combining them |
| MoE | Yes (attention is independent of MLP block) |
| RoPE | Yes (unchanged) |
| YaRN / long-context scaling | Yes (exactly where DIFF helps most) |
| FlashAttention | Yes in V2 (was no in V1) |
| Speculative decoding | Yes (attention change is invisible to the spec-decode loop) |


> **【拓展：注意力机制的关键创新时间线】**2017 年 đa đầu chú ý đến năm 2022 GQA(Llama 2, giảm KV-cache) đến năm 2024 MLA(DeepSeek-V2,KV ưng cục đến tiềm năng không gian) đến năm 2024 年  Differential Attention(Eliminate attention noise)。MLA sẽ giảm KV-cache 缩小约10倍。


## Hãy xây dựng nó.
```figure
differential-attention
```

## Hãy xây dựng nó

`code/main.py`thực hiện sự chú ý khác biệt trong Python tinh khiết. Một truy vấn đồ chơi với cấu trúc tín hiệu cộng tiếng ồn được biết cho phép bạn đo tỷ lệ hủy tiếng ồn trực tiếp.

### Bước 1: sự chú ý softmax tiêu chuẩn

Stdlib matrix ops: danh sách danh sách, matmul thủ công, softmax với số ổn định trừ tối đa.

```python
def softmax(row):
    m = max(row)
    exps = [math.exp(x - m) for x in row]
    s = sum(exps)
    return [e / s for e in exps]
```

### Bước 2: Chia Q, K thành hai nửa

Thiết kế V1: giảm một nửa chiều kích đầu. Thiết kế V2: giữ chiều kích đầu và tăng gấp đôi số đầu. Việc thực hiện đồ chơi sử dụng V1 để làm rõ hơn về giáo dục.

### Bước 3: hai nhánh softmax + trừ

```python
A1 = [softmax([dot(q1, k) / scale for k in K1]) for q1 in Q1]
A2 = [softmax([dot(q2, k) / scale for k in K2]) for q2 in Q2]
diff_weights = [[a1 - lam * a2 for a1, a2 in zip(r1, r2)] for r1, r2 in zip(A1, A2)]
out = [[sum(w * v[j] for w, v in zip(row, V)) for j in range(d_v)] for row in diff_weights]
```

Lưu ý: trọng lượng đầu ra có thể âm. Điều đó tốt  bộ nhớ cache giá trị vẫn xử lý các đóng góp ký kết. Dự án V tiếp theo hấp thụ dấu hiệu.

### Bước 4: đo lường hủy tiếng ồn

Xây dựng một chuỗi tổng hợp dài 1024. Đặt tín hiệu ở một vị trí được biết, và lấp đầy phần còn lại với tiếng ồn. Xét (a) trọng lượng chú ý softmax tiêu chuẩn trên vị trí tín hiệu và (b) trọng lượng chú ý khác biệt. Đánh giá tỷ lệ tín hiệu/ruốt trong mỗi. DIFF chú ý có thể được tin cậy tạo ra một tỷ lệ tín hiệu-xồn cao hơn bằng một nhân tố 3x-10x tùy thuộc vào mức độ hai nhánh đã được đào tạo để khác nhau.

### Bước 5: V1 vs V2 tính toán các tham số

Với một cấu hình (họp=4096, đầu=32, d_head=128), in:

- Bộ biến đổi đường cơ bản: Q, K, V mỗi kích thước `hidden * hidden`, MLP ở 4 * ẩn.
- DIFF V1: Q, K mỗi kích thước `hidden * hidden`, kích thước V `hidden * hidden`(không thay đổi), đầu mờ đi một nửa bên trong.`lambda`Các tham số (O(head * d_head)).
- DIFF V2: kích thước Q `2 * hidden * hidden`, K kích thước `hidden * hidden`, kích thước V `hidden * hidden`. Tâm tối hơn dự kiến xuống trước O_W. Thêm tương tự `lambda`Các tham số.

Trò chơi đo chi phí phụ tham số cho V2 (khoảng `hidden * hidden`thêm mỗi khối chú ý) và in nó.

## Hãy sử dụng nó để thực hiện

DIFF V2 chưa được chuyển giao trên tất cả các máy chủ suy luận sản xuất vào tháng 4 năm 2026, nhưng tích hợp đang được tiến hành trong vLLM và SGLang. Trong khi đó mô hình xuất hiện trong:

- Mô hình sản xuất nội bộ của Microsoft trong bối cảnh dài.
- Các bản sao nghiên cứu trong một số khóa đào tạo mô hình mở nhắm mục tiêu vào hơn 256k ngữ cảnh.
- Thiết kế lai kết hợp sự chú ý DIFF với sự chú ý cửa sổ trượt trên các lớp thay thế.

Khi bạn đạt được điều này vào năm 2026:

- Căn luyện một mô hình mới từ đầu nhắm mục tiêu vào bối cảnh hiệu quả hơn 64k.
- Hoạt động tinh chỉnh mô hình ngữ cảnh dài nơi thất bại bị mất ở giữa thống trị đánh giá của bạn.

Khi anh không muốn:

- Bạn đang phục vụ một mô hình dày đặc được đào tạo trước với hiệu suất ổn định trong bối cảnh dài.
- Mối quan hệ của anh luôn dưới 16k.

## Chuyển nó đi.

Bài học này sẽ mang lại kết quả `outputs/skill-diff-attention-integrator.md`Với kiến trúc mô hình, chiều dài nội dung mục tiêu, hồ sơ ảo giác và ngân sách đào tạo, nó tạo ra một kế hoạch tích hợp để thêm sự chú ý khác biệt vào một cuộc chạy trước đào tạo mới hoặc điều chỉnh tinh tế LoRA.

> 本课产 出 `outputs/skill-diff-attention-integrator.md` Được định cấu trúc mô hình, mục tiêu, quy mô, cấu trúc và ngân sách đào tạo, nó sẽ tạo ra sự phân biệt sự tập trung vào các hoạt động đào tạo mới hoặc các kế hoạch tập trung LoRA 微调.

## Tập luyện bài tập

1. Đi chạy`code/main.py`- Kiểm tra tỷ lệ tín hiệu-xồn được báo cáo cho sự chú ý khác biệt cao hơn so với sự chú ý softmax tiêu chuẩn trên truy vấn tổng hợp.
   Trung ngữ翻译:运行 `code/main.py` Phân tích phân biệt độ chú ý của báo cáo ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ 

2. Xét số lượng tham số-đánh giá từ đường cơ sở đến DIFF V1 và từ đường cơ sở đến DIFF V2 cho mô hình lớp 7B (họp=4096, đầu=32, d_head=128, 32 lớp).
   Trung文翻译:计算 7B 级模型(họ = 4096,heads = 32,d_head = 128,32 层) từ基线 đến DIFF V1 和 từ基线 đến DIFF V2 của参数差异──展示哪些组件增加参数,哪些保持不变──

3. Đọc Phần 3 của bài báo DIFF V1 (arXiv:2410.05258) và Phần 2 của blog DIFF V2 Hugging Face. Trong hai câu, giải thích tại sao V1 trên đầu RMSNorm là cần thiết và tại sao V2 có thể loại bỏ nó mà không gây ra sự khác biệt trong đào tạo.
   Trung ngữ翻译:阅读DIFF V1 论文第3节和DIFF V2 Hugging Face 博客第2节──用两句解释为什么V1的逐头 RMSNorm是必要的,以及为什么V2可以在不导致训练发散的情况下移除它──

4. Thực hiện một việc phân tích: tính toán sự chú ý khác biệt với `lambda = 0`(đối đa mềm đầu tiên) và `lambda = 1`(trừ trừ đầy đủ). Trong truy vấn tổng hợp, đo lường cách tín hiệu-đại tiếng ồn thay đổi qua các quét.`lambda`tối đa hóa tín hiệu đến tiếng ồn.
   Trung ngữ翻译:实现消融实验:用 `lambda = 0`(Tất cả) và`lambda = 1`(Tổng giảm法) tính toán phân biệt chú ý.`lambda`

5. Lớn toy đến GQA + DIFF V2. chọn 8 đầu KV và 32 đầu Q. Cho thấy kích thước bộ nhớ cache KV phù hợp với mô hình GQA cơ bản với cấu hình tương tự (8, 32).
   Trung文翻译:将玩具模型扩展到 GQA + DIFF V2──选择 8 个 KV 头和 32 个 Q 头──展示 KV 缓存大小与相同 (8, 32) 配置的基线 GQA 模型匹配──

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|------------------------|---------|
| Differential attention | "Two softmaxes minus each other" | Split Q, K into two halves, compute two softmax maps, subtract the second (scaled by lambda) from the first, then multiply by V | 差分注意力，两个 softmax 相减消除噪声 |
| Noise floor | "The non-zero tail of softmax" | The O(1/N) weight softmax puts on every unrelated token, which sums to O(1) across long contexts | 噪声基底，softmax 对不相关 token 的非零权重 |
| lambda | "The subtraction scale" | Per-head learnable scalar parameterized as `exp(lq1.lk1) - exp(lq2.lk2) + lambda_init`; can be negative | lambda 参数，可学习的减法缩放标量 |
| DIFF V1 | "The ICLR 2025 version" | Original Differential Transformer; halves head dim to preserve parameter count, needs custom kernel, slower decode | DIFF V1，原始差分 Transformer，需要自定义核 |
| DIFF V2 | "The January 2026 fix" | Doubles Q heads keeping KV heads; matches baseline decode speed and works with FlashAttention | DIFF V2，双倍 Q 头保持 KV 头，兼容 FlashAttention |
| Per-head RMSNorm | "The V1 stabilizer" | Extra norm V1 applied after the difference; V2 removed it to prevent late-training instability | 逐头 RMSNorm，V1 的稳定器，V2 移除 |
| Signal-to-noise ratio | "How much attention is wasted" | Ratio of weight on the true signal position to average weight on unrelated positions | 信噪比，信号位置权重与不相关位置平均权重之比 |
| Lost in the middle | "Long-context failure mode" | Empirical phenomenon where retrieval accuracy dips for documents in the middle of a long context — DIFF attention reduces this | 中间丢失现象，长上下文中间文档检索准确率下降 |
| Arithmetic intensity | "FLOPs per byte loaded" | Ratio V2 increased at decode by doubling queries per KV load; important for memory-bound decode | 算术强度，每次字节加载的 FLOPs 比 |

## Xem thêm 延伸阅读

- [Ye et al. — Differential Transformer (arXiv:2410.05258, ICLR 2025)](https://arxiv.org/abs/2410.05258) bài bản gốc với lý thuyết hủy tiếng ồn và các đoạn văn dài
- [Microsoft unilm — Differential Transformer V2 (Hugging Face blog, January 2026)](https://huggingface.co/blog/microsoft/diff-attn-v2) bản viết lại sản xuất, mã hóa đường cơ sở phù hợp, tương thích với FlashAttention
- [Understanding Differential Transformer Unchains Pretrained Self-Attentions (arXiv:2505.16333)](https://arxiv.org/abs/2505.16333) Phân tích lý thuyết về lý do tại sao việc trừ lại cấu trúc chú ý trước khi được đào tạo
- [Shared DIFF Transformer (arXiv:2501.17900)](https://arxiv.org/html/2501.17900) Phân biến chia sẻ tham số
- [Vaswani et al. — Attention Is All You Need (arXiv:1706.03762)](https://arxiv.org/abs/1706.03762) dòng cơ sở DIFF biến đổi trừ từ
- [Liu et al. — Lost in the Middle (arXiv:2307.03172)](https://arxiv.org/abs/2307.03172) tiêu chuẩn dài hạn của mục tiêu chú ý của DIFF
