# Chaos Engineering for LLM Production 工程 生产 混沌 LLM

> Kỹ thuật hỗn loạn cho LLM là ngành riêng của nó vào năm 2026. Các điều kiện tiên quyết trước khi chạy các thí nghiệm trong sản xuất: SLI/SLO xác định, khả năng quan sát trace+metric+log, rollback tự động, runbook, on call. Kiến trúc có bốn tầng: điều khiển (chế hoạch hóa thí nghiệm), mục tiêu (công vụ, hạ tầng, kho dữ liệu), an toàn (các vệ sĩ + hủy bỏ + bộ lọc giao thông), khả năng quan sát (thường đo + dấu vết + nhật ký), phản hồi (trong các điều chỉnh SLO). Các đường dây bảo vệ là bắt buộc: báo cáo tỷ lệ đốt tạm dừng các thí nghiệm nếu dự kiến đốt cháy ngân sách lỗi hàng ngày > 2 lần; cửa sổ nén + mối tương quan theo dõi-ID giảm tiếng ồn báo động. Thời gian: đánh giá hàng tuần về loài cá thể nhỏ + SLO; ngày chơi hàng tháng + sau khi chết; kiểm tra khả năng phục hồi giữa các nhóm hàng quý + bản đồ phụ thuộc. Các thí nghiệm cụ thể của LLM: quá tải bộ nhớ, lỗi mạng, gián đoạn nhà cung cấp, các lời nhắc sai, bão sơ tán cache KV. Công cụ: Harness Chaos Engineering (sự khuyến nghị bắt nguồn từ LLM, giảm độ phóng xạ, tích hợp công cụ MCP); LitmusChaos (CNCF); Chaos Mesh (CNCF Kubernetes bản địa).

> **【中文解读】**Bài viết này giới thiệu về LLM 混沌工程 chủ động đắm vào故障 để kiểm tra thực tiễn LLM 服务性──


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy chaos experiment runner) | **语言:** Python
**Prerequisites:** Phase 17 · 23 (SRE for AI), Phase 17 · 13 (Observability) | **前置知识:** Phase 17 · 23 (SRE for AI), Phase 17 · 13 (Observability)

>  **【前置】**Học本节前请先掌握:Phase 17·23(SRE) 、Phase 17·13(可观测性) 、SRE 基础(SLI/SLO/错误预算) ⋅LLM 混沌工程 = 主动注入故障测性。
>  **【类比】**LLM 混沌工程 = "các tập luyện cứu hỏa"。 tiền đề:SLI/SLO 定义好、可观测、自动回滚、runbook、on-call。四平面:控制(实验调度) + mục tiêu(服务/数据/基础设施) +安全(守卫/中止/流量过) +可观测。必须护:错误预算燃烧率 > 2x 时暂停实验──节奏:每周小卡纳里度+月度游戏日+季度跨团队审计。LLM 专属实验:内存过载、网络故障、供应商 机、坏快点、KV cache 驱逐风暴──
**Time:** ~60 minutes | **时间:** ~60 minutes

## Mục tiêu học tập

- Hãy nêu tên năm yêu cầu kỹ thuật hỗn loạn (SLI/SLO, khả năng quan sát, quay lại, sổ chạy, khi gọi) và giải thích tại sao bỏ qua bất kỳ thực hành nào phá vỡ thực hành.
  Trung文翻译:说出五个混沌工程前置条件 (SLI/SLO、可观测性、回滚、运行手册、待命文化)
- Chụp đồ thị bốn tầng (chống chế, mục tiêu, an toàn, khả năng quan sát) và vòng phản hồi thành SLO.
  Trung文翻译: vẽ bốn hình ảnh (控制,目标,安全,可观测性) và phản  vòng quay đến bảng thiết bị SLO.
- Quảng cáo năm thí nghiệm cụ thể của LLM (thực lượng ghi nhớ quá tải, thất bại mạng, dịch vụ bị gián đoạn, thông báo sai lệch, cơn bão sơ tán KV).
  Trung文翻译:列举五个 LLM 特定的混沌实验(内存过载、网络故障、提供商机、形输入、缓存失效)
- Chọn một công cụ  Lợi dây, LitmusChaos, Chaos Mesh  được đưa ra hàng.
  中文翻译:选择工具Harness、LitmusChaos、Chaos Mesh根据技术。

## Vấn đề  vấn đề giới thiệu

> **【中文解读】**LLM 混沌工程 là một ngành độc lập năm 2026 ∙ LLM  tăng thêm mô hình故障 mới: 4K-token của các ký tự độc hóa làm cho phân từ器卡 tồn tại 12 giây; Up游 provider 429 触发网关重试,重试放大并发 dẫn đến OOM;突发负载下 KV Cache 淘汰风暴引发重新预填级联,耗尽计算资源──这些都不会 xuất hiện trong đơn vị thử nghiệm 混沌工程工具用户才发现它们的方法──

> **【拓展：LLM 混沌工程的五类实验】**2026 năm LLM 特定五类混沌实验:(1) 内存过载发送长上下文高并发请求引发 KV Cache 抢占风暴,观察服务是优雅降级还是崩;(2) 网络故障断断推理网关与供应商的连接,观察故障是否在SLA内生效;(3) 供应商中断模拟100% OpenAI 429,观察路由是否失败到Anthropic;(4) 形提示注入器具死负载吗(分层嵌套 Unicode、 UTF-8码点),观察单个请求锁住员工淘汰;5) KV 淘汰巨大暴风和vLLM 块预算强制淘汰, L L L 恢复服务量.

Các thử nghiệm hỗn loạn trong các đống truyền thống được thiết lập. Các đống LLM thêm các chế độ thất bại mới. Một lệnh mã thông báo 4K với ký tự độc ngăn chặn token trong 12 giây. Một nhà cung cấp cấp trên dòng chảy 429s; cửa cổng của bạn thử lại; OOM dịch vụ của bạn trên đồng thời tăng cường thử lại. Một cơn bão sơ tán cache KV dưới tải nổ gây ra các thác tái lấp đầy mà bão hòa tính toán.

Không có một trong những điều này xuất hiện trong các thử nghiệm đơn vị.

## Khái niệm cốt lõi

### Các điều kiện tiên quyết

> **【中文解读】**Trong sản xuất vận hành kiểm tra hỗn loạn có 5 điều kiện: 1) SLI/SLO 已定义; 2) 可观测性(trace + metric + log) đã triển khai; 3) 自动回滚机制就绪; 4) 结构化 runbook 已编写; 5) Có nhân viên có giá trị đáp ứng; thiếu bất kỳ một điều gì, hỗn loạn就会变成真实事件――四个平面:控制面(实验调度器) 目标面服务/基础设施) 安全、面杀开关 + 抑制窗口 + blast radius 限制) 、观测面标签 + 轨迹 关联)  反循环将发现可回到 SLO 调整、运行 更新和代码书修复.

Đừng gây hỗn loạn trong sản xuất mà không có:

1. **SLI/SLO** xác định các chỉ số và mục tiêu cấp độ dịch vụ.
2. **Observability** dấu vết, số liệu, nhật ký, được nối với bảng điều khiển.
3. **Automated rollback** Giai đoạn 17 · 20 Phục hồi cờ chính sách.
4. **Runbooks** cấu trúc, giai đoạn 17 · 23.
5. **On-call** ai đó để trả lời.

Không có bất kỳ phương tiện nào, hỗn loạn trở thành sự cố thực sự.

### Bốn máy bay + phản hồi

**Control plane** lập trình thí nghiệm (Litmus workflow, lịch trình Chaos Mesh, Harness UI).

**Target plane** dịch vụ, pods, nút, cân bằng tải, lưu trữ dữ liệu.

**Safety plane** chuyển đổi tắt, cửa sổ nén, giới hạn bán kính nổ, cửa sổ ngân sách lỗi.

**Observability plane** các số liệu bình thường + mối tương quan theo dõi ID để phân biệt sự hỗn loạn gây ra từ các thất bại tự nhiên.

**Feedback loop** các phát hiện được đưa vào điều chỉnh SLO, cập nhật sổ chạy, sửa mã.

### Các đường dây bảo vệ là bắt buộc

> **【拓展：混沌工程的安全护栏】**3 bảo mật thiết yếu của công trình hỗn loạn: 1) 燃尽率告警 trong quá trình thí nghiệm nếu mỗi ngày tiêu thụ ngân sách sai lầm vượt quá dự kiến 2x, tự động tạm dừng thí nghiệm; 2) 抑制窗口 trong vòng bán kính nổ của thí nghiệm, tránh tiếng ồn; 3) Trace-ID 关联 tất cả các thí nghiệm gây ra sai lầm mang theo nhãn hiệu, để trên cuộc gọi có thể được tái tạo.

- **Burn-rate alert**: thử nghiệm tạm dừng nếu số lượng lỗi ngân sách hư hỏng hàng ngày vượt quá 2 lần dự kiến.
- **Suppression windows**: làm im lặng các cảnh báo không thử nghiệm trong bán kính nổ trong khi thử nghiệm.
- **Trace-ID correlation**: tất cả các lỗi do thí nghiệm gây ra đều có thẻ để người gọi có thể rút ra.

### Năm thí nghiệm đặc biệt về LLM

1. **Memory overload** gây ra một cơn bão dự phòng KV bằng cách gửi yêu cầu trong bối cảnh dài với đồng thời cao.

2. **Network failure** cắt kết nối giữa cổng dẫn đầu và nhà cung cấp.

3. **Provider outage simulation** 100% 429 từ OpenAI. Quan sát: việc định tuyến không chuyển sang Anthropic? (Phase 17 · 16, 19)

4. **Malformed prompt** Inject token-stalling payload (ví dụ, Unicode sâu tổ, codepoint UTF-8 khổng lồ).

5. **KV eviction storm** buộc phải sơ tán bằng cách bão hòa ngân sách khối vLLM.

### Tỷ lệ

- **Weekly** thí nghiệm nhỏ của loài cá voi trong giai đoạn, có lẽ là 5%
- **Monthly** ngày chơi được lên kế hoạch trong một kịch bản cụ thể; sự tham dự của các đội; sau khi chết.
- **Quarterly** kiểm toán khả năng phục hồi giữa các nhóm; cập nhật bản đồ phụ thuộc.

### Thiết bị công cụ

> **【拓展：混沌工程工具选择】**2026 năm hỗn loạn kỹ thuật công cụ chọn:(1) Harness Chaos Engineering thương mại,AI 驱动的实验推,blast radius自动缩放,MCP 工具集成;(2) LitmusChaosCNCF 毕业,Kubernetes 工作流式;(3) Chaos MeshCNCF 沙箱,Kubernetes-native CRD风格;(4) Gremlin thương mại,广泛支持;(5) AWS FIS / Azure Chaos Studio托管云服务;;节奏建议:每周小卡纳里 实验 + SLO 审查,每月游戏日 + hậu quả,每季度跨团队性审计 + 依赖映射更新;;

- **Harness Chaos Engineering** thương mại; khuyến nghị thí nghiệm có nguồn gốc từ AI; giảm quy mô bán kính nổ; tích hợp công cụ MCP.
- **LitmusChaos** CNCF tốt nghiệp; Kubernetes dựa trên dòng công việc.
- **Chaos Mesh** hộp cát CNCF; phong cách CRD gốc Kubernetes.
- **Gremlin** thương mại; hỗ trợ rộng rãi.
- **AWS FIS**- **Azure Chaos Studio** cung cấp đám mây được quản lý.

### Bắt đầu nhỏ

thí nghiệm đầu tiên: giết một bản sao decode dưới lưu lượng truy cập ổn định. quan sát chuyển hướng và phục hồi. Nếu điều này hoạt động và trông an toàn, tốt nghiệp cho hỗn loạn mạng.

thí nghiệm đầu tiên của LLM: tiêm 429 cho một nhà cung cấp trong 5 phút. quan sát sự lùi. hầu hết các nhóm phát hiện ra sự lùi của họ không được kiểm tra đầy đủ.

### Những con số mà bạn nên nhớ

- Bốn máy bay: điều khiển, mục tiêu, an toàn, khả năng quan sát.
- Hỗng hỏng: 2 lần dự kiến ngân sách hỏng hàng ngày.
- Thời gian: hàng tuần canary, ngày chơi hàng tháng, kiểm toán hàng quý.
- Năm thí nghiệm LLM: bộ nhớ, mạng, nhà cung cấp, phản ứng sai, cơn bão KV.

## Hãy sử dụng nó để thực hiện
```figure
i4-chaos-guard
```

## Sử dụng nó

`code/main.py`mô phỏng ba thí nghiệm hỗn loạn với cổng máy bay an toàn.

> `code/main.py`mô phỏng ba thí nghiệm hỗn loạn với cổng máy bay an toàn.

> `code/main.py`mô phỏng ba thí nghiệm hỗn loạn với cổng máy bay an toàn.

## Chuyển nó đi.

Bài học này sẽ mang lại kết quả `outputs/skill-chaos-plan.md`Với sự phát triển và sự trưởng thành, chọn ba thí nghiệm đầu tiên và công cụ.

> 本课产 出 `outputs/skill-chaos-plan.md`Với sự phát triển và sự trưởng thành, chọn ba thí nghiệm đầu tiên và công cụ.

## Tập luyện bài tập

1. Đi chạy`code/main.py`Thử nghiệm nào làm vỡ cửa đốt và tại sao?
   Trung ngữ翻译:运行 `code/main.py`◊ Chuyện nào đã làm cho nhiệt độ đốt cháy được kiểm soát?
2. Thiết kế năm thí nghiệm hỗn loạn đầu tiên cho một dịch vụ RAG dựa trên vLLM. Bao gồm các tiêu chí thành công.
   Trung文翻译:为基于vLLM的RAG 服务设计前五个混沌实验──
3. Lần báo động của bạn đã dừng một thí nghiệm.
   Trung ngữ翻译: Your burn rate告警暂停了一个实验. Làm thế nào để xác định kết quả của việc làm so với dự kiến?
4. tranh luận liệu sự hỗn loạn có nên diễn ra trong sản xuất hay chỉ là sự dàn dựng. Khi nào sản xuất là câu trả lời đúng?
   Trung ngữ翻译:论证混沌实验应该在生产中还是仅在预发布环境运行中.
5. Hãy nêu tên ba chế độ thất bại cụ thể của LLM mà hỗn loạn mạng chung không thể tái tạo.

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| SLI / SLO | "service targets" | Indicator + objective; required prerequisite |
| Blast radius | "scope" | Set of services / users affected by experiment |
| Burn-rate alert | "budget gate" | Fires when error-budget burn rate > 2x expected |
| Game day | "monthly drill" | Scheduled cross-team chaos exercise |
| LitmusChaos | "CNCF workflow" | Graduated CNCF Kubernetes chaos tool |
| Chaos Mesh | "CNCF CRD" | CNCF sandbox Kubernetes-native chaos |
| Harness CE | "commercial AI-assisted" | Harness chaos with AI recommendations |
| Malformed prompt | "tokenizer bomb" | Input that stalls tokenization |
| KV eviction storm | "preemption cascade" | Mass eviction triggering re-prefills |

## Xem thêm 延伸阅读

- [DevSecOps School — Chaos Engineering 2026 Guide](https://devsecopsschool.com/blog/chaos-engineering/)
- [Ankush Sharma — Observability for LLMs (book)](https://www.amazon.com/Observability-Large-Language-Models-Engineering-ebook/dp/B0DJSR65TR)
- [LitmusChaos (CNCF)](https://litmuschaos.io/)
- [Chaos Mesh (CNCF)](https://chaos-mesh.org/)
- [Harness Chaos Engineering](https://www.harness.io/products/chaos-engineering)
- [AWS FIS](https://aws.amazon.com/fis/)
