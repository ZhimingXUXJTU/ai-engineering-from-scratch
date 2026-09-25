# Nhiều khu vực LLM phục vụ và KV Cache địa điểm .

> Sự cân bằng tải trọng vòng tròn là tích cực gây hại cho suy luận LLM được lưu trữ trong cache. Một yêu cầu không đáp xuống nút giữ tiền đề của nó trả phí hoàn toàn prefill  khoảng 800 ms tại P50 trên một prompt dài so với ~ 80 ms với một cache hit. Năm 2026, mô hình sản xuất là một router có ý thức cache (vLLM Router in Rust, llm-d router) tiêu thụ các sự kiện cache KV và các tuyến đường trên prefix-hash match. Nghiên cứu gần đây (GORGO) làm cho độ trễ mạng xuyên khu vực là một thuật ngữ rõ ràng trong mục tiêu định tuyến. Các dịch vụ "chỉ số thu thập giá xuyên khu vực" thương mại (chỉ số thu thập giá xuyên khu vực Bedrock, cửa ngõ đa cụm GKE) xử lý suy luận như không minh bạch  họ xử lý tính sẵn có, không phải TTFT. JPMorgan và Mayo Clinic đã tiến hành vụ thất bại của chúng ta ở phía đông-1 vào tháng 11 năm 2024 với khoảng 22 phút. Thực tế DR: 32% thất bại LLM DR là vì các nhóm sao lưu trọng lượng nhưng quên các tệp token hoặc cấu hình định lượng.

> **【中文解读】**Bài viết này giới thiệu nhiều khu vực KV 局部性跨区域部署 LLM 时的 KV Cache 优化策略──


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy prefix-cache-aware router simulator) | **语言:** Python
**Prerequisites:** Phase 17 · 04 (vLLM Serving), Phase 17 · 06 (SGLang RadixAttention) | **前置知识:** Phase 17 · 04 (vLLM Serving), Phase 17 · 06 (SGLang RadixAttention)

>  **【前置】**学本节前请先掌握:Phase 17·04(vLLM) 、Phase 17·06(RadixAttention) 多区域部署 phải sử dụng bộ định tuyến có tính cache, không thể round-robin。
>  **【类比】**多区域 LLM = "连锁餐厅中央厨房"――Round-robin = 随机送单到分店(缓存命中率 0,每次重做);Cache-aware router = 按前哈希送到已有缓存的分店(命中 80ms vs 未命中 800ms) ――JPMorgan/Mayo Clinic 2024 灾备演练 22 分钟切换;;失败教学:32% LLM DR 失败因为只备权重忘了代币器量或配置文件清单必须完整――
**Time:** ~60 minutes | **时间:** ~60 minutes

## Mục tiêu học tập

- Giải thích tại sao việc cân bằng tải trọng vòng tròn phá vỡ suy luận và định lượng hình phạt TTFT.
  Trung文翻译:解释为什么轮询负载均衡破坏缓存推理,并量化 TTFT 惩罚。
- Chụp đồ họa một router có ý thức về cache: đầu vào (kết quả cache KV), thuật toán (đáp ứng với prefix-hash), tie-breaker (tận dụng GPU).
  Trung文翻译:绘制缓存感知路由器:输入(KV 缓存事件) 算法(前哈希匹配) 决胜(GPU利用率) ⋅
- Hãy nêu tên trình điều khiển thất bại DR 32% cho LLMs (tài liệu tokenizer / cấu hình định lượng bị thiếu) và nêu danh sách kiểm tra DR ba tệp.
  Trung ngữ翻译:说出 LLM 32% DR 失败的原因(缺失分词器文件/量化配置)并陈述三文件 DR 检查清单。
- Sự khác biệt giữa các dịch vụ thương mại xuyên khu vực (Bedrock CRI, GKE Multi-Cluster Gateway) và định tuyến KV-aware.
  Trung文翻译:区分商业跨区域产品(Bedrock CRI、GKE Multi-Cluster Gateway) với KV 感知路由──

## Vấn đề  vấn đề giới thiệu

> **【中文解读】**Nhiều khu vực LLM  dịch vụ ba vấn đề trung tâm: 1) 缓存路由轮询 tải trọng cân bằng phá vỡ KV Cache 局部性, dẫn đến tỷ lệ dự phòng trung bình từ 70%  giảm xuống 8%; 2) DR 卫生32% của LLM DR  thất bại vì nhóm đã đăng ký quyền trọng nhưng quên phân từ文件 hoặc định lượng định cấu hình; 3) dữ liệu ở lại GDPR  yêu cầu EU người dùng dữ liệu không thể rời khỏi EU, bộ định tuyến lưu trữ không thể phù hợp trước với yêu cầu của người dùng Paris đến từ phía đông Mỹ-1。

> **【拓展：多区域推理的产业实践】**Các thực hành tốt nhất của LLM đa khu vực được triển khai vào năm 2026 bao gồm: 1) Mỗi khu vực 独立的缓存知性路由器 (vLLM Router / llm-d router),避免跨区域 KV 转移高延迟(US-EU RTT 约75ms,US-APAC 约220ms);(2) GORGO nghiên cứu sẽ sử dụng网络延迟作为路由目标的显式项联合优化 prefill_time + network_latency;(3) Bedrock cross-region inference 和 GKE Multi-Cluster Gateway 处理可用性,但不处理 TTFT你仍然需要应用层缓存性路由器.

Dịch vụ của bạn chạy ở US-East-1, US-West-2 và EU-West-1. Bạn đặt một ALB trước với round-robin. tỷ lệ hit cache tiền đề trong sản xuất giảm xuống còn 8%. TTFT P50 gấp ba lần. nhật ký vLLM của bạn cho thấy mỗi yêu cầu trả đầy phí tiền mua.

> Bạn đang ở phía trước để đặt ALB làm các cuộc hỏi. Trong sản xuất, tỷ lệ dự phòng dự phòng đã giảm xuống còn 8%. TTFT P50 tăng gấp ba lần.

Round-robin là tối ưu cho các dịch vụ không có quốc tịch. LLM suy luận là trạng thái theo thiết kế  bộ nhớ cache KV mã hóa mọi thứ mô hình đã thấy.

> 轮询负载均衡对无状态服务优优――LLM 推理自然是有状态的KV 缓存编码了模型看到的所有内容――盲路由就是路由到错误的缓存――

Một cách riêng biệt, nhóm của bạn có một kế hoạch DR. Bạn sao lưu trọng lượng mô hình cho khu vực S3. Một sự cố khu vực xảy ra; bạn cố gắng không hoạt động; bản sao từ chối khởi động. Bạn quên tokenizer.json, cấu hình định lượng, và cấu hình quy mô RoPE ở trong một thùng riêng mà bạn không đồng bộ hóa.

> Mặt khác, nhóm của bạn có kế hoạch phục hồi thảm họa. Bạn sẽ tải trọng mô hình trên khu vực dự trữ đến S3.

Việc phục vụ LLM đa khu vực là một vấn đề cache, một vấn đề định tuyến, và một vấn đề vệ sinh DR không phải là vấn đề cân bằng tải trọng.

> Nhiều khu vực LLM  dịch vụ là một vấn đề lưu trữ  một vấn đề đường dẫn và một vấn đề sức khỏe phục hồi thảm họa  không phải là vấn đề cân bằng tải trọng 

## Khái niệm cốt lõi

### Đường dẫn có tính cache

> **【中文解读】**Cache-aware 路由工作机制:请求到达后,路由器对前 (如前512 token) làm哈希,查询每个副本"你是否有这个前缓存?"──副本通过pub/sub 频道发布 KV Cache 事件(分配/淘汰块),路由器维护前哈希→副本的索引──匹配到则路由到该副本,未匹配则按GPU利用率选择──vLLM Router(Rust 实现,2026生产-堆积) hỗ trợ O(1) 寻找,未匹配时回归至最小队列深度──

Các yêu cầu đến với một lời nhắc. Router hashes tiền đề (chẳng hạn, đầu tiên 512 token); nó hỏi mỗi bản sao "bạn có tiền đề này được lưu trữ trong cache không?". Các bản sao xuất bản các sự kiện lưu trữ KV trên một kênh pub / sub khi họ phân bổ và loại bỏ các khối. Router chọn bản sao với sự phù hợp, rơi qua vào tie-breaker dựa trên GPU-util nếu không ai làm.

> Xin hãy mang theo gợi ý đến. Đường dẫn cho trước (như trước 512 token) làm哈希; nó hỏi mỗi bản "Có phải bạn có dự trữ trước đây này không?"

**vLLM Router**(Rust, 2026 sản xuất-phân): đăng ký `kv.cache.block_added`events, duy trì một prefix-hash → replica index, đường dẫn với O(1) tìm kiếm.

> **vLLM Router**(Rust,2026 sản xuất-stack): 订阅 `kv.cache.block_added`事件,维护前哈希 → 副本索引,O(1) 查找路由──无匹配时回归最小队列深度──

**llm-d router**: cùng một mô hình, Kubernetes bản địa. xuất bản các sự kiện thông qua ControlPlane API.

> **llm-d router**: cùng một mô hình,Kubernetes 原生── thông qua ControlPlane API 发布事件──

**SGLang RadixAttention**(Phase 17 · 06) là tương đương trong bản sao.

> **SGLang RadixAttention**(Phase 17 · 06) là các giá tương đương trong dự án.

### Số

> **【拓展：KV Cache 路由的性能数据】**多区域 KV Cache 路由的性能差距:2K-token提示在 Llama 3.3 70B FP8 H100 上, cache hit(同副本、前常驻)TTFT ~80ms; cache miss(冷预填)TTFT ~800ms10x 差距。 Nếu router trong副本实现 60-80% 的前缓存命中率, có thể trong N副本容量下近似单副本性能──区域间 RTT cũng là yếu tố quan trọng:us-east-1  us-west-2 ~65ms、us-east-1  eu-west-1 ~75ms、us-east-1   southeast-1 ~220ms跨区域路由只在远 网络中延迟时间才有价格──

TTFT P50 trên một lệnh 2K-token, Llama 3.3 70B FP8, H100:
- Cache hit (những bản sao tương tự, prefix resident): ~ 80 ms.
- Cache miss (cụ trước lạnh): ~ 800 ms.

10x khoảng cách. Nếu router của bạn đạt 60-80% cache tiền tố trên các bản sao, bạn ước tính hiệu suất bản sao đơn tại N-thực lượng bản sao. Nếu nó đạt 10%, bạn ước tính quy mô ngây thơ.

> 2K-token 提示在 Llama 3.3 70B FP8 H100 上的 TTFT P50:缓存命中(同副本,前常驻) khoảng 80ms;缓存未命中(冷预填充) khoảng 800ms──10倍差距── Nếu bộ viên của bạn trong副本实现 60-80% của dự phòng trước缓存命中率, bạn có thể ở N 副本容量下近似单副本性能──如果只有 10%,你近似朴素扩展──

### Cross-region có một hạn chế mới  độ trễ mạng

RTT liên khu vực:
- US-East-1  US-West-2: ~65 ms.
- US-East-1  eu-west-1: ~ 75 ms.
- US-East-1  ap-southeast-1: ~ 220 ms.

Nếu định tuyến đưa yêu cầu từ us-east-1 đến một tiền tố nóng ở ap-southeast-1, prefill lưu (800 → 80 ms) sẽ bị làm nhỏ hơn 440 ms đi lại. GORGO (2026 nghiên cứu) làm cho điều này rõ ràng  giảm thiểu `prefill_time + network_latency`Thông thường câu trả lời là tiếp tục định tuyến khu vực ngoại trừ trên các tiền tố đa MB lớn nơi prefill thống trị.

> 区域间 RTT:us-east-1  us-west-2 约 65ms;us-east-1  eu-west-1 约 75ms;us-east-1  ap-southeast-1 约 220ms;;如果路由将请求从us-east-1 发送到ap-southeast-1 的热前,节省的预填(800 → 80ms) 被 440ms 的往返延迟淹没;;GORGO(2026年研究) 明确指出联合优化`prefill_time + network_latency`, không phải là đơn vị tối ưu hóa prefillment. Câu trả lời thường là giữ đường dẫn khu vực hóa, trừ khi quá trình prefillment chiếm chủ quyền trên nhiều MB trước.

### "Phân luận xuyên khu vực" thương mại không giúp ở đây

AWS Bedrock cross-region inference tự động chuyển các yêu cầu sang các khu vực khác trong khi áp lực công suất. Nó tối ưu hóa tính sẵn có, không phải TTFT, và xử lý inference như không minh bạch. GKE Multi-Cluster Gateway là cùng một  service level failover, không có nhận thức về cache KV.

> AWS Bedrock 跨区域推理在容量压力下自动将请求路由到其他区域――它优化可用性而不是TTFT,将推理视为不透明――GKE Multi-Cluster Gateway 也是如此服务级故障转移,不感知 KV 缓存――

Bạn vẫn cần một bộ định tuyến có tính cache trong lớp ứng dụng ngay cả khi sử dụng chúng. Chúng xử lý trường hợp "US-East-1 đang cháy".

> Ngay cả khi sử dụng các sản phẩm này, bạn vẫn cần áp dụng các bộ xử lý cảm giác phòng ngừa.

### DR vệ sinh  32% vấn đề file bị mất

> **【中文解读】**DR 卫生的三文件最低清单:(1) HF 模型仓库下的所有文件(权重 + 配置 + 分词器);(2) 引擎特定服务配置(vllm_config.yaml等);(3) 部署清单(K8s YAML、Dockerfile、依赖锁文件) ⋅加上:

> **【拓展：LLM 灾难恢复最佳实践】**Thực hành quan trọng của LLM DR năm 2026: 1) 模型制品完整性不只是权重文件,还包含tokenizer.json、quantize_config.json、RoPE 缩放配置、聊天模板; 2) 跨区域同步S3 跨区域复制 用于模型仓库,确保所有地区有完整副本; 3) tự động hóa DR 测试使用混沌工程;;

Số liệu được trích dẫn rộng rãi năm 2026: 32% thất bại LLM DR xảy ra bởi vì các nhóm đã sao lưu trọng lượng nhưng quên:

- `tokenizer.json`hoặc `tokenizer.model`
- Các cấu hình định lượng (`quantize_config.json`, AWQ scale, GPTQ điểm không)
- Các cấu hình cụ thể cho mô hình (RoPE quy mô, mặt nạ chú ý, mẫu trò chuyện)
- Thiết lập động cơ (`vllm_config.yaml`, các mẫu mặc định, biểu hiện bộ chuyển đổi LoRA)

> Số liệu được trích dẫn rộng rãi năm 2026: 32% của LLM  thảm họa phục hồi thất bại là vì nhóm đã lưu trữ trọng lượng nhưng quên:分词器文件、量化配置、模型特定配置、引擎配置──

Việc sửa là một văn bản DR tối thiểu ba tập tin:

1. Tất cả các tệp dưới dạng repo mô hình HF (nặng + cấu hình + tokeniser).
2. Định hướng dịch vụ cụ thể cho động cơ.
3. Bản biểu triển khai (K8s YAML, Dockerfile, khóa phụ thuộc).

> 修复方案是三文件最低 DR 清单:(1) HF 模型仓库下的所有文件(权重 + 配置 + 分词器);(2) 引擎特定服务配置;(3) 部署清单(K8s YAML、Dockerfile、依赖锁文件) ⋅

Thêm vào đó, chạy một cuộc tập luyện DR hàng quý.

> Ngoài ra: mỗi quý hoạt động DR 演练――JPMorgan 2024 年 11 月 us-east-1 演练 đạt 22 phút phục hồi, chính vì dự án đã trải qua排练――

### Data Residency là orthogonal

PHI khách hàng EU không thể rời EU. Nếu router có ý thức về cache của bạn gửi yêu cầu gốc Paris đến us-east-1 cho một sự phù hợp tiền tố, bạn đã vi phạm GDPR bất kể lợi ích của TTFT. Chia các router theo ranh giới cư trú trước khi tối ưu hóa cho cache.

> Nếu bộ chuyển hóa cảm nhận của bạn sẽ được gửi đến phía đông Mỹ-1 để thực hiện việc so sánh trước, bất kể TTFT có lợi thế như thế nào, bạn đã vi phạm GDPR trước khi tối ưu hóa bộ chuyển hóa.

### Những con số mà bạn nên nhớ

- Hỗ trợ cache vs miss TTFT khoảng cách: ~ 10x (80 ms vs 800 ms trên 2K prompt).
- RTT liên khu vực Mỹ-EU: ~ 75 ms.
- DR thất bại: 32% bỏ qua các cấu hình tokenizer/quant.
- JPMorgan us-east-1 failover tháng 11 năm 2024: 22 phút (30 phút SLA).

## Hãy sử dụng nó để thực hiện
```figure
cache-aware-router
```

## Sử dụng nó

`code/main.py`mô phỏng ba chiến lược định tuyến (round-robin, cache-aware khu vực, cache-aware toàn cầu) trên khối lượng công việc đa khu vực.

> `code/main.py`Trong nhiều khu vực tải trọng công việc mô phỏng ba phương pháp:

## Chuyển nó đi.

Bài học này sẽ mang lại kết quả `outputs/skill-multi-region-router.md`Với các khu vực, hạn chế cư trú và SLA, thiết kế kế kế hướng đi.

> 本课产 出 `outputs/skill-multi-region-router.md` Định định khu vực  Giao tiếp và SLA, thiết kế đường lối

## Tập luyện bài tập

1. Đi chạy`code/main.py`- Dường độ nhanh nào của đường dẫn xuyên khu vực vượt qua đường dẫn chỉ ở địa phương, với 75 ms RTT?
   Trung ngữ翻译:运行 `code/main.py`❖ Đưa ra 75ms RTT, trong khi đường xuyên khu vực cao hơn đường bộ địa phương?
2. Tỷ lệ truy cập cache của bạn giảm từ 70% xuống còn 12%. Chẩn đoán ba nguyên nhân có thể và các nguyên nhân quan sát có thể xác nhận mỗi nguyên nhân.
   Trung ngữ: Trung Quốc: tỷ lệ dự phòng của bạn từ 70% giảm xuống còn 12%  Chẩn đoán ba nguyên nhân có thể và mỗi chỉ số xác nhận 
3. Thiết kế một biểu đồ DR cho mô hình 70B AWQ-quantized phục vụ trong vLLM với 5 bộ chuyển đổi LoRA.
   Trung文翻译:为vLLM 中有5个 LoRA 适配器的70B AWQ 量化模型设计 DR 清单――列出每个文件和配置――
4.    Trung ngữ翻译:论证 Bedrock 跨区域推理对有严格的 TTFT SLO的金融科技公司是否足够──引用具体行为──
   Trung ngữ翻译: 中文翻译:论证 Bedrock 跨区域推理对有严格的 TTFT SLO的金融科技公司是否足够──引用具体行为──
5. Một yêu cầu có nguồn gốc từ Paris phù hợp với một dấu tiền ở phía đông Mỹ-1.
   Trung ngữ翻译:一个巴黎源的请求在美国东部-1 匹配到前──你路由它吗?写出策略──

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Cache-aware routing | "smart LB" | Route on prefix-hash match to KV-cache-holding replica |
| KV-cache events | "cache pub-sub" | Replicas publish block add/evict; router indexes |
| Prefix hash | "cache key" | Hash of first N tokens used as router lookup |
| GORGO | "cross-region routing research" | arXiv 2602.11688; network latency as explicit term |
| Cross-region inference | "Bedrock CRI" | AWS product; availability failover, not TTFT awareness |
| DR manifest | "the backup list" | Every file needed to restore — not just weights |
| Data residency | "GDPR boundary" | Legal constraint on which region sees user data |
| RTT | "round-trip time" | Network latency; 75 ms US-EU, 220 ms US-APAC |
| LLM-aware LB | "cache-hit LB" | Cache-aware router as a product category |

## Xem thêm 延伸阅读

- [BentoML — Multi-cloud and cross-region inference](https://bentoml.com/llm/infrastructure-and-operations/multi-cloud-and-cross-region-inference)
- [arXiv — GORGO (2602.11688)](https://arxiv.org/html/2602.11688v1) tái sử dụng cache KV xuyên khu vực với thời hạn trễ mạng.
- [TianPan — Multi-Region LLM Serving Cache Locality](https://tianpan.co/blog/2026-04-17-multi-region-llm-serving-data-residency-routing)
- [AWS Bedrock Cross-Region Inference](https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html) Tài liệu về sự sẵn có của sự cố chuyển.
- [vLLM Production Stack Router](https://github.com/vllm-project/production-stack) nguồn router có tính cache.
