# Đánh bật, phá mạch và mã thông báo Canary

> Một chuyển đổi kill là một boolean được giữ bên ngoài bề mặt chỉnh sửa của đại lý  một phím Redis, một cờ tính năng, một cấu hình được ký  vô hiệu hóa đại lý hoàn toàn. Một máy cắt mạch có tinh tế hơn: nó đâm vào một mô hình cụ thể (lên năm công cụ giống nhau liên tiếp), dừng lại con đường phạm tội, và leo thang lên con người. Một mã thông báo canary thừa hưởng từ lừa dối cổ điển: một giấy chứng nhận giả hoặc hồ sơ honeypot một đại lý không có lý do hợp pháp để chạm vào, truy cập của người đó kích hoạt một cảnh báo. Các đường dữ liệu dựa trên eBPF (ví dụ: Cilium) có thể viết lại sự ra đi của một pod bị cách ly sang một honeypot pháp y ở lớp lõi; các điểm chuẩn Cilium được xuất bản báo cáo độ trễ của đường dữ liệu P99 dưới mi-millisecond dưới tải (khuế ngân sách truyền thông của bạn phụ thuộc vào cách cập nhật chính sách đạt đến nút, chứ không phải chính đường dữ liệu). Các máy dò thống kê (EWMA, CUSUM) thích nghi với một đường cơ sở di chuyển sẽ lặng lẽ chấp nhận drift  lớp chúng với các giới hạn hiến pháp cứng mà không xoay.

> **【中文解读】**终止开关是位于代理 编辑面之外的布尔值Redis 键、功能标志、签名配置完全禁用 Agent。断路器更细粒度:跳在特定模式上(连续五次相同工具调用),暂停违规路径并升级到人类。金雀代币 继承经典欺骗:Agent 无合法理由触及假凭证或蜜记录,其访问触发警报──基于 eBPF的数据路径 (例如Cilium) 可在内核层将分离pod的输出重写到取证;公开Cilium 准载下亚秒 P99 数据路径延迟美国传播预算取决于策略更新到达决点,非路径本身) 移动报告检测器的基层 CUMM 如何接受CUM 基层的移动化 CUM CUM CUM CUM CUM CUM CUM CUM CUM CUM CUM CUM  CUM                                                                                                                             

> **【拓展：三层不信任架构】**三個检测器全部不信任 Agent 自報告:终止开关外置(Agent 不能编辑) 断路器模式匹配(不看 Agent 意图)  金丝雀 dựa trên nguyên tắc "不应触及" (không nên chạm vào) 访问即警报)  统计检测器 (EWMA/CUSUM) 适应漂移 (适应漂移) nhưng sẽ bị kẻ tấn công kiên nhẫn chậm di chuyển (缓移基线绕过) 硬宪法限制 (永不发邮给秘密@) 简单、可审计、不可博︎: 统计检测器捕获大多数噪音, 硬限制捕获通过检测器的攻击.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, three-detector simulator: kill switch, circuit breaker, canary) | **语言:** Python（标准库，三检测器模拟器：终止开关、断路器、金丝雀）
**Prerequisites:** Phase 15 · 13 (Cost governors), Phase 15 · 10 (Permission modes) | **前置知识:** Phase 15 · 13（成本治理器），Phase 15 · 10（权限模式）
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**Học本节前请先掌握:Phase 15·13(Cost Governors) Phase 15·10(chế độ quyền hạn) 网络安全基础 (网络安全基础) 蜜、断路器)  三道防线 = 不信任 代理自报告──
>  **【类比】**三道防线 = "银行保三层"――Kill Switch = 总( tình huống khẩn cấp một键断电,Agent 不能改);Circuit Breaker = tự động nhảy(检测到异常模式自动暂停,如连续 5次相同操作);Canary Token = 银行假(不应触及的假数据,一被访问就报警)。三层都不信 Agent依赖外置基础设施检查──
> 🤔 **【困惑】**Q: Tại sao không dựa vào Agent trong đặt kiểm tra an ninh? Vì Agent có thể bị phá vỡ hoặc tự sửa đổi qua DGM trường hợp)。修复: kiểm tra thiết bị phải độc lập với Agent (Redis键、内核 eBPF、签名配置),Agent 看不到、改不了、绕不过── đây là cốt lõi của "trust-but-verify"。

## Vấn đề  vấn đề giới thiệu

> **【中文解读】**终止开关) 和金雀测试) là một trong hai tuyến phòng thủ an toàn của Agent. 终止开关 cho phép người vận hành ngay lập tức ngừng tất cả các hoạt động của Agent.

> **【拓展：kill switches canaries】**终止开关和金雀测试借鉴软件工程和工业安全的最佳实践. 终止开关部署 trong phần mềm工程指向1%用户发布新版本,检测问题后再全面部署. 终止开关指向在代理上下文中,金雀测试指向在执行高风险操作前先使用安全数据进行小规模测试.

Các nhà quản lý chi phí (Lớp 13) giới hạn những gì đại lý có thể chi tiêu.

> 成本控制器 (第13 课) hạn chế người đại lý 能花什么――它们不限制 người đại lý 在预算内能做什么――

Một đại lý với giới hạn tốc độ 50 đô la vẫn có thể giải quyết một bí mật, xuất bản bài đăng sai, hoặc xóa tài nguyên  hành động đắt tiền thường là một ít tiền trong token.

> 带50$ 速度限制的代理 仍可泄露秘密,发布错误帖子或删除资源 昂贵动作往往是标志上便宜的──

Bài học này bao gồm ba bộ dò có vị trí bên cạnh lớp chi phí:

> Chương trình này bao gồm ba máy kiểm tra nằm bên cạnh tầng chi phí:

> **【中文解读】**Bài này giới thiệu khái niệm và phương pháp thực hiện cốt lõi của AI Agent.

1. **Kill switch**: nút tắt boolean được giữ ngoài tầm với của đại lý.
   Trung ngữ翻译:**终止开关**: nằm bên ngoài của Agent 触及
2. **Circuit breaker**: máy dò mô hình hành động dừng một con đường cụ thể.
   Trung ngữ翻译:**断路器**: tạm dừng các phương pháp cụ thể của động tác mô hình kiểm tra
3. **Canary token**: mồi mà một nhân viên không có lý do hợp pháp để chạm vào sẽ tiết lộ mình bằng cách chạm vào.
   Trung ngữ翻译:**金丝雀 token**Đội ngũ nhân viên không có lý do hợp pháp để xúc phạm, xúc phạm, và lộ ra sự cám dỗ của mình.

Tất cả ba đều là kỹ thuật trước LLM. Sự lừa dối cổ điển, phá vỡ giới hạn tốc độ và tiêu diệt cờ tính năng trước các đại lý tự trị. Điều mới là bề mặt tấn công: các đại lý đọc nội dung không đáng tin cậy (Học 11), chỉnh sửa bộ nhớ của riêng họ, và có thể soạn nhiều hành động trông an toàn thành một hành động không an toàn. Các máy dò được đặt tên ở đây hoạt động vì họ không tin tưởng vào bản báo cáo của đại lý.

> 三者都是 LLM 前工程。经典欺骗、速率限制断路器和功能标志终止早于自主代理。 mới là攻击面:Agent 读取不信任内容(第 11 课) 、编辑 bản ghi nhớ của mình、可将多个安全动作组合为不安全动作──此处命名的检测器有效因为它们不信任代理的自报告──

## Khái niệm cốt lõi

### Đánh tắt chuyển động.

Một chuyển đổi kill là một boolean mà đại lý đọc nhưng không thể viết.

> 终止开关是代理不可读的价值.

Các lựa chọn thực hiện:

> 实现选择:

- **Feature flag in a managed service.**Thả lên, phát hành, phát hành, phát hành, phát hành, phát hành, phát hành, phát hành, phát hành, phát hành, phát hành, phát hành, phát hành, phát hành, phát hành, phát hành, phát hành, phát hành, phát hành, phát hành, phát hành, phát hành, phát hành, phát hành, phát hành, phát hành, phát hành, phát hành, phát hành, phát hành, phát hành, phát hành, phát hành, phát hành, phát hành, phát hành, phát hành, phát hành, phát hành, phát hành, phát hành, phát hành, phát hành, phát hành, phát hành, phát hành, phát hành, phát hành, phát hành, phát hành, phát hành, phát hành, phát hành, phát hành, phát hành, phát hành, phát hành, phát hành, phát hành, phát hành, phát hành, phát hành, phát hành, phát hành, phát hành, phát hành, phát hành
  Trung ngữ翻译:**管理服务中的功能标志。**Thả lên: Đen Đen, Đứng, Thả ra, cập nhật trong vài giây
- **Redis key the agent polls.**Khả năng đơn giản, đòi hỏi các nhân viên phải kiểm tra mọi bước.
  Trung ngữ翻译:**Agent 轮询的 Redis 键。**简单; yêu cầu đại lý 进程 mỗi vòng kiểm tra.
- **Signed config in object storage.**Trưởng kiểm tra chữ ký trên boot; từ chối các trạng thái chưa ký.
  Trung ngữ翻译:**对象存储中的签名配置。**Trưởng 启动时验证签名; từ chối trạng thái chưa ký kết
- **OS-level signal or container-lifecycle kill.**Docker `kill`, Kubernetes `kubectl delete pod`, hệ thống sẽ dừng lại.
  Trung ngữ翻译:**OS 级信号或容器生命周期终止。**Docker `kill`、Kubernetes `kubectl delete pod`、Systemd dừng lại.

Các tính chất của một nút tắt chính xác có:

> Đặc tính chính xác kết thúc:

- Cảnh sát không thể đặt nó lên `off`(Trong một hệ thống mà các chứng chỉ của đại lý không viết.)
  Trung文翻译:Công ty không thể đặt nó thành`off`◊(位于 Agent 凭据不写的系统──)
- Nó được kiểm tra trên mọi hành động hậu quả, không chỉ trong khởi động.
  Trung ngữ翻译: 在每后果性动作上检查,不仅在启动时――
- Khi nó tắt, đại lý không làm gì ngoài nhìn thấy, bao gồm cả ghi vào các hệ thống mà đại lý có thể đạt được.
  Trung ngữ翻译:关闭时,Công ty không làm bất cứ điều gì có thể quan sát được bên ngoài, bao gồm ghi lại đến Hệ thống của Công ty 可达.
- Việc tái tạo nó là một hành động của con người, không phải là một thời gian tự động.
  Trung ngữ翻译:重新启动是显式人类动作,不是自动超时――

### Máy cắt mạch.

Một máy cắt mạch dừng một mô hình cụ thể, không phải toàn bộ chất.

> 断路器暂停特定模式,而不是整个 Agent──经典形状(来自 2007年 Nygard 书,仍然当前):

- **Closed**: hành động được phép.
  Trung ngữ翻译:**闭合**:动作允许──: 动作允许──:
- **Open**: hành động bị chặn.
  Trung ngữ翻译:**打开**Động tác ngăn chặn.
- **Half-open**: sau khi làm mát, 13 thử nghiệm thăm dò được phép (tầm 1); thành công đóng bộ ngắt, bất kỳ thất bại còn lại nào mở lại nó.
  Trung ngữ翻译:**半开**: chưng lại sau, cho phép 1-3 lần tìm kiếm; thành công đóng cửa máy, để phần còn lại thất bại mở lại.

Các tác động tác động liên quan đến tác nhân:

> Trình tác giả:

- Năm cuộc gọi công cụ giống nhau liên tiếp (cuối lặp).
  Trung ngữ翻译:连续五次相同工具调用 (重复循环)
- Năm lỗi liên tiếp trên cùng một công cụ với các đầu vào khác nhau (sự thất bại hệ thống).
  Trung文翻译:同一工具不同输入连续五次失败 (một trong những công cụ khác nhau)
- Tốc độ gọi công cụ vượt qua ngưỡng (tốc độ bài học 13).
  Trung文翻译:工具调用速率超过值(第 13 课速度)
- Công cụ cụ cụ thể được sử dụng (ví dụ: `file.delete`) sau khi đọc một nội dung không đáng tin cậy (Học 11).
  Trung ngữ翻译: 在不信任的内容读取后调用特定工具 (nói: 调用特定工具)`file.delete`(第 11 课)

### Đồ biểu tượng Canary

Các mã thông báo Canary (còn được gọi là honeyotokens) là các đầu vào mà người đại lý không bao giờ nên chạm vào.

> Địa chỉ 金丝雀 (也称蜜 token) là Trưởng không nên chạm vào.

Ví dụ về các đại lý:

> Ví dụ:

- Một giả `AWS_SECRET_ACCESS_KEY`Trong môi trường không có đặc quyền thực tế.
  Trung ngữ翻译:环境中无实际特权的假`AWS_SECRET_ACCESS_KEY`❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖
- Một bản ghi cơ sở dữ liệu giả được đánh dấu với giá trị Sentinel được biết đến.
  Trung ngữ翻译:以已知哨兵值标记的假数据库记录──此记录的任何阅读或更新触发警报──
- Một tập tin giả trong không gian làm việc.
  Trung ngữ翻译:工作区中的假文件──此文件的读或编辑可疑──
- Một mục ghi nhớ giả được tiêm vào khi bắt đầu phiên. Nếu nó xuất hiện trong một đầu ra sau đó, bộ nhớ đã được lọc.
  Trung文翻译:会话开始时注入的假记忆条目──如果它出现后续输出中,记忆已被泄露──

Thiết kế của cá thể là đặc biệt cho dòng công việc. Một cá thể có lý do hợp pháp để người đại lý chạm vào là tiếng ồn.

> Kỹ thuật của Kim C雀 là tiếng ồn.

### Tại sao lại có giới hạn thống kê và hạn chế cứng?

Các máy dò thống kê (EWMA, CUSUM, điểm z trên tỷ lệ gọi công cụ) thích nghi với một đường cơ sở di chuyển. Đó là một tính năng cho drift hợp pháp và một lỗi cho drift đối lập.

> 统计检测器(EWMA、CUSUM、工具调用速率 z 分数) 适应移动基线── đây là đặc điểm của漂移 hợp pháp, là chống lại漂移 bug──耐心攻击者可足够缓慢地移动基线使无警报触发──

Các giới hạn hiến pháp cứng rắn (Dạy học 17) không bị nghiêng.`secrets@`"như một quy tắc hiến pháp đơn giản hơn, kiểm toán, và không thể chơi bằng cách lôi kéo chậm. mô hình lớp: máy dò thống kê bắt được tiếng ồn nhiều nhất, giới hạn cứng bắt được cuộc tấn công đi qua máy dò.

> 硬宪法限制 (第 17 课) 不折──"永不发邮给 `secrets@`" Như quy tắc của hiến pháp đơn giản hơn, có thể kiểm tra, không thể bị chậm trễ di chuyển.

### Quarantaine thông qua đường dẫn dữ liệu eBPF chuyển hướng .

Chính sách mạng dựa trên eBPF của Cilium có thể viết lại sự ra đi của một chiếc máy móc bị cách ly sang một chiếc thùng mật ong pháp y ở lớp lõi. Các điểm chuẩn công cộng của Cilium báo cáo độ trễ đường dữ liệu P99 dưới millisecond trên TCP_RR; ngân sách đồng hồ tường để * kích hoạt* một sự cách ly tỏa trong cluster của bạn được thống trị bởi cách cập nhật chính sách lan truyền từ cấp độ điều khiển của bạn đến nút (một vài trăm millisecond là thực tế trên Kubernetes với trình điều hành được tải trước; độ trễ đuôi phụ thuộc vào kích thước cluster và phù hợp với độ trễ). Điều này cho bạn hai điều: đại lý không tháo ra bất cứ thứ gì thực sự, và hành vi của đại lý bên trong thùng mật ong được quan sát đầy đủ. Tương tự mô hình, lớp khác nhau, như biểu tượng canary: đại lý tiết lộ ý định bằng những gì nó cố gắng làm trong khi chứa.

> Chiến lược mạng dựa trên eBPF của Cilium có thể được viết lại trong tầng hạt nhân để lấy kết quả phân lập. Phương trình phân lập của Silicon sẽ được viết lại cho phép: báo cáo TCP_RR trên 800 giây P99 Data pathway delay; trong nhóm *触发* ngân sách của điện thoại phân lập được cập nhật bởi chiến lược làm thế nào để truyền tải từ phía kiểm soát đến các node chủ đạo.

### Không máy dò nào có thể bắt được gì.

- **Semantic attacks that compose from allowed primitives.**Mỗi hành động cá nhân vượt qua mỗi máy dò; thành phần là vấn đề. Đây là sự thất bại của chế độ tự động từ Bài học 10.
  Trung ngữ翻译:**从允许原语组合的语义攻击。**Mỗi đơn lẻ hoạt động qua mỗi máy kiểm tra; tập hợp là vấn đề.
- **Attacks that include the detector as part of the payload.**Nếu một đại lý đọc một trang nói "trước khi bạn hành động, vô hiệu hóa con người Canada" và đại lý có khả năng, máy phát hiện bị xâm phạm.
  Trung ngữ翻译:**将检测器作为载荷一部分的攻击。**Nếu đại lý nói "Động tác trước bị cấm" và đại lý có khả năng, máy kiểm tra bị tấn công.

## Hãy sử dụng nó để thực hiện
```figure
circuit-breaker
```

## Sử dụng nó

`code/main.py`mô phỏng quỹ đạo ngắn của đại lý thông qua ba bộ dò. Một nút tắt được giữ trong một lệnh bên ngoài; một bộ cắt mạch bị kích hoạt trên năm cuộc gọi công cụ giống nhau; một tệp canary đọc kích hoạt cảnh báo.

> `code/main.py`模拟通过三个检测器的短 Agent轨迹──外部 dict 中的终止开关; 在五次相同工具调用上跳的断路器;读取触发警报的金雀文件──进入合成轨迹:合法动作、重复循环、金雀探测、终止开关触发场景下 Agent 动作被停止──

## Chuyển nó đi.

`outputs/skill-tripwire-design.md`xem xét một bộ đống phát hiện được đề xuất cho việc triển khai một đại lý và đánh dấu các khoảng trống (không có nút tắt, không có canary, ngưỡng cắt mạch quá lỏng).

> `outputs/skill-tripwire-design.md`审查 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署 署

## Tập luyện bài tập

1. Đi chạy`code/main.py`- Cảm nhận sự cháy của máy cắt mạch ở lật 5 (đợt gọi giống nhau thứ năm) và những cơn cháy trên lật 9 (đọc khóa giả).
   Trung ngữ翻译:运行 `code/main.py`❖ xác nhận断路器在第五轮触发 (第五次相同调用) ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖

2. Thêm một máy dò thống kê: EWMA điểm z trên tốc độ gọi công cụ. Đưa vào một quỹ đạo di chuyển chậm và cho thấy máy dò không bao giờ nổ. Bây giờ thêm một giới hạn cứng (không quá 50 cuộc gọi công cụ trong 10 phút) và cho thấy các lửa giới hạn cứng trên cùng quỹ đạo.
   Trung ngữ翻译:添加统计检测器:工具调用速率的 EWMA z 分数──进缓慢漂移的轨迹并显示检测器从不触发──现在添加硬限制(10分钟内不超过50工具调用)并显示硬限制在同一轨道上触发──

3. Thiết kế một mã thông báo canary cho một trình duyệt (Học 11) Đặt ít nhất ba mã thông báo và mỗi mã sẽ phát hiện ra gì.
   Trung文翻译:为浏览器 Agent(第 11 课) 设计金丝雀代币 集──列出至少三金丝雀及各检测什么──

4. Đọc các tài liệu chính sách mạng Cilium. Mô tả một dòng chảy kiểm dịch chuyển hướng xuất cảnh cụ thể: chọn chính sách nào, pod nào, chuyển đổi xuất cảnh nào, cảnh báo nào. Điều gì điều chỉnh thời gian trễ của đồng hồ tường từ "thành quyết đến kiểm dịch" đến "bộ gói chuyển hướng đầu tiên"?
   Trung ngữ翻译:阅读 Cilium 网络策略文档――具体描述出口重定向隔离流:哪个策略选择器、哪个 pod、哪个出口重写、哪个警报──什么主导从"决定隔离"到"第一重定向包"的墙钟延迟?

5. Định nghĩa một quy trình tái kích hoạt cho một nhân viên bị chuyển đổi làm chết. Ai có thể tái kích hoạt?
   Trung ngữ翻译:为终止开关的代理 定义重新启动流程──谁可以重新启动?必须档档化什么?重新启动前代理 必须改变什么?

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| Kill switch | "Off button" | Boolean outside the agent's edit surface; checked on every consequential action |
| 终止开关 | "关闭按钮" | Agent 编辑面之外的布尔值；每个后果性动作上检查 |
| Circuit breaker | "Pattern pause" | Action-specific trip on repetition, failure rate, or rate-limit |
| 断路器 | "模式暂停" | 在重复、失败率或速率限制上动作特定跳闸 |
| Canary token | "Honeytoken" | Bait the agent has no legitimate reason to touch; access fires an alert |
| 金丝雀 token | "蜜罐 token" | Agent 无合法理由触及的诱饵；访问触发警报 |
| Honeypot | "Forensic sandbox" | Redirected traffic / workspace where a quarantined agent is observed |
| 蜜罐 | "取证沙箱" | 隔离 Agent 被观察的重定向流量/工作区 |
| EWMA | "Moving average" | Exponentially weighted; adapts to drift (feature + bug) |
| EWMA | "移动平均" | 指数加权；适应漂移（特性 + bug） |
| CUSUM | "Cumulative sum" | Detects sustained shift from baseline |
| CUSUM | "累积和" | 检测相对基线的持续偏移 |
| Hard limit | "Constitutional rule" | Does not adapt; constant regardless of history |
| 硬限制 | "宪法规则" | 不适应；不论历史的常量 |
| Constitutional limit | "Always-true rule" | Tied to Lesson 17's constitution; cannot be edited by the agent |
| 宪法限制 | "始终为真的规则" | 绑定第 17 课的宪法；Agent 不能编辑 |

## Xem thêm 延伸阅读

- [Anthropic — Measuring agent autonomy in practice](https://www.anthropic.com/research/measuring-agent-autonomy) khung chuyển đổi và cắt mạch cho các đại lý tự trị.
  Trung ngữ翻译: tự do Thuộc lập của kết thúc mở cửa và kết thúc khung máy.
- [Microsoft Agent Framework — HITL and oversight](https://learn.microsoft.com/en-us/agent-framework/workflows/human-in-the-loop) các mô hình quản lý sản xuất.
  Trung ngữ翻译:生产治理模式。
- [OWASP LLM / Agentic Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/) Yêu cầu phát hiện và phản ứng.
  Trung ngữ翻译:检测和响应要求。
- [Cilium — Network policy and eBPF](https://docs.cilium.io/en/stable/security/network/) chuyển hướng thoát cấp pod và hình mẫu honeypot pháp y.
  Trung文翻译:pod 级出口重定向和取证蜜模式。
- [Anthropic — Claude's Constitution (January 2026)](https://www.anthropic.com/news/claudes-constitution) cấm cứng mã hóa như là "các giới hạn hiến pháp".
  Trung ngữ翻译:硬编码禁止作为"宪法限制"──
