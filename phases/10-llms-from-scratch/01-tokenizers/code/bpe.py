"""BPE (Byte Pair Encoding) 分词器 —— 大语言模型文本处理的第一步

核心概念：
  - BPE 是一种数据压缩算法：反复找到文本中出现频率最高的字节对，合并为新 token
  - 训练过程：从 256 个基础字节开始，每次合并最高频的相邻 token 对，扩展词表
  - 编码过程：将文本转为字节序列，按训练时学到的合并规则逐步替换
  - 解码过程：将 token ID 映射回字节序列，再还原为 UTF-8 字符串

AI 对应：
  - GPT-4 使用 cl100k_base 分词器（词表大小 ~100K），tiktoken 库就是 BPE 的高效 C 实现
  - Llama 3 使用基于 SentencePiece 的 BPE 分词器（词表大小 128K）
  - 分词器直接决定模型的上下文利用率：好的分词器能用更少的 token 表示相同内容
"""

from collections import Counter


class BPETokenizer:
    """BPE 分词器：通过迭代合并高频字节对来构建子词词表

    训练时学习合并规则（哪些字节对最值得合并），编码时应用这些规则。
    这就是 GPT 系列模型分词器的核心思想。
    """

    def __init__(self):
        self.merges = {}  # 合并规则：(token_a, token_b) -> new_token_id
        self.vocab = {}   # 词表：token_id -> 对应的字节序列

    def _get_pairs(self, tokens):
        """统计 token 序列中所有相邻 token 对的出现频率"""
        pairs = Counter()
        for i in range(len(tokens) - 1):
            pairs[(tokens[i], tokens[i + 1])] += 1
        return pairs

    def _merge_pair(self, tokens, pair, new_token):
        """将 token 序列中所有匹配的 pair 替换为 new_token"""
        merged = []
        i = 0
        while i < len(tokens):
            if i < len(tokens) - 1 and tokens[i] == pair[0] and tokens[i + 1] == pair[1]:
                merged.append(new_token)  # 找到匹配对，替换为新 token
                i += 2
            else:
                merged.append(tokens[i])
                i += 1
        return merged

    def train(self, text, num_merges):
        """训练 BPE 分词器：从 UTF-8 字节开始，迭代合并最高频的 token 对

        每次合并都会：(1) 找到出现最频繁的相邻 token 对
        (2) 给它分配一个新的 token ID（从 256 开始，因为 0-255 是基础字节）
        (3) 在整个序列中替换这个 token 对
        """
        tokens = list(text.encode("utf-8"))  # 将文本转为 UTF-8 字节序列作为初始 token
        self.vocab = {i: bytes([i]) for i in range(256)}  # 初始词表：256 个基础字节

        for i in range(num_merges):
            pairs = self._get_pairs(tokens)
            if not pairs:
                break
            best_pair = max(pairs, key=pairs.get)  # 找到出现频率最高的相邻 token 对
            new_token = 256 + i  # 新 token ID 从 256 开始递增
            tokens = self._merge_pair(tokens, best_pair, new_token)  # 在序列中执行合并
            self.merges[best_pair] = new_token  # 记录合并规则
            self.vocab[new_token] = self.vocab[best_pair[0]] + self.vocab[best_pair[1]]  # 新 token 的字节表示 = 两个子 token 拼接
            merged_str = self.vocab[new_token]
            print(f"Merge {i + 1}: {best_pair} -> {new_token} = {merged_str}")

        return self

    def encode(self, text):
        """将文本编码为 token ID 序列：先转字节，再按训练学到的合并规则逐步替换"""
        tokens = list(text.encode("utf-8"))
        for pair, new_token in self.merges.items():
            tokens = self._merge_pair(tokens, pair, new_token)
        return tokens

    def decode(self, tokens):
        """将 token ID 序列解码回文本：每个 token 映射到字节，拼接后解码为 UTF-8"""
        byte_sequence = b"".join(self.vocab[t] for t in tokens)
        return byte_sequence.decode("utf-8", errors="replace")

    def vocab_size(self):
        return len(self.vocab)

    def get_token_str(self, token_id):
        return self.vocab.get(token_id, b"<?>")


def demo_bpe():
    """演示 BPE 分词器的训练和编码/解码过程

    【拓展】在真实系统中，tiktoken 库用 C 实现了 BPE 算法，速度比纯 Python 快 10-100 倍。
    GPT-4 的 cl100k_base 分词器训练了约 100K 个合并规则，能高效处理多语言文本和代码。
    """
    corpus = (
        "The cat sat on the mat. The cat ate the rat. "
        "The dog sat on the log. The dog ate the frog. "
        "Natural language processing is the study of how computers "
        "understand and generate human language."
    )

    print("=" * 60)
    print("Training BPE tokenizer")
    print("=" * 60)

    tokenizer = BPETokenizer()
    tokenizer.train(corpus, num_merges=30)

    print(f"\nVocabulary size: {tokenizer.vocab_size()}")

    test_sentences = [
        "The cat sat on the mat.",
        "The frog sat on the log.",
        "language processing",
        "unhappiness",
    ]

    print("\n" + "=" * 60)
    print("Encoding test sentences")
    print("=" * 60)

    for sentence in test_sentences:
        encoded = tokenizer.encode(sentence)
        decoded = tokenizer.decode(encoded)
        raw_bytes = len(sentence.encode("utf-8"))
        print(f"\nOriginal:  {sentence}")
        print(f"Encoded:   {encoded}")
        print(f"Decoded:   {decoded}")
        print(f"Tokens:    {len(encoded)} (from {raw_bytes} bytes)")
        print(f"Ratio:     {len(encoded) / raw_bytes:.2f}")


def demo_tiktoken():
    """与 OpenAI 的 tiktoken 库对比，展示真实生产级分词器的效果"""
    try:
        import tiktoken
    except ImportError:
        print("\ntiktoken not installed. Run: pip install tiktoken")
        return

    print("\n" + "=" * 60)
    print("Comparing with tiktoken (GPT-4 tokenizer)")
    print("=" * 60)

    enc = tiktoken.get_encoding("cl100k_base")

    test_texts = [
        "The cat sat on the mat.",
        "unhappiness",
        "Hello, world!",
        "def fibonacci(n):",
        "3.14159265358979",
    ]

    for text in test_texts:
        tokens = enc.encode(text)
        decoded_pieces = [enc.decode([t]) for t in tokens]
        print(f"\n'{text}'")
        print(f"  Tokens:  {decoded_pieces}")
        print(f"  IDs:     {tokens}")
        print(f"  Count:   {len(tokens)}")


if __name__ == "__main__":
    demo_bpe()
    demo_tiktoken()
