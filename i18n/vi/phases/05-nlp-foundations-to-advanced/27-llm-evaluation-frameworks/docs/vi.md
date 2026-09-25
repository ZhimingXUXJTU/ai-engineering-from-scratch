# Đánh giá LLM  RAGAS, DeepEval, G-Eval  LLM  đánh giá  RAGAS  DeepEval

> Sự phù hợp chính xác và F1 không có sự tương đương ngữ nghĩa. Phân tích của con người không có quy mô. LLM-as-judge là câu trả lời sản xuất  với đủ hiệu chuẩn để tin vào số.
> 精确匹配和 F1 捕捉不到语义等价――đánh giá nhân tạo không thể mở rộng――LLM 作为评审是生产答案经过足够校准可以信任这个数字――

> **【中文解读】** đánh giá chất lượng sinh sản LLM, bao gồm RAG 效果──RAGAS、DeepEval、G-Eval là khuôn khổ chính thức──

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 23 (Chunking), Phase 5 · 14 (IR & Search) | **前置知识:** Phase 5 · 23（分块），Phase 5 · 14（信息检索）
**Time:** ~60 minutes | **时间:** ~60 分钟

## Vấn đề  vấn đề giới thiệu

Hệ thống RAG của bạn trả lời: "29 tháng 6 năm 2007". Câu trả lời tham khảo nói: "29 tháng 6 năm 2007". Sự phù hợp chính xác nói sai. BLEU nói một phần. Một con người nói đúng. Bạn cần một số liệu phù hợp với con người, cân bằng với hàng ngàn kết quả, và chi phí ít hơn so với ghi chú của con người.

> Bạn của RAG 系统 trả lời:"29 tháng 6 năm 2007"."" 参考答案是:"29 tháng 6 năm 2007"."" 精确匹配说错了。BLEU 说部分对──人类说正确──你需要一个与人类一致的量度,可扩展到数千输出,且成本低于人工标签──

> **【中文解读】**Câu hỏi được đặt ra trong phần này là: làm thế nào để hiểu và áp dụng đúng công nghệ này trong công trình thực tế.

Bây giờ nhân bằng 10.000 trường hợp thử nghiệm. nhân lần lần nữa bằng mỗi bản cập nhật mô hình bạn muốn gửi. Thử nghiệm con người không có quy mô. Bạn cần các số liệu tự động tương quan với phán đoán con người ở r ≥ 0,85.

> Bây giờ nhân bằng 10.000 thí nghiệm thử nghiệm.

## Khái niệm cốt lõi

> **【中文解读】**本节介绍核心概念和理论基础──

2026 có ba khung có chủ quyền về vấn đề này.

> Năm 2026 có ba khung thống trị vấn đề này.

**RAGAS.**Đánh giá RAG. Đánh giá thu hồi + sản xuất chung. Tỷ lệ: trung thực, liên quan đến câu trả lời, độ chính xác trong bối cảnh, thu hồi bối cảnh. Tỷ lệ đánh giá RAG.

> **RAGAS。**RAG  đánh giá. 联合评估检索和生成. 标志: trung thực. 答案相关性. 上下文精确率. 上下文召回率.

**DeepEval.**Khung khung kiểm tra đơn vị cho kết quả LLM. Các số liệu: đáp ứng phù hợp, trung thực, thiên vị, độc tính.

> **DeepEval。**LLM 输出单元测试框架──指标:答案相关性、忠诚度、偏见、毒性──与 pytest 集成──
```figure
n5-judge-gauge
```

## Hãy xây dựng nó

**G-Eval.**- Dòng tư tưởng thúc đẩy tạo ra các tiêu chí đánh giá, sau đó ghi kết quả.

> **G-Eval。**Sử dụng tư tưởng để tạo ra các tiêu chuẩn đánh giá, sau đó đánh giá và đưa ra các kết quả.

> **【拓展：大语言模型的工程实践】**Từ GPT đến ChatGPT, NLP đã trải qua một quá trình chuyển đổi.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) là cấu trúc phổ biến nhất trong ứng dụng AI trong doanh nghiệp hiện tại.

> **【拓展：NLP 的多语言挑战】**Trên toàn cầu có hơn 7000 ngôn ngữ, nhưng nghiên cứu về NLP tập trung chủ yếu vào tiếng Anh và một số ít ngôn ngữ.

## Hãy xây dựng nó.

> **【中文解读】**Bài viết này thông qua mã từ zero thực hiện các thuật toán cốt lõi.

```python
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision

# Evaluate RAG pipeline
results = evaluate(
    dataset=rag_dataset,
    metrics=[faithfulness, answer_relevancy, context_precision],
    llm=judge_llm,
    embeddings=embed_model,
)
print(results)
```

```python
from deepeval import assert_test
from deepeval.metrics import FaithfulnessMetric

metric = FaithfulnessMetric(threshold=0.7, model="gpt-4")
assert_test(test_case, [metric])
```

> **【中文解读】**Bài này sẽ cho thấy cách sử dụng một khuôn khổ đã trưởng thành để nhanh chóng áp dụng công nghệ này.

> **【拓展：Prompt Engineering 与 LLM 应用】**Kỹ thuật nhanh chóng đã trở thành kỹ năng cốt lõi của các kỹ sư NLP.

## Hãy sử dụng nó để thực hiện

> **【中文解读】**Bài viết này tập trung vào cách thức triển khai mô hình cho các sản phẩm có thể sử dụng.

| Framework / 框架 | Focus / 重点 | Best for / 最适合 |
|---------|--------|---------|
| RAGAS | RAG evaluation / RAG 评估 | Retrieval + generation / 检索 + 生成 |
| DeepEval | Unit testing / 单元测试 | CI/CD integration / CI/CD 集成 |
| G-Eval | Research / 研究 | Custom metrics / 自定义指标 |

## Chuyển nó đi.

Cứ như `outputs/skill-llm-eval.md`- Có thể là:

> 保存为 `outputs/skill-llm-eval.md`- Có thể là:

```markdown
Given an LLM application (chatbot, RAG, agent), design evaluation pipeline.
1. Framework (RAGAS, DeepEval, G-Eval).
2. Metrics to track.
3. Calibration against human labels.
```

## Tập luyện bài tập

1. **Easy.**Đánh giá một đường ống RAG đơn giản với RAGAS. / **简单。**Sử dụng RAGAS  đánh giá đơn giản RAG 流水线。
2. **Medium.**Xây dựng một bộ thử nghiệm DeepEval cho chatbot.**中等。**为聊天机器人构建 DeepEval 测试套件──
3. **Hard.**Định so sánh LLM như một thẩm phán với 200 nhãn của con người.**困难。**Sử dụng 200 个体类标签校准 LLM 评审――报告相关性――

## Từ khóa  Từ khóa nhanh chóng

| Term / 术语 | What it means / 含义 |
|------|-----------------------|
| RAGAS | RAG evaluation framework. / RAG 评估框架。 |
| Faithfulness（忠实度） | Answer is supported by context. / 答案有上下文支持。 |
| LLM-as-judge | LLM evaluates other LLM outputs. / LLM 评估其他 LLM 输出。 |

## Xem thêm 延伸阅读

- [RAGAS](https://docs.ragas.io/) Quadro đánh giá RAG. / RAG 评估框架──
- [DeepEval](https://docs.confident-ai.com/) LLM test unit. / LLM 单元测试。
- [G-Eval](https://arxiv.org/abs/2303.16634) đánh giá chuỗi suy nghĩ. / 思维链评估。
