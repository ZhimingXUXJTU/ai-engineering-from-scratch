# Chia sẻ bộ nhớ và hình mẫu bảng đen 黑板 模式 记忆共享

> Hai phương pháp tiếp cận tồn tại cùng nhau trong hệ thống đa tác nhân năm 2026:**message pool**(mọi người thấy tin nhắn của mọi người, như trong AutoGen GroupChat hoặc MetaGPT) và **blackboard with subscription**(các đại lý đăng ký các sự kiện liên quan, như trong MCP Context-Aware hoặc khung Matrix). Cả hai là phần trạng thái duy nhất của một hệ thống đa đại lý  nghĩa là cả hai đều là nơi các lỗi thú vị sống.**memory poisoning**Một đại lý ảo giác một "thực tế", các đại lý khác đối xử với nó như xác minh, và độ chính xác suy giảm dần theo cách khó khăn hơn nhiều để gỡ lỗi hơn một vụ tai nạn ngay lập tức. Bài học này xây dựng cả hai cấu trúc từ stdlib, tiêm một cuộc tấn công độc hại, và cho thấy ba giảm thiểu thực sự hoạt động trong sản xuất.

> **【中文解读】**Bài viết này giới thiệu về cơ chế phối hợp và cơ sở chia sẻ kiến thức trong hệ thống đa đại lý.

> **【拓展：shared memory blackboard→具体应用】**Mô hình chia sẻ ký ức/黑板模型是多 Agent 系统的经典协调机制所有 Agent 读写一个共享知识库――黑板模型起源于1980年代的听证会-II语音识别系统――现代实现包括 Redis 共享状态、向量数据库和MCP Resources――优势是简单,劣势是竞争条件(多 Agent 同时写入) ――


**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib, `threading`) | **语言:** Python (标准库, `threading`)
**Prerequisites:** Phase 16 · 04 (Primitive Model), Phase 16 · 09 (Parallel Swarm Networks) | **前置知识:** Phase 16 · 04 (原语模型), Phase 16 · 09 (并行群体网络)
**Time:** ~75 minutes | **时间:** ~75 分钟

>  **【前置】**学本节前请先掌握:Phase 16·04(原语) 、Phase 16·09(Swarm) 、并发编程(锁、竞态) ⋅共享记忆 = 多 Agent 协调的核心数据结构──
>  **【类比】**共享记忆两种模式 = "办公场景"──消息池(AutoGen GroupChat) = 开放办公区(大家都听);黑板+订阅(Context-Aware MCP) = 公告板(按订阅推送)──失败模式 = 记忆投毒(一个代理幻觉,其他代理 当真) 比崩更难调试──修复:版本号 + 来源标记 + 多源验证──

##                                                                                                                                                                                                                                                               

Các hệ thống đa đại lý cần một nơi để các đại lý chia sẻ dữ liệu. Một tùy chọn theo nghĩa đen là "làm tất cả mọi thứ trong tin nhắn" nhưng lại phát minh lại trạng thái chia sẻ với việc sao chép thêm. Một khác là "cứu mọi người một nhật ký toàn cầu" nhưng các nhật ký toàn cầu phát triển không giới hạn và độc hại dễ dàng. Một thứ ba là "được dự án một cái nhìn cho mỗi đại lý"

> Nhiều đại lý  hệ thống cần một địa điểm để để đại lý chia sẻ thực tế. Một tùy chọn chữ cái là "trả mọi thứ trong tin nhắn" nhưng đây giống như phát minh lại với bản sao cộng thêm chia sẻ trạng thái. Một khác là "đưa cho mỗi người một toàn局日志" nhưng toàn局日志 không giới hạn phát triển và dễ bị ô nhiễm.

Ba lựa chọn này theo dõi một sự thỏa hiệp cổ điển về hệ thống phân tán: rẻ nhưng yếu (thông điệp), đơn giản nhưng không có quy mô (bản sổ toàn cầu), có thể mở rộng nhưng cứng (bản chiếu cho mỗi đại lý).

> 三个选项追溯经典分布式系统权衡: rẻ nhưng yếu kém (nói) 消息 (nói) 简单 nhưng không thể mở rộng (nói) 整局日志 (nói) 可扩展但化 (nói) 每个代理投影 (nói) 没有选项占主导地位 (nói) 实系统混合:用于规划的小局池、用于工作机的投影视图──

Khi một trong những nhân viên ảo giác và viết ảo giác vào trạng thái chia sẻ, mỗi nhân viên tiếp theo đọc trạng thái đó chấp nhận ảo giác như là một sự thật. Đến khi con người nhận ra, chuỗi lý luận sâu năm bước và nguyên nhân gốc là thông điệp thứ ba từng được viết.

> Khi một trong số đó là một đại lý 幻觉并将幻觉写入共享状态, mỗi đọc của trạng thái này dưới游 Đại lý sẽ 幻觉 như thực tế chấp nhận. Khi con người nhận ra, chuỗi suy luận đã có năm bước sâu, và nguyên nhân cơ bản là 3条消息.

Một vụ tai nạn cho bạn một dấu vết đống. Món độc trí cho bạn một báo cáo chắc chắn sai lầm.

> 崩给你堆跟踪――内存污染给你自信错误报告―― thứ nhất là vài giây có thể kiểm tra; thứ hai có thể cần vài ngày để xác minh để quay lại với ảo tưởng ban đầu――

Đây là nhiễm độc trí nhớ. Đây là gia đình thất bại thứ hai được ghi nhận nhiều nhất trong phân loại MAST (Cemri et al., arXiv:2503.13657) và nó cấu trúc: bất kỳ thiết kế bộ nhớ chia sẻ nào mà không có nguồn gốc và một xác minh không thể viết sẽ hiển thị nó cuối cùng.

> Đây là sự ô nhiễm trong bộ nhớ. Nó là thứ hai trong các quy trình phân loại MAST trong các trường hợp thất bại trong gia đình (Cemri et al., arXiv:2503.13657), và cũng là cấu trúc: bất kỳ nguồn gốc nào không có nguồn gốc và không thể ghi lại được thiết kế chia sẻ bộ nhớ cuối cùng sẽ xuất hiện vấn đề này.

## Khái niệm cốt lõi

### Hai topology chính

**Full message pool.**Mỗi đại lý đọc mọi tin nhắn. AutoGen GroupChat và MetaGPT sử dụng điều này. đơn giản, minh bạch, kiểm tra, nhưng không mở rộng vượt quá ~ 10 đại lý bởi vì bối cảnh của mỗi đại lý chứa đầy công việc của các đại lý khác.

> **完整消息池。**Mỗi đại lý 读取每条消息──AutoGen GroupChat 和 MetaGPT sử dụng cách này── đơn giản, minh bạch, kiểm tra, nhưng không thể mở rộng đến khoảng 10 đại lý trên, vì mỗi đại lý trên dưới đây sẽ điền vào các công việc của các đại lý khác──

**Blackboard with subscription.**Các đại lý tuyên bố quan tâm đến các chủ đề; các tuyến đường phụ chỉ hướng các thông điệp liên quan. CA-MCP (arXiv:2601.11595) và khung phân cấp Matrix (arXiv:2511.21686) sử dụng điều này.

> **带订阅的黑板。**Các nhà đại lý tuyên bố về sự quan tâm của chủ đề; tầng dưới chỉ đường từ các thông tin liên quan. CA-MCP: arXiv: 2601.11595) và Matrix 去中心化框架: arXiv: 2511.21686) sử dụng phương pháp này.

### Khi mỗi người thắng

- **Full pool**chiến thắng khi các đại lý ít (< 10), đa dạng, và cuộc trò chuyện là ngắn hạn.
  Trung ngữ翻译:**完整池**Trong Đại lý 少(< 10) 、异构且对话短时时胜出;; Khi mọi người nhìn thấy mọi thứ, suy nghĩ ai nói gì là đơn giản:.
- **Blackboard**chiến thắng khi các đại lý là nhiều, đồng nhất trong vai trò nhưng rất nhiều trong trường hợp (swarms), và cuộc trò chuyện là dài hạn.
  Trung ngữ翻译:**黑板**Trong các trường hợp khác, người chơi có thể tham gia vào các cuộc chơi và chơi game.

Các hệ thống sản xuất thường trộn lẫn: một hồ bơi đầy đủ nhỏ ở phía trên (phần lập kế hoạch), bảng đen dưới (phần công nhân).

> Hệ thống sản xuất thường sử dụng hỗn hợp: trên một tầng nhỏ của một bể hoàn chỉnh (đơn vị quy hoạch), dưới đây là tầng đen (đơn vị máy).

Hệ thống nghiên cứu của Anthropic thực hiện điều này: một giám sát viên (một nhóm đầy đủ giữa một số đại lý chính) đại diện cho các đối tượng phụ (mỗi người có bối cảnh có phạm vi riêng, tách biệt với anh chị em).

> Sự kết hợp này được thực hiện bởi hệ thống nghiên cứu nhân văn: giám sát viên (supervisor) n toàn bộ nhóm các đại lý chủ đạo (supervisor) n ủy nhiệm cho các đại lý (commissioned to children) n mỗi đại lý có phạm vi riêng của mình (下文,与同级隔离) .

### Mùi độc trí nhớ, trong một kịch bản

Ba đại lý đang làm việc trong một nhiệm vụ nghiên cứu, đại lý A là đại lý tìm kiếm, đại lý B là tổng hợp, đại lý C là nhà phân tích.

> 三个代理 处理一个研究任务――Agent A là kiểm tra viên――Agent B là摘要器――Agent C là nhà phân tích viên――

1. A lấy một trang và viết một thông điệp cho trạng thái chia sẻ: "Study báo cáo cải thiện độ chính xác 42%".
   Trung ngữ翻译:A 获取一个页面并向共享状态写入消息:" Nghiên cứu báo cáo tỷ lệ xác thực tăng 42%".""
2. Trang được lấy lại nói "tăng 4,2%". Một ảo giác là một số thập phân.
   Trung ngữ翻译:获取的页面实际上说是"4.2% 提升──"A 幻觉一个小数点──"
3. B, đọc trạng thái chia sẻ, viết: "Tăng độ chính xác lớn 42% được báo cáo (nguồn: A). "
   Trung văn翻译:B 读取共享状态,写入:" báo cáo tăng 42% 准确率提升(来源:A) 』
4. C, đọc trạng thái chia sẻ, viết: "Cố gắng chấp nhận  42% nâng là biến đổi".
   Trung văn 读取共享状态,写入:" đề nghị chấp nhận 42% của nâng cao là thay đổi tình dục.
5. Báo cáo cuối cùng đề cập đến một con số 42% chưa từng tồn tại.
   Trung ngữ翻译:最终报告引用一个从未存在的 42% 数字──

Không có nhân viên nào bị hỏng, không có thử nghiệm nào thất bại, hệ thống "sự làm việc" ảo giác đã chuyển từ bối cảnh của một nhân viên sang tư duy của mỗi nhân viên qua trạng thái chia sẻ.

> Không có đại lý 崩── không có kiểm tra thất bại──系统"工作"了──幻觉通过共享状态从一个代理的上下文进入每个下游代理的推理──

Đây là lý do tại sao ngộ độc trí nhớ là lừa đảo: không có tai nạn, không có lỗi, không có cảnh báo. Hệ thống sản xuất một báo cáo sai trái. Cách duy nhất để phát hiện nó là lấy lại từng sự thật từ các nguồn chính  điều này đánh bại điểm của việc có các tác nhân.

> Đó là lý do tại sao nội dung bị ô nhiễm 阴险: không bị sụp đổ, không có lỗi, không có cảnh báo. Hệ thống tạo ra báo cáo tự tin sai lầm.

### Tại sao điều này là cấu trúc

Nếu không có trạng thái chia sẻ, ảo giác của nhân vật A vẫn ở trong bối cảnh của A. Các nhân vật dòng chảy xuống sẽ lấy lại hoặc dẫn lại và có thể bắt được lỗi. Với trạng thái chia sẻ ngây thơ, bối cảnh của A trở thành bối cảnh của mọi người, và ảo giác được rửa thành thực tế.

> 没有共享状态,Agent A's illusion stays in A's upper down文中──下游 Agent 会重新获取或重新推导并可能捕获错误── With a simple shared state,A's upper down文变成每个人的上下文,幻觉被洗白为事实──

Vấn đề không phải là quốc gia chia sẻ bản thân nó là quốc gia chia sẻ**without provenance and without an independent verifier**Ba biện pháp giảm thiểu giải quyết vấn đề này:

> 问题不是共享状态本身而是**没有来源追溯和没有独立验证器**Các biện pháp giảm thiểu giải quyết vấn đề này:

Mỗi chế độ giảm thiểu nhắm vào một chế độ thất bại khác nhau. Provenance cho phép bạn theo dõi lỗi trở lại. Versioning bảo vệ dấu vết kiểm toán.

> Mỗi loại biện pháp giảm thiểu đối với các mô hình thất bại khác nhau.

1. **Attribute provenance on every write.**Mỗi mục trong hồ sơ nhà nước được chia sẻ là ai đã viết nó, khi nào, dưới thời nào, và (nếu có) nguồn nào mà đại lý trích dẫn.
   Trung ngữ翻译:**每次写入时归属来源。**Mỗi bài viết trong trạng thái chia sẻ ghi lại những gì người viết 、何時、在什么提示下、以及( nếu có thể)
2. **Version writes; treat them as append-only.**Một sửa đổi là một mục mới thay thế cho mục cũ, không phải là một bản cập nhật tại chỗ.
   Trung ngữ翻译:**版本化写入；视为仅追加。**修正是一个取代旧条目的新条条,不是原地更新──审计跟踪被保留──
3. **Keep at least one agent that cannot write to shared state.**Một đại lý xác minh chỉ đọc lấy mẫu các mục nhập, lấy lại nguồn và đánh dấu sự không phù hợp. Bởi vì nó không thể viết cho hồ bơi, nó không thể bị nhiễm độc bởi hồ bơi.
   Trung ngữ翻译:**保留至少一个不能写入共享状态的 Agent。**Chỉ đọc chứng chỉ  Agent 采样条目、重新获取来源并标记不一致──因为 nó không thể được ghi vào bể, vì vậy không thể bị bể ô nhiễm──

### Tỷ lệ tiền lệ của bảng đen (Hayes-Roth, 1985)

Mô hình bảng đen này đã có trước các đại lý LLM bốn thập kỷ. Hayes-Roth (1985, "A Blackboard Architecture for Control") mô tả các nguồn kiến thức chuyên môn quan sát một bảng đen toàn cầu, đóng góp các giải pháp một phần và kích hoạt các nguồn khác. Bảng đen 2026 (CA-MCP, Matrix) là mô hình tương tự với các đại lý LLM như Nguồn tri thức và các điểm JSON như các giải pháp một phần. Văn học cũ đã ghi lại các giải pháp để viết tranh chấp, kiểm soát cơ hội, và sự nhất quán mà các hệ thống hiện đại tái phát hiện.

> 黑板模式比 LLM Agent早了四十年. Hayes-Roth (Hays-Roth, 1985, "A Blackboard Architecture for Control") mô tả việc quan sát toàn bộ Blackboard, đóng góp phần giải pháp và kích động các nguồn khác của kiến thức chuyên môn.

Bài học từ Hearsay-II (bảng ảnh nhận dạng giọng nói năm 1970): kiểm soát cơ hội  để bất kỳ nguồn kiến thức nào kích hoạt khi điều kiện kích hoạt của nó phù hợp  tạo ra giải quyết vấn đề nổi lên. Hệ thống đại lý hiện đại mà các biểu đồ lưu lượng công việc mã hóa mất điều này.

> Lời nghe-II(1970s年代语音识别黑板) bài học: cơ hội kiểm soát để bất kỳ nguồn kiến thức nào có nguồn gốc từ các điều kiện ứng dụng khi các điều kiện ứng dụng tạo ra vấn đề xuất hiện để giải quyết.

### Dự án so với toàn bộ hình ảnh

Một bảng đen tinh khiết cho mỗi thuê bao cùng một dự án (chương diện chủ đề).**per-agent projection**Các nhà giảm trạng thái của LangGraph là thực hiện 2026  chức năng giảm tính gấp trạng thái toàn cầu thành một mảnh cụ thể về vai trò.

> 纯黑板给每个订阅者相同的投影 (Tạm dịch: 纯黑板给每个订阅者相同的投影) 更多激进的设计是**每个 Agent 投影**Mỗi đại lý được định hình theo vai trò của mình. Các chức năng của LongGraph sẽ được lắp ráp thành các đoạn cụ thể của vai trò.

Dự án mỗi đại lý sẽ mở rộng hơn nhưng cần một kế hoạch.

> Mỗi đại lý  chiếu mở rộng hơn tốt hơn nhưng cần mô hình. Không mô hình, bạn xây dựng lại dự án tạm thời trong các lời khuyên của mỗi đại lý.

### Các mô hình văn bản

Nhiều đại lý viết cùng một lúc là một vấn đề đồng thời, không chỉ là một vấn đề LLM. Ba mô hình hoạt động:

> Nhiều đại lý cùng lúc viết là một vấn đề, không chỉ là vấn đề LLM ;;

- **Sequential writer (single producer).**Tất cả những gì viết đều được thông qua một đại lý điều phối mà sẽ làm cho nó trở nên liên tục.
  Trung ngữ翻译:**顺序写入者（单一生产者）。**Tất cả đều được viết bằng một đại lý phối hợp.
- **Optimistic concurrency with versioning.**Mỗi mục có một phiên bản; các nhà văn thất bại trong phiên bản không phù hợp và thử lại.
  Trung ngữ翻译:**带版本控制的乐观并发。**Mỗi bài viết có phiên bản; người viết trong phiên bản không phù hợp thất bại và thử lại.
- **Topic partitioning.**Các đại lý khác nhau sở hữu các chủ đề khác nhau, không có tranh chấp liên quan đến chủ đề, đòi hỏi phải thiết kế ranh giới phân vùng.
  Trung ngữ翻译:**主题分区。**Không có xung đột giữa các chủ đề.

Hầu hết các khung 2026 mặc định cho người viết theo trình tự bởi vì các cuộc gọi LLM là đủ chậm để tranh chấp hiếm và nút thắt không làm tổn thương.

> Phần lớn 2026 框架默认使用顺序写入者, vì LLM 调用足够慢, xung đột rất ít, không ảnh hưởng.

Khi bạn thực hiện tranh chấp (những nhóm nghiên cứu có hiệu suất cao, các đại lý nghiên cứu song song viết kết quả), phân vùng chủ đề thường là sự khắc phục rẻ nhất.

> Khi bạn thực sự gặp phải xung đột, các phân vùng chủ đề thường là sửa chữa rẻ nhất.

### Chứng minh không thể viết

Việc giảm tải chịu tải nhất là trình xác minh chỉ đọc.

> Các biện pháp giảm thiểu quan trọng nhất là chỉ đọc chứng chỉ.

- Người xác minh chia sẻ trạng thái với nhóm (đọc bảng đen hoặc hồ bơi).
  Trung ngữ翻译:验证者与团队共享状态 (tạm dịch: 验证者与团队共享状态)
- Verifier không có tay ghi để chia sẻ trạng thái  chỉ cho một kênh xác minh riêng biệt.
  Trung ngữ翻译:验证者没有对共享状态的写入句柄只有一个单独的验证通道──
- Người xác minh độc lập lấy nguồn được trích dẫn trong văn bản.
  Trung ngữ翻译:验证者独立获取写入中引用的来源──标记不一致──
- Các kết quả của người xác minh được chuyển đến một người hoặc một đại lý quyết định riêng biệt, không bao giờ được đưa trở lại hồ bơi.
  Trung ngữ: Người chứng minh chính mình xuất phát từ con người hoặc một đại lý quyết định độc lập, luôn không quay lại trong hồ.

Nếu không có sự tách biệt này, các sản phẩm của người xác minh sẽ trở thành các mục nhập mới trong hồ bơi, có nghĩa là một hồ bơi độc hại đã làm độc người xác minh, làm độc các xác minh của nó.

> Không có sự phân tách này, xuất khẩu của người kiểm chứng trở thành mục mới trong hồ, điều này có nghĩa là hồ bị ô nhiễm đã ô nhiễm người kiểm chứng, và trong đó làm ô nhiễm chứng minh của nó.

Đây là nguyên tắc không thể viết được kiểm tra viên: kiểm toán viên phải được đọc chỉ đối với hệ thống được kiểm tra. Thỏa hiệp với kiểm toán viên và bạn thỏa hiệp kiểm toán.

> Đây là nguyên tắc không thể viết được của kiểm toán viên: kiểm toán viên phải chỉ đọc về hệ thống được kiểm toán.

## Hãy xây dựng nó.
```figure
swarm-blackboard
```

## Hãy xây dựng nó

`code/main.py`thực hiện cả hai topology trong stdlib Python cộng với một cuộc tấn công độc đồ chơi và ba giảm thiểu.

> `code/main.py`Sử dụng Python đã thực hiện hai loại phát triển và một cuộc tấn công ô nhiễm đồ chơi và ba loại biện pháp giảm bớt.

- `MessagePool` Nhập nhật ký chỉ có thêm dây an toàn với đọc đầy đủ.
  Trung ngữ翻译:`MessagePool` 线程安全的仅添日志,支持完整读取──
- `Blackboard` Pub/sub có chủ đề khóa với thuê bao mỗi đại lý.
  Trung ngữ翻译:`Blackboard`  基于主题发布/订阅, hỗ trợ mỗi Agent's订阅──
- `ProvenanceEntry` tất cả các ghi chép (tác giả, dấu thời gian, prompt_hash, source_uri).
  Trung ngữ翻译:`ProvenanceEntry` Mỗi lần viết vào ghi chép (写入记录)
- `PoisoningScenario` thực hiện một nhiệm vụ nghiên cứu ba đại lý trong đó đại lý A ảo giác một số thập phân.
  Trung ngữ翻译:`PoisoningScenario` 运行三 Agent 研究任务, trong đó Agent A 幻觉一个小数点――印最终报告――
- `Verifier` một đại lý chỉ đọc mà lấy lại các nguồn và đánh dấu sự không nhất quán.
  Trung ngữ翻译:`Verifier` Một nguồn thu hồi lại và chỉ được đánh dấu là đại lý không phù hợp.

Tạo sản lượng dự kiến:
- Tiếp tục 1 (không xác minh): 42% ảo giác được truyền lên báo cáo cuối cùng.
  Trung ngữ翻译:运行 1(无验证者):幻觉的 42% 传播到最终报告──
- Run 2 (với xác minh): người xác minh đánh dấu sự không phù hợp, hồ bơi được dán nhãn "được đánh dấu", báo cáo cuối cùng bao gồm một sự rút lại.
  Trung ngữ翻译:运行 2(有验证者):验证者标记不一致,池被标记为"已标记",最终报告包含撤回。

## Hãy sử dụng nó để thực hiện

`outputs/skill-memory-auditor.md`là một kỹ năng kiểm tra thiết kế bộ nhớ chia sẻ của bất kỳ hệ thống đa đại lý nào cho nguồn gốc, phiên bản và phân tách xác minh.

> `outputs/skill-memory-auditor.md`là một kỹ năng, kiểm toán bất kỳ nhiều đại lý  hệ thống  chia sẻ trong bộ nhớ trong thiết kế nguồn gốc 追溯、版本控制和验证者分离──

## Chuyển nó đi.

Đối với bất kỳ thiết kế bộ nhớ chung nào:

>  Đối với bất kỳ shared内存 thiết kế:

- ghi lại nguồn gốc trên mỗi bài viết: `(writer, timestamp, prompt_hash, tool_calls_cited, source_uri)`- Tôi không biết.
  Trung ngữ翻译:每次写入时记录来源:`(写入者, 时间戳, prompt_hash, 引用的工具调用, source_uri)`
- Làm cho nhật ký chỉ thêm vào. Cửa chữa là các mục mới tham khảo thứ thay thế.
  Trung文翻译:使日志仅追加──修正项是引用被取代项的新条目──
- Việc triển khai ít nhất một đại lý xác minh chỉ đọc với quyền truy cập nguồn độc lập.
  Trung ngữ翻译:部署 ít nhất một người có nguồn độc lập truy cập chỉ người đọc chứng minh đại lý.
- Khả năng xác minh đường đến một kênh riêng biệt, không trở lại hồ bơi chung.
  Trung ngữ翻译:将验证者输出路由到单独通道, chứ không phải quay lại đến池共享.
- Lập tỷ lệ của những bài viết là sự thay thế  một tỷ lệ tăng là bằng chứng sớm về các mô hình ảo giác.
  Trung ngữ翻译: tỷ lệ ghi chép bao gồm văn bản tỷ lệ tăng là bằng chứng sớm về mô hình ảo giác

## Tập luyện bài tập

1. Đi chạy`code/main.py`- Đảm bảo chạy 1 truyền tải ảo giác và chạy 2 bắt được nó.
   Trung ngữ翻译:运行 `code/main.py`❖ xác nhận hành động 1 传播幻觉且运行 2 捕获它──
2. Thêm một ảo giác thứ hai: đại lý B phát minh ra một bộ dữ liệu kích thước.
   Trung ngữ翻译:添加第二幻觉:Agent B 虚构一个数据集大小──验证者应该捕获两者而无需针对任何一个手动调优──
3. Chuyển toàn bộ hồ bơi vào bảng màu với các phân vùng chủ đề (`prices`- `summaries`- `analyses`(văn số 1): Các tình huống nhiễm độc nào mà việc phân chia chủ đề làm khó khăn hơn để thực hiện, và điều gì không giúp ích?
   Trung文翻译:将完整池切换为带主题分区的黑板`prices``summaries``analyses`(■) Các vấn đề phân chia làm cho những tình huống gây nghiện khó khăn hơn để thực hiện, những gì không giúp?
4. Đọc Hayes-Roth (1985, "A Blackboard Architecture for Control"). Định danh hai mô hình điều khiển từ bài báo không được thảo luận trong bài học này mà hệ thống 2026 sẽ được hưởng lợi.
   Trung文翻译:阅读 Hayes-Roth(1985,"A Blackboard Architecture for Control")。识别论文中两个本课未讨论的2026年系统会受益的控制模式──
5. Đọc CA-MCP (arXiv:2601.11595). Khóa kho lưu trữ ngữ cảnh chia sẻ của nó vào lớp MessagePool hoặc Blackboard trong `code/main.py`CA-MCP thêm vào những thứ nguyên thủy nào?
   Trung văn翻译:阅读 CA-MCP(arXiv:2601.11595)`code/main.py`Trung ương MessagePool hoặc bảng đen 类──CA-MCP đã thêm vào nó những ngôn ngữ gốc nào?

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Message pool / 消息池 | "Shared chat history" / "共享聊天历史" | Append-only log that every agent reads. Full transparency, poor scaling. / 每个 Agent 读取的仅追加日志。完全透明，扩展性差。 |
| Blackboard / 黑板 | "Shared workspace" / "共享工作区" | Topic-keyed pub/sub. Agents subscribe to relevant topics. Scales farther. / 基于主题的发布/订阅。Agent 订阅相关主题。扩展性更好。 |
| Provenance / 来源追溯 | "Who wrote what" / "谁写了什么" | Metadata on each write: writer, timestamp, prompt, sources. / 每次写入的元数据：写入者、时间戳、提示、来源。 |
| Memory poisoning / 内存污染 | "Hallucinations spreading" / "幻觉传播" | One agent's error enters shared state, downstream agents adopt it as fact. / 一个 Agent 的错误进入共享状态，下游 Agent 将其作为事实采纳。 |
| Append-only / 仅追加 | "No in-place updates" / "无原地更新" | Corrections are new entries that supersede. Preserves audit trail. / 修正项是取代旧条目的新条目。保留审计跟踪。 |
| Unwritable verifier / 不可写验证者 | "Independent auditor" / "独立审计者" | Read-only agent that re-fetches sources and flags inconsistencies. / 重新获取来源并标记不一致的只读 Agent。 |
| Projection / 投影 | "Scoped view" / "范围视图" | Per-agent view computed from global state. LangGraph reducers are the canonical case. / 从全局状态计算的每个 Agent 视图。LangGraph 归约器是典型实现。 |
| Knowledge Source / 知识源 | "Specialist agent" / "专家 Agent" | Hayes-Roth's 1985 term for a blackboard participant. / Hayes-Roth 1985 年对黑板参与者的称呼。 |

## Xem thêm 延伸阅读

- [Cemri et al. — Why Do Multi-Agent LLM Systems Fail?](https://arxiv.org/abs/2503.13657) Định dạng phân loại MAST; ngộ độc trí nhớ là một phụ gia đình thất bại phối hợp
  Trung文翻译:Cemri 等人  为什么多 Agent LLM 系统会失败? MAST 分类法;内存污染是协调失败子家族
- [CA-MCP — Context-Aware Multi-Server MCP](https://arxiv.org/abs/2601.11595) Kho lưu trữ ngữ cảnh chung cho các máy chủ MCP phối hợp
  Trung ngữ翻译:CA-MCP  上下文感知多服务器 MCP  协调 MCP 服务器的共享上下文存储
- [Matrix — decentralized multi-agent framework](https://arxiv.org/abs/2511.21686) bảng màu dựa trên dòng tin nhắn mà không có nhạc cụ trung tâm
  Trung ngữ翻译:Matrix  去中心化多 Agent 框架  基于消息队列的黑板,无中央编排器
- [LangGraph state and reducers](https://docs.langchain.com/oss/python/langgraph/workflows-agents) mô hình chiếu mỗi đại lý trong sản xuất
  Trung文翻译:LangGraph  trạng thái và归约器  生产中的每个代理 投影模式
- [Anthropic — How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) Các ghi chép về nguồn gốc và xác minh từ một hoạt động sản xuất
  Trung ngữ翻译:Anthropic  我们如何构建多代理研究系统  来自生产部署的来源追溯和验证笔记
