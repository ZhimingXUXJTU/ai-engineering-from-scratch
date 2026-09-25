# Quick Caching và Semantic Caching Kinh tế  Economique 缓存 PR

> **Pricing snapshot dated 2026-04.**Các yêu cầu số dưới đây phản ánh thẻ giá bán hàng được thu thập tại ấn phẩm bài học này; kiểm tra với các tài liệu liên kết trước khi trích dẫn chúng theo dòng chảy.

> **【中文解读】**Phần này giới thiệu các gợi ý ngữ nghĩa缓存 thông qua các phản ứng của các gợi ý tương tự như缓存 để giảm chi phí suy đoán


> L2 ( cấp độ nhà cung cấp) prompt/prefix caching sử dụng lại sự chú ý KV cho các prefix lặp đi lặp lại  Các tài liệu cache prompt của Anthropic quảng cáo giảm chi phí lên đến 90% và giảm độ trễ 85% trên các yêu cầu dài; cho Claude 3.5 Sonnet đọc cache là $0.30/M vs $3,00/M tươi với TTL 5 phút và tiền thưởng viết 2 lần cho tùy chọn TTL 1 giờ (docs.anthropic.com, 2026-04). OpenAI prompt caching áp dụng tự động cho các prompt ≥1024 token và giá nhập cache với giá giảm giá khoảng 90% so với mới (platform.openai.com, 2026-04); tỷ lệ cache chính xác cho mỗi mô hình phụ thuộc vào thẻ tỷ lệ sống. L1 (tầng ứng dụng) lưu trữ ngữ nghĩa bỏ qua LLM hoàn toàn trên nhúng hit tương tự. Nhà cung cấp "95% chính xác" đề cập đến sự phù hợp, không đạt tỷ lệ  tỷ lệ đạt được sản xuất được báo cáo dao động từ 10% (tác thảo mở) đến 70% (FAQ có cấu trúc); không có nhà cung cấp nào xuất bản một đường cơ sở chính thức, vì vậy hãy coi chúng như viễn thông cộng đồng chứ không phải là đảm bảo. Các bẫy sản xuất: song song giết cache (N yêu cầu song song được phát hành trước khi ghi cache đầu tiên có thể làm tăng chi tiêu nhiều lần), và nội dung động bên trong tiền tố ngăn chặn cache tấn công hoàn toàn. ProjectDiscovery báo cáo chuyển từ 7% lên tỷ lệ hit 74% (2025-11) bằng cách di chuyển văn bản động ra khỏi tiền tố có thể lưu trữ.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy two-layer cache simulator) | **语言:** Python
**Prerequisites:** Phase 17 · 04 (vLLM Serving Internals), Phase 17 · 06 (SGLang RadixAttention) | **前置知识:** Phase 17 · 04 (vLLM Serving Internals), Phase 17 · 06 (SGLang RadixAttention)
**Time:** ~60 minutes | **时间:** ~60 minutes
**Type:** Learn
**Languages:** Python (stdlib, toy two-layer cache simulator)
**Prerequisites:** Phase 17 · 04 (Serving Engine Internals), Phase 17 · 06 (SGLang RadixAttention)
**Time:** ~60 minutes

>  **【前置】**学本节前请先掌握:Phase 17·04(vLLM)、Phase 17·06(RadixAttention)、Phase 11·04(Tài đặt dùng để语义缓存)。
>  **【类比】**缓存 = "翻历史聊天记录"──L2 提示缓存(Anthropic/OpenAI) = 服务商帮你存储(90% 成本降,85% 延迟降);L1 语义缓存 = tự dùng nhúng 找相似问题直接返回──陷:并行请求会破坏缓存、前里塞动态内容(时间) = 永远命中不了──ProjectDiscovery 把动态文本挪出可存前后,命中 7%率→74%──
> ️ **【易错点】**厂商宣传 "95% 准确率" là tỷ lệ phù hợp đúng hơn là tỷ lệ không có dự định.

## Mục tiêu học tập

- Sự phân biệt giữa L2 prompt/prefix caching (kV tái sử dụng tại nhà cung cấp) và L1 semantic caching (LLM bypass trên các prompt tương tự).
  Trung文翻译:区分 L2提示/前缓存(提供商级 KV 复用) 和 L1语义缓存(相似提示跳过 LLM) 』
- Giải thích Anthropic `cache_control`đánh dấu rõ ràng và hai tùy chọn TTL (5 phút so với 1 giờ) với nhân giá của chúng.
  中文翻译:解释 Antropic 的 `cache_control`显式标记和两种 TTL 选项(5 分钟对 1 小时) và giá乘数──
- Xét dự kiến tiết kiệm hàng tháng với tỷ lệ hit, hỗn hợp phản hồi/quick, và giá token.
  Trung文翻译:给定命中率、提示/响应比例和代币价,计算预期月度节省。
- Hãy cho tên mẫu chống đối tương đồng làm tăng tỷ lệ tiền bằng 5-10x và mẫu chống đối nội dung động làm giảm tỷ lệ hit.
  Trung ngữ翻译: nói ra việc tăng trưởng kế toán 5-10 lần của đồng hóa chống lại mô hình và dẫn đến sự sụp đổ tỷ lệ tỷ lệ sống động nội dung chống lại mô hình.

## Vấn đề  vấn đề giới thiệu

> **【中文解读】**提示缓存 có hai kiểu thất bại phổ biến: 1) 并行化反模式Agent 发出 10 个并行工具调用, tất cả các yêu cầu trong bộ nhớ cache đầu tiên viết 完成前到达,10 次写入、0 次读取,账单膨胀 5-10x; 2) 动态内容反模式系统提示中包含当前时间、请求 ID 等动态内容,每个请求都唯一,缓存中中率 0%──修复方法:将静态内容放缓存前,动态内容放缓存边界后──

> **【拓展：提示缓存的经济价值】**提示缓存是 LLM 成本优化中最直接的杆──Anthropic 的缓存 仅读 仅读$0.30/M（Claude 3.5 Sonnet），比 fresh input $3.00/M 便宜 10x──OpenAI đối với ≥1024 token gợi ý tự động缓存, đầu vào缓存 khoảng 10% giá của đầu vào mới── trong sản xuất RAG 系统, tỷ lệ trung bình缓存 của shared system gợi ý có thể lên đến 60-80%, mỗi tháng có thể tiết kiệm hàng triệu đô la──语义缓存(L1) trong các trường hợp FAQ cấu trúc có thể lên đến 40-70% tỷ lệ sống──

Bạn thêm bộ nhớ cache nhanh vào dịch vụ RAG của bạn. Tài khoản vẫn ổn định. Bạn đo tỷ lệ hit; nó là 7%. Các yêu cầu của bạn trông tĩnh nhưng họ không phải là  yêu cầu hệ thống bao gồm ngày hiện tại định dạng đến phút, một ID yêu cầu, và một ví dụ ngẫu nhiên sắp xếp lại cho sự đa dạng. Mỗi yêu cầu viết một mục bộ nhớ cache mới, đọc bằng không.

> **【中文解读】**
> 提示缓存分两层:L2(提供商级) 重用重复前的 KV cacheAnthropic 声称缓存读取成本降低90%、延迟降低85%;L1(应用级)语义缓存存在嵌入相似度命中时直接跳过LLM。 nhưng hai phản模式 sẽ phá hủy缓存效果:(1) prompt 中的动态内容(时间、请求 ID) 阻止缓存命中;(2) 并行请求在第一个缓存写入前全部到达,导致N 次取写入次读零──

Một cách riêng biệt, đại lý của bạn chạy mười cuộc gọi song song với công cụ mỗi câu hỏi của người dùng. Tất cả mười đều đến với nhà cung cấp trước khi ghi nhớ cache đầu tiên hoàn thành. mười viết, không đọc. hóa đơn của bạn là 5-10 lần so với "với ghi nhớ cache" được cho là chi phí.

Caching là một giao thức, không phải là một cờ.

## Khái niệm cốt lõi

### L2  Caching prompt/prefix của nhà cung cấp

> **【中文解读】**L2 层(提供商级)提示缓存复用重复前的注意力 KV──Anthropic 使用显式 `cache_control`标记,TTL 选项有5分钟(写入成本 1.25x) 和 1 小时(2x),读取成本仅为新鲜输入的1/10──OpenAI đối với ≥1024 token提示自动缓存,无需标记──Google Gemini 通过显式 API 提供语境缓存──自部署方案使用vLLM tiền đề缓存或SGLang RadixAttention──

Nhà cung cấp lưu trữ sự chú ý KV cho một prefix có thể lưu trữ và sử dụng lại nó trên yêu cầu tiếp theo phù hợp với prefix. Bạn trả chi phí viết một lần, đọc gần như miễn phí.

**Anthropic (Claude 3.5 / 3.7 / 4 series)**: rõ ràng `cache_control`TTL: 5 phút (tài liệu chi phí 1.25x cơ sở) hoặc 1 giờ (tài liệu chi phí 2x cơ sở).$0.30/M on Claude 3.5 Sonnet vs $3,00/M tươi  10 lần rẻ hơn (docs.anthropic.com, từ năm 2026-04). Giá khác nhau cho mỗi mẫu (Opus/Haiku được xuất bản riêng); luôn luôn kiểm tra chéo trang giá trực tiếp.

**OpenAI**: tự động lưu trữ trước khi gửi các thông báo ≥1024 token (platform.openai.com, 2026-04). Không có cờ rõ ràng. Cài nhập trước khi gửi là khoảng 10 lần rẻ hơn so với mới trên thẻ tốc độ gpt-4o / gpt-5 hiện tại. Cả các tài liệu và các bản ghi bản phát hành đều không công bố một đường cơ sở chính thức về tỷ lệ hit; báo cáo cộng đồng tập hợp khoảng 3060% với thiết kế nhanh chóng cẩn thận.`usage.cached_tokens`để đo lường của riêng bạn.

**Google (Gemini)**: cache ngữ cảnh thông qua API rõ ràng; 1M-token context có nghĩa là cache trả tiền nhiều hơn nữa.

**Self-hosted (vLLM, SGLang)**: Giai đoạn 17 · 06 bao gồm RadixAttention  mô hình tương tự trong tính toán của bạn.

### L1  Caching ngữ nghĩa cấp ứng dụng

> **【中文解读】**L1 层(应用级)语义缓存在调用 LLM 之前,对提示做哈希和嵌入查找。 nếu tìm thấy sự tương đồng vượt quá值(通常 0.95+) của yêu cầu缓存, trực tiếp trả lại缓存响应。

Trước khi gọi LLM, hãy chọn hash prompt, nhúng nó và tìm kiếm yêu cầu được lưu trữ trong cache tương tự (sự tương đồng đồng đồng tính trên ngưỡng, thường là 0,95+).

Mã nguồn mở: Redis Vector Similarity, GPTCache, Qdrant. Tiếp thị: Portkey Cache, Helicone Cache.

Các yêu cầu chính xác của nhà cung cấp đề cập đến việc trả lời được lưu trữ trong cache trở lại thường xuyên như thế nào là phù hợp theo nghĩa ngữ  chứ không phải là bạn đánh số thường xuyên.

- - Tự động trò chuyện: 10-15%.
- Các câu hỏi thường gặp / hỗ trợ có cấu trúc: 40-70%.
- Các câu hỏi mã: 20-30% (những biến thể nhỏ giết chết các lượt truy cập).
- Các đại lý giọng nói lặp lại các lời nhắc: 50-80% (định dạng bình thường giọng nói cố định).

### Phương pháp chống đồng đều hóa

> **【拓展：并行化反模式的真实案例】**Kết quả: 10 lần viết vào溢价、0次读取折扣── sửa chữa phương pháp: trình tự đầu tiên先单独发送请求 1,等缓存 填充后再发送 2-10── tăng 300ms đến đầu tiên công cụ调整, nhưng tiết kiệm 5-10x 账单── Dự án phát hiện 通过动态内容将移动缓存, dự án sẽ tăng từ 7% 升至 74% 之前的案例,2025年11月发布案例)

Trưởng lý của bạn thực hiện 10 cuộc gọi công cụ song song. Tất cả 10 đều có cùng một lệnh báo 4K-token hệ thống. Anthropic cache viết là theo yêu cầu; đầu tiên cache-tập hoàn thành khoảng 300 ms sau khi nhà cung cấp thấy lệnh báo. Các yêu cầu 2-10 đến trong cùng một cửa sổ millisecond và mỗi thấy cache bị bỏ lỡ. Bạn trả 10 tiền thưởng viết, 0 giảm giá đọc.

Xác định: hàng với thứ tự đầu tiên  thực hiện yêu cầu 1 một mình, sau đó phát 2-10 sau khi bộ nhớ nhớ bộ nhớ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ nhớ bộ

### Các nội dung động chống mô hình

Đơn vị hệ thống của bạn trông như:

```
You are a helpful assistant. The current time is 14:32:17.
User ID: abc123. Today is Tuesday...
```

Mỗi yêu cầu đều độc đáo, mỗi yêu cầu đều có điểm số không truy cập.

Xác định: di chuyển mọi thứ thực sự tĩnh vào tiền tố có thể lưu trữ; thêm nội dung động sau ranh giới lưu trữ:

```
[cacheable]
You are a helpful assistant. [rules, examples, instructions]
[/cacheable]
[dynamic, not cached]
Current time: 14:32:17. User: abc123.
```

ProjectDiscovery chuyển từ 7% lên 74% tỷ lệ hit cache theo cách này và xuất bản giải phẫu.

### Lưu trữ hàng loạt + cache cho tải trọng làm việc qua đêm

Các API hàng loạt (Phase 17 · 15) cung cấp giảm 50% khi quay 24 giờ. Tiền nhập được lưu trữ trên cùng cung cấp cho bạn ~ 10 lần trên cùng. Nhiệm vụ phân loại, dán nhãn và sản xuất báo cáo qua đêm có thể giảm xuống ~ 10% chi phí không được xếp chồng đồng bộ bằng cách xếp chồng.

### Những con số mà bạn nên nhớ

Điểm giá được ghi lại 2026-04 từ các tài liệu nhà cung cấp liên kết và trôi qua mỗi vài tháng  kiểm tra lại trước khi dựa vào chúng.

- Anthropic được lưu trữ đọc: $0.30/M trên Claude 3.5 Sonnet, khoảng 10 lần rẻ hơn so với đầu vào mới (docs.anthropic.com).
- Antropic cache write premium: 1.25x (5-min TTL) hoặc 2x (1-hour TTL).
- OpenAI tự động lưu trữ: áp dụng cho các mã thông báo ≥1024 mã thông báo; nhập khẩu được lưu trữ trong cache với giá khoảng 10% của nhập khẩu mới trên thẻ giá hiện tại (platform.openai.com).
- Tỷ lệ hit cache ngữ nghĩa (được báo cáo bởi cộng đồng): ~ 10% mở trò chuyện; lên đến ~ 70% FAQ có cấu trúc. Không có đường cơ sở được cung cấp bằng văn bản.
- ProjectDiscovery: 7% → 74% tỷ lệ hit bằng cách di chuyển động từ tiền tố (blog dự án, 2025-11).
- Phương pháp chống đồng bộ hóa: báo cáo điển hình về lạm phát hóa đơn 510x khi các yêu cầu song song N bỏ lỡ ghi nhớ cache đầu tiên.

## Hãy sử dụng nó để thực hiện

> **【中文解读】**
>                                                                                                                                                                                                                                                               `cache_control`标记静态前──实测案例:把动态内容移出缓存前,命中率从7% 跳到74%── đối với RAG 系统,静态系统提示 + 检索到的文档属于缓存范围,用户问题不属于──

> **【拓展：提示缓存→成本优化】**提示缓存是 LLM 成本优化最直接的手段──Anthropic Claude 的缓存读取价格为$0.30/M token，不到新鲜输入 $Một phần mười của 3.00/M. OpenAI cho 1024+ token tự động dự trữ, giá nhập dự trữ giảm khoảng 90%. Đối với hệ thống RAG xử lý hàng triệu yêu cầu hàng ngày, dự trữ dự trữ có thể làm giảm tính toán API hàng tháng từ hàng trăm nghìn USD xuống hàng trăm ngàn USD.
```figure
semantic-cache-hit
```

## Sử dụng nó

`code/main.py`mô phỏng L1 + L2 lưu trữ trên tải trọng công việc hỗn hợp. báo cáo đánh giá, hóa đơn, và cho thấy hình phạt song song.

> `code/main.py`mô phỏng L1 + L2 lưu trữ trên tải trọng công việc hỗn hợp. báo cáo đánh giá, hóa đơn, và cho thấy hình phạt song song.

> `code/main.py`mô phỏng L1 + L2 lưu trữ trên tải trọng công việc hỗn hợp. báo cáo đánh giá, hóa đơn, và cho thấy hình phạt song song.

## Chuyển nó đi.

> **【拓展：缓存 + 批处理叠加优化】**缓存与批处理 API(Phase 17·15) 叠加效果:批处理 API 50% 折扣 + 缓存输入 ~10x 折扣 = 约 10% của đồng步-未缓存成本──隔夜分类、标记和报告生成工作负载可通过叠加这两种优化降至基准约10%──关键是将提示模板视为缓存键修复排序、移动内容,这是最容易忽视但最有效的优化──

Bài học này sẽ mang lại kết quả `outputs/skill-cache-auditor.md`Với mô hình và lưu lượng truy cập nhanh chóng, kiểm toán khả năng lưu trữ và khuyến cáo tái cấu trúc.

> 本课产 出 `outputs/skill-cache-auditor.md`Với mô hình và lưu lượng truy cập nhanh chóng, kiểm toán khả năng lưu trữ và khuyến cáo tái cấu trúc.

## Tập luyện bài tập

1. Đi chạy`code/main.py`- Đổi cờ tương đồng.
   Trung ngữ翻译:运行 `code/main.py`◊ chuyển đổi và chuyển đổi  tăng trưởng kế toán
2. Đặt ngày cho hệ thống của bạn, hãy di chuyển nó ra.
   Trung ngữ翻译:你的系统提示包含日期──将它移出──展示前后命中率数学──
3. Xét điểm hòa cho 1 giờ TTL (2x viết) so với 5 phút TTL (1.25x viết) với tốc độ đến yêu cầu của bạn.
   Trung文翻译:计算 1 小时 TTL(2x 写入成本) VS 5 分钟 TTL(1.25x 写入成本) 的亏平衡──
4. Cache ngữ nghĩa ở ngưỡng 0,95 đạt 20%. ở mức 0,85 đạt 50% nhưng bạn thấy các phản ứng được lưu trữ trong cache không chính xác.
   Trung文翻译:语义缓存值 0.95 时命中率 20%──0.85 时命中率 50% Nhưng bạn sẽ thấy幻觉──值设多少?
5. Bạn xếp hàng 10 câu hỏi phụ song song cho mỗi câu hỏi của người dùng.

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| L2 prompt cache | "prefix cache" | Provider stores KV for repeated prefix |
| `cache_control` | "Anthropic cache marker" | Explicit attribute marking cacheable blocks |
| Cache write premium | "write tax" | Extra cost for first miss-to-cache (1.25x or 2x) |
| L1 semantic cache | "embedding cache" | App-level hash-and-embed before calling LLM |
| GPTCache | "LLM caching lib" | Popular OSS L1 cache library |
| Cache hit rate | "hits / total" | Fraction of requests served from cache |
| Parallelization anti-pattern | "the N-write trap" | N parallel requests miss cache N times |
| Dynamic content trap | "the time-in-prompt trap" | Dynamic bytes in prefix kill hit rate |
| RadixAttention | "intra-replica cache" | SGLang's prefix-cache implementation |

## Xem thêm 延伸阅读

- [Anthropic Prompt Caching](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching) chính thức `cache_control`ngữ nghĩa và TTL.
- [OpenAI Prompt Caching](https://platform.openai.com/docs/guides/prompt-caching) Hành vi lưu trữ tự động và đủ điều kiện.
- [TianPan — Semantic Caching for LLMs Production](https://tianpan.co/blog/2026-04-10-semantic-caching-llm-production)
- [ProjectDiscovery — Cut LLM Costs 59% With Prompt Caching](https://projectdiscovery.io/blog/how-we-cut-llm-cost-with-prompt-caching)
- [DigitalOcean / Anthropic — Prompt Caching](https://www.digitalocean.com/blog/prompt-caching-with-digital-ocean)
