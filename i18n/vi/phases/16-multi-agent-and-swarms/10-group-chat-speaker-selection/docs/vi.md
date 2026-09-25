# Nhóm trò chuyện và chọn người nói 群聊 选择 发言人

> Phong phối trò chuyện chia sẻ đặt N đại lý vào một cuộc trò chuyện; một chức năng chọn (LLM, round-robin, hoặc tùy chỉnh) chọn ai nói tiếp theo. Đây là kiểu nguyên mẫu của cuộc trò chuyện đa đại lý nổi lên  đại lý không biết vai trò của họ trong biểu đồ tĩnh, họ chỉ phản ứng với hồ bơi chung. AutoGen GroupChat và AG2 GroupChat là các thực hiện tham chiếu: ngữ nghĩa GroupChat của AutoGen v0.2 được bảo tồn trong ga AG2; AutoGen v0.4 viết lại nó như một mô hình diễn viên do sự kiện thúc đẩy. Microsoft đưa AutoGen vào chế độ bảo trì vào tháng 2 năm 2026 và sáp nhập nó với Semantic Kernel vào Microsoft Agent Framework (RC tháng 2 năm 2026). GroupChat nguyên thủy tồn tại trong cả AG2 và Microsoft Agent Framework  học nó một lần, sử dụng nó ở mọi nơi.

> **【中文解读】**Chương trình này giới thiệu nhóm trò chuyện người phát biểu chọn nhiều đại lý trong cuộc thảo luận quyết định ai phát biểu, thời gian phát biểu cơ chế.

> **【拓展：group chat speaker selection→具体应用】**群聊发言人选择是多 Agent 讨论中的关键问题谁发言、什么时候发言、发言多久──三种主要策略:(1) 轮流制按固定顺序发言;(2) 相关性制最相关的 Agent 发言;(3) 仲裁制一个专门协调员决定谁发言──AutoGen's GroupChat sử dụng LLM 作为仲裁者──


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 16 · 04 (Primitive Model) | **前置知识:** Phase 16 · 04 (Primitive Model)
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**学本节前请先掌握:Phase 16·04(原语模型) 、AutoGen 基础──群聊 = N 个 Agent 共享一个对话池,发言人选择决定谁说话──
>  **【类比】**群聊发言人选择 = "chủ tịch hội nghị"──轮流制 = 圆桌按序;相关性制 = 谁懂谁说;仲裁制 = Chủ tịch chỉ định──AutoGen GroupChat dùng LLM khi chủ tịch 成本高但灵活──2026 chú ý:AutoGen đã được Microsoft hợp nhất với Microsoft Agent Framework,AG2 là một nhánh cộng đồng, cả hai đều giữ lại GroupChat 原语──

##                                                                                                                                                                                                                                                               

Các biểu đồ tĩnh (LangGraph) rất tốt khi workflow được biết. Các cuộc trò chuyện thực sự không phải là tĩnh: đôi khi người lập trình hỏi người xem, đôi khi người nghiên cứu, đôi khi người viết. Hardcoding mỗi lần giao hàng có thể tạo ra một vụ nổ cạnh. Bạn muốn * đại lý phản ứng với một bể chia sẻ*, với một số chức năng quyết định ai nói tiếp theo.

> 静态图 (图) 长图) trong dòng công việc đã biết rất tốt. 实话 không phải là静态. Có lúc bộ lập trình hỏi người xem, có lúc hỏi nhà nghiên cứu, có lúc hỏi tác giả.

Vấn đề nổ cạnh là thực tế: một hệ thống 5 đại lý với tất cả các giao dịch có thể có 25 cạnh hướng. Thêm một đại lý thứ sáu và bạn có 36. Cách tiếp cận biểu đồ không mở rộng cho các cuộc trò chuyện mới nổi; bạn cần một hồ bơi.

> Vấn đề nổ bên là thực:带所有可能交接的 5 Agent 系统有25条有向边──添加第六 Agent 就有36条──图方法不能扩展到现有的对话;你需要池──

Đó chính xác là những gì AutoGen GroupChat làm.

> Đó là điều mà AutoGen GroupChat đã làm.

## Khái niệm cốt lõi

### Hình dạng

```
              ┌─── shared pool ────┐
              │   m1  m2  m3  ...  │
              └─────────┬──────────┘
                        │ (everyone reads all)
      ┌───────┬─────────┼─────────┬───────┐
      ▼       ▼         ▼         ▼       ▼
    Agent A  Agent B  Agent C  Agent D  Selector
                                           │
                                           ▼
                                  "next speaker = C"
```

Mỗi đại lý đều thấy mọi thông điệp, và mỗi lượt họ gọi một chức năng chọn để chọn ai nói tiếp theo.

> Mỗi đại lý nhìn thấy mỗi bài báo. Mỗi vòng sử dụng các hàm chọn để chọn người phát biểu tiếp theo.

Các nhóm chia sẻ thông minh đầy đủ là cả hai điểm mạnh và điểm yếu của GroupChat. Năng lực: bất kỳ đại lý nào có thể phản ứng với bất cứ điều gì mà bất kỳ ai nói. Điểm yếu: sau 20 lượt, bối cảnh của mỗi đại lý là rất lớn, tốn kém và mỏng.

> 完全透明池既是Grouppchat的优点也是弱点. 优点: Bất kỳ Đại diện nào cũng có thể phản ứng bất cứ điều gì mà bất cứ ai nói. 弱点:20 轮后, mỗi Đại diện có những biện pháp giảm thiểu: cho mỗi Đại diện 投影范围视图 (Lớp 15) hoặc提前终止.

### Ba hương vị chọn lọc

**Round-robin.**Chuyện cố định. Định nghĩa. Scales linearly in N nhưng bỏ qua ngữ cảnh  một coder nhận được lượt ngay cả khi chủ đề là đánh giá pháp lý.

> **轮询。**固定循环──确定性──按N 线性扩展但忽略上下文即使主题是法务审阅,编码器也能获得发言权──

**LLM-selected.**Một cuộc gọi đến một LLM đọc hồ sơ gần đây và trả lại người phát biểu tiếp theo tốt nhất. Biết bối cảnh nhưng chậm: mỗi lượt thêm một cuộc gọi LLM.

> **LLM 选择。**调用 LLM 读取近期并返回最佳下文发言人──上下文感知但慢: mỗi vòng tăng thêm một lần LLM 调用──AutoGen 的默认选择──

**Custom.**Một chức năng Python với bất kỳ logic nào bạn muốn. điển hình: LLM được chọn với các quy tắc trở lại (ví dụ, "luôn cho người xác minh sự xoay sau người lập trình").

> **自定义。**Một hàm Python, sử dụng bất kỳ logic nào bạn muốn.

### ConversableAgent API

```
agent = ConversableAgent(
    name="coder",
    system_message="You write Python.",
    llm_config={...},
)
chat = GroupChat(agents=[coder, reviewer, tester], messages=[])
manager = GroupChatManager(groupchat=chat, llm_config={...})
```

`GroupChatManager`khi một đại lý hoàn thành một lượt, người quản lý gọi cho người chọn, người đó trả lại đại lý tiếp theo. vòng lặp tiếp tục cho đến khi một điều kiện chấm dứt.

> `GroupChatManager`持有选择器──当代理 完成一轮时,管理者调用选择器,返回下一个代理──循环继续直到终止条件──

Chức năng chọn lọc là cốt lõi của GroupChat. Thay đổi nó, thay đổi phong cách dàn nhạc. chọn tròn-robin = xác định. chọn LLM = thích ứng. chọn tùy chỉnh = bất kỳ quy tắc nào bạn mã hóa.

> 选择器函数 là cốt lõi của GroupChat. 换掉它,改变编排风格. 轮询选择器 = 确定性. LLM 选择器 = 自适应.

### Tháo dỡ

Ba mô hình phổ biến:

> 三种常见模式:

- **Max rounds.**Tấm bốc cứng trên vòng hoàn toàn.
  Trung ngữ翻译:**最大轮数。**总轮数的硬上限──
- **"TERMINATE" token.**Các đại lý có thể phát ra một thông điệp của một người lính canh; người quản lý dừng lại khi một người xuất hiện.
  Trung ngữ翻译:**"TERMINATE" 标记。**Trưởng có thể gửi thông điệp; người quản lý sẽ dừng lại khi xuất hiện.
- **Goal-reached check.**Một bộ xác minh nhẹ chạy mỗi lượt và dừng cuộc trò chuyện khi hoàn thành.
  Trung ngữ翻译:**目标达成检查。**轻量级验证人每轮运行和完成时停止聊天──

### AutoGen -> AG2 chia và Microsoft Agent Framework hợp nhất
### Hạt gốc: các cành và hợp nhất

Đầu năm 2025, Microsoft bắt đầu viết lại AutoGen (v0.4) lớn xung quanh mô hình diễn viên dựa trên sự kiện. Cộng đồng đã chia rẽ GroupChat của AutoGen v0.2 thành AG2, bảo tồn API mà người dùng đầu tiên đã tích hợp.

> Đầu năm 2025, Microsoft bắt đầu viết lại một loạt các mô hình về AutoGen (v0.4) để bao quanh các diễn viên thúc đẩy sự kiện.

Vẻo là cần thiết bởi vì v0.4 phá vỡ tương thích ngược theo những cách cơ bản. AG2 giữ nguyên bản gốc `GroupChat`- `ConversableAgent`, và`GroupChatManager`API ổn định, trong khi v0.4 giới thiệu các nguyên thủy mới dựa trên sự kiện. Cả hai dòng đều được duy trì tích cực từ năm 2026.

> Chia chia là cần thiết, vì v0.4 trong các khía cạnh cơ bản phá hủy khả năng tương thích phía sau.`GroupChat``ConversableAgent`和 `GroupChatManager`API 稳定, trong khi v0.4  giới thiệu sự kiện mới thúc đẩy nguyên ngữ.

Vào tháng 2 năm 2026, Microsoft đã thông báo AutoGen sẽ chuyển sang chế độ bảo trì, với mô hình diễn viên dựa trên sự kiện được sáp nhập vào **Microsoft Agent Framework**(RC tháng 2 năm 2026, bây giờ hợp nhất với Semantic Kernel). Khái niệm GroupChat tồn tại trong cả hai đường ray; chi tiết thực hiện khác nhau. AG2 là phương thức ưu tiên trên dòng cho mã tương thích v0.2.

> 2026 年 2 月, Microsoft tuyên bố AutoGen 进入维护模式,事件驱动 actor 模型合并到 **Microsoft Agent Framework**(RTC, hiện đã có với Kernel Semantic 合并) ――GroupChat 概念在两个轨道中存活;实现细节不同──AG2 是 v0.2 兼容代码的首选上游──

Bài học: API bề mặt tồn tại hơn khung. Mã được viết chống lại GroupChat API của AutoGen v0.2 vào năm 2024 vẫn chạy không thay đổi thông qua AG2 vào năm 2026.

> Học tập:API 表面比框架持久──2024 năm đối với AutoGen v0.2 GroupChat API 编写的代码在 2026年通过AG2 仍然不变运行──框架变化;原语(共享池 + 选择器) 不变──押注原语──

### Khi GroupChat phù hợp

- **Emergent conversations.**Bạn không muốn pre-thường dây tất cả các khả năng tiếp theo loa.
  Trung ngữ翻译:**涌现对话。**Bạn không muốn kết nối trước với người phát ngôn tiếp theo của mỗi người.
- **Role-mixing tasks.**Coder hỏi nhà nghiên cứu, nhà nghiên cứu hỏi lưu trữ viên, lưu trữ viên hỏi coder trở lại.
  Trung ngữ翻译:**角色混合任务。**编码器问研究员,研究员问档案员,档案员反问编码器──流程不是DAG──
- **Exploratory problem-solving.**Hãy nghĩ "cuộc họp đột phá" chứ không phải "các đường dây tập hợp".
  Trung ngữ翻译:**探索性问题解决。**想想"头脑风暴会议", thay vì "装配线"

### Khi nó thất bại

- **Strict determinism.**Các lựa chọn của LLM có thể không phù hợp, cùng một prompt, chạy khác nhau, diễn giả tiếp theo khác nhau.
  Trung ngữ翻译:**严格确定性。**LLM 选择器可能不一致──相同提示,不同运行,不同下一个发言者──
- **Sycophancy cascades.**Các đặc vụ sẽ tiếp cận những người nói với sự tự tin nhất.
  Trung ngữ翻译:**谄媚级联。**Trưởng lý 屈从于最自信的发言人──明确反提示──
- **Context bloat.**Mỗi đại lý đọc mọi tin nhắn; sau 10 lượt ngữ cảnh là rất lớn. Sử dụng dự đoán (Dạy học 15) để phạm vi xem.
  Trung ngữ翻译:**上下文膨胀。**Mỗi đại lý 读取每条消息;10轮后上下文巨大──使用投影(Lớp 15) để hạn chế视图──
- **Hot speakers.**Một đại lý thống trị cuộc trò chuyện vì người chọn ưu tiên đặc biệt của mình.
  Trung ngữ翻译:**热发言者。**Một đại lý chủ đạo đối thoại, vì các lựa chọn bị chuyển hướng sang chuyên长.

### Nhóm trò chuyện với người giám sát

Tương tự nguyên thủy, mặc định khác nhau:

> 相同原语,不同默认值:

- Giám đốc: một đại lý lập kế hoạch và những người khác thực hiện.
  Trung文翻译:监督者:一个代理 规划,其他执行──选择器是"问规划者做什么──"
- Group chat: tất cả các đại lý đều là đồng nghiệp; chọn là một chức năng trên hồ bơi chung.
  Trung ngữ翻译:群聊:所有 Agent 是对等的; chọn器 是共享池上的函数──

Cả hai đều sử dụng bốn nguyên thủy từ Bài học 04. Các trò chuyện nhóm mặc định đến dàn nhạc LLM được chọn và trạng thái chia sẻ toàn bộ.

> 两者都使用课04的四个原语──群聊默认使用 LLM 选择的编排和全池共享状态──

Sự lựa chọn giữa giám sát viên và trò chuyện nhóm chủ yếu là về *người nắm giữ kế hoạch*. giám sát viên: một đại lý sở hữu kế hoạch và đại diện. trò chuyện nhóm: kế hoạch là ngầm, xuất hiện từ cuộc trò chuyện.

> Sự lựa chọn giữa giám sát viên và nhóm trò chuyện chủ yếu là về * ai có kế hoạch *。 giám sát viên: một đại lý  sở hữu kế hoạch và ủy nhiệm;; nhóm trò chuyện: kế hoạch là ẩn hình, xuất hiện trong cuộc trò chuyện;. người trước có thể kiểm soát hơn; người sau có thể sống hơn。

## Hãy xây dựng nó.
```figure
swarm-speaker
```

## Hãy xây dựng nó

`code/main.py`thực hiện một GroupChat từ đầu trong stdlib. ba đại lý (coder, kiểm tra viên, quản lý), round-robin và LLM lựa chọn biến thể, và một chấm dứt trên một `TERMINATE`- Đồ tín hiệu.

> `code/main.py`Sử dụng các tiêu chuẩn từ đầu để thực hiện một GroupChat.`TERMINATE`标记上终止──

Demo in bản ghi lại cuộc trò chuyện cộng với dấu vết quyết định của người chọn cho cả hai biến thể.

> 演示印对话记录以及两种变体的选择器决策追踪──

## Hãy sử dụng nó để thực hiện

`outputs/skill-groupchat-selector.md`cấu hình một bộ chọn GroupChat cho một nhiệm vụ nhất định  round-robin vs LLM-selected vs custom, và các đầu vào của bộ chọn (tin nhắn gần đây, đặc biệt của đại lý, đếm lượt) để sử dụng.

> `outputs/skill-groupchat-selector.md`Để xác định nhiệm vụ định vị GroupChat  chọn器轮询 vs LLM  chọn lựa vs tự định nghĩa,以及使用什么选择器输入(最近消息、Agent 专长、轮次计数) ⋅

## Chuyển nó đi.

Danh sách kiểm tra:

> 检查清单:

- **Max rounds cap.**Luôn luôn. 10-20 cho các nhiệm vụ điển hình.
  Trung ngữ翻译:**最大轮数上限。**总是使用──典型任务 10-20──
- **Speaker-balance metric.**Đường quay mỗi đại lý; cảnh báo khi mất cân bằng vượt quá ngưỡng.
  Trung ngữ翻译:**发言者平衡指标。**Theo dõi mỗi lần của các đại lý; khi không cân bằng vượt quá giá trị của cảnh sát.
- **Termination token.** `TERMINATE`hoặc một đại lý xác minh chuyên dụng.
  Trung ngữ翻译:**终止标记。** `TERMINATE`Hoặc là một đặc vụ kiểm chứng.
- **Projection or scoped memory.**Sau ~ 10 tin nhắn, hãy xem xét cung cấp cho mỗi đại lý chỉ một khung cảnh để ngăn chặn bùng phát ngữ cảnh.
  Trung ngữ翻译:**投影或范围内存。**Sau khoảng 10 thông tin, hãy xem xét cho mỗi đại lý chỉ một phạm vi quan sát để ngăn chặn sự bùng nổ trên.
- **Selector logging.**Đối với các biến thể được chọn LLM, ghi lại cả đầu vào của người chọn và sự lựa chọn của nó. Nếu không, việc gỡ lỗi là không thể.
  Trung ngữ翻译:**选择器日志。**Đối với LLM  chọn biến thể, ghi chọn器的输入和选择──否则调试不可能──

## Tập luyện bài tập

1. Đi chạy`code/main.py`So sánh cuộc trò chuyện trong vòng tròn-robin với LLM-chọn-được.
   Trung ngữ翻译:运行 `code/main.py`◊ So sánh các câu hỏi và các cuộc hội thoại trong ngành LLM.
2. Thêm một quy tắc "tối đa nói trên mỗi đại lý" vào bộ chọn.
   Trung ngữ翻译:在选择器中添加"每个代理最大发言次数"规则── nó ảnh hưởng đến hồ sơ như thế nào?
3. Thực hiện một kết thúc đạt mục tiêu: dừng khi người xem trả lại "được chấp thuận".
   Trung ngữ翻译:实现目标达成终止: Khi người xem trở lại "được chấp thuận" thì dừng lại.
4. Đọc các tài liệu ổn định AutoGen trên GroupChat.`GroupChatManager`- Tôi không biết.
   中文翻译:阅读 AutoGen 稳定文档中的 GroupChat。识别 `GroupChatManager`Sử dụng của tùy chọn tùy chọn:.
5. Đọc repo AG2 và so sánh GroupChat v0.2 của nó với phiên bản v0.4 dựa trên sự kiện.
   Trung文翻译:阅读 AG2 仓库并比较其 v0.2 GroupChat với v0.4 事件驱动版本──v0.4 添加了什么具体属性(吞吐量、容错、可组合性)?

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| GroupChat / 群聊 | "Agents in one chat room" / "一个聊天室中的 Agent" | Shared message pool + selector function. AutoGen / AG2 primitive. / 共享消息池 + 选择器函数。AutoGen / AG2 原语。 |
| Speaker selection / 发言者选择 | "Who talks next" / "谁下一个说话" | The function that picks the next agent. Round-robin, LLM-selected, or custom. / 选择下一个 Agent 的函数。轮询、LLM 选择或自定义。 |
| GroupChatManager / 群聊管理者 | "The meeting host" / "会议主持人" | AutoGen component that owns the selector and loops over turns. / 拥有选择器并循环轮次的 AutoGen 组件。 |
| ConversableAgent / 可对话 Agent | "The base agent" / "基础 Agent" | AutoGen base class; an agent that can send and receive messages. / AutoGen 基类；可以发送和接收消息的 Agent。 |
| Termination token / 终止标记 | "The 'stop' word" / "停止词" | Sentinel string (usually `TERMINATE`) that ends the chat. / 结束聊天的哨兵字符串（通常是 `TERMINATE`）。 |
| Hot speaker / 热发言者 | "One agent dominates" / "一个 Agent 主导" | Failure mode where the selector keeps picking the same agent. / 选择器持续选择同一 Agent 的失败模式。 |
| Context bloat / 上下文膨胀 | "Pool grows unbounded" / "池无限增长" | Each agent reads every prior message; context grows with turns. / 每个 Agent 读取每条先前消息；上下文随轮次增长。 |
| Projection / 投影 | "Scoped view" / "范围视图" | Role-specific view into the shared pool to prevent context bloat. / 角色特定的共享池视图以防止上下文膨胀。 |

## Xem thêm 延伸阅读

- [AutoGen group chat docs](https://microsoft.github.io/autogen/stable/user-guide/core-user-guide/design-patterns/group-chat.html) thực hiện tham chiếu
  中文翻译:AutoGen 群聊文档  参考实现
- [AG2 repo](https://github.com/ag2ai/ag2) cộng đồng AutoGen v0.2 tiếp tục
  中文翻译:AG2 仓库  社区 AutoGen v0.2 延续
- [Microsoft Agent Framework docs](https://microsoft.github.io/agent-framework/) người kế nhiệm hợp nhất, RC tháng 2 năm 2026
  Trung文翻译:Microsoft Agent Framework 文档  合并后的继任者,2026 年 2 月 RC
- [Microsoft Agent Framework docs](https://learn.microsoft.com/en-us/agent-framework/) người kế nhiệm hợp nhất, RC tháng 2 năm 2026
- [AutoGen v0.4 release notes](https://microsoft.github.io/autogen/stable/) chi tiết viết lại mô hình diễn viên dựa trên sự kiện
  中文翻译:AutoGen v0.4 发布说明  事件驱动演员 模型重写详情
