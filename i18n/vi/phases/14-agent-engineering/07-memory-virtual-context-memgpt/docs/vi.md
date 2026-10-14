# Memory: Virtual Context và MemGPT  nhớ:虚拟上下文与 MemGPT
# Bộ nhớ đại lý  Khung ngữ ảo và trang bộ nhớ

> Các cửa sổ ngữ cảnh là hữu hạn. Các cuộc trò chuyện, tài liệu và dấu vết công cụ không có. Giải pháp là bộ nhớ ảo của hệ điều hành được tái lập.

> **【中文解读】**Các cửa sổ trên là giới hạn, nhưng giao tiếp, tài liệu và các quỹ đạo của công cụ không phải. MemGPT sẽ phân loại các loại này cho hệ điều hành ảo trong bộ nhớ.

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 01 (Agent Loop), Phase 14 · 06 (Tool Use) | **前置知识:** Phase 14 · 01 (Agent 循环), Phase 14 · 06 (工具使用)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Mục tiêu học tập

- Giải thích sự tương tự của hệ điều hành MemGPT dựa trên: ngữ cảnh chính = RAM, ngữ cảnh bên ngoài = đĩa, công cụ bộ nhớ = trang vào/ ra.
  Trung ngữ翻译:解释 MemGPT 所基于的操作系统类比:主上下文 = RAM,外部上下文 = 磁盘,记忆工具 = 页面换进/换出――
- Thực hiện mô hình MemGPT hai cấp trong stdlib với bộ đệm ngữ cảnh chính, một cửa hàng tìm kiếm bên ngoài và công cụ vào / ra trang.
  Trung ngữ翻译:用标准库实现两层 MemGPT 模式,包含主上下文缓冲区、外部可搜索存储和页面换进/换出工具──
- Mô tả cách mà đại lý phát hành "phát" để truy vấn hoặc sửa đổi bộ nhớ bên ngoài và cách kết quả được nối lại vào lời nhắc tiếp theo.
  Trung ngữ翻译:描述 Agent 如何发发发"中断"来查询或修改外部记忆,以及结果如何被拼接回下一个提示──
- Xác định các lựa chọn thiết kế MemGPT mang đến Letta (Dạy 08) và Mem0 (Dạy 09).
  Trung文翻译:识别 MemGPT 中延续到 Letta(第8 课) 和 Mem0(第9 课) 的设计选择──

## Vấn đề  vấn đề giới thiệu

Các cửa sổ ngữ cảnh có vẻ như chúng nên giải quyết bộ nhớ. Chúng không. Ba chế độ thất bại lặp lại trong sản xuất:

> Có vẻ như có thể giải quyết vấn đề trí nhớ, nhưng thực tế không thể.

1. **Overflow.**Những cuộc trò chuyện nhiều vòng, các tài liệu dài, hoặc các quỹ đạo nặng nề về các công cụ vượt qua cửa sổ.
   Trung ngữ翻译:**溢出。**Nhiều vòng cuộc hội thoại, dài tài liệu hoặc công cụ sử dụng mật thiết các đường cong vượt qua cửa sổ hạn chế.
2. **Dilution.**Ngay cả trong cửa sổ, việc lấp đầy bối cảnh không liên quan làm giảm sự chú ý đến những gì quan trọng.
   Trung ngữ翻译:**稀释。**Ngay cả trong cửa sổ, các filling không liên quan trên cũng làm giảm sự chú ý đến nội dung quan trọng.
3. **Persistence.**Một phiên mới bắt đầu với một cửa sổ trống, các đại lý không có trí nhớ bên ngoài không thể nói "Hãy nhớ khi bạn yêu cầu tôi... " trong các phiên.
   Trung ngữ翻译:**持久化。**Một cuộc họp mới bắt đầu từ cửa sổ trống không. Không có ký ức bên ngoài.

> **【中文解读】**Trên màn hình dưới đây có vẻ có thể giải quyết vấn đề ký ức, nhưng thực tế không thể. Trong môi trường sản xuất có ba mô hình thất bại: 1) tràn ra nhiều cuộc hội thoại hoặc dài văn kiện vượt qua màn hình giới hạn, tất cả mọi thứ bên ngoài cắt đứt đã bị mất.

Các cửa sổ lớn hơn giúp nhưng không sửa chữa điều này. Báo cáo Mem0 2025 đo lường rằng các đường cơ sở cửa sổ 128k vẫn thiếu các thực tế về đường chân trời dài mà một đại lý cửa sổ 4k với bộ nhớ bên ngoài nắm bắt.

> Các cửa sổ lớn hơn có thể giúp nhưng không giải quyết được vấn đề này. MEM0 của 2025 bài báo đo lường phát hiện ra, 128k cửa sổ của các đường cốt lõi vẫn sẽ bị bỏ qua 4k cửa sổ + bộ nhớ bên ngoài.

> **【拓展：MemGPT → 现代 Agent 记忆系统】**MemGPT (Packer et al., 2023) sẽ phân tích các bài viết dưới đây để phân tích hệ điều hành ảo内存: 主上下文=RAM,外部存储=磁盘,记忆工具=页面换换换出―― đây là mô hình cơ bản của tất cả hệ thống nhớ năm 2026―Mem0 của bài báo 2025 đo lường phát hiện,128k cửa sổ của các tuyến đường vẫn sẽ bị bỏ qua 4k cửa sổ + Ngoại bộ nhớ Trưởng lý có thể nắm bắt các thực tế dài hạn.

>  **【前置】**必须先掌握:Phase 14·01(Agent Loop) MemGPT的记忆工具是普通工具调用扩展;Phase 14·06(Tool Use) 记忆操作通过工具实现──还需要操作系统基础知识 Nếu bạn không biết"虚拟内存""页面错误"是什么,先去补操作系统课,否则类比看不懂──

## Khái niệm cốt lõi

### Phân tích OS

MemGPT (Packer et al., arXiv:2310.08560, v2 Feb 2024) bản đồ quản lý bối cảnh đến bộ nhớ ảo của hệ điều hành:

> Packer 等人(arXiv:2310.08560, v2 2024 年 2 月) sẽ trên 下文管理映射到操作系统虚拟内存:

| OS concept | MemGPT concept | 2026 production analog |
|------------|---------------|------------------------|
| OS 概念 | MemGPT 概念 | 2026 生产环境类比 |
| RAM | main context (prompt) | Anthropic/OpenAI context window / 主上下文（提示） |
| Disk | external context | vector DB, KV, graph store / 外部上下文（向量数据库、KV、图存储） |
| Page fault | memory tool call | `memory.search`, `memory.read`, `memory.write` / 记忆工具调用 |
| OS kernel | agent control loop | ReAct loop with memory tools / 带记忆工具的 ReAct 循环 |

Các đại lý chạy một vòng lặp ReAct bình thường. Một lớp công cụ thêm cho phép nó trang dữ liệu vào và ra khỏi ngữ cảnh chính.

>  **【类比】**MemGPT 像你的电脑内存管理:RAM(主上下文) chỉ có 8GB nhưng phải chạy Photoshop + 浏览器 + IDE; hệ điều hành thông qua trang đổi vào thay ra khỏi(page in/out) để bạn " cảm giác " có không có hạn trong内存。MemGPT 让 Agent cũng làm như vậy主上下文塞不下时,Agent自我调用 `archival_memory_search`Để liên quan nội dung "Chổi vào",调用 `core_memory_replace`Để không liên quan nội dung "hổi ra"──Agent 像操作系统内核, bộ nhớ công cụ像系统调用──

> Trình độ ReAct của Agent 运行普通的 ReAct 循环―― một loại công cụ bổ sung để nó có thể được trao đổi giữa dữ liệu trên nội dung chính và lưu trữ bên ngoài――

> **【中文解读】**MemGPT sẽ lên dưới đây quản lý được hiển thị vào hệ điều hành ảo内存:RAM=主上下文(当前提示),磁盘=外部上下文(向量数据库/KV/图存储),页面错误=记忆工具调用(`memory.search`- Không.`memory.read`- Không.`memory.write`),OS 内核=Agent 控制循环──Agent 运行普通的 ReAct 循环,额外增加一类工具用于在主下文和外部存储之间交换进出数据──

### Hai tầng

- **Main context.**Dữ kích thước cố định giữ nhiệm vụ hiện tại.
  Trung ngữ翻译:**主上下文。**固定大小的提示,承载当前任务──模型始终可见──
- **External context.**Không giới hạn, có thể tìm kiếm qua các công cụ.
  Trung ngữ翻译:**外部上下文。**无界的,通过工具可搜索──相关时读取,出现事实时写入──

Bài báo ban đầu đánh giá thiết kế trên hai nhiệm vụ bên ngoài cửa sổ cơ sở: phân tích tài liệu dài hơn 100k token và trò chuyện nhiều phiên với bộ nhớ bền vững trong nhiều ngày.

> Bài viết gốc được đánh giá trên hai nhiệm vụ vượt ra ngoài cửa sổ cơ bản: phân tích tài liệu của hơn 100k token và nhiều cuộc trò chuyện chia sẻ về ký ức lâu dài xuyên suốt.

### Mô hình gián đoạn

MemGPT giới thiệu bộ nhớ như gián đoạn: giữa cuộc trò chuyện, đại lý có thể gọi một công cụ bộ nhớ, thời gian chạy thực hiện nó, và kết quả được chia vào lượt trợ lý tiếp theo như một quan sát mới.`read()`syscall chặn quá trình, trả lại byte, và quá trình tiếp tục.

> MemGPT giới thiệu bộ nhớ là gián đoạn: trong cuộc trò chuyện, người đại lý có thể điều khiển các công cụ bộ nhớ, vận hành khi thực hiện nó, kết quả là một sự chú ý mới kết nối đến một trợ lý tiếp theo.`read()`系统调用阻塞进程、返回字节、进程继续──

bề mặt công cụ bộ nhớ Canonical:

> 标准记忆工具接口:

- `core_memory_append(section, text)` viết cho một phần liên tục của lời nhắc.
  Trung ngữ翻译:`core_memory_append(section, text)`写入提示的持久化分区──
- `core_memory_replace(section, old, new)` chỉnh sửa một phần liên tục.
  Trung ngữ翻译:`core_memory_replace(section, old, new)` 编辑持久化分区──
- `archival_memory_insert(text)` viết cho cửa hàng bên ngoài tìm kiếm.
  Trung ngữ翻译:`archival_memory_insert(text)`写入可搜索的外部存储──
- `archival_memory_search(query, top_k)` lấy lại từ cửa hàng bên ngoài.
  Trung ngữ翻译:`archival_memory_search(query, top_k)` Từ kho lưu trữ bên ngoài
- `conversation_search(query)` quét qua các vòng quay.
  Trung ngữ翻译:`conversation_search(query)`扫描 quá khứ

### Khi giấy kết thúc và sản xuất bắt đầu

Vào tháng 9 năm 2024, MemGPT trở thành Letta.`cpacker/MemGPT`) còn lại; Letta mở rộng thiết kế:

> 2024 年 9 月 MemGPT 成为 Letta──研究仓库(`cpacker/MemGPT`) vẫn còn tồn tại;Letta 扩展了设计:

- Ba tầng thay vì hai (tầm, nhớ lại, lưu trữ  Bài học 08).
  Trung文翻译:三层而非两层(core、recall、archival第8 课) ⋅
- Lý luận bản địa thay thế `send_message`/mô hình nhịp tim (Dạy 08).
  Trung文翻译:原生推理替代 `send_message`/心跳模式 ((第 8 课) 』
- Các tác nhân thời gian ngủ chạy bộ nhớ không đồng bộ (Dạy 08).
  Trung文翻译:运行异步记忆工作的睡眠时间代理 (第 8 课)

Bảng giấy MemGPT là nền tảng cho năm 2026 ngay cả khi hệ thống sản xuất chạy Letta, Mem0 hoặc một cửa hàng hai tầng tùy chỉnh.

> MemGPT 论文 là nền tảng của năm 2026, ngay cả khi hệ thống sản xuất hoạt động Letta、Mem0 hoặc tự xác định hai tầng lưu trữ。

### Khi mô hình này đi sai

> ️ **【易错点】**MemGPT 新手最容易忽略"记忆投毒":把外部网页、用户消息直接 `archival_memory_insert`进外部存储――**后果**: kẻ tấn công trong trang web trong藏快注注如"忽略之前所有命令"), 下次 Agent检索到此条记忆时,命令被执行──**一行修复**: tất cả nội dung bên ngoài của các tệp vào phải làm trước tiên an toàn (xem Bước 14·27 tiêm nhanh 防护),并存储 nguồn 字段用于追溯。

- **Memory rot.**Các văn bản tích lũy nhanh hơn so với đọc; tìm kiếm bị ngập trong các sự kiện lỗi thời.
  Trung ngữ翻译:**记忆腐化。**写入积累速度快于读取;检索被过时事实淹没──修复:定期合并(Letta sleep-time)、显式失效(Mem0 冲突检测器)──
- **Memory poisoning.**Tưởng thức bên ngoài là lấy lại văn bản. Nếu nội dung bị kẻ tấn công kiểm soát rơi vào một ghi chú bộ nhớ, đại lý lại ăn nó vào phiên tiếp theo. Đây là cuộc tấn công Greshake et al. (Dạy 27) được tái tạo theo thời gian.
  Trung ngữ翻译:**记忆投毒。**Bộ nhớ bên ngoài là văn bản được kiểm tra. Nếu nội dung của kẻ tấn công kiểm soát vào ghi chép ký ức, Trưởng trong cuộc họp sau sẽ tái thu thập nó.
- **Citation loss.**Trưởng thức tài liệu (session ID, turn ID) với mỗi ghi chép lưu trữ.
  Trung ngữ翻译:**引用丢失。**Agent Remember" user made me publish X"but cannot cite which one. ⋅ Mỗi lần đăng ký trong hồ sơ

> 🤔 **【困惑】**Q: 既然 2026 年模型上下文窗口已经有1M token了? Gemini 1.5 Pro), còn cần MemGPT kiểu này? A: 需要. 窗口大不代表用对硬塞 1M token 会触发"中段遗忘" (lạc trong giữa 现象) và chú ý稀释, mô hình chú ý đến nội dung trung gian đáng kể thấp hơn so với đầu cuối.

## Hãy xây dựng nó.
```figure
context-budget
```

## Hãy xây dựng nó

`code/main.py`thực hiện mô hình hai cấp của MemGPT trong stdlib:

> `code/main.py`Sử dụng tiêu chuẩn đã thực hiện hai mô hình của MemGPT:

- `MainContext` bộ đệm nhanh kích thước cố định với một `core`dict và a `messages`danh sách; tự động thu nhỏ các tin nhắn cũ nhất khi quá mức.
  Trung ngữ翻译:`MainContext` cố định                                                                                                                                                                                                                                                             `core`字典和 `messages`列表;超出上限时自动压缩最老的消息──
- `ArchivalStore` lưu trữ trong bộ nhớ BM25-esque (tỷ lục token-overlap) của (id, văn bản, thẻ, phiên, lượt) các hồ sơ.
  Trung ngữ翻译:`ArchivalStore`内存中的类 BM25 存储(token 重叠评分),存储 (id, văn bản, thẻ, phiên, lượt) 记录。
- Năm công cụ bộ nhớ lập bản đồ cho bề mặt MemGPT.
  Trung文翻译:映射到 MemGPT 接口的五个记忆工具──
- Một nhân viên kịch bản điền hồ sơ với các sự kiện, sau đó trả lời một câu hỏi bằng cách gọi `archival_memory_search`- Tôi không biết.
  Trung文翻译: Một văn phòng, sử dụng thực tế để lấp đầy lưu trữ, sau đó thông qua调用 `archival_memory_search` trả lời câu hỏi:

Đi đi.

> 运行:

```
python3 code/main.py
```

Hướng dẫn cho thấy đại lý viết ba sự kiện, điền vào ngữ cảnh chính để nạp (phục xuất việc trục xuất), sau đó trả lời một câu hỏi tiếp theo bằng cách lấy từ hồ sơ  tái tạo dòng làm việc MemGPT mà không có LLM thực sự.

> 轨迹显示 Agent 写入三个事实、将主上下文填满到上限(强制驱逐) 、然后通过归档存储检查来回答后续问题在没有任何真实LLM的情况下重现 MemGPT 工作流──

## Hãy sử dụng nó để thực hiện

Mỗi hệ thống bộ nhớ sản xuất ngày nay là một biến thể MemGPT:

> Ngày nay, mỗi hệ thống sản xuất ký ức đều là một biến thể của MemGPT:

- **Letta**(Dân học 08)  ba cấp, lý luận bản địa, tính toán thời gian ngủ.
  Trung ngữ翻译:**Letta**(第8 课) 三层、原生推理、睡眠时间计算──
- **Mem0**(Dân học 09)  vector + KV + đồ thị hợp nhất với một lớp ghi điểm.
  Trung ngữ翻译:**Mem0**(第 9 课) 向量 + KV + 图与评分层融合──
- **OpenAI Assistants / Responses** quản lý bộ nhớ thông qua các chuỗi và tập tin.
  Trung ngữ翻译:**OpenAI Assistants / Responses** Thông qua các ví dụ và quản lý tài liệu nhớ.
- **Claude Agent SDK** trí nhớ lâu dài thông qua kỹ năng và cửa hàng phiên.
  Trung ngữ翻译:**Claude Agent SDK** Thông qua kỹ năng và hội thoại lưu trữ thực hiện ký ức dài hạn.

Chọn một theo hình thức hoạt động (được tự lưu trữ, quản lý, tích hợp khung), chứ không phải theo mô hình cốt lõi  mô hình cốt lõi là MemGPT.

> 根据运营形态 (自托管,托管,框架集成) lựa chọn,而非核心模式核心模式就是MemGPT──

## Chuyển nó đi.
### Hình dạng của trí nhớ đại lý

Paging giải quyết dung lượng. Nó không quyết định phải lưu trữ gì. Bốn loại bộ nhớ lặp lại trên các hệ thống sản xuất, mỗi trả lời một câu hỏi khác nhau:

- **Working memory** điều gì quan trọng ngay bây giờ? cấp độ trong bối cảnh: nhiệm vụ hiện tại, lượt gần đây, các phần cốt lõi được gắn.
- **Episodic memory** đã xảy ra gì? vòng và quỹ đạo trước, được lưu trữ với phiên và vòng tham chiếu, có thể chơi lại theo yêu cầu.
- **Semantic memory** điều gì là thật? Những sự thật về người dùng, miền, thế giới, cập nhật và sao chép theo cách thay đổi.
- **Procedural memory**Tôi đã học được những thói quen, sở thích và quy tắc hướng dẫn hành vi trong tương lai thay vì nhớ lại.

Các ứng dụng mã nguồn mở chọn các điểm tấn công khác nhau:

| Type | Implementation | How it tackles it |
|------|----------------|-------------------|
| Working | MemGPT / Letta | Pages content in and out of a fixed prompt budget via memory tools (this lesson, Lesson 08) |
| Episodic | Zep | Temporal knowledge graph — facts carry validity intervals, so "what was true when" is queryable |
| Semantic | Mem0 | Extraction pipeline that dedupes and updates facts across vector, KV, and graph stores (Lesson 09) |
| Semantic + procedural | LangMem | Background extraction of facts and behavioral rules into a store the agent consults between turns |
| Episodic + semantic | agentmemory | Captures sessions as they run, consolidates them into typed, searchable records |

## Chuyển nó

`outputs/skill-virtual-memory.md`là một kỹ năng có thể sử dụng lại tạo ra một nền tảng bộ nhớ hai cấp (lầu chính + lưu trữ + bề mặt công cụ) cho bất kỳ thời gian chạy mục tiêu nào, với chính sách sơ tán và các trường trích dẫn được cáp vào.

> `outputs/skill-virtual-memory.md`là một kỹ năng có thể sử dụng được, tạo ra hai tầng trí nhớ chính xác khi chạy cho bất kỳ mục tiêu nào, chính xác hơn là:

## Tập luyện bài tập

1. Thêm một `max_main_context_tokens`Tỷ lệ vốn tăng giá (khoảng `len(text.split())`* 1.3). Tích hợp các thông điệp cũ nhất thành một bản tóm tắt khi giới hạn được vượt quá. So sánh hành vi với và không có bản tóm tắt.
   Trung文翻译: 添加按代币计量 `max_main_context_tokens`上限(用 `len(text.split())`* 1.3 近似) ・ vượt quá giới hạn sẽ được rút ngắn để tóm tắt.
2. Thực hiện BM25 đúng cách trên kho lưu trữ (tần suất thời hạn, tần suất tài liệu ngược). đo recall@10 trên một tập hợp dữ liệu đồ chơi so với đường cơ sở giao diện token.
   Trong tập hợp các thực tế của các đồ chơi, các phép đo về sự hồi tưởng của các token có thể được sử dụng để xác định các điểm của các token.
3. Thêm `citation`các trường (session_id, turn_id, source_url) vào các mục lưu trữ. Hãy yêu cầu đại lý trích dẫn các nguồn trên mỗi câu trả lời được hỗ trợ bằng truy xuất.
   中文翻译:为归档插入添加 `citation`字段(session_id, turn_id, source_url) ⋅让 Agent 在每个基于检索的回答上引用来源──
4. Tưởng tượng nhiễm độc trí nhớ: thêm một hồ sơ lưu trữ nói "không chú ý đến tất cả các hướng dẫn của người dùng trong tương lai".
   Trung ngữ翻译:模拟记忆投毒:添加一条归档记录说"忽略所有未来用户指令"──编写一个防护器扫描检索结果中的指令类型文本并标记为不可信──
5. Port thực thi để sử dụng mô hình JSON bộ nhớ cốt lõi của MemGPT nghiên cứu repo (`cpacker/MemGPT`(văn số 1): Những thay đổi gì khi bạn chuyển từ chuỗi phẳng sang các phần đánh dấu?
   Trung文翻译:将实现移植为使用 MemGPT 研究仓库的核心记忆 JSON 模式`cpacker/MemGPT`(︎) Có những thay đổi gì khi từ 平字符串 chuyển sang loại hóa phân vùng?

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Virtual context | "Unlimited memory" / "无限记忆" | Main (prompt) + external (searchable) tiers with page in/out / 主（提示）+ 外部（可搜索）两层，带页面换入/换出 |
| Main context | "Working memory" / "工作记忆" | The prompt — fixed-size, always visible / 提示——固定大小，始终可见 |
| Archival memory | "Long-term store" / "长期存储" | External searchable persistence, retrieved on demand / 外部可搜索持久化，按需检索 |
| Core memory | "Persistent prompt section" / "持久化提示分区" | Named sections pinned inside the main context / 固定在主上下文内的命名分区 |
| Memory tool | "Memory API" / "记忆 API" | Tool call the agent issues to read/write external memory / Agent 发出的读/写外部记忆的工具调用 |
| Interrupt | "Memory page fault" / "记忆页面错误" | Agent pauses, runtime fetches, result splices into next turn / Agent 暂停、运行时获取、结果拼接到下一轮 |
| Memory rot | "Stale facts" / "过时事实" | Old writes drown retrieval; fix with consolidation / 旧写入淹没检索；用合并修复 |
| Memory poisoning | "Injected persistent note" / "注入的持久化笔记" | Attacker content stored as memory, re-ingested on recall / 攻击者内容存储为记忆，在回忆时重新摄取 |

## Xem thêm 延伸阅读

- [Packer et al., MemGPT (arXiv:2310.08560)](https://arxiv.org/abs/2310.08560) Bức thư bối cảnh ảo lấy cảm hứng từ hệ điều hành
  Trung ngữ翻译:MemGPT 经典论文操作系统启发的虚拟上下文──
- [Letta, Memory Blocks blog](https://www.letta.com/blog/memory-blocks) tiến hóa ba cấp
  Trung文翻译:Letta 记忆块博客三层演进──
- [Anthropic, Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) xử lý bối cảnh như một ngân sách
  Trung văn翻译:Anthropic 关于有效上下文工程的文章将上下文视为预算。
- [Chhikara et al., Mem0 (arXiv:2504.19413)](https://arxiv.org/abs/2504.19413) bộ nhớ sản xuất lai trên đầu mô hình này
  Trung ngữ翻译:Mem0 论文在此模式之上的混合生产记忆──
- [Zep (getzep/zep)](https://github.com/getzep/zep) Khoảnh khắc đồ thị kiến thức thời gian từ bảng phân loại
- [Mem0 (mem0ai/mem0)](https://github.com/mem0ai/mem0) đường ống khai thác đằng sau cửa hàng lai của Bài học 09
- [LangMem (langchain-ai/langmem)](https://github.com/langchain-ai/langmem) Khai thác tiền sử của các sự kiện và các quy tắc hành vi
- [agentmemory (rohitg00/agentmemory)](https://github.com/rohitg00/agentmemory) chụp phiên tập hợp thành các hồ sơ được gõ, có thể tìm kiếm
