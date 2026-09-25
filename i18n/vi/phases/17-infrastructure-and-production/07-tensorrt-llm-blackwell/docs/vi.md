# TensorRT-LLM trên Blackwell với FP8 và NVFP4
# Bộ máy cứng chuyên ngành Inference Compilation  FP8 và NVFP4 trên Blackwell

> Bộ máy tính chuyên dụng thu thập kết luận giao dịch khả năng di động cho thông suất, và TensorRT-LLM  NVIDIA-chỉ, điều chỉnh cho Blackwell  là ví dụ rõ ràng nhất về việc giao dịch trả tiền.$0.012 per million tokens on a 120B model in Q1-Q2 2026, against $0.09/M trên H100 + vLLM  khoảng cách kinh tế 7 lần. Bộ đống là ba chế độ điểm nổi hợp nhất: FP8 vẫn quan trọng cho kho lưu trữ KV và hạt nhân chú ý vì nó có phạm vi động lực họ cần; NVFP4 (4 bit vi mô) xử lý trọng lượng và kích hoạt; dự đoán đa token (MTP) và prefill / decode phân chia thêm 2-3x khác trên cùng. Day-0 hỗ trợ mô hình tải trọng FP4 trực tiếp mà không cần chuyển đổi sau đào tạo. Sự bắt giữ cho các nhóm kỹ thuật năm 2026: TRT-LLM là nguồn mở nhưng đặc biệt cho NVIDIA  CUDA- và Blackwell chuyên dụng  vì vậy việc áp dụng nó thương mại khả năng di động cho thông suất. Hãy thử toán toán cho các mô hình và phần cứng trước khi bắt đầu.

> **【中文解读】**Bài viết này giới thiệu về TensorRT-LLM và BlackwellNVIDIA's LLM 推理优化框架和最新 GPU 架构──
**Type:** Learn
**Languages:** Python (stdlib, toy FP8/NVFP4 memory and cost calculator)
**Prerequisites:** Phase 17 · 04 (Serving Engine Internals), Phase 10 · 13 (Quantization)
**Time:** ~75 minutes


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy FP8/NVFP4 memory and cost calculator) | **语言:** Python（标准库，FP8/NVFP4 内存和成本计算器）
**Prerequisites:** Phase 17 · 04 (vLLM Serving Internals), Phase 10 · 13 (Quantization) | **前置知识:** Phase 17 · 04（vLLM 服务内部）, Phase 10 · 13（量化）

>  **【前置】**Học本节前请先掌握:Phase 17·04(vLLM) 、Phase 10·13(量化基础) ・・・TensorRT-LLM là NVIDIA 专属优化, trên Blackwell GPU 上性能最强──
>  **【类比】**TensorRT-LLM = "NVIDIA 专属跑车"―GB200 NVL72 上 SemiAnalysis 测:120B 模型 $0.012/百万 token（H100+vLLM $0.09)  7 倍经济性差距──三套浮点叠加:FP8(KV cache+注意 动态范围) + NVFP4(4-bit 权重激活) + MTP/解 prefill-decode 再加 2-3 倍──代价:闭源 NVIDIA ,可移植性换吞吐──选型前必须按你的模型/硬件组合算账──
**Time:** ~75 minutes | **时间:** ~75 分钟

## Mục tiêu học tập

- Giải thích tại sao FP8 vẫn quan trọng đối với cache và sự chú ý của KV ngay cả khi trọng lượng ở NVFP4.
  Trung ngữ翻译: giải thích tại sao ngay cả trong NVFP4, FP8 đối với KV 缓存和注意力 vẫn quan trọng.
- Xét dấu chân HBM của mô hình biên giới theo BF16, FP8 và NVFP4 và lý luận về nguồn gốc tiết kiệm.
  Trung ngữ翻译:计算前沿模型在BF16、FP8 和 NVFP4 下的HBM占用,分析节省来自哪里──
- Tên các tính năng đặc biệt của Blackwell TRT-LLM khai thác (ngày-0 FP4, MTP, phân chia dịch vụ, tất cả các nguyên thủy).
  Trung文翻译:说出 TRT-LLM利用的黑威尔特有功能(day-0 FP4、MTP、分离式服务、all-to-all 原语)。
- Hãy quyết định khi nào khóa NVIDIA của TRT-LLM sẽ đáng giá 7 lần chênh lệch giá so với vLLM trên Hopper.
  Trung文翻译: quyết định TRT-LLM của NVIDIA 锁定何时值相比Hopper 上 vLLM của 7x 成本差距──

## Vấn đề  vấn đề giới thiệu

> **【中文解读】**2026 năm suy nghĩ về vấn đề tiền tuyến kinh tế là" mỗi USD多少 token"──答案取决于四层叠加选择:硬件代际(Hopper H100/H200 vs Blackwell B200/GB200)、精度(BF16 → FP8 → NVFP4)、推理引擎(vLLM vs SGLang vs TRT-LLM) 和编排(朴素 vs 分离式 vs Dynamo)──在 Hopper + vLLM 上运行 120B MoE 约$0.09/M tokens；在 Blackwell + TRT-LLM + Dynamo 上仅 $0.012/M7x 差距── giá của sự khác biệt này là NVIDIA 锁定你无法复现在其他厂商的硬件──

> **【拓展：NVIDIA Blackwell 架构】**Blackwell (B200/GB200) là một cấu trúc GPU được phát hành trong năm 2024-2025 của NVIDIA, tương đương với Hopper (H100) trong LLM 推理 có 11-15x mỗi GPU 吞吐提升.

Biên giới của kinh tế suy luận vào năm 2026 là "các mã thông báo mỗi đô la". Câu trả lời phụ thuộc vào bốn lựa chọn xếp chồng lên: thế hệ phần cứng (Hopper H100/H200 vs Blackwell B200/GB200), độ chính xác (BF16 → FP8 → NVFP4), động cơ phục vụ (vLLM vs SGLang vs TRT-LLM), và dàn xếp (sơn vs phân chia vs Dynamo).

> 2026 năm suy nghĩ kinh tế học tiền tuyến là" mỗi USD bao nhiêu token"──答案取决于四个叠加选择:硬件代际(Hopper vs Blackwell)、精度(BF16 → FP8 → NVFP4)、推理引擎(vLLM vs SGLang vs TRT-LLM) 和编排(朴素 vs 分离式 vs Dynamo)──

Trên Hopper với vLLM, một MoE 120B chạy ở ~$0.09 per million tokens. On Blackwell with TRT-LLM + Dynamo, the same model runs at ~$0.012  7x rẻ hơn. Một số khoảng cách đó là phần cứng (Blackwell là 11-15x cho mỗi GPU LLM thông qua so với Hopper). Một số là hàng: trọng lượng FP4, bản thảo MTP, prefill / decode phân chia, và NVLink 5 toàn bộ cho giao tiếp chuyên gia MoE.

> Trong Hopper + vLLM 上,120B MoE 运行约 $0.09/M tokens。在 Blackwell + TRT-LLM + Dynamo 上，同一模型运行约 $0.012便宜 7 倍──部分差距来自硬件(Blackwell vs Hopper Mỗi GPU LLM 吞吐 11-15 倍)──部分来自:FP4 权重、MTP草案、分离式预填/解码和 NVLink 5 tất cả mọi người dùng cho MoE 专家通信──

Bạn không thể sao chép điều này bên ngoài nồi NVIDIA. Đó là sự thỏa hiệp  khả năng di chuyển cho kinh tế học.

> Bạn không thể có được sự tái hiện bên ngoài NVIDIA. Đó là trọng lượng chuyển thể chuyển thể kinh tế.

## Khái niệm cốt lõi

### Tại sao FP8 vẫn là sàn cho KV cache

> **【中文解读】**FP8 là yêu cầu độ chính xác tối thiểu của KV Cache. KV Cache  lưu trữ giá trị trọng tâm  kiều trị vượt qua rất rộng động thái phạm vi. KV  định lượng đến FP4 sẽ dẫn đến mất độ chính xác thảm họa. NVFP4 chỉ áp dụng cho trọng lượng và kích hoạt 缩缩 để cho mỗi khối trọng lượng có yếu tố缩 tự do.

Một sai lầm phổ biến vào năm 2026: giả định NVFP4 áp dụng ở mọi nơi. Nó không. KV cache cần FP8 (8 bit floating point) vì nó lưu trữ các khóa chú ý và giá trị trải dài một phạm vi động rộng. Quantizing KV đến FP4 gây ra mất độ chính xác thảm khốc.

> Một sai lầm phổ biến năm 2026: giả định NVFP4  áp dụng cho tất cả mọi nơi. Không có. KV 缓存 cần FP8 (vùng 8 位浮点), vì nó lưu trữ vượt qua phạm vi động thái rộng.

NVFP4 (2025-2026) áp dụng cho trọng lượng và kích hoạt. Microscaling: mỗi khối trọng lượng có nhân thang riêng của nó để các khối nhỏ có thể trải dài các phạm vi động khác nhau mà không mất thang độ per-tensor. Đối với các kích hoạt, FP4 giữ lại vì các kích hoạt là phạm vi nhỏ trong một lớp.

> NVFP4(2025-2026) áp dụng cho trọng lượng và kích hoạt.

Một kiểu hình ảnh của Blackwell:

- trọng lượng: NVFP4 (4 bit quy mô nhỏ).
  Trung文翻译:权重:NVFP4(4-bit 微缩放) 』
- Tích hoạt: NVFP4.
  Trung ngữ翻译:激活:NVFP4──
- KV cache: FP8.
  Trung文翻译:KV 缓存:FP8。
- Bộ tích lũy sự chú ý: FP32 (thường độ ổn định tối đa mềm).
  Trung文翻译:注意力累加器:FP32(softmax 稳定性)

### Các nguyên thủy đặc biệt của Blackwell TRT-LLM sử dụng

- **Day-0 FP4 weights**: các nhà cung cấp mô hình vận chuyển trọng lượng FP4 trực tiếp; tải TRT-LLM mà không cần chuyển đổi sau đào tạo. Không có bước AWQ / GPTQ cho FP4.
  Trung ngữ翻译:**Day-0 FP4 权重**: mô hình cung cấp trực tiếp phát hành FP4 权重;TRT-LLM 无需训练后转换即可载;;FP4 不需要 AWQ/GPTQ 步骤;;
- **Multi-token prediction (MTP)**: cùng một ý tưởng như EAGLE (Phase 17 · 05) nhưng tích hợp vào TRT-LLM xây dựng.
  Trung ngữ翻译:**多 token 预测 (MTP)**: 与 EAGLE 相同的想法(Phase 17 · 05), nhưng tập hợp thành TRT-LLM 构建中──
- **Disaggregated serving**: prefill và decode trên các bộ nhớ GPU riêng biệt, cache KV được chuyển qua NVLink hoặc InfiniBand.
  Trung ngữ翻译:**分离式服务**: Prefill và mã hóa trên GPU độc lập, KV 缓存 thông qua NVLink hoặc InfiniBand 传输
- **All-to-all communication primitives**NVLink 5 cắt giảm độ trễ giao tiếp chuyên gia MoE bằng 3x so với Hopper.
  Trung ngữ翻译:**All-to-all 通信原语**NVLink 5 sẽ giảm thời gian thông tin thông tin 3 lần.
- **NVFP4 + MXFP8 microscaling**: xử lý các yếu tố quy mô nhanh chóng trên các lõi Tensor Blackwell.
  Trung ngữ翻译:**NVFP4 + MXFP8 微缩放**: Blackwell Tensor Core trên phần cứng tăng tốc gia tăng xử lý yếu tố

### Những con số mà bạn nên ghi nhớ

- HGX B200 tại $ 0.02 / M token trên GPT-OSS-120B thông qua TRT-LLM.
  Trung文翻译:HGX B200 在 GPT-OSS-120B 上通过TRT-LLM 为 $0.02/M token──
- GB200 NVL72 tại $ 0,012/M token thông qua Dynamo (trong tổ chức TRT-LLM).
  Trung文翻译:GB200 NVL72 通过 Dynamo(编排 TRT-LLM)为 $0.012/M token。
- H100 + vLLM ≈ $ 0.09 / M token trên khối lượng công việc tương đương.
  Trung ngữ翻译:H100 + vLLM 在可比工作负载上约$0.09/M token──
- tăng thông qua 2,8 lần trong ba tháng cập nhật TRT-LLM (2026).
  Trung ngữ翻译:TRT-LLM 2026 年三月更新的 2.8 倍吞吐量提升──
- 11-15 lần mỗi lần GPU LLM, Blackwell vs Hopper.
  Trung文翻译:Blackwell vs Hopper Mỗi GPU LLM 吞吐量 11-15 倍。
- MLPerf Inference v6.0 (ngày 4 tháng 4 năm 2026): Blackwell thống trị mọi nhiệm vụ được gửi.
  Trung文翻译:MLPerf Inference v6.0(2026 年 4 月):Blackwell 在所有提交任务中领先──

### Giá trị thực tế của FP4 về chất lượng

> **【中文解读】**NVFP4 trong việc tính toán tải trọng công việc dày đặc (思维链、数学、长上下文代码生成) sẽ dẫn đến sự suy giảm chất lượng có thể nhìn thấy được. Mỗi khối tiêu chuẩn có thể giảm nhưng không thể loại bỏ.

> **【拓展：量化精度 vs 推理成本权衡】** chọn lọc độ chính xác là cân bằng chất lượng và chi phí:(1) BF16 không có tổn thất chất lượng, nhưng nhu cầu trong bộ nhớ lớn(70B  mô hình cần 140GB);(2) FP8 gần như không bị tổn thất, Hopper / Blackwell  tần hóa phần cứng, được khuyến cáo để đưa ra các nhiệm vụ đặc biệt;(3) INT4(AWQ / GPTQ) 4-bit  trọng lượng, MATH 分数 giảm 3-5 điểm, phù hợp với các cuộc trò chuyện chung;(4) NVFP4 cực kỳ, Blackwell  chuyên dụng, phải được đánh giá mục tiêu.

NVFP4 là tích cực. Trên khối lượng công việc có tính toán nặng (thể sợi tư duy, toán học, mã gen với bối cảnh dài), trọng lượng FP4 giảm đi đáng kể. Độ chuẩn hóa mỗi khối giảm nhưng không loại bỏ. Các mô hình lý luận vận chuyển của nhóm thường sử dụng trọng lượng FP8 + kích hoạt FP4 như một thỏa hiệp, hoặc gắn bó với H200 với FP8 trong suốt.

> NVFP4 là kích thích. Trong các khối lượng công việc dày đặc của suy nghĩ (思维链,数学,长上下文代码生成) trên, FP4 权重明显退化.

Quy tắc: luôn xác nhận chất lượng nhiệm vụ trên bộ đánh giá của bạn trước khi cam kết với trọng lượng NVFP4.

> Quy tắc: Trước khi nộp NVFP4 权重, luôn luôn trong tập hợp đánh giá của bạn trên xác minh chất lượng nhiệm vụ.

### Tại sao đây là quyết định khóa NVIDIA

> **【中文解读】**TRT-LLM là một bộ phận của C++ + CUDA + 闭源内核. Mô hình cần được cấu trúc SKU GPU cụ thể. Không hỗ trợ AMD, Intel hoặc ARM. Nếu chiến lược cơ sở hạ tầng của bạn là nhiều nhà cung cấp, TRT-LLM là một lựa chọn không thể lựa chọn.

> **【拓展：NVIDIA vs AMD 推理生态】**2026  AI  Tâm lý thị trường chip:NVIDIA  Với CUDA 生态 và TRT-LLM chiếm khoảng 80% cổ phần trung tâm dữ liệu  AMD MI300X có sức cạnh tranh trên tính năng ban đầu, nhưng phần mềm (ROCm + vLLM) vẫn đang theo đuổi  Intel Gaudi 3 là một lựa chọn khác nhưng tỷ lệ sử dụng thấp hơn  Đối với doanh nghiệp có chi tiêu đầu tư hàng năm $100M +, chuyển đến Blackwell + TRT-LLM + Dynamo 7x chênh lệch chi phí có thể tiết kiệm hàng ngàn triệu đô la.

TRT-LLM là các lõi nguồn đóng C++ + CUDA +. Các mô hình cần được biên soạn cho một SKU GPU cụ thể. Không AMD, không Intel, không ARM. Nếu chiến lược hạ tầng của bạn là đa nhà cung cấp, TRT-LLM là một không khởi động cho cấp độ TRT-LLM phục vụ.

> TRT-LLM là một bộ phận của C++ + CUDA + 闭源内核. Mô hình cần được cấu trúc SKU GPU cụ thể. Không hỗ trợ AMD, Intel hoặc ARM. Nếu chiến lược cơ sở hạ tầng của bạn là nhiều nhà cung cấp, TRT-LLM là không thể chạy. Bạn vẫn có thể sử dụng vLLM trên các phần cứng hỗn hợp. Nếu chỉ có NVIDIA, khoảng cách 7x đáng để khóa này.

### 2026 công thức thực tế

Đối với hóa đơn suy luận hàng năm 100 triệu +, chạy trên Hopper + vLLM để lại 7-10x trên bảng. Chuyển tải công việc chi phí thống trị đến Blackwell + TRT-LLM + Dynamo. Giữ cấp thử nghiệm trên H100 + vLLM cho tốc độ lặp lại mô hình. Thiết lập chất lượng trên mỗi mô hình NVFP4 chuyển đổi trước khi sản xuất.

> Đối với chi phí dự đoán hàng năm 100M +, hoạt động trên Hopper + vLLM có nghĩa là để lại 7-10 lần tiết kiệm không gian.

### Tặng thưởng phân tích

Các bộ phận phân chia của TRT-LLM (bể chứa và giải mã riêng biệt) được bao gồm sâu trong giai đoạn 17 · 20. Ở Blackwell, các bộ đống nhân: trọng lượng FP4 × tăng tốc MTP × vị trí phân chia × định tuyến lưu trữ. Số 7x giả định bộ đống đầy đủ này.

> TRT-LLM's phân chia式服务(独立预填充和码池) trong giai đoạn 17 · 20 中深入讨论。 trên Blackwell,乘数叠加:FP4 权重 × MTP 加速 × 分离式部署 × 缓存感知路由──7x 数字假设使用完整──

## Hãy sử dụng nó để thực hiện

> **【拓展：Blackwell 迁移决策】**Từ Hopper 迁移到Blackwell + TRT-LLM 决策框架:(1) Giai đoạn chi tiêu suy luận hàng năm có vượt quá $5M không?是→ đáng đánh giá chuyển động;(2) Có thể chấp nhận NVIDIA 锁定?否→ tiếp tục sử dụng vLLM + Hopper;(3) 工作负载是否包含 MoE 模型?是→Blackwell NVLink 5 toàn bộ 提供额外3x 加速;(4) 推理密集型任务占比是否超过30%?是→需要验证 NVFP4 质量――迁移 ROI通常在 6-12 个月内回本.
```figure
pipeline-parallel
```

## Sử dụng nó

`code/main.py`tính toán dấu chân HBM, giải mã thông qua (chế độ gắn nhớ) và mã thông báo $/M cho một mô hình trên ba ngăn xếp: H100 + BF16 + vLLM, H100 + FP8 + vLLM, B200 + NVFP4/FP8 + TRT-LLM.

> `code/main.py`计算模型在三个上 HBM 占用、解码吞吐量(内存受限) 和 $/M-tokens:H100 + BF16 + vLLM、H100 + FP8 + vLLM、B200 + NVFP4/FP8 + TRT-LLM──运行它查看复合效应和每个变化贡献差距份额──

## Chuyển nó đi.

Bài học này sẽ mang lại kết quả `outputs/skill-trtllm-blackwell-advisor.md`Với khối lượng công việc, kích thước mô hình và khối lượng mã thông báo hàng năm, nó quyết định liệu khối Blackwell + TRT-LLM có đáng giá với khóa NVIDIA hay không.

> 本课产 出 `outputs/skill-trtllm-blackwell-advisor.md` Được định nghĩa tải trọng làm việc  mô hình  và lượng token hàng năm, nó quyết định Blackwell + TRT-LLM  liệu nó có đáng để NVIDIA  khóa 

## Tập luyện bài tập

1. Đi chạy`code/main.py`. Trên một 120B MoE với các tham số hoạt động 30%, tính toán thông qua mã hóa có giới hạn băng thông bộ nhớ trên H100 BF16, H100 FP8, và B200 NVFP4/FP8.
   Trung ngữ翻译:运行 `code/main.py` Trong 30%  active parameter 120B MoE trên, tính H100 BF16、H100 FP8 và B200 NVFP4/FP8 trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong trong
2. Một khách hàng chi 2 triệu USD/năm cho H100 + vLLM. Số lượng GPU Blackwell cần mua để giảm giá chuyển sang TRT-LLM trong 12 tháng, với khoảng cách kinh tế 7x?
   Trung ngữ翻译: khách hàng trên H100 + vLLM 上每年花费2M $.
3. Bạn sẽ thấy độ chính xác giảm 3 điểm trên MATH sau khi chuyển đổi trọng lượng NVFP4. Hãy cho biết hai con đường phục hồi: một chất lượng trước (giữ trọng lượng FP8) và một chi phí trước (sự chuẩn hóa với dữ liệu trong lĩnh vực).
   Trung文翻译:NVFP4 权重转换后 MATH 精度下降 3 点──说出两条恢复路径:一条质量优先(保持 FP8 权重),一条成本优先(用领域内数据校准)
4. Đọc kết quả suy luận MLPerf v6.0. nhiệm vụ nào có khoảng cách nhỏ nhất về Blackwell-over-Hopper, và tại sao?
   Trung文翻译:阅读 MLPerf v6.0 推理结果──哪个任务的黑威尔-over-Hopper 差距最小,为什么?
5. Xét HBM cần thiết cho mô hình 405B ở trọng lượng NVFP4 + FP8 KV cache ở ngữ cảnh 128k.
   Trung文翻译:计算 405B 模型在 NVFP4 权重 + FP8 KV 缓存 + 128k 上下文下 HBM 需求──它 có phù hợp với một GB200 NVL72 节点?

## Từ khóa  Từ khóa nhanh chóng

| Term / 术语 | What people say / 通俗说法 | What it actually means / 实际含义 |
|------|----------------|------------------------|
| FP8 | "eight-bit float" / "8-bit 浮点" | 8-bit floating point; used for KV cache and attention due to dynamic range / 8-bit 浮点；因动态范围用于 KV 缓存和注意力 |
| NVFP4 | "four-bit micro" / "4-bit 微缩放" | NVIDIA's 4-bit microscaling FP format; weights and activations on Blackwell / NVIDIA 4-bit 微缩放浮点格式；Blackwell 上的权重和激活 |
| MXFP8 | "MX eight" / "MX 8-bit" | Microscaling FP8 variant; hardware-accelerated on Blackwell Tensor Cores / 微缩放 FP8 变体；Blackwell Tensor Core 硬件加速 |
| Day-0 FP4 | "ship FP4 weights" / "直接发布 FP4 权重" | Model providers release weights already in FP4; no post-train conversion step / 模型提供商直接发布 FP4 权重；无训练后转换步骤 |
| MTP | "multi-token prediction" / "多 token 预测" | TRT-LLM's integrated speculative-decoding draft (Phase 17 · 05) / TRT-LLM 集成的推测解码 draft |
| Disaggregated serving | "split prefill/decode" / "分离预填充/解码" | Prefill and decode on separate GPU pools; KV transferred over NVLink/IB / 独立 GPU 池的预填充和解码 |
| All-to-all | "MoE expert comm" / "MoE 专家通信" | Communication pattern routing tokens to expert GPUs; NVLink 5 cuts 3x / 将 token 路由到专家 GPU 的通信模式 |
| InferenceX | "SemiAnalysis inference bench" / "推理基准" | The 2026 industry-accepted cost-per-token benchmark / 2026 年行业接受的每 token 成本基准 |

## Xem thêm 延伸阅读

- [NVIDIA — Blackwell Ultra MLPerf Inference v6.0](https://developer.nvidia.com/blog/nvidia-blackwell-ultra-sets-new-inference-records-in-mlperf-debut/) Tháng 4 năm 2026 kết quả MLPerf.
- [NVIDIA — MoE Inference on Blackwell](https://developer.nvidia.com/blog/delivering-massive-performance-leaps-for-mixture-of-experts-inference-on-nvidia-blackwell/) NVLink 5 tất cả mọi người và hạt nhân MoE.
- [TensorRT-LLM Overview](https://nvidia.github.io/TensorRT-LLM/overview.html) Tài liệu động cơ chính thức.
- [NVIDIA — Introducing Dynamo](https://developer.nvidia.com/blog/introducing-nvidia-dynamo-a-low-latency-distributed-inference-framework-for-scaling-reasoning-ai-models/) dàn nhạc phân chia trên TRT-LLM.
- [MLPerf Inference](https://mlcommons.org/benchmarks/inference-datacenter/) bộ điểm chuẩn xuất bản số Blackwell.
