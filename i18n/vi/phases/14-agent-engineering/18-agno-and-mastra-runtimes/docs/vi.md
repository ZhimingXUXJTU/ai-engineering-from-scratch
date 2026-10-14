# Agno và Mastra: Thời gian sản xuất
# Thời gian vận hành của đại lý sản xuất  Lần thực hiện nhanh và dòng công việc được đánh dấu

> Một trình sản xuất vận hành thời gian tối ưu hóa những gì các khung nguyên mẫu bỏ qua: chi phí thực hiện, bề mặt luồng công việc được gõ, và một phần mềm sẵn sàng phục vụ. Sự kết hợp năm 2026: Agno (Python) nhằm mục đích thực hiện thực hiện đại lý microsecond và các phần mềm FastAPI không có trạng thái. Mastra gửi các đại lý, công cụ, luồng công việc, định tuyến mô hình thống nhất và lưu trữ tổng hợp trên nền SDK Vercel AI.

**Type:** Learn | **类型:** 学习
**Languages:** Python, TypeScript | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 01 (Agent Loop), Phase 14 · 13 (LangGraph) | **前置知识:** 见原文
**Time:** ~45 minutes | **时间:** 见原文

## Mục tiêu học tập

- Hãy xác định mục tiêu hiệu suất của Agno và khi nào chúng quan trọng.
- Tên gọi ba nguyên thủy của Mastra  Đại lý, Công cụ, Luồng làm việc  và các bộ điều chỉnh máy chủ được hỗ trợ.
- Giải thích tại sao một backend FastAPI không có nội dung được phân tích theo phiên bản là con đường sản xuất Agno được khuyến cáo.
- Chọn Agno vs Mastra cho một đống nhất định (Python-đầu tiên vs TypeScript-đầu tiên).

## Vấn đề  vấn đề giới thiệu

LangGraph, AutoGen, CrewAI là các khung nặng. Các nhóm muốn "chỉ cần vòng tròn đại lý, nhanh chóng, trong thời gian chạy của tôi" tiếp cận với Agno (Python) hoặc Mastra (TypeScript). Cả hai đều trao đổi một số nguyên thủy thuộc sở hữu khung cho tốc độ thô và phù hợp chặt chẽ hơn với hàng đống xung quanh.

> LangGraph、AutoGen、CrewAI đều là một khung có trọng lượng cao hơn. ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️ ➡️


> **【中文解读】**Agno 和 Mastra đại diện cho hai loại Agent của năm 2026 运行时设计哲学。Agno(原 PhiData) theo đuổi极简 với ít nhất mã xây dựng Agent。Mastra(TypeScript) theo đuổi đầy đủ chức năng cung cấp đầy đủ Agent 生命周期管理。 lựa chọn phụ thuộc vào kỹ thuật và nhu cầu phức tạp của nhóm。

> **{【拓展：Agno (GitHub 15k+ stars) 和 Mastra 是 2026 年 Agent 运...】}**Agno (GitHub 15k+ sao) 和 Mastra là 2026 năm Agent 运行时的新秀。Agno của triết lý là 'Agent 即函数' Mỗi Agent là một hàm khác biệt có bộ dụng cụ. Mastra dựa trên TypeScript, hướng tới toàn bộ nhà phát triển, cung cấp đầy đủ của Agent 生命周期管理(部署、监控、扩展)。 cả hai đều hỗ trợ nhiều mô hình hậu端 và MCP 集成。

>  **【前置】**必须先掌握:Phase 14·01(Agent Loop) vàPhase 14·13(LangGraph) 本节是这两者"轻量替代品"──如果不知道为什么要"轻量化"LangGraph,说明你还没在生产中遇到LangGraph的工程负担,建议先使用LangGraph 几周再回头看本节──

## Khái niệm cốt lõi

### Agno

- Thời gian chạy Python, trước đây là Phi-data.
- "Không có đồ thị, chuỗi, hoặc các mẫu phức tạp  chỉ là Python thuần túy".
- Mục tiêu hiệu suất từ tài liệu của họ: ~ 2μs đại lý thực hiện, ~ 3,75 KiB bộ nhớ mỗi đại lý, ~ 23 nhà cung cấp mô hình.
- Chế độ sản xuất: FastAPI backend không có trạng thái phiên bản. Mỗi yêu cầu bắt đầu một đại lý mới; trạng thái phiên bản sống trong DB.
- Native multimodal (text, image, audio, video, file) và RAG cơ quan.

Các mục tiêu tốc độ quan trọng khi bạn có hàng ngàn nhân viên ngắn ngủi mỗi giây (bàn máy trò chuyện, đường ống đánh giá), nhưng ít quan trọng hơn khi một nhân viên chạy trong 10 phút.

>  **【类比】**Agno 像摩托车、LangGraph 像SUV:摩托车启动快、轻便、能钻小(2μs 实例化、3.75 KiB 内存),适合短途高频通勤(每秒数千短任务);SUV 装得多、能跑长途、有空调导航(持久化、人回路、复杂图), nhưng khởi động、慢占地大──**关键洞察**:                                                                                                                                                                                                                                                               

> 速度目标 bạn có hàng ngàn nhân viên tạm thời mỗi giây rất quan trọng. Khi một nhân viên chạy 10 phút, chúng không quan trọng như vậy.

> Agno 和 Mastra là hai loại đại lý hạng nhẹ 运行时.Agno 专注快速构建,Mastra 专注 TypeScript 生产部署.

### Mastra

- TypeScript, được xây dựng trên Vercel AI SDK.
- Ba nguyên thủy:**Agents**- **Tools**(Tý dạng vùng),**Workflows**- Tôi không biết.
- Mô hình thống nhất Router  3,300+ mô hình trên 94 nhà cung cấp (tháng 3 năm 2026).
- lưu trữ kết hợp: bộ nhớ, luồng công việc, khả năng quan sát cho các nền khác nhau; ClickHouse được khuyến cáo để có thể quan sát được ở quy mô.
- Apache 2.0 với `ee/`Các thư mục dưới giấy phép doanh nghiệp có sẵn từ nguồn.
- Các bộ điều chỉnh máy chủ cho Express, Hono, Fastify, Koa; kết hợp Next.js và Astro hạng nhất.
- Tàu Mastra Studio (localhost:4111) để debugging.
- 22k+ GitHub sao, 300k+ tải về npm hàng tuần ở mức 1.0 (Từ tháng 1 năm 2026).

### Định vị

Họ cũng không muốn trở thành LangGraph.

> Cả hai đều không cố gắng trở thành LangGraph.

> Agno 和 Mastra là hai loại đại lý hạng nhẹ 运行时.Agno 专注快速构建,Mastra 专注 TypeScript 生产部署.

- **Language fit.**Agno cho các nhóm đầu tiên của Python; Mastra cho TypeScript đầu tiên.
- **Runtime ergonomics.**Agno = gần không chi phí hàng đầu; Mastra = tích hợp với hệ sinh thái Vercel.
- **Observability.**Cả hai tích hợp với Langfuse / Phoenix / Opik (Dạy 24) nhưng Mastra Studio là bên đầu tiên.

### Khi nào để chọn mỗi

- **Agno** Python backend, nhiều đại lý ngắn ngủi, yêu cầu perf mạnh mẽ, FastAPI shop.
- **Mastra** TypeScript backend, Next.js / Vercel triển khai, định tuyến mô hình đa nhà cung cấp thống nhất, công cụ kiểu Zod.
- **LangGraph**(Dân học 13)  khi trạng thái bền và lý luận biểu đồ rõ ràng quan trọng hơn tốc độ thô.
- **OpenAI / Claude Agent SDK** khi bạn muốn hình dạng sản xuất của nhà cung cấp (Dạy học 1617).

### Khi mô hình này đi sai

> ️ **【易错点】**见Agnó "2μs 实例化"就无脑选Agnó。**后果**Nếu trường hợp của bạn là "một lần yêu cầu chạy một đại lý 10 phút", 2μs  thực thi hóa ảnh hưởng đến tổng tiêu thụ thời gian là 0.0000003%  chọn sai khung cũng mất khả năng bền vững của LangGraph.**一行修复**:先测量您的工作负载的"Agent 实例化次数 × 单次实例化开销 vs 总耗时", chiếm > 30% 才值得的性能选择 Agno,否则继续使用 LangGraph。

- **Perf-for-perf's-sake.**Chọn Agno vì "2μs" nghe có vẻ tốt khi tải trọng công việc là một cuộc gọi chậm của đại lý theo yêu cầu.
- **Ecosystem lock-in.**Sự tích hợp hương vị Vercel của Mastra là một cộng với Vercel, một trừ ở nơi khác.
- **Enterprise license confusion.**Mastra của `ee/`thư mục có nguồn, không phải Apache 2.0. đọc giấy phép nếu bạn đang lên kế hoạch để fork.

> 🤔 **【困惑】**Q: 我团队是Python 后端,又想要Mastra's"多模型路由"功能,能用Agno 实现吗? A: 能,但要自己写;;Agno cũng có ~23 nhà cung cấp mô hình, nhưng Mastra's 3300+ 模型 94 nhà cung cấp dựa trên Vercel AI SDK's庞大生态;; Nếu"模型路由" là yêu cầu cốt lõi và nhóm chấp nhận TypeScript,Mastra là sự lựa chọn của tỉnh hơn; nếu kiên trì vào Python,Agno + tự đóng gói một lớp mô hình router cũng đi, khối lượng công việc khoảng 2-3 天;; không phải là khung quyết định về kỹ thuật,反过来;;

> **为性能而性能。**Vì "2μs" nghe có vẻ không sai khi chọn Agno, và tải trọng công việc là mỗi yêu cầu một đại lý chậm 调用.
> **生态系统锁定。**Mastra's Vercel 风格集集在Vercel 上是优势,在其他地方是劣势.
> **企业许可困惑。**Mastra của `ee/`Nó là mã nguồn có sẵn, không phải Apache 2.0. Nếu bạn muốn chia rẽ, hãy đọc giấy phép trước.

## Hãy xây dựng nó.
```figure
wb-runtime-spawn
```

## Hãy xây dựng nó

Bài học này chủ yếu là so sánh  không có một tạo vật mã duy nhất sẽ làm cho cả hai khung công bằng. Xem `code/main.py`cho một đồ chơi bên cạnh: một dòng chảy tối thiểu "đưa ra một chất, truyền ra đầu ra, tiếp tục phiên" được thực hiện hai lần (một lần hình Agno, một lần hình Mastra).

> Bài học này chủ yếu là so sánh tính chất không có một sản phẩm mã có thể thể thể hiện được đặc điểm của hai khung.`code/main.py`Trung 并排演示: một quá trình "运行 Agent"",流式输出"",持久化会话" được thực hiện hai lần (một lần Agno 形态, một lần Mastra 形态) 

> Agno 和 Mastra là hai loại đại lý hạng nhẹ 运行时.Agno 专注快速构建,Mastra 专注 TypeScript 生产部署.

Đi đi.

```
python3 code/main.py
```

Hai dấu vết khác nhau về cấu trúc nhưng tương đương về chức năng.

> Hai cấu trúc khác nhau nhưng chức năng của giá cả giống nhau theo dõi.

> Agno 和 Mastra là hai loại đại lý hạng nhẹ 运行时.Agno 专注快速构建,Mastra 专注 TypeScript 生产部署.

## Hãy sử dụng nó để thực hiện

- **Agno** Python backend cần tốc độ và hình dạng FastAPI.
- **Mastra** TypeScript backend với nhiều nhà cung cấp và dòng công việc nguyên thủy.
- Cả hai tàu đều có các cái nén quan sát được sử dụng.

## Chuyển nó đi.

`outputs/skill-runtime-picker.md`chọn Agno, Mastra, LangGraph, hoặc một SDK nhà cung cấp dựa trên xếp chồng, ngân sách độ trễ và hình dạng hoạt động.

> `outputs/skill-runtime-picker.md`根据技术、延迟预算和运营形态选择 Agno、Mastra、LangGraph 或提供商 SDK。

> Agno 和 Mastra là hai loại đại lý hạng nhẹ 运行时.Agno 专注快速构建,Mastra 专注 TypeScript 生产部署.

## Tập luyện bài tập

1. Đọc tài liệu của Agno, chuyển mạch ReAct (Dạy 01) đến Agno.
  Trung ngữ翻译:思考并实践此练习。
2. Đọc các tài liệu của Mastra. Đưa cùng một vòng lặp đến Mastra. Điều gì thay đổi trong công cụ gõ (Zod vs không gì)?
  Trung ngữ翻译:思考并实践此练习。
3. Định nghĩa: đo thời gian trễ của các đại lý trên đống của bạn.
  Trung ngữ翻译:思考并实践此练习。
4. Thiết kế một di chuyển: nếu bạn đã chạy CrewAI trong Python, những gì bị phá vỡ nếu bạn chuyển đến Agno?
  Trung ngữ翻译:思考并实践此练习。
5. Đọc bài của Mastra `ee/`Những hạn chế nào sẽ ảnh hưởng đến một fork mã nguồn mở?
  Trung ngữ翻译:思考并实践此练习。

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| Agno | "Fast Python agents" | Stateless session-scoped agent runtime |  |
| Mastra | "TypeScript agents on Vercel AI SDK" | Agents + Tools + Workflows + Model Router |  |
| Unified Model Router | "Multi-provider access" | Single client for 3,300+ models across 94 providers |  |
| Composite storage | "Multiple backends" | Memory/workflows/observability each to a different store |  |
| Mastra Studio | "Local debugger" | localhost:4111 UI for introspecting agents |  |
| Source-available | "Not OSS" | License permits source reading but restricts commercial use |  |

## Xem thêm 延伸阅读

- [Agno Agent Framework docs](https://www.agno.com/agent-framework) Mục tiêu hiệu suất, tích hợp FastAPI
  Trung ngữ: 翻译:见原文.
- [Mastra docs](https://mastra.ai/docs) nguyên thủy, máy chủ chuyển đổi, Model Router
  Trung ngữ: 翻译:见原文.
- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview) thay thế biểu đồ nhà nước
  Trung ngữ: 翻译:见原文.
- [Comet Opik](https://www.comet.com/site/products/opik/) so sánh khả năng quan sát được trích dẫn bởi các tích hợp Mastra
  Trung ngữ: 翻译:见原文.
