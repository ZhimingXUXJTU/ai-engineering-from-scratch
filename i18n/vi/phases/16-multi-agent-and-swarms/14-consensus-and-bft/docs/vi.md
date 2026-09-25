# Nhận đồng thuận và sự dung nạp lỗi của Byzantine đối với các đặc vụ

> Các hệ thống phân tán cổ điển BFT đáp ứng LLM stochastic. Trong năm 2025-2026 ba hướng nghiên cứu đã xuất hiện: **CP-WBFT**(arXiv:2511.10400) cân nhắc mỗi phiếu bằng một cuộc điều tra tin tưởng; **DecentLLMs**(arXiv:2507.14928) đi không có lãnh đạo với các đề xuất công nhân song song và tổng hợp hình học-đối trung; **WBFT**(arXiv:2505.05103) kết hợp bỏ phiếu cân nhắc với Cluster Structure Hierarchical để chia các nút Core và Edge. Kết quả thực tế thực nghiệm từ "Can AI Agents Agree?" (arXiv:2603.01213) là ngay cả thỏa thuận quy mô là mỏng manh ngày nay  một đại lý lừa đảo duy nhất có thể làm tổn hại một hỗn hợp các đại lý. BFT là cần thiết nhưng không đủ. Bài học này xây dựng một giao thức BFT tối thiểu, tiêm ba cuộc tấn công cụ thể của các đại lý (sự dối trá Byzantine, sự phù hợp sycophantic, đồng văn hóa lỗi liên quan), và đo lường cách mỗi biến thể đồng thuận đối phó như thế nào.

> **【中文解读】**Bài này giới thiệu về sự đồng ý và cách đạt được sự đồng thuận trong trường hợp có thể có sự cố hoặc hành vi xấu.

> **【拓展：consensus and bft→具体应用】**拜占庭容错 (BFT) trong nhiều Agent 系统中的应用:当部分 Agent 可能故障或被攻击时,如何确保系统整体正确?经典 BFT 算法 (PBFT) cần 3f+1 个节点容忍 f 个故障节点―― trong LLM Agent 上下文中,'故障' có thể là ảo giác, được tiêm hoặc từ chối thực hiện―― thực tế sử dụng đa số bỏ phiếu như đơn giản hóa BFT──


**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib) | **语言:** Python（标准库）
**Prerequisites:** Phase 16 · 07 (Society of Mind and Debate), Phase 16 · 13 (Shared Memory) | **前置知识:** Phase 16 · 07（心智社会与辩论），Phase 16 · 13（共享内存）

>  **【前置】**学本节前请先掌握:Phase 16·07(辩论) Phase 16·13(共享内存) 分布式系统 BFT(PBFT、Raft)  Lệnh "故障" của Đại lý LLM =幻觉、被注入、拒绝执行。
>  **【类比】**BFT = "bộ thẩm phán bỏ phiếu nhưng phải phòng thủ trong hồn"。经典 BFT = 容忍 1/3 节点说谎(PBFT 3f+1);LLM 版 = 加权投票(按置信度) + 几何中位数聚合 + 层级聚类。三类攻击:拜占庭说谎、附和、相关错误(同一基模型 全错)。结论:BFT cần thiết nhưng không đầy đủ, "Can AI Agents Agree?"论文显示单一欺骗 Agent 就能破坏混合-of-Agents。
**Time:** ~75 minutes | **时间:** ~75 分钟

##                                                                                                                                                                                                                                                               

Bạn có các đại lý LLM N mỗi sản xuất một câu trả lời. Họ không đồng ý. Phần lớn bỏ phiếu chọn sai bởi vì hai đại lý có liên quan (những mô hình cơ sở tương tự, dữ liệu đào tạo tương tự, các chế độ thất bại tương tự). Một đại lý thứ ba xảy ra sai một cách mới lạ  do đó đa số là đa số sai.

> Bạn có N 个 LLM Agent, mỗi người đều tạo ra một câu trả lời. Chúng không phù hợp. Phần lớn bỏ phiếu chọn câu trả lời sai, vì hai Agent là liên quan.

Bây giờ thêm một tác nhân lừa dối: nó nằm cố ý. hoặc một tác nhân đồng cảm: nó đồng ý với ai nói cuối cùng. Trong BFT cổ điển, giả định là các nút Byzantine là một phần nhỏ.`f < n/3`thực tế là các nút LLM là stochastic ngay cả khi trung thực, tương quan giữa các mô hình, và bị ảnh hưởng bởi kết quả của nhau. Bạn không thể đối xử với họ như cử tri Bernoulli độc lập.

> 现在加入一个欺骗性代理:它故意撒谎――或一个性代理:它同意最后发言人的意见―― 在经典BFT中,假设占占庭节点占占占比`f < n/3`Và hành vi tùy ý. Thực tế của năm 2026 là, LLM 节点 ngay cả khi trung thực cũng là tự nhiên, liên quan đến các mô hình, và chịu ảnh hưởng của các sản phẩm của nhau. Bạn không thể coi chúng là cử tri độc lập.

BFT cổ điển (PBFT, 1999) không sai  nó không đầy đủ. Nó xử lý chuyển đổi bit tùy ý. Nó không xử lý "ba đại lý trung thực chia sẻ ảo giác vì họ chia sẻ dữ liệu đào tạo". Bài học này xây dựng từ nền tảng và lớp của PBFT trên ba sự thích nghi 2025-2026.

> 经典 BFT(PBFT, 1999)并非错它是不完整的──它处理任意位翻转──但它不处理"三个诚实代理因为共享训练数据产生相同的幻觉"──本课程从PBFT的基础上发发,叠加三个2025-2026年改进──

## Khái niệm cốt lõi

### BFT cổ điển cho bạn

Thực tế Biệt Vị Thể Thoả Thận Phụng (Castro & Liskov, OSDI 1999) `f < n/3`Các nút Byzantine. Các giao thức có ba giai đoạn (sẵn sàng, chuẩn bị, cam kết) và hai nguyên thủy (tin nhắn ký kết, chứng chỉ số số lượng).`n >= 3f + 1`các nút trung thực hay độc hại.

> 实用拜占庭容错(Castro & Liskov, OSDI 1999) `f < n/3`个拜占庭节点──协议 có ba giai đoạn (prepreparatment、preparation、commit) và hai ngôn ngữ gốc (signing消息、仲裁证书)`n >= 3f + 1`个诚意或恶意节点之间就单一价值达成一致.

Các bảo đảm là mạnh mẽ nhưng giả định:

> Những đảm bảo này rất mạnh mẽ, nhưng giả sử:

1. **Independent faults.**Người Byzantine không phối hợp.
   Trung ngữ翻译:**独立故障。**拜占庭节点不协调──
2. **Honest nodes are truly honest.**Sự chính xác của các kết quả trung thực là một vấn đề không có vấn đề; giao thức chỉ phù hợp với sự bất đồng.
   Trung ngữ翻译:**诚实节点真正诚实。**Sự thật là sự thật không phải là vấn đề; thỏa thuận chỉ xử lý sự phân biệt.
3. **The question has a ground-truth answer.**Sự đồng thuận về một sự thật sai lầm vẫn là sự đồng thuận.
   Trung ngữ翻译:**问题有标准答案。**Sự đồng ý về những sự thật sai lầm vẫn là sự đồng ý.

Các đại lý LLM vi phạm cả ba. Hai đại lý chạy cùng một mô hình cơ bản chia sẻ sai lầm. Một LLM "sự thật" vẫn ảo giác. Và trên những câu hỏi mơ hồ, "thực" là những gì các đại lý quyết định  không có lời tiên tri bên ngoài.

> Trưởng lý LLM 违反了所有三个假设――运行两个相同基础模型的特工 共享故障――"诚实的" LLM 仍然会产生幻觉――在模糊的问题上,"真相"由特工决定没有外部预言机――

### Ba vụ tấn công đặc biệt của LLM

**Byzantine lie.**Một đại lý đưa ra một câu trả lời sai lầm cố ý.`f < n/3`- Tôi không biết.

> **拜占庭撒谎。**Một đại lý 输出故意错误的答案... Nếu `f < n/3`, BFT cổ điển có thể xử lý.

**Sycophantic conformity.**Một đại lý đọc câu trả lời của người khác trước khi bỏ phiếu và phù hợp với người nói cuối cùng. Không có ý hại, nhưng tương quan với giọng nói lớn nhất. BFT cổ điển không ngăn chặn điều này bởi vì đại lý vượt qua mọi kiểm tra chữ ký.

> **谄媚从众。**Một đại lý trước khi bỏ phiếu đọc câu trả lời của đại lý khác, và giữ nguyên sự đồng thuận với người phát biểu cuối cùng. Không có ý xấu, nhưng liên quan đến tiếng nói lớn nhất.

**Correlated-error monoculture.**Ba đại lý chia sẻ một mô hình cơ bản. Họ ảo giác cùng một câu trả lời sai. Phần lớn sai. BFT cổ điển không giúp vì cả ba "thực sự" đồng ý.

> **相关错误单一文化。**Ba đại lý chia sẻ một mô hình cơ bản. Chúng tạo ra những sai lầm giống nhau.

### Các câu trả lời 2025-2026

**CP-WBFT**(arXiv:2511.10400)  BFT có trọng lượng được chứng minh bởi sự tin tưởng. Mỗi cử tri gắn một cuộc thăm dò tin tưởng vào câu trả lời của mình (một xác suất tự báo cáo hoặc dự đoán của mô hình hiệu chuẩn riêng).

> **CP-WBFT**(arXiv:2511.10400) sự tin cậy tìm kiếm tăng quyền BFT── mỗi cử tri cho câu trả lời của mình thêm một sự tin cậy tìm kiếm( tự báo cáo tỷ lệ, hoặc dự đoán mô hình độc lập chuẩn bị)── quyền bỏ phiếu tăng theo sự tin cậy giảm── báo cáo trên toàn bộ biểu đồ có +85.71% của BFT  cải tiến── nhằm mục đích  các biện pháp giảm thiểu từ người dân  từ đại lý 倾向于自动提出立场信任较低)──

**DecentLLMs**(arXiv:2507.14928)  Không có lãnh đạo. Các nhân viên lao động đề xuất song song, các nhân viên đánh giá ghi điểm các đề xuất, câu trả lời cuối cùng là trung bình hình học của các vị trí được ghi điểm.`f < n/2`. Giảm thiểu cho: Sự dối trá của Byzantine và các lỗi tương quan (đường trung bình hình học là mạnh mẽ đến các điểm ngoại lệ và kéo về phía cluster dày đặc, không phải là trung bình dựa trên mô hình).

> **DecentLLMs**(arXiv:2507.14928)  Không có nhà lãnh đạo                                                                                                                                                                                                                                                       `f < n/2`时稳健.                                                                                                                                                                                                                                                             

**WBFT**(arXiv:2505.05103)  BFT được cân nhắc với Clustering cấu trúc hàng bậc. Nên phiếu bầu được gán theo chất lượng phản ứng cộng với điểm tin cậy học được từ lịch sử. Các đại lý cluster vào Core và Edge; Các đại lý cốt phải đạt được sự đồng thuận trước, các đại lý Edge tiếp theo. Giảm thiểu cho: khả năng mở rộng (Core consensus là nhỏ và nhanh chóng) và một phần cho monoculture (Core có thể được chọn cho sự đa dạng).

> **WBFT**(arXiv:2505.05103) 带层次结构聚类的加权 BFT;; quyền bỏ phiếu được phân phối bởi chất lượng phản ứng cộng với số lượng tin tưởng được học từ lịch sử;.将 Agent 聚类为核心和边缘;核心 Agent 必须先达成共识,边缘 Agent 跟随;;针对可扩展性的缓解措施(核心共识小而快) 和部分针对单一文化的缓解;;核心可以选择多样性) 

### Phương pháp kinh nghiệm: "Các đại lý AI có thể đồng ý không?" (arXiv:2603.01213)

Các giấy đo lường sự đồng thuận quy mô (những đại lý LLM đồng ý về một giá trị số duy nhất) trên nhiều mô hình biên giới.

> Bài viết này đo lường sự phù hợp của các tiêu chuẩn trên nhiều mô hình phía trước.

- Ngay cả khi không có đối thủ, các đại lý LLM không đồng ý về các câu hỏi quy mô ở mức cao hơn 30% trên nhiều tiêu chuẩn.
  Trung ngữ: ngay cả khi không có đối thủ, LLM Agent trong nhiều thử nghiệm chuẩn bị trên tỷ lệ không phù hợp với các vấn đề về khối lượng vượt quá 30%.
- Một đại lý duy nhất áp dụng một nhân vật lừa dối có thể rút ra sự đồng thuận của Mixture of Agents 40+ điểm phần trăm khỏi đường cơ bản trung thực.
  Trung ngữ翻译: Sử dụng một đại lý cá nhân lừa đảo có thể hỗn hợp đại lý 共识偏离诚实基线 40 个百分点以上.
- Tỷ lệ bất đồng tương quan với sự đa dạng mô hình  các tập hợp đa dạng không đồng ý nhiều hơn so với các tập hợp đồng nhất (tốt: sai lầm không tương quan) nhưng cũng lôi kéo chậm hơn (xấu: thời gian dài hơn để đạt được thỏa thuận).
  Trung ngữ翻译:不一致率与模型多样性相关异构集成比同构集成不一致更多(好:不相关错误),但漂移更慢(坏:更长的一致达成时间)。

Điểm rút ra: BFT cung cấp cho bạn một thiết bị để sắp xếp các kết quả, nhưng nó không cho bạn biết liệu kết quả sắp xếp có đúng hay không.

> Kết luận:BFT cung cấp cơ chế xuất khẩu đối diện, nhưng không nói cho bạn biết liệu xuất khẩu đối diện có đúng không.

### Các giao thức cốt lõi, được tháo dỡ

Một vòng BFT tối thiểu cho các đại lý LLM:

```
1. task arrives; each agent i produces answer a_i
2. each agent attaches confidence probe c_i in [0, 1]
3. aggregator collects (a_i, c_i) from all n agents
4. aggregator groups by semantic cluster (equivalent answers)
5. aggregator computes weight for each cluster C:
     w(C) = sum_{i in C} c_i
6. winner = cluster with max weight, if max > threshold * sum(c_i)
   else: retry or escalate
7. minority clusters logged with provenance for post-hoc audit
```

Bước cụm hợp ngữ là sự xoay quanh cụm LLM. Hai câu trả lời "báo cáo nghiên cứu 4,2%" và "bảo tiến 4,2%" là cùng một cụm.

> 语义聚类步骤是 LLM đặc biệt sáng tạo. Hai câu trả lời" nghiên cứu báo cáo 4.2%" và"4.2% cải tiến" là cùng một ── đơn giản của các chuỗi phác thảo như kiểm tra sẽ bỏ qua điểm này. Trong sản xuất, sử dụng mô hình nhúng rẻ tiền hoặc quy định rõ ràng.

### Định hướng ngưỡng

- `threshold`các thông số cho phép bạn chấp nhận khi nào và khi nào để thử lại. quá thấp: bạn chấp nhận đa số yếu. quá cao: bạn không bao giờ chấp nhận bất cứ điều gì.`n=5-7`đại lý, cao hơn cho nhỏ hơn `n`- Ở dưới ngưỡng, leo thang lên một con người hoặc một nhóm đặc vụ khác.

> `threshold`参数决定何时接受、何时重试──太低:接受弱多数──太高:永远不接受任何东西── trải nghiệm phạm vi:`n=5-7`个 Agent 时为0.5-0.67,较小的 `n`时更高. 低于值. 时更高. 低于值. 升级给人类或不同的代理集合.

### Khi sự đồng thuận không giúp ích

- **Ambiguous questions.**Nếu câu hỏi không có sự thật cơ bản thì sự đồng thuận là một ý kiến.
  Trung ngữ翻译:**模糊问题。**Nếu vấn đề không có câu trả lời tiêu chuẩn, đồng ý là ý kiến.
- **Compound questions.**"Thiết mã và giải thích nó"  hai câu trả lời.
  Trung ngữ翻译:**复合问题。**"编写代码并解释"两个答案――分别独立投票――
- **Adversarial multi-round.**Nếu các đại lý có thể quan sát các vòng trước và bắt chước (debat Du 2023), họ bắt đầu đồng ý với nhau bất kể sự thật.
  Trung ngữ翻译:**对抗性多轮。**Nếu đại lý có thể quan sát trước vài vòng并模仿 (Dú 2023 辩论), chúng sẽ không thể thực sự đồng ý với nhau.

## Hãy xây dựng nó.
```figure
swarm-consensus-wave
```

## Hãy xây dựng nó

`code/main.py`thực hiện:

- `AgentVoter` một chính sách được viết kịch bản với (phản hồi, sự tự tin).
  Trung ngữ翻译:`AgentVoter` 带有(答案,置信度) của kịch bản chiến lược.
- `MajorityVote` đa dạng cổ điển.
  Trung ngữ翻译:`MajorityVote` 经典多数投票──
- `CPWBFT` Đánh phiếu dựa trên sự tin tưởng với phân nhóm ngữ nghĩa.
  Trung ngữ翻译:`CPWBFT` 带语义聚类的信任度加权投票──
- `DecentLLMs` tổng hợp số liệu trung bình hình học về các đề xuất được ghi điểm.
  Trung ngữ翻译:`DecentLLMs` 评分 提案上的几何中位数聚聚──
- `Scenario` chạy mỗi bộ tổng hợp theo ba mô hình tấn công.
  Trung ngữ翻译:`Scenario` Trong 3 kiểu tấn công hoạt động trên mỗi cluster.

Các mô hình tấn công được thực hiện:

> 实现的攻击模式:

1. `byzantine`Một nhân viên nói dối với sự tự tin cao.
   Trung ngữ翻译:`byzantine`Một đặc vụ đã nói dối.
2. `sycophancy`Một đại lý sao chép câu trả lời đầu tiên mà họ thấy, với sự tự tin tương tự.
   Trung ngữ翻译:`sycophancy`Một đại lý sao chép câu trả lời đầu tiên mà nó thấy, chắc chắn phù hợp.
3. `monoculture`: ba đại lý chia sẻ một câu trả lời sai (sự sai lầm liên quan) với sự tự tin vừa phải.
   Trung ngữ翻译:`monoculture`:三个 Agent 共享一个错误答案(相关错误),置信度中等──

Đi chạy:

```
python3 code/main.py
```

Kết quả dự kiến: một bảng của (việc tấn công, tổng hợp) -> câu trả lời cuối cùng, với câu trả lời chính xác được nhấn mạnh. Sự đa dạng thất bại trong trường hợp monoculture. Đánh nặng sự tin tưởng của CPWBFT giảm bớt sự đồng hóa. Đường trung gian hình học của DecentLLMs kéo về phía cụm trung thực khi monoculture ít hơn một nửa dân số.

> 预期输出:一张(攻击,聚合器) -> 形式 最终答案,正确答案高亮显示――多数投票在单一文化案中失败――CPWBFT的信心加权缓解――当单一文化不到半时,几何中位的数量趋向诚实──

## Sử dụng nó.

`outputs/skill-consensus-designer.md`thiết kế một giao thức đồng thuận cho một tập hợp đa tác nhân: phương pháp nhóm, trọng lượng, ngưỡng và chính sách leo thang cho các vòng dưới ngưỡng.

> `outputs/skill-consensus-designer.md`Đối với nhiều đại lý 集合设计共识协议:聚类方法、权重、值,以及低于值轮次升级策略──

## Đưa nó lên mạng

Trước khi vận chuyển bất kỳ cơ chế đồng thuận nào:

- **Attack-test with at least the three patterns**Quy tắc của bạn sẽ thất bại một cách có thể đoán trước, không phải là lặng lẽ.
  Trung ngữ翻译:**至少用上述三种模式进行攻击测试。**Thỏa thuận của anh nên thất bại, chứ không phải thất bại lặng lẽ.
- **Log every minority cluster**Các nhóm thiểu số là hệ thống cảnh báo sớm cho các lỗi liên quan.
  Trung ngữ翻译:**记录每个少数派簇**及其来源──少数派是你相关错误的早期预警系统──
- **Enforce bounded rounds.**Không "đang thảo luận cho đến khi có thỏa thuận"  mà thưởng cho sự đồng tình.
  Trung ngữ翻译:**强制限制轮次。**Đừng cứ tranh luận cho đến khi đồng ý.
- **Separate agreement from correctness.**Khả năng đồng thuận đi đến một người xác minh; người xác minh độc lập với tập hợp.
  Trung ngữ翻译:**分离一致性和正确性。**共识输出交给验证器;验证器 độc lập với tập hợp.
- **Monitor the agreement rate.**Một sự gia tăng mạnh có nghĩa là sự thiên vị về sự phù hợp; một sự sụt giảm mạnh có nghĩa là sự trôi dạt của mô hình.
  Trung ngữ翻译:**监控一致率。**Tăng đột ngột có nghĩa là sự phân biệt của người; giảm đột ngột có nghĩa là chuyển động mô hình.

## Tập luyện bài tập

1. Đi chạy`code/main.py`- Đảm bảo đa số không đạt được cuộc tấn công của đơn cây nhưng CPWBFT giảm thiểu một phần khi sự tin tưởng của đơn cây dưới 0,7.
   Trung ngữ翻译:运行 `code/main.py`❖ xác nhận đa số phiếu bầu thất bại trong cuộc tấn công vào nền văn hóa đơn, nhưng khi sự tin tưởng vào nền văn hóa đơn thấp hơn 0,7 giờ CPWBFT phần đã giảm bớt vấn đề.
2. Thêm một mô hình tấn công thứ tư: **silent abstention** một đại lý từ chối trả lời ("Tôi không biết").
   Trung ngữ翻译:添加第四种攻击模式:**静默弃权** Một đại lý 拒绝回答 (("我不知道")  Mỗi bộ sưu tập nên xử lý việc bỏ phiếu như thế nào? thực hiện lựa chọn của bạn 
3. Thay đổi nhóm ngữ nghĩa từ canonicalization chuỗi sang tương tự nhúng ( Sử dụng bất kỳ mô hình nhúng nguồn mở nào).
   Trung ngữ翻译:将语义聚类从字符串规范化替换为嵌入相似度 ()                                                                                                                                                                                                                                                 
4. Đọc CP-WBFT (arXiv:2511.10400). Thực hiện bước hiệu chuẩn hóa bằng dò tin cậy (một mô hình hiệu chuẩn riêng biệt kiểm tra sự tin tưởng tự báo cáo của mỗi đại lý). Đo mức độ tăng độ chính xác trên kịch bản monoculture.
   Trung ngữ翻译:阅读 CP-WBFT(arXiv:2511.10400) ⋅实现信任探测校准步骤(单独的校准模型检查每个代理的自报信度) ⋅测量在单单文化场景上的准确率增益──
5. Đọc "Can AI Agents Agree?" (arXiv:2603.01213). Tạo lại một thí nghiệm thỏa thuận quy mô đơn giản: ba đại lý, một câu hỏi quy mô, lời nhắc người lừa dối. CPWBFT hay DecentLLMs có nhận được nó không?
   Trung文翻译:阅读"AI Agent 能达成一致吗?"(arXiv:2603.01213)。复现一个简化标量一致性实验:三个 Agent,一个标量问题,欺骗人格提示──CPWBFT或DecentLLMs 能捕获吗?

## Từ khóa  Keyword

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| BFT / 拜占庭容错 | "Byzantine fault tolerance" / "拜占庭容错" | Castro-Liskov 1999 protocol for consensus with `f < n/3` arbitrary faults. / Castro-Liskov 1999 协议，容忍 `f < n/3` 个任意故障节点的共识。 |
| Byzantine / 拜占庭 | "Any bad behavior" / "任何不良行为" | A node that can lie, drop messages, fail silently — anything but crash safely. / 可以撒谎、丢弃消息、静默失败的节点——除了安全崩溃外的任何行为。 |
| Confidence probe / 置信度探测 | "How sure are you?" / "你有多确定？" | Self-reported or calibrator-predicted probability attached to a vote. / 附加在投票上的自报或校准器预测的概率。 |
| Semantic clustering / 语义聚类 | "Same answer, different words" / "相同答案，不同措辞" | Grouping equivalent answers before counting votes. / 在计票前将等价答案分组。 |
| Geometric median / 几何中位数 | "Robust center" / "稳健中心" | The point minimizing sum of distances to sample points. Robust to outliers, unlike the mean. / 最小化到样本点距离之和的点。对异常值稳健，与均值不同。 |
| Monoculture / 单一文化 | "Same model, same failures" / "相同模型，相同失败" | Correlated errors when agents share training data or base model. / Agent 共享训练数据或基础模型时的相关错误。 |
| Sycophantic conformity / 谄媚从众 | "Agreeing with the loud voice" / "附和最大声的声音" | An agent's vote biases toward whoever spoke first/loudest. / Agent 的投票偏向最先/最大声发言的人。 |
| Core/Edge / 核心/边缘 | "Hierarchical BFT" / "层次化 BFT" | WBFT split: small Core consensus first, Edge nodes follow. Bounds latency. / WBFT 分割：小核心先达成共识，边缘节点跟随。限制延迟。 |

## Xem thêm 延伸阅读

- [Castro & Liskov — Practical Byzantine Fault Tolerance (OSDI 1999)](https://pmg.csail.mit.edu/papers/osdi99.pdf) cơ sở
- [CP-WBFT — Confidence-Probe Weighted BFT](https://arxiv.org/abs/2511.10400) trọng lượng phiếu bằng sự tin tưởng
- [DecentLLMs — leaderless multi-agent consensus](https://arxiv.org/abs/2507.14928) Phân tích trung bình hình học
- [WBFT — Weighted BFT with Hierarchical Structure Clustering](https://arxiv.org/abs/2505.05103) Chia Core/Edge cho thời gian trễ giới hạn
- [Can AI Agents Agree?](https://arxiv.org/abs/2603.01213) Sự dễ dàng của thỏa thuận quy mô và tấn công cá nhân lừa đảo
