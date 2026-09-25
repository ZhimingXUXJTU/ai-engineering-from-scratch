# Kiến trúc hàng đầu và chế độ thất bại của nó

> Các nhà quản lý là những người quản lý, các nhân viên quản lý là những người quản lý.`Process.hierarchical`là phiên bản sách giáo khoa: a `manager_llm`Động lực phân bổ nhiệm vụ và xác nhận đầu ra.`create_supervisor(create_supervisor(...))`. Đây là mô hình tự nhiên khi công việc là một biểu đồ cơ cấu thực tế. Nó cũng là mô hình có nhiều khả năng sụp đổ vào vòng lặp quản lý.

> **【中文解读】**Phần này giới thiệu cấu trúc phân cấp của nhiều tầng tổ chức tổ chức được sử dụng cho việc phân giải các nhiệm vụ phức tạp.

> **【拓展：hierarchical architecture→具体应用】**Các cấu trúc phân cấp sẽ chuyển sang mô hình giám sát viên  cấp trên quản lý phân bổ cho quản lý cấp trung, quản lý cấp trung phân bổ lại cho nhân viên cấp dưới.


**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 16 · 05 (Supervisor Pattern) | **前置知识:** Phase 16 · 05 (监督者模式)
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**Học本节前请先掌握:Phase 16·05(Supervisor 模式)。本节 = Supervisor 嵌套 Supervisor多层管理。失败模式 = "Các quản lý mở cuộc họp và không làm gì"。
>  **【类比】**Cấp cấu trúc = "Cấp cấp công ty"──1 tầng = 创业公司(CEO 直接带工程师);2-3 tầng = 中型公司(最优);4+层 = 大企业病(信息失真、决策缓慢、经理们皮)──Agent cũng như2-3层最优,多了就"管理循环":经理 经理 相互指派却不真做事──
> ️ **【易错点】**Xem " nhiệm vụ phức tạp" về cấp độ gia tăng → 管理开销压系统──修复:先用序列或监督者单层跑,确认不够再分层;2-3层是上限──

##                                                                                                                                                                                                                                                               

Khi mô hình giám sát viên được nhấp vào, bước tiếp theo là "vì những người lao động tự mình là giám sát viên?" Các nhóm có các nhóm phụ; các công ty có các bộ phận của các bộ phận. Các kiến trúc hàng đầu phản ánh điều đó.

> Một khi mô hình giám sát viên được hiểu, bước tiếp theo của tự nhiên là "Nếu các thiết bị làm việc cũng là giám sát viên sao?"

Sự cám dỗ là mạnh mẽ bởi vì các tổ chức của con người hoạt động theo cách này. Nhưng các bậc bậc bậc LLM thừa hưởng tất cả các bệnh lý của bậc bậc bậc của con người (sự mất thông tin, giao tiếp sai, lặp lại chậm) mà không có tác động ổn định của các mối quan hệ con người và văn hóa chung.

> 诱惑 rất mạnh, vì tổ chức nhân loại làm việc như vậy. Nhưng cấp độ LLM thừa kế tất cả các bệnh tật cấp độ nhân loại, nhưng không có hiệu ứng ổn định của mối quan hệ và văn hóa chia sẻ nhân loại.

Vấn đề: Các nhà quản lý LLM không giống như các nhà quản lý con người. Một nhà quản lý con người có tiền lệ ổn định về những gì báo cáo của họ biết. Một nhà quản lý LLM tái hợp lý luận về tổ chức mỗi lần từ bất cứ điều gì trong bối cảnh của nó. Sự trôi dạt nhỏ trong bối cảnh đó, và toàn bộ cây phân bổ sai trái công việc.

>  vấn đề nằm ở: LLM  quản lý khác với người quản lý.  Người quản lý con người biết những gì có sự cố định trước tiên đối với những người thuộc về nó.

Đây là chế độ thất bại cốt lõi của các hệ thống LLM hàng bậc: mỗi cấp quản lý tăng cường các lỗi của cấp độ trước đó.

> Đây là mô hình thất bại cốt lõi của hệ thống LLM: mỗi cấp quản lý cấp độ tăng lên một lớp lỗi.

## Khái niệm cốt lõi

### Hình dạng

```
                 Manager
                 ┌─────┐
                 └──┬──┘
           ┌────────┴────────┐
           ▼                 ▼
       Sub-Mgr A         Sub-Mgr B
       ┌─────┐           ┌─────┐
       └──┬──┘           └──┬──┘
         ┌┴──┬──┐          ┌┴──┐
         ▼   ▼  ▼          ▼   ▼
       W1  W2  W3         W4  W5
```

Mỗi nút nội bộ lập kế hoạch, đại diện và tổng hợp.

> Mỗi nội bộ lập kế hoạch, ủy ban và tổng hợp. Chỉ có các cột làm việc thực tế.

Điều này phản ánh biểu đồ cơ quan con người, đó là cả sức mạnh (chương trình tâm lý quen thuộc) và yếu đuối (những cơ quan con người có tiền lệ ổn định mà LLM thiếu).

> Đây là một bản đồ về cấu trúc tổ chức của con người, đây là cả lợi thế của nó (được biết đến với mô hình tâm trí) cũng là điểm yếu của nó (được biết đến với các mô hình tâm lý) tổ chức của con người có LLM thiếu sự cố định trước tiên)

### Ở nơi nó tỏa sáng

- **Clear org mapping.**Nếu nhiệm vụ thực sự là bộ phận ("sự xem xét pháp lý tài liệu, tài chính xem xét tài liệu, kỹ thuật xem xét tài liệu, sau đó tóm tắt cho exec"), hệ thống phân cấp là rõ ràng.
  Trung ngữ翻译:**清晰的组织映射。**Nếu nhiệm vụ thực tế là của bộ phận (("quản lý kiểm tra tài liệu, tài chính kiểm tra tài liệu, kỹ thuật kiểm tra tài liệu, sau đó là cho quản lý tổng kết"), cấu trúc cấp là rõ ràng.
- **Local summarization.**Mỗi người phụ quản lý tổng hợp sản lượng của nhóm trước khi người quản lý hàng đầu nhìn thấy nó. Người quản lý hàng đầu nhìn thấy ba bản tóm tắt của người phụ quản lý, chứ không phải mười lăm sản lượng của công nhân.
  Trung ngữ翻译:**局部摘要。**Mỗi nhà quản lý ở cấp trên nhìn thấy trước tổng hợp các sản phẩm của nhóm của mình.

### Khi nó vỡ

Ba chế độ thất bại các bài kiểm tra sau năm 2026 tiếp tục tìm thấy:

> 2026 năm sự kiện phân tích liên tục phát hiện ra ba mô hình thất bại:

Cemri et al. (MAST, arXiv:2503.13657) ghi lại những thứ này như là "sự thất bại trong việc xác định" và "sự không phù hợp giữa con người".

> Cemri 等人(MAST,arXiv:2503.13657) sẽ ghi lại những vấn đề này như " quy tắc thất bại" và " nhân际不对齐"子家族──分层系统比平系统更容易出现这些问题,因为每个层添加重新解释步骤──

1. **Task assignment error.**Người quản lý đọc mục tiêu, ảo giác phân hủy và ủy thác cho người quản lý phụ sai. Bởi vì người quản lý phụ tuân thủ làm việc trên những gì nó đã được trao, lỗi chỉ xuất hiện ở tổng hợp trên cùng một cấp độ xa nơi mà một con người có thể đã bắt được nó.
   Trung ngữ翻译:**任务分配错误。**管理者读取目标,幻觉出分解,并委派给错误的子管理者──因为子管理者服从处理给定的任务,错误只存在于顶层综合时时浮现高于人类本能抓获的位置一层――
2. **Output misinterpretation.**Sub-manager trả lại "không thể xác minh yêu cầu X". Top manager tóm tắt như " yêu cầu X không được xác nhận. " Ý nghĩa biến động ở mọi cấp độ.
   Trung ngữ翻译:**输出误解。**子管理者返回" không xác nhận tuyên bố X──"Top level administrator总结为" tuyên bố X 未确认──"含义在每层都漂移──"
3. **Consensus loops.**Hai người phụ quản lý không đồng ý; người quản lý hàng đầu yêu cầu họ hòa giải; họ chuyển nhượng lại; nhân viên chạy lại; người phụ quản lý trả lời khác nhau một chút; vòng lặp.`Process.hierarchical`Có những biện pháp bảo vệ chống lại điều này với giới hạn bước, nhưng giới hạn chính nó bây giờ là một siêu tham số.
   Trung ngữ翻译:**共识循环。**Hai người quản lý không nhất trí; người quản lý cấp trên yêu cầu họ phối hợp; họ hướng xuống tái ủy nhiệm; máy工作器 tái vận hành; người quản lý trở lại có câu trả lời khác nhau; vòng.`Process.hierarchical`通过步骤限制来保护, nhưng hạn chế tự nó hiện là một siêu参数.

### Câu hỏi quyết định

Tiếp theo (hạch đường ống) vs bậc phân cấp: nhiệm vụ của bạn có thực sự có các nhóm phụ độc lập, hoặc nó là một dòng dòng tuyến tính giả vờ là một cây? Nếu thứ hai, sử dụng thứ tự. Nếu thứ nhất, sử dụng các quy tắc hòa giải bậc phân cấp nhưng ngân sách rõ ràng.

> 顺序(线性流水线) vs 分层: nhiệm vụ của bạn thực sự có một nhóm phụ độc lập, còn là một quá trình线性 giả tạo thành cây? Nếu là sau, sử dụng顺序. Nếu là trước, sử dụng phân tầng nhưng cần ngân sách rõ ràng của quy tắc phối hợp.

Đây là bài kiểm tra mà hầu hết các nhóm bỏ qua. Họ tìm kiếm thứ tự vì nó nghe có vẻ phức tạp, sau đó dành hàng tuần để cố gắng làm trục trặc sự phân hủy. Các đường ống theo trình kết thúc nhanh hơn, dễ dàng hơn và hiếm khi "kết mất cốt truyện".

> Đây là bài kiểm tra mà hầu hết các nhóm nhảy qua. Họ chọn phân tầng vì nghe có vẻ cao cấp, sau đó dành vài tuần để thử phân tách và di chuyển.

### Việc thực hiện CrewAI
### Thực hiện khung vai trò

Đội ngũ của CrewAI `Process.hierarchical`Người quản lý:

> `Process.hierarchical`Trong nhóm chuyên gia kết nối một quản lý LLM── quản lý:

Người quản lý LLM là một đại lý đầy đủ với bối cảnh, prompt và công cụ riêng của mình. Nó không phải là một nhà phân phối xác định.

> 管理者 LLM bản thân là một người làm việc đầy đủ của mình trên các văn bản, gợi ý và công cụ. Nó không phải là một điều chỉnh xác định, nó làm cho các ủy ban đưa ra phán quyết, điều đó có nghĩa là nó có thể đưa ra phán quyết sai lầm về việc đưa ra phán quyết.

- nhận nhiệm vụ cấp cao,
  Trung ngữ翻译:接收顶层任务,
- Đề xuất các nhiệm vụ phụ cho các phi hành đoàn,
  Trung ngữ翻译:将子任务分配给团队,
- đánh giá các sản phẩm của phi hành đoàn,
  Trung ngữ翻译:评估团队输出,
- quyết định xem phải chấp nhận, đại diện lại hay lặp lại.
  Trung ngữ翻译:决定是接受、重新委派还是代──

Tài liệu: https://docs.crewai.com/en/introduction(đ tìm "Phương trình hàng bậc" trong các khái niệm cốt lõi).

> 文档:https://docs.crewai.com/en/introduction（在核心概念中查找"HierarchicalQuá trình") ").

### Việc thực hiện LangGraph
### Thực hiện khung đồ thị

LangGraph sử dụng nested `create_supervisor`Người giám sát bên trong có biểu đồ riêng của mình; người giám sát bên ngoài xử lý biểu đồ bên trong như một nút không rõ ràng. Điều này sạch hơn CrewAI để gỡ lỗi (bạn có thể bước qua mỗi biểu đồ riêng biệt) nhưng khó khăn hơn để thể hiện sự tái định hình động của cây.

> LangGraph sử dụng các bộ `create_supervisor`调用── giám sát viên bên trong có bản đồ riêng của mình; giám sát viên bên ngoài sẽ xem bản đồ bên trong như một nét không minh bạch── điều này trong khía cạnh调试 có thể rõ ràng hơn so với CrewAI, nhưng khó hơn để thể hiện động thái của cây tái tạo──

Sự thắng lợi trong việc gỡ lỗi là thực: khi có gì đó sai trong một hệ thống phân cấp LangGraph 3 cấp, bạn có thể cô lập mức thất bại bằng cách bước qua mỗi biểu đồ độc lập.

> 调试优势真实: Khi 3 cấp độ LangGraph cấp độ sai, bạn có thể thông qua các bước độc lập vào mỗi bức tranh để tách ra những cấp độ thất bại. Trong CrewAI, quản lý LLM là một có thể ủy thác sai lầm không minh bạch调用.

Đề xuất: https://reference.langchain.com/python/langgraph-supervisor.

> 参考:https://reference.langchain.com/python/langgraph-supervisor。

## Hãy xây dựng nó.
```figure
swarm-hierarchy-token
```

## Hãy xây dựng nó

`code/main.py`chạy một hệ thống phân cấp 3 cấp:

> `code/main.py`运行一个3层层级:

- Giám đốc cấp cao: chia một nhiệm vụ thành các ngành "kỹ thuật" và "quyền",
  Trung ngữ翻译:顶层管理者:将任务分分为工程和法务分支,
- Phó quản lý kỹ thuật: chia thành công nhân "phát" và "phát",
  Trung ngữ翻译:工程子管理者:拆分为"前端"和"后端"工作器,
- Phó giám đốc pháp lý: một nhân viên.
  Trung ngữ翻译:法务子管理者:一个工作器──

Demo tương phản happy path (tất cả mọi người đồng ý) với một **perturbed path**khi phân hủy của người quản lý hàng đầu ghi sai " hợp pháp" là " tài chính" và xem các lỗi hàng loạt  người phụ quản lý vâng lời làm việc tài chính, bộ tổng hợp hàng đầu báo cáo kết quả tài chính, câu hỏi pháp lý ban đầu không được trả lời.

> 演示对比了正常路径 (所有人一致) với**扰动路径**, trong đó phân tích quản lý cấp cao sẽ "lập pháp" được đánh dấu sai là " tài chính"并 quan sát sai cấp liên kết quản lý tuân thủ làm việc tài chính, báo cáo tổng hợp cấp cao tài chính phát hiện, vấn đề pháp lý ban đầu không được trả lời.

Đường lối bị rối loạn là cảnh báo: các hệ thống phân cấp tăng cường lỗi lặng lẽ. Người phụ quản lý không đẩy lùi ("bạn nói tài chính, nhưng nhiệm vụ nói hợp pháp"). Nó cho rằng người quản lý biết tốt hơn. Khi ai đó nhận ra, ý định ban đầu đã bị mất.

> 扰动路径是警告:分层系统静默放大错误――子管理者不反驳("Các bạn nói về tài chính, nhưng nhiệm vụ nói về pháp务")――它假设管理者更了解──当任何人注意到时,原始意图已丢失──

Đi chạy:

```
python3 code/main.py
```

Kết quả cho thấy cả hai con đường với một bên cạnh rõ ràng của "cái gì đã được yêu cầu" vs "cái gì đã được giao".

> 输出显示两条路径的清晰并排对比:" yêu cầu gì"与"交付什么"

## Hãy sử dụng nó để thực hiện

`outputs/skill-hierarchy-fitness.md`đánh giá liệu một nhiệm vụ nhất định có nên sử dụng trình tự phân cấp, trình tự hoặc giám sát phẳng không. Các đầu vào: mô tả nhiệm vụ, cấu trúc tổ chức, ngân sách hòa giải.

> `outputs/skill-hierarchy-fitness.md` đánh giá các nhiệm vụ nhất định nên sử dụng phân cấp 序列还是平监督者──输入: nhiệm vụ mô tả、组织结构、协调预算──输出:模式建议及需要防护的特定失败模式──输出:模式建议及需要防护的特定失败模式──输入: mô hình mô hình

## Chuyển nó đi.

Nếu bạn vận chuyển hàng bậc:

> Nếu bạn triển khai cấu trúc:

- **Cap tree depth at 2.**Ba cấp độ đã che giấu hầu hết các lỗi khỏi khả năng quan sát.
  Trung ngữ翻译:**将树深度限制在 2。**Ba tầng đã được hầu hết các sai lầm ẩn trong khả quan sát ngoài.
- **Explicit reconciliation budget.**Đặt tối đa các vòng trước khi người quản lý hàng đầu phải cam kết.
  Trung ngữ翻译:**明确的协调预算。**Trong cấp trên quản lý phải gửi trước khi đặt số vòng tối đa.
- **Provenance on every synthesis.**Kết luận của mỗi nút phải nêu ra các sản phẩm từ lá nào đã tạo ra nó.
  Trung ngữ翻译:**每次综合的来源追溯。**Mỗi đoạn trích của mỗi nút phải trích dẫn để tạo ra các con cái của nó.
- **Alert on decomposition drift.**Lập mục phân hủy của quản lý theo từng bước; khác với truy vấn của người dùng. Nếu phân hủy không còn bao gồm truy vấn, hãy kích hoạt cảnh báo.
  Trung ngữ翻译:**分解漂移告警。**记录管理员的每步的分解;与用户查询对比. Nếu phân giải không còn bao gồm các truy vấn,触发告警.

## Tập luyện bài tập

1. Đi chạy`code/main.py`và so sánh happy vs disturbed. cần bao nhiêu cấp độ quản lý giao ra trước khi đầu ra hàng đầu hoàn toàn khác biệt với câu hỏi của người dùng?
   Trung ngữ翻译:运行 `code/main.py`Không so sánh con đường bình thường với con đường nhiễu. Phải có bao nhiêu cấp quản lý giao tiếp để làm cho cấp trên xuất ra hoàn toàn tách rời khỏi người dùng vấn đề?
2. Thêm một cấp độ thứ ba (trên -> dưới -> dưới -> nhân viên). đo đạc số lần con đường bị nhiễu loạn tự sửa chữa và hoàn toàn khác nhau khi độ sâu tăng lên.
   Trung文翻译:添加第三层(顶层 -> 子 -> 子子 -> 工作器) ⋅ đo lường theo chiều sâu tăng lên, làm rối loạn đường lối tự khắc phục với tần suất hoàn toàn lệch离.
3. Thực hiện một nhân viên "canary" tại mỗi người quản lý phụ luôn được hỏi câu hỏi người dùng ban đầu không thay đổi. Sử dụng câu trả lời canary để phát hiện sự trôi dạt phân hủy. Người quản lý nên phản ứng như thế nào khi canary không đồng ý với câu trả lời tổng hợp?
   Trung ngữ翻译: 在每个子管理员处实现一个"金雀"工作器,总是被问及原始用户问题不变――使用金雀答案检测分解漂移――当金雀与综合答案不一致时,管理员应如何反应?
4. Đọc CrewAI `Process.hierarchical`Docs. xác định một màn chắn bê tông CrewAI áp dụng (khuyết hạn bước, quản lý_llm) và mô tả chế độ thất bại mà nó nhắm mục tiêu.
   Trung ngữ翻译:阅读 CrewAI 的 `Process.hierarchical`文档──识别 CrewAI 应用一个具体防护措施(步骤限制、管理员_llm 约束)并描述它针对的失败模式──
5. So sánh các giám sát viên LangGraph nhúng với hệ thống phân cấp CrewAI.
   Trung ngữ翻译:Comparing嵌套的 LangGraph 监督者与 CrewAI 分层──哪个使协调循环更容易检测?

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Hierarchical / 分层 | "Org chart pattern" / "组织架构模式" | Supervisors over supervisors; only leaves do work. / 监督者之上还有监督者；只有叶子节点做实际工作。 |
| Manager LLM / 管理者 LLM | "The boss" / "老板" | The LLM that decomposes, assigns, and validates at an internal node. / 在内部节点进行分解、分配和验证的 LLM。 |
| Decomposition drift / 分解漂移 | "The boss lost the plot" / "老板偏离了主题" | Top manager's split no longer covers the original question. / 顶层管理者的拆分不再覆盖原始问题。 |
| Reconciliation loop / 协调循环 | "Endless meetings" / "无尽会议" | Sub-managers disagree; top re-delegates; workers re-run; loop until budget exhausted. / 子管理者不一致；顶层重新委派；工作器重新运行；循环直到预算耗尽。 |
| Depth-2 ceiling / 深度-2 上限 | "Don't go deeper than 2 levels" / "不要超过 2 层" | Empirical guardrail: 3+ levels collapses observability. / 经验防护：3+ 层使可观测性崩溃。 |
| Canary question / 金丝雀问题 | "Ground truth at every level" / "每层的基准真相" | A worker that is always asked the original query unchanged, to detect drift. / 一个总是被问及原始查询不变的工作器，用于检测漂移。 |
| Provenance chain / 来源链 | "Who said what" / "谁说了什么" | Trace from each synthesis back to the leaf outputs that produced it. / 从每个综合追溯到产生它的叶子输出。 |

## Xem thêm 延伸阅读

- [CrewAI introduction — Process.hierarchical](https://docs.crewai.com/en/introduction) sách giáo khoa bậc bậc với một quản lý LLM
  Trung文翻译:CrewAI 介绍  Process.hierarchical 带管理者 LLM 的教科书式分层
- [LangGraph supervisor reference](https://reference.langchain.com/python/langgraph-supervisor) giám sát viên tổ hợp qua `create_supervisor`
  中文翻译:LangGraph 监督者参考  通过 `create_supervisor`của các giám sát viên
- [Anthropic engineering — Research system](https://www.anthropic.com/engineering/multi-agent-research-system) tại sao Anthropic cố ý chọn giám sát viên phẳng hơn là cấp bậc
  Trung文翻译:Anthropic 工程  研究系统  Tại sao Antropic 有意选择平监督者而不是分层
- [Cemri et al. — Why Do Multi-Agent LLM Systems Fail?](https://arxiv.org/abs/2503.13657) Định dạng phân loại MAST; phần về các thất bại phối hợp tài liệu phân hủy
  Trung ngữ翻译:Cemri 等人  为什么多 Agent LLM 系统会失败?  MAST 分类法;协调失败部分记录了分解漂移
