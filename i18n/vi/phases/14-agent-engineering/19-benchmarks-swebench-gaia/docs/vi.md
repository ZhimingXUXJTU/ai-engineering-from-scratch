# Định hướng: SWE-bench, GAIA, AgentBench 基准测试 GAIA

> Ba điểm chuẩn đánh giá các đại lý neo vào năm 2026. SWE-bench kiểm tra mã patching. GAIA kiểm tra việc sử dụng công cụ tổng quát. AgentBench kiểm tra lý luận đa môi trường. Biết thành phần của chúng, lịch sử ô nhiễm của chúng và những gì chúng không đo.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 06 (Tool Use) | **前置知识:** 见原文
**Time:** ~60 minutes | **时间:** 见原文

## Mục tiêu học tập

- Tên gọi dây thừng thử nghiệm của SWE-bench (FAIL_TO_PASS) và giải thích lý do tại sao nó không được kiểm tra đơn vị.
- Giải thích lý do tại sao SWE-bench Verified (OpenAI, 500 nhiệm vụ) tồn tại và nó loại bỏ những gì.
- Mô tả thiết kế của GAIA: đơn giản cho con người, khó khăn cho AI; ba mức độ khó khăn.
- Tên tám môi trường của AgentBench và ngăn chặn chính của nó cho mã nguồn mở LLM.
- Kết luận về kết quả nhiễm SWE-bench+ và những tác động của nó.

## Vấn đề  vấn đề giới thiệu

Các bảng xếp hạng cho bạn biết mô hình nào thắng trên một điểm chuẩn.

> 排行榜 cho bạn biết mô hình nào thắng trên một nền tảng nào đó.

> SWE-bench và GAIA là hai cơ sở cốt lõi của Agent 能力.SWE-bench  đánh giá khả năng sửa đổi mã, GAIA  đánh giá khả năng suy luận chung.

- Nếu chỉ số chuẩn bị bị ô nhiễm (solution trong dữ liệu đào tạo, rò rỉ thử nghiệm).
- Nếu chỉ số chuẩn đo lường những gì bạn quan tâm (định nghĩa so với duyệt web so với tổng thể).
- Liệu người đánh giá có mạnh mẽ hay không (sự phù hợp của AST, kiểm tra nhà nước, đánh giá của con người).


> **【中文解读】**SWE-bench và GAIA là hai điểm quan trọng nhất của năm 2026 Agent 能力基准。SWE-bench 评估 Agent 修复真实 GitHub issue 的能力(软件工程)。GAIA 评估 Agent 回答需要多步推理和工具使用的复杂问题的能力──通用推理──两者共同定义 Agent 的能力边界──

> **{【拓展：SWE-bench (Princeton, 2023) 包含 2,294 个真实 GitHub is...】}**SWE-bench (Princeton, 2023) 包含 2,294 个真实 GitHub issue,Agent 必须在真实代码库中定位 bug、编写修复并通过测试──2026 年 SOTA 是 72% 解决率(OpenAI 的 Codex) ・GAIA (Meta, 2023) 包含 2,294 个真实 GitHub issue,Agent 必须在真实代码库中定位 bug、编写修复并通过测试──2026 年 SOTA 是 72% 解决率(OpenAI 的 Codex) ・GAIA (Meta, 2023) 包含 466 个问题需要 web 搜索、文件处理、代码执行等工具──人类平均 92% ,最佳代理约70%──
Biết ba điểm chuẩn neo và các chế độ thất bại của chúng trước khi bạn trích dẫn một số.

> Trước khi trích dẫn dữ liệu, hãy hiểu được ba bài kiểm tra cơ bản này và mô hình thất bại của nó.

>  **【前置】**建议先过:Phase 14·06(Tận dụng công cụ)  hiểu Agent 如何调用工具是看懂 GAIA的前提;以及基本的"机器学习评估方法论"精度/回忆"",污染") 测试集泄漏──如果你引用过模型基准,但不知道污染是什么,本节必须学──

## Khái niệm cốt lõi

### SWE-bench (Jimenez et al., ICLR 2024 uống)

- 2.294 lỗi GitHub thực sự từ 12 bộ nhớ Python phổ biến.
- Trình tác viên nhận: cơ sở mã tại commit trước + mô tả vấn đề ngôn ngữ tự nhiên.
- Thuộc nhân sản xuất: một vá.
- Thử nghiệm: áp dụng bản vá, chạy bộ thử nghiệm của repo. Bản vá phải lật lại các thử nghiệm FAIL_TO_PASS (trước đây thất bại, bây giờ vượt qua) mà không phá vỡ các thử nghiệm PASS_TO_PASS.

SWE-agent (Yang et al., 2024) đạt 12,5% khi phát hành bằng cách nhấn mạnh giao diện đại lý- máy tính (pháp lệnh biên tập tập tệp, tổng hợp tìm kiếm mô hình hiểu).

>  **【类比】**SWE-bench 像考"开卷实操": cho Agent một thư viện mã thực tế 描述 考题) 、一套已有的单元测试 评分标准) ―― Agent 像人类工程师一样读代码定位 bug、写补丁、跑测试──**关键设计**:测试用 FAIL_TO_PASS(修复前失败、修复后通过) + PASS_TO_PASS(không thể phá hủy đã có chức năng), Dujujin"修复 A 破了 B"的伪通过──

> SWE-agent(Yang等,2024) đạt 12,5% trong thời gian phát hành, thông qua nhấn mạnh vào giao tiếp máy tính-agent-documented.

> SWE-bench và GAIA là hai cơ sở cốt lõi của Agent 能力.SWE-bench  đánh giá khả năng sửa đổi mã, GAIA  đánh giá khả năng suy luận chung.

### SWE-bench Verified

OpenAI, tháng 8 năm 2024. Bộ phận 500 nhiệm vụ do con người điều chỉnh. loại bỏ các vấn đề mơ hồ, thử nghiệm không đáng tin cậy và nhiệm vụ mà sự khắc phục không rõ ràng. Điểm chuẩn chính cho "có đại lý của bạn gửi các bản vá thực sự không?"

> OpenAI,2024 年 8 月── 500 个任务子集 of artificial策划──移除模糊问题──不可靠的测试和修复不明任务──"Hội ngũ của bạn có thể giao hàng sửa chữa thực sự không?"

> SWE-bench và GAIA là hai cơ sở cốt lõi của Agent 能力.SWE-bench  đánh giá khả năng sửa đổi mã, GAIA  đánh giá khả năng suy luận chung.

### Ô nhiễm

- Hơn 94% các vấn đề của SWE ban trước hầu hết các model cắt giảm.
- **SWE-bench+**thấy 32,67% các bản vá thành công đã rò rỉ các giải pháp trong văn bản vấn đề (chương tự đã thấy sự sửa chữa trong mô tả), và 31,08% là đáng ngờ do bảo hiểm thử nghiệm kém.
- Được xác minh sạch hơn nhưng không bị ô nhiễm.

Hướng dẫn thực tế: mô hình có điểm 50% trên SWE-bench có thể đạt điểm 35% trên SWE-bench+. Luôn báo cáo cả hai nếu bạn tuyên bố hiệu suất SWE-bench.

> ️ **【易错点】**引用 SWE-bench 分数时不提 Được xác minh/SWE-bench+。**后果**Trong khi đó có 32% là "động thái trong vấn đề 文本里看到了答案" (trong nhiễm) ⋅ Đây là "虚高分数" phổ biến nhất trong vòng AI ⋅**一行修复**: bất kỳ trích dẫn SWE-bench số字时, phải đồng thời cung cấp xác minh 子集分数和 SWE-bench+(去污染版) 分数,注明数据来源日期。

> 实际影响: một mô hình trên SWE-bench 上 score 50% trên SWE-bench + 上 chỉ có thể nhận được 35% 👇 Nếu bạn tuyên bố SWE-bench  hiệu suất, xin hãy bắt buộc phải báo cáo cùng lúc cả hai 👇

> SWE-bench và GAIA là hai cơ sở cốt lõi của Agent 能力.SWE-bench  đánh giá khả năng sửa đổi mã, GAIA  đánh giá khả năng suy luận chung.

### GAIA (Mialon et al., Nov 2023)

- 466 câu hỏi; 300 được giữ lại cho bảng xếp hạng tư nhân tại huggingface.co/gaia-benchmark.
- Triết lý thiết kế: "từ quan điểm đơn giản cho con người (92%) nhưng khó khăn cho AI (GPT-4 với plugin: 15%). "
- Thử lý lý luận, đa phương pháp, web, sử dụng công cụ.
- Ba mức độ khó khăn; cấp độ 3 đòi hỏi chuỗi công cụ dài trên các phương pháp.

GAIA là những gì bạn chạy để đo "capacity tổng quát". Đừng nhầm lẫn với các chuẩn mực cụ thể về mã.

> GAIA là một cách để đo lường cơ sở của "capacity general".

> SWE-bench và GAIA là hai cơ sở cốt lõi của Agent 能力.SWE-bench  đánh giá khả năng sửa đổi mã, GAIA  đánh giá khả năng suy luận chung.

### AgentBench (Liu et al., ICLR 2024)

- 8 môi trường trên mã (Bash, DB, KG), trò chơi (Alfworld, LTP), web (WebShop, Mind2Web), và thế hệ mở.
- Nhiều vòng quay, khoảng 4k-13k vòng quay mỗi chia.
- Kết quả chính: lý luận dài hạn, ra quyết định và hướng dẫn sau đây là những rào cản cho các LLM OSS bắt kịp thương mại.

### Những gì chúng không đo

- Chi phí hoạt động trong thế giới thực (tokens, wall-clock).
- Hành vi an toàn trong điều kiện đối kháng.
- Hiệu suất trên miền của bạn ( Sử dụng đánh giá của riêng bạn, Bài học 30).
- Các lỗi đuôi (tỷ lệ chuẩn trung bình; các nhà khai thác sản xuất quan tâm đến 1% tồi tệ nhất).

### Khi đánh giá so sánh đi sai

- **Single-number fixation.**SWE-bench 50% cho bạn biết ít hơn chi phí P50/P75/P95 + phân phối bước.
- **Contaminated claims.**Báo cáo SWE-bench mà không đề cập đến Verified hoặc SWE-bench+ là sai lầm.
- **Benchmark-as-development-target.**Việc tối ưu hóa cho chỉ số chuẩn khác với lợi ích sản xuất.

> 🤔 **【困惑】**Q: SWE-bench Verified 上 70% + mô hình đã xuất hiện, có phải nói rằng các kỹ sư phần mềm phải thất nghiệp không? A: 还早──三个原因:(1) vấn đề của SWE-bench đều là vấn đề "có rõ ràng thử nghiệm sử dụng trường hợp、 có rõ ràng tái hiện đường" được hình thành tốt, trong sản xuất 50% vấn đề không được đáp ứng;(2) 70% có nghĩa là mỗi 3 nhiệm vụ thất bại 1 , sản xuất môi trường thất bại sửa chữa chi phí cao hơn lợi nhuận của sửa chữa thành công;(3)**生产代码库比 SWE-bench 的 12 个开源 Python 仓库复杂得多**私有代码、跨语言、几十年遗留代码──Bênchmark trên 70% không bằng với 70% môi trường sản xuất──

> **单一数字执念。**SWE-bench 50%  nói cho bạn thông tin ít hơn P50/P75/P95 成本 + 步骤分布──
> **污染声明。**报告 SWE-bench 时不提及 Được xác minh hoặc SWE-bench+ là sai lầm.
> **基准作为开发目标。**Để cơ sở tối ưu hóa sẽ chuyển hướng từ sản xuất thực dụng.

## Hãy xây dựng nó.
```figure
ae-swebench-gate
```

## Hãy xây dựng nó

`code/main.py`thiết lập một dây thắt toy SWE-bench-like:

> `code/main.py`实现 một công cụ thử nghiệm đồ chơi giống như SWE-bench:

> SWE-bench và GAIA là hai cơ sở cốt lõi của Agent 能力.SWE-bench  đánh giá khả năng sửa đổi mã, GAIA  đánh giá khả năng suy luận chung.

- Nhiệm vụ sửa lỗi tổng hợp (3 nhiệm vụ).
- Một "hội nhân" có kịch bản đề xuất các bản vá.
- Một người chạy thử nghiệm kiểm tra FAIL_TO_PASS (thói lỗi đã được sửa chữa) và PASS_TO_PASS (không có gì bị hỏng).
- Một phân loại khó khăn theo kiểu GAIA dựa trên độ sâu phân hủy câu hỏi.

Đi đi.

```
python3 code/main.py
```

Kết quả xuất hiện cho thấy tỷ lệ giải pháp cho mỗi nhiệm vụ + cho mỗi khó khăn và làm cho các quy tắc đánh giá cụ thể.

> 输出 cho thấy tỷ lệ giải quyết của mỗi nhiệm vụ và từng cấp độ khó khăn, và làm cho các quy tắc của máy đánh giá được cụ thể hóa.

> SWE-bench và GAIA là hai cơ sở cốt lõi của Agent 能力.SWE-bench  đánh giá khả năng sửa đổi mã, GAIA  đánh giá khả năng suy luận chung.

## Hãy sử dụng nó để thực hiện

- **SWE-bench Verified**luôn báo cáo điểm xác minh.
- **GAIA**dùng phân chia bảng xếp hạng tư nhân.
- **AgentBench**cho so sánh đa môi trường.
- **Custom evals**(Dân học 30) cho hình dạng thực tế của sản phẩm của bạn.

## Chuyển nó đi.

`outputs/skill-benchmark-harness.md`xây dựng một vòng xoáy kiểu SWE-bench cho bất kỳ cặp công việc mã cốt lõi nào với cửa FAIL_TO_PASS / PASS_TO_PASS.

> `outputs/skill-benchmark-harness.md`Đối với bất kỳ bộ thư ký mã nào, nhiệm vụ xây dựng một công cụ thử nghiệm kiểu SWE-bench, với FAIL_TO_PASS / PASS_TO_PASS 门控.

> SWE-bench và GAIA là hai cơ sở cốt lõi của Agent 能力.SWE-bench  đánh giá khả năng sửa đổi mã, GAIA  đánh giá khả năng suy luận chung.

## Tập luyện bài tập

1. Đưa dây đeo đồ chơi chạy trên một repo thực sự (đưa ra một trong số của bạn).
  Trung ngữ翻译:思考并实践此练习。
2. Thêm một số liệu đếm từng bước. Trong 3 nhiệm vụ của bạn, bao nhiêu bước của đại lý cho mỗi giải pháp?
  Trung ngữ翻译:思考并实践此练习。
3. Đọc bài báo SWE-bench +. Thực hiện kiểm tra rò rỉ giải pháp (chọn mẫu phù hợp với văn bản vấn đề so với sự khác biệt).
  Trung ngữ翻译:思考并实践此练习。
4. Tải xuống câu hỏi của GAIA từ công chúng, theo dõi những gì một đặc vụ lớp GPT-4 sẽ làm.
  Trung ngữ翻译:思考并实践此练习。
5. Đọc phân tích môi trường của AgentBench. Môi trường nào phản ánh bề mặt sản phẩm của bạn?
  Trung ngữ翻译:思考并实践此练习。

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| SWE-bench | "Code agent benchmark" | 2,294 GitHub issues; patch must flip FAIL_TO_PASS tests |  |
| SWE-bench Verified | "Clean SWE-bench" | 500 human-curated tasks, OpenAI |  |
| FAIL_TO_PASS | "Fix gate" | Tests previously failing that must pass after the patch |  |
| PASS_TO_PASS | "No-regression gate" | Tests that were passing and must still pass |  |
| GAIA | "Generalist benchmark" | 466 human-easy / AI-hard multi-tool questions |  |
| AgentBench | "Multi-env benchmark" | 8 environments; long-horizon multi-turn |  |
| Contamination | "Training-set leak" | Benchmark tasks present in model training |  |
| SWE-bench+ | "Contamination audit" | 32.67% solution leakage found in successful SWE-bench patches |  |

## Xem thêm 延伸阅读

- [Jimenez et al., SWE-bench (arXiv:2310.06770)](https://arxiv.org/abs/2310.06770) chỉ số chuẩn ban đầu
  Trung ngữ: 翻译:见原文.
- [OpenAI, SWE-bench Verified](https://openai.com/index/introducing-swe-bench-verified/) bộ phận được chọn lọc
  Trung ngữ: 翻译:见原文.
- [Mialon et al., GAIA (arXiv:2311.12983)](https://arxiv.org/abs/2311.12983) điểm chuẩn chung
  Trung ngữ: 翻译:见原文.
- [Liu et al., AgentBench (arXiv:2308.03688)](https://arxiv.org/abs/2308.03688) Suite đa môi trường
  Trung ngữ: 翻译:见原文.
