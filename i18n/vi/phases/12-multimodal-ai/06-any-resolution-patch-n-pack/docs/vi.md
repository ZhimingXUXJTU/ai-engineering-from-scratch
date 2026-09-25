# Any-Resolution Vision: Patch-n'-Pack và NaFlex 任意分辨率视觉: Patch-n'-Pack với NaFlex

> Hình ảnh thực không phải là 224x224 vuông. Một tờ biên lai là 9:16, một biểu đồ là 16:9, một quét y tế có thể là 4096x4096, một ảnh màn hình di động là 9:19.5. Câu trả lời VLM trước năm 2024  thay đổi kích thước mọi thứ thành một hình vuông cố định  ném đi tín hiệu làm cho OCR, hiểu tài liệu và phân tích cảnh độ phân giải cao làm việc. NaViT (Google, 2023) cho thấy bạn có thể gói các bản vá độ phân giải biến thành một lô biến đổi đơn với nén đường khối. M-RoPE (2024) của Qwen2-VL đã loại bỏ hoàn toàn các bảng vị trí tuyệt đối. AnyRes của LLaVA-NeXT đã làm phẳng hình ảnh độ phân giải cao thành hình ảnh cơ sở + phụ. Thay đổi NaFlex của SigLIP 2 (2025) hiện là mã hóa mặc định cho các VLM mở muốn một điểm kiểm soát duy nhất phục vụ mọi tỷ lệ khía cạnh. Bài học này thực hiện patch-n'-pack cuối đến cuối.

> **【中文解读】**Hình ảnh thế giới thực không phải hình vuông 224x224  thu nhập là 9:16, hình ảnh là 16:9, hình ảnh y tế có thể 4096x4096──2024 trước VLM 统一将图像缩小为固定正方形,这会丢失 OCR、文档理解和高分辨率场景解析的关键信息──本课讲解如何让变压器以原始分辨率处理任意宽高比的图像──

> **【拓展：金融文档场景的分辨率挑战】**Trong bối cảnh tài chính, vở báo cáo, phát phiếu, hợp đồng và các tài liệu khác nhau có độ rộng cao hơn hàng ngàn khác nhau. Sự thu hẹp hình chữ bằng hình chữ cố định sẽ dẫn đến sự biến đổi hình chữ cái, độ chính xác OCR giảm.

**Type:** Build  | **类型:** 构建
**Languages:** Python (stdlib, patch packer + block-diagonal mask)  | **语言:** Python（标准库，补丁打包器 + 块对角掩码）
**Prerequisites:** Phase 12 · 01 (ViT patches), Phase 12 · 05 (LLaVA)  | **前置知识:** Phase 12 · 01（ViT补丁）、Phase 12 · 05（LLaVA）
**Time:** ~120 minutes  | **时间:** ~120 分钟

>  **【前置】**Học本节前请先掌握:Phase 12·01(ViT 把图切成补丁);Phase 12·05(LLaVA 投影器);Phase 7·04(RoPE 位置编码,本节用2D-RoPE)
>  **【类比】**NaViT's patch-n'-pack = "搬家打包"──传统 ViT = Đặt mọi thứ theo một hộp nhỏ cắt 
> ️ **【易错点】**实现 NaViT 时忘记块对角掩码 → 三张图的补丁 会相互注意,模型训练完全失败──修复: phải xây dựng (N,N) 矩阵注意, chỉ trong mỗi张图对应的补丁索引块内允许注意,块外为 -inf──

## Mục tiêu học tập

- Lắp ráp các bản vá từ một loạt hình ảnh độ phân giải biến thành một chuỗi và xây dựng mặt nạ chú ý khối-châm.
  > Để đóng gói các bản sửa chữa của hình ảnh phân giải khác nhau vào một chuỗi, xây dựng khối để ẩn sự chú ý góc.
- Chọn giữa AnyRes tileing (LLaVA-NeXT), NaFlex (SigLIP 2) và M-RoPE (Qwen2-VL) cho một nhiệm vụ nhất định.
  > 根据任务选择 AnyRes 切片(LLaVA-NeXT)、NaFlex(SigLIP 2) hoặc M-RoPE(Qwen2-VL)。
- Lập kế hoạch ngân sách token cho OCR, biểu đồ và chụp ảnh mà không cần đổi kích thước.
  > 计算无缩缩的情况下 OCR, biểu đồ và biểu tượng chụp ảnh 预算
- Hãy nêu tên ba chế độ thất bại của việc hình vuông: văn bản bị bẻ, nội dung bị cắt, mã thông báo bị lãng phí trên đệm.
  > 列举正方形缩放的三种失败模式:文字压缩,内容裁剪,padding 浪费――

## Vấn đề  vấn đề nền

Các bộ biến đổi mong đợi một chuỗi. Một lô là một loạt các chuỗi cùng chiều dài. Nếu hình ảnh của bạn là 224x224, bạn nhận được 196 mã đệm mỗi lần, không cần đệm, công việc đã hoàn thành. Đào trên 224, suy luận trên 224, không bao giờ nghĩ về độ phân giải nữa.

> Transformer 期望固定长度序列──一批就是一堆等长序列──如果图像都是224x224,每次都产生196补丁代币,无需填充,问题解决──训练和推理都用224,永远不用考虑分辨率──

Các tài liệu là chân dung (8,5x11 inch, 2:3-ish). Chart screenshots là cảnh quan (16:9). Quản đơn là cao và mỏng (1:3). Tàu hình ảnh y tế ở 2048x2048 hoặc lớn hơn.

> 现实世界不配──文档是向的(8.5x11英寸,约 2:3)──图表截图是横向的(16:9)──收据又高又窄(1:3)──医疗影像动 2048x2048或更大──移动设备截图是1170x2532(0.46:1)──

Ba lựa chọn trước năm 2024 và tại sao mỗi lựa chọn đều thất bại:

> Ba lựa chọn trước năm 2024 và nguyên nhân thất bại của họ:

1. Tái kích thước lên một hình vuông cố định (224x224 hoặc 336x336).
   > 缩放为固定正方形(224x224或336x336) ―― 缩缩会扭曲文字和人脸──下采样会破坏图表标签和OCR 内容──LLaVA-1.5 之前的标准做法──
2. Crop to a fixed aspect ratio. Bạn ném đi phần lớn hình ảnh, và chọn vị trí của crop là vấn đề thị giác của nó.
   > 剪裁为固定宽高比. 剪裁为固定宽高比. 剪裁为固定宽高比. 剪裁为固定宽高比. 剪裁为固定宽高比. 剪裁为固定宽高比. 剪裁为固定宽高比. 剪裁为固定宽高比. 剪裁为固定宽高比. 剪裁为固定宽高比. 剪裁为固定宽高比. 剪裁为固定宽宽宽比. 剪裁为固定宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽. 剪裁为宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽,宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽宽
3. Pad đến phía dài nhất. sửa sai lệch nhưng lãng phí 50% + của các token trên đệm hình ảnh chân dung. chi phí chú ý vuông trên tất cả các token pad.
   > 填充到最长边── sửa lại biến dạng nhưng lãng phí 50% + của token trên màn hình                                                                                                                                                                                                                                                    

> **【中文解读】**Transformer 期望固定长度的序列── thực tế thế giới hình ảnh宽高比不同,2024年前有三种做法:(1) 缩小为正方形文字变形、OCR 内容丢失;(2) 剪丢弃大量内容;(3) 填充屏图像浪费50%+的代币 在填充上,注意计算成本第二次增长──

Câu trả lời 2024-2025: để biến đổi ăn các đốm ở độ phân giải bản địa của hình ảnh, và tìm ra cách đóng gói một lô khác nhau vào một chuỗi mà không lãng phí tính toán.

> Câu trả lời trong năm 2024-2025: Hãy để Transformer trực tiếp sử dụng các "đồ" sửa chữa phân giải ban đầu, sau đó nghĩ cách để đưa các khối khác nhau được gói thành một chuỗi mà không lãng phí tính toán.

## Khái niệm cốt lõi

### NaViT và Patch-n'-pack

NaViT (Dehghani et al., 2023) là bài báo cho thấy công việc này trên quy mô.

> NaViT(Dehghani 等人,2023) chứng minh cách nghĩ này có thể được thực hiện trên quy mô lớn.

1. Đối với mỗi hình ảnh trong lô, tính toán lưới nhựa bản địa của nó ở kích thước nhựa được chọn (chẳng hạn là 14).
   > Đối với mỗi hình ảnh trong số các lô, để xác định sửa chữa lớn (((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((
2. Mời các bản vá của mỗi hình ảnh vào chuỗi dài biến của riêng nó.
   > Phong cách để mỗi hình ảnh được phẳng cho chuỗi độ dài thay đổi của riêng mình.
3. Kết hợp tất cả các bản vá hình ảnh thành một chuỗi dài cho lô.
   > Đặt tất cả các hình ảnh trong một chuỗi dài như một loạt.
4. Xây dựng một mặt nạ chú ý khối-châm để các bản vá hình ảnh A chỉ đi bên trong hình ảnh A.
   > Xây dựng khối để ẩn sự chú ý đối với góc, để sửa chữa của hình ảnh A chỉ được tập trung vào hình ảnh A bên trong.
5. Mang theo thông tin vị trí cho mỗi vá (2D RoPE hoặc các embedment vị trí phân đoạn).
   > Để mỗi bổ sung mang theo thông tin vị trí ((2D RoPE hoặc phần số vị trí được đặt vào)

Một loạt ba hình ảnh ở 336x336 (576 mã thông báo), 224x224 (256 mã thông báo) và 448x336 (768 mã thông báo) trở thành một chuỗi 1600 mã thông báo với một mặt nạ khối-châm 1600x1600. Không đệm. Không có tính toán lãng phí.

> 三张不同分辨率图像(336x336=576 token、224x224=256 token、448x336=768 token) của hàng hóa biến thành một chuỗi 1600 token,配配 1600x1600块对角掩码──零填充,零浪费──Transformer tự nhiên xử lý tùy ý宽高比──

NaViT cũng giới thiệu giảm đệm phân đoạn trong khi tập luyện  giảm 50% các đệm ngẫu nhiên trên toàn bộ đệm  điều này cả đều điều chỉnh và tăng tốc độ tập luyện. SigLIP 2 thừa hưởng điều này.

> NaViT cũng đưa ra các bài tập về số lượng các bổ sung bị bỏ rơi trong các lần tập trung tự bỏ 50%  sửa chữa vừa được chuẩn hóa vừa được tăng tốc các bài tập.

> **【中文解读】**Nô của NaViT: 三张不同分辨率的图像(576 + 256 + 768 = 1600 个代币) được gói trong một chuỗi, sử dụng khối đối góc ẩn để ngăn chặn sự chú ý qua hình ảnh.

### AnyRes (LLaVA-Next)  AnyRes 切片策略

AnyRes của LLaVA-NeXT là một lựa chọn thay thế thực tế. Với hình ảnh độ phân giải cao và mã hóa cố định (CLIP hoặc SigLIP ở 336), hình ảnh được làm bằng tile:

1. Chọn một bố cục lưới từ một bộ định nghĩa trước  (1x1), (1x2), (2x1), (1x3), (3x1), (2x2), vv  phù hợp nhất với tỷ lệ hình ảnh.
2. Đặt tấm hình đầy đủ vào lưới; mỗi tấm trở thành một sản phẩm 336x336.
3. Ngoài ra tạo ra một hình ảnh nhỏ: toàn bộ hình ảnh được kích thước lại thành 336x336 như một mã thông báo ngữ cảnh toàn cầu.
4. Mã hóa mỗi con gạch thông qua mã hóa 336 đóng băng. Kết nối các mã thông báo gạch + mã thông báo hình ảnh nhỏ.

Đối với một hình ảnh 672x672 ở lưới 2x2 cộng với hình ảnh nhỏ: 4 * 576 + 576 = 2880 mã thông báo trực quan.

AnyRes là tuyến đường lựa chọn khi mã hóa của bạn bị đóng băng và chỉ hỗ trợ một độ phân giải. Nó làm nổ số lượng token cho hình ảnh lớn (một hình ảnh 1344x1344 ở lưới 4x4 là 9216 + 576 ≈ 9800 token, chứa hầu hết các bối cảnh LLM 8k).

> **【中文解读】**AnyRes  thích hợp cho các máy lập trình được kết hợp và chỉ hỗ trợ trong trường hợp phân giải đơn lẻ. Giá cả là mã số hình ảnh lớn tăng lên.

### M-RoPE (Qwen2-VL) ➜ M-RoPE nhiều mô hình quay vị trí mã

Qwen2-VL đã giới thiệu Đường xếp vị trí xoay đa phương tiện. Thay vì vị trí phân tích của NaViT hoặc tấm và hình ảnh nhỏ của AnyRes, mỗi bản vá có vị trí 3D (thời gian, chiều cao, chiều rộng). Các vòng quay truy vấn / khóa xử lý chiều dài tùy ý H, W và thời gian.

M-RoPE cung cấp độ phân giải động bản địa mà không cần đào tạo lại. Khi bạn đưa ra bất kỳ hình ảnh HxW nào, người nhúng vá sẽ tạo ra các mã H/14 x W/14, mỗi mã sẽ có vị trí (t=0, r=row, c=col), RoPE sẽ quay sự chú ý với tần số phù hợp, được thực hiện. Qwen2.5-VL và Qwen3-VL tiếp tục như vậy.

Không giống như AnyRes, M-RoPE là token O(H x W / P^2) ở độ phân giải bản địa  không có chi phí cao phay nhân. Không giống như NaViT, nó vẫn mong đợi một hình ảnh duy nhất mỗi chuyển tiếp.

> **【中文解读】**M-RoPE cho mỗi bổ sung cấp ba chiều vị trí (( thời gian、 chiều cao、 chiều rộng), sử dụng quay vị trí编码 xử lý bất kỳ H、W 和 thời gian độ dài。

### NaFlex (SigLIP 2)

NaFlex là chế độ tự nhiên của điểm kiểm tra SigLIP 2. Một mô hình duy nhất phục vụ nhiều chiều dài chuỗi (256, 729, 1024 token) khi suy luận. Bên trong nó sử dụng kiểu NaViT patch-n'-pack trong quá trình đào tạo và các vị trí phân tích tuyệt đối cho mỗi bản vá. Điểm bán hàng: một điểm kiểm tra, chọn ngân sách token của bạn khi suy luận dựa trên nhiệm vụ.

Đối với một nhiệm vụ ngữ nghĩa (thân loại, lấy lại), 256 token. Đối với OCR hoặc hiểu đồ thị, 1024 token. Không có đào tạo lại.

> **【中文解读】**Điểm bán hàng cốt lõi của NaFlex: Một điểm kiểm tra, được đưa ra khi chọn token 预算。语义任务使用 256 token,OCR hoặc biểu đồ hiểu bằng 1024 token, không cần đào tạo nặng。

### Mặt nạ đóng gói

Mặt nạ hình khối là nơi mà hầu hết các triển khai gặp trục trặc.`N_total`hình ảnh `i=0..B-1`với độ dài `n_i`, mặt nạ `M`hình dạng`(N_total, N_total)`là 1 nếu cả hai chỉ số rơi vào khối hình ảnh tương tự, nếu không 0. Bạn có thể xây dựng nó từ một danh sách chiều dài tích lũy:

```
offsets = [0, n_0, n_0+n_1, ..., N_total]                         # 累积偏移量
M[i, j] = 1 iff there exists b where offsets[b] <= i < offsets[b+1] # 同一图像块内为1
                        and offsets[b] <= j < offsets[b+1]
```

Đây là một dòng trong PyTorch với `torch.block_diag`FlashAttention's variable-length path (`cu_seqlens`) bỏ qua mặt nạ hoàn toàn và tham gia theo trình tự sử dụng tensor chiều dài tích lũy trực tiếp  ~ 10x nhanh hơn một mặt nạ dày đặc cho các lô điển hình.

> **【中文解读】**块对角掩码 đảm bảo mỗi bức ảnh sửa chữa chỉ tập trung vào bản thân, sẽ không " thấy " các sửa chữa của các bức ảnh khác trong số các lô.`cu_seqlens`(với tốc độ khoảng 10 lần)

### - Đơn vị ngân sách

Chọn chiến lược theo nhiệm vụ:

- OCR / tài liệu: 1024-4096 token. SigLIP 2 NaFlex tại 1024, hoặc AnyRes 3x3 + thumbnail.
- Hình và UI: 729-1024 token ở 384-448 bản địa. Qwen2.5VL độ phân giải động với tối đa pixel.
- Ảnh tự nhiên: 256-576 token là tốt. LLM downstream thấy đủ. Thanh tiền cho token nơi mật độ nội dung cao.
- Video: 64-128 token mỗi khung sau khi tích hợp không gian, 2-8 FPS. Bài học 12.17 bao gồm điều này.

Quy tắc sản xuất năm 2026: chọn một nắp tối đa pixel mỗi nhiệm vụ, mã hóa ở tỷ lệ độ native lên nắp đó, đóng gói lô, và bỏ đi đệm.`min_pixels`và `max_pixels`chính xác là cái nút này.

> **【拓展：Token 预算与成本优化】**Trong môi trường sản xuất, token  ngân sách ảnh hưởng trực tiếp đến API 成本和延迟。 phân bổ 1024+ token cho nhiệm vụ OCR là cần thiết, nhưng tự nhiên ảnh sử dụng 256 token là đủ.

> 🤔 **【困惑】**Học完本节还会问:1) 真要部署 OCR 系统,min_pixels 和 max_pixels 该设多少?文档类 min=28*28*4、max=28*28*2560(Qwen2-VL 默认);过高会爆显存,过低会丢失小字──2) Tại sao không trực tiếp sử dụng 2k×2k? token 二次爆,长文档一张图就吃掉整个 LLM 上下文──3) NaFlex vs AnyRes 哪个更通用? NaFlex(SigLIP 2) 更现代,单一点检查 适应所有分辨率;AnyRes 是过渡方案──

## Hãy dùng nó để thực hành
```figure
mm-patch-n-pack
```

## Sử dụng nó

`code/main.py`thực hiện patch-n'-pack cho một loạt hình ảnh đa dạng với các phối điểm pixel nguyên số.

> `code/main.py`Sử dụng toàn bộ số hình ảnh được đặt trên các hình ảnh khác nhau.

- Có một danh sách kích thước hình ảnh (H, W).
  > 接收 (H, W) 图像尺寸列表
- Xét chiều dài chuỗi các bản vá của mỗi hình ảnh ở kích thước bản vá 14.
  > 计算每张图像在补丁大小 14 下的序列长度──
- Bao gồm chúng thành một chuỗi dài tổng cộng`sum(n_i)`- Tôi không biết.
  > 打包为总长度 `sum(n_i)`của một chuỗi đơn lẻ.
- Xây dựng mặt nạ chú ý khối-châm-phương (thấp, để rõ ràng hơn).
  > 构建块对角注意力掩码 (năm hình thức, dễ hiểu)
- So sánh chi phí đóng gói so với kích thước vuông và các tấm AnyRes.
  > Đối với việc đóng gói chi phí so với hình dạng hình chữ số và AnyRes 切片.
- Bác bản bảng ngân sách token cho một lô hỗn hợp (trình, biểu đồ, ảnh chụp màn hình, ảnh).
  > 打印混合批次(收据、图表、截图、照片) của biểu tượng 预算表。

Số lượng bị bỏ rơi là lý do tại sao mỗi VLM mở năm 2026 sử dụng gói vá.

> Số lượng in được là lý do tại sao mỗi VLM 2026 đều sử dụng các bản vá n'-pack.

## Đưa nó lên mạng

Bài học này sẽ mang lại kết quả `outputs/skill-resolution-budget-planner.md`. Với khối lượng công việc hỗn hợp tỷ lệ khía cạnh (OCR, biểu đồ, ảnh, khung video) và ngân sách tổng cộng token, nó chọn chiến lược phù hợp (NaFlex, AnyRes, M-RoPE, hoặc vuông cố định) và phát ra cấu hình theo yêu cầu. Sử dụng kỹ năng này khi bạn kích thước một VLM cho một sản phẩm  nó ngăn chặn sự bùng nổ token 10x im lặng giết chết ngân sách trễ.

> 本课产 出 `outputs/skill-resolution-budget-planner.md` Được cung cấp hỗn hợp rộng cao hơn tải trọng công việc (OCR, biểu đồ, ảnh, video) và tổng token ngân sách, nó chọn đúng chiến lược (NaFlex, AnyRes, M-RoPE hoặc hình chữ nhật cố định) và tạo ra theo yêu cầu).

> **【中文解读】**本课产出分辨率预算规划工具──给定混合宽高比工作负载和总代币 预算, tự chọn tối ưu nhất策略(NaFlex/AnyRes/M-RoPE/正方形), ngăn chặn sự phân giải không dẫn đến 10 lần token 爆炸──

## Tập luyện bài tập

1. Một hóa đơn là 600x1500 (1:2.5). Ở kích thước vá 14, có bao nhiêu mã thông báo bản địa? bao nhiêu sau khi kích thước vuông lên 336?
   | 一张收据 600x1500（1:2.5）。补丁大小14下，原始分辨率多少 token？缩放到336正方形后多少？实际中哪种 OCR 精度损失更大？

2. Xây dựng mặt nạ hình khối-châm hình cho một loạt bốn hình ảnh với chiều dài 256, 576, 729, 1024.`256^2 + 576^2 + 729^2 + 1024^2`các mục không bằng 0.
   | 为四张长度分别为 256、576、729、1024 的图像构建块对角掩码。验证注意力矩阵为 2585x2585 且非零元素数精确为 `256^2 + 576^2 + 729^2 + 1024^2`。

3. Đối với một hình ảnh 1792x896 ở bản vá 14, so sánh: (a) kích thước vuông thành 336 sau đó mã hóa, (b) AnyRes 2x1 + hình ảnh nhỏ, (c) M-RoPE ở bản địa.
   | 对于 1792x896 的图像（补丁14），对比：(a) 缩放到336正方形，(b) AnyRes 2x1+缩略图，(c) M-RoPE 原始分辨率。哪种 token 最少？哪种保留最多细节？

4. Thực hiện giảm đệm phân đoạn: với một chuỗi đóng gói, thả 50% mã thông báo một cách ngẫu nhiên, và cập nhật mặt nạ khối-châm tương ứng. Đo sự thay đổi độ ít của mặt nạ.
   | 实现分数补丁丢弃：给定打包序列，随机均匀丢弃50%的token，更新块对角掩码，测量掩码稀疏度变化。

5. Đọc Phần 3.2 của bài báo Qwen2-VL (arXiv:2409.12191).`min_pixels`và `max_pixels`kiểm soát và tại sao cả hai ranh giới đều quan trọng.
   | 阅读 Qwen2-VL 论文第 3.2 节（arXiv:2409.12191）。用两句话描述 `min_pixels` 和 `max_pixels` 控制什么，为什么两个边界都很重要。

## Từ khóa  Keyword

| Term | What people say | What it actually means | 中文含义 | 中文释义 |
|------|-----------------|------------------------|----------|---------|
| Patch-n'-pack | "NaViT-style packing" | Concatenate variable-length patch sequences from different images into one batch dimension | 将不同图像的可变长度补丁序列拼接到一个批次维度 | |
| Block-diagonal mask | "Packing mask" | Attention mask that confines each image's patches to attend only to themselves, not neighbors in the pack | 块对角掩码：限制每张图像的补丁只关注自身 | |
| AnyRes | "LLaVA-NeXT tiling" | Split a high-res image into a grid of fixed-size tiles plus a global thumbnail; encode every tile with a fixed encoder | 将高分辨率图像切分为固定大小网格+全局缩略图 | |
| NaFlex | "SigLIP 2 native-flex" | Single SigLIP 2 checkpoint that serves 256/729/1024-token budgets at inference without retraining | 单一 SigLIP 2 checkpoint 推理时支持多种 token 预算 | |
| M-RoPE | "Multimodal RoPE" | 3D rotary position encoding (time, row, column) that handles arbitrary H, W, T without position tables | 三维旋转位置编码（时间、行、列），处理任意宽高和时间长度 | |
| cu_seqlens | "FlashAttention packing" | Cumulative-length tensor the FlashAttention varlen path uses instead of a dense block-diagonal mask | FlashAttention 可变长度路径使用的累积长度张量 | |
| min_pixels / max_pixels | "Resolution bounds" | Qwen2.5-VL per-request knobs capping token count on very small or very large inputs | Qwen2.5-VL 按请求控制最小/最大像素数的参数 | |
| Visual token budget | "How many tokens per image" | Rough count of patch tokens emitted per image; sets the LLM's prompt budget and attention cost | 每张图像产生的补丁 token 数，决定 LLM 的提示预算和注意力成本 | |

## Xem thêm 延伸阅读

- [Dehghani et al. — Patch n' Pack: NaViT (arXiv:2307.06304)](https://arxiv.org/abs/2307.06304)                                                                                                                                                                                                                                                              
- [Wang et al. — Qwen2-VL (arXiv:2409.12191)](https://arxiv.org/abs/2409.12191) Qwen2-VL nhiều hình thức quay vị trí mã hóa
- [Laurençon et al. — What matters when building vision-language models? (Idefics2, arXiv:2405.02246)](https://arxiv.org/abs/2405.02246) Các yếu tố quan trọng để xây dựng VLM
- [Tschannen et al. — SigLIP 2 (arXiv:2502.14786)](https://arxiv.org/abs/2502.14786) Siglip 2 NaFlex
- [Qwen Team — Qwen2.5-VL Technical Report (arXiv:2502.13923)](https://arxiv.org/abs/2502.13923) Quần 2,5 VL  báo cáo kỹ thuật
