# Pre-Training một Mini GPT (124M Parameters) 预训迷你 GPT(1.24 tỷ参数)

> GPT-2 Small có 124 triệu tham số. đó là 12 lớp biến đổi, 12 đầu chú ý, và 768 chiều nhúng. bạn có thể đào tạo nó từ đầu trên một GPU trong vài giờ. hầu hết mọi người không làm điều này. họ sử dụng các điểm kiểm tra được đào tạo trước. nhưng nếu bạn không đào tạo một cái đó, bạn không thực sự hiểu những gì đang xảy ra bên trong mô hình bạn đang xây dựng sản phẩm trên.

> **【中文解读】**GPT-2 Small có 1.24 tỷ tham số: 12 tầng Transformer  12 个注意力头 768 维嵌入── đơn GPU 几小时即可从头训――理解预训是理解大模型的第一步──

> **【拓展：大模型三阶段】**Đại mô hình đào tạo三阶段:(1) 预训练(海量无标注数据,学习语言表示)→ (2) SFT(指令微调,学会跟随指令)→ (3) RLHF/DPO(对齐人类偏好)。本课是第一阶段,GPT-2 是所有GPT 系列的原型──

>  **【前置】**学本节前请先掌握:(1) Bước 10·01-03(分词器、数据管线) 理解代币 ID 序列如何输入模型;(2) Transformer 架构(Bước 05) 自注意、LayerNorm、FFN;(3) numpy 矩阵运算、反向传播手算(Bước 03 微积分与链式法则);(4) 交叉损失函数的梯度推导――本课**用 numpy 实现**, không còn phụ thuộc vào PyTorch Autograd, để có thể tự viết `backward()`

**Type:** Build
**Languages:** Python (with numpy)
**Prerequisites:** Phase 10, Lessons 01-03 (Tokenizers, Building a Tokenizer, Data Pipelines)
**Time:** ~120 minutes

## Mục tiêu học tập

- Thực hiện kiến trúc GPT-2 đầy đủ (124M tham số) từ đầu: nhúng token, nhúng vị trí, khối biến thể và đầu mô hình ngôn ngữ
  Từ zero thực hiện hoàn chỉnh GPT-2 架构(124M 参数):token 嵌入、位置嵌入、Transformer 块和语言模型头
- Trình luyện mô hình GPT trên một cơ thể văn bản bằng cách sử dụng dự đoán token tiếp theo với mất entropy chéo
  Sử dụng biểu tượng 预测和交叉损失在文本语料上训练 GPT 模型
- Thực hiện việc tạo văn bản tự rút bằng cách lấy mẫu nhiệt độ và lọc top-k/top-p
  实现带温度采样和 top-k/top-p 过的自归文本生成
- Theo dõi đường cong mất tập luyện và xác nhận rằng mô hình học các mô hình ngôn ngữ nhất quán
  监控训练损曲线,验证模型学到了连贯的语言模式

> **【中文解读】**Bài học này sử dụng numpy tinh khiết từ zero thực hiện GPT-2 Small(124M 参数)  Bạn sẽ thấy 1.24 tỷ tham số làm thế nào thông qua vòng tập luyện chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển tiếp chuyển chuyển tiếp chuyển tiếp chuyển tiếp chuyển chuyển tiếp chuyển tiếp chuyển tiếp chuyển chuyển chuyển tiếp chuyển tiếp chuyển chuyển chuyển tiếp chuyển tiếp chuyển chuyển chuyển chuyển tiếp chuyển tiếp chuyển chuyển chuyển chuyển tiếp chuyển tiếp chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển chuyển

## Vấn đề  vấn đề giới thiệu

Bạn biết biến đổi là gì, bạn đã đọc sơ đồ, bạn có thể đọc "trông trọng là tất cả những gì bạn cần" và vẽ các hộp có nhãn "Trong trọng tâm đa đầu" trên bảng màu.

> Bạn biết cái gì là biến đổi. Bạn đã xem biểu đồ. Bạn có thể ghi nhớ "trọng tâm là tất cả những gì bạn cần" và vẽ trên bảng màu trắng một hộp có nhãn "Trong tâm trí đa đầu".

Không có nghĩa là bạn hiểu được những gì xảy ra khi mô hình tạo ra văn bản.

> Tất cả điều này không có nghĩa là bạn hiểu được những gì đã xảy ra khi mô hình tạo văn bản.

Có 124,438,272 tham số trong GPT-2 Small (với cân nặng). Mỗi một trong số chúng được thiết lập bằng cách chạy một vòng tròn đào tạo: vượt qua phía trước, mất tính toán, vượt qua trở lại, nâng cấp trọng lượng. 12 khối biến đổi. 12 đầu chú ý mỗi khu. Một không gian nhúng 768 chiều. Một từ vựng của 50,257 token. Mỗi khi mô hình tạo ra một token, tất cả 124 triệu tham số tham gia vào một chuỗi nhân số tử liệu đơn lẻ lấy một chuỗi ID token và tạo ra phân phối xác suất trên token tiếp theo.

> GPT-2 Small có 124,438,272 个参数 (含权重共享) ⋅ mỗi参数 đều thông qua vòng tròn tập luyện: trước hướng传播、计算损失、反向传播、更新权重── 12 khối Transformer, mỗi khối 12 个注意力头,768 维嵌入空间,50,257 词表── mỗi lần tạo token, tất cả 1.24 tỷ参数链 tham gia một条矩阵乘法, sẽ chuyển đổi token ID 序列 thành các token tiếp theo 概率分布率──

Nếu bạn chưa bao giờ tự xây dựng nó, bạn đang làm việc với một hộp đen. Bạn có thể sử dụng API. Bạn có thể điều chỉnh. Nhưng khi một cái gì đó sai lầm - khi mô hình ảo giác, khi nó lặp lại, khi nó từ chối làm theo hướng dẫn - bạn không có mô hình tâm lý về * tại sao*.

> Nếu bạn chưa từng tự xây dựng mô hình này, bạn đang sử dụng một hộp đen. Bạn có thể điều chỉnh API, có thể điều chỉnh nhỏ. Nhưng khi mô hình có cảm giác lặp lại hoặc từ chối tuân theo chỉ dẫn, bạn không biết tại sao.

Bài học này xây dựng GPT-2 Small từ đầu. Không phải trong PyTorch. Trong numpy. Mỗi nhân tử liệu là hiển thị. Mỗi gradient được tính toán bằng mã của bạn. Bạn sẽ thấy chính xác 124 triệu số âm mưu để dự đoán từ tiếp theo.

> 本课从零构建 GPT-2 Small──不用 PyTorch──用 numpy──每矩阵乘法都可见──每梯度都由你的代码计算──你将看到1.24亿个数字如何协作预测 下一个词──

> 本课从零构建 GPT-2 Small──不用 PyTorch──用 numpy──每矩阵乘法都可见──每梯度都由你的代码计算──你将看到1.24亿个数字如何协作预测 下一个词──

## Khái niệm cốt lõi

### Kiến trúc GPT

Dưới đây là biểu đồ tính toán đầy đủ từ ID token đến xác suất token tiếp theo:

> Dưới đây là biểu đồ tính toán đầy đủ từ ID token đến xác suất token  kế tiếp:

1. Các thẻ nhận dạng nhập. hình dạng: (batch_size, seq_len).
2. Đơn hiệu nhúng tìm kiếm. Mỗi ID bản đồ đến một vector 768 chiều. hình dạng: (batch_size, seq_len, 768).
3. Định vị tìm kiếm. Mỗi vị trí (0, 1, 2, ...) được lập ra với một vector 768 chiều.
4. Thêm token + position embeddings.
5. Đi qua 12 khối biến đổi.
6. Tăng bình thường hóa lớp cuối cùng.
7. Định dạng: (batch_size, seq_len, vocab_size).
8. Softmax để có được xác suất.

Đó là toàn bộ mô hình, không có biến động, không có tái phát, chỉ có nhúng, chú ý, mạng feedforward và các quy tắc lớp xếp chồng lên 12 lần.

> Đó là toàn bộ mô hình. Không có vòng lặp. Chỉ có sự nhúng vào.

>  **【类比】**GPT 像一台"流水线打字机":纸带送进代币 ID → 印章 1(代币嵌入)盖出 768 维向量 → 印章 2( vị trí嵌入) 叠加位置 → 12 道工人(Transformer block) từng tầng sửa đổi 量 → 末端喷墨头(LM head) trên 50257 个候选词喷概率分布 → 选择最高概率的词输出 → 把新词同时再送回纸带开头,循环──一切秘藏在那12 道工人怎么修改"量而自注意就是工人只用眼睛的看序列里其他代币能力──

```mermaid
graph TD
    A["Token IDs\n(batch, seq_len)"] --> B["Token Embeddings\n(batch, seq_len, 768)"]
    A --> C["Position Embeddings\n(batch, seq_len, 768)"]
    B --> D["Add"]
    C --> D
    D --> E["Transformer Block 1"]
    E --> F["Transformer Block 2"]
    F --> G["..."]
    G --> H["Transformer Block 12"]
    H --> I["Layer Norm"]
    I --> J["Linear Head\n(768 -> 50257)"]
    J --> K["Softmax\nNext-token probabilities"]

    style A fill:#1a1a2e,stroke:#e94560,color:#fff
    style B fill:#1a1a2e,stroke:#0f3460,color:#fff
    style C fill:#1a1a2e,stroke:#0f3460,color:#fff
    style D fill:#1a1a2e,stroke:#16213e,color:#fff
    style E fill:#1a1a2e,stroke:#e94560,color:#fff
    style F fill:#1a1a2e,stroke:#e94560,color:#fff
    style H fill:#1a1a2e,stroke:#e94560,color:#fff
    style I fill:#1a1a2e,stroke:#16213e,color:#fff
    style J fill:#1a1a2e,stroke:#0f3460,color:#fff
    style K fill:#1a1a2e,stroke:#51cf66,color:#fff
```

### Phép biến đổi

Mỗi trong 12 khối theo cùng một mô hình. Kiến trúc trước chuẩn (GPT-2 sử dụng chuẩn trước, không phải chuẩn sau như biến đổi ban đầu):

> Mỗi trong 12 khối theo cùng một mô hình.

1. LayerNorm
2. Sự chú ý nhiều người
3. Kết nối còn lại (tăng đầu vào trở lại)
4. LayerNorm
5. Mạng lưới chuyển tiếp (MLP)
6. Kết nối còn lại (tăng đầu vào trở lại)

Các kết nối dư thừa là rất quan trọng. Nếu không có chúng, gradient biến mất khi chúng đạt đến khối 1 trong quá trình lan rộng ngược. Với chúng, gradient có thể chảy trực tiếp từ lỗ đến bất kỳ lớp nào thông qua con đường "lút".

> Còn lại là quan trọng. Không có chúng, thang độ di truyền ngược chiều đến 1 khối sẽ biến mất. Nếu có chúng, thang độ có thể đi qua đường " nhảy " trực tiếp từ mất mát chảy đến bất kỳ tầng nào.

> **【中文解读】**GPT 架构的核心是变压器 解码器块的堆积──每个块包含:LayerNorm → 多头自注意力 →残差连接 → LayerNorm → 前网络(MLP)→残差连接──GPT-2 使用预规(先归化再注意力),而不是原始变压器的后规──残差连接是关键没有它,梯度在12层反向传播后会消失,无法训练深层网络──

> **【拓展：GPT 系列的架构演进】**GPT-2 Small(124M,12 层 768 维)→ GPT-2 Medium(355M,24 层 1024 维)→ GPT-2 Large(774M,36 层 1280 维)→ GPT-2 XL(1.5B,48 层 1600 维)→ GPT-3(175B,96 层 12288 维)。 cấu trúc cơ bản giống nhau, chỉ là các tầng và chiều kích liên tục mở rộng。

### Lưu ý: Cơ chế cốt lõi

Sự chú ý tự nhiên cho phép mỗi token nhìn vào mỗi token trước đó và quyết định bao nhiêu để tham gia cho mỗi token.

> Từ chú ý để mỗi token  nhìn thấy mỗi token trước,并 quyết định cho mỗi token 给予多少关注;;:

Đối với mỗi vị trí token, tính toán ba vector từ đầu vào:
- **Query (Q)**"Tôi đang tìm gì?"
  Trung ngữ翻译:**查询（Q）**"Em đang tìm gì?"
- **Key (K)**"Tôi có gì trong đó?"
  Trung ngữ翻译:**键（K）**"Em có chứa gì?"
- **Value (V)**"Tôi mang thông tin gì?"
  Trung ngữ翻译:**值（V）**"Tôi mang theo thông tin gì?"

```
Q = input @ W_q    (768 -> 768)
K = input @ W_k    (768 -> 768)
V = input @ W_v    (768 -> 768)

attention_scores = Q @ K^T / sqrt(d_k)
attention_scores = mask(attention_scores)   # causal mask: -inf for future positions
attention_weights = softmax(attention_scores)
output = attention_weights @ V
```

Mặt nạ nguyên nhân là điều làm cho GPT tự rút lui. Vị trí 5 có thể tham gia vào các vị trí 0-5 nhưng không phải 6, 7, 8, v.v. Điều này ngăn chặn mô hình "bảo quy" bằng cách nhìn vào các token trong tương lai trong quá trình đào tạo.

> 因果掩码使 GPT trở thành mô hình tự quay lại. vị trí 5 có thể chú ý đến vị trí 0-5 nhưng không thể chú ý đến 6、7、8 và như vậy. Điều này ngăn chặn mô hình trong quá trình tập luyện qua các biểu tượng tương lai để "lâm kỉnh".

**Multi-head attention**chia không gian 768 chiều thành 12 đầu có mỗi chiều 64 chiều. Mỗi đầu học một mô hình chú ý khác nhau. Một đầu có thể theo dõi các mối quan hệ tổng hợp (thỏa thuận đối tượng-ngôn ngữ). Một đầu khác có thể theo dõi sự tương đồng ngữ học (ngôn ngữ). Một đầu khác có thể theo dõi sự gần gũi vị trí (ngôn ngữ gần gũi).

> **多头注意力**Để phân chia 768 维空间 thành 12 维的头── mỗi đầu học một kiểu chú ý khác nhau── một đầu có thể theo dõi 句法关系(主谓一致)── một đầu có thể theo dõi 语义相似性(同义词)── một đầu có thể theo dõi vị trí gần gũi (相邻词)── tất cả 12 đầu được kết hợp và đưa vào 768 维──

```mermaid
graph LR
    subgraph MultiHead["Multi-Head Attention (12 heads)"]
        direction TB
        I["Input (768)"] --> S1["Split into 12 heads"]
        S1 --> H1["Head 1\n(64 dims)"]
        S1 --> H2["Head 2\n(64 dims)"]
        S1 --> H3["..."]
        S1 --> H12["Head 12\n(64 dims)"]
        H1 --> C["Concat (768)"]
        H2 --> C
        H3 --> C
        H12 --> C
        C --> O["Output Projection\n(768 -> 768)"]
    end

    subgraph SingleHead["Each Head Computes"]
        direction TB
        Q["Q = X @ W_q"] --> A["scores = Q @ K^T / 8"]
        K["K = X @ W_k"] --> A
        A --> M["Apply causal mask"]
        M --> SM["Softmax"]
        SM --> MUL["weights @ V"]
        V["V = X @ W_v"] --> MUL
    end

    style I fill:#1a1a2e,stroke:#e94560,color:#fff
    style O fill:#1a1a2e,stroke:#e94560,color:#fff
    style Q fill:#1a1a2e,stroke:#0f3460,color:#fff
    style K fill:#1a1a2e,stroke:#0f3460,color:#fff
    style V fill:#1a1a2e,stroke:#0f3460,color:#fff
```

Việc chia bằng sqrt(d_k) -- sqrt(64) = 8 -- là quy mô. Nếu không có nó, các sản phẩm chấm lớn hơn cho các vector chiều cao, đẩy softmax vào các vùng mà gradient gần như không. Đây là một trong những hiểu biết chính trong bài viết ban đầu "Trông tâm là tất cả bạn cần".

> Ngoài ra, mảng d_k_sqrt_64) = 8 là thu nhỏ hơn. Không có nó, điểm积 ở độ cao sẽ trở nên rất lớn, sẽ đẩy độ mềm vào độ gần như không.

### KV Cache: Tại sao việc suy luận nhanh chóng

Trong quá trình đào tạo, bạn xử lý toàn bộ chuỗi một lần. Trong quá trình suy luận, bạn tạo ra một token một lúc. Không có tối ưu hóa, tạo token N đòi hỏi phải tính lại sự chú ý cho tất cả các token trước đó N-1. đó là O(N^2) cho mỗi token được tạo ra, hoặc tổng cộng O(N^3) cho một chuỗi dài N.

> 训练时,你一次处理整个序列──推理时,你个别生成代币──没有优化的话,生成代币 N 需要为所有N-1 个前代币重新计算注意力──这是每个生成代币的O(N^2),或长度N 的序列总共O(N^3)。

KV Cache sẽ giải quyết chuyện này. Sau khi tính toán K và V cho mỗi token, lưu trữ chúng. Khi tạo token N + 1, bạn chỉ cần tính toán Q cho token mới và tìm kiếm K và V được lưu trữ từ tất cả token trước đó. Điều này làm giảm chi phí mỗi token từ O(N) đến O(1) cho tính toán K và V. Việc tính toán điểm chú ý vẫn là O(N) bởi vì bạn chăm sóc tất cả các vị trí trước đó, nhưng bạn tránh sự nhân số tử liệu dư thừa trên đầu vào.

> KV 缓存 giải quyết vấn đề này.  tính toán mỗi token của K và V 后 lưu chúng.  Tạo ra token N+1  Khi bạn chỉ cần tính toán các token mới của Q và tìm ra tất cả các token trước đó 缓存 của K và V.  Điều này sẽ làm cho K và V 计算 mỗi token thành phần từ O(N) giảm xuống O(1)                                                                                                                                                                                                                  

Đối với GPT-2 với 12 lớp và 12 đầu, bộ nhớ cache KV lưu trữ 2 (K + V) x 12 lớp x 12 đầu x 64 dims = 18.432 giá trị mỗi token. Đối với một chuỗi 1024 token, đó là khoảng 75MB trong FP32. Đối với Llama 3 405B với 128 lớp, bộ nhớ cache KV cho một chuỗi duy nhất có thể vượt quá 10GB. Đây là lý do tại sao suy luận ngữ cảnh dài bị ràng buộc bởi bộ nhớ.

> Đối với 12 tầng 12 đầu GPT-2,KV 缓存 mỗi token  lưu trữ 2(K + V) x 12 tầng x 12 đầu x 64 维 = 18,432 个值。 Đối với 1024 token序列, trong FP32 khoảng 75MB。 Đối với 128 tầng Llama 3 405B, KV 缓存 của một chuỗi có thể vượt quá 10GB。 đó là lý do tại sao dài hạn của các định nghĩa là trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong

### Prefill vs Decode: Hai giai đoạn của việc đưa ra

Khi bạn gửi một lời nhắc đến một LLM, suy luận xảy ra trong hai giai đoạn khác nhau.

> Khi bạn gửi thư đến LLM, việc đưa ra quyết định sẽ diễn ra trong hai giai đoạn khác nhau.

**Prefill**xử lý toàn bộ lệnh liên tục của bạn song song. Tất cả các token được biết đến, vì vậy mô hình có thể tính toán sự chú ý cho tất cả các vị trí cùng một lúc.

> **预填充（Prefill）**Và hành trình xử lý toàn bộ lệnh. Tất cả các token được biết đến, vì vậy mô hình có thể tính cùng một lúc tất cả các vị trí chú ý.

**Decode**tạo ra token một lần. Mỗi token mới phụ thuộc vào tất cả các token trước đó. Giai đoạn này là kết nối với bộ nhớ -- nút thắt đọc trọng lượng mô hình và bộ nhớ cache KV từ bộ nhớ GPU, không phải chính toán tử. Các lõi tính toán của GPU hầu hết ngồi yên chờ đọc bộ nhớ. Đối với GPT-2, mỗi bước giải mã mất khoảng cùng một thời gian bất kể số FLOPs mà các matmuls yêu cầu, bởi vì băng thông bộ nhớ là hạn chế.

> **解码（Decode）**个别生成代币――每个新代币取决于所有之前代币――这个阶段是访问存储密集型的瓶是从 GPU 内存读取模型权重和KV缓存,而不是矩阵运算本身――GPU的计算核心大部分时间在等待内存读取――对于GPT-2,每个解码步骤的时间大致相同,无论矩阵乘法需要多少FLOP,因为内存宽度是有限的――

Sự khác biệt này quan trọng đối với hệ thống sản xuất. Scale thông qua trước với tính toán GPU (more FLOPS = prefill nhanh hơn). Decode thông qua scale với băng thông bộ nhớ (memory faster = decode nhanh hơn). Đó là lý do tại sao H100 của NVIDIA tập trung vào cải thiện băng thông bộ nhớ so với A100 - nó trực tiếp tăng tốc việc tạo token.

> Sự khác biệt này rất quan trọng đối với hệ thống sản xuất. Phân tích dung lượng dự trữ và GPU tính năng tương đương. FLOPS nhiều hơn = 更快预充)  Giải mã dung lượng và dung lượng dự trữ.

```mermaid
graph LR
    subgraph Prefill["Phase 1: Prefill"]
        direction TB
        P1["Full prompt\n(all tokens known)"]
        P2["Parallel computation\n(compute-bound)"]
        P3["Builds KV Cache"]
        P1 --> P2 --> P3
    end

    subgraph Decode["Phase 2: Decode"]
        direction TB
        D1["Generate token N"]
        D2["Read KV Cache\n(memory-bound)"]
        D3["Append to KV Cache"]
        D4["Generate token N+1"]
        D1 --> D2 --> D3 --> D4
        D4 -.->|repeat| D1
    end

    Prefill --> Decode

    style P1 fill:#1a1a2e,stroke:#51cf66,color:#fff
    style P2 fill:#1a1a2e,stroke:#51cf66,color:#fff
    style P3 fill:#1a1a2e,stroke:#51cf66,color:#fff
    style D1 fill:#1a1a2e,stroke:#e94560,color:#fff
    style D2 fill:#1a1a2e,stroke:#e94560,color:#fff
    style D3 fill:#1a1a2e,stroke:#e94560,color:#fff
    style D4 fill:#1a1a2e,stroke:#e94560,color:#fff
```

### Lòng huấn luyện

Việc đào tạo LLM là dự đoán token tiếp theo. Với các token [0, 1, 2, ..., N-1], dự đoán token [1, 2, 3, ..., N].

> 训练 LLM 就是下一代币 预测──给定代币 [0, 1, 2, ..., N-1],预测代币 [1, 2, 3, ..., N]──损失函数是模型预测的概率分布与实际下一代币 之间交叉──

Một bước huấn luyện:

> Một bước tập luyện:

1. **Forward pass**: Tham gia các lô thông qua tất cả 12 khối.
2. **Compute loss**: Cross-entropy giữa logits và token mục tiêu (khả năng nhập chuyển đổi bằng một vị trí).
3. **Backward pass**: Xét gradient cho tất cả các tham số 124M bằng cách sử dụng backpropagation.
4. **Optimizer step**GPT-2 sử dụng Adam để tăng tốc độ học tập và phân hủy cosine.

Chương trình học tập có nhiều tính quan trọng hơn bạn có thể mong đợi. GPT-2 nóng lên từ 0 đến tốc độ học tập đỉnh trong 2.000 bước đầu tiên, sau đó phân rã theo đường cong cosine. Bắt đầu với tốc độ học tập cao làm cho mô hình phân biệt. Cần suất học tập cao liên tục gây ra dao động trong đào tạo sau đó.

> GPT-2 trong 2.000 bước trước từ 0 预热到峰值学习率, sau đó theo đường cong string giảm dần.

### GPT-2 Small: Số

| Component | Shape | Parameters |
|-----------|-------|------------|
| Token embeddings | (50257, 768) | 38,597,376 |
| Position embeddings | (1024, 768) | 786,432 |
| Per-block attention (W_q, W_k, W_v, W_out) | 4 x (768, 768) | 2,359,296 |
| Per-block FFN (up + down) | (768, 3072) + (3072, 768) | 4,718,592 |
| Per-block LayerNorms (2x) | 2 x 768 x 2 | 3,072 |
| Final LayerNorm | 768 x 2 | 1,536 |
| **Total per block** | | **7,080,960** |
| **Total (12 blocks)** | | **85,054,464 + 39,383,808 = 124,438,272** |

Dự án đầu ra ( đầu logits) chia sẻ trọng lượng với các mã hóa nhúng. Điều này được gọi là liên kết trọng lượng - nó làm giảm số lượng tham số bằng 38M và cải thiện hiệu suất bởi vì nó buộc mô hình sử dụng cùng không gian đại diện cho đầu vào và đầu ra.

> **【中文解读】**GPT-2 phân bố các tham số: token 嵌入层占 38.6M(50257 x 768),12 个 Transformer块各占 7.1M,最终 LayerNorm 仅1.5K。权重共享(权重绑定)让输出投影层复用代币 嵌入矩阵,减少38M 参数的同时还提升性能因为输入和输出被强制使用相同表示空间──

## Hãy xây dựng nó.

### Bước 1: Đặt lớp

Các token embedment lập bản đồ mỗi 50257 token có thể được chuyển thành một vector 768 chiều.

> Token 嵌入将 50,257 个可能的 token 各映射到一个768 维向量――位置嵌入 添加每个 token 在序列中位置的信息――两者相加――

```python
import numpy as np

class Embedding:
    def __init__(self, vocab_size, embed_dim, max_seq_len):
        self.token_embed = np.random.randn(vocab_size, embed_dim) * 0.02
        self.pos_embed = np.random.randn(max_seq_len, embed_dim) * 0.02

    def forward(self, token_ids):
        seq_len = token_ids.shape[-1]
        tok_emb = self.token_embed[token_ids]
        pos_emb = self.pos_embed[:seq_len]
        return tok_emb + pos_emb
```

Sự lệch chuẩn 0,02 cho khởi tạo xuất phát từ giấy GPT-2. quá lớn và các bước đi trước ban đầu tạo ra các giá trị cực đoan gây mất ổn định cho đào tạo. quá nhỏ và các đầu ra ban đầu gần như giống nhau cho tất cả các đầu vào, làm cho các tín hiệu gradient sớm vô dụng.

> 0.02 标准差的初始化来自GPT-2 论文──太大则初始前向传播产生极端值,破坏训练稳定性──太小则所有输入的初始输出几乎相同,使得早期梯度信号无用──

### Bước 2: Kiểm tra bản thân bằng mặt nạ nguyên nhân

Đầu tiên là chú ý một đầu. Mặt nạ nguyên nhân đặt vị trí tương lai lên vô hạn âm trước softmax, đảm bảo mỗi vị trí chỉ có thể chăm sóc cho chính nó và vị trí trước đó.

> Trước tiên làm một cái đầu chú ý. Trước tiên ẩn dấu hiệu trong Softmax trước tiên định vị trí tương lai là âm tính vô hạn, đảm bảo mỗi vị trí chỉ có thể chú ý đến vị trí của chính mình và trước đó.

```python
def attention(Q, K, V, mask=None):
    d_k = Q.shape[-1]
    scores = Q @ K.transpose(0, -1, -2 if Q.ndim == 4 else 1) / np.sqrt(d_k)
    if mask is not None:
        scores = scores + mask
    weights = np.exp(scores - scores.max(axis=-1, keepdims=True))
    weights = weights / weights.sum(axis=-1, keepdims=True)
    return weights @ V
```

Việc thực hiện softmax trừ tối đa trước khi tăng trưởng. Nếu không có điều này, exp(large_number) tràn sang vô hạn. Đây là một thủ thuật ổn định số mà không thay đổi đầu ra bởi vì softmax(x - c) = softmax(x) cho bất kỳ định vị c nào.

> softmax 实现在取指数前减去最大值──没有这个,exp(lớn_number) 会溢出到无穷大──这是一个数值稳定性技巧,不改变输出,因为 đối với bất kỳ thường số c,softmax(x - c) = softmax(x)──

### Bước 3: Cung cấp nhiều đầu

Chia các đầu vào 768 chiều thành 12 đầu có mỗi chiều 64 chiều. Mỗi đầu tính toán sự chú ý độc lập. Kết quả kết hợp và dự án trở lại 768 chiều.

> Để phân chia 768 维输入 thành 12 个 64 维的头―― mỗi đầu độc lập tính toán chú ý――拼接结果并投影回 768 维――

```python
class MultiHeadAttention:
    def __init__(self, embed_dim, num_heads):
        self.num_heads = num_heads
        self.head_dim = embed_dim // num_heads
        self.W_q = np.random.randn(embed_dim, embed_dim) * 0.02
        self.W_k = np.random.randn(embed_dim, embed_dim) * 0.02
        self.W_v = np.random.randn(embed_dim, embed_dim) * 0.02
        self.W_out = np.random.randn(embed_dim, embed_dim) * 0.02

    def forward(self, x, mask=None):
        batch, seq_len, d = x.shape
        Q = (x @ self.W_q).reshape(batch, seq_len, self.num_heads, self.head_dim).transpose(0, 2, 1, 3)
        K = (x @ self.W_k).reshape(batch, seq_len, self.num_heads, self.head_dim).transpose(0, 2, 1, 3)
        V = (x @ self.W_v).reshape(batch, seq_len, self.num_heads, self.head_dim).transpose(0, 2, 1, 3)

        scores = Q @ K.transpose(0, 1, 3, 2) / np.sqrt(self.head_dim)
        if mask is not None:
            scores = scores + mask
        weights = np.exp(scores - scores.max(axis=-1, keepdims=True))
        weights = weights / weights.sum(axis=-1, keepdims=True)
        attn_out = weights @ V

        attn_out = attn_out.transpose(0, 2, 1, 3).reshape(batch, seq_len, d)
        return attn_out @ self.W_out
```

Chín chuyển hình-hình hình-hình hình lại là phần nhầm lẫn nhất của sự chú ý đa đầu. Đây là những gì xảy ra: tensor (batch, seq_len, 768) trở thành (batch, seq_len, 12, 64), sau đó (batch, 12, seq_len, 64). Bây giờ mỗi 12 đầu có matrix riêng của mình (seq_len, 64) để chạy sự chú ý. Sau khi chú ý, chúng ta đảo ngược quá trình: (batch, 12, seq_len, 64) trở thành (batch, seq_len, 12, 64) trở thành (batch, seq_len, 768).

> 张量变为 (batch, seq_len, 12, 64),然后 (batch, 12, seq_len, 64)。现在 12个头各有自己的 (seq_len, 64) 矩阵来运行注意力。注意力后,我们反转过程:(batch, 12, seq_len, 64) 变为 (batch, seq_len, 12, 64) 变为 (batch, seq_len, 768)。

### Bước 4: Phòng chuyển đổi

Một khối biến đổi hoàn chỉnh: LayerNorm, chú ý nhiều đầu với dư, LayerNorm, feedforward với dư.

> Một bộ biến đổi hoàn chỉnh 块:LayerNorm、带残差的多头注意力、LayerNorm、带残差的前网络──

```python
class LayerNorm:
    def __init__(self, dim, eps=1e-5):
        self.gamma = np.ones(dim)
        self.beta = np.zeros(dim)
        self.eps = eps

    def forward(self, x):
        mean = x.mean(axis=-1, keepdims=True)
        var = x.var(axis=-1, keepdims=True)
        return self.gamma * (x - mean) / np.sqrt(var + self.eps) + self.beta


class FeedForward:
    def __init__(self, embed_dim, ff_dim):
        self.W1 = np.random.randn(embed_dim, ff_dim) * 0.02
        self.b1 = np.zeros(ff_dim)
        self.W2 = np.random.randn(ff_dim, embed_dim) * 0.02
        self.b2 = np.zeros(embed_dim)

    def forward(self, x):
        h = x @ self.W1 + self.b1
        h = np.maximum(0, h)  # GELU approximation: ReLU for simplicity
        return h @ self.W2 + self.b2


class TransformerBlock:
    def __init__(self, embed_dim, num_heads, ff_dim):
        self.ln1 = LayerNorm(embed_dim)
        self.attn = MultiHeadAttention(embed_dim, num_heads)
        self.ln2 = LayerNorm(embed_dim)
        self.ffn = FeedForward(embed_dim, ff_dim)

    def forward(self, x, mask=None):
        x = x + self.attn.forward(self.ln1.forward(x), mask)
        x = x + self.ffn.forward(self.ln2.forward(x))
        return x
```

Mạng feedforward mở rộng đầu vào 768 chiều lên 3.072 chiều (4x), áp dụng tính không tuyến tính, sau đó chiếu trở lại 768. Mô hình thu nhỏ mở rộng này cung cấp cho mô hình một đại diện nội bộ "thế hơn" để làm việc tại mỗi vị trí. GPT-2 sử dụng kích hoạt GELU, nhưng chúng tôi sử dụng ReLU ở đây để đơn giản hơn - sự khác biệt nhỏ để hiểu kiến trúc.

> Trước đây, mạng sẽ mở rộng 768 维输入 lên 3.072 维(4 倍), ứng dụng không tuyến tính, sau đó chiếu lại 768 ⋅.

### Bước 5: Mô hình GPT đầy đủ

Lắp lên 12 khối biến đổi. Thêm lớp nhúng ở phía trước và dự đoán đầu ra ở phía sau.

> 堆叠 12 变压器 块──前面加嵌层,后面加输出投影──

```python
class MiniGPT:
    def __init__(self, vocab_size=50257, embed_dim=768, num_heads=12,
                 num_layers=12, max_seq_len=1024, ff_dim=3072):
        self.embedding = Embedding(vocab_size, embed_dim, max_seq_len)
        self.blocks = [
            TransformerBlock(embed_dim, num_heads, ff_dim)
            for _ in range(num_layers)
        ]
        self.ln_f = LayerNorm(embed_dim)
        self.vocab_size = vocab_size
        self.embed_dim = embed_dim

    def forward(self, token_ids):
        seq_len = token_ids.shape[-1]
        mask = np.triu(np.full((seq_len, seq_len), -1e9), k=1)

        x = self.embedding.forward(token_ids)
        for block in self.blocks:
            x = block.forward(x, mask)
        x = self.ln_f.forward(x)

        logits = x @ self.embedding.token_embed.T
        return logits

    def count_parameters(self):
        total = 0
        total += self.embedding.token_embed.size
        total += self.embedding.pos_embed.size
        for block in self.blocks:
            total += block.attn.W_q.size + block.attn.W_k.size
            total += block.attn.W_v.size + block.attn.W_out.size
            total += block.ffn.W1.size + block.ffn.b1.size
            total += block.ffn.W2.size + block.ffn.b2.size
            total += block.ln1.gamma.size + block.ln1.beta.size
            total += block.ln2.gamma.size + block.ln2.beta.size
        total += self.ln_f.gamma.size + self.ln_f.beta.size
        return total
```

Nhận ra sự liên kết trọng lượng: `logits = x @ self.embedding.token_embed.T`. Dự án đầu ra sử dụng lại các mã thông báo nhúng tử liệu (được chuyển giao). Đây không chỉ là một thủ thuật tiết kiệm tham số. Nó có nghĩa là mô hình sử dụng cùng không gian vector để hiểu các mã thông báo (nhúng) và dự đoán chúng (phản xuất).

> chú ý quyền chia sẻ:`logits = x @ self.embedding.token_embed.T`△输出投影复用代币 嵌入矩阵(转置) ・・・ Đây không chỉ là kỹ thuật tiết kiệm các参数── nó có nghĩa là mô hình sử dụng cùng một không gian khối lượng để hiểu các token(嵌入) và预测 token(输出) ・・・

### Bước 6: Lòng huấn luyện

Để thực hiện một cuộc tập luyện thực sự trên các tham số 124M, bạn sẽ cần một GPU và PyTorch. vòng tập luyện này cho thấy cơ học trên một mô hình nhỏ chạy trong numpy tinh khiết. Chúng tôi sử dụng một mô hình nhỏ (4 lớp, 4 đầu, 128 dims) để làm cho nó dễ xử lý.

> Đối với các hệ thống thực tế của các số 124M, bạn cần GPU và PyTorch.

```python
def cross_entropy_loss(logits, targets):
    batch, seq_len, vocab_size = logits.shape
    logits_flat = logits.reshape(-1, vocab_size)
    targets_flat = targets.reshape(-1)

    max_logits = logits_flat.max(axis=-1, keepdims=True)
    log_softmax = logits_flat - max_logits - np.log(
        np.exp(logits_flat - max_logits).sum(axis=-1, keepdims=True)
    )

    loss = -log_softmax[np.arange(len(targets_flat)), targets_flat].mean()
    return loss


def train_mini_gpt(text, vocab_size=256, embed_dim=128, num_heads=4,
                   num_layers=4, seq_len=64, num_steps=200, lr=3e-4):
    tokens = np.array(list(text.encode("utf-8")[:2048]))
    model = MiniGPT(
        vocab_size=vocab_size, embed_dim=embed_dim, num_heads=num_heads,
        num_layers=num_layers, max_seq_len=seq_len, ff_dim=embed_dim * 4
    )

    print(f"Model parameters: {model.count_parameters():,}")
    print(f"Training tokens: {len(tokens):,}")
    print(f"Config: {num_layers} layers, {num_heads} heads, {embed_dim} dims")
    print()

    for step in range(num_steps):
        start_idx = np.random.randint(0, max(1, len(tokens) - seq_len - 1))
        batch_tokens = tokens[start_idx:start_idx + seq_len + 1]

        input_ids = batch_tokens[:-1].reshape(1, -1)
        target_ids = batch_tokens[1:].reshape(1, -1)

        logits = model.forward(input_ids)
        loss = cross_entropy_loss(logits, target_ids)

        if step % 20 == 0:
            print(f"Step {step:4d} | Loss: {loss:.4f}")

    return model
```

Sự mất mát bắt đầu gần ln(vocab_size) - cho một từ vựng cấp bay 256 token, đó là ln(256) = 5.55. Một mô hình ngẫu nhiên gán xác suất bằng nhau cho mỗi token. Khi đào tạo tiến triển, sự mất mát giảm vì mô hình học cách dự đoán các mẫu phổ biến: "th" sau "t", không gian sau một khoảng thời gian, v.v.

> 损失初始接近 ln(vocab_size)  đối với 256 token 字节级词表,即 ln(256) = 5.55。随机模型给每个 token 分配等概率。随着训练进行,损失下降,因为模型学会预测常见模式:"t" 后面是"th",句号后面是空格等。

Trong sản xuất, bạn sẽ sử dụng tối ưu hóa Adam với tích lũy gradient, tăng tốc độ học tập và cắt gradient.

> Trong sản xuất, bạn sẽ sử dụng Adam  tối ưu hóa cùng hợp tác độ tích lũy ∞ tỷ lệ học dự kiến nhiệt và độ cắt ∞ vòng chuyển tiếp-lạc-lạc-lạc-tải tiến là giống nhau ∞

### Bước 7: Tạo văn bản

Tạo ra sử dụng mô hình được đào tạo để dự đoán một token một lúc. Mỗi dự đoán được lấy mẫu từ phân phối đầu ra (hoặc được lấy tham lam như argmax).

> 生成使用训练好的模型个个预测 token──每个预测从输出分布中采样(或贪心地取 argmax)──

```python
def generate(model, prompt_tokens, max_new_tokens=100, temperature=0.8):
    tokens = list(prompt_tokens)
    seq_len = model.embedding.pos_embed.shape[0]

    for _ in range(max_new_tokens):
        context = np.array(tokens[-seq_len:]).reshape(1, -1)
        logits = model.forward(context)
        next_logits = logits[0, -1, :]

        next_logits = next_logits / temperature
        probs = np.exp(next_logits - next_logits.max())
        probs = probs / probs.sum()

        next_token = np.random.choice(len(probs), p=probs)
        tokens.append(next_token)

    return tokens
```

Nhiệt độ điều khiển sự ngẫu nhiên. Nhiệt độ 1.0 sử dụng phân phối nguyên thô. Nhiệt độ 0.5 sắc sắc nét nó (đáng xác định hơn - mô hình chọn lựa hàng đầu thường xuyên hơn). Nhiệt độ 1.5 làm cho nó mảng (những token ngẫu nhiên hơn - các token xác suất thấp có cơ hội lớn hơn). Nhiệt độ 0.0 là giải mã tham lam (luôn chọn token xác suất cao nhất).

> 温度控制随机性──温度 1.0 使用原始分布──温度 0.5 使其更尖(更确定性模型更频繁地选择顶部候选)──温度 1.5 使其更平坦(更随机低概率代币 获得更大的机会)──温度 0.0 是贪心解码(始终选择最高概率代币)──

- `tokens[-seq_len:]`cửa sổ là cần thiết bởi vì mô hình có chiều dài ngữ cảnh tối đa (1024 cho GPT-2). Một khi bạn vượt quá nó, bạn phải thả các mã thông báo cũ nhất. Đây là "bỗng cửa sổ ngữ cảnh" mà mọi người nói về.

> `tokens[-seq_len:]`窗口 là cần thiết, vì mô hình có chiều dài tối đa trên 下文.

## Hãy sử dụng nó để thực hiện
```figure
sampling-decoder
```

## Sử dụng nó

### Đào tạo và Demo thế hệ đầy đủ

```python
corpus = """The transformer architecture has revolutionized natural language processing.
Attention mechanisms allow the model to focus on relevant parts of the input.
Self-attention computes relationships between all pairs of positions in a sequence.
Multi-head attention splits the representation into multiple subspaces.
Each attention head can learn different types of relationships.
The feedforward network provides nonlinear transformations at each position.
Residual connections enable gradient flow through deep networks.
Layer normalization stabilizes training by normalizing activations.
Position embeddings give the model information about token ordering.
The causal mask ensures autoregressive generation during training.
Pre-training on large text corpora teaches the model general language understanding.
Fine-tuning adapts the pre-trained model to specific downstream tasks."""

model = train_mini_gpt(corpus, num_steps=200)

prompt = list("The transformer".encode("utf-8"))
output_tokens = generate(model, prompt, max_new_tokens=100, temperature=0.8)
generated_text = bytes(output_tokens).decode("utf-8", errors="replace")
print(f"\nGenerated: {generated_text}")
```

Trên một bản nhỏ với một mô hình nhỏ, văn bản được tạo ra sẽ là bán nhất quán trong tốt nhất. Nó sẽ học được một số mẫu cấp bayt từ văn bản đào tạo nhưng không thể tổng quát cách GPT-2 làm với dữ liệu đào tạo 40GB và kiến trúc tham số đầy đủ 124M. Điểm là không phải chất lượng đầu ra. Ý tưởng là bạn có thể theo dõi từng bước: tìm kiếm tích hợp, tính toán chú ý, chuyển đổi chuyển tiếp, dự đoán logit, softmax và lấy mẫu. Mọi hoạt động đều hiển thị.

> Trong các mô hình nhỏ và nhỏ, lượng văn bản được tạo là nửa liên tục. Nó sẽ học từ các mô hình lớp chữ cái, nhưng không thể phổ biến như GPT-2 trong 40GB dữ liệu đào tạo và cấu trúc số liệu 124M hoàn chỉnh.

## Chuyển nó đi.

Bài học này sẽ mang lại kết quả `outputs/prompt-gpt-architecture-analyzer.md`-- một lời nhắc phân tích các lựa chọn kiến trúc trong bất kỳ mô hình kiểu GPT nào. Đưa cho nó một thẻ mô hình hoặc báo cáo kỹ thuật và nó phân chia phân bổ tham số, thiết kế chú ý và quyết định quy mô.

> 本课产 出 `outputs/prompt-gpt-architecture-analyzer.md` Một phân tích bất kỳ GPT 风格模型架构选择的提示──输入模型卡或技术报告, nó sẽ phân chia phân phối các tham số、注意设计和缩缩决策──

## Tập luyện bài tập

1. Thay vào 12/12, hãy sửa đổi mô hình để sử dụng 24 lớp và 16 đầu.

2. Thực hiện chức năng kích hoạt GELU (GELU(x) = x * 0.5 * (1 + erf(x / sqrt(2)))) và thay thế ReLU trong mạng feedforward.

3. Thêm một bộ nhớ cache KV vào chức năng tạo. Cung cấp các tensor K và V cho mỗi lớp sau khi chuyển tiếp trước đầu tiên, và sử dụng lại cho các token tiếp theo. Đo tốc độ tăng tốc: tạo 200 token với và không có bộ nhớ cache và so sánh thời gian đồng hồ tường.

4. Thực hiện lấy mẫu top-k (chỉ xem xét các token có xác suất cao nhất k) và lấy mẫu top-p (chọn mẫu lõi: xem xét bộ token nhỏ nhất có xác suất tích lũy vượt quá p). So sánh chất lượng đầu ra ở nhiệt độ 0,8 với top-k=50 so với top-p=0,95.

5. Xây dựng một trình soạn thảo đường cong mất tập luyện. Xây dựng mô hình cho 1000 bước và đường cong mất vs bước. Xác định ba giai đoạn: giảm ban đầu nhanh (đọc các byte phổ biến), giai đoạn trung gian chậm hơn (đọc các mô hình byte), và trũng cao (đóng trên cơ thể nhỏ).

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|----------------------|---------|
| Autoregressive | "It generates one word at a time" | Each output token is conditioned on all previous tokens -- the model predicts P(token_n \| token_0, ..., token_{n-1}) | 自回归，逐 token 生成，每个 token 依赖之前所有 token |
| Causal mask | "It can't see the future" | An upper-triangular matrix of -infinity values that prevents attention to future positions during training | 因果掩码，防止看到未来位置 |
| Multi-head attention | "Multiple attention patterns" | Splitting Q, K, V into parallel heads (e.g., 12 heads of 64 dims each for GPT-2) so each head can learn different relationship types | 多头注意力，并行学习不同关系类型 |
| KV Cache | "Caching for speed" | Storing computed Key and Value tensors from previous tokens to avoid redundant computation during autoregressive generation | KV 缓存，避免重复计算已生成 token 的 K/V |
| Prefill | "Processing the prompt" | The first inference phase where all prompt tokens are processed in parallel -- compute-bound on GPU FLOPS | 预填充阶段，并行处理 prompt，计算密集 |
| Decode | "Generating tokens" | The second inference phase where tokens are generated one at a time -- memory-bound on GPU bandwidth | 解码阶段，逐 token 生成，访存密集 |
| Weight tying | "Sharing embeddings" | Using the same matrix for input token embeddings and the output projection head -- saves 38M params in GPT-2 | 权重共享，输入输出共用嵌入矩阵 |
| Residual connection | "Skip connection" | Adding the input directly to the output of a sublayer (x + sublayer(x)) -- enables gradient flow in deep networks | 残差连接，使深层网络梯度流通 |
| Layer normalization | "Normalizing activations" | Normalizing across the feature dimension to mean 0 and variance 1, with learnable scale and bias parameters | 层归一化，特征维度归一化 |
| Cross-entropy loss | "How wrong the predictions are" | -log(probability assigned to the correct next token), averaged over all positions -- the standard LLM training objective | 交叉熵损失，LLM 训练的标准目标函数 |

## Xem thêm 延伸阅读

- [Radford et al., 2019 -- "Language Models are Unsupervised Multitask Learners" (GPT-2)](https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf)-- giấy GPT-2 giới thiệu các thông số từ 124M đến 1.5B
- [Vaswani et al., 2017 -- "Attention Is All You Need"](https://arxiv.org/abs/1706.03762)- giấy biến đổi gốc với sự chú ý của sản phẩm điểm và sự chú ý đa đầu
- [Llama 3 Technical Report](https://arxiv.org/abs/2407.21783)-- làm thế nào Meta mở rộng kiến trúc GPT đến 405B tham số với 16K GPU
- [Pope et al., 2022 -- "Efficiently Scaling Transformer Inference"](https://arxiv.org/abs/2211.05102)-- bài báo đã chính thức hóa phân tích cache KV và prefill vs decode
