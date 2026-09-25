# Giám đốc / Phong trào nhạc sĩ-người làm việc mô hình

> Một đại lý chính lập kế hoạch và đại diện; nhân viên chuyên môn thực hiện trong bối cảnh song song và báo cáo lại. Đây là mô hình đằng sau hệ thống nghiên cứu của Anthropic (Claude Opus 4 là chì, Sonnet 4 là chất phụ), được đo ở +90.2% so với Opus 4 đơn đại lý trên các đánh giá nghiên cứu nội bộ. Bài đăng kỹ thuật của Anthropic báo cáo rằng 80% sự khác biệt trên BrowseComp được giải thích bởi việc sử dụng mã chỉ riêng  đa đại lý thắng phần lớn bởi vì mỗi subagent nhận được một cửa sổ bối cảnh mới. Bài học này xây dựng mô hình giám sát từ nguyên thủy và bao gồm các bài học kỹ thuật năm 2026 từ triển khai sản xuất.

> **【中文解读】**Một chủ quản đại lý 规划并委派任务;专业化工作器在并行上下文中执行并汇报. Đây là mô hình đằng sau của Antropic Research 系统.

> **【拓展：Supervisor 模式 → Claude DevFleet】**Claude Code của nhiều đại lý  tổ chức công cụ Claude DevFleet là giám sát viên  thực hiện mô hình  một đại lý phân giải nhiệm vụ, gửi đến nhiều phân biệt worktree trong các con đại lý và làm việc, kết quả tổng kết.

**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib, `threading`) | **语言:** Python (标准库, `threading`)
**Prerequisites:** Phase 16 · 04 (Primitive Model) | **前置知识:** Phase 16 · 04 (原语模型)
**Time:** ~75 minutes | **时间:** ~75 分钟

>  **【前置】**学本节前请先掌握:Phase 16·04(4 个原语) 、Phase 14·01(Agent 循环)  Giám sát 模式 = 多 Agent 中最常用的一种一个主管 + 多个工作器──
>  **【类比】**Giám đốc 模式 = "Project manager + 工程师团队"──主管(Opus) phân giải nhiệm vụ+审查,工作器(Sonnet) 各干一摊──Anthropic 数据:BrowseComp 80% 方差由代币 使用解释多 代理 赢是因为每个子 代理有独立上下文窗口(新背景),不是协调本身魔法──

##                                                                                                                                                                                                                                                               

Nghiên cứu là nhiệm vụ nguyên mẫu mà các hệ thống đơn tác nhân thất bại. Bạn hỏi "sự thay đổi trong các hệ thống đa tác nhân giữa năm 2023 và 2026 là gì?" Một tác nhân đơn độc đọc 5 bài báo theo trình tự, lấp đầy một nửa ngữ cảnh của nó với văn bản của chúng, và sau đó phải suy luận về tất cả chúng cùng nhau. Nó quên bài báo đầu tiên vào thời điểm đạt đến năm. Nó không thể song song.

> Nghiên cứu là một nhiệm vụ điển hình của một hệ thống thất bại. Bạn hỏi "2023 đến 2026 năm giữa nhiều hệ thống đại lý đã thay đổi gì?" Một đại lý đơn lẻ  trình tự đọc năm bài báo, sử dụng văn bản của chúng để điền đầy một nửa trên bài viết dưới đây, sau đó phải suy luận với chúng.

Sự thất bại của một đại lý duy nhất là cấu trúc, không thể khắc phục được bằng các lời nhắc tốt hơn. Bất kể lời nhắc hệ thống tốt đến mức nào, cửa sổ ngữ cảnh sẽ tràn đầy. Thông tin cần thiết cho tổng hợp (những phát hiện chính của tất cả năm bài báo) về mặt vật lý không phù hợp với văn bản thô của các bài báo.

> 单代理 失败是结构性的,无法用更好的提示修复──不管系统提示多好,上下文窗口都会填满──综合需要的信息(所有五篇论文的关键发现)

Mô hình giám sát khắc phục điều này: một đại lý dẫn đầu lập kế hoạch tìm kiếm, ủy quyền mỗi phụ câu hỏi cho một nhân viên, và tổng hợp. Mỗi nhân viên nhận được cửa sổ mã thông báo 200k riêng cho một câu hỏi hẹp.

> 监督者模式修复了这个问题: một quản lý Agent 规划搜索,将每个子问题委派给一个工作器,然后综合――每个工作器获得自己的200k代币 窗口用于一个狭窄的问题――主管永远不看原始论文只看工作器摘要――

Dòng thông tin là thiết kế: dữ liệu thô vẫn ở trong bối cảnh người lao động; chỉ có kết quả nén đạt đến lead. bối cảnh lead được dành riêng cho tổng hợp, không phải tải dữ liệu. Đây là chiến thắng kiến trúc  tách biệt các công việc dữ liệu nặng từ công việc tổng hợp nặng.

> 信息流是设计: dữ liệu nguyên thủy vẫn còn trên máy tính làm việc; chỉ có những phát hiện bị nén đến người quản lý. 信息流是设计:原始数据留在工作器上下文;只有压缩的发现到主导者.

Hệ thống nghiên cứu sản xuất của Anthropic báo cáo +90.2% về các đánh giá nghiên cứu nội bộ so với một Opus 4. cùng một bài viết lưu ý rằng 80% sự khác biệt của BrowseComp được giải thích bởi * việc sử dụng mã chỉ riêng*.

> Phương trình nghiên cứu sản xuất của Anthropic báo cáo trong đánh giá nghiên cứu nội bộ tăng +90.2% so với đơn vị Opus 4 👍

Số 80% là kết quả tiêu đề: lựa chọn mô hình, kỹ thuật nhanh chóng và công cụ cùng nhau giải thích chỉ 20% sự khác biệt. Nếu bạn muốn hiệu suất của đại lý nghiên cứu tốt hơn, hãy chi tiêu nhiều token (nhiều subgen, bối cảnh lớn hơn) trước khi điều chỉnh các lời nhắc. Chi phí, không phải sự thông minh, là đòn bẩy.

> 80% số này là con số tìm thấy: mô hình chọn, gợi ý kỹ thuật và công cụ tăng lên chỉ giải thích 20% của sự khác biệt. Nếu bạn muốn nghiên cứu tốt hơn về hiệu suất của đại lý, hãy chi nhiều hơn trước khi điều chỉnh gợi ý.

## Khái niệm cốt lõi

### Mô hình

```
                 ┌──────────────┐
                 │   Lead       │  plans, decomposes,
                 │  (Opus 4)    │  synthesizes
                 └──┬────┬───┬──┘
                    │    │   │
            ┌───────┘    │   └───────┐
            ▼            ▼           ▼
      ┌─────────┐  ┌─────────┐  ┌─────────┐
      │ Worker1 │  │ Worker2 │  │ Worker3 │
      │(Sonnet) │  │(Sonnet) │  │(Sonnet) │
      └─────────┘  └─────────┘  └─────────┘
         fresh       fresh        fresh
         context     context      context
```

Các công nhân không bao giờ thấy công việc của nhau cho đến khi chì tổng hợp. Mỗi mũi tên là một giao tiếp với một đồ tạo vật hẹp.

> Chủ đạo luôn không đọc nguyên liệu. Máy làm việc không bao giờ nhìn thấy công việc của nhau trước khi chủ đạo kết hợp. Mỗi mũi tên là một giao tiếp của các công cụ nhỏ gọn.

Sự cô lập thông tin này là lựa chọn thiết kế cốt lõi. cửa sổ bối cảnh của lead vẫn tập trung vào lập kế hoạch và tổng hợp  không bao giờ bị ô nhiễm bởi 200k token của kết quả tìm kiếm thô. Mỗi công nhân nhận được ngân sách sạch 200k cho câu hỏi hẹp của họ.

> Sự phân biệt thông tin là một lựa chọn thiết kế cốt lõi.

### Tại sao nó thắng

Ba cơ chế:

> 3 cơ chế:

1. **Fresh context per subagent.**Một công nhân khám phá "Di sản của FIPA-ACL" không mang theo 40k token đầu tư kế hoạch. Nó nhận được một cửa sổ 200k cho một câu hỏi.
   Trung ngữ翻译:**每个子 Agent 的清新上下文。**探索"FIPA-ACL 遗产"的工作器不携带主导人用于规划的40k代币――它获得一个用于一个问题的200k窗口――
2. **Specialization via prompt.**Lời nhắc của người dẫn đầu là "xử lý và tổng hợp", không phải "phát tích". Lời nhắc của mỗi người làm việc là hẹp: "để tìm ra những gì đã thay đổi trong X. " Các lời nhắc tập trung tạo ra kết quả tập trung.
   Trung ngữ翻译:**通过提示专业化。**Các gợi ý của chủ đạo là " phân tích và tổng hợp ", chứ không phải " nghiên cứu "...... gợi ý của mỗi máy làm việc là rất hẹp:" tìm ra X đã thay đổi gì ".... gợi ý của tập trung tạo ra kết quả tập trung "....
3. **Parallelism.**Công nhân chạy cùng lúc.`max(worker_times) + plan + synthesis`Không .`sum(worker_times)`- Tôi không biết.
   Trung ngữ翻译:**并行性。**工作器并发运行──挂钟时间大约是 `max(worker_times) + plan + synthesis`, thay vì `sum(worker_times)`

### Bài học kỹ thuật (Anthropic 2025)

Bài đăng Anthropic liệt kê một số bài học sản xuất vẫn có liên quan đến năm 2026:

> Anthropic's bài viết liệt kê một số điều vẫn áp dụng cho kinh nghiệm sản xuất năm 2026:

- **Scale effort to query complexity.**Các câu hỏi đơn giản: một đại lý, 3-10 cuộc gọi công cụ. Các câu hỏi phức tạp: 10+ đại lý. Người dẫn đầu phải đánh giá điều này, không phải người gọi.
  Trung ngữ翻译:**按查询复杂度缩放工作量。**简单查询: một đại lý,3-10次工具调用──复杂查询:10+ 个 đại lý──主持者必须估计这一点,而不是调用者──
- **Broad then narrow.**Đầu tiên phân chia thành các câu hỏi phụ rộng, sau đó tạo ra nhiều người lao động hơn cho mỗi câu hỏi phụ nếu câu trả lời cho phép chiều sâu.
  Trung ngữ翻译:**先宽后窄。**Trước tiên phân giải thành các vấn đề nhỏ rộng, nếu câu trả lời cần độ sâu, thì cho mỗi vấn đề nhỏ tạo ra nhiều máy làm việc hơn.
- **Rainbow deployments.**Các đại lý là lâu dài và có tính trạng thái. màu xanh lá cây truyền thống không hoạt động. Anthropic sử dụng cầu vồng: triển khai dần các phiên bản mới trong khi các phiên bản cũ cạn kiệt.
  Trung ngữ翻译:**彩虹部署。**Agent là thời gian dài hoạt động và có trạng thái.
- **Token usage dominates.**Multi-agent là ~ 15x các token của single-agent. chỉ chạy nó khi giá trị nhiệm vụ biện minh cho chi phí.
  Trung ngữ翻译:**Token 使用量占主导。**Nhiều đại lý là chỉ số khoảng 15 lần của một đại lý. Chỉ cần chứng minh giá trị nhiệm vụ khi vận hành nó hợp lý.

### Lập trình bản địa quay

LangGraph ban đầu đã gửi một `langgraph-supervisor`thư viện có cấp cao `create_supervisor`trợ lý. Năm 2025, LangChain chuyển khuyến nghị để thực hiện mô hình giám sát thông qua gọi công cụ trực tiếp, bởi vì các cuộc gọi công cụ cung cấp nhiều quyền kiểm soát hơn về những gì giám sát thấy * (kỹ thuật ngữ). Thư viện vẫn hoạt động; các tài liệu bây giờ khuyên dùng hình thức gọi công cụ.

> LangGraph ban đầu phát hành một cái có cấp cao .`create_supervisor`助手 của `langgraph-supervisor`库──2025年 LangChain sẽ đề nghị được chuyển đổi thành thông qua công cụ调用 trực tiếp thực hiện chế độ giám sát viên, vì công cụ调用 đối với * giám sát viên xem gì*(上下文工程) cung cấp nhiều hơn kiểm soát.

Sự thay đổi phản ánh một cái nhìn sâu sắc 2025-2026: kỹ thuật bối cảnh quan trọng hơn kỹ thuật dàn nhạc. Những gì người giám sát thấy quyết định những gì họ có thể lên kế hoạch.

> Sự chuyển đổi này phản ánh những hiểu biết về năm 2025-2026: trên văn bản kỹ thuật quan trọng hơn so với việc sắp xếp. Người giám sát thấy những gì quyết định nó có thể lên kế hoạch.

### Các chế độ thất bại

- **Lead hallucinates the plan.**Nếu dẫn tạo ra các câu hỏi phụ mà không phân hủy câu hỏi thực sự, nhân viên nghiên cứu chính xác về mục tiêu sai.
  Trung ngữ翻译:**主导者幻觉计划。**Nếu các vấn đề con được tạo ra bởi người quản lý không giải quyết được vấn đề thực sự, máy sẽ thực hiện nghiên cứu chính xác trên mục tiêu sai lầm.
- **Workers over-explore.**Không có ranh giới phạm vi rõ ràng, công nhân trôi qua ngoài các phụ câu hỏi được giao cho họ và làm ô nhiễm bước tổng hợp.
  Trung ngữ翻译:**工作器过度探索。**Không có giới hạn phạm vi rõ ràng, máy sẽ di chuyển vượt ra ngoài các vấn đề phân phối của nó và làm ô nhiễm toàn bộ bước.
- **Synthesis conflicts.**Hai công nhân trả lại những sự thật mâu thuẫn. Người dẫn đầu phải hỏi lại (chưa thêm một vòng) hoặc ghi nhận sự bất đồng rõ ràng.
  Trung ngữ翻译:**综合冲突。**两个工作器回复矛盾的事实――主导者必须重新询问(增加一轮) 或明确记录分歧――静默选择一方是最糟糕的失败:用户永远不知道发生分歧――

### Khi người giám sát sai

- **Sequential tasks.**Nếu bước 2 thực sự cần đầu ra bước 1, song song không mua gì. Sử dụng một đường ống (CrewAI Sequential, LangGraph đồ thị tuyến tính).
  Trung ngữ翻译:**顺序任务。**Nếu bước 2 thực sự cần bước 1 của đầu ra,并行性没有帮助──使用流水线(CrewAI Sequential、LangGraph 线性图)──
- **Simple queries.**Một đại lý đơn xử lý chúng nhanh hơn và rẻ hơn.
  Trung ngữ翻译:**简单查询。**单代理 更快更便宜地处理它们―― sử dụng chủ nhân "缩放工作量" kiểm tra trước khi tạo máy.
- **Strict determinism.**Giám sát viên sử dụng ủy quyền được lựa chọn bởi LLM. Hình đồ tĩnh tốt hơn khi kiểm toán / phát lại quan trọng hơn khả năng thích nghi.
  Trung ngữ翻译:**严格确定性。**监督者使用 LLM 选择的委派──当审计/回放比适应性更重要时,静态图更好──

## Hãy xây dựng nó.
```figure
supervisor-hierarchy
```

## Hãy xây dựng nó

`code/main.py`thực hiện một giám sát viên gồm ba công nhân song song bằng cách sử dụng `threading`. Lead phân hủy một truy vấn thành các câu hỏi phụ, công nhân chạy đồng thời trên mỗi câu hỏi phụ, và lead tổng hợp. Không có LLM thực sự

> `code/main.py`Sử dụng `threading`实现一个三个并行工作器的监督者――主导将查询分解为子问题,工作器在每个子问题上发行并运行,主导综合――没有真正的LLM 工作器被编写为模拟获取和总结――

Cấu trúc chính:

> 关键结构:

- `Lead.plan(query)`chia câu hỏi thành 3 câu hỏi phụ.
  Trung ngữ翻译:`Lead.plan(query)`Sẽ chia các câu hỏi thành 3 câu hỏi:
- `Worker.run(sub_q)`trả lại một bản tóm tắt giả (có thể là bất kỳ tác nhân sử dụng công cụ nào trong sản xuất).
  Trung ngữ翻译:`Worker.run(sub_q)`返回一个假摘要(可以在生产中是任何工具的代理)
- `Lead.run(query)`Thả người lao động ra trong các dây, kết hợp và tổng hợp.
  Trung ngữ翻译:`Lead.run(query)`Trong quá trình khởi động máy, chờ, rồi kết hợp.

Đi chạy:

```
python3 code/main.py
```

Kết quả cho thấy kế hoạch, các công nhân song song theo dấu thời gian bắt đầu / kết thúc, và tổng hợp cuối cùng. Bạn có thể thấy đồng hồ tường thắng: ba công nhân 0,3 giây chạy trong ~ 0,35 giây, không phải 0,9.

> 输出显示计划、带有开始/结束时间的并行工作器跟踪和最终综合―― bạn có thể thấy thời gian 挂钟优势:三个 0.3秒工作器运行在约0.35秒内,而不是0.9秒――

## Hãy sử dụng nó để thực hiện

`outputs/skill-supervisor-designer.md`thực hiện một truy vấn người dùng và tạo ra một thiết kế mô hình giám sát: prompt hệ thống dẫn đầu, vai trò của công nhân, các quy tắc phân hủy phụ câu hỏi và mẫu tổng hợp. Sử dụng điều này trước khi xây dựng một hệ thống đại lý kiểu nghiên cứu mới.

> `outputs/skill-supervisor-designer.md`接收用户查询并生成监督者模式设计:主导系统提示、工作器角色、子问题分解规则和综合模板──在构建新研究风格 系统之前使用──

## Chuyển nó đi.

Danh sách kiểm tra trước khi triển khai mô hình giám sát:

> 部署监督者模式之前的检查清单:

- **Model pairing.**Tạo nguyên tắc trên mô hình cấp độ lý luận ( lớp Opus, `o3`Các công nhân trên một mô hình nhanh hơn, rẻ hơn (Sonnet, `o4-mini`().
  Trung ngữ翻译:**模型配对。**主导者使用推理级模型(Opus 类、`o3`类) ・工作器使用更快、更便宜的模型(Sonnet、`o4-mini`(■)
- **Worker timeout.**Bất kỳ công nhân nào vượt quá thời gian chạy trung bình 2x sẽ bị giết; dẫn đầu hoặc tái tạo với phạm vi hạn hẹp hơn hoặc tiếp tục không có nó.
  Trung ngữ翻译:**工作器超时。** Bất kỳ máy nào có thời gian hoạt động hơn 2 lần trung bình bị chấm dứt; người quản lý hoặc tái tạo trong phạm vi khắt khe hơn, hoặc không sử dụng nó tiếp tục.
- **Token cap per worker.**Giới hạn cứng (chẳng hạn là 10 lần lượng tổng hợp dự kiến) ngăn cản một công nhân chạy trốn không phá vỡ ngân sách.
  Trung ngữ翻译:**每个工作器的 Token 上限。**硬限制 (ví dụ như dự kiến tổng số đầu vào 10 lần) ngăn chặn máy lao động bị mất kiểm soát tiêu tốn hết ngân sách.
- **Observability.**Theo dõi kế hoạch của người dẫn đầu, các cuộc gọi công cụ của mỗi công nhân, và tổng hợp. Đây là cơ sở cho bất kỳ debugging hậu hoc.
  Trung ngữ翻译:**可观测性。**Theo kế hoạch của người quản lý, mỗi công cụ của công cụ được điều chỉnh và tổng hợp.
- **Rainbow rollout.**Các đại lý lâu đời của tiểu bang cần chuyển đổi phiên bản dần dần, không phải đổi mới nóng.
  Trung ngữ翻译:**彩虹推出。**Có trạng thái vận hành dài thời gian Trưởng  cần chuyển phiên bản dần dần, thay vì trao đổi nóng.

## Tập luyện bài tập

1. Đi chạy`code/main.py`, sau đó thay đổi dẫn để sinh 5 công nhân thay vì 3. quan sát hiệu ứng đồng hồ tường.
   Trung ngữ翻译:运行 `code/main.py`, sau đó sửa đổi chủ nhân để tạo ra 5 thay vì 3 máy.
2. Thực hiện thời gian nghỉ lao động: giết bất kỳ lao động nào chạy dài hơn 0,5 giây và cho người dẫn đầu tổng hợp kết quả còn lại.
   Trung語翻译:实现工作器超时:终止任何运行超过0.5秒的工作器,让主导者综合剩余结果――你需要什么可观测性才能知道工作器被截断?
3. Thêm một bước phát hiện xung đột vào tổng hợp của người dẫn đầu: nếu hai công nhân trả lời mâu thuẫn, người dẫn đầu ghi nhận sự bất đồng thay vì chọn một. Làm thế nào để phát hiện mâu thuẫn mà không gọi một LLM?
   Trung ngữ翻译: Trong tổng hợp của người quản lý thêm các bước kiểm tra xung đột: Nếu hai máy làm việc trả lại câu trả lời mâu thuẫn, người quản lý ghi nhận sự phân biệt thay vì chọn một trong số đó.
4. Đọc bài viết kỹ thuật hệ thống nghiên cứu của Anthropic.
   Trung ngữ翻译:阅读Anthropic的研究系统工程文章.
5. So sánh LangGraph's `create_supervisor`(Legacy) vs. khuyến nghị gọi công cụ mới. Điều gì cho bạn kiểm soát tốt hơn những gì người giám sát thấy? Tại sao Anthropic rõ ràng chỉ chuyển các câu trả lời phụ và không phải bối cảnh người lao động thô vào tổng hợp?
   Trung ngữ翻译:比较 LangGraph 的 `create_supervisor`(Vài bản cũ) Với các công cụ mới điều khiển khuyến nghị. Làm thế nào để bạn kiểm soát tốt hơn giám sát viên xem? Tại sao Anthropic 明确 chỉ truyền tải các câu trả lời thay vì các công cụ gốc xuống tổng thể?

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Supervisor / 监督者 | "Lead agent" / "主导 Agent" | An orchestrator agent that plans, delegates, and synthesizes. Does not do the work itself. / 规划、委派和综合的编排 Agent。不做实际工作。 |
| Worker / 工作器 | "Subagent" / "子 Agent" | A focused agent invoked by the supervisor with narrow scope and its own context window. / 由监督者调用的聚焦 Agent，具有狭窄范围和自己的上下文窗口。 |
| Orchestrator-worker / 编排器-工作器 | "Supervisor pattern" / "监督者模式" | Same thing, different name. The 2026 literature uses both. / 同一事物，不同名称。2026 年文献两者都用。 |
| Fresh context / 清新上下文 | "Clean window" / "干净窗口" | A worker's context starts from its system prompt and assigned question, not the lead's history. / 工作器的上下文从其系统提示和分配的问题开始，而不是主导者的历史。 |
| Rainbow deployment / 彩虹部署 | "Gradual rollout" / "渐进推出" | Long-running stateful agents need versioned drain-and-replace, not blue-green. / 长时间运行的有状态 Agent 需要版本化的排空和替换，而不是蓝绿部署。 |
| Token dominance / Token 主导 | "Context is the variable" / "上下文是变量" | 80% of research-eval variance comes from total tokens used, not model choice, per Anthropic. / 80% 的研究评估方差来自使用的总 token，而不是模型选择，据 Anthropic。 |
| Scale effort / 缩放工作量 | "Match agent count to complexity" / "按复杂度匹配 Agent 数量" | Lead estimates query difficulty, spawns 1 vs 10+ workers accordingly. / 主导者估计查询难度，相应地生成 1 个或 10+ 个工作器。 |
| Synthesis conflict / 综合冲突 | "Workers disagree" / "工作器不一致" | Two workers return contradictory facts; the lead must surface disagreement, not silently pick one. / 两个工作器返回矛盾的事实；主导者必须揭示分歧，而不是静默选择一方。 |

## Xem thêm 延伸阅读

- [Anthropic engineering — How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) tham chiếu sản xuất cho mô hình giám sát
  Trung文翻译:Anthropic 工程  我们如何构建多 Agent 研究系统  监督者模式的生产参考
- [LangGraph workflows and agents](https://docs.langchain.com/oss/python/langgraph/workflows-agents) giám sát gọi công cụ bây giờ là hình thức được khuyến cáo
  Trung文翻译:LangGraph 工作流和 Agent  工具调用监督者现在是推的形式
- [LangGraph supervisor reference](https://reference.langchain.com/python/langgraph-supervisor) trợ lý di sản, vẫn được sử dụng trong sản xuất năm 2026
  中文翻译:LangGraph 监督者参考  旧版助手, vẫn được sử dụng 2026 年生产
- [OpenAI cookbook — Orchestrating Agents: Routines and Handoffs](https://developers.openai.com/cookbook/examples/orchestrating_agents) Phân phiên giám sát dựa trên giao hàng
  Trung文翻译:OpenAI 手册  编排 代理:例程和交接  基于交接的监督者变体
