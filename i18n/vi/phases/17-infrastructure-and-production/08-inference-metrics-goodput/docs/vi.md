# TTFT, TPOT, ITL, Goodput, P99  推理指标 Goodput

> Bốn số liệu quyết định liệu việc triển khai suy luận có hiệu quả hay không. TTFT là prefill cộng với queue cộng với mạng. TPOT (tương đương ITL) là chi phí giải mã liên quan đến bộ nhớ mỗi token. Thời gian trễ cuối đến cuối là TTFT cộng với TPOT lần chiều dài đầu ra. Tạo thông là các token mỗi giây được tổng hợp trên toàn bộ hạm đội. Nhưng điều quan trọng đối với sản phẩm là goodput  phần nhỏ của các yêu cầu đáp ứng tất cả SLO cùng một lúc. Tăng suất cao với goodput thấp có nghĩa là bạn đang xử lý token mà không bao giờ đạt đến người dùng đúng giờ. Số tham chiếu cho Llama-3.1-8B-Instruct trên TRT-LLM vào năm 2026: trung bình TTFT 162 ms, trung bình TPOT 7,33 ms, trung bình E2E 1,093 ms. Luôn báo cáo P50, P90, P99  không bao giờ chỉ là xấu. Và xem cái bẫy đo: GenAI-Perf loại trừ TTFT khỏi tính toán ITL, LLMPerf bao gồm nó; hai công cụ không đồng ý về TPOT cho cùng một chạy.

> **【中文解读】**Bài viết này giới thiệu các chỉ số quan trọng về chất lượng dịch vụ và Goodput
**Type:** Learn
**Languages:** Python (stdlib, toy percentile calculator and goodput reporter)
**Prerequisites:** Phase 17 · 04 (Serving Engine Internals)
**Time:** ~60 minutes


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy percentile calculator and goodput reporter) | **语言:** Python（标准库，百分位计算器和 Goodput 报告器）
**Prerequisites:** Phase 17 · 04 (vLLM Serving Internals) | **前置知识:** Phase 17 · 04（vLLM 服务内部）

>  **【前置】**学本节前请先掌握:Phase 17·04(vLLM) 统计基础(百分位) ・・・推理指标四件套:TTFT(首代币 时间) + TPOT(每代币 时间) + 吞吐量 + Goodput。
>  **【类比】**推理指标 = "餐厅 KPI"。TTFT = 顾客坐下第一道菜上桌(prefill+queue+network);TPOT = 后续每道菜间隔(解码成本);吞吐量 = 餐厅 mỗi giờ ra ngoài bữa ăn tổng số;Goodput = 满足所有SLO yêu cầu tỷ lệ (关键!)。陷:高吞吐低 Goodput = đã làm rất nhiều món ăn nhưng khách hàng không có giá trị khi ăn đến。 phải báo cáo P50/P90/P99 không thể chỉ báo trung bình。GenAI-Perf và LLMPerf đối với TPOT 口径 khác nhau cùng một vận hành kết quả sẽ xung đột。
**Time:** ~60 minutes | **时间:** ~60 分钟

## Mục tiêu học tập

- Định nghĩa chính xác TTFT, TPOT, ITL, E2E, thông suất và goodput và đặt tên thành phần mỗi phép đo.
  Trung文翻译:精确定义 TTFT、TPOT、ITL、E2E、吞吐量和 Goodput,并说出每个指标测量的组件──
- Giải thích tại sao trung bình là số liệu thống kê sai lầm cho việc phục vụ LLM và cách đọc P50/P90/P99.
  Trung ngữ翻译:解释为什么平均值是 LLM 服务的错统计量,以及如何阅读P50/P90/P99──
- Xây dựng một SLO đa hạn chế (ví dụ: TTFT <500 ms Và TPOT <15 ms Và E2E <2 s) và tính toán hiệu suất tốt với nó.
  中文翻译:构造 SLO 多约束(如 TTFT<500ms 且TPOT<15ms 且E2E<2s)并据此计算 Goodput。
- Hãy nêu tên hai công cụ chuẩn mà không đồng ý về TPOT cho cùng một mục đích và giải thích lý do tại sao.
  Trung ngữ翻译: nói出两个在同一运行中对TPOT产生不同结果的基准测试工具并解释原因──

## Vấn đề  vấn đề giới thiệu

> **【中文解读】**推理服务有多个延迟轴,每个轴以不同方式失败──预先是计算有限的,随提示长度增长;Decode是内存有限的,随批量 增长;排队延迟是运维问题;网络是物理距离问题──需要不同的指标来衡量每个维度,需要百分数,还需要一个综合指标说"用户是否得到预期的体验"这就是Goodput──

> **【拓展：LLM 推理指标体系】**Hệ thống chỉ số đầy đủ của LLM 推理 bao gồm: 1) TTFT 首代币 延迟) 用户感知到的首次响应时间; 2) TPOT/ITL(每代币 延迟/inter-token 延迟) 流式输出平滑度; 3) E2E(端到端延迟) 从请求到完成的总时间; 4) 吞吐量 (吞吐量) 集群效率指标; 5) Goodput (有效吞吐) 同时满足所有 SLA 请求比例;;ML已Perf Inference v6.0  Goodput 作为官方提交指标.

"Tổng thông qua của chúng tôi là 15.000 token mỗi giây". Vậy thì sao? Nếu 40% yêu cầu vượt quá 2 giây từ đầu đến cuối, người dùng đã bỏ cuộc. Chỉ riêng thông qua không cho bạn biết sản phẩm có hoạt động hay không.

> "Tổng thông tin của chúng tôi là 15.000 token mỗi giây. "Tại sao? Nếu 40% yêu cầu kết thúc hơn 2 giây, người dùng sẽ từ bỏ cuộc họp.

Inference có nhiều trục độ trễ và mỗi trục thất bại khác nhau. Prefill là tính toán và cân bằng với độ dài nhanh chóng. Việc giải mã là kết nối với bộ nhớ và quy mô với kích thước lô. Lễ xếp hàng là một vấn đề hoạt động. Mạng lưới là vấn đề về khoảng cách vật lý. Bạn cần các số liệu riêng biệt cho mỗi người, và bạn cần percentiles, và bạn cần một đơn vị đơn hợp nhất nói "có người dùng nhận được những gì họ mong đợi" đó là tốt.

> 推理 có nhiều vòng trục chậm, mỗi vòng trục thất bại theo cách khác nhau. 预填是计算限制的,随提示长度增长的. 解码是内存限制的,随批次大小增长的. 排列延迟是运维问题. 网络是物理距离问题. 你需要每个维度不同的指标,需要百分数,还需要一个综合指标说"用户是否得到预期的体验"这是Goodput.

## Khái niệm cốt lõi

### TTFT  thời gian để token đầu tiên

> **【中文解读】**TTFT = queue_time + network_request + prefill_time。Prefill 在长提示时占主导32K prompt 在 Llama 3.3 70B FP8 H100 上需要约800ms的纯预填──排队时间是调度器的行为,网络请求包括 TLS 的线缆时间──TTFT 是用户在流式返回任何内容之前感知到的延迟──

`TTFT = queue_time + network_request + prefill_time`

Prefill chiếm ưu thế khi các yêu cầu dài. Trên Llama-3.3-70B FP8 trên H100, một yêu cầu 32k mất ~ 800 ms prefill tinh khiết. Thời gian xếp hàng là hành vi lập trình khi tải. yêu cầu mạng là thời gian dây bao gồm TLS. TTFT là thời gian trễ người dùng thấy trước khi bất cứ thứ gì phát lại.

> 预充在长提示时占主导──Llama-3.3-70B FP8 在 H100 上,32K提示需要约800ms的纯预充──排队时间是调度器的行为──网络请求是包括TLS的线缆时间──TTFT是用户在任何内容流式返回前感知到的延迟──

### TPOT / ITL  độ trễ giữa các token

> **【中文解读】**TPOT(thời gian mỗi token đầu ra) = ITL(thời gian trễ giữa các token) = thời gian trễ giải mã mỗi token。公式:TPOT = (decode_forward_time + scheduler_overhead) / tokens_produced。在 Llama 3.3 70B H100 + 分块预填充下,TPOT 均值约 7ms;无分块预填时,在长预填 邻居序列期间 TPOT 可升至50ms。永远监控 P99 而非均值。

Nhiều tên cho một số lượng.`TPOT`(giờ mỗi token đầu ra), `ITL`(tạm thời giữa các mã thông báo),`decode latency per token` tất cả đều. Đó là thời gian giữa các token được phát liên tiếp sau đầu tiên.

> Một số lượng nhiều tên gọi.`TPOT`(per输出 token 时间)`ITL`(trong mã thông báo 延迟)`每 token 解码延迟`都是同一个──它是第一个标志 之后连续流式标志 间的时间──

`TPOT = (decode_forward_time + scheduler_overhead) / tokens_produced`

Trên cùng một đống Llama-3.3-70B H100 với prefill chia nhỏ, TPOT trung bình là ~ 7 ms. Không prefill chia nhỏ, trong một prefill dài trên một chuỗi lân cận, TPOT có thể tăng lên 50 ms. Watch P99, không trung bình.

> Trong cùng Llama-3.3-70B H100  tăng phân khối dự trữ, TPOT 平均值约7ms──无分块预充时, trong quá trình dự trữ dài của hàng xóm, TPOT có thể tăng lên 50ms──关注 P99, không phải là trung bình.

### E2E latency

`E2E = TTFT + TPOT * output_tokens + network_response`

Đối với các đầu ra dài (> 500 token), E2E là TPOT thống trị. Đối với các đầu ra ngắn với các lời nhắc dài, E2E là TTFT thống trị.

> Đối với dài输出(>500 token),E2E bởi TPOT 主导── đối với dài提示的短输出,E2E bởi TTFT 主导── báo cáo按输出长度分条件的E2E──

### Tải thông

`throughput = total_output_tokens / elapsed_time`

Chỉ số tổng hợp cho bạn hiệu quả của hạm đội, không cho bạn biết sức khỏe yêu cầu cá nhân.

> 聚合指标―― nói với bạn hiệu quả tập hợp―― không nói với bạn tình trạng sức khỏe đơn lẻ của yêu cầu――

### Goodput  số liệu bạn thực sự quan tâm đến

> **【中文解读】**Goodput là chỉ số tổng hợp duy nhất thực sự quan trọng. SLO là một yêu cầu chỉ được đáp ứng đồng thời TTFT <= a、TPOT <= b、E2E <= c 才算"好"。 High throughput ở 60% Goodput 时是失败; Low throughput ở 99% Goodput 时才是目标。 2026 năm MLPerf Inference v6.0 和 AI 平台供应商内部 SLA 追踪都以 Goodput 为核心指标──

`goodput = fraction of requests meeting (TTFT <= a) AND (TPOT <= b) AND (E2E <= c)`

SLO là một hạn chế đa. Một yêu cầu chỉ "tốt" nếu mỗi hạn chế được đáp ứng. Goodput là phần. Tốc suất cao với 60% goodput là thất bại. Tốc suất thấp hơn với 99% goodput là mục tiêu.

> SLO là nhiều hạn chế. Chỉ khi tất cả các hạn chế được đáp ứng, yêu cầu là "tốt" của.

Năm 2026, goodput là số liệu được sử dụng trong các bài đăng MLPerf Inference v6.0 và theo dõi SLA nội bộ tại các nhà cung cấp nền tảng AI.

> 2026 年,Goodput 是 MLPerf Inference v6.0 提交和AI 平台提供商内部 SLA 追踪使用的指标──

### Tại sao số liệu thống kê sai là xấu

> **【中文解读】**LLM 延迟分布是右偏的──一个包含长预填 邻居的解码批可能发发出 500 个 TPOT ~7ms的代币 和 20 个 TPOT ~60ms的代币──平均值 TPOT là 9ms, nhưng P99 TPOT là 65ms──用户经常遇到 P99这是他们离开的原因──永远报告三元组(P50, P90, P99), đối với trải nghiệm người dùng, P99 là cần tối ưu hóa mục tiêu──

Các phân phối độ trễ LLM là phải. Một loạt mã hóa với một hàng xóm dài có thể gửi 500 token với TPOT ~ 7 ms và 20 token với TPOT ~ 60 ms. TPOT trung bình là 9 ms. P99 TPOT là 65 ms. Người dùng thường xuyên nhấn P99 đó là lý do tại sao họ rời đi.

> LLM 延迟分布是右偏的──一个包含长预填充邻居的解码批次可以发发出500 个 TPOT 约7ms的代币和20 个 TPOT 约60ms的代币──平均值 TPOT 是9ms──P99 TPOT 是65ms──用户经常遇到P99这是他们离开的原因──

Luôn báo cáo ba (P50, P90, P99). Đối với trải nghiệm người dùng, P99 là một bạn tối ưu hóa.

> 始终报告三元组(P50、P90、P99)。 Đối với trải nghiệm người dùng,P99 là bạn cần được cải thiện。

### Số tham chiếu  Llama-3.1-8B-Instruct on TRT-LLM, 2026

- TTFT trung bình: 162 ms
  Trung ngữ翻译:均值 TTFT:162ms
- TPOT trung bình: 7,33 ms
  Trung ngữ翻译:均值 TPOT:7.33ms
- trung bình E2E: 1,093 ms
  Trung文翻译:均值 E2E:1,093ms
- P99 TPOT: dao động từ 10-25 ms tùy thuộc vào cấu hình mua phần.
  Trung文翻译:P99 TPOT:10-25ms,取决于分块预填配置──

Đây là các điểm tham chiếu NVIDIA được công bố. Chúng thay đổi theo kích thước mô hình (70B sẽ cho thấy 3-5x), phần cứng (H100 vs B200 ~ 3x), và tải.

> Đây là dữ liệu tham khảo của NVIDIA. Chúng theo mô hình lớn.

### Trầm đo

> **【中文解读】**Hai công cụ kiểm tra cơ sở phổ biến nhất trong năm 2026 trên TPOT sẽ có kết quả khác nhau: NVIDIA GenAI-Perf sẽ loại bỏ TTFT từ ITL 计算中 loại trừ( từ token 2 开始),LLMPerf 包含 TTFT( từ token 1 开始)  cùng một yêu cầu(TTFT 500ms、100 输出 token、700ms decode),GenAI-Perf 报告 ITL=7.07ms,LLMPerf 报告 ITL=12.00ms。永远说明 sử dụng các công cụ nào,永远发布定义──

> **【拓展：LLM 基准测试工具生态】**2026 năm LLM 推理基准测试工具包括:(1) NVIDIA GenAI-PerfTriton 客户端,全面指标覆盖,ITL 不含TTFT;(2) LLMPerf(Anyscale)Rust-backed 分词,流式感知,含TTFT的ITL;(3) LLM-Locust(TrueFoundry)Locust 扩展,修复GIL 问题;4) guidelm大规模合成基准测试;5)((((6 v2026.1.0流式感知,Kubernetes-native──选择工具时要了解其ITL 定义差异──

Hai trong số các công cụ chuẩn 2026 được sử dụng nhiều nhất không đồng ý về TPOT cho cùng một chạy:

- **NVIDIA GenAI-Perf**: loại trừ TTFT từ tính toán ITL. ITL bắt đầu từ token 2.
  Trung ngữ翻译:**NVIDIA GenAI-Perf**Từ ITL 计算中排除 TTFT──ITL Từ thứ 2 个代币 开始──
- **LLMPerf**: bao gồm TTFT. ITL bắt đầu từ token 1.
  Trung ngữ翻译:**LLMPerf**:包含 TTFT──ITL Từ # 1 个标志 开始──

Đối với yêu cầu với TTFT 500 ms và 100 mã thông báo đầu ra trong 700 ms mã hóa tổng thể, GenAI-Perf báo cáo `ITL = 700/99 = 7.07 ms`, LLMPerf báo cáo `ITL = 1200/100 = 12.00 ms`Sự lựa chọn công cụ thay đổi số.

> Đối với một TTFT 500ms  100 输出 token  700ms 总解码的请求,GenAI-Perf 报告 `ITL = 700/99 = 7.07ms`,LLMPerf  báo cáo `ITL = 1200/100 = 12.00ms`❖ Công cụ chọn thay đổi số.

Luôn cho biết công cụ nào. Luôn công bố định nghĩa.

> 始终说明 sử dụng nào 始终发布定义──

### Xây dựng một SLO

> **【拓展：LLM SLO 设定参考】**2026 年推的消费级 70B 对话模型 SLO:TTFT P99 <= 800ms、TPOT P99 <= 25ms、E2E P99 <= 3s(<300 token 输出)、Goodput >= 99%。企业级 SLO 收紧 TTFT(200-400ms) nhưng放宽 E2E──测量方法:使用真流量或LLMPerf 合成流量(`--mean-input-tokens 800 --stddev-input-tokens 300 --mean-output-tokens 150`), mục tiêu 2x 峰值并发,运行 30-50 次代取百分位数──

Một SLO hợp lý đối với người tiêu dùng cho mô hình trò chuyện 70B vào năm 2026:

- TTFT P99 <= 800 ms.
  Trung文翻译:TTFT P99 <= 800ms(首代币 延迟上限)
- TPOT P99 <= 25 ms.
  Trung文翻译:TPOT P99 <= 25ms(每代币 延迟上限)
- E2E P99 <= 3 s cho <300 token output.
  中文翻译:E2E P99 <= 3s(<300 token 输出) 』
- Mục tiêu sản lượng tốt >= 99%.
  中文翻译:Goodput 目标 >= 99%。

Enterprise SLOs thắt chặt TTFT (200-400 ms) và thả E2E. Điểm là ghi lại chúng, đo cả ba và theo dõi hiệu suất tốt như một hợp chất duy nhất.

> 企业级 SLO 收紧 TTFT(200-400ms)并放宽 E2E──关键是要写下来、测量全部三、并将 Goodput 作为单一综合指标追踪──

### Cách đo

- Tiếp tục giao thông thực tế hoặc thực tế tổng hợp (LLMPerf với `--mean-input-tokens 800 --stddev-input-tokens 300 --mean-output-tokens 150`().
  Trung ngữ翻译:运行真实流量或逼真合成流量(LLMPerf 使用 `--mean-input-tokens 800 --stddev-input-tokens 300 --mean-output-tokens 150`(■)
- Mục tiêu 2x đồng thời điểm cao nhất cho chạy benchmark.
  Trung文翻译:基准测试运行目标为2倍峰值并发──
- Lên 30-50 lần lặp lại, lấy phần trăm của mẫu kết hợp.
  Trung文翻译:运行 30-50 次代,取合并样本的百分位数──
- Giới thiệu với tên công cụ, phiên bản công cụ, mô hình, phần cứng, đồng thời, phân phối nhanh chóng.
  Trung文翻译:发布时标注工具名、版本、模型、硬件、并发数、提示分布──

## Hãy sử dụng nó để thực hiện
```figure
throughput-latency
```

## Sử dụng nó

`code/main.py`là một máy tính tính hiệu suất đồ chơi. tạo ra phân phối độ trễ tổng hợp, áp dụng SLO, và tính hiệu suất tốt.

> `code/main.py`là một mô hình Goodput  máy tính. 生成合成延迟分布,应用 SLO,计算 Goodput.

## Chuyển nó đi.

> **【拓展：SLO 设定与 Goodput 门控】**Năm 2026 đề xuất 70B đối thoại mô hình SLO:TTFT P99 <= 800ms、TPOT P99 <= 25ms、E2E P99 <= 3s(<300 token 输出)、Goodput 目标 >= 99%。 doanh nghiệp cấp SLO 收紧 TTFT(200-400ms) nhưng放宽 E2E──关键实践:(1) Trong CI/CD cổng 部署 quyết định về giá trị Goodput chứ không phải lượng吞吐量;(2) sử dụng 2x 峰并发行基准测试;((((运行 30-50 lần取百分位数;(4) 发布时标工具名、版本、模型、硬件、发行数、代提示分布.

Bài học này sẽ mang lại kết quả `outputs/skill-slo-goodput-gate.md`Với khối lượng công việc và SLO, nó tạo ra một công thức chuẩn chuẩn CI/CD sẵn sàng mà các cổng triển khai trên goodput thay vì thông qua.

> 本课产 出 `outputs/skill-slo-goodput-gate.md` Được định nghĩa tải trọng công việc và SLO, nó tạo ra một chương trình thử nghiệm cơ sở của CI/CD về tình trạng, với Goodput chứ không phải dung lượng như một quy định kiểm soát.

## Tập luyện bài tập

1. Đi chạy`code/main.py`Làm thế nào để goodput thay đổi khi bạn củng cố P99 TPOT từ 30 ms đến 15 ms?
   Trung ngữ翻译:运行 `code/main.py` tạo có 1% phân bố sắc bén ở cuối phần  Khi P99 TPOT từ 30ms  sát đến 15ms  Khi Goodput  thay đổi như thế nào?
2. Một nhà cung cấp trích dẫn "15,000 tok/s trên Llama 3.3 70B H100". Hãy nêu tên ba câu hỏi để hỏi trước khi tin tưởng nó.
   Trung ngữ翻译:供应商报价"Llama 3.3 70B H100 上 15,000 tok/s"──在信任之前说出三个要问问题──
3. Tại sao việc lấp trước bằng mảnh bảo vệ P99 TPOT nhưng không có nghĩa là TPOT?
   Trung ngữ翻译:为什么分块预填充保护 P99 TPOT 但不保护平均值 TPOT?
4. Xây dựng một SLO tiêu dùng cho trợ lý giọng nói (tốc hiệu đầu tiên được nghe, không được đọc).
   Trung ngữ翻译:为语音助手构建消费级 SLO(首代标是听到而非读到) ―― कौन là chỉ số được nhìn thấy nhiều nhất đối với người dùng?
5. Đọc các tài liệu LLMPerf README và GenAI-Perf.
   Trung文翻译:阅读 LLMPerf README 和 GenAI-Perf 文档──找出工具在另外三个标志上的分歧──

## Từ khóa  Từ khóa nhanh chóng

| Term / 术语 | What people say / 通俗说法 | What it actually means / 实际含义 |
|------|----------------|------------------------|
| TTFT | "time to first token" / "首 token 时间" | Queue + network + prefill; dominated by prefill at long prompts / 队列+网络+预填充；长提示时由预填充主导 |
| TPOT | "time per output token" / "每输出 token 时间" | Memory-bound decode cost per token after first / 首个 token 后每 token 的内存受限解码成本 |
| ITL | "inter-token latency" / "inter-token 延迟" | Same as TPOT in most tools (not all — see GenAI-Perf) / 大多数工具中同 TPOT（非所有——见 GenAI-Perf） |
| E2E | "end to end" / "端到端" | TTFT + TPOT * output_len; response-side network on top / TTFT + TPOT * 输出长度；加上响应端网络 |
| Throughput | "tok/s" / "token 每秒" | Fleet efficiency; useless without latency percentiles / 集群效率；无延迟百分位数则无意义 |
| Goodput | "SLO-met rate" / "SLO 达标率" | Fraction of requests meeting every SLO constraint simultaneously / 同时满足所有 SLO 约束的请求比例 |
| P99 | "tail" / "尾部" | 1-in-100 worst-case latency; the user experience metric / 百分之一最差延迟；用户体验指标 |
| SLO multi-constraint | "the joint" / "联合约束" | AND of all three latency bounds; a request fails if any one is violated / 三个延迟界限的 AND；任一违反即失败 |
| GenAI-Perf vs LLMPerf | "the tool trap" / "工具陷阱" | Tools disagree on whether ITL includes TTFT / 工具在 ITL 是否包含 TTFT 上不一致 |

## Xem thêm 延伸阅读

- [NVIDIA NIM — LLM Benchmarking Metrics](https://docs.nvidia.com/nim/benchmarking/llm/latest/metrics.html) định nghĩa của TTFT, ITL, TPOT.
- [Anyscale — LLM Serving Benchmarking Metrics](https://docs.anyscale.com/llm/serving/benchmarking/metrics) Các định nghĩa và công thức đo lường thay thế.
- [BentoML — LLM Inference Metrics](https://bentoml.com/llm/inference-optimization/llm-inference-metrics) đo lường được áp dụng trên các triển khai thực tế.
- [LLMPerf](https://github.com/ray-project/llmperf) Định nghĩa chuẩn nguồn mở dựa trên Ray.
- [GenAI-Perf](https://github.com/triton-inference-server/perf_analyzer/blob/main/genai-perf/README.md) Công cụ chuẩn của NVIDIA.
- [MLPerf Inference](https://mlcommons.org/benchmarks/inference-datacenter/) chỉ số chuẩn dựa trên giá trị tốt được công nghiệp chấp nhận.
