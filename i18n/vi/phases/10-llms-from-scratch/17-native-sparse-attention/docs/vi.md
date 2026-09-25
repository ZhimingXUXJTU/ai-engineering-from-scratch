# Native Sparse Attention (Dân sâu tìm NSA)

> Với 64k token, sự chú ý tiêu thụ 70-80% thời gian trễ giải mã. Mỗi phòng thí nghiệm mở có kế hoạch sửa chữa nó. NSA của DeepSeek (ACL 2025 bài báo tốt nhất) là một trong những gì bị mắc kẹt: ba chi nhánh chú ý song song  token hạt thô bị nén, token hạt mỏng được giữ lại một cách chọn lọc, và cửa sổ trượt cho bối cảnh địa phương  kết hợp thông qua một cổng học. Nó được sắp xếp theo phần cứng (tương tự với lõi), có thể đào tạo bản địa (công việc trong đào tạo trước, không được khóa vào khi suy luận), và trên 64k decodes nó chạy nhanh hơn FlashAttention trong khi phù hợp hoặc đánh bại chất lượng chú ý đầy đủ. Bài học này xây dựng ba nhánh đầu đến cuối và cho thấy tại sao sự ít có thể phân biệt được đầu đến cuối.

> **【中文解读】**64K token 时注意力消耗 70-80%解码延迟──DeepSeek NSA(ACL 2025 最佳论文) sử dụng 3条并行注意力分支解决: 压缩粗粒度 token、选择保留细粒度 token、滑窗局部上下文,通过可学习门控组合──硬件友好、可预训、比FlashAttention更快──

> **【拓展：稀疏注意力→长上下文】**长上下文(64K-128K token) là năng lực cốt lõi của mô hình lớn năm 2025-2026;; NSA, MHA, GQA đều là một giải pháp giảm tính toán phức tạp của sự chú ý;; Đổi mới của DeepSeek là về sự hiếm có có thể phân biệt từ đầu đến cuối, có thể được sử dụng trực tiếp trong giai đoạn đào tạo trước.

>  **【前置】**Học本节前请先掌握:Phase 10·16(差分注意力);FlashAttention 概念;softmax 门控机制。本节是注意力优化进阶。
>  **【类比】**NSA = 看长文档的三种策略同时进行:**压缩分支**= 看目录摘要(粗粒度);(2) **选择分支**= 重点看自己感兴趣的章节(细粒度);(3) **滑动窗口**= 当前页前后 5页仔细看(局部上下文) ――门控(gate) = quyết định mỗi vị trí nên sử dụng chiến lược nào, tự động học tập kết hợp tốt nhất。

**Type:** Build
**Languages:** Python (stdlib)
**Prerequisites:** Phase 7 · 12 (KV cache, flash-attention), Phase 7 · 15 (attention variants), Phase 10 · 16 (differential attention)
**Time:** ~60 minutes

## Mục tiêu học tập

- Hãy nói cho tôi biết ba cơ quan quan sát của NSA và mỗi cơ quan này bắt được gì.
  Nói rõ 3 chi tiết của NSA và thông tin bắt giữ của họ
- Giải thích tại sao NSA là "đáng tạo có thể đào tạo" trong khi các phương pháp chú ý hiếm hoi trước đó chỉ là suy luận.
  Giải thích tại sao NSA là "đáng sinh có thể đào tạo", trong khi phương pháp chú ý hiếm hoi trước đó chỉ có thể được sử dụng để đưa ra lý luận.
- Xét tính tiết kiệm tính toán chú ý của NSA so với sự chú ý đầy đủ tại ngữ cảnh 64k như một chức năng của kích thước khối nén và chọn top-k.
  计算在 64K 上下文中 NSA 相对全注意的计算节省量(作为压缩块大小和选择 top-k 的函数)
- Thực hiện kết hợp ba chi nhánh trong stdlib Python trên một chuỗi tổng hợp ngắn và xác minh hành vi của các trọng lượng gating.
  Sử dụng Python trong chuỗi tổng hợp ngắn để thực hiện bộ kết hợp, kiểm chứng và kiểm soát trọng lượng

## Vấn đề  vấn đề giới thiệu

Sự chú ý đầy đủ tại chiều dài chuỗi N chi phí `O(N^2)`thời gian và`O(N)`KV cache mỗi lớp. Tại 64k token, số lượng băng thông tính toán và bộ nhớ là thảm khốc. ước tính lý thuyết được đo từ giấy NSA: sự chú ý chiếm 70-80% tổng thời gian trễ giải mã tại 64k. Mọi thứ theo dòng  TTFT, token / giây, chi phí mỗi triệu token  được chi phí chú ý thống trị.

> 序列长度 N 的全注意力成本为 `O(N^2)`Thời gian và từng tầng`O(N)`KV 缓存── trong 64k token 时,计算和显存带宽的数字是灾难性的──NSA 论文的测量理论估计:64k 时注意占总解码延迟的70-80%──所有下游指标TTFT、代币/秒、每百万代币 成本都由注意成本主导──

Sự chú ý ít là câu trả lời rõ ràng. Những nỗ lực trước đây đã bị chia thành hai cái rỗng. Sự thâm hụt của mô hình cố định (trung cửa sổ trượt, bước, khối địa phương) làm rơi thông tin và thất bại trong các nhiệm vụ nhớ tầm xa. Sự thâm hụt thời gian suy luận (KV cache pruning, H2O, StreamingLLM) được áp dụng cho một mô hình được đào tạo trước khi tập trung vào sự chú ý dày đặc và chỉ phục hồi một phần nhỏ của tốc độ tăng tốc tiềm năng vì mô hình chưa bao giờ được yêu cầu định tuyến thông tin thông qua mô hình thâm hụt.

> 稀疏注意力是显而易见的答案―― trước đây đã được phân chia thành hai loại―― cố định模式稀疏性 (nước cửa sổ trượt, bước qua, khối) bị bỏ rơi thông tin và thất bại trong nhiệm vụ nhớ dài hạn――推理时稀疏性 (KV 缓存剪枝, H2O, StreamingLLM) được sử dụng trong mô hình đào tạo tập trung tập trung, chỉ có thể phục hồi một phần nhỏ của tiềm năng tăng tốc, vì mô hình chưa bao giờ được yêu cầu thông tin thông tin thông qua đường lối模式稀疏.

Native Sparse Attention (Yuan et al., DeepSeek + PKU + UW, ACL 2025 best paper, arXiv:2502.11089) làm cả hai: một mô hình sự thâm hụt mà mô hình học được trong quá trình đào tạo trước, được thực hiện như một thuật toán liên kết với lõi thực sự cung cấp tiết kiệm tính toán khi suy luận. Hai năm nữa, NSA hoặc một hậu duệ trực tiếp là sự chú ý mặc định trên mọi mô hình ngữ cảnh dài biên giới.

> 原生稀疏注意力(Yuan 等人,DeepSeek + PKU + UW,ACL 2025 最佳论文,arXiv:2502.11089): hai quan điểm: một mô hình trong quá trình đào tạo học tập trong mô hình稀疏, thực hiện cho hệ thống hạt nhân, thực sự giao dịch trong quá trình đưa ra ý kiến về tính toán tiết kiệm.

## Khái niệm cốt lõi

> **【中文解读】**Nguyên tắc: để học tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập tập

> **【拓展：长上下文的稀疏注意力方案】**稀疏注意力工程实现包括:滑动窗口(Mistral's 32K 窗口) + 全局 token([CLS]) + 选择性关注。Google's Ring Attention 和 Block-Sparse Attention 将上下文扩展到百万 token。DeepSeek's NSA(Native Sparse Attention) 在训练时直接学习稀疏模式。


### Ba nhánh song song

Đối với mỗi truy vấn, NSA chạy sự chú ý ba lần, đối với ba lượt xem khác nhau của bộ nhớ cache KV:

1. **Compressed branch.**Các token được nhóm thành khối kích thước `l`(thường là 32 hoặc 64). Mỗi khối được nén thành một token tóm tắt duy nhất thông qua một MLP học được nhỏ.

2. **Selected branch.**Sử dụng điểm chú ý từ chi nhánh nén, các khối top-k phù hợp nhất với truy vấn hiện tại được xác định. Các token hạt mỏng (không nén) từ các khối đó được đọc và truy vấn được xem trên tất cả chúng. Hãy nghĩ về sự chú ý của chi nhánh nén như là tín hiệu định tuyến cho sự lựa chọn.

3. **Sliding-window branch.**Câu hỏi này được trả lời cho các câu hỏi gần đây nhất `W`Các mã thông báo (thường là 512) cho bối cảnh địa phương. Chi nhánh này nắm bắt các mô hình tầm ngắn nặng cấu trúc (tế ngôn, coreference địa phương) mà hai người khác có thể bỏ lỡ.

Ba đầu ra của nhánh được kết hợp qua một cổng học được học theo vị trí:

```
out = g_cmp * out_cmp + g_sel * out_sel + g_win * out_win
```

`g_cmp, g_sel, g_win`là trọng lượng cổng từ một MLP nhỏ trên truy vấn. Họ không phải cộng vào 1  họ có thể cân nặng các nhánh độc lập.

### Tại sao điều này là "đáng tạo"

Bước lựa chọn (những khối top-k) là riêng biệt. Các hoạt động riêng biệt phá vỡ dòng chảy gradient. Công việc chú ý ít trước đó hoặc bỏ qua backprop thông qua lựa chọn (các khóa học) hoặc sử dụng thư giãn liên tục mà không cung cấp sự ít thực tế khi suy luận.

NSA bỏ qua điều này: sự chú ý của các nhánh nén là một sự chú ý thô lỗ phân biệt trên toàn bộ chuỗi. Hoạt động top-k chỉ sử dụng lại điểm chú ý cao nhất từ nhánh nén để chọn những khối hạt mỏng để tải. Các gradient chảy qua các điểm số của các nhánh nén (được ảnh hưởng đến cả kết quả nén và logic lựa chọn), và đóng góp của các khối được chọn vào kết quả cuối cùng cũng có thể phân biệt. Không phân biệt được`top_k`hoạt động là không hoạt động trên biểu đồ tính toán phía trước nó chỉ kiểm soát những khối nào được tải từ bộ nhớ.

Đây là lý do tại sao NSA có thể được sử dụng trong việc huấn luyện trước cuối đến cuối. mô hình học cách định tuyến thông tin qua ba chi nhánh chung, tạo ra một mô hình hiếm có mà khi suy luận thực sự cung cấp tốc độ hứa hẹn.

### Bộ hạt nhân được sắp xếp với phần cứng

Lớp lõi của NSA được thiết kế cho các hệ thống phân cấp bộ nhớ GPU hiện đại. Lớp lõi tải các truy vấn bởi các nhóm GQA (cuối bên ngoài), lấy các khối KV hiếm tương ứng trên mỗi nhóm (cuối bên trong), và chạy sự chú ý trên SRAM. Bởi vì mỗi nhóm truy vấn nhìn thấy các khối được chọn giống nhau (chuyển chọn là mỗi nhóm truy vấn, không phải mỗi đầu truy vấn), các khối KV được giảm giá trên toàn nhóm. Độ cường số toán vẫn cao.

Báo cáo báo cáo hạt nhân Triton chạy nhanh hơn 9 lần so với FlashAttention trên 64k decode, với tỷ lệ tăng tốc tăng theo chiều dài chuỗi.

### Ngân sách tính toán

Để `N`có chiều dài chuỗi, `l`kích thước khối nén, `k`số lựa chọn trên cùng k, `w`cửa sổ trượt, `b`kích thước khối được chọn (thường bằng `l`().

- Chiếc nhánh bị nén: `O(N/l)`khóa cho mỗi truy vấn, vì vậy `O(N * N / l)`Toàn bộ.
- Nh chọn nhánh: `O(k * b)`khóa cho mỗi truy vấn, vì vậy `O(N * k * b)`- Tôi không biết.
- Chiếc nhánh trượt: `O(w)`khóa cho mỗi truy vấn, vì vậy `O(N * w)`- Tôi không biết.

Tổng số: `O(N * (N/l + k*b + w))`- Tôi không biết.

Với `N = 64k, l = 64, k = 16, b = 64, w = 512`: chi phí cho mỗi yêu cầu là `1000 + 1024 + 512 = 2536 keys`- Cảm ơn anh rất nhiều.`64000 keys`. 25 lần giảm tính toán.

Với `N = 128k, l = 64, k = 16, b = 64, w = 512`: chi phí cho mỗi yêu cầu là `2000 + 1024 + 512 = 3536 keys`- Cảm ơn anh rất nhiều.`128000 keys`Tỷ lệ giảm 36x. Lợi ích tăng lên theo chiều dài chuỗi, đó là toàn bộ điểm.

### Nó so sánh như thế nào?

| Method | Differentiable | Real inference speedup | Long-range recall |
|--------|---------------|----------------------|-------------------|
| Sliding window only | yes | yes | fails |
| Strided / block-sparse | yes | yes | partial |
| KV pruning (H2O, StreamingLLM) | N/A (inference-time) | yes | partial |
| MoBA (Moonshot) | partial | yes | good |
| NSA | yes (natively) | yes (9x at 64k) | matches full attention |

MoBA (Moonshot, arXiv:2502.13189) được xuất bản đồng thời và áp dụng một cách tiếp cận tương tự như ba là tốt hơn một, áp dụng nguyên tắc MoE cho các khối chú ý. NSA và MoBA là hai kiến trúc để biết cho 2026 dài ngữ cảnh đào tạo trước.


> **【拓展：稀疏注意力在长上下文中的应用】**密集注意力 O(n^2) 计算量使 128K 上下文的预填阶段需要约30秒──稀疏方法(如 NSA、Ring Attention) 将其降至可接受范围──Gemini 1.5 Pro 的1M token 上下文依赖于稀疏注意力──


## Hãy xây dựng nó.
```figure
sliding-window-attention
```

## Hãy xây dựng nó

`code/main.py`thực hiện ba chi nhánh trên một chuỗi tổng hợp ngắn và cho thấy:

- MLP nén (một đường cơ sở trung bình đơn giản được sử dụng để làm rõ về giáo dục; NSA thực sự sử dụng MLP được học).
- Việc lựa chọn khối top-k được thúc đẩy bởi điểm số của các nhánh nén.
- Sự chú ý của cửa sổ trượt trên cuối cùng `w`- Đồ chơi.
- Sự kết hợp bị khóa.
- Một bản in tính toán so sánh với sự chú ý đầy đủ.

### Bước 1: nén token thành khối

```python
def compress(K, l):
    n = len(K)
    n_blocks = (n + l - 1) // l
    out = []
    for b in range(n_blocks):
        start, end = b * l, min((b + 1) * l, n)
        block = K[start:end]
        summary = [sum(row[d] for row in block) / len(block) for d in range(len(K[0]))]
        out.append(summary)
    return out
```

### Bước 2: Kiểm tra các nhánh bị nén

Tiếp tục softenmax sự chú ý của truy vấn đối với các phím nén. điểm nén-cánh nén gấp đôi như tín hiệu cho lựa chọn top-k.

### Bước 3: Chọn khối top-k

Chọn các chỉ số của `k`Các khối nén có điểm số cao nhất, tải các token không nén gốc từ các khối đó và chú ý đến chúng.

### Bước 4: Kiểm tra cửa sổ trượt

Hãy lấy cái cuối cùng`w`Đèn chỉ và chạy sự chú ý tiêu chuẩn đối với chúng.

### Bước 5: cổng + kết hợp

Một MLP nhỏ trên truy vấn tạo ra ba trọng lượng cổng.

### Bước 6: tính toán

Bác in số lượng phím được tham gia cho mỗi truy vấn cho mỗi chi nhánh và tổng số. So sánh với `N`(có thể chú ý) trên một token tổng hợp 1024 với`l = 32, k = 4, w = 128`NSA thấy`32 + 128 + 128 = 288`các khóa mỗi truy vấn so với 1024 để chú ý đầy đủ  3,5 lần ít hơn.

## Hãy sử dụng nó để thực hiện

NSA đang vận chuyển trong đường ống dẫn đào tạo dài của DeepSeek.

- **DeepSeek internal**: bản địa, các trọng lượng được công bố sử dụng NSA hoặc kế nhiệm của nó DSA (Deepseek Sparse Attention).
- **vLLM**: hỗ trợ thử nghiệm của NSA trong quá trình phát triển cho trọng lượng DeepSeek-V3.x.
- **SGLang**: Các chỉ số chuẩn của NSA được công bố; con đường sản xuất theo vLLM.
- **llama.cpp / CPU**: không được hỗ trợ; Overhead của phân hủy hạt nhân không đáng giá tại CPU thông qua.

Khi nào để liên lạc với NSA:

- Các khóa đào tạo trước hoặc tiếp tục đào tạo nhắm mục tiêu vào hơn 64k bối cảnh với ngân sách tính toán nghiêm trọng.
- Đánh giá từ các điểm kiểm tra trong bối cảnh dài của DeepSeek.

Khi nào không nên:

- Bạn không thể nâng cấp NSA mà không cần đào tạo.
- Mức độ dưới 16k.
- Chat tương tác Batch-1 có lợi ích giải mã nhạy cảm với độ trễ, nhưng chỉ trong các bối cảnh dài.

## Chuyển nó đi.

Bài học này sẽ mang lại kết quả `outputs/skill-nsa-integrator.md`. Với một kỹ thuật chạy trước khi đào tạo trong bối cảnh dài, nó tạo ra một kế hoạch tích hợp NSA: kích thước khối nén, top-k, cửa sổ trượt, chiều rộng gate MLP, lựa chọn lõi và các đánh giá cụ thể trong bối cảnh dài sẽ biện minh cho sự thay đổi kiến trúc.

> 本课产 出 `outputs/skill-nsa-integrator.md` Giấy dài trên dưới đây chuẩn bị cho các quy tắc vận hành, nó tạo ra NSA 集成 kế hoạch: cục khối cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ cục bộ

## Tập luyện bài tập

1. Đi chạy`code/main.py`trên một token tổng hợp 1024.`(l, k, w)`xác định các thiết lập sẵn đạt được số lượng khóa thấp nhất cho mỗi truy vấn trong khi giữ 95% nhớ lại với sự chú ý đầy đủ trong một bài kiểm tra kim cương.
   Trung文翻译: 在 1024-token 合成数据上运行 `code/main.py` Trong 3 dự kiến`(l, k, w)`并印计算量―― tìm thấy trong thử nghiệm lầy lúa  để giữ toàn bộ sự chú ý 95%  quay lại tỷ lệ đồng thời đạt được tối thiểu của mỗi điều tra khóa tính toán dự đoán──

2. Thay thế máy nén trung bình bằng một máy nén trung bình nhỏ được học MLP (2 lớp, ẩn 32). Đào tạo nó trên một nhiệm vụ tổng hợp nơi tín hiệu là trung bình của một khối. đo khoảng cách phức tạp so với đường cơ sở trung bình trên dữ liệu được giữ.
   Trung文翻译:用小型学习 MLP(2层, hidden 32) thay thế trung bình giá trị của khối lượng 压缩机.

3. Thực hiện các cửa MLP. Nó lấy truy vấn như đầu vào và xuất ra ba scalars. cho thấy rằng cửa cư xử hợp lý: trọng lượng gần giống nhau trên truy vấn ngẫu nhiên, trọng lượng nặng trên nhánh được chọn khi truy vấn chạm vào một khối phía sau xa.
   Trung ngữ翻译:实现门控 MLP──它以查询为输入输出三个标量──展示门控行为合理:随机查询时近似均加权,查询命中远回块时对选定分支重度加权──

4. Xét ngân sách bộ nhớ cache KV cho mô hình 70B được hỗ trợ bởi NSA ở ngữ cảnh 128k. Đầu KV là 8, đầu tối 128, BF16. So sánh với sự chú ý đầy đủ và với MLA (Phase 10 · 14 cho thấy số MLA).
   Trung ngữ翻译:计算 NSA 启动的70B 模型在 128K 上下文 下 KV 缓存内存预算。KV 头 8 个,头维度 128,BF16。与全注意力和MLA比较。找到 NSA 细粒度分支 KV 缓存等于全注意序列长度。

5. Đọc Phần 4 của bài báo NSA (arXiv:2502.11089) và giải thích bằng ba câu tại sao điểm chú ý của nhánh nén được sử dụng lại cho việc lựa chọn top-k thay vì tính toán điểm định tuyến riêng biệt.
   Trung ngữ翻译:阅读 NSA 论文第4节, sử dụng ba câu giải thích tại sao số lượng chú ý của phân đoạn nén được sử dụng để chọn top-k thay vì tính số lượng phân đoạn đường riêng lẻ.

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|------------------------|---------|
| Compressed branch | "Coarse view" | Attention over block-averaged keys that provides global context in O(N/l) keys per query | 压缩分支，块平均键上的注意力 |
| Selected branch | "Top-k blocks" | Fine-grained attention over the `k` blocks with highest compressed-branch scores | 选择分支，对 top-k 块做细粒度注意力 |
| Sliding window | "Local context" | Attention over the last `W` tokens for short-range patterns | 滑动窗口，最近 W 个 token 的局部上下文 |
| Native trainability | "Pre-train with the sparsity on" | The sparsity pattern is learned during pre-training, not bolted on at inference | 原生可训练，预训练时就使用稀疏模式 |
| Compression block size l | "Group size for coarse view" | How many tokens get merged into one summary; 32-64 typical | 压缩块大小，每组合并多少 token |
| Top-k | "Blocks to keep" | Number of compressed blocks whose uncompressed tokens get read; 16 typical | Top-k，保留的压缩块数量 |
| Sliding window W | "Local attention radius" | Typically 512; shorter hurts local coherence, longer wastes compute | 滑动窗口大小，典型值 512 |
| Branch gate | "How to mix the three" | Per-position MLP output that weights the three branches' contributions | 分支门控，MLP 输出加权三分支贡献 |
| Hardware alignment | "Kernel-friendly sparsity" | Sparse pattern chosen so that the actual GPU kernel achieves the theoretical speedup | 硬件对齐，稀疏模式适配 GPU 核函数 |
| DSA | "NSA's successor" | Deepseek Sparse Attention, the architecture that followed NSA in DeepSeek's lineage | DSA，DeepSeek 稀疏注意力，NSA 的后继架构 |

## Xem thêm 延伸阅读

- [Yuan et al. — Native Sparse Attention: Hardware-Aligned and Natively Trainable Sparse Attention (arXiv:2502.11089, ACL 2025 Best Paper)](https://arxiv.org/abs/2502.11089) tờ báo
- [DeepSeek-V3 Technical Report (arXiv:2412.19437)](https://arxiv.org/abs/2412.19437) các mục tiêu của gia đình kiến trúc NSA
- [Moonshot AI — MoBA: Mixture of Block Attention for Long-Context LLMs (arXiv:2502.13189)](https://arxiv.org/abs/2502.13189) Công việc đồng thời, tập trung vào các khối theo phong cách MoE
- [Beltagy et al. — Longformer: The Long-Document Transformer (arXiv:2004.05150)](https://arxiv.org/abs/2004.05150) nguồn gốc cửa sổ trượt
- [Xiao et al. — StreamingLLM: Efficient Streaming Language Models with Attention Sinks (arXiv:2309.17453)](https://arxiv.org/abs/2309.17453) Tiêu chuẩn cơ sở của sự thâm hụt thời gian suy luận NSA cải thiện trên
- [Dao et al. — FlashAttention-2 (arXiv:2307.08691)](https://arxiv.org/abs/2307.08691) cơ sở của sự chú ý đầy đủ của các hạt nhân NSA đánh bại ở 64k
