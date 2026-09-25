# Xây dựng một Transformer từ đầu  The Capstone  Từ zero xây dựng Transformer  毕业项目

> 13 bài học, 1 mô hình, không có lối tắt.

> **【中文解读】**Kết hợp tất cả kiến thức, từ zero thực hiện hoàn chỉnh GPT cấu trúc. Đây là thực hành cốt lõi của giai đoạn này.

**Type:** Hands-on | **类型:** 动手
**Language:**Python**语言:**Python
**Prerequisites:** Phase 7 · 01 through 13. Don't skip. | **前置知识:** Phase 7 · 01 through 13. Don't skip.
**Time:** ~120 minutes | **时间:** ~120 分钟

## Vấn đề  vấn đề giới thiệu

Bạn đã đọc mọi bài báo, bạn đã thực hiện sự chú ý, chia chia nhiều đầu, mã hóa vị trí, mã hóa và mã hóa khối, BERT và GPT mất mát, MoE, KV cache. Bây giờ làm cho chúng làm việc cùng nhau trên một nhiệm vụ thực sự.

> Bạn đã đọc từng bài báo. Bạn đã thực hiện sự chú ý, nhiều phân chia, lập trình vị trí, lập trình và mã hóa khối, BERT và GPT mất mát, MOE, KV 缓存. Bây giờ hãy để chúng cùng nhau làm việc trên một nhiệm vụ thực sự.

Chất cốt: đào tạo một bộ biến đổi nhỏ chỉ có trình giải mã từ đầu đến cuối trong một nhiệm vụ mô hình hóa ngôn ngữ cấp độ nhân vật. Nó đọc Shakespeare. Nó tạo ra Shakespeare mới. Nó đủ nhỏ để đào tạo trên máy tính xách tay trong vòng chưa đầy 10 phút. Nó đủ chính xác rằng việc trao đổi trong một tập dữ liệu lớn hơn và đào tạo lâu hơn sẽ giúp bạn có một LM thực sự.

> 毕业项目: 在字符级语言建模任务上端到端训练一个小型解码器专用变压器──它读 Shakespeare,生成新的 Shakespeare──它足够小,可以在笔记本上完成训练在10分钟内──它足够正确,转换成更大的数据集和更长的训练时间就能得到真正的语言模型──

Đây là "nanoGPT" của khóa học. Nó không phải là gốc  Karpathy's 2023 nanoGPT hướng dẫn là thực hiện tham chiếu mỗi học sinh viết ít nhất một lần. Chúng tôi nâng hình dạng và tái cấu trúc nó xung quanh những gì chúng tôi đã bao gồm.

> Đây là "nanoGPT" của chương trình. Nó không phải là bản gốc của Karpathy năm 2023 chương trình nanoGPT là mỗi học sinh viết ít nhất một lần để thực hiện tham khảo. Chúng tôi đã lấy cấu trúc của nó và được cải tạo dựa trên nội dung mà chúng tôi đã học.

> **【中文解读】**Dự án này sẽ được thực hiện trong 13 phần của khóa học: mã hóa ngôn ngữ xây dựng, mã hóa, đặt khoá, RMSNorm, nhiều nguyên nhân, tập trung vào các kết nối, đào tạo một máy Shakespeare sinh sản có thể hoàn thành trong 10 phút trên sổ cái. Mặc dù nhỏ, nhưng cấu trúc tương tự như GPT-4 tăng dữ liệu lớn và số lượng đào tạo để có thể có được mô hình ngôn ngữ thực sự.

> **【拓展：从 nanoGPT 到生产级 LLM】**Karpathy's nanoGPT là điểm khởi đầu tốt nhất để học Transformer. Sự khác biệt quan trọng của nanoGPT đến cấp sản xuất LLM là: quy mô dữ liệu (bởi MB đến TB) ✓ cơ sở hạ tầng đào tạo (bởi GPU đơn đến hàng ngàn GPU) ✓ đào tạo phân tán (bởi dữ liệu và dòng chảy) ✓ và đào tạo sau (bởi SFT + RLHF) ✓ nhưng cấu trúc cốt lõi là giống nhau.

## Khái niệm cốt lõi

![Transformer-from-scratch block diagram](../assets/capstone.svg)

Kiến trúc, ghi chú:

> 架构,带注释:

```
input tokens (B, N)
   │
   ▼
token embedding + positional embedding  ◀── Lesson 04 (RoPE option)
   │
   ▼
┌──── block × L ────────────────────┐
│  RMSNorm                          │  ◀── Lesson 05
│  MultiHeadAttention (causal)      │  ◀── Lesson 03 + 07 (causal mask)
│  residual                         │
│  RMSNorm                          │
│  SwiGLU FFN                       │  ◀── Lesson 05
│  residual                         │
└────────────────────────────────── ┘
   │
   ▼
final RMSNorm
   │
   ▼
lm_head (tied to token embedding)
   │
   ▼
logits (B, N, V)
   │
   ▼
shift-by-one cross-entropy            ◀── Lesson 07
```

### Những gì chúng ta vận chuyển

> Chúng tôi giao dịch nội dung:

- `GPTConfig` một nơi để cấu hình tất cả các siêu tham số.
  Trung ngữ翻译:`GPTConfig` Một vị trí đặt tất cả các siêu参数
- `MultiHeadAttention` nguyên nhân, đợt, với hướng theo kiểu Flash tùy chọn (PyTorch's `scaled_dot_product_attention`().
  Trung ngữ翻译:`MultiHeadAttention` 因果的、批量,可选闪光 风格路径(PyTorch của `scaled_dot_product_attention`(■)
- `SwiGLUFFN` FFN hiện đại.
  Trung ngữ翻译:`SwiGLUFFN` 现代 FFN。
- `Block` trước chuẩn, lưu tâm bao bì dư thừa + FFN.
  Trung ngữ翻译:`Block` 前归一化,残差包裹的注意力 + FFN。
- `GPT` nhúng, khối xếp chồng, đầu LM, tạo().
  Trung ngữ翻译:`GPT` 嵌入、堆叠块、LM 头、生成()
- Chuyện tập với AdamW, cosine LR, cắt gradient.
  Trung ngữ翻译:带 AdamW、余弦学习率、梯度裁剪的训练循环──
- Đồ ký cấp Char về văn bản Shakespeare.
  Trung文翻译:Shakespeare 文本上的字符级分词器──

> **【中文解读】**完整的GPT 实现包含:配置类型、多头因果注意力(可选 Flash Attention)、SwiGLU FFN、前归归归归化残差块、完整的GPT 模型类型(嵌入 + 堆叠块 + LM 头 + 生成函数)、AdamW + 余弦学习率训练循环──为了简洁,使用学习式位置嵌入(而不是RoPE) 并实现KV 缓存,但练习要求你添加这些──

### Những gì chúng ta không vận chuyển

> Chúng tôi không giao hàng nội dung:

- RoPE  được thực hiện theo khái niệm trong Bài học 04. Ở đây chúng tôi sử dụng các tích hợp vị trí được học để đơn giản hóa.
  Trong bài học thứ 4, RoPE có khái niệm thực hiện.
- KV cache trong quá trình tạo  mỗi bước tạo tính lại sự chú ý trên tiền tố đầy đủ. chậm hơn nhưng đơn giản hơn. Các bài tập yêu cầu bạn thêm một cache KV.
  Trung ngữ翻译:生成时的 KV 缓存  Mỗi bước tạo lên toàn bộ trước 重新计算注意力──慢慢但更简单──练习要求你添加 KV 缓存──
- Flash Attention  PyTorch 2.0+ tự động gửi nếu đầu vào phù hợp; chúng tôi sử dụng `F.scaled_dot_product_attention`- Tôi không biết.
  Trung文翻译:Flash Attention  PyTorch 2.0+ 在输入匹配时自动分派;我们使用 `F.scaled_dot_product_attention`
- MoE  một FFN mỗi khối. Bạn đã xem MoE trong Bài học 11.
  Trung ngữ翻译:Moe  每块单个FFN──你在第11课见过Moe──

### Các số liệu mục tiêu

Trên máy tính xách tay Mac M2, một máy tính xách tay 4 tầng, 4 đầu, d_model=128 GPT được đào tạo cho 2.000 bước trên `tinyshakespeare.txt`- Có thể là:

> Trong Mac M2 笔记本上,4 层、4 头、d_model=128 của GPT trong `tinyshakespeare.txt`上训练 2000 步:

- Khối mất tập luyện hội tụ từ ~ 4,2 (thuộc tình cờ) đến ~ 1,5 trong khoảng 6 phút.
  Trung ngữ翻译: training loss từ khoảng 4.2(随机) trong khoảng 6 phút nhận được đến khoảng 1,5。
- Kết quả lấy mẫu trông hình Shakespeare: từ cổ điển, đoạn đường, tên thích hợp như "ROMEO:" xuất hiện.
  Trung ngữ翻译:采样输出看起来像莎士比亚:古词、换行、"ROMEO:"等专名词出现──
- Sự mất mát của Val (từ 10% cuối cùng của văn bản) theo dõi chặt chẽ sự mất mát của đào tạo; không quá phù hợp với quy mô/ ngân sách này.
  Trung ngữ翻译:验证损失 (留出最后10%的文本)紧跟训练损失; không quá phù hợp với quy mô/ ngân sách này.

> **【拓展：从字符级到子词级 Tokenizer】**本项目使用字符级代币器(简单但低效) ――生产级 LLM 使用 BPE(Byte Pair Encoding) 或 SentencePiece 等子词级代币器──Llama 使用 BPE,GPT-4 使用 cl100k_base BPE tokenizer──子词代币化 在词汇量、序列长度和语义粒度之间取得平衡,是现代 LLM的标配──

## Hãy xây dựng nó.
```figure
n5-block-stack
```

## Hãy xây dựng nó

Bài học này sử dụng PyTorch.`torch`(Phát triển CPU là tốt).`code/main.py`- Lịch bản xử lý:

> 本课使用 PyTorch。安装 `torch`(CPU 版本即可)`code/main.py`❖ 該脚本处理:

- Tải xuống `tinyshakespeare.txt`nếu thiếu (hoặc đọc bản sao địa phương).
  Trung文翻译: Nếu thiếu thì xuống `tinyshakespeare.txt`(或读取本地副本)
- Tầm biểu tượng cấp độ byte.
  Trung ngữ翻译:字节级字符分词器──
- Đường lửa/vùng chia ở 90/10.
  Trung ngữ翻译:90/10 的训练/验证分割──
- Chuyển tập vòng với bf16 tự độngcast trên phần cứng hỗ trợ.
  Trung文翻译:支持硬件上的 bf16 自动混合精度训练循环──
- Việc lấy mẫu sau khi huấn luyện hoàn thành.
  Trung ngữ翻译:训练完成后的采样──

### Bước 1: dữ liệu

```python
text = open("tinyshakespeare.txt").read()
chars = sorted(set(text))
stoi = {c: i for i, c in enumerate(chars)}
itos = {i: c for c, i in stoi.items()}
encode = lambda s: [stoi[c] for c in s]
decode = lambda xs: "".join(itos[x] for x in xs)
```

65 ký tự độc đáo, từ vựng nhỏ, có kích thước từ vựng 4byte, không có BPE, không có kịch bản token.

> 65 个唯一字符──微型词表──适配 4 字节 vocab_size──没有 BPE,没有分词器的麻烦──

### Bước 2: mô hình

Nhìn xem`code/main.py`. Bảng là sách giáo khoa từ Bài học 05  chuẩn trước, RMSNorm, SwiGLU, MHA nguyên nhân.

> 参见 `code/main.py`△ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △

### Bước 3: vòng đào tạo

Nhận một loạt các cửa sổ biểu tượng dài 256 trước, chuyển đổi qua một, ngược, bước AdamW, ghi lại, lặp lại.

> 获取随机批量长度为 256 标签窗口──前向传播──偏移一位的交叉──反向传播──AdamW 步进──记录──重复──

```python
for step in range(max_steps):
    x, y = get_batch("train")
    logits = model(x)
    loss = F.cross_entropy(logits.view(-1, vocab_size), y.view(-1))
    loss.backward()
    torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
    opt.step()
    opt.zero_grad()
```

### Bước 4: mẫu

Khi được yêu cầu, liên tục chuyển tiếp, lấy mẫu từ các log top-p, thêm vào, và tiếp tục.

> 给定一个提示,反复前向传播, từ top-p logits 采样,追加,继续──500 个标志 后停止──

### Bước 5: đọc đầu ra

Sau 2.000 bước:

> 2000 bước sau:

```
ROMEO:
Away and mild will not thy friend, that thou shalt wit:
The chief that well shame and hath been his friends,
...
```

Không phải Shakespeare, nhưng hình Shakespeare, một chiến thắng rõ ràng với khoảng 800K tham số và 6 phút trên máy tính xách tay.

> Không phải Shakespeare, nhưng như Shakespeare, khoảng 800K người đã thắng trong 6 phút.

## Hãy sử dụng nó để thực hiện

Ngọc đá này là một kiến trúc tham chiếu.

> Dự án này là một cấu trúc tham khảo.

1. **Swap the tokenizer.**Sử dụng BPE (ví dụ:`tiktoken.get_encoding("cl100k_base")`(Vocal size jumps from 65 to ~ 50,000.
   Trung ngữ翻译:**替换分词器。**Sử dụng BPE`tiktoken.get_encoding("cl100k_base")`(■) Từ表大小 từ 65 跳到约50,000――模型容量需要相应扩展――
2. **Train on a bigger corpus.**Sử dụng `OpenWebText`hoặc `fineweb-edu`(HuggingFace). 10B token trên một A100 chỉ mất khoảng 24 giờ để có được một GPT 125M-param.
   Trung ngữ翻译:**在更大的语料上训练。**Sử dụng `OpenWebText`Hoặc`fineweb-edu`(HuggingFace) ―― 在单张 A100 上用10B token 训练 125M 参数 GPT 约需24小时──
3. **Add RoPE + KV cache + Flash Attention.**Các bài tập dưới đây sẽ hướng dẫn bạn thông qua từng bài tập.
   Trung ngữ翻译:**添加 RoPE + KV 缓存 + Flash Attention。**Bài tập sau đây sẽ hướng dẫn bạn hoàn thành từng bước.

Điều này kết thúc như một GPT 125M tham số mà tạo ra tiếng Anh lưu động. Không phải là mô hình biên giới. Nhưng cùng một đường mã  chỉ lớn hơn  là những gì Karpathy, EleutherAI, và Viện Allen sử dụng để đào tạo các điểm kiểm soát nghiên cứu vào năm 2026.

> Cuối cùng có được một có thể tạo ra một dòng chảy tiếng Anh 125M 参数 GPT── không phải là mô hình tiền tuyến── nhưng cùng một mã chỉ là lớn hơn là Karpathy、EleutherAI 和 Allen Institute trong năm 2026 được sử dụng trong các điểm kiểm tra nghiên cứu.

> **【拓展：Karpathy 的 nanoGPT 与教育意义】**Andrej Karpathy's nanoGPT(2023) là một trong những bài học có ảnh hưởng nhất trong lịch sử giáo dục AI. Nó chứng minh một GPT hoàn chỉnh có thể được đào tạo có thể được thực hiện bằng khoảng 300 bài PyTorch.

## Chuyển nó đi.

Nhìn xem`outputs/skill-transformer-review.md`. Kỹ năng xem xét việc thực hiện biến đổi từ đầu để xác định tính chính xác trong tất cả 13 bài học trước đó.

> 参见 `outputs/skill-transformer-review.md`◊ Kỹ năng này kiểm tra một biến thể xây dựng từ không thực hiện, kiểm tra tất cả các bài học trước 13 

## Tập luyện bài tập

1. **Easy.**Đi chạy`code/main.py`Hãy xác minh rằng mất tích xác thực bước cuối cùng của mô hình được đào tạo của bạn là dưới 2.0. Thay đổi `max_steps`từ 2.000 đến 5.000  liệu sự mất val tiếp tục cải thiện?
   Trung ngữ翻译:运行 `code/main.py`❖ Thiết lập mô hình đào tạo của bạn bước cuối cùng ❖ Thiết lập mất mát thấp hơn 2.0 ❖`max_steps`Từ 2,000 改 thành 5,000  chứng nhận mất tích có tiếp tục cải thiện không?
2. **Medium.**Thay thế các embedment vị trí học được bằng RoPE.`MultiHeadAttention`- Đường và xác minh mất val ít nhất là thấp.
   Trung文翻译:用 RoPE 替换学习式位置嵌入──在 `MultiHeadAttention`Trung đối với Q và K  ứng dụng quay lại.
3. **Medium.**Thực hiện một bộ nhớ cache KV trong vòng lấy mẫu. Tạo 500 token với và không có bộ nhớ cache. Clock tường nên được cải thiện 520x trên máy tính xách tay.
   Trong vòng tròn lấy mẫu, KV 缓存── có 缓存 và không 缓存 tạo ra 500 token── trên sổ ghi chép nên có 5-20 lần cải thiện thời gian thực tế──
4. **Hard.**Thêm một đầu thứ hai vào mô hình dự đoán mã thông báo cộng thêm một tiếp theo (MTP  Multi-Token Prediction từ DeepSeek-V3).
   Trung文翻译:添加第二个头预测下一个代币(MTP来自DeepSeek-V3的多代币 预测) ――联合训练――有帮助吗?
5. **Hard.**Thay thế FFN đơn lẻ trên mỗi khối bằng một MoE 4 chuyên gia. Router + top-2 định tuyến. Xem cách mất val thay đổi ở các tham số hoạt động phù hợp.
   Trung ngữ翻译:将每块的单个FFN 替换为4 专家 MoE──路由器 + top-2 路由──观察在匹配活跃参数下验证损失的变化──

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| nanoGPT | "Karpathy's tutorial repo" | Minimal decoder-only transformer training code, ~300 LOC; the canonical reference. |
| nanoGPT | "Karpathy 的教程仓库" | 最小解码器专用 Transformer 训练代码，约 300 行；经典参考。 |
| tinyshakespeare | "The standard toy corpus" | ~1.1 MB of text; every character-LM tutorial since 2015 uses it. |
| tinyshakespeare | "标准玩具语料库" | 约 1.1 MB 文本；自 2015 年以来每个字符级语言模型教程都用它。 |
| Tied embeddings | "Share input/output matrix" | LM head weight = transpose of token embedding matrix; saves parameters, improves quality. |
| 绑定嵌入 | "共享输入/输出矩阵" | LM 头权重 = token 嵌入矩阵的转置；节省参数，提高质量。 |
| bf16 autocast | "Training precision trick" | Run forward/back in bf16, keep optimizer state in fp32; standard since 2021. |
| bf16 自动混合精度 | "训练精度技巧" | 前向/反向用 bf16，优化器状态用 fp32；2021 年以来的标准。 |
| Gradient clipping | "Stops spikes" | Cap global grad norm at 1.0; prevents training blowups. |
| 梯度裁剪 | "阻止尖峰" | 将全局梯度范数限制在 1.0；防止训练爆炸。 |
| Cosine LR schedule | "The 2020+ default" | LR ramps up linearly (warmup) then decays cosine-shaped to 10% of peak. |
| 余弦学习率调度 | "2020+ 默认" | 学习率线性升温（warmup）然后余弦衰减到峰值的 10%。 |
| MFU | "Model FLOP Utilization" | Achieved FLOPs / theoretical peak; 40% dense, 30% MoE is strong in 2026. |
| MFU | "模型 FLOP 利用率" | 实际 FLOPs / 理论峰值；2026 年稠密 40%、MoE 30% 是好的。 |
| Val loss | "Held-out loss" | Cross-entropy on data the model never saw; overfit detector. |
| 验证损失 | "留出损失" | 模型从未见过的数据上的交叉熵；过拟合检测器。 |

## Xem thêm 延伸阅读

- [The Annotated Transformer (Harvard NLP)](https://nlp.seas.harvard.edu/annotated-transformer/) thực hiện thông tin chú thích cổ điển.
  Trung ngữ翻译:哈佛 NLP 的注解版 Transformer,经典参考实现──
