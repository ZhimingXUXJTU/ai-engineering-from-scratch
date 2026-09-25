# Streaming Speech-to-Speech  Moshi, Hibiki, và Full-Duplex Dialogue  流式语音到语音  Moshi、Hibiki 与全双工对话

> 2024-2026 định nghĩa lại AI giọng nói. Moshi đưa ra một mô hình duy nhất nghe và nói đồng thời với độ trễ 200 ms. Hibiki thực hiện dịch thuật từ nói đến nói từng phần. Cả hai đều từ bỏ đường ống ASR → LLM → TTS để tạo ra kiến trúc tổng hợp đầy đủ duplex trên mã codec Mimi. Đây là thiết kế tham chiếu mới.

> **【中文解读】**2024-2026 năm tái định nghĩa âm thanh AI。Moshi sử dụng một mô hình duy nhất trong 200ms 延迟内同时听和说。Hibiki 逐块进行语音到语音翻译。 cả hai đều từ bỏ ASR→LLM→TTS 流水线, áp dụng dựa trên Mimi 编解码器 token 统一全双工构── đây là thiết kế tham khảo mới。

> **【拓展：全双工语音 AI】**傳統语音助手是"半双工" (听时不能说),Moshi 实现了"全双工" (全双工) (听时不能说),就像人类自然对话一样――这是2026年语音 AI 最前沿的方向――

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 13 (Neural Audio Codecs), Phase 6 · 11 (Real-Time Audio), Phase 7 · 05 (Full Transformer) | **前置知识:** 阶段 6 · 13（神经音频编解码器），阶段 6 · 11（实时音频），阶段 7 · 05（完整 Transformer）
**Time:** ~75 minutes | **预计用时:** ~75 分钟

## Vấn đề  vấn đề giới thiệu

Mỗi đại lý giọng nói được xây dựng từ Bài học 11 + 12 có một tầng độ trễ cơ bản khoảng 300-500 ms: VAD cháy, quy trình STT, LLM lý do, TTS tạo ra. Mỗi giai đoạn có độ trễ tối thiểu của riêng nó. Bạn có thể điều chỉnh và song song, nhưng hình dạng đường ống phủ bạn.

> 基于第11和12课构建的每个语音助手都有一个约300-500 ms的基础延迟下限:VAD 触发、STT 处理、LLM 推理、TTS 生成──每个阶段都有自己的最小延迟──你可以调优和并行化,但流水线架构本身限制你──

> **【中文解读】**Câu hỏi được đặt ra trong phần này là: làm thế nào để hiểu và áp dụng đúng công nghệ này trong công trình thực tế.


Moshi (Kyutai, 2024-2026) đặt ra một câu hỏi khác: nếu không có đường ống thì sao?

> Moshi ((Kyutai,2024-2026) đưa ra một vấn đề khác: nếu không có dòng nước? Nếu một mô hình trực tiếp tiếp tiếp nhận âm thanh nhập và xuất âm thanh, văn bản chỉ là một giai đoạn "内心独白" giữa chứ không phải là giai đoạn cần thiết?

Câu trả lời là:**full-duplex speech-to-speech**. độ trễ lý thuyết 160 ms (80 ms Mimi khung hình + 80 ms chậm âm thanh). độ trễ thực tế 200 ms trên một GPU L4 duy nhất. Đó là một nửa những gì một đại lý tiếng nói ống dẫn tốt nhất trong lớp đạt được.

> Câu trả lời là:**全双工语音到语音**△ Theoretical delay 160 ms(80 ms Mimi  + 80 ms 声学延迟) ・・・ 在单张 L4 GPU 上实际延迟 200 ms──这是最好的流水线语音助手延迟的一半──

## Khái niệm cốt lõi

> **【中文解读】**Bài viết này giới thiệu các khái niệm và lý thuyết cốt lõi.


![Moshi architecture: two parallel Mimi streams + inner-monologue text](../assets/moshi-hibiki.svg)

### Kiến trúc Moshi

> Moshi 架构

**Inputs.**Hai dòng codec Mimi, cả hai ở 12,5 Hz × 8 codebook:

> **输入。**2 dòng máy tính, trung bình là 12,5 Hz × 8 个码本:

- Stream 1: âm thanh người dùng (Mimi-encoded, liên tục đến)
  Trung ngữ翻译:流 1:用户音频(Mimi 编码,持续到达)
- Stream 2: âm thanh của riêng Moshi (được tạo bởi Moshi)
  Trung ngữ翻译:流 2:Moshi 自身的音频(由Moshi 生成)

**The transformer.**Một biến đổi thời gian tham số 7B xử lý cả dòng và dòng văn bản "monolog nội bộ".

> **Transformer。**Một biến thể thời gian 70 tỷ parameter cùng lúc xử lý hai dòng và một dòng văn bản "内心独白" . Trong mỗi bước thời gian 80 ms, nó:

1. Tiêu thụ các token Mimi mới nhất (8 codebook).
   Trung ngữ翻译:消费最新的用户 Mimi token(8个码本)
2. Tiêu thụ các mã thông báo Moshi Mimi mới nhất (8 codebook, như đã sản xuất).
   Trung文翻译:消费最近生成的Moshi Mimi token(8个码本)
3. Tạo ra mã thông báo văn bản Moshi tiếp theo (mônolog bên trong).
   中文翻译:生成下一个 Moshi 文本 token (内心独白)
4. Tạo ra các mã thông báo Moshi Mimi tiếp theo (8 sổ mã thông qua một bộ biến đổi độ sâu nhỏ).
   Trung文翻译:生成下一组 Moshi Mimi token ((8 个码本, thông qua小型深度 Transformer) ⋅

Cả ba dòng  âm thanh người dùng, âm thanh Moshi, văn bản Moshi  chạy song song. Moshi có thể nghe người dùng trong khi nói; có thể tự gián đoạn khi người dùng gián đoạn; có thể quay lại kênh ("mhm") mà không phá vỡ phát biểu chính của nó.

> 三流用户音频、Moshi 音频、Moshi 文本并行运行──Moshi có thể nghe người dùng trong khi nói; có thể tự cắt đứt khi người dùng phá vỡ; có thể thực hiện phản("")。

**The depth transformer.**Trong một khung, 8 codebook không được dự đoán song song  chúng có phụ thuộc giữa codebook. Một "hình biến chiều sâu" 2 lớp nhỏ dự đoán chúng theo trình tự trong vòng 80 ms. Đây là yếu tố tiêu chuẩn cho LMs codec AR (còn được sử dụng bởi VALL-E, VibeVoice).

> **深度 Transformer。**Trong một 内,8 码本 không đồng hành dự đoán  giữa chúng tồn tại 码本间依赖. Một 2 tầng nhỏ "đối độ biến đổi" trong 80 ms tự序 dự đoán chúng. Đây là cách chuẩn hóa của mô hình ngôn ngữ tự归编解编码器.

### Tại sao văn bản trong một bài viết có ích

Nếu không có văn bản rõ ràng, mô hình phải mô hình hóa ngôn ngữ trong dòng âm thanh của nó. Nhìn của Moshi: buộc nó phát ra các mã thông báo văn bản cùng với âm thanh. dòng văn bản về cơ bản là bản sao chép của những gì Moshi nói. Điều này cải thiện sự liên tục ngữ nghĩa, giúp dễ dàng để thay đổi đầu mô hình ngôn ngữ, và cung cấp cho bạn bản sao miễn phí.

> Tại sao nội tâm độc lập văn bản có ích: không có văn bản rõ ràng, mô hình phải được ẩn trong dòng âm học trong dòng hình thành ngôn ngữ. Nhìn của Moshi: bắt buộc nó đồng thời xuất mã văn bản và âm thanh.

### Hibiki: dịch vụ phát trực tuyến từ từ từ

Thiết kế tương tự, được đào tạo trên các cặp dịch thuật. Source audio in, target language audio out, liên tục. Hibiki-Zero (Feb 2026) loại bỏ sự cần thiết cho dữ liệu đào tạo phù hợp ở mức từ ngữ  sử dụng dữ liệu ở mức câu + GRPO tăng cường học tập cho tối ưu hóa độ trễ.

> Hibiki:流式语音到语音翻译──相同的架构,使用翻译对训练──源语言音频输入,目标语言音频输出,持续进行── Hibiki-Zero(2026 年 2 月) loại bỏ nhu cầu về dữ liệu đào tạo đối với các lớp từ sử dụng dữ liệu về các lớp từ + GRPO 强化学习进行延迟优化──

Bốn cặp ngôn ngữ được hỗ trợ ban đầu; có thể được điều chỉnh cho một ngôn ngữ mới với ≈1000 giờ.

> Ban đầu hỗ trợ bốn ngôn ngữ đối với; có thể sử dụng khoảng 1000 giờ dữ liệu để phù hợp với các ngôn ngữ mới.

### Thống Kyutai rộng hơn (2026)

> 更广泛的 Kyutai 技术(2026 年)

- **Moshi** Đối thoại đầy đủ (tiếng Pháp trước, tiếng Anh được hỗ trợ tốt)
  Trung ngữ翻译:Moshi  全双工对话(法语优先,英语支持良好)
- **Hibiki / Hibiki-Zero** dịch thuật ngôn ngữ đồng thời
  中文翻译:Hibiki / Hibiki-Zero  同步语音翻译
- **Kyutai STT** streaming ASR (500 ms hoặc 2,5 s nhìn về phía trước)
  Trung文翻译:Kyutai STT  流式语音识别(500 ms hoặc 2,5 s 前视)
- **Kyutai Pocket TTS** 100M-param TTS chạy trên CPU (Từ 2026)
  Trung文翻译:Kyutai Pocket TTS  1 tỷ参数 TTS,可在 CPU 上运行(2026 年 1 月)
- **Unmute** toàn bộ đường ống kết hợp các máy chủ công cộng
  Trung ngữ翻译:Unmute  在公共服务器上组合这些组件的完整流水线

Tăng suất trên GPU L40S: 64 phiên đồng thời tại 3x thời gian thực.

> Trong L40S GPU trên: 64 个并发会话,3 倍实时速度──

### Sesame CSM  người anh em họ

Sesame CSM (2025) sử dụng một ý tưởng tương tự  một xương sống Llama-3 với đầu codec Mimi. Nhưng CSM là một hướng (giấy ngữ cảnh + văn bản, sản xuất giọng nói) thay vì đầy đủ.

> Sesame CSM(2025) sử dụng ý tưởng tương tự như Llama-3 骨干网络 + Mimi 编解码器头―― nhưng CSM là đơn hướng của(接收上下文 +文本,生成语音), chứ không phải là toàn bộ công trình―― nó là thị trường tốt nhất"语音存在感" TTS; nhưng không hoàn toàn giống với toàn bộ công trình của Moshi.

### Số hiệu suất 2026

| Model | Latency | Use case | License |
|-------|---------|----------|---------|
| Moshi | 200 ms (L4) | full-duplex English / French dialogue / 全双工英/法对话 | CC-BY 4.0 |
| Hibiki | 12.5 Hz framerate | French ↔ English streaming translation / 法↔英流式翻译 | CC-BY 4.0 |
| Hibiki-Zero | same | 5 language-pairs, no aligned data / 5 语言对，无需对齐数据 | CC-BY 4.0 |
| Sesame CSM-1B | 200 ms TTFA | context-conditioned TTS / 上下文条件 TTS | Apache-2.0 |
| GPT-4o Realtime | ~300 ms | closed, OpenAI API / 闭源，OpenAI API | commercial |
| Gemini 2.5 Live | ~350 ms | closed, Google API / 闭源，Google API | commercial |

> **【中文解读】**本节通过代码实现核心算法从零――这种" từ đầu"的方式能帮助理解框架背后的原理,遇到问题时不会被黑盒困住――

> **【拓展：语音 AI 的产品化】**语音技术在产品化中面临独特挑战:不同口音,背景噪音,远场拾音,多人说话等. Siri, Alexa,小爱同学等产品都投入大量工程优化解决这些长尾问题.

> **【拓展：多语言语音技术】**Các đặc điểm ngữ âm của toàn cầu ngôn ngữ khác biệt rất lớn: tiếng调 ngôn ngữ (如中文) của âm cao mang ngữ nghĩa, nguồn lực thấp ngôn ngữ thiếu đào tạo dữ liệu.




## Hãy xây dựng nó.
```figure
sp-fullduplex
```

## Hãy xây dựng nó

### Bước 1: giao diện

> 步骤 1:接口

Moshi đã phát hiện ra một máy chủ WebSocket lấy 80 ms âm thanh được mã hóa bởi Mimi và trả lại 80 ms âm thanh được mã hóa bởi Mimi.

> Moshi  Khám phá một WebSocket  máy chủ, nhận 80 ms của Mimi 编码音频块并返回 80 ms của Mimi 编码音频块──双向,持续进行──

```python
import asyncio
import websockets
from moshi.client_utils import encode_audio_mimi, decode_audio_mimi

async def moshi_chat():
    async with websockets.connect("ws://localhost:8998/api/chat") as ws:
        mic_task = asyncio.create_task(stream_mic_to(ws))
        spk_task = asyncio.create_task(stream_from_to_speaker(ws))
        await asyncio.gather(mic_task, spk_task)
```

### Bước 2: vòng lặp duplex đầy đủ

> 步骤 2: toàn bộ vòng lặp công nghiệp

```python
async def stream_mic_to(ws):
    async for chunk_80ms in mic_stream_at_12_5_hz():
        mimi_tokens = encode_audio_mimi(chunk_80ms)
        await ws.send(serialize(mimi_tokens))

async def stream_from_to_speaker(ws):
    async for msg in ws:
        mimi_tokens, text_token = deserialize(msg)
        audio = decode_audio_mimi(mimi_tokens)
        await play(audio)
```

Cả hai hướng chạy cùng một lúc. Python asyncio hoặc Rust tương lai là phương tiện giao thông tiêu chuẩn.

> 两个方向同时运行──Python asyncio 或 Rust futures là phương thức truyền tải tiêu chuẩn──

### Bước 3: mục tiêu đào tạo (tầm nhìn)

> 步骤 3: 训练目标 (trình thức)

Đối với mỗi khung 80 ms `t`- Có thể là:

> Đối với mỗi 80 ms của`t`- Có thể là:

- Nhập: `user_mimi[0..t]`- `moshi_mimi[0..t-1]`- `moshi_text[0..t-1]`
  Trung ngữ翻译:输入:`user_mimi[0..t]``moshi_mimi[0..t-1]``moshi_text[0..t-1]`
- Dự đoán: `moshi_text[t]`, sau đó `moshi_mimi[t, codebook_0..7]`
  Trung ngữ翻译:预测:`moshi_text[t]`, rồi là`moshi_mimi[t, codebook_0..7]`

Văn bản được dự đoán trước âm thanh (mônolog bên trong); âm thanh được dự đoán theo trình tự trong bộ biến đổi độ sâu.

> 文本在音频之前预测(内心独白);音频在深度 Transformer 内按码本顺序预测。

### Bước 4: nơi Moshi thắng và nơi không thắng

> Bước 4: Các ưu điểm và thiếu sót của Moshi

Moshi thắng:

> Ưu điểm của Moshi:

- Sub-250 ms từ đầu đến cuối trên phần cứng rẻ tiền.
  Trung ngữ翻译: 在廉价硬件上端到端低于250 ms。
- Các kênh quay lại tự nhiên và sự gián đoạn.
  Trung ngữ翻译:自然的反和打断能力──
- Không có mã dán ống dẫn.
  Trung ngữ翻译:无需流水线水代码──

Moshi không thắng:

> Mất điểm của Moshi:

- Công cụ gọi (không được đào tạo cho nó; bạn cần một con đường LLM riêng biệt).
  Trung ngữ翻译:工具调用 (未针对此训练;需要单独的 LLM 路径)
- Lý luận dài (Moshi là mô hình đối thoại 8B, không phải Claude/GPT-4).
  Trung文翻译:长链推理(Moshi là mô hình đối thoại của khoảng 80 tỷ参数, không phải là Claude/GPT-4)。
- Sự chính xác thực tế về các chủ đề niche.
  Trung ngữ翻译:小众话题的事实准确性──
- Hầu hết các trường hợp sử dụng của doanh nghiệp sản xuất (vẫn sử dụng đường ống vào năm 2026).
  Trung ngữ翻译: Hầu hết các doanh nghiệp cấp sản xuất vẫn sử dụng dòng nước vào năm 2026.

> **【中文解读】**Bài này sẽ trình bày cách sử dụng một khung đã phát triển như PyTorch, HuggingFace, và các khác.





> **【拓展：语音与情感计算】**语音 không chỉ truyền tải thông tin văn bản, còn mang lại một tín hiệu cảm xúc phong phú (语调、语速、音高变化)  cảm xúc (语音识别, Speech Emotion Recognition, SER) có ứng dụng rộng rãi trong lĩnh vực kiểm tra chất lượng khách hàng, giám sát sức khỏe tâm thần, giáo dục thông minh, etc.  Mô hình SOTA hiện tại thường dựa trên wave2vec 2.0 hoặc HuBERT 等

## Hãy sử dụng nó để thực hiện

| Situation | Pick |
|-----------|------|
| Lowest-latency voice companion / 最低延迟语音伴侣 | Moshi |
| Live translation call / 实时翻译通话 | Hibiki |
| Voice demo / research / 语音演示/研究 | Moshi, CSM |
| Enterprise agent with tools / 企业级带工具的 agent | Pipeline（第 12 课），不是 Moshi |
| Custom-voice TTS in context / 上下文中的自定义音色 TTS | Sesame CSM |
| Speech-to-speech, any languages / 任意语言的语音到语音 | GPT-4o Realtime 或 Gemini 2.5 Live（商业） |



## Những bẫy

> 常见陷

- **Limited tool calling.**Moshi là một mô hình đối thoại, không phải là một cơ sở hợp tác.
  Trung ngữ翻译:**有限的工具调用。**Moshi là mô hình đối thoại, không phải là một cơ quan 框架.
- **Specific-voice conditioning.**Moshi sử dụng một cá nhân được đào tạo duy nhất; Khẩu nhân là một cuộc tập luyện riêng biệt.
  Trung ngữ翻译:**特定语音调节。**Moshi sử dụng một người đào tạo đơn lẻ; Klon cần một quá trình đào tạo đơn lẻ.
- **Language coverage.**Tiếng Pháp + tiếng Anh là tuyệt vời; những người khác hạn chế. Hibiki-Zero giúp, nhưng bạn vẫn cần dữ liệu đào tạo.
  Trung ngữ翻译:**语言覆盖。**Pháp语 + 英语表现优秀;其他语言有限──Hibiki-Zero có giúp đỡ, nhưng vẫn cần đào tạo dữ liệu──
- **Resource cost.**Một phiên Moshi đầy đủ chứa một khe GPU; không phải một mô hình triển khai thuê nhà chia sẻ rẻ tiền.
  Trung ngữ翻译:**资源成本。**Một cuộc họp Moshi hoàn chỉnh chiếm một GPU 插槽; không phải là một mô hình phân phối thuê nhà rẻ tiền.

> **【中文解读】**Phần này tập trung vào cách phân phối mô hình như một sản phẩm có thể sử dụng.


## Chuyển nó đi.

Cứ như `outputs/skill-duplex-pipeline.md`Chọn đường ống so với kiến trúc duplex đầy đủ cho một khối lượng công việc đại lý giọng nói, hợp lý.

> 保存为 `outputs/skill-duplex-pipeline.md`❖ cho một trợ lý tiếng ❖ cho một người dùng tiếng ❖ cho một người dùng tiếng ❖ cho một người dùng tiếng ❖ cho một người dùng tiếng ❖ cho một người dùng tiếng ❖ cho một người dùng tiếng ❖ cho một người dùng tiếng ❖ cho một người dùng tiếng ❖ cho một người dùng tiếng ❖ cho một người dùng tiếng ❖ cho một người dùng tiếng ❖ cho một người dùng tiếng ❖ cho một người dùng tiếng ❖ cho một người dùng tiếng ❖ cho một người dùng tiếng ❖ cho một người dùng tiếng ❖ cho một người dùng tiếng ❖ cho một người dùng tiếng ❖ cho một người dùng tiếng ❖ cho một người dùng tiếng ❖ cho một người dùng tiếng ❖ cho một người dùng tiếng ❖ cho một người dùng tiếng ❖ cho một người dùng tiếng ❖ cho một người dùng tiếng ❖ cho một người dùng tiếng ❖ cho một người dùng tiếng ❖ cho một người dùng tiếng ❖ cho một người dùng tiếng ❖ cho một người dùng tiếng ❖ cho một người dùng tiếng ❖ cho một người ❖ cho một người ❖ cho một người ❖ cho một người ❖ cho một người ❖ cho một người ❖

## Tập luyện bài tập

1. **Easy.**Đi chạy`code/main.py`Nó mô phỏng kiến trúc hai dòng + monologue bên trong một cách tượng trưng.
   Trung ngữ翻译:**简单。**运行 `code/main.py` Nó có hình thức biểu tượng giống như hai dòng chảy + nội tâm độc lập cấu trúc
2. **Medium.**Nhổ Moshi từ HuggingFace, chạy máy chủ, thử một cuộc trò chuyện, đo độ trễ của đồng hồ tường từ cuối cuộc nói chuyện của người dùng đến bắt đầu phản ứng của Moshi.
   Trung ngữ翻译:**中等。**Từ HuggingFace 拉取 Moshi,运行服务器,测试一段对话──测量 từ người dùng语音结束到 Moshi 回复开始的实际延迟──
3. **Hard.**Hãy lấy đại lý đường ống học 12 của bạn và so sánh độ trễ P50 vs Moshi trên 20 bài kiểm tra phù hợp.
   Trung ngữ翻译:**困难。**Sử dụng thứ 12  课程流水线助手与Moshi 在 20 条匹配测试语句上比较P50 延迟――写一份报告说明流水线在架构上何时优越――

> **【中文解读】**Trong 术语表中的"Những gì mọi người nói" vs "Những gì nó thực sự có nghĩa" 区分日常口语和精确技术含义── 在团队协作中,统一术语定义可以避免大量沟通误解──


## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Full-duplex | Hear-and-speak at once | Two audio streams active simultaneously on the same model. / 同一模型同时维护两条音频流 |
| Inner monologue | Model's text stream | Moshi emits text tokens alongside its audio output. / Moshi 在音频输出同时输出文本 token |
| Depth transformer | Inter-codebook predictor | Small transformer that predicts 8 codebooks within one 80 ms frame. / 在一个 80 ms 帧内预测 8 个码本的小型 Transformer |
| Mimi | Kyutai's codec | 12.5 Hz × 8 codebooks; semantic+acoustic; powers Moshi. / 12.5 Hz × 8 码本；语义+声学；驱动 Moshi |
| Streaming S2S | Audio → audio live | Chunk-by-chunk translation/dialogue, no pipeline stages. / 逐块翻译/对话，无流水线阶段 |
| Back-channeling | "Mhm" reactions | Moshi can emit small acknowledgments without breaking its turn. / Moshi 可发出小反馈而不打断自己的轮次 |

> **【中文解读】**延伸阅读 cung cấp các nguồn chất lượng cao cho việc học sâu. Những bài báo và giảng dạy này là tài liệu tham khảo cổ điển trong lĩnh vực này, phù hợp với những người đọc cần hiểu sâu hơn.


## Xem thêm 延伸阅读

- [Défossez et al. (2024). Moshi — speech-text foundation model](https://arxiv.org/html/2410.00037v2)- Báo.
  Défossez 等(2024). Moshi语音-文本基础模型原始论文──
- [Kyutai Labs (2026). Hibiki-Zero](https://arxiv.org/abs/2602.12345) dịch vụ phát trực tuyến mà không có dữ liệu được sắp xếp.
  Kyutai Labs (pp. 2026) Hibiki-Zero 无需对齐数据的流式翻译.
- [Sesame (2025). Crossing the uncanny valley of voice](https://www.sesame.com/research/crossing_the_uncanny_valley_of_voice) Định hướng CSM
  Sesame (năm 2025) 跨越语音的恐怖谷CSM 规范──
- [Kyutai — Moshi repo](https://github.com/kyutai-labs/moshi) cài đặt + máy chủ.
  KyutaiMoshi 仓库安装 + 服务器。
- [OpenAI — Realtime API](https://platform.openai.com/docs/guides/realtime) đóng cửa thương mại đồng cấp.
  OpenAITIME APITài nguồn thương mại đóng đối phó
- [Kyutai — Delayed Streams Modeling](https://github.com/kyutai-labs/delayed-streams-modeling) khung STT/TTS dưới nắp.
  KyutaiDelayed Streams Modeling底层 STT/TTS 框架──

> **【中文解读】**延伸阅读 cung cấp các nguồn chất lượng cao để học sâu, bao gồm các bài báo, giảng dạy và công cụ.

