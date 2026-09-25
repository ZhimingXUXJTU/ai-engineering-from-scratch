# LLaVA và hướng dẫn thị giác điều chỉnh .

> LLaVA (ngày tháng 4 năm 2023) là kiến trúc đa phương thức được sao chép nhiều nhất trên hành tinh. Nó thay thế BLIP-2's Q-Former bằng một MLP 2 lớp, thay thế sự chú ý chéo của Flamingo bằng sự kết nối mã thông báo ngây thơ, và được đào tạo trên 158k lượt hướng dẫn thị giác được tạo bởi GPT-4 từ các tiêu đề chỉ văn bản. Bất kỳ học viên nào xây dựng một VLM giữa năm 2023 và 2026 đã xây dựng một số biến thể của LLaVA. LLaVA-1.5 đã thêm AnyRes. LVA-Next tăng độ phân giải. LLaVA-OneVision hình ảnh thống nhất, nhiều hình ảnh và video trong một công thức. Bài học này đọc công thức, thực hiện máy chiếu và giải thích tại sao "simple hơn thắng".

> **【中文解读】**LLaVA là cấu trúc đa mô hình được sao chép nhiều nhất trong năm 2023-2026[6]. Ý tưởng cốt lõi của nó rất đơn giản: sử dụng 2 tầng MLP để đưa ra đầu ra của bộ lập trình hình ảnh vào không gian nhúng của mô hình ngôn ngữ, sau đó sẽ đưa ra các mã thông báo hình ảnh trực tiếp nối vào chuỗi văn bản. LLaVA chứng minh "lời cấu trúc đơn giản + dữ liệu chất lượng cao" đủ để vượt quá các thiết kế phức tạp.

> **【拓展：多模态大模型的起源】**Trước LLaVA, mô hình đa hình thức chủ yếu phụ thuộc vào cơ chế chú ý đa hình thức phức tạp như Flamingo's门控交叉注意力, BLIP-2's Q-Former)  Thành công của LLaVA đánh dấu nghiên cứu đa hình thức từ "định dạng kết nối đa hình thức tốt hơn" chuyển sang "đối diện đơn giản hơn + 更多数据"  Phương pháp này ảnh hưởng trực tiếp đến tất cả các VLM chính tiếp tiếp (InternVL, Qwen-VL, Phi-Vision, v.v.)

**Type:** Build  | **类型：构建**
**Languages:** Python (stdlib, projector + instruction-template builder)  | **语言：Python（标准库，投影器 + 指令模板构建器）**
**Prerequisites:** Phase 12 · 02 (CLIP), Phase 11 (LLM Engineering — instruction tuning)  | **前置：阶段12第02课（CLIP）、阶段11（LLM工程——指令微调）**
**Time:** ~180 minutes  | **时长：约180分钟**

>  **【前置】**Học本节前请先掌握:Phase 12·02(CLIP 视觉编码器);Phase 12·03(BLIP-2 桥接,对照学习);Phase 11·08(Instruction Tuning 指令微调)。LLaVA 是BLIP-2 的反面刻意简化桥接,靠数据取胜──
>  **【类比】**LLaVA = "把图片直接打印出来贴在文档里"――BLIP-2 Q-Former = "把 256页书压成 32页摘要再交给LLM";LLaVA MLP = "576页原文整本贴给LLM"――前者省纸张但丢信息,后者费纸张但LLM 看得到全部细节LLM 上下文变长后",费纸"不再是问题,LLaVA自然就赢了――

## Mục tiêu học tập

- Xây dựng một máy chiếu MLP 2 tầng mà lập bản đồ ViT patch embedments (dim 1024) để LLM embedment dim (dim 4096).
- Đi theo công thức LLaVA hai giai đoạn: (1) sắp xếp máy chiếu trên 558k cặp tiêu đề, (2) điều chỉnh hướng dẫn trực quan trên 158k GPT-4-được tạo ra lượt.
- Xây dựng một biểu tượng biểu tượng LLaVA theo định dạng LLaVA với vị trí biểu tượng hình ảnh, biểu tượng hệ thống, và người dùng / trợ lý quay.
- Giải thích tại sao cộng đồng chuyển từ Q-Former sang MLP mặc dù Q-Former đã giành chiến thắng trong ngân sách token.

## Vấn đề  vấn đề nền

BLIP-2's Q-Former (Dạy 12.03) nén một hình ảnh thành 32 token. sạch, hiệu quả, tốt cho các điểm chuẩn. Nhưng nó có hai vấn đề.

Đầu tiên, Q-Former có thể được đào tạo nhưng mất nó không phải là nhiệm vụ cuối cùng. Giai đoạn 1 đào tạo ITC + ITM + ITG. Giai đoạn 2 đào tạo mất LM. Các truy vấn học được một số đại diện trung gian mà LLM sau đó phải giải mã. Thông tin bị mất trong nút thắt.

Thứ hai, Q-Former có 188 triệu param, và ở thang LLaVA năm 2023, bạn phải cùng thiết kế với LLM mục tiêu của mình. Thay đổi LLM, đào tạo lại Q-Former. Thay đổi bộ mã hóa tầm nhìn, đào tạo lại. Mỗi sự kết hợp là một dự án R&D riêng biệt.

> **【中文解读】**BLIP-2 của Q-Former sẽ hình ảnh nén thành 32 token, trông hiệu quả cao, nhưng có hai vấn đề cốt lõi: 1)  tập luyện mục tiêu không phù hợp giai đoạn đầu tiên sử dụng ITC/ITM/ITG 损失, giai đoạn hai sử dụng ngôn ngữ xây dựng 损失, thông tin bị mất trong chai; 2) 参数 lớn 188M) và với LLM cụ thể 合, thay đổi LLM cần phải tái tập.

Câu trả lời của LLaVA là đáng xấu hổ vì đơn giản: lấy 576 mã đệm của ViT, mỗi lần thông qua một MLP 2 lớp (`1024 → 4096 → 4096`Không có nút thắt, không có giai đoạn 1 dự tập về các mục tiêu kỳ lạ, chỉ cần huấn luyện MLP về một mất LM trực tiếp.

> **【中文解读】**LLaVA's scheme simple to embarrassing: trực tiếp đưa 576 token bổ sung của ViT qua một MLP 2 tầng`1024 → 4096 → 4096`), sau đó tất cả đều bị bỏ vào chuỗi nhập của LLM. Không có chai, không có mục tiêu đào tạo kỳ lạ, chỉ sử dụng ngôn ngữ xây dựng.

> ️ **【易错点】**Vị trí đầu tiên: Vị trí đầu tiên: Vị trí đầu tiên: Vị trí đầu tiên: Vị trí đầu tiên: Vị trí đầu tiên: Vị trí đầu tiên: Vị trí đầu tiên: Vị trí đầu tiên: Vị trí đầu tiên: Vị trí đầu tiên: Vị trí đầu tiên: Vị trí đầu tiên: Vị trí đầu tiên: Vị trí đầu tiên: Vị trí đầu tiên: Vị trí đầu tiên: Vị trí đầu tiên: Vị trí đầu tiên: Vị trí đầu tiên: Vị trí đầu tiên: Vị trí đầu tiên: Vị trí đầu tiên: Vị trí đầu tiên: Vị trí đầu tiên: Vị trí đầu tiên: Vị trí đầu tiên: Vị trí đầu tiên: Vị trí đầu tiên: Vị trí đầu tiên: Vị trí đầu tiên: Vị trí đầu tiên: Vị trí đầu tiên: Vị trí đầu tiên: Vị trí đầu tiên: Vị trí đầu tiên: Vị trí đầu tiên: Vị trí đầu tiên: Vị trí đầu tiên: Vị trí đầu tiên: Vị trí đầu tiên: Vị trí đầu tiên: Vị trí đầu tiên: Vị trí đầu tiên: Vị trí đầu tiên: Vị trí đầu tiên: Vị trí đầu tiên: Vị trí đầu tiên: Vị trí đầu tiên: Vị trí đầu tiên: Vị trí đầu tiên: Vị trí đầu tiên: Vị trí đầu tiên: Vị trí đầu tiên: Vị trí trí đầu tiên: Vị trí trí đầu tiên: Vị trí trí trí đầu tiên: Vị trí trí: Vị trí trí trí: Vị trí trí trí trí: Vị trí: Vị trí: Vị trí: Vị trí: Vị trí: Vị trí: Vị trí: Vị trí: Vị trí: Vị trí: Vị trí: Vị trí: Vị trí: Vị trí: Vị trí: Vị trí: Vị trí: Vị trí: Vị trí: Vị trí: Vị trí: Vị trí: Vị trí: Vị trí: Vị trí: Vị trí: Vị trí: Vị trí: Vị trí: Vị trí: Vị trí: Vị trí: Vị trí: Vị trí: Vị trí: Vị trí: Vị

Dữ liệu này xuất phát từ đâu? Nhìn sâu thứ hai của LLaVA: sử dụng GPT-4 (chỉ văn bản) để tạo dữ liệu hướng dẫn. Đưa GPT-4 tiêu đề COCO và dữ liệu hộp biên giới cho một hình ảnh, yêu cầu nó tạo ra các cuộc trò chuyện, mô tả và câu hỏi lý luận phức tạp. 158k hướng dẫn-đáp ứng quay miễn phí. Không có ghi chú của con người.

> **【中文解读】**LLaVA có một cách sáng tạo thứ hai: sử dụng GPT-4 (đơn văn bản mô hình) để tạo ra dữ liệu chỉ thị.

Kết quả: một VLM chạy trên 8 chiếc A100 trong một ngày, đánh bại Flamingo trên MMMU, và gửi một điểm kiểm soát mở mà cộng đồng có thể mở rộng. Đến cuối năm 2023, nó đã sinh ra hơn 50 chiếc gao.

> **【拓展：LLaVA 的产业影响】**LLaVA chứng minh rằng VLM không cần tính năng lớn. 8 张 A100  chạy một ngày đã đủ. Điều này đã làm giảm đáng kể các cửa của nghiên cứu đa mô hình, thúc đẩy sự bùng nổ của môi trường VLM mở nguồn. Trong bối cảnh tài chính, cấu trúc LLaVA được sử dụng để hiểu các biểu đồ tài chính, hình ảnh phiếu, v.v., là thành phần cơ bản của đường ống hiểu tài liệu.

## Khái niệm cốt lõi

> **【中文解读】**LLaVA sẽ kết nối CLIP  video codec và LLM  thông qua video instruction, tạo ra các mô hình khác nhau, sử dụng dữ liệu của GPT-4 để chuyển hóa mô hình thành câu hỏi.

> **【拓展：LLaVA 的开源生态】**LLaVA là mô hình đa mô hình mở thành công nhất. LLaVA-NeXT hỗ trợ đầu vào phân giải tùy chọn, LLaVA-OneVision 统一图像和视频理解.


### Kiến trúc, kiến trúc.

LLaVA-1.5 ở 13B:  LLaVA-1.5 13B 参数版本:
- Bộ mã hóa thị giác / 视觉编码器: CLIP ViT-L/14 @ 336 (đóng trong giai đoạn 1, tùy chọn không đóng băng giai đoạn 2 / 第一阶段结,第二阶段可选解).
- Động cơ chiếu sáng / 投影器: 2 lớp MLP với kích hoạt GELU / 2层MLP + GELU激活, `1024 → 4096 → 4096`- Tôi không biết.
- LLM / 语言模型: Vicuna-13B (sau này là Llama-3.1-8B / 后续使用 Llama-3.1-8B).

Chuyển tiếp hình ảnh + văn bản nhanh chóng: 图像+文本提示的前向传播:

```
img -> ViT -> 576 patches of dim 1024           # 图像 -> ViT -> 576个维度1024的补丁
patches -> MLP -> 576 tokens of dim 4096         # 补丁 -> MLP -> 576个维度4096的token
prompt: system + "<image>" placeholder + user question  # 提示词：系统提示 + <image>占位符 + 用户问题
replace <image> token with the 576 projected tokens      # 用576个投影token替换<image>
feed the full sequence to the LLM                       # 将完整序列送入LLM
decode response                                         # 解码响应
```

Hình ảnh chiếm 576 token của ngữ cảnh LLM. Ở ngữ cảnh 2048, nó để lại 1472 token cho văn bản. Ở ngữ cảnh 32k, đó là một lỗi tròn.

> **【中文解读】**Một张图像占用LLM 上下文的 576 token. Trong 2048 上下文窗口, nó chiếm 28%, chỉ còn lại 1472 token 给文本; nhưng trong 32k 上下文, nó gần như có thể bỏ qua không đếm. Đó là lý do tại sao theo thời gian LLM 上下文窗口 tăng trưởng, chiến lược "violent拼接" của LAVA ngày càng có thể thực hiện.

### Giai đoạn 1: Định hướng máy chiếu.

Freeze ViT. Freeze LLM. Train chỉ 2 lớp MLP. Dataset: 558k image-caption pairs (LAION-CC-SBU). Loss: ngôn ngữ mô hình hóa trên tiêu đề, điều kiện trên các token hình ảnh dự đoán.

Trong một thời đại duy nhất với lô 128 điều này được thực hiện trong vài giờ. máy chiếu học cách lập bản đồ không gian ViT đến không gian LLM. Không giám sát cụ thể về nhiệm vụ.

> **【中文解读】**Đầu tiên, học tập tập 2 tầng MLP, sử dụng 558k hình ảnh đối với, để xây dựng ngôn ngữ mất mát đào tạo.

### Giai đoạn 2: Định hướng thị giác điều chỉnh

Tháo đông máy chiếu (vẫn có thể đào tạo). Tháo đông LLM (thường là hoàn toàn, đôi khi là LoRA).

Dữ liệu hướng dẫn là thủ thuật. Liu et al. đã tạo ra nó bằng:
1. Hãy chụp ảnh COCO.
2. Tạo ra mô tả văn bản (5 phụ đề con người + danh sách hộp giới hạn).
3. GPT-4 với 3 mẫu đơn giản:
   - Cuộc trò chuyện / 对话: "Tạo ra một cuộc đối thoại trở lại giữa người dùng và trợ lý về hình ảnh này".
   - Mô tả chi tiết / 详细描述: "Đưa một mô tả chi tiết phong phú về hình ảnh".
   - Lý luận phức tạp: "Hãy hỏi một câu hỏi đòi hỏi phải có lý luận về hình ảnh, sau đó trả lời nó".
4. Phân tích đầu ra của GPT-4 thành (số lệnh, phản ứng) cặp.

Không có gì trong những điều này chạm trực tiếp vào hình ảnh  chỉ mô tả văn bản. GPT-4 ảo giác nội dung hình ảnh hợp lý. Một số tiếng ồn, nhưng nó đã hoạt động: 158k quay là đủ để mở khóa đối thoại.

> **【中文解读】**关键创新: dữ liệu tạo hoàn toàn không liên hệ với hình ảnh tự nó chỉ sử dụng mô tả văn bản. GPT-4 sẽ "phản hiện" ra nội dung hình ảnh hợp lý, mặc dù sẽ có tiếng ồn, nhưng 158k 条 dữ liệu đủ để giải quyết khả năng đối thoại.

> 🤔 **【困惑】**Q: GPT-4 没看图只看描述,那 LLaVA 训练时实际学学的"视觉"是什么?A: LLaVA 学习是两件事: 1) 投影机把 ViT 的视觉特征翻译成 LLM 能理解的语义; 2) LLM 学会"看图片 → 生成符合GPT-4风格的描述"――GPT-4 的"幻觉"实际上是合理的描述(基于标题),所以最终 LLaVA 也能产生合理的描述――
> ️ **【易错点】**Bản thân tập LLaVA 时数据不清洗 → GPT-4 của ảo giác ô nhiễm tập hợp tập tập,模型可能描述图中没有的东西──修复:用 GPT-4V(多模态版本) thay thế văn bản thuần túy GPT-4,让 GPT-4V 真的看图生成描述(ShareGPT4V就是这个思路),质量更高──

> **【拓展：数据合成的范式意义】**LLaVA đã sử dụng phương pháp tổng hợp dữ liệu này. Trong lĩnh vực trực tiếp như hình ảnh y tế, hình ảnh tài chính, cũng có thể sử dụng dữ liệu chỉ thị cụ thể trong lĩnh vực sản xuất dữ liệu GPT-4V để điều chỉnh VLM.

### Tại sao cộng đồng lại sao chép lại điều này? Tại sao cộng đồng lại làm theo?

- Không có lỗ cụ thể giai đoạn 1 để điều chỉnh. LM mất trong suốt.
- Bộ chiếu sẽ được huấn luyện trong vài giờ, không phải vài ngày.
- LLM có thể được đổi (LLaVA-Llama2, LLaVA-Mistral, LLaVA-Llama3) bằng cách tái đào tạo chỉ với máy chiếu.
- Dòng ống dữ liệu hướng dẫn thị giác sử dụng GPT-4 và rẻ để tái tạo cho một miền mới.

### LLaVA-1.5 và LLaVA-Next

LLaVA-1.5 (Ôktober 2023) thêm:  LLaVA-1.5 ((2023年10月) 新增:
- Dữ liệu nhiệm vụ học thuật (VQA, OKVQA, RefCOCO) trộn vào điều chỉnh hướng dẫn.
- Hệ thống tốt hơn.
- 2048 → 32k ngữ cảnh.

LLaVA-NeXT (từ tháng 1 năm 2024) thêm: ➡ LLaVA-NeXT(2024年1月) 新增:
- AnyRes: chia hình ảnh độ phân giải cao thành lưới 2x2 hoặc 1x3 của 336x336 cây trồng, cộng với một bản thu nhỏ độ phân giải thấp toàn cầu. Mỗi cây trồng trở thành 576 token; tổng cộng khoảng 2880 token hình ảnh mỗi hình ảnh. OCR và các nhiệm vụ biểu đồ đã nhảy vọt.
- Kết hợp dữ liệu chỉ dẫn tốt hơn với ShareGPT4V (chủ đề chất lượng cao GPT-4V).
- Các cơ sở LLM mạnh hơn (Mistral-7B, Yi-34B).

> **【拓展：AnyRes 与高分辨率理解】**AnyRes là một công nghệ quan trọng của LLaVA để xử lý hình ảnh phân giải cao. Đối với các hình ảnh tài liệu trong trường hợp tài chính, phân giải cao là rất quan trọng để hiểu.

### LLaVA-OneVision

Bài học 12.08 bao gồm OneVision sâu sắc. Phiên bản ngắn: cùng một máy chiếu, nhưng được đào tạo với chương trình giảng dạy bao gồm hình ảnh đơn, nhiều hình ảnh và video trong một mô hình với ngân sách biểu tượng trực quan được chia sẻ.

> **【中文解读】**Chương 12.08 课将深入讲解 OneVision──简言之: sử dụng cùng một máy chiếu, nhưng thông qua khóa học học bao gồm một hình ảnh, nhiều hình ảnh và video ba nhiệm vụ, chia sẻ hình ảnh token trong một mô hình 预算──

### So sánh với Q-Former với Q-Former

| | Q-Former (BLIP-2) | MLP (LLaVA) |
|---|---|---|
| Visual tokens per image / 每张图视觉token数 | 32 | 576 (base/基础) or 2880 (AnyRes) |
| Trainable params / 可训练参数 | 188M + LM | 40M + LM |
| Stage 1 loss / 第一阶段损失 | ITC+ITM+ITG | LM only / 仅语言建模 |
| LLM drop-in / LLM替换 | Requires retrain / 需重新训练 | Swap with minimal retrain / 几乎无需重训 |
| Multi-image / 多图像 | Awkward / 不自然 | Natural (concat) / 自然拼接 |
| Video / 视频 | Awkward / 不自然 | Natural (per-frame concat) / 逐帧拼接 |
| Token budget / Token预算 | Small / 小 | Large / 大 |

MLP thắng về sự đơn giản và tính linh hoạt của token. Q-Former thắng về ngân sách token. Đến cuối năm 2023, ngân sách token không còn là ràng buộc (các bối cảnh LLM tăng lên 32k-128k+) và sự đơn giản thống trị.

> **【中文解读】**MLP trong đơn giản và token 灵活性上胜出,Q-Former trong token 预算上胜出. Nhưng đến cuối năm 2023, với LLM trên sau cửa sổ tăng lên 32k-128k+, token 预算 không còn là một chai, đơn giản trở thành yếu tố quyết định.

> 🤔 **【困惑】**Học完本节还会问:1) Tại sao không có LLaVA 上加 Q-Former?加加复杂度变高、训练难度大、收益小( trừ khi ví频 token như vậy 预算紧张场景) ⋅2) LLaVA-1.5 和 LLaVA-NeXT 该选哪个? 默认 LLaVA-NeXT(支持高分辨率 AnyRes,OCR 和文档任务更强) ⋅

### Phương thức nhanh chóng 提示词格式

```
A chat between a curious human and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the human's questions. USER: <image> Describe this image in detail. ASSISTANT: The image shows ...
```

`<image>`là một token giữ chỗ. Trước khi token hóa, nó được thay thế bằng 576 token thị giác (hoặc 2880 với AnyRes). Tokenizer nhìn thấy một chuỗi dài hơn một chút so với nó được đào tạo, nhưng LLM xử lý đầu vào mới vì giai đoạn 1 đã dạy nó.

> **【中文解读】** `<image>`là mã thông báo, trước khi được chuyển vào token  sẽ được thay thế thành 576 个 (hoặc 2880 个) mã thông báo hình ảnh dưới mô hình AnyRes ⋅ LLM 之所以能处理这些从未见过的输入, chính vì giai đoạn đầu tiên đào tạo dạy nó hiểu các biểu tượng hình ảnh sau khi chiếu.

### Tỷ lệ kinh tế tham số

LLaVA-1.5-7B phân hủy:  LLaVA-1.5-7B 参数 phân giải:
- CLIP ViT-L/14 @ 336: 303M (phase đông lạnh 1, thường không đông lạnh giai đoạn 2 / 第一阶段结,第二阶段通常解).
- Động cơ chiếu (2x tuyến tính) / 投影器: ~ 22M có thể đào tạo / 可训练.
- Llama-7B: 7B.
- Tổng / 总计: 7.3B Params. Có thể được đào tạo trong giai đoạn 2 / 第二阶段可训练: đầy đủ 7B + 22M máy chiếu / 全部7B + 22M投影器.

Chi phí đào tạo cho giai đoạn 2: ~ 20 giờ trên 8xA100. Đây là số khóa  một ngày, một nút, có thể tái tạo. Đó là lý do tại sao LLaVA lan rộng.

> **【中文解读】**Cần suất tập luyện giai đoạn thứ hai: 8 张 A100  chạy khoảng 20 小时── đây là con số quan trọng một ngày── một máy  可复现── đây là lý do tại sao LLaVA có thể lây lan nhanh chóng──
```figure
mm-llava-projector
```

## Sử dụng nó

## Hãy dùng nó để thực hành

`code/main.py`Các thiết bị:`code/main.py`实现:

1. Bộ chiếu MLP 2 tầng (dim 16 → 32 → 32 cho quy mô đồ chơi) trong Python tinh khiết.
2. Các đường ống xây dựng nhanh chóng: hệ thống nhanh chóng + `<image>`thay thế bằng N dự báo token + user turn + trợ lý thế hệ vị trí.`<image>`替换为N个投影代币 + 用户轮次 + 助手生成占位符。
3. Một trình hiển thị cho khối hình ảnh 576 token trông như thế nào trong bối cảnh LLM (phân trăm 2k / 32k / 128k bối cảnh tiêu thụ).

## Đưa nó lên mạng

Bài học này sẽ mang lại kết quả `outputs/skill-llava-vibes-eval.md`. Với một điểm kiểm soát gia đình LLaVA, nó chạy một bộ vibes-eval 10 lần (3 captioning, 3 VQA, 2 lý luận, 2 từ chối) và báo cáo một thẻ điểm số có thể đọc được bởi con người. Không phải một điểm chuẩn; một thử nghiệm khói để xác nhận máy chiếu và LLM kết nối tốt.

> **【中文解读】**本课产 出 `outputs/skill-llava-vibes-eval.md` Đặt một điểm kiểm tra của LLaVA 系列, chạy 10 个提示 "vibes-ev" 测试套件 ((3 mô tả, 3 VQA, 2 lý luận, 2 từ chối), tạo ra một kết quả có thể đọc được nhân tạo  Đây không phải là một bài kiểm tra cơ bản chính thức, mà là một bài kiểm tra khói, để xác nhận máy chiếu và LLM  kết nối tốt 

## Tập luyện bài tập

1. Xét số các tham số có thể được đào tạo cho máy chiếu MLP 2 lớp tại `1024 → 4096 → 4096`Với GELU và bias, nó đại diện cho phần nào của LLaVA-13B?
   | 计算维度为 `1024 → 4096 → 4096` 的 2 层 MLP 投影器的可训练参数量。含 GELU 和 bias，它占 LLaVA-13B 的多少比例？

2. Xây dựng một lời nhắc LLaVA cho một trường hợp "đưa" hình ảnh chứa một cá nhân. Viết phản ứng trợ lý dự kiến. Tại sao LLaVA nên từ chối cú bắn không và dữ liệu đào tạo nào sẽ cần thiết để củng cố sự từ chối?
   | 为"拒绝"场景构建 LLaVA 提示词——图像包含私人个体。写出期望的助手回复。为什么 LLaVA 应该零样本拒绝？需要什么训练数据来强化拒绝行为？

3. Đọc phần AnyRes của blog LLaVA-NeXT. Xét số lượng mã thông báo trực quan cho một hình ảnh 1344x672 tại AnyRes. So sánh với 576 mã thông báo cơ sở tại 336x336.
   | 阅读 LLaVA-NeXT 博客的 AnyRes 部分。计算 1344x672 图像在 AnyRes 下的视觉 token 数量，并与 336x336 基础设置的 576 个 token 比较。

4. Máy chiếu LLaVA giai đoạn 1 được đào tạo với mất LM trên tiêu đề. Điều gì sẽ xảy ra nếu bạn bỏ qua giai đoạn 1 và đi thẳng đến giai đoạn 2 (chính giác hướng dẫn điều chỉnh)?
   | LLaVA 第一阶段投影器用描述文本的语言建模损失训练。如果跳过第一阶段直接进入第二阶段会怎样？引用 Prismatic VLMs 消融实验（arXiv:2402.07865）回答。

5. LLaVA-Instruct-150k sử dụng GPT-4 với phụ đề COCO để tạo ra hướng dẫn. Đối với một lĩnh vực mới (những tia X y tế, hình ảnh vệ tinh), mô tả đường ống dữ liệu bốn bước để tạo ra hướng dẫn lĩnh vực.
   | LLaVA-Instruct-150k 用 GPT-4 从 COCO 描述生成指令。对于新领域（医疗X光、卫星图像），描述生成领域指令的四步数据管线。每步可能出什么问题？

## Từ khóa  Keyword

| Term | What people say | What it actually means | 中文含义 | 中文释义 |
|------|----------------|------------------------|----------|---------|
| Projector | "MLP bridge" | 2-layer MLP with GELU mapping ViT dim to LLM dim | 投影器：将ViT维度映射到LLM维度的2层MLP | |
| Image token | "<image> placeholder" | Prompt marker replaced by N projected visual tokens before inference | 图像token：推理前被替换为N个投影视觉token的提示标记 | |
| Visual instruction tuning | "LLaVA stage 2" | Training on GPT-4-generated (image, instruction, response) triplets | 视觉指令微调：在GPT-4生成的（图像,指令,回复）三元组上训练 | |
| Stage 1 alignment | "Projector pretraining" | Freeze ViT and LLM, train projector with LM loss on captions | 第一阶段对齐：冻结ViT和LLM，用描述文本的LM损失训练投影器 | |
| AnyRes | "Multi-crop tiling" | Split high-res image into a tile grid and concatenate each tile's visual tokens | AnyRes：将高分辨率图像切分为网格，拼接各切片的视觉token | |
| LLaVA-Instruct | "GPT-4-generated" | 158k instruction-response pairs synthesized from COCO captions + GPT-4 | LLaVA指令数据：用COCO描述+GPT-4合成的158k指令-回复对 | |
| Vision encoder freeze | "Backbone locked" | CLIP weights do not update in stage 1, sometimes not in stage 2 either | 视觉编码器冻结：CLIP权重在阶段1不更新，有时在阶段2也不更新 | |
| ShareGPT4V | "Better captions" | 1M dense captions generated by GPT-4V, used for higher-quality alignment | 100万条GPT-4V生成的密集描述，用于更高质量的对齐 | |
| VQA | "Visual question answering" | Task of answering a free-form question about an image | 视觉问答：回答关于图像的自由形式问题 | |
| Prismatic VLMs | "Design-space paper" | Karamcheti 2024 ablation systematically testing projector and data choices | 系统测试投影器和数据选择的设计空间消融实验论文 | |

## Xem thêm 延伸阅读

- [Liu et al. — Visual Instruction Tuning (arXiv:2304.08485)](https://arxiv.org/abs/2304.08485) báo LLaVA.  LLaVA Original Essay
- [Liu et al. — Improved Baselines with Visual Instruction Tuning (arXiv:2310.03744)](https://arxiv.org/abs/2310.03744) LLaVA-1.5.  LLaVA-1.5 改进版
- [Chen et al. — ShareGPT4V (arXiv:2311.12793)](https://arxiv.org/abs/2311.12793) tập hợp dữ liệu tiêu đề dày đặc. 密集 mô tả tập dữ liệu
- [Karamcheti et al. — Prismatic VLMs (arXiv:2402.07865)](https://arxiv.org/abs/2402.07865) thiết kế không gian-ablations.
- [Li et al. — LLaVA-OneVision (arXiv:2408.03326)](https://arxiv.org/abs/2408.03326) Unified single-image, multi-image, video. 统一单图多图视频版本
