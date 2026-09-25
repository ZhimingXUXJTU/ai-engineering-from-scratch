# LLM Routing Layer  LiteLLM, OpenRouter, Portkey LLM 路由层:LiteLLM、OpenRouter và Portkey

> Việc khóa nhà cung cấp là đắt tiền. Các khối lượng công việc gọi công cụ khác nhau phù hợp với các mô hình khác nhau. Các cổng định tuyến cung cấp một bề mặt API, thử lại, lỗi, theo dõi chi phí và hàng rào. Ba kiểu nguyên mẫu thống trị năm 2026: LiteLLM (đánh nguồn tự lưu trữ), OpenRouter (đánh giá SaaS), Portkey (tạo sản xuất, nguồn mở vào tháng 3 năm 2026). Bài học này nêu tên các tiêu chí quyết định và đi bộ một cửa ngõ định tuyến stdlib.

> **【中文解读】**供应商锁定成本高昂. 工具调用工作负载适合不同的模型. 路由网关提供统一的 API. 接口,重试,故障转移. 成本追踪和护.

> **【拓展】**LLM 路由层解决的核心问题:按任务复杂度自动路由至优模型 (đơn giản là: 按任务复杂度自动路由至优模型) 成本优化 (đơn giản là: 按任务复杂度自动路由至优模型) 供应商故障自动切换 (đơn giản là: 按任务复杂度自动路由至优模型) 供应商故障自动切换 (đơn giản là: 按任务复杂度自动路由至优模型) 供应商故障自动切换 (高可用) 延迟敏感路由 (đơn giản là: 延迟敏感路由) 延迟敏感路由 (đơn giản là: 延迟敏感路由至高可用) 合规区域路由 (đơn giản là: 合规区域路由) 数据主权 (đơn giản là: A/B 测试路由) 实验 (đơn giản là: AI 工程 từ một mô hình hướng tới nhiều mô hình) 关键 cơ sở hạ tầng của cấu trúc mô hình đa mô hình.

>  **【前置】**Học本节前 vui lòng nắm bắt trước:(1) Giai đoạn 13·02(Fungsi gọi Deep Dive)  hiểu 3 nhà cung cấp API 差异,本节是统一它们的方案;(2) Giai đoạn 13·17(Gateways) 网关和路由经常一起部署;(3) HTTP 代理基础、重试与超时机制──

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, routing + failover + cost tracker) | **语言:** Python (stdlib, routing + failover + cost tracker)
**Prerequisites:** Phase 13 · 02 (function calling), Phase 13 · 17 (gateways) | **前置知识:** Phase 13 · 02 (function calling), Phase 13 · 17 (gateways)
**Time:** ~45 minutes | **时间:** ~45 分钟

## Mục tiêu học tập

- Sự khác biệt giữa các tùy chọn định tuyến tự lưu trữ, quản lý và cấp sản xuất.
  Trung ngữ翻译:区分自托管、托管和生产级路由选项。
- Thực hiện một chuỗi trở lại để thử lại các lỗi của nhà cung cấp theo một thứ tự ưu tiên xác định.
  Trung ngữ翻译:实现按定义优先级顺序在供应商失败时重试的回归链──
- Theo dõi chi phí theo yêu cầu và việc sử dụng token trên các nhà cung cấp.
  Trung ngữ翻译:跨供应商追踪每请求成本和代币使用量──
- Quyết định giữa LiteLLM, OpenRouter và Portkey cho một hạn chế sản xuất nhất định.

> **【中文解读】**Mục tiêu học tập: phân biệt tự quản lý, quản lý và các lựa chọn đường dẫn cấp sản xuất; thực hiện chuỗi quay lại khi nhà cung cấp bị hỏng; xuyên nhà cung cấp theo dõi từng yêu cầu chi phí và số lượng sử dụng token; dựa trên quy tắc sản xuất chọn LiteLLM/OpenRouter/Portkey。

## Vấn đề  vấn đề giới thiệu

> **【中文解读】**路由重要场景:(1) 成本Claude Sonnet 费用是 Haiku 的3倍,分流任务用 Haiku 足够;(2) 故障转移OpenAI 机时自动切换到人类;(3) 延迟实时聊天需要快速首代币;(4) 合规EU用户留在欧盟地区;(5) 实验A/B 两个模型──路由网关提供统一的 OpenAI 兼容 API 处理一切──

Các kịch bản trong đó định tuyến nhà cung cấp quan trọng:

> 供应商路由 quan trọng trường hợp:

1. **Cost.**Claude Sonnet chi phí 3 lần so với Haiku, cho một nhiệm vụ phân loại, Haiku là đủ, cho một nhiệm vụ tổng hợp, Sonnet là đáng giá.
  Trung ngữ翻译:**成本。**Claude Sonnet 成本是 Haiku's 3 倍──对分流任务,Haiku 够用;对综合任务,Sonnet 值得──每请求路由──

2. **Failover.**OpenAI có một giờ tồi tệ, mọi yêu cầu đều thất bại, bạn muốn tự động quay lại Anthropic mà không cần chuyển đổi.
  Trung ngữ翻译:**故障转移。**OpenAI có một giờ tồi tệ. Mỗi yêu cầu thất bại. Bạn muốn tự động trở lại Anthropic mà không cần phải tái triển khai.

3. **Latency.**Một giao diện trò chuyện trực tiếp cần mã thông báo thời gian nhanh chóng.
  Trung ngữ翻译:**延迟。**实时聊天 UI 需要快速首代币──批量摘摘器不需要──按延迟 SLA 路由──

4. **Compliance.**Người dùng EU phải ở lại các vùng EU.
  Trung ngữ翻译:**合规。**Người dùng EU phải ở lại EU 区域――按区域路由――

5. **Experimentation.**A/B hai mô hình trên cùng một khối lượng công việc.
  Trung ngữ翻译:**实验。**Trong cùng một tải trọng làm việc trên A/B 两个模型――按试桶路由――

Mã hóa bằng tay tất cả điều này mỗi tích hợp là lặp đi lặp lại. Một cửa cổng định tuyến cung cấp một API tương thích với OpenAI và xử lý phần còn lại.

> Mỗi người viết tất cả những điều này rất nhiều lần nữa.

>  **【类比】**LLM 路由网关像"万能充电转接头"──每个手机厂商(OpenAI/Anthropic/Google) có giao thức nhanh chóng tải riêng của mình(API 形态),原本你出差要带三根线──路由网关是一个" trung chuyển器"代码 của bạn chỉ dành cho giao diện USB-C (OpenAI 兼容 API) lập trình, chuyển đổi bên trong tùy thuộc vào nhiệm vụ tự động chọn nhanh nhất、 giao thức giao thức thất bại khi chuyển giao giao thức dự trữ giao thức(fallback)、计算 mỗi mức độ điện tiêu tốn bao nhiêu tiền(chi phí theo dõi)──换手机厂商你不需要重写代码──

## Khái niệm cốt lõi

### Hình dạng đại diện tương thích với OpenAI

Mọi người đều nói OpenAI.`/v1/chat/completions`, chấp nhận chương trình OpenAI, và nội bộ đại diện cho Anthropic / Gemini / Cohere / Ollama / bất cứ điều gì.

> Mỗi người nói OpenAI 形态──路由网关曝光 `/v1/chat/completions`、 chấp nhận OpenAI scheme、内部代理到Anthropic/Gemini/Cohere/Ollama/ bất cứ gì──客户端不关心──

### Tên đếm mẫu

Thay vì ghi thẻ ID, mã của bạn nói `our_smart_model`Khi một nhà cung cấp gửi một thế hệ mới, bạn thay đổi phía máy chủ tên; mã của bạn không chạm vào bất cứ thứ gì.

> Bạn của code không nói `claude-3-5-sonnet-20251022`Nhưng `our_smart_model` 网关将别名映射到真实模型──当Anthropic 发布Claude 4 时,你在服务器端改别名;代码不动──

> ️ **【易错点】**场景:fallback 链设置 5 nhà cung cấp và không thực hiện giới hạn ngân sách / 后果:上游故障时 5 nhà cung cấp都重试一遍,单请求成本升5倍;某些故障(如快速 违规) tất cả nhà cung cấp都会拒绝,重试无意而烧钱 / 修复:(1) 设置全局预算 cap,超出直接拒绝;(2) 区分"重试有意的错误"的错误(5xx、超时) 和"重试意的错误4xx、内容违规);(3) 同一请求总重试 ≤ 3 次;(4) 监控常规回落率,异升告警发.

> 🤔 **【困惑】**Q: 既然 LiteLLM 开源自托管, tại sao lại cần OpenRouter hoặc Portkey? A: 取决于团队能力:(1) **LiteLLM**适合有 DevOps 团队公司, tự bảo trì có thể kiểm soát chi phí, nhưng phải chịu trách nhiệm nâng cấp, giám sát, xử lý lỗi;**OpenRouter**SaaS  phù hợp với các dự án đầu tiên hoặc nhà phát triển cá nhân, nhưng giá đơn cao hơn;**Portkey**介于两者之间,开源但有商业版本――生产级(>10M req/day) thường là LiteLLM tự托管 + 商业 Portkey 混合:核心流量自托管,溢出走 Portkey。

### Các chuỗi quay trở lại

```
primary: openai/gpt-4o
on 5xx: anthropic/claude-3-5-sonnet
on 5xx: google/gemini-1.5-pro
on 5xx: refuse
```

Gateways định nghĩa điều này trong một cấu hình. Các thử nghiệm trở lại tính toán với ngân sách để các cơn suy giảm không làm nổ chi phí.

> 网关在配置中定义──重试计入预算,使退级联不爆炸成本──

### Caching ngữ nghĩa

Các lời nhắc giống hệt hoặc gần giống hệt nhau xảy ra trong cache thay vì nhà cung cấp.

> Tương tự hoặc gần như cùng một nhanh chóng trong dự trữ thay vì nhà cung cấp.

### Đường dây bảo vệ

Tầng cửa:

> 网关级:

- **PII redaction.**Regex hoặc ML-based pass trước khi gửi lời nhắc.
  Trung ngữ翻译:**PII 脱敏。**发送快速 前基于正则或ML 的脱敏──
- **Policy violations.**Tránh các lời nhắc với nội dung bị cấm.
  Trung ngữ翻译:**策略违规。**拒绝包含禁止内容的提示──
- **Output filters.**Trải hoàn thành để tìm thấy rò rỉ.
  Trung ngữ翻译:**输出过滤器。**清理补全中漏漏──

Portkey và Kong đều có hệ thống bảo vệ, LiteLLM lại cho phép chúng không được sử dụng.

> Portkey 和 Kong 都发布带主张的护──LiteLLM 留作可选──

### Các giới hạn lãi suất mỗi khóa

Một API key = một nhóm. Ngân sách mỗi khóa ngăn cản một nhóm tiêu thụ hạn ngạch chia sẻ. Hầu hết các cổng thông tin hỗ trợ điều này.

> Một khóa API = một nhóm. Mỗi khóa ngân sách ngăn chặn một nhóm tiêu thụ chia sẻ phần trăm.

### Các giao dịch tự lưu trữ vs giao dịch quản lý

| Factor | LiteLLM (self-hosted) | OpenRouter (managed) | Portkey (production) |
|--------|----------------------|----------------------|----------------------|
| Code | Open source, Python | Managed SaaS | Open source (Mar 2026) + managed |
| Setup | Deploy a proxy | Sign up | Either |
| Providers | 100+ | 300+ | 100+ |
| Billing | Your own keys | OpenRouter credits | Your own keys |
| Observability | OpenTelemetry | Dashboard | Full OTel + PII redaction |
| Best for | Teams that want full control | Rapid prototyping | Production with compliance |

LiteLLM thắng khi bạn có một đội SRE và muốn quyền chủ dữ liệu. OpenRouter thắng khi bạn muốn một thuê bao duy nhất và không có infra. Portkey thắng khi bạn cần các rào chắn và tuân thủ ra khỏi hộp.

> LiteLLM trong bạn có SRE  đội ngũ và muốn quyền sở hữu dữ liệu khi thắng đi.OpenRouter trong bạn muốn đơn đăng ký không cơ sở hạ tầng khi thắng đi.Portkey trong bạn cần mở hộp ngay lập tức với bảo vệ và quy định khi thắng đi.

### Theo dõi chi phí

Mỗi yêu cầu đều có`provider`- `model`- `input_tokens`- `output_tokens`- Tăng bằng giá mỗi mẫu/token (được rút ra từ bảng giá mà cửa khẩu duy trì).

> Mỗi yêu cầu mang theo`provider``model``input_tokens``output_tokens`△ nhân trên mỗi mô hình 价格 △ từ 网关维护的价格表拉取) △ theo người dùng/ đội ngũ/ dự án tập hợp △

### MCP cộng với định tuyến

Một gateway có thể định tuyến cả hai cuộc gọi LLM và yêu cầu lấy mẫu MCP. Khi mô hình yêu cầu lấy mẫuTích thích thích một mô hình cụ thể, gateway chuyển sang phía sau phải. Đây là nơi giai đoạn 13 · 17 (MCP gateway) và gateway định tuyến của bài học này đôi khi hợp nhất thành một dịch vụ.

> 网关可同时路由 LLM 调用和MCP sampling 请求──当采样 请求的模型 偏好特定模型时,网关翻译到正确后端──这是阶段13 · 17(MCP 网关) 和本课的路由网关有时合并为单一服务的地方──

### Chiến lược định tuyến

- **Static priority.**Đầu tiên trong danh sách; quay lại lỗi.
  Trung ngữ翻译:**静态优先级。**列表中第一; 出错时回退──
- **Load balancing.**Round-robin hoặc cân nặng.
  Trung ngữ翻译:**负载均衡。**轮询或加权──
- **Cost-aware.**Chọn mô hình rẻ nhất đáp ứng độ trễ / chất lượng.
  Trung ngữ翻译:**成本感知。**选择满足延迟/质量的最便宜模型――
- **Latency-aware.**Chọn mô hình nhanh nhất trong vòng 9 phút.
  Trung ngữ翻译:**延迟感知。**选最近 N 分钟最快的模型──
- **Task-aware.**Các tuyến phân loại nhanh có mã hóa cho một mô hình, tóm tắt cho mô hình khác.
  Trung ngữ翻译:**任务感知。**Ngay lập tức phân loại sẽ mã hóa đường dẫn đến một mô hình 摘要到另一个.

## Hãy sử dụng nó để thực hiện

> **【中文解读】** `code/main.py`实现约150行路由网关: chấp nhận OpenAI 格式请求,翻译到每供应商存根,运行优先级回归链,追踪每请求成本,应用 PII 脱敏――三个场景:正常请求、主供应商机触发故障转移、PII 泄露被脱敏拦截──
```figure
tp-router-failover
```

## Sử dụng nó

`code/main.py`thực hiện một cửa ngõ định tuyến trong ~ 150 dòng: chấp nhận các yêu cầu hình dạng OpenAI, dịch sang các đoạn thu thập hàng cho mỗi nhà cung cấp, chạy chuỗi sự cố trở lại ưu tiên, theo dõi chi phí mỗi yêu cầu, và áp dụng một thông qua chỉnh sửa PII cho các đầu vào.

> `code/main.py`实现约150 行的路由网关:接受OpenAI 形态请求"",翻译到每供应商存根"",运行优先级回归链"",追踪每请求成本"",对输入应用 PII 脱敏"",用三个场景运行:正常请求"",主要供应商机触发故障转移"",PII 泄露被脱敏捕"",

Những gì cần xem:

- `ROUTES`dict: alias -> danh sách các nhà cung cấp cụ thể theo thứ tự ưu tiên.
  Trung ngữ翻译:`ROUTES`字典:别名 -> 优先级排序的具体供应商列表──
- Chuyện quay lại lại lại ở 5xx.
  Trung文翻译: 回退循环在 5xx 上重试──
- Cost tracker nhân số việc sử dụng token bằng tỷ lệ cho mỗi mô hình.
  Trung ngữ翻译: Cost Tracker sẽ token dùng lượng nhân bằng mỗi tỷ lệ phí mô hình.
- PII biên tập scrubs SSN hình mẫu trước khi chuyển tiếp.
  Trung文翻译:PII 脱敏器在转发前清理 SSN 形状模式。

## Chuyển nó đi.

> **【中文解读】**本课产 出 `outputs/skill-routing-config-designer.md`给定工作负载配置(延迟、成本、合规), chọn LiteLLM/OpenRouter/Portkey 并生成路由配置──

Bài học này sẽ mang lại kết quả `outputs/skill-routing-config-designer.md`. Với một hồ sơ tải trọng công việc (sự trễ, chi phí, tuân thủ), kỹ năng chọn LiteLLM / OpenRouter / Portkey và tạo ra một cấu hình định tuyến.

> 本课产 出 `outputs/skill-routing-config-designer.md` Đưa định định vị tải trọng công việc (延迟、成本、合规), cho phép chọn LiteLLM/OpenRouter/Portkey và tạo ra các định vị đường bộ (路由配置).

## Tập luyện bài tập

1. Đi chạy`code/main.py`- Tạo ra tình huống ngừng hoạt động; xác nhận sự thất bại trên nhà cung cấp thứ hai và chi phí được gán đúng.
   Trung ngữ翻译:运行 `code/main.py`❖ Khả năng phát triển; xác nhận trở lại với nhà cung cấp thứ hai  chi phí chính xác thuộc về 

2. Thêm bộ nhớ cache ngữ nghĩa: SHA256 của lời nhắc là một khóa tìm kiếm; các lần nhấn bộ nhớ cache trở lại ngay lập tức. Đo tiết kiệm chi phí trên một cuộc gọi lặp lại.
   Trung文翻译:添加语义缓存:prompt 的 SHA256 是查找键;缓存命中立即返回──测量重复调用成本节省──

3. Thêm một trình phân loại nhanh chóng hướng dẫn "code ... " yêu cầu một tên gọi ủng hộ thông minh và "chổ chốt ... " yêu cầu một tên gọi ủng hộ tốc độ.
   Trung文翻译:添加快速 分类器,将"code ..."快速 路由到偏好智能的别名"",summarize ..." 路由到偏好速度的别名──

4. Thiết kế ngân sách cho mỗi nhóm: mỗi nhóm có một giới hạn chi tiêu hàng tháng; Gateway từ chối yêu cầu một khi giới hạn được chạm. Chọn một độ phân tích thực thi (per request hoặc windowsed).
   Trung ngữ翻译:设计每团队预算: mỗi团队 có chi tiêu hàng tháng lên giới hạn;网关在达到上限时拒绝请求――选择执行粒度(每请求或窗口)。

5. Đọc các tài liệu LiteLLM, OpenRouter và Portkey bên cạnh nhau.
   Trung文翻译:并排阅读 LiteLLM、OpenRouter 和 Portkey 文档──命名每个发布的但其他两个没有一个功能──

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means | 中文 |
|------|----------------|------------------------|------|
| Routing gateway | "LLM proxy" | One-API-surface layer in front of many providers | 路由网关：多供应商统一 API |
| OpenAI-compatible | "Speaks the OpenAI schema" | Accepts `/v1/chat/completions` shape, translates to any backend | OpenAI 兼容接口 |
| Model alias | "our_smart_model" | Name in your code that the gateway maps to a concrete model | 模型别名：代码中的抽象名 |
| Fallback chain | "Retry list" | Ordered list of providers attempted on failure | 回退链：失败时的有序重试列表 |
| Semantic caching | "Prompt-embedding cache" | Key is embedding of the prompt; near-duplicates share a cache hit | 语义缓存：嵌入向量近似匹配 |
| Guardrails | "Input/output filters" | Redact PII, reject policy violations | 护栏：输入输出过滤器 |
| Per-key rate limit | "Team budget" | Quota scoped to an API key | 按密钥限流：团队预算 |
| Cost tracking | "Per-request spend" | Aggregate token usage x price per model | 成本追踪：每请求费用 |
| LiteLLM | "The open proxy" | Self-hostable OSS routing gateway | LiteLLM：开源自托管路由网关 |
| OpenRouter | "The managed SaaS" | Hosted gateway with credit-based billing | OpenRouter：托管 SaaS 路由 |
| Portkey | "The production option" | Open-source + managed with guardrails built in | Portkey：生产级路由+护栏 |

## Xem thêm 延伸阅读

- [LiteLLM — docs](https://docs.litellm.ai/) Gateway tự lưu trữ
  Trung ngữ翻译:自托管路由网关
- [OpenRouter — quickstart](https://openrouter.ai/docs/quickstart) quản lý định tuyến SaaS
  Trung ngữ翻译:托管路由 SaaS
- [Portkey — docs](https://portkey.ai/docs) định tuyến sản xuất với đường dây bảo vệ
  Trung ngữ翻译:带护的生产路由
- [TrueFoundry — LiteLLM vs OpenRouter](https://www.truefoundry.com/blog/litellm-vs-openrouter) hướng dẫn quyết định
  Trung ngữ翻译:决策指南
- [Relayplane — LLM gateway comparison 2026](https://relayplane.com/blog/llm-gateway-comparison-2026) Nghiên cứu nhà cung cấp
  Trung ngữ翻译:供应商调研
