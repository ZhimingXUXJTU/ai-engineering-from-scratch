# CrewAI: Đội ngũ dựa trên vai trò và dòng chảy
# Các nhóm đại lý dựa trên vai trò  Vai trò, nhiệm vụ, quy trình

> Bốn nguyên thủy: Agent, Task, Crew, Process. Hai hình dạng cấp cao: Crews (tự trị, hợp tác dựa trên vai trò) và Flow (tự động, xác định). CrewAI là thực hiện tham chiếu năm 2026, và tài liệu của nó là thẳng thắn: "cho bất kỳ ứng dụng sẵn sàng sản xuất nào, bắt đầu với Flow".

**Type:** Learn + Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 12 (Workflow Patterns), Phase 14 · 14 (Actor Model) | **前置知识:** 见原文
**Time:** ~75 minutes | **时间:** 见原文

## Mục tiêu học tập

- Tên bốn nguyên thủy của CrewAI (Đội ngũ, nhiệm vụ, phi hành đoàn, quy trình) và những gì mỗi người sở hữu.
- Sự phân biệt giữa trình tự, cấp bậc và quy trình đồng thuận được lên kế hoạch; chọn một trong mỗi khối lượng công việc.
- Sự khác biệt giữa các nhóm (tự trị dựa trên vai trò) và các dòng chảy (chỉ định dựa trên sự kiện) và giải thích khuyến nghị sản xuất của các docs.
- Các công cụ dây với `@tool`trang trí và `BaseTool`Subclass; lý luận về các kết quả có cấu trúc so với văn bản tự do.
- Hãy cho tên bốn loại bộ nhớ CrewAI và khi nào mỗi loại sẽ được trả giá.
- Thực hiện một đội ngũ 3 nhân viên (phác giả, nhà văn, biên tập viên) tạo ra một bản ngắn.
- Nhận ra ba chế độ thất bại của CrewAI: Thổi bốc, thuế quản lý-LLM, giao hàng dễ vỡ.

## Vấn đề  vấn đề giới thiệu

Các nhóm áp dụng các khung đa đại lý chạm vào cùng một bức tường. "Công tác tự động" nghe có vẻ tuyệt vời trong một bản demo. Sau đó một khách hàng gửi lỗi và bạn cần lặp lại xác định. hoặc tài chính hỏi một đội ngũ LLM-routed chi phí mỗi chạy. hoặc trên cuộc gọi cần biết đại lý nào đã dừng lại vào 3 giờ sáng.

> 采用多代理框架的团队都会遇到相同的墙──"协作自主" trong buổi trình diễn nghe rất tuyệt vời──然后客户提出了一个bug, bạn cần xác định lại──或财务部门问一次 LLM 路由的团队运营需要花多少钱──或值班人员需要知道哪个代理在凌晨3点卡住──

Các nhóm chuyên môn tự do không trả lời một câu hỏi nào một cách sạch sẽ, nhưng những DAG hoàn toàn không có câu trả lời nào, nhưng mất đi hình dạng khám phá mà một nhân viên đầu óc cần.

> Phương pháp tự do LLM 路由团队 không thể trả lời được những câu hỏi này.


> **【中文解读】**CrewAI 采用角色模板模型每个代理有角色(角色) 目标(目标) 和背景故事(Backstory)  成员组成 成员组成 成员协作完成任务──CrewAI 独特的特点是将组织管理理论(角色定义、团队协作) được映射到 Agent 设计中,使非技术用户也能定义 Agent 团队──

> **{【拓展：CrewAI 是 2024-2025 年增长最快的 Agent 框架之一（GitHub 20k+ s...】}**CrewAI là một trong những khuôn khổ của các đại lý phát triển nhanh nhất trong năm 2024-2025 (GitHub 20k+ sao) ⋅ điểm bán trung tâm là thấp mã Agent 协作 通过YAML 配置文件定义 Agent 角色和任务流──CrewAI 支持两种模式:Crew(预定义角色团队) 和流量(动态工作流)──企业用户 (尤其是非技术团队) 特别青其直观的角色定义方式──
Sự chia rẽ của CrewAI là trung thực về thương mại. Đội ngũ cho công việc hợp tác, dựa trên vai trò, khám phá. Xu hướng cho sự kiện, sở hữu mã, kiểm toán sản xuất. cùng một khung, hai hình dạng, chọn cho mỗi bề mặt.

> Sự phân chia trung thực của CrewAI dựa trên trọng lượng này. Cầu dùng để hợp tác, dựa trên vai trò tìm kiếm.

>  **【前置】**必须先掌握:Phase 14·12(Anthropic Workflow Patterns) CrewAI's Flow chính là những mô hình này được thực hiện,Crew chính là "đầu tự do" của dòng chảy làm việc; cũng nhưPhase 14·14(Actor Model) Crew 内部的代理 协作本质上是消息传递──还需要理解Pydantic(结构化输出验证),因为 nhiệm vụ của `output_pydantic`Đó là một hiệp định cốt lõi.

## Khái niệm cốt lõi

### Bốn nguyên thủy

Màn hình của CrewAI nhỏ, hãy ghi nhớ lại và phần còn lại sẽ được cấu hình.

> Chuẩn bị cho các máy bay.

> CrewAI sẽ nhiều Agent 协作建模为角色团队(Crew) 和事件驱动流程(Flow)两种模式──四种原语:Agent(角色+目标+背景故事)、Task(任务)、Crew(团队容器)、Process(执行策略)。

- **Agent.** `role + goal + backstory + tools + (optional) llm`- Hình ảnh hậu trường là chịu tải. Nó hình thành giọng nói, phán đoán, khi đại lý dừng lại.

>  **【类比】**                                                                                                                                                                                                                                                              **关键洞察**Câu chuyện đằng sau không phải là trang trí, nó thực sự ảnh hưởng đến cách đánh giá của LLM  đưa cùng một đại lý 写作"严谨学者" hoặc"激进创业者",输出风格 hoàn toàn khác nhau.
- **Task.** `description + expected_output + agent + (optional) context + (optional) output_pydantic`Một đơn vị công việc có thể được sử dụng nhiều lần.`expected_output`là hợp đồng.`context`danh sách các nhiệm vụ trước dòng mà các kết quả được chuyển vào. `output_pydantic`tạo ra một hình dạng có cấu trúc.
- **Crew.**Container, sở hữu danh sách các`agents`, danh sách của `tasks`, `process`, và tùy chọn `memory`+ `verbose`+ `manager_llm`cài đặt.
- **Process.**Chiến lược thực hiện: theo trình tự, Hiérarchical, Consensus (được lên kế hoạch).

Các nhân viên không nhìn thấy nhau trực tiếp, nhiệm vụ của các nhân viên tham khảo, các nhân viên theo dõi nhiệm vụ, quá trình quyết định ai chọn nhiệm vụ tiếp theo.

> Agent 之间不直接见彼此──Task 引用 Agent──Crew 排列任务顺序──Process quyết định ai thực hiện nhiệm vụ tiếp theo──这是完整的心智模型──

> **Validated against**CrewAI 0.86 (2026-05). Các phiên bản mới hơn có thể đổi tên hoặc hợp nhất các loại quy trình; kiểm tra các [CrewAI Processes docs](https://docs.crewai.com/concepts/processes)trước khi dựa vào một hình dạng cụ thể.

### Theo trình tự vs Đường bậc vs Thỏa thuận

- **Sequential.**Các nhiệm vụ chạy theo thứ tự tuyên bố.`context`N + 1 là một nhiệm vụ. chi phí thấp nhất.
- **Hierarchical.**Một quản lý đại lý (câu lạc LLM riêng biệt) các tuyến đường giữa các chuyên gia.`manager_llm`config hoặc mặc định. người quản lý chọn nhiệm vụ tiếp theo mỗi vòng và có thể từ chối hoặc định tuyến lại. sử dụng khi bạn có bốn chuyên gia hoặc nhiều hơn và đặt hàng thực sự phụ thuộc vào đầu ra trước đó.
- **Consensus.**Được lên kế hoạch, hiện chưa được triển khai trong API công cộng. Các tài liệu lưu tên cho một quy trình dựa trên bỏ phiếu trong tương lai. Đừng dựa vào nó hôm nay.

Các hệ thống phân cấp thêm một cuộc gọi LLM mỗi vòng (người quản lý) trên đầu mỗi cuộc gọi chuyên gia. Chi phí token có thể tăng gấp ba lần trong một lần chạy năm bước. Chỉ trả cho nó khi bạn cần đường dẫn.

> ️ **【易错点】**Xem CrewAI 文档 ví dụ đều sử dụng Lịch trình 模式就跟随使用──**后果**Tài khoản: 单爆炸Trang bậc Mỗi vòng nhiều lần quản lý LLM 调用,5 步任务变 10 lần LLM 调用,token 成本翻 3 倍。**一行修复**:默认使用序列 () 成本最低、最可预测), chỉ có nhiệm vụ 顺序 thực sự phụ thuộc vào bước đầu tiên输出 (如客服分流)才升级到等级.

> Các mô hình cấp độ tăng lên trên mỗi vòng của các chuyên gia điều khiển điều khiển. Trong 5 bước hoạt động, chi phí token có thể tăng gấp 3 lần. Chỉ khi bạn cần đường dẫn là đáng trả cho nó.

> CrewAI sẽ nhiều Agent 协作建模为角色团队(Crew) 和事件驱动流程(Flow)两种模式──四种原语:Agent(角色+目标+背景故事)、Task(任务)、Crew(团队容器)、Process(执行策略)。

### Đội ngũ vs dòng chảy

Đây là khung hình mà các bác sĩ dẫn đầu vào năm 2026.

> Đây là khung phân chia trung tâm nhất trong tài liệu năm 2026:

- **Crew.**Phương pháp tự trị dựa trên LLM. Khung tâm chọn hình dạng khi chạy. Khả năng cho: nghiên cứu, suy nghĩ, bản thảo đầu tiên, bất cứ nơi nào con đường là một phần của câu trả lời. Khó để chơi lại. Khó để thử nghiệm. Murah để nguyên mẫu.
- **Flow.**Hình đồ dựa trên sự kiện mà bạn sở hữu.`@start`đánh dấu lối vào. `@listen(topic)`là một bước phát nổ khi một bước khác phát ra chủ đề đó. mỗi bước là Python đơn giản (có thể gọi một Crew nội bộ).

Các bác sĩ đề nghị sản xuất năm 2026: bắt đầu với một dòng chảy.`Crew.kickoff()`Flow cho bạn những con đường kiểm tra, Crew cho bạn những cuộc khám phá.

> 文档 2026 年的生产建议: từ Flow 开始――当自主性值其成本时,将 Crew 作为 `Crew.kickoff()`调用嵌入 Flow 步骤中. Flow 提供审计追踪,Crew 提供探索能力.

> CrewAI sẽ nhiều Agent 协作建模为角色团队(Crew) 和事件驱动流程(Flow)两种模式──四种原语:Agent(角色+目标+背景故事)、Task(任务)、Crew(团队容器)、Process(执行策略)。

### Kết hợp công cụ

Ba cách để cho một nhân viên một công cụ.

> Có 3 cách để cung cấp cho đại lý một công cụ.

> CrewAI sẽ nhiều Agent 协作建模为角色团队(Crew) 和事件驱动流程(Flow)两种模式──四种原语:Agent(角色+目标+背景故事)、Task(任务)、Crew(团队容器)、Process(执行策略)。

1. **`@tool` decorator.**Các chức năng tinh khiết trở thành công cụ. Biên bản là sơ đồ; docstring là mô tả mà LLM thấy.

   ```python
   from crewai.tools import tool

   @tool("Search the web")
   def search(query: str) -> str:
       """Return top results for the query."""
       return run_search(query)
   ```

2. **`BaseTool` subclass.**Công cụ dựa trên lớp với schema args rõ ràng, hỗ trợ async, thử lại. Sử dụng khi công cụ có trạng thái (một client, một cache) hoặc cần các args cấu trúc.

   ```python
   from crewai.tools import BaseTool
   from pydantic import BaseModel

   class SearchArgs(BaseModel):
       query: str
       limit: int = 10

   class SearchTool(BaseTool):
       name = "web_search"
       description = "Search the web and return top results."
       args_schema = SearchArgs

       def _run(self, query: str, limit: int = 10) -> str:
           return self.client.search(query, limit=limit)
   ```

3. **Built-in toolkits.**CrewAI cung cấp các bộ chuyển đổi bên đầu tiên: `SerperDevTool`- `FileReadTool`- `DirectoryReadTool`- `CodeInterpreterTool`- `RagTool`- `WebsiteSearchTool`- Được cáp bằng một khẩu.

Các kết quả cấu trúc sử dụng Pydantic.`output_pydantic=MyModel`CrewAI xác nhận phản ứng LLM đối với mô hình và hoặc ép buộc hoặc thử lại.`expected_output`string. Các kết quả văn bản tự do là tốt cho bản thảo; kết quả cấu trúc là những gì dòng chảy hạ lưu có thể tiêu thụ.

> 结构化输出使用 Pydantic──在 任务 上传入 `output_pydantic=MyModel` Đơn vị tuyển dụng theo mô hình 校验 LLM  đáp ứng, không phù hợp 强制转换或重试――搭配严格的 `expected_output`字符串使用──自由文本输出适合草稿; cấu trúc输出才是下游 Flow 可以消费的──

> CrewAI sẽ nhiều Agent 协作建模为角色团队(Crew) 和事件驱动流程(Flow)两种模式──四种原语:Agent(角色+目标+背景故事)、Task(任务)、Crew(团队容器)、Process(执行策略)。

### Cây móc nhớ

CrewAI đưa ra bốn loại bộ nhớ ra khỏi hộp.

> CrewAI  mở hộp cung cấp bốn loại ký ức. Chúng có thể được sử dụng: một Crew có thể kích hoạt tất cả bốn loại cùng một lúc.

> **Validated against**CrewAI 0.86 (2026-05). Các bản phát hành gần đây sẽ hướng mọi thứ qua một hệ thống thống nhất `Memory`mô hình khái niệm dưới đây vẫn còn tồn tại, nhưng bề mặt lớp công cộng có thể sụp đổ thành một`Memory`điểm nhập vào trong các phiên bản mới hơn; kiểm tra [CrewAI memory docs](https://docs.crewai.com/concepts/memory)cho API hiện tại.

- **Short-term.**Buffer trò chuyện trong một lần chạy.
- **Long-term.**Cung cấp trong các lần chạy. Cung cấp trong một vector DB (Chroma mặc định, có thể thay đổi).
- **Entity.**"Điều kiện của khách hàng X là trong kế hoạch doanh nghiệp". Định nghĩa bởi tổ chức, không phải bởi sự tương đồng.
- **Contextual.**Lấy lại thời gian tập hợp, lấy bộ nhớ liên quan vào thời điểm mà đại lý cần nó, không phải tải trước.

Khả năng trên phi hành đoàn với `memory=True`Memory là một trong những nơi mà CrewAI kiếm được sự giữ gìn của mình đối với các khung mỏng hơn; LangGraph tinh khiết đòi hỏi bạn phải tự dây mỗi trong số này.

> Trong phi hành đoàn lên qua `memory=True`Hoặc theo loại cấu hình để kích hoạt. Từ các bản nhúng của bạn.

> CrewAI sẽ nhiều Agent 协作建模为角色团队(Crew) 和事件驱动流程(Flow)两种模式──四种原语:Agent(角色+目标+背景故事)、Task(任务)、Crew(团队容器)、Process(执行策略)。

### Khi CrewAI phù hợp
### Khi các nhóm dựa trên vai trò phù hợp

- 3 đến 6 nhân viên với vai trò được đặt tên và một quy trình làm việc hợp tác.
- Đường dẫn nơi phán quyết của LLM về bước tiếp theo là một phần của giá trị (Tầm bậc).
- Bất cứ nơi nào mà đội ngũ đều vui hơn khi đọc sách.`role + goal + backstory`hơn là đọc một định nghĩa biểu đồ.

### Khi họ không

- Các DAG xác định với thứ tự nghiêm ngặt. Sử dụng LangGraph (Dạy học 13).
- Các ngân sách chậm thứ hai. Hiérarchical thêm đi lại và đi lại. Ngay cả Sequential cũng liên tục liên tục các yêu cầu bao gồm các câu chuyện sau và các kết quả trước đó.
- Các vòng lặp đơn đại lý. Trượt khung; một vòng lặp đại lý (Dạy 1) cộng với một sổ đăng ký công cụ ngắn hơn.

Bài học 17 (Tradeoffs của cơ quan cơ quan) đưa ra điều này trong một matrix.

> 第 17 课(Agent 框架权衡) sử dụng矩阵 cho thấy điều này.

> 🤔 **【困惑】**Q: CrewAI 文档 nói" sản xuất môi trường từ dòng chảy  bắt đầu", nhưng tôi xem YouTube 教程全是 Crew 例子, ¿底该信谁? A: 信文档。YouTube 教程偏向演示 效果(Crew tự chủ协作看起来更酷), nhưng môi trường sản xuất cần là**可重放、可审计、可监控** Những chỉ có dòng chảy 能给;; gợi ý Pathway: dùng Crew làm nguyên thủy thử nghiệm ý tưởng;;

> CrewAI sẽ nhiều Agent 协作建模为角色团队(Crew) 和事件驱动流程(Flow)两种模式──四种原语:Agent(角色+目标+背景故事)、Task(任务)、Crew(团队容器)、Process(执行策略)。

### Hình dạng phụ thuộc

Không phụ thuộc vào LangChain. Python 3.10 đến 3.13. sử dụng `uv`Nhìn xem.[crewAIInc/crewAI](https://github.com/crewAIInc/crewAI)(Snapshot từ năm 2026-05). Sự tích hợp AWS Bedrock được ghi nhận; các điểm chuẩn của nhà cung cấp báo cáo về tốc độ tăng đáng kể so với LangGraph trên khối lượng công việc QA, nhưng phương pháp (dữ liệu, phần cứng, métrics đánh giá) không được công bố, vì vậy hãy coi số nhà cung cấp khung như chỉ hướng.

> Không phụ thuộc vào LangChain. 支持Python 3.10 đến 3.13. 使用`uv`包管理──AWS Bedrock 集成已有文件; 供应商基准测试报告称在QA 工作负载上有显著加速,但方法论(数据集、硬件、评估指标) chưa được công bố, do đó sẽ chỉ dùng dữ liệu của framework供应商作为参考──

> CrewAI sẽ nhiều Agent 协作建模为角色团队(Crew) 和事件驱动流程(Flow)两种模式──四种原语:Agent(角色+目标+背景故事)、Task(任务)、Crew(团队容器)、Process(执行策略)。

### Khi mô hình này đi sai

- **Prompt-bloat from backstories.**Một câu chuyện hậu cảnh 2000 từ cho mỗi đại lý và một đội ngũ 5 đại lý đốt cháy ngân sách ngữ cảnh trước khi gọi công cụ đầu tiên. Giữ câu chuyện hậu thuẫn dưới 200 từ. Sử dụng lại các cụm từ trên các đại lý; không lặp lại phong cách nhà năm lần.

> **背景故事导致的提示膨胀。**Mỗi câu chuyện bối cảnh của Agent 2000 字, cộng với 5 nhóm của Agent, đã hết trên ngân sách sau khi sử dụng công cụ đầu tiên.
- **Manager-LLM token tax.**Quá trình phân cấp thêm một cuộc gọi LLM quản lý trước mỗi cuộc gọi chuyên gia. Trong một đội ngũ năm nhiệm vụ là sáu cuộc gọi LLM thay vì năm, và cuộc gọi quản lý mang theo danh sách nhiệm vụ đầy đủ cộng với các đầu ra trước đó.

> **管理者 LLM 的 Token 税。**Các nhóm của 5 nhiệm vụ được chuyển thành 6 nhiệm vụ LLM thay vì 5 lần, và các quản lý được chuyển thành một danh sách nhiệm vụ đầy đủ và các sản phẩm trước đó.
- **Brittle handoffs.**Nhiệm vụ N.`expected_output`là "một phác thảo". Nhiệm vụ N+1 đọc nó như `context`Và cố gắng phân tích ba phần. LLM đã tạo ra bốn.`output_pydantic`trên Task N do đó Task N+1 đọc một đối tượng được gõ, không phải văn bản tự do.

> **脆弱的交接。**任务 N của `expected_output`là "một bản thảo"―― nhiệm vụ N+1 sẽ được coi là`context`读取并尝试解析三个部分──LLM 生成四个──下游 代理 即兴发挥──用 `output_pydantic`修复任务 N,让任务 N+1 读取类型化对象而非自由文本。
- **Crew-as-prod.**Đơn vị tự do Crew được vận chuyển đến sản xuất mà không có một vòng vòng vòng dòng.

> **Crew 直接上生产。**Không bao bì thành dòng chảy 就将自由形式 Crew 发布到生产环境──输出变异性高;无法重放;值班人员无法对抗好坏运行──使用 Flow 包装──

## Hãy xây dựng nó.
```figure
ae-crew-vs-flow
```

## Hãy xây dựng nó

`code/main.py`thực hiện các phiên bản STDlib của cả hai hình dạng cộng với một phi hành đoàn 3 nhân viên.

> `code/main.py`Sử dụng các tiêu chuẩn thực hiện hai hình dạng và một nhóm 3 đại lý.

> CrewAI sẽ nhiều Agent 协作建模为角色团队(Crew) 和事件驱动流程(Flow)两种模式──四种原语:Agent(角色+目标+背景故事)、Task(任务)、Crew(团队容器)、Process(执行策略)。

Hình dạng:

- `Agent`- `Task`Các lớp dữ liệu phù hợp với bề mặt của CrewAI.
- `SequentialCrew.kickoff(inputs)`chạy các nhiệm vụ theo thứ tự tuyên bố, threading các kết quả như `context`- Tôi không biết.
- `HierarchicalCrew.kickoff(topic)`thêm một quản lý đại lý chọn chuyên gia tiếp theo mỗi vòng, dừng lại ở "đã làm".
- `Flow`với `@start`và `@listen(topic)`những người trang trí, một vòng lặp nhỏ, và một dấu vết.
- `tool(name)`Bộ trang trí phản chiếu CrewAI `@tool`hình dạng.
- `Memory`với `short_term`- `long_term`- `entity`cửa hàng; sự tương đồng đùa sử dụng numpy.
- Phản ứng LLM giả là chuỗi mã hóa cứng được khóa khỏi vai trò cộng với tiền tố nhập. Không mạng.

Demo cụ thể: nhà nghiên cứu, nhà văn, nhóm biên tập viên sản xuất một bản tóm tắt về "kỹ thuật đại lý 2026". Nhà nghiên cứu kéo (cười) các nguồn. Nhà văn bản thảo. biên tập viên chặt chẽ. cùng một nhóm chạy qua một dòng chảy để hiển thị hình dạng xác định.

> 具体演示:研究员、作者、编辑组成团队,生成一篇关于"agent engineering 2026"的简报──研究员获取(模拟的) 来源──作者起草──编辑精炼──同一个团队通过流动 运行以展示确定性形态──

> CrewAI sẽ nhiều Agent 协作建模为角色团队(Crew) 和事件驱动流程(Flow)两种模式──四种原语:Agent(角色+目标+背景故事)、Task(任务)、Crew(团队容器)、Process(执行策略)。

Đi đi.

```bash
python3 code/main.py
```

Các dấu vết: các dòng băng thông của thủy thủ đoàn`context`, nhóm cấp bậc với các lựa chọn quản lý (phác giả, nhà văn, biên tập viên, sau đó "được thực hiện"), dòng chảy chạy cùng ba bước với các chủ đề rõ ràng (`researched`- `drafted`- `edited`), các cuộc gọi công cụ được chuyển qua `@tool`, và trí nhớ lâu dài sống sót sau hai cú đá.

> CrewAI sẽ nhiều Agent 协作建模为角色团队(Crew) 和事件驱动流程(Flow)两种模式──四种原语:Agent(角色+目标+背景故事)、Task(任务)、Crew(团队容器)、Process(执行策略)。

Hình ảnh của phi hành đoàn là chất lỏng, người quản lý có thể đặt lại nguyên tắc.

> Việc theo dõi phi hành đoàn là di động; về nguyên tắc quản lý có thể được sắp xếp lại.

> CrewAI sẽ nhiều Agent 协作建模为角色团队(Crew) 和事件驱动流程(Flow)两种模式──四种原语:Agent(角色+目标+背景故事)、Task(任务)、Crew(团队容器)、Process(执行策略)。

## Hãy sử dụng nó để thực hiện

- **CrewAI Flow**cho sản xuất. ngay cả khi dòng chảy là một bước đòi hỏi`Crew.kickoff()`- Tầm chảy cho phép kiểm toán.
- **CrewAI Crew (Sequential)**cho việc hợp tác sắp xếp rõ ràng, đặc biệt là các bản thảo đầu tiên và vòng xem xét.
- **CrewAI Crew (Hierarchical)**khi định tuyến phụ thuộc vào đầu ra và bạn có bốn chuyên gia hoặc nhiều hơn.
- **LangGraph**(Dân học 13) cho máy trạng thái rõ ràng, hồ sơ lâu dài, sắp xếp nghiêm ngặt.
- **AutoGen v0.4**(Dân học 14) cho đồng thời diễn viên-chương model và sự cô lập lỗi.
- **OpenAI Agents SDK**(Dân học 16) cho các sản phẩm đầu tiên của OpenAI với bàn tay và hàng rào.
- **Claude Agent SDK**(Dân học 17) cho các sản phẩm Claude-first với các bộ phận phụ và cửa hàng phiên.

## Chuyển nó đi.

`outputs/skill-crew-or-flow.md`chọn Crew vs Flow cho một nhiệm vụ và chuẩn bị cho việc thực hiện tối thiểu. Hard từ chối về Crew-without-backstory, Flow-without-explicit-topics, Hierarchical với dưới ba chuyên gia.

> `outputs/skill-crew-or-flow.md`Để một nhiệm vụ chọn Crew còn là Flow,并搭建最小实现──硬性拒绝:没有背景故事的 Crew、没有明显的主题的 Flow、少于三个专家的层级模式──

> CrewAI sẽ nhiều Agent 协作建模为角色团队(Crew) 和事件驱动流程(Flow)两种模式──四种原语:Agent(角色+目标+背景故事)、Task(任务)、Crew(团队容器)、Process(执行策略)。

## # Thói bẫy #

- **Backstory as flavor.**Nó tạo ra các kết quả, thử 3 biến thể cho mỗi đại lý, biến thể là thực.

> **把背景故事当装饰。**Nó thực sự tạo ra ra các sản xuất. Mỗi đại lý thử nghiệm ba biến thể; sự khác biệt là thực.
- **Skipping `expected_output`.**Không có hợp đồng cho mỗi nhiệm vụ, các nhiệm vụ tiếp theo sẽ thu được bất cứ điều gì mà LLM đã sản xuất.

> **跳过 `expected_output`。**Không có thỏa thuận của mỗi nhiệm vụ, nhiệm vụ sẽ nhận bất kỳ nội dung nào của LLM 生成.
- **Memory always-on.**Long term viết mỗi run vector DB tăng lên lấy lại trở nên ồn ào phạm vi viết cho các nhiệm vụ nơi thực tế là duy trì

> **记忆始终开启。**长期记忆每次运行都写入――向量数据库不断增长――检索变杂――将写入范围限制在需要持久化事实任务――
- **Manager prompt drift.**Nếu đường dẫn trở nên kỳ lạ, hãy bỏ nó vào chế độ từ ngữ và đọc.

> **管理者提示漂移。**层级模式的管理者提示是隐式的──如果路由变得奇怪,用词 模式导出并阅读──
- **Tool side effects in Crews.**Một phi hành đoàn có thể gọi công cụ nhiều lần hơn dự kiến.

> **Crew 中的工具副作用。**Thuỷ thủ đoàn có thể sử dụng nhiều hơn dự kiến các công cụ.

## Tập luyện bài tập

1. Chuyển đổi bộ phận của bộ máy theo dõi thành dòng chảy, đếm các điểm liên lạc khi biến động giảm, ghi lại khi độ đọc giảm.
  Trung ngữ翻译:思考并实践此练习。
2. Thêm bộ nhớ thực thể vào đội ngũ: các thông tin về khách hàng tồn tại qua các kickoff.
  Trung ngữ翻译:思考并实践此练习。
3. Thực hiện một quy trình Hiérarchical trong đó người quản lý từ chối định tuyến đến biên tập viên cho đến khi xuất của nhà văn có ít nhất ba đoạn.
  Trung ngữ翻译:思考并实践此练习。
4. Đưa dây a `BaseTool`Subclass cho một tìm kiếm web (phản chế). So sánh hình dạng dấu vết so với `@tool`phiên bản trang trí.
  Trung ngữ翻译:思考并实践此练习。
5. Thêm `output_pydantic=Brief`cho nhiệm vụ biên tập viên, nơi `Brief`- Có `title`- `summary`- `sections`. Làm cho tác vụ nhà văn xuất phát JSON bị trục trặc một lần; xác minh hành vi thử lại của CrewAI trong theo dõi.
  Trung ngữ翻译:思考并实践此练习。
6. Đọc phần giới thiệu về tài liệu của CrewAI.`crewai`API, phiên bản STDlib bỏ qua những đảm bảo nào?
  Trung ngữ翻译:思考并实践此练习。
7. Đưa AgentOps hoặc Langfuse (Dạy 24) vào một cuộc chạy thực sự.
  Trung ngữ翻译:思考并实践此练习。

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| Agent | "Persona" | Role + goal + backstory + tools |  |
| Task | "Unit of work" | Description + expected output + assignee + optional structured output |  |
| Crew | "Agent team" | Container for Agents + Tasks + Process |  |
| Process | "Execution strategy" | Sequential / Hierarchical / Consensus (planned) |  |
| Flow | "Deterministic workflow" | Event-driven, code-owned, testable |  |
| Backstory | "Persona prompt" | Tone and judgment shaper for the Agent |  |
| `@tool` | "Function tool" | Decorator that turns a function into a tool the Agent can call |  |
| `BaseTool` | "Class tool" | Class-based tool with args schema, retries, async support |  |
| Entity memory | "Per-entity facts" | Memory scoped to a customer / account / issue |  |
| Long-term memory | "Cross-run memory" | Vector-backed memory that survives between kickoffs |  |
| Contextual memory | "Just-in-time retrieval" | Memory pulled at the moment the Agent needs it |  |
| Manager LLM | "Router agent" | Extra LLM in Hierarchical process that picks the next task |  |
| `expected_output` | "Task contract" | String that tells the Agent (and audit) what shape to return |  |

## Xem thêm 延伸阅读

- [CrewAI docs introduction](https://docs.crewai.com/en/introduction): khái niệm và con đường sản xuất được khuyến cáo
  Trung ngữ: 翻译:见原文.
- [CrewAI Flows guide](https://docs.crewai.com/en/concepts/flows): hình dạng dựa trên sự kiện,`@start`- `@listen`
  Trung ngữ: 翻译:见原文.
- [CrewAI tools reference](https://docs.crewai.com/en/concepts/tools)`@tool`- `BaseTool`, bộ dụng cụ tích hợp
  Trung ngữ: 翻译:见原文.
- [CrewAI memory](https://docs.crewai.com/en/concepts/memory): ngắn hạn, dài hạn, đơn vị, ngữ cảnh
  Trung ngữ: 翻译:见原文.
- [Anthropic, Building Effective Agents](https://www.anthropic.com/research/building-effective-agents): khi multi-agent giúp đỡ và khi nó không
  Trung ngữ: 翻译:见原文.
- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview): sự thay thế của máy nhà nước
  Trung ngữ: 翻译:见原文.
