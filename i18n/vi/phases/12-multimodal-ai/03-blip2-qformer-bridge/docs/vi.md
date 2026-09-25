# Từ CLIP đến BLIP-2  Q-Former như cầu Modality  Từ CLIP đến BLIP-2:Q-Former 模态桥接

> CLIP sắp xếp hình ảnh và văn bản nhưng không thể tạo tiêu đề, trả lời câu hỏi hoặc tổ chức cuộc trò chuyện. BLIP-2 (Salesforce, 2023) giải quyết điều đó với một cây cầu có thể đào tạo nhỏ: 32 vector truy vấn có thể học được tham gia qua các tính năng của ViT đóng băng thông qua sự chú ý chéo, sau đó slot trực tiếp vào dòng đầu vào của LLM đóng băng. 188 triệu tham số cầu nối một LLM 11B với một ViT-g/14. Mỗi VLM dựa trên bộ điều chỉnh thông qua năm 2026  MiniGPT-4, InstructBLIP, anh em họ của LLaVA  là một hậu duệ. Bài học này đọc kiến trúc của Q-Former, giải thích đào tạo hai giai đoạn của nó, và xây dựng một phiên bản đồ chơi cung cấp các token hình ảnh vào một bộ giải mã văn bản đóng băng.

> **【中文解读】**CLIP chỉ có thể đối phó với các bản đồ nhưng không thể tạo ra. BLIP-2 sử dụng 32 khối lượng truy vấn có thể học thông qua giao thông chú ý của ViT và LLM, chỉ có 188M tham số có thể đưa các đặc điểm hình ảnh vào mô hình ngôn ngữ của 11B.

> **【拓展：Q-Former→多模态架构演进】**Q-Đã là người sáng lập của mô hình "结视觉编码器+结LLM+轻量桥接", MiniGPT-4、InstructBLIP、LLaVA 都是其思想的后代──

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, cross-attention + learnable-query demo) | **语言:** Python（标准库，交叉注意力 + 可学习查询演示）
**Prerequisites:** Phase 12 · 02 (CLIP), Phase 7 (Transformers) | **前置知识:** Phase 12 · 02（CLIP），Phase 7（Transformer）
**Time:** ~180 minutes | **时间:** ~180 分钟

>  **【前置】**学本节前请先掌握:Phase 12·02(CLIP đối với học tập);Phase 7(Transformer自注意力和交叉注意力);Phase 11·04(Embeddings)。
>  **【类比】**Q-Former = "记者采访"──32 个记者(query) đứng 256 补丁 ViT 出来 前面,每个人都提问自己的问题,听完回答后写下 32 条新闻摘要──这32 条摘要就是给 LLM 的"新闻简报",LLM 不用看完整 256 张原始图片──

## Mục tiêu học tập

- Giải thích tại sao một nút thắt có thể đào tạo giữa một bộ mã hóa thị giác đóng băng và LLM đóng băng vượt qua việc điều chỉnh chi phí và ổn định từ đầu đến cuối.
  Trung ngữ翻译:解释为什么在结视觉编码器和结 LLM 之间的可训练瓶在成本和稳定性上优于端到端微调──
- Thực hiện một khối chú ý qua nhau nơi một bộ truy vấn học tập cố định chăm sóc các tính năng hình ảnh bên ngoài.
  Trung ngữ翻译: thực hiện một khối tập trung tập trung, trong đó một nhóm các câu hỏi có thể học được cố định để quan tâm đến các đặc điểm hình ảnh bên ngoài.
- Đi qua quá trình huấn luyện trước hai giai đoạn của BLIP-2: đại diện (ITC + ITM + ITG) sau đó tạo ra (sự mất mát LM với máy giải mã đóng băng).
  Trung ngữ翻译:理 BLIP-2 的两阶段预训:表示学习(ITC + ITM + ITG) 然后生成学习(结解码器的 LM 损失) 』
- So sánh Q-Former với máy chiếu MLP đơn giản hơn được sử dụng trong LLaVA và tranh luận khi mỗi lựa chọn thắng.
  Trung ngữ翻译:比较 Q-Former 和 LLaVA 使用的更简单的 MLP 投影器,论证各自优势场景──

## Vấn đề  vấn đề giới thiệu

Bạn có ViT đóng băng sản xuất 256 mã thông báo váy của dim 1408 mỗi hình ảnh. Bạn có một mã thông báo váy 7B đóng băng dự kiến nhúng mã thông báo của dim 4096. Cầu rõ ràng  một lớp tuyến tính từ 1408 đến 4096  hoạt động, nhưng cung cấp tất cả 256 mã thông báo váy vào bối cảnh của LLM chi phí 256 mã thông báo thêm mỗi hình ảnh.

> Bạn có một kết nối ViT, mỗi hình ảnh tạo ra 256 kích thước patch token 1408 . Bạn có một kết nối 7B LLM, mong đợi kích thước 4096 token 嵌入. Rõ ràng các giao diện nối từ 1408 đến 4096 có thể, nhưng sẽ có tất cả 256 patch token  vào LLM.

Câu hỏi BLIP-2: bạn có thể nén đại diện hình ảnh 256 token thành ít hơn nhiều token (chẳng hạn là 32) trong khi vẫn giữ đủ thông tin cho LLM để ghi chú, trả lời các câu hỏi và lý luận về hình ảnh? Và bạn có thể đào tạo cây cầu này mà không chạm vào xương sống đóng băng, giữ chi phí đào tạo chỉ ở các tham số của cây cầu?

> Câu hỏi của BLIP-2: Bạn có thể nén 256 token biểu tượng hình ảnh xuống còn ít hơn 32 token, trong khi vẫn giữ đủ thông tin để LLM tiến hành mô tả hình ảnh, trả lời câu hỏi và suy luận?

Câu trả lời: một Q-Former. 32 vector "query" có thể học được, liên kết với các mã hóa patch của ViT, tạo ra một bản tóm tắt trực quan 32 mã hóa mà LLM tiêu thụ.

> 答案是:Q-Former──32 个可学习的"查询"量通过交叉关注关注 ViT's patch token,产生LLM 消费的32 token 视觉摘要──总共188M参数──在接触LLM 之前使用比较、匹配和生成目标进行训练──

## Khái niệm cốt lõi

> **【中文解读】**BLIP-2  giới thiệu Q-Former  như một kết nối nhẹ giữa các máy lập trình hình ảnh và LLM Former sử dụng một nhóm mã truy vấn có thể học được từ các máy lập trình hình ảnh lấy các đặc điểm hình ảnh liên quan nhất đến văn bản, giảm đáng kể số lượng các tập luyện chỉ tập Q-Former), đạt được hiệu quả cao về ngôn ngữ hình ảnh đối với nhau.

> **【拓展：BLIP-2 的高效训练】**BLIP-2 có thể hoàn thành tập luyện trong 12 giờ trên đơn张 A100 (với chỉ Q-Former 参数), so với phương pháp trước đó nhanh 10-100 lần.


> **【拓展：Q-Former 的影响】**Các ý tưởng thiết kế của Q-Former ([[Use a learning query from 结编码器提取任务相关特征) được lấy đi rộng rãi]].InstructBLIP sử dụng một cách tương tự để làm các chỉ thị cảm nhận các đặc điểm thị giác提取──Q-Former của nhẹ lượng ([[ chỉ khoảng 188M 参数)) cho phép đào tạo nhiều mô hình trên GPU cấp tiêu dùng trở nên có thể──


### Các câu hỏi có thể học được

Trù cốt lõi của Q-Former: thay vì để các mã thông báo văn bản của LLM tham gia vào các bản vá hình ảnh, giới thiệu một bộ mới của 32 vector truy vấn có thể học `Q`Các truy vấn là các tham số của mô hình  chúng được học trong quá trình đào tạo và cùng 32 truy vấn được sử dụng cho mỗi hình ảnh.

> Kỹ năng cốt lõi của Q-Former: Đừng để LLM của văn bản token  tập trung vào hình ảnh patch, mà thay vào đó giới thiệu một nhóm mới 32                                                                                                                                                                                                                                            `Q`,让*它们*关注图像补丁――查询是模型的参数在训练中学习,并且每个图像都使用相同的32查询――

> ️ **【易错点】**Để "32 câu hỏi là 32 张不同图片的查询"错!32 câu hỏi là cố định, giống như tất cả các hình ảnh.
> 🤔 **【困惑】**Q: 32 个 truy vấn 怎么知道每个该看什么?A: 训练时三个损失(ITC/ITM/ITG) sẽ ngược向传播梯度告诉每个 truy vấn 该专精什么;; cuối cùng学到的 32 维编码是"损失下降最快的那个方向",不是为人定"颜色/物体/背景"――

Sau khi chú ý qua nhau, mỗi truy vấn chứa một bản tóm tắt nén của hình ảnh  "xác định đối tượng chính", "xác định nền", "đếm các đối tượng", vv Các truy vấn không chuyên về nhãn ngữ nghĩa; họ học bất cứ điều gì mã hóa làm giảm tổn thất dòng chảy.

> Sau khi giao lưu, mỗi truy vấn có một bản tóm tắt của hình ảnh " mô tả đối tượng chính""", mô tả bối cảnh""", số lượng đối tượng tính toán" và các khác.

### Kiến trúc

Q-Former là một bộ biến đổi nhỏ (12 lớp, ~ 100M params) với hai con đường:

> Q-Former là một Transformer nhỏ ((12 tầng, khoảng 100M 参数), có hai đường:

1. Chặng đường truy vấn: 32 vector truy vấn chảy qua sự chú ý tự (tạm dịch: tự chú ý), sau đó là sự chú ý chéo qua các mã thông báo vá của ViT đóng băng, sau đó là FFN.
   Trung ngữ翻译:查询路径:32 个查询向量流过自注意力(彼此之间), sau đó đối với 结 ViT của patch token làm交叉注意力, cuối cùng là FFN。
2. Hướng dẫn văn bản: một bộ mã hóa văn bản giống BERT chia sẻ sự chú ý tự và trọng lượng FFN với đường truy vấn.
   Trung ngữ翻译:文本路径:类 BERT 的文本编码器与查询路径共享自注意力和FFN 权重──文本路径禁用交叉注意力──

Trong thời gian đào tạo, cả hai con đường đều chạy. Các truy vấn và văn bản tương tác thông qua sự tập trung chung, có nghĩa là các truy vấn có thể điều chỉnh văn bản cho các nhiệm vụ cần thiết (ITM, ITG).

>  training时两条路径同时运行──查询和文本通过共享的自注意交互,这意味着查询可以在需要文本的任务中进行处理.

### Việc đào tạo hai giai đoạn

BLIP-2 tập luyện trước trong hai giai đoạn:

> BLIP-2 分两阶段预训练:

Giai đoạn 1: học đại diện (không có LLM). Ba lỗ:
- ITC (phản ứng tương phản hình ảnh-tinh văn): Tương ứng tương phản CLIP giữa các mã thông báo truy vấn tập hợp và mã thông báo CLS văn bản.
  Trung ngữ翻译:ITC(图文对比):池化查询 token với文本 CLS token 之间类 CLIP对比损失──
- ITM (phản ứng hình ảnh- văn bản): phân loại nhị phân  cặp hình ảnh- văn bản này là một sự phù hợp? Hard-negative-mined.
  Trung ngữ翻译:ITM(图文匹配):
- ITG (tạo văn bản dựa trên hình ảnh): LM nguyên nhân đầu trên văn bản, tùy thuộc vào các truy vấn.
  Trung văn翻译:ITG(图像条件文本生成): kết quả trên văn bản LM 头,以查询为条件──强制查询编码可生成文本内容──

>  **【类比】**三损失的分工:ITC = "看图找文字" (粗粒度对齐);ITM = "nhận xét rằng bức tranh này không thực sự được phân phối" (细粒度区分);ITG = " nhìn vào bức tranh để viết ra văn bản đối phó) (生成能力)

Chỉ có tàu Q-Former, ViT bị đóng băng, không có LLM.

> 仅训练 Q-Former──ViT 结──不涉及 LLM──

Giai đoạn 2: học sinh sinh. Thêm một LLM đóng băng (OPT-2.7B hoặc Flan-T5-XL, vv). Dự án 32 đầu ra truy vấn vào các LLM nhúng thấp hơn thông qua một lớp tuyến tính nhỏ. Chuẩn bị chúng cho văn bản prompt. Chỉ tập chiếu tuyến tính và Q-Former trên LM mất trên chuỗi liên kết prompt + hình ảnh + tiêu đề.

> II giai đoạn: tạo học tập. Cụ kết nối một kết thúc LLM(OPT-2.7B hoặc Flan-T5-XL và như vậy)  Thông qua một lớp nhỏ của đường dẫn sẽ có 32 câu hỏi xuất phát đầu tư đến các bước phẳng của LLM.

Sau giai đoạn 2, dự án Q-Former + là bộ điều chỉnh trực quan đầy đủ. Khi suy luận: hình ảnh → ViT → Q-Former → dự án tuyến tính → trước văn bản → LLM đóng băng phát ra.

> 第二阶段后,Q-Former + 投影就是完整的视觉适配器──推理时:图像 → ViT → Q-Former → 线性投影 → 前置到文本 → 结 LLM 生成输出──

### Kinh tế tham số

BLIP-2 với ViT-g/14 (1.1B, đông lạnh) + OPT-6.7B (6.7B, đông lạnh) + Q-Former (188M, được đào tạo) = tổng cộng 8B, 188M được đào tạo.

> BLIP-2 sử dụng ViT-g/14(11 tỷ,结) + OPT-6.7B(67 tỷ,结) + Q-Former(1.88 tỷ,训练) = 共 80 tỷ,训练1.88 tỷ,训练1.88 tỷ,Q-Former 仅占全参数约2.4%──训练成本反映这一点:少量A100 上数天 vs 端到端数周──

Chất lượng: BLIP-2 tương thích hoặc đánh bại Flamingo-80B trên VQA bắn không nhưng nhỏ hơn 50 lần.

> 质量:BLIP-2 在零样本 VQA 上匹配或超越 Flamingo-80B,同时小了50倍──桥接方案有效──

### InstructBLIP và Q-Former có ý thức về hướng dẫn

InstructBLIP (2023) mở rộng Q-Former với một đầu vào bổ sung: bản văn hướng dẫn. Trong thời gian chú ý chéo, các truy vấn bây giờ có quyền truy cập cả vào các bản vá hình ảnh và hướng dẫn. Các truy vấn có thể chuyên về từng hướng dẫn ("đếm xe", "xác định tâm trạng") thay vì học một bản tóm tắt cố định duy nhất. Điểm chuẩn tăng lên trên các nhiệm vụ đã được tổ chức.

> InstructBLIP(2023) thông qua额外输入 mở rộng Q-Former: chỉ thị văn bản bản bản thân mình. Trong giao thông chú ý, truy vấn có thể truy cập cùng lúc vào các bản vá hình ảnh và chỉ thị.

### MiniGPT-4 và phương pháp tiếp cận chỉ dùng máy chiếu

MiniGPT-4 giữ Q-Former nhưng chỉ đào tạo các dự đoán đường thẳng đầu ra trong khi đóng băng tất cả mọi thứ khác. rẻ, nhưng chi phí là chất lượng  các truy vấn là BLIP-2, không phải của bạn.

> MiniGPT-4 giữ lại Q-Former, nhưng chỉ tập luyện để đưa ra các dự án trực tuyến, kết thúc tất cả mọi thứ.

### Tại sao LLaVA trở nên đơn giản hơn

LLaVA (2023, Bài học 12.05) thay thế Q-Former bằng một MLP 2 tầng đơn giản chiếu mỗi token ViT patch vào không gian LLM  576 token mỗi hình ảnh cho một lưới 24x24, tất cả được cung cấp cho LLM. Khử trùng tồi tệ hơn nhưng cho phép LLM tham gia hơn các vết tháo nguyên liệu. Vào thời điểm đó điều này gây tranh cãi; vào cuối năm 2023 nó đã thống trị bởi vì dữ liệu hướng dẫn thị giác (LLaVA-Instruct-150k) chứng minh rằng MLP có thể được đào tạo để bảo tồn đủ tín hiệu. Sự thỏa hiệp: ngữ cảnh của LLaVA điền nhanh hơn, nhưng nó tự nhiên mở rộng sang nhiều hình ảnh và video.

> LLaVA(2023,第 12.05 课) sử dụng đơn giản 2 tầng MLP  thay thế Q-Former, sẽ chiếu mỗi mã ViT patch token vào LLM 空间24x24 网格下 mỗi hình ảnh 576 个 token, tất cả  cho LLM.

> 🤔 **【困惑】**Học完本节还会问:Q-Former vs LLaVA MLP 该选哪个? 短上下文 + 高质量 → Q-Former(压缩 32 token 精心训练);长上下文 + 多图/视频 → LLaVA MLP(per token 信息量大但灵活) ⋅ 2026 năm hầu hết VLM sử dụng MLP, vì dữ liệu chỉ thị thị thị là đủ, MLP học được đủ tốt và dễ mở rộng hơn ~~

Đến năm 2026, phân chia lĩnh vực: Q-Former tồn tại ở nơi ngân sách token quan trọng (video dài, nhiều hình ảnh); máy chiếu MLP thống trị nơi chất lượng thô mỗi token là ưu tiên.

> Đến năm 2026, lĩnh vực phân chia: Q-Former trong token  ngân sách quan trọng khi;;长视频、多图像) tồn tại;MLP 投影器 trong chất lượng ban đầu của mỗi token chiếm ưu thế khi chủ yếu.

### Sự chú ý qua cửa: Flamingo, tổ tiên

Flamingo (Dạy 12.04) trước BLIP-2 và sử dụng cùng một ý tưởng chú ý chéo nhưng ở mỗi lớp LLM đóng băng, không phải là một cầu duy nhất. BLIP-2 cho thấy bạn có thể nén đến lớp đầu vào chỉ và vẫn hoạt động. Gemini và Idefics kết hợp cả hai: mã thông báo đầu vào được giao tiếp cộng với sự chú ý chéo được đóng cửa tùy chọn cho vài cú chụp trong bối cảnh.

> Flamingo (第 12.04 课) trước BLIP-2, sử dụng cùng một ý tưởng giao thông nhưng trong mỗi kết thúc của LLM layer, chứ không phải là một cầu nối. BLIP-2 chứng minh chỉ có thể nén đến các bước vào vẫn còn hiệu quả.

### Những người kế thừa năm 2026

- Q-Former: BLIP-2, InstructBLIP, MiniGPT-4, và hầu hết các mô hình ngôn ngữ video vì lý do ngân sách token.
  Trung文翻译:Q-Former:BLIP-2、InstructBLIP、MiniGPT-4,以及大多数视频语言模型 (因为 token 预算原因) ⋅
- Các thiết bị nhận dạng: biến thể Flamingo (Dạy 12.04); Gia đình Idefics, Eagle, OmniMAE.
  Trung文翻译:Perceiver resampler:Flamingo 的变体;;第 12.04 课);Idefics 系列、Eagle、OmniMAE。
- Máy chiếu MLP: LLaVA, LLaVA-NeXT, LLaVA-OneVision, Cambrian-1.
  中文翻译:MLP 投影器:LLaVA、LLaVA-NeXT、LLaVA-OneVision、Cambrian-1。
- Đội Vị VILA, PaliGemma.
  Trung文翻译:注意力池化:VILA、PaliGemma。

Tất cả bốn đều hợp lệ. Câu hỏi quyết định là liệu bạn có bị hạn chế về ngân sách token hay về chất lượng mỗi token.

> Bốn quy trình đều có hiệu quả. Vấn đề quyết định là bạn bị ràng buộc là token.

## Hãy sử dụng nó để thực hiện
```figure
modality-projection
```

## Sử dụng nó

`code/main.py`xây dựng một sự chú ý qua nhau theo kiểu Stdlib Q-Former:

> `code/main.py`构建一个标准库 Q-Former 风格的交叉注意力:

1. Mô phỏng 256 mã hóa vá hình ảnh (dim 128).
   Trung文翻译:模拟 256 个图像补丁代号 ((维度 128) 』
2. Tự nhiên 32 truy vấn có thể học được (vùng 128).
   Trung ngữ翻译:实例化 32 个可学习查询(维度 128)。
3. Tiếp tục quy mô điểm- sản phẩm sự chú ý chéo (Q từ truy vấn, K/V từ các bản vá).
   Trung文翻译:运行缩放点积交叉注意力(Q 来自查询,K/V 来自补丁) 』
4. Dự án LLM-dim (512) thông qua một lớp tuyến tính.
   Trung ngữ翻译:通过线性层投影到 LLM 维度 ((512) 』
5. Tạo ra 32 mã thị giác sẵn sàng cho LLM.
   Trung文翻译:输出 32 个 LLM 就绪的视觉代号.

Tất cả toán học trong Python tinh khiết (đường vòng tròn trên các vector). Toy nhưng hình dạng chính xác.

> Tất cả các toán học vận hành sử dụng Python tinh khiết (,) khối lượng 嵌套循环) ⋅ lớp đồ chơi nhưng hình dạng chính xác ⋅ in chú ý quyền lực trọng lượng矩阵, bạn có thể xem mỗi truy vấn từ những váy 提取信息──

## Chuyển nó đi.

Bài học này sẽ mang lại kết quả `outputs/skill-modality-bridge-picker.md`. Với cấu hình VLM mục tiêu (số mã hóa hình ảnh, ngân sách bối cảnh LLM, hạn chế triển khai, mục tiêu chất lượng), nó khuyên Q-Former vs MLP vs Perceiver resampler với một lý do ngắn và ước tính số parameter cho mỗi cầu.

> 本课产 出 `outputs/skill-modality-bridge-picker.md`△给定目标 VLM 配置(视觉编码器代币 数、LLM 上下文预算、部署约束、质量目标), nó đề xuất Q-Former vs MLP vs Perceiver resampler,附简短理由和每个桥接层的参数估算──

## Tập luyện bài tập

1. Thực hiện khối chú ý chéo trong PyTorch. Kiểm tra rằng với 32 truy vấn và 256 phím / giá trị, các khối lượng chú ý là 32 x 256 và mỗi hàng tổng cộng đến 1 sau softmax.
   Trung文翻译:用 PyTorch 实现交叉注意力块──验证 32 个查询和 256 个关键/值,注意力权重矩阵为 32 x 256,每行软max 后和为 1──

2. Trong BLIP-2 giai đoạn 1, Q-Former chạy ba lỗ đồng thời: ITC, ITM, ITG. Viết chữ ký về phía trước cho mỗi trong mã giả.
   Trong giai đoạn đầu tiên của BLIP-2, Q-Former cùng thời gian vận hành có ba lỗ hổng: ITC, ITM, ITG.

3. So sánh số lượng tham số: Q-Former (12 lớp, 768 ẩn) so với một máy chiếu MLP 2 lớp (1408 → 4096, hai lớp).
   Trung文翻译:比较参数:Q-Former(12层,768 隐藏维度) vs 2层 MLP 投影器(1408 → 4096,两层) ・・・ 在什么 LLM 规模下,188M 的Q-Former 成本在训练效率超过本?

4. Đọc Phần 3.2 của bài báo BLIP-2 (arXiv:2301.12597) về cách khởi tạo Q-Former. Giải thích tại sao khởi tạo từ cơ sở BERT (không ngẫu nhiên) tăng tốc sự hội tụ.
   Trung ngữ翻译:阅读 BLIP-2 论文(arXiv:2301.12597) 第 3.2 节关于Q-Former 初始化的部分──解释为什么从BERT-(base非随机)初始化加速收──

5. Đối với một video 10 phút với 1 FPS lấy mẫu đến 60 khung hình, tính toán chi phí token mỗi khung hình ở (Q-Former → 32 token / khung hình) so với (MLP projector → 576 token / khung hình).
   Trung ngữ翻译:对于10分钟视频以1 FPS 样样为60 ,计算每代币 成本:(Q-Former → 32代币/)vs(MLP 投影器 → 576代币/) ――哪个能放进 128k代币的 LLM 上下文窗口?

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|------------------------|---------|
| 术语 | 通俗说法 | 实际含义 | |
| Q-Former | "Querying transformer" | Small transformer with 32 learnable query vectors that cross-attend to frozen ViT features | 带有 32 个可学习查询向量的小型 Transformer，交叉关注冻结的 ViT 特征 |
| Learnable queries | "Soft prompt for vision" | A fixed set of parameters that serve as the query side of cross-attention; learned per model, shared across all inputs | 作为交叉注意力查询侧的固定参数集；按模型学习，所有输入共享 |
| Cross-attention | "Q from here, K/V from there" | Attention where query, key, and value come from different sources; how the queries pull from ViT patches | 查询、键和值来自不同来源的注意力；查询如何从 ViT patch 提取信息 |
| ITC | "Image-text contrastive" | CLIP-style loss applied to Q-Former pooled queries vs text CLS | 应用于 Q-Former 池化查询与文本 CLS 的类 CLIP 对比损失 |
| ITM | "Image-text matching" | Binary classifier on hard-negative-mined pairs; forces the queries to discriminate fine-grained mismatches | 难负例挖掘对上的二分类器；强制查询区分细粒度不匹配 |
| ITG | "Image-grounded text generation" | Causal LM loss where text is generated conditioned on queries; forces queries to encode text-decodable content | 以查询为条件生成文本的因果 LM 损失；强制查询编码可解码为文本的内容 |
| Two-stage pretraining | "Representation then generative" | Stage 1 trains Q-Former alone (ITC/ITM/ITG); Stage 2 attaches frozen LLM and trains only the projection + Q-Former | 第一阶段仅训练 Q-Former；第二阶段连接冻结 LLM，仅训练投影 + Q-Former |
| Frozen backbone | "Do not finetune" | The vision encoder and LLM weights are fixed; only the bridge trains | 视觉编码器和 LLM 权重固定；仅训练桥接层 |
| Projection head | "Linear to LLM dim" | Final linear layer mapping Q-Former output to the LLM's embedding dimension | 将 Q-Former 输出映射到 LLM 嵌入维度的最终线性层 |
| Perceiver resampler | "Flamingo's version" | Similar learnable-query cross-attention, used by Flamingo at every layer rather than as a single bridge | 类似的可学习查询交叉注意力，Flamingo 在每层使用而非单一桥接 |

## Xem thêm 延伸阅读

- [Li et al. — BLIP-2 (arXiv:2301.12597)](https://arxiv.org/abs/2301.12597) giấy cốt lõi.
  Trung ngữ翻译:BLIP-2 核心论文──
- [Li et al. — BLIP (arXiv:2201.12086)](https://arxiv.org/abs/2201.12086) người tiền nhiệm với bộ ba ITC/ITM/ITG.
  中文翻译:前作,包含 ITC/ITM/ITG 三联损失──
- [Li et al. — ALBEF (arXiv:2107.07651)](https://arxiv.org/abs/2107.07651) "định hướng trước khi hợp nhất"  tổ tiên khái niệm của giai đoạn 1 đào tạo.
  Trung ngữ翻译:"先对齐再融合"第一阶段训练的概念先驱──
- [Dai et al. — InstructBLIP (arXiv:2305.06500)](https://arxiv.org/abs/2305.06500) Q-Former biết hướng dẫn.
  中文翻译:指令感知的 Q-Former。
- [Zhu et al. — MiniGPT-4 (arXiv:2304.10592)](https://arxiv.org/abs/2304.10592) Phương pháp chỉ sử dụng máy chiếu.
  Trung ngữ翻译:仅投影器方案。
- [Jaegle et al. — Perceiver IO (arXiv:2107.14795)](https://arxiv.org/abs/2107.14795) kiến trúc chung cho sự chú ý chéo của những người có thể học hỏi.
  Trung文翻译:可学习查询交叉注意力的一般架构──
