# Các nền tảng LLM quản lý  Bedrock, Vertex AI, Azure OpenAI

> Ba siêu quy mô, ba chiến lược khác nhau. AWS Bedrock là một thị trường mô hình  Claude, Llama, Titan, ổn định, Cohere đằng sau một API. Azure OpenAI là một quan hệ đối tác OpenAI độc quyền cộng với các đơn vị thông qua được cung cấp (PTU) cho công suất chuyên dụng. Vertex AI là Gemini đầu tiên với câu chuyện dài và đa phương tiện tốt nhất. Năm 2026, Phân tích nhân tạo đo Azure OpenAI ở ~ 50 ms trung bình và Bedrock ở ~ 75 ms trên tương đương Llama 3.1 405B  PTU giải thích khoảng cách bởi vì năng lượng chuyên dụng đánh bại chia sẻ theo yêu cầu. Quy tắc quyết định không phải là "các mô hình nào nhanh nhất" mà là "mô hình nào và bề mặt FinOps phù hợp với sản phẩm của tôi". Bài học này dạy bạn chọn với các sự thỏa hiệp được ghi lại, không phải là xung.

> **【中文解读】**Bài viết này giới thiệu về các lựa chọn và đối tác của các nền tảng dịch vụ mô hình được cung cấp bởi OpenAI, Anthropic, Google và các nền tảng khác.

>  **【前置】**Học本节前请先掌握:Phase 11 (LLM Engineering)全部你已经会使用OpenAI/Anthropic API 调模型;Phase 13 (Tools & Protocols) 理解 MCP等协议。本节讲生产部署选哪个云不是技术问题,是商业+合规+技术综合决策。

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy cost-and-latency comparator) | **语言:** Python（标准库，成本-延迟比较器）
**Prerequisites:** Phase 11 (LLM Engineering), Phase 13 (Tools & Protocols) | **前置知识:** Phase 11（LLM 工程）, Phase 13（工具与协议）
**Time:** ~60 minutes | **时间:** ~60 分钟

## Mục tiêu học tập

- Hãy nêu tên ba chiến lược nền tảng (trọng trường vs độc quyền vs Gemini-lần đầu tiên) và phù hợp với từng trường hợp sử dụng sản phẩm.

>  **【类比】**三大云平台 LLM 服务 = 三种餐厅:(1) **AWS Bedrock**= 美食广场(一个API 调多家模型,Claude/Llama/Titan,灵活但延迟略高);(2) **Azure OpenAI**= 米其林餐厅(OpenAI 独家合作,PTU 专属容量,延迟最低 ~50ms, nhưng tốn kém và bị ràng buộc OpenAI);(3) **Vertex AI**= 主题餐厅(Google Gemini 主打,长上下文和多模态最强,2M token 窗口) ――选择哪个看你的菜谱(用Claude 还是GPT 还是 Gemini) 和预算──

> ️ **【易错点】**托管平台选型的 3 个坑:(1) **只看标价**Bedrock 上 Claude 比 Anthropic 直连贵 15-20% (云税), nhưng合规和统一计值钱;做 TCO (总拥有成本) chứ không phải đơn giá比较 ()**忽略数据驻留** Dữ liệu người dùng châu Âu phải ở lại châu Âu, chọn Azure EU 区域 hoặc Bedrock eu-central-1; truyền dữ liệu xuyên biên giới vi phạm GDPR。(3) **没做厂商锁定评估** sử dụng OpenAI PTU 后想换 Bedrock 需重写 SDK 和 prompt 格式; sử dụng LiteLLM 等抽象层降低锁风险──
  Trung ngữ翻译:说出三种平台策略(集市 vs 独家合作 vs Gemini 优先),并将每种匹配到产品用例──
- Giải thích các đơn vị thông qua được cung cấp (PTU) mua cho bạn trong Azure OpenAI và tại sao Bedrock theo yêu cầu thường đọc chậm hơn ~ 25 ms ở thang 405B.
  Trung ngữ翻译:解释 Azure OpenAI's preposition吞吐量单位 (PTU) đã mang lại điều gì, và tại sao Bedrock 按量部署 ở quy mô 405B thường chậm khoảng 25ms.
- Chụp đồ thị bề mặt thuộc về FinOps cho mỗi nền tảng (Bedrock Application Inference Profiles vs Vertex project-per-team vs Azure scopes + PTU reservations).
  Trung文翻译:绘制各平台的 FinOps 归因界面(Bedrock Application Inference Profiles vs Vertex 项目-per-团队 vs Azure 作用域 + PTU 预留)
- Viết ra một chính sách "mức tối thiểu hai nhà cung cấp" và giải thích tại sao khóa vào một nhà cung cấp là sai lầm đắt tiền vào năm 2026.
  Trung ngữ翻译:写下"双供应商最低"策略,并解释为什么单供应商锁定是2026年昂贵的错误――

## Vấn đề  vấn đề giới thiệu

Bạn đã chọn Claude 3.7 Sonnet cho sản phẩm của mình. Bây giờ bạn cần phải phục vụ nó. Bạn có thể gọi API Anthropic trực tiếp, hoặc bạn có thể gọi nó thông qua AWS Bedrock, hoặc bạn có thể đi qua một cổng thông tin. API trực tiếp là đơn giản nhất; Bedrock thêm BAAs, điểm cuối VPC, IAM và CloudWatch thuộc tính. Cổng thông tin thêm failover, hóa đơn thống nhất và giới hạn tỷ lệ trên các nhà cung cấp.

> Bạn đã chọn sản phẩm Claude 3.7 Sonnet. Bây giờ cần triển khai nó. Bạn có thể trực tiếp điều khiển API Anthropic, cũng có thể thông qua AWS Bedrock.

Câu hỏi sâu hơn là danh mục. Nếu bạn cần Claude và Llama và Gemini trong cùng một sản phẩm, bạn không thể mua tất cả chúng từ một nơi trừ khi nơi đó là Bedrock cộng với Vertex cộng với Azure OpenAI cùng một lúc.

> Một vấn đề sâu sắc hơn là danh sách mô hình. Nếu bạn cần Claude, Llama và Gemini trong cùng một sản phẩm, bạn không thể mua tất cả các mô hình từ một nơi, trừ khi sử dụng đồng thời Bedrock + Vertex + Azure OpenAI.

Bài học này mô tả ba cược, khoảng cách trễ, khoảng cách FinOps và rủi ro khóa.

> Bài học này đã vẽ ra ba điểm: 注,延迟差距, FinOps 差距, và khóa风险.

> **【中文解读】**选择 LLM 后, "在哪里部署" là một quyết định cấp cơ sở hạ tầng. 直接调用 API 最简单,但缺乏企业级控制; 通过云平台(Bedrock/Vertex/Azure)调用增加了合规、审计能力; 通过网关调用则获得多供应商容量和统计费用.

> **【拓展：LLM 部署模式】**Các dự án mạng AI như OpenRouter, Portkey, LiteLLM và các dự án mạng AI khác được sử dụng rộng rãi vào năm 2025, giá trị cốt lõi là cung cấp kết nối thống nhất giữa nhiều nhà cung cấp, tự động không kết nối và tối ưu hóa chi phí. Trong các dự án trên cấp doanh nghiệp, khoảng 60% đã sử dụng mô hình mạng AI (Gartner 2025 AI Infrastructure Report)

## Khái niệm cốt lõi

> **【中文解读】**Chiến lược của các nhà sản xuất 3 đại đám mây LLM là khác nhau: AWS Bedrock là "đồng thị trường mô hình", tập hợp nhiều nhà cung cấp; Azure OpenAI là "sự hợp tác độc lập", chuyên về mô hình OpenAI; Vertex AI là "đồng ưu tiên", để vượt lên trên văn bản và năng lực đa phương tiện để bán điểm.

> **【拓展：全球 LLM 云平台格局】**Ngoài ba siêu quy mô bên ngoài, năm 2026 đáng quan tâm còn có: Cloudflare Workers AI(边缘推理) ✓ Cùng với AI(开源模型推理平台, $0.18/M mã thông báo cho Llama 3.1 70B) ✓ Groq(LPU 推理引擎,TTFT < 20ms) ✓ Cerebras(CS-3 wafer-scale 推理,2000+ mã thông báo/s)  trong nước có hàng trăm ngàn ✓帆阿里百炼、火山方舟等, nhưng danh mục mô hình không kết nối với các nền tảng quốc tế.

### Ba chiến lược

**AWS Bedrock** thị trường. Claude (Anthropic), Llama (Meta), Titan (AWS first-party), Stability (image), Cohere (embeddings), Mistral, cộng với hình ảnh và nhúng các danh mục phụ. Một API, một bề mặt IAM, một xuất CloudWatch. Bedrock đặt cược là khách hàng muốn tùy chọn hơn họ muốn một mô hình duy nhất.

> **AWS Bedrock** 模型集市──Claude(Anthropic)、Llama(Meta)、Titan(AWS 自有)、Stability(图像)、Cohere(嵌入)、Mistral,以及图像和嵌入子目录──一个API、一个IAM 界面、一个CloudWatch 导出──Bedrock 的注是客户想要可选择性而不是单一模型──

**Azure OpenAI** hợp tác độc quyền. Bạn có được GPT-4 / 4o / 5 / o-series, DALL·E, Whisper, và điều chỉnh tinh tế các mô hình OpenAI trong các trung tâm dữ liệu Azure. Không có mô hình không phải OpenAI trong danh mục "Azure OpenAI Service"  những người đi đến Azure AI Foundry (sản phẩm riêng biệt).

> **Azure OpenAI** 独家合作──你在Azure 数据中心获得GPT-4/4o/5/o 系列、DALL·E、Whisper 和 OpenAI 模型微调──"Azure OpenAI Service" 目录中没有非 OpenAI 模型那些在Azure AI Foundry(独立产品) 中──Azure 注是OpenAI 保持前沿地位和客户想要对此关系的企业级控制──

**Vertex AI** Gemini đầu tiên, tất cả mọi thứ khác thứ hai. Gemini 1.5 / 2.0 / 2.5 Flash và Pro, cộng với Model Garden (các bên thứ ba). Vertex đặt cược là đa phương thức ngữ cảnh dài  1M-token Gemini ngữ cảnh là sự khác biệt.

> **Vertex AI** Gemini 优先,其他其次──Gemini 1.5/2.0/2.5 Flash 和 Pro,加上 Model Garden(第三方)──Vertex 的注是多模态长上下文1M 代币的 Gemini 上文是差异化因素──

### Khoảng cách độ trễ ở quy mô

Phân tích nhân tạo chạy các điểm chuẩn liên tục. Trên các triển khai tương đương Llama 3.1 405B (cùng theo yêu cầu), độ trễ trung bình của token đầu tiên của Azure OpenAI là khoảng 50 ms; Bedrock là khoảng 75 ms. Sự khác biệt không phải là sự thất bại của AWS  nó là sự khác biệt về mô hình năng lực. Azure bán PTU (Provisioned Throughput Units), dự trữ dung lượng GPU cho người thuê nhà của bạn. Đồng bằng của Bedrock (Provisioned Throughput) tồn tại nhưng bắt đầu khoảng $ 21 / giờ mỗi đơn vị, và hầu hết khách hàng vẫn ở trên chia sẻ theo yêu cầu.

> Phân tích nhân tạo 运行持续基准测试。在等效的Llama 3.1 405B 部署) 上,Azure OpenAI 中位首代币 延迟约50ms;Bedrock 约75ms。差距不是AWS的问题而是容量模型差异──Azure 销售 PTU(预置吞吐量单位),为您租户预留 GPU 容量──Bedrock 等效功能存在但起价约21$/户小时/按量模式,大多数客户使用共享量模式──

Khả năng chia sẻ theo yêu cầu cạnh tranh với lưu lượng truy cập của mọi khách hàng khác. Khả năng chuyên dụng không. Nếu SLA sản phẩm của bạn là TTFT < 100 ms tại P99, bạn hoặc mua PTU trên Azure, mua Bedrock Provisioned Throughput, hoặc chấp nhận sự khác biệt mặc định.

> 按量共享容量与所有其他客户的流量竞争 GPU资源──专用容量不会──如果你的产品 SLA是 P99 TTFT < 100ms,你要么在Azure 购买PTU,要么购买Bedrock Provisioned Throughput,要么接受默认方差──

> **【中文解读】**延迟差距的本质是"容量模型"差异――在共享按量部署中,你的请求与其他客户的流量竞争 GPU资源;专用容量(PTU)则保留独占的 GPU――Azure PTU在 40-60%的利用率时可节省高达70%的成本,但空时仍然付费――Bedrock's按量模式 TTFT 中位数约75ms,Azure PTU约50ms,25ms差距在高频交互场景中被用户感知――

### Kinh tế thông qua cung cấp

Azure PTU: một khối dự trữ của tính toán suy luận. Tương đương đến ~ 70% tiết kiệm so với nhu cầu cho tải trọng công việc dự đoán được. Chi phí cố định mỗi giờ bất kể lưu lượng truy cập  bạn trả tiền cho việc đặt chỗ ngay cả khi không hoạt động. Break-even thường là khoảng 40-60% sử dụng bền vững.

> Azure PTU: dự kiến tính toán khối lượng. Đối với tải trọng công việc có thể dự đoán, tỷ lệ tiết kiệm khối lượng là khoảng 70%.

Tấm thông qua được cung cấp bằng giường: $21-$50/giờ tùy thuộc vào mô hình và khu vực. Phân tích tương tự  Break-even là khoảng một nửa mức sử dụng đỉnh.

> Bedrock Provided Throughput: mỗi giờ $21-$50, phụ thuộc vào mô hình và khu vực. mô hình kinh tế tương tự.

Công suất cung cấp Vertex được bán cho mỗi SKU Gemini; giá thay đổi theo mô hình và khu vực và ít được quảng cáo công khai hơn.

> Vertex  dự định đặt dung lượng theo Gemini SKU 销售; giá khác nhau theo mô hình và khu vực, công khai thông tin ít hơn.

### bề mặt FinOps  phân biệt thực tế

**Bedrock Application Inference Profiles**là tính năng sạch nhất trên thị trường.`team`- `product`- `feature`; chuyển tất cả các cuộc gọi mô hình thông qua nó; CloudWatch phá vỡ chi phí cho mỗi hồ sơ mà không cần xử lý sau.

> **Bedrock Application Inference Profiles**là giải pháp tính toán chi phí rõ ràng nhất trên thị trường.`team``product``feature`标记配置文件; thông qua nó, tất cả các mô hình được điều chỉnh; CloudWatch  không cần xử lý sau đó có thể phân chia theo cấu hình. Ưu điểm mới năm 2025, vẫn là chương trình gốc tinh tế nhất trong đám mây siêu lớn.

**Vertex**bạn mô hình hóa mỗi nhóm như một dự án GCP, đặt nhãn trên mọi tài nguyên, và sử dụng BigQuery Billing Export + DataStudio cho các rollup.

> **Vertex**归因是项目-per-团队加无处不在标签――你将每个团队建模为一个GCP项目,放置标签在每个资源上,使用BigQuery Billing Export + DataStudio 进行汇总――工作量更大,但BigQuery 允许你对成本数据执行任意SQL――

**Azure**dựa trên phạm vi đăng ký / nhóm tài nguyên cộng với thẻ, với đặt phòng PTU như một đối tượng chi phí hạng nhất. Tags được thừa kế từ các nhóm tài nguyên, chứ không phải yêu cầu, vì vậy thuộc tính theo yêu cầu đòi hỏi các métrics tùy chỉnh của Application Insights hoặc một cổng để dán tiêu đề.

> **Azure**Tùy thuộc vào đăng ký/Resource Group Role Domain Add tags, PTU 预留 như một đối tượng chi phí thứ nhất.

Mô hình: Bedrock là bản địa sạch nhất, Vertex linh hoạt nhất thông qua BigQuery, Azure là không minh bạch nhất trừ khi bạn chơi nhạc cụ.

> 总结:Bedrock 原生最清晰,Vertex 通过 BigQuery 最灵活,Azure 除非自行埋点否则最不透明──

> **【中文解读】**FinOps (云财务运营) là một trong những nền tảng LLM được đánh giá thấp nhất. Biểu đồ Inference ứng dụng của Bedrock là hiện tại chính xác nhất về nguyên phát và tính năng của nó.

> **【拓展：LLM FinOps 实践】**企业 LLM 支出在 2025年平均增长300%(Flexera 2025 云状态报告) 常见FinOps 策略包括:(1) 按代币 消耗设置团队预算告警;(2) 使用缓存层(Semantic Cache) giảm重调约 30-40%;(3) 模型路由简单任务用小模型、复杂任务用大模型,可节省50%+ 成本;(4) 批量API在非实时场景可降低50%价格;;

### Khóa lại là rủi ro năm 2026

Lập kế hoạch đơn siêu quy mô là tốt khi một mô hình thống trị. Năm 2026 biên giới di chuyển hàng tháng  Claude 3.7 một quý, Gemini 2.5 tiếp theo, GPT-5 quý sau đó.

> Khi một mô hình chủ đạo, một đám mây hứa hẹn cũng có thể. Năm 2026 mô hình tiền tuyến hàng tháng đều thay đổi. Một mùa là Claude 3.7, một mùa tiếp theo là Gemini 2.5, một lần nữa là GPT-5.

Các nhóm làm việc theo mô hình áp dụng: tối thiểu hai nhà cung cấp cho bất kỳ cuộc gọi LLM quan trọng sản phẩm nào. Bedrock cộng với Azure OpenAI là cặp chung  Claude từ một, GPT từ một, sự cố giữa hai, cùng cổng thông tin. Việc tăng chi phí là không đáng kể vì các tuyến đường cổng tối ưu; tăng khả năng sẵn có trong thời gian bị gián đoạn (như sự cố Azure OpenAI tháng 1 năm 2025, sự cố AWS us-east-1) là quyết định.

> Mô hình sử dụng của đội ngũ cao hiệu quả: bất kỳ sản phẩm quan trọng nào LLM 调用双供应商最低策略。Bedrock + Azure OpenAI là sự kết hợp phổ biến nhất một cung cấp Claude, một khác cung cấp GPT, thông qua cùng một kết nối mạng để thực hiện chuyển đổi故障。 chi phí tăng đáng bỏ qua, vì kết nối mạng là tốt nhất; trong thời gian 机期间 khả dụng tăng lên(như Azure OpenAI năm 2025 月事件、AWS us-east-1 机) là quyết định.

> **【中文解读】**Nguy cơ cơ cơ sở hạ tầng lớn nhất năm 2026 là các nhà cung cấp khóa. Mô hình tiền tuyến mỗi quý đều thay đổi Q1 sử dụng Claude 3.7, Q2 sử dụng Gemini 2.5, Q3 sử dụng GPT-5. Lệnh khóa một nền tảng có nghĩa là có khả năng tiền tuyến hơn 2/3. Thực hành tốt nhất là "bằng nhà cung cấp tối thiểu" chiến lược:Bedrock + Azure OpenAI là hợp thể phổ biến nhất, thông qua các kết nối mạng, chi phí tăng lên có thể bỏ qua, nhưng khả năng tăng lên rõ ràng trong thời gian bị hỏng.

> **【拓展：云厂商宕机事件】**Vào tháng 1 năm 2025, Azure OpenAI đã trải qua một số giờ cố tình toàn diện, ảnh hưởng đến tất cả các khách hàng doanh nghiệp ChatGPT của Azure duy nhất. Cũng trong năm đó, AWS us-east-1 khu vực cũng xảy ra sự cố nghiêm trọng. Chiến lược của nhiều nhà cung cấp trong những sự kiện này chứng minh giá trị của nó: khi một 机, các mạng lưới sẽ tự động chuyển lưu lượng sang một thời gian khác, thực hiện chuyển đổi lỗi cảm giác.

### Data residency, BAA và các ngành công nghiệp được quy định

Bedrock: BAA ở hầu hết các khu vực; điểm cuối VPC; vỉa hè.
Azure OpenAI: HIPAA, SOC 2, ISO 27001; cư trú dữ liệu EU; mặc định do doanh nghiệp quy định.
Vertex: HIPAA, GDPR, cư trú dữ liệu theo khu vực; Google Cloud's compliance stack.

> Bedrock:多数区域提供 BAA; VPC 端点;防护──常见金融科技默认选择──
> Azure OpenAI:HIPAA、SOC 2、ISO 27001; EU 数据驻留;企业监管默认选择。
> Vertex:HIPAA、GDPR、according to regional data residing;Google Cloud's compliance──

Tất cả ba đều đáp ứng các hộp kiểm cơ bản. Sự khác biệt là các chính sách lưu trữ dữ liệu, cách xử lý nhật ký, và liệu giám sát lạm dụng có đọc lưu lượng truy cập của bạn (đưa chọn mặc định trên hầu hết; chọn bỏ sẵn cho doanh nghiệp).

> 三者都满足基本合规要求── khác biệt nằm ở các chiến lược lưu trữ dữ liệu、日志 xử lý và việc lạm dụng giám sát xem liệu lưu lượng của bạn có được đọc không.

### Những con số mà bạn nên nhớ

- TTFT trung bình của Azure OpenAI trên tương đương Llama 3.1 405B: ~ 50 ms (với PTU).
  Trung文翻译:Azure OpenAI 在 Llama 3.1 405B 等效模型上的中位 TTFT:~50ms(使用PTU)。
- TTFT trung bình trên nhu cầu: ~ 75 ms.
  Trung文翻译:Bedrock 按量模式中位 TTFT:~75ms。
- Tấm thông qua được cung cấp bằng giường: $21-$50/h/ đơn vị.
  中文翻译:Bedrock Provided Throughput: mỗi单位 $21-$50/小时.
- Azure PTU Break-Even: ~ 40-60% sử dụng bền vững.
  Trung文翻译:Azure PTU 亏平衡点:~40-60% 持续利用率。
- Tiết kiệm PTU so với nhu cầu khi sử dụng cao: lên đến 70%.
  Trung ngữ翻译:PTU trong tỷ lệ sử dụng cao tương đương với khối lượng mô hình tiết kiệm lên đến 70%

## Hãy sử dụng nó để thực hiện
```figure
i4-platform-lanes
```

## Sử dụng nó

`code/main.py`So sánh ba nền tảng trên một khối lượng công việc tổng hợp  nó mô hình về kinh tế theo yêu cầu so với PTU, sự khác biệt TTFT và độ trung thành quy định chi phí.

> `code/main.py`Trong tổng hợp tải trọng làm việc so sánh ba nền tảng nó xây dựng khối lượng so với PTU  kinh tế tính, TTFT  tỷ lệ khác biệt và chi phí do tính bảo mật.

> **【中文解读】**实践部分通过模拟工作负载对比三大平台──关键指标包括:TTFT(首代币延迟)、吞吐量、每百万代币 成本──通过调整利用率参数,可以直观看PTU 在什么负载水平下比按量计费更划算──

## Chuyển nó đi.

Bài học này sẽ mang lại kết quả `outputs/skill-managed-platform-picker.md`. Với một hồ sơ tải trọng công việc (mô hình cần thiết, TTFT SLA, khối lượng hàng ngày, yêu cầu tuân thủ), nó khuyên nên một nền tảng chính, một sự suy giảm và một kế hoạch dụng cụ FinOps.

> 本课产 出 `outputs/skill-managed-platform-picker.md` Đặt ra các tập tin định kỳ, các chương trình dự án và các chương trình dự án.

> **【拓展：生产环境平台选型 Checklist】**生产环境 LLM 平台选型应考虑:(1) 模型目录是否覆盖所需模型;(2) 延迟 SLA 是否满足用户体验要求(对话 < 200ms TTFT,批处理无严格要求);(3) 合规认证(HIPAA/SOC2/ISO27001);(4) 数据驻留(GDPR 要求 EU 区域存储);(5) 成本归因粒度(能否按团队/产品拆分账单);(6) 容灾方案(多区域/多应供商失败)

## Tập luyện bài tập

1. Đi chạy`code/main.py`- Azure PTU vượt qua theo yêu cầu cho một mô hình lớp 70B ở mức sử dụng bền vững nào?
   Trung ngữ翻译:运行 `code/main.py`◊ Blue PTU trong những gì ở mức sử dụng liên tục so với mô hình lớp 70B tốt hơn mô hình khối lượng?
2. Sản phẩm của bạn cần Claude 3.7 Sonnet và GPT-4o. Thiết kế một triển khai hai nhà cung cấp  đi đến hypercaler nào, cửa cổng nào ở phía trước, chính sách lỗi là gì?
   Trung ngữ翻译:你的产品需要Claude 3.7 Sonnet 和 GPT-4o──设计双供应商部署哪到哪个云商,前面放什么网关,故障转移策略是什么?
3. Một khách hàng chăm sóc sức khỏe được quy định yêu cầu BAA, cư trú dữ liệu Đông Mỹ và sub-100ms P99 TTFT. Chọn một nền tảng và biện minh với ba tính năng cụ thể.
   Trung ngữ翻译: một khách hàng chăm sóc sức khỏe được quản lý cần BAA, Mỹ-Thương số liệu cư trú và P99 TTFT < 100ms.
4. Nếu không có hồ sơ thông tin, làm thế nào bạn sẽ tìm ra kẻ phạm tội?
   Trung ngữ翻译:你发现本月Bedrock 账单翻了4倍但流量未变──没有应用推理资料 怎么找到原因?有个人资料 需要多长时间?
5. Đọc các trang giá của Azure OpenAI và Bedrock. Đối với khối lượng công việc Claude 100M-token / tháng, rẻ hơn  trực tiếp API Anthropic, Bedrock theo yêu cầu, hoặc Bedrock Provisioned Throughput?
   Trung ngữ翻译:阅读Azure OpenAI 和 Bedrock 定价页面──对于100M token/月的Claude 工作负载,哪个更便宜直接人类 API、Bedrock 按量还是Bedrock 提供吞吐量?

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|------------------------|----------|
| Bedrock | "AWS LLM service" | Model marketplace across Claude, Llama, Titan, Mistral, Cohere | AWS 的 LLM 模型集市平台 |
| Azure OpenAI | "Azure's ChatGPT" | Exclusive OpenAI models in Azure datacenters with enterprise controls | Azure 独家托管 OpenAI 模型的企业服务 |
| Vertex AI | "Google's LLM" | Gemini-first platform with Model Garden for third-party models | Google 的 Gemini 优先 AI 平台 |
| PTU | "dedicated capacity" | Provisioned Throughput Unit — reserved inference GPUs, priced per hour | 预置吞吐量单位——独占推理 GPU 容量 |
| Application Inference Profile | "Bedrock tagging" | Per-product cost/usage profile with tags, CloudWatch-native | Bedrock 按产品归因的推理配置文件 |
| Model Garden | "Vertex catalog" | Vertex AI's third-party model section, separate from Gemini | Vertex AI 第三方模型目录 |
| Two-provider minimum | "LLM redundancy" | Policy of running every critical LLM path across ≥2 hyperscalers | 双供应商最低策略——关键 LLM 调用跨 2+ 云商 |
| BAA | "HIPAA paperwork" | Business Associate Agreement; required for PHI; provided by all three | 业务关联协议——HIPAA 合规必需 |
| Abuse monitoring | "the log watcher" | Provider-side safety scan on prompts/outputs; opt-out in enterprise | 平台侧的 prompt/输出安全扫描 |

## Xem thêm 延伸阅读

- [AWS Bedrock Pricing](https://aws.amazon.com/bedrock/pricing/) thẻ giá trị chính đáng và giá cả thông qua được cung cấp.
- [Azure OpenAI Service Pricing](https://azure.microsoft.com/en-us/pricing/details/azure-openai/) Kinh tế và thẻ lãi suất của PTU.
- [Vertex AI Generative AI Pricing](https://cloud.google.com/vertex-ai/generative-ai/pricing) Đứa đôi và Model Garden phụ phí.
- [Artificial Analysis LLM Leaderboard](https://artificialanalysis.ai/) Các điểm chuẩn thời gian trễ và thông qua liên tục trên các nhà cung cấp.
- [The AI Journal — AWS Bedrock vs Azure OpenAI CTO Guide 2026](https://theaijournal.co/2026/03/aws-bedrock-vs-azure-openai/) Quản lý quyết định của doanh nghiệp.
- [Finout — Bedrock vs Vertex vs Azure FinOps](https://www.finout.io/blog/bedrock-vs.-vertex-vs.-azure-cognitive-a-finops-comparison-for-ai-spend) cơ học phân bổ bên cạnh nhau.
