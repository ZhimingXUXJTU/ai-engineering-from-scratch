# LLaVA-OneVision: Một hình ảnh, nhiều hình ảnh, video trong một mô hình

> Trước LLaVA-OneVision (Li et al., tháng 8 năm 2024) thế giới VLM mở có dòng dõi riêng biệt: LLaVA-1.5 cho hình ảnh đơn, các mô hình hình ảnh đa như Mantis và VILA, các mô hình video như Video-LLaVA và Video-LLaMA. Mỗi người đều giành được điểm chuẩn của mình và thất bại ở những người khác. LLaVA-OneVision lập luận rằng một chương trình giảng dạy duy nhất có thể đào tạo một mô hình để thống trị cả ba kịch bản, và rằng các hiệu ứng chuyển giao nhiệm vụ mới nổi (nghệ năng hình ảnh duy nhất được xuất khẩu sang video, lý luận nhiều hình ảnh được xuất khẩu sang hình ảnh duy nhất) vượt qua tổng số các chuyên gia. Công thức này rất đơn giản: một ngân sách biểu tượng hình ảnh duy trì liên tục trong mọi kịch bản, cộng với một chương trình giảng dạy rõ ràng chuyển từ hình ảnh đơn đến OneVision (phần hình đa) sang video. Bài học này đọc ngân sách, chương trình học, và hành vi mới nổi.

> **【中文解读】**LLaVA-OneVision đóng góp cốt lõi: sử dụng một mã hình ảnh thống nhất  ngân sách 约3000-4000 mã thông báo) và một chương trình học tập 3 giai đoạn (单图→多图→视频), đào tạo một mô hình cùng lúc giỏi 3 cảnh tượng.

> **【拓展：统一多模态模型的产业价值】**Trong các sản phẩm thực tế, người dùng có thể cùng lúc tải lên một bức ảnh, một bức ảnh và một video.

**Type:** Build  | **类型：构建**
**Languages:** Python (stdlib, token budget solver + curriculum planner)  | **语言：Python（标准库，token预算求解器 + 课程规划器）**
**Prerequisites:** Phase 12 · 05 (LLaVA), Phase 12 · 06 (any-resolution)  | **前置：阶段12第05课（LLaVA）、阶段12第06课（任意分辨率）**
**Time:** ~180 minutes  | **时长：约180分钟**

>  **【前置】**学本节前请先掌握:Phase 12·05(LLaVA 投影器) 、Phase 12·06(AnyRes/NaFlex 分辨率调度) 、Phase 11·07(Curriculum Learning 课程学习) ⋅本节是LLaVA 系列的集大成一个模型干三件事──
>  **【类比】**LLaVA-OneVision = "全能瑞士军刀"。其他 VLM = 专门的单功能刀(单图刀、多图刀、视频刀)。 Mỗi chức năng của Swiss军刀 đều không giống như chuyên môn刀精专, nhưng có thể đối phó với tình huống chưa biết;维护一个统一代币 预算(3000-4000) = 子和刀片总长恒定,根据场景切换主功能──

## Mục tiêu học tập

- Thiết kế một ngân sách biểu tượng hình ảnh giữ liên tục trên đầu vào hình ảnh đơn, nhiều hình ảnh, và video.
- Đặt một chương trình giảng dạy đào tạo chuyển giao kỹ năng từ hình ảnh đơn sang video mà không bị lãng quên thảm họa.
- Giải thích tại sao một mô hình đơn lẻ đánh bại các chuyên gia ở cùng số tham số khi chương trình giảng dạy được thực hiện đúng.
- Hãy nêu tên ba khả năng mới nổi được báo cáo bởi LLaVA-OneVision: lý luận đa máy ảnh, gợi ý set-of-mark, đại lý chụp màn hình iPhone.

## Vấn đề  vấn đề nền

Hình ảnh, đa hình ảnh và video đều nhấn mạnh một mô hình khác nhau.

Một hình ảnh cần các token độ phân giải cao (AnyRes, ~ 2880 token hình ảnh) để chụp OCR và chi tiết tinh tế.

Multi-image muốn nhiều hình ảnh ở độ phân giải vừa phải (~ 576 token mỗi) vì vậy lý luận giữa các hình ảnh phù hợp với bối cảnh. Ngân sách cho mỗi mẫu: 4-8 hình ảnh, 576 mỗi, 2300-4600 token.

Video cần nhiều khung hình ở độ phân giải thấp (~ 196 token mỗi khung hình sau khi hợp nhất) để nắm bắt động lực thời gian. Ngân sách cho mỗi mẫu: 8-32 khung hình, 196 mỗi, 1600-6200 token.

> **【中文解读】**Có 3 tình huống khác nhau về token  ngân sách nhu cầu: đơn sơ cần có độ phân giải cao (((khoảng 2880 token), nhiều sơ đồ cần có độ phân giải trung bình (((khoảng 576 token), video cần có độ phân giải thấp nhưng nhiều hơn (((khoảng 196 token)  thách thức nằm ở: làm thế nào để đáp ứng cùng một lúc với một ngân sách cố định ba tình huống──

Nếu bạn đào tạo các mô hình riêng biệt, bạn chọn một ngân sách. Nếu bạn đào tạo một mô hình, bạn cần ngân sách để quy mô hợp lý qua các kịch bản mà không làm hỏng bối cảnh.

Trước OneVision, câu trả lời mặc định là "để đào tạo một kịch bản, bỏ qua những kịch bản khác". Video-LLaVA đã trang bị video vào một mô hình hình ảnh với các giai đoạn đào tạo bổ sung. LLaVA-NeXT đã thêm hỗ trợ nhiều hình ảnh với gạch. Không ai xử lý cả ba đều sạch.

## Khái niệm cốt lõi

### Ngân sách mã thông báo OneVision

LLaVA-OneVision chọn một ngân sách thị thực thống nhất khoảng 3000-4000 token cho mỗi mẫu, phân bổ khác nhau cho mỗi kịch bản:

- Hình đơn: AnyRes-9 (3x3 gạch + hình ảnh nhỏ), mỗi gạch ở 384 với 729 đệm, tích hợp bilinear tích cực 2x2 → 182 mỗi gạch. Tổng cộng: 9 * 182 + 182 = 1820 mã thông báo.
- Multi-image / 多图: mỗi hình ảnh ở độ phân giải vừa phải (384, không có mảng), 729 token mà không có hợp nhất.
- Video / 视频: 32 khung hình với độ phân giải 384 với hồ bơi hàng tỷ hình 3x3 hung hăng → 81 token mỗi khung hình.

Các mã hóa phân bổ duy trì tổng số token gần như không đổi. LLM không bao giờ thấy một lô mà thổi ngữ cảnh của nó.

> **【中文解读】**核心思想:总代币 预算保持恒定(约3000-4000), nhưng cách phân phối khác nhau theo cảnh tượng.

### Chương trình giảng dạy 3 giai đoạn

Các chuyến tàu LLaVA-OneVision được chia thành ba giai đoạn:

1. SFT hình ảnh đơn (stage SI) / 单图指令微调. Tất cả dữ liệu là hình ảnh đơn-thêm văn bản. Đào tạo vào đầu vào AnyRes độ phân giải cao. Điều này dạy nhận thức, OCR và hiểu biết tinh tế. Sử dụng dữ liệu LLaVA-NeXT cộng với dữ liệu hình ảnh đơn cụ thể OneVision.
2. OneVision SFT (phases OV) / 统一指令微调. Trộn hình ảnh đơn + nhiều hình ảnh + video (phases được lấy mẫu một cách đồng nhất). Tập luyện vào ngân sách token thống nhất. Điều này dạy cho mô hình xử lý hình dạng lô khác nhau. Không có trọng lượng đặt lại  tiếp tục từ giai đoạn SI.
3. Chuyển giao nhiệm vụ (phase TT) / 任务迁移. Cứ tiếp tục với một hỗn hợp nhiệm vụ mục tiêu, thường nặng hơn với nhiều hình ảnh hoặc video tùy thuộc vào sản phẩm.

Điều quan trọng: trật tự chương trình học quan trọng. Việc đào tạo video đầu tiên hoặc nhiều hình ảnh đầu tiên tạo ra hiệu suất hình ảnh tồi tệ hơn so với hình ảnh một lần, ngay cả với cùng một dữ liệu. Bài báo này rõ ràng loại bỏ điều này.

> ️ **【易错点】**Bản thân tập trung thống nhất VLM 时课程顺序搞反了(先训视频再训单图)→ 单图性能大幅下降──原因:视频低分辨率输入让模型先学到"模糊是正常的",再训高分辨率单图时模型适应不过来──修复:必须单图 → 多图 → 视频的顺序,先学精细再学粗──
> 🤔 **【困惑】**Q: Tại sao Fixed Token  Budget là quan trọng? Bởi vì cửa sổ trên dưới của LLM là cố định, đơn sơ đột nhiên chiếm 5000 token、 video 10000 token sẽ phá hủy hàng loạt 和推理预算── Fixed Budget = dự đoán chi phí推理, là chìa khóa của việc triển khai sản phẩm──

> **【中文解读】**序列课程至关重要:先单图、再多图+视频、最后任务迁移―― nếu trước tiên đào tạo video hoặc多图, hiệu suất đơn图 sẽ giảm―― vì việc đào tạo đơn图 đã xây dựng nền tảng nhận thức, quá trình và không gian của video cần phải dựa trên đó――

### Tại sao chương trình học hiệu quả

Việc đào tạo hình ảnh đơn xây dựng cơ sở nhận thức. Các mã hóa patch mang các tính năng trực quan tinh tế; LLM học cách tích hợp chúng với văn bản. Nhiều hình ảnh và video giới thiệu những thách thức cấu trúc (phình nào là cái gì, điều gì xảy ra đầu tiên) khó học nếu không có cơ sở nhận thức mạnh mẽ.

Nếu bạn tập hợp tất cả các kịch bản từ đầu cùng nhau, mô hình này không phù hợp với nhận thức (dữ liệu hình ảnh đơn giới hạn mỗi lô) và cấu trúc quá mức (rất dữ liệu đa hình ảnh / video). Kết quả: mô hình theo các mô hình lý luận qua hình ảnh nhưng là nông cạn về thị giác.

Việc sắp xếp chương trình giảng dạy cho bạn sức mạnh nhận thức từ giai đoạn SI, sau đó là lý luận về cấu trúc/thời gian từ giai đoạn OV, mà không mất cả hai.

> **【中文解读】**Nếu tập luyện tất cả các cảnh, mô hình sẽ thiếu khả năng cảm nhận phù hợp (đối với mỗi lô đơn sơ dữ liệu giới hạn) và quá phù hợp cấu trúc (đối với một lượng lớn các mô hình / video dữ liệu), dẫn đến mô hình có thể làm cho các mô hình hình ảnh nhưng hiểu biết thị giác là yếu.

### Khả năng giao diện kịch bản mới nổi

Báo cáo LLaVA-OneVision báo cáo ba khả năng mới nổi:

1. Nhận xét đa máy ảnh / 多摄像头推理. Được đào tạo trên nhiều hình ảnh + video riêng biệt; khi suy luận, được yêu cầu suy luận về một cảnh lái xe đa máy ảnh. Mô hình tích hợp chính xác các quan điểm mặc dù chưa bao giờ thấy định dạng chính xác đó trong đào tạo.
2. Set-of-mark prompting / 标记提示. Người dùng ghi chú các đối tượng trong một hình ảnh với các dấu hiệu có số; mô hình lý luận về "điều gì mà dấu 3 đang làm tương đối với dấu 7." Được đào tạo về cả dấu hiệu và ghi chú; học từ sự kết hợp của việc đặt đất không gian + tham chiếu nhiều hình ảnh.
3. Người dùng cung cấp một ảnh chụp màn hình của màn hình iPhone và yêu cầu lập kế hoạch nhấp chuột tiếp theo. Được đào tạo về ảnh chụp màn hình UI, video của dòng công việc của người dùng và nhiều hình ảnh trước / sau cặp.

Đây không phải là những nhiệm vụ được đào tạo; chúng xuất hiện từ cấu trúc thành phần của chương trình giảng dạy.

> **【拓展：涌现能力的工程启示】**Khả năng hiện tại có nghĩa là giá trị của mô hình thống nhất vượt qua các chuyên gia khác nhau. Khả năng suy luận nhiều hình ảnh có thể được sử dụng để giám sát an toàn, lái xe tự động; ý tưởng ghi dấu có thể được sử dụng để đánh dấu hình ảnh; người dùng có thể sử dụng để kiểm tra tự động hóa UI.

### Visual token pooling  Visual token pooling

Ngân sách token đòi hỏi sự hợp nhất. OneVision sử dụng sự phân cực hàng tuyến trên lưới đệm 2D: 24x24 = 576 đệm trở thành 12x12 = 144 (2x factor) hoặc 8x8 = 64 (3x factor).

Sự lựa chọn của các yếu tố hợp nhất cho mỗi kịch bản là một siêu tham số. ít hợp nhất = nhiều token = đại diện phong phú hơn.

> **【中文解读】**池化在2D 补丁网格空间进行(而不是代币 空间), để giữ lại không gian ở chỗ性──池化因子是每个场景的超参数:少池化=更多代币=更丰富表示;多池化=更少代币=可容纳更多/图像──

### LLaVA-OneVision-1.5

Việc tiếp tục năm 2025 (LLaVA-OneVision-1.5, arXiv 2509.23661) là "bình trọn mở" về dữ liệu đào tạo, trọng lượng mô hình và mã.

### Khác biệt với Qwen2.5VL

Qwen2.5-VL (Dạy 12.09) đưa ra các lựa chọn khác nhau. Nó sử dụng M-RoPE và FPS động thay vì hợp nhất cố định.

> **【中文解读】**Qwen2.5VL sử dụng M-RoPE và động thái tỷ lệ, biểu tượng  ngân sách theo đầu vào thu nhỏ;LLaVA-OneVision  ngân sách cố định 调整池化── hai chiến lược có những ưu điểm: trước là dễ dàng nhưng chi phí không thể dự đoán được, sau là chi phí có thể kiểm soát được nhưng có thể lãng phí hoặc thiếu hụt──
```figure
l5-onevision-budget
```

## Sử dụng nó

## Hãy dùng nó để thực hành

`code/main.py`là một kế hoạch giảng dạy và ngân sách cho một VLM kiểu OneVision. Với ngân sách token cho mỗi mẫu và một hỗn hợp kịch bản mục tiêu (chẳng hạn 40% hình ảnh đơn, 30% hình ảnh đa, 30% video), nó:

- Đưa ra độ phân giải, yếu tố hợp nhất, và khung hình cho mỗi kịch bản.
- Kiểm tra xem mọi kịch bản đều phù hợp với ngân sách chung hay không.
- Báo cáo số lượng token dự kiến, LLM FLOPs, và những kịch bản nào là ít token.
- Bác in một chương trình đào tạo từng giai đoạn.

## Đưa nó lên mạng

Bài học này sẽ mang lại kết quả `outputs/skill-onevision-budget-planner.md`Với phân phối nhiệm vụ mục tiêu và ngân sách cho mỗi mẫu, nó phát ra nhân tố AnyRes, tích hợp mỗi khung hình, số lượng khung video và trọng lượng giai đoạn chương trình giảng dạy.

> **【中文解读】**Bài viết này được phát hành bởi OneVision  ngân sách kế hoạch dụng cụ.

## Tập luyện bài tập

1. Sản phẩm của bạn hỗ trợ 80% hình ảnh đơn, 10% hình ảnh đa (2-4 hình ảnh), 10% video (8-16 khung hình). Thiết kế ngân sách token. Bạn sẽ đặt ngân sách bổ sung mà bạn tiết kiệm vì không làm nhiều hình ảnh nặng?
   | 产品支持 80% 单图、10% 多图（2-4张）、10% 视频（8-16帧）。设计 token 预算。从轻量多图中省下的预算放在哪？

2. Đọc LLaVA-OneVision Phần 4.3 (capacities emergent). đề xuất một kỹ năng mới nổi thứ tư mà chương trình giảng dạy có thể mở ra nhưng báo cáo không báo cáo.
   | 阅读 LLaVA-OneVision 第 4.3 节（涌现能力）。提出课程学习可能解锁但论文未报告的第四种涌现技能。

3. Thay đổi trình tự chương trình học tập  đào tạo hình ảnh đa hình ảnh trước, sau đó hình ảnh đơn, sau đó video.
   | 交换课程顺序——先多图，再单图，最后视频。预测哪些基准会下降以及原因。

4. Bài báo báo cáo các tiêu chuẩn video được đào tạo chỉ trên 8 khung hình mỗi mẫu. Liệu điều đó có tổng quát hóa thành video 30 giây khi suy luận?
   | 论文报告视频基准只用每样本8帧训练。这对推理时的30秒视频泛化吗？先崩溃的是 token 预算还是时序推理？

5. Kết hợp hai tuyến của 24x24 các bản vá đến 12x12 là giảm 4x cho mỗi dim. Thực hiện việc kết hợp trong stdlib Python và xác minh rằng trung bình trên mỗi khối 2x2 phù hợp với đầu ra hai tuyến.
   | 将 24x24 补丁双线性池化为 12x12 是每维 4 倍缩减。用标准库 Python 实现池化，验证每个 2x2 块的均值与双线性输出一致。

## Từ khóa  Keyword

| Term | What people say | What it actually means | 中文含义 | 中文释义 |
|------|-----------------|------------------------|----------|---------|
| OneVision scenario | "Single-image, multi-image, or video" | One of three input shapes the unified VLM handles; the budget stays constant across | 统一 VLM 处理的三种输入形态之一，预算在场景间保持恒定 | |
| Token budget | "How many tokens per sample" | Total visual tokens the LLM sees per training / inference sample, typically 3000-4000 | LLM 每样本看到的总视觉 token 数，通常 3000-4000 | |
| Curriculum | "Training order" | Stage ordering (single-image → multi-image → video) chosen for emergent transfer | 课程学习：按单图→多图→视频顺序训练，促进技能迁移 | |
| Bilinear pooling | "Token shrink" | Applying bilinear interpolation to the patch grid (2D) to reduce token count while preserving locality | 在补丁网格上做双线性插值，减少 token 数并保留空间局部性 | |
| Emergent skill | "Not trained, still works" | Capability that appears at inference without matching training data, due to curriculum composition | 课程学习组合带来的未训练即涌现的能力 | |
| AnyRes-k | "k-tile setup" | k sub-tiles of fixed resolution plus one thumbnail, typical k ∈ {4, 9} | k 个固定分辨率子切片加一个缩略图 | |
| Task transfer | "Cross-scenario generalization" | Skills learned on single-image that apply to video (and vice versa) via shared backbone | 通过共享骨干网络，单图技能迁移到视频（反之亦然） | |

## Xem thêm 延伸阅读

- [Li et al. — LLaVA-OneVision (arXiv:2408.03326)](https://arxiv.org/abs/2408.03326)♬ LLaVA-OneVision
- [LLaVA-OneVision-1.5: Fully Open Framework (arXiv:2509.23661)](https://arxiv.org/abs/2509.23661)                                                                                                                                                                                                                                                              
- [Lin et al. — Video-LLaVA (arXiv:2311.10122)](https://arxiv.org/abs/2311.10122) Video-LLaVA  video nhiều hình thức
- [Lin et al. — VILA (arXiv:2312.07533)](https://arxiv.org/abs/2312.07533)Ưu điểm của VILA
- [Wang et al. — Qwen2-VL (arXiv:2409.12191)](https://arxiv.org/abs/2409.12191) Qwen2-VL đối với Reference
