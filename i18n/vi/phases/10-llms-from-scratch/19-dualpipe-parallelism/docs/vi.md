# DualPipe Parallelism 双向流水线并行

> DeepSeek-V3 được đào tạo trên 2.048 GPU H800 với các chuyên gia MoE phân tán trên các nút. Chuyên gia giao tiếp toàn cầu qua nút chi phí 1 giờ giao tiếp GPU cho mỗi giờ tính toán GPU. GPU đã không hoạt động một nửa thời gian. DualPipe (DeepSeek, Dec 2024) là một đường ống hai chiều mà chồng chéo về phía trước và ngược với các giao tiếp tất cả mọi thứ mà họ kích hoạt. Sự giảm bong bóng, tăng thông suất, và giữ hai bản sao mô hình-pharameter (những "những đôi" cho tên gọi) là rẻ khi Expert Parallelism đã phân tán các chuyên gia trên các hàng không bất cứ cách nào. Bài học này là một bài học về những gì DualPipe thực sự làm và tại sao tinh chỉnh DualPipeV của Sea AI Lab làm giảm chi phí tham số 2x với chi phí của bong bóng chặt chẽ hơn.

> **【中文解读】**DeepSeek-V3 trong 2048 张 H800 上训练,MoE 专家分布在节点间――跨节点所有-to-all 通信让 GPU một nửa thời gian chờ đợi――DualPipe là dòng chảy nước hai chiều, sẽ chuyển về phía trước/ ngược về phía tính toán với tất cả-to-all 通信重叠, giảm气泡、提升吞吐──

> **【拓展：DualPipe→大规模训练】**DualPipe là chìa khóa của đào tạo hiệu quả cao của DeepSeek-V3: nó sẽ làm cho việc giao tiếp của MoE với chuyển tiếp / ngược ngược tính toán chồng lên, khiến hiệu quả đào tạo trên 2048 card gần như mở rộng tuyến tính.

>  **【前置】**学本节前请先掌握:Phase 10·05(Scaling Distributed);MoE(Mích hợp các chuyên gia) khái niệm;流水线并行(Pipeline Parallelism) cơ sở; tất cả mọi người 通信模式。本节是Phase 10·20(DeepSeek-V3 Walkthrough) 的并行策略详解。

**Type:** Learn
**Languages:** Python (stdlib, schedule simulator)
**Prerequisites:** Phase 10 · 05 (distributed training, FSDP, DeepSpeed), Phase 10 · 14 (open-model architectures and MoE)
**Time:** ~60 minutes

## Mục tiêu học tập

- Hãy cho tên bốn thành phần của một bộ phận DualPipe về phía trước và về phía sau và tại sao mỗi bộ phận có cửa sổ chồng chéo riêng.
  Nói ra bốn thành phần của DualPipe phía trước- ngược phía bên kia khối và các nguyên nhân của cửa sổ chồng lên của riêng mình
- Giải thích vấn đề bong bóng đường ống ở quy mô, và "không bong bóng" có nghĩa là gì trong thực tế so với tiếp thị.
  Giải thích vấn đề về nước chảy lớn, cũng như sự khác biệt giữa "không khí" và lý thuyết tiếp thị trong thực tế
- Theo dõi lịch trình DualPipe bằng tay cho 8 hàng PP và 16 micro-batch và xác nhận dòng chảy về phía trước và ngược lấp đầy các khe trống của nhau.
  Cử lý theo dõi 8 giai đoạn PP và 16 tập nhỏ DualPipe 调度, xác nhận hướng thẳng và ngược dòng điền vào các khoảng trống của nhau
- Cụ thể hóa sự thỏa hiệp DualPipeV (Sea AI Lab, 2025) thực hiện: giảm bản sao hóa tham số 2x với chi phí của một bong bóng lớn hơn một chút khi Expert Parallelism không hoạt động.
  Nói rõ DualPipeV(Sea AI Lab, 2025) 权衡:取消 2x 参数复制,代价是专家平行 不活时气泡稍大

## Vấn đề  vấn đề giới thiệu

Việc đào tạo một mô hình MoE 671B trên 2k H800 GPU chạy vào ba nút thắt:

1. **Memory pressure.**Mỗi GPU chứa một mảnh của mô hình. Khoảnh khắc kích hoạt ở chuỗi 8k trên 61 lớp trên 128 đầu là rất lớn.
2. **Pipeline bubbles.**Sự tương đồng đường ống truyền thống (GPipe, 1F1B) khiến các GPU không hoạt động trong khi họ chờ đợi đầu vào hoặc độ nghiêng của giai đoạn của họ.
3. **Cross-node all-to-all.**MoE với sự song song chuyên gia phân tán các chuyên gia qua các nút. Mỗi thông qua phía trước kích hoạt tất cả mọi người để gửi token cho các chuyên gia của họ, và một khác để kết hợp.

> Trong 2k H800 GPU 上训练 671B MoE 模型会遇到三个复合瓶:

1. **内存压力。**Mỗi GPU có một đoạn mô hình. Dường độ chuỗi 8k, 61 tầng, 128 đầu hoạt động là rất lớn.
   Trung ngữ翻译: 每张 GPU 持有模型的一个片──8k 序列长度、61层、128头的活显存是巨大的──
2. **流水线气泡。**传统流水线并行(GPipe、1F1B) để GPU chờ đợi bước vào hoặc bước ở thời gian空──8 个阶段, ngay cả khi sử dụng 1F1B调度, khoảng 12% thời gian của GPU có thể là bong bóng──
   Trung ngữ翻译:传统流水线并行让GPU 在等待时空──8个阶段时,约 12% của GPU 时间是气泡──
3. **跨节点全互联。**带专家并行的MOE sẽ phân tán các chuyên gia đến từng node. Mỗi lần phát sóng, một lần toàn bộ mạng sẽ phân phối token cho các chuyên gia, một lần khác sẽ kết quả hợp lại.
   Trung ngữ翻译:MoE 专家并行每次前向传播触发两次全互联通信, trong 2k GPU 时计算通信比接近 1:1──

Mỗi một trong những giải pháp này có các giải pháp riêng biệt: kiểm tra độ cho bộ nhớ, Vung điện Zero (Sea AI Lab, 2023) cho các bong bóng đường ống, hạt nhân truyền thông chuyên gia song song song cho tất cả mọi người. DualPipe làm gì là làm cho họ chơi cùng nhau. Lập trình chồng chéo tính toán và truyền thông trong một phần phía trước-lưng lại duy nhất, tiêm các lô vi nhỏ từ cả hai đầu của đường ống đồng thời, và sử dụng lịch trình kết quả để ẩn tất cả mọi thứ bên trong cửa sổ tính toán.

Kết quả được báo cáo: gần như loại bỏ các bong bóng đường ống, sử dụng GPU trên 95% trong quá trình đào tạo mã thông báo 14.8T của DeepSeek-V3.

## Khái niệm cốt lõi

> **【中文解读】**DualPipe là DeepSeek-V3 đưa ra thuật toán tiếp tục dòng chảy hai chiều, thông qua tính toán chồng lên giữa đường hướng trước và ngược chiều để tối đa hóa tỷ lệ sử dụng GPU.

> **【拓展：DualPipe 与 DeepSeek-V3 的效率】**DeepSeek-V3 sẽ giảm tỷ lệ buồng nước xuống khoảng 5% (khoảng 20% theo phương pháp truyền thống), là một trong những kỹ thuật quan trọng của DeepSeek-V3 được đào tạo với khoảng 5.60 triệu USD cho mô hình hàng đầu.


### Tái mới sự song song đường đường đường ống

Chia mô hình lớp N trên các thiết bị P. Thiết bị `i`giữ các lớp`i * N/P .. (i+1) * N/P - 1`. Một micro-batch chảy về phía trước qua các thiết bị 0 đến P-1, sau đó trở lại từ P-1 đến 0. Mỗi thiết bị chỉ có thể bắt đầu giai đoạn tiến của nó khi thiết bị trước đó gửi ra đầu ra của nó và chỉ có thể bắt đầu trở lại khi thiết bị dòng chảy xuống gửi gradient dòng chảy lên.

GPipe (Huang et al., 2019) lập kế hoạch một micro-batch một lúc, mà lãng phí hầu hết thời gian GPU. 1F1B (Narayanan et al., 2021) chuyển giao chuyển tiếp về phía trước và ngược cho nhiều lô vi. Zero Bubble (Qi et al., 2023) chia quá trình ngược lại thành hai phần  ngược-đối với đầu vào (B) và ngược-đối với trọng lượng (W)  và lập lịch trình để lấp đầy bong bóng. Sau "Thùng Xanh", đường ống đã gần như bị chặt chẽ.

DualPipe là bước tiếp theo. Nó thêm hai ý tưởng lên:

### Ý tưởng 1: phân hủy phần

Mỗi phần phía trước được chia thành bốn thành phần:

- **Attention.**Dự án Q/K/V, chú ý, dự án đầu ra.
- **All-to-all dispatch.**Truyền thông qua các nút, gửi token cho các chuyên gia của họ.
- **MLP.**Các chuyên gia tính toán của Bộ.
- **All-to-all combine.**Truyền thông qua các nút mang lại kết quả chuyên môn.

Một phần ngược thêm các phiên bản gradient của mỗi phần này. DualPipe lập lịch chúng để tất cả các chuyển phát xảy ra song song với tính toán chú ý của phần tiếp theo, và tất cả kết hợp xảy ra song song với tính toán MLP của phần tiếp theo.

### Ý tưởng 2: lập trình hai chiều

Hầu hết các kế hoạch đường ống tiêm các lô vi nhỏ từ giai đoạn 0 và chảy về hướng giai đoạn P-1. DualPipe tiêm các lô vi nhỏ từ cả hai đầu.

Để điều này hoạt động, thiết bị `i`phải giữ cả hai lớp ống đầu tiên `i`Và lớp ống cuối cùng.`P - 1 - i`Đây là phần "hai" của DualPipe: mỗi thiết bị giữ hai bản sao của các lớp mô hình cần thiết để phục vụ (một cho mỗi hướng). Ở quy mô của DeepSeek-V3, đây là chi phí sao chép tham số 2x. Nó có giá cả phải chăng vì Expert Parallelism đã phân tán các chuyên gia MoE mỏng đến nỗi sao chép các lớp không chuyên gia hai lần là khoai tây nhỏ.

Điều quan trọng là dòng chảy về phía trước và dòng chảy ngược về phía sau cùng nhau ở đúng nơi mà các bong bóng sẽ ở trong một lịch trình hướng duy nhất.

### Một lịch trình được theo dõi bằng tay

Hãy xem xét P = 4 hàng, 8 micro-batch, chia 4 về phía trước / 4 ngược. Thời gian di chuyển từ trái sang phải; hàng là hàng thiết bị.

```
           Time →
rank 0:  F1 F2 F3 F4  F5R F6R F7R F8R  B1 B2 B3 B4  ...
rank 1:     F1 F2 F3  F4/F5R F6R F7R   B1 B2 ...
rank 2:        F1 F2  F3/F5R F4/F6R    B1 ...
rank 3:           F1  F2/F5R F3/F6R    ...
```

Đọc ghi chú "F4/F5R": xếp hạng 1 là đi trước micro-batch 4 (đi từ trái sang phải trong đường ống dẫn) Và đi trước micro-batch 5 (đi từ phải sang trái) trong khoảng thời gian tương tự. Đó là điều mà "tương hướng hai" có nghĩa là hoạt động.

Ở cấp 2 các dòng băng chồng chéo sớm hơn, ở cấp 0 và P-1 chúng chồng chéo sau cùng. Trong giai đoạn trung bình ổn định của lịch trình, mỗi cấp chạy về phía trước của X-nghĩa hướng chồng chéo với phía sau của Y-nghĩa hướng.

### Tài khoản bong bóng

Hình thức thông thường 1F1B bong bóng đường ống (thời gian lãng phí theo cấp):

```
bubble_1F1B = (P - 1) * forward_chunk_time
```

Phong trào tinh tế của bong bóng không mang lại nó xuống nhưng không đến không. DualPipe, trong giai đoạn ổn định, có bong bóng không nếu số lượng các lô vi nhỏ được chia bằng 2 lần độ sâu đường ống. Bên ngoài giai đoạn ổn định (sưởi ấm và làm mát), có một số bong bóng nhưng nó không phát triển với số lượng các lô vi nhỏ.

Về mặt tiếp thị: "không bong bóng". Về mặt kỹ thuật: bong bóng không phát triển với số lượng các lô vi. Phân tích tiếp theo của Sea AI Lab (DualPipeV / Cut-in-half) chỉ cho thấy bong bóng không đầy đủ khi Expert Parallelism không phải là nút thắt; với EP-driven all-to-all, một số thỏa hiệp lập lịch luôn có mặt.

### DualPipeV  tinh chế

Sea AI Lab (2025) nhận thấy rằng việc sao chép các tham số 2x là lãng phí khi sự chồng chéo truyền thông EP không phải là điểm. Chương trình DualPipeV của họ gấp lại tiêm hai chiều thành một lịch trình "v-shaped" chạy trên một bản sao tham số duy nhất. Vung bóng lớn hơn DualPipe một chút, nhưng tiết kiệm bộ nhớ là đáng kể. DeepSeek đã áp dụng DualPipeV trong việc triển khai DualPipe mã nguồn mở của họ như một chế độ EP-off.

Sự đổi mới:

| Feature | DualPipe | DualPipeV | 1F1B | Zero Bubble |
|---------|---------|-----------|------|------------|
| Param copies per device | 2 | 1 | 1 | 1 |
| Bubble vs micro-batches | constant | small growth | grows | grows |
| Compute-comm overlap | full | partial | minimal | partial |
| Use when | EP-heavy MoE | dense or EP-light | baseline | any pipeline |

### Điều đó có nghĩa là một token 14.8T chạy

Việc đào tạo trước của DeepSeek-V3 đã tiêu thụ 14,8T token trên 2.048 GPU H800 trong khoảng 2,8M giờ GPU. Với 1F1B ngây thơ, họ sẽ mất 12-15% của số đó để bong bóng đường ống  340-420K giờ GPU, đủ để đào tạo một mô hình 70B đầy đủ. DualPipe đã lấy lại phần lớn. Việc định lượng trực tiếp đóng góp là khó khăn mà không có nhật ký nội bộ, nhưng tuyên bố trong bài báo là sử dụng GPU trung bình trên 95% trong suốt đào tạo.

Đối với các chạy nhỏ hơn (dưới 1k GPU), DualPipe là quá mức  bong bóng đường ống nhỏ hơn so với tổng chi phí, và đào tạo mô hình dày đặc hiếm khi chạm vào nút thắt toàn bộ.

### Ở chỗ nó ngồi trong đống

- Dùng với **FSDP**(Phase 10 · 05). FSDP chia nhỏ các tham số mô hình qua các hàng; DualPipe lập kế hoạch tính toán qua các hàng.
- Thích hợp với **ZeRO-3**Các kế toán cho bản sao hai bản cần hợp tác với các gradient của ZeRO.
- - Đang yêu cầu**custom all-to-all kernels**Các lõi nguồn mở của DeepSeek là thực hiện tham chiếu.


> **【拓展：流水线并行的工程细节】**DualPipe trong cùng một hướng chuyển đổi về phía trước và ngược về phía lây lan, tỷ lệ phun khí sẽ giảm từ khoảng 20% xuống còn khoảng 5%.


## Hãy sử dụng nó để thực hiện
```figure
expert-capacity
```

## Sử dụng nó

`code/main.py`là một mô phỏng lịch trình đường ống.`(P, n_micro_batches, schedule)`và in sử dụng giai đoạn ổn định cho mỗi 1F1B, Vung điện không, DualPipe và DualPipeV. Đây là một công cụ giảng dạy  các con số phù hợp với các tuyên bố chất lượng trong các bài báo, chúng không phải là một tuyên bố về sản xuất đo tốc độ.

Giá trị của máy mô phỏng: chạy nó với số lượng P và micro-batch khác nhau và xem cách phân số bong bóng phát triển cho 1F1B nhưng không DualPipe.

Các cân nhắc tích hợp cho một khóa đào tạo thực tế:

- Chọn một độ sâu song song đường ống phân chia rõ ràng vào số lượng micro-batch của bạn.
- Hãy đảm bảo lưới đồng đều của chuyên gia của bạn hỗ trợ tất cả mọi thứ hai chiều.
- Hãy mong đợi một tuần thời gian làm lỗi trên lịch trình lần đầu tiên.
- Theo dõi GPU sử dụng theo cấp bậc, không chỉ tổng hợp lợi ích của DualPipe đến từ việc chặt chẽ các chất lỏng.

## Chuyển nó đi.

Bài học này sẽ mang lại kết quả `outputs/skill-dualpipe-planner.md`. Với một đặc điểm cụm đào tạo (đếm GPU, topology, kết nối, hình dạng mô hình), nó khuyến cáo một chiến lược song song đường đường ống, thuật toán lập lịch sử để sử dụng, và phần bong bóng dự kiến ở quy mô mục tiêu.

> 本课产 出 `outputs/skill-dualpipe-planner.md` Đưa ra các quy tắc tập hợp tập hợp của GPU số lượng,拓、互连、模型形状), nó đề xuất các chiến lược và quy trình dòng chảy, điều chỉnh thuật toán và tỷ lệ dự kiến của khối lượng khí trong quy mô mục tiêu.

## Tập luyện bài tập

1. Đi chạy`code/main.py``(P=8, micro_batches=16, schedule=dualpipe)`và `(P=8, micro_batches=16, schedule=1f1b)`- Xét sự khác biệt sử dụng GPU và thể hiện nó như GPU-hours phục hồi trên mỗi triệu token đào tạo.
   Trung ngữ翻译:在 `(P=8, micro_batches=16, schedule=dualpipe)`和 `(P=8, micro_batches=16, schedule=1f1b)`上运行 `code/main.py`△ tính GPU sử dụng tỷ lệ khác nhau并 cho mỗi triệu training token 回收的 GPU 小时数──

2. Dấu họa bảng lịch cho `(P=4, micro_batches=8, schedule=dualpipe)`bằng tay. đánh dấu mỗi khe thời gian với thẻ ID và hướng của micro batch. xác định khe thời gian đầu tiên mà các bong bóng không có.
   Trung ngữ翻译:手动画出 `(P=4, micro_batches=8, schedule=dualpipe)`                                                                                                                                                                                                                                                              

3. Đọc Hình 5 của báo cáo kỹ thuật DeepSeek-V3 (arXiv:2412.19437). Xác định cửa sổ chồng chéo cho việc gửi tất cả mọi thứ bên trong một phần phía trước DualPipe. Giải thích cách lịch trình tính toán che giấu nó.
   Trung文翻译:阅读 DeepSeek-V3 技术报告图 5――识别 DualPipe 前向块内所有对所有调度的重叠窗口――解释计算调度如何隐藏它――

4. Xét số 2x tham số chi phí trên của DualPipe cho một mô hình dày 70B với các giai đoạn đường ống P=8 và mô hình 671B MoE với các giai đoạn đường ống P=16.
   Trung ngữ翻译:计算 DualPipe đối với 70B 密集模型 ((P=8 流水线阶段) và 671B MoE 模型 ((P=16 阶段) của 2 倍参数开销;;展示为什么 MoE 情况的开销比例较小;;大多数参数是专家,跨大型 EP 组分片) ;;

5. So sánh DualPipe với Chimera (một lập trình viên hai chiều cạnh tranh từ năm 2021).
   Trung ngữ翻译:比较 DualPipe 与 Chimera(2021年的竞争双向调度器) ◦识别 DualPipe 添加的 Chimera 没有的两个特定属性,使用论文第 3.4 节作为参考──

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|------------------------|---------|
| Pipeline bubble | "Idle time per rank" | GPU cycles wasted because a pipeline stage is waiting for its input or gradient | 流水线气泡，GPU 等待输入或梯度时空转的周期 |
| 1F1B | "Default pipeline schedule" | One forward / one backward interleaved scheduling; the baseline DualPipe beats | 1F1B 调度，一前向一反向交替 |
| Zero Bubble | "Sea AI Lab 2023" | Splits backward into B (input gradient) and W (weight gradient); almost fully tightens the pipeline | 零气泡，将反向拆为输入梯度和权重梯度 |
| DualPipe | "DeepSeek-V3 schedule" | Bidirectional pipeline + compute-comm overlap; bubbles do not grow with micro-batch count | DualPipe，双向流水线+计算通信重叠 |
| DualPipeV | "Cut-in-half" | V-shape refinement that drops the 2x parameter replication at the cost of slightly larger bubbles | DualPipeV，取消 2x 参数复制，气泡略增 |
| Chunk | "Unit of pipeline work" | A forward or backward pass of one micro-batch through one pipeline stage | 块，一个微批次在一个流水线阶段的前向/反向 |
| All-to-all dispatch | "Send tokens to experts" | Cross-node comm that routes tokens to their assigned MoE experts | 全互联分派，将 token 路由到 MoE 专家 |
| All-to-all combine | "Bring expert outputs back" | Cross-node comm that gathers expert outputs after the MLP | 全互联组合，收集专家输出 |
| Expert Parallelism (EP) | "Experts across GPUs" | Shards MoE experts across ranks so different GPUs hold different experts | 专家并行，不同 GPU 持有不同 MoE 专家 |
| Pipeline Parallelism (PP) | "Layers across GPUs" | Shards model layers across ranks; the dimension DualPipe schedules | 流水线并行，模型层分布在不同 GPU |
| Bubble fraction | "Wasted GPU time" | (bubble_time / total_time); the fraction DualPipe drives toward zero | 气泡比例，DualPipe 将其压向零 |

## Xem thêm 延伸阅读

- [DeepSeek-AI — DeepSeek-V3 Technical Report (arXiv:2412.19437), Section 3.3.2 and Figure 5](https://arxiv.org/abs/2412.19437) tham chiếu chính DualPipe
- [DeepSeek — DualPipe GitHub repository](https://github.com/deepseek-ai/DualPipe) thực hiện tham chiếu nguồn mở, bao gồm chế độ DualPipeV (Cut-in-half)
- [Qi et al. — Zero Bubble Pipeline Parallelism (arXiv:2401.10241, Sea AI Lab 2023)](https://arxiv.org/abs/2401.10241) người tiền nhiệm của Zero Bubble
- [Sea AI Lab — DualPipe could be better without the Dual](https://sail.sea.com/blog/articles/63) phân tích DualPipeV thông báo chế độ tắt EP của DeepSeek
- [Narayanan et al. — PipeDream / 1F1B (arXiv:1806.03377, 2018-2021)](https://arxiv.org/abs/1806.03377) lịch trình 1F1B DualPipe so sánh với
- [Huang et al. — GPipe (arXiv:1811.06965, 2018)](https://arxiv.org/abs/1811.06965) vấn đề song song đường ống gốc giấy và bong bóng
