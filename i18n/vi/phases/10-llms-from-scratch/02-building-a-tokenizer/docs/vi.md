# Xây dựng một Tokenizer từ đầu ừ không xây dựng分词器

> Bài học 01 cho bạn một đồ chơi. Bài học này cho bạn một vũ khí.

> **【中文解读】**BPE của lớp thứ nhất là đồ chơi,本课构建生产级分词器: xử lý Unicode、空白归归一化、特殊代币、字节级回退(让任何输入都能编码,包括emoji 和中文) ⋅

> **【拓展：tiktoken/HuggingFace】**Các chữ ký và các chữ cái của GPT-4 đều là sự thực hiện của các loại từ sản xuất.

>  **【前置】**学本节前请先掌握:(1) Bước 10·01(Tokenizers: BPE/WordPiece/SentencePiece)  hiểu BPE 合并循环和合并表的概念;(2) Unicode và UTF-8 编码codepoint、字节、NFC/NFKC 归一化的区别;(3) 正则表达式特别是`\p{L}``\p{N}`、负向先行断言 `(?!\S)`;(4) Python `regex`库(不是标准 `re`Vì`re`Không hỗ trợ thuộc tính Unicode)。

**Type:** Build
**Languages:** Python
**Prerequisites:** Phase 10, Lesson 01 (Tokenizers: BPE, WordPiece, SentencePiece)
**Time:** ~90 minutes

## Mục tiêu học tập

- Xây dựng một token BPE cấp sản xuất xử lý Unicode, chuẩn hóa không gian trắng và các token đặc biệt
   cấu trúc xử lý Unicode、空白归归化和特殊代币的生产级 BPE 分词器
- Thực hiện fallback cấp bayt để tokenizer có thể mã hóa bất kỳ đầu vào (bao gồm emoji, CJK và mã) mà không có token không rõ
  实现字节级回退,使分词器能编码任何输入(包括emoji、CJK、代码) mà không tạo ra mã thông báo không rõ ràng
- Thêm các mẫu regex trước khi kết hợp mã hóa để chia văn bản ở giới hạn từ trước khi áp dụng các sự kết hợp BPE
  添加预分词正则模式, trong BPE 合并前按词边界拆分文本
- Trình luyện một token custom trên một corpus và đánh giá tỷ lệ nén của nó so với tiktoken trên văn bản đa ngôn ngữ
  Trong ngữ cảnh, tập luyện tự định nghĩa phân từ, và đánh giá tỷ lệ nén của nó với tiktoken trên văn bản đa ngôn ngữ

> **【中文解读】**Mục tiêu của bài học này là nâng cấp các trò chơi BPE cho các loại phân từ sản xuất. Những cải tiến quan trọng bao gồm: Unicode 归一化 (NFC) 预分词正则 (để ngăn chặn sự hợp并 (tích hợp) 字节级回退 (tích nhận) 零未知) 特别代币 (để quản lý) BOS/EOS/聊天模板标记器 (chữ liệu).

## Vấn đề  vấn đề giới thiệu

BPE của bạn từ bài học 01 hoạt động trên văn bản tiếng Anh. Bây giờ ném tiếng Nhật vào nó hoặc emoji hoặc mã Python với các tab và không gian hỗn hợp.

> Bạn có thể dùng các mã Python để xử lý các văn bản tiếng Anh.

Nó bị vỡ.

> Nó sẽ sụp đổ.

Không phải vì BPE sai, bởi vì việc thực hiện là không hoàn chỉnh. Một tokenizer sản xuất xử lý các byte thô trong bất kỳ mã hóa nào, bình thường hóa Unicode trước khi chia, quản lý các token đặc biệt không bao giờ được hợp nhất, chuỗi pre-tokenization với phân chia từ phụ, và làm tất cả những điều này đủ nhanh để không làm tắc nghẽn một đường ống đào tạo xử lý 15 nghìn tỷ token.

> Không phải vì BPE có vấn đề, mà vì thực hiện không hoàn chỉnh. Các sản phẩm phân từ thiết bị xử lý các phần tử gốc của bất kỳ mã hóa, trong phân chia trước khi phân phối Unicode, quản lý không bao giờ tham gia hợp tác các mã thông báo đặc biệt,串联预分词与子词分割, và tất cả các hoạt động đều đủ nhanh, sẽ không trở thành xử lý 15 tỷ token của training pipeline.

GPT-2 có 50.257 token. Llama 3 có 128.256. GPT-4 có khoảng 100.000. Đây không phải là những con số đồ chơi. Các bảng hợp tác đằng sau các từ vựng đó được đào tạo trên hàng trăm gigabytes văn bản, và các thiết bị xung quanh -- bình thường hóa, pre-tokenization, tiêm mã thông báo đặc biệt, định dạng mẫu trò chuyện -- là những gì tách biệt một tokenizer xử lý "hello world" từ một cái xử lý toàn bộ Internet.

> GPT-2 có 50,257 token. Llama 3 có 128,256 token. GPT-4 có khoảng 100.000 token. Đây không phải là một số trò chơi. Những biểu đồ này được tập hợp trên 100 GB, trong khi cơ chế xung quanh của nó là một phần của các biểu tượng.

Anh sẽ xây dựng máy móc đó.

> Anh sẽ xây dựng cơ chế đó.

> **【中文解读】**生产级分词器不是单一算法,而是一个五阶段管线:归一化 → 预分词 → BPE 合并 → 特殊代币注入 → ID 映射──每个阶段解决不同的问题──例如 NFKC 归一化把"fi" 连字(U+FB01) biến thành "fi" 两个字符,预分词防止"cat"被合并出"e c" 这样代币──

>  **【类比】**生产级分词器像"邮局的信件处理流水线":归一化是"统一邮编格式"(U+FB01 "fi" → "fi",全角字母 → 半角),预分词是"按目的地先分堆"(按词边界、数字、标点切,避免跨城市混装),BPE 合并是"高频包裹自动拼箱"(常见词直接整箱), đặc điểm là"挂号信标签"(BOS/EOS/PAD 最后永远不参与拼箱),才是"贴条形码" ((ID 映射) ⋅ bất kỳ gói nào bị bỏ rơi,邮件就乱.

> **【拓展：Llama 3 的分词器升级】**Meta 在 Llama 3 中将词表从 32K(Llama 2 的句子Piece BPE) nâng cấp lên 128K(tiktoken风格字节级 BPE), đặc biệt tăng mã thông báo không tiếng Anh phân chia.

## Khái niệm cốt lõi

### Lối ống dẫn đầy đủ

Một token sản xuất không phải là một thuật toán, nó là một đường ống của năm giai đoạn, mỗi giải quyết một vấn đề khác nhau.

> Kiểu phân từ sinh sản không phải là một thuật toán đơn lẻ. Nó là một đường ống năm giai đoạn, mỗi giai đoạn giải quyết các vấn đề khác nhau.

```mermaid
graph LR
    A[Raw Text] --> B[Normalize]
    B --> C[Pre-Tokenize]
    C --> D[BPE Merge]
    D --> E[Special Tokens]
    E --> F[Token IDs]

    style A fill:#1a1a2e,stroke:#e94560,color:#fff
    style B fill:#1a1a2e,stroke:#e94560,color:#fff
    style C fill:#1a1a2e,stroke:#e94560,color:#fff
    style D fill:#1a1a2e,stroke:#e94560,color:#fff
    style E fill:#1a1a2e,stroke:#e94560,color:#fff
    style F fill:#1a1a2e,stroke:#e94560,color:#fff
```

Mỗi giai đoạn có một công việc cụ thể:

> Mỗi giai đoạn có trách nhiệm cụ thể:

| Stage | What It Does | Why It Matters |
|-------|-------------|----------------|
| Normalize | NFKC Unicode, lowercase optional, strip accents optional | "fi" ligature (U+FB01) becomes "fi" (two chars). Without this, same word gets different tokens. |
| Pre-Tokenize | Split text into chunks before BPE | Prevents BPE from merging across word boundaries. "the cat" should never produce a token "e c". |
| BPE Merge | Apply learned merge rules to byte sequences | The core compression. Turns raw bytes into subword tokens. |
| Special Tokens | Inject [BOS], [EOS], [PAD], chat template markers | These tokens have fixed IDs. They never participate in BPE merges. The model needs them for structure. |
| ID Mapping | Convert token strings to integer IDs | The model sees integers, not strings. |

### BPE cấp bằng byte

Bài học 01 của tokenizer hoạt động trên UTF-8 byte. Đó là lời gọi đúng. Nhưng chúng tôi bỏ qua một điều quan trọng: điều gì xảy ra khi các byte đó không hợp lệ UTF-8?

> Phần đầu tiên của phân từ là hoạt động trên các chữ cái UTF-8. Đây là một lựa chọn đúng đắn. Nhưng chúng ta đã bỏ qua một số điều quan trọng: Điều gì sẽ xảy ra khi các chữ cái này không hiệu quả trong UTF-8?

BPE cấp bayt giải quyết điều này bằng cách xử lý mọi giá trị byte có thể (0-255) như một token hợp lệ. Từ vựng cơ sở của bạn chính xác là 256 mục. Bất kỳ tập tin nào - văn bản, nhị phân, bị hư hỏng - có thể được token mà không tạo ra một token không rõ.

> 字节级 BPE 通过将每个可能的字节值(0-255)视为有效代币来解决这个问题――你的基础词表恰好 256条条点――任何文件文本、二进制、损坏的都可以被分词而不会产生未知代币――

GPT-2 đã thêm một thủ thuật: lập bản đồ mỗi byte cho một ký tự Unicode in được để từ vựng vẫn có thể đọc được bởi con người. Byte 0x20 (không gian) trở thành ký tự "G" trong bản đồ của họ.

> GPT-2 thêm một lời khuyên: sẽ mỗi chữ cái được chiếu vào một chữ cái Unicode có thể in, để làm cho từ biểu hiện được đọc được.

Nguồn thực sự: BPE cấp bayt xử lý mọi ngôn ngữ trên thế giới. Các ký tự Trung Quốc là 3 byte UTF-8 mỗi. tiếng Nhật có thể là 3-4 byte. Ả Rập, Devanagari, emoji - tất cả chỉ là chuỗi byte. thuật toán BPE tìm kiếm các mẫu trong các chuỗi byte chính xác giống như nó tìm thấy các mẫu trong các byte ASCII tiếng Anh.

> Thực sự có thể: BPE  xử lý từng ngôn ngữ trên trái đất. Các chữ trung ký mỗi ngôn ngữ chiếm 3 chữ UTF-8.

> **【中文解读】**字节级 BPE:基础字符表恰好 256 字节值, bất kỳ输入都能编码;;GPT-2 còn làm một "花招" để mỗi字节 được映射 thành một Unicode 字符, để làm cho từ表 dễ đọc hơn;; Trung字符 trong UTF-8 chiếm 3 字节, tiếng Nhật chiếm 3-4 字节, emojis chiếm 4 字节BPE 算法 trong tất cả các chuỗi các字节 này hoạt động hoàn toàn giống nhau;;

### Pre-Tokenization

Trước khi BPE chạm vào văn bản của bạn, bạn cần chia nó thành các mảnh. Điều này ngăn chặn thuật toán kết hợp tạo ra các token trải dài ranh giới từ.

> Trước khi BPE xử lý văn bản của bạn, bạn cần phân chia nó thành khối. Điều này ngăn chặn thuật toán hợp tác tạo ra các token vượt qua giới hạn từ.

GPT-2 sử dụng mô hình regex để chia văn bản:

> GPT-2 sử dụng biểu hiện chính thức để phân chia văn bản:

```
'(?:[sdmt]|ll|ve|re)| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+
```

Mô hình này chia thành các ký tự (don't trở thành don + t), từ có không gian dẫn, số, dấu chấm và không gian trắng tùy chọn.

> 这个模式按缩写拆分("don't" 变成"don" + "'t")、带可选前导空格的词、数字、标点和空格。前导空格保持在词上所以"the cat" 变成 ["the", "cat"],而不是 ["the", "", "cat"]。

Llama sử dụng SentencePiece, mà bỏ qua regex hoàn toàn. Nó xử lý dòng byte thô như một chuỗi dài và cho phép thuật toán BPE tìm ra ranh giới. Điều này đơn giản hơn nhưng cho phép BPE tự do hơn để tạo các mã thông báo chữ chéo.

> Llama sử dụng SentencePiece, hoàn toàn nhảy qua biểu hiện chính thức. Nó sẽ được xem như một chuỗi dài, để BPE tự xác định biên giới.

Sự lựa chọn quan trọng. Regex của GPT-2 ngăn chặn tokenizer học rằng "the" ở cuối một từ và "the" ở đầu của từ tiếp theo nên hợp nhất. SentencePiece cho phép điều này, đôi khi tạo ra nén hiệu quả hơn nhưng ít giải thích các token.

> Sự lựa chọn này rất quan trọng. Quy tắc chính thức của GPT-2 là ngăn chặn phân từ học một từ cuối cùng của "the" 和下一个词开头 của "the" 合并──SentencePiece cho phép làm như vậy, đôi khi tạo ra hiệu quả hơn trong việc nén nhưng không quá dễ giải thích.

### Các token đặc biệt

Mỗi token sản xuất lưu trữ ID token cho các dấu hiệu cấu trúc:

> Mỗi sản xuất cấp分词器都为结构标记保留代币 ID:

| Token | Purpose | Used By |
|-------|---------|---------|
| `[BOS]` / `<s>` | Beginning of sequence | Llama 3, GPT |
| `[EOS]` / `</s>` | End of sequence | All models |
| `[PAD]` | Padding for batch alignment | BERT, T5 |
| `[UNK]` | Unknown token (byte-level BPE eliminates this) | BERT, WordPiece |
| `<\|im_start\|>` | Chat message boundary start | ChatGPT, Qwen |
| `<\|im_end\|>` | Chat message boundary end | ChatGPT, Qwen |
| `<\|user\|>` | User turn marker | Llama 3 |
| `<\|assistant\|>` | Assistant turn marker | Llama 3 |

Các mã thông báo đặc biệt không bao giờ được chia bởi BPE. Chúng được kết hợp chính xác trước khi thuật toán kết hợp chạy, thay thế bằng ID cố định của chúng, và văn bản xung quanh được mã thông báo bình thường.

> Các mã đặc biệt sẽ không bao giờ bị BPE phân chia. Chúng được xác định phù hợp trước khi hợp với thuật toán được thực hiện, thay thế cho ID cố định, văn bản xung quanh được phân chia.

> **【中文解读】**特殊 token 是分词器中"不可触"的保留标记:`[BOS]`(序列开始)`[EOS]`(序列结束)`[PAD]`(批次填充) 聊天模板标记等──它们 có ID cố định, không bao giờ tham gia BPE 合并, nhưng được lấy ra thông qua sự phù hợp chính xác trước khi hợp hợp. Llama 3 使用 `<|start_header_id|>``<|end_header_id|>``<|eot_id|>`Để ký kết cấu trúc đối thoại,ChatGPT `<|im_start|>`和 `<|im_end|>`

> **【拓展：聊天模板的工程陷阱】**聊天模板 là nơi dễ dàng nhất trong thực tế triển khai. Mỗi mô hình trong đào tạo sử dụng các mã thông báo đặc biệt theo định dạng cụ thể, bất kỳ sự khác biệt nào, bất kỳ sự khác biệt nào, không có thay đổi, nhiều không gian, mã thông báo, sự sai lầm trong trật tự sẽ khiến các đầu vào phân tán, dẫn đến mô hình phát ra rác.`chat_template`Jinja2 模板机制就是为了标准化这个过程――

> ️ **【易错点】**实现特殊代币的三个陷:(1) **特殊 token 内含正则元字符**如 `<|im_start|>`Trung `|`, phải dùng `re.escape()`转义,否则在 GPT-2 预分词的正则上会被解析成选择符;(2) **未从 BPE 词表中排除特殊 token**若 `<|im_end|>`Không được chia trước được tách ra, chuỗi ký tự của nó sẽ được BPE chia thành 8 biểu tượng, mô hình sẽ luôn nhìn không đến toàn bộ cấu trúc được đánh dấu;**`add_special_tokens=False` 漏配**调用 `tokenizer.encode(text)`默认会自动加 BOS/EOS,做拼接时会出现 BOS BOS EOS EOS 序列,破坏注意口罩对齐──修复:编码时显式传 `add_special_tokens=False`, cuối cùng bởi mô hình logic thống nhất vào.

### Các mẫu trò chuyện

Đây là nơi mà hầu hết mọi người bị nhầm lẫn và hầu hết các triển khai bị phá vỡ.

> Đó là nơi mà hầu hết mọi người bị bối rối, cũng là nơi mà hầu hết mọi người đều thực hiện sai lầm.

Khi bạn gửi tin nhắn đến mô hình trò chuyện, API chấp nhận một danh sách tin nhắn:

> Khi bạn gửi tin nhắn, API  chấp nhận một danh sách tin nhắn:

```
[
  {"role": "system", "content": "You are helpful."},
  {"role": "user", "content": "Hello"},
  {"role": "assistant", "content": "Hi there!"}
]
```

Mô hình không thấy JSON. Nó thấy một chuỗi token phẳng. Mô hình trò chuyện chuyển đổi tin nhắn thành chuỗi phẳng đó bằng cách sử dụng các token đặc biệt. Mỗi mô hình làm điều này khác nhau:

> 模型看不到 JSON──它 nhìn thấy là một chuỗi token 平── chat模板 sử dụng mã thông báo đặc biệt, sẽ chuyển đổi thông điệp thành chuỗi token 平── mỗi mô hình có cách khác nhau:

```
Llama 3:
<|begin_of_text|><|start_header_id|>system<|end_header_id|>

You are helpful.<|eot_id|><|start_header_id|>user<|end_header_id|>

Hello<|eot_id|><|start_header_id|>assistant<|end_header_id|>

Hi there!<|eot_id|>

ChatGPT:
<|im_start|>system
You are helpful.<|im_end|>
<|im_start|>user
Hello<|im_end|>
<|im_start|>assistant
Hi there!<|im_end|>
```

Nếu bạn sai mô hình, mô hình sẽ tạo ra rác. Nó được đào tạo theo một định dạng chính xác. Bất kỳ sự lệch nào - một dòng mới bị thiếu, một token được trao đổi, một không gian bổ sung - sẽ đưa đầu vào ra ngoài phân phối đào tạo.

> 模板搞错了模型就会产生垃圾输出――它 được đào tạo theo một cách chính xác―― bất kỳ sự khác biệt nào 缺少换行、交换代币、多一个空格都会使输入偏离训练分布――

> 🤔 **【困惑】**Q: Llama 3 tại sao lại bỏ lại SentencePiece 改用tiktoken?字节级 BPE 比原版强在哪? A: 两点关键优势:(1) **SentencePiece 用 ⊗（U+2581）代替空格**, đối với ASCII 字符和原始空格的混在聊天场景下导致代币序列 đối với prompt 微小变化过于敏感;tiktoken 直接保留前导空格,"hello"和"hello"是不同的代币,更稳定;**字节级 BPE 词表恰好 256 个基础 token**, về lý thuyết có thể mã hóa bất kỳ chuỗi chữ nào (bao gồm emoji、私有区字符), không phụ thuộc vào các ngữ料 cụ thể;SentencePiece 词表若未训练到某字符直接 [UNK]。Llama 3 词表 từ 32K 扩至 128K,多语言压缩比升升 ~2x, đây là một quyết định kỹ thuật để suy đoán chi phí mua đơn ⋅

### Tốc độ

Python quá chậm để làm token sản xuất.

> Python 对于生产级分词太慢了.

tiktoken (OpenAI) được viết bằng Rust với liên kết Python. HuggingFace tokenizers cũng là Rust. SentencePiece là C ++.

> tiktoken(OpenAI) dùng Rust 编写并提供 Python 绑定──HuggingFace tokenizers 也是Rust──SentencePiece 是C++──这些比纯Python 快 10-100倍──

Đối với viễn cảnh: token hóa 15 nghìn tỷ token cho Llama 3 trước đào tạo với 1 triệu token mỗi giây (fast Python) sẽ mất 174 ngày.

> Ví dụ: tốc độ của 100 triệu token mỗi giây (Quick Python) là Llama 3 预训分词 15 tỷ token 需要174 天――以每秒 1 tỷ token (Rust) tốc độ, chỉ cần 1.7 天――

Bạn đang xây dựng trong Python để hiểu thuật toán. Trong sản xuất, bạn sẽ sử dụng một thực hiện được biên soạn và chỉ chạm vào gói Python.

> Bạn sử dụng Python để xây dựng để hiểu thuật toán. Trong quá trình sản xuất, bạn sẽ sử dụng biên dịch để thực hiện, chỉ tiếp xúc với Python.

## Hãy xây dựng nó.
```figure
weight-tying
```

## Hãy xây dựng nó

### Bước 1: Mã hóa cấp độ byte

Các nền tảng. Chuyển đổi bất kỳ chuỗi nào thành một chuỗi các byte, lập bản đồ mỗi byte để hiển thị một ký tự in, và đảo ngược quá trình.

> 基础── sẽ chuyển bất kỳ chữ cái nào thành chuỗi chữ cái, sẽ mỗi chữ cái được chiếu đến các chữ cái có thể in được để hiển thị,并反转该过程──

```python
def bytes_to_tokens(text):
    return list(text.encode("utf-8"))

def tokens_to_text(token_bytes):
    return bytes(token_bytes).decode("utf-8", errors="replace")
```

Kiểm tra trên văn bản đa ngôn ngữ để xem số lượng byte:

```python
texts = [
    ("English", "hello"),
    ("Chinese", "你好"),
    ("Emoji", "🔥"),
    ("Mixed", "hello你好🔥"),
]

for label, text in texts:
    b = bytes_to_tokens(text)
    print(f"{label}: {len(text)} chars -> {len(b)} bytes -> {b}")
```

"hello" là 5 byte. "你好" là 6 byte (3 mỗi ký tự). Fire emoji là 4 byte.

> "Hello" là 5 字节──"你好" là 6 字节── mỗi字符 là 3 字节──火焰 emoji là 4 字节──字节级分词器不关心它是什么语言──字节就是字节──

### Bước 2: Pre- Tokenizer với Regex

Chia văn bản thành các mảnh bằng cách sử dụng mô hình GPT-2 regex. Mỗi mảnh được token hóa độc lập bởi BPE.

> Sử dụng GPT-2 正则模式将文本分成块──每个块由BPE 独立分词──

```python
import re

try:
    import regex
    GPT2_PATTERN = regex.compile(
        r"""'(?:[sdmt]|ll|ve|re)| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+"""
    )
except ImportError:
    GPT2_PATTERN = re.compile(
        r"""'(?:[sdmt]|ll|ve|re)| ?[a-zA-Z]+| ?[0-9]+| ?[^\s\w]+|\s+(?!\S)|\s+"""
    )

def pre_tokenize(text):
    return [match.group() for match in GPT2_PATTERN.finditer(text)]
```

- `regex`module hỗ trợ Unicode tính năng thoát (`\p{L}`cho thư, `\p{N}`cho các số). Thư viện tiêu chuẩn `re`module không, vì vậy chúng ta rơi lại vào lớp ký tự ASCII. Đối với sản xuất các tokenizers đa ngôn ngữ, cài đặt `regex`- Tôi không biết.

> `regex`模块支持 Unicode 属性转义(`\p{L}`表示字母,`\p{N}`表示数字) ・标准库 `re`模块不支持,所以我们回归 ASCII 字符类──对于生产级多语言分词器,请安装 `regex`

Hãy thử đi.

```python
print(pre_tokenize("Hello, world! Don't stop."))
# [' Hello', ',', ' world', '!', " Don", "'t", ' stop', '.']
```

Không gian dẫn tiếp tục gắn liền với từ. Khác nét chia ở chữ ký. Vị trí trở thành một phần của nó. BPE sẽ không bao giờ hợp nhất các token qua các ranh giới này.

>                                                                                                                                                                                                                                                               

### Bước 3: BPE trên các chuỗi byte

Các thuật toán cốt lõi từ bài học 01, nhưng bây giờ hoạt động trên các khối tiền-tokenized độc lập.

> Các thuật toán cốt lõi của lớp thứ nhất, nhưng bây giờ tự do thực hiện các hoạt động trên các khối của các từ dự định.

```python
from collections import Counter

def get_byte_pairs(chunks):
    pairs = Counter()
    for chunk in chunks:
        byte_seq = list(chunk.encode("utf-8"))
        for i in range(len(byte_seq) - 1):
            pairs[(byte_seq[i], byte_seq[i + 1])] += 1
    return pairs

def apply_merge(byte_seq, pair, new_id):
    merged = []
    i = 0
    while i < len(byte_seq):
        if i < len(byte_seq) - 1 and byte_seq[i] == pair[0] and byte_seq[i + 1] == pair[1]:
            merged.append(new_id)
            i += 2
        else:
            merged.append(byte_seq[i])
            i += 1
    return merged
```

### Bước 4: xử lý mã thông báo đặc biệt

Các token đặc biệt cần phải phù hợp chính xác và xác định danh tính.

> Các mã đặc biệt cần phải xác định sự phù hợp và xác định ID.

```python
class SpecialTokenHandler:
    def __init__(self):
        self.special_tokens = {}
        self.pattern = None

    def add_token(self, token_str, token_id):
        self.special_tokens[token_str] = token_id
        escaped = [re.escape(t) for t in sorted(self.special_tokens.keys(), key=len, reverse=True)]
        self.pattern = re.compile("|".join(escaped))

    def split_with_specials(self, text):
        if not self.pattern:
            return [(text, False)]
        parts = []
        last_end = 0
        for match in self.pattern.finditer(text):
            if match.start() > last_end:
                parts.append((text[last_end:match.start()], False))
            parts.append((match.group(), True))
            last_end = match.end()
        if last_end < len(text):
            parts.append((text[last_end:], False))
        return parts
```

### Bước 5: Kiểu Tokenizer đầy đủ

Kết nối mọi thứ với nhau: bình thường hóa, chia thành các token đặc biệt, pre-tokenize, BPE hợp nhất, bản đồ đến ID.

> 将所有步骤串联:归一化,按特殊代号 分割,预分词, BPE 合并,映射到ID,

```python
import unicodedata

class ProductionTokenizer:
    def __init__(self):
        self.merges = {}
        self.vocab = {i: bytes([i]) for i in range(256)}
        self.special_handler = SpecialTokenHandler()
        self.next_id = 256

    def normalize(self, text):
        return unicodedata.normalize("NFKC", text)

    def train(self, text, num_merges):
        text = self.normalize(text)
        chunks = pre_tokenize(text)
        chunk_bytes = [list(chunk.encode("utf-8")) for chunk in chunks]

        for i in range(num_merges):
            pairs = Counter()
            for seq in chunk_bytes:
                for j in range(len(seq) - 1):
                    pairs[(seq[j], seq[j + 1])] += 1
            if not pairs:
                break
            best = max(pairs, key=pairs.get)
            new_id = self.next_id
            self.next_id += 1
            self.merges[best] = new_id
            self.vocab[new_id] = self.vocab[best[0]] + self.vocab[best[1]]
            chunk_bytes = [apply_merge(seq, best, new_id) for seq in chunk_bytes]

    def add_special_token(self, token_str):
        token_id = self.next_id
        self.next_id += 1
        self.special_handler.add_token(token_str, token_id)
        self.vocab[token_id] = token_str.encode("utf-8")
        return token_id

    def encode(self, text):
        text = self.normalize(text)
        parts = self.special_handler.split_with_specials(text)
        all_ids = []
        for part_text, is_special in parts:
            if is_special:
                all_ids.append(self.special_handler.special_tokens[part_text])
            else:
                for chunk in pre_tokenize(part_text):
                    byte_seq = list(chunk.encode("utf-8"))
                    for pair, new_id in self.merges.items():
                        byte_seq = apply_merge(byte_seq, pair, new_id)
                    all_ids.extend(byte_seq)
        return all_ids

    def decode(self, ids):
        byte_parts = []
        for token_id in ids:
            if token_id in self.vocab:
                byte_parts.append(self.vocab[token_id])
        return b"".join(byte_parts).decode("utf-8", errors="replace")

    def vocab_size(self):
        return len(self.vocab)
```

### Bước 6: Kiểm tra đa ngôn ngữ

Thử nghiệm thực sự là ném tiếng Anh, tiếng Trung, emoji và mã vào nó.

> Thực sự test.                                                                                                                                                                                                                                                             

```python
corpus = (
    "The quick brown fox jumps over the lazy dog. "
    "The quick brown fox runs through the forest. "
    "Machine learning models process natural language. "
    "Deep learning transforms how we build software. "
    "def train(model, data): return model.fit(data) "
    "def predict(model, x): return model(x) "
)

tok = ProductionTokenizer()
tok.train(corpus, num_merges=50)

bos = tok.add_special_token("<|begin|>")
eos = tok.add_special_token("<|end|>")

test_texts = [
    "The quick brown fox.",
    "你好世界",
    "Hello 🌍 World",
    "def foo(x): return x + 1",
    f"<|begin|>Hello<|end|>",
]

for text in test_texts:
    ids = tok.encode(text)
    decoded = tok.decode(ids)
    print(f"Input:   {text}")
    print(f"Tokens:  {len(ids)} ids")
    print(f"Decoded: {decoded}")
    print()
```

Chữ Trung Quốc tạo ra 3 byte mỗi. emoji tạo ra 4 byte. Không một trong số này bị hỏng tokenizer. Không một tạo ra token không rõ. Đó là sức mạnh của BPE cấp bằng byte.

> 中文字符 mỗi tạo ra 3 字节。emoji 产生 4 字节。这些都不会使分词器崩──都不会产生未知代币──这是字节级 BPE 的力量──

> **【中文解读】**Trên đây có mã sẽ kết nối tất cả các thành phần:归一化 → 特殊代币 分割 → 预分词 → BPE 合并 → ID 映射――测试覆盖英文,中文,emoji,代码和特殊代币的混合场景――字节级 BPE đảm bảo bất kỳ nhập khẩu nào sẽ không tạo ra mã thông báo không rõ ràng

> **【拓展：分词速度的工程意义】**纯Python 分词器每秒处理约1M token,Llama 3预训语料有15亿亿 token,使用Python 需要174 天――tiktoken(Rust 实现) 每秒需要100M token,只需1.7 天――这就是为什么生产级分词器都用编译语言:tiktoken用Rust,HuggingFace tokenizers用Rust,SentencePiece用C++──

## Hãy sử dụng nó để thực hiện

### So sánh các token thực sự

Lắp các mã thông báo thực tế từ Llama 3, GPT-4 và Mistral. Xem cách mỗi đoạn xử lý cùng một đoạn văn đa ngôn ngữ.

> 加载 Llama 3、GPT-4 和 Mistral 的实际分词器──看看每个分词器如何处理同一段多语言文本──

```python
import tiktoken

gpt4_enc = tiktoken.get_encoding("cl100k_base")

test_paragraph = "Machine learning is powerful. 机器学习很强大。 L'apprentissage automatique est puissant. 🤖💪"

tokens = gpt4_enc.encode(test_paragraph)
pieces = [gpt4_enc.decode([t]) for t in tokens]
print(f"GPT-4 ({len(tokens)} tokens): {pieces}")
```

```python
from transformers import AutoTokenizer

llama_tok = AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-3-8B")
mistral_tok = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-v0.1")

for name, tok in [("Llama 3", llama_tok), ("Mistral", mistral_tok)]:
    tokens = tok.encode(test_paragraph)
    pieces = tok.convert_ids_to_tokens(tokens)
    print(f"{name} ({len(tokens)} tokens): {pieces[:20]}...")
```

Bạn sẽ thấy số lượng token khác nhau cho cùng một văn bản. Llama 3 với từ vựng 128K là tích cực hơn trong việc hợp nhất các mẫu phổ biến. GPT-4 với 100K nằm ở giữa. Mistral với 32K sản xuất nhiều token hơn nhưng có một lớp nhúng nhỏ hơn.

> Bạn sẽ thấy các mã khác nhau trong cùng văn bản số lượng mã số. Llama 3 có 128K từ biểu biểu trên cùng hợp并常见模式.

Sự thỏa hiệp luôn luôn giống nhau: từ vựng lớn hơn có nghĩa là các chuỗi ngắn hơn nhưng nhiều tham số hơn.

> 权衡 luôn giống nhau: biểu tượng lớn hơn có nghĩa là chuỗi ngắn hơn nhưng nhiều tham số hơn.

## Chuyển nó đi.

Bài học này tạo ra một lời nhắc để xây dựng và debugging token sản xuất.`outputs/prompt-tokenizer-builder.md`- Tôi không biết.

> Bài viết này được phát hành để xây dựng và điều chỉnh các trình độ phân từ của các thiết bị sản xuất.`outputs/prompt-tokenizer-builder.md`

## Tập luyện bài tập

1. **Easy:**Thêm một `get_token_bytes(id)`phương pháp cho thấy các byte nguyên liệu cho bất kỳ ID token. Sử dụng nó để kiểm tra những gì các token hợp nhất của bạn thực sự đại diện.
   Trung ngữ翻译:添加 `get_token_bytes(id)`方法,显示任意 token ID 的原始字节──用它检查您最常用的合并代币──实际代表什么──
2. **Medium:**Thực hiện các pre-tokenizer kiểu Llama chia trên không gian trắng và chữ số nhưng giữ không gian dẫn đầu. So sánh từ vựng của nó với cách tiếp cận GPT-2 regex trên cùng một corpus.
   Trung ngữ翻译:实现 Llama 风格的预分词器,按空格和数字分分但保留前导空格── 在相同语料上比较其词表与GPT-2 正则方法──
3. **Hard:**Thêm một phương pháp mẫu trò chuyện có danh sách `{"role": ..., "content": ...}`và tạo ra chuỗi mã thông báo chính xác cho định dạng trò chuyện Llama 3. kiểm tra nó với thực hiện HuggingFace.
   Trung文翻译:添加聊天模板方法, chấp nhận `{"role": ..., "content": ...}`消息列表并生成 Llama 3 聊天格式的正确代币序列──对照 HuggingFace 实现进行测试──

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|----------------------|---------|
| Byte-level BPE | "Tokenizer that works on bytes" | BPE with a base vocabulary of 256 byte values -- handles any input without unknown tokens | 字节级 BPE，基础词表 256 个字节值 |
| Pre-tokenization | "Splitting before BPE" | Regex or rule-based splitting that prevents BPE from merging across word boundaries | 预分词，防止跨词边界的 token 合并 |
| NFKC normalization | "Unicode cleanup" | Canonical decomposition followed by compatibility composition -- "fi" ligature becomes "fi", fullwidth "A" becomes "A" | NFKC 归一化，统一 Unicode 表示 |
| Chat template | "How messages become tokens" | The exact format for converting a list of role/content messages into a flat token sequence -- model-specific and must match training format | 聊天模板，消息转 token 的格式规则 |
| Special tokens | "Control tokens" | Reserved token IDs that bypass BPE -- [BOS], [EOS], [PAD], chat markers -- matched exactly before merge | 特殊 token，绕过 BPE 的控制标记 |
| Fertility | "Tokens per word" | Ratio of output tokens to input words -- 1.3 for English in GPT-4, 2-3 for Korean, higher means wasted context | 生育率，每词 token 数 |
| tiktoken | "OpenAI tokenizer" | Rust BPE implementation with Python bindings -- 10-100x faster than pure Python | OpenAI 的 Rust 分词器实现 |
| Merge table | "The vocabulary" | Ordered list of byte-pair merges learned during training -- this IS the tokenizer's learned knowledge | 合并表，分词器的核心知识 |

## Xem thêm 延伸阅读

- [OpenAI tiktoken source](https://github.com/openai/tiktoken)-- Thực hiện BPE dung nhựa được sử dụng bởi GPT-3.5/4
- [HuggingFace tokenizers](https://github.com/huggingface/tokenizers)-- Thư viện token hóa Rust hỗ trợ BPE, WordPiece, Unigram
- [Llama 3 paper (Meta, 2024)](https://arxiv.org/abs/2407.21783)-- chi tiết về 128K từ vựng và đào tạo tokeniser
- [SentencePiece (Kudo & Richardson, 2018)](https://arxiv.org/abs/1808.06226)-- token hóa ngôn ngữ-người hiểu biết
- [GPT-2 tokenizer source](https://github.com/openai/gpt-2/blob/master/src/encoder.py)-- bản đồ ban đầu từ byte đến Unicode
