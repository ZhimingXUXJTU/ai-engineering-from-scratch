# Advanced RAG (Chunking, Ranking, Hybrid Search) 

> RAG cơ bản lấy các phần tương tự nhất trên k. Điều đó hoạt động cho các câu hỏi đơn giản. Nó bị phá vỡ cho lý luận đa hop, các truy vấn mơ hồ và các cơ quan lớn. RAG nâng cao là sự khác biệt giữa một bản demo hoạt động trên 10 tài liệu và một hệ thống hoạt động trên 10 triệu.

> **【中文解读】**基础 RAG 检索 top-k 相似块, thích hợp cho các câu hỏi đơn giản. Nhưng trong nhiều suy luận, các câu hỏi khác nhau và các nội dung quy mô lớn sẽ không hiệu quả.

> **【拓展：高级RAG→金融场景】**金融研报分析需要多跳推理 (跨文档关联数据),混合搜索 (混合搜索) (关键词+语义) có thể tăng đáng kể tỷ lệ kiểm tra dữ liệu tài chính.

>  **【前置】**学本节前请先掌握:Phase 11·06(RAG) 理解基础RAG 流程。本节是其进阶,假设你已经能写出 chunk→embed→retrieve→prompt→generate 的最小可用RAG。会用 `chromadb``rank_bm25``sentence-transformers`Hoặc`cohere`Đổi cấp API.

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 11, Lesson 06 (RAG) | **前置知识:** Phase 11 · 06 (RAG)
**Time:** ~90 minutes | **时间:** ~90 分钟
**Related:**Giai đoạn 5 · 23 (Chunking Strategies for RAG) bao gồm tất cả sáu thuật toán chunking  tái phát, ngữ nghĩa, câu, tài liệu cha mẹ, chunking muộn, truy xuất ngữ cảnh  với các tiêu chuẩn Vectara / Anthropic. Bài học này xây dựng trên đỉnh: tìm kiếm lai, xếp hạng lại, chuyển đổi truy vấn.**相关:**Giai đoạn 5 · 23(RAG 分块策略) bao gồm tất cả sáu loại phân khối thuật toán递归、语义、句子、父文档、晚分块、上下文检索含 Vectara/Anthropic基准──本课在其上构建:混合搜索、重排、查询转换──

## Mục tiêu học tập

- Thực hiện các chiến lược phân chia tiên tiến (tanthau nghĩa, thu hồi, cha mẹ-child) để bảo vệ cấu trúc và bối cảnh tài liệu
  实现保留文档结构和上下文的高级分块策略 (语义、递归、父子)
- Xây dựng một đường ống tìm kiếm lai kết hợp từ khóa BM25 phù hợp với tìm kiếm vector ngữ nghĩa và một trình xếp hạng lại mã hóa chéo
  构建结合 BM25 关键词匹配、语义向量搜索和交叉编码器重排器的混合搜索管线
- Sử dụng kỹ thuật chuyển đổi truy vấn (HyDE, nhiều truy vấn, bước trở lại) để cải thiện việc truy cập vào các câu hỏi mơ hồ hoặc phức tạp
  应用查询转换技术(HyDE、多查询、step-back) cải thiện模糊或复杂问题的检查
- Chẩn đoán và khắc phục các lỗi RAG phổ biến: lấy lại phần sai, trả lời không trong ngữ cảnh, phân tích lý luận đa hop
  诊断和修复常见 RAG 失败:检索错块、答案不上下文中、多跳推理崩

> **【中文解读】**Mục tiêu của bài học: nắm bắt các kỹ thuật cao cấp RAG 技术查询重写、混合检索、重排序、自适应检索、多跳推理──这些技术解决基础 RAG 在复杂查询上的局限性──

>  **【类比】**基础 RAG 像新手图书管理员你说"营收",他按字面找带"营收"的书──高级RAG 像资深管理员:(1) **Query 改写** nói "营收", ông dịch thành "上一季度财报中的收入数字"再找;**混合搜索**既翻主题目录 (语义) 又翻关键词索引 (BM25),两边结果合并;(3) **重排**召回100本后,仔细看每本摘要排序挑出最相关的5本(cross-encoder)

> ️ **【易错点】**高级 RAG 的 3 个坑:(1) **HyDE 用错场景**HyDE( để LLM trước tạo giả thuyết trả lời lại sử dụng trả lời kiểm tra) trong thực tế tìm kiếm ngược lại sai lầm kiểm tra; chỉ có hiệu quả đối với vấn đề mở.**重排模型选错** Sử dụng bi-encoder khi cross-encoder rranker(như BGE-M3 tự重排自己), không nhận được sự tăng cường độ độ của cross-encoder thực sự; sử dụng đặc biệt BGE-renker-v2、Cohere Rranker──(3) **混合搜索没归一化**BM25 分数 0-30,向量相似度 0-1,直接相加向量永远被淹没; dùng tương ứng cấp độ hợp nhất (RRF) hoặc tối thiểu 归一化。

> 🤔 **【困惑】**Q: 多跳推理该让模型做还是检索做? A: 检索做. 让模型在快速里推理,每跳检索一次,把上一跳结果作为下一跳查询的输入. Ví dụ:"哪个团队满意度升高最大?"→先检索"所有团队满意度分数"→让模型比较→得出"A 团队"→再检索"A 团队详细"――一跳一次检索,避免一次性塞所有可能相关文档――


## Vấn đề  vấn đề giới thiệu

Bạn đã xây dựng một đường ống dẫn RAG cơ bản trong bài học 06 nó hoạt động cho các câu hỏi đơn giản trên một tập hợp nhỏ.

> Bạn đã xây dựng một nền tảng RAG 流水线. Nó có hiệu quả đối với các vấn đề trực tiếp trên các thư viện ngôn ngữ nhỏ.

**Ambiguous query**"Thiết kế doanh thu quý trước là gì?" Tìm kiếm ngữ nghĩa trả về các phần về chiến lược doanh thu, dự báo doanh thu và suy nghĩ của CFO về tăng trưởng doanh thu. Tất cả đều tương tự như từ " doanh thu". Không có một phần nào chứa số thực tế. Phần chính xác nói "$47.2M in Q3 2025" but uses the word "earnings" instead of "revenue." The embedding model thinks "revenue strategy" is closer to the query than "Q3 earnings were $47,2M".

> **模糊查询**:"Quá số doanh thu trong quý trước?" Từ ngữ tìm kiếm trả về về chiến lược doanh thu, dự báo doanh thu và CFO về quan điểm tăng trưởng doanh thu.

**Multi-hop question**"Đội nào có điểm số hài lòng khách hàng tốt nhất?" Điều này đòi hỏi phải tìm kiếm điểm số hài lòng cho mỗi nhóm, so sánh chúng và xác định tối đa.

> **多跳问题**:"Điều gì trong nhóm đạt được điểm số hài lòng khách hàng cao nhất?" Điều này cần tìm thấy điểm số hài lòng của mỗi nhóm, so sánh chúng, và xác định giá trị tối đa. Không có một đoạn nào có chứa câu trả lời.

**Large corpus problem**Bạn có 2 triệu khối. Câu trả lời chính xác là trong phần #1,847,293. Tìm kiếm top-5 của bạn kéo các khối # 14, #89,201, #1,200,000, #44, và #901,333. đóng trong không gian nhúng, nhưng không có chứa câu trả lời. Ở quy mô này, tìm kiếm hàng xóm gần nhất đưa ra lỗi đủ để kết quả liên quan được đẩy ra khỏi top-k.

> **大型语料库问题**: bạn có 2 triệu đoạn phim. Đáp chính xác trong số 1.847.293 đoạn phim. Top 5 của bạn đã tìm ra các đoạn phim khác.

RAG cơ bản thất bại vì sự tương đồng vector không giống nhau với sự liên quan. Một phần có thể tương tự như một câu hỏi mà không hữu ích để trả lời nó. Advanced RAG giải quyết vấn đề này bằng bốn kỹ thuật: tìm kiếm lai (số kết hợp từ khóa), xếp hạng lại (số ứng viên cẩn thận hơn), chuyển đổi truy vấn (làm chính xác truy vấn trước khi tìm kiếm) và phân tích tốt hơn (tại lại với độ phân tích đúng).

> 基础 RAG 失败是因为向量相似度不等于相关性──高级 RAG sử dụng bốn loại kỹ thuật giải quyết:混合搜索(添加关键词匹配)、重排序(更仔细评分候选人)、查询转换(搜索前修复查询) 和更好的分块(以正确的粒度检查)。

## Khái niệm cốt lõi

> **【中文解读】**Cao cấp RAG 技术解决基础 RAG 局限性:查询重写将模糊问题转为精确查询) 混合检索(向量 + 关键词) 重排序(使用跨编码器 精排) 自适应检索(判断是否需要检索) 多跳推理(分解复杂问题为多次检索) 

> **【拓展：高级 RAG 的工业应用】**生产级 RAG 系统 thường bao gồm: 查询意图分类到查询扩展/重写到混合检索(BM25 + 向量) đến Cross-encoder 重排序到上下文缩写到答案生成 + 引用标注。Notion AI、Perplexity 等产品都使用高级 RAG 技术──Self-RAG 让模型自己决定何时检索──


### Tìm kiếm lai: ngữ nghĩa + từ khóa

Tìm kiếm ngữ nghĩa (sự tương tự vector) là tốt để hiểu ý nghĩa. "Tôi hủy đăng ký của tôi như thế nào?" phù hợp với "Các bước để chấm dứt kế hoạch của bạn" mặc dù họ không chia sẻ các từ. Nhưng nó không có sự phù hợp chính xác. "Công mã lỗi E-4021" có thể không phù hợp với một phần chứa "E-4021" nếu mô hình nhúng xử lý nó như tiếng ồn.

> 语义搜索(向量相似度)擅长理解含义──"如何取消订阅?"匹配"终止计划的步骤"尽管不共享单词──但它错过精确匹配──"错误码 E-4021"可能不匹配包含"E-4021"的块,如果嵌入模型将视为噪音──

Tìm kiếm từ khóa (BM25) là ngược lại. Nó xuất sắc khi phù hợp chính xác. "E-4021" phù hợp hoàn hảo. Nhưng "hoái đăng ký của tôi" trả lại kết quả không nếu tài liệu nói "hoái kế hoạch của bạn".

> 关键词搜索(BM25)相反──它擅长精确匹配──"E-4021"完美匹配──但"取消我的订阅"如果文档说"终止你的计划"则返回零结果──

Tìm kiếm lai chạy cả hai, sau đó kết hợp kết quả.

> 混合搜索同时运行两者,然后合并结果──

**BM25**(Best Matching 25) là thuật toán tìm kiếm từ khóa tiêu chuẩn. Nó đã là xương sống của các công cụ tìm kiếm kể từ những năm 1990. Công thức:

> **BM25**(Best Matching 25) là tiêu chuẩn từ khóa tìm kiếm. Từ năm 1990 là trụ cột của công cụ tìm kiếm.

```
BM25(q, d) = sum over terms t in q:
    IDF(t) * (tf(t,d) * (k1 + 1)) / (tf(t,d) + k1 * (1 - b + b * |d| / avgdl))
```

Trong khi tf(t,d) là t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t t

> Trong số đó, tf(t,d) là t trong văn bản d 中的词频,IDF(t) là ngược văn bản频率,

Nói một cách đơn giản: BM25 đánh giá cao hơn tài liệu khi chúng chứa các thuật ngữ truy vấn (đặc biệt là những thuật ngữ hiếm), nhưng với lợi nhuận giảm đối với các thuật ngữ lặp đi lặp lại.

> 简而言之:BM25 给包含查询词 (尤其是稀有词) 的文档更高分,但重复词有递减收益.

### Phối hợp cấp độ tương đối (RRF)

Bạn có hai danh sách xếp hạng: một từ tìm kiếm vector, một từ BM25. Làm thế nào để kết hợp chúng?

> Bạn có hai thứ tự danh sách: một từ khối lượng tìm kiếm, một từ BM25.

```
RRF_score(d) = sum over rankings R:
    1 / (k + rank_R(d))
```

K là một liên tục (thường là 60) ngăn cản kết quả xếp hạng hàng đầu thống trị.

> Trong đó k là số thường (tương tự là 60), ngăn ngừa xếp hạng đầu tiên của kết quả chủ đạo.

Một tài liệu xếp hạng #1 trong tìm kiếm vector và #5 trong BM25 nhận được: 1/(60+1) + 1/(60+5) = 0.0164 + 0.0154 = 0.0318

Một tài liệu xếp hạng #3 trong tìm kiếm vector và #2 trong BM25 nhận được: 1/(60+3) + 1/(60+2) = 0.0159 + 0.0161 = 0.0320

> Trong số đó, số lượng người tìm kiếm được xếp hạng thứ nhất, số lượng người tìm kiếm được xếp hạng thứ nhất, số lượng người tìm kiếm được xếp hạng thứ nhất, số lượng người tìm kiếm được xếp hạng thứ nhất, số lượng người tìm kiếm được xếp hạng thứ nhất, số lượng người tìm kiếm được xếp hạng thứ nhất, số lượng người tìm kiếm được xếp hạng thứ nhất, số lượng người tìm kiếm được xếp hạng thứ nhất, số lượng người tìm kiếm được xếp hạng thứ nhất, số lượng người tìm kiếm được xếp hạng thứ nhất, số lượng người tìm kiếm được xếp hạng thứ nhất, số lượng người tìm kiếm được xếp hạng thứ nhất, số lượng người tìm kiếm được xếp hạng thứ nhất, số lượng người tìm kiếm được xếp hạng thứ nhất, số lượng người tìm kiếm được xếp hạng thứ nhất, số lượng người tìm kiếm được xếp hạng thứ nhất, số lượng người tìm kiếm được xếp hạng thứ nhất, số lượng người tìm kiếm được xếp hạng thứ nhất, số lượng người tìm kiếm được xếp hạng thứ nhất, số lượng người tìm kiếm được xếp hạng thứ nhất, số lượng người tìm kiếm được xếp hạng thứ nhất, số lượng người tìm kiếm được xếp hạng thứ nhất, số lượng người tìm kiếm được xếp hạng thứ nhất, số lượng người tìm kiếm được xếp hạng thứ nhất, số lượng người tìm kiếm được xếp hạng thứ nhất, số lượng người tìm kiếm được xếp hạng thứ nhất, số lượng người tìm kiếm được xếp hạng thứ nhất, số lượng người tìm kiếm được xếp hạng thứ nhất, số lượng người tìm kiếm được xếp hạng thứ nhất, số lượng người tìm kiếm được xếp hạng thứ nhất, số lượng người tìm kiếm được xếp hạng thứ nhất, số lượng người tìm kiếm được xếp hạng thứ nhất, số lượng người tìm kiếm được xếp hạng thứ nhất, số lượng người tìm kiếm được xếp hạng thứ nhất, số lượng người tìm kiếm được xếp hạng nhất, số lượng người tìm kiếm được xếp hạng nhất, số lượng người tìm kiếm được xếp hạng nhất, số lượng người tìm kiếm được xếp hạng nhất, số lượng người tìm kiếm, số số số lượng người tìm kiếm được xếp hạng nhất, số số số số số số số số số số số số số số số số số số số số số số số số số số số số số số số số số số số số số số số số số số số số số số số số số số số số số số số số số số số số số số số số số số số số số số số số số số

RRF tự nhiên cân bằng hai tín hiệu. Một tài liệu xếp hạng cao trong cả hai danh sách nhận được điểm số tốt nhất. Một tài liệu xếp hạng #1 trong một danh sách nhưng vắng mặt trong danh sách khác nhận được điểm số trung bình. Điều này mạnh mẽ bởi vì nó sử dụng xếp hạng, không sử dụng điểm số thô, vì vậy sự khác biệt về phân phối điểm số giữa hai hệ thống không quan trọng.

> RRF tự nhiên cân bằng hai tín hiệu. Trong hai danh sách, tất cả các tài liệu xếp hạng cao đều có điểm cao nhất. Trong một danh sách xếp hạng đầu tiên nhưng trong danh sách khác, tài liệu thiếu có điểm trung bình.

### Tái xếp hạng

Khám truy xuất (dù là vector, keyword, hoặc hybrid) là nhanh nhưng không chính xác. Nó sử dụng các mã hóa hai: truy vấn và mỗi tài liệu được nhúng độc lập, sau đó so sánh. Các nhúng được tính toán một lần và được lưu trữ trong cache. Điều này có thể đạt đến hàng triệu tài liệu.

> 检索(无论向量、关键词还是混合)快但不精确──它 sử dụng hai bộ lập trình:查询和每个文档独立嵌入,然后比较──嵌入计算一次并缓存──这可扩展到百万文档──

Việc xếp hạng lại sử dụng các mã hóa chéo: truy vấn và tài liệu ứng cử viên được đưa vào một mô hình đưa ra điểm liên quan. Mô hình nhìn thấy cả hai văn bản cùng một lúc và có thể nắm bắt các tương tác tinh tế giữa chúng. Một mã hóa chéo có thể hiểu rằng "Lợi nhuận Q3 là gì?" rất có liên quan đến một phần có chứa "$47.2M trong Q3" ngay cả khi một mã hóa đôi bỏ lỡ kết nối.

> 重排使用交叉编码器: Query và ứng cử viên cùng nhau nhập một mô hình của các phân tích liên quan đến đầu ra. Mô hình cùng nhìn thấy hai đoạn văn bản, có thể nắm bắt sự tương tác nhỏ giữa chúng.

Sự đổi giá: cross-encoder là 100-1000x chậm hơn các bi-encoder vì họ xử lý cặp truy vấn-tài liệu cùng nhau. Bạn không thể tính toán trước điểm số cross-encoder cho một triệu tài liệu. Giải pháp: lấy một tập hợp ứng cử viên lớn hơn (top-50 từ tìm kiếm lai), sau đó xếp hạng lại với một cross-encoder để có được top-5 cuối cùng.

> 权衡:交叉编码器比双编码器慢100-1000倍, vì nó hợp tác xử lý truy vấn-档对――你无法为百万档预计算交叉编码器分数――解决方案:检索更大候选集(混合搜索 top-50), sau đó sử dụng交叉编码器重排得到最终 top-5――

```mermaid
graph LR
    Q["Query"] --> H["Hybrid Search"]
    H --> C50["Top 50 candidates"]
    C50 --> RR["Cross-Encoder Reranker"]
    RR --> C5["Top 5 final results"]
    C5 --> P["Build prompt"]
    P --> LLM["Generate answer"]
```

Các mô hình xếp hạng lại phổ biến (2026 lineup):

> 常见重排模型(2026 年阵容):

- Cohere Rerank 3.5: quản lý API, đa ngôn ngữ, lợi ích nhớ tốt nhất trên các cơ quan hỗn hợp
  托管 API、多语言、混合语料
- Đơn vị xếp hạng lại của Voyage-2.5: API được quản lý, thời gian trễ thấp nhất trong các tùy chọn được lưu trữ
  托管 API、托管选项 trong thời gian trễ tối thiểu
- Jina-Reranker-v2 Nhiều ngôn ngữ: trọng lượng mở, hơn 100 ngôn ngữ
  开源权重、100+ 语言
- bge-re-ranker-v2-m3: trọng lượng mở, cơ sở mạnh
  开源权重、强基线
- cross-encoder/ms-marco-MiniLM-L-6-v2: Open-weight, chạy trên CPU để tạo mẫu
  开源权重、可在CPU上运行原型
- ColBERTv2 / Jina-ColBERT-v2: Interaction Late-Multi-vector Ranger  O(tokens) không O(docs) tại thời điểm ghi điểm
  后期交互多向量重排器评分时 O(tokens) chứ không phải O(docs)

### Query Transformation

Đôi khi vấn đề không phải là tìm kiếm mà chính là câu hỏi. "Điều đó là gì về sự thay đổi chính sách mới?" là một câu hỏi tìm kiếm khủng khiếp. Nó không chứa các thuật ngữ cụ thể. Việc nhúng là mơ hồ. Không có hệ thống tìm kiếm nào có thể tìm thấy các tài liệu phù hợp từ điều này.

> Đôi khi vấn đề không phải là tìm kiếm mà là tìm kiếm chính nó. "Thứ gì là sự thay đổi chính sách mới?" là tìm kiếm tồi tệ. Nó không có chứa các từ cụ thể.

**Query rewriting**: tái định nghĩa truy vấn của người dùng thành truy vấn tìm kiếm tốt hơn.

> **查询重写**:将用户查询重述为更好的搜索查询――LLM 可做这件事:

```
User: "What was that thing about the new policy change?"
Rewritten: "Recent policy changes and updates"
```

**HyDE (Hypothetical Document Embeddings)**: thay vì tìm kiếm với câu hỏi, tạo ra một câu trả lời giả thuyết, nhúng vào đó, và tìm kiếm các tài liệu thực tương tự.

> **HyDE（假设文档嵌入）**: không cần tìm kiếm tìm kiếm, mà tạo ra giả định trả lời, nhúng vào nó, tìm kiếm giống như các tài liệu thực sự.

```
Query: "What is the refund policy for enterprise?"
Hypothetical answer: "Enterprise customers are eligible for a full refund
within 60 days of purchase. Refunds are pro-rated based on the remaining
subscription period and processed within 5-7 business days."
```

Nhập câu trả lời giả thuyết và tìm kiếm các tài liệu thực tương tự nó. Nhận thức: câu trả lời giả thuyết sống gần hơn trong không gian nhúng vào câu trả lời thực hơn câu hỏi ban đầu. Câu hỏi và câu trả lời có cấu trúc ngôn ngữ khác nhau. Bằng cách tạo ra câu trả lời giả thuyết, bạn sẽ thu hẹp khoảng cách giữa "không gian câu hỏi" và "không gian trả lời" trong nhúng.

> 嵌入假设答案并搜索与它相似的真实文档――直觉:假设答案在嵌入空间中比原始问题更接近真实答案――问题和答案有不同的语言结构――通过生成假设答案,你弥合嵌入中的"问题空间"和"答案空间"的差距――

HyDE thêm một cuộc gọi LLM trước khi truy xuất. Điều này làm tăng độ trễ 500-2000ms.

> HyDE trong kiểm tra trước thêm một lần LLM 调用──This increased 500-2000ms 延迟──原始查询检索质量差时值──

### Bắt đầu với con

Việc làm phân mảnh thông thường buộc phải thỏa hiệp: các mảnh nhỏ để lấy lại chính xác, các mảnh lớn để đủ bối cảnh.

> 标准分块强制权衡:小块精确检索,大块足够上下文──父子分块消除这个权衡──

Chỉ số các đoạn nhỏ (128 token) để lấy lại. Khi một đoạn nhỏ được lấy lại, hãy trả lại phần mẹ của nó (512 token) cho lời nhắc. Phần nhỏ phù hợp chính xác với truy vấn. Phần mẹ cung cấp đủ bối cảnh để LLM tạo ra một câu trả lời tốt.

> 索引小块(128 token) được sử dụng để kiểm tra. 检索到小块时,返回其父块.

```mermaid
graph TD
    P["Parent chunk (512 tokens)<br/>Full section about refund policy"]
    C1["Child chunk (128 tokens)<br/>Standard plan: 30-day refund"]
    C2["Child chunk (128 tokens)<br/>Enterprise: 60-day pro-rated"]
    C3["Child chunk (128 tokens)<br/>Processing time: 5-7 days"]
    C4["Child chunk (128 tokens)<br/>How to submit a request"]

    P --> C1
    P --> C2
    P --> C3
    P --> C4

    Q["Query: enterprise refund?"] -.->|"matches child"| C2
    C2 -.->|"return parent"| P
```

Câu hỏi "trái tiền doanh nghiệp?" phù hợp với phần nhỏ C2 chính xác. Nhưng lời nhắc nhận nhận phần chính đầy đủ P, bao gồm bối cảnh xung quanh về thời gian xử lý và quá trình gửi.

> 查询"trái hoàn doanh nghiệp?" chính xác phù hợp với khối C2── nhưng gợi ý nhận toàn bộ khối P, bao gồm về thời gian xử lý và đề xuất các quá trình trao đổi.

### Phân lọc metadata

Trước khi chạy tìm kiếm vector, lọc bộ phận theo metadata: ngày, nguồn, loại, tác giả, ngôn ngữ. Điều này làm giảm không gian tìm kiếm và ngăn chặn kết quả không liên quan.

> Trong quá trình tìm kiếm khối lượng, theo số liệu của các nhà nghiên cứu, các nhà nghiên cứu đã tìm kiếm các kết quả không liên quan.

"Điều gì đã thay đổi trong chính sách bảo mật tháng trước?" chỉ nên tìm kiếm tài liệu từ 30 ngày qua trong danh mục bảo mật. Không lọc siêu dữ liệu, bạn tìm kiếm toàn bộ bộ và có thể lấy lại một tài liệu bảo mật 2 năm tuổi mà xảy ra tương tự về ngữ nghĩa.

> "Các chiến lược an ninh trong tháng trước có gì thay đổi?" chỉ nên tìm kiếm trong 30 ngày qua các tài liệu về an ninh không có dữ liệu quá, bạn tìm kiếm toàn bộ bộ bộ tài liệu, có thể tìm kiếm một tài liệu an ninh tương tự như 2 năm trước.

Hệ thống sản xuất RAG lưu trữ metadata bên cạnh từng phần: tài liệu nguồn, ngày tạo, loại, tác giả, phiên bản. Các cơ sở dữ liệu vector hỗ trợ lọc trước bằng metadata trước khi tìm kiếm tương đồng, điều này rất quan trọng đối với hiệu suất ở quy mô.

> 生产 RAG 系统在每个块旁边存储元数据:源文档、创建日期、类别、作者、版本──向量数据库支持相似度搜索前按元数据预过, điều này rất quan trọng đối với hiệu suất quy mô lớn.

### Đánh giá

Anh đã xây dựng một hệ thống RAG. Làm sao anh biết nó có hoạt động không?

> Bạn đã xây dựng hệ thống RAG... làm thế nào để biết nó hiệu quả?

**Retrieval relevance (Recall@k)**: cho một tập hợp các câu hỏi thử nghiệm với các tài liệu có liên quan được biết, bao nhiêu phần trăm tài liệu có liên quan xuất hiện trong kết quả top-k?

> **检索相关性（Recall@k）**: Đối với một nhóm các câu hỏi kiểm tra có liên quan đến các tài liệu đã biết, tỷ lệ phần trăm tài liệu xuất hiện trong kết quả top-k là bao nhiêu? Nếu một câu hỏi được trả lời ở 47 khối, 47 khối có xuất hiện trong top-5 không?

**Faithfulness**Nếu các phần được lấy lại nói "trung cửa hàng hoàn trả 60 ngày" và mô hình nói "trung cửa hàng hoàn trả 90 ngày", đó là một sự thất bại. mô hình ảo giác mặc dù có bối cảnh chính xác.

> **忠实度**Nếu một khối kiểm tra nói "60 天退款窗口" và mô hình nói "90 天退款窗口", đó là sự trung thành thất bại.

**Answer correctness**: câu trả lời được tạo tương ứng với câu trả lời mong đợi? Đây là chỉ số kết thúc đến kết thúc. Nó kết hợp chất lượng thu thập và chất lượng sản xuất.

> **答案正确性**: kết quả của kết quả có phù hợp với kết quả của kết quả?

Một kiểm tra độ trung thực đơn giản: lấy từng tuyên bố trong câu trả lời được tạo và xác minh rằng nó xuất hiện (trong chất lượng) trong các mảnh thu hồi. Nếu câu trả lời có một sự thật không trong bất kỳ mảnh thu hồi nào, nó có thể bị ảo giác.

> 简单忠实检查:取生成答案中的每个声明,验证它(实质上) xuất hiện trong khối kiểm tra. Nếu câu trả lời không chứa các sự kiện trong bất kỳ khối kiểm tra nào, nó rất có thể bị hình dung.

```mermaid
graph TD
    subgraph "Evaluation Framework"
        Q["Test questions<br/>+ expected answers<br/>+ relevant doc IDs"]
        Q --> Ret["Retrieval evaluation<br/>Recall@k: are right<br/>docs retrieved?"]
        Q --> Faith["Faithfulness evaluation<br/>Is answer grounded<br/>in retrieved docs?"]
        Q --> Correct["Correctness evaluation<br/>Does answer match<br/>expected answer?"]
    end
```

## Hãy xây dựng nó.
```figure
agentic-rag-loop
```

## Hãy xây dựng nó

### Bước 1: Thực hiện BM25

```python
import math
from collections import Counter

class BM25:
    def __init__(self, k1=1.2, b=0.75):
        self.k1 = k1
        self.b = b
        self.docs = []
        self.doc_lengths = []
        self.avg_dl = 0
        self.doc_freqs = {}
        self.n_docs = 0

    def index(self, documents):
        self.docs = documents
        self.n_docs = len(documents)
        self.doc_lengths = []
        self.doc_freqs = {}

        for doc in documents:
            words = doc.lower().split()
            self.doc_lengths.append(len(words))
            unique_words = set(words)
            for word in unique_words:
                self.doc_freqs[word] = self.doc_freqs.get(word, 0) + 1

        self.avg_dl = sum(self.doc_lengths) / self.n_docs if self.n_docs else 1

    def score(self, query, doc_idx):
        query_words = query.lower().split()
        doc_words = self.docs[doc_idx].lower().split()
        doc_len = self.doc_lengths[doc_idx]
        word_counts = Counter(doc_words)
        score = 0.0

        for term in query_words:
            if term not in word_counts:
                continue
            tf = word_counts[term]
            df = self.doc_freqs.get(term, 0)
            idf = math.log((self.n_docs - df + 0.5) / (df + 0.5) + 1)
            numerator = tf * (self.k1 + 1)
            denominator = tf + self.k1 * (1 - self.b + self.b * doc_len / self.avg_dl)
            score += idf * numerator / denominator

        return score

    def search(self, query, top_k=10):
        scores = [(i, self.score(query, i)) for i in range(self.n_docs)]
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]
```

### Bước 2: Sự hợp nhất cấp bậc

```python
def reciprocal_rank_fusion(ranked_lists, k=60):
    scores = {}
    for ranked_list in ranked_lists:
        for rank, (doc_id, _) in enumerate(ranked_list):
            if doc_id not in scores:
                scores[doc_id] = 0.0
            scores[doc_id] += 1.0 / (k + rank + 1)
    fused = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return fused
```

### Bước 3: Đường ống tìm kiếm lai

```python
def hybrid_search(query, chunks, vector_embeddings, vocab, idf, bm25_index, top_k=5, fusion_k=60):
    query_emb = tfidf_embed(query, vocab, idf)
    vector_results = search(query_emb, vector_embeddings, top_k=top_k * 3)
    bm25_results = bm25_index.search(query, top_k=top_k * 3)
    fused = reciprocal_rank_fusion([vector_results, bm25_results], k=fusion_k)
    return fused[:top_k]
```

### Bước 4: Đặt lại đơn giản

Trong sản xuất, bạn sẽ sử dụng mô hình mã hóa chéo. Ở đây chúng tôi xây dựng một reanker mà đánh giá liên quan đến tài liệu truy vấn bằng cách sử dụng sự chồng chéo từ, tầm quan trọng của thuật ngữ và sự phù hợp cụm từ.

> Trong sản xuất bạn sẽ sử dụng mô hình biên tập giao thông. Ở đây chúng tôi xây dựng với từ chồng lên, sự quan trọng của từ và sự phù hợp của từ ngữ để đánh giá các truy vấn- tài liệu liên quan.

```python
def rerank(query, candidates, chunks):
    query_words = set(query.lower().split())
    stop_words = {"the", "a", "an", "is", "are", "was", "were", "what", "how",
                  "why", "when", "where", "do", "does", "for", "of", "in", "to",
                  "and", "or", "on", "at", "by", "it", "its", "this", "that",
                  "with", "from", "be", "has", "have", "had", "not", "but"}
    query_terms = query_words - stop_words

    scored = []
    for doc_id, initial_score in candidates:
        chunk = chunks[doc_id].lower()
        chunk_words = set(chunk.split())

        term_overlap = len(query_terms & chunk_words)

        query_bigrams = set()
        q_list = [w for w in query.lower().split() if w not in stop_words]
        for i in range(len(q_list) - 1):
            query_bigrams.add(q_list[i] + " " + q_list[i + 1])
        bigram_matches = sum(1 for bg in query_bigrams if bg in chunk)

        position_boost = 0
        for term in query_terms:
            pos = chunk.find(term)
            if pos != -1 and pos < len(chunk) // 3:
                position_boost += 0.5

        rerank_score = (
            term_overlap * 1.0
            + bigram_matches * 2.0
            + position_boost
            + initial_score * 5.0
        )
        scored.append((doc_id, rerank_score))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored
```

### Bước 5: HyDE (Hypothetical Document Embeddings)

```python
def hyde_generate_hypothesis(query):
    templates = {
        "what": "The answer to '{query}' is as follows: Based on our documentation, {topic} involves specific policies and procedures that define how the process works.",
        "how": "To address '{query}': The process involves several steps. First, you need to initiate the request. Then, the system processes it according to the defined rules.",
        "default": "Regarding '{query}': Our records indicate specific details and policies related to this topic that provide a comprehensive answer."
    }
    query_lower = query.lower()
    if query_lower.startswith("what"):
        template = templates["what"]
    elif query_lower.startswith("how"):
        template = templates["how"]
    else:
        template = templates["default"]

    topic_words = [w for w in query.lower().split()
                   if w not in {"what", "is", "the", "how", "do", "does", "a", "an",
                                "for", "of", "to", "in", "on", "at", "by", "and", "or"}]
    topic = " ".join(topic_words) if topic_words else "this topic"

    return template.format(query=query, topic=topic)


def hyde_search(query, chunks, vector_embeddings, vocab, idf, top_k=5):
    hypothesis = hyde_generate_hypothesis(query)
    hypothesis_emb = tfidf_embed(hypothesis, vocab, idf)
    results = search(hypothesis_emb, vector_embeddings, top_k)
    return results, hypothesis
```

### Bước 6: Biết cách làm cho con mẹ

```python
def create_parent_child_chunks(text, parent_size=200, child_size=50):
    words = text.split()
    parents = []
    children = []
    child_to_parent = {}

    parent_idx = 0
    start = 0
    while start < len(words):
        parent_end = min(start + parent_size, len(words))
        parent_text = " ".join(words[start:parent_end])
        parents.append(parent_text)

        child_start = start
        while child_start < parent_end:
            child_end = min(child_start + child_size, parent_end)
            child_text = " ".join(words[child_start:child_end])
            child_idx = len(children)
            children.append(child_text)
            child_to_parent[child_idx] = parent_idx
            child_start += child_size

        parent_idx += 1
        start += parent_size

    return parents, children, child_to_parent
```

### Bước 7: Đánh giá lòng trung thành

```python
def evaluate_faithfulness(answer, retrieved_chunks):
    answer_sentences = [s.strip() for s in answer.split(".") if len(s.strip()) > 10]
    if not answer_sentences:
        return 1.0, []

    grounded = 0
    ungrounded = []
    context = " ".join(retrieved_chunks).lower()

    for sentence in answer_sentences:
        words = set(sentence.lower().split())
        stop_words = {"the", "a", "an", "is", "are", "was", "were", "and", "or",
                      "to", "of", "in", "for", "on", "at", "by", "it", "this", "that"}
        content_words = words - stop_words
        if not content_words:
            grounded += 1
            continue

        matched = sum(1 for w in content_words if w in context)
        ratio = matched / len(content_words) if content_words else 0

        if ratio >= 0.5:
            grounded += 1
        else:
            ungrounded.append(sentence)

    score = grounded / len(answer_sentences) if answer_sentences else 1.0
    return score, ungrounded


def evaluate_retrieval_recall(queries_with_relevant, retrieval_fn, k=5):
    total_recall = 0.0
    results = []

    for query, relevant_indices in queries_with_relevant:
        retrieved = retrieval_fn(query, k)
        retrieved_indices = set(idx for idx, _ in retrieved)
        relevant_set = set(relevant_indices)
        hits = len(retrieved_indices & relevant_set)
        recall = hits / len(relevant_set) if relevant_set else 1.0
        total_recall += recall
        results.append({
            "query": query,
            "recall": recall,
            "hits": hits,
            "total_relevant": len(relevant_set)
        })

    avg_recall = total_recall / len(queries_with_relevant) if queries_with_relevant else 0
    return avg_recall, results
```

## Hãy sử dụng nó để thực hiện

Với một mã hóa chéo thực sự để xếp hạng lại:

> 用真实交叉编码器重排:

```python
from sentence_transformers import CrossEncoder

reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

def rerank_with_cross_encoder(query, candidates, chunks, top_k=5):
    pairs = [(query, chunks[doc_id]) for doc_id, _ in candidates]
    scores = reranker.predict(pairs)
    scored = list(zip([doc_id for doc_id, _ in candidates], scores))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:top_k]
```

Với người quản lý của Cohere:

> 用 Cohere 的托管重排器:

```python
import cohere

co = cohere.Client()

def rerank_with_cohere(query, candidates, chunks, top_k=5):
    docs = [chunks[doc_id] for doc_id, _ in candidates]
    response = co.rerank(
        model="rerank-english-v3.0",
        query=query,
        documents=docs,
        top_n=top_k
    )
    return [(candidates[r.index][0], r.relevance_score) for r in response.results]
```

Đối với HyDE với một LLM thực sự:

> 用真实LLM做 HyDE:

```python
import anthropic

client = anthropic.Anthropic()

def hyde_with_llm(query):
    response = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=256,
        messages=[{
            "role": "user",
            "content": f"Write a short paragraph that would be a good answer to this question. Do not say you don't know. Just write what the answer would look like.\n\nQuestion: {query}"
        }]
    )
    return response.content[0].text
```

Đối với việc tìm kiếm sản xuất lai với Weaviate:

> 用 Weaviate làm sản xuất hỗn hợp tìm kiếm:

```python
import weaviate

client = weaviate.connect_to_local()

collection = client.collections.get("Documents")
response = collection.query.hybrid(
    query="enterprise refund policy",
    alpha=0.5,
    limit=10
)
```

Các tham số alpha kiểm soát cân bằng: 0.0 = từ khóa thuần túy (BM25), 1.0 = vector thuần túy, 0.5 = trọng lượng bằng nhau.

> alpha 参数控制平衡:0.0=纯关键词(BM25),1.0=纯向量,0.5=等权重──大多数生产系统使用 alpha 在 0.3 到 0.7 之间──

## Chuyển nó đi.

Bài học này mang lại:
- `outputs/prompt-advanced-rag-debugger.md`-- một lời nhắc để chẩn đoán và khắc phục các vấn đề chất lượng RAG
  诊断和修复 RAG 质量问题提示
- `outputs/skill-advanced-rag.md`-- một kỹ năng để xây dựng RAG cấp sản xuất với tìm kiếm lai và xếp hạng lại
  Khả năng xây dựng RAG cấp sản xuất và xếp hạng hỗn hợp

## Tập luyện bài tập

1. So sánh BM25 vs tìm kiếm vector vs tìm kiếm lai trên các tài liệu mẫu. Đối với mỗi trong 5 truy vấn thử nghiệm, ghi lại cách tiếp cận nào trả lại phần liên quan nhất ở vị trí # 1. Tìm kiếm lai nên thắng ít nhất 3 trong số 5.
   Trong các tài liệu mẫu so sánh BM25 vs 向量搜索 vs 混合搜索.

2. Thực hiện một bộ lọc siêu dữ liệu. Thêm một trường "luật hạng" vào mỗi tài liệu (tự an ninh, hóa đơn, API, sản phẩm). Trước khi chạy tìm kiếm vector, lọc các đoạn chỉ vào danh mục liên quan. Kiểm tra bằng "Công mật mã nào được sử dụng?" và xác minh nó chỉ tìm kiếm các đoạn của danh mục bảo mật.
   实现元数据过器──给每个文档加"类"字段(security、billing、api、product)──运行向量搜索前,过块到相关类别──用"使用什么加密?"测试,验证它只搜索安全 类块──

3. Xây dựng một đường ống HyDE đầy đủ bằng cách sử dụng chức năng tạo đơn giản từ Bài học 06. So sánh chất lượng thu thập (tối ưu 3 hàng đầu) giữa tìm kiếm truy vấn trực tiếp và tìm kiếm HyDE trên tất cả 5 truy vấn thử nghiệm. HyDE nên cải thiện kết quả cho các truy vấn mơ hồ.
   Sử dụng bài học 06 của Simple Generating Function xây dựng toàn bộ HyDE 管线―― So sánh tìm kiếm trực tiếp tìm kiếm và HyDE  tìm kiếm trên 5 测试查询检查质量(top-3 相关性)。HyDE 应改进模糊查询的结果──

4. Thực hiện chiến lược chia nhỏ cha mẹ con trên các tài liệu mẫu. Sử dụng child_size=30 và parent_size=100. Tìm kiếm với các phần nhỏ của trẻ em nhưng trả lại các phần nhỏ của cha mẹ trong lời nhắc. So sánh các câu trả lời được tạo ra cho chia nhỏ tiêu chuẩn với chunk_size=50.
   Trong tài liệu mẫu thực hiện các tác phẩm chia sẻ chia sẻ.

5. Tạo một bộ dữ liệu đánh giá: 10 câu hỏi với các đoạn trả lời được biết đến. đo Recall@3, Recall@5, và Recall@10 chỉ cho (a) tìm kiếm vector, (b) chỉ cho BM25, (c) tìm kiếm lai, (d) tìm kiếm lai + xếp hạng lại.
   创建评估数据集:10 个带已知答案块问题──为 (a) 仅向量搜索、((b) 仅 BM25、((c) 混合搜索、((d) 混合 + 重排测量 Recall@3、Recall@5、Recall@10──绘制结果并识别重排在哪里帮助最大──

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|----------------------|---------|
| BM25 | "Keyword search" | A probabilistic ranking algorithm that scores documents by term frequency, inverse document frequency, and document length normalization | BM25：按词频、逆文档频率和文档长度归一化给文档评分的概率排序算法 |
| Hybrid search | "Best of both worlds" | Running semantic (vector) and keyword (BM25) search in parallel, then merging results with rank fusion | 混合搜索：并行运行语义（向量）和关键词（BM25）搜索，然后用排名融合合并结果 |
| Reciprocal Rank Fusion | "Merge ranked lists" | Combining multiple ranked lists by summing 1/(k + rank) for each document across all lists | 倒数排名融合：通过对每个文档在所有列表中求和 1/(k + rank) 合并多个排序列表 |
| Reranking | "Second pass scoring" | Using a more expensive cross-encoder model to re-score a candidate set from initial retrieval | 重排：用更昂贵的交叉编码器模型对初始检索的候选集重新评分 |
| Cross-encoder | "Joint query-document model" | A model that takes a query and document as a single input, producing a relevance score; more accurate than bi-encoders but too slow for full corpus search | 交叉编码器：将查询和文档作为单一输入的模型，输出相关性分数；比双编码器精确但太慢无法全语料搜索 |
| Bi-encoder | "Independent embedding model" | A model that embeds queries and documents independently; fast because embeddings are precomputed, but less accurate than cross-encoders | 双编码器：独立嵌入查询和文档的模型；快因为嵌入预计算，但比交叉编码器精度低 |
| HyDE | "Search with a fake answer" | Generate a hypothetical answer to the query, embed it, and search for real documents similar to it | HyDE：生成查询的假设答案，嵌入它，搜索相似真实文档 |
| Parent-child chunking | "Small search, big context" | Index small chunks for precise retrieval but return the larger parent chunk to provide sufficient context | 父子分块：索引小块精确检索但返回较大父块提供足够上下文 |
| Metadata filtering | "Narrow before searching" | Filtering documents by attributes (date, source, category) before running vector search to reduce the search space | 元数据过滤：运行向量搜索前按属性（日期、来源、类别）过滤文档以缩小搜索空间 |
| Faithfulness | "Did it stay grounded" | Whether the generated answer is supported by the retrieved documents, as opposed to hallucinated from the model's training data | 忠实度：生成的答案是否被检索文档支持，而非从模型训练数据幻觉 |

## Xem thêm 延伸阅读

- Robertson & Zaragoza, "The Probabilistic Relevance Framework: BM25 and Beyond" (2009) - tham chiếu cuối cùng cho BM25, giải thích các nền tảng xác suất đằng sau công thức
  Robertson & Zaragoza, "The Probabilistic Relevance Framework: BM25 and Beyond" (The Probabilityist Relevance Framework: BM25 and Beyond) (2009) BM25's authority reference, explain公式背后的概率基础
- Cormack et al., "Thiết hợp cấp độ tương ứng vượt trội hơn phương pháp học tập Condorcet và cấp độ cá nhân" (2009) - bài báo RRF ban đầu cho thấy nó đánh bại các phương pháp hợp nhất phức tạp hơn
  Cormack 等, "Reciprocal Rank Fusion..." (2009) RRF 原始论文,展示它击败更复杂的融合方法
- Gao et al., "Cũng xác nhận mật độ không chụp bằng không mà không có nhãn liên quan" (2022) - bài HyDE chứng minh rằng việc nhúng tài liệu giả thuyết cải thiện việc lấy lại mà không cần bất kỳ dữ liệu đào tạo nào
  Gao 等, "Cũng xác Zero Shot Cấp độ Khám Khám... "(2022)  HyDE 论文,展示假设文档嵌入无需训练数据即可改进检索
- Nogueira & Cho, "Passage Re-ranking with BERT" (2019) -- cho thấy việc xếp hạng lại qua mã hóa trên đỉnh BM25 cải thiện đáng kể chất lượng truy xuất
  Nogueira & Cho, "Passage Re-ranking with BERT" (Tạm dịch: "Đổi lại xếp hạng thông qua với BERT") (BH2019) 展示在 BM25 之上的交叉编码器重排显著改善检索质量
- [Khattab et al., "DSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelines" (2023)](https://arxiv.org/abs/2310.03714)-- xử lý việc xây dựng nhanh chóng và lựa chọn trọng lượng như một vấn đề tối ưu hóa trên đường ống thu hồi; đọc điều này cho " LLM chương trình" thay vì " LLM nhanh chóng".
  Khattab 等, "DSPy" (năm 2023) sẽ đưa ra các đề xuất về cấu trúc và quyền chọn xem như vấn đề tối ưu hóa trên đường kiểm tra; đọc nó để "định trình LLM" chứ không phải "định hướng LLM" (năm 2023)
- [Edge et al., "From Local to Global: A Graph RAG Approach to Query-Focused Summarization" (Microsoft Research 2024)](https://arxiv.org/abs/2404.16130)- Bức tranh GraphRAG: khai thác mối quan hệ thực thể + phát hiện cộng đồng Leiden cho tổng kết tập trung vào truy vấn; sự phân biệt về việc lấy lại toàn cầu và địa phương.
  Edge 等,"Từ địa phương đến toàn cầu: Một cách tiếp cận RAG đồ thị..."(Microsoft Research 2024)GraphRAG 论文:实体关系抽取 + Leiden 社区检测用于查询聚焦摘摘;全局 vs 局部检索的区别。
- [Asai et al., "Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection" (ICLR 2024)](https://arxiv.org/abs/2310.11511)-- tự đánh giá RAG với các token phản xạ; biên giới của các đại lý qua thu hồi tĩnh-đã tạo.
  Asai 等, "Self-RAG" ((ICLR 2024) 带反思代币的自评RAG;静态先检索后生成之外的智能体前沿──
- [LangChain Query Construction blog](https://blog.langchain.dev/query-construction/)-- cách dịch các truy vấn ngôn ngữ tự nhiên thành truy vấn cơ sở dữ liệu có cấu trúc (Text-to-SQL, Cypher) như một bước mua phục hồi.
  LangChain 查询构建博客如何将自然语言查询翻译为结构化数据库查询(Text-to-SQL、Cypher) như là bước dự đoán kiểm tra.
