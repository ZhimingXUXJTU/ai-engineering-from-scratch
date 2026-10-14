# Các chế độ thất bại: Tại sao các đại lý bị phá vỡ

> MASFT (Berkeley, 2025) liệt kê 14 chế độ thất bại đa đại lý trong 3 loại. Taxonomy của Microsoft ghi lại cách các lỗi AI hiện có tăng cường trong cài đặt đại lý. Dữ liệu lĩnh vực công nghiệp hội tụ về năm chế độ lặp lại: hành động ảo giác, trượt phạm vi, sai lầm hàng loạt, mất ngữ cảnh, lạm dụng công cụ.

**Type:** Learn + Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 05 (Self-Refine and CRITIC), Phase 14 · 24 (Observability) | **前置知识:** 见原文
**Time:** ~60 minutes | **时间:** 见原文

>  **【前置】**Học本节前请先掌握:Phase 14·05(Tự tinh chỉnh / CRITIC)  hiểu đơn vị Thuốc tự mình纠错的局限;Phase 14·24(Observability) 本节假设你已经能使用OpenTelemetry 看完整的痕迹──本节教你**识别 trace 中的失败模式**, là giai đoạn 14·29 ((Thời gian chạy sản xuất) của tiền đợt.

> 🤔 **【困惑】**Q: Tại sao Agent  thất bại hơn so với phần mềm truyền thống thất bại khó phát hiện hơn? A: Bởi vì Agent  thất bại là "software failure"代码没崩、API 没返回错误, nhưng Agent dùng các công cụ sai lầm调用、错误参数、错误顺序"成功完成" nhiệm vụ.

## Mục tiêu học tập

- Đặt tên ba loại thất bại của MASFT và ít nhất bốn chế độ cụ thể trong mỗi.
- Giải thích tại sao sự thất bại của nhân viên làm tăng cường các chế độ thất bại AI hiện có (chính hướng, ảo giác).
- Mô tả năm chế độ lặp lại trong ngành và giảm thiểu chúng.
- Thực hiện một máy dò stdlib mà thẻ chất liệu theo dõi với các nhãn chế độ thất bại.

## Vấn đề  vấn đề giới thiệu

Các nhóm vận chuyển các đại lý làm việc trên 90% các dấu vết. 10% lỗi không phải là tiếng ồn ngẫu nhiên  chúng rơi vào một số nhỏ các loại lặp lại. Một khi bạn có thể đặt tên cho chúng, bạn có thể theo dõi chúng và sửa chữa chúng.

>  Nhóm phát hành của Agent trong 90% theo dõi hoạt động bình thường. 10% thất bại không phải là tiếng ồn ngẫu nhiên. Chúng thuộc một số ít các loại xuất hiện lặp lại. Một khi bạn có thể đặt tên chúng, bạn có thể giám sát và sửa chữa chúng.


> **【中文解读】**Mô hình thất bại của một đại lý khác với phần mềm thông thường: 1) 级联失败 một sai lầm quyết định触发后续一系列错误; 2) 目标漂移Agent trong chuỗi dài thực hiện chuyển hướng từ mục tiêu ban đầu; 3) 过度自信Agent在错误结果上编制成功故事――理解这些模式是构建可靠的代理的前提――

> **{【拓展：2025-2026 年的 Agent 事故报告揭示了系统性失败模式。典型案例如下：(1) 编码 Ag...】}**Báo cáo tai nạn của Agent trong năm 2025-2026 tiết lộ mô hình thất bại hệ thống. Các trường hợp điển hình như: 1) 编码 Agent sửa đổi các tài liệu không liên quan dẫn đến sụp đổ hệ thống; 2) nghiên cứu Agent trong giai đoạn 15 bắt đầu thảo luận về vấn đề về triết học; 3) 客服 Agent nói với người dùng về thành công của hoạt động nhưng thực tế không thực hiện;

>  **【类比】**5 nguyên nhân điển hình của một đại lý: 1)**幻觉动作**=看错导航开错路;(2) **范围蔓延**= Đáng lẽ mua菜 đã đến khu vực lân cận;**级联错误**=小擦后慌乱撞墙;(4) **上下文丢失**= quên đi từ đâu ra đi;(5) **工具误用**=把油门当车. 每种失败有应对防御:导航验证、明确终点、紧急停车按、定期回顾、工具白名单──

> ️ **【易错点】**Trưởng phòng 3 个坑:**只看最终输出**Agent tự tin nói " hoàn thành ", nhưng trong giai đoạn trung gian toàn bộ lỗi;务必看完整的痕迹,不仅看结尾() 的输出──(2) **不设失败预算** cùng một sai lầm连续重试 20 次烧光预算; dùng max_retries=3 + 失败计计器──(3) **没做意图验证**Công viên quyết định" xóa file X", nhưng X là /etc/passwd;高危操作必须用户二次确认 + 路径白名单。

## Khái niệm cốt lõi

### MASFT (Berkeley, arXiv:2503.13657)

Các loại này có thể phân biệt đáng tin cậy.

> Các mô hình thất bại của đại lý bao gồm:级联失败 (một sai lầm truyền đến nhiều người) 幻觉成功 (một sai lầm) 循环爆炸 (một vòng lặp không giới hạn hoặc một lần nữa hoạt động) 信任边界崩──

Tầm quan trọng: các lỗi là những lỗi thiết kế cơ bản trong các hệ thống đa đại lý, chứ không phải là những hạn chế LLM để sửa chữa bằng các mô hình cơ bản tốt hơn.

> 核心主张: thất bại là một thiếu sót thiết kế cơ bản của nhiều đại lý 系统, không phải là có thể sửa chữa các hạn chế LLM thông qua mô hình cơ bản tốt hơn.

> Các mô hình thất bại của đại lý bao gồm:级联失败 (một sai lầm truyền đến nhiều người) 幻觉成功 (một sai lầm) 循环爆炸 (một vòng lặp không giới hạn hoặc một lần nữa hoạt động) 信任边界崩──

### Microsoft Taxonomy của chế độ thất bại trong các hệ thống AI đại lý

- Những thất bại AI hiện có (chính hướng, ảo giác, rò rỉ dữ liệu) tăng cường trong các thiết lập cơ quan.
- Những thất bại mới xuất hiện từ tự trị: hành động không dự định trên quy mô, lạm dụng công cụ, trôi dạt nhiệm vụ.
- Báo trắng là sổ đăng ký rủi ro cho các sản phẩm đại lý.

### Characterizing Faults in Agentic AI (arXiv:2603.06847)

- Những thất bại phát sinh từ sự dàn xếp, sự tiến hóa của trạng thái nội bộ và sự tương tác của môi trường.
- Không chỉ là "định dạng xấu" hay "mô hình xấu xuất phát".

### LLM Agent Hallucinations Survey (arXiv:2509.18970)

Hai biểu hiện chính:

1. **Instruction-following Deviation** Đại lý không theo lệnh hệ thống.
2. **Long-range Contextual Misuse** đại lý quên hoặc áp dụng sai ngữ cảnh từ lượt trước.

Hầm lẫn dự định: Tránh (giải hành vi bị bỏ qua), Tháo phí (giải hành vi lặp lại), Tránh (giải hành hành vi không hợp lệ).

> Các mô hình thất bại của đại lý bao gồm:级联失败 (một sai lầm truyền đến nhiều người) 幻觉成功 (một sai lầm) 循环爆炸 (một vòng lặp không giới hạn hoặc một lần nữa hoạt động) 信任边界崩──

### Năm chế độ lặp lại trong ngành

Các phân tích trường Arize, Galileo, NimbleBrain 2024-2026 hội tụ về:

> Các mô hình thất bại của đại lý bao gồm:级联失败 (một sai lầm truyền đến nhiều người) 幻觉成功 (một sai lầm) 循环爆炸 (một vòng lặp không giới hạn hoặc một lần nữa hoạt động) 信任边界崩──

1. **Hallucinated actions.**Trưởng lý gọi một công cụ không tồn tại hoặc chế tạo ra những lập luận.
2. **Scope creep.**Trưởng lý mở rộng nhiệm vụ vượt ra ngoài yêu cầu của người dùng (tạo thêm PR, gửi thêm email).
3. **Cascading errors.**Một cuộc gọi sai tạo ra các hiệu ứng dòng chảy sau. Một ảo giác SKU ảo tạo ra bốn cuộc gọi API.
4. **Context loss.**Các nhiệm vụ dài hạn quên đi những hạn chế quay sớm.
5. **Tool misuse.**gọi công cụ đúng với các lập luận sai, hoặc công cụ sai hoàn toàn.

Các đại lý không thể phân biệt "Tôi thất bại" và "các nhiệm vụ là không thể" và thường ảo giác một thông điệp thành công trên 400 lỗi để đóng vòng lặp.

> 级联是最致命的──Agent 无法区分"I failed"和"任务不可能完成", thường xuyên trong 400 错误上幻觉出一个成功消息来关闭循环──

> Các mô hình thất bại của đại lý bao gồm:级联失败 (một sai lầm truyền đến nhiều người) 幻觉成功 (một sai lầm) 循环爆炸 (một vòng lặp không giới hạn hoặc một lần nữa hoạt động) 信任边界崩──

### Giảm thiểu: cổng ở mỗi bước

Các cổng xác minh tự động tại mọi bước của chuỗi lý luận, kiểm tra cơ sở thực tế đối với tình trạng môi trường.

> Các mô hình thất bại của đại lý bao gồm:级联失败 (một sai lầm truyền đến nhiều người) 幻觉成功 (một sai lầm) 循环爆炸 (một vòng lặp không giới hạn hoặc một lần nữa hoạt động) 信任边界崩──

- Định dạng an toàn từng bước (Học 21).
- Truy hiệu hóa lập luận gọi công cụ (Dạy 06).
- Kiểm tra nội dung được lấy lại với các sự kiện được biết (Dạy học 05, CRITIC).
- Khám phá ảo giác thành công bằng cách kiểm tra lại trạng thái (tệp thực sự được tạo ra không?).

### Khi việc giám sát thất bại đi sai

- **Tagging only crashes.**Hầu hết các lỗi của đại lý đều tạo ra hiệu quả.
- **No baseline.**Việc phát hiện sự biến động cần một điều tốt nhất; nếu không có nó bạn không thể nói "điều này đang trở nên tồi tệ hơn".
- **Over-alerting.**Mỗi thất bại tạo ra một trang, nhóm và giới hạn tốc độ.

> **仅标记崩溃。**Đại đa số đại lý  thất bại tạo ra trông có hiệu quả xuất khẩu ∙ cần kiểm tra nội dung ∙
> **没有基线。**漂移检测 cần một trạng thái tốt cuối cùng được biết đến; không có nó bạn không thể nói "đây đang biến mất"
> **过度告警。**Mỗi lần thất bại đều có một trang.

## Hãy xây dựng nó.
```figure
failure-cascade
```

## Hãy xây dựng nó

`code/main.py`thực hiện một stdlib mode failure tagger:

> Các mô hình thất bại của đại lý bao gồm:级联失败 (một sai lầm truyền đến nhiều người) 幻觉成功 (một sai lầm) 循环爆炸 (một vòng lặp không giới hạn hoặc một lần nữa hoạt động) 信任边界崩──

- Một bộ dữ liệu theo dõi tổng hợp bao gồm năm chế độ.
- Các chức năng phát hiện theo chế độ (chương thức ký hiệu trên các cuộc gọi công cụ, đầu ra, các hành động lặp lại).
- Một thẻ đánh dấu từng dấu vết và báo cáo phân phối chế độ.

Đi đi.

```
python3 code/main.py
```

Kết quả: nhãn theo dõi + phân phối tổng thể, tái tạo giá rẻ của những gì bề mặt tập hợp dấu vết của Phoenix.

> 输出: mỗi theo dõi标签 + 聚合分布,Phoenix  theo dõi聚类所显示内容的廉价复现――

> Các mô hình thất bại của đại lý bao gồm:级联失败 (một sai lầm truyền đến nhiều người) 幻觉成功 (một sai lầm) 循环爆炸 (một vòng lặp không giới hạn hoặc một lần nữa hoạt động) 信任边界崩──

## Hãy sử dụng nó để thực hiện

- **Phoenix**cho việc phân nhóm sản xuất (Lớp 24).
- **Langfuse**cho việc chơi lại phiên + ghi chú.
- **Custom**cho các chữ ký cụ thể về miền mà nền tảng quan sát của bạn không thể phát hiện.

## Chuyển nó đi.

`outputs/skill-failure-detector.md`tạo ra các máy dò chế độ thất bại phù hợp với miền của bạn, được kết nối với một cửa hàng theo dõi.

> `outputs/skill-failure-detector.md`Tạo ra một bộ kiểm tra mô hình thất bại trong lĩnh vực của bạn, kết nối lưu trữ theo dõi.

> Các mô hình thất bại của đại lý bao gồm:级联失败 (một sai lầm truyền đến nhiều người) 幻觉成功 (một sai lầm) 循环爆炸 (một vòng lặp không giới hạn hoặc một lần nữa hoạt động) 信任边界崩──

## Tập luyện bài tập

1. Thêm một bộ phát hiện cho "hạt giác thành công": đại lý trả lại thành công nhưng trạng thái mục tiêu không thay đổi.
  Trung ngữ翻译:思考并实践此练习。
2. Đánh dấu 100 dấu vết thực sự từ một sản phẩm mà bạn đã xây dựng.
  Trung ngữ翻译:思考并实践此练习。
3. Thực hiện một số liệu "đường kính thủy triều": do sự thất bại ở bước N, nó ảnh hưởng đến bao nhiêu bước hạ lưu?
  Trung ngữ翻译:思考并实践此练习。
4. Hãy đọc 14 chế độ thất bại của MASFT, chọn 3 chế độ áp dụng cho sản phẩm của bạn, viết các máy dò.
  Trung ngữ翻译:思考并实践此练习。
5. Đưa một bộ dò vào một công việc CI: thất bại khi xây dựng nếu >=5% các dấu vết gắn thẻ một chế độ.
  Trung ngữ翻译:思考并实践此练习。

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| MASFT | "Multi-agent failure taxonomy" | Berkeley 14-mode categorization |  |
| Cascading error | "Ripple failure" | One early mistake propagates through N steps |  |
| Context loss | "Forgot the constraint" | Long-horizon turn drops early-turn facts |  |
| Tool misuse | "Wrong tool / wrong args" | Valid call, wrong invocation |  |
| Success hallucination | "Faked completion" | Agent claims success on a 400; state unchanged |  |
| Scope creep | "Overreach" | Agent does more than asked |  |
| Instruction-following deviation | "Disobedience" | Ignores system prompt or user constraint |  |
| Sub-intention errors | "Plan bugs" | Omission, redundancy, disorder in plan execution |  |

## Xem thêm 延伸阅读

- [Cemri et al., MASFT (arXiv:2503.13657)](https://arxiv.org/abs/2503.13657) 14 chế độ thất bại, 3 loại
  Trung ngữ: 翻译:见原文.
- [Microsoft, Taxonomy of Failure Mode in Agentic AI Systems](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/final/en-us/microsoft-brand/documents/Taxonomy-of-Failure-Mode-in-Agentic-AI-Systems-Whitepaper.pdf) Đăng ký rủi ro
  Trung ngữ: 翻译:见原文.
- [Arize Phoenix](https://docs.arize.com/phoenix) Nhóm phân phối lở trong thực tế
  Trung ngữ: 翻译:见原文.
- [Anthropic, Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) khi các mô hình đơn giản hơn tránh các chế độ hoàn toàn
  Trung ngữ: 翻译:见原文.
