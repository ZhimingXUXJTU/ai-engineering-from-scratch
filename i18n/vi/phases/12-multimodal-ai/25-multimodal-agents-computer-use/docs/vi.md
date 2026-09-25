# Các đại lý đa phương tiện và sử dụng máy tính (Capstone) 

> Sản phẩm 2026 frontier là một đại lý đa phương thức đọc ảnh chụp màn hình, nhấp vào nút, điều hướng UI web, điền biểu mẫu và hoàn thành dòng công việc từ đầu đến cuối. SeeClick và CogAgent (2024) chứng minh nguyên thủy của GUI-grounding. Ferret-UI thêm điện thoại di động. ChartAgent đã giới thiệu công cụ sử dụng hình ảnh cho các biểu đồ. VisualWebArena và AgentVista (2026) là điểm chuẩn của các cuộc truy đuổi biên giới  và thậm chí Gemini 3 Pro và Claude Opus 4.7 điểm ~ 30% trên các nhiệm vụ khó khăn của AgentVista. Bạch đá này kéo tất cả các chuỗi của giai đoạn 12: nhận thức (VLM độ phân giải cao), lý luận (LLM với việc sử dụng công cụ), đặt đất (tạo ra phối hợp), bộ nhớ đường chân trời dài và đánh giá.

> **【中文解读】**Các sản phẩm tiên phong của năm 2026 là có thể đọc截截图、点按、导航网页、填表单、端到端完成工作流的多模态 Agent。SeeClick 和 CogAgent 证明 GUI 定位原语可行,Ferret-UI 扩展到移动端,ChartAgent 引入视觉工具调用──但在 AgentVista 困难任务上,即使是 Gemini 3 Pro 和 Claude Opus 4.7 也只有30%通过率这是Phase 12 的收费课程,整合感知、推理、定位、长期记忆和评估──

**Type:** Capstone
**Languages:** Python (stdlib, action schema + agent loop skeleton)
**Prerequisites:** Phase 12 · 05 (LLaVA), Phase 12 · 09 (Qwen-VL JSON), Phase 14 (Agent Engineering)
**Time:** ~240 minutes

>  **【前置】**Học本节前请先掌握:Phase 12 全部(VLM 演进) 、Phase 14·01-10(Agent 循环、工具调用) 、Phase 14·30+(工作台系列 Agent 实践) ⋅本节是Phase 12 的毕业课所有多模态 + Agent 技术整合成一个能操作电脑的产品──
>  **【类比】**多模态 Agent = "AI 实习生"──看截图(感知) + 想"下一步该点哪里"(推理) + 输出点击击坐标(行动) + 看新页面(观察) + 循环。普通 VLM = 看图说话(描述);Agent VLM = 看图做事(执行动作) ・・・困难在于:坐标精度(点错按) 长程规划(10步订票流程) 错误恢复(弹窗、广告、登录页) ・・・
> ️ **【易错点】**让 Agent 直接执行动作不设人工审核 = 灾难(可能误转账、错删除) 修复:所有"破坏性动作" (tiếng thăm 提交、确认、删除按) phải được kiểm tra con người hoặc chạy khô 模式。Phương pháp thiết kế của sử dụng máy tính nhân tạo là " đề xuất→ 批准人类→执行", đối phó với giai đoạn 15·15 đề xuất-sau-thành 模式。

## Mục tiêu học tập

- Thiết kế một vòng tròn tác nhân đa phương thức: nhận thức → lý do → hành động → quan sát → lặp lại.
  设计多模态 Trình tròn:感知 → 推理 → 行动 → 观察 → 重复。
- Xây dựng một sơ đồ đầu ra đầu ra GUI (thấp xích, gõ văn bản, cuộn, kéo) VLM có thể phát ra như JSON.
  构建 GUI 定位输出模式(点击坐标、输入文字、滚动、拖),VLM 以 JSON 格式输出──
- So sánh các đại lý chỉ chụp màn hình vs đại lý cây truy cập vs đại lý lai.
  Đối với chất thải đơn giản 无障碍树 无障碍树 无障碍树 无障碍树 无障碍树 无障碍树 无障碍树 无障碍树 无障碍树 无障碍树 无障碍树 无障碍树 无障碍树 无障碍树 无障碍树 无障碍树 无障碍树 无障碍树 无障碍树 无障碍树 无障碍树 无障碍树 无障碍树 无障碍树 无障碍树 无障碍树 无障碍树 无障碍树 无障碍树 无障碍树 无障碍树 无障碍树 无障碍树 无障碍树 无障碍树 无障碍树 无障碍树 无障碍树 无障碍树 无障碍树 无障碍树 无障碍树 无障碍树 无障碍树 无障碍树 无障碍树 无障碍树 无障碍树 无障碍树 无障碍树 无障碍 无障碍树 无障碍 无障碍 无障碍树 无障碍 无障碍 无障碍 无障碍 无障碍 无障碍 无障碍 无障碍 无障碍 无障碍 无障碍 无障碍 无障碍 无障碍 无障碍 无障碍 无障碍 无障碍 无障碍 无障碍 无障碍 无障碍 无障碍 无障碍 无障碍 无障碍 无障碍 无障碍 无障碍 无障碍 无障碍 无障碍 无障 无障 无障 无障 无障 无障 无障 无障 无障 无障 无障 无障 无障 无障 无障 无障 无障 无障 无障 无 无障 无 无 无 无 无 无 无 无 无 无 无 无 无 无 无 无 无 无 无 无 无
- Thiết lập đánh giá điểm chuẩn của đại lý đa phương thức trên một đoạn nhỏ của VisualWebArena.
  Trong VisualWebArena, tập hợp nhỏ xây dựng nhiều mô hình Agent 基准评估。

## Vấn đề được định nghĩa

> **【中文解读】**Ví dụ: Trình duyệt cần cắt ảnh trang trình duyệt, phân tích cắt ảnh + URL + mục tiêu tạo kế hoạch, xuất động cấu trúc (output structured) click 坐标, nhập chữ,滚动, chọn), thực hiện động tác trên trình duyệt, quan sát trạng thái mới, vòng lặp cho đến khi nhiệm vụ hoàn thành.

Một quy trình làm việc tại chỗ đặt chỗ: "đặt cho tôi một chuyến bay đến Tokyo vào ngày 15 tháng 4, chỗ ngồi dưới 800 đô la, đặt nó".

> Một dòng người dùng: "Help me find 4 月 15 日飞东京的航班,靠走道, $800 以下,预订. "

Một đại lý đa phương tiện cần:

> 多模态 Trực sự 需要:

1. Hãy chụp ảnh màn hình của trình duyệt.
   Trung ngữ翻译:截取浏览器屏幕截图──
2. Phân tích ảnh chụp màn hình + URL + mục tiêu thành một kế hoạch.
   中文翻译:解析截图 + URL + 目标,生成计划。
3. Tạo một hành động có cấu trúc: nhấp vào (ở x,y), gõ "Tokyo" (ở phần tử E), cuộn xuống, chọn (phím radio).
   中文翻译:输出结构化动作:点击(x,y) 、输入"Tokyo"(元素 E) 、向下滚动、选择(单选按) ✿
4. Đưa hành động vào trình duyệt.
   Trung ngữ翻译:在浏览器上执行动作──
5. Xem trạng thái mới (bức ảnh màn hình tiếp theo).
   Trung ngữ翻译:观察新状态 (năm mới)
6. Lặp lại cho đến khi hoàn thành nhiệm vụ.
   Trung ngữ翻译:重复直到任务完成──

Mỗi bước là một cuộc gọi VLM đa phương thức. Khả năng xuất VLM phải là JSON có thể phân tích. Các lỗi liên tục trong các bước, vì vậy phục hồi quan trọng.

> Mỗi bước là một lần nhiều mô hình VLM 调用──VLM 输出 phải là JSON có thể phân tích── lỗi trong bước trong tích lũy, do đó cơ chế phục hồi rất quan trọng──

## Khái niệm cốt lõi

> **【中文解读】**多模态 Agent (tương tự như Computer Use Agent) để AI trực tiếp điều hành giao diện máy tính:截图理解屏幕内容,生成鼠标/键盘操作―― đây là ứng dụng cuối cùng của多模态理解.

> **【拓展：Computer Use 的前沿**Sử dụng máy tính của Anthropic 让 Claude 直接操作桌面应用,完成网页浏览、表单填写等任务──OpenAI của Operator 使用类似方法──关键技术挑战:精确定位(准确点击按) 、状态跟踪(理解界面变化)、错误恢复(操作失败后重试)──


### GUI đặt đất  nguyên thủy  GUI  định vị  cơ sở nguyên ngữ

GUI đặt đất là: được chụp màn hình và hướng dẫn ngôn ngữ tự nhiên, xuất x, y phối hợp để nhấp vào (hoặc hành động khác).

> GUI 定位是:给定一张截图和自然语言指令,输出需要点击的 (x, y) 坐标(或其他动作)

> **【中文解读】**GUI 定位是:给定一张截图和自然语言指令,输出需要点击的 (x, y) 坐标(或其他动作) ――SeeClick là kết quả mở rộng lớn đầu tiên,CogAgent 增加了1120x1120 mã mã độ phân giải cao,Ferret-UI 聚焦移动端 UI──输出格式通常是JSON,`element_desc`字段帮助恢复当坐标在截图间漂移时,语义提示让系统重新定位──

SeeClick (arXiv:2401.10935) là kết quả mở đầu tiên ở quy mô: điều chỉnh tinh tế một VLM trên dữ liệu GUI tổng hợp + thực, phối hợp đầu ra như các token văn bản đơn giản.

> SeeClick là kết quả mở rộng lớn đầu tiên: trong tổng hợp + thực GUI dữ liệu trên VLM, với mã thông báo văn bản thuần túy 输出坐标──有效──

CogAgent (arXiv:2312.08914) đã thêm mã hóa độ phân giải cao 1120x1120 cho các UI dày đặc. Điểm số: ~84% trên định hướng web.

> CogAgent cho UI mật thiết thêm 1120x1120 mã mã độ phân giải cao.

Ferret-UI (arXiv:2404.05719) tập trung vào UI di động, tích hợp với dữ liệu truy cập iOS.

> Ferret-UI 聚焦移动端 UI,集成 iOS 无障碍数据──

Phương thức đầu ra thường là JSON:

> 输出格式 thường là JSON:

```json
{"action": "click", "x": 384, "y": 220, "element_desc": "Search button"}
```

- `element_desc`giúp phục hồi: nếu các phối hợp di chuyển giữa các ảnh chụp màn hình, gợi ý ngữ nghĩa cho phép hệ thống tái đặt đất.

> `element_desc`帮助恢复: Nếu坐标在截图间漂移,语义提示让系统重新定位──

### Các kế hoạch hành động

Một kế hoạch hành động điển hình có 6-10 loại hành động:

> Mô hình động tác điển hình bao gồm 6-10 loại động tác:

> **【中文解读】**Mô hình động tác điển hình bao gồm 6-10 loại động tác: click(点击) √type(输入) √ scroll(滚动) √drag(拖) √select(选择) √hover(悬停) √navigate(导航) √wait(wait) √ done) √完成 (※Agent Mỗi bước输出一个动作,浏览器包装器执行后返回新状态――

- `click`(x, y)
  Trung ngữ翻译:`click`:点击 (x, y)
- `type`: (text, x?, y?)
  Trung ngữ翻译:`type`:输入文本,可选位置──
- `scroll`: (nghĩa, số lượng)
  Trung ngữ翻译:`scroll`:滚动(方向,量)
- `drag`(x0, y0, x1, y1)
  Trung ngữ翻译:`drag`Từ (x0, y0) 拖到 (x1, y1)
- `select`: (option_index)
  Trung ngữ翻译:`select`: chọn lựa
- `hover`(x, y)
  Trung ngữ翻译:`hover`:悬停 (x, y) 』
- `navigate`: (url)
  Trung ngữ翻译:`navigate`Đưa đến URL:
- `wait`(ms)
  Trung ngữ翻译:`wait`: chờ vài giây
- `done`: (sự thành công, giải thích)
  Trung ngữ翻译:`done`:完成(成功/失败,解释)

Các đại lý phát ra một hành động mỗi bước. Bỏ trình duyệt thực hiện và trả lại trạng thái mới.

> Agent mỗi bước输出一个动作──浏览器包装器执行后返回新状态──

### Chỉ chụp màn hình và cây truy cập.

> **【中文解读】**2 kiểu nhập khẩu: mô hình cắt tỉa đơn giản phổ biến nhất nhưng độ chính xác thấp hơn; cây không có cản trở (DOM/iOS 信息无障碍) đáng tin cậy hơn nhưng chỉ có thể sử dụng trong dữ liệu cấu trúc; mô hình hỗn hợp sử dụng cùng lúc cả hai, cây dùng cho định vị động động nguyên tử, cắt tỉa dùng cho ngữ nghĩa hiểu biết.

Hai chế độ đầu vào:

> 两种输入模式:

- Chỉ chụp màn hình: hình ảnh đầy đủ, không có thông tin cấu trúc.
  Trung ngữ翻译:纯截图:完整图像,无结构信息──最通用;适用于任何应用──
- Cây truy cập: thông tin truy cập DOM / iOS có cấu trúc. đáng tin cậy hơn nhiều cho việc hạ cánh; hoạt động khi cây có sẵn.
  Trung文翻译:无障碍树:结构化 DOM / iOS 无障碍信息──定位更可靠;在有树数据时可用──
- Hybrid: cả hai, với cây như là một nền đáng tin cậy cho các hành động nguyên tử và ảnh chụp màn hình cho ngữ cảnh.
  Trung ngữ翻译:混合:两者都用,树用于原子动作定位,截图用于语义理解。

Các đại lý sản xuất sử dụng hybrid khi có thể. Tự động hóa trình duyệt (Selenium + khả năng truy cập) luôn có cây; các ứng dụng máy tính để bàn đôi khi làm.

> 生产 Agent 尽可能使用混合模式;;浏览器自动化(Selenium + 无障碍) luôn có cây; 桌面应用有时有;;

### Khoảnh khắc dài hạn 长期记忆

Một dòng công việc 20 bước tạo ra 20 ảnh chụp màn hình.

> 20 bước làm việc dòng chảy tạo ra 20 张截图──VLM 上下文快快填满──三种压缩策略:

> **【中文解读】**20 bước công việc dòng tạo ra 20 张截图,VLM 上下文快速填满──三种缩略策略:摘要链(每5 bước总结一次,丢弃旧截图) 跳(保留首尾和每第3张) 、工具记录日志(只保留文本日志不看旧截图)──Claude's computer use API 使用日志模式,更简单可靠──

- Summary-chain: sau mỗi 5 bước, tóm tắt những gì đã xảy ra, thả các ảnh chụp màn hình cũ.
  Trung ngữ翻译:摘要链: mỗi 5 步总结 đã xảy ra, bỏ qua đoạn kết cũ.
- Skip-frame: giữ lần đầu tiên, cuối cùng, và mỗi lần chụp màn hình thứ 3.
  Trung文翻译:跳:保留首、尾和每第 3 张截图──
- Lập nhật ký ghi lại công cụ: thực hiện các hành động, giữ nhật ký văn bản về những gì đã được thực hiện; không nhìn lại ảnh chụp màn hình cũ.
  Trung văn翻译:工具记录日志:执行动作,保留文本日志;不重新查看旧截图──

API sử dụng máy tính của Claude sử dụng mô hình nhật ký đơn giản hơn, đáng tin cậy hơn.

> Máy tính của Claude sử dụng API sử dụng 日志模式──更简单,更可靠──

### Sử dụng công cụ hình ảnh Sử dụng công cụ hình ảnh

> **【中文解读】**ChartAgent  giới thiệu Visual Tool调用:Agent có thể xuất " cắt vùng (100,200,300,400) rồi调用 OCR" như một tool调用.

ChartAgent (arXiv:2510.04514) giới thiệu việc sử dụng công cụ trực quan để hiểu biểu đồ: crop, zoom, OCR, gọi phát hiện bên ngoài.

> ChartAgent 引入视觉工具调用用于图表理解:剪剪,缩放,OCR、调用外部检测──Agent có thể输出"剪到区域 (100, 200, 300, 400) 然后调用OCR"作为工具调用──工具返回文本;VLM 继续推理──

Mô hình này tổng quát: set-of-mark prompting, vùng ghi chú, và công cụ phát hiện bên ngoài tất cả phù hợp với cùng một "output một tool call, nhận một phản ứng có cấu trúc" sơ đồ.

> Mô hình này có thể được quảng bá: tập hợp dấu hiệu gợi ý, dấu hiệu khu vực và các công cụ kiểm tra bên ngoài đều phù hợp với cùng một mô hình "các công cụ xuất khẩu, nhận, đáp ứng cấu trúc".

### Các điểm chuẩn năm 2026

> **【拓展：多模态 Agent 基准全景】**ScreenSpot-Pro 测试 GUI 定位(开放模型 ~85%,前沿 ~90%);VisualWebArena 测试端到端网页任务(开放模型 ~20%,Gemini 3 Pro ~27%);AgentVista là 2026 最难基准,覆盖 12 个领域的真实工作流,前沿模型只有 27-40%;WebArena/WebShop 已被前沿模型和──

- ScreenSpot Pro. GUI đặt đất trên ~ 1k ảnh màn hình web. mở SOTA Qwen2.5-VL-72B ~85%.
  Trung文翻译:ScreenSpot-Pro。 khoảng 1k 网页截图 GUI 定位──开放 SOTA Qwen2.5-VL-72B 约 85%──前沿约 90%──
- VisualWebArena. Các công việc web kết thúc đến kết thúc (thửa hàng, diễn đàn, quảng cáo). SOTA mở ~ 20%. Gemini 3 Pro ~ 27%.
  Trung文翻译:VisualWebArena。端到端网页任务(购物、论坛、分类广告)。开放 SOTA 约20%──Gemini 3 Pro 约27%──
- AgentVista (arXiv:2602.23166). Định điểm chuẩn khó nhất năm 2026.
  Trung文翻译:AgentVista──2026 年最难基准──跨 12 领域真实工作流──前沿模型 27-40%;开放模型 10-20%──
- WebArena / WebShop. Định nghĩa tiêu chuẩn cũ hơn; bão hòa bởi biên giới.
  Trung文翻译:WebArena / WebShop。旧基准;已被前沿模型和。

### Tại sao vẫn khó khăn? Tại sao vẫn khó khăn?

> **【中文解读】**Agent 性能瓶:1) 细粒度视觉定位("点击小 X"在移动分辨率下经常失败);2) 长期规划(10 步后 Agent 偏离目标);3) 错误恢复(点击失败时检测和恢复缺乏训练数据);4) 跨页面上下文(跳转标签页面或长表单丢失状态) ――研究方向包括记忆架构、、式重规划多样式验证――

Khân khói hiệu suất của chất:

> Thuốc 性能瓶:

1. "Click the small X" thường thất bại khi phân giải di động.
   Trung文翻译:细粒度视觉定位──"点击小 X"在移动分辨率下经常失败──
2. Sau 10 hành động, nhân viên sẽ rời khỏi mục tiêu.
   Trung文翻译:长期规划──10 个动作后 代理 偏离目标──
3. Khôi phục lỗi: Khi một nhấp chuột không thành công (phím sai), phát hiện + phục hồi hiếm khi là dữ liệu được đào tạo.
   Trung文翻译:错误恢复──点击失败时(按错按),检测+恢复缺乏训练数据──
4. Mối quan điểm qua các trang. Nhảy giữa các tab hoặc các biểu mẫu dài mất trạng thái.
   Trung ngữ翻译:跨页面上下文──跳转标签页面或长表单丢失状态──

Các hướng nghiên cứu: kiến trúc bộ nhớ, lập kế hoạch lại rõ ràng, xác minh đa phương thức (chụp màn hình phù hợp với thành công hành động).

> Nghiên cứu hướng: bộ nhớ cấu trúc, hình thức tái lập kế hoạch, nhiều mô hình kiểm tra

### Đá đá cuối xây dựng nó  Dự án tốt nghiệp xây dựng

> **【中文解读】**毕业项目任务: xây dựng một máy tính sử dụng Agent,能够读取预订网站模拟页面的 HTML+截图,规划多步序列(搜索→选择→填表→提交),输出匹配动作模式的 JSON动作,并评估10 固定任务――

Nhiệm vụ cuối: xây dựng một đại lý sử dụng máy tính mà:

> 毕业项目任务: xây dựng một máy tính sử dụng Agent, yêu cầu:

1. Đọc ảnh chụp màn hình HTML + của trang giả trang trang đặt chỗ.
   Trung ngữ翻译:读取预订网站模拟页面的HTML + 截图──
2. Kế hoạch một chuỗi nhiều bước: tìm kiếm → chọn → điền biểu mẫu → gửi.
   中文翻译:规划多步序列:搜索→选择→填表→提交──
3. Phát hành các hành động JSON phù hợp với sơ đồ hành động.
   Trung ngữ翻译:输出匹配动作模式的 JSON 动作.
4. Đánh giá trên một mảnh cố định 10 nhiệm vụ.
   Trung文翻译: 在固定的10个任务上评估──

Bài học cung cấp mã treo mà dễ dàng mở rộng vào một trình duyệt thực sự.

> 课程 cung cấp mã viết tay, dễ dàng mở rộng đến trình duyệt thực tế.

## Hãy sử dụng nó để thực hiện
```figure
mm-agent-loop
```

## Sử dụng nó

`code/main.py`là sàn đá cột:

- Action schema JSON definition (10 hành động).
  Trung ngữ翻译:动作模式 JSON 定义(10种动作)
- Tờ trạng thái trình duyệt giả như lệnh.
  中文翻译:模拟浏览器状态 (字典)
- Cơ thể vòng tròn của đại lý: nhận trạng thái, phát hành hành động, áp dụng, vòng tròn.
  Trung文翻译:Agent 循环骨架:接收状态、输出动作、执行、循环。
- 10 nhiệm vụ mini-benchmark (đảng tổng hợp) để đo lường tỷ lệ thành công từ đầu đến cuối.
  Trung ngữ翻译:10 任务迷你基准(合成页面) đo lường kết thúc đến kết thúc tỷ lệ thành công.
- Cây cắm lỗi để khi hành động thất bại.
  Trung ngữ翻译:动作失败时的错误恢复子──

## Chuyển nó đi.

Bài học này sẽ mang lại kết quả `outputs/skill-multimodal-agent-designer.md`. Với một sản phẩm sử dụng máy tính (khu vực, bộ hành động, mục tiêu đánh giá), thiết kế vòng tròn đầy đủ của đại lý, chiến lược bộ nhớ, chế độ đặt đất và điểm chuẩn dự kiến.

> 本课产 出 `outputs/skill-multimodal-agent-designer.md` Định dạng các sản phẩm sử dụng máy tính (nơi sử dụng máy tính), thiết kế đầy đủ của Agent vòng, chiến lược nhớ, định vị mô hình và dự đoán cơ sở phân tích.

## Tập luyện bài tập

1. Chuyển rộng kế hoạch hành động bằng một `screenshot_region`công cụ (crop + zoom). Những nhiệm vụ nào có lợi?
   扩展动作模式, thêm `screenshot_region`工具(裁剪+缩放) ◊ những nhiệm vụ nào sẽ được hưởng lợi?

2. Đọc AgentVista (arXiv:2602.23166). Mô tả danh mục nhiệm vụ khó khăn nhất và lý do tại sao các mô hình biên giới vẫn thất bại.
   阅读 AgentVista 论文── mô tả các loại nhiệm vụ khó khăn nhất và nguyên nhân tại sao mô hình phía trước vẫn thất bại──

3. Nhiệm độ nén chân trời dài: thiết kế chuỗi tổng kết với ≤4 ảnh chụp màn hình được giữ trực tiếp, bất kỳ số nào được ghi lại.
   长期记忆压缩: thiết kế một chuỗi tóm tắt, giữ ≤4张截图活跃, số lượng tùy ý ghi đến日志。

4. Xây dựng một cái nát lỗi-chăm phục hồi: khi hành động thất bại (phím không tìm thấy), đại lý làm gì tiếp theo?
   构建错误恢复子:当动作失败 (按未找到) 时,Agent 下一步做什么?

5. So sánh chỉ chụp màn hình Claude 4.7 với chụp màn hình hybrid + cây truy cập Qwen2.5 - VL trên 10 nhiệm vụ web.
   So với các tác phẩm của Claude 4.7 trong 10 trang web, mỗi tác phẩm đã thành công trong các loại nào?

## Từ khóa  Keyword

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|------------------------|----------|
| GUI grounding | "Click coordinates" | Model outputs (x,y) for the target of an instruction on a screenshot | GUI 定位：模型输出截图上指令目标的 (x,y) 坐标 |
| Action schema | "Tool definitions" | JSON description of valid actions (click, type, scroll, drag) | 动作模式：有效动作的 JSON 描述 |
| Accessibility tree | "Structured DOM" | Machine-readable UI hierarchy from browser/iOS APIs | 无障碍树：来自浏览器/iOS API 的机器可读 UI 层级 |
| Hybrid agent | "Screenshot + tree" | Uses both image and structured info; more reliable than either alone | 混合 Agent：同时使用图像和结构化信息 |
| Visual tool use | "Zoom/crop/detect" | Agent calls external vision tools (OCR, detection) mid-plan | 视觉工具使用：Agent 在规划中调用外部视觉工具 |
| Summary-chain | "Memory compression" | Periodic text summaries replace long screenshot history | 摘要链：定期文本摘要替代长截图历史 |
| VisualWebArena | "E2E web bench" | 2024 benchmark for end-to-end web tasks | 端到端网页任务基准（2024） |
| AgentVista | "2026 hard bench" | 12-domain realistic workflows; even Gemini 3 Pro scores ~30% | 12 领域真实工作流基准，前沿模型仅约 30% |

## Xem thêm 延伸阅读

- [Cheng et al. — SeeClick (arXiv:2401.10935)](https://arxiv.org/abs/2401.10935)
- [Hong et al. — CogAgent (arXiv:2312.08914)](https://arxiv.org/abs/2312.08914)
- [You et al. — Ferret-UI (arXiv:2404.05719)](https://arxiv.org/abs/2404.05719)
- [ChartAgent (arXiv:2510.04514)](https://arxiv.org/abs/2510.04514)
- [Koh et al. — VisualWebArena (arXiv:2401.13649)](https://arxiv.org/abs/2401.13649)
- [AgentVista (arXiv:2602.23166)](https://arxiv.org/abs/2602.23166)
