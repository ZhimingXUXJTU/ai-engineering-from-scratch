# NLP đa ngôn ngữ

> Một mô hình, 100+ ngôn ngữ, không có dữ liệu đào tạo cho hầu hết. Chuyển chuyển xuyên ngôn ngữ là phép lạ thực tế của những năm 2020.
> Một mô hình, 100+ ngôn ngữ, hầu hết ngôn ngữ không có dữ liệu đào tạo.

> **【中文解读】**Nhiều ngôn ngữ BERT, XLM-R 等模型处理多种语言.

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 04 (GloVe, FastText, Subword), Phase 5 · 11 (Machine Translation) | **前置知识:** Phase 5 · 04（GloVe、FastText、子词），Phase 5 · 11（机器翻译）
**Time:** ~45 minutes | **时间:** ~45 分钟

## Vấn đề  vấn đề giới thiệu

Tiếng Anh có hàng tỷ ví dụ được dán nhãn. Tiếng Urdu có hàng ngàn ví dụ. Tiếng Maithili gần như không có ví dụ nào. Bất kỳ hệ thống NLP thực tế nào phục vụ một khán giả toàn cầu phải làm việc trên đuôi dài của các ngôn ngữ mà không có dữ liệu đào tạo cụ thể về nhiệm vụ.

> Tiếng Anh có hàng tỷ mẫu biểu tượng. Tiếng Urdu có hàng ngàn. Tiếng Việt hầu như không có.

> **【中文解读】**Câu hỏi được đặt ra trong phần này là: làm thế nào để hiểu và áp dụng đúng công nghệ này trong công trình thực tế.

Các mô hình đa ngôn ngữ giải quyết vấn đề này bằng cách đào tạo một mô hình trên nhiều ngôn ngữ cùng một lúc. Sự đại diện được chia sẻ cho phép mô hình chuyển giao các kỹ năng được học trong các ngôn ngữ có nguồn lực cao sang các ngôn ngữ có nguồn lực thấp. Định chỉnh mô hình dựa trên phân tích cảm xúc tiếng Anh, và nó tạo ra những dự đoán cảm xúc đáng ngạc nhiên về tiếng Urdu. Đó là chuyển đổi ngôn ngữ qua không, và nó đã định hình lại cách NLP chuyển sang thế giới.

> Mô hình đa ngôn ngữ thông qua cùng một lúc đào tạo một mô hình để giải quyết vấn đề này trên nhiều ngôn ngữ. chia sẻ cho thấy mô hình sẽ chuyển giao các kỹ năng học được từ các ngôn ngữ có nguồn lực cao sang các ngôn ngữ có nguồn lực thấp. Trong phân tích cảm xúc bằng tiếng Anh, mô hình này có thể tạo ra một dự đoán cảm xúc tốt đáng kinh ngạc đối với tiếng Urdu.

Bài học này nêu tên những sự thỏa hiệp, các mô hình truyền thống, và quyết định duy nhất khiến các nhóm mới làm việc đa ngôn ngữ: chọn một ngôn ngữ nguồn để chuyển.

> Bài này đặt tên cho các phương pháp định nghĩa và các phương pháp định nghĩa của nhóm người mới trong quá trình chuyển đổi đa ngôn ngữ:

## Khái niệm cốt lõi

> **【中文解读】**Bài viết này giới thiệu các khái niệm và lý thuyết cốt lõi.

![Cross-lingual transfer via shared multilingual embedding space](../assets/multilingual.svg)

**Shared vocabulary.**Các mô hình đa ngôn ngữ sử dụng một token SentencePiece hoặc WordPiece được đào tạo trên văn bản từ tất cả các ngôn ngữ mục tiêu.`anti-`bằng tiếng Anh và tiếng Ý có được cùng một dấu hiệu.

> **共享词表。**Nhiều ngôn ngữ mô hình sử dụng trên tất cả các văn bản ngôn ngữ mục tiêu được đào tạo SentencePiece hoặc WordPiece 分词器──词表是共享的:相同的子词单元表示相同的语素──英语和意大利语的`anti-`获得同样的标志――

**Shared representation.**Một người biến đổi được đào tạo trước trên mô hình hóa ngôn ngữ mặt nạ trên nhiều ngôn ngữ học được rằng các câu ngữ nghĩa tương tự trong các ngôn ngữ khác nhau tạo ra các trạng thái ẩn tương tự. mBERT, XLM-R và NLLB đều thể hiện điều này.

> **共享表示。**Trong nhiều ngôn ngữ ẩn ngữ xây dựng trên đào tạo trước Transformer học học để các câu tương tự trong các ngôn ngữ khác nhau tạo ra trạng thái ẩn tương tự. MBERT, XLM-R và NLLB đều chứng minh điều này.

**Zero-shot transfer.**Định chỉnh mô hình trên dữ liệu được dán nhãn bằng một ngôn ngữ (thường là tiếng Anh). Khi suy luận, chạy nó trên bất kỳ ngôn ngữ nào khác mà mô hình hỗ trợ. Không cần các nhãn ngôn ngữ mục tiêu. Kết quả mạnh mẽ cho các ngôn ngữ có liên quan theo kiểu và yếu hơn cho các ngôn ngữ xa hơn.

> **零样本迁移。**Trong một ngôn ngữ (thường là tiếng Anh) các nhãn dữ liệu trên mô hình được điều chỉnh nhỏ hơn.

**Few-shot fine-tuning.**Thêm 100-500 ví dụ được dán nhãn trong ngôn ngữ mục tiêu. Độ chính xác nhảy lên 95-98% của đường cơ sở tiếng Anh về các nhiệm vụ phân loại. Đây là đòn bẩy chi phí hiệu quả nhất trong NLP đa ngôn ngữ.

> **少样本微调。**Trong ngôn ngữ mục tiêu, thêm 100-500 mẫu đánh dấu. Trong phân loại nhiệm vụ, tỷ lệ độ chính xác tăng lên 95-98% của cơ sở tiếng Anh. Đây là đòn lợi nhuận cao nhất trong NLP đa ngôn ngữ.

> **【拓展：大语言模型的工程实践】**Từ GPT đến ChatGPT, NLP đã trải qua sự chuyển đổi từ "mỗi nhiệm vụ đào tạo một mô hình" đến "một mô hình giải quyết tất cả các nhiệm vụ". Trong công trình thực tế, việc triển khai LLM cần phải xem xét các vấn đề như: giới hạn token, trì hoãn, chi phí, kiểm tra an toàn, và các vấn đề khác.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) là cấu trúc phổ biến nhất trong ứng dụng AI của doanh nghiệp hiện tại: sẽ truy vấn người dùng trước tiên truy vấn các đoạn tài liệu liên quan, tiếp tục truy vấn kết quả như trên dưới đây cho LLM 生成答案──

> **【拓展：NLP 的多语言挑战】**Trên toàn cầu có hơn 7000 ngôn ngữ, nhưng nghiên cứu về NLP tập trung chủ yếu vào tiếng Anh và một số ít ngôn ngữ.

## Những người mẫu

| Model / 模型 | Year / 年份 | Coverage / 覆盖 | Notes / 说明 |
|-------|------|----------|-------|
| mBERT | 2018 | 104 languages / 104 种语言 | Trained on Wikipedia. First practical multilingual LM. Weak on low-resource. / 在 Wikipedia 上训练。首个实用多语言 LM。低资源语言较弱。 |
| XLM-R | 2019 | 100 languages / 100 种语言 | Trained on CommonCrawl. Sets the cross-lingual baseline. / 在 CommonCrawl 上训练。设定跨语言基线。 |
| XLM-V | 2023 | 100 languages / 100 种语言 | XLM-R with 1M-token vocabulary. Better on low-resource. / XLM-R 配 1M token 词表。低资源更好。 |
| mT5 | 2020 | 101 languages / 101 种语言 | T5 architecture for multilingual generation. / T5 架构用于多语言生成。 |
| NLLB-200 | 2022 | 200 languages / 200 种语言 | Meta's translation model; includes 55 low-resource languages. / Meta 翻译模型；含 55 种低资源语言。 |
| BLOOM | 2022 | 46 languages + 13 programming / 46 种语言 + 13 种编程语言 | Open 176B LLM trained multilingually. / 开源 176B 多语言 LLM。 |
| Aya-23 | 2024 | 23 languages / 23 种语言 | Cohere's multilingual LLM. Strong on Arabic, Hindi, Swahili. / Cohere 多语言 LLM。阿拉伯语、印地语、斯瓦希里语强。 |

Chọn theo trường hợp sử dụng. Việc phân loại hoạt động tốt với XLM-R-base như là mặc định hợp lý. Các nhiệm vụ thế hệ yêu cầu mT5 hoặc NLLB tùy thuộc vào phiên dịch so với thế hệ mở. Các cặp làm việc theo phong cách LLM với Aya-23 hoặc Claude sử dụng nhắc nhở đa ngôn ngữ rõ ràng.

> 按用例选择──分类任务以 XLM-R-base 作为合理默认──生成任务根据翻译 vs 开放生成选择 mT5 或 NLLB──LLM 风格工作配合 Aya-23 或 Claude 使用显式多语言提示──

## Quyết định ngôn ngữ nguồn (2026 nghiên cứu) 源语言决策

Hầu hết các nhóm đều mặc định sử dụng tiếng Anh như nguồn điều chỉnh tinh tế.

> Đại đa số nhóm người dùng đã đồng ý với tiếng Anh như là một nguồn nhỏ. Nghiên cứu mới nhất của năm 2026 cho thấy điều này thường là sai lầm.

Sự tương đồng ngôn ngữ dự đoán chất lượng chuyển giao tốt hơn kích thước cơ thể thô. Đối với các mục tiêu Slavic, tiếng Đức hoặc tiếng Nga thường đánh bại tiếng Anh. Đối với các mục tiêu Ấn Độ, tiếng Hindi thường đánh bại tiếng Anh.**qWALS**Metric tương đồng (2026, dựa trên các tính năng của World Atlas of Language Structures) định lượng điều này. **LANGRANK**(Lin et al., ACL 2019) là một phương pháp riêng biệt, sớm hơn xếp hạng các ngôn ngữ nguồn ứng cử viên từ sự kết hợp của sự tương đồng ngôn ngữ, kích thước cơ thể và liên quan di truyền.

> 语言相似性比原始语料大小更好地预测迁移质量── đối với mục tiêu của Slavic, tiếng Đức hoặc tiếng俄 thường thắng hơn tiếng Anh── đối với mục tiêu của tiếng Ấn, tiếng Ấn thường thắng hơn tiếng Anh──**qWALS**Tương tự như tính chất đo lường (tương tự như tính chất đo lường) năm 2026.**LANGRANK**(Lin 等,ACL 2019) Từ ngôn ngữ tương tự tính, ngôn ngữ lớn và quan hệ di truyền trong bộ sưu tập

Quy tắc thực tế: nếu ngôn ngữ mục tiêu của bạn có một người thân có nguồn lực cao, hãy thử điều chỉnh kỹ trước, sau đó so sánh với tiếng Anh.

> Quy tắc thực tế: Nếu ngôn ngữ mục tiêu của bạn có một loại học gần như thân mật với nguồn lực cao, trước tiên hãy thử điều chỉnh trên ngôn ngữ đó, sau đó so sánh với tiếng Anh.

## Hãy xây dựng nó.

> **【中文解读】**本节通过代码实现核心算法从零――这种" từ đầu"的方式能帮助理解框架背后的原理,遇到问题时不会被黑盒困住――
```figure
n5-crosslingual-bridge
```

## Hãy xây dựng nó

### Bước 1: phân loại qua ngôn ngữ không có dấu hiệu

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

tok = AutoTokenizer.from_pretrained("joeddav/xlm-roberta-large-xnli")
model = AutoModelForSequenceClassification.from_pretrained("joeddav/xlm-roberta-large-xnli")


def classify(text, candidate_labels, hypothesis_template="This text is about {}."):
    scores = {}
    for label in candidate_labels:
        hypothesis = hypothesis_template.format(label)
        inputs = tok(text, hypothesis, return_tensors="pt", truncation=True)
        with torch.no_grad():
            logits = model(**inputs).logits[0]
        entail_score = torch.softmax(logits, dim=-1)[2].item()
        scores[label] = entail_score
    return dict(sorted(scores.items(), key=lambda x: -x[1]))


print(classify("I love this product!", ["positive", "negative", "neutral"]))
print(classify("मुझे यह उत्पाद पसंद है!", ["positive", "negative", "neutral"]))
print(classify("J'adore ce produit !", ["positive", "negative", "neutral"]))
```

Một mô hình, ba ngôn ngữ, cùng một API. XLM-R được đào tạo trên NLI dữ liệu chuyển tốt đến phân loại thông qua thủ thuật liên kết.

> Một mô hình, ba ngôn ngữ, cùng một API. XLM-R được đào tạo trên dữ liệu NLI thông qua kỹ thuật rất tốt chuyển sang phân loại.

### Bước 2: không gian nhúng đa ngôn ngữ

```python
from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

pairs = [
    ("The cat is sleeping.", "Le chat dort."),
    ("The cat is sleeping.", "El gato está durmiendo."),
    ("The cat is sleeping.", "Die Katze schläft."),
    ("The cat is sleeping.", "The dog is barking."),
]

for eng, other in pairs:
    emb_eng = model.encode([eng], normalize_embeddings=True)[0]
    emb_other = model.encode([other], normalize_embeddings=True)[0]
    sim = float(np.dot(emb_eng, emb_other))
    print(f"  {eng!r} <-> {other!r}: cos={sim:.3f}")
```

Các bản dịch kết thúc gần trong không gian nhúng. Một câu tiếng Anh khác đi xa hơn. Đây là điều làm cho việc tìm kiếm, nhóm và tương đồng giữa các ngôn ngữ hoạt động.

> 翻译在嵌入空间中距离很近. 距离更远. Đó là cơ sở của việc tìm kiếm, phân loại và tương tự.

### Bước 3: Chiến lược điều chỉnh tinh tế ít ảnh

```python
from transformers import TrainingArguments, Trainer
from datasets import Dataset


def few_shot_finetune(base_model, base_tokenizer, examples):
    ds = Dataset.from_list(examples)

    def tokenize_fn(ex):
        out = base_tokenizer(ex["text"], truncation=True, max_length=128)
        out["labels"] = ex["label"]
        return out

    ds = ds.map(tokenize_fn)
    args = TrainingArguments(
        output_dir="out",
        per_device_train_batch_size=8,
        num_train_epochs=5,
        learning_rate=2e-5,
        save_strategy="no",
    )
    trainer = Trainer(model=base_model, args=args, train_dataset=ds)
    trainer.train()
    return base_model
```

Đối với 100-500 ví dụ về ngôn ngữ mục tiêu, `num_train_epochs=5`và `learning_rate=2e-5`Tỷ lệ học tập cao hơn khiến sự sắp xếp đa ngôn ngữ sụp đổ và bạn có được mô hình chỉ bằng tiếng Anh.

> Đối với 100-500 个目标语言样本,`num_train_epochs=5`和 `learning_rate=2e-5`Đó là giá trị mặc định. Tỷ lệ học tập cao hơn sẽ dẫn đến sự sụp đổ của nhiều ngôn ngữ, bạn có được một mô hình chỉ giới hạn trong tiếng Anh.

> **【拓展：Prompt Engineering 与 LLM 应用】**Kỹ thuật nhanh chóng đã trở thành kỹ năng cốt lõi của các kỹ sư NLP. Từ Zero-shot đến Few-shot, từ Chain-of-Thought đến ReAct, các chiến lược khác nhau áp dụng cho các tình huống khác nhau. Trong các dự án thực tế, thiết kế của System提示(System Prompt) ảnh hưởng trực tiếp đến sự ổn định và chất lượng sản xuất của ứng dụng LLM.

## Đánh giá thực sự hiệu quả

- **Per-language accuracy on held-out sets.**Không được tổng hợp, tổng hợp ẩn lại đuôi dài.
  **每种语言在留出集上的准确率。**Đừng tập hợp.
- **Benchmark against monolingual baseline.**Đối với các ngôn ngữ có đủ dữ liệu, một mô hình đơn ngôn ngữ được đào tạo từ đầu đôi khi vượt qua một ngôn ngữ đa ngôn ngữ.
  **与单语基线比较。**Đối với ngôn ngữ có đủ dữ liệu, từ đầu đào tạo mô hình ngôn ngữ đơn đôi khi vượt qua nhiều mô hình ngôn ngữ.
- **Entity-level tests.**Các mô hình đa ngôn ngữ thường có biểu tượng yếu cho các chữ viết xa từ tiếng Latinh.
  **实体级测试。**目标语言中的命名实体──多语言模型对远离拉丁文的书写的分词通常较弱──
- **Cross-lingual consistency.**cùng một ý nghĩa trong hai ngôn ngữ nên tạo ra dự đoán tương tự.
  **跨语言一致性。**两种语言中相同含义应产生相同预测――测量差距――

> **【中文解读】**Bài này sẽ trình bày cách sử dụng một khung đã phát triển như PyTorch, HuggingFace, và các khác.

## Hãy sử dụng nó để thực hiện

Số 2026:

> 2026 năm của công nghệ:

| Task / 任务 | Recommended / 推荐 |
|-----|-------------|
| Classification, 100 languages / 分类，100 种语言 | XLM-R-base (~270M) fine-tuned / 微调 |
| Zero-shot text classification / 零样本文本分类 | `joeddav/xlm-roberta-large-xnli` |
| Multilingual sentence embeddings / 多语言句子嵌入 | `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` |
| Translation, 200 languages / 翻译，200 种语言 | `facebook/nllb-200-distilled-600M` |
| Generative multilingual / 生成式多语言 | Claude, GPT-4, Aya-23, mT5-XXL |
| Low-resource language NLP / 低资源语言 NLP | XLM-V or domain-specific fine-tune / XLM-V 或领域微调 |

Luôn luôn có ngân sách để điều chỉnh kỹ lưỡng trong ngôn ngữ mục tiêu nếu hiệu suất quan trọng.

> Nếu hiệu suất quan trọng, luôn luôn cho mục tiêu ngôn ngữ của ngân sách dự phòng.

### Thuế công nghệ.

Các mô hình đa ngôn ngữ chia sẻ một token trên tất cả các ngôn ngữ của họ. Thuật từ đó được đào tạo trên một tập hợp thống trị bởi tiếng Anh, tiếng Pháp, tiếng Tây Ban Nha, tiếng Trung, tiếng Đức. Đối với bất kỳ ngôn ngữ nào bên ngoài tập hợp thống trị, ba loại thuế được hợp tác lặng lẽ:

> Nhiều ngôn ngữ mô hình trong tất cả các ngôn ngữ chia sẻ một phân từ.

- **Fertility tax.**Các văn bản ngôn ngữ có nguồn lực thấp được mã hóa thành nhiều mã thông báo hơn nhiều so với tiếng Anh. Một câu tiếng Hindi có thể cần 3-5 lần mã thông báo của một câu tiếng Anh tương đương.
  **繁殖税。**低资源语言文本每词分词成比英语多多的代币―― một câu tiếng Ấn Độ có thể cần giá tương đương với câu tiếng Anh 3-5 lần của một câu.
- **Variant recovery tax.**Mỗi lỗi đánh chữ, biến thể phân tử, sự không phù hợp chuẩn hóa Unicode, hoặc biến thể trường hợp trở thành một chuỗi không liên quan bắt đầu lạnh trong không gian nhúng.
  **变体恢复税。**Mỗi chữ viết sai, biến âm biểu tượng biến, Unicode 归结不匹配或大小写变都变成嵌入空间中的冷启动无关序列.
- **Capacity spillover tax.**Các khoản thuế 1 và 2 tiêu thụ vị trí ngữ cảnh, độ sâu lớp và kích thước nhúng.
  **容量溢出税。**Thuế 1 và 2  tiêu thụ trên vị trí dưới đây, độ sâu và độ nhúng.

Các triệu chứng thực tế: mô hình của bạn thường tập luyện bằng tiếng Hindi, đường cong mất mát trông đúng, sự bối rối đánh giá trông hợp lý, và sản xuất sản xuất là sai lầm tinh tế. **You cannot data-scale your way out of a broken tokenizer.**

> 实际症状: mô hình trên tiếng Ấn Độ được đào tạo bình thường, mất đường cong chính xác, đánh giá sự bối rối hợp lý, nhưng sản xuất xuất rất nhỏ gọn.**你无法通过数据扩展来修复损坏的分词器。**

Giảm thiểu: chọn một tokenizer có sự bao phủ tốt cho ngôn ngữ mục tiêu của bạn; kiểm tra khả năng sinh sản của token hóa trên văn bản mục tiêu bị giữ; sử dụng độ fallback cấp bayt cho các kịch bản thực sự dài đuôi.

> 缓解措施: chọn cho mục tiêu ngôn ngữ覆盖良好的分词器; trên bài viết mục tiêu đã được bỏ ra chứng nhận分词繁殖率; đối với thực tế长尾书写使用字节级回退──

> **【中文解读】**Phần này tập trung vào cách phân phối mô hình như một sản phẩm có thể sử dụng.

## Chuyển nó đi.

Cứ như `outputs/skill-multilingual-picker.md`- Có thể là:

> 保存为 `outputs/skill-multilingual-picker.md`- Có thể là:

```markdown
---
name: multilingual-picker
description: Pick source language, target model, and evaluation plan for a multilingual NLP task.
version: 1.0.0
phase: 5
lesson: 18
tags: [nlp, multilingual, cross-lingual]
---

Given requirements (target languages, task type, available labeled data per language), output:

1. Source language for fine-tuning. Default English; check LANGRANK or qWALS if target language has a typologically close high-resource language.
2. Base model. XLM-R (classification), mT5 (generation), NLLB (translation), Aya-23 (generative LLM).
3. Few-shot budget. Start with 100-500 target-language examples if available.
4. Evaluation plan. Per-language accuracy, cross-lingual consistency, entity-level F1 on non-Latin scripts.

Refuse to ship a multilingual model without per-language evaluation. Flag scripts with low tokenization coverage as needing byte-fallback.
```

> **【中文解读】**练题按照 Easy/Medium/Hard 三个难度递进;;建议至少完成 级别的题目, 级别适合深入研究或面试准备;;

## Tập luyện bài tập

1. **Easy.**Hãy chạy đường ống phân loại bằng cách không bắn trên 10 câu mỗi ngôn ngữ trên tiếng Anh, tiếng Pháp, tiếng Hindi và tiếng Ả Rập.
   **简单。**Trong tiếng Anh, tiếng Pháp, tiếng Ấn và tiếng Ả Rập, hoạt động trên không có mẫu phân loại dòng nước, mỗi ngôn ngữ có 10 câu.
2. **Medium.**Sử dụng `paraphrase-multilingual-MiniLM-L12-v2`để xây dựng một máy tìm kiếm đa ngôn ngữ trên một tập hợp ngôn ngữ hỗn hợp nhỏ.
   **中等。**构建跨语言检索器──用英语查询,检索任何语言的文档──测量回忆@5──
3. **Hard.**So sánh nguồn tiếng Anh và nguồn tiếng Hindi tinh chỉnh cho một nhiệm vụ phân loại tiếng Hindi. Báo cáo nguồn nào tạo ra độ chính xác tiếng Hindi tốt hơn. Đây là luận án LANGRANK trong mô hình nhỏ.
   **困难。**So sánh nguồn tiếng Anh và nguồn tiếng Ấn Độ về hiệu quả của các nhiệm vụ phân loại tiếng Ấn Độ. Báo cáo có nguồn nào tạo ra tỷ lệ chính xác tốt hơn. Đây là cú tóm tắt của bài báo LANGRANK.

> **【中文解读】**Trong 术语表中的"Những gì mọi người nói" vs "Những gì nó thực sự có nghĩa" 区分日常口语和精确技术含义── 在团队协作中,统一术语定义可以避免大量沟通误解──

## Từ khóa  Từ khóa nhanh chóng

| Term / 术语 | What people say / 人们常说的 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| Multilingual model（多语言模型） | One model, many languages / 一个模型多种语言 | Shared vocabulary and parameters across languages. / 跨语言共享词表和参数。 |
| Cross-lingual transfer（跨语言迁移） | Train on one, run on another / 训练一种，运行另一种 | Fine-tune on source, evaluate on target without target labels. / 在源语言微调，在目标语言评估。 |
| Zero-shot（零样本） | No target labels / 无目标标签 | Transfer without target-language fine-tuning. / 无目标语言微调的迁移。 |
| Few-shot（少样本） | Small target labels / 少量目标标签 | 100-500 target-language examples for fine-tuning. / 100-500 个目标语言样本。 |
| mBERT | First multilingual LM / 首个多语言 LM | 104-language BERT on Wikipedia. / 104 语言 BERT。 |
| XLM-R | Cross-lingual baseline / 跨语言基线 | 100-language RoBERTa on CommonCrawl. / 100 语言 RoBERTa。 |
| NLLB | 200-language MT / 200 语言 MT | No Language Left Behind. 55 low-resource languages. / 不让任何语言掉队。55 种低资源语言。 |

> **【中文解读】**延伸阅读 cung cấp các nguồn chất lượng cao cho việc học sâu. Những bài báo và giảng dạy này là tài liệu tham khảo cổ điển trong lĩnh vực này, phù hợp với những người đọc cần hiểu sâu hơn.

## Xem thêm 延伸阅读

- [Conneau et al. (2019). XLM-R](https://arxiv.org/abs/1911.02116) bài báo XLM-R. / XLM-R 论文。
- [Pires et al. (2019). How Multilingual is Multilingual BERT?](https://arxiv.org/abs/1906.01502) phân tích chuyển giao xuyên ngôn ngữ. / 跨语言迁移分析。
- [Costa-jussà et al. (2022). No Language Left Behind](https://arxiv.org/abs/2207.04672) NLLB-200. / NLLB-200 论文。
- [Üstün et al. (2024). Aya Model](https://arxiv.org/abs/2402.07827) Cohere's đa ngôn ngữ LLM. / Cohere 多语言 LLM。
- [Language Similarity Predicts Cross-Lingual Transfer (2026)](https://www.mdpi.com/2504-4990/8/3/65) QWALS / LANGRANK. / qWALS / LANGRANK 源语言论文。
