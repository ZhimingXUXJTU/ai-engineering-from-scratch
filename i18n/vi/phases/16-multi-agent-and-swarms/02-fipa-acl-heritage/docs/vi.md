# Di sản của FIPA-ACL và các luật ngôn ngữ .

> Trước khi MCP, trước khi A2A, có FIPA-ACL. Năm 2000, IEEE Foundation for Intelligent Physical Agents đã phê chuẩn một ngôn ngữ giao tiếp đại lý với hai mươi biểu diễn, hai ngôn ngữ nội dung và một bộ giao thức tương tác  hợp đồng net, đăng ký/ thông báo, yêu cầu khi nào. Nó đã biến mất khỏi ngành công nghiệp vì chi phí trên của ontology quá nặng cho web, nhưng sự hồi sinh LLM của các hệ thống đa đại lý đang lặng lẽ triển khai lại những ý tưởng tương tự mà không có ngữ nghĩa chính thức: Hợp đồng JSON đứng vào chỗ các biểu hiện, ngôn ngữ tự nhiên đứng vào chỗ các ontology. Bài học này đọc nghiêm túc FIPA-ACL để bạn có thể thấy những quyết định giao thức 2026 là tái phát minh, những gì là sự mới mẻ, và nơi sóng hiện tại sẽ khám phá lại các vấn đề mà những năm 2000 đã giải quyết.

> **【中文解读】**Trong bài học này, các nhà nghiên cứu của FIPA-ACL 遗产多代理 系统通信协议的历史标准与现代发展. 2000 năm: 20 型施事行为 (performatives) 内容语言和交互协议, chính xác là 2026 năm MCP/A2A/ACP đang tái phát triển thứ gì: JSON 契约替施事行为,自然语言替代本体.

> **【拓展：FIPA ACL 遗产→具体应用】**FIPA ACL (Foundation for Intelligent Physical Agents Agent Communication Language) là một tiêu chuẩn giao tiếp của các đại lý trong giai đoạn 1990-2000 . Mặc dù FIPA đã tan rã vào năm 2013, nhưng ý tưởng cốt lõi của nó vẫn ảnh hưởng đến các giao tiếp nguyên ngữ như INFORM, REQUEST, PROPOSE.

>  **【前置】**Học tập trước:Phase 16·01 ((Why need more Agent) Phase 13 ((MCP/工具协议)  本课是历史课理解FIPA ACL 才能看懂 2026 协议(MCP/A2A/ACP) 是重新发明还是真创新──

>  **【类比】**FIPA-ACL = "AI 界的拉丁语"── 2000 年的标准,2026 年的协议(MCP/A2A)大量继承其思想──区别:FIPA 用形式化本体(重)、现代协议用 JSON+自然语言(轻)──学历史的价值:避免重复FIPA 因为"本体太重"而死,现代协议要保持轻量──

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib) | **语言:** Python（标准库）
**Prerequisites:** Phase 16 · 01 (Why Multi-Agent) | **前置知识:** Phase 16 · 01（为什么需要多 Agent）
**Time:** ~60 minutes | **时间:** 约 60 分钟

##                                                                                                                                                                                                                                                               

> **【中文解读】**Các thỏa thuận của Agent năm 2026 dường như đã được thực hiện một cách nhanh chóng, thực tế là nhiều trong quá trình tái tạo một phần trong 20 năm trước.

Tân cảnh của các ứng viên-bản thức năm 2026 đang bận rộn: MCP cho các công cụ, A2A cho các đại lý, ACP cho kiểm toán doanh nghiệp, ANP cho niềm tin phi tập trung, NLIP cho nội dung ngôn ngữ tự nhiên, cộng với CA-MCP và hai chục đề xuất nghiên cứu.

> 2026 năm của Agent  giao ước lĩnh vực rất nóng:MCP sử dụng các công cụ A2A sử dụng Agent ACP sử dụng kiểm toán doanh nghiệp ANP sử dụng chuyển trung tâm tín ngưỡng NLIP sử dụng nội dung ngôn ngữ tự nhiên, còn CA-MCP và hơn 20 đề xuất nghiên cứu. Mỗi quy tắc đều tuyên bố mình là cơ bản.

Sự thật là hầu hết họ đang khám phá lại một cây quyết định rất cụ thể, 20 năm tuổi. Lý thuyết diễn văn từ Austin (1962) và Searle (1969) cho chúng ta "những phát biểu là hành động". KQML (1993) biến điều đó thành một giao thức dây. FIPA-ACL (được phê chuẩn năm 2000) đã tạo ra tiêu chuẩn hóa tham chiếu: hai mươi biểu diễn, ngôn ngữ nội dung SL0/SL1, giao thức tương tác cho contract-net và subscribe-notify. JADE và JACK là nền tảng tham chiếu Java. Những nỗ lực này đã mờ dần vào khoảng năm 2010 bởi vì chi phí trên của ontology quá nặng và web đang chiến thắng.

> 诚实的看法是, hầu hết trong số họ đang tái phát hiện một cái cây quyết định rất cụ thể từ hai mươi năm trước.  Austin  1962 và Searle  1969  thuyết hành vi ngôn ngữ nói cho chúng ta biết"话语即行动" KQML  1993 sẽ chuyển thành thỏa thuận đường dây FIPA-ACL  2000 phê duyệt) đã tạo ra tiêu chuẩn hóa tham chiếu: 20 hành vi xây dựng 内容语言 SL0/SL1  用于 hợp đồng mạng và giao dịch thông tin thông tin JADE 和 JACK là nền tảng tham chiếu Java 

Khi bạn nhìn vào MCP `tools/call`, chu kỳ cuộc sống nhiệm vụ của A2A, hoặc kho lưu trữ ngữ cảnh chia sẻ của CA-MCP, bạn đang xem xét một sự tái tạo mềm hơn, bản địa JSON của các quyết định FIPA.

> Khi bạn kiểm tra MCP của `tools/call`Khi lưu trữ các tài liệu chung của A2A hoặc CA-MCP, bạn sẽ thấy những gì FIPA  quyết định 柔和 hơn  JSON nguyên thủy tái mô tả.

## Khái niệm cốt lõi

> **【中文解读】**本节把谱系讲全:言语行为理论(Austin/Searle)→ KQML(1993)→ FIPA-ACL(2000,二十个施事行为 + SL0/SL1 内容语言 + 交互协议)→ JADE/JACK 平台 → 衰落 → LLM 时代以 JSON 语法复活──核心洞察:Agent 通信的语法表示小而稳定,只有方式在变──

### Các hành động diễn văn, trong một đoạn

> **【中文解读】**Một段话讲清理论根基:有些句子不是在描述世界,而是在改变世界 (("我承诺""我请求") ").

Austin nhận thấy rằng một số câu không mô tả thế giới  chúng thay đổi nó. "Tôi hứa". "Tôi yêu cầu". "Tôi tuyên bố". Ông gọi những phát biểu biểu biểu diễn này là "đồ chơi". Searle đã chính thức hóa năm loại: khẳng định, hướng dẫn, ủy thác, biểu hiện, tuyên bố. KQML (Finin et al., 1993) đã làm cho điều này hoạt động cho các đại lý phần mềm: một tin nhắn là một hoạt động (các hành động) cộng với nội dung (các hành động là gì). FIPA-ACL đã dọn dẹp các khoảng trống của KQML và chuẩn hóa khoảng hai mươi biểu diễn.

> Austin lưu ý rằng một số câu không mô tả thế giới chúng thay đổi thế giới. "Tôi hứa"", Tôi yêu cầu"", Tôi tuyên bố"", ông gọi những câu này là những lời nói xây dựng. Searle sẽ định hình nó thành năm loại: những lời nói, các lệnh, các cam kết, các biểu hiện, các tuyên bố.

### Hai mươi biểu diễn của FIPA (dân sách một phần)

| Performative | Intent |
|---|---|
| `inform` | "I tell you P is true" |
| `request` | "I ask you to do X" |
| `query-if` | "Is P true?" |
| `query-ref` | "What is the value of X?" |
| `propose` | "I propose we do X" |
| `accept-proposal` | "I accept the proposal" |
| `reject-proposal` | "I reject the proposal" |
| `agree` | "I agree to do X" |
| `refuse` | "I refuse to do X" |
| `confirm` | "I confirm P is true" |
| `disconfirm` | "I deny P" |
| `not-understood` | "Your message did not parse" |
| `cancel` | "Cancel the ongoing X" |
| `cfp` | "Call for proposals on X" |
| `subscribe` | "Notify me when X changes" |
| `failure` | "I tried X and failed" |

Danh sách đầy đủ đã được đưa vào `fipa00037.pdf`(FIPA ACL Message Structure) Điểm không phải là ghi nhớ nó  Điểm là mỗi một trong những điều này tương ứng với một nguyên thủy một giao thức LLM cuối cùng thêm lại.

> 完整列表在 `fipa00037.pdf`(FIPA ACL 消息结构) 中── trọng tâm không phải là ghi nhớ mà là mỗi người đối phó với một thỏa thuận LLM cuối cùng sẽ được thêm lại ngôn ngữ gốc──

### Thông điệp FIPA-ACL theo quy định

> **【中文解读】**Chỉ có 7 chữ cái nữa.`content`载荷字段。`conversation-id`和 `reply-with`Yêu cầu đáp ứng liên quan đến ngôn ngữ nguyên thủy Hệ thống thay đổi hiện đại liên tục tái phát minh những thứ; không có chúng thì không thể chuyển đổi nhiều vòng.

```
(inform
  :sender       agent1@platform
  :receiver     agent2@platform
  :content      "((price IBM 83))"
  :language     SL0
  :ontology     finance
  :protocol     fipa-request
  :conversation-id   conv-42
  :reply-with   msg-17
)
```

Bảy trường mang phong bì giao thức; một trường (`content`Các trường còn lại chính xác là những gì bạn phát minh lại mỗi khi bạn boult các thử nghiệm, threading và ontology vào một giao thức JSON.

> 七个字段承载协议信封;一个字段(`content`(Bài nguyên là bạn sẽ thử lại mỗi lần, các đường dẫn và bản chất được thêm vào giao thức JSON.

### Hai nền tảng di sản

**JADE**(Java Agent DEvelopment framework, 19992020s) là thời gian chạy phù hợp với FIPA được sử dụng nhiều nhất. Các đại lý mở rộng lớp cơ sở, trao đổi tin nhắn ACL, chạy bên trong container và phối hợp bằng cách sử dụng "hành vi". Thư viện giao tiếp giao thức được gửi với contract-net, đăng ký- thông báo, yêu cầu-lần, và đề xuất- chấp nhận.

> **JADE**(Java Agent Development Framework, 1999-2020 年代) là các loại thông thường nhất của FIPA 兼容运行时.

**JACK**(Software hướng đến đại lý, thương mại) nhấn mạnh lý luận BDI (Trái-Thiên-Thiên-Thiên) trên các thông điệp FIPA.

> **JACK**(Agent Oriented Software, Commercial Products) nhấn mạnh rằng FIPA 消息之上进行BDI (truyền định, ý định, ý định)

Cả hai đều giảm khi web stack ăn nhiều trường hợp sử dụng đại lý. MCP và A2A là "nhà chứa" chạy vào năm 2026.

> Một khi Web 技术吞了多代理用例, cả hai đều suy giảm. MCP và A2A là "container" trong năm 2026

### Tại sao FIPA bị xóa sổ

- **Ontology overhead.**FIPA yêu cầu một ontology chung để phân tích `content`. Thỏa thuận về các ontology là một quá trình tiêu chuẩn kéo dài nhiều năm.
  Trung ngữ翻译:**本体开销。**FIPA  cần chia sẻ bản thân để giải quyết `content`                                                                                                                                                                                                                                                              
- **Formal semantics nobody used.**SL (Ngôn ngữ ngữ ngữ nghĩa) đã đưa ra các điều kiện chân lý nghiêm ngặt, nhưng hầu hết các hệ thống sản xuất sử dụng nội dung dạng tự do và bỏ qua chủ nghĩa hình thức.
  Trung ngữ翻译:**没人用的形式语义。**SL (语义语言) cung cấp các điều kiện giá trị thực nghiêm ngặt, nhưng hầu hết các hệ thống sản xuất sử dụng nội dung theo hình thức tự do và bỏ qua hình thức主义.
- **Tooling lock-in.**JADE chỉ dùng Java, JACK là thương mại, các nhóm đa ngôn ngữ đều đi xung quanh cả hai.
  Trung ngữ翻译:**工具锁定。**JADE  chỉ hỗ trợ Java; Jack là thương mại.
- **The internet won the stack.**REST, sau đó là JSON-RPC, sau đó là gRPC thay thế vận chuyển của ACL.
  Trung ngữ翻译:**互联网赢得了技术栈。**REST, sau đó là JSON-RPC, sau đó là gRPC thay thế ACL truyền tải.

### Sự hồi sinh của LLM là FIPA-lite

> **【中文解读】**Để FIPA `request`和 MCP `tools/call`Và排放: 同一个信封(谁、对谁、意图、载荷、关联 id), khác nhau语法──Liu 等 2025 综述明确给出谱系映射:MCP=工具使用语行为,A2A=Agent đối với các hành vi ngôn ngữ,ACP=审计轨迹言语行为,ANP=去中心化身份扩展──新规范都是JSON语法、更松语义的ACL 后代──

So sánh FIPA `request`cho một MCP `tools/call`- Có thể là:

> FIPA`request`Với MCP`tools/call` để so sánh:

```
(request                                {
  :sender  agent1                         "jsonrpc": "2.0",
  :receiver tool-server                   "method":  "tools/call",
  :content "(lookup stock IBM)"           "params":  {"name":"lookup_stock",
  :ontology finance                                   "arguments":{"symbol":"IBM"}},
  :conversation-id c42                    "id": 42
)                                        }
```

cùng một phong bì, phân biệt tổng hợp. cả hai mang theo: ai, ai, ý định, tải trọng, liên quan ID. Cả hai không phải là một cuộc cách mạng trên người khác  họ là các thương mại khác nhau trên cùng một thiết kế.

> Các phong cách khác nhau, ngôn ngữ khác nhau. Cả hai đều mang theo: ai, đối với ai, ý định, tải trọng, liên quan.

Cuộc khảo sát năm 2025 của Liu et al. ("A Survey of Agent Interoperability Protocols: MCP, ACP, A2A, ANP", arXiv:2505.02279) làm rõ dòng dõi này: MCP tương ứng với các hành động ngôn ngữ sử dụng công cụ, A2A với các hành động ngôn ngữ đại lý-tương đương, ACP với các hành động ngôn ngữ kiểm tra, ANP với các tiện ích danh tính phi tập trung. Các thông số kỹ thuật mới là hậu duệ của ACL với tổng hợp JSON và ngữ nghĩa lỏng lẻo hơn.

> Liu 等人 2025年综述("Agent 互操作性协议综述:MCP, ACP, A2A, ANP",arXiv:2505.02279) rõ ràng chỉ ra dòng dõi này:MCP đối phó với các công cụ sử dụng ngôn ngữ,A2A đối phó với các đại lý đối phó với các hành vi ngôn ngữ khác,ACP đối phó với kiểm toán các quỹ đạo ngôn ngữ,ANP đối phó với sự mở rộng danh tính tập trung.

### Sự thỏa hiệp, được nói rõ ràng

> **【中文解读】**权衡要明说:FIPA 给形式语义(可证明) 规范施事行为目录(不用重辩) 带正确性保证的交互协议模式;现代规范给 JSON 原生载荷、自然语言内容、Web 传输、能力发现──交换的就是"更松散的意图语义换更容易实现"──

**What FIPA gave you and modern specs drop:**

> **FIPA 给你的而现代规范丢弃的：**

- Hình thức ngữ nghĩa  bạn có thể chứng minh `inform`cho thấy người gửi tin vào nội dung.
  中文翻译:形式语义你可以证明 `inform`Ý nghĩa là người gửi tin vào nội dung đó.
- Một danh mục biểu diễn theo luật pháp  bạn không cần phải tranh luận lại "chẳng lẽ chúng ta nên có một `cancel`? "
  Trung ngữ翻译:规范的施事行为目录你不必重新争论"我们应该有"`cancel`吗?"
- Nhiều thập kỷ các mô hình tương tác-bản thức giao dịch  hợp đồng-net, đăng ký- thông báo, đề xuất- chấp nhận  với các tính chất chính xác được biết đến.
  Trung ngữ翻译: nhiều thập kỷ giao dịch giao ước mô hình 合同网、订阅-通知、提议-接受具有已知正确性属性──

**What modern specs give you and FIPA did not:**

> **现代规范给你的而 FIPA 没有的：**

- Các tải trọng hữu ích gốc JSON tương thích với mọi công cụ hiện đại.
  Trung ngữ翻译:与每个现代工具兼容的 JSON 原生有效载荷──
- Nội dung ngôn ngữ tự nhiên mà LLM có thể giải thích mà không cần có một ontology mã hóa bằng tay.
  Trung ngữ翻译:LLM có thể giải thích nội dung ngôn ngữ tự nhiên trong trường hợp không có mã hóa tự nhiên.
- Giao thông web-stack (HTTP, SSE, WebSocket).
  Trung文翻译:Web 技术传输(HTTP、SSE、WebSocket)
- Khám phá khả năng thông qua MCP trực tiếp `server/discover`và A2A Agent Cards.
  Trung文翻译:通过实时 MCP `server/discover`Và A2A Agent Card  thực hiện khả năng phát hiện.

Hỗn định nghĩa ý định thô lỗ hơn để dễ dàng thực hiện. Đó là giao dịch chính xác.

> Hơn nữa, ý nghĩa của việc thực hiện dễ dàng hơn là thực hiện.

### Các giao thức tương tác đáng được chuyển

> **【中文解读】**FIPA 约15 交互协议里,三个值搬进 LLM 多 Agent 系统:合同网(任务市场模式,应应阶段16·16 协商) 订阅/通知(每个事件总线) 请求当(持久工作流引擎的延迟任务,应阶段16·22) 它们都能干净映射到现代消息队列、HTTP + 轮询或 SSE 流──

FIPA đã vận chuyển ~ 15 giao thức tương tác. Ba là đáng để chuyển tiếp vào các hệ thống đa đại lý LLM:

> FIPA đã công bố khoảng 15 hiệp định giao tiếp. Trong đó ba nên được kéo dài cho LLM đa đại lý trong hệ thống:

1. **Contract Net Protocol (CNP).**Các vấn đề của quản lý `cfp`(cần mời đề xuất); người đề nghị trả lời bằng cách:`propose`; người quản lý chấp nhận/rước đi. Đây là mô hình thị trường công việc theo quy định (Phase 16 · 16 đàm phán).
   Trung ngữ翻译:**合同网协议 (CNP)。**管理者发布 `cfp`(征求提案);投标者用 `propose`响应;管理者接受/拒绝──这是典型任务市场模式(Phase 16 · 16 协商)──
2. **Subscribe/Notify.**Người đăng ký gửi `subscribe`; nhà xuất bản gửi `inform`Đây là tất cả các sự kiện-băng trong năm 2026.
   Trung ngữ翻译:**订阅/通知。**订阅者发送 `subscribe`; nhà phát hành trong chủ đề thay đổi `inform`Đây là toàn bộ các sự kiện của năm 2026.
3. **Request-When.**"Do X khi điều kiện Y giữ". Hành động chậm với điều kiện trước. 2026 analog là các nhiệm vụ bị hoãn trong động cơ lưu lượng công việc bền (Phase 16 · 22 Scaling sản xuất).
   Trung ngữ翻译:**请求-当。**"when condition Y 成立时执行 X──"带前置条件的延迟动作──2026 年的类似物是持久工作流引擎中的延迟任务(Phase 16 · 22 生产扩展)──

Mỗi bản đồ được vẽ sạch sẽ vào hàng rào thông điệp hiện đại, thăm dò HTTP + hoặc phát trực tuyến SSE.

> Mỗi một trong số chúng có thể được hiển thị rõ ràng đến các dòng tin tức hiện đại, HTTP + 轮询 hoặc SSE 流.

### Điều gì bị phá vỡ khi bạn bỏ ra ontology

> **【中文解读】**Giá cả của việc mất cơ thể là**语义漂移**: hai đại lý đối với cùng một từ (("thành khách") có những khái niệm khác nhau, nhận theo sự hiểu lầm hành động, trong khi các quy trình 验证器 không tồn tại.`content`上加 JSON Schema、类型化工件(A2A)、信封里显式施事行为──

Không có một ontology chung, các đại lý suy luận ý nghĩa từ nội dung ngôn ngữ tự nhiên.**semantic drift**: hai đại lý sử dụng cùng một từ (`"customer"`) đối với các khái niệm khác nhau tinh tế, đại lý của người nhận hành động trên giải thích sai lầm, không có người xác nhận sơ đồ nào bắt được nó.

> Không chia sẻ nội dung,Agent từ nội dung ngôn ngữ tự nhiên 推断含义──记录在案的2026年失败模式是**语义漂移**: 2 đại lý đối với cùng một từ`"customer"`(văn khoái) có một khái niệm khác nhau, người nhận đại lý dựa trên hành động hiểu lầm, không có mô hình xác nhận có thể bắt được nó.

Giảm thiểu mà không đi theo toàn bộ ontology:

> Không sử dụng hoàn toàn các biện pháp giảm bớt nội tại:

- JSON Schema trên `content` từ chối các lỗi cấu trúc trên dây.
  Trung ngữ翻译:对 `content`Sử dụng JSON Schema trong truyền tải cấp từ chối cấu trúc lỗi
- Các đồ tạo tác kiểu (A2A)  từ chối phương thức sai lầm.
  Trung ngữ翻译:类型化工件(A2A) 拒绝错误的模态。
- Các biểu diễn rõ ràng trong phong bì  làm cho ý định không rõ ràng ngay cả khi nội dung là ngôn ngữ tự nhiên.
  Trung ngữ翻译:信封中显式施事行为 ngay cả khi nội dung là ngôn ngữ tự nhiên cũng làm ý định rõ ràng.

### Các thông số kỹ thuật năm 2026, được lập bản đồ theo di sản hành động nói

| Modern spec | FIPA analog | What it keeps | What it drops |
|---|---|---|---|
| MCP `tools/call` | `request` | explicit intent, correlation id | formal semantics, ontology |
| MCP `resources/read` | `query-ref` | explicit intent, correlation id | formal semantics |
| A2A Task lifecycle | contract-net + request-when | async lifecycle, state transitions | formal completeness guarantees |
| A2A streaming events | subscribe/notify | async push | typed-predicate subscription |
| CA-MCP shared context | blackboard (Hayes-Roth 1985) | multi-writer shared memory | logical consistency model |
| NLIP | natural-language content | LLM-native | schema |

Đọc bảng từ trên xuống dưới, mô hình là: giữ nguyên chất cấu trúc, bỏ đi sự hình thức, để LLM ghi chép về sự mơ hồ.

> Từ trên xuống đọc biểu mẫu, mô hình là: giữ lại cấu trúc nguyên ngữ, bỏ qua hình thức主义, để LLM 弥补模糊性.

> **【中文解读】**Một câu nói tổng kết toàn表:2026 规范保留的是结构性原语(显式意图、关联 id、异步生命周期), bị bỏ qua là形式主义(形式语义、本体、逻辑一致性), sử dụng năng lực giải thích của LLM để điền vào歧义── đây là "capacity chứng minh tương tác giá rẻ"

```figure
sw-contract-net
```

## Hãy xây dựng nó.

> **【中文解读】**Example Code là một bộ nhớ tiêu chuẩn FIPA-ACL 翻译器:把五条 MCP/A2A 风格消息编码成 FIPA-ACL 再解码回来,并跑一个"一个管理员 + 三投标者"玩具合同网协商――输出并排显示相同消息的2026 JSON 形态和FIPA-ACL 形态和一些协议原语在往返中存活,只有语法不同――

`code/main.py`thực hiện một trình dịch FIPA-ACL tự nhiên. Nó mã hóa và giải mã phong bì ACL theo quy định và cho thấy cách mỗi hình dạng thông điệp MCP / A2A giảm xuống đến cùng bảy trường.

> `code/main.py`实现一个纯标准库的FIPA-ACL翻译器──它编解标准标准ACL 信封,并展示每个MCP / A2A 消息形状如何简化为相同的七段──演示内容:

- Mã hóa năm thông điệp kiểu MCP và kiểu A2A như FIPA-ACL.
  Trung ngữ翻译:将将五个 MCP 风格和 A2A 风格的消息编码为 FIPA-ACL。
- Đánh mã FIPA-ACL trở lại với tương đương hiện đại.
  Trung文翻译:将 FIPA-ACL 解码回现代等效形式──
- Giao dịch giao dịch giữa một nhà quản lý và ba nhà đấu thầu sử dụng `cfp`- `propose`- `accept-proposal`- `reject-proposal`- Tôi không biết.
  中文翻译:使用 `cfp``propose``accept-proposal``reject-proposal`Trong một quản lý và ba nhà đầu tư vận hành một hợp đồng chơi game.

Đi chạy:

```
python3 code/main.py
```

Kết quả là một dấu vết bên cạnh cho thấy mỗi tin nhắn hiện đại trong cả dạng JSON 2026 và dạng FIPA-ACL của nó, sau đó là một chuyến đi về của một lệnh hợp đồng-net.

> 输出 là một trình theo dõi, hiển thị mỗi 条现代消息的 2026 JSON 形式和 FIPA-ACL 形式, sau đó là 往返的合同网投标.

## Hãy sử dụng nó để thực hiện

`outputs/skill-fipa-mapper.md`là một kỹ năng đọc bất kỳ thông số đặc trưng của các nguyên tắc và tạo ra bản đồ FIPA-ACL. Sử dụng nó trước khi áp dụng một nguyên tắc mới để trả lời: "Đây có thực sự mới, hay nó là`inform`với ngữ pháp JSON?"

> `outputs/skill-fipa-mapper.md`là một kỹ năng, đọc bất kỳ Agent 协议规范并生成 FIPA-ACL 映射.`inform`"Điều gì?"

## Chuyển nó đi.

> **【中文解读】**Đừng làm nổi FIPA-ACL, hãy mang lại nó lại:意图原语、关联 id、显式内容语言、一等公民的交互协议、语义漂移预案── bất kỳ giao ước mới nào được sản xuất trước, trước trả lời năm câu hỏi này──

Đừng mang lại FIPA-ACL.

> Đừng mang lại FIPA-ACL...

- Ý định ban đầu (sản xuất) của mỗi tin nhắn là gì?
  Trung ngữ翻译:每条消息的意图原语(施事行为) là gì?
- Có một ID tương quan cho yêu cầu-phản ứng và hủy bỏ?
  Trung ngữ翻译: Có liên kết ID được sử dụng để yêu cầu- đáp ứng và hủy bỏ không?
- Có một ngôn ngữ nội dung rõ ràng (JSON-RPC, văn bản đơn giản, tạo vật được đánh chữ có cấu trúc)?
  Trung văn翻译: có một ngôn ngữ nội dung rõ ràng không?
- Các giao thức tương tác có hạng nhất không, hay bạn đang tái triển khai hợp đồng từ đầu?
  Trung ngữ翻译:交互协议 là công dân bình đẳng, hay bạn đang bắt đầu tái thực hiện hợp đồng mạng?
- Điều gì xảy ra khi hai nhân viên không đồng ý về ý nghĩa nội dung (trái hướng ngữ nghĩa)?
  Trung ngữ翻译:当两个代理对内容含义有分歧时会发生什么?

Hãy ghi lại 5 câu hỏi này cho bất kỳ giao thức mới nào trước khi bạn đưa nó vào sản xuất.

> Trước khi bất kỳ thỏa thuận mới nào được công bố cho đến khi sản xuất môi trường, ghi lại 5 vấn đề này.

## Tập luyện bài tập

1. Đi chạy`code/main.py`- Quan sát mã hóa đi về và đi. xác định các hiệu ứng FIPA tương ứng với `tools/call`- `resources/read`, và tạo nhiệm vụ A2A.
   Trung ngữ翻译:运行 `code/main.py` quan sát 往返编码  nhận ra những hành vi của FIPA 施事对应 `tools/call``resources/read`Và A2A  nhiệm vụ tạo dựng
2. Cải tiến bản demo hợp đồng với một `cancel`- Điều gì xảy ra khi thất bại?`cancel`giải quyết những thử nghiệm này một mình, phải không?
   中文翻译:用 `cancel`施事行为扩展合同网演示, để quản lý có thể rút lại nhiệm vụ trong quá trình đấu thầu.`cancel`đang giải quyết những tình huống không thể giải quyết được bằng cách thử lại?
3. Đọc FIPA ACL Message Structure (http://www.fipa.org/specs/fipa00037/) các phần 4.14.3. Chọn một biểu diễn không được đề cập trong bài học này và mô tả các tương tự JSON-RPC hiện đại của nó.
   Trung文翻译:阅读 FIPA ACL 消息结构(http://www.fipa.org/specs/fipa00037/）第4.1-4.3 节──选择本课未涵盖的一个施事行为并描述其现代 JSON-RPC类比──
4. Đọc Liu et al., arXiv:2505.02279. Đối với mỗi MCP, A2A, ACP, ANP, liệt kê các gia đình hiệu suất FIPA họ giữ và thả.
   Trung văn翻译:阅读 Liu 等人,arXiv:2505.02279── đối với mỗi trong số MCP、A2A、ACP、ANP, liệt kê chúng giữ lại và bỏ rơi của FIPA 施事行为族──
5. Thiết kế một JSON-Schema tối thiểu cho `content`trường của a `request`Điều gì mà chương trình này cung cấp cho bạn mà ngôn ngữ tự nhiên không cung cấp, và nó tốn bao nhiêu tiền?
   Trung ngữ                                    `request`施事行为 `content`字段设计一个最小的JSON-Schema――这个模式给你提供纯自然语言没有什么,价格是多少?

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means | 中文术语 |
|------|----------------|------------------------|----------|
| Speech act | "An utterance that does something" | Austin/Searle: utterances as actions. The theoretical parent of ACL. | 言语行为 |
| FIPA | "That old XML thing" | IEEE Foundation for Intelligent Physical Agents. Standardized ACL in 2000. | FIPA 基金会 |
| ACL | "Agent Communication Language" | FIPA's envelope format: performative + content + metadata. | Agent 通信语言 |
| Performative | "The verb" | The intent class of a message: `inform`, `request`, `propose`, `cfp`, etc. | 施事行为 |
| KQML | "FIPA's predecessor" | Knowledge Query and Manipulation Language (1993). Simpler, narrower. | KQML |
| Ontology | "Shared vocabulary" | A formal definition of the concepts the content language talks about. | 本体 |
| SL0 / SL1 | "FIPA content languages" | Semantic Language levels 0 and 1 — the formal content language family. | SL 内容语言 |
| Contract Net | "Task market" | Manager issues cfp; bidders propose; manager accepts. The canonical interaction protocol. | 合同网 |
| Interaction protocol | "Pattern of messages" | A sequence of performatives with known correctness: request-when, subscribe-notify, etc. | 交互协议 |

## Xem thêm 延伸阅读

- [Liu et al. — A Survey of Agent Interoperability Protocols: MCP, ACP, A2A, ANP](https://arxiv.org/html/2505.02279v1) khảo sát kinh điển năm 2025 kết nối các thông số kỹ thuật hiện đại với di sản của FIPA
  Trung ngữ翻译:Liu 等人Agent 互操作性协议综述,连接现代规范与FIPA 遗产的权威 2025 综述
- [FIPA ACL Message Structure Specification (fipa00037)](http://www.fipa.org/specs/fipa00037/) định dạng gói 2000 được phê chuẩn
  Trung ngữ翻译:FIPA ACL 消息结构规范2000年批准的信封格式
- [FIPA Communicative Act Library Specification (fipa00037)](http://www.fipa.org/specs/fipa00037/) danh mục thực hiện đầy đủ
  Trung文翻译:FIPA 通信行为库规范完整的施事行为目录
- [MCP specification 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28) tương đương sử dụng công cụ hiện tại không có quốc tịch của `request`- Không.`query-ref`
  Trung文翻译:MCP 2026-07-28 规范`request`- Không.`query-ref`                                                                                                                                                                                                                                                              
- [A2A specification](https://a2a-protocol.org/latest/specification/) tương đương đại lý-bạn đồng cấp hiện đại của hợp đồng-net và đăng ký- thông báo
  Trung ngữ翻译:A2A 规范合同网和订阅通知的现代代理对等效
