# Phát triển nhân viên Eval-Driven

> Lời chỉ dẫn của Anthropic: "bắt đầu với các lời khuyên đơn giản, tối ưu hóa chúng bằng đánh giá toàn diện, và chỉ thêm nhiều hệ thống hành động khi cần thiết".

**Type:** Learn + Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** All of Phase 14. | **前置知识:** 见原文
**Time:** ~60 minutes | **时间:** 见原文

>  **【前置】**Học本节前请先掌握:Phase 14·01-29 全部本节是Phase 14 的综合应用──还需要Phase 11·10(Hán đánh giá) 的基础──本节是Phase 14·26(Failure Modes) 的"预防版"用 eval 提前发现失败模式──

## Mục tiêu học tập

- Tên gọi ba lớp đánh giá  điểm chuẩn tĩnh, tùy chỉnh ngoại tuyến, sản xuất trực tuyến  và mỗi lớp là gì.
- Giải thích vòng lặp chặt chẽ của đánh giá-optimizer.
- Mô tả các thực tiễn tốt nhất năm 2026: đánh giá sống bên cạnh mã, chạy trong CI, PR cổng.
- Kết nối mỗi bài học giai đoạn 14 với trường hợp đánh giá mà nó tạo ra.

## Vấn đề  vấn đề giới thiệu

Các đại lý vượt qua các bản demo. Họ thất bại trong sản xuất theo cách mà các bản demo không thể dự đoán. Các điểm chuẩn trả lời "có mô hình này có khả năng rộng rãi không?" không phải "hợp tác viên này đang vận chuyển các bản vá phù hợp cho sản phẩm của tôi không?" Câu trả lời: đánh giá ở ba lớp, chạy liên tục, với mỗi khung và quy tắc được học được được lập bản đồ cho một trường hợp đánh giá.

>  **【类比】**Agent eval 像给运动员做体检3 个层级:(1) **静态基准**(SWE-bench、BFCL) =国家体能测试,比平均水平;**定制离线 eval**= đối với thiết kế dự án của bạn (((ví dụ như "đường thành công của sửa lỗi này") = đội trong tập luyện;(3) **在线生产 eval**= thực tế người dùng phản=A/B 测试──三层缺一不可

> ️ **【易错点】**Cảnh sát đánh giá của 3 个坑:(1) **只测 happy path**eval 集全是简单查询,复杂情况没覆盖;务必构构造对抗性 测试(模糊指令、攻击、边界值)**eval 不进 CI** phát triển时手工跑一次就过,上线后没人跑;eval 必须进 GitHub Actions,PR 不过 eval 不能合并──(3) **eval 集污染**eval 数据混进快速的少数shot示例,分数虚高;eval 数据严格隔离──

> Trưởng lý đã vượt qua cuộc biểu diễn. Chúng thất bại trong quá trình sản xuất bằng cách không thể đoán trước. Đáp chuẩn là "Có khả năng rộng lớn của mô hình này không?" thay vì "Trưởng lý này có phải đang cung cấp các bổ sung chính xác cho sản phẩm của tôi không?" Đáp trả lời là: ba cấp đánh giá, hoạt động liên tục, mỗi bảo trì và các quy tắc học tập đều được mô tả thành một ví dụ đánh giá.


> **【中文解读】**评估驱动的代理 开发(Eval-Driven Development) sẽ được sử dụng trong công trình phần mềm truyền thống TDD 应用于 Agent:先定义评估标准,再实现 Agent。 thách thức cốt lõi là sự không chắc chắn của Agent Các đầu vào tương tự có thể tạo ra các đường thực hiện và đầu ra khác nhau, cần dựa trên đánh giá dựa trên quỹ đạo chứ không phải dựa trên đánh giá nhanh.

> **{【拓展：Eval-Driven Agent Development 是 2025-2026 年的最佳实践。核...】}**Phát triển đại lý Eval-Driven là thực hành tốt nhất trong năm 2025-2026  Công cụ cốt lõi: 1) AgentOps Agent 追踪和评估平台; 2) LangSmith LangChain 评估套件; 3) Braintrust AI 评估框架.
## Khái niệm cốt lõi

### Ba lớp đánh giá

1. **Static benchmarks** SWE-bench Được xác minh cho mã (Dạy học 19), WebArena/OSWorld cho duyệt web / máy tính để bàn (Dạy học 20), GAIA cho người nói chung (Dạy học 19), BFCL V4 cho việc sử dụng công cụ (Dạy học 06). Sử dụng cho so sánh và khép lại giữa các mô hình.

2. **Custom offline evals** hình dạng của sản phẩm của bạn:
   - LLM như một thẩm phán (Langfuse, Phoenix, Opik  Bài học 24).
   - Dựa trên thực hiện (cái vá chạy, kiểm tra kiểm tra).
   - Dựa trên quỹ đạo (so sánh các chuỗi hành động với vàng; OSWorld-Human cho thấy các đại lý hàng đầu 1,4-2.7x so với vàng).

3. **Online evals** sản xuất:
   - Các phiên lặp lại (Langfuse).
   - Các cảnh báo được kích hoạt bởi guardrail (Dân học 16, 21).
   - Theo dõi chi phí / độ trễ từng bước (Dạy học 23 OTel trải dài).

### Tỷ lệ của các loại hình:

- Lòng vòng chặt chẽ:

1. Proposer tạo ra đầu ra.
2. Các thẩm phán đánh giá.
3. Tốt hơn cho đến khi kiểm tra viên vượt qua.

Đây là tự tinh chỉnh (Dạy 05) tổng quát. Bất kỳ dòng chảy đại lý nào bạn quan tâm có thể được gói trong đánh giá tối ưu hóa cho độ tin cậy.

> Đây là sự phổ biến của tự tinh chỉnh. Bất kỳ hành động nào bạn quan tâm đều có thể được sử dụng để tăng độ tin cậy.

> 评估驱动的代理 开发(Eval-Driven Development) sẽ được đánh giá như là cốt lõi của Agent 开发.

### 2026 thực hành tốt nhất

- Evals sống bên cạnh code.
- Đi báo cáo mọi chuyện.
- Gate hợp nhất trên điểm đánh giá (ví dụ: "không có sự lùi > 5% so với chính").
- Mỗi đường dây bảo vệ đều được xem xét.
- Mỗi quy tắc được học (Tình phản, quy tắc học tập thuận lợi cho dòng công việc) lập bản đồ cho trường hợp thất bại.

### Kết nối giai đoạn 14

Mỗi bài học trong giai đoạn 14 tạo ra các trường hợp đánh giá:

| Lesson | Eval case it generates |
|--------|------------------------|
| 01 Agent Loop | Budget-exhausted, infinite-loop guard |
| 02 ReWOO | Planner replans correctly when a tool fails |
| 03 Reflexion | Learned reflections apply on retry |
| 05 Self-Refine/CRITIC | Judge passes refined output |
| 06 Tool Use | Argument coercion works; unknown tools rejected |
| 07-10 Memory | Retrieval citations match sources; stale facts invalidate |
| 12 Workflow Patterns | Each pattern produces correct output |
| 13 LangGraph | Resume reproduces state exactly |
| 14 AutoGen Actors | DLQ catches crashed handlers |
| 16 OpenAI Agents SDK | Guardrail trips on the right inputs |
| 17 Claude Agent SDK | Subagent results return to orchestrator |
| 19-20 Benchmarks | SWE-bench Verified score, WebArena success rate, OSWorld efficiency |
| 21 Computer Use | Per-step safety catches injected DOM |
| 23 OTel | Spans emit required attributes |
| 26 Failure Modes | Detectors tag known failures |
| 27 Prompt Injection | PVE refuses poisoned retrievals |
| 28 Orchestration | Supervisor routes to the right specialist |
| 29 Runtime Shapes | DLQ handles N% failure |

Nếu bộ đánh giá của bạn có các trường hợp cho mỗi người, bạn đã bao gồm giai đoạn 14.

> Nếu bộ đánh giá của bạn có từng trường hợp sử dụng của mỗi khóa học, bạn đã bao gồm giai đoạn 14.

> 评估驱动的代理 开发(Eval-Driven Development) sẽ được đánh giá như là cốt lõi của Agent 开发.

### Khi phát triển dựa trên đánh giá thất bại

- **No baseline.**Evals không có một cái tốt cuối cùng được biết là không thể đọc được.
- **LLM-judge without grounding.**Các thẩm phán cũng ảo giác. mô hình CRITIC (Dạy 05)  thẩm định các lý do trên các công cụ bên ngoài.
- **Over-fitting to evals.**Tích cực cho đánh giá khác với hữu ích sản xuất.
- **Flaky evals.**Các trường hợp không xác định gây ra báo động sai.

> **没有基线。**Không có đánh giá tốt nhất được biết là không thể đọc được.
> **LLM 评审器没有基础。**评审器也会幻觉──CRITIC 模式(第 5 课) 评审器 dựa trên các công cụ bên ngoài──
> **过拟合评估。**Để đánh giá sự tối ưu hóa sẽ được phân lập khỏi sản xuất thực dụng.
> **不稳定的评估。**Không xác định sử dụng trường hợp dẫn đến báo cáo sai lầm.

## Hãy xây dựng nó.
```figure
ae-eval-three-layers
```

## Hãy xây dựng nó

`code/main.py`là một vòng đánh giá stdlib:

- Danh sách trường hợp với các loại (chỉ số chuẩn, tùy chỉnh, trực tuyến).
- Một nhân viên kịch bản đang được kiểm tra.
- Loop đánh giá- tối ưu hóa: đề xuất, đánh giá, tinh chỉnh cho đến khi vượt qua hoặc tối đa vòng.
- Cổng CI: tỷ lệ vượt qua tổng cộng + sự lùi ngược so với đường cơ bản.

Đi đi.

```
python3 code/main.py
```

Kết quả: mỗi trường hợp vượt qua/không thành công, cờ quay lại, phán quyết CI gate.

> 输出: mỗi trường hợp thông qua/ thất bại 归归标志 CI 门控裁定

> 评估驱动的代理 开发(Eval-Driven Development) sẽ được đánh giá như là cốt lõi của Agent 开发.

## Hãy sử dụng nó để thực hiện

- Viết các trường hợp đánh giá trong cùng một repo như mã đại lý của bạn.
- Hãy kiểm tra mọi thông tin liên lạc thông qua thông tin thông tin.
- Thất bại trong việc xây dựng về sự hồi quy.
- Theo dõi tốc độ vượt qua theo thời gian.
- Kết nối mọi thất bại sản xuất với một trường hợp mới.

## Chuyển nó đi.

`outputs/skill-eval-suite.md`xây dựng một bộ đánh giá ba lớp cho một sản phẩm đại lý với cổng CI và theo dõi trôi trở.

> `outputs/skill-eval-suite.md`Đối với các đại lý  sản phẩm xây dựng ba tầng đánh giá bộ, bao gồm CI 门控和回归追踪.

> 评估驱动的代理 开发(Eval-Driven Development) sẽ được đánh giá như là cốt lõi của Agent 开发.

## Tập luyện bài tập

1. Hãy lấy một trong những thất bại sản xuất của bạn, viết một trường hợp đánh giá mà tái tạo nó.
  Trung ngữ翻译:思考并实践此练习。
2. Xây dựng một chương trình thẩm phán LLM cho lĩnh vực của bạn với ba chiều (thực tế, âm thanh, phạm vi).
  Trung ngữ翻译:思考并实践此练习。
3. Chuyên chuyển bộ đánh giá vào CI. Thiết lập không thành công trên >=5% hồi quy.
  Trung ngữ翻译:思考并实践此练习。
4. Thêm một số liệu hiệu quả quỹ đạo: đại lý đã thực hiện bao nhiêu bước so với quỹ đạo vàng?
  Trung ngữ翻译:思考并实践此练习。
5. Hãy lập bản đồ từng bài học giai đoạn 14 cho một vụ đánh giá trong phòng của bạn.
  Trung ngữ翻译:思考并实践此练习。

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| Static benchmark | "Off-the-shelf eval" | SWE-bench, GAIA, AgentBench, WebArena, OSWorld |  |
| Custom offline eval | "Domain eval" | LLM-as-judge / exec / trajectory on your product shape |  |
| Online eval | "Production eval" | Session replay, guardrail alerts, cost/latency tracking |  |
| Evaluator-optimizer | "Propose-judge-refine" | Iterate until judge passes |  |
| CI gate | "Merge blocker" | Fail the build on eval regression |  |
| Baseline | "Last-known-good" | Reference score to detect regression |  |
| Trajectory efficiency | "Steps over gold" | Agent step count divided by human expert minimum |  |

## Xem thêm 延伸阅读

- [Anthropic, Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) "bắt đầu đơn giản, tối ưu hóa với các đánh giá"
  Trung ngữ: 翻译:见原文.
- [OpenAI, SWE-bench Verified](https://openai.com/index/introducing-swe-bench-verified/) chỉ số chuẩn được chọn lọc
  Trung ngữ: 翻译:见原文.
- [Berkeley Function Calling Leaderboard](https://gorilla.cs.berkeley.edu/leaderboard.html) Chỉ số chuẩn sử dụng công cụ
  Trung ngữ: 翻译:见原文.
- [Langfuse docs](https://langfuse.com/) đánh giá + lặp lại phiên trong thực tế
  Trung ngữ: 翻译:见原文.
