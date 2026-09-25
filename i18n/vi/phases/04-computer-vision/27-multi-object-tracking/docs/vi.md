# Multi-Object Tracking & Video Memory Ứng dụng theo dõi nhiều mục tiêu và video memory

> Theo dõi là phát hiện cộng với liên kết. phát hiện mọi khung hình. Tích hợp các phát hiện của khung hình này với các dấu vết của khung hình cuối cùng bằng ID.

> **【中文解读】**跟踪 = 检测 + 关联── mỗi mục tiêu kiểm tra, sau đó sẽ kết quả kiểm tra hiện tại của  với các quỹ đạo theo dõi trên thông qua ID 匹配──多目标跟踪(MOT) là công nghệ cốt lõi của video hiểu, cần phải xử lý , biến mất, tái hiện, v.v. tình huống phức tạp──

> **【拓展：MOT 的应用】**Nhiều mục tiêu theo dõi trong an ninh giám sát (Buy Track, SORT, DeepSORT)

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 4 Lesson 06 (YOLO Detection), Phase 4 Lesson 08 (Mask R-CNN), Phase 4 Lesson 24 (SAM 3) | **前置知识:** Phase 4 Lesson 06（YOLO 检测），Phase 4 Lesson 08（Mask R-CNN），Phase 4 Lesson 24（SAM 3）
**Time:** ~60 minutes | **时间:** ~60 分钟

## Mục tiêu học tập

- Hóa ra phân biệt theo dõi theo dò từ theo dõi dựa trên truy vấn và đặt tên cho các gia đình thuật toán (SORT, DeepSORT, ByteTrack, BoT-SORT, SAM 2 bộ nhớ theo dõi, SAM 3.1 Object Multiplex)
- Thực hiện IoU + Hungary assignment từ đầu cho theo dõi theo dò
- Giải thích ngân hàng bộ nhớ của SAM 2 và lý do tại sao nó xử lý sự bịt kín tốt hơn so với liên kết dựa trên IoU
- Đọc ba số liệu theo dõi (MOTA, IDF1, HOTA) và chọn một trong số đó quan trọng cho một trường hợp sử dụng nhất định

> **【中文解读】**Mục tiêu học tập được liệt kê trong danh sách các khả năng cốt lõi cần được nắm bắt sau khi hoàn thành bài học.


## Vấn đề  vấn đề giới thiệu

Một máy dò cho bạn biết các đối tượng ở đâu trong một khung hình.`t`là cùng một đối tượng như một phát hiện trong khung`t-1`Nếu không có nó, bạn không thể đếm được những vật vượt qua một đường, theo dõi một quả bóng qua một sự bịt kín, hoặc biết "cỗ xe #4 đã ở trong làn đường trong 8 giây".

> 检测器 nói với bạn vị trí của vật thể trong đơn . 追踪器 nói với bạn `t` trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong  trong `t-1`Trong số đó, có một vật thể nào cũng được kiểm tra. Không có nó, bạn không thể tính số lượng vật thể vượt qua đường, theo dõi bóng bị che giấu, hoặc biết chiếc xe số 4 đã đi trên đường này trong 8 giây.

Theo dõi là điều cần thiết cho mọi sản phẩm đối diện với video: phân tích thể thao, giám sát, lái xe tự động, phân tích video y tế, giám sát động vật hoang dã, đếm dấu từ. Các khối xây dựng cốt lõi được chia sẻ: một bộ phát hiện mỗi khung, một mô hình chuyển động (trình lọc Kalman hoặc một cái gì đó giàu hơn), một bước liên kết (đồ pháp Hungary về IoU / cosine / các tính năng học), và một vòng đời đường (sự sinh, cập nhật, cái chết).

> Theo dõi đối với mỗi mặt video là rất quan trọng: phân tích thể thao, giám sát, tự lái, phân tích video y tế, giám sát động vật hoang dã, số lượng thương hiệu.

Năm 2026 đã mang lại hai mô hình mới: **SAM 2 memory-based tracking**(tức nhớ tính năng thay vì kết hợp mô hình chuyển động) và **SAM 3.1 Object Multiplex**Bài học này đi theo các phương pháp cổ điển trước, sau đó là phương pháp dựa trên bộ nhớ.

> Năm 2026 mang lại hai mô hình mới:**SAM 2 基于记忆的跟踪**(特征记忆替代运动模型关联) và **SAM 3.1 Object Multiplex**(Vì nhiều ví dụ về chia sẻ ký ức cùng một khái niệm) ⋅本课先走经典,然后走基于记忆的方法──

## Khái niệm cốt lõi

> **【中文解读】**Bài viết này giới thiệu các khái niệm và lý thuyết cốt lõi.


### Theo dõi bằng phát hiện

```mermaid
flowchart LR
    F1["Frame t"] --> DET["Detector"] --> D1["Detections at t"]
    PREV["Tracks up to t-1"] --> PREDICT["Motion predict<br/>(Kalman)"]
    PREDICT --> PRED["Predicted tracks at t"]
    D1 --> ASSOC["Hungarian assignment<br/>(IoU / cosine / motion)"]
    PRED --> ASSOC
    ASSOC --> UPDATE["Update matched tracks"]
    ASSOC --> NEW["Birth new tracks"]
    ASSOC --> DEAD["Age unmatched tracks; delete after N"]
    UPDATE --> NEXT["Tracks at t"]
    NEW --> NEXT
    DEAD --> NEXT

    style DET fill:#dbeafe,stroke:#2563eb
    style ASSOC fill:#fef3c7,stroke:#d97706
    style NEXT fill:#dcfce7,stroke:#16a34a
```

Mỗi bộ theo dõi mà bạn sẽ gặp vào năm 2026 là một biến thể trong vòng lặp này.

> Mỗi bộ theo dõi bạn gặp vào năm 2026 đều là một biến thể của vòng này.

- **SORT**(2016): Kalman filter + IoU Hungarian. đơn giản, nhanh chóng, không có mô hình ngoại hình.
  Trung ngữ翻译:**SORT**(2016):Karlmann 波器 + IoU 匈牙利算法──简单、快速、无外观模型──
- **DeepSORT**(2017): SORT + một tính năng xuất hiện dựa trên CNN cho mỗi bài hát (ReID).
  Trung ngữ翻译:**DeepSORT**(2017):SORT + Mỗi quỹ đạo của CNN 外观特征(ReID 嵌入)
- **ByteTrack**(2021): liên kết các phát hiện độ tự tin thấp với giai đoạn thứ hai; không cần thiết các tính năng xuất hiện nhưng hiệu suất cao nhất trên MOT17.
  Trung ngữ翻译:**ByteTrack**(2021): sẽ kiểm tra độ tin cậy thấp như giai đoạn thứ hai kết nối; không cần các đặc điểm ngoại hình nhưng trong MOT17 biểu hiện tốt nhất.
- **BoT-SORT**(2022): Byte + camera motion compensation + ReID.
  Trung ngữ翻译:**BoT-SORT**(2022):Byte + 相机运动补偿 + ReID。
- **StrongSORT / OC-SORT** Những người theo dõi ByteTrack có chuyển động và ngoại hình tốt hơn.
  Trung ngữ翻译:**StrongSORT / OC-SORT**ByteTrack 后代, cải tiến mô hình vận động và ngoại hình

### Bộ lọc Kalman trong một đoạn

Một bộ lọc Kalman duy trì trạng thái theo dõi .`(x, y, w, h, dx, dy, dw, dh)`với một sự đồng hóa.**predict**trạng thái sử dụng mô hình tốc độ liên tục, sau đó **update**Các bản cập nhật này tin tưởng vào việc phát hiện nhiều hơn khi sự không chắc chắn dự đoán cao. Điều này cung cấp quỹ đạo trơn tru và khả năng tiếp tục theo dõi thông qua một sự đóng kín ngắn (1-5 khung).

> 卡尔曼波器维护每个轨迹的状态`(x, y, w, h, dx, dy, dw, dh)`和协方差──每先用恒速模型**预测** trạng thái, tái sử dụng thi công phù hợp**更新**△预测不确定性高时更新更信任检测──

Mỗi bộ theo dõi cổ điển sử dụng bộ lọc Kalman trong bước dự đoán chuyển động.

> Mỗi bộ theo dõi cổ điển trong các bước dự đoán vận động đều sử dụng máy tính.

### Algoritm Hungary

Với một `M x N`Matrix chi phí (tracks x detections), tìm việc giao dịch một đối với một để giảm thiểu tổng chi phí.`1 - IoU(track_bbox, detection_bbox)`hoặc tương đồng âm tính của các tính năng xuất hiện. thời gian chạy là O(((M+N) ^ 3); cho M, N lên đến ~ 1000 nó đủ nhanh trong Python thông qua `scipy.optimize.linear_sum_assignment`- Tôi không biết.

> 给定 `M x N`Các nhà phân phối giá trị của các nhà phân phối giá trị của các nhà phân phối giá trị của các nhà phân phối giá trị của các nhà phân phối giá trị của các nhà phân phối giá trị của các nhà phân phối giá trị của các nhà phân phối giá trị của các nhà phân phối giá trị của các nhà phân phối giá trị của các nhà phân phối giá trị của các nhà phân phối giá trị của các nhà phân phối giá trị của các nhà phân phối giá trị của các nhà phân phối giá trị của các nhà phân phối giá.`1 - IoU(轨迹框, 检测框)`Hoặc ngoại quan đặc điểm của负余弦相似度──运行时间为 O(((M+N) ^3);M、N 约 1000 以内在Python中通过 `scipy.optimize.linear_sum_assignment`足足足快――

### Ý tưởng chính của ByteTrack

Các máy theo dõi tiêu chuẩn cho thấy độ tự tin thấp (< 0, 5).**second-stage candidates**: sau khi kết hợp các đường ray với các phát hiện độ tin cậy cao, các đường ray không sánh được cố gắng kết hợp các phát hiện độ tin cậy thấp với ngưỡng IoU nhẹ nhàng hơn.

> 标准跟踪器丢弃低置信度检测(< 0.5)。ByteTrack sẽ giữ chúng cho**第二阶段候选**: sẽ phù hợp với các đường mòn trong quá trình kiểm tra độ cao, cố gắng không phù hợp với các đường mòn trong quá trình kiểm tra độ thấp hơn một chút.

### SAM 2 theo dõi dựa trên bộ nhớ

SAM 2 xử lý video bằng cách giữ một **memory bank**Các bộ nhớ được phân tích với các tính năng của khung mới, và bộ giải mã tạo ra một mặt nạ cho cùng một bản trong khung mới.

Không bộ lọc Kalman, không có bài tập tiếng Hungary.

Lợi thế:
- Đứng vững đến các sự che giấu lớn (tưởng thức mang lại danh tính trường hợp trên nhiều khung).
- Từ khóa mở khi kết hợp với các lời nhắn văn bản của SAM 3.
- Nó hoạt động mà không có mô hình chuyển động riêng biệt.

Khối tác:
- Hạt chậm hơn ByteTrack để theo dõi nhiều vật thể.
- Ngân hàng bộ nhớ tăng lên; hạn chế cửa sổ ngữ cảnh.

### SAM 3.1 Object Multiplex

SAM 2 / SAM 3 theo dõi trước giữ một ngân hàng bộ nhớ riêng biệt mỗi lần. Đối với 50 đối tượng, 50 ngân hàng bộ nhớ. Object Multiplex (March 2026) sụp đổ chúng thành một bộ nhớ chung với **per-instance query tokens**- Giá cả tăng theo đường thẳng dưới số trường hợp.

Multiplex là tiêu chuẩn mặc định mới cho việc theo dõi đám đông vào năm 2026: đám đông biểu diễn, nhân viên kho, giao thông giao thông.

### Ba số liệu cần biết

- **MOTA (Multi-Object Tracking Accuracy)** 1 - (FN + FP + ID switch) / GT. Đánh nặng theo loại lỗi; một số liệu đơn lẻ kết hợp các lỗi phát hiện và liên kết.
  Trung ngữ翻译:**MOTA（多目标跟踪精度）**1 - (FN + FP + ID 切换) / GT──按错类加权;将检测和关联失败混混的单一标标──
- **IDF1 (ID F1)** trung bình hợp đồng của độ chính xác và nhớ ID. Tập trung cụ thể vào mức độ tốt của mỗi đường dẫn thực tại giữ ID của mình theo thời gian.
  Trung ngữ翻译:**IDF1（ID F1）** ID  độ chính xác và tỷ lệ gọi lại 调和平均―― tập trung đo lường sự phù hợp của ID trên mỗi đường thực theo thời gian―― đối với nhiệm vụ nhạy cảm chuyển đổi ID tốt hơn MOTA――
- **HOTA (Higher Order Tracking Accuracy)** phân hủy thành độ chính xác phát hiện (DetA) và độ chính xác liên kết (AssA).
  Trung ngữ翻译:**HOTA（高阶跟踪精度）** phân giải cho kiểm tra độ chính xác (DetA) và关联精度 (AssA) ⋅ quy chuẩn cộng đồng kể từ năm 2020; toàn diện nhất.

Đối với giám sát (còn là ai): IDF1 là những gì bạn báo cáo. Đối với phân tích thể thao (tài đếm): HOTA. Đối với so sánh học thuật chung: HOTA.

> 监控(谁是谁): báo cáo IDF1──运动分析(计数传球):HOTA──一般学术比较:HOTA──

> **【拓展：工业部署中的视觉系统】**Trong thực tế, mô hình hình ảnh cần phải xem xét các vấn đề về sự chậm trễ, mô hình lớn, thiết bị cạnh phù hợp, vv.

> **【拓展：数据标注与质量】**视觉任务的效果高度依赖标签数据质量――Label Studio、CVAT là công cụ标签 chính thống――在工业场景中,主动学习(Active Learning) có thể giảm chi phí đánh dấu: mô hình đối với yêu cầu mẫu không xác định



## Hãy xây dựng nó.

> **【中文解读】**本节通过代码实现核心算法从零――这种" từ đầu"的方式能帮助理解框架背后的原理,遇到问题时不会被黑盒困住――

```figure
cv3-track-assoc
```

## Hãy xây dựng nó

### Bước 1: Matrix chi phí dựa trên IoU

```python
import numpy as np


def bbox_iou(a, b):
    """
    a, b: (N, 4) arrays of [x1, y1, x2, y2].
    Returns (N_a, N_b) IoU matrix.
    """
    ax1, ay1, ax2, ay2 = a[:, 0], a[:, 1], a[:, 2], a[:, 3]
    bx1, by1, bx2, by2 = b[:, 0], b[:, 1], b[:, 2], b[:, 3]
    inter_x1 = np.maximum(ax1[:, None], bx1[None, :])
    inter_y1 = np.maximum(ay1[:, None], by1[None, :])
    inter_x2 = np.minimum(ax2[:, None], bx2[None, :])
    inter_y2 = np.minimum(ay2[:, None], by2[None, :])
    inter = np.clip(inter_x2 - inter_x1, 0, None) * np.clip(inter_y2 - inter_y1, 0, None)
    area_a = (ax2 - ax1) * (ay2 - ay1)
    area_b = (bx2 - bx1) * (by2 - by1)
    union = area_a[:, None] + area_b[None, :] - inter
    return inter / np.clip(union, 1e-8, None)
```

### Bước 2: Trình theo dõi kiểu SORT tối thiểu

Calman bỏ qua cho ngắn gọn  chúng ta sử dụng một liên kết IoU đơn giản ở đây; trong sản xuất dự đoán Kalman là thiết yếu.`sort`Phạm Python cung cấp phiên bản đầy đủ.

```python
from scipy.optimize import linear_sum_assignment


class Track:
    def __init__(self, tid, bbox, frame):
        self.id = tid
        self.bbox = bbox
        self.last_frame = frame
        self.hits = 1

    def update(self, bbox, frame):
        self.bbox = bbox
        self.last_frame = frame
        self.hits += 1


class SimpleTracker:
    def __init__(self, iou_threshold=0.3, max_age=5):
        self.tracks = []
        self.next_id = 1
        self.iou_threshold = iou_threshold
        self.max_age = max_age

    def step(self, detections, frame):
        if not self.tracks:
            for d in detections:
                self.tracks.append(Track(self.next_id, d, frame))
                self.next_id += 1
            return [(t.id, t.bbox) for t in self.tracks]

        track_boxes = np.array([t.bbox for t in self.tracks])
        det_boxes = np.array(detections) if len(detections) else np.empty((0, 4))

        iou = bbox_iou(track_boxes, det_boxes) if len(det_boxes) else np.zeros((len(track_boxes), 0))
        cost = 1 - iou
        cost[iou < self.iou_threshold] = 1e6

        matched_track = set()
        matched_det = set()
        if cost.size > 0:
            row, col = linear_sum_assignment(cost)
            for r, c in zip(row, col):
                if cost[r, c] < 1.0:
                    self.tracks[r].update(det_boxes[c], frame)
                    matched_track.add(r); matched_det.add(c)

        for i, d in enumerate(det_boxes):
            if i not in matched_det:
                self.tracks.append(Track(self.next_id, d, frame))
                self.next_id += 1

        self.tracks = [t for t in self.tracks if frame - t.last_frame <= self.max_age]
        return [(t.id, t.bbox) for t in self.tracks]
```

60 dòng. lấy các phát hiện trên mỗi khung, trả lại ID theo dõi trên mỗi khung. Hệ thống thực thêm dự đoán Kalman, sự phù hợp lại của ByteTrack giai đoạn hai, và tính năng xuất hiện.

### Bước 3: Kiểm tra đường mòn tổng hợp

```python
def synthetic_frames(num_frames=20, num_objects=3, H=240, W=320, seed=0):
    rng = np.random.default_rng(seed)
    starts = rng.uniform(20, 200, size=(num_objects, 2))
    velocities = rng.uniform(-5, 5, size=(num_objects, 2))
    frames = []
    for f in range(num_frames):
        dets = []
        for i in range(num_objects):
            cx, cy = starts[i] + f * velocities[i]
            dets.append([cx - 10, cy - 10, cx + 10, cy + 10])
        frames.append(dets)
    return frames


tracker = SimpleTracker()
for f, dets in enumerate(synthetic_frames()):
    tracks = tracker.step(dets, f)
```

Ba vật di chuyển thẳng phải giữ thẻ ID của họ trên tất cả 20 khung hình.

### Bước 4: Métric chuyển đổi ID

```python
def count_id_switches(tracks_per_frame, gt_per_frame):
    """
    tracks_per_frame:  list of list of (track_id, bbox)
    gt_per_frame:      list of list of (gt_id, bbox)
    Returns number of ID switches.
    """
    prev_assignment = {}
    switches = 0
    for tracks, gts in zip(tracks_per_frame, gt_per_frame):
        if not tracks or not gts:
            continue
        t_boxes = np.array([b for _, b in tracks])
        g_boxes = np.array([b for _, b in gts])
        iou = bbox_iou(g_boxes, t_boxes)
        for g_idx, (gt_id, _) in enumerate(gts):
            j = iou[g_idx].argmax()
            if iou[g_idx, j] > 0.5:
                t_id = tracks[j][0]
                if gt_id in prev_assignment and prev_assignment[gt_id] != t_id:
                    switches += 1
                prev_assignment[gt_id] = t_id
    return switches
```

Đây là một số liệu đơn giản hóa IDF1 lân cận: đếm bao nhiêu lần một đối tượng thực tại mặt đất thay đổi ID đường theo dõi dự đoán được gán.`py-motmetrics`và `TrackEval`- Tôi không biết.

> **【中文解读】**Bài này sẽ trình bày cách sử dụng một khung đã phát triển như PyTorch, HuggingFace, và các khác.





> **【拓展：视觉模型的持续学习】**Trong môi trường sản xuất, mô hình hình ảnh cần phải liên tục thích ứng với dữ liệu mới.

## Hãy sử dụng nó để thực hiện

Các máy theo dõi sản xuất vào năm 2026:

- `ultralytics` YOLOv8 + ByteTrack / BoT-SORT tích hợp. `results = model.track(source, tracker="bytetrack.yaml")`- Đáng mặc định.
- `supervision`(Roboflow)  Bị trùm ByteTrack cộng với tiện ích ghi chú.
- SAM 2 / SAM 3.1  theo dõi dựa trên bộ nhớ qua `processor.track()`- Tôi không biết.
- Dòng tùy chỉnh: máy dò (YOLOv8 / RT-DETR) + `sort-tracker`- `OC-SORT`- `StrongSORT`- Tôi không biết.

Chọn:

- Người đi bộ / xe hơi / hộp ở tốc độ 30+ fps: **ByteTrack with ultralytics**- Tôi không biết.
- Nhiều trường hợp của một lớp trong đám đông:**SAM 3.1 Object Multiplex**- Tôi không biết.
- Các vết lấn nặng với hình dạng có thể xác định được: **DeepSORT / StrongSORT**(Các tính năng ReID).
- Thể thao / tương tác phức tạp: **BoT-SORT**hoặc các máy theo dõi học (MOTRv3).

> **【中文解读】**Phần này tập trung vào cách phân phối mô hình như một sản phẩm có thể sử dụng.




## Chuyển nó đi.

> **【中文解读】**练题按照 Easy/Medium/Hard 三个难度递进;;建议至少完成 级别的题目, 级别适合深入研究或面试准备;;


Bài học này mang lại:

- `outputs/prompt-tracker-picker.md` chọn SORT / ByteTrack / BoT-SORT / SAM 2 / SAM 3.1 cho các loại cảnh, mô hình bịt kín và ngân sách thời gian trễ.
- `outputs/skill-mot-evaluator.md` viết một vòng đánh giá đầy đủ cho MOTA / IDF1 / HOTA chống lại các đường mòn thực tại mặt đất.

## Tập luyện bài tập

1. **(Easy)**Hãy chạy bộ theo dõi tổng hợp ở trên với 3, 10 và 30 đối tượng. báo cáo số lượng chuyển đổi ID trong mỗi trường hợp. xác định nơi liên kết đơn giản chỉ với IoU bắt đầu thất bại.
2. **(Medium)**Thêm một bước dự đoán tốc độ liên tục Kalman trước khi kết hợp.
3. **(Hard)**Thêm vào bộ theo dõi dựa trên bộ nhớ của SAM 2 (via `transformers`Thử cả SimpleTracker và SAM 2 trên một clip 30 giây của đám đông và so sánh số lượng chuyển đổi ID, bằng cách dán nhãn bằng tay các ID thực tại cho 5 người nổi bật.

> **【中文解读】**Trong 术语表中的"Những gì mọi người nói" vs "Những gì nó thực sự có nghĩa" 区分日常口语和精确技术含义── 在团队协作中,统一术语定义可以避免大量沟通误解──


## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Tracking-by-detection | "Detect then associate" | Per-frame detector + Hungarian assignment on IoU / appearance |
| Kalman filter | "Motion predict" | Linear dynamics + covariance for smooth track predictions and occlusion handling |
| Hungarian algorithm | "Optimal assignment" | Solves the minimum-cost bipartite matching problem; `scipy.optimize.linear_sum_assignment` |
| ByteTrack | "Low-confidence second pass" | Re-match unmatched tracks to low-confidence detections to recover short occlusions |
| DeepSORT | "SORT + appearance" | Adds a ReID feature for cross-frame matching; better for ID preservation |
| Memory bank | "SAM 2 trick" | Per-instance spatio-temporal features stored across frames; cross-attention replaces explicit association |
| Object Multiplex | "SAM 3.1 shared memory" | Single shared memory with per-instance queries for fast many-object tracking |
| HOTA | "Modern tracking metric" | Decomposes into detection and association accuracy; community standard |

> **【中文解读】**延伸阅读 cung cấp các nguồn chất lượng cao cho việc học sâu. Những bài báo và giảng dạy này là tài liệu tham khảo cổ điển trong lĩnh vực này, phù hợp với những người đọc cần hiểu sâu hơn.


## Xem thêm 延伸阅读

- [SORT (Bewley et al., 2016)](https://arxiv.org/abs/1602.00763) giấy theo dõi bằng phát hiện tối thiểu
- [DeepSORT (Wojke et al., 2017)](https://arxiv.org/abs/1703.07402) thêm tính năng xuất hiện
- [ByteTrack (Zhang et al., 2022)](https://arxiv.org/abs/2110.06864) Tiếp tục thông qua thứ hai có độ tự tin thấp
- [BoT-SORT (Aharon et al., 2022)](https://arxiv.org/abs/2206.14651) Khấu trừ chuyển động của máy ảnh
- [HOTA (Luiten et al., 2020)](https://arxiv.org/abs/2009.07736) Metric theo dõi phân hủy
- [SAM 2 video segmentation (Meta, 2024)](https://ai.meta.com/sam2/) bộ theo dõi dựa trên bộ nhớ
- [SAM 3.1 Object Multiplex (Meta, March 2026)](https://ai.meta.com/blog/segment-anything-model-3/)
