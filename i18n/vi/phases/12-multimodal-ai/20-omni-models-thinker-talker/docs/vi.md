# Mô hình Omni: Qwen2.5 Omni và Thinker-Talker chia cắt

> GPT-4o đã trình bày sản phẩm vào tháng 5 năm 2024 không phải vì mô hình cơ bản mà vì hình dạng sản phẩm  một giao diện giọng nói nơi bạn nói, mô hình nhìn thấy những gì máy ảnh nhìn thấy, và nó nói lại trong dưới 250ms. Hệ sinh thái mở đã dành phần còn lại của năm 2024 và 2025 để chạy đua để đạt đến bề mặt sản phẩm đó. Qwen2.5-Omni (tháng 3 năm 2025) là thiết kế mở tham chiếu: một Thinker (hình biến tạo văn bản lớn) cộng với một Talker (hình biến tạo giọng nói song song), được kết nối bằng các token phát thanh trực tuyến. Mini-Omni đơn giản hóa nó, Moshi phù hợp với độ trễ của nó, GLM-4-Voice mở rộng nó cho Trung Quốc. Bài học này đọc kiến trúc Thinker-Talker và ngân sách thời gian trễ làm cho việc phát trực tuyến trong thời gian thực.

> **【中文解读】**Sự đột phá của GPT-4o không nằm trong mô hình tầng dưới, mà nằm trong hình dạng sản phẩm 250ms .Qwen2.5-Omni là nguồn mở của thế giới:Thinker(大型文本生成Tranformator) chịu trách nhiệm về"说什么",Talker(小型语音生成Tranformator) chịu trách nhiệm về并行生成语音代币──两者通过流式代币 连接,实现实时对话──

**Type:** Build
**Languages:** Python (stdlib, streaming pipeline latency simulator + VAD loop)
**Prerequisites:** Phase 12 · 19 (audio-LLMs), Phase 12 · 16 (any-to-any)
**Time:** ~180 minutes

>  **【前置】**Học本节前请先掌握:Phase 12·16(MIO 任意到任意流式)、Phase 12·19(音频 LLM)、Phase 6·04(VAD 语音活动检测)。Qwen2.5-Omni = "开源版 GPT-4o",核心是Thinker-Talker 双流架构,并行化降低延迟到250ms 内。
>  **【类比】**Thinker-Talker 架构 = "翻译员 + 同传播音员"。其他 omni 模型 = 一个人又要思考又要说话(串行,慢);Qwen2.5-Omni = Thinker(大脑,想"说什么")+ Talker(嘴巴,把文字变语音)并行工作。Thinker 流式吐出文本代币,Talker 一边接收一边合成语音,用户听到的是流水线输出,总延迟大幅降低。

## Mục tiêu học tập

- Chia đường ống dẫn suy luận thành Thinker (sự lý luận văn bản) và Talker (sự tổng hợp ngôn ngữ) và giải thích tại sao streaming song song hoạt động.
  Trung ngữ翻译:将推理管道分为 Thinker (文本推理) 和 Talker (语音合成),解释为什么并行流式可行──
- Xét ngân sách thời gian đến đầu tiên-byte âm thanh (TTFAB) cho một tương tác trò chuyện, thành phần theo thành phần.
  Trung ngữ翻译:逐组件计算对话交互的首音频字节时间(TTFAB) ngân sách。
- Mô tả vị trí phù hợp với thời gian của TMRoPE mã hóa qua thị giác, âm thanh và văn bản trong Thinker.
  Trung ngữ翻译:描述 Thinker 内 TMRoPE 跨视觉、音频和文本的时间对齐位置编码──
- Hãy cho chúng ta biết tên ba kiểu trò chuyện thời gian thực: nửa kép, quay lại, và đầy đủ kép.
  Trung ngữ翻译:列举三种实时对话模式:半双工、轮流、全双工。

## Vấn đề  vấn đề giới thiệu

Một trợ lý giọng nói thời gian thực phải làm rất nhiều, nhanh chóng:

> 实时语音助手 cần nhanh chóng hoàn thành nhiều thứ:

1. Nghe người dùng. Đánh dấu giọng nói thời gian thực, phát hiện hoạt động giọng nói (VAD) để biết khi nào họ nói xong.
   Trung ngữ翻译:听用户说话──实时语音分词化,语音活动检测(VAD) phán đoán người dùng何时说完──
2. Nhớ xem, camera nhập vào với tốc độ 2-4 FPS, được truyền vào Thinker cùng với âm thanh.
   Trung ngữ翻译:可选地看──摄像头输入 2-4 FPS,与音频一起流式传入 Thinker──
3. Hãy nghĩ lại, viết câu trả lời dựa trên lịch sử cuộc trò chuyện.
   Trung ngữ翻译:思考.
4. Nói, tổng hợp các mã thông báo âm thanh, giải mã thành dạng sóng, phát trực tuyến đến loa của người dùng.
   Trung ngữ翻译:说话──合成音频代号,解码为波形,流式传输到用户扬声器──

Mỗi bước thêm độ trễ. cảm giác trò chuyện đòi hỏi tổng chuyến đi vòng < 500ms  dưới đó, người dùng ngừng nhận thấy sự chậm trễ. GPT-4o tuyên bố ~250ms. Moshi ~160ms. Qwen2.5-Omni ~350-500ms.

> Mỗi bước đều tăng chậm lại. Ứng dụng chia sẻ:

Không có gì có thể là "đặt hàng tất cả rồi giải mã".

> Mỗi bộ phận đều cần xử lý bằng quy trình. Không thể "được xử lý hàng trước khi giải mã lại".

## Khái niệm cốt lõi

> **【中文解读】**全能模型(Omni Models) đồng thời xử lý văn bản、语音、图像、视频等所有模态──Thinker-Talker 架构将"思考" (thinker) 内部推理) 和"说话" (说话) 语音输出) giải:Thinker là mô hình ngôn ngữ lớn chịu trách nhiệm về推理,Talker là语音合成模块 chịu trách nhiệm về tự nhiên语音输出──

> **【拓展：实时多模态交互**GPT-4o là mô hình giao tiếp thực tế thực hiện thực tế đầu tiên: người dùng có thể hỏi câu hỏi tiếng, mô hình đồng thời xem hình ảnh, trả lời bằng tiếng nói thực tế.


### Người suy nghĩ và người nói

Sự phân hủy của Qwen2.5 Omni:

> Qwen2.5-Omni 的分解:

- Thinker: một bộ biến đổi tạo văn bản 7B-80B. Nêu thụ các mã thông báo văn bản + hình ảnh + âm thanh liên kết. Xuất khẩu mã thông báo văn bản đại diện cho những gì phải nói.
  Trung ngữ翻译:Thinker:7B-80B 文本生成 Transformer。消费交错的文本+图像+音频代码──输出代表"说什么"的文本代码──
- Speaker: một bộ biến đổi tạo giọng nói nhỏ hơn (200M-1B). tiêu thụ các token đầu ra văn bản của Thinker cộng với các token ngữ cảnh giọng nói gần đây.
  Trung ngữ翻译:Speaker:更小的语音生成 Transformer(200M-1B) ――消费 Thinker 的文本输出代号 和近期语音上下文代号──输出离散语音代号(残差 VQ索引) ――
- Bộ giải mã giọng nói: một bộ giải mã dạng sóng phát sóng (SNAC, gia đình MoVQGAN) đưa các token giọng nói đến các mẫu âm thanh trong thời gian thực.
  Trung ngữ翻译:语音解码器:流式波形解码器(SNAC、MoVQGAN 系列),实时将语音代币 转为音频样本。

Sự tách biệt quan trọng. Người suy nghĩ phải lớn để có lý luận tốt. Người nói có thể nhỏ bởi vì công việc của nó là địa phương  chuyển đổi văn bản thành mã thông báo nói chuyện. Người nói lớn hơn không thể diễn tả nhiều hơn; nó chậm hơn.

> Chia tách rất quan trọng. Người suy nghĩ phải có năng lực để đưa ra suy luận. Người nói có thể nhỏ vì nhiệm vụ của nó là biểu tượng chuyển ngữ văn bản. Người nói lớn hơn sẽ không thể biểu hiện tốt hơn, chỉ chậm hơn.

Đi cả hai cùng nhau:

> Và hành trình:

1. Thinker phát hành mã thông báo văn bản t_i.
   Trung文翻译:Thinker 输出文本代号 t_i。
2. Người nói tiêu thụ t_i (thông qua streaming) và phát ra các token nói s_i, s_{i+1}, ..., s_{i+k}.
   中文翻译:Speaker 消费 t_i(通过流式)并输出语音符号 s_i, s_i{i+1}, ..., s_{i+k}。
3. Bộ giải mã giọng nói tiêu thụ các mã thông báo giọng nói khi chúng đến và phát ra các mẫu âm thanh.
   Trung ngữ翻译:语音解码器在语音代码到达时消费并输出音频样本。
4. Đến khi Thinker ở điểm văn bản t_{i+3}, Talker đã phát âm cho t_0..t_{i+2}.
   中文翻译:当 Thinker 在处理文本代币 t_{i+3} 时,Talker 已在播放 t____{i+2} 的音频了.

> **【中文解读】**Người nghĩ  phải lớn ((7B-80B) để làm suy nghĩ tốt, Người nói có thể nhỏ ((200M-1B) vì nhiệm vụ của nó là biểu tượng chuyển ngữ văn bản địa phương.

> **【拓展：Token 速率数学】**16kHz 语音 sử dụng 50Hz 语音 token cơ bản, có nghĩa là mỗi giây cần 50 语音 token── Người nói mỗi giây phải phát ra >= 50 token 才能跟上── Người nói trên H100 trên 200-300M mỗi giây có thể phát ra hàng trăm token, vượt quá nhu cầu; nhưng 7B Talkers 会跟不上── đó là lý do tại sao cần mô hình nhỏ nói riêng chứ không phải mô hình chủ trực tiếp──

### TMRoPE  Vị trí đa phương tiện phù hợp với thời gian

Người suy nghĩ cần tích hợp khung hình ảnh (đến với, nói, 4 FPS), khung âm thanh (đến với 50 khung / giây), và văn bản từ lịch sử cuộc trò chuyện.

> Người suy nghĩ cần tích hợp hình ảnh (ví dụ: 4 FPS) 音频 (với 50 /秒) và văn bản trong lịch sử cuộc nói chuyện (với các thứ tự đơn giản)

TMRoPE gán dấu thời gian tuyệt đối cho mỗi token. Địa chỉ thị giác ở t = 2.3s. Địa chỉ âm thanh ở t = 2.32s. Địa chỉ văn bản từ người dùng " dừng " ở t = 2.35s. RoPE xoay sự chú ý theo dấu thời gian; mô hình nhìn thấy chúng như đồng thời tạm thời.

> TMRoPE dành cho mỗi token chia sẻ tuyệt đối thời gian──视觉 token 在 t=2.3s──音频 token 在 t=2.32s──用户的"停"文本 token 在 t=2.35s──RoPE 按时间旋转注意力;模型将它们视为时间同时发生──

Đây là cơ sở hạ tầng cho "nhưng anh ta vẫy tay chào" để làm việc  mô hình nhìn thấy khung video và âm thanh cùng một khoảnh khắc khái niệm.

> Đó là "Anh ấy đang nói anh ấy tốt" có thể hoạt động bình thường cơ sở hạ tầng mô hình trong cùng một khái niệm nhìn video和音频

### Kết hợp phát biểu trực tuyến

Các token phát biểu phải được truyền tải. Mini-Omni (Xie & Wu, 2024) giới thiệu "những mô hình ngôn ngữ có thể nghe, nói chuyện trong khi suy nghĩ trong streaming": Các token đầu ra Thinker và các token đầu ra Talker liên tục trong cùng một chuỗi.

> 语音 token 必须流式传输──Mini-Omni 引入了"语言模型可以在流式思考的同时听和说":Thinker 输出 token 和 Talker 输出 token 在同一序列中交错──Thinker 一旦提交下一个文本 token,Talker 立即触发──没有批量边界──

Moshi (Défossez et al., tháng 10 năm 2024) là triển khai mở nhanh nhất. 160ms TTFAB trên một A100 duy nhất. Kiến trúc: một biến thể 7B duy nhất phát ra các mã thông báo văn bản và giọng nói trên các vị trí thay thế, với một "mônolog bên trong" tách dòng suy nghĩ khỏi dòng nói.

> Moshi là nguồn mở nhanh nhất thực hiện. Một A100 trên 160ms TTFAB.

### VAD và quay

Khám phá hoạt động giọng nói chạy trên bên đầu vào.

> 语音活动检测在输入端运行──两种模式:

- Half-duplex: người dùng nói, mô hình lắng nghe. mô hình nói, người dùng lắng nghe.
  Trung ngữ翻译:半双工: người dùng nói话,模型听――模型说话, người dùng nghe――通过 VAD 静音检测(约200ms)明确交接――
- Full-duplex: cả hai có thể nói cùng một lúc. Model có thể backchannel ("uh-huh") hoặc gián đoạn. Khó hơn nhiều. Moshi hỗ trợ điều này.
  Trung ngữ翻译:全双工: cả hai bên có thể nói đồng thời.

Qwen2.5 Omni hỗ trợ nửa duplex theo mặc định, với chuyển đổi qua ngưỡng im lặng. Full duplex đòi hỏi xử lý lớp ứng dụng.

> Qwen2.5 - Omni 默认支持半双工, thông qua静音值实现轮流──全双工需要应用层处理──

### Qwen3-Omni (Tháng 11 năm 2025)

Người kế nhiệm. Qwen3-80B Thinker, lớn hơn Talker, cải thiện TMRoPE-v2. độ trễ gần 250ms của GPT-4o. trọng lượng mở.

> 继任者──Qwen3-80B Thinker, Greater Talker,改进的TMRoPE-v2──延迟接近GPT-4o的250ms──开放权重──OmniBench 基准与 Gemini 2.0 Live 竞争──

### Ngân sách thời gian trễ sản xuất

Đối với một tương tác truyền hình điển hình:

> 典型流式交互:

- Mic -> mã thông báo âm thanh: 40-80ms.
  Trung文翻译:麦克风 → 音频 token:40-80ms。
- Prefill (quan nhanh + lịch sử): 100-200ms ở 7B, nhiều hơn ở 70B.
  Trung文翻译:预填充(快速 + 历史):7B 约 100-200ms,70B 更长──
- Đơn vị văn bản đầu tiên của Thinker: 40ms.
  Trung文翻译:首个 Thinker 文本代币:40ms。
- Người nói xử lý mã thông báo văn bản đầu tiên: 20ms.
  Trung文翻译:Talker 处理首个文本代币:20ms。
- Đơn vị giao dịch đầu tiên: 40ms.
  Trung ngữ翻译:首个语音代币 提交:40ms。
- Tự giải mã residual-VQ: 30ms.
  Trung文翻译:残差 VQ 解码:30ms。
- Tự giải mã dạng sóng nói: 50-80ms.
  Trung ngữ翻译:语音波形解码:50-80ms。

Tổng TTFAB: 320-510ms tại 7B, 600-900ms tại 70B. Chất lượng biên giới thường có nghĩa là 70B +; do đó khoảng cách độ trễ biên giới.

> Tổng TTFAB:7B 约 320-510ms,70B 约 600-900ms──前沿质量通常意味着70B+; do đó có khoảng cách延迟前沿──

### Phương pháp toán tỷ lệ token

Tại 16kHz nói chuyện với 50 Hz điểm thoại cơ bản, bạn cần 50 điểm thoại mỗi giây đầu ra. Người nói phải phát ra ≥50 điểm/s để theo kịp. Ở một hiệu suất LLM điển hình là 30-80 điểm/s trên H100, một người nói nhỏ (200-300M) đủ nhanh; một người nói 7B sẽ tụt lại phía sau.

> 16kHz 语音以 50 Hz 基础语音代号 计算, mỗi giây输出需要50语音代号――Speaker 必须以 ≥50 tok/s 的速度输出──H100 上典型 LLM 吞吐量为 30-80 tok/s,小型(200-300M)Speaker 足够快;7B Speaker 会跟不上──

Đây là lý do tại sao các mô hình Talker chuyên dụng nhỏ tồn tại thay vì "chỉ sử dụng mô hình chính".

> Đó là lý do tại sao có mô hình Speakers chuyên dụng nhỏ hơn là mô hình chủ trực tiếp.

## Hãy sử dụng nó để thực hiện
```figure
l5-thinker-talker
```

## Sử dụng nó

`code/main.py`- Có thể là:

- Mô phỏng một đường ống Thinker-Talker với tỷ lệ phát hành token giả.
  Trung文翻译:用模拟的代码 输出速率模拟Thinker-Talker 管道。
- Tính toán TTFAB cho kích thước mô hình có thể cấu hình và tỷ lệ mẫu mic.
  Trung ngữ翻译:为可配置的模型大小和麦风采样样率计算 TTFAB。
- Chứng minh việc quay nửa duplex với ngưỡng im lặng VAD.
  Trung文翻译:用 VAD 静音值演示半双工轮流。

## Chuyển nó đi.

Bài học này sẽ mang lại kết quả `outputs/skill-omni-streaming-budget.md`. Với mục tiêu TTFAB và bộ tính năng của sản phẩm giọng nói thời gian thực (vision-in, hai ngôn ngữ, duplex đầy đủ), chọn Qwen2.5-Omni, Qwen3-Omni, Moshi hoặc Mini-Omni và kích thước Thinker/Speaker.

> 本课产 出 `outputs/skill-omni-streaming-budget.md`△ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △

## Tập luyện bài tập

1. Mục tiêu của bạn TTFAB là 300ms. trên một 7B Thinker và 300M Talker, viết ra thời gian trễ của mỗi thành phần. của bạn TTFAB  mục tiêu là 300ms.

2. Qwen2.5-Omni sử dụng TMRoPE. Mô tả những gì mô hình nhìn thấy cho một lời nhắc khi người dùng bắt đầu nói ở t=1s và máy ảnh bắt được một cử chỉ ở t=1.2s. Qwen2.5-Omni sử dụng TMRoPE。 mô hình mô tả trên người dùng t=1s  bắt đầu nói chuyện、摄像头 t=1.2s 捕获手势时看的输入。

3. Hỗ trợ kép đầy đủ yêu cầu mô hình phát âm trong khi nghe. đề xuất một định dạng dữ liệu đào tạo dạy điều này.

4. Đọc bài báo của Moshi Phần 4. Mô tả sự tách biệt "mônolog nội bộ" và lý do tại sao nó tránh sự chia rẽ của Nhà tư tưởng-Người nói.

5. Lập toán ngân sách thông qua: một người nói phải phát token nhanh như thế nào để theo kịp với 16kHz nói chuyện ở 50 token lớp cơ sở / giây?

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|------------------------|---------|
| Thinker | "Reasoning brain" 思考者 | Large text-generating transformer producing what to say 生成"说什么"的大型文本生成 Transformer | |
| Talker | "Speech-generating mouth" 说话者 | Small transformer producing discrete speech tokens from Thinker's text 将 Thinker 文本转为语音 token 的小型 Transformer | |
| TTFAB | "Latency budget" 首音频字节延迟 | Time-to-first-audio-byte: from user speech end to first audio sample out 从用户说话结束到首个音频样本输出的延迟 | |
| TMRoPE | "Time-aligned RoPE" 时间对齐旋转位置编码 | Position encoding using absolute timestamps across vision, audio, text 跨视觉、音频、文本使用绝对时间戳的位置编码 | |
| Half-duplex | "Turn-taking" 半双工 | User and model alternate; VAD silence detects user-done 用户和模型交替说话；VAD 静音检测用户说完 | |
| Full-duplex | "Simultaneous" 全双工 | Model can speak and listen at the same time; backchannel capable 模型可同时说话和监听；支持回话 | |
| Inner monologue | "Moshi separation" 内心独白 | Single-model design where thinking-stream and speaking-stream interleave 单模型设计，思考流和说话流交替出现 | |

## Xem thêm 延伸阅读

- [Xu et al. — Qwen2.5-Omni (arXiv:2503.20215)](https://arxiv.org/abs/2503.20215)
- [Qwen Team — Qwen3-Omni (arXiv:2509.17765)](https://arxiv.org/html/2509.17765v1)
- [Xie & Wu — Mini-Omni (arXiv:2408.16725)](https://arxiv.org/abs/2408.16725)
- [Défossez et al. — Moshi (arXiv:2410.00037)](https://arxiv.org/abs/2410.00037)
- [Zeng et al. — GLM-4-Voice (arXiv:2412.02612)](https://arxiv.org/abs/2412.02612)
