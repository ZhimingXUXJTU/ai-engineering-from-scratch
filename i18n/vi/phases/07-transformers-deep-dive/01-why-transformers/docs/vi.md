# Tại sao Transformers  Các vấn đề với RNN
# Tại sao là vấn đề của Transformer  RNN

> RNN xử lý các token một lần. Transformers xử lý tất cả các token cùng một lúc. Đặt cược kiến trúc duy nhất đó đã thay đổi mọi đường cong quy mô trong học sâu sau năm 2017.

> RNN 个别处理 token──Transformer 一次性处理所有 token──This one architecture注 改变了2017年后深度学习中的每条扩展曲线──

> **【中文解读】**RNN có ba vấn đề chết người: không thể đi cùng, độ dài biến mất, độ dài cố định.

**Type:** Learn | **类型:** 学习
**Language:**Python**语言:**Python
**Prerequisites:** Phase 3 (Deep Learning Core), Phase 5 · 09 (Sequence-to-Sequence), Phase 5 · 10 (Attention Mechanism) | **前置知识:** 阶段 3（深度学习基础），阶段 5 · 09（序列到序列），阶段 5 · 10（注意力机制）
**Time:** ~45 minutes | **时间:** ~45 分钟

## Mục tiêu học tập

- Hiểu được ba điểm yếu gây tử vong của mạng thần kinh tái phát (RNN)
  Nghĩ được 3 điểm yếu của mạng lưới thần kinh
- Giải thích tại sao độ sâu hàng loạt, chứ không phải số lượng hoạt động, xác định thời gian đào tạo GPU
  解释 tại sao chuỗi đi sâu hơn là số hoạt động) quyết định thời gian đào tạo của GPU
- So sánh RNN vs Transformer phức tạp trên các nhiệm vụ mô hình hóa chuỗi
  So sánh RNN với Transformer trong trình tự xây dựng nhiệm vụ phức tạp
- Xác định các kịch bản mà RNN hoặc mô hình không gian nhà nước vẫn có thể được ưu tiên
  识别 RNN hoặc trạng thái mô hình không gian vẫn còn tốt hơn
- Nhận ra sự chuyển hướng thiên vị inductive từ địa phương sang sự chú ý toàn cầu
  认识从局部性到全局注意力归纳偏好转移

## Vấn đề  vấn đề giới thiệu

Trước năm 2017, mọi mô hình trình tự hiện đại trên hành tinh  ngôn ngữ, dịch, ngôn ngữ  là một mạng lưới thần kinh tái phát. LSTM và GRU đã giành được các tiêu chuẩn dịch thuật tương đương với ImageNet trong nửa thập kỷ.

> Trước năm 2017, mỗi mô hình chuỗi tiên tiến nhất trên toàn cầu 语言,翻译,语音 đều là mạng thần kinh vòng lặp. LSM và GRU được gọi là 5 năm qua trên các bài kiểm tra dịch cơ sở trình độ của ImageNet.

Họ có ba điểm yếu chết người. tính toán theo trình tự có nghĩa là bạn không thể song song dọc theo trục thời gian: token`t+1`cần trạng thái ẩn từ token `t`Một chuỗi 1.024 token có nghĩa là 1.024 bước liên tục trên GPU có thể thực hiện 1.000.000 hoạt động điểm nổi mỗi chu kỳ. Thời gian đào tạo tường-thành tròn theo chiều dài chuỗi trên phần cứng được thiết kế cho sự song song.

> Chúng có ba điểm yếu gây chết người.`t+1`需要来自代币 `t`Trong một chuỗi 1,024 token, GPU có thể thực hiện 1,000,000 lần hoạt động trên các điểm trên mỗi chu kỳ sẽ chạy 1,024 bước liên tục.

> **【中文解读】**Điểm yếu thứ nhất: chuỗi tính toán. RNN phải xử lý từng token theo thứ tự, hoàn toàn không thể sử dụng khả năng tính toán đồng tuyến của GPU.

Các gradient biến mất có nghĩa là thông tin 50 token trở lại đã bị nén thông qua 50 không tuyến tính. Các đơn vị lặp lại được gài (LSTM, GRU) làm mềm sự đập vỡ nhưng không bao giờ loại bỏ nó.

> 梯度消失 nghĩa là 50 token  trước đây thông tin đã bị 50 thay đổi không tuyến tính nén hầu hết. 门控循环单元 (LSTM、GRU) đã giảm áp lực này nhưng chưa bao giờ loại bỏ nó. 长程依赖 "Tôi đã đọc trong chuyến bay đến Kyoto vào mùa hè năm ngoái là......" thường thất bại──

> **【中文解读】**Điểm yếu thứ hai là: độ biến mất. Sau 50 tầng thay đổi không dây, thông tin ở xa gần như hoàn toàn bị mất.

Các trạng thái ẩn chiều rộng cố định có nghĩa là bộ mã hóa đã ép toàn bộ chuỗi nguồn thành một vector trước khi bộ mã hóa thấy bất cứ điều gì. Không quan trọng liệu nguồn là 5 token hay 500; nút thắt chai là hình dạng tương tự.

> Tình trạng ẩn của độ rộng cố định có nghĩa là trước khi bộ lập trình nhìn thấy bất kỳ nội dung nào của máy giải mã, sẽ nén toàn bộ chuỗi nguồn thành một khối lượng.

> **【中文解读】**Điểm yếu thứ ba: khối lượng cố định của bộ máy lập trình phải thu nhỏ toàn bộ chuỗi nguồn thành một khối lượng dài cố định.

Bài báo năm 2017 "Trông tâm là tất cả những gì bạn cần" đề xuất một điều cực đoan: bỏ lại sự tái phát hoàn toàn. Hãy để mỗi vị trí chăm sóc mọi vị trí khác song song. Tập trong một số nhân tử lớn thay vì 1.024 thứ tự.

> Bài luận năm 2017 "Trông tâm là tất cả những gì bạn cần" đề xuất một chương trình kích thích: hoàn toàn từ bỏ vòng lặp.

Kết quả thống trị mọi phương thức vào năm 2026. Ngôn ngữ (GPT-5, Claude 4, Llama 4), thị giác (ViT, DINOv2, SAM 3), âm thanh (Whisper), sinh học (AlphaFold 3), robot (RT-2).

> Đến năm 2026, kết quả của nó đã chủ đạo mọi mô hình.

## Khái niệm cốt lõi

![RNN sequential compute vs Transformer parallel attention](../assets/rnn-vs-transformer.svg)

**Recurrence as a bottleneck.**Một RNN tính toán `h_t = f(h_{t-1}, x_t)`Mỗi bước phụ thuộc vào bước trước.`h_5`trước đây`h_4`Trên các GPU hiện đại với hơn 10.000 lõi song song, điều này lãng phí 99% silicon trên một chuỗi dài.

> **循环即瓶颈。**RNN 计算`h_t = f(h_{t-1}, x_t)`Mỗi bước đều phụ thuộc vào bước trước.`h_4`之前计算 `h_5`❖ Với hơn 10.000 GPU hiện đại và có lõi, nó đã lãng phí 99% năng lượng chip trong chuỗi dài.

> **【中文解读】**Chuyện này là bản chất của khối lượng: mỗi bước tính toán thời gian đều phụ thuộc vào kết quả của bước trước. GPU giỏi trong việc thực hiện hàng ngàn hành trình cùng hành trình, trong khi các chuỗi RNN phụ thuộc vào nó để chỉ sử dụng một phần nhỏ của GPU.

**Attention as a broadcast.**- Lưu ý về sự chú ý của chính mình`output_i = sum_j(a_ij * v_j)`cho mỗi cặp `(i, j)`cả nxn sự chú ý của các bộ viền chứa trong một loạt các matmul. không bước phụ thuộc vào một bước khác. GPUs thích nó.

> **注意力即广播。**tự chú ý đồng thời cho mỗi đối tác`(i, j)`计算 `output_i = sum_j(a_ij * v_j)`◊ toàn bộ N×N cúi lực tập hợp được lấp đầy trong một khối lượng tập hợp tập hợp.

**The speedup is not a constant.**Đó là sự khác biệt giữa `O(N)`độ sâu hàng loạt và`O(1)`Trong thực tế, các bộ biến chuyển tập luyện nhanh hơn 510x mỗi thời đại trên phần cứng phù hợp ở N=512, và khoảng cách mở rộng theo chiều dài chuỗi cho đến khi bạn chạm vào `O(N²)`tường bộ nhớ của sự chú ý (mà Flash Attention sau đó sửa chữa  xem Bài học 12).

> **加速不是常数。**Nó là `O(N)`串行深度与 `O(1)`Trong thực tế, trên các bộ máy phù hợp N=512 时,Transformer mỗi thời đại tốc độ đào tạo nhanh 5-10 lần, và khoảng cách tăng lên theo chiều dài của chuỗi, cho đến khi bạn gặp phải sự chú ý.`O(N²)`内存墙(Flash Attention 后来修复了它见第 12 课)

**What transformers cost.**Tăng cường bộ nhớ chú ý như `O(N²)`Đối với bối cảnh 2K, tốt. Đối với bối cảnh 128K, bạn cần cửa sổ trượt, ngoại phân RoPE, flash chú ý, hoặc biến thể chú ý tuyến tính.`O(N)`trong cả thời gian và trí nhớ; những người biến đổi đổi thời gian với trí nhớ và sau đó giành lại thời gian thông qua sự song song.

> **Transformer 的代价。**注意力内存按 `O(N²)`增长── đối với 2K 上下文, không có vấn đề── đối với 128K 上下文, bạn cần phải xoay cửa sổ、RoPE 外推、Flash Attention 分块计算或线性注意力变化──循环在时间和内存都是`O(N)`Transformer dùng trong bộ nhớ để thay đổi thời gian, rồi qua đường đi để giành lại thời gian.

**The inductive bias shift.**RNN giả định địa phương và tính gần đây. Các biến thể không giả định gì  mỗi cặp là ứng cử viên để chú ý. Đó là lý do tại sao các biến thể cần nhiều dữ liệu hơn để đào tạo tốt nhưng mở rộng hơn khi họ có nó. Chinchilla (2022) đã chính thức hóa điều này: nếu có đủ token, một biến thể luôn đánh bại một RNN với số lượng tham số bằng nhau.

> **归纳偏好的转变。**RNN giả định về địa phương và gần gũi. Transformer không làm bất kỳ giả định nào. Mỗi cặp đều là ứng cử viên để tập trung. Đó là lý do tại sao Transformer cần nhiều dữ liệu hơn để tập luyện tốt, nhưng một khi có đủ dữ liệu thì có thể mở rộng hơn. Chinchilla: 2022 đã hình thành điều này: cho đủ token, Transformer luôn đánh bại RNN với số lượng các tham số tương tự.

> **【中文解读】**Ưu điểm chuyển đổi của chuyển đổi là quan trọng trong thành công của Transformer. RNN 隐式假设" gần đó của token là quan trọng hơn", trong khi Transformer không làm bất kỳ giả định nào  giữa hai vị trí nào có thể được xây dựng liên kết trực tiếp.

> **【拓展：Chinchilla 缩放定律】**Bài luận của DeepMind Chinchilla 文章(2022) chứng minh, tỷ lệ tăng trưởng của các mô hình và số lượng dữ liệu đào tạo tương tự. Điều này giải thích tại sao các mô hình Llama 、 GPT-4 và các mô hình khác cần dữ liệu đào tạo hàng triệu tỷ cấp mã thông báo  yếu về sự thích hợp cần rất nhiều dữ liệu để "bồi thường" ‖

## Hãy xây dựng nó.
```figure
rnn-vs-parallel
```

## Hãy xây dựng nó

Không có mạng thần kinh ở đây  chúng tôi mô phỏng nút thắt chai lõi theo số để bạn cảm thấy khoảng trống trên máy tính xách tay của bạn.

> Không có mạng thần kinh nào, chúng tôi dùng các giá trị số để mô phỏng các khối lượng, để bạn cảm nhận sự khác biệt trên máy tính xách tay.

> **【中文解读】**Phần này sử dụng mô hình số nguyên để bạn cảm nhận được sự khác biệt hiệu suất của chuỗi so với chuỗi. Điều quan trọng là độ sâu của chuỗi liên kết dựa vào độ sâu của chuỗi là N, trong khi độ sâu của chuỗi liên kết chỉ là O(1) hoặc O(log N) ⋅. Đây là nguyên nhân cơ bản của Transformer so với RNN ⋅.

### Bước 1: đo độ sâu hàng loạt.

Nhìn xem`code/main.py`Chúng ta xây dựng hai hàm. Một mã hóa một chuỗi như một chuỗi các sự gia tăng (serial, như một RNN). Một mã hóa nó như một giảm song song (broadcast, như sự chú ý).

> 参见 `code/main.py`△ Chúng ta xây dựng hai hàm. Một sẽ được mã hóa để thêm chuỗi.

```python
def rnn_style(xs):
    h = 0.0
    for x in xs:
        h = 0.9 * h + x   # can't parallelize: h depends on previous h
    return h

def attention_style(xs):
    return sum(xs) / len(xs)  # every x is independent
```

Chúng ta có thời gian cả hai trên chuỗi lên đến 100.000 yếu tố. phiên bản RNN là O(N) và một ống dẫn CPU duy nhất. Ngay cả trong Python tinh khiết, sự giảm kiểu chú ý vượt qua nó ở độ dài ≥ 1.000 vì Python `sum()`được thực hiện bằng C và lặp lại mà không có chi phí thông dịch viên trên mỗi bước.

> Chúng tôi có thể tính toán các chuỗi dài đến 100.000 yếu tố. RNN phiên bản là một CPU đơn của O(N) 流水线. Ngay cả trong Python hoàn toàn, tập trung theo kiểu tập trung trong độ dài ≥ 1.000 时也能胜出, vì Python `sum()`là sử dụng C 实现, 代时没有解释器的逐步开销.

### Bước 2: Đếm các hoạt động lý thuyết .

Cả hai thuật toán đều thêm N. Sự khác biệt là * độ sâu phụ thuộc *: bao nhiêu hoạt động phải xảy ra theo trình tự trước khi tiếp theo có thể bắt đầu. RNN độ sâu = N. Độ sâu chú ý = log(N) với một giảm cây, hoặc 1 với một quét song song. Độ sâu, không phải số op, quyết định thời gian GPU.

> 两种算法都做N 次加法。区别在*依赖深度*: 在下一个操作开始之前,必须顺序执行多少操作。RNN深度 = N。注意力深度 = 用树形归约时为 log(N),用并行扫描时为 1。决定 GPU 时间是深度,而不是操作数。

### Bước 3: Scaling Empirical on Long Sequences 步骤 3: thực tế trên long sequence mở rộng

Chúng tôi in một bảng thời gian làm cho khoảng cách O(N) hiển thị. Trên máy tính xách tay Mac 2026, các chuỗi dưới 1.000 yếu tố quá nhanh để đo. Các chuỗi 100.000 cho thấy quét tuyến tính sạch. Đánh giá đó đến một biến đổi 16,384 token với tương đương LSTM 12 lớp và bạn thấy tại sao tập tường đồng hồ là một chất chặn trong năm 2016.

> Chúng tôi đã in một张使 O(N) khoảng cách có thể nhìn thấy lịch trình. Trong sổ tay Mac năm 2026, chuỗi ít hơn 1.000 yếu tố quá nhanh và không thể đo lường. 100.000 yếu tố của chuỗi cho thấy một quét tuyến tính rõ ràng.

## Hãy sử dụng nó để thực hiện

Khi nào để chọn một RNN vào năm 2026:

> 2026 年何时仍应选择 RNN:

> **【中文解读】**Trong khi Transformer trong hầu hết các trường hợp chiến thắng, nhưng并非万能――流式推理((每次只处理一个代币) 、超长序列(>1M代币) 和边缘设备场景下,RNN或状态空间模型(如Mamba) vẫn có ưu điểm.

> **【拓展：Mamba 与状态空间模型】**Mamba(2023) thông qua cơ chế quét chọn lọc đã thực hiện O(N)  phức tạp của chuỗi xây dựng, đồng thời hỗ trợ cùng hành trình đào tạo. Nó bản chất là một RNN được phân tích, nhưng trong hiệu quả đào tạo gần với Transformer. Trong các nhiệm vụ tạo mã, hiểu văn bản dài, cấu trúc Mamba + Transformer đã trở thành một hướng khám phá quan trọng của phòng thí nghiệm phía trước.

| Situation | Pick / 场景 | 选择 |
|-----------|-------------|------|
| Streaming inference, one token at a time, constant memory | RNN or state-space model (Mamba, RWKV) |
| Very long sequences (>1M tokens) where attention memory explodes | Linear attention, Mamba 2, Hyena |
| Edge device with no matmul accelerator | Depthwise-separable RNN still wins on FLOPs/watt |
| Anything else (training, batched inference, context up to 128K) | Transformer |

Các mô hình không gian nhà nước (SSM) như Mamba về cơ bản là RNN với các tham số cấu trúc cho họ tốt nhất của cả hai: `O(N)`Tự do học tập của các nhà khoa học đã được thực hiện trong các năm nay, và các nhà khoa học đã được nghiên cứu về các phương pháp học học.

> 状态空间模型 (SSM) như Mamba 本质上是具有结构化参数化的 RNN,兼具两者的优势:`O(N)`扫描内存, thông qua chọn lọc扫描实现并行训练――它们恢复了变体90%质量,同时具有更好的长上下文扩展性――2026年大多数前沿实验室训练混合SSM+Transformer 模型(如Jamba、Samba) 循环没有灭亡,它是一个组件――

## Chuyển nó đi.

Nhìn xem`outputs/skill-architecture-picker.md`. Kỹ năng chọn một kiến trúc cho một vấn đề chuỗi mới do độ dài, thông suất và hạn chế ngân sách đào tạo.

> 参见 `outputs/skill-architecture-picker.md` Kỹ năng này cho các vấn đề về chuỗi mới lựa chọn cấu trúc, cho phép định lượng, dung lượng và ngân sách đào tạo.

> **【拓展：架构选择决策树】**Trong công trình thực tế, lựa chọn cấu trúc cần phải xem xét nhiều chiều: chuỗi dài, trì hoãn yêu cầu, ngân sách lưu trữ, đào tạo dữ liệu, triển khai phần cứng. Đối với hầu hết các nhiệm vụ NLP, Decoder-only Transformer là lựa chọn mặc định. Đối với chuỗi quá dài, xem xét Mamba hoặc cấu trúc hỗn hợp; đối với biên giới triển khai, RNN/SSM có thể phù hợp hơn.

## Tập luyện bài tập

1. **Easy / 简单。**Nhận đi`rnn_style`từ `code/main.py`và thay thế trạng thái ẩn scalar bằng một chiều dài-64 vector của trạng thái ẩn.
   取 `code/main.py`Trung `rnn_style`, sẽ thay thế kích thước ẩn trạng thái với chiều dài 64 của ẩn trạng thái向量―― tái đo―― liên tục phát hành với ẩn trạng thái chiều kích tăng lên bao nhiêu?

2. **Medium / 中等。**Thực hiện một tổng tiền tố song song (Hillis-Steele scan) trong Python tinh khiết. Kiểm tra nó tạo ra cùng một đầu ra số như một quét hàng loạt trên chiều dài 1024.
   Sử dụng Python 实现并行前和(Hillis-Steele 扫描) 验证它在长度 1024 上产生与串行扫描相同的数值输出──计算深度──

3. **Hard / 困难。**Đưa giảm kiểu chú ý vào PyTorch trên GPU. Thời gian cả hai khi bạn lau dọc chuỗi từ 64 đến 65.536.
   Phân tích tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập trung tập

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say / 术语 | 人们怎么说 | What it actually means / 实际含义 |
|------|----------------------|-----------|----------------------------------|
| Recurrence | "RNNs are sequential" | 循环 (Recurrence) | Computation where step `t` depends on step `t-1`, forcing serial execution along the time axis. 步骤 `t` 依赖于步骤 `t-1` 的计算，强制沿时间轴串行执行。 |
| Serial depth | "How deep the graph is" | 串行深度 (Serial depth) | Longest chain of dependent ops; bounds wall-clock even on infinite hardware. 依赖操作的最长链；即使在无限硬件上也限制了时间开销。 |
| Attention | "Let tokens look at each other" | 注意力 (Attention) | Weighted sum `sum_j a_ij v_j` where `a_ij` comes from a similarity score between positions i and j. 加权求和 `sum_j a_ij v_j`，其中 `a_ij` 来自位置 i 和 j 之间的相似度得分。 |
| Context window | "How much the model sees" | 上下文窗口 (Context window) | Number of positions an attention layer can take as input; quadratic memory cost scales here. 注意力层可作为输入的位置数；二次内存开销在这里缩放。 |
| Inductive bias | "Assumptions baked into the architecture" | 归纳偏好 (Inductive bias) | Prior about what the data looks like; CNNs assume translation invariance, RNNs assume recency. 关于数据外观的先验；CNN 假设平移不变性，RNN 假设邻近性。 |
| State-space model | "RNN with algebra behind it" | 状态空间模型 (State-space model) | Recurrence parameterized for parallel training via structured state-space matrices. 通过结构化状态空间矩阵参数化以实现并行训练的循环。 |
| Quadratic bottleneck | "Why context costs so much" | 二次瓶颈 (Quadratic bottleneck) | Attention memory = `O(N²)` in sequence length; Flash Attention hides the constants, not the scaling. 注意力内存 = 序列长度的 `O(N²)`；Flash Attention 隐藏了常数，而非缩放。 |

## Xem thêm 延伸阅读

- [Vaswani et al. (2017). Attention Is All You Need](https://arxiv.org/abs/1706.03762) bài báo đã giết chết sự tái phát trong NLP chính thống.
  Vaswani 等人(2017)  终结了主流NLP 中循环的论文──

- [Bahdanau, Cho, Bengio (2014). Neural MT by Jointly Learning to Align and Translate](https://arxiv.org/abs/1409.0473) nơi sự chú ý được sinh ra, được gắn vào một RNN.
  Bahdanau, Cho, Bengio(2014)  注意力诞生的地方,附加在RNN 上。

- [Hochreiter, Schmidhuber (1997). Long Short-Term Memory](https://www.bioinf.jku.at/publications/older/2604.pdf) giấy LSTM gốc, để ghi lại.
  Hochreiter, Schmidhuber(1997)  原始 LSTM 论文,留作记录。

- [Gu, Dao (2023). Mamba: Linear-Time Sequence Modeling with Selective State Spaces](https://arxiv.org/abs/2312.00752) câu trả lời tái phát hiện đại cho các bộ biến đổi.
  Gu, Dao(2023)  Chuyển đổi mô hình hiện đại của Transformer

> **【拓展："Attention Is All You Need" 的历史影响】**Các bài viết của Vaswani 等人 năm 2017 không chỉ giải quyết vấn đề đồng hành hóa của RNN, còn dẫn đến một cuộc cách mạng范式── từ BERT(2018) đến GPT-4(2023), từ ViT(2020) đến AlphaFold 2(2021), Tranhistor 架构 đã trở thành một mô-đun cơ bản của AI hiện đại── nó chứng minh "những ưu tiên về tính năng + dữ liệu lớn + tính toán" có thể vượt qua các cấu trúc cụ thể trong lĩnh vực thiết kế.
