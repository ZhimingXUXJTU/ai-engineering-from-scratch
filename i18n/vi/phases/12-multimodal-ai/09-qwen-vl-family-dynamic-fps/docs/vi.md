# Qwen-VL Gia đình và Dynamic-FPS Video  Qwen-VL 系列与动态率视频

> Gia đình Qwen-VL  Qwen-VL (2023), Qwen2-VL (2024), Qwen2.5-VL (2025), Qwen3-VL (2025)  là dòng dõi mô hình ngôn ngữ thị giác mở có ảnh hưởng nhất vào năm 2026. Mỗi thế hệ đã đặt cược kiến trúc quyết định duy nhất mà phần còn lại của hệ sinh thái mở đã sao chép trong vòng mười hai tháng: độ phân giải động bản địa thông qua M-RoPE, lấy mẫu động-FPS với sự sắp xếp thời gian tuyệt đối, chú ý cửa sổ trong ViT và các định dạng xuất phát của đại lý có cấu trúc. Bằng Qwen3-VL, công thức đã ổn định: một bộ mã hóa 2D-RoPE-ViT với đầu vào tỷ lệ khía cạnh bản địa, một máy chiếu MLP vào cơ sở ngôn ngữ Qwen3 lớn, và các giai đoạn đào tạo nhấn mạnh OCR, hạ tầng và hành vi của đại lý như các mục tiêu hạng nhất. Bài học này đọc theo thời gian của gia đình để bạn hiểu tại sao mỗi nút ở nơi nó ở.

> **【中文解读】**Qwen-VL 系列 là một trong những mô hình ngôn ngữ có ảnh hưởng nhất năm 2026 . Mỗi thế hệ đã đưa ra một quyết định cấu trúc quan trọng, được cộng đồng mở trong 12 tháng theo: M-RoPE nguyên thủy động thái phân giải, động thái tỷ lệ lấy mẫu + thời gian tuyệt đối đối đối với齐, ViT cửa sổ chú ý, cấu trúc hóa các đại lý mô hình xuất khẩu .

> **【拓展：Qwen-VL 的产业生态位】**Qwen-VL 系列 có lợi thế đáng kể trong lĩnh vực hiểu biết tiếng Trung 语双语场景、GUI 代理、OCR 和视频. Trong lĩnh vực tài chính, Qwen2.5VL có thể được sử dụng để hiểu được báo cáo tài chính ภาษา Trung Quốc、发票 OCR、 cũng như giám sát video phân tích.

**Type:** Learn  | **类型：学习**
**Languages:** Python (stdlib, M-RoPE encoder + dynamic-FPS sampler)  | **语言：Python（标准库，M-RoPE 编码器 + 动态帧率采样器）**
**Prerequisites:** Phase 12 · 06 (patch-n'-pack)  | **前置：阶段12第06课（补丁打包）**
**Time:** ~120 minutes  | **时长：约120分钟**

>  **【前置】**学本节前请先掌握:Phase 12·06(patch-n'-pack 任意分辨率);Phase 7·04(RoPE 旋转位置编码,本节升级为 3D M-RoPE);Phase 14·04(Agent 工具调用,本节讲解 VLM 如何输出 JSON)
>  **【类比】**Qwen-VL 系列 = "中文 VLM 旗舰"──和 LLaVA 系列的区别:LLaVA 主打英文 + 简单架构;Qwen-VL 主打中英双语 + 高分辨率 + 结构化输出──如果你做中文场景(财报、合同、票据),Qwen-VL 是默认选择──
> ️ **【易错点】**Qwen-VL 输出边界框坐标时混"绝对像素 vs相对比例"不同代次使用不同约定──Qwen2-VL 用绝对像素(0-1000 范围),Qwen2.5-VL 改用归一化比例(0-1)──修复:使用前查文档,按代次正确解析坐标──

## Mục tiêu học tập

- Xét các vòng xoay ba trục của M-RoPE (kỷ nguyên thời gian, chiều cao, chiều rộng) và giải thích tại sao tất cả ba đều cần thiết.
- Chọn một chiến lược lấy mẫu FPS động cho một video và lý luận về độ chính xác của token-per-second vs. event-detection.
- Hãy nêu tên bốn nâng cấp thế hệ Qwen-VL theo thứ tự và những gì mỗi thế hệ đã cho phép.
- Cụm một định dạng đầu ra của đại lý JSON kiểu Qwen2.5VL và phân tích các cuộc gọi công cụ có cấu trúc từ phản ứng VLM. 构建 Qwen2.5VL 风格的 JSON 代理输出格式,解析 VLM 响应中的结构化工具调用──

## Vấn đề  vấn đề nền

Qwen-VL được xuất khẩu vào tháng 8 năm 2023 như là phản ứng trực tiếp với LLaVA-1.5 và BLIP-2.

Giải pháp: LLaVA-1.5 chạy ở 336x336. Đẹp cho ảnh, vô dụng cho một hóa đơn bằng tiếng Trung hoặc một ảnh chụp màn hình bảng tính dày đặc.

Video: Video-LLaMA xếp chồng các bộ mã hóa mỗi khung hình và cung cấp chúng cho LLM. Nó hoạt động cho các clip ngắn, không phải cho các video dài nhiều phút nơi trục thời gian là tín hiệu. Nhóm Qwen muốn một bộ mã hóa duy nhất hiểu thời gian.

Khả năng xuất phát được cấu trúc: LLaVA phát ra văn bản dạng tự do. Một đại lý cần JSON. Qwen-VL được đào tạo về các định dạng xuất phát JSON rõ ràng bao gồm các phối hợp hộp biên như văn bản.

Mỗi thế hệ Qwen-VL mở rộng một trong ba trục này.

> **【中文解读】**Qwen-VL  đối với LLaVA-1.5  Three big shortfalls发起挑战:(1) 分辨率336x336 无法处理中文发票或密集表格截图;(2) 视频Video-LLaMA chỉ có thể xử lý đoạn ngắn;(3) 结构化输出LLaVA 输出自由文本,代理需要 JSON──每一代 Qwen-VL 都在三个轴上延伸──

## Khái niệm cốt lõi

### Qwen-VL (Tháng 8 năm 2023)

Thế hệ đầu tiên: OpenCLIP ViT-bigG/14 như một bộ mã hóa (2.5B param), LLama tương thích Q-Former (1 bước với 256 truy vấn), cơ sở Qwen-7B.

- 448x448 độ phân giải (sau đó là SOTA cho một VLM mở).
- Địa điểm / 定位: được đào tạo trên các cặp hình ảnh- văn bản với đầu ra mã phối hợp rõ ràng. "Căn nuôi ở <box> 112, 204, (280, 344)</box>".
- Trung + Anh đào tạo đa ngôn ngữ ngay từ đầu. Từ đầu, chúng tôi đã hỗ trợ Trung tiếng Anh đào tạo hai ngôn ngữ.

Các điểm chuẩn vào thời điểm đó: cạnh tranh với GPT-4V ở tiếng Anh, thống trị ở tiếng Trung Quốc.

> **【中文解读】**Qwen-VL đầu tiên thế hệ đột phá:448x448 phân giải độ phân giải ((超越 LLaVA 的 336x336)  định vị khả năng ((输出边界框坐标)  中英双语──在中文基准上显著领先──

### Qwen2-VL (Ngày 9 năm 2024)  M-RoPE và độ phân giải bản địa  Qwen2-VL: M-RoPE với độ phân giải nguyên sinh

Qwen2-VL đã thay thế stack Q-Former với độ phân giải cố định bằng một bộ mã hóa ViT có độ phân giải động bản địa.

- Định nghĩa động bản địa / 原生动态分辨率. ViT chấp nhận bất kỳ HxW nào có thể chia bằng 28 (phát 14 với 2x kết hợp không gian). Một hình ảnh ở 1120x672 (40x24 phát kết hợp) tạo ra 960 token thị giác. Không có kích thước, không có tay, không có hình ảnh nhỏ.
- M-RoPE (Multimodal RoPE) / 多模态旋转位置编码. Mỗi token mang một vị trí 3D (t, h, w) thay vì 1D. Đối với hình ảnh t = 0, cho video t = frame_index. RoPE xoay các vector truy vấn / khóa theo tần số mỗi trục. Không có bảng nhúng vị trí.
- MLP Projector / MLP 投影器. Thả Q-Former; sử dụng 2 lớp MLP trên các mã thông báo vá hợp nhất.
- Video với FPS động / 动态率视频. Video lấy mẫu ở 1-2 FPS mặc định, nhưng mô hình chấp nhận tính toán khung hình tùy ý.

Kết quả: Qwen2-VL-7B phù hợp với GPT-4o trên một số điểm chuẩn đa phương thức và đánh bại nó trên DocVQA (94.5 vs 88.4).

> **【中文解读】**Quý cấu trúc cốt lõi của Qwen2-VL thay đổi: loại bỏ độ phân giải cố định + Q-Former, thay đổi thành độ phân giải động thái gốc ViT + M-RoPE + MLP 投影器。M-RoPE cho mỗi token 赋予 3D 位置(时间、高度、宽度), để cùng vị trí编码能统一处理文本、图像和视频。7B 参数就匹配 GPT-4o 的多模态基准。

### Qwen2.5VL (tháng 2 năm 2025)  FPS động + thời gian tuyệt đối  Qwen2.5VL: động thái 率 + 绝对时间

Vị trí lớn của Qwen2.5VL là video. FPS động không chỉ là "chọn mẫu nhiều khung hình hơn khi cần thiết".

- Các biểu tượng thời gian tuyệt đối / 绝对时间 token. Thay vì các chỉ số vị trí (trình 0, 1, 2...), sử dụng các dấu thời gian thực. "À 0:04, con mèo nhảy. " Mô hình thấy `<time>0.04</time>`- Không, không, không, không.
- Phạm vi động lực FPS / 动态率. Sample tại 1 FPS cho hình ảnh chậm, 4+ FPS cho hành động. người dùng hoặc huấn luyện viên chọn; M-RoPE thích nghi.
- Vệch quan tâm trong ViT / ViT  cửa sổ chú ý. Vệch quan tâm không gian được cửa sổ (địa phương trong các khối) cho thông qua; Vệch quan tâm toàn cầu mỗi vài lớp.
- Mô hình đầu ra JSON rõ ràng / 显式 JSON 输出格式. Được đào tạo trên dữ liệu gọi công cụ: `{"tool": "click", "coords": [380, 220]}`. Trưởng thức sẵn sàng.                                                                                                                                                                                                                                                            
- MRoPE-v2 quy mô / MRoPE-v2 缩放. Các vị trí quy mô với kích thước đầu vào tối đa để một video 10 phút không chạy ra khỏi phạm vi tần số.

Điểm chuẩn: Qwen2.5-VL-72B vượt qua GPT-4o trên hầu hết các điểm chuẩn video, phù hợp với Gemini 2.0 trên tài liệu, và thiết lập SOTA mô hình mở cho việc kết nối GUI (ScreenSpot: 84% chính xác so với 38% cho GPT-4o).

> **【中文解读】**Sự đột phá của Qwen2.5VL nằm trong video hiểu: mã thời gian tuyệt đối 让模型知道"第4秒猫跳了", động thái 率让模型在动作密集时自动提高采采采率,窗口注意力提升 ViT 吞吐量──72B 版本在视频基准上超越GPT-4o,GUI 定位精度(ScreenSpot 84%)远超GPT-4o(38%)──

> **【拓展：结构化输出对 Agent 工程的意义】**Trong trường hợp tài chính, điều này có nghĩa là VLM có thể xuất ra cấu trúc "点击坐标" hoặc "提取的字段", trực tiếp được tiêu thụ bởi hệ thống Down游系统, không cần phải biểu hiện chính thức phân tích.

### Qwen3-VL (Tháng 11 năm 2025)

Qwen3-VL là một nâng cấp tăng lên tập hợp thay vì tái phát minh: xương sống LLM lớn hơn (Qwen3-72B), dữ liệu đào tạo mở rộng, OCR cải thiện, lý luận mạnh mẽ hơn thông qua "chế độ suy nghĩ" Qwen3. ViT và M-RoPE ở lại.

Điểm cuối cùng: vào năm 2025, kiến trúc Qwen-VL đã ổn định. Các thế hệ khác tính toán và dữ liệu quy mô, không phải nguyên thủy.

> **【中文解读】**Qwen3-VL là tăng cường tăng cường thay vì tái phát minh: lớn hơn LLM 骨干、更多训练数据、更好的OCR、更强的推理(Qwen3 " suy nghĩ模式")。ViT 和 M-RoPE 保持不变──到2025年,Qwen-VL 架构已经稳定,后版本主要通过扩大和优化数据来升级──

### M-RoPE toán học

RoPE cổ điển xoay một truy vấn `q`kích thước `d`theo vị trí `m`sử dụng các phối hợp:

```
q_rot[2i]   = q[2i]   * cos(m * theta_i) - q[2i+1] * sin(m * theta_i)   # 经典 RoPE 旋转
q_rot[2i+1] = q[2i]   * sin(m * theta_i) + q[2i+1] * cos(m * theta_i)
theta_i     = 10000^(-2i/d)                                                 # 频率基
```

M-RoPE chia mờ ẩn thành ba băng.`d = 96`. Đưa 32 điểm tối đến thời gian, 32 điểm cao, 32 điểm rộng. Mỗi băng xoay theo vị trí trục riêng của nó. Một đệm ở (t=5, h=10, w=20) có được xoay `R_t(5)`- `R_h(10)`- `R_w(20)`được áp dụng cho ba băng của nó.

Sử dụng mã thông báo văn bản `t = text_index, h = 0, w = 0`(hoặc một lựa chọn bình thường), giữ sự tương thích.`t = frame_time, h = row, w = col`. Sử dụng hình ảnh đơn `t = 0`- Tôi không biết.

Lợi ích: một mã vị trí xử lý văn bản, hình ảnh và video mà không cần mã phân nhánh hoặc bảng vị trí khác nhau.

> **【中文解读】**M-RoPE sẽ phân chia kích thước ẩn thành ba đoạn (đường), mỗi đoạn theo vị trí trục của riêng mình xoay vòng.

### Phân tích lấy mẫu FPS động 动态 率采样逻辑

Với đoạn video thời gian `T`giây và ngân sách token mục tiêu `B`- Có thể là:

1. Xét FPS tối đa mà bạn có thể đủ khả năng: `fps_max = B / (T * tokens_per_frame)`                                                                                                                                                                                                                                                              
2. Chọn một mục tiêu FPS từ `{1, 2, 4, 8}`Điều đó làm thỏa mãn `fps <= fps_max`Từ tỷ lệ ứng cử viên chọn
3. Nếu chuyển động cao (phần học lưu lượng quang học hoặc yêu cầu rõ ràng của người dùng), chọn FPS cao hơn. Nếu chuyển động thấp, chọn thấp hơn.
4. Mô hình đồng nhất tại FPS được chọn; nhập `<time>t</time>`- Đồ tín hiệu giữa các khung.

Qwen2.5-VL đào tạo logic này ngầm; khi suy luận người dùng kiểm soát qua `fps`Parameter: Một chuỗi hành động 60 giây ở 4 FPS với 81 token mỗi khung = 19440 token, có thể quản lý trong bối cảnh 32k.

> **【中文解读】**动态率的核心思想:根据视频时长、代币 预算和运动量, tự động chọn 优率──60秒动作场景在4FPS下产生19440代币,可在32k上下文中处理──

### Tạo ra các đại lý cấu trúc

Việc đào tạo các đại lý của Qwen2.5VL rõ ràng nhắm vào các cuộc gọi công cụ có cấu trúc:

```
{
  "tool": "mouse_click",          # 工具名称
  "coords": [1024, 512],          # 点击坐标
  "button": "left",               # 鼠标按钮
  "modifier": null                # 修饰键
}
```

Phân tích là xác định: JSON.parse trên đầu ra của mô hình. So sánh với dạng tự do "thấp vào (1024, 512) " đòi hỏi phải xử lý regex và mơ hồ. Sự thay đổi là lý do tại sao điểm ScreenSpot của Qwen2.5-VL đã nhảy từ 55% đến 84%.

> **【中文解读】**结构化输出让VLM có thể trực tiếp phát hành các công cụ phân tích được sử dụng (如点击坐标), không cần phải biểu hiện chính thức.
```figure
mm-mrope-axes
```

## Sử dụng nó

## Hãy dùng nó để thực hành

`code/main.py`thực hiện:

- M-RoPE tính vị trí cho một chuỗi đóng gói trộn văn bản, các bản vá hình ảnh, và khung video.
- Mô hình FPS động: được cho (thời gian, ngân sách, motion_level), chọn FPS và phát ra khung thời gian.
- Một bộ phân tích sản xuất JSON Qwen2.5VL xử lý các phản ứng gọi công cụ với các trường phối hợp.

## Đưa nó lên mạng

Bài học này sẽ mang lại kết quả `outputs/skill-qwen-vl-pipeline-designer.md`Với một nhiệm vụ video (phòng dõi, đại lý, nhận dạng hành động, khả năng truy cập), nó phát ra cấu hình Qwen2.5 - VL (kế hoạch khung, chiến lược FPS, cờ chú ý cửa sổ, chế độ xuất phát đại lý) và ước tính độ trễ. Sử dụng điều này bất cứ khi nào bạn triển khai mô hình gia đình Qwen-VL cho một sản phẩm video.

> **【中文解读】**本课产出 Qwen-VL pipeline 设计工具;;给定视频任务(监控、代理、动作识别、无障碍),输出 Qwen2.5VL 配置(预算、FPS 策略、窗口注意力标志、代理输出模式) và延迟估计──

## Tập luyện bài tập

1. Xét các vòng quay M-RoPE cho một đệm ở (t=3, h=5, w=7) với ẩn 48 (16 mỗi băng, cơ sở theta 10000).
   | 计算 (t=3, h=5, w=7) 补丁的 M-RoPE 旋转，隐藏维度48（每频段16），基数10000。展示每频段前三对的旋转角度。

2. Một máy ảnh bảo mật 10 phút ghi lại ở 1 FPS tạo ra bao nhiêu khung hình? ở độ phân giải 384 với 3x pool, bao nhiêu mã thông báo tổng cộng?
   | 10分钟安防摄像头录像在 1FPS 下产生多少帧？384分辨率+3x池化后多少 token？Qwen2.5-VL 默认 32k 上下文能处理吗？

3. Chọn FPS cho một cuộc đua quần vợt 30 giây so với một bản demo công thức 30 giây so với một ghi lại của đại lý UI 30 giây.
   | 为 30 秒网球比赛、30 秒食谱演示、30 秒 UI 代理录像选择帧率。用动态帧率逻辑论证每个选择。

4. Qwen2.5VL hoàn toàn loại bỏ Q-Former. Tại sao một MLP đơn giản hoạt động vào năm 2025 nhưng không hoạt động vào năm 2023?
   | Qwen2.5-VL 完全去掉了 Q-Former。为什么 MLP 在 2025 年可行但 2023 年不行？（提示：数据规模和编码器质量。）

5. Phân tích ba các sản phẩm gọi công cụ JSON Qwen2.5-VL vào các phím Python.
   | 将三个 Qwen2.5-VL JSON 工具调用输出解析为 Python 字典。畸形 JSON 会出什么问题？Qwen 食谱推荐的恢复策略是什么？

## Từ khóa  Keyword

| Term | What people say | What it actually means | 中文含义 | 中文释义 |
|------|-----------------|------------------------|----------|---------|
| M-RoPE | "Multimodal RoPE" | 3D rotary position embedding with temporal, height, and width bands in the hidden dim | 三维旋转位置编码，隐藏维度分时间、高度、宽度三个频段 | |
| Dynamic FPS | "Smart sampling" | Frame sampling rate chosen per video based on motion, duration, and token budget | 根据运动量、时长和 token 预算动态选择帧率 | |
| Absolute time token | "Timestamp token" | `<time>t</time>` interleaved in the sequence so the model sees actual seconds not frame index | 在序列中插入真实时间戳 token | |
| Window attention | "Local attention" | Spatial self-attention restricted to small windows for speed; global attention added periodically | 空间自注意力限制在小窗口内加速，周期性加入全局注意力 | |
| Structured agent output | "JSON mode" | Training data supervision teaching the VLM to emit parseable JSON with coords and tool names | 训练 VLM 输出可解析的 JSON（含坐标和工具名） | |
| min_pixels / max_pixels | "Resolution bounds" | Per-request Qwen2.5-VL controls bounding total pixel count and therefore token count | 按请求控制最小/最大像素数从而控制 token 数 | |
| Grounding | "Point-at-it" | Outputting bounding-box coordinates as text tokens; used since Qwen-VL v1 | 输出边界框坐标作为文本 token，从 Qwen-VL v1 开始支持 | |

## Xem thêm 延伸阅读

- [Bai et al. — Qwen-VL (arXiv:2308.12966)](https://arxiv.org/abs/2308.12966) Quyen-VL thế hệ đầu tiên
- [Wang et al. — Qwen2-VL (arXiv:2409.12191)](https://arxiv.org/abs/2409.12191) Qwen2-VL M-RoPE
- [Qwen Team — Qwen2.5-VL Technical Report (arXiv:2502.13923)](https://arxiv.org/abs/2502.13923) Tỷ lệ động lực Qwen2.5VL
- [Qwen Team — Qwen3-VL (arXiv:2511.21631)](https://arxiv.org/abs/2511.21631) Qwen3-VL tăng cường
- [Zhu et al. — InternVL3 (arXiv:2504.10479)](https://arxiv.org/abs/2504.10479)Ứng viên của VL3
