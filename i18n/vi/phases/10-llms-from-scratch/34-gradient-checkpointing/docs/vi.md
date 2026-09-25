# Đánh giá và tính toán lại kích hoạt độ kiểm tra điểm và tính toán kích hoạt

> Backprop giữ mọi kích hoạt trung gian. ở các tham số 70B và ngữ cảnh 128K đó là 3 TB kích hoạt mỗi cấp bậc. Checkpoint giao dịch FLOPs cho bộ nhớ: tính lại thay vì lưu. Câu hỏi là những phân đoạn nào để thả, và câu trả lời không phải là "tất cả chúng".

> **【中文解读】**Tránh hướng truyền cần lưu tất cả các hoạt động trung gian ∞70B 参数 + 128K 上下文 = 每卡 3TB 激活∞梯度检查点使用计算换显存:丢弃部分激活,需要时重新计算∞关键问题是丢弃哪些答案不是"全部"∞

> **【拓展：梯度检查点→大模型训练】**梯度检查点是训练大模型的标标技术――PyTorch's torch.utils.checkpoint、DeepSpeed's activation checkpointing 都是实现这一思想――在128K 上下文训练中,选择性检查点可以节省60%+的显存――

>  **【前置】**Học本节前请先掌握:Phase 10·04(Pre-Training GPT); 反向传播算法;GPU 显存层次(SRAM vs HBM)。本节是训练超大模型 + 长上下文时的关键技术。
>  **【类比】**梯度检查点 = 出差只带必要文件──反向传播── 工作完成后回顾所有材料;不检查点 = 把出差路上的所有材料都背着(占满行李箱);全检查点 = 只带护照,需要时重新打印(重算成本高);选择性检查点 = 只扔重算的(如草稿),保留重建的(如合同) 平衡存储和速度显著──

**Type:** Build
**Languages:** Python (with numpy, optional torch)
**Prerequisites:** Phase 10 Lesson 04 (Pre-Training Mini-GPT), Phase 10 Lesson 05 (Scaling & Distributed)
**Time:** ~70 minutes

## Vấn đề  vấn đề giới thiệu

Việc đào tạo một bộ biến đổi lưu trữ, cho mỗi lớp, các đầu vào cho mỗi hoạt động được phân biệt ngược: đầu vào chú ý, dự đoán Q / K / V, đầu ra softmax, đầu vào FFN, đầu ra chuẩn và dòng dư thừa. Đối với một lớp có kích thước ẩn `d`, chiều dài chuỗi `L`, lô`B`, đây là theo lệnh của `12 * B * L * d`Lượng nước lơ lửng trên mỗi lớp.

>  training transformer 时, mỗi tầng cần lưu trữ ngược chiều truyền trong mỗi nhỏ hoạt động của đầu vào: chú ý đầu vào  Q/K/V 投影、softmax 输出、FFN 输入、归化输出和残差流── đối với ẩn lớn`d`、序列长度 `L`、 lượng `B`Lớp, đó là khoảng mỗi lớp.`12 * B * L * d`个浮点数.

Vì `d=8192, L=8192, B=1`, đó là 800 MB / lớp trong BF16. Một mô hình 64 lớp là 51 GB của kích hoạt  và đó là trước khi bạn nhân bằng kích thước microbatch, trước khi bạn thêm trung gian chú ý-softmax (`L^2`mỗi đầu), và trước khi bạn tính toán các bản sao phụ song thoáng.

>  Đối với `d=8192, L=8192, B=1`,BF16 下 mỗi tầng 800 MB──64 tầng mô hình kích hoạt là 51 GB`L^2`), còn không có kế hoạch vào phần phụ của đường hành trình

Các hóa đơn hai mặt: BF16 trọng lượng cộng với trạng thái tối ưu hóa có thể phù hợp với 80GB, nhưng kích hoạt đẩy bạn qua. kiểm tra điểm (tương tự là tính toán lại kích hoạt) là sự cố tiêu chuẩn. Thả hầu hết các kích hoạt; làm lại phía trước trong thời gian ngược để lấy lại chúng. Chi phí: FLOPs bổ sung. Lợi ích: trí nhớ giảm theo tỷ lệ các phân đoạn điểm kiểm tra với tổng lớp.

> 双面账单:BF16 权重加优化器状态可能放入80GB,但激活值让你超出──梯度检查点(又称激活重计算) là quy tắc sửa chữa tiêu chuẩn── bỏ đi phần lớn giá trị kích hoạt; trong quá trình truyền ngược lại, tái làm trước và truyền để phục hồi chúng──代价:额外FLOPs──收益:显存按检查段数与总层数比例下降──

Khi kiểm tra điểm là một bước đi, chi phí kiểm tra điểm là khoảng 33% hơn FLOP vượt qua phía trước mỗi bước. Được thực hiện tốt. kiểm tra điểm chọn lọc cho "sự lựa chọn thông minh" của Korthikanti et al. Bạn tiết kiệm bộ nhớ 5x cho dưới 5% FLOP Overhead. Và với các bộ phận FP8, FSDP offload, và chuyên gia đồng bộ MoE điều này thực sự quan trọng: bạn không thể đủ khả năng cho bộ nhớ hoặc tính toán lãng phí.

## Khái niệm cốt lõi

> **【中文解读】**梯度检查点(Gradient Checkpointing) sử dụng tính toán chuyển lưu: trước hướng传播时不保存中间激活值,反向传播时重新计算需要的激活──

> **【拓展：梯度检查点在训练中的关键作用】**梯度检查点是训练大模型的标标技术――对于Llama 3 70B, không có điểm kiểm tra khi mỗi mẫu cần khoảng 16GB 激活值显存, mở sau giảm xuống khoảng 5GB―― kết hợp với FSDP và 混合精度, điểm kiểm tra梯度 cho phép đào tạo trong GPU 显存有限 显存大模型成为可能――


### Những gì người trở lại thực sự cần

`output = layer(input)`- Thằng kia muốn`grad_input`và `grad_params`Để tính toán chúng, cần:

- `input`(để tính toán `grad_params = input.T @ grad_output`cho các lớp tuyến tính)
- một số chất trung gian dẫn xuất kích hoạt (trái xuất của ReLU/GELU/softmax phụ thuộc vào giá trị kích hoạt)

Các thông qua phía trước lưu trữ chúng tự động trong biểu đồ autograd.`tensor.retain_grad()`và mỗi hoạt động cần thông tin của nó giữ một tham chiếu.

### Thêm vào toàn bộ điểm kiểm soát

Chia mạng thành 2 phần`N`Trong thời gian chuyển tiếp, chỉ lưu trữ * input * cho mỗi phân đoạn. Khi ngược cần trung gian, chạy lại đoạn chuyển tiếp của phân đoạn để thực hiện chúng, sau đó phân biệt.

Ví dụ: Máy biến 32 lớp chia thành 32 phân đoạn mỗi lớp là 1 lớp.

- Khoá: 32 đầu vào lớp (các) so với 32 * (thời lượng kích hoạt mỗi lớp) (chưa lớn).
- Lượng tính toán thêm: 1 phần nào thêm tiến lên, tức là tổng số FLOP tiến lên ~33% (vì ngược lại là 2x tiến lên, bước hoàn chỉnh trở thành 1 + 1 + 2 = 4 đơn vị thay vì 1 + 2 = 3).

Đây là công thức của Chen et al. 2016: mỗi điểm kiểm soát`sqrt(L)`L=64, đó là 8 điểm kiểm tra.

### Địa chỉ chọn lọc (Korthikanti 2022)

Không phải tất cả các kích hoạt đều có giá tương tự.`B*L*L*heads`và tăng lên *quadratically* với chiều dài chuỗi.`B*L*4d`và phát triển theo đường thẳng. Đối với các chuỗi dài Softmax thống trị.

Việc kiểm tra chọn lọc giữ lại các kích hoạt giá rẻ để lưu trữ (những dự đoán tuyến tính, dư lượng) và tính lại chỉ những thứ đắt tiền (trông trọng).

Megatron-Core thực hiện điều này như là tính toán lại kích hoạt "đặc biệt". được sử dụng trong hầu hết các cuộc đào tạo biên giới 2024+.

### Thả tải

Thay vì tính toán lại: vận chuyển kích hoạt CPU RAM giữa phía trước và phía sau. yêu cầu băng thông PCIe; có lợi khi băng thông vô hiệu vượt quá chi phí tái vật liệu hóa. Các chiến lược hỗn hợp phổ biến: kiểm tra một số lớp, thả các lớp khác.

FSDP2 đưa ra tải xuống như một lựa chọn hạng nhất. tải xuống chiếu sáng khi GPU bị tắc nghẽn trong bộ nhớ nhưng chuyển giao CPU-GPU có không gian đầu.

### Mô hình chi phí tính lại

Các bước phác động với các điểm kiểm soát ngây thơ mỗi `k`các lớp ngoài `L`- Có thể là:

```
flops_fwd_normal = L * f_layer
flops_bwd_normal = 2 * L * f_layer
flops_total_normal = 3 * L * f_layer

flops_fwd_ckpt = L * f_layer
flops_recompute = L * f_layer  # one extra forward per layer in the segment
flops_bwd_ckpt = 2 * L * f_layer
flops_total_ckpt = 4 * L * f_layer
overhead = 4 / 3 - 1 = 0.33 = 33%
```

Với việc kiểm tra chọn lọc bạn chỉ tính lại hạt nhân chú ý, không phải toàn bộ lớp:

```
flops_recompute_selective = L * f_attention ~= L * f_layer * 0.15
overhead_selective = (3 + 0.15) / 3 - 1 = 0.05 = 5%
```

### Mô hình tiết kiệm trí nhớ

Tăng lượng kích hoạt mỗi lớp: `A`- Vì `L`Lớp, bộ nhớ kích hoạt tổng thể: `L * A`- Tôi không biết.

Điểm kiểm soát đầy đủ (kích thước phân đoạn 1): chỉ lưu trữ `L * input_volume`(~`L * 1/10 A`cho một biến đổi tiêu chuẩn).`9 * L * A * 1/10`- Tôi không biết.

Địa điểm kiểm soát mỗi lần`k`Lớp: lưu trữ `L/k * A`+`k-1`giá trị của các lớp trong phân khúc hoạt động.

Tại `k = sqrt(L)`, bộ nhớ và tính toán lại chi phí cả hai quy mô với `sqrt(L)` sự thỏa hiệp tối ưu cho các lớp chi phí đồng nhất.

### Khi không đến điểm kiểm soát

- Các tầng sâu nhất của một giai đoạn đường ống đã được thực hiện.
- Các lớp đầu tiên và cuối cùng nếu họ thống trị tính toán của giai đoạn ( hiếm khi ở các bộ chuyển đổi).
- Các hạt nhân chú ý đã sử dụng FlashAttention  Flash đã tính lại softmax nhanh chóng, vì vậy việc kiểm tra cấp độ lớp bổ sung thêm ít hơn.

### Các mẫu thực hiện

1. **Function wrapper:**lấn một phần trong `torch.utils.checkpoint.checkpoint(fn, input)`Chỉ có cửa hàng PyTorch thôi`input`, tính toán lại mọi thứ khác ngược lại.

2. **Decorator-based:**nhãn các lớp như là kiểm tra điểm; huấn luyện viên quyết định tại thời điểm cấu hình những phân đoạn nào được gói.

3. **Manual explicit recompute:**tự viết bài đi ngược lại, gọi là một thói quen `recompute_forward`Tái lặp đi lặp lại forward với input được lưu trữ.

Cả ba đều có kết quả chức năng tương tự.

### Sự tương tác với TP / PP / FP8

- **Tensor parallel:**Các đầu vào tại điểm kiểm soát phải được thu thập hoặc phân phối lại trên máy tính lại; xử lý chi phí truyền thông.
- **Pipeline parallel:**mô hình điển hình là kiểm tra các bước đường ống dẫn dẫn để các microbacch có thể sử dụng lại bộ nhớ kích hoạt.
- **FP8 recompute:**các lịch sử amax được cập nhật trong thời gian tính toán lại phải phù hợp với các chuyển động quy mô trước ban đầu, hoặc FP8.


> **【拓展：梯度检查点与 FSDP 的配合】**Các điểm kiểm tra độ thường được sử dụng cùng với FSDP/ZeRO. Phân tích phân tích và tình trạng tối ưu hóa của FSDP, điểm kiểm tra độ giảm giá trị hoạt động hiển thị, hai thứ này là sự bổ sung. Đối với mô hình cấp 70B, điểm kiểm tra độ FSDP + độ kiểm tra độ + độ chính xác hỗn hợp cho phép tập luyện trên 8xA100 trở nên có thể.


## Hãy xây dựng nó.
```figure
activation-recompute
```

## Hãy xây dựng nó

### Bước 1: Một mô hình đồ chơi với các đoạn

```python
import numpy as np


def linear_forward(x, w, b):
    return x @ w + b


def relu(x):
    return np.maximum(x, 0)


def layer_forward(x, w1, b1, w2, b2):
    h = relu(linear_forward(x, w1, b1))
    return linear_forward(h, w2, b2)


def model_forward(x, params):
    activations = [x]
    h = x
    for w1, b1, w2, b2 in params:
        h = layer_forward(h, w1, b1, w2, b2)
        activations.append(h)
    return h, activations
```

### Bước 2: Thử trở lại một cách ngây thơ cần tất cả các hoạt động

```python
def model_backward(grad_output, activations, params):
    grads = [None] * len(params)
    g = grad_output
    for i in range(len(params) - 1, -1, -1):
        w1, b1, w2, b2 = params[i]
        x_in = activations[i]
        h_pre = linear_forward(x_in, w1, b1)
        h = relu(h_pre)
        gh = g @ w2.T
        gw2 = h.T @ g
        gb2 = g.sum(axis=0)
        g_pre = gh * (h_pre > 0)
        gx = g_pre @ w1.T
        gw1 = x_in.T @ g_pre
        gb1 = g_pre.sum(axis=0)
        grads[i] = (gw1, gb1, gw2, gb2)
        g = gx
    return g, grads
```

### Bước 3: Điểm kiểm tra - Mỗi bộ nhớ

```python
def model_forward_checkpointed(x, params, k=4):
    saved_inputs = [x]
    h = x
    for i, (w1, b1, w2, b2) in enumerate(params):
        h = layer_forward(h, w1, b1, w2, b2)
        if (i + 1) % k == 0:
            saved_inputs.append(h)
    return h, saved_inputs


def model_backward_checkpointed(grad_output, saved_inputs, params, k=4):
    grads = [None] * len(params)
    g = grad_output
    segments = [(j * k, min((j + 1) * k, len(params))) for j in range(len(saved_inputs))]
    for seg_idx in range(len(saved_inputs) - 1, -1, -1):
        start, end = segments[seg_idx]
        if start >= end:
            continue
        x_in = saved_inputs[seg_idx]
        _, seg_acts = model_forward(x_in, params[start:end])
        g, seg_grads = model_backward(g, seg_acts, params[start:end])
        for j, gr in enumerate(seg_grads):
            grads[start + j] = gr
    return g, grads
```

### Bước 4: Mô hình chi phí

```python
def checkpoint_cost(n_layers, segment_size, flops_per_layer=1.0):
    fwd = n_layers * flops_per_layer
    recompute = n_layers * flops_per_layer
    bwd = 2 * n_layers * flops_per_layer
    return {
        "fwd": fwd,
        "recompute": recompute,
        "bwd": bwd,
        "total": fwd + recompute + bwd,
        "overhead_vs_no_ckpt": (fwd + recompute + bwd) / (fwd + bwd) - 1.0,
    }


def selective_checkpoint_cost(n_layers, attention_fraction=0.15,
                              flops_per_layer=1.0):
    fwd = n_layers * flops_per_layer
    recompute = n_layers * attention_fraction * flops_per_layer
    bwd = 2 * n_layers * flops_per_layer
    return {
        "fwd": fwd,
        "recompute": recompute,
        "bwd": bwd,
        "total": fwd + recompute + bwd,
        "overhead_vs_no_ckpt": (fwd + recompute + bwd) / (fwd + bwd) - 1.0,
    }
```

### Bước 5: Máy đánh giá bộ nhớ

```python
def activation_memory_mb(n_layers, hidden=8192, seq=8192,
                        batch=1, bytes_per_value=2):
    per_layer = 12 * batch * seq * hidden * bytes_per_value
    return n_layers * per_layer / 1e6


def memory_after_checkpoint(n_layers, segment_size, hidden=8192,
                           seq=8192, batch=1, bytes_per_value=2):
    n_seg = max(1, n_layers // segment_size)
    saved = (n_seg + segment_size) * 1 * batch * seq * hidden * bytes_per_value
    return saved / 1e6
```

### Bước 6: kích thước phân đoạn tối ưu

```python
def optimal_segment(n_layers):
    return int(round(np.sqrt(n_layers)))
```

### Bước 7: Quyết định kiểm soát chọn lọc

```python
def should_recompute(layer_type, activation_bytes, recompute_flops_ratio):
    if layer_type == "attention" and activation_bytes > 100 * 1e6:
        return True
    if layer_type == "ffn" and activation_bytes > 500 * 1e6:
        return recompute_flops_ratio < 0.1
    return False
```

## Hãy sử dụng nó để thực hiện

- **torch.utils.checkpoint**`from torch.utils.checkpoint import checkpoint` bọc canonical trong PyTorch. Bọc một chức năng; chỉ lưu trữ đầu vào, tính lại về phía sau.
- **Megatron-Core activation recomputation**: hỗ trợ `selective`- `full`, và`block`Các phương pháp chuẩn trong đào tạo biên giới 2024+.
- **FSDP2 offload**`module.to_empty(device="cpu")`với `offload_policy`trong FSDP2 chia các kích hoạt vào CPU thay vì tính lại.
- **DeepSpeed ZeRO-Offload**: CPU offload cho trạng thái tối ưu hóa và kích hoạt, bổ sung vào kiểm tra điểm.

## Chuyển nó đi.

Bài học này sẽ mang lại kết quả `outputs/prompt-activation-recompute-policy.md` một lời nhắc lấy cấu hình mô hình của bạn (vị lớp, ẩn, seq, batch) và bộ nhớ GPU có sẵn và phát hành chính sách tính lại mỗi lớp (không / chọn lọc / đầy đủ / tải xuống).

> 本课产 出 `outputs/prompt-activation-recompute-policy.md` Một cấu hình mô hình chấp nhận (nói: 层数, 隐藏维度,序列长度,批次) và GPU có sẵn trong lưu trữ và输出 mỗi tầng về kế hoạch tính toán (无 / 选择性 / 完全 / 卸载) 

## Tập luyện bài tập

1. Kiểm tra tính chính xác.`model_forward`+ `model_backward`(bản kích hoạt đầy đủ) vs `model_forward_checkpointed`+ `model_backward_checkpointed`Các gradient tham số phải giống nhau với độ chính xác máy.
   Trung文翻译:验证正确性──运行 `model_forward`+ `model_backward`(完整激活) với `model_forward_checkpointed`+ `model_backward_checkpointed`(分段) ◊ Đường độ số phải phù hợp với độ chính xác của máy.

2. kích thước phân đoạn dọn `k`từ 1 đến `L`- Tìm đầu gối của đường cong.
   Trung ngữ翻译:将段大小 `k`Từ 1 đến 1`L`◊ vẽ FLOP 开销和内存―― tìm đường cong của góc.

3. Thực hiện kiểm tra chọn lọc: lưu trữ đầu vào của mô-đun chú ý nhưng không phải trung gian của nó. đo đạc FLOP trên cùng với kiểm tra toàn lớp cho mô hình 32 lớp ở seq=8192.
   Trung文翻译:实现选择性检查点: lưu trữ注意力模块输入但不存中间结果──测量 32层模型在 seq=8192 下与全层检查点的 FLOP 开销比较──

4. Thêm tải xuống. Tự lưu các đầu vào phân đoạn vào một "cuộc đệm CPU" mô phỏng (một danh sách riêng biệt). đo "giới băng thông PCIe" như byte / thời gian và tìm điểm chia cắt giữa tải xuống và tính lại.
   Trung文翻译:添加卸载──将段输入保存到模拟的"CPU缓冲区" (CPU缓冲区) 单独的列表) 以字节/时间测量"PCIe 带宽"并找到卸载和重计算之间的平衡点──

5. Đánh giá một biến đổi PyTorch thực sự với và không có `torch.utils.checkpoint`- đo bộ nhớ (via `torch.cuda.max_memory_allocated`) và thời gian bước.
   Trung文翻译:对真实 PyTorch biến đổi 分别使用和不使用 `torch.utils.checkpoint`进行基准测试──测量内存(通过 `torch.cuda.max_memory_allocated`(Với người hâm mộ lựa chọn)

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|----------------------|---------|
| Gradient checkpointing | "Save memory by redoing forward" | Store segment inputs only; recompute intermediates during backward to get gradient-support tensors | 梯度检查点，仅保存段输入，反向时重算中间值 |
| Activation recomputation | "Same as checkpointing" | The HPC-flavored name for the same technique | 激活重计算，梯度检查点的 HPC 叫法 |
| Segment size (k) | "How many layers per checkpoint" | Number of layers whose intermediates are dropped and rematerialized together | 段大小，每个检查点包含的层数 |
| Selective checkpointing | "Korthikanti's trick" | Recompute only expensive-to-store activations (attention softmax); keep cheap ones | 选择性检查点，只重算存储昂贵的激活 |
| Full checkpointing | "The naive version" | Recompute every layer's intermediates in every segment | 全量检查点，朴素版本重算所有中间值 |
| Block checkpointing | "Coarse-grained" | Checkpoint whole transformer blocks; largest granularity | 块级检查点，以 Transformer 块为粒度 |
| FLOP overhead | "The compute tax" | Extra FLOPs per step = (recompute FLOPs) / (fwd + bwd FLOPs); 33% naive, 5% selective | FLOP 开销，朴素版 33%，选择性版 5% |
| Activation offload | "Ship to CPU" | Move activations to CPU RAM across forward->backward; alternative to recompute | 激活卸载，将激活移到 CPU 内存 |
| sqrt-L rule | "The classical optimum" | For uniform-cost layers, optimal checkpoint spacing is sqrt(L) layers | sqrt-L 规则，均匀层代价的最优检查点间隔 |
| Attention-softmax volume | "The O(L^2) problem" | L^2 * heads * batch floats; dominates activation memory at long contexts | 注意力 softmax 体积，O(L^2) 的显存问题 |

## Xem thêm 延伸阅读

- [Chen et al., 2016 -- "Training Deep Nets with Sublinear Memory Cost"](https://arxiv.org/abs/1604.06174)- giấy gốc đã chính thức hóa kiểm tra độ
- [Korthikanti et al., 2022 -- "Reducing Activation Recomputation in Large Transformer Models"](https://arxiv.org/abs/2205.05198)-- tính toán lại hoạt động chọn lọc và phân tích chi phí chính thức
- [Pudipeddi et al., 2020 -- "Training Large Neural Networks with Constant Memory using a New Execution Algorithm"](https://arxiv.org/abs/2002.05645)-- Phương pháp tiếp cận thay thế về bộ nhớ liên tục thông qua tái vật lý hóa chế độ ngược
- [Ren et al., 2021 -- "ZeRO-Offload: Democratizing Billion-Scale Model Training"](https://arxiv.org/abs/2101.06840)-- kích hoạt tải xuống trên quy mô
- [PyTorch torch.utils.checkpoint docs](https://pytorch.org/docs/stable/checkpoint.html)-- API tiêu chuẩn
- [Megatron-Core activation recomputation documentation](https://docs.nvidia.com/nemo-framework/user-guide/latest/nemotoolkit/features/memory_optimizations.html)-- các chế độ chọn lọc, đầy đủ và chặn
