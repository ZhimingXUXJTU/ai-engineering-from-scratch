# Tại sao lại có nhiều đại lý?

> Một nhân viên đâm vào một bức tường.

> **【中文解读】**Phần này giới thiệu lý do tại sao cần nhiều đại lý  hệ thống  đơn đại lý  trên các vấn đề  hỗn loạn vai trò và chuỗi , cũng như cách nhiều đại lý  thông qua sự hợp tác phân công để giải quyết những vấn đề này.

> **【拓展：why multi agent→具体应用】**Một đại lý trong việc xử lý nhiệm vụ phức tạp phải đối mặt với ba chai: 1) 上下文溢出 tất cả thông tin vào một cửa sổ, quan trọng bị lấp lánh; 2) 角色混乱 một đại lý đóng nhiều vai trò dẫn đến lời nói xung đột; 3) 串行执行工具调用只能排队――多 đại lý 通过分工协作解决这些问题――Anthropic nghiên cứu cho thấy, nhiều đại lý 系统在BrowseComp 基准上多 đại lý 升 90.2%,80% của người chỉ bằng mã hóa sử dụng khác biệt giải thích――

>  **【前置】**Học本节前请先掌握:Phase 14(Agent Engineering)全部, đặc biệt làPhase 14·01(Agent Loop) vàPhase 14·28(Orchestration Patterns)。本节回答"什么时候用多 Agent"简单回答:单 Agent + 工具不够时。Anthropic 经验法则:任务需要 > 50 工具调用、或 > 1 个角色(如研究员 + 写手)、或并行能省时间,才考虑多 Agent。

>  **【类比】**单 Agent vs 多 Agent = 全能管家 vs 专业团队──全能管家──单 Agent) có thể làm tất cả mọi thứ nhưng mỗi thứ đều không精: buổi sáng làm ăn, buổi chiều làm việc, buổi tối làm việc, mỗi cách đều nửa吊子──专业团队──多 Agent:厨师专做饭、机修工专修车、家教专辅导, mỗi người精一行──代价:协调成本(Agent 间通信) và phức tạp tăng đơn giản nhiệm vụ với Agent 更划算──

**Type:** Learn | **类型:** 学习
**Languages:** TypeScript | **语言:** TypeScript
**Prerequisites:** Phase 14 (Agent Engineering) | **前置知识:** Phase 14 (Agent 工程)
**Time:** ~60 minutes | **时间:** ~60 分钟

## Mục tiêu học tập

- Xác định giới hạn đơn tác nhân (sự lội lội trong bối cảnh, chuyên môn hỗn hợp, nút thắt lỏng theo trình tự) và giải thích khi phân chia thành nhiều tác nhân là động đúng đắn
  Trung文翻译:识别单代理上限(上下文溢出、专业能力混合、串行瓶),并解释何时分为多代理 是正确的选择
- So sánh các mô hình dàn nhạc (chuồng ống, fan-out song song, giám sát, cấp bậc) và chọn đúng cho một cấu trúc nhiệm vụ nhất định
  Trung ngữ翻译:比较编排模式(流水线、并行扇出、监督者、分层),并为给定任务结构选择合适的模式
- Thiết kế một hệ thống đa đại lý với ranh giới vai trò rõ ràng, trạng thái chia sẻ và hợp đồng giao tiếp
  Trung ngữ翻译: thiết kế một hệ thống đa đại lý với vai trò rõ ràng.
- Phân tích các sự thỏa hiệp về sự phức tạp của nhiều đại lý (sự trễ, chi phí, khó khăn trong việc gỡ lỗi) so với sự đơn giản của một đại lý
  Trung ngữ翻译:分析多 Agent 复杂性(延迟、成本、调试难度) và đơn Agent 简单性

## Vấn đề  vấn đề giới thiệu

Bạn đã xây dựng một đại lý duy nhất trong giai đoạn 14. Nó hoạt động. Nó có thể đọc các tệp, chạy lệnh, gọi API và lý luận về kết quả. Sau đó bạn chỉ nó vào một cơ sở mã thực sự: 200 tệp, ba ngôn ngữ, các bài kiểm tra phụ thuộc vào cơ sở hạ tầng, và yêu cầu nghiên cứu các API bên ngoài trước khi viết mã.

> Bạn xây dựng một Agent đơn trong giai đoạn 14. Nó hoạt động tốt, có thể đọc các tài liệu, thực hiện lệnh, điều chỉnh API và đưa ra suy luận về kết quả. Sau đó bạn sẽ hướng nó đến một thư viện mã thực tế: 200 tài liệu, 3 ngôn ngữ, kiểm tra dựa trên cơ sở hạ tầng, cũng như cần phải nghiên cứu trước các yêu cầu của API bên ngoài để viết lại mã.

Khoảng cách giữa các đại lý demo và đại lý sản xuất là khoảng cách giữa "một tập tin, một ngôn ngữ, một công cụ" và "rất nhiều tập tin, nhiều ngôn ngữ, nhiều công cụ có phụ thuộc".

> Sự khác biệt giữa đại lý và đại lý sản xuất là sự khác biệt giữa "một tài liệu, một ngôn ngữ, một công cụ" và "nhiều tài liệu, nhiều ngôn ngữ, nhiều công cụ phụ thuộc".

Đại lý bị ngạt không phải vì LLM là ngốc, mà vì nhiệm vụ vượt quá những gì một vòng lặp đại lý có thể xử lý. cửa sổ ngữ cảnh chứa đầy nội dung tập tin. Đại lý quên những gì họ đọc 40 cuộc gọi công cụ trước. Nó cố gắng trở thành một nhà nghiên cứu, một lập trình viên, và một nhà phê bình tất cả cùng một lúc, và làm cả ba đều kém.

> Trưởng lý đã bị phá hủy. Không phải vì LLM  ngu ngốc, mà vì nhiệm vụ vượt quá phạm vi xử lý của một Trưởng lý.

Đây là trần nhà đơn, bạn phải đánh vào nó mỗi khi một nhiệm vụ đòi hỏi:

> Đó là một đặc vụ duy nhất. Mỗi nhiệm vụ cần phải có những điều kiện sau đây.

Màn giới là cấu trúc, không phải là thuật toán. LLM tốt hơn trì hoãn màn giới nhưng không loại bỏ nó. Một cửa sổ ngữ cảnh mã thông báo 1M lấp đầy chắc chắn như một 200k  nó chỉ cần mất nhiều tệp hơn.

> Upper limit là cấu trúc, không phải là thuật toán. Có một LLM tốt hơn 延迟上限但不移除它.

- **More context than fits in one window**- đọc 50 tập tin thổi qua 200k token
  Trung ngữ翻译:**超出一个窗口容量的上下文** 读取 50 文件会超过200k token
- **Different expertise at different stages**- nghiên cứu đòi hỏi sự thúc đẩy khác so với việc tạo ra mã
  Trung ngữ翻译:**不同阶段需要不同的专业知识** Nghiên cứu cần tạo ra các gợi ý khác với mã
- **Work that can happen in parallel**- Tại sao đọc ba tập tin theo trình tự khi bạn có thể đọc chúng cùng lúc?
  Trung ngữ翻译:**可以并行执行的工作**  Vì vậy, nếu có thể đọc 3 tài liệu cùng lúc, tại sao lại phải đọc một cách trật tự?

## Khái niệm cốt lõi

### Màn giới đơn tác nhân

Một đại lý đơn lẻ là một vòng lặp, một cửa sổ ngữ cảnh, một lệnh hệ thống.

> 单代理是一个循环,一个上下文窗口,一个系统提示,一个系统提示,一个系统提示,一个系统提示,一个系统提示,一个系统提示,一个系统提示,一个系统提示,一个系统提示,一个系统提示,一个系统提示,一个系统提示,一个系统提示,一个系统提示,一个系统提示,一个系统提示,一个系统提示,一个系统提示,一个系统提示,一个系统提示,一个循环,一个循环,一个循环,一个循环,一个循环,一个循环,一个系统提示,一个系统提示,一个系统提示,一个系统提示,一个系统提示,一个系统提示,一个循环,一个循环,一个循环,一个循环,一个循环,一个循环,一个循环,一个循环,一个循环,一个循环,一个循环,一个一个循环,一个一个一个循环,一个一个一个一个循环,一个一个一个一个一个循环,一个一个一个一个一个一个一个一个一个一个一个一个一个一个一个一个一个一个一个一个一个一个一个一个一个一个一个一个一个一个一个一个一个一个一个一个一个一个一个一个一个一个一个一个一个一个一个一个一个一个一个一个一个一个一个一个一个一个一个一个一个一个一个一个一个一个一个一个一个一个一个一个一个一个一个一个一个一个一个一个一个一个一个一个一个一个一个一个一个一个一个一个一个一个一个一个

```
┌─────────────────────────────────────────┐
│            SINGLE AGENT                 │
│                                         │
│  ┌───────────────────────────────────┐  │
│  │         Context Window            │  │
│  │                                   │  │
│  │  research notes                   │  │
│  │  + code files                     │  │
│  │  + test output                    │  │
│  │  + review feedback                │  │
│  │  + API docs                       │  │
│  │  + ...                            │  │
│  │                                   │  │
│  │  ██████████████████████ FULL ███  │  │
│  └───────────────────────────────────┘  │
│                                         │
│  One system prompt tries to cover       │
│  research + coding + review + testing   │
│                                         │
│  Result: mediocre at everything         │
└─────────────────────────────────────────┘
```

Chỉ cần một hệ thống đơn giản là nguyên nhân gốc rễ. Nó phải đưa ra hướng dẫn cho nghiên cứu, lập trình, xem xét và thử nghiệm cùng một lúc. Mỗi hướng dẫn làm suy yếu các hướng dẫn khác.

> 单系统提示是根本原因――它必须同时提供指令用于研究,编码,审核和测试――每条指令稀释其他――Agent 最终在所有事上"还行",在任何事上都不优秀――

Ba thứ bị phá vỡ:

> Ba vấn đề sẽ dẫn đến sự sụp đổ:

1. **Context saturation**- Kết quả công cụ tích lũy. Đến lượt 30, đại lý đã tiêu thụ 150k token nội dung tập tin, đầu ra lệnh, và lý luận trước.
   Trung ngữ翻译:**上下文饱和** 工具结果不断堆积──到第30轮时,Agent 已消耗150k token 文件内容、命令输出和先前推理──第5轮关键细节丢失──

2. **Role confusion**- một lệnh hệ thống nói "bạn là một nhà nghiên cứu, lập trình, kiểm tra và kiểm tra" tạo ra một đại lý nửa nghiên cứu, nửa mã hóa, và không bao giờ hoàn thành kiểm tra.
   Trung ngữ翻译:**角色混乱** Một lời khuyên hệ thống viết "tên là nhà nghiên cứu, lập trình viên, kiểm tra viên và kiểm tra viên" sẽ tạo ra một nửa nghiên cứu, nửa biên tập, luôn là một đại lý không hoàn thành kiểm tra.

3. **Sequential bottleneck**- đại lý đọc tập tin A, rồi tập tin B, rồi tập tin C. Ba cuộc gọi liên tiếp của LLM. Ba vụ xử tử liên tiếp của công cụ.
   Trung ngữ翻译:**串行瓶颈** Đại lý 读取文件 A,然后文件 B,然后文件 C──三次串行 LLM 调用──三次串行工具执行──没有并行性──

Một đại lý đơn là một nhà nói chung được yêu cầu là một chuyên gia ở mỗi bước.

> Một đại lý là một người được yêu cầu trở thành chuyên gia trong mỗi bước. Nhiều đại lý phân chia công việc, để mỗi đại lý trở thành chuyên gia trong một vấn đề.

### Giải pháp đa tác nhân

Chia công việc cho mỗi nhân viên một công việc, một cửa sổ ngữ cảnh, và một hệ thống nhắc nhở được điều chỉnh cho công việc đó:

> 拆分工作──给每位代理一个任务、一个上下文窗口和一个系统提示:

Đây là "lần phân tách các mối quan tâm" áp dụng cho các đại lý LLM. Các lời nhắc của mỗi đại lý là ngắn hơn và tập trung hơn.

> Đây là một ứng dụng cho "trong điểm phân chia" của LLM Agent. Mỗi Agent's tip ngắn hơn tập trung hơn. Mỗi Agent's upside window chỉ có nó cần. Mỗi Agent có thể tự kiểm tra và cải tiến.

```
┌──────────────────────────────────────────────────────────┐
│                    ORCHESTRATOR                          │
│                                                          │
│  "Build a REST API for user management"                  │
│                                                          │
│         ┌──────────┬──────────┬──────────┐               │
│         │          │          │          │               │
│         ▼          ▼          ▼          ▼               │
│   ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │
│   │RESEARCHER│ │  CODER   │ │ REVIEWER │ │  TESTER  │  │
│   │          │ │          │ │          │ │          │  │
│   │ Reads    │ │ Writes   │ │ Checks   │ │ Runs     │  │
│   │ docs,    │ │ code     │ │ code     │ │ tests,   │  │
│   │ finds    │ │ based on │ │ quality, │ │ reports  │  │
│   │ patterns │ │ research │ │ finds    │ │ results  │  │
│   │          │ │ + spec   │ │ bugs     │ │          │  │
│   └─────┬────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘  │
│         │           │            │             │         │
│         └───────────┴────────────┴─────────────┘         │
│                          │                               │
│                     Merge results                        │
└──────────────────────────────────────────────────────────┘
```

Mỗi đại lý có:
- Một lời nhắc hệ thống tập trung ("Bạn là một nhà kiểm tra mã. Công việc duy nhất của bạn là tìm ra lỗi. ")
  Trung ngữ翻译:一个聚焦的系统提示("你是一个代码审阅者──你的唯一任务是发现 bug──")
- Chiếc cửa sổ ngữ cảnh của riêng nó (không bị ô nhiễm bởi công việc của các nhân viên khác)
  Trung ngữ翻译:自己的上下文窗口(不被其他代理的工作污染)
- Hợp đồng đầu vào/ ra ra rõ ràng (tận nhận ghi chú nghiên cứu, mã ra ra)
  Trung ngữ翻译:清晰的输入/输出契约(接收研究笔记,输出代码)

Các đại lý tổ chức chỉ cần hiểu nhiệm vụ cấp cao và cách ủy thác. Nó không cần phải biết làm thế nào để làm mỗi nhiệm vụ phụ. Mỗi đại lý chuyên gia chỉ cần biết công việc hẹp của riêng mình.

> 编排 Đại lý chỉ cần hiểu nhiệm vụ cấp cao và làm thế nào để ủy nhiệm. Nó không cần biết làm thế nào để hoàn thành từng nhiệm vụ.

### Hệ thống thực sự làm điều này

**Claude Code subagents**- khi Claude Code sinh ra một con người với `Task`, nó tạo ra một nhân viên trẻ với một nhiệm vụ có mục tiêu. Cha mẹ giữ bối cảnh của nó sạch sẽ. đứa trẻ làm công việc tập trung và trả lại một bản tóm tắt.

> **Claude Code 子 Agent** 当 Claude Code 使用 `Task`Khi sinh thành con Trưởng 时, nó sẽ tạo ra một Trưởng 具有有限范围的子 代理.

Mô hình này là viral bởi vì nó tạo thành: một subagent có thể sinh ra các subagent của riêng mình. Ba cấp độ sâu là phổ biến trong các nhiệm vụ mã hóa phức tạp; ngoài đó, gỡ lỗi trở nên đau đớn.

> Mô hình này được truyền tải bởi vì nó có thể được kết hợp: Sub Agent có thể tạo ra Sub Agent của riêng mình.

**Devin**- chạy một đại lý lập kế hoạch, một đại lý lập trình và một đại lý trình duyệt.

> **Devin** 运行一个规划代理一个编码代理 和一个浏览器代理――规划器将工作分解成步骤――编码器编写代码――浏览器研究文档――每个都有独立的上下文――

Kiến trúc của Devin là mô hình giám sát sách giáo khoa: một nhà hoạch định sở hữu kế hoạch toàn cầu, nhiều nhân viên chuyên môn thực hiện các đoạn.

> Kiến trúc của Devin là mô hình giám sát viên của các giáo khoa: một lập trình viên có kế hoạch toàn diện, một chuyên gia làm việc nhiều đoạn trình duyệt.

**Multi-agent coding teams (SWE-bench)**- các hệ thống hiệu suất cao nhất trên ghế SWE sử dụng một nhà nghiên cứu đọc cơ sở mã, một lập kế hoạch thiết kế sửa chữa và một lập trình điều chỉnh mã thực hiện nó.

> **多 Agent 编码团队 (SWE-bench)** SWE-bench trên hệ thống hiệu suất tốt nhất sử dụng một nhà nghiên cứu trong thư viện mã hóa, một lập trình viên sửa đổi kế hoạch thiết kế và một bộ lập trình viên sửa đổi thực hiện.

Các bảng xếp hạng SWE-bench 2026 được thống trị bởi các hệ thống đa đại lý. Mô hình: một nhà nghiên cứu với một bối cảnh lớn để hiểu cơ sở mã, một lập kế hoạch với một lời nhắc tập trung để thiết kế sửa chữa, một lập trình mã có các yêu cầu gõ nghiêm ngặt cho thực hiện. Mỗi vai trò nhận được lời nhắc cần thiết.

> 2026 năm SWE-bench  xếp hạng bởi nhiều đại lý  hệ thống thống quản lý 模式:带大上下文的研究员用于代码库理解 带焦点提示的规划器用于修复设计 带严格类型要求的编码器用于实现 带大上下文的研究员用于代码库理解 带焦点提示的规划器用于修复设计 带严格类型要求用于实现 带严格类型要求的编码器用于实现 带大上下文的研究员用于编码库理解 带焦点提示的规划器用于修复设计 带严格类型要求的编码器用于实现 带大上下文的研究员用于实现 带大上下文的编码库理解 带焦点提示的编码器用于实现 带严格类型要求的编码器用于实现 带大上角色获得其需要的提示──

**ChatGPT Deep Research**- tạo ra nhiều nhân viên tìm kiếm song song, mỗi người khám phá một góc độ khác nhau, sau đó tổng hợp kết quả.

> **ChatGPT Deep Research** và tạo ra nhiều search agent, mỗi tìm kiếm góc độ khác nhau, sau đó tổng hợp kết quả.

### Phân quang phổ

Multi-agent không phải là nhị phân.

> 多 Agent không phải là 2元.

Các hệ thống nghiên cứu thực sự sử dụng 5-50 đại lý. Điểm đúng trên phổ phụ thuộc vào sự phức tạp của nhiệm vụ.

> Phương pháp quang phổ quan trọng, bởi vì hầu hết các hệ thống sản xuất không có một cực.

```
SIMPLE ──────────────────────────────────────────── COMPLEX

 Single        Sub-         Pipeline      Team         Swarm
 Agent         agents

 ┌───┐       ┌───┐        ┌───┐───┐    ┌───┐───┐    ┌─┐┌─┐┌─┐
 │ A │       │ A │        │ A │ B │    │ A │ B │    │ ││ ││ │
 └───┘       └─┬─┘        └───┘─┬─┘    └─┬─┘─┬─┘    └┬┘└┬┘└┬┘
               │                │        │   │       ┌┴──┴──┴┐
             ┌─┴─┐          ┌───┘───┐    │   │       │shared │
             │ a │          │ C │ D │  ┌─┴───┴─┐    │ state │
             └───┘          └───┘───┘  │  msg   │    └───────┘
                                       │  bus   │
 1 loop      Parent +      Stage by    │       │    N peers,
 1 context   child tasks   stage       └───────┘    emergent
                                       Explicit      behavior
                                       roles
```

**Single agent**- Một vòng lặp, một cú thôi thúc.

> **单 Agent**Một vòng, một gợi ý, phù hợp với một nhiệm vụ đơn giản.

**Subagents**- một người cha sinh con để tập trung các nhiệm vụ phụ. người cha duy trì kế hoạch. trẻ báo cáo lại. Đây là điều Claude Code làm.

> **子 Agent** Bác sĩ đối phó vì tập trung các nhiệm vụ của mình  Bác sĩ đối phó  Bác sĩ đối phó  Bác sĩ đối phó  Bác sĩ đối phó  Bác sĩ đối phó  Bác sĩ đối phó  Bác sĩ đối phó  Bác sĩ đối phó  Bác sĩ đối phó  Bác sĩ đối phó  Bác sĩ đối phó  Bác sĩ đối phó  Bác sĩ đối phó  Bác sĩ đối phó  Bác sĩ đối phó  Bác sĩ đối phó  Bác sĩ đối phó  Bác sĩ đối phó  Bác sĩ đối phó  Bác sĩ đối phó  Bác sĩ đối phó  Bác sĩ đối phó  Bác sĩ đối phó  Bác sĩ đối phó  Bác sĩ đối phó  Bác sĩ đối phó  Bác sĩ đối phó  Bác sĩ đối phó  Bác sĩ đối phó  Bác sĩ đối phó  Bác sĩ đối phó 

**Pipeline**- các đại lý chạy theo trình tự. đầu ra của đại lý A trở thành đầu vào của đại lý B. Được cho các dòng công việc giai đoạn: nghiên cứu -> mã -> đánh giá -> thử nghiệm.

> **流水线** Agent 顺序运行──Agent A's输出成为 Agent B's输入──适合分阶段的工作流:研究 -> 编码 -> 审阅 -> 测试──

**Team**- các đại lý chạy song song với một bus thông điệp chia sẻ mỗi người có một vai trò một dàn nhạc phối hợp tốt khi có những kỹ năng khác nhau được yêu cầu cùng lúc

> **团队** Đại diện 通过共享消息总线并行运行.

**Swarm**- nhiều đại lý giống hệt hoặc gần giống hệt với trạng thái chung không có nhạc cụ cố định đại lý nhận công việc từ hàng đợi tốt cho các nhiệm vụ song song song có hiệu suất cao

> **群体**  Nhiều đồng hoặc gần giống nhau Agent 共享状态── không có trình sắp xếp cố định──Agent lấy việc từ hàng ngũ── thích hợp với các nhiệm vụ đồng hành với lượng thụ lượng cao──

### Bốn mô hình đa tác nhân

#### Mô hình 1: đường ống dẫn

```
Input ──▶ Agent A ──▶ Agent B ──▶ Agent C ──▶ Output
          (research)  (code)      (review)
```

Mỗi đại lý biến đổi dữ liệu và truyền chúng ra.

> Mỗi đại lý chuyển dữ liệu và chuyển tiếp cho người tiếp theo.

Sử dụng khi: mỗi giai đoạn có một đầu vào / đầu ra rõ ràng và các giai đoạn tự nhiên là liên tục. Nghiên cứu → mã → đánh giá → thử nghiệm là ví dụ điển hình. Tránh khi: các giai đoạn có thể chạy song song hoặc cần lặp lại giữa chúng.

> Sử dụng trường hợp: mỗi giai đoạn có một sự nhập/ ra và giai đoạn tự nhiên để thực hiện.

#### Mô hình 2: Fan-out / Fan-in

```
                ┌──▶ Agent A ──┐
                │              │
Input ──▶ Split ├──▶ Agent B ──├──▶ Merge ──▶ Output
                │              │
                └──▶ Agent C ──┘
```

Chia công việc qua các đại lý song song, sau đó kết hợp kết quả.

> Đưa công việc cho Đại lý cùng hành trình, sau đó kết quả cùng hành trình.

Sử dụng khi: nhiệm vụ chia thành các phần độc lập (ví dụ: tìm kiếm 5 nguồn khác nhau, tóm tắt 10 tài liệu). Tránh khi: các nhiệm vụ phụ thuộc vào nhau hoặc hợp nhất đòi hỏi suy luận sâu sắc.

> Sử dụng trường hợp: nhiệm vụ có thể được chia ra rõ ràng thành phần độc lập (如搜索 5 个不同来源,总结 10 份文档)

#### Mô hình 3: Người làm nhạc cụ

```
                    ┌──────────┐
                    │  Orch.   │
                    └──┬───┬───┘
                  task │   │ task
                 ┌─────┘   └─────┐
                 ▼               ▼
           ┌──────────┐   ┌──────────┐
           │ Worker A │   │ Worker B │
           └──────────┘   └──────────┘
```

Một nhà dàn nhạc thông minh quyết định những gì phải làm, ủy quyền cho công nhân, và tổng hợp kết quả.

> 智能编排器决定做什么,委派给工作器,并综合结果――编排器本身是一个具有生成工作器工具的代理――

Sử dụng khi nào: nhiệm vụ là đủ phức tạp để quyết định phải làm gì là một vấn đề khó khăn.

> Sử dụng trường hợp: nhiệm vụ đủ phức tạp, quyết định làm gì tự nó là một vấn đề khó khăn.

#### Mô hình 4: Nhóm đồng nghiệp

```
         ┌───┐ ◄──── msg ────▶ ┌───┐
         │ A │                  │ B │
         └─┬─┘                  └─┬─┘
           │                      │
      msg  │    ┌───────────┐     │ msg
           └───▶│  Shared   │◄────┘
                │  State    │
           ┌───▶│  / Queue  │◄────┐
           │    └───────────┘     │
      msg  │                      │ msg
         ┌─┴─┐                  ┌─┴─┐
         │ C │ ◄──── msg ────▶ │ D │
         └───┘                  └───┘
```

Không có người tổ chức trung tâm, các đại lý giao tiếp với nhau, quyết định xuất hiện từ sự tương tác, khó khăn hơn để sửa lỗi, nhưng có thể đạt được nhiều đại lý.

> Không có bộ điều chỉnh trung ương.

Sử dụng khi: nhiều đại lý đồng nhất làm việc tương tự (các loại, phân loại) trên quy mô. Tránh khi: bạn cần một kế hoạch nhất quán hoặc sắp xếp nghiêm ngặt.

> Sử dụng trường hợp: Nhiều đồng chất Đại lý làm việc tương tự quy mô lớn

### Khi nào không nên sử dụng nhiều chất

Multi-agent thêm sự phức tạp. Mỗi tin nhắn giữa các đại lý là một điểm thất bại tiềm năng. Debug từ "đọc một cuộc trò chuyện" đến "để theo dõi tin nhắn trên năm đại lý".

> Nhiều đại lý  tăng độ phức tạp. Mỗi thông điệp giữa các đại lý là một điểm cố tiềm ẩn.

**Stay single-agent when:**
- Nhiệm vụ phù hợp trong một cửa sổ ngữ cảnh (dưới ~ 100k token dữ liệu làm việc)
  Trung ngữ翻译:任务适合一个上下文窗口(工作数据不超过约100k token)
- Bạn không cần các hệ thống khác nhau cho các giai đoạn khác nhau
  Trung語翻译:不同阶段不需要不同的系统提示
- Việc xử lý theo trình tự là đủ nhanh
  Trung ngữ翻译:顺序执行速度足够快
- Nhiệm vụ là đủ đơn giản để chia nó thêm thêm chi phí hơn giá trị
  Trung ngữ翻译: nhiệm vụ đủ đơn giản, chia chia tăng chi phí hơn giá trị của nó

**The complexity cost:**
- Mỗi ranh giới của đại lý là một bước nén thua lỗ: toàn bộ bối cảnh của đại lý A được tóm tắt thành một thông điệp cho đại lý B
  Trung ngữ翻译: Mỗi đại lý 边界都是有损压缩步骤:
- Lễ thuật phối hợp (người làm gì, khi nào, theo thứ tự nào) là nguồn lỗi của riêng nó
  中文翻译:协调逻辑(谁做什么、何时做、按什么顺序) tự nó là một lỗi nguồn
- N đại lý có nghĩa là N liên hệ LLM gọi tối thiểu, nhiều hơn nếu họ cần nói chuyện về phía trước và về phía sau
  Trung ngữ翻译:延迟增加:N 个代理 nghĩa là ít nhất N 次串行 LLM 调用, nếu cần đến lại cuộc hội thoại则更多
- Chi phí nhân: mỗi đại lý đốt token độc lập
  Trung文翻译:成本倍增: mỗi đại lý 独立消耗代币

Quy tắc: nếu một nhiệm vụ mất ít hơn 20 cuộc gọi công cụ và phù hợp với 100k token, hãy giữ nó đơn đại lý.

> 经验法则: Nếu một nhiệm vụ chỉ cần ít hơn 20 lần sử dụng công cụ, và phù hợp với 100k token, hãy giữ một đại lý.

## Hãy xây dựng nó.
```figure
swarm-messages
```

## Hãy xây dựng nó

### Bước 1: Người đơn bị quá tải

Đây là một đại lý đơn lẻ cố gắng làm mọi thứ. Nó có một hệ thống lớn nhắc và một cửa sổ ngữ cảnh chứa nghiên cứu, mã, và đánh giá:

> Đây là một đại lý đơn lẻ cố gắng làm mọi thứ. Nó có một hệ thống lớn và một cửa sổ chứa nghiên cứu, mã và kiểm tra trên:

```typescript
type AgentResult = {
  content: string;
  tokensUsed: number;
  toolCalls: number;
};

async function singleAgentApproach(task: string): Promise<AgentResult> {
  const systemPrompt = `You are a full-stack developer. You must:
1. Research the requirements
2. Write the code
3. Review the code for bugs
4. Write tests
Do ALL of these in a single conversation.`;

  const contextWindow: string[] = [];
  let totalTokens = 0;
  let totalToolCalls = 0;

  const research = await fakeLLMCall(systemPrompt, `Research: ${task}`);
  contextWindow.push(research.output);
  totalTokens += research.tokens;
  totalToolCalls += research.calls;

  const code = await fakeLLMCall(
    systemPrompt,
    `Given this research:\n${contextWindow.join("\n")}\n\nNow write code for: ${task}`
  );
  contextWindow.push(code.output);
  totalTokens += code.tokens;
  totalToolCalls += code.calls;

  const review = await fakeLLMCall(
    systemPrompt,
    `Given all previous context:\n${contextWindow.join("\n")}\n\nReview the code.`
  );
  contextWindow.push(review.output);
  totalTokens += review.tokens;
  totalToolCalls += review.calls;

  return {
    content: contextWindow.join("\n---\n"),
    tokensUsed: totalTokens,
    toolCalls: totalToolCalls,
  };
}
```

Vấn đề với phương pháp này:
- Chiếc cửa sổ ngữ cảnh tăng lên với mỗi giai đoạn.
  Trung ngữ翻译:上下文窗口随着每个阶段的增长──到审阅步骤时,它包含研究笔记和代码以及前先的推理──
- Các hệ thống yêu cầu là chung. Nó không thể được điều chỉnh cho mỗi giai đoạn.
  Trung ngữ翻译:系统提示是通用──不能为每个阶段调优──
- Không có gì chạy song song.
  Trung ngữ翻译:没有并行执行。

Loop đơn-chỉ buộc LLM phải chuyển đổi ngữ cảnh giữa các nhiệm vụ nhận thức rất khác nhau (bảo sát vs mã hóa vs đánh giá) ở mỗi lượt.

> 单代理循环迫使 LLM Mỗi vòng trong rất khác nhau nhận thức nhiệm vụ (研究 vs 编码 vs 审阅) giữa chuyển đổi trên 下文──每次切换都损质量──

### Bước 2: Các đại lý chuyên nghiệp

Giờ thì chia nó ra.

> Giờ thì hãy chia tay nó. Mỗi đại lý sẽ có được một nhiệm vụ.

```typescript
type SpecialistAgent = {
  name: string;
  systemPrompt: string;
  run: (input: string) => Promise<AgentResult>;
};

function createSpecialist(name: string, systemPrompt: string): SpecialistAgent {
  return {
    name,
    systemPrompt,
    run: async (input: string) => {
      const result = await fakeLLMCall(systemPrompt, input);
      return {
        content: result.output,
        tokensUsed: result.tokens,
        toolCalls: result.calls,
      };
    },
  };
}

const researcher = createSpecialist(
  "researcher",
  "You are a technical researcher. Read documentation, find patterns, and summarize findings. Output only the facts needed for implementation."
);

const coder = createSpecialist(
  "coder",
  "You are a senior TypeScript developer. Given requirements and research notes, write clean, tested code. Nothing else."
);

const reviewer = createSpecialist(
  "reviewer",
  "You are a code reviewer. Find bugs, security issues, and logic errors. Be specific. Cite line numbers."
);
```

Mỗi chuyên gia có một lời nhắc tập trung. Mỗi người nhận được một cửa sổ ngữ cảnh sạch sẽ chỉ có đầu vào cần thiết.

> Mỗi chuyên gia có một gợi ý tập trung. Mỗi người đều có một cửa sổ văn bản trên sạch, chỉ chứa các mục nhập cần thiết.

Các yêu cầu của nhà nghiên cứu được tối ưu hóa để đọc và tóm tắt. yêu cầu của lập trình viên được tối ưu hóa để viết mã sạch. yêu cầu của nhà đánh giá được tối ưu hóa để tìm ra lỗi. Không một yêu cầu đơn lẻ cố gắng làm cả ba.

> Các gợi ý của nhà nghiên cứu về đọc và tổng kết tối ưu hóa. Các gợi ý của nhà biên tập về viết mã sạch tối ưu hóa.

### Bước 3: Kết hợp thông qua tin nhắn

Đưa tin nhắn cho các chuyên gia cùng với thông điệp rõ ràng:

> Thông qua thông tin thông báo sẽ chuyên gia kết nối:

```typescript
type AgentMessage = {
  from: string;
  to: string;
  content: string;
  timestamp: number;
};

async function multiAgentApproach(task: string): Promise<AgentResult> {
  const messages: AgentMessage[] = [];
  let totalTokens = 0;
  let totalToolCalls = 0;

  const researchResult = await researcher.run(task);
  messages.push({
    from: "researcher",
    to: "coder",
    content: researchResult.content,
    timestamp: Date.now(),
  });
  totalTokens += researchResult.tokensUsed;
  totalToolCalls += researchResult.toolCalls;

  const coderInput = messages
    .filter((m) => m.to === "coder")
    .map((m) => `[From ${m.from}]: ${m.content}`)
    .join("\n");

  const codeResult = await coder.run(coderInput);
  messages.push({
    from: "coder",
    to: "reviewer",
    content: codeResult.content,
    timestamp: Date.now(),
  });
  totalTokens += codeResult.tokensUsed;
  totalToolCalls += codeResult.toolCalls;

  const reviewerInput = messages
    .filter((m) => m.to === "reviewer")
    .map((m) => `[From ${m.from}]: ${m.content}`)
    .join("\n");

  const reviewResult = await reviewer.run(reviewerInput);
  messages.push({
    from: "reviewer",
    to: "orchestrator",
    content: reviewResult.content,
    timestamp: Date.now(),
  });
  totalTokens += reviewResult.tokensUsed;
  totalToolCalls += reviewResult.toolCalls;

  return {
    content: messages.map((m) => `[${m.from} -> ${m.to}]: ${m.content}`).join("\n\n"),
    tokensUsed: totalTokens,
    toolCalls: totalToolCalls,
  };
}
```

Mỗi đại lý chỉ nhận được những thông điệp được gửi đến họ. Không có ô nhiễm ngữ cảnh. 50k token của nhà nghiên cứu đọc tài liệu không bao giờ vào ngữ cảnh của nhà phê bình.

> Mỗi đại lý chỉ nhận được thông điệp của mình. Không có bất cứ thứ gì bị ô nhiễm.

Đây là chiến thắng cốt lõi: sự cô lập thông tin. cửa sổ bối cảnh của mỗi đại lý được dành riêng cho nhiệm vụ của riêng mình. Ngân sách 200k token của một đại lý không bị lãng phí cho việc cạo cạo của các đại lý khác.

> Đó là ưu điểm cốt lõi: Information isolation. Mỗi cửa sổ trên dưới của mỗi đại lý tập trung vào nhiệm vụ của mình.

### Bước 4: So sánh

```typescript
async function compare() {
  const task = "Build a rate limiter middleware for an Express.js API";

  console.log("=== Single Agent ===");
  const single = await singleAgentApproach(task);
  console.log(`Tokens: ${single.tokensUsed}`);
  console.log(`Tool calls: ${single.toolCalls}`);

  console.log("\n=== Multi-Agent ===");
  const multi = await multiAgentApproach(task);
  console.log(`Tokens: ${multi.tokensUsed}`);
  console.log(`Tool calls: ${multi.toolCalls}`);
}
```

Phiên bản đa đại lý sử dụng nhiều mã thông báo tổng cộng hơn (ba đại lý, ba cuộc gọi LLM riêng biệt) nhưng bối cảnh của mỗi đại lý vẫn sạch sẽ.

> Nhiều đại lý  phiên bản sử dụng nhiều hơn tổng token ((3 đại lý, 3 lần độc lập LLM 调用), nhưng mỗi đại lý trên dưới văn bản giữ sạch.

Việc giao dịch là rõ ràng: chi tiêu nhiều hơn, có được sản lượng tốt hơn. Đáng giá khi nhiệm vụ khó khăn. Không đáng giá cho "đánh tổng hợp đoạn này".

> 权衡很清晰:花更多代币,获得更好的输出――任务难时值得――对"总结这一段"不值得――

## Hãy sử dụng nó để thực hiện

Bài học này tạo ra một lời nhắc tái sử dụng để quyết định khi nào nên đi đa đại lý.`outputs/prompt-multi-agent-decision.md`- Tôi không biết.

> Bài học này đưa ra một gợi ý có thể lặp lại, để quyết định khi nào sử dụng nhiều đại lý.`outputs/prompt-multi-agent-decision.md`

Các yêu cầu đặt ra bốn câu hỏi chẩn đoán: (1) nhiệm vụ cần hơn 100k token của bối cảnh làm việc? (2) nó cần chuyên môn khác nhau tại các giai đoạn khác nhau? (3) có công việc song song? (4) sự phức tạp có đáng để chi phí chung?

> Các đề nghị hỏi bốn câu hỏi chẩn đoán: 1) 任务 có cần hơn 100k token 工作上下文? 2) 不同阶段 có cần kiến thức chuyên môn khác nhau? 3) có có có có có có có có có được làm? 4) 复杂性是否值得开销?

## Tập luyện bài tập

1. Thêm một chuyên gia thứ tư: một đại lý "tử nghiệm" nhận mã từ trình lập trình và xem xét phản hồi từ người xem xét, sau đó viết các bài kiểm tra
   Trung ngữ翻译:添加第四专家: một "测试员" Trưởng, nhận mã của biên tập viên và phản của người xem, sau đó biên tập bài kiểm tra
2. Thay đổi đường ống để người xem có thể gửi phản hồi trở lại cho trình lập trình để một vòng sửa đổi (tối đa 2 vòng)
   Trung ngữ翻译:修改流水线, để người xem có thể sẽ phản gửi trở lại编码器 để thực hiện sửa đổi vòng lặp ((最多 2 轮)
3. Chuyển đổi đường ống nối theo trình tự thành một fan-out: chạy nhà nghiên cứu và một "đánh phân tích yêu cầu" đại lý song song, sau đó kết hợp các đầu ra của họ trước khi chuyển đến coder
   Trung ngữ翻译:将顺序流水线转换为扇出:并行运行研究员和"需求分析师"代理, sau đó hợp并输出再传递它们给编码器

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Swarm / 群体 | "A hive mind of AI agents" / "AI Agent 的蜂巢思维" | A set of peer agents with shared state and no fixed leader. Behavior emerges from local interactions. / 一组具有共享状态且无固定领导者的对等 Agent。行为从局部交互中涌现。 |
| Orchestrator / 编排器 | "The boss agent" / "老板 Agent" | An agent whose tools include spawning and managing other agents. It plans and delegates but may not do the actual work. / 一个工具包括生成和管理其他 Agent 的 Agent。它规划和委派，但可能不做实际工作。 |
| Coordinator / 协调器 | "The traffic cop" / "交通警察" | A non-agent component (often just code, not an LLM) that routes messages between agents based on rules. / 一个非 Agent 组件（通常只是代码，不是 LLM），根据规则在 Agent 之间路由消息。 |
| Consensus / 共识 | "The agents agree" / "Agent 们达成一致" | A protocol where multiple agents must reach agreement before proceeding. Used when conflicting outputs need resolution. / 多个 Agent 在继续之前必须达成一致的协议。用于需要解决冲突输出的情况。 |
| Emergent behavior / 涌现行为 | "The agents figured it out themselves" / "Agent 自己想出来的" | System-level patterns that arise from agent interactions but were not explicitly programmed. Can be useful or harmful. / 从 Agent 交互中产生但未被明确编程的系统级模式。可能有用也可能有害。 |
| Fan-out / fan-in / 扇出/扇入 | "Map-reduce for agents" / "Agent 的 Map-reduce" | Splitting a task across parallel agents (fan-out), then combining their results (fan-in). / 将任务分配给并行 Agent（扇出），然后合并它们的结果（扇入）。 |
| Message passing / 消息传递 | "Agents talk to each other" / "Agent 之间互相交谈" | The communication mechanism between agents: structured data sent from one agent to another, replacing shared context windows. / Agent 之间的通信机制：从一个 Agent 发送到另一个 Agent 的结构化数据，替代共享上下文窗口。 |

## Xem thêm 延伸阅读

- [The Landscape of Emerging AI Agent Architectures](https://arxiv.org/abs/2409.02977)- khảo sát các mô hình đa tác nhân
  Trung文翻译:新兴 AI Agent 架构概览  多 Agent 模式综述
- [AutoGen: Enabling Next-Gen LLM Applications](https://arxiv.org/abs/2308.08155)- Microsoft đa đại lý hội thoại framework
  Trung ngữ翻译:AutoGen:赋能下一代 LLM 应用  微软的多代理对话框架
- [Claude Code subagents documentation](https://docs.anthropic.com/en/docs/claude-code)- cách Claude Code ủy nhiệm với Task
  中文翻译:Claude Code 子 Agent 文档  Claude Code 如何使用任务委派
- [CrewAI documentation](https://docs.crewai.com/)- khung đa tác nhân dựa trên vai trò
  Trung文翻译:CrewAI 文档  基于角色的多代理框架
