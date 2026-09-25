# Người phát ngôn nhận dạng và xác minh nói chuyện nhận dạng và xác minh người

> ASR hỏi "bọn họ nói gì?" nhận dạng loa hỏi "người nói nó?" toán học trông giống nhau  nhúng cộng với cosine  nhưng mọi quyết định sản xuất phụ thuộc vào một số EER duy nhất.

> **【中文解读】**ASR 问"说了什么",说话人识别问"谁说的"―― toán học trông giống như嵌向量+余弦相似度但每个生产决策都取决于一个EER(等错误率) 数值──EER 越低,系统越可靠──

> **【拓展：声纹识别应用】**声纹识别用于银行电话认证、智能音箱用户识别、安防监控──声纹(声纹) như dấu vân tay của语音, là một phần quan trọng của nhận dạng các đặc điểm sinh học──

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 02 (Spectrograms & Mel), Phase 5 · 22 (Embedding Models) | **前置知识:** 阶段 6 · 02（频谱图与 Mel），阶段 5 · 22（嵌入模型）
**Time:** ~45 minutes | **预计用时:** ~45 分钟

## Vấn đề  vấn đề giới thiệu

Người dùng nói một từ khóa. Bạn muốn biết: liệu đây là người mà họ tuyên bố là (* xác minh*, 1:1), hay liệu đây là người đầu tiên trong ngân hàng đăng ký của bạn (* xác định*, 1:N)?

> Người dùng nói một câu lệnh. Bạn biết không: Đây là người mà họ tuyên bố là người đó?

> **【中文解读】**Câu hỏi được đặt ra trong phần này là: làm thế nào để hiểu và áp dụng đúng công nghệ này trong công trình thực tế.

Trước năm 2018: GMM-UBM + i-vector. EER hợp lý nhưng dễ bị hỏng khi chuyển đổi kênh (cô điện thoại so với máy tính xách tay) và cảm xúc. 20182022: x-vector (cột sống TDNN được đào tạo với biên góc). 2022+: ECAPA-TDNN và WavLM-bích sâu lớn. Đến năm 2026 lĩnh vực này bị thống trị bởi ba mô hình và một métric.

> 2018 年前:GMM-UBM + i-vectors。EER 合理但对信道偏移(电话 vs 笔记本) 和情绪敏感。2018-2022:x-vectors(用角度间隔训练的 TDNN 骨干)。2022+:ECAPA-TDNN 和 WavLM-large 嵌入──到2026 年,该领域由三个模型和一个指标主导────

Métric là**EER** Tỷ lệ lỗi bình đẳng. Đặt ngưỡng quyết định của bạn để Tỷ lệ chấp nhận sai = Tỷ lệ từ chối sai.

> Chỉ số này là**EER**等错误率──设置决策值使假接受率 =假拒绝率──交叉点就是 EER──用于每篇论文、每排行榜、每采购评审──

## Khái niệm cốt lõi

> **【中文解读】**Bài viết này giới thiệu các khái niệm và lý thuyết cốt lõi.


![Enrollment + verification pipeline with embedding + cosine + EER](../assets/speaker-verification.svg)

**The pipeline.**Đăng ký: ghi lại 530 giây của loa mục tiêu; tính toán một kết hợp kích thước cố định (192-d cho ECAPA-TDNN, 256-d cho WavLM-lớn).

> **流水线。**注册:录制目标说话人 5-30秒语音;计算固定维度嵌入(ECAPA-TDNN 为 192 维,WavLM-large 为 256 维) 验证:获取测试语音嵌入;计算余弦相似度;与值比较──

**ECAPA-TDNN (2020, still dominant 2026).**Căng cường Chuyện Chăm sóc kênh, Chuyện truyền và Tập hợp - Mạng thần kinh chậm thời gian. 1D conv khối với kích thích squeeze, tập hợp sự chú ý đa đầu, tiếp theo là một lớp tuyến tính đến 192-d. Được đào tạo trên VoxCeleb 1 + 2 (2,700 loa, 1.1M phát biểu) với mất biên độ góc phụ (AAM-softmax).

> **ECAPA-TDNN（2020，2026 年仍占主导）。**Nhấn mạnh thông qua tập trung, truyền tải và tập hợp thời gian 延神经网络──1D 卷积块 + squeeze-excitation + 多头注意池化,接线性层输出 192 维──在 VoxCeleb 1+2(2,700 说话人,110万条语音) 上加性角度间隔损失(AAM-softmax) 训练──

**WavLM-SV (2022+).**Định chỉnh xương sống SSL WavLM lớn được đào tạo trước với mất AAM. chất lượng cao hơn nhưng chậm hơn  300+ MB so với 15 MB.

> **WavLM-SV（2022+）。**Sử dụng AAM 损失微调预训的 WavLM-大SSL 骨干──质量更高但更慢300+ MB vs 15 MB──

**x-vector (baseline).**TDNN + thống kê tập hợp. Classic; vẫn hữu ích trên CPU / cạnh.

> **x-vector（基线）。**TDNN + 统计池化──经典方案; vẫn còn hữu ích trên các thiết bị CPU/边缘──

**AAM-softmax.**Softmax tiêu chuẩn với margin bổ sung `m`trong không gian góc: `cos(θ + m)`cho lớp đúng. lực phân tách góc giữa các lớp. điển hình `m=0.2`, quy mô `s=30`- Tôi không biết.

> **AAM-softmax。**Trong góc không gian thêm khoảng cách`m`                                                                                                                                                                                                                                                              `cos(θ + m)` Cấp độ giữa các góc phân chia.`m=0.2`,缩放 `s=30`

### Điểm số

> ### 评分

- **Cosine**giữa việc đăng ký và việc thử nghiệm.
  **余弦**Sự tương tự, tính toán giữa đăng ký và thử nghiệm.
- **PLDA (Probabilistic LDA).**Dự án nhúng vào một không gian ẩn trong đó cùng một loa so với người nói khác có tỷ lệ xác suất hình thức đóng. Thêm trên cosine để giảm +1020% EER. tiêu chuẩn trước năm 2020; bây giờ chỉ được sử dụng trong thiết lập tập hợp đóng.
  **PLDA（概率 LDA）。**sẽ được nhúng vào các dự án vào không gian tiềm ẩn, trong đó người nói nói với người nói khác có tỷ lệ đóng kín giống như vậy.
- **Score normalization.** `S-norm`hoặc `AS-norm`: bình thường hóa mỗi điểm với một nhóm các phương tiện giả mạo và các loại khác.
  **分数归一化。** `S-norm`Hoặc`AS-norm`: Đánh giá trung bình và tiêu chuẩn của nhóm người nhập khẩu được phân loại cho mỗi phân số.

### Số bạn nên biết (2026)

> 2026 năm bạn nên biết số

| Model | VoxCeleb1-O EER | Params | Throughput (A100) |
|-------|-----------------|--------|-------------------|
| x-vector (classic) | 3.10% | 5 M | 400× RT |
| ECAPA-TDNN | 0.87% | 15 M | 200× RT |
| WavLM-SV large | 0.42% | 316 M | 20× RT |
| Pyannote 3.1 segmentation + embedding | 0.65% | 6 M | 100× RT |
| ReDimNet (2024) | 0.39% | 24 M | 100× RT |

| 模型 | VoxCeleb1-O EER | 参数量 | 吞吐量（A100） |
|------|-----------------|--------|----------------|
| x-vector（经典） | 3.10% | 500 万 | 400× 实时 |
| ECAPA-TDNN | 0.87% | 1500 万 | 200× 实时 |
| WavLM-SV large | 0.42% | 3.16 亿 | 20× 实时 |
| Pyannote 3.1 分割 + 嵌入 | 0.65% | 600 万 | 100× 实时 |
| ReDimNet（2024） | 0.39% | 2400 万 | 100× 实时 |

### Lượng chảy máu

> ### Nói话人日志 ((谁在何时说话)

"Ai nói khi nào" trong clip multi-speaker. Pipeline: VAD → phân đoạn → nhúng mỗi phân đoạn → cluster (gộp hoặc quang phổ) → ranh giới mịn.`pyannote.audio`3.1, kết hợp phân đoạn loa + nhúng + tập hợp sau một cuộc gọi.

> 多说话人音频中"谁在何时说话"──流水线:VAD → 分段 → đối với mỗi段嵌入 →聚类(层聚类或谱聚类)→ 平滑边界──现代技术:`pyannote.audio`3.1,将说话人分割 + 嵌入 + 聚类打包为一个调用──2026 年 AMI 上 SOTA DER 约 15%(从2022 年的 23% 下降)──

> **【拓展：语音 AI 的产品化】**语音技术在产品化中面临独特挑战:不同口音,背景噪音,远场拾音,多人说话等. Siri, Alexa,小爱同学等产品都投入大量工程优化解决这些长尾问题.

> **【拓展：多语言语音技术】**Các đặc điểm ngữ âm của toàn cầu ngôn ngữ khác biệt rất lớn: tiếng调 ngôn ngữ (如中文) của âm cao mang ngữ nghĩa, nguồn lực thấp ngôn ngữ thiếu đào tạo dữ liệu.



## Hãy xây dựng nó.

> **【中文解读】**本节通过代码实现核心算法从零――这种" từ đầu"的方式能帮助理解框架背后的原理,遇到问题时不会被黑盒困住――

```figure
sp-eer-crossover
```

## Hãy xây dựng nó

### Bước 1: Nhập đồ chơi từ số liệu thống kê của MFCC

```python
def embed_mfcc_stats(signal, sr):
    frames = featurize_mfcc(signal, sr, n_mfcc=13)
    mean = [sum(f[i] for f in frames) / len(frames) for i in range(13)]
    std = [
        math.sqrt(sum((f[i] - mean[i]) ** 2 for f in frames) / len(frames))
        for i in range(13)
    ]
    return mean + std  # 26-d
```

Không phải là một dặm để chỉ dạy.`code/main.py`sử dụng điều này như là một bằng chứng về khái niệm trên dữ liệu loa tổng hợp.

> 离 SOTA 差得远 chỉ dùng để dạy học.`code/main.py`Giống như một khái niệm chứng minh của một người nói.

### Bước 2: tương tự cosine + ngưỡng

```python
def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(x * x for x in b))
    return dot / (na * nb) if na and nb else 0.0

def verify(enroll, test, threshold=0.75):
    return cosine(enroll, test) >= threshold
```

### Bước 3: EER từ các cặp tương đồng

```python
def eer(same_scores, diff_scores):
    thresholds = sorted(set(same_scores + diff_scores))
    best = (1.0, 1.0, 0.0)  # (fa, fr, threshold)
    for t in thresholds:
        fr = sum(1 for s in same_scores if s < t) / len(same_scores)
        fa = sum(1 for s in diff_scores if s >= t) / len(diff_scores)
        if abs(fa - fr) < abs(best[0] - best[1]):
            best = (fa, fr, t)
    return (best[0] + best[1]) / 2, best[2]
```

Trả về (eer, threshold_at_eer). báo cáo cả hai.

> 返回 (eer, threshold_at_eer) ⋅两者都要报告──

### Bước 4: sản xuất với SpeechBrain

```python
from speechbrain.pretrained import EncoderClassifier

clf = EncoderClassifier.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb")

# enroll: average the embeddings of 3-5 clean samples
enroll = torch.stack([clf.encode_batch(load(x)) for x in enrollment_clips]).mean(0)
# verify
score = clf.similarity(enroll, clf.encode_batch(load("test.wav"))).item()
verdict = score > 0.25   # ECAPA typical threshold; tune on your data
```

### Bước 5: ghi nhật ký với note

```python
from pyannote.audio import Pipeline

pipe = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1")
diarization = pipe("meeting.wav", num_speakers=None)
for turn, _, speaker in diarization.itertracks(yield_label=True):
    print(f"{turn.start:.1f}–{turn.end:.1f}  {speaker}")
```

> **【中文解读】**Bài này sẽ trình bày cách sử dụng một khung đã phát triển như PyTorch, HuggingFace, và các khác.





> **【拓展：语音与情感计算】**语音 không chỉ truyền tải thông tin văn bản, còn mang lại một tín hiệu cảm xúc phong phú (语调、语速、音高变化)  cảm xúc (语音识别, Speech Emotion Recognition, SER) có ứng dụng rộng rãi trong lĩnh vực kiểm tra chất lượng khách hàng, giám sát sức khỏe tâm thần, giáo dục thông minh, etc.  Mô hình SOTA hiện tại thường dựa trên wave2vec 2.0 hoặc HuBERT 等

## Hãy sử dụng nó để thực hiện

Số 2026:

> 2026 năm của công nghệ:

| Situation | Pick |
|-----------|------|
| Closed-set 1:1 verification, edge | ECAPA-TDNN + cosine threshold |
| Open-set verification, cloud | WavLM-SV + AS-norm |
| Diarization (meetings, podcasts) | `pyannote/speaker-diarization-3.1` |
| Anti-spoofing (replay / deepfake detection) | AASIST or RawNet2 |
| Tiny embedded (KWS + enrollment) | Titanet-Small (NeMo) |

| 场景 | 选择 |
|------|------|
| 封闭集 1:1 验证，边缘设备 | ECAPA-TDNN + 余弦阈值 |
| 开放集验证，云端 | WavLM-SV + AS-norm |
| 说话人日志（会议、播客） | `pyannote/speaker-diarization-3.1` |
| 反欺诈（回放/深度伪造检测） | AASIST 或 RawNet2 |
| 小型嵌入式（关键词检测 + 注册） | Titanet-Small（NeMo） |



## Những bẫy

> 常见陷

- **Channel mismatch.**Mô hình được đào tạo trên VoxCeleb (video web) ≠ âm thanh cuộc gọi điện thoại.
  **信道不匹配。**Mô hình đào tạo trên VoxCeleb không bằng với điện thoại.
- **Short utterances.**EER giảm mạnh dưới 3 giây âm thanh thử nghiệm.
  **短语音。**测试音频低于3秒时 EER 急剧恶化──
- **Enrollment with noise.**Một lần ghi âm tiếng ồn sẽ làm độc đinh.
  **带噪注册。**Một mẫu đăng ký trong tạp chí sẽ được hóa chất. Sử dụng ít nhất 3 mẫu sạch và lấy trung bình.
- **Fixed threshold across conditions.**Luôn điều chỉnh ngưỡng trên một bộ phát triển được giữ từ miền mục tiêu.
  **跨条件固定阈值。**始终在目标领域的留出开发集上调整值──
- **Cosine on non-normalized embeddings.**L2- bình thường trước; nếu không, độ lớn thống trị.
  **未归一化嵌入上的余弦。**Trước làm L2 归一化;否则模值会占主导.

> **【中文解读】**Phần này tập trung vào cách phân phối mô hình như một sản phẩm có thể sử dụng.


## Chuyển nó đi.

Cứ như `outputs/skill-speaker-verifier.md`- Chọn mô hình, giao thức đăng ký, kế hoạch điều chỉnh ngưỡng và bảo vệ gian lận.

> 保存为 `outputs/skill-speaker-verifier.md` lựa chọn mô hình, hợp đồng đăng ký, chương trình và biện pháp phòng chống gian lận.

## Tập luyện bài tập

> **【中文解读】**Trong 术语表中的"Những gì mọi người nói" vs "Những gì nó thực sự có nghĩa" 区分日常口语和精确技术含义── 在团队协作中,统一术语定义可以避免大量沟通误解──


1. **Easy.**Đi chạy`code/main.py`- Xây dựng "những loa" tổng hợp (những hồ sơ âm thanh khác nhau), ghi danh, tính toán EER trong danh sách thử nghiệm 100 cặp.
   **简单。**运行 `code/main.py`❖ xây dựng tổng hợp "说话人" (语调配置), đăng ký, trong 100 đối với các danh sách thử nghiệm trên số liệu EER
2. **Medium.**Sử dụng SpeechBrain ECAPA trên 30 phát biểu VoxCeleb1 (mỗi phát ngôn viên 5 × 6).
   **中等。**Trong 30 条 VoxCeleb1 语音上使用SpeechBrain ECAPA(5 个说话人 × 6 条) ――用余弦和 PLDA 计算 EER。
3. **Hard.**Xây dựng toàn bộ đăng ký → nhật ký → xác minh đường ống với `pyannote.audio`Đánh giá DER trên bộ phát triển AMI.
   **困难。**用 `pyannote.audio`构建完整的注册 → 日志 → 验证流水线──在 AMI 开发集上评估 DER──

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| EER | The headline metric | Threshold where False Accept = False Reject. |
| Verification | 1:1 | "Is this Alice?" |
| Identification | 1:N | "Who is speaking?" |
| Open-set | Unknown possible | Test set can contain unenrolled speakers. |
| Enrollment | Registering | Computing a speaker's reference embedding. |
| AAM-softmax | The loss | Softmax with additive angular margin; forces cluster separation. |
| PLDA | Classic scoring | Probabilistic LDA; likelihood-ratio scoring on top of embeddings. |
| DER | Diarization metric | Diarization Error Rate — miss + false alarm + confusion. |

| 术语 | 人们常说的 | 实际含义 |
|------|-----------|---------|
| EER | 头条指标 | 假接受率 = 假拒绝率时的阈值。 |
| 验证 | 1:1 | "这是 Alice 吗？" |
| 识别 | 1:N | "谁在说话？" |
| 开放集 | 可能有未知者 | 测试集可包含未注册的说话人。 |
| 注册 | 登记 | 计算说话人的参考嵌入。 |
| AAM-softmax | 那个损失 | 带加性角度间隔的 softmax；强制聚类分离。 |
| PLDA | 经典评分 | 概率 LDA；嵌入之上的似然比评分。 |
| DER | 日志指标 | 说话人日志错误率——漏检 + 误检 + 混淆。 |

> **【中文解读】**延伸阅读 cung cấp các nguồn chất lượng cao cho việc học sâu. Những bài báo và giảng dạy này là tài liệu tham khảo cổ điển trong lĩnh vực này, phù hợp với những người đọc cần hiểu sâu hơn.


## Xem thêm 延伸阅读

- [Snyder et al. (2018). X-Vectors: Robust DNN Embeddings for Speaker Recognition](https://www.danielpovey.com/files/2018_icassp_xvectors.pdf) giấy sâu sâu cổ điển.
  Snyder 等 (2018). X-Vectors: nói话人识别的鲁棒 DNN 嵌入经典的深度嵌入论文──
- [Desplanques et al. (2020). ECAPA-TDNN](https://arxiv.org/abs/2005.07143) kiến trúc thống trị 20202026.
  Các dự án này được tổ chức từ năm 2020 đến năm 2026.
- [Chen et al. (2022). WavLM: Large-Scale Self-Supervised Pre-Training for Full Stack Speech Processing](https://arxiv.org/abs/2110.13900) Lớp xương sống SSL cho SV và nhật ký hóa.
  Chen 等 (2022). WavLM: toàn bộ xử lý tiếng Anh quy mô lớn tự giám sát dự kiến đào tạo SV 和日志的 SSL 骨干──
- [Bredin et al. (2023). pyannote.audio 3.1](https://github.com/pyannote/pyannote-audio) nhật ký sản xuất + đống nhúng.
  Bredin 等 (2023). pyannote.audio 3.1生产级日志 + 嵌入技术。
- [VoxCeleb leaderboard (updated 2026)](https://www.robots.ox.ac.uk/~vgg/data/voxceleb/) Định dạng EER hiện tại trên các mô hình.
  VoxCeleb 排行榜(2026年更新) 各模型当前 EER 排名。

> **【中文解读】**延伸阅读 cung cấp các nguồn chất lượng cao để học sâu, bao gồm các bài báo, giảng dạy và công cụ.

