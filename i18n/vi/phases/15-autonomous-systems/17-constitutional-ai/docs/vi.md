# AI Hiến pháp và Quy tắc bị bỏ qua

> Anthropic's 22 tháng 1 năm 2026 Claude Constitution chạy 79 trang và là CC0. Nó chuyển từ quy tắc dựa vào sự phù hợp dựa trên lý do và thiết lập một hệ thống ưu tiên bốn cấp: (1) an toàn và hỗ trợ giám sát của con người, (2) đạo đức, (3) hướng dẫn nhân văn, (4) hữu ích. Hành vi chia thành cấm mã hóa cứng (cải thiện vũ khí sinh học, CSAM) mà các nhà khai thác và người dùng không thể bỏ qua và các mặc định mã hóa mềm mà các nhà khai thác có thể điều chỉnh trong giới hạn được xác định. Bản gốc năm 2022 (Bai et al.) đã đào tạo sự vô hại thông qua tự phê bình và RLAIF chống lại hiến pháp. Lời cảnh báo trung thực: sự sắp xếp dựa trên lý do dựa trên mô hình tổng quát các nguyên tắc cho các tình huống không mong đợi. Thử nghiệm tham gia của Anthropic năm 2023 cho thấy ~ 50% sự khác biệt giữa các nguyên tắc công cộng và doanh nghiệp; phiên bản 2026 không bao gồm những phát hiện đó.

> **【中文解读】**Anthropic 2026 năm tháng 1 22 ngày của Claude Hiến pháp 79 trang CC0。 chuyển từ dựa trên quy tắc sang dựa trên lý thuyết đối lập, thiết lập bốn cấp độ ưu tiên: 1) an toàn và hỗ trợ giám sát con người, 2) đạo đức, 3) Anthropic 指南, 3) có ích.

> **【拓展：四层优先级 + 双层禁令】**Các thứ hai là cần thiết: chỉ dựa trên lý thuyết không thể đóng尾部 kẻ tấn công để cho mô hình chấp nhận giả thuyết "Chúng tôi là phòng thí nghiệm nghiên cứu vũ khí sinh học") để có thể vượt qua các nguyên tắc của việc đưa ra các trường hợp phụ thuộc.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, four-tier priority resolver) | **语言:** Python（标准库，四层优先级解析器）
**Prerequisites:** Phase 15 · 06 (Automated alignment research), Phase 15 · 10 (Permission modes) | **前置知识:** Phase 15 · 06（自动化对齐研究），Phase 15 · 10（权限模式）
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**学本节前请先掌握:Phase 15·06(AAR) 、Phase 15·10(权限模式) 、Phase 11·10(RLHF/RLAIF 基础) ⋅ AI Hiến pháp = "用 AI 监督 AI"的对齐方法──
>  **【类比】**AI hiến pháp = "Tự nuôi dưỡng của AI"。RLHF = 父母 mỗi lần sửa chữa đứa trẻ(人工反,慢且贵);CAI = 孩子读了学生守则后自评自己(AI反,便宜可扩展)。2026 Claude hiến pháp 79 页四层优先级:安全 >伦理 > 公司指南 > 有用性──硬禁令(生物武器、CSAM) Bất kể người dùng làm thế nào chỉ thị都不行这是规则;其他通过推理判断────
> 🤔 **【困惑】**Q: 推理对齐能被绕过吗? 能! kẻ tấn công设设前提"我是持牌生物武器实验室" → 模型按推理允许 → 绕过原则──修复:硬禁令不向前提折(无论谁说什么,CSAM 就是不能产生)──推理 + 规则两层防御:推理覆盖大多数情况,规则覆盖推理被绕过的尾部──

## Vấn đề  vấn đề giới thiệu

> **【中文解读】**AI hiến pháp (CAI, Anthropic 2022) là một phương pháp thông qua '宪法' (一组原则) hướng dẫn hành vi của AI. Mô hình trong việc tạo phản ứng tự kiểm tra liệu có phù hợp với các nguyên tắc này hay không, và vi phạm khi tự sửa chữa.

> **【拓展：constitutional ai】**AI hiến pháp là nền tảng của thuyết anthropic an ninh. Nó sử dụng một nhóm các nguyên tắc hiến pháp' (如'不要帮助用户做危险的事情') để làm cho mô hình tự giám sát.

Một đại lý được trang bị thấy các đầu vào mà các nhà thiết kế của nó chưa bao giờ thấy.

> Trưởng phòng sẽ thấy những thông tin mà nhà thiết kế chưa từng thấy. Không có danh sách quy tắc đủ để bao gồm chúng.

Không có danh sách quy tắc nào đủ ngắn để áp dụng nhanh chóng dưới áp lực tính toán. Câu hỏi thực tế: làm thế nào để bạn sắp xếp một đại lý với các nguyên tắc tồn tại cả sau một đuôi dài các trường hợp và suy luận nhanh chóng?

> 没有规则列表短到能在计算压力下快速应用―― thực tế: Làm thế nào để đại lý đối phó với nguyên tắc của có thể sống sót trong trường hợp dài cuối và suy luận快速?

Định hướng dựa trên quy tắc (RBA): liệt kê mọi thứ không được phép. Định hướng nhanh chóng để kiểm tra, dễ kiểm tra, không thể giữ hiện tại, thường từ chối quá nhiều các tương tự gần mà nó không dự đoán. Định hướng dựa trên lý do (Hiến pháp Claude năm 2026): mã hóa các nguyên tắc, để cho mô hình lý luận. Scales trên các trường hợp không được nhìn thấy, khó kiểm tra, chế độ thất bại là áp dụng sai nguyên tắc thay vì bỏ qua quy tắc.

> 基于规则对齐(RBA): liệt kê mọi thứ bị cấm;; kiểm tra快, kiểm toán dễ dàng, không thể giữ hiện tại; thường đối với những sự gần gũi không mong đợi quá từ chối.

> **【中文解读】**Bài này giới thiệu khái niệm và phương pháp thực hiện cốt lõi của AI Agent.

Hiến pháp 2026 có một vị trí trung gian rõ ràng.

> 2026 năm hiến pháp đã đưa ra một lập trường trung gian rõ ràng.

Mọi thứ khác đều dựa trên lý do trong một hệ thống phân cấp bốn cấp: an toàn và hỗ trợ giám sát của con người trước hết; đạo đức thứ hai; các hướng dẫn được tuyên bố bởi Anthropic thứ ba; hữu ích cuối cùng. Các nhà điều hành có thể điều chỉnh các mặc định trong khu vực mã mềm nhưng không thể chạm vào lệnh cấm mã cứng.

> Mọi thứ khác được dựa trên các lý thuyết trong bốn cấp độ: an ninh và hỗ trợ giám sát con người ưu tiên;伦理其次;Anthropic 声明的指南第三;有用性最后――

## Khái niệm cốt lõi

### Lớp thứ ba cấp độ ưu tiên

1. **Safety and supporting human oversight.**Tối cao nhất. Mô hình ưu tiên không làm suy yếu khả năng của con người và Anthropic để giám sát và sửa chữa AI. Điều này không phải là "sự thận trọng"; cụ thể là "không hành động theo cách làm cho việc giám sát của con người trở nên khó khăn hơn".
   Trung ngữ翻译:**安全和支持人类监督。**最高──模型优先不破坏人类和人类 监督和纠正 AI 的能力──不是"谨慎";具体是"không làm cho việc giám sát con người trở nên khó khăn hơn"──
2. **Ethics.**Sự trung thực, tránh làm hại người, không lừa dối, không thao túng.
   Trung ngữ翻译:**伦理。**诚实、避免对人伤害、不欺骗、不操纵──冲突时取代 汉族指南──
3. **Anthropic guidelines.**Các quy tắc hoạt động Anthropic đã quyết định vấn đề: phạm vi sản phẩm, mô hình tương tác, những công cụ nào để sử dụng khi nào.
   Trung ngữ翻译:**Anthropic 指南。**Nhân văn quyết định quan trọng vận hành quy tắc: phạm vi sản phẩm, giao tiếp mô hình, làm thế nào sử dụng các công cụ.
4. **Helpfulness.**Tối thiểu, hữu ích nhất có thể trong các ưu tiên cao hơn.
   Trung ngữ翻译:**有用性。**Tối thiểu. Trong cấp độ ưu tiên cao nhất có thể hữu ích.

Khi các cấp độ xung đột, mức độ cao hơn thắng. Đây là hình dạng tương tự như các ưu tiên Unix hoặc mạng QoS  khung được thiết kế để tạo ra độ phân giải dự đoán, không nhất thiết là hành vi tốt nhất trên bất kỳ trục nào.

> 层冲突时高者赢── đây là một khuôn khổ tương tự như Unix  ưu tiên hoặc mạng QoS  khuôn khổ nhằm tạo ra phân tích có thể dự đoán được, chứ không phải là hành vi tốt nhất trên một trục.

### Thiết lập lệnh cấm cứng so với mặc định mềm 硬编码禁令 so với 软编码默认

**Hardcoded:**

> **硬编码：**

- Tăng cường vũ khí sinh học / CBRN
  Trung ngữ翻译:生物武器 / CBRN 提升
- CSAM
  Trung ngữ翻译:CSAM (CSAM)
- Các cuộc tấn công vào cơ sở hạ tầng quan trọng
  Trung ngữ翻译: đối với các cuộc tấn công cơ sở hạ tầng quan trọng
- Sự lừa dối của người dùng về danh tính của mô hình khi được hỏi trực tiếp
  Trung文翻译:被直接问时对模型身份欺骗用户

Người vận hành không thể bỏ qua những điều này. Người dùng không thể bỏ qua những điều này. Chúng được thực thi ở mức độ trọng lượng mô hình khi có thể (trình đào tạo AI Hiến pháp / RLHF) và ở lớp suy luận khi không.

> 操作员 không thể phủ nhận được những điều này. Người dùng không thể phủ nhận được những điều này.

**Soft-coded defaults (operator-adjustable):**

> **软编码默认（操作员可调）：**

- Dường độ phản hồi mặc định
  Trung ngữ翻译:响应长度默认
- phạm vi hiện tại (chương tự có thể từ chối các chủ đề ngoài việc triển khai của nhà khai thác)
  Trung văn翻译:主题范围模型可拒绝操作员部署外的主题)
- Thiết kế (thông thức vs bình thường)
  Trung文翻译:风格(正式 vs 随意)
- Các mô hình sử dụng công cụ
  Trung ngữ翻译:工具使用模式

Các điều chỉnh của nhà điều hành xảy ra trong một giới hạn được tuyên bố. Nhà điều hành không thể loại bỏ các lệnh cấm có mã cứng bằng cách đổi tên chúng.

> 操作员调整发生在声明边界内――操作员 không thể thông qua đổi tên chuyển lệnh mã hóa cứng――

### Lớp huấn luyện CAI 2022

AI Hiến pháp ban đầu (Bai et al., 2022) đã đào tạo sự vô hại:

> Đạo luật AI (Bây 等人, 2022)

1. Tạo phản ứng cho một bộ các lời nhắc nhở.
   Trung文翻译:对一组提示生成响应──
2. Hãy yêu cầu mô hình chỉ trích mỗi phản ứng chống lại hiến pháp (quan tắc rõ ràng).
   Trung ngữ翻译:要求模型对照宪法(显式原则) phê bình mỗi响应。
3. Xem xét lại câu trả lời dựa trên lời chỉ trích.
   Trung văn翻译:基于批评修订响应──
4. RLAIF (tiến thức tăng cường từ phản hồi AI) trên các cặp được sửa đổi.
   Trung ngữ翻译:在修订对上 RLAIF (trên tiếng Anh từ AI 反的强化学习)

Kết quả: một mô hình từ chối các yêu cầu gây hại với những lời giải thích nguyên tắc, chứ không phải từ chối tổng quát. Hiến pháp 2026 sử dụng một hậu duệ của đào tạo này cộng với đào tạo sau sau bổ sung về hệ thống phân cấp cấp rõ ràng.

> Kết quả: dựa trên một cách giải thích về nguyên tắc thay vì một cách nói chung từ chối để từ chối mô hình yêu cầu gây hại.

### Định hướng dựa trên lý do nào bắt và bỏ lỡ dựa trên lý luận về việc bắt và bỏ lỡ những gì

**Catches:**

> **捕获：**

- Sự kết hợp không mong đợi của các nguyên thủy được phép khi nguyên tắc áp dụng rõ ràng.
  Trung ngữ翻译:原则清晰适用的允许原语的未预期组合──
- Những yêu cầu mới mẻ gần giống với những yêu cầu cấm.
  Trung文翻译:禁止请求的近似类似物新请求──
- Những cuộc tấn công kỹ thuật xã hội dựa trên "bạn không nói X bị cấm".
  Trung ngữ翻译:依赖"你没说X被禁止" của công nghệ xã hội tấn công.

**Misses:**

> **遗漏：**

- Các cuộc tấn công khai thác nguyên tắc không rõ ràng ("người dùng yêu cầu điều này vì vậy hữu ích nói có").
  Trung ngữ翻译:利用原则模糊的攻击" người dùng cần điều này để hữu ích nói có thể")
- Các kịch bản mà hai nguyên tắc xung đột theo cách không mong đợi, và thứ tự cấp độ là mơ hồ.
  Trung ngữ翻译:两个原则以未预期方式冲突且层次顺序模糊的场景──
- Trở về chậm trong nguyên tắc giải thích trên chu kỳ đào tạo (sự giải thích lại).
  Trung文翻译:跨训练周期的原则解释缓慢漂移 (缓慢漂移)

### Cuộc thử nghiệm tham gia năm 2023

Anthropic đã tiến hành một thí nghiệm năm 2023 so sánh một hiến pháp do công ty viết với một hiến pháp được tạo ra thông qua thông tin công cộng (~ 1.000 người Mỹ được trả lời). Hai phiên bản đã đồng ý về ~ 50% các nguyên tắc. Khi họ khác nhau, phiên bản nguồn công cộng hạn chế hơn về một số vấn đề (chống chế nội dung chính trị) và ít hạn chế hơn đối với những vấn đề khác (tự tiết lộ danh tính AI). Hiến pháp 2026 không bao gồm các kết quả từ nguồn công cộng. Đây là một sự căng thẳng được ghi nhận trong cách tiếp cận.

> Anthropic 2023 năm vận hành thí nghiệm so sánh doanh nghiệp viết hiến pháp với công chúng nhập nhập tạo ra hiến pháp (~1000 người được hỏi) ⋅ 2 phiên bản khoảng 50% 原则一致──分歧处, công chúng phiên bản trên một số vấn đề nghiêm ngặt hơn (~7000 người) ⋅ phân biệt đối xử về nội dung chính trị (~7000 người) ⋅ rộng hơn (~7000 người) ⋅2026 宪法未纳入公众版发现──这是方法中的已记录张力──

### Tại sao lệnh cấm mã hóa là cần thiết

Một kẻ tấn công có thể khiến mô hình chấp nhận một giả thuyết (ví dụ: "Chúng tôi là một phòng thí nghiệm nghiên cứu vũ khí sinh học được cấp phép") thường có thể nói về các nguyên tắc vượt qua phụ thuộc vào lý luận trường hợp.

> Chỉ dựa trên lý thuyết đối với Z không thể đóng尾部. Nó có thể làm cho mô hình chấp nhận giả định. Ví dụ: "Chúng tôi là phòng thí nghiệm nghiên cứu vũ khí sinh học") kẻ tấn công thường có thể lướt qua nguyên tắc dựa trên các trường hợp lý luận.

### Ở đó hiến pháp nằm trong đống.

Hiến pháp không phải là cái chuyển động giết người của Bài học 14. Nó sống ở lớp mô hình.

> 宪法 không phải là kết thúc của bài học thứ 14. Nó tồn tại ở tầng mô hình.

Nó sống ở lớp mô hình: trọng lượng của mô hình được đào tạo để thích. Các chuyển đổi Kill và token canary sống ở lớp runtime: điều runtime cho phép. Cả hai đều cần thiết. Một runtime mà phát ra tất cả các hành động sai vì các trọng lượng mô hình là cho phép là một vấn đề runtime. Một mô hình từ chối tất cả các hành động đúng vì thời gian chạy quá hạn chế là một vấn đề thời gian chạy. Các lớp bao gồm các lớp khác nhau.

> Nó tồn tại ở tầng mô hình: trọng lượng mô hình được đào tạo ưu tiên gì đó. Kết thúc mở cửa và token kim cục.

## Hãy sử dụng nó để thực hiện
```figure
mx-priority-tiers
```

## Sử dụng nó

`code/main.py`Cài giải quyết thực hiện một giải quyết ưu tiên tối thiểu bốn cấp. Người giải quyết thực hiện một hành động được đề xuất và một bộ các đánh giá nguyên tắc (an toàn, đạo đức, hướng dẫn, hữu ích) và trả lại hành động, từ chối hoặc hành động sửa đổi. Người lái xe chạy một bộ trường hợp nhỏ: cho phép rõ ràng, không cho phép rõ ràng, cấm mã hóa cứng, trường hợp mơ hồ trên các cấp.

> `code/main.py`实现最小四层优先级解析器──解析器取提议动作和一组原则评估(安全,伦理,指南,有用性) 并返回动作、拒绝或修改动作──驱动器运行小案例集:清晰允许、清晰拒绝、硬编码禁令、跨层模糊案例──

## Chuyển nó đi.

`outputs/skill-constitution-review.md`kiểm tra lớp hiến pháp của một triển khai: mã cứng, mã mềm, nơi mà người vận hành có thể điều chỉnh, và liệu hệ thống phân cấp bốn cấp thực sự là lệnh giải pháp hay không.

> `outputs/skill-constitution-review.md`审计部署的宪法层:什么硬编码什么软编码什么操作员在哪可调调四层层是否真是解析顺序――

## Tập luyện bài tập

1. Đi chạy`code/main.py`- Cấm lệnh cấm cứng ngay cả khi tính hữu ích cao.
   Trung ngữ翻译:运行 `code/main.py`❖ xác nhận tính hữu ích ❖ kiểm soát các hệ thống phân tích sẽ được sửa đổi dựa trên đạo đức;

2. Đọc Hiến pháp Claude (tổ chức, 79 trang, CC0). Chọn một nguyên tắc mà bạn cho là chưa được xác định rõ ràng.
   Trung ngữ翻译:阅读Claude Constitution(公开,79页,CC0)。识别你认为缺规范的一个原则──写两段解释具体模糊并提议更紧的表述──

3. Thiết kế một thiết lập mặc định có mã mềm cho một đại lý hỗ trợ khách hàng. Điều gì mà người vận hành điều chỉnh? Điều gì mà người vận hành không thể chạm vào? Định lý mỗi ranh giới.
   Trung ngữ翻译:为客服代理 设计软编码默认集.

4. Đọc bài báo CAI năm 2022 của Bai et al. Mô tả một trường hợp mà vòng lặp phê bình và sửa đổi của AI Hiến pháp sẽ tạo ra kết quả tồi tệ hơn quy tắc chung.
   Trung văn翻译:阅读 Bai 等人 2022 CAI 论文。 mô tả AI Hiến pháp  phê bình- sửa đổi vòng lặp tạo ra hơn một quy tắc 较差结果的一个案例──识别类别。

5. Thử nghiệm tham gia năm 2023 của Anthropic cho thấy khoảng 50% sự khác biệt giữa các nguyên tắc công cộng và doanh nghiệp. Chọn một loại nơi điều này quan trọng cho việc triển khai sản xuất (ví dụ, trung lập chính trị). đề xuất một thiết kế cho phép các nhà khai thác thể hiện các giá trị của riêng họ trong khi các lệnh cấm cứng vẫn không bị ảnh hưởng.
   Trung ngữ翻译:Anthropic 2023 参与式实验发现公众和企业原则约50% 分歧──选择一个对生产部署重要的类别──例如政治中立──提议让操作员表达自己的价值观同时硬编码禁令不变的设计──

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| Constitutional AI | "Anthropic's alignment method" | Self-critique + RLAIF against a written constitution |
| Constitutional AI | "Anthropic 的对齐方法" | 对照书面宪法的自我批评 + RLAIF |
| Reason-based alignment | "Principles, not rules" | Model reasons over principles to handle unseen cases |
| 基于推理对齐 | "原则而非规则" | 模型对原则推理以处理未见案例 |
| Hardcoded prohibition | "Never do X" | Rule-based prohibition no operator or user can override |
| 硬编码禁令 | "永不做 X" | 操作员或用户不能覆盖的基于规则的禁令 |
| Soft-coded default | "Operator-adjustable" | Behaviour within a declared bound, operator controls |
| 软编码默认 | "操作员可调" | 声明边界内的行为，操作员控制 |
| Four-tier hierarchy | "Priority order" | safety > ethics > guidelines > helpfulness |
| 四层层次 | "优先级顺序" | 安全 > 伦理 > 指南 > 有用性 |
| RLAIF | "AI feedback RL" | RL where the reward comes from model-generated critiques |
| RLAIF | "AI 反馈 RL" | 奖励来自模型生成批评的 RL |
| Participatory constitution | "Public-sourced principles" | 2023 Anthropic experiment; ~50% divergence from corporate |
| 参与式宪法 | "公众来源原则" | 2023 Anthropic 实验；与企业约 50% 分歧 |
| Principle drift | "Interpretation slip" | Slow change in how the model reads a fixed principle text |
| 原则漂移 | "解释滑移" | 模型如何读取固定原则文本的缓慢变化 |

## Xem thêm 延伸阅读

- [Anthropic — Claude's Constitution (January 2026)](https://www.anthropic.com/news/claudes-constitution) Tài liệu CC0 dài 79 trang.
  中文翻译:79 页 CC0 文档。
- [Bai et al. — Constitutional AI: Harmlessness from AI Feedback](https://www.anthropic.com/research/constitutional-ai-harmlessness-from-ai-feedback) 2022 gốc.
  Trung văn翻译:2022 原始版本──
- [Anthropic — Collective Constitutional AI (2023)](https://www.anthropic.com/research/collective-constitutional-ai-aligning-a-language-model-with-public-input) thí nghiệm tham gia.
  Trung文翻译: tham gia thử nghiệm.
- [Anthropic — Responsible Scaling Policy v3.0](https://anthropic.com/responsible-scaling-policy/rsp-v3-0) nơi hiến pháp nằm trong hàng RSP.
  Trung ngữ翻译:宪法在 RSP 中的位置──
- [Anthropic — Measuring agent autonomy in practice](https://www.anthropic.com/research/measuring-agent-autonomy) Vai trò của Hiến pháp trong các triển khai theo chiều dài.
  Trung ngữ翻译:宪法在长程部署中的角色──
