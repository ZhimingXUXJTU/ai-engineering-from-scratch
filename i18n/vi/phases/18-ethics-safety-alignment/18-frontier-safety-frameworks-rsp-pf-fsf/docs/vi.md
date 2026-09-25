# Các khung an toàn biên giới  RSP, PF, FSF  framework                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             

> Ba khung phòng thí nghiệm chính xác định quản lý ngành công nghiệp của khả năng biên giới năm 2026. Chính sách quy mô chịu trách nhiệm nhân loại v3.0 (Thiáng Hai 2026) giới thiệu các mức độ an toàn AI cấp bậc (ASL-1 đến ASL-5+), được mô hình hóa dựa trên mức độ an toàn sinh học, với ASL-3 được kích hoạt vào tháng 5 năm 2025 cho các mô hình liên quan đến CBRN. OpenAI Preparedness Framework v2 ( Tháng 4 năm 2025) xác định năm tiêu chí cho khả năng theo dõi và tách ra các báo cáo khả năng từ báo cáo bảo vệ. DeepMind Frontier Safety Framework v3.0 (Tháng 9 năm 2025) giới thiệu các cấp độ khả năng quan trọng bao gồm một CCL thao tác độc hại mới. Cả ba hiện có các điều khoản điều chỉnh đối thủ cạnh tranh cho phép hoãn nếu các phòng thí nghiệm đồng nghiệp vận chuyển mà không có bảo vệ tương đương. Sự sắp xếp giữa các phòng thí nghiệm vẫn là cấu trúc, không phải là thuật ngữ: "Thỉ số khả năng", "Thỉ số khả năng cao" và "Thực lượng khả năng quan trọng" chỉ ra các cấu trúc tương tự.

> **【中文解读】**Bài viết này giới thiệu khung an toàn tiên phong RSP, OpenAI Preparedness, DeepMind FSF, và các khung an toàn khác đối với các mô hình khác.

> **【拓展：竞争调整条款 → 竞赛动态】**Tất cả ba khung đều bao gồm các điều khoản điều chỉnh cạnh tranh  cho phép vận chuyển thời gian trễ trong khi đối thủ cạnh tranh không có biện pháp bảo vệ có thể so sánh. Các nhà phê bình cho rằng điều này tạo ra nền tảng cạnh tranh: Nếu ba phòng thí nghiệm đều có đối thủ cạnh tranh vi phạm khi giảm yêu cầu, cân bằng chuyển hướng vi phạm.

**Type:** Learn | **类型:** 学习
**Languages:** none | **语言:** 无
**Prerequisites:** Phase 18 · 17 (WMDP), Phase 18 · 07-09 (deception failures) | **前置知识:** Phase 18 · 17 (WMDP), Phase 18 · 07-09 (欺骗失败)
**Time:** ~75 minutes | **时间:** ~75 分钟

>  **【前置】**学本节前请先掌握:Phase 18·17(WMDP) 、Phase 18·07-09(欺骗三角) ・・・三大前沿实验室安全框架横向对比(与Phase 15·19-20 互补) ・・・
>  **【类比】**Safety framework = "AI 实验室的生物安全等级"――Anthropic RSP v3.0(ASL-1 đến ASL-5+, tương tự như BSL 生物安全);OpenAI PF v2(5 跟踪能力+能力报告/保障报告分离);DeepMind FSF v3(关键能力等级+操纵 CCL)。ASL-3 已 2025.5 激利用于 CBRN。三家都加"竞争调整"条款若行无类似保障可暂缓──

## Mục tiêu học tập

- Mô tả cấu trúc cấp độ ASL của Anthropic và điều gì kích hoạt ASL-3.

> Mô tả cấu trúc cấp độ ASL của Anthropic và điều gì kích hoạt ASL-3:

- Tên gọi năm tiêu chí OpenAI Preparedness Framework v2 cho khả năng theo dõi.

> 列出 OpenAI Preparedness Framework v2  Capacity of Tracking's 5 tiêu chuẩn:

- Mô tả cấu trúc cấp độ khả năng quan trọng của DeepMind và CCL thao tác gây hại.

> Mô tả về khả năng quan trọng của DeepMind, cấu trúc và hoạt động có hại của CCL.

- Giải thích các điều khoản điều chỉnh đối thủ cạnh tranh và lý do tại sao chúng quan trọng đối với động lực chủng tộc.

> 解释 quy định về cạnh tranh và tác động đến động thái cạnh tranh.

- Định nghĩa một trường hợp an toàn và mô tả cấu trúc ba trụ (phòng dõi, không thể đọc, không thể đọc).

> 定义安全案例并描述三支柱结构(监控、不可读性、无能)

## Vấn đề  vấn đề

Bài học 7-17 thiết lập rằng lừa dối có thể xảy ra, khả năng sử dụng kép tồn tại, và đánh giá có giới hạn. Một phòng thí nghiệm có mô hình có khả năng biên giới cần một cấu trúc quản trị nội bộ:
- Định nghĩa ngưỡng khi cần có biện pháp bảo vệ mới.
- Định nghĩa các đánh giá cần thiết trước khi mở rộng quy mô.
- Mô tả một trường hợp an toàn trông như thế nào.
- Xử lý vấn đề động lực đua (nếu các đối thủ cạnh tranh vận chuyển mà không có bảo vệ, bạn làm gì?).

> Bài học 7-17 xác định lừa đảo là có thể, khả năng sử dụng hai lần tồn tại, đánh giá có hạn chế, phòng thí nghiệm có mô hình khả năng cạnh tranh cần cấu trúc quản lý nội bộ: xác định khi nào cần bảo đảm mới, mở rộng trước khi cần đánh giá, mô hình trường hợp an toàn, vấn đề động thái cạnh tranh.

Ba khung 2025-2026 là hiện đại  không hoàn hảo, phát triển và phù hợp đủ giữa các phòng thí nghiệm để câu hỏi quản trị bây giờ là liệu các khung có phù hợp không, chứ không phải liệu chúng có tồn tại hay không.

> Ba khung 2025-2026 là những kỹ thuật tiên tiến nhất không hoàn hảo, trong quá trình phát triển, qua phòng thí nghiệm đủ để phù hợp, vấn đề quản lý hiện tại là liệu khung có đủ hay không hay không có hay không.

## Khái niệm

> **【中文解读】** cấu trúc ASL của Anthropic RSP v3.0:ASL-1 非前沿模型;ASL-2 当前前前沿基线;ASL-3 大幅更高的灾难性滥用风险(CBRN),2025 年 5 月激活;ASL-4 AI R&D-2 跨越值(可自动化进入门级 AI 研究);ASL-5+ 高级 AI R&D(公开加速有效扩张);;v3.0 新增前沿安全路线图片(开修版) 季度风险报告(部分外部审查) 分 AI R&D 拆分为 R&D-2 和 R&D-4;;

### Chính sách quy mô chịu trách nhiệm nhân loại v3.0 (Tháng 2 năm 2026)

Cấu trúc ASL:
- ASL-1: không phải mô hình biên giới (được tổng hợp bằng cơ sở yếu hơn biên giới).
- ASL-2: đường cơ sở biên giới hiện tại; được triển khai với các biện pháp bảo vệ thông thường.
- ASL-3: nguy cơ lạm dụng thảm họa cao hơn đáng kể; khả năng liên quan đến CBRN. Được kích hoạt vào tháng 5 năm 2025.
- ASL-4: AI R&D-2 vượt ngưỡng; mô hình có thể tự động hóa nghiên cứu AI cấp độ nhập học.
- ASL-5+: mô hình nghiên cứu và phát triển AI tiên tiến, đẩy nhanh hiệu quả quy mô.

> ASL 结构:ASL-1 非前沿模型;ASL-2 当前前沿基线;ASL-3 大幅更高的灾难性滥用风险(CBRN),2025 年 5 月激活;ASL-4 AI R&D-2 跨越值;ASL-5+ 高级 AI R&D──

Tới trong v3.0:
- Bản đồ đường bộ an toàn biên giới (tự do trong hình thức được biên soạn).
- Báo cáo rủi ro (tứ ba năm, một số được xem xét bên ngoài).
- AI R&D được phân chia thành AI R&D-2 và AI R&D-4.
- Một khi AI R&D-4 đã được vượt qua, một trường hợp an toàn xác nhận là cần thiết, xác định rủi ro không phù hợp từ các mô hình theo đuổi mục tiêu không phù hợp.

> v3.0 新增:前沿安全路线图 (前沿安全路线图) 公開修订版) 季度风险报告 (季度风险报告) 部分外部审查) 、AI R&D 拆分为 R&D-2 和 R&D-4、R&D-4 跨越后需要肯定性安全案例──

> **【拓展：OpenAI PF v2 → 五项追踪标准】**5 tiêu chuẩn khả năng theo dõi của OpenAI: 1) hợp lý  tồn tại mô hình đe dọa hợp lý; 2) có thể đo lường được  kinh nghiệm đánh giá có thể; 3) nghiêm trọng  gây tổn thương lớn; 4) không có nguy cơ gia tăng ; 5) ngay lập tức hoặc không thể khắc phục  gây tổn thương nhanh chóng xảy ra hoặc không thể hủy bỏ;.

### OpenAI Preparedness Framework v2 (15 tháng 4 năm 2025)

Năm tiêu chí cho khả năng theo dõi:
- **Plausible.**Có một mô hình đe dọa hợp lý.
- **Measurable.**Đánh giá bằng chứng có thể.
- **Severe.**Hành vi gây ra rất lớn.
- **Net-new.**Không phải là một rủi ro đã tồn tại.
- **Instantaneous-or-irremediable.**Sự tổn thương xảy ra nhanh chóng hoặc không thể được khắc phục.

> 5 tiêu chuẩn về khả năng theo dõi: hợp lý, có thể đo lường, nghiêm trọng, mới, tức thời hoặc không thể khắc phục được.

Khả năng đáp ứng tất cả 5 được theo dõi.

> 满足所有五项的能力被追踪,其他不追踪──

Dấu trúc PF v2 khác:
- Các báo cáo về khả năng (các mô hình có thể làm gì) và báo cáo về bảo vệ (các kiểm soát nào tồn tại).
- Các đánh giá của nhóm tư vấn an toàn.
- Lãnh đạo chấp thuận; Ủy ban An toàn & An toàn của Hội đồng giám sát.
- "Thỏa khoản điều chỉnh": OpenAI có thể giảm yêu cầu nếu một tàu phòng thí nghiệm khác không có bảo vệ tương đương.

> PF v2 其他结构: phân tách năng lực báo cáo và bảo đảm báo cáo, kiểm tra nhóm tư vấn an ninh, phê duyệt của lãnh đạo, giám sát của Ủy ban an ninh của hội đồng quản trị, "调整条款"

### DeepMind Frontier Safety Framework v3.0 (Tháng 9 năm 2025)

Các cấp độ khả năng quan trọng (CCL) theo lĩnh vực:
- Tăng cường vũ khí sinh học
- Tăng cường mạng
- ML Tăng tốc R&D
- Phong thủ độc hại (mới trong v3.0): mô hình có thể thay đổi đáng kể niềm tin / hành vi trong bối cảnh rủi ro cao.

> 按领域关键能力级别(CCL): Biological weapons提升、网络提升、ML R&D 加速、有害操纵(v3.0 新增)

V2.0 (tháng 2 năm 2025) đã thêm một phần Khớp Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định Định

> V2.0 đã thêm phần lừa đảo đối với phần và ML R&D CCL cấp độ an ninh cao hơn.

### Định hướng giữa các phòng thí nghiệm

- "Thỉ số khả năng" nhân văn.
- DeepMind "Cấp độ khả năng quan trọng".
- OpenAI "Thỉ số khả năng cao".

> Nhân văn "Thỉ số khả năng"、Thực lượng khả năng quan trọng"",OpenAI"Thỉ số khả năng cao"──

Không có thuật ngữ tiêu chuẩn ngành. Dòng cấu trúc: ba cấp độ khả năng biên giới với các tiêu chí đánh giá được công bố.

> Không có tiêu chuẩn ngành thuật ngữ.

> **【中文解读】**Các trường hợp an toàn có thể gây ra những tổn thương liên quan không? Các trường hợp an toàn khác nhau đối với các trụ sở khác nhau:ASL-3 CBRN các trường hợp chủ yếu nhắm vào những người không có khả năng thông qua quên lãng), lừa đảo đối với tất cả đối với giám sát và không thể đọc được, nâng cao mạng đều liên quan.

### Các trường hợp an toàn

Một trường hợp an toàn là một lập luận bằng văn bản cho rằng một triển khai là an toàn theo các giả định tồi tệ nhất.

> Ví dụ: an ninh là văn bản, được triển khai trong tình huống tồi tệ nhất giả định có thể chấp nhận an ninh không.

- **Monitoring.**Chúng ta có thể phát hiện hành vi xấu nếu nó xảy ra không?
- **Illegibility.**Liệu mô hình không có khả năng thực hiện một kế hoạch liên kết để gây hại?
- **Incapability.**Có phải mô hình không có khả năng gây ra thiệt hại trong vấn đề?

> **监控：**Nếu có hành vi xấu, chúng ta có thể kiểm tra được không?**不可读性：**模型是否缺乏执行连贯伤害计划的能力?**无能：**模型是否缺乏能力造成相关伤害?

Các trường hợp an toàn khác nhau nhắm vào các trụ cột khác nhau. Đối với trường hợp ASL-3 CBRN, không thể (thông qua không học) là mục tiêu chính. Đối với sự sắp xếp lừa đảo, giám sát và không thể đọc được là mục tiêu. Đối với nâng cao mạng, cả ba đều có liên quan.

> Các trường hợp an ninh khác nhau đối với các trụ cột khác nhau: trường hợp ASL-3 CBRN chủ yếu đối với không năng lực (không có thông qua quên), gian lận đối với giám sát và không thể đọc được, nâng cao mạng đều liên quan.

### Vấn đề động lực chủng tộc

Các điều khoản điều chỉnh đối thủ cạnh tranh là gây tranh cãi. Các nhà phê bình cho rằng họ tạo ra một cuộc đua xuống đáy: nếu cả ba phòng thí nghiệm sẽ giảm yêu cầu khi một đối thủ cạnh tranh bị lỗi, sự cân bằng chuyển sang đào ngũ. Những người bảo vệ cho rằng thay thế (các biện pháp bảo vệ đơn phương) sẽ tạo ra kết quả tồi tệ hơn nếu phòng thí nghiệm đào ngũ ít ý thức về an toàn hơn.

> 竞争调整条款有争议──批评者认为它们创造竞争底: nếu ba phòng thí nghiệm đều có đối thủ cạnh tranh vi phạm khi giảm yêu cầu, cân bằng chuyển hướng vi phạm.

AISI của Anh, CAISI của Mỹ và Văn phòng AI của EU (Dạy 24) là đối tác quản trị bên ngoài.

> AISI UK, CAISI Mỹ và Văn phòng AI EU là quản lý bên ngoài đối phó với các phương pháp.

### Khi điều này phù hợp với giai đoạn 18

Bài học 17-18 là lớp đo lường và quản lý trên đỉnh của các phân tích lừa đảo và nhóm đỏ. Bài học 19-24 bao gồm phúc lợi, thiên vị, quyền riêng tư, đánh dấu nước và cấu trúc quy định. Bài học 28 vẽ bản đồ hệ sinh thái nghiên cứu (MATS, Redwood, Apollo, METR) hoạt động các đánh giá.

> Bài học 17-18 là các biện pháp đo lường và quản lý trên phân tích lừa đảo và đội đỏ. Bài học 19-24 bao gồm lợi ích, quan điểm, sự riêng tư, nước ấn và cấu trúc quản lý. Bài học 28 mô tả các hệ sinh thái nghiên cứu về đánh giá hoạt động.

> **【拓展：跨实验室对齐 → 结构性而非术语性】**三个框架在术语上不一致但结构上对齐:Anthropic "Capacity Thresholds" = DeepMind "Critical Capacity Levels" = OpenAI "High Capacity Thresholds"──三层前沿能力、发布评估标准、竞争调整条款结构趋同──英国AISI,美国CAISI和欧盟AI Office (Lớp 24) là quản lý bên ngoài đối với các phương pháp应对――实验室框架是自愿的;监管框架正在出现――

## Sử dụng nó.
```figure
al-asl-ladder
```

## Sử dụng nó

Không có mã cho bài học này. Đọc ba nguồn chính: RSP v3.0, PF v2, FSF v3.0. Hình ảnh cấu trúc cấp độ của mỗi phòng thí nghiệm với các lớp khác và xác định một ngưỡng mà mỗi phòng thí nghiệm xác định mà các phòng thí nghiệm khác không.

> 本课没有代码──阅读三个主要来源:RSP v3.0、PF v2、FSF v3.0──将每个实验室的层级结构映射到其他实验室,并识别每个实验室定义但其他没有一个值──

## Đưa nó lên mạng

Bài học này sẽ mang lại kết quả `outputs/skill-framework-diff.md`. Với một khung an toàn hoặc thông báo phát hành, nó so sánh các định nghĩa ngưỡng của khung, các đánh giá cần thiết và cấu trúc trường hợp an toàn với RSP v3.0, PF v2, FSF v3.0 và các khoảng trống chéo giữa các phòng thí nghiệm.

> 本课产 出 `outputs/skill-framework-diff.md` Đưa ra một khung hoặc thông báo về an ninh, định nghĩa giá trị của nó, đánh giá cần thiết và cấu trúc trường hợp an ninh so với RSP v3.0PF, v2 ▌FSF v3.0, đánh dấu khoảng cách giữa phòng thí nghiệm

## Tập luyện bài tập

1. Đọc RSP v3.0, PF v2 và FSF v3.0. Sẵn sàng biên soạn bảng về ngưỡng CBRN của mỗi phòng thí nghiệm, ngưỡng R&D AI của mỗi phòng thí nghiệm và đánh giá trước khi triển khai.

2. Điều khoản điều chỉnh đối thủ cạnh tranh được đưa ra trong cả ba khung (2025+).

3. Thiết kế một trường hợp an toàn cho một mô hình vượt qua ngưỡng R&D-4 AI của Anthropic.

4. FSF v3.0 của DeepMind giới thiệu một CCL thao tác gây hại. đề xuất ba phép đo kinh nghiệm cho thấy một mô hình đã vượt qua ngưỡng này.

5. Đọc "Các yếu tố chung của các chính sách an toàn AI biên giới" (2025) của METR. Hãy nêu tên ba sự hội tụ mạnh nhất giữa các phòng thí nghiệm và hai sự khác biệt lớn nhất.

## Từ khóa  Keyword

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| RSP | "Anthropic's framework" | Responsible Scaling Policy; ASL tiers; v3.0 February 2026 |
| PF | "OpenAI's framework" | Preparedness Framework; five criteria; v2 April 2025 |
| FSF | "DeepMind's framework" | Frontier Safety Framework; CCLs; v3.0 September 2025 |
| ASL-3 | "biosafety level 3-analog" | Anthropic tier for CBRN-relevant capabilities; activated May 2025 |
| CCL | "critical capability level" | DeepMind's threshold construct; per-domain |
| Safety case | "the formal argument" | Written argument that deployment is acceptably safe under worst-case U |
| Adjustment clause | "competitor defection allowance" | Framework provision for reducing requirements if competitors ship without comparable safeguards |

## Xem thêm 延伸阅读

- [Anthropic — Responsible Scaling Policy v3.0 (February 2026)](https://www.anthropic.com/responsible-scaling-policy) Các cấp ASL, lộ trình, phân chia R&D AI
- [OpenAI — Updating the Preparedness Framework (April 15, 2025)](https://openai.com/index/updating-our-preparedness-framework/)5 tiêu chí, điều khoản điều chỉnh
- [DeepMind — Strengthening our Frontier Safety Framework (September 2025)](https://deepmind.google/blog/strengthening-our-frontier-safety-framework/) CCL v3.0, Manipulation có hại
- [METR — Common Elements of Frontier AI Safety Policies (2025)](https://metr.org/blog/2025-03-26-common-elements-of-frontier-ai-safety-policies/) So sánh giữa các phòng thí nghiệm
