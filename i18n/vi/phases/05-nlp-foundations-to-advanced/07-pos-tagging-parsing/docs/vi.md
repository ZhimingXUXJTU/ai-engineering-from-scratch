# POS Tagging và Syntactic Parsing 词性标注与句法分析

> ngữ pháp đã không còn thời trang trong một thời gian, sau đó mỗi LLM cần phải xác nhận việc khai thác có cấu trúc, và nó trở lại.
> 语法 từng không phổ biến. Sau đó mỗi LLM 流水线都需要验证结构化抽取, nó lại trở lại.

> **【中文解读】**给每个词标注词性,分析句子的语法结构──

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 01 (Text Processing), Phase 2 · 14 (Naive Bayes) | **前置知识:** Phase 5 · 01（文本处理），Phase 2 · 14（朴素贝叶斯）
**Time:** ~45 minutes | **时间:** ~45 分钟

## Vấn đề  vấn đề giới thiệu

Bài học 01 hứa rằng việc làm lemmatization cần một phần của bài phát biểu mà không biết.`running`là động từ, một lemmatizer không thể giảm nó xuống `run`Không biết`better`là một từ đặc tính, nó không thể giảm xuống `good`- Tôi không biết.

> 第01 课 承诺过词形还原需要词性标注──不知道 `running`是动词,词形还原器无法将其恢复为 `run`✿ không biết ✿`better`                                                                                                                                                                                                                                                              `good`

Lời hứa đó che giấu một lĩnh vực phụ. Việc gắn thẻ phần của bài phát biểu gán các danh mục ngữ pháp. Phân tích tổng hợp phục hồi cấu trúc cây của câu: từ nào sửa đổi cái nào, động từ nào cai trị lập luận nào. NLP cổ điển dành hai mươi năm để tinh chế cả hai. Sau đó học sâu đã đổ chúng thành một nhiệm vụ phân loại token trên đỉnh của một biến thể được đào tạo trước, và cộng đồng nghiên cứu chuyển tiếp.

> Đó là một cam kết đằng sau ẩn chứa một toàn bộ lĩnh vực nhỏ. Từ ngữ phân phối phân bố ngôn ngữ.

Không phải cộng đồng ứng dụng. Mỗi đường ống khai thác cấu trúc vẫn sử dụng cây POS và cây phụ thuộc dưới nắp. JSON được tạo bằng LLM được xác nhận chống lại các hạn chế ngữ pháp. Hệ thống trả lời câu hỏi phân hủy các truy vấn bằng cách sử dụng phân tích phụ thuộc. Các nhà đánh giá chất lượng dịch thuật máy kiểm tra sự sắp xếp của cây phân tích.

> 应用界没有──每个结构化抽取流水线仍在底层使用POS 和依赖树──LLM 生成的JSON 会根据语法约束进行验证──问答系统使用依赖分析来分解查询──机器翻译质量评估器检查分析树的对齐──

Bài học này giới thiệu các thẻ, đường cơ sở, và điểm bạn ngừng thực hiện từ đầu và gọi spaCy.

> Ưu điểm để hiểu.                                                                                                                                                                                                                                                            

## Khái niệm cốt lõi

> **【中文解读】**Bài viết này giới thiệu các khái niệm và lý thuyết cốt lõi.

**POS tagging**Đánh dấu mỗi biểu tượng với một danh mục ngữ pháp.**Penn Treebank (PTB)**Tagset là mặc định tiếng Anh. 36 thẻ với sự khác biệt người đọc thường thấy khó khăn: `NN`singular noun, `NNS`danh từ đa số, `NNP`tự danh nghĩa đơn vị, `VBD`động từ quá khứ, `VBZ`động từ 3rd person singular present, và như vậy.**Universal Dependencies (UD)**Tagset là thô hơn (17 thẻ) và ngôn ngữ-người ngộ; nó trở thành mặc định cho công việc xuyên ngôn ngữ.

> **词性标注（POS Tagging）**Đối với mỗi biểu tượng 标注语法类别。**Penn Treebank (PTB)**标签集 là một lựa chọn mặc định của tiếng Anh.`NN`单数名词、`NNS`复数名词`NNP`专名词单数`VBD`动词过去时,`VBZ`动词第三人称单数现在时等等等──**通用依存（Universal Dependencies, UD）**标签集更粗(17 个标签) và không liên quan đến ngôn ngữ; nó đã trở thành lựa chọn mặc định của việc làm trên khắp các ngôn ngữ.

```
The/DET cats/NOUN were/AUX running/VERB at/ADP 3pm/NOUN ./PUNCT
```

**Syntactic parsing**tạo ra một cây. Hai phong cách chính:

> **句法分析（Syntactic Parsing）**产生一棵树──两种主要风格:

- **Constituency parsing.**Các cụm từ danh nghĩa, cụm từ động từ, cụm từ tiền định tổ bên trong nhau.
  **成分分析（Constituency Parsing）。**Nên từ ngắn gọn, động từ ngắn gọn, từ ngắn gọn, từ ngắn gọn, từ ngắn gọn, từ ngắn gọn, từ ngắn gọn, từ ngắn gọn, từ ngắn gọn, từ ngắn gọn, từ ngắn gọn, từ ngắn gọn, từ ngắn gọn, từ ngắn gọn, từ ngắn gọn, từ ngắn gọn, từ ngắn gọn, từ ngắn gọn, từ ngắn gọn, từ ngắn gọn, từ ngắn gọn, từ ngắn gọn, từ ngắn gọn, từ ngắn gọn, từ ngắn gọn, từ ngắn gọn, từ ngắn gọn, từ nhỏ, từ nhỏ, từ nhỏ, từ nhỏ, từ nhỏ, từ nhỏ, từ nhỏ, từ nhỏ, từ nhỏ, từ nhỏ, từ nhỏ, từ nhỏ, từ nhỏ, từ nhỏ, từ nhỏ, từ nhỏ, từ nhỏ, từ nhỏ, từ nhỏ, từ nhỏ, từ nhỏ, từ nhỏ, từ nhỏ, từ nhỏ, từ nhỏ, từ nhỏ, từ nhỏ, từ nhỏ, từ nhỏ, từ nhỏ, từ nhỏ, từ nhỏ, từ nhỏ, từ nhỏ, từ nhỏ, từ nhỏ, từ nhỏ, đến đến đến đến mức, từ nhỏ, từ nhỏ, từ nhỏ, từ nhỏ, từ nhỏ, đến đến đến đến mức, từ nhỏ, đến đến mức, đến mức có có có có có có thể có thể có thể có thể có thể có thể có thể có thể có thể có thể có thể có thể có thể có thể có thể có thể có thể có thể có thể có thể có thể có thể có thể có thể có thể có thể có thể có thể có thể có thể có thể có thể có thể có thể có thể có thể có thể có thể có thể có thể có thể có thể có thể có thể có thể có thể có thể có thể có thể có thể có thể có thể có thể có thể có thể có thể có thể.
- **Dependency parsing.**Mỗi từ có một từ đầu duy nhất mà nó phụ thuộc vào, được dán nhãn với một mối quan hệ ngữ pháp.
  **依存分析（Dependency Parsing）。**Mỗi từ có một từ trung tâm, biểu thị ngữ pháp quan hệ.

Phân tích phụ thuộc đã giành chiến thắng trong những năm 2010 bởi vì nó tổng quát rõ ràng qua các ngôn ngữ, đặc biệt là các ngôn ngữ tự do.

> 依赖分析在2010年代胜出, vì nó跨语言泛化更干净, đặc biệt là自由语序语言.

```
running is ROOT
cats is nsubj of running
were is aux of running
at is prep of running
3pm is pobj of at
```

> **【拓展：大语言模型的工程实践】**Từ GPT đến ChatGPT, NLP đã trải qua sự chuyển đổi từ "mỗi nhiệm vụ đào tạo một mô hình" đến "một mô hình giải quyết tất cả các nhiệm vụ". Trong công trình thực tế, việc triển khai LLM cần phải xem xét các vấn đề như: giới hạn token, trì hoãn, chi phí, kiểm tra an toàn, và các vấn đề khác.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) là cấu trúc phổ biến nhất trong ứng dụng AI của doanh nghiệp hiện tại: sẽ truy vấn người dùng trước tiên truy vấn các đoạn tài liệu liên quan, tiếp tục truy vấn kết quả như trên dưới đây cho LLM 生成答案──

> **【拓展：NLP 的多语言挑战】**Trên toàn cầu có hơn 7000 ngôn ngữ, nhưng nghiên cứu về NLP tập trung chủ yếu vào tiếng Anh và một số ít ngôn ngữ.

## Hãy xây dựng nó.

> **【中文解读】**本节通过代码实现核心算法从零――这种" từ đầu"的方式能帮助理解框架背后的原理,遇到问题时不会被黑盒困住――
```figure
pos-tagger
```

```figure
dependency-arcs
```

## Hãy xây dựng nó

### Bước 1: Tỷ lệ cơ bản thẻ thường xuyên nhất

Đánh dấu POS ngu ngốc nhất có thể làm việc.

>  Nhưng dùng để đánh dấu POS                                                                                                                                                                                                                                                           

```python
from collections import Counter, defaultdict


def train_mft(train_examples):
    word_tag_counts = defaultdict(Counter)
    all_tags = Counter()
    for tokens, tags in train_examples:
        for token, tag in zip(tokens, tags):
            word_tag_counts[token.lower()][tag] += 1
            all_tags[tag] += 1
    word_best = {w: c.most_common(1)[0][0] for w, c in word_tag_counts.items()}
    default_tag = all_tags.most_common(1)[0][0]
    return word_best, default_tag


def predict_mft(tokens, word_best, default_tag):
    return [word_best.get(t.lower(), default_tag) for t in tokens]
```

Trên cơ thể Brown, đường cơ sở này đạt độ chính xác khoảng 85%.

> Trong bộ 语料 Brown, đường nét này đạt được tỷ lệ chính xác khoảng 85%. Không tốt, nhưng đây là bất kỳ mô hình nghiêm ngặt nào không nên thấp hơn đường nét.

### Bước 2: Bigram HMM Tagger

Mô hình xác suất chung của chuỗi:

> 建模序列的联合概率:

```
P(tags, words) = prod P(tag_i | tag_{i-1}) * P(word_i | tag_i)
```

Hai bảng: xác suất chuyển tiếp (tag cho thẻ trước), xác suất phát thải (tag cho từ).

> 两个表:转移概率 (转移概率)  发射概率 (发射概率)  发射概率 (发射概率)  发射概率 (发射概率)  发射概率 (发射概率)  发射概率 (发射概率)  发射概率 (发射概率)  发射概率 (发射概率)  发射概率 (发射概率)  发射概率 (发射概率)  发射概率 (发射概率)  发射概率 (发射概率)  发射概率 (发射概率)  发射概率 (发射概率)  发射概率 (发射概率)  发射概率 (发射概率)  发射概率 (发射概率)  发射概率 (发射概率)  发射概率 (发射概率)  发射概率)  发射概率 (发射概率) 发射概率 (发射概率) 发射概率) 发射概率 (发射概率) 发射概率) 发射概率 (发射概率) 发射概率) 发射概率 (发射概率) 发射率 (发射率) 发射率) 发射率 (发射率) 发射率 (发射率) 发射率)

```python
import math


def train_hmm(train_examples, alpha=0.01):
    transitions = defaultdict(Counter)
    emissions = defaultdict(Counter)
    tags = set()
    vocab = set()

    for tokens, ts in train_examples:
        prev = "<BOS>"
        for token, tag in zip(tokens, ts):
            transitions[prev][tag] += 1
            emissions[tag][token.lower()] += 1
            tags.add(tag)
            vocab.add(token.lower())
            prev = tag
        transitions[prev]["<EOS>"] += 1

    return transitions, emissions, tags, vocab


def log_prob(table, given, key, smooth_denom, alpha):
    return math.log((table[given].get(key, 0) + alpha) / smooth_denom)


def viterbi(tokens, transitions, emissions, tags, vocab, alpha=0.01):
    tags_list = list(tags)
    n = len(tokens)
    V = [[0.0] * len(tags_list) for _ in range(n)]
    back = [[0] * len(tags_list) for _ in range(n)]

    for j, tag in enumerate(tags_list):
        em_denom = sum(emissions[tag].values()) + alpha * (len(vocab) + 1)
        tr_denom = sum(transitions["<BOS>"].values()) + alpha * (len(tags_list) + 1)
        tr = log_prob(transitions, "<BOS>", tag, tr_denom, alpha)
        em = log_prob(emissions, tag, tokens[0].lower(), em_denom, alpha)
        V[0][j] = tr + em
        back[0][j] = 0

    for i in range(1, n):
        for j, tag in enumerate(tags_list):
            em_denom = sum(emissions[tag].values()) + alpha * (len(vocab) + 1)
            em = log_prob(emissions, tag, tokens[i].lower(), em_denom, alpha)
            best_prev = 0
            best_score = -1e30
            for k, prev_tag in enumerate(tags_list):
                tr_denom = sum(transitions[prev_tag].values()) + alpha * (len(tags_list) + 1)
                tr = log_prob(transitions, prev_tag, tag, tr_denom, alpha)
                score = V[i - 1][k] + tr + em
                if score > best_score:
                    best_score = score
                    best_prev = k
            V[i][j] = best_score
            back[i][j] = best_prev

    last_best = max(range(len(tags_list)), key=lambda j: V[n - 1][j])
    path = [last_best]
    for i in range(n - 1, 0, -1):
        path.append(back[i][path[-1]])
    return [tags_list[j] for j in reversed(path)]
```

Bigram HMM trên Brown đạt độ chính xác ~ 93%.`DET NOUN`là phổ biến và `NOUN DET`là hiếm.

> Trong Brown 语料库上二元组 HMM  đạt khoảng 93% tỷ lệ chính xác  Từ 85% đến 93% nhảy từ tỷ lệ chuyển động 模型学到`DET NOUN`là thường thấy và`NOUN DET`Đó là điều hiếm gặp.

### Bước 3: tại sao các tagger hiện đại đánh bại điều này

Chuyển đổi + khả năng phát thải là địa phương.`saw`là một từ trong "Tôi mua một cây đeo" nhưng là một động từ trong "Tôi đã xem phim". Một CRF với các tính năng tùy tiện (đối hậu, hình chữ, từ trước và sau, từ chính nó) đạt ~97%. Một BiLSTM-CRF hoặc biến thể đạt ~98%+.

> 转移 + 发射概率 là ở một địa điểm. Chúng không thể bắt được.`saw`Trong "Tôi mua một cây cưa" trong đó có từ danh nhưng trong "Tôi xem phim" trong đó có từ động.

Các nhà ghi chú con người đồng ý khoảng 97% thời gian trên Penn Treebank.

> Các nhà đánh dấu con người đã đạt được sự đồng thuận trong khoảng 97% thời gian trên Penn Treebank. Hơn 98% mô hình có thể đã được phù hợp với các tập hợp thử nghiệm.

### Bước 4: bản phác thảo phân tích phụ thuộc

Việc phân tích phụ thuộc hoàn toàn từ đầu là không có phạm vi; việc xử lý sách giáo khoa kinh điển là ở Jurafsky và Martin.

> Từ zero thực hiện toàn bộ phụ thuộc phân tích vượt ra ngoài phạm vi; kinh điển của các giáo khoa xử lý xem Jurafsky và Martin.

- **Transition-based**Các parsers (tham dự arc, arc-standard) hoạt động giống như một trình phân tích giảm chuyển: chúng đọc token, chuyển chúng vào một đống, và áp dụng các hành động giảm tạo cung.
  **基于转移的**解析器(arc-eager、arc-standard) như chuyển vào-归约解析器一样工作:读进代币,移进到上,应用创建弧的归约动作──贪解码很快──经典实现是MaltParser──现代神经版本:Chen 和 Manning 的基于转移的解析器──
- **Graph-based**Các parsers (định thuật của Eisner, Dozat-Manning biaffine) ghi điểm mỗi cạnh phụ thuộc vào đầu có thể và chọn cây trải dài tối đa.
  **基于图的**解析器(Eisner 算法、Dozat-Manning 双仿射) đối với mỗi khả năng phụ thuộc vào đầu 边打分, chọn tạo lớn nhất cây.

Đối với hầu hết các công việc được áp dụng, gọi spaCy:

>  Đối với hầu hết các ứng dụng,调用 spaceCy:

```python
import spacy

nlp = spacy.load("en_core_web_sm")
doc = nlp("The cats were running at 3pm.")
for token in doc:
    print(f"{token.text:10s} tag={token.tag_:5s} pos={token.pos_:6s} dep={token.dep_:10s} head={token.head.text}")
```

```
The        tag=DT    pos=DET    dep=det        head=cats
cats       tag=NNS   pos=NOUN   dep=nsubj      head=running
were       tag=VBD   pos=AUX    dep=aux        head=running
running    tag=VBG   pos=VERB   dep=ROOT       head=running
at         tag=IN    pos=ADP    dep=prep       head=running
3pm        tag=NN    pos=NOUN   dep=pobj       head=at
.          tag=.     pos=PUNCT  dep=punct      head=running
```

Đọc `dep`cột dưới lên và cấu trúc ngữ pháp của câu rơi ra.

> Từ dưới lên lên đọc `dep`列,句子的语法结构就自然呈现了──

> **【中文解读】**Bài này sẽ trình bày cách sử dụng một khung đã phát triển như PyTorch, HuggingFace, và các khác.

> **【拓展：Prompt Engineering 与 LLM 应用】**Kỹ thuật nhanh chóng đã trở thành kỹ năng cốt lõi của các kỹ sư NLP. Từ Zero-shot đến Few-shot, từ Chain-of-Thought đến ReAct, các chiến lược khác nhau áp dụng cho các tình huống khác nhau. Trong các dự án thực tế, thiết kế của System提示(System Prompt) ảnh hưởng trực tiếp đến sự ổn định và chất lượng sản xuất của ứng dụng LLM.

## Hãy sử dụng nó để thực hiện

Mỗi thư viện sản xuất NLP gửi POS và các bộ phân tích phụ thuộc như là một phần của một đường ống tiêu chuẩn.

> Mỗi sản xuất NLP 库都把 POS 和依赖解析器作为标准流水线的一部分提供──

- **spaCy**(`en_core_web_sm`- `md`- `lg`- `trf`). Nhanh chóng, chính xác, tích hợp với tokenization + NER + lemmatization. `token.tag_`(Penn), `token.pos_`(UD), `token.dep_`(sự tương quan phụ thuộc).
  **spaCy**(`en_core_web_sm`- `md`- `lg`- `trf`(→快速、准确,与分词 + NER + 词形还原集成。)`token.tag_`(Penn)`token.pos_`(UD)`token.dep_`(có phụ thuộc)
- **Stanford NLP (stanza)**- Đại học Stanford kế nhiệm CoreNLP.
  **Stanford NLP (stanza)**❖ Người kế nhiệm của Stanford CoreNLP ❖ đạt được mức độ tiên tiến trên 60+ ngôn ngữ ❖
- **trankit**- Dựa trên biến thể, độ chính xác UD tốt.
  **trankit**❖ dựa trên Transformer, tốt UD 准确率──
- **NLTK**- `pos_tag`- Thậm chí, chậm, già hơn, tốt cho việc dạy.
  **NLTK**`pos_tag`❖ 可用、慢、较旧──适合教学──

### Nếu điều này vẫn quan trọng vào năm 2026

- **Lemmatization.**Bài học 01 cần POS để làm việc đúng.
  **词形还原。**第01 课需要 POS 才能正确词形还原──始终如此──
- **Structured extraction from LLM outputs.**Thiết lập rằng một câu được tạo tuân thủ các hạn chế ngữ pháp (ví dụ: thỏa thuận đối tượng và động từ, các sửa đổi cần thiết).
  **LLM 输出的结构化抽取。**验证生成的句子满足语法约束 (如主谓一致,必要修饰语)
- **Aspect-based sentiment.**Các phân tích phụ thuộc cho bạn biết từ đặc tính nào thay đổi từ nào.
  **基于方面的情感分析。**依赖分析告诉你哪个形容词修饰哪个名词──
- **Query understanding.**"Những bộ phim do Wes Anderson đạo diễn với Bill Murray" phân hủy thành những hạn chế cấu trúc thông qua phân tích.
  **查询理解。**"Những bộ phim do Wes Anderson đạo diễn với Bill Murray"
- **Cross-lingual transfer.**Các thẻ UD và mối quan hệ phụ thuộc là ngôn ngữ-người, cho phép phân tích cấu trúc không chụp ảnh của các ngôn ngữ mới.
  **跨语言迁移。**UD 标签和依赖与语言无关,支持新语言的零样本结构化分析.
- **Low-compute pipelines.**Nếu bạn không thể vận chuyển một biến đổi, POS + phụ thuộc phân tích + báo chí đưa bạn xa lạ.
  **低算力流水线。**Nếu không thể triển khai Transformer, POS + 依赖分析 + 地名词典能让你走相当远――

> **【中文解读】**Phần này tập trung vào cách phân phối mô hình như một sản phẩm có thể sử dụng.

## Chuyển nó đi.

Cứ như `outputs/skill-grammar-pipeline.md`- Có thể là:

> 保存为 `outputs/skill-grammar-pipeline.md`- Có thể là:

```markdown
---
name: grammar-pipeline
description: Design a classical POS + dependency pipeline for a downstream NLP task.
version: 1.0.0
phase: 5
lesson: 07
tags: [nlp, pos, parsing]
---

Given a downstream task (information extraction, rewrite validation, query decomposition, lemmatization), you output:

1. Tagset to use. Penn Treebank for English-only legacy pipelines, Universal Dependencies for multilingual or cross-lingual.
2. Library. spaCy for most production, stanza for academic-grade multilingual, trankit for highest UD accuracy. Name the specific model ID.
3. Integration pattern. Show the 3-5 lines that call the library and consume the needed attributes (`.pos_`, `.dep_`, `.head`).
4. Failure mode to test. Noun-verb ambiguity (`saw`, `book`, `can`) and PP-attachment ambiguity are the classical traps. Sample 20 outputs and eyeball.

Refuse to recommend rolling your own parser. Building parsers from scratch is a research project, not an application task. Flag any pipeline that consumes POS tags without handling lowercase/uppercase variants as fragile.
```

> **【中文解读】**练题按照 Easy/Medium/Hard 三个难度递进;;建议至少完成 级别的题目, 级别适合深入研究或面试准备;;

## Tập luyện bài tập

1. **Easy.**Sử dụng đường cơ sở thẻ thường xuyên nhất trên một tập hợp nhỏ được dán nhãn (ví dụ, bộ phụ Brown của NLTK), đo độ chính xác trên các câu được giữ.
   **简单。**Trong một phần nhỏ của NLTK, tỷ lệ xác thực trên các câu được đo là khoảng 85%.
2. **Medium.**Đọc các HMM lớn trên và báo cáo độ chính xác / thu hồi mỗi thẻ.
   **中等。**训练上述二元组 HMM 并报告每标签精确率/召回率──HMM 最容易混哪些标签?
3. **Hard.**Sử dụng phân tích phụ thuộc của spaCy để lấy các đối tượng-tên-từ-từ từ một mẫu 1000 câu. Đánh giá trên 50 bộ ba được dán nhãn bằng tay. Tài liệu khi thu thập thất bại (thường là thụ động, phối hợp và đối tượng bị loại bỏ).
   **困难。**Sử dụng phân tích phụ thuộc của spaCy từ 1000 câu mẫu trong khi lấy được các nhóm thứ ba trong 50 bài viết.

> **【中文解读】**Trong 术语表中的"Những gì mọi người nói" vs "Những gì nó thực sự có nghĩa" 区分日常口语和精确技术含义── 在团队协作中,统一术语定义可以避免大量沟通误解──

## Từ khóa  Từ khóa nhanh chóng

| Term / 术语 | What people say / 人们常说的 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| POS tag（词性标签） | Word's type / 词的类型 | Grammatical category. PTB has 36; UD has 17. / 语法类别。PTB 有 36 个；UD 有 17 个。 |
| Penn Treebank | Standard tagset / 标准标签集 | English-specific. Fine-grained verb tenses and noun number. / 特定于英语。细粒度的动词时态和名词数。 |
| Universal Dependencies（通用依存） | Multilingual tagset / 多语言标签集 | Coarser than PTB; language-neutral; defaults for cross-lingual work. / 比 PTB 更粗；语言无关；跨语言工作的默认选择。 |
| Dependency parse（依存分析） | Sentence tree / 句子树 | Each word has one head, each edge has a grammatical relation. / 每个词有一个中心词，每条边有一个语法关系。 |
| Viterbi（维特比算法） | Dynamic programming / 动态规划 | Finds the highest-probability tag sequence given emissions and transitions. / 给定发射和转移概率，找到最高概率的标签序列。 |

> **【中文解读】**延伸阅读 cung cấp các nguồn chất lượng cao cho việc học sâu. Những bài báo và giảng dạy này là tài liệu tham khảo cổ điển trong lĩnh vực này, phù hợp với những người đọc cần hiểu sâu hơn.

## Xem thêm 延伸阅读

- [Jurafsky and Martin — Speech and Language Processing, chapters 8 and 18](https://web.stanford.edu/~jurafsky/slp3/) việc xử lý sách giáo khoa kinh điển của POS và phân tích. / POS 和解析的经典教科书处理──
- [Universal Dependencies project](https://universaldependencies.org/) bộ Tagset và Treebank đa ngôn ngữ được sử dụng bởi mỗi trình phân tích đa ngôn ngữ. / 每个多语言解析器使用的跨语言标签集和树库集合。
- [spaCy linguistic features guide](https://spacy.io/usage/linguistic-features) tham chiếu thực tế cho mỗi thuộc tính được nêu trên `Token`. / `Token`Các tài liệu trên được sử dụng để xem xét các tính năng trên.
- [Chen and Manning (2014). A Fast and Accurate Dependency Parser using Neural Networks](https://nlp.stanford.edu/pubs/emnlp2014-depparser.pdf) bài báo đưa các phân tích thần kinh vào dòng chính. / 将神经解析器带入主流的论文.
