# Cảnh sát Langfuse, Phoenix, Opik

> Ba nền tảng quan sát đối tượng nguồn mở thống trị năm 2026. Langfuse (MIT)  6M+ cài đặt / tháng, theo dõi + quản lý nhanh chóng + đánh giá + lặp lại phiên. Arize Phoenix (Elastic 2.0)  đánh giá sâu cụ thể đối với các đối tượng, sự liên quan RAG, OpenInference tự động dụng cụ. Comet Opik (Apache 2.0)  tối ưu hóa nhanh chóng tự động, guardrails, phát hiện ảo giác của thẩm phán LLM.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 23 (OTel GenAI) | **前置知识:** 见原文
**Time:** ~45 minutes | **时间:** 见原文

## Mục tiêu học tập

- Hãy cho tên ba nền tảng quan sát các đại lý nguồn mở hàng đầu và giấy phép của họ.
- Nhận ra những gì mỗi người là mạnh nhất: Langfuse (giữa họp mgmt + nhanh), Phoenix (RAG + tự động dụng cụ), Opik (tích cực + guardrails).
- Giải thích tại sao 89% các tổ chức báo cáo có khả năng quan sát các chất tác nhân vào năm 2026.
- Thực hiện một đường ống dẫn trace-to-dashboard với đánh giá của thẩm phán LLM.

## Vấn đề  vấn đề giới thiệu

OTel GenAI (Dạy 23) cung cấp cho bạn sơ đồ. Bạn vẫn cần nền tảng hấp thụ khoảng thời gian, chạy đánh giá, lưu trữ phiên bản nhanh và làm trượt các sự lùi. Ba đối thủ đều nhấn mạnh các phần khác nhau của chu kỳ cuộc sống.

> OTel GenAI (第 23 课) đã cho bạn một kế hoạch. Bạn vẫn cần một nền tảng để nhận thời gian, hoạt động đánh giá, lưu trữ và hiển thị trở lại.

>  **【前置】**Học本节前请先掌握:Phase 14·23(OTel GenAI Convention) 本节是把上一节的方案落到具体平台上,不知道 `invoke_agent`(Phase 14·05(Tự tinh tế/CRITIC)  hiểu LLM như một thẩm phán bản chất là mô hình CRITIC, nếu không bạn sẽ coi thẩm phán là "một LLM khác 调用" chứ không phải "đánh giá thực tế dựa trên bằng chứng bên ngoài"


> **【中文解读】**Cơ sở thực hiện của người dùng: Track (tracking) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (Center) (

## Khái niệm cốt lõi

### Langfuse (MIT)

>  **【类比】**三个观测平台像三种医院信息系统的分工:**Langfuse**là tổng hợp bệnh viện HIS(住院、门诊、药房全打通tracing+prompt 管理+eval 一站式, nhấn mạnh"you changed提示版本 v3 后,第三天崩的痕迹都能分到这个版本");**Phoenix**là chuyên ngành kiểm tra trung tâm ((( chuyên ngành RAG 检索质量、行为漂移聚类, vết cluster 能告诉你" tuần này Hành vi của Đại lý và tuần trước không giống như "nhưng không quan tâm bạn đã thay đổi bất kỳ lời khuyên nào);**Opik**Đây là hệ thống quản lý thử nghiệm lâm sàng.

- 6M+ SDK cài đặt / tháng, 19k+ GitHub sao.
- Tính năng: theo dõi, quản lý nhanh chóng với phiên bản + sân chơi, đánh giá (LLM-as-judge, phản hồi của người dùng, tùy chỉnh), phiên bản thay thế.
- Tháng 6 năm 2025: trước đây là các mô-đun thương mại (LLM-as-a-judge, hàng lưu ý, thí nghiệm nhanh chóng, sân chơi) nguồn mở dưới MIT.
- Nguyệt nhất cho: khả năng quan sát kết thúc với vòng quản lý nhanh chặt chẽ.

### Arize Phoenix (Lí thư 2.0)

- Đánh giá chuyên sâu hơn về các tác nhân: phân nhóm dấu vết, phát hiện bất thường, liên quan đến việc lấy lại cho RAG.
- Native OpenInference tự động dụng cụ.
- Các cặp với quản lý Arize AX cho sản xuất.
- Không có phiên bản nhanh  được định vị như một công cụ chuyển hướng/hành vi-hệch giảm cùng với các nền tảng rộng hơn.
- Nguyệt nhất cho: sự liên quan RAG, biến động hành vi, phát hiện bất thường.

### Sao chổi Opik (Apache 2.0)

- Tự động tối ưu hóa nhanh thông qua thử nghiệm A / B.
- Các đường dây bảo vệ (đánh dấu PII, hạn chế hiện tại).
- Đánh giá chứng ảo giác.
- Điểm chuẩn từ đo lường của Comet: Các bản ghi Opik + đánh giá trong 23.44s so với Langfuse 327.15s (~ 14x khoảng cách)  lấy các điểm chuẩn của nhà cung cấp như là hướng dẫn.
- Nguyệt nhất cho: vòng tối ưu hóa, thử nghiệm tự động, thực thi thám.

### Dữ liệu ngành công nghiệp

Theo Maxim (2026 phân tích thực địa): 89% các tổ chức có khả năng quan sát các đại lý; vấn đề chất lượng là rào cản sản xuất hàng đầu (32% người được hỏi trích dẫn chúng).

> Cơ sở hoạt động của đại lý có thể theo dõi, theo dõi, kiểm soát và điều chỉnh các công cụ.

### Chọn một

| Need | Pick |
|------|------|
| All-in-one with prompt management | Langfuse |
| Deep RAG evaluation + drift | Phoenix |
| Automated optimization + guardrails | Opik |
| Open licensing, no ELv2 | Langfuse (MIT) or Opik (Apache 2.0) |
| Datadog / New Relic integration | Any — they all export OTel |

### Khi mô hình này đi sai

> 🤔 **【困惑】**Q: 89% tổ chức đều nói mình có đại lý có thể quan sát được, nhưng vì sao tai nạn vẫn còn? A: 多数团队 chỉ làm" kết nối OTel → trace 进入 Langfuse" bước này, giống như lắp đặt một tấm ảnh giám sát nhưng không ai nhìn.

- **No eval strategy.**Việc theo dõi mà không có đánh giá chỉ là việc khai thác gỗ đắt tiền.
- **Self-rolled LLM-judge without grounding.**Mô hình CRITIC (Dạy học 05) áp dụng  các thẩm phán cần các công cụ bên ngoài để xác minh thực tế.
- **Prompt versions not tied to traces.**Khi sự phản ứng giảm, bạn không thể phân chia cho sự thúc đẩy đã gây ra nó.

> **没有评估策略。**Không có đánh giá, chỉ có một cuốn nhật ký đắt tiền.
> **自建的 LLM 评审器没有基础。**模式 (第 5 课) 适用评审器需要外部工具进行事实核查──
> **提示版本未与追踪关联。**Khi sản xuất trở lại, bạn không thể định vị để dẫn đến vấn đề.

## Hãy xây dựng nó.

> ️ **【易错点】**场景:团队把OTel trace 接到 Langfuse 后,写个 LLM- thẩm phán 给每条 trace 打 1-5分, nhưng rubric chỉ có một câu" trả lời rất tốt không tốt" → 后果:分数 vô nghĩa, thẩm phán  把"礼貌但答错"打 5分"",正确但简短"打 2分,dashboard 上 95% 满意度但客户投诉暴 → 修复: rubric 必须分维维度(事实正确度, phạm vi tuân thủ,音调), mỗi维度的失败定义 (((就是" phạm vi tuân thủ: đại lý có thể không làm được yêu cầu của người dùng không không"),且配 50-100条 标签 nhân tạo làm cơ sở  准备为何强调 "phenix                                                                                                                                                                 
```figure
wb-trace-ingest
```

## Hãy xây dựng nó

`code/main.py`thực hiện một bộ sưu tập dấu vết stdlib + thẩm phán đánh giá LLM:

> Cơ sở hoạt động của đại lý có thể theo dõi, theo dõi, kiểm soát và điều chỉnh các công cụ.

- Giống các con giọt hình GenAI.
- Nhóm theo phiên, thẻ không chạy (các chuyến đi bảo vệ, đánh giá low-trust).
- Một thẩm phán LLM có kịch bản ghi điểm phản ứng của đại lý trên một rubric.
- Một bản tóm tắt giống như bảng điều khiển: tỷ lệ thất bại, lý do thất bại hàng đầu, phân phối điểm đánh giá.

Đi đi.

```
python3 code/main.py
```

Kết quả: điểm đánh giá mỗi phiên và phân loại thất bại phù hợp với những gì Langfuse / Phoenix / Opik sẽ hiển thị.

> 输出: mỗi buổi họp phân tích đánh giá và thất bại phân loại, phù hợp Langfuse/Phoenix/Opik 会显示内容──

> Cơ sở hoạt động của đại lý có thể theo dõi, theo dõi, kiểm soát và điều chỉnh các công cụ.

## Hãy sử dụng nó để thực hiện

- **Langfuse**tự lưu trữ hoặc đám mây; dây thông qua OTel hoặc SDK của họ.
- **Arize Phoenix**tự lưu trữ; tự động công cụ OpenInference.
- **Comet Opik**tự lưu trữ hoặc đám mây; vòng tối ưu hóa tự động.
- **Datadog LLM Observability**cho các đội hỗn hợp + ML đã chạy Datadog.

## Chuyển nó đi.

`outputs/skill-obs-platform-wiring.md`chọn một nền tảng và dẫn các dấu vết + đánh giá + phiên bản nhanh vào một đại lý hiện có.

> `outputs/skill-obs-platform-wiring.md`选择一个平台,并将追踪 + 评估 + 提示版本接入现有代理──

> Cơ sở hoạt động của đại lý có thể theo dõi, theo dõi, kiểm soát và điều chỉnh các công cụ.

## Tập luyện bài tập

1. Xuất khẩu một tuần các dấu vết OTel sang đám mây Langfuse.
  Trung ngữ翻译:思考并实践此练习。
2. Viết một chương trình thẩm phán LLM cho lĩnh vực của bạn (sự chính xác thực tế, âm thanh, tuân thủ phạm vi).
  Trung ngữ翻译:思考并实践此练习。
3. So sánh phiên bản Langfuse với tập hợp dấu vết của Phoenix.
  Trung ngữ翻译:思考并实践此练习。
4. Đọc hồ sơ của Opik, đưa một tấm dây bảo vệ thông tin thông tin thông tin cho một trong những người làm việc của anh.
  Trung ngữ翻译:思考并实践此练习。
5. Hãy đánh giá điểm số của 3 người trong cơ thể của bạn, bỏ qua số lượng được công bố bởi nhà cung cấp, đo lường số của bạn.
  Trung ngữ翻译:思考并实践此练习。

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| Tracing | "Spans collector" | Ingest OTel / SDK spans; index by session |  |
| Prompt management | "Prompt CMS" | Versioned prompts tied to traces |  |
| LLM-as-judge | "Automated eval" | Separate LLM scores agent output against a rubric |  |
| Session replay | "Trace playback" | Step through past runs for debugging |  |
| RAG relevancy | "Retrieval quality" | Does the retrieved context match the query |  |
| Trace clustering | "Behavioral grouping" | Cluster similar runs for drift detection |  |
| Guardrail enforcement | "Policy at log time" | PII/toxicity/scope checks on logged content |  |

## Xem thêm 延伸阅读

- [Langfuse docs](https://langfuse.com/) theo dõi, đánh giá, nhanh chóng
  Trung ngữ: 翻译:见原文.
- [Arize Phoenix docs](https://docs.arize.com/phoenix) tự động dụng cụ, trôi
  Trung ngữ: 翻译:见原文.
- [Comet Opik](https://www.comet.com/site/products/opik/) tối ưu hóa + tháp bảo vệ
  Trung ngữ: 翻译:见原文.
- [OpenTelemetry GenAI semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/) các kế hoạch cả ba tiêu thụ
  Trung ngữ: 翻译:见原文.
