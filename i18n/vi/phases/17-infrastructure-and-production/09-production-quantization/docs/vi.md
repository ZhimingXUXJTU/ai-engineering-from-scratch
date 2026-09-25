# Phân lượng sản xuất  AWQ, GPTQ, GGUF K-quants, FP8, MXFP4/NVFP4 量化 生产

> Phương thức định lượng không phải là một lựa chọn phổ quát  nó là một chức năng của phần cứng, máy phục vụ và tải trọng công việc. GGUF Q4_K_M hoặc Q5_K_M sở hữu CPU và cạnh, được cung cấp thông qua llama.cpp và Ollama. GPTQ thắng trong vLLM khi bạn cần nhiều LoRA trên cùng một cơ sở. AWQ với hạt nhân Marlin-AWQ cung cấp ~ 741 tok/s trên một mô hình lớp 7B với Pass@1 tốt nhất tại INT4  mặc định 2026 cho sản xuất trung tâm dữ liệu. FP8 vẫn là trung tâm trên Hopper, Ada và Blackwell  gần như không mất mát và được hỗ trợ rộng rãi. NVFP4 và MXFP4 (Blackwell microscaling) là tích cực và yêu cầu xác thực mỗi khối. Hai nhóm cắn bẫy: bộ dữ liệu hiệu chuẩn phải phù hợp với miền triển khai, và bộ nhớ cache KV tách biệt với định lượng trọng lượng  bài học AWQ "chương tự của tôi bây giờ là 4 GB" quên bộ nhớ cache KV 10-30 GB ở kích thước loạt sản xuất.

> **【中文解读】**Bài viết này giới thiệu về ứng dụng trong việc giảm chi phí dự đoán của Bộ Sản xuất môi trường quy mô INT8/INT4/FP8.
**Type:** Learn
**Languages:** Python (stdlib, toy memory and throughput comparison across formats)
**Prerequisites:** Phase 10 · 13 (Quantization foundations), Phase 17 · 04 (Serving Engine Internals)
**Time:** ~75 minutes


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy memory and throughput comparison across formats) | **语言:** Python
**Prerequisites:** Phase 10 · 13 (Quantization foundations), Phase 17 · 04 (vLLM Serving Internals) | **前置知识:** Phase 10 · 13 (Quantization foundations), Phase 17 · 04 (vLLM Serving Internals)

>  **【前置】**Học本节前请先掌握:Phase 10·13(量化基础) 、Phase 17·04(vLLM) ⋅量化格式不是普适选择按硬件+引擎+工作负载选──
>  **【类比】**量化格式 = "压缩行李"。GGUF Q4_K_M = 适合火车/edge(CPU 友好);GPTQ = vLLM 多 LoRA 场景;AWQ + Marlin 内核 = 数据中心默认(7B 模型 741 tok/s,INT4 最佳);FP8 = Hopper/Ada/Blackwell 中选择(近乎无损);NVFP4/MXFP4 = 激进,需块逐验证。
> ️ **【易错点】**两个陷:(1) 校准数据集必须匹配部署领域(医疗模型用通用文本校准会失真);(2) "我的模型只有4GB" 忘了KV cache(生产批次10-30GB)。
**Time:** ~75 minutes | **时间:** ~75 minutes

## Mục tiêu học tập

- Hãy nêu tên sáu định dạng định lượng sản xuất và điểm ngọt ngào của chúng vào năm 2026.
  Trung ngữ翻译:说出 2026 年六种生产级量化格式及其最佳使用场景──
- Chọn định dạng phần cứng (CPU vs GPU, Hopper vs Blackwell), động cơ (vLLM, TRT-LLM, llama.cpp), và tải trọng công việc (tác thảo thường xuyên, lý luận, đa LoRA).
  Trung文翻译:根据硬件(CPU vs GPU、Hopper vs Blackwell) 、引擎(vLLM、TRT-LLM、llama.cpp) 和工作负载(通用聊天、推理、多 LoRA) chọn格式──
- Xét bộ nhớ trọng lượng được lưu và bộ nhớ cache KV được để lại không bị ảnh hưởng cho định dạng được chọn.
  Trung ngữ翻译:计算选定格式节省的权重内存和未触及的 KV 缓存──
- Tên lỗi dữ liệu định đo làm suy giảm mô hình định lượng trên lưu lượng domain.
  Trung ngữ翻译: nói出导致量化模型在领域流量上退化的校准数据集陷──

## Vấn đề  vấn đề giới thiệu

> **【中文解读】**量化减少内存和HBM 带宽消耗正是最需要的阶段. 阶段 解码. 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段 阶段

> **【拓展：量化技术演进】**量化技术经历了三代:(1) 均量化(INT8/INT4)  đơn giản nhưng mất độ chính xác lớn;(2) 感知量化(AWQ/GPTQ)  bảo vệ trọng lực,INT4 下质量接近BF16;(3) 浮点量化(FP8/NVFP4) 硬件加速,动态范围更好──2024-2026 年量化研究的核心突破是"微缩"(microscaling)  Mỗi khối trọng lực có yếu tố缩放独立, ở 4-bit 下仍然保持良好──ARK Invest 估计量化贡献了推成本下降约30%──

Quantization làm giảm bộ nhớ và băng thông HBM, đó chính xác là những gì cần để giải mã. Một mô hình FP16 70B là 140 GB trọng lượng. Quantize trọng lượng đến INT4 (AWQ hoặc GPTQ) và mô hình là 35 GB  phù hợp với một H100 với không gian cho bộ nhớ cache KV, điều này quan trọng bởi vì ở 128 chuỗi đồng thời với 2k bối cảnh, bộ nhớ cache KV một mình là 20-30 GB.

> Phân tích giảm bộ nhớ và HBM 带宽 tiêu thụ, chính là điều cần thiết nhất. Phân tích của 70B của FP16 chiếm 140GB. Phân tích sẽ được cân nhắc đến INT4 ((AWQ hoặc GPTQ) mô hình sau chỉ có 35GB.

Nhưng định lượng không phải là miễn phí. định lượng tích cực làm suy giảm chất lượng, đặc biệt là trong các nhiệm vụ suy luận nặng. Các định dạng khác nhau hoạt động với các động cơ khác nhau. Phần cứng khác nhau hỗ trợ độ chính xác khác nhau bản địa. Sở thú định dạng 2026 là thực tế và bạn không thể sao chép sự lựa chọn của người khác.

> Nhưng định lượng hóa không phải là miễn phí. Ưu độ hóa định lượng hóa giảm chất lượng, đặc biệt là tính toán các nhiệm vụ đặc biệt.

## Khái niệm cốt lõi

### 6 hình thức

| Format | Bits | Sweet spot | Engines |
|--------|------|-----------|---------|
| GGUF Q4_K_M / Q5_K_M | 4-5 | CPU, edge, laptops | llama.cpp, Ollama |
| GPTQ | 4-8 | Multi-LoRA on vLLM | vLLM, TGI |
| AWQ | 4 | Datacenter GPU production | vLLM (Marlin-AWQ), TGI |
| FP8 | 8 | Hopper/Ada/Blackwell datacenter | vLLM, TRT-LLM, SGLang |
| MXFP4 | 4 | Blackwell multi-user | TRT-LLM |
| NVFP4 | 4 | Blackwell multi-user | TRT-LLM |

### GGUF  CPU / Edge mặc định

> **【拓展：GGUF 在边缘推理中的地位】**GGUF là định dạng của llama.cpp 和 Ollama, chiếm ưu thế trong suy luận CPU/边缘. Q4_K_M 和 Q5_K_M là sản xuất định dạng trong 4-5 bit xuống đạt gần chất lượng BF16.

GGUF là một định dạng tập tin, không phải là một kế hoạch định lượng riêng  nó kết hợp các biến thể K-quan (Q2_K, Q3_K_M, Q4_K_M, Q5_K_M, Q6_K, Q8_0) trong một thùng. Q4_K_M và Q5_K_M là các mặc định sản xuất  chất lượng gần BF16 ở 4-5 bit.

> GGUF là một định dạng tập tin, bản thân nó không phải là một phương pháp định lượng. Nó sẽ đóng gói K-quant 变体 打包在一个容器中. Q4_K_M 和 Q5_K_M là sản xuất tiêu chuẩn 4-5 bit.

Hình thức không được tối ưu hóa cho các lõi GPU. Sử dụng GGUF khi mục tiêu triển khai là CPU / Edge. Không khác.

> Trong vLLM: 7B  mô hình khoảng 93 tok/s mô hình này không nhắm đến GPU trong hạt nhân tối ưu hóa.

### GPTQ  Multi-LoRA trong vLLM

GPTQ là một thuật toán định lượng sau khi đào tạo với một hiệu suất hiệu chuẩn. lõi Marlin làm cho nó nhanh trên GPU (2.6x tốc độ so với không Marlin GPTQ). ~ 712 tok / s trên 7B.

> GPTQ là một loại thuật toán định lượng sau khi được đào tạo.

Chiến thắng độc đáo: GPTQ-Int4 hỗ trợ bộ chuyển đổi LoRA trong vLLM. Nếu bạn đang phục vụ một mô hình cơ bản cộng với 10-50 biến thể được điều chỉnh tốt (mỗi một là một LoRA), GPTQ là con đường của bạn. NVFP4 vẫn không hỗ trợ LoRA từ đầu năm 2026.

> 独特优势:GPTQ-Int4 trong vLLM hỗ trợ LoRA 适配器── nếu bạn đang trong dịch vụ một mô hình cơ bản thêm 10-50 个微调变体( mỗi như LoRA),GPTQ là con đường của bạn──截至 2026年初 NVFP4 尚不支持 LoRA──

### AWQ  GPU trung tâm dữ liệu mặc định

> **【中文解读】**AWQ(Activation-aware Weight Quantization) là lựa chọn mặc định của GPU trung tâm dữ liệu năm 2026 推理的默认选择──它 trong quá trình bảo vệ lượng hóa khoảng 1% trọng lượng quan trọng nhất, cộng tác với Marlin-AWQ 内核实现 10.9x 加速── trên mô hình 7B đạt ~741 tok/s, là INT4 格式 Pass@1最高的──除非需要多 LoRA(选择 GPTQ) hoặc Blackwell FP4(选择 NVFP4),否应新 GPU 推理项目默认使用 AWQ──

Tiêu chuẩn kích hoạt: Tiêu chuẩn kích hoạt: Tiêu chuẩn kích hoạt: Tiêu chuẩn kích hoạt: Tiêu chuẩn kích hoạt: Tiêu chuẩn kích hoạt: Tiêu chuẩn kích hoạt: Tiêu chuẩn kích hoạt: Tiêu chuẩn kích hoạt: Tiêu chuẩn kích hoạt: Tiêu chuẩn kích hoạt: Tiêu chuẩn kích hoạt: Tiêu chuẩn kích hoạt: Tiêu chuẩn kích hoạt: Tiêu chuẩn kích hoạt: Tiêu chuẩn kích hoạt: Tiêu chuẩn kích hoạt: Tiêu chuẩn kích hoạt: Tiêu chuẩn kích hoạt: Tiêu chuẩn kích hoạt: Tiêu chuẩn kích hoạt: Tiêu chuẩn kích hoạt: Tiêu chuẩn kích hoạt: Tiêu chuẩn kích hoạt: Tiêu chuẩn kích hoạt: Tiêu chuẩn kích hoạt: Tiêu chuẩn kích hoạt: Tiêu chuẩn kích hoạt: Tiêu chuẩn kích hoạt: Tiêu chuẩn kích hoạt: Tiêu chuẩn kích hoạt: Tiêu chuẩn kích hoạt: Tiêu chuẩn kích hoạt: Tiêu chuẩn kích hoạt: Tiêu chuẩn kích hoạt: Tiêu chuẩn kích hoạt: Tiêu chuẩn: Tiêu chuẩn: Tiêu chuẩn: Tiêu chuẩn: Tiêu chuẩn: Tiêu chuẩn: Tiêu chuẩn: Tiêu chuẩn: Tiêu chuẩn: Tiêu chuẩn: Tiêu chuẩn: Tiêu chuẩn: Tiêu chuẩn: Tiêu chuẩn: Tiêu chuẩn: Tiêu chuẩn: Tiêu chuẩn: Tiêu chuẩn: Tiêu chuẩn: Tiêu chuẩn: Tiêu chuẩn: Tiêu chuẩn: Tiêu chuẩn: Tiêu chuẩn: Tiêu chuẩn: Tiêu chuẩn: Tiêu chuẩn: Tiêu chuẩn: Tiêu chuẩn: Tiêu chuẩn: Tiêu chuẩn: Tiêu chuẩn: Tiêu chuẩn: Tiêu chuẩn: Tiêu chuẩn: Tiêu chuẩn: Tiêu chuẩn: Tiêu chuẩn: Tiêu chuẩn: Tiêu chuẩn: Tiêu chuẩn: Tiêu chuẩn: Tiêu chuẩn: Tiêu chuẩn: Tiêu chuẩn: Tiêu chuẩn Títítítítítítítítítít Tít Tít Tít Tít Tít Tít Tít Tít Tít Tít Tít Tít Tít Tít Tít Tít Tít Tít Tít Tít Tít Tít Tít Tít Tít Tít Tít Tít Tít Tít Tít Tít Tít Tít Tít Tít Tít Tít Tít Tít Tít Tít Tít Tít Tít Tít Tít Tít Tít Tít

> 激活感知权重量化──保护量化过程中约1% 最显著的权重──Marlin-AWQ 内核:比朴素方法快 10.9 倍──7B 模型约 741 tok/s,INT4 格式中 Pass@1 最高──

Chọn AWQ cho GPU mới giao dịch trừ khi bạn cần nhiều LoRA (GPTQ) hoặc Blackwell FP4 (NVFP4) hung hăng.

> New GPU 推理项目选择 AWQ, trừ khi cần nhiều LoRA(选择 GPTQ) hoặc激进的 Blackwell FP4(选择 NVFP4)。

### FP8  trung tâm đáng tin cậy

> **【拓展：FP8 量化的生产应用】**FP8(8-bit 浮点) là độ xác định của tình huống không thể thỏa hiệp chất lượng năm 2026[6]. HOPP Tensor Cores nguyên sinh tăng tốc FP8, Blackwell 继承 hỗ trợ。FP8 trong bộ nhớ tiết kiệm là một nửa của INT4, nhưng chất lượng rủi ro là rất thấp trong các trường hợp phát triển mã hóa, y tế, gần như không bị tổn thất.

Điểm nổi 8 bit. gần như không mất mát. Được hỗ trợ rộng rãi. Húpper Tensor Cores tăng tốc FP8 theo bản địa. Blackwell thừa kế. FP8 là mặc định an toàn 2026 khi chất lượng không thể thương lượng (thông luận, y tế, mã gen).

> 8-bit 浮点──近乎无损──广泛支持──Hopper Tensor Cores 原生加速 FP8──Blackwell 继承──当质量不可妥协时(推理、医疗、代码生成),FP8 là lựa chọn được chấp nhận an toàn năm 2026──内存节省 là một nửa của INT4, nhưng chất lượng rủi ro là rất thấp──

### MXFP4 / NVFP4  Blackwell hung hăng

Phân tích nhỏ FP4. Mỗi khối trọng lượng có yếu tố quy mô riêng. Khủng bố nhưng tăng tốc phần cứng trên các lõi Tensor Blackwell. Giảm một nửa các byte mỗi token so với FP8  chiến thắng kinh tế trong giai đoạn 17 · 07.

> 微缩 FP4── mỗi khối trọng lượng có yếu tố缩缩 riêng của nó── kích thích nhưng Blackwell Tensor Cores 硬件加速──相比 FP8 每字节减半Phase 17 · 07 中的经济优势──

Các hang động:
- Không có hỗ trợ LoRA (trước 2026).
  Trung文翻译:截至2026 年初尚不支持 LoRA。
- Sự sụt giảm chất lượng có thể nhìn thấy trên các khối lượng công việc nặng nề.
  Trung ngữ翻译:推理密集型工作负载上可见质量下降──
- Thiết lập giá trị của bạn cho mỗi mô hình.
  Trung ngữ翻译:每个模型在评估集上验证──

### Mẫy hiệu chuẩn

> **【中文解读】**校准数据集陷:AWQ 和 GPTQ 需要校准数据集来决定保护哪些权重. 普遍使用的C4/WikiText 数据集在领域模型 ((代码、医疗、法律) 上会导致错误决策HumanEval Pass@1 可能下降几百分点.

> **【拓展：量化对 LLM 能力的影响】**量化对不同能力的影响程度不同:(1) 简单聊天/摘要INT4 几乎无影响;(2) 翻译/写作INT4 轻微退化;(3) 数学/推理INT4 损失 3-5 分(MATH benchmark);(4) 长上下文理解INT4 在 128K+ 背景上质量显著下降;(5) 代码生成INT4 在 HumanEval 上下降 2-3 分──核心原则:推理密集型任务应使用 FP8 或 BF16,通用聊天可用INT4──

AWQ và GPTQ yêu cầu một bộ dữ liệu hiệu chuẩn  thường là C4 hoặc WikiText. Đối với các mô hình miền (định luật, y tế, pháp lý), hiệu chuẩn trên văn bản web chung cho phép thuật toán đưa ra quyết định sai về trọng lượng nào để bảo vệ. Pass@1 trên HumanEval có thể giảm một số điểm.

> AWQ và GPTQ 需要校准数据集通常是C4或WikiText──对于领域模型(代码、医疗、法律),在通用网络文本上校准会让算法误决策保护哪些权重──HumanEval Pass@1可能下降几百分点──

Phong cách: chuẩn hóa trên dữ liệu trong miền. Hàng trăm mẫu miền thường là đủ. kiểm tra trên bộ đánh giá trước khi vận chuyển.

> Phương pháp sửa chữa: sử dụng các lĩnh vực trong dữ liệu chuẩn bị.

### Trầm lẫy cache KV

> **【中文解读】**KV Cache 陷:AWQ sẽ tải trọng nén lên 4 bit, nhưng KV Cache là độc lập, giữ ở FP16/FP8。70B AWQ 模型的完整内存预算是:权重35GB + KV Cache(128 并发 × 2K文本) 20GB + 激活 5GB = 总计60GB。朴素地认为"我的模型量化到4GB 已忘记另外30-50GB──必须整体预算HBM。

AWQ giảm trọng lượng xuống còn 4 bit. KV cache là riêng biệt và ở mức FP16/FP8. Đối với mô hình 70B với AWQ:

- trọng lượng: ~ 35 GB (INT4 từ 140 GB).
  Trung ngữ翻译:权重:约 35GB(从140GB的INT4)。
- KV cache ở 128 đồng thời × 2k bối cảnh: ~ 20 GB.
  Trung文翻译:128 并发 × 2K 上下文的 KV 缓存: khoảng 20GB。
- Tích hoạt: ~ 5 GB.
  Trung ngữ翻译:激活: khoảng 5GB.
- Tổng: ~ 60 GB  phù hợp với H100 80 GB.
  Trung文翻译:总计:约60GB适合H100 80GB。

Thần truyền "Tôi đã định lượng mô hình của mình thành 4 GB" quên đi 30 - 50 GB khác.

> 朴素地认为" mô hình của tôi đã được định lượng lên 4GB 了" quên thêm 30-50GB  phải có tổng ngân sách HBM 

Ngoài ra, định lượng cache KV (FP8 KV hoặc INT8 KV) là một lựa chọn khác với sự thỏa hiệp của riêng nó  nó ảnh hưởng trực tiếp đến độ chính xác sự chú ý và không phải là một chiến thắng miễn phí.

> Ngoài ra, KV 缓存量化 ((FP8 KV hoặc INT8 KV) là một lựa chọn độc lập có trọng lượng khác nhau, nó ảnh hưởng trực tiếp đến độ chính xác tập trung, không phải là lợi ích miễn phí.

### AWQ INT4 là nguy hiểm cho lý luận

Dòng tư tưởng, toán học, mã gen với bối cảnh dài  những người này bị ảnh hưởng rõ ràng bởi định lượng tích cực. AWQ INT4 mất ~ 3-5 điểm trên MATH. Đối với tải trọng công việc nặng lý luận, gửi FP8 hoặc BF16; chấp nhận chi phí bộ nhớ.

> Các hệ thống này được kích thích bởi các hệ thống mã hóa.

### 2026 hướng dẫn chọn

- CPU/ Edge serve: GGUF Q4_K_M. Được rồi.
  中文翻译:CPU/边缘服务:GGUF Q4_K_M。
- GPU phục vụ, trò chuyện thường xuyên, không có LoRA.
  Trung文翻译:GPU 服务,通用聊天,无 LoRA:AWQ。
- GPU phục vụ, nhiều LoRA: GPTQ với Marlin.
  中文翻译:GPU 服务,多 LoRA:GPTQ + Marlin。
- Lượng công việc lý luận: FP8.
  Trung文翻译:推理工作负载:FP8──
- Trung tâm dữ liệu Blackwell, chất lượng được xác nhận: NVFP4 + FP8 KV.
  Trung ngữ翻译:Blackwell 数据中心,已验证质量:NVFP4 + FP8 KV。
- Không rõ ràng: chạy một đánh giá 1.000 mẫu trên mỗi định dạng ứng cử viên.
  Trung文翻译:不确定: 在每个候选格式上运行 1,000 样本评估──

## Hãy sử dụng nó để thực hiện
```figure
gpu-memory-breakdown
```

## Sử dụng nó

`code/main.py`tính toán dấu chân bộ nhớ (nâng trọng + KV + kích hoạt) và dung lượng tương đối trên sáu định dạng cho một loạt các kích thước mô hình.

> `code/main.py`计算一系列模型大小在六种格式下内存占用(权重 + KV + 激活) và tương đối吞吐量──展示 KV 缓存在在哪里占主导、权重压缩在哪里划算、FP8 在哪里是安全选择──

## Chuyển nó đi.

> **【拓展：量化选型决策树】**2026 年量化格式选择决策树:(1) CPU/边缘部署 → GGUF Q4_K_M;(2) GPU 通用聊天、无 LoRA → AWQ;(3) GPU 多 LoRA → GPTQ + Marlin;(4) 推理密集型任务 → FP8;(5) Blackwell 数据中心、已验证质量 → NVFP4 + FP8 KV;(6) không chắc → 在候选格式运行1000样本评估;;量化后的验证步骤不可省略每个模型 × 量化格式 × 硬件组合都需要独立验.

Bài học này sẽ mang lại kết quả `outputs/skill-quantization-picker.md`. Với phần cứng, kích thước mô hình, loại tải trọng công việc và dung nạp chất lượng, chọn định dạng và tạo ra kế hoạch hiệu chuẩn/bảo quy.

> 本课产 出 `outputs/skill-quantization-picker.md`❖ Đưa ra các phần cứng, mô hình, tải trọng và dung lượng chất lượng, chọn các hình thức và tạo các quy trình chuẩn bị/thiết lập.

## Tập luyện bài tập

1. Đi chạy`code/main.py`Đối với mô hình 70B ở 128 đồng thời với 2k ngữ cảnh, tính toán tổng HBM cho mỗi định dạng.
   Trung ngữ翻译:运行 `code/main.py`❖ Đối với 128 và phát triển 2K trên mô hình 70B, tính toán tổng HBM của mỗi kiểu hình thức.
2. Bạn có mô hình mã hóa 7B, chọn định dạng và biện minh. Nếu bạn sai về khả năng dung nạp chất lượng, con đường phục hồi là gì?
   Trung ngữ翻译:你有一个7B编码模型――选择一个格式并说明理由―― nếu bạn phán đoán sai về dung lượng chất lượng, đường phục hồi là gì?
3. Xét kích thước bộ dữ liệu hiệu chuẩn cần thiết để hiệu chuẩn AWQ cho mô hình lĩnh vực y tế. Tại sao nhiều dữ liệu không phải lúc nào cũng tốt hơn?
   Trung ngữ翻译:计算医疗领域模型 AWQ 校准所需的数据集大小──为什么更多数据不总是好?
4. Đọc giấy hạt nhân Marlin-AWQ hoặc ghi chú phát hành. Giải thích bằng ba câu tại sao AWQ đạt 741 tok/s trên 7B trong khi GPTQ thô đạt ~712.
   Trung ngữ翻译:阅读 Marlin-AWQ 内核论文或发布说明。用三句话解释为什么AWQ 在 7B 上达到 741 tok/s而原始GPTQ 约712。
5. Khi nào có ý nghĩa để kết hợp trọng lượng AWQ với FP8 KV cache vs giữ KV ở BF16?
   Trung文翻译:何时将 AWQ 权重与 FP8 KV 缓存组合有意义,何时保持 BF16 KV?

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| GGUF | "llama.cpp format" | File format bundling K-quant variants; CPU/edge default |
| Q4_K_M | "Q4 K M" | 4-bit K-quant medium; the production GGUF default |
| GPTQ | "gee pee tee q" | Post-train INT4 with calibration; supports LoRA in vLLM |
| AWQ | "a w q" | Activation-aware INT4; Marlin kernels; best Pass@1 at INT4 |
| Marlin kernels | "fast INT4 kernels" | Custom CUDA kernels for INT4 on Hopper; 10x speedup |
| FP8 | "eight-bit float" | Safe precision default on Hopper/Ada/Blackwell |
| MXFP4 / NVFP4 | "microscaling four" | Blackwell 4-bit FP with per-block scale factors |
| Calibration dataset | "cal data" | Input text used to pick quantization parameters; must match domain |
| KV cache quantization | "KV INT8" | Separate choice from weights; affects attention accuracy |

## Xem thêm 延伸阅读

- [VRLA Tech — LLM Quantization 2026](https://vrlatech.com/llm-quantization-explained-int4-int8-fp8-awq-and-gptq-in-2026/) các chỉ số chuẩn so sánh.
- [Jarvis Labs — vLLM Quantization Complete Guide](https://jarvislabs.ai/blog/vllm-quantization-complete-guide-benchmarks) Số lượng thông qua theo định dạng.
- [PremAI — GGUF vs AWQ vs GPTQ vs bitsandbytes 2026](https://blog.premai.io/llm-quantization-guide-gguf-vs-awq-vs-gptq-vs-bitsandbytes-compared-2026/) chọn định dạng theo định dạng.
- [vLLM docs — Quantization](https://docs.vllm.ai/en/latest/features/quantization/index.html) các định dạng và cờ được hỗ trợ.
- [AWQ paper (arXiv:2306.00978)](https://arxiv.org/abs/2306.00978) Công thức AWQ ban đầu.
- [GPTQ paper (arXiv:2210.17323)](https://arxiv.org/abs/2210.17323) Công thức GPTQ ban đầu.
