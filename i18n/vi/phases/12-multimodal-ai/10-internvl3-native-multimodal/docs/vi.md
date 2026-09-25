# InternVL3: Đào tạo đa phương tiện bản địa Ứng dụng

> Mỗi VLM mở trước InternVL3 đều theo cùng một công thức ba bước: lấy một văn bản LLM được đào tạo trên hàng nghìn tỷ mã thông báo văn bản, bấm vào một bộ mã hóa thị giác, sau đó chỉnh sửa các đường nét. Điều này hoạt động nhưng có nợ sắp xếp  văn bản LLM đã chi tiêu toàn bộ ngân sách trước đào tạo của mình cho văn bản thuần túy và không hiểu bản địa các token hình ảnh. Khi bạn thêm tầm nhìn sau khi làm việc, LLM phải học lại cách liên kết đầu vào trực quan với lý luận văn bản mà không quên văn bản. InternVL3 (Zhu et al., tháng 4 năm 2025) bác bỏ cách tiếp cận sau hoc: một chạy trước khi tập luyện, văn bản và đa phương thức được giao tiếp từ bước một. Kết quả tương ứng với Gemini 2.5 Pro trên MMMU-Pro ở 78B. Bài học này sẽ giải thích về việc đào tạo trước bản địa và những gì thay đổi khi bạn làm điều đó.

> **【中文解读】**Sự đổi mới cốt lõi của InternVL3: từ chối "được đào tạo trước văn bản LLM tái tiếp nhận văn bản lập trình" chương trình sau, thay đổi từ bước đầu về văn bản và nhiều mô hình dữ liệu giao tiếp đào tạo.

> **【拓展：原生预训练 vs 后装的成本权衡】**Dự án dự án sau sinh đã loại bỏ nợ nần, nhưng chi phí cao hơn nhiều so với dự án sau sinh ổng  cần hàng triệu GPU thời gian từ đầu, và từ bỏ tính linh hoạt của cơ sở LLM thay thế bất cứ lúc nào. Đối với hầu hết các dự án, dự án sau sinh vẫn còn kinh tế hơn.

**Type:** Learn  | **类型：学习**
**Languages:** Python (stdlib, training-corpus mixer)  | **语言：Python（标准库，训练语料混合器）**
**Prerequisites:** Phase 12 · 05, Phase 12 · 07 (recipes)  | **前置：阶段12第05课、阶段12第07课（配方）**
**Time:** ~120 minutes  | **时长：约120分钟**

>  **【前置】**Học本节前请先掌握:Phase 12·05(LLaVA 后装方案) 、Phase 12·07(开源 VLM 配方) ⋅本节是"反 LLaVA"拒后装,主张原生多模态预训――
>  **【类比】**后装 VLM(LLaVA) = "成年后学外语"已经掌握母语(文本),再艰难学第二语言(视觉) ・・・原生 VLM(InternVL3) = "双语家庭长大"两种语言同时学,没有翻译损耗──后装方案便宜但有口音(对齐债务),原生方案昂贵但流利──
> 🤔 **【困惑】**Q: 既然原生预训练如此好,为什么LLaVA 仍然主流? 成本!原生预训练需要数百万GPU 小时从头跑(一次 ~数百万美元),后装LLaVA只需8×A100 跑一天――除非你是大厂从头训新模型,否则LLaVA 路线性价格高得多――

## Mục tiêu học tập

- Giải thích tại sao đào tạo VLM sau khi làm việc tập trung nợ sắp xếp, trích dẫn ba triệu chứng có thể đo lường (hoàn quên thảm họa, dẫn dắt trả lời, không phù hợp văn bản thị giác).
- Mô tả sự kết hợp cơ thể trước tập luyện của InternVL3 và lý do tại sao tỷ lệ văn bản: liên kết: phụ đề quan trọng.
- So sánh V2PE (tạo mã vị trí thị giác biến đổi) với M-RoPE của Qwen2-VL.
- Tên của Visual Resolution Router (ViR) và DvD (Discoupled Vision-Language) triển khai tối ưu hóa.

## Vấn đề  vấn đề nền

Các khóa đào tạo VLM sau đại học là mặc định. LLaVA, BLIP-2, Qwen-VL, Idefics  tất cả đều có một LLM đã được đào tạo trước (Llama, Vicuna, Qwen, Mistral) và thêm thị lực.

1. Thử nghiệm làm việc bằng cách làm việc của mình. Thử nghiệm làm việc bằng cách làm việc của mình.
2. Giải phóng LLM, đào tạo về dữ liệu hướng dẫn (LLaVA-Instruct, ShareGPT4V).
3. Tùy chọn tùy chỉnh kỹ thuật cụ thể.

Ba triệu chứng của nợ sắp xếp xuất hiện:

- Sự quên lãng thảm khốc / 灾难性遗忘. VLM sau khi làm việc quên đi kỹ năng chỉ dùng văn bản. Điểm GSM8K giảm 5-10 điểm. Điểm Hellaswag giảm.
- Câu trả lời: Drift / 回答漂移. Các cụm từ nhỏ của cùng một câu hỏi trực quan có được các câu trả lời khác nhau.
- Visual-text inconsistency / 视觉-文本不一致. VLM có thể mô tả một hình ảnh một cách chính xác và sau đó trả lời một câu hỏi mâu thuẫn với mô tả của riêng nó.

> **【中文解读】**Các mô hình của VLM được mô tả đúng, nhưng lại đưa ra những câu trả lời mâu thuẫn. Những triệu chứng này là bởi vì các biểu tượng hình ảnh không giống như các biểu tượng văn bản đã tham gia sâu vào kiểm tra phù hợp bên trong LLM.

## Khái niệm cốt lõi

### Đội hình đa phương tiện chuẩn bị

InternVL3 đào tạo từ đầu trên một cơ thể là đa phương pháp bản địa từ bước một.

- 40% dữ liệu chỉ có văn bản (FineWeb, Proof-Pile-2, vv) / 40% 纯文本数据
- 35% dữ liệu hình ảnh-môn ngữ được giao tiếp (OBELICS, kiểu MMC4) / 35% 交织图文数据
- 20% dữ liệu ghi chú hình ảnh kết hợp / 20% 图文配对数据
- 5% dữ liệu video văn bản / 5% 视频文本数据

Các token thị giác, token văn bản và tương tác chéo-mô-đal đều tham gia vào sự mất mát tương tự từ bước gradient đầu tiên. Không có sự sắp xếp trước khi tập luyện, không có giai đoạn đóng băng máy chiếu, không có sự quên lãng thảm khốc để phục hồi.

Việc đào tạo là một giai đoạn duy nhất cho mô hình cơ bản.

> **【中文解读】**InternVL3 từ bước đầu tiên về việc đưa ra các biểu tượng hình ảnh、 văn bản token 和跨模态交互纳入 cùng một hàm mất mát── không cần chuẩn bị huấn luyện, không cần thiết cho máy chiếu kết thúc giai đoạn, không cần thiết phục hồi từ quên lãng thảm họa── cơ bản mô hình đã được xem như một công dân bình đẳng sau khi hoàn thành các bài tập chuẩn bị──

### V2PE (tự định vị hình ảnh biến đổi)

Qwen2-VL sử dụng M-RoPE với phân bổ trục cố định. InternVL3 giới thiệu V2PE: mã hóa vị trí thay đổi theo loại phương thức (tinh văn, hình ảnh, video) với quy mô học tập.

- Các mã thông báo văn bản có vị trí 1D (tín chỉ văn bản).
- Các bản vá hình ảnh có vị trí 2D (đường, cột).
- Các khung hình video có vị trí 3D (giờ, hàng, col).

Ba nhóm này chia sẻ cùng một cơ sở tần số RoPE, nhưng phân bổ độ mờ ẩn trên mỗi băng là một tham số được học chứ không phải là một phân chia cố định.

V2PE tuyên bố của ablation: 1-2 điểm trên video benchmarks so với M-RoPE tại cùng một tính toán.

> **【中文解读】**Sự khác biệt giữa V2PE và M-RoPE: độ ẩn được phân chia giữa các đoạn tần số là phân chia có thể học được thay vì phân chia cố định. Mô hình có thể tự động cân nhắc thời gian và tần số không gian trong quá trình đào tạo trước.

### Visual Resolution Router (ViR)  định tuyến phân giải hình ảnh

Tích ứng tối ưu hóa. Không phải tất cả hình ảnh đều cần mã hóa độ phân giải đầy đủ. Một bức ảnh với một đối tượng ở chi tiết thấp lãng phí token khi mã hóa ở 1280px bản địa. ViR là một phân loại nhỏ dự đoán độ phân giải tối thiểu cần thiết để trả lời câu hỏi, trước khi mã hóa.

Các tuyến đường có ba cấp độ: độ phân giải thấp (256 token), trung bình (576), cao (2048+). Đối với 60% truy vấn trong lưu lượng sản xuất, thấp hoặc trung bình là đủ.

> **【中文解读】**ViR là triển khai tối ưu hóa: một phân loại nhỏ có độ phân giải tối thiểu cần thiết trong việc lập trình trước khi dự đoán các truy vấn.

> **【拓展：ViR 与金融场景】**Trong quá trình xử lý tài liệu tài chính, phần lớn các truy vấn như " tổng số tiền phát hành này là bao nhiêu") chỉ cần độ phân giải thấp, nhưng các nhiệm vụ đặc biệt của OCR như "tạo tất cả các dự án") cần độ phân giải cao.

### Việc triển khai ngôn ngữ thị giác (DvD) 解视觉语言部署

Khi bạn phục vụ một VLM lớn, bộ mã hóa thị giác chạy một lần cho mỗi hình ảnh nhưng LLM chạy theo cách tự động cho mỗi token đầu ra. Hai thành phần có những nút thắt khác nhau (viết = băng thông bộ nhớ GPU cho conv + chú ý; LLM = KV cache). DvD chia chúng thành GPU riêng biệt với lưu lượng giữa.

Đối với mô hình mã hóa 8B + 400M, DvD gần gấp đôi dung lượng mỗi nút so với vị trí cùng.

> **【中文解读】**DvD sẽ sử dụng bộ xử lý video và LLM trên các GPU khác nhau, thông qua các kết nối truyền tải truyền thống.

### Chất lượng một giai đoạn so với nhiều giai đoạn.

Đề xuất chuẩn chính của InternVL3: ở 78B Params, phù hợp với MMMU-Pro của Gemini 2.5 Pro. Ở 38B, phù hợp với GPT-4o. Ở 8B, dẫn đầu bảng xếp hạng mở-8B. Tất cả trên một công thức chuẩn bị trước tập luyện + hướng dẫn-đấu hiệu.

Hipoteis nợ phù hợp có thể đo lường: InternVL3-8B mất ít điểm chuẩn văn bản (MMLU, GSM8K) hơn Qwen2.5-VL-7B mỗi đơn vị tăng điểm chuẩn thị giác. Mô hình này là một mô hình tổng quát hơn vì đào tạo là một mảnh, chứ không phải hai.

> **【中文解读】**InternVL3-8B Mỗi nhận được một hình ảnh cơ sở phần tử của tăng, mất văn bản cơ sở phần tử hơn Qwen2.5-VL-7B 少──模型更"全科", bởi vì đào tạo là một bộ, không phải là hai đoạn拼接──

### InternVL3.5 và InternVL-U

InternVL3.5 (Tháng 8 năm 2025) mở rộng công thức. Cách tiếp cận trước đào tạo bản địa tương tự, nhiều dữ liệu hơn, nhiều param hơn.

InternVL-U (2026) thêm sản xuất hình ảnh  thế hệ thống thông qua đầu MMDiT trên cùng một xương sống. "U" là "Giải quan + thế hệ", theo đuổi các mô hình thống nhất kiểu Transfusion (Dạy 12.13).

> **【中文解读】**InternVL-U(2026) đã gia nhập khả năng tạo hình ảnh trên cùng một xương rồng (via MMDiT) để theo đuổi sự hiểu biết về Transfusion 风格+ tạo ra một mô hình.

### Sự thay đổi của việc đào tạo trước sinh viên bản địa

Đào tạo trước bản địa không miễn phí:

- Lưu ý: Phân tích / 计算. Việc đào tạo một VLM mới từ đầu có giá tương tự như đào tạo một văn bản LLM  triệu giờ GPU.
- dữ liệu / 数据. hình ảnh- văn bản có thể được chuyển đổi ở quy mô rất hiếm. OBELICS là 141M tài liệu; MMC4 là 571M. Chỉ văn bản được chuyển đến 15T token.
- Làm việc làm bằng cơ sở bằng cử nhân học (LLM) tái sử dụng / 基础LLM复用. Đào tạo trước bản địa từ bỏ tùy chọn để bỏ vào một LLM mới sau đó.

InternVL3 đặt cược: nợ sắp xếp tệ hơn tổn thất tái sử dụng. Các điểm chuẩn ủng hộ tuyên bố. Chi phí sản xuất ngăn chặn các phòng thí nghiệm tương lai từ sao chép rẻ. VLM sau khi được thực hiện sẽ tiếp tục tồn tại vì chúng vẫn rẻ hơn cho hầu hết các dự án.

> **【中文解读】**InternVL3 注: đối với nợ nần hơn mất tính linh hoạt tái sử dụng tệ hơn.

## Hãy dùng nó để thực hành
```figure
l5-native-pretrain
```

## Sử dụng nó

`code/main.py`là một bộ trộn tập thể và bộ viR.

- Lấy một hỗn hợp mục tiêu (% văn bản, % chia sẻ, % tiêu đề, % video) và tính toán các bước dự kiến theo phương thức.
- Mô phỏng ViR định tuyến trên một loạt các truy vấn (cải phân phối: 50% chi tiết thấp, 30% trung bình, 20% chi tiết cao) và báo cáo số lượng token trung bình.
- Báo cáo ước tính dung lượng DvD cho mã hóa so với LLM FLOPs.
- Bác tạo ra một bản ghi trình độ của các bài học trước khi học tập, tính toán, dữ liệu và các triệu chứng nợ.

## Đưa nó lên mạng

Bài học này sẽ mang lại kết quả `outputs/skill-native-vs-posthoc-auditor.md`. Với kế hoạch đào tạo VLM được đề xuất, nó kiểm toán xem có nên làm việc bản địa hay sau khi làm việc, đánh dấu rủi ro liên kết nợ và đề nghị một hỗn hợp cơ bản.

> **【中文解读】**本课产出"Tổ số đối với 后装审计工具"──给定 VLM 训练计划,评估应走原生还是后装路线,标记对齐债务风险,推语料混合比例──

## Tập luyện bài tập

1. ước tính số lượng điện toán delta giữa InternVL3-8B (đáng tập bản địa) và LLaVA-OneVision-7B (sau hoc).
   | 估算 InternVL3-8B（原生预训练）和 LLaVA-OneVision-7B（后装）的计算量差距。GPU 小时比率大约多少？什么解释了这个差距？

2. InternVL3 báo cáo 40% văn bản / 35% giao lưu / 20% tiêu đề / 5% video. Nếu nhiệm vụ mục tiêu của bạn là video nặng, đề xuất một tỷ lệ mới và tranh luận tại sao mô hình cơ bản vẫn cần dữ liệu văn bản và tiêu đề đáng kể.
   | InternVL3 的语料比例是 40/35/20/5。如果目标任务是视频密集的，提出新比例，论证为什么基础模型仍需要大量文本和描述数据。

3. Đọc MM1.5 Phần 4 về quên lãng. Hãy nêu tên chỉ số chuẩn xác định nơi đào tạo sau hoc đã cho thấy sự lùi lại lớn nhất.
   | 阅读 MM1.5 第 4 节关于遗忘的内容。指出后装训练在哪个基准上退化最大？退化了多少？

4. ViR chuyển 60% lưu lượng truy cập sang mã hóa độ phân giải thấp. Quý vị này chuyển hướng sai hướng (đưa đến độ phân giải thấp khi cần độ phân giải cao) cho các chế độ thất bại router ba.
   | ViR 将 60% 流量路由到低分辨率。哪些查询会被错误路由（需要高分辨率却发了低分辨率）？提出三种路由失败模式。

5. DvD chia thị giác và LLM thành GPU riêng biệt.
   | DvD 将视觉和 LLM 分到不同 GPU。在什么流量模式下 DvD 反而降低吞吐量？

## Từ khóa  Keyword

| Term | What people say | What it actually means | 中文含义 | 中文释义 |
|------|-----------------|------------------------|----------|---------|
| Native multimodal pretraining | "From scratch together" | Text + image + video tokens participate in the loss from step 1, not bolted on later | 从第一步就将文本+图像+视频 token 纳入损失函数 | |
| Alignment debt | "Post-hoc penalty" | Measurable regression in text skills and answer consistency that comes from bolting vision onto a frozen LLM | 后装 VLM 带来的文本技能退化和回答一致性下降 | |
| V2PE | "Variable visual pos encoding" | Per-modality learnable position encoding allocation; InternVL3's M-RoPE successor | 按模态类型可学习的位置编码分配 | |
| ViR | "Resolution router" | Small classifier that picks minimum resolution needed per query before encoding, saving inference tokens | 编码前选择最低所需分辨率的小型分类器 | |
| DvD | "Decoupled deployment" | Vision encoder on one GPU, LLM on another, with stream handoff; doubles throughput for large VLMs | 视觉编码器和 LLM 分 GPU 部署，流式传输连接 | |
| InternVL-U | "Unified understanding + generation" | 2026 follow-up that adds image-generation heads to the native-pretrain backbone | 在原生预训练骨干上加入图像生成头的统一模型 | |
| Interleaved corpus | "OBELICS / MMC4" | Documents with text and images in natural reading order; the raw material for native pretraining | 文本和图像按自然阅读顺序交织的文档语料 | |

## Xem thêm 延伸阅读

- [Chen et al. — InternVL 1 (arXiv:2312.14238)](https://arxiv.org/abs/2312.14238)Ứng viên đầu tiên
- [Zhu et al. — InternVL3 (arXiv:2504.10479)](https://arxiv.org/abs/2504.10479) Ứng viên VL3
- [InternVL3.5 (arXiv:2508.18265)](https://arxiv.org/abs/2508.18265)➡️ InternVL3.5 mở rộng quy mô
- [InternVL-U (arXiv:2603.09877)](https://arxiv.org/abs/2603.09877) Ứng viên VĐV-U hiểu + tạo hợp nhất
- [Zhang et al. — MM1.5 (arXiv:2409.20566)](https://arxiv.org/abs/2409.20566) MM1.5 đối với việc định lượng nợ
