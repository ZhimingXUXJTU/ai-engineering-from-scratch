# MIO và bất kỳ mô hình đa mô hình trực tuyến nào

> GPT-4o đưa ra một sản phẩm mà hầu hết các mô hình mở không thể sao chép: một đại lý nghe giọng nói, xem video và nói lại trong thời gian thực. Câu trả lời về hệ sinh thái mở vào cuối năm 2024 là MIO (Wang et al., tháng 9 năm 2024). MIO ký hiệu hóa văn bản, hình ảnh, ngôn ngữ và âm nhạc, đào tạo một biến thể nguyên nhân trên các chuỗi liên kết, và tạo ra bất kỳ phương thức nào cho bất kỳ phương thức nào. AnyGPT (Zhan et al., tháng 2 năm 2024) là bằng chứng về khái niệm; MIO là quy mô; Unified-IO 2 (Allen AI, tháng 12 năm 2023) là người anh em họ với nền tảng thị giác + hành động. Bài học này đọc mô hình bất cứ gì đến bất cứ gì 4 tokenizers, một biến thể, giải mã thân thiện với streaming.

> **【中文解读】**GPT-4o  trình bày một hình thức sản phẩm đáng kinh ngạc: một người có thể nghe, có thể xem, có thể thực hiện trong thời gian lặp lại tiếng nói.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, four-modality token allocator + streaming decode loop) | **语言:** Python（标准库，四模态 token 分配器 + 流式解码循环）
**Prerequisites:** Phase 12 · 11 (Chameleon), Phase 6 (Speech and Audio) | **前置知识:** Phase 12 · 11（Chameleon），Phase 6（语音与音频）
**Time:** ~120 minutes | **时间:** ~120 分钟

>  **【前置】**学本节前请先掌握:Phase 12·11(Chameleon 早期融合 token 思路)、Phase 6·01-03(语音/音频 tokeniser:SpeechTokenizer、EnCodec)、Phase 8(VQ-VAE) ・・・MIO = 把Chameleon 思路扩展到4种模态(文本+图像+语音+音乐) ・・・
>  **【类比】**MIO = "万能翻译耳机"──其他多模态系统 = 一堆翻译器接力(视觉翻译→文本→语音翻译→音频), mỗi nhảy chậm hơn + mất thông tin;MIO = một bộ não đồng thời nghe, nhìn, nói, như GPT-4o 那样端到端低延迟── thách thức là mỗi kiểu hình thức phải được token hóa, và token không thể xung đột với nhau──

## Mục tiêu học tập

- Thiết kế một từ vựng chung để lưu trữ các mã thông báo văn bản, hình ảnh, nói và âm nhạc mà không va chạm.
  Trung ngữ翻译:设计一个共享词汇表,容纳文本、图像、语音和音乐代号而不冲突──
- So sánh SEED-Tokenizer (hình ảnh) và SpeechTokenizer residual-VQ (những lời nói) về sự bớt áp suất + tái thiết.
  Trung文翻译:比较 SEED-Tokenizer (图像) 和 SpeechTokenizer 残差 VQ (语音) 在压缩+重建方面的权衡──
- Giải thích chương trình học bốn giai đoạn xây dựng bất kỳ thế hệ nào.
  Trung文翻译:解释构建任意到任意生成的四阶段课程学习。
- Hãy nêu tên ba công thức mở bất cứ ai và các sự thỏa hiệp chính của chúng: MIO, AnyGPT, Unified-IO 2.
  Trung文翻译:列举三个开放的任意到任意方案及其主要权衡:MIO、AnyGPT、Unified-IO 2。

## Vấn đề  vấn đề giới thiệu

Một mô hình đa phương tiện thống nhất dễ tuyên bố và khó xây dựng ở quy mô. Hầu hết các hệ thống "bất cứ ai đến bất kỳ ai" cho đến năm 2024 đã được đưa vào đường ống dẫn: mô hình thị giác → đại diện văn bản → mô hình nói chuyện → âm thanh. Mỗi hop mất thông tin, thêm độ trễ và phức tạp đào tạo. Video demo của GPT-4o cho thấy một lựa chọn thay thế mô hình duy nhất với phản ứng tiếp theo; hệ thống mở theo sau nhiều tháng.

> 统一多模态模型 dễ tuyên bố nhưng khó xây dựng quy mô lớn. Trước năm 2024, hầu hết các hệ thống "任意到任意" đều là ống dẫn: hình ảnh模型→文本表示→语音模型→音频。 mỗi nhảy đều sẽ bị mất thông tin, tăng trì hoãn、 phức tạp hóa đào tạo。 GPT-4o trình bày video cho thấy một mô hình thay thế đơn lẻ, thời gian đáp ứng ở cấp độ thứ hai dưới; hệ thống mở đã bị chậm lại một vài tháng。

> **【中文解读】**"任意到任意"多模态系统最大的挑战是:不能再使用级联管道 (见面→文本→语音→音频),因为 mỗi giai đoạn đều sẽ bị mất thông tin và tăng trì hoãn.

Những thách thức kỹ thuật:

> 工程挑战:

- Các token phải tồn tại cho mọi phương thức, nén không mất - đủ để tái tạo, và sản xuất token theo tốc độ mà biến thể có thể tiêu thụ.
  Trung ngữ翻译: Mỗi kiểu hình thức đều phải có một bộ phận, nén mất đủ nhỏ để xây dựng lại, và tạo ra một biểu tượng với tốc độ chuyển đổi có thể tiêu thụ.
- Một từ vựng duy nhất phải phân bổ không gian cho văn bản (32k+), hình ảnh (16k+), nói (4k+), âm nhạc (8k+).
  Trung văn翻译:单一词汇表必须为文本(32k+) 图像(16k+) 语音(4k+) 音乐(8k+) phân phối không gian──至少四万条以上──
- Dữ liệu đào tạo phải bao gồm mỗi cặp đầu vào-phản xuất (text→image, image→speech, speech→image, vv) hoặc mô hình phải được tạo thành.
  Trung ngữ翻译: training data must cover every input-output对(文本→图像、图像→语音、语音→图像等), hoặc mô hình phải được组合。
- Inference phải truyền các token đầu ra đủ nhanh để có thể trì hoãn cuộc trò chuyện (<500ms thời gian đến đầu tiên-byte âm thanh).
  Trung ngữ翻译:推理必须以足够快的速度流式输出代币,以满足对话延迟 ((<500ms 首个音频字节时间) ]]

## Khái niệm cốt lõi

> **【中文解读】**MIO thực hiện tùy ý đến tùy ý đa dạng xử lý: văn bản, hình ảnh, âm thanh, video có thể được kết hợp tùy ý với các đầu vào và đầu ra.

> **【拓展：全模态模型的趋势】**Xu hướng năm 2025 là từ "viết + ngôn ngữ" hướng đến "tình hình":GPT-4o 原生支持语音输入输出,Gemini 支持视频实时流,Meta's Spirit LM 统一语音和文本。


### Bốn tokeniser cho bốn phương thức

Bộ token của MIO:

> **【中文解读】**MIO vì bốn mô hình khác nhau được phân phối với một token đặc biệt, các token được phát ra đều được chiếu vào chia sẻ từ ngữ biểu đồ không chồng lên ID 区间.

- Văn bản: BPE tiêu chuẩn, từ ngữ ~ 32000.
  Trung ngữ翻译:文本:标准 BPE,词汇量约32,000。
- Hình ảnh: SEED-Tokenizer (2023)  VAE được định lượng với sổ mã riêng biệt, 4096 mục, 32x32 token mỗi hình ảnh.
  Trung文翻译:图像:SEED-Tokenizer(2023) 带离散码本的量化 VAE,4096 条目,每张图 32x32 个代币──
- Phát biểu: SpeechTokenizer residual-VQ (2023)  mã hóa hình dạng sóng 16kHz thành 8 cuốn sách mã thứ bậc; cấp độ đầu tiên là nội dung thô, cấp độ sau này thêm prosody và danh tính loa.
  Trung文翻译:语音:SpeechTokenizer 残差 VQ(2023) 将 16kHz 波形编码为 8层级码本; tầng nhất là nội dung粗粒度,后层添加律和说话人身份──
- Âm nhạc: tương tự residual-VQ (các gia đình MusicGen / Encodec của Meta), 4-8 codebook.
  Trung文翻译:音乐:类似残差 VQ(Meta 的 MusicGen / Encodec 系列),4-8 个码本。

Mỗi phương thức tạo ra các token nguyên số. Các token nhận được các phạm vi ID không liên kết trong từ vựng chung:

> Mỗi mô hình tạo ra một số lượng mã thông báo.

```
text:   0..31999
image:  32000..36095  (4096 image tokens)
speech: 36096..40191  (4096 speech base tokens, plus residual layers)
music:  40192..48383  (8192 music tokens)
sep:    48384..48390  (<image>, <speech>, <music>, </...>, etc.)
```

Tổng: ~ 48k từ vựng.

> 总计约 48k 词汇量──输入嵌入和输出投影覆盖全部词汇──

### Đánh mã phát sóng

Tạo phát biểu sử dụng residual-VQ. Bộ biến đổi dự đoán các token phát biểu cơ sở (vị lớp 0); một bộ định lượng residual được mã hóa song song dự đoán các lớp tiếp theo. Mỗi token lớp 0 là khoảng 50ms âm thanh ở 16kHz.

> 语音生成使用残差 VQ──Transformer 预测基础层(第0层)语音代币;并行解码的残差量化器预测后续层──每个第0层代币 大约对应 16kHz 下的50ms 音频──

> **【中文解读】**流式解码的关键是并行处理:Transformer 预测语音基础层代币,残差量化器并行预测后层――每个基础层代币应应约50ms 音频――整个链路从麦克风到首个音频输出约300-500ms,接近GPT-4o的250ms――

Mô hình phát sóng:

> 流式模式:

1. Người dùng nói trong mic; đồng hồ ghi âm thời gian thực phát ra các đồng hồ ghi âm mỗi 50ms.
   Trung ngữ翻译:用户对着麦克风说话;实时音频分词器每50ms 输出语音代币──
2. MIO tiêu thụ token khi chúng đến (quayền nhanh + tăng lên tăng lên).
   Trung文翻译:MIO 在 token 到达时即时消费(快速 预填充 + 增量前向传播) 』
3. Các token đầu ra được phát ra khi được tạo ra; một bộ giải mã giọng nói song song chuyển chúng thành mẫu âm thanh với độ trễ ~ 50-150ms.
   Trung文翻译:输出代币 在生成时流式输出;并行语音解码器以约50-150ms 延迟将其转换为音频样本。
4. Thời gian đến đầu tiên-byte âm thanh: ~ 300-500ms trong giấy MIO, gần ~ 250ms của GPT-4o.
   Trung ngữ翻译:首音频字节时间(TTFAB):MIO 论文约300-500ms,接近GPT-4o 的约250ms──

Mini-Omni (arXiv:2408.16725), GLM-4-Voice (arXiv:2412.02612), và Moshi (arXiv:2410.00037) là các thiết kế phát âm-LLM phát sóng bổ sung.

> Mini-Omni、GLM-4-Voice 和 Moshi là một thiết kế LLM ⋅Moshi trên một GPU đã thực hiện 160ms 往返延迟──

### Chương trình giảng dạy bốn giai đoạn

Chương trình giảng dạy đào tạo của MIO:

> Chương trình đào tạo của MIO:

1. Giai đoạn 1  sự sắp xếp. Cặp thể hình ảnh văn bản, văn bản, âm nhạc. Mỗi cặp sử dụng phân đoạn từ vựng mã thông báo riêng của mình.
   Trung văn翻译:阶段 1  对齐──大规模模态对语料:文本图像、文本语音、文本音乐── mỗi người sử dụng biểu tượng của riêng mình 词汇段──训练共享词汇表──
2. Giai đoạn 2  liên kết. Tài liệu liên kết đa phương pháp (blog với hình ảnh + video, podcast với bản ghi chép, vv.).
   Trung ngữ翻译:阶段 2  交错──多模态交错文档(带图片+视频的博客、带文字稿的播客等)
3. Giai đoạn 3  tăng cường giọng nói. Dữ liệu âm thanh bổ sung để nâng cao chất lượng giọng nói mà không mất khả năng văn bản.
   Trung ngữ翻译:阶段 3  语音增强──额外音频数据提升语音质量,不损失文本能力──
4. Giai đoạn 4  SFT. Định hướng điều chỉnh qua các phương pháp: VQA, ghi chú, kể chuyện, đối thoại từ nói đến nói.
   中文翻译:阶段 4  指令微调(SFT) 』跨模态指令调优:VQA、描述、旁白、语音对话。

Thiếu một giai đoạn làm suy giảm khả năng cụ thể: bỏ qua giai đoạn 2 và mô hình mất bối cảnh liên tục; bỏ qua giai đoạn 3 và ngôn ngữ kém.

> 跳过某一阶段会导致特定能力退化:跳过阶段 2 模型失去跨模态上下文;跳过阶段 3 语音质量差──

> **【中文解读】**Chương trình đào tạo bốn giai đoạn của MIO là một cách từng bước xây dựng khả năng: 1) 模态 đối với  hình ảnh quy mô lớn  văn bản-语音 đối tác  đào tạo chia sẻ 词汇表; 2) 交错训练多模态交错文档 训跨模态上下文; 3) 语音增强额外音频数据提升语音质量; 4) chỉ thị微调跨模态的VQA、描述对话等等.

### Dòng tư tưởng trực quan

MIO giới thiệu chuỗi tư duy thị giác: mô hình phát ra các token hình ảnh trung gian như một bước lý luận. Đối với "con mèo leo lên cây hay không?" mô hình:

> MIO đã giới thiệu ví dụ tư tưởng chuỗi tư tưởng: mô hình trong quá trình suy nghĩ tạo ra biểu tượng hình ảnh trung gian. Ví dụ: "Căn có leo trên cây không?" mô hình sẽ:

1. Tạo ra `<image>`Các token hiển thị cảnh (từ hình ảnh nhập hoặc bản phác thảo).
   Trung ngữ翻译:输出 `<image>`token 染场景 (được lấy từ输入图像或草图)
2. Gửi tin nhắn phân tích bản phác thảo.
   Trung ngữ翻译:输出文本分析草图.
3. Giả lời cuối cùng.
   Trung ngữ翻译:输出最终答案──

Hình ảnh trung gian được hiển thị phục vụ như một bảng điểm. Điểm so sánh cải thiện các nhiệm vụ lý luận không gian. Ý tưởng phản ánh chuỗi suy nghĩ cho lý luận văn bản.

> 染的中间图像充当草稿板──在空间推理任务上基准测试有所改善──这个思路映射了文本推理中的思维链──

> **【拓展：视觉思维链的应用前景】**Trong lĩnh vực tài chính, kỹ thuật này có thể được sử dụng để phân tích biểu đồ phức tạp: trong lĩnh vực máy tính, mô hình VLA có thể sử dụng hình ảnh để lập kế hoạch hành động, thực hiện lại.

### Các đối thủ cạnh tranh trong bất kỳ

- AnyGPT (arXiv:2402.12226): 4 phương thức (môn văn, hình ảnh, ngôn ngữ, âm nhạc), thiết kế tương tự.
  Trung ngữ翻译:AnyGPT:4 种模态(文本、图像、语音、音乐),类似设计──
- Unified-IO 2 (arXiv:2312.17172): thêm các kết quả hành động thị giác, độ sâu, bình thường.
  Trung ngữ翻译:Unified-IO 2:添加视觉动作输出、深度、法线──任务更多样,规模更小──
- NExT-GPT (arXiv:2309.05519): LLM + các bộ giải mã phân tán cụ thể về phương thức. Không phải là một cách tiếp cận mô hình duy nhất.
  中文翻译:NExT-GPT:LLM + 模态特定扩散解码器──非单模型方案──
- CoDi (arXiv:2305.11846): sự pha trộn hợp nhất; bất kỳ-to-nhà qua chia sẻ tiềm ẩn.
  Trung ngữ翻译:CoDi:可组合扩散; thông qua chia sẻ ẩn không gian thực hiện bất cứ điều gì đến bất cứ điều gì.

MIO là gần nhất với mã thông báo nguyên chất bất kỳ ai. AnyGPT là tổ tiên khái niệm của nó.

> MIO gần nhất với mã thông báo tinh khiết của bất kỳ tùy chọn nào.

### Ngân sách thời gian trễ

Đối với một sản phẩm trò chuyện, độ trễ của mỗi thành phần quan trọng:

> Đối với các sản phẩm đối thoại, sự chậm trễ của mỗi bộ phận là rất quan trọng:

- Mic đến mã thông báo âm thanh: ~ 50ms.
  Trung ngữ翻译:麦克风到音频 token: khoảng 50ms。
- Prefill (tài báo âm thanh + lịch sử): ~ 100ms trên mô hình 8B.
  Trung文翻译:预填充(音频代币 + 历史):8B 模型约100ms。
- Điểm đầu tiên: ~ 50ms.
  Trung文翻译:首个输出代币:约50ms。
- Các bộ giải mã giọng nói tương đối - VQ +: ~ 100-150ms.
  Trung文翻译:并行残差 VQ + 语音解码器: khoảng 100-150ms。

Tổng thời gian từ đầu tiên đến đầu tiên: ~ 300ms tối thiểu. GPT-4o tuyên bố ~ 250ms. Moshi tuyên bố 160ms. MIO / AnyGPT nằm trong phạm vi 400-600ms cho các tiêu chuẩn công cộng.

> 首音频字节时间总计至少约300ms──GPT-4o 声称约250ms──Moshi 声称160ms──MIO/AnyGPT 在公开基准测试中约400-600ms──

> **【中文解读】**Đối thoại sản phẩm của chậm ngân sách:麦克风→语音 token(~50ms)→ 预填充(~100ms)→ 首个输出 token(~50ms)→ 残差 VQ + 语音解码(~100-150ms)。 tổng số TTFAB 约300ms 起──GPT-4o 约250ms,Moshi 仅160ms(单 GPU 上最快的开源方案)。

### Tại sao bất cứ ai cũng không thể

Ngay cả năm 2026, mở bất kỳ mô hình nào theo dõi những mô hình đóng cửa trên hai trục:

> Ngay cả trong năm 2026, mô hình mở tùy chọn cho tùy chọn vẫn còn ở sau mô hình nguồn đóng:

- Chất lượng nói chuyện. Tokenizer residual-VQ là lỗ hổng; nói chuyện âm thanh robot so với giọng nói lớp ElevenLabs.
  Trung ngữ翻译:语音质量──残差 VQ 分词器是有损的; 与 ElevenLabs 级别的语音相比,对话语音听起来机械──
- Việc hỏi mô hình "tự hát về những gì bạn thấy" vẫn thất bại thường xuyên hơn các nhiệm vụ nhìn tinh khiết.
  Trung ngữ翻译:跨模态推理──让模型"唱出你看的" vẫn còn thất bại hơn nhiệm vụ trực quan đơn giản.

Đây là những vấn đề nghiên cứu mở. Qwen3-Omni (Dạy 12.20) là nỗ lực mở tiên tiến nhất vào năm 2025.

> Đây là những vấn đề nghiên cứu mở.

## Hãy sử dụng nó để thực hiện
```figure
any-to-any-stream
```

## Sử dụng nó

`code/main.py`- Có thể là:

> `code/main.py`- Có thể là:

- Định nghĩa phân bổ từ vựng bốn phương thức và in nó.
  Trung文翻译:定义四模态词汇分配并打印。
- Đường bộ một danh sách đầu vào đa phương thức (léc văn bản, hình ảnh, âm thanh, âm nhạc) thông qua bộ định tuyến tokeniser.
  Trung ngữ翻译:通过分词器路由器路由多模态输入(文本、图像、音频片段、音乐)
- Tái bộ giải mã phát sóng cho phản ứng văn bản-thủ ngôn với tính độ trễ.
  Trung ngữ翻译:模拟文本转语响应的流式解码并计算延迟。
- Xét toán thời gian dự kiến đến đầu tiên-byte âm thanh cho mã hóa, prefill, và decoder latencies.
  Trung文翻译:根据编码器、预填充和码器延迟计算预期的首音频字节时间──

## Chuyển nó đi.

Bài học này sẽ mang lại kết quả `outputs/skill-any-to-any-pipeline-auditor.md`. Với một thông số cụ thể của sản phẩm nói chuyện (các cách thức vào, các cách thức ra, mục tiêu trễ), nó kiểm tra các lựa chọn thiết kế của gia đình MIO và tính toán ngân sách trễ.

> 本课产 出 `outputs/skill-any-to-any-pipeline-auditor.md` Định định các quy tắc sản phẩm giao tiếp (输入模态、输出模态、延迟目标), nó kiểm tra các lựa chọn thiết kế của MIO 系列并计算延迟预算.

## Tập luyện bài tập

1. Sản phẩm của bạn chấp nhận đầu vào giọng nói và trả lại đầu ra giọng nói. Mục tiêu ngân sách trễ cuối đến cuối là gì?

2. SpeechTokenizer residual-VQ sử dụng 8 codebook. đề xuất tại sao việc giải mã tương tự các mức dư là cần thiết (trên theo trình tự) và tiết kiệm độ trễ mà nó mang lại. SpeechTokenizer残差 VQ sử dụng 8 个码本。 giải thích为什么需要并行(而非串行) giải码残差层,以及节省了多少延迟。

3. Từ vựng của bạn có 32k văn bản + 4k hình ảnh + 4k ngôn ngữ. Thêm 8k âm nhạc và ~10 bộ tách. Chi phí tham số mã số nhúng là bao nhiêu ở hidden dim 4096?

4. Mạng lưới tư tưởng trực quan phát ra một hình ảnh trung gian. Những loại câu hỏi nào có lợi? Những loại nào bị tổn thương bởi các token bổ sung?

5. Đọc Moshi (arXiv:2410.00037). Mô tả kỹ thuật "mônolog nội bộ" của nó và so sánh với chuỗi tư duy thị giác của MIO.

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|------------------------|---------|
| Any-to-any | "Multimodal in/out" 任意模态进出 | A single model that accepts and emits text, image, speech, and music in any direction 单一模型接受并以任意方向输出文本、图像、语音、音乐 | |
| Residual-VQ | "Speech tokenizer stack" 语音分词器栈 | Multi-codebook tokenization where each layer adds information; base layer is content, later layers are prosody 多码本分词，每层添加信息；基础层是内容，后续层是韵律 | |
| SEED-Tokenizer | "Image codes" 图像编码 | Discrete image tokenizer with 4096-entry codebook used by MIO 离散图像分词器，4096 码本 | |
| Chain-of-visual-thought | "Visual scratchpad" 视觉草稿板 | The model generates an intermediate image as a reasoning step before its final answer 模型在最终回答前生成中间图像作为推理步骤 | |
| Time-to-first-audio-byte | "TTFAB" 首音频字节延迟 | Latency from user voice to first audio output; <500ms for conversational feel 用户语音到首个音频输出的延迟；<500ms 才有对话感 | |
| Four-stage curriculum | "Training recipe" 训练配方 | Alignment -> interleaved -> speech-enhanced -> SFT, in that order 对齐→交错→语音增强→指令微调的四阶段训练流程 | |

## Xem thêm 延伸阅读

- [Wang et al. — MIO (arXiv:2409.17692)](https://arxiv.org/abs/2409.17692)
- [Zhan et al. — AnyGPT (arXiv:2402.12226)](https://arxiv.org/abs/2402.12226)
- [Lu et al. — Unified-IO 2 (arXiv:2312.17172)](https://arxiv.org/abs/2312.17172)
- [Wu et al. — NExT-GPT (arXiv:2309.05519)](https://arxiv.org/abs/2309.05519)
- [Tang et al. — CoDi (arXiv:2305.11846)](https://arxiv.org/abs/2305.11846)
