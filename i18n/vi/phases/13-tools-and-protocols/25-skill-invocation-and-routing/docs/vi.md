# Khéo năng gọi và định tuyến

> Việc kêu gọi là một quyết định của cơ quan và sau đó là một quyết định liên quan.

> **【中文解读】**调用(chuyên dẫn) là một chuỗi hai quyết định độc lập: "先问权限"这个角色允许请求这个技能吗",再问相关性"这个请求真的该路由到它吗"― 详细介绍 帮模型做对第二决策,好的政策决定第一决策的答案;描述 写得再好也替代不了政策―― 本课把"谁能调用" (见见性人类 × 模型可选性) 和"该不应调用" (该不应调用)  分成两个正维交道,并给出五阶段调用生命周期的精确词汇――

> **【拓展：Agent Skills 子系列→本课位置】**Bài học 22  định nghĩa kỹ năng gói hợp đồng, Bài học 24  giải quyết phát hiện và tiết lộ, bài học này trả lời " kỹ năng làm thế nào được kích hoạt": rõ ràng调用(nói người dùng) 隐式调用(模型按描述路由) 应用编排、技能间组组合、评测利用 五条通道。 Bài học 26 处理调用后权限沙箱与信任, Bài học 27 接近-miss 评测量路由质量──

>  **【前置】**Học本课前请先掌握:Phase 13 · 24(Khám phá kỹ năng và tiết lộ tiến bộ) 目录 元数据是隐式路由的输入,Liv 1 描述写法(能力分句 + 触发边界分句) 来自那一课──

**Type:** Build | **类型:** 动手实践
**Languages:** Python (stdlib) | **语言:** Python（标准库）
**Prerequisites:** Phase 13 · 24 (Skill Discovery and Progressive Disclosure) | **前置知识:** Phase 13 · 24（技能发现与渐进式披露）
**Time:** ~105 minutes | **时间:** 约 105 分钟

## Mục tiêu học tập

- Sự khác biệt giữa việc gọi người dùng rõ ràng, việc gọi mô hình ngầm, việc gọi ứng dụng và việc gọi kỹ năng cho kỹ năng.
  Trung ngữ翻译:区分显式用户调用"",隐式模型调用"",应用调用与技能间调用"",
- Mô hình khả năng nhìn thấy con người và mô hình đủ điều kiện như các chiều kích chính sách độc lập.
  Trung ngữ翻译:把"人类可见性" và"模型可选性" hình thành thành hai chiến lược độc lập.
- Viết mô tả định tuyến với các kích hoạt tích cực và biên giới gần bị bỏ lỡ.
  Trung文翻译:写出带正向触发条件和近似未命中 (近-miss) đường biên giới
- Sự đủ điều kiện, lựa chọn, kích hoạt, liên kết đối số và thực hiện trong các dấu vết và thử nghiệm.
  Trong trace và test, hãy chọn và kích hoạt các tham số.
- Chuyển đổi các trường gọi cụ thể thời gian chạy mà không trình bày chúng như là vật liệu mặt trước di động.
  Trung ngữ翻译:适配运行时专属的调用字段, đừng giả mạo chúng thành vật liệu mặt trước có thể di chuyển.

## Vấn đề  vấn đề giới thiệu

Bạn cài đặt một `database-migration`Skill. người dùng có thể chạy nó bằng tên, nhưng mô hình cũng thấy mô tả của nó và chọn nó khi ai đó hỏi một câu hỏi cơ sở dữ liệu chung.

> Anh đã cài một cái.`database-migration`技能── người dùng có thể chạy nó theo tên, nhưng mô hình cũng có thể nhìn thấy mô tả của nó, và một người hỏi về các vấn đề cơ sở dữ liệu chung khi chọn nó là kỹ năng này cho một nhiệm vụ chỉ cần giải thích đề xuất schema 变化──

Ông thêm vào`user-invocable: false`Trong một thời gian chạy khác, trường đó bị phớt lờ.`disable-model-invocation: true`Trong thời gian chạy mà người dùng hiểu nó, người dùng vẫn có thể gọi nó rõ ràng.

> Anh gia tăng`user-invocable: false`,                                                                                                                                                                                                                                                               `disable-model-invocation: true`, Quý năng trông đợi hoàn toàn biến mất; trong khi hiểu được hoạt động của nó, người dùng vẫn có thể rõ ràng điều chỉnh nó.

Không có gì sai với tên trường. Mô hình là sai. "Người dùng có thể thấy nó", " Mô hình có thể chọn nó, " " ứng dụng có thể tải trước nó, "và "các công cụ bên trong nó có thể thực hiện" là các thực tế riêng biệt.`invocable`không thể thể diễn tả được.

> 错不在字段名,错在心智模型――" người dùng có thể nhìn thấy nó"" mô hình có thể chọn trong nó"" ứng dụng có thể tải trước nó"" các công cụ bên trong nó có thể thực hiện" là bốn thực tế độc lập, một gọi là`invocable`Những giá trị của biểu hiện không có chúng.

Routing có một chế độ thất bại thứ hai. Nếu mô tả mơ hồ, một số kỹ năng trở nên hợp lý. Nếu mô tả được lấp đầy với các từ khóa, các nhiệm vụ không liên quan sẽ kích hoạt chúng.

> 路由还有第二种失败模式: mô tả含糊, một số kỹ năng đều có vẻ hợp lý; mô tả塞满关键词,无关任务也会触发;;

## Khái niệm cốt lõi

> **【中文解读】**本节要点:(1) 五条通道都能启动调用生命周期人类用户、模型/自主代理、应用、另一个技能/子代理、评测 harness,各有典型用途和主要风险;(2) 五阶段词汇要精确合格(政策允许) /选择(被点名或被路由) /激活(命令进入上下文) /执行(开始干活) /完成(输出通过独立成功检查),只记`skill_used=true`会掩盖失败发生在哪边界; 3) 人类可见 × 模型可选构成 2×2矩阵; 4) trước过资格再排序相关性,否则被禁最高分会挤出法规次高分――

### 5 kênh có thể bắt đầu chu kỳ đời. 5 đường dẫn có thể bắt đầu chu kỳ đời.

| Actor | Invocation shape | Typical use | Main risk |
|---|---|---|---|
| Human user | Names a skill in the UI or prompt | Deliberate workflow selection | User expects availability or authority the host does not grant |
| Model or autonomous agent | Selects a catalog entry from task context | Automatic expert procedure | False-positive routing |
| Application | Activates or preloads a skill through runtime code | Fixed product workflow | Hidden coupling to one host |
| Another skill or subagent | Requests an exact skill as a workflow dependency | Composition | Cycles, missing dependency, or context bleed |
| Evaluation harness | Activates an exact skill under a fixed scenario | Repeatable measurement | Tests the skill while accidentally bypassing the production policy under study |

Các thông số kỹ năng đại lý di động xác định gói. Nó không tiêu chuẩn hóa một UI lệnh slash phổ quát, cờ định tuyến ngầm, API ứng dụng hoặc vòng đời subagent.

> Có thể di chuyển được Kỹ năng của đại lý  quy tắc được định nghĩa là包──它不标准化统一的斜命令 UI、隐式路由开关、应用 API或子代理 生命周期──

### 5 giai đoạn của cuộc gọi.

```figure
skill-invocation-stages
```

Sử dụng chính xác những từ này:

- **Eligible**nghĩa là chính sách cho phép diễn viên này yêu cầu kỹ năng.
- **Selected**nghĩa là người dùng đặt tên nó hoặc một bộ định tuyến đánh giá nó có liên quan.
- **Activated**nghĩa là các hướng dẫn của nó được đưa vào bối cảnh làm việc.
- **Executing**nghĩa là đại lý bắt đầu làm việc mô hình hoặc công cụ theo các hướng dẫn đó.
- **Completed**nghĩa là sản phẩm đã đáp ứng kiểm tra thành công độc lập.

Một dấu vết chỉ ghi lại`skill_used=true`ẩn ranh giới nơi một thất bại xảy ra.

> Chỉ ghi lại`skill_used=true`Hình ảnh của sự thất bại xảy ra ở những biên giới nào.

> **【中文解读】**Đó là một trong những từ ngữ được chọn để sử dụng trong vòng đời: được chọn bởi chính sách, được chọn bởi người hoặc nhà mạng, được kích hoạt bởi các nhân vật, thực hiện bởi các nhân vật, và được hoàn thành bởi các nhân vật.

### Người và mô hình invocation hình thành một 2x2 matrix . người dùng và mô hình dùng cấu thành 2x2 矩阵

| Human can invoke | Model can invoke | Mode | Suitable examples |
|:---:|:---:|---|---|
| Yes | Yes | Shared | Code explanation, test planning, documentation review |
| Yes | No | Human-only | Publish preparation, billing export, destructive cleanup plan |
| No | Yes | Model-only | Internal style guide, domain reference, automatic support procedure |
| No | No | Disabled or application-only | Staged rollout, deprecated package, programmatic preload |

Matrix là một mô hình chính sách, không phải YAML tiêu chuẩn.

> Đây là một mô hình chiến lược, không phải là tiêu chuẩn YAML.

Một máy chủ hiện tại sử dụng `disable-model-invocation: true`cho hàng chỉ dành cho con người và `user-invocable: false`cho dòng chỉ mô hình. mặc định là cả hai. Một máy chủ khác sử dụng `agents/openai.yaml`với `allow_implicit_invocation: false`để giữ cho cuộc gọi rõ ràng trong khi vô hiệu hóa lựa chọn ngầm. Đây là bộ điều chỉnh thời gian chạy.

> Một chủ nhà hiện tại `disable-model-invocation: true`Nói "chỉ con người"`user-invocable: false`biểu diễn " chỉ mô hình "行,默认两者皆可;另一个宿主用 `agents/openai.yaml`của `allow_implicit_invocation: false`Bảo trì điều chỉnh hiển nhiên 关掉隐式选择.

Những chi tiết gây nhầm lẫn là quan trọng:`user-invocable: false`không có nghĩa là "chương trình không thể sử dụng điều này". Nó loại bỏ cuộc gọi trực tiếp của người dùng trong máy chủ xác định nó. `disable-model-invocation: true`không có nghĩa là "nghệ năng bị vô hiệu hóa". Nó loại bỏ sự lựa chọn bắt đầu theo mô hình trong khi vẫn giữ cho truy cập rõ ràng của người dùng.

> Đó là một phần rất quan trọng:`user-invocable: false`Không giống như " mô hình không thể sử dụng nó " nó chỉ trong việc xác định chủ sở hữu của nó chuyển hướng trực tiếp người dùng sử dụng;`disable-model-invocation: true`Nó cũng không đồng nghĩa với "nghiện năng bị cấm" để loại bỏ các lựa chọn được khởi xướng, trong khi vẫn giữ lại truy cập của người dùng rõ ràng.

### Sự kêu gọi rõ ràng là danh tính đầu tiên.

Một cuộc gọi rõ ràng cung cấp danh tính trực tiếp:

```text
/release-readiness v2.4.0
```

hoặc:

```text
release-readiness check v2.4.0 without publishing
```

Tài liệu giao diện Codex hiện tại `/skills`cho việc lựa chọn và tên kỹ năng đơn giản trong các yêu cầu yêu cầu khai báo rõ ràng.`/skill-name`và mở rộng lập luận cụ thể cho máy chủ. Hình pháp chính xác, khả năng hiển thị menu, quy tắc trích dẫn và mở rộng biến thuộc về máy chủ.

> 现行 Codex 界面用 `/skills`Làm lựa chọn  sử dụng nghệ năng trong yêu cầu nghệ năng trong yêu cầu nghệ năng trong yêu cầu nghệ năng trong yêu cầu nghệ năng trong yêu cầu nghệ năng trong yêu cầu nghệ năng trong yêu cầu nghệ năng trong yêu cầu nghệ năng trong yêu cầu nghệ năng trong yêu cầu nghệ năng trong yêu cầu nghệ năng trong yêu cầu nghệ thuật nghệ thuật nghệ thuật nghệ thuật nghệ thuật nghệ thuật nghệ thuật nghệ thuật nghệ thuật nghệ thuật nghệ thuật nghệ thuật nghệ thuật nghệ thuật nghệ thuật nghệ thuật nghệ thuật nghệ thuật nghệ thuật nghệ thuật `/skill-name`和宿主专属参数展开――精确语法、菜单可见性、引号规则和变量展开都属于宿主──

Một yêu cầu rõ ràng vẫn thông qua chính sách. Chọn tên một kỹ năng không nên bỏ qua các quyền bị thiếu, hạn chế không gian làm việc, cửa phê duyệt hoặc cách ly thời gian chạy.

> 显式请求仍需过策略──点名一个技能不应绕过缺失权限──工作区限制──审批门禁或运行时隔离──

### Sự kêu gọi ngầm là mô tả trước tiên.

Đối với định tuyến ngầm, mô hình ban đầu nhìn thấy metadata danh mục thay vì toàn bộ cơ thể.

> Đối với các đường ẩn, mô hình ban đầu nhìn thấy là danh mục dữ liệu và không phải là văn bản chính xác hoàn chỉnh.

Thất yếu:

```yaml
description: Helps with releases.
```

Tự rộng quá:

```yaml
description: Use for release, version, package, build, deploy, publish, tag, changelog, GitHub, CI, or software tasks.
```

Giới hạn:

```yaml
description: Inspect an already prepared release candidate and produce a readiness report. Use when the user asks whether a version, tag, package, or image is ready to publish; do not use for ordinary build failures or feature development.
```

Phiên bản giới hạn có chứa:

1. **Capability:**kiểm tra một ứng cử viên đã chuẩn bị.
2. **Output:**báo cáo sẵn sàng.
3. **Positive boundary:**hỏi liệu một vật thể được phóng thích có sẵn không.
4. **Negative boundary:**Những công trình xây dựng và phát triển bình thường là không có tầm quan trọng.

Biên giới tiêu cực hữu ích khi hai kỹ năng gần nhau chia sẻ từ vựng.

> Có giới phiên bản chứa bốn yếu tố: 1) 能力 kiểm tra đã sẵn sàng 候选版本; 2) 输出就绪报告; 3) 正向边界询问发布工件是否就绪; 4) 负向边界普通构建与功能开发不在范围内;;

### Đường dẫn là phân loại với tùy chọn từ chối.

Để có kỹ năng`s`và yêu cầu`x`, tưởng tượng điểm của router:

```text
score(s, x) = capability_match + trigger_match + context_match - exclusion_match - ambiguity_penalty
```

Điểm số chính xác có thể là một quyết định LLM thay vì toán học. Nguyên tắc kỹ thuật vẫn giữ nguyên: sự lựa chọn nên vượt qua ngưỡng và kỹ năng cạnh tranh. Khi bằng chứng yếu, hãy kiềm chế.

> 精确打分可以由LLM 判断而非算术完成──但工程原则不变:选中必须同时赢过值和竞争技能;证据不足时就弃权(弃权)──

```figure
skill-routing-abstention
```

Đối với các kỹ năng có tác động cao, định tuyến ngầm có thể không phù hợp ngay cả khi có mô tả mạnh mẽ. Sử dụng chính sách chỉ dành cho con người khi chi phí của một dương tính giả vượt quá sự tiện lợi của việc lựa chọn tự động.

> Đối với kỹ năng ảnh hưởng cao, ngay cả khi mô tả rất mạnh, đường ẩn cũng có thể không phù hợp.

### Đáng đủ điều kiện phải đi trước thứ hạng.

> **【中文解读】**序列错误是路由实现最常见的 bug:先给所有发现的技能打分、选择最高分、再检查那一个技能的策略被禁的最高分会住本可入选的合法次高分──正确序列:先按请求角色和宿主适配器过资格,只对合格者打分,选择最强且过值者,无人合格或分数不足弃则权──例:`incident-triage`Nhưng chủ nhà của nó mở rộng sử dụng mô hình调用,`incident-review`0,55 và cho phép các router được`incident-review`Khi được chọn là ứng cử viên tốt nhất, chứ không phải là người được chọn.`incident-triage`、 từ chối 、 rồi dừng lại ∼ Đây là một thứ tự cũng đảm bảo rằng sự thay đổi chiến lược sẽ không thay đổi ý nghĩa của số điểm liên quan:

Đừng ghi được từng kỹ năng được phát hiện, chọn được điểm mạnh nhất, và sau đó kiểm tra chính sách của một kỹ năng.

Sử dụng thứ tự này cho định tuyến ngầm:

1. Bộ lọc phát hiện ra kỹ năng của người yêu cầu và bộ chuyển đổi chủ động.
2. Chỉ ghi điểm cho các ứng viên đủ điều kiện.
3. Chọn trận đấu đủ điều kiện mạnh nhất nếu nó xóa ngưỡng và các quy tắc mơ hồ.
4. Tránh khi không có ứng cử viên nào đủ điều kiện hoặc không có điểm số đủ mạnh.

Giả sử`incident-triage`điểm số`0.80`nhưng phần mở rộng host của nó vô hiệu hóa việc gọi mô hình. `incident-review`điểm số`0.55`và cho phép gọi mô hình.`incident-review`là ứng cử viên tốt nhất đủ điều kiện.`incident-triage`, phủ nhận nó, và dừng lại.

Việc sắp xếp này cũng giữ cho các thay đổi chính sách không thay đổi ý nghĩa của điểm số liên quan.

> Sự thay đổi này cũng cho phép thay đổi chiến lược không phải là thay đổi ý nghĩa của số điểm liên quan: đủ điều kiện xác định danh sách ứng cử viên, liên quan chỉ cho danh sách ứng cử viên xếp hạng.

### Các đánh giá định tuyến cần gần thất bại 路由评测 cần gần như không định mệnh mẫu

Các trường hợp tích cực chứng minh sự hồi tưởng:

```json
{"prompt":"Is version 2.4.0 ready to publish?","expected":"release-readiness"}
```

Những âm tính rõ ràng chứng minh sự chính xác cơ bản:

```json
{"prompt":"Explain rotary position embeddings.","expected":null}
```

Những thất bại gần sẽ làm lộ chất lượng giới hạn:

```json
{"prompt":"Why did today's package build fail?","expected":"build-diagnostics"}
```

Những cổ phiếu gần như bị bỏ lỡ `package`và `build`Một bộ định tuyến chỉ có những điểm tích cực rõ ràng và những điểm tiêu cực không liên quan sẽ đánh giá cao chất lượng.

> gần似未命中样本与发布技能共享 `package``build`词汇, nhưng thuộc về một dòng khác. Chỉ có một nhóm đường bộ gồm các mẫu hình chính xác rõ ràng và các mẫu hình không có liên quan.

### Các lập luận có ba biểu diễn.

Một lập luận triệu hồi vượt qua một số ranh giới:

```figure
skill-argument-boundaries
```

Ở mỗi ranh giới, giữ nguyên ý định mà không coi văn bản như mã.

- Các máy phân tích chủ quyết định tổng hợp lệnh và trích dẫn.
- Kỹ năng nhận được văn bản hoặc biến bị ràng buộc theo quy tắc chủ.
- Các hướng dẫn xác nhận các giá trị và mặc định yêu cầu.
- Một tool call chuyển đổi giá trị thành một schema được gõ và tái xác nhận chúng.

Đừng liên kết các lập luận nguyên liệu vào các lệnh shell. C prefer a script invoked with an argument vector or a typed MCP tool.

> Đừng đưa các tham số nguyên thủy vào shell 命令. 首选选选用参数向量调用脚本或有类型的MCP 工具.

### Việc gọi ứng dụng là sự dàn xếp rõ ràng.

Một sản phẩm có thể kích hoạt một kỹ năng bởi vì dòng công việc của nó đã biết loại nhiệm vụ. Ví dụ, một dịch vụ xem xét pull-request có thể tải trước `pull-request-risk-review`sau khi người dùng nhấn Review.

> 产品 có thể kích hoạt kỹ năng, vì quá trình của nó đã biết loại nhiệm vụ. Ví dụ: kéo- yêu cầu  đánh giá dịch vụ có thể được sử dụng trên người dùng nhấn  đánh giá  sau tải trước `pull-request-risk-review`

Điều này loại bỏ sự không chắc chắn định tuyến nhưng tạo ra sự phụ thuộc vào API thời gian chạy. Giữ bộ điều chỉnh đó bên ngoài cơ thể di động:

```figure
skill-host-adapter
```

Kỹ năng này nên vẫn dễ hiểu khi được mở bởi một khách hàng khác tuân thủ.

> Khi một khách hàng khác mở kỹ năng này, nó vẫn nên được đọc và sử dụng.

### Sự kêu gọi kỹ năng là một công cụ như cạnh.

Giả sử`release-readiness`yêu cầu `security-change-review`khi các tập tin phụ thuộc thay đổi.

Người gọi phải cung cấp:

- danh tính kỹ năng mục tiêu;
- một nhiệm vụ và các con đường tạo vật bị giới hạn;
- hợp đồng phản ứng dự kiến;
- Lý do của việc kêu gọi;
- một sự thất bại nếu không có;
- Quy tắc độ sâu tối đa hoặc chu kỳ.

```json
{
  "target_skill": "security-change-review",
  "task": "Review dependency changes in the candidate diff",
  "inputs": ["artifacts/release.diff"],
  "expected": "risk-report.json",
  "max_depth": 2
}
```

Kỹ năng thứ hai không được dán mù quáng vào kỹ năng đầu tiên. Người chủ quyết định làm thế nào để kích hoạt nó và liệu nó có chia sẻ ngữ cảnh, chạy trong một garpu, hoặc trả lại thông qua kết quả công cụ.

> Kỹ năng thứ hai sẽ không bị dán mù quáng vào thứ nhất. Người chủ quyết định làm thế nào để kích hoạt nó. Nó được chia sẻ trên các phân cổng, hoặc thông qua kết quả của công cụ trả lại.

### Chuyện sống của người chủ là cụ thể.

Sau khi kích hoạt, bộ phận kỹ năng có thể vẫn còn trong cuộc trò chuyện, được tóm tắt trong khi nén hoặc chạy trong một bối cảnh ủy quyền.

> Sau khi kích hoạt, kỹ năng chính thức có thể ở trong cuộc trò chuyện, được rút ngắn trong quá trình nén, hoặc được vận hành trong văn bản dưới đó trên ủy quyền.

Đừng viết một kỹ năng phụ thuộc vào giả định không thể nhìn thấy được trong suốt đời. Đặt các sản phẩm bền vững trong các tệp hoặc trạng thái đánh dấu, làm cho việc tái nhập an toàn, và nói ra những gì phải được tải lại sau khi bị gián đoạn.

> Đừng viết dựa vào kỹ năng giả định chu kỳ đời ẩn. Hãy viết lâu dài, đưa ra vào tài liệu hoặc có trạng thái kiểu nào đó, hãy viết lại vào an toàn, và viết lại những gì phải được tải lại sau khi gián đoạn.

```markdown
On resume, read `artifacts/release-readiness.json` if it exists.
Revalidate the candidate commit before continuing.
Do not repeat an external write whose idempotency key is already recorded.
```

## Hãy xây dựng nó.

> **【中文解读】** `code/main.py`Đặt chiến lược và thực hiện đường dẫn thành hai bộ điều chỉnh tách biệt:`CorePolicyAdapter`Chỉ nhận được ứng dụng các chiến lược cung cấp không mang bất kỳ chủ sở hữu mở rộng;`ExtensionPolicyAdapter`识别一组明确的宿主字段(如 `disable-model-invocation`(văn bản ghi là những gì đã thay đổi quyết định. Ý nghĩa của phân tách: nếu cùng một bộ phân tích cho tất cả các nguyên nhân trước 字段都赋义, nó sẽ đưa thời gian vận hành được xác định  nâng lên thành tiêu chuẩn giả mạo.

`code/main.py`thực hiện chính sách và định tuyến như các bộ chuyển đổi riêng biệt.

Mô hình bao gồm:

- `Actor`cho người, mô hình, nhân viên tự trị, ứng dụng, kỹ năng và người gọi sử dụng;
- `SkillMetadata`cho danh tính định tuyến;
- `InvocationPolicy`Đối với các mô hình người/mẫu;
- `InvocationRequest`và `InvocationDecision`cho các đầu vào và kết quả có thể theo dõi;
- `CorePolicyAdapter`cho hành vi di động mà không có phần mở rộng host;
- `ExtensionPolicyAdapter`cho các trường runtime được công nhận;
- `build_invocation_matrix(policy)`cho khung cảnh 2x2;
- `route_request(skills, request, adapter)`cho việc lọc đủ điều kiện trước khi xếp hạng, lựa chọn và từ chối liên quan.

Đi đi.

```bash
cd phases/13-tools-and-protocols/25-skill-invocation-and-routing
python3 code/main.py
python3 -m unittest discover -s code/tests -v
```

Demo in một matrix và quyết định cho mô hình con người rõ ràng, ngầm, đại lý tự trị, ứng dụng, kỹ năng-sự tạo thành, và kênh khai thác. Kết quả của nó cho thấy một kết hợp từ điển bị chặn trên được loại bỏ trước khi một lựa chọn thay thế đủ điều kiện được xếp hạng. Nó cũng bao gồm danh sách tên chính xác. Không cần thiết API mô hình. Các định tuyến xác định tồn tại để làm cho các ranh giới chính sách được kiểm tra, không phải để tuyên bố rằng sự phù hợp từ điển tái tạo định tuyến mô hình sản xuất.

### Tại sao bộ điều chỉnh lõi và bộ điều chỉnh mở rộng được tách biệt

Nếu một bộ phân tích gán ý nghĩa cho mỗi trường vật liệu trước được quan sát, nó lặng lẽ thúc đẩy các quy ước thời gian chạy thành một tiêu chuẩn giả.

> Nếu một bộ giải thích cho thấy mỗi phần trước của nó 字段都赋义, nó đã đưa nó vào hoạt động khi định  nâng lên thành tiêu chuẩn giả .

- `CorePolicyAdapter`sử dụng chỉ chính sách được cung cấp theo ứng dụng.`ExtensionPolicyAdapter`nhận ra một tập hợp rõ ràng của các trường chủ và ghi chép mà trường đã thay đổi quyết định.

> `CorePolicyAdapter`Chỉ sử dụng các chiến lược được áp dụng.`ExtensionPolicyAdapter`识别一组明确的宿主字段,并记录是哪个字段改变了决定──

## Hãy sử dụng nó. Hãy học cách sử dụng nó.

Viết một hợp đồng triệu tập trước khi xuất bản một kỹ năng:

```yaml
actors:
  human: allow
  model: deny
  application: allow
  skill: deny
explicit_name: release-readiness
arguments:
  candidate: required
  publish: fixed_false
ambiguity: ask_user
missing_dependency: stop
context:
  durable_state: artifacts/release-readiness.json
  max_composition_depth: 2
```

Hợp đồng này là tài liệu thiết kế cho các bộ điều chỉnh và thử nghiệm.`SKILL.md`Các vấn đề trước trừ khi một tiêu chuẩn đã rõ ràng chấp nhận nó.

> Đây là một hợp đồng cho các thiết kế và các tài liệu thử nghiệm.`SKILL.md`mặt trước.

## Chuyển nó đi.

Bài học này tạo ra những`skill-invocation-router`Nó bao gồm một tham chiếu mô hình gọi, một chính sách chủ host ví dụ và một CLI không thực hiện đánh giá một con người, mô hình, đại lý tự trị, ứng dụng, thành phần kỹ năng hoặc yêu cầu khai thác và trả lại quyết định JSON với kênh, bộ điều chỉnh, điểm số và lý do.

> 本课产 出 `skill-invocation-router`包: một quy định mô hình tham khảo, một ví dụ về chiến lược chủ nhà, cũng như một CLI không thực hiện bất cứ điều gì  đánh giá một nhân vật, mô hình, đại lý tự do, ứng dụng, skill set hoặc sử dụng                                                                                                                                                                                                                                   

CLI một yêu cầu là một cuộc thăm dò chính sách, không phải là đánh giá kích hoạt đầy đủ. Sử dụng thiết kế được dán nhãn tích cực và gần bị bỏ lỡ trong Bài học 27 để tính toán số lượng nhầm lẫn, độ chính xác, thu hồi và ổn định chạy lặp lại.

> 单请求 CLI là một cụm từ chiến lược, không phải là một đánh giá kích hoạt đầy đủ. Sử dụng mẫu thực của Bài học 27 + thiết kế nhãn gần như bị bỏ lỡ để tính toán số lượng mê, tỷ lệ chính xác, tỷ lệ triệu hồi và tính ổn định hoạt động lặp lại.

## Tập luyện.

1. Tạo tất cả bốn hàng của bộ vi mô hình/mô hình và viết một trường hợp sử dụng hợp pháp cho mỗi hàng.
2. Thêm kích hoạt chỉ ứng dụng vào `CorePolicyAdapter`Bằng chứng rằng người và người gọi mẫu vẫn bị từ chối.
3. Viết mười điểm gần như bị bỏ lỡ cho một kỹ năng triển khai.
4. Thêm một khoảng cách mơ hồ giữa hai điểm dẫn đầu.`ask`khi biên giới quá nhỏ.
5. Thêm độ thành phần tối đa cho các yêu cầu kỹ năng cho kỹ năng và phát hiện một chu kỳ hai kỹ năng.
6. Đưa ra cùng một bộ nhãn thông qua bộ chuyển đổi lõi và mở rộng.

## Từ khóa  Keyword

> 下表左列是术语、中列是"người thường nói"、右列是" thực tế nghĩa"── dễ nhất để bước vào hai dòng:`user-invocable`Đây là tiêu chuẩn không phải là tiêu chuẩn chính của chủ nhà.

| Term | What people say | What it actually means |
|---|---|---|
| Explicit invocation | "Slash command" | An actor supplies skill identity directly, subject to policy |
| Implicit invocation | "The model chooses" | A router selects from eligible catalog metadata based on task context |
| User-invocable | "Humans can use it" | A host-specific menu or direct-invocation property, not a core field |
| Model-invocable | "The agent can use it" | Eligibility for implicit model selection under host policy |
| Invocation adapter | "Frontmatter parser" | Code that maps a host's fields and APIs into a declared policy model |
| Near miss | "Hard negative" | A non-triggering request that resembles a skill's intended inputs |
| Abstention | "No skill selected" | A deliberate routing result when evidence is absent or ambiguous |

## Xem thêm 延伸阅读

- [Optimizing skill descriptions](https://agentskills.io/skill-creation/optimizing-descriptions)cho các tác động tích cực, tính cụ thể và đánh giá.
- [Evaluating skills](https://agentskills.io/skill-creation/evaluating-skills)cho thiết kế đánh giá kích hoạt và đầu ra.
- [OpenAI: Build skills](https://learn.chatgpt.com/docs/build-skills)cho các kiểm soát khai báo rõ ràng và ngầm của Codex hiện tại.
- [Claude Code skills](https://code.claude.com/docs/en/skills)cho một người chủ nhà `user-invocable`- `disable-model-invocation`, các lập luận và bối cảnh ủy quyền.

> 阅读顺序建议:先读优化-描述 掌握触发边界写法;再读评估- kỹ năng 学触发与输出评测设计;最后对照 Codex 与 Claude Code 两份宿主文档,看同一个策略维度在不同宿主中的字段名差异──
