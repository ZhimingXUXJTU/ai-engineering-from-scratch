# Audio Classification  Từ k-NN trên MFCC đến AST và BEATs  音频分类  Từ MFCC+KNN đến AST và BEATs

> Mọi thứ từ "dog barking vs siren" đến "thế ngữ này là gì" là phân loại âm thanh. Các tính năng là melt. Kiến trúc di chuyển mỗi thập kỷ. Thử nghiệm vẫn là AUC, F1, và nhớ mỗi lớp.

> **【中文解读】**Từ "dog calling还是警笛" đến "这是什么语言", đều là âm thanh phân loại.

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 02 (Spectrograms & Mel), Phase 3 · 06 (CNNs), Phase 5 · 08 (CNNs & RNNs for Text) | **前置知识:** 阶段 6 · 02（频谱图与 Mel），阶段 3 · 06（CNN），阶段 5 · 08（文本的 CNN 与 RNN）
**Time:** ~75 minutes | **预计用时:** ~75 分钟

## Vấn đề  vấn đề giới thiệu

Bạn có một đoạn clip 10 giây. Bạn muốn biết: "đó là gì?" âm thanh đô thị (siren, khoan, chó), lệnh nói (có/không/ dừng), ID ngôn ngữ (en/es/ar), cảm xúc loa (cực tức/ trung lập), hoặc âm thanh môi trường (trang / ngoài trời, đùa). Tất cả những điều này là * phân loại âm thanh*, và vào năm 2026 kiến trúc cơ bản đã trưởng thành: log-mel → CNN hoặc Transformer → softmax.

> Bạn nhận được một đoạn 10 giây âm thanh. Bạn nghĩ rằng:"Đây là gì?" tiếng ồn của thành phố: tiếng ồn: tiếng ồn: tiếng ồn: tiếng ồn: tiếng ồn: tiếng ồn: tiếng ồn: tiếng ồn: tiếng ồn: tiếng ồn: tiếng ồn: tiếng ồn: tiếng ồn: tiếng ồn: tiếng ồn: tiếng ồn: tiếng ồn: tiếng ồn: tiếng ồn: tiếng ồn: tiếng ồn: tiếng ồn: tiếng ồn: tiếng ồn: tiếng ồn: tiếng ồn: tiếng ồn: tiếng ồn: tiếng ồn: tiếng ồn: tiếng ồn: tiếng ồn: tiếng ồn: tiếng ồn: tiếng ồn: tiếng ồn: tiếng ồn: tiếng ồn: tiếng ồn: tiếng ồn: tiếng ồn: tiếng ồn: tiếng ồn: tiếng ồn: tiếng ồn: tiếng ồn: tiếng ồn: tiếng ồn: tiếng ồn: tiếng ồn: tiếng ồn: tiếng ồn: tiếng ồn: tiếng ồn: tiếng ồn: tiếng ồn: tiếng ồn: tiếng ồn: tiếng ồn: tiếng ồn: tiếng ồn: tiếng ồn: tiếng ồn: tiếng ồn: tiếng ồn: tiếng ồn: tiếng ồn: tiếng ồn: tiếng ồn: tiếng ồn: tiếng ồn: tiếng ồn: tiếng ồn: tiếng ồn: tiếng ồn: tiếng ồn: tiếng ồn: tiếng ồn: tiếng ồn: tiếng ồn: tiếng ồn: tiếng ồn: tiếng ồn: tiếng ồn: tiếng ồn: ồn: tiếng ồn: ồn: ồn: ồn: ồn: ồn: ồn: ồn: ồn: ồn: ồn: ồn: ồn: ồn: ồn: ồn: ồn: ồn: ồn: ồn: ồn: ồn: ồn: ồn: ồn: ồn: ồn: ồn: ồn: ồn: ồn: ồn: ồn: ồn: ồn: ồn: ồn: ồn: ồn: ồn: ồn: ồn: ồn: ồn: ồn: ồn: ồn

> **【中文解读】**Câu hỏi được đặt ra trong phần này là: làm thế nào để hiểu và áp dụng đúng công nghệ này trong công trình thực tế.

Vấn đề cốt lõi không phải là mạng. Đó là dữ liệu. Dữ liệu âm thanh có sự mất cân bằng lớp học tàn bạo, chuyển đổi miền mạnh mẽ (t sạch so với tiếng ồn), và tiếng ồn nhãn (người nào quyết định "bố ồn đô thị" so với "bồn ồn nhà hàng"?). 80% vấn đề là bảo quản, tăng cường và đánh giá, không thay đổi CNN với Transformer.

> 核心难点不在网络,而在数据──音频数据集有严重类别不平衡、强领域偏移(干净 vs 杂) 和标签噪音(谁定义了"城市杂"vs"餐厅噪音"?)──80% vấn đề là sắp xếp, tăng cường và đánh giá dữ liệu, thay vì thay đổi CNN thành Transformer──

## Khái niệm cốt lõi

> **【中文解读】**Bài viết này giới thiệu các khái niệm và lý thuyết cốt lõi.


![Audio classification ladder: k-NN on MFCCs to AST to BEATs](../assets/audio-classification.svg)

**k-NN on MFCCs (the 1990s baseline).**MFCCs phẳng mỗi clip, tính toán sự tương tự cosine với một ngân hàng được dán nhãn, trả lại phiếu đa số của K trên cùng. Đáng ngạc nhiên mạnh mẽ trên các bộ dữ liệu sạch, nhỏ (Speech Commands, ESC-50).

> **MFCC 上的 k-NN（1990 年代基线）。**Để phân tích các đoạn âm thanh của MFCC 展平, tính toán tương tự với các ký hiệu, trả lại trước K 个 个 个 多数投票──在干净的小数据集(Speech Commands、ESC-50) trên bất ngờ地强──不需要 GPU──

**2D CNN on log-mels (2015-2019).**Chăm sóc `(T, n_mels)`Log-mail như một hình ảnh. áp dụng ResNet-18 hoặc kiểu VGG. trung bình toàn cầu tích hợp trục thời gian. Softmax trên lớp học.

> **log-mel 上的 2D CNN（2015-2019）。**sẽ`(T, n_mels)`Trong năm 2026, hầu hết các loại kaggle vẫn còn là một phần cốt lõi.

**Audio Spectrogram Transformer, AST (2021-2024).**Lắp đặt log-mail (ví dụ: 16×16 patches), thêm các vị trí nhúng, cấp dữ liệu cho một ViT. State of the art trên AudioSet (mAP 0.485) cho việc học theo giám sát.

> **音频频谱图 Transformer，AST（2021-2024）。**将 log-mail 分块(如 16×16块),添加位置嵌入,送入 ViT──AudioSet 上监督学习的 SOTA(map 0.485)──

**BEATs and WavLM-base (2024-2026).**Bản thân giám sát trước khi tập luyện hàng triệu giờ. Hoạt động tốt cho nhiệm vụ của bạn với 1-10% dữ liệu giám sát bạn cần. Năm 2026 đây là điểm khởi đầu mặc định cho âm thanh không nói. BEATs-iter3 đánh bại AST 1-2 mAP trên AudioSet trong khi sử dụng 1/4 tính toán.

> **BEATs 和 WavLM-base（2024-2026）。**Trong hàng triệu giờ dữ liệu trên giám sát dự kiến đào tạo. Với 1-10% dữ liệu giám sát bạn có thể cần được điều chỉnh. Năm 2026 đây là điểm bắt đầu mặc định của các kênh không nói.

**Whisper-encoder as a frozen backbone (2024).**Hãy lấy bộ mã hóa của Whisper, bỏ bộ mã hóa, gắn một bộ phân loại tuyến tính gần SOTA trên ID ngôn ngữ và phân loại sự kiện đơn giản với không tăng âm thanh.

> **Whisper 编码器作为冻结骨干（2024）。**取 Whisper 的编码器,丢弃解码器,接一个线性分类器.

### Sự mất cân bằng lớp học là thách thức thực sự

> ### Sự bất cân là thách thức thực sự

ESC-50: 50 lớp, 40 clip mỗi  cân bằng, dễ dàng. UrbanSound8K: 10 lớp, không cân bằng 10:1. AudioSet: 632 lớp với đuôi dài 100.000: 1.

> ESC-50:50 个类, mỗi lớp 40 个片段平衡、简单。UrbanSound8K:10 个类,10:1 不平衡。AudioSet:632 个类,长尾比例 100,000:1──有效的技术:

- Tiêu chuẩn lấy mẫu cân bằng trong quá trình đào tạo (không phải trong đánh giá).
  训练时平衡采样(评估时不用)
- Trộn lại: liên kết trực tuyến hai clip (và nhãn của chúng) như sự tăng cường.
  Mixup:线性插值两段音频 (nói là "nói" trong "nói" trong "nói" trong "nói" trong "nói" trong "nói" trong "nói" trong "nói" trong "nói" trong "nói" trong "nói" trong "nói" trong "nói" trong "nói" trong "nói" trong "nói" trong "nói" trong "nói" trong "nói" trong "nói" trong "nói" trong "nói" trong "nói" trong "nói" trong "nói" trong "nói" trong "nói" trong "nói" trong "nói" trong "nói" trong "nói" trong "nói" trong "nói" trong "nói" trong "nói" trong "nói" trong "nói"
- SpecAugment: che giấu thời gian ngẫu nhiên và băng tần số.
  SpecAugment: 遮蔽随机时间和频率带――简单但关键――

### Đánh giá

> ### 评估

- Tác dụng độc quyền đa lớp (Thật lệnh nói): độ chính xác top-1, độ chính xác top-5.
  Có lẽ loại trò chơi khác nhau:
- Multi-class multi-label (AudioSet, UrbanSound-style): độ chính xác trung bình (mAP).
  Có lẽ类多标签(AudioSet、UrbanSound 类型): trung bình độ chính xác trung bình
- Không cân bằng nặng: thu hồi mỗi lớp + macro F1.
  严重不平衡: mỗi loại triệu hồi tỷ lệ + 宏观 F1。

2026 số bạn nên biết:

> 2026 năm bạn nên biết số:

| Benchmark | Baseline | SOTA 2026 | Source |
|-----------|----------|-----------|--------|
| ESC-50 | 82% (AST) | 97.0% (BEATs-iter3) | BEATs paper (2024) |
| AudioSet mAP | 0.485 (AST) | 0.548 (BEATs-iter3) | HEAR leaderboard 2026 |
| Speech Commands v2 | 98% (CNN) | 99.0% (Audio-MAE) | HEAR v2 results |

| 基准测试 | 基线 | 2026 SOTA | 来源 |
|----------|------|-----------|------|
| ESC-50 | 82%（AST） | 97.0%（BEATs-iter3） | BEATs 论文（2024） |
| AudioSet mAP | 0.485（AST） | 0.548（BEATs-iter3） | HEAR 排行榜 2026 |
| Speech Commands v2 | 98%（CNN） | 99.0%（Audio-MAE） | HEAR v2 结果 |

> **【中文解读】**本节通过代码实现核心算法从零――这种" từ đầu"的方式能帮助理解框架背后的原理,遇到问题时不会被黑盒困住――

> **【拓展：语音 AI 的产品化】**语音技术在产品化中面临独特挑战:不同口音,背景噪音,远场拾音,多人说话等. Siri, Alexa,小爱同学等产品都投入大量工程优化解决这些长尾问题.

> **【拓展：多语言语音技术】**Các đặc điểm ngữ âm của toàn cầu ngôn ngữ khác biệt rất lớn: tiếng调 ngôn ngữ (如中文) của âm cao mang ngữ nghĩa, nguồn lực thấp ngôn ngữ thiếu đào tạo dữ liệu.

> **【拓展：语音隐私与安全】**语音数据 chứa rất nhiều thông tin cá nhân riêng tư (音纹、对话内容) ◦深度伪造 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术 (深度伪造) 语音技术) 语音技术 (反欺诈) 语音技术 (反欺诈) 防伪 (反伪造) 防伪研究热点) 热点





## Hãy xây dựng nó.
```figure
mfcc-pipeline
```

## Hãy xây dựng nó

### Bước 1: Featurise

```python
def featurize_mfcc(signal, sr, n_mfcc=13, n_mels=40, frame_len=400, hop=160):
    mag = stft_magnitude(signal, frame_len, hop)
    fb = mel_filterbank(n_mels, frame_len, sr)
    mels = apply_filterbank(mag, fb)
    log = log_transform(mels)
    return [dct_ii(frame, n_mfcc) for frame in log]
```

### Bước 2: Tổng kết dài cố định

```python
def summarize(mfcc_frames):
    n = len(mfcc_frames[0])
    mean = [sum(f[i] for f in mfcc_frames) / len(mfcc_frames) for i in range(n)]
    var = [
        sum((f[i] - mean[i]) ** 2 for f in mfcc_frames) / len(mfcc_frames) for i in range(n)
    ]
    return mean + var
```

Đơn giản nhưng mạnh mẽ: trung bình + sự khác biệt qua thời gian cung cấp một nhúng cố định 26 chiều cho một MFCC 13 khoang.

>  đơn giản nhưng hiệu quả: giá trị trung bình trên trục thời gian + 方差 là 13 số MFCC  đưa ra 26 维固定嵌入──运行瞬间── trên ESC-50 lên đến năm 2017 vẫn có thể đánh bại SOTA thời đó.

### Bước 3: k-NN

```python
def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a)) or 1e-12
    nb = math.sqrt(sum(x * x for x in b)) or 1e-12
    return dot / (na * nb)

def knn_classify(q, bank, labels, k=5):
    sims = sorted(range(len(bank)), key=lambda i: -cosine(q, bank[i]))[:k]
    votes = Counter(labels[i] for i in sims)
    return votes.most_common(1)[0][0]
```

### Bước 4: nâng cấp lên CNN trên log-mels

Trong PyTorch:

```python
import torch.nn as nn

class AudioCNN(nn.Module):
    def __init__(self, n_mels=80, n_classes=50):
        super().__init__()
        self.body = nn.Sequential(
            nn.Conv2d(1, 32, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(32, 64, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(64, 128, 3, padding=1), nn.ReLU(),
            nn.AdaptiveAvgPool2d(1),
        )
        self.head = nn.Linear(128, n_classes)

    def forward(self, x):  # x: (B, 1, T, n_mels)
        return self.head(self.body(x).flatten(1))
```

Các thông số 3M. Các tàu trong ~ 10 phút trên ESC-50 với một RTX 4090. 80% + độ chính xác.

> 300.000 tham số. trên ESC-50 上 dùng đơn张 RTX 4090  luyện tập khoảng 10 phút.

### Bước 5: các 2026 mặc định  tinh chỉnh BEAT

```python
from transformers import ASTFeatureExtractor, ASTForAudioClassification

ext = ASTFeatureExtractor.from_pretrained("MIT/ast-finetuned-audioset-10-10-0.4593")
model = ASTForAudioClassification.from_pretrained(
    "MIT/ast-finetuned-audioset-10-10-0.4593",
    num_labels=50,
    ignore_mismatched_sizes=True,
)

> **【中文解读】** 本节展示如何用成熟框架（如 PyTorch、HuggingFace 等）快速应用该技术。在实际项目中，优先使用经过验证的框架实现，可以减少 bug 并提高开发效率。


inputs = ext(audio, sampling_rate=16000, return_tensors="pt")
logits = model(**inputs).logits
```

Đối với BEAT, sử dụng `microsoft/BEATs-base`qua `beats`thư viện; API biến đổi là cùng một hình dạng.

> 对于BATs, qua `beats`库使用 `microsoft/BEATs-base`;form of transformers API là giống nhau.




> **【拓展：语音与情感计算】**语音 không chỉ truyền tải thông tin văn bản, còn mang lại một tín hiệu cảm xúc phong phú (语调、语速、音高变化)  cảm xúc (语音识别, Speech Emotion Recognition, SER) có ứng dụng rộng rãi trong lĩnh vực kiểm tra chất lượng khách hàng, giám sát sức khỏe tâm thần, giáo dục thông minh, etc.  Mô hình SOTA hiện tại thường dựa trên wave2vec 2.0 hoặc HuBERT 等

## Hãy sử dụng nó để thực hiện

Số 2026:

> 2026 năm của công nghệ:

| Situation | Start with |
|-----------|-----------|
| Tiny dataset (<1000 clips) | k-NN on MFCC means (your baseline) + audio augmentation |
| Medium dataset (1K–100K) | BEATs or AST fine-tune |
| Large dataset (>100K) | Train from scratch or fine-tune Whisper-encoder |
| Real-time, edge | 40-MFCC CNN, quantized to int8 (KWS-style) |
| Multi-label (AudioSet) | BEATs-iter3 with BCE loss + mixup + SpecAugment |
| Language ID | MMS-LID, SpeechBrain VoxLingua107 baseline |

| 场景 | 起始方案 |
|------|----------|
| 小数据集（<1000 段） | MFCC 均值上的 k-NN（基线）+ 音频增强 |
| 中等数据集（1K–100K） | BEATs 或 AST 微调 |
| 大数据集（>100K） | 从零训练或微调 Whisper 编码器 |
| 实时、边缘设备 | 40-MFCC CNN，量化为 int8（关键词检测风格） |
| 多标签（AudioSet） | BEATs-iter3 + BCE 损失 + mixup + SpecAugment |
| 语言识别 | MMS-LID，SpeechBrain VoxLingua107 基线 |

> **【中文解读】**Phần này tập trung vào cách phân phối mô hình như một sản phẩm có thể sử dụng.


Quy tắc quyết định: **start with a frozen backbone, not a fresh model**Định chỉnh đầu của BEATs sẽ giúp bạn có được 95% SOTA chỉ trong vài giờ, không phải vài tuần.

> 决策规则:**从冻结骨干开始，而不是从头训练模型**❖ Các phân loại BEATs có thể đạt đến 95% SOTA trong vài giờ, thay vì vài tuần.



## Chuyển nó đi.

Cứ như `outputs/skill-classifier-designer.md`Chọn kiến trúc, tăng cường, chiến lược cân bằng lớp học và đánh giá métrics cho một nhiệm vụ phân loại âm thanh nhất định.

> 保存为 `outputs/skill-classifier-designer.md`◊ Đối với các loại âm thanh nhất định, chọn cấu trúc nhiệm vụ, tăng cường chiến lược, phân loại cân bằng chiến lược và đánh giá chỉ số.

## Tập luyện bài tập

1. **Easy.**Đi chạy`code/main.py`Nó đào tạo k-NN MFCC cơ sở trên một tập dữ liệu tổng hợp 4 lớp (tôn tinh khiết ở các độ cao khác nhau).
   **简单。**运行 `code/main.py`◊ Nó được tập hợp trên 4 bộ dữ liệu tổng hợp (不同音高的纯音) trên k-NN MFCC 基线――报告混矩阵――
2. **Medium.**Thay thế `summarize`với [tỷ lệ trung bình, var, skew, kurtosis]. 4 khoảnh khắc tích hợp đánh giá trung bình + var trên cùng một tập dữ liệu tổng hợp?
   **中等。**sẽ`summarize`替换为 [mean, var, skew, kurtosis]──四矩池化 có trên cùng một tập hợp dữ liệu được tạo ra trên 优于平均值+方差?
3. **Hard.**Sử dụng `torchaudio`, đào tạo một 2D CNN trên ESC-50 gấp 1. báo cáo độ chính xác xác xác thực hóa chéo 5 lần. Thêm SpecAugment (mác thời gian = 20, mác tần số = 10) và báo cáo delta.
   **困难。**Sử dụng `torchaudio`, trên ESC-50 gấp 1 上训练 2D CNN。 báo cáo 5 lần交叉验证准确率。添加 具体Augment(时间掩码 = 20,频率掩码 = 10)并报告差值。

> **【中文解读】**Trong 术语表中的"Những gì mọi người nói" vs "Những gì nó thực sự có nghĩa" 区分日常口语和精确技术含义── 在团队协作中,统一术语定义可以避免大量沟通误解──


## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| AudioSet | The ImageNet of audio | Google's 2M-clip, 632-class weakly-labeled YouTube dataset. |
| ESC-50 | Small classification benchmark | 50 classes × 40 clips of environmental sounds. |
| AST | Audio Spectrogram Transformer | ViT on log-mel patches; 2021 SOTA. |
| BEATs | Self-supervised audio | Microsoft model, iter3 leads AudioSet as of 2026. |
| Mixup | Pair augmentation | `x = λ·x1 + (1-λ)·x2; y = λ·y1 + (1-λ)·y2`. |
| SpecAugment | Mask-based augmentation | Zero-out random time and frequency bands of the spectrogram. |
| mAP | Main multi-label metric | Mean average precision across classes and thresholds. |

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| AudioSet | 音频界的 ImageNet | Google 的 200 万片段、632 类弱标注 YouTube 数据集。 |
| ESC-50 | 小型分类基准 | 50 类 × 40 个环境声音片段。 |
| AST | 音频频谱图 Transformer | log-mel 块上的 ViT；2021 SOTA。 |
| BEATs | 自监督音频 | 微软模型，iter3 截至 2026 年领先 AudioSet。 |
| Mixup | 配对增强 | `x = λ·x1 + (1-λ)·x2; y = λ·y1 + (1-λ)·y2`。 |
| SpecAugment | 掩码增强 | 将频谱图的随机时间和频率带置零。 |
| mAP | 主要多标签指标 | 各类别和阈值的平均精度均值。 |

> **【中文解读】**延伸阅读 cung cấp các nguồn chất lượng cao cho việc học sâu. Những bài báo và giảng dạy này là tài liệu tham khảo cổ điển trong lĩnh vực này, phù hợp với những người đọc cần hiểu sâu hơn.


## Xem thêm 延伸阅读

- [Gong, Chung, Glass (2021). AST: Audio Spectrogram Transformer](https://arxiv.org/abs/2104.01778) kiến trúc ghi chép từ 20212024.
  Gong, Chung, Glass (2021). AST:音频频谱图 Transformer2021-2024 年的记录架构──
- [Chen et al. (2022, rev. 2024). BEATs: Audio Pre-Training with Acoustic Tokenizers](https://arxiv.org/abs/2212.09058) dự định 2024+.
  Chen 等 (2022, 修订 2024). BEATs:声学 tokenizer 的音频预训2024+ 的默认选择──
- [Park et al. (2019). SpecAugment](https://arxiv.org/abs/1904.08779) sự tăng cường âm thanh chiếm ưu thế.
  Park 等 (2019). SpecAugment主流音频增强方法──
- [Piczak (2015). ESC-50 dataset](https://github.com/karolpiczak/ESC-50) Định nghĩa 50 lớp sống sót.
  Piczak (2015). ESC-50 数据集持续使用的50类基准──
- [Gemmeke et al. (2017). AudioSet](https://research.google.com/audioset/) Định dạng phân loại YouTube lớp 632; vẫn là tiêu chuẩn vàng.
  Gemmeke 等 (2017). AudioSet632 类 YouTube 分类体系; vẫn là tiêu chuẩn vàng。

> **【中文解读】**延伸阅读 cung cấp các nguồn chất lượng cao để học sâu, bao gồm các bài báo, giảng dạy và công cụ.

