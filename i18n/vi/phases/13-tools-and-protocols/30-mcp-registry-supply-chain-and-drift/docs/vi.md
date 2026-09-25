# MCP Registry Supply Chain: Admission, Drift, and Rollback  MCP Registration Center 

> Một mục đăng ký cho bạn biết một nhà xuất bản đã tuyên bố gì.

> **【中文解读】**Các mục của trung tâm đăng ký chỉ cho bạn biết" nhà phát hành tuyên bố gì"; sản xuất nhập cảnh (Production entry) để chứng minh là "bạn thực sự lấy lại gì, quan sát gì, phê duyệt gì, và có thể an toàn phục hồi gì"

>  **【前置】**Học tập trước:Phase 13 · 17(网关与注册中心官方注册登记的名称空间验证、网关在架构中的位置) vàPhase 13 · 18(生产认证OAuth 2.1 与凭证治理)。 本课是这两课的运维延伸: một máy chủ MCP 进入生产之前,证链如何审批、安装后漂移如何被发现、出路后如何回滚──本课基于MCP 2026-07-28 规范的`server/discover`

**Type:** Build | **类型:** 动手实践
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 13 · 17 (gateways and registries), Phase 13 · 18 (production authentication) | **前置知识:** Phase 13 · 17（网关与注册中心）、Phase 13 · 18（生产认证）
**Time:** ~90 minutes | **时间:** 约 90 分钟

## Mục tiêu học tập

- Việc xuất bản Registry riêng biệt, nguồn gốc gói, phát hiện thời gian chạy và phê duyệt địa phương.
  Trung文翻译:区分 Registry 发布、包来源证明 (来源证明) 、运行时发现与本地审批 这四件事――
- Kiểm tra không gian tên máy chủ MCP mà không tin vào tên trong hồ sơ của riêng nó.
  Trong một bản ghi tự mang tên trong hồ sơ, xác nhận MCP 服务器的命名空间.
- Pin ấn phẩm không thay đổi, nguồn thực hiện, nguồn gốc và bằng chứng mô tả trực tiếp.
  Trung文翻译:锁定(pin)不可变的发布记录、执行来源、来源证明与在线描述符证据──
- Khám phá thay đổi trạng thái đăng ký và biến động thời gian chạy sau khi nhập học.
  Trung ngữ翻译:在准入后检测注册中心状态变化与运行时漂移 (漂移) 
- Chuyển lại định tuyến sang phiên bản đã được chấp nhận trước đây mà không viết lại lịch sử.
  Trung ngữ翻译:把路由回滚到一个此前已通过准入的版本,且不改写历史──
- Giữ một sổ tay tuyển dụng rõ ràng, giải thích mọi quyết định.
  Trung ngữ翻译:维护一个防改(tamper-evident) 的准入账本(账本),能解释每一次决策──

## Vấn đề  vấn đề giới thiệu

Anh tìm thấy`com.example/inventory`Nó có thể được mô tả đúng, gói của nó tồn tại, máy chủ trả lời.`server/discover`- Tôi không biết.

> Anh tìm thấy nó trong trung tâm đăng ký.`com.example/inventory`                                                                                                                                                                                                                                                              `server/discover`

> **【中文解读】**"It's in the registration center" không phải là một sự thật, mà là bốn điều từ các cơ quan khác nhau: nhà phát hành chứng nhận, gói đăng ký trung tâm giao hàng, vận hành điểm tự kể, tổ chức phê duyệt. Đưa chúng vào "in the registration center" để có thể tin tưởng.

Đó không phải là một sự thật, mà là một chuỗi các sự kiện từ các cơ quan khác nhau:

1. Một nhà xuất bản xác thực cho một không gian tên đã gửi một bản ghi.
2. Một danh sách gói phục vụ một đồ tạo vật với một danh tính và tiêu hóa cụ thể.
3. Một điểm cuối đang chạy báo cáo phiên bản giao thức, khả năng, công cụ và thông tin máy chủ chẩn đoán.
4. Tổ chức của ông quyết định rằng sự kết hợp chính xác này được phép.

> Đây không phải là một sự thật, mà là một chuỗi sự kiện từ các cơ quan khác nhau: 1) Một nhà phát hành đã thông qua chứng chỉ không gian tên gọi đã gửi hồ sơ; 2) một trung tâm đăng ký đóng gói đã giao hàng có danh tính và bản tóm tắt cụ thể; 3) một điểm cuối trong hoạt động đã báo cáo phiên bản giao thức;

Việc sụp đổ những sự kiện đó thành it nằm trong registry, vì vậy hãy tin rằng nó tạo ra một điểm mù chuỗi cung ứng. Một ấn phẩm hợp lệ vẫn có thể bị lỗi thời. Một thẻ gói có thể chỉ ra một vật cổ vật bất ngờ nếu bạn không ghi dấu của nó. Một máy chủ có thể thêm một công cụ phá hủy sau khi xem xét. Một rollback có thể lặng lẽ chọn một phiên bản chưa bao giờ được chấp nhận.

> Để áp dụng những sự kiện này thành "đó đang ở trung tâm đăng ký, vì vậy có thể tin tưởng", bạn đã tạo ra một khu vực mù chuỗi cung ứng. Một bản đăng ký có hiệu lực vẫn có thể được đánh dấu là lỗi thời. Nếu bạn không khóa bản tóm tắt, gói nhãn có thể chỉ ra sản phẩm ngoài mục đích.

Đơn vị là một người kiểm soát nhập cảnh với bằng chứng ở mọi biên giới.

> 修复方式 là một bộ điều khiển nhập cảnh ở mỗi biên giới.

## Đăng ký là một chỉ số, không phải hệ thống chấp thuận của bạn.

Các MCP Registry chính thức lưu trữ dữ liệu siêu dữ liệu máy chủ.`server.json`ghi tên phiên bản máy chủ và tuyên bố một hoặc nhiều gói hoặc điểm cuối từ xa. Các quy tắc xuất bản thêm xác thực không gian tên, kiểm tra quyền sở hữu gói, các quy tắc đăng ký hạn chế và vị trí siêu dữ liệu nhà xuất bản hẹp.

> 官方 MCP Registry  lưu trữ là server元数据──它的 `server.json`记录为一个服务器版本命名,并声明一个或多个包或远端点――发布规则额外提供命名空间认证、包所有权检查、限限注册中心规则,以及一个狭窄的发行者元数据存储位置――

Các kiểm soát đó trả lời các câu hỏi về xuất bản. Chính sách sản xuất của bạn vẫn trả lời các câu hỏi về triển khai:

> Những kiểm soát này trả lời là "thế xuất" vấn đề.

| Boundary | Question | Evidence owner |
|---|---|---|
| Namespace | Was the publisher allowed to use this name? | Registry authentication plus your verified namespace input |
| Record | What did the publisher declare for this version? | Immutable `server.json` digest |
| Execution source | Which package or remote endpoint will execute? | Declared source fields, verified ownership result, transport, and trusted digest |
| Runtime | What does the endpoint expose now? | `server/discover` and tool descriptors |
| Admission | Did your policy approve this exact set? | Local pin and ledger entry |
| Operations | Is it still safe, and what can replace it? | Drift checks, status sync, health, and rollback route |

> **【中文解读】**Chế độ này là cấu trúc của toàn lớp: sáu biên giới, mỗi biên giới một vấn đề, một chứng cứ có người.`server.json`摘要), execution source question"实际执行的会是哪个包或端点",运行时问"端点现在暴露什么" ((证据是)`server/discover`Và các công cụ mô tả),准入问"Your strategy is rightly approved this group",运维问"It is now safe again?

>  **【类比】**Registry 像手机应用商店的"上架审核",你的入门系统像企业的MDM(移动设备管理) 装机审核。App 通过商店审核只说明"发行人身份合规、包没被偷换"",不代表"你的公司允许在办公设备上运行它"―npm/PyPI

Phiên bản schema Registry và phiên bản giao thức MCP là độc lập.`2025-12-11`schema server trong khi live server hỗ trợ MCP `2026-07-28`Đừng bao giờ suy luận về nhau.

> Registry's schema 版本与 MCP 协议版本是相互独立的──一条记录可能使用已发布的`2025-12-11`服务器 schema, còn trên mạng máy chủ hỗ trợ là MCP `2026-07-28`Đừng bao giờ đưa ra quyết định từ một đến một.

```figure
mcp-registry-admission
```

## 7 điều khiển trong 1 quyết định nhập học

> **【中文解读】**Một lần an toàn nhập cảnh cần phải chia 7 điểm kiểm soát để kết hợp thành một quyết định: 1) 命名空间验证 nhà phát hành có thực sự có quyền sử dụng tên này không; 2) nguồn拼音: source join)  tuyên bố về gói và thực tế lấy lại sản phẩm trên nhiều đoạn; 3) 锁定决策而非仅锁版本pin 里里有各层摘要; 4) 在线漂移检查对将真正接流的服务器做发现与工具描述符; 5) 注册中心状态是活态活态/衰退/删除; 6) 转滚路由恢复只选择准入和当前合格目标; 7) 额外进入账本哈哈链历史让验证已有七个小节目.

### 1. Thêm vào danh mục của bạn.

Tên đăng ký chính thức sử dụng không gian tên xác thực. Một tên miền được xác minh có thể lập bản đồ đến một tiền tố tên miền đảo ngược. Ví dụ, kiểm soát của `example.com`có thể thiết lập`com.example/*`- Tôi không biết.

> 官方 Registry's name using经过认证的命名空间── một miền đã được chứng nhận có thể được hiển thị như tên miền được chuyển đổi. Ví dụ: đối với `example.com`Quyền kiểm soát có thể được thiết lập.`com.example/*`

Không chấp nhận kiểm tra tiền tố chuỗi:

```python
server_name.startswith("com.example")
```

Điều đó cũng chấp nhận `com.exampleevil/tool`. Chia tên ở `/`, yêu cầu một con sưu tập không trống, và so sánh phân đoạn namespace chính xác. Quan trọng hơn, chuyển namespace xác minh vào nhập từ kết quả xác thực. Đừng lấy niềm tin từ hồ sơ không tin cậy.

> Chuyện này cũng sẽ được kiểm tra.`com.exampleevil/tool` Thực tế là theo`/`切分名字、要求 slug 非空,并对命名空间段做精确比较──更重要的是, để đưa kết quả xác nhận trong xác nhận đã được xác nhận trong namespace传入进入流程不要从未被信任的记录自推信──

Các namespace được hỗ trợ bởi GitHub và namespace được hỗ trợ bởi domain sử dụng các con đường xác thực khác nhau.

> GitHub 背书的命名空间和域名背书的命名空间走不同的认证路径──把两种路径都归结为一个准入输入:精确的、已验证的命名空间字符串──

### 2. Provenance tham gia

Đối với một bản ghi gói, tuyên bố và vật thể được lấy phải kết hợp trên các trường rõ ràng:

- kiểu hồ sơ gói
- Định dạng gói
- phiên bản gói
- Kết quả sở hữu được xác minh
- Downloaded artefact digest

> Đối với hồ sơ gói, tuyên bố và lấy lại sản phẩm phải được soạn thảo trên những đoạn rõ ràng này: loại trung tâm đăng ký gói, nhãn hiệu gói, phiên bản gói, kết quả sở hữu đã được xác minh, bản tóm tắt của sản phẩm.

Ngoài ra, xác nhận vận chuyển gói được tuyên bố. Một hồ sơ chỉ có một điểm cuối từ xa là hợp lệ và không thể bị từ chối vì thiếu gói. Đối với một nguồn từ xa, kết nối URL và loại vận chuyển được tuyên bố với chủ sở hữu điểm cuối được xác minh độc lập và một bản ghi của kết nối đáng tin cậy hoặc bằng chứng triển khai.

> Ngoài ra, phải có tuyên bố kiểm tra trong vận chuyển gói. Một điều chỉ mang hồ sơ về điểm cuối từ xa là hợp pháp, không thể bị từ chối vì "không có gói". Đối với nguồn từ xa, phải có URL của tuyên bố và loại vận chuyển, cùng với quyền sở hữu điểm cuối được kiểm tra độc lập, cũng như bản tóm tắt của chứng cứ kết nối đáng tin cậy hoặc triển khai.

Mã bài học hỗ trợ cả hai loại nguồn và hashes nguồn được chọn cùng với nguồn Registry, tên máy chủ, phiên bản Registry, ghi âm ghi âm và ghi âm chứng cứ.

> Bộ mã khóa này đồng thời hỗ trợ hai loại nguồn, và chọn nguồn được chọn với Registry Source, Server Name, Registry Edition, Record Summary và Testimonial Summary cùng nhau.

Đừng bao giờ chấp nhận một bản thu được cung cấp chỉ bởi vật cổ mà bạn đang cố gắng xác minh.

> Không bao giờ chấp nhận chỉ trích được cung cấp bởi "những sản phẩm bạn đang xác minh" cho mình.

### 3. Đặt quyết định, không chỉ phiên bản, không chỉ phiên bản.

Các phiên bản đăng ký là các công cụ xác định ấn phẩm độc đáo. Các metadata được xuất bản là không thể thay đổi. Một bản ghi thay đổi đòi hỏi một phiên bản mới. Việc phiên bản ngữ nghĩa được khuyến cáo, nhưng Registry không yêu cầu nó và không chấp nhận phạm vi phiên bản.

> Registry 版本 là bản đăng ký duy nhất. Các dữ liệu đã được đăng tải không thể thay đổi; ghi chép phải thay đổi nếu cần phải phát hành phiên bản mới.

Điều này có nghĩa là`^1.4`không phải là pin nhập học. Không phải là lastest. Một pin hữu ích chứa:

> Điều này có nghĩa là`^1.4`Không sẵn sàng vào pin, "hậu nhất" (最新) cũng không. Một pin hữu ích (有用的) 应包含:

```json
{
  "server": "com.example/inventory",
  "version": "1.0.0",
  "recordDigest": "...",
  "source": {"kind": "package", "registryType": "pypi"},
  "sourceDigest": "...",
  "toolsetDigest": "...",
  "provenanceDigest": "...",
  "registryStatus": "active"
}
```

Đặt nhiều lớp cho phép bạn xác định ranh giới thay đổi. Một thay đổi ghi nhớ trong cùng phiên bản Registry là một sự cố tính toàn vẹn Registry. Một thay đổi ghi nhớ nguồn dưới cùng một phối hợp gói hoặc triển khai từ xa là một sự cố tính toàn vẹn của nguồn thực thi.

> 锁定多层,你才能定位是哪边界变了:Registry 版本不变而记录摘要变了,是Registry 完整性故障;包坐标或远程部署不变而来源摘要变了,是执行来源完整性故障;工具集摘要变了,就是运行时漂移;; giá trị của pin đa tầng không nằm trong "đóng được", mà nằm trong một lớp mà báo cáo cảnh sát có thể xác định được mất đi.

### 4. Khám phá hoạt động trực tiếp

Đăng nhập nên quan sát máy chủ thực sự sẽ nhận lưu lượng truy cập.`server/discover`, liệt kê hoặc bằng cách khác nhận được các mô tả công cụ được phơi bày thông qua con đường đáng tin cậy của bạn, và xác minh:

> 准入应观察那将真正接收流量的服务器――调用`server/discover`, qua các đường dẫn đáng tin cậy của bạn để liệt kê hoặc bằng cách khác để có được các mô tả công cụ được phơi bày, sau đó xác minh:

- `2026-07-28`là trong `supportedVersions`
- tất cả các khả năng cần thiết tại địa phương đều có mặt
- Mỗi mô tả công cụ có bề mặt danh tính và sơ đồ cần thiết
- tiêu hóa mô tả bình thường phù hợp với pin được chấp nhận trong kiểm tra sau đó

> 验证四件事:`2026-07-28`Trong `supportedVersions`里;(2) 所有本地必需能力都在;(3) Mỗi mô tả công cụ có yêu cầu về danh tính và cấu trúc sơ đồ;(4) Trong kiểm tra tiếp theo, quy định sau đó mô tả mô tả sơ lược và nhập pin 一致──

Kết quả tùy chọn `_meta["io.modelcontextprotocol/serverInfo"]`giá trị là bản ghi tự báo cáo hiển thị, nhật ký và điều chỉnh kết cấu. ghi lại nó như bằng chứng chẩn đoán, nhưng không bao giờ sử dụng nó để thiết lập không gian tên, sở hữu gói, sở hữu điểm cuối, nhập, hoặc bất kỳ quyết định bảo mật nào khác.`serverInfo`- Tớ gọi là ngoài `_meta`không phải là lĩnh vực hợp đồng và không nên được quảng bá thành bằng chứng chẩn đoán.

> Kết quả `_meta["io.modelcontextprotocol/serverInfo"]`Giá trị của nó là hiển thị của máy chủ tự kể, nhật ký và điều tra trên các nội dung dưới đây. Hãy ghi nhận nó như bằng chứng chẩn đoán có thể, nhưng không thể sử dụng nó để xác định không gian đặt tên, quyền sở hữu gói, quyền sở hữu điểm kết thúc, quyền vào hoặc bất kỳ quyết định an ninh nào khác.`_meta` ngoài `serverInfo`直接别名不是契约字段,不应升级为诊断证券──

Chỉ bình thường hóa các trường mà thứ tự không có ý nghĩa. Mô hình sắp xếp danh sách công cụ bằng tên ổn định trước khi hashing, vì vậy thay đổi thứ tự danh sách không gây ra trục xuất. Nó không loại bỏ các trường mô tả. Một công cụ mới, thay đổi sơ đồ, thay đổi mô tả hoặc ghi chú mới thay đổi pin.

> Chỉ làm quy định các đoạn của "định dạng vô nghĩa". Ví dụ: trong trường hợp của Haci trước, thay đổi thứ tự của danh sách không gây ra sự di chuyển; nhưng nó không bỏ qua mô tả các đoạn của các phần mới, các đoạn mới, các đoạn mới, các đoạn mới, các đoạn mới, các đoạn mới, các đoạn mới.

Các mẫu xử lý các mô tả sai dạng và bất kỳ thay đổi tiêu hóa mô tả nào như là trôi dạt, cách ly pin, loại bỏ tuyến đường hoạt động của nó và chặn phiên bản đó như mục tiêu quay trở lại.

> Ví dụ: 形描述符和任何描述符摘要变化都当作漂移:隔离(quarantine)  pin này、摘除其活跃路由、并把这个版本拉入回滚黑单――:                                                                                                                                                                                                                                     

> **【中文解读】**Chương 4  Điều khiển là cái nhìn cốt lõi của toàn lớp: kiểm tra chuỗi cung ứng không phải là một động tác một lần. Sau khi kiểm tra máy chủ qua ̇ trong quá trình vận hành, mặt công cụ cũng có thể thay đổi ̇ đây là thời gian vận hành漂移 đối phó với giai đoạn 13 · 15 của các công cụ đưa vào trường hợp ma túy.

### 5. Tình trạng đăng ký là trạng thái trực tiếp

Registry API gắn một mức độ phản ứng `_meta`đối tượng bên cạnh mỗi hồ sơ máy chủ. Các trường quản lý Registry sống dưới `_meta["io.modelcontextprotocol.registry/official"]`- Đưa câu trả lời đi.`_meta`phản đối việc nhận và đọc `_meta["io.modelcontextprotocol.registry/official"].status`- Một cái trực tiếp`_meta.status`giá trị không phải là hình dạng dây chính thức. Đừng nhầm lẫn dữ liệu siêu dữ liệu phản hồi với bản ghi bản bản `_meta`- Tình trạng có thể là:

> Registry API trong mỗi server ghi lại bên cạnh kèm theo một lớp đáp ứng `_meta`đối tượng:  регистр 管理的字段位于 `_meta["io.modelcontextprotocol.registry/official"]`之下.`_meta`đối tượng truyền vào quá trình nhập học,读取 `_meta["io.modelcontextprotocol.registry/official"].status` trực tiếp `_meta.status`值不是官方线形态. Đừng để lại dữ liệu phản ứng với bản đăng ký của chính mình.`_meta`混为一谈.

- `active`: được trả theo mặc định và đủ điều kiện cho nhập học tại địa phương
- `deprecated`: vẫn có thể phát hiện với một cảnh báo, nhưng không còn một lựa chọn tự động an toàn
- `deleted`: ẩn theo mặc định trong khi hồ sơ lịch sử của nó vẫn có sẵn thông qua các lượt xem bị xóa hoặc tăng

> 三种状态:`active`(默认返回,可进入本地准入)`deprecated`(Tại còn được phát hiện nhưng có cảnh báo, không còn là tự chọn an toàn)`deleted`(默认隐藏, nhưng lịch sử vẫn có thể được xóa hoặc tăng lượng xem thu được)

Tích hợp trạng thái sau khi nhập. Nếu một phiên bản hoạt động trở nên lỗi thời hoặc bị xóa, hãy kiểm soát pin của nó và ngừng định tuyến công việc mới cho nó. Giữ bằng chứng. Việc xóa khỏi danh sách mặc định không phải là quyền xóa dấu vết kiểm toán của bạn.

> 准入后要持续同步状态――如果一个活跃版本变过时或删除,就隔离它 pin、停止将新工作路由给它――但证据要保留从默认列表中消失,并不是让你抹掉审计轨迹的许可――

Các metadata tùy chỉnh được cung cấp bởi nhà xuất bản chỉ thuộc về `_meta.io.modelcontextprotocol.registry/publisher-provided`trong một bản ghi xuất bản. Các metadata phản hồi được quản lý bởi Registry là riêng biệt. Đừng để cho một nhà xuất bản đặt vị trí chính thức của riêng mình.

> DATA tự định của nhà phát hành chỉ được đặt trong hồ sơ phát hành `_meta.io.modelcontextprotocol.registry/publisher-provided`之下. ・Registry 管理的响应元数据与之分离. ―绝不让发行人自己设置自己的官方状态. ―

### 6. Rollback nghĩa là khôi phục đường.

Một ấn phẩm không thay đổi không được chỉnh sửa trong quá trình quay lại. Rollback chọn một pin được chấp nhận trước đây, hiện có đủ điều kiện và thay đổi tuyến đường hoạt động.

> Chuyển lại sẽ không được chuyển đổi ghi chép xuất bản không thể thay đổi. Chuyển lại là chọn một pin đã sẵn sàng trước đây, hiện tại vẫn đủ điều kiện, sau đó chuyển đổi đường hoạt động.

Một mục tiêu an toàn phải:

1. Có hồ sơ nhập học đầy đủ.
2. Còn có trạng thái đăng ký hoạt động theo chính sách của bạn.
3. Không được cách ly bởi thời gian chạy hoặc bằng chứng an ninh.
4. vẫn được giải quyết cho gói được gắn và thiết lập mô tả trực tiếp.
5. Tham khảo sức khỏe hiện tại.

> Mục tiêu của an toàn phải: 1) Có một bài đăng đầy đủ về nhập cảnh; 2) Trong kế hoạch của bạn Registry  trạng thái vẫn hoạt động; 3) Không được vận hành hoặc chứng minh an toàn tách biệt; 4) vẫn có thể phân tích đến pin 住 的包和在线描述符集; 5) thông qua kiểm tra sức khỏe hiện tại.

Các mẫu tập trung vào ba điều kiện đầu tiên. Một người hòa giải thực sự nên lấy lại gói và kiểm tra lại điểm cuối trực tiếp trước khi kích hoạt.

> Ví dụ tập trung trước 3 điều kiện.

### 7. Thêm sổ ghi nhận.

Một cơ sở dữ liệu nhập học cho biết hoạt động của người nào.

> 准入数据库 nói là "tì giờ gì đang hoạt động";账本(ledger) giải thích là "why"―

Mỗi mục nhập mẫu chứa một chuỗi, thời gian, sự kiện, máy chủ, phiên bản, kết quả, lý do, bằng chứng, hash mục nhập trước đó và hash của riêng nó.

> Mỗi bài viết trong ví dụ bao gồm các mục đầu tiên, thời gian, sự kiện, máy chủ, phiên bản, kết luận, nguyên nhân, chứng cứ, mục đích của bài viết trước và chính bản thân của mình.

Điều này là rõ ràng, không phải là phép thuật chống vi phạm. Các sổ cái định kỳ đầu vào một miền tin cậy riêng biệt, chẳng hạn như dữ liệu bán tựa được ký hoặc lưu trữ một lần viết. Giới hạn ai có thể thêm vào. Giữ mã thông tin ủy quyền, thông tin tin tin tin tin gói, các lập luận công cụ và dữ liệu điểm cuối riêng tư ra khỏi bằng chứng.

> Đây là "có thể chứng minh" (đáng rõ ràng), không phải là "được chứng minh") (được chứng minh) (được chứng minh) (được chứng minh là có thể chứng minh) (được chứng minh là có thể chứng minh) (được chứng minh là có thể chứng minh) (được chứng minh là có thể chứng minh) (được chứng minh là có thể chứng minh là có thể chứng minh là có thể chứng minh là có thể chứng minh là có thể chứng minh là có thể có chứng minh là có thể có chứng minh).

## Hãy xây dựng nó.

Bộ điều khiển chạy được `code/main.py`Nó chỉ sử dụng thư viện tiêu chuẩn Python.

> 可运行的控制器在 `code/main.py`, chỉ sử dụng Python 标准库──

Bắt đầu với sự chứng minh hữu hạn:

```bash
cd phases/13-tools-and-protocols/30-mcp-registry-supply-chain-and-drift
python3 code/main.py
```

Cuộc biểu tình thực hiện năm hoạt động:

1. Hãy thừa nhận`1.0.0`với không gian tên phù hợp, nguồn gốc gói, giao thức, khả năng và công cụ.
2. Hãy thừa nhận`1.1.0`và làm cho nó hoạt động.
3. Nhận thấy một công cụ xóa bất ngờ trong thời gian chạy.
4. Xem trạng thái Registry của `1.1.0`trở thành`deprecated`- Tôi không biết.
5. Khôi phục đường dẫn cho các vẫn được chấp nhận `1.0.0`Đèn.

> 演示的五个操作:准入 `1.0.0`(命名空间、包 provenance、协议、能力、工具全部匹配);准入 `1.1.0`Không được cài đặt để hoạt động; quan sát khi chạy một không ngờ xóa  công cụ; quan sát Registry `1.1.0`                                                                                                                                                                                                                                                              `deprecated`; đưa đường trở lại cho đến khi vẫn còn trong trạng thái đã sẵn sàng `1.0.0`Pin

Hình dạng dự kiến:

```json
{
  "admitted": [true, true],
  "driftAllowed": false,
  "rollbackAllowed": true,
  "activeVersion": "1.0.0",
  "ledgerValid": true
}
```

Đọc việc thực hiện theo thứ tự này:

> 预期输出形状:两次准入都成功`admitted: [true, true]`),运行时漂移被拒绝路由`driftAllowed: false`), quay lại được phép`rollbackAllowed: true`),活跃版本回到 `1.0.0`,账本校验通过──按以下顺序阅读实现:

1. `namespace_for_domain()`và `namespace_matches()`xác định chính xác quyền đặt tên.
2. `digest()`và `normalized_tools()`tạo ra bằng chứng xác định.
3. `RegistryAdmissionController.admit()`kết hợp với xuất bản, nguồn gốc, thời gian chạy và chính sách.
4. `check_live()`so sánh một quan sát mới với pin.
5. `observe_registry_status()`Các phiên bản cách ly có trạng thái đăng ký thay đổi.
6. `rollback()`chỉ kích hoạt một mục tiêu đủ điều kiện trước đây được chấp nhận.
7. `AdmissionLedger.verify()`phát hiện ra những thay đổi trong lịch sử ghi lại.

## Hãy sử dụng nó để thực hiện

Đặt bộ điều khiển giữa phát hiện và định tuyến:

> Đặt thiết bị điều khiển vào giữa phát hiện và đường dẫn:

```text
Registry sync -> artifact verifier -> live discovery -> admission controller -> route table
                                               |                 |
                                               v                 v
                                          evidence store    admission ledger
```

Sử dụng danh tính riêng biệt cho các công việc này. Một nhân viên đồng bộ hóa Registry cần truy cập đọc đến metadata. Một xác minh artefact cần truy cập lấy gói. Một người đồng bộ đường cần quyền để kích hoạt một pin được phê duyệt. Không ai trong số họ cần tất cả các giấy chứng nhận.

> Để làm việc này sử dụng các danh tính phân biệt giữa nhau. Registry cùng công nhân chỉ cần quyền đọc dữ liệu; sản phẩm chứng minh chỉ cần gói nắm quyền; đường dẫn công giải chỉ cần kích hoạt được phê duyệt pin. Không một vai trò cần có toàn bộ giấy phép.

Làm cho thông báo triển khai rõ ràng. Từ chối  nghĩa là chính sách bằng chứng đã được thông qua. Active  nghĩa là tuyến đường hiện chọn nó.  Quarantine  nghĩa là nó không thể nhận được công việc mới. Superseded  nghĩa là một phiên bản khác được chấp nhận đang hoạt động. Đừng mã hóa tất cả bốn ý nghĩa trong một tiếng Boolean.

> 让发布状态显式化:"Tuyển thuận"(已批准)表示证据通过策略;"Active"(活跃)表示路由当前选中的是它;" Quarantained"(已隔离)表示它不能再接收新工作;"Superseded"(已取代)表示另一个已准备版本处于活跃――不要把这四层含义塞进一个布尔──

Thử nhập trước khi phơi bày một máy chủ trong `tools/list`Nếu không, khách hàng có thể phát hiện ra một công cụ trong khoảng cách giữa việc xuất bản và đánh giá chính sách.

> Trong khi máy chủ bị lộ ra`tools/list`之前先完成准入──否则客户端可能在"已发布"和"策略已评估"之间的空窗期里发现并调用一个工具──

> **【中文解读】**Sử dụng nó một phần cho ba điểm sản xuất:流水线各环节用独立身份 (được sử dụng như một thành phần bị rơi trong tình trạng mất toàn线); xuất bản trạng thái bằng bốn từ thay vì một cái lề (được chấp thuận/Active/ Quarantined/Superseded có ý nghĩa khác nhau); nhập phải được thực hiện trước khi`tools/list`暴露 (堵住发布与审批之间的发现空窗) . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

## - Bác sĩ, tôi đã làm việc trong phòng thí nghiệm tương tác.

Bạn sẽ xem một ranh giới thất bại một lúc.

> Bạn sẽ từng nhìn thấy mỗi biên giới là như thế nào thất bại.

### Phòng thí nghiệm A: Vụ nổ không gian tên

Mở một shell Python từ thư mục mã:

```bash
cd phases/13-tools-and-protocols/30-mcp-registry-supply-chain-and-drift/code
python3 -q
```

Rồi chạy:

```python
from main import namespace_matches
namespace_matches("com.example/inventory", "com.example")
namespace_matches("com.exampleevil/inventory", "com.example")
```

Kết quả đầu tiên là`True`; thứ hai là `False`Thay thế so sánh chính xác bằng `startswith`và quan sát tại sao tên thứ hai vượt biên giới.

> Kết quả đầu tiên là:`True`, thứ hai là`False`                                                                                                                                                                                                                                                              `startswith`, quan sát cái tên thứ hai vì sao có thể vượt qua biên giới.

### Phòng thí nghiệm B: Drift mô tả  B: Drift mô tả

```python
from main import *
times = iter(f"2026-08-21T12:00:{n:02d}+00:00" for n in range(10))
c = RegistryAdmissionController(clock=lambda: next(times))
meta = {OFFICIAL_META_KEY: {"status": "active"}}
c.admit(sample_record("1.0.0"), meta, "com.example", evidence_for("1.0.0"), sample_live("1.0.0"))
c.check_live("com.example/inventory", "1.0.0", sample_live("1.0.0", True))
```

Kiểm tra lý do và trạng thái đường. Tài liệu gói và Registry không thay đổi. Bề mặt công cụ chạy đã thay đổi, vì vậy người điều khiển đã kiểm định và vô hiệu hóa pin.

> 检查原因 和路由状态:包与注册 记录都没变, thay đổi là khi vận hành công cụ mặt 于是控制器隔离并停用这个. Đây là lý do tại sao chuỗi cung ứng phải tiếp tục tồn tại sau khi cài đặt.

### Phòng thí nghiệm C: trạng thái và quay lại

Hãy thừa nhận`1.1.0`, đánh dấu nó đã lỗi thời, và thử cả hai mục tiêu quay lại:

```python
c.admit(sample_record("1.1.0"), meta, "com.example", evidence_for("1.1.0"), sample_live("1.1.0"))
c.observe_registry_status("com.example/inventory", "1.1.0", "deprecated")
c.rollback("com.example/inventory", "1.1.0", "unsafe retry")
c.rollback("com.example/inventory", "1.0.0", "restore known release")
c.ledger.verify()
```

Mục tiêu bị cách ly bị từ chối, pin hoạt động trước được chấp nhận, sổ cái vẫn còn hợp lệ.

> Được tách rời trở lại mục tiêu được từ chối; còn sớm hơn hoạt động pin được chấp nhận; sổ sách học tập vẫn thông qua.

## Phòng thí nghiệm tập luyện.

Tăng bộ điều khiển với cổng chấp thuận hai người.

> 给控制器扩展一道双人审批门 (một cửa phê duyệt hai người)

> **【中文解读】**进阶练把第7条控制升级为"破坏性工具必须两人审批":审批必须以签名证引用的形式存储,不能是 pin 里可变的名字;工具集出现`destructiveHint: true`Trong quá trình kiểm tra, yêu cầu hai loại thẩm định khác nhau; tái kiểm tra bị từ chối; khi phê duyệt không hoàn thành, nỗ lực nhập nhập ban đầu cũng phải được giữ trong sổ sách.

Yêu cầu:

- Cung cấp lưu trữ như tham chiếu bằng chứng đã ký kết, không phải tên thay đổi trong pin.
- Cần hai danh tính kiểm tra viên khác nhau cho một bộ công cụ chứa một công cụ với `destructiveHint: true`- Tôi không biết.
- Tránh nhận dạng người xem trùng lặp.
- Giữ nỗ lực nhập học ban đầu trong sổ cái khi phê duyệt chưa đầy đủ.
- Thêm các thử nghiệm cho 0, một, hai lần phê duyệt và hai lần phê duyệt khác nhau.
- Đừng ghi lại chữ ký, giấy chứng nhận, hoặc các đối số công cụ riêng tư đầy đủ.

Thành công có nghĩa là một công cụ phá hủy không thể hoạt động cho đến khi cả hai danh tính chấp thuận bản ghi chính xác, gói và bộ công cụ.

> Các tiêu chuẩn thành công: Trước khi cả hai chức năng đều phê chuẩn bản ghi chép chính xác đó, bản ghi gói và tập hợp công cụ, các công cụ phá hoại không thể hoạt động được.

## Thuật vật được vận chuyển.

Bài học này sẽ đi theo `outputs/skill-mcp-registry-admission.md`Sử dụng nó như một sổ chạy phẳng, có thể sử dụng lại khi xem xét phiên bản Registry mới hoặc điều tra trôi. Nó xác định các đầu vào, quy tắc từ chối, gói bằng chứng, kết hợp trạng thái và chứng minh quay lại mà không phụ thuộc vào tên lớp mẫu.

> 本课附带 `outputs/skill-mcp-registry-admission.md` Khi đánh giá một Registry mới  phiên bản hoặc cuộc khảo sát漂移, hãy coi nó như một 平、可复用 runbook 使用── nó xác định nhập, từ chối quy tắc, chứng thực gói, trạng thái đối với chứng minh và quay lại, và không phụ thuộc vào tên trong mã ví dụ.

## Hãy kiểm tra.

> **【中文解读】**验收清单逐条过:形似前的命名空间被精确边界拒绝;只有官方命名空间的登记处 状态能让版本合格;未验证或不匹配的包与远程证书被拒绝;发行者元数据冒充不了登记处 管理元数据;工具顺序规范化但不掩盖描述符变化;形的包和工具结构安全拒绝;`serverInfo`始终只是诊断、不提供准入权威;描述符漂移会隔离、停止使用并封锁该的回滚;状态变化隔离活活;回滚不出被隔离或未知版本;账本改被检测到──

Tiến hành trình chứng minh và bộ xác định:

```bash
cd phases/13-tools-and-protocols/30-mcp-registry-supply-chain-and-drift
python3 code/main.py
python3 -m unittest discover -s code/tests -v
```

Việc kiểm tra phải chứng minh:

- ranh giới không gian tên chính xác từ chối các tiền tố giống nhau
- Chỉ có trạng thái Registry có tên chính thức mới có thể làm cho một phiên bản đủ điều kiện
- gói không được xác minh hoặc không phù hợp và bằng chứng từ xa bị từ chối
- Các metadata của nhà xuất bản không thể giả bộ như các metadata được quản lý bởi Registry
- sắp xếp công cụ được bình thường hóa mà không che giấu các thay đổi mô tả
- các cấu trúc gói và công cụ bị biến dạng bị từ chối an toàn
- `serverInfo`vẫn là chẩn đoán và không bao giờ cung cấp cho cơ quan nhận
- description drift quarantine, deactivates và blocks rollback to the pin
- Thay đổi trạng thái pin hoạt động kiểm dịch
- rollback không thể chọn phiên bản bị cách ly hoặc không biết
- bị thao túng sổ cái được phát hiện

## Các chế độ sản xuất thất bại

> 下表三列: thất bại, vì sao xảy ra, cần thiết đáp ứng. Đường cao nhất: cùng gói坐标 trở lại 节新字节 ((可变上游或被攻陷的分发道停止激活,保留两份摘要,调查抓取边界); 回滚目标从未通过准入; 回滚目标从未通过准入; 回滚目标从未通过路由控制和审批状态; 回滚拒绝断绝; 回滚目标重新进入; 账本被全重写后仍在本地通过; 哈希链外部没有点将签名本头发布到独立信任账域)

| Failure | Why it happens | Required response |
|---|---|---|
| Name looks valid but namespace was never authenticated | Policy trusted record text | Reject until a trusted namespace verifier supplies the exact prefix |
| Same package coordinate returns new bytes | Mutable upstream or compromised distribution | Stop activation, retain both digests, investigate the fetch boundary |
| “Latest” changes without review | Floating selection escaped the pin | Resolve only exact admitted versions and digests |
| New tool appears after approval | Runtime drift or a different deployment | Quarantine the route and capture a fresh descriptor observation |
| Deprecated version remains active | Status sync is missing or delayed | Reconcile status on a schedule and before activation |
| Deleted record disappears from default sync | Client requested only active records | Use incremental or deleted-aware reconciliation and preserve local history |
| Rollback target was never admitted | Route control and approval state are disconnected | Refuse rollback and run a new admission for the target |
| Ledger verifies locally after an attacker rewrites all entries | Hash chain has no external anchor | Publish signed ledger heads to a separate trust domain |
| Evidence contains bearer tokens or tool arguments | Logging copied whole requests | Redact at collection time and store only the minimum proof |

## Quy tắc hoạt động

Câu trả lời xuất bản có thể danh tính này xuất bản tên này? Câu trả lời nhận Chúng ta sẽ thực hiện hiện hiện vật chính xác này và phơi bày hành vi chính xác này? Giữ những quyết định đó tách biệt, gắn mỗi liên kết, và làm cho rollback chọn bằng chứng thay vì trí nhớ.

> 发布 trả lời là "This Identity Can Publish This Name?" 进入 trả lời là "Chúng ta sẽ thực hiện sản phẩm chính xác này 暴露 chính xác hành vi này ư?" chia hai quyết định này ra, khóa mỗi lần拼接, để quay lại dựa trên bằng chứng thay vì ký ức để lựa chọn.

## Xem thêm 延伸阅读

- [Official Registry server.json requirements](https://github.com/modelcontextprotocol/registry/blob/main/docs/reference/server-json/official-registry-requirements.md)
- [Official Registry OpenAPI contract](https://registry.modelcontextprotocol.io/openapi.yaml)
- [MCP 2026-07-28 server discovery](https://modelcontextprotocol.io/specification/2026-07-28/server/discover)
