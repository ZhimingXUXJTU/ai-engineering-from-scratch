# Phòng song / Swarm / Networked Architectures

> Sự khác biệt với giám sát viên: không có người quyết định trung tâm. Các đại lý đọc một chuyến đi chung, bắt đầu công việc không đồng bộ, viết lại kết quả. LangGraph rõ ràng hỗ trợ "Swarm Architecture" cho môi trường phi tập trung, động. Matrix (arXiv:2511.21686) đại diện cho cả sự kiểm soát và lưu lượng dữ liệu như các tin nhắn được phân phối qua hàng phân tán để loại bỏ nút thắt của nhạc công. Sự thỏa hiệp là rõ ràng: quyết định và khả năng truy xuất để có thể mở rộng. Swarm phù hợp với các nhiệm vụ với nhiều phụ vấn độc lập; nó không phù hợp với các nhiệm vụ cần một kế hoạch nhất quán.

> **【中文解读】**Bài viết này giới thiệu mô hình tổ chức của các tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập đoàn tập trung tập đoàn tập đoàn tập đoàn tập trung tập đoàn tập đoàn tập trung tập đoàn tập đoàn tập đoàn tập trung tập đoàn tập đoàn tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập

> **【拓展：parallel swarm networks→具体应用】**Và làm cho một số lượng lớn Agent đồng thời xử lý các nhiệm vụ, sau đó tập hợp kết quả.


**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 16 · 05 (Supervisor Pattern), Phase 16 · 04 (Primitive Model) | **前置知识:** Phase 16 · 05 (Supervisor Pattern), Phase 16 · 04 (Primitive Model)
**Time:** ~75 minutes | **时间:** ~75 分钟

>  **【前置】**Học本节前请先掌握:Phase 16·04-05(原语+Supervisor)。本节是Supervisor's反面无中心协调器的群体网络。
>  **【类比】**Swarm vs Supervisor = "decentralization" vs "层级制"──Supervisor = 公司(CEO调度);Swarm = 开源社区(每个人看问题 板自己领取)──Swarm 适合独立子任务(多文件编辑、多源查询),不适合需要单一计划的任务──5-10 个代理是最优太多会聚聚时打架──

##                                                                                                                                                                                                                                                               

Giám đốc chỉ định một vài người lao động. Còn hàng trăm người thì sao? Giám đốc chính là nút thắt: mọi quyết định về việc ai làm gì thông qua một đại lý. Một bước kế hoạch chậm chạp làm đình trệ toàn bộ hệ thống.

> Người giám sát có thể mở rộng đến một vài máy. Những trăm người đó? Người giám sát tự trở thành một cái chai: mỗi quyết định về ai làm gì đều thông qua một Đại lý.

Người giám sát là một cuộc gọi LLM. Ở hàng trăm công nhân, người giám sát thực hiện hàng trăm cuộc gọi LLM chỉ để gửi. Mỗi cuộc gọi là giây; chi phí gửi thống trị. Swarm loại bỏ người giám sát hoàn toàn.

> 监督者本身就是 LLM 调用. 在数百个工作器时,监督者只调度就进行数百次 LLM 调用.

Các kiến trúc đám đông đảo thay đổi thiết kế. Thay vì một nhà hoạch định trung tâm gửi công việc, công nhân chọn công việc từ một hàng đợi chung. "sự phối hợp" được nướng vào ngữ nghĩa của xe buýt sự kiện. Không có nhạc cụ; hệ thống cân bằng cho đến khi hàng đợi làm.

> 群体架构翻转了设计――不是中央规划者分发工作,而是工作器从共享队列中获取工作――"协调"被嵌入事件总线语义中――没有编排器;系统扩展直到队列成为瓶──

Sự đảo ngược kiến trúc là đáng kể: nút thắt lưng chuyển từ "các LLM quyết định phải làm gì" sang "các môi giới thông điệp làm việc".

> 架构反转重大:瓶 từ " quyết định làm gì của LLM " chuyển sang "路由工作的消息代理 "──LLM 慢且昂贵;消息代理快且便宜──群体用代理瓶换 LLM 瓶几乎总是赢──

## Khái niệm cốt lõi

### Hình dạng

```
                ┌──── shared queue ────┐
                │                      │
       ┌────────┼────────┐  ◄──────┬───┘
       ▼        ▼        ▼         │
     Worker  Worker  Worker   Worker
      A       B       C        D
       │        │        │         │
       └────────┴────────┴─────────┘
                 │
                 ▼
            results pool
```

Không có người dàn nhạc. Mỗi người lao động lặp lại: kéo một nhiệm vụ, tiến hành, viết kết quả (và tùy chọn là theo dõi theo dõi).

> Không có trình lập trình. Mỗi trình lập trình.

Việc thiếu một người quyết định trung tâm là tính năng xác định. Người lao động không chờ đợi chỉ dẫn; họ tự tổ chức xung quanh hàng. Đây là mô hình diễn viên được áp dụng cho LLM.

> 缺乏中央决策者是定义特征──工作器不等待指令;它们围绕队列自组织──这是应用于 LLM 模型每个工作器是响应消息的独立演员──

### Khi đám đông phù hợp

- **Many independent tasks.**Việc phế liệu, biến đổi, phân loại, nhiệm vụ không phụ thuộc vào nhau.
  Trung ngữ翻译:**许多独立任务。**抓取、转换、分类── nhiệm vụ giữa các nhiệm vụ không phụ thuộc lẫn nhau.
- **Variable-duration work.**Nếu một số công việc mất 100ms và những công việc khác mất 10s, một đám cân bằng tải tự động  nhanh nhân viên kéo ra công việc tiếp theo.
  Trung ngữ翻译:**可变持续时间的工作。**Nếu một số nhiệm vụ cần 100ms và một số khác cần 10s, nhóm sẽ tự động cân bằng tải 快速工作器拉取下一个任务──监督者必须预测持续时间──
- **Throughput over determinism.**Anh quan tâm đến thời gian hoàn thành, không phải quy định nghiêm ngặt.
  Trung ngữ翻译:**吞吐量优先于确定性。**Bạn quan tâm đến thời gian hoàn thành, chứ không phải sắp xếp nghiêm ngặt.

### Khi đám đông thất bại

- **Ordered workflows.**Nếu bước 3 cần đầu ra bước 2, một đám nguy cơ bước 3 bắn trước khi bước 2 được thực hiện.
  Trung ngữ翻译:**有序工作流。**Nếu bước 3 cần bước 2 để xuất, nhóm có bước 3 để hoàn thành bước 2 trước khi kích hoạt.
- **Global-plan tasks.**Những câu hỏi nghiên cứu phức tạp được một nhà lập kế hoạch lợi ích.
  Trung ngữ翻译:**全局计划任务。**Các vấn đề nghiên cứu phức tạp được hưởng lợi từ các nhà lập kế hoạch.
- **Debugging.**Không có nhật ký trung tâm và công việc không đồng bộ, tái tạo một lỗi là tốn kém.
  Trung ngữ翻译:**调试。**Không có hệ thống phân tích, giá của các lỗi hiện tại rất cao.

### Matrix (arXiv:2511.21686)

Matrix là bài báo năm 2025 đưa hàng loạt đến kết luận tự nhiên của nó: cả lưu lượng điều khiển và lưu lượng dữ liệu là các tin nhắn được phân phối theo chuỗi trên hàng rào phân phối. Không có điều phối viên trung tâm. Sự dung nạp lỗi đến từ độ bền của tin nhắn. Scalability là vấn đề của người môi giới tin nhắn, không phải của hệ thống.

> Matrix là một luận án năm 2025 đưa ra kết luận tự nhiên: dòng kiểm soát và dòng dữ liệu là các thông tin sắp xếp trên hàng rào phân tán. Không có bộ điều phối trung ương.

Bằng cách làm cho nhà môi giới (Kafka, Redis Streams, NATS) trở thành nút thắt lưng quy mô, Matrix hoàn toàn tránh được nút thắt LLM như một nhà tổ chức. Hệ thống có thể mở rộng đến hàng ngàn đại lý nếu nhà môi giới có thể; LLM là công nhân thuần túy, không bao giờ là điều phối viên.

> 通过使代理(Kafka、Redis Streams、NATS) trở thành một khối mở rộng, Matrix  hoàn toàn tránh khỏi LLM 作为编排器的瓶──如果代理可以,系统可以扩展到数千个代理;LLM là một khối hoàn toàn,永远不是一个协调器──

Đóng góp: một mô hình lập trình mà phối hợp đa đại lý là "những thông điệp chủ đề đại lý này đăng ký?" thay vì "những đại lý nào giám sát chọn tiếp theo?" Điều này làm cho hệ thống trông giống như một lưới pub / sub sự kiện.

> 贡献: một mô hình lập trình, nhiều đại lý 协调 là "Đại lý này 订阅什么消息主题?" thay vì "监督者下一个选择哪个代理?"

### Thiết kế Swarm của LangGraph
### Swarm trong khung đồ thị

Các tài liệu LangGraph 2025 mô tả rõ ràng "Swarm Architecture" là một trong những mô hình đa đại lý: đại lý là nút, nhưng cạnh hình thành một biểu đồ hướng dẫn với chu kỳ và bất kỳ nút nào có thể được kích hoạt từ hồ bơi.

> LangGraph 2025 文档明确将"群体架构" được mô tả là nhiều Agent 模式之一:Agent là một mô hình, nhưng bên hình thành có một mô hình có chiều hướng, bất kỳ mô hình nào có thể được kích hoạt trong hồ.

Lỗ trợ của LangGraph: mô hình tâm lý dựa trên đồ thị tương tự hiện hỗ trợ động lực hàng loạt. Các nút được kích hoạt dựa trên điều kiện thay vì cạnh cố định. Điều này nối liền thế giới đồ thị tĩnh và thế giới hàng loạt thuần túy.

> Lưu ý của LangGraph: mô hình tâm trí dựa trên biểu đồ tương tự hiện đang hỗ trợ động thái nhóm.

### Phương thức không hoạt động: đói và phát hiện điểm nóng

Nếu tất cả nhân viên làm việc nhanh nhất có sẵn, các công việc dài không bao giờ được chọn cho đến khi chúng là những người duy nhất còn lại.

> Nếu tất cả các thiết bị làm việc đều có nhiệm vụ nhanh nhất có thể, nhiệm vụ chạy dài sẽ không bao giờ được chọn cho đến khi chúng trở thành một số duy nhất còn lại.

Động thái thất bại của đám đông là cách thức thất bại của đám đông. Không có sự lão hóa rõ ràng (tự ưu tiên tăng với thời gian chờ đợi) hoặc công nhân chuyên nghiệp có nhiệm vụ dài, một nhiệm vụ 10 giây chờ mãi mãi phía sau một dòng nhiệm vụ 100ms.

> 饥饿 là một mô hình thất bại của nhóm. Không có sự lão hóa rõ ràng.

Giảm thiểu:
- Các hàng xếp ưu tiên với sự lão hóa rõ ràng (tăng ưu tiên với thời gian chờ đợi).
  Trung文翻译:带显式老化优先队列 (带显式老化优先队列)
- Sự chuyên môn của công nhân: một số công nhân chỉ thực hiện các nhiệm vụ "trường dài".
  Trung ngữ翻译:工作器专业化: một số工作器 chỉ chấp nhận nhiệm vụ长.
- Khác áp lực: giới hạn số lượng các nhiệm vụ nhanh vào hàng.
  Trung文翻译:背压:限制多少快速任务进入队列──

### Liên kết định tuyến dựa trên nội dung

Các cặp sưu tập tự nhiên với định tuyến dựa trên nội dung (Dạy 22) Thay vì một hàng hàng chung, có một hàng hàng cho mỗi loại tin nhắn.

> 群体与内容基础的路由 (Lớp 22) Sự tương tác tự nhiên không phải là một hàng hàng chung, mà là một hàng hàng cho mỗi loại thông tin.

Các thông tin liên kết dựa trên nội dung cộng với swarm cung cấp cho bạn lưới pub / sub event: một nền tảng mà bất kỳ đại lý nào có thể xuất bản bất kỳ loại thông điệp nào, và chỉ có các đại lý quan tâm nhận được nó. Đây là nền tảng của Matrix, CA-MCP và hầu hết các hệ thống đa đại lý sản xuất năm 2026.

> 基于内容的路由加群给你发布/订阅事件网格: Một đại lý nào cũng có thể phát hành bất kỳ loại tin nhắn nào và chỉ có một đại lý quan tâm nhận được nó. Đây là nền tảng của Matrix, CA-MCP và hầu hết các hệ thống sản xuất đa đại lý năm 2026 ⋅

## Hãy xây dựng nó.
```figure
sw-work-stealing
```

## Hãy xây dựng nó

`code/main.py`thực hiện một đám 4 dây lao động kéo từ một chia sẻ `queue.Queue`Các nhiệm vụ có thời gian thay đổi (một số nhanh, một số chậm).

> `code/main.py`实现 4 个 chia sẻ `queue.Queue`拉取工作线程──任务有可变持续时间(一些快,一些慢)──演示对比:

So sánh ba chiều là giá trị giáo dục: cùng một nhiệm vụ, cùng một công nhân, chỉ có chiến lược chuyển giao thay đổi.

> 三方对比是教育价值:相同任务、相同工作器,只有调度策略变化──顺序 = 慢──固定 = 浪费──群体 = 最优──挂钟时间数字经验性地证明了案例──

- **Sequential baseline:**Một người lao động xử lý tất cả các nhiệm vụ theo một loạt.
  Trung ngữ翻译:**顺序基线：**Một công cụ xử lý tất cả các nhiệm vụ.
- **Fixed assignment:**mỗi nhiệm vụ được giao trước cho một công nhân cụ thể (tương tự giám sát viên).
  Trung ngữ翻译:**固定分配：**Mỗi nhiệm vụ trước tiên được phân bổ cho một công cụ cụ thể.
- **Swarm:**Công nhân rút ra khỏi hàng.
  Trung ngữ翻译:**群体：**工作器 từ chia sẻ đội ngũ kéo lấy.

Các cân nặng đống tự động tải lên; việc giao nhiệm kỳ cố định khiến người lao động nhanh chóng không làm việc khi nhiệm vụ giao nhiệm vụ của họ chậm.

> 群体 tự động cân bằng tải trọng; phân phối cố định trong phân phối nhiệm vụ chậm khi làm cho nhanh chóng

Phân bố "không đồng đều nhưng tối ưu" là chữ ký đám đông. Một công nhân hoàn thành nhiệm vụ của mình trong 50ms kéo thêm ba trong khi một công nhân trên một nhiệm vụ 2 giây vẫn còn trên đầu tiên. Tổng đồng hồ tường được giới hạn bởi nhiệm vụ đơn giản chậm nhất, không phải là tổng.

> Phân bố "không đồng đều nhưng tốt nhất" là đặc điểm nhóm. 50ms  hoàn thành nhiệm vụ máy tính làm việc trong 2 giây nhiệm vụ vẫn có 3 nhiệm vụ hơn khi trên nhiệm vụ đầu tiên.

Kết quả cho thấy số lượng công việc cho mỗi người lao động (square phân phối không đồng đều nhưng tối ưu) và thời gian đồng hồ tường.

> 输出显示 mỗi công cụ của nhiệm vụ tính toán 

## Hãy sử dụng nó để thực hiện

`outputs/skill-swarm-fit.md`đánh giá liệu một nhiệm vụ có nên sử dụng swarm vs supervisor hay không. Các đầu vào: độc lập nhiệm vụ, sự khác biệt thời gian, yêu cầu đặt hàng, nhu cầu gỡ lỗi.

> `outputs/skill-swarm-fit.md`评估 nhiệm vụ nên sử dụng nhóm hay giám sát viên ∞输入: nhiệm vụ độc lập ∞持续时间差 ∞排序要求 ∞调试性需求 ∞

## Chuyển nó đi.

Danh sách kiểm tra:

> 检查清单:

- **Priority queue with aging.**Giữ phòng khỏi nạn đói.
  Trung ngữ翻译:**带老化的优先队列。**防止长任务 đói.
- **Worker idempotency.**Một công việc có thể được kéo ra nhiều lần nếu một công nhân bị tai nạn giữa thời gian chạy.
  Trung ngữ翻译:**工作器幂等性。**Nếu máy tính bị hỏng, nhiệm vụ có thể bị kéo nhiều lần.
- **Durable queue.**Sử dụng Kafka, Redis Streams, hoặc một hàng xếp dựa trên cơ sở dữ liệu để sản xuất. `queue.Queue`chỉ là trong ký ức.
  Trung ngữ翻译:**持久队列。**生产环境使用 Kafka、Redis Streams 或数据库支持的队列──`queue.Queue`Chỉ trong lưu trữ.
- **Observability per task.**Mỗi nhiệm vụ đều có một thẻ nhận dạng; mỗi nhân viên ghi lại bắt đầu/sự kết thúc với nó.
  Trung ngữ翻译:**每个任务的可观测性。**Mỗi nhiệm vụ có thẻ truy cập; mỗi công cụ sử dụng nó ghi lại bắt đầu / kết thúc.
- **Back-pressure.**Nếu hàng đợi tăng nhanh hơn người lao động cạn kiệt, hãy làm chậm người sản xuất.
  Trung ngữ翻译:**背压。**Nếu hàng tăng tốc nhanh hơn tốc độ máy xếp hàng không, giảm tốc độ nhà sản xuất.

## Tập luyện bài tập

1. Đi chạy`code/main.py`Thống lượng nhanh hơn bao nhiêu so với thứ tự trên khối lượng công việc thời gian biến đổi?
   Trung ngữ翻译:运行 `code/main.py`◊ Nhóm có thể thay đổi thời gian kéo dài làm việc tải lên hơn bao nhiêu?
2. Thêm một biến thể hàng ưu tiên ( Sử dụng `queue.PriorityQueue`Đặt ưu tiên theo mục "bất quan trọng" nhiệm vụ. Xem xem các nhiệm vụ ưu tiên thấp có bao giờ bị đói khi tải liên tục hay không.
   中文翻译:添加优先队列变体(使用 `queue.PriorityQueue`(■) Theo nhiệm vụ "bách trọng" 字段 phân phối ưu tiên■ để xem nhiệm vụ ưu tiên thấp có đang bị đói trong tải trọng liên tục■
3. Thực hiện một máy dò điểm nóng: ghi lại khi một công nhân nào đó xử lý 3 lần nhiều nhiệm vụ hơn công nhân chậm nhất. Điều đó cho thấy gì về phân phối thời gian nhiệm vụ?
   Trung ngữ翻译:实现热点检测器: Khi bất kỳ máy tính nào xử lý hơn 3 lần nhiệm vụ của máy tính chậm nhất, điều này cho thấy việc phân phối thời gian kéo dài của nhiệm vụ có đặc điểm gì?
4. Đọc bài viết Matrix (arXiv:2511.21686) trừu tượng và Phần 3. Xác định một tradeoff cụ thể Matrix chấp nhận (scability gain) và một nó từ bỏ (traceability, định nghĩa).
   Trung văn翻译:阅读 Matrix 论文(arXiv:2511.21686)摘要和第 3 节──识别 Matrix 接受一个具体权衡(可扩展性收益) 和一个放弃的(可追溯性、确定性)──
5. Chuyển đổi demo swarm để sử dụng `queue.Queue`của (task_type, payload) tuples, với người lao động chỉ đăng ký các loại cụ thể.
   Trung文翻译:将群体演示转换为使用 (task_type, payload) 元组的 `queue.Queue`, bộ máy chỉ đăng ký loại cụ thể. Khi nhiệm vụ được cấu trúc, quy tắc của đường nào hợp lý?

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Swarm architecture / 群体架构 | "Decentralized agents" / "去中心化 Agent" | Workers pull from shared queue; no central orchestrator. / 工作器从共享队列拉取；没有中央编排器。 |
| Event bus / 事件总线 | "Agents subscribe to topics" / "Agent 订阅主题" | Message broker that routes tasks to workers by type or content. / 按类型或内容将任务路由到工作器的消息代理。 |
| Starvation / 饥饿 | "Task never runs" / "任务永远不运行" | Low-priority task never gets picked because higher-priority work arrives continuously. / 低优先级任务因为高优先级工作持续到达而永远不被选中。 |
| Hot-spotting / 热点 | "One worker drowns" / "一个工作器淹没" | Load imbalance where one worker gets most tasks. / 一个工作器获得大部分任务的负载不均衡。 |
| Back-pressure / 背压 | "Slow down the producer" / "减慢生产者" | Mechanism that signals upstream to stop producing when the queue fills up. / 当队列填满时向上游发出停止生产的信号机制。 |
| Idempotent worker / 幂等工作器 | "Safe to re-run" / "安全重新运行" | A task processed twice produces the same result. Required because workers may crash mid-run. / 任务处理两次产生相同结果。因为工作器可能中途崩溃所以需要。 |
| Durable queue / 持久队列 | "Survives crashes" / "崩溃后存活" | Queue backed by disk or replicated storage; tasks are not lost when a worker crashes. / 由磁盘或复制存储支持的队列；工作器崩溃时任务不丢失。 |
| Matrix framework / Matrix 框架 | "Full message-passing swarm" / "全消息传递群体" | Both data and control flow are serialized messages on distributed queues. / 数据流和控制流都是分布式队列上的序列化消息。 |

## Xem thêm 延伸阅读

- [LangGraph workflows and agents — Swarm Architecture](https://docs.langchain.com/oss/python/langgraph/workflows-agents) hỗ trợ đống đông rõ ràng
  Trung文翻译:LangGraph 工作流和 Agent  群体架构  明确的群体支持
- [Matrix — A Decentralized Framework for Multi-Agent Systems](https://arxiv.org/abs/2511.21686) Lâu đài thông điệp đầy đủ
  Trung ngữ翻译:Matrix  多 Agent 系统的去中心化框架  全消息传递群体
- [Anthropic engineering — why supervisor not swarm in Research](https://www.anthropic.com/engineering/multi-agent-research-system) lý do tại sao một hệ thống sản xuất cụ thể đã chọn rõ ràng người giám sát hơn đàn
  Trung ngữ翻译:Anthropic 工程  为什么研究系统选择监督者而不是群体  为什么一个特定生产系统明确选择监督者而不是群体
- [AutoGen v0.4 actor-model docs](https://microsoft.github.io/autogen/stable/) diễn viên dựa trên sự kiện viết lại, gần hơn với đám đông hơn GroupChat của v0.2
  Trung文翻译:AutoGen v0.4 actor 模型文档  事件驱动 actor 重写,比 v0.2 的 GroupChat 更接近群体
