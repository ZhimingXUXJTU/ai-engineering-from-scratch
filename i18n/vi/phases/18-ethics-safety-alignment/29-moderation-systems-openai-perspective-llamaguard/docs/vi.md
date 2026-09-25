# Hệ thống kiểm soát  OpenAI, Perspective, Llama Guard  Llama Guard Perspective  kiểm tra OpenAI

> Hệ thống kiểm soát sản xuất hoạt động các chính sách an toàn được định nghĩa trong Bài học 12-16. OpenAI Moderation API: `omni-moderation-latest`(2024) dựa trên GPT-4o phân loại văn bản + hình ảnh trong một cuộc gọi; 42% tốt hơn trên bộ thử nghiệm đa ngôn ngữ so với phiên bản trước đó; sơ đồ phản hồi trả lại 13 loại booleans  quấy rối, quấy rối/cảnh đe dọa, thù hận, thù hận/cảnh đe, bất hợp pháp, bất hợp pháp/ bạo lực, tự gây hại, tự gây hại/cố định, tự gây hại/sự hướng dẫn, tình dục, tình dục/chỉ thiếu niên, bạo lực, bạo lực/phic; miễn phí cho hầu hết các nhà phát triển. Các mô hình lớp: Tự trì nhập (tự tạo), Tự trì sản xuất (tự tạo sau), Tự trì tùy chỉnh (quản lý miền). Các cuộc gọi song song đồng bộ ẩn độ trễ; các phản ứng giữ vị trí trên cờ. Llama Guard 3/4 (Dạy học 16): 14 nguy cơ MLCommons, Quá lạm dụng thông dịch mã, 8 ngôn ngữ (v3), nhiều hình ảnh (v4). API viễn cảnh (Google Jigsaw): điểm độc tính trước sóng LLM-as-moderator; chủ yếu độc tính một chiều với các biến thể độc tính nghiêm trọng / xúc phạm / nói xấu; cơ sở cho nghiên cứu về độ kiểm duyệt nội dung. Sự suy giảm: Moderator Nội dung Azure đã hết hạn vào tháng 2 năm 2024, nghỉ hưu vào tháng 2 năm 2027, thay thế bởi Azure AI Content Safety.

> **【中文解读】**本节介绍内容审核系统OpenAI Perspective、Llama Guard等内容安全工具──OpenAI Moderation API(omni-moderation-last, 2024) dựa trên GPT-4o, trong đơn次调用中分类文本+图像, trả lại 13 个类别布尔值──三层模式是 2026 年默认配置:输入审核(预生成)、输出审核(后生成)、自定义审核(域规则)──

> **【拓展：审核栈 → 生产配置】**OpenAI và Llama Guard có "không hợp pháp" như một loại rộng rãi, Llama Guard phân chia cho "giá phạm bạo lực" và "giá phạm không bạo lực"── triển khai theo chiến lược phân loại pháp luật thích hợp lựa chọn──Tầm nhìn API của Google Jigsaw) là một trong những hệ thống đánh giá độc hại trước thời đại LLM, vẫn được sử dụng rộng rãi trong nghiên cứu kiểm tra nội dung vì có nhiều năm qua định kỳ dữ liệu──Azure Content Moderator 2024 tháng 2 tháng 2 từ bỏ, tháng 2 năm 2027 trở lại, chuyển đến Azure AI Content Safety──

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, three-layer moderation harness) | **语言:** Python（标准库，三层审核框架）
**Prerequisites:** Phase 18 · 16 (Llama Guard / Garak / PyRIT) | **前置知识:** Phase 18 · 16 (Llama Guard / Garak / PyRIT)
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**学本节前请先掌握:Phase 18·16(红队工具) 』内容审核 = Đặt 12-16 课的安全政策操作化的产品层──
>  **【类比】**审核系统 = "AI 服务台的保安"。OpenAI Moderation API(GPT-4o 驱动) = 一次调用分类 13 类(骚扰/仇恨/非法/自残/性/暴力等);Llama Guard 3/4(14 MLCommons 类别,多模态);Perspective API(Google Jigsaw,毒性打分,LLM 前的旧时代)。
>  三层默认配置:输入审核(pre-gen) + 输出审核(post-gen) + 自定义审核(域规则) ――异步并行调用来藏延迟──

## Mục tiêu học tập

- Mô tả phân loại phân loại của OpenAI Moderation API và cách nó khác với bộ MLCommons của Llama Guard 3.
- Mô tả ba mô hình lớp độ trung bình (input, output, custom) và đặt tên một chế độ thất bại của mỗi.
- Mô tả vị trí của API Perspective như là một đường cơ sở trước thời đại LLM và lý do tại sao nó vẫn được sử dụng trong nghiên cứu.
- Cung cấp thời gian khấu trừ Azure.

> Mô tả các phân loại của OpenAI Moderation API và sự khác biệt của nó với Llama Guard 3 MLCommons 集. Mô tả mô hình kiểm tra ba cấp và mô hình thất bại của mỗi cấp. Mô tả API viễn cảnh như vị trí của LLM.

## Vấn đề  vấn đề

Bài học 12-16 mô tả các cuộc tấn công và công cụ phòng thủ. Bài học 29 bao gồm các hệ thống điều hòa được triển khai để hoạt động các hệ thống phòng thủ ở bề mặt mà người dùng chạm vào sản phẩm.

> Bài học 12-16  mô tả các công cụ tấn công và phòng thủ. Bài học 29 bao gồm các hệ thống kiểm tra đã được triển khai để điều hành phòng thủ.

## Khái niệm

> **【中文解读】**13 个类别:骚扰/骚扰-威胁、仇恨/仇恨-威胁、自残/自残意图/自残指示、性/性-未成年人、暴力/暴力图形、非法/非法-暴力──多模态支持适用于暴力、自残和性但不包括性-未成年人,其余仅仅文本──比上一代审核端点多语言测试集上 42%好──

### OpenAI Moderation API

`omni-moderation-latest`(2024). Được xây dựng trên GPT-4o. Định dạng văn bản + hình ảnh trong một cuộc gọi. miễn phí cho hầu hết các nhà phát triển.

Các loại (13 boolean trong sơ đồ phản ứng):
- Trẻ em, quấy rối/cảnh đe dọa
- thù hận, thù hận/cảnh đe dọa
- tự gây hại, tự gây hại/cố định, tự gây hại/sự hướng dẫn
- tình dục, tình dục/từ tuổi thơ
- bạo lực, bạo lực/phần đồ họa
- bất hợp pháp, bất hợp pháp/ bạo lực

Nỗ trợ đa phương tiện áp dụng cho `violence`- `self-harm`, và`sexual`Nhưng không`sexual/minors`Phần còn lại chỉ dùng văn bản.

Để có mã trong `code/main.py`Chúng ta sẽ phá hủy `/threatening`- `/intent`- `/instructions`, và`/graphic`Các bộ phận phụ thuộc vào các bậc cha mẹ cấp cao của họ để đơn giản hóa giáo dục.

42% tốt hơn trong tập hợp thử nghiệm đa ngôn ngữ so với điểm cuối độ trung bình thế hệ trước đó.

### Llama Guard 3/4

Được bao gồm trong Bài học 16. 14 MLCommons các danh mục nguy hiểm (được tổ chức khác với 13 biểu hiện-chương trình boolean của OpenAI). hỗ trợ 8 ngôn ngữ (v3). Llama Guard 4 (ngày 4 tháng 4 năm 2025) là đa phương thức, 12B.

Các phân loại OpenAI và Llama Guard chồng chéo nhưng khác nhau. OpenAI có "không hợp pháp" như một loại rộng; Llama Guard có "quá phạm bạo lực" và "quá phạm không bạo lực" riêng biệt.

### API Perspective (Google Jigsaw)

Hệ thống điểm độc tính trước sóng LLM-as-moderator (trước năm 2020). Các loại: TOXICITY, SEVERE_TOXICITY, INSULT, PROFANITY, THREAT, IDENTITY_ATTACK. Điểm chính một chiều (TOXICITY) với biến thể tiểu chiều.

Được sử dụng rộng rãi như một cơ sở nghiên cứu về kiểm duyệt nội dung vì API ổn định, được ghi chép và có dữ liệu hiệu chuẩn hàng năm. Đối với các trường hợp sử dụng LLM gần đó, Llama Guard hoặc OpenAI Moderation thường phù hợp hơn.

> **【中文解读】**Logi thiết kế của mô hình kiểm toán ba tầng: nhập kiểm toán phải được hoàn thành trước khi tạo, xuất kiểm toán phải được hoàn thành sau khi tạo.

### Mô hình ba lớp

1. **Input moderation.**Đánh phân loại lệnh yêu cầu của người dùng trước khi tạo. Từ chối nếu được đánh dấu. Trễ: một cuộc gọi phân loại.
2. **Output moderation.**Đánh phân loại đầu ra của mô hình trước khi giao hàng. Thay thế bằng từ chối nếu được đánh dấu. Trễ: một cuộc gọi phân loại sau mỗi thế hệ.
3. **Custom moderation.**Các quy tắc cụ thể về miền (regex, allowlists, chính sách kinh doanh).

Ba lớp này theo thiết kế là liên tục: độ trung bình đầu vào phải hoàn thành trước khi tạo ra, và độ trung bình đầu ra chạy sau khi tạo ra. Sự song song áp dụng trong một lớp  chạy nhiều trình phân loại (ví dụ, OpenAI Moderation + Llama Guard + Perspective) đồng thời trên cùng một văn bản che giấu độ trễ mỗi trình phân loại. Là một tối ưu hóa tùy chọn, một phản ứng giữ vị trí ("một khoảnh khắc, kiểm tra...") có thể được hiển thị trong khi độ kiểm soát đầu vào hoàn thành và lưu lượng token-1 được hoãn lại. Hành vi cờ có thể cấu hình: từ chối, khử trùng, leo thang đến kiểm tra của con người.

> **【拓展：失败模式 → 为什么需要多层】**仅输入审核无法捕获输出幻觉(Lớp 12-14 编码攻击绕过输入分类器);仅输出审核允许任何输入到达模型(增加成本,向攻击者暴露内部推理);仅自定义审核不跨类别鲁棒(正则表达式脆弱) ――分层是默认安全带+吊带――

### Các chế độ thất bại

- **Input only.**Không bắt được ảo giác đầu ra (Dạy học 12-14 mã hóa các cuộc tấn công bỏ qua các phân loại đầu vào).
- **Output only.**Cho phép bất kỳ đầu vào nào đến mô hình; tăng chi phí; làm cho lý luận nội bộ cho kẻ tấn công.
- **Custom only.**Không mạnh mẽ trong các loại; Regexes là mỏng manh.

Layered là mặc định.

### Sự giảm giá Azure

Moderator Nội dung Azure: đã hết hạn vào tháng 2 năm 2024, nghỉ hưu vào tháng 2 năm 2027. Được thay thế bởi Azure AI Content Safety, dựa trên LLM và tích hợp với Azure OpenAI.

### Khi điều này phù hợp với giai đoạn 18

Bài học 16 bao gồm các công cụ kiểm duyệt trong bối cảnh đội đỏ. Bài học 29 bao gồm kiểm duyệt triển khai. Bài học 30 kết thúc với bằng chứng khả năng sử dụng kép hiện tại.

> Bài học 16 trong bối cảnh đội đỏ bao gồm các công cụ kiểm tra. Bài học 29 bao gồm kiểm tra đã được triển khai. Bài học 30 以当前双重用途能力证证末.

> **【拓展：Azure 迁移 → 2024-2027 行业项目】**Azure Content Moderator 2024 năm 2 tháng 2 từ bỏ, năm 2 tháng 2 đã bị loại bỏ, thay thế cho Azure AI Content Safety dựa trên LLM và được tích hợp với Azure OpenAI. Việc di chuyển là một dự án cấp ngành trong giai đoạn 2024-2027.

## Sử dụng nó.
```figure
an-moderation-layers
```

## Sử dụng nó

`code/main.py`xây dựng một vòng kiểm soát ba lớp: bộ điều chỉnh đầu vào (từ khóa + điểm số hạng mục), bộ điều chỉnh đầu ra (những phân loại tương tự trên đầu ra), bộ điều chỉnh tùy chỉnh (quyền hạn miền). Bạn có thể chạy đầu vào thông qua và quan sát lớp nào bắt được cái gì.

> `code/main.py`构建三层审核框架:输入审核器"",输出审核器"",自定义审核器"", bạn có thể vận hành输入并观察哪一层捕获什么――

Bài học này sẽ mang lại kết quả `outputs/skill-moderation-stack.md`- Với một triển khai, nó khuyến cáo cấu hình dung lượng độ kiểm duyệt: phân loại nào ở đầu vào, nào ở đầu ra, những quy tắc tùy chỉnh nào và những phán xét nào cho các trường hợp cạnh.

> 本课产 出 `outputs/skill-moderation-stack.md`❖ Đề xuất, đề xuất kiểm tra  quy định

## Tập luyện bài tập

1. Đi chạy`code/main.py`- Đưa vào một lớp tốt, biên giới và gây hại qua cả ba lớp.

2. Tăng vòng xoáy bằng cách ghi điểm độc tính theo kiểu Perspective-API cho một loại cụ thể. So sánh hành vi ngưỡng của nó với điểm hạng mục.

3. Đọc các tài liệu API OpenAI Moderation và danh sách danh mục Llama Guard 3. Chét mỗi danh mục OpenAI đến các danh mục Llama Guard gần nhất.

4. Thiết kế một bộ sưu tập điều chỉnh cho việc triển khai trợ lý mã (ví dụ, GitHub Copilot). Xác định các loại có liên quan nhất và ít nhất và đề xuất các quy tắc tùy chỉnh.

5. Azure Content Moderator sẽ nghỉ hưu vào tháng 2 năm 2027.

## Từ khóa  Keyword

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| OpenAI Moderation | "omni-moderation-latest" | GPT-4o-based 13-category (text) classifier with partial multimodal support |
| Perspective API | "Google Jigsaw toxicity" | Pre-LLM-era toxicity scoring baseline |
| Llama Guard | "MLCommons 14-category" | Meta's hazard classifier (v3: 8B text, 8 langs; v4: 12B multimodal) |
| Input moderation | "pre-generation filter" | Classifier on user prompt before model call |
| Output moderation | "post-generation filter" | Classifier on model output before delivery |
| Custom moderation | "domain rules" | Deployment-specific rules (regex, allowlist, policy) |
| Layered moderation | "all three layers" | Standard production deployment pattern |

## Xem thêm 延伸阅读

- [OpenAI Moderation API docs](https://platform.openai.com/docs/api-reference/moderations) Điểm cuối của sự ôn hòa
- [Meta PurpleLlama + Llama Guard](https://github.com/meta-llama/PurpleLlama) Llama Guard repo
- [Google Jigsaw Perspective API](https://perspectiveapi.com/) Điểm số độc tính
- [Azure AI Content Safety](https://learn.microsoft.com/en-us/azure/ai-services/content-safety/) Thay thế Azure
