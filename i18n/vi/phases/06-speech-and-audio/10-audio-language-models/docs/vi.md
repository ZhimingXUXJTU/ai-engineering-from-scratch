# Mô hình tiếng  Qwen2.5 Omni, Audio Flamingo, GPT-4o Audio 音频语言模型

> Các mô hình ngôn ngữ âm thanh 2026 suy luận về ngôn ngữ + âm thanh môi trường + âm nhạc. Qwen2.5-Omni-7B phù hợp với GPT-4o Audio trên MMAU-Pro. Audio Flamingo Next đánh bại Gemini 2.5 Pro trên LongAudioBench. Khoảng cách giữa mở và đóng về cơ bản là đóng  ngoại trừ các nhiệm vụ đa âm thanh, nơi mọi người gần như ngẫu nhiên.

> **【中文解读】**2026 năm của các mô hình ngôn ngữ âm thanh có thể hiểu语音+环境声+音乐──Qwen2.5-Omni-7B trên MMAU-Pro trên phù hợp GPT-4o Audio,Audio Flamingo Next trên LongAudioBench trên vượt qua Gemini 2.5 Pro──đánh nguồn và đóng nguồn khác biệt đã biến mất cơ bản──

> **【拓展：音频大模型的新时代】**音频语言模型 sẽ mở rộng khả năng suy luận của LLM sang lĩnh vực 音频, có thể đồng thời hiểu nội dung tiếng nói, nhận dạng môi trường âm thanh, phân tích cấu trúc âm nhạc. Đây là một hướng quan trọng của AI đa dạng.

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 04 (ASR), Phase 12 · 03 (Vision-Language Models), Phase 7 · 10 (Audio Transformers) | **前置知识:** 阶段 6 · 04（ASR），阶段 12 · 03（视觉语言模型），阶段 7 · 10（音频 Transformer）
**Time:** ~45 minutes | **预计用时:** ~45 分钟

## Vấn đề  vấn đề giới thiệu

Bạn có 5 giây âm thanh: chó quát, ai đó hét "hãy dừng!", sau đó im lặng.

> Bạn có 5 giây: chó kêu, ai đó kêu "hết!", rồi là tĩnh音.

> **【中文解读】**Câu hỏi được đặt ra trong phần này là: làm thế nào để hiểu và áp dụng đúng công nghệ này trong công trình thực tế.

- **Transcription.**"Cái gì đã được nói?"  Lãnh thổ ASR.
  **转录。**" nói đã gì?"
- **Semantic reasoning.**"Người đó có nguy hiểm không?"  đòi hỏi sự hiểu biết chung về tiếng la hét + hét lên + im lặng.
  **语义推理。**"Đây là người nguy hiểm không?" cần phải cùng hiểu chó gọi + 喊 + 静音──
- **Music reasoning.**"Những nhạc cụ nào chơi giai điệu?"
  **音乐推理。**"What instrument playing melody?"
- **Long-audio retrieval.**"Trong bài giảng 90 phút này, vị giảng viên giải thích sự giảm độ ở đâu?"
  **长音频检索。**"Trong buổi nói chuyện 90 phút này, vị giảng viên ở đâu giải thích sự giảm thang?"

Một mô hình đơn lẻ trả lời tất cả những câu hỏi này với một lời nhắc nhở là một **audio-language model**(LALM / ALM). tách biệt với ASR tinh khiết: LALM tạo ra các câu trả lời tự do bằng ngôn ngữ tự nhiên, không chỉ là bản ghi.

> Với một gợi ý, trả lời tất cả những câu hỏi này là một mô hình đơn giản.**音频语言模型**(LALM / ALM) 区别于纯 ASR:LALM 生成自由形式的自然语言答案, không chỉ là chuyển thể văn bản

## Khái niệm cốt lõi

> **【中文解读】**Bài viết này giới thiệu các khái niệm và lý thuyết cốt lõi.


![Audio-language model: audio encoder + projector + LLM decoder](../assets/alm-architecture.svg)

### Mô hình ba thành phần

Mỗi LALM năm 2026 đều có cùng một bộ xương:

> ### 三组件模板

> Năm 2026 mỗi LALM đều có cùng một cấu trúc:

1. **Audio encoder.**Whisper encoder · BEATs · CLAP · WavLM · hoặc một bộ encoder tùy chỉnh cho mỗi mô hình.
   **音频编码器。**Whisper 编码器 · BEATs · CLAP · WavLM · 或每个模型的自定义编码器──
2. **Projector.**Các tính năng mã âm thanh nối tuyến tính hoặc MLP vào không gian nhúng token của LLM.
   **投影器。**Để tạo ra các mô hình của LLM, bạn có thể sử dụng các mô hình của các mô hình này.
3. **LLM.**Llama / Qwen / Gemma dựa trên decoder. lấy văn bản liên kết + mã thông báo âm thanh; tạo văn bản.
   **LLM。**基于 Llama / Qwen / Gemma 的解码器──接收交织的文本 + 音频代码;生成文本──

Việc đào tạo:

> 训练:

- **Stage 1.**Freeze encoder + LLM; tàu chiếu chỉ trên dữ liệu ASR / captioning.
  **阶段 1。**结编码器 + LLM; chỉ được đào tạo trên ASR/标注数据投影器。
- **Stage 2.**Định nghĩa âm thanh đầy đủ / LoRA về các nhiệm vụ âm thanh theo hướng dẫn (QA, lý luận, hiểu âm nhạc).
  **阶段 2。**Trong lệnh theo dõi các nhiệm vụ âm thanh (QA、推理、音乐理解) thực hiện toàn bộ các tham số / LoRA 微调。
- **Stage 3 (optional).**Voice-in / voice-out thêm một bộ giải mã giọng nói. Qwen2.5-Omni và AF3-Chat làm điều này.
  **阶段 3（可选）。**语音入/语音出添加语音解码器──Qwen2.5-Omni 和 AF3-Chat 实现这一点──

### Bản đồ mô hình 2026

> ### 2026 năm模型地图

| Model | Backbone | Audio encoder | Output modality | Access |
|-------|----------|---------------|-----------------|--------|
| Qwen2.5-Omni-7B | Qwen2.5-7B | Custom + Whisper | text + speech | Apache-2.0 |
| Qwen3-Omni | Qwen3 | Custom | text + speech | Apache-2.0 |
| Audio Flamingo 3 | Qwen2 | AF-CLAP | text | NVIDIA non-commercial |
| Audio Flamingo Next | Qwen2 | AF-CLAP v2 | text | NVIDIA non-commercial |
| SALMONN | Vicuna | Whisper + BEATs | text | Apache-2.0 |
| LTU / LTU-AS | Llama | CAV-MAE | text | Apache-2.0 |
| GAMA | Llama | AST + Q-Former | text | Apache-2.0 |
| Gemini 2.5 Flash/Pro (closed) | Gemini | proprietary | text + speech | API |
| GPT-4o Audio (closed) | GPT-4o | proprietary | text + speech | API |

| 模型 | 骨干 | 音频编码器 | 输出模态 | 访问方式 |
|------|------|-----------|---------|---------|
| Qwen2.5-Omni-7B | Qwen2.5-7B | 自定义 + Whisper | 文本+语音 | Apache-2.0 |
| Qwen3-Omni | Qwen3 | 自定义 | 文本+语音 | Apache-2.0 |
| Audio Flamingo 3 | Qwen2 | AF-CLAP | 文本 | NVIDIA 非商业 |
| Audio Flamingo Next | Qwen2 | AF-CLAP v2 | 文本 | NVIDIA 非商业 |
| SALMONN | Vicuna | Whisper + BEATs | 文本 | Apache-2.0 |
| LTU / LTU-AS | Llama | CAV-MAE | 文本 | Apache-2.0 |
| GAMA | Llama | AST + Q-Former | 文本 | Apache-2.0 |
| Gemini 2.5 Flash/Pro（闭源） | Gemini | 专有 | 文本+语音 | API |
| GPT-4o Audio（闭源） | GPT-4o | 专有 | 文本+语音 | API |

### Kiểm tra thực tế chuẩn (2026)

**MMAU-Pro.**1800 cặp QA bao gồm giọng nói / âm thanh / âm nhạc / hỗn hợp.

| Model | Overall | Speech | Sound | Music | Multi-audio |
|-------|---------|--------|-------|-------|-------------|
| Gemini 2.5 Pro | ~60% | 73.4% | 51.9% | 64.9% | ~22% |
| Gemini 2.5 Flash | ~57% | 73.4% | 50.5% | 64.9% | 21.2% |
| GPT-4o Audio | 52.5% | — | — | — | 26.5% |
| Qwen2.5-Omni-7B | 52.2% | 57.4% | 47.6% | 61.5% | ~20% |
| Audio Flamingo 3 | ~54% | — | — | — | — |
| Audio Flamingo Next | SOTA on LongAudioBench | — | — | — | — |

- **multi-audio column is damning for everyone.**Cơ hội ngẫu nhiên trên 4 lựa chọn nhiều lựa chọn = 25%; hầu hết các mô hình ghi điểm xung quanh đó. LALM vẫn gặp khó khăn để so sánh hai clip.

> **多音频列对所有人都是致命的。**4 选择 1 多选题的随机概率 = 25%; hầu hết các mô hình có điểm là gần đó.

### Lâu đài LALM có ích vào năm 2026

- **Compliance audit of call-center recordings.**"Đội ngũ đã đề cập đến việc tiết lộ yêu cầu không?"
  **合规审计通话录音。**" khách hàng có đề cập đến một tuyên bố miễn phí cần thiết không?"
- **Accessibility.**Mô tả các sự kiện âm thanh cho người dùng điếc (không chỉ là bản sao).
  **无障碍。**为听障用户描述声音事件(不只是转录)
- **Content moderation.**Khám phá ngôn ngữ bạo lực + giọng nói đe dọa + bối cảnh nền.
  **内容审核。**检测暴力语言 + 威胁语气 + 背景上下文。
- **Podcast / meeting chaptering.**Kết luận ngữ nghĩa, không chỉ là quay người nói.
  **播客/会议章节化。**语义摘要, không chỉ nói chuyện người lượt sau.
- **Music catalog analysis.**"Xem tất cả các đường ray với một thay đổi khóa phần B".
  **音乐目录分析。**"Hãy tìm ra tất cả các đoạn B có chuyển đổi của các bài hát:"

### Khi chúng không (vẫn) hữu ích

- Lý thuyết âm nhạc tinh tế (dưới mức hợp âm).
  精细音乐理论(和弦级别以下)
- Lý luận do người nói về các cuộc trò chuyện dài (tăng độ qua 10 phút).
  长对话中的说话人归因推理 (trên hơn 10 phút trôi qua)
- So sánh đa âm thanh (22-26% chỉ là trên ngẫu nhiên).
  多音频比较(22-26% 几乎等于随机)
- Nguyên lý phát trực tuyến thời gian thực (hầu hết là suy luận hàng loạt ngoại tuyến).
  Thực tế: Hầu hết là các loại hàng không

> **【中文解读】**本节通过代码实现核心算法从零――这种" từ đầu"的方式能帮助理解框架背后的原理,遇到问题时不会被黑盒困住――

> **【拓展：语音 AI 的产品化】**语音技术在产品化中面临独特挑战:不同口音,背景噪音,远场拾音,多人说话等. Siri, Alexa,小爱同学等产品都投入大量工程优化解决这些长尾问题.

> **【拓展：多语言语音技术】**Các đặc điểm ngữ âm của toàn cầu ngôn ngữ khác biệt rất lớn: tiếng调 ngôn ngữ (如中文) của âm cao mang ngữ nghĩa, nguồn lực thấp ngôn ngữ thiếu đào tạo dữ liệu.




## Hãy xây dựng nó.
```figure
v4-alm-tokens
```

## Hãy xây dựng nó

### Bước 1: truy vấn Qwen2.5-Omni

```python
from transformers import AutoModelForCausalLM, AutoProcessor

processor = AutoProcessor.from_pretrained("Qwen/Qwen2.5-Omni-7B")
model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-Omni-7B", torch_dtype="auto")

audio, sr = load_wav("clip.wav", sr=16000)
messages = [{
    "role": "user",
    "content": [
        {"type": "audio", "audio": audio},
        {"type": "text", "text": "What sounds do you hear, and what's happening?"},
    ],
}]
inputs = processor.apply_chat_template(messages, tokenize=True, return_tensors="pt")
output = model.generate(**inputs, max_new_tokens=200)
print(processor.decode(output[0], skip_special_tokens=True))
```

### Bước 2: mô hình máy chiếu

```python
import torch.nn as nn

class AudioProjector(nn.Module):
    def __init__(self, audio_dim=1280, llm_dim=4096):
        super().__init__()
        self.down = nn.Linear(audio_dim, llm_dim)
        self.act = nn.GELU()
        self.up = nn.Linear(llm_dim, llm_dim)

    def forward(self, audio_features):
        return self.up(self.act(self.down(audio_features)))
```

Đó là tất cả. máy chiếu thường là 1-3 lớp tuyến tính. đào tạo nó trên cặp ASR (audio → transcript) là nhiệm vụ tiền đề giai đoạn 1.

### Bước 3: đánh giá chuẩn MMAU / LongAudioBench

```python
from datasets import load_dataset
mmau = load_dataset("MMAU/MMAU-Pro")

correct = 0
for item in mmau["test"]:
    answer = call_model(item["audio"], item["question"], item["choices"])
    if answer == item["correct_choice"]:
        correct += 1
print(f"Accuracy: {correct / len(mmau['test']):.3f}")
```

> **【中文解读】**Bài này sẽ trình bày cách sử dụng một khung đã phát triển như PyTorch, HuggingFace, và các khác.


Báo cáo cho từng loại (nhân ngữ / âm thanh / âm nhạc / đa âm thanh) riêng biệt.




> **【拓展：语音与情感计算】**语音 không chỉ truyền tải thông tin văn bản, còn mang lại một tín hiệu cảm xúc phong phú (语调、语速、音高变化)  cảm xúc (语音识别, Speech Emotion Recognition, SER) có ứng dụng rộng rãi trong lĩnh vực kiểm tra chất lượng khách hàng, giám sát sức khỏe tâm thần, giáo dục thông minh, etc.  Mô hình SOTA hiện tại thường dựa trên wave2vec 2.0 hoặc HuBERT 等

## Hãy sử dụng nó để thực hiện

| Task | 2026 pick |
|------|-----------|
| Free-form audio QA (open) | Qwen2.5-Omni-7B |
| Best open on long audio | Audio Flamingo Next |
| Best closed | Gemini 2.5 Pro |
| Voice-in / voice-out agent | Qwen2.5-Omni or GPT-4o Audio |
| Music reasoning | Audio Flamingo 3 or 2 (music-specialized AF-CLAP) |
| Call-center audit | Gemini 2.5 Pro via API, with RAG over your policy docs |

| 任务 | 2026 年选择 |
|------|-----------|
| 自由格式音频 QA（开源） | Qwen2.5-Omni-7B |
| 最佳开源长音频 | Audio Flamingo Next |
| 最佳闭源 | Gemini 2.5 Pro |
| 语音入/语音出智能体 | Qwen2.5-Omni 或 GPT-4o Audio |
| 音乐推理 | Audio Flamingo 3 或 2（音乐专用 AF-CLAP） |
| 呼叫中心审计 | Gemini 2.5 Pro via API，配合策略文档 RAG |



## Những bẫy

> 常见陷

- **Over-trust on multi-audio.**Nếu nhiệm vụ của bạn cần "clip nào có X", hiệu suất theo cấp tình cờ là thực.
  **过度信任多音频。**Nếu nhiệm vụ của bạn cần "một đoạn có X", thì hiệu suất của một trình độ ngang là thực.
- **Long-audio degradation.**10 phút sau, hầu hết các mô hình có thể không được phân tích.
  **长音频退化。**超过10分钟, hầu hết các mô hình nói chuyện người ta bị kết luận thất bại.
- **Hallucinations on silence.**Vấn đề kiểu Whisper giống như LALM, sử dụng mã hóa Whisper.
  **静音上的幻觉。**Với sử dụng Whisper 编码器的 LALM 继承的 Whisper 式问题相同──用 VAD 过──
- **Benchmark cherry-picking.**Các bài đăng trên blog của nhà cung cấp nhấn mạnh các loại trường hợp tốt nhất.
  **基准挑挑拣拣。**供应商博客文章突出最佳类别──自运行 MMAU-Pro 多音频子集──

> **【中文解读】**Phần này tập trung vào cách phân phối mô hình như một sản phẩm có thể sử dụng.


## Chuyển nó đi.

Cứ như `outputs/skill-alm-picker.md`. Chọn LALM + phân nhóm tham chiếu + mô hình đầu ra (text vs speech) cho một nhiệm vụ hiểu âm thanh nhất định.

> 保存为 `outputs/skill-alm-picker.md`◊为给定的音频理解任务选择 LALM + 基准子集 + 输出模态(文本 vs 语音) ◊

## Tập luyện bài tập

1. **Easy.**Đi chạy`code/main.py`để xem mô hình máy chiếu đồ chơi + đường dẫn LALM giả của (audio-embedding, text-tokens) → output tokens.
   **简单。**运行 `code/main.py`查看玩具投影器模式 + 假 LALM 路由(音频嵌入,文本代币)→ 输出代币──
2. **Medium.**Đánh điểm Qwen2.5 Omni-7B trên 100 bài phát biểu MMAU-Pro. So sánh với số báo cáo của báo.
   **中等。**Trong 100 bài MMAU-Pro 语音项评分 Qwen2.5-Omni-7B──与论文报告的数字比较──
3. **Hard.**Xây dựng một dòng gốc ghi âm tối thiểu: BEATs encoder + máy chiếu 2 lớp + Llama-3.2-1B đóng băng. Chỉ chỉnh sửa kỹ các máy chiếu trên AudioCaps. So sánh với SALMONN trên Clotho-AQA.
   **困难。**构建最小音频标注基线:BEATs 编码器 + 2层投影器 + 结 Llama-3.2-1B── chỉ ở AudioCaps 上微调投影器──在 Clotho-AQA 上与 SALMONN 比较──

> **【中文解读】**Trong 术语表中的"Những gì mọi người nói" vs "Những gì nó thực sự có nghĩa" 区分日常口语和精确技术含义── 在团队协作中,统一术语定义可以避免大量沟通误解──


## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| LALM | Audio ChatGPT | Audio encoder + projector + LLM decoder. |
| Projector | Adapter | Small MLP mapping audio features into LLM embedding space. |
| MMAU | The benchmark | 10k audio-QA pairs across speech, sound, music. |
| MMAU-Pro | Harder MMAU | 1800 multi-audio / reasoning-heavy questions. |
| LongAudioBench | Long-form eval | Multi-minute clips with semantic queries. |
| Voice-in / voice-out | Speech-native | Model ingests speech and emits speech without text detour. |

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| LALM | 音频 ChatGPT | 音频编码器 + 投影器 + LLM 解码器。 |
| 投影器 | 适配器 | 将音频特征映射到 LLM 嵌入空间的小型 MLP。 |
| MMAU | 那个基准 | 跨语音、声音、音乐的 1 万音频-QA 对。 |
| MMAU-Pro | 更难的 MMAU | 1800 个多音频/重推理问题。 |
| LongAudioBench | 长音频评估 | 带语义查询的多分钟片段。 |
| 语音入/语音出 | 原生语音 | 模型直接接收和输出语音，不经文本。 |

> **【中文解读】**延伸阅读 cung cấp các nguồn chất lượng cao cho việc học sâu. Những bài báo và giảng dạy này là tài liệu tham khảo cổ điển trong lĩnh vực này, phù hợp với những người đọc cần hiểu sâu hơn.


## Xem thêm 延伸阅读

- [Chu et al. (2024). Qwen2-Audio](https://arxiv.org/abs/2407.10759) kiến trúc tham chiếu.
  Chu 等 (2024). Qwen2-Audio 参考架构──
- [Alibaba (2025). Qwen2.5-Omni](https://huggingface.co/Qwen/Qwen2.5-Omni-7B) nói chuyện trong nói chuyện.
  Alibaba (2025). Qwen2.5-Omni语音入语音出。
- [NVIDIA (2025). Audio Flamingo 3](https://arxiv.org/abs/2507.08128) người dẫn đầu âm thanh mở dài.
  NVIDIA (2025). Audio Flamingo 3开源长音频领先者
- [NVIDIA (2026). Audio Flamingo Next](https://arxiv.org/abs/2604.10905) LongAudioBench SOTA.
  NVIDIA (2026). Audio Flamingo NextLongAudioBench SOTA──
- [Tang et al. (2023). SALMONN](https://arxiv.org/abs/2310.13289) tiên phong trong việc mã hóa kép.
  Tang 等 (2023). SALMONN双编码器先驱──
- [MMAU-Pro leaderboard](https://mmaubenchmark.github.io/) Live 2026 xếp hạng.
  MMAU-Pro 排行榜2026 年实时排名──

> **【中文解读】**延伸阅读 cung cấp các nguồn chất lượng cao để học sâu, bao gồm các bài báo, giảng dạy và công cụ.

