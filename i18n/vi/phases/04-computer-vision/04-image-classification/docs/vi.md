# Phân loại hình ảnh   Image

> Một phân loại là một hàm từ các pixel đến phân bố xác suất trên các lớp.

> **【中文解读】**图像分类器 bản chất là một hàm phân phối phân phối từ hình ảnh đến phân loại概率. 检测(分类区域) 、分割(分类像素) 、检索(按类相似度排序) Kết quả là tất cả là phân loại.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 2 Lesson 09 (Model Evaluation), Phase 3 Lesson 10 (Mini Framework), Phase 4 Lesson 03 (CNNs) | **前置知识:** Phase 2 Lesson 09（模型评估），Phase 3 Lesson 10（迷你框架），Phase 4 Lesson 03（CNN）
**Time:** ~75 minutes | **时间:** ~75 分钟

## Mục tiêu học tập

- Xây dựng một đường ống phân loại hình ảnh từ đầu đến cuối trên CIFAR-10: bộ dữ liệu, tăng cường, mô hình, vòng đào tạo, đánh giá
- Giải thích vai trò của mỗi thành phần (data loader, mất mát, tối ưu hóa, lập lịch, tăng cường) và dự đoán cách phá vỡ bất kỳ một trong số chúng biểu hiện trong đường cong mất mát
- Thực hiện trộn lẫn, cắt và làm trơn nhãn từ đầu và biện minh khi nào mỗi loại đáng thêm
- Đọc một số liệu hỗn loạn và một bảng độ chính xác/tái nhớ cho mỗi lớp để chẩn đoán các lỗi tập hợp dữ liệu và mô hình vượt quá độ chính xác tổng thể

> **【中文解读】**Mục tiêu học tập được liệt kê trong danh sách các khả năng cốt lõi cần được nắm bắt sau khi hoàn thành bài học.


## Vấn đề  vấn đề giới thiệu

Mỗi nhiệm vụ nhìn thấy được chuyển đến phân loại hình ảnh ở một mức độ nào đó. Khám phá phân loại các khu vực. phân loại phân loại các pixel. Khám phục hồi xếp hạng theo sự tương đồng với các lớp trung tâm.

> Mỗi nhiệm vụ hình ảnh được giao giao đều được kết hợp với các loại hình. Phân tích phân loại vùng. Phân tích phân loại phân loại phân loại. Phân tích theo sự tương đồng của trung tâm phân loại. Phân tích phân loại làm cho các vòng lặp tập dữ liệu, tăng cường chiến lược, hàm mất mát, đánh giá.

> **【中文解读】**Tất cả các nhiệm vụ trực quan thực tế được triển khai có thể được kết luận về bản chất là phân loại hình ảnh: mục tiêu kiểm tra là " đối với phân loại khu vực", phân vùng là " đối với phân loại hình ảnh", tìm kiếm hình ảnh là " theo phân loại trung tâm sự tương tự sắp xếp"...... để làm rõ từng phần của dòng chảy phân loại, là chìa khóa của tất cả các khóa học tiếp theo của giai đoạn này.

Hầu hết các lỗi phân loại không có trong mô hình. Chúng sống trong đường ống dẫn: một chuẩn hóa bị hỏng, một bộ đào tạo không bị thay đổi, tăng cường làm sai nhãn, một phân chia xác thực bị ô nhiễm bởi dữ liệu đào tạo, tỷ lệ học tập lặng lẽ khác nhau sau thời kỳ 30. Một CNN sẽ đạt 93% trên CIFAR-10 với một thiết lập chính xác thường đạt điểm 70-75% với một bị hỏng, và đường cong thua lỗ trông hợp lý suốt thời gian.

> Phần lớn các loại lỗi không trong mô hình. Chúng tồn tại trong dòng chảy: sự kết hợp sai lầm, tập hợp đào tạo không bị rối loạn, tăng cường các nhãn biến dạng, tập hợp xác minh các dữ liệu bị ô nhiễm được đào tạo, tỷ lệ học tập phát tán tĩnh lặng sau thời đại thứ 30. Một định vị đúng có thể đạt 93% trên CIFAR-10 trên CNN, thường chỉ đạt 70-75% trong định vị sai lầm, và đường cong mất mát luôn trông rất hợp lý.

Bài học này dây cáp toàn bộ đường ống bằng tay để mọi bộ phận đều có thể kiểm tra.`torchvision.datasets`có thể giấu một con bọ.

> Bài học này tự tạo ra toàn bộ dòng nước, để mọi phần đều có thể kiểm tra.`torchvision.datasets`Trong bất cứ thứ gì có thể ẩn được của lỗi.

> **【中文解读】**Hầu hết các loại lỗi không nằm trong mô hình, mà nằm trong dòng chảy: tập hợp làm sai lầm, tập hợp đào tạo không lộn xộn, tăng cường phá hủy nhãn hiệu, tập hợp xác nhận được đào tạo, dữ liệu bị ô nhiễm, tỷ lệ học tập ải rác.

## Khái niệm cốt lõi

### Hành trình phân loại

```mermaid
flowchart LR
    A["Dataset<br/>(images + labels)"] --> B["Augment<br/>(random transforms)"]
    B --> C["Normalise<br/>(mean/std)"]
    C --> D["DataLoader<br/>(batch + shuffle)"]
    D --> E["Model<br/>(CNN)"]
    E --> F["Logits<br/>(N, C)"]
    F --> G["Cross-entropy loss"]
    F --> H["Argmax<br/>at eval"]
    G --> I["Backward"]
    I --> J["Optimizer step"]
    J --> K["Scheduler step"]
    K --> E

    style A fill:#dbeafe,stroke:#2563eb
    style E fill:#fef3c7,stroke:#d97706
    style G fill:#fecaca,stroke:#dc2626
    style H fill:#dcfce7,stroke:#16a34a
```

Mỗi dòng trong vòng lặp này là nơi mà một lỗi có thể sống. Cross-entropy lấy logits nguyên liệu, không phải đầu ra softmax, vì vậy bất kỳ `model(x).softmax()`trước khi mất mát lặng lẽ tính toán gradient sai.

> Mỗi dòng trong vòng này đều là lỗi có thể tồn tại ở đâu.`model(x).softmax()`Thành phố sẽ lặng lẽ tính toán độ sai lầm.

> **【中文解读】**Trong mỗi dòng dòng nước có thể chứa lỗi. giao thông. 接收 là các log nguyên thủy. Nếu trước đó làm được hàm softmax tái truyền vào lỗ, gradience tính toán sẽ hoàn toàn sai.  nhưng sẽ không báo cáo sai. `optimizer.zero_grad()`phải xảy ra một lần mỗi bước; bỏ qua nó tích lũy gradient và trông giống như một tỷ lệ học tập vô cùng không ổn định. Mỗi một trong những lỗi này làm phẳng đường cong học tập mà không ném một lỗi.

### Cross-entropy, logits, và softmax

Một phân loại sản xuất `C`số cho mỗi hình ảnh được gọi là logits. Sử dụng softmax chuyển đổi chúng thành phân phối xác suất:

> 分类器为每张图像产生 `C`个数字, được gọi là logits. ứng dụng softmax sẽ chuyển chúng thành phân bố概率:

```
softmax(z)_i = exp(z_i) / sum_j exp(z_j)
```

Cross-entropy đo khả năng log âm của lớp đúng:

> 交叉 đo đúng loại của tỷ lệ tỷ lệ đối với số:

```
CE(z, y) = -log( softmax(z)_y )
        = -z_y + log( sum_j exp(z_j) )
```

Hình dạng bên phải là số ổn định (log-sum-exp).`nn.CrossEntropyLoss`Fuses softmax + NLL trong một op và lấy logits thô trực tiếp.

> Right边的形式是数值稳定的 (), log-sum-exp (),`nn.CrossEntropyLoss`Trong một hoạt động kết hợp softmax + NLL, trực tiếp nhận logits nguyên thủy.

> **【中文解读】**PyTorch của `nn.CrossEntropyLoss`内部已经融合了软max + 负对数似然,直接传入原始logits 即可── Nếu bạn trước tiên chuyển động điều chỉnh softmax tái传入损失, tương đương với làm hai lần softmax, gradient计算 hoàn toàn sai lầm──

### Tại sao tăng cường hiệu quả

Một CNN có thiên hướng inductive cho dịch (từ chia sẻ trọng lượng) nhưng không có bất biến tích hợp vào cây trồng, cúi, màu jitter, hoặc mùi. Cách duy nhất để dạy cho nó những bất biến đó là bằng cách cho nó hiển thị các pixel thực hành chúng.

> CNN có tính cách chuyển động đối với các hình ảnh khác nhau, nhưng không có sự thay đổi nội tại trong việc cắt, chuyển đổi, màu sắc hoặc phủ kín. Cách duy nhất để dạy nó những điều này là thể hiện các hình ảnh của chúng.

> **【拓展：数据增强与模型泛化】**Đăng cường dữ liệu là phương tiện tự động hóa AI hiện đại mạnh nhất. Trong các bài tập mô hình cổ điển như ResNet, EfficientNet, các chiến lược tăng cường có tác động trực tiếp đến tỷ lệ xác thực 3-5%.

```
Original crop:  "dog facing left"
Flip:           "dog facing right"       <- same label, different pixels
Rotate(+15):    "dog, slight tilt"
Colour jitter:  "dog in warmer light"
RandomErasing:  "dog with patch missing"
```

Quy tắc: tăng cường phải giữ nhãn. Cutout và xoay trên một chữ số có thể xoay "6" vào "9"; cho bộ dữ liệu đó bạn sử dụng phạm vi xoay nhỏ hơn và chọn tăng cường tôn trọng các bất biến cụ thể về chữ số.

> Quy tắc: tăng cường phải giữ nhãn không thay đổi. Đối với số có thể làm "6" trở thành "9"; Đối với bộ dữ liệu đó, bạn sử dụng phạm vi quay nhỏ hơn,并 chọn tôn trọng tăng cường không thay đổi số cụ thể.

### Trộn và cắt trộn

Sự tăng cường thông thường biến đổi các pixel nhưng giữ cho các nhãn chỉ nóng. **Mixup**và **cutmix**phá vỡ bằng cách liên kết cả hai.

> Thông thường tăng cường thay đổi hình ảnh nhưng giữ nhãn là một-hót.**Mixup**和 **cutmix** Tham gia vào cả hai đã phá vỡ điều này.

```
Mixup:
  lambda ~ Beta(a, a)
  x = lambda * x_i + (1 - lambda) * x_j
  y = lambda * y_i + (1 - lambda) * y_j

Cutmix:
  paste a random rectangle of x_j into x_i
  y = area-weighted mix of y_i and y_j
```

Tại sao nó giúp ích: mô hình ngừng ghi nhớ các mục tiêu nóng nhất và học cách liên kết giữa các lớp học.

> Tại sao có ích: mô hình dừng ghi nhớ đỉnh điểm  mục tiêu nóng nhất, học tập vào các lớp giá trị.

> **【拓展：Mixup 在大模型中的应用】**Ý tưởng hỗn hợp đã mở rộng đến lĩnh vực NLP để hỗn hợp giá trị đính kèm vào văn bản. Trong các bài tập của LLM như ChatGPT, kỹ thuật đánh dấu và đánh dấu mềm cũng được sử dụng rộng rãi, giúp mô hình tạo ra xác suất xuất phát tốt hơn, giảm sự tự tin quá mức.

### Đơn vị nhãn

Một người anh em của sự nhầm lẫn.`[0, 0, 1, 0, 0]`, tàu chống lại `[eps/C, eps/C, 1-eps, eps/C, eps/C]`cho một người nhỏ `eps`như 0.1. ngăn chặn mô hình từ việc sản xuất logit sắc nét tùy tiện và cải thiện hiệu chuẩn hầu như không chi phí.`nn.CrossEntropyLoss(label_smoothing=0.1)`từ PyTorch 1.10.

> Mixup của gần亲──不使用 `[0, 0, 1, 0, 0]` thực hiện tập luyện, thay vì sử dụng `[eps/C, eps/C, 1-eps, eps/C, eps/C]`, trong số đó `eps`Nếu 0.1 ⋅ ngăn chặn mô hình tạo ra bất kỳ logs cấp cao, hầu như không có chi phí cải thiện chuẩn bị ⋅ từ PyTorch 1.10                                       `nn.CrossEntropyLoss(label_smoothing=0.1)`Ở giữa.

### Đánh giá vượt quá độ chính xác

Sự chính xác tổng hợp che giấu sự mất cân bằng. Một phân loại nhị phân 90-10 luôn dự đoán điểm số lớp đa số là 90%. Các công cụ thực sự cho bạn biết những gì đang xảy ra:

> 总体准确率藏藏不平衡―― 一总是预测多数类90-10 二分类器能达到90%―― 真实告诉你发生了什么工具:

- **Per-class accuracy** một số cho mỗi lớp; ngay lập tức xuất hiện các loại có hiệu suất thấp.
  Trung ngữ翻译: 每类准确率 每类一个数字;立即暴露表现不佳的类别──
- **Confusion matrix** C x C lưới với hàng i col j = số lượng lớp thực i dự đoán như lớp j; đường vạch là chính xác, các đường vạch ngoài là nơi mô hình của bạn sống.
  Trung ngữ翻译:混矩阵C x C 网格,行 i 列 j = 真实类 i 被预测为类 j 的计量;对角线是正确的,非对角线是你的模型出错的地方──
- **Top-1 / Top-5** liệu lớp học chính xác có nằm trong dự đoán đầu 1 hoặc đầu 5; Top-5 quan trọng đối với ImageNet vì các lớp học như "Norwich terrier" so với "Norfolk terrier" thực sự không rõ ràng.
  Trung ngữ翻译:Top-1 / Top-5正确类别是否在前1或前5 预测中;Top-5 đối với ImageNet  rất quan trọng, vì loại này giống như "Norwich Terrier" vs "Norfolk Terrier"确实模两可──
- **Calibration (ECE)** dự đoán độ tin cậy 0,8 có đúng 80% thời gian không?
  Trung ngữ翻译:校准(ECE) 0.8 置信度的预测 80% 的时间是对的吗?现代网络系统性地过度自信;用温度缩缩或标签平滑修复。

> **【拓展：工业部署中的视觉系统】**Trong thực tế, mô hình hình ảnh cần phải xem xét các vấn đề về sự chậm trễ, mô hình lớn, thiết bị cạnh phù hợp, vv.


## Hãy xây dựng nó.

> **【中文解读】**本节通过代码实现核心算法从零――这种" từ đầu"的方式能帮助理解框架背后的原理,遇到问题时不会被黑盒困住――

```figure
receptive-field
```

## Hãy xây dựng nó

### Bước 1: Một bộ dữ liệu tổng hợp xác định

CIFAR-10 sống trên đĩa. Để làm cho bài học này có thể tái tạo và nhanh chóng chúng tôi xây dựng một tập dữ liệu tổng hợp trông giống như CIFAR  32x32 hình ảnh RGB với cấu trúc cụ thể cho lớp mà mô hình phải học.

> CIFAR-10 tồn tại trên đĩa. Để làm cho bài học này có thể thực hiện và nhanh chóng, chúng tôi xây dựng một bộ dữ liệu tổng hợp trông giống như CIFAR với mô hình phải học các loại cấu trúc cụ thể của 32x32 RGB hình ảnh.

```python
import numpy as np
import torch
from torch.utils.data import Dataset


def synthetic_cifar(num_per_class=1000, num_classes=10, seed=0):
    rng = np.random.default_rng(seed)
    X = []
    Y = []
    for c in range(num_classes):
        centre = rng.uniform(0, 1, (3,))
        freq = 2 + c
        for _ in range(num_per_class):
            yy, xx = np.meshgrid(np.linspace(0, 1, 32), np.linspace(0, 1, 32), indexing="ij")
            r = np.sin(xx * freq) * 0.5 + centre[0]
            g = np.cos(yy * freq) * 0.5 + centre[1]
            b = (xx + yy) * 0.5 * centre[2]
            img = np.stack([r, g, b], axis=-1)
            img += rng.normal(0, 0.08, img.shape)
            img = np.clip(img, 0, 1)
            X.append(img.astype(np.float32))
            Y.append(c)
    X = np.stack(X)
    Y = np.array(Y)
    idx = rng.permutation(len(X))
    return X[idx], Y[idx]


class ArrayDataset(Dataset):
    def __init__(self, X, Y, transform=None):
        self.X = X
        self.Y = Y
        self.transform = transform

    def __len__(self):
        return len(self.X)

    def __getitem__(self, i):
        img = self.X[i]
        if self.transform is not None:
            img = self.transform(img)
        img = torch.from_numpy(img).permute(2, 0, 1)
        return img, int(self.Y[i])
```

Mỗi lớp có màu sắc và tần số riêng của nó, cộng với tiếng ồn Gaussian để buộc mô hình học tín hiệu thay vì ghi nhớ pixel.

> Mỗi loại có mô hình định dạng và tần suất riêng của mình, cộng với tiếng ồn cao để ép buộc mô hình học tập tín hiệu thay vì hình ảnh nhớ.

### Bước 2: Tiêu chuẩn hóa và tăng cường

Hai biến đổi mà mọi đường ống thị giác đều có.

> Mỗi dòng video có hai biến đổi.

```python
def standardize(mean, std):
    mean = np.array(mean, dtype=np.float32)
    std = np.array(std, dtype=np.float32)
    def _fn(img):
        return (img - mean) / std
    return _fn


def random_hflip(p=0.5):
    def _fn(img):
        if np.random.random() < p:
            return img[:, ::-1, :].copy()
        return img
    return _fn


def random_crop(pad=4):
    def _fn(img):
        h, w = img.shape[:2]
        padded = np.pad(img, ((pad, pad), (pad, pad), (0, 0)), mode="reflect")
        y = np.random.randint(0, 2 * pad)
        x = np.random.randint(0, 2 * pad)
        return padded[y:y + h, x:x + w, :]
    return _fn


def compose(*fns):
    def _fn(img):
        for fn in fns:
            img = fn(img)
        return img
    return _fn
```

Nhấp vào tấm trước khi trồng, không phải là tấm bằng không, bởi vì biên giới đen là một tín hiệu mà mô hình sẽ học cách bỏ qua theo cách không hữu ích.

> 剪裁 trước sử dụng phản xạ điền thay vì điền không, vì khung màu đen là một tín hiệu mà các mô hình học học tập bỏ qua một cách vô dụng.

### Bước 3: Trộn lẫn

Trộn hai hình ảnh và hai nhãn bên trong bước đào tạo. được thực hiện như một biến đổi hàng loạt để nó sống bên cạnh các thông qua phía trước thay vì bên trong bộ dữ liệu.

> Trong giai đoạn tập luyện, hai hình ảnh và hai nhãn được pha trộn.

```python
def mixup_batch(x, y, num_classes, alpha=0.2):
    if alpha <= 0:
        return x, torch.nn.functional.one_hot(y, num_classes).float()
    lam = float(np.random.beta(alpha, alpha))
    idx = torch.randperm(x.size(0), device=x.device)
    x_mixed = lam * x + (1 - lam) * x[idx]
    y_onehot = torch.nn.functional.one_hot(y, num_classes).float()
    y_mixed = lam * y_onehot + (1 - lam) * y_onehot[idx]
    return x_mixed, y_mixed


def soft_cross_entropy(logits, soft_targets):
    log_probs = torch.log_softmax(logits, dim=-1)
    return -(soft_targets * log_probs).sum(dim=-1).mean()
```

`soft_cross_entropy`là sự phân phối giữa các điểm giao hợp với các điểm giao hợp mềm. nó giảm xuống mức một điểm giao hợp khi mục tiêu chính xác là một điểm giao hợp.

> `soft_cross_entropy`── khi mục tiêu đúng là một , nó biến thành một                 

### Bước 4: Chuyển tập

Công thức hoàn chỉnh: một lần vượt qua dữ liệu, gradient một lần mỗi lô, lập trình viên bước một lần mỗi thời đại.

> 完整方案: dữ liệu được thực hiện một lần qua, mỗi lô tính một lần gradient, mỗi thời đại 调度 một lần học率

```python
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torch.optim import SGD
from torch.optim.lr_scheduler import CosineAnnealingLR

def train_one_epoch(model, loader, optimizer, device, num_classes, use_mixup=True):
    model.train()
    total, correct, loss_sum = 0, 0, 0.0
    for x, y in loader:
        x, y = x.to(device), y.to(device)
        if use_mixup:
            x_m, y_soft = mixup_batch(x, y, num_classes)
            logits = model(x_m)
            loss = soft_cross_entropy(logits, y_soft)
        else:
            logits = model(x)
            loss = nn.functional.cross_entropy(logits, y, label_smoothing=0.1)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        loss_sum += loss.item() * x.size(0)
        total += x.size(0)
        # Training accuracy vs the un-mixed labels `y` is only an approximation
        # when mixup is on (the model saw soft targets, not y). Treat it as a
        # rough progress signal; rely on val accuracy for real performance.
        with torch.no_grad():
            pred = logits.argmax(dim=-1)
            correct += (pred == y).sum().item()
    return loss_sum / total, correct / total


@torch.no_grad()
def evaluate(model, loader, device, num_classes):
    model.eval()
    total, correct = 0, 0
    loss_sum = 0.0
    cm = torch.zeros(num_classes, num_classes, dtype=torch.long)
    for x, y in loader:
        x, y = x.to(device), y.to(device)
        logits = model(x)
        loss = nn.functional.cross_entropy(logits, y)
        pred = logits.argmax(dim=-1)
        for t, p in zip(y.cpu(), pred.cpu()):
            cm[t, p] += 1
        loss_sum += loss.item() * x.size(0)
        total += x.size(0)
        correct += (pred == y).sum().item()
    return loss_sum / total, correct / total, cm
```

Năm tính bất biến mà bạn kiểm tra mỗi khi bạn viết một vòng tròn huấn luyện:

> Mỗi lần viết tập trung vòng kiểm tra năm không thay đổi:

1. `model.train()`trước khi đào tạo,`model.eval()`trước khi đánh giá  biến đổi hành vi bỏ và batchnorm.
2. `.zero_grad()`trước đây`.backward()`- Tôi không biết.
3. `.item()`khi tích lũy số liệu để không có gì giữ cho biểu đồ tính toán sống.
4. `@torch.no_grad()`trong quá trình đánh giá  tiết kiệm trí nhớ và thời gian, ngăn ngừa tai nạn tinh tế.
5. Argmax so với logits thô, không phải softmax  kết quả tương tự, một lần ít hơn.

### Bước 5: Đặt nó lại

Sử dụng `TinyResNet`từ bài học trước, đào tạo cho một vài thời đại, đánh giá.

> Sử dụng trên một lớp của `TinyResNet`, đào tạo vài thời đại, đánh giá.

```python
from main import synthetic_cifar, ArrayDataset
from main import standardize, random_hflip, random_crop, compose
from main import mixup_batch, soft_cross_entropy
from main import train_one_epoch, evaluate
# TinyResNet comes from the previous lesson (03-cnns-lenet-to-resnet).
# Adjust the import path to wherever you stored the previous lesson's code.
from cnns_lenet_to_resnet import TinyResNet  # example placeholder

X, Y = synthetic_cifar(num_per_class=500)
split = int(0.9 * len(X))
X_train, Y_train = X[:split], Y[:split]
X_val, Y_val = X[split:], Y[split:]

mean = [0.5, 0.5, 0.5]
std = [0.25, 0.25, 0.25]
train_tf = compose(random_hflip(), random_crop(pad=4), standardize(mean, std))
eval_tf = standardize(mean, std)

train_ds = ArrayDataset(X_train, Y_train, transform=train_tf)
val_ds = ArrayDataset(X_val, Y_val, transform=eval_tf)

train_loader = DataLoader(train_ds, batch_size=128, shuffle=True, num_workers=0)
val_loader = DataLoader(val_ds, batch_size=256, shuffle=False, num_workers=0)

device = "cuda" if torch.cuda.is_available() else "cpu"
model = TinyResNet(num_classes=10).to(device)
optimizer = SGD(model.parameters(), lr=0.1, momentum=0.9, weight_decay=5e-4, nesterov=True)
scheduler = CosineAnnealingLR(optimizer, T_max=10)

for epoch in range(10):
    tr_loss, tr_acc = train_one_epoch(model, train_loader, optimizer, device, 10, use_mixup=True)
    va_loss, va_acc, _ = evaluate(model, val_loader, device, 10)
    scheduler.step()
    print(f"epoch {epoch:2d}  lr {scheduler.get_last_lr()[0]:.4f}  "
          f"train {tr_loss:.3f}/{tr_acc:.3f}  val {va_loss:.3f}/{va_acc:.3f}")
```

Trên bộ dữ liệu tổng hợp, điều này đạt đến độ chính xác xác xác thực gần như hoàn hảo trong vòng năm thời đại, đó là điểm: đường ống là chính xác, mô hình có thể học được điều gì. Thay đổi bộ dữ liệu cho CIFAR-10 thực và cùng một vòng lặp tàu đến ~ 90% mà không thay đổi.

> Trong tập dữ liệu tổng hợp, trong 5 thời gian này, nó có thể đạt được tỷ lệ xác minh hoàn hảo gần như, đó là trọng tâm: dòng chảy là đúng, mô hình có thể học được những gì có thể học được.

### Bước 6: Đọc các mã số nhầm lẫn

Chỉ riêng độ chính xác không bao giờ cho bạn biết mô hình đang thất bại ở đâu.

> Tỷ lệ chính xác độc lập sẽ không bao giờ cho bạn biết mô hình thất bại ở đâu.

```python
def print_confusion(cm, labels=None):
    c = cm.shape[0]
    labels = labels or [str(i) for i in range(c)]
    print(f"{'':>6}" + "".join(f"{l:>5}" for l in labels))
    for i in range(c):
        row = cm[i].tolist()
        print(f"{labels[i]:>6}" + "".join(f"{v:>5}" for v in row))
    print()
    tp = cm.diag().float()
    fp = cm.sum(dim=0).float() - tp
    fn = cm.sum(dim=1).float() - tp
    prec = tp / (tp + fp).clamp_min(1)
    rec = tp / (tp + fn).clamp_min(1)
    f1 = 2 * prec * rec / (prec + rec).clamp_min(1e-9)
    for i in range(c):
        print(f"{labels[i]:>6}  prec {prec[i]:.3f}  rec {rec[i]:.3f}  f1 {f1[i]:.3f}")

_, _, cm = evaluate(model, val_loader, device, 10)
print_confusion(cm)
```

Các hàng là các lớp thực, cột là dự đoán. Một nhóm số lượng ngoài đường chọc giữa lớp 3 và 5 có nghĩa là mô hình nhầm lẫn hai thứ đó và cung cấp cho bạn một điểm khởi đầu cho việc thu thập dữ liệu nhắm mục tiêu hoặc tăng cường cụ thể cho lớp.

> 行 là các loại thực,列 là dự đoán. Sự tập hợp các số không đối nghịch giữa các loại 3 và 5 có nghĩa là mô hình kết hợp hai loại này, và cung cấp cho bạn điểm khởi đầu thu thập dữ liệu cụ thể hoặc tăng cường các loại.



## Hãy sử dụng nó để thực hiện

> **【中文解读】**Bài này sẽ trình bày cách sử dụng một khung đã phát triển như PyTorch, HuggingFace, và các khác.


`torchvision`cho CIFAR-10 thực sự toàn bộ đường ống là bốn dòng cộng với một vòng lặp huấn luyện.

> `torchview`Để sử dụng các thành phần thông thường, CIFAR-10 thực sự là một vòng tròn tập luyện.

```python
from torchvision.datasets import CIFAR10
from torchvision.transforms import Compose, RandomCrop, RandomHorizontalFlip, ToTensor, Normalize

mean = (0.4914, 0.4822, 0.4465)
std = (0.2470, 0.2435, 0.2616)
train_tf = Compose([
    RandomCrop(32, padding=4, padding_mode="reflect"),
    RandomHorizontalFlip(),
    ToTensor(),
    Normalize(mean, std),
])
eval_tf = Compose([ToTensor(), Normalize(mean, std)])

train_ds = CIFAR10(root="./data", train=True,  download=True, transform=train_tf)
val_ds   = CIFAR10(root="./data", train=False, download=True, transform=eval_tf)
```

Hai điều cần lưu ý: trung bình / std là **dataset-specific** được tính trên bộ đào tạo CIFAR-10, không phải ImageNet  và tấm phản xạ là chính sách thu hoạch mặc định của cộng đồng.

> 两点注意事项: trung bình/标准差 là**数据集特定的** tính trên tập hợp đào tạo CIFAR-10, chứ không phải ImageNet phản ứng lấp đầy là chiến lược cắt giảm mặc định của cộng đồng.


> **【拓展：数据标注与质量】**视觉任务的效果高度依赖标签数据质量――Label Studio、CVAT là công cụ标签 chính thống――在工业场景中,主动学习(Active Learning) có thể giảm chi phí đánh dấu: mô hình đối với yêu cầu mẫu không xác định

## Chuyển nó đi.

> **【中文解读】**Phần này tập trung vào cách phân phối mô hình như một sản phẩm có thể sử dụng.


Bài học này mang lại:

- `outputs/prompt-classifier-pipeline-auditor.md` một lời nhắc kiểm tra kịch bản đào tạo cho năm biến số trên và xuất hiện vi phạm đầu tiên.
- `outputs/skill-classification-diagnostics.md` một kỹ năng, với một số lượng hỗn loạn và một danh sách tên lớp, tóm tắt các thất bại cho từng lớp và đề xuất giải pháp độc đáo có tác động nhất.

> **【中文解读】**练题按照 Easy/Medium/Hard 三个难度递进;;建议至少完成 级别的题目, 级别适合深入研究或面试准备;;


## Tập luyện bài tập

1. **(Easy | 简单)**Cụ thể, các mô hình có thể được sử dụng trong 5 thời gian trên bộ dữ liệu tổng hợp.
   分别用有/无混 训练 5 时代, vẽ luyện tập và chứng minh mất 曲线, giải thích tại sao sự mất tập của sự hỗn hợp còn cao hơn nhưng tỷ lệ xác minh chính xác vẫn không khác nhau.

2. **(Medium | 中等)**Thực hiện Cutout  0, một hình vuông 8x8 ngẫu nhiên trong mỗi hình ảnh đào tạo  và chạy một sự trừu tượng so với không tăng, hflip+crop, hflip+crop+cutout, hflip+crop+mixup.
   实现 Cutout (随机遮 8x8 区域), đối với không tăng cường,翻转+ cắt cắt,翻转+ cắt+ cắt+Cutout,翻转+ cắt+Míchup bốn cách thức thực hiện các thí nghiệm tiêu hóa, báo cáo xác nhận tỷ lệ准确――

3. **(Hard | 困难)**Xây dựng một đường ống CIFAR-100 (100 lớp, cùng kích thước đầu vào) và tái tạo một cuộc tập luyện ResNet-34 chạy trong phạm vi 1% độ chính xác được xuất bản.
   Lập CIFAR-100 流水线(100 类),复现 ResNet-34 kết quả đào tạo với tỷ lệ độ phân biệt công khai 1% 以内。进阶: tìm kiếm

## Từ khóa  Keyword

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|----------------------|---------|
| Logits | "Raw outputs" | The pre-softmax vector of C numbers per image; cross-entropy expects these, not softmaxed values | Logits：softmax 之前的原始输出向量，交叉熵直接接收它 |
| Cross-entropy | "The loss" | Negative log-probability of the correct class; combines log-softmax and NLL in one stable op | 交叉熵：正确类别的负对数概率，融合了 log-softmax 和 NLL |
| DataLoader | "The batcher" | Wraps a dataset with shuffling, batching, and (optional) multi-worker loading; gets blamed for half of training bugs | 数据加载器：封装数据集的打乱、分批、多进程加载 |
| Augmentation | "Random transforms" | Any pixel-level transform at training time that preserves the label; teaches invariances the CNN does not have natively | 数据增强：训练时保持标签不变的像素级变换，教会模型 CNN 天生不具备的不变性 |
| Mixup / Cutmix | "Mix two images" | Blend both inputs and labels so the classifier learns smooth interpolations instead of hard boundaries | Mixup/Cutmix：混合两张图像及其标签，让分类器学习平滑插值 |
| Label smoothing | "Softer targets" | Replace one-hot with (1-eps, eps/(C-1), ...); improves calibration and slightly boosts accuracy | 标签平滑：用软标签替代 one-hot，改善概率校准 |
| Top-k accuracy | "Top-5" | The correct class is in the k highest-probability predictions; used on datasets with genuinely ambiguous classes | Top-k 准确率：正确类别在前 k 个预测中即算对 |
| Confusion matrix | "Where errors live" | C x C table where entry (i, j) counts images of true class i predicted as j; diagonal is right, off-diagonal tells you what to fix | 混淆矩阵：C×C 表格，对角线是正确预测，非对角线揭示混淆的类别对 |

> **【中文解读】**延伸阅读 cung cấp các nguồn chất lượng cao cho việc học sâu. Những bài báo và giảng dạy này là tài liệu tham khảo cổ điển trong lĩnh vực này, phù hợp với những người đọc cần hiểu sâu hơn.


## Xem thêm 延伸阅读

- [CS231n: Training Neural Networks](https://cs231n.github.io/neural-networks-3/) vẫn là chuyến đi rõ ràng nhất của đường ống đào tạo trên một trang
- [Bag of Tricks for Image Classification (He et al., 2019)](https://arxiv.org/abs/1812.01187) mỗi trò lừa nhỏ cộng lại thêm 3-4% cho độ chính xác ResNet trên ImageNet
- [mixup: Beyond Empirical Risk Minimization (Zhang et al., 2017)](https://arxiv.org/abs/1710.09412) bài viết hỗn hợp ban đầu; ba trang lý thuyết cộng với các thí nghiệm thuyết phục
- [Why temperature scaling matters (Guo et al., 2017)](https://arxiv.org/abs/1706.04599) giấy chứng minh các mạng hiện đại là sai cân và sửa nó với một tham số scalar
