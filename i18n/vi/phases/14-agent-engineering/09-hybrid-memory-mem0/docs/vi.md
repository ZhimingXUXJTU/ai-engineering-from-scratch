# Tưởng thức lai: Vector + Graph + KV (Mem0) 混合记忆:向量+图+KV(Mem0)
# Tưởng nhớ lai: Vector + Graph + KV

> Bộ nhớ lai chạy ba cửa hàng song song  vector cho sự tương đồng ngữ nghĩa, KV cho tìm kiếm thực tế nhanh, biểu đồ cho lý luận mối quan hệ thực thể  với một lớp điểm số kết hợp chúng khi lấy lại. Đây là một mô hình sản xuất được sử dụng rộng rãi cho bộ nhớ bên ngoài; Mem0 (Chhikara et al., 2025) là một thực hiện tham chiếu.

> **【中文解读】**Mem0 sẽ xem trí nhớ như ba chuỗi lưu trữ  khối lượng được sử dụng cho ngữ nghĩa tương tự KV được sử dụng cho việc tìm kiếm thực tế nhanh chóng ∞ được sử dụng cho lý luận về quan hệ thực tế ∞ một cấp độ đánh giá trong quá trình tìm kiếm ∞ đây là tiêu chuẩn sản xuất trí nhớ bên ngoài năm 2026∞

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 07 (MemGPT), Phase 14 · 08 (Letta Blocks) | **前置知识:** Phase 14 · 07 (MemGPT), Phase 14 · 08 (Letta 块)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Mục tiêu học tập

- Giải thích lý do tại sao một kho lưu trữ duy nhất (chỉ vector, chỉ biểu đồ, chỉ KV) là không đủ cho bộ nhớ đại lý.
  Trung文翻译:解释为什么单一存储(仅向量、仅图、仅KV) không đủ để支 Agent 记忆──
- Hãy cho tên 3 cửa hàng song song của Mem0 và mỗi cửa hàng tối ưu hóa cho những gì.
  Trung ngữ翻译:说出 Mem0's三个并行存储及各自优化的目标──
- Mô tả điểm kết hợp của Mem0  liên quan, quan trọng, gần đây  và lý do tại sao nó là một tổng hợp cân nhắc, chứ không phải là một hệ thống phân cấp.
  Trung ngữ翻译:描述 Mem0的融合评分相关性,重要性,时效性以及为什么是加权和而非层级
- Thực hiện một bộ nhớ đồ chơi ba tầng trong stdlib với một `add()`- Nó viết cho cả ba và một.`search()`kết quả kết hợp.
  Trung文翻译:用标准库实现玩具三存储记忆,`add()`写入所有三个存储,`search()`Kết quả kết hợp

## Vấn đề  vấn đề giới thiệu

Một cửa hàng sai cho một trong ba lớp truy vấn:

> 单存储对三类查询之一是错误的:

- **Semantic similarity**"Chúng ta đã thảo luận về sự trôi dạt của đại lý tuần trước?" Vector thắng; KV và biểu đồ thất bại.
  Trung ngữ翻译:**语义相似性**"Chúng tôi đã thảo luận về việc đại lý 漂移 của?"
- **Fact lookup** "nọm điện thoại của người dùng là gì?" KV thắng; vector là lãng phí, biểu đồ là quá chết.
  Trung ngữ翻译:**事实查找**" User's phone number is what?" KV 胜出;向量浪费,图过度──
- **Relationship reasoning** "customers share the same billing entity?" Graph thắng; vector và KV không thể trả lời.
  Trung ngữ翻译:**关系推理**" Những khách hàng nào chia sẻ cùng một tính toán thực thể?" 图胜出;向量和 KV 无法回答──

Các đại lý sản xuất phát hành cả ba trong một phiên.`add`- Không.`search`bề mặt với một chức năng ghi điểm mà hợp nhất chúng.

>  **【类比】**3 hệ thống chỉ dẫn của Mem0: 量库像"按主题相关性"的智能推,KV库像"按书名/ISBN"的精确查找,KV库像"按书名/ISBN"的精确查找,KV库像"按作者-出版社-引用关系"的网络,KV库像"按作者-出版社-引用关系"的网络,KV库像"按作者-引用关系"的网络,KV库像"按作者-出版社-引用关系"的网络,KV库像"按作者-引用关系")

> Trong một cuộc họp, đại lý sản xuất gửi tất cả ba loại truy vấn. Một bộ nhớ lưu trữ duy nhất về hai loại này luôn là sai lầm.`add`- Không.`search`接口后面,并使用评分函数融合它们──

> **【中文解读】**混合记忆系统 (Mem0) kết hợp ký ức làm việc ngắn hạn và ký ức lâu dài. Trong cửa sổ sau, ký ức ngắn hạn sử dụng cơ sở dữ liệu và cơ sở dữ liệu hình ảnh.

> **【拓展：Mem0 是目前最流行的 Agent 记忆解决方案之一】**Mem0 (2024-2025) là một trong những giải pháp nhớ đại lý phổ biến nhất hiện tại,GitHub 25k+ ngôi sao.

>  **【前置】**必须先掌握:Phase 14·07(MemGPT) vàPhase 14·08(Letta Blocks) Mem0 là "khả năng lưu trữ cuối nâng cấp" của chúng.

## Khái niệm cốt lõi

### Ba cửa hàng song song

Mem0 (arXiv:2504.19413, tháng 4 năm 2025) ngày `add(text, user_id, metadata)`- Có thể là:

> Mem0(arXiv:2504.19413,2025 年 4 月) 在 `add(text, user_id, metadata)`上:

1. Thu thập các sự kiện ứng cử viên từ văn bản (một bước được thúc đẩy bởi LLM).
   Trung ngữ翻译:从文本中提取候选事实 (Làm việc làm theo quy tắc)
2. Viết từng sự thật vào kho vector (trình tích hợp) để tìm kiếm ngữ nghĩa.
   Trung ngữ翻译:将每个事实写入向量存储 (嵌入) dùng để语义搜索。
3. Viết từng dữ liệu vào kho KV được khóa vào (user_id, fact_type, entity) để tìm kiếm O(1).
   Trung文翻译:将每个事实写入 KV 存储,以 (user_id, fact_type, entity) 为键,实现 O(1) 查找。
4. Viết từng sự kiện vào kho đồ họa (Mem0g) như các cạnh được gõ cho các truy vấn mối quan hệ.
   Trung ngữ翻译:将每个事实写入图存储(Mem0g) như một loại hóa边, được sử dụng để hỏi mối quan hệ.

- Đưa ra`search(query, user_id)`- Có thể là:

> Trong `search(query, user_id)`上:

1. Vektor store trả lại top-k bằng cách nhúng cosine.
   Trung文翻译:向量存储按嵌入余弦相似度返回顶-k。
2. KV store trả về các truy cập trực tiếp được khóa trên truy vấn (user_id, type, entity).
   Trung文翻译:KV 存储返回基于查询推导的 (user_id, type, entity) 键的直接命中──
3. Graph store trả lại subgraph có thể truy cập từ các thực thể truy vấn.
   Trung ngữ翻译:图存储返回从查询实体可达的子图.
4. Một lớp điểm kết hợp ba.
   Trung ngữ翻译:评分层融合三者──

### Điểm số hợp nhất

```
score = w_relevance * relevance(q, record)
      + w_importance * importance(record)
      + w_recency * recency(record)
```

- **Relevance** vector cosine, KV chính xác phù hợp, trọng lượng đường biểu đồ.
  Trung ngữ翻译:**相关性**向量余弦、KV 精确匹配、图路径权重──
- **Importance** được gắn vào thời điểm viết hoặc được học (một số sự kiện quan trọng hơn: tên, ID, chính sách).
  Trung ngữ翻译:**重要性**写入时标记或学习得到 (((某些事实更重要:姓名、ID、策略)
- **Recency** suy giảm theo thời gian kể từ lần viết hoặc đọc cuối cùng.
  Trung ngữ翻译:**时效性** Từ lần viết hoặc đọc lần trước, chỉ số thời gian giảm đi.

Các trọng lượng được điều chỉnh theo sản phẩm.`w_recency`cho các đại lý trò chuyện; cao hơn `w_importance`cho các nhân viên tuân thủ; cao hơn `w_relevance`cho các nhân viên tìm kiếm.

> ️ **【易错点】**三种权重照搬 Mem0 论文默认值(如 0.4/0.4/0.2) trực tiếp trên线──**后果**Trong khi đó, các thông tin chính sách quan trọng như "thành khách này là người dùng giới hạn") đã bị áp lực bởi "ngày hôm qua của thời tiết", kiểm tra không đến vì `w_recency`太高,老的高重要性事实被时间衰减淹没了──**一行修复**: 上线前使用 20-30 个真实查询做 A/B 测试调权重,不同产品方向完全不同(聊天靠近期,合规靠重要)

> 权重按产品调优──聊天 代理 使用更高的 `w_recency`; 合规 Agent 使用更高的 `w_importance`;检索代理 使用更高的 `w_relevance`

### Mem0g và lý luận thời gian

Mem0g thêm một máy dò xung đột. Khi một sự kiện mới mâu thuẫn với một cạnh hiện có, cạnh hiện có được đánh dấu là không hợp lệ nhưng không bị xóa. Các truy vấn thời gian ("thành phố của người dùng vào tháng 3 là gì?") xuyên qua tiểu biểu hợp lệ tại thời gian.

> Mem0g đã thêm một máy kiểm tra xung đột. Khi những sự kiện mới và những mâu thuẫn hiện có, những mâu thuẫn hiện có được đánh dấu là không hiệu quả nhưng không được xóa bỏ.

Đây là hành vi cấp độ tuân thủ mô hình vô hiệu hóa của Letta nói chung.

> Đây là hành vi quy định của Letta 失效模式泛化.

### Số điểm chuẩn

Báo cáo của Mem0 (2025):

> Mem0 论文报告(2025):

- **LoCoMo**(khúc lưu dạng trò chuyện dài): 91.6
- **LongMemEval**(Tưởng thức tập thể dài chân trời): 93.4
- **BEAM 1M**(1M-token memory benchmark): 64.1

Các đường cơ sở so sánh (LLC đầy đủ ngữ cảnh 128k, kho vector phẳng, KV phẳng) đều mất hơn 10 điểm. Chỉ số chỉ đơn thuần không biện minh cho sự lựa chọn  hình dạng hoạt động  nhưng các số cho thấy thiết kế hợp nhất không phải là một lỗi tròn.

> So sánh cơ sở tuyến ((全上下文 128k LLM、平向量储存、平 KV) 都落后 10+ 分── chỉ bằng cơ sở chuẩn không thể chứng minh lựa chọn运营形态才行, nhưng số cho thấy kết hợp thiết kế không phải là một sự sai lầm trong bốn舍五入──

### Định dạng phân loại phạm vi

Mem0 chia trí nhớ theo phạm vi:

> Mem0 按范围拆分记忆:

- **User memory** kéo dài qua các phiên, được khóa vào `user_id`- Tôi không biết.
  Trung ngữ翻译:**用户记忆**跨会话持久化,以 `user_id`Vì thế.
- **Session memory** tồn tại trong một chuỗi.
  Trung ngữ翻译:**会话记忆** trong một đường dài.
- **Agent memory** trạng thái trường hợp mỗi đại lý.
  Trung ngữ翻译:**Agent 记忆** Mỗi đại lý 实例状态――

Mỗi bài viết chọn một phạm vi. Phục hồi có thể truy vấn qua phạm vi với trọng lượng mỗi phạm vi. Trộn phạm vi mà không suy nghĩ là cách bạn nhận được "hỗ trợ nói với Alice về dự án Bob" sự cố.

> 🤔 **【困惑】**Q: Mem0 三种储存必须部署运维, chi phí quá cao đối với nhóm nhỏ, có thể chỉ sử dụng kho lưu trữ khối lượng?**纯聊天机器人**UZ向量库 + KV đã đủ ((< 90% 复杂度);**多用户企业 Agent**( liên quan đến quyền hạn, quan hệ, quy định) phải sử dụng thư viện, nếu không sẽ xuất hiện "Alice nhìn thấy dữ liệu của Bob" như vậy.

> Mỗi lần viết chọn một phạm vi. Tìm kiếm có thể vượt qua phạm vi. Tìm kiếm có thể vượt qua phạm vi.

### Khi mô hình này đi sai

- **Embedding drift.**Kết quả vector trông đúng trên hàng trăm truy vấn đầu tiên giảm khi corpus phát triển. Thêm tái nhúng định kỳ các hồ sơ được sử dụng trên cùng.
  Trung ngữ翻译:**嵌入漂移。**Trước 100 lần truy vấn trông đúng kết quả khối lượng với các ngôn ngữ tăng và giảm.
- **KV schema creep.** `(user_id, type, entity)`trông đơn giản cho đến khi mỗi đội thêm một đội của riêng mình `type`- kiểm tra các loại thiết lập hàng quý.
  Trung ngữ翻译:**KV 模式蔓延。** `(user_id, type, entity)`Nhìn như đơn giản, cho đến khi mỗi đội thêm của riêng mình `type`❖ Các loại kiểm toán hàng tháng
- **Graph explosion.**Một máy thu hút tiếng ồn sẽ thêm 50 cạnh cho mỗi tin nhắn.`add`gọi; bỏ các cạnh thấp tự tin.
  Trung ngữ翻译:**图爆炸。**Một bộ rút thông tin mỗi lần thêm 50 biên giới giới hạn mỗi lần`add`调用图写入数; bỏ bỏ thấp置信度边缘.

## Hãy xây dựng nó.
```figure
ae-memory-fusion
```

## Hãy xây dựng nó

`code/main.py`thực hiện mô hình ba tầng trong stdlib:

> `code/main.py`Sử dụng tiêu chuẩn库 thực hiện ba chế độ lưu trữ:

- `VectorStore` sự tương đồng ngây thơ của token-overlap như một embedding stand-in.
  Trung ngữ翻译:`VectorStore` Sử dụng biểu tượng đơn giản 重叠相似性替代嵌入──
- `KVStore` dict được khóa vào `(user_id, fact_type, entity)`- Tôi không biết.
  Trung ngữ翻译:`KVStore`以 `(user_id, fact_type, entity)`Vì vậy, chúng tôi đã làm việc rất tốt.
- `GraphStore` các cạnh được đánh vào (chủ đề, mối quan hệ, đối tượng, hợp lệ).
  Trung ngữ翻译:`GraphStore`类型化边 ()
- `Mem0` mặt tiền cấp cao với `add()`- `search()`, điểm kết hợp, và thu thập tầm nhìn.
  Trung ngữ翻译:`Mem0`顶层门面,带 `add()``search()`、 kết hợp đánh giá và phạm vi nhận thức kiểm tra.
- Một dấu vết đã hoạt động trên một cuộc trò chuyện đa người dùng, đa phiên.
  Trung ngữ翻译:多用户、多会话对话的演练轨迹。

Đi đi.

> 运行:

```
python3 code/main.py
```

Kết quả phát xuất cho thấy ba đường gọi riêng biệt cộng với top-k hợp nhất. Chuyển các trọng lượng ghi điểm ở đầu của `main()`và xem xếp hạng thay đổi.

> 输出显示三条独立的召回路径加上融合的顶-k---在 `main()`顶部翻转评分权重观察排名变化──

## Hãy sử dụng nó để thực hiện

- **Mem0 (Apache 2.0)** sẵn sàng sản xuất. tự lưu trữ với Postgres + Qdrant + Neo4j, hoặc sử dụng đám mây quản lý.
  Trung ngữ翻译:**Mem0 (Apache 2.0)**生产就绪──用 Postgres + Qdrant + Neo4j 自托管,或使用托管云──
- **Letta** lõi/tái nhớ/bưu trữ ba cấp; mang lại các nền vector và biểu đồ của riêng bạn.
  Trung ngữ翻译:**Letta** 3 tầng lõi/hướng lại/bưu trữ;自带向量和图后端──
- **Zep** thay thế thương mại với KG thời gian và khai thác thực tế.
  Trung ngữ翻译:**Zep**带时序知识图谱和事实提取的商业替代方案──
- **Custom builds** khi bạn cần kiểm soát chính xác về chất thu hút (sự tuân thủ) hoặc trọng lượng hợp nhất (những chất gây âm thanh nơi sự gần đây chiếm ưu thế).
  Trung ngữ翻译:**自定义构建** khi bạn cần kiểm soát chính xác                                                                                                                                                                                                                                                           

## Chuyển nó đi.

`outputs/skill-hybrid-memory.md`tạo ra một cái bàn trí trí nhớ ba tầng với một điểm số kết hợp, phân loại phạm vi, và vô hiệu hóa thời gian được cáp vào.

> `outputs/skill-hybrid-memory.md`生成三存储记忆脚手架,内置融合评分器、范围分类和时序失效──

## Tập luyện bài tập

1. Thay thế sự tương đồng vector đồ chơi bằng một mô hình nhúng thực (những biến đổi câu, Ollama, nhúng OpenAI). đo recall@10 trên một cuộc trò chuyện dài tổng hợp.
   Trung ngữ翻译:将玩具向量相似性替换为真实嵌入模型──在合成长对话上测量 recall@10──1000次写入后排名会漂移?
2. Thêm truy vấn thời gian: `search(query, as_of=timestamp)`- Chỉ trả lại những hồ sơ hợp lệ vào thời điểm đó hoặc trước đó.
   Trung văn翻译:添加时序查询:`search(query, as_of=timestamp)` Chỉ quay lại thời gian này hoặc trước đây đã có hiệu lực                                                                                                                                                                                                                                                        
3. Thực hiện một máy dò xung đột: nếu một sự kiện đến trái ngược với một cạnh biểu đồ, vô hiệu hóa cạnh cũ và ghi cả hai.
   Trung ngữ翻译:实现冲突检测器:如果传入事实与图边矛盾,使旧边失效并记录两者──用"user lives in Berlin" -> "user lives in Lisbon"测试──
4. Port điểm kết hợp để bao gồm một `user_feedback`kích thước (đánh tay lên trên các hồ sơ được lấy lại). Làm thế nào để ngăn chặn trò chơi (nhà chỉ trả lại các hồ sơ mà họ đã thích)?
   Trung文翻译:将融合评分器移植为包含 `user_feedback`维度──如何防止操纵?
5. Đọc các tài liệu Mem0 (`docs.mem0.ai` ). Đưa đồ chơi vào `mem0`So sánh chất lượng thu hồi trên cùng 20 truy vấn thử nghiệm.
   Trung文翻译:阅读 Mem0 文档――将玩具移植为 `mem0`客户端调用──比较相同 20 测试查询的检索质量──

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Hybrid memory | "Vector plus graph plus KV" / "向量加图加 KV" | Three stores written in parallel, fused on retrieval / 三个存储并行写入，检索时融合 |
| Fact extraction | "Memory ingestion" / "记忆摄取" | LLM step that breaks text into (entity, relation, fact) tuples / 将文本拆分为（实体、关系、事实）元组的 LLM 步骤 |
| Fusion scoring | "Relevance ranking" / "相关性排序" | Weighted sum of relevance, importance, recency / 相关性、重要性、时效性的加权和 |
| Scope | "Memory namespace" / "记忆命名空间" | user / session / agent — determines who sees what / 用户/会话/Agent——决定谁看到什么 |
| Mem0g | "Memory graph" / "记忆图" | Typed edges with temporal validity for relationship queries / 带时序有效性的类型化边，用于关系查询 |
| Temporal invalidation | "Soft delete" / "软删除" | Mark contradicted edges invalid; never delete / 标记矛盾边为无效；永不删除 |
| Embedding drift | "Retrieval rot" / "检索腐化" | Vector quality degrades as corpus grows; re-embed periodically / 向量质量随语料增长退化；定期重新嵌入 |

## Xem thêm 延伸阅读

- [Chhikara et al., Mem0 (arXiv:2504.19413)](https://arxiv.org/abs/2504.19413) giấy gốc
  Trung văn翻译:Mem0 原始论文。
- [Mem0 docs](https://docs.mem0.ai/platform/overview) API sản xuất, SDK, đám mây quản lý
  Trung文翻译:Mem0 文档生产 API、SDK、托管云。
- [Packer et al., MemGPT (arXiv:2310.08560)](https://arxiv.org/abs/2310.08560) người tiền nhiệm của ngữ cảnh ảo
  Trung ngữ翻译:MemGPT 论文虚拟上下文的前身──
- [Letta, Memory Blocks blog](https://www.letta.com/blog/memory-blocks) thiết kế ba cấp
  Trung文翻译:Letta 记忆块博客三层兄弟设计。
