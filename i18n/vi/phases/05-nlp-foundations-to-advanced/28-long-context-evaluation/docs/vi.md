# Đánh giá trong bối cảnh dài  NIAH, RULER, LongBench, MRCR 长上下文评估  NIAH、RULER

> Gemini 3 Pro quảng cáo 10M token của ngữ cảnh. với 1M token, 8-nháp MRCR giảm xuống còn 26,3%. quảng cáo ≠ sử dụng. đánh giá ngữ cảnh dài cho bạn biết khả năng thực tế của mô hình bạn đang vận chuyển trên.
> Gemini 3 Pro 宣称 10M token 上下文── 在 1M token 时,8-针 MRCR 降至 26.3%──宣称的 ≠可用──长上下文评估告诉你你正在部署模型的实际能力──

> **【中文解读】** đánh giá LLM trong dài trên dưới văn phòng cửa sổ thực tế

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 27 (LLM Evaluation) | **前置知识:** Phase 5 · 27（LLM 评估）
**Time:** ~45 minutes | **时间:** ~45 分钟

## Vấn đề  vấn đề giới thiệu

Đây là khoảng cách dung lượng ngữ cảnh năm 2026. Các bảng thông số nói 1M token. Các điểm chuẩn nói: ở 100K token, độ chính xác lấy lại giảm 15-40%. ở 500K, nó giảm 40-70%. mô hình không thực sự "xem" mọi thứ trong cửa sổ ngữ cảnh của nó bằng nhau.

> Đây là khoảng cách dung lượng trên dưới năm 2026 ∙ quy trình biểu đồ nói 1M token ∙基准说: trong 100K token ∙, kiểm tra xác thực tỷ lệ giảm 15-40% ∙ trong 500K, giảm 40-70% ∙ mô hình không giống như trong cửa sổ trên dưới nó ∙ nhìn "nhiên" nội dung ∙

> **【中文解读】**Câu hỏi được đặt ra trong phần này là: làm thế nào để hiểu và áp dụng đúng công nghệ này trong công trình thực tế.

Đánh giá ngữ cảnh dài đo lường các trục này: độ chính xác thu thập ở các độ sâu khác nhau, lý luận đa hop trên các tài liệu và tổng hợp thông tin phân tán.

> 长上下文评估测量这些轴: các chiều sâu khác nhau, tỷ lệ xác định tìm kiếm, các biện pháp nhảy nhiều trên các tài liệu, và sự tập hợp của thông tin phân tán.

## Khái niệm cốt lõi

> **【中文解读】**本节介绍核心概念和理论基础──

**NIAH (Needle in a Haystack).**Đặt một sự kiện cụ thể vào một tài liệu dài ở nhiều vị trí khác nhau. Hãy yêu cầu mô hình lấy nó. Các biện pháp: mô hình có thể tìm thấy một kim cáp ở độ sâu X trong một đống cỏ cỏ Y-token không?

> **NIAH（大海捞针）。**Trong các vị trí trong long档插入特定事实──让模型检索──测:模型能否在Y token的干草堆中深度X 处找到针?

**RULER.**NIAH mở rộng với nhiều kim, khoảng cách biến và các nhiệm vụ tổng hợp.

> **RULER。**扩展 NIAH 添加多针、可变距离和聚合任务──更全面──

**LongBench.**Các nhiệm vụ trong bối cảnh dài trong thế giới thực: tổng hợp, QA, tìm kiếm, mã.

> **LongBench。**Thực sự dài trên nhiệm vụ: tóm tắt, câu hỏi, kiểm tra, mã hóa.

**MRCR (Multi-hop Reasoning over Context).**Điều đó đòi hỏi phải kết nối thông tin giữa nhiều tài liệu.

> **MRCR（上下文多跳推理）。**需要跨多文档连接信息的推理──最难的长上下文测试──

> **【拓展：大语言模型的工程实践】**Từ GPT đến ChatGPT, NLP đã trải qua một quá trình chuyển đổi.
```figure
gx-niah-decay
```

## Hãy xây dựng nó

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) là cấu trúc phổ biến nhất trong ứng dụng AI trong doanh nghiệp hiện tại.

> **【拓展：NLP 的多语言挑战】**Trên toàn cầu có hơn 7000 ngôn ngữ, nhưng nghiên cứu về NLP tập trung chủ yếu vào tiếng Anh và một số ít ngôn ngữ.

## Hãy xây dựng nó.

> **【中文解读】**Bài viết này thông qua mã từ zero thực hiện các thuật toán cốt lõi.

### Bước 1: kiểm tra NIAH đơn giản

```python
def needle_in_haystack(model, context_length, needle, needle_position):
    """Insert needle at position in a long document and test retrieval."""
    haystack = generate_irrelevant_text(context_length)
    full_text = haystack[:needle_position] + f"\n{needle}\n" + haystack[needle_position:]
    question = f"What is the secret fact hidden in the text?"
    response = model(full_text + "\n\n" + question)
    return needle.lower() in response.lower()
```

> **【中文解读】**Bài này sẽ cho thấy cách sử dụng một khuôn khổ đã trưởng thành để nhanh chóng áp dụng công nghệ này.

> **【拓展：Prompt Engineering 与 LLM 应用】**Kỹ thuật nhanh chóng đã trở thành kỹ năng cốt lõi của các kỹ sư NLP.

## Hãy sử dụng nó để thực hiện

> **【中文解读】**Bài viết này tập trung vào cách thức triển khai mô hình cho các sản phẩm có thể sử dụng.

| Benchmark / 基准 | Type / 类型 | Measures / 测量 |
|---------|------|---------|
| NIAH | Synthetic / 合成 | Single-fact retrieval at depth. / 深度单事实检索。 |
| RULER | Synthetic / 合成 | Multi-needle + aggregation. / 多针 + 聚合。 |
| LongBench | Real / 真实 | Practical long-context tasks. / 实用长上下文任务。 |
| MRCR | Synthetic / 合成 | Multi-hop reasoning. / 多跳推理。 |

## Chuyển nó đi.

Cứ như `outputs/skill-long-context-eval.md`- Có thể là:

> 保存为 `outputs/skill-long-context-eval.md`- Có thể là:

```markdown
Given a model claiming long-context support, verify actual performance.
1. Context length to test.
2. Benchmarks to run (NIAH, RULER, LongBench).
3. Minimum acceptable accuracy at target length.
```

## Tập luyện bài tập

1. **Easy.**Tiếp tục NIAH trên một mô hình với 10K và 50K token.**简单。**Trong 10K và 50K token 上运行 NIAH。
2. **Medium.**Xây dựng một thử nghiệm đa kim và đo lường lấy 5 sự thật trong một bối cảnh 100K. / **中等。**构建多针测试──
3. **Hard.**So sánh 3 mô hình trên LongBench. báo cáo mà suy giảm nhanh nhất. / **困难。**Trong LongBench 上比较 3 个模型──

## Từ khóa  Từ khóa nhanh chóng

| Term / 术语 | What it means / 含义 |
|------|-----------------------|
| NIAH（大海捞针） | Insert fact in long text, test retrieval. / 在长文本中插入事实，测试检索。 |
| Context window（上下文窗口） | Maximum input length a model can process. / 模型能处理的最大输入长度。 |
| Multi-hop reasoning（多跳推理） | Connect info across multiple documents. / 跨文档连接信息。 |

## Xem thêm 延伸阅读

- [NIAH original](https://arxiv.org/abs/2404.05460) Đồ đéo trong đống cỏ. / 大海捞针。
- [RULER](https://arxiv.org/abs/2404.02372) mở rộng tiêu chuẩn ngữ cảnh dài. / 扩展长上下文基准。
- [LongBench](https://arxiv.org/abs/2308.14508) thực tế thế giới nhiệm vụ trong bối cảnh dài. / 真实长上下文任务。
