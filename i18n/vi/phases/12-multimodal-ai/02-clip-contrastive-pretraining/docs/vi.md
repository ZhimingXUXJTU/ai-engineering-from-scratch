# CLIP và tương phản thị giác ngôn ngữ Pretraining

> CLIP (2021) của OpenAI chứng minh một ý tưởng duy nhất đủ lớn để cung cấp năng lượng trong năm năm tiếp theo: sắp xếp một bộ mã hóa hình ảnh và một bộ mã hóa văn bản trong cùng một không gian vector chỉ sử dụng các cặp hình ảnh-chủ đề web ồn ào và một lỗ hổng tương phản. Không có nhãn giám sát. 400 triệu cặp. Không gian nhúng kết quả làm phân loại chụp không, lấy lại hình ảnh văn bản, và cắm vào mỗi VLM năm 2026 như tháp tầm nhìn của nó. SigLIP 2 (2025) thay thế softmax bằng sigmoid và quy mô sau CLIP với chi phí thấp hơn. Bài học này đi bộ toán từ InfoNCE đến mất tích cặp sigmoid và xây dựng bước đào tạo trong stdlib Python.

> **【中文解读】**CLIP sử dụng 400 triệu hình ảnh mạng để, qua so sánh mất sẽ mã hóa hình ảnh và văn bản đến cùng một không gian khối lượng.

> **【拓展：CLIP→多模态大模型】**CLIP's graphics versus comparative learning là nền tảng của LLaVA、BLIP-2 等多模态大模型.

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, InfoNCE + sigmoid loss implementations) | **语言:** Python（标准库，InfoNCE + sigmoid 损失实现）
**Prerequisites:** Phase 12 · 01 (ViT patches), Phase 7 (Transformers) | **前置知识:** Phase 12 · 01（ViT patch），Phase 7（Transformer）
**Time:** ~180 minutes | **时间:** ~180 分钟

>  **【前置】**Học本节前请先掌握:Phase 12·01(ViT 把图像切成补丁);Phase 11·04(Embeddings 向量空间概念);Phase 7(Transformer自注意力)。本节核心数学是软max + 交叉,Phase 7·04 有详细推导──
>  **【类比】**CLIP 训练 = "中外文词典配对游戏"── cho 32k đối với hình ảnh, mô tả), để模型学会 đưa mỗi hình ảnh và mô tả của nó đến cùng một vị trí trong không gian khối lượng, đưa mô tả của các hình ảnh khác 31999 张推开── sau khi được đào tạo, mô hình có thể đưa "một bức ảnh của một con mèo" với một con mèo thực sự được vẽ cùng nhau ngay cả khi không thấy con mèo trong quá trình đào tạo.

## Mục tiêu học tập

- Thuộc dẫn mất InfoNCE từ thông tin lẫn nhau và thực hiện một phiên bản vector hóa ổn định về số.
  Trung ngữ翻译:从互信息推导 InfoNCE 损失,并实现数值稳定的向量化版本──
- Giải thích tại sao Sigmoid pairwise loss (SigLIP) đạt 32768+ mà không có yêu cầu về tổng tổng tổng chi phí trên mềm.
  Trung文翻译:解释为什么sigmoid 成对损失(SigLIP) có thể mở rộng đến 32768+ 批次大小,而无需软max 所需的全部集装 开销。
- Thực hiện phân loại ImageNet bằng cách xây dựng các mẫu văn bản (`a photo of a {class}`) và dùng argmax thay vì sự tương đồng cosine.
  Trung ngữ翻译:通过构建文本模板`a photo of a {class}`)并对余弦相似度取 argmax 来运行零样本 ImageNet 分类──
- Tên bốn đòn bẩy CLIP / SigLIP trước khi đào tạo cho bạn: kích thước lô, nhiệt độ, mẫu yêu cầu, chất lượng dữ liệu.
  Trung文翻译:列举 CLIP / SigLIP 预训给你四杆:批次大小、温度、提示模板、数据质量。

## Vấn đề  vấn đề giới thiệu

Tầm nhìn trước CLIP được giám sát. Thu thập các tập dữ liệu có nhãn (ImageNet: 1.2M hình ảnh, 1000 lớp), đào tạo một CNN, vận chuyển nó.

> CLIP  trước đây là một quá trình giám sát. 收集标注数据集. ImageNet:120.000张图像,1000 个类别), đào tạo CNN, triển khai. 标注昂贵,标注偏向标注者能达成共识的内容,并且标注不通过微调就无法迁移到新任务.

Các hình ảnh tựa đề web có hơn một tỷ cặp được dán nhãn miễn phí. Một bức ảnh của một chiếc xe thu hồi vàng với văn bản thay thế "con chó Max của tôi ở công viên" mang theo một tín hiệu giám sát văn bản mô tả hình ảnh. Câu hỏi: bạn có thể biến điều này thành một bài tập hữu ích không?

> Trên mạng có hơn một tỷ hình ảnh có sẵn miễn phí. Một bức ảnh của một con chó săn lùng có chứa các bài viết khác.

Câu trả lời của CLIP: coi cặp hình ảnh-chủ đề như một nhiệm vụ phù hợp. Với một loạt các hình ảnh N và các tiêu đề N, hãy học cách phù hợp với mỗi hình ảnh với tiêu đề riêng của nó đối với các chất phân tâm N-1.

> Câu trả lời của CLIP: 将图文对视为匹配任务――给定一批N 张图像和N 条描述,学习在N-1 干扰项目中将每个图像匹配自己的描述――监督信号是"这两样东西属于一起;这N-1 不属于"――没有类标签,没有人工标签,只有对比损失――

Không gian nhúng kết quả làm nhiều hơn CLIP được đào tạo cho. ImageNet chụp không hoạt động bởi vì "một bức ảnh của một con mèo" nhúng gần hình ảnh của mèo mà không bao giờ được gắn nhãn rõ ràng mèo. Đây là sự đặt cược đã sinh ra mỗi 2026 VLM.

> 得到的嵌入空间超越了CLIP的训练目标──ImageNet 零样本分类有效,因为"một bức ảnh của một con mèo" được嵌入到没有被明确标记为猫的猫图片附近──这就是催生所有2026年VLM的注──

## Khái niệm cốt lõi

> **【中文解读】**CLIP(Contrastive Language-Image Pre-training) thông qua việc so sánh học sẽ hình ảnh và văn bản được chiếu vào cùng một không gian khối lượng: phù hợp hình ảnh đối với khoảng cách gần, không phù hợp với các đề xuất. CLIP trong 4 tỷ hình ảnh đối với trên đào tạo, không cần phải điều chỉnh nhỏ để đạt được ảnh chụp không, là nền tảng của khả năng OpenAI đa mô hình.

> **【拓展：CLIP 的应用生态】**CLIP đối với mô hình học tập đã tạo ra rất nhiều ứng dụng:DALL-E 2/3 sử dụng CLIP để tạo hình ảnh,Stable Diffusion sử dụng OpenCLIP như một bộ lọc an toàn,LLaVA sử dụng CLIP  thiết bị lập lập trình hình ảnh kết nối LLM và hiểu hình ảnh.


> **【拓展：CLIP 的 zero-shot 能力】**CLIP có khả năng tuyệt vời nhất là không bắn 分类 không cần bất kỳ dữ liệu đào tạo nhiệm vụ dưới, chỉ cần cung cấp các danh mục về hình ảnh phân loại.


### Bộ mã hóa kép

CLIP có hai tháp:

> CLIP có hai tháp:

- Mã mã hình ảnh `f`: ViT hoặc ResNet, đưa ra một vector D-dim cho mỗi hình ảnh.
  Trung ngữ翻译:图像编码器 `f`:ViT hoặc ResNet, mỗi张图像输出一个D 维向量──
- Mã mã văn bản `g`: biến đổi nhỏ, phát ra một D-dim vector mỗi caption.
  中文翻译:文本编码器 `g`:小型变压器, mỗi条描述输出一个 D 维向量──

Cả hai tháp đều bình thường hóa đầu ra của họ cho chiều dài đơn vị.`cos(f(x), g(y)) = f(x)^T g(y)`vì cả hai đều là chuẩn đơn vị.

> Hai tòa nhà sẽ được kết hợp với các đơn vị dài.`cos(f(x), g(y)) = f(x)^T g(y)`, vì cả hai đều là đơn vị chiều kích.

> ️ **【易错点】**忘归一化(L2 bình thường hóa) 就计算相似度 → 向量模长大的样本天然有更大的点积,模型会偏向"长向量"而不是"语义匹配"──修复:每次前进 后必须`f = f / ||f||`, rồi mới tính`cos`
> 🤔 **【困惑】**Q: Tại sao sử dụng sự tương tự của các dây không sử dụng khoảng cách của O?A: O: O: O: chỉ nhìn theo hướng không nhìn dài, đối với "sáng khác nhau nhưng nội dung giống nhau" hình ảnh là ruột; khoảng cách của O sẽ được định hướng bởi khối lượng dài.

Đối với một loạt các cặp N (hình ảnh, tiêu đề), xây dựng mô hình giống nhau矩阵 `S`hình dạng`(N, N)`- Có thể là:

> Đối với một loạt các hình ảnh, mô tả) đối với, cấu trúc hình dạng`(N, N)`của sự tương đồng`S`- Có thể là:

```
S[i, j] = cos(f(x_i), g(y_j)) / tau
```

nơi `tau`là nhiệt độ được học (CLIP bắt đầu với 0.07; được học trong log-space).

> Trong số đó `tau`là một điều kiện nhiệt độ có thể học được (CLIP khởi nghiệp là 0.07; trong đối số không gian học)

### Lãng InfoNCE

CLIP sử dụng một entropy chéo đối xứng trên các hàng và cột:

> CLIP đối với行和列使用对称交叉:

```
loss_i2t = CE(S, labels=identity)     # each image's positive is its own caption
loss_t2i = CE(S^T, labels=identity)   # each caption's positive is its own image
loss = (loss_i2t + loss_t2i) / 2
```

Đây là InfoNCE. Softmax trong CE buộc mỗi hình ảnh phù hợp với tiêu đề của nó nhiều hơn bất kỳ tiêu đề nào khác trong lô. "Lối tiêu cực" là tất cả các mục lô khác.

> Đây là điểm mềm của InfoNCE──CE 强制每张图像与自己的描述的匹配率高于批次中所有其他描述──"负样本" là tất cả các mục khác trong批次──批次越大 = 负样本越多 = 信号越强──CLIP 在 32k批次下训练;规模很重要──

> ️ **【易错点】**batch_size 太小(如 64) 训不出好 CLIP负样本太少,模型学不到"什么算真正的相似"──CLIP 原文 batch_size=32768 才有效果──如果你只能跑批量=256,要么要用 SigLIP(不需要大批量),要么要用梯度累积模拟大批量(但不等价)──
>  **【类比】**InfoNCE 像" tìm kiếm trò chơi ngầm":32k 张图片对应 32k 个描述, mỗi hình ảnh phải tìm ra trong một đống mô tả của mình đối phó thực sự.

### Nhiệt độ

`tau`kiểm soát độ sắc nét của Softmax. Low tau → phân bố sắc nét, tác dụng khai thác tiêu cực cứng. High tau → mềm, tất cả các mẫu đóng góp. CLIP học log(1/tau), cắt để ngăn chặn sự sụp đổ. SigLIP 2 sửa chữa tau ban đầu và sử dụng một thiên vị học thay thế.

> `tau`控制 softmax 的度──低 tau → 尖分布,具有难负例挖掘效果──高 tau → 平滑, tất cả các mẫu đều có đóng góp──CLIP 学习 log(1/tau),并剪剪以防止崩──SigLIP 2 固定初始 tau 并使用可学习的偏置替──

### Tại sao cân bằng sigmoid tốt hơn (SigLIP)

Softmax cần toàn bộ các matrix tương đồng đồng. trong đào tạo phân tán bạn phải tập hợp tất cả mọi nhúng vào mỗi bản sao, sau đó làm softmax.

> Softmax  cần toàn bộ mô hình tương tự. Trong tập phân tán, bạn phải đặt mỗi mô hình vào tất cả các mô hình, sau đó làm softmax.

SigLIP thay thế softmax bằng sigmoid thông minh về yếu tố: cho mỗi cặp `(i, j)`, mất là phân loại nhị phân của "có cặp phù hợp không?" nhãn lớp tích cực là đường viền, tất cả mọi thứ khác là âm. mất là:

> SigLIP dùng từng yếu tố sigmoid  thay thế softmax: đối với mỗi đối tượng `(i, j)`, mất mát là đối với "có phải chúng phù hợp với?"

> 🤔 **【困惑】**Q: Tại sao softmax 需要全集而sigmoid 不需要?A: softmax 的分母是" tất cả N2 个配对的相似度之和", mỗi张 GPU 必须看到全部;sigmoid 只看每个 (i,j) 配对独立判断是/否匹配,不依赖全局信息──多 GPU 训练时 sigmoid 损失可以在地计算后减少──
>  **【类比】**InfoNCE = "32k 选 1 选择题", phải xem toàn张卷子才能做;SigLIP = "32k 个判断题 (((这对配对吗?)", mỗi câu trả lời độc lập.

```
L = -1/N sum over (i, j) [ y_ij log sigmoid(S[i,j]) + (1-y_ij) log sigmoid(-S[i,j]) ]
```

`y_ij = 1`Nếu`i == j`, khác 0. mỗi cặp mất tích độc lập. Không cần tất cả. Mỗi GPU tính toán khối và số tiền địa phương của mình. SigLIP 2 cân bằng để lô 32k-512k rẻ nơi CLIP cần tương xứng nhiều hơn giao tiếp.

> `y_ij = 1`Nếu `i == j`, nếu không thì là 0── mỗi đối tác mất mát là độc lập── không cần tất cả các bộ sưu tập── mỗi GPU tính toán khối lượng của nó và tìm kiếm và tìm kiếm──SigLIP 2 có thể chi phí thấp mở rộng đến 32k-512k lô, trong khi CLIP 需要相应更多的通信──

### Định dạng không bắn

Với tên lớp N, cho mỗi lớp tạo một mẫu văn bản:

> 给定 N 个类别名称, cho mỗi类构建文本模板:

```
"a photo of a {class}"
```

Nhập mỗi mẫu với mã hóa văn bản. Nhập hình ảnh của bạn với mã hóa hình ảnh. Argmax cosine tương đồng = lớp dự đoán. Không có đào tạo về các lớp mục tiêu.

> Sử dụng mã hóa văn bản đặt vào mỗi mô hình. Sử dụng mã hóa hình ảnh đặt vào hình ảnh.

> ️ **【易错点】**直接用 `"cat"`作为提示 → 比 `"a photo of a cat"`差 10+ 个百分点──CLIP 训练时文本端看的描述大多是完整句子,单词作为提示会让分布偏移──修复:始终使用模板`"a photo of a {class}"`,多模板集成更好.
> 🤔 **【困惑】**Q: ImageNet 1000 类全算一遍文嵌入 不是很慢吗?A: Chỉ tính một lần rồi缓存──1000 个提示 在文本编码器里跑一遍(毫秒级),后面每张新图片只需要1次图像嵌入+1000 次余弦相似度(向量化矩阵乘)──

Các mẫu nhanh là quan trọng. Bức giấy ban đầu của CLIP sử dụng 80 mẫu cho mỗi lớp (sơn, nghệ thuật, ảnh, vẽ, vv) và trung bình các nhúng. +3 điểm ImageNet. Sử dụng hiện đại thường chọn một hoặc hai mẫu.

> 提示模板很重要──CLIP 原始论文每类使用80模板(普通、艺术、照片、绘画等)并对嵌入取平均──ImageNet 上提升3个百分点──现代用法通常选择一个两个模板──

### Các thăm dò tuyến tính và điều chỉnh tinh tế

Zero-shot là một đường cơ sở. Một thăm dò tuyến tính (đưa một lớp tuyến tính trên các tính năng CLIP đóng băng cho các lớp mục tiêu của bạn) vượt qua zero-shot trên các nhiệm vụ trong lĩnh vực.

> 零样本是基线――线性探测(在结的 CLIP特征之上为目标类训练一个线性层) trên nhiệm vụ trong miền vượt quá零样本――全量微调在域 vượt quá线性探测,但可能损害零样本迁移――三种模式,三种权衡――

### SigLIP 2: NaFlex và các tính năng dày đặc

SigLIP 2 (2025) thêm:

> SigLIP 2(2025) thêm:

- NaFlex: mô hình đơn xử lý tỷ lệ và độ phân giải của các khía cạnh thay đổi.
  Trung ngữ翻译:NaFlex: đơn một mô hình xử lý có thể biến rộng cao比和分辨率。
- Các tính năng mật thiết tốt hơn cho phân đoạn và ước tính độ sâu, nhắm mục tiêu sử dụng như một xương sống đóng băng trong VLMs.
  Trung ngữ翻译:更好的密集特征用于分和深度估计, mục tiêu là trong VLM như là kết nối mạng lưới chính.
- Nhiều ngôn ngữ: được đào tạo trên 100+ ngôn ngữ nơi CLIP chỉ có tiếng Anh.
  Trung文翻译:多语言: 在100+种语言上训练,而CLIP 仅限英文――
- 1B param scale nơi CLIP đạt đỉnh ở 400M.
  Trung ngữ翻译: 10 tỷ số lượng, CLIP cao nhất là 4 tỷ.

Trong 2026 VLM mở, SigLIP 2 SO400m/14 là tháp tầm nhìn mặc định. CLIP vẫn là mặc định cho việc lấy lại văn bản hình ảnh khi phân phối đào tạo LAION-2B cụ thể phù hợp với mô hình truy vấn của bạn.

> Trong VLM mở cửa năm 2026, SigLIP 2 SO400m/14 là một lựa chọn mặc định trong việc kiểm tra văn bản tinh khiết, đặc biệt là khi các chuyên gia LAION-2B  đào tạo phân phối phù hợp với mô hình truy vấn của bạn.

### ALIGN, BASIC, OpenCLIP, EVA-CLIP

ALIGN (Google, 2021): cùng một ý tưởng như CLIP, thang đo đôi 1.8B, 90% tiếng ồn. Scales dữ liệu ồn ào được chứng minh. OpenCLIP (LAION): tái tạo CLIP mở trên LAION-400M / 2B, nhiều thang đo, điểm kiểm soát mở. EVA-CLIP: khởi tạo từ mô hình hình hóa mặt nạ; xương sống mạnh mẽ cho VLMs. BASIC: CLIP + ALIGN lai của Google. Tất cả cùng một gia đình, dữ liệu khác nhau và điều chỉnh.

> ALIGN(Google,2021): ý tưởng tương tự như CLIP,18 tỷ đối với quy mô, 90% ồn dữ liệu.

### Màn trần không bắn

Các mô hình CLIP-class có mức tối đa khoảng 76% ImageNet zero-shot (CLIP-G, OpenCLIP-G). Ngoài ra có thể cần dữ liệu lớn hơn nhiều (SigLIP 2 nhận 80% +) hoặc thay đổi kiến trúc (chủ đầu giám sát, nhiều tham số hơn).

> CLIP 类模型 trên ImageNet 零样本分类上限约为76%(CLIP-G、OpenCLIP-G) ・・・ vượt qua mức này cần dữ liệu lớn hơn(SigLIP 2  đạt đến 80%+) hoặc cấu trúc thay đổi hơn(监督头、更多参数) ・基准测试正在和; giá trị thực sự nằm trong 嵌入空间下游 VLM 消费的.

> 🤔 **【困惑】**Học完本节还会问:1) Tại sao CLIP không có ảnh chụp không giống như GPT-4 đó là cách hiểu "các người trong bức tranh làm gì"? CLIP chỉ học được "图文匹配", không học được suy đoán về mối quan hệ chi tiết, đó là VLM(như LLaVA) làm việc.

## Hãy sử dụng nó để thực hiện
```figure
multimodal-fusion
```

## Sử dụng nó

`code/main.py`thực hiện:

> `code/main.py`实现:

1. Một mã hóa đồ chơi kép (chương tính hình ảnh dựa trên hash, tính năng biểu đồ văn bản) để bạn có thể xem hình dạng InfoNCE mà không cần numpy.
   Trung ngữ翻译:一个玩具双编码器 (tựa trên các hình ảnh của Hash, không cần phải numpy ngay cả khi bạn có thể xem hình dạng của InfoNCE).
2. InfoNCE mất mát trong Python tinh khiết (thường ổn định số bằng log-sum-exp).
   Trung文翻译:纯Python 实现的 InfoNCE 损失(通过日记总数-exp 实现数值稳定性) ⋅
3. Lối mất cặp Sigmoid để so sánh.
   Trung ngữ翻译:Sigmoid 成对损失用于对比.
4. Một thói quen phân loại chụp không: tính toán sự tương đồng cosine với một tập hợp các lời nhắc văn bản, argmax cho dự đoán.
   Trung ngữ翻译:零样本分类例程:计算与一组文本提示的余弦相似度,argmax 得出预测──

Hãy chạy nó và xem đường cong thua lỗ. Số tuyệt đối là đồ chơi; hình dạng phù hợp với những gì một huấn luyện viên CLIP thực sự phát ra.

> 运行它并观察损失曲线──绝对数值是玩具级的; nhưng hình dạng phù hợp với thực tế CLIP 训练器的输出──

## Chuyển nó đi.

Bài học này sẽ mang lại kết quả `outputs/skill-clip-zero-shot.md`. Với một bộ hình ảnh (via path) và một danh sách các lớp mục tiêu, nó xây dựng các lời nhắc văn bản với mẫu CLIP, nhúng cả hai bên với một điểm kiểm soát được chỉ định (ví dụ: `openai/clip-vit-large-patch14`), và trả lại dự đoán top-1 / top-5 với điểm tương đồng. Kỹ năng từ chối đưa ra tuyên bố về các lớp không trong danh sách yêu cầu.

> 本课产 出 `outputs/skill-clip-zero-shot.md`△ Đưa định một nhóm hình ảnh (通过路径) và một nhóm mục tiêu (目标类别) nó sử dụng CLIP 模板 xây dựng văn bản提示, sử dụng các điểm kiểm tra xác định như`openai/clip-vit-large-patch14`(văn) được đặt vào hai bên, và trở lại với số lượng tương đồng trên 1 / trên 5 预测。

## Tập luyện bài tập

1. Thực hiện InfoNCE cho một loạt 4 cặp bằng tay. Xây dựng các hình tử hình tương tự 4x4, chạy softmax, chọn đường chéo, tính toán chéo entropy. Kiểm tra Python thực hiện của bạn với tính toán tay này.
   Trung文翻译:手动实现 4 đối với mẫu InfoNCE。 xây dựng 4x4 相似度矩阵,运行 softmax,提取对角线,计算交叉──验证你的Python 实现与手算一致──

2. SigLIP sử dụng một tham số thiên vị `b`Ngoài nhiệt độ: `S'[i,j] = S[i,j]/tau + b`- Vai trò của nó là gì?`b`chơi khi các lô có sự mất cân bằng lớp lớn (nhiều hơn nhiều âm tính so với tích cực cho mỗi hàng)?
   Trung ngữ翻译:SigLIP ngoại trừ nhiệt độ cũng sử dụng các tham số định vị `b`- Có thể là:`S'[i,j] = S[i,j]/tau + b`◊ Khi có nhiều loại không cân bằng (trong mỗi dòng tiêu cực có nhiều hơn mô hình chính xác)`b`起什么作用?阅读 SigLIP 第 3 节(arXiv:2303.15343)

3. Xây dựng một phân loại không bắn cho mèo so với chó.`a photo of a {class}`và `a picture of a {class}`- Đánh giá độ chính xác trên 100 hình ảnh thử nghiệm.
   Trung ngữ翻译:构建猫狗零样本分类器──尝试两种提示模板:`a photo of a {class}`和 `a picture of a {class}`◊ tỷ lệ đo chính xác trên 100 张试图图.

4. Xét chi phí truyền thông của Softmax InfoNCE vs sigmoid cặp cho một 512-GPU chạy tại lô 32k.
   Trung文翻译:计算 512 GPU、批次 32k 下softmax InfoNCE 与 sigmoid 成对损失的通信成本──哪个是 O(N),哪个是 O(N^2)?引用 SigLIP 第 4 节──

5. Đọc bài báo OpenCLIP về quy mô quy mô (arXiv:2212.07143, Cherti et al.). Tạo lại kết luận của họ về quy mô dữ liệu từ các con số: ở kích thước mô hình cố định, mối quan hệ log-linear giữa độ chính xác chụp không của ImageNet và kích thước dữ liệu đào tạo là gì?
   Trung ngữ翻译:阅读 OpenCLIP 缩放定律论文(arXiv:2212.07143,Cherti 等人)  Từ biểu đồ trong mô tả kết luận về việc mở rộng dữ liệu: Trong mô hình cố định,ImageNet 零样本准确率 và training dữ liệu lớn là gì đối với số lượng liên quan?

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|------------------------|---------|
| 术语 | 通俗说法 | 实际含义 | |
| InfoNCE | "Contrastive loss" | Cross-entropy over a batch's similarity matrix; each item's positive is its paired item, negatives are everything else | 批次相似度矩阵上的交叉熵；每项的正样本是其配对项，负样本是所有其他项 |
| Sigmoid loss | "SigLIP loss" | Per-pair binary cross-entropy; no softmax, no all-gather, scales cheaply in distributed training | 逐对二分类交叉熵；无 softmax，无 all-gather，分布式训练中扩展成本低 |
| Temperature | "tau" | Scalar that scales logits before softmax/sigmoid; controls sharpness of the distribution | softmax/sigmoid 前缩放 logits 的标量；控制分布的锐度 |
| Zero-shot | "no-finetune classification" | Use text prompts to construct class embeddings and classify by cosine similarity; no training on target classes | 用文本提示构建类别嵌入，通过余弦相似度分类；无需在目标类别上训练 |
| Prompt template | "a photo of a ..." | Text scaffold around a class name; affects zero-shot accuracy by 1-5 points | 类别名周围的文本支架；影响零样本准确率 1-5 个百分点 |
| Dual encoder | "Two-tower" | One image encoder + one text encoder, outputs in shared D-dim space | 一个图像编码器 + 一个文本编码器，输出在共享的 D 维空间 |
| Hard negative | "Tough distractor" | A negative similar enough to the positive that the model has to work to separate them | 与正样本足够相似的负样本，模型需要努力区分它们 |
| Linear probe | "Frozen + one layer" | Train only a linear classifier on top of frozen features; measures feature quality | 仅在冻结特征之上训练线性分类器；衡量特征质量 |
| NaFlex | "Native flexible resolution" | SigLIP 2 capability to ingest images at any aspect ratio and resolution without resizing | SigLIP 2 以任意宽高比和分辨率输入图像的能力，无需调整大小 |
| Temperature scaling | "log-parametrized tau" | CLIP parametrizes `log(1/tau)` so gradients behave; clips to prevent collapse to near-zero tau | CLIP 参数化 `log(1/tau)` 使梯度行为正常；裁剪防止 tau 崩溃到接近零 |

## Xem thêm 延伸阅读

- [Radford et al. — Learning Transferable Visual Models From Natural Language Supervision (arXiv:2103.00020)](https://arxiv.org/abs/2103.00020) giấy CLIP.
  Trung ngữ翻译:CLIP 论文。
- [Zhai et al. — Sigmoid Loss for Language Image Pre-Training (arXiv:2303.15343)](https://arxiv.org/abs/2303.15343) SigLIP.
  Trung ngữ翻译:SigLIP 论文。
- [Tschannen et al. — SigLIP 2 (arXiv:2502.14786)](https://arxiv.org/abs/2502.14786) đa ngôn ngữ + NaFlex.
  中文翻译:多语言 + NaFlex。
- [Jia et al. — ALIGN (arXiv:2102.05918)](https://arxiv.org/abs/2102.05918) quy mô với dữ liệu web ồn ào.
  Trung ngữ翻译:用噪声网络数据扩展──
- [Cherti et al. — Reproducible scaling laws for contrastive language-image learning (arXiv:2212.07143)](https://arxiv.org/abs/2212.07143) OpenCLIP quy mô luật.
  Trung文翻译:OpenCLIP 缩放定律。
