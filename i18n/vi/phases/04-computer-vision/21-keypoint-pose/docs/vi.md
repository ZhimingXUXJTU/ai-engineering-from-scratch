# Khám phá điểm chính & ước tính vị trí .

> Một tư thế là một tập hợp các điểm khóa được sắp xếp. Một máy dò điểm khóa là một máy quay lại bản đồ nhiệt. Mọi thứ khác là kế toán.

> **【中文解读】**姿态 là một nhóm các điểm quan trọng có trật tự như của cơ thể người (tương tự như 17 个关节点) ⋅ 关键点检测器 bản chất là một thiết bị quay trở về nhiệt lực lượng để dự đoán một tỷ lệ nhiệt lực lượng cho mỗi điểm quan trọng ⋅ 姿态 ước tính được sử dụng rộng rãi trong phân tích vận động、人机交互和AR 镜──

> **【拓展：姿态估计的应用】**OpenPose、MediaPipe、YOLO-Pose là một công cụ đánh giá thái độ thường thấy.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 4 Lesson 06 (Detection), Phase 4 Lesson 07 (U-Net) | **前置知识:** Phase 4 Lesson 06（目标检测），Phase 4 Lesson 07（U-Net）
**Time:** ~45 minutes | **时间:** ~45 分钟

## Mục tiêu học tập

- Sự khác biệt giữa ước tính tư thế từ trên xuống và từ dưới lên và nói khi nào mỗi người được sử dụng
- Hình ảnh nhiệt hồi phục cho các điểm khóa K với mục tiêu Gaussian-per-keypoint và trích xuất các điều phối điểm khóa tại suy luận
- Giải thích các trường liên quan phần (PAF) và cách các đường ống từ dưới lên liên kết các điểm khóa thành các trường hợp
- Sử dụng MediaPipe Pose hoặc MMPose để ước tính điểm chính sản xuất và hiểu định dạng đầu ra của chúng

> **【中文解读】**Mục tiêu học tập được liệt kê trong danh sách các khả năng cốt lõi cần được nắm bắt sau khi hoàn thành bài học.


## Vấn đề  vấn đề giới thiệu

Các nhiệm vụ chủ chốt ẩn dưới nhiều tên: tư thế con người (17 khớp cơ thể), dấu hiệu khuôn mặt (68 hoặc 478 điểm), tay (21 điểm), tư thế động vật, tư thế vật robot, các dấu hiệu giải phẫu y tế.

> 关键点任务隐藏在许多名称下: 的人体姿态(17 个身体关节) 面部特征点(68 hoặc 478 个点) 手部(21 个点) 动物姿态、机器人物体姿态、医学解剖标志── mỗi người có cấu trúc giống nhau: kiểm tra vật thể trên K 个离散点并输出它们的 (x, y) 坐标──

Tín hình hình ảnh là nền tảng của chụp chuyển động, ứng dụng thể dục, phân tích thể thao, kiểm soát cử chỉ, hoạt hình, thử nghiệm AR và nắm bắt robot.

> 姿势估计是动作捕捉,健身应用,运动分析,手势控制,动画,AR 试穿和机器人抓取的基础――2D 情况已经成熟;3D 姿势(从单个相机估计世界坐标中的关节位置) là một nghiên cứu hiện tại.

Câu hỏi kỹ thuật là quy mô. Một hình ảnh đơn, một người tư thế là một vấn đề 20ms.

> 工程问题是规模――单图片、单人姿态是一个20ms的问题――群体中30fps的多人姿态是一个不同结构的不同的问题――

## Khái niệm cốt lõi

> **【中文解读】**Bài viết này giới thiệu các khái niệm và lý thuyết cốt lõi.


### Từ trên xuống xuống xuống

```mermaid
flowchart LR
    subgraph TD["Top-down pipeline"]
        A1["Detect person boxes"] --> A2["Crop each box"]
        A2 --> A3["Per-box keypoint model<br/>(HRNet, ViTPose)"]
    end
    subgraph BU["Bottom-up pipeline"]
        B1["One pass over image"] --> B2["All keypoint heatmaps<br/>+ association field"]
        B2 --> B3["Group keypoints into<br/>instances (greedy matching)"]
    end

    style TD fill:#dbeafe,stroke:#2563eb
    style BU fill:#fef3c7,stroke:#d97706
```

- **Top-down** phát hiện người trước tiên, sau đó chạy mô hình điểm khóa cho mỗi người trên mỗi cây trồng. Độ chính xác cao nhất; cân bằng theo đường thẳng với số người.
  Trung ngữ翻译:**自顶向下** Đầu tiên kiểm tra khung người, sau đó mở rộng từng khu vực cắt.
- **Bottom-up** một bước đi trước dự đoán tất cả các điểm khóa cộng với một trường liên kết; nhóm chúng. Thời gian liên tục bất kể kích thước đám đông.
  Trung ngữ翻译:**自底向上** một lần trước hướng truyền tải tiên đoán tất cả các điểm quan trọng; rồi分组── bất kể số lượng người là số lượng thường xuyên──

Top-down (HRNet, ViTPose) là người dẫn đầu độ chính xác; bottom-up (OpenPose, HigherHRNet) là người dẫn đầu thông qua cho các cảnh đông đúc.

> 自顶向下(HRNet、ViTPose) là người lãnh đạo độ cao;自底上;;OpenPose、HigherHRNet) là người lãnh đạo lượng tràn ngập của cảnh tượng đông đúc。

### Khung trở lại bản đồ nhiệt

Thay vì lùi lại `(x, y)`trực tiếp, dự đoán một `H x W`heatmap mỗi điểm khóa với một khối Gaussian tập trung vào vị trí thực.

> Không quay lại trực tiếp`(x, y)`, nhưng cho mỗi điểm quan trọng`H x W`热力图, đặt ở trung tâm vị trí thực

```
target[k, y, x] = exp(-((x - cx_k)^2 + (y - cy_k)^2) / (2 sigma^2))
```

Khi suy luận, argmax của mỗi heatmap là vị trí điểm khóa dự đoán.

Tại sao heatmaps hoạt động tốt hơn so với sự lùi ngược trực tiếp: cấu trúc không gian của mạng (conv feature map) tự nhiên phù hợp với đầu ra không gian.

> Tại sao nhiệt lực图 tốt hơn trực tiếp trở lại: cấu trúc không gian của mạng (volume of space) với không gian ra ngoài tự nhiên đối với sự ổn định.

### Định vị vị của các subpixel

Argmax cho các tọa độ nguyên số. Để chính xác sub-pixel, tinh chỉnh bằng cách gắn một hình ngụng vào argmax và các hàng xóm của nó, hoặc sử dụng các ofset nổi tiếng `(dx, dy) = 0.25 * (heatmap[y, x+1] - heatmap[y, x-1], ...)`hướng đi.

> Argmax  đưa ra số trọn ⋅ để đạt được độ chính xác của hình ảnh, có thể qua được đối với argmax  và các đường tròn phù hợp với các vùng lân cận ⋅ để tinh chỉnh

### Các lĩnh vực liên quan phần (PAF)

OpenPose's thủ thuật cho kết nối từ dưới lên. Đối với mỗi cặp điểm khóa kết nối (ví dụ: vai trái đến khuỷu tay trái), dự đoán một lĩnh vực 2 kênh mã hóa vector đơn vị chỉ ra từ một đến một. Để kết nối một vai với khuỷu tay của nó, tích hợp PAF dọc theo đường nối cặp ứng cử viên; cặp có tích hợp cao nhất được kết hợp.

```
For each connection (limb):
  PAF channels: 2 (unit vector x, y)
  Line integral: sum over sample points of (PAF . line_direction)
  Higher integral = stronger match
```

Tốt và quy mô đến kích thước đám đông tùy ý mà không có cây trồng cho mỗi người.

### Các điểm khóa COCO

Bộ dữ liệu đặt cơ thể tiêu chuẩn: 17 điểm khóa mỗi người, PCK (Tỷ lệ phần trăm điểm khóa chính xác) và OKS (Tương tự điểm khóa đối tượng) như là métrics. OKS là điểm khóa tương tự của IoU và là những gì COCO mAP@OKS báo cáo.

> 标准人体姿态数据集: mỗi người 17 个关键点,PCK(正确关键点百分比) và OKS(目标关键点相似度) như là thước đo。OKS là bản quan trọng của IoU, là COCO mAP@OKS 报告内容。

### 2D vs 3D

- **2D pose** các phối hợp hình ảnh; giải quyết ở chất lượng sản xuất (MediaPipe, HRNet, ViTPose).
- **3D pose** các phối hợp thế giới / máy ảnh; nghiên cứu vẫn đang hoạt động.
  - Tăng dự đoán 2D lên 3D với một MLP nhỏ (VideoPose3D).
  - Trở lại 3D trực tiếp từ hình ảnh (PyMAF, MHFormer).
  - Thiết lập đa quan sát (CMU Panoptic) cho sự thật trên mặt đất.

> **【中文解读】**本节通过代码实现核心算法从零――这种" từ đầu"的方式能帮助理解框架背后的原理,遇到问题时不会被黑盒困住――

> **【拓展：工业部署中的视觉系统】**Trong thực tế, mô hình hình ảnh cần phải xem xét các vấn đề về sự chậm trễ, mô hình lớn, thiết bị cạnh phù hợp, vv.

> **【拓展：数据标注与质量】**视觉任务的效果高度依赖标签数据质量――Label Studio、CVAT là công cụ标签 chính thống――在工业场景中,主动学习(Active Learning) có thể giảm chi phí đánh dấu: mô hình đối với yêu cầu mẫu không xác định




## Hãy xây dựng nó.
```figure
cv3-pose-heatmap
```

## Hãy xây dựng nó

### Bước 1: Mục tiêu bản đồ nhiệt Gaussian

```python
import numpy as np
import torch

def gaussian_heatmap(size, cx, cy, sigma=2.0):
    yy, xx = np.meshgrid(np.arange(size), np.arange(size), indexing="ij")
    return np.exp(-((xx - cx) ** 2 + (yy - cy) ** 2) / (2 * sigma ** 2)).astype(np.float32)

hm = gaussian_heatmap(64, 32, 32, sigma=2.0)
print(f"peak: {hm.max():.3f} at ({hm.argmax() % 64}, {hm.argmax() // 64})")
```

Các bản đồ nhiệt mỗi điểm khóa được xếp dọc theo trục kênh cho ra toàn bộ tensor mục tiêu.

> Mỗi điểm quan trọng của nhiệt lực được xếp chồng lên dọc theo đường trục, tạo thành một mục tiêu đầy đủ.

### Bước 2: Đầu phím nhỏ

Một mô hình kiểu U-Net đưa ra các kênh heatmap K.

> Một mô hình U-Net, đầu ra K 个热力图通道.

```python
import torch.nn as nn
import torch.nn.functional as F

class TinyKeypointNet(nn.Module):
    def __init__(self, num_keypoints=4, base=16):
        super().__init__()
        self.down1 = nn.Sequential(nn.Conv2d(3, base, 3, 2, 1), nn.ReLU(inplace=True))
        self.down2 = nn.Sequential(nn.Conv2d(base, base * 2, 3, 2, 1), nn.ReLU(inplace=True))
        self.mid = nn.Sequential(nn.Conv2d(base * 2, base * 2, 3, 1, 1), nn.ReLU(inplace=True))
        self.up1 = nn.ConvTranspose2d(base * 2, base, 2, 2)
        self.up2 = nn.ConvTranspose2d(base, num_keypoints, 2, 2)

    def forward(self, x):
        h1 = self.down1(x)
        h2 = self.down2(h1)
        h3 = self.mid(h2)
        u1 = self.up1(h3)
        return self.up2(u1)
```

Nhập `(N, 3, H, W)`, sản lượng`(N, K, H, W)`Loss là MSE/pixel đối với các mục tiêu Gaussian.

### Bước 3: Thuyết định  trích xuất các tọa độ điểm khóa

```python
def heatmap_to_coords(heatmaps):
    """
    heatmaps: (N, K, H, W)
    returns:  (N, K, 2) float coordinates in image pixels
    """
    N, K, H, W = heatmaps.shape
    hm = heatmaps.reshape(N, K, -1)
    idx = hm.argmax(dim=-1)
    ys = (idx // W).float()
    xs = (idx % W).float()
    return torch.stack([xs, ys], dim=-1)

coords = heatmap_to_coords(torch.randn(2, 4, 32, 32))
print(f"coords: {coords.shape}")  # (2, 4, 2)
```

Một đường để suy luận. để tinh chỉnh sub-pixel, liên kết xung quanh argmax.

### Bước 4: Bộ dữ liệu điểm khóa tổng hợp

Khả năng đơn giản: vẽ bốn điểm trên một tấm vải trắng và học cách dự đoán chúng.

```python
def make_synthetic_sample(size=64):
    img = np.ones((3, size, size), dtype=np.float32)
    rng = np.random.default_rng()
    kps = rng.integers(8, size - 8, size=(4, 2))
    for cx, cy in kps:
        img[:, cy - 2:cy + 2, cx - 2:cx + 2] = 0.0
    hms = np.stack([gaussian_heatmap(size, cx, cy) for cx, cy in kps])
    return img, hms, kps
```

Đủ dễ để một mô hình nhỏ học trong một phút.

### Bước 5: Căn luyện

```python
model = TinyKeypointNet(num_keypoints=4)
opt = torch.optim.Adam(model.parameters(), lr=3e-3)

for step in range(200):
    batch = [make_synthetic_sample() for _ in range(16)]
    imgs = torch.from_numpy(np.stack([b[0] for b in batch]))
    hms = torch.from_numpy(np.stack([b[1] for b in batch]))
    pred = model(imgs)
    # Upsample pred to full resolution
    pred = F.interpolate(pred, size=hms.shape[-2:], mode="bilinear", align_corners=False)
    loss = F.mse_loss(pred, hms)
    opt.zero_grad(); loss.backward(); opt.step()
```

> **【中文解读】**Bài này sẽ trình bày cách sử dụng một khung đã phát triển như PyTorch, HuggingFace, và các khác.





> **【拓展：视觉模型的持续学习】**Trong môi trường sản xuất, mô hình hình ảnh cần phải liên tục thích ứng với dữ liệu mới.

## Hãy sử dụng nó để thực hiện

- **MediaPipe Pose** Máy ước tính hình ảnh sản xuất của Google; vận chuyển thời gian chạy WebGL + di động với độ trễ dưới 10ms.
- **MMPose**(OpenMMLab)  cơ sở mã nghiên cứu toàn diện; mọi kiến trúc SOTA với trọng lượng được đào tạo trước.
- **YOLOv8-pose** nhanh nhất thời gian thực nhiều người tư thế với một chuyển tiếp phía trước.
- **transformers HumanDPT / PoseAnything** các phương pháp tiếp cận ngôn ngữ thị giác mới hơn cho tư thế từ vựng mở (bất kỳ đối tượng, bất kỳ tập hợp điểm chính nào).

> **【中文解读】**Phần này tập trung vào cách phân phối mô hình như một sản phẩm có thể sử dụng.




## Chuyển nó đi.

> **【中文解读】**练题按照 Easy/Medium/Hard 三个难度递进;;建议至少完成 级别的题目, 级别适合深入研究或面试准备;;


Bài học này mang lại:

- `outputs/prompt-pose-stack-picker.md` một lời nhắc chọn MediaPipe / YOLOv8-pose / HRNet / ViTPose cho độ trễ, kích thước đám đông, và nhu cầu 2D vs 3D.
- `outputs/skill-heatmap-to-coords.md` một kỹ năng viết các bản đồ nhiệt sub-pixel-to-coordinate thói quen được sử dụng bởi mỗi mô hình tư thế sản xuất.

## Tập luyện bài tập

1. **(Easy)**Tập hình mẫu điểm khóa nhỏ trên bộ dữ liệu tổng hợp 4 điểm. báo cáo trung bình lỗi L2 giữa các điểm khóa dự đoán và đúng sau 200 bước.
2. **(Medium)**Thêm tinh tế sub-pixel: do vị trí argmax, phù hợp một hình dụ 1D dọc theo x và y từ các pixel lân cận.
3. **(Hard)**Xây dựng một bộ dữ liệu tổng hợp 2 người trong đó mỗi hình ảnh cho thấy hai ví dụ của mô hình 4 điểm khóa. Đọc một đường ống từ dưới lên với PAF dự đoán điểm khóa thuộc về ví dụ nào, và đánh giá OKS.

> **【中文解读】**Trong 术语表中的"Những gì mọi người nói" vs "Những gì nó thực sự có nghĩa" 区分日常口语和精确技术含义── 在团队协作中,统一术语定义可以避免大量沟通误解──


## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Keypoint | "A landmark" | A specific ordered point on an object (joint, corner, feature) |
| Pose | "The skeleton" | An ordered set of keypoints belonging to one instance |
| Top-down | "Detect then pose" | Two-stage pipeline: person detector + per-crop keypoint model; highest accuracy |
| Bottom-up | "Pose first, group later" | Single-pass all-keypoint prediction + grouping; constant time in crowd size |
| Heatmap | "Gaussian target" | H x W tensor per keypoint with peak at the true location; the preferred regression target |
| PAF | "Part Affinity Field" | 2-channel unit vector field encoding limb directions; used to group keypoints into instances |
| OKS | "Keypoint IoU" | Object Keypoint Similarity; the COCO metric for pose |
| HRNet | "High-Resolution Net" | The dominant top-down keypoint architecture; preserves high-res features throughout |

> **【中文解读】**延伸阅读 cung cấp các nguồn chất lượng cao cho việc học sâu. Những bài báo và giảng dạy này là tài liệu tham khảo cổ điển trong lĩnh vực này, phù hợp với những người đọc cần hiểu sâu hơn.


## Xem thêm 延伸阅读

- [OpenPose (Cao et al., 2017)](https://arxiv.org/abs/1812.08008) từ dưới lên với PAF; vẫn là bản ghi tốt nhất của cách tiếp cận
- [HRNet (Sun et al., 2019)](https://arxiv.org/abs/1902.09212) kiến trúc tham chiếu từ trên xuống
- [ViTPose (Xu et al., 2022)](https://arxiv.org/abs/2204.12484) ViT đơn giản như một xương sống tư thế; SOTA hiện tại trên nhiều điểm tham khảo
- [MediaPipe Pose](https://developers.google.com/mediapipe/solutions/vision/pose_landmarker) sản xuất thời gian thực; đống nhanh nhất được triển khai vào năm 2026
