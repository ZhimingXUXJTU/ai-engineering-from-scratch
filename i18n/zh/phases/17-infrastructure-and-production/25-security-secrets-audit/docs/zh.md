# 安全 秘密,API关键旋转,审计日志,护卫轨 安全 密钥 审计

> 通过集中式库存 (HashiCorp Vault, AWS 秘密管理器,Azure 密钥库) 消除秘密扩散. 永远不要存储凭据在配置文件, 使用IAM角色而不是静态键;用于CI/CD的OIDC. AI-gateway模式是2026年解决方案:应用程序 → gateway →模型提供商, 换机,没有 Slack"谁有新钥匙"的消息. 转换政策 ≤90天;每次提交时使用TruffleHog/GitGuardian/Gitleaks扫描. 零信任:MFA,SSO,RBAC/ABAC,短寿命的代币,设备姿势.  PII 清理使用实体识别来掩盖 PHI/PII 在转发之前;一致的代码化 (Mesh 方法) 将对稳定的位持有人的敏感值映射,因此 LLM 保持代码/关系语义. 网络退出:仅在专用VPC/VNet子网上提供LLM服务`api.openai.com`现在`api.anthropic.com`通过被破坏的CI/CD凭证攻击, 通过数千个客户部署, 泄露了环境.

> **【中文解读】**本节介绍了安全密钥审计 LLM 服务中的密钥管理和安全审计.


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy PII-scrubber + audit-log writer) | **语言:** Python
**Prerequisites:** Phase 17 · 19 (AI Gateways), Phase 17 · 13 (Observability) | **前置知识:** Phase 17 · 19 (AI Gateways), Phase 17 · 13 (Observability)

>  **【前置】**学本节前请先掌握:阶段17·19(AI门户) ‧阶段17·13(可观测性) ‧零信任架构基础──安全核心:消除密钥散落+集中化保管──
>  **【类比】**简称: 网关 模式 模式 应用 网关 模型商,网关运行时从 库取密钥 轮换 ≤90 天,所有应用自动跟上,无需重新部署.
> ️ **【易错点】**据报道,该公司已在3月9日发布了"中国"的信息.
**Time:** ~60 minutes | **时间:** ~60 minutes

## 学习目标

- 列出四种秘密管理反模式 (VCS中的配置文件,硬码的 env,电子表格,静态密钥) 并命名它们的替代.
  中文翻译:列举四个密钥管理反模式(VCS 中配置文件、硬编码环境变量、电子表格共享密钥、共享服务账户) 』
- 解释AI-gateway-pulls-from-vault模式作为2026年生产标准.
  中文翻译:解释AI 网关从 Vault 拉取密钥的模式作为2026年生产标准.
- 实现一个具有一致的代码化 (相同值 →相同的位置持有者) 的 PII 清洗器,以便语义存活下来.
  中文翻译:实现带一致性标记化的 PII 清洗器(同值 -> 相同占位符) 』
- 举个2026年维尔塞尔供应链事件,以及它所教导的关于CI/CD认证卫生情况.
  中文翻译:说出2026年  Vercel 供应链事件以及对CI/CD 凭证卫生的教训.

## 问题 问题引入

> **【中文解读】**证书管理 实习生提交 `.env`包含API密钥,已在 git 历史中,轮换流程是"Slack 群发,更新40个配置文件,重新部署所有服务8小时后只有一半服务上线";[2] PII 泄露用户提示包含"我的SSN是123-45-6789",直接发送到OpenAI,虽然有BAA但内部政策要求发送前脱敏;[3]网络出口EKS集群的LLM Pod可以访问任何互联网主机,有人通过DNS查询攻击者控制的域名外泄漏数据.

> **【拓展：2026 年 LLM 安全事件】**2026年典型的LLM安全事件包括: 1) 变化了数千个客户部署的环境变化; 2) 提示进入攻击通过用户输入操纵LLM 执行意想不到的操作; 3) 数据泄露LLM 在响应中泄露训练数据中的敏感信息.

实习生承诺`.env`关键已经在 git 历史中 GitGuardian 扫描捕获它,你的旋转过程是"缓慢团队,更新40个配置文件,重新部署所有服务". 8 小时后,你的服务的半数已经开启,而另一半正在等待部署窗户.

单独,用户提示包括"我的SSN是123-45-6789."提示是向OpenAI.你有BAA,但你的内部政策是在转发之前掩盖个人信息.你没有.

另外,你的EKS集群的LLM组件可以到达任何互联网主机.有人通过DNS搜索将数据输入攻击者控制的域名.

法律法师服务的安全必须解决三个向量:安全库支持的凭证,个人信息清除,网络输出过,审计日志.

## 概念的核心概念

### 集中式保险柜+IAM角色拉

> **【拓展：AI 网关密钥管理模式】**2026年 服务的密钥管理最佳实践AI 网关模式:应用→网关→模型提供商,网关在请求时从 Vault 拉取 `OPENAI_API_KEY`△ 在库中轮换密钥后,下一次自动请求获得新密钥无需重新部署"",无需 Slack"谁有新密钥"消息──支持的库包括:哈希公司库,AWS秘密管理员、Azure密钥库,GCP秘密管理员──配合IAM角色认证(通过IAM身份而非静态密钥认证应用),轮换策略 <= 90 天,可消除密钥散布问题──

**Vault**鱼公司的秘密管理器,Azure Key Vault,GCP秘密管理器.

**IAM role**:app/gateway通过其IAM身份进行认证,而不是静态密钥.Vault返回代币的终身秘密.

**The AI-gateway pattern**门口拉动`OPENAI_API_KEY`随着请求的时间,从库存中转换,下一个请求得到了新的钥匙.

### 转换政策 ≤90天

所有API密钥,库存根代币,CI/CD凭证,自动旋转,如果可能,手动旋转记录和追踪.

### 秘密扫描

- **TruffleHog**                     
- **GitGuardian**商业,高精度.
- **Gitleaks**OSS,运行在CI.

击每一个承诺,如果发现新的秘密.

### 零可靠的姿势

- 对于所有账户,必须进行外汇.
- 通过SAML/OIDC进行SSO.
- 基于角色的RBAC或基于属性的ABAC,用于细粒度的访问.
- 短暂的代币 (小时,不是几天).
- 设备姿势  只有具有磁盘加密的体内设备.

### 清洗PII/PHI

> **【中文解读】**脱敏的四步流程:(1) 实体识别(太空NER、Presidio、商业工具);(2) 掩码匹配的实体"我的SSN是123-45-6789" → "我的SSN是[SSN_TOKEN_A3F]";(3) 一致性标记化(Mesh 方法) 相同值映射到相同占位符,LLM 可以保持关系语义;(4) 可选的LLM 响应逆映射;;静态正则过器捕获基本模式,NER 捕获更多两者都使用.

在提示离开你的内射之前:

1. 实体认可 (空间NER,Presidio,商业).
2. 面具匹配的实体: `"My SSN is 123-45-6789"`其他`"My SSN is [SSN_TOKEN_A3F]"`现在,我们要去.
3. 连贯的标记化 (Mesh方法):将相同的值映射到同一位持有者,因此LLM保持关系.
4. 选择性反向映射,用于LLM响应.

静态regex过器捕获基本模式,NER捕获更多.使用两者.

### 输入+输出防护

输入:阻止已知 jailbreaks,禁止主题;每用户的利率限制.

输出:泄露的秘密 (API密钥模式,拒绝文本中的电子邮件模式),政策违规的分类器.

### 网络出口白名单

> **【拓展：LLM 安全纵深防御】**服务的全身防御策略包括: 1) 集中式 Vault + IAM 角色拉取应用/网关通过 IAM 身份认证, Vault 返回有限期令牌,轮换在 Vault 中完成,所有应用自动获得新密钥; 2) AI 网关模式应用→网关→提供商,网关从 Vault 拉取凭证,无需重新部署; 3) 90 天轮换策略所有 API 密钥,密钥根代币、CI/CD 凭证; 4) 每年提交扫描 TruffleHog / GitGuardian / Gitleaks 在 CI 中阻止新密钥的 PR; 5) 不变的审核日志 每次使用 LLM 调用户户时间应应应应应应/租、哈希模型版本、SO ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ 

在专门的子网中提供LLM服务:
- 清单:`api.openai.com`现在`api.anthropic.com`导向DB终点,保险终点.
- 其他一切:放下.
- 通过只允许列表的解决器 (避免 DNS 道输出).

### 审计日志

每次LLM电话的不可变记录:
- 时间标签.
- 用户/租户
- 快速哈希 (不是原始的隐私提示).
- 模型+版本.
- 标志数量.
- 价格.
- 响应哈希.
- 任何护旅行.

根据监管要求保留 (SOC2 1年,HIPAA 6年).

### 2026年,弗塞尔事件

供应链攻击:受损的CI/CD凭证在数千个客户部署中被泄露. 课程:CI/CD凭证是产品等等价. 存储在保险箱中. 范围狭窄. 激进旋转.

### 你应该记住的数字

- 转换政策: ≤90天
- 查看每一个提交:TruffleHog / GitGuardian / Gitleaks.
- 据报道, 据报道, 据报道, 据报道,
- 审计日志保存:SOC2 = 1年,HIPAA = 6年.

## 用它实现框架
```figure
i4-vault-rotation
```

## 用它

`code/main.py`实现具有一致的标记化和仅附录的审计日志的玩具 PII清洗器.

> `code/main.py`实现具有一致的标记化和仅附录的审计日志的玩具 PII清洗器.

> `code/main.py`实现具有一致的标记化和仅附录的审计日志的玩具 PII清洗器.

## 运送它.

这一课产生了`outputs/skill-llm-security-plan.md`鉴于监管范围和当前状态, 计划库迁移,清洗,出口,审计日志.

> 本课产出发 `outputs/skill-llm-security-plan.md`鉴于监管范围和当前状态, 计划库迁移,清洗,出口,审计日志.

## 练习题

1. 跑步`code/main.py`发送两个引用相同的SSN的提示,确认两者都得到了相同的位置.
   中文翻译:运行 `code/main.py`△发送两个引用相同的SSN提示──确认两者获得相同的占位符──
2. 设计一个vLLM-on-EKS部署的网络退出政策,称为OpenAI + Anthropic + Weaviate.
   中文翻译:为调用OpenAI和人类的vLLM-on-EKS部署设计网络出口策略.
3. 您在 git 历史中发现一个关键 (2岁) 什么是正确的答案?
   中文翻译:你在 Git 历史中发现了一个密钥(2年前) ――正确的响应流程是什么?
4. 设计保留层次 (热30天,热12个月,冷6个月).
   中文翻译:你的审计日志每天增长10GB──设计保留层级(热 30 天、温 12 月、冷 6 年)──
5. 辩论反向标记 (将实际值替换为LLM响应) 是否值得复杂性与保持位持有人可见性.

## 关键词 快速查找表

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Vault | "secrets store" | Centralized credential management service |
| IAM role | "identity-based auth" | Role assumed by app; returns short-lived creds |
| OIDC for CI/CD | "cloud-issued tokens" | No static keys in CI — identity via OIDC |
| TruffleHog / GitGuardian / Gitleaks | "secret scanners" | Commit-time secret detection |
| RBAC / ABAC | "access control" | Role-based vs attribute-based |
| PII scrubbing | "data masking" | Remove or tokenize sensitive entities |
| Consistent tokenization | "stable placeholders" | Same value → same token each time |
| Mesh approach | "Mesh tokenization" | Semantic-preserving tokenization pattern |
| Egress whitelist | "outbound allowlist" | Only permitted domains reachable |
| Audit log | "immutable history" | Append-only record for compliance |

## 继续阅读 继续阅读

- [Doppler — Advanced LLM Security](https://www.doppler.com/blog/advanced-llm-security)
- [Portkey — Manage LLM API keys with secret references](https://portkey.ai/blog/secret-references-ai-api-key-management/)
- [Datadog — LLM Guardrails Best Practices](https://www.datadoghq.com/blog/llm-guardrails-best-practices/)
- [JumpServer — Secrets Management Best Practices 2026](https://www.jumpserver.com/blog/secret-management-best-practices-2026)
- [Microsoft Presidio](https://github.com/microsoft/presidio) 检测和匿名化个人信息.
- [HashiCorp Vault docs](https://developer.hashicorp.com/vault/docs)
