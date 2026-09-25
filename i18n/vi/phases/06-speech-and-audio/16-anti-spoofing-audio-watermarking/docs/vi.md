# Voice Anti-Spoofing & Audio Watermarking  ASVspoof 5, AudioSeal, WaveVerify 语音防伪与音频水印

> Phân phối giọng nói được vận chuyển nhanh hơn phòng thủ. Hệ thống giọng nói sản xuất năm 2026 cần hai thứ: một bộ phát hiện (AASIST, RawNet2) phân loại giọng nói thực và giả, và một dấu nước (AudioSeal) tồn tại sau khi nén và chỉnh sửa.

> **【中文解读】**语音克隆技术跑在防防前面──2026年生产级语音系统需要两样东西:检测器(AASIST、RawNet2)区分真假语音,水印(AudioSeal) vẫn có thể tồn tại sau khi nén và chỉnh sửa── không làm hai thứ này bạn không cần lên line语音克隆功能──

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 06 (Speaker Recognition), Phase 6 · 08 (Voice Cloning) | **前置知识:** 阶段 6 · 06（说话人识别），阶段 6 · 08（语音克隆）
**Time:** ~75 minutes | **预计用时:** ~75 分钟

## Vấn đề  vấn đề giới thiệu

Ba biện pháp phòng thủ liên quan:

> 三种相关防御手段:

> **【中文解读】**Câu hỏi được đặt ra trong phần này là: làm thế nào để hiểu và áp dụng đúng công nghệ này trong công trình thực tế.


1. **Anti-spoofing / deepfake detection.**Với một đoạn băng âm thanh, nó là tổng hợp hay thực sự?
   Trung ngữ翻译:**反欺骗/深度伪造检测。**给定一段音频,判断它是合成的还是真实的?ASVspoof 基准测试(ASVspoof 2019 → 2021 → 5) là tiêu chuẩn vàng。
2. **Audio watermarking.**Đưa một tín hiệu không thể nhận thấy vào âm thanh được tạo ra mà một máy dò có thể lấy ra sau đó.
   Trung ngữ翻译:**音频水印。**Trong các âm thanh được tạo ra được gắn vào các tín hiệu không thể nhận thức được, sau đó có thể lấy được.
3. **Authenticated provenance.**Chữ ký mã hóa của các tệp âm thanh + siêu dữ liệu.
   Trung ngữ翻译:**认证来源。**音频文件 + 元数据的加密签名──C2PA / 内容真实性倡议──

Khám phá xử lý đối thủ không hợp tác. Watermarking xử lý tuân thủ  âm thanh được tạo ra bởi AI nên được xác định như vậy. Cả hai đều cần thiết vào năm 2026.

> 检测应对不配合的攻击者──水印应对合规性AI 生成的音频应被识别──2026年两者都是必需──

## Khái niệm cốt lõi

> **【中文解读】**Bài viết này giới thiệu các khái niệm và lý thuyết cốt lõi.


![Anti-spoofing vs watermarking vs provenance — three defense layers](../assets/spoofing-watermark.svg)

### ASVspoof 5  điểm tham chiếu 2024-2025

> ASVspoof 5  2024-2025 年基准测试

Thay đổi lớn nhất so với các phiên bản trước đây:

> Sự thay đổi lớn nhất so với phiên bản trước:

- **Crowdsourced data**(không phải studio sạch)  điều kiện thực tế.
  Trung ngữ翻译:**众包数据**(非录音棚纯净数据) 真实条件──
- **~2000 speakers**(Vì ~ 100 trước đó).
  Trung ngữ翻译:**约 2000 名说话人**(之前约100名)
- **32 attack algorithms.**TTS + chuyển đổi giọng nói + nhiễu loạn đối kháng.
  Trung ngữ翻译:**32 种攻击算法。**TTS + 语音转换 + đối kháng với sự nhiễu loạn.
- **Two tracks.**Phản ứng (CM) phát hiện độc lập; ASV mạnh mẽ chống lừa đảo (SASV) cho hệ thống sinh trắc học.
  Trung ngữ翻译:**两个赛道。**Động thái chống gian lận (CM)

State of the art trên ASVspoof 5: ~ 7,23% EER. Trên ASVspoof cũ hơn 2019 LA: 0,42% EER.

> ASVspoof 5 上的SOTA:约7.23% EER──在较旧的 ASVspoof 2019 LA 上:0.42% EER──实际部署:预期在野外音频上 EER为5-10%──

### AASIST và RawNet2  gia đình mô hình phát hiện

> AASIST 和 RawNet2  检测模型家族

**AASIST**(2021, cập nhật đến 2026). Chú ý đồ họa về các tính năng quang phổ. SOTA hiện tại về nhiệm vụ phản biện ASVspoof 5.

> **AASIST**(Năm 2021, tiếp tục cập nhật đến năm 2026) ⋅ dựa trên các đặc điểm của tần số ⋅ hệ thống chú ý của 5 phản制措施任务的当前SOTA⋅

**RawNet2.**Convolutional front-end trên dạng sóng nguyên liệu + TDNN xương sống.

> **RawNet2。**Đường hình dạng đầu tiên của khối lượng đầu cuối + TDNN 骨干网络──简单的基线;微调后仍有竞争力──

**NeXt-TDNN + SSL features.**2025: ECAPA-style + WavLM tính năng + mất tiêu cực. đạt được 0,42% EER trên ASVspoof 2019 LA.

> **NeXt-TDNN + SSL 特征。**2025 年变体:ECAPA 风格 + WavLM đặc trưng + mất tập trung──在 ASVspoof 2019 LA tăng đạt 0,42% EER──

### AudioSeal  watermark 2024 mặc định

> AudioSeal  2024 năm của nước印默认方案

Meta's **AudioSeal**(Từ tháng 1 năm 2024, v0.2 tháng 12 năm 2024).

> Meta của **AudioSeal**(2024 年 1 月,v0.2 于 2024 年 12 月) ⋅核心设计:

- **Localized.**Khám nhận thấy dấu nước mỗi khung ở độ phân giải mẫu 16 kHz (1/16000 s).
  Trung ngữ翻译:**局部化。**以 16 kHz 采样分辨率逐检测水印(1/16000 秒)
- **Generator + detector jointly trained.**Máy phát điện học cách nhúng tín hiệu không nghe; máy phát hiện học cách tìm thấy nó thông qua tăng cường.
  Trung ngữ翻译:**生成器 + 检测器联合训练。**生成器学习嵌入不可听信号;检测器学习通过增强找到它──
- **Robust.**Thử nghiệm nén MP3 / AAC, EQ, thay đổi tốc độ ± 10%, hỗn hợp tiếng ồn + 10 dB SNR.
  Trung ngữ翻译:**鲁棒。**能经受 MP3/AAC 压缩, cân bằng, ± 10% 变速, +10 dB SNR 噪音混合
- **Fast.**Máy phát hiện chạy 485x thời gian thực; 1000x nhanh hơn WavMark.
  Trung ngữ翻译:**快速。**检测器 vận hành với tốc độ 485 倍;比WavMark 快 1000 倍.
- **Capacity.**Load hữu ích 16 bit (có thể mã hóa ID mô hình, dấu thời gian tạo, ID người dùng) được nhúng vào mỗi phát biểu.
  Trung ngữ翻译:**容量。**16 位载荷(可编码模型 ID、生成时间、用户 ID) có thể được nhúng vào mỗi đoạn语音。

### WavMark

Hướng dẫn mở trước AudioSeal, mạng thần kinh đảo ngược, 32 bit/thì.

> AudioSeal 之前的开源基线──可逆神经网络,32 位/秒──问题:

- Đồng bộ hóa lực lượng thô là chậm.
  Trung ngữ翻译:同步暴力破解很慢──
- Có thể được loại bỏ bằng tiếng ồn Gaussian hoặc nén MP3.
  Trung文翻译:可被高斯噪音或 MP3 压缩删除──
- Không thân thiện trong thời gian thực.
  Trung ngữ翻译:不适合实时场景──

### WaveVerify (tháng 7 năm 2025)

Giải quyết các điểm yếu của AudioSeal  đặc biệt là thao tác thời gian (phản hồi, tốc độ). Sử dụng máy phát điện dựa trên FiLM + máy dò Mixture-of-Experts. Thang với AudioSeal trong các cuộc tấn công tiêu chuẩn; xử lý chỉnh sửa thời gian.

> WaveVerify(2025 年 7 月) ―― giải quyết điểm yếu của AudioSeal 特别是时间操作(反转、变速) ―― sử dụng dựa trên FiLM của máy phát triển + MoE 检测器──在标准攻击上与 AudioSeal 相当;能处理时间编辑──

### Những kẻ thù khai thác khoảng cách

Từ AudioMarkBench: "trong độ chuyển động, tất cả các dấu nước cho thấy độ chính xác phục hồi Bit dưới 0,6, cho thấy loại bỏ gần như hoàn chỉnh". **Pitch-shift is the universal attack.**Watermark No 2026 hoàn toàn mạnh mẽ để thay đổi độ cao tích cực.

> 攻击者利用的漏洞──来自 AudioMarkBench:"Bằng độ chuyển động cao âm thanh, tỷ lệ xác thực phục hồi tất cả các dấu ấn nước dưới 0,6, cho thấy gần như hoàn toàn bị xóa bỏ──"**音高偏移是通用攻击。**Không có bất kỳ nước印 nào trong năm 2026 có thể chống lại hoàn toàn sự thay đổi âm thanh.

### C2PA / Động thái xác thực nội dung

Không phải kỹ thuật ML  định dạng biểu hiện. Các tệp âm thanh mang lại metadata được ký mã hóa về công cụ tạo, tác giả, ngày. Audobox / Seamless sử dụng nó.

> C2PA / 内容真实性倡议──不是机器学习技术是一种清单形式──音频文件携带关于创建工具、作者、日期的加密签名元数据──Audobox / Seamless 使用它──有利于追溯源; nhưng nếu kẻ ác ý tái mã hóa và剥离元数据则无效──

> **【拓展：语音 AI 的产品化】**语音技术在产品化中面临独特挑战:不同口音,背景噪音,远场拾音,多人说话等. Siri, Alexa,小爱同学等产品都投入大量工程优化解决这些长尾问题.

> **【拓展：多语言语音技术】**Các đặc điểm ngữ âm của toàn cầu ngôn ngữ khác biệt rất lớn: tiếng调 ngôn ngữ (如中文) của âm cao mang ngữ nghĩa, nguồn lực thấp ngôn ngữ thiếu đào tạo dữ liệu.

> **【拓展：语音隐私与安全】**语音数据 chứa rất nhiều thông tin cá nhân riêng tư (音纹、对话内容) ◦深度伪造 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术) 语音技术 (反欺诈) 语音技术 (反欺诈) 防伪 (反伪造) 防伪研究热点) 热点




## Hãy xây dựng nó.

> **【中文解读】**本节通过代码实现核心算法从零――这种" từ đầu"的方式能帮助理解框架背后的原理,遇到问题时不会被黑盒困住――

```figure
v4-audio-watermark
```

## Hãy xây dựng nó

### Bước 1: một máy dò tính quang phổ đơn giản ( đồ chơi)

> 步骤 1: đơn giản 频谱特征检测器

```python
def spectral_rolloff(spec, percentile=0.85):
    cum = 0
    total = sum(spec)
    if total == 0:
        return 0
    threshold = total * percentile
    for k, v in enumerate(spec):
        cum += v
        if cum >= threshold:
            return k
    return len(spec) - 1

def is_suspicious(audio):
    spec = magnitude_spectrum(audio)
    rolloff = spectral_rolloff(spec)
    return rolloff / len(spec) > 0.92
```

Nói cách tổng hợp thường có năng lượng tần số cao không thường xuyên.

> 合成语音 thường có năng lượng cao bình thường.

### Bước 2: AudioSeal embed + detect

> 步骤 2:AudioSeal 嵌入 + 检测

```python
from audioseal import AudioSeal
import torch

generator = AudioSeal.load_generator("audioseal_wm_16bits")
detector = AudioSeal.load_detector("audioseal_detector_16bits")

audio = load_wav("generated.wav", sr=16000)[None, None, :]
payload = torch.tensor([[1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0]])
watermark = generator.get_watermark(audio, sample_rate=16000, message=payload)
watermarked = audio + watermark

result, decoded_payload = detector.detect_watermark(watermarked, sample_rate=16000)
# result: float in [0, 1] — probability of watermark presence
# decoded_payload: 16 bits; match against embedded payload
```

### Bước 3: đánh giá  EER

> 步骤 3: đánh giá  EER(等错误率)

```python
def eer(real_scores, fake_scores):
    thresholds = sorted(set(real_scores + fake_scores))
    best = (1.0, 0.0)
    for t in thresholds:
        far = sum(1 for s in fake_scores if s >= t) / len(fake_scores)
        frr = sum(1 for s in real_scores if s < t) / len(real_scores)
        if abs(far - frr) < best[0]:
            best = (abs(far - frr), (far + frr) / 2)
    return best[1]
```

### Bước 4: sự tích hợp sản xuất

> Bước 4: sản xuất cấp tập hợp

```python
def safe_tts(text, voice, clone_reference=None):
    if clone_reference is not None:
        verify_consent(user_id, clone_reference)
    audio = tts_model.synthesize(text, voice)
    audio_with_wm = audioseal_embed(audio, payload=build_payload(user_id, model_id))
    manifest = c2pa_sign(audio_with_wm, user_id, timestamp=now())
    return audio_with_wm, manifest
```

> **【中文解读】**Bài này sẽ trình bày cách sử dụng một khung đã phát triển như PyTorch, HuggingFace, và các khác.


Mỗi dòng tàu: (1) dấu nước, (2) bản ghi ký, (3) sổ kiểm toán tuân thủ chính sách lưu giữ.

> Mỗi lần tạo ra các sản phẩm đều bao gồm: 1) nước印, 2) ký danh sách, 3) phù hợp với chiến lược giữ gìn của kiểm toán日志.




> **【拓展：语音与情感计算】**语音 không chỉ truyền tải thông tin văn bản, còn mang lại một tín hiệu cảm xúc phong phú (语调、语速、音高变化)  cảm xúc (语音识别, Speech Emotion Recognition, SER) có ứng dụng rộng rãi trong lĩnh vực kiểm tra chất lượng khách hàng, giám sát sức khỏe tâm thần, giáo dục thông minh, etc.  Mô hình SOTA hiện tại thường dựa trên wave2vec 2.0 hoặc HuBERT 等

## Hãy sử dụng nó để thực hiện

| Use case | Defense |
|----------|---------|
| Shipping TTS / voice cloning / 上线 TTS/语音克隆 | AudioSeal embed on every output (non-negotiable) / 每次输出嵌入 AudioSeal（不可妥协） |
| Biometric voice unlock / 生物识别语音解锁 | AASIST + ECAPA ensemble; liveness challenge / AASIST + ECAPA 集成；活体挑战 |
| Call-center fraud detection / 呼叫中心欺诈检测 | AASIST on 20% sample of incoming calls / 对 20% 的来电做 AASIST 检测 |
| Podcast authenticity / 播客真实性 | C2PA signing on upload, AudioSeal if AI-generated / 上传时 C2PA 签名，AI 生成则加 AudioSeal |
| Research / training detectors / 研究/训练检测器 | ASVspoof 5 train/dev/eval sets / ASVspoof 5 训练/开发/评估集 |



## Những bẫy

> 常见陷

- **Watermark without detector ever running.**Không có ý nghĩa, đưa máy dò vào máy tính thông tin của anh.
  Trung ngữ翻译:**嵌入水印但从未运行检测器。**Không có ý nghĩa gì cả.
- **Detection without calibration.**AASIST được đào tạo về các vụ phóng to của Mỹ, giảm độ chính xác trong thế giới thực.
  Trung ngữ翻译:**检测未校准。**Trong ASVspoof LA trên đào tạo của AASIST sẽ được chuẩn bị; thực tế准确率 giảm.
- **Pitch-shift gap.**Chuyển độ hung hăng sẽ loại bỏ hầu hết các dấu hiệu nước.
  Trung ngữ翻译:**音高偏移漏洞。**激进的音高偏移能去除大多数水印──准备检测作为后备──
- **Metadata strip-and-rehost.**C2PA là không có gì khác với mã hóa lại. Luôn thêm hệ thống bảo vệ mật mã + nhận thức (chước biển) cùng nhau.
  Trung ngữ翻译:**元数据剥离重新托管。**C2PA 通过重新编码即可轻松绕过──始终同时使用加密 + 感知(水印)防御──
- **Liveness as detection.**Hãy yêu cầu người dùng nói một cụm từ ngẫu nhiên.
  Trung ngữ翻译:**活体检测作为检测手段。**让用户说一个随机短语――能防止重发攻击但不能防止实时克隆――

> **【中文解读】**Phần này tập trung vào cách phân phối mô hình như một sản phẩm có thể sử dụng.


## Chuyển nó đi.

Cứ như `outputs/skill-spoof-defender.md`. Chọn mô hình phát hiện, dấu nước, biểu đồ xuất xứ và sổ tay hoạt động cho việc triển khai voice-gen.

> 保存为 `outputs/skill-spoof-defender.md`◊ cho một ngôn ngữ tạo triển khai lựa chọn kiểm tra mô hình, nước印, nguồn gốc và hoạt động.

## Tập luyện bài tập

1. **Easy.**Đi chạy`code/main.py`. Máy phát hiện đồ chơi + dấu nước đồ chơi nhúng/ phát hiện trên âm thanh tổng hợp.
   Trung ngữ翻译:**简单。**运行 `code/main.py`                                                                                                                                                                                                                                                              
2. **Medium.**Thiết lập `audioseal`, nhúng tải 16 bit vào đầu ra TTS, mã hóa lại, làm hỏng âm thanh bằng tiếng ồn và đo độ chính xác phục hồi bit.
   Trung ngữ翻译:**中等。**                                          `audioseal`, trong TTS 输出嵌入 16 位载荷,重新解码──用噪音损坏音频并测量位恢复准确率──
3. **Hard.**Định chỉnh một RawNet2 hoặc AASIST trên ASVspoof 2019 LA. đo EER. Thử nghiệm trên một bộ clip được tạo ra bằng F5-TTS  xem việc phát hiện OOD suy giảm như thế nào.
   Trung ngữ翻译:**困难。**Trong ASVspoof 2019 LA 上微调 RawNet2 hoặc AASIST。 đo EER。 trong F5-TTS 生成音频集上测试观察 OOD 检测的退化程度。

> **【中文解读】**Trong 术语表中的"Những gì mọi người nói" vs "Những gì nó thực sự có nghĩa" 区分日常口语和精确技术含义── 在团队协作中,统一术语定义可以避免大量沟通误解──


## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| ASVspoof | The benchmark | Biennial challenge; 2024 = ASVspoof 5. / 双年挑战赛；2024 = ASVspoof 5 |
| CM (countermeasure) | Detector | Classifier: real speech vs synthetic / converted. / 分类器：真实语音 vs 合成/转换语音 |
| SASV | Speaker verif + CM | Integrated biometric + spoof detection. / 集成生物识别 + 欺骗检测 |
| AudioSeal | Meta watermark | Localized, 16-bit payload, 485× faster than WavMark. / 局部化，16 位载荷，比 WavMark 快 485 倍 |
| Bit Recovery Accuracy | Watermark survival | Fraction of payload bits recovered after attack. / 攻击后恢复的载荷位比例 |
| C2PA | Provenance manifest | Cryptographic metadata about creation / authorship. / 关于创建/作者身份的加密元数据 |
| AASIST | Detector family | Graph-attention-based anti-spoofing SOTA. / 基于图注意力的反欺骗 SOTA |

> **【中文解读】**延伸阅读 cung cấp các nguồn chất lượng cao cho việc học sâu. Những bài báo và giảng dạy này là tài liệu tham khảo cổ điển trong lĩnh vực này, phù hợp với những người đọc cần hiểu sâu hơn.


## Xem thêm 延伸阅读

- [Todisco et al. (2024). ASVspoof 5](https://dl.acm.org/doi/10.1016/j.csl.2025.101825) chỉ số chuẩn hiện tại.
  Todisco 等(2024). ASVspoof 5当前基准。
- [Defossez et al. (2024). AudioSeal](https://arxiv.org/abs/2401.17264) watermark mặc định.
  Defossez 等(2024).
- [Chen et al. (2025). WaveVerify](https://arxiv.org/abs/2507.21150) Bộ dò MoE cho các cuộc tấn công thời gian.
  Chen 等(2025). WaveVerify 针对时间攻击的MoE 检测器──
- [Jung et al. (2022). AASIST](https://arxiv.org/abs/2110.01200) xương sống phát hiện SOTA.
  Jung 等(2022). AASISTSOTA 检测骨干。
- [AudioMarkBench (2024)](https://proceedings.neurips.cc/paper_files/paper/2024/file/5d9b7775296a641a1913ab6b4425d5e8-Paper-Datasets_and_Benchmarks_Track.pdf) Đánh giá độ bền.
  AudioMarkBench ((2024) 鲁棒性评估──
- [C2PA specification](https://c2pa.org/specifications/specifications/) định dạng biểu hiện xuất xứ.
  C2PA 规范来源清单格式──

> **【中文解读】**延伸阅读 cung cấp các nguồn chất lượng cao để học sâu, bao gồm các bài báo, giảng dạy và công cụ.

