# CAIS, CAISI, và rủi ro quy mô xã hội

> Trung tâm An toàn AI (CAIS, San Francisco, được thành lập năm 2022 bởi Hendrycks và Zhang) công bố khung bốn rủi ro  sử dụng độc hại, cuộc đua AI, rủi ro tổ chức, AI gian lận  và tuyên bố tháng 5 năm 2023 về nguy cơ tuyệt chủng được ký bởi hàng trăm giáo sư và lãnh đạo công ty. Các bản phát hành năm 2026 từ CAIS: bảng điều khiển AI cho đánh giá mô hình biên giới, Chỉ số lao động từ xa (với AI quy mô), Tờ chiến lược siêu thông minh, Báo chí AI Frontiers. Một thực thể riêng biệt: Trung tâm tiêu chuẩn và đổi mới AI của NIST (CAISI)  Các thỏa thuận tình nguyện đối mặt với chính phủ Hoa Kỳ và đánh giá khả năng không được phân loại tập trung vào rủi ro vũ khí mạng, sinh học và hóa học. CAIS đánh dấu rủi ro tổ chức là một trong bốn rủi ro cấp cao nhất: văn hóa an toàn, kiểm toán nghiêm ngặt, phòng thủ đa tầng và an ninh thông tin là cơ bản nhưng thường xuyên được giao dịch so với tốc độ triển khai. California SB-53, nếu được ký kết, sẽ là quy định rủi ro thảm họa cấp tiểu bang đầu tiên của Hoa Kỳ.

> **【中文解读】**Bài viết này giới thiệu về đánh giá rủi ro xã hội của CAIS/CAISI AI 系统 đối với tác động tiềm ẩn và phân tích rủi ro xã hội


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, four-risk inventory and mitigation matcher) | **语言:** Python（标准库，四风险盘点与缓解匹配器）
**Prerequisites:** Phase 15 · 19 (RSP), Phase 15 · 20 (PF + FSF) | **前置知识:** Phase 15 · 19（RSP）、Phase 15 · 20（PF + FSF）
**Time:** ~45 minutes | **时间:** ~45 分钟

>  **【前置】**Học本节前请先掌握:Phase 15·19-20(实验室 RSP) Phase 15·21(METR 外部评估) 本节是"第三视角"民间社会和政府对AI风险的态度──
>  **【类比】**CAIS = "AI 风险的智囊团" (民间研究,发言,推框架);CAISI = "AI 风险的政府办公室" (NIST 下属,协调自愿协议) (Bản danh từ "AI 风险的智囊团") (Bản danh từ "AI 风险的智囊团" (AI 风险的智囊团) (Bản danh từ "AI 风险的智囊团"), nhưng nhiệm vụ khác.
> 🤔 **【困惑】**Q: Những tổ chức này có lợi gì cho tôi làm AI 工程 có lợi gì? 直接用途是合规: nếu sản phẩm của bạn liên quan đến trường hợp rủi ro cao (làm y tế, tài chính, tuyển dụng), cần tham khảo CAIS framework for risk assessment, có thể cần phải tuân thủ EU AI Act, California SB-53 等法规.

## Vấn đề  vấn đề giới thiệu

Bài học 19 và 20 bao gồm các chính sách quy mô nội bộ trong phòng thí nghiệm. Bài học 21 bao gồm đánh giá khả năng độc lập. Bài học này bao gồm quan điểm thứ ba: xã hội dân sự và các tổ chức chính phủ định hình cuộc thảo luận công cộng và cơ sở quy định cho rủi ro AI thảm họa.

> Các bài học 19 và 20 bao gồm chính sách mở rộng nội bộ phòng thí nghiệm. Bài học 21 bao gồm đánh giá năng lực độc lập. Bài học này bao gồm góc nhìn thứ ba: hình thành cuộc thảo luận công cộng và thảm họa AI 风险监管基线民间社会和政府组织.

CAIS là một tổ chức nghiên cứu phi lợi nhuận xuất bản khung để suy nghĩ về rủi ro AI và phối hợp các tuyên bố công cộng. CAISI là một trung tâm chính phủ Hoa Kỳ trong NIST điều hành các thỏa thuận tự nguyện với các phòng thí nghiệm và đánh giá khả năng không được phân loại. Tên bắt chước; các nhiệm vụ không chồng chéo.

> 两个实体很重要――CAIS là tổ chức nghiên cứu phi lợi nhuận trong NIST, với các phòng thí nghiệm hoạt động theo thỏa thuận tự nguyện và đánh giá khả năng bí mật.

Nội dung thực tế: Quadro bốn rủi ro của CAIS là phân loại rủi ro quy mô xã hội được trích dẫn rộng rãi nhất trong văn học. Văn hóa an toàn và rủi ro tổ chức là một trong bốn, và đây là một trong những trực tiếp nhất dưới sự kiểm soát của một học viên. SB-53 (California) sẽ là quy định rủi ro thảm họa cấp tiểu bang đầu tiên của Hoa Kỳ nếu được ký; các vấn đề khung của dự luật vì quy định cấp tiểu bang đã dẫn đến hành động liên bang trong chính sách công nghệ của Hoa Kỳ.

> Ứng dụng:Căn cứ bốn rủi ro của CAIS là một trong những tài liệu được trích dẫn rộng rãi nhất về quy mô xã hội. Bảo an văn hóa và tổ chức rủi ro là một trong số đó, là một trong những điều trực tiếp kiểm soát bởi các nhà thực hành. SB-53 ((Kazor) Nếu ký kết sẽ là một trong những điều khoản quản lý rủi ro thảm họa cấp tiểu bang đầu tiên của Hoa Kỳ; khung của dự luật này quan trọng, vì điều khoản cấp tiểu bang là một trong những hành động liên bang hàng đầu trong lịch sử chính sách công nghệ Hoa Kỳ.

## Khái niệm cốt lõi

### CAIS  Trung tâm An toàn AI

- Được thành lập: 2022 tại San Francisco, bởi Dan Hendrycks và các đồng nghiệp (tên "Zhang" đề cập đến một cộng tác viên ban đầu, không phải là một đồng sáng lập hiện tại; xem trang web CAIS cho lãnh đạo hiện tại).
  Trung ngữ翻译:成立:2022年在旧金山,由 Dan Hendrycks 和同事创立("Zhang"指早期合作者,非当前联合创始人;当前领导见 CAIS 网站) ]]
- Tình trạng: 501 ((c) ((3) phi lợi nhuận.
  中文翻译:状态:501(c)(3) 非营利。
- Kết quả đáng chú ý năm 2023: tuyên bố về nguy cơ tuyệt chủng, được đồng ký bởi hàng trăm nhà nghiên cứu và CEO. Được tuyên bố: "Há giảm nguy cơ tuyệt chủng từ AI nên là ưu tiên toàn cầu cùng với các rủi ro quy mô xã hội khác như đại dịch và chiến tranh hạt nhân".
  Trung ngữ翻译:2023 显著产出:灭绝风险声明,数百研究员和首席执行官联合签署――声明:"Làm giảm AI 灭绝风险应对与流行病和核战争等其他社会规模风险并列为全球优先――"
- 2026 sản phẩm: bảng điều khiển AI cho đánh giá mô hình biên giới, Chỉ số lao động từ xa (cùng với AI quy mô), Tờ chiến lược siêu thông minh, Báo chí AI Frontiers.
  中文翻译:2026 产出:前沿模型评估 AI Dashboard、Remote Labor Index(与 Scale AI 联合)、Superintelligence Strategy Paper、AI Frontiers 简报。

### Quadro bốn rủi ro

Các cơ sở khung của CAIS nhóm rủi ro AI thảm họa thành bốn loại cấp cao:

> Các khuôn khổ của CAIS sẽ phân chia AI 风险 thảm họa thành bốn loại hàng đầu:

1. **Malicious use**: một diễn viên xấu sử dụng AI để gây hại (sự tổng hợp vũ khí sinh học, thông tin sai lệch, tấn công mạng).
   Trung ngữ翻译:**恶意使用**:坏人 sử dụng AI gây tổn thương
2. **AI races**: áp lực cạnh tranh giữa các phòng thí nghiệm, các công ty hoặc các quốc gia đẩy triển khai vượt qua điểm nơi nó an toàn.
   Trung ngữ翻译:**AI 竞赛**: phòng thí nghiệm, công ty hoặc quốc gia áp lực cạnh tranh thúc đẩy triển khai hơn điểm an toàn.
3. **Organizational risks**: động lực trong phòng thí nghiệm (những thất bại trong văn hóa an toàn, kiểm toán không đủ, an ninh thiếu nguồn lực) tạo ra một sự triển khai kém.
   Trung ngữ翻译:**组织风险**: interne实验室动态(安全文化失败、审计不足、安全资源不足) tạo ra triển khai tồi tệ.
4. **Rogue AIs**: một AI đủ khả năng theo đuổi các mục tiêu mâu thuẫn với phúc lợi con người.
   Trung ngữ翻译:**失控 AI**: đủ khả năng AI  theo đuổi mục tiêu xung đột với phúc lợi con người.

Đây không phải là phân loại duy nhất; nó là được trích dẫn nhiều nhất. Các loại không loại trừ lẫn nhau  AI gian lận được sản xuất bởi một tổ chức giao dịch kiểm toán tốc độ trong một cuộc đua là tất cả bốn.

> Đây không phải là quy luật phân loại duy nhất; nó là những quy định được trích dẫn thường xuyên nhất.

### Những nơi có rủi ro tổ chức

Trong bốn loại, rủi ro tổ chức là điều dễ thực hiện nhất cho các học viên. Văn hóa an toàn của phòng thí nghiệm, sự nghiêm ngặt kiểm toán, lớp bảo vệ và an ninh thông tin quyết định liệu các mẫu tàu của họ với các kiểm soát của Bài học 1018 thực sự có được thực hiện hay không, hoặc liệu những kiểm soát đó là các mục danh sách kiểm tra không ai xác minh.

> Trong bốn loại, tổ chức rủi ro là khả năng hoạt động tốt nhất đối với các nhà thực hành. Văn hóa an ninh phòng thí nghiệm, kiểm toán nghiêm ngặt, phòng thủ và an ninh thông tin quyết định mô hình của họ có được phát hành thực tế với các điều khiển của bài học 1018 hay không.

Các đòn bẩy rủi ro tổ chức cụ thể:

> 具体组织风险杆:

- **Safety culture**Các cuộc khảo sát của CAIS cho thấy đây là một dự đoán mạnh mẽ về các đòn bẩy khác.
  Trung ngữ翻译:**安全文化**: Nhóm thành viên có thể tăng cấp trong trường hợp không trả chi phí nghề nghiệp không? CAIS nghiên cứu phát hiện ra đây là yếu tố dự đoán mạnh của các nhóm khác.
- **Rigorous audits**Các kiểm toán nội bộ chỉ tạo ra báo cáo lạc quan.
  Trung ngữ翻译:**严格审计**: bên ngoài và bên trong. Chỉ trong kiểm toán tạo ra một quan điểm.
- **Multi-layered defenses**: không có một lớp duy nhất là đủ (đề tài chạy của giai đoạn 15).
  Trung ngữ翻译:**多层防御**:无单层足够 (không có một tầng đủ)
- **Information security**: model weights leak, eval data leak, monitor-bypass techniques leak. RAND SL-4 trong bài học 19 là một tiêu chuẩn cụ thể.
  Trung ngữ翻译:**信息安全**Mô hình quyền nặng rò rỉ, đánh giá rò rỉ dữ liệu, giám sát quy định tránh rò rỉ kỹ thuật.

### CAISI  Trung tâm tiêu chuẩn và đổi mới AI

- Hoạt động trong NIST.
  Trung ngữ翻译:在NIST内运营。
- Có thỏa thuận tự nguyện với các phòng thí nghiệm biên giới.
  Trung ngữ翻译:与前沿实验室运行自愿协议。
- Ghiên bản đánh giá khả năng không được phân loại tập trung vào rủi ro vũ khí mạng, sinh học và hóa học.
  Trung ngữ翻译: phát hành tập trung mạng lưới, sinh học và hóa học
- Khác với CAIS; các ký tự viết tắt va chạm; kiểm tra URL (nist.gov) để xác nhận bạn đang đọc.
  Trung文翻译:与 CAIS 不同;首字母缩写冲突;检查URL(nist.gov) xác nhận bạn đang đọc ở đâu.

Vai trò của CAISI là đối tác công cộng, đối diện với chính phủ đối với các hoạt động phòng thí nghiệm tư nhân của METR (Dạy 21). Các báo cáo CAISI không được phân loại; báo cáo METR thường được NDA-gate.

> Vai trò của CAISI là METR Private Person Laboratory合作 (第 21 课) của công cộng 面向政府对应物──CAISI 报告非密;METR 报告通常是NDA门控──读者获得更完整的图景──

### California SB-53

Dự luật Thượng viện California (2025-2026 phiên) giải quyết rủi ro thảm họa từ các mô hình biên giới.

> 加州参议院法案 (加州参议院法案) (→20252026 会期) xử lý trước bờ của mô hình thảm họa风险.

- Các ngưỡng khả năng cụ thể gây ra các nghĩa vụ ở cấp độ nhà nước.
  Trung ngữ翻译:触发州级义务的特定能力值──
- Bảo vệ người báo cáo cho nhân viên phòng thí nghiệm AI.
  Trung ngữ翻译:AI 实验室员工举报人保护。
- Yêu cầu báo cáo sự cố đối với các thất bại thảm họa.
  Trung文翻译: 灾难性失败的事故报告要求──

Nếu được ký kết, nó sẽ là quy định nguy cơ thảm họa cấp tiểu bang đầu tiên của Hoa Kỳ. Bất kể tình trạng ký kết, khung của dự luật định hình hóa cách các nhà lập pháp tiểu bang khác tiếp cận vấn đề. Các học viên ở California nên theo dõi tình trạng dự luật; học viên ở nơi khác nên đọc nó để hiểu quy định cấp tiểu bang Hoa Kỳ có thể sẽ trông như thế nào.

> Nếu được ký kết, nó sẽ là giám sát rủi ro thảm họa cấp tiểu bang đầu tiên của Hoa Kỳ. Bất kể tình trạng ký kết, khuôn khổ của dự luật hình thành cách các cơ quan lập pháp tiểu bang khác xử lý vấn đề.

### Nguy cơ trên quy mô xã hội không phải là một vấn đề đơn

Chủ đề chạy của giai đoạn 15  phòng thủ sâu sắc  cũng áp dụng cho tầng xã hội. Không có tổ chức, quy định hoặc khung nào đóng cửa rủi ro thảm họa. Hệ sinh thái chỉ hoạt động khi:

> Chương 15 阶段 贯穿主题深度防御也适用于社会层. Không có tổ chức, quy định hay khung pháp lý nào có thể đóng cửa nguy cơ thảm họa.

- Các nhà thí nghiệm quy mô các chính sách tàu (Dạy 19, 20).
  Trung文翻译:实验室发布扩展政策 (第 19、20 课)
- Các nhà đánh giá bên ngoài tạo ra các phép đo (Học 21).
  Trung文翻译:外部评估者产出测量 (第 21 课)
- Công chúng dân sự theo dõi và công bố (CAIS).
  Trung ngữ翻译:民间社会跟踪和宣传 (CAIS)
- Chính phủ chạy các chương trình tự nguyện và quy định cơ bản (CAISI, SB-53).
  Trung ngữ翻译:政府运行自愿计划和基线监管(CAISI、SB-53)
- Các học viên xây dựng các điều khiển đa tầng (Dạy 1018).
  Trung文翻译:从业者构建多层控件 (从业者构建多层控件) (第 1018 课)

Đây là tổng hợp cuối cùng cho giai đoạn: mỗi bài học trước đó là một lớp trong một chồng có tính toàn diện quan trọng hơn sức mạnh của bất kỳ lớp nào.

> Đây là tổng hợp cuối cùng của giai đoạn: mỗi phần trước đó là một lớp trong khối, tính toàn vẹn của nó quan trọng hơn sức mạnh của bất kỳ một lớp nào.

## Hãy sử dụng nó để thực hiện
```figure
a5-four-risks
```

## Sử dụng nó

`code/main.py`thực hiện một công cụ kiểm tra rủi ro nhỏ. Với một triển khai được đề xuất, nó đánh dấu việc triển khai theo bốn loại rủi ro và trả lại danh sách kiểm tra giảm thiểu. Nó là một trợ giúp đọc cho khung, không thay thế cho phán đoán của con người.

> `code/main.py`实现小型风险盘点工具──给定提议的部署, nó được phân phối theo 4 loại风险, nó được phân phối theo 4 loại风险, nó được phân phối theo 4 loại风险, nó được phân phối theo 4 loại风险, nó được phân phối theo 4 loại风险, nó được phân phối theo 4 loại风险, nó được phân phối theo 4 loại风险, nó được phân phối theo 4 loại风险, nó được phân phối theo 4 loại风险, nó được phân phối theo 4 loại风险, nó được phân phối theo 4 loại风险, nó được phân phối theo 4 loại风险, nó được phân phối theo 4 loại风险, nó được phân phối theo 4 loại风险, nó được phân phối theo 4 loại风险, nó được phân phối theo 4 loại风险, nó được phân phối theo 4 loại.

## Chuyển nó đi.

`outputs/skill-societal-risk-review.md`xem xét một triển khai đối với các rủi ro trên quy mô xã hội: trong bốn loại nào nó liên quan, những biện pháp giảm thiểu nào đang được thực hiện, những rủi ro tổ chức nào.

> `outputs/skill-societal-risk-review.md`审查 triển khai của quy mô xã hội 风险姿态: chạm vào những gì trong bốn loại 已有哪些缓解 组织风险暴露是什么

## Tập luyện bài tập

1. Đi chạy`code/main.py`. Đưa vào ba triển khai tổng hợp ở các quy mô khác nhau. xác nhận các thẻ bốn rủi ro phù hợp với những gì bạn mong đợi; xác định một trường hợp nơi công cụ dưới hoặc quá thẻ.
   Trung ngữ翻译:运行 `code/main.py` nhập vào ba bộ phận khác nhau của bộ phận này.

2. Đọc toàn bộ bài báo CAIS về bốn rủi ro. Chọn một danh mục rủi ro và viết hai đoạn về những gì bạn tin là sự phát triển quan trọng nhất năm 2026 trong danh mục đó.
   Trung ngữ翻译:完整阅读 CAIS 四风险论文──选一个风险类别,写两段关于你认为该类别 2026 最重要发展──

3. Hãy đọc bản thảo hiện tại của California SB-53. xác định một điều khoản mà bạn tin rằng củng cố tư thế nguy cơ thảm họa và một điều mà bạn tin rằng làm suy yếu nó.
   Trung ngữ翻译:阅读加州 SB-53 当前──草案识别你认为强化灾难性风险姿态的一个条款和弱化一个──论证两者──

4. Chọn một triển khai AI sản xuất mà bạn biết (của bạn hoặc một công bố). Đánh giá nó so với các yếu tố rủi ro tổ chức: văn hóa an toàn, nghiêm ngặt kiểm toán, phòng thủ đa tầng, an ninh thông tin.
   Trung ngữ翻译:选一个你知道的生产AI部署 (你知道的生产AI部署) 杆打分: 安全文化,审计严格性,多层防防信息安全, 什么是最弱的?达到标准需要多少成本?

5. Hãy vẽ một phiên bản năm 2028 của khung bốn rủi ro phản ánh một năm năng lực bổ sung và một năm kinh nghiệm triển khai bổ sung. Bạn sẽ thêm, loại bỏ hoặc tập hợp lại gì?
   Trung ngữ翻译:勾勒反映一年额外能力和一年额外外署经验的四风险框架 2028 版本──你会添加、移除或重组什么?

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means | 中文 |
|---|---|---|---|
| CAIS | "Center for AI Safety" | Non-profit; four-risk framework; 2023 extinction statement | CAIS：非营利，四风险框架 |
| CAISI | "US government AI safety" | NIST Center; voluntary agreements; unclassified evals | CAISI：NIST 中心，自愿协议 |
| Four-risk framework | "CAIS's taxonomy" | malicious use, AI races, organizational risks, rogue AIs | 四风险框架：恶意使用/AI 竞赛/组织风险/失控 AI |
| Malicious use | "Bad actor uses AI" | Bioweapons, disinformation, cyberattacks | 恶意使用：生物武器、虚假信息、网络攻击 |
| AI races | "Competitive pressure" | Labs/companies/nations push deployment past safety | AI 竞赛：竞争压力推动部署越过安全 |
| Organizational risk | "Lab internal failure" | Safety culture, audit, defenses, infosec | 组织风险：安全文化、审计、防御、信息安全 |
| Rogue AI | "Misaligned agent" | Capable AI pursuing goals conflicting with human welfare | 失控 AI：追求冲突目标的强大 AI |
| California SB-53 | "State-level regulation" | 2025–2026 bill; first US state catastrophic-risk regulation if signed | 加州 SB-53：州级灾难性风险监管法案 |

## Xem thêm 延伸阅读

- [Center for AI Safety](https://safe.ai/) tổ chức nhà của khung bốn rủi ro.
  Trung ngữ翻译:四风险框架的机构之家
- [CAIS — AI Risks that Could Lead to Catastrophe](https://safe.ai/ai-risk) giấy có 4 rủi ro.
  Trung ngữ翻译:四风险论文
- [CAIS — May 2023 statement on extinction risk](https://safe.ai/statement-on-ai-risk) tuyên bố chung ngắn gọn.
  Trung ngữ翻译:简短联合声明
- [NIST CAISI](https://www.nist.gov/caisi) Trung tâm công nghệ thông minh và đổi mới đối diện với chính phủ.
  Trung ngữ翻译:面向政府的AI标准和创新中心
- [Anthropic — Measuring agent autonomy in practice](https://www.anthropic.com/research/measuring-agent-autonomy) kết nối các cam kết ở cấp độ phòng thí nghiệm với việc định hình quy mô xã hội.
  Trung語翻译:连接实验室级承诺与社会规模框架
