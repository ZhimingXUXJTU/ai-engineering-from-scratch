# 管理的LLM平台 Bedrock,Vertex AI,Azure OpenAI

> 只有三个超级级级别,三个不同的策略. AWS Bedrock是一个模型市场 克劳德,拉马,泰坦,稳定,协同在一个API后面.  Azure OpenAI是一个专属的OpenAI合作伙伴关系,加上为专用容量提供通量单位 (PTU). 果AI是双胞胎第一,拥有最好的长文本和多模式故事. 2026年,人工分析测量Azure OpenAI的中位数为50 ms,Bedrock的Llama 3.1 405B等级为75 ms. 决定的规则不是"哪个是最快的"而是"哪个模型目录和FinOps表面匹配我的产品".

> **【中文解读】**本节介绍了托管 LLM 平台的选择和对比.

>  **【前置】**学本节前请先掌握:第11阶段 (LLM工程) 全部你已经会使用OpenAI/人类API调模型;第13阶段 (工具和协议) 理解MCP等协议――本节讲生产部署选择哪个云不是技术问题,是商业+合规+技术综合决策――

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy cost-and-latency comparator) | **语言:** Python（标准库，成本-延迟比较器）
**Prerequisites:** Phase 11 (LLM Engineering), Phase 13 (Tools & Protocols) | **前置知识:** Phase 11（LLM 工程）, Phase 13（工具与协议）
**Time:** ~60 minutes | **时间:** ~60 分钟

## 学习目标

- 列出三个平台策略 (市场对独家对双子座第一) 并将每个平台与产品使用情况匹配.

>  **【类比】**三大云平台 LLM 服务 = 三种餐厅:(1) **AWS Bedrock**,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,**Azure OpenAI**                                                                                                                                                                                                                                                              **Vertex AI**选择哪个看你的菜谱(使用Cloed 还是GPT 还是Gemini) 和预算──

> ️ **【易错点】**托管平台选型的3个坑:**只看标价**Bedrock 上 Claude 比人类直连贵15-20% (云税),但合规和统一计值钱;做 TCO (总拥有成本) 而不是单价比较――(2) **忽略数据驻留**欧洲用户数据必须留在欧洲,选择Azure EU区域或Bedrock eu-central-1;跨境数据传输违反GDPR──(3) **没做厂商锁定评估**使用OpenAI PTU 后想换Bedrock 要重写SDK 和快速格式;使用LiteLLM等抽象层降低锁定风险──
  中文翻译:说出三种平台策略(集市 vs 独家合作 vs 双子座 优先),并将每个种类匹配到产品用例――
- 解释Azure OpenAI中提供吞吐量单位 (PTU) 如何购买您,以及为什么按需Bedrock通常在405B尺度上读取速度低于25 ms.
  中文翻译:解释Azure OpenAI的预置吞吐量单位 (PTU) 带来了什么,以及为什么Bedrock 按量部署在405B 规模下通常慢约25ms──
- 图表每个平台的FinOps属性表面 (Bedrock应用程序推理资料与 Vertex项目/团队与Azure范围 + PTU预订).
  中文翻译:绘制各平台的FinOps 归因界面(Bedrock应用推理个人资料对 Vertex 项目-每团队对 Azure 作用域 + PTU 预留) 。
- 写下"两供应商最低"政策,并解释为什么单供应商锁定是2026年的昂贵错误.
  中文翻译:写下"双供应商最低"策略,并解释为什么单供应商锁定是2026年昂贵的错误.

## 问题 问题引入

您选择了Claude 3.7 Sonnet为您的产品.现在您需要服务.您可以直接调用Anthropic API,或者通过AWS Bedrock,或者通过网关.直接 API是最简单的;Bedrock添加BAA,VPC终端点,IAM和CloudWatch属性.网关添加了故障转账,统一的发票和跨供应商的利率限制.

> 你选择了Claude 3.7 Sonnet.现在需要部署它.你可以直接调用Anthropic API,也可以通过AWS Bedrock调用,或者通过网关调用.

更多的问题是目录.如果你需要克劳德,拉马和双胞胎在同一产品中,你不能从一个地方购买它们,除非那个地方是Bedrock加上Vertex加上AzureOpenAI同时.

> 更深层次的问题是模型目录. 如果你在同一产品中需要克劳德·拉玛和双胞胎,你不能从一个地方购买所有模型,除非同时使用Bedrock + Vertex + Azure OpenAI.

这一课将三个投注,延迟差距,FinOps差距,

> 本课程绘制了三个注,延迟差距,FinOps差距和锁定风险.

> **【中文解读】**选择LLM 后",在哪里部署"是一个基础设施级别的决策.直接调用API 最简单,但缺乏企业级控制;通过云平台 (Bedrock/Vertex/Azure)调用增加了合规,审计能力;通过网关调用则获得多供应商容量和统计费用.核心矛盾在于:三大云厂商的模型目录不重叠,无法在单一平台上获取所有前沿模型.

> **【拓展：LLM 部署模式】**2024-2026年,LLM服务部署模式从"直接API" →"云平台托管" →"AI网关统一路由"发展.OpenRouter、Portkey、LiteLLM等AI网关项目在2025年获得大量采用,核心价值是为多供应商提供统一接口、自动故障过关和成本优化.企业级部署中,约60%已采用网关模式.

## 概念的核心概念

> **【中文解读】**三大云厂商的LLM平台策略截然不同:AWS Bedrock是"模型集市",聚合多家供应商;Azure OpenAI是"独家合作",专为OpenAI模型;Vertex AI是"双子优先",以超长上下文和多媒体能力为卖点.

> **【拓展：全球 LLM 云平台格局】**除三大超级级外,2026年值得关注的还有:Cloudflare 工人 AI(边缘推理) 、一起 AI(开源模型推理平台,$0.18/M代币为Llama 3.1 70B) 、Groq(LPU 推理引擎,TTFT < 20ms) 、Cerebras(CS-3晶圆尺度推理,2000+代币/s) ──国内有百度千万帆阿里百炼、火山方舟等,但模型目录与国际平台不互通.

### 三种策略

**AWS Bedrock**市场.克劳德 (人类),Llama (Meta),Titan (AWS首方),稳定性 (图像),Cohere (嵌入),Mistral,加上图像和嵌入子目录.一个API,一个IAM表面,一个CloudWatch出口.贝德罗克的投注是客户希望选项更多的比他们想要单个模型.

> **AWS Bedrock** 模型集市──Claude(Anthropic)、Llama(Meta)、Titan(AWS自有)、稳定性(图像)、Cohere(嵌入)、Mistral,以及图像和嵌入子目录──一个API、一个IAM界面、一个CloudWatch 导出──Bedrock的注是客户想要可选择性而不是单一模型──

**Azure OpenAI**独家合作.你得到了GPT-4/4o/5/o系列,DALL·E,Whisper和Azure数据中心的OpenAI模型的细节调整.Azure OpenAI服务目录中没有非OpenAI模型.这些模型进入Azure AI Foundry (单独的产品).Azure的投注是OpenAI仍然是边界,客户希望对该特定关系进行企业控制.

> **Azure OpenAI** 独家合作──你在Azure 数据中心获得了GPT-4/4o/5/o 系列、DALL·E、Whisper 和 OpenAI 模型微调──"Azure OpenAI 服务" 目前没有非 OpenAI 模型在Azure AI  Foundry(独立产品中.

**Vertex AI**双子座第一,其他的一切第二.双子座1.5/2.0/2.5闪电和Pro,加上模型园 (第三方).Vertex的投注是多模式长语境  1M标志双子座背景是区别.

> **Vertex AI**双子座 优先,其他其次. 双子座 1.5/2.0/2.5 Flash 和 Pro,加上Model Garden.

### 缩放时间的差距

人工分析运行持续的基准. 在相当于Llama 3.1 405B部署 (按要求共享) 上,Azure OpenAI的初代币延迟平均约为50ms;Bedrock约为75ms. 缺口不是AWS故障,而是能力模型差异.  Azure 销售PTU (提供通量单位),为租户保留GPU容量. 贝德罗克的相当量 (提供通量) 存在,但每单位的价格从每小时21美元左右开始,大多数客户都在按需共享.

> 人工分析 运行持续基准测试――在等效的Llama 3.1 405B 部署 (共享按量) 上,Azure OpenAI 中位首代币 延迟约50ms;Bedrock 约75ms――差距不是AWS的问题而是容量模型差异――Azure 销售PTU(预置吞吐量单位),为您的租户预留GPU 容量――Bedrock 的等效功能存在但起价约21美元/户小时/按量模式,大多数客户使用共享量模式――

如果您的产品 SLA 在 P99 时 TTFT < 100 ms,则您要么在 Azure 上购买 PTU,要么购买 Bedrock 提供通量,要么接受默认变量.

> 按量共享容量与所有其他客户流量竞争GPU资源――专用容量不会――如果你的产品SLA是P99 TTFT <100ms,你要么在Azure购买PTU,要么购买Bedrock提供吞吐量,要么接受默认差――

> **【中文解读】**延迟差距的本质是"容量模型"差异. 在共享量部署中,您的请求与所有其他客户的流量竞争 GPU 资源;专用容量(PTU)则预留独占的 GPU.Azure PTU在40%60%的利用率上可节省高达70%的成本,但空时仍然付费.Bedrock的量模式 TTFT中位数约75ms,Azure PTU中位数约50ms,25ms差距在高频交互场景中被用户感知.

### 提供吞吐量经济学

 Azure PTU:一个保留的推理计算区块.可预测的工作负载的节省率高达70%对需求. 固定的每小时成本,无论流量如何. 您即使在空中时也支付预订费用. 折扣平衡通常在持续利用率的40%-60%.

> 预留的推理计算块――对于可预测的工作负载,按量模式节省约70%――每小时固定成本,无论流量如何即使空也需要支付费――损失平衡点通常在40%-60%的持续利用率――

床提供过量: $21-$根据模型和地区,每小时50分. 类似的数学  破平率是大约半峰值利用率. 需要每月承诺.

> 床提供输出:每小时 $21-$经济模型的亏损平衡点约占峰值利用率的一半.

根据Gemini SKU,Vertex提供的容量销售;价格因车型和地区而异,并且不公开广告.

> 模预定容量按双子座 SKU 销售;价格因模型和区域而异,公开信息较少.

### 终端表面 真正的区分器

**Bedrock Application Inference Profiles**标签一个个人资料`team`现在`product`现在`feature`通过它将所有模型调用路由;CloudWatch没有后处理,每个配置文件的成本都会破裂.

> **Bedrock Application Inference Profiles**是市场上最清晰的成本归因方案.`team`,我知道.`product`,我知道.`feature`标记配置文件;通过它调用所有模型;CloudWatch 无需后处理即可按配置文件分拆成本──2025年新增,仍然是超大规模云中最精细的原生方案──

**Vertex**您可以将每个团队作为一个GCP项目,将标签放在每个资源上,并使用BigQuery 计费出口+数据研究.更多的工作,但BigQuery 给你任意的SQL在成本数据.

> **Vertex**归因是项目-每组加无处不在标签――你将每个团队建成一个GCP项目,在每个资源上放置标签,使用BigQuery 发票出口+数据研究 进行汇总――工作量更大,但BigQuery 允许你对成本数据执行任意SQL――

**Azure**基于订阅/资源组范围以及标签,PTU预订作为一流成本对象.标签是从资源组继承的,而不是请求,因此每请求属性需要应用洞察的定制度或盖茨标签.

> **Azure**根据订阅/资源组作用域加标,PTU 预留作为一等成本对象.标签从资源组继承而非请求,因此每次请求的归因需要应用程序洞察力自定义标标标或可以打标的网关.

模式:Bedrock是最干净的本地,Vertex是通过BigQuery最灵活的,Azure是最不透明的,除非你是仪器.

> 总结:Bedrock 原生最清晰,Vertex 通过BigQuery 最灵活,Azure 除非自行埋点否则最不透明

> **【中文解读】**贝德罗克的应用推理资料是目前最精细的原产本归因方案按团队,产品,功能标签分调调成本; 通过BigQuery 导出提供最大灵活性,可用SQL做任意聚合;Azure 最为不透明,除非你自行使用应用洞察力埋藏点. 在选择平台时,FinOps 能力和延迟、价格等同重要.

> **【拓展：LLM FinOps 实践】**企业LLM 支出在2025年平均增长300%(Flexera 2025 云状态报告) 常见FinOps 策略包括:(1) 按代币设置团队预算告警;(2) 使用缓存层(语义缓存) 减少重复调用约30-40%;(3) 模型路由简单任务用小模型、复杂任务用大模型,可节省50%+ 成本;(4) 批量API在非实时场景可降低50%的价格.

### 锁定是2026年风险

单个高层级的承诺是很好的,当一个模型占主导地位. 2026年,边界每月移动 克劳德 3.7 一季度,双胞胎 2.5 下一个季度,GPT-5 后一个季度.锁定一个平台锁定你两个三分之一的边界.

> 当一个模型主导时,单云承诺也可以.2026年前沿模型每月都在变化.一个季度是克劳德3.7,下一个季度是双子座2.5,再下一个是GPT-5――锁定一个平台意味着错过三分之二的前沿能力.

模式工作团队采用:任何产品关键的LLM调用时至少有两家提供商.Bedrock加上Azure OpenAI是一个共同的对Claude,另一种GPT,它们之间的故障,相同的门户.成本上升是微不足道的,因为门户路线是最佳的;停机期间可用性上升 (如Azure OpenAI2025年1月事件,AWS us-east-1停机) 是决定性的.

> 高效团队采用模式:任何产品关键 LLM 调用双供应商最低策略.Bedrock + Azure OpenAI是最常见的组合.一个提供Claude,另一个提供GPT,通过同一网关进行故障转移.成本增加可忽略,因为网关路由最优;在机期间可用性升级 (如Azure OpenAI 2025年1月事件,AWS us-east-1 机) 是决定性的.

> **【中文解读】**2026年最大基础设施风险是供应商锁定.前沿模型每季度都在变Q1使用Claude 3.7,Q2使用Gemini 2.5,Q3使用GPT-5.锁定单一平台意味着错过 2/3的前沿能力.最佳实践是"双供应商最低"策略:Bedrock + Azure OpenAI是最常见的组合,通过网关统一路由,成本增加可以忽略,但在故障时显著提高可用性.

> **【拓展：云厂商宕机事件】**2025年1月,Azure OpenAI经历了长达数小时的全局故障,影响了所有依赖单一Azure的ChatGPT 企业客户.同年,AWS us-east-1地区也发生了严重故障.多供应商策略在这些事件中证明了其价值:当一个机时,网关自动将流量转换到另一个机时,实现零感知故障转移.Cloudflare的2025年可用性报告显示,多供应商架构的LLM服务可用性可达99.99%,而单个供应商通常为99.9%.

### 数据居住,BAA和受监管的行业

床:大多数地区的BAA;VPC终端点;防护.常见的金融科技默认.
 Azure OpenAI: HIPAA,SOC 2,ISO 27001;欧盟数据居住权;企业规范的默认.
根据"环保标准"的规定,

> 其他地方: 金融科技 默认选择
> 果: 企业监管默认选择
> 根据区域数据的规定,Google云的合规规则

它们都符合基本的选项框. 差异在于数据保留政策,记录处理方式以及滥用监测是否读取您的流量 (大多数情况下默认选择进入;企业可选择退出).

> 三者都满足基本合规要求. 差异在于数据保留策略,日志处理方式以及滥用监控是否读取您的流量.

### 你应该记住的数字

- 在Llama 3.1 405B等级的Azure OpenAI中介TTF: ~50 ms (含PTU).
  中文翻译:Azure OpenAI 在 Llama 3.1 405B 等效模型上的中位 TTFT:~50ms(使用PTU) 』
- 床床中位数TTFT按要求: ~75 ms.
  中文翻译:床单按量模式中位 TTFT:~75ms。
- 床提供过量: $21-$每个单位50小时.
  中文翻译:床单提供吞吐量:每单位 $21-$五十个小时.
- 光电源平衡率:持续使用率为40-60%.
  中文翻译:蓝色PTU 亏平衡点:~40-60% 持续利用率──
- 储蓄与使用量高的需求:最高70%.
  中文翻译:PTU 在高利用率时相比按量模式节省高达70%──

## 用它实现框架
```figure
i4-platform-lanes
```

## 用它

`code/main.py`通过测试,测试了三种平台的合成工作负载,它模拟了需求对比PTU经济学,TTFT差异和成本归因忠诚度.运行它来看看PTU在哪里收益,以及市场的模型宽度在哪里超过TTFT差距.

> `code/main.py`运行它看看PTU在哪里划算,以及集市的模型广度在哪里超过TTFT差距.

> **【中文解读】**实践部分通过模拟工作负载对三大平台的关键指标包括:TTFT(首代币延迟) 、吞吐量、每百万代币 成本──通过调整利用率参数,可以直观看PTU在什么负载水平下比按量计费更划算──

## 运送它.

这一课产生了`outputs/skill-managed-platform-picker.md`鉴于工作负载配置 (需要的模型,TTFT SLA,每日量,合规要求),它建议一个主要平台,一个倒退和一个FinOps仪器计划.

> 本课产出发 `outputs/skill-managed-platform-picker.md`△给定工作负载配置文件 (※所需模型、TTFT SLA、日调用量、合规要求),它推主平台、备选平台和FinOps 埋点方案──

> **【拓展：生产环境平台选型 Checklist】**生产环境 LLM 平台选型应考虑:(1) 模型目录是否覆盖所需模型;(2) 延迟SLA 是否满足用户体验要求;((对话 < 200ms TTFT,批处理无严格要求);(3) 合规认证(HIPAA/SOC2/ISO27001);(4) 数据驻留(GDPR 要求欧盟 区域存储);(5) 成本归因粒度(能否按团队/产品拆分账单);(6) 容量灾方案(多区域/多应供应商失败) ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓

## 练习题

1. 跑步`code/main.py`根据要求,Azure PTU 能比70B类型的需求更好?
   中文翻译:运行 `code/main.py`青PTU在持续利用率下比70B级模型优于按量模式?计算亏平衡点并与广告的40-60%区间比较.
2. 设计一个两个供应商的部署, 进入哪个超级级级, 哪个门口坐着前面, 什么是故障转移政策?
   中文翻译:你的产品需要Claude 3.7 Sonnet 和 GPT-4o――设计双供应商部署哪到哪个云商,前面放什么网关,故障转移策略是什么?
3. 监管的医疗保健客户需要BAA,美国东部数据居住,以及100ms以下P99TTFT.
   中文翻译:一个受监管的医疗保健客户需要BAA,美国东部数据驻留和P99 TTFT < 100ms.
4. 你发现你的Bedrock账单本月增长了四倍,没有交通变化.没有应用程序推理资料,你怎么会找到罪犯?
   中文翻译:你发现本月Bedrock账单翻了4倍但流量未变──没有应用推理资料 怎么找到原因?有资料 需要多长时间?
5. 阅读Azure OpenAI和Bedrock的价格页面. 对于一个100M代币/月的Claud工作负载,哪个更便宜?
   中文翻译:阅读Azure OpenAI 和 Bedrock 定价页面──对于100M代币/月的Claude 工作负载,哪个更便宜直接的人类API、Bedrock 按量还是Bedrock 提供吞吐量?

## 关键词 快速查找表

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

## 继续阅读 继续阅读

- [AWS Bedrock Pricing](https://aws.amazon.com/bedrock/pricing/)权威率卡和提供通量定价.
- [Azure OpenAI Service Pricing](https://azure.microsoft.com/en-us/pricing/details/azure-openai/) PTU经济学和利率卡
- [Vertex AI Generative AI Pricing](https://cloud.google.com/vertex-ai/generative-ai/pricing)双子座和模型园的附加费用.
- [Artificial Analysis LLM Leaderboard](https://artificialanalysis.ai/)提供商之间持续延迟和吞吐量基准.
- [The AI Journal — AWS Bedrock vs Azure OpenAI CTO Guide 2026](https://theaijournal.co/2026/03/aws-bedrock-vs-azure-openai/)企业决策框架
- [Finout — Bedrock vs Vertex vs Azure FinOps](https://www.finout.io/blog/bedrock-vs.-vertex-vs.-azure-cognitive-a-finops-comparison-for-ai-spend) 配属机制
