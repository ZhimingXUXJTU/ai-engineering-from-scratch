# Các nghiên cứu trường hợp và tình trạng nghệ thuật năm 2026

> Ba tham chiếu cấp sản xuất để nghiên cứu từ đầu đến cuối, mỗi mô tả một mảnh khác nhau của kỹ thuật đa đại lý. **Anthropic's Research system**(nhà nhạc công, 15x token, +90.2% so với đơn đại lý Opus 4, rainbow triển khai) là trường hợp giám sát giáo. **MetaGPT / ChatDev**(SOP mã hóa chuyên môn vai trò cho kỹ thuật phần mềm; "dehallucination truyền thông" của ChatDev; MacNet mở rộng đến > 1000 đại lý thông qua DAGs, arXiv:2406.07155) là trường hợp phân hủy vai trò theo luật. **OpenClaw / Moltbook**(trước đây là Clawdbot của Peter Steinberger, tháng 11 năm 2025; đổi tên hai lần; 247k sao GitHub vào tháng 3 năm 2026; các đại lý ReAct-loop địa phương; Moltbook như một mạng xã hội chỉ có đại lý với ~ 2.3M tài khoản đại lý trong vài ngày sau khi ra mắt, được Meta mua lại 2026-03-10) minh họa những gì xảy ra ở quy mô dân số: hoạt động kinh tế mới nổi, rủi ro tiêm nhanh, quy định cấp nhà nước (Trung Quốc hạn chế OpenClaw trên máy tính của chính phủ, tháng 3 năm 2026).**Framework landscape April 2026:**LangGraph và CrewAI dẫn đầu sản xuất; AG2 là sự tiếp tục của AutoGen cộng đồng; Microsoft AutoGen đang trong chế độ bảo trì (đã hợp nhất vào Microsoft Agent Framework, RC Feb 2026); OpenAI Agents SDK là người kế nhiệm sản xuất Swarm; Google ADK ( Tháng Tư 2025) là người tham gia A2A bản địa. Mỗi khung lớn hiện nay cung cấp hỗ trợ MCP; hầu hết tàu A2A. Bài học này đọc từng trường hợp từ đầu đến cuối và phân tích các mô hình phổ biến để bạn có thể chọn đúng tham chiếu cho hệ thống sản xuất tiếp theo của bạn.

> **【中文解读】**Bài viết này giới thiệu các phân tích của hệ thống SOTA đa đại lý  trường hợp nghiên cứu  mới nhất 系统 系统 最佳多 đại lý 系统 

> **【拓展：case studies 2026 sota→具体应用】**2026 năm SOTA 多 Agent 系统案例:(1) Claude Research 多 Agent của nhân chủng học 协作进行深度研究;(2) OpenAI  Codex 多 Agent 协作编码;(3) Microsoft  AutoGen 团队 多 Agent 软件开发──共同趋势:专业化分工、层化编排、MCP 工具使用和A2A Agent 间通信的结合──


**Type:** Learn (capstone) | **类型:** 学习（顶点）
**Languages:** — | **语言:** —
**Prerequisites:** all of Phase 16 (Lessons 01-24) | **前置知识:** Phase 16 全部（第 01-24 课）

>  **【前置】**本节是阶段 16 收官课,整合 01-24 所有内容──三个生产级案例:Anthropic Research (Phương pháp nghiên cứu nhân tạo) MetaGPT/ChatDev (Phương pháp nghiên cứu nhân tạo) OpenClaw (Moltbook) 群体规模涌现典范) 
>  **【类比】**三个案例 = "三种规模多代理社会"――Anthropic Research = 精小队(10 个代理,深度研究);MetaGPT = 标准开发团队(角色分工,SOP 编码);OpenClaw/Moltbook = 城市级社会(百万代理 涌现经济、被政府监管) ――2026 框架格局:LangGraph + CrewAI 领跑生产、AG2 接 AutoGen Microsoft AutoGen 合并、Open Agents SDK 是 Swarm 生产版、Google ADK 是 A2A 原生──
**Time:** ~90 minutes | **时间:** ~90 分钟

##                                                                                                                                                                                                                                                               

Kỹ thuật đa đại lý là một ngành học trẻ. Các tham chiếu sản xuất là ít, và mỗi người bao gồm một phần khác nhau của không gian. Đọc chúng một lần là hữu ích; so sánh chúng như một tập hợp là hữu ích hơn. Bài học này xử lý ba nghiên cứu trường hợp theo luật 2026 như một danh sách đọc từ đầu đến cuối, ghi lại các mô hình phổ biến, và lập bản đồ khung cảnh để bạn có thể lựa chọn khung dựa trên kiến thức, chứ không phải tiếp thị.

> Nhiều đại lý 工程 là một ngành học trẻ. Việc sản xuất tham khảo rất ít, mỗi phần khác nhau của không gian bao gồm.

## Khái niệm cốt lõi

### Hệ thống Nghiên cứu Nhân chủng

Trường hợp người giám sát sản xuất: Claude Opus 4 lập kế hoạch và tổng hợp; Claude Sonnet 4 nghiên cứu phụ song.https://www.anthropic.com/engineering/multi-agent-research-system.

Kết quả đo lường chính:

> 关键测量结果:

- **+90.2%**cải thiện so với đơn tác nhân Opus 4 về các đánh giá nghiên cứu nội bộ.
  Trung文翻译: 在内部研究评估上比单 Agent Opus 4 提升 **+90.2%**
- **80% of BrowseComp variance**được giải thích bởi **token usage alone** Multi-agent thắng phần lớn bởi vì mỗi subagent nhận được một cửa sổ bối cảnh mới.
  Trung ngữ翻译:**80% 的 BrowseComp 方差**Chỉ bởi**token 使用量**解释多 Agent 胜出主要因为每个子 Agent 获得新的上下文窗口──
- **15x tokens per query**Vâng, tôi không có gì khác.
  Trung ngữ翻译:每查询 **15 倍 token**Vâng, tôi không muốn làm việc với anh.
- **Rainbow deployment**Bởi vì các đại lý là người lâu dài và có quyền lực.
  Trung ngữ翻译:**彩虹部署**Bởi vì đại lý là một người hoạt động lâu dài và có tình trạng.

Các bài học thiết kế được hợp pháp hóa:

> 编码化的设计训练:

1. **Scale effort to query complexity.**Simple → 1 đại lý với 3-10 công cụ gọi trung bình → 3 đại lý nghiên cứu phức tạp → 10+ phụ gia.
   Trung ngữ翻译:**按查询复杂度扩展工作量。**简单 → 1 个代理 3-10 次工具调用──中等 → 3 个代理──复杂研究 → 10+ 子代理──
2. **Broad first, then narrow.**Các subagent làm tìm kiếm rộng; tổng hợp chì; các subagent theo dõi làm các chiều sâu nhắm mục tiêu.
   Trung ngữ翻译:**先广后窄。** Agent làm tìm kiếm rộng rãi; Main Agent 综合;后续子 Agent做定向深挖──
3. **Rainbow deploys.**Giữ phiên bản chạy thời gian cũ còn sống cho đến khi các nhân viên trên chuyến bay của họ kết thúc.
   Trung ngữ翻译:**彩虹部署。**保持旧运行时版本活跃直到进行中的代理完成──
4. **Verification is not optional.**Hệ thống được quan sát thấy ảo giác mà không có vai trò xác minh rõ ràng.
   Trung ngữ翻译:**验证不是可选的。**Hệ thống được quan sát khi không có vai trò chứng minh rõ ràng được phát sinh ảo giác.

Đây là trường hợp tham chiếu cho topology người giám sát-người làm việc (Phase 16 · 05) trên quy mô sản xuất.

### MetaGPT / ChatDev

Vụ SOP-role-decomposition case sản xuất. bao gồm arXiv:2308.00352 (MetaGPT) và arXiv:2307.07924 (ChatDev).

MetaGPT mã hóa các SOP kỹ thuật phần mềm như các lời nhắc vai trò: Giám đốc sản phẩm, kiến trúc sư, quản lý dự án, kỹ sư, kỹ sư QA.`Code = SOP(Team)`Mỗi vai trò có một đơn giản đơn giản, chuyên môn; giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao giao

Tham gia của ChatDev: **communicative dehallucination**. Các đại lý yêu cầu các thông tin cụ thể trước khi trả lời  một đại lý thiết kế hỏi lập trình viên ngôn ngữ nào được dự định trước khi phác thảo UI, thay vì đoán.

MacNet (arXiv:2406.07155) mở rộng ChatDev đến **>1000 agents via DAGs**Mỗi nút DAG là một chuyên môn vai trò; cạnh mã hóa các hợp đồng giao dịch. Skala là có thể bởi vì định tuyến là rõ ràng và có thể tính ngoại tuyến.

Bài học thiết kế:

> 设计教训:

1. **Structure matters more than size.**Một đội SOP 5 vai chặt chẽ đánh bại một nhóm không cấu trúc 50 nhân viên.
   Trung ngữ翻译:**结构比规模更重要。**5 nhân vật của SOP 团队 thắng hơn 50 người trong nhóm không cấu trúc của Agent.
2. **Handoff contracts in writing.**Các đồ tạo vật được chuyển qua giữa các vai diễn theo một kế hoạch.
   Trung ngữ翻译:**书面交接契约。**角色间传递的制品遵循模式──
3. **Communicative dehallucination**là một mô hình rẻ tiền, chịu tải.
   Trung ngữ翻译:**交际去幻觉**Đó là một mô hình rẻ tiền, chịu nặng.
4. **DAGs scale further than chat.**Khi dòng chảy được biết, mã hóa nó.
   Trung ngữ翻译:**DAG 比聊天扩展更远。**Khi quá trình được biết, hãy mã nó.

Đây là trường hợp tham chiếu cho chuyên môn vai trò (Phase 16 · 08) và topology có cấu trúc (Phase 16 · 15).

### Hệ sinh thái OpenClaw / Moltbook

Trường hợp quy mô dân số sản xuất.

- **Nov 2025:**Tàu Clawdbot (truyện viên mã hóa vòng ReAct của Peter Steinberger)
- **Dec 2025 – Mar 2026:**đổi tên hai lần (Clawdbot → OpenClaw → tiếp tục dưới OpenClaw).
- **Feb 2026:**Moltbook ra mắt như một mạng xã hội chỉ dành cho các đại lý trên cùng một nguyên thủy; ~ 2.3M tài khoản đại lý trong vài ngày.
- **Mar 2026 (2026-03-10):**Meta mua lại Moltbook.
- **Mar 2026:**Trung Quốc hạn chế OpenClaw trên máy tính của chính phủ.
- **Mar 2026:**OpenClaw vượt qua 247k sao GitHub.

Đây là cái gì đa đại lý trông như khi bạn đặt hàng triệu đại lý trên một phân nhựa chia sẻ:

- **Emergent economic activity.**Các đại lý mua, bán và phục vụ lẫn nhau bằng cách trả tiền bằng token.
- **Prompt-injection risks at population scale.**Một lời nhắc độc hại trong hồ sơ của một đại lý virus lan truyền đến hàng ngàn tương tác giữa đại lý và đại lý trong vài giờ.
- **State-level regulatory response.**Trong vòng vài tuần sau khi ra mắt, quy định đã đến hệ sinh thái.

Những bài học về thiết kế từ trường hợp này là một phần kỹ thuật, một phần quản lý:

1. **Multi-agent at population scale is a new regime.**Các thực hành tốt nhất của hệ thống cá nhân (sự xác minh, rõ ràng về vai trò) vẫn áp dụng nhưng không đủ.
2. **Prompt injection is the new XSS.**Chế độ thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin
3. **Regulation is faster than design cycles.**Hãy lên kế hoạch.
4. **Open-source + viral scale compounds.**247k ngôi sao trong ~ 4 tháng là bất thường; thiết kế cho triển khai-bùng nổ-thực lượng.

Nhìn xem[OpenClaw Wikipedia](https://en.wikipedia.org/wiki/OpenClaw)Các bản tin về các hệ thống sinh thái được công bố bởi CNBC / Palo Alto Networks. Đối với các cơ sở kỹ thuật, các kho lưu trữ Clawdbot / OpenClaw phơi bày vòng lặp ReAct địa phương; các bài đăng công khai của Moltbook tiết lộ kiến trúc đồ thị xã hội ở trên.

### Quang khung cảnh tháng 4 năm 2026

| Framework | Status | Best for | Notes |
|---|---|---|---|
| **LangGraph** (LangChain) | Production leader | structured graph + checkpointing + human-in-the-loop | recommended default for production |
| **CrewAI** | Production leader | role-based crews with Sequential/Hierarchical processes | strong for role decomposition |
| **AG2** | Community maintained | GroupChat + speaker selection | AutoGen v0.2 continuation |
| **Microsoft AutoGen** | Maintenance mode (Feb 2026) | — | merged into Microsoft Agent Framework RC |
| **Microsoft Agent Framework** | RC (Feb 2026) | orchestration patterns + enterprise integration | new entrant; watch |
| **OpenAI Agents SDK** | Production | Swarm successor | tool-return handoff pattern |
| **Google ADK** | Production (April 2025) | A2A-native | Google Cloud integration |
| **Anthropic Claude Agent SDK** | Production | single-agent + Research extension | see the Research system post |

Mọi khung hình lớn đều được đưa ra.**MCP**hỗ trợ; hầu hết tàu **A2A**Sự tương thích của giao thức không còn là một sự khác biệt nữa.

### Các mô hình chung trong cả ba trường hợp

1. **Orchestrator + workers**(Giám sát nhân rõ ràng, MetaGPT PM-as-supervisor, các đại lý cá nhân OpenClaw + hiệu ứng mạng).
   Trung ngữ翻译:**编排者 + 工作者**(Anthropic 显式监督者,MetaGPT PM 作监督者,OpenClaw 独立代理 + 网络效应)
2. **Structured handoff contracts**(Thông tả nhiệm vụ của bộ phận nhân tạo, tài liệu PRD/kiến trúc MetaGPT, các vật thể OpenClaw A2A).
   Trung ngữ翻译:**结构化交接契约**(Anthropic 子 Agent 任务描述,MetaGPT PRD/架构文档,OpenClaw A2A 制品)
3. **Verification as first-class role**(Điểm tra viên của Anthropic, Kỹ sư QA của MetaGPT, các xác thực viên trong mạng của OpenClaw).
   Trung ngữ翻译:**验证作为一等角色**(Anthropic 的验证器,MetaGPT 的 QA 工程师,OpenClaw 的网络内验证器)
4. **Scaling is topology + substrate, not just more agents**(các hoạt động của cầu vồng, các DAG MacNet, các phụ phân dân số).
   Trung ngữ翻译:**扩展是拓扑 + 基底，不仅是更多 Agent**(彩虹部署, MacNet DAG,群体规模基底)
5. **Cost is material and disclosed**(15x token, ngân sách cho mỗi vai trò trong MetaGPT, giá cho mỗi tương tác trong Moltbook).
   Trung ngữ翻译:**成本是实质性的且已披露**(Tương tự: 15 lần,Bản mục: MetaGPT 中每角色预算,Moltbook 中每次交互定价)
6. **Security posture is explicit**(Anthropic sandboxing, MetaGPT hạn chế vai trò, OpenClaw nhanh chóng tiêm như diện tích tấn công được biết đến).
   Trung ngữ翻译:**安全态势是显式的**(Anthropic 的沙盒,MetaGPT 的角色限制,OpenClaw 的提示注入作为已知攻击面)

### Chọn tài liệu tham khảo cho dự án tiếp theo của bạn

- **Production research / knowledge task → Anthropic Research.**Những người phụ thuộc vào bối cảnh mới thắng.
- **Engineering / tool-chain workflow → MetaGPT / ChatDev.**Vai trò + SOP + hợp đồng giao tiếp.
- **Network-effect social product → OpenClaw / Moltbook.**Substrate + nền kinh tế mới nổi.
- **Classic enterprise automation → CrewAI or LangGraph**(Đạo lực sản xuất, thời gian chạy ổn định).

### Tổng kết hiện đại năm 2026

Ở đâu là cánh đồng vào tháng 4 năm 2026:

- **Frameworks are converging.**MCP + A2A hỗ trợ là bàn cược. Handoff ngữ nghĩa là lựa chọn thiết kế còn lại.
- **Evaluation is hardening.**SWE-bench Pro, MARBLE, STRATUS là chuẩn mực giảm thiểu.
- **Production failure rates are measurable**(Cemri 2025 MAST; 41-86,7% trên MAS thực).
- **Cost is the central engineering constraint.**Chi phí token mỗi nhiệm vụ, đồng hồ tường mỗi tương tác, cung điện triển khai trênhead. Multi-agent thắng trên độ chính xác nhưng mất trên chi phí  và giao dịch đó là quyết định kinh doanh.
- **Regulation is a near-term input, not a background concern.**Các khu vực pháp lý đang di chuyển nhanh hơn các chu kỳ triển khai cá nhân.

## Sử dụng nó.
```figure
a5-orchestrator-scale
```

## Sử dụng nó

`outputs/skill-case-study-mapper.md`là một kỹ năng đọc một thiết kế hệ thống đa đại lý được đề xuất và lập bản đồ cho nghiên cứu trường hợp gần nhất, làm nổi lên các quyết định thiết kế mà nghiên cứu trường hợp đã thử nghiệm.

## Đưa nó lên mạng

Quy tắc khởi động cho sản xuất đa đại lý vào năm 2026:

- **Start from a case study, not from scratch.**Chọn một trong những nghiên cứu gần nhất của Anthropic Research / MetaGPT / OpenClaw và thích nghi.
  Trung ngữ翻译:**从案例研究开始，不是从零开始。**选择最接近的人类研究 / MetaGPT / OpenClaw 并适配──
- **Adopt MCP + A2A.**Sự di động giữa các khung là có giá trị; hỗ trợ giao thức là miễn phí.
  Trung ngữ翻译:**采用 MCP + A2A。**跨框架的可移植性有价值;协议支持是免费的.
- **Measure against SWE-bench Pro or your internal Pro-equivalent.**Được xác minh là bị nhiễm trùng.
  Trung ngữ翻译:**用 SWE-bench Pro 或你的内部 Pro 等效物衡量。**Được xác minh đã bị nhiễm trùng.
- **Pay the verification tax.**Một kiểm chứng độc lập chi phí ~ 20-30% ngân sách token của bạn và mua độ chính xác có thể đo lường.
  Trung ngữ翻译:**支付验证税。**独立验证器花费约 20-30% của token 预算, đổi lấy tính chính xác của phép đo.
- **Rainbow deploy long-running agents.**Hi vọng các hoạt động của đại lý sẽ là thói quen.
  Trung ngữ翻译:**彩虹部署长时间运行 Agent。**预期多小时 Agent 运行是常规──
- **Read WMAC 2026 and the MAST follow-ups.**Sự kỷ luật đang tiến triển nhanh chóng.
  Trung ngữ翻译:**阅读 WMAC 2026 和 MAST 后续。**Học tập này đang phát triển nhanh chóng.

## Tập luyện bài tập

1. Đọc hệ thống nghiên cứu nhân học từ đầu đến cuối. Xác định ba quyết định thiết kế sẽ thay đổi nếu bạn thay thế Opus 4 bằng một mô hình nhỏ hơn (ví dụ: Haiku 4).
2. Đọc MetaGPT Phần 3-4 (arXiv:2308.00352). Mã hóa một SOP từ miền của riêng bạn (không phải phần mềm) như các lời nhắc vai trò.
3. Đọc ChatDev (arXiv:2307.07924). xác định cơ chế của "sự giải ảo thông tin". Thực hiện nó trong một trong các hệ thống đa tác nhân hiện tại của bạn.
4. Hãy đọc về OpenClaw và Moltbook. Chọn một chế độ thất bại cụ thể xuất hiện trên quy mô dân số mà không xuất hiện trong một hệ thống 5 đại lý.
5. Chọn dự án đa đại lý hiện tại của bạn. Trong ba nghiên cứu trường hợp nào là tham chiếu gần nhất? Những quyết định thiết kế nào từ nghiên cứu trường hợp đó bạn chưa chấp nhận? Viết ra một bạn sẽ chấp nhận quý này.

## Từ khóa  Keyword

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Anthropic Research / Anthropic 研究 | "The supervisor reference" / "监督者参考" | Claude Opus 4 + Sonnet 4 subagents; 15x tokens; +90.2% over single-agent. / Claude Opus 4 + Sonnet 4 子 Agent；15 倍 token；比单 Agent +90.2%。 |
| MetaGPT | "SOP as prompts" / "SOP 作为提示" | Role decomposition for software engineering; `Code = SOP(Team)`. / 软件工程的角色分解；`Code = SOP(Team)`。 |
| ChatDev | "Agents as roles" / "Agent 作为角色" | Designer / programmer / reviewer / tester; communicative dehallucination. / 设计师/程序员/审阅者/测试者；交际去幻觉。 |
| MacNet | "Scale ChatDev via DAG" / "通过 DAG 扩展 ChatDev" | arXiv:2406.07155; 1000+ agents via explicit DAG routing. / arXiv:2406.07155；通过显式 DAG 路由实现 1000+ Agent。 |
| OpenClaw | "Local ReAct-loop agents" / "本地 ReAct 循环 Agent" | Steinberger's project; 247k stars by March 2026. / Steinberger 的项目；2026 年 3 月 247k 星。 |
| Moltbook | "Agent-only social network" / "Agent 专用社交网络" | 2.3M agent accounts; acquired by Meta March 2026. / 230 万 Agent 账户；2026 年 3 月被 Meta 收购。 |
| Rainbow deploy / 彩虹部署 | "Multiple versions concurrent" / "多版本并发" | Keep old runtime versions alive for in-flight long-running agents. / 保持旧运行时版本活跃以支持进行中的长时间 Agent。 |
| Communicative dehallucination / 交际去幻觉 | "Ask before answering" / "先问后答" | Agents request specifics from peers instead of guessing. / Agent 从同伴请求具体信息而非猜测。 |
| WMAC 2026 | "The AAAI workshop" / "AAAI 研讨会" | April 2026 community focal point for multi-agent coordination. / 2026 年 4 月多 Agent 协调的社区焦点。 |

## Xem thêm 延伸阅读

- [Anthropic — How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) tham chiếu sản xuất của người lao động giám sát
- [MetaGPT — Meta Programming for Multi-Agent Collaborative Framework](https://arxiv.org/abs/2308.00352) Sự phân hủy vai trò SOP
- [ChatDev — Communicative Agents for Software Development](https://arxiv.org/abs/2307.07924) Tự giải ảo giác truyền thông
- [MacNet — scaling role-based agents to 1000+](https://arxiv.org/abs/2406.07155) Skala dựa trên DAG
- [OpenClaw on Wikipedia](https://en.wikipedia.org/wiki/OpenClaw) tổng quan hệ sinh thái
- [WMAC 2026](https://multiagents.org/2026/)Hội thảo Chương trình Cầu AAAI 2026 về Hợp tác đa đại lý
- [LangGraph docs](https://docs.langchain.com/oss/python/langgraph/workflows-agents) Lãnh đạo sản xuất
- [CrewAI docs](https://docs.crewai.com/en/introduction) Quản lý dựa trên vai trò
