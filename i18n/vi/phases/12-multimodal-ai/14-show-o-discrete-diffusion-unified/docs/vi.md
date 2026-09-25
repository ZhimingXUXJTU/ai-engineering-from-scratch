# Show-o và Different-Diffusion Models

> Thuốc truyền trộn các biểu diễn liên tục và riêng biệt. Show-o (Xie et al., tháng 8 năm 2024) đi theo hướng khác: mã thông báo văn bản sử dụng dự đoán mã thông báo tiếp theo nguyên nhân, mã thông báo hình ảnh sử dụng sự lan truyền kín kín trong tinh thần của MaskGIT. Cả hai đều ngồi trong một bộ biến đổi với một mặt nạ tập trung lai. Kết quả thống nhất VQA, text-to-image, inpainting, và sản xuất modality hỗn hợp trên một xương sống, một tokeniser mỗi modality, một công thức mất mát (token tiếp theo mở rộng đến dự đoán che giấu). Bài học này đi theo thiết kế Show-o tại sao sự phân tán phân biệt được che giấu là một máy tạo hình ảnh song song, vài bước và tương phản với Transfusion và Emu3.

> **【中文解读】**Show-o(2024年8月)走另一条路:文本代币 用因果下一代币 预测,图像代币 用掩码离散散散散散(MaskGIT风格) ・・・两者共用一个变压器,用混合注意力掩码──结果是一个检查点 同时支持VQA、文本生成图像和图像修复──

> **【拓展：并行解码的速度优势】**Show-o sinh thành hình ảnh chỉ cần khoảng 16 bước, trong khi Chameleon / Emu3 cần 1024-4096 bước, cho mỗi token tự quay trở lại.

**Type:** Learn  | **类型:** 学习
**Languages:** Python (stdlib, masked-discrete-diffusion sampler) | **语言:** Python（标准库，掩码离散扩散采样器）
**Prerequisites:** Phase 12 · 13 (Transfusion) | **前置知识:** Phase 12 · 13（Transfusion）
**Time:** ~120 minutes | **时间:** ~120 分钟

>  **【前置】**Học本节前请先掌握:Phase 12·13(Tâm nhập 双损失) Phase 12·11-12(Chameleon/Emu3 离散代币) Phase 8(MaskGIT 离散扩散概念) ――Show-o = toàn离散 + 图像使用MaskGIT 风格并行解码,速度比Emu3 快 60倍──
>  **【类比】**Show-o = "并行开锁"──Emu3 = 一把钥匙开 1024 把锁(自归单代币);Show-o = 16 步内同时尝试所有锁(掩码扩散并行解码)──代价:图像质量略差(VQ 量化损失),但推理快得多──

## Mục tiêu học tập

- Giải thích sự phân tán phân biệt được che giấu: lịch trình che giấu token một cách đồng nhất sau đó yêu cầu biến đổi để phục hồi chúng.
  > 解释掩码离散扩散:均掩码 token 然后让变压器恢复调度.
- So sánh việc giải mã hình ảnh song song (Show-o, MaskGIT) với việc giải mã hình ảnh tự rút (Chameleon, Emu3) về tốc độ và chất lượng.
  > So sánh并行图像解码(Show-o、MaskGIT) với tự quay lại图像解码(Chameleon、Emu3) trong tốc độ và chất lượng khác biệt。
- Tên gọi ba nhiệm vụ Show-o xử lý tại một điểm kiểm soát: T2I, VQA, vẽ hình ảnh.
  > 列举 Show-o ở một điểm kiểm soát Trung hỗ trợ ba nhiệm vụ: T2I、VQA、图像修复──
- Chọn một lịch trình che giấu (các, tuyến tính, cắt) và lý luận về tác động của nó đối với chất lượng mẫu.
  > 选择掩码调度 (余弦、线性、截断) và phân tích tác động của nó đối với chất lượng mẫu.

## Vấn đề  vấn đề nền

Việc đào tạo hai lỗ của sự truyền máu hoạt động nhưng có động lực phức tạp hơn.

> Tập luyện hai lỗ hổng của truyền máu có thể thực hiện nhưng động thái phức tạp hơn liên tục mở rộng lỗ hổng và phân tán NTP  lỗ hổng khác nhau trên các thước đo số lượng── cân bằng mất trọng lượng là một siêu số tìm kiếm── cấu trúc hiệu quả nhưng phức tạp──

Câu trả lời của Show-o: giữ cả hai phương pháp tách biệt (như Chameleon), nhưng tạo ra hình ảnh song song bằng cách phân tán phân biệt được che giấu thay vì theo trình tự. Mục tiêu đào tạo trở thành một dự đoán mã hóa được che giấu duy nhất, tổng quát dự đoán mã hóa tiếp theo tự nhiên.

> Câu trả lời của Show-o: giữ hai kiểu hình thức đều phân tán, nhưng thông qua ẩn dấu phân tán và phát triển và tạo ra hình ảnh, chứ không phải tạo ra theo thứ tự.

## Khái niệm cốt lõi

> **【中文解读】**Show-o 统一多模态理解和生成, sử dụng phân tán扩散替代传统连续扩散── phân tán扩散 trực tiếp trong token 级别操作, sẽ phủ kín dự đoán  understanding task) và 噪音 生成任务) 统一在同一框架下──

> **【拓展：离散扩散的统一优势】**离散扩散将文本生成和图像生成统一到同一个数学框架 (掩码代币预测), làm cho việc tập luyện hợp tác đa dạng đơn giản hơn. Đây là xu hướng của AI đa dạng năm 2025.


### Phân phối phân biệt được che giấu (MaskGIT)

Trận thuật của Chang et al. (2022) MaskGIT là thanh lịch. Bắt đầu từ một hình ảnh hoàn toàn che giấu (mỗi biểu tượng là đặc biệt `<MASK>`ID). Tại mỗi bước, dự đoán tất cả các token che giấu song song, sau đó giữ các dự đoán tự tin nhất ở trên-K và che giấu lại phần còn lại. Sau ~ 8-16 lần lặp lại, tất cả các token được điền vào.

> Nguyên nhân của Chang 等人(2022) MaskGIT 技巧 rất đẹp. Từ hình ảnh được ẩn hoàn toàn bắt đầu.`<MASK>`ID) ・ mỗi bước并行预测 tất cả các mã hóa mã hóa, sau đó giữ cho top-K 最有信心的预测并重新掩盖其余的──经过约8-16次代, tất cả các mã hóa đều được lấp đầy── mỗi bước giải ẩn bao nhiêu mã hóa điều chỉnh cần điều chỉnh 优余弦调调效好──

Việc đào tạo đơn giản: lấy mẫu tỷ lệ che giấu một cách đồng đều từ [0, 1], áp dụng nó vào các token VQ của hình ảnh, đào tạo bộ biến đổi để lấy lại những mã che phủ.

> 训练 rất đơn giản: từ [0, 1] 均采样掩码比例, áp dụng cho hình ảnh VQ token,训练 Transformer 恢复被掩码的 token──就是BERT对文本做,扩展到图像生成──

### Show-o: một biến thể, mặt nạ lai

Show-o đặt MaskGIT bên trong một biến thể mô hình ngôn ngữ nguyên nhân.

> Show-o sẽ MaskGIT 放入因果语言模型 Transformer 中──注意力掩码是:

- Các mã thông báo văn bản: nguyên nhân (Mỹ pháp luật tiêu chuẩn).
  Trung文翻译:文本代号:因果(标准 LLM) 』
- Các token hình ảnh: hoàn toàn hai chiều trong khối hình ảnh (vì vậy các token che giấu có thể nhìn thấy mọi token hình ảnh khác trong quá trình dự đoán).
  Trung ngữ翻译:图像代币:图像块内全双向(掩码代币可以在预测时看到所有其他图像代币) ⋅
- Text-to-image: text sẽ phụ thuộc vào hình ảnh trước, hình ảnh sẽ phụ thuộc vào text trước.
  Trung văn翻译:文本到图像:文本关注之前的图像,图像关注之前的文本──

Các sự thay thế đào tạo giữa:
1. NTP tiêu chuẩn trên các chuỗi văn bản.
   Trung ngữ翻译:文本序列上的标准 NTP──
2. Các mẫu T2I: văn bản → hình ảnh với mã thông báo hình ảnh che giấu, mất tiền báo ký hiệu che giấu.
   Trung ngữ翻译:T2I 样本:文本→带掩码图像代号的图像,掩码代号 预测损失──
3. Các mẫu VQA: hình ảnh → văn bản với các mã thông báo văn bản được che giấu (thực sự chỉ là NTP).
   Trung văn翻译:VQA 样本:图像→带掩码文本代币的文本(实际上就是NTP) 』

Sự mất mát thống nhất là sự chuyển động giữa các loài.`<MASK>`token, bao gồm cả NTP văn bản (chỉ token cuối cùng là "đã che giấu") và hình ảnh được che giấu-sải (đã bộ phận ngẫu nhiên được che giấu).

> 统一损失是 `<MASK>`token 上的交叉,同时覆盖文本 NTP( Chỉ có token cuối cùng là "掩码" của) và hình ảnh掩码扩散(随机子集被掩码)

### Tiêu chuẩn lấy mẫu song song

Show-o tạo ra một hình ảnh trong ~ 16 bước thay vì ~ 1000 (để tự rút lại mỗi token) hoặc ~ 20 (đối truyền).

> Show-o trong khoảng 16 bước trong tạo hình ảnh, thay vì khoảng 1000 bước (một lần tự trở lại) hoặc khoảng 20 bước (một lần mở rộng)

So sánh:
- Chameleon / Emu3 (được tự rút trên token): N_tokens đi trước, thường là 1024-4096 cho mỗi hình ảnh.
  Trung文翻译:Chameleon / Emu3(逐 token 自归归):N_tokens 次前向传播, thường mỗi张图像 1024-4096。
- Thuốc truyền (tải truyền liên tục): ~ 20 bước, mỗi bước là một chuyển đổi viên đầy đủ.
  Trung文翻译:Transfusion(连续扩散): khoảng 20 步, mỗi bước một lần hoàn chỉnh Transformer 传播。
- Show-o (các pha trộn phân biệt được che giấu): ~ 16 bước, mỗi bước là một bước chuyển đổi đầy đủ.
  Trung文翻译:Show-o(掩码离散扩散): khoảng 16 步, mỗi bước một lần hoàn chỉnh Transformer 传播。

Show-o nhanh hơn Chameleon ở các mô hình quy mô tương tự, tương đương với số bước Transfusion với chi phí từng bước thấp hơn (những logit từ ngữ riêng biệt so với mất MSE liên tục).

> Show-o trên mô hình tương tự hơn Chameleon, bước số lớn phù hợp Transfusion, nhưng chi phí mỗi bước thấp hơn

### Các nhiệm vụ tại một điểm kiểm soát

Show-o hỗ trợ bốn nhiệm vụ khi suy luận, được chọn theo định dạng nhanh:

> Show-o trong việc đề xuất hỗ trợ bốn nhiệm vụ, thông qua các gợi ý:

- Tạo văn bản: đầu ra văn bản tự rút tiêu chuẩn.
  中文翻译:文本生成:标准自归文本输出。
- VQA: hình ảnh vào, tin nhắn ra.
  Trung văn翻译:VQA:图像输入,文本输出。
- T2I: text in, image out qua masked discrete diffusion.
  Trung văn翻译:T2I:文本输入,通过掩码离散扩散输出图像──
- Đơn: hình ảnh với một số mã thông báo được che giấu, điền vào.
  Trung ngữ翻译:图像修复:带部分掩码代号的图像,填充缺失部分──

Khả năng vẽ màu được miễn phí từ đào tạo dự đoán ẩn mặt. n một khu vực của lưới mã VQ, cung cấp phần còn lại cộng với lời nhắc văn bản, dự đoán mã ẩn mặt.

> 图像修复能力从掩码预测训练中免费获得──掩码 VQ token 网格的一个区域,进入其余部分加上文本提示,预测被掩码的 token──

### Thời gian đeo mặt nạ

Chương trình về số lượng token để tháo mặt nạ mỗi bước hình thành chất lượng.

> Mỗi bước giải ẩn码 số lượng token của调度 ảnh hưởng đến chất lượng.

```
mask_ratio(t) = cos(pi * t / (2 * T))   # t = 0..T
```

Ở bước 0, tất cả các token được che giấu ( tỷ lệ 1.0). Ở bước T, không có một cái nào che giấu. Cosine tập trung khối lượng vào tỷ lệ giữa phạm vi nơi dự đoán là thông tin thông tin nhất.

> 第 0 步, tất cả các token được ẩn chứa( tỷ lệ 1.0)。第 T 步,无掩码。余弦调度将质量集中在中程比例上,此时预测信息量最大──线性调度也可用但更早和──

### Show-o2

Show-o2 (2025 theo dõi, arXiv 2506.15564) quy mô Show-o: cơ sở LLM lớn hơn, tokenizer tốt hơn, lịch trình mặt nạ cải thiện.

### Ở chỗ Show-o ngồi

Trong phân loại năm 2026:

> Trong năm 2026:

- Các mã thông báo riêng biệt + NTP: Chameleon, Emu3.
  中文翻译:离散代币 + NTP:Chameleon、Emu3──简单但推理慢──
- Các token riêng biệt + phân tán ẩn: Show-o, MaskGIT, LlamaGen, Muse.
  Trung文翻译:离散代币 + 掩码扩散:Show-o、MaskGIT、LlamaGen、Muse。并行采样, vẫn受分词器损失限制。
- Tiếp tục + phân tán: Thuốc truyền, MMDiT, DiT. Chất lượng cao nhất, đào tạo phức tạp hơn.
  Trung文翻译:连续 + 扩散:Tâm nhập, MMDiT, DiT, 训练更复杂, 训练更复杂, 训练更复杂, 训练更复杂, 训练更复杂, 训练更复杂, 训练更复杂, 训练更复杂, 训练更复杂, 训练更复杂, 训练更复杂, 训练更复杂, 训练更复杂, 训练更复杂, 训练更复杂, 训练更复杂, 训练更复杂, 训练更复杂, 训练更复杂, 训练更复杂, 训练更复杂, 训练更复杂, 训练更复杂, 训练更复杂, 转变, 转变, 转变, 转变, 转变, 转变, 转变, 转变,转变,转变
- Tiếp tục + dòng chảy phù hợp trong một VLM: JanusFlow, InternVL-U.
  中文翻译:VLM 中连续 + 流匹配:JanusFlow、InternVL-U──最新──

Chọn theo nhiệm vụ: Show-o khi bạn muốn T2I + inpainting + VQA trong một mô hình mở với tốc độ hợp lý; Chuyển máu khi chất lượng là tối ưu và bạn có thể đủ khả năng để trả tiền cho ống nước hai lỗ.

> 按任务选择: cần một mô hình mở đồng thời thực hiện T2I + 修复 + VQA 且速度合理时选 Show-o;质量至上且能承担双损失复杂性时选 转血。


> **【拓展：Show-o 的离散扩散方法】**Show-o của phân tán phổ biến sử dụng ẩn dự đoán:随机遮盖部分 token,模型预测被遮盖的 token──理解任务遮盖答案部分,生成任务从全遮盖开始逐步到噪声──数学上等价于多项式扩散──


## Hãy dùng nó để thực hành
```figure
masked-diffusion-unmask
```

## Sử dụng nó

`code/main.py`mô phỏng lấy mẫu show-o:

> `code/main.py`模拟 Show-o 采样:

- Một lưới đồ chơi gồm 16 token VQ.
  Trung文翻译: một 16 VQ token của đồ chơi网格.
- Một "giới chuyển đổi" giả mạo dự đoán logits dựa trên một lời nhắc và các token hiện chưa được che giấu.
  Trung文翻译:一个模拟"Transformer", dựa trên提示和当前未掩码 token 预测 logits。
- Phân tích mẫu ngụy trang song song trên 8 bước với lịch trình cosine.
  Trung文翻译:余弦调度下的 8 步并行掩码采样。
- Bác in các trạng thái trung gian (tự tiến hóa mô hình mặt nạ) và các token cuối cùng.
  Trung ngữ翻译:打印中间状态 (Bộ hình thức diễn biến) và cuối cùng token (Tương tự: dấu chấm cuối cùng).

Đi, xem mặt nạ tan chảy từng bước.

> 运行它,观察掩码逐步消解.

## Đưa nó lên mạng

Bài học này sẽ mang lại kết quả `outputs/skill-unified-gen-model-picker.md`. Với một sản phẩm cần cả sự hiểu biết (VQA, captioning) và thế hệ (T2I, inpainting) với giới hạn trọng lượng mở, chọn giữa gia đình Show-o, gia đình Transfusion/MMDiT, và gia đình Emu3 / Chameleon với sự thỏa hiệp cụ thể.

> 本课产 出 `outputs/skill-unified-gen-model-picker.md`△给定需要理解(VQA、描述) 和生成(T2I、修复) 且限开权重的产品,在 Show-o、Transfusion/MMDiT 和 Emu3/Chameleon 家族间选择,附具体权衡──

## Tập luyện bài tập

1. Các mẫu phân tán phân tán được che giấu trong ~ 16 bước. Tại sao không 1?
   Trung ngữ翻译:掩码离散散散散在约16步内采样――为什么不是1步?

2. Đơn màu miễn phí với sự pha trộn che giấu. đề xuất một trường hợp sử dụng sản phẩm (thực tế hoặc giả thuyết) nơi mà màu màu của Show-o vượt qua mô hình chuyên môn.
   Trung ngữ翻译:掩码扩散的图像修复是免费的── đề xuất một Show-o 修复能力胜过专业模型的产品用例──

3. Chương trình Cosine vs lịch trình tuyến tính: theo dõi số lượng các token không che giấu mỗi bước cho T = 8.
   Trung文翻译:余弦调度 VS 线性调度: theo dõi T=8 时每步解掩码的符号 数――哪个更平衡?

4. Một hình ảnh hiển thị 512x512 là 1024 mã thông báo. Ở từ K = 16384, mô hình phát ra 1024 * log2(16384) = 14,336 bit (~ 1,75 KiB) dữ liệu.
   Trung ngữ翻译:512x512 Show-o 图像是1024 个代币──词汇表 K=16384 下,模型输出约1.75 KiB 数据──SD 输出约768 KiB 原始像素──压缩比是多少?换来什么质量?

5. LlamaGen (arXiv:2406.06525). mô hình hình ảnh tự rút theo điều kiện lớp học của LlamaGen khác với cách tiếp cận che giấu của Show-o như thế nào?
   Trung文翻译:阅读 LlamaGen(arXiv:2406.06525) ―― Các điều kiện tự quay lại của LlamaGen với phương pháp ẩn giấu của Show-o có gì khác nhau?

## Từ khóa  Keyword

| Term | What people say | What it actually means | 中文含义 | 中文释义 |
|------|-----------------|------------------------|---------|
| Masked discrete diffusion | "MaskGIT-style" | Training to predict masked tokens; at inference, iteratively unmask the most-confident predictions | 训练预测掩码 token；推理时迭代解掩码最有信心的预测 |
| Cosine schedule | "Unmask schedule" | Decay of mask ratio over inference steps; concentrates confidence growth at mid-range | 推理步骤中掩码比例的衰减；将信心增长集中在中程 |
| Parallel decoding | "All tokens at once" | Every step predicts the full sequence of masked tokens in one forward pass, then commits top-K | 每步在一次前向传播中预测所有掩码 token，然后提交 top-K |
| Hybrid attention | "Causal + bidirectional" | Mask that is causal over text tokens and bidirectional within image blocks | 文本 token 因果、图像块内双向的掩码 |
| Inpainting | "Fill-in generation" | Condition on an image with some tokens masked, predict the missing ones; free from the training objective | 以部分掩码图像为条件，预测缺失 token；从训练目标免费获得 |
| Commitment rate | "Top-K per step" | How many tokens are declared "done" per iteration; controls inference vs quality trade-off | 每次迭代声明"完成"的 token 数；控制推理与质量的权衡 |

## Xem thêm 延伸阅读

- [Xie et al. — Show-o (arXiv:2408.12528)](https://arxiv.org/abs/2408.12528)
  Trung văn翻译:Show-o 论文。
- [Show-o2 (arXiv:2506.15564)](https://arxiv.org/abs/2506.15564)
  中文翻译:Show-o2 后续论文。
- [Chang et al. — MaskGIT (arXiv:2202.04200)](https://arxiv.org/abs/2202.04200)
  Trung ngữ翻译:MaskGIT 论文,掩码离散扩散的原始工作──
- [Sun et al. — LlamaGen (arXiv:2406.06525)](https://arxiv.org/abs/2406.06525)
  Trung文翻译:LlamaGen 自归图像生成──
- [Chang et al. — Muse (arXiv:2301.00704)](https://arxiv.org/abs/2301.00704)
  Trung文翻译:Muse 掩码图像生成──
