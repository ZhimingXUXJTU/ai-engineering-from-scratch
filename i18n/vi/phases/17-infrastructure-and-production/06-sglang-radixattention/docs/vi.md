# SGLang và RadixCảnh sát cho các tải trọng công việc nặng trước.
# Prefix-Cache Serving  RadixAttention và KV Reuse

> Chế độ dự trữ KV như một tài nguyên có thể sử dụng lại được lưu trữ trong một cây gốc, và thay đổi lịch trình với nó: thay vì FCFS (lần đầu tiên đến, lần đầu tiên phục vụ) như các lịch trình vLLM, một lập trình viên có ý thức về cache ưu tiên các yêu cầu với các phụ đề chia sẻ dài hơn  hiệu quả là một chiều sâu đầu tiên xuyên qua gốc để các nhánh nóng vẫn ở trong HBM. SGLang là động cơ đã xây dựng phục vụ cho ý tưởng này. Trên Llama 3.1 8B với các lời nhắc 1K giống như ShareGPT, SGLang đạt ~ 16.200 tok/s đến ~ 12.500 vLLM, một cạnh ~ 29%. Với khối lượng công việc RAG nặng tiền tố, lợi thế đạt 6,4x. Trên các khối lượng công việc hình dạng nhượng bộ giọng nói, tỷ lệ truy cập cache đã được xóa 86%. Được triển khai trên 400.000+ GPU vào năm 2026 trên xAI, LinkedIn, Cursor, Oracle, GCP, Azure, AWS. Vấn đề là số 6.4x bị biến mất khi lệnh tiền tố không phù hợp.

> **【中文解读】**Bài viết này giới thiệu SGLang và RadixAttention 通过前共享优化推理效率──
**Type:** Learn
**Languages:** Python (stdlib, toy radix-tree cache + cache-aware scheduler)
**Prerequisites:** Phase 17 · 04 (Serving Engine Internals), Phase 14 (Agentic RAG)
**Time:** ~75 minutes


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy radix-tree cache + cache-aware scheduler) | **语言:** Python（标准库，radix tree 缓存 + 缓存感知调度器模拟）
**Prerequisites:** Phase 17 · 04 (vLLM Serving Internals), Phase 14 (Agentic RAG) | **前置知识:** Phase 17 · 04（vLLM 服务内部）, Phase 14（Agentic RAG）

>  **【前置】**学本节前请先掌握:Phase 17·04(vLLM) 、Phase 14(Agentic RAG) ・SGLang dùng cây gốc 复用 KV cache比 vLLM FCFS 更智能的调度。
>  **【类比】**SGLang RadixAttention = " kỷ niệm图书馆"。vLLM = 每次重新查目录;SGLang = 热门前(系统提示+RAG context)存 radix tree 复用。Llama 3.1 8B 在 ShareGPT 上比 vLLM 快 29%;RAG 工作负载快 6.4 倍;语音克隆场景缓存命中 86%──2026 部署在40万+ GPU(xAI、LinkedIn、Cursor)──关键:前必须稳定排序才有效──
**Time:** ~75 minutes | **时间:** ~75 分钟

## Mục tiêu học tập

- Chụp đồ họa RadixAttention: cách các tiền tố được lưu trữ trong một cây radix và cách các khối KV được chia sẻ qua các chuỗi có gốc cùng một nhánh.
  Trung文翻译:绘制 RadixAttention:前如何在radix树中存储,KV 块如何在同分支的序列间共享──
- Giải thích lập trình biết cache và tại sao FCFS là sai đối với giao thông cao tiền tố.
  Trung ngữ翻译: giải thích缓存感知调度以及为什么FCFS đối với trước密集流量 là sai lầm.
- Xét tốc độ dự kiến cho khối lượng công việc với tốc độ hit prefix-cache và phân phối chiều dài nhanh chóng.
  Trung ngữ翻译:给定前缓存命中率和快速长度分布,计算工作负载的预期加速──
- Hãy cho tên kỷ luật đặt hàng nhanh cho số 6.4x thực với một lợi thế bị mất.
  Trung ngữ翻译:说出使 6.4x 加速成为现实而非流失的快速 排序纪律──

## Vấn đề  vấn đề giới thiệu

> **【中文解读】**传统推理服务将每个请求的提示视为不透明即使5000 RAG 请求共享相同的2000代币 系统提示,vLLM也将执行5000次完整的预填――RadixAttention 通过将代币序列存储在radix tree中解决这个问题:新请求沿树匹配已有前,只需预填 新增的后部分──挑战在调度FCFS(先来先服务) 破坏前局部性,需要缓存意识调度器优先服务共享前的请求──

> **【拓展：前缀共享在 Agent 场景的价值】**Agent 工作负载天然具有前共享特征:系统提示、工具方案、少数拍示例、对话历史跨请求重复──Cursor(AI 代码编辑器) trong năm 2026 báo cáo của mình Agent 调用中系统提示 + 工具定义占快速的80%,仅仅用户查询部分不同──使用SGLang的 RadixAttention 后,这些共享前只需计算一次,后续请求复用KV Cache,将推理成本降低60-80%.──

Các ứng dụng truyền thống xử lý mỗi yêu cầu như là không minh bạch. Ngay cả khi 5.000 yêu cầu RAG tất cả bắt đầu với cùng một yêu cầu hệ thống 2.000 token cộng với nguyên tắc lấy lại tương tự, vLLM điền trước 2000 token tiền tố 5.000 lần. GPU làm việc tương tự nhiều lần.

> 经典服务将每次请求的快速 视为不透明的──即使5000 RAG请求都以相同的2000代币 系统提示加相同检查前开始,vLLM也会预填那2,000代币前5,000次──GPU 重复做同样工作──

Quan sát: các yêu cầu trong tải công việc của agentc và RAG hầu như luôn chia sẻ các tiền đề dài. Các yêu cầu hệ thống, các sơ đồ công cụ, vài lần chụp ví dụ, tiêu đề truy xuất, lịch sử cuộc trò chuyện  tất cả lặp lại qua các yêu cầu. Nếu bạn lưu trữ bộ nhớ cache KV cho tiền đề đó một lần và sử dụng lại, bạn sẽ không phải điền lại nó một lần nữa.

> 观察:Agent 和 RAG 工作负载中的提示 几乎总是共享长前──系统提示、工具方案、少数截图示例、检索头、对话历史都在请求间重复── nếu bạn lưu trữ một lần trước KV 缓存并复用,就不需要再次预填──

RadixAttention thực hiện chính xác điều này. Các mã thông báo được lập chỉ mục trong một cây gốc; mỗi nút sở hữu các khối KV cho chuỗi mã thông báo trên con đường của nó từ gốc. Một yêu cầu mới đi qua cây: bất kỳ nút nào có mã thông báo phù hợp lại sử dụng các khối KV của nút đó. Chi phí điền trước trở nên tương xứng với hậu tố "mới", chứ không phải yêu cầu đầy đủ.

> RadixAttention 正是这样做──Token 在 radix tree 中索引; mỗi node có từ gốc đến đường dẫn của token 序列 của KV 块──新请求遍历树: bất kỳ token 匹配的节点复用该节点的 KV 块──预填成本与"新"后成正比,而不是完整的提示──

Thách thức là lập lịch. Nếu hai yêu cầu chia sẻ 2000 mã thông báo trước và một thứ ba chia sẻ chỉ 200 mã thông báo của cùng một mã thông báo trước, bạn muốn phục vụ hai yêu cầu chia sẻ dài cùng nhau để các mã thông báo trước dài vẫn ở trong HBM. FCFS làm ngược lại  nó phục vụ ai đến đầu tiên, có khả năng trục xuất chi nhánh nóng trước khi yêu cầu dài tiếp theo đạt được.

> 挑战 nằm trong điều chỉnh. Nếu hai yêu cầu chia sẻ 2.000 token trước, thứ ba chỉ chia sẻ 200 token, bạn muốn đồng thời phục vụ hai yêu cầu chia sẻ dài để giữ dài trước trong HBM.

## Khái niệm cốt lõi

### Cây gốc như một chỉ số KV

> **【中文解读】**Cây Radix (Radix tree) là cấu trúc dữ liệu cốt lõi của SGLang. Mỗi node có một token  phạm vi và đối phó với các khối KV. Ứng dụng mới vào thời gian phù hợp: hệ thống提示匹配节点复用124 khối KV,文档分支匹配复用31块, chỉ cần phân bổ 4-6 khối cho vấn đề mới. Ví dụ: 160 khối tổng thể, cây radix chỉ cần 4 khối tính toán mới ((40x 省省).

Một cây gốc (trie nhỏ gọn) lưu trữ chuỗi token. Mỗi nút sở hữu một phạm vi token và các khối KV được tính toán cho phạm vi đó. Trẻ em mở rộng chuỗi một hoặc nhiều token.

> Cây Radix (紧前树) lưu trữ token 序列── mỗi节点 có một token 范围和为该范围计算的 KV块──子节点扩展序列一个或多个 token──

```
root
 |- "You are a helpful assistant..."  (2,000 tokens, 124 KV blocks)
      |- "Context: <doc A>..."        (500 tokens, 31 blocks)
           |- "Question: Alice..."    (80 tokens, 5 blocks)
           |- "Question: Bob..."      (95 tokens, 6 blocks)
      |- "Context: <doc B>..."        (520 tokens, 33 blocks)
```

Một yêu cầu mới được gửi với hệ thống prompt + "Context: <doc A>" + "Question: Carol". Scheduler chạy: hệ thống prefix phù hợp (124 khối được sử dụng lại), doc-A nhánh phù hợp (31 khối được sử dụng lại), sau đó chỉ phân bổ các khối mới cho "Question: Carol" (4 khối). Chi phí prefill: 4 khối mã thông báo mới. Không cây: 160 khối. ~40x tiết kiệm trên prefill.

> Một yêu cầu mới với hệ thống提示 + "Context: <doc A>" + "Question: Carol" 进入──调度器遍历:系统前匹配(复用124块),doc-A 分支匹配(复用31块),然后只为 "Question: Carol" 分配新块(4块)──预填成本:4块新代币──没有树:160块──预填节省约40倍──

### Lịch trình lưu trữ

> **【中文解读】**Hai chiến lược quan trọng của điều chỉnh cảm nhận缓存: 1) điều chỉnh ưu tiên sâu  dịch vụ ưu tiên với yêu cầu chia sẻ chia sẻ chia sẻ của tập hợp vận hành hiện tại, giữ nhiệt điểm chia sẻ chia sẻ tại HBM; 2) phân cấp LRU 淘汰以整棵分支为单位淘汰(从最少使用叶开始), chứ không phải là một khối đơn lẻ.

Việc tái sử dụng được hỗ trợ bởi Radix Tree là vô ích nếu bộ nhớ cache bị hỏng.

> Nếu lưu trữ liên tục hoạt động, việc sử dụng lại cây gốc không có ý nghĩa.

1. **Depth-first dispatch**Khi chọn yêu cầu tiếp theo từ hàng, hãy chọn yêu cầu được gốc ở cùng một nhánh với bộ chạy hiện tại. Điều này giữ cho nhánh nóng bị gắn.
   Trung ngữ翻译:**深度优先调度**❖ Khi chọn yêu cầu tiếp theo trong hàng, chọn ưu tiên với yêu cầu của tập hợp và chi nhánh hiện tại.
2. **LRU at branch level, not block level**. Tránh ra toàn bộ nhánh (bắt đầu từ lá ngắn nhất sử dụng) thay vì các khối riêng lẻ, do đó hình dạng cache phù hợp với hình dạng gốc.
   Trung ngữ翻译:**分支级 LRU**❖ loại bỏ toàn bộ phân支 (~ từ ít nhất sử dụng của các lá bắt đầu), thay vì một khối, để các dạng dự trữ phù hợp với hình dạng gốc ∼

FCFS vi phạm cả hai, một yêu cầu chia sẻ 2.000 token nằm phía sau một yêu cầu chia sẻ 50, sau đó chi nhánh 2.000 token bị đuổi để chấp nhận một token 50.

> FCFS 违反两者── một yêu cầu chia sẻ 2.000 token排在共享 50 token yêu cầu sau đó 2.000 token 分支被淘汰以接受50 token yêu cầu──

### Số điểm chuẩn bạn nên ghi nhớ

- Llama 3.1 8B, H100, ShareGPT 1K yêu cầu: SGLang ~ 16,200 tok/s so với vLLM ~ 12,500 (~ 29% cạnh).
  中文翻译:Llama 3.1 8B,H100,ShareGPT 1K prompt:SGLang 约 16,200 tok/s vs vLLM 约 12,500(约 29% 优势)。
- RAG nặng tiền tố (hình thức tương tự + tài liệu tương tự, câu hỏi khác nhau): lên đến 6,4x trên SGLang.
  Trung文翻译:前密集 RAG(同系统 + 相同文档,不同问题):SGLang 上最高 6.4 倍。
- Nồng độ công việc nhân bản giọng nói: 86,4% tỷ lệ hit prefix-cache.
  Trung ngữ翻译:语音克隆工作负载:86.4% 前缓存命中率。
- Tỷ lệ sản xuất đạt được trên khách hàng SGLang: 50-99% tùy thuộc vào kỷ luật nhanh chóng.
  Trung ngữ翻译:SGLang 客户的生产命中率:50-99%, tùy thuộc vào 排序纪律.
- Được triển khai trên 400.000+ GPU vào năm 2026.
  Trung ngữ翻译:2026 年部署在 400,000+ GPU 上.

### Việc đặt hàng đã làm cho anh

> **【中文解读】**6.4x tăng tốc phụ thuộc vào quy trình mô hình đề xuất phù hợp. Nếu khách hàng có thời gian xây dựng.`[system, tools, context, history, question]`, đôi khi xây dựng`[system, context, tools, history, question]`,radix tree  không thể tìm thấy chia sẻ trước  đối với con người trông giống nhau, đối với cây radix là hai chuỗi khác nhau. 杆 của kỹ sư là: sẽ提示模板视为缓存键.

> **【拓展：SGLang 在生产中的采用】**SGLang đã được triển khai trên hơn 400.000 khối GPU vào năm 2026, người dùng bao gồm xAI(Grok)、LinkedIn、Cursor、Oracle, cũng như dịch vụ quản lý của GCP/Azure/AWS。 điểm ưu điểm cốt lõi là Agent 和 RAG 工作负载

Số 6.4x dựa trên đơn đặt hàng mẫu đơn giản nhất quán. Nếu khách hàng của bạn xây dựng các đơn giản như `[system, tools, context, history, question]`trong một số yêu cầu và `[system, context, tools, history, question]`Trong những người khác, cây không thể tìm thấy tiền tố được chia sẻ.

> 6.4x số phụ thuộc vào phù hợp 模板排序 模板排序 模板排序 模板排序 模板排序 模板排序 模板排序 模板排序 模板排序 模板排序 模板排序 模板排序 模板排序 模板排序 模板排序 模板排序 模板排序 模板排序 模板排序 模板排序 模板排序 模板排序 模板排序 模板排序 模板排序 模板排序 模板排序 模板排序 模板排序 模板排序 模板排序 模板排序 模板排序 模板排序 模板排序 模板排序 模板排序 模板 模板 模板 模板 模板 模板 模板 模板 模板 模板 模板 模板 模板 模板 模板 模板 模板 模板 模板 模板 模板 模板 模板 模板 模板 模板 模板 模板 模板 模板 模板 模板 模板 模板 模板 模板 模板 模板 模板 模板 模板 模板 模板 模板 模板 模板 模板 模板 模板 模板 模板 模板 模板 模板 模板 模板 模板`[system, tools, context, history, question]`, trong các yêu cầu khác xây dựng `[system, context, tools, history, question]`, cây không thể tìm thấy chia sẻ trước 🏼 đối với con người trông giống như chia sẻ trước 🏻 đối với cây gốc là hai chuỗi khác nhau 🏼

Chế độ đầu tư của kỹ sư: mẫu yêu cầu của bạn là một khóa cache. Dũng chỉnh thứ tự. Đặt mọi thứ không thay đổi (hệ thống, công cụ, sơ đồ) trước. Đặt ngữ cảnh tìm kiếm tiếp theo. Đặt câu hỏi người dùng cuối cùng. Đừng để nội dung động vào tiền tố.

> 工程师的杆:你的提示 模板是缓存键──固定顺序──将所有不可变内容(系统、工具、方案) 放最前──检索上下文放中间──用户问题放最后──不要在可缓存前中交错动态内容──

Trường hợp thực tế từ nghiên cứu: di chuyển nội dung động ra khỏi tiền tố có thể lưu trữ trong cache đã mất một triển khai từ 7% đến 74% tỷ lệ hit cache trong một thay đổi.

> Ví dụ thực tế trong nghiên cứu: chuyển nội dung động từ dự trữ sẵn, tỷ lệ dự trữ dự trữ được triển khai một lần tăng từ 7% lên 74%

### Ở đâu RadixAttention thắng và thua

> **【拓展：RadixAttention vs Prefix Caching 性能对比】**SGLang với vLLM có khả năng lưu trữ trước tương đối: trên Llama 3.1 8B H100 trên, SGLang đạt ~16,200 tok/s so với vLLM ~12,500 tok/s;; 29% 优势; trên trọng lượng trước 重度前 重复使用 RAG 工作负载 đạt 6.4x;语音克隆工作负载缓存命中率 86% . Nhưng vLLM vào năm 2026 cũng sẽ thêm tiền cài đặt cache và cache-aware router  Rust 实现) 距差缩小但未完全消除,因为 toàn bộ SGLang  là 设计 radix-first .

Chiến thắng:
- RAG (chương tự thu thập cùng một câu hỏi khác nhau).
  Trung文翻译:RAG(相同检索前,不同问题)
- Các đại lý (chương trình công cụ tương tự, truy vấn khác nhau).
  中文翻译:Agent(相同工具 schema,不同查询) 』
- Nói chuyện với hệ thống nhanh chóng.
  Trung ngữ翻译:长系统提示的聊天──
- Lượng công việc bằng giọng nói / thị giác với các đoạn văn lặp đi lặp lại.
  Trung ngữ翻译:重复前的语音/视觉工作负载。

Thiệt (tái trở lại mức độ thông qua vLLM):
- Sản xuất một lần với các yêu cầu độc đáo (sự hoàn thành mã, trò chuyện mở không cần yêu cầu hệ thống).
  Trung文翻译:独立 prompt 的单次生成(代码补全、无系统提示的开放聊天) 』
- Các lệnh động động nơi mỗi yêu cầu liên kết nội dung độc đáo vào tiền tố.
  Trung ngữ翻译: Mỗi yêu cầu trong có thể lưu trữ trước中交错独特内容的动态提示──

### Tại sao đây là một vấn đề lập trình, không chỉ là một vấn đề hạt nhân

Bạn có thể thực hiện KV tái sử dụng như một thủ thuật hạt nhân. Nhìn sâu của SGLang là việc tái sử dụng chỉ trả tiền nếu lập trình viên giữ cho chi nhánh nóng cư trú. Chính sách " tái sử dụng nếu có sẵn" ngây thơ sẽ làm tăng bộ nhớ cache dưới tải hỗn hợp.

> Bạn có thể thực hiện KV  sử dụng lại để sử dụng kỹ thuật hạt nhân. Nhìn nhận của SGLang là chỉ có giá trị trong điều chỉnh để giữ nhiệt phân chia thường trú thời gian.

### Sự tương tác với vLLM

Hai hệ thống này không phải là đối thủ cạnh tranh nghiêm ngặt.`--enable-prefix-caching`Vỗng trống đã đóng nhưng không biến mất hoàn toàn  toàn bộ hàng SGLang là radix-first; vLLM ghép nó vào. Đối với tải trọng công việc bị chi phối bởi việc tái sử dụng tiền tố, SGLang vẫn là mặc định. Đối với các mục đích chung không có mô hình tiền tố mạnh mẽ, vLLM vẫn bằng hoặc tốt hơn.

> 两个系统不是严格竞争者──2026年 vLLM 添加了前缓存(`--enable-prefix-caching`(vLLM là kết nối trên trên trên trên. Đối với tải trọng công việc chủ yếu của trước, SGLang vẫn là tùy chọn mặc định. Đối với không có mô hình trước mạnh, VLLM vẫn tương đương hoặc tốt hơn.

## Hãy sử dụng nó để thực hiện
```figure
roofline
```

## Sử dụng nó

`code/main.py`thực hiện một bộ nhớ cache KV toy radix-tree cộng với một trình lập lịch với hai chính sách: FCFS và cache-aware. chạy tải trọng công việc tương tự qua cả hai, báo cáo tỷ lệ hit prefix-cache và thông suất delta. Sau đó chạy một tải trọng công việc "scrambled ordering" để hiển thị sự sụp đổ 6.4x.

> `code/main.py`实现一个模拟基根树 KV 缓存加两个策略调度器:FCFS 和缓存感知──用两者运行相同工作负载,报告前缓存命中率和吞吐量差异──然后运行"乱序排序"工作负载显示 6.4x 崩──

## Chuyển nó đi.

> **【拓展：前缀缓存策略选择】**2026 năm trước 缓存 có ba cấp: 1) 应用级语义缓存(Phase 17·14)  在调用 LLM 前用嵌入相似度匹配历史响应,命中率 10-70%;(2) 服务端前缓存(SGLang RadixAttention / vLLM prefix caching) 复用 KV Cache,10x 延迟降低;(3) 跨节点缓存路由(Phase 17·11) 通过缓存意识路由将请求路由由由由持有前的副本──三者可以叠加:语义缓存 → 避免 LLM 调用 端端前缓存避免重复预填 → 跨节点路由避免请求配配──

Bài học này sẽ mang lại kết quả `outputs/skill-radix-scheduler-advisor.md`. Với mô tả khối lượng công việc (phương dạng mẫu đơn giản, mô hình thu hồi, số lượng người thuê cùng lúc), nó tạo ra một đơn đặt hàng đơn giản và một đi/không đi cho việc chấp nhận SGLang.

> 本课产 出 `outputs/skill-radix-scheduler-advisor.md`△给定工作负载描述(quan 模板形状、检索模式、并发租户数), nó tạo ra 排序处方和 SGLang 采用 go/no-go 建议。

## Tập luyện bài tập

1. Đi chạy`code/main.py`. So sánh FCFS và cache-aware trên cùng tải trọng công việc.
   Trung ngữ翻译:运行 `code/main.py`◊ So sánh với FCFS và cảm giác lưu trữ trên cùng tải trọng làm việc.
2. Thay đổi tải trọng để các yêu cầu chuyển đổi ngẫu nhiên `[system, tools, context]`- Chuyện gì xảy ra với tốc độ?
   Trung文翻译:修改工作负载使 prompt 随机排列 `[system, tools, context]` tái vận hành                                                                                                                                                                                                                                                            
3. Xét chi phí HBM của việc giữ một hệ thống lập tức 2.000 token cư trú như một nhánh radix trên Llama 3.1 8B. So sánh với chi phí của một lô 16 chuỗi mà không sử dụng lại tiền đề.
   Trung文翻译:计算在 Llama 3.1 8B 上保持 2,000 token 系统提示作为一个基因 分支常驻的HBM 成本──与无前复用16序列批次成本比较──
4. Đọc bài báo SGLang RadixAttention. Giải thích bằng ba câu tại sao việc xả lôi lôi lôi lôi lôi hình cây hơn việc xả lôi lôi lôi lôi lôi lôi lôi lôi lôi lôi lôi lôi lôi dưới khối lượng nặng.
   Trung文翻译:阅读 SGLang RadixAttention 论文──用三句话解释为什么树形 LRU 淘汰在前密集负载下优于块形 LRU──
5. Một khách hàng báo cáo chỉ 8% tỷ lệ cache hit.
   Trung ngữ: khách hàng báo cáo chỉ 8% 缓存命中率── nói ra ba nguyên nhân có thể và mỗi phương pháp chẩn đoán──

## Từ khóa  Từ khóa nhanh chóng

| Term / 术语 | What people say / 通俗说法 | What it actually means / 实际含义 |
|------|----------------|------------------------|
| RadixAttention | "the SGLang thing" / "SGLang 的那个" | KV cache indexed as a radix tree so shared prefixes reuse blocks / KV 缓存以 radix tree 索引，共享前缀复用块 |
| Radix tree | "compact trie" / "紧凑前缀树" | Tree where each node owns a token range and its KV blocks / 每个节点拥有 token 范围和 KV 块的树 |
| Cache-aware scheduler | "hot-branch-first" / "热分支优先" | Scheduler that prefers requests sharing the resident branch / 优先服务共享常驻分支请求的调度器 |
| Prefix-cache hit rate | "how much of your prompt was free" / "prompt 多少是免费的" | Fraction of prompt tokens served from reused KV blocks / 从复用 KV 块服务的 prompt token 比例 |
| FCFS | "first-come first-served" / "先来先服务" | Default scheduling that breaks prefix locality / 破坏前缀局部性的默认调度 |
| Branch-level LRU | "evict the leaf" / "淘汰叶子" | Eviction policy matched to radix shape / 匹配 radix 形状的淘汰策略 |
| Prompt template ordering | "the cache key" / "缓存键" | The prompt's component order determines what the tree can share / prompt 组件顺序决定树能共享什么 |
| System prompt pinning | "resident prefix" / "常驻前缀" | Keep the immutable system portion pinned to avoid eviction thrash / 保持不可变系统部分固定避免淘汰抖动 |

## Xem thêm 延伸阅读

- [SGLang GitHub](https://github.com/sgl-project/sglang) nguồn và tài liệu.
- [SGLang documentation](https://sgl-project.github.io/) RadixCông tâm và chi tiết lịch trình.
- [SGLang paper — Efficiently Programming Large Language Models (arXiv:2312.07104)](https://arxiv.org/abs/2312.07104) tham chiếu thiết kế.
- [LMSYS blog — SGLang with RadixAttention](https://www.lmsys.org/blog/2024-01-17-sglang/) Số điểm tham chiếu và lý do lập trình viên.
- [vLLM — Prefix Caching](https://docs.vllm.ai/en/latest/features/prefix_caching.html) Thực hiện giống như rễ của vLLM, để so sánh.
