# Mô hình định tuyến như một chi phí giảm nguyên thủy

> Một nhà môi giới năng động đánh giá mọi yêu cầu (loại nhiệm vụ, chiều dài token, nhúng tương tự, sự tự tin) và gửi các yêu cầu đơn giản đến một mô hình rẻ tiền, leo thang những yêu cầu phức tạp đến một mô hình biên giới. Cũng gọi là mẫu vỏ. Các nghiên cứu trường hợp sản xuất cho thấy giảm chi phí từ 20-60% ở chất lượng iso trên các triển khai của Mỹ / Anh / EU; cải thiện hiệu quả định tuyến 30% trên SaaS khối lượng cao chuyển thành tiết kiệm hàng năm sáu chữ số. Tầm quan điểm của năm 2026 là giá suy luận LLM giảm ~ 10 lần mỗi năm  một token lớp GPT-4 đã đi từ $20/M to ~$0,40/M từ cuối năm 2022 đến năm 2026. Phần lớn sự giảm là phục vụ tốt hơn các đống (Phase 17 · 04-09), chứ không phải phần cứng. Đường dẫn là cách bạn chuyển đổi giá giảm thành biên mà không có sự lùi sản phẩm. Phương thức thất bại là biến động mô hình rẻ tiền: tuyến đường đẩy 40% lên mô hình yếu hơn, chất lượng giảm 3-5% đối với các nhiệm vụ lý luận, không ai nhận ra cho một phần tư. Các tuyến đường Gate theo các métrics chất lượng trực tuyến, không chỉ là các thiết lập đánh giá ngoại tuyến.

> **【中文解读】**Phần này giới thiệu các chiến lược tối ưu hóa chi phí của các mô hình khác nhau dựa trên sự phức tạp của nhiệm vụ.


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy cascading router simulator) | **语言:** Python
**Prerequisites:** Phase 17 · 01 (Managed LLM Platforms), Phase 17 · 19 (AI Gateways) | **前置知识:** Phase 17 · 01 (Managed LLM Platforms), Phase 17 · 19 (AI Gateways)

>  **【前置】**学本节前请先掌握:Phase 17·01(托管平台) 、Phase 17·19(AI Gateway) 』模型路由 = 动态经纪人 按任务复杂度选便宜或贵模型──
>  **【类比】**模型路由 = "医院分诊"──简单感冒→社区医生(Haiku/Sonnet);疑难杂症→专家(Opus);急诊→主任(GPT-4)──20-60% 成本降,30% 路由效率改进=六位数年省──背景:LLM 价格 2022-2026 降10倍/年,多数降来自服务改进而非硬件路由把价格转转转为利──
> ️ **【易错点】**便宜模型漂移:40% 路由到弱模型→推理质量降低 3-5%→ một季度没人发现──修复:用在线质量监控(不仅离线评估)守住底线──
**Time:** ~60 minutes | **时间:** ~60 minutes

## Mục tiêu học tập

- Giải thích mô hình hàng loạt: rẻ tiền đầu tiên với kiểm tra sự tin tưởng, leo thang trên sự tin tưởng thấp.
  Trung ngữ翻译:解释模型级联:廉价优先加置信度检查,低置信度时升级──
- Đếm theo bốn tín hiệu định tuyến (tỷ lệ phân loại nhiệm vụ, độ dài nhanh, nhúng tương tự với bộ cứng được biết, tự tin từ lần qua đầu tiên).
  Trung文翻译:列举四种路由信号(任务分类、提示长度、嵌入相似度、首次通过自置信度)
- Xét chi phí hỗn hợp dự kiến tại mục tiêu định tuyến chia và dung nạp mất chất lượng.
  Trung文翻译:计算目标路由分流和质量损失耐受度下预期混合成本。
- Hãy cho biết số liệu giám sát drift (cổng chất lượng trực tuyến) bắt được những người lăn lăn rẻ tiền.
  Trung ngữ翻译:说出捕获廉价模型质量漂移的漂移监控指标 (在线质量门控)

## Vấn đề  vấn đề giới thiệu

> **【中文解读】**模型路由的核心洞察:70% truy vấn là đơn giản ("Paris đã vài điểm rồi?"), có thể được xử lý hoàn hảo với mô hình cấp Haiku với chi phí 3%  Chỉ 30% cần khả năng suy luận cấp GPT-5  70% từ mô hình giá rẻ, 30% từ mô hình tiền tuyến, có thể giảm giá trị sản phẩm tương tự khoảng 65%  thách thức chính là xây dựng bộ đường không làm giảm chất lượng 

> **【拓展：模型路由的产业案例】**2026 năm mô hình đường từ trong sản xuất: 20-60% giảm chi phí: GPT-4  cấp từ năm 2022 đến 2026$20/M 降到 $0,40/M), phần lớn giảm từ các biện pháp tối ưu hóa (Phase 17·04-09)  Các phương pháp làm cho bạn có thể nắm bắt được những lợi ích này trong ứng dụng, thay vì chờ đợi tất cả người dùng chuyển đến các phương pháp giá rẻ  Các phương pháp làm cho các phương tiện làm việc có thể được sử dụng tốt hơn.

Dịch vụ của bạn chi phí 80k USD/tháng trên GPT-5. phân tích của bạn cho thấy 70% các câu hỏi là đơn giản: "Thời gian là bao nhiêu giờ ở Paris?" "được định nghĩa lại câu này". Một mô hình lớp Haiku xử lý hoàn hảo với 3% chi phí. 30% cần lý luận của GPT-5  mã hóa, toán học, lập kế hoạch đa bước.

Nếu bạn chuyển 70% sang rẻ và 30% sang đắt tiền, hóa đơn của bạn giảm khoảng 65% với chất lượng sản phẩm tương tự. Đây là chuyển hướng. Trù là xây dựng nhà môi giới mà không làm giảm chất lượng.

## Khái niệm cốt lõi

### Bốn tín hiệu định tuyến

> **【中文解读】**四种路由信号:(1) 任务分类简单/复杂/代码/数学/聊天,可用规则分类器或小 LLM($0.25/M);(2) 提示长度>4K token thường cần mô hình tiền tuyến,<500 thường không cần;(3) 嵌入相似度与已知困难集的余弦相似度 >0.88 则直接升级;(4) 首次通过自信度发送到廉价模型,如果日志检查 显示低信任度或拒绝,重试到沿模型──

1. **Task classification**: đơn giản/ phức tạp/ codegen/ toán học/ trò chuyện. Có thể là một phân loại dựa trên quy tắc, một LLM nhỏ (Haiku-class ở $0.25/M), hoặc nhúng sự tương tự với các bình có nhãn.

2. **Prompt length**Các mã thông báo <500 mã thông báo thường không.

3. **Embedding similarity to known-hard set**: nếu truy vấn gần (cosine > 0,88) với một thùng cứng được biết đến, leo thang trực tiếp đến biên giới.

4. **Self-confidence from first-pass**: gửi cho rẻ; nếu các bản kiểm tra nhật ký của mô hình cho thấy sự tin cậy thấp OR nó từ chối OR xuất khẩu ngôn ngữ bảo hiểm, thử lại ở biên giới.

### Ba mô hình

> **【拓展：模型路由的三种模式】**1) Pre-route前置分类器 (định luật hoặc LLM nhỏ), tăng 5-10ms 延迟,总体最快; 2) Cascade先发到廉价模型,低信度时升级到前沿模型,中位延迟约1.2x、升级时约2x,质量底线最好; 3) Ensemble route并行运行廉价和前沿模型,奖励模型选择最佳,最高质量但最高成本;; trong sản xuất 建议 Cascade 作为默认它提供最佳平衡在质量,成本,延迟之间.

**Pre-route**(classifier trước): ~ 5-10ms latency thêm; nhanh nhất tổng thể.

**Cascade**(tô-lệ nhất, tăng lên trên độ tin cậy thấp): ~ 1.2x độ trễ trung bình (điều chạy rẻ cộng với xác minh), ~ 2x trên tăng lên. chất lượng tốt nhất sàn.

**Ensemble route**(điều kiện rẻ và biên giới song song cho một mẫu, chọn mô hình thưởng): chất lượng cao nhất, chi phí cao nhất; chỉ sử dụng cho A/B quan trọng.

### Thực hiện

Các cổng thông tin AI (Phase 17 · 19) phơi bày định tuyến. LiteLLM đã `router`config với fallback và cost-routing. Portkey có guard + routing. Kong AI Gateway có plugin-based routing.

Mã nguồn mở: RouteLLM (LMSYS), Không Diamond (thị thương mại), Prompt Mule.

### Lập giá năm 2026

| Model class | Late 2022 | 2026 | Change |
|-------------|-----------|------|--------|
| GPT-4-level quality | ~$20/M | ~$0.40/M | 50x cheaper |
| Frontier (GPT-5, Claude 4) | — | ~$3-10/M | new tier |

Phần lớn cải tiến là phục vụ hiệu quả  các bài học cốt lõi trong giai đoạn 17 · 04-09 biến thành giảm chi phí bên nhà cung cấp. Routing cho phép bạn nắm bắt những lợi nhuận đó ở lớp ứng dụng thay vì chờ đợi tất cả người dùng của bạn di chuyển sang cấp độ rẻ.

### Sự trôi chảy là rủi ro thực sự

> **【中文解读】**漂移是模型路由的真正风险──路由将将40% 发送到廉价模型,6 个月后任务分布变化(用户更成熟、问题更长), nhưng phân loại thiết bị của router vẫn dựa trên Q1 数据训练──质量下降没有投诉足够响亮,直到在竞争对手基准测试中落败才知道──必须通过在线质量指标门控路由:用户反自动LLM 评审(5% 采样) 升级率、拒绝率──

> **【拓展：模型路由的实现方案】**2026 năm mô hình đường dẫn thực hiện các lựa chọn:(1) AI 网关(Phase 17·19) LiteLLM của router cấu hình, Portkey của các vệ sĩ+routing,Kong AI Gateway của plug-like路由,OpenRouter của khuyến cáo API;(2) 开源RouteLLM(LMSYS) cung cấp đầy đủ các bộ 路由库;(3) 商业Not Diamond 提供 SaaS 模型路由产品;;

Tuy nhiên, bạn có thể không nhận thấy được các thông tin về các công cụ phân loại của mình, vì nó được đào tạo dựa trên dữ liệu Q1.

Các tuyến đường cổng theo các chỉ số chất lượng trực tuyến:

- Người dùng thumbs-up / thumbs-down trên mỗi tuyến đường.
- Thẩm phán LLM tự động trên một mẫu (5%) cho mỗi tuyến đường.
- Tốc độ leo thang: nếu dòng băng đang tăng lên > 30%, mô hình rẻ tiền đang bị chuyển quá mức.
- Tỷ lệ từ chối trên mỗi tuyến đường.

### Những con số mà bạn nên nhớ

- 2026 tiết kiệm đường dẫn ở chất lượng iso: 20-60% nghiên cứu trường hợp.
- Thảm giá LLM 2022-2026: tổng cộng 10 lần mỗi năm.
- GPT-4 cấp 2022 vs 2026: ~$20/M → ~$0,40/M.
- Tác động độ trễ ngập: ~ 1.2x trung bình, ~ 2x leo thang (~ 10% lưu lượng truy cập).

## Hãy sử dụng nó để thực hiện
```figure
model-cascade-router
```

## Sử dụng nó

`code/main.py`mô phỏng trước đường, hàng loạt và tập hợp trên một khối lượng công việc hỗn hợp.

> `code/main.py`mô phỏng trước đường, hàng loạt và tập hợp trên một khối lượng công việc hỗn hợp.

> `code/main.py`mô phỏng trước đường, hàng loạt và tập hợp trên một khối lượng công việc hỗn hợp.

## Chuyển nó đi.

Bài học này sẽ mang lại kết quả `outputs/skill-router-plan.md`Với khối lượng công việc và ngân sách chất lượng, chọn một mô hình định tuyến và tín hiệu.

> 本课产 出 `outputs/skill-router-plan.md`Với khối lượng công việc và ngân sách chất lượng, chọn một mô hình định tuyến và tín hiệu.

## Tập luyện bài tập

1. Đi chạy`code/main.py`- Ở tầng độ chính xác nào, thủy thủ đợt vượt qua đường dẫn trước?
   Trung ngữ翻译:运行 `code/main.py`◊ Cấp độ liên kết ở mức độ nào thấp hơn đường dẫn trước?
2. Cơ sở người dùng của bạn là 30% doanh nghiệp (phân tích phức tạp), 70% cấp độ miễn phí ( đơn giản). Thiết kế phân chia định tuyến.
   Trung ngữ翻译:Your user group 30% là doanh nghiệp,70% là miễn phí.
3. Một tuyến đường giảm chất lượng 2% nhưng tiết kiệm 40%. đó là một con tàu?
   Trung ngữ: một đường dẫn giảm chất lượng 2% nhưng tiết kiệm 40%── giá trị lên đường?
4. Thực hiện kiểm tra sự tin cậy bằng cách sử dụng logprobs từ OpenAI / Anthropic API.
   Trung文翻译: sử dụng OpenAI / Anthropic API của logprobs 实现置信度检查──什么值触发升级?
5. Trong vòng 6 tháng, tỷ lệ leo thang tăng từ 8% lên 22%. Chẩn đoán 3 nguyên nhân và khắc phục cho mỗi nguyên nhân.

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Model routing | "cost broker" | Dynamic choice of model per request |
| Model cascade | "cheap-first escalate" | Run cheap, fall through to frontier on low confidence |
| Pre-route | "classify first" | Classifier up front; no re-run |
| Ensemble route | "parallel pick" | Run multiple, reward-model picks best |
| Escalation rate | "uprouted %" | Fraction of cascade requests that escalated |
| RouteLLM | "LMSYS router" | OSS router library |
| Not Diamond | "commercial router" | SaaS model-routing product |
| Drift | "cheap creep" | Distribution shift without router noticing |
| Online quality gate | "live check" | Automated LLM-judge sampling live traffic |

## Xem thêm 延伸阅读

- [AbhyashSuchi — Model Routing LLM 2026 Best Practices](https://abhyashsuchi.in/model-routing-llm-2026-best-practices/)
- [Lukas Brunner — Rise of Inference Optimization 2026](https://dev.to/lukas_brunner/the-rise-of-inference-optimization-the-real-llm-infra-trend-shaping-2026-4e4o)
- [RouteLLM paper / code](https://github.com/lm-sys/RouteLLM)
- [Not Diamond — model routing](https://www.notdiamond.ai/)
- [OpenRouter](https://openrouter.ai/) Gateway đa mô hình với các nguyên thủy định tuyến.
