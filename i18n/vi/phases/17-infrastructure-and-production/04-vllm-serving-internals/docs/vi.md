# vLLM Serving Internals: PagedAttention, Continuous Batching, Chunked Prefill  vLLM n định dịch vụ cơ chế nội bộ:分页注意力、连续批处理、分块预填
# Dịch vụ động cơ nội bộ  PagedAttention, liên tục batching, Chunked Prefill

> Công cụ phục vụ hiện đại dựa trên ba sự cố định hợp nhất, không phải một thủ thuật duy nhất. PagedAttention luôn bật. Các lần phát tập liên tục cho phép các yêu cầu mới vào các lần phát tập hoạt động giữa các lần lặp mã hóa. Các mảnh prefill slic dài để giải mã token không bao giờ chết đói. Động tất cả ba và một Llama 3.3 70B FP8 trên một H100 SXM5 đẩy 2.200-2.400 tok / s ở 128 đồng thời  khoảng 25% trên vLLM tự mặc định và 3-4x một vòng PyTorch ngây thơ. Bài học này đọc lập trình và hạt nhân chú ý của vLLM  động cơ tham chiếu cho cả ba kỹ thuật  ở một mức độ bạn có thể vẽ, và kết thúc với một bộ đúc đồ chơi liên tục trong `code/main.py`những lịch trình prefill và decode như vLLM làm.

> **【中文解读】**vLLM trong năm 2026 chủ quyền dựa trên ba phức tạp tối ưu hóa:PagedAttention(分页注意力)始终开启;连续批处理在解码代间注入新请求;分块预填片长提示以防止解码代币 饥饿。三者全开时,Llama 3.3 70B FP8 在单卡H100上以 128并发达2,200-2,400 tok/s比朴素PyTorch 循环快 3-4倍。

> **【拓展：vLLM → LLM 推理服务标准】**vLLM là công cụ dịch vụ mở nguồn phổ biến nhất năm 2026 của LLM 推理服务引擎。PagedAttention 借借借操作系统的虚拟内存分页思想管理 KV Cache, sẽ kiểm soát tỷ lệ mảnh vỡ ở mức 4% 以下。 tiếp tục xử lý hàng loạt cho phép trong các bước giải mã động động trong khi gia nhập yêu cầu mới, tăng đáng kể tỷ lệ sử dụng GPU。 đây là một kỹ thuật cần thiết của LHM trong Bộ Sản xuất Môi trường。

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy continuous batching scheduler) | **语言:** Python（标准库，连续批处理调度器模拟）
**Prerequisites:** Phase 17 · 01 (Model Serving), Phase 11 (LLM Engineering) | **前置知识:** Phase 17 · 01（模型服务）, Phase 11（LLM 工程）
**Time:** ~75 minutes | **时间:** ~75 分钟

>  **【前置】**Học本节前请先掌握:Phase 11·12(推理优化基础) 、KV cache 概念、连续批处理──vLLM 是 2026 开源推理引擎的事实标准──
>  **【类比】**vLLM 三件套 = "高效餐厅厨房"。PagedAttention = 分块管理 KV cache(像操作系统虚拟内存分页,碎片率 < 4%);Continuous Batching = 动态拼单(新请求随时插入运行批);Chunked Prefill = 切长快速(长输切片避免阻塞解码)。Llama 3.3 70B FP8 在 H100 上 128 并发达 2200-2400 tok/s,比朴素实现快 3-4 ⋅倍

## Mục tiêu học tập

- Giải thích PagedAttention như một bộ phân bổ cache KV: khối, bảng khối, và tại sao phân mảnh vẫn dưới 4% khi tải sản xuất.
  Trung文翻译:将 PagedAttention 解释为 KV 缓存分配器:块、块表,以及为什么在生产负载下碎片率保持在4% 以下──
- Chụp đồ họa liên tục đợt đợt đợt lặp ở cấp độ lặp: các chuỗi hoàn thành rời khỏi đợt và các chuỗi mới kết hợp mà không bị khử.
  Trung ngữ翻译:在代级别绘制连续批处理: đã hoàn thành序列如何离开批次,新序列如何加入而无需清空──
- Mô tả prefill cục cục trong một câu và tên là métric độ trễ mà nó bảo vệ (khí dụ: đó là đuôi TTFT, không phải là thông qua trung bình).
  Trung ngữ翻译:用一句话描述分块预填充,并说出它保护哪个延迟指标(提示:是 TTFT 尾部,而不是平均吞吐量)
- Tên gọi 2026 vLLM v0.18.0 có được một cái gì đó mà cắn đội cho phép mọi tối ưu hóa cùng một lúc.
  Trung文翻译:说出 2026 年 vLLM v0.18.0 中同时启动所有优化团队会遇到问题──

## Vấn đề  vấn đề giới thiệu

> **【中文解读】**朴素 PyTorch 服务循环一次处理一个请求――静态批处理将所有请求填充到最长序列,浪费 GPU资源并让快请求等待慢请求――vLLM 通过三个核心优化解决这个问题:PagedAttention(KV Cache 碎片率从60-80% 降至4% 以下) 连续批处理(在解码代间动态加入新请求) 分块预填(将长提示切片以防止解码饥饿) 

Một vòng phục vụ PyTorch ngây thơ chạy một yêu cầu một lần: token, prefill, decode cho đến EOS, trả lại. Với một người dùng, điều này hoạt động. Ở một trăm, đó là một hàng người kiên nhẫn. Việc sửa chữa rõ ràng  đóng gói tĩnh  pads mỗi yêu cầu đến prompt dài nhất trong cửa sổ, pads mỗi decode đến đầu ra dài nhất mong đợi, và trì hoãn toàn bộ lô trên chuỗi chậm nhất. Bạn trả tiền cho chất đệm mà bạn không bao giờ sử dụng, và yêu cầu nhanh chờ đợi những yêu cầu chậm.

> 朴素 PyTorch 服务循环一次处理一个请求:分词、预填、解码直到EOS、返回。 một người dùng khi nào đó đã được thực hiện.

vLLM giải quyết ba vấn đề cùng một lúc. PagedAttention ngăn chặn phân mảnh cache KV ăn 60-80% bộ nhớ GPU theo cách phân bổ liên tục cổ điển. Lập liên tục cho phép các yêu cầu kết nối và rời khỏi lô giữa mỗi lần lặp lại mã hóa, vì vậy lô luôn đầy đủ công việc thực sự. Chunked prefill phá vỡ một token 32k-token thành ~512 token slices mà liên kết với decode, vì vậy một prompt dài không đóng băng mọi token decode trên GPU.

> vLLM một lần giải quyết ba vấn đề. PagedAttention  ngăn chặn KV 缓存碎片 như phân phối liên tục cổ điển như vậy 吞 60-80% của GPU 内存. 连续批处理让请求在每个解码代之间加入和离开批次,所以批次总是充满真实工作.

Các sản phẩm 2026 mặc định là tất cả ba vào. Bạn cần phải hiểu mỗi người làm gì bởi vì các chế độ thất bại tất cả trên lịch trình, không phải mô hình.

> Các thiết lập mặc định sản xuất năm 2026 là ba. Bạn cần phải biết mỗi cái làm gì, bởi vì các mô hình lỗi đều trên điều chỉnh, chứ không phải trên mô hình.

## Khái niệm cốt lõi

### PagedAttention như một hệ thống bộ nhớ ảo

> **【中文解读】**PagedAttention 借借鉴操作系统虚拟内存分页思想管理 KV Cache。 truyền thống tiếp tục phân phối cho mỗi chuỗi预分配最大长度(如8192 token), nhưng trung bình yêu cầu chỉ sử dụng 1500 token, lãng phí 82% của HBM。PagedAttention sẽ phân chia KV Cache thành khối cố định lớn nhỏ ((默认16 token), mỗi chuỗi có một khối bảng映射逻辑 vị trí đến ID khối vật lý, phân phối theo yêu cầu, tỷ lệ mảnh nhỏ dưới 4%。 đây là phân phối viên duy nhất của vLLM, thông qua`--gpu-memory-utilization`(默认 0.9) kiểm soát KV Cache có thể sử dụng HBM Ví dụ:

> **【拓展：KV Cache 内存管理演进】**KV Cache 内存管理 đã trải qua ba thế hệ phát triển: 1) 连续预分配简单但浪费60-80%内存; 2) PagedAttention(vLLM 2023) 分页管理,碎片率 <4%, trở thành tiêu chuẩn ngành; 3) RadixAttention(SGLang 2024)                                                                                                                                                                                                                          

Một bộ nhớ cache KV là `num_layers × 2 × num_heads × head_dim × seq_len × bytes_per_element`Đối với Llama 3.3 70B với 8192 token, đó là khoảng 1,25 GB mỗi chuỗi trong BF16. Nếu bạn dự trữ trước 8192 khe cho mỗi yêu cầu nhưng yêu cầu trung bình chỉ sử dụng 1500 token, bạn lãng phí khoảng 82% HBM bạn đã dự trữ.

> Mỗi chuỗi KV 缓存大小为 `num_layers × 2 × num_heads × head_dim × seq_len × bytes_per_element`❖ Llama 3.3 70B trong 8192 token 时,BF16 下 mỗi chuỗi khoảng 1.25 GB ⋅ Nếu bạn cho mỗi yêu cầu dự kiến dự kiến dự kiến 8192 槽位, nhưng yêu cầu trung bình chỉ sử dụng 1500 token, bạn lãng phí khoảng 82% 预留 HBM ⋅ Classic批处理承担这种浪费──

PagedAttention vay ra ý tưởng từ bộ nhớ ảo của hệ điều hành. KV cache không liên kết cho từng chuỗi. Nó được phân bổ trong các khối kích thước cố định (tầm 16 token). Mỗi chuỗi có một bảng khối mà lập bản đồ vị trí mã thông báo logic của nó cho ID khối vật lý. Khi một chuỗi phát triển vượt qua các khối được phân bổ, một khối nữa được thêm vào. Khi nó hoàn thành, các khối của nó trở lại hồ bơi.

> PagedAttention 借借借操作系统虚拟内存的思想──KV 缓存 không phải là của mỗi chuỗi liên tục── nó được phân phối bằng một khối lớn cố định(默认 16 token)── mỗi chuỗi có một bảng khối, sẽ có một biểu tượng logic 位置映射到物理块 ID── khi chuỗi tăng lên hơn khối đã phân phối, thêm một khối mới── hoàn thành, khối trở lại trong池──

Phân tích giảm từ 60-80% (classic) xuống dưới 4% (PagedAttention). Bạn không kích hoạt PagedAttention với cờ  nó là tàu phân bổ vLLM duy nhất. nút là `--gpu-memory-utilization`(trọng lượng mặc định 0.9), cho biết vLLM phải lưu lượng HBM cho các khối KV sau khi tải trọng và kích hoạt.

> 碎片率 từ 60-80% (经典) giảm xuống còn 4% 以下 (PagedAttention) ――you don't need a tag to enable PagedAttention它是vLLM 唯一分配器──旋是`--gpu-memory-utilization`(默认 0.9), nói với vLLM trong tải trọng và kích hoạt sau khi cho KV khối dự trữ bao nhiêu HBM.

### Lượng hàng liên tục ở cấp độ lặp lại

> **【中文解读】**连续批处理在每个解码步骤之间做出接受/释放决策――每个代:(1) 移除已完成的序列;;(((2) 检查等队列, nếu có空 KV块则接收新序列;(3) đối với tất cả các序列 trong danh sách chạy thực hiện một lần tiến triển传播;;批次大小不定,不同输出位置序列共享一次融合前向计算;;2026 vLLM V1 调度器的核心不变量是:调度器解码每个代运一次,而不是每请求运一次;;

"Dynamic batching" cũ chờ đợi một cửa sổ (chẳng hạn là 10 ms) để lấp đầy một lô, sau đó chạy prefill + decode + decode + decode cho đến khi mỗi chuỗi kết thúc.

> 旧的"动态批处理" chờ một cửa sổ (như 10ms) để lấp đầy các lô, sau đó chạy prefill + decode + decode + decode cho đến khi mỗi chuỗi hoàn thành.

Lần phát tập liên tục hoạt động giữa mỗi bước giải mã.`RUNNING`danh sách. Tại mỗi lần lặp lại:

> 连续批处理在每个解码步骤之间操作――将运行中的序列集合称为 `RUNNING`列表──每次代:

1. Bất kỳ chuỗi nào trong `RUNNING`chỉ cần nhấn EOS hoặc max_tokens được xóa.
   Trung ngữ翻译:`RUNNING`Trong khi đạt EOS hoặc max_tokens bất kỳ chuỗi nào được di chuyển.
2. Người lập trình nhìn vào hàng chờ. Nếu có các khối KV miễn phí, nó sẽ chấp nhận các chuỗi mới (số trước hoặc tiếp tục).
   Trung文翻译:调度器查看等队列──如果有空 KV 块,它接纳新序列(预填充或恢复)──
3. Lệnh đi trước sẽ chạy trên bất cứ thứ gì đang ở trong.`RUNNING`, phát ra một token mới cho mỗi chuỗi.
   Trung文翻译:前向传播对 `RUNNING`Trong tất cả các nội dung hoạt động, mỗi chuỗi phát hành một mã thông báo mới.

Kích thước lô không bao giờ được đệm đến một số cố định.`V1 scheduler`. Key invariant: Scheduler chạy một lần mỗi lần lặp lại mã hóa, không phải một lần mỗi yêu cầu.

> 批次大小从不填充到固定数字――输出不同位置的序列共享一次融合前向传播――2026年 vLLM 中称为`V1 scheduler`❖关键不变量:调度器 mỗi解码代运行一次,而不是每个请求运行一次──

### Lưu trữ trước được làm mảnh bảo vệ đuôi TTFT

> **【中文解读】**分块预填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填填

> **【拓展：vLLM 生产部署最佳实践】**Các cấu hình quan trọng của VLLM 生产部署 năm 2026 bao gồm:`--gpu-memory-utilization 0.9`预留 90% HBM 给 KV Cache;(2) `--max-model-len`根据实际需求设置而非默认最大值;(3) 分块预填默认开启但与某些推测解码模式不兼容;(4) `--enable-prefix-caching`Trong trường hợp RAG/Agent có thể giảm đáng kể việc lặp lại và lấp đầy trước;

Prefill được tính toán. Một lệnh 32k-token trên Llama 3.3 70B mất ~ 800 ms prefill tinh khiết trên một H100. Trong khi prefill chạy, giải mã token cho mọi chuỗi khác trong vòng chờ. Trong vòng bán hàng, latency token đầu tiên (TTFT) của một lệnh dài trở thành điểm trôi giữa token (ITL) cho hàng chục người dùng khác.

> 预充是计算密集型的──Llama 3.3 70B 上一个32K token提示在单卡H100 上需要约800ms的纯预充──预充运行时,批次中所有其他序列的解码代码代码都在等待── 在服务循环中, một长提示的首个代码 延迟(TTFT) đã biến thành vài chục代码 của các người dùng khác 间延迟(ITL) 毛刺──

Chunked prefill chia prefill thành các khối kích thước cố định (tầm 512 token) và lập lịch từng phần như một đơn vị. Giữa các khối người lập lịch có thể tiến bộ các chuỗi giải mã bằng một token. Bạn trao đổi một lần trúng trúng thời gian trúng trúng tuyệt đối nhỏ (một vài ms mỗi phần) cho thời gian giải mã thấp hơn nhiều. P99 ITL dưới tải hỗn hợp giảm từ ~ 50 ms đến ~ 15 ms trong các tiêu chuẩn được xuất bản.

> Chia các khối dự trữ sẽ được phân bổ trước chia thành khối cố định kích thước lớn (默认 512 token), mỗi khối là một đơn vị điều chỉnh. Trong các khối, bộ điều chỉnh có thể thúc đẩy chuỗi giải mã một token. Bạn sử dụng một lượng nhỏ để hoàn toàn dự trữ chậm trễ.

### Ba mặc định tương tác

Tất cả ba tính năng đều giả định nhau. PagedAttention cung cấp cho lập trình viên một nguồn KV hạt mỏng để giao dịch với.`RUNNING`danh sách  đó là một chính sách lập lịch hơn, không phải một hệ thống riêng biệt.

> Ba đặc điểm phụ thuộc lẫn nhau. PageedAttention cho điều chỉnh cung cấp các KV tài nguyên để điều chỉnh.`RUNNING`Các quyết định được đưa ra trên danh sách đó là một chiến lược điều chỉnh khác, không phải là hệ thống độc lập.

Bạn không cần phải biết mọi cờ, bạn cần phải biết những gì lập trình viên tối ưu hóa: tốt trong ngân sách khối KV, tùy thuộc vào cắt prefill mảnh.

> Bạn không cần biết mỗi biểu tượng. Bạn cần biết điều chỉnh máy điều chỉnh.

### 2026 v0.18.0 đã có bạn

> **【中文解读】**vLLM v0.18.0 中 không thể bật cùng lúc `--enable-chunked-prefill`和 mô hình dự thảo 推测解码`--speculative-model`(..) Một ngoại lệ duy nhất là N-gram GPU trong V1 điều chỉnh 推测解码. Không đọc thông báo phát hành về việc mở tất cả các dấu hiệu tối ưu hóa sẽ gặp lỗi trong khi chạy khi khởi động, chứ không phải là suy giảm tính chất.

Trong vLLM v0.18.0 bạn không thể kết hợp `--enable-chunked-prefill`Với mô hình dự thảo giải mã dự đoán (`--speculative-model`(). Ngoại lệ được ghi chép là giải mã GPU đầu cơ N-gram trong trình lập lịch V1. Các đội bật mọi cờ mà không đọc thông báo phát hành sẽ có lỗi thời gian chạy khi khởi động, không phải sự lùi lại mềm. Nếu lợi nhuận đầu cơ của bạn đáng để cho phép prefill cho, xem lại sự lựa chọn  câu trả lời đúng vào năm 2026 thường là EAGLE-3 mà không có prefill cho, không phải một mô hình dự thảo cộng với prefill cho không biên soạn.

> Trong vLLM v0.18.0, bạn không thể bật cùng lúc `--enable-chunked-prefill`和 mô hình dự thảo 推测解码`--speculative-model`(N1 调度器中的 N-gram GPU 推测解码――不读发布说明 về mở tất cả các mã hiệu của nhóm khi khởi động gặp lỗi trong khi chạy chứ không phải bị suy giảm tính mềm. Nếu giá trị lợi nhuận của việc mở các khối dự kiến, hãy xem xét lại 选择2026 Câu trả lời chính xác thường là EAGLE-3 chứ không phải mô hình dự thảo.

### Những con số mà bạn nên nhớ

- Llama 3.3 70B FP8, H100 SXM5, 128 đồng thời, cả ba trên: 2.200-2.400 tok / s.
  Trung文翻译:Llama 3.3 70B FP8,H100 SXM5,128 并发,三个优化全开:2,200-2,400 tok/s。
- Mô hình tương tự, vLLM mặc định (không có prefill cục bộ): ~ 1,800 tok/s.
  Trung文翻译:同模型,默认 vLLM(无分块预填充): khoảng 1.800 tok/s。
- Tương tự mô hình, PyTorch forward loop ngây thơ: ~600 tok/s.
  Trung文翻译:同模型,朴素 PyTorch 前向循环: khoảng 600 tok/s。
- Lưu thải phân mảnh KV dưới PagedAttention khi tải sản xuất: < 4%.
  Trung文翻译:PagedAttention 在生产负载下 KV碎片浪费:<4%──
- P99 ITL dưới tải hỗn hợp: ~ 15 ms với prefill mảnh, ~ 50 ms mà không có.
  Trung文翻译:混合负载下 P99 ITL:有分块预填充约15ms,无约50ms。

### Định trình lịch trình trông như thế nào

```
while True:
    finished = [s for s in RUNNING if s.is_done()]
    for s in finished: release_blocks(s); RUNNING.remove(s)

    while WAITING and have_free_blocks_for(WAITING[0]):
        s = WAITING.pop(0)
        allocate_initial_blocks(s)
        RUNNING.append(s)

    # schedule prefill chunks + decode in one batch
    batch = []
    for s in RUNNING:
        if s.in_prefill:
            batch.append(next_prefill_chunk(s))   # e.g. 512 tokens
        else:
            batch.append(decode_one_token(s))     # 1 token

    run_forward(batch)                            # one fused GPU call
```

`code/main.py`là chính xác vòng lặp này trong stdlib Python với số lượng token giả và độ trễ về phía trước giả.

> `code/main.py`Chính là vòng lặp này của Python 实现, sử dụng mã thông báo giả 计数 và giả tiền trễ 延迟.

## Hãy sử dụng nó để thực hiện
```figure
tensor-parallel
```

## Sử dụng nó

`code/main.py`mô phỏng một trình lập lịch kiểu vLLM với các tính năng có thể chuyển đổi.

> `code/main.py`模拟一个带有可换功能的 vLLM 风格调度器──运行它 có thể xem:

- `NAIVE`chế độ: một yêu cầu một lần, không có hàng.
  Trung ngữ翻译:`NAIVE`模式: một lần một yêu cầu, không xử lý.
- `STATIC`chế độ: pad và chờ, batching cổ điển.
  Trung ngữ翻译:`STATIC`模式:填充并等待, cổ điển xử lý批量──
- `CONTINUOUS`chế độ: nhập và phát hành ở cấp lặp.
  Trung ngữ翻译:`CONTINUOUS`模式: 代级的接纳和释放──
- `CONTINUOUS + CHUNKED`chế độ: Prefill slices được trộn với decode.
  Trung ngữ翻译:`CONTINUOUS + CHUNKED`模式:预填切片与解码交错.

Kết quả xuất hiện cho thấy tổng thông qua (tốc hiệu mỗi giây ảo), trung bình TTFT và P99 ITL.`CONTINUOUS + CHUNKED`hàng nên thống trị giao thông hỗn hợp.

> 输出显示总吞吐量(每虚拟秒代币 数) 、TTFT 平均值和 P99 ITL。`CONTINUOUS + CHUNKED`行在混合流量下应占主导地位.

## Chuyển nó đi.

> **【拓展：LLM 推理引擎对比】**2026 năm LHQ 推理引擎包括:vLLM(通用生产默认,PagedAttention+连续批处理) 、SGLang(前共享优化,RadixAttention) 、TensorRT-LLM(NVIDIA 专属,Blackwell 上吞吐最高)、llama.cpp(CPU/边缘,GGUF 格式) ⋅选择取取于硬件(CPU/GPU/Hopper/Blackwell) ⋅工作负载(通用聊天/Agent/RAG) 和合规要求自(托管/云托管) ⋅vLLM 约60%的生产部署量根据2026 AI 基础设施调查) ⋅

Bài học này sẽ mang lại kết quả `outputs/skill-vllm-scheduler-reader.md`Với cấu hình phân phối (kích thước lô, sử dụng bộ nhớ KV, kích thước prefill chia nhỏ, cấu hình đầu cơ), nó tạo ra một chẩn đoán lập trình cho tên là ba mặc định là nút thắt chai và điều gì để điều chỉnh.

> 本课产 出 `outputs/skill-vllm-scheduler-reader.md`△ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △                                                                                                               

## Tập luyện bài tập

1. Đi chạy`code/main.py`- So sánh`STATIC`đến`CONTINUOUS`khi tải trọng công việc với các yêu cầu ngắn và dài hỗn hợp.
   Trung ngữ翻译:运行 `code/main.py`◊ trong hỗn hợp dài hạn yêu cầu tải trọng làm việc`STATIC`和 `CONTINUOUS`◊ Sự khác biệt dung lượng từ đâu  hiệu quả dự kiến lấp đầy  hiệu quả giải mã  hoặc chậm trễ?
2. Thay đổi lập trình đồ chơi để thêm `--max-num-batched-tokens`. Giá trị chính xác của H100 chạy Llama 3.3 70B FP8 là gì? (Đề nghị: nó là một hàm của kích thước khối KV và số lượng khối tự do, không phải là HBM thô.)
   Trung ngữ翻译:修改模拟调度器添加 `--max-num-batched-tokens`H100 运行 Llama 3.3 70B FP8 的正确值是多少?提示:是 KV 块大小和空块数的函数,而不是原始 HBM。)
3. Đọc lại các ghi chú phát hành vLLM v0.18.0.
   Trung文翻译:重新读 vLLM v0.18.0 发布说明──哪些标志组合互斥?列出它们──
4. Xét lượng lãng phí phân mảnh cache KV cho một số 1000 yêu cầu với trung bình 1.500 token đầu ra, std 600 token, dưới (a) phân bổ liên tiếp mỗi yêu cầu ở mức 8192 tối đa, (b) PagedAttention với 16 block token.
   Trung文翻译:计算 1,000 个请求的 KV 缓存碎片浪费(平均值 1,500 输出代币,标准差 600),在 (a) 最大 8192 的连续每请求分配和 (b) 16代币块的 PagedAttention 下。
5. Giải thích trong một đoạn tại sao việc sơn trước bằng mảnh giúp P99 ITL nhưng không giúp tính năng thông qua một cách riêng biệt.
   Trung ngữ翻译:用一段话解释为什么分块预填充帮助P99 ITL但不单独提升吞吐量──实际中吞吐量提升从何而来?

## Từ khóa  Từ khóa nhanh chóng

| Term / 术语 | What people say / 通俗说法 | What it actually means / 实际含义 |
|------|----------------|------------------------|
| PagedAttention | "the KV trick" / "KV 技巧" | Fixed-size block allocator for KV cache; fragmentation <4% / KV 缓存的固定大小块分配器；碎片率 <4% |
| Block table | "the page table" / "页表" | Per-sequence map from logical token position to physical KV block / 每序列的逻辑 token 位置到物理 KV 块的映射 |
| Continuous batching | "dynamic batching, but right" / "正确的动态批处理" | Admit/release decisions made every decode iteration / 每个解码迭代做出接纳/释放决策 |
| Chunked prefill | "prefill splitting" / "预填充切片" | Break long prefill into 512-token slices interleaved with decode / 将长预填充切为 512 token 片段与解码交错 |
| TTFT | "first token time" / "首 token 时间" | Prefill + queue + network; dominated by prefill at long prompts / 预填充+队列+网络；长提示时由预填充主导 |
| ITL | "inter-token latency" / "token 间延迟" | Time between consecutive decode tokens; dominated by batch size / 连续解码 token 之间的时间；由批次大小主导 |
| Goodput | "throughput that meets SLO" / "满足 SLO 的吞吐量" | Tokens/sec where every request still hit TTFT and ITL targets / 每秒 token 数，每个请求仍满足 TTFT 和 ITL 目标 |
| V1 scheduler | "the new scheduler" / "新调度器" | vLLM's 2026 scheduler; N-gram spec decode is the chunked-prefill-compatible path / vLLM 2026 调度器；N-gram 推测解码与分块预填充兼容 |
| `--gpu-memory-utilization` | "the memory knob" / "内存旋钮" | Fraction of HBM reserved for KV blocks after weights and activations / 加载权重和激活后为 KV 块预留的 HBM 比例 |

## Xem thêm 延伸阅读

- [vLLM documentation — Speculative Decoding](https://docs.vllm.ai/en/latest/features/spec_decode/) nguồn chính thức về tính tương thích của prefill và decoding đầu cơ.
- [vLLM Release Notes (NVIDIA)](https://docs.nvidia.com/deeplearning/frameworks/vllm-release-notes/index.html) 2026 phát hành chuỗi và hành vi cụ thể cho phiên bản.
- [vLLM Blog — PagedAttention](https://blog.vllm.ai/2023/06/20/vllm.html) bản viết ban đầu vẫn xác định cách suy nghĩ về người phân bổ.
- [PagedAttention paper (arXiv:2309.06180)](https://arxiv.org/abs/2309.06180) Phân tích phân mảnh và thiết kế lập lịch trình.
- [Aleksa Gordic — Inside vLLM](https://www.aleksagordic.com/blog/vllm) trình lập lịch V1 chi tiết đi qua với biểu đồ lửa.
