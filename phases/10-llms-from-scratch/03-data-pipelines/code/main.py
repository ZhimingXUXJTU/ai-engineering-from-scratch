"""LLM 预训练数据流水线 —— 从原始文本到训练就绪的 token 序列

核心概念：
  - 数据清洗：去除 HTML 标签、URL、多余空白等噪声
  - 质量过滤：根据文档长度、大写比例、特殊字符比例过滤低质量数据
  - 去重 (MinHash + LSH)：用局部敏感哈希快速检测近似重复文档
  - BPE 分词：将清洗后的文本转换为 token ID 序列
  - 序列打包：将 token 序列切分为固定长度的训练样本，附加 attention mask

AI 对应：
  - GPT-4 的预训练数据经过严格的清洗、去重和质量过滤（CommonCrawl -> FineWeb）
  - Llama 3 使用了超过 15T tokens 的训练数据，去重是节省算力的关键步骤
  - 生产级流水线使用 Apache Beam / Spark 分布式处理 TB 级数据
"""

import re
import hashlib
import random
import time
from collections import Counter, defaultdict


def clean_text(text):
    """清洗文本：去除 HTML 标签、URL、不可打印字符和多余空白"""
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^\x20-\x7E\n]", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r" {2,}", " ", text)
    return text.strip()


def quality_filter(text, min_words=50, max_ratio_caps=0.3, max_ratio_special=0.1):
    """质量过滤器：根据字数、大写比例和特殊字符比例判断文档是否高质量

    GPT-3 论文中使用了类似的启发式过滤，并结合了分类器打分。
    """
    words = text.split()
    if len(words) < min_words:
        return False
    caps_ratio = sum(1 for w in words if w.isupper()) / len(words)
    if caps_ratio > max_ratio_caps:
        return False
    special_chars = sum(1 for c in text if not c.isalnum() and not c.isspace())
    if special_chars / max(len(text), 1) > max_ratio_special:
        return False
    return True


def get_shingles(text, k=5):
    """生成 k-shingle 集合：将文本按滑动窗口切分为 k 个连续词的短语

    两个文档的 shingle 集合越相似，它们的内容越重复。
    """
    words = text.lower().split()
    if len(words) < k:
        return set()
    return {" ".join(words[i:i + k]) for i in range(len(words) - k + 1)}


def minhash_signature(shingles, num_hashes=128):
    """计算 MinHash 签名：将 shingle 集合压缩为固定长度的数值向量

    两个集合的 MinHash 签名在相同位置相等的概率 = Jaccard 相似度。
    这是一种概率近似方法，用于快速估计集合相似性。
    """
    signature = []
    for i in range(num_hashes):
        min_hash = float("inf")
        for shingle in shingles:
            h = int(hashlib.sha256(f"{i}:{shingle}".encode()).hexdigest(), 16)
            min_hash = min(min_hash, h)
        if min_hash == float("inf"):
            min_hash = 0
        signature.append(min_hash)
    return signature


def lsh_buckets(signature, bands=16):
    """局部敏感哈希 (LSH)：将签名分 band，同一 band 哈希到同一桶的文档对为候选重复

    核心思想：将 128 维签名分为 16 个 band（每 band 8 行），
    如果两个文档在任一 band 完全相同，就可能是近似重复。
    """
    rows_per_band = len(signature) // bands
    buckets = []
    for b in range(bands):
        start = b * rows_per_band
        band_data = tuple(signature[start:start + rows_per_band])
        bucket_hash = hashlib.md5(str(band_data).encode()).hexdigest()
        buckets.append((b, bucket_hash))
    return buckets


def deduplicate(documents, threshold=0.8, num_hashes=128, bands=16):
    """MinHash + LSH 去重：快速找到并移除近似重复文档

    流程：(1) 对每个文档计算 MinHash 签名
    (2) 用 LSH 将签名分桶，找到候选重复对
    (3) 对候选对精确计算 Jaccard 相似度，超过阈值则移除
    """
    signatures = []
    shingle_sets = []
    for doc in documents:
        shingles = get_shingles(doc)
        shingle_sets.append(shingles)
        signatures.append(minhash_signature(shingles, num_hashes))

    bucket_map = defaultdict(list)
    for doc_idx, sig in enumerate(signatures):
        for band_id, bucket_hash in lsh_buckets(sig, bands):
            bucket_map[(band_id, bucket_hash)].append(doc_idx)

    duplicate_pairs = set()
    for bucket_docs in bucket_map.values():
        if len(bucket_docs) < 2:
            continue
        for i in range(len(bucket_docs)):
            for j in range(i + 1, len(bucket_docs)):
                duplicate_pairs.add((bucket_docs[i], bucket_docs[j]))

    removed = set()
    for i, j in duplicate_pairs:
        if i in removed or j in removed:
            continue
        s1, s2 = shingle_sets[i], shingle_sets[j]
        if not s1 or not s2:
            continue
        jaccard = len(s1 & s2) / len(s1 | s2)  # Jaccard 相似度 = 交集 / 并集
        if jaccard >= threshold:
            removed.add(j)

    return [doc for idx, doc in enumerate(documents) if idx not in removed], len(removed)


class SimpleTokenizer:
    def __init__(self, vocab_size=256):
        self.vocab = {i: bytes([i]) for i in range(256)}
        self.merges = {}
        self.next_id = 256
        self.eos_id = None
        self.pad_id = 0

    def train_bpe(self, text, num_merges):
        tokens = list(text.encode("utf-8"))
        for i in range(num_merges):
            pairs = Counter()
            for j in range(len(tokens) - 1):
                pairs[(tokens[j], tokens[j + 1])] += 1
            if not pairs:
                break
            best = max(pairs, key=pairs.get)
            new_id = self.next_id
            self.next_id += 1
            self.merges[best] = new_id
            self.vocab[new_id] = self.vocab[best[0]] + self.vocab[best[1]]
            merged = []
            j = 0
            while j < len(tokens):
                if j < len(tokens) - 1 and tokens[j] == best[0] and tokens[j + 1] == best[1]:
                    merged.append(new_id)
                    j += 2
                else:
                    merged.append(tokens[j])
                    j += 1
            tokens = merged

        self.eos_id = self.next_id
        self.vocab[self.eos_id] = b"<EOS>"
        self.next_id += 1

    def encode(self, text):
        tokens = list(text.encode("utf-8"))
        for pair, new_id in self.merges.items():
            merged = []
            j = 0
            while j < len(tokens):
                if j < len(tokens) - 1 and tokens[j] == pair[0] and tokens[j + 1] == pair[1]:
                    merged.append(new_id)
                    j += 2
                else:
                    merged.append(tokens[j])
                    j += 1
            tokens = merged
        return tokens

    def decode(self, ids):
        byte_parts = []
        for token_id in ids:
            if token_id in self.vocab and token_id != self.eos_id:
                byte_parts.append(self.vocab[token_id])
        return b"".join(byte_parts).decode("utf-8", errors="replace")

    def vocab_size(self):
        return len(self.vocab)


def tokenize_corpus(documents, tokenizer):
    all_tokens = []
    for doc in documents:
        tokens = tokenizer.encode(doc)
        all_tokens.extend(tokens)
        all_tokens.append(tokenizer.eos_id)
    return all_tokens


def pack_sequences(token_ids, seq_length, pad_id=0):
    sequences = []
    attention_masks = []
    for i in range(0, len(token_ids), seq_length):
        seq = token_ids[i:i + seq_length]
        mask = [1] * len(seq)
        if len(seq) < seq_length:
            pad_count = seq_length - len(seq)
            seq = seq + [pad_id] * pad_count
            mask = mask + [0] * pad_count
        sequences.append(seq)
        attention_masks.append(mask)
    return sequences, attention_masks


class PreTrainingDataLoader:
    """预训练数据加载器：将序列打包为 batch，支持 shuffle 和 attention mask

    功能类似于 PyTorch 的 DataLoader，但纯 Python 实现。
    每个 batch 包含等长的序列和对应的 attention mask（标记哪些位置是 padding）。
    """

    def __init__(self, sequences, attention_masks, batch_size, shuffle=True):
        self.sequences = sequences
        self.attention_masks = attention_masks
        self.batch_size = batch_size
        self.shuffle = shuffle

    def __len__(self):
        return (len(self.sequences) + self.batch_size - 1) // self.batch_size

    def __iter__(self):
        indices = list(range(len(self.sequences)))
        if self.shuffle:
            random.shuffle(indices)
        for start in range(0, len(indices), self.batch_size):
            batch_idx = indices[start:start + self.batch_size]
            batch_seqs = [self.sequences[i] for i in batch_idx]
            batch_masks = [self.attention_masks[i] for i in batch_idx]
            yield batch_seqs, batch_masks


def compute_statistics(documents, token_ids, sequences, tokenizer_vocab_size):
    total_chars = sum(len(d) for d in documents)
    total_tokens = len(token_ids)
    unique_tokens = len(set(token_ids))
    compression_ratio = total_chars / max(total_tokens, 1)

    doc_lengths = [len(d.split()) for d in documents]
    avg_doc_length = sum(doc_lengths) / max(len(doc_lengths), 1)
    max_doc_length = max(doc_lengths) if doc_lengths else 0
    min_doc_length = min(doc_lengths) if doc_lengths else 0

    token_counts = Counter(token_ids)
    top_tokens = token_counts.most_common(10)

    non_pad_tokens = sum(sum(1 for t in seq if t != 0) for seq in sequences)
    total_positions = sum(len(seq) for seq in sequences)
    utilization = non_pad_tokens / max(total_positions, 1)

    return {
        "total_documents": len(documents),
        "total_characters": total_chars,
        "total_tokens": total_tokens,
        "unique_tokens": unique_tokens,
        "vocab_utilization": unique_tokens / max(tokenizer_vocab_size, 1),
        "compression_ratio": compression_ratio,
        "avg_doc_length_words": avg_doc_length,
        "max_doc_length_words": max_doc_length,
        "min_doc_length_words": min_doc_length,
        "num_sequences": len(sequences),
        "sequence_utilization": utilization,
        "top_10_tokens": top_tokens,
    }


def generate_sample_corpus():
    base_docs = [
        "Machine learning is a subset of artificial intelligence that provides systems the ability "
        "to automatically learn and improve from experience without being explicitly programmed. "
        "Machine learning focuses on the development of computer programs that can access data and "
        "use it to learn for themselves. The process of learning begins with observations or data, "
        "such as examples, direct experience, or instruction, in order to look for patterns in data "
        "and make better decisions in the future based on the examples that we provide.",

        "Deep learning is part of a broader family of machine learning methods based on artificial "
        "neural networks with representation learning. Learning can be supervised, semi-supervised "
        "or unsupervised. Deep learning architectures such as deep neural networks, recurrent neural "
        "networks, convolutional neural networks and transformers have been applied to fields "
        "including natural language processing, speech recognition, computer vision, and many other tasks.",

        "Natural language processing is a subfield of linguistics, computer science, and artificial "
        "intelligence concerned with the interactions between computers and human language, in "
        "particular how to program computers to process and analyze large amounts of natural language "
        "data. The result is a computer capable of understanding the contents of documents, including "
        "the contextual nuances of the language within them.",

        "Transformers are a type of neural network architecture that has become the dominant approach "
        "for natural language processing tasks. The key innovation is the self-attention mechanism, "
        "which allows the model to weigh the importance of different parts of the input when producing "
        "each part of the output. This enables transformers to capture long-range dependencies in text "
        "much more effectively than previous recurrent approaches.",

        "The attention mechanism in neural networks allows the model to focus on relevant parts of "
        "the input sequence when generating each element of the output. In the transformer architecture, "
        "multi-head attention computes attention in parallel across multiple representation subspaces, "
        "enabling the model to jointly attend to information from different representation subspaces "
        "at different positions in the sequence.",

        "Reinforcement learning is an area of machine learning concerned with how intelligent agents "
        "ought to take actions in an environment in order to maximize the notion of cumulative reward. "
        "Reinforcement learning is one of three basic machine learning paradigms, alongside supervised "
        "learning and unsupervised learning. It differs from supervised learning in that correct input "
        "and output pairs need not be presented.",

        "Computer vision is an interdisciplinary scientific field that deals with how computers can "
        "gain high-level understanding from digital images or videos. From the perspective of "
        "engineering, it seeks to understand and automate tasks that the human visual system can do. "
        "Computer vision tasks include methods for acquiring, processing, analyzing and understanding "
        "digital images, and extraction of high-dimensional data from the real world.",

        "Convolutional neural networks are a class of deep learning architecture commonly applied to "
        "analyze visual imagery. They use a variation of multilayer perceptrons designed to require "
        "minimal preprocessing. They are also known as shift invariant or space invariant artificial "
        "neural networks based on their shared-weights architecture and translation invariance "
        "characteristics. Convolutional networks were inspired by biological processes.",

        "Generative adversarial networks consist of two neural networks that contest with each other "
        "in the form of a zero-sum game, where one agent gain is another agent loss. Given a training "
        "set, this technique learns to generate new data with the same statistics as the training set. "
        "For example, a generative adversarial network trained on photographs can generate new "
        "photographs that look authentic to human observers.",

        "Transfer learning is a machine learning method where a model developed for a task is reused "
        "as the starting point for a model on a second task. It is a popular approach in deep learning "
        "where pre-trained models are used as the starting point on computer vision and natural language "
        "processing tasks given the vast compute and time resources required to develop neural network "
        "models on these problems and the large improvements they provide.",
    ]

    near_dup_1 = (
        "Machine learning is a subset of artificial intelligence that provides systems the ability "
        "to automatically learn and improve from experience. Machine learning focuses on developing "
        "computer programs that can access data and use it to learn for themselves. The learning "
        "process begins with observations or data, such as examples or direct experience, in order "
        "to look for patterns and make better decisions based on the examples provided."
    )

    near_dup_2 = (
        "Deep learning is part of a broader family of machine learning methods based on artificial "
        "neural networks with representation learning. Learning can be supervised, semi-supervised "
        "or unsupervised. Deep learning architectures such as deep neural networks, recurrent neural "
        "networks, convolutional neural networks and transformers have been applied to fields "
        "including natural language processing, speech recognition, computer vision, and many other tasks."
    )

    short_doc = "This is too short to be useful."

    html_doc = (
        "<html><body><h1>Title</h1><p>Machine learning is transforming how we build software. "
        "Deep neural networks can learn complex patterns from data. The transformer architecture "
        "has become the dominant approach for language tasks. Self-attention allows models to capture "
        "long-range dependencies. Pre-training on large corpora produces strong foundation models. "
        "Fine-tuning adapts these models to specific tasks with minimal additional data.</p></body></html>"
    )

    spam_doc = "BUY NOW CLICK HERE FREE MONEY GUARANTEED RESULTS " * 20

    docs = base_docs + [near_dup_1, near_dup_2, short_doc, html_doc, spam_doc]
    return docs


def run_pipeline():
    print("=" * 60)
    print("Data Pipeline for Pre-Training")
    print("=" * 60)

    raw_docs = generate_sample_corpus()
    print(f"\nRaw documents: {len(raw_docs)}")

    print("\n--- Stage 1: Cleaning ---")
    cleaned_docs = [clean_text(doc) for doc in raw_docs]
    print(f"After HTML stripping: {len(cleaned_docs)} documents")

    print("\n--- Stage 2: Quality Filtering ---")
    filtered_docs = [doc for doc in cleaned_docs if quality_filter(doc)]
    removed_quality = len(cleaned_docs) - len(filtered_docs)
    print(f"Removed {removed_quality} low-quality documents")
    print(f"Remaining: {len(filtered_docs)} documents")

    print("\n--- Stage 3: Deduplication (MinHash + LSH) ---")
    start = time.time()
    deduped_docs, num_removed = deduplicate(filtered_docs, threshold=0.8)
    dedup_time = time.time() - start
    print(f"Removed {num_removed} near-duplicates in {dedup_time:.2f}s")
    print(f"Remaining: {len(deduped_docs)} documents")

    print("\n--- Stage 4: Tokenization ---")
    all_text = " ".join(deduped_docs)
    tokenizer = SimpleTokenizer()
    start = time.time()
    tokenizer.train_bpe(all_text, num_merges=100)
    train_time = time.time() - start
    print(f"Trained tokenizer with {tokenizer.vocab_size()} tokens in {train_time:.2f}s")

    start = time.time()
    token_ids = tokenize_corpus(deduped_docs, tokenizer)
    tok_time = time.time() - start
    print(f"Tokenized {len(token_ids):,} tokens in {tok_time:.2f}s ({len(token_ids)/max(tok_time, 0.001):,.0f} tokens/sec)")

    print("\n--- Stage 5: Sequence Packing ---")
    seq_length = 128
    sequences, masks = pack_sequences(token_ids, seq_length, pad_id=0)
    print(f"Packed into {len(sequences)} sequences of length {seq_length}")

    print("\n--- Stage 6: DataLoader ---")
    batch_size = 4
    loader = PreTrainingDataLoader(sequences, masks, batch_size)
    print(f"DataLoader: {len(loader)} batches of size {batch_size}")

    batch_count = 0
    total_tokens_served = 0
    for batch_seqs, batch_masks in loader:
        batch_count += 1
        total_tokens_served += sum(sum(m) for m in batch_masks)
        if batch_count <= 2:
            print(f"\n  Batch {batch_count}:")
            print(f"    Sequences: {len(batch_seqs)}")
            print(f"    First seq (first 20 tokens): {batch_seqs[0][:20]}...")
            print(f"    First mask (first 20): {batch_masks[0][:20]}...")
    print(f"\n  Total batches served: {batch_count}")
    print(f"  Total non-padding tokens served: {total_tokens_served:,}")

    print("\n--- Dataset Statistics ---")
    stats = compute_statistics(deduped_docs, token_ids, sequences, tokenizer.vocab_size())
    print(f"  Documents:          {stats['total_documents']}")
    print(f"  Total characters:   {stats['total_characters']:,}")
    print(f"  Total tokens:       {stats['total_tokens']:,}")
    print(f"  Unique tokens:      {stats['unique_tokens']}")
    print(f"  Vocab utilization:  {stats['vocab_utilization']:.1%}")
    print(f"  Compression ratio:  {stats['compression_ratio']:.2f} chars/token")
    print(f"  Avg doc length:     {stats['avg_doc_length_words']:.0f} words")
    print(f"  Num sequences:      {stats['num_sequences']}")
    print(f"  Seq utilization:    {stats['sequence_utilization']:.1%}")

    print("\n--- Pipeline Summary ---")
    print(f"  Raw documents:       {len(raw_docs)}")
    print(f"  After cleaning:      {len(cleaned_docs)}")
    print(f"  After quality filter: {len(filtered_docs)} (-{removed_quality})")
    print(f"  After dedup:         {len(deduped_docs)} (-{num_removed})")
    print(f"  Final tokens:        {len(token_ids):,}")
    print(f"  Training sequences:  {len(sequences)}")
    print(f"  Training batches:    {len(loader)}")


if __name__ == "__main__":
    run_pipeline()
