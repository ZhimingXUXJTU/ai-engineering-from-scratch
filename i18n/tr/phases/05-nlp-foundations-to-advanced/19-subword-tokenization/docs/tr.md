# Alt kelime işaretleme  BPE, WordPiece, Unigram, SentencePiece  子词分词  BPE、WordPiece、SentencePiece

> Sözcüğü işaretleyenler görünmeyen kelimelerle boğulur. Karakter işaretleyicileri dizilerin uzunluğunu patlatır. Alt kelime işaretleyicileri farkı bölür. Her modern LLM bir teker gemiler.
> 词级分词器在未见词上卡住──字符分词器爆炸序列长度──子词分词器取中值──每个现代 LLM 都用子词分词──

> **【中文解读】**BPE GPT'nin kullanıldığı分词算法, WordPiece'nin kullanıldığı BERT'dir.

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 01 (Text Processing), Phase 5 · 04 (GloVe / FastText / Subword) | **前置知识:** Phase 5 · 01（文本处理），Phase 5 · 04（GloVe / FastText / 子词）
**Time:** ~60 minutes | **时间:** ~60 分钟

## Sorunlar. Sorunlar.

Sözcükte 50.000 kelime var. Kullanıcı "içerçilemez" yazıyor. Tokenizer geri dönüyor.`[UNK]`Daha da kötüsü, korpusunuzdaki %90'lu belge 40 nadir kelimeyi içerir. Bu da her belgeye 40 bit kaybedilen bilgi anlamına gelir.

> Suçlu Sözcükler: %100. %100. %100. %100. %100. %100. %100. %100. %100. %100. %100. %100. %100. %100. %100. %100. %100. %100. %100. %100. %100. %100. %100. %100. %100. %100. %100. %100. %100. %100. %100. %100. %100. %100. %100. %100. %100. %100. %100. %100. %100. %100. %100. %100. %100. %100. %100. %100. %100. %100. %100. %100. %100. %100. %100. %100. %100. %100. %100. %100. %100. %100. %100. %100. %100. %100. %100. %100. %100. %100. %100. %100. %100. %100. %100. %100. %100. %100. %100. %100. %100. %100%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%`[UNK]`◊ Model şimdi bu kelime için sinyal yok. Daha da kötüsü:语料中第90百分位文档中第90百分位文档中有40稀见词, yani her bir文档 kayboluyor 40位信息──

> **【中文解读】**Bu bölümde sorulan soru şu: Bu tekniği pratik projede nasıl doğru bir şekilde anlayabilir ve uygulayabilirsiniz.

Alt kelime işaretleme bunu çözür. Ortak kelimeler tek işaret olarak kalır. Nadir kelimeler anlamlı parçalara parçalanır:`untokenizable`→ `un`- Evet .`token`- Evet .`izable`Eğitim verileri her şeyi kapsar çünkü her bir dizilenin sonunda bir bayt dizisi vardır.

> 子词分词解决了这个问题──常见词保持单个标志──罕见词分解为有意的片段:`untokenizable`→ `un`- Evet.`token`- Evet.`izable`❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖

2026'da her sınır LLM üç algoritmadan (BPE, Unigram, WordPiece) birine gönderilmektedir.

> 2026 yılının her önde kalan LLM ⇒ BPE ∞ Unigram ∞ WordPiece ∞ üç algoritma ∞ BPE ∞ Unigram ∞ WordPiece ∞ BPE ∞ BPE ∞ BPE ∞ BPE ∞ BPE ∞ BPE ∞ BPE ∞ BPE ∞ BPE ∞ BPE ∞ BPE ∞ BPE ∞ BPE ∞ BPE ∞ BPE ∞ BPE ∞ BPE ∞ BPE ∞ BPE ∞ BPE ∞ BTE ∞ BTE ∞ BTE ∞ BTE ∞ B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B B

## Konsepten bir şey.

> **【中文解读】**Bu bölümde temel kavramlar ve teoriler hakkında konuşuluyor. Bu kavramları öğrenmek, sonradan gerçekleştirilme önemi, aynı zamanda, görüşmeler ve mühendislik uygulamalarında yüksek sıklıkta yapılan incelemelerin bilgi noktasıdır.

![BPE vs Unigram vs WordPiece, character-by-character](../assets/subword-tokenization.svg)

**BPE (Byte-Pair Encoding).**Karakter seviyesindeki kelime birikimi ile başlayın. Her yanlışı çift sayın. En sık gelen çiftleri yeni bir jetonla birleştirin. Hedef kelime birikimi boyutuna ulaşana kadar tekrarlayın.

> **BPE（字节对编码）。**Bir de, bir de, bir de, bir de, bir de, bir de, bir de, bir de, bir de, bir de, bir de, bir de, bir de, bir de, bir de, bir de, bir de, bir de, bir de, bir de, bir de, bir de, bir de, bir de, bir de, bir de, bir de, bir de, bir de, bir de, bir de, bir de, bir de, bir de, bir de, bir de, bir de, bir de, bir de, bir de, bir de, bir de, bir de, bir de, bir de, bir de, bir de, bir de, bir de, bir de, bir de, bir de, bir de, bir de, bir de, bir de, bir de, bir de, bir de, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir de, bir de, bir de, bir de, bir de, bir de, bir de, bir de, bir de, bir, bir de, bir de, bir, bir de, bir, bir de, bir, bir de, bir, bir de, bir, bir de, bir, bir de bir, bir, bir, bir, bir, bir de bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir, bir

**Byte-level BPE.**Aynı algoritma ama Unicode karakterleri yerine çiğ baytlar (256 temel jeton) üzerinde.`[UNK]`GPT-2 50.257 jeton kullanır (256 byte + 50.000 birleşim + 1 özel).

> **字节级 BPE。**Aynı algoritma ama orijinal yazılımlarda ((256 个基础代币) değil, Unicode 字符上──保证零 `[UNK]`Token  任何字节序列都可编码──GPT-2 使用 50,257 个 token──

**Unigram.**Büyük bir kelime birikimi ile başlayın. Her bir token'e bir unigram olasılığı verin. En az korpus log olasılığını artıran tokenleri tekrar tekrar kesin. Tahmin için muhtemel: örneği örnekleyebilir. T5, mBART, ALBERT, XLNet, Gemma tarafından kullanılır.

> **Unigram。**Büyük kelime şemasından başlayalım. Her bir simgeye tek bir tekerleme paylaşılabilir.

**WordPiece.**Birleştirme çiftleri, çürük frekans yerine eğitim korpusunun olasılığını arttırır.

> **WordPiece。**合并使训练语料似然最大化而非原始频率最高对──用于BERT、DistilBERT、ELECTRA──

**SentencePiece vs tiktoken.**SentencePiece, kelime kitaplarını (BPE veya Unigram) doğrudan çiğ Unicode metnini kullanarak beyaz alanı `▁`. tiktoken, OpenAI'nin önceden oluşturulmuş kelime hazinelerine karşı hızlı *encoder*idir; eğitim almıyor.

> **SentencePiece vs tiktoken。**SentencePiece is in original Unicode 文本上*训练*词表的库,将空格编码为 `▁`△tiktoken is OpenAI 针对预构建词表的快速*编码器*;它不训练──

- Başparmak kuralı:

> 经验法则:

- **Training a new vocabulary:**SentencePiece (çok dilli, önceden tokenizasyon yapılmamış) veya HF Tokenizers.
  **训练新词表：**SatinSincePiece(多语言,无预分词) 或 HF Tokenizers──
- **Fast inference against GPT vocab:**tiktoken (cl100k_base, o200k_base).
  **针对 GPT 词表的快速推理：**Ticket.
- **Both:**HF Tokenizers  bir kütüphanede eğitim + hizmet.
  **两者兼有：**HF Tokenizers  一个库,训练 + 服务。

> **【中文解读】**Bu bölüm kodla sıfırdan gerçekleştirilen çekirdek algoritmasıdır. Bu "sıfırdan" yöntem çerçevenin arkasındaki prensipleri anlama yardımcı olur.
```figure
bpe-merge
```

## Yapın

> **【拓展：大语言模型的工程实践】**GPT'den ChatGPT'e kadar, NLP alanında "her görev bir model eğitimi" ile "her görevyi çözmek için bir model" biçiminin değişiminden geçti.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) şu anki işletme AI 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用  应用 应用 应用    应用     应用   应用        应用    应用       应用          应用        应用      应用          应用                                                                                                       

> **【拓展：NLP 的多语言挑战】**Küresel olarak 7000'den fazla dil vardır, ancak NLP çalışmaları çoğunlukla İngilizce ve az sayıda dil üzerinde yoğunlaşmaktadır.

## Yapın.

> **【中文解读】**Bu bölüm kodla sıfırdan gerçekleştirilen çekirdek algoritmasıdır. Bu "sıfırdan" yöntem çerçevenin arkasındaki prensipleri anlama yardımcı olur.

### Adım 1: BPE sıfırdan

```python
from collections import Counter, defaultdict


def train_bpe(corpus, vocab_size, special_tokens=None):
    """Train BPE tokenizer from a list of pre-tokenized word strings."""
    special_tokens = special_tokens or ["<unk>"]
    word_freqs = Counter(corpus)
    splits = {word: list(word) for word in word_freqs}
    merges = {}

    while len(special_tokens) + len(set(t for parts in splits.values() for t in parts)) + len(merges) < vocab_size:
        pair_counts = Counter()
        for word, freq in word_freqs.items():
            symbols = splits[word]
            for i in range(len(symbols) - 1):
                pair_counts[(symbols[i], symbols[i + 1])] += freq
        if not pair_counts:
            break
        best = max(pair_counts, key=pair_counts.get)
        new_token = best[0] + best[1]
        merges[best] = new_token
        for word in splits:
            symbols = splits[word]
            new_symbols = []
            i = 0
            while i < len(symbols):
                if i < len(symbols) - 1 and (symbols[i], symbols[i + 1]) == best:
                    new_symbols.append(new_token)
                    i += 2
                else:
                    new_symbols.append(symbols[i])
                    i += 1
            splits[word] = new_symbols
    return merges, special_tokens


def bpe_encode(text, merges, special_tokens):
    """Encode text using learned BPE merges."""
    tokens = list(text)
    for (a, b), merged in merges.items():
        new_tokens = []
        i = 0
        while i < len(tokens):
            if i < len(tokens) - 1 and tokens[i] == a and tokens[i + 1] == b:
                new_tokens.append(merged)
                i += 2
            else:
                new_tokens.append(tokens[i])
                i += 1
        tokens = new_tokens
    return tokens
```

BPE, eğitim sırasındaki birleşmeleri uyguluyor, bu nedenle daha önceki birleşmeler daha sonraki belirtileri engelleyen daha uzun belirtiler oluşturur.

> 合并顺序很重要──BPE 按训练顺序应用合并,所以较早的合并创建更长的代币,阻止后续合并──这就是为什么BPE 词表不能跨模型移植──

### Adım 2: Tiktoken ve SentencePiece ile simgelik

```python
import tiktoken

enc = tiktoken.get_encoding("cl100k_base")
tokens = enc.encode("Hello, world!")
print(tokens)           # [9906, 11, 1917, 0]
print(enc.decode(tokens))  # Hello, world!
```

```python
import sentencepiece as spm

spm.SentencePieceTrainer.train(input="corpus.txt", model_prefix="m", vocab_size=1000)
sp = spm.SentencePieceProcessor(model_file="m.model")
print(sp.encode("Hello world", out_type=str))  # ['▁Hello', '▁world']
```

### Adım 3: Doğurganlık karşılaştırması

```python
def fertility(text, tokenizer_fn):
    return len(tokenizer_fn(text))

# BPE on English: ~1.3 tokens/word
# BPE on Hindi: ~3.5 tokens/word
# BPE on Amharic: ~8 tokens/word
```

> **【中文解读】**Bu bölümde, PyTorch, HuggingFace gibi olgun çerçeveler nasıl kullanılacağını gösterir.

> **【拓展：Prompt Engineering 与 LLM 应用】**Hızlı Mühendislik NLP mühendislerinin temel beceri haline geldi. Zero-shot'tan birkaç-shot'a, Chain-of-Thought'tan ReAct'e kadar, farklı fikir stratejileri farklı durumlarda uygulanmaktadır.

## Çerçeveyi kullanın.

Ekosistemden seçin.

> 按生态系统选择──

- **OpenAI models (GPT-4, GPT-4o):**tiktoken. OpenAI'nin simgeselleştirilmesinin hızlı ve kesin bir şekilde yeniden üretilmesi. / tiktoken。快速、精确复现 OpenAI 分词。
- **Multilingual / custom training:**SentencePiece. Çiğ metinden trenler, herhangi bir senaryoyu ele alır.
- **Hugging Face models:**AutoTokenizer. Sağ arka uç otomatik olarak sarılır. / AutoTokenizer.
- **Maximum speed at inference:**HF Tokenizers (Rust backend) veya tiktoken (Python + C). / 推理最高速度:HF Tokenizers 或 tiktoken。

> **【中文解读】**Bu bölümde modellerin kullanılabilir ürünler için nasıl dağıtılacağı üzerinde yoğunlaşmaktadır.

## İndirin . Ürünler .

- Kaydet .`outputs/prompt-tokenizer-picker.md`- ...

> 保存为 `outputs/prompt-tokenizer-picker.md`- ...

```markdown
---
name: tokenizer-picker
description: Pick the right tokenizer for a given model or training pipeline.
phase: 5
lesson: 19
---

Given a model family or training goal, output:

1. Algorithm. BPE (GPT family), Unigram (T5 family), WordPiece (BERT family).
2. Library. tiktoken (GPT inference), SentencePiece (training), HF Tokenizers (both).
3. Vocabulary size and its impact on context window utilization.
4. Fertility estimate for the target language(s).

Refuse to mix tokenizer families in the same pipeline without explicit encode/decode boundaries.
```

> **【中文解读】**练习题按照易/中级/难三度递进;;建议至少完成中级题,Hard级适合深入研究或面试准备;;

## Egzersizler.

1. **Easy.**BPE'yi küçük bir korpus üzerinde eğit (1000 kelime). 20 test kelimeyi kodlayıp çözün.**简单。**Küçük dilde eğitim BPE 编码解码 20 个测试词 验证往返保真度 
2. **Medium.**Tiktoken'in cl100k_base'ını kullanarak İngilizce, Çinci ve Hintçe için tokenizasyon verimliliğini karşılaştırın.**中等。**TikTok kullanın İngilizce, Çince ve Hintçe'de sözcük çoğalımı oranı karşılaştırın.
3. **Hard.**SentencePiece Unigram modelini İngilizce-Hindî bir kurpus üzerinde eğit.**困难。**Karışık İngilizce-Hind dil dil dilinde dil dilde eğitim SentencePiece Unigram 模型── aynı veriler üzerinde eğitim verilen BPE 模型 ile karşılaştırma 繁殖率──

> **【中文解读】**术语表中的"İnsanların ne dediği" vs "Gerçekten ne anlama geldiği" 区分日常口语和精确技术含义──在团队协作中,统一术语定义可以避免大量沟通误解──

## Anahtar Şartlar .

| Term / 术语 | What people say / 人们常说的 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| BPE（字节对编码） | GPT's tokenizer / GPT 的分词器 | Iteratively merge most frequent adjacent pairs. / 迭代合并最频繁的相邻对。 |
| Unigram | T5's tokenizer / T5 的分词器 | Prune tokens from large vocabulary by likelihood. / 按似然从大词表剪枝。 |
| WordPiece | BERT's tokenizer / BERT 的分词器 | Merge pairs that maximize corpus likelihood. / 合并使语料似然最大化的对。 |
| SentencePiece | Training library / 训练库 | Train BPE or Unigram on raw text. Encodes whitespace as `▁`. / 在原始文本上训练 BPE 或 Unigram。 |
| tiktoken | OpenAI's encoder / OpenAI 编码器 | Fast encoding against pre-built GPT vocabularies. / 针对预构建 GPT 词表的快速编码。 |
| Fertility（繁殖率） | Tokens per word / 每词 token 数 | How many subword tokens a word produces. Lower is better. / 一个词产生多少子词 token。越低越好。 |

> **【中文解读】**延伸阅读, derinlemesine öğrenme için yüksek kaliteli kaynaklar sağladı. Bu makaleler ve dersler, derinlemesine anlama ihtiyacı olan okuyuculara uygun olarak bu alanın klasik referanslarıdır.

## Daha fazla okumak

- [Sennrich et al. (2016). Neural Machine Translation of Rare Words with Subword Units](https://arxiv.org/abs/1508.07909)BPE kağıdı.
- [Kudo (2018). Subword Regularization](https://arxiv.org/abs/1804.10959) Unigram makalesi. / Unigram 论文。
- [SentencePiece documentation](https://github.com/google/sentencepiece) eğitim ve hizmet. / 訓練和服務。
- [tiktoken](https://github.com/openai/tiktoken) OpenAI'nin hızlı simgeselcisi. / OpenAI 快速分词器──
- [Hugging Face Tokenizers](https://huggingface.co/docs/tokenizers/) Rust desteklenen eğitim + servis. / Rust 后端训练 + 服务。
