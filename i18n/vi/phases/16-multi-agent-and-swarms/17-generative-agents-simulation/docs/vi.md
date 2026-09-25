# Các đại lý tạo và mô phỏng mới

> Park et al. 2023 (UIST '23, arXiv:2304.03442) dân cư **Smallville**, một hộp cát gồm 25 đại lý, với cấu trúc ba phần: **memory stream**(Lập nhật ngôn ngữ tự nhiên),**reflection**(sự tổng hợp cấp cao hơn mà chất gây ra về dòng chảy của nó) và**plan**(các hành vi ở mức độ ngày, sau đó là kế hoạch phụ). Kết quả là sự xuất hiện của bữa tiệc Ngày Valentine: một đại lý đã gieo giống với "cần tổ chức một bữa tiệc Ngày Valentine", mà không cần viết kịch bản thêm, sản xuất các lời mời lan rộng khắp dân số, ngày phối hợp, và bữa tiệc xảy ra từ 24 đại lý không biết gì về nó. Các Ablation cho thấy cả ba thành phần đều cần thiết để có thể tin tưởng. Các lỗi được ghi nhận là lỗi về quy tắc không gian (trong cửa hàng đóng cửa, chia sẻ phòng tắm một người). Đây là kiến trúc tham chiếu cho mô phỏng đại lý và đánh giá xã hội đa đại lý vào năm 2026.

> **【中文解读】**Chương trình này giới thiệu về việc tạo ra đại lý 模拟斯坦福 AI Small Town Experiment, 25 đại lý AI trong cộng đồng ảo sống tự do.

> **【拓展：generative agents simulation→具体应用】**斯坦福的生成式代理 实验(Park et al., 2023) đã tạo ra 25 nhân viên AI trong cuộc sống tự do trong một thị trấn ảo mỗi ngày dậy dậy, lên làm, xã hội, hình thành mối quan hệ và ký ức。 sáng tạo cốt lõi là cấu trúc lưu lượng ký ̇ Mỗi nhân viên 维护 theo thứ tự thời gian của chuỗi kinh nghiệm, thông qua phản ánh và kết luận提取高层洞察──


**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib) | **语言:** Python（标准库）
**Prerequisites:** Phase 16 · 04 (Primitive Model), Phase 16 · 13 (Shared Memory) | **前置知识:** Phase 16 · 04（原语模型），Phase 16 · 13（共享内存）

>  **【前置】**学本节前请先掌握:Phase 16·04(原语)、Phase 16·13(共享内存)、Phase 11·04(Tập nhập, ký ức流检索用)。Stanford Smallville = 多 Agent 涌现社会行为里程碑实验。
>  **【类比】**Smallville = "AI 版模拟人生"──25 个 AI 居民各有生活、记忆、计划──情人节派对奇迹: một Đại diện 想办派对→邀请传开→其他人调整日程→派对真发生全是涌现,无脚本──三件套:memory stream(经历日志) + suy nghĩ(自我总结) + kế hoạch(日计划)──三者缺一不可, loại bỏ任一 Đại diện 行为变得不可信──
**Time:** ~75 minutes | **时间:** ~75 分钟

##                                                                                                                                                                                                                                                               

Hầu hết các hệ thống đa đại lý là các nhóm được viết chặt chẽ: kế hoạch lập kế hoạch, mã lập trình, đánh giá của nhà đánh giá. Điều đó hoạt động cho các nhiệm vụ được xác định rõ ràng. Nó không nắm bắt hành vi nổi lên, không được viết ra khi các đại lý có bộ nhớ, ưu tiên và một thế giới mở. Nghiên cứu, mô phỏng xã hội và ngày càng nhiều AI trò chơi cần loại thứ hai này.

> Đại đa số các hệ thống đại lý là một nhóm các kịch bản chặt chẽ: lập trình viên lập kế hoạch, biên tập viên lập lập trình, thẩm phán đánh giá. Điều này có hiệu quả đối với nhiệm vụ xác định rõ ràng. Nhưng nó không thể nắm bắt được khi đại lý có trí nhớ, ưu tiên và hành vi không phải kịch bản xuất hiện trong thế giới mở. Nghiên cứu, mô phỏng xã hội và ngày càng nhiều trò chơi AI cần các loại thứ hai.

Thiết kế Smallville là điểm chuẩn cho nó. Cho đến Park 2023, các mô phỏng đại lý tốt nhất là người theo kịch bản nông; sau đó, mô hình là mặc định cho các đại lý tạo trong thế giới mở. Nếu bạn xây dựng mô phỏng đại lý vào năm 2026, bạn hoặc sử dụng ba thành phần của Smallville hoặc biện minh rõ ràng tại sao bạn không.

> Smallville kiến trúc là cơ sở của loại này. Trước Park 2023, tốt nhất Agent 模拟 là một người theo dõi kịch bản tầng thấp; sau đó, mô hình này trở thành một tiêu chuẩn của Agent được tạo ra trong thế giới mở. Nếu bạn xây dựng Agent 模拟 vào năm 2026, bạn sẽ sử dụng ba thành phần của Smallville, bạn sẽ giải thích rõ ràng tại sao không sử dụng.

## Khái niệm cốt lõi

### Ba thành phần

**Memory stream.**Một nhật ký chỉ có phụ lục về quan sát, hành động, suy nghĩ và kế hoạch. Mỗi mục có dấu thời gian, loại, mô tả (ngôn ngữ tự nhiên) và siêu dữ liệu bắt nguồn:**recency**- **importance**(đánh giá 1-10 của đại lý), và **relevance**(có sự tương đồng với truy vấn hiện tại).

> **记忆流。**Một chỉ thêm một quan sát, hành động, phản ánh và kế hoạch nhật ký. Mỗi bài viết có thời gian, kiểu, mô tả và dữ liệu sinh học:**时效性****重要性**(Hội tác tự đánh giá 1-10) và**相关性**(Tương tự như các câu hỏi hiện tại)

```
[2026-02-14 09:12:03] observation: Isabella Rodriguez asked me if I like jazz
[2026-02-14 09:14:22] reflection:   I enjoy long conversations about music
[2026-02-14 10:05:00] plan:         Attend Isabella's Valentine's Day party tonight
```

Tận dụng trí nhớ kết hợp ba điểm:`score = w_recency * e^(-decay * age) + w_importance * importance + w_relevance * cos_sim`. mục đầu k nhập vào lệnh hiện tại.

**Reflection.**Chuẩn bị (mỗi N ký ức hoặc trên các sự kiện quan trọng), đại lý tạo ra tổng hợp thứ tự cao hơn từ ký ức gần đây. Các mục phản ánh trở lại dòng chảy và có thể lấy lại như bất kỳ ký ức nào khác. Đây là cách đại lý xây dựng "sự hiểu biết"

> **反思。**定期(每 N 条记忆或在重要事件时),Agent từ trong ký ức gần đây tạo ra một tổng hợp cao cấp。反思条目回到流中,像其他记忆一样可检查──这是 Agent建立"理解"的方式架构中等于长期信念──

**Plan.**Sự phân hủy từ trên xuống. Đầu tiên, một kế hoạch cấp ngày trong các đoạn rộng ("đi làm việc, ăn tối với Klaus"). Sau đó là kế hoạch cấp giờ. Sau đó là kế hoạch cấp hành động.

> **计划。**Bản thân lên xuống phân bố. Trước tiên, kế hoạch ngày cơ bản (上班,和 Klaus 共进晚餐)  tiếp theo là kế hoạch giờ nhỏ.

### Tại sao cả ba đều quan trọng (bỏ)

Park et al. chạy các ablation giảm từng quan sát, suy nghĩ và kế hoạch.

> Park 等人 đã tiến hành các thí nghiệm tiêu thụ, phân biệt bỏ qua quan sát, phản chiếu và kế hoạch.

- Không có**observation**Đại lý bỏ qua bối cảnh và hành động dựa trên niềm tin cũ.
  Trung ngữ翻译:没有**观察**,Agent 缺失上下文, dựa trên quá khứ niềm tin hành động.
- Không có**reflection**người đại lý không thể hình thành niềm tin cấp cao; sự tương tác vẫn nông cạn.
  Trung ngữ翻译:没有**反思**,Công ty không thể hình thành niềm tin cao cấp; giao tiếp giữ tầng thấp.
- Không có**plan**hành vi trở thành tiếng ồn phản ứng; mục tiêu bị phân tán.
  Trung ngữ翻译:没有**计划**, hành vi trở thành tiếng ồn phản ứng; mục tiêu tiêu tiêu diệt.

Điểm tin cậy từ các điểm đánh giá của con người là cao nhất với cả ba; giảm bất kỳ một sản xuất một sự lùi đo lường.

> Số lượng độ tin cậy của người đánh giá là cao nhất trong thời gian; loại bỏ bất kỳ sự phân hủy nào có thể đo lường được.

### Sự xuất hiện của Ngày Valentine

Một đại lý, Isabella Rodriguez, được gieo với mục tiêu "cần tổ chức một bữa tiệc ngày Valentine tại Hobbs Cafe vào ngày 14 tháng 2 lúc 5 giờ chiều".

> Một đại lý, Isabella Rodriguez, được trồng mục tiêu "làm việc vào ngày 14 tháng 2 ngày 14 chiều 5 giờ tại Hobbs Cafe tổ chức một bữa tiệc lễ hội tình cảm"...... 24 đại lý khác không nhận được giống như vậy... trong vài ngày trong mô phỏng:

1. Kế hoạch của Isabella bao gồm mời mọi người.
   Trung ngữ翻译:Isabella's kế hoạch bao gồm mời mọi người.
2. Mỗi lời mời trở thành một quan sát trong dòng nhớ của người hàng xóm.
   Trung文翻译: Mỗi người được mời trở thành một quan sát trong dòng lưu niệm hàng xóm.
3. Nhìn lại của người hàng xóm đó tạo ra niềm tin: "Isabella đang tổ chức một bữa tiệc".
   Trung ngữ翻译:邻居的反思产生信念:"Isabella phải办派对──"
4. Kế hoạch của hàng xóm bao gồm "đang tham dự bữa tiệc vào ngày 14 tháng 2".
   Trung文翻译:邻居的计划纳入"2月14日参加派对"──
5. Hàng xóm nói với hàng xóm khác.
   Trung ngữ翻译:邻居告诉其他邻居──邀请在没有中央协调的情况下传播──
6. Vào lúc 5 giờ tối ngày 14 tháng 2, một số nhân viên tụ họp tại quán cà phê Hobbs.
   Trung ngữ翻译:2 月 14 日下午 5 点,几个经纪人汇聚到霍布斯咖啡馆──

Đây là sự xuất hiện theo nghĩa kỹ thuật: hành vi cấp hệ thống (một đảng) phát sinh từ các tương tác địa phương (cý nghị song phương + lập kế hoạch cá nhân) mà không có một dàn nhạc trung tâm.

> Đây là một hiện tượng trên nghĩa kỹ thuật: hệ thống cấp hành vi (sistem class behavior) xuất phát từ giao tiếp địa phương (bi-lateral invitation + 个体规划) không có người tổ chức trung ương.

### Các chế độ thất bại được ghi nhận

Park et al. ghi rõ ràng:

> Park 等人 đã ghi lại:

- **Spatial norm errors.**Các đại lý đi vào các cửa hàng đóng cửa. Các đại lý cố gắng sử dụng cùng một phòng tắm một người. Các đại lý ăn trong các phòng không dành cho ăn. Mô hình không suy luận các quy tắc xã hội-physical chỉ từ môi trường.
  Trung ngữ翻译:**空间规范错误。**Trưởng thức: Trưởng thức: Trưởng thức: Trưởng thức: Trưởng thức: Trưởng thức: Trưởng thức: Trưởng thức: Trưởng thức: Trưởng thức: Trưởng thức: Trưởng thức: Trưởng thức: Trưởng thức: Trưởng thức: Trưởng thức: Trưởng thức: Trưởng thức: Trưởng thức: Trưởng thức: Trưởng thức: Trưởng thức: Trưởng thức: Trưởng thức: Trưởng thức: Trưởng thức: Trưởng thức: Trưởng thức: Trưởng thức: Trưởng thức: Trưởng thức: Trưởng thức: Trưởng thức: Trưởng thức: Trưởng thức: Trưởng thức: Trưởng thức: Trưởng thức: Trưởng thức: Trưởng thức: Trưởng thức: Trưởng thức: Trưởng thức: Trưởng thức: Trưởng thức: Trưởng thức: Trưởng thức: Trưởng thức: Trưởng thức: Trưởng thức: Trưởng thức: Trưởng thức: Trưởng thức: Trưởng thức: Trưởng thức: Trưởng thức: Trưởng thức: Trưởng thức: Trưởng thức: Trưởng thức: Trưởng thức: Trưởng thức: Trưởng thức: Trưởng thức: Trưởng thức: Trưởng thức: Trưởng thức: Tránh về về về về về về về về về về về về về về về về về về về về về về về về về về về về về về về về về về về về về về về về về về về về về về về về về về về về về về về về về về về về mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt mặt
- **Memory overflow.**Các hoạt động mô phỏng sâu gây ra chi phí thu hồi bộ nhớ tăng lên.
  Trung ngữ翻译:**记忆溢出。**Sự sử dụng hình thức làm tăng chi phí tìm kiếm trí nhớ.
- **Reflection hallucination.**Nhận phản xạ có thể phát minh ra các mối quan hệ không tồn tại trong dòng lưu trữ.
  Trung ngữ翻译:**反思幻觉。**反思可能发明记忆流中不存在的关系──缓解: trong反思提示包含来源记忆 ID 并在检查时验证──

Đây là các chế độ thất bại liên quan đến sản xuất: bất kỳ mô phỏng đại lý nào năm 2026 thừa kế chúng.

> Đây là những mô hình thất bại liên quan đến sản xuất: bất kỳ đại lý nào trong năm 2026 sẽ kế thừa chúng.

### Quy tắc thực hiện ba thành phần

1. **Memory is append-only.**Đừng bao giờ biến đổi một mục trong bộ nhớ.
   Trung ngữ翻译:**记忆只追加。**永远不修改记忆条目──更正是新条目──
2. **Importance scores are cheap.**Hãy gọi cho trường đại học để đánh giá tầm quan trọng 1-10 vào thời điểm viết.
   Trung ngữ翻译:**重要性分数是廉价的。**写入时调用 LLM 评分 1-10──缓存分数──
3. **Retrieval is ranked, not filtered.**Top-k theo điểm kết hợp; không sử dụng bộ lọc cứng (mà mất ngữ cảnh).
   Trung ngữ翻译:**检索是排序的，不是过滤的。**按综合分数取 top-k; đừng sử dụng cứng过(会丢失上下文)。
4. **Reflection runs periodically.**Trigger khi tổng số trọng lượng của các ký ức chưa được xử lý vượt quá ngưỡng (ví dụ: 150).
   Trung ngữ翻译:**反思定期运行。**Khi không xử lý nhớ tầm quan trọng tổng cộng vượt quá giá trị (ví dụ: 150)
5. **Plans are revisable.**Khi một quan sát mới mẻ mâu thuẫn với một kế hoạch, chỉ tái tạo phần bị ảnh hưởng, không phải toàn bộ kế hoạch.
   Trung ngữ翻译:**计划可修订。**Khi quan sát mới và kế hoạch mâu thuẫn, chỉ tái tạo phần bị ảnh hưởng, không phải toàn bộ kế hoạch.

### Các đại lý tạo ra ngoài Smallville

Văn học tiếp theo 2024-2026 mở rộng kiến trúc:

> Các tài liệu tiếp theo trong năm 2024-2026 mở rộng cấu trúc này:

- **Multi-agent social simulation for policy / market research.**Các nhóm người giống như Smallville mô phỏng hành vi của người dùng để đáp ứng các tính năng.
  Trung ngữ翻译:**用于政策/市场研究的多 Agent 社会模拟。**类似Smalville 的人群模拟用户对功能的响应──比 A/B 测试更快;准确性有争议──
- **NPC AI for games.**Các trò chơi RPG với các đại lý Smallville tạo ra các câu chuyện mới nổi thay vì các nhiệm vụ kịch bản.
  Trung ngữ翻译:**游戏 NPC AI。**Với vai trò của Smallville Agent, nó sẽ tạo ra một bộ phim kể chuyện nổi lên thay vì một nhiệm vụ kịch bản.
- **Generative-agent evaluation benchmarks.**Thay vì chính xác nhiệm vụ, số liệu trở thành khả năng tin cậy + sự liên kết của hành vi trong các thời gian dài.
  Trung ngữ翻译:**生成式 Agent 评估基准。**Và không phải là nhiệm vụ xác thực, chỉ số biến đổi cho thời gian dài hoạt động đáng tin cậy +  hành vi liên tục.

Kiến trúc là tham chiếu. Các phần mở rộng thay đổi thành phần (khám vector lưu trữ cho bộ nhớ, phản xạ tăng cường lấy, kế hoạch thần kinh) nhưng giữ lại cấu trúc ba phần.

> Các cấu trúc này là tham khảo.

### Tại sao điều này quan trọng đối với kỹ thuật đa đại lý

Smallville là bằng chứng về khái niệm rằng sự xuất hiện của nhiều đại lý rẻ khi các thành phần đúng. Kiến trúc đã được sao chép trên các mô hình nguồn mở (LLC nhỏ hơn mất tính đáng tin cậy một cách đẹp trai, không phải sắc bén). Bất kỳ hệ thống sản xuất nào cần **emergent social behavior**sử dụng hình dạng này.**tight task execution**sử dụng các mô hình giám sát viên / vai trò / nguyên thủy từ trước trong giai đoạn này.

> Smallville là một chứng minh khái niệm, cho thấy khi các thành phần đúng, nhiều đại lý xuất hiện là rẻ tiền.**涌现社会行为**Hệ thống sản xuất đều sử dụng hình thức này.**紧密任务执行**Hệ thống đều sử dụng mô hình giám sát viên/角色/原语模式.

## Hãy xây dựng nó.
```figure
a5-memory-reflection
```

## Hãy xây dựng nó

`code/main.py`thực hiện ba thành phần trong stdlib Python với chính sách đại lý kịch bản (không có LLM thực sự).

- `MemoryStream` chỉ thêm log với tính gần đây/sự quan trọng/sự liên quan.
  Trung ngữ翻译:`MemoryStream` 带时效性/重要性/相关性检索的仅额日志──
- `reflect(stream)` Nhận xét kịch bản về những kỷ niệm quan trọng gần đây.
  Trung ngữ翻译:`reflect` Đánh giá lại những ký ức quan trọng gần đây
- `plan(agent_state)` kế hoạch cấp ngày và cấp giờ dựa trên niềm tin hiện tại.
  Trung ngữ翻译:`plan` 基于当前信仰的日级和小时级计划──
- Kịch bản: 5 nhân viên, nhân viên 1 bắt đầu với "thay bữa tiệc vào 5 giờ chiều".
  Trung ngữ翻译:场景:5 个 代理──Agent 1 以"下午5 点办派对"开始──在模拟的时间步中,邀请传播,Agent 汇聚──

Đi chạy:

```
python3 code/main.py
```

Kết quả dự kiến: dấu vết tick-by-tick. Khi tick cuối cùng, ít nhất 3 trong số 5 đại lý cho thấy đảng trong kế hoạch của họ, và họ hội tụ tại địa điểm của đảng.

> 预期输出: từng bước theo dõi. Trong thời gian cuối cùng, ít nhất 3 trong số 5 đại lý trong kế hoạch cho thấy bữa tiệc, chúng tập hợp tại địa điểm bữa tiệc.

## Sử dụng nó.

`outputs/skill-simulation-designer.md`thiết kế mô phỏng đại lý tạo: số lượng đại lý, sơ đồ bộ nhớ, độ phản xạ, chân trời kế hoạch và métrics đánh giá.

> `outputs/skill-simulation-designer.md`设计一个生成式代理 模拟:Agent 数量、记忆模式、反思频率、计划范围和评估标志──

## Đưa nó lên mạng

Quy tắc đối với mô phỏng sản xuất:

- **Memory is the database.**Chọn một cửa hàng thực sự (vector DB, Postgres) trên quy mô.
  Trung ngữ翻译:**记忆是数据库。**Trong quy mô chọn thực tế lưu trữ (~ DB ∼ Postgres) ∼ trong lưu trữ các tiêu chuẩn chỉ được sử dụng cho nguyên mẫu ∼
- **Log the retrieval trace.**Với mỗi hành động, ghi lại những ký ức dẫn đến nó.
  Trung ngữ翻译:**记录检索轨迹。**Để mỗi động tác, ghi chép thúc đẩy nó ức nhớ top-k ở đây là khả năng điều tra của bạn ở đây.
- **Budget per-agent tokens.**Các đại lý lấy + phản xạ + kế hoạch mỗi tick là O(k) LLM cuộc gọi. N đại lý × T ticks × cuộc gọi-per-tick có thể làm nhỏ bé ngân sách của bạn.
  Trung ngữ翻译:**预算每 Agent token。**Mỗi đại lý Mỗi thời gian bước kiểm tra + phản hồi +  kế hoạch là O(k) lần LLM 调用。N 个 đại lý × T 个时间步 × 每时间步调用数可能让你的预算相形见──
- **Compact memory periodically.**Kết luận và cắt giảm các mục có tầm quan trọng thấp. Chính sách giữ lại là một quyết định thiết kế, không phải là chi tiết.
  Trung ngữ翻译:**定期压缩记忆。**摘要和修剪低重要性条目──保留策略是设计决策,不是细节──
- **Detect spatial / social norm violations**kiến trúc không học được chúng.
  Trung ngữ翻译:**显式检测空间/社会规范违规。**架构不会学习它们.

## Tập luyện bài tập

1. Đi chạy`code/main.py`- Đảm bảo 3 nhân viên hợp nhất tại bữa tiệc.
   Trung ngữ翻译:运行 `code/main.py`❖ xác nhận 3 đại lý 汇聚到派对── sẽ tăng lên 10 đại lý 涌现还会发生吗?
2. Làm thế nào để hành vi trông giống như? Bản đồ đến phát hiện của ablation trong Park 2023.
   Trung ngữ翻译:移除反思步骤──行为看起来怎么样?映射到园区 2023 的消融发现──
3. Hãy giới thiệu một mục tiêu được gieo giống cạnh tranh ("Klaus muốn nói chuyện nghiên cứu vào 5 giờ chiều").
   Trung ngữ翻译:引入一个竞争的种子目标("Klaus 想在下午5点做研究报告") ――Agent 会分裂还是一个目标主导?
4. Thêm những hạn chế không gian: Hobbs Cafe có tối đa 4 đại lý. Máy cầm mô phỏng tràn đầy sự hào nhoáng, hoặc nó chạm vào mô hình thất bại "tắm một người"?
   Trung ngữ翻译:添加空间约束:Hobbs Cafe 最多容纳 4 代理――模拟能优雅地处理溢出,还是会碰到"单人浴室"失败模式吗?
5. Đọc Park et al. (arXiv:2304.03442) Phần 6 (Các thí nghiệm hành vi mới nổi).
   Trung ngữ翻译:阅读 Park 等人(arXiv:2304.03442) 第 6 节(涌现行为实验) ―― nhận ra một hành vi không thể lặp lại trong phiên bản nhỏ của bạn―― bạn cần tăng cường cấu trúc?

## Từ khóa  Keyword

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Memory stream / 记忆流 | "The agent's diary" / "Agent 的日记" | Append-only log of observations, actions, reflections, plans. / 观察、行动、反思、计划的只追加日志。 |
| Recency / 时效性 | "How new is the memory" / "记忆有多新" | Exponential-decay score by age. / 按年龄的指数衰减分数。 |
| Importance / 重要性 | "How much does the agent care" / "Agent 有多在意" | Self-rated 1-10 at write time. Cached. / 写入时自评 1-10。已缓存。 |
| Relevance / 相关性 | "How related to the current query" / "与当前查询有多相关" | Cosine similarity (embedding-based). / 余弦相似度（基于嵌入）。 |
| Reflection / 反思 | "Higher-order belief" / "高阶信念" | Synthesis generated from recent memories, re-ingested as a new memory. / 从最近记忆生成的综合，作为新记忆重新摄入。 |
| Plan / 计划 | "Day/hour/action decomposition" / "日/小时/动作分解" | Top-down plan tree. Revisable when observations contradict. / 自顶向下计划树。观察矛盾时可修订。 |
| Smallville / 小镇 | "Park 2023's sandbox" / "Park 2023 的沙盒" | 25-agent simulation that produced the Valentine's Day emergence. / 25 个 Agent 的模拟，产生了情人节涌现。 |
| Believability / 可信度 | "The quality metric" / "质量指标" | Human-rater score for whether behavior seems like a plausible agent. / 人类评分者对行为是否像合理 Agent 的评分。 |

## Xem thêm 延伸阅读

- [Park et al. — Generative Agents: Interactive Simulacra of Human Behavior](https://arxiv.org/abs/2304.03442) kiến trúc tham chiếu
- [UIST '23 paper page](https://dl.acm.org/doi/10.1145/3586183.3606763) địa điểm xuất bản
- [Smallville code release](https://github.com/joonspk-research/generative_agents) thực hiện Python tham chiếu
- [Hayes-Roth 1985 — A Blackboard Architecture for Control](https://www.sciencedirect.com/science/article/abs/pii/0004370285900639) nghệ thuật trước đây cho các đại lý bộ nhớ có cấu trúc
