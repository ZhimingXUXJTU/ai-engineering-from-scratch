# Khám phá kỹ năng và tiết lộ tiến bộ

> Một kỹ năng trở nên hữu ích trước khi được tải lên cơ thể. Tên và mô tả của nó giành được một vị trí trong danh mục; các tập tin sâu hơn của nó chỉ có được ngữ cảnh khi công việc đạt đến chúng.

> **【中文解读】**技能在正文被加载之前就已经开始发挥作用:名称和描述先赢得它在目录中;文件更深层只有当任务真正走到那一步才进入下文. 本课解决两个工程问题:发现 (发现) 发现 (发现) 没有简单的递归文件搜索 (搜索) 处理作用域,试验,同名冲突和目录发布;渐进披露 (披露) 渐进的披露) 必须是有意的分层加载,否则会退回为"渐进的困惑" (Phát hiện) 已开始发挥作用:名称和描述先赢得它在目录中;文件更深层的文件只有当任务真正走到那一步才进入下文. 本课解决两个工程问题:发现 (发现) 发现 (发现) 没有简单的递归文件搜索处理作用域,试验,同名冲突和目录发布;渐进的披露 (披露) 必须是有意的分层加载,否则会退回为"渐进的困惑" (Phát hiện) 了.

> **【拓展：Agent Skills 子系列→本课位置】**本课是代理技能子系列的第二课程;;Phase 13 · 22-27) 课22 定义技能包的可移植契约;;SKILL.md;本课解决" chủ nhà quản lý tìm thấy kỹ năng và phân cấp tải"; Bài25 处理调用与路由, Bài26 处理权限、沙箱与信任, Bài27 处理评测与打包;;发现与披露是每个支持代理技能的主管;;Claude Code、Codex等) phải đối mặt với vấn đề đầu tiên trong quá trình vận hành.

>  **【前置】**Học本课前请先掌握:Phase 13 · 22(Công trình của đại lý:可移植契约与运行时边界) SKILL.md 的包结构(làm trước + 正文 + tham chiếu/tác phẩm/ tài sản),以及"技能是上下文而非工具"的边界──

**Type:** Build | **类型:** 动手实践
**Languages:** Python (stdlib) | **语言:** Python（标准库）
**Prerequisites:** Phase 13 · 22 (Agent Skills: Portable Contract and Runtime Boundary) | **前置知识:** Phase 13 · 22（Agent Skills：可移植契约与运行时边界）
**Time:** ~105 minutes | **时间:** 约 105 分钟

## Mục tiêu học tập

- Xây dựng một hệ thống phát hiện hệ thống tập tin phân biệt phạm vi, xác thực, chính sách va chạm và xuất bản danh mục.
  Trung ngữ翻译:构建一条文件系统发现流水线,把作用域、校验、冲突策略和目录 发布分开处理──
- Giải thích ba mức tiết lộ: danh mục metadata, hướng dẫn hoạt động và tài nguyên cụ thể cho nhiệm vụ.
  Trung文翻译:解释三级披露:catalog 元数据、活跃指令、任务特定资源──
- Các tham chiếu thiết kế để một đại lý có thể tiếp cận chi tiết cần thiết trực tiếp mà không cần tải toàn bộ gói.
  Trung文翻译:设计引用结构,使代理能直达所需细节而无需加载整个包──
- Không gian danh mục ngân sách độc lập với bối cảnh kỹ năng hoạt động.
  Trung文翻译:为目录空间与活跃技能上下文分别做预算。
- Tháo đường đi và thoát khỏi đường dây khi một kỹ năng đọc tài nguyên của riêng mình.
  Trung文翻译:在技能读取自身资源时拒绝路径穿越 (nước qua) 和符号链接 (tín kết) 逃逸 (nước trốn).

## Vấn đề  vấn đề giới thiệu

Trưởng của anh có 200 kỹ năng được cài đặt.`SKILL.md`, tệp tham khảo, kịch bản và mẫu khi bắt đầu phiên sẽ chôn vùi nhiệm vụ hiện tại trong thủ tục không liên quan. Không tải gì sẽ buộc người dùng nhớ chính xác các con đường hệ thống tệp.

> Trưởng phòng của anh đã cài đặt 200 kỹ năng.`SKILL.md`、 tài liệu tham khảo、 kịch bản và mô hình, sẽ khiến nhiệm vụ hiện tại bị chìm trong quá trình không liên quan; bất cứ điều gì không tải, người dùng cũng phải nhớ rõ ràng các đường bộ hệ thống tài liệu.

Sự thỏa hiệp thông thường là một danh mục: cho mô hình một danh tính nhỏ gọn và mô tả định tuyến cho mỗi kỹ năng đủ điều kiện, sau đó tải toàn bộ cơ thể chỉ sau khi lựa chọn.

> Thông thường, các chương trình được phân tích là một danh mục: trước đó mô hình sẽ hiển thị tính chất và cách thức mô tả của mỗi kỹ năng đủ điều kiện, sau đó chỉ tải đầy đủ văn bản chính xác.

Đầu tiên, phát hiện không chỉ là tìm kiếm tệp khôi phục. Kỹ năng có thể tồn tại tại tại tại dự án, người dùng, quản trị viên, plugin hoặc phạm vi tích hợp. Hai gói có thể chia sẻ một tên. Một liên kết đồng nghĩa có thể chỉ ra bên ngoài gốc đáng tin cậy. Một gói bị hình thành sai có thể tiêu thụ không gian danh mục hoặc trở nên không thể được gọi.

> Đầu tiên, tìm thấy không chỉ là tìm kiếm tài liệu gửi đi. Khả năng có thể tồn tại trong các dự án, người dùng, người quản lý, tiện ích hoặc phạm vi đóng góp; hai gói có thể cùng tên; một mã liên kết có thể chỉ ra bên ngoài gốc nhận; một gói hình có thể chiếm catalog không gian, hoặc trở nên không thể sử dụng.

Thứ hai, việc tiết lộ dần dần có thể trở thành sự nhầm lẫn dần dần.`SKILL.md`"đọc hướng dẫn liên quan" và gói chứa mười hai hướng dẫn, mô hình phải đoán. Nếu mỗi hướng dẫn chỉ ra ba tập tin khác, tải trở thành một bước đi biểu đồ không giới hạn.

> Thứ hai, việc tiết lộ tiến bộ có thể trở thành một sự bối rối tiến bộ. Nếu`SKILL.md`Chỉ cần nói "đọc liên quan hướng dẫn" và bao gồm 12 hướng dẫn, mô hình chỉ có thể dựa vào đoán; nếu mỗi hướng dẫn lại hướng đến ba tài liệu khác, tải trở thành một bức tranh vô biên.

Một thời gian chạy tốt làm cho khám phá xác định và tiết lộ có ý định.

> Một hoạt động tốt khi làm cho phát hiện là xác định, tiết lộ là có ý định.

## Khái niệm cốt lõi

> **【中文解读】**Chương trình này được "xám" thành một bộ biên dịch viên dòng chảy: hệ thống tài liệu là nguồn nhập, không bao giờ đưa đường gốc trực tiếp ra mô hình. Ưu điểm có năm: 1) 作用域 (số) là chiến lược thời gian vận hành  quy định có thể di chuyển chỉ xác định gói kỹ năng tự nó, không xác định thống nhất đường cài đặt hoặc thứ tự ưu tiên, chủ nhà phải tuyên bố rõ ràng tìm kiếm những danh mục gốc nào, ai có quyền viết về nó; 2) cùng tên xung đột (collision)                                                                                                                                                                                                  

### Discovery là một đường ống biên dịch. Discovery là một đường ống biên dịch.

Hãy xem hệ thống tệp như là đầu vào nguồn. Đừng xuất bản các đường dẫn nguyên liệu trực tiếp vào mô hình.

> Hãy đưa hệ thống tài liệu như nguồn nhập. Đừng đưa đường gốc trực tiếp ra mô hình.

```figure
skill-discovery-pipeline
```

Mỗi giai đoạn nên tạo ra dữ liệu có cấu trúc và lỗi có cấu trúc.

- Những gốc rễ nào đã được tìm kiếm?
- Những ứng cử viên nào được tìm thấy?
- Những ứng cử viên nào bị từ chối và tại sao?
- Bác nào thắng vụ va chạm?
- Những mục danh mục nào đã bị rút ngắn hoặc bỏ qua vì ngân sách?

Nếu không có bằng chứng đó, "mô hình không sử dụng kỹ năng của tôi" gần như không thể chẩn đoán.

> 没有这些证据,"模型没有用我的技能"几乎无法诊断. 发现日志应能回答: tìm kiếm những danh mục gốc nào, tìm thấy những ứng cử viên nào, từ chối những ứng cử viên nào, nguyên nhân nào, ai thắng cuộc xung đột nào, những danh mục nào vì ngân sách bị cắt giảm hoặc省略.

### Mức độ là chính sách thời gian chạy.

Các thông số kỹ thuật di động xác định một gói kỹ năng, không phải là một con đường cài đặt phổ biến hoặc thứ tự ưu tiên.

> Quy tắc di chuyển được xác định bởi gói kỹ năng, chứ không phải là một cách cài đặt thống nhất hoặc theo thứ tự ưu tiên.

Một runtime chung có thể sử dụng các phạm vi này:

| Scope | Example root | Intended ownership |
|---|---|---|
| Workspace | `<repo>/.agents/skills/` | Project maintainers |
| User | `<user-data>/skills/` | One developer |
| Administrator | `<system>/skills/` | Machine or organization policy |
| Plugin | A signed plugin bundle | Plugin publisher and installer |
| Built-in | Runtime package | Runtime vendor |

Tính đến tháng 8 năm 2026, Codex tài liệu dự án khám phá từ `$CWD/.agents/skills`thông qua thư mục tổ tiên đến gốc kho, cộng với người dùng, quản trị viên và các vị trí tích hợp. Nó hỗ trợ thư mục kỹ năng liên kết. Hai tên trùng lặp có thể xuất hiện thay vì được sáp nhập. Đó là hành vi Codex, không phải là yêu cầu của `SKILL.md`; kiểm tra dòng [Codex skill documentation](https://learn.chatgpt.com/docs/build-skills)khi viết một bộ điều chỉnh.

Không bao giờ phát minh ra ưu tiên từ tên thư mục. tuyên bố nó như chính sách và kiểm tra nó.`Scope`Vì vậy, cùng một bộ ứng cử viên luôn giải quyết theo cùng một cách.

> 永远不要从目录名字构造优先级. 应将它声明为策略并测试.`Scope`Một thứ hạng toàn bộ rõ ràng, khiến cho cùng một nhóm ứng cử viên总是解析出相同结果──(表中五种作用域:Workspace=项目维护者、User=单个开发者、Administrator=机器或组织策略、Plugin=插件发布者与安装者、Built-in=运行时厂商──)

### Các vụ va chạm cần sự xác định vượt ra ngoài `name` Thêm vào đó, cần giấy tờ nhận dạng ngoài tên.

Hai gói được đặt tên `release-readiness`Một trong số đó có thể là một không gian làm việc bị bỏ qua và một người dùng mặc định.

```json
{
  "name": "release-readiness",
  "description": "Inspect a release candidate for this repository.",
  "scope": "workspace",
  "source": "/repo/.agents/skills/release-readiness",
  "selected": true
}
```

Các chính sách va chạm chung bao gồm:

| Policy | Benefit | Risk |
|---|---|---|
| Keep every candidate | Nothing is hidden | The model sees ambiguous names |
| Highest-precedence scope wins | Simple invocation | A local package can shadow a trusted one |
| Reject duplicates | No silent shadowing | Legitimate overrides stop working |
| Qualify names by source | Explicit identity | User-facing names become longer |

Chọn một chính sách cho người chủ. Giữ các ứng cử viên bị từ chối hoặc bị ám ảnh trong chẩn đoán ngay cả khi họ không có trong danh mục mẫu.

> Đối với chủ nhà chọn một chiến lược:即可. 即便被拒绝或被遮蔽的候选人不进模型目录,也应保留它们在诊断信息里.

### Ba cấp độ tiết lộ.

Các kỹ năng đặc biệt của Agent mô tả việc tải theo từng giai đoạn.

> Kỹ năng đại lý quy định mô tả là phân giai đoạn tải.

> **【中文解读】**3 cấp tiết lộ giải quyết các vấn đề khác nhau:Tầng 1 ((catalog 元数据) giải quyết" mô hình có thể phân biệt nó với hàng xóm không", quy định ước tính mỗi hiệp ước 100 token, mô tả để viết hai phân đoạn 能力是什么 + 什么情况触发;Tầng 2 ((active instruction) giải quyết" kích hoạt sau mô hình có thể chính xác bắt đầu hoạt động không", quy định khuyến cáo SKILL.md  giữ trong 500 行  Đây là tín hiệu thiết kế không phải là để điền đầy chỉ, trình diễn chủ yếu không thể để rút ngắn các tài liệu nhập khẩu mà điền vào trích dẫn;Tầng 3 tài nguyên)  tài liệu tham chiếu  đọc các kịch bản  cung cấp tính toán xác định, tài sản là mô hình chứ không phải chỉ thị Những tên này là định nghĩa không phải là khả năng ma thuật, chủ sở hữu vẫn cần các công cụ truy cập và thực hiện tài liệu.

```figure
skill-disclosure-levels
```

#### Lớp 1: Catalog Metadata Lớp 1: Catalog Data

Mô hình cần đủ thông tin để phân biệt kỹ năng từ hàng xóm. Khác định ước tính khoảng 100 token cho mỗi mục danh mục, nhưng chuỗi và token thực tế thuộc về chủ nhà.

Một mô tả hữu ích có hai câu:

```yaml
description: Validate a release candidate and produce a readiness report. Use when the user asks whether a version, tag, or package is ready to publish.
```

Điều thứ nhất nói về khả năng, điều thứ hai nói về giới hạn kích hoạt, và bài học 25 đánh giá giới hạn này bằng các lời nhắc tích cực và gần như bị bỏ lỡ.

> Bài học 25 会用正向与近似未命中 (nằm gần) 快速来评测这条边界――

#### Lớp 2: Chỉ thị hoạt động

Sau khi kích hoạt, cơ thể nên hoạt động như một bản đồ và một thủ tục.`SKILL.md`dưới 500 dòng. Đó là tín hiệu thiết kế, không phải mục tiêu để lấp đầy.

>                                                                                                                                                                                                                                                               `SKILL.md`Giữ trong 500 行 trong đó là một tín hiệu thiết kế, không phải để điền vào chỉ số.

Cơ thể nên chứa:

- giới hạn nhiệm vụ;
- dòng công việc mặc định;
- Điều kiện của ngành;
- tham chiếu trực tiếp đến các tệp sâu hơn;
- Hợp đồng công cụ và kịch bản;
- Hành vi thất bại và dừng lại;
- sản lượng dự kiến và xác minh.

Không di chuyển dòng công việc trung tâm vào một tham chiếu chỉ để làm cho tệp nhập ngắn.

> Đừng để rút ngắn các file nhập vào mà chuyển các quy trình cốt lõi vào các tài liệu tham khảo.

#### Lớp 3: hỗ trợ tài nguyên

Các tài sản được sao chép, điền vào hoặc biến thành các sản phẩm được giao ra thay vì được xem như hướng dẫn.

> 引用(引用)提供文字或数据;脚本(skripts)提供确定性计算;资产(资产) được sao chép、填充或转换为交付物,而不是被当作命令──

| Directory | Model reads it? | Model executes it? | Typical content |
|---|:---:|:---:|---|
| `references/` | Yes, when needed | No | schemas, policies, domain guides |
| `scripts/` | May inspect it | Through a permitted tool | validators, converters, collectors |
| `assets/` | Only if useful | No | templates, fixtures, images, starter files |

Những tên này là các quy ước, không phải khả năng ma thuật.

> Những tên này là một phép thuật, không phải là khả năng ma thuật.

### Các tham chiếu cụ thể của ngành vượt qua các bài viết về chủ đề

Viết file nhập như một bản đồ quyết định:

```markdown
## Choose the path

- For a Python package, read `references/python-release.md`.
- For a container image, read `references/container-release.md`.
- For a documentation-only release, read `references/docs-release.md`.
- If the release combines artifact types, read only the guides for those artifacts.
```

Điều này cho mỗi tham chiếu một điều kiện tải có thể quan sát được.`references/`"Đừng có gì hơn" không.

> Để cho mỗi trích dẫn có một điều kiện tải có thể quan sát được.`references/`了解更多"则没有──

Giữ biểu đồ tham chiếu nông.`SKILL.md`Một cú nhảy làm cho khả năng tiếp cận được kiểm tra và làm giảm khả năng hạn chế cần thiết không bao giờ vào ngữ cảnh.

> 保持引用图浅──官方指南建议从 `SKILL.md`直接链接、避免深链──一跳(one hop) để có thể kiểm tra, cũng làm giảm tỷ lệ "bắt buộc cần thiết chưa bao giờ vào trên 下文"

```figure
skill-reference-map
```

### Ngân sách danh mục và bối cảnh hoạt động là ngân sách khác nhau.

Để `c_i`là chi phí danh mục hàng loạt của kỹ năng `i`- `B_c`ngân sách danh mục, `b_j`chi phí cơ thể hoạt động, và `r_k`nguồn lực thực sự được tải.

```text
catalog_cost = sum(c_i for every published skill)
active_cost = sum(b_j for every activated skill) + sum(r_k for every disclosed resource)
```

Giảm một ngân sách không tự động giảm một ngân sách khác. Biểu đồ ngắn có thể tiết kiệm không gian danh mục trong khi một cơ thể 900 dòng hoạt động vẫn làm quá tải nhiệm vụ. Chia cơ thể thành tham chiếu chỉ có thể giảm chi phí hoạt động khi thời gian chạy và hướng dẫn thực sự tránh tải các chi nhánh không liên quan.

> 削减 một ngân sách sẽ không tự động cắt giảm một khác ⋅短描述能省目录空间, nhưng sau khi kích hoạt 900 行正文照样淹没任务; đưa正文拆 into引用只有当运行时和命令确实避免加载无关分支时,才能真正降低活跃成本.

Codex hiện đang lập kế hoạch cho danh sách kỹ năng ban đầu ở mức 2% trong bối cảnh
cửa sổ khi kích thước cửa sổ ngữ cảnh được biết.
fallback chỉ khi kích thước đó không được biết; nó không phải là một nắp thứ hai kết hợp với
Quy tắc 2% Khi danh mục vượt quá ngân sách áp dụng,
Các mô tả có thể được rút ngắn hoặc bỏ qua.
Chính sách Codex, không phải thuộc về tiêu chuẩn kỹ năng đại lý.

> Codex hiện tại trong cửa sổ có sẵn trên văn bản dưới đây: , hãy đặt 2% ngân sách của danh sách kỹ năng ban đầu; 8.000 ký tự chỉ là giá trị trở lại của thời gian không rõ ràng, không phải là giới hạn trên đường thứ hai của 2% .

### Các đường nguồn tài nguyên là ranh giới niềm tin.

> **【中文解读】**技能 chỉ cần đọc các tài liệu trong bản thân, nhưng chữ字符串前检查不够`references/../../../../.ssh/config`(routée traversée) và chỉ dẫn các liên kết mã bên ngoài bao gồm cả có thể lừa dối trước đây. Thực hành chính xác: sử dụng hệ thống tài liệu ngữ nghĩa giải quyết danh mục rễ và các đường dẫn ứng cử viên, từ chối tuyệt đối các đường lối nhập, xác nhận các ứng cử viên vẫn còn dưới gốc rễ của các đường dẫn; các liên kết mã cho phép để được quyết định trước khi phát hiện, cho phép các mục tiêu sau mỗi lần phân tích các bài học.

Một kỹ năng chỉ nên đọc các tệp bên trong gói của nó.

```text
references/../../../../.ssh/config
references/external-link -> /private/company-secrets
```

Giải quyết gốc gói và ứng cử viên bằng ngữ nghĩa hệ thống tập tin, từ chối đầu vào tuyệt đối và xác minh rằng ứng cử viên được giải quyết vẫn nằm dưới gốc được giải quyết.

> Sử dụng hệ thống tài liệu để phân tích danh mục gốc và đường dẫn ứng cử viên, từ chối hoàn toàn các đường dẫn nhập, và xác minh các ứng cử viên sau khi phân tích vẫn nằm dưới gốc của sau khi phân tích.

```figure
skill-resource-containment
```

Việc giữ đường dẫn không thiết lập sự tin cậy nội dung. Một tham chiếu hợp lệ trong gói vẫn có thể chứa các hướng dẫn độc hại. Bài học 26 xử lý mối đe dọa đó.

> 路径包含不等于内容可信.  Một quy định pháp lý bao gồm trong có thể vẫn có chứa lệnh ác ý.

### Lái phải được quan sát.

Lưu ý các sự kiện tiết lộ mà không ghi lại bí mật:

```json
{
  "event": "skill.resource.loaded",
  "skill": "release-readiness",
  "resource": "references/python-release.md",
  "reason": "candidate contains pyproject.toml",
  "bytes": 2840
}
```

Lý do biến một lựa chọn ngữ cảnh thành bằng chứng có thể xem xét. Nó cũng giúp xác định các hướng dẫn khiến cho đại lý tải mỗi tệp "chỉ vì trường hợp".

> Lý do 字段 biến một lần trên văn bản dưới đây chọn thành chứng cứ có thể xét nghiệm, cũng có thể giúp xác định những người để cho đại lý "để ngăn chặn" tải các chỉ thị của mỗi tài liệu.

## Hãy xây dựng nó.

> **【中文解读】** `code/main.py` xây dựng một công cụ phát hiện và công bố xác định:`Scope`(tài liệu từ:`SkillCandidate`(未校验的文件系统候选)`discover_scope`(枚举直接子目录中的技能)`resolve_collisions`(apply a条已声明冲突策略)`CatalogEntry`+ `build_catalog`(đưa ra có giới hạn dữ liệu)`CatalogBudget`(nước tính toán, thay vì số chữ giả bằng số biểu tượng chung)`load_skill_body`(Tầng 2 激活)`validate_reference`(路径包含校验)`load_reference`(有界的 Level 3 读取) ⋅demo 会创建临时项目与用户作用域、插入一个冲突、在意调小的预算下构建目录、激活一个技能,并分别尝试一次合法引用读取和一次穿越逃逸不装任何永久文件──

`code/main.py`xây dựng một động cơ phát hiện và tiết lộ xác định.

Mối phát hiện bao gồm:

- `Scope`cho nguồn và các metadata ưu tiên;
- `SkillCandidate`đối với ứng viên hệ thống tệp không được xác nhận;
- `discover_scope(scope)`để liệt kê các thư mục kỹ năng ngay lập tức;
- `resolve_collisions(candidates, precedence)`áp dụng một chính sách được tuyên bố;
- `CatalogEntry`và `build_catalog(...)`để công bố các metadata giới hạn;
- `CatalogBudget`để giải thích các mục nhập theo chuỗi mà không giả vờ là các mã thông báo phổ quát.

Màn hình tiết lộ bao gồm:

- `load_skill_body(entry, ...)`cho kích hoạt cấp 2;
- `validate_reference(skill_dir, reference)`cho việc ngăn chặn đường đi;
- `load_reference(...)`cho các bài đọc cấp 3 bị giới hạn.

- Đi phòng thí nghiệm.

```bash
cd "$(git rev-parse --show-toplevel)"
cd phases/13-tools-and-protocols/24-skill-discovery-and-progressive-disclosure
python3 code/main.py
python3 -m unittest discover -s code/tests -v
```

Khóa này yêu cầu một bản sao lập bản địa và giải quyết nguồn kho từ bất kỳ
thư mục làm việc bên trong clone đó.

Demos tạo ra phạm vi dự án và người dùng tạm thời, chèn một vụ va chạm, xây dựng một danh mục theo ngân sách nhỏ cố ý, kích hoạt một kỹ năng, và cố gắng cả đọc tham chiếu hợp lệ và thoát khỏi. Không có tệp vĩnh viễn được cài đặt.

### Tại sao khám phá là nông hơn, tại sao khám phá là thấp hơn?

`discover_scope`kiểm tra thư mục trẻ em ngay lập tức cho `SKILL.md`Nó không chữa trị mỗi con lồng.`SKILL.md`Như vậy bảo vệ ranh giới gói và tránh xuất bản vô tình các ví dụ hoặc thiết bị trong một kỹ năng được cài đặt.

> `discover_scope`Chỉ kiểm tra trực tiếp trong danh mục của con `SKILL.md`, không đặt mỗi cái nhựa `SKILL.md`归归地作为独立包──这保住包边界,避免意外发布已安装技能内部的示例或固定──

### Tại sao phòng thí nghiệm không phân tích YAML tùy ý ?

Phòng thí nghiệm hỗ trợ các mặt hàng scalar cần thiết cho danh mục của nó. Một thời gian chạy sản xuất nên sử dụng một trình phân tích YAML an toàn với một sơ đồ rõ ràng, giới hạn kích thước và vô hiệu hóa cấu trúc đối tượng tùy chỉnh. "Stdlib-only" là một hạn chế giảng dạy, không phải là quyền để phát minh ra một phương ngữ YAML một phần im lặng.

> 实验只支持目录所需标量前材料――生产运行时应使用安全的YAML解析器显式方案、大小限制、禁用自定义对象构建――"仅标准库" là một tập hợp, không phải là một phép发明 một cách còn sót lại của YAML 方言――

## Hãy sử dụng nó. Hãy học cách sử dụng nó.

Sử dụng danh sách kiểm tra này cho bất kỳ bộ điều chỉnh phát hiện nào:

1. Đăng danh sách tất cả các nguồn được cấu hình và ai có thể viết cho nó.
2. Cần xác định liệu các gói liên kết có được phép hay không.
3. Thiết lập tên gói, tên thư mục, siêu dữ liệu cần thiết và kích thước của cơ thể nhập.
4. Bảo tồn nguồn gốc và phạm vi trong bản sắc bên trong.
5. Thiết lập và kiểm tra hành vi tên trùng lặp.
6. Đánh giá danh mục liên kết chính xác được gửi đến mô hình.
7. ghi lại lý do tại sao một cơ thể hoặc tài nguyên đã được tải.
8. Giữ nguồn đọc bên trong gốc gói được giải quyết.
9. Thiếu rõ ràng khi một tập tin tham chiếu bị thiếu.
10. Tạo lại danh mục khi cài đặt hoặc chính sách thay đổi.

## Chuyển nó đi.

Bài học này tạo ra những`skill-catalog-builder`Nó quét các gốc được sắp xếp rõ ràng, từ chối các tệp nhập liên kết và sự không phù hợp của thư mục tên, giải quyết các vụ va chạm phạm vi, từ chối các bản sao có ưu tiên tương đương và kết hợp các siêu dữ liệu được chọn vào mục nhập, mô tả và ngân sách ký tự được trình tự.

> 本课产 出 `skill-catalog-builder`包: theo thứ tự của tuyên bố rõ ràng quét danh mục gốc, từ chối các mã liên kết nhập khẩu tài liệu và tên-thư mục không phù hợp, phân tích các xung đột trong phạm vi tác dụng, từ chối các bài lặp lại có cùng ưu tiên, và đưa các dữ liệu được chọn vào số lượng các mục đã được tuyên bố, mô tả độ dài và ngân sách ký tự sắp xếp.

Báo cáo JSON của nó chứa các mục đã chọn, ứng cử viên bị bóng tối, các mục bị bỏ qua, lỗi xác thực, ưu tiên và sử dụng ngân sách. Lập cơ thể và tham chiếu vẫn là các hoạt động chạy riêng biệt, vì vậy người tạo danh mục không thực hiện kịch bản hoặc đưa toàn bộ gói vào ngữ cảnh.

> Bản báo cáo JSON của nó chứa các mục được chọn, các ứng cử viên bị che giấu, các mục bị bỏ qua, các sai lầm trong quá trình kiểm tra, ưu tiên và chiếm đóng ngân sách.

## Tập luyện.

1. Thêm phạm vi plugin và đặt nó giữa người dùng và ưu tiên tích hợp.
2. Thay đổi chính sách va chạm từ ưu tiên cao nhất để có đủ điều kiện tên.
3. Thêm giới hạn kích thước byte vào `load_reference`Thử một tập tin ở mức giới hạn và một byte trên đó.
4. Tạo hai mô tả có âm thanh gần giống nhau và viết lại để ranh giới kích hoạt không chồng chéo.
5. Thêm một biểu đồ chứa hash cho mỗi tham chiếu và kịch bản. Khám phá một tài nguyên được sửa đổi trước khi tải nó.
6. Công cụ demo để báo cáo cấp 1, cấp 2, và cấp 3 đếm byte riêng biệt.

## Từ khóa  Keyword

> Các bài viết được viết dưới đây là các bài viết được viết dưới đây:

| Term | What people say | What it actually means |
|---|---|---|
| Skill discovery | "Find every SKILL.md" | Search configured scopes, validate packages, attach provenance, and apply policy |
| Skill catalog | "The list of installed skills" | Compact model-visible routing metadata for eligible packages |
| Collision policy | "Which duplicate wins" | A declared rule for same-name candidates from different sources |
| Progressive disclosure | "Lazy loading" | Staged context admission from catalog to body to branch-specific resources |
| Reference graph | "Files linked by the skill" | The reachable resource structure and its load conditions |
| Path containment | "Stay in the folder" | Verify resolved resource targets remain inside the resolved package root |

## Xem thêm 延伸阅读

- [Agent Skills specification](https://agentskills.io/specification)cho hình dạng gói và mức độ tiết lộ tiến bộ.
- [Optimizing skill descriptions](https://agentskills.io/skill-creation/optimizing-descriptions)cho metadata định tuyến danh mục.
- [Agent Skills best practices](https://agentskills.io/skill-creation/best-practices)cho các tham chiếu trực tiếp và kích thước tệp nhập.
- [OpenAI: Build skills](https://learn.chatgpt.com/docs/build-skills)cho phạm vi khám phá Codex hiện tại và giới hạn danh mục.

> 阅读顺序建议:先读 经纪人技能 规范掌握包形与披露分级;再使用优化描述 学写路由描述;最佳实践讲直接引用与入口文件大小;最后查看 Codex 文档了解某宿主当前发现作用域和目录 限量;;
