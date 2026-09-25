# Hệ thống trả lời câu hỏi.

> Ba hệ thống hình thành QA hiện đại. Extractive tìm thấy khoảng thời gian. lấy lại tăng cường chúng đất trong tài liệu. Generative sản xuất câu trả lời. Mỗi trợ lý AI hiện đại là một hỗn hợp của ba.
> 三种系统塑造了现代问答――抽取式找到文本片段――检索增强将其定到文档――生成式产生答案――每个现代AI 助手都是三者的混合――

> **【中文解读】**Từ tìm kiếm thông tin đến tạo ra câu trả lời.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 11 (Machine Translation), Phase 5 · 10 (Attention Mechanism) | **前置知识:** Phase 5 · 11 (Machine Translation), Phase 5 · 10 (Attention Mechanism)
**Time:** ~75 minutes | **时间:** ~75 minutes


## Vấn đề  vấn đề giới thiệu

Người dùng gõ "Lần đầu tiên iPhone ra mắt khi nào?" và mong đợi "Ngày 29 tháng 6 năm 2007". Không phải "lịch sử của Apple dài và đa dạng". Không phải "2007" ngồi cách ly mà không có câu. Một câu trả lời trực tiếp, có nền tảng, chính xác.
> Người dùng nhập mục "Khi nào iPhone đầu tiên ra mắt?" 并期望得到 "29 tháng 6 năm 2007."──不是 "lịch sử của Apple là dài và đa dạng. "──不是孤立的"2007" 没有句子上下文──一个直接、有据可依、正确的答案──

> **【中文解读】**Câu hỏi được đặt ra trong phần này là: làm thế nào để hiểu và áp dụng đúng công nghệ này trong công trình thực tế.


Ba kiến trúc đã thống trị QA trong thập kỷ qua.
> Trong thập kỷ qua, ba cấu trúc đã chủ yếu là câu hỏi:

- **Extractive QA.**Với một câu hỏi và một đoạn văn được biết có chứa câu trả lời, tìm các chỉ số bắt đầu và kết thúc của khoảng thời gian trả lời trong đoạn văn.
- **Open-domain QA.**Không có đoạn văn được đưa ra. Nhận đoạn văn liên quan trước, sau đó lấy hoặc tạo ra một câu trả lời. Đây là nền tảng của mọi đường ống dẫn RAG ngày nay.
- **Generative / Closed-book QA.**Một mô hình ngôn ngữ lớn trả lời từ bộ nhớ thông số của nó không có truy xuất nhanh nhất trong suy luận, ít nhất đáng tin cậy trên các sự kiện.
> - **抽取式问答（Extractive QA）。**给定一个问题和已知包含答案的段落, tìm câu trả lời trong段落中的起和结尾索引.
- **开放域问答（Open-domain QA）。**段落未给定──先检查相关段落,然后抽取或生成答案──这是当今每个RAG流水线的基石──
- **生成式/闭卷问答（Generative / Closed-book QA）。**Đại ngôn ngữ mô hình từ ký ức tham số hóa trả lời. Không kiểm tra.

Xu hướng năm 2026 là lai: lấy lại một vài đoạn tốt nhất, sau đó yêu cầu một mô hình tạo ra câu trả lời dựa trên những đoạn đó. Đó là RAG, và bài học 14 bao gồm một nửa chiều sâu về việc lấy lại. Bài học này xây dựng một nửa QA.
> Xu hướng năm 2026 là hỗn hợp: tìm kiếm một vài đoạn tốt nhất, sau đó đưa ra các mô hình để tạo ra các câu trả lời dựa trên những đoạn này.

## Khái niệm cốt lõi

> **【中文解读】**Bài viết này giới thiệu các khái niệm và lý thuyết cốt lõi.


![QA architectures: extractive, retrieval-augmented, generative](../assets/qa.svg)
> ![问答架构：抽取式、检索增强、生成式](../assets/qa.svg)

**Extractive.**Câu hỏi mã hóa và đoạn đường cùng với một biến thể (các bộ phận của BERT). Đào tạo hai đầu tiên dự đoán các chỉ số bắt đầu và kết thúc của câu trả lời.
> **抽取式。**用变压器(BERT 系列) cùng mã hóa vấn đề và段落──训练两个预测答案起始和结束代币索引的头──损失是有效位置交叉──输出是段落中的一个段段──不会幻觉(结构上如此),无法处理段落不能回答问题(结构上如此)──

**Retrieval-augmented (RAG).**Hai giai đoạn, đầu tiên, một chiếc Retriever tìm thấy đỉnh...`k`Các đoạn văn từ một tập thể. Thứ hai, một người đọc (từ hoặc tạo) tạo ra câu trả lời bằng cách sử dụng những đoạn văn đó.
> **检索增强（RAG）。**Hai giai đoạn. Thứ nhất, kiểm tra từ kho chứa các từ khóa tìm thấy trên cùng.`k`段落──第二,阅读器(抽取式或生成式) sử dụng những段落产生答案──检索器-阅读器分离允许各自独立训练和评估──现代RAG thường là một hệ thống xếp hạng nặng giữa hai hệ thống này──

**Generative.**Một LLM chỉ có trình giải mã (GPT, Claude, Llama) trả lời từ các trọng lượng học. Không có bước lấy lại. xuất sắc về kiến thức chung, thảm họa về các sự kiện hiếm hoặc gần đây. Tỷ lệ ảo giác tương phản với tần số thực tế trong dữ liệu trước khi tập luyện.
> **生成式。**仅解码器的 LLM(GPT、Claude、Llama) từ học tập để có được những câu trả lời.

> **【拓展：大语言模型的工程实践】**Từ GPT đến ChatGPT, NLP đã trải qua sự chuyển đổi từ "mỗi nhiệm vụ đào tạo một mô hình" đến "một mô hình giải quyết tất cả các nhiệm vụ". Trong công trình thực tế, việc triển khai LLM cần phải xem xét các vấn đề như: giới hạn token, trì hoãn, chi phí, kiểm tra an toàn, và các vấn đề khác.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) là cấu trúc phổ biến nhất trong ứng dụng AI của doanh nghiệp hiện tại: sẽ truy vấn người dùng trước tiên truy vấn các đoạn tài liệu liên quan, tiếp tục truy vấn kết quả như trên dưới đây cho LLM 生成答案──

> **【拓展：NLP 的多语言挑战】**Trên toàn cầu có hơn 7000 ngôn ngữ, nhưng nghiên cứu về NLP tập trung chủ yếu vào tiếng Anh và một số ít ngôn ngữ.


## Hãy xây dựng nó.

> **【中文解读】**本节通过代码实现核心算法从零――这种" từ đầu"的方式能帮助理解框架背后的原理,遇到问题时不会被黑盒困住――

```figure
qa-span
```

## Hãy xây dựng nó

### Bước 1: QA khai thác với mô hình được đào tạo trước
> `deepset/roberta-base-squad2`Trong SQuAD 2.0 trên đào tạo, chứa câu hỏi không thể trả lời.`question-answering`流水线返回最高分分的片段, ngay cả khi số lượng空分胜出模型的它不自动返回空答案── để có được hành vi "không trả lời" rõ ràng, 流水线调用中传入`handle_impossible_answer=True`:流水线 chỉ có số lượng không gian hơn tất cả các đoạn phân số khi trả về không gian.`score`字段。

```python
from transformers import pipeline

qa = pipeline("question-answering", model="deepset/roberta-base-squad2")

passage = (
    "Apple Inc. released the first iPhone on June 29, 2007. "
    "The device was announced by Steve Jobs at Macworld in January 2007."
)
question = "When was the first iPhone released?"

answer = qa(question=question, context=passage)
print(answer)
```

```python
{'score': 0.98, 'start': 57, 'end': 70, 'answer': 'June 29, 2007'}
```

`deepset/roberta-base-squad2`được đào tạo trên SQuAD 2.0, bao gồm các câu hỏi không có câu trả lời.`question-answering`pipeline trả lại khoảng thời gian ghi điểm cao nhất ngay cả khi điểm số null của mô hình thắng  nó không * không * tự động trả lại câu trả lời trống. Để có được hành vi "không trả lời" rõ ràng, vượt qua `handle_impossible_answer=True`cho cuộc gọi đường ống: đường ống sau đó trả lời trống chỉ khi điểm không vượt quá mỗi điểm span.`score`trường dù sao.
> 两阶段流水线──密检索器(Sentence-BERT) thông qua ngữ义相似度 tìm thấy liên quan段落──抽取式阅读器(RoBERTa-SquAD) từ 合并的顶段落中提取答案片段──适用于小语料库──对于百万级文档语料,使用 FAISS或向量数据库──

### Bước 2: một đường ống tăng cường thu hồi (phác thảo)
> 提示模式 rất quan trọng. 提示模式 rất quan trọng. 提示模式 rất quan trọng. 提示模式很重要. 提示模式很重要. 提示模式很重要. 提示模式很重要. 提示模式很重要. 提示模式很重要. 提示模式很重要. 提示模式很重要. 提示模式很重要. 提示模式很重要. 提示模式很重要. 提示模式很重要. 提示模式很重要. 提示模式很重要. 提示模式很重要. 提示模式很重要. 提示模式很重要. 提示模式很重要. 提示模式很重要. 提示模式很重要. 提示模式很重要. 提示模式很重要. 提示模式很重要. 提示模式很重要. 提示模式很重要. 提示模式很重要. 提示模式很重要.

```python
from sentence_transformers import SentenceTransformer
import numpy as np

encoder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

corpus = [
    "Apple Inc. released the first iPhone on June 29, 2007.",
    "Macworld 2007 featured the iPhone announcement by Steve Jobs.",
    "Android launched in 2008 as Google's mobile operating system.",
    "The first iPod was released in 2001.",
]
corpus_embeddings = encoder.encode(corpus, normalize_embeddings=True)


def retrieve(question, top_k=2):
    q_emb = encoder.encode([question], normalize_embeddings=True)
    sims = (corpus_embeddings @ q_emb.T).squeeze()
    order = np.argsort(-sims)[:top_k]
    return [corpus[i] for i in order]


def answer(question):
    passages = retrieve(question, top_k=2)
    combined = " ".join(passages)
    return qa(question=question, context=combined)


print(answer("When was the first iPhone released?"))
```

Các đoạn đường ống dẫn hai giai đoạn. Density retriever (Sentence-BERT) tìm thấy các đoạn văn liên quan theo sự tương đồng ngữ nghĩa. Extractive reader (RoBERTa-SquAD) kéo khoảng câu trả lời từ các đoạn văn trên kết hợp.
> SQUAD 使用**精确匹配（Exact Match, EM）**和 **token 级 F1**◦ EM là sự phù hợp nghiêm ngặt sau khi kết hợp (小写, loại bỏ dấu chấm, loại bỏ từ) 预测 么精确匹配, 么得到 0♦ F1 在预测和参考的代号重叠上计算,给部分分──两者都低估释义:"29 tháng 6 năm 2007" vs "29 tháng 6 năm 2007" thường đạt 0 EM (序数词破坏归结) nhưng vẫn từ một代号重叠 获得可观的 F1♦

### Bước 3: tạo ra với RAG
> 对于生产问答:

```python
def rag_generate(question, llm):
    passages = retrieve(question, top_k=3)
    prompt = f"""Context:
{chr(10).join('- ' + p for p in passages)}

Question: {question}

Answer using only the context above. If the context does not contain the answer, say "I don't know."
"""
    return llm(prompt)
```

Mô hình prompt là quan trọng. Nói rõ ràng cho mô hình để đặt nền trong bối cảnh và trả lời "Tôi không biết" khi bối cảnh không đủ làm giảm tỷ lệ ảo giác 40-60% so với việc nhắc nhở ngây thơ. Mô hình phức tạp hơn thêm trích dẫn, điểm độ tin cậy và thu hoạch cấu trúc.
> - **答案准确率**(LLM 评判或人工评判, vì chỉ số không nắm bắt ngữ义等价)
- **引用准确率。**引用的段落是否实际支持答案? Sử dụng để tạo các đoạn trích và truy cập giữa các đoạn trích là dễ dàng tự động kiểm tra.
- **拒绝校准。**Khi câu trả lời không có trong đoạn kiểm tra, hệ thống có đúng cách nói "Tôi không biết"? đo tỷ lệ tin tưởng giả ư:
- **检索召回率。**Trước khi đánh giá, kiểm tra đo liệu sẽ đúng đắn nào để đưa vào top...`k`❖阅读器无法修复缺失的段落──

### Bước 4: đánh giá phản ánh thế giới thực
> `RAGAS`专为RAG 系统构建,是2026年发布默认选择――它在不需要黄金参考的情况下从四维度评分:

SQUAD sử dụng **Exact Match (EM)**và **token-level F1**- Tôi không biết. EM là một sự phù hợp nghiêm ngặt sau khi bình thường hóa (bản chữ dưới, dấu chấm thoát, loại bỏ các mục)  hoặc dự đoán phù hợp chính xác hoặc nó ghi điểm 0. F1 được tính toán qua sự chồng chéo giữa dự đoán và tham chiếu và cung cấp tín dụng một phần. Cả hai đoạn phần tín dụng thấp: "Ngày 29 tháng 6 năm 2007" so với "Ngày 29 tháng 6 năm 2007" thường nhận được 0 EM (sự bình thường hóa của sự phá vỡ trật tự) nhưng vẫn kiếm được F1 đáng kể từ các token chồng chéo.
> - **忠实度（Faithfulness）。**Mỗi tuyên bố trong câu trả lời có đến từ các bài kiểm tra trên?
- **答案相关性。**答案是否回应了问题? Bằng cách tạo ra giả thuyết từ câu trả lời và so sánh với vấn đề thực tế để đo lường.
- **上下文精确率。**Trong các khối kiểm tra, có bao nhiêu thực tế liên quan?
- **上下文召回率。**检索集 có chứa tất cả các thông tin cần thiết?

Đối với sản xuất QA:
> 无参考评分让你可以在实时评估生产流量,无需策划黄金答案――在精确匹配指标无用的开放式问题上叠加 LLM 评委――

- **Answer accuracy**(Điều trị của LLM hoặc đánh giá của con người, vì các số liệu không nắm bắt sự tương đương ngữ nghĩa).
- **Citation accuracy.**Bài trích dẫn có thực sự hỗ trợ câu trả lời không? Không có gì khác để tự động kiểm tra với chuỗi phù hợp giữa các trích dẫn được tạo và các đoạn trích dẫn được lấy lại.
- **Refusal calibration.**Khi câu trả lời không nằm trong các đoạn trích được tìm thấy, hệ thống có nói đúng "Tôi không biết" không?
- **Retrieval recall.**Trước khi đánh giá người đọc, hãy đo lường xem người tìm kiếm có được lối đi đúng vào phía trên không.`k`Một người đọc không thể sửa chữa một đoạn văn bị mất.
> `pip install ragas`△ Cụm vào máy kiểm tra của bạn △ đọc máy △ mỗi truy vấn nhận được 4 tiêu chuẩn △ quay lại ⋅ báo cảnh báo △

### RAGAS: khung đánh giá sản xuất năm 2026

`RAGAS`được xây dựng đặc biệt cho các hệ thống RAG và là mặc định vận chuyển vào năm 2026. Nó có bốn chiều mà không cần tham chiếu vàng:

- **Faithfulness.**Mỗi câu hỏi trong câu trả lời có xuất phát từ bối cảnh được lấy lại không?
- **Answer relevance.**Câu trả lời có giải quyết câu hỏi không? được đo bằng cách tạo ra các câu hỏi giả thuyết từ câu trả lời và so sánh với câu hỏi thực.
- **Context precision.**Trong số các mảnh thu hồi, phần nào thực sự có liên quan?
- **Context recall.**Bộ thu hồi có chứa tất cả thông tin cần thiết không?

Đánh giá không tham khảo cho phép bạn đánh giá lưu lượng sản xuất trực tiếp mà không có câu trả lời vàng được chọn. Layer LLM-as-judge trên cùng cho các câu hỏi mở khi métrics phù hợp chính xác là vô dụng.

`pip install ragas`Đưa máy thu hồi + đọc, lấy 4 scalar cho mỗi truy vấn, cảnh báo về sự lùi lại.

> **【中文解读】**Bài này sẽ trình bày cách sử dụng một khung đã phát triển như PyTorch, HuggingFace, và các khác.


> **【拓展：Prompt Engineering 与 LLM 应用】**Kỹ thuật nhanh chóng đã trở thành kỹ năng cốt lõi của các kỹ sư NLP. Từ Zero-shot đến Few-shot, từ Chain-of-Thought đến ReAct, các chiến lược khác nhau áp dụng cho các tình huống khác nhau. Trong các dự án thực tế, thiết kế của System提示(System Prompt) ảnh hưởng trực tiếp đến sự ổn định và chất lượng sản xuất của ứng dụng LLM.

## Hãy sử dụng nó để thực hiện

- Cổ hàng năm 2026.
> 2026 年技术──

| Use case | Recommended |
|---------|-------------|
| Given passage, find answer span | `deepset/roberta-base-squad2` |
| Over a fixed corpus, closed-book not acceptable | RAG: dense retriever + LLM reader |
| Real-time over a document store | RAG with hybrid (BM25 + dense) retriever + reranker (lesson 14) |
| Conversational QA (follow-up questions) | LLM with conversation history + RAG on each turn |
| Highly factual, regulated domains | Extractive over an authoritative corpus; never generative alone |
>  Sử dụng cảnh                                                                                                                                                                                                                                                             
|---------|------|
| 给定段落，找答案片段 | `deepset/roberta-base-squad2` |
| 固定语料上，闭卷不可接受 | RAG：稠密检索器 + LLM 阅读器 |
| 实时文档存储 | RAG 配混合（BM25 + 稠密）检索器 + 重排序器（第 14 课） |
| 对话式问答（追问） | 带对话历史的 LLM + 每轮 RAG |
| 高度事实性、受监管领域 | 在权威语料上的抽取式；永远不要单独用生成式 |

> **【中文解读】**Phần này tập trung vào cách phân phối mô hình như một sản phẩm có thể sử dụng.


Quản lý chất lượng trích xuất đã trở nên không hiện đại vào năm 2026 bởi vì RAG với LLM xử lý nhiều trường hợp hơn. Nó vẫn được đưa ra trong các bối cảnh mà cần trích dẫn theo nghĩa đen: nghiên cứu pháp lý, tuân thủ quy định, công cụ kiểm toán.
> 抽取式问答在2026年不流行,因为带 LLM RAG 处理更多情况――它 vẫn còn trong tình huống cần trích dẫn từng chữ xuất bản:


## Chuyển nó đi.

Cứ như `outputs/skill-qa-architect.md`- Có thể là:
> 保存为 `outputs/skill-qa-architect.md`- Có thể là:

```markdown
---
name: qa-architect
description: Choose QA architecture, retrieval strategy, and evaluation plan.
version: 1.0.0
phase: 5
lesson: 13
tags: [nlp, qa, rag]
---

Given requirements (corpus size, question type, factuality constraint, latency budget), output:

1. Architecture. Extractive, RAG with extractive reader, RAG with generative reader, or closed-book LLM. One-sentence reason.
2. Retriever. None, BM25, dense (name the encoder), or hybrid.
3. Reader. SQuAD-tuned model, LLM by name, or "domain-fine-tuned DistilBERT."
4. Evaluation. EM + F1 for extractive benchmarks; answer accuracy + citation accuracy + refusal calibration for production. Name what you are measuring and how you are measuring it.

Refuse closed-book LLM answers for regulatory or compliance-sensitive questions. Refuse any QA system without a retrieval-recall baseline (you cannot evaluate the reader without knowing the retriever surfaced the right passage). Flag questions that require multi-hop reasoning as needing specialized multi-hop retrievers like HotpotQA-trained systems.
```

> **【中文解读】**练题按照 Easy/Medium/Hard 三个难度递进;;建议至少完成 级别的题目, 级别适合深入研究或面试准备;;


## Tập luyện bài tập

1. **Easy.**Thiết lập đường ống khai thác SQuAD trên 10 đoạn Wikipedia. Làm thủ công 10 câu hỏi. đo số câu trả lời đúng bao nhiêu lần. Bạn nên thấy 7-9 đúng nếu các đoạn và câu hỏi sạch sẽ.
2. **Medium.**Thêm một phân loại từ chối. Khi điểm thu hồi cao nhất dưới ngưỡng (chẳng hạn là 0,3 cosine), trả lại "Tôi không biết" thay vì gọi cho người đọc.
3. **Hard.**Xây dựng một đường ống RAG trên một tập hợp tài liệu 10.000 tùy chọn của bạn. Thực hiện thu thập lai (BM25 + dày) bằng sự hợp nhất RRF (xem bài học 14). đo độ chính xác trả lời với và không có bước lai. Tài liệu loại câu hỏi nào có lợi nhiều nhất.
> 1. **简单。**Trong 10 bài viết trên Wikipedia, các đoạn văn được thiết lập trên SQuAD 抽取式流线――手工设计 10 câu hỏi――测量答案正确率―― nếu đoạn văn và câu hỏi干净, bạn nên thấy 7-9 câu hỏi正确――
2. **中等。**添加拒绝分类器──当最高检索分数低于值(例如 0.3余弦) 当, trả lại "Tôi không biết" thay vì调用阅读器──在留出集上调整值──
3. **困难。**Trong 10 000 文档语料 bạn chọn xây dựng RAG 流水线。 thực hiện kiểm tra hỗn hợp(BM25 + 密) thêm RRF 融合(见第 14 课)。 đo có và không hỗn hợp các bước câu trả lời xác định tỷ lệ── ghi lại những vấn đề loại được hưởng lợi lớn nhất。

> **【中文解读】**Trong 术语表中的"Những gì mọi người nói" vs "Những gì nó thực sự có nghĩa" 区分日常口语和精确技术含义── 在团队协作中,统一术语定义可以避免大量沟通误解──


## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Extractive QA | Find the answer span | Predict start and end indices of the answer within a given passage. |
| Open-domain QA | QA over a corpus | No given passage; must retrieve then answer. |
| RAG | Retrieve then generate | Retrieval-augmented generation. Retriever + reader pipeline. |
| SQuAD | Canonical benchmark | Stanford Question Answering Dataset. EM + F1 metrics. |
| Hallucination | Made-up answer | Reader output not supported by retrieved context. |
| Refusal calibration | Know when to shut up | System correctly says "I don't know" when unable to answer. |
>  Từ ngữ  Mọi người thường nói 
|------|-----------|---------|
| 抽取式问答 | 找答案片段 | 预测给定段落中答案的起始和结束索引。 |
| 开放域问答 | 语料上的问答 | 无给定段落；必须先检索再回答。 |
| RAG | 检索再生成 | 检索增强生成。检索器 + 阅读器流水线。 |
| SQuAD | 经典基准 | 斯坦福问答数据集。EM + F1 指标。 |
| 幻觉 | 编造答案 | 阅读器输出不被检索上下文支持。 |
| 拒绝校准 | 知道何时闭嘴 | 系统在无法回答时正确地说 "I don't know"。 |

> **【中文解读】**延伸阅读 cung cấp các nguồn chất lượng cao cho việc học sâu. Những bài báo và giảng dạy này là tài liệu tham khảo cổ điển trong lĩnh vực này, phù hợp với những người đọc cần hiểu sâu hơn.


## Xem thêm 延伸阅读

- [Rajpurkar et al. (2016). SQuAD: 100,000+ Questions for Machine Comprehension of Text](https://arxiv.org/abs/1606.05250) giấy chuẩn.
- [Karpukhin et al. (2020). Dense Passage Retrieval for Open-Domain QA](https://arxiv.org/abs/2004.04906)DPR, máy thu hồi mật độ của QA.
- [Lewis et al. (2020). Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401) tờ báo đặt tên RAG.
- [Gao et al. (2023). Retrieval-Augmented Generation for Large Language Models: A Survey](https://arxiv.org/abs/2312.10997) khảo sát toàn diện RAG.
> - [Rajpurkar et al. (2016). SQuAD: 100,000+ Questions for Machine Comprehension of Text](https://arxiv.org/abs/1606.05250) 基准论文──
- [Karpukhin et al. (2020). Dense Passage Retrieval for Open-Domain QA](https://arxiv.org/abs/2004.04906) DPR,问答的经典密检索器──
- [Lewis et al. (2020). Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401) 命名 RAG 的论文──
- [Gao et al. (2023). Retrieval-Augmented Generation for Large Language Models: A Survey](https://arxiv.org/abs/2312.10997) 综合 RAG 综述。
