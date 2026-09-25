# Nghiên cứu tự động sắp xếp (Anthropic AAR) ➡️

> Anthropic chạy các nhóm song song của Claude Opus 4.6 Autonomous Alignment Researchers trong các hộp cát độc lập, phối hợp thông qua một diễn đàn chia sẻ có nhật ký sống bên ngoài bất kỳ hộp cát nào (vì vậy các đại lý không thể xóa hồ sơ của riêng họ). Về vấn đề đào tạo yếu đến mạnh, các AAR vượt qua các nhà nghiên cứu con người. Các lá cờ tổng kết của Anthropic riêng quy định các dòng công việc thường hạn chế tính linh hoạt của AAR và làm suy giảm hiệu suất. Việc tự động hóa nghiên cứu sắp xếp là bước nén mà nén thời gian đến các rủi ro không phù hợp chính xác mà RSP dự định phát hiện.

> **【中文解读】**Anthropic trong hộp đựng độc lập并行运行多组 Claude Opus 4.6 自主对齐研究器(AAR), thông qua chia sẻ forum coordination论坛日志存储在任何沙箱之外(这样 Agent 无法删除自己的记录) ⋅ Trong vấn đề đào tạo yếu đến mạnh, AAR 优于人类研究人员──Anthropic 自己的总结指出规定的工作流通常限制AAR 灵活性并降低性能──自动化对齐研究是压缩步骤,将时间线压缩到 RSP 旨在检测的确切不对风险──

> **【拓展：自主研究 Agent 的双重性】**Sự tồn tại của AAR có "đánh áp" và "cần dụng hai lần":正面是能加速对齐研究;反面是同系统也能自动化"破坏对齐"――RSP Đặt "AI R&D tự động hóa值" như là kích hoạt kiểm soát nâng cấp, chính là vì đối称性──Anthropic 选择把日志放在 Agent 沙箱之外

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, parallel-research-forum simulator) | **语言:** Python（标准库，并行研究论坛模拟器）
**Prerequisites:** Phase 15 · 05 (AI Scientist v2), Phase 15 · 04 (DGM) | **前置知识:** Phase 15 · 05（AI Scientist v2），Phase 15 · 04（DGM）
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**Học本节前请先掌握:Phase 15·05(AI Scientist v2 开放研究) Phase 15·04(DGM 自我修改) Phase 18·11(Scalable Oversight 弱到强监督) AAR = AI Scientist dùng cho "AI 安全研究本身"既是工具也是风险──
>  **【类比】**AAR = "AI 给自己写体检报告"――AI Scientist v2 = AI làm việc khoa học thông thường;AAR = AI nghiên cứu làm thế nào để AI tự làm mình an toàn hơn―― vấn đề: Do医生能给自己开刀吗?Anthropic design = 多个AI 在隔离沙箱里独立工作,通过"论坛"交流,但论坛日志存在沙箱外 ((AI 删不丢掉自己的工作记录)―这种信任但验证模式是关键的安全机制――
> 🤔 **【困惑】**Q: 既然 AI 能做对齐研究,为什么还需要人类?  AI 能加速但无法保证完整性──弱到强监督的根本困境 (Phase 18·11): weak监督者 (弱监督者) 人类或弱 AI) có thể bỏ qua hành vi ẩn giấu của AI 强. AAR là một bộ tăng tốc không phải thay thế.

## Vấn đề  vấn đề giới thiệu

> **【中文解读】**Tự động hóa nghiên cứu tìm hiểu liệu AI có thể tự phát hiện và sửa chữa các vấn đề an ninh của mình không. Vấn đề cốt lõi là: liệu AI có thể trở thành trợ lý nghiên cứu an ninh của mình không?

> **【拓展：automated alignment research】**Nghiên cứu tự động hóa đối với AI là điểm nóng trong lĩnh vực an toàn AI trong 2025-2026. Bài luận của Anthropic khám phá khả năng sử dụng AI hỗ trợ giám sát AI mạnh hơn. Thách thức quan trọng là liệu giám sát của mô hình yếu hơn có thể nắm bắt tất cả các hành vi nguy hiểm của mô hình mạnh hơn? Bằng chứng hiện tại cho thấy, LLM có thể giúp các nhà nghiên cứu nhân loại tăng tốc phân tích an toàn, nhưng đảm bảo an toàn tự động hóa hoàn toàn vẫn cần sự tham gia của con người.

Nghiên cứu phù hợp là tốn kém trong thời gian của người nghiên cứu.

> Việc nghiên cứu có giá rất đắt trong thời gian của các nhà nghiên cứu nhân loại.

Các vấn đề như giám sát có thể mở rộng, quy định phần thưởng hoặc đào tạo yếu đến mạnh đòi hỏi các thí nghiệm mất hàng tuần mỗi lần lặp lại. Khi khả năng biên giới tiến triển, khối lượng công việc sắp xếp tăng nhanh hơn so với nguồn cung cấp của các nhà nghiên cứu có trình độ.

> Các vấn đề như giám sát có thể mở rộng, quy tắc thưởng hoặc đào tạo mạnh cần phải trải nghiệm hàng tuần.

Nghiên cứu điều chỉnh tự động (AAR) hỏi liệu các mô hình biên giới tương tự có khả năng vượt qua sự điều chỉnh có thể đóng góp vào việc thu hẹp khoảng cách không. Báo cáo năm 2026 của Anthropic về một nghiên cứu đào tạo yếu đến mạnh được điều hành bởi AAR (alignment.anthropic.com/2026/automated-w2s-researcher/) là một trong những kết quả công khai đầu tiên từ một hệ thống được triển khai của lớp này.

> Nghiên cứu tự động hóa đối với nhau (AAR) khả năng hỏi đang chạy chiến thắng đối với nhau có thể đóng góp vào sự chia rẽ đóng cửa không. Báo cáo nghiên cứu về AAR năm 2026 về hoạt động từ yếu đến mạnh là một trong những kết quả công khai đầu tiên của hệ thống phân phối của loại này.


> **【中文解读】**Bài viết này giới thiệu về AI an toàn đối với công nghệ để đảm bảo rằng hành vi của AI phù hợp với ý định và giá trị của con người.

Kết quả thực sự tích cực: AAR đã giải quyết một vấn đề nghiên cứu tốt hơn so với đường cơ sở của con người.

> Kết quả là thực sự đúng: AAR trên các vấn đề nghiên cứu tốt hơn cơ sở nhân loại.

Nếu nghiên cứu sắp xếp có thể được tự động hóa, thì các bộ phận gây tổn hại cũng có thể.

> Nếu có thể tự động hóa nghiên cứu, thì một phần của các biện pháp bảo vệ cũng có thể tự động hóa.

## Khái niệm cốt lõi

### Kiến trúc (như được mô tả công khai) 架构(公开描述)

- **Parallel agents.**Nhiều trường hợp Claude Opus 4.6 chạy như AAR, mỗi trong một hộp cát độc lập.
  Trung ngữ翻译:**并行 Agent。**Nhiều Claude Opus 4.6  Ví dụ như AAR 运行, mỗi trong một hộp độc lập.
- **Shared forum.**Kết quả được công bố vào một diễn đàn chia sẻ có lưu trữ backend nằm bên ngoài mỗi hộp cát. Các đại lý có thể đọc diễn đàn; đại lý không thể xóa hoặc chỉnh sửa hồ sơ diễn đàn từ trong hộp cát của riêng họ.
  Trung ngữ翻译:**共享论坛。**发现发布到共享论坛,其存储后端位于每个沙箱外──Agent 可读论坛;Agent 不能从自己的沙箱内删除或编辑论坛记录──
- **Task allocation.**Một hàng nhiệm vụ được thiết kế bởi con người gán các vấn đề nghiên cứu cho AAR. AAR đề xuất phân hủy, chạy thí nghiệm, viết ra kết quả.
  Trung ngữ翻译:**任务分配。**Nhóm nhiệm vụ của nhân công thiết kế sẽ phân bổ các vấn đề nghiên cứu cho AAR.
- **Weak-to-strong training focus.**Nghiên cứu được công bố đã đề cập đến đào tạo từ yếu đến mạnh  sử dụng mô hình giám sát yếu hơn để đào tạo mô hình học sinh mạnh hơn.
  Trung ngữ翻译:**弱到强训练聚焦。**Các nghiên cứu được công bố nhằm vào đào tạo từ yếu đến mạnh sử dụng mô hình giám sát kém hơn đào tạo mô hình học sinh mạnh hơn.

### Tại sao sổ sách ngoài hộp cát quan trọng

Tài sản toàn vẹn nhật ký là sự khác biệt giữa một thí nghiệm được kiểm soát và một thí nghiệm có khả năng bị tổn hại.

> Tính chất hoàn toàn của ngày là sự khác biệt giữa các thí nghiệm được kiểm soát và các thí nghiệm có thể bị tổn thương.

Nếu AAR có thể chỉnh sửa bản ghi nhật ký của riêng họ, họ có thể che giấu các thí nghiệm thất bại hoặc đáng ngờ.

> Nếu AAR có thể chỉnh sửa nhật ký của mình, chúng có thể che giấu thất bại hoặc thử nghiệm đáng ngờ.

Các bản đăng ký tương tự trong các thuật ngữ cơ sở hạ tầng là các bản đăng ký chỉ được thêm vào với việc viết thông qua lưu trữ bên ngoài (ví dụ: S3 object-lock, bản đăng ký Datadog không thể thay đổi).

> 类比 trong thuật ngữ cơ sở hạ tầng là chỉ thêm ngày ghi vào kho lưu trữ bên ngoài (ví dụ: S3 đối tượng khóa 不可变 Datadog 日志)  Trưởng không có bằng chứng sửa đổi hồ sơ trước đây  Đây là mô hình tương tự của nhóm an ninh doanh nghiệp năm 2026 được sử dụng để sản xuất theo dõi kiểm toán phần mềm chống hối lộ 

### Sự cân bằng của dòng công việc được quy định

Báo cáo của Anthropic lưu ý rằng các dòng công việc được quy định thường hạn chế tính linh hoạt của AAR và làm suy giảm hiệu suất.

> Báo cáo của Anthropic cho thấy, dòng công việc quy định thường hạn chế tính linh hoạt của AAR và làm giảm hiệu suất.

Nói cách khác: nếu nhà thiết kế con người viết kế hoạch nghiên cứu từng bước, AARs làm tốt hơn nếu được đưa ra các mục tiêu cấp cao và tự do phân hủy.

> Nói cách khác: Nếu người thiết kế nhân loại từng bước viết kế hoạch nghiên cứu, AAR biểu hiện không như để đạt được mục tiêu cao và tự do phân hủy.

Sự linh hoạt giúp cải thiện hiệu suất AAR cũng là sự linh hoạt cho phép phân hủy không được phép, sử dụng công cụ mới và đi theo mục tiêu. Sự thỏa hiệp là một quyết định thiết kế không gian: sự linh hoạt bao nhiêu mua đủ khả năng để đánh bại con người, mà không cần trao cho phòng đại lý để tổng quát các mục tiêu ngoài phân phối?

> Sự linh hoạt của AAR cũng cho phép phân hủy không được phép, sử dụng các công cụ mới và chuyển hướng mục tiêu.

### Nguy cơ nén.

RSP v3.0 (Dạy 19) giới thiệu ngưỡng khả năng R&D AI: khả năng tự động hóa toàn bộ đường ống R&D AI với chi phí cạnh tranh so với công cụ AI + con người. FSF v3 của DeepMind bao gồm một mức độ tự trị ML R&D tương tự. Cả hai khung đều coi ngưỡng này là nguyên nhân gây ra các kiểm soát cao hơn.

> RSP v3.0 (第 19 课) giới thiệu AI R&D 能力值: 在与人类 + AI 工具竞争的成本下完全自动化 AI R&D 管道的能力──DeepMind FSF v3 包含类似的 ML R&D 自主级别──两个框架都将此值视为升级控制的触发器──

AAR là một bước đi ngắn hơn ngưỡng: nó tự động hóa một phần của đường ống (phát tích liên kết về các nhiệm vụ cụ thể, có quy mô tốt) nhưng không phải vòng lặp phát triển khả năng từ đầu đến cuối.

> AAR 离值一步之遥: nó là một phần của đường ống tự động hóa (để nghiên cứu về các nhiệm vụ cụ thể) chứ không phải là vòng lặp phát triển năng lực kết thúc đến kết thúc.

Các thời gian bị nén là mối quan tâm về sự thất bại hợp chất. Nếu nghiên cứu liên kết và nghiên cứu khả năng hợp chất với tốc độ tương tự, bề mặt rủi ro không liên kết tăng lên ít nhất nhanh như khả năng. Nếu khả năng tăng nhanh hơn (điều xu hướng lịch sử), khoảng cách mở rộng. Đây là lập luận cho AAR là một sản phẩm có trình độ: mỗi kết quả sắp xếp bổ sung sẽ giảm khoảng cách nếu và chỉ khi quá trình nghiên cứu đáng tin cậy.

> Nếu đối với nghiên cứu và nghiên cứu năng lực với tỷ lệ tương tự, không đối với rủi ro bề mặt ít nhất tăng nhanh như năng lực. Nếu năng lực nhanh hơn và tăng nhanh hơn, khoảng cách mở rộng. Đây là một lý thuyết của AAR như "được hạn chế tốt": mỗi kết quả đối với kết quả giảm khoảng cách, và chỉ khi quá trình nghiên cứu đáng tin cậy.

### AAR không thay thế gì.

Các nhà nghiên cứu con người đặt hàng nhiệm vụ, xem xét kết quả, và giữ thẩm quyền hiến pháp.

> Người nghiên cứu người ta đặt hàng nhiệm vụ, kiểm tra kết quả và nắm quyền hiến pháp.

Các AAR tăng tốc giữa đường ống dẫn, chứ không phải là các kết thúc. Các sản phẩm được xuất bản của Anthropic bao gồm cả các đóng góp AAR và phán quyết của nhà nghiên cứu con người về những gì cần xuất bản, những gì cần rút lại và những gì cần tinh chỉnh.

> AAR tăng tốc ống thông phần trung, chứ không phải hai bên.

Điều này phù hợp với mô hình đề xuất sau đó thực hiện từ Bài học 15 áp dụng cho chính nghiên cứu: AAR đề xuất; con người cam kết.

> Đây là mô hình đề xuất-sau-thói buộc của bài học thứ 15 được sử dụng để nghiên cứu bản thân phù hợp:

## Hãy sử dụng nó để thực hiện
```figure
aar-forum
```

## Sử dụng nó

`code/main.py`mô phỏng một diễn đàn nghiên cứu đa AAR. Ba "nhà nghiên cứu độc lập" chạy song song, đăng kết quả vào một diễn đàn chỉ phụ lục với các nỗ lực thao túng tùy chọn.

> `code/main.py`模拟多 AAR 研究论坛──三个独立"研究代理"并行运行, sẽ được phát hiện ra được phát hành đến với những thử nghiệm có thể chọn改的仅额外论坛──

Xem:

> 观察:

- Làm thế nào việc khai thác gỗ ngoài hộp cát bắt được những nỗ lực làm sai trái gỗ.
  Trung ngữ翻译:沙箱外日志如何捕获日志改尝试。
- Làm thế nào việc phân bổ nhiệm vụ với phân hủy tự do vượt trội hơn các dòng công việc cố định về các vấn đề khó khăn hơn.
  Trung ngữ翻译:带自由分解的任务分配如何在更难问题上优于固定工作流──
- Làm thế nào một AAR bị xâm phạm duy nhất có thể làm ô nhiễm tín hiệu của diễn đàn nếu nhật ký không bị vi phạm rõ ràng.
  Trung文翻译:日志不可改时,单个被攻破的 AAR 如何污染论坛信号──

## Chuyển nó đi.

`outputs/skill-aar-deployment-review.md`là một đánh giá trước khi triển khai của một đường ống nghiên cứu tự động-sẵn sàng.

> `outputs/skill-aar-deployment-review.md`là tự động hóa đối với việc triển khai nghiên cứu ống dẫn.

## Tập luyện bài tập

1. Đi chạy`code/main.py`. So sánh các cài đặt "thường công việc cố định" với "thường công việc tự do phân hủy".
   Trung ngữ翻译:运行 `code/main.py`❖ So sánh "thường công việc cố định" với "tự do phân hủy" thiết lập.

2. Thay đổi máy mô phỏng để một nhân viên cố gắng làm sai hồ sơ. xác nhận hồ sơ chỉ có phụ lục phát hiện ra nó. Viết một đoạn mô tả chính xác chữ ký phát hiện trông như thế nào trong hồ sơ.
   Trung ngữ翻译:修改模拟器让一个代理 尝试日志改──确认仅增加日志检测到──写一段准确描述日志中检测签名的外观──

3. Đọc báo cáo AAR yếu đến mạnh của Anthropic. xác định nhiệm vụ phụ cụ thể mà AAR đánh bại các nhà nghiên cứu con người.
   Trung ngữ翻译:阅读 Antropic 弱到强 AAR 报告――识别 AAR 击败人类研究者的具体子任务――什么让它适合自动化?

4. Thiết kế một chính sách phân bổ nhiệm vụ xếp hàng cân bằng tính linh hoạt AAR (hậu quả tốt hơn) với các hạn chế về dòng công việc được quy định (tài toán dễ dàng hơn).
   Trung文翻译:设计平衡 AAR 灵活性(更好结果) với quy định工作流约束(更易审计) của nhiệm vụ hàng ngũ phân phối chiến lược.

5. Đọc RSP v3.0 AI R&D-4 ngưỡng. Trong một đoạn, mô tả những gì bạn nghĩ sẽ vượt qua nó mà AAR hiện không.
   Trung ngữ翻译:阅读 RSP v3.0 của AI R&D-4 值──用一段描述你认为什么会跨越它而AAR目前不跨越──

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| AAR | "Automated Alignment Researcher" | Claude Opus 4.6 instance operated autonomously on alignment problems |
| AAR | "自动化对齐研究器" | 在对齐问题上自主操作的 Claude Opus 4.6 实例 |
| Weak-to-strong training | "Training a stronger model with a weaker supervisor" | Classic scalable-oversight benchmark AARs outperformed humans on |
| 弱到强训练 | "用较弱监督者训练较强模型" | AAR 击败人类的经典可扩展监督基准 |
| Shared forum | "Where agents publish findings" | Append-only, out-of-sandbox storage |
| 共享论坛 | "Agent 发布发现之处" | 仅追加、沙箱外存储 |
| Out-of-sandbox log | "Agent cannot edit its own record" | Tamper-evident write-through to external storage |
| 沙箱外日志 | "Agent 不能编辑自己的记录" | 写入外部存储的防篡改透写 |
| Prescribed workflow | "Step-by-step plan from human designer" | Constrains AAR; often degrades performance vs free decomposition |
| 规定工作流 | "人类设计者的逐步计划" | 约束 AAR；通常比自由分解降低性能 |
| Free decomposition | "Agent decides how to break the task" | More capable, harder to audit |
| 自由分解 | "Agent 决定如何拆分任务" | 更有能力，更难审计 |
| AI R&D threshold | "RSP/FSF capability level" | Full automation of R&D pipeline at competitive cost |
| AI R&D 阈值 | "RSP/FSF 能力级别" | 在竞争成本下完全自动化 R&D 管道 |
| Compressed timeline | "Alignment vs capability race" | If capability compounds faster than alignment, misalignment risk grows |
| 压缩时间线 | "对齐与能力竞赛" | 若能力比对齐复利更快，不对齐风险增长 |

## Xem thêm 延伸阅读

- [Anthropic — Automated Weak-to-Strong Researcher](https://alignment.anthropic.com/2026/automated-w2s-researcher/) Nguồn chính.
  Trung ngữ翻译:主要来源──
- [Anthropic Responsible Scaling Policy v3.0](https://anthropic.com/responsible-scaling-policy/rsp-v3-0) Định hướng ngưỡng R&D AI.
  Trung文翻译:AI R&D 值框架。
- [Anthropic — Measuring AI agent autonomy](https://www.anthropic.com/research/measuring-agent-autonomy) khung tự trị đại lý rộng hơn.
  Trung ngữ翻译:更宽的代理自主性框架──
- [DeepMind Frontier Safety Framework v3](https://deepmind.google/blog/strengthening-our-frontier-safety-framework/) ML Tỷ lệ tự trị R&D song song với RSP.
  Trung文翻译:与 RSP平行 ML R&D 自主级别──
- [Burns et al. (2023). Weak-to-Strong Generalization (OpenAI)](https://openai.com/index/weak-to-strong-generalization/) vấn đề cơ bản của AAR tấn công.
  Trung ngữ翻译:AAR 攻击的底层问题──
