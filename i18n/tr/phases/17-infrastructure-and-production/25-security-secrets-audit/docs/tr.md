# Güvenlik  Sırlar, API Anahtar Dönüşüm, Denetim Günlükleri, Gardalar  Güvenlik  Anahtar  Denetim

> Merkezi kasayı (HashiCorp Vault, AWS Gizemleri Yöneticisi, Azure Anahtar Kasası) kullanarak gizli yayılma ortadan kaldırın. İtirafları asla konfigüratör dosyalarda, VCS'deki env dosyalarında, kalıp sayfalarında saklama. Statik anahtarlar yerine IAM rollerini kullanın; CI/CD için OIDC. AI-gateway örneği 2026 çözümüdür: uygulama → gateway → model sağlayıcısı, gateway çalıştırma zamanında kasadan kredi bilgileri çekmektedir. Altınlıkta dön ve tüm uygulamalar dakika içinde yüklenir. Rotasyon politikası ≤90 gün; her commit'de TruffleHog / GitGuardian / Gitleaks ile tarama. ZERO-trust: MFA, SSO, RBAC/ABAC, kısa ömürlü tokenler, cihaz duruşu. PII temizleme, PHI/PII'yi göndermeden önce gizlemek için kuruluş tanınmasını kullanır; tutarlı işaretleme (Mesh yaklaşımı) sabit yer sahiplerine hassas değerleri haritası yapar, böylece LLM kod/ ilişki semantiğini korur. Ağ çıkışı: Sadece özel VPC/VNet alt ağlarında LLM hizmetleri`api.openai.com`- Evet .`api.anthropic.com`2026 olay sürücüsü: Vercel tedarik zinciri saldırısı, tehlikeye atılan CI/CD kimlikleri ile binlerce müşteri dağıtımında çevreyi sızdırdı.

> **【中文解读】**Bu bölüm, güvenlik anahtarı denetimi ile LLM hizmetindeki anahtar yönetimi ve güvenlik denetimi hakkında bilgi verdi.


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy PII-scrubber + audit-log writer) | **语言:** Python
**Prerequisites:** Phase 17 · 19 (AI Gateways), Phase 17 · 13 (Observability) | **前置知识:** Phase 17 · 19 (AI Gateways), Phase 17 · 13 (Observability)

>  **【前置】**Önemli bir şekilde, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir sürece bir sürece bir sürece, bir sürece bir sürece, bir sürece bir sürecececececececece, bir sürececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececece
>  **【类比】**LLM 安全 = "金库管理"。集中化 vault(HashiCorp Vault/AWS Secrets Manager/Azure Key Vault) = 钱放银行;config/env/电子表格存储密钥 = 藏在床下。AI Gateway 模式 = 应用→网关→模型商,网关运行时从库取密钥;轮换 ≤90 天,所有应用自动跟上,无需重新部署──零信任:MFA+SSO+RBAC+短时──PII 脱敏:实体识别遮蔽 PHI/PII──egress 白名单只放.openai.com 等──
> ️ **【易错点】**Vercel 2026  tedarik zinciri saldırısı olayı:CI/CD 凭证被攻破→泄露数千客户环境──修复:CI/CD OIDC而非长期密钥──
**Time:** ~60 minutes | **时间:** ~60 minutes

## Öğrenme hedefleri

- Gizli yönetim için kullanılan dört anti-önemlemeyi (VCS'deki yapılandırma dosyaları, sert kodlanmış env, kalıp sayfaları, statik anahtarlar) listeleyin ve onların yerine geçirilmesini belirleyin.
  Çinçe Çevirimiçi:列举四个密钥管理反模式(VCS'deki konfigürasyon dosyaları、硬编码环境变量、电子表格共享密钥、共享服务账户)
- AI-gateway-pull-from-vault modelini 2026 üretim standardı olarak açıklayın.
  Çinçe Çevirim: Açıklama AI 网关 from Vault 拉取密钥的模式作为 2026年生产标准──
- Semantik hayatta kalmak için tutarlı bir tokenizasyonla (eşit değer → aynı yer tutma) bir PII scrubber uygulamak.
  Çinçe Çevirim:实现带一致性标记化的 PII 清洗器(相同值 -> 相同占位符) 』
- Vercel 2026 tedarik zinciri olayını ve CI/CD sertifika hijyenine dair neyi öğrettiğini söyleyin.
  Çinçe Çevirisi: 讲出 2026年 Vercel 供应链事件以及它对CI/CD 凭证卫生的教训──

## Sorunlar. Sorunlar.

> **【中文解读】**LLM サービス セキュリティの需要解決三向量:(1) 凭证管理 实习生提交 `.env`包含 API anahtarları,已在 git 历史中,轮换流程是"Slack 群发,更新 40 配置文件,重新部署所有服务8小时后只有一半服务上线";(2) PII 泄露用户提示包含"My SSN is 123-45-6789",直接发送到 OpenAI,虽然有 BAA但内部政策要求发送前脱敏;(3) 网络出口EKS 集群的 LLM Pods herhangi bir internet sunucusuna ulaşabilir, birisi DNS 通过查询到攻击者控制的域名外泄数据;;

> **【拓展：2026 年 LLM 安全事件】**2026 yılının tipik LLM güvenlik olayları şunları içerir: 1) Vercel  tedarik zinciri saldırıları zararlı CI/CD 凭证 dışı salgılamak binlerce müşteri görevlendirmesinin çevresel değişimleri; 2) 提示注入攻击通过用户输入操纵 LLM 执行意料操作; 3) 数据泄漏LLM 在响应中泄漏训练数据中的敏感信息──防御措施包括:集中式 Vault(HashiCorp Vault、AWS White Secrets Manager)、PII 脱敏(spaCy NER + Presidio)、网络出口名单、不可变审计日志──

Bir stajyer yaptırıyor.`.env`API anahtarları ile. Hemen silinir. Anahtarlar git tarihinde zaten  GitGuardian taraması yakalar, dönüşüm süreci "Timi yavaşlat, 40 yapılandırma dosyasını güncelle, tüm hizmetleri yeniden dağıt". 8 saat sonra, hizmetlerin yarısı canlı ve yarısı pencereleri dağıtmayı bekliyor.

Bu nedenle, bu uygulamaların kullanıcısı tarafından gönderilen bilgiler için, bu uygulamaların kullanıcısı tarafından gönderilen bilgiler için kullanılabilir.

Ayrı bir şekilde, EKS klüsterinizin LLM kapsülü herhangi bir internet barındırmacıya ulaşabilir.

LLM hizmetleri için güvenlik üç vektörü de ele almalıdır.

## Konsepten bir şey.

### Merkezi kas + IAM rol çekimi

> **【拓展：AI 网关密钥管理模式】**2026 yıl LLM サービス キー管理最佳实践AI 网关模式:应用→网关→模型提供商,网关在请求时从 Vault 拉取 `OPENAI_API_KEY` Vault'da sırayla anahtar değiştirdikten sonra, bir sonraki istek otomatik olarak yeni anahtar alınması  İHA yeniden dağıtımına gerek yoktur  Slack'ın yeni anahtarı olan kişi  desteklenen Vault içerir: HashiCorp Vault、 AWS Sırları Yöneticisi、 Azure Key Vault、 GCP Sır Yöneticisi。 IAM 角色认证  uygulama IAM 身份而非静态密钥认证), sırayla anahtar değiştirme stratejisi <= 90 天, anahtar yayılma sorunu ortadan kaldırılabilir 

**Vault**HashiCorp Vault, AWS Gizemleri Yöneticisi, Azure Anahtar Vault, GCP Gizemli Yöneticisi.

**IAM role**: app/gateway, statik bir anahtar değil, IAM kimliği ile doğruluğu doğruluyor. Vault, token'ın ömür boyu sırrı iade eder.

**The AI-gateway pattern**: geçit çekimleri `OPENAI_API_KEY`Arama vakti için kasadan. Kasada döndürün, bir sonraki aramak yeni anahtar alır.

### Dönüş politikası ≤ 90 gün

Tüm API anahtarları, kasanın kök belirtileri, CI/CD kimlikleri, mümkünse otomatik dönüşüm, elle dönüşüm kaydedildi ve izlendi.

### Gizli tarama

- **TruffleHog** Komitlerde regex + entropi.
- **GitGuardian** Ticari, yüksek doğruluk.
- **Gitleaks**- OSS, CI'de çalışıyor.

Her seferinde çalış, yeni bir sır keşfedildiğinde PR'yi engelle.

### Zira güvenli duruş

- Tüm hesaplarda MFA gereklidir.
- SSO'nun SAML/OIDC üzerinden gönderilmesi.
- RBAC (rol tabanlı) veya ABAC (attribut tabanlı) ince tanelerle erişmek için.
- Kısa ömürlü tokenler (saatler, günler değil).
- Cihaz duruşu  Sadece disk şifreleme ile corp cihazları.

### PII / PHI temizleme

> **【中文解读】**PII/PHI 脱敏的四步流程:(1) 实体识别(spaCy NER、Presidio、商业工具);(2) 掩码匹配的实体"SSN'im 123-45-6789" → "SSN'im [SSN_TOKEN_A3F]";(3) 一致性标记化(Mesh 方法)相同值映射到相同占位符,LLM 可以保持关系语义;(4) 可选的LLM 响应逆映射;;静态正则过器捕获基本模式,NER 捕获更多两者都使用;;

İndirme mesajı alt kısmını terk etmeden önce:

1. Birim tanınması (spaCy NER, Presidio, ticari).
2. Maske eşleşen varlıklar: `"My SSN is 123-45-6789"`→ `"My SSN is [SSN_TOKEN_A3F]"`- Evet .
3. Düzgün bir işaretleme (Mesh yaklaşımı): aynı değerleri aynı yer sahibi için haritanlar böylece LLM ilişkileri korur.
4. LLM tepkisi için seçeneği geri haritası.

Statik regex filtreleri temel desenleri yakalar, NER daha fazla yakalar.

### Giriş + çıkış koruma rayları

Giriş: Bilinen jailbreaks'i engelle, yasak konuları; kullanıcı başına ücret sınırları.

Çıktı: sızmış sırlar için regex scrub (API anahtar kalıpları, reddedilme bağlamlarında e-posta kalıpları), politika ihlalleri için sınıflandırıcı.

### Ağ çıkış beyaz listesi

> **【拓展：LLM 安全纵深防御】**LLM サービスの 纵深防御策略包括:(1) 集中式 Vault + IAM 角色拉取应用/网关通过 IAM 身份认证,Vault 返回有限期令牌,轮换在Vault 中完成,所有应用自动获得新密钥;(2) AI 网关模式应用→网关→提供商,网关从Vault 拉取凭证,无需重新部署;(3) 90 天轮换策略所有API keynote、vault root token、CI/CD 凭证;•••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••

Özel bir alt ağta LLM hizmetleri:
- Beyaz listesi:`api.openai.com`- Evet .`api.anthropic.com`, vektör DB son noktaları, kasanın son noktaları.
- Diğer her şey: bırak.
- DNS'in sadece izin listesi çözücü aracılığıyla (DNS tünel çıkışından kaçının).

### Denetim günlüğü

Her LLM görüşmesinin değişmez kayıtları:
- Zaman damgası.
- Kullanıcı / kiracı.
- Hızlı haş (özellikle özel olmak için ham hızlı değil).
- Model + versiyon.
- İşaret sayılır.
- - Maliyet.
- Cevap hash.
- Herhangi bir koruma yolculuğu.

Yönetim gerekliliklerine göre tutma (SOC 2 1 yıl, HIPAA 6 yıl).

### 2026 Vercel olayı

Tedarik zinciri saldırısı: Tehlikeli CI/CD kimlikleri binlerce müşteri dağıtımında çevreyi sızdırıyor. Ders: CI/CD kimlikleri prod-e eşittir. Kasada saklayın. Sınır dar. Ateşli bir şekilde döndürün.

### Hatırlamalısın numaralar

- Dönüş politikası: ≤ 90 gün.
- Her commit'i tarayın: TruffleHog / GitGuardian / Gitleaks.
- Vercel 2026: CI/CD kredileri bozulmuş → Binlerce müşteri çevresi sızmış.
- Denetim günlüğü tutuluşu: SOC 2 = 1 yıl, HIPAA = 6 yıl.

## Çerçeveyi kullanın.
```figure
i4-vault-rotation
```

## Kullan

`code/main.py`tutarlı bir tokenleşme ile oyuncak PII temizleyicisi ve yalnızca ekleme denetim günlüğü uygulanır.

> `code/main.py`tutarlı bir tokenleşme ile oyuncak PII temizleyicisi ve yalnızca ekleme denetim günlüğü uygulanır.

> `code/main.py`tutarlı bir tokenleşme ile oyuncak PII temizleyicisi ve yalnızca ekleme denetim günlüğü uygulanır.

## İndirin . Ürünler .

Bu ders bize çok yararlı .`outputs/skill-llm-security-plan.md`Yönetim kapsamı ve mevcut durum göz önüne alındığında, kasayı göç, temizleme, çıkış, denetim kayıtlarını planlıyor.

> 本课产 出 `outputs/skill-llm-security-plan.md`Yönetim kapsamı ve mevcut durum göz önüne alındığında, kasayı göç, temizleme, çıkış, denetim kayıtlarını planlıyor.

## Egzersizler.

1. Çık .`code/main.py`Aynı SSN'ye referans eden iki mesaj gönderin.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`code/main.py` göndermek için aynı SSN'den iki alıntı göndermek için iki tane göndermek için aynı SSN'den iki tane göndermek için iki tane göndermek için aynı yer alması için iki tane göndermek için iki tane göndermek için iki tane göndermek için iki tane göndermek için iki tane göndermek için iki tane göndermek için iki tane göndermek için iki tane göndermek için iki tane göndermek için iki tane göndermek için iki tane göndermek için iki tane göndermek için iki tane göndermek için iki tane göndermek için iki tane göndermek için iki tane göndermek için iki tane göndermek için iki tane göndermek için iki tane göndermek için iki tane göndermek için iki tane göndermek için iki tane göndermek için iki tane göndermek için iki tane göndermek için bir tane göndermek için bir tane göndermek için bir tane göndermek için bir tane göndermek için.
2. OpenAI + Anthropic + Weaviate olarak adlandırılan vLLM-on-EKS dağıtımı için ağ çıkış politikasını tasarlayın.
   Çinçe Çevirisi: 部署设计网络出口策略.
3. Git tarihinde bir anahtar bulursanız doğru cevap nedir? anahtarı döndürün, tarih silin, ya da her ikisi de?
   Çinçe Çevirimiçi: You in git 歷史中發現一個密钥(2年前) ―― 正確的响应流程是什么?
4. Denetim kayıtlarınız günde 10 GB büyüyor.
   Çinçe Çevirimi: Senin Auditing日志 her gün büyüyor 10GB。 tasarım koruma seviyesi(热 30 天、温 12 月、冷 6年)。
5. Geri dönüştürülmüş tokenizasyonun (gerçek değerlerin yeniden LLM tepkisine değiştirilmesi) yer tutanları görünür tutmakla karşılaştırıldığında karmaşıklığa değer olup olmadığını tartışın.

## Anahtar Şartlar .

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

## Daha fazla okumak

- [Doppler — Advanced LLM Security](https://www.doppler.com/blog/advanced-llm-security)
- [Portkey — Manage LLM API keys with secret references](https://portkey.ai/blog/secret-references-ai-api-key-management/)
- [Datadog — LLM Guardrails Best Practices](https://www.datadoghq.com/blog/llm-guardrails-best-practices/)
- [JumpServer — Secrets Management Best Practices 2026](https://www.jumpserver.com/blog/secret-management-best-practices-2026)
- [Microsoft Presidio](https://github.com/microsoft/presidio) PII tespit ve anonimleştirme.
- [HashiCorp Vault docs](https://developer.hashicorp.com/vault/docs)
