# VLA thể hiện: RT-2, OpenVLA, π0, GR00T 具身 VLA:视觉语言动作模型与机器人控制

> Lần đầu tiên một mô hình đọc một công thức từ một trang web và thực hiện nó trong một robot nhà bếp là RT-2 (Google DeepMind, tháng 7 năm 2023). RT-2 đã phân loại các hành động như các mã thông báo văn bản, đồng thời điều chỉnh một VLM trên dữ liệu web cộng với dữ liệu hành động robot, và chứng minh rằng kiến thức ngôn ngữ thị giác quy mô web chuyển sang kiểm soát robot. OpenVLA (tháng 6 năm 2024) đã gửi tham chiếu mở 7B. Phòng π0 của Cơ thể Trí tuệ (2024-2025) đã thêm các chuyên gia hành động phù hợp với dòng chảy. GR00T N1 (Tổng thống NVIDIA) (Từ tháng 3 năm 2025) cung cấp hệ thống kiểm soát kép (System 1 / System 2) cho robot nhân vật ở quy mô lớn. VLA nguyên thủy  thị giác-lời nói-phản ứng, một mô hình duy nhất nhìn thấy, đọc và hành động  là cầu nối giữa các mô hình hiểu biết của giai đoạn này và các hệ thống tự trị trong giai đoạn 15.

> **【中文解读】**RT-2  lần đầu tiên chứng minh mạng cấp hình ảnh ngôn ngữ kiến thức có thể di chuyển sang kiểm soát máy tính:将关节动作分散化为文本代币,与VLM 联合微调。OpenVLA là nguồn mở 7B 参考,π0 引入流匹配动作专家,GR00T N1 实现双系统(快思考/慢思考) 人形机器人控制──VLA(视觉语言动作) là nối kết đa mô hình hiểu biết và hệ thống tự chủ của桥梁──

> **【拓展：Embodied VLA 到机器人产业】**Mô hình VLA đang chuyển từ phòng thí nghiệm sang ngành công nghiệp: Tesla Optimus, Hình 01  1X Công ty máy tính người khác đang nghiên cứu và phát triển hệ thống điều khiển dựa trên VLA. Trong bối cảnh công nghiệp, VLA có thể được sử dụng cho máy móc lưu trữ vật liệu, máy vận hành dây chuyền, vv.

**Type:** Learn
**Languages:** Python (stdlib, action tokenizer + VLA inference skeleton)
**Prerequisites:** Phase 12 · 05 (LLaVA), Phase 15 (Autonomous Systems, referenced)
**Time:** ~180 minutes

>  **【前置】**Học本节前请先掌握:Phase 12·05(LLaVA VLM 基础) Phase 15·01(Agent 循环) 控制理论基础(关节空间、末端执行器位姿) VLA = VLM 输出从文本变成机器人动作,是Phase 12 到Phase 15(自主系统) 的桥梁──
>  **【类比】**VLA = "đưa cho người máy装脑和眼睛"。传统机器人 = 程序员写死 if-else 规则(看红色就停下);VLA = 像人看图说话做事("把红杯放到桌上"→看杯→规划路径→控制关节执行)。RT-2 把动作分散成代币 = 把动作作为文字写进即时;π0 流匹配 = 输出连续动作而非分散代币,更精确──

## Mục tiêu học tập

- Mô tả mã hóa hành động: mã hóa bin riêng biệt (RT-2), mã hóa hành động hiệu quả FAST, các hành động phù hợp dòng chảy liên tục (π0).
  Trung文翻译:描述动作分词化:离散bin 编码(RT-2) 、FAST 高效动作代币、连续流匹配动作(π0)。
- Giải thích tại sao việc đồng chỉnh trên dữ liệu web + robot bảo vệ việc chuyển giao kiến thức chung cho các nhiệm vụ mới.
  Trung ngữ翻译: giải thích tại sao trong các trang web + cơ quan dữ liệu kết hợp các điều chỉnh nhỏ có thể giữ lại kiến thức chung chuyển đến nhiệm vụ mới khả năng.
- So sánh OpenVLA (cởi mở 7B Llama + VLM), π0 (sự phù hợp dòng chảy) và GR00T N1 (hệ thống kép) trên cùng một nhiệm vụ robot.
  Trung文翻译: 在同一机器人任务上比较 OpenVLA(开放 7B Llama+VLM) 、π0(流匹配) 和 GR00T N1(双系统) ⋅
- Hãy nêu tên bộ dữ liệu Open X-Embodiment và vai trò của nó như là cơ quan đào tạo RT-X.
  Trung文翻译:列举 Open X-Embodiment 数据集及其作为 RT-X 训练语料的角色──

## Vấn đề  vấn đề giới thiệu

Một robot làm việc từ hướng dẫn ngôn ngữ tự nhiên đã là mục tiêu nghiên cứu kể từ những năm 1970. Câu trả lời của những năm 2020: mô hình hoạt động ngôn ngữ thị giác (VLA).

> Sử dụng ngôn ngữ tự nhiên để làm việc trong nhà từ 1970 là mục tiêu nghiên cứu.

Những thách thức đặc biệt đối với VLA:

> Những thách thức đặc biệt của VLA:

1. Không gian hành động là liên tục (thây góc, lực) và có chiều cao (7-DOF cánh tay + 3-DOF nắm giữ = 10 dims ở 30 Hz).
   Trung ngữ翻译:动作空间是连续的(关节角度、力) 且高维(7自由度臂 + 3自由度爪 = 30Hz 下 10维) ⋅
2. Dữ liệu đào tạo cụ thể cho robot hiếm. Open X-Embodiment có ~ 1M quỹ đạo; hình ảnh văn bản web là 5B+.
   Trung ngữ翻译:机器人专用训练数据稀缺──Open X-Embodyment 约100万条轨迹;网页文本图像有50亿+──
3. Điều khiển tần số quan trọng. vòng điều khiển 30 Hz có nghĩa là ngân sách 33ms mỗi hành động.
   Trung ngữ翻译:控制频率 rất quan trọng. 30Hz 控制回路 nghĩa là mỗi động tác 33ms 预算.
4. An toàn: Một hành động sai lầm làm hỏng phần cứng, con người hoặc tài sản.
   Trung ngữ翻译:安全性. 错误的动作会损坏硬件.

## Khái niệm cốt lõi

> **【中文解读】**具身視觉-语言-动作模型(VLA)让机器人理解语言指令和视觉场景后执行物理动作。OpenVLA là nguồn mở VLA, pi0(Tâm trí vật lý) và NVIDIA Groot là mô hình đại diện của具身智能──VLA = 视觉编码器 + LLM + 动作解码器──

> **【拓展：具身智能的进展**OpenVLA-7B trên Google Robot đạt được tỷ lệ thành công nhiệm vụ khoảng 80%  Pi0 sử dụng quy trình phù hợp (flow matching) tạo ra các quỹ đạo hoạt động liên tục, so với các hoạt động phân tán truyền thống dễ dàng hơn. NVIDIA Groot  chuyên về máy tính nhân tạo.


### Đánh dấu hành động (RT-2)

Trù của RT-2: đại diện cho mỗi mục tiêu chung như một token văn bản định lượng. Phân biệt phạm vi bình thường hóa [-1, 1] thành 256 bin, lập bản đồ mỗi bin cho một ID từ vựng. Một hành động 10-DOF trở thành 10 token tại mỗi bước kiểm soát.

> Kỹ thuật của RT-2: 将每个关节目标表示为量化文本代币――将归结的 [-1, 1] 范围离散为 256 个 bin, mỗi bin 映射到一个词汇 ID――10 自由度动作在每个控制步变成10 个 token――

Đồng tinh chỉnh PaLM-X VLM trên một hỗn hợp:

> Trong dữ liệu hỗn hợp trên PaLM-X VLM:

- Cặp hình ảnh-tinh văn web (chữ viết tắt, VQA).
  Trung văn翻译:网页图文对(描述、VQA)。
- Robot biểu tình, hành động như các token.
  Trung ngữ翻译:机器人演示,动作为标志──

Mô hình thấy "tăng khối đỏ" ( ngôn ngữ) → hình ảnh (thìn) → chuỗi hành động 10 token (những mục tiêu liên kết được phân tiết). Web pretraining bảo tồn chuyển giao kiến thức chung: RT-2 có thể theo "lưu ý đối tượng chuyển động nhanh" mặc dù "lưu ý nhanh" không có trong dữ liệu đào tạo.

> 模型看"拿起红色方块" (→ 图像) 视觉) → 10 token 动作序列 (→ 动作序列) 离散关节目标) ⋅ 网页预训练保留通用知识迁移:RT-2 能执行"移向快速移动的物体", ngay cả khi "快速移动" không nằm trong dữ liệu đào tạo。

Nhẫn ở 3-5 Hz trong giấy RT-2, bị giới hạn bởi mã tự rút VLM.

> RT-2 论文中推理速度 3-5 Hz, giới hạn ở VLM 自归解码──

### OpenVLA  tham chiếu mở 7B

OpenVLA (Kim et al., tháng 6 năm 2024) là tương đương RT-2 trọng lượng mở. 7B Llama backbone, DINOv2 + SigLIP mã hóa thị giác kép, mã hóa hành động trên 256 thùng.

> OpenVLA là mở quyền trọng RT-2 等价物品.

Được đào tạo trên Open X-Embodiment (970k quỹ đạo trên 22 robot).

> Trong Open X-Embodiment 上训练(22 个机器人共 97万条轨迹) ・内置 LoRA 微调支持,适应新机器人。

Tự động: 4-5 Hz trên A100 với định lượng, đủ nhanh để thao tác chậm, không phải để điều khiển tần số cao.

> 推理:A100 上量化后 4-5 Hz──对慢速操作足够,不适合高频控制──

### FAST tokenizer  mã hóa hành động nhanh hơn

Pertsch et al. (2024) cho thấy rằng token hóa bin phân biệt là không hiệu quả  hầu hết các tập hợp hành động trong một khu vực nhỏ của bin-space. FAST (Frequency-domain Action Sequence Tokenizer) nén các chuỗi hành động thông qua DCT và định lượng các hệ số.

> Pertsch 等人(2024) cho thấy sự phân tán của bin phân từ hóa hiệu quả thấp Hầu hết các động tác tập hợp trong bin 空间的小区域──FAST(频域动作序列分词器) thông qua DCT 压缩动作序列并量化系数──

Một quỹ đạo hành động 30 bước trở thành ~ 10 token FAST thay vì 300 token bin riêng biệt.

> 30 bước chuyển động quỹ đạo trở thành khoảng 10 token nhanh, thay vì 300 token phân tán.

### π0 và các hành động phù hợp dòng chảy

Phương pháp π0 của Physical Intelligence (Black et al., tháng 10 năm 2024) thay thế các token hành động riêng biệt bằng chuyên gia hành động phù hợp dòng chảy:

> Phương pháp thông minh vật lý của π0 dùng dòng phù hợp động tác

- Một biến đổi hành động nhỏ đọc các trạng thái ẩn của VLM và phát ra một chuỗi hành động liên tục 50 bước thông qua dòng chảy được chỉnh sửa.
  Trung文翻译:小型动作 Transformer 读取 VLM 隐藏状态,通过正流输出连续的50步动作序列──
- Các bộ phận đầu hành động có sự mất mát phù hợp dòng chảy; VLM trước khi tập luyện vẫn không thay đổi.
  Trung文翻译:动作头用流匹配损失训练;VLM 预训练不变──
- Tự phát: chuỗi hành động đầy đủ phát ra trong ~ 5 bước biểu thị, kiểm soát hiệu quả 50 Hz.
  Trung ngữ翻译:推理:完整动作序列在约5步去噪中输出,等效50Hz 控制。

Đề xuất của π0: vượt qua OpenVLA và Octo trong một loạt các nhiệm vụ thao tác.

> π0 声称: trong các nhiệm vụ hoạt động rộng lớn đánh bại OpenVLA và Octo.

> **【中文解读】**π0 sử dụng dòng phù hợp thay thế chuyển động tần số: một động cơ nhỏ Transformer 读取 VLM 隐藏状态, thông qua 正流输出连续的50步动序列──推理时只需约5步去噪声,实现效率等效50Hz 控制频率──连续动作表达保留了离散会破坏的动作平滑性──

π0.5 và π0-FAST là nâng cấp theo từng bước. π0-FAST kết hợp mã hóa FAST với sự phù hợp dòng chảy.

> π0.5 và π0-FAST là tăng trưởng tăng trưởng.

### GR00T N1  Hệ thống kép cho người

NVIDIA's GR00T N1 (March 2025) được chế tạo cho robot nhân vật (> 30 DOF, toàn thân):

> NVIDIA's GR00T N1 为人形机器人设计 ((>30自由度,身材):

- Hệ thống 2: một cảnh đọc VLM lớn + hướng dẫn, tạo ra các mục tiêu dưới cấp cao ở ~ 1 Hz.
  Trung ngữ翻译:系统 2: VLM lớn 读取场景+ chỉ thị,以约 1Hz 生成高层子目标──
- Hệ thống 1: một biến đổi đầu hành động nhỏ tạo ra các lệnh liên kết 50-100 Hz cấp thấp được điều chỉnh trên các mục tiêu phụ.
  Trung文翻译:系统 1:小型动作头 Transformer 根据子目标生成底层 50-100Hz 关节命令。

Các bản đồ chia để suy nghĩ nhanh và chậm của Kahneman: Hệ thống 2 kế hoạch, Hệ thống 1 hoạt động.

> Hệ thống 2 规划, hệ thống 1 执行. 优势:慢速VLM 级规划不会阻快速控制. hệ thống 1 保持小规模以保证低延迟.

GR00T N1.7 (khuyến 2025) cải thiện quy mô dữ liệu. GR00T tinh chỉnh với dữ liệu sim-to-real từ Omniverse.

> GR00T N1.7 ((2025 年末) cải tiến dữ liệu mở rộng.

### Khám X mở

Dữ liệu đào tạo. RT-X ( Tháng 10 năm 2023) đã tập hợp 22 bộ dữ liệu bao gồm 1M quỹ đạo trên 22 robot. Open X-Embodiment là bộ phận mà mọi người sử dụng:

> 训练数据──RT-X(2023 年 10 月) đã tích hợp 22 tập dữ liệu, bao gồm 100 000条轨迹 của 22 cơ quan.

- ALOHA / Bridge V2 / Droid / RT-2 Kitchen / Language Table.
  中文翻译:ALOHA / Bridge V2 / Droid / RT-2 Kitchen / Language Table。
- Mỗi mẫu: (tiếng robot, hình ảnh máy ảnh, hướng dẫn, chuỗi hành động).
  Trung ngữ翻译:每个样本:(机器人状态、摄像头视图、指令、动作序列)
- Hoán vệ sinh đào tạo: thống nhất không gian hành động, bình thường hóa phạm vi khớp, thay đổi kích thước máy ảnh.
  Trung ngữ翻译:训练规范:统一动作空间、归一化关节范围、统一摄像头分辨率──

OpenVLA và π0 đào tạo trên Open X-Embodiment. Khoảng cách miền đối với bất kỳ robot cụ thể nào được đóng bằng cách điều chỉnh tinh tế LoRA trên 100-1000 bài tập cụ thể.

> OpenVLA và π0 trong Open X-Embodiment trên đào tạo.

### Đồng-định-thượng-được so sánh với robot-chỉ

Việc điều chỉnh đồng bộ trộn dữ liệu VQA web với quỹ đạo robot. Tỷ lệ quan trọng: quá nhiều VQA và mô hình quên hành động; quá nhiều dữ liệu robot và mô hình mất kiến thức chung.

> 联合微调将网页 VQA 数据与机器人轨迹混合──比例 rất quan trọng: VQA 太多模型忘记动作;机器人数据太多模型失去通用知识──

Tỷ lệ RT-2: ~1:1. OpenVLA: ~0.5:1 web-to-robot. π0: tương tự. Tỷ lệ chính xác là một siêu tham số để điều chỉnh theo kích thước tập dữ liệu.

> RT-2 tỷ lệ khoảng 1:1──OpenVLA 约 0.5:1──π0 类似──精确比例是按数据集大小调节的超参数──

Việc đào tạo chỉ bằng robot tạo ra các mô hình cụ thể về nhiệm vụ không thể thực hiện theo hướng dẫn không phân phối. Co-fine-tuning là sự khác biệt giữa "tôi lấy khối đỏ (trong demo) " và "tôi lấy đối tượng lớn thứ ba từ trái (những cụm từ mới). "

> Chỉ cần luyện tập máy tính để tạo ra mô hình nhiệm vụ cụ thể, thất bại trên lệnh phân phối ngoài.

### Các giới hạn an toàn và hoạt động

Mỗi tàu VLA sản xuất có:

> Mỗi loại VLA sản xuất được trang bị:

- Giới hạn khớp cứng (không thể mô-men xoắn vượt qua thông số kỹ thuật).
  Trung文翻译:硬性关节限制(不能超过规格的力矩)
- Giới hạn tốc độ (clip mềm).
  Trung文翻译:速度限制 (tự hạn tốc độ)
- Các giới hạn không gian làm việc (tài liệu cuối không thể rời khỏi bàn).
  Trung文翻译:工作空间边界(末端执行器不能离开桌面)。
- Kiểm duyệt người trong vòng cho các nhiệm vụ mới.
  Trung ngữ翻译:新任务的人工审批──

Những thứ này nằm bên ngoài VLA như kiểm tra lớp kiểm soát.

> Những điều này nằm bên ngoài kiểm tra VLA.

## Hãy sử dụng nó để thực hiện
```figure
mm-action-tokens
```

## Sử dụng nó

`code/main.py`- Có thể là:

- Thực hiện token hóa và de-tokenization hành động 256 bin.
  Trung ngữ翻译:实现 256 bin 动作分词化和反分词化。
- Dấu họa một token hóa FAST dựa trên DCT + định lượng.
  Trung ngữ翻译:基于DCT + 量化勾勒 FAST 分词器──
- So sánh số lượng token cho mỗi bước hành động qua (discrete-bin, FAST, continuous-flow).
  Trung文翻译:Bài tráng lệ, nhanh chóng, liên tục chảy
- Bác bản tổng kết dòng dõi của RT-2 → OpenVLA → π0 → GR00T.
  Trung文翻译:打印 RT-2 → OpenVLA → π0 → GR00T 的谱系摘要──

## Chuyển nó đi.

Bài học này sẽ mang lại kết quả `outputs/skill-vla-action-format-picker.md`. Với một nhiệm vụ robot (chống chế, điều hướng, toàn bộ cơ thể nhân vật), chọn giữa phân khúc-bin + RT-2, FAST + OpenVLA, phù hợp dòng chảy + π0, hoặc hệ thống kép + GR00T.

> 本课产 出 `outputs/skill-vla-action-format-picker.md`△给定机器人任务(操作、导航、人形全身), 在离散bin+RT-2、FAST+OpenVLA、流匹配+π0 或双系统+GR00T 之间选择──

## Tập luyện bài tập

1. Một cánh tay 10 DOF với tốc độ điều khiển 30 Hz. Địa chỉ của các bin riêng biệt tại 256 thùng phát ra bao nhiêu token mỗi giây?

2. FAST token hóa nén các quỹ đạo 30 bước lên ~ 10 token. Người dùng mất gì nếu quỹ đạo có chuyển động tần số cao (ví dụ, trống)? FAST sẽ 30 bước轨迹压缩 thành khoảng 10 token.

3. Chuỗi phù hợp với dòng chảy của π0 bị phân hủy trong ~ 5 bước. So sánh dung lượng với mã hóa tự rút của OpenVLA ở 4-5 Hz.

4. Hệ thống 1 / Hệ thống 2 của GR00T chia các bản đồ cho Kahneman. đề xuất một phân chia khác (System 3?) có thể giúp đi bộ đôi chân. GR00T's hệ thống1/ hệ thống2 chia rẽ đối với hệ thống卡尼曼理论── đề xuất một giải pháp chia rẽ khác nhau( hệ thống3?) để giúp hai chân đi đi──

5. Đọc Open X-Embodiment Phần 4 về bảo quản tập hợp dữ liệu. Hãy nêu tên ba quy tắc bảo quản ngăn chặn rò rỉ tên miền.

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|------------------------|---------|
| VLA | "Vision-language-action" 视觉-语言-动作模型 | Model that takes image + instruction and outputs action commands 接受图像+指令并输出动作命令的模型 | |
| Action tokenization | "Discrete bins" 离散 bin 编码 | Quantize continuous joint targets into 256 bins per dim, each a vocab ID 将连续关节目标量化为每维 256 个 bin，每个 bin 对应一个词表 ID | |
| FAST tokenizer | "Frequency action tokens" 频域动作 token | DCT + quantize to compress 30-step trajectories to ~10 tokens 用 DCT + 量化将 30 步轨迹压缩为约 10 个 token | |
| Co-fine-tune | "Mix web + robot" 混合微调 | Train on web VQA data alongside robot demos to preserve general knowledge 在网络 VQA 数据和机器人演示上联合训练以保留通用知识 | |
| Flow-matching action head | "pi0 continuous output" 流匹配动作头 | Small transformer that outputs a 50-step action sequence via rectified flow 通过矫正流输出 50 步连续动作序列的小型 Transformer | |
| System 1 / System 2 | "Dual-system control" 双系统控制 | Large VLM plans slowly, small action head acts quickly; GR00T pattern 大 VLM 慢规划，小动作头快执行；GR00T 模式 | |
| Open X-Embodiment | "RT-X dataset" 开放具身数据集 | 1M-trajectory cross-robot dataset; the training corpus 100 万轨迹跨机器人数据集；标准训练语料 | |

## Xem thêm 延伸阅读

- [Brohan et al. — RT-2 (arXiv:2307.15818)](https://arxiv.org/abs/2307.15818)
- [Kim et al. — OpenVLA (arXiv:2406.09246)](https://arxiv.org/abs/2406.09246)
- [Black et al. — π0 (arXiv:2410.24164)](https://arxiv.org/abs/2410.24164)
- [NVIDIA — GR00T N1 (arXiv:2503.14734)](https://arxiv.org/abs/2503.14734)
- [Open X-Embodiment Collab — RT-X (arXiv:2310.08864)](https://arxiv.org/abs/2310.08864)
