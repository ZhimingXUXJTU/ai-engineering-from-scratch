# ASCII Nghệ thuật và hình ảnh jailbreaks

> Jiang, Xu, Niu, Xiang, Ramasubramanian, Li, Poovendran, "ArtPrompt: ASCII Art-based Jailbreak Attacks against Aligned LLMs" (ACL 2024, arXiv:2402.11753). Mùi các mã thông báo liên quan đến an toàn trong một yêu cầu có hại, thay thế chúng bằng các phiên bản nghệ thuật ASCII của cùng một chữ cái, và gửi lời yêu cầu che giấu. GPT-3.5, GPT-4, Gemini, Claude, Llama-2 đều không nhận ra các token nghệ thuật ASCII. Cuộc tấn công bỏ qua PPL (trình lọc phức tạp), phòng thủ Paraphrase và Retokenization. Liên quan: ViTC chuẩn đo nhận dạng các lời nhắc thị giác không nghĩa; StructuralSleight tổng quát đến các cấu trúc mã hóa văn bản không phổ biến (cây, đồ thị, JSON tổ) như một gia đình các cuộc tấn công mã hóa.

> **【中文解读】**本节介绍 ASCII 艺术视觉越狱用文本图形绕过安全过器的攻击技术。ArtPrompt(ACL 2024) 两步攻击:识别安全相关词,用 ASCII 艺术染替换。安全过器看无害的标点符号网格,模型看一个词──GPT-4、Gemini、Claude、Llama-2 全部失败,攻击成功率超过75%──

> **【拓展：ArtPrompt → 编码攻击家族】**标准防御 (困惑度过、释义、重新分词) trên ArtPrompt trên toàn bộ thất bại, vì các thiết bị an ninh trong lệnh牌/语义级操作, trong khi ArtPrompt trong hình ảnh nhận dạng cấp độ操作。StructuralSleight sẽ được quảng bá đến hiếm thấy văn bản mã hóa cấu trúc (UTS) 树、图、嵌套 JSON、CSV-in-JSON bất kỳ đào tạo dữ liệu an ninh hiếm gặp nhưng các mô hình phân giải được cấu trúc có thể ẩn nội dung độc hại。

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, ArtPrompt token-masking harness) | **语言:** Python（标准库，ArtPrompt token 掩码框架）
**Prerequisites:** Phase 18 · 12 (PAIR), Phase 18 · 13 (MSJ) | **前置知识:** Phase 18 · 12 (PAIR), Phase 18 · 13 (MSJ)
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**Học本节前请先掌握:Phase 18·12-13──视觉越狱 = 用 ASCII 艺术/树状图/JSON 等编码攻击绕过文本过器──
>  **【类比】**ASCII 越狱 = "隐形墨水"。安全过器看无害的标点网格,模型视觉理解为一个词。ArtPrompt ACL 2024:GPT-4/Gemini/Claude/Llama-2 全失败,>75% 攻击成功率──绕过PPL 过、改写、重代币 化防御──结构性变种(StructuralSleight) mở rộng thành树/图/嵌套 JSON所有非语义视觉提示都是攻击面──

## Mục tiêu học tập

- Mô tả cuộc tấn công ArtPrompt: bước xác định từ, thay thế ASCII-art, lời nhắc cuối cùng được che giấu.

> 描述 ArtPrompt 攻击:词识别步骤、ASCII 艺术替换、最终伪装提示──

- Giải thích lý do tại sao các hệ thống phòng thủ tiêu chuẩn (PPL, Paraphrase, Retokenization) thất bại trên ArtPrompt.

> 解释为什么标准防御(困惑度过、释义、重新分词) 在 ArtPrompt 上失败──

- Định nghĩa ViTC và mô tả những gì nó đo lường.

> 定义 ViTC并 mô tả nội dung đo lường của nó.

- Mô tả StructuralSleight như là một khái quát hóa cho các cấu trúc mã hóa văn bản bất thường tùy ý.

> Mô tả StructuralSleight như là một sự quảng bá cho bất kỳ một số ít có thể được sử dụng trong các văn bản.

## Vấn đề  vấn đề

Các cuộc tấn công thông qua đoạn phrasing và role play (Dạy học 12) và thông qua ngữ cảnh dài (Dạy học 13) hoạt động trên mô hình cấp văn bản. ArtPrompt hoạt động ở cấp độ nhận dạng: mô hình không phân tích mã thông báo cấm. Nó phân tích một hình ảnh được hiển thị bằng ký tự.

> Thông qua giải thích và vai diễn (Lection 12) và长上下文 (Lection 13) của tấn công trên mô hình văn bản cấp độ hoạt động.

## Khái niệm

> **【中文解读】**ArtPrompt 两步攻击的细节:第一步给定有害请求,使用LLM 识别安全相关词(如"bomb"在"how to make a bomb"中);第二步将每个识别的词换为其ASCII 艺术染(7x5或7x7字符块形成字母形状) ;; mô hình nhận được là标点和空格网格, đủ mạnh mô hình có thể nhận dạng thành từ;安全过器只看网格;;

### ArtPrompt, hai bước

Bước 1. Chứng nhận từ: Khi có yêu cầu gây hại, kẻ tấn công sử dụng LLM để xác định các từ liên quan đến an toàn (ví dụ: "bomb" trong " làm thế nào để làm một quả bom"). 

Bước 2. Phép tạo Prompt được che giấu. Thay thế mỗi từ được xác định bằng cách hiển thị nghệ thuật ASCII của nó (một khối ký tự 7x5 hoặc 7x7 tạo thành hình chữ). Mô hình nhận được một lưới dấu chấm và không gian mà một mô hình đủ khả năng có thể nhận ra như là từ; một bộ lọc an toàn chỉ nhìn thấy lưới.

Kết quả: GPT-4, Gemini, Claude, Llama-2, GPT-3.5 đều thất bại. tỷ lệ thành công tấn công trên 75% trên bộ phận chuẩn của họ.

> Kết quả: GPT-4、Gemini、Claude、Llama-2、GPT-3.5 全部失败── tỷ lệ thành công tấn công trên基准子集超过75%──

> **【拓展：防御失败 → 多层安全启示】**困惑度过器失败是因为合法结构化输入也得分高;释义失败是因为释义 LLM 常保留或重建 ASCII 艺术;重新分词失败是因为识别是视觉的而不是令牌级的──安全必须泛化到模型能解析的所有结构化表示这个集合很大且正在增长──

### Tại sao các hệ thống phòng thủ tiêu chuẩn thất bại

- **PPL (perplexity filter).**Nghệ thuật ASCII có độ phức tạp cao nhưng cũng như tất cả các đầu vào mới. Các lựa chọn ngưỡng chặn ArtPrompt cũng chặn đầu vào có cấu trúc hợp pháp.

> **困惑度过滤。**ASCII 艺术 có độ bối rối cao nhưng tất cả các nhập mới cũng vậy── ngăn chặn sự lựa chọn giá trị của ArtPrompt cũng sẽ ngăn chặn nhập cấu trúc hợp pháp──

- **Paraphrase.**Các quy định định định định nghĩa của các quy định định định nghĩa của các quy định định định nghĩa của các quy định định định nghĩa của các quy định định định nghĩa của các quy định định định nghĩa của các quy định định định nghĩa của các quy định định định nghĩa của các quy định định định nghĩa của các quy định định định nghĩa của các quy định định định nghĩa của các quy định định định nghĩa của các quy định định định nghĩa của các quy định định định nghĩa của các quy định định định nghĩa của các quy định định định nghĩa của các quy định định định nghĩa của các quy định định định nghĩa của các quy định định định định nghĩa của quy định định nghĩa của quy định định nghĩa của quy định định nghĩa.

> **释义。**释义提示会破坏 ASCII 艺术── thực tế,释义 LLM 常常保留或重建艺术──

- **Retokenization.**Chia mã hiệu khác nhau không thay đổi rằng tầm nhìn của mô hình là nhận ra hình chữ cái.

> **重新分词。**Không giống như phân chia các biểu đồ sẽ không thay đổi mô hình của hình ảnh trong nhận dạng hình chữ cái thực tế.

Vấn đề cơ bản là bộ lọc an toàn là cấp token hoặc cấp ngữ nghĩa; ArtPrompt hoạt động ở cấp độ nhận dạng thị giác.

> 根本问题是安全过器在令牌或语义级操作;ArtPrompt在视觉识别级操作;;

> **【中文解读】**ViTC 基准:ArtPrompt's有效性与模型读取视觉文本的能力相关ViTC 准确率越高,ArtPrompt 越有效。这是一个能力-安全权衡:提升模型的多模态理解能力会同时增加编码攻击的脆弱性──视觉 LLM(GPT-5.2, Gemini 3 Pro, Claude Opus 4.5, Grok 4.1) đã mở rộng các cuộc tấn công trên mặt  hình ảnh thực tế của ArtPrompt 式 tấn công mạnh hơn ASCII 艺术更强──

### Chỉ số chuẩn ViTC

Việc nhận dạng các lời nhắc thị giác không ngữ nghĩa. đo khả năng của mô hình để đọc ASCII-art, wingdings và nội dung thị giác không ngữ nghĩa văn bản khác. Hiệu quả của ArtPrompt tương quan với độ chính xác ViTC: mô hình đọc văn bản thị giác tốt hơn, ArtPrompt làm việc tốt hơn trên nó. Đây là một sự thỏa hiệp về khả năng và an toàn.

> Không ngữ nghĩa hình ảnh提示的识别──衡量模型读取 ASCII 艺术、 Wingdings 和其他非文本语义视觉内容的能力──ArtPrompt's有效性与ViTC 准确率相关:模型读取视觉文本越好,ArtPrompt's效果越好──这是能力-安全权衡──

### Dòng cấu trúc

ArtPrompt: Các cấu trúc mã hóa văn bản không phổ biến (UTES). Cây, đồ thị, JSON nhốt, CSV-in-JSON, khối mã phong cách khác nhau. Nếu một cấu trúc hiếm khi được đào tạo dữ liệu an toàn nhưng có thể phân tích bằng mô hình, nó có thể che giấu nội dung có hại.

> 推广 ArtPrompt:罕见文本编码结构(UTES) ――树、图、嵌套 JSON、JSON trong CSV、diff 风格代码块── Nếu một cấu trúc trong đào tạo dữ liệu an toàn hiếm nhưng mô hình có thể phân tích, nó có thể ẩn nội dung độc hại──

Sự liên quan của phòng thủ: an toàn phải tổng quát trên các đại diện cấu trúc mô hình có thể phân tích.

> 防御启示: an ninh phải được phổ biến thành mô hình có thể giải quyết tất cả các biểu hiện cấu trúc.

### Phương pháp tương tự hình ảnh

Các LLM hình ảnh (GPT-5.2, Gemini 3 Pro, Claude Opus 4.5, Grok 4.1) mở rộng bề mặt tấn công. Các cuộc tấn công theo kiểu ArtPrompt với hình ảnh thực tế mạnh hơn so với các tương tự ASCII-art vì mã hóa hình ảnh tạo ra tín hiệu phong phú hơn.

> 视觉 LLM  mở rộng diện tích tấn công. Sử dụng hình ảnh thực tế ArtPrompt 式 tấn công mạnh hơn ASCII 艺术, vì bộ điều chỉnh hình ảnh tạo ra các tín hiệu phong phú hơn.

### Khi điều này phù hợp với giai đoạn 18

Bài học 12-14 mô tả ba vector tấn công trực giác: tinh chỉnh lặp lại (PAIR), chiều dài ngữ cảnh (MSJ) và mã hóa (ArtPrompt / StructuralSleight). Bài học 15 chuyển từ các cuộc tấn công tập trung vào mô hình sang các cuộc tấn công giới hạn hệ thống (động lắp sao trực tiếp). Bài học 16 mô tả phản ứng công cụ phòng thủ.

> Bài học 12-14  mô tả ba chính交 tấn công向量:代改进(PAIR)、上下文长度(MSJ) 和编码(ArtPrompt/StructuralSleight)。 Bài học 15 Từ mô hình trung tâm tấn công chuyển hướng hệ thống biên giới tấn công。 Bài học 16  mô tả các công cụ phòng thủ đáp ứng。

> **【拓展：视觉 LLM → 攻击面扩展】**视觉 LLM(GPT-5.2, Gemini 3 Pro, Claude Opus 4.5, Grok 4.1) đã mở rộng các cuộc tấn công.

## Sử dụng nó.
```figure
al-ascii-cloak
```

## Sử dụng nó

`code/main.py`Bạn có thể che giấu các từ cụ thể trong truy vấn gây hại bằng glyph ASCII-art, xác minh chuỗi che giấu vượt qua một bộ lọc từ khóa, và (tự chọn) giải mã lại chuỗi che giấu bằng cách sử dụng một công nhận đơn giản.

> `code/main.py`构建一个玩具 ArtPrompt── bạn có thể sử dụng ASCII 艺术字形伪装有害查询中的特定词,验证伪装字符串通过关键词过,并(可选地) sử dụng đơn giản识别器解码──

## Đưa nó lên mạng

Bài học này sẽ mang lại kết quả `outputs/skill-encoding-audit.md`. Với báo cáo phòng thủ jailbreak, nó liệt kê các nhóm mã hóa tấn công được bao gồm (ASCII art, base64, leet-speak, UTF-8 homoglyph, UTES) và lớp phòng thủ bắt được mỗi nhóm.

> 本课产 出 `outputs/skill-encoding-audit.md`❖ Đưa ra báo cáo phòng thủ tù, liệt kê các lớp phòng thủ của mỗi nhóm đối phó.

## Tập luyện bài tập

1. Đi chạy`code/main.py`- Kiểm tra chuỗi che giấu vượt qua một bộ lọc từ khóa đơn giản. báo cáo sự thay đổi cấp độ ký tự cần thiết.

2. Thực hiện mã hóa thứ hai: base64 cho cùng một từ mục tiêu. So sánh tỷ lệ bỏ lọc so với ArtPrompt và khó khăn phục hồi.

3. Đọc Jiang et al. 2024 Mục 4.3 (hậu quả năm mô hình). đề xuất một lý do tại sao độ kháng ArtPrompt của Claude cao hơn so với Gemini trên cùng một tiêu chuẩn.

4. Thiết kế một hệ thống phòng thủ trước thế hệ phát hiện các vùng hình dạng nghệ thuật ASCII trong prompt. đo tỷ lệ dương tính sai trên mã hợp pháp, bảng và ghi chú toán học.

5. StructuralSleight liệt kê 10 cấu trúc mã hóa. vẽ một hệ thống phòng thủ tổng quát xử lý tất cả 10 và ước tính chi phí tính toán cho mỗi lệnh bảo vệ.

## Từ khóa  Keyword

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| ArtPrompt | "the ASCII-art attack" | Two-step jailbreak that masks safety words with ASCII-art renderings |
| Cloaking | "hide the word" | Replace a forbidden token with a visual representation the model reads but the filter does not |
| UTES | "uncommon structure" | Uncommon Text-Encoded Structure — tree, graph, nested JSON, etc. used to smuggle content |
| ViTC | "visual-text capability" | Benchmark for model's ability to read non-semantic visual encoding |
| Perplexity filter | "PPL defense" | Reject prompts with high perplexity; fails because legitimate structured input also scores high |
| Retokenization | "tokenizer shift defense" | Pre-process the prompt with a different tokenizer; fails because recognition is visual |
| Homoglyph | "lookalike characters" | Unicode characters that look identical to Latin letters; bypass substring checks |

## Xem thêm 延伸阅读

- [Jiang et al. — ArtPrompt (ACL 2024, arXiv:2402.11753)](https://arxiv.org/abs/2402.11753) giấy jailbreak ASCII-art
- [Li et al. — StructuralSleight (arXiv:2406.08754)](https://arxiv.org/abs/2406.08754) UTS tổng quát
- [Chao et al. — PAIR (Lesson 12, arXiv:2310.08419)](https://arxiv.org/abs/2310.08419) tấn công lặp lại bổ sung
- [Anil et al. — Many-shot Jailbreaking (Lesson 13)](https://www.anthropic.com/research/many-shot-jailbreaking) tấn công dài bổ sung
