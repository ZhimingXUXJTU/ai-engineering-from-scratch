# Trình biến hình (ViT) 视觉 Transformer (ViT)

> Một hình ảnh là một lưới các bản vá. Một câu là một lưới các mã thông báo. cùng một biến thể ăn cả hai.

> **【中文解读】**ViT Đặt hình ảnh cắt thành vá 当作 token 序列处理──理解 ViT = hiểu Transformer không giới hạn ở NLP──CLIP、DALL-E、Sora 都基于Transformer──

**Type:** Hands-on | **类型:** 动手
**Language:**Python**语言:**Python
**Prerequisites:** Phase 7 · 05 (Full Transformer), Phase 4 · 03 (CNNs), Phase 4 · 14 (Vision Transformers intro) | **前置知识:** Phase 7 · 05 (Full Transformer), Phase 4 · 03 (CNNs), Phase 4 · 14 (Vision Transformers intro)
**Time:** ~45 minutes | **时间:** ~45 分钟

## Vấn đề  vấn đề giới thiệu

Trước năm 2020, tầm nhìn máy tính có nghĩa là biến động. Mỗi SOTA trên ImageNet, COCO, và các tiêu chuẩn phát hiện sử dụng một xương sống CNN.

> Trước năm 2020, computer vision có nghĩa là卷积. Mỗi SOTA trên ImageNet, COCO và kiểm tra đều sử dụng mạng lưới cục bộ của CNN.

Dosovitskiy et al. (2020)  "Một hình ảnh có giá trị 16x16 từ"  cho thấy bạn có thể giảm hoàn toàn các biến dạng. Cắt một hình ảnh thành các bản vá kích thước cố định, chiếu theo tuyến tính mỗi bản vá vào một bản nhúng, cung cấp chuỗi cho một bộ mã hóa biến thể vanilla. Ở quy mô đủ (ImageNet-21k trước khi đào tạo hoặc lớn hơn), ViT phù hợp hoặc vượt qua các mô hình dựa trên ResNet.

> Dosovitskiy 等人(2020) "一张图像值 16x16 个词"证明可以完全放弃卷积──将图像切成固定大小的补丁,线性投影每补丁为嵌入,将序列送入标准变压器编码器──在足够大的下规模(ImageNet-21k 预训或更大),ViT có thể匹配或超越基于ResNet的模型──

ViT là khởi đầu của một mô hình rộng hơn vào năm 2026: một kiến trúc, nhiều phương pháp. Whisper biểu thị âm thanh. ViT biểu thị hình ảnh. Action token cho robot. Pixel token cho video. Transformer không quan tâm  cung cấp cho nó một chuỗi và nó học.

> ViT là điểm khởi đầu của xu hướng rộng hơn năm 2026: một cấu trúc, nhiều mô hình. ViT sẽ là biểu tượng hình ảnh.

Đến năm 2026, ViT và các hậu duệ của nó (DeiT, Swin, DINOv2, ViT-22B, SAM 3) sở hữu hầu hết tầm nhìn. CNN vẫn giành chiến thắng trên các thiết bị cạnh và nhiệm vụ nhạy cảm với độ trễ. Mọi thứ khác đều có ViT ở đâu đó trong đống.

> Đến năm 2026, ViT và các thành viên tiếp theo của nó (DeiT, Swin, DINOv2, ViT-22B, SAM3) chiếm phần lớn lĩnh vực thị giác.

> **【中文解读】**ViT's Core Insight: hình ảnh có thể được cắt như văn bản được cắt thành "token" chuỗi. sẽ có 224x224 hình ảnh được cắt thành 14x14 个 16x16 đệm, mỗi đệm sẽ được chiếu theo chiều dài, sau đó được gửi vào tiêu chuẩn Transformer 编码器.

## Khái niệm cốt lõi

![Image → patches → tokens → transformer](../assets/vit.svg)

### Bước 1  Lắp đặt

Chia một `H × W × C`hình ảnh thành một `N × (P·P·C)`Dòng dải phẳng.`224 × 224`hình ảnh, `16 × 16`các bản vá → 196 bản vá có giá trị 768 mỗi.

> sẽ`H × W × C`图像 chia thành `N × (P·P·C)`序列. 平 patch 序列.`224 × 224`Hình ảnh,`16 × 16`Patch → 196 个 768 值的补丁──

```
image (224, 224, 3) → 14 × 14 grid of 16x16x3 patches → 196 vectors of length 768
```

kích thước patch là đòn bẩy. patch nhỏ hơn = nhiều token, độ phân giải tốt hơn, chi phí chú ý vuông. patch lớn hơn = thô hơn, rẻ hơn.

> Patch 大小是控制参数──更小的补丁 = 更多代币、更好的分辨率、二次注意力成本──更大的补丁 = 更粗、更便宜──

### Bước 2  nhúng tuyến tính

Một matrix học tập duy nhất dự đoán mỗi phát phẳng đến `d_model`. Tương đương với một convolution kích thước hạt nhân `P`và bước đi.`P`Trong PyTorch , đây là từ ngữ`nn.Conv2d(C, d_model, kernel_size=P, stride=P)` một thực hiện hai dòng.

> Một mô hình học tập sẽ tạo ra mỗi bản vá phẳng`d_model`◊ giá bằng với hạt nhân`P`、步长为 `P`Trong PyTorch, đó là`nn.Conv2d(C, d_model, kernel_size=P, stride=P)`两行实现。

> **【拓展：Swin Transformer 的层级设计】**标准 ViT sử dụng cố định váy 大小和全局注意力,计算量 O(N^2)。Swin Transformer 引入层级结构:在小补丁上做局部窗口注意力,逐层合并补丁 扩大感受野。这使计算复杂变为O(N),同时保留层级特征提取的能力──Swin 在检测和分任务仍优于标准 ViT。

### Bước 3  Prepend `[CLS]`token, thêm các tích hợp vị trí

- Hãy chuẩn bị cho một bài học được học`[CLS]`Đơn vị ẩn cuối cùng của nó là đại diện hình ảnh được sử dụng để phân loại.
  Trung ngữ翻译: 在开头添加一个可学习的`[CLS]`token──đối cùng được sử dụng để biểu hiện hình ảnh phân loại──
- Thêm các embedment vị trí có thể học được (ViT- gốc) hoặc 2D sinusoidal (những biến thể sau đó).
  Trung文翻译:添加可学习的位置嵌入 (ViT 原始版) 或正弦 2D嵌入 (后续变体)
- Năm 2024+ RoPE mở rộng thành 2D cho vị trí, đôi khi không có nhúng rõ ràng.
  Trung văn翻译:2024 năm sau, RoPE mở rộng sang 2D  vị trí mã hóa, đôi khi không cần phải hiển nhiên cài đặt.

### Bước 4  mã hóa biến đổi tiêu chuẩn

Lập các khối của `LayerNorm → Self-Attention → + → LayerNorm → MLP → +`- Không có lớp đặc biệt về tầm nhìn. Đây là điểm nhấn giáo dục của bài báo.

> 堆叠 L 个 `LayerNorm → Self-Attention → + → LayerNorm → MLP → +`块──与BERT 完全相同──没有视觉特有的层──这是这篇论文的教学要点──

### Bước 5  đầu

Để phân loại: lấy `[CLS]`trạng thái ẩn → tuyến tính → softmax. Đối với DINOv2 hoặc SAM, loại bỏ `[CLS]`, sử dụng các bản che đính trực tiếp.

> 分类:取 `[CLS]`隐藏状态 → 线性层 → softmax── đối với DINOv2 hoặc SAM, bị bỏ rơi `[CLS]`, trực tiếp sử dụng vá 嵌入──

### Các biến thể quan trọng

| Model | Year | Change |
|-------|------|--------|
| 模型 | 年份 | 变化 |
| ViT | 2020 | The original. Fixed patch size, full global attention. |
| ViT | 2020 | 原始版本。固定 patch 大小，全局注意力。 |
| DeiT | 2021 | Distillation; trainable on ImageNet-1k only. |
| DeiT | 2021 | 蒸馏；仅在 ImageNet-1k 上可训练。 |
| Swin | 2021 | Hierarchical with shifted windows. Fixed sub-quadratic cost. |
| Swin | 2021 | 层级结构，移位窗口。固定的亚二次成本。 |
| DINOv2 | 2023 | Self-supervised (no labels). Best general vision features. |
| DINOv2 | 2023 | 自监督（无标签）。最佳通用视觉特征。 |
| ViT-22B | 2023 | 22B params; scaling laws apply. |
| ViT-22B | 2023 | 22B 参数；缩放定律适用。 |
| SigLIP | 2023 | ViT + language pair, sigmoid contrastive loss. |
| SigLIP | 2023 | ViT + 语言配对，sigmoid 对比损失。 |
| SAM 3 | 2025 | Segment anything; ViT-Large + promptable mask decoder. |
| SAM 3 | 2025 | 分割一切；ViT-Large + 可提示的掩码解码器。 |

### Tại sao nó mất một thời gian

ViT cần *chất lượng dữ liệu rất nhiều* để phù hợp với CNN vì nó không có bất kỳ thiên vị cảm ứng của CNN (trình ảnh không thay đổi dịch, địa điểm). Không có hình ảnh có nhãn > 100M hoặc tự giám sát trước khi tập luyện mạnh mẽ, CNN vẫn chiến thắng ở tính toán phù hợp. DeiT đã khắc phục điều này vào năm 2021 bằng các thủ thuật chưng cất; DINOv2 đã khắc phục vĩnh viễn vào năm 2023 bằng tự giám sát.

> ViT cần rất nhiều dữ liệu để phù hợp với hiệu suất của CNN, vì nó không có sự thích hợp về tính năng của CNN (không có hình ảnh đánh dấu hoặc kiểm soát tự kiểm soát cao hơn 1 tỷ张), CNN vẫn thắng trong cùng một số lượng.

> **【中文解读】**ViT có ưu điểm phân bổ yếu là một chiến thuật hai mũi: cần nhiều dữ liệu hơn để phù hợp với hiệu suất của CNN, vì CNN có ưu điểm phân bổ không thay đổi và địa phương.

> **【拓展：ViT 在多模态系统中的角色】**CLIP sử dụng ViT 编码图像、Transformer 编码文本, thông qua đối chiếu học tập đối với hai mô hình. DALL-E 和 Sora sử dụng ViT hiểu hình ảnh/vídeo, tái tạo thành nội dung mới. SAM(Segment Anything) sử dụng ViT như một mạng chủ yếu để thực hiện phân chia hình ảnh chung.

## Hãy xây dựng nó.
```figure
n5-patch-stream
```

## Hãy xây dựng nó

Nhìn xem`code/main.py`Không có đào tạo ViT ở bất kỳ quy mô thực tế nào cần PyTorch và giờ GPU thời gian.

> 参见 `code/main.py`◊ Phân tích các bản tính chuẩn trong bộ nhớ thông tin và các bản ghi nhớ thông tin.

### Bước 1: hình ảnh giả

Một hình ảnh RGB 24 × 24 như một danh sách các hàng của `(R, G, B)`Chúng tôi sử dụng 6×6 patch → 16 patch, mỗi vector nhúng 108-d.

> Một hình ảnh RGB 24 × 24`(R, G, B)`元组的行列表形式表示──使用 6×6 patch → 16 个 patch, mỗi 108 维嵌入向量──

### Bước 2: Lắp đặt

```python
def patchify(image, P):
    H = len(image)
    W = len(image[0])
    patches = []
    for i in range(0, H, P):
        for j in range(0, W, P):
            patch = []
            for di in range(P):
                for dj in range(P):
                    patch.extend(image[i + di][j + dj])
            patches.append(patch)
    return patches
```

Trình tự Raster: hàng lớn trên lưới.

> Trang  序列: 网格上按行优先遍历──每ViT都使用这种排列──

### Bước 3: nhúng tuyến tính

Bội mỗi phố phẳng bằng một số ngẫu nhiên `(patch_flat_size, d_model)`Matrix. kiểm tra hình dạng đầu ra là `(N_patches + 1, d_model)`sau khi chuẩn bị `[CLS]`- Tôi không biết.

> Mỗi đệm sẽ được nhân bằng một đệm tùy ý.`(patch_flat_size, d_model)`矩阵──验证在添加 `[CLS]`后输出形状为 `(N_patches + 1, d_model)`

### Bước 4: đếm các tham số cho ViT thực tế

Bác in số param cho ViT-Base: 12 lớp, 12 đầu, d=768, vá=16. So sánh với ResNet-50 (~25M). ViT-Base hạ cánh ở ~86M. ViT-Large ~307M. ViT-Huge ~632M.

> 打印 ViT-Base 的参数:12 层、12 头、d=768、patch=16──与ResNet-50(约25M) đối比──ViT-Base 约86M──ViT-Large 约307M──ViT-Huge 约632M──

## Hãy sử dụng nó để thực hiện

```python
from transformers import ViTImageProcessor, ViTModel
import torch
from PIL import Image

processor = ViTImageProcessor.from_pretrained("google/vit-base-patch16-224-in21k")
model = ViTModel.from_pretrained("google/vit-base-patch16-224-in21k")

img = Image.open("cat.jpg")
inputs = processor(img, return_tensors="pt")
out = model(**inputs).last_hidden_state   # (1, 197, 768): [CLS] + 196 patches
cls_emb = out[:, 0]                       # image representation
```

**DINOv2 embeddings are the 2026 default for image features.**Làm lạnh xương sống, tập luyện một cái đầu nhỏ. Nó hoạt động cho phân loại, lấy lại, phát hiện, ghi chú. Các điểm kiểm tra DINOv2 của Meta vượt qua CLIP trong mọi nhiệm vụ nhìn không văn bản.

> **DINOv2 嵌入是 2026 年图像特征的默认选择。**结骨干网络,训练一个小头──适用于分类,检查,检测,图像描述──Meta's DINOv2 检查点在每个非文本视觉任务上都优于CLIP──

**Patch-size picking.**Các mô hình nhỏ sử dụng 16×16 (ViT-B/16). Dự đoán mật (tín phân) sử dụng 8×8 hoặc 14×14 (SAM, DINOv2).

> **Patch 大小选择。**小模型使用 16×16(ViT-B/16)。密集预测(分割) sử dụng 8×8 hoặc 14×14(SAM、DINOv2)。 rất lớn模型使用 14×14。

## Chuyển nó đi.

Nhìn xem`outputs/skill-vit-configurator.md`. Khả năng chọn một biến thể ViT và kích thước vá cho một nhiệm vụ tầm nhìn mới do kích thước tập dữ liệu, độ phân giải và ngân sách tính toán.

> 参见 `outputs/skill-vit-configurator.md` Kỹ năng này dựa trên bộ dữ liệu, độ phân giải và ngân sách tính toán, để chọn các nhiệm vụ mới của video

## Tập luyện bài tập

1. **Easy.**Đi chạy`code/main.py`- Kiểm tra số lượng các vết bẻ bằng nhau`(H/P) * (W/P)`và kích thước của đệm phẳng bằng nhau `P*P*C`- Tôi không biết.
   Trung ngữ翻译:运行 `code/main.py` Kiểm tra đệm số lượng bằng `(H/P) * (W/P)`,平 patch 维度等于 `P*P*C`
2. **Medium.**Thực hiện 2D sinusoidal vị trí nhúng  hai mã sinusoidal độc lập cho `row`và `col`Đưa chúng vào một PyTorch ViT nhỏ và so sánh độ chính xác vs. các vị trí có thể học được trên CIFAR-10.
   Trung文翻译:实现 2D 正弦位置嵌入每个补丁的`row`和 `col`独立编码后拼接──在小型 PyTorch ViT 上使用,与可学习位置嵌入在CIFAR-10 上对比准确率──
3. **Hard.**Xây dựng một ViT (PyTorch) 3 tầng, đào tạo trên 1.000 hình ảnh MNIST với 4×4 bản vá. đo độ chính xác của thử nghiệm. Bây giờ thêm DINOv2 trước khi đào tạo trên cùng 1.000 hình ảnh (đơn giản hóa: chỉ cần đào tạo trình mã hóa để dự đoán nhúng bản vá từ các bản vá che giấu).
   中文翻译:构建 3层 ViT(PyTorch), sử dụng 4×4 patch 在 1,000 张 MNIST 图像上训练。测量测试准确率。然后添加 DINOv2 预训练(简化版:训练编码器从掩码补丁 预测补丁 嵌入) ――准确率是否提升?

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Patch | "The vision-transformer token" | Flat vector of pixel values for a `P × P × C` region of the image. |
| Patch | "视觉 Transformer 的 token" | 图像中 `P × P × C` 区域的像素值扁平向量。 |
| Patchify | "Chop + flatten" | Slice image into non-overlapping patches, flatten each to a vector. |
| Patchify | "切分 + 展平" | 将图像切成不重叠的 patch，每个展平为向量。 |
| `[CLS]` token | "The image summary" | Prepended learnable token; its final embedding is the image representation. |
| `[CLS]` token | "图像摘要" | 预置的可学习 token；其最终嵌入是图像表示。 |
| Inductive bias | "What the model assumes" | ViT has fewer priors than CNNs; needs more data to make up the gap. |
| 归纳偏好 | "模型假设了什么" | ViT 的先验比 CNN 少；需要更多数据来弥补差距。 |
| DINOv2 | "Self-supervised ViT" | Trained without labels using image augmentation + momentum teacher. Best general image features in 2026. |
| DINOv2 | "自监督 ViT" | 使用图像增强 + 动量教师无标签训练。2026 年最佳通用图像特征。 |
| SigLIP | "CLIP's successor" | ViT + text encoder trained with sigmoid contrastive loss; better than CLIP on matched compute. |
| SigLIP | "CLIP 的继承者" | 用 sigmoid 对比损失训练的 ViT + 文本编码器；相同计算量下优于 CLIP。 |
| Swin | "Windowed ViT" | Hierarchical ViT with local attention + shifted windows; sub-quadratic. |
| Swin | "窗口 ViT" | 带局部注意力 + 移位窗口的层级 ViT；亚二次复杂度。 |
| Register tokens | "2023 trick" | A few extra learnable tokens that soak up attention sinks; improves DINOv2 features. |
| Register tokens | "2023 技巧" | 几个额外的可学习 token，吸收注意力汇聚；改善 DINOv2 特征。 |

## Xem thêm 延伸阅读

- [Dosovitskiy et al. (2020). An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale](https://arxiv.org/abs/2010.11929) tờ ViT.
  Trung ngữ翻译:ViT 原始论文。
- [Touvron et al. (2021). Training data-efficient image transformers & distillation through attention](https://arxiv.org/abs/2012.12877) Định nghĩa.
  Trung ngữ翻译:DeiT 论文。
- [Liu et al. (2021). Swin Transformer: Hierarchical Vision Transformer using Shifted Windows](https://arxiv.org/abs/2103.14030) Động.
  Trung文翻译:Swin Transformer 论文。
- [Oquab et al. (2023). DINOv2: Learning Robust Visual Features without Supervision](https://arxiv.org/abs/2304.07193) DINOv2.
  Trung ngữ翻译:DINOv2 论文。
- [Darcet et al. (2023). Vision Transformers Need Registers](https://arxiv.org/abs/2309.16588) sửa đổi mã đăng ký cho DINOv2.
  Trung文翻译:DINOv2 的注册代码 修复论文。
