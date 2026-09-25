# Sự kết hợp của các chuyên gia (MoE) 混合专家模型 (MoE)

> Một biến thể 70B dày đặc kích hoạt mọi tham số cho mỗi token. một 671B MoE kích hoạt chỉ 37B cho mỗi token và đánh bại nó trên mọi điểm chuẩn. Sparsity là ý tưởng quy mô quan trọng nhất của thập kỷ.

> **【中文解读】**MoE chỉ kích hoạt một phần chuyên gia mạng xử lý mỗi token, tăng đáng kể số lượng không tăng lượng tính toán.

**Type:** Hands-on | **类型:** 动手
**Language:**Python**语言:**Python
**Prerequisites:** Phase 7 · 05 (Full Transformer), Phase 7 · 07 (GPT) | **前置知识:** Phase 7 · 05 (Full Transformer), Phase 7 · 07 (GPT)
**Time:** ~45 minutes | **时间:** ~45 分钟

## Vấn đề  vấn đề giới thiệu

FLOPs của một biến thể dày đặc khi suy luận bằng số parameter của nó (nói 2 cho chuyển tiếp phía trước). Scale lên một mô hình dày đặc và mỗi token trả phí đầy đủ. Đến năm 2024 biên giới đã đâm vào một bức tường tính toán: để có ý nghĩa thông minh hơn, bạn cần tăng trưởng theo tỉ lệ tăng FLOPs cho mỗi token.

> 密 biến đổi 推理时的FLOPs等于其参数(前向传播乘以2);;扩大密模型意味着每个代币都必须支付全部代价;; đến năm 2024, các mô hình tiền tuyến đã gặp phải bức tường tính toán: để trở nên thông minh hơn, cần tăng trưởng chỉ số FLOPs của mỗi token;;

Sự kết hợp của các chuyên gia phá vỡ mối liên kết này.`E`các chuyên gia độc lập + một bộ định tuyến chọn `k`Các chuyên gia cho mỗi token.`E × FFN_size`. Các tham số hoạt động cho mỗi token = `k × FFN_size`. Tự cấu hình điển hình năm 2026: `E=256`- `k=8`. Scales lưu trữ với `E`, tính toán các quy mô với `k`- Tôi không biết.

> 混合专家模型打破了这个联系.`E`个独立专家 + 一个路由器, mỗi token 选择 `k`个专家──总参数 = `E × FFN_size`◊ Số lượng active参数 của mỗi token = `k × FFN_size`❖ Tương tự của 2026:`E=256``k=8`❖ Kho lưu trữ`E`扩展,计算随`k`扩展──

Biên giới 2026 gần như hoàn toàn là MoE: DeepSeek-V3 (671B tổng / 37B hoạt động), Mixtral 8×22B, Qwen2.5-MoE, Llama 4, Kimi K2, gpt-oss.

> 2026 năm của tiền tuyến gần như hoàn toàn là MoE:DeepSeek-V3(671B 总参数 / 37B 活跃) ✓ Mích 8×22B、Qwen2.5-MoE、Llama 4、Kimi K2、gpt-oss── trên danh sách xếp hạng độc lập của Phân tích Kỹ thuật,排名前 10 của các mô hình nguồn mở là MoE──

> **【中文解读】**MoE đã phá vỡ phương trình "参数 = 计算量" ⋅ mỗi FFN 层 được thay thế thành E 个独立专家 + 路由器, mỗi token chỉ kích hoạt k 个专家。 tổng参数 theo E 增长, nhưng mỗi token 计算量 chỉ theo k 增长── điển hình cấu hình E=256, k=8, lưu trữ theo E 缩缩, tính toán theo k 缩缩── đây là một trong những suy nghĩ mở rộng quan trọng nhất của thập niên 2020──

> **【拓展：DeepSeek-V3 的 MoE 创新】**DeepSeek-V3  sở hữu 671B  tổng số nhưng mỗi token chỉ kích hoạt 37B thông qua 256 chuyên gia đường + 1 chuyên gia chia sẻ thực hiện. Nó cũng đưa ra chiến lược cân bằng tải không liên quan đến mất tích hỗ trợ, tránh được vấn đề sụp đổ đường truyền thống của MoE.

## Khái niệm cốt lõi

![MoE layer: router selects k of E experts per token](../assets/moe.svg)

### Việc trao đổi FFN

Phong chuyển đổi dày đặc:

> 密 Transformer 块:

```
h = x + attn(norm(x))
h = h + FFN(norm(h))
```

Phòng MoE:

```
h = x + attn(norm(x))
scores = router(norm(h))              # (N_tokens, E)
top_k = argmax_k(scores)              # pick k of E per token
h = h + sum_{e in top_k}(
        gate(scores[e]) * Expert_e(norm(h))
    )
```

Mỗi chuyên gia là một FFN độc lập (thường là SwiGLU).`k`chuyên gia và có được một hỗn hợp được khóa ra của sản phẩm của họ.

> Mỗi chuyên gia là một FFN độc lập (thường là SwiGLU)  Các router là một tầng đơn tuyến  Mỗi token  chọn riêng `k`个专家, nhận được chúng xuất khẩu

### Vấn đề cân bằng tải

Nếu router đưa 90% mã thông qua Expert 3, các chuyên gia khác chết đói.

> Nếu router sẽ phân phối 90% mã thông báo cho chuyên gia 3, các chuyên gia khác sẽ "nạn đói"

1. **Auxiliary load-balancing loss**(Switch Transformer, Mixtral). Thêm một hình phạt tương xứng với sự khác biệt trong việc sử dụng chuyên gia.
   Trung ngữ翻译:**辅助负载均衡损失**(Switch Transformer、Mixtral)  thêm với các chuyên gia sử dụng tỷ lệ khác biệt của hình phạt──有效, nhưng tăng siêu参数 và tín hiệu cấp hai──
2. **Expert capacity + token dropping**(Switch sớm). Mỗi chuyên gia quá trình tối đa`C × N/E`token; token quá tải bỏ qua lớp.
   Trung ngữ翻译:**专家容量 + token 丢弃**(早期 Switch) ✿ Mỗi chuyên gia nhất xử lý `C × N/E`个 token;溢出的 token 跳过这个层――损害质量――
3. **Auxiliary-loss-free balancing**(DeepSeek-V3). Thêm một sự thiên vị được học theo chuyên gia thay đổi lựa chọn top-k của router. Bias được cập nhật bên ngoài sự mất tập. Không có hình phạt về mục tiêu chính.
   Trung ngữ翻译:**辅助损失无关均衡**(DeepSeek-V3)。 thêm một học tập để được phân biệt, điều chỉnh các lựa chọn trên đường bộ─k │偏置在训练损失之外更新──不对主目标施加惩罚──2024年重大突破──

Phương pháp của DeepSeek-V3: sau mỗi bước đào tạo, cho mỗi chuyên gia, kiểm tra xem việc sử dụng nó có trên hoặc dưới mục tiêu.`±γ`. Sử dụng lựa chọn `scores + bias`Các xác suất chuyên gia được sử dụng để gài là nguyên liệu`scores`Không thay đổi.

> Phương pháp DeepSeek-V3: Sau mỗi bước tập luyện, mỗi chuyên gia kiểm tra liệu sử dụng của nó có cao hơn hoặc thấp hơn mục tiêu không.`±γ`△ chọn sử dụng `scores + bias` Tỷ lệ chuyên gia được sử dụng để kiểm soát là nguyên thủy không thay đổi`scores`将路由与表达解──

### Các chuyên gia chung

DeepSeek-V2/V3 cũng chia các chuyên gia thành *shared* và *routed*. Mỗi token đi qua tất cả các chuyên gia được chia sẻ. Các chuyên gia được chia sẻ được chọn qua top-k. Các chuyên gia được chia sẻ nắm bắt kiến thức chung; các chuyên gia được chia sẻ chuyên môn. V3 chạy 1 chuyên gia được chia sẻ cộng với top-8 trong 256 người được định tuyến.

> DeepSeek-V2/V3 cũng sẽ phân chia chuyên gia thành 2 loại: * chia sẻ* và * đường *. Mỗi token đều thông qua tất cả các chuyên gia chia sẻ.

### Các chuyên gia hạt mỏng

Classic MoE (GShard, Switch): mỗi chuyên gia rộng như một FFN đầy đủ. `E`là nhỏ (864), `k`là nhỏ (12).

> 经典 MoE(GShard、Switch): Mỗi chuyên gia với FFN hoàn chỉnh 一样宽──`E`较小(8-64),`k`较小(1-2)。

MoE hạt mỏng hiện đại (DeepSeek-V3, Qwen-MoE): mỗi chuyên gia nhỏ hơn (1/8 kích thước FFN). `E`là lớn (256+), `k`là lớn hơn (8+). cùng số tham số tổng thể, nhưng kết hợp quy mô nhanh hơn nhiều. `C(256, 8) = 400 trillion`có thể có "người chuyên gia" cho mỗi token chất lượng tăng lên, độ trễ vẫn ổn định.

> 现代细粒度 MoE(DeepSeek-V3、Qwen-MoE): mỗi chuyên gia hơn ngắn hơn(1/8 FFN 大小)`E`较大(256+),`k`Cũng hơn ((8+) ✿总参数 giống nhau, nhưng组合增长更快──`C(256, 8) = 400 万亿`种可能的"专家"组合──质量提升,延迟不变──

> **【拓展：MoE 的路由崩塌问题】**Thách thức cốt lõi trong đào tạo MoE là: đường dẫn sụp đổ (đã sụp đổ của router) 路由器可能将大部分代币分配给少数专家,导致其他专家不到训练.

### Tương tự chi phí

Mỗi token, mỗi lớp:

> Mỗi token, mỗi tầng:

| Config | Active params / token | Total params |
|--------|-----------------------|--------------|
| 配置 | 每个 token 活跃参数 | 总参数量 |
| Mixtral 8×22B | ~39B | 141B |
| Llama 3 70B (dense) | 70B | 70B |
| DeepSeek-V3 | 37B | 671B |
| Kimi K2 (MoE) | ~32B | 1T |

DeepSeek-V3 đánh bại Llama 3 70B (thấp) trên hầu hết mọi điểm chuẩn trong khi làm **fewer active FLOPs per token**. nhiều tham số hơn = nhiều kiến thức hơn. FLOP hoạt động hơn = nhiều tính toán hơn cho mỗi token. MoE tách chúng ra.

> DeepSeek-V3 đã đánh bại Llama 3 70B trong hầu hết các thử nghiệm chuẩn bị, đồng thời**每个 token 的活跃 FLOPs 更少**△更多参数 = 更多知识──更多活跃 FLOPs = Mỗi token 更多计算──MoE 将两者解──

### Lòng nhớ

Tất cả các chuyên gia sống trên GPU bất kể người nào bắn. Một mô hình 671B cần ~ 1.3 TB VRAM cho trọng lượng fp16. Việc triển khai MoE biên giới đòi hỏi sự song song chuyên gia  các chuyên gia phân mảnh trên GPU, đường dẫn token trên mạng.

> Tất cả các chuyên gia bất kể hoạt động hay không đều ở trên GPU. Một mô hình 671B cần khoảng 1.3TB của fp16 权重显存.

> **【中文解读】**Mức cân trọng tâm của MoE: sử dụng bộ nhớ thay đổi tính toán. DeepSeek-V3 với 37B  active parameter đạt được hiệu suất trên 70B 密 mô hình, nhưng cần 1.3TB 显存储所有专家.

> **【拓展：细粒度专家 vs 粗粒度专家】**传统 MoE(Switch Transformer) sử dụng một số ít chuyên gia lớn(E=8-64)。现代细粒度 MoE(DeepSeek-V3) sử dụng một số lượng lớn chuyên gia nhỏ(E=256+), mỗi chuyên gia chỉ có 1/8 FFN 宽度──组合数 C(256,8) 约为40000000000种,远超粗粒度的组合空间──质量提升显著,延迟基本不变──

## Hãy xây dựng nó.
```figure
expert-routing
```

## Hãy xây dựng nó

Nhìn xem`code/main.py`Một lớp MoE nhỏ gọn trong chất xơ tinh khiết với:

> 参见 `code/main.py`Một tầng quan trọng của việc thực hiện các tiêu chuẩn đơn giản, bao gồm:

- `n_experts=8`Các chuyên gia SwiGLU (mỗi người đều có một hình tuyến tính, ví dụ)
  Trung ngữ翻译:`n_experts=8`个类 SwiGLU 专家( mỗi một条线性层, dùng để biểu diễn)
- top-k=2 định tuyến
  Trung文翻译:top-k=2 路由
- trọng lượng cửa được chuẩn hóa với độ mềm tối đa
  Trung文翻译:softmax 归一化门控权重
- cân bằng không mất mát phụ trợ thông qua sự thiên vị của mỗi chuyên gia
  Trung文翻译: qua từng chuyên gia định vị để thực hiện hỗ trợ mất không liên quan cân bằng

### Bước 1: bộ định tuyến

```python
def route(hidden, W_router, top_k, bias):
    scores = [sum(h * w for h, w in zip(hidden, W_router[e])) for e in range(len(W_router))]
    biased = [s + b for s, b in zip(scores, bias)]
    top_idx = sorted(range(len(biased)), key=lambda i: -biased[i])[:top_k]
    # softmax over ORIGINAL scores of the chosen experts
    chosen = [scores[i] for i in top_idx]
    m = max(chosen)
    exps = [math.exp(c - m) for c in chosen]
    s = sum(exps)
    gates = [e / s for e in exps]
    return top_idx, gates
```

Bias ảnh hưởng đến sự lựa chọn, không phải trọng lượng cổng. Đó là thủ thuật DeepSeek-V3  Bias sửa chữa mất cân bằng tải mà không điều khiển dự đoán của mô hình.

> 偏置影响选择,不影响门控制权重―― đây là kỹ thuật của DeepSeek-V3 偏置纠正负载不平衡, nhưng không干预模型的预测――

### Bước 2: chạy 100 token qua bộ định tuyến

Theo dõi các chuyên gia bắn bao nhiêu lần.`-γ`cho các chuyên gia sử dụng quá mức, `+γ`cho sử dụng chưa được sử dụng), sử dụng hội tụ đến phân phối đồng nhất trong một vài lần lặp lại.

> Theo dõi những chuyên gia được kích hoạt nhiều lần không có sự chuyển nhượng, sử dụng không bình đẳng.`-γ`, sử dụng thiếu chuyên gia `+γ`), sử dụng số lượng trong vài lần 代 sau nhận đến phân phối trung bình.

### Bước 3: So sánh số param

Bác "đồng độ mật độ" của cấu hình MoE. DeepSeek-V3-shaped: 256 routed + 1 shared, 8 active, d_model=7168.

> 印 MoE 配置的"密等价"──DeepSeek-V3 形状:256 个路由 + 1 个共享,8 个活跃,d_model=7168──总参数令人惊叹──活跃参数数只有密 Llama 3 70B 的七分之一──

## Hãy sử dụng nó để thực hiện

HuggingFace Loading:

> Nhấp mặt

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
model = AutoModelForCausalLM.from_pretrained("mistralai/Mixtral-8x22B-v0.1")
```

2026 kết luận sản xuất: vLLM hỗ trợ định tuyến MoE theo bản địa. SGLang có con đường đồng bộ chuyên gia nhanh nhất. Cả hai đều tự động xử lý lựa chọn top-k và đồng bộ chuyên gia.

> 2026 năm sản xuất: vLLM 原生支持 MoE 路由──SGLang 拥有最快专家并行路径──两者都自动处理顶级k 选择和专家并行──

**When to pick MoE:**
- Bạn muốn chất lượng hàng rào với chi phí suy luận thấp hơn cho mỗi token.
  Trung ngữ翻译:你想以低的每代币 推理成本获得前沿质量──
- Bạn có cơ sở hạ tầng VRAM / chuyên gia song song.
  Trung ngữ翻译:你有足够的显存/专家并行基础设施──
- Nhiệm vụ công việc của bạn là token-heavy (chat, code) không có ngữ cảnh-heavy (doc dài).
  Trung ngữ翻译:你的工作负载是标志密集型(聊天、代码) 而不是上下文密集型(长文档)。

**When NOT to pick MoE:**
- Việc triển khai cạnh  bạn trả tiền cho lưu trữ đầy đủ cho bất kỳ FLOP hoạt động nào.
  Trung ngữ翻译:边缘部署你要为任何活跃FLOP支付全部储备──
- Lạt-chẩn đoán một người dùng phục vụ  chuyên gia định tuyến thêm chi phí chung.
  Trung ngữ翻译:延迟敏感的单用户服务专家路由增加开销。
- Các mô hình nhỏ (<7B)  Lợi thế chất lượng của MoE chỉ xuất hiện trên ngưỡng tính toán (~ 6B các tham số hoạt động).
  Trung文翻译:小模型(<7B) MoE's质量优势只在计算值以上(约6B 活跃参数)才会出现──

## Chuyển nó đi.

Nhìn xem`outputs/skill-moe-configurator.md`. Kỹ năng chọn E, k, và chia sẻ chuyên gia bố cục cho một bộ phận mới của Bộ cho tham số ngân sách, mã thông báo đào tạo và mục tiêu triển khai.

> 参见 `outputs/skill-moe-configurator.md` Kỹ năng này 根据参数预算、训练代号 数和部署目标,为新MOE 选择 E、k 和共享专家布局──

## Tập luyện bài tập

1. **Easy.**Đi chạy`code/main.py`Xem cách cập nhật thiên vị không mất tích phụ giúp như thế nào để đồng hóa việc sử dụng chuyên gia trên 50 lần lặp lại.
   Trung ngữ翻译:运行 `code/main.py`❖ quan sát trợ giúp mất mát không liên quan thay đổi làm thế nào để sử dụng trong 50 lần 代 cân bằng chuyên gia
2. **Medium.**Thay thế bộ định tuyến được học bằng một bộ định tuyến dựa trên hash (định nghĩa, không học). So sánh chất lượng và cân bằng. Tại sao bộ định tuyến được học tốt hơn?
   Trung ngữ翻译: dùng các bộ máy học dựa trên Hash để thay thế các bộ máy học theo Hash (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach) (Hach)
3. **Hard.**Thực hiện "chế độ phân phối phù hợp" theo kiểu GRPO (truc DeepSeek-V3.2): ghi lại các chuyên gia bắn trong quá trình suy luận, buộc cùng một định tuyến trong quá trình tính toán gradient. Đo hiệu ứng trên thiết lập chính sách đồ chơi-gradient.
   Trung ngữ翻译:实现GRPO 风格的"推演匹配路由" (DeepSeek-V3.2 技巧): ghi lại khi các chuyên gia được kích hoạt, trong khi tính toán thang, bắt buộc cùng một đường.

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Expert | "One FFN among many" | An independent feed-forward network; parameters dedicated to a sparse slice of the FFN computation. |
| 专家 | "众多 FFN 之一" | 独立的前馈网络；专用于 FFN 计算的稀疏切片的参数。 |
| Router | "The gate" | A tiny linear layer that scores each token against each expert; top-k selection. |
| 路由器 | "门控" | 一个小线性层，对每个 token 与每个专家打分；top-k 选择。 |
| Top-k routing | "k active experts per token" | Each token's FFN computation goes through exactly k experts, weighted by gate. |
| Top-k 路由 | "每个 token 激活 k 个专家" | 每个 token 的 FFN 计算经过恰好 k 个专家，按门控加权。 |
| Auxiliary loss | "Load-balance penalty" | Extra loss term that penalizes skewed expert usage. |
| 辅助损失 | "负载均衡惩罚" | 惩罚专家使用不均衡的额外损失项。 |
| Auxiliary-loss-free | "DeepSeek-V3's trick" | Balance via per-expert bias on the router's selection only; no extra gradient. |
| 辅助损失无关 | "DeepSeek-V3 的技巧" | 仅通过路由器选择上的逐专家偏置实现均衡；无额外梯度。 |
| Shared expert | "Always on" | Extra expert through which every token passes; captures common knowledge. |
| 共享专家 | "始终开启" | 每个 token 都通过的额外专家；捕获通用知识。 |
| Expert parallelism | "Shard by expert" | Distribute different experts to different GPUs; route tokens across the network. |
| 专家并行 | "按专家分片" | 将不同专家分配到不同 GPU；通过网络路由 token。 |
| Sparsity | "Active params < total params" | The ratio `k × expert_size / (E × expert_size)`; 37/671 ≈ 5.5% for DeepSeek-V3. |
| 稀疏性 | "活跃参数 < 总参数" | 比率 `k × expert_size / (E × expert_size)`；DeepSeek-V3 为 37/671 ≈ 5.5%。 |

## Xem thêm 延伸阅读

- [Shazeer et al. (2017). Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer](https://arxiv.org/abs/1701.06538) ý tưởng.
  Trung ngữ翻译:MoE 的原始论文──
- [Fedus, Zoph, Shazeer (2022). Switch Transformer: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity](https://arxiv.org/abs/2101.03961) Switch, MoE cổ điển.
  Trung ngữ翻译:Switch Transformer,经典的MoE论文。
- [Jiang et al. (2024). Mixtral of Experts](https://arxiv.org/abs/2401.04088) Mixtral 8×7B.
  中文翻译:Xơ 8×7B 论文。
- [DeepSeek-AI (2024). DeepSeek-V3 Technical Report](https://arxiv.org/abs/2412.19437) MLA + MoE không mất mát hỗ trợ + MTP.
  Trung文翻译:DeepSeek-V3 技术报告,MLA + 辅助损失无关 MoE + MTP。
- [Wang et al. (2024). Auxiliary-Loss-Free Load Balancing Strategy for Mixture-of-Experts](https://arxiv.org/abs/2408.15664) giấy cân bằng dựa trên sự thiên vị.
  Trung ngữ翻译: dựa trên định vị của sự cân bằng chiến lược luận văn.
- [Dai et al. (2024). DeepSeekMoE: Towards Ultimate Expert Specialization in Mixture-of-Experts Language Models](https://arxiv.org/abs/2401.06066) các chi tiết tinh tế + chia sẻ chuyên gia chia sẻ các sử dụng của router bài học này.
  中文翻译:DeepSeekMoE 论文,细粒度 + 共享专家拆分──
- [Kim et al. (2022). DeepSpeed-MoE: Advancing Mixture-of-Experts Inference and Training](https://arxiv.org/abs/2201.05596) bài báo chuyên gia chung gốc.
  Trung văn翻译:DeepSpeed-MoE 原始共享专家论文──
