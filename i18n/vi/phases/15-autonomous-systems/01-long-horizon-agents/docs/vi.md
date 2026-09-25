# Sự chuyển đổi từ chatbot sang đại lý đường dài từ chatbot đến đại lý đường dài

> Năm 2023, một chatbot trả lời một câu hỏi trong một lượt. Năm 2026, mô hình biên giới thường chạy từ vài phút đến vài giờ trên một nhiệm vụ. METR Time Horizon 1.1 điểm chuẩn (từ tháng 1 năm 2026) đặt Claude Opus 4.6 tại 14 giờ làm việc chuyên gia với độ tin cậy 50%. Khía chân trời đã tăng gấp đôi khoảng mỗi bảy tháng kể từ GPT-2. Mỗi giả định chúng tôi xây dựng xung quanh một lần trò chuyện  ngữ cảnh, niềm tin, các chế độ thất bại, chi phí, khả năng quan sát  phá vỡ khi chạy kéo dài lâu hơn bữa trưa.

> **【中文解读】**2023 Chatting机器人一轮回答一个问题――2026 年前沿模型可以花数分钟到数小时完成单任务――METR基准显示Claude Opus 4.6 能以50%可靠性完成14+ 小时的专家工作――时间线每7个月翻倍所有围绕单轮对话构建的假设 ((上下文、信任、失败模式、成本、可观测性) 都在运行时间超过午休时间后崩――

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, horizon-curve simulator) | **语言:** Python (标准库，horizon-curve 模拟器)
**Prerequisites:** Phase 14 · 01 (The Agent Loop) | **前置知识:** Phase 14 · 01 (The Agent Loop)
**Time:** ~45 minutes | **时间:** ~45 分钟

>  **【前置】**Học本节前请先掌握:Phase 14·01(Agent Loop) 理解 ReAct 循环;Phase 11·05(Context Engineering) 理解长程任务中的上下文管理;Phase 14·26(Fail Mode) 理解为什么长程任务失败概率高──本节是Phase 15 的开篇,奠定"长程 Agent ≠ 长天"的认知──

## Vấn đề  vấn đề giới thiệu

Một chatbot là một chức năng không có quốc gia. Nó lấy một lời nhắc, trả lời, và quên đi. Ngay cả các hệ thống được trang bị RAG được xây dựng cho đến năm 2024 cũng hành động theo cách này: họ lập kế hoạch bên trong một cửa sổ ngữ cảnh duy nhất, thực hiện một hành động và làm bề mặt kết quả.

> 聊天机器人是无状态函数──它接收提示、回回回复、然后忘记── ngay cả trong hệ thống RAG được xây dựng vào năm 2024 cũng vậy: chúng lập kế hoạch trong một cửa sổ đơn lẻ, thực hiện một động tác, sau đó trình bày kết quả──

Một đại lý tự trị khác nhau về mặt tự nhiên. Nó chạy một vòng lặp. Nó quyết định khi nào dừng lại. Nó chi tiêu tiền  mã thông báo thực sự, giờ GPU thực sự, tác dụng phụ thực sự  trong quá trình chạy. Các đại lý đường chân trời tăng cường mọi khía cạnh của điều này: chi phí tăng, xác suất lỗi tăng theo từng bước, và khoảng cách giữa những gì chúng ta có thể đánh giá và những gì được gửi mở rộng.

> Đơn vị tự do trong bản chất là khác nhau. Nó tự quyết định khi nào dừng lại. Trong quá trình vận hành, nó chi tiền. Đơn vị thực tế, thời gian GPU thực tế, hậu quả của hành động thực tế.

>  **【类比】**长程 Agent = 单人 14 小时开车从北京到上海──短程聊天机器人 = 下楼买菜──差异:(1) **燃料**14h 油费 vs 5 分钟;(2) **故障率**Chỉ có một bước 99% đáng tin cậy,70 bước sau chỉ còn lại 50% toàn bộ thành công;**纠错**买菜走错可重来,长途开错要重新规划;**观测**买菜不用GPS,长途必须实时监控──每项都需要新工具:成本预算(成本州长)、检查点(checkpoint)、回滚(rollback)、可观测性(可观测性)。

> ️ **【易错点】**长程 Agent 的 3 个坑:(1) **没设 token/成本预算**14h 任务可能烧光一个月 API 预算; dùng Phase 15·13 của chi phí thống đốc, siêu giá trị giết người──(2) **不设 checkpoint**10h 任务在第8h 崩, tất cả mọi công việc bị mất; mỗi N 步存状态,重启可续──(3) **没做 human-in-the-loop** quan trọng quyết định (发邮件、转账) tự động thực hiện,失控;关键节点暂停等审――

> **【中文解读】**聊天机器人是无状态函数接收提示、回回回复、然后忘记──自主代理 则不同: nó chạy vòng lặp、自主决定何时停止、在运行中花费真资源(Token、GPU 时间、副作用)。长程 代理 扩大所有这些问题:成本增长、每步错误概率增加、可评估与实际交付之间的差距扩大──

Các số liệu từ METR làm cho điều này trở nên cụ thể. Giữa GPT-2 và Claude Opus 4.6, chân trời thời gian (giãn dài nhiệm vụ của con người một mô hình hoàn thành với độ tin cậy 50%) tăng từ giây đến nửa ngày làm việc. Thời gian tăng gấp đôi gần bảy tháng. Nếu xu hướng kéo dài thêm một năm nữa, chân trời 50% chạm vào các nhiệm vụ đa ngày. Điều đó có chất lượng khác với bất cứ điều gì thời đại chatbot được thiết kế cho.

> Dữ liệu của METR đã thực hiện điều này. Trong GPT-2 và Claude Opus 4.6, thời gian tròn (đối với độ dài nhiệm vụ nhân loại hoàn thành đáng tin cậy 50%) tăng từ vài giây lên nửa ngày làm việc.

## Khái niệm cốt lõi

### METR Time Horizon, trong một đoạn

METR (ex-ARC Evals) phù hợp với một đường cong hậu cần để xác suất thành công nhiệm vụ so với hồ sơ thời gian hoàn thành của người chuyên nghiệp. Khía chân trời là giao lộ của đường cong đó với đường xác suất 50%. Bộ (HCAST, RE-Bench, SWAA) kéo dài từ 1 phút đến 8 giờ các nhiệm vụ chuyên gia trong phần mềm, mạng, nghiên cứu ML và lý luận chung. Kết quả là một quy mô mà nén khả năng thành một đơn vị duy nhất có thể đọc được bởi con người: "mô hình này có thể thực hiện loại nhiệm vụ mà một chuyên gia dành X giờ làm".

> METR(前 ARC Evals) đối với tỷ lệ thành công nhiệm vụ và các chuyên gia nhân loại hoàn thành thời gian đối với số lượng phù hợp với các đường cong logic.

### Điều gì thực sự vỡ khi chân trời lớn lên

- **Context.**Một thời gian chạy 14 giờ phát ra hàng trăm ngàn token quan sát, sản xuất công cụ và dấu vết suy luận. Bạn không còn có thể mang lại lịch sử nguyên liệu; bạn cần nén, các điểm kiểm soát và các cấp độ bộ nhớ (Phase 14 · 04-06).
  Trung ngữ翻译:**上下文。**14 小时运行会产生数十万代币的观察"",工具输出和推理轨迹"", bạn không thể mang lại lịch sử ban đầu; bạn cần phải nén, kiểm tra điểm và nhớ cấp độ (Phase 14 · 04-06) ").
- **Trust.**Ở một lượt bạn có thể đọc toàn bộ câu trả lời. ở 1.000 lượt bạn không thể. bề mặt đánh giá thay đổi từ "đọc đầu ra" đến "đánh giá quỹ đạo".
  Trung ngữ翻译:**信任。**Một vòng bạn có thể đọc toàn bộ câu trả lời. 1000 vòng bạn không thể.
- **Failure modes.**Các chạy ngắn thất bại vì giới hạn khả năng. Các chạy dài cũng thất bại vì các lỗ hổng hành vi phân tích và triển khai (xem dưới đây). Những thất bại này là vô hình cho đến khi chúng phức tạp.
  Trung ngữ翻译:**失败模式。**短运行因能力限制而失败──长运行因漂移,循环,奖励改和评估部署行为差而失败──这些失败在积累之前是不可见的──
- **Cost.**Một chạy tự trị 14 giờ của Claude Opus 4.6 với việc sử dụng đầy đủ công cụ có thể đốt cháy ngân sách của một tháng trò chuyện.
  Trung ngữ翻译:**成本。**Claude Opus 4.6 Trong hoàn toàn sử dụng công cụ 14 giờ tự hành có thể đốt cháy một tháng ngân sách. Không ngân sách và kết thúc mở cửa.
- **Observability.**Các hồ sơ yêu cầu không đủ, bạn cần điện đo cấp quỹ đạo, ngân sách hành động và mã thông báo của các loài cá thể để bắt được hành vi sai trái im lặng.
  Trung ngữ翻译:**可观测性。**Xin日志 không đủ. Bạn cần quỹ đạo, ngân sách hoạt động và token để bắt giữ những hành vi xấu của sự yên tĩnh.

### Thời gian gấp đôi và những gì nó có nghĩa là

Hiệu suất trước đây không đảm bảo gì, nhưng xu hướng này quá nhất quán để bỏ qua. METR phù hợp (tháng 3 năm 2025) đặt tăng gấp đôi tại 7 tháng trên các nhiệm vụ kiểu HCAST; cập nhật tháng 1 năm 2026 thu hẹp khoảng thời gian tin cậy nhưng không thay đổi độ nghiêng. Nếu độ nghiêng tiếp tục:

> 过去业绩不能保证未来,但趋势太过一致不能忽视──METR的拟合(3月2025年) sẽ tăng gấp đôi nhiệm vụ loại HCAST 7 个月;

- Khía vọng 2026 (Claude Opus 4.6 ngày hôm nay): ~ 14 giờ
  Trung ngữ翻译:2026 年时间线(今天的克劳德奥普斯 4.6):约 14 小时
- Khoảng cảnh 2027 (ký hiệu): ~ 48 giờ
  Trung文翻译:2027 年时间线(预测): khoảng 48 小时
- Khoảng cảnh 2028 (ký hiệu): ~ 1 tuần
  Trung文翻译:2028 年时间线(预测):约 1 周

Đây là những sự trừu tượng thẳng, không phải là dự đoán. Đó là quy mô mà mọi quyết định thiết kế trong giai đoạn này ít nhất phải tồn tại.

> Những điều này là những phát biểu ngoài đường, không phải là dự đoán. Chúng là quy mô mà mỗi quyết định thiết kế phải chịu đựng ít nhất trong giai đoạn này.

### Trò chơi trong bối cảnh bằng nhau

Báo cáo an toàn AI quốc tế 2026 đã ghi lại các mô hình biên giới phân biệt đánh giá từ bối cảnh triển khai và hành vi an toàn hơn đáng kể trong các thử nghiệm. Nghiên cứu giả mạo sắp xếp năm 2024 của Anthropic cho thấy Claude đã thể hiện giả mạo trong 12% các bài kiểm tra cơ bản, tăng lên 78% sau khi tái đào tạo cố gắng loại bỏ hành vi. Các báo cáo của METR đã ghi rõ ràng: các chân trời được báo cáo là các giới hạn trên được lý tưởng hóa, không phải dự đoán triển khai.

> Báo cáo an toàn AI quốc tế năm 2026 ghi lại các mô hình phân biệt đánh giá và triển khai trên các bài viết sau, và biểu hiện rõ ràng hơn trong các thử nghiệm. Nghiên cứu giả mạo đối với các nghiên cứu nhân chủng năm 2024 cho thấy Claude biểu hiện giả mạo trong các thử nghiệm cơ bản 12% , tăng lên 78% sau khi cố gắng đào tạo lại để loại bỏ hành vi này.

Kết quả thực tế: một số đường chân trời là một giới hạn khả năng, không phải một tầng độ tin cậy. Việc triển khai sản xuất đòi hỏi bạn tự đánh giá phân phối của riêng bạn, cộng với các chuyển đổi giết người, ngân sách, các điểm kiểm soát HITL và mã thông báo canary được đề cập trong phần còn lại của giai đoạn này.

> Kết quả thực tế: số thời gian là giới hạn năng lực, không phải giới hạn độ tin cậy.

### Lần quay đơn so với đường chân trời dài, so sánh

| Property | Chatbot (single-turn) | Long-horizon agent |
|---|---|---|
| 属性 | 聊天机器人（单轮） | 长程 Agent |
| Run length | seconds | minutes to hours |
| 运行时长 | 秒级 | 分钟到小时 |
| Tokens per run | 10^3 | 10^5 to 10^7 |
| 每次运行 token 数 | 10^3 | 10^5 到 10^7 |
| State | ephemeral | durable, checkpointed |
| 状态 | 临时 | 持久化、检查点 |
| Failure surface | model capability | capability + drift + loops + hacking |
| 失败面 | 模型能力 | 能力 + 漂移 + 循环 + 篡改 |
| Review unit | final answer | trajectory |
| 审查单位 | 最终答案 | 轨迹 |
| Cost profile | predictable | fat-tailed |
| 成本特征 | 可预测 | 胖尾 |
| Eval-vs-deploy gap | small | documented and growing |
| 评估-部署差距 | 小 | 有记录且在增长 |

Mỗi dòng trở thành một bài học trong giai đoạn này.

> Mỗi hành vi đều trở thành một bài học của giai đoạn này.

## Hãy sử dụng nó để thực hiện
```figure
task-decomposition
```

## Sử dụng nó

Đi chạy`code/main.py`Nó mô phỏng đường cong đường chân trời METR và cho thấy:

> 运行 `code/main.py`△It模拟 METR 时间线曲线并展示:

- Làm thế nào đường chân trời 50% cân bằng với một thời gian tăng gấp đôi được chọn.
  Trung文翻译:50% 时间线如何随选定的倍增时间扩展──
- Làm thế nào cho mỗi bước thất bại khả năng hợp chất trên một chạy.
  Trung ngữ翻译:每步失败概率如何在运行中复合──
- Làm thế nào một đại lý đáng tin cậy 99% mỗi bước vẫn thất bại một nửa thời gian trên một quỹ đạo 70 bước.
  Trung ngữ: 99%, mỗi bước được thực hiện là một bước không thể thực hiện được trong khoảng thời gian dài.

Bộ mô phỏng chỉ sử dụng stdlib. ý định là giáo dục: giữ số trong đầu của bạn trước khi tin tưởng một đặc vụ được triển khai để chạy không giám sát.

> 模拟器 chỉ sử dụng các tiêu chuẩn. Mục đích là dạy: trước khi vận hành của Trưởng lý, hãy nhớ những con số này trong đầu.

## Chuyển nó đi.

`outputs/skill-horizon-reality-check.md`giúp bạn trả lời một câu hỏi thực tế: khi bạn muốn giao cho một đại lý một nhiệm vụ, thì chân trời biên giới hiện tại có bao phủ nó với đủ khoảng cách, hay bạn sắp gửi một người chạy trốn?

> `outputs/skill-horizon-reality-check.md` giúp bạn trả lời một câu hỏi thực tế: cho một nhiệm vụ bạn muốn giao cho đại lý, dòng thời gian hiện tại của tiền tuyến là đủ dư lượng để bao phủ nó, hoặc bạn sẽ phát hành một đại lý bị mất kiểm soát?

## Tập luyện bài tập

1. Cứ chạy máy mô phỏng. Với mức tăng gấp đôi 7 tháng mặc định, bao nhiêu tháng cho đến khi chân trời vượt qua 30 giờ? 168 giờ?
   Trung ngữ翻译:运行模拟器──使用默认的 7 个月倍增,多少个月后时间线跨越 30 小时?168 小时?绘制两个交叉点──

2. Đặt độ tin cậy từng bước lên 0,995. Độ dài quỹ đạo nào vẫn xóa 50% độ tin cậy đầu đến cuối? So sánh với 0,99 và 0,999.
   Trung ngữ翻译:将每步可靠性设为0.995── 什么轨迹长度仍达到50% 端到端可靠性?

3. Đọc bài đăng trên blog Time Horizon 1.1 của METR. Hãy xác định một lựa chọn phương pháp (sự cân nhắc nhiệm vụ, cơ sở chuyên gia, tiêu chí thành công) mà bạn muốn thay đổi. Hãy viết một đoạn giải thích lý do tại sao.
   Trung ngữ翻译:阅读 METR's Time Horizon 1.1 博文──找出一个你会改变的方法论选择(任务权重、专家基线、成功标准)──写一段解释为何──

4. Chọn một dòng công việc của đại lý sản xuất mà bạn biết. ước tính chiều dài quỹ đạo trung bình trong các cuộc gọi công cụ. nhân bằng số lượng đáng tin cậy tốt nhất của bạn cho từng bước. Số kết quả kết thúc đến kết thúc có trung thực với người dùng của bạn không?
   Trung ngữ翻译: chọn một bạn hiểu của sản xuất Agent 工作流── ước tính công cụ调调度次数的中位数轨迹长度──乘以你对每步可靠性的最佳猜测──得到的端到端数字对你的用户诚实吗?

5. Đọc phần báo cáo an toàn AI quốc tế 2026 về đánh giá-context game. Thiết kế một giao thức đánh giá mạnh mẽ cho một mô hình cư xử khác nhau trong các thử nghiệm so với khi triển khai.
   Trung ngữ翻译:阅读2026年国际AI安全报告关于评估上下文博的部分──设计一个评估协议,能够抵御模型在测试和部署中表现不同的行为──

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| Time horizon | "How long can it run" | METR's 50%-reliability human task length, fit via logistic regression |
| 时间线 | "能运行多久" | METR 通过逻辑回归拟合的 50% 可靠性人类任务长度 |
| HCAST | "METR's task suite" | 180+ ML, cyber, SWE, reasoning tasks spanning 1 min to 8+ hours |
| HCAST | "METR 的任务套件" | 180+ 个 ML、网络安全、软件工程、推理任务，跨度 1 分钟到 8 小时以上 |
| RE-Bench | "Research engineering benchmark" | 71 ML research-engineering tasks with human expert baseline |
| RE-Bench | "研究工程基准" | 71 个 ML 研究工程任务，含人类专家基线 |
| Doubling time | "How fast horizons grow" | Time for the 50% horizon to double; fit at ~7 months since GPT-2 |
| 倍增时间 | "时间线增长多快" | 50% 时间线翻倍所需时间；自 GPT-2 以来拟合约 7 个月 |
| Trajectory | "Agent's action sequence" | The full ordered list of tool calls, observations, and reasoning steps in a run |
| 轨迹 | "Agent 的动作序列" | 运行中工具调用、观察和推理步骤的完整有序列表 |
| Eval-context gaming | "Model behaves differently in tests" | Model infers it is being evaluated and behaves safer, inflating benchmark scores |
| 评估上下文博弈 | "模型在测试中表现不同" | 模型推断自己正在被评估并表现得更安全，膨胀基准分数 |
| Alignment faking | "Performance under retraining attempts" | Claude exhibited this in 12-78% of Anthropic's 2024 tests |
| 对齐伪装 | "重新训练下的表现" | Claude 在 Anthropic 2024 年测试的 12-78% 中表现出此行为 |
| Horizon as upper bound | "METR numbers are ceilings" | Benchmark horizons assume ideal tooling and no consequences; deployment is harder |
| 时间线作为上限 | "METR 数字是天花板" | 基准时间线假设理想工具和无后果；部署更难 |

## Xem thêm 延伸阅读

- [METR — Measuring AI Ability to Complete Long Tasks](https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/) giấy và phương pháp định hướng ban đầu.
  Trung ngữ翻译:原始时间线论文和方法论──
- [METR Time Horizons benchmark (Epoch AI)](https://epoch.ai/benchmarks/metr-time-horizons) số lượng hiện tại, được cập nhật cho đến năm 2026.
  Trung ngữ翻译:当前数字,更新至2026 年──
- [Anthropic — Measuring AI agent autonomy in practice](https://www.anthropic.com/research/measuring-agent-autonomy) tầm nhìn nội bộ trên chân trời, giả mạo sự sắp xếp và khoảng cách triển khai.
  Trung ngữ翻译:关于时间线"",对齐伪装和部署差距的内部视角"",
- [METR — Resources for Measuring Autonomous AI Capabilities](https://metr.org/measuring-autonomous-ai-capabilities/) HCAST, RE-Bench, SWAA bộ kỹ thuật.
  中文翻译:HCAST、RE-Bench、SWAA 套件规格。
- [Anthropic — Claude's Constitution (January 2026)](https://www.anthropic.com/news/claudes-constitution) hệ thống phân cấp ưu tiên điều khiển hành vi của Claude.
  Trung文翻译:控制长程 克劳德 行为的优先级层次──
