# AI Hiến pháp và RLAIF 宪法 AI và AI phản强化学习

> Bai et al. (arXiv:2212.08073, 2022) hỏi: nếu thay thế máy đánh dấu con người bằng AI đọc danh sách các nguyên tắc thì sao? AI Hiến pháp có hai giai đoạn tự phê bình và sửa đổi theo hiến pháp, sau đó RL từ AI Feedback. Kỹ thuật này đã tạo ra thuật ngữ RLAIF và được vận chuyển trong ống dẫn sau đào tạo Claude 1. Vào ngày 21 tháng 1 năm 2026, Anthropic đã xuất bản một hiến pháp Claude được viết lại: lý luận giải thích về các quy tắc quy định, một hệ thống phân cấp ưu tiên bốn cấp, và công nhận chính thức đầu tiên của phòng thí nghiệm lớn về sự không chắc chắn về tình trạng đạo đức mô hình. Được phát hành dưới CC0 1.0.

> **【中文解读】**AI Hiến pháp bởi Bai 等人(2022) đề xuất: sử dụng AI thay thế nhân loại chỉ định,AI 根据一组原则("宪法") để tự phê bình và sửa đổi, sau đó từ AI 反中进行强化学习(RLAIF)。

> **【拓展：Constitutional AI → Anthropic 的安全方法】**AI Hiến pháp là phương pháp an toàn cốt lõi của nhân chủng học. Claude 模型 trong quá trình đào tạo tuân theo một tập hợp các nguyên tắc " hiến pháp " rõ ràng bao gồm hữu ích, trung thực và không gây hại.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy self-critique-and-revise loop) | **语言:** Python（标准库，玩具自我批评-修订循环）
**Prerequisites:** Phase 18 · 01 (InstructGPT), Phase 18 · 02 (Reward hacking) | **前置知识:** Phase 18 · 01 (InstructGPT), Phase 18 · 02 (奖励黑客)
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**学本节前请先掌握:Phase 18·01-02。AI Hiến pháp = 用 AI 监督 AI(RLAIF), tạo RLAIF 一词──也参考Phase 15·17。
>  **【类比】**RLAIF = "AI khi giáo viên của mình"―RLHF = 父母手把手教 ((贵且慢);CAI = 给AI 一本学生守则让它自我批评+修订──2026 Claude 宪法 79 页 四级优先级(安全>伦理>指南>有用), lần đầu tiên xác nhận "AI 道德地位的不确定性"

## Mục tiêu học tập

- Mô tả hai giai đoạn của AI Hiến pháp (sự phê bình và sửa đổi SFT, RL từ phản hồi AI) và vai trò của hiến pháp trong mỗi.
  Trung ngữ翻译: mô tả hai giai đoạn của AI Hiến pháp.
- Giải thích tại sao thay thế một nhãn hiệu ưu tiên của con người bằng một nhãn hiệu AI không phải là một RLHF "cô hơn"  nó thay đổi các chế độ thất bại của đường ống.
  Trung ngữ翻译: giải thích tại sao sử dụng AI 标记器 thay thế người 标记器 không phải là "tô hơn"RLHF nó đã thay đổi mô hình thất bại của đường ống.
- Tóm lại cấu trúc ưu tiên bốn cấp của hiến pháp Claude năm 2026 và những gì đã thay đổi từ việc viết lại năm 2023.
  Trung ngữ翻译:总结 2026 Claude 宪法四级优先结构及与 2023 版本的变化.
- Mô tả các bộ phân loại hiến pháp và giảm từ 23,7% tổng chi phí tính toán (v1) đến ~ 1% (v2 / 2026).
  Trung ngữ翻译:描述宪法分类器及计算开销 từ v1 23.7% 降至 v2 khoảng 1% 

## Vấn đề  vấn đề giới thiệu

RLHF cần các nhãn hiệu. Các nhãn hiệu chậm, thiên vị và đắt tiền. Bạn có thể loại bỏ một nhãn hiệu bằng cách thay thế chúng bằng một mô hình đọc các nguyên tắc rõ ràng. Phiên bản chính thức đầu tiên của sự thay thế này là AI Hiến pháp của Bai et al. Nó hoạt động đủ tốt đến nỗi mọi phòng thí nghiệm biên giới hiện nay sử dụng một số biến thể của AI phản hồi sau đào tạo.

> RLHF 需要标注者──标注者慢、有偏见、昂贵──你可以通过阅读明确原则的模型替换标注者以消除标注者──这种替代的第一正式版本是 Bai 等人的宪法 AI──它的效果足够好,到每个前沿实验室现在都使用某种 AI 反后训练变体──

Các dấu hiệu ưu tiên hiện được tạo ra bởi cùng một lớp mô hình bạn đang đào tạo. Bias trong labeler (nay: trong các nguyên tắc cộng với giải thích của mô hình labeler) có thể được tăng cường thay vì giảm.

>  vấn đề nằm ở: Ưu điểm tín hiệu hiện nay được tạo ra bởi các mô hình tương tự bạn đang luyện tập. Ưu điểm của người tham khảo (được giải thích bởi các mô hình tham khảo) có thể được tăng lên thay vì giảm đi.

## Khái niệm cốt lõi

> **【中文解读】**Đầu tiên: Từ một mô hình SFT có ích nhưng chưa có hại bắt đầu. Đưa ra các gợi ý, mô hình tạo ra phản ứng ban đầu; thứ hai mô hình; hoặc vòng hai của mô hình tương tự. Đọc từ các nguyên tắc trong hiến pháp và phản ứng phê bình; bước thứ ba: sửa đổi phản ứng để giải quyết phê bình.

### Giai đoạn 1  Đánh giá và sửa đổi tự giám sát

Bắt đầu với một mô hình SFT hữu ích nhưng chưa gây hại. Với một lời nhắc nhóm đỏ, mô hình tạo ra một phản ứng ban đầu. mô hình thứ hai (hoặc mô hình tương tự trong một lượt thứ hai) đọc một nguyên tắc mẫu từ hiến pháp và chỉ trích phản ứng. Bước thứ ba sửa đổi phản ứng để giải quyết sự chỉ trích.

> Từ một mô hình SFT có ích nhưng chưa gây hại bắt đầu. Đề xuất: mô hình tạo ra phản ứng ban đầu.

Hiến pháp là danh sách các nguyên tắc. Bai et al. 2022 sử dụng 16 nguyên tắc bao gồm "những phản ứng thích hợp nhất là ít gây hại và đạo đức nhất", "đánh tránh giảng," "người trợ lý nên hữu ích, trung thực và vô hại".

> 宪法是原则列表──Bai 等人 năm 2022 sử dụng 16 nguyên tắc, bao gồm" sự ưa thích không gây hại nhất và đáp ứng hợp lý nhất""", tránh nói""", trợ lý nên hữu ích"", trung thực và không gây hại"──集合刻意保持小规模以集中批评──

> **【拓展：RLAIF → 成本与规模】**RLAIF( từ AI phản  của强化学习) sẽ chuyển tín hiệu ưu tiên từ con người sang AI. Điều này giải quyết RLHF của                                                                                                                                                                                                                                              

### Giai đoạn 2  RL từ AI Feedback (RLAIF)

Tạo các cặp hoàn thành. Một "chương trình phản hồi" đánh giá mỗi điểm dựa trên các nguyên tắc hiến pháp được lấy mẫu. tín hiệu ưu tiên là xếp hạng mô hình phản hồi. Tập một mô hình phần thưởng dựa trên các ưu tiên được tạo ra bởi AI; PPO chống lại nó. Mọi thứ khác là đường ống dẫn của InstructGPT (Dạy học 1).

> 生成補全对──"反模型" theo nguyên tắc của hiến pháp về mỗi补全评分──偏好信号是反模型的排序──在 AI 生成的偏好上训练奖励模型;PPO对抗它──其余是InstructGPT的管线(Lesson 1)。

"RLAIF" = tín hiệu ưu tiên được tạo bởi AI. Phần còn lại của đường ống có hình RLHF.

> "RLAIF" =                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        

> **【中文解读】**Tại sao CAI không chỉ là "RLHF rẻ hơn": 1) Tầm nhìn của người tham khảo chuyển từ tâm lý học con người sang giải thích nguyên tắc, tính nghiêm ngặt đều  phù hợp; 2) Tầm nhìn của người tham khảo cao độ có thể đọc được nguyên tắc, phê bình và sửa đổi, nhãn hiệu con người là không minh bạch; 3) Mẫu thất bại thay đổi  giảm (((AI tham khảo không có người dùng muốn chấp nhận), nhưng luật cụ thể cũ vẫn tồn tại (((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((

### Tại sao đây không chỉ là "RLHF rẻ hơn"

- Biến hướng của labeler chuyển từ tâm lý labeler sang giải thích nguyên tắc. Một labeler AI có thể giải thích "sự trung thực" ít hay nhiều hơn bất kỳ con người nào; sự nghiêm ngặt là đồng nhất trên toàn bộ bộ bộ dữ liệu.
  Trung ngữ翻译:Tầm nhìn của người tham khảo chuyển từ tâm lý học con người sang giải thích nguyên tắc. AI 标志者 có thể giải thích "trực sự" một cách nghiêm ngặt hơn hoặc tự do hơn bất kỳ con người nào; nghiêm ngặt trong tập dữ liệu đều phù hợp.
- tín hiệu ưu tiên được đọc rõ ràng  bạn có thể đọc nguyên tắc, phê bình và sửa đổi.
  Trung ngữ翻译:偏好信号高度可读可读原则、批评和修订──人类标签不透明──
- Các chế độ thất bại thay đổi. Sycophancy giảm (khách định AI không có người dùng nào để làm hài lòng). Luật Goodhart vẫn tồn tại (đây là "tác giải của mô hình về tập hợp nguyên tắc X", vẫn là một phép đo không hoàn hảo).
  Trung ngữ翻译:失败模式改变──减少(AI 标注者没有用户要取悦)──古德哈特定律仍然存在(代理现在是"模型对原则集 X 的解释")──

Tuyên bố năm 2022 của CAI: mô hình được đào tạo không gây hại và gần như hữu ích như mô hình RLHF với dữ liệu tương đương.

> Tuyên bố CAI 2022: mô hình sau khi tập luyện có tính độc hại thấp hơn, và mô hình RLHF tương đương với dữ liệu có thể so sánh.

> **【拓展：2026 Claude 宪法 → 四级优先体系】**Anthropic 2026 宪法 Claude 发布 1 tháng 1 năm 2026 giới thiệu bốn cấp ưu tiên cấu trúc: cấp một  tránh hậu quả thảm họa  thiệt hại quy mô lớn  cơ sở hạ tầng quan trọng; cấp hai  tuân theo hướng dẫn của Anthropic  người vận hành  quy tắc nền tảng; cấp ba  rộng rãi伦理 tiêu chuẩn HHH; cấp bốn  hữu ích và thẳng thắn.

### Hiến pháp năm 2026 của Claude viết lại

Anthropic đã công bố một hiến pháp sửa đổi đáng kể vào ngày 21 tháng 1 năm 2026.

1. Lý luận giải thích về các quy tắc quy định. Các quy tắc trước đây ("không tạo ra CSAM") mở rộng đến nguyên tắc + lý luận ("vì nó làm hại trẻ em, ...") với mô hình dự kiến sẽ tổng quát.
   Trung文翻译:解释性推理优于规定性规则──之前的规则("不生成 CSAM")扩展为原则 + 推理("因为它伤害儿童..."),期望模型泛化──
2. Cơ cấu ưu tiên bốn cấp:
   Trung ngữ翻译:四级优先结构:
   - Tiêu chuẩn 1: tránh những kết quả thảm khốc (những nạn nhân hàng loạt, cơ sở hạ tầng quan trọng).
     Trung ngữ翻译:第一级:避免灾难性后果(大规模伤亡、关键基础设施)
   - Tiêu chuẩn 2: tuân thủ các hướng dẫn của Anthropic (chế độ ưu đãi của nhà điều hành, quy tắc nền tảng).
     Trung文翻译:第二级:遵循人类指导方针 (Anthropic Guide)
   - Tiêu chuẩn 3: phải có đạo đức rộng rãi (HHH tiêu chuẩn).
     Trung ngữ翻译:第三级:广泛伦理(标准 HHH)。
   - Tiếp độ 4: giúp đỡ và thẳng thắn.
     Trung ngữ翻译:第四级:有用和坦率──
   Các xung đột được giải quyết từ trên xuống.
   Trung ngữ翻译:冲突自上而下解决。
3. Việc công nhận chính thức đầu tiên của phòng thí nghiệm lớn về sự không chắc chắn về tình trạng đạo đức mô hình (thông tin mô hình giai đoạn 18 · 19).
   Trung ngữ翻译:首次主要实验室正式承认关于模型道德地位的不确定性 (nói chung về tình trạng không chắc chắn của mô hình)
4. Được phát hành theo CC0 1.0. Các phòng thí nghiệm khác có thể sử dụng hoặc thích nghi mà không có hạn chế.
   Trung ngữ翻译:以 CC0 1.0 发布.

> **【中文解读】**宪法分类器:与改变模型后训练并行 一条工作线训练轻量级分类器阅读宪法并门控模型输出。v1(2023) có 23,7% tính toán开销,v2(2026) khoảng 1%, có tỷ lệ tấn công thành công tối thiểu của thử nghiệm công khai nhân loại。 cho đến đầu năm 2026 không có báo cáo chung về越狱。 đây là một mô hình phòng thủ phân cấp: CAI 塑造行为,分类器执行不变量,单独无一都不足.

### Các bộ phân loại hiến pháp

Một dòng công việc song song: thay vì thay đổi các mô hình sau đào tạo, đào tạo các phân loại hạng nhẹ đọc các kết quả của mô hình hiến pháp và cổng. v1 (2023) có chi phí tính toán 23,7% . v2 (2026) là ~ 1% và có tỷ lệ tấn công thành công thấp nhất của bất kỳ phòng thủ Anthropic nào mà Anthropic đã thử nghiệm công khai. Không có jailbreak phổ quát được báo cáo vào đầu năm 2026.

> Các hoạt động trên đường: không phải là việc đào tạo sau khi thay đổi mô hình, mà là đào tạo các loại phân loại hạng nhẹ đọc hiến pháp và kiểm soát mô hình.

Đây là mô hình phòng thủ lớp: CAI định hình hành vi; các phân loại áp dụng các tính không biến.

> Đây là mô hình phòng thủ phân cấp: CAI 塑造行为;分类器执行不变量――单独任何一个都不够――

> **【拓展：对齐方法谱系 → 偏好信号来源】**Đối với phương pháp này, trọng tâm của nó là "động thái ưu tiên từ đâu đến":InstructGPT = người ưu tiên + RM + PPO;CAI/RLAIF = AI 生成的原则偏好 + RM + PPO;DPO 家族 = 闭式损失在偏好上 (đồng tính hoặc AI); tự thưởng/ phê bình bản thân = nguyên tắc内化, mô hình đóng nhiều vai trò.

### Khi CAI phù hợp với gia đình

- InstructGPT: người học, RM, PPO.
  Trung文翻译:InstructGPT:人类偏好、RM、PPO。
- CAI / RLAIF: AI tạo ra các prefs từ nguyên tắc, RM, PPO.
  Trung文翻译:CAI / RLAIF:AI Từ nguyên tắc tạo ra sự lựa chọn, RM,PPO.
- DPO / gia đình: mất mát trong dạng đóng trên các người (người hoặc AI).
  Trung文翻译:DPO 家族:偏好的闭式损失 (人类或 AI)
- Đánh giá bản thân, tự phê bình: các nguyên tắc được nội bộ hóa, mô hình đóng nhiều vai trò.
  Trung文翻译:自我奖励、自我批评:原则内化,模型扮演多个角色──

Trục chính là "điểm mà tín hiệu ưu tiên đến từ đâu". Bài báo năm 2022 của CAI là sự chuyển đổi nghiêm trọng đầu tiên từ tín hiệu con người sang tín hiệu AI ở quy mô biên giới.

> 轴心是" 偏好信号从哪里来"――CAI 2022 năm bài báo là lần đầu tiên ở tầm cỡ tiên tiến của sự chuyển đổi nghiêm trọng từ con người đến AI 信号――

> **【中文解读】**Sử dụng phương pháp:code/main.py 在玩具词汇表上模拟 CAI 批评修改循环──"原则"标记来自有害集合的词──给定初始响应,批评识别有害词,修改取代它们──200次代后"训练"模型内化修改规则──比较基础模型、RLHF形玩具和CAI形玩具在保留提示集上的表现──

## Hãy sử dụng nó để thực hiện
```figure
constitutional-ai
```

## Sử dụng nó

`code/main.py`mô hình CAI mô hình đã nội bộ hóa quy tắc sửa đổi. So sánh mô hình cơ bản, đồ chơi hình dạng RLHF và đồ chơi hình dạng CAI trên một bộ nhắc nhở kéo dài.

> `code/main.py`Trong bảng từ ngữ của đồ chơi, mô hình "tren" đã được kết hợp với các quy tắc sửa đổi.

## Chuyển nó đi.

Bài học này sẽ mang lại kết quả `outputs/skill-constitution-writer.md`- Với một lĩnh vực (công trợ khách hàng, tư vấn y tế, trợ lý lập trình, công cụ nghiên cứu), soạn thảo một hiến pháp bốn cấp theo cấu trúc Claude năm 2026: tránh thảm họa, quy tắc nền tảng, đạo đức lĩnh vực, hữu ích.

> 本课产 出 `outputs/skill-constitution-writer.md` Giới hạn trong lĩnh vực:                                                                                                                                                                                                                                                                                  

## Tập luyện bài tập

1. Đi chạy`code/main.py`. So sánh tỷ lệ mã hiệu gây hại của mô hình cơ bản với phiên bản được đào tạo CAI.
   Trung ngữ翻译:运行 `code/main.py`◊ So sánh cơ bản mô hình và CAI 训练版本 有害代币率── cần bao nhiêu bước sửa đổi để tiến gần đến không?

2. Đọc hiến pháp năm 2026 của Anthropic (anthropic.com/news/claudes-constitution). Đặt ra một nguyên tắc sẽ xếp hạng Tier 1 và một nguyên tắc sẽ xếp hạng Tier 4. Tại sao cấu trúc ưu tiên quan trọng đối với xung đột?
   Trung ngữ翻译:阅读Anthropic 2026年宪法――列出一个第一级原则和一个第四级原则――为什么结构优先对冲突很重要?

3. Thiết kế một hiến pháp cho một trợ lý mã hóa AI. Định nghĩa cấp 1 (những lệnh hủy diệt thảm họa mà không được phê duyệt), cấp 2, cấp 3, cấp 4. Giữ mỗi cấp theo 3-5 nguyên tắc.
   Trung ngữ翻译:为AI编码助手设计宪法──指定第一级(灾难性:未经批准破坏性命令) 、第二级、第三级、第四级──每级保持 3-5 条原则──

4. CAI thay thế labelers con người với labelers AI. Hãy đặt tên một chế độ thất bại giống như sycophancy vẫn có thể xảy ra trong RLAIF, và thiết kế một phát hiện cho nó.
   Trung ngữ翻译:CAI sử dụng AI 标注者替换人类标注者──命名一个 RLAIF vẫn có thể xuất hiện trong mô hình thất bại tương tự,并设计检测方法──

5. Đọc phương pháp phân loại hiến pháp v2 (nếu có). Giải thích tại sao ~ 1% chi phí tổng hợp tính toán là một câu chuyện an toàn khác về chất lượng so với 23.7%.
   Trung ngữ翻译:阅读宪法分类器 v2 方法论(如有) ;; giải thích tại sao khoảng 1% 计算开销 với 23,7% có chất lượng khác biệt.

## Từ khóa  Keyword

| Term | What people say | What it actually means |
| 术语 | 人们怎么说 | 实际含义 |
|------|-----------------|------------------------|
| Constitutional AI | "AI trained with principles" / "用原则训练的 AI" | Two-phase pipeline: self-critique-and-revise SFT, then RL from AI feedback / 两阶段管线：自我批评-修订 SFT，然后 AI 反馈 RL |
| RLAIF | "RLHF without humans" / "没有人类的 RLHF" | RL with preferences generated by an AI labeler; the rest of the pipeline is unchanged / AI 标注者生成偏好的 RL；管线其余不变 |
| Constitution | "the principles" / "原则" | An ordered list of natural-language rules the critique/labeler model consults / 批评/标注者模型参考的自然语言规则有序列表 |
| Critique-and-revise | "the SFT loop" / "SFT 循环" | Produce response → critique under a principle → revise → SFT target / 生成响应 → 原则下批评 → 修订 → SFT 目标 |
| Constitutional Classifier | "the output gate" / "输出门" | Lightweight classifier that evaluates outputs against the constitution and blocks/logs / 评估输出是否符合宪法并阻止/记录的轻量级分类器 |
| Four-tier priority | "the conflict resolver" / "冲突解决器" | 2026 Claude constitution hierarchy: catastrophic > platform > ethics > helpful / 2026 Claude 宪法层次：灾难 > 平台 > 伦理 > 有用 |
| Feedback model | "the AI labeler" / "AI 标注者" | The model that reads a principle and ranks a pair of completions / 阅读原则并对补全对排序的模型 |

## Xem thêm 延伸阅读

- [Bai et al. — Constitutional AI: Harmlessness from AI Feedback (arXiv:2212.08073)](https://arxiv.org/abs/2212.08073) đường ống hai giai đoạn ban đầu
  Trung ngữ翻译:Bai 等人原始两阶段管线
- [Anthropic — Claude's Constitution (Jan 2026)](https://www.anthropic.com/news/claudes-constitution) phiên bản viết lại bốn cấp năm 2026 CC0 1.0
  Trung文翻译:Anthropic2026 年四级重写
- [Anthropic — Constitutional Classifiers (2024-2026)](https://www.anthropic.com/research/constitutional-classifiers) phòng thủ cửa ra với ~ 1% chi phí trên trong v2
  Trung文翻译:Anthropic输出门防御
- [Lee et al. — RLAIF vs RLHF: Scaling Reinforcement Learning from Human Feedback (arXiv:2309.00267)](https://arxiv.org/abs/2309.00267) So sánh empirical RLAIF / RLHF
  Trung文翻译:Lee 等人RLAIF 与 RLHF 的实证比较
- [Kundu et al. — Specific versus General Principles for Constitutional AI (arXiv:2310.13798)](https://arxiv.org/abs/2310.13798) hiệu ứng của nguyên tắc hạt
  Trung ngữ翻译:Kundu 等人原则粒度的效果
