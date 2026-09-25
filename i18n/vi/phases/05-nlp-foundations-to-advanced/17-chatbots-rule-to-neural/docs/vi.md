# Chatbot  Rule-Based đến Neural đến LLM Agents  Chat chat机器人  quy tắc đến mạng thần kinh đến LLM Agent

> ELIZA trả lời bằng các mô hình phù hợp. DialogFlow lập bản đồ ý định. GPT trả lời từ trọng lượng. Claude chạy công cụ và xác minh. Mỗi thời đại giải quyết sự thất bại tồi tệ nhất của thời đại trước.
> ELIZA 用模式匹配回复──DialogFlow 映射意图──GPT Từ trọng lượng trả lời──Claude 运行工具并验证──每时代解决了上一时代最严重失败──

> **【中文解读】**Từ ELIZA đến Seq2Seq đến GPT Agent.

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 13 (Question Answering), Phase 5 · 14 (Information Retrieval) | **前置知识:** Phase 5 · 13（问答系统），Phase 5 · 14（信息检索与搜索）
**Time:** ~75 minutes | **时间:** ~75 分钟

## Vấn đề  vấn đề giới thiệu

Một người dùng nói "Tôi muốn thay đổi chuyến bay của mình". Hệ thống phải tìm ra những gì họ muốn, thông tin nào bị thiếu, làm thế nào để có được nó, và làm thế nào để hoàn thành hành động. Sau đó người dùng nói "ngợi đã, nếu tôi hủy thay thế thì sao?" và hệ thống phải nhớ bối cảnh, thay đổi các nhiệm vụ, và bảo tồn trạng thái.

> Người dùng nói "我想改变签航班――" 系统 phải hiểu rõ họ muốn gì, thiếu thông tin gì, làm thế nào để có được nó, làm thế nào để hoàn thành hoạt động đó.

> **【中文解读】**Câu hỏi được đặt ra trong phần này là: làm thế nào để hiểu và áp dụng đúng công nghệ này trong công trình thực tế.

Cuộc trò chuyện là khó khăn cho một hệ thống ML. Các đầu vào là mở. Các đầu ra phải có liên kết qua nhiều lượt. Hệ thống có thể cần phải hành động trên thế giới (hãy thay đổi chuyến bay, sạc thẻ). Mỗi bước sai đều hiển thị cho người dùng.

> Đối thoại đối với hệ thống ML rất khó khăn. Lập nhập là mở. Lập phát phải được duy trì liên tục trong nhiều vòng. Hệ thống có thể cần phải hành động đối với thế giới.

Các kiến trúc chatbot đã đi qua bốn mô hình, mỗi mô hình được giới thiệu bởi vì mô hình trước đã thất bại quá rõ ràng. Bài học này đưa chúng vào thứ tự.

> 聊天机器人架构经历了四种范式, mỗi loại đều là do thất bại trước quá rõ ràng và được giới thiệu.

## Khái niệm cốt lõi

> **【中文解读】**Bài viết này giới thiệu các khái niệm và lý thuyết cốt lõi.

![Chatbot evolution: rule-based → retrieval → neural → agent](../assets/chatbot.svg)

### Lần viết kịch bản nửa thế kỷ, 1950-2001

Các mô hình đầu tiên không kéo dài năm năm. Nó kéo dài năm mươi. Biết cung của nó quan trọng bởi vì mọi hệ thống trong nó là cùng một máy  nhập phù hợp, phát ra một phản ứng đóng hộp, cập nhật một trạng thái  và năm mươi năm thêm các quy tắc vào máy đó không bao giờ tạo ra trường hợp chung.

**1950.**Turing tránh "cỗ máy có thể nghĩ được không?" bằng cách đề xuất một thay thế hoạt động: nếu một người thẩm vấn không thể phân biệt máy với một người qua máy tính, câu hỏi triết học là tranh cãi.

**1956.**Tên gọi đến từ một hội thảo mùa hè tại Dartmouth đồng xu "kỹ thuật nhân tạo" dựa trên giả định rằng mọi tính năng của trí tuệ "có thể được mô tả chính xác đến mức có thể tạo ra một máy móc để mô phỏng nó".

**1966.**ELIZA đưa ra thủ thuật phản xạ bạn xây dựng trong bước 1: các quy tắc phân hủy kéo các mảnh vỡ từ đầu vào, các quy tắc tái lắp ráp phản hồi chúng như câu hỏi. Khoảng 200 mẫu tổng cộng, trạng thái không, không hiểu biết  và người dùng tin tưởng nó bất cứ cách nào. Weizenbaum đã dành phần còn lại của sự nghiệp của mình lo lắng bởi số máy móc ít nó mất.

**1972.**PARRY, được xây dựng tại Stanford để mô hình sự hoang tưởng, thêm vào phần ELIZA thiếu: trạng thái nội tâm. Các biến số cho nỗi sợ hãi, giận dữ và mất tin cập nhật ở mỗi lượt và cổng mà kịch bản phát ra tiếp theo, do đó các đầu vào giống nhau tạo ra các phản ứng khác nhau tùy thuộc vào cuộc trò chuyện cho đến nay. Trong một xét nghiệm ghi chép mù, các bác sĩ tâm thần đã phân biệt PARRY với bệnh nhân con người. Nó là tổ tiên trực tiếp của điều kiện persona  một hệ thống nhanh chóng được triển khai như ba float. Cùng năm, hai robot được chỉ vào nhau qua ARPANET: một kịch bản của một nhà trị liệu phỏng vấn một máy trạng thái hoang tưởng, cuộc trò chuyện đầu tiên giữa bot và bot trên mạng.

**1995.**ALICE mở rộng quy mô công thức ELIZA với AIML, một phương ngữ XML cho các cặp mẫu mẫu. Khoảng 40.000 danh mục được viết tay, ba giải thưởng Loebner. Nó chứng minh luật mở rộng của các hệ thống dựa trên quy tắc: nhiều quy tắc hơn mua bảo hiểm, không bao giờ nói chung. Mỗi quy tắc là một trách nhiệm mà ai đó phải duy trì.

**2001.**SmarterChild đặt công thức trước mặt 30 triệu người dùng nhắn tin tức thời và thêm tìm kiếm hậu cảnh  thời tiết, cổ phiếu, thời gian phim  được chia thành mẫu.

Năm mươi năm, một cơ chế, một quy tắc tăng lên đếm. mô hình đã kết thúc không phải vì ai đã bác bỏ nó mà bởi vì chi phí bảo trì của máy viết tay tăng theo tuyến tính với bảo hiểm trong khi kỳ vọng của người dùng tăng với bất cứ điều gì họ đã thấy tuần trước.

```figure
chatbot-lineage
```

**Rule-based (ELIZA, AIML, DialogFlow).**Các mô hình được viết tay phù hợp với thông tin nhập của người dùng và tạo ra phản ứng. Các bộ phân loại ý định định hướng đến dòng chảy được xác định trước. Máy lấp đầy trạng thái thu thập thông tin cần thiết. Làm việc tuyệt vời bên trong phạm vi hẹp nó được thiết kế. Thất bại ngay bên ngoài nó.

> **基于规则（ELIZA、AIML、DialogFlow）。**│ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │

**Retrieval-based.**Một hệ thống kiểu FAQ. Mã hóa từng cặp (những phát biểu, phản ứng). Vào thời gian chạy, mã hóa thông điệp của người dùng và lấy lại phản ứng được lưu trữ gần nhất. Hãy nghĩ về tính năng "những bài viết tương tự" cổ điển của Zendesk.

> **基于检索。**FAQ 式系统──编码每对(话语、响应) ――运行时编码用户消息并检索最近储存响应──类似于Zendesk's classic "类似文章" 功能──比规则更好处理释义──无生成,所以无幻觉──

**Neural (seq2seq).**Các mã hóa-các mã hóa được đào tạo trên nhật ký trò chuyện. Tạo ra phản ứng từ đầu. Thông thường nhưng dễ bị kết quả chung ("Tôi không biết") và biến động thực tế. Không bao giờ đáng tin cậy về chủ đề. Lý do Google, Facebook và Microsoft đều có chatbot thất vọng trong năm 2016-2019.

> **神经（seq2seq）。**Trong cuộc hội thoại ngày học tập trên các bộ lập trình viên giải mã. Từ zero tạo phản ứng. Từ dòng chảy nhưng xu hướng chung xuất.

**LLM agents.**Một mô hình ngôn ngữ được gói trong một vòng tròn có kế hoạch, gọi công cụ và xác minh kết quả. Không phải chatbot với một lời nhắc dài. Một vòng tròn đại lý: kế hoạch → gọi công cụ → quan sát kết quả → quyết định bước tiếp theo. lấy lại-làm đất đầu tiên (RAG) giữ cho nó khỏi ảo giác. gọi công cụ thực sự cho nó làm những thứ. Đây là kiến trúc 2026 .

> **LLM Agent。**包装在循环中的语言模型,规划,调用工具并验证结果──不是带长提示的聊天机器人──一个代理 循环:规划 → 调用工具 → 观察结果 → quyết định next step──检索优先的定(RAG) 防止幻觉──工具调用让它实际做事──这就是2026年的架构──

Bốn mô hình này không phải là thay thế theo trình tự. Một chatbot sản xuất năm 2026 sẽ đi qua tất cả bốn: dựa trên quy tắc cho xác thực và hành động phá hủy, lấy lại cho các câu hỏi thường gặp, tạo ra thần kinh cho các cụm từ tự nhiên, đại lý LLM cho các truy vấn mở mơ hồ.

> Những mô hình này không thay thế theo thứ tự. Năm 2026, các máy tính chat sản xuất thông qua tất cả bốn tuyến đường: dựa trên quy tắc để xác nhận và hoạt động phá hủy, tìm kiếm để FAQ, sinh lý để ngôn ngữ tự nhiên, LLM Agent sử dụng để tìm kiếm mở mờ.

> **【拓展：大语言模型的工程实践】**Từ GPT đến ChatGPT, NLP đã trải qua sự chuyển đổi từ "mỗi nhiệm vụ đào tạo một mô hình" đến "một mô hình giải quyết tất cả các nhiệm vụ". Trong công trình thực tế, việc triển khai LLM cần phải xem xét các vấn đề như: giới hạn token, trì hoãn, chi phí, kiểm tra an toàn, và các vấn đề khác.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) là cấu trúc phổ biến nhất trong ứng dụng AI của doanh nghiệp hiện tại: sẽ truy vấn người dùng trước tiên truy vấn các đoạn tài liệu liên quan, tiếp tục truy vấn kết quả như trên dưới đây cho LLM 生成答案──

> **【拓展：NLP 的多语言挑战】**Trên toàn cầu có hơn 7000 ngôn ngữ, nhưng nghiên cứu về NLP tập trung chủ yếu vào tiếng Anh và một số ít ngôn ngữ.

## Hãy xây dựng nó.

> **【中文解读】**本节通过代码实现核心算法从零――这种" từ đầu"的方式能帮助理解框架背后的原理,遇到问题时不会被黑盒困住――

### Bước 1: Đáp hợp mô hình dựa trên quy tắc

```python
import re


class RulePattern:
    def __init__(self, pattern, response_template):
        self.regex = re.compile(pattern, re.IGNORECASE)
        self.template = response_template


PATTERNS = [
    RulePattern(r"my name is (\w+)", "Nice to meet you, {0}."),
    RulePattern(r"i (need|want) (.+)", "Why do you {0} {1}?"),
    RulePattern(r"i feel (.+)", "Why do you feel {0}?"),
    RulePattern(r"(.*)", "Tell me more about that."),
]


def rule_based_respond(user_input):
    for pattern in PATTERNS:
        m = pattern.regex.match(user_input.strip())
        if m:
            return pattern.template.format(*m.groups())
    return "I don't understand."
```

ELIZA trong 20 dòng. Tránh suy nghĩ ("Tôi cảm thấy buồn" → "Tại sao bạn cảm thấy buồn") là bản demo của nhà tâm lý trị liệu giáo học từ Weizenbaum 1966.

> 20 行 ELIZA──反射技巧("Tôi cảm thấy buồn" → "Tại sao bạn cảm thấy buồn") là bài thuyết trình của nhà trị liệu tâm lý học cổ điển của Weizenbaum năm 1966.

### Bước 2: dựa trên truy xuất (FAQ)

Đoạn minh họa này đòi hỏi:`pip install sentence-transformers`(được kéo trong ngọn đuốc).`code/main.py`cho bài học này sử dụng một sự tương đồng Stdlib Jaccard thay vào đó, vì vậy bài học chạy mà không có phụ thuộc bên ngoài.

> Ví dụ này có thể được xem như là một phần của`pip install sentence-transformers`(会拉取火) │本课的可运行 `code/main.py`Sử dụng Jaccard tương tự của thư viện tiêu chuẩn thay thế, như vậy các khóa học không cần phải phụ thuộc bên ngoài là có thể vận hành.

```python
from sentence_transformers import SentenceTransformer
import numpy as np


FAQ = [
    ("how do i reset my password", "Go to Settings > Security > Reset Password."),
    ("how do i cancel my order", "Go to Orders, find the order, click Cancel."),
    ("what is your return policy", "30-day returns on unused items, original packaging."),
]


encoder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
faq_questions = [q for q, _ in FAQ]
faq_embeddings = encoder.encode(faq_questions, normalize_embeddings=True)


def faq_respond(user_input, threshold=0.5):
    q_emb = encoder.encode([user_input], normalize_embeddings=True)[0]
    sims = faq_embeddings @ q_emb
    best = int(np.argmax(sims))
    if sims[best] < threshold:
        return None
    return FAQ[best][1]
```

Việc từ chối dựa trên ngưỡng là lựa chọn thiết kế quan trọng. Nếu sự phù hợp tốt nhất không đủ gần, hãy trả lại `None`và để hệ thống leo thang.

> 基于值的拒绝是关键设计选择. Nếu sự phù hợp tốt nhất không đủ gần, trả lại `None`让系统升级处理――

### Bước 3: Tạo ra thần kinh (tầm cơ bản)

Sử dụng một bộ mã hóa-tử toán nhỏ có điều chỉnh hướng dẫn (FLAN-T5) hoặc mô hình trò chuyện được điều chỉnh tốt. Sản xuất không thể sử dụng riêng vào năm 2026 (sự mâu thuẫn, trôi dạt ngoài chủ đề, vô nghĩa thực tế), nhưng tàu trong hệ thống lai để định nghĩa tự nhiên. Các mô hình chỉ có trình giải mã kiểu DialoGPT cần các bộ tách vòng rõ ràng và xử lý EOS để tạo ra các câu trả lời nhất quán; một đường ống văn bản FLAN-T5 làm việc ngoài hộp cho một ví dụ giảng dạy.

> Sử dụng các chỉ thị nhỏ nhỏ điều chỉnh lập trình viên giải mã máy (FLAN-T5) hoặc mô hình đối thoại nhỏ điều chỉnh. Năm 2026 sử dụng độc lập không phù hợp với sản xuất.

```python
from transformers import pipeline

chatbot = pipeline("text2text-generation", model="google/flan-t5-small")

response = chatbot("Respond politely to: Hi there!", max_new_tokens=40)
print(response[0]["generated_text"])
```

### Bước 4: vòng đại lý LLM

Hình thức sản xuất năm 2026:

> Tương tự sản xuất năm 2026:

```python
def agent_loop(user_message, tools, llm, max_steps=5):
    history = [{"role": "user", "content": user_message}]
    for _ in range(max_steps):
        response = llm(history, tools=tools)
        tool_call = response.get("tool_call")
        if tool_call:
            tool_name = tool_call.get("name")
            args = tool_call.get("arguments")
            if not isinstance(tool_name, str) or tool_name not in tools:
                history.append({"role": "assistant", "tool_call": tool_call})
                history.append({"role": "tool", "name": str(tool_name), "content": f"error: unknown tool {tool_name!r}"})
                continue
            if not isinstance(args, dict):
                history.append({"role": "assistant", "tool_call": tool_call})
                history.append({"role": "tool", "name": tool_name, "content": f"error: arguments must be a dict, got {type(args).__name__}"})
                continue
            fn = tools[tool_name]
            result = fn(**args)
            history.append({"role": "assistant", "tool_call": tool_call})
            history.append({"role": "tool", "name": tool_name, "content": result})
        else:
            return response["content"]
    return "I could not complete the task in the step budget."
```

Các công cụ là các chức năng có thể gọi mà LLM có thể gọi. vòng lặp kết thúc khi LLM trả lời cuối cùng thay vì một cuộc gọi công cụ. Ngân sách bước ngăn chặn vòng lặp vô hạn trên các nhiệm vụ mơ hồ.

> Trò chơi chơi game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game game

Sản xuất thực sự thêm: lấy lại-đầu tiên đặt đất (đưa các tài liệu liên quan trước mỗi cuộc gọi LLM), guardrails (đưa hành động phá hủy mà không có xác nhận), khả năng quan sát (đăng từng bước), và đánh giá (điểm tra tự động rằng hành vi của đại lý vẫn theo đặc điểm).

> Thực tế sản xuất cũng cần: kiểm tra ưu tiên định( mỗi lần LLM 调用前注入相关文档) 护(未经确认拒绝破坏性操作) 可观测性(记录每步) 和评估(自动检查代理 行为保持规范) 

### Bước 5: Đường dẫn lai

```python
def hybrid_chat(user_input):
    if is_destructive_action(user_input):
        return structured_flow(user_input)

    faq_answer = faq_respond(user_input, threshold=0.6)
    if faq_answer:
        return faq_answer

    return agent_loop(user_input, tools, llm)


def is_destructive_action(text):
    danger_words = ["delete", "cancel", "charge", "refund", "transfer"]
    return any(w in text.lower() for w in danger_words)
```

Mô hình: quy tắc xác định cho bất cứ điều gì phá hủy, tìm kiếm cho các câu hỏi thường gặp được đóng hộp, đại lý LLM cho mọi thứ khác. Đây là những gì các hệ thống hỗ trợ khách hàng năm 2026 sẽ đưa ra.

> 模式: đối với bất kỳ hoạt động phá hoại nào sử dụng quy tắc xác định, đối với các câu hỏi thường gặp cố định sử dụng kiểm tra, đối với mọi thứ khác sử dụng LLM Agent.

> **【中文解读】**Bài này sẽ trình bày cách sử dụng một khung đã phát triển như PyTorch, HuggingFace, và các khác.

> **【拓展：Prompt Engineering 与 LLM 应用】**Kỹ thuật nhanh chóng đã trở thành kỹ năng cốt lõi của các kỹ sư NLP. Từ Zero-shot đến Few-shot, từ Chain-of-Thought đến ReAct, các chiến lược khác nhau áp dụng cho các tình huống khác nhau. Trong các dự án thực tế, thiết kế của System提示(System Prompt) ảnh hưởng trực tiếp đến sự ổn định và chất lượng sản xuất của ứng dụng LLM.

## Hãy sử dụng nó để thực hiện

Số 2026:

> 2026 năm của công nghệ:

| Use case / 使用场景 | Architecture / 架构 |
|---------|---------------|
| Booking, payment, authentication / 预订、支付、认证 | Rule-based state machines + slot filling / 基于规则的状态机 + 槽位填充 |
| Customer support FAQs / 客户支持 FAQ | Retrieval over curated answers / 对精选答案的检索 |
| Open-ended help chat / 开放式帮助聊天 | LLM agent with RAG + tool calls / 带 RAG + 工具调用的 LLM Agent |
| Internal tools / IDE assistants / 内部工具 / IDE 助手 | LLM agent with tool calls (search, read, write) / 带工具调用的 LLM Agent（搜索、读写） |
| Companion / character chatbots / 伴侣/角色聊天机器人 | Tuned LLM with persona system prompt, retrieval on knowledge / 微调 LLM 配角色系统提示和知识检索 |

Luôn sử dụng định tuyến lai trong sản xuất. Không một kiến trúc duy nhất xử lý mọi yêu cầu tốt.

> Trong sản xuất luôn sử dụng đường hỗn hợp. Không có cấu trúc đơn lẻ có thể xử lý từng yêu cầu.

## Các chế độ thất bại vẫn được vận chuyển sẽ tiếp tục được sản xuất.

- **Confident fabrication.**Trưởng LLM tuyên bố đã hoàn thành một hành động mà họ không làm.
  **自信捏造。**LLM Agent tuyên bố đã hoàn thành một hoạt động chưa hoàn thành.
- **Prompt injection.**Người dùng chèn văn bản vượt qua lệnh hệ thống. LLM01 xếp hạng trong Top 10 của OWASP cho các ứng dụng LLM 2025. Hai hương vị: tiêm trực tiếp (được dán vào cuộc trò chuyện) và tiêm gián tiếp (được ẩn trong tài liệu, email hoặc các sản phẩm công cụ mà đại lý đọc).
  **提示注入。**Người dùng插入覆盖系统提示的文本── 在 OWASP LLM 应用 2025 Top 10 中排 LLM01──两种形式: trực tiếp注入(粘贴到聊天中) 和间接注入(藏在文档、邮件或代理 读取的工具输出中)

  Tỷ lệ tấn công khác nhau theo kịch bản. Tỷ lệ thành công được đo lường dao động từ ~ 0,5-8,5% trên các mô hình biên giới trong các tiêu chuẩn sử dụng công cụ và mã hóa chung. Các thiết lập rủi ro cao cụ thể (những cuộc tấn công thích nghi chống lại các tác nhân mã hóa AI, dàn xếp dễ bị tổn thương) đã đạt đến ~ 84%. Các CVE sản xuất bao gồm EchoLeak (CVE-2025-32711, CVSS 9.3)  một lỗi xóa dữ liệu bằng nhấp chuột không trong Microsoft 365 Copilot được kích hoạt bởi một email bị kẻ tấn công kiểm soát.
  攻击成功率因场景而异. Trong các công cụ chung và chuẩn lập lập trình, tỷ lệ thành công của mô hình tiền tuyến được đo lường là khoảng 0,5-8,5%. 设置 rủi ro cao nhất: 针对 AI 编码代理自适应攻击, 脆弱编排) đã đạt khoảng 84%. 生产 CVE bao gồm EchoLeak: CVE-2025-32711, CVSS 9.3.  Microsoft 365 Copilot: 零点击数据泄漏漏漏洞, được kiểm soát bởi kẻ tấn công.

  Giảm thiểu: xử lý đầu vào của người dùng như không đáng tin cậy trong suốt vòng lặp; làm sạch trước khi gọi công cụ; tách các sản phẩm công cụ khỏi lời nhắc chính; sử dụng mô hình Plan-Verify-Execute (PVE) nơi người đại lý lập kế hoạch trước, sau đó xác minh từng hành động chống lại kế hoạch trước khi thực hiện (điều này ngăn chặn kết quả công cụ từ tiêm các hành động không được lập kế hoạch mới); yêu cầu xác nhận người dùng cho các hành động phá hủy; áp dụng quyền tối thiểu cho phạm vi công cụ.
  缓解措施: trong suốt chu kỳ sẽ người dùng nhập vào như không thể tin được; tool调用前消毒;将工具输出与主提示隔离; sử dụng quy hoạch-验证-执行 (PVE) mô hình,Agent先规划,然后对每个操作按计划验证后再执行 (This blocks tool result to in new unplanned operation); cho phép người dùng xác nhận yêu cầu về các hoạt động phá hủy; cho phép tối thiểu đối với phạm vi ứng dụng của các công cụ.

  Không có một số lượng kỹ thuật nhanh chóng loại bỏ hoàn toàn rủi ro này.
  Bất kể có bao nhiêu gợi ý kỹ thuật đều không thể loại bỏ hoàn toàn rủi ro này.
- **Scope creep.**Trưởng lý sẽ không làm việc vì một cuộc gọi công cụ trả về thông tin liên quan liên quan. Giảm thiểu: hợp đồng công cụ hẹp; giữ cho hệ thống nhanh chóng tập trung; thêm đánh giá cho tỷ lệ ngoài nhiệm vụ.
  **范围蔓延。**Trình tác viên vì công cụ调用 trả về thông tin liên quan gián tiếp và chạy vấn đề.
- **Infinite loops.**Trưởng phòng liên tục gọi cùng một công cụ, giảm thiểu ngân sách, giảm gấp đôi công cụ, thẩm phán về "chúng ta đang tiến bộ".
  **无限循环。**Trưởng lý tiếp tục sử dụng cùng một công cụ.
- **Context window exhaustion.**Các cuộc trò chuyện dài đẩy các lượt đầu tiên ra khỏi ngữ cảnh. Giảm nhẹ: tóm tắt các lượt cũ hơn, lấy lượt trước tương quan bằng sự tương đồng hoặc sử dụng mô hình ngữ cảnh dài.
  **上下文窗口耗尽。**长对话将最早轮次推出上下文──缓解:摘要旧轮次、根据相似性检查相关历史轮次、或使用长上下文模型──

> **【中文解读】**Phần này tập trung vào cách phân phối mô hình như một sản phẩm có thể sử dụng.

## Chuyển nó đi.

Cứ như `outputs/skill-chatbot-architect.md`- Có thể là:

> 保存为 `outputs/skill-chatbot-architect.md`- Có thể là:

```markdown
---
name: chatbot-architect
description: Design a chatbot stack for a given use case.
version: 1.0.0
phase: 5
lesson: 17
tags: [nlp, agents, chatbot]
---

Given a product context (user need, compliance constraints, available tools, data volume), output:

1. Architecture. Rule-based, retrieval, neural, LLM agent, or hybrid (specify which paths go where).
2. LLM choice if applicable. Name the model family (Claude, GPT-4, Llama-3.1, Mixtral). Match to tool-use quality and cost.
3. Grounding strategy. RAG sources, retrieval method (see lesson 14), tool contracts.
4. Evaluation plan. Task success rate, tool-call correctness, off-task rate, hallucination rate on held-out dialogs.

Refuse to recommend a pure-LLM agent for any destructive action (payments, account deletion, data modification) without a structured confirmation flow. Refuse to skip the prompt-injection audit if the agent has write access to anything.
```

> **【中文解读】**练题按照 Easy/Medium/Hard 三个难度递进;;建议至少完成 级别的题目, 级别适合深入研究或面试准备;;

## Tập luyện bài tập

1. **Easy.**Thực hiện các câu trả lời dựa trên quy tắc ở trên với 10 mẫu cho một bot đặt hàng quán cà phê. Các trường hợp kiểm tra: đặt hàng hai lần, sửa đổi, hủy bỏ, ý định không rõ ràng.
   **简单。**Để thực hiện các phản ứng dựa trên quy tắc trên, 10 mô hình.
2. **Medium.**Xây dựng một FAQ lai + LLM fallback. 50 mục FAQ đóng hộp cho một sản phẩm SaaS, LLM fallback với truy xuất trên trang web tài liệu. Đo tỷ lệ từ chối và độ chính xác trên 100 câu hỏi hỗ trợ thực.
   **中等。**构建混合FAQ + LLM 回退──50 个 SaaS 产品的固定FAQ 条目,LLM 回退带文档站检索──100 个真实支持问题测量拒绝率和准确率──
3. **Hard.**Thực hiện vòng tròn đại lý ở trên với ba công cụ (bảo sát, dữ liệu người dùng đọc, gửi email). Thực hiện đánh giá với 50 kịch bản thử nghiệm bao gồm các nỗ lực tiêm nhanh. Báo cáo tỷ lệ bỏ nhiệm vụ, tỷ lệ thất bại nhiệm vụ và bất kỳ sự thành công tiêm.
   **困难。**Sử dụng ba công cụ (đọc dữ liệu người dùng, gửi thư) để thực hiện các vòng lặp trên của Agent.

> **【中文解读】**Trong 术语表中的"Những gì mọi người nói" vs "Những gì nó thực sự có nghĩa" 区分日常口语和精确技术含义── 在团队协作中,统一术语定义可以避免大量沟通误解──

## Từ khóa  Từ khóa nhanh chóng

| Term / 术语 | What people say / 人们常说的 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| Intent（意图） | What the user wants / 用户想要什么 | Categorical label (book_flight, reset_password). Routed to a handler. / 分类标签（book_flight、reset_password）。路由到处理器。 |
| Slot（槽位） | A piece of info / 一条信息 | Parameter the bot needs (date, destination). Slot filling is the sequence of asks. / 机器人需要的参数（日期、目的地）。槽位填充是依次询问的过程。 |
| RAG（检索增强生成） | Retrieval plus generation / 检索加生成 | Retrieve relevant docs, then ground the LLM's response. / 检索相关文档，然后锚定 LLM 的响应。 |
| Tool call（工具调用） | Function invocation / 函数调用 | LLM emits a structured call with name + args. Runtime executes, returns result. / LLM 发出带名称和参数的结构化调用。运行时执行并返回结果。 |
| Agent loop（Agent 循环） | Plan, act, verify / 规划、执行、验证 | Controller that runs LLM calls interleaved with tool calls until task complete. / 运行 LLM 调用与工具调用交错直到任务完成的控制器。 |
| Prompt injection（提示注入） | User attacks prompt / 用户攻击提示 | Malicious input that tries to override the system prompt. / 试图覆盖系统提示的恶意输入。 |

> **【中文解读】**延伸阅读 cung cấp các nguồn chất lượng cao cho việc học sâu. Những bài báo và giảng dạy này là tài liệu tham khảo cổ điển trong lĩnh vực này, phù hợp với những người đọc cần hiểu sâu hơn.

## Xem thêm 延伸阅读

- [Weizenbaum (1966). ELIZA — A Computer Program For the Study of Natural Language Communication](https://web.stanford.edu/class/cs124/p36-weizenabaum.pdf) bài báo chatbot dựa trên quy tắc ban đầu. / 原始基于规则的聊天机器人论文──
- [Thoppilan et al. (2022). LaMDA: Language Models for Dialog Applications](https://arxiv.org/abs/2201.08239) Bài báo về chatbot thần kinh cuối cùng của Google, ngay trước khi các đại lý LLM tiếp quản.
- [Yao et al. (2022). ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629) tờ báo đặt tên cho mô hình vòng tròn đại lý. / 命名 Agent 循环模式的论文。
- [Anthropic's guide on building effective agents](https://www.anthropic.com/research/building-effective-agents) 2024 chỉ thị sản xuất vẫn còn giữ trong năm 2026. / 2024 年生产指南,2026 年仍然有效。
- [Greshake et al. (2023). Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection](https://arxiv.org/abs/2302.12173) giấy tiêm nhanh. / 提示注入论文。
- [OWASP Top 10 for LLM Applications 2025 — LLM01 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/) xếp hạng khiến cho việc tiêm nhanh trở thành mối quan tâm an ninh hàng đầu. / 使提示注入成为首要安全关注的排名──
- [AWS — Securing Amazon Bedrock Agents against Indirect Prompt Injections](https://aws.amazon.com/blogs/machine-learning/securing-amazon-bedrock-agents-a-guide-to-safeguarding-against-indirect-prompt-injections/) Phòng phòng thủ lớp dàn xếp thực tế bao gồm Plan-Verify-Execute và user-confirmation flow. / 实用编排层防御,包括规划-验证-执行和用户确认流程──
- [EchoLeak (CVE-2025-32711)](https://www.vectra.ai/topics/prompt-injection) CVE không nhấp dữ liệu-exfiltration CVE từ tiêm trực tiếp nhanh chóng. trường hợp tham chiếu tại sao các đại lý truy cập viết cần bảo vệ thời gian chạy. / 间接提示注入的典型零点击数据泄露 CVE──写入权限 Agent 需要运行时防御的参考案例──
| Intent | What the user wants | Categorical label (book_flight, reset_password). Routed to a handler. |
| Slot | A piece of info | Parameter the bot needs (date, destination). Slot filling is the sequence of asks. |
| RAG | Retrieval plus generation | Retrieve relevant docs, then ground the LLM's response. |
| Tool call | Function invocation | LLM emits a structured call with name + args. Runtime executes, returns result. |
| Agent loop | Plan, act, verify | Controller that runs LLM calls interleaved with tool calls until task complete. |
| Prompt injection | User attacks prompt | Malicious input that tries to override the system prompt. |

## Đọc thêm

- [Turing (1950). Computing Machinery and Intelligence](https://academic.oup.com/mind/article/LIX/236/433/986238) bài báo làm cho cuộc trò chuyện là tiêu chuẩn của lĩnh vực.
- [Weizenbaum (1966). ELIZA — A Computer Program For the Study of Natural Language Communication](https://web.stanford.edu/class/cs124/p36-weizenabaum.pdf) giấy chatbot gốc dựa trên các quy tắc.
- [Colby, Weber, Hilf (1971). Artificial Paranoia](https://doi.org/10.1016/0004-3702(71)90002-6)  Thiết kế biến ảnh hưởng của PARRY, chatbot trạng thái đầu tiên.
- [Thoppilan et al. (2022). LaMDA: Language Models for Dialog Applications](https://arxiv.org/abs/2201.08239) Bài báo về chatbot thần kinh của Google, ngay trước khi các đại lý LLM tiếp quản.
- [Yao et al. (2022). ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629) tờ báo đặt tên cho mô hình vòng tròn của đại lý.
- [Anthropic's guide on building effective agents](https://www.anthropic.com/research/building-effective-agents) Dự báo sản xuất 2024 vẫn còn tồn tại vào năm 2026.
- [Greshake et al. (2023). Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection](https://arxiv.org/abs/2302.12173) giấy tiêm nhanh.
- [OWASP Top 10 for LLM Applications 2025 — LLM01 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/) xếp hạng khiến việc tiêm nhanh trở thành mối quan tâm an ninh hàng đầu.
- [AWS — Securing Amazon Bedrock Agents against Indirect Prompt Injections](https://aws.amazon.com/blogs/machine-learning/securing-amazon-bedrock-agents-a-guide-to-safeguarding-against-indirect-prompt-injections/) Các hệ thống phòng thủ lớp dàn xếp thực tế bao gồm Plan-Verify-Execute và user-confirmation flows.
- [EchoLeak (CVE-2025-32711)](https://www.vectra.ai/topics/prompt-injection) CVE phântrình dữ liệu bằng nhấp chuột không theo quy định của CVE từ tiêm trực tiếp.
