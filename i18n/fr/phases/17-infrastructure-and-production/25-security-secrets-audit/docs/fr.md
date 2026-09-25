# Sécurité  Secrets, API clé rotation, journaux d'audit, gardages  Sécurité  clé  vérification

> Éliminer la diffusion secrète via des coffres-forts centralisés (coffre-fort HashiCorp, gestionnaire de secrets AWS, coffre-fort Azure). Ne stockez jamais les informations dans les fichiers de configuration, env fichiers dans VCS, feuilles de calcul. Utiliser des rôles IAM au lieu de clés statiques; OIDC pour CI/CD. Le modèle d'IA-gateway est la solution 2026: applications → gateway → fournisseur de modèle, avec gateway tirant des informations d'identification de la caisse en temps d'exécution. Retournez dans la caisse et toutes les applications se dérouleront en quelques minutes  pas de redéploiements, pas de Slack "qui a la nouvelle clé" messages. Politique de rotation ≤ 90 jours; analyse avec TruffleHog / GitGuardian / Gitleaks à chaque commande. La confiance nulle: MFA, SSO, RBAC/ABAC, jetons de courte durée, posture du dispositif. Le scrubbing des PII utilise la reconnaissance d'entités pour masquer les PHI/PII avant de les transférer; la tokenization cohérente (approche Mesh) trace les valeurs sensibles aux titulaires de places stables afin que le LLM préserve la sémantique du code/relation. Exit du réseau: services de LLM dans des sous-réseaux VPC/VNet dédiés uniquement en liste blanche `api.openai.com`- Je suis là .`api.anthropic.com`Le pilote d'incident 2026: l'attaque de la chaîne d'approvisionnement Vercel via des informations de base CI/CD compromises a filtré l'environnement sur des milliers de déploiements de clients.

> **【中文解读】**Ce chapitre présente la gestion et l'audit des clés de sécurité dans le service LLM.


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy PII-scrubber + audit-log writer) | **语言:** Python
**Prerequisites:** Phase 17 · 19 (AI Gateways), Phase 17 · 13 (Observability) | **前置知识:** Phase 17 · 19 (AI Gateways), Phase 17 · 13 (Observability)

>  **【前置】**Pour les autres, il est nécessaire de se préparer à la mise en œuvre de la stratégie de mise en œuvre de la stratégie de mise en œuvre de la stratégie de mise en œuvre de la stratégie de mise en œuvre de la stratégie de mise en œuvre de la stratégie de mise en œuvre de la stratégie de mise en œuvre de la stratégie de mise en œuvre de la stratégie de mise en œuvre de la stratégie de mise en œuvre de la stratégie de mise en œuvre de la stratégie de mise en œuvre de la stratégie de mise en œuvre de la stratégie de mise en œuvre de la stratégie de mise en œuvre de la stratégie de mise en œuvre de la stratégie de mise en œuvre de la stratégie de mise en œuvre de la stratégie de mise en œuvre de la stratégie de mise en œuvre de la stratégie de mise en œuvre de la stratégie de mise en œuvre de la stratégie de mise en œuvre de la stratégie de mise en œuvre de la stratégie de mise en œuvre de la stratégie de mise en œuvre de la stratégie de mise en œuvre de la stratégie de mise en œuvre de la stratégie de mise en œuvre de la stratégie de mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de mise en en en en en en en en en en en en en en en en en en en.
>  **【类比】**La gestion de la trésorerie est une fonction de la gestion de la trésorerie et de la gestion des trésorerie. Elle est la fonction de la gestion de la trésorerie et de la gestion des trésorerie.
> ️ **【易错点】**Vercel 2026  attaque de chaîne de fourniture Cas: CI/CD 凭证被攻破→ divulguer des milliers de clients envèrs──修复:CI/CD Utiliser OIDC而非长期密钥──
**Time:** ~60 minutes | **时间:** ~60 minutes

## Objectifs d'apprentissage

- Enumérez les quatre modèles anti-gestion secrète (fichiers de configuration dans VCS, env hardcodé, feuilles de calcul, clés statiques) et nommez leurs remplacements.
  Le code de gestion de la clé est un code de gestion de la clé.
- Expliquez le modèle d'IA-gateway-pulls-from-vault comme norme de production de 2026.
  Le modèle de production de l'IA 网关从 Vault 拉取密钥的模式作为2026年生产标准.
- Implémenter un dépistage des PII avec une tokénisation cohérente (même valeur → même placeholder) afin que la sémantique survienne.
  Le même nombre de personnes qui ont été identifiées dans le même document sont les personnes qui ont été identifiées dans le même document.
- Nombre de l'incident de 2026 de la chaîne d'approvisionnement Vercel et ce qu'il a enseigné sur l'hygiène des certificats CI/CD.
  Le programme de formation de la société de l'information et de l'information (CCI) a été lancé en 2026 par Vercel.

## Le problème , l' introduction du problème

> **【中文解读】**Les besoins en sécurité de la formation en droit sont résolus en trois dimensions: 1)`.env`含 API keys, déjà dans l'histoire, le processus de rotation est "Slack 群发, mettre à jour 40 配置文件, redéploiement de tous les services8 小时后只有一半服务上线";(2) PII 泄露用户提示包含"Mon SSN est 123-45-6789", directement envoyé à OpenAI, bien qu'il existe des BAA mais une politique interne exige l'envoi de pré-détachement;(3) 网络出口EKS 集群的LLM Pod peut accéder à n'importe quel hôte Internet, quelqu'un peut consulter les données de domaine contrôlé par l'attaquant via DNS 外泄密数据.

> **【拓展：2026 年 LLM 安全事件】**Les événements de sécurité typiques de l'année 2026 comprennent: 1) Attaques de chaîne de fourniture versables  Attaques de chaîne de fourniture  Attaques de chaîne de fourniture  Attaques de chaîne de fourniture  Attaques de chaîne de fourniture  Attaques de chaîne de fourniture  Attaques de chaîne de fourniture  Attaques de chaîne de fourniture  Attaques de chaîne de fourniture  Attaques de chaîne de fourniture  Attaques de chaîne de fourniture  Attaques de chaîne de fourniture  Attaques de chaîne de fourniture  Attaques de chaîne de fourniture  Attaques de chaîne de fourniture  Attaques de chaîne de fourniture  Attaques de chaîne de fourniture  Attaques de chaîne de fourniture  Attaques de chaîne de fourniture  Attaques de chaîne de fourniture  Attaques de chaîne de fourniture  Attaques de chaîne de fourniture  Attaques  Attaques de chaîne de fourniture  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques  Attaques

Un stagiaire s' engage `.env`Les clés sont déjà dans l'historique de git  GitGuardian scan le capture, votre processus de rotation est "Réfraîchir l'équipe, mettre à jour 40 fichiers de configuration, redéployer tous les services". 8 heures plus tard, la moitié de vos services sont en direct et la moitié attendent le déploiement des fenêtres.

Les instructions de l'utilisateur incluent "Mon SSN est 123-45-6789. " L'adresse est OpenAI. Vous avez un BAA mais votre politique interne est de masquer les informations personnelles avant de les envoyer.

Par ailleurs, le module de votre groupe EKS peut atteindre n'importe quel hôte Internet, quelqu'un exfilte les données via DNS à un domaine contrôlé par l'attaquant.

La sécurité des services de LLM doit s'attaquer à tous les trois vecteurs: les informations de confiance sous forme de voûte, le dépistage des données personnelles, le filtrage des sorties réseau, les journaux d'audit.

## Le concept de base.

### Voûte centralisée + tirage du rôle IAM

> **【拓展：AI 网关密钥管理模式】**2026 ans LLM 服务的密钥管理最佳实践AI 网关模式:应用→网关→模型提供商,网关在请求时从 Vault 拉取 `OPENAI_API_KEY` Après avoir changé la clé de la Vault, la prochaine fois que vous aurez demandé de la clé de la Vault, vous obtiendrez automatiquement la clé de la Vault sans avoir besoin de la déployer sans avoir besoin de Slack.

**Vault**HashiCorp Vault, AWS Secrets Manager, Azure Key Vault, GCP Secret Manager. Une source de vérité.

**IAM role**: app/gateway authentifie par son identité IAM, pas une clé statique. Vault renvoie le secret pour la durée de vie du jeton.

**The AI-gateway pattern**: porte de sortie `OPENAI_API_KEY`Retournez dans la chambre à sous, la prochaine demande obtient la nouvelle clé.

### Politique de rotation ≤ 90 jours

Toutes les clés API, les jetons racines de la caisse, les informations d'identification CI/CD, la rotation automatique lorsque cela est possible, la rotation manuelle enregistrée et suivie.

### Scanner secret

- **TruffleHog** régex + entropie sur les commits.
- **GitGuardian** commercial, haute précision.
- **Gitleaks** OSS, fonctionne dans l'IC.

Arrêtez les relations si un nouveau secret est détecté.

### Poise de confiance zéro

- Les FAM sont exigés sur tous les comptes.
- SSO par SAML/OIDC.
- RBAC (basé sur le rôle) ou ABAC (basé sur les attributs) pour l'accès aux grains fins.
- Les jetons de courte durée (heures, pas jours).
- Position de l'appareil  seulement les appareils corporels avec cryptage disque.

### PII / PHI de détergition

> **【中文解读】**PII/PHI 脱敏的四步流程:(1) 实体识别(spaCy NER、Presidio、商业工具);(2) 掩码匹配的实体"Mon SSN est 123-45-6789" → "Mon SSN est [SSN_TOKEN_A3F]";(3) 一致性标记化(Mesh 方法)相同值映射到相同占位符,LLM可以保持关系语义;(4) 可选的LLM 响应逆映射;;静态正则过器捕获基本模式,NER 捕获更多两者都使用;;

Avant que le message ne quitte votre infra:

1. Le système de reconnaissance d'entités (spaCy NER, Presidio, commercial).
2. Masque d' entités correspondantes: `"My SSN is 123-45-6789"`- Je suis là.`"My SSN is [SSN_TOKEN_A3F]"`- Je suis désolé .
3. Tokenization cohérente (approche Mesh): cartes de la même valeur pour le même titulaire de place afin que le LLM préserve les relations.
4. Le suivi des résultats de la recherche est un processus de révision des résultats de la recherche.

Les filtres de régex statiques capturent les schémas de base, le NER en capture plus.

### Gardiens d'entrée + sortie

Entrée: blocage des jailbreaks connus, des sujets interdits; limite de tarifs par utilisateur.

Résultats: scrub de régex pour les secrets divulgués (modèles de clés API, modèles de courrier électronique dans les contextes de refus), classifiant pour les violations de politiques.

### Liste blanche des sorties de réseau

> **【拓展：LLM 安全纵深防御】**Les stratégies de défense de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application de l'application

Services de MLL dans un sous-réseau dédié:
- Liste blanche: `api.openai.com`- Je suis là .`api.anthropic.com`, points d'extrémité de vecteur DB, points d'extrémité de voûte.
- Tout le reste: déposez.
- DNS via résolveur réservé aux autorisations (éviter d'exfil d'exfil d'exfil d'exfil de DNS).

### Registre d'audit

Logique immutable de chaque appel de LLM avec:
- Une timestamp.
- Utilisateur / locataire.
- Hash rapide (pas demande brute pour la confidentialité).
- Modèle + version.
- Les jetons comptent.
- Le coût.
- Le hash de réponse.
- Toutes les sorties de garde.

Réservation selon les exigences réglementaires (SOC 2 1 an, HIPAA 6 ans).

### L'incident de Vercel de 2026

Attaque de la chaîne d'approvisionnement: les informations d'identification de l'interface informatique/CD compromises sont filtrées dans l'environnement dans des milliers de déploiements de clients.

### Les chiffres que vous devriez vous rappeler

- Politique de rotation: ≤ 90 jours.
- Scan sur chaque commande: TruffleHog / GitGuardian / Gitleaks.
- Vercel 2026: Crédits d'informations et de données personnelles compromis → Des milliers d'environnements de clients ont été divulgués.
- Rétention du journal d'audit: SOC 2 = 1 an, HIPAA = 6 ans.

## Utilisez-le avec le cadre de réalisation
```figure
i4-vault-rotation
```

## Utilisez-le

`code/main.py`met en œuvre un dépistage des DII de jouets avec une tokenization cohérente et un journal d'audit uniquement annexe.

> `code/main.py`met en œuvre un dépistage des DII de jouets avec une tokenization cohérente et un journal d'audit uniquement annexe.

> `code/main.py`met en œuvre un dépistage des DII de jouets avec une tokenization cohérente et un journal d'audit uniquement annexe.

## Envoyez-le . Produit .

Cette leçon produit `outputs/skill-llm-security-plan.md`- Compte tenu de la portée réglementaire et de l'état actuel, les plans de migration de la caisse, de scrubber, de sortie, de vérification.

> 本课产 出 `outputs/skill-llm-security-plan.md`- Compte tenu de la portée réglementaire et de l'état actuel, les plans de migration de la caisse, de scrubber, de sortie, de vérification.

## Les exercices

1. On court .`code/main.py`Envoyez deux messages faisant référence au même SSN. Confirmez que les deux obtiennent le même placeholder.
   Le mot " l' économie " est traduit par " l' économie ".`code/main.py` Envoyer deux citations du même SSN  Confirmer que les deux ont obtenu le même occupant 
2. Conceptualiser la politique d'exode du réseau pour un déploiement vLLM-on-EKS appelant OpenAI + Anthropic + Weaviate.
   Pour le développement de l'OpenAI et de l'anthropic, le VLLM-on-EKS est un outil de développement de la stratégie de développement de l'OpenAI.
3. Vous découvrez une clé dans l'historique de la git (deux ans). Quelle est la bonne réponse  tourner la clé, scrub l'historique, ou les deux? justifier.
   Vous avez trouvé une clé dans l'histoire.
4. Votre journal d'audit augmente de 10 Go par jour.
   Le nombre de pages de votre journal d'audit augmente de 10 Go par jour.
5. Débattez si la reverse-tokenization (remplacement des valeurs réelles dans la réponse LLM) vaut la complexité par rapport à garder les titulaires de place visibles.

## Les termes clés

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

## Encore une lecture

- [Doppler — Advanced LLM Security](https://www.doppler.com/blog/advanced-llm-security)
- [Portkey — Manage LLM API keys with secret references](https://portkey.ai/blog/secret-references-ai-api-key-management/)
- [Datadog — LLM Guardrails Best Practices](https://www.datadoghq.com/blog/llm-guardrails-best-practices/)
- [JumpServer — Secrets Management Best Practices 2026](https://www.jumpserver.com/blog/secret-management-best-practices-2026)
- [Microsoft Presidio](https://github.com/microsoft/presidio) Détection et anonymisation des informations personnelles.
- [HashiCorp Vault docs](https://developer.hashicorp.com/vault/docs)
