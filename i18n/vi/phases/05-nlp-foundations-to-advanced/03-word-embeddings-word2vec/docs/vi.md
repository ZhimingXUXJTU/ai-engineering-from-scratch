# Word Embeddings  Word2Vec từ đầu  Word2Vec từ không thực hiện

> Một từ là công ty mà nó giữ. Hãy tập trung vào ý tưởng đó và hình học sẽ rơi ra.
> Một từ phụ thuộc vào công ty mà nó giữ. Trong ý tưởng này đào tạo một mạng lưới tầng thấp, những gì tự nhiên xuất hiện.

> **【中文解读】**Word2Vec 把词映射到密向量空间,相似词在向量空间中接近──这是现代NLP的基石──

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 02 (BoW + TF-IDF), Phase 3 · 03 (Backpropagation from Scratch) | **前置知识:** Phase 5 · 02（BoW + TF-IDF），Phase 3 · 03（反向传播从零实现）
**Time:** ~75 minutes | **时间:** ~75 分钟

## Vấn đề  vấn đề giới thiệu

TF-IDF biết `dog`và `puppy`là những từ khác nhau. nó không biết chúng có nghĩa gần như cùng một điều.`dog`không thể nói chung đến một đánh giá về `puppy`Bạn có thể viết qua nó bằng cách liệt kê các từ đồng nghĩa, nhưng điều đó không có trong các thuật ngữ hiếm, thuật ngữ miền, và mọi ngôn ngữ bạn không dự đoán.

> TF-IDF 知道 `dog`和 `puppy`Đó là một từ khác nhau. Nó không biết ý nghĩa của chúng gần như giống nhau.`dog`Các phân loại trên không thể được phổ biến về`puppy`Bạn có thể khắc phục bằng cách liệt kê các từ ngữ có cùng nghĩa, nhưng điều này sẽ thất bại trong các thuật ngữ hiếm gặp, và trong mỗi ngôn ngữ mà bạn không mong đợi.

Anh muốn một đại diện ở đâu?`dog`và `puppy`- Không gian gần nhau.`king - man + woman`Đất gần đó`queen`Một người mẫu được đào tạo`dog`chuyển một số tín hiệu đến `puppy`miễn phí.

> Bạn muốn một cách biểu hiện,让 `dog`和 `puppy`Trong không gian gần.`king - man + woman`落在 `queen`附近──让在 `dog`Mô hình tập luyện miễn phí`puppy`Chuyển lại một số tín hiệu.

Word2Vec đã cho chúng ta không gian đó. Mạng lưới thần kinh hai lớp, hàng nghìn tỷ token được phát hành vào năm 2013. Kiến trúc này gần như đơn giản đáng xấu hổ. Kết quả đã định hình lại NLP trong một thập kỷ.

> Word2Vec đã cho chúng ta không gian như vậy.

## Khái niệm cốt lõi

> **【中文解读】**Bài viết này giới thiệu các khái niệm và lý thuyết cốt lõi.

**Distributional hypothesis**(Tất cả hai từ này được viết trong năm 1957): "Bạn sẽ biết một từ từ từ những người mà nó giữ".

> **分布假设（Distributional Hypothesis）**(Năm thứ nhất, 1957):"You will know it through a word held by company" Nếu hai từ xuất hiện giống nhau trên văn bản dưới, chúng có thể có nghĩa là những điều tương tự.

Word2Vec có hai hương vị, cả hai đều khai thác ý tưởng đó.

> Word2Vec có hai biến thể, chúng tôi đã sử dụng ý tưởng này.

- **Skip-gram.**Với một từ trung tâm, hãy dự đoán những từ xung quanh. `cat -> (the, sat, on)`với kích thước cửa sổ 2.
  **Skip-gram（跳字模型）。**给定中心词,预测周围的词──`cat -> (the, sat, on)`, cửa sổ lớn là 2...
- **CBOW (continuous bag of words).**Với những từ xung quanh, hãy dự đoán trung tâm.`(the, sat, on) -> cat`- Tôi không biết.
  **CBOW（连续词袋模型）。**给定周围的词,预测中心词――`(the, sat, on) -> cat`

Skip-gram là chậm hơn để đào tạo nhưng xử lý từ hiếm hơn.

> Skip-gram  luyện tập chậm hơn nhưng tốt hơn để xử lý hiếm thấy từ.

Mạng lưới có một lớp ẩn mà không có tính không tuyến tính. Input là một vector nóng trên từ vựng. Output là một softmax trên từ vựng. Sau khi đào tạo, bạn ném ra lớp xuất.

> 网络 có một lớp ẩn của hàm hoạt động không dây không liên kết. 输入 là một-mạnh trên bảng chữ cái. 向量. 输出 là mềm trên bảng chữ cái.

```
one-hot(center) ── W ──▶ hidden (d-dim) ── W' ──▶ softmax(vocab)
                          ^
                          this is the embedding
```

Trù: Softmax trên 100k từ là quá đắt tiền. Word2Vec sử dụng **negative sampling**để biến nó thành một nhiệm vụ phân loại nhị phân. Dự đoán "có bao nhiêu từ ngữ trong ngữ cảnh xuất hiện gần từ trung tâm này, có hay không".

> : đối với 100.000 từ làm mềmmax 代价太高──Word2Vec 使用**负采样（Negative Sampling）**Để chuyển đổi thành nhiệm vụ phân loại hai. Dự đoán " liệu từ trên có xuất hiện ở gần từ trung tâm này hay không".

> **【拓展：大语言模型的工程实践】**Từ GPT đến ChatGPT, NLP đã trải qua sự chuyển đổi từ "mỗi nhiệm vụ đào tạo một mô hình" đến "một mô hình giải quyết tất cả các nhiệm vụ". Trong công trình thực tế, việc triển khai LLM cần phải xem xét các vấn đề như: giới hạn token, trì hoãn, chi phí, kiểm tra an toàn, và các vấn đề khác.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) là cấu trúc phổ biến nhất trong ứng dụng AI của doanh nghiệp hiện tại: sẽ truy vấn người dùng trước tiên truy vấn các đoạn tài liệu liên quan, tiếp tục truy vấn kết quả như trên dưới đây cho LLM 生成答案──

> **【拓展：NLP 的多语言挑战】**Trên toàn cầu có hơn 7000 ngôn ngữ, nhưng nghiên cứu về NLP tập trung chủ yếu vào tiếng Anh và một số ít ngôn ngữ.

## Hãy xây dựng nó.

> **【中文解读】**本节通过代码实现核心算法从零――这种" từ đầu"的方式能帮助理解框架背后的原理,遇到问题时不会被黑盒困住――
```figure
word-vector-arithmetic
```

## Hãy xây dựng nó

### Bước 1: các cặp đào tạo từ một corpus

```python
def skipgram_pairs(docs, window=2):
    pairs = []
    for doc in docs:
        for i, center in enumerate(doc):
            for j in range(max(0, i - window), min(len(doc), i + window + 1)):
                if i == j:
                    continue
                pairs.append((center, doc[j]))
    return pairs
```

```python
>>> skipgram_pairs([["the", "cat", "sat", "on", "mat"]], window=2)
[('the', 'cat'), ('the', 'sat'),
 ('cat', 'the'), ('cat', 'sat'), ('cat', 'on'),
 ('sat', 'the'), ('sat', 'cat'), ('sat', 'on'), ('sat', 'mat'),
 ...]
```

Mỗi cặp (trung tâm, ngữ cảnh) trong cửa sổ là một ví dụ đào tạo tích cực.

> 窗口中的每个(中心词,上下文词) đối với là một mô hình thực tập chính xác.

### Bước 2: nhúng bảng

Hai cái.`W`là bảng nhúng từ trung tâm (một bạn giữ). `W'`là bảng từ ngữ ngữ cảnh (thường bị loại bỏ, đôi khi trung bình với `W`().

> Hai cái xe.`W`Đó là một từ trong một cái tên.`W'`là trên 下文词表( thường bị bỏ rơi, đôi khi với `W`取平均) ⋅

```python
import numpy as np


def init_embeddings(vocab_size, dim, seed=0):
    rng = np.random.default_rng(seed)
    W = rng.normal(0, 0.1, size=(vocab_size, dim))
    W_prime = rng.normal(0, 0.1, size=(vocab_size, dim))
    return W, W_prime
```

Từ vựng kích thước 10k và dim 100 là thực tế; cho việc giảng dạy, 50 từ vựng x 16 dim là đủ để xem hình học.

> Ước tính: Ước tính: Ước tính: Ước tính: Ước tính: Ước tính: Ước tính: Ước tính: Ước tính: Ước tính: Ước tính: Ước tính: Ước tính: Ước tính: Ước tính: Ước tính: Ước tính: Ước tính: Ước tính: Ước tính: Ước tính: Ước tính: Ước tính: Ước tính: Ước tính: Ước tính: Ưu điểm: Ưu điểm: Ưu điểm: Ưu điểm: Ưu điểm: Ưu điểm: Ưu điểm: Ưu điểm: Ưu điểm: Ưu điểm: Ưu điểm: Ưu điểm: Ưu điểm: Ưu điểm: Ưu điểm: Ưu điểm: Ưu điểm: Ưu điểm: Ưu điểm: Ưu điểm: Ưu điểm: Ưu điểm: Ưu điểm: Ưu điểm: Ưu điểm: Ưu điểm: Ưu điểm: Ưu điểm: Ưu điểm: Ưu điểm: Ưu điểm: Ưu điểm: Ưu điểm: Ưu điểm: Ưu điểm: Ưu điểm: Ưu điểm: Ưu điểm: Ưu điểm: Ưu điểm:

### Bước 3: mục tiêu lấy mẫu tiêu cực

Đối với mỗi cặp tích cực `(center, context)`, mẫu `k`Từ ngẫu nhiên từ từ vựng như âm.`W[center] · W'[context]`là cao cho tích cực và thấp cho tiêu cực.

> Đối với mỗi mẫu thực`(center, context)`, từ từ biểu diễn trong mẫu`k`个随机词作为负例──训练模型使正例的点积 `W[center] · W'[context]`高,负例的低――

```python
def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-np.clip(x, -20, 20)))


def train_pair(W, W_prime, center_idx, context_idx, negative_indices, lr):
    v_c = W[center_idx]
    u_pos = W_prime[context_idx]
    u_negs = W_prime[negative_indices]

    pos_score = sigmoid(v_c @ u_pos)
    neg_scores = sigmoid(u_negs @ v_c)

    grad_center = (pos_score - 1) * u_pos
    for i, u in enumerate(u_negs):
        grad_center += neg_scores[i] * u

    W[context_idx] = W[context_idx]
    W_prime[context_idx] -= lr * (pos_score - 1) * v_c
    for i, neg_idx in enumerate(negative_indices):
        W_prime[neg_idx] -= lr * neg_scores[i] * v_c
    W[center_idx] -= lr * grad_center
```

Công thức ma thuật: mất hậu cần trên cặp dương (nhiều cần sigmoid gần 1) cộng với mất hậu cần trên cặp âm (nhiều cần sigmoid gần 0).

> Kỹ thuật của 神奇:正例对上逻辑损失(希望 sigmoid 接近 1)加上负例对上逻辑损失(希望 sigmoid 接近 0) ・・・梯度流向两个表――完整推导见原始论文; nếu bạn muốn làm cho nó hiểu sâu hơn, hãy dùng giấy viết đi một lần nữa――

### Bước 4: tập luyện trên một bộ đồ chơi

```python
def train(docs, dim=16, window=2, k_neg=5, epochs=100, lr=0.05, seed=0):
    vocab = build_vocab(docs)
    vocab_size = len(vocab)
    rng = np.random.default_rng(seed)
    W, W_prime = init_embeddings(vocab_size, dim, seed=seed)
    pairs = skipgram_pairs(docs, window=window)

    for epoch in range(epochs):
        rng.shuffle(pairs)
        for center, context in pairs:
            c_idx = vocab[center]
            ctx_idx = vocab[context]
            negs = rng.integers(0, vocab_size, size=k_neg)
            negs = [n for n in negs if n != ctx_idx and n != c_idx]
            train_pair(W, W_prime, c_idx, ctx_idx, negs, lr)
    return vocab, W
```

Sau đủ thời gian trên một tập hợp lớn, những từ chia sẻ bối cảnh có những nhúng cốt tương tự. trên một tập hợp đồ chơi, bạn thấy hiệu ứng yếu. trên hàng tỷ token, bạn thấy nó đáng kể.

> Sau nhiều lần chia sẻ trên các ngôn ngữ lớn, các từ chia sẻ trên các ngôn ngữ dưới đây có một từ trung tâm tương tự được nhúng vào.

### Bước 5: thủ thuật tương tự

```python
def nearest(vocab, W, target_vec, topk=5, exclude=None):
    exclude = exclude or set()
    inv_vocab = {i: w for w, i in vocab.items()}
    norms = np.linalg.norm(W, axis=1, keepdims=True) + 1e-9
    W_norm = W / norms
    target = target_vec / (np.linalg.norm(target_vec) + 1e-9)
    sims = W_norm @ target
    order = np.argsort(-sims)
    out = []
    for i in order:
        if i in exclude:
            continue
        out.append((inv_vocab[i], float(sims[i])))
        if len(out) == topk:
            break
    return out


def analogy(vocab, W, a, b, c, topk=5):
    v = W[vocab[b]] - W[vocab[a]] + W[vocab[c]]
    return nearest(vocab, W, v, topk=topk, exclude={vocab[a], vocab[b], vocab[c]})
```

Trên các vector Google News 300d được đào tạo trước:

```python
>>> analogy(vocab, W, "man", "king", "woman")
[('queen', 0.71), ('monarch', 0.62), ('princess', 0.59), ...]
```

`king - man + woman = queen`Không phải vì người mẫu biết hoàng gia là gì, vì người dẫn đường là người có quyền.`(king - man)`bắt được thứ gì đó như " hoàng gia", và thêm nó vào `woman`đất gần vùng đất nữ hoàng.

> `king - man + woman = queen`Không phải vì mô hình biết cái gì là nhà vua mà vì trọng lượng.`(king - man)`n bắt được thứ gì đó giống như "Nhà vua", sẽ thêm nó vào `woman`上落在王室女性区域附近.

> **【中文解读】**Bài này sẽ trình bày cách sử dụng một khung đã phát triển như PyTorch, HuggingFace, và các khác.

> **【拓展：Prompt Engineering 与 LLM 应用】**Kỹ thuật nhanh chóng đã trở thành kỹ năng cốt lõi của các kỹ sư NLP. Từ Zero-shot đến Few-shot, từ Chain-of-Thought đến ReAct, các chiến lược khác nhau áp dụng cho các tình huống khác nhau. Trong các dự án thực tế, thiết kế của System提示(System Prompt) ảnh hưởng trực tiếp đến sự ổn định và chất lượng sản xuất của ứng dụng LLM.

## Hãy sử dụng nó để thực hiện

Viết Word2Vec từ đầu là dạy.`gensim`- Tôi không biết.

> Từ零编写 Word2Vec là để dạy.`gensim`

```python
from gensim.models import Word2Vec

sentences = [
    ["the", "cat", "sat", "on", "the", "mat"],
    ["the", "dog", "ran", "across", "the", "room"],
]

model = Word2Vec(
    sentences,
    vector_size=100,
    window=5,
    min_count=1,
    sg=1,
    negative=5,
    workers=4,
    epochs=30,
)

print(model.wv["cat"])
print(model.wv.most_similar("cat", topn=3))
```

Để làm việc thực sự, bạn hầu như không bao giờ tự đào tạo Word2Vec. Bạn tải xuống các vector được đào tạo trước.

> Trong thực tế, bạn hầu như không tự tập luyện Word2Vec──你下载预训向量──

- **GloVe** Phương pháp phân tích các yếu tố tử liệu đồng xuất hiện của Stanford. 50d, 100d, 200d, 300d điểm kiểm soát.
  **GloVe**  斯坦福's共现矩阵分解方法──50维、100维、200维、300维的检查点──通用覆盖良好──第04 课专讲 GloVe──
- **fastText** Word2Vec mở rộng của Facebook nhúng n-gram ký tự. xử lý từ ngoài từ vựng bằng cách soạn các từ phụ. Bài học 04.
  **fastText** Word2Vec của Facebook  mở rộng, nhúng vào chữ n-gram── thông qua组合子词处理词表外词──第 04 课──
- **Pretrained Word2Vec on Google News** 300d, từ vựng 3M, được xuất bản năm 2013.
  **Google News 预训练 Word2Vec** 300 维,300.000 từ表,2013 năm phát hành.

### Khi Word2Vec vẫn thắng vào năm 2026

- Đọc về các bản tóm tắt y tế trong một giờ trên máy tính xách tay, có được các vector chuyên dụng không có mô hình tổng quát.
  ️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️
- Kỹ thuật tính năng theo kiểu tương tự. `gender_vector = mean(man - woman pairs)`- Trả nó ra từ những từ khác để có được một trục trung lập về giới tính.
  类比式特征工程──`gender_vector = mean(man - woman pairs)` Từ từ khác giảm nó để đạt được giới tính trung tính vẫn được sử dụng trong nghiên cứu tính công bằng
- 100d đủ nhỏ để vẽ qua PCA hoặc t-SNE và thực sự thấy các cụm hình thành.
  可解释性──100 维足够小, có thể qua PCA hoặc t-SNE 绘图并实际看到聚类形成──
- Bất cứ nơi nào, suy luận phải chạy trên thiết bị mà không có GPU. Word2Vec tìm kiếm là một hàng lấy.
  Bất kỳ nhu cầu nào trên thiết bị không có GPU được vận hành trong trường hợp này.

### Khi Word2Vec thất bại

Bức tường đa sắc.`bank`có một vector. `river bank`và `financial bank`Hãy chia sẻ nó.`table`Một bộ phân loại dòng chảy xuống không thể phân biệt các giác quan từ vector.

> 多义词 rào cản`bank`Chỉ có một đường.`river bank`和 `financial bank`共享 nó.`table`(电子表格 vs 家具) chia sẻ nó.

Các bản nhúng ngữ cảnh (ELMo, BERT, mọi biến thể kể từ đó) giải quyết vấn đề này bằng cách tạo ra một vector khác nhau cho mỗi sự xuất hiện của từ dựa trên bối cảnh xung quanh.

> 上下文嵌入(ELMo、BERT 以及之后的所有 Transformer) thông qua việc tạo ra các khối lượng khác nhau cho sự xuất hiện của mỗi từ trên xung quanh đã giải quyết vấn đề này.

Vấn đề không có từ vựng là sự thất bại khác.`Zoomer-approved`nếu nó không có trong dữ liệu đào tạo. Không có sự lùi. fastText sửa chữa điều này bằng cách tạo thành từ phụ (đọc 04).

> 词表外(Out-of-Vocalory) vấn đề là một thất bại khác.`Zoomer-approved`Không trong dữ liệu đào tạo, Word2Vec 就从未见过它. Không có kế hoạch sau.

> **【中文解读】**Phần này tập trung vào cách phân phối mô hình như một sản phẩm có thể sử dụng.

## Chuyển nó đi.

Cứ như `outputs/skill-embedding-probe.md`- Có thể là:

```markdown
---
name: embedding-probe
description: Inspect a word2vec model. Run analogies, find neighbors, diagnose quality.
version: 1.0.0
phase: 5
lesson: 03
tags: [nlp, embeddings, debugging]
---

You probe trained word embeddings to verify they are working. Given a `gensim.models.KeyedVectors` object and a vocabulary, you run:

1. Three canonical analogy tests. `king : man :: queen : woman`. `paris : france :: tokyo : japan`. `walking : walked :: swimming : ?`. Report the top-1 result and its cosine.
2. Five nearest-neighbor tests on domain-specific words the user supplies. Print top-5 neighbors with cosines.
3. One symmetry check. `similarity(a, b) == similarity(b, a)` to within float precision.
4. One degenerate check. If any embedding has a norm below 0.01 or above 100, the model has a training bug. Flag it.

> **【中文解读】** 练习题按照 Easy/Medium/Hard 三个难度递进。建议至少完成 Medium 级别的题目，Hard 级别适合深入研究或面试准备。

Refuse to declare a model good on analogy accuracy alone. Analogy benchmarks are gameable and do not transfer to downstream tasks. Recommend intrinsic + downstream evaluation together.
```

## Tập luyện bài tập

1. **Easy.**Thực hiện vòng tròn huấn luyện trên một bộ phận nhỏ (20 câu về mèo và chó).`nearest(vocab, W, W[vocab["cat"]])`trả lại `dog`Nếu không, tăng thời đại hoặc từ vựng.
   **简单。**Trong một vòng tròn tập luyện trên một ngôn ngữ nhỏ.`nearest(vocab, W, W[vocab["cat"]])`返回的 top 3 中包含 `dog`Nếu không, tăng lượt sau hoặc từ表.
2. **Medium.**Thêm mẫu phụ của các từ thường xuyên.`10^-5`được loại bỏ từ các cặp đào tạo với xác suất tương xứng với tần suất của chúng.
   **中等。**添加高频词子采样──频率高于 `10^-5`Từ từ theo tần suất của nó tương đương với xác suất từ tập luyện đối với từ bỏ.
3. **Hard.**Tập một mô hình trên 20 Newsgroups corpus.`he - she`và `doctor - nurse`. Dự án các từ nghề trên cả hai trục. báo cáo các nghề có khoảng cách thiên vị lớn nhất. Đây là loại hình của các nhà nghiên cứu công bằng thăm dò sử dụng.
   **困难。**Trong 20 Newsgroups 语料上训练模型――计算两个偏见轴:`he - she`和 `doctor - nurse`将职业词投投向两个轴上 报告哪些职业有最大偏见差距                                                                                                                                                                                                                                                  

> **【中文解读】**练题按照 Easy/Medium/Hard 三个难度递进;;建议至少完成 级别的题目, 级别适合深入研究或面试准备;;

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means | 术语 | 人们常说的 | 实际含义 |
|------|-----------------|-----------------------|------|-----------|---------|
| Word embedding | Word as a vector | A dense, low-dim (typically 100-300) representation learned from context. | 词嵌入 | 词向量 | 从上下文学习的稠密、低维（通常 100-300）表示。 |
| Skip-gram | Word2Vec trick | Predict context words from center word. Slower than CBOW, better for rare words. | Skip-gram | Word2Vec 技巧 | 从中心词预测上下文词。比 CBOW 慢，对罕见词更好。 |
| Negative sampling | Training shortcut | Replace softmax over full vocab with binary classification against `k` random words. | 负采样 | 训练捷径 | 用对 `k` 个随机词的二分类替换对整个词表的 softmax。 |
| Static embedding | One vector per word | Same vector regardless of context. Fails on polysemy. | 静态嵌入 | 每个词一个向量 | 无论上下文如何都是同一个向量。在多义词上失败。 |
| Contextual embedding | Context-sensitive vector | Different vector for each occurrence based on surrounding words. What transformers produce. | 上下文嵌入 | 上下文敏感向量 | 根据周围词，每次出现都是不同的向量。Transformer 产生的。 |
| OOV | Out of vocabulary | Word not seen in training. Word2Vec cannot produce a vector for these. | OOV（词表外） | 词表外 | 训练中未见过的词。Word2Vec 无法为这些词产生向量。 |

> **【中文解读】**Trong 术语表中的"Những gì mọi người nói" vs "Những gì nó thực sự có nghĩa" 区分日常口语和精确技术含义── 在团队协作中,统一术语定义可以避免大量沟通误解──

## Xem thêm 延伸阅读

- [Mikolov et al. (2013). Distributed Representations of Words and Phrases and their Compositionality](https://arxiv.org/abs/1310.4546) bài báo lấy mẫu âm. ngắn và dễ đọc. / 负采样论文。短小易读。
- [Rong, X. (2014). word2vec Parameter Learning Explained](https://arxiv.org/abs/1411.2738) dẫn xuất rõ ràng nhất của các gradient, nếu toán học của bài viết ban đầu cảm thấy dày đặc. / 最清晰的梯度推导, nếu bạn cảm thấy toán học quá密集.
- [gensim Word2Vec tutorial](https://radimrehurek.com/gensim/models/word2vec.html) cài đặt đào tạo sản xuất thực sự hoạt động. / 真正有效的生产训练设置──
