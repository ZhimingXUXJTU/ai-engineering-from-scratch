# Định hướng: WebArena và OSWorld

> WebArena kiểm tra khả năng đại lý web trên bốn ứng dụng tự lưu trữ. OSWorld kiểm tra khả năng đại lý máy tính để bàn trên Ubuntu, Windows, macOS. Khi phát hành (20232024) cả hai đều cho thấy khoảng cách lớn giữa các đại lý tốt nhất trong lớp và con người.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 19 (SWE-bench, GAIA) | **前置知识:** 见原文
**Time:** ~60 minutes | **时间:** 见原文

## Mục tiêu học tập

- Mô tả bốn ứng dụng tự lưu trữ của WebArena và lý do tại sao đánh giá dựa trên thực hiện quan trọng.
- Giải thích tại sao OSWorld sử dụng ảnh chụp màn hình thực của hệ điều hành thay vì API truy cập.
- Hãy nêu tên hai chế độ thất bại chính của OSWorld: GUI và kiến thức hoạt động.
- Tóm lại những gì OSWorld-G và OSWorld-Human thêm vào điểm tham khảo cơ bản.

## Vấn đề  vấn đề giới thiệu

Các đại lý tổng quát có thể gọi công cụ. Họ có thể điều khiển trình duyệt qua 20 nhấp chuột để hoàn thành thanh toán mua sắm? Họ có thể cấu hình một hộp Linux chỉ sử dụng bàn phím và chuột? Đây là câu hỏi WebArena và OSWorld trả lời.

> Thông thường, đại lý có thể điều khiển các công cụ. Nhưng chúng có thể điều khiển trình duyệt hoàn thành 20 lần click để hoàn thành thanh toán mua hàng? chúng có thể chỉ sử dụng bàn phím và chuột để cấu hình một máy Linux? Đó là WebArena và OSWorld phải trả lời câu hỏi.


> **【中文解读】**WebArena và OSWorld  đánh giá Cung cấp trong môi trường thực tế tính toán.

> **{【拓展：WebArena (CMU, 2023) 创建了真实的 Web 环境（电商、论坛、GitLab），A...】}**WebArena (CMU, 2023) 创建真实的 Web 环境(电商、论坛、GitLab),Agent 需要像人类一样浏览和操作。2026年 SOTA 约 35% tỷ lệ thành công,人类约 80%。OSWorld (HKU, 2024) 提供真实的 Ubuntu/Windows/macOS 桌面环境,Agent 需要操作 GUI 完成任务。 tỷ lệ thành công thấp hơn, tốt nhất Agent 约 12%。

>  **【前置】**建议先过:Phase 14·19(SWE-bench/GAIA) 本节是其姐妹篇,专门评估"GUI 操作"能力;以及Phase 14·21(Computer Use Agents) 本节是评估那些代理的"考试题"──理解GUI 操作和工具调用区别(GUI 是像素+点击,工具调用是API+JSON) là chìa khóa──

## Khái niệm cốt lõi

### WebArena (Zhou et al., ICLR 2024)

- 812 nhiệm vụ dài đường dài trên bốn ứng dụng web tự lưu trữ: một trang web mua sắm, một diễn đàn, một công cụ phát triển giống như GitLab, một CMS kinh doanh.
- Thêm các tiện ích: bản đồ, máy tính, scratchpad.
- Đánh giá dựa trên việc thực hiện thông qua APIs phòng tập thể dục  đã đặt hàng, vấn đề đã bị đóng, trang CMS đã được cập nhật?
- Khi phát hành: chất độc GPT-4 tốt nhất đạt thành công 14,41% so với con người 78,24%.

Các bản khung tự lưu trữ quan trọng  điểm chuẩn không nhét bởi vì các ứng dụng mục tiêu được gắn và có thể tái tạo.

> Quadro tự quản lý rất quan trọng vì cơ sở sẽ không được cố định và có thể tái tạo không ổn định vì mục tiêu ứng dụng.

>  **【类比】**WebArena và OSWorld khác biệt như "模拟驾驶" và "真车上路":WebArena là模拟驾驶 bốn ứng dụng web cố định (ecommerce,论坛, v.v.), môi trường hoàn toàn có thể kiểm soát được, giống như trường tiêu chuẩn hóa của trường lái xe; OSWorld là thực车上路 thực tế Ubuntu/Windows/macOS 系统, mỗi phiên bản UI có thể không giống nhau, cũng có thể bật cửa sổ,卡顿, quảng cáo.**关键**: WebArena 测 là "Agent 能不能使用Web", OSWorld 测 là "Agent 能不能使用电脑"

> WebArena và OSWorld là môi trường đánh giá của Agent sử dụng máy tính. WebArena 模拟网页操作, OSWorld 模拟完整桌面环境.

### Các mở rộng

- **VisualWebArena** các nhiệm vụ dựa trên hình ảnh nơi thành công phụ thuộc vào việc giải thích hình ảnh (các bức ảnh màn hình như quan sát hạng nhất).
- **TheAgentCompany**(Dec 2024)  thêm terminal + mã hóa; giống như một môi trường làm việc từ xa thực sự.

### OSWorld (Xie et al., NeurIPS 2024)

- 369 nhiệm vụ máy tính thực sự trên Ubuntu, Windows, macOS.
- Kiểm soát bàn phím và chuột dạng tự do của các ứng dụng thực.
- 1920×1080 ảnh chụp màn hình như quan sát.
- Khi phát hành: mô hình tốt nhất 12,24% so với con người 72,36%.

### Các chế độ thất bại chính

1. **GUI grounding.**Phép đồ thị phần tử Pixel →. Các mô hình vật lộn để định vị các phần tử UI một cách đáng tin cậy trong 1920 × 1080.
2. **Operational knowledge.**Menu nào có cài đặt, cách tắt bàn phím nào, bảng ưu tiên nào.

> ️ **【易错点】**Sử dụng DOM hoặc API truy cập chạy OSWorld và báo cáo "高分"**后果**分数虚高且无意义  OSWorld  thiết kế mục đích là测**视觉 grounding**(像素到元素的映射), sử dụng DOM API như vượt qua các thách thức cốt lõi.**一行修复**: trên OSWorld 上 chỉ có thể sử dụng chụp màn hình như nhập thông tin của đại lý, nếu không không tính" trên OSWorld 上 đánh giá"―― nếu bạn muốn kiểm tra đại lý dựa trên DOM, xin hãy sử dụng WebArena hoặc Mind2Web。

### Tiếp tục

- **OSWorld-G** 564 mẫu bộ ghép đất + bộ huấn luyện Jedi.
- **OSWorld-Human** các quỹ đạo hành động vàng được chọn bằng tay.

### Tại sao điều này quan trọng

Claude sử dụng máy tính, OpenAI CUA, Gemini 2.5 sử dụng máy tính (Dạy học 21) tất cả đào tạo trên khối lượng công việc được định hình bởi WebArena và OSWorld.

> Claude 计算机使用、OpenAI CUA、Gemini 2.5 计算机使用(第 21 课) đều được đào tạo trên WebArena và OSWorld 塑造的工作负载──基准是目标;生产模型是交付的答案──

> WebArena và OSWorld là môi trường đánh giá của Agent sử dụng máy tính. WebArena 模拟网页操作, OSWorld 模拟完整桌面环境.

### Khi đánh giá so sánh đi sai

- **Screenshot-only evals.**OSWorld được điều khiển bằng ảnh chụp màn hình; đánh giá một đại lý sử dụng DOM hoặc API truy cập trên OSWorld bỏ lỡ thách thức đặt đất.
- **Ignoring trajectory length.**Chỉ đạt tỷ lệ thành công bỏ lỡ 1.4-2.7x không hiệu quả bước OSWorld-Human bề mặt.
- **Stale self-hosted apps.**Các ứng dụng của WebArena pin các phiên bản cụ thể; cập nhật mà không cần tái điều chỉnh phá vỡ khả năng so sánh.

> 🤔 **【困惑】**Q: WebArena 上 SOTA 才 35%,OSWorld 才 12%, đây không phải là một biểu hiện của máy tính sử dụng đại lý 现在不能用吗 A: 不能如此看;;基准测试的任务是"最难的那批"长程(20+步) 多模态、需要精确的基础;;**针对性优化**Các trang web nhất định, dòng nhiệm vụ rõ ràng, người dùng đang đi trên đường.**结论**Kiểm tra cơ bản là "capacity upper limit", sản xuất sử dụng "khác đặc biệt", hai thứ không thể thay đổi trực tiếp.

> **仅截图评估。**OSWorld là một hệ thống điều khiển; trong OSWorld để đánh giá sử dụng DOM hoặc không có rào cản API của Đại lý sẽ gặp phải các thách thức liên kết.
> **忽略轨迹长度。**Chỉ đánh giá tỷ lệ thành công sẽ vượt qua OSWorld-Human  tiết lộ 1.4-2.7 lần 步骤低效──
> **过时的自托管应用。**Các ứng dụng của WebArena đã cố định một phiên bản cụ thể; không tái lập kế hoạch về việc cập nhật sẽ phá hủy khả năng tương thích.

## Hãy xây dựng nó.
```figure
ae-agent-human-gap
```

## Hãy xây dựng nó

`code/main.py`thực hiện một dây thắt máy web đồ chơi:

> `code/main.py`实现一个玩具 Web Agent 测试工具:

> WebArena và OSWorld là môi trường đánh giá của Agent sử dụng máy tính. WebArena 模拟网页操作, OSWorld 模拟完整桌面环境.

- Một máy trạng thái "app mua sắm" tối thiểu: list_items, add_to_cart, checkout.
- Các quỹ đạo vàng cho 3 nhiệm vụ.
- Một nhân viên có kịch bản cố gắng mỗi nhiệm vụ.
- Đánh giá dựa trên thực hiện (điểm tra trạng thái) và chỉ số hiệu quả quỹ đạo (giải pháp so với vàng).

Đi đi.

```
python3 code/main.py
```

Kết quả: tỷ lệ thành công và hiệu quả đường mòn mỗi nhiệm vụ, phản ánh phương pháp của OSWorld-Human.

> 输出: tỷ lệ thành công và hiệu quả của nhiệm vụ, phản ánh phương pháp của OSWorld-Human.

> WebArena và OSWorld là môi trường đánh giá của Agent sử dụng máy tính. WebArena 模拟网页操作, OSWorld 模拟完整桌面环境.

## Hãy sử dụng nó để thực hiện

- **WebArena Verified**tự lưu trữ trên một cluster nội bộ để đánh giá liên tục.
- **OSWorld**trong một đội máy tính ảo cho các đại lý máy tính để bàn.
- **Computer-use agents**(Dân học 21) Claude, OpenAI CUA, Gemini đều được đào tạo về những khối lượng công việc như thế này.
- **Your own product flows** bắt được quỹ đạo vàng cho 20 nhiệm vụ hàng đầu của bạn; chạy các đại lý chống lại chúng hàng tuần.

## Chuyển nó đi.

`outputs/skill-web-desktop-harness.md`xây dựng một hệ thống web/desktop với các metric evalu và trajectory efficiency dựa trên thực hiện.

> `outputs/skill-web-desktop-harness.md`Xây dựng một công cụ kiểm tra Web / Desktop Agent, với các chỉ số hiệu quả đánh giá và quỹ đạo dựa trên thực hiện.

> WebArena và OSWorld là môi trường đánh giá của Agent sử dụng máy tính. WebArena 模拟网页操作, OSWorld 模拟完整桌面环境.

## Tập luyện bài tập

1. Cải đệm đồ chơi với một ứng dụng thứ hai (một diễn đàn).
  Trung ngữ翻译:思考并实践此练习。
2. Thêm báo cáo hiệu quả quỹ đạo cho mỗi nhiệm vụ.
  Trung ngữ翻译:思考并实践此练习。
3. Thực hiện một công cụ "đánh nhiễu"  một quỹ đạo vàng không bao giờ sử dụng.
  Trung ngữ翻译:思考并实践此练习。
4. Đọc OSWorld-G. Làm thế nào bạn phân biệt thất bại về việc đặt đất với thất bại về kế hoạch trong các đánh giá của riêng bạn?
  Trung ngữ翻译:思考并实践此练习。
5. Đọc các ứng dụng của WebArena README. Khi bạn nâng cấp một trong các phiên bản ứng dụng gắn kết, bạn sẽ bị hỏng gì?
  Trung ngữ翻译:思考并实践此练习。

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| WebArena | "Web agent benchmark" | 812 tasks across 4 self-hosted apps; gym-style evaluation |  |
| VisualWebArena | "Visual WebArena" | Visually grounded WebArena; screenshots are observations |  |
| OSWorld | "Desktop agent benchmark" | 369 tasks on real Ubuntu/Windows/macOS |  |
| GUI grounding | "Pixel-to-element mapping" | Model localizing UI elements in 1920x1080 |  |
| Operational knowledge | "OS know-how" | Which menu, which shortcut, which preference pane |  |
| OSWorld-G | "Grounding suite" | 564 grounding-only samples + training set |  |
| OSWorld-Human | "Gold trajectories" | Manual expert action sequences to measure efficiency |  |
| Trajectory efficiency | "Steps over gold" | Agent step count divided by human minimum |  |

## Xem thêm 延伸阅读

- [Zhou et al., WebArena (arXiv:2307.13854)](https://arxiv.org/abs/2307.13854) Định nghĩa web bốn ứng dụng
  Trung ngữ: 翻译:见原文.
- [Xie et al., OSWorld (arXiv:2404.07972)](https://arxiv.org/abs/2404.07972) Định nghĩa bảng điều khiển trên máy tính để bàn
  Trung ngữ: 翻译:见原文.
- [Anthropic, Introducing computer use](https://www.anthropic.com/news/3-5-models-and-computer-use) Khả năng hình dạng chuẩn của Claude
  Trung ngữ: 翻译:见原文.
- [OpenAI, Computer-Using Agent](https://openai.com/index/computer-using-agent/) Số OSWorld và WebArena
  Trung ngữ: 翻译:见原文.
