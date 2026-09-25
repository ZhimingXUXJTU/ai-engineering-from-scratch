# Segurança  Segredos, rotação de chaves API, registros de auditoria, guardrails  Segurança  chave  auditoria

> Eliminar a expansão secreta através de cofres centralizadas (HashiCorp Vault, AWS Secrets Manager, Azure Key Vault). Nunca armazenem credenciais em arquivos de configuração, arquivos env em VCS, planilhas. Usar roles IAM em vez de chaves estáticas; OIDC para CI/CD. O padrão de gateway da IA é a solução 2026: aplicativos → gateway → provedor de modelo, com gateway tirando credenciais do cofre no tempo de execução. Rote em cofre e todos os aplicativos captam em minutos. Sem redistribuições, sem mensagens do Slack "quem tem a nova chave". Política de rotação ≤ 90 dias; escaneamento com TruffleHog / GitGuardian / Gitleaks em cada compromisso. Capacidade de segurança zero: MFA, SSO, RBAC/ABAC, tokens de curta duração, postura do dispositivo. A limpeza de PII utiliza o reconhecimento de entidades para mascarar o PHI/PII antes da encaminhamento; a tokenização consistente (abordagem Mesh) mapeia valores sensíveis para titulares de posições estáveis, de modo que o MLL preserva a semântica de código/relação. A saída da rede: serviços de LLM em sub-rede VPC/VNet dedicada apenas em lista branca `api.openai.com`- Não .`api.anthropic.com`O motor de incidente de 2026: ataque da cadeia de suprimentos Vercel através de credenciais de CI/CD comprometidas, filtrado em milhares de implantações de clientes.

> **【中文解读】**Esta secção apresenta o gerenciamento e o auditório de segurança das chaves no serviço LLM.


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy PII-scrubber + audit-log writer) | **语言:** Python
**Prerequisites:** Phase 17 · 19 (AI Gateways), Phase 17 · 13 (Observability) | **前置知识:** Phase 17 · 19 (AI Gateways), Phase 17 · 13 (Observability)

> - Não .**【前置】**O primeiro passo é o primeiro passo: a fase 17·19 (AI Gateway)  a fase 17·13 (可观测性)  a base de estrutura de confiança.
> - Não .**【类比】**LLM 安全 = "金库管理"──集中化 vault(HashiCorp Vault/AWS Secrets Manager/Azure Key Vault) = 钱放银行;config/env/电子表格存储密钥 = 藏在床下。AI Gateway 模式 = 应用→网关→模型商,网关运行时从 vault 取密钥;轮换 ≤90 天,所有应用自动跟上,无需重新部署──零信任:MFA+SSO+RBAC+短时──PII 脱敏:实体识别遮蔽 PHI/PII──egress 白名单只放.openai.com 等──
> ️ **【易错点】**Vercel 2026  fornecimento cadeia de ataque caso:CI/CD 凭证被攻破→泄露数千客户环境──修复:CI/CD 用OIDC而非长期密钥──
**Time:** ~60 minutes | **时间:** ~60 minutes

## Objetivos de aprendizagem

- Enumere os quatro padrões anti-gestão secreta (arquivos de configuração em VCS, env codificado com código rígido, planilhas, chaves estáticas) e nomeie os seus substitutores.
  Chinese Language Translation:列举四个密钥管理反模式(VCS配置文件、硬编码环境变量、电子表格共享密钥、共享服务账户) ⋅
- Explicar o padrão de AI-gateway-puls-out-vault como padrão de produção de 2026.
  Tradução do inglês para tradução do inglês: Explain AI 网关从 Vault 拉取密钥的模式作为2026年生产标准──
- Implementar um esfregador de PII com tokenização consistente (o mesmo valor → mesmo reservatório) para que a semântica sobreviva.
  中文翻译:实现带一致性标记化的 PII 清洗器(相同值 -> 相同占位符) 』
- Cite o incidente da cadeia de suprimentos da Vercel de 2026 e o que ele ensinou sobre a higiene de credenciais CI/CD.
  Chinese:                                                                                                                                                                                                                                                              

## O problema é o problema da introdução

> **【中文解读】**Mestrado em Direito e Direito em Direito e Direito em Direito e Direito em Direito e Direito em Direito e Direito em Direito e Direito em Direito e Direito em Direito e Direito em Direito e Direito em Direito e Direito em Direito e Direito em Direito e Direito em Direito e Direito em Direito e Direito em Direito e Direito em Direito e Direito em Direito e Direito em Direito e Direito em Direito e Direito em Direito e Direito em Direito e Direito em Direito e Direito em Direito e Direito`.env`含 API keys,已在 git 历史中,轮换流程是"Slack 群发,更新 40 配置文件,重新部署所有服务8 小时后只有半服务上线";(2) PII 泄露用户提示包含"Meu SSN é 123-45-6789", enviada diretamente para OpenAI, embora haja BAA, mas a política interna exige que seja enviada antes de sair;(3) 网络出口EKS 集群的 LLM Pod pode visitar qualquer internet host, alguém pode consultar através do DNS até o domínio do nome do invasor controlar dados fora de fuga.

> **【拓展：2026 年 LLM 安全事件】**Os eventos de segurança típicos do LLM de 2026 incluem: 1) Ataques de cadeia de fornecimento Vercel                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    

Um estagiário comete `.env`As chaves já estão no histórico de git  GitGuardian scan capta-o, o seu processo de rotação é "Relax a equipe, atualizar 40 arquivos de configuração, redistribuir todos os serviços". 8 horas depois, metade dos seus serviços estão em funcionamento e metade estão esperando para a implantação de janelas.

Separadamente, as instruções do usuário incluem "Meu SSN é 123-45-6789." A instrução vai para OpenAI. Você tem um BAA, mas sua política interna é mascarar PII antes de reenviar.

Separadamente, o módulo de LLM do seu cluster EKS pode chegar a qualquer hospedeiro de Internet. Alguém exfila dados através da busca DNS para um domínio controlado pelo atacante. Nada o bloqueou.

A segurança dos serviços LLM tem de abordar os três vetores: credenciais de segurança, limpeza de PII, filtragem de saída de rede, registros de auditoria.

## O conceito central.

### Segurança de segurança

> **【拓展：AI 网关密钥管理模式】**2026 ano LLM  serviços de gestão de chaves                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  `OPENAI_API_KEY` Depois de trocar a chave de chave no Vault, a próxima vez que você solicitar automaticamente obter a nova chave, não é necessário a redeposição, não é necessário o Slack.

**Vault**HashiCorp Vault, AWS Secrets Manager, Azure Key Vault, GCP Secret Manager. Uma fonte de verdade.

**IAM role**O aplicativo/gateway autentica através da sua identidade IAM, não de uma chave estática.

**The AI-gateway pattern**: gateway pulls `OPENAI_API_KEY`A próxima solicitação recebe a nova chave.

### Política de rotação ≤ 90 dias

Todas as chaves API, token de raiz do cofre, credenciais CI/CD, rotação automática quando possível, rotação manual registrada e rastreada.

### Escanagem secreta

- **TruffleHog** regex + entropia em commits.
- **GitGuardian** comercial, alta precisão.
- **Gitleaks**OSS, em CI.

Corra em cada compromisso, bloqueia as relações públicas se descobrirem um novo segredo.

### Posição de confiança zero

- A MFA é exigida em todas as contas.
- OSS através do SAML/OIDC.
- RBAC (baseado em funções) ou ABAC (baseado em atributos) para acesso a grãos finos.
- Tokens de curta duração (horas, não dias).
- Posição do dispositivo  apenas dispositivos corporativos com criptografia de disco.

### Esfriamento PII/PHI

> **【中文解读】**PII/PHI 脱敏的四步流程:(1) 实体识别(spaCy NER、Presidio、商业工具);(2) 掩码匹配的实体"Meu SSN é 123-45-6789" → "Meu SSN é [SSN_TOKEN_A3F]";(3) 一致性标记化(Mesh 方法)相同值映射到相同占位符,LLM可以保持关系语义;(4) 可选的LLM 响应逆映射;;静态正则过器捕获基本模式,NER 捕获更多两者都使用;;

Antes que o aviso deixe a sua infra:

1. Reconhecimento da entidade (spaCy NER, Presidio, comercial).
2. Mascaras de equiparamento: `"My SSN is 123-45-6789"`→ `"My SSN is [SSN_TOKEN_A3F]"`- Não .
3. Tokenization consistente (approche Mesh): mapas de valores iguais para o mesmo titular de lugar para que o MLL preserve as relações.
4. Mapeamento opcional para resposta ao Mestrado em Direito Jurídico.

Os filtros estáticos regex capturam padrões básicos, o NER capturam mais.

### Proteção de entrada + saída

Entrada: bloquear os jailbreaks conhecidos, tópicos proibidos; limite de taxa por usuário.

Resultado: scrub regex para segredos vazados (patrões de chave API, padrões de e-mail em contextos de recusa), classificador para violações de políticas.

### Lista branca de saída da rede

> **【拓展：LLM 安全纵深防御】**As estratégias de defesa de longo prazo do LLM incluem: 1) 集中式 Vault + IAM 角色拉取应用/网关通过 IAM 身份认证, Vault 返回有限期令牌,轮换在 Vault 中完成,所有应用自动获得新密钥; 2) AI 网关模式应用→网关→供应商,网关从 Vault 拉取凭证,无需重新部署; 3) 90 天轮换策略所有API keynote 关键基 token、CI/CD 凭证; 4) Cada ano de submissão de uma análise TruffleHog / GitGuardian / Gitleaks bloqueia um PR de nova chave no CIPA; 5) 无可变审计日志

Serviços de MLL numa subrede dedicada:
- Lista branca: `api.openai.com`- Não .`api.anthropic.com`, pontos finais do vector DB, pontos finais do cofre.
- Tudo o resto: lança.
- DNS via resolvedor de apenas alistado (evitar exfil de túnel DNS).

### Registo de auditoria

Registo imutável de cada chamada de LLM com:
- - O tempo.
- Utilizador/arrendador.
- Hash de imediato (não de imediato para privacidade).
- Modelo + versão.
- Os tokens contam.
- - O custo.
- Resposta hash.
- Qualquer viagem de guarda.

Reter por exigência regulatória (SOC 2 1 ano, HIPAA 6 anos).

### O incidente de Vercel de 2026

Ataque de cadeia de suprimentos: credenciais de CI/CD comprometidas filtradas em milhares de implantações de clientes. Lição: credenciais de CI/CD são equivalentes a prod. Armazenar em cofre. Capacidade estreita. Rotar agressivamente.

### Números que você deve lembrar

- Política de rotação: ≤ 90 dias.
- Escanar em cada compromisso: TruffleHog / GitGuardian / Gitleaks.
- Vercel 2026: Créditos de CI/CD comprometidos → milhares de clientes em contacto com a empresa foram vazados.
- Retenção do registro de auditoria: SOC 2 = 1 ano, HIPAA = 6 anos.

## Use-o com o framework implementado.
```figure
i4-vault-rotation
```

## Usá-lo

`code/main.py`Implementa um esfregador de PII de brinquedo com tokenização consistente e um registro de auditoria apenas apêndice.

> `code/main.py`Implementa um esfregador de PII de brinquedo com tokenização consistente e um registro de auditoria apenas apêndice.

> `code/main.py`Implementa um esfregador de PII de brinquedo com tokenização consistente e um registro de auditoria apenas apêndice.

## Envia-o . Produto .

Esta lição produz`outputs/skill-llm-security-plan.md`Considerando o âmbito regulamentar e o estado atual, planeja a migração do cofre, a limpeza, a saída, o registro de auditoria.

> 本课产 出 `outputs/skill-llm-security-plan.md`Considerando o âmbito regulamentar e o estado atual, planeja a migração do cofre, a limpeza, a saída, o registro de auditoria.

## Exercícios.

1. Corra .`code/main.py`Envie duas mensagens com a mesma identidade de nome e confirme que ambos têm o mesmo nome.
   Tradução: 运行`code/main.py` Enviar duas citações do mesmo SSN  confirmar que ambos obtiveram o mesmo ocupador 
2. Desenhar a política de saída de rede para uma implantação vLLM-on-EKS chamando OpenAI + Anthropic + Weaviate.
   Tradução do inglês para Chinês: 部署设计网络出口策略.
3. Você descobre uma chave no histórico de git (2 anos). Qual é a resposta correta  rodar a chave, esfregar o histórico, ou ambos?
   Tradução do inglês:You discovered a key in git 历史 (You found a key in git 历史)
4. O seu registro de auditoria cresce 10 GB/dia. Níveis de retenção de design (caldo 30 dias, quente 12 meses, frio 6 anos).
   Chinese: 你的审计日志每天增长 10GB──设计保留层级(热 30 天、温 12 月、冷 6 年)──
5. Argumentar se a tokenização inversa (substituindo os valores reais de volta para a resposta de LLM) vale a pena a complexidade versus manter os titulares de lugar visíveis.

## Termos-chave .

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

## Mais leitura 延伸阅读

- [Doppler — Advanced LLM Security](https://www.doppler.com/blog/advanced-llm-security)
- [Portkey — Manage LLM API keys with secret references](https://portkey.ai/blog/secret-references-ai-api-key-management/)
- [Datadog — LLM Guardrails Best Practices](https://www.datadoghq.com/blog/llm-guardrails-best-practices/)
- [JumpServer — Secrets Management Best Practices 2026](https://www.jumpserver.com/blog/secret-management-best-practices-2026)
- [Microsoft Presidio](https://github.com/microsoft/presidio) Detecção e anonimização de PII.
- [HashiCorp Vault docs](https://developer.hashicorp.com/vault/docs)
