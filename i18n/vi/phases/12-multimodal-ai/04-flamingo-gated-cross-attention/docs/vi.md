# Flamingo và Gate Cross-Atention cho VLMs ít bắn .

> Flamingo của DeepMind (2022) đã làm hai điều trước bất cứ ai khác. Nó cho thấy một mô hình duy nhất có thể xử lý theo trình tự tự tự nhiên của hình ảnh, video và văn bản. Và nó cho thấy VLM có thể học trong bối cảnh  đưa ra một vài cú chụp với ba cặp ví dụ (hình ảnh, tiêu đề) và mô hình ghi chú một hình ảnh mới mà không cần bất kỳ bước gradient nào. Cơ chế: các lớp chú ý chéo bị khóa, được đưa vào giữa các lớp hiện có của LLM đóng băng, với một cổng tanh học được bắt đầu từ không để khả năng văn bản của LLM được bảo tồn khi khởi tạo. Bài học này đi bộ với thiết kế thiết kế nhận thức của Flamingo và kiến trúc quan tâm chéo  tổ tiên của các đầu vào liên kết của Gemini và các token thị giác của Idefics2.

> **【中文解读】**Flamingo  lần đầu tiên thực hiện hình ảnh giao tiếp nhập và trên dưới văn bản ít mẫu học.

> **【拓展：Flamingo→Gemini交织输入】**Phương thức xử lý hình ảnh của Flamingo là mô hình gốc của biểu tượng hình ảnh của Gemini, bắt đầu với nhiều mô hình văn học.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, gated cross-attention + Perceiver resampler demo) | **语言:** Python（标准库，门控交叉注意力 + Perceiver resampler 演示）
**Prerequisites:** Phase 12 · 03 (BLIP-2 Q-Former) | **前置知识:** Phase 12 · 03（BLIP-2 Q-Former）
**Time:** ~120 minutes | **时间:** ~120 分钟

>  **【前置】**Học本节前请先掌握:Phase 12·03(BLIP-2 Q-Former,理解交叉注意力和学习性查询);Phase 7(Transformer残差结构);Phase 11·05(In-context Learning 概念)。Flamingo 和 BLIP-2 最大的不同:BLIP-2 在 LLM 输入端桥接一次;Flamingo 在 LLM 每隔几层插入门控制层。
>  **【类比】**Flamingo's Gate Control giao thông chú ý = "Việc sửa đổi nhỏ trong các ngành ngoại khoa"。BLIP-2 = "trong LLM 大门口装一个翻译员"(输入端桥接一次);Flamingo = "trong mỗi tầng văn phòng của LLM đặt một cửa sổ"(mỗi 4 tầng một cửa sổ kiểm soát giao thông chú ý)。门控初始为 0 = 窗口一开始关闭, mô hình hành vi giống như LLM nguyên thủy 完全一样;训练慢慢开窗 = 视觉信息逐渐注入但不破坏原始文本能力──

## Mục tiêu học tập

- Giải thích cách thức quan tâm chéo được gài giữ lại khả năng văn bản của LLM đóng băng khi khởi tạo thông qua tanh(gate) = 0.
  Trung ngữ翻译:解释门控交叉注意力如何通过tanh(gate) = 0 在初始化时保持结 LLM 的文本能力──
- Đi qua một thiết bị lấy mẫu lại của Perceiver: N image patches → K cố định các truy vấn "latent" thông qua sự chú ý chéo.
  Trung文翻译:理 Perceiver resampler:N 个图像 patch → 通过交叉注意力产生 K 个固定"潜在"查询。
- Mô tả cách Flamingo xử lý các chuỗi hình ảnh-môn văn được giao với sự che giấu nguyên nhân tôn trọng vị trí hình ảnh.
  Trung ngữ翻译:描述 Flamingo 如何使用尊重图像位置的因果掩码处理交织的图文序列──
- Tạo lại cấu trúc đơn giản đa phương pháp với vài lần chụp (3 ví dụ về tựa đề hình ảnh sau đó là hình ảnh truy vấn).
  Trung ngữ翻译:复现少样本多模态提示结构(3 个图文示例后跟一个查询图像) 』

## Vấn đề  vấn đề giới thiệu

BLIP-2 cung cấp 32 token thị giác vào lớp đầu vào của LLM đóng băng. Làm việc cho một hình ảnh mỗi lời nhắc. Nhưng nếu bạn muốn cung cấp nhiều hình ảnh với văn bản, như trong "đây là hình ảnh A, ghi chú nó; đây là hình ảnh B, ghi chú nó; bây giờ đây là hình ảnh C, ghi chú nó"? Sự tự chú ý của LLM sẽ cần phải xử lý các token hình ảnh và các token văn bản trong một dòng chảy duy nhất, và câu hỏi về vị trí nào có thể tham gia vào hình ảnh nào trở nên khó khăn.

> BLIP-2 sẽ đưa ra 32 biểu tượng hình ảnh  vào vào vào các tầng nhập của LLM. Nó có thể được áp dụng cho mỗi gợi ý một hình ảnh. Nhưng nếu bạn muốn tham gia vào các hình ảnh liên quan đến văn bản, ví dụ như "Đây là hình ảnh A, mô tả nó; đây là hình ảnh B, mô tả nó; đây là hình ảnh C, mô tả nó"?

Câu trả lời của Flamingo: không thay đổi dòng đầu vào của LLM. Đặt thêm các lớp chú ý chéo giữa các khối LLM hiện có. Các mã thông báo văn bản vẫn chảy qua sự chú ý tự do của LLM như thường lệ. Giữa mỗi vài khối LLM, các mã thông báo văn bản cũng xuyên qua các tính năng hình ảnh thông qua một lớp bị khóa mới. Cổng (được khởi tạo thành không) có nghĩa là ở bước không, các lớp mới là không có hoạt động. Khi đào tạo tiến triển, cánh cổng mở ra và thông tin trực quan bắt đầu chảy.

> Phản ứng của Flamingo: hoàn toàn không thay đổi dòng chảy nhập vào LLM. Trong các khối LLM hiện có, các giao lưu lưu chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển đổi chuyển

Flamingo trả lời câu hỏi thứ hai: làm thế nào để xử lý một số hình ảnh biến đổi (0, 1 hoặc nhiều) mỗi prompt? Một Perceiver resampler  một mô-đun liên quan nhỏ có thể lấy bất kỳ số lượng các bản vá nào bạn có và tạo ra một số lượng cố định của các token ẩn thị.

> Flamingo  trả lời câu hỏi thứ hai: làm thế nào để xử lý mỗi gợi ý số lượng hình ảnh có thể thay đổi trong số đó?

## Khái niệm cốt lõi

> **【中文解读】**Flamingo(DeepMind) Introduction Gate Control giao thông chú ý(Gated Cross-Attention), trong kết thúc LLM layer vào giữa 结插入可训练的交叉注意力层 để inject视觉信息──门控机控制视觉信息的流入量,初始化时门控制值为0(视觉信息不流入), trong quá trình đào tạo dần mở──

> **【拓展：Flamingo 的高效适配】**Flamingo chỉ tập luyện khoảng 1% của các tham số (với chỉ số 1), được thực hiện trong một vài lần chụp 视觉推理任务 để đạt được SOTA.


> **【拓展：门控机制的数学原理】**门控交叉注意的门控值初始化为0, nghĩa là khi bắt đầu đào tạo, thông tin thị giác hoàn toàn không chảy vào LLM。


### LLM đóng băng

Flamingo bắt đầu với một bộ phim LLM 70B của Chinchilla.

> Flamingo 以结的Chinchilla 70B LLM 为起点──所有700亿权重不触碰──现有文本自注意力和FFN 正常运行──

### Tâm đơn nhận thức

Đối với mỗi hình ảnh trong prompt, ViT tạo ra N patch token. Perceiver resampler có K cố định học được laten (Flamingo sử dụng K=64).

> Đối với mỗi bức ảnh trong gợi ý,ViT tạo ra N 个 patch token。Sampler nhận thức có K 个 xác định có thể học được tiềm năng向量(Flamingo sử dụng K=64)。 Mỗi mẫu mẫu 块 có hai bước:

> 🤔 **【困惑】**Q: Perceiver resampler 和 BLIP-2 của Q-Former có gì khác biệt?A: 思想 gần như giống nhau(phàn hỏi có thể học từ bản vá 提取信息), nhưng Flamingo của Perceiver resampler chỉ làm hình ảnh đặc điểm nén, không tham gia đối với đào tạo mất mát; Q-Former là biến thể  cấu trúc và có ITC/ITM/ITG 三个损失── có thể cho rằng Perceiver resampler là Q-Former của phiên bản đơn giản hóa──

1. Sự chú ý chéo: các dấu ẩn K là đối tượng của các mã thông báo N (Q từ dấu ẩn, K/V từ các dấu cố).
   Trung文翻译:交叉注意力:K 个潜在向量关注 N 个补丁代币(Q 来自潜在向量,K/V 来自补丁) 』
2. Sự chú ý tự chủ + FFN trong những điều ẩn dật.
   Trung ngữ翻译: tiềm năng lực trong trong của tự chú ý + FFN。

Sau 6 khối resampler, đầu ra là K = 64 token thị giác của dim 1024, bất kể ViT đã tạo ra bao nhiêu bản vá.

> Sau 6 khối mẫu lại, đầu ra là K=64 个维度为 1024 视觉代币, bất kể ViT  tạo ra bao nhiêu bản váy. 224x224 图像(196 bản váy) và 480x480 图像(900 bản váy) đều xuất ra là 64 个 mẫu lại代币.

Đối với video, resampler được áp dụng theo thời gian: các bản vá của mỗi khung tạo ra 64 laten, và mã hóa vị trí thời gian cho phép mô hình phân biệt t=0 từ t=N. Video đầy đủ trở thành token thị giác T * 64.

> Đối với video, mẫu 按时间维度应用:每的补丁 产生 64 潜在向量,时间位置编码让模型区分 t=0 和 t=N──完整视频变成T * 64 视觉代币──

### Sự chú ý qua nhau

Giữa mỗi lớp M của LLM đông lạnh (Flamingo sử dụng M=4), hãy chèn một khối quan tâm chéo bị khóa mới:

> Trong kết thúc LLM của mỗi M 层之间(Flamingo sử dụng M=4),插入一个新的门控交叉注意力块:

```
x_after_llm_block = llm_block(x_before)
cross = cross_attn(x_after, resampler_output)
gated = tanh(alpha) * cross + x_after
x_before_next_block = gated
```

- `alpha`là một scalar có thể học được khởi tạo lên 0.
  Trung ngữ翻译:`alpha`là một số lượng có thể học được, khởi nghiệp là 0.
- `tanh(0) = 0`, vì vậy tại init, chi nhánh đóng cửa đóng góp bằng không.
  Trung ngữ翻译:`tanh(0) = 0`, vì vậy trong quá trình khởi nghiệp, chi phí đóng góp là 0.
- Như `alpha`nếu chuyển xa khỏi 0 thì sự đóng góp của sự chú ý qua nhau sẽ tăng lên một cách trơn tru.
  Trung ngữ翻译:随随`alpha`远离零,交叉注意力贡献平滑增长──
- Kết nối còn lại có nghĩa là ngay cả một cổng mở hoàn toàn không ghi lại bản đại diện văn bản của LLM; nó chỉ thêm thông tin trực quan ở trên.
  Trung ngữ翻译:残差连接 có nghĩa là ngay cả khi cửa được kiểm soát hoàn toàn mở, cũng sẽ không bao gồm văn bản của LLM; nó chỉ là trên để thêm thông tin trực quan.

Đây là lựa chọn thiết kế duy nhất quan trọng nhất trong Flamingo: điều kiện thị giác là cộng, bị khóa và không khi khởi tạo.

> Đây là lựa chọn thiết kế quan trọng nhất trong Flamingo: điều kiện hình ảnh là có thể tăng lên, được kiểm soát, được khởi tạo thành 0.

> ️ **【易错点】**Bản thân thực hiện thời gian quên bắt đầu alpha=0, trực tiếp随机初始化 → 训练前几步 LLM 文本能力就会崩──原因:未训练的交叉注意力输出是噪音,混入 LLM 内部表示会破坏文本知识──修复:alpha 必须初始化为0,让模型从"完美 LLM"发发,缓慢学习──
>  **【类比】**零初始化门控 = "new员工进入职模式"──新员工 (新员工) 视层) 第一周只观察、不说话(gate=0); quen thuộc với kinh doanh sau khi dần phát言(gate 慢慢打开)──直接让新员工主导决策(gate≠0初始化) sẽ làm rối loạn đội ngũ có bản chất của mình(破坏 LLM 文本能力)──

### Sự chú ý chéo che giấu cho các đầu vào được giao tiếp

Trong một lệnh như "<image A> caption A <image B> caption B <image C> ?", mỗi mã thông báo văn bản chỉ nên hiển thị các hình ảnh trước đó trong chuỗi.`t`chỉ tham gia vào các token resampler hình ảnh có chỉ số hình ảnh `i < i_t`nơi `i_t`là hình ảnh gần đây nhất trước vị trí `t`"Hãy nhìn thấy hình ảnh trước cuối cùng" hoặc "hãy nhìn thấy tất cả hình ảnh trước" là cả hai lựa chọn hợp lệ; Flamingo chọn trước.

> Trong các gợi ý của "<图像 A> 描述 A <图像 B> 描述 B <图像 C> ?" , mỗi biểu tượng văn bản chỉ nên xem trong chuỗi nằm trước đó của nó hình ảnh.`t`                                                                                                                                                                                                                                                              `i < i_t`                                                                                                                                                                                                                                                              `i_t``t`之前最近图像──" chỉ xem gần nhất图像" hoặc "看所有之前图像" đều là lựa chọn hợp lệ; Flamingo 选择前者──

### Học tập trong bối cảnh ít ảnh

Một lời nhắc nhở của Flamingo trông giống như:

> Flamingo 提示 trông như thế này:

```
<image1> A photo of a cat. <image2> A photo of a dog. <image3> A photo of a
```

Mô hình nhìn thấy mô hình hoàn thành và xuất hiện "con chim" (hoặc bất cứ hình ảnh nào3 cho thấy). Không có bước nghiêng. Khả năng học tập trong bối cảnh của LLM đóng băng mang thông qua sự chú ý chéo bị khóa.

> 模型看补全模式并输出"bird" (或图3 显示任何内容) ⋅无需梯度步骤――结 LLM's上下文学习能力通过门控交叉注意力传递这是论文的关键点,也是它的重要原因

> 🤔 **【困惑】**Q: Tại sao Flamingo 能 trong ngữ cảnh học, còn BLIP-2 不能?A: Flamingo trong LLM Mỗi 4 tầng được thấm vào thông tin trực quan,LLM 内部的视频信息注入视频信息,LLM 内部的视频学习(在阶段11·05学习过) vẫn hoàn chỉnh工作;BLIP-2 放置32 视频代币 直接拼到快速前面,LLM 把它们作为普通代币处理,但训练目标里没有显式的少数射击模式,所以能力弱――

### Dữ liệu đào tạo

Flamingo được đào tạo trên ba bộ dữ liệu:

> Flamingo trong ba tập hợp dữ liệu tập luyện:

1. MultiModal MassiveWeb (M3W): 43M trang web với hình ảnh và văn bản được giao lưu, tái cấu trúc thứ tự đọc.
   Trung ngữ翻译:多模态 MassiveWeb(M3W):4300.000包含交织图像和文本的网页,重建阅读顺序──
2. Cặp hình ảnh-môn văn bản (ALIGN + LTIP): 4,4B cặp.
   Trung文翻译:图文对(ALIGN + LTIP):44 亿对──
3. Video-Text Pairs (VTP): 27M clip video ngắn.
   Trung ngữ翻译:视频-文本对(VTP): 270000000个短视频片段──

OBELICS (2023) là một bản sao mở của các kết nối web được giao lưu, mà Idefics, Idefics2 và hầu hết các mô hình "Flamingo-like" mở được đào tạo.

> OBELICS(2023) là một tập hợp mở của các bộ nhớ ngôn ngữ mạng, các ý tưởng, ý tưởng2 và hầu hết các mô hình "chẳng loại Flamingo" mở trên nó.

### OpenFlamingo và Otter

OpenFlamingo (2023) là bản sao mở. Kiến trúc giống hệt nhau (Perceiver resampler + gated cross-attention trên LLaMA hoặc MPT đóng băng).

> OpenFlamingo(2023) là mở复现──架构相同(Perceiver resampler + 结 LLaMA hoặc MPT 上的门控交叉注意力)──3B、4B、9B 检查点──由于基础 LLM 更小和数据更少,质量落后于 Flamingo──

Otter (2023) xây dựng trên OpenFlamingo với điều chỉnh hướng dẫn trên MIMIC-IT (một bộ dữ liệu của các hướng dẫn đa phương thức), cho thấy các công việc chú ý chéo bị khóa cho hướng dẫn theo dõi cũng vậy.

> Otter(2023) trên cơ sở OpenFlamingo  sử dụng MIMIC-IT(多模态指令数据集) để thực hiện chỉ thị nhỏ调, chứng minh门控交叉注意力 cũng áp dụng cho chỉ thị theo dõi。

### Những hậu duệ

- Idefics / Idefics2 / Idefics3: dòng dõi chú ý chéo được đóng cửa của Hugging Face, dần đơn giản hơn (Idefics2 đã bỏ lại mẫu lại để ủng hộ các mã thông báo vá trực tiếp với sự hợp tác thích ứng).
  Trung文翻译:Idefics / Idefics2 / Idefics3: Hugging Face 的门控交叉注意力谱系,逐步简化(Idefics2 去掉样品,改用自适应池化的直接补丁代币)
- Chuyển đổi Flamingo-Chameleon: đến năm 2024, nhiều đội đã chuyển sang hợp nhất sớm (Dạy 12.11); Sự chú ý chéo theo phong cách Flamingo vẫn còn trong sản xuất nơi cần đóng băng xương sống.
  Trung ngữ翻译:Flamingo đến Chameleon: đến năm 2024 nhiều đội chuyển sang sự kết hợp sớm (第 12.11 课);
- Sự nhập vào liên kết của Gemini: theo khái niệm thừa hưởng tính linh hoạt định dạng liên kết của Flamingo, mặc dù cơ chế chính xác là độc quyền.
  Trung ngữ翻译:Gemini 的交织输入:概念上继承了 Flamingo 的交织形式灵活性, mặc dù cơ chế cụ thể là chuyên nghiệp.

### So sánh với BLIP-2

| | BLIP-2 | Flamingo |
|---|---|---|
| / | BLIP-2 | Flamingo |
| Visual bridge | Q-Former once at input | Gated cross-attention at every M layers |
| 视觉桥接 | 输入层一次 Q-Former | 每 M 层一次门控交叉注意力 |
| Visual tokens | 32 per image | 64 per image per cross-attn layer |
| 视觉 token | 每图 32 个 | 每个交叉注意力层每图 64 个 |
| Frozen LLM | Yes | Yes |
| 冻结 LLM | 是 | 是 |
| Few-shot in-context | Weak | Strong — the paper's centerpiece |
| 少样本上下文学习 | 弱 | 强——论文的核心亮点 |
| Interleaved inputs | No native support | Yes, the design target |
| 交织输入 | 无原生支持 | 是，设计目标 |
| Training data | 130M pairs | 1.3B pairs + 43M interleaved pages |
| 训练数据 | 1.3 亿对 | 13 亿对 + 4300 万交织网页 |
| Parameter count | 188M trained | ~10B trained (cross-attn layers) |
| 参数量 | 训练 1.88 亿 | 训练约 100 亿（交叉注意力层） |
| Compute | Days on 8 A100s | Weeks on thousands of TPUv4 |
| 计算量 | 8 块 A100 数天 | 数千块 TPUv4 数周 |

Chọn BLIP-2 cho VQA hình ảnh đơn trên một ngân sách. Chọn Flamingo / Idefics2 cho lý luận hình ảnh liên kết, ít ảnh hoặc nhiều hình ảnh.

> 预算 giới hạn của đơn hình ảnh VQA  chọn BLIP-2──交织、少样本或多图像推理选 Flamingo/Idefics2──

## Hãy sử dụng nó để thực hiện
```figure
cross-attention-fusion
```

## Sử dụng nó

`code/main.py`chứng minh:

> `code/main.py`演示了:

1. Một thiết bị lấy mẫu lại Perceiver trên 36 mã thông báo vá giả với 8 dấu ẩn có thể học (trong Python tinh khiết).
   Trung文翻译:对36 个假补丁代币的感知器重样,使用8 个可学习潜在向量(纯 Python 交叉注意力)
2. Một bước đi quan tâm qua cửa với `alpha = 0`→ đầu ra bằng đầu vào (LLM không thay đổi), sau đó `alpha = 2.0`→ đóng góp thị giác trộn lẫn.
   Trung ngữ翻译:门控交叉注意力步骤,`alpha = 0`→ 输出等于输入(LLM 不变), rồi `alpha = 2.0`→ 视觉贡献混入──
3. Một nhà xây dựng mặt nạ nhộn nhịp tạo ra mặt nạ chú ý 2D cho chuỗi "(hình 1) (màn văn 1) (hình 2) (màn văn 2)".
   Trung văn翻译:交织掩码构建器,为"(图像 1) (文本 1) (图像 2) (文本 2)"序列生成 2D 注意力掩码。

## Chuyển nó đi.

Bài học này sẽ mang lại kết quả `outputs/skill-gated-bridge-diagnostic.md`. Với cấu hình của một VLM mở (sampleer Y/N, tần số giao tiếp chéo, hệ thống cổng), nó xác định các yếu tố dòng dõi Flamingo và giải thích chiến lược đóng băng. hữu ích để cố định lý do tại sao một bản chỉnh tinh tế suy giảm hiệu suất văn bản (câu trả lời: cổng đã quá rộng quá nhanh).

> 本课产 出 `outputs/skill-gated-bridge-diagnostic.md` Định định mở VLM cấu hình (có mẫu khác không, tỷ lệ tập trung tập trung, tỷ lệ kiểm soát), nó nhận ra Flamingo 血统元素并解释结策略.

## Tập luyện bài tập

1. Xét số tham số thị giác của Flamingo-9B: 9B LLM + 1.4B lớp quan tâm chéo được vạch + 64M resampler.
   Trung ngữ翻译:计算 Flamingo-9B 的视觉参数:9B LLM + 14亿门控交叉注意力层 + 6400万复制器――训练参数占总参数的比例是多少?

2. Thực hiện các phần còn lại bị khóa `y = tanh(alpha) * cross + x`Trong PyTorch.`alpha=0`- `y==x`chính xác ở init.
   中文翻译:用 PyTorch 实现门控残差 `y = tanh(alpha) * cross + x`❖ Bằng chứng thực nghiệm`alpha=0`时 `y==x`精确成立──

3. Đọc phần 3.2 (arXiv:2308.01390) của OpenFlamingo về cách xử lý nhiều hình ảnh trong một lô khi mỗi prompt có số hình ảnh khác nhau.
   Trung ngữ翻译:阅读 OpenFlamingo 第 3.2 节(arXiv:2308.01390) về cách xử lý từng số lượng hình ảnh trong mỗi số lượng hình ảnh khác nhau tình huống.

4. Tại sao mặt nạ thu hút sự chú ý của Flamingo cho phép một mã thông báo văn bản chỉ xem * hình ảnh gần đây nhất* trước đó chứ không phải tất cả hình ảnh trước đó?
   Trung ngữ翻译:为什么 Flamingo的交叉注意力掩码让文本代币只关注*最近的*前一张图像而不是所有的前序图像?阅读 Flamingo 论文第 2.4 节并解释权衡──

5. Trong bối cảnh vài lần chụp: xây dựng một lời nhắc với 4 ví dụ về "phức ảnh → màu của đối tượng chính" cho một biến thể Flamingo mới. Mô tả mô hình độ chính xác mong đợi khi bạn thay đổi số ví dụ từ 0 đến 8.
   Trung văn翻译:上下文少样本:构建包含 4 个"图像 → 主要对象颜色"示例的提示――描述示例数从0 变到8 时预期的准确率模式――

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|------------------------|---------|
| 术语 | 通俗说法 | 实际含义 | |
| Perceiver resampler | "Fixed-latent cross-attention" | Module that produces K fixed tokens from a variable number of input patches | 从可变数量输入 patch 产生 K 个固定 token 的模块 |
| Gated cross-attention | "Tanh-gated bridge" | Residual layer `y = tanh(alpha)*cross + x`, learnable alpha, init 0 | 残差层 `y = tanh(alpha)*cross + x`，可学习 alpha，初始化为 0 |
| Interleaved input | "Mixed sequence" | Prompt format with images and text mixed freely in reading order | 图像和文本按阅读顺序自由混合的提示格式 |
| Frozen LLM | "No LLM gradients" | The text LLM's weights do not update; only resampler + cross-attn layers train | 文本 LLM 权重不更新；仅 resampler + 交叉注意力层训练 |
| Few-shot | "In-context examples" | Give a few (image, answer) pairs in the prompt; model generalizes without finetuning | 在提示中给几个（图像，答案）对；模型无需微调即可泛化 |
| OBELICS | "Interleaved web corpus" | Open dataset of 141M web pages with images and text in reading order | 1.41 亿网页的开放数据集，包含按阅读顺序排列的图像和文本 |
| Chinchilla | "70B frozen base" | Flamingo's frozen text LLM, from DeepMind's Chinchilla paper | Flamingo 的冻结文本 LLM，来自 DeepMind 的 Chinchilla 论文 |
| Gate schedule | "How alpha moves" | The rate at which the cross-attention gate opens during training | 训练过程中交叉注意力门控打开的速率 |
| Cross-attn frequency | "Every M layers" | How often a gated cross-attention block is inserted; Flamingo uses M=4 | 门控交叉注意力块插入的频率；Flamingo 使用 M=4 |
| OpenFlamingo | "Open reproduction" | MosaicML/LAION open checkpoint at 3-9B; architecture-identical to Flamingo | MosaicML/LAION 的 3-9B 开放检查点；架构与 Flamingo 相同 |

## Xem thêm 延伸阅读

- [Alayrac et al. — Flamingo (arXiv:2204.14198)](https://arxiv.org/abs/2204.14198) giấy gốc.
  Trung ngữ翻译:Flamingo 原始论文。
- [Awadalla et al. — OpenFlamingo (arXiv:2308.01390)](https://arxiv.org/abs/2308.01390) sinh sản mở.
  Trung ngữ翻译:开放复现――
- [Laurençon et al. — OBELICS (arXiv:2306.16527)](https://arxiv.org/abs/2306.16527) các trang web được giao nhau.
  Trung ngữ翻译:交织网络语料库.
- [Jaegle et al. — Perceiver IO (arXiv:2107.14795)](https://arxiv.org/abs/2107.14795) kiến trúc Perceiver chung.
  Trung文翻译:通用 Perceiver 架构。
- [Li et al. — Otter (arXiv:2305.03726)](https://arxiv.org/abs/2305.03726)- Thủy sao Flamingo theo hướng dẫn.
  Trung ngữ翻译:指令微调的 Flamingo 后代。
- [Laurençon et al. — Idefics2 (arXiv:2405.02246)](https://arxiv.org/abs/2405.02246) đơn giản hóa hiện đại của cách tiếp cận Flamingo.
  Trung ngữ翻译:Flamingo 方法的现代化简化──
