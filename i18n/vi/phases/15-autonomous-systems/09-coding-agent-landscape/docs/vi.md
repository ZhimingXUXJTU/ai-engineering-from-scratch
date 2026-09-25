# Các tác nhân tự lập mã hóa Landscape (2026) ➡️

> SWE-bench Verified đã tăng từ 4% lên 80,9% trong vòng chưa đầy ba năm. Cùng Claude Sonnet 4.5 ghi 43,2% trên SWE-agent v1 và 59,8% trên Cline tự động OpenHands (trước đây là OpenDevin) là nền tảng được cấp phép MIT hoạt động nhất và vòng lặp CodeAct của nó thực hiện các hành động Python trực tiếp trong một hộp cát thay vì các cuộc gọi công cụ JSON. Các số tiêu đề che giấu một vấn đề về phương pháp: 161 trong số 500 nhiệm vụ SWE-bench Verified chỉ yêu cầu thay đổi đường dây 12, và SWE-bench Pro (10 nhiệm vụ đường dây) nằm ở mức 2359% cho các mô hình biên giới tương tự.

> **【中文解读】**SWE-bench Verified trong vòng 3 năm tăng từ 4% lên đến 80.9%。 cùng Claude Sonnet 4.5 trên SWE-agent v1 lên tới 43.2%, trên Cline tự trị lên đến 59.8% mô hình xung quanh脚手架架现在和模型本身一样重要。OpenHands(前 OpenDevin) là nền tảng 许可 MIT hoạt động nhất, có CodeAct 循环 trực tiếp thực hiện Python 动作 trong hộp chứ không phải JSON 工具调用。 tiêu đề số liệu ẩn phương pháp học:500 个 SWE-bench Verified 任务中 161 个只需要1-2 行变更,SWE-bench Pro(10+ 行任务) 藏藏前沿模型只有23-59%。

> **【拓展：脚手架 > 模型】**Khúc trình 2022-2026 cho thấy khả năng nâng cao của Codification Agent có ba nguồn phức tạp: mô hình cơ bản tốt hơn, mô hình tay tay tay tay tay tay tay tốt hơn (CodeAct, phản ánh, vòng lặp của máy kiểm chứng)  mô hình tốt hơn (Verified, clear noise)  Các mô hình tương tự khác nhau trên các mô hình tay tay tay tay tay khác nhau có sự khác biệt 16.6 điểm tuyệt đối.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, CodeAct vs JSON tool-call comparison) | **语言:** Python（标准库，CodeAct vs JSON 工具调用对比）
**Prerequisites:** Phase 14 · 07 (Tool use), Phase 15 · 01 (Long-horizon agents) | **前置知识:** Phase 14 · 07（工具使用），Phase 15 · 01（长程 Agent）
**Time:** ~45 minutes | **时间:** ~45 分钟

>  **【前置】**学本节前请先掌握:Phase 14·07(工具调用) 、Phase 14·30+(工作台 实践) 、Phase 15·01(长程 代理) ⋅本节是 2026 年编码 代理 全景图选型必读──
>  **【类比】**选编码 Agent = "选车" thay vì "选发动机"。 cùng một发动机(Claude Sonnet 4.5) được cài đặt trên xe khác nhau(SWE-agent vs Cline) tốc độ khác nhau 16 个百分点。脚手架(检索层、规划器、沙箱、edit-verify 循环) chỉ là sản phẩm, mô hình chỉ là bộ phận。 vì vậy đừng chỉ nhìn vào bảng xếp hạng mô hình, để xem "My task+my脚手架" của cuối đến cuối độ tin cậy。
> ️ **【易错点】**Xem SWE-bench Verified 分数选 Agent = 被基准骗了──500 个任务里 161 个只需要1-2 行修改(容易), xem SWE-bench Pro(10+ 行真实任务) 分数才有参考价值──修复:选 Agent 前用自己代码库的真实问题 测试,而不是看营销基准──

## Vấn đề  vấn đề giới thiệu

> **【中文解读】**编码 Agent 景观 là một trong những lĩnh vực ứng dụng AI thay đổi nhanh nhất trong năm 2025-2026  Các cầu thủ chính bao gồm Claude Code, Cursor, GitHub Copilot, Devin, Windsurf, v.v.

> **【拓展：coding agent landscape】**2026年编码 代理的竞争格局:(1) Claude CodeAnthropic's tự lập编码 代理,支持全开发、Git 操作和终端命令执行;(2) Cursor基于 VS Code的 AI 编辑器,强调人机协作;(3) DevinCognition AI's全自编码 代理,可以独立完成开发任务;(4) Windsurf(原 Codeium) AI 优先 IDE──SWE-bench 上的表现是主要竞争指标.

"Đại diện lập trình nào là tốt nhất" là câu hỏi sai lầm. Câu hỏi đúng là: trên một phân phối nhiệm vụ phù hợp với công việc của tôi, với các giàn khoan tôi sẽ chạy trong sản xuất, tôi có được độ tin cậy cuối đến cuối như thế nào?

> "Cái bộ phận mã hóa nào là tốt nhất" là câu hỏi sai lầm. Câu hỏi chính xác là: Trong phân bố nhiệm vụ phù hợp với công việc của tôi, sử dụng kệ tay tôi sẽ chạy trong sản xuất, tôi có thể đạt được độ tin cậy cuối cùng?

Giữa năm 2022 và 2026, lĩnh vực này đã học được rằng sàn nhà  lớp lấy lại, lập kế hoạch, hộp cát, vòng chỉnh sửa-thêm lại, định dạng phản hồi  chịu tải. Claude Sonnet 4.5 trên SWE-agent v1 đạt điểm 43,2% trên SWE-bench Verified; cùng một mô hình bên trong giàn tay tự động của Cline đạt điểm 59,8%. 16.6 điểm khác biệt tuyệt đối, cùng trọng lượng. Mô hình cơ bản là một thành phần; vòng lặp là sản phẩm.

> 2022 đến 2026 năm, lĩnh vực học đến khung tay  kiểm tra tầng, lập trình viên, hộp 沙 ̊ 编辑-thiết nghiệm vòng lặp  phản hình thức là chịu tải. Claude Sonnet 4.5 trên SWE-agent v1 trên SWE-bench Được xác minh đạt 43,2%; cùng mô hình trong Cline tự động bàn tay  trong 59.8%;; cùng trọng lượng khác nhau 16.6 điểm tuyệt đối;; mô hình cơ bản là bộ phận; vòng lặp là sản phẩm.

> **【中文解读】**Bài này giới thiệu khái niệm và phương pháp thực hiện cốt lõi của AI Agent.

Vấn đề đồng hành là sự bão hòa của chuẩn chứa đựng sự lùi lại.

> Vấn đề kèm theo là sự chuẩn bị và ẩn lại trở lại.

SWE-bench Verified gần như bão hòa, và đuôi dễ làm (161 trong 500 nhiệm vụ đòi hỏi ≤ 2 dòng) kéo điểm số hàng đầu lên. Chất lượng thế giới thực được đo tốt hơn trên các phân phối như SWE-bench Pro (10+ thay đổi dòng), nơi cùng một nhà lãnh đạo vẫn ngồi ở 2359%.

> SWE-bench Verified 接近和,简单任务尾部(500 个任务中 161 个需要 ≤2 行) 拉高顶级分数――现实世界质量在SWE-bench Pro(10+ 行变更)等分布测量更好,同领先者仍只有23-59%──

## Khái niệm cốt lõi

### SWE-bench, một đoạn.

SWE-bench (Jimenez et al.) lấy các vấn đề thực của GitHub với các bản vá thực tại và yêu cầu một đại lý sản xuất một bản vá mà làm cho bộ thử nghiệm vượt qua. SWE-bench Verified (OpenAI, 2024) là một bộ phận 500 nhiệm vụ do con người điều chỉnh với các nhiệm vụ mơ hồ và bị phá vỡ được loại bỏ. SWE-bench Pro là người kế nhiệm khó khăn hơn  các nhiệm vụ đòi hỏi 10 + dòng thay đổi, nơi các đại lý biên giới hiện tại ngồi ở 2359%.

> SWE-bench(Jimenez 等人) lấy thực sự sửa chữa của thực tế GitHub vấn đề, yêu cầu Agent  tạo ra để làm cho các bộ thử nghiệm thông qua sửa chữa.

### Điều gì đường cong 2022 → 2026 thực sự cho thấy 

- **2022**: các mô hình nghiên cứu ở ~ 4% trên sàn SWE thô.
  Trung ngữ翻译:**2022**: nghiên cứu mô hình trong ban đầu SWE lên khoảng 4%
- **2024**: GPT-4 + bàn phẳng kiểu Devin ở ~ 14%; SWE-agent ở ~ 12%.
  Trung ngữ翻译:**2024**:GPT-4 + Devin 式脚手架约 14%;SWE-agent 约 12%──
- **2025**Claude 3.5/3.7 Sonnet bên trong Aider và SWE-được đẩy vào phạm vi 4055%.
  Trung ngữ翻译:**2025**:Claude 3.5/3.7 Sonnet 在 Aider 和 SWE-agent 内推进 40-55% 范围──
- **2026**Claude Sonnet 4.5 và các đối thủ cạnh tranh biên giới ở mức 7080%+ trên SWE-bench Verified.
  Trung ngữ翻译:**2026**Claude Sonnet 4.5 和前沿竞争者在SWE-bench Verified 上 70-80%+──Epoch AI 的排行榜实时跟踪──

Sự nghiêng đến từ ba nguồn hợp chất: mô hình cơ sở tốt hơn, sàn nhà tốt hơn (CodeAct, phản xạ, vòng xác minh), và điểm tham khảo tốt hơn (Tài minh loại bỏ tiếng ồn).

> 斜率来自三个复合源: Better基础模型、更好的脚手架(CodeAct、反思、验证器循环)、更好的基准(Verified 去除噪音)。

### CodeAct vs JSON công cụ gọi .

OpenHands (All-Hands-AI, arXiv:2407.16741, trước đây là OpenDevin) đã đặt cược kiến trúc cụ thể: thay vì mô hình phát ra các cuộc gọi công cụ JSON mà một máy chủ giải mã và thực hiện, mô hình phát ra mã Python và một hạt nhân kiểu Jupyter chạy nó trong một hộp cát.

> OpenHands(All-Hands-AI,arXiv:2407.16741,前 OpenDevin) theo cấu trúc cụ thể: mô hình không còn được phát hành bởi nhà máy giải mã thực hiện JSON 工具调用, mà phát hành Python 代码, được vận hành bởi Jupyter 风格内核在沙箱中.

Sự đổi mới:

> 权衡:

- **JSON tool calls**: mỗi hành động là một lượt; dễ kiểm tra; tính kết hợp hạn chế; an toàn theo mặc định vì mỗi cuộc gọi đi qua một xác thực viên rõ ràng.
  Trung ngữ翻译:**JSON 工具调用**Mỗi động tác một vòng; dễ kiểm toán;组合性有限;默认安全因为每次调用经过显式验证器──
- **CodeAct**: một hành động có thể là một chương trình toàn bộ; kết hợp; yêu cầu một hộp cát cứng (OpenHands sử dụng cách ly Docker); chế độ thất bại bao gồm bất cứ điều gì thời gian chạy sandbox cho phép.
  Trung ngữ翻译:**CodeAct**Một động tác có thể là toàn bộ quy trình; có thể được kết hợp; cần phải được cố định hộp thư; không thể làm được bất cứ điều gì được phép.

Cả hai kiến trúc đều đang được sản xuất. CodeAct chiếm ưu thế trong các nền tảng mở (OpenHands, smolagents). Các cuộc gọi công cụ JSON vẫn chiếm ưu thế trong các dịch vụ được quản lý (Anthropic Managed Agents, OpenAI Assistants) nơi nhà cung cấp kiểm soát người thực hiện.

> 两种架构都在生产中.CodeAct 在开放平台(OpenHands、smolagents) 主导.

### Những bàn phím trong khung cảnh năm 2026

| Scaffold | License | Execution model | Notable property |
|---|---|---|---|
| 脚手架 | 许可 | 执行模型 | 显著属性 |
| OpenHands (OpenDevin) | MIT | CodeAct in Docker | Most active open platform; event-stream replayable |
| OpenHands（OpenDevin） | MIT | Docker 中 CodeAct | 最活跃开放平台；事件流可重放 |
| SWE-agent | MIT | Agent-Computer Interface (ACI) | First end-to-end SWE-bench scaffold |
| SWE-agent | MIT | Agent-计算机接口（ACI） | 首个端到端 SWE-bench 脚手架 |
| Aider | Apache-2 | edit-via-diff in local repo | Minimal scaffold, strong regression stability |
| Aider | Apache-2 | 本地仓库 edit-via-diff | 最小脚手架，强回归稳定性 |
| Cline | Apache-2 | VS Code agent with tool policy | Highest-scoring open scaffold on Sonnet 4.5 |
| Cline | Apache-2 | 带工具策略的 VS Code Agent | Sonnet 4.5 上得分最高的开放脚手架 |
| Devin (Cognition) | Proprietary | Managed VM + planner | First "AI software engineer" product category |
| Devin（Cognition） | 专有 | 管理 VM + 规划器 | 首个"AI 软件工程师"产品类别 |
| Claude Code | Proprietary | Permission modes + routines | Lesson 10 covers the agent loop in detail |
| Claude Code | 专有 | 权限模式 + 例程 | 第 10 课详细介绍 Agent 循环 |

### Tại sao bàn phẳng thống trị vì sao bàn phế quản

Một đường chạy mã hóa là một quỹ đạo đường chân trời dài (Học 1).

> 编码运行是长程轨迹 (第 1 课) ⋅可靠性跨步骤复合 (编码运行是长程轨迹) ⋅可靠性跨步骤复合 (编码运行是长程轨迹) ⋅可靠性跨步骤复合 (编码运行是长程轨迹) ⋅可靠性跨步骤复合 (编码运行是长程轨迹) ⋅可靠性跨步骤复合 (编码运行是长程轨迹) ⋅可靠性跨步骤复合 (编码运行是长程轨迹) ⋅可靠性跨步骤复合 (编码架买入分数的三个地方:

1. **Retrieval**Tìm ra các tệp thích hợp để đọc là nút thắt kín. ACI của SWE-agent, chỉ mục tệp của OpenHands và repo-map của Aider tất cả tấn công điều này.
   Trung ngữ翻译:**检索**Tìm thấy những tài liệu chính xác cần đọc là một cái hộp lặng.
2. **Verifier loop**: chạy thử nghiệm, đọc dấu vết hàng, và thử lại là một điểm delta 10+ trên ghế SWE.
   Trung ngữ翻译:**验证器循环**:运行测试、读堆跟踪、重试在SWE-bench 上是10+ điểm tăng量──
3. **Failure containment**Một mô hình với và không có vòng xác minh trông giống như hai sản phẩm khác nhau.
   Trung ngữ翻译:**失败遏制**: error time rolling of sandbox preventing complex damage。 mô hình có và không có chứng minh vòng quay trông giống như hai sản phẩm khác nhau。

### Định nghĩa độ bão hòa và phân phối thực sự.

Các tác giả OpenHands và Epoch AI đều chỉ ra rằng SWE-bench Verified có một đuôi dễ dàng: 161 trong 500 nhiệm vụ chỉ cần 12 dòng thay đổi. Điểm cao được thúc đẩy một phần bởi đuôi này. SWE-bench Pro hạn chế cho 10 + thay đổi dòng và trả lại điểm trong phạm vi 2359% ngay cả cho các hệ thống biên giới. Phân phối sản xuất của bạn gần như chắc chắn gần hơn với Pro hơn với Verified.

> OpenHands tác giả và Epoch AI đều đánh dấu SWE-bench Verified có đơn giản尾部:500 个任务中 161 个 个 chỉ cần 1-2 行变更。高分部分由该尾部驱动。SWE-bench Pro 限制 10+ 行变更, ngay cả trước沿系统也返回 23-59% 范围──你的生产分布几乎肯定更接近Pro而非 Verified。

Sự liên quan để lựa chọn một đại lý: chạy một bộ phận giống Pro của bản bug của riêng bạn. Điểm quan trọng là điểm trên các nhiệm vụ đại diện cho những gì bạn gửi.

> 选择 Agent 的含义: Trong bản thân bạn 积压 trên chạy Pro 类子集── quan trọng分数 là đại diện cho bạn phát hành nhiệm vụ──

## Hãy sử dụng nó để thực hiện
```figure
a5-scaffold-delta
```

## Sử dụng nó

`code/main.py`so sánh hai bàn phẳng đại lý đồ chơi trên phân phối mini-cách cố định:

> `code/main.py`Trong phân bố nhiệm vụ nhỏ cố định so sánh hai đồ chơi Agent 脚手架:

1. A **JSON tool-call**một cái bàn phế liệu có thể thực hiện một hành động mỗi lần.
   Trung ngữ翻译:**JSON 工具调用**脚手架, mỗi vòng một động tác.
2. A **CodeAct**một cái bàn phẳng có thể phát ra một đoạn Python nhỏ mỗi hành động.
   Trung ngữ翻译:**CodeAct**脚手架, mỗi động tác có thể phát hành nhỏ Python 代码片段──

Cả hai đều sử dụng một "chương tự" (quyền định nghĩa) để so sánh tách ra sàn nhà từ chất lượng mô hình.

> 两者使用存根模型 (定性规则) để so sánh các khung tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay tay

## Chuyển nó đi.

`outputs/skill-scaffold-audit.md`giúp bạn kiểm tra một sàn dự kiến của các bộ phận lập trình trước khi được chấp nhận: chất lượng thu thập, sự hiện diện của các xác minh viên, cách ly hộp cát và phù hợp với phân phối điểm chuẩn.

> `outputs/skill-scaffold-audit.md` giúp bạn trong việc sử dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng dụng Ứng

## Tập luyện bài tập

1. Đi chạy`code/main.py`Mỗi bàn gác có bao nhiêu lượt đi trong cùng một tập nhiệm vụ?
   Trung ngữ翻译:运行 `code/main.py`Mỗi tay tay tay trong cùng một tập nhiệm vụ bao nhiêu vòng?

2. Đọc bài báo OpenHands (arXiv:2407.16741). Bài báo cho rằng CodeAct vượt qua các cuộc gọi công cụ JSON trong các nhiệm vụ phức tạp.
   Trung ngữ翻译:阅读 OpenHands 论文(arXiv:2407.16741)。论文论证 CodeAct 在复杂任务上胜胜 JSON 工具调用。识别论文承认一个失败模式并写一句该模式在生产中何时主导。

3. Chọn một nhiệm vụ từ backlog lỗi của bạn mà sẽ yêu cầu 10 + dòng thay đổi trên hai tệp. ước tính xác suất thành công kết thúc đến kết thúc cho một mô hình biên giới dưới (a) JSON tool calls và (b) CodeAct. Định lý khoảng cách.
   Từ 积压中选一个需要跨两文件 10+ 行变更的任务──估算前沿模型在 (a) JSON 工具调用和 (b) CodeAct 下的端到端成功概率──论证差距──

4. SWE-bench Verified có 161 task đơn, 12 dòng.
   Trung ngữ翻译:SWE-bench Verified có 161 个单文件 1-2 行任务――构建排除它们的分数――排行榜如何重排?

5. Đọc "Tạo SWE-bench Verified" (OpenAI). Giải thích phương pháp cụ thể được sử dụng để loại bỏ các nhiệm vụ mơ hồ, và đặt tên một danh mục mà người quản lý sẽ bỏ lỡ.
   Trung文翻译:阅读"Tạo SWE-bench Verified" (OpenAI) ⋅ giải thích dùng để loại bỏ các nhiệm vụ khó khăn cụ thể,命名策划会遗漏的一个类别.

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| SWE-bench | "Coding benchmark" | Real GitHub issues with ground-truth patches and test suites |
| SWE-bench | "编码基准" | 带真实补丁和测试套件的真实 GitHub issue |
| SWE-bench Verified | "Cleaned subset" | 500 human-curated tasks, easier-tail present |
| SWE-bench Verified | "清理的子集" | 500 个手工策划任务，存在简单尾部 |
| SWE-bench Pro | "Harder subset" | 10+ line changes; frontier sits at 23–59% |
| SWE-bench Pro | "更难的子集" | 10+ 行变更；前沿在 23-59% |
| CodeAct | "Code-as-action" | Agent emits Python; Jupyter-style kernel executes in sandbox |
| CodeAct | "代码即动作" | Agent 发出 Python；Jupyter 风格内核在沙箱执行 |
| JSON tool call | "Function calling" | Each action is a structured JSON payload validated before execution |
| JSON 工具调用 | "函数调用" | 每动作是执行前验证的结构化 JSON 负载 |
| Scaffold | "Agent framework" | Retrieval + planner + executor + verifier loop around the base model |
| 脚手架 | "Agent 框架" | 围绕基础模型的检索 + 规划器 + 执行器 + 验证器循环 |
| ACI (Agent-Computer Interface) | "SWE-agent's format" | Command set designed for LLM ergonomics, not human shells |
| ACI（Agent-计算机接口） | "SWE-agent 格式" | 为 LLM 人体工程学设计的命令集，非人类 shell |
| Verifier loop | "Test-and-retry" | Run tests, read output, revise patch; biggest non-model reliability gain |
| 验证器循环 | "测试并重试" | 运行测试、读输出、修订补丁；最大非模型可靠性增益 |

## Xem thêm 延伸阅读

- [Jimenez et al. — SWE-bench](https://www.swebench.com/) chỉ số chuẩn và phương pháp ban đầu.
  Trung ngữ翻译:原始基准和方法论。
- [OpenAI — Introducing SWE-bench Verified](https://openai.com/index/introducing-swe-bench-verified/) cách xây dựng bộ phụ được sắp xếp.
  Trung文翻译:策划子集如何构建──
- [Wang et al. — OpenHands: An Open Platform for AI Software Developers](https://arxiv.org/abs/2407.16741) Kiến trúc CodeAct và thiết kế dòng sự kiện.
  Trung ngữ翻译:CodeAct 架构和事件流设计。
- [Epoch AI — SWE-bench leaderboard](https://epoch.ai/benchmarks) Điểm số được theo dõi trực tiếp.
  Trung ngữ翻译:实时跟踪分数──
- [Anthropic — Measuring agent autonomy](https://www.anthropic.com/research/measuring-agent-autonomy) khung độ tin cậy của các tác nhân mã hóa đường chân trời dài.
  Trung ngữ翻译:长程编码 Agent 可靠性框架──
