# CNN và RNN để Text

> Convolutions học n-gram, recidivities nhớ, cả hai đều bị thay thế bởi sự chú ý, cả hai vẫn quan trọng trên phần cứng bị hạn chế.
> 卷积学习 n-gram. 循环负责记忆. 循环负责记忆. 循环负责记忆. 循环负责记忆. 循环负责记忆. 循环负责记忆. 循环负责记忆. 循环负责记忆. 循环负责记忆. 循环负责记忆. 循环负责记忆. 循环负责记忆. 循环负责记忆. 循环负责记忆. 循环负责记忆. 循环负责记忆.

> **【中文解读】**CNN 捕捉局部 n-gram 特征,RNN 处理长程依赖――Transformer 之前的主流架构――

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 3 · 11 (PyTorch Intro), Phase 5 · 03 (Word Embeddings), Phase 4 · 02 (Convolutions from Scratch) | **前置知识:** Phase 3 · 11（PyTorch 入门），Phase 5 · 03（词嵌入），Phase 4 · 02（从零实现卷积）
**Time:** ~75 minutes | **时间:** ~75 分钟

## Vấn đề  vấn đề giới thiệu

TF-IDF và Word2Vec tạo ra các vector phẳng mà bỏ qua thứ tự từ.`dog bites man`từ `man bites dog`Đôi khi, thứ tự từ ngữ là tín hiệu.

> TF-IDF và Word2Vec  tạo ra sự bỏ qua các từ ngữ 平向量.`dog bites man`和 `man bites dog`                                                                                                                                                                                                                                                              

Hai gia đình kiến trúc đã lấp đầy khoảng trống đó trước khi các nhà biến đổi đến.

> Trước khi Transformer xuất hiện, hai bộ tộc đã lấp đầy khoảng trống này.

**Convolutional nets for text (TextCNN).**Sử dụng các biến dạng 1D trên các chuỗi các chữ nhúng. Một bộ lọc chiều rộng 3 là một bộ dò hình ba chữ được học: nó trải dài ba từ và đưa ra một điểm số. Lắp xếp chiều rộng khác nhau (2, 3, 4, 5) để phát hiện các mẫu đa quy mô. Max-pool đến một đại diện kích thước cố định. Dũng, song song, nhanh.

> **文本卷积网络（TextCNN）。**Trong các chuỗi nhúng từ được áp dụng một chiều卷积── chiều rộng 3 波器 là một bộ vi xử lý triều đại có thể học được: nó vượt qua ba từ và xuất số phân số── chồng lên với chiều rộng khác nhau(2、3、4、5) để kiểm tra mô hình đa chiều──最大池化 thành biểu hiện cố định kích thước──平、并行、快速──

**Recurrent nets (RNN, LSTM, GRU).**xử lý token một lần, duy trì một trạng thái ẩn mang thông tin về phía trước. Dường độ đầu vào liên tục, ghi nhớ, linh hoạt. Mô hình hóa chuỗi thống trị từ năm 2014 đến năm 2017, sau đó sự chú ý xảy ra.

> **循环网络（RNN、LSTM、GRU）。**个个处理代币,维护向前传递信息的隐藏状态――顺序、有记忆、灵活输入长度── từ năm 2014 đến năm 2017 序列主导建模, sau đó là cơ chế chú ý xuất hiện──

Bài học này xây dựng cả hai, sau đó đặt tên thất bại đã thúc đẩy sự chú ý.

> Bài học này xây dựng hai, sau đó chỉ ra sự thất bại của động cơ tập trung.

## Khái niệm cốt lõi

> **【中文解读】**Bài viết này giới thiệu các khái niệm và lý thuyết cốt lõi.

**TextCNN**(Kim, 2014). Các token được nhúng.`k`1D convolution slide một bộ lọc trên liên tiếp `k`-gram của các nhúng, tạo ra một bản đồ tính năng. toàn cầu max-pooling trên bản đồ đó chọn kích hoạt mạnh nhất. Concatenate max-pooled đầu ra từ nhiều độ rộng bộ lọc. cung cấp cho một đầu phân loại.

> **TextCNN**(Kim, 2014)  Địa chỉ được đặt vào                                                                                                                                                                                                                                     `k`                                                                                                                                                                                                                                                              `k`-gram 嵌入上滑波器,产生特征图――对该特征图做全局最大化选取最强激活――从多个波器宽度最大化输出拼接――送进分类器头――

Tại sao nó hoạt động. Một bộ lọc là một n-gram có thể học được. Max-pooling là không thay đổi vị trí, vì vậy "không tốt" bắn cùng một tính năng vào đầu hoặc giữa một đánh giá. Ba chiều rộng bộ lọc với mỗi bộ lọc 100 cho bạn 300 máy dò n-gram học.

> Tại sao có hiệu quả. 波器 là n-gram có thể học được. 池化最大是位置不变,所以"không tốt" 在评论开头或中间触发相同特征.

**RNN.**Mỗi bước đi`t`, trạng thái ẩn`h_t = f(W * x_t + U * h_{t-1} + b)`- Chia sẻ`W`- `U`- `b`Trong thời gian, trong trạng thái ẩn trong thời gian.`T`là một bản tóm tắt của toàn bộ tiền tố.`h_1 ... h_T`(tối đa, trung bình hoặc cuối cùng).

> **RNN。**Trong mỗi bước thời gian`t`, trạng thái ẩn`h_t = f(W * x_t + U * h_{t-1} + b)``W``U``b`跨时间共享──时间 `T`Các trạng thái ẩn là tổng kết của toàn bộ phần trước.`h_1 ... h_T`上池化(最大、平均值或最后)

Các RNN đơn giản bị biến mất gradient.**LSTM**thêm các cổng quyết định những gì để quên, những gì để lưu trữ, và những gì để ra, ổn định gradient thông qua chuỗi dài.**GRU**đơn giản hóa LSTM thành hai cổng; hoạt động tương tự với ít tham số hơn.

> Thông thường RNN  tồn tại vấn đề biến mất cấp độ.**LSTM**Thêm quyết định quên những gì ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư ư**GRU**Lần đầu tiên, các công cụ này được phân tích với các phương pháp khác nhau.

**Bidirectional RNNs**chạy một RNN về phía trước và một RNN trở lại, liên kết các trạng thái ẩn.

> **双向 RNN**运行一个RNN向前、另一个向后,拼接隐藏状态──每个代币的表示看左右两侧的上下文──对标注任务必不可少──

> **【拓展：大语言模型的工程实践】**Từ GPT đến ChatGPT, NLP đã trải qua sự chuyển đổi từ "mỗi nhiệm vụ đào tạo một mô hình" đến "một mô hình giải quyết tất cả các nhiệm vụ". Trong công trình thực tế, việc triển khai LLM cần phải xem xét các vấn đề như: giới hạn token, trì hoãn, chi phí, kiểm tra an toàn, và các vấn đề khác.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) là cấu trúc phổ biến nhất trong ứng dụng AI của doanh nghiệp hiện tại: sẽ truy vấn người dùng trước tiên truy vấn các đoạn tài liệu liên quan, tiếp tục truy vấn kết quả như trên dưới đây cho LLM 生成答案──

> **【拓展：NLP 的多语言挑战】**Trên toàn cầu có hơn 7000 ngôn ngữ, nhưng nghiên cứu về NLP tập trung chủ yếu vào tiếng Anh và một số ít ngôn ngữ.

## Hãy xây dựng nó.

> **【中文解读】**本节通过代码实现核心算法从零――这种" từ đầu"的方式能帮助理解框架背后的原理,遇到问题时不会被黑盒困住――
```figure
rnn-unroll
```

## Hãy xây dựng nó

### Bước 1: TextCNN bằng PyTorch

```python
import torch
import torch.nn as nn
import torch.nn.functional as F


class TextCNN(nn.Module):
    def __init__(self, vocab_size, embed_dim, n_classes, filter_widths=(2, 3, 4), n_filters=64, dropout=0.3):
        super().__init__()
        self.embed = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
        self.convs = nn.ModuleList([
            nn.Conv1d(embed_dim, n_filters, kernel_size=k)
            for k in filter_widths
        ])
        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(n_filters * len(filter_widths), n_classes)

    def forward(self, token_ids):
        x = self.embed(token_ids).transpose(1, 2)
        pooled = []
        for conv in self.convs:
            c = F.relu(conv(x))
            p = F.max_pool1d(c, c.size(2)).squeeze(2)
            pooled.append(p)
        h = torch.cat(pooled, dim=1)
        return self.fc(self.dropout(h))
```

- `transpose(1, 2)`hình dạng lại `[batch, seq_len, embed_dim]`đến`[batch, embed_dim, seq_len]`Vì `nn.Conv1d`xử lý trục trung tâm như các kênh.

> `transpose(1, 2)`sẽ`[batch, seq_len, embed_dim]`重塑为 `[batch, embed_dim, seq_len]`Vì`nn.Conv1d`Để xem trọng tâm như đường dẫn.

### Bước 2: Định dạng LSTM

```python
class LSTMClassifier(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_dim, n_classes, bidirectional=True, dropout=0.3):
        super().__init__()
        self.embed = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
        self.lstm = nn.LSTM(embed_dim, hidden_dim, batch_first=True, bidirectional=bidirectional)
        factor = 2 if bidirectional else 1
        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(hidden_dim * factor, n_classes)

    def forward(self, token_ids):
        x = self.embed(token_ids)
        out, _ = self.lstm(x)
        pooled = out.max(dim=1).values
        return self.fc(self.dropout(pooled))
```

Max-pool trên chuỗi, không phải là pool trạng thái cuối cùng. Đối với phân loại, max-pooling thường đánh bại việc lấy trạng thái ẩn cuối cùng vì thông tin ở cuối một chuỗi dài có xu hướng thống trị trạng thái cuối cùng.

> Trong chuỗi, tập hợp tối đa hơn là tập hợp trạng thái cuối cùng. Đối với phân loại, tập hợp tối đa thường tốt hơn so với tập hợp trạng thái ẩn cuối cùng, vì thông tin ở cuối chuỗi dài có xu hướng dẫn trạng thái cuối cùng.

### Bước 3: trình diễn gradient biến mất (thấu hiểu)

Một RNN đơn giản mà không có gài không thể học các phụ thuộc tầm xa.`A`xuất hiện ở bất cứ đâu trong một chuỗi.`A`Nếu các hàm này được chuyển đổi từ 0 đến 0, thì các hàm này sẽ được chuyển đổi từ 0 đến 0, nếu chúng ở vị trí 1 và chuỗi dài 100 token, độ lệch từ mất mát phải chảy trở lại thông qua 99 lần của trọng lượng tái phát.

> Không có kiểm soát trong RNN thông thường không thể học được.`A`Có phải hiện diện ở bất kỳ vị trí nào trong chuỗi. Nếu.`A`Ở vị trí 1, độ dài chuỗi là 100, độ mất phải đi qua 99 lần vòng xoay trọng lượng của trọng lượng. Nếu trọng lượng nhỏ hơn 1, độ biến mất. Nếu lớn hơn 1, độ nổ.

```python
def vanishing_gradient_sim(seq_len, recurrent_weight=0.9):
    import math
    return math.pow(recurrent_weight, seq_len)


# At weight=0.9 over 100 steps:
#   0.9 ^ 100 ≈ 2.7e-5
# The gradient from step 100 to step 1 is effectively zero.
```

LSTMs sửa chữa điều này với một **cell state**Các GRU làm điều tương tự với ít tham số hơn. Cả hai đều cung cấp cho bạn đào tạo ổn định thông qua 100+ chuỗi bước.

> LSTM  thông qua một**细胞状态** sửa chữa vấn đề này, trạng thái này chỉ thông qua tăng thêm giao tiếp xuyên mạng                                                                                                                                                                                                                                                      

### Bước 4: tại sao điều này vẫn chưa đủ

Ba vấn đề vẫn tồn tại ngay cả với LSTM.

> Ngay cả khi có LSTM, ba vấn đề vẫn tồn tại.

1. **Sequential bottleneck.**Việc đào tạo một RNN trên một chuỗi dài 1000 đòi hỏi 1000 bước tiến/lái lại hàng loạt. Không thể song song qua thời gian.
   **顺序瓶颈。**Trong một chuỗi dài dài 1000, RNN cần 1000 bước thẳng/ ngược chiều liên tục. Không thể vượt qua thời gian.
2. **Fixed-size context vector in encoder-decoder setups.**Các bộ giải mã chỉ nhìn thấy trạng thái ẩn cuối cùng của bộ mã hóa, được nén trên toàn bộ đầu vào.
   **编码器-解码器中的固定大小上下文向量。**解码器 chỉ nhìn thấy trạng thái ẩn cuối cùng của 编码器, nén toàn bộ nhập.
3. **Distant-dependency accuracy ceiling.**LSTM vượt trội hơn RNN đơn giản nhưng vẫn gặp khó khăn trong việc truyền bá thông tin cụ thể qua hơn 200 bước.
   **远距离依赖准确率天花板。**LSTM 优于普通RNN, nhưng vẫn còn khó khăn trong việc truyền tải thông tin cụ thể giữa 200 + bước.

Sự chú ý đã giải quyết cả ba, biến đổi đã giảm hoàn toàn sự tái phát, bài học 10 là trọng tâm.

> chú ý giải quyết tất cả ba vấn đề. Transformer hoàn toàn từ bỏ vòng lặp.

> **【中文解读】**Bài này sẽ trình bày cách sử dụng một khung đã phát triển như PyTorch, HuggingFace, và các khác.

> **【拓展：Prompt Engineering 与 LLM 应用】**Kỹ thuật nhanh chóng đã trở thành kỹ năng cốt lõi của các kỹ sư NLP. Từ Zero-shot đến Few-shot, từ Chain-of-Thought đến ReAct, các chiến lược khác nhau áp dụng cho các tình huống khác nhau. Trong các dự án thực tế, thiết kế của System提示(System Prompt) ảnh hưởng trực tiếp đến sự ổn định và chất lượng sản xuất của ứng dụng LLM.

## Hãy sử dụng nó để thực hiện

PyTorch's `nn.LSTM`- `nn.GRU`, và`nn.Conv1d`Có thể làm việc với các nhà sản xuất.

> PyTorch của `nn.LSTM``nn.GRU`和 `nn.Conv1d`                                                                                                                                                                                                                                                              

Chuyển mặt tàu được đào tạo trước khi nhúng bạn cắm vào như là lớp đầu vào:

> Hugging Face 提供预训嵌入作为输入层插入:

```python
from transformers import AutoModel

encoder = AutoModel.from_pretrained("bert-base-uncased")
for param in encoder.parameters():
    param.requires_grad = False


class BertCNN(nn.Module):
    def __init__(self, n_classes, filter_widths=(2, 3, 4), n_filters=64):
        super().__init__()
        self.encoder = encoder
        self.convs = nn.ModuleList([nn.Conv1d(768, n_filters, kernel_size=k) for k in filter_widths])
        self.fc = nn.Linear(n_filters * len(filter_widths), n_classes)

    def forward(self, input_ids, attention_mask):
        with torch.no_grad():
            out = self.encoder(input_ids=input_ids, attention_mask=attention_mask).last_hidden_state
        x = out.transpose(1, 2)
        pooled = [F.max_pool1d(F.relu(conv(x)), kernel_size=conv(x).size(2)).squeeze(2) for conv in self.convs]
        return self.fc(torch.cat(pooled, dim=1))
```

Danh sách kiểm tra khi nào phù hợp với giới hạn.

> 适用约束检查清单──

- **Edge / on-device inference.**TextCNN với nhúng GloVe nhỏ hơn 10-100 lần so với một biến thể. Nếu mục tiêu triển khai của bạn là điện thoại, đây là đống.
  **边缘/设备端推理。**带 GloVe 嵌入的 TextCNN 比变压器 小 10-100倍──如果部署目标是手机,这就是你的技术──
- **Streaming / online classification.**RNN xử lý một token một lúc; các bộ chuyển đổi cần toàn bộ chuỗi. Đối với văn bản nhập vào thời gian thực, LSTM vẫn thắng.
  **流式/在线分类。**RNN Mỗi lần xử lý một token; Transformer  cần toàn bộ chuỗi.
- **Tiny models for baselines.**Lập trình nhanh trên một nhiệm vụ mới.
  **用于基线的微型模型。**Trong nhiệm vụ mới, nhanh chóng thay đổi. Trong CPU, 5 phút tập một TextCNN.
- **Sequence labeling with limited data.**BiLSTM-CRF (câu 06), vẫn là một kiến trúc NER cấp sản xuất cho 1k-10k đánh dấu câu.
  **数据有限的序列标注。**BiLSTM-CRF (第 06 课) Đối với 1k-10k 标注句子 vẫn là sản xuất cấp NER 架构。

Mọi thứ khác đều đi đến một bộ biến đổi.

> Mọi thứ khác với Transformer.

> **【中文解读】**Phần này tập trung vào cách phân phối mô hình như một sản phẩm có thể sử dụng.

## Chuyển nó đi.

Cứ như `outputs/prompt-text-encoder-picker.md`- Có thể là:

> 保存为 `outputs/prompt-text-encoder-picker.md`- Có thể là:

```markdown
---
name: text-encoder-picker
description: Pick a text encoder architecture for a given constraint set.
phase: 5
lesson: 08
---

Given constraints (task, data volume, latency budget, deploy target, compute budget), output:

1. Encoder architecture: TextCNN, BiLSTM, BiLSTM-CRF, transformer fine-tune, or "use a pretrained transformer as a frozen encoder + small head".
2. Embedding input: random init, GloVe / fastText frozen, or contextualized transformer embeddings.
3. Training recipe in 5 lines: optimizer, learning rate, batch size, epochs, regularization.
4. One monitoring signal. For RNN/CNN models: attention mechanism absence means they miss long-range deps; check per-length accuracy. For transformers: fine-tuning collapse if LR too high; check train loss.

Refuse to recommend fine-tuning a transformer when data is under ~500 labeled examples without showing that a TextCNN / BiLSTM baseline has plateaued. Flag edge deployment as needing architecture-before-everything.
```

> **【中文解读】**练题按照 Easy/Medium/Hard 三个难度递进;;建议至少完成 级别的题目, 级别适合深入研究或面试准备;;

## Tập luyện bài tập

1. **Easy.**Đào tạo một TextCNN trên một bộ dữ liệu đồ chơi 3 lớp (bạn phát minh ra dữ liệu).
   **简单。**Trong một tập dữ liệu 3 loại đồ chơi trên tập luyện TextCNN(((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((
2. **Medium.**Thực hiện tập hợp tối đa, trung bình và trạng thái cuối cùng cho trình phân loại LSTM. So sánh trên một tập dữ liệu nhỏ; tài liệu tập hợp nào thắng và giả định lý do tại sao.
   **中等。**Để LSTM phân loại đạt được tối đa phân tích, trung bình phân tích và cuối cùng phân tích trạng thái.
3. **Hard.**Xây dựng thẻ BiLSTM-CRF NER (combination lesson 06 and this one). Trén trên CoNLL-2003. So sánh với CRF-Alone baseline từ lesson 06 và BERT fine-tune.
   **困难。** cấu trúc BiLSTM-CRF NER 标标标器(结合第 06 课和本课) ⋅ 在 CoNLL-2003 上训练──与第 06 课的纯CRF基线和BERT 微调比较──报告训练时间、内存和F1──

> **【中文解读】**Trong 术语表中的"Những gì mọi người nói" vs "Những gì nó thực sự có nghĩa" 区分日常口语和精确技术含义── 在团队协作中,统一术语定义可以避免大量沟通误解──

## Từ khóa  Từ khóa nhanh chóng

| Term / 术语 | What people say / 人们常说的 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| TextCNN | CNN for text / 文本 CNN | Stack of 1D convolutions over word embeddings with global max-pool. Kim (2014). / 在词嵌入上堆叠一维卷积加全局最大池化。Kim (2014)。 |
| RNN（循环神经网络） | Recurrent net / 循环网络 | Hidden state updated at each time step: `h_t = f(W x_t + U h_{t-1})`. / 每个时间步更新隐藏状态：`h_t = f(W x_t + U h_{t-1})`。 |
| LSTM | Gated RNN / 门控 RNN | Adds input / forget / output gates + a cell state. Trains stably through long sequences. / 添加输入/遗忘/输出门 + 细胞状态。在长序列上稳定训练。 |
| GRU | Simpler LSTM / 更简单的 LSTM | Two gates instead of three. Similar accuracy, fewer parameters. / 两个门代替三个。类似准确率，更少参数。 |
| Bidirectional（双向） | Both directions / 两个方向 | Forward + backward RNN concatenated. Every token sees both sides of its context. / 前向 + 后向 RNN 拼接。每个 token 看到其上下文两侧。 |
| Vanishing gradient（梯度消失） | Training signal dies / 训练信号消失 | Repeated multiplication by <1 weights in plain RNNs makes early-step gradients effectively zero. / 普通 RNN 中对小于 1 的权重反复乘法使早期步骤的梯度实际上为零。 |

> **【中文解读】**延伸阅读 cung cấp các nguồn chất lượng cao cho việc học sâu. Những bài báo và giảng dạy này là tài liệu tham khảo cổ điển trong lĩnh vực này, phù hợp với những người đọc cần hiểu sâu hơn.

## Xem thêm 延伸阅读

- [Kim, Y. (2014). Convolutional Neural Networks for Sentence Classification](https://arxiv.org/abs/1408.5882) bài báo TextCNN. 8 trang. Đọc được. / TextCNN 论文──八页──易读──
- [Hochreiter, S. and Schmidhuber, J. (1997). Long Short-Term Memory](https://www.bioinf.jku.at/publications/older/2604.pdf) bài báo LSTM. Không ngờ sáng suốt. / LSTM 论文──出乎意料地清晰──
- [Olah, C. (2015). Understanding LSTM Networks](https://colah.github.io/posts/2015-08-Understanding-LSTMs/) các sơ đồ làm cho LSTMs có thể tiếp cận được với tất cả mọi người. / 让 LSTM đối với mọi người trở nên dễ hiểu.
