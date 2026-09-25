# Load Testing LLM API  Tại sao k6 và chấy dối  tải test API Tại sao LLM  Mỹ

> Các máy kiểm tra tải trọng truyền thống không được thiết kế cho các phản ứng phát trực tuyến, độ dài đầu ra biến, số liệu cấp token hoặc độ bão hòa GPU. Hai cái bẫy đâm hầu hết đội. Trạm GIL: Đo lường cấp token của Locust chạy token hóa dưới Python GIL, cạnh tranh với việc tạo yêu cầu trong sự đồng thời nặng; backlog token hóa sau đó làm tăng độ trễ giữa các token được báo cáo. Trạm đồng nhất định nhanh: các lệnh đồng nhất trong vòng lặp kiểm tra một điểm trên phân phối token; lưu lượng thực có chiều dài thay đổi và sự phù hợp của tiền tố khác nhau. LLMPerf sửa chữa điều này với `--mean-input-tokens`+ `--stddev-input-tokens`. Định hướng công cụ vào năm 2026: chuyên ngành LLM (GenAI-Perf, LLMPerf, LLM-Locust, guidellm) cho độ chính xác ở mức token; **k6 v2026.1.0**+ **k6 Operator 1.0 GA (Sept 2025)** lưu trữ thông tin, Kubernetes bản địa phân phối thông qua các CRD TestRun / PrivateLoadZone, tốt nhất cho cổng CI / CD; Vegeta for Go saturation rate không đổi; Locust 2.43.3 chỉ với mở rộng LLM-Locust cho lưu trữ.

> **【中文解读】**Bài viết này giới thiệu LLM API  tải trọng test  đánh giá các dịch vụ thử nghiệm thực hiện dưới tải trọng cao 


**Type:** Build | **类型:** 学习
**Languages:** Python (stdlib, toy realistic-prompt generator + latency collector) | **语言:** Python
**Prerequisites:** Phase 17 · 08 (Inference Metrics), Phase 17 · 03 (GPU Autoscaling) | **前置知识:** Phase 17 · 08 (Inference Metrics), Phase 17 · 03 (GPU Autoscaling)

>  **【前置】**学本节前请先掌握:Phase 17·08(指标) 、Phase 17·03(GPU 扩缩) 。
>  **【类比】**LLM  tải trọng test = "测自动驾驶 vs 测传统车"──两个陷:(1) GIL 陷:Locust 在 Python GIL 下做代币化,与请求生成抢锁→报告的代币 间延迟虚高(客户端是瓶不是服务端);(2) 快速 一致性陷:循环相同 快速只测分布一个点,真流量有多样化前匹配──LLMPerf 用`--mean-input-tokens+stddev`修复──2026 工具:GenAI-Perf/LLMPerf/LLM-Locust(LLM 专用) + k6 v2026.1(流式+K8s) + Vegeta(Go 常速率) + Locust(仅配 LLM-Locust 扩展)
**Time:** ~75 minutes | **时间:** ~75 minutes

## Mục tiêu học tập

- Giải thích hai kiểu chống (trầm GIL, cái bẫy đồng nhất nhanh) khiến các nhà kiểm tra tải trọng chung nói dối cho API LLM.
  Trung文翻译:解释两个反模式 (GIL 陷、提示均性陷), chúng làm cho các công cụ thử nghiệm tải trọng phổ biến gây ra sai hướng.
- Chọn một công cụ cho một mục đích nhất định: LLMPerf (động cơ chuẩn), k6 + mở rộng phát trực tuyến (cổng CI), guidellm (sản phẩm tổng hợp quy mô lớn), GenAI-Perf (chỉ lục NVIDIA).
  中文翻译:选择工具Harness、LitmusChaos、Chaos Mesh根据技术。
- Thiết kế bốn mô hình tải (năng thẳng, trượt, đập, ngâm) và đặt tên chế độ thất bại mỗi lần bắt.
  Trung ngữ翻译:设计四种负载模式 (tạm dịch: 设计四种负载模式) và nói ra mỗi loại 障碍模式.
- Xây dựng phân phối nhanh thực tế bằng cách sử dụng trung bình + stddev của các token đầu vào thay vì chiều dài cố định.
  Trung文翻译: sử dụng nhập mã thông báo của trung bình giá trị + 标准差构建真实提示分布,而非固定长度──

## Vấn đề  vấn đề giới thiệu

> **【中文解读】**Các công cụ thử nghiệm tải trọng truyền thống không được thiết kế cho LLM  chúng không hỗ trợ dòng phản ứng、 có thể thay đổi đầu ra độ dài、tốc độ  và độ GPU  và độ。 hai câu lạc bộ thường gặp:(1) GIL 

> **【拓展：LLM 负载测试的四种模式】**Năm 2026 LLM  tải test của bốn mô hình: 1) ổn định (stable-state) 恒定 RPS 持续 30-60 phút, bắt đầu hiệu suất giảm; 2) 渐增 (ramp)  từ 0 线性增加到目标 RPS, bắt đầu dung lượng断点和预热异常; 3) 突发 (spike) 突然 3-10x RPS 持续 2 phút rồi quay lại,测试自动扩张响应,队列和和冷启动影响; 4) 时间 (soak) 稳定 (stable) 持续 4-8小时,捕获内存漏,连接池漂移和可观测性溢出.

Bạn đã thử nghiệm điểm cuối của LLM của mình với 500 người dùng đồng thời. Nó đã được. Bạn đã vận chuyển. Trong sản xuất với 200 người dùng thực tế dịch vụ rơi trên P99 TTFT nổ, GPUs bị gắn.

Thứ nhất, k6 gửi 500 lời nhắc giống nhau  việc thu thập yêu cầu và lưu trữ trước tiên của bạn làm cho nó trông giống như bạn đang xử lý 500 mã giải mã đồng thời khi bạn thực sự xử lý một. Thứ hai, k6 không theo dõi độ trễ giữa các mã thông báo trên các phản ứng phát trực tuyến theo cách mà mắt trải nghiệm nó; nó thấy một kết nối HTTP, không phải 500 mã thông báo đến với khoảng thời gian khác nhau.

Kiểm tra tải trọng cho LLM là kỷ luật của riêng nó.

## Khái niệm cốt lõi

### Trầm gẫy GIL (Locust)

> **【拓展：Python GIL 对 LLM 负载测试的影响】**Python GIL(全局解释器锁) ảnh hưởng đến các bài kiểm tra tải trọng của LLM:Locust sử dụng Python 运行客户端分词,在高并发时代代码化 队列排在请求生成后面。 báo cáo 延迟包含客户端代码化 积压你以为是服务器慢,其实是测试工具的瓶──解决方案:(1) LLM-Locust 扩展将代码化 移动到独立进程;(2) 使用编译语言工具k6(Go) MPerf(Rust-backed tokenizers.rs)。 Đây là một trong những rào cản phổ biến nhất trong các bài kiểm tra tải trọng của LLM.

Locust sử dụng Python và chạy phần mềm token hóa bên khách hàng dưới GIL. Trong thời gian đồng thời cao, các hàng đầu token hóa đứng sau việc tạo ra yêu cầu.

Giải quyết: LLM-Locust mở rộng di chuyển token hóa thành các quy trình riêng biệt, hoặc sử dụng một vòng xoắn ngôn ngữ được biên soạn (k6, LLMPerf sử dụng tokeners.rs).

### Mẫy đồng nhất nhanh chóng

Tất cả các trình kiểm tra tải được biết đến cho phép bạn cấu hình một prompt. Trong một thử nghiệm vòng lặp 10.000 lần lặp lại cùng một prompt gửi mỗi lần. Server thấy cùng một dấu tiền mỗi khi  dấu tiền đề cache chạm gần 100%, thông suất trông tuyệt vời.

Phác định: mẫu từ phân phối nhanh.`--mean-input-tokens 500 --stddev-input-tokens 150` độ dài khác nhau, nội dung khác nhau.

### Bốn mô hình tải

1. **Steady-state** RPS liên tục trong 30-60 phút.
2. **Ramp** tăng RPS theo tuyến tính từ 0 đến mục tiêu trong 15 phút.
3. **Spike** đột ngột 3-10x RPS trong 2 phút sau đó quay lại.
4. **Soak** trạng thái ổn định trong 4-8 giờ.

### 2026 thiết bị lập bản đồ

> **【中文解读】**2026 năm LLM 负载测试工具选择:(1) LLMPerf(Anyscale)Rust-backed 分词 + 流式感知,性能测试的默认选择;(2) NVIDIA GenAI-PerfNVIDIA 参考工具,注意其 ITL 不含 TTFT;(3) LLM-Locust(TrueFoundry)Locust 扩展,修复 GIL 问题;(4) k6 v2026.1.0 + k6 Operator 1.0 GA(2025 年 9 月) Go编译、无 GIL、流式、知感ernetes-native 分布测试,CI/CD gate 最佳选择──

> **【拓展：CI/CD 中的 SLA Gate】**Trong CI sử dụng cửa SLA của k6 配置: mỗi lần PR 运行 30-50 次代,gate 指标包括 P50/P95 TTFT、5xx < 5%、TPOT 在值以下──违规构建失败──使用真实提示分布(mean + stddev of input tokens) thay vì cố định长度LLMPerf 使用`--mean-input-tokens 500 --stddev-input-tokens 150`生成多样化提示

**LLMPerf**(Anyscale)  Python nhưng hỗ trợ token hóa Rust. Mean / stddev yêu cầu.

**NVIDIA GenAI-Perf** NVIDIA tham chiếu. Sử dụng khách hàng Triton; bao gồm cả các metric. Lưu ý ITL của nó không bao gồm TTFT; LLMPerf của nó. Hai công cụ tạo ra TPOT khác nhau cho cùng một máy chủ.

**LLM-Locust**(TrueFoundry)  Lễ mở rộng chấy rắc câu bẫy GIL.

**guidellm** Phân tích phân tích tổng hợp quy mô lớn.

**k6 v2026.1.0**+ **k6 Operator 1.0 GA (Sept 2025)**- Có thể là:
- k6 chính nó (Go, biên soạn, không có GIL) thêm các métrics biết streaming.
- k6 Nhà điều hành sử dụng các CRD TestRun / PrivateLoadZone cho các thử nghiệm phân tán gốc Kubernetes.
- Tốt nhất cho các cổng CI / CD và kiểm tra SLA.

**Vegeta** Go, đơn giản hơn k6. Nồng độ HTTP liên tục. Không có ý thức LLM nhưng tốt cho các thử nghiệm gateway / giới hạn tốc độ.

**Locust 2.43.3 stock** có cái bẫy GIL cho LLM. Chỉ với LLM-Locust mở rộng.

### Cổng SLA trong CI

Đi k6 trên PR với:

- 30-50 lần lặp mỗi lần ở RPS cơ bản.
- Cổng: P50/P95 TTFT, 5xx < 5%, TPOT dưới ngưỡng.
- Đánh phá sự cố.

### Phân phối nhanh chóng thực tế

Xây dựng từ các mẫu lưu lượng thực (nếu bạn có chúng) hoặc từ các phân phối được xuất bản (ví dụ, ShareGPT yêu cầu cho trò chuyện, HumanEval cho mã). Đưa trung bình + stddev đến LLMPerf. Tránh vòng với một yêu cầu với mọi giá.

### Những con số mà bạn nên nhớ

- k6 Nhà điều hành 1.0 GA: Tháng 9 năm 2025.
- k6 v2026.1.0: Métric nhận thức về streaming.
- Tiêu chuẩn LLMPerf chạy: 100-1000 yêu cầu tại đồng thời X.
- Cổng CI điển hình: 30-50 lần lặp mỗi PR.
- Bốn mô hình: ổn định, trượt, đòn, ngâm.

## Hãy sử dụng nó để thực hiện
```figure
load-pattern-waves
```

## Sử dụng nó

`code/main.py`mô phỏng một thử nghiệm tải với phân phối nhanh thực tế, đo TPOT hiệu quả và chứng minh cái bẫy nhanh đồng nhất.

> `code/main.py`mô phỏng một thử nghiệm tải với phân phối nhanh thực tế, đo TPOT hiệu quả và chứng minh cái bẫy nhanh đồng nhất.

> `code/main.py`mô phỏng một thử nghiệm tải với phân phối nhanh thực tế, đo TPOT hiệu quả và chứng minh cái bẫy nhanh đồng nhất.

## Chuyển nó đi.

Bài học này sẽ mang lại kết quả `outputs/skill-load-test-plan.md`Với khối lượng công việc và SLA, chọn công cụ và thiết kế bốn mô hình tải.

> 本课产 出 `outputs/skill-load-test-plan.md`Với khối lượng công việc và SLA, chọn công cụ và thiết kế bốn mô hình tải.

## Tập luyện bài tập

1. Đi chạy`code/main.py`So sánh phân bố đồng nhất với phân bố thực tế  khoảng cách ở đâu?
   Trung ngữ翻译:运行 `code/main.py`◊ So sánh trung bình so với phân bố thực sự P99 TTFT 差异在哪里?
2. Viết kịch bản k6 cho cổng CI: TTFT P95 < 800 ms ở 100 đồng thời, thời gian chạy 5 phút.
   Trung文翻译:编写 CI 门控的 k6 脚本:100 并发下 TTFT P95 < 800ms,运行 5 分钟──
3. Thử nghiệm ngâm của bạn cho thấy bộ nhớ tăng lên 50 MB/giờ. Hãy cho biết ba nguyên nhân và dụng cụ để chọn giữa chúng.
   Trung ngữ翻译:Your Immersion Test Show内存 tăng 50MB mỗi giờ.
4. Kiểm tra Spike từ 10 RPS đến 100 RPS. Thời gian phục hồi dự kiến là bao nhiêu nếu các sản phẩm vLLM Karpenter + vLLM được triển khai (Phase 17 · 03 + 18)?
   Trung ngữ翻译: Từ 10 RPS 尖峰测试到100 RPS── Nếu Karpenter 需要45秒供应,预期恢复时间是多少?
5. GenAI-Perf báo cáo TPOT=6ms; LLMPerf báo cáo TPOT=11ms trên cùng một máy chủ.

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| LLMPerf | "the LLM harness" | Anyscale benchmark tool, streaming-aware |
| GenAI-Perf | "NVIDIA tool" | NVIDIA reference harness |
| LLM-Locust | "Locust for LLMs" | Locust extension fixing GIL trap |
| guidellm | "synthetic benchmark" | Large-scale synthetic tool |
| k6 Operator | "K8s k6" | CRD-based distributed k6 |
| GIL trap | "Python client overhead" | Tokenization backlog inflates reported latency |
| Prompt-uniformity trap | "single-prompt lie" | Loop with same prompt hits cache, inflates throughput |
| Steady-state | "constant load" | Flat RPS for N minutes |
| Ramp | "linear up" | 0 to target over duration |
| Spike | "burst test" | Sudden multiplier then revert |
| Soak | "long test" | Hours for leak detection |

## Xem thêm 延伸阅读

- [TianPan — Load Testing LLM Applications](https://tianpan.co/blog/2026-03-19-load-testing-llm-applications)
- [PremAI — Load Testing LLMs 2026](https://blog.premai.io/load-testing-llms-tools-metrics-realistic-traffic-simulation-2026/)
- [NVIDIA NIM — Introduction to LLM Inference Benchmarking](https://docs.nvidia.com/nim/large-language-models/1.0.0/benchmarking.html)
- [TrueFoundry — LLM-Locust](https://www.truefoundry.com/blog/llm-locust-a-tool-for-benchmarking-llm-performance)
- [LLMPerf](https://github.com/ray-project/llmperf)
- [k6 Operator](https://github.com/grafana/k6-operator)
