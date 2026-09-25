# Tiếng bỏ phiếu, sự đồng nhất, và Topology tranh luận 拓 辩论 投票

> Sự tổng hợp rẻ nhất: mẫu N các đại lý độc lập, đa số phiếu. Wang et al. 2022 tự nhất quán đã làm điều này với một mô hình được lấy mẫu N lần.**heterogeneous**Các tác nhân để thoát khỏi monoculture  các mô hình khác nhau, các cúm thanh khác nhau, nhiệt độ khác nhau, bối cảnh khác nhau. Ngoài phiếu bầu đa số, tranh luận về vấn đề topology: MultiAgentBench (arXiv:2503.01935, ACL 2025) đánh giá sự phối hợp sao / chuỗi / cây / biểu đồ và tìm thấy **graph best for research**AgentVerse (ICLR 2024) ghi lại hai mô hình mới nổi  hành vi tình nguyện và hành vi tuân thủ  và sự tuân thủ là cả một tính năng (khám phá sự đồng thuận) và một rủi ro (thân trí nhóm, Bài 24). Bài học này lập bản đồ không gian topology, xây dựng mỗi biến thể, và đo lường thuế phối hợp.

> **【中文解读】**Phần này giới thiệu cấu trúc tổ chức của các đại lý quyết định thông qua bỏ phiếu hoặc tranh luận.

> **【拓展：voting debate topology→具体应用】**投票和辩論拓定义多代理 决策的结构──三种常见拓:(1) 星形所有 Agent 独立投票,中心聚合;(2) 链形Agent 根据修改前一个 Agent 的输出;(3) 图形Agent 形成讨论网络,多轮交互──研究表明,图形拓在复杂推理任务上效果最好,但协调成本最高──


**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib) | **语言:** Python（标准库）
**Prerequisites:** Phase 16 · 07 (Society of Mind and Debate), Phase 16 · 14 (Consensus and BFT) | **前置知识:** Phase 16 · 07（心智社会与辩论），Phase 16 · 14（共识与 BFT）

>  **【前置】**学本节前请先掌握:Phase 16·07(辩论) Phase 16·14(BFT 共识) Phase 13·03(Tổng thống tự nhất quán)  Vote拓 = 多 Agent 决策的几何形状──
>  **【类比】**投票拓 = "会议桌摆放方式"──星形 = 圆桌投票(独立);链形 = 接力修改(前面 Agent 的输出传给下一个);图形 = 圆桌讨论(多轮交互)──MultiAgentBench 结论:图形适合研究任务但有"协调税"──>4 个 Agent 性价比下降)──异质性是关键不同模型/温度/快速 防单一文化错误──
**Time:** ~75 minutes | **时间:** ~75 分钟

##                                                                                                                                                                                                                                                               

Cuộc tranh luận có thể cải thiện độ chính xác (Du et al., arXiv:2305.14325). Nó cũng có thể làm suy giảm nó.

> 辩论可以提高准确性 (Du 等人,arXiv:2305.14325), cũng có thể giảm准确性 (Dear)

1. Ai nói chuyện với ai (topology).
   Trung ngữ翻译:谁和谁对话 (谁和谁对话)
2. Bao nhiêu vòng (Du 2023: cả hai vòng và các đại lý đều có ý nghĩa độc lập).
   Trung文翻译:多少轮次(Du 2023:轮次和 Agent 数量都独立重要)
3. Liệu các chất có phân loại (những mô hình cơ sở khác nhau phá vỡ monoculture).
   Trung文翻译:Công viên 是否异构(不同基础模型打破单一文化)
4. Nếu có một giọng nói đối lập (nhựa-manning vs. straw-manning).
   Trung文翻译: có có có chống đối âm thanh không?

Các nhóm "đánh 5 đại lý và bỏ phiếu" cho một nhiệm vụ thường trở lại so với một đại lý duy nhất. Các thất bại không ngẫu nhiên. Họ theo dõi topology và tính khác nhau. Bài học này là bản đồ topology.

> Nhóm sẽ "đi hành 5 đại lý và bỏ phiếu" cứng thêm vào nhiệm vụ, thường xuyên hơn một đại lý biểu hiện kém hơn.

## Khái niệm cốt lõi

### Sự nhất quán của bản thân, cơ sở mô hình đơn

Wang et al. 2022 ("Tự nhất quán cải thiện chuỗi suy nghĩ") đã lấy mẫu cùng một mô hình N lần ở nhiệt độ > 0 và được bỏ phiếu đa số trên các câu trả lời đường lý luận. Kết quả trên GSM8K: tăng đáng kể với các mẫu N = 40 trên một mã hóa tham lam.

> Wang 等人 2022 年 (("自一致性改进思维链推理") trong điều kiện nhiệt độ > 0, đã bỏ phiếu đa số cho cùng một mô hình 采样 N 次,并 cho các câu trả lời về đường lối推理 N 次, và kết quả trên:N=40 lần采样比单次贪心解码有显著提升;;

Biên giới: tự nhất quán sử dụng một mô hình cơ sở. sai lầm liên quan đến cấu trúc. Nếu mô hình có một thiên vị hệ thống, tất cả các mẫu N chia sẻ nó.

> Ưu điểm: tự đồng nhất sử dụng một mô hình cơ bản. Ưu điểm trong cấu trúc là liên quan. Nếu mô hình có sự phân biệt hệ thống, tất cả các mô hình đều chia sẻ nó.

### Tiếng bỏ đa đại diện, sự mở rộng đa dạng

Thay thế các mẫu N bằng các đại lý khác nhau. Các mô hình cơ sở khác nhau (Claude, GPT, Llama), các lời nhắc khác nhau, truy cập công cụ khác nhau. Lợi ích: sai lầm không liên quan. Chi phí: các đại lý khác nhau chi phí khác nhau; phối hợp chúng thêm chi phí chung.

> Để thay thế N 个样本 thành N 个* khác nhau* của Agent;; khác nhau cơ sở mô hình;;Claude、GPT、Llama), khác nhau提示, khác nhau công cụ truy cập;;

Tên thức của năm 2026 cho cuộc tranh luận đa dạng là **A-HMAD** Cuộc tranh luận đa tác nhân đa nguyên. Không được phổ biến, nhưng các báo cáo sử dụng thuật ngữ này cho "chương luận về các mô hình khác nhau, làm giảm các lỗi tương quan từ sự sụp đổ của đơn văn hóa".

> 2026 năm khác cấu trúc辩论的规范名称是**A-HMAD** đối kháng khác cấu trúc đa tác nhân 辩论――并非普遍采用, nhưng luận văn sử dụng từ này指"不同模型辩论,减少单一文化崩的相关错误"――

### Bốn topology

```
star                chain               tree                graph

    ┌─A─┐           A─B─C─D         ┌──A──┐              A───B
    │   │                           │     │              │ × │
    B   C                           B     C              D───C
    │   │                          / \   / \
    D   E                         D   E F   G           (fully connected)
```

Một trung tâm, tất cả các trung tâm khác chỉ nói chuyện với trung tâm. tương đương với người giám sát không có kênh quay lại.
Dòng: tuyến tính, mỗi đại lý nhìn thấy đầu ra của người trước đó.
Cây: phân cấp, được sử dụng bởi các hệ thống đại lý phân cấp (Dạy 06).
Hình: bất cứ ai. Bao gồm các nhóm liên kết hoàn toàn và DAG tùy ý.

> 星形: một trung tâm, tất cả các đại lý khác chỉ đối thoại với trung tâm.
> 链形:线性, mỗi đại lý 看到前一个 đại lý 的输出──类似流水线──
> 树形:层次化, dùng để làm cấp độ hóa Agent 系统 (第 06 课)
> 图形:任意到任意──包括完全连接的团和任意DAG──

### Thuế phối hợp (MultiAgentBench)

MultiAgentBench (MARBLE, ACL 2025, arXiv:2503.01935) đánh giá sao, chuỗi, cây, biểu đồ trên một bộ nhiệm vụ bao gồm nghiên cứu, lập trình và lập kế hoạch. Kết quả đo chính:

> MultiAgentBench ((MARBLE,ACL 2025,arXiv:2503.01935) đã tiến hành基准测试对星形、链形、树形、图形在包括研究、编码和规划的任务套件上:

- **Graph**Topology thắng trong các nhiệm vụ nghiên cứu thông tin chảy bất cứ ai; các đại lý có thể chỉ trích lẫn nhau.
  Trung ngữ翻译:**图形**拓在研究任务上获胜;信息随意流动;Agent có thể chỉ trích lẫn nhau.
- **Star**Trận đấu với các nhiệm vụ thực tế nhanh chóng. Hub lọc và hợp nhất.
  Trung ngữ翻译:**星形**Trong nhiệm vụ thực tế trả lời nhanh chóng, giành chiến thắng.
- **Chain**thắng lợi trên đường ống từng bước (phong lọc từng bước).
  Trung ngữ翻译:**链形**Trong từng bước dòng nước
- **Coordination tax**xuất hiện qua ~ 4 đại lý trong topology đồ thị. Wall-clock và giá token tăng nhanh hơn chất lượng.
  Trung ngữ翻译:**协调税**Trong hình ảnh, khoảng 4 đại lý xuất hiện sau đó.

Mức giới hạn 4 đại lý là kinh nghiệm, không phải cơ bản. Nó phản ánh khả năng bối cảnh LLM 2026: bối cảnh của mỗi đại lý chứa đầy các sản phẩm của các đồng nghiệp, và giá trị biên của cộng đại lý N + 1 giảm khi mọi người có thể thấy mọi người.

> 4 Đường giới hạn trên của đại lý là kinh nghiệm, không phải là cơ bản. Nó phản ánh dung lượng của LLM năm 2026: mỗi đại lý trên đầy các sản phẩm của đồng nghiệp, một khi mọi người có thể thấy mỗi người, thêm N + 1 giá trị biên của đại lý đã giảm.

### Chiến lược tranh luận đa đại lý ("Chúng ta nên điên lên?")

ArXiv:2311.17371 là cuộc khảo sát năm 2023 về các chiến lược MAD. Kết quả chính được lặp lại bởi những người khác: Các biến thể MAD có cấu trúc tương tự với sự nhất quán (tự chọn mẫu + tổng hợp) thường kém nhất quán khi sử dụng cùng một ngân sách. MAD giúp nhiều nhất khi các đại lý thực sự đa dạng và cuộc tranh luận có cấu trúc đối kháng (một đại lý tranh luận chống lại).

> arXiv:2311.17371 là 2023 MAD 策略综述──关键发现已被他人复现: Trong cấu trúc tương tự với sự đồng nhất của MAD 变体(独立采样 + 聚合) trong sử dụng cùng ngân sách──MAD 在 Agent 真正异构且辩论具有对抗结构时最大的帮助──

### AgentVerse các mô hình mới nổi

AgentVerse (ICLR 2024, https://proceedings.iclr.cc/paper_files/paper/2024/file/578e65cdee35d00c708d4c64bce32971-Paper-Conference.pdf) ghi lại hai hành vi xuất hiện từ cuộc tranh luận đa tác nhân ngay cả khi không có thiết kế rõ ràng:

- **Volunteer.**Một đại lý cung cấp sự giúp đỡ ("Tôi có thể thực hiện bước tiếp theo") không được nhắc nhở. hữu ích: nó phân bổ công việc cho đại lý có khả năng nhất cho một nhiệm vụ phụ.
  Trung ngữ翻译:**自愿者。**Trưởng lý chủ động cung cấp trợ giúp (I can take the next step)
- **Conformity.**Một đại lý điều chỉnh lập trường của mình để phù hợp với một nhà phê bình, ngay cả khi nhà phê bình sai.
  Trung ngữ翻译:**从众。**Trưởng lý 调整立场以匹配批评者, ngay cả khi批评者是错的──这是辩论中行为的等价.

Sự phù hợp là lý do tại sao cuộc tranh luận cho đến khi thỏa thuận sẽ thưởng cho những kẻ bắt nạt.

> Từ nhiều người là tại sao "diễn giải cho đồng ý" sẽ thưởng cho những người mạnh mẽ. Có một vòng quay để thêm vào các ủy ban thẩm phán độc lập có thể giảm nhẹ.

### Sự khác biệt: nút thực tế di chuyển chính xác

Một mô hình 2024-2026 trong văn học thực tế: trao đổi một trong các đại lý N của bạn cho một mô hình cơ sở khác tạo ra một đợt tăng độ chính xác lớn hơn so với tăng N bằng 1. Nhận thức là monoculture  mỗi nguồn lỗi độc lập mới có giá trị hơn một mẫu tương quan bổ sung.

> Một mô hình trong tài liệu thực tế 2024-2026: thay đổi một trong các N 个代理 thành một mô hình cơ sở khác so với tăng N + 1 个代理 带来更大的准确率提升──直觉是单一文化 mỗi nguồn sai lầm độc lập mới có giá trị hơn so với các mẫu liên quan bổ sung──

Trong giới hạn, sự đa dạng vượt qua sự đa dạng. Ba mô hình khác nhau đánh bại năm bản sao của một mô hình trong hầu hết các nhiệm vụ có thực tại sạch.

> Trong trường hợp tối đa, các cấu trúc khác nhau thắng số lượng. Trong hầu hết các nhiệm vụ có tiêu chuẩn rõ ràng, ba mô hình khác nhau thắng hơn năm mô hình giống nhau.

### Phương pháp của bồi thẩm đoàn

Các cơ sở của Sibyl (được trích dẫn trong văn học Minsky-LLM) chính thức hóa một "đội thẩm phán" một tập hợp nhỏ các đại lý chuyên môn tinh chỉnh câu trả lời bằng cách bỏ phiếu tại mỗi giai đoạn. Không giống như bỏ phiếu đa số đơn giản, một ban giám khảo có vai trò: một đại lý kiểm tra chéo, một cung cấp bối cảnh, một điểm xác thực. Các phương pháp của ban giám khảo là điểm trung giữa bỏ phiếu đơn giản (cô rẻ, dễ bị đơn văn hóa) và MAD đầy đủ (cô đắt, dễ tuân thủ).

> Sibyl framework (trích dẫn trong văn bản Minsky-LLM) đã hình thành "đội thẩm phán" 一小组 chuyên nghiệp đại lý 通过每阶段投票来改进答案──与简单多数投票不同,陪审团 có vai trò: một đại lý 交叉质询, một cung cấp trên 下文, một đánh giá hợp lý──

### Khi cuộc bầu cử với cuộc tranh luận chiếm ưu thế

- Câu hỏi có sự thật cơ bản (thực tế, toán học, hành vi mã).
  Trung文翻译:问题有标准答案 ((事实、数学、代码行为) ⋅投票收是有意义的──
- Các đại lý có thể truy cập vào các nguồn hoặc công cụ khác nhau (có sự khác biệt).
  Trung ngữ翻译:Công viên có thể truy cập các nguồn khác nhau hoặc các công cụ khác nhau (异构性可用)
- Các vòng được giới hạn (2-3 điển hình) và có một thẩm phán hoặc kiểm chứng riêng biệt.
  Trung ngữ翻译:轮次有界 (thường là 2-3 vòng), có thẩm phán hoặc chứng nhân độc lập.
- Ngân sách cho phép 3-5 đại lý.
  Trung ngữ 翻译: ngân sách cho phép 3-5 代理.

### Khi bỏ phiếu với cuộc tranh luận đau đớn

- Câu hỏi này có hình dạng ý kiến, các đại lý tụ tụ tập với câu trả lời nào có vẻ chắc chắn nhất, không phải chính xác nhất.
  Trung ngữ翻译:问题是意见型的──Agent 收到看起来最自信的答案,而不是最正确的──
- Tất cả các đại lý đều có một mô hình cơ bản.
  Trung文翻译:所有 Agent 共享基础模型──单一文化使共识毫无意义──
- Các vòng không giới hạn, sự phù hợp luôn thắng.
  Trung ngữ翻译:轮次无界──从众每次都赢──
- Nhiệm vụ đơn giản. Một đại lý đơn với tính nhất quán ở N = 5 rẻ hơn và chính xác như vậy.
  Trung ngữ翻译:任务简单――单代理 在 N=5 时的自一致性更便宜且同样准确――

## Hãy xây dựng nó.
```figure
sw-debate-topology
```

## Hãy xây dựng nó

`code/main.py`thực hiện:

- `run_star(agents, hub, question)` Các cuộc thăm dò trung tâm cho mỗi công nhân, tổng số.
  Trung ngữ翻译:`run_star` Trung tâm                                                                                                                                                                                                                                                             
- `run_chain(agents, question)` tinh chế theo trình tự.
  Trung ngữ翻译:`run_chain` 顺序改进──
- `run_tree(root, children, question)` phân cấp với tổng hợp độ sâu-2.
  Trung ngữ翻译:`run_tree` 层次化, độ sâu 2 聚合──
- `run_graph(agents, question, rounds)`- Vấn đề toàn diện, vòng giới hạn.
  Trung ngữ翻译:`run_graph` 全对全辩论, có giới hạn lượt次.
- Một số tính khác nhau được viết: mỗi đại lý có một `error_bias`cho thấy sai lầm hệ thống của nó.
  Trung văn翻译:脚本化的异构度旋: Mỗi đại lý có một `error_bias`Cụ thể là một lỗi hệ thống.
- Một dây đo chạy mỗi topology ở N=3, 5, 7 và báo cáo (sự chính xác, total_tokens, wallclock_simulated).
  Trung ngữ翻译:测量工具在 N=3, 5, 7 时运行每个拓并报告(准确率,总代币,模拟挂钟时间) ⋅

Đi chạy:

```
python3 code/main.py
```

Kết quả dự kiến: một bảng topology × N → (sự chính xác, token, độ trễ). Hình thắng ở N=3-5 trên các nhiệm vụ theo kiểu nghiên cứu; sao thắng trên các nhiệm vụ thực tế nhanh; biểu đồ ở N=7 cho thấy thuế phối hợp (sự trễ tăng nhanh hơn độ chính xác).

> 预期输出:拓 × N →(准确率,token,延迟)表格。图形在 N=3-5的研究风格任务上获胜;星形在快速事实性任务上获胜;图形在 N=7 时显示协调税(延迟膨胀快于准确率)

## Sử dụng nó.

`outputs/skill-topology-picker.md`là một kỹ năng đọc mô tả nhiệm vụ và đề nghị một topology (những ngôi sao / chuỗi / cây / biểu đồ), một N (nhiều đại viên), một hồ sơ tính khác nhau (chương trình cơ bản để sử dụng), và một đường tròn.

> `outputs/skill-topology-picker.md`Đây là một kỹ năng,读取任务描述并推拓(星形/链形/树形/图形)

## Đưa nó lên mạng

Đối với bất kỳ bộ phận nào:

- Bắt đầu với **self-consistency at N=5**sử dụng một mô hình cơ sở mạnh mẽ. Đó là cơ sở giá rẻ.
  Từ một mô hình cơ bản mạnh mẽ**N=5 自一致性**开始――这是廉价基线――
- Tăng lên **heterogeneous voting at N=3**Nếu chính xác là quan trọng, hãy đo đợt delta.
  Trung ngữ翻译: Nếu tỷ lệ xác thực quan trọng, nâng cấp đến **N=3 异构投票**                                                                                                                                                                                                                                                              
- Chỉ nâng cấp lên **debate topology**nếu nhiệm vụ có cấu trúc (sự nghiên cứu, nhiều bước) và các vòng giới hạn là khả thi.
  Trung ngữ翻译: chỉ có cấu trúc trong nhiệm vụ (研究多步骤) và có vòng lặp có thể thực hiện khi được nâng cấp lên**辩论拓扑**
- Luôn ghi lại nhóm thiểu số. Khi một nhóm thiểu số luôn đúng, bạn có tín hiệu đa dạng.
  Trung ngữ翻译:始终记录少数派──当少数派持续正确时,你就有多样性信号──
- Đánh giá đồng hồ tường và mã thông báo cùng với độ chính xác. "Tương tự chính xác tốt hơn với chi phí 10 lần" là một quyết định kinh doanh.
  Trung ngữ翻译:基准测试挂钟时间和代币以及准确率──"10倍成本的更好准确率" là quyết định thương mại──

## Tập luyện bài tập

1. Đi chạy`code/main.py`. Chụp đường cong thuế phối hợp cho topology đồ thị: độ chính xác so với N, token so với N. Ở n nào đường cong cong cong cong cong?
   Trung ngữ翻译:运行 `code/main.py`◊ vẽ hình dạng拓的协调税曲线:准确率 vs N,token vs N──曲线在哪个N处转折?
2. Thực hiện A-HMAD: ba tác nhân có thiên vị khác nhau.
   Trung ngữ翻译:实现 A-HMAD:三个有故意不同偏差的代理──全同偏差基线与 A-HMAD 在第十四课单一文化攻击上如何比较?
3. Thêm một vai trò "đánh án" vào topology đồ thị không bỏ phiếu, chỉ ghi điểm đồng thuận cuối cùng.
   Trung ngữ翻译: Trong hình tượng拓中添加一个"评委"角色,不投票只评分最终共识―― điều này sẽ thay đổi hành vi của người dân nổi lên?
4. Đọc bài báo AgentVerse (ICLR 2024). Xác định hành vi mới nổi nào mà thực hiện của bạn thể hiện mạnh nhất. Bạn có thể tạo ra hành vi ngược lại bằng cách thay đổi nhanh chóng không?
   Trung ngữ翻译:阅读 AgentVerse 论文(ICLR 2024) ―― nhận ra thực hiện của bạn mạnh mẽ nhất biểu hiện hành vi nào.
5. Đọc MultiAgentBench (arXiv:2503.01935) Phần 4 (các thí nghiệm topology).
   Trung văn翻译:阅读 MultiAgentBench(arXiv:2503.01935) 第 4 节(拓实验) ―― 用你的工具复现论文中一个任务上的图形胜于研究的结果──

## Từ khóa  Keyword

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Self-consistency / 自一致性 | "Sample N times, vote" / "采样 N 次，投票" | Wang 2022. Single model, N temperature>0 samples, majority vote on reasoning paths. / Wang 2022。单模型，N 次 temperature>0 采样，推理路径多数投票。 |
| Heterogeneity / 异构性 | "Different models" / "不同模型" | Ensemble of different base models or prompt families. Breaks monoculture. / 不同基础模型或提示族的集成。打破单一文化。 |
| MAD / 多 Agent 辩论 | "Multi-agent debate" / "多 Agent 辩论" | Generic term for agents exchanging critiques over rounds. See Du 2023. / Agent 跨轮次交换批评的通用术语。见 Du 2023。 |
| A-HMAD / 对抗性异构 MAD | "Adversarial Heterogeneous MAD" / "对抗性异构 MAD" | MAD variant emphasizing different models + adversarial structure. / 强调不同模型 + 对抗结构的 MAD 变体。 |
| Topology / 拓扑 | "Who talks to whom" / "谁和谁对话" | Star, chain, tree, graph. Determines information flow. / 星形、链形、树形、图形。决定信息流。 |
| Coordination tax / 协调税 | "Diminishing returns" / "边际收益递减" | Above ~4 agents on graph, cost grows faster than quality. / 图形拓扑约 4 个 Agent 后，成本增长快于质量。 |
| Volunteer behavior / 自愿者行为 | "Unprompted help" / "主动帮助" | AgentVerse emergent pattern: an agent offers to take a step. / AgentVerse 涌现模式：Agent 主动提出执行步骤。 |
| Conformity behavior / 从众行为 | "Agreement under pressure" / "压力下的同意" | AgentVerse emergent pattern: an agent aligns with a critic. / AgentVerse 涌现模式：Agent 与批评者对齐。 |
| Jury / 陪审团 | "Small specialized panel" / "小型专业小组" | Sibyl-style ensemble with roles (examiner, context, scorer). / Sibyl 风格的带角色集成（质询者、上下文、评分者）。 |

## Xem thêm 延伸阅读

- [Wang et al. — Self-Consistency Improves Chain of Thought Reasoning](https://arxiv.org/abs/2203.11171) Tỷ lệ cơ sở mô hình đơn
- [Du et al. — Improving Factuality and Reasoning via Multiagent Debate](https://arxiv.org/abs/2305.14325) cả hai đại lý và vòng liên quan độc lập
- [MultiAgentBench / MARBLE](https://arxiv.org/abs/2503.01935) chỉ số chuẩn topology cho thấy biểu đồ tốt nhất cho nghiên cứu, chuỗi cho đường ống
- [Should we be going MAD?](https://arxiv.org/abs/2311.17371) Nghiên cứu chiến lược MAD; phát hiện ra MAD thường mất tính nhất quán với ngân sách bình đẳng
- [AgentVerse (ICLR 2024)](https://proceedings.iclr.cc/paper_files/paper/2024/file/578e65cdee35d00c708d4c64bce32971-Paper-Conference.pdf) Tự nguyện và các mô hình tuân thủ mới nổi
- [MARBLE repo](https://github.com/ulab-uiuc/MARBLE) Thực hiện tham chiếu
