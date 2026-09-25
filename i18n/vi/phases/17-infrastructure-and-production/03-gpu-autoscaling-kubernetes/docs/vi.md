# GPU tự động mở rộng trên Kubernetes  Karpenter, KAI lập trình, lập trình băng đảng  tự động mở rộng Kubernetes  điều chỉnh GPU

> Ba lớp, không phải một lớp. Các dự án Karpenter nối động (dưới một phút, 40% nhanh hơn Cluster Autoscaler). KAI Scheduler xử lý lập trình nhóm, nhận thức về topology và hàng ngũ bậc thang  nó ngăn chặn bẫy phân bổ phần 7 trong 8 nơi bảy nút chờ và đốt cháy trên một GPU bị mất. Các bộ tự động cấp ứng dụng (NVIDIA Dynamo Planner, llm-d Workload Variant Autoscaler) đo lường trên các tín hiệu cụ thể suy luận  độ sâu hàng, sử dụng bộ nhớ cache KV  không phải chu kỳ hoạt động của CPU / DCGM. Cái bẫy HPA cổ điển là`DCGM_FI_DEV_GPU_UTIL`là một phép đo chu kỳ nhiệm vụ: 100% có thể là 10 yêu cầu hoặc 100. vLLM phân bổ trước bộ nhớ cache KV, vì vậy bộ nhớ không bao giờ kích hoạt quy mô xuống. Bài học này dạy bạn cách soạn ba lớp và tránh mặc định Karpenter `WhenEmptyOrUnderutilized`Chính sách chấm dứt việc chạy các công việc GPU giữa thời gian.

> **【中文解读】**Bài viết này giới thiệu về GPU tự động mở rộng  Kubernetes 上 LLM 推理服务的 GPU资源 tự động mở rộng chiến lược.
**Type:** Learn
**Languages:** Python (stdlib, toy queue-depth autoscaler simulator)
**Prerequisites:** Phase 17 · 02 (Inference Platform Economics), Phase 17 · 04 (Serving Engine Internals)
**Time:** ~75 minutes


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy queue-depth autoscaler simulator) | **语言:** Python（标准库，队列深度自动扩缩模拟器）
**Prerequisites:** Phase 17 · 02 (Inference Platform Economics), Phase 17 · 04 (vLLM Serving Internals) | **前置知识:** Phase 17 · 02（推理平台经济学）, Phase 17 · 04（vLLM 服务内部）

>  **【前置】**学本节前请先掌握:Phase 17·02(平台经济学)、Phase 17·04(vLLM)、Kubernetes 基础。三层扩缩:Karpenter(节点层) + KAI Scheduler(Pod 层帮规划) + 应用层(队列深度/KV利用率)。
>  **【类比】**GPU 扩缩 = "餐厅运力调度"。Karpenter = 开新店(分钟级);KAI = 桌位组合(gang scheduling 防 7/8 部分分配,7 桌等 1 桌);应用层 = 服务员按等位队列长度调座。HPA 陷:DCGM 率占空比,100% 可能是10个或100个请求必须使用 Goodput(Phase 17·08) 替补。

## Mục tiêu học tập

- Chụp đồ thị ba lớp tự động quy mô (định lượng nút, lập lịch nhóm, cấp độ ứng dụng) và đặt tên công cụ được sử dụng tại mỗi lớp.
  Trung文翻译:绘制三层自动扩缩层(节点供给、gang 调度、应用级)并命名每个层使用的工具──
- Hãy giải thích lý do tại sao `DCGM_FI_DEV_GPU_UTIL`là tín hiệu HPA sai cho vLLM và đặt tên cho hai thay thế (thâm sâu hàng rào, sử dụng cache KV).
  Trung ngữ翻译:解释为什么`DCGM_FI_DEV_GPU_UTIL`là vLLM 错误的 HPA 信号,并说出两个替代方案 (quang dung lượng  KV 缓存利用率)
- Mô tả lập trình nhóm và chế độ thất bại phân bổ một phần KAI Scheduler ngăn chặn (7 trong số 8 GPU không hoạt động).
  Trung文翻译:描述帮 调度和 KAI Scheduler 防止的部分分配故障模式(8 个 GPU 中 7 个空) ⋅
- Tên chính sách hợp nhất của Karpenter (`WhenEmptyOrUnderutilized`) chấm dứt việc chạy các công việc GPU và nêu ra sự thay thế an toàn vào năm 2026.
  Trung文翻译:说出终止正在运行 GPU 任务的 Karpenter 合并策略(`WhenEmptyOrUnderutilized`),并说明 chương trình thay thế an ninh năm 2026

## Vấn đề  vấn đề giới thiệu

> **【中文解读】**GPU tự động mở rộng trên Kubernetes có ba cấp độ của các mô hình cố cố cố: 1) HPA sử dụng sai tín hiệu (những tín hiệu) (những tín hiệu sử dụng GPU không phải là độ sâu hàng), dẫn đến việc mở rộng không mở rộng; 2) Cluster Autoscaler 节点 cung cấp quá chậm, dài提示请求超时; 3) nhiều GPU phân phối các phần suy luận (những đoạn phân phối) (những đoạn 7 trong 8 cạm bẫy), 7 GPU không chuyển tiếp chờ đợi thứ 8.

> **【拓展：GPU 集群管理】**Năm 2026 Kubernetes đã trở thành nền tảng chuẩn lập dịch vụ LLM 推理服务的编排平台――NVIDIA DGX Cloud、Google GKE、AWS EKS đều cung cấp GPU 节点池管理──关键 thách thức nằm ở GPU là tài nguyên đắt tiền và hiếm có(H100 约 $3-4/h), việc mở rộng quyết định phải xác định chi phí quá mức cung cấp, thiếu cung tác động đến SLA──Karpenter + KAI Scheduler

Nhóm của anh đưa ra dịch vụ LLM trên Kubernetes.`DCGM_FI_DEV_GPU_UTIL`HPA không bao giờ tăng quy mô  nó đã nghĩ bạn đã đầy. bạn thêm một bản sao bằng tay; TTFT giảm. HPA vẫn không tăng quy mô. tín hiệu đang nói dối bạn.

> Nhóm của anh đã triển khai dịch vụ LLM tại Kubernetes.`DCGM_FI_DEV_GPU_UTIL`作为信号设置 HPA──服务在业务时段保持在100%利用率──HPA 从不扩容它认为你已经满满了──你手动添加一副本;TTFT 下降──HPA 仍然不扩容──信号在欺骗你──

Một lệnh mã thông báo 1M đến lúc 2 giờ sáng; cluster dành 3 phút để cung cấp một nút, và thời gian yêu cầu.

> Mặt khác, bạn sử dụng Cluster Autoscaler 管理节点──凌晨2点来一个M token 的提示;集群花 3分钟供给节点,请求超时──

Một lần nữa, bạn triển khai một mô hình 70B đòi hỏi 8 GPU trên 2 nút. Cluster có 7 GPU miễn phí và 1 trải rộng trên 3 nút. Cluster Autoscaler cung cấp một nút cho 1 GPU thiếu. Bảy nút chờ 4 phút đốt tiền trong khi Kubernetes nhận GPU cuối cùng lên.

> Một lần nữa, bạn triển khai một mô hình 70B của 8 GPU cần 2 node. 集群 có 7 GPU không còn, 1 phân tán trên 3 node. Cluster Autoscaler vì thiếu hụt 1 GPU cung cấp một node.

Ba lớp, ba chế độ thất bại khác nhau. Auto-scaling GPU nhận thức vào năm 2026 không phải là "tập vào HPA". Nó là tạo ra các nút cung cấp, lập lịch nhóm, và ứng dụng tín hiệu tự động.

> Ba tầng, ba kiểu khác nhau của các lỗi. Năm 2026 GPU cảm nhận tự động mở rộng không phải là " mở HPA " .

## Khái niệm cốt lõi

### Lớp 1  Định lượng nút (Karpenter)

> **【中文解读】**Lớp đầu tiên là các nút cung cấp.`WhenEmptyOrUnderutilized`合并策略它 sẽ chấm dứt hoạt động 节点 GPU 推理 để chuyển sang kiểu ví dụ rẻ hơn, dẫn đến yêu cầu thất bại và mô hình tải lại(5-20 phút gián đoạn)。GPU 池应使用 `WhenEmpty`+ `consolidateAfter: 1h`Chiến lược an ninh.

Karpenter xem các pods và các nút dự trữ đang chờ trong khoảng 45-60 giây (Cluster Autoscaler thường mất 90-120 giây cho các nút GPU).`NodePool`hạn chế  nếu pod của bạn cần 8 H100 và cluster không có nút phù hợp, Karpenter cung cấp một trực tiếp thay vì mở rộng quy mô một nhóm hiện có.

> Karpenter  giám sát chờ điều chỉnh của Pod, trong khoảng 45-60 giây cung cấp các nút(Cluster Autoscaler đối với GPU 节点 thường cần 90-120 giây) ⋅ tùy thuộc vào nó `NodePool`约束动态选择实例类型 Nếu Pod của bạn 需要8 H100 且集群没有匹配节点,Karpenter 直接供给一个,而不是扩展现有组──

**The consolidation trap**: Karpenter's default `consolidationPolicy: WhenEmptyOrUnderutilized`là nguy hiểm cho các GPU pool. Nó sẽ chấm dứt một nút GPU đang chạy để di chuyển pods sang một phiên bản kích thước phù hợp rẻ hơn. Đối với tải trọng công việc suy luận có nghĩa là loại bỏ các yêu cầu đang chạy và tải lại mô hình 70B trên nút mới.

> **合并陷阱**: Carpenter's默认 `consolidationPolicy: WhenEmptyOrUnderutilized`Đối với GPU 池 rất nguy hiểm. Nó sẽ chấm dứt hoạt động của các GPU 节, sẽ chuyển Pod sang các ví dụ phù hợp rẻ hơn. Đối với các dự đoán tải trọng, điều này có nghĩa là yêu cầu trong quá trình chạy và tải lại 70B mô hình trên các node mới.

Cài đặt an toàn cho các hồ GPU:

```yaml
disruption:
  consolidationPolicy: WhenEmpty
  consolidateAfter: 1h
```

Cho phép Karpenter hợp nhất các nút thực sự trống rỗng sau một giờ nhưng không bao giờ đuổi việc đang chạy.

> Hãy để Karpenter trong một giờ sau cùng thực sự không có một điểm, nhưng không bao giờ đuổi theo nhiệm vụ trong hành trình.

### Lớp 2  lập trình băng đảng (KAI Scheduler)

> **【中文解读】**Lớp thứ hai là điều chỉnh phối hợp;. KAI Scheduler  giải quyết các vấn đề mặc định khi lập trình viên không thể xử lý được ba vấn đề: 1) Gang Scheduling toàn có toàn không điều chỉnh, 8-GPU 推理要么全部启动要么全部等待; 2) 拓感知根据 NVLink/InfiniBand/机架拓放置 Pod; 3) 分层队列多团队竞争同一 GPU 池时按优先级和配额管理;;

> **【拓展：GPU 调度器生态】**2026 năm GPU 调度器 选择包括 KAI Scheduler(原 Karp,支持帮 + topology + queue) 、YuniKorn(Apache 项目,支持队列和抢占) 、以及默认 kube-scheduler + 设备插件。KAI Scheduler là một giải pháp lập lịch nhóm duy nhất, đã được Ray 和 vLLM sản xuất-stack 集成── đối với nhu cầu nhiều trường hợp về GPU phân bố n định hình ◎70B+ 模型),KAI là một lựa chọn cần thiết──

KAI Scheduler (phương án "Karp" sau đó được đổi tên) xử lý những gì kube-scheduler mặc định không làm:

**Gang scheduling** lập trình tất cả hoặc không có gì. một pods phân phối suy luận đòi hỏi 8 GPU hoặc tất cả 8 bắt đầu cùng nhau hoặc không làm. Nếu không có điều này, bạn có cái bẫy phân bổ một phần: 7 trong số 8 pods bắt đầu, chờ vô thời hạn, đốt tiền.

**Topology awareness** biết GPU nào chia sẻ NVLink, nằm trên cùng một ngăn xếp, có InfiniBand giữa họ. Đặt pods tương ứng.

**Hierarchical queues** nhiều đội cạnh tranh cho cùng một nhóm GPU với ưu tiên và hạn chế.

KAI được triển khai cùng với kube-scheduler như một scheduler thứ cấp; bạn ghi chú tải trọng công việc để sử dụng nó.

> KAI 作为二级调度器和 kube-scheduler 一起部署;你通过注解让工作负载使用它──Ray 和 vLLM生产堆已集成──

### Lớp 3  Các tín hiệu cấp ứng dụng

> **【中文解读】**Lớp thứ ba là ứng dụng cấp tín hiệu.`DCGM_FI_DEV_GPU_UTIL`là GPU  chiếm dụng tỷ lệ (các chu kỳ nhiệm vụ) chỉ số 100% có thể có nghĩa là 10 个请求 hoặc 100 个请求, vì GPU đều bận rộn.

> **【拓展：推理感知自动扩缩】**NVIDIA Dynamo Planner 和 llm-d Workload Variant Autoscaler là một bộ mở rộng chuyên về thiết kế 推理 của LLM vào năm 2026  chúng trực tiếp tiêu thụ các chỉ số nội bộ của động cơ推理 (nội dung độ  KV Cache 块 sử dụng), chứ không phải chỉ số GPU phổ biến  "thảm giác推理" mở rộng so với HPA truyền thống.

**The HPA trap**`DCGM_FI_DEV_GPU_UTIL`là một phép đo chu kỳ nhiệm vụ  nó đo liệu GPU có đang làm việc tại mỗi khoảng thời gian lấy mẫu. 100% sử dụng có thể có nghĩa là 10 yêu cầu đồng thời hoặc 100; GPU đã bận rộn theo cả hai cách. Scaling trên chu kỳ nhiệm vụ đang mở rộng mù quáng.

Tệ hơn, vLLM và các động cơ tương tự đã phân bổ bộ nhớ cache KV (từ `--gpu-memory-utilization`HPA dựa trên bộ nhớ không bao giờ giảm.

**2026 replacement signals**- Có thể là:

- Độ sâu hàng (nước yêu cầu chờ dự kiến).
  Trung文翻译:队列深度 (quantify)
- Sử dụng cache KV (nhiều phần nào các khối được phân bổ cho các chuỗi hoạt động).
  Trung文翻译:KV 缓存利用率 (KV 缓存利用率)
- Per-replica P99 TTFT (sín hiệu SLA của bạn).
  Trung文翻译:每副本 P99 TTFT(你的SLA 信号)
- Goodput (cần đáp ứng tất cả các SLO mỗi giây).
  Trung文翻译:Goodput(每秒满足所有SLO的请求数)。

NVIDIA Dynamo Planner và llm-d Workload Variant Autoscaler tiêu thụ các tín hiệu và sao chép quy mô này.

> NVIDIA Dynamo Planner 和 llm-d Workload Variant Autoscaler 消费这些信号并扩缩副本──它们完全取代了 LLM 服务中的 HPA──

### Khi nào sử dụng gì

| Scale decision / 扩缩决策 | Tool / 工具 |
|----------------|------|
| Add/remove nodes / 添加/移除节点 | Karpenter |
| Schedule multi-GPU jobs / 调度多 GPU 任务 | KAI Scheduler |
| Add/remove replicas / 添加/移除副本 | Dynamo Planner / llm-d WVA (or custom HPA on queue depth) |
| Choose GPU type / 选择 GPU 类型 | Karpenter NodePool |
| Preempt low-priority / 抢占低优先级 | KAI Scheduler queues |

> **【拓展：GPU 集群成本优化策略】**Các chiến lược quan trọng của GPU 集群成本优化 trong năm 2026 bao gồm: 1) Spot InstanceAWS/GCP/Azure's GPU Spot instance 节省 60-70%, nhưng cần xử lý gián đoạn(Karpenter + 热池缓解);(2) tự động mở rộngKarpenter trong thời gian không cao điểm tự động giảm节点池,50% chi phí tiết;(3) GPU chia sẻ thông qua MIG(Multi-Instance GPU) sẽ chia H100 thành nhiều instance, phù hợp với mô hình nhỏ được đề xuất;(4) 混合 GPUFP8/INT4 量化 giảm nhu cầu lưu trữ, cho phép nhiều hơn;(5) phân chia các loại triển khaiprefill/decode phân chia thành các loại khác nhau ,30-40% chi phí tiết省;;

### Việc phân tích các mẫu prefill/decode làm phức tạp mọi thứ

> **【中文解读】**Phase 17·17) tiếp tục tăng cường sự phức tạp mở rộng: Prefill Pod 按队列深度扩缩,解码 Pod 按 KV Cache 压力扩缩──不能在两者上使用单一HPA需要各自独立扩缩策略──llm-d将两者暴露为独立的Kubernetes Service,每个服务都有自己的HPA──

> **【拓展：Kubernetes GPU 生态】**Các thành phần quan trọng của Kubernetes GPU quản lý năm 2026 bao gồm:NVIDIA GPU Operator (NVIDIA GPU Operator) ]]> tự động cài đặt động cơ/CUDA/container toolkit) ]]NVIDIA Device Plugin (NVIDIA Device Plugin) ]]GPU 资源发现和分配) ]]MIG]]Multi-Instance GPU, sẽ được chia thành nhiều ví dụ) ]]时间分片 (GPU 共享) ]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]

Nếu bạn chạy prefill / decode phân chia (Phase 17 · 17), bạn có hai lớp pod với các kích hoạt quy mô khác nhau: prefill pods scale trên chiều sâu hàng, decode pods scale trên áp suất cache KV. llm-d phơi bày chúng như riêng biệt `Services`Không cố gắng đặt một HPA trước cả hai.

> Nếu bạn chạy phân chia phân chia prefill/解码(Phase 17 · 17), bạn có hai Pod có kích hoạt kích thích mở rộng khác nhau: prefill Pod 按队列深度扩充,解码 Pod 按 KV 缓存压缩──llm-d sẽ phơi bày chúng độc lập `Services`Mỗi vai diễn đều có HPA riêng của mình. Đừng cố gắng để một HPA riêng ở phía trước của hai người.

### Bắt đầu lạnh cũng quan trọng ở đây

Khử hiệu ứng khởi động lạnh (Phase 17 · 10) là khi thời gian cung cấp nút trở nên hiển thị cho người dùng.`min_workers=1`) cho các đường SLO-chẩn đoán, hoặc sử dụng Modal kiểu kiểm tra chỉ số tại lớp ứng dụng.

> Mức độ nóng tăng lên từ 45-60 giây trước khi tăng lên 20GB  mô hình tải lên động cơ khởi động có nghĩa là yêu cầu bắt đầu từ 0 cần 2-5 phút.`min_workers=1`), hoặc trong ứng dụng sử dụng Modal 风格的检查点──

### Những con số mà bạn nên nhớ

- Định lượng nút Karpenter: ~ 45-60s vs Cluster Autoscaler ~ 90-120s (gpuu node).
  Trung văn翻译:Carpenter 节点供给:约45-60秒 VS Cluster Autoscaler 约90-120秒(GPU 节点)。
- KAI Scheduler ngăn chặn chất thải phân bổ một phần  7 trong 8 bẫy.
  Trung文翻译:KAI Scheduler 防止部分分配浪费7 trong 8 陷。
- `DCGM_FI_DEV_GPU_UTIL`như tín hiệu HPA: bị hỏng; sử dụng độ sâu hàng hoặc sử dụng KV.
  Trung ngữ翻译:`DCGM_FI_DEV_GPU_UTIL`作为 HPA 信号:有缺陷; sử dụng quãng đường hầm độ hoặc KV sử dụng tỷ lệ.
- Thợ làm gỗ `WhenEmptyOrUnderutilized`: chấm dứt việc chạy GPU. Sử dụng `WhenEmpty + consolidateAfter: 1h`để suy luận.
  Trung ngữ翻译:Karpenter `WhenEmptyOrUnderutilized`:终止运行中的 GPU 任务──推理使用 `WhenEmpty + consolidateAfter: 1h`

## Hãy sử dụng nó để thực hiện

> **【拓展：GPU 自动扩缩成本模型】**GPU tự động mở rộng chi phí tối ưu hóa cốt lõi là giảm thời gian chuyển đổi không gian.$3/hr）为例，8-GPU 集群 24/7 运行每月成本约 $17,280── thông qua Karpenter 按需供应 + `WhenEmpty`合并策略 + 推理感知 HPA, có thể tự động giảm dung lượng đến 2GPU trong thời gian không cao, sẽ giảm chi phí hàng tháng xuống còn khoảng $ 8,640 (khos cọc 50%) .
```figure
autoscaling
```

## Sử dụng nó

`code/main.py`mô phỏng một bộ tự động quy mô ba lớp trên khối lượng làm việc của GPU nổ. So sánh HPA ngây thơ (thời gian nhiệm vụ), HPA chiều sâu hàng rào và quy mô theo lịch trình của KAI-gang. báo cáo yêu cầu không được đáp ứng, phút GPU vô hiệu và điểm số tổng hợp.

> `code/main.py`Trong突发 GPU 工作负载上模拟三层自动扩缩器──比较简单 HPA(占用率) 队列深度 HPA 和 KAI 调度扩缩──报告未满足的请求数、空 GPU 分钟数和综合评分──

## Chuyển nó đi.

Bài học này sẽ mang lại kết quả `outputs/skill-gpu-autoscaler-plan.md`Với topology cluster, hình dạng tải trọng và SLO, nó thiết kế một kế hoạch tự động quy mô ba lớp.

> 本课产 出 `outputs/skill-gpu-autoscaler-plan.md`❖ Định định tập hợp, hình dạng tải trọng và SLO, thiết kế 3 tầng tự động mở rộng quy trình.

## Tập luyện bài tập

1. Đi chạy`code/main.py`Trong một khối lượng công việc bùng nổ, bao nhiêu yêu cầu HPA trong chu kỳ nhiệm vụ ngây thơ bỏ ra những HPA sâu hàng rào bắt bắt?
   Trung ngữ翻译:运行 `code/main.py`Trong quá trình phát triển, tỷ lệ chiếm đóng đơn giản của HPA đã bị loại bỏ bao nhiêu yêu cầu được bắt giữ bởi HPA sâu hàng?
2. Thiết kế một Karpenter NodePool cho một cluster phục vụ Llama 3.3 70B FP8 trên H100 SXM5.`capacity-type`- `disruption.consolidationPolicy`- `consolidateAfter`, và một vết bẩn giữ không GPU tải trọng làm việc khỏi các nút này.
   Trung文翻译:为在 H100 SXM5 上服务 Llama 3.3 70B FP8 的集群设计 Karpenter NodePool──指定 `capacity-type``disruption.consolidationPolicy``consolidateAfter`和将非 GPU 工作负载隔离的污点──
3. Nhóm của bạn báo cáo rằng triển khai bị mắc kẹt trong chờ bởi vì "GPU có sẵn nhưng không có chương trình". Chẩn đoán  đây là Karpenter, kube-scheduler, hoặc KAI Scheduler?
   Trung文翻译:你的团队报告部署卡在等待状态因为"GPU có thể sử dụng nhưng Pod 无法调度"――诊断是卡宾特,库布-调度器还是KAI调度器?
4. Chọn một tín hiệu cho các pods sạc tự động và một tín hiệu khác cho các pods giải mã.
   Trung ngữ翻译: chọn một tín hiệu để mở rộng phân chia式预填Pod, một tín hiệu khác được sử dụng để giải mã Pod──为两者提供理由──
5. Xét chi phí của `WhenEmptyOrUnderutilized`Trầm kết hợp hợp nhất định trên một dịch vụ sản xuất 24x7 với trung bình 60 sự kiện giảm yêu cầu/ngày tại P99 TTFT > 10s.
   Trung ngữ翻译:计算 `WhenEmptyOrUnderutilized`合并陷在24x7 生产服务上的成本,该服务平均每天60次请求丢弃事件,P99 TTFT > 10秒──

## Từ khóa  Từ khóa nhanh chóng

| Term / 术语 | What people say / 通俗说法 | What it actually means / 实际含义 |
|------|----------------|------------------------|
| Karpenter | "the node provisioner" / "节点供给器" | Kubernetes node autoscaler; sub-minute provisioning / Kubernetes 节点自动扩缩器；亚分钟级供给 |
| Cluster Autoscaler | "the old scaler" / "旧扩缩器" | Kubernetes node autoscaler predecessor; slower, group-based / K8s 节点扩缩前身；更慢，基于组 |
| KAI Scheduler | "the GPU scheduler" / "GPU 调度器" | Secondary scheduler for gang + topology + queues / 用于 gang + 拓扑 + 队列的二级调度器 |
| Gang scheduling | "all or nothing" / "全有全无" | Schedule N pods atomically or defer all of them / 原子调度 N 个 Pod 或全部推迟 |
| Topology awareness | "rack-aware" / "机架感知" | Place pods based on NVLink/IB/rack placement / 基于 NVLink/IB/机架放置 Pod |
| `DCGM_FI_DEV_GPU_UTIL` | "GPU utilization" / "GPU 利用率" | Duty-cycle metric; NOT a scaling signal for LLMs / 占用率指标；不是 LLM 的扩缩信号 |
| Queue depth | "waiting requests" / "等待请求" | Correct HPA signal for prefill-bound scaling / 预填充扩缩的正确 HPA 信号 |
| KV cache utilization | "memory pressure" / "内存压力" | Correct HPA signal for decode-bound scaling / 解码扩缩的正确 HPA 信号 |
| Consolidation | "Karpenter consolidation" / "Karpenter 合并" | Node termination to cheaper instance type / 终止节点迁移到更便宜实例 |
| `WhenEmpty + 1h` | "safe consolidation" / "安全合并" | Policy that doesn't evict running GPU jobs / 不驱逐运行中 GPU 任务的政策 |

## Xem thêm 延伸阅读

- [KAI Scheduler GitHub](https://github.com/kai-scheduler/KAI-Scheduler) các tài liệu thiết kế và ví dụ cấu hình.
- [Karpenter Disruption Controls](https://karpenter.sh/docs/concepts/disruption/) ngữ nghĩa chính sách hợp nhất và các mặc định an toàn GPU.
- [NVIDIA — Disaggregated LLM Inference on Kubernetes](https://developer.nvidia.com/blog/deploying-disaggregated-llm-inference-workloads-on-kubernetes/) Dynamo Planner quy mô tín hiệu.
- [Ray docs — KAI Scheduler for RayClusters](https://docs.ray.io/en/latest/cluster/kubernetes/k8s-ecosystem/kai-scheduler.html) Mô hình tích hợp tia.
- [AWS EKS Compute and Autoscaling Best Practices](https://docs.aws.amazon.com/eks/latest/best-practices/aiml-compute.html) hướng dẫn cụ thể cho Kubernetes.
- [llm-d GitHub](https://github.com/llm-d/llm-d) Thiết kế Autoscaler Load Variant
