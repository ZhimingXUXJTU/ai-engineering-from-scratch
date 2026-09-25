# Hướng dẫn tình trạng đối thoại

> "Tôi muốn một nhà hàng rẻ ở phía bắc... thực sự làm nó vừa phải... và thêm tiếng Ý". 3 lượt, 3 cập nhật trạng thái. DST giữ cho giá trị khe cắm dict đồng bộ để đặt phòng hoạt động.
> "我要北边一家便宜的餐厅......改成中等价位......加意菜──" 三轮对话,三次状态更新──DST 保持槽位-值字典同步,让预订成功──

> **【中文解读】**跟踪对话中的状态变化 (số vị trí- giá trị đối với), đảm bảo nhiều vòng đàm thoại phù hợp.

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 17 (Chatbots), Phase 5 · 07 (POS & Parsing) | **前置知识:** Phase 5 · 17（聊天机器人），Phase 5 · 07（POS 与解析）
**Time:** ~45 minutes | **时间:** ~45 分钟

## Vấn đề  vấn đề giới thiệu

Nếu bạn sai một khe cắm và hệ thống đặt phòng cho một nhà hàng sai, tính phí thẻ sai hoặc lên lịch một ngày sai. DST là sự khác biệt giữa một chatbot có cảm giác như một truy vấn cơ sở dữ liệu và một chatbot có cảm giác như một cuộc trò chuyện.

> Một cái cỗ máy làm sai, hệ thống đặt hàng sai, đặt hàng sai, đặt hàng sai, đặt hàng sai, đặt hàng sai, đặt hàng sai, đặt hàng sai, đặt hàng sai, đặt hàng sai, đặt hàng sai, đặt hàng sai, đặt hàng sai, đặt hàng sai, đặt hàng sai, đặt hàng sai, đặt hàng sai, đặt hàng sai, đặt hàng sai, đặt hàng sai, đặt hàng sai, đặt hàng sai, đặt hàng sai, đặt hàng sai, đặt hàng sai, đặt hàng sai, đặt hàng sai, đặt hàng sai, đặt hàng sai, đặt hàng sai, đặt hàng sai, đặt hàng sai, đặt hàng sai, đặt hàng sai, đặt hàng sai, đặt hàng sai, đặt hàng sai, đặt hàng sai, đặt hàng sai, đặt hàng sai, đặt hàng sai, đặt hàng sai, đặt hàng sai, đặt hàng, đặt hàng, đặt hàng, đặt hàng, đặt hàng, đặt hàng, đặt hàng, đặt hàng, đặt hàng, đặt hàng, đặt hàng, đặt hàng, đặt hàng, đặt hàng, đặt hàng, đặt hàng, đặt hàng, đặt hàng, đặt hàng, đặt hàng, đặt hàng, đặt hàng, đặt hàng, đặt hàng, đặt hàng, đặt hàng, đặt hàng, đặt hàng, đặt hàng, đặt hàng, đặt hàng, đặt hàng, đặt hàng, đặt hàng, đặt hàng, đặt hàng, đặt hàng, đặt hàng, đặt hàng, đặt hàng, đặt hàng, đặt hàng, đặt hàng, đặt hàng, đặt hàng, đặt hàng, đặt hàng, đặt hàng, đặt hàng, đặt hàng, đặt hàng, đặt hàng, đặt hàng, đặt hàng, đặt hàng, hoặc đặt hàng, đặt hàng, hoặc đặt hàng, đặt hàng, hoặc đặt hàng, đặt hàng, hoặc đặt hàng, hoặc đặt hàng, đặt hàng, hoặc đặt hàng.

> **【中文解读】**Câu hỏi được đặt ra trong phần này là: làm thế nào để hiểu và áp dụng đúng công nghệ này trong công trình thực tế.

Tại sao nó vẫn quan trọng trong năm 2026 mặc dù LLM: LLM xử lý trạng thái đơn giản ngầm nhưng thất bại trong các bản cập nhật đa khe phức tạp, các vụ sửa chữa ("ngợi, làm cho nó là ngày 7 chứ không phải ngày 8 và thay đổi thời gian thành 3 giờ chiều"), và trạng thái kiên trì trong các phiên dài. DST rõ ràng vẫn là câu trả lời sản xuất cho các hệ thống định hướng nhiệm vụ.

> Năm 2026 tại sao vẫn quan trọng:LLM 隐式处理简单状态但在复杂多槽更新、纠正级联("等等等,改成7号不是8号,时间改成下午3点") và长会话的持久状态失败;;显然DST 仍然是任务导向系统的生产答案;;

## Khái niệm cốt lõi

> **【中文解读】**本节介绍核心概念和理论基础──

**Dialogue state.**Một bộ các cặp (đường khe, giá trị) ghi lại những gì hệ thống biết về mục tiêu của người dùng tại mỗi lượt. Ví dụ: {nấu ăn: Ý, giá: trung bình, khu vực: bắc}.

> **对话状态。**Mỗi vòng cuộc hội thoại trong một nhóm (槽位, 值) đối với, nắm bắt hệ thống đối với mục tiêu của người dùng.

**State update.**Mỗi lần, cập nhật trạng thái dựa trên phát biểu người dùng mới. Ba hoạt động: đặt, cập nhật, xóa.

> **状态更新。**Mỗi vòng trò chuyện dựa trên trạng thái mới của người dùng.

**Belief state.**Phân bố xác suất trên các giá trị khe cắm có thể xảy ra. hữu ích khi người dùng không rõ ràng ("một nhà hàng" → nhà bếp = Không, nhưng niềm tin cho thấy Ý = 0,3, Trung Quốc = 0,2, ...).

> **信念状态。**Có thể phân bố tỷ lệ sử dụng của người dùng.

> **【拓展：大语言模型的工程实践】**Từ GPT đến ChatGPT, NLP đã trải qua một quá trình chuyển đổi.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) là cấu trúc phổ biến nhất trong ứng dụng AI trong doanh nghiệp hiện tại.
```figure
n5-slot-tracker
```

## Hãy xây dựng nó

> **【拓展：NLP 的多语言挑战】**Trên toàn cầu có hơn 7000 ngôn ngữ, nhưng nghiên cứu về NLP tập trung chủ yếu vào tiếng Anh và một số ít ngôn ngữ.

## Hãy xây dựng nó.

> **【中文解读】**Bài viết này thông qua mã từ zero thực hiện các thuật toán cốt lõi.

### Bước 1: Trình theo dõi trạng thái giá trị khe

```python
class DialogueStateTracker:
    def __init__(self, slots):
        self.state = {slot: None for slot in slots}
        self.history = []

    def update(self, slot_values):
        for slot, value in slot_values.items():
            if slot in self.state:
                self.state[slot] = value
        self.history.append(dict(self.state))

    def get_missing_slots(self):
        return [s for s, v in self.state.items() if v is None]

    def is_complete(self):
        return all(v is not None for v in self.state.values())


tracker = DialogueStateTracker(["cuisine", "price", "area", "party_size"])
tracker.update({"cuisine": "Italian", "area": "north"})
print(tracker.get_missing_slots())  # ['price', 'party_size']
print(tracker.is_complete())  # False
```

### Bước 2: Cập nhật trạng thái dựa trên LLM

```python
def llm_state_update(dialogue_history, current_state, llm):
    prompt = f"""Given the dialogue history and current state, extract slot updates.

Current state: {current_state}
Dialogue: {dialogue_history[-1]}

Output JSON of updated slots."""
    return llm(prompt)
```

> **【中文解读】**Bài này sẽ cho thấy cách sử dụng một khuôn khổ đã trưởng thành để nhanh chóng áp dụng công nghệ này.

> **【拓展：Prompt Engineering 与 LLM 应用】**Kỹ thuật nhanh chóng đã trở thành kỹ năng cốt lõi của các kỹ sư NLP.

## Hãy sử dụng nó để thực hiện

> **【中文解读】**Bài viết này tập trung vào cách thức triển khai mô hình cho các sản phẩm có thể sử dụng.

- **Rule-based DST.**Lấp đầy khe với regex + khai thác thực thể. / 基于规则的 DST──正则 + 实体提取──快速、可预测──
- **Neural DST.**Đào tạo trên MultiWOZ hoặc bộ dữ liệu tương tự.
- **LLM-based DST.**Đăng tiến chương trình học để lấy thông tin cập nhật về trạng thái.
- **Hybrid.**LLM cho việc khai thác + dựa trên quy tắc để xác nhận. khuyến nghị sản xuất. / 混合──LLM 提取 + 规则验证──生产推──

## Chuyển nó đi.

Cứ như `outputs/skill-dst-builder.md`- Có thể là:

> 保存为 `outputs/skill-dst-builder.md`- Có thể là:

```markdown
Given a task-oriented dialogue system, design DST.
1. Slots to track.
2. State update method (rule, neural, LLM).
3. Confirmation and correction handling.
```

## Tập luyện bài tập

1. **Easy.**Xây dựng một DST dựa trên quy tắc cho một hệ thống đặt phòng nhà hàng. / **简单。**为餐厅预订系统构建基于规则的DST──
2. **Medium.**Thêm LLM dựa trên khai thác nhà nước. So sánh với dựa trên quy tắc. / **中等。**添加基于LLM的状态提取──
3. **Hard.**Đánh giá DST trên MultiWOZ. Báo cáo chính xác mục tiêu chung. / **困难。**Trong nhiều WOZ 上 đánh giá DST

## Từ khóa  Từ khóa nhanh chóng

| Term / 术语 | What it means / 含义 |
|------|-----------------------|
| Dialogue state（对话状态） | Current (slot, value) pairs. / 当前槽位-值对。 |
| Slot filling（槽位填充） | Extracting values for predefined slots. / 为预定义槽位提取值。 |
| Belief state（信念状态） | Probability distribution over slot values. / 槽位值的概率分布。 |
| MultiWOZ | Multi-domain dialogue dataset. / 多领域对话数据集。 |

## Xem thêm 延伸阅读

- [MultiWOZ](https://arxiv.org/abs/1810.00278) tập hợp dữ liệu DST tiêu chuẩn. / 标准 DST 数据集──
- [TRADE](https://arxiv.org/abs/1810.00278) chuyển giao trạng thái đối thoại theo dõi. / 可迁移对话状态跟踪器──
- [SimpleTOD](https://arxiv.org/abs/2005.00796) đơn giản DST đầu đến cuối. / 简单端到端 DST。
