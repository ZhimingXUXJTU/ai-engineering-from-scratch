# 从零构建分词器

> 第1课给你玩具,这课给你武器.

> **【中文解读】**第一个课程的BPE 是玩具,本课构建生产级分词器:处理Unicode、空白归归一化、特殊代币、字节级回退(让任何输入都能编码,包括emoji 和中文) ⋅

> **【拓展：tiktoken/HuggingFace】**了解它们的内部原理有助于优化快速工程和成本控制.

>  **【前置】**学本节前请先掌握:(1) 阶段10·01(Tokenizers:BPE/WordPiece/SentencePiece) 理解BPE 合并循环和合并表的概念;(2) 联合编码与 UTF-8 编码码点、字节、NFC/NFKC 归一化的区别;(3) 正则表达式特别是`\p{L}`,我知道.`\p{N}`负向先行断言`(?!\S)`鱼`regex`库(不是标准`re`因为`re`不支持 Unicode 属性) 』

**Type:** Build
**Languages:** Python
**Prerequisites:** Phase 10, Lesson 01 (Tokenizers: BPE, WordPiece, SentencePiece)
**Time:** ~90 minutes

## 学习目标

- 建立一个处理 Unicode,白色空间规范化和特殊代币的生产级 BPE 代币器
  构建处理 统计编码、空白归结和特殊代币的生产级 BPE 分词器
- 实现字节级下降,以便代币器可以在未知的代币的情况下编码任何输入 (包括emoji,CJK和代码)
  实现字节级回退,使分词器能编码任何输入 (包括emoji、CJK、代码) 而不产生未知的代码
- 在应用BPE合并之前添加预代币化regex模式,将文字分为词界限
  添加预分词正则模式,在 BPE 合并前按词边界分文本
- 训练一个定制代码符号在一个体积上,并评估其压缩比与多语言文本上的代码符号
  在语料上训练自定义分词器,并在多语言文本上评估其与TikTok的压缩比率

> **【中文解读】**本课目的是将第一课的玩具BPE 升级为生产级分词器――关键改进包括:Unicode 归一化(NFKC) 、预分词正则(防止跨词边界的合并) 、字节级回退(零未知代币)、特殊代币 管理(BOS/EOS/聊天模板标记器) ――这些是让分词处理"整个互联网"的必备机制――

## 问题 问题引入

你从01课的BPE标记器使用英语文,现在把日本文写在上面,或者是爱默契,或者是Python代码,

> 你第一课的BPE 分词器能处理英文文本.现在给它日文.或者是爱默生.

它会破裂.

> 它会崩.

不是因为BPE是错误的,因为实现是不完整的.一个生产代币器处理任何编码中的原始字节,在分化之前将Unicode正常化,管理永远不会合并的特殊代币,

> 不是因为BPE有问题,而是因为实现不完整.生产级分词器处理任何编码的原始字节,在分类前归化Unicode,管理永不参与合并的特殊代币,串联预分词与子词分类,并且所有操作都足够快,不会成为处理15亿代币的训练管线的瓶.

现在,我们可以看到一个新的代码. 拉马3号有128,256. GPT-4有大约10万个. 这些不是玩具号码. 这些词汇背后的结合表是用数百个千兆字节的文字训练的, 周围的机器 - - 正常化,预代币化,特殊代币注射,聊天模板格式化 - - 是区分一个处理"你好世界"的代币器与一个处理整个互联网的代币器的东西.

> 格普特-2分词器有50,257个代币. 格普特-3有128,256个. 格普特-4大约有10万个. 这些不是玩具数字. 这些词表背后的合并表在数百GB文本上训练,而周围的机制归结,预分词,特殊代币注入,聊天模板格式化正是区分能处理"你好世界"和能够处理整个互联网分词器的关键.

你将建造那种机器.

> 你会构建那套机制.

> **【中文解读】**生产级分词器不是单一算法,而是一个五阶段管线:归一化 → 预分词 → BPE 合并 → 特殊代币注入 → ID 映射――每个阶段解决不同的问题――例如NFKC 归一化把"fi"连字(U+FB01) 变成"fi" 两个字符,预分词防止"猫"被合并出"e c" 这样的代币――

>  **【类比】**生产级分词器像"邮局的信件处理流水线":归一化是"统一邮编格式"(U+FB01 "fi" → "fi",全角字母 → 半角),预分词是"按目的先分堆"(按词边界、数字、标点切,避免跨城市混装),BPE 合并是"高频包裹自动拼箱"(常见词直接整箱),特殊代币是"挂号信标签"(BOS/EOS/PAD 最后永远不参与拼箱),才是"贴条形码" ((ID 映射) ⋅任何套件都漏掉,邮件就乱乱了──

> **【拓展：Llama 3 的分词器升级】**Meta 在 Llama 3 中将词表从32K (Llama 2 的句子) 升级到128K (tiktoken风格字节级 BPE),专门增加非英语文字的代币分配.

## 概念的核心概念

### 整个管道

生产代币不是一个算法,而是五个阶段的管道,每个阶段都解决了不同的问题.

> 生产阶级分词器不是单一算法. 它是一个五阶段的管线,每个阶段解决不同的问题.

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

每个阶段都有一个特定的工作:

> 每个阶段都有特定的职责:

| Stage | What It Does | Why It Matters |
|-------|-------------|----------------|
| Normalize | NFKC Unicode, lowercase optional, strip accents optional | "fi" ligature (U+FB01) becomes "fi" (two chars). Without this, same word gets different tokens. |
| Pre-Tokenize | Split text into chunks before BPE | Prevents BPE from merging across word boundaries. "the cat" should never produce a token "e c". |
| BPE Merge | Apply learned merge rules to byte sequences | The core compression. Turns raw bytes into subword tokens. |
| Special Tokens | Inject [BOS], [EOS], [PAD], chat template markers | These tokens have fixed IDs. They never participate in BPE merges. The model needs them for structure. |
| ID Mapping | Convert token strings to integer IDs | The model sees integers, not strings. |

### 字节级BPE

课01的代币器运行在UTF-8字节.这是一个正确的呼叫.但我们错过了一些重要的事情:当这些字节不有效的UTF-8时会发生什么?

> 首先,我们在 UTF-8 字节上操作.这是一个正确的选择.

字节级BPE通过将每一个可能的字节值 (0-255) 作为一个有效的代币来解决这个问题.你的基础词汇库是正确的 256 个条目.任何文件 - 文字,二进制,损坏 - 可以在没有产生未知的代币的情况下代币化.

> 字节级 BPE 通过将每个可能的字节值 ((0-255) 视为有效代币来解决这个问题――你的基础词表恰好 256条条点――任何文件文本、二进制、损坏的都可以被分词而不会产生未知的代币――

GPT-2 增加了一个技巧:将每个字节映射到可打印的 Unicode 字符,使词汇保持于人能读取的.字节0x20 (空间) 成为它们的映射中的字符"G".这纯粹是化品.算法不关心.

> 字节2加了一个花招:将每个字节映射到一个可打印的Unicode字符,使词表保持可读性.字节0x20(空格) 在他们的映射中变成字符"G"――这纯粹是装饰性的――算法不关心这个――

实际实力:字节级BPE处理地球上的每一种语言.中国字符每字母是3 UTF-8字节.日本字母可以是3-8字节.阿拉伯语,德瓦纳加里,爱莫吉语 - - 所有这些都是字节序列.BPE算法在这些字节序列中找到模式,就像它在英语ASCII字节中找到模式一样.

> 真正的力量:字节级BPE 处理地球上的每种语言──中文字符每个占有3个 UTF-8字节──日文占有3个字节──阿拉伯文、天城文、情感都只是字节序列──BPE 算法在这些字节序列中寻找模式的方式与英文ASCII 字节中完全一样──

> **【中文解读】**字符级 BPE 的核心优势:基础词表恰好 256 个字符值,任何输入都能编码.GPT-2 还做了一个"花招"把每个字符映射到一个可打印的 Unicode 字符,让词表更容易阅读. 中文字符在 UTF-8 中占 3 字符,日文占 3-4 字节,emoji占 4 字节BPE 算法在所有这些字节序列上完全相同的方式工作.

### 预托克化

在BPE触及你的文本之前,你需要将它分成块. 这阻止了合并算法创建跨越词界限的代币.

> 在BPE处理你的文本之前,你需要把它分成块.

通过使用regex模式来分开文本:

>  GPT-2 使用正规表达式来分开文本:

```
'(?:[sdmt]|ll|ve|re)| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+
```

这种模式分为缩写 ("don't"变成"don" + "'t"),有可选的领先空间,数字,分点和白色空间的单词.领先空间被附加到单词 - - 因此"猫"变成 ["the", "cat"],而不是 ["the", "", "cat"].

> 这个模式按缩写拆分("don't" 变成"don" + "'t")、带可选前导空格的词、数字、标点和空格。前导空格保持在词上所以"猫" 变成 ["the", "cat"],而不是 ["the", "cat"]。

拉马使用SentencePiece,它完全跳过regex.它将原始字节流作为一个长序列,并让BPE算法弄清楚边界.这更简单,但给BPE更多的自由创建交叉字符.

> 拉马使用SentencePiece,完全跳过正则表达式──它将原始字节流视为长序列,让BPE 算法自动确定边界──这更简单,但给BPE 更多创建跨词代币的自由──

选择是重要的.GPT-2的regex阻止令牌商学习一个词的结尾和下一个词的开始应该合并.SentencePiece允许,这有时会产生更有效的压缩,但更不易解释的令牌.

> 这个选择很重要――GPT-2的正规规规则防止分词器学习一个词的最后的"the" 和下一个词的开头的"the"合并――SentencePiece允许这样做,有时产生更高效的压缩,但不太解释的符号――

### 特殊的代币

每个生产代币商都保留了结构标记的代币ID:

> 每个生产级分词器都为结构标记保留代币ID:

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

特殊代币从来没有被BPE分开.它们在合并算法运行之前就匹配,用固定ID取代,周围的文本通常被代币化.

> 特殊代币永远不会被BPE拆分.它们在合并算法运行之前被精确匹配,替换为固定ID,周围文本正常分词.

> **【中文解读】**特殊标志是分词器中"不可触摸"的保留标志:`[BOS]`开始的序列`[EOS]`没有任何其他方法.`[PAD]`它们有固定的ID,永远不参与BPE合并,而在合并之前通过精确匹配被提取出来.`<|start_header_id|>`,我知道.`<|end_header_id|>`,我知道.`<|eot_id|>`标记对话结构,聊天GPT 使用 `<|im_start|>`和 `<|im_end|>`,我知道.

> **【拓展：聊天模板的工程陷阱】**聊天模板是实际部署中最容易出错的地方. 每个模型在训练中使用特定格式的特殊代币,任何偏差缺少换行、多个空格、代币 顺序错误都会让输入偏离训练分布,导致模型输出垃圾.`chat_template`为了标准化这个过程.

> ️ **【易错点】**实现特殊标志的三个陷:**特殊 token 内含正则元字符**如 `<|im_start|>`中中 `|`必须使用`re.escape()`转义,否则在 GPT-2 预分词的正则上会被解析为选择符;(2) **未从 BPE 词表中排除特殊 token**若`<|im_end|>`不在被拆除前,它的字符序列被BPE拆成8个标志,模型永远看不到完整结构标记;**`add_special_tokens=False` 漏配**调用`tokenizer.encode(text)`默认会自动加BOS/EOS,做拼接时会出现BOS BOS EOS EOS 序列,破坏注意力面具对齐──修复:编码时显式传 `add_special_tokens=False`现在,我们必须做一个.

### 聊天模板

这就是大多数人感到困惑的地方,

> 这也是大多数人困惑的地方,

当你发送消息给聊天模型时,API接受一个消息列表:

> 当你发送消息时,API 接受一个消息列表:

```
[
  {"role": "system", "content": "You are helpful."},
  {"role": "user", "content": "Hello"},
  {"role": "assistant", "content": "Hi there!"}
]
```

模型不看到JSON. 它看到一个平坦的代币序列.聊天模板将消息转换成那个平坦的序列使用特殊的代币.每个模型都会以不同的方式进行:

> 模型看不到JSON──它看到的是一个平的代币序列──聊天模板使用特殊的代币将消息转换为平的序列──每个模型的做法不同:

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

错误的模板,模型产生垃圾.它是训练在一个准确的格式.任何偏差 - - 缺失的新线,交换的代币,额外的空间 - - 将输入置于训练分布之外.

> 模板搞错了模型就会产生垃圾输出――它是在精确的形式上训练的――任何偏差缺少换行、交换代币、多一个空格都会使输入偏离训练分布――

>  **【困惑】**问:Llama 3 为什么放弃SentencePiece 改用TikTok?字节级BPE比原版强在哪?A: 两点关键优势:(1) **SentencePiece 用 ⊗（U+2581）代替空格**对于 ASCII 字符和原始空格的混在聊天场景下导致代币序列对快速微小变化过于敏感; 代币直接保留前导空格,"你好"和"你好"是不同的代币,更稳定;**字节级 BPE 词表恰好 256 个基础 token**理论上可以编码任何字节序列 (包括情感符号,私有区字符),不依赖具体语料;SentencePiece 词表若未训练到某个字符直接 [UNK]。Llama 3 词表从32K 扩大到128K,多语言压缩比升升 ~2x,这是为推理成本买单的工程决策──

### 速度

对于生产代码化来说,Python太慢了.

> 字符串的生产速度太慢了.

接脸标记器也叫做Rust.SentencePiece是C++.这些标记器可以实现10-100倍的速度.

> 面标记也就是面标记也就是面标记,SentencePiece是C++──这些比纯Python快10-100倍──

为了展望:在每秒100万代币 (Rust) 时,需要174天,在每秒15万代币 (Rust) 时,需要1.7天.

> 举例:以每秒100万代币的速度为Llama 3 预训分词需要15亿代币需要174天――以每秒100亿代币的速度,只需要1.7天――

在制作中,你会使用编译的实现,只触摸Python包装.

> 在生产中,你会使用编译实现,只接触到Python包装器.

## 建立它,实现它.
```figure
weight-tying
```

## 建立它

### 步骤1:字节级编码

转换任何字符串为字节序列,将每个字节映射到可打印的字符中,然后逆转过程.

> 基础──将任何字符串转换为字节序列,将每个字节映射到可打印字符用于显示,并反转该过程──

```python
def bytes_to_tokens(text):
    return list(text.encode("utf-8"))

def tokens_to_text(token_bytes):
    return bytes(token_bytes).decode("utf-8", errors="replace")
```

测试多语言文本,以查看字节数量:

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

"hello"是5字节. "你好"是6字节 (3个字符).火焰的爱默契是4字节.字节级代币符号不关心它是什么语言.字节是字节.

> "你好"是5字节──"你好"是6字节──每字符3字节──火焰的爱情符号是4字节──字节级分词器不关心它是什么语言──字节就是字节──

### 步骤2:使用 Regex 的预托克尼化器

通过GPT-2regex模式将文本分成块,每个部分由BPE独立地代码化.

> 使用GPT-2 正则模式将文本分成块.

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

其他`regex`模块支持 Unicode 属性逃逸 (`\p{L}`对于信件,`\p{N}`标准图书馆`re`对于生产多语言代币器,安装 `regex`现在,我们要去.

> `regex`模块支持 Unicode 属性转义(`\p{L}`表示字母,`\p{N}`表示数字) 』标准库 `re`模块不支持,所以我们回到了ASCII字符类.`regex`,我知道.

试试吧.

```python
print(pre_tokenize("Hello, world! Don't stop."))
# [' Hello', ',', ' world', '!', " Don", "'t", ' stop', '.']
```

位将保持与词的连接.缩写在位分开.点击成为自己的部分.BPE永远不会将代币融合在这些边界.

> 前导空格保持在词上. 缩写在撇号处分开. 标点成为独立块.

### 步骤3: 字节序列上的 BPE

核心算法从课01中,但现在在预先代币的块上独立运行.

> 现在独立地对预分词的块进行操作.

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

### 步骤4:特殊的标志处理

特殊的代币需要精确的匹配和固定的身份证.

> 特殊的代币需要精确匹配和固定的ID.

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

### 步骤5: 完整的标记器类

链接所有东西:正常化,分成特殊代币,预代币化,BPE合并,地图到身份证.

> 将所有步骤串联:归一化,按特殊标志 分割,预分词,BPE 合并,映射到ID──

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

### 六步:多语言测试

试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试试

> 现在,我已经开始做了一些事情.

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

汉字每字产生3字节. 情感符号产生4字节. 没有一个字符打破代币器. 没有一个字符产生未知的代币. 这就是字节级BPE的功率.

> 中文字符每个产生3字节. 情感符产生4字节. 这些都不会使分词器崩.

> **【中文解读】**以上代码将所有组件串联起来:归结 → 特殊代币 分割 → 预分词 → BPE 合并 → ID 映射――测试覆盖英文,中文,情感符号和特殊代币的混合场景――字节级 BPE保证任何输入都不会产生未知的代币这就是它成为工业标准的根本原因――

> **【拓展：分词速度的工程意义】**纯Python 分词器每秒处理约1M代币,Llama 3的预训语料有15亿代币,使用Python 需要174天――tiktoken(Rust 实现) 每秒需要1.7天――这就是为什么生产级分词器都用编译语言:tiktoken 用Rust,HuggingFace代币器用Rust,SentencePiece 用C++――

## 用它实现框架

### 实际的代币交易者

查看各个语言段落的处理方式.

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

您将看到相同文本的代币数量不同. 128K 词汇的 Llama 3 在合并常见模式方面更具侵略性. 100K 的 GPT-4 在中间. 32K 的 Mistral 生产更多代币,但具有较小的嵌入层.

> 你会看到相同文本的不同代币数量――Llama 3 的 128K 词表在合并常见模式上更积极――GPT-4 的 100K 在中间――Mistral 的 32K 产生更多代币,但嵌层更小――

交易总是相同的:更大的词汇意味着更短的序列,但更多的参数.

> 权衡始终相同:更大的词表意味着更短的序列,但更多的参数.

## 运送它.

这一课产生的提示是建立和调试生产代币.`outputs/prompt-tokenizer-builder.md`现在,我们要去.

> 本课产出于构建和调试生产级分词器的提示.`outputs/prompt-tokenizer-builder.md`,我知道.

## 练习题

1. **Easy:**添加一个`get_token_bytes(id)`使用它检查您最常见的合并代币实际上代表什么.
   中文翻译:添加 `get_token_bytes(id)`方法,显示任意代币ID的原始字节──用它检查您最常用的合并代币──实际代表什么──
2. **Medium:**实现Llama式预代币器,它分为白色空间和数字,但保持领先空间. 比较其词汇与GPT-2regex方法在同一体.
   中文翻译:实现拉马风格的预分词器,按空格和数字分分,但保留前导空格──在相同语料上比较其词表与GPT-2 正则方法──
3. **Hard:**添加一个聊天模板方法,包含列表`{"role": ..., "content": ...}`通过"HuggingFace"实现,测试它.
   中文翻译:添加聊天模板方法,接受 `{"role": ..., "content": ...}`消息列表并生成 Llama 3 聊天格式的正确代币序列──对照 HuggingFace 实现进行测试──

## 关键词 快速查找表

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

## 继续阅读 继续阅读

- [OpenAI tiktoken source](https://github.com/openai/tiktoken)-- GPT-3.5/4 所使用的性BPE实现
- [HuggingFace tokenizers](https://github.com/huggingface/tokenizers)-- 支持BPE,WordPiece,Unigram的结代币库
- [Llama 3 paper (Meta, 2024)](https://arxiv.org/abs/2407.21783)-- 128K词汇和代币化培训的详细信息
- [SentencePiece (Kudo & Richardson, 2018)](https://arxiv.org/abs/1808.06226)--语言认知标记
- [GPT-2 tokenizer source](https://github.com/openai/gpt-2/blob/master/src/encoder.py)-- 原始的字节到Unicode映射
