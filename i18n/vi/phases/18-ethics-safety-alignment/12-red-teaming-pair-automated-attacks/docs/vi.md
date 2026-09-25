# Đội đỏ: PAIR và tấn công tự động

> Chao, Robey, Dobriban, Hassani, Pappas, Wong (NeurIPS 2023, arXiv:2310.08419). PAIR  Quick Automatic Iterative Refinement  là jailbreak hộp đen tự động. Một LLM tấn công với hệ thống yêu cầu nhóm đỏ lặp đi lặp lại đề xuất jailbreak cho LLM mục tiêu, tích lũy các nỗ lực và phản ứng trong lịch sử trò chuyện của riêng mình như phản hồi trong ngữ cảnh. PAIR thường thành công trong vòng 20 truy vấn, hiệu quả hơn GCG (sự tìm kiếm gradient cấp token của Zou et al.) và không yêu cầu truy cập hộp trắng. PAIR hiện là một đường cơ sở tiêu chuẩn trong JailbreakBench (arXiv:2404.01318) và HarmBench, cùng với GCG, AutoDAN, TAP và Persuasive Adversarial Prompt.

> **【中文解读】**Bài viết này giới thiệu phương pháp đánh giá an toàn của Red Team Testing hệ thống hóa, sử dụng tự động tấn công phát hiện AI 系统漏洞──PAIR(Prompt Automatic Iterative Refinement, NeurIPS 2023) là tiêu chuẩn tự động hóa hộp đen越狱: Attacker LLM 在红队系统提示下代提出越狱, thường trong 20 truy vấn thành công, hiệu quả cao hơn GCG vài số lượng và không cần truy cập hộp trắng──

> **【拓展：PAIR → GCG → 攻击家族谱系】**GCG(Zou 等人 2023) trong令牌级梯度搜索对抗后,需要白盒访问,产生不可读字符串;;PAIR 是黑盒的,产生自然语言攻击且可跨模型迁移;;AutoDAN 使用进化搜索,TAP 引入分支剪枝,PAP 编码人类服服技术;;JailbreakBench(100 有害行为) 和 HarmBench;;510 行为) đã chuẩn hóa đánh giá;;

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, mock PAIR loop against a toy target) | **语言:** Python（标准库，针对玩具目标的模拟 PAIR 循环）
**Prerequisites:** Phase 18 · 01 (instruction-following), Phase 14 (agent engineering) | **前置知识:** Phase 18 · 01 (指令遵循), Phase 14 (Agent 工程)
**Time:** ~75 minutes | **时间:** ~75 分钟

>  **【前置】**Học本节前请先掌握:Phase 18·01、Phase 14──PAIR = tự động hóa hộp đen越狱, tấn công LLM 代生成越狱 prompt──
>  **【类比】**PAIR = "AI tự động tìm lỗ hổng"――手工红队 = 人写越狱(慢);PAIR = 攻击 LLM 看目标 LLM 反应,代改进(通常20 查询内成功,比 GCG 快几个数量级) ――JailbreakBench/HarmBench 标准基线。

## Mục tiêu học tập

- Mô tả thuật toán PAIR: hệ thống tấn công nhanh chóng, tinh chỉnh lặp lại, phản hồi trong ngữ cảnh.

> 描述 PAIR 算法: kẻ tấn công hệ thống提示、代改进、上下文反──

- Giải thích tại sao PAIR hiệu quả hơn GCG khi mục tiêu là hộp đen.

> 解释 tại sao PAIR trong mục tiêu là hộp đen thì nghiêm ngặt hơn GCG hơn cao hiệu quả.

- Hãy nêu tên bốn đường cơ sở tấn công tự động khác (GCG, AutoDAN, TAP, PAP) và nêu một tính năng phân biệt của mỗi đường.

> 列出其他四种自动化攻击基线 (GCG,AutoDAN,TAP,PAP) và các đặc điểm riêng biệt của riêng mình.

- Mô tả các giao thức đánh giá JailbreakBench và HarmBench và "tỷ lệ thành công tấn công" có nghĩa là gì trong mỗi.

> Mô tả JailbreakBench và HarmBench  đánh giá thỏa thuận và ý nghĩa của "nhiều thành công tấn công" của riêng họ.

## Vấn đề  vấn đề

Red-teaming từng là một hoạt động thủ công. Một số lượng nhỏ các nhà kiểm tra chuyên gia xây dựng các lời nhắc đối kháng và theo dõi những lời nhắc nào hoạt động. Điều này không có quy mô: tỷ lệ thành công của cuộc tấn công cần một mẫu thống kê, và mục tiêu là một mục tiêu di chuyển với mỗi phiên bản mô hình. PAIR hoạt động hóa red-teaming như một vấn đề tối ưu hóa với mục tiêu hộp đen.

> 红队测试过去是手动活动――少数专家测试者构建对抗性提示并跟踪哪些有效――This cannot be extended: tỷ lệ thành công của cuộc tấn công cần thống kê mẫu, và mục tiêu của mỗi mô hình được phát hành đều thay đổi――PAIR sẽ biến Red Team test hoạt động thành vấn đề tối ưu hóa mục tiêu hộp đen――

## Khái niệm

> **【中文解读】**PAIR 算法流程:输入目标 LLM T、评判 LLM J、攻击者 LLM A、目标字符串 G、预算 K(通常 20 查询) 循环 k=1..K:A 根据目标和历史(提示,响应) đối với phát hành新提示 p_k;提交 p_k đến T 获得响应 r_k;J 评分; nếu số分超过值则停止;否则增加到历史继续;; NeurIPS 2023 结果: đối với GPT-3.5-turbo 和 Llama-2-7B-chat 攻击成功率 >50%,平均成功查询数在 10-20 范围内.

### Algoritm PAIR

Các đầu vào:
- Mục tiêu LLM T (chương trình chúng ta đang tấn công).
- Thẩm phán LLM J (đánh điểm xem câu trả lời là jailbreak hay không).
- Đội tấn công LLM A (những người tối ưu hóa đội đỏ).
- Đường mục tiêu G: "đưa lời [cảnh dẫn gây hại]".
- Ngân sách K (thường là 20 câu hỏi).

> 输入: mục tiêu LLM T(我们攻击的模型) 评判 LLM J(评分响应是否越狱) 攻击者 LLM A(红队优化器) 目标字符串 G("用[有害指令]响应") 预算 K(通常 20 查询) ⋅

Loop, cho k trong 1..K:
1. A được nhắc đến với mục tiêu G và lịch sử của (quá trình, phản ứng) cặp cho đến nay.
2. A phát ra một thông báo mới.
3. Đưa p_k đến T; nhận phản ứng r_k.
4. J ghi điểm (p_k, r_k) trên bàn thắng.
5. Nếu điểm >= ngưỡng, dừng  jailbreak tìm thấy.
6. Nếu không, thêm (p_k, r_k) vào lịch sử của A; tiếp tục.

> 循环 k=1..K:1. A 被提示目标 G 和历史(提示,响应) 对──2. A 发出新提示 p_k──3. 提交 p_k 到 T;接收响应 r_k──4. J 评分(p_k, r_k) ・・・5.

Kết quả thực nghiệm (NeurIPS 2023): > 50% tỷ lệ thành công của cuộc tấn công đối với GPT-3.5-turbo, Llama-2-7B-chat; trung bình các truy vấn thành công trong phạm vi 10-20

> Kết quả thực tế: NeurIPS 2023): đối với GPT-3.5-turbo、Llama-2-7B-chat  tấn công tỷ lệ thành công > 50%; số lượng truy vấn thành công trung bình nằm trong phạm vi 10-20 ⋅

### Tại sao PAIR hiệu quả

GCG (Zou et al. 2023) tìm kiếm các hậu tố token đối lập theo gradient; nó đòi hỏi truy cập mô hình hộp trắng và tạo ra hậu tố không thể đọc được. PAIR là hộp đen và tạo ra các cuộc tấn công ngôn ngữ tự nhiên chuyển qua các mô hình. Phản hồi trong bối cảnh của PAIR cho phép kẻ tấn công học hỏi từ mỗi từ chối; GCG không có tương đương (mỗi cập nhật mã thông báo mới phải khám phá lại tiến bộ trước đó).

> GCG 通过梯度搜索对抗性令牌后;需要白盒访问且产生不可读后──PAIR là hộp đen,产生可跨模型迁移的自然语言攻击──PAIR的上下文反让攻击者从每次拒绝中学习; GCG 没有等价机制──

### Các cuộc tấn công tự động liên quan

- **GCG (Zou et al. 2023, arXiv:2307.15043).**Tìm kiếm gradient cấp token cho hậu tố đối lập. hộp trắng, chuyển thể, tạo ra chuỗi không thể đọc được.

> **GCG（Zou 等人 2023）。**Làm cho các cấp độ tìm kiếm đối kháng sau ──白盒、可迁移、产生不可读字符串──

- **AutoDAN (Liu et al. 2023).**Tìm kiếm tiến hóa về các yêu cầu, được hướng dẫn bởi một mục tiêu hàng đầu.

> **AutoDAN（Liu 等人 2023）。**进化搜索提示, bởi trình độ mục tiêu hướng dẫn

- **TAP (Mehrotra et al. 2024).**Cây tấn công với cắt  nhánh nhiều triển khai kiểu PAIR.

> **TAP（Mehrotra 等人 2024）。**带剪枝的攻击树分支多个 PAIR式推出──

- **PAP (Zeng et al. 2024).**Các lời khuyên phản đối thuyết phục  mã hóa các kỹ thuật thuyết phục con người như các mẫu lời khuyên.

> **PAP（Zeng 等人 2024）。**Nói thuyết phục đối với thuyết phục sẽ được sử dụng để làm người thuyết phục

> **【拓展：ASR 指标 → 评估陷阱】**Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng: Ứng dụng:

### JailbreakBench và HarmBench

Cả hai (2024) chuẩn hóa đánh giá:

> 两者(2024) đã chuẩn hóa đánh giá:

- JailbreakBench (arXiv:2404.01318). 100 hành vi gây hại trong 10 danh mục chính sách OpenAI. Tỷ lệ thành công tấn công (ASR) như là thước đo chính.

> JailbreakBench: 100 个有害行为,横跨 10 个 OpenAI 政策类别──攻击成功率(ASR) như một chỉ số chính──需要一个评判者──

- HarmBench (Mazeika et al. 2024). 510 hành vi trong 7 loại, với các thử nghiệm tổn hại ngữ nghĩa và chức năng. So sánh 18 cuộc tấn công với 33 mô hình.

> HarmBench:510 个行为,横跨 7 个类别,包含语义和功能性危害测试──比较 18 种攻击对 33 模型──

ASR thường được báo cáo với một ngân sách truy vấn cố định. So sánh các cuộc tấn công đòi hỏi phải phù hợp ngân sách; 90% ASR tại 200 truy vấn không tương đương với 85% ASR tại 20.

> ASR thường được báo cáo dưới ngân sách truy vấn cố định                                                                                                                                                                                                                                                         

> **【中文解读】**2026 年部署意义:每个前沿实验室现在正在发布前对生产模型运行 PAIR 和 TAP──ASR轨迹出现模型卡(Lớp 26) 和安全案例附录(Lớp 18) 中──这不是特殊攻击它是标准基础设施──

### Lý do nó quan trọng cho các triển khai năm 2026

Mỗi phòng thí nghiệm biên giới hiện đang chạy PAIR và TAP đối với các mô hình sản xuất trước khi phát hành. Các quỹ đạo ASR xuất hiện trong thẻ mô hình (Dạy học 26) và phụ lục trường hợp an toàn (Dạy học 18).

> Mỗi phòng thí nghiệm tiên tiến hiện đang được phát hành trước khi phát hành đối với mô hình sản xuất chạy PAIR và TAP.

### Khi điều này phù hợp với giai đoạn 18

Bài học 12 là nền tảng tấn công tự động. Bài học 13 (Many-Shot Jailbreaking) là một hoạt động khai thác dài bổ sung. Bài học 14 (ASCII Art / Visual) là một cuộc tấn công mã hóa. Bài học 15 (Indirect Prompt Injection) là bề mặt tấn công sản xuất năm 2026. Bài học 16 bao gồm các đối tác công cụ phòng thủ (Llama Guard, Garak, PyRIT).

> Bài học 12 là cơ sở tự động hóa tấn công. Bài học 13 là sự bổ sung của longitude utilization. Bài học 14 là mã hóa tấn công. Bài học 15 là 2026 năm sản xuất tấn công. Bài học 16 bao gồm các công cụ phòng thủ.

> **【拓展：TAP 和 PAP → 攻击进化】**TAP(Mehrotra 等人 2024) thông qua phân支多 PAIR 式推出并剪枝扩展 PAIR更高ASR但更多计算──PAP(Zeng 等人 2024) sẽ đưa ra công nghệ thuyết phục của con người như một mô hình dụ── tấn công gia đình từ tìm kiếm hộp trắng của GCG tiến hóa đến tìm kiếm hộp đen của PAIR代 cải tiến, tiếp tục đến tìm kiếm cây của TAP và công trình xã hội của PAP mỗi thế hệ đều mạnh hơn ở các kích thước tấn công khác nhau──

## Sử dụng nó.
```figure
al-pair-loop
```

## Sử dụng nó

`code/main.py`mục tiêu là một phân loại giả mạo từ chối các lời nhắc "bất ngờ" gây hại (trình lọc từ khóa). Người tấn công là một nhà tinh chế dựa trên quy tắc thử định nghĩa, khung chơi vai và mã hóa. Thẩm phán ghi điểm phản ứng. Bạn xem kẻ tấn công thành công trong ~ 5-15 lặp lại chống lại bộ lọc từ khóa và thất bại chống lại bộ lọc ngữ nghĩa.

> `code/main.py`构建一个玩具 PAIR 循环──目标是拒绝"明显"有害提示的模拟分类器 (模拟分类器)  (关键词过) ──攻击者是尝试释义,角色扮演和编码的规则精化器──你可以看到攻击者在大约5-15次代中对关键词过成功,对语义过失败──

## Đưa nó lên mạng

Bài học này sẽ mang lại kết quả `outputs/skill-attack-audit.md`- Với một báo cáo đánh giá của nhóm đỏ, nó kiểm tra: những cuộc tấn công nào đã được thực hiện (PAIR, GCG, TAP, AutoDAN, PAP), với ngân sách nào mỗi cuộc tấn công, với thẩm phán nào, hành vi gây hại nào được thiết lập (JailbreakBench, HarmBench, nội bộ).

> 本课产 出 `outputs/skill-attack-audit.md` Định điểm báo cáo đánh giá của nhóm đỏ, kiểm toán: các cuộc tấn công nào đã được thực hiện; ngân sách của mỗi cuộc tấn công; sử dụng các thẩm phán nào; trong các tập hợp hành vi gây hại nào;

## Tập luyện bài tập

1. Đi chạy`code/main.py`- Đánh giá các yêu cầu trung bình cho thành công cho ba chiến lược tấn công tích hợp. Giải thích các giả định phòng thủ mục tiêu nào mỗi khai thác.

2. Thực hiện chiến lược tấn công thứ tư (ví dụ: dịch sang ngôn ngữ khác, mã hóa base64). báo cáo các yêu cầu trung bình mới để thành công đối với mục tiêu lọc từ khóa và mục tiêu lọc ngữ nghĩa.

3. Đọc Chao et al. 2023 Hình 5 (PAIR vs GCG so sánh). Mô tả hai kịch bản mà GCG được ưa thích mặc dù lợi thế hiệu quả của PAIR.

4. JailbreakBench báo cáo ASR đối với một mục tiêu cố định. Thiết kế một số liệu bổ sung đo đa dạng tấn công (phân biến trong các lời nhắc thành công). Giải thích tại sao đa dạng quan trọng đối với đánh giá phòng thủ.

5. TAP (Mehrotra 2024) mở rộng PAIR bằng cách nhánh + cắt.`code/main.py`và mô tả sự cân bằng giữa chi phí tính toán và tỷ lệ thành công.

## Từ khóa  Keyword

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| PAIR | "automated jailbreak" | Prompt Automatic Iterative Refinement; attacker-LLM + judge-LLM loop |
| GCG | "gradient jailbreak" | White-box token-level gradient search for adversarial suffixes |
| Attack success rate (ASR) | "% jailbreaks at k queries" | Primary metric; must be reported with query budget and judge identity |
| Judge LLM | "the scorer" | LLM that grades whether a response satisfies the harmful goal |
| JailbreakBench | "the evaluation" | Standardized harmful-behaviour set with tagged categories |
| HarmBench | "the broader bench" | 510 behaviours, functional + semantic harm tests |
| TAP | "tree of attacks" | PAIR with branching + pruning; better ASR at higher compute |

## Xem thêm 延伸阅读

- [Chao et al. — Jailbreaking Black Box LLMs in Twenty Queries (arXiv:2310.08419)](https://arxiv.org/abs/2310.08419) Tờ PAIR, NeurIPS 2023
- [Zou et al. — Universal and Transferable Adversarial Attacks on Aligned LLMs (arXiv:2307.15043)](https://arxiv.org/abs/2307.15043) Bảng giấy GCG
- [Chao et al. — JailbreakBench (arXiv:2404.01318)](https://arxiv.org/abs/2404.01318) Đánh giá tiêu chuẩn hóa
- [Mazeika et al. — HarmBench (ICML 2024)](https://arxiv.org/abs/2402.04249) đánh giá rộng hơn
