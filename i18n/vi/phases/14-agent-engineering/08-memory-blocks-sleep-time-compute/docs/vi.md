# Khóa trí nhớ và tính toán thời gian ngủ (Letta) 記憶块与休眠計算 (Letta)
# Chế độ ghi nhớ và tính toán thời gian ngủ

> Các bộ nhớ chức năng khác nhau ngăn chặn mô hình có thể chỉnh sửa trực tiếp, và một đại lý thời gian ngủ hợp nhất bộ nhớ không đồng bộ trong khi đại lý chính là vô hiệu.

> **【中文解读】**MemGPT trong năm 2024 trở thành Letta. Sự tiến triển năm 2026 đã tăng thêm hai ý tưởng: mô hình có thể trực tiếp chỉnh sửa các khối ký ức chức năng phân tán, và trong chủ yếu Agent 空时异步合并 ký ức. Đây là cách mà ký ức sẽ mở rộng ra ngoài cuộc trò chuyện đơn lẻ.

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 07 (MemGPT) | **前置知识:** Phase 14 · 07 (MemGPT)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Mục tiêu học tập

- Tên gọi ba cấp độ bộ nhớ Letta sử dụng (cốt lõi, nhớ lại, lưu trữ) và vai trò của mỗi.
  Trung文翻译:说出 Letta 使用的三个记忆层级 (core, recall, archive)及各自作用.
- Giải thích mô hình khối bộ nhớ: khối người, khối Persona và khối được người dùng xác định như các đối tượng được đánh máy hạng nhất.
  Trung文翻译:解释记忆块模式:Human 块、Persona 块和用户自定义块作为一等类型化对象──
- Mô tả tính toán thời gian ngủ là gì, tại sao nó nằm ngoài con đường quan trọng, và tại sao nó có thể chạy một mô hình mạnh hơn so với tác nhân chính.
  Trung ngữ翻译:描述休眠计算是什么,为什么它不在关键路径之外,为什么它能运行比主代理更强的模型.
- Thực hiện một vòng lặp hai đại lý được kịch bản trong đó một đại lý chính phục vụ các phản ứng và một đại lý thời gian ngủ hợp nhất các khối giữa các lượt.
  Trung文翻译:实现一个脚本化的双代理循环,主代理提供响应,休眠代理 在轮次间合并块――

## Vấn đề  vấn đề giới thiệu

MemGPT (Dạy 07) đã giải quyết dòng chảy kiểm soát bộ nhớ ảo. Ba vấn đề sản xuất xuất xuất ra:

> MemGPT (第 7 课) giải quyết được dòng kiểm soát trong bộ nhớ ảo.

1. **Latency.**Mỗi hoạt động trong bộ nhớ nằm trên đường dẫn quan trọng. Nếu đại lý phải cắt, tóm tắt hoặc hòa giải trong khi người dùng chờ đợi, thời gian trễ đuôi sẽ nổ.
   Trung ngữ翻译:**延迟。**Mỗi hoạt động nhớ đều trên một đường chính. Nếu đại lý phải cắt 摘要 hoặc phối hợp khi người dùng chờ đợi,尾部延迟会爆炸.
2. **Memory rot.**Những tài liệu được tích lũy, những sự thật trái ngược vẫn còn, việc tìm lại bị ngập trong nội dung cũ.
   Trung ngữ翻译:**记忆腐化。**写入积累――矛盾的事实保留――检索被过时内容淹没――
3. **Structure loss.**Một kho lưu trữ phẳng không thể thể hiện "hình khối người luôn luôn trong prompt; khối Persona luôn trong prompt; khối Task thay đổi mỗi phiên".
   Trung ngữ翻译:**结构丢失。**平的归档存储不能表达"Human 块始终在提示中;Persona 块始终在提示中;Task 块按会话交换――"

Letta (letta.com) là tên nền tảng dự án MemGPT ban đầu được thông qua vào năm 2024  mô hình của giấy giữ tên MemGPT  và viết lại Letta V1 năm 2026 là một bước sau, riêng biệt.

> Letta (Letta.com) là một phần của năm 2026 tái viết.

> **【中文解读】**記憶塊 (memory block) 和休眠計算 (休眠計算) là hai phương pháp tối ưu hóa của MemGPT/Letta. 記憶塊 là một phần nhỏ của phần mềm trên, tương tự như một trang trong bộ nhớ, được sử dụng để kiểm soát chi tiết các loại thông tin trong cửa sổ dưới.

> **【拓展：Letta 的演进】**Letta(mở thành MemGPT) trong các diễn biến 2024-2025 đã đưa ra hai khái niệm quan trọng về khối trí nhớ và khối ngủ tính toán.

>  **【前置】**必须先过阶段14·07(MemGPT) 本节是它的直接延续──如果不理解 MemGPT的"主上下文与外部上下文"两层模型,那么 Letta的三层(core/recall/archival)扩展会把你搞──

## Khái niệm cốt lõi

### Ba tầng

| Tier | Scope | Where it lives | Written by |
|------|-------|----------------|------------|
| 层级 | 范围 | 存储位置 | 写入者 |
| Core | Always visible | Inside the main prompt | Agent tool call + sleep-time rewrites / Agent 工具调用 + 休眠重写 |
| Recall | Conversation history | Retrievable | Automatic turn logging / 自动轮次日志 |
| Archival | Arbitrary facts | Vector + KV + graph | Agent tool call + sleep-time ingest / Agent 工具调用 + 休眠摄取 |

Core là lõi MemGPT. nhớ là bộ đệm trò chuyện với đuôi bị tẩy ra. lưu trữ là cửa hàng bên ngoài. chia tách làm sạch quá tải hai cấp của MemGPT.

> Core là lõi của MemGPT. Khoan dung là bộ phận chia sẻ chia sẻ của bộ phận chia sẻ chia sẻ.

### Các khối bộ nhớ

Một khối là một phần được gõ, bền vững, có thể chỉnh sửa của tầng cốt lõi.

> 块 là loại hóa, duy trì, edit được phân vùng của tầng cốt lõi.

- **Human block** những sự thật về người dùng (tên, vai trò, sở thích, mục tiêu).
  Trung ngữ翻译:**Human 块** Về thực tế người dùng (姓名,角色,偏好,目标)
- **Persona block** khái niệm về bản thân của đại lý (tình danh, giọng nói, hạn chế).
  Trung ngữ翻译:**Persona 块**Agent's ego concept (tự nhận thức của mình)

Letta tổng quát hóa thành các khối được người dùng định nghĩa tùy ý: a `Task`khối cho mục tiêu hiện tại, một `Project`khối cho các dữ liệu cơ sở mã, một `Safety`khối cho các hạn chế cứng. Mỗi khối có một`id`- `label`- `value`- `limit`(chế độ giới hạn), `description`(vì vậy mô hình biết khi nào để chỉnh sửa nó).

> Letta 泛化为任意用户定义块:用于当前目标的 `Task`块、用于代码库事实 `Project`块 、 được sử dụng trong các khối cứng `Safety`Mỗi khối có`id``label``value``limit`(字符上限)`description`(让模型知道何时编辑它)

Các khối có thể chỉnh sửa thông qua bề mặt công cụ:

> 块 thông qua công cụ tiếp xúc có thể edit:

- `block_append(label, text)`
  Trung ngữ翻译:`block_append(label, text)`向块追加文本。
- `block_replace(label, old, new)`
  Trung ngữ翻译:`block_replace(label, old, new)`替换块中的文本──
- `block_read(label)`
  Trung ngữ翻译:`block_read(label)`读取块内容──
- `block_summarize(label)` ngưng tụ một khối gần giới hạn của nó.
  Trung ngữ翻译:`block_summarize(label)`                                                                                                                                                                                                                                                              

### Lượng ngủ

Letta 2025 bổ sung: chạy một đại lý thứ hai trong nền, ra khỏi con đường quan trọng.`learned_context`thành các khối chung, và hợp nhất hoặc vô hiệu hóa hồ sơ lưu trữ.

> 2025 Letta's new addition function: ếch hành trình thứ hai của Letta, không có đường lối quan trọng trên.`learned_context`写入共享块,并合并或使归档记录失效──

Các tính năng bị phá vỡ:

> 随之产生的特性:

- **No latency cost.**Các phản ứng chính không chờ đợi cho các hoạt động bộ nhớ.
  Trung ngữ翻译:**无延迟成本。**主响应不等待记忆操作――
- **Stronger model allowed.**Máy tác dụng thời gian ngủ có thể là một mô hình đắt hơn, chậm hơn vì nó không bị hạn chế bởi độ trễ.
  Trung ngữ翻译:**允许更强的模型。**休眠代理 có thể là một mô hình đắt hơn, chậm hơn, vì nó không bị ràng buộc bởi sự chậm trễ.
- **Natural consolidation window.**Dedup, tóm tắt, vô hiệu hóa các sự kiện mâu thuẫn khi người dùng không chờ đợi.
  Trung ngữ翻译:**天然的合并窗口。**Trong khi người dùng không chờ đợi, hãy tập lại, rút ngắn, làm cho sự thật bất hợp lý không hiệu quả.

Hình dạng phù hợp với cách con người làm việc: bạn làm nhiệm vụ, bạn ngủ trên nó, trí nhớ dài hạn ổn định qua đêm.

>  **【类比】**Giống như người làm việc trong đêm:白天你(主代理) bận đáp ứng khách hàng, văn phòng(主上下文)堆满今天会议记录、文件、咖啡杯;晚晚清洁工(睡眠时间代理)进来擦桌子、归档文件、把"明天要跟进的事"贴到便利贴上(写入人/任务块) ・・・第二天你上班,看整洁待的桌面和清晰的办公清单――**关键**: Cleanpie工可以慢一点、贵一点(使用更强的模型), vì khách hàng không chờ đợi.

> Mô hình này phù hợp với cách làm của con người: Bạn làm nhiệm vụ, bạn ngủ, nhớ dài trong đêm.

### Letta V1 và lý luận bản địa
### Lý luận bản địa

Letta V1 (`letta_v1_agent`, 2026) đã bị phá vỡ `send_message`/những nhịp tim và đường thẳng `Thought:`Các mã thông báo ủng hộ lý luận bản địa. Các API phản ứng (OpenAI) và các API tin nhắn với tư duy mở rộng (Anthropic) phát ra lý luận trên một kênh riêng biệt, đi qua các lượt (được mã hóa trên các nhà cung cấp trong sản xuất).

> Letta V1`letta_v1_agent`,2026) đã bỏ qua`send_message`/ tâm nhảy và trong `Thought:`token,转而使用原生推理. Response API(OpenAI) 和带扩展思考的消息 API(Anthropic) trên một đường dẫn độc lập, trên một đường dẫn xuất推理, trên một đường dẫn xuyên vòng lặp qua một đường dẫn truyền (在生产环境中跨供应商加密)  Control loop vẫn là ReAct.

### Khi mô hình này đi sai

> ️ **【易错点】**"静默漂移" là lỗi đáng sợ nhất trong Letta 部署: đại lý ngủ ở hậu台 đã thay đổi Persona 块 (ví dụ như "始终使用中文回复"改成中英文混用), nhưng đại lý không biết.**后果**Người dùng tìm thấy hành vi của đại lý thay đổi nhưng không tìm ra lý do vì nhật ký thoại chỉ ghi lại xuất khẩu của đại lý chủ nhân.**一行修复**: Mỗi lần ngủ 写入后版本化块 内容, và trong vòng tiếp theo của chủ nhân 里注入" kể từ lần trước 变化:..." của các khác biệt 提示。

- **Block bloat.**Không có tận`block_append`Đưa một đoạn tổng kết trước khi viết mà đẩy qua nắp.
  Trung ngữ翻译:**块膨胀。**无限的`block_append`快速达到上限──在超越上限的写入之前接入块摘要器──
- **Silent drift.**Thuốc ngủ viết lại một khối và đại lý chính không bao giờ nhận ra.
  Trung ngữ翻译:**静默漂移。**休眠 代理 重写块但主代理 从未注意到──版本化块并在轨迹中显示差异──
- **Poisoned consolidation.**Thuốc ngủ xử lý nội dung có thể tiếp cận được kẻ tấn công vào lõi. Bài học 27 cũng áp dụng cho bề mặt ngủ.
  Trung ngữ翻译:**投毒合并。**休眠代理将攻击者可达的内容处理进核心. 第27 课也适用于休眠接口.

> 🤔 **【困惑】**Q: Thuốc thời gian ngủ sử dụng mô hình mạnh hơn sẽ không đắt hơn sao? Tại sao là tiết kiệm tiền thay vì đốt tiền? A: Xem thời gian quy mô. Thời gian ngủ không nằm trong các tuyến đường quan trọng, có thể chọn thời gian thấp nhất (như 3 giờ sáng) sử dụng API hàng rẻ hơn (OpenAI)**避开了关键路径的高价** Đại lý chủ  phải sử dụng phát trực tuyến + cao ưu tiên, đơn giá là 2-3 lần của lô.

## Hãy xây dựng nó.
```figure
memory-blocks
```

## Hãy xây dựng nó

`code/main.py`thực hiện:

> `code/main.py`实现:

- `Block` ID, nhãn, giá trị, giới hạn, mô tả.
  Trung ngữ翻译:`Block`id、label、value、limit、description──
- `BlockStore` CRUD + `near_limit(label)`- Thợ giúp.
  Trung ngữ翻译:`BlockStore`CRUD + `near_limit(label)`辅助方法――
- Hai nhân viên kịch bản  `PrimaryAgent`phục vụ một lượt, `SleepTimeAgent`kết hợp giữa các vòng.
  Trung文翻译:两个脚本 Agent`PrimaryAgent`提供轮次,`SleepTimeAgent`Trong vòng lần thứ hai
- Một dấu vết cho thấy cuộc trò chuyện ba vòng với Block viết, cộng với một thẻ ngủ thời gian tóm tắt một block và vô hiệu hóa một sự thật cũ.
  Trung ngữ翻译:展示三轮对话带块写入的轨迹,加加压缩块和使过时事实失效的休眠处理.

Đi đi.

> 运行:

```
python3 code/main.py
```

Bản ghi cho thấy sự chia rẽ: các lượt đầu tiên nhanh và tạo ra các bài viết thô; con đường ngủ nhỏ gọn và làm sạch.

> 转录记录显示分工: 主轮次快速产生原始写入;休眠处理压缩和清理──

## Hãy sử dụng nó để thực hiện

- **Letta**(letta.com) cho việc thực hiện tham chiếu. tự lưu trữ hoặc đám mây quản lý.
  Trung ngữ翻译:**Letta**(letta.com) để làm việc
- **Claude Agent SDK skills**như kiến thức hình khối  một kỹ năng là một tên, phiên bản, có thể lấy lại khối hướng dẫn mà đại lý tải theo yêu cầu.
  Trung ngữ翻译:**Claude Agent SDK skills**作为块状知识技能是命名的,版本化的,检查的指令块,Agent 按需加载,
- **Custom builds**cho các nhóm muốn kiểm soát backend lưu trữ. sử dụng hợp đồng Letta API để bạn có thể di chuyển sau đó.
  Trung ngữ翻译:**自定义构建** thích hợp với những người muốn kiểm soát lưu trữ hậu端 của nhóm.

## Chuyển nó đi.

`outputs/skill-memory-blocks.md`tạo ra một hệ thống khối hình Letta với các cái nén thời gian ngủ cho bất kỳ thời gian chạy nào, bao gồm các quy tắc an toàn và dây dẫn dẫn.

> `outputs/skill-memory-blocks.md`Để bất kỳ hoạt động nào tạo ra Letta hình dạng hệ thống khối,带休眠子, quy tắc an toàn và liên kết trích dẫn.

## Tập luyện bài tập

1. Thêm một `block_summarize`công cụ thay thế giá trị khối bằng một bản tóm tắt được tạo bởi mô hình khi `near_limit`Thâm số kích hoạt nào giảm thiểu cả cuộc gọi tổng kết và quá tải khối?
   Trung ngữ翻译:添加 `block_summarize`工具, trong `near_limit`返回 true 时使用模型生成的摘要替换块值──哪个触发值最小化摘要调用和块溢出?
2. Thực hiện thời gian ngủ giảm trên lưu trữ: hai ghi chép có văn bản có quá 90% token chồng chéo sụp đổ đến một.
   Trong khi đó, các công cụ này được sử dụng để xử lý các sản phẩm trong quá trình xử lý.
3. Các khối phiên bản. trên mỗi ghi chép viết giá trị cũ và một sự khác biệt.`block_history(label)`để các nhà điều hành có thể gỡ lỗi "tại sao đại lý quên X".
   Trung文翻译:版本化块──每次写入记录旧值和差异──暴露 `block_history(label)`Làm cho nó có thể kiểm tra tại sao đại lý quên X?
4. Hãy đối xử với các nhân viên ngủ như những nhà văn không tin cậy. Khi họ chạm vào khối Persona hoặc an toàn, cần phải xem xét của nhân viên thứ hai trước khi thực hiện.
   Trung văn翻译:将休眠 代理视为不可信写入者──当它们碰到个体或安全块时,提交前需要第二个代理 审查──
5. Port ví dụ để sử dụng Letta API (`letta_v1_agent`(v. 5). Những thay đổi nào trong khuôn mẫu khối, và lý luận bản địa thay đổi hình dạng dấu vết như thế nào?
   Trung文翻译:将示例移植为使用 Letta API`letta_v1_agent`(■) Các mô hình khối đã thay đổi như thế nào?

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Memory block | "Editable prompt section" / "可编辑提示分区" | Typed, persistent, LLM-editable segment of core memory / 类型化、持久化、LLM 可编辑的核心记忆段 |
| Human block | "User memory" / "用户记忆" | Facts about the user, pinned in core / 关于用户的事实，固定在 core 中 |
| Persona block | "Agent identity" / "Agent 身份" | Self-concept, tone, constraints, pinned in core / 自我概念、语气、约束，固定在 core 中 |
| Sleep-time compute | "Async memory work" / "异步记忆工作" | Second agent doing consolidation off the critical path / 第二个 Agent 在关键路径之外做合并 |
| Core / Recall / Archival | "Tiers" / "层级" | Three-layer memory split: always-visible / conversation / external / 三层记忆拆分：始终可见 / 对话 / 外部 |
| Block limit | "Cap" / "上限" | Character limit per block; forces summarization / 每个块的字符限制；强制摘要 |
| Native reasoning | "Thinking channel" / "思考通道" | Provider-level reasoning output, not prompt-level `Thought:` / 提供商级推理输出，非提示级 `Thought:` |
| Learned context | "Sleep output" / "休眠输出" | Facts the sleep-time agent writes into shared blocks / 休眠 Agent 写入共享块的事实 |

## Xem thêm 延伸阅读

- [Letta, Memory Blocks blog](https://www.letta.com/blog/memory-blocks) mô hình khối
  Trung ngữ翻译:Letta 记忆块博客块模式。
- [Letta, Sleep-time Compute blog](https://www.letta.com/blog/sleep-time-compute) Hợp nhất đồng thời
  Trung文翻译:Letta 休眠计算博客异步合并──
- [Letta, Rearchitecting the Agent Loop](https://www.letta.com/blog/letta-v1-agent) viết lại lý luận bản địa
  Trung文翻译:Letta 重建 Agent 循环博客原生推理重写。
- [Packer et al., MemGPT (arXiv:2310.08560)](https://arxiv.org/abs/2310.08560) nguồn gốc
  Trung ngữ翻译:MemGPT 论文起源。
