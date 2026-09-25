# Đội đỏ dụng cụ Garak, Llama Guard, Pyrit

> Ba công cụ sản xuất khung các đội đỏ 2026 xếp hàng. Llama Guard (Meta)  một bộ phân loại Llama-3.1-8B được điều chỉnh tốt trên 14 loại nguy cơ MLCommons; Llama Guard 4 năm 2025 là một bộ phân loại đa phương thức 12B được cắt từ Llama 4 Scout. Garak (NVIDIA)  Tấm mã mở của scanner lỗ hổng LLM với các thăm dò tĩnh, động và thích ứng cho ảo giác, rò rỉ dữ liệu, tiêm nhanh, độc tính và jailbreaks. PyRIT (Microsoft)  nhiều vòng đội đỏ chiến dịch với Crescendo, TAP, và chuỗi chuyển đổi tùy chỉnh cho khai thác sâu. Llama Guard 3 được ghi lại trong Meta's "Llama 3 Herd of Models" (arXiv:2407.21783); Llama Guard 3-1B-INT4 trong arXiv:2411.17713; kiến trúc thăm dò của Garak trong github.com/NVIDIA/garak. Những công cụ này là giao diện sản xuất năm 2026 giữa nghiên cứu nhóm đỏ (Dân học 12-15) và triển khai (Dân học 17+).

> **【中文解读】**Bài viết này giới thiệu phương pháp đánh giá an toàn của Red Team Testing hệ thống hóa, sử dụng các cuộc tấn công tự động phát hiện AI  hệ thống lỗ hổng.

> **【拓展：2026 红队技术栈 → 生产配置】**标准配置:Llama Guard 放在模型两侧(输入+输出),Garak 每晚运行回归测试,PyRIT dùng cho các hoạt động phát hành trước đây。Prompt-Guard-86M là một loại phân loại nhập hạng nhẹ của Meta, được sử dụng cùng với Llama Guard。TrustyAI sẽ tập hợp Garak và Llama Stack Shields để tiến hành đánh giá kết thúc。

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, tool-architecture simulator and Llama Guard-style classifier mock) | **语言:** Python（标准库，工具架构模拟器和 Llama Guard 风格分类器模拟）
**Prerequisites:** Phase 18 · 12-15 (jailbreaks and IPI) | **前置知识:** Phase 18 · 12-15 (越狱和 IPI)
**Time:** ~75 minutes | **时间:** ~75 分钟

>  **【前置】**学本节前请先掌握:Phase 18·12-15(越狱+IPI 全套) ⋅2026 红队工具三件套──
>  **【类比】**红队工具 = "AI 安全的透透测试套件"――Llama Guard(Meta) = 输入输出分类器(14 危险类别,类似Phase 15·18);Garak(NVIDIA) = 漏洞扫描器(静态+动态+自适应探针,覆盖幻觉/数据泄漏/越狱);PyRIT(Microsoft) = 多轮深度攻击编排(Crescendo/TAP/自定义链)。三件套是研究(12-15) 和部署(17+) 之间的工程界面──

## Mục tiêu học tập

- Mô tả vị trí của Llama Guard 3/4 trong đống an toàn: phân loại đầu vào, phân loại đầu ra hoặc cả hai.

> Mô tả Llama Guard 3/4 trong công nghệ an ninh  vị trí: nhập phân loại out phân loại  hoặc cả hai và có.

- Hãy nêu tên 14 loại nguy cơ MLCommons và chỉ ra một loại không rõ ràng (Việc lạm dụng thông dịch mã).

> 列出 14  MLCommons 危险类,并说明一个不明显的类 (không rõ ràng)

- Mô tả kiến trúc thăm dò của Garak: thăm dò, máy dò, dây đeo.

> 描述 Garak's探针架构:探针、检测器、线束──

- Mô tả cấu trúc chiến dịch nhiều lượt của PyRIT và cách nó kết hợp với các thăm dò Garak.

> Mô tả cấu trúc hoạt động đa vòng của PyRIT và cách nó kết hợp với Garak 探针组合──

## Vấn đề  vấn đề

Bài học 12-15 trình bày bề mặt tấn công. Việc triển khai sản xuất cần đánh giá lặp lại, có thể mở rộng. Ba công cụ thống trị năm 2026: Llama Guard (chính định phòng thủ), Garak (tài duyệt), PyRIT (các tổ chức chiến dịch). Mỗi mục tiêu là một lớp khác nhau của vòng đời đội đỏ.

> Bài học 12-15  trình bày mặt tấn công. Việc triển khai sản xuất cần có thể lặp lại. Có thể mở rộng.

## Khái niệm

> **【中文解读】**Llama Guard 3 là Llama-3.1-8B 模型微调到 MLCommons AILuminate 14 类别的输入/输出分类, hỗ trợ 8种语言。Llama Guard 3-1B-INT4 là quy mô bên cạnh biến体(440MB, di động CPU 约 30 token/s)。Llama Guard 4(4月2025 年) là 12B 原生多模态分类器, từ Llama 4 Scout 剪枝, thay thế trước đây 8B 文本和 11B 视觉分类器。

### Llama Guard (Meta)

Llama Guard 3 là một mô hình Llama-3.1-8B được điều chỉnh tốt để phân loại đầu vào / ra ngoài trên các loại MLCommons AILuminate 14:
- Hành vi bạo lực, tội phạm không bạo lực, liên quan đến tình dục, CSAM, sự sỉ nhục
- Tư vấn chuyên môn, quyền riêng tư, IP, vũ khí vô phân biệt, thù hận
- Tự tử/ngăn thương bản thân, nội dung tình dục, bầu cử, lạm dụng người giải thích mã

> Llama Guard 3 là Llama-3.1-8B mô hình, dành cho MLCommons AILuminate 14 个类进行输入/输出分类微调――支持 8种语言――

Hỗ trợ 8 ngôn ngữ. Sử dụng: đặt trước LLM (trình độ nhập), sau LLM (trình độ sản xuất), hoặc cả hai.

> Sử dụng cách: đặt LLM 之前(输入审核) 之后(输出审核) 或两者兼有──Llama Guard 3 作为单一模型处理两者──

Llama Guard 3-1B-INT4 (arXiv:2411.17713, 440MB, ~ 30 token / s trên CPU di động) là biến thể cạnh lượng tử.

> Llama Guard 3-1B-INT4 là quy mô bên cạnh biến体(440MB, di động CPU 约30 token/s)

Llama Guard 4 (ngày 4 tháng 4 năm 2025) là 12B, đa phương tiện, được cắt từ Llama 4 Scout. Nó thay thế cả văn bản 8B và tiền nhiệm tầm nhìn 11B bằng một trình phân loại hấp thụ văn bản + hình ảnh.

> Llama Guard 4(2025 年 4 月) là 12B 原生多模态分类器, từ Llama 4 Scout 剪枝, thay thế trước đây 8B 文本和 11B 视觉分类器。

> **【拓展：Garak 架构 → 探针/检测器/线束】**Garak có ba tầng cấu trúc: thám tử 幻觉、数据泄露、提示注入、毒性、越狱的攻击生成器,分为静态(固定提示)、动态(生成提示)、自适应(响应目标输出); kiểm tra器针对预期失败模式评分输出;线束管理 thám tử-检测器对,运行活动,生成报告――基于层评分(TBSA) thay thế二元通过/失败模型可以通过重度相同的级别 3但失败级别 5

### Garak (NVIDIA)

Bộ quét lỗ hổng nguồn mở.
- **Probes.**Các máy phát điện tấn công cho ảo giác, rò rỉ dữ liệu, tiêm nhanh, độc tính, jailbreak.
- **Detectors.**Kết quả kết quả với các chế độ thất bại dự kiến  độc, rò rỉ, jailbreak.
- **Harnesses.**Quản lý các cặp dò dò, chạy chiến dịch, tạo ra báo cáo.

> 开源漏洞扫描器.架构:探针. ️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️

TrustyAI tích hợp Garak với các tấm khiên Llama-Stack (Prompt-Guard-86M phân loại đầu vào, Llama-Guard-3-8B phân loại đầu ra) để đánh giá mục tiêu được bảo vệ từ đầu đến cuối. Điểm số dựa trên cấp (TBSA) thay thế pass / fail nhị phân.

> TrustyAI sẽ tập hợp Garak và Llama Stack Shields để tiến hành đánh giá.

### PyRIT (Microsoft)

Python Risk Identification Toolkit, nhiều chiến dịch của nhóm đỏ.
- **Converters.**Chuyển đổi một lời nhắc hạt giống  phrasing, mã hóa, dịch, role play.
- **Orchestrators.**Tiến hành chiến dịch: Crescendo (sự leo thang), TAP (các chi nhánh), RedTeaming (lòng tùy chỉnh).
- **Scoring.**LLM- như thẩm phán hoặc phân loại như thẩm phán.

> PyRIT là Python 风险识别工具包──多轮红队活动──核心组件:转换器:转换种子提示) 编排器:运行活动) 评分:LLM 或分类器评判)

PyRIT là người anh em họ nặng hơn của Garak. Garak chạy hàng ngàn tàu thăm dò quay một lần; PyRIT chạy các chiến dịch nhiều lượt sâu được thiết kế để phá vỡ các chế độ thất bại cụ thể.

> PyRIT là một chương trình hạng nặng của Garak. Garak vận hành hàng ngàn quả thám đơn vòng.

### - Đám

Đặt Llama Guard ở cả hai bên của mô hình. chạy Garak mỗi đêm để hồi phục. chạy PyRIT cho các chiến dịch trước khi phát hành. Đây là cấu hình mặc định 2026 cho hầu hết các triển khai sản xuất.

> Trong mô hình, hai bên đặt Llama Guard. Mỗi đêm vận hành Garak trở lại thử nghiệm.

> **【中文解读】**评估陷:评判身份 tất cả ba công cụ đều có thể sử dụng LLM 评判,评判校准驱动报告的ASR(Lớp 12), phải xác định đánh giá;探针过时Garak 探针随着模型修改和老化,自适应探针(PAIR 式) 比静态探针老化慢;Llama Guard 在良性内容上的误报率早期版本过标记政治和LGBTQ+ 内容,v3/v4 校准有改善但未按部署校准;;

### Các bẫy đánh giá

- **Judge identity.**Cả ba công cụ đều có thể sử dụng một thẩm phán LLM; các ổ đĩa hiệu chuẩn thẩm phán báo cáo ASR (Dạy 12.
- **Probe staleness.**Garak thám tử tuổi khi các mô hình được dán vào chúng. thám tử thích ứng (PAIR hình dạng) tuổi chậm hơn các thám tử tĩnh.
- **Llama Guard FPR on benign content.**Các phiên bản Llama Guard sớm có nội dung chính trị và LGBTQ +; Llama Guard 3/4 hiệu chuẩn được cải thiện nhưng không được hiệu chuẩn cho mỗi triển khai.

### Khi điều này phù hợp với giai đoạn 18

Bài học 12-15 là các gia đình tấn công. Bài học 16 là công cụ sản xuất. Bài học 17 (WMDP) là đánh giá khả năng sử dụng kép. Bài học 18 là các khung an toàn biên giới bao gồm các công cụ này trong một cấu trúc chính sách.

> Bài học 12-15 là tấn công gia đình. Bài học 16 là công cụ sản xuất. Bài học 17 là đánh giá khả năng sử dụng hai lần. Bài học 18 là bao gồm các công cụ này trong khuôn khổ an ninh phía trước trong cấu trúc chính sách.

> **【拓展：PyRIT → 多轮深度利用】**PyRIT(Microsoft) là một phần của Garak. Garak chạy hàng ngàn vòng dò đơn, PyRIT chạy nhằm phá vỡ các mô hình thất bại cụ thể của nhiều vòng sâu hoạt động.

## Sử dụng nó.
```figure
al-guard-stack
```

## Sử dụng nó

`code/main.py`xây dựng một bộ phân loại kiểu đồ chơi Llama Guard (từ khóa + tính năng ngữ nghĩa trên 14 loại), một vòng xoáy đồ chơi Garak (lòng dò dò), và một chuỗi chuyển đổi nhiều vòng kiểu PyRIT. Bạn có thể chạy ba công cụ chống lại một mục tiêu giả và quan sát các chữ ký bảo hiểm khác nhau.

> `code/main.py` cấu trúc đồ chơi Llama Guard 风格分类器、 đồ chơi Garak 线束和 PyRIT 风格多轮转换链── bạn có thể xem các mô hình mục tiêu vận hành ba công cụ并观察 các đặc điểm khác nhau bao phủ──

## Đưa nó lên mạng

Bài học này sẽ mang lại kết quả `outputs/skill-red-team-stack.md`Với mô tả triển khai, nó nêu tên những công cụ nào trong ba công cụ phù hợp, điều gì để cấu hình trong mỗi công cụ và thời gian quay trở nào để chạy.

> 本课产 出 `outputs/skill-red-team-stack.md` Định nghĩa về việc sử dụng, đặt tên cho những công cụ nào phù hợp, cho mỗi bộ phận, và cho những gì trở lại.

## Tập luyện bài tập

1. Đi chạy`code/main.py`So sánh tốc độ phát hiện của bộ phân loại kiểu Llama-Guard trên các cuộc tấn công một lần và nhiều lần.

2. Thực hiện một con tàu Garak mới: một yêu cầu gây hại mã hóa base64. đo được phát hiện của nó bằng bộ phân loại kiểu Llama-Guard.

3. Cải rộng chuỗi chuyển đổi kiểu PyRIT bằng một chuyển đổi "t dịch sang tiếng Pháp, sau đó phác thảo".

4. Đọc danh sách các danh mục nguy hiểm của Llama Guard 3. Xác định hai danh mục mà dữ liệu đào tạo thực tế sẽ tạo ra tỷ lệ dương tính sai cao đối với nội dung phát triển hợp pháp.

5. So sánh các nguyên tắc thiết kế của Garak và PyRIT. Phúc tụi việc triển khai nơi mỗi công cụ là công cụ phù hợp.

## Từ khóa  Keyword

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| Llama Guard | "the classifier" | Fine-tuned Llama-3.1-8B/4-12B safety classifier with 14 hazard categories |
| Garak | "the scanner" | NVIDIA open-source vulnerability scanner; probes, detectors, harnesses |
| PyRIT | "the campaign tool" | Microsoft multi-turn red-team orchestrator; converters, orchestrators, scoring |
| Prompt-Guard | "the small classifier" | Meta's 86M prompt-injection classifier, paired with Llama Guard |
| TBSA | "tier-based scoring" | Garak's tier-based pass/fail replacing binary outcomes |
| Converter chain | "paraphrase + encode + ..." | PyRIT composition primitive for building multi-step attacks |
| MLCommons hazard categories | "the 14 taxonomies" | Industry-standard taxonomy Llama Guard targets |

## Xem thêm 延伸阅读

- [Meta — Llama Guard 3 (in Llama 3 Herd paper, arXiv:2407.21783)](https://arxiv.org/abs/2407.21783) Bộ phân loại 8B
- [Meta — Llama Guard 3-1B-INT4 (arXiv:2411.17713)](https://arxiv.org/abs/2411.17713) Bộ phân loại di động định lượng
- [NVIDIA Garak — GitHub](https://github.com/NVIDIA/garak) bộ nhớ và tài liệu của máy quét
- [Microsoft PyRIT — GitHub](https://github.com/Azure/PyRIT) bộ công cụ chiến dịch
