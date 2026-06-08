# Security — Secrets, API Key Rotation, Audit Logs, Guardrails | 安全 密钥 审计

> Eliminate secret sprawl via centralized vaults (HashiCorp Vault, AWS Secrets Manager, Azure Key Vault). Never store credentials in config files, env files in VCS, spreadsheets. Use IAM roles over static keys; OIDC for CI/CD. The AI-gateway pattern is the 2026 solution: apps → gateway → model provider, with gateway pulling credentials from vault at runtime. Rotate in vault and all apps pick up in minutes — no redeploys, no Slack "who has the new key" messages. Rotation policy ≤90 days; scan with TruffleHog / GitGuardian / Gitleaks on every commit. Zero-trust: MFA, SSO, RBAC/ABAC, short-lived tokens, device posture. PII scrubbing uses entity recognition to mask PHI/PII before forwarding; consistent tokenization (Mesh approach) maps sensitive values to stable placeholders so the LLM preserves code/relationship semantics. Network egress: LLM services in dedicated VPC/VNet subnet whitelisting only `api.openai.com`, `api.anthropic.com` etc; block all other outbound. The 2026 incident driver: Vercel supply-chain attack via compromised CI/CD credentials exfiltrated env vars across thousands of customer deployments.

> **【中文解读】** 本节介绍了安全密钥审计——LLM 服务中的密钥管理和安全审计。


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy PII-scrubber + audit-log writer) | **语言:** Python
**Prerequisites:** Phase 17 · 19 (AI Gateways), Phase 17 · 13 (Observability) | **前置知识:** Phase 17 · 19 (AI Gateways), Phase 17 · 13 (Observability)
**Time:** ~60 minutes | **时间:** ~60 minutes

## Learning Objectives | 学习目标

- Enumerate the four secret-management anti-patterns (config files in VCS, hardcoded env, spreadsheets, static keys) and name their replacements.
  中文翻译：列举四个密钥管理反模式（VCS 中的配置文件、硬编码环境变量、电子表格共享密钥、共享服务账户）。
- Explain the AI-gateway-pulls-from-vault pattern as 2026 production standard.
  中文翻译：解释 AI 网关从 Vault 拉取密钥的模式作为 2026 年生产标准。
- Implement a PII scrubber with consistent tokenization (same value → same placeholder) so semantics survive.
  中文翻译：实现带一致性标记化的 PII 清洗器（相同值 -> 相同占位符）。
- Name the 2026 Vercel supply-chain incident and what it taught about CI/CD credential hygiene.
  中文翻译：说出 2026 年 Vercel 供应链事件以及它对 CI/CD 凭证卫生的教训。

## The Problem | 问题引入

> **【中文解读】** LLM 服务的安全需要解决三个向量：(1) 凭证管理——实习生提交 `.env` 含 API keys，已在 git 历史中，轮换流程是"Slack 群发，更新 40 个配置文件，重新部署所有服务——8 小时后只有一半服务上线"；(2) PII 泄露——用户提示包含"My SSN is 123-45-6789"，直接发送到 OpenAI，虽然有 BAA 但内部政策要求发送前脱敏；(3) 网络出口——EKS 集群的 LLM Pod 可以访问任何互联网主机，有人通过 DNS 查询到攻击者控制的域名外泄数据。

> **【拓展：2026 年 LLM 安全事件】** 2026 年的典型 LLM 安全事件包括：(1) Vercel 供应链攻击——受损的 CI/CD 凭证外泄了数千个客户部署的环境变量；(2) 提示注入攻击——通过用户输入操纵 LLM 执行非预期操作；(3) 数据泄露——LLM 在响应中泄露训练数据中的敏感信息。防御措施包括：集中式 Vault（HashiCorp Vault、AWS Secrets Manager）、PII 脱敏（spaCy NER + Presidio）、网络出口白名单、不可变审计日志。

An intern commits `.env` with API keys. They delete it quickly. The keys are already in git history — GitGuardian scan catches it, your rotation process is "Slack the team, update 40 config files, redeploy all services." 8 hours later, half your services are live and half are waiting for deploy windows.

Separately, user prompts include "My SSN is 123-45-6789." Prompt goes to OpenAI. You have a BAA but your internal policy is to mask PII before forwarding. You didn't.

Separately, your EKS cluster's LLM pod can reach any internet host. Someone exfils data via DNS lookup to an attacker-controlled domain. Nothing blocked it.

Security for LLM services has to address all three vectors. Vault-backed credentials. PII scrubbing. Network egress filtering. Audit logs.

## The Concept | 核心概念

### Centralized vault + IAM-role pull

> **【拓展：AI 网关密钥管理模式】** 2026 年 LLM 服务的密钥管理最佳实践——AI 网关模式：应用→网关→模型提供商，网关在请求时从 Vault 拉取 `OPENAI_API_KEY`。在 Vault 中轮换密钥后，下一次请求自动获得新密钥——无需重新部署、无需 Slack"谁有新密钥"消息。支持的 Vault 包括：HashiCorp Vault、AWS Secrets Manager、Azure Key Vault、GCP Secret Manager。配合 IAM 角色认证（应用通过 IAM 身份而非静态密钥认证），轮换策略 <= 90 天，可消除密钥散布问题。

**Vault**: HashiCorp Vault, AWS Secrets Manager, Azure Key Vault, GCP Secret Manager. One source of truth.

**IAM role**: app/gateway authenticates via its IAM identity, not a static key. Vault returns the secret for the lifetime of the token.

**The AI-gateway pattern**: gateway pulls `OPENAI_API_KEY` from vault at request time. Rotate in vault; next request gets the new key. No redeploys.

### Rotation policy ≤ 90 days

All API keys, vault root tokens, CI/CD credentials. Automated rotation where possible. Manual rotation logged and tracked.

### Secret scanning

- **TruffleHog** — regex + entropy on commits.
- **GitGuardian** — commercial, high accuracy.
- **Gitleaks** — OSS, runs in CI.

Run on every commit. Block PR if new secret detected.

### Zero-trust posture

- MFA required on all accounts.
- SSO via SAML/OIDC.
- RBAC (role-based) or ABAC (attribute-based) for fine grained access.
- Short-lived tokens (hours, not days).
- Device posture — only corp devices with disk encryption.

### PII / PHI scrubbing

> **【中文解读】** PII/PHI 脱敏的四步流程：(1) 实体识别（spaCy NER、Presidio、商业工具）；(2) 掩码匹配的实体——"My SSN is 123-45-6789" → "My SSN is [SSN_TOKEN_A3F]"；(3) 一致性标记化（Mesh 方法）——相同值映射到相同占位符，LLM 可以保持关系语义；(4) 可选的 LLM 响应逆映射。静态正则过滤器捕获基本模式，NER 捕获更多——两者都使用。

Before the prompt leaves your infra:

1. Entity recognition (spaCy NER, Presidio, commercial).
2. Mask matched entities: `"My SSN is 123-45-6789"` → `"My SSN is [SSN_TOKEN_A3F]"`.
3. Consistent tokenization (Mesh approach): same value maps to the same placeholder so the LLM preserves relationships.
4. Optional reverse mapping for LLM response.

Static regex filters catch basic patterns; NER catches more. Use both.

### Input + output guardrails

Input: block known jailbreaks, forbidden topics; rate-limit per-user.

Output: regex scrub for leaked secrets (API key patterns, email patterns in refusal contexts), classifier for policy violations.

### Network egress whitelist

> **【拓展：LLM 安全纵深防御】** LLM 服务的纵深防御策略包括：(1) 集中式 Vault + IAM 角色拉取——应用/网关通过 IAM 身份认证，Vault 返回有限期令牌，轮换在 Vault 中完成，所有应用自动获得新密钥；(2) AI 网关模式——应用→网关→提供商，网关从 Vault 拉取凭证，无需重新部署；(3) 90 天轮换策略——所有 API key、vault root token、CI/CD 凭证；(4) 每次提交扫描——TruffleHog / GitGuardian / Gitleaks 在 CI 中阻止含新密钥的 PR；(5) 不可变审计日志——每次 LLM 调用的时间戳、用户/租户、提示哈希、模型+版本、token 数、成本、响应哈希、guardrail 触发。SOC 2 保留 1 年，HIPAA 保留 6 年。

LLM services in a dedicated subnet:
- Whitelist: `api.openai.com`, `api.anthropic.com`, vector DB endpoints, vault endpoints.
- Everything else: drop.
- DNS via allowlist-only resolver (avoid DNS-tunneling exfil).

### Audit log

Immutable log of every LLM call with:
- Timestamp.
- User / tenant.
- Prompt hash (not raw prompt for privacy).
- Model + version.
- Token counts.
- Cost.
- Response hash.
- Any guardrail trips.

Retain per regulatory requirement (SOC 2 1 year, HIPAA 6 years).

### The 2026 Vercel incident

Supply-chain attack: compromised CI/CD credentials exfiltrated env vars across thousands of customer deployments. Lesson: CI/CD credentials are prod-equivalent. Store in vault. Scope narrowly. Rotate aggressively.

### Numbers you should remember

- Rotation policy: ≤ 90 days.
- Scan on every commit: TruffleHog / GitGuardian / Gitleaks.
- Vercel 2026: CI/CD creds compromised → thousands of customer env vars leaked.
- Audit log retention: SOC 2 = 1 year, HIPAA = 6 years.

## Use It | 用框架实现

`code/main.py` implements a toy PII scrubber with consistent tokenization and an append-only audit log.

> `code/main.py` implements a toy PII scrubber with consistent tokenization and an append-only audit log.

> `code/main.py` implements a toy PII scrubber with consistent tokenization and an append-only audit log.

## Ship It | 产出物

This lesson produces `outputs/skill-llm-security-plan.md`. Given regulatory scope and current state, plans the vault migration, scrubber, egress, audit log.

> 本课产出 `outputs/skill-llm-security-plan.md`. Given regulatory scope and current state, plans the vault migration, scrubber, egress, audit log.

## Exercises | 练习题

1. Run `code/main.py`. Send two prompts referencing the same SSN. Confirm both get the same placeholder.
   中文翻译：运行 `code/main.py`。发送两个引用相同 SSN 的提示。确认两者获得相同的占位符。
2. Design the network egress policy for a vLLM-on-EKS deployment calling OpenAI + Anthropic + Weaviate.
   中文翻译：为调用 OpenAI 和 Anthropic 的 vLLM-on-EKS 部署设计网络出口策略。
3. You discover a key in git history (2 years old). What's the correct response — rotate the key, scrub history, or both? Justify.
   中文翻译：你在 git 历史中发现一个密钥（2 年前）。正确的响应流程是什么？
4. Your audit log grows 10 GB/day. Design retention tiers (hot 30d, warm 12mo, cold 6yr).
   中文翻译：你的审计日志每天增长 10GB。设计保留层级（热 30 天、温 12 月、冷 6 年）。
5. Argue whether reverse-tokenization (substituting real values back into LLM response) is worth the complexity versus keeping placeholders visible.

## Key Terms | 术语速查表

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

## Further Reading | 延伸阅读

- [Doppler — Advanced LLM Security](https://www.doppler.com/blog/advanced-llm-security)
- [Portkey — Manage LLM API keys with secret references](https://portkey.ai/blog/secret-references-ai-api-key-management/)
- [Datadog — LLM Guardrails Best Practices](https://www.datadoghq.com/blog/llm-guardrails-best-practices/)
- [JumpServer — Secrets Management Best Practices 2026](https://www.jumpserver.com/blog/secret-management-best-practices-2026)
- [Microsoft Presidio](https://github.com/microsoft/presidio) — PII detection and anonymization.
- [HashiCorp Vault docs](https://developer.hashicorp.com/vault/docs)
