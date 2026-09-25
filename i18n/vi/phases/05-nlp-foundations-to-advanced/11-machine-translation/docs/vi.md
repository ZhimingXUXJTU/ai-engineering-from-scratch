#  Truyền dịch máy  Truyền dịch máy

> Việc dịch là nhiệm vụ đã trả tiền cho nghiên cứu NLP trong ba mươi năm và vẫn trả tiền cho nó ngay bây giờ.
> 翻译是为NLP研究买单三十年的任务,现在仍在继续──

> **【中文解读】**Từ统计机器翻译到神经机器翻译──现代用变压器──

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 10 (Attention Mechanism), Phase 5 · 04 (GloVe, FastText, Subword) | **前置知识:** Phase 5 · 10 (Attention Mechanism), Phase 5 · 04 (GloVe, FastText, Subword)
**Time:** ~75 minutes | **时间:** ~75 minutes


## Vấn đề  vấn đề giới thiệu

Một mô hình đọc một câu trong một ngôn ngữ và tạo ra một câu trong một ngôn ngữ khác. Độ dài thay đổi. Tỷ tự từ thay đổi. Một số từ nguồn lập bản đồ cho nhiều từ mục tiêu và ngược lại. Các ngôn ngữ từ chối lập bản đồ một đến một. "Tôi nhớ bạn" bằng tiếng Pháp là "tu me manques"  nghĩa đen "bạn đang thiếu tôi". Không có sự sắp xếp ở mức từ tồn tại.
> 模型读取一种语言的句子并产生另一种语言的句子──长度不同──词序不同──一些源词映射到多个目标词,反之亦然──习语拒绝对一映射── "Tôi nhớ anh"

> **【中文解读】**Câu hỏi được đặt ra trong phần này là: làm thế nào để hiểu và áp dụng đúng công nghệ này trong công trình thực tế.


Truyền dịch máy là nhiệm vụ buộc NLP phát minh ra các bộ mã hóa-chế định, chú ý, biến đổi và cuối cùng là toàn bộ mô hình LLM. Mỗi bước tiến đã đến vì chất lượng dịch thuật có thể đo lường và khoảng cách giữa con người và máy tính là cứng đầu.
> 机器翻译是迫使NLP 发明编码器-解码器、注意力、Transformer以及最终整个LLM 范式的任务── mỗi bước tiến đều do sự khác biệt giữa người và máy tính.

Bài học này bỏ qua bài học lịch sử và dạy đường ống làm việc của năm 2026: mã hóa-bản giải đa ngôn ngữ được đào tạo trước (NLLB-200 hoặc mBART), mã hóa từ phụ, tìm kiếm chùm, đánh giá BLEU và chrF, và một số chế độ thất bại vẫn được chuyển đến sản xuất chưa bị bắt.
> 本课跳过历史课,教授 2026 年的工作流水线:预训练多语言编码器-解码器(NLLB-200 或 mBART) 、子词分词、束搜索、BLEU 和 chrF 评估,以及少数仍将逃过检查进入生产失败模式──

## Khái niệm cốt lõi

> **【中文解读】**Bài viết này giới thiệu các khái niệm và lý thuyết cốt lõi.


![MT pipeline: tokenize → encode → decode with attention → detokenize](../assets/mt-pipeline.svg)
> ![MT 流水线：分词 → 编码 → 带注意力的解码 → 去分词](../assets/mt-pipeline.svg)

MT hiện đại là một bộ mã hóa mã hóa được đào tạo trên văn bản song song. Bộ mã hóa đọc nguồn trong mã hóa ngôn ngữ của nó. Bộ mã hóa tạo ra mục tiêu, một từ phụ một lúc, sử dụng đầu ra của bộ mã hóa thông qua sự chú ý qua chéo (câu 10). Việc mã hóa sử dụng tìm kiếm chùm để tránh bẫy mã hóa tham lam.
> 现代 MT là một bộ chuyển đổi được đào tạo trên văn bản bình thường 编码器-解码器. 编码器以其语言分词读取源语言. 解码器通过交叉注意力.

Ba lựa chọn hoạt động thúc đẩy chất lượng MT trong thế giới thực.
> 三个运营选择驱动真世界MT质量──

- **Tokenizer.**SentencePiece BPE được đào tạo trên một cơ sở ngôn ngữ hỗn hợp.
- **Model size.**NLLB-200 600M được chưng cất phù hợp với máy tính xách tay. NLLB-200 3.3B là sản phẩm mặc định được công bố. 54.5B là giới hạn nghiên cứu.
- **Decoding.**Độ rộng chùm 4-5 cho nội dung chung. Độ dài phạt để tránh đầu ra quá ngắn. Khóa mã hạn chế khi bạn cần sự nhất quán thuật ngữ.
> - **分词器。**Trong tập luyện trên các ngôn ngữ hỗn hợp, SentencePiece BPE。跨语言共享词表是 NLLB 支持零样本语言对的关键──
- **模型大小。**NLLB-200 蒸 600M 适合笔记本。NLLB-200 3.3B là đã được xuất bản sản xuất默认。54.5B là nghiên cứu天花板。
- **解码。**Thường dùng nội dung 束宽度 4-5。长度惩罚避免输出过短──需要术语一致性时使用约束解码──

> **【中文解读】**本节通过代码实现核心算法从零――这种" từ đầu"的方式能帮助理解框架背后的原理,遇到问题时不会被黑盒困住――

> **【拓展：大语言模型的工程实践】**Từ GPT đến ChatGPT, NLP đã trải qua sự chuyển đổi từ "mỗi nhiệm vụ đào tạo một mô hình" đến "một mô hình giải quyết tất cả các nhiệm vụ". Trong công trình thực tế, việc triển khai LLM cần phải xem xét các vấn đề như: giới hạn token, trì hoãn, chi phí, kiểm tra an toàn, và các vấn đề khác.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) là cấu trúc phổ biến nhất trong ứng dụng AI của doanh nghiệp hiện tại: sẽ truy vấn người dùng trước tiên truy vấn các đoạn tài liệu liên quan, tiếp tục truy vấn kết quả như trên dưới đây cho LLM 生成答案──

> **【拓展：NLP 的多语言挑战】**Trên toàn cầu có hơn 7000 ngôn ngữ, nhưng nghiên cứu về NLP tập trung chủ yếu vào tiếng Anh và một số ít ngôn ngữ.


## Hãy xây dựng nó.
```figure
seq2seq-alignment
```

## Hãy xây dựng nó

### Bước 1: cuộc gọi MT được đào tạo trước
> Ba điều rất quan trọng.`src_lang`告诉分词器使用哪种文字和分割──`forced_bos_token_id`告诉解码器生成哪种语言──两者都是 NLLB đặc biệt技巧;mBART 和 M2M-100 使用各自的约定,不可互换──

```python
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

model_id = "facebook/nllb-200-distilled-600M"
tok = AutoTokenizer.from_pretrained(model_id, src_lang="eng_Latn")
model = AutoModelForSeq2SeqLM.from_pretrained(model_id)

src = "The cats are running."
inputs = tok(src, return_tensors="pt")

out = model.generate(
    **inputs,
    forced_bos_token_id=tok.convert_tokens_to_ids("fra_Latn"),
    num_beams=5,
    length_penalty=1.0,
    max_new_tokens=64,
)
print(tok.batch_decode(out, skip_special_tokens=True)[0])
```

```text
Les chats courent.
```

Ba điều quan trọng ở đây.`src_lang`cho tokenizer biết kịch bản và phân đoạn nào để áp dụng. `forced_bos_token_id`cho decoder biết ngôn ngữ nào để tạo. Cả hai đều là thủ thuật cụ thể của NLLB; mBART và M2M-100 sử dụng các quy ước riêng của họ và chúng không thể thay thế.
> BLEU  đo đầu ra và tham chiếu giữa n-gram 重叠──四种参考 n-gram 大小(1-4), tỷ lệ xác định của几何平均, đối với quá ngắn输出的简洁惩罚──分数在 [0, 100]──常用但难解读:30 BLEU là "可用";40 là "好";50 là "出色";1 BLEU 以内的差异是噪音──

### Bước 2: BLEU và chrF
> chrF  đo chữ cái hạng F 分数。 đối với BLEU 低估匹配的形态丰富语言更敏感──通常与BLEU 一起报告──

BLEU đo n-gram chồng chéo giữa đầu ra và tham chiếu. Bốn kích thước n-gram tham chiếu (1-4), trung bình hình học của độ chính xác, phạt ngắn gọn cho đầu ra quá ngắn. Điểm số là trong [0, 100].
> 始终使用 `sacrebleu` It is a translation of the word "để tạo ra một số lượng lớn các bài luận có thể so sánh".

chrF đo điểm F ở cấp độ ký tự. Thậm chí nhạy cảm hơn với các ngôn ngữ giàu định hình học khi số lượng BLEU thấp phù hợp.
> 现代 MT 评估 sử dụng ba chỉ số bổ sung.

```python
import sacrebleu

hypotheses = ["Les chats courent."]
references = [["Les chats courent."]]

bleu = sacrebleu.corpus_bleu(hypotheses, references)
chrf = sacrebleu.corpus_chrf(hypotheses, references)
print(f"BLEU: {bleu.score:.1f}  chrF: {chrf.score:.1f}")
```

Luôn sử dụng `sacrebleu`Nó làm bình thường hóa token hóa để điểm số được so sánh trên các bài báo.
> - **启发式**(BLEU、chrF)──快速、基于参考、可解释、对释义不敏感──用于遗留比较和归归检测──
- **学习型**(COMET、BLEURT、BERTScore) ―― trong việc đánh giá con người được đào tạo về mô hình thần kinh; so sánh dịch thuật với nguồn và tương tự ngữ nghĩa của tham khảo──COMET kể từ năm 2023 liên quan đến MT, là sản xuất tiêu chuẩn quan trọng nhất năm 2026
- **LLM 评委**(không có tham chiếu)  gợi ý mô hình lớn trong dòng chảy, đầy đủ, ngữ调 và văn hóa thích hợp để dịch cho chia sẻ.

### Các cấp bậc đánh giá ba cấp (2026)
> 2026 年实用技术:`sacrebleu`dùng cho BLEU và chrF,`unbabel-comet`Sử dụng COMET, gợi ý LLM Sử dụng để cuối cùng hướng tới con người tín hiệu.

Phân tích MT hiện đại sử dụng ba gia đình métric bổ sung.
> 无参考指标(COMET-QE、BLEURT-QE、LLM 评委) để bạn đánh giá dịch trong trường hợp không có tham chiếu, điều này đối với không có tham khảo dịch 长尾语言 đối với rất quan trọng.

- **Heuristic**(BLEU, chrF) nhanh, dựa trên tham chiếu, giải thích, không nhạy cảm với các câu.
- **Learned**(COMET, BLEURT, BERTScore). mô hình thần kinh được đào tạo dựa trên phán đoán của con người; so sánh sự tương đồng ngữ nghĩa của dịch thuật với nguồn và tham chiếu. COMET có mối liên hệ cao nhất với nghiên cứu MT kể từ năm 2023 và là sản xuất mặc định năm 2026 khi chất lượng quan trọng.
- **LLM-as-judge**(không tham chiếu). Tạo một mô hình lớn để ghi điểm dịch về độ thông thạo, thích hợp, giọng nói, thích hợp văn hóa. GPT-4 như thẩm phán phù hợp với sự đồng ý của con người ~ 80% thời gian khi rubric được thiết kế tốt. Sử dụng cho nội dung mở khi không có tham chiếu.
> Up面工作流水线 80% thời gian có thể chảy, còn lại 20% là thất bại.

Lưu trữ thực tế năm 2026: `sacrebleu`cho BLEU và chrF, `unbabel-comet`Các phương pháp đo lường được đánh giá bằng 50-100 ví dụ được gắn nhãn con người trước khi tin tưởng vào dữ liệu sản xuất.
> - **幻觉。**模型发明源中没有的内容──在不熟悉的领域词汇中常见──症状:输出流但声称源没有陈述的事实──缓解: đối với các thuật ngữ trong lĩnh vực, đối với nội dung được quản lý kiểm tra nhân tạo, giám sát xuất khẩu so với nhập khẩu dài hơn rất nhiều bất thường──
- **偏离目标语言生成。**模型翻译成错误的语言――NLLB 在罕见语言对上出奇地容易出错――缓解:验证 `forced_bos_token_id`并始终使用语言识别模型检查输出.
- **术语漂移。**"Sign up" trong文档 1 trở thành "s'inscribe", trong文档 2 trở thành "creer un compte"── đối với UI 文本和面向用户的字符串,一致性比原始质量更重要──缓解:词汇表约束解码或后编辑字典──
- **语体不匹配。**Pháp语 "tu" vs "vous",日语敬语级别──模型选择训练中更常见的形式── đối với nội dung đối mặt với khách hàng, đây thường là sai lầm──缓解: Nếu mô hình được hỗ trợ, sử dụng biểu tượng ngôn ngữ 作为提示前, hoặc chỉ trong ngôn ngữ chính thức nhỏ调模型──
- **短输入长度爆炸。**非常短的输入句子经常产生过长的翻译,因为长度惩罚在约5源代币下面急剧下降──缓解:

Các số liệu không tham chiếu (COMET-QE, BLEURT-QE, LLM-as-judge) cho phép bạn đánh giá các bản dịch mà không có tham chiếu, điều này quan trọng đối với các cặp ngôn ngữ đuôi dài nơi không có bản dịch tham chiếu.
> Mô hình đào tạo trước là thông minh. Luật, y tế hay trò chơi.

### Bước 3: những gì phá vỡ trong sản xuất
> Một vài ngàn mẫu bình đẳng chất lượng cao đã vượt qua hàng trăm triệu mẫu thu thập mạng lưới tiếng ồn.

Các đường ống làm việc trên sẽ dịch dịch bằng cách lưu động 80% thời gian và im lặng thất bại 20% còn lại.

- **Hallucination.**Mô hình phát minh ra nội dung không có trong nguồn. phổ biến trong từ vựng miền không quen thuộc. triệu chứng: đầu ra là chảy nhưng tuyên bố thực tế nguồn không nêu. Giảm thiểu: mã hóa hạn chế trên các thuật ngữ miền, đánh giá của con người về nội dung được quy định, giám sát cho đầu ra lâu hơn nhiều so với đầu vào.
- **Off-target generation.**Mô hình dịch sang ngôn ngữ sai. NLLB là đáng ngạc nhiên dễ bị điều này trên các cặp ngôn ngữ hiếm.`forced_bos_token_id`và luôn luôn giải mã bằng một kiểm tra mô hình ID ngôn ngữ trên đầu ra.
- **Terminology drift.**"Sign up" trở thành "s'inscribe" trong doc 1 và "creer un compte" trong doc 2. Đối với văn bản UI và chuỗi đối diện người dùng, sự nhất quán quan trọng hơn chất lượng thô.
- **Formality mismatch.**Tiêu chuẩn "tu" vs "vous" của tiếng Pháp, mức độ lịch sự của Nhật Bản. Mô hình chọn hình thức nào phổ biến hơn trong đào tạo. Đối với nội dung đối mặt với khách hàng, điều này thường sai.
- **Length explosion on short input.**Các câu nhập rất ngắn thường tạo ra các bản dịch quá dài vì hình phạt chiều dài rơi xuống dốc dưới ~ 5 mã thông báo nguồn.

### Bước 4: Định chỉnh cho một tên miền

Các mô hình được đào tạo trước là người nói chung. Dịch pháp lý, y tế hoặc trò chơi đối thoại có lợi ích đáng kể từ việc điều chỉnh tinh tế trên dữ liệu song song miền.

```python
from transformers import Trainer, TrainingArguments
from datasets import Dataset

pairs = [
    {"src": "The defendant pleaded guilty.", "tgt": "L'accusé a plaidé coupable."},
]

ds = Dataset.from_list(pairs)


def preprocess(ex):
    return tok(
        ex["src"],
        text_target=ex["tgt"],
        truncation=True,
        max_length=128,
        padding="max_length",
    )


ds = ds.map(preprocess, remove_columns=["src", "tgt"])

args = TrainingArguments(output_dir="out", per_device_train_batch_size=4, num_train_epochs=3, learning_rate=3e-5)
Trainer(model=model, args=args, train_dataset=ds).train()
```

> **【中文解读】**Bài này sẽ trình bày cách sử dụng một khung đã phát triển như PyTorch, HuggingFace, và các khác.


Một vài ngàn ví dụ song song chất lượng cao vượt qua vài trăm ngàn ví dụ lướt web có tiếng ồn.


> **【拓展：Prompt Engineering 与 LLM 应用】**Kỹ thuật nhanh chóng đã trở thành kỹ năng cốt lõi của các kỹ sư NLP. Từ Zero-shot đến Few-shot, từ Chain-of-Thought đến ReAct, các chiến lược khác nhau áp dụng cho các tình huống khác nhau. Trong các dự án thực tế, thiết kế của System提示(System Prompt) ảnh hưởng trực tiếp đến sự ổn định và chất lượng sản xuất của ứng dụng LLM.

## Hãy sử dụng nó để thực hiện

Lớp sản xuất 2026 cho MT:
> MT 生产技术2026 năm:

| Use case | Recommended starting point |
|---------|---------------------------|
| Any-to-any, 200 languages | `facebook/nllb-200-distilled-600M` (laptop) or `nllb-200-3.3B` (production) |
| English-centric, high quality, 50 languages | `facebook/mbart-large-50-many-to-many-mmt` |
| Short runs, cheap inference, English-French/German/Spanish | Helsinki-NLP / Marian models |
| Latency-critical browser-side | ONNX-quantized Marian (~50 MB) |
| Maximum quality, willing to pay | GPT-4 / Claude / Gemini with translation prompts |
>  Sử dụng cảnh                                                                                                                                                                                                                                                             
|---------|---------|
| 任意到任意，200 种语言 | `facebook/nllb-200-distilled-600M`（笔记本）或 `nllb-200-3.3B`（生产） |
| 以英语为中心，高质量，50 种语言 | `facebook/mbart-large-50-many-to-many-mmt` |
| 短任务，廉价推理，英语-法语/德语/西班牙语 | Helsinki-NLP / Marian 模型 |
| 延迟敏感的浏览器端 | ONNX 量化的 Marian（约 50 MB） |
| 最高质量，愿意付费 | GPT-4 / Claude / Gemini 配合翻译提示 |

LLM hiện đang vượt trội hơn các mô hình MT chuyên ngành trên một số cặp ngôn ngữ từ năm 2026, đặc biệt là về nội dung ngữ pháp và ngữ cảnh dài. Sự thỏa hiệp là chi phí và độ trễ mỗi token. Chọn LLM khi chiều dài ngữ cảnh, tính nhất quán phong cách hoặc thích ứng miền thông qua việc thúc đẩy các vấn đề hơn là thông qua.
> Đến năm 2026, LLM ở nhiều ngôn ngữ đã vượt quá mô hình MT chuyên biệt, đặc biệt là trên nội dung và giá trị của bài học.

> **【中文解读】**Phần này tập trung vào cách phân phối mô hình như một sản phẩm có thể sử dụng.


## Chuyển nó đi.

Cứ như `outputs/skill-mt-evaluator.md`- Có thể là:
> 保存为 `outputs/skill-mt-evaluator.md`- Có thể là:

```markdown
---
name: mt-evaluator
description: Evaluate a machine translation output for shipping.
version: 1.0.0
phase: 5
lesson: 11
tags: [nlp, translation, evaluation]
---

Given a source text and a candidate translation, output:

1. Automatic score estimate. BLEU and chrF ranges you would expect. State whether a reference is available.
2. Five-point human-verifiable check list: (a) content preservation (no hallucinations), (b) correct language, (c) register / formality match, (d) terminology consistency with glossary if provided, (e) no truncation or length explosion.
3. One domain-specific issue to probe. E.g., for legal: named entities and statute citations. For medical: drug names and dosages. For UI: placeholder variables `{name}`.
4. Confidence flag. "Ship" / "Ship with review" / "Do not ship". Tie to the severity of issues found in step 2.

> **【中文解读】** 练习题按照 Easy/Medium/Hard 三个难度递进。建议至少完成 Medium 级别的题目，Hard 级别适合深入研究或面试准备。


Refuse to ship a translation without a language-ID check on output. Refuse to evaluate without a reference unless the user explicitly opts in to reference-free scoring (COMET-QE, BLEURT-QE). Flag any content over 1000 tokens as likely needing chunked translation.
```

## Tập luyện bài tập

1. **Easy.**Dịch một đoạn văn tiếng Anh 5 câu sang tiếng Pháp và trở lại tiếng Anh bằng cách sử dụng `nllb-200-distilled-600M`- Hãy đo mức độ đi lại gần với bản gốc.
2. **Medium.**Thực hiện kiểm tra ID ngôn ngữ trên các kết quả dịch thuật bằng cách sử dụng `fasttext lid.176`hoặc `langdetect`Tham gia vào cuộc gọi MT để các thế hệ ngoài mục tiêu được bắt trước khi quay trở lại.
3. **Hard.**- Đúng rồi.`nllb-200-distilled-600M`trên một bộ phận miền 5000 cặp tùy chọn của bạn. đo BLEU trên một bộ kéo dài trước và sau khi điều chỉnh tinh tế. báo cáo các loại câu nào đã cải thiện và những câu nào đã giảm.
> 1. **简单。**Sử dụng `nllb-200-distilled-600M`将 5 句英语段落翻译成法语再翻回英语──测量往返与原文接近程度── bạn nên thấy ngữ义保留但用词漂移──
2. **中等。**Sử dụng `fasttext lid.176`Hoặc`langdetect`实现翻译输出的语言识别检查──集成到MT调用中,在返回前捕获偏离目标语言的生成──
3. **困难。**Trong 5000 lựa chọn của bạn đối với các lĩnh vực ngôn ngữ`nllb-200-distilled-600M`◊ đo lường các điều chỉnh nhỏ trước sau trong bài viết trên BLEU.

> **【中文解读】**Trong 术语表中的"Những gì mọi người nói" vs "Những gì nó thực sự có nghĩa" 区分日常口语和精确技术含义── 在团队协作中,统一术语定义可以避免大量沟通误解──


## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| BLEU | Translation score | N-gram precision with brevity penalty. [0, 100]. |
| chrF | Character F-score | Character-level F-score. More sensitive for morphologically rich languages. |
| NMT | Neural MT | Transformer encoder-decoder trained on parallel text. The 2017+ default. |
| NLLB | No Language Left Behind | Meta's 200-language MT model family. |
| Constrained decoding | Controlled output | Force specific tokens or n-grams to appear / not appear in the output. |
| Hallucination | Invented content | Model output that is not supported by the source. |
>  Từ ngữ  Mọi người thường nói 
|------|-----------|---------|
| BLEU | 翻译分数 | 带简洁惩罚的 n-gram 精确率。[0, 100]。 |
| chrF | 字符 F 分数 | 字符级 F 分数。对形态丰富语言更敏感。 |
| NMT | 神经机器翻译 | 在平行文本上训练的 Transformer 编码器-解码器。2017+ 的默认。 |
| NLLB | No Language Left Behind | Meta 的 200 语言 MT 模型系列。 |
| 约束解码 | 控制输出 | 强制特定 token 或 n-gram 出现/不出现在输出中。 |
| 幻觉 | 发明内容 | 模型输出中不被源支持的内容。 |

> **【中文解读】**延伸阅读 cung cấp các nguồn chất lượng cao cho việc học sâu. Những bài báo và giảng dạy này là tài liệu tham khảo cổ điển trong lĩnh vực này, phù hợp với những người đọc cần hiểu sâu hơn.


## Xem thêm 延伸阅读

- [Costa-jussà et al. (2022). No Language Left Behind: Scaling Human-Centered Machine Translation](https://arxiv.org/abs/2207.04672) bài báo của NLLB.
- [Post (2018). A Call for Clarity in Reporting BLEU Scores](https://aclanthology.org/W18-6319/) tại sao `sacrebleu`là cách duy nhất chính xác để báo cáo BLEU.
- [Popović (2015). chrF: character n-gram F-score for automatic MT evaluation](https://aclanthology.org/W15-3049/) giấy chrF.
- [Hugging Face MT guide](https://huggingface.co/docs/transformers/tasks/translation) thực tế điều chỉnh tinh tế qua đường đi.
> - [Costa-jussà et al. (2022). No Language Left Behind: Scaling Human-Centered Machine Translation](https://arxiv.org/abs/2207.04672) NLLB 论文。
- [Post (2018). A Call for Clarity in Reporting BLEU Scores](https://aclanthology.org/W18-6319/) Tại sao `sacrebleu`Đó là cách duy nhất chính xác để báo cáo BLEU.
- [Popović (2015). chrF: character n-gram F-score for automatic MT evaluation](https://aclanthology.org/W15-3049/) chrF 论文。
- [Hugging Face MT guide](https://huggingface.co/docs/transformers/tasks/translation) 实用微调演练。
