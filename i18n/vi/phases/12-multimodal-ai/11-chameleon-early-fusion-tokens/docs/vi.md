# Chameleon và Early-Fusion Token-Only Multimodal Models  Chameleon 早期融合纯代币多模态模型

> Mỗi VLM mà chúng ta đã thấy cho đến nay giữ hình ảnh và văn bản riêng biệt. Các token hình ảnh đến từ một bộ mã hóa thị giác, chảy vào một máy chiếu, sau đó gặp văn bản bên trong LLM. Từ vựng của tầm nhìn và văn bản không bao giờ chồng chéo. Chameleon (Meta, tháng 5 năm 2024) hỏi: nếu họ làm thế thì sao? Trình luyện một VQ-VAE biến hình thành một chuỗi các token riêng biệt từ một từ vựng chung. Mỗi tài liệu đa phương thức hiện là một chuỗi mã thông báo văn bản và mã thông báo hình ảnh được giao nhau, một lỗ tự động. Hiệu ứng phụ: mô hình có thể tạo ra các đầu ra hỗn hợp  mã thông báo văn bản và hình ảnh thay thế trong một cuộc gọi suy luận duy nhất. Bài học này đọc luận án early-fusion và xây dựng một phiên bản đồ chơi cuối cùng.

> **【中文解读】**Chameleon (Meta,2024年5月) đề xuất một cách thức đa mô hình cực đoan: sử dụng VQ-VAE để chuyển hình ảnh thành mã thông báo phân tán, chia sẻ cùng một bảng từ ngữ, sử dụng một bài tập tự quay lại bị mất trí tuệ.

> **【拓展：早期融合 vs 后期融合】**Trước tất cả VLM (LLaVA, BLIP-2, Qwen-VL) đều giữ hình ảnh và văn bản phân chia. "Thiết hợp sớm" của Chameleon có nghĩa là hình ảnh và văn bản từ đầu được xử lý trong cùng một không gian, mô hình có thể tự nhiên thay thế với các mô hình và văn bản.

**Type:** Build  | **类型:** 构建
**Languages:** Python (stdlib, VQ-VAE tokenizer + interleaved decoder) | **语言:** Python（标准库，VQ-VAE tokenizer + 交织解码器）
**Prerequisites:** Phase 12 · 05, Phase 8 (Generative AI) | **前置知识:** Phase 12 · 05，Phase 8（生成式 AI）
**Time:** ~180 minutes | **时间:** ~180 分钟

>  **【前置】**学本节前请先掌握:Phase 12·05(LLaVA 后期融合方案) 、Phase 8(VQ-VAE 离散表示) 、Phase 7(Tranformator next-token 训练) ⋅Chameleon là "反 LLaVA" ở một cực khác: tất cả các mô hình đều sử dụng next-token loss。
>  **【类比】**Chameleon = "WORLD语"――LLaVA = 翻译机;;视觉编码器把图片翻译成LLM 能懂的语言);Chameleon = 世界语;;图片和文本都用同一种人造语言,模型不用翻译) ・・・ World语的好处是模型可以无交换生成文本和图片;坏处是每种模态必须分离化(VQ-VAE 给图片"造词"),信息损失大──

## Mục tiêu học tập

- Giải thích lý do tại sao một từ vựng chung + mất một lần thay đổi những gì mô hình có thể làm.
  > 解释为什么共享词汇表 + 单一损失能改变模型能力──
- Mô tả cách một VQ-VAE biểu tượng hóa một hình ảnh thành một chuỗi riêng biệt tương thích với mục tiêu biểu tượng tiếp theo của một biến thể.
  > 描述 VQ-VAE 如何将图像分词为与变压器 下一代币 目标兼容的离散序列──
- Tên các thủ thuật huấn luyện ổn định của Chameleon: QK-Norm, đặt hàng bỏ học, LayerNorm đặt hàng.
  > 列举 Chameleon's training稳定性技巧:QK-Norm、Dropout 位置、LayerNorm 顺序。
- So sánh cách tiếp cận Q-Former của Chameleon vs BLIP-2 và mô tả khi nào là lựa chọn đúng.
  > So sánh các chương trình Q-Former của Chameleon với BLIP-2, mô tả các tình huống thích hợp của riêng mình.

## Vấn đề  vấn đề nền

VLM dựa trên bộ điều chỉnh (LLaVA, BLIP-2, Qwen-VL) xử lý văn bản và hình ảnh như hai thứ khác nhau.`embed(text_token)`Một hình ảnh đi qua `visual_encoder(image) → projector → ... pseudo_tokens`Mô hình có hai đường lối nhập mà hợp nhất một phần trong.

> 适配器式 VLM(LLaVA、BLIP-2、Qwen-VL) sẽ văn bản và hình ảnh được xem như hai loại khác nhau.`embed(text_token)`; hình ảnh qua `visual_encoder(image) → projector → ... pseudo_tokens`◊ mô hình có hai đường nhập trong giữa hợp hợp.

Ba hậu quả:

> 3 hậu quả:

1. LLM chỉ có thể tiêu thụ hình ảnh, không phát ra chúng.
   Trung ngữ翻译:LLM 只能消费图像,不能生成图像──输出只能是文本──
2. Các tài liệu có tính cách hỗn hợp (làm thay đổi các đoạn văn và hình ảnh, như trong một bài viết) là khó khăn  bạn hoặc phân tích đầu vào đa phương thức bên ngoài mô hình hoặc các thế hệ chuỗi.
   Trung ngữ翻译:混合模态文档(段落和图像交替,如文章) 很别扭你要么在模型外解析多模态输入,要么链式生成──
3. Sự không phù hợp phân phối. Các token hình ảnh và các token văn bản sống ở các khu vực khác nhau của không gian ẩn, tạo ra các vấn đề sắp xếp tinh tế.
   Trung ngữ翻译:分布不匹配──视觉代号和文本代号 位于隐藏空间的不同区域,造成微妙的对齐问题──

Chameleon bác bỏ giả định: hình ảnh chỉ là chuỗi các token riêng biệt từ một từ vựng chung. Tập mô hình trên các tài liệu được giao lưu, một lỗ, một máy giải mã tự động, và bạn mở khóa việc tạo các chế độ hỗn hợp miễn phí.

> Chameleon  từ chối giả định này: hình ảnh chỉ là một chuỗi các token chia sẻ từ ngữ表中离散.

## Khái niệm cốt lõi

> **【中文解读】**Chameleon (Meta) sử dụng chiến lược kết hợp sớm: hình ảnh và văn bản đều phân tán thành một chuỗi mã thông báo, sử dụng cùng một Transformer xử lý.

> **【拓展：早期融合 vs 晚期融合】**早期融合 (Chameleon) sẽ có nhiều mô hình thống nhất đến cùng một biểu tượng không gian, lý thuyết tốt hơn nhưng chi phí đào tạo cao hơn.


### VQ-VAE như là tokenizer hình ảnh

Tokenizer là một bộ mã hóa tự động biến thể theo phương thức vector.

> 分词器 là một 量化变分自编码器.

- Mã hóa: CNN + ViT mà lập bản đồ hình ảnh cho một bản đồ tính năng không gian, nói 32x32 tính năng của dim 256.
  Trung ngữ翻译:编码器:CNN + ViT sẽ hiển thị hình ảnh cho các đặc điểm không gian, ví dụ như 32x32 个维度为 256 个特征.
- Codebook: một từ vựng được học của các vector K (Chameleon sử dụng 8192), cũng là dim 256.
  Trung文翻译:码本:K 个学习向量的词汇表(Chameleon 使用 8192 个), cũng là 256 维──
- Quantization: cho mỗi tính năng không gian, tìm kiếm mục codebook gần nhất bằng khoảng cách L2. Thay thế tính năng liên tục bằng chỉ số nguyên.
  Trung文翻译:量化: đối với mỗi đặc điểm không gian, sử dụng L2 距离查找最近的码本条目──用整数索引替换连续特征──
- Bộ giải mã: CNN đưa các tính năng lượng tử trở lại các pixel.
  Trung ngữ翻译:解码器:CNN sẽ định lượng tính năng tái tạo thành hình ảnh.

Việc đào tạo: VAE tái tạo mất + mất cam kết + mất sổ sách code.

> 训练:VAE 重建损失 + 承诺损失 + 码本损失──码本索引构成图像的离散字母表──

Đối với Chameleon: một hình ảnh trở thành 32 * 32 = 1024 token được rút ra từ một từ vựng của 8192.

> Đối với Chameleon: 一张图像变成32*32 = 1024 个代币, 来自8192 的词汇表――与文本代币( 来自LLM 的 BPE 词汇表,如32000)拼接──最终词汇表:40192──Transformer 见一个序列,一个损失──

### Thuật ngữ chung

Từ vựng của Chameleon kết hợp mã thông báo văn bản, mã thông báo hình ảnh và phân chia phương thức. Mỗi mã thông báo có một ID duy nhất. Lớp nhúng đầu vào lập bản đồ mỗi ID cho một vector ẩn D-dim. Bản đồ chiếu đầu ra ẩn lại cho logit từ vựng. Softmax chọn mã thông báo tiếp theo, bất kể phương thức nào.

> Chameleon's từ ngữ bảng kết hợp văn bản token、图像 token 和模态分隔符── mỗi token có một ID duy nhất── nhập vào lớp nhúng sẽ mỗi ID 映射到 D 维隐藏向量──输出投影将隐藏向量映射回 từ ngữ bảng logits──Softmax 选择下一个 token,无论什么模态──

Các bộ phân tách quan trọng: `<image>`và `</image>`Tags bracket chuỗi mã hóa hình ảnh.`<image>`, phần mềm dòng chảy biết 1024 token tiếp theo là chỉ số VQ để gửi đến decoder cho rendering pixel.

> 分隔符 rất quan trọng:`<image>`和 `</image>`标签包裹图像代币 序列──生成时,如果模型输出 `<image>`, Download software đã biết 1024 token tiếp theo là VQ chỉ mục, cần phải gửi cho máy giải mã để thực hiện hình ảnh 染.

### Sản xuất hỗn hợp

Inference là dự đoán mã thông báo tiếp theo trong từ vựng chung. Ví dụ: "Hãy vẽ một con mèo và mô tả nó". Chameleon phát ra:

> 推理是共享词汇表中的下一代标语 预测。 ví dụ提示:"画一只猫并描述它──"Chameleon 输出:

```
<image> 4821 1029 2891 ... (1024 image tokens) </image>
The cat is orange, sitting on a windowsill...
```

Mô hình chọn thứ tự tự động  nó có thể tạo ra hình ảnh sau văn bản, văn bản sau hình ảnh, hoặc chia sẻ.

> Mô hình tự chọn thứ tự  có thể trước hình ảnh 后文本 后文本 后文本 后图像, hoặc trao đổi输出 

So sánh với các máy điều chỉnh VLM nơi việc tạo chỉ có văn bản. Chameleon mở lại câu hỏi về các phương thức sản xuất mô hình.

> Chuyện này đã được giải quyết bởi các nhà nghiên cứu.

### Sự ổn định đào tạo  QK-Norm, bỏ cuộc, LayerNorm đặt hàng

Việc đào tạo với sự hợp nhất sớm là không ổn định về quy mô.

> 早期融合训练大规模时不稳定――Chameleon 论文 ghi lại ba kỹ thuật:

- QK-Norm. Sử dụng LayerNorm cho truy vấn và dự đoán chính bên trong sự chú ý, trước khi sản phẩm chấm. ngăn chặn vụ nổ độ lớn logit ở độ sâu. Được sử dụng bởi nhiều mô hình lớn sau năm 2024.
  Trung文翻译:QK-Norm──在注意力内部的查询 和关键 投影上应用 LayerNorm,在点积之前──防止深度上的逻辑幅度爆炸──被多个2024年后的大模型使用──
- Đặt bỏ. bỏ bỏ sau mỗi phần dư thêm, không chỉ sau sự chú ý và MLP. cần phải có sự điều chỉnh hơn khi gradient từ các token hình ảnh có thể thống trị.
  Trung ngữ翻译:Droput 位置──在每次残差加法后放 Dropout,不仅是注意力和MLP 后──当图像代币的梯度可能主导时需要更多正则化──
- LayerNorm sắp xếp. Pre-LN trên chi nhánh còn lại (thực lệ), cộng thêm một LN thêm trên kết nối skip của khối cuối cùng.
  Trung文翻译:LayerNorm 顺序──残差分支上的 Pre-LN(标准做法),加上最后一个块跳连接上的额外LN──稳定最后一层的梯度流──

Không có những thủ thuật này, huấn luyện 34B-param Chameleon đã đi ngược tại nhiều điểm kiểm soát. Với họ, nó hội tụ.

> Không có những kỹ thuật này, 340 tỷ thành phần của Chameleon được đào tạo tại nhiều điểm kiểm tra và phát triển.

### Trần nhà tái tạo của tokeniser

VQ-VAE là lỗ hổng. Với 8192 mục codebook và 1024 token mỗi hình ảnh 512x512, tái tạo PSNR là khoảng 26-28 dB.

> VQ-VAE là có tổn thất. 8192 个码本条目和每张 512x512 图像 1024 个代币, tái tạo PSNR lên giới hạn khoảng 26-28 dB.

Tokenizer là nút thắt. Tokenizer tốt hơn (MAGVIT-v2, IBQ, SBER-MoVQGAN) nâng trần. Emu3 (Dạy 12.12) đạt được sản xuất chất lượng SDXL thông qua một tokenizer tốt hơn một mình.

> 分词器是瓶──更好的分词器(MAGVIT-v2、IBQ、SBER-MoVQGAN) có thể nâng cao giới hạn trên.

### Chameleon vs BLIP-2 / LLaVA

Chameleon (sự hợp nhất sớm, từ ngữ chung):
- Một lỗ, một decoder.
  Trung ngữ翻译:一个损失,一个解码器――
- Tạo ra sản lượng hỗn hợp.
  Trung文翻译:生成混合模态输出。
- Tokenizer là trần chất lượng.
  Trung ngữ翻译:分词器是质量上限──
- Chi phí: VQ-VAE decoder cho mỗi hình ảnh được tạo trên đường suy luận.
  Trung文翻译:昂贵:推理路径上每张生成图像都需要VQ-VAE 解码器──

BLIP-2 / LLaVA (trộn hợp nhất, tháp riêng biệt):
- Nhìn vào, chỉ gửi tin nhắn.
  Trung văn翻译:视觉输入,仅文本输出──
- Sử dụng lại bằng LLM trước khi được đào tạo.
  Trung文翻译:复用预训练 LLM。
- Không có nút thắt để hiểu.
  Trung ngữ翻译:理解没有分词器瓶──
- Giá rẻ: một lần đi trước.
  Trung文翻译:便宜:单次前向传播。

Nếu bạn cần tạo hình ảnh, gia đình Chameleon, nếu bạn chỉ cần hiểu, adapter-VLM đơn giản hơn và sử dụng lại tính toán được đào tạo trước.

> Nếu cần hình ảnh, chọn Chameleon 系列. Nếu chỉ cần hiểu, thích ứng VLM hơn đơn giản và sử dụng nhiều hơn.

### Fuyu và AnyGPT

Fuyu (Adept, 2023) là một cách tiếp cận tương tự: bỏ qua bộ mã hóa thị giác riêng biệt hoàn toàn, cho các bản vá hình ảnh thô thông qua dự đoán đầu vào của LLM như thể chúng là token, không có tokeniser. đơn giản hơn Chameleon, mất sản xuất phát ra từ ngữ chia sẻ.

> Fuyu(Adept,2023) là một phương pháp liên quan: hoàn toàn nhảy qua độc lập của bộ viền biên tập, sẽ được tạo ra một bản vá hình ảnh nguyên thủy thông qua LLM của nhập chiếu, như chúng là biểu tượng, không có phân từ.

AnyGPT (Zhan et al., 2024) mở rộng Chameleon cho bốn phương pháp: văn bản, hình ảnh, nói, âm nhạc.

> AnyGPT(Zhan 等人,2024) sẽ mở rộng Chameleon thành bốn mô hình: văn văn, hình ảnh, ngữ音, âm nhạc, mỗi mô hình sử dụng các kỹ thuật VQ-VAE tương tự, chia sẻ Transformer, tùy ý đến tùy ý tạo ra.


> **【拓展：早期融合的训练挑战】**早期融合需要将图像和文本统一分散化,对图像代币器的质量要求极高――Meta 的马勒翁使用8192 码本的VQGAN,在 ImageNet重建质量(rFID 约 5.0) và文本兼容性之间做精心衡量――


## Hãy dùng nó để thực hành
```figure
vq-codebook
```

## Sử dụng nó

`code/main.py`xây dựng mô hình sáp nhập sớm đồ chơi từ đầu đến cuối:

> `code/main.py`Construction một mô hình kết hợp đầu đầu đầu của đồ chơi:

- Một máy định lượng kiểu VQ-VAE nhỏ xíu, lập bản đồ 8x8 bản vá cho chỉ số codebook (K=16).
  Trung文翻译: một mô hình nhỏ VQ-VAE 风格的量化器,将 8x8 patch 映射到码本索引(K=16)。
- Một từ vựng chung của (tác giả văn bản 0..31) + (tác giả hình ảnh 32..47) + (những phân chia 48, 49).
  Trung文翻译:共享词汇表(文本 id 0..31) +(图像 id 32..47) +(分隔符 48, 49)。
- Một máy giải trí tự động (bảng hình lớn) được đào tạo trên các tiêu đề tổng hợp + chuỗi mã hình ảnh.
  Trung文翻译:一个玩具自归归解码器 (一个玩具自归归解码器), trong tổng hợp mô tả + 图像代币 序列上训练──
- Phòng lấy mẫu phát ra các mã thông báo văn bản + hình ảnh thay thế khi được yêu cầu.
  Trung văn翻译:采样循环,给定提示后输出交换的文本 + 图像代币──

Mã cố tình giữ cho bộ biến đổi nhỏ (những chữ cái lớn) để bạn có thể theo dõi dòng tín hiệu từ đầu đến cuối.

> 代码故意将 Transformer 保持得非常小(二元组), để bạn có thể từ đầu đến cuối theo dõi tín hiệu.

## Đưa nó lên mạng

Bài học này sẽ mang lại kết quả `outputs/skill-tokenizer-vs-adapter-picker.md`. Với một đặc điểm sản phẩm (được hiểu chỉ với hiểu + tạo, chất lượng hình ảnh cần thiết, ngân sách chi phí), nó chọn giữa gia đình Chameleon (sự hợp nhất sớm) và gia đình LLaVA (sự hợp nhất muộn) và biện minh bằng các quy tắc số lượng.

> 本课产 出 `outputs/skill-tokenizer-vs-adapter-picker.md` Giữ định sản phẩm quy mô (仅理解 vs.理解+生成、所需图像质量、成本预算), nó được lựa chọn giữa chuỗi Chameleon 早期融合) và chuỗi LLaVA 晚期融合) và được sử dụng quy mô kinh nghiệm để tiến hành luận.

## Tập luyện bài tập

1. Chameleon sử dụng K=8192 codebook và 1024 token cho mỗi hình ảnh 512x512 . ước tính tỷ lệ nén so với hình ảnh RGB 24 bit.
   Trung文翻译:Chameleon 使用 K=8192 个码本条目和每张 512x512 图像 1024 个代币――估算对24位 RGB 图像的压缩比──有损吗?损失多少?

2. Một hình ảnh 4K (3840x2160) với cùng mật độ VQ-VAE tạo ra bao nhiêu mã thông báo hình ảnh? Một mô hình kiểu Chameleon có thể tạo ra một hình ảnh 4K trong một cuộc gọi suy luận? Điều gì phá vỡ đầu tiên  ngữ cảnh, chất lượng tokeniser, hoặc cache KV?
   Trung ngữ翻译:4K 图像(3840x2160) tạo ra bao nhiêu mã hình ảnh dưới cùng độ dày đặc VQ-VAE? mô hình phong cách chameleon có thể một lần suy luận điều chỉnh để tạo ra 4K 图像 không?

3. Thực hiện QK-Norm trong Python tinh khiết. Với truy vấn và khóa 64-dim, hiển thị sản phẩm điểm trước và sau LayerNorm. Tại sao điều khiển độ lớn quan trọng ở độ sâu?
   Trung ngữ翻译:用纯Python 实现QK-Norm。给定 64 维的查询 和键,展示LayerNorm 前后的点积──为什么在深度网络中幅度控制很重要?

4. Đọc phần Chameleon 2.3 về sự ổn định tập luyện. mô tả chế độ thất bại chính xác được ghi nhận trên giấy ở 34B mà không có QK-Norm.
   Bài viết mô tả bài luận không sử dụng QK-Norm dưới 340 tỷ tham số  quan sát được mô hình thất bại thực sự.

5. Lớn bộ giải mã đồ chơi để phát ra phản ứng kiểu hỗn hợp khi chỉ có lời nhắc văn bản. đo số lần mô hình chọn hình ảnh trước vs văn bản trước khi được đào tạo phân phối dữ liệu 60% văn bản trước / 40% hình ảnh trước.
   Trung ngữ翻译:扩展玩具解码器,使其能够发出混合模态响应在给定的纯文提示时. Trong tập luyện dữ liệu phân bố 60% 文优先 / 40% 图像优先时,测量模型选择图像优先与文优先的频率.

## Từ khóa  Keyword

| Term | What people say | What it actually means | 中文含义 | 中文释义 |
|------|-----------------|------------------------|---------|
| Early fusion | "Unified tokens" | Images converted to discrete tokens sharing the transformer's vocabulary from step one | 图像从第一步就转换为与 Transformer 共享词汇表的离散 token |
| VQ-VAE | "Image tokenizer" | CNN + ViT + codebook that maps images to integer indices the transformer can predict | CNN + ViT + 码本，将图像映射为 Transformer 可预测的整数索引 |
| Shared vocabulary | "One dictionary" | A single token ID space covering text + image + modality separators | 覆盖文本 + 图像 + 模态分隔符的单一 token ID 空间 |
| QK-Norm | "Attention stabilizer" | LayerNorm applied to query and key before their dot product, prevents norm blowup | 在 query 和 key 点积前应用 LayerNorm，防止范数爆炸 |
| Mixed-modality generation | "Text + image output" | Inference that autonomously produces interleaved text and image tokens in one pass | 推理时自主产生交替的文本和图像 token |
| Codebook size | "K entries" | Number of discrete vectors the VQ-VAE can quantize to; trades compression for fidelity | VQ-VAE 可量化到的离散向量数；压缩与保真度的权衡 |
| Tokenizer ceiling | "Reconstruction limit" | Best PSNR achievable by decoding VQ tokens; bounds the model's image quality | 解码 VQ token 可达到的最佳 PSNR；限制模型的图像质量上限 |

## Xem thêm 延伸阅读

- [Chameleon Team — Chameleon: Mixed-Modal Early-Fusion Foundation Models (arXiv:2405.09818)](https://arxiv.org/abs/2405.09818)
  Trung文翻译:Chameleon 混合模态早期融合基础模型。
- [Aghajanyan et al. — CM3 (arXiv:2201.07520)](https://arxiv.org/abs/2201.07520)
  Trung văn翻译:CM3 论文,Chameleon's前身──
- [Yu et al. — CM3Leon (arXiv:2309.02591)](https://arxiv.org/abs/2309.02591)
  Trung ngữ翻译:CM3Leon,Chameleon's close kinship.
- [Zhan et al. — AnyGPT (arXiv:2402.12226)](https://arxiv.org/abs/2402.12226)
  Trung ngữ翻译:AnyGPT, mở rộng thành bốn hình thức.
- [Adept — Fuyu-8B blog (adept.ai)](https://www.adept.ai/blog/fuyu-8b)
  Trung ngữ翻译:Fuyu-8B 博客,跳过视觉编码器的方案──
