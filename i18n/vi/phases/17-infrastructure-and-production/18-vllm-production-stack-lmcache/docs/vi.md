# VLLM sản xuất hàng đống với LMCache KV Thả ra .
# Sản xuất phục vụ Stack  KV Offloading và Cache-Aware Routing

> Một sản xuất phục vụ bộ định tuyến, động cơ và khả năng quan sát trong một triển khai Kubernetes và xử lý bộ nhớ cache KV như một nguồn tài nguyên có thể rời khỏi GPU. KV khi tải xuống lấy bộ nhớ cache KV ra khỏi bộ nhớ GPU và sử dụng lại trên các truy vấn và động cơ (CPU DRAM, sau đó đĩa / Ceph). Vàn sản xuất vLLM là sự triển khai tham chiếu; LMCache là lớp thả. VLLM 0.11.0 KV Offloading Connector (từ tháng 1 năm 2026) làm cho nó không đồng bộ và có thể cắm thông qua Connector API (v0.9.0+). Đường tải xuống thường được ẩn khỏi đường yêu cầu, mặc dù cache bị bỏ lỡ và các khuyến mãi có thể thêm độ trễ cuối đến cuối. LMCache có giá trị ngay cả khi không có tiền đề được chia sẻ khi GPU hết các khe KV, các yêu cầu trước có thể được khôi phục từ CPU thay vì tính lại prefill. Các điểm chuẩn được công bố trên 16x H100 (80GB HBM) trên 4 a3-highgpu-4g: khi cache KV vượt quá HBM, cả CPU gốc và LMCache cải thiện đáng kể thông qua; ở dấu chân KV thấp, tất cả các cấu hình phù hợp với đường cơ sở với chi phí trên nhỏ.

> **【中文解读】**Bài viết này giới thiệu vLLM                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
**Type:** Learn
**Languages:** Python (stdlib, toy KV-spill simulator)
**Prerequisites:** Phase 17 · 04 (Serving Engine Internals), Phase 17 · 06 (SGLang/RadixAttention)
**Time:** ~60 minutes


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy KV-spill simulator) | **语言:** Python
**Prerequisites:** Phase 17 · 04 (vLLM Serving Internals), Phase 17 · 06 (SGLang/RadixAttention) | **前置知识:** Phase 17 · 04 (vLLM Serving Internals), Phase 17 · 06 (SGLang/RadixAttention)

>  **【前置】**学本节前请先掌握:Phase 17·04(vLLM)、Phase 17·06(RadixAttention)。vLLM sản xuất-thống = K8s 部署参考,LMCache = KV offload đến CPU/磁盘。
>  **【类比】**LMCache = "GPU 内存搬家"──KV cache 装不下 HBM → 溢出到 CPU DRAM 再到磁盘──GPU 满时预先 请求可从 CPU 恢复(无需重算预填)──异步、对用户透明──即使无共享前也值──16x H100基准:KV 超HBM 时大幅升吞;低KV 占用时开销很小──
**Time:** ~60 minutes | **时间:** ~60 minutes

## Mục tiêu học tập

- Hình đồ các lớp vLLM sản xuất: bộ định tuyến, động cơ, KV offload, khả năng quan sát.
  Trung文翻译:绘制 vLLM sản xuất-stack 层次:路由器、引擎、KV 卸载、可观测性。
- Giải thích API KV Offloading Connector (v0.9.0+) và cách đường đi không đồng bộ 0.11.0 che giấu độ trễ của việc tải xuống.
  中文翻译:解释 KV Offloading Connector API(v0.9.0+) và 0.11.0 异步路径如何隐藏卸载延迟──
- Quantify khi LMCache CPU-DRAM giúp (KV > HBM) vs thêm overhead (KV đủ nhỏ để phù hợp với HBM).
  Trung文翻译:量化 LMCache CPU-DRAM 在何时有帮助(KV > HBM)vs 何时增加开销(KV 足够小可放进 HBM) ⋅
- Chọn giữa vLLM CPU gốc và kết nối LMCache cho hạn chế triển khai.
  Trung文翻译:给定部署约束, trong nguyên sinh vLLM CPU 卸载和 LMCache 连接器之间选择──

## Vấn đề  vấn đề giới thiệu

> **【中文解读】**vLLM 推理服务在高并发时 GPU HBM 占满,发生抢占事件请求被逐出、重新排队、同一个2K-token提示一分钟内被重新填充四次。GPU 计算花在冗余预填上,Goodput 远低于原始吞吐──添加更多 GPU 是线性成本,但CPU DRAM 很便宜一个插座有512GB+, mặc dù chậm hơn HBM 差几个数级,但对于"临时热"的KV Cache 足够──

> **【拓展：vLLM Production Stack 架构】**VLLM sản xuất-phát là Kubernetes 部署方案 năm 2026 đề xuất, chứa năm thành phần: 1) Router cache-aware(Phase 17·11), tiêu thụ KV 事件;(2) Động cơ vLLM công nhân, mỗi GPU hoặc mỗi TP / PP 组一个;(3) KV Cache 卸载LMCache 部署 hoặc sinh gốc kết nối;(4) 可观测性Prometheus + Grafana + OTel dấu vết;(5) 控制面面服务发现、配置、滚动更新──以 Helm + 运营商形式发布──((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((

Dịch vụ vLLM của bạn cho thấy GPU ở 100% HBM với các sự kiện ưu tiên bất cứ khi nào đồng thời tăng lên. Các yêu cầu được trục xuất, xếp hàng, và bạn tái dự kiến yêu cầu 2K-token cùng một lần bốn lần trong một phút. tính toán GPU được chi tiêu cho việc dự trữ dư thừa; Goodput thấp hơn rất nhiều so với thông qua nguyên liệu.

Thêm nhiều GPU chi phí theo đường thẳng. Thêm nhiều HBM không thể. Nhưng CPU DRAM rẻ  một ổ cắm có 512 GB + ở các thứ tự độ trễ của quy mô tồi tệ hơn HBM nhưng tốt cho bộ nhớ cache KV "nói tạm thời".

LMCache trích xuất bộ nhớ cache KV vào CPU DRAM để các yêu cầu được dự đoán phục hồi nhanh chóng, và các bộ nhớ trước lặp đi lặp lại trên các động cơ chia sẻ bộ nhớ cache mà không cần mỗi động cơ tái lấp đầy.

## Khái niệm cốt lõi

### Vòng sản xuất vLLM

`github.com/vllm-project/production-stack`là việc triển khai Kubernetes tham chiếu:

- **Router** cache-aware (Phase 17 · 11).
- **Engines** nhân viên vLLM. Một người cho mỗi GPU hoặc cho mỗi nhóm TP/PP.
- **KV cache offload** LMCache triển khai hoặc kết nối bản địa.
- **Observability** Prometheus scrape, bảng điều khiển Grafana, dấu vết OTel.
- **Control plane** phát hiện dịch vụ, cấu hình, cập nhật.

Được chuyển như là người vận hành Helm chart +.

### KV Kloading Connector API (v0.9.0+)

vLLM 0.9.0 đã giới thiệu một Connector API cho các backend cache KV có thể cắm. Máy động của bạn tháo các khối vào kết nối; kết nối lưu trữ chúng (RAM, đĩa, lưu trữ đối tượng, LMCache).

vLLM 0.11.0 (từ tháng 1 năm 2026) thêm một đường thoát không đồng bộ  thoát tải có thể xảy ra trong nền để động cơ không bị chặn trên nó trong trường hợp thông thường. Sự trễ và thông qua cuối đến cuối vẫn phụ thuộc vào hình dạng tải trọng công việc, tỷ lệ hit cache KV và áp lực hệ thống; ghi chú của vLLM cho biết rằng việc tải xuống lõi tùy chỉnh có thể làm giảm thông qua ở tỷ lệ hit thấp và lập trình đồng bộ đã biết các vấn đề tương tác với giải mã phỏng đoán.

### Native CPU offload vs LMCache

> **【中文解读】**两种KV Cache 卸载方案对比:(1) 原生 vLLM CPU 卸载引擎本地,存储KV块到主机 RAM,实现快速,零网络跳转,但不跨引擎共享;(2) LMCache 连接器集群级,存储块到共享LMCache 服务器(CPU DRAM + Ceph/S3 压层), bất kỳ động cơ nào đều truy cập được.

**Native vLLM CPU offload**: động cơ-địa phương. lưu trữ các khối KV trong RAM chủ. nhanh để thực hiện, không tăng mạng. Không vượt qua động cơ.

**LMCache connector**Các khối được truy cập bởi bất kỳ động cơ nào. 16x H100 tham chiếu được công bố.

Chọn bản địa khi một động cơ duy nhất có áp suất HBM. Chọn LMCache khi nhiều động cơ chia sẻ tiền đề (RAG với các yêu cầu hệ thống chung, multi-tenant với các mẫu được chia sẻ).

### Hành vi đánh giá

> **【拓展：LMCache 基准测试数据】**LMCache trên 16x H100(80GB HBM) xuyên 4 个 a3-highgpu-4g 的基准测试表现:(1) 低KV 足迹(短提示、低并发) 所有配置匹配基线,LMCache 增加~3-5% 开销;(2) 中等足迹LMCache 开始在前复用方面提供帮助;(3) KV 超过 HBM原生 CPU 卸载和LMCache 都有改善吞吐,LMCache 因引擎共享收益更大.

H100 16x (80 GB HBM) trải rộng trên 4 thử nghiệm a3-highgpu-4g:

- KV thấp (các lời nhắc ngắn, đồng thời thấp): tất cả các cấu hình phù hợp với đường cơ sở, LMCache thêm ~ 3-5% chi phí chung.
- Hình ảnh vừa phải: LMCache bắt đầu giúp việc tái sử dụng tiền tố trên các động cơ.
- KV vượt quá HBM: CPU gốc và LMCache đều cải thiện thông suất đáng kể; LMCache tăng trưởng lớn hơn do chia sẻ đa động cơ.

### Khi LMCache là quyết định

> **【中文解读】**LMCache trong các trường hợp sau đây là quyết định:(1) 多租户服务系统提示跨租户共享;(2) RAG文档块跨查询重复;(3) 微调变体(LoRA) KV 复用减少冗余工作;(4) 抢占密集型工作负载从CPU 恢复比重新预填 更便宜;;不应启动场景:HBM 压力小(只有开销没有收益) 短上下文(<1K token,传输时间 > 重新预填) 单租户单单单无复用可捕获提示)

> **【拓展：KV Cache 卸载的集成】**Giai đoạn 17·17 phân chia dịch vụ + LMCache 协同效应: chuyển từ prefill 池 đến decode 池 của KV nếu không ngay lập tức sử dụng, có thể lưu vào LMCache; truy vấn tiếp theo từ LMCache 拉取而不是重新 prefill。 Giai đoạn 17·11 của bộ định tuyến có tính cache có thể được chuyển đến địa phương hoặc LMCache chia sẻ bộ nhớ phù hợp với động cơ。 vLLM 0.11.0 ((1 tháng 1 năm 2026) thêm các bước khác nhau để tải xuống đường trên trạm sau để thực hiện tải xuống, động cơ sẽ không bị chặn trong trường hợp thường xuyên。

- Dịch vụ nhiều người thuê nơi các thông báo hệ thống được chia sẻ giữa người thuê.
- RAG nơi các đoạn tài liệu lặp lại qua các truy vấn.
- Các biến thể được điều chỉnh tốt (LoRA) trên cùng một cơ sở khi sử dụng lại KV mô hình cơ bản cắt giảm công việc dư thừa.
- Nhiệm lượng công việc nặng trước: khôi phục từ CPU rẻ hơn so với tái đổ.

### Khi NOT để kích hoạt

- Giảm áp suất HBM nhỏ  bạn trả phí không có lợi ích.
- Các bối cảnh ngắn (< 1K token)  thời gian chuyển giao > tái lấp đầy.
- Lượng công việc đơn thuần của người thuê nhà  không sử dụng lại để chụp.

### Kết hợp với dịch vụ phân chia

Giai đoạn 17 · 17 phân chia dịch vụ + hợp chất LMCache: KV chuyển từ hồ chứa trước để giải mã đất hồ chứa trong LMCache nếu không được sử dụng; các truy vấn sau đó rút khỏi LMCache. Giai đoạn 17 · 11 bộ định tuyến nhận thức cache có thể định tuyến đến động cơ có tương ứng cache chia sẻ LMCache địa phương hoặc LMCache.

### Những con số mà bạn nên nhớ

- vLLM 0.9.0: Connector API được vận chuyển.
- vLLM 0.11.0 (Từ tháng 1 năm 2026): đường tải không đồng bộ; tác động độ trễ đầu đến cuối phụ thuộc vào tải công việc, tốc độ KV và áp suất hệ thống (không phải là một đảm bảo tuyệt đối).
- Định hướng 16x H100: LMCache giúp khi dấu chân KV vượt quá HBM.
- Áp suất HBM nhỏ: 3-5% chi phí trên không có lợi ích.

## Hãy sử dụng nó để thực hiện
```figure
zero-sharding
```

## Sử dụng nó

`code/main.py`mô phỏng tải trọng công việc nặng trước khi có và không có LMCache. báo cáo việc lấp đầy lại được tránh, tăng thông suất và việc sử dụng HBM bằng nhau.

> `code/main.py`mô phỏng tải trọng công việc nặng trước khi có và không có LMCache. báo cáo việc lấp đầy lại được tránh, tăng thông suất và việc sử dụng HBM bằng nhau.

> `code/main.py`mô phỏng tải trọng công việc nặng trước khi có và không có LMCache. báo cáo việc lấp đầy lại được tránh, tăng thông suất và việc sử dụng HBM bằng nhau.

## Chuyển nó đi.

Bài học này sẽ mang lại kết quả `outputs/skill-vllm-stack-decider.md`. Với hình dạng tải trọng công việc và triển khai vLLM, quyết định bản địa vs LMCache vs không.

> 本课产 出 `outputs/skill-vllm-stack-decider.md`. Với hình dạng tải trọng công việc và triển khai vLLM, quyết định bản địa vs LMCache vs không.

## Tập luyện bài tập

1. Đi chạy`code/main.py`LMCache bắt đầu trả tiền khi sử dụng HBM nào?
   Trung ngữ翻译:运行 `code/main.py`LMCache bắt đầu lập kế hoạch dưới mức sử dụng HBM nào?
2. Một người thuê nhà chia sẻ hệ thống mã thông báo 6K trên 200 truy vấn / giờ.
   Trung文翻译:一个租户在 200 查询/小时中共享 6K token 系统提示――计算 LMCache 的预期节省――
3. LMCache máy chủ là một điểm thất bại duy nhất. Thiết kế chiến lược HA (những bản sao, trở lại bản gốc).
   Trung文翻译:LMCache 服务器是单点故障──设计 HA 策略(副本、回退到重算)。
4. LMCache lưu trữ cho Ceph trên đĩa quay. cho một KV 4K-token ở 70B FP8 (500 MB), thời gian đọc là bao nhiêu so với tái lấp đầy?
   Trung文翻译:LMCache 存储到机械硬盘 Ceph── đối với 70B FP8 上 4K token KV(500MB),读取延迟是多少?与重算比较──
5. Thảo luận liệu con đường vLLM 0.11.0 không đồng bộ là "tự do"  nơi mà đầu hàng ẩn?

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Production-stack | "the reference deployment" | vLLM's Kubernetes Helm chart + operator |
| Connector API | "KV backend interface" | vLLM 0.9.0+ pluggable KV store interface |
| Native CPU offload | "engine-local spill" | Store KV in host RAM of same engine |
| LMCache | "cluster KV cache" | Cross-engine KV cache server on CPU DRAM + disk |
| 0.11.0 async | "non-blocking offload" | Offload hidden behind engine stream |
| Preemption | "evict to make room" | KV cache shuffle when HBM full |
| Prefix reuse | "same system prompt" | Multiple queries share beginning; cache hit |
| Ceph tier | "disk tier" | Durable storage below DRAM in the cache hierarchy |

## Xem thêm 延伸阅读

- [vLLM Blog — KV Offloading Connector (Jan 2026)](https://blog.vllm.ai/2026/01/08/kv-offloading-connector.html)
- [vLLM Production Stack GitHub](https://github.com/vllm-project/production-stack) Hình ảnh Helm + người vận hành.
- [LMCache for Enterprise-Scale LLM Inference (arXiv:2510.09665)](https://arxiv.org/html/2510.09665v2)
- [LMCache GitHub](https://github.com/LMCache/LMCache) Thực hiện các kết nối.
- [vLLM 0.11.0 release notes](https://github.com/vllm-project/vllm/releases) chi tiết đường đi không đồng bộ.
