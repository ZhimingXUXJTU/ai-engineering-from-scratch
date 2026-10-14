# Máy làm việc của nhân viên tối thiểu

> Bàn làm việc hữu ích nhỏ nhất là ba tập tin: một bộ định tuyến hướng dẫn gốc, một tập tin trạng thái và một bảng tác vụ. Mọi thứ khác được xếp lớp trên. Nếu một repo không thể mang được ba tập tin này, không có mô hình nào sẽ lưu nó.

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 31 (Why Capable Models Still Fail) | **前置知识:** 见原文
**Time:** ~45 minutes | **时间:** 见原文

>  **【前置】**学本节前请先掌握:Phase 14·31(Workbench 为什么需要) ――本节实现最小可用工作板:3 个文件(root router、状态、任务板) ――

>  **【类比】** 最小工作桌 = 厨房最基础的 3 件物品:菜单板(root router,告诉厨师今天做什么) ✓备菜笔记(状态,记录已经切了什么) ✓待办清单(任务板,还剩什么没做) ✓Claude Code、Cursor等 Agent 工具底层都是这3 件套的扩展`CLAUDE.md`là router,`memory/`là tiểu bang,`tasks/`Đó là hội đồng nhiệm vụ.

## Mục tiêu học tập

- Định nghĩa ba tập tin tạo thành bảng làm việc tối thiểu khả thi.
- Giải thích tại sao một router gốc ngắn đánh bại một router monolithic dài `AGENTS.md`- Tôi không biết.
- Hãy tạo ra một tập tin nhà nước mà nhân viên có thể đọc ở mỗi lượt và viết ở cuối.
- Xây dựng một bảng nhiệm vụ tồn tại nhiều phiên làm việc mà không có lịch sử trò chuyện.

## Vấn đề  vấn đề giới thiệu

Hầu hết các nhóm tìm đến một bàn làm việc bằng cách viết một dòng 3000 `AGENTS.md`mô hình tải nó, bỏ qua các bộ phận mà nó không thể tóm tắt, và vẫn thất bại trên cùng một bề mặt mà nó luôn thất bại trên.

> Hầu hết các đội đã viết một bài 3000 bài.`AGENTS.md`Và gọi nó là hoàn thành để tìm kiếm một nền tảng làm việc. Mô hình tải nó, bỏ qua phần không thể kết luận, vẫn thất bại trên cùng một bề mặt.

Bạn cần ngược lại. Một tệp gốc nhỏ chỉ định tuyến người đại lý vào các tệp sâu hơn khi có liên quan. trạng thái bền người đại lý đọc trước khi hành động và viết sau đó. Một bảng tác vụ cho biết những gì đang bay, những gì bị chặn, và những gì tiếp theo.

> Bạn cần cách ngược lại. Một tập tin gốc nhỏ, chỉ trong thời gian liên quan sẽ dẫn đến các tập tin sâu hơn.


> **【中文解读】**工作台是理解编码 内部机制的起点──它包含五个核心组件:(1) 文件读写工具;(2) 代码执行沙盒;(3) 简单的 ReAct循环;(4) 消息缓冲区;(5) 停止条件──目标是让学习者从头上理解每个组件的作用和交互──

Ba tập tin, mỗi tập tin có một công việc, mỗi tập tin có thể đọc được bằng máy để phát triển thành một hệ thống thực sự sau này.

> Mỗi người đều có trách nhiệm của mình. Mỗi người đều có đủ máy tính để đọc để sau đó phát triển thành hệ thống thực.

> Máy làm việc của đại lý là một môi trường nhẹ để thử nghiệm và điều chỉnh hành vi của đại lý. Nó cung cấp không gian thực hiện tách biệt và các công cụ phân tích quỹ đạo chi tiết.

## Khái niệm cốt lõi

```mermaid
flowchart LR
  Agent[Agent Loop] --> Router[AGENTS.md]
  Router --> State[agent_state.json]
  Router --> Board[task_board.json]
  State --> Agent
  Board --> Agent
```


> **【中文解读】**工作台是理解编码 内部机制的起点──它包含五个核心组件:(1) 文件读写工具;(2) 代码执行沙盒;(3) 简单的 ReAct循环;(4) 消息缓冲区;(5) 停止条件──目标是让学习者从头上理解每个组件的作用和交互──

### AGENTS.md là một router, không phải là một hướng dẫn

Một cái tốt `AGENTS.md`Nó chỉ ra người đại lý đến:

> Máy làm việc của đại lý là một môi trường nhẹ để thử nghiệm và điều chỉnh hành vi của đại lý. Nó cung cấp không gian thực hiện tách biệt và các công cụ phân tích quỹ đạo chi tiết.

- Tài liệu của tiểu bang (nơi bạn đang ở).
- Bảng nhiệm vụ (điều còn lại).
- Các quy tắc sâu hơn (dưới `docs/agent-rules.md`().
- Chỉ thị xác minh (làm thế nào để biết nó hoạt động).

Bất cứ thứ gì dài hơn đều được ghi vào các tài liệu sâu hơn, chỉ được tải khi cần thiết, các hướng dẫn dài bị bỏ qua, các bộ định tuyến ngắn bị theo dõi.

> Nội dung dài hơn được đặt trong tài liệu sâu hơn, chỉ cần được tải lên.

> Máy làm việc của đại lý là một môi trường nhẹ để thử nghiệm và điều chỉnh hành vi của đại lý. Nó cung cấp không gian thực hiện tách biệt và các công cụ phân tích quỹ đạo chi tiết.

### agent_state.json là hệ thống ghi chép

Các trạng thái mang theo: ID nhiệm vụ hoạt động, các tệp được chạm vào, các giả định được thực hiện, các ngăn chặn, và hành động tiếp theo.

> Máy làm việc của đại lý là một môi trường nhẹ để thử nghiệm và điều chỉnh hành vi của đại lý. Nó cung cấp không gian thực hiện tách biệt và các công cụ phân tích quỹ đạo chi tiết.

Nhà nước sống trong một tập tin vì lịch sử trò chuyện không đáng tin cậy, các buổi nói chuyện bị cắt giảm, tập tin không.

>  trạng thái tồn tại trong tài liệu, vì lịch sử trò chuyện là không thể tin cậy.

> Máy làm việc của đại lý là một môi trường nhẹ để thử nghiệm và điều chỉnh hành vi của đại lý. Nó cung cấp không gian thực hiện tách biệt và các công cụ phân tích quỹ đạo chi tiết.

### task_board.json là hàng

Ban công việc thực hiện mọi nhiệm vụ với trạng thái `todo | in_progress | done | blocked`Đó là hàng đợi mà nhân viên rút ra khi trạng thái trống rỗng, và hàng đợi bạn đọc khi bạn muốn biết liệu nhân viên có trên đường đúng không.

> Máy làm việc của đại lý là một môi trường nhẹ để thử nghiệm và điều chỉnh hành vi của đại lý. Nó cung cấp không gian thực hiện tách biệt và các công cụ phân tích quỹ đạo chi tiết.

Một nhiệm vụ trên bảng có một ID, một mục tiêu, một chủ sở hữu (`builder`- `reviewer`, hoặc`human`), và các tiêu chí chấp nhận. bảng nhỏ: khi nó phát triển vượt qua màn hình, bạn có một vấn đề lập kế hoạch, không phải là vấn đề bảng.

> Máy làm việc của đại lý là một môi trường nhẹ để thử nghiệm và điều chỉnh hành vi của đại lý. Nó cung cấp không gian thực hiện tách biệt và các công cụ phân tích quỹ đạo chi tiết.

### Ba tập tin là sàn nhà, không phải trần nhà.

Các bài học sau đó thêm các hợp đồng phạm vi, các bộ chạy phản hồi, cổng xác minh, danh sách kiểm tra của các nhà phê bình và các gói giao hàng. Ba tập tin ở đây là những gì tất cả họ giả định.

> Các khóa học tiếp theo sẽ thêm phạm vi hợp đồng, phản vận hành, kiểm tra kiểm soát, kiểm tra kiểm tra và giao tiếp.

> Máy làm việc của đại lý là một môi trường nhẹ để thử nghiệm và điều chỉnh hành vi của đại lý. Nó cung cấp không gian thực hiện tách biệt và các công cụ phân tích quỹ đạo chi tiết.

## Hãy xây dựng nó.
```figure
wb-three-files
```

## Hãy xây dựng nó

`code/main.py`viết bảng làm việc tối thiểu thành repo trống và chứng minh một đại lý đơn biến đổi rằng:

> Máy làm việc của đại lý là một môi trường nhẹ để thử nghiệm và điều chỉnh hành vi của đại lý. Nó cung cấp không gian thực hiện tách biệt và các công cụ phân tích quỹ đạo chi tiết.

1. Đọc `agent_state.json`- Tôi không biết.
2. Lấy nhiệm vụ tiếp theo từ `task_board.json`nếu tiểu bang trống.
3. Đúng là một tập tin trong phạm vi.
4. Tác lại trạng thái cập nhật.

Đi đi.

```
python3 code/main.py
```

Bản kịch bản tạo ra`workdir/`bên cạnh chính nó, đặt xuống ba tập tin, chạy một lượt, và in sự khác biệt. chạy lại nó để xem như thế nào lượt thứ hai bắt đầu nơi mà lượt đầu tiên đã dừng lại.

> Máy làm việc của đại lý là một môi trường nhẹ để thử nghiệm và điều chỉnh hành vi của đại lý. Nó cung cấp không gian thực hiện tách biệt và các công cụ phân tích quỹ đạo chi tiết.

## Hãy sử dụng nó để thực hiện

Bên trong sản phẩm đại lý sản xuất, cùng ba tập tin xuất hiện dưới tên khác nhau:

> Máy làm việc của đại lý là một môi trường nhẹ để thử nghiệm và điều chỉnh hành vi của đại lý. Nó cung cấp không gian thực hiện tách biệt và các công cụ phân tích quỹ đạo chi tiết.

- **Claude Code:** `AGENTS.md`hoặc `CLAUDE.md`cho router, `.claude/state.json`- các cửa hàng kiểu nhà nước, móng tay cho hội đồng quản trị.
- **Codex / Cursor:**Quy tắc không gian làm việc cho router, bộ nhớ phiên cho trạng thái, các nhiệm vụ xếp hàng trong thanh bên trò chuyện cho bảng.
- **Custom Python agent:**cùng các tập tin mà anh vừa viết.

Tên thay đổi, hình dạng thay đổi.

## Các mô hình sản xuất trong tự nhiên

Bàn làm việc tối thiểu tồn tại khi tiếp xúc với monorepos thực sự khi ba mô hình được xếp lớp trên nó.

> Máy làm việc của đại lý là một môi trường nhẹ để thử nghiệm và điều chỉnh hành vi của đại lý. Nó cung cấp không gian thực hiện tách biệt và các công cụ phân tích quỹ đạo chi tiết.

**Nested `AGENTS.md` with nearest-wins precedence.**Các tàu OpenAI 88 `AGENTS.md`Các tập tin trên repo chính của nó, một trong mỗi thành phần phụ. Codex, Cursor, Claude Code, và Copilot tất cả đi từ tập tin làm việc đến gốc repo và kết nối mỗi `AGENTS.md`Các tập tin phụ thư mục mở rộng tập tin gốc.`AGENTS.override.md`thay vì mở rộng; cơ chế bỏ qua là đặc biệt của Codex và tránh nó cho công việc chéo công cụ.`AGENTS.md`các file cung cấp một bước nhảy chất lượng tương đương với nâng cấp từ Haiku sang Opus; những file tồi tệ nhất làm cho sản xuất tồi tệ hơn không có file nào cả.

**Anti-patterns to refuse, even when they look like coverage.**Các hướng dẫn xung đột lặng lẽ thả chất từ chế độ tương tác sang chế độ tham lam (ICLR 2026 AMBIG-SWE: 48,8% → 28% tỷ lệ giải quyết); số ưu tiên thay vì xếp chúng bằng phẳng. Các quy tắc kiểu không xác minh ("để theo hướng dẫn kiểu Python của Google") mà không có lệnh thực thi cho phép đại lý phát minh ra sự tuân thủ; kết hợp mọi quy tắc kiểu với lệnh lint chính xác. Tiếp tục bằng phong cách thay vì lệnh chôn đi con đường xác minh; lệnh trước, phong cách sau. Viết cho con người thay vì các đại lý lãng phí ngân sách ngữ cảnh; ngắn gọn là một tính năng.

**Cross-tool symlinks.**Một tệp gốc duy nhất với liên kết (`ln -s AGENTS.md CLAUDE.md`- `ln -s AGENTS.md .github/copilot-instructions.md`- `ln -s AGENTS.md .cursorrules`) giữ cho mọi nhân viên lập trình trên cùng một nguồn sự thật.`nx ai-setup`tự động hóa điều này qua Claude Code, Cursor, Copilot, Gemini, Codex, và OpenCode từ một cấu hình duy nhất.

## Chuyển nó đi.

`outputs/skill-minimal-workbench.md`tạo ra bàn làm việc ba tập tin cho bất kỳ repo mới: một `AGENTS.md`router được điều chỉnh cho dự án, một `agent_state.json`với các khóa đúng, và một `task_board.json`được gieo trồng với số dư hiện tại.

> Máy làm việc của đại lý là một môi trường nhẹ để thử nghiệm và điều chỉnh hành vi của đại lý. Nó cung cấp không gian thực hiện tách biệt và các công cụ phân tích quỹ đạo chi tiết.

## Tập luyện bài tập

1. Thêm một `last_run`dấu thời gian đến `agent_state.json`- Không chạy nếu tập tin đã có hơn 24 giờ trừ khi một nhà điều hành xác nhận.
  Trung ngữ翻译:思考并实践此练习。
2. Thêm một `priority`trường vào bảng tác vụ và thay đổi kéo để luôn chọn ưu tiên cao nhất `todo`- Tôi không biết.
  Trung ngữ翻译:思考并实践此练习。
3. Di cư`task_board.json`để JSON Lines để mỗi nhiệm vụ là một dòng và các sự khác biệt là sạch trong điều khiển phiên bản.
  Trung ngữ翻译:思考并实践此练习。
4. Hãy viết một `lint_workbench.py`Nếu không,`AGENTS.md`là hơn 80 dòng hoặc tham chiếu một tập tin không tồn tại.
  Trung ngữ翻译:思考并实践此练习。
5. Hãy quyết định là một trong ba tập tin nào sẽ làm tổn thương nhiều nhất nếu mất.
  Trung ngữ翻译:思考并实践此练习。

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| Router | `AGENTS.md` | Short root file that points the agent at deeper docs and files |  |
| State file | "The notes" | Machine-readable record of where the agent is, written every turn |  |
| Task board | "The backlog" | JSON queue of work with status, owner, acceptance |  |
| System of record | "Source of truth" | The file the workbench treats as authoritative when chat is gone |  |

## Xem thêm 延伸阅读

- [agents.md — the open spec](https://agents.md/) được thông qua bởi Cursor, Codex, Claude Code, Copilot, Gemini, OpenCode
  Trung ngữ: 翻译:见原文.
- [Augment Code, A good AGENTS.md is a model upgrade. A bad one is worse than no docs at all](https://www.augmentcode.com/blog/how-to-write-good-agents-dot-md-files) tăng cường chất lượng được đo
  Trung ngữ: 翻译:见原文.
- [Blake Crosley, AGENTS.md Patterns: What Actually Changes Agent Behavior](https://blakecrosley.com/blog/agents-md-patterns) những gì hoạt động theo kinh nghiệm, những gì không
  Trung ngữ: 翻译:见原文.
- [Datadog Frontend, Steering AI Agents in Monorepos with AGENTS.md](https://dev.to/datadog-frontend-dev/steering-ai-agents-in-monorepos-with-agentsmd-13g0) ưu tiên trong thực tế
  Trung ngữ: 翻译:见原文.
- [Nx Blog, Teach Your AI Agent How to Work in a Monorepo](https://nx.dev/blog/nx-ai-agent-skills) Sản xuất nguồn duy nhất trên sáu công cụ
  Trung ngữ: 翻译:见原文.
- [The Prompt Shelf, AGENTS.md Best Practices: Structure, Scope, and Real Examples](https://thepromptshelf.dev/blog/agents-md-best-practices/) mục sắp xếp tồn tại xem xét
  Trung ngữ: 翻译:见原文.
- [Anthropic, Claude Code subagents and session store](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/sub-agents)
  Trung ngữ: 翻译:见原文.
- [Anthropic, Claude Code subagents](https://code.claude.com/docs/en/sub-agents)
- Giai đoạn 14 · 31  các chế độ thất bại tối thiểu này hấp thụ
- Giai đoạn 14 · 34  các kế hoạch trạng thái bền vững bài học này xem trước
