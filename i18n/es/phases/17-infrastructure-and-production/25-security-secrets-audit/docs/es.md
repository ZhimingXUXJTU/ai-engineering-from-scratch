# Seguridad  Secretos, API de rotación de llaves, registros de auditoría, guardrails  Seguridad  llave  auditoría

> Eliminar la expansión secreta a través de bóvedas centralizadas (Bóveda de HashiCorp, Administrador de secretos de AWS, bóveda de llaves de Azure). Nunca almacenes credenciales en archivos de configuración, archivos env en VCS, hojas de cálculo. Utilice roles de IAM en lugar de claves estáticas; OIDC para CI/CD. El patrón de puerta de entrada de IA es la solución 2026: aplicaciones → puerta de entrada → proveedor de modelos, con puerta de entrada extrayendo credenciales de la bóveda en el tiempo de ejecución. Gira en la bóveda y todas las aplicaciones se recogen en minutos  no redistribuciones, no Slack "quién tiene la nueva llave" mensajes. Política de rotación ≤ 90 días; escaneo con TruffleHog / GitGuardian / Gitleaks en cada compromiso. Cero confianza: MFA, SSO, RBAC/ABAC, fichas de corta duración, postura del dispositivo. El despeje de PII utiliza el reconocimiento de entidades para enmascarar PHI/PII antes de su reenvío; la tokenización consistente (enfoque Mesh) mapea valores sensibles para los titulares de puestos estables para que el LLM preserve la semántica de código/relación. Exceso de red: servicios de LLM en subredes VPC/VNet dedicadas en la lista blanca `api.openai.com`¿ Qué ?`api.anthropic.com`El controlador de incidente 2026: el ataque de la cadena de suministro de Vercel a través de credenciales de CI / CD comprometidas exfiltraron el entorno a través de miles de implementaciones de clientes.

> **【中文解读】**Este capítulo presenta la gestión y la auditoría de claves de seguridad en el servicio LLM.


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy PII-scrubber + audit-log writer) | **语言:** Python
**Prerequisites:** Phase 17 · 19 (AI Gateways), Phase 17 · 13 (Observability) | **前置知识:** Phase 17 · 19 (AI Gateways), Phase 17 · 13 (Observability)

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 17·19(AI Gateway) ‧Fase 17·13(可观测性) ‧零信任架构基础──安全核心:消除密钥散落+集中化保管──
> ¿ Qué es esto ?**【类比】**LLM 安全 = "金库管理"──集中化 vault(HashiCorp Vault/AWS Secrets Manager/Azure Key Vault) = 钱放银行;config/env/电子表格存储密钥 = 藏在床下。AI Gateway 模式 = 应用→网关→模型商,网关运行时从库取密钥;轮换 ≤90 天,所有应用自动跟上,无需重新部署──零信任:MFA+SSO+RBAC+短时──PII 脱敏:实体识别遮蔽 PHI/PII──egress 白名单只放.openai.com 等──
> ️ **【易错点】**Vercel 2026  cadena de suministro ataque caso:CI/CD 凭证被攻破→泄露数千客户环境──修复:CI/CD 用OIDC而非长期密钥──
**Time:** ~60 minutes | **时间:** ~60 minutes

## Objetivos de aprendizaje

- Enumera los cuatro patrones anti-gestión secreta (archivos de configuración en VCS, env codificado en forma dura, hojas de cálculo, claves estáticas) y nombra sus reemplazos.
  ChinaXiv:列举四个密钥管理反模式(VCS配置文件、硬编码环境变量、电子表格共享密钥、共享服务账户)
- Explica el patrón de AI-gateway-pulls-from-vault como estándar de producción de 2026.
  China 网关从 Vault 拉取密钥的模式作为2026年生产标准.
- Implementar un despector de PII con tokenización consistente (el mismo valor → el mismo poseedor de lugar) para que la semántica sobreviva.
  En el caso de los equipos de limpieza, el PII 清洗器 (PII) 清洗器 (PII) 清洗器 (PII) 清洗器 (PII) 清洗器 (PII) 清洗器 (PII) 清洗器 (PII) 清洗器 (PII) 清洗器 (PII) 清洗器 (PII) 清洗器 (PII) 清洗器 (PII) 清洗器 (PII) 清洗器 (PII) 清洗器 (PII) 清洗器 (PII) 清洗器 (PII) 清洗器 (PII) 清洗器 (PII) 清洗器 (PII) 清洗器) 清洗器 (PII) 清洗器 (PII) 清洗器) 清洗器 (PII) 清洗器) 清洗器 (PII) 清洗器) 清洗器 (PII) 清洗器) 清洗器 (PII) 清洗器) 清洗器 (P) 清洗器) 清洗器
- Nombre del incidente de la cadena de suministro Vercel 2026 y lo que enseñó sobre la higiene de las credenciales CI/CD.
  China                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             

## El problema es la introducción del problema

> **【中文解读】**La seguridad de los servicios de LLM se debe resolver en tres fases: 1)`.env`含 API keys,已在 git 历史中,轮换流程是"Slack 群发,更新 40 配置文件,重新部署所有服务8小时后只有一半服务上线";(2) PII 泄露用户提示包含"Mi SSN es 123-45-6789", directamente enviado a OpenAI, aunque hay BAA pero la política interna requiere que se envíe pre-脱敏;(3) 网络出口EKS 集群的 LLM Pod puede acceder a cualquier Internet host, alguien puede consultar a través de DNS a los dominios de los datos fuera de los nombres de los atacantes controlados.

> **【拓展：2026 年 LLM 安全事件】**Los eventos de seguridad típicos de LLM del año 2026 incluyen: 1) Un ataque a la cadena de suministro de versales  un CI / CD dañado 凭证外泄漏数千客户部署的环境变量; 2) una sugerencia de ataque  a través de un usuario ingresar a manipular LLM  ejecutar operaciones inesperadas; 3) una fuga de datos  LLM en respuesta a una fuga de datos de entrenamiento  información sensible  medidas de defensa incluyen:集中式 Vault  HashiCorp Vault  AWS White Secrets Manager)  PII 脱敏  Psypy NER + Presidio)  nombre de exportación de red                                                                                                                                                                                

Un pasante se compromete `.env`Las claves ya están en el historial de git  GitGuardian scan lo capta, su proceso de rotación es "Reacordar el equipo, actualizar 40 archivos de configuración, redistribuir todos los servicios". 8 horas después, la mitad de sus servicios están en vivo y la mitad están esperando para implementar ventanas.

Separadamente, las instrucciones de usuario incluyen "Mi SSN es 123-45-6789." La instrucción va a OpenAI. Tienes un BAA pero tu política interna es enmascarar PII antes de reenviar.

Separadamente, el módulo de LLM de tu grupo EKS puede llegar a cualquier host de Internet alguien exfila datos a través de búsqueda DNS a un dominio controlado por el atacante.

La seguridad para los servicios de LLM tiene que abordar los tres vectores: credenciales respaldadas por bóvedas, limpieza de PII, filtrado de salida de red, registros de auditoría.

## El concepto central.

### Tresera centralizada + tirón de rol de IAM

> **【拓展：AI 网关密钥管理模式】**2026 años LLM  servicios de gestión de llaves                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  `OPENAI_API_KEY` Después de cambiar la clave en el Vault, la próxima vez que se solicite obtener la nueva clave automáticamente  No se necesita volver a implementar  No se necesita Slack  Quien tiene la nueva clave  El Vault es compatible con: HashiCorp Vault  AWS Secrets Manager  Azure Key Vault  GCP Secret Manager  Aplicar la clave de IAM 角色认证  Aplicación a través de IAM Personalidad y no Identificación de la clave de estado 

**Vault**HashiCorp Vault, AWS Secrets Manager, Azure Key Vault, GCP Secret Manager. Una fuente de verdad.

**IAM role**: app/gateway autentica a través de su identidad IAM, no una clave estática. Vault devuelve el secreto para la vida útil del token.

**The AI-gateway pattern**: puesta de puerta `OPENAI_API_KEY`girar en la bóveda, la próxima solicitud obtiene la nueva llave.

### Política de rotación ≤ 90 días

Todas las claves de API, token de raíz de la bóveda, credenciales CI/CD. Rotación automática cuando sea posible.

### Escaneo secreto

- **TruffleHog** regex + entropía en los commits.
- **GitGuardian** comercial, alta precisión.
- **Gitleaks** OSS, se ejecuta en CI.

En cualquier momento, bloquear las relaciones públicas si se descubre un nuevo secreto.

### Posición de cero confianza

- Exigen las MFA en todas las cuentas.
- SSO a través de SAML/OIDC.
- RBAC (basado en el papel) o ABAC (basado en el atributo) para el acceso a granos finos.
- Tokens de corta duración (horas, no días).
- Posición del dispositivo  solo dispositivos corporativos con encriptación de disco.

### El uso de la limpieza PII/PHI

> **【中文解读】**PII/PHI 脱敏的四步流程:(1) 实体识别(spaCy NER、Presidio、商业工具);(2) 掩码匹配的实体"Mi SSN es 123-45-6789" → "Mi SSN es [SSN_TOKEN_A3F]";(3) 一致性标记化(Mesh 方法)相同值映射到相同占位符,LLM可以保持关系语义;(4) 可选的LLM 响应逆映射;;静态正则过器捕获基本模式,NER 捕获更多两者都使用;;

Antes de que el aviso salga de su infra:

1. Reconocimiento de entidades (spaCy NER, Presidio, comercial).
2. Las entidades que se encuentran en la máscara: `"My SSN is 123-45-6789"`¿ Qué es esto ?`"My SSN is [SSN_TOKEN_A3F]"`¿ Qué ?
3. Tokenización consistente (enfoque Mesh): mapas de valores similares a los mismos titulares de lugar para que el LLM preserve las relaciones.
4. Mapeo opcional inverso para la respuesta del LLM.

Los filtros de regex estáticos capturan patrones básicos, el NER capta más.

### Barrancas de entrada y salida

Entrada: bloquear las violaciones de seguridad conocidas, temas prohibidos; límite de tarifas por usuario.

Resultado: regex scrub para secretos filtrados (patrones de claves API, patrones de correo electrónico en contextos de rechazo), clasificador de violaciones de políticas.

### Lista blanca de salida de red

> **【拓展：LLM 安全纵深防御】**Las estrategias de defensa de larga duración del servicio LLM incluyen: 1) 集中式 Vault + IAM 角色拉取应用/网关通过 IAM 身份认证, Vault 返回有限期令牌,轮换在 Vault 中完成,所有应用自动获得新密钥; 2) AI 网关模式应用→网关→供应商,网关从 Vault 拉取凭证,无需重新部署; 3) 90 天轮换策略所有API key 关键基代币、CI/CD 凭证; 4) Cada año envío de una exploración TruffleHog / GitGuardian 关键在 CI contiene nuevos llaves de PR; 5) 无可变审计日志 每次提示 LLM 调tok户时间应应用户/租、哈希模型 哈希模型 版本 SO ̊、响应 响应   关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 

Servicios de LLM en una subred dedicada:
- Lista blanca: `api.openai.com`¿ Qué ?`api.anthropic.com`, puntos finales de vector DB, puntos finales de bóveda.
- Todo lo demás: dejar caer.
- DNS a través de resolver de solo permisores (evitar exfil de tunelado de DNS).

### Registro de auditoría

Registro inmutable de cada llamada de LLM con:
- - Es un sello de tiempo.
- Usuario / inquilino.
- Hash rápido (no en bruto para privacidad).
- Modelo + versión.
- Las fichas cuentan.
- El costo.
- Respuesta de la hacha.
- Cualquier viaje de vigilancia.

Recepción por requerimiento regulatorio (SOC 2 1 año, HIPAA 6 años).

### El incidente de Vercel de 2026

El ataque de cadena de suministro: las credenciales de CI/CD comprometidas se filtraron en el entorno a través de miles de implementaciones de clientes.

### Números que debes recordar

- Política de rotación: ≤ 90 días.
- Escanear en cada comit: TruffleHog / GitGuardian / Gitleaks.
- Vercel 2026: Créditos de CI/CD comprometidos → miles de clientes se filtraron.
- Retención del registro de auditoría: SOC 2 = 1 año, HIPAA = 6 años.

## Usalo con el marco de ejecución
```figure
i4-vault-rotation
```

## Usalo

`code/main.py`Implementa un limpiador de DII de juguete con tokenización consistente y un registro de auditoría solo en apéndice.

> `code/main.py`Implementa un limpiador de DII de juguete con tokenización consistente y un registro de auditoría solo en apéndice.

> `code/main.py`Implementa un limpiador de DII de juguete con tokenización consistente y un registro de auditoría solo en apéndice.

## Envíe el producto .

Esta lección produce`outputs/skill-llm-security-plan.md`Dado el alcance regulatorio y el estado actual, los planes de migración de la bóveda, limpieza, salida, registro de auditoría.

> 本课产 出  `outputs/skill-llm-security-plan.md`Dado el alcance regulatorio y el estado actual, los planes de migración de la bóveda, limpieza, salida, registro de auditoría.

## Los ejercicios.

1. - ¿ Qué ?`code/main.py`Envía dos mensajes de referencia al mismo nombre de identidad.
   Traducción:运行`code/main.py` Enviar dos citas del mismo SSN  confirmar que ambos obtuvieron el mismo ocupante 
2. Diseñar la política de salida de red para una implementación de vLLM-on-EKS llamando OpenAI + Anthropic + Weaviate.
   China 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部署 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 部 
3. Descubre una llave en el historial de git (2 años) ¿Cuál es la respuesta correcta  girar la llave, borrar el historial, o ambos?
   En la historia encontraste una clave. ¿Cuál es el verdadero proceso de respuesta?
4. Su registro de auditoría crece 10 GB/día.
   En el caso de los bancos centrales, el número de bancos centrales en el país es de 10 GB.
5. Argumentar si la tokenización inversa (sustituir los valores reales de nuevo en respuesta de LLM) vale la complejidad frente a mantener a los titulares de lugar visibles.

## Términos clave .

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

## Más Leer más Leer más

- [Doppler — Advanced LLM Security](https://www.doppler.com/blog/advanced-llm-security)
- [Portkey — Manage LLM API keys with secret references](https://portkey.ai/blog/secret-references-ai-api-key-management/)
- [Datadog — LLM Guardrails Best Practices](https://www.datadoghq.com/blog/llm-guardrails-best-practices/)
- [JumpServer — Secrets Management Best Practices 2026](https://www.jumpserver.com/blog/secret-management-best-practices-2026)
- [Microsoft Presidio](https://github.com/microsoft/presidio) Detección y anonimización de PII.
- [HashiCorp Vault docs](https://developer.hashicorp.com/vault/docs)
