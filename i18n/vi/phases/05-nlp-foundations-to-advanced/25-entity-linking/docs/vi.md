# Entity Linking & Disambiguation  thực thể liên kết với tiêu歧

> NER tìm thấy "Paris". Cơ quan liên kết quyết định: Paris, Pháp? Paris Hilton? Paris, Texas? Paris (tổng hoàng tử Trojan)?
> NER 找到了 "Paris"──实体链接决定:巴黎:法国:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎;巴黎:巴黎:巴黎;巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎:巴黎;巴黎;巴黎:巴黎:巴黎:巴黎:巴黎;巴黎:巴黎:巴黎:巴黎;巴黎:巴黎:巴黎:巴黎;

> **【中文解读】**Để NER 提取 các thực thể liên kết đến các mục duy nhất trong thư viện kiến thức.

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 06 (NER), Phase 5 · 22 (Embedding Models) | **前置知识:** Phase 5 · 06（NER），Phase 5 · 22（嵌入模型）
**Time:** ~45 minutes | **时间:** ~45 分钟

## Vấn đề  vấn đề giới thiệu

Liên kết thực thể (EL) giải quyết mỗi đề cập đến một mục duy nhất trong cơ sở kiến thức (Wikidata, Wikipedia, GeoNames).

> 实体链接(EL) sẽ mỗi chỉ称解析为知识库(Wikidata、Wikipedia、GeoNames) trong số các mục đích duy nhất.

> **【中文解读】**Câu hỏi được đặt ra trong phần này là: làm thế nào để hiểu và áp dụng đúng công nghệ này trong công trình thực tế.

## Khái niệm cốt lõi

> **【中文解读】**本节介绍核心概念和理论基础──

**Candidate generation.**Với "Jordan", mục KB nào phù hợp? Sử dụng kết hợp chuỗi, phân giải chuyển hướng và tiền lệ phổ biến. Thông thường lấy 10 - 50 ứng viên hàng đầu.

> **候选生成。**给定 "Jordan", which knowledge library条目匹配? use字符串匹配、重定向解析和流行度先验──通常检索前 10-50个候选──

**Disambiguation.**Đánh giá các ứng cử viên theo tương đồng ngữ cảnh. Bi-encoder cho tốc độ, cross-encoder cho độ chính xác.

> **消歧。**按上下文相似度排名候选──双编码器用于速度,交叉编码器用于准确率──上下文 = 周围文本 + 知识库中的实体描述──

> **【拓展：大语言模型的工程实践】**Từ GPT đến ChatGPT, NLP đã trải qua một quá trình chuyển đổi.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) là cấu trúc phổ biến nhất trong ứng dụng AI trong doanh nghiệp hiện tại.

> **【拓展：NLP 的多语言挑战】**Trên toàn cầu có hơn 7000 ngôn ngữ, nhưng nghiên cứu về NLP tập trung chủ yếu vào tiếng Anh và một số ít ngôn ngữ.

## Hãy xây dựng nó.

> **【中文解读】**Bài viết này thông qua mã từ zero thực hiện các thuật toán cốt lõi.
```figure
gx-entity-linking
```

## Hãy xây dựng nó

### Bước 1: tạo một danh mục từ các chuyển hướng Wikipedia

```python
alias_to_entities = {
    "jordan": ["Q41421 (Michael Jordan)", "Q810 (Jordan, country)", "Q254110 (Michael B. Jordan)"],
    "paris":  ["Q90 (Paris, France)", "Q663094 (Paris, Texas)", "Q55411 (Paris Hilton)"],
    "apple":  ["Q312 (Apple Inc.)", "Q89 (apple, fruit)"],
}
```

Dữ liệu từ Wikipedia: ~ 18M (tên gọi, thực thể) cặp. Tải từ các bãi rác Wikidata. Cung cấp như chỉ mục đảo ngược.

### Bước 2: Sự phân biệt rõ ràng dựa trên bối cảnh

```python
def entity_link(mention, context, kb_lookup, embed_model):
    candidates = kb_lookup.get(mention.lower(), [])
    if not candidates:
        return None
    ctx_emb = embed_model.encode([context])
    scores = []
    for cand in candidates:
        cand_emb = embed_model.encode([cand["description"]])
        scores.append((cand, float(np.dot(ctx_emb[0], cand_emb[0]))))
    return max(scores, key=lambda x: x[1])[0]
```

> **【中文解读】**Bài này sẽ cho thấy cách sử dụng một khuôn khổ đã trưởng thành để nhanh chóng áp dụng công nghệ này.

> **【拓展：Prompt Engineering 与 LLM 应用】**Kỹ thuật nhanh chóng đã trở thành kỹ năng cốt lõi của các kỹ sư NLP.

## Hãy sử dụng nó để thực hiện

> **【中文解读】**Bài viết này tập trung vào cách thức triển khai mô hình cho các sản phẩm có thể sử dụng.

- **OpenTapioca.**EL nhẹ cho Wikidata. / OpenTapioca。Wikidata 轻量 EL。
- **REL (Radboud Entity Linker).**State of the art Wikipedia EL. / REL。先进 Wikipedia EL。
- **GENRE.**Cơ quan tự do lập liên kết bởi Facebook. / GENRE。Facebook 自回归实体链接。
- **LLM prompting.**Hãy yêu cầu LLM để không rõ ràng.

## Chuyển nó đi.

Cứ như `outputs/skill-entity-linker.md`- Có thể là:

> 保存为 `outputs/skill-entity-linker.md`- Có thể là:

```markdown
Given mentions from NER, link them to a knowledge base.
1. KB choice (Wikidata, Wikipedia, custom).
2. Candidate generation strategy.
3. Disambiguation method (embedding similarity, cross-encoder, LLM).
```

## Tập luyện bài tập

1. **Easy.**Xây dựng một máy phát triển ứng cử viên dựa trên Wikipedia. / **简单。**构建基于Wikipedia 的候选生成器──
2. **Medium.**Thực hiện phân biệt định nghĩa bằng mã hóa hai và đánh giá trên một bộ thử nghiệm. / **中等。**实现双编码器消歧──
3. **Hard.**So sánh EL dựa trên LLM với EL thần kinh trên một tập dữ liệu đa ngôn ngữ. / **困难。**Trong tập dữ liệu đa ngôn ngữ so sánh LLM EL vs 神经 EL.

## Từ khóa  Từ khóa nhanh chóng

| Term / 术语 | What it means / 含义 |
|------|-----------------------|
| Entity linking（实体链接） | Map mentions to KB entries. / 将指称映射到知识库条目。 |
| Disambiguation（消歧） | Pick the correct entity among candidates. / 在候选中选择正确实体。 |
| Candidate generation（候选生成） | Retrieve possible KB matches for a mention. / 为指称检索可能的知识库匹配。 |

## Xem thêm 延伸阅读

- [Wu et al. (2020). Scalable Zero-shot Entity Linking](https://arxiv.org/abs/1910.02854)/ 可扩展零样本实体链接──
- [De Cao et al. (2020). GENRE](https://arxiv.org/abs/1912.01572)/ 自归实体链接──
