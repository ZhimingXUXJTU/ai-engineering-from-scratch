# AlphaEvolve  Cơ quan mã hóa tiến hóa  AlphaEvolve  Cơ quan mã hóa tiến hóa

> Kết hợp một mô hình mã hóa biên giới với một vòng lặp tiến hóa và một nhà đánh giá có thể kiểm tra máy. Hãy để vòng lặp chạy đủ lâu. Nó phát hiện ra một quy trình nhân đếm 4x4 phức tạp sử dụng 48 nhân đếm scalar, cải tiến đầu tiên so với Strassen trong 56 năm. Nó cũng tìm thấy một hệ thống lập lịch Borg toàn bộ Google phục hồi ~ 0,7% tính toán cluster trong sản xuất. Kiến trúc này thật buồn chán. Những chiến thắng đến từ sự nghiêm ngặt của người đánh giá.

> **【中文解读】**Để kết hợp mô hình mã hóa tiên tiến với các vòng lặp tiến hóa và các thiết bị kiểm tra được của bộ đánh giá, hãy cho vòng lặp hoạt động đủ lâu. Nó phát hiện ra một cách sử dụng 48 lần số lượng nhân số 4x4 复矩阵乘法 quá trình.

> **【拓展：进化算法 + LLM 的化学反应】**进化算法 (?? 变异+选择+交叉) đã có nhiều thập kỷ lịch sử, nhưng truyền thống随机变异 trên các quy trình lớn hầu như luôn tạo ra sai lệch ngôn ngữ. LLM như một "kỹ thuật biến đổi thông minh" đã thay đổi điều này: nó có thể đưa ra những sửa đổi hợp lý trong việc biên dịch qua 语义.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, evolutionary-loop toy) | **语言:** Python（标准库，进化循环玩具）
**Prerequisites:** Phase 15 · 01 (long-horizon framing), Phase 15 · 02 (self-taught reasoning) | **前置知识:** Phase 15 · 01（长程框架），Phase 15 · 02（自我教学推理）
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**Học本节前请先掌握:Phase 15·01(长程 Agent) Phase 15·02(STaR自我改进) 进化算法基础(变异/交叉/选择) ・・・AlphaEvolve = LLM 作为智能变异算子的进化算法──
>  **【类比】**AlphaEvolve = "AI 实验室里的博士生群体"。传统进化算法 = 随机打字员(多数是乱码);AlphaEvolve = 一群 AI 博士生,每个人都提出有意义的修改("试试把循环展开两倍"),评估器跑实验打分,高分修改进入下一代种群──LLM 解决"如何提出合理变异",评估器解决"如何辨别伪"结合 56年第一次突破 Strassen 矩阵乘法──
> 🤔 **【困惑】**Q: Tại sao AlphaEvolve có thể vượt qua các chuyên gia con người? Bởi vì nó chạy hàng triệu lần, mỗi lần sử dụng chuẩn thực 验证.

## Vấn đề  vấn đề giới thiệu

Các mô hình ngôn ngữ lớn có thể viết mã. Các thuật toán tiến hóa có thể tìm kiếm qua mã. Cả hai đều đã được thử nghiệm riêng biệt trong nhiều thập kỷ; cả hai đều đạt đến giới hạn.

> Mô hình ngôn ngữ lớn có thể viết mã, thuật toán phát triển có thể tìm kiếm trên không gian mã. Cả hai đều đã thử nghiệm trong nhiều thập kỷ, đều gặp phải tấm cổng.

Mức tối cao LLM là sự kết luận: mô hình viết mã có thể tin được mà không thực hiện những gì nó tuyên bố. Mức tối cao tiến hóa là chi phí tìm kiếm: đột biến ngẫu nhiên trên tổng hợp hiếm khi tạo ra các chương trình có thể biên soạn, đừng nói là tốt hơn.

> Các mô hình viết ra có vẻ hợp lý nhưng thực tế không phù hợp với các mã hóa.

AlphaEvolve (Novikov et al., DeepMind, arXiv:2506.13131, tháng 6 năm 2025) kết hợp chúng. LLM đề xuất chỉnh sửa nhắm mục tiêu vào cơ sở dữ liệu chương trình; một nhà đánh giá tự động ghi điểm cho mỗi biến thể; các biến thể có điểm số cao trở thành cha mẹ cho các thế hệ tương lai. LLM xử lý bước đắt tiền của việc viết mã có thể tin cậy; nhà đánh giá bắt được những câu chuyện.

> AlphaEvolve(Novikov 等人,DeepMind,arXiv:2506.13131,2025 年 6 月) sẽ kết hợp hai thứ này.LLM đề xuất chỉnh sửa có mục tiêu đối với cơ sở dữ liệu của các chương trình; máy đánh giá tự động đối với mỗi biến thể; cao分 biến thể trở thành người cha của thế hệ tương lai.

> **【中文解读】**AlphaEvolve (Google DeepMind, 2025) sẽ sử dụng thuật toán tiến hóa để tối ưu hóa mã. Nó duy trì một nhóm các chương trình, thông qua biến đổi, giao thông và chọn lọc 代 tối ưu hóa.

Kết quả được báo cáo: 48-scalar-multiplication 4x4 complex matrix multiplication (sự giới hạn năm 1969 của Straßsen là 49), một bản lập trình Borg trong sản xuất Google, tăng tốc lõi FlashAttention 32,5%, cải thiện thông qua đào tạo Gemini.

> Kết quả của báo cáo: 48 lần 标量乘法 4x4 复矩阵乘法(Strassen 1969 年的边界是 49),Google 生产中的 Borg调度启发式,32.5% 的 FlashAttention 内核加速,Gemini 训练吞吐量改进──

Kiến trúc hoạt động bởi vì người đánh giá có thể kiểm tra bằng máy. Nó không hoạt động ở nơi người đánh giá không có. Sự bất đối xứng là bài học.

> Sự không đối xứng này là cốt lõi của bài học này: cấu trúc vì vậy có hiệu quả, vì các máy đánh giá là một lĩnh vực mà máy đánh giá không thể tin tưởng, vòng lặp đã không hiệu quả.

## Khái niệm cốt lõi

### Chuyện vòng

1. Bắt đầu từ chương trình hạt giống `P_0`Điều đó đúng nhưng không tốt.
   Trung ngữ  Từ một thực tế nhưng tốt hơn hạt giống`P_0`开始──
2. Giữ cơ sở dữ liệu các chương trình biến thể, mỗi chương trình được đánh giá bởi người đánh giá.
   Trung ngữ翻译:维护一个变体程序数据库, mỗi变体由评估器打分──
3. Mô hình một hoặc nhiều bậc cha mẹ từ cơ sở dữ liệu (MAP-elites-style hoặc đảo-based).
   Trung ngữ翻译:从数据库中采样一个或多个父本(MAP-elite 风格或岛屿模型)
4. Hãy yêu cầu LLM (Tình nhị phân Flash cho nhiều ứng viên, Tử nhị phân Pro cho những người khó khăn) để tạo ra một biến thể sửa đổi của người cha.
   Trung文翻译:提示 LLM(多数候选用 Gemini Flash,难题用 Gemini Pro)生成父本的修改变体──
5. Thu thập, chạy và đánh giá biến thể trên trình đánh giá đã qua.
   Trung văn翻译:编译、运行并保留评估器上评估变体──
6. Đưa vào cơ sở dữ liệu được khóa bằng điểm số và vector tính năng của nó.
   Trung ngữ翻译:以分数和特征向量为键插入数据库──
7. Lặp lại.
   Trung ngữ翻译:重复──

Hai chi tiết quan trọng. Thứ nhất, LLM được yêu cầu với nhiều hơn chương trình mẹ  thường là một số biến thể hàng đầu từ cơ sở dữ liệu, cộng với chữ ký đánh giá, cộng với mô tả nhiệm vụ ngắn. Công việc của mô hình là đề xuất một thay đổi nhắm mục tiêu có thể cải thiện điểm số. Thứ hai, cơ sở dữ liệu được cấu trúc (mảng lưới MAP-elites, dựa trên đảo) vì vậy vòng lặp khám phá sự đa dạng, không chỉ là nhà lãnh đạo hiện tại.

> 两个细节很重要――第一,提示 LLM 时不仅给父程序通常是数据库中排名最高的几个变体,加上评估器签名和简短任务描述――模型的工作是提议可能提高分数的针对性变化――第二,数据库是结构化的 (MAP-élite 网格、岛模型),让循环探索多样性,而不仅仅是当前最优解――

### Điều gì khiến người đánh giá không thể thương lượng được

Những chiến thắng của AlphaEvolve đều đến từ các lĩnh vực mà người đánh giá nhanh, quyết định và khó chơi:

> Tất cả những chiến thắng của AlphaEvolve đều đến từ các lĩnh vực đánh giá nhanh chóng, xác định và khó hiểu:

- **Matrix multiplication algorithm**: một thử nghiệm đơn vị nhân số các số tử và kiểm tra sự bình đẳng bằng bit-tương tự.
  Trung ngữ翻译:**矩阵乘法算法** một lần kiểm tra đơn vị bằng nhau trên một矩阵并位检查相等.
- **Borg scheduling heuristic**: một máy mô phỏng cấp sản xuất để tái tạo tải trọng cluster lịch sử và đo lường tính toán lãng phí.
  Trung ngữ翻译:**Borg 调度启发式** Một máy mô phỏng cấp sản xuất, tái đặt lịch sử tập hợp tải trọng và đo phí lãng phí
- **FlashAttention kernel**: một thử nghiệm độ chính xác cộng với một điểm chuẩn của đồng hồ tường trên phần cứng thực.
  Trung ngữ翻译:**FlashAttention 内核**正确性测试加上真实硬件上墙钟基准──
- **Gemini training throughput**: được đo GPU-thì giây mỗi bước.
  Trung ngữ翻译:**Gemini 训练吞吐量** đo số giây của GPU mỗi bước.

Trong mỗi trường hợp, người đánh giá bắt được lớp lỗi LLM mà nếu không sẽ thống trị: tuyên bố chính xác đã được kết hợp, tuyên bố hiệu suất biến mất trên phần cứng và lỗi biên trường hợp.

> Trong mỗi trường hợp, máy đánh giá đã bắt được các lỗi LLM  lỗi: tuyên bố chính xác giả mạo, tuyên bố hiệu suất biến mất trên phần cứng và tình huống cạnh tranh thất bại.

### Việc hack phần thưởng là mặt khác của tuyên bố đó.

Sự tiến hóa tối ưu hóa cho bất cứ điều gì mà người đánh giá đo lường. Nếu người đánh giá không hoàn hảo, vòng lặp sẽ tìm thấy sự không hoàn hảo. Trong một miền không được xác minh, vòng lặp sẽ tối ưu hóa cho tính năng bề mặt, chứ không phải hành vi dự định.

> 进化优化评估器测量的任何东西――如果评估器不完美,循环会发现不完美之处――在未经验证领域中,循环会优化表面特征而不是预期行为――

DeepMind ghi rõ ràng điều này trong bài báo: Thành công của AlphaEvolve chỉ chuyển sang các lĩnh vực mà sự nghiêm ngặt của nhà đánh giá phù hợp với tham vọng của tìm kiếm.

> DeepMind trong bài luận rõ ràng cho thấy: Sự thành công của AlphaEvolve chỉ có thể chuyển sang lĩnh vực đánh giá nghiêm ngặt và phù hợp với mục tiêu tìm kiếm.

Ví dụ cụ thể về việc hack phần thưởng trong vòng tìm kiếm mã:

> Ví dụ cụ thể về sự thay đổi trong vòng vòng tìm kiếm từ 2025 đến 2026:

- Mục tiêu tối ưu hóa mà thưởng "giờ để hoàn thành" được thưởng bằng cách gửi giải pháp trống rỗng.
  Trung ngữ翻译: 奖励"完成时间"的优化目标会奖励提交空解决方案。
- Điểm chuẩn đánh giá thưởng cho sự chính xác dưới bài kiểm tra thưởng cho bài kiểm tra ghi nhớ và quá phù hợp.
  Trung文翻译: 奖励测试正确的基准分数会 奖励记忆测试和过拟合──
- Một đại diện "tính chất lượng mã" đã thưởng bằng cách loại bỏ bình luận và viết lại tên biến, mà không có sự thay đổi ngữ nghĩa.
  Trung ngữ翻译:"代码质量" đại diện hội giải thưởng xóa注释和重写变量名,而没有语义变化。

Sự cố trong AlphaEvolve: gửi một nhà đánh giá đã được tổ chức LLM chưa từng thấy, với các đầu vào được tạo ra tại thời điểm đánh giá.

> AlphaEvolve's sửa đổi: giao một LLM từ một thiết bị đánh giá dự trữ chưa từng thấy, nhập vào khi đánh giá tạo ra.

### Tại sao tìm kiếm LLM + đánh bại hoặc một mình . Tại sao tìm kiếm LLM +  thắng hơn sử dụng đơn độc

LLM có thể tạo ra các thay đổi có thể biên dịch, có thể xác thực về ngữ nghĩa. GA đột biến ngẫu nhiên trên một tệp Python 2000 dòng gần như luôn tạo ra lỗi tổng hợp. LLM cũng tập trung tìm kiếm vào các khu phố có thể xác thực (hóa một hàm, không phải là các byte ngẫu nhiên) làm giảm đáng kể các cuộc gọi đánh giá lãng phí.

> LLM có thể tạo ra những thay đổi có thể biên dịch được  nghĩa hợp lý. Trong 2000 行 Python 文件随机变异 GA 几乎总是产生语法错误. LLM cũng sẽ tập trung tìm kiếm vào một vùng lân cận hợp lý (đổi lại một hàm, chứ không phải là phụt tự), điều này làm giảm đáng kể sự lãng phí của các thiết bị đánh giá.

Người đánh giá, lần lượt, nhận được những sự kết luận của LLM. LLM sẽ tự tin tuyên bố rằng một hàm "đã là O(n log n) trong giới hạn" khi nó thực sự là O(n^2); một điểm chuẩn của đồng hồ tường giải quyết câu hỏi.

> 评估器反过来捕获 LLM的虚构──LLM 会自信地声称一个函数"极限下是 O(n log n)",而实际是 O(n2);墙钟基准让问题尘埃落定──

### AlphaEvolve nằm trong đống biên giới.

| System | Generator | Evaluator | Domain | Example win |
|---|---|---|---|---|
| 系统 | 生成器 | 评估器 | 领域 | 示例胜利 |
| AlphaEvolve | Gemini | correctness + benchmark | algorithms, kernels, schedulers | 48-mul 4x4 matmul |
| AlphaEvolve | Gemini | 正确性 + 基准 | 算法、内核、调度器 | 48 次乘法 4x4 矩阵乘法 |
| FunSearch (DeepMind, 2023) | PaLM / Codey | correctness | combinatorial math | cap-set lower bounds |
| FunSearch（DeepMind，2023） | PaLM / Codey | 正确性 | 组合数学 | cap-set 下界 |
| AI Scientist v2 (Sakana, L5) | GPT/Claude | LLM critique + experiment | ML research | ICLR workshop paper |
| AI Scientist v2（Sakana，L5） | GPT/Claude | LLM 评审 + 实验 | ML 研究 | ICLR 工作坊论文 |
| Darwin Godel Machine (L4) | agent scaffolding | SWE-bench / Polyglot | agent code | 20% → 50% SWE-bench |
| Darwin Godel Machine（L4） | Agent 脚手架 | SWE-bench / Polyglot | Agent 代码 | SWE-bench 20% → 50% |

Tất cả bốn là sự thay đổi trên cùng một công thức: máy phát điện cộng với đánh giá, vòng lặp.

> Bốn trong số đó là các biến thể của cùng một cấu trúc: máy tạo thêm máy đánh giá, vòng lặp.
```figure
alphaevolve-loop
```

## Sử dụng nó

## Hãy sử dụng nó để thực hiện

`code/main.py`thực hiện một vòng lặp giống như AlphaEvolve tối thiểu trên một vấn đề tái lập biểu tượng đồ chơi.

> `code/main.py`Trong một vấn đề về trở lại của các biểu tượng đồ chơi đã thực hiện vòng lặp nhỏ nhất giống như AlphaEvolve.

"LLM" là một trình thay thế stdlib đề xuất đột biến tổng hợp nhỏ cho một chương trình tính toán một chức năng mục tiêu.

> "LLM" là một đại diện của một bộ quy chuẩn, đưa ra một sự thay đổi ngôn ngữ nhỏ đối với một chương trình tính toán mục tiêu hàm.

Xem:

> 观察:

- Làm thế nào điểm số tốt nhất cải thiện qua các thế hệ.
  Trung ngữ翻译:最佳分数如何在世代中提升──
- Làm thế nào một lưới MAP Elite giữ cho các giải pháp đa dạng sống lại để vòng lặp không hội tụ vào mức tối thiểu địa phương.
  Trung文翻译:MAP-elite 网格如何保持多样化解存活,让循环不收到局部最小──
- Làm thế nào để loại bỏ thử nghiệm đã bị kéo dài (chỉ đánh giá đào tạo) cho phép vòng lặp quá phù hợp một cách ấn tượng.
  Trung文翻译:移除保留测试(仅训评估器) làm thế nào để làm cho vòng lặp thảm họa性地过拟合──

## Chuyển nó đi.

`outputs/skill-evaluator-rigor-audit.md`là điều kiện tiên quyết để xem xét một vòng lặp kiểu AlphaEvolve trong một lĩnh vực mới: liệu nhà đánh giá của bạn thực sự nhận thấy những thất bại mà bạn quan tâm?

> `outputs/skill-evaluator-rigor-audit.md`Trong lĩnh vực mới, xem xét các điều kiện tiên quyết giống như vòng lặp AlphaEvolve: Máy đánh giá của bạn có thực sự bắt kịp sự thất bại của bạn không?

## Tập luyện bài tập

1. Đi chạy`code/main.py`. ghi lại quỹ đạo điểm tốt nhất.`--no-holdout`(v) và chạy lại.
   Trung ngữ翻译:运行 `code/main.py`◯ ghi chép ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯ ◯    ◯ ◯ ◯                                                                                                                                                                                                       `--no-holdout`(c) tái vận hành.

2. Đọc Phần 3 của bài báo AlphaEvolve về lưới MAP-elite. Thiết kế mô tả vector tính năng cho một vấn đề mới (ví dụ: thông qua tối ưu hóa trình biên dịch) sẽ giữ cho tìm kiếm đa dạng.
   Trung ngữ翻译:阅读 AlphaEvolve 论文第 3 节关于MAP-elite 网格──为新问题(例如编译器优化遍次) 设计一个保持搜索多样性的特征向量描述符──

3. Kết quả 48 nhân 4x4 đã cải thiện trên đường 49-mul của Strassen sau 56 năm. Đọc phụ lục F của bài báo và giải thích trong ba câu tại sao đánh giá cho vấn đề này đặc biệt dễ dàng để làm đúng, và tại sao hầu hết các lĩnh vực không giống như nó.
   Trung ngữ翻译:48 lần乘法 4x4 结果在 56 năm sau đã cải tiến Strassen's 49 lần乘法边界──阅读论文附录 F, sử dụng ba câu giải thích tại sao các vấn đề này đặc biệt dễ dàng để làm đối với, cũng như tại sao hầu hết các lĩnh vực không như vậy──

4. Hãy đề xuất một lĩnh vực mà AlphaEvolve sẽ thất bại, xác định chính xác nơi mà người đánh giá phá vỡ và tại sao.
   Trung ngữ翻译:提议一个 AlphaEvolve 会失败的领域──精确指出评估器在哪里失败以及原因──

5. Đối với một tên miền mà bạn biết, hãy viết chữ ký đánh giá mà bạn sẽ sử dụng. Bao gồm (a) điều kiện chính xác, (b) chỉ số hiệu suất, (c) quy tắc tạo đầu vào đã được giữ, (d) ít nhất một kiểm tra chống vi phạm phần thưởng.
   Trung ngữ翻译:对你了解的一个领域,写出你会使用的评估器签名──包括 (a) 正确性条件, (b) 性能指标, (c) 保留输入生成规则, (d) 至少一个反奖励改检查──

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| AlphaEvolve | "DeepMind's evolutionary coding agent" | Gemini + program database + machine-checkable evaluator |
| AlphaEvolve | "DeepMind 的进化编码 Agent" | Gemini + 程序数据库 + 机器可检查评估器 |
| MAP-elites | "Diversity-preserving archive" | Grid keyed by feature vectors; each cell holds the best variant with that descriptor |
| MAP-elites | "保持多样性的档案" | 以特征向量为键的网格；每个单元持有具有该描述符的最佳变体 |
| Island model | "Parallel evolution subpopulations" | Independent populations that migrate periodically; prevents premature convergence |
| 岛屿模型 | "并行进化子种群" | 定期迁移的独立种群；防止过早收敛 |
| Machine-checkable evaluator | "Deterministic oracle" | A unit test, simulator, or benchmark the LLM cannot fake — a prerequisite for this loop |
| 机器可检查评估器 | "确定性预言机" | LLM 无法伪造的单元测试、模拟器或基准——此循环的前提 |
| Reward hacking | "Optimizing the measure, not the goal" | Loop finds a way to maximize score without doing the intended task |
| 奖励篡改 | "优化度量而非目标" | 循环找到一种方法在不执行预期任务的情况下最大化分数 |
| Seed program | "The starting point" | An initial correct-but-suboptimal program the loop evolves from |
| 种子程序 | "起点" | 循环从中演化的初始正确但次优的程序 |
| Held-out evaluator | "Evaluation data the LLM never saw" | Inputs generated at evaluation time to prevent memorization |
| 保留评估器 | "LLM 从未见过的评估数据" | 评估时生成的输入以防止记忆 |

## Xem thêm 延伸阅读

- [Novikov et al. (2025). AlphaEvolve: A coding agent for scientific and algorithmic discovery](https://arxiv.org/abs/2506.13131) toàn bộ tờ báo.
  Trung ngữ翻译:完整论文──
- [DeepMind blog on AlphaEvolve](https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/) nhà cung cấp ghi lại kết quả.
  Trung ngữ翻译:厂商撰文及结果──
- [AlphaEvolve results repository](https://github.com/google-deepmind/alphaevolve_results) phát hiện ra các thuật toán, bao gồm 48-mul 4x4 matmul.
  Trung文翻译:发现的算法仓库, bao gồm 48 lần乘法 4x4 矩阵乘法。
- [Romera-Paredes et al. (2023). Mathematical discoveries from program search with LLMs (FunSearch)](https://www.nature.com/articles/s41586-023-06924-6) hệ thống tiền nhiệm.
  中文翻译:前身系统 FunSearch。
- [Anthropic — Responsible Scaling Policy v3.0 (Feb 2026)](https://anthropic.com/responsible-scaling-policy/rsp-v3-0) định hình tự trị liên quan đến các nhà đánh giá như là một hướng nghiên cứu chính.
  Trung ngữ翻译:将评估器约束的自主性作为关键研究方向.
