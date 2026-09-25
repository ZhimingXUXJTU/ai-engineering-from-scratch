# Mô hình ngôn ngữ âm thanh: từ Whisper đến Audio Flamingo 3 Arc

> Whisper (Radford et al., tháng 12 năm 2022) đã giải quyết nhận dạng giọng nói  680k giờ nói nhiều ngôn ngữ được giám sát yếu, một bộ biến đổi mã hóa-đánh mã đơn giản, một tiêu chuẩn khiến mọi bản phát hành ASR sau đó trích dẫn nó. Nhưng sự nhận ra không phải là lý luận. Để hỏi "vài nhạc cụ nào trong bản ghi âm này" hay "người nói đang bày tỏ cảm xúc gì" hay "cái gì đã xảy ra trong phút 3" cần phải hiểu âm thanh, chứ không phải bản sao. Qwen-Audio, SALMONN, LTU và NVIDIA's Audio Flamingo 3 (AF3, tháng 7 năm 2025) dần xây dựng đống đó: giữ các bộ mã lớp Whisper, đập vào các máy hình thành Q, đào tạo dữ liệu hướng dẫn văn bản âm thanh, thêm lý luận chuỗi suy nghĩ. Bài học này đi qua vòng cung.

> **【中文解读】**Whisper  giải quyết nhận dạng tiếng nói, nhưng nhận dạng không phải là lý thuyết. "thông đoạn này thu âm sử dụng những dụng cụ gì""", người nói đã thể hiện những cảm xúc gì" như các vấn đề cần khả năng hiểu âm thanh, không phải chuyển tiếp đơn giản. Từ SALMONN đến Audio Flamingo 3(AF3), con đường phát triển của Sound频 LLM là: giữ lại bộ lập trình cấp độ Whisper + 加 Q-Former 桥接 + 用音频-文本指令数据训练 + 加链式思考推理.

**Type:** Build
**Languages:** Python (stdlib, log-Mel spectrogram + audio Q-former skeleton)
**Prerequisites:** Phase 6 (Speech and Audio), Phase 12 · 03 (Q-Former)
**Time:** ~180 minutes

>  **【前置】**Học本节前请先掌握:Phase 6·01-02(语音信号处理:FFT/Mel 频谱图/Whisper);Phase 12·03(Q-Former 桥接,本节复用为音频 Q-Former);Phase 7(Transformer 编码器-解码器)。音频 LLM = 视觉 LLM 的"听觉版",只是输入从图像补丁 变成 Mel 频谱图片补丁──
>  **【类比】**音频 LLM = "为 LLM 装耳朵"──Whisper = 助听器(只能转录不能思考); SALMONN = 聋学校的翻译员(Whisper 转录→LLM 思考);AF3 = 直接给 LLM 装耳(端到端听+想+答)──端到端的好处:能捕捉转录丢失的信息(语调、情绪、停顿),这些是推理的关键点──

## Mục tiêu học tập

- Xét ra một quang phổ log-Mel từ hình dạng sóng: cửa sổ, FFT, ngân hàng lọc, chuyển đổi log.
  Trung文翻译:从波形计算 log-Mel 频谱图:窗口化、FFT、波器组、对数变换──
- So sánh các tùy chọn mã hóa: mã hóa Whisper, BEAT, AF-Whisper hybrid.
  Trung文翻译:比较编码器选项:Tầm 编码器、BEATs、AF-Tầm 混合──各自何时胜出──
- Xây dựng một âm thanh Q-former: N tìm kiếm có thể học được phục vụ chéo cho các bản vá quang phổ.
  Trung文翻译:构建音频 Q-former:N 个可学习查询对频谱图补丁做交叉注意力──
- Giải thích đào tạo âm thanh-LLM theo từng giàn (Whisper-then-LLM) so với đào tạo âm thanh-LLM từ đầu đến cuối: tại sao kết thúc đến cuối cân bằng tốt hơn cho lý luận.
  Trung文翻译:解释级联(Whisper 后接 LLM)vs 端到端音频 LLM 训练:为什么端到端在推理上扩展更好──

## Vấn đề  vấn đề giới thiệu

Việc nhận dạng giọng nói được giải quyết bởi Whisper. OCR của âm thanh là một hàng hóa. Nhưng " hàng hóa " dừng lại khi ghi âm. Nếu mô hình không thể lý luận về những gì nó nghe thấy  thời gian, loa, cảm xúc, cấu trúc âm nhạc, âm thanh môi trường  bản ghi âm một mình không thể thúc đẩy các tính năng sản phẩm.

> 语音识别已被语音识别已被语音已被解决. 音频 OCR 已成为基础能力──但"基础能力" dừng lại trong việc ghi lại. Nếu mô hình không thể suy nghĩ về những gì họ nghe được, thì thời gian, nói chuyện, cảm xúc, âm nhạc cấu trúc, môi trường 声 chỉ dựa trên ghi lại không thể thúc đẩy các chức năng sản phẩm.

Ba tuyến đường rõ ràng:

> 三条 rõ ràng:

1. Cascade: Whisper ghi lại, LLM lý luận về ghi chép. Làm việc cho kịch bản nói chuyện thuần túy. thất bại cho âm nhạc, âm thanh môi trường, chồng chéo đa loa, cảm xúc.
   Trung ngữ翻译:级联:Whisper 转录,LLM đối với chuyển âm văn bản suy luận。 áp dụng cho trường hợp âm thanh đơn thuần。 đối với âm nhạc、环境音频、多人重叠、情绪不适用。

2. End-to-end audio-LLM: một bộ mã hóa âm thanh cung cấp các token âm thanh trực tiếp vào LLM, bỏ qua bản sao chép. Giữ lại thông tin âm thanh ( cảm xúc, loa, môi trường).
   Trung ngữ翻译:端到端音频 LLM:音频编码器将音频代码器 直接输入 LLM,跳过转录──保留声学信息(情绪、说话人、环境) ・需要新训练数据──

3. Hybrid: mã hóa âm thanh + mã hóa văn bản có thể cả sao chép và lý luận. Qwen-Audio và Audio Flamingo chọn con đường này.
   Trung ngữ翻译:混合:音频编码器 + 文本解码器,既能转录又能推理──Qwen-Audio 和 Audio Flamingo 选择此路径──

## Khái niệm cốt lõi

> **【中文解读】**语音语言模型 từ Whisper(OpenAI của 语音识别模型) đến AudioFlamingo của sự tiến triển. 语音语言模型的基础模型是从 Whisper (OpenAI) 语音识别模型到 AudioFlamingo的演练.

> **【拓展：语音 AI 的前沿**Whisper-large-v3  hỗ trợ khoảng 100 种语言的语音识别──2024-2025 năm xu hướng là语音大模型:GPT-4o 原生语音输入输出(延迟约 320ms),Gemini's实时语音对话,ElevenLabs's语音克隆──AudioFlamingo trong nhiệm vụ hiểu âm thanh đạt được SOTA, có thể trả lời về các vấn đề phức tạp về âm nhạc và âm thanh──


### Nhãn quang phổ Log-Mel: tính năng đầu vào

Mỗi bộ mã hóa âm thanh bắt đầu với cùng một tính năng: một quang phổ log-Mel.

> Mỗi bộ lập trình âm thanh đều có cùng một đặc điểm bắt đầu: log-Mel 频谱图.

1. Mẫu lại lên 16 kHz.
   Trung ngữ翻译:重采样至16 kHz。
2. Chuyển đổi Fourier ngắn thời gian với cửa sổ 25ms, nhảy 10ms.
   Trung文翻译:短时里叶变换,25ms 窗口,10ms 步长。
3. Hãy lấy kích thước của kết quả FFT.
   Trung文翻译:取 FFT 结果的幅度──
4. Sử dụng các băng lọc Mel (thường là 80 bộ lọc có khoảng thời gian log 0-8000 Hz) để biến dạng đến tần số nhận thức.
   Trung ngữ翻译:应用 Mel 波器组( thường là 80 个波器, đối với số间隔 0-8000 Hz)映射到感知频率──
5. Log compress (log(1 + x)) cho phạm vi động.
   Trung文翻译:对数压缩(log(1 + x))以处理动态范围──

Kết quả: một mảng hình dạng 2D (T, 80) nơi T là số khung thời gian. Đối với clip 30 giây với tốc độ khung hình 100 Hz: (3000, 80).

> Kết quả: hình dạng为 (T, 80) của 2D 数组, trong đó T là thời gian số──30 秒片段在 100 Hz 率下:(3000, 80)──

### Bộ mã hóa của Whisper

Bộ mã hóa của Whisper là một bộ biến đổi kiểu ViT 12 tầng xử lý quang phổ log-Mel như một chuỗi khung thời gian.

> Whisper's编码器 là một bộ chuyển đổi ViT 风格 12 tầng, sẽ log-Mel 频谱图作为时间序列处理――输出: mỗi thời gian一个隐藏状态向量――

Đối với ASR, decoder của Whisper là một biến đổi sự chú ý qua nhau tạo ra các mã thông báo văn bản được điều chỉnh trên đầu ra encoder.

> Đối với ASR,Whisper's解码器 là một giao thông chú ý Transformer, theo编码器输出生成文本代币――标准编码器-解码器――

Đối với ALM (audio-LLM), bạn muốn nguồn đầu ra mã hóa như là đầu vào một LLM khác.

> 对于ALM(音频 LLM), cần将编码器输出作为另一个LLM的输入──模式:Whisper 编码器结,Q-former 可训练,LLM 结或微调──

### Các bộ mã hóa BEAT và các bộ mã hóa âm thanh cụ thể

Whisper được đào tạo dựa trên dữ liệu nói chung. Nó yếu hơn cho âm nhạc và âm thanh môi trường.

> Phầm phầm trên dữ liệu của tiếng nói dẫn tập.

BEATs (Chen et al., 2022) là một bộ biến đổi tự giám sát được đào tạo trên AudioSet.

> BEATs(Chen 等人,2022) được đào tạo trên AudioSet trên tự giám sát Transformer──在相同参数下比 语更好地捕捉音乐和环境声──

AF-Whisper (Audio Flamingo 3's hybrid): Concat Whisper + BEATs có tính năng như đầu vào âm thanh.

> AF-Whisper(Audio Flamingo 3 的混合方案):拼音 Whisper + BEATs 特征作为音频输入──Whisper 携带语言信号,BEATs 携带声学信号──

### Audio Q-former

Tương tự như hình mẫu hình ảnh Q-former của BLIP-2. Một số lượng cố định của các truy vấn có thể học (thường là 32 hoặc 64) tham gia qua các khung sản xuất của bộ mã hóa âm thanh. Các truy vấn trở thành các token âm thanh được tiêu thụ bởi LLM.

> Với BLIP-2 của quan điểm Q-trước đây tương tự mô hình.

Giai đoạn sắp xếp đào tạo: Q-former đơn độc, giảm điểm + ghi chú trên cặp âm thanh văn bản (AudioCaps, Clotho).

> 训练对齐阶段:仅 Q-former,音频-文本对上对比+描述损失(AudioCaps、Clotho) 』 chỉ định阶段:端到端,解 LLM,在指令数据上训练──

### Vòng vòm  SALMONN, Qwen-Audio, AF3

SALMONN (Tang et al., 2023): Whisper + BEATs + Q-former + LLaMA.

> SALMONN(Tang 等人,2023):Tầm + BEATs + Q-former + LLaMA。第一个具有严推理能力的开放音频 LLM。MMAU 基准综合约 0.55。

Qwen-Audio (Chu et al., 2023): kiến trúc tương tự, được đào tạo trên một bộ dữ liệu phong phú hơn, được điều chỉnh cho đối thoại nhiều lượt. MMAU ~ 0,60.

> Qwen-Audio(Chu 等人,2023): tương tự cấu trúc, trong tập hợp dữ liệu phong phú hơn, tập luyện, để cải thiện nhiều vòng đối thoại.

LTU  Listen, Think, Understand (Gong et al., 2023): dữ liệu lý luận rõ ràng, tập trung vào chuỗi suy nghĩ hơn các clip âm thanh.

> LTU听、想、理解(Gong 等人,2023):显式推理数据,专注于音频片段上的链式思考──更小但更专注──

Audio Flamingo 3 (Goel et al., tháng 7 năm 2025): SOTA mở hiện tại. 8B LLM backbone (Qwen2 7B), Whisper-large encoder concat BEATs, 64-query Q-former, đào tạo trên 1M + cặp hướng dẫn văn bản âm thanh. MMAU 0.72, phù hợp với biên giới độc quyền trên một số nhiệm vụ phụ.

> Audio Flamingo 3(Goel 等人,2025年7月):当前开放 SOTA──8B LLM 主干(Qwen2 7B),Whisper-big 编码器拼接 BEATs,64 查询 Q-former,在100万+音频-文本指令对上训练──MMAU 0.72,在某些子任务上匹配闭源前沿──

AF3 cũng giới thiệu chuỗi suy nghĩ theo yêu cầu cho âm thanh: mô hình có thể tùy chọn phát ra các token suy nghĩ ("hãy cho tôi xác định các công cụ trước: ...") trước khi trả lời cuối cùng. Độ chính xác trong các nhiệm vụ suy luận phức tạp nâng cao 3-5 điểm khi suy nghĩ được bật.

> AF3 cũng giới thiệu các hệ thống suy nghĩ: mô hình có thể được trả lời trước chọn tính để xuất mã tư tưởng.

### Cascaded vs end-to-end

Đường ống nước:

> 级联管道:

1. Whisper ghi âm → văn bản.
   Trung ngữ翻译:Whisper 将音频转录为文本──
2. Lý do LLM trên văn bản.
   Trung văn翻译:LLM đối với văn bản để tiến hành suy luận.

Làm việc hoàn hảo cho "đánh lại podcast này". Không thành công cho:
- "Cái tâm trạng của bài hát này là gì?"  tâm trạng là trong âm thanh, không phải từ ngữ.
- "Ai đang nói, Alice hay Bob?"  đòi hỏi phải xác định người nói.
- "Vào giây nào vụ nổ xảy ra?"  Địa điểm thời gian bị mất trong văn bản.
- "Đây là âm thanh thực sự hay được tạo ra?"  Phát hiện deepfake cần các tính năng âm thanh.

> Đối với "总结这个播客" hoàn toàn phù hợp. Nhưng trong các trường hợp sau đây thất bại:
> - "Cái tình của bài hát này là gì?"
> - "Ai đang nói chuyện, Alice là Bob?"
> - "Bùng nổ trong vài giây?" trong văn bản đã mất thời gian.
> - "Đây là âm thanh thật hay là phát sinh?"

End-to-end bảo tồn tín hiệu âm thanh. Qwen-Audio và AF3 xử lý âm nhạc, môi trường và cảm xúc theo cách bản địa.

> 端到端保留声学信号──Qwen-Audio 和 AF3 原生处理音乐、环境和情绪──

> **【中文解读】**级联管道 (Whisper 转录→LLM 推理) phù hợp với hoàn cảnh âm thanh thuần túy như bản tóm tắt của người nghe, nhưng không thể xử lý tình cảm âm nhạc, nói chuyện nhận dạng người, định vị thời gian, kiểm tra giả mạo sâu, etc. cần các đặc điểm âm thanh.

> **【拓展：金融场景的音频理解】**Trong lĩnh vực tài chính, hiểu âm thanh có thể được sử dụng: phân tích tình cảm của hội nghị tài chính, không chỉ là chuyển âm, còn có ngữ气 và调语)  nhận dạng lệnh thoại của người giao dịch, kiểm tra tình cảm của khách hàng theo dõi chất lượng, phân chia các bài phát của hội nghị.

### Công thức sản xuất 2026

Đối với một sản phẩm mới để hiểu âm thanh:

> 对于新音频理解产品:

- Nếu: bản sao là mục tiêu, không có âm nhạc, không có suy luận cảm xúc.
  Trung ngữ翻译:级联方案: Nếu mục tiêu là chuyển âm, không có âm nhạc, không cần tâm lý.
- AF3 / Qwen-Audio-family nếu: âm nhạc, cảm xúc, multi-speaker, hoặc lý luận âm thanh phức tạp.
  Trung ngữ翻译:AF3 / Qwen-Audio 系列: Nếu có âm nhạc、情绪、多人说话或复杂音频推理──

Cascaded rẻ hơn và đơn giản hơn.

> 级联更便宜更简单――端到端更强大――

### MMAU  điểm chuẩn lý luận âm thanh

MMAU (Masssive Multimodal Audio Understanding) là tiêu chuẩn lý luận âm thanh 2024-2025:

> MMAU (MMAU) là cơ sở chính của các dự án âm thanh trong giai đoạn 2024-2025.

- 10.000 cặp âm thanh qua âm thanh, âm nhạc, âm thanh môi trường.
  Trung ngữ翻译:10,000 个跨语音、音乐、环境声的音频-文本 QA 对──
- Bao gồm phân loại, lý luận thời gian, lý luận nguyên nhân, QA mở.
  Trung文翻译:覆盖分类、时间推理、因果推理、开放式 QA。
- Kiểm tra những đường ống nước bị rơi xuống ngập nước mà hệ thống bị bỏ lỡ.
  Trung ngữ翻译:测试级联管道系统性遗漏的内容.

Open SOTA (AF3) ở mức 0,72; biên giới độc quyền ~ 0,78 (Gemini 2.5 Pro, Claude Opus 4.7).

> 开源 SOTA(AF3) 0.72;闭源前沿约0.78(Gemini 2.5 Pro、Claude Opus 4.7)。差距小于VideoMME 的开源-闭源差距,说明音频 LLM 正在成熟──

## Hãy sử dụng nó để thực hiện
```figure
audio-text-ctc
```

## Sử dụng nó

`code/main.py`- Có thể là:

- Thực hiện tính toán quang phổ log-Mel trong stdlib: windowsing, DFT ngây thơ, filter-bank Mel.
  Trung文翻译:用标准库实现 log-Mel 频谱图计算:窗口化、朴素 DFT、Mel 波器组。
- Audio Q-ex xương: được cung cấp khung phát ra bộ mã hóa, tính toán Q, K, V, chú ý, và phát ra N token.
  Trung文翻译:音频 Q-former 骨架:给定编码器输出,计算 Q、K、V、注意力并输出 N 个代币──
- So sánh giữa các trò chơi với nhau.
  Trung ngữ翻译: đối phó với các chương trình cấp liên với kết thúc trên nhiệm vụ đồ chơi.

## Chuyển nó đi.

Bài học này sẽ mang lại kết quả `outputs/skill-audio-llm-pipeline-picker.md`. Với một nhiệm vụ âm thanh (tác giả, gắn thẻ âm nhạc, suy luận cảm xúc, nhật ký đa loa, phân loại môi trường), nó chọn AF3 kết thúc đến kết thúc hoặc lai.

> 本课产 出 `outputs/skill-audio-llm-pipeline-picker.md`◊ cho định thanh频 nhiệm vụ (转录、音乐标注、情绪推断、多人说话分离、环境分类), nó chọn cấp liên kết、端到端 AF3 或混合方案。

## Tập luyện bài tập

1. Xét kích thước quang phổ log-Mel cho một clip 30 giây ở 16kHz, cửa sổ 25ms, nhảy 10ms, 80 Mel bins.

2. Tại sao Whisper hoạt động kém trong âm nhạc? Những tính năng âm thanh nào mà BEATs ghi lại mà Whisper không? Tại sao Whisper trong âm nhạc không hoạt động tốt?

3. Audio Q-former với 64 truy vấn so với 32: ở độ phức tạp của nhiệm vụ nào 64 trả giá? 32 lưu tính toán cho cái gì? 64 查询 so với 32 查询 của Audio Q-former: 在什么任务复杂度下 64 更值得?32 节省了什么计算?

4. Đọc AF3 Phần 4 về suy nghĩ theo yêu cầu. đề xuất ba nhiệm vụ âm thanh mà chuỗi suy nghĩ giúp ích nhiều nhất.

5. Thực hiện một đường ống nhật ký tối thiểu sử dụng đầu ra AF3. Làm thế nào để báo hiệu thay đổi loa? sử dụng AF3 输出实现一个最小的说话人分离管道.

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|------------------------|---------|
| Log-Mel spectrogram | "Mel features" Mel 频谱 | 2D (time, frequency) array of log-magnitude values after Mel filter banks 经 Mel 滤波器组后的对数幅度二维数组 | |
| Audio Q-former | "Audio Perceiver" 音频感知器 | Cross-attention bottleneck from audio encoder output to fixed-length queries feeding the LLM 音频编码器输出到固定长度查询的交叉注意力瓶颈 | |
| Cascaded | "ASR-then-LLM" 级联管道 | Pipeline where Whisper transcribes and a text LLM reasons; loses acoustic information Whisper 转录后文本 LLM 推理的管道；丢失声学信息 | |
| End-to-end | "Audio-LLM" 端到端音频 LLM | Audio features enter the LLM directly via Q-former; preserves acoustic signal 音频特征通过 Q-former 直接进入 LLM；保留声学信号 | |
| BEATs | "Audio AudioSet encoder" 音频自监督编码器 | SSL transformer trained on AudioSet; strong on music + environmental sounds 在 AudioSet 上训练的自监督 Transformer；擅长音乐和环境声 | |
| MMAU | "Audio reasoning bench" 音频推理基准 | 10k QA pairs across speech, music, environment; 2024 eval standard 跨语音、音乐、环境的 1 万条 QA；2024 年评估标准 | |
| On-demand thinking | "Audio CoT" 按需音频思考 | Model can optionally emit reasoning tokens before final answer, lifts accuracy 3-5 pts 模型可在最终回答前输出推理 token，提升准确率 3-5 个百分点 | |

## Xem thêm 延伸阅读

- [Radford et al. — Whisper (arXiv:2212.04356)](https://arxiv.org/abs/2212.04356)
- [Chu et al. — Qwen-Audio (arXiv:2311.07919)](https://arxiv.org/abs/2311.07919)
- [Goel et al. — Audio Flamingo 3 (arXiv:2507.08128)](https://arxiv.org/abs/2507.08128)
- [Tang et al. — SALMONN (arXiv:2310.13289)](https://arxiv.org/abs/2310.13289)
- [Gong et al. — LTU (arXiv:2305.10790)](https://arxiv.org/abs/2305.10790)
