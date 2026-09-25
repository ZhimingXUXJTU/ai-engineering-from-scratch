# Theo quy định SOC 2, HIPAA, GDPR, PCI-DSS, EU AI Act, ISO 42001 合规 行动 欧盟 PR

> Bảo hiểm đa khung là những cổ phần bàn cho các giao dịch doanh nghiệp năm 2026. **EU AI Act**: có hiệu lực từ ngày 1 tháng 8 năm 2024. Hầu hết các yêu cầu rủi ro cao được thực thi ngày 2 tháng 8 năm 2026. Hình phạt lên đến 15 triệu euro hoặc 3% doanh thu hàng năm toàn cầu cho các nghĩa vụ hệ thống rủi ro cao (Công nghệ 99(4)); lên đến 35 triệu euro hoặc 7% cho các thực hành AI bị cấm (Công nghệ 99(3)).**Colorado AI Act**: có hiệu lực từ ngày 30 tháng 6 năm 2026 (đã trì hoãn từ tháng 2 năm 2026 bởi SB25B-004)  đánh giá tác động cho các hệ thống có rủi ro cao, quyền kháng cáo quyết định AI. Virginia tương tự cho tín dụng / việc làm / nhà ở / giáo dục. **SOC 2 Type II**: yêu cầu thực tế về AI B2B (Typ II, không phải Type I, cho fintech). **GDPR**: tiền phạt lớn nhất được ghi nhận về AI là 30,5 triệu euro đối với Clearview AI (DPA Hà Lan, tháng 9 năm 2024); Garante của Ý đã phát hành 15 triệu euro đối với OpenAI vào tháng 12 năm 2024 (sau đó bị đảo ngược khi kháng cáo vào tháng 3 năm 2026). Việc chỉnh sửa PII theo thời gian thực là tiêu chuẩn có thể bảo vệ; thanh lọc sau khi xử lý không đủ. **HIPAA**: chăm sóc sức khỏe bị ràng buộc không thể gửi PHI đến các dịch vụ AI bên ngoài mà không có BAA. **PCI-DSS**: Cụ thể của AI-interaction layer đòi hỏi cấu hình + thỏa thuận hợp đồng, không phải tự động. **ISO 42001**: tiêu chuẩn quản lý AI mới nổi, nhu cầu mua sắm ngày càng tăng cùng với ISO 27001. hồ sơ tham chiếu: OpenAI duy trì SOC 2 Type 2, ISO/IEC 27001:2022, ISO/IEC 27701:2019, GDPR/CCPA/HIPAA (BAA) / FERPA, PCI-DSS cho các thành phần thanh toán ChatGPT. Khép đồ xuyên khung giảm mệt mỏi kiểm toán: kiểm soát truy cập bản đồ trên ISO 27001 A.5.15-5.18, GDPR Art. 32, HIPAA §164.312(a).

> **【中文解读】**Bài viết này giới thiệu khuôn khổ hợp pháp LLM  dịch vụ cần đáp ứng các quy định và yêu cầu hợp pháp.


**Type:** Learn | **类型:** 学习
**Languages:** (Python optional — compliance is policy + process, not code) | **语言:** Python
**Prerequisites:** Phase 17 · 25 (Security), Phase 17 · 13 (Observability) | **前置知识:** Phase 17 · 25 (Security), Phase 17 · 13 (Observability)

>  **【前置】**学本节前请先掌握:Phase 17·25(安全) 、Phase 17·13(可观测性) ⋅多框架合规 = 2026 企业单的桌面注。
>  **【类比】**合规框架 = "AI 公司的驾照"――EU AI Act(2024.8 生效,2026.8 高风险全执行) = 欧盟驾照,罚款最高营业额 7%;SOC 2 Type II = B2B必备(fintech 必须 Type II);GDPR = 隐私(Clearview AI 被罚30,5M €);HIPAA = 医疗(无A 不能传 PHI);BAPCI-DSS = 支付;ISO 42001 = 新AI 治理──跨框架映射减审负担(访问控制在ISO/GDPR/HIPAA通用) ;;OpenAI 是参考图像:HIPAC 2 Type 2 + ISO 27001/27701 + GDPR/CCPA/PAABAA) /PCI-SSD-(((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((
> ️ **【易错点】**Thực时 PII 脱敏是底线,后处理清洗不够(已被GDPR 罚款)
**Time:** ~60 minutes | **时间:** ~60 minutes

## Mục tiêu học tập

- Đặt danh sách bảy khung năm 2026 liên quan đến các sản phẩm LLM và phù hợp với từng phân khúc khách hàng.
  Trung ngữ翻译:列举 2026 年与LLM 产品相关的七个框架,并将每个匹配到客户细分――
- Citing thời gian thực thi của EU AI Act (nhu cầu có hiệu lực tháng 8 năm 2024; thực thi rủi ro cao tháng 8 năm 2026) và giới hạn phạt hai cấp (€ 15M / 3% đối với các nghĩa vụ rủi ro cao, € 35M / 7% đối với các hoạt động bị cấm).
  Trung văn翻译:引用 EU AI Act 执法时间表(2024 年 8 月生效;高风险执法 2026 年 8 月) ⋅
- Giải thích tại sao việc làm sạch PII sau khi xử lý không đủ cho GDPR và đặt tên biên dịch lớp suy luận thời gian thực như tiêu chuẩn đáng bảo vệ.
  Trung ngữ翻译:解释为什么后处理 PII 清理对GDPR不够,并说出实时推理层的替代方案──
- Mô tả bản đồ kiểm soát xuyên khung (ví dụ: bản đồ kiểm soát truy cập ISO 27001 A.5.15-5.18 + GDPR Art. 32 + HIPAA §164.312(a)).
  Trung文翻译:描述跨框架控制映射 (如访问控制映射到ISO 27001 A.5.15-5.18 + SOC 2 CC6 + HIPAA 安全规则)

## Vấn đề  vấn đề giới thiệu

> **【中文解读】**多框架覆盖是2026年企业交易的入场券──企业客户的采购要求SOC 2 Type II、GDPR、HIPAA BAA、ISO 27001 和"EU AI Act 合规声明"──这是不是LLM特有问题是企业SaaS 问题加上LLM 特定叠层──采购团队2026年想要一个矩阵(框架×控制),而不是一个PDF──

> **【拓展：EU AI Act 关键时间线】**Luật AI của EU 关键时间线:(1) 2024 年 8 月 1 日生效;(2) 2025 年 2 月 2 日 cấm AI 实践条款执行;(3) 2026 年 8 月 2 日高风险系统条款执行(合规评估,文档、日志);(4) 2027 年 8 月受协调立法约束产品中的高风险系统;;罚款:高风险系统违规最高15M €或全球年营业额3%(Art. 994);;禁止 AI 实践最高35M €或7%(Art. 993));;

Nhóm mua sắm của khách hàng doanh nghiệp yêu cầu SOC 2 Type II, GDPR, HIPAA BAA, ISO 27001, và "Báo cáo tuân thủ Luật AI EU". Nhóm của bạn có SOC 2 Type I. Bạn đã sáu tháng từ Type II và chưa bắt đầu ghi lại Điều 30 GDPR.

Bảo hiểm đa khung không phải là vấn đề LLM  đó là vấn đề Enterprise-SaaS, với các lớp phủ cụ thể của LLM. Các nhóm mua sắm vào năm 2026 muốn một matrix với một hàng trên mỗi khung và một cột trên mỗi điều khiển, không phải là một PDF.

## Khái niệm cốt lõi

### Bảy khung

> **【拓展：2026 年 LLM 合规框架全景】**Các sản phẩm LLM cần phải quan tâm đến bảy quy định: 1) SOC 2 Type IIB2B SaaS 基线,Type II  yêu cầu 6-12 个月的操作控制审计; 2) HIPAA美国医疗,BAA不可选,PHI không thể được gửi đến AI bên ngoài không có BAA; 3) GDPREU người dùng,实时推理层脱敏是 2026年防范标准,最大 AI 相关罚款 €30.5M; 4) PCI-DSS支付数据,AI 触及支付需要配置+合同;(5) EU AI Act服务 EU用户,高风险系统 2026年 8月执行,罚款 €35M/7%;6) Colorado Act26 年 6月 30日生效,影响诉权;((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((

| Framework | Scope | LLM-specific requirement |
|-----------|-------|--------------------------|
| SOC 2 Type II | B2B SaaS baseline | Process controls audited over 6-12 months |
| HIPAA | US healthcare | BAA required; PHI cannot leave infrastructure without signed agreement |
| GDPR | EU users | Real-time PII redaction; data subject rights; Article 30 records |
| PCI-DSS | Payment data | Configuration + contracts for AI touching payment |
| EU AI Act | Serving EU users | Risk tier classification; high-risk systems: conformity assessment, documentation, logging |
| Colorado AI Act | Serving CO residents | Impact assessments; right to appeal |
| ISO 42001 | AI governance | Emerging; pairs with ISO 27001 |

### Thời gian của EU AI Act

- Ngày 1 tháng 8 năm 2024: có hiệu lực.
- Ngày 2 tháng 2 năm 2025: thực thi các hoạt động AI bị cấm.
- Ngày 2 tháng 8 năm 2026: các hệ thống rủi ro cao được thực thi (phác định phù hợp, tài liệu, ghi chép).
- Tháng 8 năm 2027: hệ thống rủi ro cao trong sản phẩm theo luật pháp hài hòa.

Các cấp rủi ro: Không thể chấp nhận được (được cấm), rủi ro cao (sự tuân thủ + ghi chép), rủi ro hạn chế (tự minh bạch), rủi ro tối thiểu (không có ràng buộc). Hầu hết các dịch vụ SaaS LLM B2B có rủi ro hạn chế; rủi ro cao được đưa vào việc làm, tín dụng, giáo dục, thực thi pháp luật, di cư, dịch vụ thiết yếu.

Cồi thường (Công Điều 99): lên đến 15 triệu euro hoặc 3% doanh thu hàng năm toàn cầu cho vi phạm các nghĩa vụ hệ thống có rủi ro cao (Công Điều 99(4); lên đến 35 triệu euro hoặc 7% cho các hoạt động AI bị cấm (Công Điều 99(3)); tùy thuộc vào mức cao hơn.

### GDPR  biên tập thời gian thực là tiêu chuẩn

> **【中文解读】**Lớp lý luận thực tế thời điểm nhạy cảm của GDPR là tiêu chuẩn phòng thủ năm 2026  sau xử lý giải quyết  LLM  xem dữ liệu  sau khi bị nhạy cảm) không thể phòng thủ  mô hình đã nhìn thấy dữ liệu  đúng thực hành: LLM 调用前的实体识别 + 一致性标记化(Mesh 方法) giữ ngữ义 + 仅存脱敏提示 + người dùng đồng ý opt-in 原始数据 最大 AI 相关 GDPR 罚款:Clearview AI €30.5M  Hà Lan DPA, 2024 9 月);最大 LLM 相关罚款:AI 开放 €15M  Italy Garante, 2024 12 月, 2026 年 3 月上诉后推翻) 

Việc làm sạch sau khi xử lý (tạo lại PII sau khi LLM thấy nó) không phải là một tư thế có thể bảo vệ  mô hình đã thấy dữ liệu.

- Việc công nhận thực thể trước khi gọi LLM.
- Đánh dấu liên tục (chương trình Mesh) bảo tồn ngữ nghĩa.
- Cung cấp chỉ các yêu cầu đã sửa đổi + đồng ý chọn vào nguyên liệu.

Việc thực thi gần đây: 30,5 triệu euro chống lại Clearview AI (DPA Hà Lan, tháng 9 năm 2024) là khoản phạt GDPR cụ thể nhất về AI được ghi chép cho đến nay; 15 triệu euro chống lại OpenAI (Garante của Ý, tháng 12 năm 2024) là khoản phạt cụ thể nhất về LLM, mặc dù nó đã bị đảo ngược khi kháng cáo vào tháng 3 năm 2026 và phán quyết vẫn đang được xem xét thêm.

### HIPAA  BAA không phải là tùy chọn

Bạn không thể gửi PHI đến các dịch vụ AI bên ngoài mà không có thỏa thuận liên kết kinh doanh được ký kết. Cả ba nền tảng LLM hyperscaler (Bedrock, Azure OpenAI, Vertex) đều cung cấp BAA. OpenAI trực tiếp API cung cấp BAA. Anthropic trực tiếp API cung cấp BAA.

### SOC 2 loại II

Loại I: các thiết kế và tài liệu điều khiển.
Loại II: các kiểm soát hoạt động hiệu quả trong 6-12 tháng.

Việc mua sắm B2B vào năm 2026 không được tính theo loại II. loại I là khởi động; loại II là cổng.

Các yếu tố điều tra phổ biến: nhật ký truy cập (người đã thấy cái gì), quản lý thay đổi (làm thế nào nó được triển khai), đánh giá rủi ro (tứ ba), phản ứng với sự cố (được thử nghiệm).

### Phân tích khung chéo

> **【拓展：跨框架映射降低审计疲劳】**跨框架控制映射是减少审计疲劳的关键. Một chiến lược kiểm soát truy cập có thể đáp ứng yêu cầu kiểm soát của nhiều khung đồng thời: 32 + HIPAA §164.312(a);变更管理 → ISO 27001 A.8.32 + PCI DSS Req. 6 + HIPAA 违规通知范围;传输加密 → ISO 27001 A.8.24 + GDPR Art. 32 + HIPAA §164.312(e);密钥管理 → ISO 27001 A.8.19 + PCI DSS Req. 8 + SOC 2 CC6.1──合规自动化工具(Drata、Vanta、Secureframe) có thể tự động hóa bản đồ này बड़े पैमाने部署时值投资──OpenAI's reference合规档案(SOC 2 Type 2 + ISO 27001 + ISO 27701 + GDPR/CCPA/HIPAA/FERPA + PCI-DSS) 大致是2026年企业入场标准──

Một chính sách kiểm soát truy cập đáp ứng nhiều kiểm soát khung:

| Control | Frameworks |
|---------|-----------|
| Access logging | ISO 27001 A.5.15-5.18, GDPR Art. 32, HIPAA §164.312(a) |
| Change management | ISO 27001 A.8.32, PCI DSS Req. 6, HIPAA breach-notification scope |
| Encryption in transit | ISO 27001 A.8.24, GDPR Art. 32, HIPAA §164.312(e) |
| Secrets management | ISO 27001 A.8.19, PCI DSS Req. 8, SOC 2 CC6.1 |

Các công cụ tuân thủ (Drata, Vanta, Secureframe) tự động hóa bản đồ này.

### ISO 42001  phát triển

Được công bố cuối năm 2023. Khóa quản lý AI bao gồm quản lý rủi ro, chất lượng dữ liệu, minh bạch, giám sát con người.

### Tương tự tham chiếu của OpenAI

OpenAI duy trì SOC 2 Type 2, ISO/IEC 27001:2022, ISO/IEC 27701:2019, GDPR/CCPA/HIPAA (BAA) / FERPA, PCI-DSS cho các thành phần thanh toán ChatGPT. Đó là khoảng phần cược của bảng doanh nghiệp vào năm 2026.

### Những con số mà bạn nên nhớ

- Các khoản phạt của EU AI Act: lên đến 15 triệu euro / 3% (các nghĩa vụ rủi ro cao, Điều 99(4)); lên đến 35 triệu euro / 7% (các hoạt động bị cấm, Điều 99(3)).
- Việc thực thi luật AI của EU có nguy cơ cao: ngày 2 tháng 8 năm 2026.
- Hình phạt GDPR lớn nhất được ghi nhận về AI: € 30,5M, Clearview AI (DPA Hà Lan, tháng 9 năm 2024).
- Hình phạt GDPR lớn nhất cụ thể cho LLM: 15 triệu euro, OpenAI (Giáo cáo Garante của Ý, tháng 12 năm 2024; bị hủy bỏ khi kháng cáo vào tháng 3 năm 2026).
- SOC 2 cửa sổ loại II: 6-12 tháng điều khiển hoạt động.
- Ngày hiệu lực của Đạo luật AI Colorado: 30 tháng 6 năm 2026 (đã bị hoãn từ tháng 2 năm 2026 bởi SB25B-004).

## Hãy sử dụng nó để thực hiện
```figure
i4-control-matrix
```

## Sử dụng nó

`code/main.py`là một bảng tính lập bản đồ tuân thủ trong Python  được kiểm soát, liệt kê các khung mà nó đáp ứng.

> `code/main.py`là một bảng tính lập bản đồ tuân thủ trong Python  được kiểm soát, liệt kê các khung mà nó đáp ứng.

## Chuyển nó đi.

Bài học này sẽ mang lại kết quả `outputs/skill-compliance-matrix.md`- Với phân khúc khách hàng và địa lý, xác định các khung và kiểm soát cần thiết.

> 本课产 出 `outputs/skill-compliance-matrix.md`- Với phân khúc khách hàng và địa lý, xác định các khung và kiểm soát cần thiết.

## Tập luyện bài tập

1. Khách hàng doanh nghiệp đầu tiên của bạn cần SOC 2 Type II, HIPAA BAA, EU AI Act tuyên bố.
   Trung文翻译:你的第一企业客户需要SOC 2 Type II、HIPAA BAA、EU AI Act 合规──按优先排序实现路线图──
2. Lớp xếp ba sản phẩm LLM giả định theo các cấp rủi ro của Đạo luật AI của EU.
   Trung ngữ翻译: Trong EU AI Act 风险等级下分类三个假设的 LLM 产品──高风险等级有什么变化?
3. Anh vô tình gửi PHI đến một nhà cung cấp mà không có BAA.
   Trung ngữ翻译:你不小心将 PHI 发送给没有BAA的提供商──走一遍事件响应流程──
4. Thảo luận liệu ISO 42001 là "cần thiết vào năm 2026" cho một nhà cung cấp AI trung bình thị trường.
   Trung ngữ翻译:论证 ISO 42001 在 2026 年对中等市场 AI供应商是否"必要"
5. Chế hoạch các lĩnh vực nhật ký kiểm toán LLM của bạn (Phase 17 · 25) cho ít nhất ba kiểm soát khung.

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| SOC 2 Type II | "audited controls" | Controls operating over 6-12 months, independently attested |
| HIPAA BAA | "healthcare contract" | Business Associate Agreement; required for PHI |
| GDPR | "EU privacy" | Real-time PII redaction is the defensible 2026 standard |
| EU AI Act | "EU AI rules" | High-risk enforcement August 2026; €15M / 3% (high-risk obligations) — €35M / 7% (prohibited practices) |
| Colorado AI Act | "US AI state law" | June 30, 2026 effective (delayed by SB25B-004); impact assessments |
| ISO 42001 | "AI governance" | Emerging framework for AI risk + transparency |
| ISO 27001 | "security ISMS" | Information Security Management System baseline |
| Conformity assessment | "EU AI doc package" | High-risk requirement: docs, testing, logging |
| Cross-framework mapping | "one control, many frames" | Single policy satisfies multiple framework controls |

## Xem thêm 延伸阅读

- [OpenAI Security and Privacy](https://openai.com/security-and-privacy/) hồ sơ tuân thủ tham chiếu.
- [GuardionAI — LLM Compliance 2026: ISO 42001, EU AI Act, SOC 2, GDPR](https://guardion.ai/blog/llm-compliance-guide-iso-42001-eu-ai-act-soc2-gdpr-2026)
- [Dsalta — SOC 2 Type 2 Audit Guide 2026: 10 AI Controls](https://www.dsalta.com/resources/ai-compliance/soc-2-type-2-audit-guide-2026-10-ai-powered-controls-every-saas-team-needs)
- [EU AI Act official text](https://eur-lex.europa.eu/eli/reg/2024/1689/oj) Nguồn chính.
- [Colorado AI Act](https://leg.colorado.gov/bills/sb24-205) Nguồn chính.
- [ISO/IEC 42001:2023](https://www.iso.org/standard/81230.html) Tiêu chuẩn hệ thống quản lý AI.
