# Xây dựng khách hàng MCP: Khám phá, định tuyến, và Dual-Era Fallback  Xây dựng khách hàng MCP  Khám phá 路由与双时代回归

> Một khách hàng MCP hiện đại lặp lại hợp đồng của mình trên mọi yêu cầu. Quyết định tương thích khó khăn nhất của nó là biết khi nào máy chủ cũ thực sự cũ và khi nào máy chủ hiện đại đang báo cáo một lỗi có thể sửa chữa.

> **【中文解读】**现代 MCP 客户端在每请求重复携带自己的契约 (契约) 版本、能力、身份) ⋅ nó khó nhất quyết định là兼容性判断:对端到底是"真旧" (trên kết thúc là "trên kết thúc là "trên kết thúc")  chỉ bắt đầu 握手的老服务器), hoặc"现代服务器在报告一个可修正的错误" (của các máy chủ hiện đại đang báo cáo một lỗi có thể sửa chữa).

> **【拓展：MCP 客户端→Agent 编排核心】**MCP 客户端 là cốt lõi của Agent  chủ nhà. Claude Desktop、Cursor 等都同时 tải nhiều máy chủ MCP 服务器(文件系统、Postgres、GitHub......), đưa danh sách công cụ hợp并后交给模型。2026-07-28 让稳态更简单(每请求自包含), nhưng để khởi động hơn 微妙四种对端形态(现代/报版错/没听到发现/沉默等) chủ yếu phải dựa vào "运营图 + 正向协议证据" để phân chia, chứ không phải làm mọi việc tìm kiếm thất bại trong phiên bản cũ.

>  **【前置】**学本节前请先掌握:(1) Giai đoạn 13 · 07(Construction MCP 服务器)`server/discover`、 từng yêu cầu từ dữ liệu`resultType`Với các gợi ý lưu trữ; 2) Phase 13 · 06 của mô hình yêu cầu không trạng thái với JSON-RPC 信封; 3) Python có thể调用 đối tượng / quay调模拟传输层的方式(本课用进程内同仁函数代替真实子进程)

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 13, Lesson 07 | **前置知识:** Phase 13, Lesson 07
**Time:** ~85 minutes | **时间:** ~85 分钟

## Mục tiêu học tập

- Xây dựng mọi MCP `2026-07-28`yêu cầu với các metadata hiện tại.
  中文翻译:为每个 MCP `2026-07-28`Xin hãy xây dựng mang theo các dữ liệu của báo cáo.
- Khám phá máy chủ stdio với `server/discover`và chọn một phiên bản hỗ trợ lẫn nhau.
  中文翻译:用 `server/discover`探测 stdio 服务器并选定双方都支持的版本──
- Cho phép một cuộc thăm dò di sản giới hạn chỉ cho các đồng nghiệp được liệt kê rõ ràng.
  Trung ngữ翻译: chỉ cho một người được phép tham gia vào danh sách trắng một lần có giới hạn.
- Hãy chấp nhận một kỷ nguyên thừa kế chỉ sau khi xác nhận một điều tích cực `initialize`kết quả cho một sửa đổi được hỗ trợ.
  Trung ngữ翻译: chỉ có trong chứng nhận được hỗ trợ sửa đổi phiên bản`initialize`Kết quả sau,才 chấp nhận thời đại cũ.
- Thủy lại danh sách các công cụ xác định học mà không bị va chạm.
  Trung文翻译:合并确定性工具列表而不静默覆盖命名冲突。
- Đường dẫn cuộc gọi đến người đồng nghiệp sở hữu mỗi công cụ mà không phát minh ra các phiên giao thức.
  Trung ngữ翻译:把调用路由到拥有该工具的对端,且不发明协议会话.

## Vấn đề  vấn đề giới thiệu

Một máy chủ đại lý thường nói chuyện với nhiều máy chủ MCP. Nó phải phát hiện từng máy chủ, hợp nhất các danh mục công cụ, giải quyết tên trùng lặp, đường dẫn gọi và phục hồi khỏi sự thất bại giao thông.

> Một đại lý chủ nhà thường giao tiếp với nhiều máy chủ MCP. Nó phải tìm thấy mỗi máy chủ. Nó phải tìm thấy danh sách công cụ. Nó phải giải quyết các vấn đề về tên gọi.

- `2026-07-28`sửa đổi làm cho trạng thái ổn định đơn giản hơn vì mỗi yêu cầu tự chủ. Sự tương thích làm cho khởi động tinh tế hơn.

> `2026-07-28`修订让稳态更简单, vì mỗi yêu cầu tự chứa.

- một máy chủ hiện đại hỗ trợ phiên bản được ưa thích;
  Trung ngữ翻译:支持首选版本的现代服务器;
- một máy chủ hiện đại trả lại một phiên bản hoặc lỗi tiêu đề được công nhận;
  Trung ngữ翻译: quay lại phiên bản có thể nhận ra hoặc đầu部错误的现代服务器;
- một máy chủ cũ mà chưa bao giờ nghe nói về `server/discover`-
  Từ xưa chưa nghe nói `server/discover`của phiên bản cũ của máy chủ;
- một máy chủ cũ mà giữ im lặng cho đến khi nó nhận được `initialize`- Tôi không biết.
  Trung ngữ翻译:收到 `initialize`之前一直沉默的旧版服务器──

> **【中文解读】**Trong bốn dạng hình thái đối đầu dễ dàng nhất là hai loại hỗn hợp sau cùng với lỗi: hình thức sai lầm của yêu cầu hiện đại, máy chủ được tải qua, quá trình chết và máy chủ cũ đều có thể tạo ra cùng một quá thời gian hoặc kết nối bị đóng.

Việc xử lý mọi lỗi của con tàu như là lỗi thừa kế là nguy hiểm. Một yêu cầu hiện đại bị sai, một máy chủ quá tải, một quá trình chết và một máy chủ cũ đều có thể tạo ra cùng một thời gian hoặc kết nối kết thúc. Những tín hiệu đó là mơ hồ. Khách hàng phải kết hợp ý định rõ ràng của nhà điều hành với bằng chứng giao thức tích cực trước khi chọn thời kỳ thừa kế.

> Đánh giá mỗi lỗi phát hiện là như phiên bản cũ là nguy hiểm. Phản ứng lỗi định dạng của các yêu cầu hiện đại, các máy chủ được tải qua, các quá trình đã chết và các máy chủ cũ có thể tạo ra cùng một siêu thời gian hoặc kết nối bị đóng cửa. Những tín hiệu này là khác biệt.

>  **【类比】**时代判断像医院急诊分诊: bệnh nhân(对端服务器)送来时, bạn không thể vì "叫不应"就断定他是外国人 (叫不应) 他可能只是昏睡 (昏睡) 过载 (过载) 耳背 (耳背) 请求格式错) 或已心跳停止 (已心跳停止) 进程死了 (已心跳停止) `server/discover`), nghe hiểu并规范应答 → 现代病人; nghe hiểu nhưng sửa chữa dùng ngữ của bạn(-32022/-32020/-32021)→ 还是现代病人,改口即可;完全叫不醒 → 也不能直接按外国人处理,除非病历上写着"确认是外国人,允许换方言再喊一次"(allowist 授权有界启动 探测),且换方言后得到清醒的规范应答(正向启动 证据) 才确诊.

## Khái niệm cốt lõi

### Một người đồng nghiệp, không phải một phiên giao thức

> **【中文解读】**客户端为每个服务器进程或端点保留一条"对端记录" (tương tự ghi):传输句柄、选定的时代和版本、最近发现的能力、最近发现工具列表、待关的请求 id、传输健康度──注意分寸: Đây là sổ kế toán của khách hàng, không phải là trạng thái giao ước会话现代 MCP 下, máy chủ vẫn tiếp nhận phiên bản và năng lực hiện tại trên mỗi yêu cầu──

Giữ một bản ghi tương tự vận chuyển cho mỗi quy trình hoặc điểm cuối của máy chủ:

- chức năng cầm hoặc gửi vận chuyển;
  Trung文翻译:传输句柄或发送函数;
- Thời đại và phiên bản giao thức được chọn;
  Trung文翻译: chọn định nghĩa
- khả năng máy chủ được phát hiện lần cuối;
  Trung ngữ翻译: gần đây发现的服务器能力;
- danh sách các công cụ xác định cuối cùng;
  Trung ngữ翻译: gần đây nhất xác định tính công cụ danh sách;
- Đơn vị nhận dạng yêu cầu tương quan đang chờ đợi;
  中文翻译: dùng để liên kết của chờ xử lý yêu cầu ID;
- sức khỏe vận tải.
  Trung ngữ翻译:传输健康度。

Đây là kế toán khách hàng. Nó không phải là trạng thái phiên giao thức. Trên MCP hiện đại, máy chủ vẫn nhận phiên bản và khả năng hiện tại trên mỗi yêu cầu.

> Đây là sổ khách hàng. Nó không phải là trạng thái giao dịch. Trong MCP hiện đại, máy chủ vẫn nhận được phiên bản và khả năng hiện tại trên mỗi yêu cầu.

### Xây dựng mọi yêu cầu hiện đại từ đầu

```python
def modern_request(request_id, method, params, version, capabilities):
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "method": method,
        "params": {
            **params,
            "_meta": {
                "io.modelcontextprotocol/protocolVersion": version,
                "io.modelcontextprotocol/clientCapabilities": capabilities,
                "io.modelcontextprotocol/clientInfo": CLIENT_INFO,
            },
        },
    }
```

Đừng gắn metadata một lần vào một đối tượng kết nối và giả định nó đã đạt đến dây.

> Đừng đặt dữ liệu của bạn một lần gắn vào đối tượng kết nối khi bạn cố tình nhận được nó trên đường.

### Phát hiện hiện đại

`server/discover`trả lại các phiên bản được hỗ trợ, khả năng máy chủ, hướng dẫn, gợi ý cache và danh tính máy chủ được khuyến cáo.

> `server/discover`返回支持的版本、服务器能力、使用说明、缓存提示与建议的服务器身份──客户端选择双方都支持的最新现代版本──

Discovery là tùy chọn cho một khách hàng hiện đại, nhưng nó được khuyến cáo trên stdio. Một số máy chủ cũ chấp nhận một hoạt động trước khi khởi động, vì vậy gửi `tools/list`đầu tiên có thể tạo ra một thành công không rõ ràng. `server/discover`tạo ra một ranh giới thời đại sạch sẽ.

> Đối với các máy chủ khách hàng hiện đại, phát hiện là lựa chọn, nhưng trong studio khuyến nghị làm. Một số máy chủ phiên bản cũ cũng được chấp nhận hoạt động trước khi khởi động, vì vậy trước tiên phát triển.`tools/list`Có thể có sự thành công khác biệt.`server/discover` tạo ra một giới hạn thời đại sạch.

### Chuẩn bị kết hợp với stdio

> **【中文解读】**stdio 兼容探测的判定树只有三条分支:(1) 收到 DiscoverResult → 现代对端,选定版本后继续;(2) 收到可识别的现代错误(-32020/-32021/-32022)→ 仍然是现代对端-32022 就从数据.支持的选版本重试,其他错误修正请求,绝不发初始化;(3) 歧义信号未识别的 JSON-RPC 错误、超时、连接关闭、空响)→ 不判定时,除非该端配置旧版兼容就失败关闭──关键不变式: 一旦对端证明认识现代错词表,即使在白名单里也不允许降级.

Một khách hàng studio hai thời đại gửi `server/discover`với các metadata hiện đại được ưa thích trước bất kỳ yêu cầu nào khác. Có ba lớp kết quả:

1. **DiscoverResult.**Các máy chủ là hiện đại. Chọn một phiên bản hỗ trợ lẫn nhau và tiếp tục với mỗi yêu cầu metadata.
   Trung ngữ翻译:**DiscoverResult。**服务器是现代的── chọn phiên bản được hỗ trợ bởi cả hai bên, để tiếp tục yêu cầu dữ liệu.
2. **Recognized modern error.**Máy chủ là hiện đại.`-32022`, chọn từ `data.supported`và thử lại với một ID yêu cầu mới. Đối với các lỗi tiêu đề hoặc khả năng, sửa lỗi yêu cầu. Không gửi `initialize`- Tôi không biết.
   Trung ngữ翻译:**可识别的现代错误。**服务器是现代的──`-32022`Từ đó`data.supported`中选择并使用新请求 id 重试;头部或能力错误就修正请求──不要发送 `initialize`
3. **Ambiguous signal.**Một lỗi JSON-RPC không được nhận ra, thời gian hết, kết nối đóng hoặc phản ứng trống không xác định một thời đại.
   Trung ngữ翻译:**歧义信号。**Không nhận ra JSON-RPC  lỗi, quá thời gian, kết nối kết nối hoặc không có phản ứng không thể xác định thời gian.

Các lỗi giao thức hiện đại được nhận ra bao gồm:

- `-32020`HeaderThật không phù hợp
  Trung ngữ翻译:`-32020`头部不一致 (Header không phù hợp)
- `-32021`Thiếu yêu cầuCơ quan
  Trung ngữ翻译:`-32021`缺失必需的客户端能力(Mất khả năng khách hàng
- `-32022`Không hỗ trợProtocolVersion
  Trung ngữ翻译:`-32022`Không hỗ trợ (không hỗ trợ)

Các lỗi hiện đại được nhận ra vẫn hiện đại ngay cả khi người đồng nghiệp đang trên danh sách quyền thừa kế. Một khi máy chủ chứng minh rằng nó hiểu từ vựng lỗi hiện đại, gửi `initialize`sẽ là một mức giảm.

> Có thể nhận ra lỗi hiện đại ngay cả khi từ các trang web trên danh sách trắng cũng được xác định là lỗi hiện đại. Một khi máy chủ chứng minh nó hiểu lỗi hiện đại từ ngữ, tái phát.`initialize`Đó là mức thấp hơn.

Không điều trị`-32601`Điều này chỉ làm cho một đồng nghiệp được phép rõ ràng đủ điều kiện cho một cuộc thăm dò thừa kế.

> Đừng làm vậy`-32601`Khi được xem như chứng minh hướng thẳng của phiên bản cũ. Nó chỉ đơn giản là để cho các bên trên danh sách trắng rõ ràng có được một lần kiểm tra phiên bản cũ.

### Việc cho phép là ý định của người vận hành, không phải bằng chứng

Sự tương thích của Legacy phải là một thuộc tính rõ ràng của một cấu hình đồng cấp gắn:

> 旧版兼容 phải là một thuộc tính rõ ràng của định vị kết thúc cố định:

```python
client.add_server("archive", archive_transport, allow_legacy=True)
```

Kết nối lựa chọn đó với lệnh hoặc điểm cuối được cấu hình. Đừng sử dụng thẻ hoang dã cho phép một máy chủ tùy tiện tự chọn cho bản thân vào ngữ nghĩa yếu hơn.`allow_legacy=True`thất bại sau khi phát hiện kết quả không rõ ràng và không bao giờ nhận được`initialize`- Tôi không biết.

> Hãy kết nối lựa chọn này với lệnh hoặc điểm cuối của cấu hình. Đừng sử dụng các mã thông báo để bất kỳ máy chủ nào tự chọn các từ ngữ yếu hơn. Không có.`allow_legacy=True`Đánh giá của kết quả sau thất bại trực tiếp, mãi mãi không được nhận được.`initialize`

Người cho phép cho phép thăm dò, không chọn thời đại.`initialize`trong thời hạn bắt buộc khi vận chuyển, sau đó yêu cầu tất cả các điều sau đây:

> Đơn vị này được cấp bằng giấy phép thăm dò, không phải là thời đại lựa chọn.`initialize`, sau đó yêu cầu các điều kiện sau đây được thực hiện:

- một JSON-RPC `2.0`trả lời bằng ID yêu cầu phù hợp;
  中文翻译:带匹配请求 id 的 JSON-RPC `2.0`响应;
- chính xác là một.`result`Và không`error`-
  Trung ngữ翻译:恰好一个 `result`且没有 `error`-
- a `protocolVersion`trong bộ sửa đổi cũ được cấu hình của khách hàng;
  Trung ngữ翻译:`protocolVersion`Trong tập hợp sửa đổi phiên bản cũ của định dạng khách hàng;
- một giá trị đối tượng `capabilities`trường;
  Trung ngữ翻译:`capabilities`字段是对象值;
- a `serverInfo`đối tượng với chuỗi không trống `name`và `version`các cánh đồng.
  Trung ngữ翻译:`serverInfo`đối tượng带非空字符串的`name`Với`version`字段。

Một thời gian nghỉ, kết nối kết thúc, phản ứng lỗi, kết quả bị sai, id không phù hợp hoặc sửa đổi không được hỗ trợ không được đóng. Chỉ có kết quả tích cực có tính cấu trúc hợp lệ chọn thời kỳ di sản. Mã thông qua `legacy_probe_timeout_ms`cho bộ chuyển đổi chuyển tiếp; một bộ chuyển đổi thực tế hoặc bộ chuyển đổi HTTP phải thực thi thời hạn đó thay vì chỉ ghi lại nó.

> 超时、连接关闭、错响应、形结果、id không phù hợp hoặc sửa đổi không được hỗ trợ,都会失败即关闭── chỉ có kết quả đúng hướng của cấu trúc hợp pháp mới chọn phiên bản cũ──代码把`legacy_probe_timeout_ms`传给传输适配器; thực tế studio hoặc HTTP 适配器 phải bắt buộc thực hiện giới hạn thời gian này, chứ không chỉ ghi lại nó.

Cache thời gian được chọn cho người giao thông. Đừng tìm kiếm lại trước mỗi cuộc gọi.

> Hãy chọn thời gian để lưu trữ đến khi truyền lên. Đừng thử lại trước khi sử dụng.

> ️ **【易错点】**场景: 把`-32601`(Phương pháp không tìm thấy) hoặc siêu thời gian trực tiếp như chứng cứ " đối với kết thúc là phiên bản cũ ",随即发送初始化 / 后果: trên máy chủ hiện đại đây là một lần hạ cấp nắm tay;恶意或故障服务器借机把客户端拖进更弱的语义;无界等待挂死启动流程 / 修复:坚持"白名单只给探测资格 + 五条正向验证全部通过才选旧版",并让传输适配器真正强制`legacy_probe_timeout_ms`时限; bất cứ điều gì không thỏa mãn就失败关闭, đối với nó giữ không thể sử dụng.

### Legacy là một nhánh tương thích

Khi thăm dò giới hạn trả lại bằng chứng thừa kế tích cực hợp lệ, khách hàng sử dụng phiên bản thừa kế được chọn chính xác như được định nghĩa bởi sửa đổi đó:

1. Kiểm tra bao bì phản ứng và ID tương quan.
   Trung文翻译:校验响应信封与关联 id──
2. Kiểm tra xem phiên bản sửa đổi được đàm phán là trong bộ nhượng bộ được cấu hình.
   Trung ngữ翻译:确认协商出的修订在配置的旧版集合内──
3. Lập lại khả năng được xác nhận và danh tính máy chủ.
   Trung文翻译:记录已验证的能力与服务器身份──
4. Gửi đi`notifications/initialized`Chỉ sau khi tất cả các kiểm tra qua.
   Trung文翻译: tất cả kiểm tra qua sau才发送 `notifications/initialized`
5. Sử dụng các hình thức yêu cầu cũ cho thời gian vận chuyển đó.
   Trung ngữ翻译: trong vòng đời truyền tải tầng sử dụng phiên bản cũ yêu cầu hình dạng.

Chi nhánh này tồn tại để tương tác với các đồng nghiệp được biết đến. Nó không phải là thiết kế mặc định cho các máy chủ mới hoặc yêu cầu mới. Nếu chuyển tiếp khởi động lại hoặc điểm cuối của nó thay đổi, hãy loại bỏ bộ nhớ cache thời đại đồng nghiệp và đàm phán lại.

> Điều này là một phần của sự tồn tại của kết nối với kết nối đã biết đến trên kết nối. Nó không phải là thiết kế mặc định của máy chủ mới hoặc yêu cầu mới. Nếu tầng truyền chuyển được khởi động lại hoặc kết nối thay đổi, bỏ lại lưu trữ và đàm phán lại trên kết nối thời gian.

### Công cụ phát hiện và lưu trữ cache

Đối với mỗi đồng nghiệp hoạt động, gọi `tools/list`Kết quả hiện đại bao gồm:`resultType`- `ttlMs`, và`cacheScope`. tôn trọng gợi ý tươi mới trong bối cảnh chính xác của phép.

> Đối với mỗi hoạt động đối với kết thúc`tools/list`现代结果包含 `resultType``ttlMs`和 `cacheScope`                                                                                                                                                                                                                                                              

Khách hàng phải chăm sóc một người mất tích.`resultType`từ một máy chủ cũ như `"complete"`Không yêu cầu các trường cache hiện đại trên một phản ứng từ một thời đại đàm phán trước đó.

> 客户端 phải bỏ phiên bản cũ của máy chủ bị mất tích `resultType`   `"complete"`◊ không đối phó với các yêu cầu đáp ứng của thời đại trả lại

Các máy chủ phải trả lại định nghĩa đặt hàng. Khách hàng cũng nên sắp xếp trước khi sáp nhập để đặt hàng đăng ký địa phương không phụ thuộc vào thời gian khởi động quy trình.

> 服务器应返回确定性排序──客户端在合并前也应排序,这样本地注册表顺序就不依赖进程启动时序──

### Thủy kết không gian tên an toàn đối với va chạm

> **【中文解读】**2 máy chủ có thể gọi`search` 3 tuyên bố về chiến lược: 1) 冲突加前保留第一规范名,后来的冲突暴露为 `<server>/<tool>`2) 冲突拒绝不加载重复项并报告清晰的配置错误; 3) 静默覆盖永远不要使用,它隐藏"模型中的动作实际发给哪个服务器"──同时存规范名和本地名:模型看规范名,发射`tools/call`Sử dụng tên địa phương của tuyên bố máy chủ sở hữu công cụ này.

Hai máy chủ có thể cho thấy cả hai .`search`Chọn chính sách được tuyên bố:

1. **Prefix on collision.**Giữ tên gọi chính thức đầu tiên và tiết lộ các vụ va chạm sau đó như `<server>/<tool>`- Tôi không biết.
   Trung ngữ翻译:**冲突加前缀。**Bảo vệ quy định thứ nhất, để lộ ra xung đột sau đó.`<server>/<tool>`
2. **Reject on collision.**Đừng tải bản sao và làm cho lỗi cấu hình rõ ràng xuất hiện.
   Trung ngữ翻译:**冲突拒绝。**Không tải trọng, bỏ ra một sai lầm định dạng rõ ràng.
3. **Silent overwrite.**Không bao giờ sử dụng nó. Nó ẩn máy chủ nào nhận được một hành động được chọn bởi mô hình.
   Trung ngữ翻译:**静默覆盖。**Không sử dụng mãi mãi. Nó ẩn trong máy chủ nào nhận được động tác trong mô hình được chọn.

lưu trữ cả hai tên theo quy luật và địa phương. mô hình thấy tên theo quy luật.`tools/call`sử dụng tên địa phương mà máy chủ chủ đã tuyên bố.

> Đồng thời lưu trữ quy định danh hiệu với địa danh.`tools/call`Sử dụng tên địa phương của tuyên bố máy chủ sở hữu công cụ này.

### Đường dẫn cuộc gọi

Đường dẫn là một tìm kiếm thuần túy:

> 路由是一次纯查表:

```text
canonical tool name
  -> peer name + local tool name
  -> new JSON-RPC request id
  -> modern request metadata or explicit legacy shape
  -> matching response id
```

Không gửi một cuộc gọi khi vận chuyển của chủ sở hữu không có sẵn.`tools/list`Các yêu cầu trong chuyến bay hiện đại bị mất trong một chuyến vận chuyển bị hỏng có thể được thử lại với một ID JSON-RPC mới khi chính sách an toàn của hoạt động cho phép.

> Khi không thể sử dụng được lớp truyền của công cụ này, đừng gửi đi.`tools/list`◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊   ◊ ◊     ◊                                                                                                                                                                    

### Thông báo và đăng ký

Các thay đổi danh sách và tài nguyên hiện đại chỉ xuất hiện khi khách hàng mở `subscriptions/listen`Khách hàng gửi bộ lọc thông báo, chờ đợi`notifications/subscriptions/acknowledged`, và tương quan các sự kiện với ID yêu cầu nghe trong các metadata thông báo.

> Các danh sách và tài nguyên hiện đại thay đổi chỉ đến khi khách hàng mở cửa.`subscriptions/listen`流上. 客户端发送通知 器, chờ `notifications/subscriptions/acknowledged`,并用通知元数据里的听 请求 id 关联事件──

Khi kết nối, mở một yêu cầu nghe mới và chỉnh sửa danh sách hoặc tài nguyên liên quan.`Last-Event-ID`- Tôi không biết.

> 断连时,打开一个新的听 请求并重新拉取相关列表或资源──现代流不用 `Last-Event-ID`恢复:

### Không có yêu cầu được khởi động bởi máy chủ

Các máy chủ hiện đại không gọi khách hàng với các yêu cầu JSON-RPC độc lập để lấy mẫu, tạo ra hoặc gốc.`input_required`, và khách hàng thử lại yêu cầu ban đầu sau khi đáp ứng các yêu cầu nhập được nhúng.

> 现代服务器 sẽ không sử dụng JSON-RPC độc lập                                                                                                                                                                                                                                                        `input_required`, khách hàng hoàn chỉnh được cài đặt vào yêu cầu sau khi thử lại yêu cầu nguyên bản.

Đừng chặn trình đọc phản ứng của đồng nghiệp trong khi thực hiện đầu vào. Giữ mối tương quan và tạo một ID JSON-RPC mới cho thử lại.

> 补齐输入时不要阻塞端的响应读取器──保持关联性,并为重试创建新的 JSON-RPC id──

> **【拓展：与旧版客户端课的对照】**旧版本节课的主角是"子进程管理 + khởi động 握手 + 样本回调"; 新版把它们全部让位给"时代协商":样本/elicitation 已废弃为多轮往返请求,握手只剩下一条白名单授权有界探测分支,进程管理抽象成对端记录(peer record) ⋅变化最大也最体会的一个点: 客户端的复杂性从"运行时会话编排"转移到"启动时代判定与失败关闭策略"──

```figure
tp-client-merge
```

## Hãy sử dụng nó để thực hiện

`code/main.py`sử dụng các chức năng tương tác trong quá trình để các quyết định giao thức vẫn hiển thị. Nó kết nối với hai tương tác hiện đại và một tương tác di sản được phép cố ý, sau đó sáp nhập và định tuyến các công cụ của họ.

> `code/main.py`Sử dụng hàm cuối trong quá trình, để cho phép quyết định giao ước được giữ có thể nhìn thấy. Nó kết nối hai cuối hiện đại và một cuối cũ cố ý gia nhập vào danh sách trắng, sau đó kết hợp và đi qua các công cụ của chúng.

```bash
cd code
python3 main.py
python3 -m unittest discover tests -v
```

Các thử nghiệm chứng minh ranh giới mà các bản demo bình thường bỏ qua:

> Những thử nghiệm này chứng minh rằng biểu diễn thường xuyên sẽ bị bỏ qua:

- Các yêu cầu hiện đại lặp lại metadata;
  Trung文翻译:现代请求重复携带元数据;
- `-32022`thử lại khám phá hiện đại mà không cần khởi tạo;
  Trung ngữ翻译:`-32022`重试现代发现而不做初始化;
- lỗi hiện đại được công nhận không bao giờ giảm cấp, ngay cả đối với một đồng nghiệp được phép;
  Trung ngữ翻译:可识别的现代错误绝不降级 ngay cả khi trên danh sách trắng;
- thời gian ra ngoài, kết nối đóng cửa, trả lời trống và lỗi không được nhận ra không kích hoạt `initialize`Không có một người được phép;
  Trung ngữ翻译:超时、连接关闭、空响应和未识别的错误在没有白名单时不会触发`initialize`-
- một đồng nghiệp được liệt kê trở thành di sản chỉ sau khi có một hợp lệ, được hỗ trợ `initialize`kết quả;
  Trung ngữ翻译:白名单对端只有在接受合法且得到支持的`initialize`Kết quả sau khi trở thành phiên bản cũ;
- kết quả thừa kế bị biến dạng và không được hỗ trợ khiến người đồng nghiệp không có sẵn;
  Trung文翻译:形或不受支持的旧版结果使对端保持不可用;
- một thời gian được chọn thành công được lưu trữ trong thời gian vận chuyển.
  Trung ngữ翻译: thành công chọn thời代会缓存整个传输层生命周期──

## Chuyển nó đi.

Bài học này sẽ đi theo `outputs/skill-mcp-client-harness.md`Nó cung cấp các thiết kế đặt dấu yêu cầu hiện đại, đàm phán thời đại studio, kết hợp không gian tên xác định, định tuyến và một nhánh tương thích di sản bị đóng cửa.

> 本课交付 `outputs/skill-mcp-client-harness.md`△ nó xây dựng 现代请求盖章、studio 时代协商、确定性命名空间合并、路由,以及一条失败关闭的旧版兼容分支──

## Tập luyện bài tập

1. Làm một máy chủ giả trở lại `-32022`Không có phiên bản hỗ trợ lẫn nhau. xác nhận khách hàng thất bại thay vì gửi `initialize`- Tôi không biết.
   Trung文翻译:让一个假服务器返回 `-32022`Không có phiên bản được cả hai bên hỗ trợ.`initialize`

2. Cho phép một máy chủ cũ giả, làm cho nó bị giới hạn `initialize`- Đánh giá thời gian và chứng minh các đồng nghiệp vẫn ở lại.`unknown`và không có sẵn.
   Trung ngữ翻译:把一个假旧版服务器加入白名单,让它有界的 `initialize`探测超时, chứng minh phải đối đầu giữ `unknown`Và không thể sử dụng được.

3. Thêm `cacheScope: "private"`danh sách công cụ cho hai ngữ cảnh ủy quyền. xác nhận khách hàng không bao giờ chia sẻ kết quả được lưu trữ trong cache của một ngữ cảnh với một ngữ cảnh khác.
   Trung ngữ翻译:为两个授权上下文添加 `cacheScope: "private"` Đảm bảo khách hàng không bao giờ chia sẻ kết quả lưu trữ của một trên sau cho một bên khác.

4. Thay đổi chính sách va chạm thành từ chối và làm cho khởi động thất bại với cả hai tên đồng nghiệp trong lỗi.
   Trung ngữ翻译:把冲突策略改为拒绝,让启动失败和带上两个对端的名字在错误信息中.

5. Thêm một số hữu hạn `subscriptions/listen`Khi mất dòng, nghe lại với một ID yêu cầu mới và các công cụ chỉnh sửa.
   Trung ngữ翻译:添加一个有限的`subscriptions/listen`模拟器──流断开时, dùng mã yêu cầu mới 重新监听并重新拉取工具──

## Từ khóa  Từ khóa nhanh chóng

| Term | Meaning |
|------|---------|
| Peer | Client-side record for one server transport and its discovered data |
| Protocol era | Modern per-request metadata or legacy initialization semantics |
| Discovery probe | Initial `server/discover` used to identify the stdio era |
| Recognized modern error | Error that proves modern behavior and forbids legacy fallback |
| Legacy allowlist | Operator configuration permitting one bounded compatibility probe for a pinned peer |
| Positive legacy evidence | Valid, correlated `initialize` result for an explicitly supported legacy revision |
| Merged namespace | Canonical tool names across all active peers |
| Collision policy | Prefix or reject rule for duplicate tool names |
| Era cache | Selected modern or legacy behavior stored for one transport peer |
| Transport recovery | Restart or reconnect, rediscover, relist, and retry safely with a new id |

> 术语中文对照:Peer=对端(客户端侧对一个服务器传输层及其发现数据的记录);Protocol era=协议时代(现代逐请求元数据或旧版初始化语义);Discovery probe=发现探测(用于判定studio 时代的首次`server/discover`);Phỏng lẻo hiện đại được nhận ra = lỗi hiện đại có thể nhận ra; chứng minh đối với端是现代的并禁止旧版回退; Legacy allowlist=旧版白名单; cho phép một lần thực hiện một lần có界兼容探测的运维配置;Cứng minh di sản tích cực = chứng minh đối với phiên bản cũ; chứng minh đối với các bản cũ được hỗ trợ rõ ràng và có liên quan.`initialize`Kết quả;Thể tích namespace=合并命名空间(跨所有活跃对端的规范工具名);Collision policy=冲突策略(重名工具的前或拒绝规则);Era cache=时代缓存(

## Xem thêm 延伸阅读

- [MCP Specification 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28/)
  Trung văn翻译:MCP 2026-07-28 规范全文
- [MCP Server Discovery](https://modelcontextprotocol.io/specification/2026-07-28/server/discover)
  Trung文翻译:server/discover 方法规范
- [MCP stdio Transport](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/stdio)
  Trung文翻译:studio 传输层规范
- [MCP Versioning](https://modelcontextprotocol.io/specification/2026-07-28/basic/versioning)
  Trung文翻译:MCP 版本协商机制
- [MCP Tools](https://modelcontextprotocol.io/specification/2026-07-28/server/tools)
  Trung ngữ翻译:tools 原语规范
