# A2A  Thông tin giao tiếp giữa đại lý và đại lý

> MCP là đại lý-đồ dùng. A2A (Agent2Agent) là một giao thức mở để cho phép các đại lý không minh bạch được xây dựng trên các khung khác nhau hợp tác. Được phát hành bởi Google vào tháng 4 năm 2025, được quyên góp cho Quỹ Linux vào tháng 6 năm 2025, đạt v1.0 vào tháng 4 năm 2026 với 150 + người ủng hộ bao gồm AWS, Cisco, Microsoft, Salesforce, SAP và ServiceNow. Nó hấp thụ ACP của IBM và thêm mở rộng thanh toán AP2. Bài học này sẽ kể về thẻ đại lý, vòng đời nhiệm vụ và hai liên kết vận tải.

> **【中文解读】**MCP là Hiệp định công cụ đại lý, A2A là Hiệp định đại lý- đại lý để tạo ra các khuôn khổ khác nhau không minh bạch của Đại lý  hợp tác với nhau. Hiệp định mở rộng được phát hành vào tháng 4 năm 2025. Google đã tặng cho Linux 基金会 vào tháng 6 năm 2025.

> **【拓展】**A2A và MCP là sự bổ sung và không thay thế. MCP được sử dụng để điều chỉnh các công cụ cụ thể, A2A được sử dụng để giao nhiệm vụ cho một đại lý khác.`/.well-known/agent.json`) tương tự như cơ chế phát hiện công cụ của MCP, nhưng mô tả về khả năng của Đại lý chứ không phải là công cụ.

>  **【前置】**学本节前请先掌握:(1) Bước 13·06(MCP cơ bản) và 13·08(MCP client)  hiểu MCP là đại lý-to-tool,本节 là đại lý-to-agent;(2) HTTP + JSON-RPC 基础;(3) SSE hoặc轮询机制A2A Task 状态订阅;(4) 异步任务概念,可参考 Bước 13·13。

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, Agent Card + Task harness) | **语言:** Python (stdlib, Agent Card + Task harness)
**Prerequisites:** Phase 13 · 06 (MCP fundamentals), Phase 13 · 08 (MCP client) | **前置知识:** Phase 13 · 06 (MCP fundamentals), Phase 13 · 08 (MCP client)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Mục tiêu học tập

- Sự khác biệt giữa các trường hợp sử dụng từ đại lý đến công cụ (MCP) và các trường hợp sử dụng từ đại lý đến đại lý (A2A).
  Trung文翻译:区分 Agent-工具(MCP) 和 Agent-Agent(A2A) 用例──
- Giới thiệu thẻ đại lý tại `/.well-known/agent.json`với các kỹ năng và metadata điểm cuối.
  Trung ngữ翻译:在 `/.well-known/agent.json`发布带技能和端点元数据的代理卡──
- Đi theo vòng đời Task (đưa -> làm việc -> nhập-cần -> hoàn thành / thất bại / hủy bỏ / từ chối).
  中文翻译:走通 Nhiệm vụ 生命周期(đưa -> làm việc -> nhập-cần -> hoàn thành / thất bại / hủy bỏ / từ chối) ]]
- Sử dụng Thông điệp với các bộ phận (tin, tệp, dữ liệu) và đồ tạo như các đầu ra.

> **【中文解读】**Học mục tiêu: phân biệt các công cụ của đại lý (MCP) với đại lý (A2A); xuất bản thẻ đại lý; đi thông qua nhiệm vụ (Task)  vòng đời; sử dụng các phần (Messages) và đồ tạo (Artefacts) 输出――

## Vấn đề  vấn đề giới thiệu

> **【中文解读】**客服 Agent 需要将报告撰写委托给专门写作 Agent──A2A 之前的选择(定制 REST API、共享代码库、MCP) 都不适宜──A2A sẽ tương tác xây dựng mô hình như một Agent sang một Agent 发送任务,具有生命周期、消息和工件──被调用 Agent 的内部状态保持不透明调用者只看到任务状态转换和最终输出──

Một đại lý dịch vụ khách hàng cần ủy quyền viết báo cáo cho một đại lý viết chuyên ngành.

> 客服 Agent 需要将报告撰写委托给专门写作 Agent。A2A 之前的选项:

- REST API tùy chỉnh, hoạt động nhưng mỗi cặp đều là một lần.
  Trung文翻译:定制 REST API──可行但每个配对都是一次性──
- Hình thức chia sẻ mã, yêu cầu hai đại lý chạy cùng một khung.
  Trung文翻译:共享代码库.
- MCP không phù hợp: MCP là để gọi công cụ, không phải cho hai đại lý hợp tác trong khi vẫn giữ cho lý luận nội bộ không rõ ràng của mỗi đại lý.
  Trung ngữ翻译:MCP──不合适:MCP 用于调用工具,而不是两个代理在保持各自不透明的内部推理下协作──

A2A lấp đầy khoảng trống. Nó mô hình hóa sự tương tác khi một đại lý gửi một Task đến một đại lý khác, với chu kỳ sống, tin nhắn và đồ tạo. trạng thái nội bộ của đại lý được gọi vẫn không minh bạch  người gọi chỉ thấy chuyển đổi trạng thái nhiệm vụ và đầu ra cuối cùng.

> A2A 填空白──它 sẽ tương tác xây dựng hình thức để một Agent gửi đến một khác Thể vụ, với chu kỳ sống、消息和工件── được调用 Ứng viên trạng thái nội bộ của Agent giữ không minh bạch Người调用 chỉ nhìn vào trạng thái chuyển đổi và cuối cùng xuất.

A2A là giao thức "cho phép các đại lý trên các khung nói chuyện với nhau".

> A2A là "để tạo ra một khung giao tiếp giữa các đại lý".

>  **【类比】**A2A vs MCP 像公司"外包项目" vs "公司内调用工具"──MCP là một kỹ sư (agent) dùng máy tính (tool) 他知道计算器怎么工作、用完就完成,是工具调用──A2A là một công ty A Đưa toàn bộ dự án (task) ngoài包 cho công ty B(một đại lý khác)A không biết B 内部怎么做(不透明), chỉ nhìn vào giao hàng (artifact);B là một công ty độc lập có dòng chảy làm việc riêng của mình, công cụ riêng của mình, trạng thái nội bộ của mình──A2A quan tâm đến biên giới nhiệm vụ, giao hàng hình dạng, trở lại, không quan tâm B sử dụng gì khung hình  LongChain hoặc AutoGen) thực hiện.

## Khái niệm cốt lõi

### Cảnh sát Thư

> **【中文解读】**Thẻ đại lý: Mỗi đại lý A2A 兼容 `/.well-known/agent.json`发布卡,包含名称、描述、URL、版本、技能列表和能力声明──发现是基于URL的获取卡,学习A2A 端点URL,枚举技能──

Mỗi đại lý tuân thủ A2A đều xuất bản một thẻ tại `/.well-known/agent.json`- Có thể là:

> Mỗi A2A 兼容 đại lý trong `/.well-known/agent.json`发布卡片:

```json
{
  "schemaVersion": "1.0",
  "name": "research-agent",
  "description": "Summarizes academic papers and drafts citations.",
  "url": "https://research.example.com/a2a",
  "version": "1.2.0",
  "skills": [
    {
      "id": "summarize_paper",
      "name": "Summarize a paper",
      "description": "Read a paper PDF and produce a 3-paragraph summary.",
      "inputModes": ["text", "file"],
      "outputModes": ["text", "artifact"]
    }
  ],
  "capabilities": {"streaming": true, "pushNotifications": true}
}
```

Khám phá dựa trên URL: lấy thẻ, tìm hiểu URL của điểm cuối A2A, liệt kê kỹ năng.

> 发现基于URL:获取卡片、学习 A2A 端点URL、枚举技能──

### Thẻ đại lý được ký (AP2)

Phiên bản mở rộng AP2 (Tháng 9 năm 2025) thêm chữ ký mật mã vào thẻ Agent. Một nhà xuất bản ký thẻ của riêng mình với một JWT; người tiêu dùng xác minh.

> AP2 扩展(2025 年 9 月) cho thẻ đại lý 添加密签名。 nhà phát hành sử dụng JWT  ký thẻ của riêng mình;消费者验证。防止冒充。

### Chuyển đời của nhiệm vụ

> **【中文解读】**Nhiệm vụ  vòng đời: gửi -> làm việc -> hoàn thành                                                                                                                                                                                                                                                        `tasks/send`发起, thông qua SSE 订阅 trạng thái cập nhật hoặc vòng hỏi.

```
submitted -> working -> completed | failed | canceled | rejected
             -> input_required -> working (loop via message)
```

Khách hàng bắt đầu với `tasks/send`Các đại lý được gọi chuyển qua các tiểu bang; khách hàng đăng ký cập nhật tiểu bang thông qua SSE hoặc thăm dò.

> 客户端用 `tasks/send`发起──被调用 通过状态转换;客户端通过 SSE或轮询订阅状态更新──

> ️ **【易错点】**场景:A2A 调用方在 `submitted` trạng thái后立刻等 `completed`而不处理 `input_required`/ 后果: được tuyển dụng Trưởng  cần bổ sung thông tin 时卡在 `input_required`,调用方误以为还在`working`永久等待, toàn bộ工作流死锁 / 修复:(1) 调用方必须实现完整的任务 生命周期状态机,每个状态都有操作员;(2) `input_required`时主动拉取消息内容并触发新一轮 `tasks/send`;(3) 设置总超时(如 10 分钟), đến khi đạt được sau hủy nhiệm vụ并报错。

> 🤔 **【困惑】**Q: 既然 A2A là đại lý-to-agent,那 đại lý A 怎么知道 đại lý B 信任它、会不会拒绝? A: 信任通过 Agent Card + AP2 签名建立:(1) 证券描述能力,AP2 dùng JWT 签名防冒充;(2) 调用前 A thường đã thông qua OAuth等机制拿到B's访问代币;(3) B có thể từ chối(`rejected`状态),如调用方没付费 (AP2 支付扩展) 权限不足,负载过满;

### Thông điệp và phần

Một tin nhắn chứa một hoặc nhiều phần:

> Một tin nhắn mang theo một hoặc nhiều phần:

- `text` nội dung đơn giản.
  Trung ngữ翻译:`text`纯文本内容──
- `file` base64 blob với mimeType.
  Trung ngữ翻译:`file`base64 blob 带 mimeType。
- `data` nhập tải trọng hữu ích JSON (tài nhập cấu trúc cho đại lý được gọi).
  Trung ngữ翻译:`data` loại hóa JSON  tải  được调用 Agent 的结构化输入)

Ví dụ:

```json
{
  "role": "user",
  "parts": [
    {"type": "text", "text": "Summarize this paper."},
    {"type": "file", "file": {"name": "paper.pdf", "mimeType": "application/pdf", "bytes": "..."}},
    {"type": "data", "data": {"targetLength": "3 paragraphs"}}
  ]
}
```

### Các đồ tạo tác

Các sản phẩm là các sản phẩm, không phải chuỗi nguyên liệu. Một sản phẩm là một sản phẩm có tên, được gõ:

> 输出是 Artifact,而非裸字符串――Artifact là kiểu hóa của tên gọi:

```json
{
  "name": "summary",
  "parts": [{"type": "text", "text": "..."}],
  "mimeType": "text/markdown"
}
```

Các đồ tạo vật có thể được truyền qua các mảnh, người gọi sẽ tích lũy.

> Các tác phẩm có thể được chuyển giao như một khối.

### Hai liên kết vận chuyển

1. **JSON-RPC over HTTP.** `/a2a`Endpoint, POST cho yêu cầu, SSE tùy chọn cho streaming.
  Trung ngữ翻译:**JSON-RPC over HTTP。** `/a2a`端点、POST 用于请求、可选SSE 用于流式──默认绑定──
2. **gRPC.**Đối với môi trường doanh nghiệp nơi gRPC là bản địa.
  Trung ngữ翻译:**gRPC。**Sử dụng gRPC nguyên thủy môi trường doanh nghiệp.

Cả hai liên kết đều có cùng một hình dạng thông điệp logic.

> 两种绑定携带相同逻辑消息形态――

### Bảo tồn độ trống

> **【中文解读】**Không minh bạch: trạng thái bên trong của Đại lý được调用 là không minh bạch. Người调用 chỉ nhìn vào trạng thái nhiệm vụ và các công cụ, không nhìn vào các công cụ tư duy liên kết.

Một nguyên tắc thiết kế chính: trạng thái nội bộ của đại lý được gọi là không minh bạch. Người gọi thấy trạng thái nhiệm vụ và các vật liệu. Dòng tư tưởng của đại lý được gọi, các cuộc gọi công cụ của nó, đại diện phụ của nó  tất cả đều vô hình. Điều này khác với MCP, nơi các cuộc gọi công cụ là minh bạch.

> 关键设计原则: được调用 Agent's internal state is opaque──调用者 see task state and workpiece──被调用 Agent's thinking chain、工具调用、子 Agent 委托全部不可见── điều này không giống với MCP, việc调用 các công cụ của MCP là rõ ràng──

Lý luận: A2A cho phép các đối thủ cạnh tranh hợp tác mà không tiết lộ nội bộ. A2A có thể là "hãy gọi cho đại lý dịch vụ khách hàng này" mà không cần người gọi học cách đại lý đó thực hiện dịch vụ.

> Nguyên tắc:A2A 让竞争对手在不露内部的情况下协作──A2A có thể là "调用此客服代理",而调用者不需要学习该代理如何实现服务──

### Thời gian

- **2025-04-09.**Google công bố A2A.
  Trung ngữ翻译:**2025-04-09。**Google công bố A2A:
- **2025-06-23.**Được tặng cho Linux Foundation.
  Trung ngữ翻译:**2025-06-23。**捐给Linux 基金会。
- **2025-08.**Thuốc ACP của IBM.
  Trung ngữ翻译:**2025-08。**吸收 IBM của ACP:
- **2025-09.**Tàu mở rộng AP2 (Giá nhân viên).
  Trung ngữ翻译:**2025-09。**AP2 扩展(Agent 支付) phát hành
- **2026-04.**v1.0 được phát hành với 150+ tổ chức hỗ trợ.
  Trung ngữ翻译:**2026-04。**V1.0 发布,150+ 支持组织──

### Mối quan hệ với MCP

| Dimension | MCP | A2A |
|-----------|-----|-----|
| Use case | Agent-to-tool | Agent-to-agent |
| Opacity | Transparent tool calls | Opaque inner reasoning |
| Typical caller | Agent runtime | Another agent |
| State | Tool-call result | Task with lifecycle |
| Authorization | OAuth 2.1 (Phase 13 · 16) | JWT-signed Agent Cards (AP2) |
| Transport | Stdio / Streamable HTTP | JSON-RPC over HTTP / gRPC |

Sử dụng MCP khi bạn muốn gọi một công cụ cụ thể. Sử dụng A2A khi bạn muốn ủy thác toàn bộ nhiệm vụ cho một đại lý khác. Nhiều hệ thống sản xuất sử dụng cả hai: một đại lý sử dụng MCP cho lớp công cụ của mình và A2A cho lớp hợp tác của mình.

> 想调用特定工具时使用MCP──想将整个任务委托给另一个代理──时使用A2A──许多生产系统都使用:

## Hãy sử dụng nó để thực hiện

> **【中文解读】** `code/main.py`实现最小A2A 线束: nghiên cứu Agent 发布卡片,写作 Agent 接收 `tasks/send`(含 PDF 和文本指令的部分),经历工作 -> input_required -> working -> completed 生命周期,返回文本 Artifact。全部标准库,使用内存传输关注消息形状。
```figure
a2a-task-lifecycle
```

## Sử dụng nó

`code/main.py`thực hiện một vòng A2A tối thiểu: một đại lý nghiên cứu xuất bản thẻ của mình, một đại lý viết nhận được một `tasks/send`với các bộ phận bao gồm một PDF và một hướng dẫn văn bản, chuyển đổi thông qua làm việc → input_required → working → hoàn thành, và trả lại một vật liệu văn bản.

> `code/main.py`实现最小A2A 线束: nghiên cứu Agent 发布卡片、写作 Agent 接收 `tasks/send`(có chứa các phần của PDF và văn bản chỉ thị) 、 kinh nghiệm làm việc → input_required → làm việc → hoàn thành、 quay lại văn bản Artifact。全部标准库; sử dụng内存传输以聚焦消息形态。

Những gì cần xem:

- Hình dạng JSON của thẻ đại lý.
  中文翻译:Tẻ đại lý JSON 形态。
- Đề xuất ID nhiệm vụ và chuyển đổi trạng thái.
  Trung文翻译:Task id 分配和状态转换──
- Thông điệp với các bộ phận hỗn hợp.
  Trung ngữ翻译:带混合类型部分的消息──
- Các chi nhánh cần phải nhập vào giữa nhiệm vụ.
  Trung ngữ翻译:任务中的输入要求分支──
- Các vật liệu sẽ được trả về khi hoàn thành.
  Trung文翻译:完成时返回 Kỹ thuật.

## Chuyển nó đi.

> **【中文解读】**本课产 出 `outputs/skill-a2a-agent-spec.md` Đưa ra một đại lý mới có thể được sử dụng                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                

Bài học này sẽ mang lại kết quả `outputs/skill-a2a-agent-spec.md`Với một đại lý mới mà nên được gọi bởi các đại lý khác, kỹ năng tạo ra thẻ đại lý JSON, kế hoạch kỹ năng và bản phác thảo điểm cuối.

> 本课产 出 `outputs/skill-a2a-agent-spec.md` Đưa ra một đại lý mới được sử dụng bởi một đại lý khác, kỹ năng này tạo ra thẻ đại lý JSON、 kỹ năng sơ đồ và điểm cuối蓝图──

## Tập luyện bài tập

1. Đi chạy`code/main.py`. Theo dõi toàn bộ vòng đời nhiệm vụ, bao gồm cả thời gian tạm dừng cần thiết khi người gọi yêu cầu giải thích.
   Trung ngữ翻译:运行 `code/main.py` Theo dõi toàn bộ nhiệm vụ 周期 đời, bao gồm được gọi Agen Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên Ứng viên ng viên Ứng viên ng viên ng viên ng viên ng viên ng viên ng viên ng viên ng viên ng viên ng viên ng viên ng viên ng viên

2. Thêm một thẻ đại lý được ký, ký với HMAC trên thẻ JSON có thể xác minh và xác nhận nó thất bại trên một thẻ đột biến.
   Trung文翻译:添加签名 证券卡. 签名 写证器,确认对变异卡失败.

3. Thực hiện truyền tải nhiệm vụ: đại lý viết phát ra ba khối tạo vật tăng lên trên SSE và người gọi tích lũy chúng.
   Trung文翻译:实现任务流式:写作 Agent 通过 SSE 发发出三个增量文物块,调用者累积它们──

4. Thiết kế một đại lý A2A bao gồm một máy chủ MCP. Bản đồ mỗi công cụ MCP để một kỹ năng A2A. Lưu ý các sự thỏa hiệp  bất độ sáng bị mất?
   Trung ngữ翻译:设计包装 MCP 服务器的A2A Agent──将每个MCP 工具映射到A2A技能──注意权衡丢失了什么不透明性?

5. Đọc thông báo A2A v1.0 và xác định một tính năng chưa được thực hiện bởi bất kỳ khung nào vào tháng 4 năm 2026. (Thông dụ: nó liên quan đến ủy quyền nhiệm vụ đa hop).
   Trung ngữ翻译:阅读 A2A v1.0 公告,识别截止2026 年 4 月尚未被任何框架实现的一个功能──(提示:与多跳任务委托有关──)

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means | 中文 |
|------|----------------|------------------------|------|
| A2A | "Agent-to-Agent protocol" | Open protocol for opaque agent collaboration | Agent 间通信协议 |
| Agent Card | "`.well-known/agent.json`" | Published metadata describing an agent's skills and endpoint | Agent 卡片：发布能力元数据 |
| Skill | "A callable unit" | A named operation the agent supports (analog to MCP tool) | 技能：Agent 支持的可调用操作 |
| Task | "Unit of delegation" | A work item with a lifecycle and final artifact | 任务：带生命周期的委托工作单元 |
| Message | "Task input" | Carries Parts (text, file, data) | 消息：携带 Parts 的任务输入 |
| Part | "Typed chunk" | `text` / `file` / `data` element of a message | 部件：消息的类型化元素 |
| Artifact | "Task output" | Named, typed output returned on completion | 工件：完成时返回的命名类型化输出 |
| AP2 | "Agent Payments Protocol" | Signed Agent Cards extension for trust and payments | Agent 支付协议：签名卡片扩展 |
| Opacity | "Black-box collaboration" | Called agent's internals are hidden from caller | 不透明性：被调用方内部隐藏 |
| Input-required | "Task pause" | Lifecycle state when the agent needs more info | 输入要求：任务暂停等待更多信息 |

## Xem thêm 延伸阅读

- [a2a-protocol.org](https://a2a-protocol.org/latest/) Cấu chỉ A2A
  Trung ngữ翻译:权威 A2A 规范
- [a2aproject/A2A — GitHub](https://github.com/a2aproject/A2A) Các thực hiện và SDK tham chiếu
  Trung ngữ翻译:参考实现和 SDK
- [Linux Foundation — A2A launch press release](https://www.linuxfoundation.org/press/linux-foundation-launches-the-agent2agent-protocol-project-to-enable-secure-intelligent-communication-between-ai-agents) Tháng 6 năm 2025 chuyển giao quản trị
  Trung文翻译:2025 年 6 月治理转移
- [Google Cloud — A2A protocol upgrade](https://cloud.google.com/blog/products/ai-machine-learning/agent2agent-protocol-is-getting-an-upgrade) Bản đồ đường và động lực của đối tác
  Trung ngữ翻译:路线图和伙伴势头
- [Google Dev — A2A 1.0 milestone](https://discuss.google.dev/t/the-a2a-1-0-milestone-ensuring-and-testing-backward-compatibility/352258) v1.0 thông báo phát hành và hướng dẫn ngược
  Trung文翻译:v1.0 发行说明和向后兼容指南
