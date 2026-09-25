# Quick Caching và Context Caching 提示缓存与上下文缓存

> Hệ thống của bạn yêu cầu là 4.000 mã thông báo. ngữ cảnh RAG của bạn là 20.000 mã thông báo. Bạn gửi cả hai với mỗi yêu cầu. Bạn cũng trả cho cả hai lần. Cấp  nhanh cho phép nhà cung cấp giữ cho tiền đề ấm ở phía của họ và tính phí bạn 10% của tỷ lệ bình thường khi tái sử dụng. Được sử dụng đúng cách, nó cắt giảm chi phí suy luận bằng 5090% và độ trễ đầu tiên mã thông báo bằng 4085%.

> **【中文解读】**系统提示4000代币 + RAG 上下文20000代币, mỗi lần yêu cầu phải trả. 提示缓存让供应商保留前,重用时只收取10%费.

> **【拓展：提示缓存→RAG生产优化】**Phản ứng được lưu trữ của Antropic và OpenAI là một công nghệ quan trọng để giảm chi phí của hệ thống sản xuất RAG, đặc biệt là có các gợi ý hệ thống cố định và nhiều truy vấn trên các trường hợp sau đây:

>  **【前置】**学本节前请先掌握:Phase 11·01(Quá trình Kỹ thuật) 、Phase 11·05(Kỹ thuật ngữ) 、Phase 11·11(Tài lưu trữ chi phí) 本节是其延伸,讲供应商层 Anthropic cache_control、OpenAI 自动缓存、Gemini CachedContent) 

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 11 · 01 (Prompt Engineering), Phase 11 · 05 (Context Engineering), Phase 11 · 11 (Caching and Cost) | **前置知识:** Phase 11 · 01 (提示工程)、05 (上下文工程)、11 (缓存与成本)
**Time:** ~60 minutes | **时间:** ~60 分钟

## Vấn đề  vấn đề giới thiệu

Một đại lý lập trình gửi cùng một thông báo hệ thống 15.000 token cho Claude mỗi lần nói chuyện.$3/M input tokens is $0,90 trong chi phí đầu vào chỉ riêng  trước bất kỳ tin nhắn thực tế của người dùng. Nồng lên 10.000 cuộc trò chuyện hàng ngày và hóa đơn đạt 9.000 đô la / ngày cho văn bản không bao giờ thay đổi.

> Một lập trình viên trong mỗi cuộc trò chuyện gửi cùng một token 15.000  hệ thống gợi ý cho Claude.$3/M 输入 token，仅输入成本就是 $0.90 không bao gồm thông tin thực tế của người dùng.

Bạn không thể thu hẹp lời nhắc mà không làm tổn hại đến chất lượng. Bạn không thể tránh gửi nó  mô hình cần nó ở mọi lượt.

> Bạn không thể giảm giá mà không làm hỏng chất lượng. Bạn không thể tránh được việc gửi nó.

>  **【类比】**Caching nhanh như "快递公司记住你的常用地址"第一次发货要详细说明"北京市朝阳区...", sau đó mỗi lần发货 chỉ cần nói"老地方",快递公司自动调出地址。技术上: nhà cung cấp đặt tiền đề KV cache 存在自己的服务器,次请求来时直接复用,无需重新计算注意的 K/V矩阵。 đối với người dùng minh bạch你只需要在API调用加个`cache_control`标记――

> ️ **【易错点】**Caching nhanh của 3 个坑:(1) **prefix 顺序敏感**cache 命中要求 prefix 完全相同(包括空格、换行), hệ thống prompt 末尾多一个空格就错过;务必把可变部分(用户输入) để最后。(2) **cache TTL 5 分钟**Anthropic 默认 5 分钟过期,没流量时 cache 失效; dùng TTL mở rộng(1 小时)保住冷启动场景──(3) **没监控命中率** không biết tỷ lệ phát triển thì không thể đánh giá được lợi nhuận;`cache_creation_input_tokens`和 `cache_read_input_tokens`, ghi lại đến bảng giám sát.

Động thái đó là lưu trữ cache nhanh chóng. Anthropic đã đưa ra nó vào tháng 8 năm 2024 (với một biến thể TTL kéo dài 1 giờ vào năm 2025), OpenAI tự động hóa nó vào cuối năm đó, Google đã đưa ra lưu trữ bối cảnh rõ ràng cùng với Gemini 1.5, và cả ba bây giờ cung cấp nó như một tính năng hạng nhất trên các mô hình biên giới của họ.

> Cách này là để gợi ý lưu trữ. Anthropic đã ra mắt vào tháng 8 năm 2024 . OpenAI đã tự động hóa nó vào cuối năm, Google đã ra mắt một bộ nhớ lưu trữ dưới dạng hiển nhiên trên Gemini 1.5 bên cạnh.


> **【中文解读】**Giá trị của Quick Caching nằm trong hệ thống Quick thường dài ((5K+ token) và không thay đổi trong tất cả các yêu cầu.


## Khái niệm cốt lõi

> **【中文解读】**Quick Caching sử dụng tính năng của LLM 推理 Nếu nhiều yêu cầu chia sẻ cùng một prompt trước, có thể缓存 KV-cache 计算结果, tránh lặp lại tính toán.

> **【拓展：Prompt Caching 的成本节省】**Anthropic's Quick Caching sẽ lặp lại đầu vào trước Ưu điểm giảm khoảng 90%;; OpenAI's similar function will cache input 价格降至 $0.50/M tokens（原价 $5) ・ đối với hệ thống nhanh chóng 5K token + 平均 10 lần sử dụng lại trường hợp,月成本可降低约75% ・


![Prompt caching: write once, read cheap](../assets/prompt-caching.svg)

**The mechanic.**Khi tiền đề của yêu cầu phù hợp với một yêu cầu gần đây, nhà cung cấp phục vụ bộ nhớ cache KV từ chạy trước thay vì mã hóa lại các token. Bạn trả tiền viết nhỏ lần đầu tiên và giảm giá đọc lớn mỗi lần sau đó.

> **机制。**Khi yêu cầu của bạn phù hợp với yêu cầu gần đây, nhà cung cấp cung cấp KV-cache từ lần vận hành trước, thay vì mã hóa lại token. Bạn lần đầu tiên thanh toán một số tiền viết vào tiền thưởng, sau đó mỗi lần thưởng thức giảm giá lớn.

**Three provider flavors in 2026.**

| Provider | API style | Hit discount | Write premium | Default TTL | Min cacheable |
|---------|-----------|--------------|---------------|-------------|---------------|
| Anthropic | Explicit `cache_control` markers on content blocks | 90% off input | 25% surcharge | 5 min (extendable to 1 hour) | 1,024 tokens (Sonnet/Opus), 2,048 (Haiku) |
| OpenAI | Automatic prefix detection | 50% off input | none | Up to 1 hour (best-effort) | 1,024 tokens |
| Google (Gemini) | Explicit `CachedContent` API | Storage-billed; read at ~25% of normal | Storage fee per token·hour | User-set (default 1 hour) | 4,096 tokens (Flash), 32,768 (Pro) |

**The invariant.**Tất cả ba bộ nhớ cache chỉ có tiền đề. Nếu bất kỳ token nào khác nhau giữa các yêu cầu, mọi thứ sau token khác nhau đầu tiên là một lỗi. Đặt các phần * ổn định * ở phía trên, các phần * biến * ở phía dưới.

> **不变量。**三者都只缓存前──如果请求之间有任何代币不同,第一个不同代币后的所有内容都是未定中──将*稳定*部分放在顶部,*可变*部分放在底部──

### Layout thân thiện với cache

```
[system prompt]          <-- cache this
[tool definitions]       <-- cache this
[few-shot examples]      <-- cache this
[retrieved documents]    <-- cache if reused, else don't
[conversation history]   <-- cache up to last turn
[current user message]   <-- never cache (different every time)
```

Vi phạm lệnh  đặt thông điệp người dùng trên lệnh hệ thống, bỏ lại các truy xuất động giữa vài lần chụp  và bộ nhớ cache không bao giờ chạm.

> 违序将用户消息放在系统提示上, trong số ít mẫu trong 穿插动态检查缓存永远不会命中.

### Việc tính toán break-even

Antropic 25% viết phí nghĩa là một khối được lưu trữ trong cache phải được đọc ít nhất hai lần để tiết kiệm tiền. 1 viết + 1 đọc trung bình 0.675x chi phí mỗi yêu cầu (gài 32%); 1 viết + 10 đọc trung bình 0.205x (gài 80%). Quy tắc ngón tay: lưu trữ bất cứ điều gì bạn mong đợi sử dụng lại ít nhất 3 lần trong TTL.

> 25%  write in溢价 của Anthropic có nghĩa là các khối dự trữ phải được đọc ít nhất hai lần để có thể tiết kiệm tiền.

## Hãy xây dựng nó.
```figure
prompt-cache-hit
```

## Hãy xây dựng nó

### Bước 1: Cấp ấp yêu cầu nhân bản với các dấu hiệu rõ ràng

```python
import anthropic

client = anthropic.Anthropic()

SYSTEM = [
    {
        "type": "text",
        "text": "You are a senior Python reviewer. Follow the rubric exactly.\n\n" + RUBRIC_15K_TOKENS,
        "cache_control": {"type": "ephemeral"},
    }
]

def review(code: str):
    return client.messages.create(
        model="claude-opus-4-7",
        max_tokens=1024,
        system=SYSTEM,
        messages=[{"role": "user", "content": code}],
    )
```

- `cache_control`Markers nói với Anthropic để lưu trữ khối trong 5 phút. sử dụng lại trong cửa sổ đó nhấn; sử dụng lại sau khi hết hạn và viết lại.

> `cache_control`标记告诉人类将该块存储 5 分钟.

**Response usage fields:**

```python
response = review(code_a)
response.usage
# InputTokensUsage(
#     input_tokens=120,
#     cache_creation_input_tokens=15023,   # paid at 1.25x
#     cache_read_input_tokens=0,
#     output_tokens=340,
# )

response_b = review(code_b)
response_b.usage
# cache_creation_input_tokens=0
# cache_read_input_tokens=15023           # paid at 0.1x
```

Kiểm tra cả hai trường trong CI  nếu `cache_read_input_tokens`giữ ở mức không qua các yêu cầu, các khóa cache của bạn đang di chuyển.

> Trong CI kiểm tra hai đoạn này nếu`cache_read_input_tokens`Trong nhiều lần yêu cầu giữ cho không, chìa khóa lưu trữ của bạn đang di chuyển.

### Bước 2: TTL kéo dài một giờ

Đối với các công việc hàng dài, thời gian mất 5 phút hết hạn giữa các công việc.`ttl`- Có thể là:

```python
{"type": "text", "text": RUBRIC, "cache_control": {"type": "ephemeral", "ttl": "1h"}}
```

TTL 1 giờ chi phí gấp 2 lần phí viết (50% so với đường gốc thay vì 25%) nhưng trả lại nhanh chóng trên bất kỳ lô nào sử dụng lại tiền đề hơn 5 lần.

> 1 小时 TTL có giá trị nhập vào gấp 2 lần 50% cơ sở chứ không phải 25%), nhưng trong bất kỳ quá trình xử lý hàng hóa nào có thể tăng gấp 5 lần.

### Bước 3: OpenAI tự động lưu trữ

OpenAI không cho bạn gì để cấu hình. bất kỳ tiền tố trên 1.024 token phù hợp với yêu cầu gần đây nhận được giảm 50% tự động.

```python
from openai import OpenAI
client = OpenAI()

resp = client.chat.completions.create(
    model="gpt-5",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},   # long and stable
        {"role": "user", "content": user_msg},
    ],
)
resp.usage.prompt_tokens_details.cached_tokens  # the discounted portion
```

Cũng như quy tắc bố trí thân thiện với cache áp dụng. Hai điều giết chết cache của OpenAI mà không giết chết của Anthropic: thay đổi `user`Field (được sử dụng như một thành phần khóa cache) và các công cụ sắp xếp lại.

> Cũng như dự trữ Ước tính quy tắc áp dụng.`user`字段和重新排序工具──

### Bước 4: Gemini cache ngữ cảnh rõ ràng

Gemini xử lý cache như một đối tượng hạng nhất bạn tạo ra và đặt tên:

```python
from google import genai
from google.genai import types

client = genai.Client()

cache = client.caches.create(
    model="gemini-3-pro",
    config=types.CreateCachedContentConfig(
        display_name="rubric-v3",
        system_instruction=RUBRIC,
        contents=[FEW_SHOT_EXAMPLES],
        ttl="3600s",
    ),
)

resp = client.models.generate_content(
    model="gemini-3-pro",
    contents=["Review this code:\n" + code],
    config=types.GenerateContentConfig(cached_content=cache.name),
)
```

Gemini tính phí lưu trữ mỗi token·hour cho đến khi bộ nhớ cache tồn tại, và đọc ở mức ~ 25% tốc độ nhập bình thường. Đây là hình dạng phù hợp khi bạn sử dụng lại cùng một lệnh khổng lồ trong nhiều phiên trong nhiều ngày.

> Gemini 按缓存存活期间每代币·小时收取存储费,读取费率约为正常输入的25%──当你在多次会议中跨天重复使用相同的大型提示时,这是正确的选择──

### Bước 5: đo tốc độ tấn công trong sản xuất

Nhìn xem`code/main.py`cho một kế toán viên ba nhà cung cấp mô phỏng theo dõi ghi chép / đọc / bỏ qua và tính toán chi phí hỗn hợp cho mỗi yêu cầu 1K. Gate triển khai với tỷ lệ hit mục tiêu  hầu hết các thiết lập Anthropic sản xuất nên thấy > 80% phần đọc sau khi nóng lên.

> 见 `code/main.py`获取模拟的三供应商会计师,跟踪写入/读取/未命中计数并计算每千请求的混合成本──按目标命中率门控部署多数生产 类型 设置在预热后应见 >80% 读取比例──

## Những bẫy vẫn còn tồn tại vào năm 2026

> Năm 2026 vẫn đang trên đường:

- **Dynamic timestamps at the top.** `"Current time: 2026-04-22 15:30:02"`ở trên cùng của hệ thống yêu cầu. mọi yêu cầu bị bỏ lỡ. Di chuyển dấu thời gian dưới điểm vỡ cache.
  **顶部的动态时间戳。**系统提示顶部放 `"Current time: 2026-04-22 15:30:02"`                                                                                                                                                                                                                                                              
- **Tool reordering.**Tạo ra các công cụ theo thứ tự ổn định  một sự sắp xếp lại giữa các triển khai phá vỡ mọi hit.
  **工具重排序。**以稳定序列化工具部署间的字典重排破坏每次命中──
- **Free-text near-duplicates.**"Bạn là người hữu ích". vs "Bạn là một trợ lý hữu ích".
  **自由文本近似重复。**"Bạn là người hữu ích". vs "Bạn là một trợ lý hữu ích".
- **Too-small blocks.**Anthropic áp dụng một sàn 1.024 token (2.048 cho Haiku).
  **过小的块。**Anthropic 强制 1,024 token 下限(Haiku 为 2,048)。更小的块静默不缓存。
- **Blind cost dashboards.**Chia "tốc số đầu vào" thành cache vs không cache. Nếu không, giảm lưu lượng truy cập sẽ giống như một chiến thắng cache.
  **盲目的成本仪表板。**Đặt "đánh nhập token" phân chia thành cache vs 未缓存. Nếu không lưu lượng giảm trông giống như cache thắng.

## Hãy sử dụng nó để thực hiện

Lưu trữ 2026:

> 2026 缓存技术:

| Situation | Pick |
|-----------|------|
| Agent with stable 10k+ system prompt, many turns | Anthropic `cache_control` with 5-min TTL |
| Batch job reusing a prefix for 30+ minutes | Anthropic with `ttl: "1h"` |
| Serverless endpoints on GPT-5, no custom infra | OpenAI automatic (just make your prefix stable and long) |
| Multi-day reuse of a giant code/doc corpus | Gemini explicit `CachedContent` |
| Cross-provider fallback | Keep the cacheable prefix layout identical across providers so any hit works |

| 场景 | 选择 |
|------|------|
| Agent 有稳定 10k+ 系统提示、多轮 | Anthropic `cache_control` 配 5 分钟 TTL |
| 批处理重用前缀 30+ 分钟 | Anthropic 配 `ttl: "1h"` |
| GPT-5 上的无服务器端点、无定制基建 | OpenAI 自动（让前缀稳定且够长） |
| 多天重用大型代码/文档语料 | Gemini 显式 `CachedContent` |
| 跨提供商回退 | 跨提供商保持可缓存前缀布局一致，任何命中都工作 |

Kết hợp với bộ nhớ cache ngữ nghĩa (Phase 11 · 11) cho lớp tin nhắn người dùng: xử lý bộ nhớ cache nhanh * token-identical * tái sử dụng, bộ nhớ cache ngữ nghĩa * nghĩa-identical * tái sử dụng.

> Với ngữ义缓存(Phase 11 · 11) kết hợp dùng để người dùng消息层:提示缓存处理*token 完全相同*的重用,语义缓存处理*语义相同*的重用──

## Chuyển nó đi.

- Cứu lại`outputs/skill-prompt-caching-planner.md`- Có thể là:

```markdown
---
name: prompt-caching-planner
description: Design a cache-friendly prompt layout and pick the right provider caching mode.
version: 1.0.0
phase: 11
lesson: 15
tags: [llm-engineering, caching, cost]
---

Given a prompt (system + tools + few-shot + retrieval + history + user) and a usage profile (requests per hour, TTL needed, provider), output:

1. Layout. Reordered sections with a single cache breakpoint marked; explain which sections are stable, which are volatile.
2. Provider mode. Anthropic cache_control, OpenAI automatic, or Gemini CachedContent. Justify from TTL and reuse pattern.
3. Break-even. Expected reads per write within TTL; net cost vs no-cache with math.
4. Verification plan. CI assertion that cache_read_input_tokens > 0 on the second identical request; dashboard split by cached vs uncached tokens.
5. Failure modes. List the three most likely reasons the cache will miss in this setup (dynamic timestamp, tool reorder, near-duplicate text) and how you will prevent each.

Refuse to ship a cache plan that places a dynamic field above the breakpoint. Refuse to enable 1h TTL without a reuse count that makes the 2x write premium pay back.
```

## Tập luyện bài tập

1. **Easy.**Hãy nói chuyện 10 lần với một hệ thống 5000 token chống lại Claude.`cache_control`báo cáo hóa đơn đầu vào-token cho mỗi người.
   取一个10轮对话和5000 token 系统提示,不使用和使用 `cache_control`分別运行, báo cáo nhập mã thông báo 费用──
2. **Medium.**Viết một vòng kiểm tra, với một mẫu nhanh chóng và một nhật ký yêu cầu, tính toán tỷ lệ hit dự kiến và tiết kiệm đô la cho mỗi nhà cung cấp (Anthropic 5m, Anthropic 1h, OpenAI tự động, Gemini rõ ràng).
    biên soạn các công cụ kiểm tra, đưa ra các mẫu gợi ý và nhật ký yêu cầu, tính toán tỷ lệ dự kiến của mỗi nhà cung cấp và tiết kiệm số tiền:
3. **Hard.**Tạo một trình tối ưu hóa bố cục: được đưa ra một lời nhắc và một danh sách các trường được đánh dấu `stable=True/False`, viết lại lời nhắc để đặt một điểm vỡ cache duy nhất ở vị trí tối đa thân thiện với cache mà không mất thông tin.
   构建布局优化器: 重写提示将缓存断点放在最大缓存友好位置.

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|-----------------------|---------|
| Prompt caching | "Makes long prompts cheap" / "让长提示变便宜" | Reusing a provider-side KV-cache for matching prefixes; 50-90% discount on repeated input tokens. | 提示缓存：重用供应商端的 KV-cache，对重复输入 token 提供 50-90% 折扣 |
| `cache_control` | "The Anthropic marker" / "Anthropic 标记" | Content-block attribute that declares "everything up to here is cacheable"; `{"type": "ephemeral"}`. | cache_control：内容块属性，声明"到这里为止的内容可缓存" |
| Cache write | "Paying the premium" / "付溢价" | The first request that populates the cache; billed at ~1.25x input rate on Anthropic, free on OpenAI. | 缓存写入：第一次填充缓存的请求 |
| Cache read | "The discount" / "折扣" | Subsequent requests matching the prefix; billed at 10% (Anthropic), 50% (OpenAI), ~25% (Gemini). | 缓存读取：匹配前缀的后续请求 |
| TTL | "How long it lives" / "存活时间" | Seconds the cache stays warm; Anthropic 5m default (extendable 1h), OpenAI best-effort up to 1h, Gemini user-set. | TTL：缓存保持活跃的秒数 |
| Extended TTL | "1-hour Anthropic cache" / "1小时缓存" | `{"type": "ephemeral", "ttl": "1h"}`; 2x write premium but worth it for batch reuse. | 扩展 TTL：1 小时缓存，2 倍写入溢价 |
| Prefix match | "Why my cache missed" / "为什么缓存未命中" | Caches only hit when every token from the start up to the breakpoint is byte-identical. | 前缀匹配：缓存只在从开头到断点的每个 token 完全相同时才命中 |
| Context caching (Gemini) | "The explicit one" / "显式缓存" | Google's named, storage-billed cache object; best for multi-day reuse of large corpora. | 上下文缓存 (Gemini)：命名、按存储计费的缓存对象 |

## Xem thêm 延伸阅读

- [Anthropic — Prompt caching](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching) `cache_control`, 1h TTL, bàn hòa.
  提示缓存文档cache_control、1 小时 TTL、亏平衡表──
- [OpenAI — Prompt caching](https://platform.openai.com/docs/guides/prompt-caching) tự động phù hợp với tiền tố.
  OpenAI 提示缓存文档自动前匹配──
- [Google — Context caching](https://ai.google.dev/gemini-api/docs/caching) `CachedContent`API và giá lưu trữ.
  Google 上下文缓存文档CachedContent API và giá lưu trữ
- [Anthropic engineering — Prompt caching for long-context workloads](https://www.anthropic.com/news/prompt-caching) Đài khởi động ban đầu với số độ trễ.
  Anthropic 工程博客长上下文工作负载的提示缓存,含延迟数据──
- Giai đoạn 11 · 05 (Kỹ thuật ngữ)  nơi để cắt prompt để bộ nhớ cache có thể hạ cánh.
  第 11 阶段 · 05(上下文工程) 在哪里切分提示以便缓存生效.
- Giai đoạn 11 · 11 (Caching and Cost)  cặp prompt caching với một cache ngữ nghĩa trên tin nhắn người dùng.
  第 11 阶段 · 11(缓存与成本)  sẽ gợi ý缓存与用户消息的语义缓存配对──
- [Pope et al., "Efficiently Scaling Transformer Inference" (2022)](https://arxiv.org/abs/2211.05102) mô hình bộ nhớ cache KV- prompt caching cho người dùng; giải thích tại sao một prefix được lưu trữ trong cache lại rẻ hơn 10x so với tính toán lại.
  解释 tại sao dự trữ trước  trọng lượng tính toán rẻ hơn khoảng 10 lần KV-cache 内存模型论文。
- [Agrawal et al., "SARATHI: Efficient LLM Inference by Piggybacking Decodes with Chunked Prefills" (2023)](https://arxiv.org/abs/2308.16369) prefill là các đường tắt lưu trữ cache prompt giai đoạn; bài báo này giải thích tại sao TTFT giảm đáng kể trên hit cache trong khi TPOT không bị ảnh hưởng.
  解释 tại sao TTFT giảm mạnh trong thời gian tồn tại ư TPOT không bị ảnh hưởng ư
- [Leviathan et al., "Fast Inference from Transformers via Speculative Decoding" (2023)](https://arxiv.org/abs/2211.17192) Caching nhanh nằm cạnh việc giải mã suy đoán, Flash Attention và MQA/GQA như là các đòn bẩy làm cong cong cong cong chi phí suy luận; đọc đây cho ba phần còn lại.
  提示缓存与投机解码、Flash Attention 和 MQA/GQA 并列的推理成本曲线杆──
