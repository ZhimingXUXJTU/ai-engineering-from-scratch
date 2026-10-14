# Cảnh sát viên Claude SDK: Subagents và Session Store
# The Harness như một thư viện  Subbagents và Sessions Store

> Một vòng xoáy bạn có thể nhập khẩu: công cụ tích hợp, các bộ phận phụ cho sự cô lập ngữ cảnh, móc, phổ biến dấu vết W3C, sự bền bỉ của phiên.

**Type:** Learn + Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 01 (Agent Loop), Phase 14 · 10 (Skill Libraries) | **前置知识:** 见原文
**Time:** ~75 minutes | **时间:** 见原文

## Mục tiêu học tập

- Giải thích sự khác biệt giữa SDK Client Anthropic (raw API) và SDK Claude Agent (phụng cáp).
- Mô tả các yếu tố phụ  song song và cách ly ngữ cảnh  và khi nào để đạt được chúng.
- Tên miền của bộ SDK Python (`append`- `load`- `list_sessions`- `delete`- `list_subkeys`) và vai trò của `--session-mirror`- Tôi không biết.
- Thực hiện một vòng xoáy stdlib với các công cụ tích hợp, sinh con con con con với bối cảnh cô lập, nát vòng đời và một cửa hàng phiên.

## Vấn đề  vấn đề giới thiệu

Một API LLM thô cung cấp cho bạn một chuyến đi trở lại. Một đại lý sản xuất cần thực thi công cụ, máy chủ MCP, móng vòng đời, sinh sản phụ, sự kiên trì phiên, phổ biến dấu vết. Claude Agent SDK gửi hình dạng này như một thư viện  cùng một vòng xoáy Claude Code sử dụng, phơi bày cho các đại lý tùy chỉnh.

> 原始 LLM API chỉ có thể cung cấp cho bạn một lần quay trở lại调用――生产级 Agent 需要工具执行、MCP 服务器、生命周期子、子 Agent 生成、会话持久化、追踪传播――Claude Agent SDK sẽ đưa ra hình thức này như một thư viện cung cấp Claude Code sử dụng cùng một vòng, tiếp xúc với tự xác định Agent sử dụng――


> **【中文解读】**Claude Agent SDK là một nhân văn 官方的 Agent 开发框架──核心特性:(1) 内置工具(文件读写、代码执行等);(2) 子 Agent 支持Agent 可以生成子 Agent 处理子任务;(3) 生命周期子在 Agent 执行的关键节点插入自定义逻辑──SDK 深度集成 Claude 的扩展思维能力──

> **{【拓展：Claude Agent SDK 是 2026 年 Claude 生态的核心开发工具。与 OpenA...】}**Claude Agent SDK là một công cụ phát triển cốt lõi của Claude năm 2026.[1][2] Compared to OpenAI Agents SDK, it focuses more on deeply integrating Claude's unique capabilities (ví dụ như Long Thinking, Computer Use)[3][3] SDK's Sub Agent Mode allows Agent to break complex tasks into subtasks, mỗi subtask is handled by a specialized sub Agent, similar to the departmental division in an organization.[4]

>  **【前置】**必须先掌握:Phase 14·01(Agent Loop) vàPhase 14·10(Skill Libraries) Claude Agent SDK đã đặt ra kỹ năng 系统作为子 Agent的标准模式── Nếu bạn chưa sử dụng Claude Code CLI, hãy khuyên mạnh mẽ sử dụng một vài ngày trước đây本 SDK đó là hình thức của Claude Code, hiểu mô hình hành vi của CLI đối với việc học SDK

## Khái niệm cốt lõi

### SDK khách hàng vs SDK đại lý

- **Client SDK (`anthropic`).**API tin nhắn nguyên liệu, bạn sở hữu vòng lặp, công cụ, nhà nước.
- **Agent SDK (`claude-agent-sdk`).**Thiết lập trình thực hiện công cụ, kết nối MCP, cục, sản xuất con, cửa hàng phiên bản.

> **Client SDK（`anthropic`）。**Định nghĩa của bản thân bạn quản lý vòng lặp, công cụ và trạng thái.
> **Agent SDK（`claude-agent-sdk`）。**Trong đó, các công cụ được sử dụng để thực hiện các công cụ của mình.

### Công cụ tích hợp

SDK đưa ra 10 công cụ hơn trong hộp: file read/write, shell, grep, glob, web fetch, nhiều hơn nữa.

> SDK 开箱提供 10+ 工具:文件读写,shell,grep,glob,网页抓取等──自定义工具通过标准工具-schema 接口注册──

> Claude Agent SDK là Cơ quan chính thức của Anthropic 框架──核心概念:Agent(带系统提示和工具的 LLM)、Tools(可调用函数)、Subagents(子代理委派)、Session Store(会话持久化)──

### Các bộ phận phụ

Hai mục đích được ghi nhận bởi Anthropic:

> Anthropic 文档 ghi lại hai mục đích:

1. **Parallelization.**Thực hiện công việc độc lập đồng thời. "Xem hồ sơ thử nghiệm cho mỗi 20 mô-đun này" là 20 nhiệm vụ phụ song song.
2. **Context isolation.**Các subagents sử dụng cửa sổ ngữ cảnh của riêng họ; chỉ có kết quả trở lại cho nhạc sĩ. Ngân sách của nhạc sĩ được bảo tồn.

Python SDK bổ sung gần đây: `list_subagents()`- `get_subagent_messages()`để đọc bản ghi của subagent.

> Python SDK gần đây nhất:`list_subagents()``get_subagent_messages()`Để đọc được bản ghi cuộc trò chuyện của đại lý.

>  **【类比】**子 Agent 像大公司的"项目组":CEO  主代理) nắm bắt toàn bộ quy trình, nhưng mỗi dự án cụ thể được thực hiện bởi một nhóm dự án đặc biệt 子 Agent) thực hiện, nhóm dự án có phòng họp độc lập **关键收益是上下文隔离**Nếu "调研竞品" như vậy làm việc để đọc 100 bài viết đầy trên các bài viết dưới đây, đại lý chính tự làm sẽ bị ngập nước; trao cho con đại lý, con đại lý của 100 bài viết đọc không làm ô nhiễm quan điểm của đại lý chính, chỉ trả lại 3 kết luận của phân tích竞品"

> Claude Agent SDK là Cơ quan chính thức của Anthropic 框架──核心概念:Agent(带系统提示和工具的 LLM)、Tools(可调用函数)、Subagents(子代理委派)、Session Store(会话持久化)──

### Tiệm bán phiên

Phân tích giao thức với TypeScript:

> Đối với các giao dịch của TypeScript 版本:

- `append(session_id, message)` thêm một vòng.
- `load(session_id)` khôi phục cuộc trò chuyện.
- `list_sessions()` đếm.
- `delete(session_id)` với các buổi tiếp theo.
- `list_subkeys(session_id)` liệt kê các chìa khóa phụ.

`--session-mirror`(CLI cờ) phản chiếu bản sao đến một tệp bên ngoài khi nó phát, để debugging.

> `--session-mirror`(CLI 标志) trong quá trình truyền tải sẽ ghi lại các video của cuộc trò chuyện vào các tài liệu bên ngoài, được sử dụng để điều tra.

> Claude Agent SDK là Cơ quan chính thức của Anthropic 框架──核心概念:Agent(带系统提示和工具的 LLM)、Tools(可调用函数)、Subagents(子代理委派)、Session Store(会话持久化)──

### Chân

Các cái nát chu kỳ đời bạn có thể đăng ký:

> Có đăng ký vòng đời:

- `PreToolUse`- `PostToolUse` gọi cổng hoặc công cụ kiểm toán.
- `SessionStart`- `SessionEnd` đặt và phá hủy.
- `UserPromptSubmit` hành động trên đầu vào của người dùng trước khi mô hình nhìn thấy nó.
- `PreCompact` chạy trước khi kết hợp ngữ cảnh.
- `Stop` làm sạch tại cửa ra của đại lý.
- `Notification` cảnh báo kênh bên.

Hooks là cách pro-workflow (phase 14 curriculum reference) và các hệ thống tương tự thêm hành vi cắt ngang.

> 子是专业工作流 (Phase 14 课程参考) và các hệ thống tương tự

> Claude Agent SDK là Cơ quan chính thức của Anthropic 框架──核心概念:Agent(带系统提示和工具的 LLM)、Tools(可调用函数)、Subagents(子代理委派)、Session Store(会话持久化)──

### W3C bối cảnh theo dõi

OTel hoạt động trên người gọi lan truyền vào các quá trình phụ CLI thông qua tiêu đề ngữ cảnh theo dõi W3C. Toàn bộ các quá trình theo dõi xuất hiện như một dấu vết trong phần sau của bạn.

> 调用方上活跃的OTel span 通过W3C 追踪上下文头传播到CLI 子进程──整个多进程追踪在你的后端显示为一个追踪──

> Claude Agent SDK là Cơ quan chính thức của Anthropic 框架──核心概念:Agent(带系统提示和工具的 LLM)、Tools(可调用函数)、Subagents(子代理委派)、Session Store(会话持久化)──

### Claude quản lý các nhân viên

Các lựa chọn khác được lưu trữ (beta header `managed-agents-2026-04-01`). Công việc đồng bộ lâu dài, lưu trữ nhanh tích hợp, nén tích hợp.

> 托管替方案`managed-agents-2026-04-01`(■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

> Claude Agent SDK là Cơ quan chính thức của Anthropic 框架──核心概念:Agent(带系统提示和工具的 LLM)、Tools(可调用函数)、Subagents(子代理委派)、Session Store(会话持久化)──

### Khi mô hình này đi sai

> ️ **【易错点】**Các thảm họa thường gặp nhất: 100 nhiệm vụ nhỏ để tạo ra 100 nhân viên.**后果**Mỗi con đại lý có hệ thống riêng của mình nhanh chóng + 工具注册 + 上下文初始化,开销 30-60 秒/个,100 个就是 1 小时;并发又有限制(Anthropic 每分钟代币 限制),最终任务跑一晚上。**一行修复**: năng lượng khối lượng nhiệm vụ sử dụng chủ nhân 串行做 (如"读 100文件" sử dụng Read 工具循环), chỉ cần thực sự cần "独立上下文窗口" nhiệm vụ (如深度调研) mới sinh ra 子 Agent。

- **Subagent over-spawn.**Cung cấp 100 bộ phận phụ cho 100 nhiệm vụ nhỏ, Overhead thống trị.
- **Hook creep.**Mỗi đội đều thêm các cái nát, các quả bóng thời gian khởi động, xem lại các cái nát hàng quý.
- **Session bloat.**Các buổi tập tích lũy; kích thước tăng lên. Sử dụng `list_sessions`+ Chính sách hết hạn.

> 🤔 **【困惑】**Q: Claude Agent SDK 和直接用人类 Python SDK 写代理循环 有什么本质区别?为什么要使用 SDK? A: 三个不可替代能力:(1) **内置工具开箱即用**(文件、shell、grep 等 10+ 工具, tự viết ít nhất hai ngày);(2) **Session 持久化协议**(包括子 Agent 会话级联删除);(3) **Hook 生命周期**Nếu đại lý của bạn chỉ đơn giản câu hỏi, hãy sử dụng SDK nhân đạo thì đủ; nếu bạn muốn viết Claude Code thì đó là đại lý cấp sản xuất, SDK 省你几周工程时间――

> **子 Agent 过度生成。**Để 100 nhiệm vụ nhỏ tạo ra 100 tác nhân,...
> **钩子膨胀。**Mỗi đội đều thêm 子; thời gian khởi động tăng lên.
> **会话膨胀。**会话不断积累; 大小增长──使用 `list_sessions`+ 过期策略──

## Hãy xây dựng nó.
```figure
ae-subagent-isolation
```

## Hãy xây dựng nó

`code/main.py`thực hiện hình dạng SDK trong stdlib:

> `code/main.py`Sử dụng tiêu chuẩn để thực hiện hình thức SDK:

> Claude Agent SDK là Cơ quan chính thức của Anthropic 框架──核心概念:Agent(带系统提示和工具的 LLM)、Tools(可调用函数)、Subagents(子代理委派)、Session Store(会话持久化)──

- `Tool`- `ToolRegistry`với tích hợp `read_file`- `write_file`- `list_dir`- Tôi không biết.
- `Subagent` bối cảnh riêng tư, chạy riêng biệt, kết quả trả lại.
- `SessionStore` thêm vào, tải, liệt kê, xóa, list_subkey.
- `Hooks` `pre_tool_use`- `post_tool_use`- `session_start`- `session_end`- Tôi không biết.
- Một demo: đại lý chính sinh ra 3 bộ phụ song song (mỗi một cách riêng biệt), tổng kết quả, tiếp tục phiên.

Đi đi.

```
python3 code/main.py
```

Hướng dẫn cho thấy sự cô lập ngữ cảnh phụ (kích thước ngữ cảnh của nhạc sĩ vẫn bị giới hạn), thực thi nồi và sự bền bỉ của phiên.

> 追踪显示子 Agent 的上下文隔离(编排者 上下文大小保持有界) 子执行和会话持久化──

> Claude Agent SDK là Cơ quan chính thức của Anthropic 框架──核心概念:Agent(带系统提示和工具的 LLM)、Tools(可调用函数)、Subagents(子代理委派)、Session Store(会话持久化)──

## Hãy sử dụng nó để thực hiện

- **Claude Agent SDK**cho các sản phẩm Claude-first muốn hình dạng vòng tay Claude Code.
- **Claude Managed Agents**cho công việc đồng bộ hoạt động lâu dài được lưu trữ.
- **OpenAI Agents SDK**(Dân học 16) đối với đối tác đầu tiên của OpenAI.
- **LangGraph + custom tools**Nếu bạn muốn máy trạng thái hình đồ thị thay vào đó.

## Chuyển nó đi.

`outputs/skill-claude-agent-scaffold.md`Thiết lập một ứng dụng Claude Agent SDK với các bộ phận phụ, nát, cửa hàng phiên, kết nối máy chủ MCP và phát triển dấu vết W3C.

> `outputs/skill-claude-agent-scaffold.md`搭建一个Claude Agent SDK 应用,包含子 Agent、子、会话存储、MCP 服务器连接和W3C 追踪传播──

> Claude Agent SDK là Cơ quan chính thức của Anthropic 框架──核心概念:Agent(带系统提示和工具的 LLM)、Tools(可调用函数)、Subagents(子代理委派)、Session Store(会话持久化)──

## Tập luyện bài tập

1. Thêm một bộ đẻ con phụ thuộc cho 20 nhiệm vụ thành các nhóm 5 bộ phụ song song. đo kích thước bối cảnh của dàn nhạc so sánh với một trong mỗi nhiệm vụ.
  Trung ngữ翻译:思考并实践此练习。
2. Thực hiện một`PreToolUse`Hook đó giới hạn lãi suất `write_file`gọi (5 phút mỗi phiên).
  Trung ngữ翻译:思考并实践此练习。
3. Sợi dây`list_subkeys`Làm thế nào để tạo ra một cây dưới lớp.
  Trung ngữ翻译:思考并实践此练习。
4. Đưa đồ chơi vào thực tế `claude-agent-sdk`Phạm vi Python. Những thay đổi gì về đăng ký công cụ?
  Trung ngữ翻译:思考并实践此练习。
5. Hãy đọc các tài liệu của Claude Managed Agents.
  Trung ngữ翻译:思考并实践此练习。

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| Agent SDK | "Claude Code as a library" | Harness shape: tools, MCP, hooks, subagents, session store |  |
| Subagent | "Child agent" | Separate context, own budget; results bubble up |  |
| Session store | "Conversation DB" | Persist, load, list, delete turns with subagent cascade |  |
| Hook | "Lifecycle callback" | Pre/post tool, session, prompt submit, compact, stop |  |
| W3C trace context | "Cross-process trace" | Parent span propagates into CLI subprocess |  |
| Managed Agents | "Hosted harness" | Anthropic-hosted long-running async work |  |
| `--session-mirror` | "Transcript mirror" | Writes session turns to an external file as they stream |  |
| MCP server | "Tool surface" | External tool/resource source attached to the agent |  |

## Xem thêm 延伸阅读

- [Claude Agent SDK overview](https://platform.claude.com/docs/en/agent-sdk/overview) hình thức thư viện của Claude Code
  Trung ngữ: 翻译:见原文.
- [Anthropic, Building agents with the Claude Agent SDK](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk) Các mô hình sản xuất
  Trung ngữ: 翻译:见原文.
- [Claude Managed Agents overview](https://platform.claude.com/docs/en/managed-agents/overview) thay thế được lưu trữ
  Trung ngữ: 翻译:见原文.
- [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/) đối tác
  Trung ngữ: 翻译:见原文.
