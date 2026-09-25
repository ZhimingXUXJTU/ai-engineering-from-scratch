# Thuyết ngữ tự nhiên  Sự liên quan văn bản    

> "t liên quan đến h" có nghĩa là một đọc của con người t sẽ kết luận h là đúng. NLI là nhiệm vụ dự đoán liên quan / mâu thuẫn / trung lập.
> "t 含 h" có nghĩa là con người đọc t 后会推断 h 为真──NLI là dự đoán 含/矛盾/中性的任务──表面无聊,生产中承重──

> **【中文解读】**NLI 判断两个句子之间的逻辑关系: 含、矛盾、中性──

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 05 (Sentiment Analysis), Phase 5 · 10 (Attention) | **前置知识:** Phase 5 · 05（情感分析），Phase 5 · 10（注意力机制）
**Time:** ~45 minutes | **时间:** ~45 分钟

## Vấn đề  vấn đề giới thiệu

Bạn đã xây dựng một chatbot. Nó trả lời "có". Làm thế nào bạn biết rằng "có" được hỗ trợ bởi các bằng chứng? Bạn cần phân loại 10.000 bài báo tin tức theo chủ đề. Bạn có 50 ví dụ được dán nhãn. Bạn biến nó thành NLI: " bài viết này là về { chủ đề} " liên quan hoặc mâu thuẫn? Bạn cần kiểm tra xem một bản tóm tắt được tạo là trung thành với nguồn gốc. NLI một lần nữa.

> Bạn đã xây dựng một máy trò chuyện. Nó trả lời "có"―― Bạn biết làm thế nào "có" có bằng chứng hỗ trợ? Bạn cần theo chủ đề phân loại 10.000 bài viết trên các trang web. Bạn có 50 bài viết trên các trang web. Bạn sẽ chuyển đổi nó thành NLI:

> **【中文解读】**Câu hỏi được đặt ra trong phần này là: làm thế nào để hiểu và áp dụng đúng công nghệ này trong công trình thực tế.

Tất cả ba vấn đề đều giảm xuống là Thuyết định ngôn ngữ tự nhiên. NLI là nhiệm vụ xương sống hỗ trợ kiểm tra thực tế, phân loại không bắn, đánh giá tổng kết và xác minh lấy lại.

> Ba vấn đề này đều kết luận vào lý thuyết ngôn ngữ tự nhiên. NLI là một nhiệm vụ cơ bản của thực tế kiểm tra, phân loại mẫu, phân tích và kiểm tra.

## Khái niệm cốt lõi

> **【中文解读】**Bài viết này giới thiệu các khái niệm và lý thuyết cốt lõi.

**The task.**Với tiền đề `t`và giả thuyết `h`, phân loại mối quan hệ của họ như một trong: liên quan (t nghĩa là h), mâu thuẫn (t mâu thuẫn h), trung lập (không).

> **任务。**给定前提 `t`和假设 `h`,将它们的关系分类为: 含含含 h) 矛盾矛盾t 矛盾 h) 、中性都不是) ∼三分类

**Cross-encoder approach.**Concatenate t và h, cấp thông qua một biến thể, phân loại. được sử dụng cho các ứng dụng chính xác-chẩn đoán. chậm bởi vì bạn chạy mô hình đầy đủ cho mỗi cặp.

> **交叉编码器方法。**拼音 t 和 h,通过变压器,分类――用于准确率关键的应用――慢因为每对运行完整模型――

**Bi-encoder approach.**Mã hóa t và h riêng biệt, so sánh các nhúng (sự tương tự coisin).

> **双编码器方法。**分别编码 t 和 h,比较嵌入 (弦相似度) ⋅检索快但不太准确──

> **【拓展：大语言模型的工程实践】**Từ GPT đến ChatGPT, NLP đã trải qua sự chuyển đổi từ "mỗi nhiệm vụ đào tạo một mô hình" đến "một mô hình giải quyết tất cả các nhiệm vụ". Trong công trình thực tế, việc triển khai LLM cần phải xem xét các vấn đề như: giới hạn token, trì hoãn, chi phí, kiểm tra an toàn, và các vấn đề khác.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) là cấu trúc phổ biến nhất trong ứng dụng AI của doanh nghiệp hiện tại: sẽ truy vấn người dùng trước tiên truy vấn các đoạn tài liệu liên quan, tiếp tục truy vấn kết quả như trên dưới đây cho LLM 生成答案──
```figure
nli-router
```

## Hãy xây dựng nó

> **【拓展：NLP 的多语言挑战】**Trên toàn cầu có hơn 7000 ngôn ngữ, nhưng nghiên cứu về NLP tập trung chủ yếu vào tiếng Anh và một số ít ngôn ngữ.

## Hãy xây dựng nó.

> **【中文解读】**本节通过代码实现核心算法从零――这种" từ đầu"的方式能帮助理解框架背后的原理,遇到问题时不会被黑盒困住――

### Bước 1: Đánh phân loại bằng không bằng NLI

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

tok = AutoTokenizer.from_pretrained("roberta-large-mnli")
model = AutoModelForSequenceClassification.from_pretrained("roberta-large-mnli")

def nli_classify(premise, hypothesis):
    inputs = tok(premise, hypothesis, return_tensors="pt", truncation=True)
    with torch.no_grad():
        logits = model(**inputs).logits[0]
    # 0=contradiction, 1=neutral, 2=entailment
    probs = torch.softmax(logits, dim=-1)
    labels = ["contradiction", "neutral", "entailment"]
    return {labels[i]: probs[i].item() for i in range(3)}

print(nli_classify("A man is playing guitar.", "Someone is making music."))
```

> **【中文解读】**Bài này sẽ cho thấy cách sử dụng một khuôn khổ đã phát triển để nhanh chóng áp dụng công nghệ này. Trong các dự án thực tế, ưu tiên sử dụng khuôn khổ đã được chứng minh để thực hiện.

> **【拓展：Prompt Engineering 与 LLM 应用】**Kỹ thuật nhanh chóng đã trở thành kỹ năng cốt lõi của các kỹ sư NLP. Từ Zero-shot đến Few-shot, từ Chain-of-Thought đến ReAct, các chiến lược khác nhau áp dụng cho các tình huống khác nhau. Trong các dự án thực tế, thiết kế của System提示(System Prompt) ảnh hưởng trực tiếp đến sự ổn định và chất lượng sản xuất của ứng dụng LLM.

## Hãy sử dụng nó để thực hiện

> **【中文解读】**Phần này tập trung vào cách phân phối mô hình như một sản phẩm có thể sử dụng.

NLI sản xuất:

> 生产 NLP 技术:

- **Zero-shot classification:**Mô hình NLI (DeBERTa-v3-lớn-mnli). / 零样本分类:NLI 模型。
- **Fact verification:**NLI mã hóa chéo trên yêu cầu so với bằng chứng. / 事实验证:交叉编码器 NLI。
- **Summary faithfulness:**Kiểm tra từng câu tóm tắt theo nguồn. / 摘摘忠度:检查每个摘摘句子与源。
- **RAG grounding:**Đảm bảo bối cảnh lấy lại hỗ trợ câu trả lời. / RAG 定:验证检索上下文支持答案──

## Chuyển nó đi.

Cứ như `outputs/skill-nli-applications.md`- Có thể là:

> 保存为 `outputs/skill-nli-applications.md`- Có thể là:

```markdown
Given a production need (fact-checking, zero-shot classification, summary evaluation), design the NLI pipeline.
1. Model choice. Cross-encoder (accuracy) or bi-encoder (speed).
2. Input format. Premise-hypothesis pairs.
3. Evaluation. Accuracy on labeled NLI datasets.
```

> **【中文解读】**练题按照 Easy/Medium/Hard 三个难度递进;;建议至少完成中级题;;

## Tập luyện bài tập

1. **Easy.**Sử dụng `roberta-large-mnli`cho phân loại chủ đề bằng không bắn trên 20 câu. / **简单。**Sử dụng `roberta-large-mnli`Đối với 20 câu làm零 mẫu chủ đề phân loại.
2. **Medium.**Xây dựng một kiểm tra độ trung thành tổng kết bằng cách sử dụng NLI. Đánh giá trên CNN / DailyMail. / **中等。**Sử dụng NLI 构建摘要忠实检查器──在 CNN/DailyMail 上评估──
3. **Hard.**So sánh cross-encoder vs bi-encoder NLI để xác minh câu trả lời RAG.**困难。**So sánh bộ lập trình giao thông với bộ lập trình hai NLI sử dụng RAG 答案验证── báo cáo tốc độ và tỷ lệ chính xác cân nhắc──

## Từ khóa  Từ khóa nhanh chóng

| Term / 术语 | What people say / 人们常说的 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| NLI（自然语言推理） | Entailment task / 蕴含任务 | Classify premise-hypothesis pairs as entailment/contradiction/neutral. / 将前提-假设对分类为蕴含/矛盾/中性。 |
| Cross-encoder（交叉编码器） | Joint encoding / 联合编码 | Encode both texts together through the full model. / 通过完整模型联合编码两个文本。 |
| Bi-encoder（双编码器） | Separate encoding / 分离编码 | Encode each text independently, compare embeddings. / 独立编码每个文本，比较嵌入。 |

## Xem thêm 延伸阅读

- [Bowman et al. (2015). SNLI](https://nlp.stanford.edu/pubs/snli_paper.pdf) bộ dữ liệu Stanford NLI. / Stanford NLI 数据集──
- [He et al. (2021). DeBERTa v3](https://arxiv.org/abs/2111.09543) mô hình NLI hiện đại. / 先进 NLI 模型。
