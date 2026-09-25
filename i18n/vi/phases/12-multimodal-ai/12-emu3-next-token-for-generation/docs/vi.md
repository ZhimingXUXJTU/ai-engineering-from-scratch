# Emu3: Dự báo mã số tiếp theo cho thế hệ hình ảnh và video

> BAAI's Emu3 (Wang et al., tháng 9 năm 2024) là kết quả năm 2024 nên kết thúc cuộc tranh luận phân tán chống lại tự rút lui. Một bộ biến đổi chỉ có decoder kiểu Llama, được đào tạo chỉ trên mục tiêu dự đoán mã thông báo tiếp theo, trên một từ vựng thống nhất của văn bản + mã thông báo hình ảnh VQ + mã thông báo video VQ 3D, đánh bại SDXL về sản xuất hình ảnh và LLaVA-1.6 về nhận thức. Không mất CLIP. Không có lịch trình phát sóng. Các hướng dẫn không phân loại được sử dụng để suy luận về chất lượng, nhưng mục tiêu đào tạo cốt lõi là dự đoán mã thông báo tiếp theo với việc buộc giáo viên. Được xuất bản trên tạp chí Nature. Bài học này đọc luận án Emu3  tại sao một tokenizer cộng quy mô tốt hơn là tất cả bạn cần  và trái ngược với các phương pháp phân phối.

> **【中文解读】**Emu3(BAAI,2024年9月) sử dụng mã thông báo tự quay lại đơn lẻ 预测目标, trong tập luyện trên bảng từ ngữ văn bản + hình ảnh + video, trong việc tạo hình ảnh đánh bại SDXL, trong việc hiểu rõ về hình ảnh đánh bại LLaVA-1.6── không có CLIP 损失, không có điều chỉnh phổ biến, mục tiêu tập luyện cốt lõi là mã thông báo 预测── được xuất bản trên Nature 上──

> **【拓展：自回归 vs 扩散的争论】**Đóng góp cốt lõi của Emu3 là khái niệm: nếu một token  dự đoán có thể phù hợp với mô hình phát triển trên hình ảnh, thì một mô hình thống nhất là một đường dẫn (một mất mát, một xương, bất kỳ mô hình nào) là khả thi.

**Type:** Learn  | **类型:** 学习
**Languages:** Python (stdlib, 3D video tokenizer math + autoregressive sampler skeleton) | **语言:** Python（标准库，3D 视频分词器数学 + 自回归采样器骨架）
**Prerequisites:** Phase 12 · 11 (Chameleon) | **前置知识:** Phase 12 · 11（Chameleon）
**Time:** ~120 minutes | **时间:** ~120 分钟

>  **【前置】**学本节前请先掌握:Phase 12·11(Chameleon 早期融合 token) 、Phase 8·01-03(扩散模型基础,对照学习) 、Phase 7(自归下次代币 训练) ⋅Emu3 =Chameleon 思路 + 更好的VQ 分词器 + 大规模训练──
>  **【类比】**扩散模型 vs Emu3 = "画油画" vs "拼乐高"。扩散 = 从噪音开始一步精修(连续去噪音),每步都重新画整张图;Emu3 = một token 往下拼拼;;离散乐高块),按顺序拼出图片。乐高看粗,但块足够小+类型足够多时也能拼出逼真画面,而且和文本生成同一套机制(都是下一个代号)。
> 🤔 **【困惑】**Q: 既然 Emu3 这么强,为什么稳定扩散 仍然主流? 推理成本!扩散模型 50 步去噪就能出图,Emu3 自回归需要生成上千代币才能出图,慢 20 倍. 量量产生 Emu3 接近 SDXL,但推理慢,所以生产仍然偏爱扩散.

## Mục tiêu học tập

- Giải thích lý do tại sao mục tiêu token tiếp theo của Emu3 có hiệu quả mặc dù giả định lâu năm rằng sự phân tán là cần thiết cho chất lượng hình ảnh.
  > 解释 tại sao Emu3 单一损失的下一代币 目标在长期假设" hình ảnh tạo phải được mở rộng" vẫn còn hiệu quả.
- Mô tả các 3D video tokenizer: một VQ codebook không gian-thời gian trông như thế nào, tại sao các bản vá kéo dài thời gian.
  > 描述 3D 视频分词器:时空 VQ 码本长什么样、为什么补丁 要跨时间维度──
- So sánh Emu3 vs Stable Diffusion XL trên (cuộc tính đào tạo, chi phí suy luận, trần chất lượng).
  > So sánh Emu3 với Stable Diffusion XL trong việc đào tạo tính năng, tính toán chi phí và chất lượng trên giới hạn khác biệt.
- Tên gọi ba vai trò mà mô hình Emu3 cùng chơi: Emu3-Gen (phần hình ảnh), Emu3-Chat (phản thức), Emu3-Stage2 (phần video).
  > 列举同一 Emu3 模型扮演的三种角色:Emu3-Gen(图像生成)、Emu3-Chat(感知)、Emu3-Stage2(视频生成)。

## Vấn đề  vấn đề nền

Sự thông minh thông thường cho đến năm 2024: việc tạo ra hình ảnh cần được phổ biến. Nguyên lý: các token hình ảnh phân biệt mất quá nhiều thông tin để tái cấu trúc chi tiết, và lấy mẫu tự rút tích lũy lỗi trên hàng ngàn token. Stable Diffusion, DALL- E 3, Imagen, Midjourney đều sử dụng một số hình thức pha trộn. Chameleon (Dân 12.11) một phần bác bỏ điều này ở quy mô nhỏ nhưng không phù hợp với SDXL về chất lượng.

> 2024 年前的共识: hình ảnh tạo cần phải phổ biến mô hình. 论点是:离散图像代币 损失太多信息无法重建细节,自归采样在数千代币上累积差.

Emu3 tấn công lập luận trực tiếp. tuyên bố: tokenizer thị giác tốt hơn + quy mô đủ + mất token tiếp theo = tạo hình ảnh bẻ cong trong cùng mô hình cũng nhận thức.

> Emu3 正面攻击这一论点──声称: Better视觉分词器 + 足够的规模 + 下一代币 损失 = tạo ra hình ảnh quá phổ biến trong cùng một mô hình, đồng thời cũng có thể làm cảm giác──

Cuộc cá cược đã gây tranh cãi khi được công bố. Hai năm sau, gia đình thế hệ thống nhất mã nguồn mở (Emu3, Show-o, Janus-Pro, Transfusion) là con đường mặc định cho nghiên cứu; các mô hình biên giới sản xuất dường như sử dụng một số biến thể.

> Đây là một trong những điều được xem là đáng chú ý nhất trong quá trình nghiên cứu.

## Khái niệm cốt lõi

> **【中文解读】**EMU3 sử dụng tự quay lại một token tiếp theo  dự đoán thống nhất nhiều mô hình hiểu và tạo.

> **【拓展：自回归图像生成的挑战】**Phương pháp tự quay lại hoàn toàn của EMU3 vẫn còn ở phía sau mô hình phổ biến trong việc tạo hình ảnh, vì độ dài của các token thị giác phụ thuộc vào văn bản khó học hơn.


### Chiếc token Emu3

Thành phần chính là token thị giác. Emu3 đào tạo một token tùy chỉnh lớp IBQ (Quantizer khớp chai ngược, SBER-MoVQGAN gia đình) với độ phân giải giảm 8x8 mỗi token. Một hình ảnh 512x512 trở thành 64x64 = 4096 token ở kích thước sổ mã 32768.

> 关键成分是视觉分词器──Emu3 训练了自定义 IBQ 类分词器(逆瓶量化器,SBER-MoVQGAN 家族), mỗi mã thông báo 8x8 分辨率缩减──一张 512x512 图像变成64x64 = 4096 个 token,码本大小 32768──

Đây là lớn hơn 1024 token của Chameleon cho mỗi 512x512 ở K = 8192 nhưng rẻ hơn cho mỗi token (bảo sát sách mã nhỏ hơn, codec đơn giản hơn).

> Đây là một hình ảnh lớn hơn mỗi biểu tượng của Chameleon (K=8192) nhưng mỗi biểu tượng rẻ hơn hơn (K=8192)

Đối với video: một tokenizer 3D VQ mã hóa một patch không gian-thời gian (4x4x4 pixel) thành một số nguyên. Một clip 4s ở 8 FPS có 32 khung hình; ở 256x256 với 4x giảm không gian và 4x giảm thời gian, số lượng token là (256/4) * (256/4) * (32/4) = 64 * 64 * 8 = 32,768 token.

> Đối với video: 3D VQ 分词器将时空补丁(4x4x4 像素)编码为整数──4秒片段在 8 FPS 下有 32 ;256x256 分辨率下 4x 空间和 4x 时间缩短,代码数字为 32768──

Chất lượng tokenizer là trần nhà. đóng góp của Emu3 là một phần "chúng tôi đào tạo một tokenizer rất tốt".

> 分词器质量是上限.  Em3  Em3  Em3  Em3  Em3  Em em3  Em em3  Em em em3  Em em em em3  Em em em3  Em em3  Em3  Em3  Em3  Em3  Em3  Em3  Em3  Em3  Em3  Em3  Em3  Em3  Em3  Em3  Em3  Em3  Em3  Em3  Em3  Em3  Em3  Em3  Em3  Em3  Em3  Em3  Em3  Em3  Em3  Em3  Em3  Em3  Em3  Em3  Em3  Em3  Em3  Em3  Em3  Em3  Em3  Em3  Em3  Em3  Em3  Em3  Em3  Em3  Em3  Em3  Em3  Em3  Em3  Em3  Em3  Em Em Em Em Em Em3  Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em Em

### Việc đào tạo một lần mất

Emu3 sử dụng một mục tiêu: dự đoán token tiếp theo trên một từ vựng chung trên các token văn bản, token hình ảnh 2D và token video 3D. Các trọng lượng được nhân bằng các yếu tố cụ thể về phương thức trong quá trình đào tạo để cân bằng đóng góp, nhưng chức năng mất mát là giống nhau.

> Emu3 sử dụng một mục tiêu: trên chia sẻ từ ngữ bảng biểu tượng 预测, bao gồm văn bản biểu tượng、 2D 图像 biểu tượng 和 3D 视频 biểu tượng。 tập luyện thời gian trọng lượng nhân bằng các yếu tố cụ thể để cân bằng đóng góp, nhưng hàm mất mát giống nhau。

Đào trên một hỗn hợp của:
- Gen hình ảnh: `<text caption> <image> image_tokens </image>`
  Trung ngữ翻译:图像生成
- Nhận thức hình ảnh: `<image> image_tokens </image> <question> text_tokens`
  Trung ngữ翻译:图像感知
- Video Gen: `<text caption> <video> video_tokens </video>`
  Trung ngữ翻译:视频生成
- Nhận thức video: tương tự.
  Trung ngữ翻译:视频感知:类似──
- Chỉ có văn bản: NTP tiêu chuẩn.
  Trung文翻译:纯文本:标准下一代币 预测。

Mô hình học được khi nào phát ra các token hình ảnh so với các token văn bản từ phân phối dữ liệu.`<image>`Đăng ký.

> 模型从数据分布中学习何时输出图像代币与文本代币―― khả năng tạo từ mô hình trong `<image>`标签后预测 hình ảnh token

### Định hướng và nhiệt độ không có trình phân loại

Tạo hình ảnh tự động trở nên tốt hơn nhiều với hướng dẫn không phân loại (CFG) khi suy luận. Emu3 sử dụng nó: tạo hai lần, một lần với tiêu đề đầy đủ, một lần với tiêu đề trống, trộn các logit với trọng lượng hướng dẫn (tình thường 3.0-7.0). Đây là cùng một CFG trick diffusion sử dụng, vay cho cài đặt tự động.

> Bản thân quay lại hình ảnh tạo trong suy luận sử dụng không phân loại thiết bị hướng dẫn(CFG) hiệu quả tốt hơn.

Nhiệt độ quan trọng: quá cao, đồ tạo vật; quá thấp, chế độ sụp đổ. Nhiệt độ khuyến cáo của Emu3 là 1.0 cho nhận thức, 0,8 cho việc tạo hình ảnh.

> 温度 rất quan trọng: quá cao sẽ có bóng giả; quá thấp sẽ dẫn đến sự sụp đổ của mô hình.

### Ba vai, một mô hình

Tàu Emu3 như ba API khác nhau về chức năng nhưng một bộ trọng lượng cơ bản:

> Emu3 以三个功能不同的API发货, nhưng sử dụng cùng một bộ权重:

- Emu3-Gen. Tạo hình ảnh.
  中文翻译:Emu3-Gen──图像生成──输入文本,输出图像代号──
- Emu3-Chat. VQA và captioning. Input image (tokens), output text.
  中文翻译:Emu3-Chat──视觉问答和描述──输入图像(token),输出文本──
- Emu3-Stage2. Tạo video và video VQA. nhập văn bản hoặc video, xuất văn bản hoặc video.
  Trung ngữ翻译:Emu3-Stage2──视频生成和视频问答──输入文本或视频,输出文本或视频──

Không có các mục tiêu cụ thể, chỉ là các mẫu đơn giản khác nhau, cùng một điểm kiểm soát.

> Không có nhiệm vụ cụ thể. Chỉ có một cái mẫu khác nhau.

### Điểm chuẩn

Từ bài báo Emu3 (Tháng 9 năm 2024):

> 来自 Emu3 论文(2024 年 9 月):

- Tạo hình ảnh: đánh bại SDXL trên MJHQ-30K FID (5.4 vs 5.6), GenEval tổng thể (0.54 vs 0.55  liên kết thống kê), và kết hợp của Deep-Eval trên bình đẳng.
  Trung文翻译:图像生成: 在 MJHQ-30K FID 上击败 SDXL(5.4 vs 5.6),GenEval 总体(0.54 vs 0.55统计上打平)。
- Nhận thức hình ảnh: vượt qua LLaVA-1.6 trên VQAv2 (75.1 vs 72.4) và gần giống nhau trên MMMU.
  Trung文翻译:图像感知: 在 VQAv2 上击败 LLaVA-1.6(75.1 vs 72.4), 在 MMMU 上大致持平──
- Sản xuất video: chất lượng clip 4 giây tại FVD cạnh tranh với các mô hình được đánh giá chung của thời kỳ Sora.
  Trung ngữ翻译:视频生成:4 秒片段质量与 Sora 时代的公开基准模型竞争力相当──

Các số không phải lúc nào cũng thắng  Emu3 giao dịch một điểm ở đây cho một điểm ở đó  nhưng tuyên bố "định đoán mã thông báo tiếp theo là tất cả những gì bạn cần" là đáng bảo vệ trên tất cả các phương pháp.

> Số không phải lúc nào cũng thắng Emus3 ở một điểm thay đổi điểm khác nhưng tuyên bố "điều tiên đoán là tất cả những gì bạn cần" trên tất cả các mô hình đều đứng vững.

### Chi phí tính toán

Emu3 được đào tạo trên ~ 300 tỷ mã thông báo đa phương tiện với mô hình tham số 7B. Thời gian GPU tương đương với Llama-2-7B trước khi đào tạo (2k-4k GPU năm trên silicon lớp A100).

> Emu3 trên khoảng 3000 tỷ nhiều mô hình token lên sử dụng 70 tỷ số số lượng mô hình đào tạo. GPU số lượng nhỏ gần như tương đương với Llama-2-7B 预训相当.

Khi suy luận, Emu3 chậm hơn SDXL mỗi hình ảnh: 4096 mã thông báo hình ảnh ở 30 tok / s là ~ 2 phút mỗi hình ảnh 512x512 , so với 2-5 giây cho SDXL. Việc giải mã suy đoán và tối ưu hóa cache KV thu hẹp khoảng cách nhưng không đóng cửa nó. Gen hình ảnh Autoregressive là tính toán nặng; đây là sự đổi mới.

> 推理时,Emu3 Mỗi张图像比SDXL 慢:4096 个图像代币 以 30 tok/s 生成, mỗi张 512x512 图像约2分钟,而SDXL chỉ mất 2-5秒――投机解码和KV 缓存优化缩小差距但没有关闭它――自归图像生成计算密度; đây là một cân bằng tồn tại.

### Tại sao nó quan trọng

Sự đóng góp sâu sắc của Emu3 là khái niệm. Nếu quy mô dự đoán token tiếp theo phù hợp với sự lan truyền trên việc tạo hình ảnh, con đường mô hình thống nhất (một lỗ, một xương sống, bất kỳ phương thức nào) là khả thi. Các mô hình trong tương lai không cần các mã hóa văn bản riêng biệt, lập trình phân phối riêng biệt, VAE riêng biệt. Một biến đổi, một tokeniser cho mỗi phương thức, quy mô.

> Lợi ích sâu sắc của Emu3 là khái niệm. Nếu token dự đoán có thể mở rộng đến sự mở rộng tương đương trên hình ảnh tạo, một phương pháp mô hình thống nhất (một mất mát, một xương, bất kỳ mô hình nào) là khả thi.

Show-o, Janus-Pro và InternVL-U đều xây dựng hoặc thách thức luận án này. Các phòng thí nghiệm Trung Quốc (BAAI, DeepSeek) xuất bản mạnh mẽ hơn các phòng thí nghiệm Mỹ vào năm 2025.

> Show-o、Janus-Pro 和 InternVL-U đều được xây dựng trên hoặc thách thức nó trên luận điểm này.


> **【拓展：EMU3 的统一训练策略】**Đó là một phần của EMU3 để chứng minh rằng phương pháp tự quay lại hoàn toàn có thể làm được cùng lúc để hiểu và tạo ra.


## Hãy dùng nó để thực hành
```figure
l5-emu3-next-token
```

## Sử dụng nó

`code/main.py`tạo ra hai đồ chơi:

> `code/main.py` xây dựng hai bộ phận đồ chơi:

- Một máy tính tính tính số lượng token 2D vs 3D VQ: được cho (định giải, vá, clip_length, FPS), tính toán số lượng token cho hình ảnh vs video.
  Trung文翻译:2D vs 3D VQ 分词器计数计算器:给定(分辨率、补丁、片段长度、FPS),计算图像与视频的代号 数量──
- Một mẫu hình ảnh tự rút theo mã hiệu với hướng dẫn không có phân loại ở nhiệt độ.
  Trung ngữ翻译:带温度和无分类器引导的自归图像代号采样器

Việc thực hiện CFG phù hợp với công thức của Emu3  trộn logit có điều kiện và không điều kiện với trọng lượng hướng dẫn.

> CFG thực hiện các giải pháp Emu3 để điều khiển quyền trọng lượng hỗn hợp điều kiện và không điều kiện logits.

## Đưa nó lên mạng

Bài học này sẽ mang lại kết quả `outputs/skill-token-gen-cost-analyzer.md`Với một mô hình sản phẩm thế hệ (hình ảnh hoặc video, độ phân giải mục tiêu, cấp độ chất lượng, ngân sách thời gian trễ), nó tính toán số lượng token, chi phí suy luận và chọn Emu3-family vs. diffusion.

> 本课产 出 `outputs/skill-token-gen-cost-analyzer.md` Đưa ra quy định sản phẩm (图像或视频), mục tiêu phân giải, chất lượng, ngân sách chậm), nó tính toán số lượng biểu tượng, chi phí dự đoán, và chọn giữa Emu3 系列 và mô hình phổ biến.

## Tập luyện bài tập

1. Emu3 tạo ra 4096 token cho mỗi hình ảnh 512x512 với giảm 8x8. tính toán tương đương cho 1024x1024 và 2048x2048.
   Trung文翻译:Emu3 在 8x8 缩减下每张 512x512 图像产生 4096 代币──计算 1024x1024 和 2048x2048 的等效值──推理延迟会怎样?

2. Đọc Emu3 Phần 3.3 trên video tokenizer. mô tả hình dạng vá VQ 3D và tại sao nó là 4x4x4 chứ không phải 8x8x1.
   Trung ngữ翻译:阅读 Emu3 第 3.3 节关于视频分词器──描述 3D VQ patch 形状以及为什么是4x4x4而不是8x8x1──

3. Đánh nặng hướng dẫn không phân loại 5.0 vs 3.0: hiệu ứng trực quan nào?`code/main.py`- Tôi không biết.
   Trung ngữ翻译:无分类器引导权重 5.0 vs 3.0: 视觉效果是什么?追踪 `code/main.py`Phương pháp toán học trung học

4. Lập toán FLOP đào tạo cho Emu3-7B với mã thông báo 300B và so sánh với Stable Diffusion 3.
   Trung ngữ翻译:计算 Emu3-7B 在 300B token 上的训练 FLOPs,并与稳定扩散3比较──哪个训练更贵?

5. Emu3 đánh bại SDXL trên FID nhưng không trên VQAv2 so với VLM chuyên ngành. Giải thích tại sao cách tiếp cận mất mát thống nhất cho thấy các điểm mạnh khác nhau so với các chuyên gia trên các tiêu chuẩn khác nhau.
   Trung ngữ翻译:Emu3 在 FID 上击败 SDXL, nhưng trong VQAv2 上不如专业 VLM──解释为什么统一损失方法在不同基准上表现出不同的优势──

## Từ khóa  Keyword

| Term | What people say | What it actually means | 中文含义 | 中文释义 |
|------|-----------------|------------------------|---------|
| Next-token prediction | "NTP" | Standard autoregressive loss: predict token[i+1] given token[0..i]; works for every modality when tokenized | 标准自回归损失：给定 token[0..i] 预测 token[i+1]；分词后适用于所有模态 |
| IBQ tokenizer | "Inverse bottleneck quantizer" | A class of VQ-VAE with larger codebooks (32768+) and better reconstruction than Chameleon's | 一类更大码本（32768+）和更好重建质量的 VQ-VAE |
| 3D VQ | "Spatiotemporal quantizer" | Codebook indexed by (time, row, col); one token covers a 4x4x4 pixel cube | 按（时间、行、列）索引的码本；一个 token 覆盖 4x4x4 像素立方体 |
| Classifier-free guidance | "CFG" | Mix conditional and unconditional logits with weight gamma; boosts image quality at inference | 用权重 gamma 混合条件和无条件 logits；提升推理图像质量 |
| Unified vocabulary | "Shared tokens" | Text + image + video all draw from the same integer space; model predicts whichever modality comes next | 文本+图像+视频共享同一整数空间；模型预测下一个模态 |
| MJHQ-30K | "Image gen benchmark" | Midjourney-quality benchmark with 30k prompts; Emu3 reports FID here | 30k 提示的 Midjourney 质量基准；Emu3 报告 FID |

## Xem thêm 延伸阅读

- [Wang et al. — Emu3: Next-Token Prediction is All You Need (arXiv:2409.18869)](https://arxiv.org/abs/2409.18869)
  Trung ngữ翻译:Emu3 论文下一代币 预测就是你需要的一切──
- [Sun et al. — Emu: Generative Pretraining in Multimodality (arXiv:2307.05222)](https://arxiv.org/abs/2307.05222)
  Trung文翻译:Emu 多模态生成预训练──
- [Liu et al. — LWM (arXiv:2402.08268)](https://arxiv.org/abs/2402.08268)
  Trung ngữ翻译:LWM 论文。
- [Yu et al. — MAGVIT-v2 (arXiv:2310.05737)](https://arxiv.org/abs/2310.05737)
  Trung ngữ翻译:MAGVIT-v2 视频分词器。
- [Tian et al. — VAR (arXiv:2404.02905)](https://arxiv.org/abs/2404.02905)
  Trung文翻译:VAR 视觉自归模型──
