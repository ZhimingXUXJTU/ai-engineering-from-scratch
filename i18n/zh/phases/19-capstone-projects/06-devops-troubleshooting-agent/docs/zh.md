# 卡普斯通 06  DevOps 解决问题代理 Kubernetes 关闭障碍排除 Kubernetes 结业 DevOps

> 亚华斯的DevOps代理进入GA,Resolve AI发布了K8s的游戏书籍,NeuBird演示了语义监测,Metro将AI SRE与每服务SLO联系起来. 制作形状已经确定:一个警报网络火,一个代理阅读远程测量,行走K8s对象的图表,排列根源假设, 默认情况下只能读取. 每个被人类关门的补救措施. 这块顶石是那个代理, 通过20起合成事件进行评估,

> **【中文解读】**本节是综合项目构建 DevOps 故障排除代理,自动诊断和修复基础设施问题


**Type:** Capstone | **类型:** 综合项目
**Languages:** Python (agent), TypeScript (Slack integration) | **语言:** Python（Agent）, TypeScript（Slack 集成）
**Prerequisites:** Phase 11 (LLM engineering), Phase 13 (tools and MCP), Phase 14 (agents), Phase 15 (autonomous), Phase 17 (infrastructure), Phase 18 (safety)

>  **【前置】**顶点项目 06 = 综合阶段 11/13/14/15/17/18──K8s DevOps 代理 = AWS DevOps 代理 / 解决AI / NeuBird / Metoro 都在做──
>  **【类比】**通过通过简报,默认只读,所有修复HITL.**前置知识:**项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目项目
**Phases exercised:**现在,我们在这个世界里,**涉及阶段:**子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子
**Time:** 30 hours | **时间:** 30 小时

## 问题 问题引入

> **【中文解读】**本节阐述了 DevOps故障排除代理的核心问题.2025-2026年SRE领域的共识是"AI代理做初步诊断,人类审批修复操作".

> **【拓展：AIOps 产业现状】**2026年AIOps 主要玩家:AWS DevOps 代理(GA 发布) 、解决AI(K8s 故障排除专业) 、NeuBird(语义监控) 、Metoro(SLO-第一 AI SRE) 、PagerDuty AIOps──共同架构是告警网关 触发 → 代理 读取遥测 → 排名根因假设 → Slack 简报 + 审批按──MTTR平均修复时间) 从45-90分钟短到 代理 辅助的 10-15分钟──在安全设计上,所有破坏性操作都需要 Slack 人工审批──

根据"人工智能"的描述,人工智能代理会对事件进行分类,人类会批准修复. 代理阅读普罗梅斯指标,洛基日志,泰波指标,Kube状态指标,以及K8对象的知识图. 它在不到五分钟内产生了与远程测量引用的排列根原因假设. 它从来没有通过Slack得到人类的明确批准.

> 2025-2026年的SRE 叙事变成:"AI代理 分诊事故,人类审批修复――"AWS DevOps代理、解决AI、新鸟、Metoro、付费者Duty AIOps 都在生产环境中提供这种形态――Agent 读取Prometheus 指标、Loki 日志、时间追踪、立方状态测量和K8对象知识图谱――它在五分钟内生成从遥测引用的排序根基因假设――它没有通过Slack 获得明确的人工审批的情况下执行破坏性命令――

经理需要一个默认只读的RBAC表面,一个硬化的MCP工具服务器,以及对每一个被考虑和执行的命令的审计日志.它需要知道它在什么时候超出了它的深度和升级.而且它必须运行足够便宜,OOM杀死场不会产生5k的经理账单.

> 大部分工作的困难在于范围界定和安全,而不是推理. 代理需要默认阅读的RBAC 表面,固定的MCP 工具服务器,以及每个被考虑和执行的命令的审计日志. 它需要知道什么时候超越能力范围和升级.

## 概念的核心概念

> **【中文解读】**代理操作基于K8s 知识图谱:节点是Pod、部署、服务等对象,边编码所有权(Pod→ReplicaSet→部署) 、调度关系(Pod→Node) 和观测关系(Pod→Prometheus 指标) ・告警触发时,代理从受影响对象发发发遍历图谱,拉取相关遥测片(最近15分钟),生成根据证据权重排序的根假设――修复操作认认默只读,破坏性操作需要 Slack 人工审批――

> **【拓展：知识图谱在 SRE 中的应用】**基因假设评分公式:近期 x 具体性 x 图形路径-长度-逆转 x 引用数量――实测数据显示,前三 假设准确率可达80%+(20个合成故障场景),p50 诊断时间 <5分钟――审计日志采用只添加JSONL格式,记录每个被考虑和执行的命令――

经纪人运作在知识图上.节点是K8s对象 (Pod,部署,服务,节点,HPA,PVC) 加上远程测量源 (Prometheus系列,Loki流,Tempo痕迹).边缘编码所有权 (Pod ->ReplicaSet ->部署),规划 (Pod -> Node),观察 (Pod -> Prometheus系列).图表通过 kube-state-metrics同步并在每个警报中重新采样.

> 经理在知识图谱上操作.节点是K8对象. 片. 部署. 服务. 节点. 节点. 电脑. 电脑. 电脑. 电脑. 电脑. 电脑. 电脑. 电脑. 电脑. 电脑. 电脑. 电脑. 电脑. 电脑. 电脑. 电脑.

当警报发射时,该代理从受影响对象中根源.它走边,拉出相关的远程测量切片 (最后15分钟),并草图了一个假设.假设由证据排列:有多少远程测量引用支持它,最近多久,具体多大.前三种假设将与图形路径可视化和修复行动的批准按一起进入 Slack.

> 当警方触发时,代理从受影响物体进行根因分析. 它遍历边,拉取相关遥测片段.

修复是关闭的.允许默认操作是仅读的.破坏性操作 (缩小,滚回,删除Pod) 需要Slack批准;ArgoCD滚回需要代理永远不会持有的 auth代币.审计日志记录了代理 *考虑*  不仅执行的每一个命令,因此审查过程几乎没有错误.

> 修复是受限的.默认允许的操作是只读的.破坏性操作 (缩减,回滚,删除 Pod) 需要 Slack 审批;ArgoCD 回滚需要一个代理 永远没有认证代币.

## 建筑,建筑

```
PagerDuty / Alertmanager webhook
           |
           v
     FastAPI receiver
           |
           v
   LangGraph root-cause agent
           |
           +---- read-only MCP tools ----+
           |                             |
           v                             v
   K8s knowledge graph              telemetry slices
     (Neo4j / kuzu)              Prometheus, Loki, Tempo
   ownership + scheduling          last 15m, scoped
           |
           v
   hypothesis ranking (evidence weight)
           |
           v
   Slack brief + approval buttons
           |
           v (approved)
   ArgoCD rollback hook / PagerDuty escalate
           |
           v
   audit log: considered vs executed, every command
```

##  技术

- 观察性来源:普罗梅泰斯,洛基,特马波,库贝状态测量
  中文翻译:可观察性来源:普罗梅泰斯,洛基,特马波,be-state-metrics
- 知识图:K8s对象的Neo4j (管理) 或 kuzu (嵌入式) +远程测量边缘
  中文翻译:知识图:K8s对象的Neo4j (管理) 或 kuzu (嵌入) +远程测量边缘
- 机器人:每工具允许列表的LangGraph,默认只能读取
  中文翻译:代理:每工具允许列表的LangGraph,默认只读取
- 工具运输:FastMCP 通过 StreamableHTTP; 通过通过门后的破坏性工具的单独服务器
  中文翻译:工具运输:快MCP 通过 StreamableHTTP; 通过门后的破坏性工具的单独服务器
- 模型:Claude Sonnet 4.7用于根源推理,双胞胎 2.5 闪存用于日志总结
  中文翻译:模型:克劳德·索内特4.7用于根源推理,双子座2.5 闪存用于日志总结
- 补救:ArgoCD滚动网关,PagerDuty升级,Slack批准卡
  中文翻译:修复:ArgoCD滚动网关,PagerDuty升级,Slack批准卡
- 审计:仅附录结构日志 (审议,执行,批准,结果)
  中文翻译:审计:仅附录结构日志 (考虑,执行,批准,结果)
- 部署:K8部署,具有自己的狭窄的RBAC角色;单独的名称空间
  中文翻译:部署:K8s部署具有自己的狭窄RBAC角色;单独的名称空间

## 动手构建

> **【中文解读】**构建9个阶段:图数据库摄入,告警接收器,只读工具面,根因代理,证据评分,Slack简报,修复门控,审计日志和合成故障场景集.

> **【拓展：合成故障场景在 SRE 训练中的价值】**本课的20个合成故障场景(OOMKill 级联、DNS 动、HPA 震荡、PVC 填满、邻居等) 是SRE代理的"单元测试"――Google的SRE书籍强调"游戏日"练习的重要性在受控环境中模拟故障以验证响应流程――本课的合成场景集是自动化的游戏日,使使代理的诊断能力可量化评估――
```figure
ce-rootcause-walk
```

## 建立它

1. **Graph ingestion.**每30年将ube-state-metrics同步到Neo4j/kuzu.节点:Pod,部署,节点,服务,PVC,HPA.边缘:OWNED_BY,SCHEDULED_ON,EXPOSES,MOUNTS,SCALE.电测量覆盖边缘:OBSERVED_BY (一个Pod由Prometheus系列观察).
   中文翻译:1. **Graph ingestion.**每30年将ube-state-metrics同步到Neo4j/kuzu.节点:Pod,部署,节点,服务,PVC,HPA.边缘:OWNED_BY,SCHEDULED_ON,EXPOSES,MOUNTS,SCALE.电测量覆盖边缘:OBSERVED_BY (一个Pod由Prometheus系列观察).

2. **Alert receiver.**快API终端接收PagerDuty或Alertmanager网络链接. 提取受影响的对象 (s) 和SLO违规.
   翻译: 翻译:**Alert receiver.**快API终端接收PagerDuty或Alertmanager网络链接. 提取受影响的对象 (s) 和SLO违规.

3. **Read-only tool surface.**包裹 kubectl,Prometheus查询,Loki logql,Tempo traceql通过FastMCP.每个工具都有一个狭窄的RBAC动词 ("获取","列表","描述").默认服务器中没有"删除","exec","规模".
   翻译: 翻译:**Read-only tool surface.**包裹 kubectl,Prometheus查询,Loki logql,Tempo traceql通过FastMCP.每个工具都有一个狭窄的RBAC动词 ("获取","列表","描述").默认服务器中没有"删除","exec","规模".

4. **Root-cause agent.**具有三个节点的兰格格拉夫: `sample`拉出了最后15分钟的遥测器片段,`walk`查询邻近物体的图表,`hypothesize`根据远程测量引用,
   翻译: 翻译:**Root-cause agent.**具有三个节点的兰格格拉夫: `sample`拉出了最后15分钟的遥测器片段,`walk`查询邻近物体的图表,`hypothesize`根据远程测量引用,

5. **Evidence scoring.**每个假设都有分数 = 近期 * 具体性 * 图形路径长度反转 * 引用数.返回前-3.
   翻译: 五.**Evidence scoring.**每个假设都有分数 = 近期 * 具体性 * 图形路径长度反转 * 引用数.返回前-3.

6. **Slack brief.**附加一个附加值,包含假设,图形路径可视化 (一个服务器侧的子图像),以及最多一个修复行动的批准按.
   翻译: 七个字**Slack brief.**附加一个附加值,包含假设,图形路径可视化 (一个服务器侧的子图像),以及最多一个修复行动的批准按.

7. **Remediation gate.**破坏性工具 (缩小,倒滚,删除) 在批准代币后的第二个MCP服务器上存活.经纪人只能在Slack卡被人批准后调用它们.
   翻译:7.**Remediation gate.**破坏性工具 (缩小,倒滚,删除) 在批准代币后的第二个MCP服务器上存活.经纪人只能在Slack卡被人批准后调用它们.

8. **Audit log.**仅添加JSONL:每一个候选命令,记录是否被考虑,是否执行,谁批准它. 每天运送到S3.
   翻译:8.**Audit log.**仅添加JSONL:每一个候选命令,记录是否被考虑,是否执行,谁批准它. 每天运送到S3.

9. **Synthetic incident suite.**构建20种场景:OOMKill,DNS,HPA,PVC填充,杂的邻居,故障的侧车,ConfigMap部署不佳,证书旋转,图像拉回,等.
   翻译:9.**Synthetic incident suite.**构建20种场景:OOMKill,DNS,HPA,PVC填充,杂的邻居,故障的侧车,ConfigMap部署不佳,证书旋转,图像拉回,等.

## 用它使用方法

```
webhook: alert.pagerduty.com -> checkout-api SLO breach, error rate 14%
[graph]   affected: Deployment checkout-api (3 Pods, Node ip-10-2-3-4)
[walk]    neighbors: ReplicaSet checkout-api-abc, Service checkout-api,
          recent rollout 14m ago
[sample]  prometheus error_rate 14%, up-trend; loki 500s on /api/v2/pay
[hypo]    #1 bad rollout: latest image checkout-api:v2.41 fails /healthz
          citations: deploy.yaml (rev 42), prometheus errorRate, loki 500 stack
[slack]   [ROLL BACK to v2.40]  [ESCALATE]  [IGNORE]
          (approval required; agent does not roll back unilaterally)
```

## 发射上线

> **【中文解读】**交付物是一个完整的 DevOps 故障排除代理,评估维度包括:RCA 准确率(20个合成场景 >= 80%) 安全性(破坏性操作必须有 Slack 审批) 诊断速度(p50 < 5 分钟) 可解释性(每个假设有图路径和遥测引用) 和集成完整性。

`outputs/skill-devops-agent.md`由于K8s集群和警报来源, 代理产生排列的根原因假设和一个Slack-gated补救流.

> `outputs/skill-devops-agent.md`是交付物质. 给定K8s集群和告警源,代理生成排序的根因假设和Slack受控修复流程.

| Weight | Criterion | How it is measured |
| 权重 | 标准 | 如何衡量 |
|:-:|---|---|
| 25 | RCA accuracy on scenario suite | ≥80% correct root cause across 20 synthetic incidents |
| 25 | 场景套件上的 RCA 准确率 | 20 个合成事故中 ≥80% 正确根因 |
| 20 | Safety | Destructive-action guard never fires without Slack approval in the audit log |
| 20 | 安全性 | 破坏性操作守卫从未在审计日志中缺少 Slack 审批就触发 |
| 20 | Time-to-hypothesis | p50 under 5 minutes from alert to Slack brief |
| 20 | 假设时间 | 从告警到 Slack 简报的 p50 低于 5 分钟 |
| 20 | Explainability | Every hypothesis has graph paths and telemetry citations |
| 20 | 可解释性 | 每个假设有图路径和遥测引用 |
| 15 | Integration completeness | PagerDuty, Slack, ArgoCD, Prometheus end-to-end working |
| 15 | 集成完整性 | PagerDuty、Slack、ArgoCD、Prometheus 端到端工作 |
| **100** | | |

## 练习题

1. 运行你的代理在同一三个事件上 AWS 的 DevOps 代理被演示了. 发布一边一边. 报告代理在哪里分歧.
   中文翻译:在同一三个事故中运行你的代理,与AWS DevOps代理的演示对比.发布并排行比较.报告代理 分歧之处.

> 中文翻译:在同一三个事故上运行你的代理,与AWS DevOps代理的演示对比.发布并排比.


2. 添加一个"接近错失"审计,标记出代理认为没有批准的任何命令是破坏性的.
   中文翻译:添加"差点"审计,标记 代理 *考虑*但没有批准就会是破坏性的任何命令――测量一周内差点率――

3. 换个假设模型从克劳德·索内特4.7到一个自主托管的Llama 3.3 70B.
   中文翻译:将假设模型从克劳德·索内特4.7 换为自托管的拉马 3.3 70B──测量RCA准确率差异和每事故美元成本──

> 中文翻译:将假设模型从克劳德·索内特 4.7 换为自托管的拉马 3.3 70B──测量RCA 准确率差异和每事故美元成本──(翻译)


4. 建立一个因果过器:区分相关的远程测量峰值与真正的根源. 训练一个小的分类器在20场景标签上.
   中文翻译:构建因果过器:区分相关的遥测尖峰和真正的根因.

5. 加入反弹干跑:ArgoCD反弹对一个具有相同的表格的阶段集群.在 Slack 批准按之前,在现场集群中验证反弹计划.
   中文翻译:添加回滚干跑:用相同的清单对舞台集群进行ArgoCD 回滚――在 Slack 审批按前验证活集群中的回滚计划――

> 中文翻译:添加回滚干跑:用相同清单对舞台集群进行ArgoCD 回滚――在 Slack 审批按前验证活集群中的回滚计划――(翻译)


## 关键词 快速查找表

| Term | What people say | What it actually means |
| 术语 | 通俗说法 | 实际含义 |
|------|-----------------|------------------------|
| K8s knowledge graph | "Cluster graph" | Nodes = K8s objects + telemetry series; edges = ownership, scheduling, observation |
| K8s 知识图谱 | "集群图" | 节点 = K8s 对象 + 遥测序列；边 = 所有权、调度、观测 |
| Read-only-by-default | "Scoped RBAC" | Agent's service account has only get/list/describe verbs; destructive verbs live in a separate server behind approval |
| 默认只读 | "限定 RBAC" | Agent 的服务账号只有 get/list/describe 动词；破坏性动词在审批后的独立服务器中 |
| Audit log | "Considered vs executed" | Append-only record of every candidate command, whether it ran, who approved |
| 审计日志 | "考虑 vs 执行" | 每个候选命令的只追加记录，是否运行，谁审批 |
| Hypothesis ranking | "Evidence score" | Recency × specificity × graph-path length inverse × citation count |
| 假设排序 | "证据分数" | 近因 × 特异性 × 图路径长度倒数 × 引用数 |
| Slack approval card | "HITL gate" | Interactive Slack message with remediation buttons; agent cannot proceed until a human clicks |
| Slack 审批卡片 | "人机交互门" | 带修复按钮的交互式 Slack 消息；Agent 直到人类点击才能继续 |
| Telemetry citation | "Evidence pointer" | A Prometheus query, Loki selector, or Tempo trace URL that supports a claim |
| 遥测引用 | "证据指针" | 支持声明的 Prometheus 查询、Loki 选择器或 Tempo 追踪 URL |
| MTTR | "Time to resolution" | Wall-clock from alert fire to SLO recovery |
| MTTR | "解决时间" | 从告警触发到 SLO 恢复的挂钟时间 |

## 继续阅读 继续阅读

- [AWS DevOps Agent GA](https://aws.amazon.com/blogs/aws/aws-devops-agent-helps-you-accelerate-incident-response-and-improve-system-reliability-preview/)2026年法典引用
  中文翻译:2026年规范的参考
- [Resolve AI K8s troubleshooting](https://resolve.ai/blog/kubernetes-troubleshooting-in-resolve-ai)竞争对手的参考
  中文翻译:竞争对手参考
- [NeuBird semantic monitoring](https://www.neubird.ai)语义图方法
  中文翻译:语义图方法
- [Metoro AI SRE](https://metoro.io) SLO-第一生产框架
  中文翻译:SLO 优先的生产框架
- [kube-state-metrics](https://github.com/kubernetes/kube-state-metrics)集群状态来源
  中文翻译:集群状态源
- [LangGraph](https://langchain-ai.github.io/langgraph/) 参考代理主管
  中文翻译:参考 编排器
- [FastMCP](https://github.com/jlowin/fastmcp) Python MCP服务器框架
  中文翻译:Python MCP 服务器框架
- [ArgoCD rollback](https://argo-cd.readthedocs.io/en/stable/user-guide/commands/argocd_app_rollback/)关闭的补救目标
  中文翻译:受限修复目标
