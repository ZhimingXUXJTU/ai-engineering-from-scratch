# Vai trò chuyên môn  Kế hoạch viên, phê bình, thực thi viên, kiểm tra viên 专业化 批评者 计划角色

> Sự phân hủy đa đại lý phổ biến nhất vào năm 2026: một đại lý lập kế hoạch, một thực hiện, một chỉ trích hoặc xác minh. MetaGPT (arXiv:2308.00352) chính thức hóa điều này như SOP được mã hóa thành lời nhắc vai trò  Giám đốc sản phẩm, kiến trúc sư, quản lý dự án, kỹ sư, kỹ sư QA  sau `Code = SOP(Team)`- Tôi không biết. ChatDev (arXiv:2307.07924) liên kết thiết kế, lập trình viên, nhà đánh giá, kiểm tra thông qua một "chỉa khóa trò chuyện" với "sự giải ảo thông tin" (chấp hành khách rõ ràng yêu cầu các chi tiết thiếu sót). Máy xác minh có thể chịu tải: Cemri et al. (MAST, arXiv:2503.13657) cho thấy mỗi sự thất bại đa đại lý có thể được theo dõi để xác minh bị mất hoặc bị hỏng. PwC báo cáo tăng độ chính xác 7x (10% → 70%) từ vòng xác thực cấu trúc trong CrewAI.

> **【中文解读】**Chương trình này giới thiệu chuyên môn hóa vai trò cho mỗi đại lý phân chia vai trò và chuyên môn rõ ràng, nâng cao hiệu quả toàn bộ đội ngũ.

> **【拓展：role specialization→具体应用】**角色专业化是 CrewAI's core psychological idea每个代理都有角色角色角色,目标,目标,目标,背景故事,背景故事. 背景故事. 背景故事. 背景故事. 背景故事. 背景故事. 背景故事. 背景故事. 背景故事. 背景故事. 背景故事. 背景故事. 背景故事. 背景故事. 背景故事. 背景故事. 背景故事. 背景故事. 背景故事. 背景故事. 背景故事. 背景故事. 背景故事. 背景故事. 背景故事. 背景故事. 背景故事. 实践表明,明确的角色定义可以显著提高多代理合作的效率. 具体专业化过度也存在风险 角色界过严格导致代理拒绝做'不是自己的责任'而不是必要操作.


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 16 · 04 (Primitive Model), Phase 16 · 05 (Supervisor) | **前置知识:** Phase 16 · 04 (Primitive Model), Phase 16 · 05 (Supervisor)
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**学本节前请先掌握:Phase 16·04-05(原语+Supervisor) ⋅本节是2026 最常见的多代理 分解模式:Planer + Critic + Executioner + Verifier。
>  **【类比】**角色专业化 = "电影制作团队"──Planner = 编剧(定方向)、Executor = 演员(执行)、Critic = 内审、Verifier = 质检员──MetaGPT、ChatDev、CrewAI 都用这种角色分解──Cemri 等人 MAST论文:所有多 Agent 失败都可追溯到"缺少或破损的验证人"验证是承重墙──PwC 案例:加验证人 让准确率从10% 到70% 7倍)──

##                                                                                                                                                                                                                                                               

Các hệ thống đa đại lý chung tạo ra đầu ra chung. Ba bộ lập trình trong một cuộc trò chuyện nhóm viết ba hương vị của cùng một mã trung bình. Bạn có thể thêm nhiều đại lý, thêm nhiều vòng, và vẫn không vượt qua ngưỡng chất lượng.

> Thông thường nhiều đại lý  hệ thống tạo ra thông thường đầu ra  3 bộ biên tập trong nhóm thảo luận viết ra 3 kiểu văn bản có cùng hương vị  Bạn có thể thêm nhiều đại lý  nhiều lượt, vẫn không thể vượt qua các cửa chất lượng 

Vấn đề không phải là số lượng mà là sự đồng nhất. Ba nhân tố giống nhau được giao cùng một nhiệm vụ sẽ tạo ra ba câu trả lời sai lầm tương tự. Họ chia sẻ cùng một điểm mù vì họ chia sẻ cùng một động tác và mô hình.

>  vấn đề không phải là số lượng mà là chất lượng. 三 相同的代理 给定相同任务会产生三相似错误答案.

Việc sửa chữa không phải là các đại lý hơn  nó là các đại lý khác nhau. Đề xuất các vai trò khác nhau. Cung cấp các công cụ phê bình mà người lập kế hoạch không có. Cung cấp cho người xác minh một bộ thử nghiệm khách quan. Bây giờ hệ thống có sự bất đồng nội bộ với sự sửa chữa có căn cứ, không chỉ là đoán song song.

> Phương pháp sửa chữa không phải là nhiều Agent mà là một Agent khác nhau                                                                                                                                                                                                                                                      

Sự thay đổi quan trọng: từ "các đại lý làm cùng một điều" đến "các đại lý làm những điều khác nhau". Sự song song mà không có chuyên môn hóa chỉ là đoán đắt tiền.

> 关键转变: Từ "More Agent Do the Same Thing" đến "Different Agent Do Different Thing"― không có sự đồng hành chuyên nghiệp hóa chỉ là một phỏng đoán đắt tiền― chuyên nghiệp hóa tạo ra để hệ thống bắt được sai lầm của mình không đối xứng―

## Khái niệm cốt lõi

### Bốn vai trò của các giáo pháp

**Planner.**Đọc mục tiêu, tạo ra một danh sách bước hoặc một thông số kỹ thuật Công cụ: lấy lại kiến thức, tài liệu.

> **规划者。**读取目标,产生步骤列表或规范──工具:知识检索、文档──输出: cấu trúc kế hoạch──

**Executor.**Đọc một kế hoạch từng bước, tạo ra vật liệu. Công cụ: các công cụ thực tế làm việc (compiler mã, shell, API client).

> **执行者。**Mỗi lần đọc một kế hoạch bước, tạo ra công cụ.

**Critic.**Đọc kết quả của người thực hiện chống lại ý định của người lập kế hoạch. Công cụ: truy cập chỉ đọc vào vật tạo, phân tích tĩnh.

> **批评者。**根据规划者意图阅读执行者输出──工具:对工件的只读访问、静态分析──输出:接受/拒绝及原因──

**Verifier.**Đọc các tác phẩm và chạy kiểm tra xác định. Công cụ: test runner, type checker, schema validator. Output: pass/fail với bằng chứng.

> **验证者。**读取工件并运行确定性检查──工具:测试运行器、类检查器、模式验证器──输出:通过/失败及证据──

Người phê bình là chủ quan, có ý kiến, thường dựa trên LLM. Người xác minh là khách quan, xác định, thường dựa trên mã.

> Người phê bình là chủ quan, có quan điểm, thường dựa trên LLM, xác nhận là khách quan, xác định, thường dựa trên mã, không phải là một vai trò.

Sự kết hợp của chúng là lỗi thiết kế đa đại lý phổ biến nhất. Một hệ thống chỉ có các nhà phê bình (LLM reviewers) có kết quả có thể tin được nhưng không đúng. Một hệ thống chỉ có các kiểm tra mã (chọn tra mã) có kết quả đúng nhưng xấu. Bạn cần cả hai: phê bình cho hương vị, kiểm tra cho sự chính xác.

> Để trộn chúng vào một cái là những lỗi thiết kế đa đại lý phổ biến nhất. Chỉ có những nhà phê bình (LLM) có thể nhận được kết quả giống như vậy nhưng không phải là sai.

### Mô hình SOP của MetaGPT

MetaGPT (arXiv:2308.00352) mã hóa các SOP kỹ thuật phần mềm như các lời nhắc vai trò:

> MetaGPT(arXiv:2308.00352)将软件工程 SOP 编码为角色提示:

Các quy trình hoạt động tiêu chuẩn biến công việc ad-hoc thành quá trình lặp lại. MetaGPT áp dụng điều này cho LLM.

> "SOP" framework lấy từ tổ chức nhân loại: quy trình hoạt động tiêu chuẩn sẽ chuyển đổi công việc tạm thời thành quy trình lặp lại.

- **Product Manager**- Ông nói.
  Trung ngữ翻译:**产品经理**编写 PRD。
- **Architect**tạo ra thiết kế hệ thống.
  Trung ngữ翻译:**架构师**产生系统设计――
- **Project Manager**chia các nhiệm vụ.
  Trung ngữ翻译:**项目经理**拆分任务──
- **Engineer**các thiết bị.
  Trung ngữ翻译:**工程师**实现──
- **QA Engineer**chạy các xét nghiệm.
  Trung ngữ翻译:**QA 工程师**运行测试──

Mỗi vai trò có một kế hoạch đầu vào/phục xuất nghiêm ngặt.`Code = SOP(Team)`Các SOP xác định biến một nhóm LLM thành một đường ống dự đoán.

> Mỗi vai diễn có một mô hình nhập/ xuất nghiêm ngặt.`Code = SOP(Team)`SOP sẽ biến một LLM  đội thành một dòng chảy dự đoán được.

Thông tin quan trọng: mã hóa dòng công việc của nhóm như mã, không phải như một cuộc trò chuyện. Mỗi vai trò LLM là một nút trong biểu đồ xác định; cấu trúc biểu đồ được viết bởi con người. LLM làm công việc địa phương; con người sở hữu dòng công việc toàn cầu.

> 关键洞察:将团队工作流编码为代码,而不是对话. Mỗi LLM 角色是确定性图中的节点.图结构由人类编写.

### Sự khước từ của ChatDev

ChatDev thêm một bước quan trọng: khi một người thực thi cần một chi tiết cụ thể không nằm trong kế hoạch, nó rõ ràng hỏi nhà thiết kế trước khi tiếp tục. Điều này ngăn chặn thất bại LLM cổ điển của phát minh chi tiết.

> ChatDev đã thêm một động thái quan trọng: Khi người thực hiện cần một chi tiết cụ thể trong một kế hoạch, nó sẽ hỏi rõ ràng nhà thiết kế trước khi tiếp tục.

Mô hình bắt được ảo giác ở nguồn gốc của chúng. Thay vì phát hiện các chi tiết đã được chế tạo sau sự kiện (khó), nó ngăn chặn việc chế tạo bằng cách yêu cầu người thực thi hỏi trước khi giả định. Chi phí là một chuyến đi trở lại thêm; lợi ích là sự chính xác.

> Mô hình này là một cách dễ dàng để ngăn chặn sự giả tạo.

Thực hiện: lời nhắc vai trò bao gồm "Khi bạn cần thông tin cụ thể mà bạn không được cung cấp, hãy hỏi vai trò liên quan bằng tên trước khi tạo ra kết quả".

> 实现:角色提示包括"When you need you not provided specific information, before generating output, according to the name ask related roles".""

### Tại sao người xác minh quan trọng nhất

Cemri et al. (MAST) đã theo dõi 1642 thất bại thực hiện đa đại lý. 21,3% là lỗ hổng xác minh  hệ thống gửi một câu trả lời không ai kiểm tra. 79% còn lại thường theo dõi trở lại "có một kiểm tra đã thất bại lặng lẽ hoặc không bao giờ được chạy. "

> Cemri 等人(MAST) theo dõi 1642 个多代理 执行失败──21.3% là chứng minh thiếu hụt hệ thống đã phát hành không có người kiểm tra các câu trả lời──其余79% thường có thể được bắt nguồn từ "một kiểm tra lặng thất bại hoặc chưa bao giờ hoạt động"──验证是承重角色──

Số 21,3% là số liệu thống kê duy nhất được trích dẫn nhiều nhất trong kỹ thuật đa đại lý năm 2026. Nó nói: nếu bạn chỉ thêm một vai trò vào hệ thống của mình, hãy làm cho nó là một xác minh. Không phải một nhà phê bình, không phải một nhà hoạch định  một xác minh xác định với kiểm tra cấp mã.

> 21,3% số này là số liệu thống kê được trích dẫn nhiều nhất trong hơn 2026 Agent Engineering. Nó nói: Nếu bạn chỉ thêm một vai trò trong hệ thống, hãy làm cho nó trở thành người xác nhận. Không phải là nhà phê bình, không phải là người lập kế hoạch.

PwC báo cáo (CrewAI triển khai, 2025) rằng việc thêm một vòng xác thực cấu trúc đã di chuyển độ chính xác từ 10% lên 70%.

> PwC  báo cáo CrewAI 部署,2025) thêm chu kỳ kiểm tra cấu trúc sẽ tăng tỷ lệ xác thực từ 10% lên 70%― một vai trò mang lại 7 lần tăng lên―

### Đánh giá đối với xác minh

- Một nhà phê bình là một thạc sĩ pháp lý xem xét một đồ tạo vật cho chất lượng.
  Trung văn翻译: nhà phê bình là một chuyên gia về chất lượng của công trình kiểm tra.
- Một xác minh là một chương trình xác định chạy trên vật thể. mục tiêu. Cho phép vượt qua / thất bại với bằng chứng.
  Trung文翻译:验证者 là một quy trình xác định được thực hiện trên công trình.

Sử dụng cả hai. Nhận xét nhận được các vấn đề về hương vị mà người xác minh không thể diễn tả.

> 两者都用──批评者捕获验证者无法表达质量问题──验证者捕获批评者看不到的 bug,因为它们只出现在运行时──

Một thứ tự phổ biến: đầu tiên xác minh (quá, giết chết rõ ràng làm việc bị hỏng), sau đó phê bình (rút, tinh chỉnh chất lượng). Một số nhóm đảo ngược thứ tự để bắt được các vấn đề về hương vị trước khi chi tiêu tính toán về mã bị hỏng.

> 常见顺序:先验证者(快,杀死明显破损的工作),然后批评者(慢,精炼质量) ・・・ Một số nhóm翻转顺序以在花计算资源修复破损代码之前捕获质量问题──测试哪种适合你的任务──

### Phản ứng phản mẫu

Mỗi vai trò trong hệ thống của bạn là một LLM và mỗi vai trò xuất hiện là "có vẻ tốt với tôi".

> Mỗi vai trò trong hệ thống của bạn là LLM, mỗi vai trò xuất phát là "nên nhìn không sai"―― mô hình thất bại MAST cổ điển―― ít nhất thêm một bởi mã thay vì LLM quyết định thông qua/ thất bại của chứng minh viên――

### Bản đồ khung

- **CrewAI** `Agent(role, goal, backstory)`là bề mặt chuyên môn sách giáo khoa.
  Trung ngữ翻译:**CrewAI** `Agent(role, goal, backstory)`là bề mặt chuyên môn hóa của giáo科书式
- **LangGraph** các nút có thể có các lời nhắc chuyên dụng; cạnh bắt buộc đường ống.
  Trung ngữ翻译:**LangGraph** 节点 có thể có gợi ý đặc biệt;边强制流水线──
- **AutoGen** Các nhân viên được trò chuyện cụ thể với một từ trong một GroupChat.
  Trung ngữ翻译:**AutoGen** Trong GroupChat có một từ tên trong một vai trò cụ thể.
- **OpenAI Agents SDK** Các công cụ giao tiếp giữa các đại lý chuyên về vai trò.
  Trung ngữ翻译:**OpenAI Agents SDK** 角色专业化 Agent 之间的交接工具──

## Hãy xây dựng nó.
```figure
swarm-roles
```

## Hãy xây dựng nó

`code/main.py`thực hiện một đường ống 4 vai tạo ra một hàm Python đơn giản:

> `code/main.py`实现 một cấu trúc đơn giản Python 函数 4 角色流水线:

- **Planner**tạo ra một spec.
  Trung ngữ翻译:**规划者**产生规范──
- **Executor**tạo ra một chuỗi mã.
  Trung ngữ翻译:**执行者**生成代码字符串──
- **Critic**(LLM-simulated) cờ các vấn đề rõ ràng.
  Trung ngữ翻译:**批评者**(LLM 模拟) 标记 rõ ràng vấn đề:
- **Verifier**chạy mã được tạo trong một hộp cát (`exec`) chống lại một trường hợp thử nghiệm.
  Trung ngữ翻译:**验证者**Trong hộp`exec`(c) trong các bài viết về các bài viết về các bài viết về các bài viết về các bài viết về các bài viết về các bài viết về các bài viết về các bài viết về các bài viết về các bài viết về các bài viết về các bài viết về các bài viết về các bài viết về các bài viết về các bài viết về các bài viết về các bài viết về các bài viết về các bài viết về các bài viết về các bài viết về các bài viết về các bài viết về các bài viết về các bài viết về các bài viết về các bài viết về các bài viết về các bài viết về các bài viết về các bài viết về các bài viết về các bài viết về các bài viết về các bài viết về các bài viết về các bài viết về các bài viết về các bài viết về các bài viết về các bài viết về các bài viết về các bài viết về các bài viết về các bài viết về các bài viết về các bài viết về các bài viết về các bài viết về các bài viết về các bài viết về các bài viết về các bài viết về các bài viết về các bài viết về các bài viết về các bài viết về các bài viết về các bài viết về các bài viết về các bài viết về các bài viết về các bài viết về các bài viết về các bài viết về các bài viết về các bài viết về các bài viết về các bài viết về các bài viết về các bài viết về các bài viết về các bài viết về các bài viết về các bài viết về các bài viết về

Demo chạy hai lần: một lần khi người thực thi tạo ra mã chính xác (các trình kiểm tra + phê duyệt cả hai đều vượt qua), một lần khi người thực thi tạo ra mã ngoài thông số (các trình kiểm tra bỏ lỡ lỗi vì nó trông có thể tin cậy, kiểm tra nhận nó vì thử nghiệm thất bại).

> 演示运行两次:一次执行者产生正确的代码(批评者 + 验证者都通过),一次执行者产生偏离规范的代码(批评者因为看起来合理而错过错误,验证者因为测试失败而捕获它)

## Hãy sử dụng nó để thực hiện

`outputs/skill-role-designer.md`thực hiện một nhiệm vụ và tạo ra danh sách vai trò (3-5 vai), sơ đồ đầu vào / ra ngoài cho mỗi vai trò và kiểm tra xác minh.

> `outputs/skill-role-designer.md`接收任务并产生角色名册(3-5 个角色) 、 mỗi角色的输入/输出模式和验证人检查──在将代理 连接到框架之前使用──

## Chuyển nó đi.

Danh sách kiểm tra:

> 检查清单:

- **At least one deterministic verifier.**Không bao giờ là toàn bộ.
  Trung ngữ翻译:**至少一个确定性验证者。**永远不要全 LLM.
- **Explicit I/O schema per role.**Người lập kế hoạch trả lại một spec, không phải prose; người thực thi đọc sơ đồ đó.
  Trung ngữ翻译:**每个角色有明确的 I/O 模式。**规划者返回规范, không phải散文;执行者读取该模式──
- **Communicative dehallucination.**Người thực thi phải hỏi người lập kế hoạch khi nào thông tin bị thiếu; không bao giờ phát minh ra nó.
  Trung ngữ翻译:**交流去幻觉。**执行者在信息缺失时必须问规划者;永远不要发明──
- **Critic/verifier ordering.**Đánh giá đầu tiên (cô rẻ, bắt được các vấn đề thiết kế), xác minh thứ hai (rút, bắt được lỗi).
  Trung ngữ翻译:**批评者/验证者顺序。**先运行批评者 (便宜,捕获设计问题),再运行验证者 (慢,捕获 bug)
- **Loop budget.**Max 2 round review trước khi leo thang lên con người.
  Trung ngữ翻译:**循环预算。**Trong nâng cấp lên con người trước 2 người phê bình-phục xuất sửa đổi vòng.

## Tập luyện bài tập

1. Đi chạy`code/main.py`và quan sát cách xác minh nhận lỗi mà nhà phê bình bỏ qua.`return`(v) như một chất kiểm chứng bổ sung.
   Trung ngữ翻译:运行 `code/main.py`并观察验证人如何捕获批评者错过的 bug──添加一个静态分析检查(计算 `return`(đáng ra số lần) như là một người kiểm tra bổ sung. Nó đã bắt được điều gì trong quá trình chạy thử nghiệm?
2. Thêm một vai trò thứ 5: "nhà phân tích yêu cầu" chuyển đổi mong muốn của người dùng thành thông số sẵn sàng cho lập kế hoạch.
   Trung ngữ翻译:添加第五个角色:"需求分析师",将用户愿望翻译为规划者可用规范──什么样的交流去幻觉请求应该流上方?
3. Đọc phần 3 của MetaGPT ("Các đại lý"). Đăng ra các sơ đồ đầu vào/ ra khỏi mỗi 5 vai trò của MetaGPT.
   中文翻译:阅读 MetaGPT 第 3 节("Hội")。列出 MetaGPT 5 个角色中每个的输入/输出模式──
4. Đọc biểu đồ chuỗi trò chuyện của ChatDev (arXiv:2307.07924 Hình 3). Xác định nơi mà sự khống chế ảo giác truyền thông phá vỡ một vòng lặp mà nếu không là vô hạn.
   Trung ngữ翻译:阅读 ChatDev's聊天链图(arXiv:2307.07924 图 3)  nhận thức giao tiếp đi ảo giác ở đâu đã phá vỡ nếu không sẽ là vòng lặp vô hạn。
5. Sự tăng cường độ chính xác 7x của PwC đến từ vòng lặp xác minh. giả định ba nhiệm vụ mà việc thêm một người xác minh sẽ không giúp  nơi kiểm tra xác định tính chính xác là không thể hoặc quá tốn kém.
   Trung ngữ翻译:PwC's 7 倍准确率提升来自验证循环──假设三个添加验证人不会有帮助任务确定性正确性检查不可能或代价过高的任务──

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Role specialization / 角色专业化 | "Different agents, different jobs" / "不同 Agent，不同工作" | Distinct system prompts tuned for planner/executor/critic/verifier roles. / 为规划者/执行者/批评者/验证者角色调优的独特系统提示。 |
| SOP pattern / SOP 模式 | "Encoded standard operating procedure" / "编码标准操作流程" | MetaGPT's framing: strict I/O schemas per role turn a team into a pipeline. / MetaGPT 的框架：每个角色的严格 I/O 模式将团队变成流水线。 |
| Communicative dehallucination / 交流去幻觉 | "Ask before inventing" / "先问再发明" | ChatDev pattern: executor asks planner when a detail is missing rather than making one up. / ChatDev 模式：执行者在细节缺失时询问规划者而不是编造。 |
| Critic / 批评者 | "LLM reviewer" / "LLM 审阅者" | Subjective, opinionated reviewer. Catches taste issues. Can be fooled by plausible prose. / 主观的、有观点的审阅者。捕获质量问题。可以被似是而非的散文愚弄。 |
| Verifier / 验证者 | "Deterministic check" / "确定性检查" | Code-based pass/fail. Test runner, type checker, schema validator. Cannot be fooled. / 基于代码的通过/失败。测试运行器、类型检查器、模式验证器。不能被愚弄。 |
| Verification gap / 验证缺口 | "No one checked" / "没人检查" | 21.3% of MAST failures. Answer shipped without a check that would have caught the bug. / 21.3% 的 MAST 失败。发布答案时没有会捕获 bug 的检查。 |
| Revision loop / 修订循环 | "Critic sends it back" / "批评者打回" | Critic rejection triggers executor re-run with feedback. Needs a budget. / 批评者拒绝触发带反馈的执行者重新运行。需要预算。 |
| All-LLM anti-pattern / 全 LLM 反模式 | "Looks good to me" / "看起来不错" | Every role is an LLM, no deterministic check. Classic MAST failure. / 每个角色都是 LLM，没有确定性检查。经典的 MAST 失败。 |

## Xem thêm 延伸阅读

- [Hong et al. — MetaGPT: Meta Programming for Multi-Agent Collaboration](https://arxiv.org/abs/2308.00352) giấy tham chiếu SOP-as-role-prompt
  中文翻译:Hong 等人  MetaGPT:多 Agent 协作的元编程  SOP 作为角色提示的参考论文
- [Qian et al. — Communicative Agents for Software Development (ChatDev)](https://arxiv.org/abs/2307.07924) chuỗi trò chuyện + sự giải ảo thông tin
  Trung文翻译:Qian 等人  软件开发的通信代理(ChatDev) 聊天链 + 交流去幻觉
- [Cemri et al. — Why Do Multi-Agent LLM Systems Fail?](https://arxiv.org/abs/2503.13657) Định dạng phân loại MAST; khoảng cách xác minh là 21,3% các thất bại
  Trung ngữ翻译:Cemri 等人  Tại sao nhiều đại lý LLM 系统会失败? MAST 分类法;验证缺口占失败的21.3%
- [CrewAI docs — Agent roles](https://docs.crewai.com/en/introduction) bề mặt đặc điểm vai trò sản xuất
  Trung文翻译:CrewAI 文档  Agent 角色  生产角色规范表面
