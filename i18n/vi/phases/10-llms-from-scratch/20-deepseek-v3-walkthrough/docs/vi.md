# Thiết kế DeepSeek-V3

> Giai đoạn 10 · Bài học 14 đặt tên cho sáu nút kiến trúc mỗi khi mô hình mở quay. DeepSeek-V3 (Từ tháng 12 năm 2024, tổng số tham số 671B, hoạt động 37B) biến tất cả sáu và thêm bốn: Multi-Head Latent Attention, cân bằng tải trọng hỗ trợ không mất, Dự đoán Multi-Token và đào tạo DualPipe. Bài học này đọc kiến trúc của DeepSeek-V3 từ trên xuống dưới và lấy mọi số parameter từ cấu hình được xuất bản. Đến cuối, bạn có thể giải thích tại sao tỷ lệ 671B/37B là cược đúng và tại sao MLA + MoE cùng nhau đánh bại một mình ở biên giới.

> **【中文解读】**DeepSeek-V3(2024年12月,671B 总参数,37B 激活) chuyển tất cả sáu cấu trúc quay并新增四个:MLA(多头潜在注意力) 无辅助损失负载平衡、MTP(多代币 预测) ∆DualPipe 训练──671B/37B tỷ lệ có nghĩa là mỗi lần suy luận chỉ kích hoạt 5,5% các参数──

> **【拓展：DeepSeek架构→开源大模型】**DeepSeek-V3 là một trong những cấu trúc mô hình mở lớn quan trọng nhất trong năm 2024-2025. MLA sẽ nén bộ nhớ cache KV xuống còn 1/10, MoE  để mô hình 671B chỉ tiêu thụ chi phí suy luận 37B.

>  **【前置】**学本节前请先掌握:Phase 10·14(Open Models Architecture) 6 个架构旋概览;Phase 10·15-19 全部(EGLE、Diff Attention、NSA、MTP、DualPipe) DeepSeek-V3 của mỗi sáng tạo.
>  **【类比】**DeepSeek-V3 = "六边形战士"把 2024 年所有前沿优化全堆上:MLA(省 KV cache) ≈ MoE(省推理算力) ≈ MTP(送投机解码) ≈ DualPipe(省训练通信) ≈ NSA(省长上下文算力) ⋅671B 总参数 nhưng chỉ kích hoạt 37B ≈ 5.5%), tương đương với "tạm bọc phong phú của Thụy Sĩ nhưng chỉ sử dụng một cái dao"

**Type:** Learn
**Languages:** Python (stdlib, parameter calculator)
**Prerequisites:** Phase 10 · 14 (open-model walkthroughs), Phase 10 · 17 (NSA), Phase 10 · 18 (MTP), Phase 10 · 19 (DualPipe)
**Time:** ~75 minutes

## Mục tiêu học tập

- Đọc cấu hình DeepSeek-V3 từ trên xuống dưới và giải thích từng trường theo các nút GPT-2 sáu cộng với bốn bổ sung cụ thể cho DeepSeek.
  Từ đầu đến cuối đọc DeepSeek-V3  Configuration, sử dụng 6 vòng quay của GPT-2 cộng với 4 DeepSeek đặc biệt có sáng tạo giải thích cho mỗi đoạn
- Thuộc dẫn tổng số parameter (671B), số parameter hoạt động (37B) và các thành phần đóng góp cho mỗi.
  推导总参数(671B) 、激活参数(37B) và thành phần
- Xét dấu chân cache KV của MLA ở ngữ cảnh 128k và so sánh với mức giá của mô hình dày đặc các param cùng hoạt động với GQA.
  计算 MLA trong 128K 上下文中的 KV 缓存占用, so với tương đương hoạt động tham số GQA 密集模型对比
- Cần nêu tên bốn sáng tạo cụ thể của DeepSeek (MLA, MTP, định tuyến không mất mát phụ trợ, DualPipe) và tên phần nào của cấu trúc/các bộ đào tạo được nhắm mục tiêu.
  Nói ra bốn điều DeepSeek đặc biệt có sáng tạo ((MLA、MTP、无辅助损失路由、DualPipe) và các cấu trúc / tập luyện tập trung

## Vấn đề  vấn đề giới thiệu

DeepSeek-V3 là mô hình mở biên giới đầu tiên mà kiến trúc của nó khác biệt đáng kể với gia đình Llama. Llama 3 405B là "GPT-2 với sáu nút xoay". DeepSeek-V3 là GPT-2 với tất cả sáu nút cộng thêm bốn nút nữa. Đọc cấu hình Llama 3 là một sự nóng lên để đọc cấu hình DeepSeek, nhưng cấu trúc sâu  hình dạng của khối chú ý, logic định tuyến, mục tiêu thời gian đào tạo  là đủ khác nhau để bạn cần một bước đi riêng biệt.

> DeepSeek-V3 là cấu trúc đầu tiên có sự khác biệt về chất lượng với Llama Family. Llama 3 405B là "GPT-2 调六旋" (GPT-2 调六旋) Llama 3 là GPT-2 六旋全调再加四个. Llama 3 được cấu hình như một bộ phận nhiệt, nhưng cấu trúc sâu  tập trung vào hình dạng của khối, hướng dẫn của logic.

Sự thưởng thức của việc học nó: Phiên bản mở của DeepSeek-V3 đã thay đổi ý nghĩa của "capacity biên giới" trong các mô hình mở. Kiến trúc là bản phác thảo mà nhiều khóa đào tạo 2026 đang sao chép.

> Học được lợi ích của nó: Việc phát hành quyền mở của DeepSeek-V3 đã thay đổi ý nghĩa của mô hình "capacity tiền tuyến" mở.

## Khái niệm cốt lõi

> **【中文解读】**DeepSeek-V3 là một trong những mô hình nguồn mở có ảnh hưởng nhất năm 2024: 671B 总参数(37B 激活参数) của MoE 架构, sử dụng MLA(多头潜在注意力) 压缩 KV-cache, sử dụng DualPipe 优化流水线并行, với chi phí đào tạo khoảng 560 triệu USD đạt hiệu suất cấp GPT-4.

> **【拓展：DeepSeek-V3 的经济性突破】**Giá đào tạo của DeepSeek-V3 chỉ khoảng 560 triệu USD [27,788M H800 GPU 小时), khoảng 1/18 của Llama 3 405B  giá đào tạo.


### Lòng lõi không thay đổi, một lần nữa

DeepSeek-V3 vẫn tự lập. Nó vẫn xếp chồng các khối decoder. Mỗi khối vẫn có sự chú ý cộng với MLP cộng với hai RMSNorms. Nó vẫn sử dụng SwiGLU trong MLP. Nó vẫn sử dụng RoPE. Pre-norm. Cài đặt gắn trọng lượng. cùng một đường cơ sở như mọi Llama hoặc Mistral.

### Sự xoay quanh: MLA thay vì GQA

Từ giai đoạn 10 · 14 bạn biết GQA thu hẹp bộ nhớ cache KV bằng cách chia sẻ K và V trên các nhóm đầu Q. Sự chú ý tiềm ẩn đa đầu (MLA) đi xa hơn: K và V được nén thành một đại diện tiềm ẩn cấp thấp được chia sẻ (the `kv_lora_rank`KV cache chỉ lưu trữ ẩn  thường là 512 floats per token per layer, không phải 8 x 128 = 1024 floats.

Trong bối cảnh 128k, DeepSeek-V3 với MLA (một shared latent `c^{KV}`mỗi token mỗi lớp; K và V đều được dẫn từ tiềm ẩn này thông qua các dự đoán lên mà có thể được hấp thụ vào matmul tiếp theo):

```
kv_cache = num_layers * kv_lora_rank * max_seq_len * bytes_per_element
         = 61 * 512 * 131072 * 2
         = 7.6 GB
```

Một đường cơ sở GQA giả định (Llama 3 hình 70B, 8 đầu KV, đầu mờ 128) sẽ trả:

```
kv_cache = 2 * 61 * 8 * 128 * 131072 * 2
         = 30.5 GB
```

MLA nhỏ hơn 4 lần so với bộ nhớ cache GQA kiểu Llama-3-70B ở ngữ cảnh 128k.

Sự thỏa hiệp: MLA thêm một bước giảm nén mỗi tính toán chú ý (trên đầu).

### Đường dẫn: cân bằng tải phụ trợ không mất mát

Các bộ định tuyến MoE quyết định các chuyên gia top-k xử lý mỗi token. Một router ngây thơ tập trung quá nhiều công việc vào một vài chuyên gia, để lại những chuyên gia khác vô hiệu.

DeepSeek-V3 giới thiệu một chương trình hỗ trợ không mất mát. Các thuật ngữ thiên vị cho mỗi chuyên gia được thêm vào các logit router, được điều chỉnh trong quá trình đào tạo bằng một quy tắc đơn giản: nếu chuyên gia `e`quá tải, giảm `bias_e`Nếu bị tải quá mức, tăng nó. Không mất thêm thời gian.

Ảnh hưởng đến lỗ hổng chính: không có thể đo lường. Ảnh hưởng đến kiến trúc MoE: sạch hơn, không có siêu tham số lỗ phụ giúp để điều chỉnh.

### MTP: đào tạo dày đặc hơn + draft miễn phí

Từ giai đoạn 10 · 18 bạn biết DeepSeek-V3 thêm mô-đun D=1 MTP dự đoán mã thông báo hai vị trí phía trước.

Các tham số: 14B trên đầu của 671B chính.

### Việc đào tạo: DualPipe

Từ giai đoạn 10 · 19 bạn biết DualPipe là một đường ống dẫn hai chiều chồng chéo về phía trước và phía sau với các đoạn truyền thông toàn bộ qua nút.

### Các cấu hình, trường theo trường

Đây là cấu hình DeepSeek-V3 (đơn giản):

```
hidden_size: 7168
intermediate_size: 18432   (dense MLP hidden size, used on first few layers)
moe_intermediate_size: 2048 (expert MLP hidden size)
num_hidden_layers: 61
first_k_dense_layers: 3    (first 3 layers use dense MLP)
num_attention_heads: 128
num_key_value_heads: 128   (formally equal to num_heads under MLA, but
                           the real compression is in kv_lora_rank)
kv_lora_rank: 512          (MLA latent dimension)
num_experts: 256            (MoE expert count per block)
num_experts_per_tok: 8      (top-8 routing)
shared_experts: 1           (always-on shared expert per block)
max_position_embeddings: 163840
rope_theta: 10000.0
vocab_size: 129280
mtp_module: 1               (1 MTP module at depth 1)
```

Hãy phân tích nó:

- `hidden_size=7168`: kích thước nhúng.
- `num_hidden_layers=61`: độ sâu khối tổng thể.
- `first_k_dense_layers=3`Các khối đầu tiên 3 sử dụng một MLP dày đặc kích thước 18432.
- `num_attention_heads=128`: 128 đầu truy vấn.
- `kv_lora_rank=512`: K và V được nén đến chiều kích ẩn này và bị nén mỗi đầu.
- `num_experts=256, num_experts_per_tok=8`Mỗi khối của Bộ Ngoại giao có 256 chuyên gia, các tuyến đường đứng đầu 8.
- `shared_experts=1`: trên đỉnh 256 chuyên gia đã được hướng dẫn, 1 chuyên gia luôn đóng góp cho mỗi token. Hãy nghĩ về nó như một "màn bằng dày đặc" đảm bảo mỗi token nhận được một cái gì đó đáng tin cậy.
- `moe_intermediate_size=2048`: kích thước ẩn của MLP của mỗi chuyên gia.

### Tài khoản tham số

Việc tính toán đầy đủ là trong `code/main.py`- Tiêu đề:

- Đêm: `vocab * hidden = 129280 * 7168 = ~0.93B`- Tôi không biết.
- 3 khối mật đầu tiên: chú ý với MLA (~144M mỗi khối) + MLP mật (~260M mỗi khối) + chuẩn mực.
- 58 khối MoE: sự chú ý với MLA (~144M) + 256 chuyên gia mỗi (30M mỗi) + 1 chuyên gia chia sẻ (30M) + chuẩn. Tổng cộng ~ 7.95B mỗi khối, bao gồm tất cả các chuyên gia.
- Module MTP: 14B.

Tổng cộng: ~476B cho kiến trúc cốt lõi + 14B MTP + rõ ràng số 671B được công bố chiếm các tham số cấu trúc bổ sung (những tensor thiên vị, các thành phần chuyên gia cụ thể, quy mô chuyên gia chia sẻ, vv). Số lượng chúng tôi tái tạo trong máy tính tính là trong vòng 3-5% của công bố  delta đến từ tài liệu báo cáo kế toán tinh tế của DeepSeek trong phần 2 phụ lục của nó.

Các tham số hoạt động cho mỗi forward:

- Lưu ý: 144M mỗi lớp * 61 = 8,8B (tất cả các lớp cháy).
- MLP hoạt động: 3 lớp đầu tiên dày đặc (3 * 260M = 780M), 58 lớp MoE mỗi lớp hoạt động với 8 đường + 1 chia sẻ + đường trên.
- Đáp nhập + chuẩn: 1.2B.
- Tổng hoạt động: khoảng 26B lõi + 14B MTP (được đào tạo nhưng không phải lúc nào cũng chạy theo suy luận) ≈ 37B.

### Tỷ lệ 671B / 37B

Hình ảnh này được xem là một trong những hình ảnh ảnh ảnh ảnh ảnh ảnh ảnh ảnh ảnh ảnh ảnh hưởng đến sự phát triển của các máy tính.

### Đâu DeepSeek-V3 ngồi

| Model | Total | Active | Ratio | Attention | Novel ideas |
|-------|------|-------|-------|-----------|-------------|
| Llama 3 70B | 70B | 70B | 100% | GQA 64/8 | — |
| Llama 4 Maverick | 400B | 17B | 4.25% | GQA | — |
| Mixtral 8x22B | 141B | 39B | 27% | GQA | — |
| DeepSeek V3 | 671B | 37B | 5.5% | MLA 512 | MLA + MTP + aux-free + DualPipe |
| Qwen 2.5 72B | 72B | 72B | 100% | GQA 64/8 | YaRN extension |

### Tiếp theo: R1, V4

DeepSeek-R1 (2025) là một cuộc chạy đào tạo lý luận trên xương sống V3. R1 sử dụng cùng một kiến trúc. Điều thay đổi là công thức sau đào tạo (RL quy mô lớn trên các nhiệm vụ có thể xác minh), chứ không phải kiến trúc trước đào tạo.

DeepSeek-V4 (nếu nó được xuất khẩu) dự kiến sẽ giữ MLA + MoE + MTP và thêm DSA (DeepSeek Sparse Attention), người kế nhiệm NSA từ giai đoạn 10 · 17.


> **【拓展：DeepSeek-V3 的 MoE 架构细节】**DeepSeek-V3 có 256 chuyên gia, mỗi lần kích hoạt 8 个(加 1 共享专家) ⋅671B 总参数 nhưng chỉ kích hoạt khoảng 37B, lượng tính toán chỉ khoảng 5,5%。


## Hãy sử dụng nó để thực hiện
```figure
moe-routing
```

## Sử dụng nó

`code/main.py`là máy tính tính tham số chuyên về hình dạng của DeepSeek-V3. chạy nó, so sánh đầu ra của nó với số của giấy, và sử dụng nó trên các biến thể giả thuyết (256 chuyên gia so với 512, top-8 so với top-16, MLA xếp hạng 512 so với 1024).

Những gì cần xem:

- Tổng số lượng tham số so với 671B được công bố.
- Số lượng tham số hoạt động so với công bố 37B.
- KV cache ở ngữ cảnh 128k  so sánh MLA vs GQA.
- Phân tích từng lớp để xem ngân sách tham số thực sự đi đâu.

## Chuyển nó đi.

Bài học này sẽ mang lại kết quả `outputs/skill-deepseek-v3-reader.md`. Với một mô hình gia đình DeepSeek (V3, R1 hoặc bất kỳ biến thể nào trong tương lai), nó tạo ra một kiến trúc đọc thành phần theo thành phần cho tên mỗi lĩnh vực của cấu hình, lấy số lượng tham số theo thành phần, và xác định được mô hình sử dụng những sáng tạo cụ thể của DeepSeek.

> 本课产 出 `outputs/skill-deepseek-v3-reader.md`△ được định định DeepSeek 系列模型 ((V3、R1 或任何未来变体), nó tạo ra cấu trúc giải thích từng bộ phận, đặt tên cho mỗi phần cấu trúc, theo số lượng các bộ phận,并识别模型 sử dụng bốn DeepSeek 特定创新中的哪些──

## Tập luyện bài tập

1. Đi chạy`code/main.py`- So sánh ước tính số tham số tổng của máy tính tính với 671B và xác định nơi delta đến.
   Trung ngữ翻译:运行 `code/main.py`                                                                                                                                                                                                                                                              

2. Thay đổi cấu hình để sử dụng MLA xếp hạng 256 thay vì 512. Xét kích thước cache KV kết quả tại ngữ cảnh 128k.
   Trung ngữ翻译: sửa đổi cấu hình sử dụng MLA 秩 256 thay vì 512──计算 128K 上下文下 KV 缓存大小──省了多少百分比,代价是什么?

3. So sánh DeepSeek-V3 (256 chuyên gia, top-8) định tuyến với một biến thể giả thuyết (512 chuyên gia, top-8). Tổng tham số tăng lên; tham số hoạt động vẫn giống nhau.
   Trung ngữ翻译:比较 DeepSeek-V3 的(256 专家,top-8)路由与假设的(512 专家,top-8)变体──总参数增长;激活参数不变──额外专家容量理论上买到了什么,推理时代价是什么?

4. Đọc Phần 2.1 của báo cáo kỹ thuật DeepSeek-V3 (arXiv:2412.19437) về MLA. Giải thích bằng ba câu tại sao các matrices decompression K và V có thể được "thấm" vào matmul sau đó để hiệu quả thời gian suy luận.
   Trung ngữ翻译:阅读DeepSeek-V3 技术报告第 2.1 节关于MLA的内容.

5. DeepSeek-V3 sử dụng đào tạo FP8 cho hầu hết các hoạt động. Xét tiết kiệm bộ nhớ của FP8 so với BF16 để lưu trữ trọng lượng 671B. Điều này giao nhau như thế nào với ngân sách đào tạo token 14.8T?

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|------------------------|---------|
| MLA | "Multi-Head Latent Attention" | Compress K and V into a shared low-rank latent (kv_lora_rank, typically 512), decompress per head on-the-fly; KV cache stores only the latent | 多头潜在注意力，将 K/V 压缩为共享低秩潜在向量 |
| kv_lora_rank | "MLA compression dim" | The size of the shared latent for K and V; DeepSeek-V3 uses 512 | MLA 压缩维度，DeepSeek-V3 使用 512 |
| First k dense layers | "Early layers stay dense" | The first few MoE-model layers skip the MoE router and run a dense MLP for stability | 前 k 层保持密集，跳过 MoE 路由保证稳定性 |
| num_experts_per_tok | "Top-k routing" | How many routed experts fire per token; DeepSeek-V3 uses 8 | 每 token 激活专家数，DeepSeek-V3 使用 8 |
| Shared experts | "Always-on experts" | Experts that process every token regardless of routing; DeepSeek-V3 uses 1 | 共享专家，每个 token 都经过的专家 |
| Auxiliary-loss-free routing | "Bias-adjusted load balance" | Per-expert bias terms adjusted during training to keep expert load balanced without adding a loss term | 无辅助损失路由，用偏置项替代辅助损失做负载均衡 |
| MTP module | "Extra prediction head" | Transformer block predicting t+2 from h^(1) and E(t+1); denser training, free speculative-decoding draft | MTP 模块，多 token 预测头 |
| DualPipe | "Bidirectional pipeline" | Training schedule that overlaps forward/backward compute with cross-node all-to-all | DualPipe，双向流水线调度 |
| Active parameter ratio | "Sparsity" | active_params / total_params; DeepSeek-V3 hits 5.5% | 激活参数比，DeepSeek-V3 仅 5.5% |
| FP8 training | "8-bit training" | Training storage and many compute ops in FP8; roughly halves memory vs BF16 at a small quality cost | FP8 训练，8 位训练节省约一半显存 |

## Xem thêm 延伸阅读

- [DeepSeek-AI — DeepSeek-V3 Technical Report (arXiv:2412.19437)](https://arxiv.org/abs/2412.19437) tài liệu kiến trúc, đào tạo và kết quả đầy đủ
- [DeepSeek-V3 model card on Hugging Face](https://huggingface.co/deepseek-ai/DeepSeek-V3) config file và các ghi chú triển khai
- [DeepSeek-V2 paper (arXiv:2405.04434)](https://arxiv.org/abs/2405.04434) người tiền nhiệm đã giới thiệu MLA
- [DeepSeek-R1 paper (arXiv:2501.12948)](https://arxiv.org/abs/2501.12948) kế thừa đào tạo lý luận về kiến trúc của V3
- [Native Sparse Attention (arXiv:2502.11089)](https://arxiv.org/abs/2502.11089) hướng tương lai cho sự chú ý của gia đình DeepSeek
- [DualPipe repository](https://github.com/deepseek-ai/DualPipe) tham chiếu lịch trình đào tạo
