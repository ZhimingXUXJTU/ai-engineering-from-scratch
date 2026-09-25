# Swarm Optimization for LLM (PSO, ACO) 优化群体 PSO ACO LLM

> Tích cực sinh học đang làm cho một LLM trở lại. **LMPSO**(arXiv:2504.09247) sử dụng PSO nơi tốc độ của mỗi hạt là một prompt và LLM tạo ra ứng cử viên tiếp theo; hoạt động tốt trên các kết quả theo trình cấu trúc (những biểu hiện toán học, các chương trình). **Model Swarms**(arXiv:2410.11163) đối xử với mỗi chuyên gia LLM như một hạt PSO trên một mô hình trọng lượng đa dạng và báo cáo **13.3% average gain**hơn 12 đường cơ sở trên 9 bộ dữ liệu với chỉ 200 trường hợp. **SwarmPrompt**(ICAART 2025) hợp chất PSO + Grey Wolf để tối ưu hóa nhanh chóng. **AMRO-S**(arXiv:2603.12933) là chuyên gia pheromone lấy cảm hứng từ ACO cho nhiều đại lý LLM định tuyến  **4.7x speedup**, bằng chứng định tuyến có thể diễn giải, cập nhật không đồng bộ với chất lượng được cổng để tách kết luận khỏi học tập. Bài học này thực hiện PSO trên không gian tham số nhanh và ACO trên định tuyến đại lý, đo lường tại sao các thuật toán cổ điển này phù hợp với thời đại LLM, và khi nào họ không.

> **【中文解读】**Bài viết này giới thiệu các thuật toán tối ưu hóa nhóm PSO (phân tử nhóm) và ACO (phân nhóm) như sinh vật bắt đầu tối ưu hóa trong nhiều đại lý ứng dụng.

> **【拓展：swarm optimization pso aco→具体应用】**群体优化算法在多代理中的应用:(1) 粒子群优化(PSO) Agent 根据自身优优位置和全局优优位置调整搜索方向;(2) 群体优化(ACO) Agent 通过信息素标记好的路径,后者倾向于遵循强信息素路径――这些算法适合大规模搜索空间中的优化问题,如 Agent 任务分配和路径规划――


**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib) | **语言:** Python（标准库）
**Prerequisites:** Phase 16 · 09 (Parallel Swarm Networks), Phase 16 · 14 (Consensus and BFT) | **前置知识:** Phase 16 · 09（并行群体网络），Phase 16 · 14（共识与 BFT）

>  **【前置】**Học本节前请先掌握:Phase 16·09(Swarm 网络) 、Phase 16·14(BFT) 、经典优化算法(PSO/ACO/GA) ⋅本节把生物启发算法应用到 LLM 时代快速 优化、模型路由──
>  **【类比】**LLM + PSO/ACO = "群找最佳快点"──PSO = Mỗi đại lý là hạt, tốc độ=快点,向全局最优移动;ACO = đại lý trong prompt 空间留下信息素,后者跟随强信息素──LMPSO 适合结构化输出(数学表达式、代码);Model Swarms Đặt mỗi LLM 专家当粒子,比 12 个基线平均高13.3%;AMRO-S sử dụng ACO làm đại lý 路由,4.7倍加速──
**Time:** ~75 minutes | **时间:** ~75 分钟

##                                                                                                                                                                                                                                                               

Bạn có một lệnh nhắc đi nhắc ghi điểm 62% trong đánh giá nhiệm vụ của bạn. Bạn muốn cải thiện nó. Lần chuyển động ngây thơ là chỉnh sửa thủ công không gradient, mà cân bằng xấu. Học tập tăng cường cần các tín hiệu phần thưởng và đủ rollouts để đào tạo. Backprop thông qua lệnh nhắc không thực sự có thể  lệnh nhắc là một chuỗi riêng biệt, không phải là một tham số phân biệt.

> Bạn có một gợi ý trong đánh giá nhiệm vụ có điểm số 62%. Bạn muốn cải thiện nó. Cách đơn giản là không có độ chuyển động, sự khác biệt mở rộng.

Tự động hóa học cổ điển tối ưu hóa  PSO cho không gian tìm kiếm liên tục, ACO cho lựa chọn đường dẫn  được thiết kế chính xác cho chế độ này: không gradient, dựa trên dân số, rẻ tiền cho mỗi đánh giá. Kết hợp chúng với LLM cho bước tìm kiếm không gradient, và bạn có được một tối ưu hóa thực tế đáng ngạc nhiên.

> PSO sử dụng không gian tìm kiếm liên tục, ACO sử dụng lựa chọn đường dẫn chính xác cho tình huống này: không thang độ, dựa trên nhóm, chi phí đánh giá thấp mỗi lần.

Các mô hình tương tự áp dụng cho các bộ phận *routing* trong các hệ thống đa bộ phận. Một bộ phận pheromone kiểu ACO ghi lại dấu vết của bộ phận nào hoạt động tốt nhất trên loại nhiệm vụ nào, cho phép bộ phận định tuyến khai thác dấu vết và phân hủy pheromone để các tuyến đường có thể được phát hiện lại.

> Tương tự mô hình cũng áp dụng cho các Agent trong nhiều Agent  hệ thống * đường dẫn*。 ACO 风格的信息素轨迹记录哪个 Agent 在哪种任务类型表现最好,让路由器利用轨迹,并减弱信息素以便重新发现路径。

## Khái niệm cốt lõi

### Tái mới PSO (Kennedy & Eberhart 1995)

Particle Swarm Optimization: dân số hạt trong không gian tìm kiếm liên tục. Mỗi hạt có vị trí `x_i`và tốc độ`v_i`Mỗi lần lặp lại:

```
v_i <- w * v_i + c1 * r1 * (p_best_i - x_i) + c2 * r2 * (g_best - x_i)
x_i <- x_i + v_i
evaluate fitness(x_i)
update p_best_i if improved
update g_best if global best
```

Ở đâu `p_best`là tốt nhất của hạt,`g_best`là những gì tốt nhất của đám đông,`w, c1, c2`là sự bất lực + nhận thức + trọng lượng xã hội,`r1, r2`là những yếu tố ngẫu nhiên.

### PSO về kết quả LLM  LMPSO

ArXiv:2504.09247 điều chỉnh PSO cho các kết quả cấu trúc được tạo ra bởi LLM (những biểu hiện toán học, các chương trình). Mỗi hạt là một kết quả ứng cử viên. Velocity là một * prompt* mô tả cách sửa đổi kết quả hiện tại hướng tới tốt nhất cá nhân / toàn cầu. LLM tạo ra kết quả mới từ động lực tốc độ. "trọng lực" của tốc độ là một động lực như "làm những thay đổi gia tăng nhỏ".

Điều này hoạt động tốt khi:
- Các sản phẩm được cấu trúc (có thể phân tích, có thể đánh giá).
  Trung ngữ翻译:输出是结构化的 (可解析,可评估)
- Kiểm tra vận động là tự động (thử nghiệm chạy, đánh giá toán học).
  Trung ngữ翻译:适应度是自动的(测试运行、算术评估)
- Dân số nhỏ (~ 10-30 hạt) vì vậy tổng số cuộc gọi LLM vẫn có thể quản lý được.
  Trung文翻译:种群小(约10-30 个粒子),总 LLM 调用可控。

Nó không hoạt động tốt khi sức khỏe cần đánh giá của con người  chi phí lặp lại trở nên cấm kỵ.

> Khi thích ứng cần kiểm tra nhân tạo thì hiệu quả không tốt  chi phí mỗi lần  cao quá.

### Mô hình Swarms

ArXiv:2410.11163 đưa PSO ra khỏi lớp đầu ra và vào lớp *model* . Mỗi "các hạt" là một LLM chuyên gia (chỉ số).

Nhìn sâu sắc chính là các mô hình chuyên gia LLM đã gần nhau trong một đa dạng tham số chung (nâng trọng bộ điều chỉnh, LoRA deltas). PSO trên không gian phụ chiều thấp này là rẻ và hiệu quả.

### Tái mới ACO (Dorigo 1992)

Khối ưu hóa thuộc địa kiến: kiến đi qua một biểu đồ; mỗi con đường có một con đường pheromone. kiến di chuyển xác suất trọng lượng theo cường độ pheromone. kiến hoàn thành nhiệm vụ lưu trữ pheromone tương ứng với chất lượng dung dịch. pheromone phân hủy theo thời gian.

### AMRO-S  ACO cho việc định tuyến đại lý

ArXiv:2603.12933 sử dụng ACO cho định tuyến đa đại lý. Mỗi loại nhiệm vụ là một "các điểm đến"; mỗi đại lý là một tuyến đường có thể. Pheromone tăng cường các tuyến đường tạo ra kết quả tốt.

- **Interpretable routing evidence.**Tăng cường pheromone là một tín hiệu được đọc bởi con người.
  Trung ngữ翻译:**可解释的路由证据。**信息素强度 là tín hiệu có thể đọc được của con người.
- **Quality-gated asynchronous update.**Phero-mon mới chỉ cập nhật sau khi kiểm tra chất lượng vượt qua, tách kết luận khỏi học tập.
  Trung ngữ翻译:**质量门控异步更新。**信息素 chỉ được kiểm tra chất lượng thông qua sau khi cập nhật, sẽ được đưa ra với việc tìm hiểu giải pháp.
- **4.7x speedup**về chỉ số chuẩn định tuyến nhiều đại lý.
  Trung ngữ翻译: 在多 Agent 路由基准上**4.7 倍加速**

Khổng chất lượng quan trọng: nếu không có nó, các chất nhanh nhưng sai tạo sẽ tích lũy pheromone, và hệ thống sẽ khóa vào các tuyến đường xấu.

> Quality Gate rất quan trọng: Không có nó, nhanh chóng nhưng sai lầm của Agent sẽ tích lũy thông tin, hệ thống bị khóa trên một con đường không tốt.

### Khi nào sử dụng PSO / ACO cho LLM

**Use PSO when:**
- Không gian tìm kiếm là liên tục hoặc bản đồ đến các tham số liên tục (đồng độ nhúng nhanh, trọng lượng LoRA, tham số tạo).
  Trung文翻译:搜索空间是连续的或映射到连续参数(提示嵌入、LoRA 权重、数值生成参数) ⋅
- Kiến thức thể dục là rẻ tiền và tự động.
  Trung文翻译:适应度评估廉价且自动──
- Dân số có thể nhỏ (10-30).
  Trung ngữ翻译:种群可以很小 ((10-30)。

**Use ACO when:**
- Bạn có vấn đề định tuyến hoặc chọn đường.
  Trung ngữ翻译:你有路由或路径选择问题──
- Các quyết định tăng cường theo thời gian (những loại nhiệm vụ tương tự trở lại).
  Trung ngữ翻译:决策随时间强化 (nói chung)
- Bạn cần bằng chứng có thể giải thích để đưa ra quyết định định định tuyến.
  Trung ngữ翻译:你需要路由决策的可解释证据──

**Do not use either when:**
- Kiến thức đòi hỏi phải được kiểm tra bởi con người (quá đắt tiền cho mỗi lần lặp lại).
  Trung文翻译:适应度需要人工审查 (适应度需要人工审查)
- Không gian tìm kiếm là riêng biệt và kết hợp theo cách mà PSO không bao gồm (nghiên sử dụng thuật toán di truyền thay vào đó).
  Trung ngữ翻译:搜索空间是离散组合的,PSO 无法覆盖 (tạm dịch: không gian tìm kiếm là phân tán, không thể phủ kín được)
- Các quyết định thời gian thực cần thời gian trễ nghiêm ngặt (PSO/ACO hội tụ chậm so với các tính toán duy nhất).
  Trung ngữ翻译:实时决策需要严格延迟(PSO/ACO 相对单次启发式收慢)

### Tại sao nguồn cảm hứng sinh học vẫn thắng

Các phương pháp dựa trên gradient cần các tín hiệu khác biệt. Các kết quả LLM và các quyết định định định tuyến không khác biệt tầm thường. Các phương pháp giả (các bộ định tuyến được học bằng tăng cường, các bộ điều chỉnh nhanh theo kiểu DPO) hoạt động nhưng cần đào tạo đắt tiền.

PSO và ACO chỉ cần một chức năng *evaluator* nếu bạn có thể ghi điểm cho một kết quả ứng cử viên hoặc một quyết định định định tuyến, bạn có thể tối ưu hóa trên không gian. Điều đó làm cho thanh ứng dụng thấp hơn nhiều.

### Các giới hạn thực tế

- **Population budget.**N hạt × T lặp lại × chi phí mỗi bằng.$0.02 / call, a 20-particle PSO running 50 iterations costs ~$20 - Hãy lên kế hoạch cho nó.
- **Exploration vs exploitation.**Tốc độ phân rã pheromone và sự bất lực của PSO thay đổi; phân rã quá nhanh → quên các giải pháp; quá chậm → bị mắc kẹt vào tối ưu địa phương sớm.
- **Catastrophic drift.**Cả hai thuật toán có thể hội tụ và sau đó phân biệt nếu phong cảnh thể dục thay đổi (cải phân phối dữ liệu mới).

## Hãy xây dựng nó.
```figure
swarm-stigmergy
```

## Hãy xây dựng nó

`code/main.py`thực hiện:

- `LMPSO` PSO trên các tham số nhanh chóng (giới nhiệt, trọng lượng top_k). "Làm thế hệ LLM" của mỗi hạt được mô phỏng như một chức năng thể dục được kịch bản. chạy thuật toán cho 30 lần lặp lại và hiển thị sự hội tụ tốt nhất.
- `AMRO_S` Đường dẫn theo kiểu ACO. 3 đại lý, 4 loại nhiệm vụ, matrix pheromone, 100 nhiệm vụ được định tuyến.
- So sánh: định tuyến ngẫu nhiên so với ACO định tuyến trên cùng một dòng nhiệm vụ. đo chất lượng và độ trễ.

Đi chạy:

```
python3 code/main.py
```

Tạo sản lượng dự kiến:
- LMPSO: g_best fitness cải thiện từ ngẫu nhiên đến gần như tối ưu hơn 30 lần lặp lại.
- AMRO-S: bảng pheromone ổn định trên đại lý đúng cho mỗi loại nhiệm vụ; ACO định tuyến đánh ngẫu nhiên khoảng ~ 30-40% về chất lượng và cũng giảm độ trễ ( ít thử lại hơn).

## Sử dụng nó.

`outputs/skill-swarm-optimizer.md`giúp lựa chọn giữa PSO, ACO, thuật toán di truyền và các chất tối ưu hóa dựa trên gradient cho các vấn đề tối ưu hóa LLM / đại lý.

## Đưa nó lên mạng

- **Start small.**10-20 hạt, 20-50 lần lặp lại. chỉ tăng lên nếu đường cong hội tụ cho thấy tăng rõ ràng.
  Trung ngữ翻译:**从小开始。**10-20 hạt, 20, 50 lần 代 chỉ trong đường thu nhập hiển thị tăng trưởng rõ ràng khi mở rộng
- **Log pheromones or g_best per iteration.**Việc giải quyết các hệ thống tối ưu hóa đám đông mà không có dấu vết là đau đớn.
  Trung ngữ翻译:**每次迭代记录信息素或 g_best。**Không có đường mòn.
- **Quality-gate updates.**Đặc biệt là cho ACO định tuyến: các chất nhanh và sai không được tích lũy pheromone.
  Trung ngữ翻译:**质量门控更新。**Đặc biệt là ACO: nhanh nhưng sai lầm.
- **Reset decay on distribution shift.**Khi phân bố của bạn thay đổi, pheromone già đã lỗi thời; thiết lập lại hoặc tăng gấp đôi tỷ lệ phân hủy tạm thời.
  Trung ngữ翻译:**分布偏移时重置衰减。**Khi đánh giá sự thay đổi phân bố, sự già hóa thông tin đã qua thời gian; tái lập hoặc tăng gấp tạm thời tỷ lệ suy giảm.
- **Cap the per-iteration cost.**Giả ra một số liệu chi phí mỗi lần lặp. PSO chi phí 500 đô la / lần lặp và tăng 0,5% không thể vận chuyển.
  Trung ngữ翻译:**限制每次迭代成本。**发发每次代成本指标──每次代花费$500 且只增加0.5%的PSO不可发行──

## Tập luyện bài tập

1. Đi chạy`code/main.py`- Quan sát sự hội tụ LMPSO. kích thước dân số khác nhau 5, 10, 20, 50.
2. Thực hiện một thí nghiệm "trái lở thảm họa": sau lần lặp 30, thay đổi chức năng thể dục. PSO thích nghi nhanh như thế nào?`p_best`giúp đỡ?
3. Thêm một cổng chất lượng vào AMRO-S: pheromone deposit chỉ trên các chạy với điểm đánh giá > 0,7.
4. Đọc LMPSO (arXiv:2504.09247). Bản đồ "tốc độ như một lời nhắc" của giấy trở lại tốc độ số của bạn.
5. Đọc AMRO-S (arXiv:2603.12933). Thực hiện "chặng đường nhanh đầu tư" tách rời với cập nhật pheromone không đồng bộ.

## Từ khóa  Keyword

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| PSO / 粒子群优化 | "Particle Swarm Optimization" / "粒子群优化" | Kennedy-Eberhart 1995. Population-based gradient-free optimizer. / Kennedy-Eberhart 1995。基于种群的无梯度优化器。 |
| ACO / 蚁群优化 | "Ant Colony Optimization" / "蚁群优化" | Dorigo 1992. Path/route optimization via pheromone trails. / Dorigo 1992。通过信息素轨迹的路径/路由优化。 |
| LMPSO / LLM 粒子群 | "PSO with LLM generation" / "LLM 生成的 PSO" | arXiv:2504.09247. Velocity is a prompt; LLM produces candidates. / arXiv:2504.09247。速度是提示；LLM 生成候选。 |
| Model Swarms / 模型群体 | "PSO on expert weights" / "专家权重的 PSO" | arXiv:2410.11163. Gradient-free update on model parameter subspace. / arXiv:2410.11163。模型参数子空间上的无梯度更新。 |
| AMRO-S / ACO Agent 路由 | "ACO for agent routing" / "Agent 路由的 ACO" | arXiv:2603.12933. Pheromone matrix over task-type × agent. / arXiv:2603.12933。任务类型 × Agent 的信息素矩阵。 |
| p_best / g_best / 个体最优/全局最优 | "Personal / global best" / "个人/全局最优" | Per-particle and swarm-wide best solutions found so far. / 每个粒子和群体目前找到的最优解。 |
| Pheromone / 信息素 | "Routing memory" / "路由记忆" | Strength on an edge; decays over time; deposits on quality. / 边上的强度；随时间衰减；按质量沉积。 |
| Quality-gated update / 质量门控更新 | "Only learn from good runs" / "只从好的运行学习" | Pheromone deposit conditioned on quality check. / 以质量检查为条件的信息素沉积。 |
| Catastrophic drift / 灾难性漂移 | "Distribution shift" / "分布偏移" | Fitness landscape changes; old p_best and pheromones become stale. / 适应度景观变化；旧的 p_best 和信息素变得过时。 |

## Xem thêm 延伸阅读

- [Kennedy & Eberhart — Particle Swarm Optimization](https://ieeexplore.ieee.org/document/488968) Báo cáo năm 1995 của PSO
- [Dorigo — Ant Colony Optimization](https://www.aco-metaheuristic.org/about.html) 1992 Tổ chức ACO
- [LMPSO — Language Model Particle Swarm Optimization](https://arxiv.org/abs/2504.09247) PSO cho các sản phẩm LLM có cấu trúc
- [Model Swarms — gradient-free LLM expert optimization](https://arxiv.org/abs/2410.11163) PSO trên mẫu trọng lượng không gian phụ
- [AMRO-S — ant-colony multi-agent routing](https://arxiv.org/abs/2603.12933) Đường dẫn dẫn pheromone với cổng chất lượng
