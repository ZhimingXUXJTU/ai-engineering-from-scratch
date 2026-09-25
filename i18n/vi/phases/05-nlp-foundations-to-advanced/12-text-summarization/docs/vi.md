# Bài viết tổng kết 文本摘要

> Hệ thống thu thập thông tin cho bạn biết tài liệu nói gì hệ thống trừu tượng cho bạn biết tác giả có ý gì các nhiệm vụ khác nhau, các bẫy khác nhau
> 抽取式系统告诉你文档说了什么――生成式系统告诉你作者意思―― nhiệm vụ khác nhau, bẫy khác nhau――

> **【中文解读】**抽取式 vs 生成式摘要──

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 02 (BoW + TF-IDF), Phase 5 · 11 (Machine Translation) | **前置知识:** Phase 5 · 02 (BoW + TF-IDF), Phase 5 · 11 (Machine Translation)
**Time:** ~75 minutes | **时间:** ~75 minutes


## Vấn đề  vấn đề giới thiệu

Một bài báo 2,000 từ sẽ được đưa vào nguồn cấp dữ liệu của bạn. Bạn cần 120 từ để nắm bắt nó. Bạn có thể chọn ba câu quan trọng nhất từ bài viết (từ) hoặc viết lại nội dung bằng những từ của riêng bạn (từ). Cả hai đều được gọi là tổng kết.
> Một bài báo 2000 từ xuất hiện trong dòng thông tin của bạn. Bạn cần 120 từ để tổng hợp nó. Bạn có thể chọn từ bài viết ba câu quan trọng nhất (trong bài viết này), hoặc viết lại nội dung của mình (trong bài viết này).

> **【中文解读】**Câu hỏi được đặt ra trong phần này là: làm thế nào để hiểu và áp dụng đúng công nghệ này trong công trình thực tế.


Lưu ý tổng kết trừu tượng là một vấn đề xếp hạng.`k`. Kết quả luôn là ngữ pháp bởi vì nó được nâng lên theo nghĩa đen.
> 抽取式摘要是一个排序问题――给每个句子打分,返回排名 `k`◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎ ◎

Kết luận trừu tượng là một vấn đề phát triển. Một bộ biến đổi tạo ra văn bản mới được điều chỉnh theo đầu vào.
> 生成式摘要是一个生成问题――Tình biến 根据输入产生新文本――输出流且压缩, nhưng có thể产生源中没有事实幻觉――风险是自信的编制――

Bài học này xây dựng cả hai, với chế độ thất bại mỗi người sở hữu.
> 本课构建两者,以及各自拥有的失败模式──

> **【中文解读】**Bài viết này giới thiệu các khái niệm và lý thuyết cốt lõi.


## Khái niệm cốt lõi

![Extractive TextRank vs abstractive transformer](../assets/summarization.svg)
> ![抽取式 TextRank vs 生成式 Transformer](../assets/summarization.svg)

**Extractive.**Hãy xem bài viết như một biểu đồ mà các nút là câu và cạnh là sự tương đồng.**TextRank**(Mihalcea và Tarau, 2004).
> **抽取式（Extractive）。**Để xem bài viết như hình ảnh, các đoạn là câu, bên là sự tương đồng.**TextRank**(Mihalcea và Tarau, 2004):

**Abstractive.**Định chỉnh kỹ thuật mã hóa-định dạng hóa biến đổi (BART, T5, Pegasus) trên cặp tài liệu-số tổng kết. Khi suy luận, mô hình đọc tài liệu và tạo ra tổng kết token-by-token thông qua sự chú ý qua chéo. Pegasus đặc biệt sử dụng mục tiêu trước tập lệnh khoảng cách làm cho nó xuất sắc trong việc tóm tắt mà không cần phải điều chỉnh kỹ lưỡng.
> **生成式（Abstractive）。**Trong tài liệu-摘要对上微调 Transformer 编码器-解码器(BART、T5、Pegasus) ・・・推理时,模型读取文档并通过交叉注意力对代币 生成摘要。Pegasus 特别使用间隔句子预训目标,使其无需太多微调就擅长摘要。

Đánh giá với **ROUGE**(Recall-Oriented Understudy for Gisting Evaluation). ROUGE-1 và ROUGE-2 điểm số đơn và lớn chồng chéo. ROUGE-L điểm số dài nhất phổ biến hậu theo dõi. cao hơn là tốt hơn nhưng 40 ROUGE-L là "tốt" và 50 là "đặc biệt".`rouge-score`gói.
> Sử dụng **ROUGE**(Remember-Oriented Understudy for Gisting Evaluation) 评估──ROUGE-1 和 ROUGE-2 评分一元组和二元组重叠──ROUGE-L 评分最长公共子序列──越高越好,但40 ROUGE-L 是"好",50 是"出色"──每篇论文都报告全部三个──使用`rouge-score`包──

> **【拓展：大语言模型的工程实践】**Từ GPT đến ChatGPT, NLP đã trải qua sự chuyển đổi từ "mỗi nhiệm vụ đào tạo một mô hình" đến "một mô hình giải quyết tất cả các nhiệm vụ". Trong công trình thực tế, việc triển khai LLM cần phải xem xét các vấn đề như: giới hạn token, trì hoãn, chi phí, kiểm tra an toàn, và các vấn đề khác.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) là cấu trúc phổ biến nhất trong ứng dụng AI của doanh nghiệp hiện tại: sẽ truy vấn người dùng trước tiên truy vấn các đoạn tài liệu liên quan, tiếp tục truy vấn kết quả như trên dưới đây cho LLM 生成答案──

> **【拓展：NLP 的多语言挑战】**Trên toàn cầu có hơn 7000 ngôn ngữ, nhưng nghiên cứu về NLP tập trung chủ yếu vào tiếng Anh và một số ít ngôn ngữ.


## Hãy xây dựng nó.

> **【中文解读】**本节通过代码实现核心算法从零――这种" từ đầu"的方式能帮助理解框架背后的原理,遇到问题时不会被黑盒困住――

```figure
summarize-collapse
```

## Hãy xây dựng nó

### Bước 1: TextRank (tài trừu tượng)
> 两件事值得注意──相似度函数 sử dụng từ so sánh đối với số hóa, đây là biến thể gốc của TextRank──TF-IDF 向量的余弦相似度也行──阻尼因子 0.85 和代次数是PageRank's默认值──

```python
import math
import re
from collections import Counter


def sentence_split(text):
    return re.split(r"(?<=[.!?])\s+", text.strip())


def similarity(s1, s2):
    w1 = Counter(s1.lower().split())
    w2 = Counter(s2.lower().split())
    intersection = sum((w1 & w2).values())
    denom = math.log(len(w1) + 1) + math.log(len(w2) + 1)
    if denom == 0:
        return 0.0
    return intersection / denom


def textrank(text, top_k=3, damping=0.85, iterations=50, epsilon=1e-4):
    sentences = sentence_split(text)
    n = len(sentences)
    if n <= top_k:
        return sentences

    sim = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                sim[i][j] = similarity(sentences[i], sentences[j])

    scores = [1.0] * n
    for _ in range(iterations):
        new_scores = [1 - damping] * n
        for i in range(n):
            total_out = sum(sim[i]) or 1e-9
            for j in range(n):
                if sim[i][j] > 0:
                    new_scores[j] += damping * sim[i][j] / total_out * scores[i]
        if max(abs(s - ns) for s, ns in zip(scores, new_scores)) < epsilon:
            scores = new_scores
            break
        scores = new_scores

    ranked = sorted(range(n), key=lambda k: scores[k], reverse=True)[:top_k]
    ranked.sort()
    return [sentences[i] for i in ranked]
```

Hai điều đáng đặt tên. chức năng tương đồng sử dụng log-normalized word overlap, đó là biến thể TextRank gốc. Cosine của các vector TF-IDF cũng hoạt động.
> BART-big-CNN trên CNN/DailyMail 语料微调──开箱即用产生新闻风格摘要── đối với các lĩnh vực khác, sử dụng đối ứng Pegasus 检查点或在目标数据上微调──

### Bước 2: trừu tượng với BART
> 始终使用词干提取──没有它, "running" 和 "run" 被视为不同的词,ROUGE 会低估──

```python
from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

article = """(long news article text)"""

summary = summarizer(article, max_length=120, min_length=60, do_sample=False)
print(summary[0]["summary_text"])
```

BART-big-CNN được điều chỉnh tốt trên CNN / DailyMail corpus. Nó tạo ra các bản tóm tắt theo kiểu tin tức ra khỏi hộp. Đối với các lĩnh vực khác (biện luận khoa học, đối thoại, pháp lý), sử dụng điểm kiểm soát Pegasus tương ứng hoặc điều chỉnh tốt dữ liệu mục tiêu của bạn.
> ROUGE đã là chỉ số tổng hợp chính trong hai thập kỷ qua, nhưng vào năm 2026 chỉ dựa vào nó đã không đủ.

### Bước 3: Đánh giá ROUGE
> - **BERTScore**(上下文嵌入相似度) được quan tâm vào năm 2023, hiện nay hầu hết các bài luận trích dẫn đều được kết hợp với ROUGE một báo cáo.
- **BARTScore**Sẽ đánh giá xem như tạo ra: thông qua dự kiến đào tạo BART                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
- **MoverScore**(上下文嵌入上的推土机距离) đạt đỉnh điểm trong Kỷ nguyên tổng thể năm 2025, vì nó nắm bắt ngữ nghĩa hơn so với ROUGE tốt hơn.
- **FactCC**和**基于 QA 的事实性检查**Trong năm 2021-2023 rất thường thấy, hiện thường được **G-Eval**(một loại GPT-4 提示链, sử dụng chuỗi hình thức suy nghĩ về đánh giá连贯性、一致性、流性和相关性) thay thế:
- **G-Eval**Và các phương pháp đánh giá LLM tương tự trong việc đánh giá tiêu chuẩn được thiết kế tốt có khoảng 80% đồng ý với phán quyết của con người.

```python
from rouge_score import rouge_scorer

scorer = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=True)
scores = scorer.score(reference_summary, generated_summary)
print({k: round(v.fmeasure, 3) for k, v in scores.items()})
```

Không có nó, "running" và "run" được tính là từ khác nhau và ROUGE được tính dưới.
> 产品建议: báo cáo ROUGE-L dùng để để lại so sánh, BERTScore dùng để ngữ nghĩa chồng lên, G-Eval dùng để liên tục và thực tế.

### Beyond ROUGE (2026 tổng kết eval)
> Các bản tóm tắt được tạo ra dễ dàng tạo ra ảo giác. Nguy cơ ảo giác của bản tóm tắt được rút ra thấp hơn nhiều, vì đầu ra được rút ra từ nguồn từ từ từ từ, mặc dù nếu các câu nguồn được tách ra khỏi văn bản sau, quá khứ hoặc không có thứ tự, chúng vẫn có thể bị sai lầm. Đây là lý do chính khiến hệ thống sản xuất vẫn thích cách rút ra về nội dung liên quan đến quy định.

ROUGE đã là chỉ số tổng hợp thống trị trong hai mươi năm và nó không đủ riêng vào năm 2026. Một phân tích meta quy mô lớn của các bài báo NLG cho thấy:
> 需要命名的幻觉类型:

- **BERTScore**(sự tương đồng nhúng ngữ cảnh) đã có được sự nổi bật đến năm 2023 và hiện được báo cáo cùng với ROUGE trong hầu hết các bài báo tóm tắt.
- **BARTScore**xử lý đánh giá như thế hệ: đánh giá tổng kết bằng cách xác định khả năng một BART được đào tạo trước đã phân bổ nó với nguồn gốc.
- **MoverScore**(Earth Mover's Distance over contextual embeddings) đạt vị trí hàng đầu trong điểm tham khảo tổng hợp năm 2025 vì nó nắm bắt sự chồng chéo ngữ học tốt hơn ROUGE.
- **FactCC**và **QA-based faithfulness**được phổ biến từ năm 2021 đến 2023, bây giờ thường được thay thế bởi **G-Eval**(một chuỗi GPT-4 báo động đánh giá sự liên kết, nhất quán, thông suốt, liên quan đến lý luận chuỗi suy nghĩ).
- **G-Eval**và các cách tiếp cận LLM- thẩm phán tương tự với phán đoán của con người ~ 80% thời gian khi các rubric được thiết kế tốt.
> - **实体替换。**源说"John Smith"―摘要说"John Brown"―
- **数字漂移。**源说 "25,000"―摘要说"25 triệu"―
- **极性翻转。**源说 "đánh giá lời đề nghị"―摘要说 "đánh giá lời đề nghị"―
- **事实编造。**源没有提到CEO.摘要说CEO 批准了.

Lời khuyên sản xuất: báo cáo ROUGE-L để so sánh truyền thống, BERTScore để chồng chéo ngữ nghĩa, G-Eval để phù hợp và tính thực tế.
> Phương pháp đánh giá hiệu quả:

### Bước 4: vấn đề thực tế
> - **FactCC。**Trong các câu nguồn và câu tóm tắt, các câu có liên quan đến các thứ hai được đào tạo.
- **基于 QA 的事实性检查。**Đối với QA 模型问源有答题――如果摘要支持不同的答案,标记――
- **实体级 F1。**So sánh nguồn với vật thể có tên trong bản tóm tắt.

Các bản tóm tắt trừu tượng có xu hướng ảo giác. Các bản tóm tắt trừu tượng có nguy cơ ảo giác thấp hơn nhiều vì sản phẩm được gỡ bỏ từ nguồn, mặc dù chúng vẫn có thể gây hiểu lầm nếu các câu nguồn bị giải ngữ cảnh, lỗi thời hoặc trích dẫn không phù hợp. Đây là lý do duy nhất khiến các hệ thống sản xuất vẫn thích các phương pháp trừu tượng cho nội dung phù hợp.
> Đối với nội dung thực tế quan trọng đối với người dùng (khán giả, y tế, luật, tài chính), việc rút ra là một lựa chọn mặc định an toàn hơn.

Các loại ảo giác để đặt tên:

- **Entity swap.**Nguồn nói "John Smith". Tổng kết nói "John Brown".
- **Number drift.**Nguồn nói "25,000". Tổng kết nói "25 triệu".
- **Polarity flip.**Nguồn tin nói "đã từ chối lời đề nghị".
- **Fact invention.**Nguồn không đề cập đến CEO.

Các phương pháp đánh giá cho công việc này:

- **FactCC.**Một phân loại nhị phân được đào tạo về liên quan giữa câu nguồn và câu tóm tắt.
- **QA-based factuality.**Hãy hỏi một câu hỏi mô hình QA có câu trả lời trong nguồn. Nếu bản tóm tắt hỗ trợ các câu trả lời khác nhau, hãy đánh dấu.
- **Entity-level F1.**So sánh các thực thể được đặt tên trong nguồn và tổng kết.

Đối với bất cứ thứ gì đối mặt với người dùng mà thực tế là quan trọng (tin tức, y tế, pháp lý, tài chính), trích xuất là mặc định an toàn hơn.

> **【中文解读】**Bài này sẽ trình bày cách sử dụng một khung đã phát triển như PyTorch, HuggingFace, và các khác.


> **【拓展：Prompt Engineering 与 LLM 应用】**Kỹ thuật nhanh chóng đã trở thành kỹ năng cốt lõi của các kỹ sư NLP. Từ Zero-shot đến Few-shot, từ Chain-of-Thought đến ReAct, các chiến lược khác nhau áp dụng cho các tình huống khác nhau. Trong các dự án thực tế, thiết kế của System提示(System Prompt) ảnh hưởng trực tiếp đến sự ổn định và chất lượng sản xuất của ứng dụng LLM.

## Hãy sử dụng nó để thực hiện

Số 2026:
> 2026 年技术:

| Use case | Recommended |
|---------|-------------|
| News, 3-5 sentence summary, English | `facebook/bart-large-cnn` |
| Scientific papers | `google/pegasus-pubmed` or a tuned T5 |
| Multi-document, long-form | Any LLM with 32k+ context, prompted |
| Dialog summarization | `philschmid/bart-large-cnn-samsum` |
| Extractive, low hallucination risk by construction | TextRank or `sumy`'s LSA / LexRank |
>  Sử dụng cảnh                                                                                                                                                                                                                                                             
|---------|------|
| 新闻，3-5 句摘要，英语 | `facebook/bart-large-cnn` |
| 科学论文 | `google/pegasus-pubmed` 或微调的 T5 |
| 多文档，长文 | 任何 32k+ 上下文的 LLM，提示 |
| 对话摘要 | `philschmid/bart-large-cnn-samsum` |
| 抽取式，结构性低幻觉风险 | TextRank 或 `sumy` 的 LSA / LexRank |

> **【中文解读】**Phần này tập trung vào cách phân phối mô hình như một sản phẩm có thể sử dụng.


LLM có bối cảnh dài thường đánh bại các mô hình chuyên môn vào năm 2026 khi tính toán không phải là một hạn chế.
> Năm 2026 trong toán không bị ràng buộc, LLM thường vượt quá mô hình đặc biệt.


## Chuyển nó đi.

Cứ như `outputs/skill-summary-picker.md`- Có thể là:
> 保存为 `outputs/skill-summary-picker.md`- Có thể là:

```markdown
---
name: summary-picker
description: Pick extractive or abstractive, named library, factuality check.
version: 1.0.0
phase: 5
lesson: 12
tags: [nlp, summarization]
---

Given a task (document type, compliance requirement, length, compute budget), output:

1. Approach. Extractive or abstractive. Explain in one sentence why.
2. Starting model / library. Name it. `sumy.TextRankSummarizer`, `facebook/bart-large-cnn`, `google/pegasus-pubmed`, or an LLM prompt.
3. Evaluation plan. ROUGE-1, ROUGE-2, ROUGE-L (use rouge-score with stemming). Plus factuality check if abstractive.
4. One failure mode to probe. Entity swap is the most common in abstractive news summarization; flag samples where source entities do not appear in summary.

> **【中文解读】** 练习题按照 Easy/Medium/Hard 三个难度递进。建议至少完成 Medium 级别的题目，Hard 级别适合深入研究或面试准备。


Refuse abstractive summarization for medical, legal, financial, or regulated content without a factuality gate. Flag input over the model's context window as needing chunked map-reduce summarization (not just truncation).
```

## Tập luyện bài tập

1. **Easy.**Đánh giá TextRank trên 5 bài báo tin tức. So sánh 3 câu đầu với một bản tóm tắt tham khảo. đo ROUGE-L. Bạn nên thấy 30-45 ROUGE-L trên các bài báo kiểu CNN / DailyMail.
2. **Medium.**Thực hiện thực tế cấp thực thể: trích xuất các thực thể được đặt tên từ nguồn và tổng kết (spaCy), thu hồi tính toán các thực thể nguồn trong tổng kết và độ chính xác của các thực thể tổng kết so với nguồn. Độ chính xác cao và độ thu hồi thấp có nghĩa là an toàn nhưng ngắn gọn; độ chính xác thấp có nghĩa là các thực thể ảo giác.
3. **Hard.**So sánh BART-chủ-CNN với LLM (Claude hoặc GPT-4) trên 50 bài báo CNN/DailyMail. báo cáo ROUGE-L, tính thực tế (bằng tổ chức F1), và chi phí cho mỗi bản tóm tắt. Tài liệu nơi mỗi người thắng.
> 1. **简单。**Trong 5 bài báo trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết trên bài viết
2. **中等。**实现实体级事实性: từ nguồn và摘要中提取命名实体(spaCy), tính toán nguồn thực thể trong摘要召唤率和摘要实体对源的精确率──高精确率低召唤率意味着安全但简略;低精确率意味着幻觉实体──
3. **困难。**Trong 50 bài viết CNN/DailyMail 文章上比较 BART-big-CNN với LLM(Claude hoặc GPT-4) ―― báo cáo ROUGE-L、事实性(按实体 F1) và chi phí của mỗi bản tóm tắt──记录各自胜利场景──

> **【中文解读】**Trong 术语表中的"Những gì mọi người nói" vs "Những gì nó thực sự có nghĩa" 区分日常口语和精确技术含义── 在团队协作中,统一术语定义可以避免大量沟通误解──


## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Extractive | Pick sentences | Return sentences verbatim from the source. Never hallucinates. |
| Abstractive | Rewrite | Generate new text conditioned on source. Can hallucinate. |
| ROUGE | Summary metric | N-gram / LCS overlap between system output and reference. |
| TextRank | Graph-based extractive | PageRank over sentence similarity graph. |
| Factuality | Is it right | Whether summary claims are supported by the source. |
| Hallucination | Made-up content | Content in the summary that the source does not support. |
>  Từ ngữ  Mọi người thường nói 
|------|-----------|---------|
| 抽取式 | 选取句子 | 从源中逐字返回句子。不会幻觉。 |
| 生成式 | 重写 | 根据源生成新文本。可能幻觉。 |
| ROUGE | 摘要指标 | 系统输出与参考之间的 n-gram / LCS 重叠。 |
| TextRank | 基于图的抽取式 | 句子相似度图上的 PageRank。 |
| 事实性 | 对不对 | 摘要声明是否被源支持。 |
| 幻觉 | 编造内容 | 摘要中源不支持的内容。 |

> **【中文解读】**延伸阅读 cung cấp các nguồn chất lượng cao cho việc học sâu. Những bài báo và giảng dạy này là tài liệu tham khảo cổ điển trong lĩnh vực này, phù hợp với những người đọc cần hiểu sâu hơn.


## Xem thêm 延伸阅读

- [Mihalcea and Tarau (2004). TextRank: Bringing Order into Texts](https://aclanthology.org/W04-3252/) giấy khai thác kinh điển.
- [Lewis et al. (2019). BART: Denoising Sequence-to-Sequence Pre-training](https://arxiv.org/abs/1910.13461) BART giấy.
- [Zhang et al. (2019). PEGASUS: Pre-training with Extracted Gap-sentences](https://arxiv.org/abs/1912.08777) Pegasus và mục tiêu câu không có dấu hiệu.
- [Lin (2004). ROUGE: A Package for Automatic Evaluation of Summaries](https://aclanthology.org/W04-1013/) BÁC HN ĐH.
- [Maynez et al. (2020). On Faithfulness and Factuality in Abstractive Summarization](https://arxiv.org/abs/2005.00661) giấy thực tế cảnh quan.
> - [Mihalcea and Tarau (2004). TextRank: Bringing Order into Texts](https://aclanthology.org/W04-3252/) 抽取式经典论文──
- [Lewis et al. (2019). BART: Denoising Sequence-to-Sequence Pre-training](https://arxiv.org/abs/1910.13461) BART 论文。
- [Zhang et al. (2019). PEGASUS: Pre-training with Extracted Gap-sentences](https://arxiv.org/abs/1912.08777) Pegasus 和间隔句子目标──
- [Lin (2004). ROUGE: A Package for Automatic Evaluation of Summaries](https://aclanthology.org/W04-1013/) ROUGE 论文。
- [Maynez et al. (2020). On Faithfulness and Factuality in Abstractive Summarization](https://arxiv.org/abs/2005.00661) 事实性全景论文──
