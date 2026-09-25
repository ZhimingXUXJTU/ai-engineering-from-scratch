# Phong truyền: Text Autoregressive + Diffusion Image in One Transformer  Phong truyền: một Transformer 兼 tự quay lại văn bản và hình ảnh phát triển

> Chameleon và Emu3 đặt cược tất cả vào các token riêng biệt. Chúng hoạt động, nhưng nút thắt lượng tử được nhìn thấy  các nguyên bằng chất lượng hình ảnh dưới các mô hình phân tán không gian liên tục. Phong truyền (Meta, Zhou et al., tháng 8 năm 2024) đưa ra cược ngược lại: giữ hình ảnh liên tục, thả VQ-VAE hoàn toàn, và huấn luyện một bộ biến đổi với hai lỗ. Các mã thông báo văn bản có được dự đoán mã thông báo tiếp theo. Các bản vá hình ảnh có sự mất mát phù hợp dòng chảy / phân tán. Cả hai mục tiêu tối ưu hóa cùng một trọng lượng. Kiến trúc cơ bản của Stable Diffusion 3 (MMDiT) là một người anh em họ gần gũi. Bài học này đọc luận án Transfusion, xây dựng một đồ chơi huấn luyện hai lỗ, và theo dõi mặt nạ chú ý cho phép một biến đổi làm cả hai công việc.

> **【中文解读】**Transfusion(Meta,2024年8月) chọn cách tương phản với Chameleon/Emu3: giữ hình ảnh để tiếp tục biểu hiện, không cần VQ-VAE, sử dụng một Transformer đồng thời chạy hai lỗ văn bản token sử dụng một token 预测, hình ảnh sửa chữa sử dụng流匹配/扩散损失──Stable Diffusion 3 của MMDiT cấu trúc là gần gũi.

> **【拓展：双损失训练的工程挑战】**Điểm khó khăn cốt lõi của sự pha trộn nằm trong việc cân bằng hai hàm mất mát khác nhau ở hai thước đo số lượng. Sự khác biệt về mức độ mất mát của NTP và phát triển MSE có thể dẫn đến một bài tập dẫn đầu mất mát.

**Type:** Build  | **类型:** 构建
**Languages:** Python (stdlib, two-loss trainer on MNIST-scale toy) | **语言:** Python（标准库，MNIST 规模玩具的双损失训练器）
**Prerequisites:** Phase 12 · 11 (Chameleon), Phase 8 (Generative AI) | **前置知识:** Phase 12 · 11（Chameleon），Phase 8（生成式 AI）
**Time:** ~180 minutes | **时间:** ~180 分钟

>  **【前置】**学本节前请先掌握:Phase 12·11(Chameleon 离散代币) 、Phase 12·12(Emu3 next-token 生成) 、Phase 8·01-03(扩散模型 / Flow Matching) Transfusion = 两套思路的融合:文本离散 + 图像连续,一个变压器 两个损失──
>  **【类比】**Trânsfusion = "双拼户型"──Chameleon = 一居室(tất cả nội dung sử dụng cùng một token);LLaVA = 联排别(视觉和文本完全分开,靠桥接连接);Trânsfusion = 双拼(一边文本下一个代号损失,一边图像扩散损失,共享承重墙 = 同一个变压器骨干)──两个损失共同优化一套参数,保留各自模态的优势──
> ️ **【易错点】**Một lỗ dẫn tập luyện thường phổ biến MSE 数值大,文本 NTP bị lấp lánh) ――修复: dùng trọng lượng mất ((如 λ_text=1.0, λ_image=0.1) hoặc GradNorm 自适应平衡──

## Mục tiêu học tập

- Đưa một bộ biến đổi chạy hai lỗ (NTP trên mã thông báo văn bản, MSE phân tán trên các bản vá hình ảnh) trên một xương sống.
  > Xây dựng một Transformer có thể chạy trên cùng một xương rể trên hai lỗ hổng (NTP + 图像 patch 扩散 MSE)
- Giải thích tại sao sự chú ý hai chiều trên các bản vá hình ảnh cộng với sự chú ý nguyên nhân trên các mã thông báo văn bản là lựa chọn tốt nhất.
  > 解释 tại sao "phát hình ảnh 双向 + 文本代币因果" là sự lựa chọn ẩn giấu chính xác.
- So sánh Transfusion-style (hình ảnh liên tục, mất pha trộn) với Chameleon-style (hình ảnh riêng biệt, NTP) về tính toán, chất lượng và phức tạp của mã.
  > So sánh Transfusion 风格 (连续图像、扩散损失) với Chameleon 风格 (离散图像、NTP) trong tính năng, chất lượng và độ phức tạp của mã.
- Tên góp của MMDiT: trọng lượng cụ thể về phương thức tại mỗi khối, sự chú ý chung tại dòng dư thừa.
  > 列举 MMDiT's contributions: mô hình của mỗi khối đặc biệt trọng lượng, sự phân biệt dòng chảy

## Vấn đề  vấn đề nền

Cuộc tranh luận về các token hình ảnh phân biệt so với liên tục là lâu hơn LLM. Các đại diện liên tục (tốc số nguyên liệu, vAE laten) giữ lại chi tiết. Các token phân biệt (tốc số VQ) phù hợp với từ vựng bản địa của biến thể nhưng mất chi tiết ở bước định lượng.

> 离散与连续图像代币的争论比 LLM 更早──连续表示(原始像素、VAE 潜变量)保留细节──离散代币(VQ索引) phù hợp với bảng từ ngữ gốc của Transformer, nhưng trong quá trình định lượng hóa mất tích细节──

Chameleon / Emu3 đã đi riêng biệt: một lỗ, một kiến trúc, nhưng độ trung thành hình ảnh bị giới hạn bởi chất lượng tokenizer.

> Chameleon / Emu3 选择离散: một mất mát, một cấu trúc, nhưng độ bảo mật hình ảnh bị giới hạn trong phân từ 器质量──

Các mô hình phân tán tiếp tục: chất lượng hình ảnh đặc biệt, nhưng một mô hình riêng biệt với LLM, kỹ thuật lịch trình tiếng ồn phức tạp và không có sự tích hợp sạch với việc tạo văn bản.

> 扩散模型选择连续:卓越的图像质量, nhưng với LLM là mô hình độc lập, cần các công trình điều chỉnh tiếng ồn phức tạp, không thể kết hợp với văn bản để tạo ra sự tích hợp sạch.

Phong truyền hỏi: chúng ta có thể có cả hai? Giữ hình ảnh liên tục, vẫn tập một mô hình, sử dụng hai lỗ đeo vào một bước gradient.

> Phân truyền 问:能否兼得两者? giữ hình ảnh连续, vẫn huấn luyện một mô hình, sử dụng hai lỗ đòn拼接到一个梯度步中──

## Khái niệm cốt lõi

> **【中文解读】**TransFusion(Meta) sẽ tự quay trở lại mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô hình mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô mô

> **【拓展：多模态训练目标的融合】**TransFusion  chứng minh tự quay trở và phát triển có thể tồn tại trong cùng một mô hình và cộng đồng.


### Kiến trúc hai lỗ

Một bộ biến đổi chỉ có bộ giải mã đơn xử lý một chuỗi chứa:

> 单一解码器 Transformer 处理 chứa các chuỗi nội dung sau:

- Các mã thông báo văn bản (tạm dịch: discrete, từ từ ngữ BPE).
  中文翻译:文本 token(离散, 来自 BPE 词汇表)
- Các bản vá hình ảnh ( liên tục, các khối pixel 16x16 được chiếu vào mờ ẩn thông qua nhúng tuyến tính  giống như đầu vào của một bộ mã hóa ViT).
  Trung文翻译:图像补丁(连续,16x16 像素块通过线性嵌入投影到隐藏维度与ViT 编码器输入相同) ⋅
- `<image>`và `</image>`Đánh dấu nơi các bản vá liên tục sống.
  Trung ngữ翻译:`<image>`和 `</image>`标签标记连续补丁的位置──

Thêm vào đó, số tiền của các đầu được chọn là 1 trong hai đầu cho mỗi token:

> 前向传播运行一次──损失为每代币 选择两个头条之一:

- Đối với các mã thông báo văn bản: trúng trúng chuẩn trên đầu từ ngữ-logits.
  Trung文翻译:文本代号:词汇表 logits 头上的标准交叉──
- Đối với các bản vá hình ảnh: mất độ phân tán trên các bản vá liên tục  dự đoán tiếng ồn được thêm vào mỗi bản vá.
  Trung文翻译:图像补丁:连续补丁 上的扩散损失预测 每个补丁 添加的噪音──

Các gradient chảy qua cơ thể biến đổi chia sẻ.

> 梯度通过共享的变压器 体回流――两个损失同时改进共享权重――

### Mặt nạ chú ý: văn bản nguyên nhân + hình ảnh hai chiều

Các mã thông báo văn bản phải là nguyên nhân  bạn không thể để một mã thông báo văn bản tham gia vào văn bản trong tương lai, hoặc giáo viên buộc phải nghỉ ngơi.

> 文本代币 必须是因果的不能让文本代币 关注未来文本,否则老师强制会失败――但图像补丁代表一个快照;它们应该在同一图像块内双向关注彼此――

Mặt nạ:

> 掩码:

```
M[i, j] = 1 if:
  (i is text and j is text and j <= i)   # causal for text
  OR (i is image and j is image and same_image_block(i, j))   # bidirectional within image
  OR (i is text and j is image and j < i_image_end)   # text attends to previous images
  OR (i is image and j is text and j < i_image_start)   # image attends to preceding text
```

Được triển khai như một mặt nạ khối-lục hình ba trong đào tạo và suy luận.

> Trong việc tập luyện và suy nghĩ, thực hiện cho khối trí góc ẩn码.

### Thiếu luồng trong biến thể

Thiếu độ phân tán là tiêu chuẩn: thêm tiếng ồn vào một bộ vá hình ảnh, yêu cầu mô hình dự đoán tiếng ồn (hoặc bộ vá sạch, tương đương). Phiên bản truyền sử dụng tương thích dòng chảy  dự đoán trường tốc độ từ tiếng ồn đến sạch.

> 扩散损失是标准的: cho một bản vá hình ảnh 添加噪音,让模型预测噪音(或等价地预测干净补丁) ――Transfusion 版本使用流匹配预测从噪音到干净的速度场――

Trong quá trình đào tạo:
1. Đối với mỗi bản vá hình ảnh x0, lấy mẫu bước thời gian ngẫu nhiên t.
   Trung文翻译:对每个图像补丁 x0,采样随机时间步 t。
2. Phản ứng âm thanh mẫu ε, tính xt = (1-t) * x0 + t * ε (sự phân cực tuyến tính để phù hợp dòng chảy).
   Trung文翻译:采样噪声 ε,计算 xt = (1-t) * x0 + t * ε(流匹配的线性插值)
3. Bộ biến đổi dự đoán v_theta(xt, t); mất mát = MSE(v_theta(xt, t), ε - x0).
   Trung文翻译:Transformer 预测 v_theta(xt, t);损失 = MSE(v_theta(xt, t), ε - x0)。
4. Backprop cùng với text NTP mất từ cùng một chuỗi.
   Trung văn: 翻译:与同序列的文本 NTP 损失一起反向传播──

Theo kết luận, thế hệ là:
- Các mã thông báo văn bản: lấy mẫu tự rút tiêu chuẩn.
  Trung ngữ翻译:文本代号:标准自归采样。
- Các bản vá hình ảnh: vòng lấy mẫu phân tán (10-30 bước điển hình) được điều chỉnh trên các token văn bản trước đó.
  Trung ngữ翻译:图像补丁:以先前文本代号 为条件的扩散采样循环(通常10-30步) ⋅

### MMDiT: biến thể của Stable Diffusion 3

Stable Diffusion 3 (Esser et al., tháng 3 năm 2024) đã vận chuyển MMDiT (Multimodal Diffusion Transformer) vào khoảng thời gian tương tự như Transfusion.

> Stable Diffusion 3 (Esser 等人,2024 年 3 月) đã phát hành MMDiT (多模态扩散变压器), với Transfusion 差不多同时──两者架构是兄弟──

Sự khác biệt chính của MMDiT:

> MMDiT's Key区别:

- Các khối chuyển đổi có trọng lượng Q, K, V và MLP riêng biệt cho các mã thông báo văn bản so với các bản vá hình ảnh.
  Trung ngữ翻译: mỗi khối có mô hình cụ thể có trọng lượng riêng biệt. Mỗi khối Transformer có mã bản văn bản độc lập với các bản vá hình ảnh của Q、K、V và MLP.
- Một biến thể phù hợp với dòng chảy cụ thể với việc lấy mẫu được biết đến và toán học đơn giản hơn DDPM.
  Trung ngữ翻译:整流流训练──一种特定流匹配变体,采样已知,数学比DDPM 更简单──
- Scale. MMDiT là xương sống cho SD3 (2B và 8B biến số param).
  Trung ngữ翻译:规模──MMDiT 是 SD3 的主干(20亿和80亿参数变体)──Transfusion 论文扩展到70亿──

Cả hai đều hội tụ về cùng một ý tưởng cốt lõi: một biến thể chạy NTP trên văn bản và phân tán trên các đại diện hình ảnh liên tục.

> 两者收到同一核心理念: một Transformer 在文本上运行NTP, 在连续图像表示上运行扩散──

### Tại sao điều này vượt qua phong cách của Chameleon

Khoảng cách chất lượng giữa phát sóng liên tục và NTP phân biệt trong việc tạo hình ảnh có thể đo lường.

>  liên tục lan rộng và phân tán NTP trong hình ảnh tạo ra sự khác biệt chất lượng là có thể định lượng.

- Ở 7B, nó vượt qua mô hình kiểu Chameleon cùng kích thước trên FID với 3-5 điểm.
  Trung文翻译:70亿参数下,FID 上击败同规模的马风格模型 3-5 分──
- Không cần đào tạo tokeniser  mã hóa hình ảnh đơn giản hơn (động chiếu tuyến tính đến ẩn, giống như lớp đầu vào của ViT).
  Trung ngữ翻译:不需要分词器训练图像编码器更简单(线性投影到隐藏层,与ViT 输入层相同)
- Inference có thể song song với việc xác định các bản vá hình ảnh, không giống như các mã thông báo hình ảnh tự rút.
  Trung ngữ翻译:推理可以并行化图像补丁 去噪音, khác với tự quay lại hình ảnh token。

Nhược điểm: Phân truyền là mô hình mất kép, làm cho động lực đào tạo khó khăn hơn. Nặng giảm cần điều chỉnh. Sự không phù hợp lịch trình giữa NTP và sự pha trộn có thể khiến một đầu thống trị.

> 缺点:Transfusion là mô hình mất mát hai, tập động thái phức tạp hơn.

### Những gì nằm bên dưới dòng chảy

Janus-Pro (Dạy 12.15) tinh chỉnh ý tưởng của Transfusion bằng cách tách lập mã hình ảnh để hiểu và tạo ra SigLIP cho một, VQ cho một  trong khi chia sẻ cơ thể biến đổi. Show-o (Dạy 12.14) thay đổi phân tán cho phân tán riêng biệt (bản đoán đeo mặt nạ).

> Janus-Pro (第 12.15 课) thông qua giải thích 视觉编码器 cải tiến ý tưởng của Transfusion SigLIP được sử dụng để hiểu, VQ được sử dụng để tạo ra  đồng thời chia sẻ Transformer 主体──Show-o (第 12.14 课) sẽ lan rộng thay vì lan rộng (离散) 掩码预测 (掩码预测) ──统一生成家族在 Transfusion 后迅速分化──

2026 sản xuất VLM phát ra hình ảnh  Gemini 3 Pro, GPT-5, Claude Opus 4.7 của hình ảnh tạo đường  gần như chắc chắn sử dụng một số hậu duệ của gia đình này. chi tiết là độc quyền.

> 2026 năm sản xuất hình ảnh VLMGemini 3 Pro、GPT-5、Claude Opus 4.7 hình ảnh sản xuất đường lối gần như có thể xác định sử dụng một số thế hệ sau của gia đình này.


> **【拓展：TransFusion 的推理过程】**TransFusion  Chuyên tắc quan trọng trong quá trình phát triển: mã hóa văn bản tự tái tạo, gặp hình ảnh bắt đầu đánh dấu khi chuyển sang mô hình mở rộng.


## Hãy dùng nó để thực hành
```figure
cfg-guidance-scale
```

## Sử dụng nó

`code/main.py`xây dựng một đồ chơi Transfusion trên một vấn đề nhỏ như MNIST:

> `code/main.py`Trong các vấn đề MNIST mô hình nhỏ xây dựng đồ chơi Phong trào:

- Các tiêu đề văn bản là chuỗi số nguyên ngắn mô tả một con số (0-9).
  Trung ngữ翻译:文本描述是描述数字(0-9) 的短整数序列──
- Hình ảnh là 4x4 lưới của các byte.
  Trung文翻译:图像是4x4 字节网格。
- Một cặp dự đoán tuyến tính chia sẻ trọng lượng hoạt động như là bộ thay thế biến đổi; mất NTP trên văn bản, mất MSE trên các bản vá âm thanh.
  Trung ngữ翻译:一对共享权重的线性投影作为变压器 替代;文本用NTP 损失,噪音补丁用MSE 损失──
- Chuyện tập trung thay đổi hai lỗ, mặt nạ chú ý là rõ ràng.
  Trung ngữ翻译: tập trung vòng tròn thay đổi hai lỗ, chú ý ẩn chứa là rõ ràng.
- Thế hệ tạo ra một dòng chữ và hình ảnh 4x4 trong một đoạn đi trước.
  Trung文翻译:生成在一次前向传播中产生文描述和 4x4 图像──

Bộ biến đổi là một đồ chơi. Phòng ống nước mất hai lỗ, xây dựng mặt nạ chú ý, và vòng suy luận là những đồ tạo vật thực sự.

> Chuyển đổi là một loại đồ chơi.

## Đưa nó lên mạng

Bài học này sẽ mang lại kết quả `outputs/skill-two-loss-trainer-designer.md`Với một nhiệm vụ đào tạo đa phương thức mới (text + image, text + audio, text + video), nó thiết kế lịch trình hai lỗ (sự giảm trọng lượng, hình dạng mặt nạ, chia sẻ so với các khối cụ thể về phương thức) và đánh dấu rủi ro thực hiện.

> 本课产 出 `outputs/skill-two-loss-trainer-designer.md`◊ Đặt nhiệm vụ đào tạo nhiều hình thức mới (文本+图像、文本+音频、文本+视频), nó thiết kế hai mất mát điều chỉnh (重损、掩码形状、共享 vs 模态特定块) và đánh dấu thực hiện风险──

## Tập luyện bài tập

1. Một mô hình kiểu Transfusion đào tạo 70% mã thông báo văn bản và 30% các bản vá hình ảnh.
   Trung ngữ翻译:Transfusion 风格模型训练 70% 文本代币 和 30% 图像补丁──图像扩散损失在量级上约为文本NTP损失的10倍──什么损失权重能平衡它们?

2. Thực hiện mặt nạ khối-lòng ba góc cho một chuỗi: `[T, T, <image>, P, P, P, P, </image>, T]`Đánh dấu mỗi mục 0 hoặc 1.
   中文翻译:为序列 `[T, T, <image>, P, P, P, P, </image>, T]`实现块三角掩码──标记每个条目为0或1──

3. MMDiT có trọng lượng QKV cụ thể về phương thức.
   Trung ngữ翻译:MMDiT 有模态特定QKV权重――相比Transfusion的全共享变压器 增加了多少参数?70亿参数下值吗?

4. Tạo: được đưa ra một lời nhắc văn bản, mô hình chạy NTP cho 50 token, sau đó nhấn `<image>`, sau đó chạy truyền trên 256 đệm trên 20 bước denoise.
   Trung ngữ翻译:生成:给定文本提示,模型运行 NTP 50 个代币,然后遇到 `<image>`, rồi trong 256 đệm lên chạy 20 bước để phát tán tiếng ồn.

5. Đọc bài báo SD3 Phần 3. Mô tả dòng chảy được chỉnh sửa và lý do tại sao nó hội tụ trong ít bước suy luận hơn DDPM.
   Trung ngữ翻译:阅读 SD3 论文第 3 节──描述整流流以及为什么它比DDPM在更少推理步骤中收──

## Từ khóa  Keyword

| Term | What people say | What it actually means | 中文含义 | 中文释义 |
|------|-----------------|------------------------|---------|
| Two-loss training | "NTP + diffusion" | A single transformer optimizes both cross-entropy on text tokens and MSE on continuous image patches in the same gradient step | 单一 Transformer 在同一梯度步中优化文本 token 交叉熵和连续图像 patch MSE |
| Flow matching | "Rectified flow" | Diffusion variant that predicts a velocity field from noise to clean data; simpler math than DDPM | 预测从噪声到干净数据速度场的扩散变体；数学比 DDPM 更简单 |
| MMDiT | "Multimodal DiT" | Stable Diffusion 3's architecture: joint attention, modality-specific MLPs and norms | SD3 架构：联合注意力、模态特定 MLP 和归一化 |
| Block-triangular mask | "Causal text + bidirectional image" | Attention mask that is causal across text but bidirectional within image regions | 文本因果、图像区域内双向的注意力掩码 |
| Continuous image representation | "No VQ" | Image patches as real-valued vectors, not integer codebook indices | 图像 patch 为实值向量，非整数码本索引 |
| Velocity prediction | "v-parameterization" | Network output is the velocity field between noise and data, not the noise itself | 网络输出为噪声和数据之间的速度场，非噪声本身 |

## Xem thêm 延伸阅读

- [Zhou et al. — Transfusion (arXiv:2408.11039)](https://arxiv.org/abs/2408.11039)
  Trung文翻译:Transfusion 论文。
- [Esser et al. — Stable Diffusion 3 / MMDiT (arXiv:2403.03206)](https://arxiv.org/abs/2403.03206)
  中文翻译:Stable Diffusion 3 / MMDiT 论文。
- [Peebles & Xie — DiT (arXiv:2212.09748)](https://arxiv.org/abs/2212.09748)
  Trung văn翻译:DiT 扩散 Transformer 论文。
- [Zhao et al. — MonoFormer (arXiv:2409.16280)](https://arxiv.org/abs/2409.16280)
  中文翻译:MonoFormer 论文。
- [Xie et al. — Show-o (arXiv:2408.12528)](https://arxiv.org/abs/2408.12528)
  Trung văn翻译:Show-o 论文。
