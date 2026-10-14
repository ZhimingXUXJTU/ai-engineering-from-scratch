# Các đại lý khác nhau thảo luận và hợp tác

> Du et al. (ICML 2024, "Society of Minds") chạy các trường hợp mô hình N độc lập đề xuất câu trả lời, sau đó lặp đi lặp lại chỉ trích lẫn nhau trên các vòng R để hội tụ.

**Type:** Learn + Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 12 (Workflow Patterns), Phase 14 · 05 (Self-Refine and CRITIC) | **前置知识:** 见原文
**Time:** ~60 minutes | **时间:** 见原文

## Mục tiêu học tập

- Giải thích giao thức thảo luận: N đề xuất, R vòng, hội tụ trên một câu trả lời chung.
- Hãy mô tả tại sao tranh luận giúp cải thiện tính thực tế, tuân thủ quy tắc và lý luận.
- Giải thích topology hiếm: không phải mọi người tranh luận cần phải nhìn thấy nhau.
- Thực hiện một cuộc tranh luận về một LLM kịch bản với các biến thể đầy đủ và hiếm; đo chi phí token so với độ chính xác.

## Vấn đề  vấn đề giới thiệu

Tự tinh chỉnh (Dạy 05) là một mô hình tự phê bình bản thân  rủi ro tư duy nhóm. CRITIC (Dạy 05) căn cứ phê bình trong các công cụ bên ngoài  không luôn có sẵn.

> Tự tinh tế (第 5 课) là một mô hình tự phê bình  tồn tại风险的群体思维;;CRITIC;;第 5 课) sẽ phê bình dựa trên các công cụ bên ngoài并非总是可用──辩论引入第三种模式:多个实例、交叉批评、通过分歧达成收收──

>  **【前置】**学本节前请先掌握:Phase 14·05(Self-Refine / CRITIC) 辩论是自我精炼的多实例扩展,不理解"一个模型自我批评为什么会陷入群体思维"就看不出辩论为什么需要 N个实例;Phase 14·12(Workflow Patterns) 理解管弦工作者和监督员工模式,本节的中心和讲话拓就是监督员的具体实现.


> **【中文解读】**Nhiều đại lý 辩论 bằng cách cho nhiều trường hợp LLM thảo luận về cùng một vấn đề từ các góc độ khác nhau để nâng cao chất lượng lý luận.

> **{【拓展：多 Agent 辩论是 2023-2025 年的研究热点。Du et al. (2023) 证明两个...】}**Du et al. (2023) chứng minh hai trường hợp tranh luận ChatGPT có thể cải thiện đáng kể tỷ lệ xác thực suy đoán. Thực hành năm 2026 cho thấy, 3-5 tác dụng tranh luận của một đại lý tốt nhất là thiếu đa dạng, quá ít dẫn đến chi phí phối hợp quá cao.
## Khái niệm cốt lõi

### Hiệp hội tâm trí (Du et al., ICML 2024)

>  **【类比】**多 Agent 辩论像学术同行评审:你写论文(N=3 个独立作者各写一版)→ 投稿后 3 个审稿人读对方的版本写回复(R 轮交叉批评)→ 作者根据回复 修改 → 几轮后论文收──关键洞察:单个作者会自信写错(Sự tinh tế của nhóm suy nghĩ),3 个独立作者挑错彼此更容易出幻觉──但全连接(每读者所有者) 审稿成本是O(N2) 所以会议"区域主席 +审稿人"的星形拓(hub-and-spoke),审稿人只使用和沟通,成本降至O(N) 

- N các trường hợp mô hình độc lập đề xuất câu trả lời cho cùng một câu hỏi.
- Trong vòng R, mỗi mô hình đọc và chỉ trích các đề xuất của những người khác.
- Các mô hình cập nhật câu trả lời của họ dựa trên các lời chỉ trích.
- Sau vòng R, trả lại câu trả lời hội tụ.

Các thí nghiệm ban đầu sử dụng N=3, R=2 do chi phí. Độ chính xác được cải thiện với nhiều đại lý và nhiều vòng hơn trên các vấn đề khó khăn (MMLU, GSM8K, Chess Move Validity, sinh nhật).

> Nhiều đại lý  tranh luận bằng cách cho phép nhiều đại lý đưa ra cùng một vấn đề và các quan điểm khác nhau của luận án để nâng cao chất lượng suy luận.

Các kết hợp giữa các mô hình vượt qua các cuộc tranh luận mô hình đơn: ChatGPT + Bard cùng > hoặc một mình.

> 跨模型组合胜过单一模型辩论:ChatGPT + Bard một khởi điểm tốt hơn bất kỳ một người nào.

> Nhiều đại lý  tranh luận bằng cách cho phép nhiều đại lý đưa ra cùng một vấn đề và các quan điểm khác nhau của luận án để nâng cao chất lượng suy luận.

### Topology Sparse

"Cải thiện cuộc tranh luận đa đại lý với Topology truyền thông Sparse" (arXiv:2406.11776, 2024-2025) cho thấy cuộc tranh luận toàn lưới không phải lúc nào cũng tối ưu. Các topology Sparse (những ngôi sao, vòng, trung tâm và đầu mối) có thể phù hợp với độ chính xác với chi phí token thấp hơn. Mỗi người tranh luận chỉ thấy một nhóm nhỏ các đồng nghiệp.

> "Cải thiện cuộc tranh luận đa đại lý với Topology Truyền thông Sparse" (ArXiv:2406.11776, 2024-2025) cho thấy toàn bộ cuộc tranh luận liên kết không phải là luôn luôn tốt nhất.

> Nhiều đại lý  tranh luận bằng cách cho phép nhiều đại lý đưa ra cùng một vấn đề và các quan điểm khác nhau của luận án để nâng cao chất lượng suy luận.

Những tác động:

- Mạng lưới đầy đủ N=5, R=3 = 5 × 3 = 15 đề xuất, mỗi đọc 4 đồng nghiệp = 60 phê bình.
- Star N=5, R=3 (một hub + 4 phát âm) = 15 đề xuất, phát âm chỉ đọc hub = 12 hoạt động phê bình.

### Khi tranh luận giúp ích

- **Factuality.**Trong các đề xuất độc lập, kiểm tra chéo làm giảm ảo giác.
- **Rule-following.**Chess move validity  một mô hình bỏ lỡ một quy tắc, những người khác bắt được nó.
- **Open-ended reasoning.**Nhiều khung hình hạn chế về câu trả lời đúng.

### Khi tranh luận đau đớn

- **Latency-sensitive UX.**N × R vòng hàng loạt là độ trễ mà bạn có thể không có.
- **Cost-sensitive scale.**N × R token cho mỗi câu hỏi.
- **Simple factual lookups.**Một lần tìm kiếm rẻ hơn năm cuộc tranh luận.

### 2026 các trường hợp thực tế

- **Anthropic orchestrator-workers**(Dân học 12)  một biến thể của cuộc tranh luận với một bước tổng hợp.
- **LangGraph supervisor**(Dạy 13)  router trung tâm + các đại lý chuyên môn có thể thực hiện tranh luận như một nút.
- **OpenAI Agents SDK**(Dạy 16)  các đại lý chuyển về phía trước và về phía sau để phê bình lặp lại.
- **Multi-agent evals** cuộc tranh luận đôi + đánh giá-optimizer cho tín hiệu đánh giá.

### Khi mô hình này đi sai

> 🤔 **【困惑】**Q: 辩论到底什么时候值得使用?N×R's delay and cost look very high? A: chỉ sử dụng trong trường hợp "một mô hình sai lầm một lần có giá cao hơn rất nhiều so với chi phí辩论"  Hình thức phán xét: chi phí辩论 = N×R× một lần suy luận chi phí; một mô hình sai lầm dự kiến mất = 误率 × một lần sai lầm mất.  Khi code tạo ra một lần lỗi vào sản xuất = 几十万损失)  Luật văn hóa thực tế kiểm tra, chẩn đoán y tế những trường hợp này, một mô hình nào cũng có 95% 准确率 cũng có được N=3,R=2 辩论 đưa ra tỷ lệ chính xác lên đến 99%  "天气 như thế nào" "hãy sử dụng tôi kết nối thư" như vậy là một lần tổng số lỗi của người dùng truy vấn, một lần辩论 

- **Convergence collapse.**Tất cả các nhân viên đều tụ tập với câu trả lời sai đầu tiên.
- **Hub failure.**Trong một topology sao, một trung tâm xấu làm hỏng tất cả mọi người.
- **Prompt homogenization.**Tất cả các đại lý đều sử dụng cùng một lời nhắc; họ tạo ra những câu trả lời tương tự.

> **收敛崩溃。**Tất cả các đại lý nhận được một câu trả lời sai lầm đầu tiên.
> **中心故障。**Trong một khu vực hình thành sao, một trung tâm xấu sẽ làm ô nhiễm tất cả mọi người.
> **提示同质化。**所有 Agent sử dụng cùng một gợi ý; tạo ra cùng một câu trả lời.

## Hãy xây dựng nó.

> ️ **【易错点】**场景: nhà phát triển sử dụng cùng một prompt  khởi động 5 người tranh luận  thí dụ mong đợi " đa dạng quan điểm " → 后果:5 个例 đưa ra gần như cùng một câu trả lời (甚至相同的错误), tranh luận rơi vào N 倍成本的自我精炼, gọi là " homogenization nhanh chóng " → 修复: 要么 sử dụng mô hình khác nhau (GPT-4o + Claude + Gemini,异构带来真分歧), 要么 đưa cho mỗi người tranh luận khác nhau vai trò () 快速"你是怀疑论者""你是乐观派""你是细节核查员"), 应么 ít nhất là nhiệt độ cơ hội hóa.
```figure
debate-converge
```

## Hãy xây dựng nó

`code/main.py`thực hiện cuộc tranh luận STDlib:

- `Debater`lớp (được viết LLM với mỗi người tranh luận suy nghĩ).
- `FullMeshDebate`và `SparseDebate`Những người chạy.
- Ba câu hỏi: một câu hỏi thực tế, một câu hỏi dựa trên quy tắc, một câu hỏi lý luận.
- Các số liệu: đáp ứng hội tụ, vòng để hội tụ, tổng quan điểm.

Đi đi.

```
python3 code/main.py
```

Kết quả: độ chính xác và chi phí cho mỗi giao thức; các trận đấu ít kết hợp đầy đủ trên 2/3 câu hỏi với chi phí thấp hơn.

> 输出: độ chính xác và chi phí của mỗi giao dịch; hiếm khi mở rộng trên 2/3 vấn đề để chi phí thấp hơn phù hợp với toàn bộ kết nối.

> Nhiều đại lý  tranh luận bằng cách cho phép nhiều đại lý đưa ra cùng một vấn đề và các quan điểm khác nhau của luận án để nâng cao chất lượng suy luận.

## Hãy sử dụng nó để thực hiện

- **Anthropic orchestrator-workers**cho các cuộc tranh luận đơn giản của 2-3 công nhân.
- **LangGraph**cho cuộc tranh luận đa vòng với kiểm soát.
- **Custom**cho nghiên cứu hoặc đảm bảo chính xác chuyên môn.

## Chuyển nó đi.

`outputs/skill-debate.md`Đặt một cuộc tranh luận đa đại lý với topology có thể cấu hình, N, R, và một quy tắc hội tụ.

> `outputs/skill-debate.md`Lập ra một số đại lý có thể được cấu hình ∞ N∞ R 和收 quy tắc 辩

> Nhiều đại lý  tranh luận bằng cách cho phép nhiều đại lý đưa ra cùng một vấn đề và các quan điểm khác nhau của luận án để nâng cao chất lượng suy luận.

## Tập luyện bài tập

1. Thực hiện quy tắc "sự bất đồng buộc": trong vòng 1, mỗi người tranh luận phải đưa ra một đề xuất riêng biệt.
  Trung ngữ翻译:思考并实践此练习。
2. Thêm một tổng hợp cân bằng sự tin tưởng: những người tranh luận trả lại (câu trả lời, tin tưởng); tổng hợp cân bằng sự tin tưởng.
  Trung ngữ翻译:思考并实践此练习。
3. Thay đổi một "hợp tác viên" cho một LLM khác với kịch bản khác với ý kiến khác nhau.
  Trung ngữ翻译:思考并实践此练习。
4. Đánh giá giá mã thông báo cho toàn bộ lưới so với thưa thớt trên 3 câu hỏi của bạn.
  Trung ngữ翻译:思考并实践此练习。
5. Đọc bài báo của Hội tâm trí. Đưa đồ chơi của bạn đến N=5, R=3.
  Trung ngữ翻译:思考并实践此练习。

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| Debate | "Multi-agent critique" | N proposers, R rounds of cross-critique, converge |  |
| Full mesh | "Everyone reads everyone" | Every debater reads every peer each round |  |
| Sparse topology | "Limited peer view" | Debaters read only a subset of peers |  |
| Hub-and-spoke | "Star topology" | One central debater, N-1 spokes read only the hub |  |
| Convergence | "Agreement" | Debaters converge on a shared answer |  |
| Society of Minds | "Du et al. debate paper" | ICML 2024 multi-agent debate method |  |

## Xem thêm 延伸阅读

- [Du et al., Society of Minds (arXiv:2305.14325)](https://arxiv.org/abs/2305.14325) tranh luận đa tác nhân
  Trung ngữ: 翻译:见原文.
- [Sparse Communication Topology (arXiv:2406.11776)](https://arxiv.org/abs/2406.11776) Kết quả topology hiếm
  Trung ngữ: 翻译:见原文.
- [Anthropic, Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) người tổ chức nhạc công như một biến thể tranh luận
  Trung ngữ: 翻译:见原文.
- [Madaan et al., Self-Refine (arXiv:2303.17651)](https://arxiv.org/abs/2303.17651) Phụng đồng minh tự phê bình mô hình đơn
  Trung ngữ: 翻译:见原文.
