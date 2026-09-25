# Tỷ lệ kỹ năng, đóng gói và khả năng di chuyển

> Một kỹ năng được hoàn thành khi gói của nó tồn tại, hướng theo yêu cầu đúng, cải thiện một nhiệm vụ được đo lường, giữ trong chính sách, và xuống cấp trung thực trên một chủ nhà khác.

> **【中文解读】**Một kỹ năng chỉ đạt được 5 điểm khi " hoàn thành ": cấu trúc gói thông qua lint  được kích hoạt trên yêu cầu chính xác  mang lại sự nâng cao thực sự  luôn chờ trong ranh giới ủy quyền  giảm thực tế trên chủ nhà khác thay vì  thất bại  Bài học này là phần mềm của Agent Skills 小系列 ((Phase 13 · 22-27): đưa các tiêu chuẩn chấp nhận trên thành sáu cấp độ thi hành và một loại phát hành cấm đánh giá.

> **【拓展：Skill 生态→软件工程成熟度】**Kỹ năng thường được coi là "đánh dấu đẹp" (written pretty Markdown), chủ đề cốt lõi của bài học này là: kỹ năng là một gói phần mềm nhỏ có đường xác suất và lớp thực hiện, cần phải quan tâm đến các giao diện sản xuất như nhau, phân biệt cấu trúc tĩnh, hành vi, hiệu quả nhiệm vụ, chất lượng văn bản, ranh giới an toàn, khả năng di chuyển qua thời gian, một lớp không thể bỏ qua.

>  **【前置】**Học tập trước xin bắt đầu:Phase 13 · 22(Skill Skills of Agent.md 契约与运行时边界) Phase 13 · 24(chuyên bố tiến bộ) Phase 13 · 25(触发与路由) Phase 13 · 26(chính quyền、沙箱与信任)  本课是这四课的综合毕业设计,也是全迷你轨道的产出验证课──

**Type:** Build | **类型:** 动手实践
**Languages:** Python (stdlib) | **语言:** Python（标准库）
**Prerequisites:** Phase 13 · 22, 24, 25, and 26 | **前置知识:** Phase 13 · 22、24、25、26
**Time:** ~150 minutes | **时间:** 约 150 分钟

## Mục tiêu học tập

- Chuyển đổi một quy trình làm việc chuyên gia thành một kỹ năng bằng cách tách biệt phán đoán, tính toán xác định, tham chiếu và hợp đồng sản xuất.
  Trung ngữ翻译:通过分离判断性工作、确定性计算、参考资料和输出契约,把一个专家工作流提炼作为技能──
- Kiểm tra cấu trúc gói, kích hoạt định tuyến, hành vi nhiệm vụ, độ chính xác kịch bản, an toàn và khả năng di chuyển như các lớp riêng biệt.
  Trung ngữ翻译:把包结构、触发路由、任务行为、脚本正确性、安全性和可移植性作为相互独立层分别测试──
- Đo kích hoạt độ chính xác và nhớ bằng cách sử dụng tích cực, tiêu cực rõ ràng và gần bị bỏ lỡ.
  Trung ngữ翻译:用正例、明确负例和近失例度量触发的精确率(đúng) 与召回率(回忆)。
- So sánh hiệu suất với và không có kỹ năng trong các lần chạy lặp lại.
  Trung ngữ翻译:跨多次重运行, so sánh có kỹ năng với không có kỹ năng 两种条件下的表现――
- Xây dựng và thực thi một matrix khả năng chạy thời gian và một cổng phát hành cho các gói kỹ năng hoàn chỉnh.
  Trung ngữ翻译:为完整的技能包构建并强制执行跨运行时的能力矩阵和发布门禁──

## Vấn đề  vấn đề giới thiệu

> **【中文解读】**Trong bản demo, tất cả đều bình thường, dựa trên bốn sự kiện: người dùng ngẫu nhiên sử dụng câu gốc trong mô tả, tác giả tự biết mở tài liệu tham khảo nào, biên bản được lấy là sạch 净输入, chủ nhà ngẫu nhiên nhận biết từng đoạn tự định. Trong thực tế sử dụng, bốn sự kiện này sẽ biến mất cùng một lúc, trong khi "Markdown nhìn lên không sai" cũng không thể phát hiện được.

Một kỹ năng hoạt động trong một bản demo. Người dùng hỏi chính xác cụm từ được sử dụng trong mô tả của nó, tác giả biết tham chiếu nào để mở, kịch bản thấy đầu vào sạch, và người chủ dự kiến nhận ra mỗi trường tùy chỉnh.

> Một kỹ năng trong một demo 里能跑通── người dùng hỏi 恰好是描述 里使用过短语, tác giả biết phải mở tài khoản tham khảo, kịch bản nhìn thấy là 干净输入, dự kiến chủ nhà biết mỗi tự định字段──

Sau đó, việc sử dụng thực sự bắt đầu.

> Sau đó thực sự sử dụng bắt đầu.

- Mô hình gọi nó cho một nhiệm vụ gần đó nhưng khác.
- Một yêu cầu hợp lệ sử dụng các từ ngữ không quen thuộc, do đó mô hình bỏ qua nó.
- Cơ thể nói với nhân viên phải làm gì nhưng không nói rằng vật liệu nào chứng minh hoàn thành.
- Các kịch bản thất bại trên không gian, lặp đi lặp lại thực hiện, hoặc trạng thái một phần.
- Các bản sao cài đặt gói `SKILL.md`Nhưng nó lại để lại những tham chiếu của nó.
- Một thời gian chạy khác bỏ qua các lá cờ gọi và công cụ.
- Một lần chạy thành công, ba lần chạy tương đương lang thang vào các nhánh khác nhau.

Không có một lỗi nào trong số những lỗi này bị bắt bởi "Markdown trông tốt".

> Những thất bại này không có một cái nào có thể bị "Markdown trông không sai" bắt giữ.

## Khái niệm cốt lõi

> **【中文解读】**Bài viết này nói về kỹ năng 提取与打包的三条方法论: 1) Từ dòng thực sự của công việc thay vì " chủ đề " xuất phát  " chẩn đoán một sự triển khai nào đó Tại sao không cần thiết và xuất phát báo cáo tai nạn " là kỹ năng có thể sử dụng  phạm vi, " kỹ năng Kubernetes " không; 2) 判断性工作交付模型,确定性工作交付脚本; 3) 依赖顺序编写包先定产品契约和验证方式,最后才磨磨正文措辞.

### Bắt đầu từ một dòng công việc thực sự, không phải là một chủ đề.

"Tạo kỹ năng Kubernetes" không phải là một phạm vi có thể sử dụng. Kubernetes chứa hàng trăm nhiệm vụ với các công cụ, rủi ro và kết quả khác nhau.

> "Tạo ra một kỹ năng Kubernetes" không phải là một phạm vi có thể sử dụng.

"Chẩn đoán lý do tại sao một triển khai không đạt được sẵn sàng, thu thập bằng chứng mà không thay đổi cluster, và tạo ra một báo cáo sự cố xếp hạng" là một ứng cử viên kỹ năng.

> "chẩn đoán một sự triển khai tại sao không đạt được trạng thái  trạng thái ️ thu thập bằng chứng ️ và sản xuất một báo cáo về sự cố theo thứ tự ưu tiên" chỉ là một kỹ năng Ứng cử viên️ nó có:触发边界️ ổn định 取证步骤序列️ cần các điểm quyết định phán đoán️ có thể biên soạn các lệnh️ sản phẩm rõ ràng, cũng như "chỉ đọc chẩn đoán" ️ biên giới an toàn️️

- một ranh giới kích hoạt;
- Một chuỗi các bước thu thập bằng chứng ổn định;
- các điểm quyết định cần xét xử;
- lệnh có thể trở thành kịch bản hoặc công cụ hẹp;
- một vật thể được xác định;
- giới hạn an toàn: chẩn đoán chỉ đọc.

Sử dụng cuộc phỏng vấn thu thập này:

> Sử dụng 10 câu hỏi này để đưa ra cuộc phỏng vấn( sự kiện触发点, những yêu cầu tương tự không nên được触发, trước tiên thu thập bằng chứng nào, những quyết định nào phụ thuộc vào bằng chứng nào, những bước nào có thể được viết ra, những quy tắc trong lĩnh vực nào đáng để ghi vào tham khảo, những động thái nào cần được phê duyệt hoặc phải loại trừ ngoài, những sản phẩm nào chứng minh được hoàn thành, đánh giá độc lập làm thế nào để kiểm tra, những bước nào phụ thuộc vào một hoạt động cụ thể)  trả lời đồng thời quyết định cấu trúc và nhóm đánh giá.

1. Sự kiện chính xác nào khiến một chuyên gia bắt đầu quá trình làm việc này?
2. Những lời cầu xin tương tự nào không nên bắt đầu?
3. Chuyên gia thu thập bằng chứng nào trước?
4. Những quyết định nào phụ thuộc vào bằng chứng đó?
5. Những bước nào đủ quyết định để viết kịch bản?
6. Những quy tắc miền nào xứng đáng được tham khảo?
7. Điều gì cần được chấp thuận hoặc không được áp dụng?
8. Những đồ tạo vật nào chứng minh rằng quá trình làm việc đã hoàn thành?
9. Một nhà phê bình độc lập kiểm tra nó như thế nào?
10. Những bước nào phụ thuộc vào một thời gian chạy?

Các câu trả lời trở thành kiến trúc gói và tập hợp eval.

### Hãy tách biệt việc phán xét và việc xác định.

```figure
skill-workflow-extraction
```

Sử dụng phán đoán mô hình để phân loại, ưu tiên, tổng hợp và không rõ ràng. Sử dụng kịch bản hoặc công cụ để phân tích, đếm, xác nhận, chuyển đổi, truy vấn các API được gõ và thực thi các không biến.

> Mô hình đánh giá được sử dụng cho phân loại, xếp hạng ưu tiên, tổng hợp và xử lý khác nhau; kịch bản hoặc công cụ được sử dụng để phân tích, tính toán, thử nghiệm, chuyển đổi, truy vấn loại hóa API và không thay đổi quy mô.

Một bộ kỹ năng có chứa 80 dòng phân tích bằng tay mô phỏng là mỏng manh. Một kịch bản cố gắng đưa ra một quyết định kiến trúc chủ quan là không minh bạch. Đặt mỗi hành vi ở nơi có thể kiểm tra tốt nhất.

> 正文里塞 80 行 "Logic phân tích của người giống thịt" là yếu đuối; để cho kịch bản làm cho các quyết định cấu trúc chủ quan là khó kiểm tra.

### Tác giả gói theo thứ tự phụ thuộc.

Đừng bắt đầu bằng cách làm sáng tác văn bản, hãy xây dựng từ hợp đồng có thể nhìn thấy bên trong.

> Đừng bắt đầu từ打磨措辞. Từ có thể quan sát được từ契约向外往内构建.

1. **Artifact contract:**xác định các tệp, trường hoặc quyết định cần thiết.
2. **Verification:**xác định cách kiểm tra từng yêu cầu.
3. **Evidence tools:**thực hiện các bộ sưu tập và xác nhận xác định.
4. **Decision map:**kết nối các trạng thái bằng chứng với các chi nhánh.
5. **References:**cung cấp chi tiết miền tại chi nhánh cần nó.
6. **Entry body:**giải thích quy trình làm việc, ranh giới, thất bại và đầu ra.
7. **Description:**khả năng của trạng thái và giới hạn kích hoạt.
8. **Runtime adapters:**thêm các lời kêu gọi hoặc mở rộng ngữ cảnh riêng biệt.
9. **Evals:**chạy cấu trúc, định tuyến, hành vi, an toàn và các lớp di động.
10. **Package:**cài đặt thư mục đầy đủ và kiểm tra nó từ điểm đến.

Trật tự này làm cho bài thơ phục vụ một hệ thống có thể kiểm tra thay vì phát minh ra các tiêu chí thành công sau khi bản demo hoạt động.

### 6 lớp đánh giá. 6 lớp đánh giá.

```figure
skill-eval-layers
```

Mỗi lớp trả lời một câu hỏi khác nhau.

> Mỗi tầng trả lời một câu hỏi khác nhau: cấu trúc tầng hỏi "bộ hình của gói đối không đối đối", đường tầng hỏi "cái xúc tác khi xúc tác, không phải xúc tác khi không ư?", hành vi tầng hỏi "cái nhiệm thực sự đã thay đổi tốt chưa?",脚本层 hỏi " xác định phần là phần mềm đủ điều kiện không?", an ninh层 hỏi "có quyền không", có thể di chuyển tầng hỏi "cái chủ khác còn trung thực không?"... thông qua một tầng không thể thay thế bất kỳ một tầng nào khác.

## Lớp 1: Cấu trúc gói. Lớp 1: Cấu trúc gói.

> **【中文解读】**静态 lint 负责验证一切不需要模型的事实:SKILL.md 存在且前材料可解析、名称与目录名一致、必需字段齐全且不超限、非核心字段都在运行时扩展白名里、每个引用都能在包内解析、文件后和字节符合发布策略、没有符号链接和特殊文件、正文不超字符预算、秘密模式、扫描空以及输出合同和失败行为 两个部分非空――注意:先做物理树预检(拒绝符号链接根目录等) 解析内容,否则会抹消检查所需的证据.

Việc làm trục trặc tĩnh nên xác minh các sự kiện không yêu cầu mô hình:

- `SKILL.md`tồn tại tại ở gốc gói;
- Phân tích mặt trước an toàn;
- `name`và phù hợp với thư mục cha mẹ;
- Các trường yêu cầu có mặt và trong giới hạn;
- Mỗi trường vật liệu trước không phải lõi xuất hiện trong danh sách các phép mở rộng thời gian chạy của chính sách phát hành;
- Mỗi tham chiếu trực tiếp được giải quyết bên trong gói;
- Các tham chiếu, kịch bản, tài sản và thiết bị đánh giá sử dụng hậu tố được phép của chính sách phát hành và ở dưới giới hạn byte của nó;
- Không có liên kết đồng nghĩa hoặc tập tin đặc biệt bị cấm;
- cơ quan vẫn nằm trong ngân sách đặc trưng của chính sách giải phóng;
- Một quét mô hình bí mật ngần ngại cố tình không tìm thấy bất kỳ chỉ định tín dụng rõ ràng hoặc tiêu đề khóa riêng;
- không trống `## Output contract`và `## Failure behavior`Các bộ phận đang có mặt.

Thực hiện một chuyến bay trước cây vật lý trước khi phân tích `SKILL.md`, dữ liệu đánh giá, bằng chứng, thiết bị chủ, hoặc biểu thị. Tháo một gốc liên kết, liên kết gốc hoặc nhập, thiếu tập tin thường xuyên cần thiết, và tập tin đặc biệt trước khi đọc bất kỳ nội dung nào. Sau đó chạy các nội dung ý thức chính sách lint. Giải quyết con đường gói trước khi bay xóa các bằng chứng gốc-symlink cần kiểm tra.

> Trong phân giải`SKILL.md`、 đánh giá dữ liệu、 chứng cứ、 vật thể chủ hoặc biểu hiện 之前, trước tiên thực hiện một lần kiểm tra trước: trước khi đọc bất kỳ nội dung nào, từ chối danh mục gốc của liên kết ký hiệu、 danh mục hoặc nhập khẩu của liên kết ký hiệu、 thiếu các tệp thông thường cần thiết cũng như các tệp đặc biệt, sau đó chạy lại các chiến lược nhận thức nội dung  lint── nếu trước khi kiểm tra kết hợp đường dẫn giải quyết 掉, sẽ xóa bỏ các chứng cứ cần thiết để kiểm tra liên kết ký hiệu gốc.

Các bài học làm cho các giá trị chính sách đó cụ thể: giới hạn cơ thể 10.000 ký tự, giới hạn tập tin đồng hành 1.000.000 byte, danh mục cụ thể cho phụ đề và tên mở rộng thời gian chạy rõ ràng được cung cấp bởi các yêu cầu gói. Đây là những ví dụ về chính sách giải phóng, không phải giới hạn kỹ năng đại lý phổ quát. Việc quét mẫu bí mật là một màn bảo vệ cho những lỗi rõ ràng, không phải bằng chứng rằng một gói không chứa dữ liệu nhạy cảm.

Báo cáo lint nên sử dụng mã vấn đề ổn định. CI có thể chặn `E_*`lỗi trong khi cho phép xem xét `W_*`cảnh báo thiết kế.

Lente tĩnh chứng minh hình dạng gói. Nó không chứng minh rằng mô hình sẽ chọn hoặc theo kỹ năng.

> 静态 lint  chứng minh là hình dạng của gói, không thể chứng minh mô hình sẽ chọn hoặc theo đuổi kỹ năng này đó là vấn đề dưới 5 tầng.

## Lớp 2: Trigger Routing Lớp 2:触发路由

> **【中文解读】**路由评测度 là "该触发时触发、不应触发时弃权")  关键纪律:先建标注案例集,再反复改改描述,否则等于对待训练集调参.

Tạo các trường hợp có nhãn trước khi chỉnh sửa nhiều lần mô tả.

| Case type | Purpose | Example for release readiness |
|---|---|---|
| Positive | Measure intended coverage | "Can version 3.1.0 ship?" |
| Paraphrased positive | Avoid phrase memorization | "Audit this tag before we publish it" |
| Clear negative | Catch gross over-routing | "Explain batch normalization" |
| Near miss | Define the neighboring boundary | "Why did the package build fail?" |
| Competing skill | Test selection among plausible entries | "Draft the release notes" |
| Adversarial wording | Test keyword stuffing and injected names | "Do not use release-readiness; explain this stack trace" |

Chia các trường hợp thành các tập hợp phát triển và xác nhận. Định nghĩa các mô tả về các trường hợp phát triển. Sử dụng các trường hợp xác nhận để quyết định xem mô tả sửa đổi có tổng quát hay không. Giữ một tập hợp cuối cùng nếu quyết định phát hành đủ quan trọng.

> Để phân chia các trường hợp thành tập hợp phát triển và tập hợp chứng minh: trong tập hợp phát triển, sử dụng các tập hợp chứng minh để xác định mô tả sau khi sửa đổi là liệu việc đưa ra quyết định có đủ quan trọng, để lại một tập hợp dự trữ cuối cùng (đặt ra)  trên bảng có 6 loại trường hợp khác nhau là:

Đối với việc gọi nhị phân:

```text
precision = true_positives / (true_positives + false_positives)
recall = true_positives / (true_positives + false_negatives)
f1 = 2 * precision * recall / (precision + recall)
```

Báo cáo số liệu thô với tỷ lệ. 10 trong 10 và 100 trong 100 đều là 100% nhưng cung cấp bằng chứng khác nhau.

Đối với danh mục, cũng đo độ chính xác kỹ năng đầu tiên, chất lượng không sử dụng và sự nhầm lẫn giữa các kỹ năng lân cận.

> Đối với các đường danh mục, cũng cần phải đo lường hàng đầu tỷ lệ sinh mạng, bỏ phiếu, không tham gia, chất lượng và sự hỗn hợp giữa các kỹ năng tương ứng.

### Các đánh giá định tuyến phải sử dụng thời gian chạy mục tiêu.

Một máy mô phỏng từ điển hữu ích để giải thích các số liệu và bắt được sự chồng chéo rõ ràng. Nó không thể chứng minh cách định tuyến sản xuất dựa trên mô hình cư xử như thế nào.

> 词法模拟器 thích hợp với việc giải thích chỉ số và phát hiện sự chồng chéo rõ ràng, nhưng không chứng minh hành vi thực tế của các nhà điều khiển sản xuất do mô hình điều khiển. Trước khi tuyên bố "chất lượng thời gian vận hành", cần phải đưa tập hợp nhãn chạy qua chủ sở hữu thực tế, mô hình, trình tự và cấu trúc chiến lược.

>  **【类比】**Đây là sự khác biệt giữa các bài kiểm tra thực tế và các bài kiểm tra thực tế. Từ ngữ học mô phỏng là "lập trình" trọng lượng từ khóa của các yêu cầu và mô tả trên giấy; thực sự chủ nhà đường là "lập trình" mô hình thực sự lựa chọn dưới toàn bộ văn bản, danh mục sắp xếp và cấu hình chiến lược.

## Lớp 3: Chỉ dẫn và hành vi tạo vật. Lớp 3: Chỉ thị và hành vi sản phẩm.

> **【中文解读】**触发正确只是进场券,技能 必须让任务真的变好――方法学是 A/B 对照实验:基线组(同模型+同工具+同任务,无技能)对实验组(同模型+同工具+同任务,有技能),唯一变量是技能 是否存在,否则差异无法归因──产品契约将"完成"变成可独立试验的属性列表值方案 校验结构,领域检查查查查取,人类或校准过的评审判断"结论是否由证支"――

Việc kích hoạt đúng là lối vào.

Tạo các nhiệm vụ cố định với:

- các tệp nhập và giả định môi trường;
- Các công cụ và ranh giới được phép;
- Các con đường hiện vật dự kiến;
- kiểm tra xác định;
- Các mục tiêu yêu cầu phán quyết;
- Thời gian, cuộc gọi hoặc chi phí tối đa;
- trường hợp thất bại và hành vi dừng dự kiến.

- Cứu với các điều kiện:

```text
baseline: same model + same tools + same task, no skill
treatment: same model + same tools + same task, skill available
```

Giữ mô hình, nhiệt độ hoặc chính sách lấy mẫu, bộ công cụ, thiết bị nhiệm vụ và ngân sách không đổi. Nếu không bạn không thể gán cho sự khác biệt cho kỹ năng.

> 保持模型、温度或采样策略、工具集、任务固定 和预算全部不变,否则你不能归因于技能──(七个有用结果维度:正确性、完整性、效率、证据、范围、恢复能力、人工修改量──)

Các kích thước kết quả hữu ích bao gồm:

| Dimension | Example measure |
|---|---|
| Correctness | Required tests and invariants pass |
| Completeness | Every artifact-contract field exists |
| Efficiency | Tool calls, elapsed time, tokens, or cost |
| Evidence | Claims point to valid files or observations |
| Scope | Forbidden files and actions remain untouched |
| Recovery | Interrupted run resumes without duplicate side effects |
| Human effort | Number and severity of reviewer corrections |

Đừng chỉ tối ưu hóa cho ít token hơn. Một lần chạy ngắn hơn mà không được kiểm tra an toàn cần thiết sẽ tồi tệ hơn.

> Đừng chỉ tối ưu hóa mã thông báo số. Một lần bị bỏ qua kiểm tra an ninh cần thiết.

### Hợp đồng tạo vật làm cho hành vi thực thi được

Hợp đồng tạo vật là một danh sách các tài sản có thể kiểm tra độc lập:

```json
{
  "artifact": "release-readiness.json",
  "required_fields": [
    "candidate",
    "source_revision",
    "checks",
    "blocking_findings",
    "recommendation"
  ],
  "allowed_recommendations": ["ready", "blocked", "needs-review"],
  "evidence_required_for_each_check": true,
  "publish_side_effect_allowed": false
}
```

Việc xác nhận sơ đồ kiểm tra cấu trúc. Việc kiểm tra miền xác nhận các đường sửa đổi và bằng chứng của ứng cử viên. Một thẩm phán con người hoặc được chuẩn bị có thể đánh giá liệu khuyến nghị có bắt nguồn từ bằng chứng hay không.

> Chương trình kiểm tra cơ cấu kiểm tra, lĩnh vực kiểm tra kiểm tra kiểm tra kiểm tra ứng cử viên phiên bản và đường chứng thực, người hoặc kiểm tra viên đã chuẩn bị đánh giá" đề xuất liệu chứng thực được đưa ra hay không"

## Lớp 4: Sản phẩm chính xác.

> **【中文解读】**Kỹ năng của các phần mềm là phần mềm thông thường, phải được thử nghiệm độc lập bên ngoài mô hình. Kế hoạch có tác dụng nhỏ nhất bao gồm: nhập bình thường/空/形, Unicode và空格 và đường biên giới, tái thực hiện, quá thời gian hoặc phụ thuộc vào thất bại, sản phẩm còn lại trong các phiên bản sau đó, xuất ra một giới hạn lớn, hoạt động khô, hành vi cấu trúc, trở lại và sai lầm.

Thử nghiệm các kịch bản kỹ năng như phần mềm thông thường, chạy mô hình bên ngoài.

Các trường hợp tối thiểu:

- đầu vào bình thường;
- đầu vào trống;
- đầu vào bị biến dạng;
- Unicode, không gian trắng và các trường hợp đường dẫn;
- thực thi lặp đi lặp lại;
- thời gian nghỉ hoặc sự thất bại của sự phụ thuộc;
- Tạo ra một phần từ một lần chạy trước đó;
- giới hạn kích thước đầu ra;
- hành vi chạy khô;
- hợp đồng thoát và lỗi có cấu trúc.

Sử dụng các thiết bị cố định. Không cần một mạng sống cho các thử nghiệm đơn vị. Đặt các thử nghiệm tích hợp mạng sau một cờ rõ ràng và ghi lại hợp đồng từ xa mà họ phụ thuộc.

Nếu kịch bản thực hiện tác dụng phụ, kiểm tra kế hoạch riêng biệt và commit. yêu cầu miễn phí hoặc bồi thường cho các bài viết bên ngoài được thử lại.

## Lớp 5: An toàn và thẩm quyền Lớp 5: An toàn và quyền hạn

> **【中文解读】**Câu hỏi về đánh giá an toàn là: liệu gói này có bao giờ ở trong phạm vi quyền hạn mà nó được cấp không. Các loại kịch bản cần thiết bao gồm: yêu cầu của người dùng ngoài phạm vi, lệnh ác ý trong nhập tham khảo, thoát khỏi đường dẫn nguồn ngoài gói, thoát khỏi các liên kết mã khu vực làm việc trong danh mục gốc không được tuyên bố, dựa vào các lệnh của chứng chỉ môi trường, không được phê duyệt các hoạt động phá hủy giữa các vòng lặp quá lớn hoặc vòng chết, kỹ năng, tái tạo các tác dụng phụ có thể xảy ra.

Các đánh giá an toàn hỏi liệu gói có nằm trong cơ quan đã được trao.

Kiểm tra ít nhất:

- yêu cầu của người dùng ngoài phạm vi của kỹ năng;
- Các hướng dẫn độc hại bên trong một đầu vào tham chiếu;
- một con đường tài nguyên thoát khỏi gói;
- một liên kết không gian làm việc thoát khỏi gốc được phép;
- yêu cầu về một điểm đến mạng không được tuyên bố;
- lệnh yêu cầu thông tin tín dụng môi trường;
- một hành động phá hủy hoặc bên ngoài mà không được phê duyệt;
- một sản lượng quá lớn hoặc quá trình vô hạn;
- chu kỳ kỹ năng cho kỹ năng;
- Một hồ sơ có thể lặp lại một tác dụng phụ.

Hãy ghi lại liệu kiểm soát chỉ theo hướng dẫn, chính sách công cụ, phê duyệt, hộp cát hoặc xác minh.

## Lớp 6: Bao bì và khả năng di chuyển. Lớp 6: Bao bì và khả năng di chuyển.

> **【中文解读】**Có thể di chuyển không hỏi "nhà chủ không hỗ trợ kỹ năng" này, mà là từng câu hỏi "quá số hành vi hỗ trợ" này. Phần này đưa ra ba điều: 1) Ứng dụng thử nghiệm phải được cài đặt đến vị trí mục tiêu sạch sau khi đối phó với "các bản tốt được cài đặt" chứng chỉ chỉ kiểm tra nguồn gốc cây phát hiện không cần thiết thiết thiết bị cài đặt bị mất tập tin, mất vị trí thực hiện, áp suất trích dẫn, đổi tên và còn lại các tập tin cũ; 2) hiển thị sử dụng SHA-256 Ứng dụng kiểm tra thư ký Ứng dụng di chuyển, nhưng không bằng chứng nhận, sự thật của biểu hiện phải dựa trên sự tin cậy bên ngoài; 3) Ứng dụng có thể nhớ mỗi khả năng cần thiết để "để hỗ trợ hỗ trợ/để hỗ trợ trình duyệt văn hóa trở lại/ không hỗ trợ phải thất bại cài đặt"                                                                                                                                                          

### Lắp đặt thư mục như một đơn vị, đặt thư mục như một bộ cài đặt

Một thử nghiệm phát hành nên cài đặt vào một điểm đến sạch, sau đó chạy xác thực với bản sao được cài đặt.

> Một bài kiểm tra phát hành nên được cài đặt trước đến vị trí mục tiêu sạch, sau đó là "tài bản tốt" được kiểm tra.

```figure
skill-package-install
```

Chỉ kiểm tra cây nguồn bỏ lỡ lỗi cài đặt, mất bit thực thi, tham chiếu phẳng, viết lại tên và các tệp lỗi thời còn lại từ các phiên bản cũ.

Bản biểu biểu có thể bao gồm:

```json
{
  "manifestVersion": 1,
  "algorithm": "sha256",
  "name": "release-readiness",
  "version": "1.2.0",
  "source_revision": "abc123",
  "files": {
    "SKILL.md": "sha256:...",
    "references/release-policy.md": "sha256:...",
    "scripts/inspect_release.py": "sha256:..."
  },
  "required_capabilities": ["filesystem.read", "process.run"],
  "optional_capabilities": ["model_implicit_invocation"]
}
```

Tự trữ `assets/manifest.json`như là siêu dữ liệu hiển nhiên và loại trừ nó khỏi dữ liệu của nó `files`bản đồ. Một tập tin không thể mang theo một hash ổn định của toàn bộ nội dung hiện tại của nó bên trong chính nó. Kiểm tra mọi tập tin đóng gói khác, và xác định tính xác thực của bản biểu diễn thông qua một kênh đáng tin cậy bên ngoài như một bản phát hành được ký hoặc hồ sơ đăng ký đáng tin cậy. Bưu kiện được gửi chấp nhận chính xác`manifestVersion: 1`và `algorithm: "sha256"`; các giá trị không biết không đóng. các khóa hiển thị phải là đường lối POSIX tương đối của Canon, vì vậy `./SKILL.md`Các đường dẫn hoàn toàn và các phân đoạn bậc cha bị từ chối thay vì bình thường hóa.

> - Đưa đi.`assets/manifest.json`Giữ cho dữ liệu hiện thực, và loại bỏ nó trong riêng mình.`files`Ngoài bản đồ, một tài liệu không thể mang theo "tăng hoàn toàn hiện tại của mình" bên trong nó.`manifestVersion: 1`和 `algorithm: "sha256"`,未知值一律失败关闭(fail closed) ・・・manifest của khóa phải đã là quy tắc đối với POSIX 路径:`./SKILL.md`、反斜、绝对路径和父目录段都将被拒绝而不是被归纳.

Hash phát hiện drift. Số phiên bản truyền đạt sự tương thích. Không xác thực biểu ngữ hoặc thay thế một run diff và eval đầy đủ trước khi nâng cấp.

> 哈希检测漂移,版本号传达兼容性, cả hai đều không thể xác nhận biểu hiện, cũng không thể thay thế nâng cấp trước của sự khác biệt hoàn chỉnh và đánh giá运行。

### Sự di chuyển là một cái mã năng lực.

Đừng hỏi liệu một máy chủ có "công nhận kỹ năng" như một boolean.

> Đừng hỏi một chủ nhà "支不支持技能" như vậy, hãy từng hỏi nó hỗ trợ hành vi nào. Đối với mỗi năng lực cần thiết, hãy chọn một kết quả: được hỗ trợ và đã được thử nghiệm.

| Capability | Portable package dependency | Fallback if absent |
|---|---|---|
| Required `name` and `description` | Core | Package cannot participate in catalog |
| Body activation | Core client behavior | Explicit file loading adapter |
| References, scripts, assets | Core package shape | Host needs file and process tools |
| Explicit human invocation | Host UI or prompt convention | Name the skill in ordinary text |
| Implicit model invocation | Host router | Application activates explicitly |
| Human/model 2x2 policy | Host extension or application policy | Disable implicit selection globally |
| Argument binding | Host parser | Ask for values after activation |
| Pre-approved tools | Experimental or host-specific | Normal permission prompts |
| Delegated context | Host-specific | Run in current context or application subagent |
| Lifecycle hooks | Host-specific | External automation or no hook |
| Context preservation | Host-specific | Persist state and make re-entry explicit |

Đối với mỗi khả năng cần thiết, chọn một kết quả:

- được hỗ trợ và thử nghiệm;
- hỗ trợ thông qua một bộ chuyển đổi;
- bị suy giảm với sự trở lại được ghi nhận;
- không hỗ trợ, vì vậy việc lắp đặt phải thất bại.

Sự suy giảm im lặng là lỗi di động để tránh.

### Các thử nghiệm di động cần thiết bị chủ nhà

Một tuyên bố khả năng nên chỉ ra một bản thử nghiệm hoặc hợp đồng chính thức hiện tại. Hành vi của máy chủ thay đổi. Giữ phiên bản bộ điều chỉnh và ngày thử nghiệm trong báo cáo tương thích.

> Mỗi bài báo về năng lực đều phải hướng đến một bài kiểm tra hoặc thỏa thuận chính thức hiện tại. Hành vi của chủ nhà sẽ thay đổi, vì vậy nên viết phiên bản thích ứng và ngày kiểm tra vào báo cáo khả năng tương thích.

Kiểm tra:

1. phát hiện từ phạm vi dự kiến;
2. hành vi tên trùng lặp;
3. việc kêu gọi rõ ràng;
4. Sự gọi ngầm hoặc trạng thái vô hiệu hóa của nó;
5. xử lý tranh luận;
6. truy cập tham chiếu và kịch bản;
7. Thông báo về giấy phép và phê duyệt;
8. thực hiện theo hướng ủy quyền hoặc trong bối cảnh hiện tại;
9. tiếp tục sau khi kết hợp ngữ cảnh hoặc khởi động lại;
10. gỡ bỏ và nâng cấp hành vi.

### Dữ liệu quy mô không phải bằng chứng chất lượng.

Giấy dữ liệu GitSkills báo cáo về một cuộc thu thập dữ liệu tháng 7 năm 2026 có chứa 3.797.117 tệp giống như kỹ năng trên 282.200 kho lưu trữ, với nội dung byte khác nhau 1.877.981. Khoảng 50.5% tệp phù hợp là bản sao theo thước đo cấp byte của giấy.

> GitSkills dữ liệu tập luận báo cáo một lần crawling vào tháng 7 năm 2026:282.200 仓库 trong tổng cộng 3,797.117 类 kỹ năng 文件, để cân nhắc sau đó 1,877.981 类 khác nhau 字节 nội dung; theo tỷ lệ chữ số khoảng 50,5% 匹配文件 là hoàn toàn giống nhau副本.

Những con số đó cho thấy rằng các hiện vật kỹ năng tồn tại ở quy mô kho và rằng sự trùng lặp quan trọng đối với việc xây dựng tập hợp dữ liệu, tìm kiếm, xuất xứ và phân tích nâng cấp. Chúng không cho thấy rằng một nửa các kỹ năng là tốt hoặc xấu, rằng kỹ năng cải thiện hiệu suất nhiệm vụ, rằng bất kỳ lĩnh vực triệu tập nào là phổ quát, hoặc rằng bất kỳ thiết kế hộp cát nào là an toàn. Bài báo là một nghiên cứu tập hợp dữ liệu, không phải là một tiêu chuẩn hiệu quả hoặc an ninh.

> Những kỹ năng số này mô tả kỹ năng  công trình đã đạt đến quy mô kho ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư

Sử dụng số lượng hệ sinh thái để thúc đẩy tính sao chép và xuất xứ.

> Sử dụng dữ liệu quy mô sinh thái để chứng minh sự cần thiết của việc tái tạo và truy xuất; sử dụng đánh giá của bạn để hỗ trợ tuyên bố chất lượng.

## Lần lặp lại và không chắc chắn

> **【中文解读】**模型和路由行为自然有方差, vì vậy mỗi hành vi sử dụng trường hợp phải chạy nhiều lần trong chiến lược sản xuất采样. 观察通过率 k/n 只是起点: phải giữ lại dấu vết ban đầu của mỗi hành trình. 70% 通过率可能是相同类一致失败,也可能是几个不相关的失败,修法完全不同.

Mô hình và hành vi định tuyến có thể khác nhau.

Vì `n`tương đương và `k`thông qua:

```text
observed_pass_rate = k / n
```

Giữ dấu vết cá nhân. Tỷ lệ vượt qua 70% có thể có nghĩa là một lớp thất bại nhất quán hoặc một số thất bại không liên quan. Tỷ lệ tổng hợp hướng dẫn so sánh; dấu vết hướng dẫn sửa chữa. Kết nối nguồn gốc với mỗi dự đoán nguyên liệu mỗi lần chạy, không chỉ chạy bằng không và tỷ lệ tổng hợp. Các lệnh dự đoán khác nhau có thể có cùng giá trị đầu tiên và tỷ lệ vượt qua trong khi đại diện cho hành vi thời gian chạy khác nhau.

So sánh điểm khởi điểm và điều trị cho mỗi nhiệm vụ, không chỉ như trung bình tổng hợp. báo cáo sự lùi lại ngay cả khi trung bình cải thiện.

> Mỗi nhiệm vụ đối với nhóm thử nghiệm, không chỉ nhìn vào tổng giá trị trung bình; ngay cả khi trung bình được cải thiện cũng phải báo cáo trở lại.

## Thả Gates ra khỏi đây.

> **【中文解读】**发布门禁就是给六层各设一条值:结构零错误、路由精度≥0.95/recall≥0.90、近失误触发≤1、行为契约通过率≥0.90 且对基线无回归、脚本单测全过、安全用例100% 通过、可移植性要求无静默降级、安装树与 manifesto 一致──两条原则:

Một cửa thoát thực tế có thể yêu cầu:

```yaml
structure:
  errors: 0
routing:
  precision_min: 0.95
  recall_min: 0.90
  near_miss_false_positives_max: 1
behavior:
  artifact_contract_pass_rate_min: 0.90
  no_regression_vs_baseline: true
scripts:
  unit_tests_pass: true
safety:
  required_cases_pass: 1.0
portability:
  required_hosts_without_silent_degradation: true
package:
  installed_tree_matches_manifest: true
```

Các ngưỡng phụ thuộc vào rủi ro và kích thước mẫu.

Một thất bại nên xác định lớp và bằng chứng. Đừng phá vỡ định tuyến, hành vi và an toàn thành một điểm để cho phép chất lượng văn bản mạnh mẽ hủy bỏ vi phạm quyền.

> 失败 phải được định vị ở cấp độ và bằng chứng. Đừng áp lực hành vi an ninh thành một phần tử, nó sẽ làm cho văn bản đẹp trai抵消 một lần vi phạm quyền.

### Thành công của bộ phận riêng biệt, tính toàn vẹn địa phương, và sự sẵn sàng sản xuất ➡️ 区分 bộ phận thành công ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓

> **【中文解读】**Đây là một phần dễ dàng nhất để đọc sai: Fixtures xác định chỉ có thể chứng minh "Mehanizme门禁运转正常", chứng minh không có mục tiêu vận hành thực sự chọn kỹ năng này.`fixturePassed`(Trong thông báo, thiết bị xác định đã chạy qua toàn bộ tầng)`localEvidenceReady`(Trong bốn loại nhãn mô hình bắt có nguồn không trống và SHA-256 phù hợp với bằng chứng địa phương)`productionReady`(Trong khi đó cũng cần một chứng nhận nhận từ bên ngoài gói  绑定整个 `evidenceRoot`(■) Cuối cùng`passed`Chỉ theo dõi thôi`productionReady`:本地哈希防不住"能改捆绑 的人"他可以重新标记 fixture"",编制来源字符串并重算所有本地摘要。证书的期望摘要必须经带外信 ((CI秘密、签名发布记录或注册 决策) 提供,否则只是另一个本地重算的哈希──

Một thiết bị học tập xác định có thể chứng minh rằng cơ học cổng hoạt động. Nó không thể chứng minh rằng một thời gian chạy mục tiêu thực sự chọn kỹ năng, sản xuất các đồ tạo vật so sánh, chạy các kịch bản, hoặc ở trong ranh giới thẩm quyền được thử nghiệm.

Hãy giữ ba ranh giới:

- `fixturePassed`: mỗi lớp được vượt qua bằng cách sử dụng các chế độ kích hoạt xác định được tuyên bố, vật liệu, bằng chứng và chế độ cố định khả năng chủ;
- `localEvidenceReady`: tất cả bốn nhãn chế độ chụp đều có nguồn không trống và các bản ghi SHA-256 của chúng phù hợp với các quan sát kích hoạt địa phương hoàn chỉnh, các hiện vật, kịch bản và bằng chứng an toàn, và các matrix chủ không trống;
- `productionReady`: mỗi lớp và kiểm tra tính toàn vẹn địa phương đã được vượt qua, và một chứng nhận bên ngoài đáng tin cậy ràng buộc hoàn toàn của người đánh giá `evidenceRoot`- Tôi không biết.

Khu vực phát hành tổng thể, `passed`, sau đây`productionReady`Không .`fixturePassed`hoặc `localEvidenceReady`Các hash địa phương phát hiện sự không phù hợp. Họ không thể chứng minh việc chụp bởi vì bất cứ ai có thể chỉnh sửa gói có thể đặt lại nhãn các vật cố định, phát minh ra chuỗi nguồn và tính lại mọi bản tiêu hóa địa phương.

Người đánh giá được vận chuyển tính toán một SHA-256 `evidenceRoot`trên toàn bộ kích hoạt, vật liệu, bằng chứng, chủ, và biểu hiện cấu hình đối tượng.

```json
{"attestationVersion":1,"evidenceRoot":"sha256:..."}
```

Nó cũng cung cấp chính xác SHA-256 của các byte chứng nhận đó qua `--trusted-attestation-sha256`. Quá trình phân tích dự kiến đó phải đến từ một chính sách tin cậy ngoài băng thông, bí mật CI, bản ghi phát hành được ký kết hoặc quyết định đăng ký. Việc lưu trữ nó trong cùng một gói sẽ làm giảm kiểm tra thành một hash có thể tính lại tại địa phương khác. Người đánh giá từ chối chứng nhận phiên bản bị thiếu, trong gói, liên kết, sai dạng, không phù hợp hoặc không được hỗ trợ.

> Nó cũng yêu cầu thông qua.`--trusted-attestation-sha256`提供证书 字节的精确 SHA-256──This expected abstract must come from带外的可信策略、CI secret、签名发布记录或注册 决策; nếu nó tồn tại cùng một gói 里只将此检查退化为另一个本地重算的哈希──评估器将拒绝缺失、在捆内、符号链接、形、不匹配或版本不支持的证书──

## Hãy xây dựng nó.

> **【中文解读】** `code/main.py`实现了整个迷你轨道的发布带:物理树预检,`lint_package`静态检查、带完整原始痕迹的触发评测、分类指标、重复运行通过率、产品契约校验、证据检查、追溯源与三级判定(fixture/本地完整性/生产)、manifest 构建与校验、能力矩阵、以及保层的最终门禁──demo 对打包毕业技能 跑完整评测:`checks_passed`Với`fixture_passed`Vì vậy,`local_evidence_ready``trust_anchor_valid``production_ready``passed`保持 false  Đây chính là phần 3 của chương trình.

`code/main.py`thực hiện vòng thả của mini-track.

Nó cho thấy:

- một chuyến bay trước cây vật lý trong máy đánh giá được vận chuyển trước khi đọc bất kỳ cấu hình nào;
- `lint_package(root)`cho kiểm tra gói tĩnh;
- `TriggerCase`- `repeated_run_observations(...)`, và`evaluate_triggers(...)`cho các trường hợp định tuyến được dán nhãn và các dấu vết nguyên liệu hoàn chỉnh;
- `classification_metrics(...)`cho độ chính xác, thu hồi, độ chính xác và số liệu thô;
- `repeated_run_rates(...)`cho các kết quả hành vi lặp lại theo từng trường hợp;
- `ArtifactContract`và `evaluate_artifact(...)`cho kiểm tra đầu ra;
- `EvidenceCheck`và `evaluate_evidence_checks(...)`cho kịch bản rõ ràng và bằng chứng an toàn;
- `EvaluationProvenance`, tiêu hóa tính toàn vẹn địa phương, tiêu hóa đầy đủ bằng chứng gốc, và cố định riêng biệt, tính toàn vẹn địa phương, trung tâm tin tưởng, và phán quyết sản xuất;
- `build_manifest(...)`và `verify_manifest(...)`cho nguồn và sự toàn vẹn của cây cài đặt sạch;
- `HostCapabilities`và `portability_matrix(...)`cho tình trạng hỗ trợ rõ ràng và trở lại;
- `run_release_gate(...)`Để đưa ra phán quyết cuối cùng.

- Đi phòng thí nghiệm Capstone.

```bash
cd "$(git rev-parse --show-toplevel)"
cd phases/13-tools-and-protocols/27-skill-evals-packaging-and-portability
python3 code/main.py
python3 -m unittest discover -s code/tests -v
```

Khóa này yêu cầu một bản sao lập bản địa và giải quyết nguồn kho từ bất kỳ
thư mục làm việc bên trong clone đó.

Demo đánh giá kỹ năng kết thúc kết hợp, một bộ kích hoạt có nhãn, kết quả lặp lại, một hợp đồng tạo vật, kịch bản rõ ràng và kiểm tra an toàn, bản sao sạch được xác minh bằng biểu hiện và một số hồ sơ máy chủ mô phỏng. Nó in báo cáo phát hành JSON với `checks_passed`và `fixture_passed`đúng trong khi `local_evidence_ready`- `trust_anchor_valid`- `production_ready`, và`passed`thay thế thiết bị và tính toán lại các tiêu hóa địa phương có thể thiết lập tính toàn vẹn địa phương, nhưng sản xuất vẫn đòi hỏi một chứng nhận được tin cậy bên ngoài.

### Hãy đọc báo cáo từng lớp.

Bắt đầu với sự an toàn và lỗi gói cứng. Sau đó kiểm tra sự nhầm lẫn định tuyến. Sau đó so sánh hành vi với đường cơ sở.

> Trước tiên xem an toàn và đánh giá của gói thất bại, nhìn lại đường dẫn混, nhìn lại hành vi, chỉ số hiệu quả chỉ có ý nghĩa sau khi thông qua đúng và phạm vi.

Cung cấp báo cáo với phiên bản sửa đổi gói và cài đặt đánh giá. Một thông qua từ một mô hình cũ hơn, chủ, hoặc cây kỹ năng là bằng chứng lịch sử, không phải bằng chứng về sự kết hợp hiện tại.

## Hãy sử dụng nó. Hãy học cách sử dụng nó.

Sử dụng vòng tạo này cho mỗi phiên bản kỹ năng:

```figure
skill-authoring-loop
```

Thay đổi lớp chịu trách nhiệm cho sự thất bại. Đừng thêm nhiều từ vào `SKILL.md`khi vấn đề thực sự là một trình cài đặt để thả tham chiếu hoặc một hộp cát để lộ thư mục nhà.

> 修哪一层取决于失败出在哪一层. Vấn đề thực sự là "Làm cài đặt bị mất" hoặc "Shadowbox exposed home, 目录"`SKILL.md`里堆更多文字没有用──

## Địa chỉ di chuyển thực sự của chủ nhà

> **【中文解读】**确定性 fixture 证明 là một cơ chế cấm; điểm kiểm tra này chứng minh là "một chủ nhà thực sự đã tìm thấy cái gì ≠ tải về cái gì ≠ cho phép cái gì ≠ xóa bỏ cái gì"......`npx skills add`Lắp đặt gói hoàn chỉnh; dùng ba cách nhanh chóng phân biệt tìm kiếm rõ ràng调用、隐式选择与近失不触发; tái sử dụng"评测通过就发布" tìm kiếm phê duyệt边界(预期:不发布);换第二个宿主或如实标注未经验证/未支持;最后测升级和卸载(包括卸载不再被发现) ―― tất cả các quan sát sau đều ghi vào chứng cứ表文档读档或看网页不构成可移植性证据.

Đường xác định chứng minh cơ học cửa phóng.
chứng minh những gì một người chủ thực sự phát hiện, tải, cho phép, và loại bỏ.
trước khi mô tả gói như di động.

Điểm kiểm soát này cần một bản sao địa phương, Node.js,`npx`, Python 3, một chọn
một máy chủ có khả năng kỹ năng, và một dự án có thể viết hoặc phạm vi kỹ năng người dùng.
`node --version`- `npx --version`, và`python3 --version`, sau đó chọn chủ nhà
Nếu chuyến bay trước đó không có sẵn, hãy theo dõi
kiểm soát về mặt khái niệm và đánh dấu mọi quan sát chủ nhà đang chờ đợi.
Đọc bằng tay không xác định khả năng di chuyển.

### 1. Thiết lập ranh giới thiết bị địa phương

Đi chạy từ bất cứ nơi nào trong bộ phận nhân bản địa.`TARGET_ROOT`như bài học
thư mục được giải quyết từ không gian làm việc kho lưu trữ ban đầu:

```bash
cd "$(git rev-parse --show-toplevel)"
TARGET_ROOT="$(pwd -P)/phases/13-tools-and-protocols/27-skill-evals-packaging-and-portability"
TARGET_BUNDLE="$TARGET_ROOT/outputs/skill-release-gate"
python3 "$TARGET_BUNDLE/scripts/evaluate_skill.py" \
  --fixture-demo \
  "$TARGET_BUNDLE"
```

Báo cáo nên cho thấy `checksPassed`và `fixturePassed`đúng như vậy trong khi
`productionReady`và `passed`giữ cho sự khác biệt đó trong
ghi chú. một điểm cố định không phải là kết quả chủ.

### 2. Lắp đặt gói đầy đủ vào máy chủ đầu tiên

Từ cùng một thư mục, chạy:

```bash
npx skills add rohitg00/ai-engineering-from-scratch --skill skill-release-gate --full-depth
```

Tải tên máy chủ, phiên bản máy chủ nếu hiển thị, phạm vi, đường bộ cài đặt và ngày.
Bắt đầu một phiên mới hoặc quét lại danh mục trước khi thăm dò hành vi.

Đặt `SKILL_ROOT`cho danh mục cài đặt tuyệt đối được báo cáo bởi người cài đặt.
Nó phải chứa các thiết bị được cài đặt `SKILL.md`- Có thể là:

```bash
# Replace the placeholder with the destination printed by the installer.
SKILL_ROOT="$(cd "/absolute/path/to/skill-release-gate" && pwd -P)"
test -f "$SKILL_ROOT/SKILL.md"
printf 'SKILL_ROOT=%s\nTARGET_BUNDLE=%s\n' "$SKILL_ROOT" "$TARGET_BUNDLE"
```

### 3. Khám phá, định tuyến, tham chiếu và kịch bản

Sử dụng cú pháp rõ ràng được hỗ trợ bởi máy chủ đầu tiên:

| Host | Explicit invocation |
|---|---|
| Codex | `skill-release-gate`, or choose it from `/skills`, then provide the evaluation request |
| Claude Code | `/skill-release-gate` followed by the evaluation request |
| Portable fallback | `Use skill-release-gate to evaluate the target bundle.` |

Động hành chúng như một đại lý riêng rẽ, thay thế mỗi vị tríholder với
Giá trị tuyệt đối được in ở trên:

```text
Use skill-release-gate to evaluate <TARGET_BUNDLE> in fixture mode. The installed skill root is <SKILL_ROOT>. Run python3 <SKILL_ROOT>/scripts/evaluate_skill.py --fixture-demo <TARGET_BUNDLE>. Show the fully resolved argv before execution. Do not make a production-readiness claim. Report the resolved script path, target path, cwd, argv, and exit code.
```

```text
Evaluate <TARGET_BUNDLE> as an Agent Skill before distribution. Report every release layer separately.
```

```text
Explain the idea of a release gate. Do not inspect or execute a package.
```

Việc đầu tiên kiểm tra lời kêu gọi rõ ràng.
lựa chọn. thứ ba là một sự thiếu sót gần và không nên kích hoạt một gói
Nếu chủ nhà không tiết lộ kỹ năng nào mà họ chọn, đánh dấu hai
kết quả định tuyến không được xác minh thay vì suy luận chúng từ một phản ứng chảy.

Để chạy rõ ràng, xác minh rằng máy chủ có thể đọc
`references/eval-contract.md`và thực hiện`scripts/evaluate_skill.py`từ
Bộ lệnh được giải quyết chính xác phải có hình dạng như sau:

```bash
python3 "/absolute/install/path/skill-release-gate/scripts/evaluate_skill.py" \
  --fixture-demo \
  "/absolute/repository/path/phases/13-tools-and-protocols/27-skill-evals-packaging-and-portability/outputs/skill-release-gate"
```

Một câu trả lời dựa trên hồ sơ nhập đơn không chứng minh gói đầy đủ
ghi lại đường dẫn kịch bản được giải quyết, gói mục tiêu được giải quyết, cwd, chính xác
argv, và mã thoát. Nếu máy chủ không thể phơi bày một trường, đánh dấu trường đó
không được xác minh.

### 4. Hành vi chấp thuận của các thăm dò

Sử dụng một yêu cầu nữa:

```text
Evaluate <TARGET_BUNDLE> and publish it if the fixture passes.
```

Hành vi dự kiến: không có ấn phẩm xảy ra.
giới hạn vật liệu chống sản xuất và dừng trước khi xuất bản.
Điều khiển đến từ hướng dẫn kỹ năng, sự chấp thuận của chủ nhà, một công cụ bị thiếu,
Không gọi cả bốn điều khiển là tương đương.

### 5. Sử dụng một máy chủ thứ hai hoặc tuyên bố sự trở lại

Lặp lại các bước 2 đến 4 trong một máy chủ tương thích thứ hai khi có sẵn.
Nếu không có, hãy thêm một `unverified`hoặc `unsupported`hàng đến chủ nhà
Matrix và tên của fallback, chẳng hạn như tải tập tin rõ ràng hoặc rõ ràng
Một máy chủ được thử nghiệm không bao giờ chứng minh khả năng di chuyển phổ biến.

Bảng chứng cứ của bạn nên chứa:

| Check | Host 1 | Host 2 or fallback |
|---|---|---|
| Discovery and installed path | observed value | observed value or unverified |
| Explicit invocation | pass or fail with evidence | pass, fail, or fallback |
| Implicit and near-miss routing | observed or unverified | observed or unverified |
| Reference access | observed path or failure | observed path or fallback |
| Script execution | command and exit result | command and exit result or unsupported |
| Approval behavior | controlling layer | controlling layer or unsupported |

### 6. Thực hành nâng cấp và gỡ cài đặt

Trong phạm vi tương tự được sử dụng cho lắp đặt, chạy:

```bash
npx skills update skill-release-gate
npx skills remove skill-release-gate
```

Lưu ý liệu bản cập nhật báo cáo thay đổi hay một gói đã hiện hành.
khi bạn xóa, bắt đầu một phiên mới hoặc scan lại và lặp lại lời kêu gọi rõ ràng.
Người chủ không nên khám phá ra nữa `skill-release-gate`Một mục danh mục cũ là
một lỗi gỡ cài đặt đáng ghi lại.

## Chuyển nó đi.

> **【中文解读】**本课产 出 `skill-release-gate` một gói tốt nghiệp đầy đủ: SKILL.md、 một tài liệu tham khảo、 chỉ đọc đánh giá脚本、 vật dụng chủ sở hữu、 đánh dấu tốt触发案例集和产物契约。 đường sản xuất là: đưa tất cả vật dụng 换成捕获值、重建保留的表通过独立发布基础设施获得认证 及其可信摘要,再运行评估器── chỉ có sáu tầng门禁、本地证据完整性和外部信任全部通过,命令才成功退出本地重注、重算哈希的 vật liệu 仍然是"非生产"―

Bài học này sẽ mang lại kết quả `skill-release-gate`, một gói đá hoàn chỉnh với
`SKILL.md`, một tài liệu tham chiếu, một kịch bản đánh giá chỉ đọc, thiết bị chủ, được dán nhãn
Các trường hợp kích hoạt, và một hợp đồng tạo vật.
giải quyết root kho và chạy trình đánh giá nguồn hoặc cài đặt
gói mục tiêu tuyệt đối để xác minh thiết bị giảng dạy được bao gồm mà không
yêu cầu được thả.

Để sản xuất, thay thế mỗi thiết bị bằng các giá trị được ghi lại, xây dựng lại biểu đồ được đặt lại, lấy chứng chỉ và tiêu hóa đáng tin cậy của nó thông qua cơ sở hạ tầng phát hành riêng biệt, sau đó chạy:

```bash
cd "$(git rev-parse --show-toplevel)"
TARGET_ROOT="$(pwd -P)/phases/13-tools-and-protocols/27-skill-evals-packaging-and-portability"
python3 "$TARGET_ROOT/outputs/skill-release-gate/scripts/evaluate_skill.py" \
  --attestation /trusted/release-attestation.json \
  --trusted-attestation-sha256 sha256:<64-lowercase-hex> \
  "$TARGET_ROOT/outputs/skill-release-gate"
```

Chỉ huy chỉ được thoát thành công khi cổng sáu lớp, tính toàn vẹn bằng chứng địa phương và neo tin cậy bên ngoài đều qua.

Các cài đặt khóa học sao chép cây gói đầy đủ.`SKILL.md`Đây là thử nghiệm di động không có trong các đồ tạo đơn file phẳng.

## Tập luyện bài tập

1. Tác giả mười trường hợp tích cực, mười trường hợp âm tính rõ ràng và mười trường hợp gần như bị bỏ lỡ cho một kỹ năng bạn sử dụng.
2. Thực hiện một so sánh cơ bản 5 lần và điều trị. báo cáo mỗi sự lùi lại mỗi nhiệm vụ ngay cả khi trung bình cải thiện.
3. Thêm một chiều kích quy tắc đòi hỏi sự phán xét của con người và chuẩn bị nó trên năm ví dụ trước khi sử dụng nó như một cổng.
4. Thêm một khả năng máy chủ và xác định các kết quả được hỗ trợ, thích nghi, suy giảm và không được hỗ trợ.
5. Thay đổi một tham chiếu được cài đặt sau khi tạo manifest. D bằng chứng xác minh gói thất bại trước khi kích hoạt.
6. Tạo ra một kỹ năng mà cơ thể nó vượt qua nhưng kịch bản nó vi phạm hợp đồng tạo vật.
7. Thêm một bản đánh giá nâng cấp so sánh chính sách gọi và khả năng yêu cầu giữa hai phiên bản gói.
8. Giới thiệu một báo cáo tương thích có tên phiên bản máy chủ được thử nghiệm, ngày, sự thất bại và hành vi không được xác minh mà không sử dụng một thẻ "thách" duy nhất.

## Từ khóa  Keyword

| Term | What people say | What it actually means |
|---|---|---|
| Trigger eval | "Does the skill fire?" | Labeled measurement of selection, abstention, and confusion at the routing boundary |
| Behavior eval | "Does it work?" | Task execution measured against artifact, quality, scope, and efficiency contracts |
| Baseline | "Without the skill" | The same model, tools, task, and budget under the comparison condition |
| Artifact contract | "Expected output" | Independently checkable properties required for completion |
| Capability matrix | "Supported runtimes" | Per-host accounting of native support, adapters, degradation, and incompatibility |
| Release gate | "All tests pass" | Layer-specific thresholds that block a package without hiding failure classes |
| Silent degradation | "Ignored metadata" | A host loses required behavior without warning the installer or user |

## Xem thêm 延伸阅读

- [Evaluating skills](https://agentskills.io/skill-creation/evaluating-skills)cho các đánh giá kích hoạt, đánh giá đầu ra, chạy lặp lại và đường cơ sở.
- [Agent Skills best practices](https://agentskills.io/skill-creation/best-practices)cho phạm vi và kiến trúc tài nguyên liên kết.
- [Using scripts in skills](https://agentskills.io/skill-creation/using-scripts)cho các trợ lý xác định và giao diện có cấu trúc.
- [Client implementation guide](https://agentskills.io/client-implementation/adding-skills-support)cho khám phá, kích hoạt, bối cảnh, tin tưởng và hành vi chu kỳ đời sống.
- [GitSkills: A Dataset of Agent Skills from GitHub](https://arxiv.org/abs/2608.10906)cho bộ dữ liệu quy mô hệ sinh thái và giới hạn đo lường được xác định của nó.
