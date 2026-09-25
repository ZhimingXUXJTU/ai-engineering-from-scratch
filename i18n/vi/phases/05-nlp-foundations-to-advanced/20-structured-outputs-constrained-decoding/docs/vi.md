# Structured Outputs & Constrained Decoding                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  

> Khi bạn làm việc với một người khác, bạn sẽ phải làm việc với người khác để làm việc với họ.
> 让LLM 输出 JSON──大多数时候能得到 JSON──在生产中,"大多数"就是问题──约束解码通过在采样前编辑逻辑将"大多数"变成"总是"──

> **【中文解读】**让LLM 输出结构化数据如JSON、SQL。

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 19 (Subword Tokenization) | **前置知识:** Phase 5 · 19（子词分词）
**Time:** ~60 minutes | **时间:** ~60 分钟

## Vấn đề  vấn đề giới thiệu

Tạo dạng tự do không phải là hợp đồng. Nó là một đề xuất. Bạn yêu cầu JSON, bạn nhận được một chuỗi hình dạng JSON với một dấu ngoặc sau, một backtick bổ sung, hoặc một khóa có tên bằng tiếng Đức. Mỗi trình phân tích dòng chảy xuống đều bị phá vỡ. Bạn yêu cầu một truy vấn SQL, bạn nhận được một cái tên cột ảo giác. Trong sản xuất, những lỗi này không phải là lỗi  chúng là sự cố.

> tự do hình thức tạo không phải là thỏa thuận, là đề nghị. Bạn yêu cầu JSON, nhận được một带尾逗号, số dư phản引号, hoặc tên của một chữ cái.

> **【中文解读】**Câu hỏi được đặt ra trong phần này là: làm thế nào để hiểu và áp dụng đúng công nghệ này trong công trình thực tế.

Ba tầng tồn tại vào năm 2026.

> Năm 2026 có ba cấp giải pháp:

1. **Prompting.**Hãy hỏi một cách tốt. "Vậy chỉ trả lại đối tượng JSON". Nó hoạt động khoảng 85-95% thời gian. Không thành công trong các trường hợp cạnh, đầu ra dài và đầu vào đối thủ. / **提示。**Ưu điểm tốt: " chỉ trả lại JSON đối tượng. " Ưu điểm 85-95% thời gian hợp lệ.
2. **Constrained decoding.**Mùi logit mã thông báo tiếp theo không hợp lệ tại mỗi bước thế hệ để đầu ra luôn phù hợp với một sơ đồ (JSON sơ đồ, regex, ngữ pháp không liên quan).**约束解码。**Trong mỗi bước tạo ngăn chặn các log log của token tiếp theo không hiệu quả, để output luôn phù hợp với mô hình.
3. **Tool/function calling.**Kết quả kết cấu thông qua giao diện gọi công cụ bản địa của mô hình. mô hình phát ra một đối tượng JSON trực tiếp, không phải như văn bản.**工具/函数调用。**通过模型原生工具调用接口的结构化输出──最佳延迟,最佳可靠性,但模型特定──

## Khái niệm cốt lõi

> **【中文解读】**Bài viết này giới thiệu các khái niệm và lý thuyết cốt lõi.

**Logit masking.**Tại mỗi bước tạo, mô hình tạo ra phân phối xác suất trên từ vựng. Khóa mã hạn chế tính toán bộ các token tiếp theo hợp lệ (giả sử sơ đồ và những gì đã được tạo ra cho đến nay) và đặt tất cả các logit khác là -inf trước softmax. mô hình chỉ có thể chọn từ các token hợp lệ.

> **Logit 屏蔽。**Trong mỗi bước tạo, mô hình trên biểu đồ tạo ra tỷ lệ phân bố.

**JSON schema constraints.**Đối với đầu ra JSON, hạn chế áp dụng: các vòng mở phù hợp với vòng đóng, các phím được trích dẫn chuỗi, các giá trị phù hợp với các loại được tuyên bố của chúng, các trường yêu cầu hiện diện, không có các trường bổ sung ngoài sơ đồ. Đây là một hạn chế ngữ pháp không có ngữ cảnh, được tính theo từng bước.

> **JSON 模式约束。**Đối với JSON 输出,约束强制:开闭括号匹配、键是带引号字符串、值匹配声明类型、必填字段存在、无模式外额外字段──这是一个上下文无关语法约束,增量计算──

> **【拓展：大语言模型的工程实践】**Từ GPT đến ChatGPT, NLP đã trải qua sự chuyển đổi từ "mỗi nhiệm vụ đào tạo một mô hình" đến "một mô hình giải quyết tất cả các nhiệm vụ". Trong công trình thực tế, việc triển khai LLM cần phải xem xét các vấn đề như: giới hạn token, trì hoãn, chi phí, kiểm tra an toàn, và các vấn đề khác.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) là cấu trúc phổ biến nhất trong ứng dụng AI của doanh nghiệp hiện tại: sẽ truy vấn người dùng trước tiên truy vấn các đoạn tài liệu liên quan, tiếp tục truy vấn kết quả như trên dưới đây cho LLM 生成答案──

> **【拓展：NLP 的多语言挑战】**Trên toàn cầu có hơn 7000 ngôn ngữ, nhưng nghiên cứu về NLP tập trung chủ yếu vào tiếng Anh và một số ít ngôn ngữ.

## Hãy xây dựng nó.
```figure
constrained-decoder
```

## Hãy xây dựng nó

> **【中文解读】**本节通过代码实现核心算法从零――这种" từ đầu"的方式能帮助理解框架背后的原理,遇到问题时不会被黑盒困住――

### Bước 1: che giấu logit đơn giản

```python
import json
import re


def mask_logits(logits, valid_token_ids):
    """Set invalid token logits to -inf."""
    mask = torch.full_like(logits, float('-inf'))
    mask[valid_token_ids] = logits[valid_token_ids]
    return mask
```

Ý tưởng cốt lõi: ở mỗi bước, chỉ có một bộ phận của các token là hợp lệ.

> 核心洞察: trong mỗi bước, chỉ có token 子集是有效的──高效计算该子集是工程挑战──

### Bước 2: Kiểm chứng sơ đồ JSON trong quá trình tạo

```python
import jsonschema

schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "integer", "minimum": 0},
    },
    "required": ["name", "age"],
}

def validate_json_output(text, schema):
    try:
        data = json.loads(text)
        jsonschema.validate(data, schema)
        return True, data
    except (json.JSONDecodeError, jsonschema.ValidationError) as e:
        return False, str(e)
```

### Bước 3: sử dụng LM Format Enforcer

```python
from lmformatenforcer import JsonSchemaParser, generate_enforced

parser = JsonSchemaParser(schema)
# Use with any Hugging Face model's generate method
# result = generate_enforced(model, tokenizer, parser, prompt)
```

> **【中文解读】**Bài này sẽ cho thấy cách sử dụng một khuôn khổ đã phát triển để nhanh chóng áp dụng công nghệ này. Trong các dự án thực tế, ưu tiên sử dụng khuôn khổ đã được chứng minh để thực hiện.

> **【拓展：Prompt Engineering 与 LLM 应用】**Kỹ thuật nhanh chóng đã trở thành kỹ năng cốt lõi của các kỹ sư NLP. Từ Zero-shot đến Few-shot, từ Chain-of-Thought đến ReAct, các chiến lược khác nhau áp dụng cho các tình huống khác nhau. Trong các dự án thực tế, thiết kế của System提示(System Prompt) ảnh hưởng trực tiếp đến sự ổn định và chất lượng sản xuất của ứng dụng LLM.

## Hãy sử dụng nó để thực hiện

> **【中文解读】**Phần này tập trung vào cách phân phối mô hình như một sản phẩm có thể sử dụng.

Các lựa chọn sản xuất năm 2026:

> Các lựa chọn sản xuất năm 2026:

| Approach / 方案 | Reliability / 可靠性 | Latency cost / 延迟成本 | Best for / 最适合 |
|---------|------------|-------------|---------|
| Prompting / 提示 | ~85-95% / 约 85-95% | None / 无 | Prototypes, non-critical paths / 原型、非关键路径 |
| Constrained decoding / 约束解码 | 100% / 100% | +10-30% / 加 10-30% | Production APIs / 生产 API |
| Tool calling / 工具调用 | ~99.9% / 约 99.9% | Lowest / 最低 | Model-native workflows / 模型原生工作流 |

## Chuyển nó đi.

Cứ như `outputs/prompt-structured-output.md`- Có thể là:

> 保存为 `outputs/prompt-structured-output.md`- Có thể là:

```markdown
Given an LLM output that must be structured (JSON, SQL, etc.), pick the right approach and implement it.
1. Schema definition. JSON Schema, regex, or grammar.
2. Enforcement method. Prompting, constrained decoding, or tool calling.
3. Fallback plan. What happens when the output still fails validation.
```

> **【中文解读】**练题按照 Easy/Medium/Hard 三个难度递进;;建议至少完成 级别的题目, 级别适合深入研究或面试准备;;

## Tập luyện bài tập

1. **Easy.**Xây dựng một máy trích xuất JSON chỉ cần thời gian. đo tỷ lệ thành công trên 100 cuộc gọi LLM. / **简单。**构建纯提示的 JSON 提取器──测量 100次 LLM 调用成功率──
2. **Medium.**Thực hiện mã hóa hạn chế cho một sơ đồ JSON đơn giản bằng cách sử dụng logit masking. / **中等。**Sử dụng logit 屏蔽为简单 JSON 模式实现约束解码──
3. **Hard.**So sánh mã hóa hạn chế so với công cụ yêu cầu tải trọng công việc sản xuất. báo cáo độ trễ, độ tin cậy và chi phí. / **困难。**Trong sản xuất tải trọng công việc so sánh các quy mô giải mã và công cụ sử dụng.

> **【中文解读】**Trong 术语表中的"Những gì mọi người nói" vs "Những gì nó thực sự có nghĩa" 区分日常口语和精确技术含义── 在团队协作中,统一术语定义可以避免大量沟通误解──

## Từ khóa  Từ khóa nhanh chóng

| Term / 术语 | What people say / 人们常说的 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| Constrained decoding（约束解码） | Force valid output / 强制有效输出 | Mask invalid logits at each step. / 每步屏蔽无效 logits。 |
| Logit masking（Logit 屏蔽） | Block bad tokens / 阻止坏 token | Set invalid token logits to -inf before softmax. / softmax 前将无效 token logits 设为 -inf。 |
| JSON Schema | JSON validation rules / JSON 验证规则 | Declarative schema for validating JSON structure and types. / 验证 JSON 结构和类型的声明式模式。 |
| Tool calling（工具调用） | Function calling / 函数调用 | Model emits structured arguments directly via native interface. / 模型通过原生接口直接发出结构化参数。 |

> **【中文解读】**延伸阅读 cung cấp các nguồn chất lượng cao cho việc học sâu. Những bài báo và giảng dạy này là tài liệu tham khảo cổ điển trong lĩnh vực này, phù hợp với những người đọc cần hiểu sâu hơn.

## Xem thêm 延伸阅读

- [LM Format Enforcer](https://github.com/noamgat/lm-format-enforcer) sản xuất hạn chế thư viện giải mã. / 生产级约束解码库。
- [Outlines](https://github.com/dottxt-ai/outlines) cấu trúc tạo với regex/JSON/CFG. / 带 regex/JSON/CFG 的结构化生成──
- [JSON Schema specification](https://json-schema.org/) tiêu chuẩn cho xác nhận JSON. / JSON 验证标准。
