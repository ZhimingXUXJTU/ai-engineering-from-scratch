# Đánh giá  FID, CLIP Score, Tích thích con người   đánh giá chỉ số  FID  CLIP Score và sở thích con người

> Mỗi bảng xếp hạng mô hình tạo ra chỉ trích FID, điểm CLIP và tỷ lệ thắng từ một lĩnh vực ưu tiên của con người. Mỗi số có chế độ thất bại mà một nhà nghiên cứu xác định có thể chơi. Nếu bạn không biết các chế độ thất bại, bạn không thể thấy sự cải thiện thực sự từ một cuộc chơi.

> **【中文解读】**Mỗi bảng xếp hạng mô hình tạo đều trích dẫn FID (Fréchet Inception Distance) ✓ CLIP Score và tỷ lệ ưu tiên của con người.

> **【拓展：FID 的局限性】**FID đo khoảng cách phân phối tạo hình ảnh với hình ảnh thực, nhưng nó có thể được tối ưu hóa như chọn lọc tạo mẫu cao.

**Type:** Build / 构建型 | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 8 · 01 (Taxonomy / 分类), Phase 2 · 04 (Evaluation Metrics / 评估指标) | **前置知识:** 阶段 8 · 01（分类），阶段 2 · 04（评估指标）
**Time:** ~45 minutes | **预计用时:** ~45 分钟

## Vấn đề  vấn đề giới thiệu

Một mô hình tạo được đánh giá dựa trên * chất lượng mẫu * và * tuân thủ điều kiện *. Cả hai đều không có thước đo hình thức đóng. Mô hình của bạn phải hiển thị 10.000 hình ảnh; có gì đó phải gán cho chúng số; bạn phải tin vào số trên các gia đình mô hình, trên các độ phân giải, trên các kiến trúc. Ba métrics đã sống sót qua bàn tay 2014-2026:

> 生成模型以*样本质量*和*条件遵循度*评判──两者都没有闭式度量──你的模型必须染色 10000张图像;必须有东西给它们打分──三个指标经历了2014-2026的考试:

- **FID (Fréchet Inception Distance).**Khoảng cách giữa hai phân phối  thực và tạo  trong không gian tính năng của mạng Inception.
  **FID。**Sự thật và sản xuất phân bố trong Inception 网络特征空间中的距离──越低越好──
- **CLIP score.**Sự tương đồng giữa việc nhúng hình ảnh CLIP của một hình ảnh được tạo và nhúng văn bản CLIP của một prompt. cao hơn là tốt hơn. đo lường sự tuân thủ nhanh chóng.
  **CLIP Score。**生成图像与文本提示的 CLIP 嵌入余弦相似度──越高越好──
- **Human preference.**Đặt hai mô hình trực tiếp trên cùng một lời nhắc, để con người (hoặc mô hình lớp GPT-4) chọn tốt hơn, tổng hợp đến điểm Elo.
  **人类偏好。**Hai mô hình đầu đối đầu, nhân loại hoặc GPT-4 级 mô hình chọn tốt hơn, tập hợp thành Elo 分数──

Bạn cũng sẽ thấy: IS (điểm khởi điểm, phần lớn nghỉ hưu), KID, CMMD, ImageReward, PickScore, HPSv2, MJHQ-30k. Mỗi sửa chữa cho một thất bại của trước đó.

> Bạn sẽ thấy:IS( đã bị loại bỏ) ✓KID、CMMD、ImageReward、PickScore、HPSv2 等── mỗi người đều sửa chữa một số lỗ hổng của người trước đó──

> **【中文解读】**3 chỉ số lớn của việc đánh giá mô hình sinh sản: 1) FID trong không gian tính năng mạng khi bắt đầu đo khoảng cách phân phối và phân phối thực sự, càng thấp hơn; 2) CLIP Score tạo ra hình ảnh và kết hợp ngữ nghĩa của prompt văn bản, càng cao hơn; 3) Nhựa của con người hai mô hình so với lựa chọn tốt hơn, tập hợp cho Elo phân số。 mỗi chỉ số có lỗ hổng đã biết, sử dụng kết hợp đáng tin cậy hơn。

> **【拓展：生成模型评估的"刷榜"问题】**FID có thể được tối ưu hóa thông qua chọn lọc tạo ra các mẫu cao, điều chỉnh Lớp tính của mô hình bắt đầu hoặc quá phù hợp với phân phối tham chiếu. CLIP Score cũng có sự thiên vị. CLIP mô hình đánh giá sự ưa thích của con người hơn với một số khái niệm.

## Khái niệm cốt lõi

![FID, CLIP, and preference: three axes, different failure modes](../assets/evaluation.svg)

### FID  chất lượng mẫu  FID  chất lượng mẫu

Heusel et al. (2017).

> Heusel 等人(2017)。步骤:

1. Tạo các tính năng Inception-v3 (2048-D) cho N hình ảnh thực và N tạo.
   为 N 张真实图像和 N 张生成图像提取 创始-v3 特征(2048 维) 』
2. Đưa một Gaussian vào mỗi hồ bơi: tính trung bình`μ_r, μ_g`và sự đồng hóa`Σ_r, Σ_g`- Tôi không biết.
   Đối với mỗi đống có thể: tính trung bình`μ_r, μ_g`和协方差 `Σ_r, Σ_g`
3. FID = `||μ_r - μ_g||² + Tr(Σ_r + Σ_g - 2 · (Σ_r · Σ_g)^0.5)`- Tôi không biết.
   FID = `||μ_r - μ_g||² + Tr(Σ_r + Σ_g - 2 · (Σ_r · Σ_g)^0.5)`

Giải thích: Khoảng cách Fréchet giữa hai Gaussia đa biến trong không gian tính năng.

> 解读: đặc điểm không gian giữa hai đa nguyên cao hơn phân bố Frechet khoảng cách.

Các chế độ thất bại:

> 失败模式:

- **Biased on small N.**FID là trung bình vuông trên phân phối tính năng  N nhỏ đánh giá thấp sự khác nhau, cho FID thấp sai.
  小 N 偏差:FID là sự khác biệt trung bình trên phân bố đặc điểm,小 N 会低估协方差, đưa ra FID thấp giả mạo.
- **Inception-dependent.**Inception-v3 được đào tạo trên ImageNet. Các miền xa khỏi ImageNet (những khuôn mặt, nghệ thuật, hình ảnh văn bản) tạo ra FID vô nghĩa. Sử dụng một bộ trích xuất tính năng cụ thể cho miền.
  Tùy thuộc vào Inception:Inception-v3 trong ImageNet 上训练──远离 ImageNet's domain (phân hình người, nghệ thuật,文字图像) sẽ tạo ra FID không có ý nghĩa── sử dụng các đặc điểm cụ thể trong lĩnh vực này──
- **Gaming.**Việc trang bị quá mức cho Inception trước tạo ra FID thấp mà không cải thiện chất lượng thị giác.
  刷分: đối với Inception đã thử nghiệm được chuẩn bị có thể cung cấp FID thấp nhưng chất lượng hình ảnh không được nâng cao.

### CLIP score  nhanh chóng tuân thủ  CLIP score  nhanh chóng tuân thủ

Radford et al. (2021). Đối với hình ảnh được tạo + prompt:

> Radford 等人(2021)。 đối với tạo hình ảnh + prompt:

```
clip_score = cos_sim( CLIP_image(x_gen), CLIP_text(prompt) )
```

Trung bình trên 30k hình ảnh được tạo ra → một mô hình có thể so sánh giữa các mô hình.

> Đối với 30k 张 tạo hình ảnh tìm trung bình → một mô hình có thể so sánh với số lượng mô hình.

Các chế độ thất bại:

> 失败模式:

- **CLIP's own blind spots.**CLIP có lý luận thành phần yếu ("một khối đỏ trên một quả cầu xanh" thường thất bại).
  CLIP 自身的盲点:CLIP 组合推理能力弱 (các người thường thất bại trong CLIP Score) 模型 có thể xếp hạng trên CLIP Score nhưng thực tế không thực sự theo dõi các bước phức tạp.
- **Short prompt bias.**Các lời nhắc ngắn có nhiều kết hợp hình ảnh CLIP hơn trong tự nhiên.
  短快 偏差:短快 在野外有更多的 CLIP-image 匹配──长快 在 CLIP Score 上机械性地更低──
- **Prompt gaming.**Bao gồm "đất lượng cao, 4k, tác phẩm xuất sắc" trong lời nhắc thổi phồng điểm CLIP mà không cải thiện kết nối hình ảnh-môn văn bản.
  刷分: 在 prompt 中加入" chất lượng cao, 4k, tác phẩm xuất sắc" 能升高 CLIP Score而不改善图文绑定──

CMMD (Jayasumana et al., 2024) khắc phục một số điều này: sử dụng các tính năng CLIP thay vì Inception, sự khác biệt trung bình tối đa thay vì Fréchet.

> CMMD(Jayasumana 等人 2024) đã sửa đổi một số vấn đề: sử dụng CLIP đặc điểm thay vì khởi đầu, sử dụng MMD(最大平均值差异) thay vì Frechet 距离──更善于检测细微的质量差异──

### Ưu tiên của con người  Sự thật trên mặt đất  Ưu tiên của con người  Ưu tiên thực tế

Chọn một nhóm các lời nhắc. Tạo ra với mô hình A và mô hình B. Cho thấy cặp với con người (hoặc một thẩm phán LLM mạnh mẽ). tổng hợp chiến thắng thành điểm số Elo hoặc Bradley-Terry. Điểm chuẩn:

> 选择一批提示――用模型 A 和模型 B 生成――把成对结果展示给人类 (或强 LLM 评判) ‖把胜场聚聚合为 Elo 或 Bradley-Terry 分数――基准:

- **PartiPrompts (Google)**: 1.600 yêu cầu khác nhau, 12 loại.
  **PartiPrompts（Google）**: 1600 个多样化 prompt,12 个类别:
- **HPSv2**: 107k chú thích của con người, được sử dụng rộng rãi như một đại diện tự động.
  **HPSv2**10,70.000 bài đăng về người dùng, sử dụng rộng rãi như một đại diện tự động.
- **ImageReward**: 137k cặp ưu tiên hình ảnh nhanh, được MIT cấp phép.
  **ImageReward**13,7 triệu cho lượt ảnh nhanh, MIT อนุญาต
- **PickScore**: được đào tạo về các sở thích Pick-a-Pic 2.6M.
  **PickScore**Trong tập luyện, có khoảng 260 triệu người thích tập.
- **Chatbot-Arena-style image arenas**https://imagearena.ai/và những người khác.
  **Chatbot-Arena 风格的图像竞技场**- Có thể là:https://imagearena.ai/Đúng vậy.

Các chế độ thất bại:

> 失败模式:

- **Judge variance.**Những người không chuyên môn có sở thích khác với các chuyên gia.
  评判者方差: phi chuyên gia và chuyên gia có sự lựa chọn khác nhau.
- **Prompt distribution.**Những lời khuyên được chọn từ một gia đình luôn là tài liệu.
  Ưu tiên: Ưu tiên: Ưu tiên: Ưu tiên: Ưu tiên: Ưu tiên: Ưu tiên: Ưu tiên: Ưu tiên: Ưu tiên: Ưu tiên: Ưu tiên: Ưu tiên: Ưu tiên: Ưu tiên: Ưu tiên: Ưu tiên: Ưu tiên: Ưu tiên: Ưu tiên: Ưu tiên: Ưu tiên: Ưu tiên: Ưu tiên: Ưu tiên: Ưu tiên: Ưu tiên: Ưu tiên: Ưu tiên: Ưu tiên: Ưu tiên: Ưu tiên: Ưu tiên: Ưu tiên: Ưu tiên: Ưu tiên: Ưu tiên: Ưu tiên: Ưu tiên: Ưu tiên: Ưu tiên: Ưu tiên: Ưu tiên: Ưu tiên: Ưu tiên: Ưu tiên: Ưu tiên: Ưu tiên: Ưu tiên: Ưu tiên: Ưu tiên: Ưu tiên: Ưu tiên: Ưu tiên: Ưu tiên: Ưu tiên: Ưu tiên: Ưu tiên: Ưu tiên: Ưu tiên: Ưu tiên: Ưu tiên: Ưu tiên: Ưu tiên: Ưu tiên: Ưu tiên:
- **LLM-judge reward hacking.**Thẩm phán GPT-4 bị lừa bởi những kết quả đẹp nhưng sai.
  LLM 评判被刷分:GPT-4 评判会被"好看但错"的输出欺骗──与人类三角验证──

## Sử dụng cùng nhau

Một báo cáo đánh giá sản xuất nên bao gồm:

> Một báo cáo đánh giá cấp sản xuất nên bao gồm:

1. FID trên 10-30k mẫu đối với phân phối thực (chất lượng mẫu).
   Trong 10-30k mẫu tương đối để lại phân phối thực FID(chất lượng mẫu)
2. Điểm CLIP / CMMD trên cùng một mẫu so với các yêu cầu của họ (sự tuân thủ).
   相同本相对各自提示的 CLIP Score / CMMD (CCMD)
3. Tỷ lệ thắng trong một đấu trường bị mù so với mô hình trước (tổng ưu tiên).
   Với mô hình trước đây, tỷ lệ thắng trong đấu trường blind đánh giá
4. Phân tích chế độ thất bại: 50 đầu ra được lấy mẫu ngẫu nhiên, được đánh dấu cho các vấn đề được biết (phân giải của tay, trình chiếu văn bản, con số đối tượng nhất quán).
   失败模式分析:随机采样 50 输出,标记已知问题(手部解剖、文字染、对象计数一致性)

Bất kỳ chỉ số nào cũng là dối trá. Ba chỉ số xác nhận + đánh giá chất lượng là một tuyên bố.

> Bất kỳ chỉ số đơn lẻ nào đều là dối trá.

## Hãy xây dựng nó.
```figure
gx-fid-distributions
```

## Hãy xây dựng nó

`code/main.py`thực hiện FID, CLIP-score-like, và Elo tổng hợp trên tổng hợp "vector tính năng" (chúng tôi sử dụng vector 4-D như là stand-in cho tính năng Inception).

> `code/main.py`Trong tổng hợp "trặc tính chiều" trên thực hiện FID、类 CLIP Score 和 Elo 聚合(Chúng tôi sử dụng 4 维向量 thay thế Trặc tính khởi đầu) ・・・ bạn sẽ thấy:

- Phân tính FID trên một N nhỏ và trên một N lớn  sự thiên vị.
  小 N 和 大 N 上 的 FID 计算偏差──
- "Chit điểm CLIP" như sự tương đồng cosine giữa các bộ tích tính năng.
  作为特征池之间余弦相似度的"CLIP Score" (tạm dịch: điểm CLIP)
- Quy tắc cập nhật Elo từ một dòng ưu tiên tổng hợp.
  Từ tạo ra các định hướng của Elo 更新规则──

### Bước 1: FID trong bốn dòng.

```python
def fid(real_features, gen_features):
    mu_r, cov_r = mean_and_cov(real_features)
    mu_g, cov_g = mean_and_cov(gen_features)
    mean_diff = sum((a - b) ** 2 for a, b in zip(mu_r, mu_g))
    trace_term = trace(cov_r) + trace(cov_g) - 2 * sqrt_cov_product(cov_r, cov_g)
    return mean_diff + trace_term
```

> FID: phân biệt đối với tính toán trung bình và tính toán so sánh, tính toán trung bình so sánh cộng cộng cộng cộng cộng cộng cộng khác biệt.

### Bước 2: CLIP kiểu cosine-similarity 步骤 2: CLIP 风格余弦相似度

```python
def clip_like(image_feat, text_feat):
    dot = sum(a * b for a, b in zip(image_feat, text_feat))
    norm = math.sqrt(dot_self(image_feat) * dot_self(text_feat))
    return dot / max(norm, 1e-8)
```

> CLIP 风格余弦相似度: điểm积除以两个向量范数乘积,加epsilon 防止除零──

### Bước 3: Tập hợp Elo

```python
def elo_update(r_a, r_b, winner, k=32):
    expected_a = 1 / (1 + 10 ** ((r_b - r_a) / 400))
    actual_a = 1.0 if winner == "a" else 0.0
    r_a_new = r_a + k * (actual_a - expected_a)
    r_b_new = r_b - k * (actual_a - expected_a)
    return r_a_new, r_b_new
```

> Elo 更新: dựa trên tỷ lệ thắng và kết quả thực tế điều chỉnh số lượng, K=32 là tiêu chuẩn cờ bạc quốc tế.

## # Thói bẫy #

- **FID at N=1000.**Heuristic không đáng tin cậy dưới N=10k. Các báo cáo báo cáo FID thấp N đang chơi game.
  N=1000 时的FID: trong N<10k 时不可靠──报告低 N FID 的论文在刷分──
- **Comparing FID across resolutions.**Sự thay đổi kích thước của Inception là 299 × 299 thay đổi phân phối tính năng. So sánh chỉ ở độ phân giải phù hợp.
  跨分辨率比较 FID:Inception 的 299×299 缩放会改变特征分布──只在匹配分辨率下比较──
- **Reporting one seed.**Đi 3 hạt tối thiểu.
  Chỉ báo một hạt giống: ít nhất chạy 3 hạt giống.
- **CLIP score inflation via negative prompts.**Một số đường ống tăng CLIP bằng cách over-mở các prompt.
  通过负向快速 抬高 CLIP Score:有些流水线通过过拟合快速 抬高 CLIP──检查视觉和──
- **Elo bias from prompt overlap.**Nếu cả hai mô hình thấy một điểm chuẩn trong quá trình đào tạo, Elo là vô nghĩa. Sử dụng các bộ nhắc nhở kéo dài.
  Lần đầu tư dẫn đến Elo 偏差: Nếu hai mô hình được đào tạo khi thấy được Kỷ chuẩn prompt, Elo 无意义──使用留出的 prompt 集──
- **Human eval paid-crowd skew.**Những nhà ghi chú MTurk có nhiều sản phẩm, có xu hướng trẻ hơn / thân thiện với công nghệ.
  Nhân công đánh giá trả phí 偏差:Prolific、MTurk 标注者偏年轻 / 偏技术友好──混合招募的艺术/设计专家──

## Hãy sử dụng nó để thực hiện

Nghị định giá sản xuất vào năm 2026:

> Hiệp định đánh giá cấp sản xuất năm 2026:

| Pillar / 支柱 | Minimum / 最低要求 | Recommended / 推荐 |
|--------|---------|-------------|
| Sample quality / 样本质量 | FID on 10k vs held-out real | + CMMD on 5k + FID on subset per category |
| Prompt adherence / Prompt 遵循 | CLIP score on 30k | + HPSv2 + ImageReward + VQA-style question answering |
| Preference / 偏好 | 200 blinded pairs vs baseline | + 2000 paired human + LLM-judge + Chatbot Arena |
| Failure analysis / 失败分析 | 50 hand-flagged | 500 hand-flagged + automated safety classifier |

Tất cả bốn trụ cột trong một báo cáo = yêu cầu.

> Bốn trụ cột hoàn toàn là một tuyên bố. Bất cứ một cái gì duy nhất chỉ là một thương mại.

## Chuyển nó đi.

- Cứu lại`outputs/skill-eval-report.md`. Skill lấy một điểm kiểm soát mô hình mới + đường cơ sở và đưa ra một kế hoạch đánh giá đầy đủ: kích thước mẫu, số liệu, các thăm dò chế độ thất bại, tiêu chí ký kết.

> 保存为 `outputs/skill-eval-report.md` Nghề này nhận được một điểm kiểm soát mô hình mới + 基线, xuất bản kế hoạch đánh giá đầy đủ: mẫu số, chỉ số, mô hình thất bại, tiêu chuẩn ký kết.

## Tập luyện bài tập

1. **Easy.**Đi chạy`code/main.py`So sánh FID ở N=100 so với N=1000 trên cùng một phân phối tổng hợp.
2. **Medium.**Thực hiện CMMD từ các tính năng kiểu CLIP tổng hợp (xem Jayasumana et al., 2024 cho công thức). So sánh độ nhạy với sự khác biệt chất lượng so với FID.
3. **Hard.**Tái tạo thiết lập HPSv2: lấy 1000 cặp hình ảnh-quan nhanh từ một bộ phụ của Pick-a-Pic, chỉnh điểm nhỏ dựa trên CLIP trên sở thích, và đo sự phù hợp của nó với một bộ kéo dài.

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| FID | "Fréchet Inception Distance" | Fréchet distance of Gaussian fits to real vs gen Inception features. |
| CLIP score | "Text-image similarity" | Cosine similarity between CLIP image and text embeddings. |
| CMMD | "FID's replacement" | CLIP-feature MMD; less biased, no Gaussian assumption. |
| IS | "Inception score" | Exp KL(p(y|x) || p(y)); correlates poorly on modern models, retired. |
| HPSv2 / ImageReward / PickScore | "Learned preference proxies" | Small models trained on human preferences; used as automatic judges. |
| Elo | "Chess rating" | Bradley-Terry aggregation of pairwise wins. |
| PartiPrompts | "The benchmark prompt set" | 1,600 Google-curated prompts across 12 categories. |
| FD-DINO | "Self-sup replacement" | FD using DINOv2 features; better for out-of-ImageNet domains. |

## Lưu ý sản xuất: đánh giá là một khối lượng công việc suy luận quá

Tiếp tục FID trên các mẫu 10k có nghĩa là tạo ra hình ảnh 10k. Đối với một cơ sở SDXL 50 bước ở 10242 trên một L4, đó là ~ 11 giờ suy luận đơn yêu cầu. Ngân sách đánh giá là thực, và khung chính xác là kịch bản suy luận ngoại tuyến (tăng cường thông qua, bỏ qua TTFT):

- **Batch hard, forget latency.**Offline eval = batching tĩnh ở kích thước lớn nhất phù hợp với bộ nhớ. `pipe(...).images`với `num_images_per_prompt=8`trên một chiếc 80GB H100 chạy nhanh hơn 4 đến 6 lần so với một lần yêu cầu.
- **Cache the real features.**Việc khai thác tính năng Inception (FID) hoặc CLIP (CLIP-score, CMMD) trên bộ tham chiếu thực được chạy * một lần*, được lưu trữ như một`.npz`Đừng tính lại cho mỗi đánh giá.

Đối với CI / cửa quay trở: chạy điểm FID + CLIP trên một bộ phụ 500 mẫu mỗi PR (~ 30 phút); chạy đầy đủ 10k FID + HPSv2 + Elo mỗi đêm.

## Xem thêm 延伸阅读

- [Heusel et al. (2017). GANs Trained by a Two Time-Scale Update Rule Converge to a Local Nash Equilibrium (FID)](https://arxiv.org/abs/1706.08500) Bức giấy FID.
- [Jayasumana et al. (2024). Rethinking FID: Towards a Better Evaluation Metric for Image Generation (CMMD)](https://arxiv.org/abs/2401.09603) CMMD.
- [Radford et al. (2021). Learning Transferable Visual Models from Natural Language Supervision (CLIP)](https://arxiv.org/abs/2103.00020) CLIP.
- [Wu et al. (2023). HPSv2: A Comprehensive Human Preference Score](https://arxiv.org/abs/2306.09341) HPSv2.
- [Xu et al. (2023). ImageReward: Learning and Evaluating Human Preferences for Text-to-Image Generation](https://arxiv.org/abs/2304.05977) ImageReward.
- [Yu et al. (2023). Scaling Autoregressive Models for Content-Rich Text-to-Image Generation (Parti + PartiPrompts)](https://arxiv.org/abs/2206.10789) PartiPrompts.
- [Stein et al. (2023). Exposing flaws of generative model evaluation metrics](https://arxiv.org/abs/2306.04675) Đánh giá chế độ thất bại.
