# Các thư viện kỹ năng và học tập suốt đời (Voyager) 技能库与终身学习(Voyager)

> Voyager (Wang et al., TMLR 2024) coi mã thực thi như một kỹ năng. Kỹ năng được đặt tên, có thể lấy lại, hợp tác và tinh chỉnh bằng phản hồi môi trường. Đây là kiến trúc tham chiếu cho kỹ năng SDK của Claude Agent, bộ kỹ năng và mô hình thư viện kỹ năng 2026.

> **【中文解读】**Voyager sẽ có thể thực hiện mã hóa như kỹ năng. Kỹ năng là được đặt tên, có thể tìm kiếm, có thể kết hợp, và thông qua môi trường chống lại tinh luyện. Đây là cấu trúc tham khảo của Claude Agent SDK kỹ năng, kỹ năng và mô hình bộ tài liệu năm 2026 .

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 07 (MemGPT), Phase 14 · 08 (Letta Blocks) | **前置知识:** Phase 14 · 07 (MemGPT), Phase 14 · 08 (Letta 块)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Mục tiêu học tập

- Tên gọi ba thành phần của Voyager  chương trình giảng dạy tự động, thư viện kỹ năng, nhắc nhở lặp đi lặp lại  và vai trò của mỗi.
  Trung ngữ翻译:说出 Voyager's三个组件自动课程、技能库、代提示及各自作用──
- Hãy giải thích tại sao Voyager lại tạo ra mã không gian hành động chứ không phải lệnh nguyên thủy.
  Trung ngữ翻译: giải thích tại sao Voyager sẽ chuyển động không gian đặt cho mã chứ không phải là lệnh ban đầu.
- Thực hiện thư viện kỹ năng stdlib với đăng ký, tìm kiếm, thành phần và tinh chỉnh dựa trên thất bại.
  Trung ngữ翻译:用标准库实现带注册,检索,组合和失败驱动精炼的技能库.
- Bản đồ mẫu của Voyager về kỹ năng SDK của Agent Claude năm 2026 và hệ sinh thái của skillkit.
  Trung ngữ翻译:将 Voyager 模式映射到2026 年 Claude Agent SDK skills 和 skillkit 生态系统。

## Vấn đề  vấn đề giới thiệu

Các đại lý xây dựng lại mọi khả năng từ đầu trong mỗi phiên làm ba điều sai:

> Mỗi lần gặp gỡ, một nhân viên có khả năng xây dựng lại tất cả sẽ làm 3 sai lầm:

1. **Waste tokens.**Mỗi nhiệm vụ lại tạo ra cùng một lý luận.
   Trung ngữ翻译:**浪费 token。**Mỗi nhiệm vụ đều đưa ra những lý do tương tự.
2. **Lose progress.**Một sự sửa đổi được học trong phiên A không chuyển sang phiên B.
   Trung ngữ翻译:**丢失进展。**Trong bài tập A, sự sửa chữa của bài học trung học sẽ không chuyển sang bài tập B.
3. **Fail on long-horizon composition.**Các nhiệm vụ phức tạp cần sự phân cấp khả năng; các lời nhắc đơn giản không thể thể diễn tả chúng.
   Trung ngữ翻译:**在长程组合上失败。**Các nhiệm vụ phức tạp cần các cấp độ năng lực; đơn giản chỉ đơn giản không thể thể hiện chúng.

> **【中文解读】**技能库(Skill Libraries) xuất phát từ Voyager (Wang et al., 2023)  Một đại lý tự tìm kiếm và học tập trong Minecraft.  Sự sáng tạo cốt lõi của Voyager là phát hiện và lưu trữ kỹ năng tự động: Đại lý phát hiện ra một chuỗi hoạt động hiệu quả trong khi thực hiện nhiệm vụ, sẽ mã hóa nó thành hàm kỹ năng có thể sử dụng được lưu trữ vào bộ nhớ kỹ năng.

Câu trả lời của Voyager: coi mỗi khả năng tái sử dụng như một phần mã được đặt tên trong thư viện, có thể lấy lại bằng sự tương đồng, có thể kết hợp với các kỹ năng khác, và được tinh chỉnh bằng phản hồi thực hiện.

> Phản ứng của Voyager: sẽ xem mỗi khả năng tái sử dụng như là một khối mã có tên trong kho lưu trữ, có thể thông qua tìm kiếm tương tự, có thể được kết hợp với các kỹ năng khác, và có thể thực hiện phản tinh luyện.

> **【拓展：Voyager 的技能库概念已被 2026 年的编码 Agent 普遍采用】**Các khóa học và hệ thống kỹ năng của Codex là những biến thể của ý tưởng này.

>  **【前置】**需要先掌握:Phase 14·05(Self-Refine/CRITIC) Voyager's"代提示机制"本质是Self-Refine + 环境反;Phase 14·07(MemGPT) 技能库的检索机制类似于档案记忆的语义搜索──还需要理解"代码即行动"的概念,区别于"文本即行动"

## Khái niệm cốt lõi

### Ba thành phần

Voyager (arXiv:2305.16291) cấu trúc một đại lý xung quanh:

> Voyager ((arXiv:2305.16291) bao quanh ba thành phần cấu trúc:

1. **Automatic curriculum.**Một người đề nghị do tò mò chọn nhiệm vụ tiếp theo dựa trên kỹ năng hiện tại của đại lý và tình trạng môi trường.
   Trung ngữ翻译:**自动课程。**Được biết, theo các thông tin của đại lý, họ đã chọn một nhiệm vụ tiếp theo.
2. **Skill library.**Mỗi kỹ năng là mã có thể thực hiện. Các kỹ năng mới được thêm vào khi một nhiệm vụ thành công.
   Trung ngữ翻译:**技能库。**Mỗi kỹ năng là có thể thực hiện mã hóa. Khi thành công trong nhiệm vụ, bạn có thể thêm kỹ năng mới.
3. **Iterative prompting mechanism.**Khi thất bại, đại lý nhận được lỗi thực thi, phản hồi môi trường, và đầu ra tự xác minh, sau đó tinh chỉnh kỹ năng.
   Trung ngữ翻译:**迭代提示机制。**Khi thất bại, đại lý nhận được thực hiện sai lầm, môi trường phản và tự kiểm tra xuất, sau đó tinh luyện kỹ năng.

Phân tích Minecraft (Wang et al., 2024): 3.3x các mặt hàng độc đáo hơn, 8.5x nhanh hơn công cụ đá, 6.4x nhanh hơn công cụ sắt, 2,3x dài hơn đường băng bản đồ so với đường cơ sở.

> Minecraft  đánh giá (((Wang 等人,2024):3.3 倍 nhiều hơn những thứ độc đáo  8,5 倍 nhanh hơn đồ dùng làm bằng đá  6,4 倍 nhanh hơn đồ dùng làm bằng sắt  2,3 倍 dài hơn trên toàn bộ địa hình đối với các tuyến đường.

### Không gian hành động = mã

Hầu hết các đại lý phát ra lệnh nguyên thủy. Voyager phát ra các chức năng JavaScript.

> Đại đa số Agent 发发原始命令──Voyager 发发 JavaScript 函数──一个技能是:

```
async function craftIronPickaxe(bot) {
  await mineIron(bot, 3);
  await mineStick(bot, 2);
  await placeCraftingTable(bot);
  await craft(bot, 'iron_pickaxe');
}
```

Được tạo thành từ các kỹ năng phụ, được lưu trữ bằng khóa mô tả và nhúng, được lấy lại như một chương trình, không phải là một lời nhắc.

> Từ các tập hợp kỹ năng và thành lập.

Đây là kỹ năng SDK của Claude Agent 2026: một phần mã có tên và có thể lấy lại cộng với các hướng dẫn mà đại lý tải theo yêu cầu.

> Đó là năm 2026 Claude Agent SDK: một mã có thể tìm kiếm được cộng với lệnh tải theo yêu cầu của Agent.

>  **【类比】**技能库像程序员的"代码片段库"或IDE的摘录:你不需要每次写Python都重新设计`read_file`函数,调用已有的就行;; 旅行者的洞察是让代理也这样做它"发明" một lần"挖铁矿"代码,存储进库,下次再要挖铁矿就直接检索调用;;**关键**: kỹ năng là**代码**Và không**提示词**代码 có thể được thực hiện trong môi trường, nhận được rõ ràng phản,提示词不行──

### Thu thập kỹ năng

Nhiệm vụ mới là "làm một cái đũa kim cương".

> 新任务"制作钻石"―Agent:

1. Nhúng mô tả nhiệm vụ.
   Trung ngữ翻译:嵌入任务描述──
2. Tìm kiếm các kỹ năng tương tự từ thư viện kỹ năng.
   Trung文翻译:查询技能库获取 top-k 相似技能──
3. Lấy lại `craftIronPickaxe`- `mineDiamond`- `placeCraftingTable`v.v.
   Trung ngữ翻译:检索 `craftIronPickaxe``mineDiamond``placeCraftingTable`Đúng vậy.
4. Sắp xếp kỹ năng mới từ nguyên thủy thu hồi + logic mới.
   Trung ngữ翻译: từ检索到的原语 + 新逻辑组合新技能──

Đây là mô hình thực hiện các nguồn lực MCP (Phase 13) và kỹ năng SDK của Agent: lấy lại trên một bề mặt kiến thức / mã, được quy mô cho nhiệm vụ hiện tại.

> Đây là MCP 资源 (Phase 13) và các kỹ năng SDK của Agent 实现的模式:在知识/代码表面上检索,限于当前任务――

### Phong lọc lặp đi lặp lại

Chuyện phản hồi của Voyager:

> Chuyển đổi của Voyager:

1. Trưởng văn viết một kỹ năng.
   Trung文翻译:Công viên 编写技能。
2. Kỹ năng chạy chống lại môi trường.
   Trung ngữ翻译:技能在环境中运行──
3. Một trong ba tín hiệu trở lại:`success`- `error`(với dấu vết đống),`self-verification failure`- Tôi không biết.
   Trung ngữ翻译:三种信号之一返回:`success``error`(带堆跟踪)`self-verification failure`
4. Trưởng văn sẽ viết lại kỹ năng bằng cách sử dụng tín hiệu như là ngữ cảnh.
   Trung文翻译:Công viên 使用信号作为上下文重写技能──
5. Lòng cho đến khi thành công hoặc vòng tối đa.
   Trung ngữ翻译: vòng tròn cho đến thành công hoặc đạt đến vòng lớn nhất.

Đây là tự tinh chỉnh (Dạy 05) được áp dụng cho việc tạo mã với xác minh dựa trên môi trường. CRITIC (Dạy 05) là mô hình tương tự với các công cụ bên ngoài như xác minh.

> ️ **【易错点】**Hãy đưa kỹ năng thất bại trực tiếp vào trong kho kỹ năng.**后果**: phiên bản cũ của công việc ban đầu bị mất, lần sau là phiên bản mới của lỗi.**一行修复**: skills库用版本化 key (khóa học kỹ năng dùng phiên bản hóa)`craft_pickaxe_v3`), thất bại时新增版本, không bao gồm phiên bản cũ; chỉ có tự xác minh 通过才标记为`latest`

> Đây là tự tinh chỉnh (第 5 课) được sử dụng để tạo mã của môi trường (环境) 定验证的代码生成;;Critic (第 5 课) là sử dụng các công cụ bên ngoài như một mô hình của các bộ chứng minh.

### Chương trình giảng dạy và khám phá

Các module chương trình giảng dạy của Voyager đề xuất các nhiệm vụ như "tạo một nơi trú ẩn gần hồ" dựa trên những gì mà người đại diện có và những gì nó chưa làm. Người đề xuất sử dụng tình trạng môi trường + hàng tồn kho kỹ năng để chọn một nhiệm vụ ngay trên khả năng hiện tại

> 🤔 **【困惑】**Q: "Kỹ năng của Voyager là JavaScript 代码" Tại sao không phải Python? Có Minecraft Mineflayer API  hạn chế không? A: 部分是──Mineflayer là Node.js 库, vì vậy mã phải là JavaScript── nhưng nguyên nhân sâu sắc hơn là:**代码作为动作空间必须可执行** ngôn ngữ không quan trọng, quan trọng là "can cannot be implemented directly by environment并返回成功/失败信号"──在浏览器中 Agent 里可能是Playwright TS 代码,在数据库中 Agent 里可能是 SQL──语言选型看环境,不在 Voyager 模式本身──

> Các mô-đun khóa học của Voyager dựa trên các tác vụ của Agent  đã có và chưa hoàn thành, chẳng hạn như "Xây dựng một nơi trú ẩn ở bờ hồ"                                                                                                                                                                                                                                            

Đối với các đại lý sản xuất điều này được dịch thành một nhà điều hành "điều gì thiếu": với thư viện kỹ năng hiện tại và một miền, chúng ta vẫn chưa bao gồm những kỹ năng nào?

> Đối với đại lý sản xuất, điều này chuyển thành một "vì thiếu" trình điều hành: cho các tài liệu và lĩnh vực kỹ năng hiện tại, chúng tôi chưa bao gồm những kỹ năng nào?

### Khi mô hình này đi sai

- **Skill library rot.**Một kỹ năng tương tự được thêm 10 lần với các mô tả khác nhau một chút.
  Trung ngữ翻译:**技能库腐化。**Cùng kỹ năng sử dụng mô tả khác nhau thêm 10 lần.
- **Composed-skill drift.**Nghệ năng của cha mẹ phụ thuộc vào một đứa trẻ được tinh chỉnh. Nghệ năng phiên bản; một cha mẹ bị gắn vào v1 không phép thuật nhận ra v3.
  Trung ngữ翻译:**组合技能漂移。**Những kỹ năng phụ thuộc vào kỹ năng cha được tinh chế.
- **Retrieval quality.**Việc lấy các vector trên mô tả kỹ năng giảm khi thư viện tăng lên hơn vài trăm.`category=tooling`").
  Trung ngữ翻译:**检索质量。**                                                                                                                                                                                                                                                              `category=tooling`"Sự kỹ năng"

## Hãy xây dựng nó.
```figure
voyager-skills
```

## Hãy xây dựng nó

`code/main.py`thực hiện thư viện kỹ năng stdlib:

> `code/main.py`Sử dụng tiêu chuẩn để thực hiện các kỹ năng:

- `Skill` tên, mô tả, mã (như chuỗi), phiên bản, thẻ, phụ thuộc.
  Trung ngữ翻译:`Skill`名称、描述、代码(字符串) 、版本、标签、依赖──
- `SkillLibrary` đăng ký, tìm kiếm (tốc hiệu chồng chéo), soạn (tốc độ topological) và tinh chỉnh (tiếng đập phiên bản khi cập nhật).
  Trung ngữ翻译:`SkillLibrary`注册、搜索(token 重叠)、组合(依赖的拓排序) 和精炼(更新时版本递增)
- Một nhân viên kịch bản ghi nhận ba kỹ năng nguyên thủy, sáng tác một thứ tư, đánh bại và tinh chỉnh.
  Trung ngữ翻译:注册三个原始技能、组合第四个、遇到失败并精炼的脚本 经纪人──

Đi đi.

> 运行:

```
python3 code/main.py
```

Hình ảnh cho thấy thư viện viết, tìm kiếm, sáng tác, một sự thực hiện thất bại, và một v2 tinh chỉnh vòng lặp cuối cùng của Voyager.

> 轨迹显示库写入,检索,组合,一次失败执行和 v2 精炼 Tại cuối vòng lặp của Voyager

## Hãy sử dụng nó để thực hiện

- **Claude Agent SDK skills**(Anthropic)  tài liệu tham khảo năm 2026: mỗi kỹ năng có mô tả, mã và hướng dẫn; được tải theo yêu cầu trong một phiên đại lý.
  Trung ngữ翻译:**Claude Agent SDK skills**(Anthropic) 2026 năm tham khảo: mỗi kỹ năng có mô tả ̊代码和指示; ̊Agent 会话中按需加载──
- **skillkit**(npm: skillkit)  Quản lý kỹ năng liên quan đến các nhân viên cho 32+ nhân viên mã hóa AI.
  Trung ngữ翻译:**skillkit**(npm: skillkit) 32+ AI 编码 Agent 的跨 Agent 技能管理。
- **Custom skill libraries** cụ thể về miền (nghệ năng SQL cho các đại lý dữ liệu, kỹ năng Terraform cho các đại lý ngoại tuyến).
  Trung ngữ翻译:**自定义技能库** lĩnh vực cụ thể DATA Agent  SQL 技能、基础设施 Agent  Terraform 技能)
- **OpenAI Agents SDK `tools`** ở cuối thấp; mỗi công cụ là một kỹ năng nhẹ.
  Trung ngữ翻译:**OpenAI Agents SDK `tools`**低端; mỗi công cụ là một kỹ năng hạng nhẹ.

## Chuyển nó đi.

`outputs/skill-skill-library.md`tạo ra một thư viện kỹ năng hình Voyager với đăng ký, lấy lại, phiên bản và tinh chỉnh được kết nối với bất kỳ thời gian chạy mục tiêu nào.

> `outputs/skill-skill-library.md`生成 Voyager 形状的技能库,内置注册,检查,版本化和精炼,适用于任何目标运行时――

## Tập luyện bài tập

1. Thêm một bộ dò chu kỳ phụ thuộc vào `compose()`Điều gì xảy ra khi kỹ năng A phụ thuộc vào B phụ thuộc vào A?
   Trung ngữ翻译:在 `compose()`Cần phải có một kỹ năng nào đó, một kỹ năng nào đó, một kỹ năng nào đó, một kỹ năng nào đó, một kỹ năng nào đó, một kỹ năng nào đó, một kỹ năng nào đó, một kỹ năng nào đó, một kỹ năng nào đó, một kỹ năng nào đó, một kỹ năng nào đó, một kỹ năng nào đó, một kỹ năng nào đó, một kỹ năng nào đó, một kỹ năng nào đó, một kỹ năng nào đó, một kỹ năng nào đó, một kỹ năng nào đó, một kỹ năng nào đó, một kỹ năng nào đó, một kỹ năng nào đó, một kỹ năng nào đó, một kỹ năng nào đó, một kỹ năng nào đó, một kỹ năng nào đó, một kỹ năng nào đó, một kỹ năng nào đó, một kỹ năng nào đó, một kỹ năng nào đó, một kỹ năng nào đó, một sự khác, một sự khác, một sự khác, một sự khác, một sự khác, một sự khác, một sự khác, một sự khác, một sự khác, một sự khác, một sự khác, một sự khác, một sự khác, một sự khác, một sự khác, một sự khác, một sự khác, một sự khác, một sự khác, một sự khác, một sự khác, một sự khác, một sự khác.
2. Thực hiện bản bản ghi kỹ năng mỗi khi một kỹ năng của cha mẹ tạo ra con`crafting@1`, một sự tinh tế cho `crafting@2`không được nâng cấp một cách im lặng.
   Trung文翻译:实现按技能版本固定──当父技能组合子技能 `crafting@1`时,`crafting@2`Chuyện tinh luyện không thể lặng lẽ nâng cấp kỹ năng của cha.
3. Thay thế lấy token-overlap bằng các embedment-transformers (hoặc một BM25 stdlib impl). đo lấy@5 trên một thư viện đồ chơi 50 kỹ năng.
   Trung文翻译:将代币 重叠检索替换为句子变换器 嵌入(或 BM25 标准库实现) ・・・ 在 50 技能玩具库上测量 retrieval@5。
4. Thêm một đại lý "các chương trình học": với thư viện hiện tại và mô tả miền, đề xuất 5 kỹ năng thiếu.
   Trung văn翻译:添加"课程"Công viên:给定当前库和领域描述, đề xuất 5 个缺失技能──每周调用一次──
5. Đọc tài liệu kỹ năng SDK của Claude Agent của Anthropic, chuyển thư viện đồ chơi sang kế hoạch kỹ năng SDK.
   Trung ngữ翻译:阅读Anthropic's Claude Agent SDK kỹ năng 文档――将玩具库移植为 SDK's skill 模式――可发现性有什么变化?

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Skill | "Reusable capability" / "可复用能力" | Named chunk of code + description, retrievable by similarity / 命名的代码块 + 描述，可按相似性检索 |
| Skill library | "Agent memory of how-to" / "Agent 的操作记忆" | Persistent store of skills, searchable and composable / 技能的持久化存储，可搜索可组合 |
| Curriculum | "Task proposer" / "任务提议器" | Bottom-up goal generator driven by current capability gap / 由当前能力差距驱动的自底向上目标生成器 |
| Composition | "Skill DAG" / "技能 DAG" | Skills invoking skills; topologically sorted on execution / 技能调用技能；执行时拓扑排序 |
| Iterative refinement | "Self-correcting loop" / "自我纠错循环" | Env feedback + errors + self-verification fold back into the next version / 环境反馈+错误+自我验证反馈到下一版本 |
| Action-space-as-code | "Programmatic actions" / "编程式动作" | Emit functions, not primitive commands, for temporally extended behavior / 发出函数而非原始命令，用于时间扩展行为 |
| Dedup on write | "Skill collapse" / "技能合并" | Near-duplicate descriptions collapse to one canonical skill / 近似重复描述合并为一个规范技能 |

## Xem thêm 延伸阅读

- [Wang et al., Voyager (arXiv:2305.16291)](https://arxiv.org/abs/2305.16291) giấy sách thư viện kỹ năng gốc
  Trung ngữ翻译:Voyager 原始技能库论文──
- [Claude Agent SDK overview](https://platform.claude.com/docs/en/agent-sdk/overview) các kỹ năng như sản xuất năm 2026
  Trung文翻译:Claude Agent SDK 概览2026 年产品化技能──
- [Anthropic, Building agents with the Claude Agent SDK](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk) kỹ năng và các yếu tố phụ trong thực tế
  Trung文翻译:Anthropic 关于使用Claude Agent SDK 构建 Agent 的文章实践中的技能和子代理──
- [Madaan et al., Self-Refine (arXiv:2303.17651)](https://arxiv.org/abs/2303.17651) vòng lọc bên dưới Voyager
  Trung文翻译:Tự tinh chỉnh 论文Thiếu khách 底层的精炼循环──
