# Mô hình chuỗi-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đối-đ-đối-đối-đối-đ-đối-đối-đ-đ-đ-đ-đ-đ-đ-đ-đ-đ-đ-đ-đ-đ-đ-đ-đ-đ-đ-đ-đ-đ-đ-đ-đ-đ-đ-đ-đ-đ-đ-đ-đ-đ-đ-đ-đ-đ-đ-đ-đ-đ-đ-đ-đ-đ-đ-đ-đ-đ-đ-đ-đ-đ-đ-đ-đ-đ-đ-đ-đ-đ-đ-đ-đ-đ-đ-đ-đ-đ-đ-đ-đ

> Hai người RNN giả vờ là một người dịch, và cái nút thắt họ gặp là lý do sự chú ý tồn tại.
> Hai RNN giả là một dịch giả.

> **【中文解读】**编码器-解码器架构──注意力机制就是为了解决它的瓶而发明的──

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 08 (CNNs + RNNs for Text), Phase 3 · 11 (PyTorch Intro) | **前置知识:** Phase 5 · 08（CNN 和 RNN 文本处理），Phase 3 · 11（PyTorch 入门）
**Time:** ~75 minutes | **时间:** ~75 分钟

## Vấn đề  vấn đề giới thiệu

Việc phân loại lập bản đồ một chuỗi dài biến cho một nhãn duy nhất. Dịch bản đồ một chuỗi dài biến cho một chuỗi dài khác.

> 分类将变长序列映射为单标. 翻译将变长序列映射为另一个变长序列.

Kiến trúc seq2seq (Sutskever, Vinyals, Le, 2014) đã phá vỡ điều này bằng một công thức đơn giản cố ý. Hai RNN. Một đọc câu nguồn và tạo ra một vector ngữ cảnh kích thước cố định.

> Seq2seq 架构(Sutskever, Vinyals, Le, 2014) đã giải quyết vấn đề này bằng một giải pháp đơn giản cố ý.

Điều này đáng để nghiên cứu vì hai lý do. Thứ nhất, nút bốc vắc-tơ ngữ cảnh là thất bại hữu ích nhất về mặt giáo dục trong NLP. Nó thúc đẩy mọi thứ sự chú ý và các bộ biến đổi đều giỏi. Thứ hai, công thức đào tạo (bắt buộc giáo viên, lấy mẫu theo lịch trình, tìm kiếm chùm khi suy luận) vẫn áp dụng cho mọi hệ thống thế hệ hiện đại bao gồm LLM.

> Đây là một trong những lý do đáng để học. Thứ nhất, nó là thất bại của giá trị giảng dạy lớn nhất trong NLP. Nó đã gây ra sự chú ý và biến đổi.

## Khái niệm cốt lõi

> **【中文解读】**Bài viết này giới thiệu các khái niệm và lý thuyết cốt lõi.

**Encoder.**Một RNN đọc câu nguồn.**context vector** một bản tóm tắt quy mô cố định của toàn bộ đầu vào.

> **编码器（Encoder）。**Một bài đọc của RNN.**上下文向量**  整条输入的固定大小摘要──据说不会丢失任何内容的源信息──

**Decoder.**Một RNN khác được khởi tạo từ vector ngữ cảnh. Tại mỗi bước nó lấy token được tạo trước đó như là đầu vào và tạo ra phân phối trên từ vựng mục tiêu. Sample hoặc argmax để chọn token tiếp theo. Đưa nó lại.`<EOS>`token được tạo ra hoặc chiều dài tối đa được đạt.

> **解码器（Decoder）。**Một RNN khác bắt đầu từ trên xuống trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên trên`<EOS>`token hoặc đạt đến độ dài tối đa.

**Training:**Lỡ entropy chéo ở mỗi bước giải mã, tổng hợp qua chuỗi.

> **训练：**Mỗi bước giải mã của giao thông  mất mát, trong chuỗi tìm kiếm trên và  thông qua hai mạng tiêu chuẩn thời gian ngược chiều truyền 

**Teacher forcing.**Trong quá trình đào tạo, đầu vào của máy giải mã theo từng bước `t`là biểu tượng thực tại tại vị trí`t-1`, không phải dự đoán trước của máy giải mã. Điều này ổn định đào tạo; nếu không có nó, sai lầm sớm rơi vào tình trạng ngập và mô hình không bao giờ học.**exposure bias**- Tôi không biết.

> **教师强制（Teacher Forcing）。**训练时,解码器在步骤 `t`Đăng nhập là vị trí`t-1`Đơn vị của* thực* thay vì dự đoán trước của máy giải mã chính nó. Nó đã ổn định được đào tạo; nếu không có nó, các lỗi lầm sớm sẽ không bao giờ được học.**暴露偏差（Exposure Bias）**

**The bottleneck.**Tất cả những gì mà bộ mã hóa đã học về nguồn phải được nén vào một vector ngữ cảnh. Các câu dài mất chi tiết. Các từ hiếm bị mờ. Việc sắp xếp lại (chat noir vs. black cat) phải được ghi nhớ, không phải tính toán.

> **瓶颈。**编码器学到的一切关于源的一切都必须缩小到那一个上下文向量中──长句子丢失细节──罕见词被模糊──重排序(chat noir vs. black cat) phải nhớ, chứ không phải tính toán──

Sự chú ý (câu 10) khắc phục điều này bằng cách cho phép máy giải mã xem * mỗi * trạng thái ẩn của bộ giải mã, không chỉ là trạng thái cuối cùng. Đó là toàn bộ độ.

> 注意力(第 10 课) Bằng cách để giải mã máy xem * mỗi * trình lập trình ẩn tình( không chỉ là cuối cùng) để sửa chữa vấn đề này.

> **【拓展：大语言模型的工程实践】**Từ GPT đến ChatGPT, NLP đã trải qua sự chuyển đổi từ "mỗi nhiệm vụ đào tạo một mô hình" đến "một mô hình giải quyết tất cả các nhiệm vụ". Trong công trình thực tế, việc triển khai LLM cần phải xem xét các vấn đề như: giới hạn token, trì hoãn, chi phí, kiểm tra an toàn, và các vấn đề khác.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) là cấu trúc phổ biến nhất trong ứng dụng AI của doanh nghiệp hiện tại: sẽ truy vấn người dùng trước tiên truy vấn các đoạn tài liệu liên quan, tiếp tục truy vấn kết quả như trên dưới đây cho LLM 生成答案──

> **【拓展：NLP 的多语言挑战】**Trên toàn cầu có hơn 7000 ngôn ngữ, nhưng nghiên cứu về NLP tập trung chủ yếu vào tiếng Anh và một số ít ngôn ngữ.

## Hãy xây dựng nó.

> **【中文解读】**本节通过代码实现核心算法从零――这种" từ đầu"的方式能帮助理解框架背后的原理,遇到问题时不会被黑盒困住――
```figure
lstm-gates
```

## Hãy xây dựng nó

### Bước 1: một bộ mã hóa

```python
import torch
import torch.nn as nn


class Encoder(nn.Module):
    def __init__(self, src_vocab_size, embed_dim, hidden_dim):
        super().__init__()
        self.embed = nn.Embedding(src_vocab_size, embed_dim, padding_idx=0)
        self.gru = nn.GRU(embed_dim, hidden_dim, batch_first=True)

    def forward(self, src):
        e = self.embed(src)
        outputs, hidden = self.gru(e)
        return outputs, hidden
```

`outputs`có hình dạng`[batch, seq_len, hidden_dim]` một trạng thái ẩn cho mỗi vị trí đầu vào. `hidden`có hình dạng`[1, batch, hidden_dim]` bước cuối cùng. Bài học 08 nói "lập lại các đầu ra để phân loại". Ở đây chúng ta giữ trạng thái ẩn cuối cùng như là vector ngữ cảnh, và bỏ qua các đầu ra từng bước.

> `outputs`hình dạng`[batch, seq_len, hidden_dim]` Mỗi nhập vị trí là một trạng thái ẩn.`hidden`hình dạng`[1, batch, hidden_dim]` 最终步 第08 课说"在输出上池化做分类"──这里我们保留最后隐藏状态作为上下文向量,忽略逐步输出──

### Bước 2: một máy giải mã

```python
class Decoder(nn.Module):
    def __init__(self, tgt_vocab_size, embed_dim, hidden_dim):
        super().__init__()
        self.embed = nn.Embedding(tgt_vocab_size, embed_dim, padding_idx=0)
        self.gru = nn.GRU(embed_dim, hidden_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim, tgt_vocab_size)

    def forward(self, token, hidden):
        e = self.embed(token)
        out, hidden = self.gru(e, hidden)
        logits = self.fc(out)
        return logits, hidden
```

Các mã hóa được gọi là một bước một lần. Nhập: một loạt các mã thông báo đơn lẻ và trạng thái ẩn hiện tại.

> 解码器每次调用一步──输入: 一批单个代币 和当前隐藏状态──输出: 下一个代币的词表 logits 和更新后的隐藏状态──

### Bước 3: vòng đào tạo với giáo viên buộc

```python
def train_batch(encoder, decoder, src, tgt, bos_id, optimizer, teacher_forcing_ratio=0.9):
    optimizer.zero_grad()
    _, hidden = encoder(src)
    batch_size, tgt_len = tgt.shape
    input_token = torch.full((batch_size, 1), bos_id, dtype=torch.long)
    loss = 0.0
    loss_fn = nn.CrossEntropyLoss(ignore_index=0)

    for t in range(tgt_len):
        logits, hidden = decoder(input_token, hidden)
        step_loss = loss_fn(logits.squeeze(1), tgt[:, t])
        loss += step_loss
        use_teacher = torch.rand(1).item() < teacher_forcing_ratio
        if use_teacher:
            input_token = tgt[:, t].unsqueeze(1)
        else:
            input_token = logits.argmax(dim=-1)

    loss.backward()
    optimizer.step()
    return loss.item() / tgt_len
```

Hai nút đáng để đặt tên.`ignore_index=0`bỏ qua lỗ trên mã đệm. `teacher_forcing_ratio`là xác suất sử dụng token thực so với dự đoán của mô hình tại mỗi bước. Bắt đầu từ 1.0 (bắt buộc giáo viên đầy đủ) và giảm xuống đến ~0.5 qua đào tạo để đóng cửa khoảng cách thiên vị tiếp xúc.

> Hai yếu tố đáng chú ý:`ignore_index=0`跳过填充代币 上的损失──`teacher_forcing_ratio`là mỗi bước sử dụng mã thông báo thực và tỷ lệ dự đoán mô hình. Từ 1.0(lực lượng giáo viên bắt buộc) bắt đầu, quá trình đào tạo sẽ giảm xuống khoảng 0,5 để giảm khoảng cách chênh lệch.

### Bước 4: vòng suy luận (cười tham)

```python
@torch.no_grad()
def greedy_decode(encoder, decoder, src, bos_id, eos_id, max_len=50):
    _, hidden = encoder(src)
    batch_size = src.shape[0]
    input_token = torch.full((batch_size, 1), bos_id, dtype=torch.long)
    output_ids = []
    for _ in range(max_len):
        logits, hidden = decoder(input_token, hidden)
        next_token = logits.argmax(dim=-1)
        output_ids.append(next_token)
        input_token = next_token
        if (next_token == eos_id).all():
            break
    return torch.cat(output_ids, dim=1)
```

Việc giải mã tham lam chọn token có khả năng cao nhất ở mỗi bước. Nó có thể đi lang thang: một khi bạn cam kết với một token, bạn không thể giải quyết nó. **Beam search**giữ cho hàng đầu...`k`Dòng phân tích sống và chọn điểm số cao nhất hoàn chỉnh ở cuối.

> 贪心解码每步选择最高概率的代币――它可能走偏: một khi bạn gửi một代币,就无法撤回――**束搜索（Beam Search）**保持排名前 `k`Các phần của chuỗi tồn tại, trong cuối cùng chọn phần cao nhất của chuỗi hoàn chỉnh.

### Bước 5: nút chai, được chứng minh

Trình luyện mô hình để làm việc sao chép đồ chơi: nguồn `[a, b, c, d, e]`, mục tiêu`[a, b, c, d, e]`- Tăng chiều dài chuỗi.

> Trong nhiệm vụ chơi game`[a, b, c, d, e]`, mục tiêu `[a, b, c, d, e]`                                                                                                                                                                                                                                                              

```
seq_len=5   copy accuracy: 98%
seq_len=10  copy accuracy: 91%
seq_len=20  copy accuracy: 62%
seq_len=40  copy accuracy: 23%
```

Một trạng thái ẩn GRU duy nhất không thể ghi nhớ một đầu vào 40 token mà không mất. Thông tin ở đó ở mỗi bước mã hóa, nhưng máy giải mã chỉ nhìn thấy trạng thái cuối cùng.

> 单个GRU 隐藏状态无法无损记忆 40 token 输入――信息存在于每个编码器步骤,但解码器只看到最后状态――注意力直接修复这个问题――

> **【中文解读】**Bài này sẽ trình bày cách sử dụng một khung đã phát triển như PyTorch, HuggingFace, và các khác.

> **【拓展：Prompt Engineering 与 LLM 应用】**Kỹ thuật nhanh chóng đã trở thành kỹ năng cốt lõi của các kỹ sư NLP. Từ Zero-shot đến Few-shot, từ Chain-of-Thought đến ReAct, các chiến lược khác nhau áp dụng cho các tình huống khác nhau. Trong các dự án thực tế, thiết kế của System提示(System Prompt) ảnh hưởng trực tiếp đến sự ổn định và chất lượng sản xuất của ứng dụng LLM.

## Hãy sử dụng nó để thực hiện

PyTorch đã có `nn.Transformer`và `nn.LSTM`- dựa trên các mẫu seq2seq.`transformers`các máy tính thư viện đầy đủ các mô hình mã hóa-chế vị (BART, T5, mBART, NLLB) được đào tạo trên hàng tỷ token.

> Có một chiếc đuôi.`nn.Transformer`Và dựa trên`nn.LSTM`模板──Hugging Face 的 模板`transformers`库 cung cấp trên hàng tỷ token  training của mô hình mã hóa hoàn chỉnh  BART、T5、mBART、NLLB)

```python
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tok = AutoTokenizer.from_pretrained("facebook/bart-base")
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-base")

src = tok("Translate this to French: Hello, how are you?", return_tensors="pt")
out = model.generate(**src, max_new_tokens=50, num_beams=4)
print(tok.decode(out[0], skip_special_tokens=True))
```

Các bộ mã hóa-chế vị hiện đại đã loại bỏ RNN cho các bộ biến đổi. Hình dạng cấp cao (chế vị mã hóa, mã hóa, tạo mã thông báo theo mã thông báo) giống nhau với giấy seq2seq 2014. Cơ chế bên trong mỗi khối khác nhau.

> 现代编码器-解码器用变压器 替代了RNN──高层结构(编码器、解码器、个代币 生成) với 2014 seq2seq 论文 hoàn toàn giống nhau── mỗi khối trong cơ chế khác nhau──

### Khi nào vẫn cần tìm ra seq2seq dựa trên RNN

Hầu như không bao giờ, đối với các dự án mới.

> Đối với các dự án mới hầu như không cần thiết:

- Truyền dịch trực tuyến nơi bạn tiêu thụ đầu vào một token một lúc với bộ nhớ bị giới hạn.
  流式翻译, từng token 消耗输入,内存有界──
- Tạo văn bản trên thiết bị nơi chi phí bộ nhớ biến đổi là cấm kỵ.
  设备端文本生成,Tranformator 内存成本过高──
- Nghĩ về rào cản mã hóa và giải mã là cách nhanh nhất để hiểu tại sao các bộ biến đổi thắng.
  Học... hiểu 编码器-解码器瓶 là hiểu 变形为什么胜出最快的路径.

### Sự thiên vị phơi nhiễm và giảm thiểu của nó

- **Scheduled sampling.**Tỷ lệ buộc giáo viên trong quá trình đào tạo để mô hình học cách phục hồi khỏi những sai lầm của mình.
  **计划采样（Scheduled Sampling）。**người giáo viên bị bắt buộc phải bỏ học trong thời gian tập luyện, để học viên có thể phục hồi khỏi những sai lầm của mình.
- **Minimum risk training.**Trén theo điểm số BLEU ở mức câu thay vì sự tham gia chéo ở mức token.
  **最小风险训练（Minimum Risk Training）。**Trong câu cấp BLEU phân số thay vì biểu tượng cấp giao giao giao  trên tập luyện.
- **Reinforcement learning fine-tuning.**Hãy thưởng cho máy phát ra chuỗi bằng một số liệu được sử dụng trong LLM RLHF hiện đại.
  **强化学习微调。**用指标奖励序列生成器──用于现代 LLM 的 RLHF──

Cả ba vẫn áp dụng cho thế hệ dựa trên biến thể.

> Điều này vẫn còn áp dụng cho việc tạo dựa trên Transformer.

> **【中文解读】**Phần này tập trung vào cách phân phối mô hình như một sản phẩm có thể sử dụng.

## Chuyển nó đi.

Cứ như `outputs/prompt-seq2seq-design.md`- Có thể là:

> 保存为 `outputs/prompt-seq2seq-design.md`- Có thể là:

```markdown
---
name: seq2seq-design
description: Design a sequence-to-sequence pipeline for a given task.
phase: 5
lesson: 09
---

Given a task (translation, summarization, paraphrase, question rewrite), output:

1. Architecture. Pretrained transformer encoder-decoder (BART, T5, mBART, NLLB) is the default. RNN-based seq2seq only for specific constraints.
2. Starting checkpoint. Name it (`facebook/bart-base`, `google/flan-t5-base`, `facebook/nllb-200-distilled-600M`). Match the checkpoint to task and language coverage.
3. Decoding strategy. Greedy for deterministic output, beam search (width 4-5) for quality, sampling with temperature for diversity. One sentence justification.
4. One failure mode to verify before shipping. Exposure bias manifests as generation drift on longer outputs; sample 20 outputs at the 90th-percentile length and eyeball.

Refuse to recommend training a seq2seq from scratch for under a million parallel examples. Flag any pipeline that uses greedy decoding for user-facing content as fragile (greedy repeats and loops).
```

> **【中文解读】**练题按照 Easy/Medium/Hard 三个难度递进;;建议至少完成 级别的题目, 级别适合深入研究或面试准备;;

## Tập luyện bài tập

1. **Easy.**Thực hiện nhiệm vụ sao chép đồ chơi. Tập một GRU seq2seq trên các cặp đầu vào-kết ra nơi mục tiêu bằng với nguồn. đo độ chính xác ở độ dài 5, 10, 20.
   **简单。**实现玩具复制任务──训练 GRU seq2seq 在目标等于源的输入输出对上──测量长度 5、10、20 的准确率──复现瓶──
2. **Medium.**Thêm mã hóa tìm kiếm chùm với chiều rộng chùm 3. đo BLEU trên một bộ phận song song nhỏ chống lại tham lam. Tài liệu nơi tìm kiếm chùm thắng (thường là token cuối cùng) và nơi nó không tạo ra sự khác biệt.
   **中等。**添加束宽度为 3束搜索解码──在小平行语料上测量对贪心的蓝色──记录束搜索在哪里胜出(通常是最后几个代币)以及在哪里没有区别──
3. **Hard.**- Đúng rồi.`facebook/bart-base`trên một bộ dữ liệu phác thảo 10k-pair. So sánh đầu ra chùm-4 của mô hình được điều chỉnh tốt với đầu ra cơ bản của mô hình. báo cáo BLEU và chọn 10 ví dụ chất lượng.
   **困难。**Trong 10.000 đối với các bản dữ liệu`facebook/bart-base`◊ trong phần 4 của mô hình so sánh nhỏ trên đầu vào để ra ổng ổng và mô hình cơ bản ⋅ báo cáo BLEU và chọn 10 ví dụ định tính ⋅

> **【中文解读】**Trong 术语表中的"Những gì mọi người nói" vs "Những gì nó thực sự có nghĩa" 区分日常口语和精确技术含义── 在团队协作中,统一术语定义可以避免大量沟通误解──

## Từ khóa  Từ khóa nhanh chóng

| Term / 术语 | What people say / 人们常说的 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| Encoder（编码器） | Input RNN / 输入 RNN | Reads source. Produces per-step hidden states and a final context vector. / 读取源。产生逐步隐藏状态和最终上下文向量。 |
| Decoder（解码器） | Output RNN / 输出 RNN | Initialized from context vector. Generates target tokens one at a time. / 从上下文向量初始化。逐个生成目标 token。 |
| Context vector（上下文向量） | The summary / 摘要 | Final encoder hidden state. Fixed size. The bottleneck attention solves. / 最终编码器隐藏状态。固定大小。注意力解决的瓶颈。 |
| Teacher forcing（教师强制） | Use true tokens / 使用真实 token | Feed the ground-truth previous token at training time. Stabilizes learning. / 训练时馈入真实的前一个 token。稳定学习。 |
| Exposure bias（暴露偏差） | Train/test gap / 训练/测试差距 | Model trained on true tokens never practiced recovering from its own mistakes. / 在真实 token 上训练的模型从未练习从自己的错误中恢复。 |
| Beam search（束搜索） | Better decoding / 更好的解码 | Keep top-k partial sequences alive at each step instead of committing greedily. / 每步保持排名前 k 的部分序列存活，而非贪心提交。 |

> **【中文解读】**延伸阅读 cung cấp các nguồn chất lượng cao cho việc học sâu. Những bài báo và giảng dạy này là tài liệu tham khảo cổ điển trong lĩnh vực này, phù hợp với những người đọc cần hiểu sâu hơn.

## Xem thêm 延伸阅读

- [Sutskever, Vinyals, Le (2014). Sequence to Sequence Learning with Neural Networks](https://arxiv.org/abs/1409.3215) giấy gốc seq2seq. 4 trang. / 原始 seq2seq 论文──四页──
- [Cho et al. (2014). Learning Phrase Representations using RNN Encoder-Decoder for Statistical Machine Translation](https://arxiv.org/abs/1406.1078) giới thiệu GRU và khung mã hóa-bản mã hóa. / 引入了 GRU 和编码器-解码器框架──
- [Bahdanau, Cho, Bengio (2014). Neural Machine Translation by Jointly Learning to Align and Translate](https://arxiv.org/abs/1409.0473) bài tập chú ý. Đọc ngay sau bài học này. / 注意力论文──在本课后立即阅读──
- [PyTorch NLP from Scratch tutorial](https://pytorch.org/tutorials/intermediate/seq2seq_translation_tutorial.html) xây dựng seq2seq + mã chú ý. / 可构建的 seq2seq + 注意力代码。
