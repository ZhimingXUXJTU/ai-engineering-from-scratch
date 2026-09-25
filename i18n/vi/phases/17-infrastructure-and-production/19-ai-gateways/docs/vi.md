# AI Gateways  LiteLLM, Portkey, Kong AI Gateway, Bifrost 网关 LLM

> Một cửa ngõ nằm giữa các ứng dụng của bạn và các nhà cung cấp mô hình. Các tính năng cốt lõi là định tuyến nhà cung cấp, trở lại, thử lại, giới hạn tốc độ, tham chiếu bí mật, khả năng quan sát, đường dây bảo vệ. Thị trường chia rẽ vào năm 2026: **LiteLLM**là MIT OSS với hơn 100 nhà cung cấp, tương thích với OpenAI, nhưng phá vỡ khoảng ~ 2000 RPS (8 GB bộ nhớ, thất bại hàng loạt trong các tiêu chuẩn được xuất bản); tốt nhất cho Python, <500 RPS, phát triển / tạo mẫu. **Portkey**được đặt trên máy điều khiển (các màn hình bảo vệ, biên soạn PII, phát hiện jailbreak, đường viếng kiểm tra), đã Apache 2.0 mã nguồn mở vào tháng 3 năm 2026, 20-40 ms latency overhead,$49/mo production tier. **Kong AI Gateway** built on Kong Gateway — Kong's own benchmark on same 12 CPUs: 228% faster than Portkey, 859% faster than LiteLLM; $Giá 100/mô hình/tháng (tối đa 5 trên cấp Plus); phù hợp với doanh nghiệp nếu bạn đã sử dụng Kong. **Bifrost**(Maxim AI)  tự động thử lại với cấu hình backoff, trở lại Anthropic trên OpenAI 429. **Cloudflare / Vercel AI Gateways** quản lý, không hoạt động, thử lại cơ bản. Data Residency thúc đẩy quyết định tự chủ; Portkey và Kong ngồi giữa với OSS + tùy chọn quản lý.

> **【中文解读】**Bài viết này giới thiệu AI 网关LLM Ứng dụng của các tuyến đường, cân bằng tải và an toàn 网关.


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy gateway-routing simulator) | **语言:** Python
**Prerequisites:** Phase 17 · 01 (Managed LLM Platforms), Phase 17 · 16 (Model Routing) | **前置知识:** Phase 17 · 01 (Managed LLM Platforms), Phase 17 · 16 (Model Routing)

>  **【前置】**Học本节前请先掌握:Phase 17·01(平台) 、Phase 17·16(路由) ・AI Gateway = 应用和模型商之间的代理 (路由/回退/限流/审计) ⋅
>  **【类比】**AI Gateway = "AI 流量交警"。LiteLLM = 开源 MIT 100+ nhà cung cấp, nhưng < 500 RPS 适合;Portkey = 控制面(PII 脱敏/越狱检测/审计) $49/月;Kong = 性能王(自家基准比 Portkey 快 228%、比 LiteLLM 快 859%), phù hợp với doanh nghiệp đã sử dụng Kong;Bifrost = 自动重试+按回退;Cloudflare/Vercel = 托管运维;;
**Time:** ~60 minutes | **时间:** ~60 minutes

## Mục tiêu học tập

- Đăng danh sáu tính năng cổng cổng cổng cổng cốt lõi (các định tuyến, quay lại, thử lại, giới hạn tốc độ, bí mật, khả năng quan sát, hàng rào).
  Trung文翻译:列举六个核心网关功能 (路由,回退,重试,速率限制,密钥管理,可观测性)
- Bản đồ bốn cửa ngõ 2026 (LiteLLM, Portkey, Kong AI, Bifrost) để mở rộng các trần và trường hợp sử dụng.
  Trung文翻译:将四个 2026 年网关(LiteLLM、Portkey、Kong AI、Bifrost)映射到规模上限和用例──
- Hãy trích dẫn chỉ số chuẩn Kong (228% so với Portkey, 859% so với LiteLLM) và giải thích tại sao nó quan trọng đối với > 500 RPS.
  Trung ngữ翻译:引用 Kong 基准测试(228% vs Portkey,859% vs LiteLLM)并解释为什么在 >500 RPS 时重要──
- Chọn tự lưu trữ vs quản lý với số liệu cư trú và ngân sách hoạt động.
  Trung ngữ翻译:给定数据驻留和运维预算, chọn tự quản lý so với quản lý.

## Vấn đề  vấn đề giới thiệu

> **【中文解读】**AI 网关 nằm giữa ứng dụng và nhà cung cấp mô hình, vấn đề cốt lõi được giải quyết là quản lý thống nhất của nhiều nhà cung cấp. Các sản phẩm đồng thời sử dụng OpenAI, Anthropic và tự quản lý Llama, mỗi nhà cung cấp có SDK khác nhau, mô hình sai lầm, giới hạn tốc độ và chương trình chứng nhận.

> **【拓展：2026 年 AI 网关市场】**4 người chơi chính của AI 网关市场 2026 năm:(1) LiteLLMMIT 开源,100+ nhà cung cấp, nhưng trong ~2000 RPS 时崩(8GB 内存);(2) Portkey 2026 năm 3 tháng 3 mở nguồn Apache 2.0, kiểm soát định vị mặt(guardrails、PII 脱敏、越狱检测、审计追踪),20-40ms 延迟开销;(3) Kong AI Gateway dựa trên các sản phẩm 网关 API trưởng thành,Kong 基准测试显示 hơn Portkey 快 228%、比 LiteLLM 快 859%;(4) Cloudflare/Vercel AI Gateway 托管、零运维、边缘部署.

Sản phẩm của bạn gọi là OpenAI, Anthropic và một Llama tự lưu trữ. Mỗi nhà cung cấp có SDK, mô hình lỗi, giới hạn tỷ lệ và chương trình auth khác nhau. Bạn muốn lỗi (nếu OpenAI 429, thử Anthropic), một cửa hàng tín chỉ duy nhất, khả năng quan sát thống nhất và giới hạn tỷ lệ cho mỗi thuê nhà.

Việc tái tạo điều này tại lớp ứng dụng kết hợp mọi dịch vụ với mỗi nhà cung cấp. Một lớp cổng kết hợp nó thành một quy trình với một API (thường tương thích với OpenAI) mà truyền tải đến các nhà cung cấp.

## Khái niệm cốt lõi

### 6 tính năng cốt lõi

1. **Provider routing** OpenAI, Anthropic, Gemini, tự lưu trữ, vv. đằng sau một API.
2. **Fallback** trên 429, 5xx, hoặc thất bại chất lượng, thử lại ở nơi khác.
3. **Retries** Vị trục trặc, cố gắng hạn chế.
4. **Rate limits** mỗi người thuê, mỗi người dùng, mỗi người mẫu.
5. **Secret references** rút thông tin tín dụng từ kho trong thời gian chạy (không bao giờ trong ứng dụng).
6. **Observability** Các thuộc tính OTel + GenAI (Phase 17 · 13) + tính phí.
7. **Guardrails** Phóng thông tin thông tin thông tin, phát hiện jailbreak, bộ lọc các chủ đề được phép.

### LiteLLM  MIT OSS, Python

- 100+ nhà cung cấp, tương thích với OpenAI, cấu hình router, sự suy giảm, khả năng quan sát cơ bản.
- Hạn nứt khoảng 2000 RPS trong chuẩn mực của Kong; 8 GB bộ nhớ, thất bại hàng loạt dưới tải liên tục.
- Ứng dụng Python, < 500 RPS, dev/staging gateway, định tuyến thử nghiệm.
- Chi phí: $ 0 cho OSS; lớp miễn phí đám mây tồn tại.

### Portkey  định vị máy bay điều khiển

- Apache 2.0 OSS tính từ tháng 3 năm 2026. Guardrails, PII redaction, jailbreak detection, audit trails.
- 20-40 ms mỗi yêu cầu thời gian trễ.
- $49/mo cho cấp sản xuất với lưu giữ + SLA.
- Khả năng phù hợp nhất: các ngành công nghiệp được quy định cần bao phủ + khả năng quan sát được kết hợp.

### Kong AI Gateway  chơi quy mô

- Được xây dựng trên Kong Gateway (thế phẩm Gateway API trưởng thành, lua+OpenResty).
- Chỉ số chuẩn của Kong trên tương đương 12 CPU: 228% nhanh hơn Portkey, 859% nhanh hơn LiteLLM.
- Giá: 100 đô la/mô hình/tháng, tối đa 5 trên Plus tier.
- Tích hợp tốt nhất: đã có Kong; > 1000 RPS; sẵn sàng cấp phép.

### Bifrost (Maximum AI)

- Lần thử lại tự động với backoff có thể cấu hình.
- Fallback to Anthropic on OpenAI 429 là một công thức truyền thống.
- Người mới đến, thương mại.

### Cloudflare AI Gateway / Vercel AI Gateway

- Được quản lý, không hoạt động, thử lại và có thể quan sát được.
- Tích hợp tốt nhất: Các ứng dụng JavaScript phục vụ Edge trên Cloudflare / Vercel.
- Giới hạn so với Kong/Portkey trên đường dây và giới hạn tốc độ.

### Tự lưu trữ vs quản lý

> **【中文解读】**Các yếu tố thúc đẩy quyết định của tự quản vs. quản lý là dữ liệu ở lại. Y tế và tài chính tự quản (LiteLLM hoặc Portkey OSS hoặc Kong); tiêu dùng sản phẩm tự quản (Cloudflare AI Gateway) hoặc tầng trung (Portkey managed)  Mẫu hỗn hợp:受监管租户自托管,其他托管.

> **【拓展：网关 + 可观测性 + 路由的组合】**Giai đoạn 17·13(可观测性) + 16(模型路由) + 19(网关) trong sản xuất là cùng một tầng.

Data residency là chức năng buộc. Chăm sóc sức khỏe và tài chính tự chủ mặc định (LiteLLM hoặc Portkey OSS hoặc Kong).

### Ngân sách thời gian trễ

> **【拓展：AI 网关延迟预算分析】**AI 网关延迟 trực tiếp ảnh hưởng đến TTFT, là yếu tố quan trọng của các loại chọn.

- LiteLLM: 5-15 ms tiêu thụ chung điển hình.
- Portkey: 20-40 ms trên cao.
- - 3-8 ms trên cao.
- Cloudflare/Vercel: 1-3 ms overhead (lợi thế cạnh).

Thời gian trễ Gateway trực tiếp thêm vào TTFT. Đối với TTFT P99 < 100 ms SLA, Kong hoặc Cloudflare. Đối với P99 < 500 ms, bất kỳ.

### Thuật ngữ giới hạn tỷ lệ

Simple token-bucket hoạt động ở quy mô vừa phải. Multi-tenant đòi hỏi cửa sổ trượt + allowance bùng nổ + tiering cho mỗi người thuê. LiteLLM vận chuyển token-bucket; Kong vận chuyển cửa sổ trượt; Portkey vận chuyển cấp.

### Gateway + khả năng quan sát + định tuyến kết hợp

Giai đoạn 17 · 13 (sự quan sát) + 16 (sự định tuyến mô hình) + 19 (cổng) là cùng một lớp trong sản xuất. Chọn một công cụ bao gồm cả ba hoặc dây chúng cẩn thận: hầu hết các triển khai 2026 kết hợp Helicone (sự quan sát) hoặc Portkey (các cửa sổ) với Kong (scale) cho vai trò chia rẽ.

### Những con số mà bạn nên nhớ

- LiteLLM: phá vỡ ở khoảng 2000 RPS, bộ nhớ 8 GB.
- Portkey: 20-40 ms overhead; Apache 2.0 từ tháng 3 năm 2026.
- Kong: 228% nhanh hơn Portkey, 859% nhanh hơn LiteLLM.
- Giá Kong: 100 đô la/mô hình/tháng, tối đa 5 đô la trên Plus tier.
- Cloudflare/Vercel: 1-3 ms trên đầu ở cạnh.

## Hãy sử dụng nó để thực hiện
```figure
mx-gateway-fallback
```

## Sử dụng nó

`code/main.py`mô phỏng định tuyến đường cổng với sự lùi ngược trên 3 nhà cung cấp dưới sự tiêm 429/5xx. báo cáo độ trễ, tỷ lệ thử lại và tỷ lệ hit sự lùi ngược.

> `code/main.py`mô phỏng định tuyến đường cổng với sự lùi ngược trên 3 nhà cung cấp dưới sự tiêm 429/5xx. báo cáo độ trễ, tỷ lệ thử lại và tỷ lệ hit sự lùi ngược.

> `code/main.py`mô phỏng định tuyến đường cổng với sự lùi ngược trên 3 nhà cung cấp dưới sự tiêm 429/5xx. báo cáo độ trễ, tỷ lệ thử lại và tỷ lệ hit sự lùi ngược.

## Chuyển nó đi.

Bài học này sẽ mang lại kết quả `outputs/skill-gateway-picker.md`Với quy mô, tư thế hoạt động, tuân thủ, ngân sách thời gian trễ, chọn một cửa ngõ.

> 本课产 出 `outputs/skill-gateway-picker.md`Với quy mô, tư thế hoạt động, tuân thủ, ngân sách thời gian trễ, chọn một cửa ngõ.

## Tập luyện bài tập

1. Đi chạy`code/main.py`. Định cấu hình fallback từ OpenAI→Anthropic→ tự lưu trữ.
   Trung ngữ翻译:运行 `code/main.py` Configuration OpenAI -> Anthropic -> 自托管的回归──哪个触发条件最合理?
2. SLA của bạn là TTFT P99 < 200 ms trên đường cơ sở 300 ms.
   Trung ngữ翻译: SLA của bạn là trên 300ms 基线 TTFT P99 < 200ms.
3. Một khách hàng chăm sóc sức khỏe cần tự lưu trữ + biên soạn PII + kiểm toán.
   Trung文翻译:一个医疗保健客户需要自托管 + PII 脱敏 + 审计――选择 Portkey OSS 或 Kong――
4. So sánh LiteLLM vs Kong: ở mức tối đa RPS nào một đội nên di chuyển?
   Trung ngữ翻译: So sánh LiteLLM vs Kong: Đội đoàn ở RPS trên giới hạn nên di chuyển?
5. Thiết kế một chính sách giới hạn lãi suất cho một SaaS đa thuê: cấp độ miễn phí, cấp độ thử nghiệm, cấp độ trả tiền.

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Gateway | "API broker" | Process sitting between apps and providers |
| LiteLLM | "the MIT one" | Python OSS, 100+ providers, breaks at 2K RPS |
| Portkey | "guardrails gateway" | Control plane + observability, Apache 2.0 |
| Kong AI Gateway | "the scale one" | Built on Kong Gateway, benchmark leader |
| Bifrost | "Maxim's gateway" | Retries + Anthropic fallback recipe |
| Cloudflare AI Gateway | "edge managed" | Edge-deployed managed gateway, zero-ops |
| PII redaction | "data scrub" | Regex + NER mask before sending to model |
| Jailbreak detection | "prompt injection guard" | Classifier on user input |
| Audit trail | "regulated log" | Immutable record of every LLM call |
| Token-bucket | "simple rate limit" | Refill-based rate limiter |
| Sliding-window | "precise rate limit" | Time-windowed rate limiter; better fairness |

## Xem thêm 延伸阅读

- [Kong AI Gateway Benchmark](https://konghq.com/blog/engineering/ai-gateway-benchmark-kong-ai-gateway-portkey-litellm)
- [TrueFoundry — AI Gateways 2026 Comparison](https://www.truefoundry.com/blog/a-definitive-guide-to-ai-gateways-in-2026-competitive-landscape-comparison)
- [Techsy — Top LLM Gateway Tools 2026](https://techsy.io/en/blog/best-llm-gateway-tools)
- [LiteLLM GitHub](https://github.com/BerriAI/litellm)
- [Portkey GitHub](https://github.com/Portkey-AI/gateway)
- [Kong AI Gateway docs](https://docs.konghq.com/gateway/latest/ai-gateway/)
