# Nhà khoa học AI v2  Tiếp tục nghiên cứu tự trị cấp độ  Nhà khoa học AI v2  工作坊 cấp tự nghiên cứu

> Nhà khoa học AI của Sakana v2 (Yamada et al., arXiv:2504.08066) chạy vòng lặp nghiên cứu đầy đủ: giả thuyết, mã, thí nghiệm, số liệu, viết, nộp. Đây là hệ thống đầu tiên có đánh giá đồng nghiệp được tạo ra trên giấy qua tại một hội thảo ICLR 2025. Đánh giá độc lập (Beel et al.) cho thấy 42% thí nghiệm thất bại từ lỗi mã hóa và đánh giá văn học thường đánh giá sai các khái niệm được thiết lập là mới. Các bác sĩ của Sakana cảnh báo rằng hệ thống mã hóa thực hiện mã LLM và khuyên nên cô lập Docker. Cả hai nửa của bức tranh là điểm.

> **【中文解读】**Sakana's AI Scientist v2(Yamada 等人,arXiv:2504.08066) chạy một vòng nghiên cứu hoàn chỉnh: giả định, lập trình, thí nghiệm, biểu đồ, viết, gửi đi. Nó là bài viết đầu tiên có sản xuất qua ICLR 2025 工作坊 đồng thời đánh giá hệ thống.

> **【拓展：开放式研究的代价】**AlphaEvolve và DGM đều có "hỗ máy kiểm tra được đánh giá" đơn vị kiểm tra hoặc基准. Nghiên cứu không có: luận văn đánh giá bởi nhà phê bình, chứ không phải đơn vị kiểm tra.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, research-loop state-machine toy) | **语言:** Python（标准库，研究循环状态机玩具）
**Prerequisites:** Phase 15 · 03 (AlphaEvolve), Phase 15 · 04 (DGM) | **前置知识:** Phase 15 · 03（AlphaEvolve），Phase 15 · 04（DGM）
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**Học本节前请先掌握:Phase 15·03-04(AlphaEvolve/DGM) Phase 14·30+(工作台 Agent 实践) 学术论文写作基础──AI Scientist = 开放式研究任务,评估器是"同行评审"(弱信号),所以安全模型完全不同──
>  **【类比】**AI Scientist = "AI 博士生"──AlphaEvolve/DGM = 工程师(评估器=单元测试,强信号);AI Scientist = 博士生(评估器=审稿人,弱信号)──同样跑实验-评估-代循环,但弱信号评估让 Agent 容易欺骗自己42% 的实验代码有错误,文献综述把已知概念当新发现──修复:(1) Docker 隔离(必须执行 LLM 代码沙箱);(2) 人类复核(披露 AI 生成);(3) 引入强信号检查(如复现性测试) 

## Vấn đề  vấn đề giới thiệu

Nghiên cứu là một nhiệm vụ không có kết thúc.

> Nghiên cứu là nhiệm vụ mở.

Không giống như tìm kiếm thuật toán của AlphaEvolve hoặc tự sửa đổi giới hạn của DGM, kết quả nghiên cứu không có tiêu chí chính xác có thể kiểm tra bằng máy. Một bài báo được đánh giá bởi các nhà đánh giá, chứ không phải là các thử nghiệm đơn vị. Điều đó làm cho vòng lặp khó khăn hơn để đóng  và có giá trị hơn nếu đóng, bởi vì nghiên cứu là nơi tiến bộ hợp chất sống.

> Không giống như các thuật toán tìm kiếm của AlphaEvolve hoặc DGM, kết quả nghiên cứu không có tiêu chuẩn chính xác có thể kiểm tra được bởi máy.

AI Scientist v1 (Sakana, 2024) đã đóng vòng lặp bằng cách bắt đầu từ các mẫu do con người viết. LLM đã thực hiện các thí nghiệm trong một nền cố định. AI Scientist v2 (Yamada et al., 2025) loại bỏ yêu cầu mẫu bằng cách sử dụng tìm kiếm cây nhân viên với vòng lặp phê bình mô hình ngôn ngữ thị giác. Hệ thống tạo ra ý tưởng, thực hiện thí nghiệm, tạo ra số liệu, viết bài báo và lặp lại phản hồi của nhà phê bình.

> AI Scientist v1(Sakana,2024) thông qua mô hình được viết bởi con người bắt đầu kết thúc vòng lặp.LLM trong khung chữ cố định để lấp đầy thí nghiệm.AI Scientist v2(Yamada 等人,2025) thông qua sử dụng vòng lặp đánh giá mô hình ngôn ngữ có hình ảnh.

> **【中文解读】**AI Scientist v2 (Sakana, 2025) 运行完整的研究循环:假设,编码,实验,图表,论文撰写和提交――它 là hệ thống đánh giá đồng thời của AI Scientist v2 (Sakana, 2025) 运行完整的研究循环:假设,编码,实验,图表,论文撰写和提交―― nó là hệ thống đầu tiên có sản xuất论文 thông qua ICLR 2025 工作坊同行评审―― nhưng đánh giá độc lập cho thấy 42% các thí nghiệm vì lỗi lập trình thất bại, các văn bản tổng hợp thường sẽ được đánh dấu các khái niệm đã được thiết lập là mới── cả hai mặt đều là sự thật――

Phán quyết đánh giá đồng nghiệp: một bài báo được tạo ra bởi v2 đã được chấp nhận tại một hội thảo ICLR 2025 (với tiết lộ). Phán quyết đánh giá độc lập: hệ thống này không đáng tin cậy. Cả hai đều đúng.

> 同行评审结论:一篇 v2 生成的论文被ICLR 2025 工作坊接受(附带披露) ・独立评估结论:系统远非可靠──两者都是事实──

## Khái niệm cốt lõi

### Kiến trúc, kiến trúc.

1. **Idea generation.**LLM đề xuất ý tưởng nghiên cứu được điều chỉnh trên một chủ đề và văn học trước đó. v1 sử dụng mẫu; v2 sử dụng tìm kiếm cơ quan trên một không gian giả thuyết.
   Trung ngữ翻译:**想法生成。**LLM dựa trên chủ đề và các văn bản trước đây đưa ra ý tưởng nghiên cứu.
2. **Novelty check.**Một bước tìm kiếm văn học kiểm tra xem ý tưởng đã được xuất bản hay không. Đây là bước mà đánh giá của Beel et al. đã tìm thấy nhãn sai  các phương pháp được thiết lập thường được phân loại là mới.
   Trung ngữ翻译:**新颖性检查。**文献检查步骤检查想法是否已发表──这是 Beel 等人评估发现错误标记的步骤已建立的方法频繁被分类为新──
3. **Experiment plan.**Đặc vụ đã thiết kế một quy định thí nghiệm và viết mã.
   Trung ngữ翻译:**实验计划。**Agent 起草实验协议并编写代码──
4. **Execution.**Mã chạy trong một hộp cát. Các lỗi được đưa lại vào vòng lặp thử lại. Trong các phép đo của Beel et al., 42% thí nghiệm thất bại vì lỗi mã hóa ở giai đoạn này.
   Trung ngữ翻译:**执行。**Trong các phép đo của người khác, 42% thí nghiệm trong giai đoạn này do lỗi lập trình thất bại.
5. **Figure generation.**Một mô hình ngôn ngữ thị giác đọc các con số được tạo ra và viết lại chúng để rõ ràng hơn. Đây là sự bổ sung kỹ thuật chính của v2.
   Trung ngữ翻译:**图表生成。**视觉语言模型读取生成图表并为清晰性重写它们──这是 v2 的关键技术添加──
6. **Writeup.**LLM soạn thảo một bài báo, lặp lại với một nhà phê bình nội bộ.
   Trung ngữ翻译:**撰写。**LLM 起草论文,与内部审稿人代──
7. **Optional: submission.**Bài báo được gửi đến một địa điểm.
   Trung ngữ翻译:**可选：提交。**论文提交到会议――

### Kết quả chấp nhận workshop có nghĩa là gì

Một bài báo được tạo ra bởi v2 đã vượt qua đánh giá của các đồng nghiệp tại một hội thảo ICLR 2025. Các tác giả tiết lộ nguồn gốc của bài báo cho ủy ban chương trình. Việc chấp nhận là một điểm dữ liệu; đó không phải là giấy phép để tuyên bố hệ thống "phát nghiên cứu".

> Một bài báo được phát triển trong ICLR 2025 工作坊 thông qua đánh giá đồng nghiệp.

Tầm quan trọng: các bài báo hội thảo là một thanh thấp hơn so với các bài báo hội nghị chính. Tin xét của các đồng nghiệp là tiếng ồn; một phần nhỏ của các bài đăng được chấp nhận vào một ngày nào đó. Một thành công là một bằng chứng về khái niệm, không phải là một tuyên bố độ tin cậy. Bài báo Nature 2026 ghi lại vòng lặp cuối đến cuối và chính nó được đồng tác giả bởi các nhà nghiên cứu con người; nó không phải là "hệ thống đã viết một bài báo Nature".

> 重要背景:工作坊论文的门低于主会议论文──同行评审有噪音;任何一天都有一小部分提交被接受──一次成功是概念证明,不是可靠性声明──Nature 2026 论文记录端到端循环,本身由人类研究人员共同撰写;不是"系统写了一篇 Nature 论文"──

### Những gì mà đánh giá độc lập đã tìm thấy

Beel et al. (arXiv:2502.14297) đã tiến hành một đánh giá bên ngoài.

> Beel 等人 ((arXiv:2502.14297) đã thực hiện các bài đánh giá bên ngoài:

- **Experiment failures.**42% thí nghiệm thất bại vì lỗi mã hóa (thu nhập sai, không phù hợp hình dạng, biến không xác định).
  Trung ngữ翻译:**实验失败。**42% thí nghiệm đã bị lỗi mã hóa, không thành công, không phù hợp, không xác định các biến thể.
- **Novelty mislabeling.**Bước tìm lại văn học thường đánh dấu các khái niệm đã được thiết lập là mới mẻ.
  Trung ngữ翻译:**新颖性错误标记。**文献检索步骤频繁将已建立的概念标记为新──这是研究界的幻觉等效──
- **Presentation-quality gap.**Việc phê bình hình ảnh ngôn ngữ thị giác đã tạo ra hình ảnh cấp ấn phẩm, che giấu những điểm yếu thử nghiệm cơ bản.
  Trung ngữ翻译:**呈现质量差距。**视觉语言图表评审产生出版级视觉效果, che giấu điểm yếu của các thí nghiệm cơ bản.

Một hệ thống tạo ra kết quả thuyết phục mà không thực hiện nghiên cứu thuyết phục là nguy hiểm hơn, không an toàn hơn, so với một hệ thống thất bại rõ ràng.

> Một phát hiện cuối cùng rất quan trọng cho giai đoạn này: tạo ra một hệ thống nghiên cứu đáng tin cậy nhưng chưa thực hiện một nghiên cứu đáng tin cậy, có nguy hiểm hơn và không an toàn hơn so với hệ thống thất bại rõ ràng.

Việc đánh giá phải đạt đến các yêu cầu cơ bản, không dừng lại ở con số.

> 评估 phải chạm vào tuyên bố cấp dưới, thay vì dừng lại trên biểu đồ.

### Vấn đề trốn thoát khỏi hộp cát.

Đồ lưu trữ của Sakana README cảnh báo:

> Sakana  kho của riêng mình README 警告:

> Do tính chất của phần mềm này, mà thực hiện mã được tạo bởi LLM, chúng tôi không thể đảm bảo an toàn. Có những rủi ro của các gói nguy hiểm, truy cập web không kiểm soát, và sinh ra các quy trình không mong muốn. Sử dụng với rủi ro của riêng bạn và xem xét cách ly Docker.

> Vì phần mềm này thực hiện mã hóa LLM sinh, chúng tôi không thể đảm bảo an toàn.

Đây là hình thức hoạt động của tự trị trong một miền không được xác minh. LLM viết mã; mã chạy; mã có thể làm bất cứ điều gì mà quá trình được phép làm. Không có hộp cát hạn chế các hệ thống tập tin, mạng và hành động quy trình, bất kỳ đại lý nghiên cứu tự hướng nào có thể lọc dữ liệu, đốt tính toán hoặc tự viết lại.

> Đây là hình thức hoạt động tự chủ trong lĩnh vực chưa được chứng minh. LLM viết mã; mã chạy; mã có thể làm quá trình được phép bất cứ điều gì. Không có hạn chế cứng về hệ thống tài liệu, mạng và quá trình hoạt động, bất kỳ đại lý nghiên cứu tự do nào đều có thể tiết lộ dữ liệu, đốt cháy tính toán hoặc viết lại bản thân.

Câu chuyện sandbox của AlphaEvolve dễ dàng hơn vì đánh giá của nó chặt chẽ. Loop của AI Scientist v2 chạy mã mở với mục tiêu mở. Đó là lý do tại sao nó cần sự cô lập mạnh mẽ hơn (Docker tối thiểu; seccomp / gVisor được ưa thích) và một đánh giá thủ công của mỗi bài đăng trước khi rời khỏi hệ thống.

> AlphaEvolve's sandbox mô tả dễ dàng hơn, vì bộ đánh giá của nó nghiêm ngặt. AI Scientist v2 của vòng lặp sử dụng mục tiêu mở hoạt động mở mã. Đó là lý do tại sao nó cần được tách biệt hơn.

### V2 nằm ở phía trước của v2

| System | Target | Output kind | Evaluator | Known failure |
|---|---|---|---|---|
| 系统 | 目标 | 输出类型 | 评估器 | 已知失败 |
| AlphaEvolve | algorithms | code | unit + benchmark | bounded by evaluator rigor |
| AlphaEvolve | 算法 | 代码 | 单元 + 基准 | 受评估器严谨性约束 |
| DGM | agent scaffolding | code | SWE-bench | reward hacking |
| DGM | Agent 脚手架 | 代码 | SWE-bench | 奖励篡改 |
| AI Scientist v2 | research papers | text + code + figures | peer review (weak) | experiment failures, mislabeling, polish masking weakness |
| AI Scientist v2 | 研究论文 | 文本 + 代码 + 图表 | 同行评审（弱） | 实验失败、错误标记、修饰掩盖弱点 |

v2 có trình đánh giá tự động yếu nhất trong ba, bề mặt đầu ra rộng nhất, và con đường ngắn nhất đến các hiện vật công cộng.

> V2 Trong số ba người có máy đánh giá tự động yếu nhất, đường dẫn sản phẩm công khai rộng nhất và đường dẫn sản phẩm công khai ngắn nhất.

Các bộ điều khiển hoạt động (thùng cát, đánh giá, tiết lộ) đang thực hiện hầu hết công việc an toàn.

> 操作控制 (nước kiểm tra, kiểm tra, công bố) đã thực hiện hầu hết công việc an ninh.

## Hãy sử dụng nó để thực hiện
```figure
mx-research-loop
```

## Sử dụng nó

`code/main.py`mô phỏng vòng v2 như một máy trạng thái: ý tưởng → kiểm tra tính mới → thí nghiệm → hình thức → viết lên → đánh giá → chấp nhận-hoặc lặp lại. Mỗi trạng thái có một xác suất thất bại có thể cấu hình được rút ra từ các phát hiện của Beel et al.

> `code/main.py`将 v2 循环模拟为状态机:想法 → 新性检查 → 实验 → 图表 → 写 → 审稿 → 接受或代―― mỗi trạng thái có từ Beel 等人发现中提取的可配置失败概率──运行模拟器 N个循环并计数:

- Có bao nhiêu ý tưởng đạt đến sự phục vụ.
  Trung文翻译:多少想法到达提交──
- Bao nhiêu bài nộp sẽ có một lỗi thử nghiệm quan trọng giấy bóng được che giấu.
  Trung ngữ翻译:多少提交会有修饰论文隐藏的关键实验缺陷──
- Làm thế nào các ngân sách thử lại giao dịch với chất lượng so với năng suất.
  Trung ngữ翻译:重试预算如何衡量质量与产量之间权衡──

## Chuyển nó đi.

`outputs/skill-ai-scientist-sandbox-review.md`là một danh sách kiểm tra hai cửa cho bất cứ thứ gì được sản xuất bởi một đại lý vòng nghiên cứu trước khi nó rời khỏi hộp cát.

> `outputs/skill-ai-scientist-sandbox-review.md`                                                                                                                                                                                                                                                              

## Tập luyện bài tập

1. Đi chạy`code/main.py`với các tham số mặc định. Phân tích nào của loop chạy tạo ra một giấy " sạch "? Phân tích nào tạo ra một giấy với một lỗi thử nghiệm-lỗi hình ảnh phê bình được đánh bóng?
   中文翻译:使用默认参数运行 `code/main.py` Quá trình hoạt động vòng lặp tạo ra bài luận " sạch "? Quá trình nghiên cứu có bài báo có hình ảnh đánh giá sửa đổi thất bại của thí nghiệm?

2. Các mặc định đã sử dụng 42% / 25% của Beel et al.`--experiment-failure 0.20 --novelty-mislabel 0.10`và sau đó với `--experiment-failure 0.60 --novelty-mislabel 0.40`- Làm thế nào để chia sẻ tốt nhưng không tốt thay đổi giữa hai vòng?
   中文翻译:默认已使用Beel等人的 42% / 25%──用 `--experiment-failure 0.20 --novelty-mislabel 0.10`Tránh rồi dùng`--experiment-failure 0.60 --novelty-mislabel 0.40`◊ Phụ thể thay đổi giữa hai chuyến đi được sửa chữa nhưng có lỗi như thế nào?

3. Đọc Sakanas AI Scientist v2 repo README về yêu cầu hộp cát. Hãy nêu tên hai hạn chế bổ sung (nên ngoài Docker) bạn sẽ áp dụng cho một chạy tự động nhiều ngày.
   Trung文翻译:阅读 Sakana AI Scientist v2 仓库 README 关于沙箱要求──命名你会为多日自主运行添加的两项额外限制(除Docker 外)──

4. Đọc Beel et al. Phần 4 về khoảng cách chất lượng trình bày. Thiết kế một đánh giá bổ sung để bắt được các giấy có vẻ đẹp đẹp nhưng có lỗi thí nghiệm.
   Trung ngữ翻译:阅读Beel 等人 第4节关于呈现质量差距――设计一个会捕获修改但实验有缺陷论文的额外评估器――

5. đề xuất một quy tắc đánh giá của con người cho kết quả của các đại lý nghiên cứu có quy mô tốt hơn "một tiến sĩ đọc mọi bài báo".
   Trung ngữ翻译:为研究 Agent 输出提议比"博士读每篇论文"扩展更好的人工审查协议──识别瓶并根据此设计──

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| AI Scientist v1 | "Sakana's templated research agent" | Filled experiments into a fixed scaffold |
| AI Scientist v1 | "Sakana 的模板研究 Agent" | 在固定脚手架中填充实验 |
| AI Scientist v2 | "Template-free research agent" | Agentic tree search with VLM figure critique |
| AI Scientist v2 | "无模板研究 Agent" | 带有 VLM 图表评审的 Agent 式树搜索 |
| Agentic tree search | "Branching research agent" | Expands multiple experiment plans in parallel; prunes by internal critic |
| Agent 式树搜索 | "分支研究 Agent" | 并行展开多个实验计划；由内部评论者修剪 |
| Vision-language critique | "VLM polish on figures" | Multimodal model reads figures and rewrites them for clarity |
| 视觉语言评审 | "VLM 修饰图表" | 多模态模型读取图表并为清晰性重写 |
| Literature retrieval | "Novelty check" | Searches prior work to confirm idea novelty — documented to mislabel |
| 文献检索 | "新颖性检查" | 搜索先前工作以确认想法新颖性——文档记录会错误标记 |
| Polish masking | "Pretty paper, broken research" | Presentation quality exceeds experimental quality; hides weaknesses |
| 修饰掩盖 | "漂亮论文，破碎研究" | 呈现质量超过实验质量；隐藏弱点 |
| Sandbox escape | "LLM code breaks out" | Agent-executed code does things the loop designer did not intend |
| 沙箱逃逸 | "LLM 代码逃逸" | Agent 执行的代码做循环设计者未预期的事 |

## Xem thêm 延伸阅读

- [Yamada et al. (2025). The AI Scientist-v2](https://arxiv.org/abs/2504.08066)- Báo.
  Trung ngữ:论文──
- [Sakana blog on the Nature 2026 publication](https://sakana.ai/ai-scientist-nature/) Tổng kết nhà cung cấp với bối cảnh đánh giá ngang hàng.
  Trung văn翻译:厂商摘要,含同行评审背景──
- [Beel et al. (2025). Independent evaluation of The AI Scientist](https://arxiv.org/abs/2502.14297) số đánh giá bên ngoài.
  Trung ngữ翻译:外部评估数字──
- [Sakana AI Scientist v1 paper](https://arxiv.org/abs/2408.06292) người tiền nhiệm được tạo mẫu.
  Trung ngữ翻译:模板化前身──
- [Anthropic — Measuring AI agent autonomy](https://www.anthropic.com/research/measuring-agent-autonomy) định hình rộng hơn về các cơ quan nghiên cứu mở.
  Trung ngữ翻译:开放式研究 Agent 的更宽框架──
