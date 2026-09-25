# Khử hiệu ứng bắt đầu lạnh cho LLM không máy chủ .

> Một hình ảnh mô hình 20 GB mất 5-10 phút (7B) đến 20+ phút (70B) để chuyển từ lạnh đến phục vụ. Trong một thế giới không có máy chủ thực sự, đó không phải là một sự nóng lên  đó là một sự gián đoạn. Các giảm hoạt động ở năm lớp: hình ảnh nút được gieo trước (Bottlerocket trên AWS, vòm hai khối), dòng dòng dòng (NVIDIA Run:ai Model Streamer, bản địa trong vLLM), chụp ảnh chụp trong bộ nhớ GPU (Mô-định kiểm tra, khởi động lại nhanh hơn 10 lần), hồ bơi ấm (`min_workers=1`), tải cấp (ServerlessLLM NVMe→DRAM→HBM đường ống dẫn, giảm độ trễ 10-200x), và di chuyển trực tiếp di chuyển các token đầu vào (KB) thay vì bộ nhớ cache KV (GB). Modal xuất bản 2-4s lạnh bắt đầu như một tầng; Baseten 5-10s mặc định, dưới giây với trước khi nóng lên. Bài học này dạy bạn để đo, ngân sách và xếp chồng năm tầng.

> **【中文解读】**Bài viết này giới thiệu các chiến lược giảm chậm đáp ứng đầu tiên của dịch vụ LLM.


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy cold-start path simulator) | **语言:** Python
**Prerequisites:** Phase 17 · 02 (Inference Platform Economics), Phase 17 · 03 (GPU Autoscaling) | **前置知识:** Phase 17 · 02 (Inference Platform Economics), Phase 17 · 03 (GPU Autoscaling)

>  **【前置】**学本节前请先掌握:Phase 17·02(平台经济学) Phase 17·03(GPU 扩缩) ・Serverless LLM 冷启动 = 5-20 分钟(不是热身,是停服)
>  **【类比】**冷启动缓解 = "汽车预热"。朴素加载 = 钥匙一从零启动(20 分钟);五层加速:(1) 预热节点镜像;(2) 模型流式加载;(3) GPU 内存快照(Modal 10 倍提速);(4) 暖池 min_workers=1;(5) 分层加载(ServerlessLLM NVMe→DRAM→HBM,10-200 倍延迟降低)。Modal实测 2-4 秒冷启动,Baseten 5-10 秒预热版亚秒)。
**Time:** ~60 minutes | **时间:** ~60 minutes

## Mục tiêu học tập

- Đặt ra danh sách năm lớp giảm thiểu khởi động lạnh và đặt tên một công cụ hoặc mô hình tại mỗi lớp.
  Trung ngữ翻译:列举冷启动缓解的五层策略,并说出每层一个工具或模式――
- Xét tổng thời gian khởi động lạnh như là tổng của (định lượng nút) + (nặng tải xuống) + (nặng tải vào HBM) + (nặng khởi động động) cho mô hình 70B.
  Trung文翻译:计算 70B 模型总冷启动时间 = 节点供给 + 权重下载 + 权重加载到HBM + 引擎初始化――
- Giải thích tại sao việc di chuyển trực tiếp chuyển giao token đầu vào (KB) chứ không phải bộ nhớ cache (GB) và hình phạt là gì (tái tính).
  Trung文翻译:解释为什么实时迁移传输输入代币(KB) thay vì KV 缓存(GB),以及代价是什么(重新计算)。
- Tên thương mại hồ ấm (trả tiền cho GPU không hoạt động hoặc chấp nhận đuôi khởi động lạnh) và ngưỡng SLA tại đó `min_workers > 0`trở nên bắt buộc.
  Trung文翻译:说出热池权衡(为空 GPU 付费或接受冷启动尾部),以及 `min_workers > 0`变为强制性的 SLA 值──

## Vấn đề  vấn đề giới thiệu

> **【中文解读】**Vấn đề khởi động lạnh của LLM không máy chủ:70B 模型 từ零到服务需要 3-8 分钟(节点供应 45-60s + 容器拉取 120-300s +权重载 45-120s + 引擎初始化 10-30s),远超2s của SLA── giải pháp là giữ nhiệt池(min_workers=1), nhưng điều này có nghĩa là 24/7 支付空 GPU 费用 5 sản phẩm mỗi dự trữ 1 热副本, mỗi tháng 3600 GPU-hours 无论 có sử dụng hữu ích 调.

> **【拓展：Serverless LLM 平台对比】**2026 năm Serverless LLM 平台的冷启动表现:Modal 凭借 GPU 快照技术实现 2-4s冷启动(业界最快);Baseten 默认 5-10s,预加热后可低于 1s;AWS Lambda + 容器镜像通常10-30s(不包含模型加载);GCP Cloud Run + GPU 较新,冷启动约15-30s──对于TTFT P99 < 60s 的70B+ 模型,热池是强制性的没有任何冷启动优化能在60s内完成全流程──

Các điểm cuối của LLM không máy chủ của bạn tăng lên không qua đêm.

> Bạn của không phục vụ LLM 端点在夜间缩容到零.

1. Karpenter cung cấp một nút GPU: 45-60s.
   Trung文翻译:Karpenter 供给 GPU 节点:45-60 秒──
2. Container kéo một hình ảnh 30 GB với trọng lượng: 120-300s.
   Trung文翻译:容器拉取 30GB của chứa trọng lượng镜像:120-300 giây.
3. Động cơ tải trọng vào HBM: 45-120s tùy thuộc vào kích thước mô hình và tốc độ lưu trữ.
   Trung ngữ翻译: động cơ sẽ tải trọng lên HBM:45-120 giây, phụ thuộc vào mô hình và tốc độ lưu trữ.
4. vLLM hoặc TRT-LLM khởi tạo biểu đồ CUDA, kho lưu trữ KV, tokeniser: 10-30s.
   中文翻译:vLLM 或 TRT-LLM 初始化 CUDA graph、KV 缓存池、分词器:10-30 秒──

Tổng cộng: 220-510s (khoảng 3-8 phút) trước khi một token trở lại. SLA của bạn là 2s. Bạn vận chuyển một hồ ấm (`min_workers=1`Nếu dịch vụ của bạn có 5 sản phẩm mỗi với một bản sao ấm áp, đó là 5 × 24 × 30 = 3.600 giờ GPU / tháng dù một người dùng gọi hay không.

> 总计:220-510 秒(约 3-8 分钟)才能返回一个代币――你的SLA是2秒――你部署热池(`min_workers=1`(văn khoáng) vấn đề dường như đã biến mất nhưng bây giờ bạn 24/7 để một GPU  trả phí. Nếu dịch vụ của bạn có 5 sản phẩm mỗi một warm副本, đó là 5 × 24 × 30 = 3.600 GPU-hours / tháng, bất kể người dùng sử dụng hay không.

Khử hiệu ứng khởi động lạnh là cách giữ cho nền kinh tế không máy chủ trong khi gần gũi với thời gian trễ của luôn bật.

> Sự giảm bớt khởi động lạnh là giữ cho sự chậm trễ của dịch vụ không có dịch vụ kinh tế trong khi tiếp cận với dịch vụ thường trú.

## Khái niệm cốt lõi

### Lớp 1  hình ảnh nút được gieo trước (Bottlerocket)

> **【中文解读】**First layer预播种节点镜像──AWS Bottlerocket's双卷架构将操作系统与数据分离──将容器镜像(含模型权重)预到数据卷快照中,在 `EC2NodeClass`Trung引用快照 ID──新节点启动权重已在本地 NVMe 上消除镜像拉取步骤,为大型模型节省 2-4 分钟──GCP 和 Azure có tương tự tự như VM 镜像模式──

Trên AWS, kiến trúc hai khối lượng của Bottlerocket tách hệ điều hành khỏi dữ liệu. chụp ảnh khối lượng dữ liệu với hình ảnh container của bạn được kéo trước; tham khảo ID chụp ảnh trong `EC2NodeClass`. Các nút mới khởi động với trọng lượng đã trên NVMe địa phương  bước 2 và một phần của 3 biến mất.

> Trên AWS, cấu trúc hai tập của Bottlerocket sẽ tách hệ điều hành và dữ liệu.`EC2NodeClass`Trung引用快照 ID──新节点启动时权重已在本地 NVMe 上步骤 2 和部分步骤 3 消除──原生与卡珀特 配合──典型节省:大型模型每次冷启动 2-4 分钟──

Tương đương trên GCP: hình ảnh VM tùy chỉnh với các lớp container được nướng trước. trên Azure: chụp ảnh nhanh được quản lý trên đĩa với cùng một mô hình.

> GCP 等价方案:预容器层的自定义 VM 镜像──Azure:托管磁盘快照加相同模式──

### Lớp 2  dòng dòng dòng (Run:ai Model Streamer)

> **【中文解读】**Thứ hai: Model Stream Loaded. NVIDIA Run:ai Model Streamer không cần cả file loaded.

Thay vì tải toàn bộ tập tin trước khi trả lời yêu cầu đầu tiên, lưu lượng tải vào bộ nhớ GPU layer-by-layer và bắt đầu xử lý ngay khi khối biến thể đầu tiên là cư dân. NVIDIA Run:ai Model Streamer được chuyển giao bản địa vào vLLM 2026.

> Không cần phải trả lời trước khi tải đầy đủ các file, mà thay vào đó sẽ tải trọng từng tầng vào bộ nhớ GPU, và chuyển tải khối đầu tiên được hoàn thành ngay sau khi bắt đầu xử lý. NVIDIA Run:ai Model Streamer trong vLLM 2026 năm nay cung cấp:兼容 S3、GCS 和本地 NVMe── thông qua cài đặt I/O và tính toán, sẽ giảm khoảng một nửa thời gian tải trọng của mô hình lớn.

### Lớp 3  GPU memory snapshots (Modal)

> **【中文解读】**Ba tầngGPU 内存快照──Modal 在第一次加载后对 GPU 状态(权重、CUDA graph、KV Cache 区域) làm điểm kiểm tra,后续重启直接反序列化到HBM比重启动快10x──这是2秒启动热 GPU"最接近的技术──代价是快照与 GPU 拓绑定如果Karpenter将你迁移到不同的 SKU,需要重制快照──

> **【拓展：冷启动优化策略叠加】**五层冷启动缓解可叠加使用:(1) 预播种镜像(消除镜像拉取) + (2) 模型流式加载(减半权重加载时间) + (3) GPU 快照(消除重重加载) + (4) 热池(避免冷启动) + (5) 分层加载(NVMe→DRAM→HBM) ――全叠加将 70B 模型从 328s冷启降到约15s22x 改善。选择哪几层取决于SLA 严格程度和预算。

Modal lấy một điểm kiểm tra của trạng thái GPU (năm trọng lượng, đồ thị CUDA, khu vực cache KV) sau khi tải đầu tiên. khởi động lại tiếp theo sẽ chuyển sang HBM 10x nhanh hơn so với khởi động lại. Đây là điều gần nhất để "bắt đầu một GPU ấm trong 2 giây".

> Modal trong lần đầu tiên tải về sau khi đối với trạng thái GPU ⋅权重、CUDA graph、KV 缓存区域) làm điểm kiểm tra。后续重启直接反序列化到HBM比重启动快 10倍。 đây là "2 giây khởi động热 GPU" gần nhất của các kỹ thuật。代价:快照与 GPU 拓绑定, nếu Karpenter 迁移到不同 SKU 需要重新制作快照。

### Lớp 4  hồ bơi ấm (min_workers=1)

> **【拓展：Serverless LLM 平台的冷启动对比】**2026 năm Serverless LLM 平台的冷启动表现:Modal 以 GPU 快照技术实现 2-4s(业界最快);Baseten 默认 5-10s,预加热后 <1s;AWS Lambda + 容器镜像通常10-30s(不含模型加载);原始 70B 模型冷启动 3-8 分钟。Modal 的快照技术是关键差它将 GPU 状态(权重 + CUDA graph + KV Cache 区域) 序列化,重启直反序列化到HBM,重启快 10x。代价是快照与 GPU 拓绑定,迁移到不同 SKU 需要重制快照──

Điều kiện đơn giản nhất: luôn luôn luôn chuẩn bị một bản sao. Chi phí là tốc độ giờ của một GPU 24x7.$0.85-$1.50/h để tránh bắt đầu lạnh 30s) và tử tế với những người lớn (trả tiền 4 $ / giờ để tránh bắt đầu lạnh 5 phút).

> Giải pháp đơn giản nhất: giữ một bản sao luôn sẵn sàng.$0.85-$1.50/小时 để tránh 30 giây khởi động lạnh),大模型则相对友好(付 $4/小时 để tránh 5 phút khởi động lạnh)。热池变为强制性SLA 值: thường là 70B+ 模型上 TTFT P99 < 60秒。

### Lớp 5  Lưu trữ cấp độ (ServerlessLLM)

ServerlessLLM xử lý lưu trữ như một hệ thống phân cấp: NVMe (nhanh nhưng lớn), DRAM (gần cấp nhưng trung bình), HBM (tín nhưng tức thời). trọng lượng được tải trước vào DRAM; tải theo yêu cầu vào HBM. Bảng báo cáo giảm độ trễ 10-200x trên tải lạnh so với đĩa ngây thơ-to-HBM. Việc áp dụng sản xuất là sớm nhưng tích hợp với vLLM tồn tại.

> ServerlessLLM sẽ lưu trữ theo cấp độ:NVMe(快但大)、DRAM(中等但分层)、HBM(小但即时)。权重预加载到DRAM;按需加载到HBM。论文报告冷启动延迟降低10-200倍──生产采用早,但已存在与vLLM的集成──

### Lớp 6  di chuyển trực tiếp (chương thức tiền thưởng)

Khi một nút không có sẵn (đánh trừ điểm, thoát node), mô hình truyền thống là khởi động lạnh một bản sao khác và thoát hàng yêu cầu. Di chuyển trực tiếp di chuyển các token đầu vào (kilobytes) đến một điểm đến mà có mô hình được tải và tính lại bộ nhớ cache KV trên điểm đến. Việc tính lại rẻ hơn so với việc chuyển GB bộ nhớ cache KV qua mạng.

> Khi các node không thể sử dụng khi đó, các mô hình truyền thống là lạnh khởi động một副本 khác并排空请求队列. thực时迁移将输入 token. thực时迁移将输入 token. thực时迁移将输入 token. thực时迁移将输入 token. thực时迁移将输入 token. thực时迁移将输入 token. thực时迁移将输入 token. thực时迁移将输入 token. thực时迁移将输入 token. thực时迁移将输入 token. thực时迁移将输入 token. thực时迁移将输入 token. thực时迁移将输入 token. thực时迁移将输入 token. thực时迁移将输入 token. thực时迁移将输入 token. thực时迁移将输入 token. thực时迁移将输入 token. thực时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时时

### Các toán học hồ bơi ấm

> **【中文解读】**热池数学: đối với dịch vụ P99 TTFT SLA 为 2s, vấn đề không phải là "热池 yes/no" mà là "多少热副本、哪些路径需要"──高价值交互路径(实时聊天、语音代理)→ min_workers=1-2;后台批处理路径(夜间分类)→ quy mô-to-zero 可接受;高级层级 → 按租户专用热副本。简单算术:5 个产品 1 热副本 = 5 × 24 × 30 = 3600 GPU-hours/月,无论是否有用户调用──

Đối với một dịch vụ với P99 TTFT SLA của 2s, câu hỏi không phải là "hồ ấm có/không" mà là "các bản sao ấm, và những con đường nào có được chúng".

> Đối với P99 TTFT SLA 为 2 秒的服务, vấn đề không phải là "热池 yes/no" mà là "how many热副本, which pathways need them" (Làm gì cần các tuyến đường).

- Các đường tương tác có giá trị cao (chát trực tiếp, đại lý giọng nói): `min_workers=1-2`- Tôi không biết.
  Trung ngữ翻译:高价值交互路径 (高价值交互路径)`min_workers=1-2`
- Các đường đợt sau (tỷ lệ phân loại hàng đêm): quy mô đến không được chấp nhận, khởi động lạnh 5-10 phút được chấp nhận.
  Trung文翻译:后台批处理路径(夜间分类): chấp nhận缩容到零,5-10 分钟冷启动可容忍。
- Tầng cao cấp: `min_workers`cho mỗi người thuê nhà có khả năng chuyên dụng.
  Trung ngữ翻译:高级层级:按租户 `min_workers`专用容量。

### Đánh giá trước khi tối ưu hóa

> **【中文解读】**70B 模型冷启动解剖(示意数据):节点供应50s + 镜像拉取180s + 权重到HBM 75s + 引擎初始化20s + 首次前向3s = 总计 328s。全缓解后:预播种消除镜像拉取、模型流式加载减半权重加载、GPU 快照消除重复初始化 = 约15s 总冷启动(22x 降低)。

Phân tích khởi động lạnh cho mô hình 70B trên một nút tươi (được minh họa):

| Phase | Time | Mitigation |
|-------|------|-----------|
| Node provision | 50s | Bottlerocket + pre-seeded image, warm pool |
| Image pull | 180s | Pre-seeded data volume (eliminate) |
| Weights to HBM | 75s | Model streamer (halve); GPU snapshot (eliminate) |
| Engine init | 20s | Persistent CUDA graph cache |
| First forward | 3s | Min inherent latency |
| **Total cold** | **328s** | |
| **Total with mitigations** | **~15s** | 22x reduction |

### Những con số mà bạn nên nhớ

- Biến lạnh mô-dal: 2-4s (với ảnh chụp GPU).
  Trung文翻译:Modal 冷启动:2-4 秒(使用GPU 快照) 』
- Baseten khởi động lạnh mặc định: 5-10s; dưới giây với quá trình nóng trước.
  Trung文翻译:Baseten 默认冷启动:5-10 秒;预加热后亚秒级。
- Bắt đầu lạnh 70B thô: 3-8 phút.
  Trung ngữ翻译:原始 70B 冷启动:3-8 分钟。
- Run:ai Model Streamer: ~ 2x trọng lượng tải tăng tốc.
  Trung文翻译:Run:ai Model Streamer:约 2倍权重加载加速──
- Lưu trữ cấp độ của ServerlessLLM: Giảm độ trễ 10-200x (năm giấy).
  Trung文翻译:ServerlessLLM 分层加载:10-200 倍延迟降低(论文数据)

## Hãy sử dụng nó để thực hiện
```figure
cold-start-pipeline
```

## Sử dụng nó

`code/main.py`mô hình một con đường khởi động lạnh với và không có mỗi giảm thiểu. báo cáo tổng thời gian khởi động lạnh, chi phí hồ bơi ấm và tỷ lệ yêu cầu chia cắt trên đó hồ bơi ấm tự trả cho mình.

> `code/main.py`建模有/无每种缓解的冷启动路径――报告总冷启动时间、热池成本和热池自付自足的亏平衡请求率──

## Chuyển nó đi.

Bài học này sẽ mang lại kết quả `outputs/skill-cold-start-planner.md`Với SLA, kích thước mô hình và hình dạng giao thông, chọn các giảm thiểu để xếp chồng lên.

> 本课产 出 `outputs/skill-cold-start-planner.md` Đưa SLA  mô hình quy mô và quy mô, chọn các chiến lược giảm thiểu 

## Tập luyện bài tập

1. Đi chạy`code/main.py`- Xét số lượng yêu cầu giảm cân trên đó một bản sao ấm rẻ hơn so với việc trả thuế khởi động lạnh thông qua giảm yêu cầu bổ sung tại SLO.
   Trung ngữ翻译:运行 `code/main.py` tính toán số tiền tăng giá hơn bằng SLO:
2. Bạn triển khai một mô hình 13B với P99 TTFT SLA của 3s. chọn ngăn xếp giảm thiểu (đất ít lớp) đạt được nó.
   Trung文翻译:你部署一个13B模型,P99 TTFT SLA 为 3 秒──选择实现它的最小缓解(最小层级)──
3. Bottlerocket pre-seeding loại bỏ thu hút hình ảnh nhưng trọng lượng vẫn tải từ snapshot đến HBM.
   Trung ngữ翻译:Bottlerocket 预播种 loại bỏ chụp ảnh, nhưng trọng lượng vẫn cần từ chụp nhanh tải lên HBM。 tính toán nhanh chụp hỗ trợ NVMe 以 7 GB/s 读取时 70B 模型的实际耗时──
4. Nhà cung cấp không có máy chủ của bạn cung cấp ảnh chụp nhanh GPU (Modal) và nhóm của bạn từ chối vì "phác chụp nhanh rò rỉ PII. " Phàn nàn cả hai bên  rủi ro thực tế là gì, và giảm thiểu là gì (phác chụp nhanh tạm thời, mã hóa, cách ly không gian tên)?
   Trung ngữ翻译:你的无服务器提供商提供 GPU 快照(Modal), nhưng nhóm từ chối vì "快照泄露 PII"──辩论双方实际风险是什么,缓解方案是什么(临时快照、加密、命名空间隔离)?
5. Thiết kế một chính sách hồ bơi ấm cấp bậc: bao nhiêu bản sao ấm cho người dùng trả tiền, người dùng thử nghiệm và khối lượng công việc hàng loạt?
   Trung ngữ翻译:设计分层热池策略:付费用户、试用用户和批处理工作负载各多少热副本?展示计算──

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Cold start | "the big pause" | Time from request to first token on a fresh replica |
| Warm pool | "always-on minimum" | `min_workers >= 1` to keep at least one replica ready |
| Pre-seeded image | "baked AMI" | Node image with container weights pre-resident |
| Bottlerocket | "AWS node OS" | AWS container-optimized OS with dual-volume snapshot support |
| Model streamer | "streaming load" | Overlap weights I/O with compute setup |
| GPU snapshot | "checkpoint to HBM" | Serialize post-load GPU state; deserialize on restart |
| Tiered loading | "NVMe + DRAM + HBM" | Hierarchy of storage tiers; load on demand |
| Live migration | "move tokens" | Transfer input (KB), recompute KV on destination |
| `min_workers` | "warm replicas" | Serverless minimum keep-alive count |
| Scale-to-zero | "full serverless" | No cost when idle; accept full cold-start tax |

## Xem thêm 延伸阅读

- [Modal — Cold start performance](https://modal.com/docs/guide/cold-start) Các tiêu chuẩn và kiến trúc điểm kiểm soát được công bố của Modal.
- [AWS Bottlerocket](https://github.com/bottlerocket-os/bottlerocket) mô hình chụp ảnh nhanh về khối lượng dữ liệu được gieo trước.
- [NVIDIA Run:ai Model Streamer](https://github.com/run-ai/runai-model-streamer) tải trọng chồng chéo với thiết lập tính toán.
- [Baseten — Cold-start mitigation](https://www.baseten.co/blog/cold-start-mitigation/) Quyển sách trước khi nóng lên.
- [ServerlessLLM paper (USENIX OSDI'24)](https://www.usenix.org/conference/osdi24/presentation/fu) Thiết kế tải hàng cấp.
- [NVIDIA — Disaggregated LLM Inference on Kubernetes](https://developer.nvidia.com/blog/deploying-disaggregated-llm-inference-workloads-on-kubernetes/) di cư trực tiếp cho các triển khai phân chia.
