# Độ sâu đơn phương & Định lượng hình học      

> Bản đồ độ sâu là một hình ảnh một kênh mà mỗi pixel là khoảng cách từ máy ảnh. Dự đoán nó từ một khung RGB đã không thể được thực hiện mà không có stereo hoặc LiDAR. Năm 2026, một bộ mã hóa ViT đóng băng cộng với một đầu nhẹ sẽ đạt được trong vài phần trăm của sự thật mặt đất.

> **【中文解读】**Độ sâu là hình ảnh một đường, mỗi giá trị của hình ảnh biểu thị khoảng cách của camera. Từ một张 RGB  hình ảnh dự đoán độ sâu từng được coi là không thể (đáng cần hai mắt hoặc LiDAR), nhưng năm 2026 ViT 编码器 + 轻量级解码器 đã có thể đạt được độ chính xác gần đúng giá trị.

> **【拓展：深度估计的应用】**单目深度估计在自动驾驶 (单目深度估计在自动驾驶) 补充 LiDAR (AR/VR) 场景理解) 机器人导航、3D 照片效果 (背景虚化)                                                                                                                                                                                                                                  

**Type:** Build + Use | **类型:** 动手 + 应用
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 4 Lesson 14 (ViT), Phase 4 Lesson 17 (Self-Supervised Vision), Phase 4 Lesson 07 (U-Net) | **前置知识:** Phase 4 Lesson 14（ViT），Phase 4 Lesson 17（自监督视觉），Phase 4 Lesson 07（U-Net）
**Time:** ~60 minutes | **时间:** ~60 分钟

## Mục tiêu học tập

- Sự phân biệt độ sâu tương đối và độ sâu métric và trạng thái mà mỗi mô hình sản xuất (MiDaS, Marigold, Depth Anything V3, ZoeDepth) giải quyết
- Sử dụng độ sâu bất cứ điều gì V3 (DINOv2 backbone) để dự đoán độ sâu cho hình ảnh độc lập tùy ý mà không có hiệu chuẩn
- Giải thích tại sao độ sâu đơn hình hoạt động từ một hình ảnh duy nhất (số quan điểm, độ nghiêng kết cấu, tiền lệ học) và điều gì nó không thể phục hồi (sự quy mô tuyệt đối, hình học bị che)
- Tăng phát hiện 2D đến các điểm 3D bằng cách sử dụng bản đồ độ sâu và nội tại của máy ảnh pinhole

> **【中文解读】**Mục tiêu học tập được liệt kê trong danh sách các khả năng cốt lõi cần được nắm bắt sau khi hoàn thành bài học.


## Vấn đề  vấn đề giới thiệu

Độ sâu là trục thiếu trong tầm nhìn máy tính 2D. Với RGB, bạn biết mọi thứ xuất hiện ở vị trí hình ảnh; bạn không biết chúng ở xa như thế nào.

> Độ sâu là một trục thiếu trong hình ảnh máy tính 2D. Với RGB, bạn biết vị trí của vật thể trên hình ảnh; bạn không biết chúng có bao nhiêu.

Đánh giá độ sâu đơn  dự đoán độ sâu từ một khung RGB  được sử dụng để tạo ra đầu ra mờ, không đáng tin cậy. Đến năm 2026, các bộ mã hóa được đào tạo trước đã thay đổi điều này: Depth Anything V3 sử dụng xương sống DINOv2 đóng băng và sản xuất bản đồ độ sâu phổ biến trên các lĩnh vực nội thất, ngoài trời, y tế và vệ tinh. Marigold tái định hình độ sâu như là một vấn đề phân tán điều kiện. ZoeDepth lùi lại khoảng cách chính xác.

> 单目深度估计从单个RGB 预测深度过去产生模糊、不可靠的输出──到2026年大型预训编码器改变了这一点:深度任何东西 V3 使用结的DINOv2骨干并产生跨室内,室外,医学和卫星领域泛化的深度图──Marigold sẽ định nghĩa lại chiều sâu như là vấn đề mở rộng điều kiện──ZoeDepth trở lại với khoảng cách công cộng thực tế──

Độ sâu cũng là cầu nối giữa phát hiện 2D và hiểu biết 3D: nhân các pixel của một hộp phát hiện bằng độ sâu và bạn nâng đối tượng 2D lên thành một đám mây điểm 3D. Đó là lõi của mọi hệ thống che giấu AR, mọi đường ống dẫn tránh trở ngại và mọi robot "tăng tách".

> Độ sâu cũng là cầu nối giữa 2D kiểm tra và 3D hiểu: sẽ kiểm tra hình ảnh của khung nhân độ sâu, bạn sẽ có thể nâng cao vật thể 2D lên 3D điểm. Đó là cốt lõi của mỗi AR 遮 hệ thống, mỗi rào cản dòng chảy nước và mỗi "tăng cốc" của máy tính.

## Khái niệm cốt lõi

> **【中文解读】**Bài viết này giới thiệu các khái niệm và lý thuyết cốt lõi.


### Tâm độ tương đối đối với độ sâu métric

- **Relative depth** được ra lệnh `z`"Pixel A gần hơn so với pixel B, nhưng tỷ lệ khoảng cách không được neo với mét".
  Trung ngữ翻译:**相对深度** có thứ tự `z`值,没有真实世界单位──"Bài hình A so với B gần, nhưng tỷ lệ khoảng cách không xác định đến米──"
- **Metric depth** khoảng cách tuyệt đối trong mét từ máy ảnh.
  Trung ngữ翻译:**度量深度** Từ từ từ từ từ từ từ từ từ khoảng cách tuyệt đối (米) ◊ cần học mô hình để tìm ra mối quan hệ thống giữa đường dẫn hình ảnh và khoảng cách thực sự.

MiDaS và Depth Anything V3 tạo ra độ sâu tương đối. Marigold tạo ra độ sâu tương đối. ZoeDepth, UniDepth và Metric3D tạo ra độ sâu métric.

> MiDaS và Độ sâu Bất cứ điều gì V3  tạo tương đối với độ sâu.

### Mô hình mã hóa-chế vị mã hóa

```mermaid
flowchart LR
    IMG["Image (H x W x 3)"] --> ENC["Frozen ViT encoder<br/>(DINOv2 / DINOv3)"]
    ENC --> FEATS["Dense features<br/>(H/14, W/14, d)"]
    FEATS --> DEC["Depth decoder<br/>(conv upsampler,<br/>DPT-style)"]
    DEC --> DEPTH["Depth map<br/>(H, W, 1)"]

    style ENC fill:#dbeafe,stroke:#2563eb
    style DEC fill:#fef3c7,stroke:#d97706
    style DEPTH fill:#dcfce7,stroke:#16a34a
```

Depth Anything V3 đóng băng bộ mã hóa và chỉ đào tạo bộ mã hóa kiểu DPT. Bộ mã hóa cung cấp các tính năng phong phú; bộ mã hóa liên kết chúng trở lại độ phân giải hình ảnh và giảm độ sâu.

> Độ sâu bất cứ điều gì V3 结编码器, chỉ tập luyện DPT 风格的解码器──编码器提供丰富特征;解码器将它们插值回图像分辨率并回归深度──

### Tại sao một hình ảnh duy nhất tạo ra độ sâu

Một hình ảnh 2D chứa nhiều tín hiệu đơn hình tương quan với độ sâu:

> Một bức ảnh 2D chứa nhiều chỉ dẫn liên quan đến độ sâu:

- **Perspective** Các đường song song trong 3D hội tụ trong 2D.
  Trung ngữ翻译:**透视**3D trung tâm đường平行线在2D trung tâm汇聚──
- **Texture gradient** bề mặt xa có kết cấu nhỏ hơn, dày đặc hơn.
  Trung ngữ翻译:**纹理梯度**                                                                                                                                                                                                                                                              
- **Occlusion order** Các vật thể gần hơn che giấu những vật thể xa hơn.
  Trung ngữ翻译:**遮挡顺序** gần ờng ờng ờng ờng ờng ờng ờng ờng ờng ờng
- **Size constancy** các vật thể được biết (các chiếc xe hơi, con người) cho phép quy mô gần như.
  Trung ngữ翻译:**大小恒常性** đã biết vật thể (车、人) cho phép đo gần như.
- **Atmospheric perspective** Các vật thể xa trông mờ hơn và xanh hơn trong cảnh ngoài trời.
  Trung ngữ翻译:**大气透视** đồ vật ở xa trong cảnh ngoài trời xuất hiện rõ hơn  màu xanh hơn.

Một ViT được đào tạo trên hàng tỷ hình ảnh nội bộ hóa các tín hiệu này. Với đủ dữ liệu và xương sống mạnh mẽ, độ sâu đơn hình đạt độ chính xác hợp lý mà không cần bất kỳ giám sát 3D rõ ràng.

> Trong hàng tỷ hình ảnh, ViT sẽ tập trung vào các đường dẫn này. Với đủ dữ liệu và cơ sở xương mạnh, không cần bất kỳ độ sâu 3D nào để kiểm soát rõ ràng để đạt được độ chính xác hợp lý.

### Độ sâu đơn hình không thể làm gì

- **Absolute metric scale**Không có nội tại hoặc một đối tượng được biết trong hiện trường. mạng có thể dự đoán "cốc là hai lần xa hơn muỗng" mà không biết liệu cốc là 1 m hoặc 10 m xa.
- **Occluded geometry** mặt sau của một chiếc ghế không thể nhìn thấy và không thể suy luận đáng tin cậy.
- **Truly untextured / reflective surfaces** gương, kính, tường đồng nhất.

### Độ sâu bất cứ điều gì V3 vào năm 2026

- Vanilla DINOv2 ViT-L/14 như một bộ mã hóa (đóng).
- DPT decoder.
- Được đào tạo trên các cặp hình ảnh được đặt từ nhiều nguồn khác nhau (không cần giám sát độ sâu rõ ràng ngoài sự nhất quán quang học).
- Dự đoán hình học không gian phù hợp từ **an arbitrary number of visual inputs, with or without known camera poses**- Tôi không biết.
- SOTA trên độ sâu đơn hình, hình học bất kỳ quan sát, hình ảnh hiển thị, camera định hình ước tính.

Đây là mô hình để gọi khi bạn cần độ sâu vào năm 2026.

> Đây là mô hình được sử dụng trực tiếp vào năm 2026

### Marigold  phân tán cho độ sâu

Marigold (Ke et al., CVPR 2024) tái định hình ước tính độ sâu như là sự phân tán hình ảnh theo điều kiện. Điều kiện: RGB. Mục tiêu: bản đồ độ sâu. Sử dụng một U-Net Stable Diffusion 2 được đào tạo trước như là xương sống. Bản đồ độ sâu sản xuất là đặc biệt sắc ở ranh giới đối tượng. Trade-off: suy luận chậm hơn so với các mô hình cấp dữ liệu (10-50 bước từ chối).

> Marigold(Ke 等,CVPR 2024) sẽ định nghĩa lại khung hình ước tính độ sâu để điều kiện hình ảnh đến hình ảnh của sự lan rộng.

### Bản chất và máy ảnh lỗ vít

Để nâng một pixel `(u, v)`với độ sâu `d`đến một điểm 3D `(X, Y, Z)`trong các tọa độ máy ảnh:

```
fx, fy, cx, cy = camera intrinsics
X = (u - cx) * d / fx
Y = (v - cy) * d / fy
Z = d
```

Bản chất đến từ siêu dữ liệu EXIF, một mô hình hiệu chuẩn hoặc một ước tính bản chất đơn (Perspective Fields, UniDepth).

### Đánh giá

Hai chỉ số tiêu chuẩn:

- **AbsRel**(sự sai lầm tương đối tuyệt đối): `mean(|d_pred - d_gt| / d_gt)`Tối thấp hơn là tốt hơn. 0,05-0,1 cho các mô hình sản xuất.
- **delta < 1.25**(sự chính xác ngưỡng): phần nhỏ của các pixel nơi `max(d_pred/d_gt, d_gt/d_pred) < 1.25`Tăng hơn thì tốt hơn. 0,9+ cho SOTA.

Đối với độ sâu tương đối (Depth Anything V3, MiDaS), đánh giá sử dụng các phiên bản không biến đổi quy mô và chuyển động của cả hai số liệu.

> **【中文解读】**本节通过代码实现核心算法从零――这种" từ đầu"的方式能帮助理解框架背后的原理,遇到问题时不会被黑盒困住――

> **【拓展：工业部署中的视觉系统】**Trong thực tế, mô hình hình ảnh cần phải xem xét các vấn đề về sự chậm trễ, mô hình lớn, thiết bị cạnh phù hợp, vv.

> **【拓展：数据标注与质量】**视觉任务的效果高度依赖标签数据质量――Label Studio、CVAT là công cụ标签 chính thống――在工业场景中,主动学习(Active Learning) có thể giảm chi phí đánh dấu: mô hình đối với yêu cầu mẫu không xác định




## Hãy xây dựng nó.
```figure
depth-sweep
```

## Hãy xây dựng nó

### Bước 1: Métric độ sâu

```python
import torch

def abs_rel_error(pred, target, mask=None):
    if mask is not None:
        pred = pred[mask]
        target = target[mask]
    return (torch.abs(pred - target) / target.clamp(min=1e-6)).mean().item()


def delta_accuracy(pred, target, threshold=1.25, mask=None):
    if mask is not None:
        pred = pred[mask]
        target = target[mask]
    ratio = torch.maximum(pred / target.clamp(min=1e-6), target / pred.clamp(min=1e-6))
    return (ratio < threshold).float().mean().item()
```

Luôn che dấu các pixel độ sâu không hợp lệ (không, NaN, bão hòa) trước khi đánh giá.

### Bước 2: Định hướng quy mô và chuyển động

Đối với các mô hình độ sâu tương đối, hãy sắp xếp dự đoán với sự thật cơ bản trước khi tính toán métrics.`a * pred + b = target`- Có thể là:

```python
def align_scale_shift(pred, target, mask=None):
    if mask is not None:
        p = pred[mask]
        t = target[mask]
    else:
        p = pred.flatten()
        t = target.flatten()
    A = torch.stack([p, torch.ones_like(p)], dim=1)
    coeffs, *_ = torch.linalg.lstsq(A, t.unsqueeze(-1))
    a, b = coeffs[:2, 0]
    return a * pred + b
```

Đi chạy`align_scale_shift`trước đây`abs_rel_error`khi đánh giá MiDaS / Depth Anything.

### Bước 3: Tăng độ sâu lên một đám mây điểm

```python
import numpy as np

def depth_to_point_cloud(depth, intrinsics):
    H, W = depth.shape
    fx, fy, cx, cy = intrinsics
    v, u = np.meshgrid(np.arange(H), np.arange(W), indexing="ij")
    z = depth
    x = (u - cx) * z / fx
    y = (v - cy) * z / fy
    return np.stack([x, y, z], axis=-1)


depth = np.random.uniform(0.5, 4.0, (240, 320))
intr = (320.0, 320.0, 160.0, 120.0)
pc = depth_to_point_cloud(depth, intr)
print(f"point cloud shape: {pc.shape}  (H, W, 3)")
```

Một chức năng, mỗi ứng dụng được nâng 3D. Xuất khẩu đám mây điểm đến `.ply`và mở trong MeshLab hoặc CloudCompare.

### Bước 4: Kiểm tra khói với cảnh độ sâu tổng hợp

```python
def synthetic_depth(size=96):
    yy, xx = np.meshgrid(np.arange(size), np.arange(size), indexing="ij")
    # Floor: linear gradient from near (top) to far (bottom)
    depth = 1.0 + (yy / size) * 4.0
    # Box in the middle: closer
    mask = (np.abs(xx - size / 2) < size / 6) & (np.abs(yy - size * 0.6) < size / 6)
    depth[mask] = 2.0
    return depth.astype(np.float32)


gt = torch.from_numpy(synthetic_depth(96))
pred = gt + 0.3 * torch.randn_like(gt)  # simulated prediction
aligned = align_scale_shift(pred, gt)
print(f"before align  absRel = {abs_rel_error(pred, gt):.3f}")
print(f"after align   absRel = {abs_rel_error(aligned, gt):.3f}")
```

### Bước 5: Độ sâu bất cứ điều gì sử dụng V3 (chỉ dẫn)

```python
import torch
from transformers import pipeline
from PIL import Image

pipe = pipeline(task="depth-estimation", model="LiheYoung/depth-anything-v2-large")

image = Image.open("street.jpg").convert("RGB")
out = pipe(image)
depth_np = np.array(out["depth"])
```

> **【中文解读】**Bài này sẽ trình bày cách sử dụng một khung đã phát triển như PyTorch, HuggingFace, và các khác.


Ba dòng.`out["depth"]`là một PIL thang xám; chuyển đổi thành numpy cho toán học. Đối với Depth Anything V3 cụ thể, thay đổi ID mô hình một khi được phát hành; API không thay đổi.




> **【拓展：视觉模型的持续学习】**Trong môi trường sản xuất, mô hình hình ảnh cần phải liên tục thích ứng với dữ liệu mới.

## Hãy sử dụng nó để thực hiện

- **Depth Anything V3**(Meta AI / ByteDance, 2024-2026)  mặc định cho độ sâu tương đối. mô hình viT lớn nhanh nhất trong sản xuất.
- **Marigold**(ETH, 2024)  chất lượng thị giác cao nhất, suy luận chậm.
- **UniDepth**(ETH, 2024)  độ sâu métric với ước tính nội tại của máy ảnh.
- **ZoeDepth**(Intel, 2023)  độ sâu mét; cũ hơn, vẫn đáng tin cậy.
- **MiDaS v3.1** di sản nhưng ổn định; điểm cơ sở tốt để so sánh.

Mô hình tích hợp điển hình:

1. RGB frame đến.
2. Mô hình độ sâu tạo ra bản đồ độ sâu.
3. Máy phát hiện tạo ra hộp.
4. Lift hộp trung tâm thông qua độ sâu đến 3D; hợp nhất với đám mây điểm nếu có sẵn.
5. Hậu: Khóa AR, lập kế hoạch đường, ước tính kích thước đối tượng, thay thế âm thanh.

> **【中文解读】**Phần này tập trung vào cách phân phối mô hình như một sản phẩm có thể sử dụng.


Để sử dụng thời gian thực, Depth Anything V2 Small (INT8 lượng hóa) đạt ~ 30 fps trên GPU tiêu dùng ở 518x518.



## Chuyển nó đi.

> **【中文解读】**练题按照 Easy/Medium/Hard 三个难度递进;;建议至少完成 级别的题目, 级别适合深入研究或面试准备;;


Bài học này mang lại:

- `outputs/prompt-depth-model-picker.md` chọn giữa Depth Anything V3, Marigold, UniDepth, MiDaS cho thời gian trễ, metric-vs-relative need, và kiểu cảnh.
- `outputs/skill-depth-to-pointcloud.md` một kỹ năng xây dựng đám mây điểm từ các bản đồ độ sâu với xử lý nội tại chính xác và xuất khẩu đến `.ply`- Tôi không biết.

## Tập luyện bài tập

1. **(Easy)**Chạy độ sâu bất cứ điều gì V2 trên bất kỳ 10 hình ảnh của bàn của bạn. Giữ độ sâu như PNGs thang xám và kiểm tra. Xác định một đối tượng có độ sâu dự đoán sai và giải thích tại sao các tín hiệu đơn hình thất bại.
2. **(Medium)**Với RGB + độ sâu từ Depth Anything V2, nâng lên một đám mây điểm và hiển thị với `open3d`So sánh hai cảnh (trên / ngoài trời) và ghi chú xem có vẻ đáng tin cậy hơn.
3. **(Hard)**Hãy lấy năm cặp hình ảnh chỉ khác nhau bởi vị trí của một đối tượng được biết (ví dụ: chai di chuyển gần hơn 30 cm). Sử dụng UniDepth để dự đoán độ sâu métric trên cả hai.

> **【中文解读】**Trong 术语表中的"Những gì mọi người nói" vs "Những gì nó thực sự có nghĩa" 区分日常口语和精确技术含义── 在团队协作中,统一术语定义可以避免大量沟通误解──


## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Monocular depth | "Single-image depth" | Depth estimation from one RGB frame, no stereo or LiDAR |
| Relative depth | "Ordered depth" | Ordered z-values without real-world units |
| Metric depth | "Absolute distance" | Depth in metres; requires calibration or a model trained with metric supervision |
| AbsRel | "Absolute relative error" | Mean of |d_pred - d_gt| / d_gt; standard depth metric |
| Delta accuracy | "delta < 1.25" | Fraction of pixels with prediction within 25% of ground truth |
| Pinhole camera | "fx, fy, cx, cy" | The camera model used to lift (u, v, d) to (X, Y, Z) |
| DPT | "Dense Prediction Transformer" | The conv-based decoder used on top of frozen ViT encoders for depth |
| DINOv2 backbone | "The reason it works" | Self-supervised features that generalise across domains without depth labels |

> **【中文解读】**延伸阅读 cung cấp các nguồn chất lượng cao cho việc học sâu. Những bài báo và giảng dạy này là tài liệu tham khảo cổ điển trong lĩnh vực này, phù hợp với những người đọc cần hiểu sâu hơn.


## Xem thêm 延伸阅读

- [Depth Anything V3 paper page](https://depth-anything.github.io/) Độ sâu SOTA đơn hình với mã hóa DINOv2
- [Marigold (Ke et al., CVPR 2024)](https://marigoldmonodepth.github.io/) Đánh giá độ sâu dựa trên sự phân tán
- [UniDepth (Piccinelli et al., 2024)](https://arxiv.org/abs/2403.18913) Độ sâu métric với nội tại
- [MiDaS v3.1 (Intel ISL)](https://github.com/isl-org/MiDaS) đường cơ sở tương đối sâu của các dòng truyền giáo
- [DINOv3 blog post (Meta)](https://ai.meta.com/blog/dinov3-self-supervised-vision-model/) gia đình mã hóa nâng độ chính xác độ sâu
