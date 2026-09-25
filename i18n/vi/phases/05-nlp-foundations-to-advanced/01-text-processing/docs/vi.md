# Quá trình xử lý văn bản  Đánh dấu, Đánh dấu, Lemmatization  文本处理  分词、词干提取、词形還原

> Ngôn ngữ là liên tục, mô hình là riêng biệt, xử lý trước là cầu nối.
> 语言是连续的. Mô hình là phân tán.

> **【中文解读】**分词 là bước đầu tiên của NLP:把连续文本切成离散代币──包括词干提取和词形还原── trong thời đại LLM,分词由 BPE 等子词分词器处理──

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 2 · 14 (Naive Bayes) | **前置知识:** Phase 2 · 14（朴素贝叶斯）
**Time:** ~45 minutes | **时间:** ~45 分钟

## Mục tiêu học tập

- Hiểu tokenization, stemming, và lemmatization như các hoạt động tiền xử lý riêng biệt
  hiểu分词、词干提取和词形还原 như các hoạt động xử lý trước khác nhau
- Xây dựng một token regex, một Porter stemmer bước, và một lemmatizer dựa trên tìm kiếm từ đầu
  Từ零 cấu trúc chính quy phân từ器、Porter 词干提取步骤和基于查找表的词形回原器
- So sánh NLTK và spaCy cho các đường ống xử lý trước sản xuất
  So sánh NLTK và spaCy trong sản xuất dự phòng xử lý dòng nước
- Nhận ra hai lỗi sản xuất phổ biến nhất: trôi chảy khả năng tái tạo và sự không phù hợp giữa tàu và thông số
  识别两种最常见的生产故障:可复现性漂移和训练/推理不匹配

## Vấn đề  vấn đề giới thiệu

Một mô hình không thể đọc "Căn mèo đang chạy". Nó đọc số nguyên.

> 模型不能直接读取 "Những con mèo đang chạy".

Mỗi hệ thống NLP bắt đầu với cùng ba câu hỏi. Từ nào bắt đầu. Nguồn từ là gì. Làm thế nào chúng ta đối xử với "run", "run", "run" như một điều giống nhau khi nó giúp đỡ, và như những thứ khác nhau khi nó không giúp đỡ?

> Mỗi hệ thống NLP đều phải trả lời cùng ba câu hỏi: một từ bắt đầu từ đâu? gốc từ của từ này là gì?

Nếu bạn sai việc mã hóa và mô hình học hỏi từ rác rác.`don't`như một dấu hiệu nhưng `do n't`Nếu các bạn bị thất bại, thì các bạn sẽ bị chia rẽ.`organization`và `organ`Nếu lemmatizer của bạn cần một phần của ngữ cảnh nói nhưng bạn không vượt qua nó, động từ được coi như các từ.

> 分词做错了, mô hình học từ dữ liệu rác. Nếu bạn phân từ máy`don't`Như một token, nhưng đưa `do n't`Khi hai người, tập phân chia sẽ chia rẽ. Nếu từ của bạn làm việc.`organization`和 `organ`Kết luận là cùng một từ干, chủ đề xây dựng sẽ thất bại. Nếu từ của bạn có thể được xử lý như từ từ.

Bài học này xây dựng ba bước xử lý trước từ đầu, sau đó cho thấy cách NLTK và spaCy làm việc tương tự để bạn có thể thấy sự thỏa hiệp.

> Bài học này bắt đầu từ zero xây dựng ba bước xử lý trước, sau đó cho thấy NLTK và spaCy làm thế nào để làm việc tương tự, để bạn thấy cân bằng trong số đó.

## Khái niệm cốt lõi

> **【中文解读】**Bài viết này giới thiệu các khái niệm và lý thuyết cốt lõi.

Ba hoạt động, mỗi hoạt động đều có một nhiệm vụ và một chế độ thất bại.

> Ba hoạt động, mỗi người có trách nhiệm và thất bại của riêng mình.

**Tokenization**"Token" là một từ không rõ ràng vì sự phân mảnh đúng đắn phụ thuộc vào nhiệm vụ.

> **分词（Tokenization）**Để chia các chuỗi thành biểu tượng. Từ này là "Token" được dự định giữ mơ hồ, vì độ phân tích phù hợp phụ thuộc vào nhiệm vụ cụ thể.

**Stemming**- Đánh dấu với quy tắc, nhanh, hung hăng, ngu ngốc.`running -> run`- `organization -> organ`Cái thứ hai là chế độ thất bại.

> **词干提取（Stemming）**Sử dụng quy tắc cắt đứt sau ──快速、激进、粗暴──`running -> run``organization -> organ`                                                                                                                                                                                                                                                              

**Lemmatization**Giảm từ thành từ điển của nó bằng cách sử dụng kiến thức ngữ pháp.`ran -> run`(đáng cần biết "run" là quá khứ của "run").`better -> good`(cần biết các hình thức so sánh).

> **词形还原（Lemmatization）**Sử dụng ngữ pháp kiến thức sẽ từ trở lại nguyên bản để hình thức từ ngữ.`ran -> run`( cần biết "run" là "run" của quá khứ)`better -> good`(đáng cần biết cách so sánh)

Quy tắc ngón tay. Nhận tiếng khi tốc độ quan trọng và bạn có thể dung nạp tiếng ồn (tăng chỉ mục tìm kiếm, phân loại thô). Lemmatize khi ý nghĩa quan trọng (phản ứng câu hỏi, tìm kiếm ngữ nghĩa, bất cứ điều gì người dùng sẽ đọc).

> 经验法则: khi tốc độ quan trọng và có thể chịu đựng tiếng ồn sử dụng từ干提取(搜索引、粗略分类) ・・・ khi ngữ义 quan trọng khi sử dụng từ形还原(问答、语义搜索、任何用户会阅读的场景) ・・・

> **【拓展：大语言模型的工程实践】**Từ GPT đến ChatGPT, NLP đã trải qua sự chuyển đổi từ "mỗi nhiệm vụ đào tạo một mô hình" đến "một mô hình giải quyết tất cả các nhiệm vụ". Trong công trình thực tế, việc triển khai LLM cần phải xem xét các vấn đề như: giới hạn token, trì hoãn, chi phí, kiểm tra an toàn, và các vấn đề khác.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) là cấu trúc phổ biến nhất trong ứng dụng AI của doanh nghiệp hiện tại: sẽ truy vấn người dùng trước tiên truy vấn các đoạn tài liệu liên quan, tiếp tục truy vấn kết quả như trên dưới đây cho LLM 生成答案──

> **【拓展：NLP 的多语言挑战】**Trên toàn cầu có hơn 7000 ngôn ngữ, nhưng nghiên cứu về NLP tập trung chủ yếu vào tiếng Anh và một số ít ngôn ngữ.

## Hãy xây dựng nó.

> **【中文解读】**本节通过代码实现核心算法从零――这种" từ đầu"的方式能帮助理解框架背后的原理,遇到问题时不会被黑盒困住――
```figure
edit-distance
```

## Hãy xây dựng nó

### Bước 1: một token từ regex

Các token hữu ích đơn giản nhất chia thành các ký tự không chữ số trong khi giữ dấu chấm như các token của riêng mình. Không hoàn hảo, không hoàn chỉnh, nhưng nó chạy trong một dòng.

> Các mã số không chữ số được phân chia, đồng thời sẽ giữ dấu chấm ký hiệu cho một biểu tượng độc lập. Không hoàn hảo, cũng không phải là giải pháp cuối cùng, nhưng một dòng mã có thể vận hành.

```python
import re

def tokenize(text):
    return re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?|[0-9]+|[^\sA-Za-z0-9]", text)
```

Ba mô hình theo thứ tự ưu tiên.`don't`- `it's`) Số nguyên chất: bất kỳ ký tự không-lượng trắng nào không phải là chữ số như một biểu tượng độc lập (chỉ dấu).

> 三个按优先排列的模式──带可选内部撇号的词`don't``it's`() : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : :     : : : : :   : : :      :    :  :                                                  

```python
>>> tokenize("The cats weren't running at 3pm.")
['The', 'cats', "weren't", 'running', 'at', '3', 'pm', '.']
```

Các chế độ thất bại để nhận thấy. `3pm`chia thành `['3', 'pm']`vì chúng tôi thay đổi giữa các dòng chữ và số. đủ tốt cho hầu hết các nhiệm vụ. URL, email, hashtags tất cả đều phá vỡ.

> 需要注意的失败模式──`3pm`Được chia cắt`['3', 'pm']`, vì chúng ta đã làm thay đổi giữa chuỗi chữ cái và chuỗi số. Nó đủ tốt cho hầu hết các nhiệm vụ.

### Bước 2: một Porter stemmer (chỉ bước 1a)

Các thuật toán Porter đầy đủ có năm giai đoạn của các quy tắc. bước 1a một mình bao gồm các hậu tố tiếng Anh thường xuyên nhất và dạy các mô hình.

> 完整的波特算法有五阶段的规则──只有步骤1a就涵盖了最常见的英语后,并展示了规则模式──

```python
def stem_step_1a(word):
    if word.endswith("sses"):
        return word[:-2]
    if word.endswith("ies"):
        return word[:-2]
    if word.endswith("ss"):
        return word
    if word.endswith("s") and len(word) > 1:
        return word[:-1]
    return word
```

```python
>>> [stem_step_1a(w) for w in ["caresses", "ponies", "caress", "cats"]]
['caress', 'poni', 'caress', 'cat']
```

Hãy đọc các quy tắc từ trên xuống.`ies -> i`vì thế là vì điều luật`ponies -> poni`Không .`pony`Porter thực sự có bước 1b sẽ sửa chữa điều đó các quy tắc cạnh tranh các quy tắc trước đó thắng lệnh quan trọng hơn bất kỳ quy tắc nào

> Từ trên xuống đọc quy tắc.`ies -> i`Quy tắc là`ponies -> poni`Không phải`pony`Lý do:  Thực tế Porter  thuật toán có bước 1b để khắc phục vấn đề  quy tắc cạnh tranh với nhau, xếp hàng trước các quy tắc chiến thắng  Quy tắc của quy tắc là quan trọng hơn bất kỳ quy tắc đơn lẻ nào 

### Bước 3: một máy tạo ra các hình ảnh

Lemmatization thích hợp cần hình học. Một phiên bản giảng dạy dễ xử lý sử dụng một bảng lemma nhỏ và một fallback.

> Thực tế của từ ngữ hình thức trở lại cần hình thức học.

```python
LEMMA_TABLE = {
    ("running", "VERB"): "run",
    ("ran", "VERB"): "run",
    ("runs", "VERB"): "run",
    ("better", "ADJ"): "good",
    ("best", "ADJ"): "good",
    ("cats", "NOUN"): "cat",
    ("cat", "NOUN"): "cat",
    ("were", "VERB"): "be",
    ("was", "VERB"): "be",
    ("is", "VERB"): "be",
}

def lemmatize(word, pos):
    key = (word.lower(), pos)
    if key in LEMMA_TABLE:
        return LEMMA_TABLE[key]
    if pos == "VERB" and word.endswith("ing"):
        return word[:-3]
    if pos == "NOUN" and word.endswith("s"):
        return word[:-1]
    return word.lower()
```

```python
>>> lemmatize("running", "VERB")
'run'
>>> lemmatize("cats", "NOUN")
'cat'
>>> lemmatize("better", "ADJ")
'good'
>>> lemmatize("watched", "VERB")
'watched'
```

Vụ cuối cùng là khoảnh khắc giảng dạy quan trọng.`watched`Không có mặt trên bàn của chúng ta và sự thất bại của chúng ta chỉ xử lý `ing`- Lêm hóa thực sự bao gồm`ed`, động từ bất thường, đặc tính so sánh, đa số với thay đổi âm thanh (`children -> child`Đó là lý do tại sao các hệ thống sản xuất sử dụng WordNet, một nhà phân tích hình thái của spaCy, hoặc một nhà phân tích hình thái đầy đủ.

> Ví dụ cuối cùng là thời gian giảng dạy quan trọng.`watched`Không nằm trong bảng của chúng ta, nhưng chiến lược dự phòng của chúng ta chỉ xử lý.`ing`◊ thực sự từ hình tái tạo `ed`、不规则动词、比较级形容词、语音变化的复数(`children -> child`)― Đó là lý do tại sao hệ thống sản xuất sử dụng WordNet, không gian của hình thức phân tích hoặc toàn bộ hình thức phân tích.

### Bước 4: Đơn vị kết hợp chúng

```python
def preprocess(text, pos_tagger=None):
    tokens = tokenize(text)
    stems = [stem_step_1a(t.lower()) for t in tokens]
    tags = pos_tagger(tokens) if pos_tagger else [(t, "NOUN") for t in tokens]
    lemmas = [lemmatize(word, pos) for word, pos in tags]
    return {"tokens": tokens, "stems": stems, "lemmas": lemmas}
```

> **【中文解读】**Bài này sẽ trình bày cách sử dụng một khung đã phát triển như PyTorch, HuggingFace, và các khác.

Phần còn lại là một thẻ POS. giai đoạn 5 · 07 (POS Tagging) tạo ra một. Cho đến nay, mặc định mọi thứ để `NOUN`và thừa nhận giới hạn.

> 缺少的部分是词性标注器──Phase 5 · 07(词性标注) sẽ xây dựng một──`NOUN`, đã thừa nhận sự hạn chế này.

> **【拓展：Prompt Engineering 与 LLM 应用】**Kỹ thuật nhanh chóng đã trở thành kỹ năng cốt lõi của các kỹ sư NLP. Từ Zero-shot đến Few-shot, từ Chain-of-Thought đến ReAct, các chiến lược khác nhau áp dụng cho các tình huống khác nhau. Trong các dự án thực tế, thiết kế của System提示(System Prompt) ảnh hưởng trực tiếp đến sự ổn định và chất lượng sản xuất của ứng dụng LLM.

## Hãy sử dụng nó để thực hiện

NLTK và spaCy sẽ đưa ra phiên bản sản xuất.

> NLTK và spaCy đã cung cấp phiên bản cấp sản xuất.

### NLTK

```python
import nltk
nltk.download("punkt_tab")
nltk.download("wordnet")
nltk.download("averaged_perceptron_tagger_eng")

from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk import pos_tag

text = "The cats were running."
tokens = word_tokenize(text)
stems = [PorterStemmer().stem(t) for t in tokens]
lemmatizer = WordNetLemmatizer()
tagged = pos_tag(tokens)


def nltk_pos_to_wordnet(tag):
    if tag.startswith("V"):
        return "v"
    if tag.startswith("J"):
        return "a"
    if tag.startswith("R"):
        return "r"
    return "n"


lemmas = [lemmatizer.lemmatize(t, nltk_pos_to_wordnet(tag)) for t, tag in tagged]
```

`word_tokenize`xử lý các sự suy giảm, Unicode, các trường hợp cạnh mà Regex của bạn bỏ lỡ. `PorterStemmer`chạy tất cả năm giai đoạn. `WordNetLemmatizer`cần thẻ POS được dịch từ chương trình Penn Treebank của NLTK sang tập hợp viết tắt của WordNet.

> `word_tokenize`处理缩写、Unicode 和你的正则表达式遗漏的边界情况──`PorterStemmer`运行所有五个阶段――`WordNetLemmatizer`需要将 NLTK's Penn Treebank 词性标注方案转换为 WordNet's缩写集── trên đây là phần của hầu hết các chương trình nhảy qua──

### spacy

```python
import spacy

nlp = spacy.load("en_core_web_sm")
doc = nlp("The cats were running.")

for token in doc:
    print(token.text, token.lemma_, token.pos_)
```

```
The      the     DET
cats     cat     NOUN
were     be      AUX
running  run     VERB
.        .       PUNCT
```

SpaceCy giấu toàn bộ đường ống sau `nlp(text)`- Đồ ký, thẻ POS, và lemmatization tất cả chạy. nhanh hơn NLTK trên quy mô. chính xác hơn ngoài hộp.

> Không gian sẽ ẩn trong toàn bộ dòng nước`nlp(text)`背后──分词、词性标注和词形还原全部运行──大规模下比NLTK 更快,开箱即用更准确──代价是你无法轻松替换单元组件──

### Khi nào để chọn

| Situation | Pick | 场景 | 选择 |
|-----------|------|------|------|
| Teaching, research, swapping components | NLTK | 教学、研究、需要替换组件 | NLTK |
| Production, multi-language, speed matters | spaCy | 生产环境、多语言、速度要求高 | spaCy |
| Transformer pipeline (you'll tokenize with the model's tokenizer anyway) | Use `tokenizers` / `transformers` and skip classical preprocessing | Transformer 流水线（反正你会用模型自带的分词器） | 使用 `tokenizers` / `transformers`，跳过经典预处理 |

### Hai chế độ thất bại không ai cảnh báo bạn về

Hầu hết các bài tập dạy các thuật toán và dừng lại. Hai thứ sẽ cắn một đường ống xử lý trước thực sự, và chúng hầu như không bao giờ được bao phủ.

> Hầu hết các khóa học dạy về thuật toán đã dừng lại. Có hai vấn đề sẽ bị cắn vào dòng chảy xử lý trước thực tế, và hầu như không bao giờ được đề cập.

**Reproducibility drift.**NLTK và spaCy thay đổi hành vi token hóa và lemmatizer giữa các phiên bản.`['do', "n't"]`trong spaCy 2.x có thể tạo ra `["don't"]`trong 3.x. mô hình của bạn được đào tạo trên một phân phối. Inference bây giờ chạy trên một phân phối khác. độ chính xác lặng lẽ suy giảm và không ai biết tại sao. Pin thư viện phiên bản trong`requirements.txt`Viết một bài kiểm tra hồi quy trước xử lý mà đóng băng dự kiến token hóa của 20 câu mẫu.

> **可复现性漂移。**NLTK và spaCy trong các phiên bản khác nhau sẽ thay đổi phân từ và hình thức từ trở lại hành vi.`['do', "n't"]`Kết quả, trong 3.x có thể xảy ra`["don't"]` mô hình của bạn tập trên một phân bố, suy nghĩ khi vận hành trên một phân bố khác.`requirements.txt`Trong tập trung cố định, viết một bài kiểm tra xử lý trở lại, kết thúc 20 个样本句子的预期分词结果.

**Training / inference mismatch.**Trình luyện với quá trình xử lý trước (bản chữ thấp, loại bỏ từ dừng, stemming), triển khai vào đầu vào của người dùng thô, miệng núi lửa hiệu suất đồng hồ. Đây là sự thất bại NLP sản xuất phổ biến nhất. Nếu bạn xử lý trước trong quá trình đào tạo, bạn phải chạy chức năng tương tự trong quá trình suy luận.

> **训练/推理不匹配。**训练时使用激进的预处理(小写化、停用词删除、词干提取), triển khai khi sử dụng đầu vào người dùng ban đầu, xem hiệu suất暴跌── đây là một lỗi đơn giản phổ biến nhất trong sản xuất NLP── nếu bạn đã thực hiện dự xử lý trong quá trình đào tạo, thì việc đưa ra ý kiến sẽ phải chạy hoàn toàn cùng một hàm── sẽ được xử lý trước như một hàm trong gói mô hình phát hành, thay vì để nhóm dịch vụ viết lại một ghi chú đơn vị──

## Chuyển nó đi.

> **【中文解读】**Phần này tập trung vào cách phân phối mô hình như một sản phẩm có thể sử dụng.

Một lời nhắc có thể được sử dụng nhiều lần giúp các kỹ sư chọn một chiến lược xử lý trước mà không cần đọc ba cuốn sách giáo khoa.

> Một cách nhanh chóng có thể sử dụng, giúp kỹ sư chọn chiến lược xử lý trước và không cần phải đọc 3 cuốn sách giáo khoa.

Cứ như `outputs/prompt-preprocessing-advisor.md`- Có thể là:

```markdown
---
name: preprocessing-advisor
description: Recommends a tokenization, stemming, and lemmatization setup for an NLP task.
phase: 5
lesson: 01
---

You advise on classical NLP preprocessing. Given a task description, you output:

1. Tokenization choice (regex, NLTK word_tokenize, spaCy, or transformer tokenizer). Explain why.
2. Whether to stem, lemmatize, both, or neither. Explain why.
3. Specific library calls. Name the functions. Quote the POS-tag translation if NLTK is involved.
4. One failure mode the user should test for.

> **【中文解读】** 练习题按照 Easy/Medium/Hard 三个难度递进。建议至少完成 Medium 级别的题目，Hard 级别适合深入研究或面试准备。

Refuse to recommend stemming for user-visible text. Refuse to recommend lemmatization without POS tags. Flag non-English input as needing a different pipeline.
```

## Tập luyện bài tập

1. **Easy.**Tăng `tokenize`để giữ URL như một token.`tokenize("Visit https://example.com today.")`sẽ tạo ra một mã URL.
   **简单。**扩展 `tokenize`Để URL 保持为单个代币──测试:`tokenize("Visit https://example.com today.")`应产生一个URL token。
2. **Medium.**Thực hiện Porter bước 1b. Nếu một từ chứa một âm và kết thúc trong `ed`hoặc `ing`, loại bỏ nó. xử lý quy tắc hai âm âm (`hopping -> hop`Không .`hopp`().
   **中等。**实现 Porter 步骤 1b. Nếu một từ chứa các từ và có`ed`Hoặc`ing`结尾,则移除它──处理双辅音规则(`hopping -> hop`, thay vì `hopp`(■)
3. **Hard.**Xây dựng một lemmatizer sử dụng WordNet như một bảng tìm kiếm nhưng rơi lại vào Porter stemmer của bạn khi WordNet không có mục nhập. đo độ chính xác trên một corpus được dán so với WordNet đơn giản và đơn giản Porter.
   **困难。** xây dựng một sử dụng WordNet  như một trình tìm kiếm biểu đồ từ hình trả lại, khi WordNet  không có mục tiêu  quay lại để bạn Porter 词干提取器──

> **【中文解读】**Trong 术语表中的"Những gì mọi người nói" vs "Những gì nó thực sự có nghĩa" 区分日常口语和精确技术含义── 在团队协作中,统一术语定义可以避免大量沟通误解──

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means | 术语 | 人们常说的 | 实际含义 |
|------|-----------------|-----------------------|------|-----------|---------|
| Token | A word | Whatever unit the model consumes. Can be word, subword, character, or byte. | Token（词元） | 一个词 | 模型消耗的任何单位。可以是词、子词、字符或字节。 |
| Stem | Root of a word | Result of rule-based suffix stripping. Not always a real word. | Stem（词干） | 词的词根 | 基于规则的后缀剥离结果。不一定是真正的词。 |
| Lemma | Dictionary form | The form you'd look up. Requires grammatical context to compute correctly. | Lemma（词元形式） | 词典形式 | 你会去词典中查找的形式。需要语法上下文才能正确计算。 |
| POS tag | Part of speech | Category like NOUN, VERB, ADJ. Needed to lemmatize accurately. | POS tag（词性标注） | 词性 | 如 NOUN、VERB、ADJ 等类别。准确词形还原需要它。 |
| Morphology | Word shape rules | How a word changes form based on tense, number, case. Lemmatization depends on it. | Morphology（形态学） | 词形变化规则 | 词如何根据时态、数、格变化形式。词形还原依赖它。 |

> **【中文解读】**延伸阅读 cung cấp các nguồn chất lượng cao cho việc học sâu. Những bài báo và giảng dạy này là tài liệu tham khảo cổ điển trong lĩnh vực này, phù hợp với những người đọc cần hiểu sâu hơn.

## Xem thêm 延伸阅读

- [Porter, M. F. (1980). An algorithm for suffix stripping](https://tartarus.org/martin/PorterStemmer/def.txt) bài báo ban đầu, năm trang, vẫn là lời giải thích rõ ràng nhất. / 原始论文,五页,至今仍然是最清晰的解释──
- [spaCy 101 — linguistic features](https://spacy.io/usage/linguistic-features) cách dây ống dẫn thực sự được kết nối.
- [NLTK book, chapter 3](https://www.nltk.org/book/ch03.html) các trường hợp cạnh của token hóa mà bạn chưa nghĩ đến. / 你还没想过分词边界情况──
