# Kỹ năng đại lý: Hợp đồng di động và giới hạn thời gian chạy

> Một kỹ năng không phải là một lời nhắc dài với tên tệp tốt hơn. Nó là một gói hướng dẫn, tài nguyên và trợ lý thực thi được tìm thấy mà nhập vào bối cảnh của một đại lý thông qua một hợp đồng thời gian chạy.

> **【中文解读】**Một kỹ năng không phải là "hãy thay đổi tên tài liệu tốt" mà là một gói chỉ dẫn, tài nguyên tham khảo và trợ lý thực thi được tìm thấy trong cuốn sách.

> **【拓展：Skill 生态的 2026 版图】**Một mô hình của Agent Skills đã được phát triển từ Anthropic để mở rộng quy tắc: Claude Code、Codex và các nhà cung cấp đều hỗ trợ theo danh sách phát hiện SKILL.md và tiết lộ nguồn lực của nó;`npx skills`Các thiết bị này có thể đưa kỹ năng trong khóa học vào chủ nhà bất kỳ. Một phần của các quan điểm khác nhau: MCP quản lý có những khả năng nào có thể điều chỉnh được.

>  **【前置】**Học本课前请先掌握:(1) giai đoạn 13 · 01(工具接口) 技能与工具的正交关系从这里来;(2) giai đoạn 13 · 05(工具 Schema 设计) 类型化输入输出是 MCP 工具的职责边界;(3) 了解YAML 面议的基本语法──本课是23 课毕业项目(打包层) 和24-27 课 技能 生命周期各阶段) 的地基──

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib) | **语言:** Python（标准库）
**Prerequisites:** Phase 13 · 01 (The Tool Interface), Phase 13 · 05 (Tool Schema Design) | **前置知识:** Phase 13 · 01（工具接口）、Phase 13 · 05（工具 Schema 设计）
**Time:** ~90 minutes | **时间:** 约 90 分钟

## Mục tiêu học tập

- Định nghĩa kỹ năng đại lý mà không nhầm lẫn nó với một lệnh, hướng dẫn kho, công cụ, móc, subagent, hoặc plugin.
  Trung文翻译:给出 代表技能的定义,不与提示词、仓库说明、工具、hook、subagen或插件混──
- Đọc trên điện thoại di động `SKILL.md`hợp đồng và tách nó khỏi các gia hạn cụ thể về thời gian chạy.
  Trung ngữ翻译:读懂可移植的`SKILL.md`契约,并把它与运行专属扩展区分开来.
- Giải thích khám phá, lựa chọn, kích hoạt, tải tài nguyên, sử dụng công cụ và xác minh như các giai đoạn vòng đời riêng biệt.
  Trung ngữ翻译:把发现,选择,激活,资源载荷,工具使用和验证解释为彼此独立的生命周期阶段──
- Thêm vào danh sách của một đại lý.
  Trung ngữ翻译: Trong vận hành đưa kỹ năng 包放进 Agent 目录之前先验证它。
- Chọn giữa một kỹ năng, công cụ MCP, móc, subagent, hoặc mã thông thường cho một nhiệm vụ cụ thể.
  Trung文翻译: Để một nhiệm vụ cụ thể trong kỹ năng, MCP 工具, hook, subagent hoặc普通代码之间做出选择.

## 10 phút thành công đầu tiên. 10 phút thắng đầu tiên.

> **【中文解读】**Trước khi bắt đầu, bạn sẽ tạo ra một kỹ năng nhỏ nhất.`npx skills add`Hãy đưa bài học này kỹ năng- hợp đồng-bảo sát viên  hoàn toàn cài đặt vào thực sự Trưởng lý  chủ nhà, hiển nhiên调用 nó kiểm tra kỹ năng của bạn 再探测隐式选择,最后干净卸载── thực sự chủ nhà kiểm tra điểm cần Node.js,`npx`、Python 3 和一个支持技能的宿主;条件不满足时退回手工打包练习契约能学到, nhưng chủ nhà phát hiện ra và hành vi gỡ bỏ chỉ có thể được đánh dấu là " chưa được chứng minh".

Làm điều này trước khi giải thích dài. Bạn sẽ tạo ra một kỹ năng nhỏ, cài đặt
bộ phận kiểm tra viên hoàn chỉnh được kết hợp thành một máy chủ thực sự, gọi nó, xác minh
kết quả, và loại bỏ nó. Điều này chứng minh chu kỳ cuộc sống với một kết quả có thể quan sát được.

> Trước khi đọc bài viết này, hãy làm điều này. Bạn sẽ tạo ra một kỹ năng nhỏ, đưa một nhà phê bình hoàn chỉnh  gói cài đặt vào thực sự Agent  chủ nhà, điều chỉnh nó, xác minh kết quả, tái di chuyển nó.

### Chuyến bay trước khi đến phòng thí nghiệm chủ nhà thực tế

Điểm kiểm soát host thực sự yêu cầu Node.js, `npx`, Python 3, một chọn
có khả năng quản lý, và viết quyền truy cập vào dự án hoặc phạm vi người dùng bạn chọn trong
Đầu tiên kiểm tra lệnh địa phương:

> Đúng là cần Node.js`npx`、Python 3、 một chủ sở hữu hỗ trợ kỹ năng được chọn, cũng như quyền viết cho phạm vi cấp dự án hoặc cấp người dùng bạn chọn trong bộ cài đặt:

```bash
node --version
npx --version
python3 --version
```

Quyết định bạn sẽ sử dụng máy chủ và phạm vi nào trước khi cài đặt.
yêu cầu không có sẵn, đọc bài học này trên trang web hoặc tiếp tục với
tập tập gói thủ công dưới đây.
không chứng minh phát hiện host, gọi, thực hiện bản ghi âm gói, hoặc
Tháo bỏ hành vi cài đặt.

> Nếu bất kỳ điều kiện nào không được đáp ứng, bạn có thể đọc bài học này trên trang web, hoặc tiếp tục thực hành gói tay sau đây.

### 1. Bắt đầu trong thư mục làm việc trống

Thực hiện các lệnh này từ bất kỳ thư mục phụ huynh nào mà bạn tiếp tục học làm việc:

> Trong thư mục bất kỳ của bạn lưu trữ học tập làm việc:

```bash
mkdir -p agent-skills-first-run
cd agent-skills-first-run
TARGET_ROOT="$(pwd -P)"
printf 'TARGET_ROOT=%s\n' "$TARGET_ROOT"
ls -A
```

Chỉ thị cuối cùng không nên in gì. Nếu nó in các tệp, hãy chọn một tệp khác
thư mục trống để đánh giá có một ranh giới rõ ràng.

> Một lệnh cuối cùng không được xuất bản. Nếu nó in ra tài liệu, thay đổi một danh mục không gian khác, để kiểm tra có ranh giới rõ ràng.

Tạo thư mục cho kỹ năng đầu tiên của bạn:

> Để có kỹ năng đầu tiên của bạn  tạo danh mục:

```bash
mkdir -p my-first-skill
```

Tạo ra`my-first-skill/SKILL.md`với nội dung này:

> 用以下内容创建 `my-first-skill/SKILL.md`- Có thể là:

```markdown
---
name: my-first-skill
description: Turn rough meeting notes into a compact decision record when the user asks to capture a technical decision.
---

# Decision record

Extract the decision, context, alternatives, owner, and next review date.
If the notes do not contain a decision, ask one clarifying question instead
of inventing one.
```

Kiểm tra rằng bạn đã tạo file trong thư mục dự định:

> 验证 bạn đã tạo tài liệu trong thư mục dự kiến:

```bash
test -f my-first-skill/SKILL.md
```

Không có mã phát và thoát 0 có nghĩa là tập tin tồn tại.

> 无输出和退出码为 0 即文件存在──

### 2. Thiết lập gói kiểm tra viên đầy đủ

- Cứ ở lại.`agent-skills-first-run`và chạy:

>  dừng lại `agent-skills-first-run`Và hành động:

```bash
npx skills add rohitg00/ai-engineering-from-scratch --skill skill-contract-reviewer --full-depth
```

Chọn máy chủ đại lý và phạm vi bạn đang sử dụng.
`skill-contract-reviewer`Và điểm đến mà nó viết.`--full-depth`là
cần thiết bởi vì kỹ năng của bài học này là một gói tổ hợp với tham chiếu, một
kịch bản, và một tài sản.

> 选择您在使用的代理 宿主和范围──安装器应列出 `skill-contract-reviewer`及其写入目的地──`--full-depth`Đó là điều cần thiết, bởi vì kỹ năng của bài học này là một gói chứa tài liệu tham khảo, kịch bản và tài sản.

Đặt `SKILL_ROOT`cho thư mục tuyệt đối được báo cáo bởi người cài đặt.
là thư mục chứa các cài đặt `SKILL.md`, không phải nguồn bài học
thư mục và không phải không gian làm việc hiện tại:

> - Đưa đi.`SKILL_ROOT`设为安装器报告的绝对目录―― nó phải được chứa đã được cài đặt `SKILL.md`Đăng ký, không phải là danh mục nguồn của chương trình, cũng không phải là hiện tại:

```bash
# Replace the placeholder with the destination printed by the installer.
SKILL_ROOT="$(cd "/absolute/path/to/skill-contract-reviewer" && pwd -P)"
test -f "$SKILL_ROOT/SKILL.md"
printf 'SKILL_ROOT=%s\n' "$SKILL_ROOT"
```

Nếu phiên đại lý đã mở, bắt đầu phiên mới hoặc sử dụng phiên chủ nhà đó
Đừng cho rằng mỗi máy chủ tải lại danh mục của nó.

> Nếu cuộc họp của đại lý đã mở, hãy mở cuộc họp mới hoặc sử dụng kỹ năng của chủ nhà để tái quét lệnh. Đừng giả định mỗi chủ nhà sẽ tải lại danh sách của nó.

### 3. Hãy gọi nó rõ ràng.

Trong đại lý được cài đặt, với `agent-skills-first-run`làm việc
thư mục, sử dụng cú pháp được hỗ trợ bởi máy chủ đó:

> Trong một đại lý đã được lắp đặt,`agent-skills-first-run`Để làm việc, sử dụng ngôn ngữ của chủ nhà:

| Host | Explicit invocation |
|---|---|
| Codex | `skill-contract-reviewer`, or choose it from `/skills`, then provide the review request |
| Claude Code | `/skill-contract-reviewer` followed by the review request |
| Portable fallback | `Use skill-contract-reviewer to review the target package.` |

Sử dụng các giá trị tuyệt đối được in cho `SKILL_ROOT`và `TARGET_ROOT`trong
yêu cầu. yêu cầu chủ sở hữu để mở rộng chúng trước khi thực hiện và hiển thị chính xác
lệnh giải quyết, không phải lệnh phụ thuộc vào thư mục hoạt động của quy trình:

> Trong yêu cầu sử dụng in ấn ra `SKILL_ROOT`Với`TARGET_ROOT`绝对值── yêu cầu chủ nhà mở chúng trước khi thực hiện,并 hiển thị lệnh xác định sau khi phân tích, thay vì phụ thuộc vào lệnh của danh mục công việc của quy trình:

```text
Use skill-contract-reviewer to review <TARGET_ROOT>/my-first-skill. The installed bundle root is <SKILL_ROOT>. Run python3 <SKILL_ROOT>/scripts/check_skill.py <TARGET_ROOT>/my-first-skill. Before running it, show the fully resolved argv. Return the validation report, selected primitives, and one sentence for each selection. Include the resolved script path, resolved target path, cwd, argv, and exit code as execution evidence.
```

Chỉ thị được giải quyết nên có hình dạng này, không còn vị trí nào:

> 解析后的命令应呈这种形态,不留任何占位符:

```bash
python3 "/absolute/install/path/skill-contract-reviewer/scripts/check_skill.py" \
  "/absolute/workspace/path/agent-skills-first-run/my-first-skill"
```

Kết quả thành công có cả ba tính chất:

> Kết quả thành công có 3 tính chất:

1. Người chủ nhà tìm thấy `skill-contract-reviewer`bằng tên.
  Trung文翻译:宿主按名称找到 `skill-contract-reviewer`
2. Người xem đọc hợp đồng gói và chạy bộ xác thực gói của nó.
  Trung文翻译:reviewer 读取包契约并运行其捆绑的验证器。
3. Phản ứng chứa một báo cáo xác thực mà không có lỗi cấu trúc cho các
   mẫu, cộng với một lựa chọn nguyên thủy hợp lý.
  Trung ngữ翻译:响应包含一个无结构性错误的验证报告 (nói theo ví dụ),以及有依据的原语选择──

Bằng chứng thực hiện cũng phải nêu tên đường kịch bản, đường mục tiêu, cwd, chính xác
Các đối tượng đối số và mã thoát.
chứng minh rằng văn bản bạn bè được cài đặt đã chạy.

> 执行证据还必须写明脚本路径、目标路径、cwd、精确参数向量和退出码──缺失这些字段的流报告证明没有安装的伴随脚本真的运行──

Nếu máy chủ báo cáo rằng kỹ năng không có sẵn, kiểm tra cài đặt
mục đích, quét lại hoặc khởi động lại một lần, và thử lại yêu cầu rõ ràng.
viết lại mô tả kỹ năng để che giấu sự cố cài đặt.

> Nếu chủ nhà báo kỹ năng không cần thiết, trước tiên kiểm tra mục đích cài đặt, quét lại hoặc khởi động lại một lần nữa, thử lại một lần nữa.

### 4. Việc chọn lọc ngầm của các con thám

Bắt đầu một lượt đại lý mới và nhập vào cùng một nhiệm vụ mà không đặt tên kỹ năng:

>  Open a whole new Agent 轮次, nhập vào cùng nhiệm vụ nhưng không chỉ huy kỹ năng:

```text
Review <TARGET_ROOT>/my-first-skill as a reusable agent package and tell me whether its package contract is valid.
```

Nếu chủ nhà cho thấy những kỹ năng đã chọn, ghi lại xem họ đã chọn hay không
`skill-contract-reviewer`Nếu chủ không tiết lộ đường dẫn, đánh dấu ngầm
Sự gọi rõ ràng là sự quay lại di động.

> Nếu chủ nhà cho thấy kỹ năng của mình, ghi lại xem nó đã chọn hay không.`skill-contract-reviewer`Nếu chủ nhà không tiết lộ đường, hãy đặt dấu chọn ẩn cho chưa được chứng minh.

### 5. Làm sạch

Chỉ xóa gói kiểm tra được cài đặt:

> Chỉ di chuyển đã được cài đặt của reviewers 包:

```bash
npx skills remove skill-contract-reviewer
```

Chọn cùng một máy chủ và phạm vi sử dụng trong quá trình cài đặt. Sau khi quét lại hoặc mới
phiên, một yêu cầu rõ ràng cho `skill-contract-reviewer`nên báo cáo rằng
Không có sẵn.`my-first-skill`cho các bài học sau đó, hoặc loại bỏ
Đồ sơ của phòng thí nghiệm sau khi bạn hoàn thành đường đua.

> 选择与安装时相同的主机和范围──重新扫描或新会话后,对 `skill-contract-reviewer`                                                                                                                                                                                                                                                              `my-first-skill`给后续课程,或在学完本轨 后删掉实验目录──

## Vấn đề  vấn đề giới thiệu

> **【中文解读】** Có hai hướng sai lầm: đưa dòng công việc vào một gợi ý từ  không có căn tính ổn định, không tìm thấy quy tắc, không có biên giới tài nguyên, không có hình dạng gói có thể kiểm tra; hoặc ngược lại, đưa mọi chỉ thị có thể lặp lại như là kỹ năng                                                                                                                                                                                                                               

Giả sử nhóm của bạn có một dòng công việc phát hành đáng tin cậy. Nó tìm thấy các thay đổi được sáp nhập, kiểm tra các ghi chú di chuyển, cập nhật nhật nhật ký thay đổi, chạy lệnh đóng gói và tạo danh sách kiểm tra xem xét.

> 假设 nhóm của bạn có một dòng công việc đáng tin cậy: tìm hợp并变更; kiểm tra chuyển động说明; cập nhật nhật nhật ký thay đổi; chạy lệnh đóng gói; sản xuất kiểm tra đơn giản.

Đặt dòng công việc đó vào một lệnh nhắc nhở làm cho nó dễ dàng dán và khó vận hành. Chỉ dẫn nhắc nhở không có danh tính ổn định, không có quy tắc phát hiện, không có giới hạn tài nguyên, không có hình dạng gói kiểm tra, và không có câu trả lời cho các câu hỏi cơ bản: Ai có thể gọi nó?

> Đặt bài viết này vào một câu hỏi: người nào có thể sử dụng nó? mô hình nên chọn vào lúc nào? nó có thể chạy được trong các kịch bản nào? những tài liệu nào đáng tin cậy?

Sai lầm ngược lại là xem mọi hướng dẫn tái sử dụng như một kỹ năng.`SKILL.md`tạo ra một thư mục trông dễ di chuyển trong khi phụ thuộc vào hành vi không được ghi chép của một máy chủ.

> Thay vào đó, sai lầm là đưa mỗi lệnh có thể sử dụng được như là một kỹ năng.`SKILL.md`Sẽ có một cái nhìn giống như có thể chuyển, thực tế phụ thuộc vào một danh sách hành vi không được ghi chép của chủ nhà.

Nhiệm vụ kỹ thuật đầu tiên là phân loại, quyết định đồ tạo vật là gì trước khi bạn quyết định cách đóng gói nó.

> Nhiệm vụ đầu tiên là phân loại. Trước tiên quyết định công trình là gì, sau đó quyết định lại làm thế nào để đóng gói.

## Khái niệm cốt lõi

### Kỹ năng mã hóa kiến thức thủ tục

Một kỹ năng đại lý là một thư mục mà điểm nhập là`SKILL.md`.Tệp nhập chứa vật liệu trước của YAML theo sau là hướng dẫn Markdown. Thư mục cũng có thể chứa tham chiếu, kịch bản và tài sản.

> Kỹ năng đại lý là một trong những`SKILL.md`Đối với danh mục nhập,... danh mục nhập bao gồm các nguyên nhân của YAML và các chỉ thị đánh dấu tiếp theo.

```figure
skill-package-anatomy
```

Thư mục, không chỉ là tập tin Markdown, là đơn vị có thể triển khai.`SKILL.md`với các tham chiếu thiếu là một gói bị hỏng ngay cả khi vật liệu phía trước của nó phân tích.

> Có thể triển khai đơn vị là danh mục, không chỉ là một tập tin đánh dấu.`SKILL.md`Nếu thiếu tài nguyên mà nó trích dẫn, ngay cả vấn đề đầu tiên cũng có thể giải quyết một gói xấu.

### Các bản trừu tượng lân cận

| Artifact | Primary job | Loaded or run when | What it should not impersonate |
|---|---|---|---|
| Prompt | Shape one model interaction | Included by an application or user | A versioned package with resources |
| Repository instructions | Explain one codebase's standing rules | A coding runtime enters that scope | A reusable task workflow |
| Agent skill | Supply reusable procedural knowledge | Explicit or implicit activation | A hard authorization boundary |
| MCP tool | Expose a typed remote capability | The model or application calls it | A detailed operating procedure |
| Hook | Run deterministic logic on an event | The declared event occurs | Probabilistic model routing |
| Subagent | Delegate work with separate context and state | An orchestrator creates or calls it | A static instruction bundle |
| Plugin | Distribute a larger runtime extension | The host installs or enables it | The portable skill contract itself |
| Learned skill library | Store behavior discovered through experience | A policy retrieves a prior program or trajectory | A standards-based `SKILL.md` package |

Một kỹ năng phát hành có thể cho đại lý biết cách kiểm tra một bản phát hành. Một máy chủ MCP có thể phơi bày sổ đăng ký phát hành. Một cái móng có thể cấm đẩy trực tiếp. Một người phụ có thể kiểm tra độc lập ứng cử viên. Những mảnh này được tạo nên bởi vì chúng giữ trách nhiệm khác nhau.

> Một kỹ năng phát hành có thể nói với đại lý cách kiểm tra phát hành; một máy chủ MCP có thể phát hiện ra đăng ký; một cái móng có thể cấm đẩy trực tiếp; một bộ phận có thể độc lập kiểm toán ứng cử phiên bản.

### Từ "khả năng" đặt tên cho hai ý tưởng khác nhau

> **【中文解读】**Từ "khả năng" có nghĩa là hai điều khác nhau: trong hệ thống nghiên cứu nó có nghĩa là các quy trình học được, quỹ đạo thành công hoặc đoạn chiến lược.

Các hệ thống nghiên cứu đôi khi gọi một chương trình học, quỹ đạo thành công hoặc phân đoạn chính sách cụ thể về môi trường là một kỹ năng. Một đại lý có thể tạo ra những hiện vật này trong quá trình khám phá, lấy lại chúng theo tương tự nhiệm vụ, thực hiện chúng và sửa đổi thư viện từ phản hồi.

> Các hệ thống nghiên cứu đôi khi gọi các quy trình học được, đường mòn thành công hoặc các chiến lược cụ thể về môi trường là kỹ năng. Các đại lý có thể tạo ra các công cụ này trong quá trình khám phá, tìm kiếm và thực hiện chúng theo nhiệm vụ, và xây dựng theo cơ sở sửa đổi.

Một kỹ năng đại lý trong mini-track này khác. Nó là một gói tác giả với một hợp đồng hệ thống tập tin được tuyên bố, siêu dữ liệu danh mục, tiết lộ tiến bộ, cuộc gọi trung gian thời gian chạy và các công cụ được kiểm soát bởi máy chủ. Nó có thể được tạo hoặc cải thiện bởi một đại lý, nhưng không cần học tập cho định dạng.

> Trong mini-track này, Agent Skill không khác. Nó là một gói được tạo ra, với các bản tuyên bố, hệ thống tài liệu, các bản mục dữ liệu, trình bày tiến bộ, việc điều chỉnh giữa thời gian vận hành và các công cụ quản lý của chủ nhà. Nó có thể được tạo ra hoặc cải tiến bởi Agent, nhưng các định dạng tự nó không yêu cầu học.

| Dimension | Agent Skill package | Learned skill library |
|---|---|---|
| Primary unit | `SKILL.md` directory | Program, policy, trajectory, or memory record |
| Creation | Authored, generated, or curated | Usually discovered from environment experience |
| Selection | Catalog description plus runtime policy | Retrieval or policy over task state |
| Execution | Model follows instructions and calls host tools | Environment runs a stored behavior or code artifact |
| Portability | Package contract can cross compatible hosts | Often tied to one environment and action space |
| Evaluation | Routing, artifact, safety, and host compatibility | Reward, success rate, transfer, and library growth |

Cả hai ý tưởng đều bao gồm năng lực tái sử dụng.

> Hai ý tưởng đều có khả năng tái sử dụng được. Nhưng không nên chỉ là vì cùng tên.

### Lái lõi di động

> **【中文解读】**可移植核心极小:`name`(nói định danh, phải đáp ứng quy tắc đặt tên và phù hợp với danh mục của cha) và `description`(Tất cả là tài liệu và là đường dẫn của dữ liệu, để nói rõ kỹ năng làm gì, khi nào áp dụng) hai phần trước là quy tắc cần phải được lấp đầy;`license``compatibility``metadata`là một phần có thể chọn,`allowed-tools`属实验性、宿主支持不一──Markdown 正文承载操作指令工作流、决策点、失败行为和通往支资源的直通路径──

Các kỹ năng đặc biệt của Agent Skills yêu cầu hai trường chủ yếu:

> Kỹ năng đại lý 规范要求两个主题 字段:

```yaml
---
name: release-readiness
description: Inspect a release candidate when the user asks whether a version is ready to publish.
---
```

`name`là định danh ổn định. Nó phải đáp ứng các quy tắc đặt tên của đặc điểm và phù hợp với thư mục gốc. `description`là cả tài liệu và định tuyến metadata. Nó nên nói những gì kỹ năng làm và khi nào nó áp dụng.

> `name`là một biểu tượng cố định, phải đáp ứng quy tắc của quy tắc đặt tên và phù hợp với danh mục của cha.`description`既是文档也是路由元数据,应说明 kỹ năng làm gì,何时适用.

Các trường tùy chọn di động là:

> 可移植的可选字段有:

| Field | Purpose | Portability note |
|---|---|---|
| `license` | State the terms for the package | Core specification |
| `compatibility` | State environmental requirements | Core specification |
| `metadata` | Carry string-valued extension data | Core specification |
| `allowed-tools` | Suggest pre-approved tools | Experimental; host support varies |

Cơ quan Markdown nắm giữ các hướng dẫn hoạt động. Nó nên xác định dòng công việc, các điểm quyết định, hành vi thất bại và các con đường trực tiếp đến các nguồn hỗ trợ.

> Markdown chính thức được viết trong lệnh hoạt động. Nó nên xác định dòng chảy làm việc, điểm quyết định, hành vi thất bại và đường dẫn trực tiếp của tài nguyên.

```markdown
# Release readiness

Use this workflow for a release candidate, not for ordinary development builds.

1. Read `references/release-policy.md`.
2. Run `python3 scripts/inspect_release.py --format json`.
3. Stop if the report contains a blocking failure.
4. Produce the checklist from `assets/release-checklist.md`.
5. Ask for approval before any publish or tag action.
```

### Các phần mở rộng thời gian chạy là một lớp thứ hai

Một số máy chủ chấp nhận cấu hình frontmatter hoặc đồng hành bổ sung. Những trường đó có thể hữu ích, nhưng chúng không tự động di động.

> Một số chủ nhà chấp nhận thêm vật liệu mặt trước hoặc việc sử dụng.

| Behavior | Example host extension | Portable core? |
|---|---|:---:|
| Hide a skill from model routing while keeping direct user invocation | `disable-model-invocation` | No |
| Hide a skill from the user's command menu while allowing model routing | `user-invocable` | No |
| Show argument help in a command menu | `argument-hint` | No |
| Run the skill in delegated context | `context`, `agent` | No |
| Pin model or reasoning settings | `model`, `effort` | No |
| Register lifecycle automation | `hooks` | No |
| Disable implicit invocation in Codex | `agents/openai.yaml` policy | No |

Hãy coi mỗi phần mở rộng như một bộ điều chỉnh. Giữ dòng công việc cốt lõi hợp lệ mà không cần nó, ghi lại sự vấp phải và kiểm tra máy chủ chủ tiêu thụ nó. Một thời gian chạy có thể bỏ qua một trường không rõ, từ chối nó hoặc bảo tồn nó mà không thực hiện hành vi.

> Đặt mỗi mở rộng như một bộ thích ứng: không có hệ thống làm việc cốt lõi của nó cũng phải giữ hiệu quả, ghi lại cách quay lại,并 kiểm tra tiêu thụ chủ sở hữu của nó.

### Frontmatter là metadata có thể thực hiện

Metadata thay đổi hành vi của hệ thống trước khi cơ thể kỹ năng được đọc.

> 元データ在技能 正文被读之前就改变系统行为──

- Một người bị hư hỏng`name`có thể khiến khám phá thất bại.
  Trung ngữ翻译:格式错误的 `name`Để tôi thấy thất bại.
- Một sự mơ hồ`description`có thể định tuyến các yêu cầu sai.
  Trung ngữ翻译:含糊的 `description`会路源错误的请求――
- Một lá cờ chỉ dành cho con người có thể loại bỏ kỹ năng từ danh mục của mô hình.
  Trung ngữ翻译:一个"仅人类"标志能把技能从模型目录中移除──
- Một khoản trợ cấp công cụ có thể thay đổi liệu chủ nhà có yêu cầu cho phép hay không.
  Trung文翻译:工具许可能改变宿主是否请求授权──
- Một cài đặt ngữ cảnh có thể di chuyển thực thi vào một phiên đặc vụ riêng biệt.
  Trung văn翻译:上下文设置能把执行移 into独立的代理会话──

Xem xét mặt vật chất như mã cấu hình, xác nhận nó, phiên bản nó, và bao gồm hành vi của nó trong các đánh giá.

> 像审查配置代码一样审查前面:验证它、给它做版本管理,并把它的行为纳入评测──

### Chuyển vòng đời kỹ năng

> **【中文解读】**八阶段生命周期:发现(在配置位置找候选包)→ 验证(目录发布前拒形或不安全的包)→ 编目(只暴露精简的名称+描述)→ 选择(判断相关性)→ 激活(把正文载入模型可见上下文)→ 披露(仅需要某分支时才读参考/资产)→ 执行(在宿主权限和隔离规则下使用主工具)→ 验证宿宿(独立于模型的声明检查产品)。把这些阶段压会导致误解心智模型:被发现的技能不等于已被发现的技能;已激活的技能不等于被授权做它的描述;所有被允许的工具调用不等于正确结果.

```figure
skill-runtime-lifecycle
```

Mỗi mũi tên là một ranh giới với chế độ thất bại riêng của nó.

> Mỗi mũi tên đều là một biên giới với mô hình cố định của riêng mình.

1. **Discovery**tìm thấy các gói có thể ở các vị trí được cấu hình.
  Trung ngữ翻译:**发现**Trong vị trí của vị trí tìm kiếm có thể của gói.
2. **Validation**từ chối các gói bị biến dạng hoặc không an toàn trước khi xuất bản danh mục.
  Trung ngữ翻译:**验证**Trong danh mục trước khi xuất bản từ chối 形或不安全包──
3. **Cataloging**phơi bày một hợp lý `name`và `description`, không phải toàn bộ gói.
  Trung ngữ翻译:**编目**Chỉ tiết lộ`name`和 `description`, không hoàn toàn.
4. **Selection**quyết định liệu kỹ năng có liên quan hay không.
  Trung ngữ翻译:**选择**quyết định kỹ năng hay không liên quan.
5. **Activation**tải cơ thể vào bối cảnh hình ảnh hình ảnh.
  Trung ngữ翻译:**激活**Đặt văn bản chính xác vào mô hình có thể nhìn thấy trên văn bản bên dưới.
6. **Disclosure**đọc tài sản hoặc tài sản chỉ khi một chi nhánh yêu cầu chúng.
  Trung ngữ翻译:**披露**Chỉ cần đọc tài sản hoặc tài sản khi cần một phần nào đó.
7. **Execution**sử dụng các công cụ chủ dưới sự cho phép và quy tắc cô lập của chủ.
  Trung ngữ翻译:**执行**Trong quy tắc quyền hạn và cách ly sử dụng công cụ của chủ nhà.
8. **Verification**kiểm tra các tác phẩm tạo ra độc lập với yêu cầu của mô hình.
  Trung ngữ翻译:**验证**独立于模型的声明检查产品

Sự sụp đổ của các giai đoạn này gây ra mô hình tâm lý xấu. Một kỹ năng được phát hiện không hoạt động. Một kỹ năng hoạt động không được phép làm tất cả những gì nó mô tả.

> Việc áp lực những giai đoạn này sẽ gây ra mô hình tâm trí tồi tệ: kỹ năng được phát hiện không được kích hoạt; kỹ năng được kích hoạt không được ủy quyền làm mọi thứ nó mô tả; việc sử dụng các công cụ được phép không chứng minh kết quả chính xác.

### Kỹ năng và công cụ là orthogonal

MCP trả lời, "Các khả năng nào mà ứng dụng này có thể yêu cầu, và những kế hoạch của họ là gì?" Một kỹ năng trả lời, "Làm thế nào một đại lý nên tiếp cận lớp này của nhiệm vụ?"

> MCP trả lời "nhiều ứng dụng này có thể điều chỉnh những khả năng nào; kế hoạch của chúng là gì"; kỹ năng trả lời "Nhà viên nên làm thế nào để thực hiện loại nhiệm vụ này"

```figure
skill-tool-orthogonality
```

Kỹ năng có thể đặt tên cho một công cụ, nhưng chủ sở hữu danh sách khả năng thực tế. Nếu công cụ không có, kỹ năng nên báo cáo một sự thất bại hoặc thất bại rõ ràng.

> Kỹ năng có thể đặt tên cho một công cụ, nhưng thực sự có khả năng đăng ký trở lại chủ sở hữu. Nếu công cụ bị thiếu, kỹ năng phải tuyên bố trở lại hoặc thất bại, chắc chắn không thể chỉ ra " đặt tên cho một khả năng đã tạo ra nó".

### Kỹ năng và hướng dẫn lưu trữ là phạm vi khác nhau

Các hướng dẫn kho chứa mô tả môi trường bạn đã ở: lệnh, quy ước, các tệp được tạo và ranh giới. Một kỹ năng cung cấp quy trình có thể được sử dụng nhiều lần cho một nhiệm vụ có thể xảy ra trên nhiều kho chứa.

> 仓库说明 mô tả môi trường bạn đã ở trong đó: lệnh, định, tạo tài liệu và biên giới; kỹ năng để cung cấp một quy trình có thể được sử dụng cho một nhiệm vụ có thể xuất hiện trên nhiều kho chứa.

Khi cả hai áp dụng, yêu cầu người dùng hoạt động và các quy tắc kho hạn chế kỹ năng. Một kỹ năng tái tạo chung không được bỏ qua một quy tắc kho cấm chỉnh sửa các tệp được tạo.

> Khi hai thứ này được áp dụng cùng lúc, yêu cầu của người dùng hiện tại và quy tắc kho bị ràng buộc kỹ năng. Một kỹ năng xây dựng lại chung không phải vượt qua các quy tắc kho của "đấu chế tạo tài liệu bị cấm".

### Kỹ năng không nhập khẩu lẫn nhau

Một kỹ năng có thể hướng dẫn người đại lý gọi một kỹ năng khác, nhưng đây không phải là nhập khẩu ở cấp độ ngôn ngữ. kỹ năng thứ hai vẫn đi qua phát hiện thời gian chạy, đủ điều kiện, kích hoạt, quyền và xử lý ngữ cảnh.

> Một kỹ năng có thể dẫn người đại lý đến một kỹ năng khác, nhưng đây không phải là một kỹ năng nhập khẩu bằng ngôn ngữ.

Viết các phụ thuộc qua kỹ năng như các cạnh luồng công việc có thể quan sát được:

> Để vượt qua kỹ năng dựa trên viết thành thị trường làm việc:

```markdown
After producing the candidate changelog, invoke the `release-risk-review` skill.
Pass the candidate path and require a blocking or non-blocking verdict.
If that skill is unavailable, stop and report the missing dependency.
```

Điều này làm cho sự phụ thuộc có thể kiểm tra và cho phép chủ nhà thực thi chính sách.

> Điều này làm cho việc phụ thuộc trở nên có thể kiểm tra, cũng cho chủ nhà một cơ hội để thực hiện chiến lược.

## Hãy xây dựng nó.

> **【中文解读】** `code/main.py`Thực hiện một bộ xác minh quy tắc hướng nhỏ và một bộ chọn ngôn ngữ nguyên thủy, toàn bộ quá trình chỉ sử dụng bộ quy tắc để mỗi quy tắc có thể được xem.`parse_frontmatter``validate_skill_text``ValidationIssue`- Không.`SkillReport`(Dữ liệu cấu trúc thay vì một giá trị không rõ ràng) và`FrontmatterSyntaxError`; lựa chọn器提供 `TaskShape`Với`select_primitives`, đưa nhu cầu nhiệm vụ được phân tích vào các mã thông thường, trình bày kho, kỹ năng, hook, subagent hoặc các công cụ MCP.

`code/main.py`thực hiện một xác thực viên định hướng tiêu chuẩn nhỏ và một người chọn đồ tạo vật. Nó chỉ còn stdlib để mọi quy tắc được nhìn thấy.

> `code/main.py`Thực hiện một bộ xác minh quy định nhỏ và một bộ chọn công cụ. Nó duy trì chỉ một bộ quy định, để mỗi quy tắc được nhìn thấy.

Người xác nhận cho thấy:

> 验证器暴露:

- `parse_frontmatter(text)`để tách metadata khỏi cơ thể.
  Trung ngữ翻译:`parse_frontmatter(text)`把元数据与正文分开.
- `validate_skill_text(text, directory_name, allowed_runtime_extensions=())`để kiểm tra các trường yêu cầu, đặt tên, mở rộng không rõ, sự hiện diện của cơ thể và giới hạn di động.
  Trung ngữ翻译:`validate_skill_text(text, directory_name, allowed_runtime_extensions=())` kiểm tra cần phải điền vào 字段、命名、未知扩展、正文存在性和可移植限制──
- `ValidationIssue`và `SkillReport`để trả lại bằng chứng cấu trúc thay vì một boolean không rõ ràng.
  Trung ngữ翻译:`ValidationIssue`和 `SkillReport` Trở lại bằng chứng cấu trúc chứ không phải là một giá trị không rõ ràng.
- `FrontmatterSyntaxError`cho các thông tin nhập mà không thể giải thích an toàn.
  Trung ngữ翻译:`FrontmatterSyntaxError` đối với các mục nhập không thể giải thích được.

Người chọn sẽ cho thấy`TaskShape`và `select_primitives(task)`Nó lập bản đồ nhu cầu của một nhiệm vụ với mã thông thường, hướng dẫn kho, kỹ năng, một cái móc, một subagent, hoặc một công cụ MCP.

> 选择器暴露 `TaskShape`和 `select_primitives(task)`Nó đưa nhu cầu nhiệm vụ được phân tích thành các mã thông thường, trình bày kho, kỹ năng, móng, phụ thuộc hoặc các công cụ MCP.

- Đi phòng thí nghiệm.

> 运行实验:

```bash
cd "$(git rev-parse --show-toplevel)"
cd phases/13-tools-and-protocols/22-skills-and-agent-sdks
python3 code/main.py
python3 -m unittest discover -s code/tests -v
```

Blok lệnh này cần một bản sao địa phương và phải bắt đầu từ bất cứ nơi nào bên trong
Cái người sao đó`git rev-parse --show-toplevel`có thể giải quyết nguồn kho.

> Bộ lệnh này cần một khối địa phương, và phải bắt đầu từ bất kỳ vị trí nào trong khối,`git rev-parse --show-toplevel`才能解析出仓库根目录──

Các bản demo in JSON cho một kỹ năng di động hợp lệ, một kỹ năng mở rộng máy chủ, một gói không hợp lệ và một số quyết định hình thức nhiệm vụ.

> 演示为一个合法的可移植技能"",一个带宿主扩展技能"",一个非法包和若干任务形态决策印印 JSON――研究那些问题 代码:包验证器应解释如何修复工件,而不是替代作者盲猜――

### Các vấn đề về lệnh xác nhận

Thiết lập các dữ liệu cấu trúc giá rẻ trước khi có quy tắc nội dung sâu hơn:

> Trước tiên kiểm chứng thực tế cấu trúc giá rẻ, tiếp tục quy tắc nội dung sâu hơn:

```figure
skill-validation-order
```

Trật tự này ngăn chặn các lỗi thứ cấp không che giấu bất biến bị hỏng đầu tiên.

> Chuyện này để ngăn chặn những sai lầm xảy ra trong cuộc sống.

## Sử dụng nó thực sự

> **【中文解读】**写技能 之前先填一张决策卡:需要跨多步的可复用模型判断?→ Kỹ năng.事件每次触发都必须执行?→ Hook 或应用代码.需要带类型输入的外部能力?→ 工具或 MCP 服务器.需要隔离的上下文/状态/所有权?→ Subagent. 指示只针对一个仓库?→ 仓库说明. 一次交互就足?→ 提示词.

Trước khi viết một kỹ năng, hãy điền vào thẻ quyết định này:

> 写技能 之前,先填写这张决策卡:

| Question | If yes | Likely primitive |
|---|---|---|
| Does this need reusable model judgment across several steps? | The procedure is stable but decisions vary | Skill |
| Must this happen every time an event fires? | Missing one execution is unacceptable | Hook or application code |
| Does the model need an external capability with typed inputs? | The operation lives outside model context | Tool or MCP server |
| Does the work need isolated context, state, or ownership? | A separate worker returns a bounded result | Subagent |
| Is this guidance specific to one repository? | It describes local commands and constraints | Repository instructions |
| Is one interaction enough? | No package lifecycle is needed | Prompt |

Nhiều dòng công việc sản xuất sử dụng nhiều hơn một hàng.

> Nhiều dòng sản xuất sẽ sử dụng không chỉ một dòng.

## Chuyển nó đi.

Bài học này tạo ra những`skill-contract-reviewer`gói dưới `outputs/`Nó chứa:

> 本课产 出 `outputs/`下的 `skill-contract-reviewer`包── nó bao gồm:

- một thiết bị di động`SKILL.md`xem xét gói kỹ năng được đề xuất;
  Trung文翻译: một kỹ năng kiểm tra ứng cử viên 包的可移植 `SKILL.md`-
- danh sách kiểm tra tham chiếu cho hợp đồng di động và lựa chọn nguyên thủy;
  Trung ngữ翻译:针对可移植契约与原语选择的参考清单;
- một kịch bản xác thực xác định;
  中文翻译: một định nghĩa xác định;
- Các thiết bị hình dạng nhiệm vụ bao gồm các lời nhắc, kỹ năng, công cụ, móng, mã thông thường và các bộ phận phụ.
  Trung文翻译:覆盖提示词、技能、工具、hook、普通代码和 subagent 的任务形态具──

Lắp đặt toàn bộ gói, không chỉ file nhập của nó:

> Ưu điểm của bạn là:

```bash
cd "$(git rev-parse --show-toplevel)"
python3 scripts/install_skills.py /tmp/aiefs-skills --phase 13 --type skill
```

Người cài đặt khóa học báo cáo mỗi kỹ năng phiên bản giai đoạn 13 và viết
`/tmp/aiefs-skills/manifest.json`. Điểm đến sạch này kiểm tra hình dạng gói;
vòng lặp thành công đầu tiên trên kiểm tra phát hiện và triệu hồi trong một máy chủ thực tế.

>  Khóa học cài đặt báo cáo mỗi bản của giai đoạn 13 kỹ năng và viết vào `/tmp/aiefs-skills/manifest.json`◊ hình thức kiểm tra mục đích của trang web này; 10 phút đầu tiên vòng kiểm tra trong nhà chủ thực sự

Các bài học sau đây làm sâu sắc hơn từng giai đoạn chu kỳ cuộc sống. Bài học 24 xây dựng khám phá và tiết lộ tiến bộ. Bài học 25 xây dựng chính sách triệu tập và định tuyến. Bài học 26 tách quyền ra khỏi sandboxing. Bài học 27 biến toàn bộ gói thành một đồ tạo được đánh giá.

> Chương trình tiếp theo từng giai đoạn của chu kỳ sống sâu sắc: Chương 24  Khám xây dựng phát hiện và công bố tiến bộ; Chương 25  Khám xây dựng điều chỉnh chiến lược và đường dẫn; Chương 26  Khám chia quyền và hộp thư; Chương 27  Khám hoàn toàn trở thành công cụ phát hành đánh giá.

## Tập luyện bài tập

1. Lập 5 dòng công việc từ nhóm của bạn bằng cách sử dụng `TaskShape`Hãy bảo vệ mọi trường hợp mà bạn chọn nhiều hơn một nguyên thủy.
   中文翻译:用 `TaskShape`Các nhóm bạn trong nhóm có 5 quy trình làm việc.

2. Thêm các thử nghiệm giới hạn chứng minh rằng một 500 ký tự `compatibility`giá trị vượt qua và giá trị 501 ký tự thất bại như một lỗi quy định.
   Trung文翻译:添加边界测试, chứng minh 500 字符的 `compatibility`值通过、501 字符的值以规范错失败──

3. Thêm một phần mở rộng thời gian chạy vào danh sách cho phép. Viết một bài kiểm tra chứng minh cùng một tệp vẫn có thể phân biệt với một kỹ năng chỉ di động.
   Trung ngữ翻译:向允许列表添加一个运行时扩展──写一个测试证明同一文件仍能与纯可移植技能区分开──

4. Chia một lời nhắc 400 dòng thành `SKILL.md`, một tham chiếu, một hợp đồng kịch bản, và một mẫu đầu ra.
   Trung ngữ翻译:把一个400 行的提示词拆成 `SKILL.md`、 một tài liệu tham khảo 、 một bản thảo hợp đồng và một mô hình xuất khẩu ⋅ để mỗi tài liệu chỉ chịu trách nhiệm một loại thông tin ⋅

5. Thiết kế phản ứng thất bại cho một kỹ năng tham chiếu một công cụ MCP không sẵn có. Đừng lặng lẽ thay thế một công cụ với các quyền rộng hơn.
   Trung文翻译:为引用了不可用 MCP 工具的技能 设计失败响应──不要替换成权限更宽的工具──

6. Xem lại một kỹ năng hiện có và dán nhãn mỗi câu như là định tuyến, quy trình, chính sách, chỉ dẫn tham chiếu hoặc hợp đồng xuất phát.
   Trung ngữ翻译: kiểm tra một kỹ năng hiện tại, đặt mỗi câu để đánh dấu cho đường dẫn, quy trình, chiến lược, chỉ dẫn hoặc giao ước xuất khẩu.

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|---|---|---|
| Agent skill | "A saved prompt" | A discoverable directory of procedural instructions and optional resources |
| Portable core | "Fields every runtime shares" | The contract defined by the Agent Skills specification |
| Runtime extension | "Extra frontmatter" | Host-specific configuration whose behavior requires a compatible adapter |
| Activation | "The skill ran" | The skill body entered model-visible context; execution may come later |
| Skill dependency | "Import another skill" | A runtime-mediated invocation edge with availability and policy checks |
| Tool contract | "A function schema" | Inputs, outputs, permissions, side effects, errors, and evidence for a capability |

## Xem thêm 延伸阅读

- [Agent Skills specification](https://agentskills.io/specification)Đối với danh mục di động và hợp đồng mặt hàng.
  Trung文翻译:Công tác Kỹ năng 规范可移植目录与前文 契约的出处
- [Agent Skills best practices](https://agentskills.io/skill-creation/best-practices)cho phạm vi, hướng dẫn và tổ chức nguồn lực.
  Trung文翻译:Công lực của đại lý 最佳实践范围、指令与资源组织
- [OpenAI: Build skills](https://learn.chatgpt.com/docs/build-skills)cho hành vi khám phá và kêu gọi Codex hiện tại.
  Trung文翻译:OpenAI  xây dựng kỹ năng Codex 当前的发现与调用行为
- [Claude Code skills](https://code.claude.com/docs/en/skills)cho một runtime của cuộc gọi, lập luận, công cụ và các phần mở rộng nội dung ủy quyền.
  Trung ngữ翻译:Claude Code skills一个运行时调用、参数、工具与委托上下文扩展
