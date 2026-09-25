# Video-Language Models: Temporal Tokens và Grounding 视频语言模型:时间 Token 与时序定位

> Video không phải là một đống ảnh. Một clip 5 giây có thứ tự nguyên nhân, động từ hành động và thời gian sự kiện mà mô hình hình ảnh không thể đại diện. Video-LLaMA (Zhang et al., tháng 6 năm 2023) đã xuất khẩu video-LLM mở đầu tiên với nền tảng âm thanh-quan hình. VideoChat và Video-LLaVA đã mở rộng mô hình. Đến năm 2025, TMRoPE của Qwen2.5-VL đã thu hẹp khoảng cách với các mô hình độc quyền biên giới. Mỗi hệ thống giải quyết các token thời gian khác nhau  Q-former mỗi clip, concat-pool mỗi khung, TMRoPE mỗi token. Bài học này đọc các mẫu, xây dựng một mẫu khung đồng nhất so với động lực, và đánh giá về các nhiệm vụ đặt đất thời gian.

> **【中文解读】**Video không phải là một đống ảnh. Video ngắn dài 5 giây chứa các kết quả, động tác, động tác và thông tin thời gian của sự kiện, đây là hình ảnh mô hình không thể thể mô tả. Từ Video-LLaMA(2023) đến Qwen2.5-VL(2025), video VLM là một phần của thời gian.

**Type:** Build
**Languages:** Python (stdlib, frame sampler + temporal-grounding evaluator)
**Prerequisites:** Phase 12 · 08 (LLaVA-OneVision)
**Time:** ~180 minutes

>  **【前置】**Học本节前请先掌握:Phase 12·08(LLaVA-OneVision 统一视觉代币 预算) 、Phase 7·04(RoPE 旋转位置编码,本节升级为TMRoPE 三轴) ⋅视频 VLM 的核心挑战:代币 爆炸(1 分钟视频 = 35万代币) + 时间维度建模──
>  **【类比】**Video VLM  xử lý thời gian chiều kích = " xem bóng đá trận đấu回放"。均采样 = 每10秒截一(错过进球瞬间);事件驱动采样 = 进球时密集采样+其他时间稀疏(捕捉关键时刻);动态 FPS = 根据画面变化自动调度──TMRoPE 让模型能理解"4.2秒发生进球"而不是"第15 ", đây là sản phẩm cấp video hiểu关键──

## Mục tiêu học tập

- Giải thích lý do tại sao mã hóa vị trí thời gian thay đổi hiệu suất video VLM độc lập với mã hóa tầm nhìn.
  Trung ngữ翻译:解释为什么时间位置编码独立于视觉编码器影响视频 VLM 性能──
- So sánh mẫu khung đồng nhất, động-FPS, và các sự kiện-động hành trên token-per-second so với độ chính xác đất.
  Trung ngữ翻译:比较均、动态 FPS 和事件驱动采样在每秒代币 数与定位准确率上的表现──
- Mô tả các thiết kế Q-ex-per-clip (Video-LLaMA) vs pooled-per-frame (Video-LLaVA) vs M-RoPE-per-token (Qwen2.5-VL).
  Trung文翻译:描述每片段 Q-former(Video-LLaMA) Vs 每池化(Video-LLaVA) Vs 每代币的 M-RoPE(Qwen2.5-VL)设计。
- Hãy nêu tên bốn tiêu chuẩn video: VideoMME, TempCompass, EgoSchema, Video-MMMU.
  Trung文翻译:列举四个视频基准测试:VideoMME、TempCompass、EgoSchema、Video-MMMU。

## Vấn đề  vấn đề giới thiệu

Một video 1 phút ở 30 FPS là 1800 khung hình. Với 196 mã thông báo trực quan mỗi khung hình (ViT-B ở 224), đó là 352k mã thông báo lớn hơn bất kỳ bối cảnh LLM nào trong kỷ nguyên 2024 .

> 1 phút 30 FPS video có 1800 ──以每 196 视觉代币(ViT-B 在 224 分辨率下) tính toán,共 352k token vượt qua bất kỳ LLM nào trên dưới chiều dài của năm 2024──

> **【中文解读】**1 phút 30FPS video có 1800 , mỗi  196 个视觉代币, tổng cộng 352k token远超 2024 năm LLM trên trên bên dưới cửa sổ.

Có ba chiến lược giảm thiểu:

> 三种压缩策略:

1. Các khung mẫu nhỏ (1-8 FPS tùy thuộc vào nội dung).
   Trung文翻译:子采样(根据内容 1-8 FPS)。
2. Đặt các mã đệm của mỗi khung một cách hung hăng (3x3 hoặc 4x4 pool hàng tỷ).
   Trung文翻译:对每的补丁代币 进行激进池化(3x3或4x4 双线性池化) ⋅
3. Nén qua một máy Q-former lấy clip 16 khung và phát ra 64 token.
   Trung文翻译:通过 Q-former 压缩,将 16 片段映射为 64 个代币──

Mỗi trade-off khác nhau. Subsampling mất chi tiết thời gian. Pooling mất chi tiết không gian. Q-former mất cả hai một chút nhưng tiết kiệm token.

> Mỗi cân nặng khác nhau. Mỗi cân nặng khác nhau.

Mã hóa vị trí thời gian là trục khác: mô hình làm thế nào biết khung 5 đến trước khung 6? Các tùy chọn bao gồm RoPE thời gian 1D đơn giản (Video-LLaMA), nhúng thời gian học (Video-LLaVA), và TMRoPE (Qwen2.5-VL, 3D đầy đủ).

> 时间位置编码是另一个维度:模型怎么知道第5 在第6 之前?选项包括简单的 1D 时间 RoPE(Video-LLaMA) 可学习时间嵌入(Video-LLaVA) 和TMRoPE(Qwen2.5-VL,完整3D) 👇

## Khái niệm cốt lõi

> **【中文解读】**视频语言时序定位(Temporal Grounding) là trong video tìm kiếm chính xác với tự nhiên ngôn ngữ mô tả đối phó với thời gian段── ví dụ: "đ tìm thấy nói cảm ơn các đoạn" cần mô hình hiểu các video của cấu trúc thời gian và ngôn ngữ của thời gian chỉ số── đây là nhiệm vụ chính xác trong video hiểu──

> **【拓展：时序定位的应用场景】**Thời gian định vị trong video tìm kiếm, tự động cắt tỉa, phân tích thể chất, an ninh giám sát, và các trường hợp khác có ứng dụng rộng rãi.


### Video-LLaMA: Q-former mỗi clip + nhánh âm thanh

Video-LLaMA (2023) là video-LLM mở đầu tiên.

> Video-LLaMA(2023) là thứ nhất mở màn video LLM.

- 16 khung hình clip với 2 FPS (vì vậy 8 giây).
  中文翻译:16 片段,2 FPS(即8秒)
- Các tính năng ViT mỗi khung -> Video Q-former phục vụ qua tất cả 16 khung -> 32 truy vấn được học -> LLM.
  Trung文翻译:每 ViT 特征 → Video Q-former 对所有 16 做交叉注意力 → 32 个学习查询 → LLM。
- Chi nhánh âm thanh song song: hình dạng sóng -> ImageBind âm thanh mã hóa -> Audio Q-former -> 32 truy vấn -> LLM.
  Trung文翻译:并行音频分支:波形 → ImageBind 音频编码器 → Audio Q-former → 32 个查询 → LLM。

Nguyên: lý luận âm thanh-thông quan.

> 优势:音视频联合推理――劣势: cố định片段长度, không thể làm bất kỳ thời gian định vị nào――

### VideoChat và Video-LLaVA

VideoChat giữ ý tưởng Video-LLaMA nhưng bỏ âm thanh và đơn giản hóa. Video-LLaVA (Lin et al., 2023) đào tạo một bộ mã hóa thị giác duy nhất trên cả hình ảnh và khung video ("sự sắp xếp trước khi chiếu"), cung cấp một đại diện thống nhất. Cả hai đều là mã hóa CLIP đóng băng + MLP + LLM.

> VideoChat giữ lại ý tưởng của Video-LLaMA nhưng bỏ qua âm thanh và đơn giản hóa.

Cả hai đều là hệ thống khung hình 8-16.

> 两者都不能处理长视频──都是8-16 系统──

### Qwen2.5-VL và TMRoPE

Qwen2.5-VL đã giới thiệu TMRoPE  Temporal-Modality Rotary Position Embedding. Mỗi mã đệm mang một vị trí (t, h, w) nơi t là dấu thời gian thực tế (không phải chỉ số khung).

> Qwen2.5-VL  đã giới thiệu TMRoPE thời gian-模态旋转位置编码── mỗi mã đệm 携带 (t, h, w) 位置, trong đó t là thời gian thực (非索引)──

Sự khác biệt chính từ việc nhúng thời gian đơn giản:

> Khác biệt quan trọng với thời gian đơn giản:

- Thời gian tuyệt đối, không chỉ số. mô hình thấy "tới 4,2 giây" chứ không phải "tới khung 15".
  Trung文翻译:绝对时间而非索引──模型看的是"4.2秒"而不是"第15"──
- Mỗi token quay không phải mỗi clip, mỗi token hình ảnh quay tự do theo dấu thời gian của nó.
  Trung文翻译: từng token 旋转而非 từng đoạn.
- Nếu bạn lấy mẫu ở 2 FPS ở đây và 4 FPS ở đó, TMRoPE xử lý khoảng cách không đồng đều một cách tự nhiên.
  Trung文翻译:兼容动态 FPS──如果某处2 FPS采样、样另一处4 FPS采样,TMRoPE 原生处理不均间隔──

TMRoPE cho phép truy vấn "tại giây nào mèo nhảy?" mô hình có thể phát ra "tới 4,2 giây". Video-LLaMA chỉ có thể nói "trước khi trong clip".

> TMRoPE 支持"猫在几秒跳的?" kiểu truy vấn này. Mô hình có thể xuất "4.2 giây".

> **【中文解读】**TMRoPE là một sáng kiến quan trọng của Qwen2.5 - VL: mỗi token hình ảnh mang theo (t, h, w) thông tin vị trí, trong đó t là thời gian thực chứ không phải chỉ dẫn. Điều này có nghĩa là mô hình nhìn thấy là "4,2 giây" thay vì "15 giây", và có thể xử lý tự nhiên các biến động theo tỷ lệ không đồng đều của thời gian.

> **【拓展：TMRoPE 在金融视频分析中的应用】**Khả năng định vị thời gian tuyệt đối của TMRoPE đối với thị trường tài chính rất quan trọng: khi phân tích tài chính, bạn có thể xác định vị trí "CEO nói về tăng trưởng doanh thu"; khi phân tích giao dịch giám sát video, bạn có thể đánh dấu thời gian của các sự kiện bất thường.

### Các chiến lược lấy mẫu khung

Một dạng: mẫu N khung đồng đều trong thời gian. đơn giản, mất đỉnh chuyển động.

> 均采样: 在时长内均采样 N ── đơn giản, nhưng mất động lực đỉnh ──

FPS động: mẫu thích ứng dựa trên cường độ chuyển động. Phân tích luồng quang học hoặc khung chọn các phân đoạn chuyển động cao để lấy mẫu dày đặc hơn. Qwen2.5VL chạy trên điều này.

> 动态 FPS:根据运动强度自适应采样――光流或差分选择高运动段进行密集采样――Qwen2.5-VL 在此上训――

Động cơ sự kiện: chạy một máy dò nhẹ, lấy mẫu hơn về nơi xảy ra hành động.

> 事件驱动:运行轻量级检测器, 在动作发生处密集采样;;VideoAgent 使用;;

Keyframe + context: mẫu ở ranh giới chụp + một vài khung lân cận. Được sử dụng cho nội dung phim.

> 关键 + 上下文: 在镜头边界采样 + 少量相邻──用于电影内容──

> **【中文解读】**四种采样策略:均采样( đơn giản nhưng mất động lực đỉnh) 动态 FPS(根据运动强度自适应采样) 事件驱动(在动作发生处密集采样) 关键+上下文(在镜头边界采样) ⋅2026最佳实践是动态 FPS + 3x3 双线性池化──

### Tỷ lệ hợp nhất mỗi khung

Với 1 FPS và 576 token mỗi khung hình, một clip 5 phút là 172.800 token.

> 1 FPS ⋅ 576 token 下,5 分钟片段 là 172.800 token──Qwen2.5-VL-72B 的 128k 上下文可以处理,但成本高──

3x3 pool hàng tỷ đường giảm xuống còn 64 token mỗi khung -> 19.200 token trong 5 phút. điểm dễ dàng cho hầu hết các nhiệm vụ.

> 3x3 双线性池化降至每 64 token → 5 分钟 19,200 token── hầu hết nhiệm vụ của món ngọt──

Đặt một nhóm mạnh mẽ hơn (6x6 -> 16 token mỗi khung) cho các dòng công việc của đại lý nơi chi tiết không gian ít quan trọng hơn.

> 更激进地池化(6x6 → 每 16 token) phù hợp với không gian细节不太重要 工作流──

### Bốn tiêu chuẩn video

- VideoMME: hiểu biết video toàn diện, ngắn + trung bình + dài.
  Trung ngữ翻译:VideoMME:综合视频理解,短+中+长。
- TempCompass: lý luận thời gian tinh tế, "trước" / "sau" câu hỏi.
  Trung文翻译:TempCompass:细粒度时间推理, "之前"/"之后"问题──
- EgoSchema: video người đầu tiên dài.
  Trung文翻译:EgoSchema:长程第一人称视频──
- Video-MMMU: các câu hỏi video đa phương pháp đa ngành.
  Trung ngữ翻译:Video-MMMU:多模态多学科视频问题──

Một đánh giá video-VLM đầy đủ chạm đến tất cả bốn. Họ nhấn mạnh các trục khác nhau  TempCompass là tất cả về đặt hàng, EgoSchema là về 3 + phút lý luận, VideoMME trải dài thời gian.

> 完整的视频 VLM 评估需要覆盖全部四基准──它们测试不同维度TempCompass 关注时序,EgoSchema 关注 3分以上的推理,VideoMME 跨越不同时长──

### Các định dạng đầu ra trục trặc

Các định dạng đầu ra cho việc đặt đất thời gian:

> 时序定位的输出格式:

- "Căn cưng nhảy quanh dấu hiệu 4 giây". Mời phân tích nhưng không chính xác.
  Trung ngữ翻译:自由文本:"猫在4秒左右跳起──" dễ phân tích nhưng không chính xác──
- JSON được cấu trúc: `{"event": "jump", "start": 4.1, "end": 4.3}`- Qwen2.5VL chạy theo.
  中文翻译: cấu trúc hóa JSON:`{"event": "jump", "start": 4.1, "end": 4.3}`✿Qwen2.5VL ✿ ✿ ✿
- Dựa trên token: đặc biệt `<time>4.1</time>`- Đơn vị nội bộ của Qwen2.5VL.
  Trung文翻译:基于标志:特殊 `<time>4.1</time>`token 与答交错──Qwen2.5VL 的内部格式──

Xây dựng dựa trên token chính xác nhất cho việc sử dụng dòng chảy. định dạng đầu ra JSON của Qwen2.5VL phân tích trực tiếp.

> 基于代币的格式在下游使用中最准确──Qwen2.5-VL 的 JSON 输出格式可直接解析──

### 2026 thực hành tốt nhất

Đối với VLM video vào năm 2026:

> 2026 Video Video VLM  ಅತ್ಯುತ್ತಮ实践:

- Bộ mã hóa: SigLIP 2 với M-RoPE hoặc TMRoPE (Qwen2.5-VL).
  Trung文翻译:编码器:带 M-RoPE 或 TMRoPE 的 SigLIP 2(Qwen2.5-VL) 』
- Phân mẫu khung: FPS động (1-4 tùy thuộc vào chuyển động) với nắp khung tối đa.
  Trung文翻译:采样:动态 FPS(根据运动 1-4), có tối đa số trên giới hạn.
- Phân hợp mỗi khung: 3x3 hàng tỉ.
  Trung ngữ翻译:每池化:3x3 双线性──
- Kết quả: cấu trúc JSON với các trường thời gian + sự kiện.
  Trung ngữ翻译:输出:带时间和事件字段的结构化 JSON。
- Các điểm chuẩn: VideoMME + TempCompass cho chung; EgoSchema cho tầm xa.
  Trung文翻译:基准测试:通用用 VideoMME + TempCompass;长程用 EgoSchema。

## Hãy sử dụng nó để thực hiện
```figure
video-temporal-patches
```

## Sử dụng nó

`code/main.py`bao gồm:

> `code/main.py`包含:

- Các mẫu khung FPS đồng nhất và động.
  Trung文翻译:均和动态 FPS 采样器。
- Một đánh giá thời gian đồ chơi: với sự kiện "thực tế cơ bản" tại thời gian T và một sản xuất mô hình, ghi điểm chính xác với dung nạp.
  Trung ngữ翻译:一个玩具时序定位评估器:给定时间 T 的"真实"事件和模型输出, 在容差范围内评分──
- Một so sánh giữa Video-LLaMA (16 khung hình, Q-ex), Video-LLaVA (8 khung hình, MLP), Qwen2.5-VL (dynamic FPS + TMRoPE).
  Trung文翻译:Video-LLaMA(16 ,Q-ex) 、Video-LLaVA(8 ,MLP) 、Qwen2.5-VL(动态 FPS + TMRoPE) 的对比──

## Chuyển nó đi.

Bài học này sẽ mang lại kết quả `outputs/skill-video-vlm-frame-planner.md`. Với một nhiệm vụ video (phòng dõi, nhận dạng hành động, định vị thời gian, tổng kết), nó chọn mẫu khung, yếu tố hợp nhất, định dạng đầu ra và mức độ chính xác dự kiến.

> 本课产 出 `outputs/skill-video-vlm-frame-planner.md`△ được cho các nhiệm vụ video định hình (监控,动作识别,时间序定位,摘要), nó chọn các thiết bị lấy mẫu, các yếu tố hóa, các định dạng xuất và tỷ lệ xác định dự đoán等级.

## Tập luyện bài tập

1. Đối với một buổi trình diễn 3 phút, chọn đơn vị phô trương đối với FPS động. Định lý bằng một số lượng token.

2. TMRoPE thêm cụ thể những gì một bảng nhúng thời gian đơn giản không thể làm? TMRoPE 具体添加了什么简单的时间嵌入表无法做到的功能?

3. Viết một sơ đồ JSON cho việc đặt đất thời gian mà một VLM có thể học được phát ra. Bao gồm các trường hợp lỗi.

4. Đọc phần 3 của Video-LLaVA về "Sự sắp xếp trước khi chiếu". Tại sao điều này tốt hơn so với đào tạo các bộ mã hóa hình ảnh và video riêng biệt? 阅读 Video-LLaVA 第 3 节"对齐先于投影",为什么这比分训练图像和视频编码器更好?

5. Với bảng xếp hạng VideoMME, khoảng cách giữa mô hình mở hàng đầu và mô hình độc quyền hàng đầu vào năm 2026 là gì? Khoảng cách đó có thể thuộc về quy mô mã hóa thời gian so với quy mô LLM cơ bản như thế nào?

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|------------------------|---------|
| Temporal grounding | "Time-localized answers" 时序定位 | VLM outputs a specific timestamp range for when an event happens VLM 输出事件发生的具体时间戳范围 | |
| TMRoPE | "Time-Multimodal RoPE" 时间-多模态旋转位置编码 | 3D rotary position with absolute timestamps, used by Qwen2.5-VL 带绝对时间戳的 3D 旋转位置编码 | |
| Dynamic FPS | "Motion-aware sampling" 运动感知采样 | Sample more frames in high-motion segments, fewer in static ones 高运动段密集采样，静态段稀疏采样 | |
| Frame pooling | "Spatial compress per frame" 逐帧空间压缩 | Reduce patches per frame with bilinear interpolation before the LLM LLM 前用双线性插值减少每帧 patch 数 | |
| Video Q-former | "Clip compressor" 片段压缩器 | Cross-attention bottleneck mapping N frames to K learned queries 将 N 帧映射为 K 个学习查询的交叉注意力瓶颈 | |
| VideoMME | "Video bench" 视频基准 | Comprehensive short/medium/long video benchmark, 2500+ samples 覆盖短/中/长视频的综合基准测试 | |

## Xem thêm 延伸阅读

- [Zhang et al. — Video-LLaMA (arXiv:2306.02858)](https://arxiv.org/abs/2306.02858)
- [Li et al. — VideoChat (arXiv:2305.06355)](https://arxiv.org/abs/2305.06355)
- [Lin et al. — Video-LLaVA (arXiv:2311.10122)](https://arxiv.org/abs/2311.10122)
- [Qwen Team — Qwen2.5-VL (arXiv:2502.13923)](https://arxiv.org/abs/2502.13923)
- [Lin et al. — VILA-1.5 (arXiv:2312.07533)](https://arxiv.org/abs/2312.07533)
