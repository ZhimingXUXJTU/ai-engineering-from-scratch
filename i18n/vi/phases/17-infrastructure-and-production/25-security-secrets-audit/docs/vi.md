# An ninh  Bí mật, API Key Rotation, sổ kiểm toán, Guardrails  an toàn  khóa kiểm toán

> Phục tiêu sự mở rộng bí mật thông qua kho trung tâm (HashiCorp Vault, AWS Secrets Manager, Azure Key Vault). Đừng bao giờ lưu trữ thông tin vào các tập tin cấu hình, tập tin env trong VCS, bảng tính. Sử dụng vai trò IAM thay vì khóa tĩnh; OIDC cho CI / CD. Mô hình AI-gateway là giải pháp 2026: ứng dụng → cửa hàng → nhà cung cấp mô hình, với cửa hàng kéo các thông tin tín dụng từ kho trong thời gian chạy. Chuyển vào kho và tất cả các ứng dụng sẽ nhận được trong vài phút không có redeploys, không Slack "người có chìa khóa mới" tin nhắn. Chính sách quay ≤ 90 ngày; quét với TruffleHog / GitGuardian / Gitleaks trên mỗi commit. Zero-trust: MFA, SSO, RBAC/ABAC, token ngắn hạn, tư thế thiết bị. Việc xóa PII sử dụng nhận dạng thực thể để che giấu PHI/PII trước khi chuyển tiếp; token hóa nhất quán (chương trình Mesh) lập bản đồ các giá trị nhạy cảm cho người nắm giữ vị trí ổn định để LLM duy trì ngữ nghĩa mã / mối quan hệ. Tác dụng của mạng: Dịch vụ LLM chỉ trong danh sách trắng của các mạng phụ VPC/VNet`api.openai.com`- `api.anthropic.com`Các vụ tấn công chuỗi cung ứng Vercel thông qua các thông tin tín dụng CI / CD bị xâm phạm đã xâm nhập vào môi trường trên hàng ngàn triển khai khách hàng.

> **【中文解读】**Bài viết này giới thiệu về kiểm toán mật khẩu an ninh LLM  dịch vụ quản lý và kiểm toán mật khẩu an ninh 


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy PII-scrubber + audit-log writer) | **语言:** Python
**Prerequisites:** Phase 17 · 19 (AI Gateways), Phase 17 · 13 (Observability) | **前置知识:** Phase 17 · 19 (AI Gateways), Phase 17 · 13 (Observability)

>  **【前置】**学本节前请先掌握:Phase 17·19(AI Gateway) 、Phase 17·13(可观测性) 、零信任架构基础──安全核心:消除密钥散落+集中化保管──
>  **【类比】**LLM 安全 = "金库管理"。集中化 vault(HashiCorp Vault/AWS Secrets Manager/Azure Key Vault) = 钱放银行;config/env/电子表格存储密钥 = 藏在床下。AI Gateway 模式 = 应用→网关→模型商,网关运行时从库取密钥;轮换 ≤90 天, tất cả các ứng dụng tự động theo dõi, không cần tái triển khai.
> ️ **【易错点】**Vercel 2026  chuỗi cung ứng tấn công trường hợp:CI/CD 凭证被攻破→泄露数千客户环境──修复:CI/CD dùng OIDC 而非长期密钥──
**Time:** ~60 minutes | **时间:** ~60 minutes

## Mục tiêu học tập

- Đặt danh sách bốn mẫu chống quản lý bí mật (tệp cấu hình trong VCS, env mã hóa cứng, bảng tính, khóa tĩnh) và đặt tên các thay thế của chúng.
  Trung ngữ翻译:列举四个密钥管理反模式(VCS trong các tệp định cấu hình、硬编码环境变量、电子表格共享密钥、共享服务账户) ⋅
- Giải thích mô hình AI-gateway-pulls-from-vault như tiêu chuẩn sản xuất năm 2026.
  Trung文翻译:解释 AI 网关从 Vault 拉取密钥的模式作为2026年生产标准──
- Thực hiện một máy lọc PII với token hóa nhất quán ( cùng giá trị → cùng vị trí) để ngữ nghĩa tồn tại.
  Trung文翻译:实现带一致性标记化的 PII 清洗器(相同值 -> 相同占位符) 』
- Hãy nêu tên sự cố chuỗi cung ứng Vercel năm 2026 và những gì nó dạy về vệ sinh chứng chỉ CI/CD.
  Trung ngữ翻译:说出 2026 年 Vercel 供应链事件以及它对CI/CD 凭证卫生的教训──

## Vấn đề  vấn đề giới thiệu

> **【中文解读】**LLM 服务的安全需要解决三个向量:(1) 凭证管理实习生提交 `.env`包含 API keys, đã trong git 历史中,轮换流程是"Slack 群发,更新 40 配置文件,重新部署 tất cả các dịch vụ8 小时后只有一半服务上线";(2) PII 泄露用户提示包含"SSN của tôi là 123-45-6789", trực tiếp gửi đến OpenAI, mặc dù có BAA nhưng trong nội bộ chính sách yêu cầu gửi trước 脱敏;(3) 网络出口EKS 集群的LLM Pod có thể truy cập bất kỳ chủ sở hữu Internet, người dùng qua DNS 查询 đến tên miền bên ngoài của tên miền bị tấn công kiểm soát dữ liệu;.

> **【拓展：2026 年 LLM 安全事件】**Các sự kiện an toàn LLM điển hình năm 2026 bao gồm: 1) Vercel  chuỗi cung ứng tấn công  bị tổn thương CI / CD 凭证外泄漏数千客户部署的环境变量; 2) 提示注入攻击通过用户输入操纵 LLM 执行不预期操作; 3) 数据泄漏LLM 在响应中泄漏训练数据中的敏感信息──防御措施包括:集中式 Vault(HashiCorp Vault、AWS White Secrets Manager)  PII 脱敏•Spa NER + Presidio) 网络出口名单单、不可变审计日志──

Một người thực tập bắt đầu`.env`với các khóa API. Họ xóa nó nhanh chóng. Các khóa đã trong lịch sử git  GitGuardian scan bắt nó, quá trình quay của bạn là "Tạm dịch đội ngũ, cập nhật 40 tập tin cấu hình, triển khai lại tất cả các dịch vụ". 8 giờ sau, một nửa dịch vụ của bạn đang hoạt động và một nửa đang chờ đợi để triển khai cửa sổ.

Các thông tin liên quan đến người dùng bao gồm "SSN của tôi là 123-45-6789." Thông tin liên quan đến OpenAI. Bạn có một BAA nhưng chính sách nội bộ của bạn là che giấu PII trước khi chuyển tiếp.

Một cách riêng biệt, các chương trình của nhóm EKS của bạn có thể tiếp cận bất kỳ máy chủ internet nào. ai đó lưu trữ dữ liệu qua DNS tìm kiếm đến một miền được kiểm soát bởi kẻ tấn công. Không gì chặn nó.

Bảo mật cho các dịch vụ LLM phải giải quyết tất cả ba phương tiện: chứng chỉ được hỗ trợ bởi kho tàng, xóa thông tin cá nhân, lọc các nguồn thoát mạng, nhật ký kiểm toán.

## Khái niệm cốt lõi

### Hộp treo tập trung + kéo vai trò IAM

> **【拓展：AI 网关密钥管理模式】**2026 năm LLM  dịch vụ  khóa quản lý thực hành tốt nhất AI 网关模式:应用→网关→模型提供商,网关在请求时从 Vault 拉取 `OPENAI_API_KEY` Sau khi chuyển khóa trong khoang, lần sau yêu cầu tự động nhận được khóa mới 无需重新部署 无需 Slack"谁有新密钥"消息──支持的 Vault 包括:HashiCorp Vault、AWS Secrets Manager、Azure Key Vault、GCP Secret Manager──配合 IAM 角色认证(应用通过IAM 身份而非静态密钥认证), chuyển khóa chiến lược <= 90 天,可消除密钥散布问题──

**Vault**HashiCorp Vault, AWS Secret Manager, Azure Key Vault, GCP Secret Manager. Một nguồn tin.

**IAM role**: app/gateway xác thực thông qua danh tính IAM của nó, không phải là một khóa tĩnh. Vault trả lại bí mật cho thời gian tồn tại của token.

**The AI-gateway pattern**: Gateway kéo `OPENAI_API_KEY`từ kho kho vào thời điểm yêu cầu. quay trong kho, yêu cầu tiếp theo nhận được chìa khóa mới. Không triển khai lại.

### Chính sách quay ≤ 90 ngày

Tất cả các khóa API, mã nguồn kho, tín chỉ CI/CD, quay tự động khi có thể, quay bằng tay được ghi lại và theo dõi.

### Hình ảnh bí mật

- **TruffleHog** regex + entropy trên commit.
- **GitGuardian** thương mại, độ chính xác cao.
- **Gitleaks** OSS, chạy trong CI.

Đi vào mọi cuộc giao tiếp, chặn PR nếu được phát hiện bí mật mới.

### Tương vị không tin cậy

- MFA cần thiết trên tất cả các tài khoản.
- SSO thông qua SAML/OIDC.
- RBAC (tương tự vai trò) hoặc ABAC (tương tự thuộc tính) cho truy cập hạt mỏng.
- Các token ngắn hạn (giờ, không ngày).
- Tương vị thiết bị  chỉ thiết bị corp có mã hóa đĩa.

### Trải sạch PII / PHI

> **【中文解读】**PII/PHI 脱敏的四步流程:(1) 实体识别(spaCy NER、Presidio、商业工具);(2) 掩码匹配的实体"SSN của tôi là 123-45-6789" → "SSN của tôi là [SSN_TOKEN_A3F]";(3) 一致性标记化(Mesh 方法)相同值映射到相同占位符,LLM可以保持关系语义;(4) 可选的LLM 响应逆映射;;静态正则过器捕获基本模式,NER 捕获更多两者都使用;;

Trước khi báo động rời khỏi bộ phận của bạn:

1. Công nhận thực thể (spaCy NER, Presidio, thương mại).
2. Các thực thể phù hợp với mặt nạ: `"My SSN is 123-45-6789"`→ `"My SSN is [SSN_TOKEN_A3F]"`- Tôi không biết.
3. Đánh dấu nhất quán (chương pháp Mesh): bản đồ giá trị tương tự cho cùng một người giữ vị trí để LLM duy trì mối quan hệ.
4. Phân tích ngược tùy chọn cho phản ứng LLM.

Bộ lọc regex tĩnh bắt được các mẫu cơ bản, NER bắt được nhiều hơn.

### Các cửa ngắm đầu vào + đầu ra

Nhập: chặn các jailbreak được biết đến, các chủ đề bị cấm; giới hạn tỷ lệ cho mỗi người dùng.

Kết quả: Regex scrub cho bí mật bị rò rỉ (mô hình khóa API, mô hình email trong bối cảnh từ chối), phân loại cho vi phạm chính sách.

### Danh sách trắng xuất mạng

> **【拓展：LLM 安全纵深防御】**Các chiến lược phòng thủ sâu của LLM  dịch vụ bao gồm: 1) tập trung Vault + IAM 角色拉取应用/网关通过 IAM 身份认证,Vault 返回有限期令牌,轮换在 Vault完成, tất cả các ứng dụng tự động nhận được khóa mới; 2) AI 网关模式应用→网关→提供商,网关从 Vault 拉取凭证,无需重新部署; 3) 90 天轮换策略所有 API key 关键 关键 基代币、CI/CD 凭证; 4) Mỗi lần gửi scan TruffleHog / GitGuardian / Gitleaks trong CI ngăn chặn các khóa mới PR; 5) không thể thay đổi lịch sử của LLM 调控时间用户应应/租,哈希模型+SOSO 版本成本、响应、响应,  关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 关键 

Dịch vụ LLM trong một mạng phụ chuyên dụng:
- Danh sách trắng: `api.openai.com`- `api.anthropic.com`, điểm cuối DB vector, điểm cuối kho.
- Mọi thứ khác: thả.
- DNS thông qua giải quyết chỉ cho phép (đánh tránh DNS-tunneling exfil).

### Lập nhật kiểm toán

Lập nhật ký không thể thay đổi của mỗi cuộc gọi LLM với:
- Tiêu khắc thời gian.
- Người dùng / thuê nhà.
- Hash nhanh (không là yêu cầu nguyên liệu cho quyền riêng tư).
- Mô hình + phiên bản.
- Đồ tín hiệu đếm.
- Chi phí.
- Hắc-si đáp ứng.
- Bất cứ chuyến đi nào.

Giữ theo yêu cầu quy định (SOC 2 1 năm, HIPAA 6 năm).

### Vụ tai nạn Vercel năm 2026

Cuộc tấn công chuỗi cung ứng: các thông tin tín dụng CI/CD bị xâm phạm được phân tích trong môi trường qua hàng ngàn triển khai khách hàng. Bài học: các thông tin tín dụng CI/CD tương đương với prod. Cung cấp trong kho. phạm vi hẹp. Chuyển xung tích.

### Những con số mà bạn nên nhớ

- Chính sách quay: ≤ 90 ngày.
- Hình ảnh trên mỗi commit: TruffleHog / GitGuardian / Gitleaks.
- Vercel 2026: tín dụng CI/CD bị xâm phạm → hàng ngàn môi trường khách hàng bị rò rỉ.
- Việc lưu giữ nhật ký kiểm toán: SOC 2 = 1 năm, HIPAA = 6 năm.

## Hãy sử dụng nó để thực hiện
```figure
i4-vault-rotation
```

## Sử dụng nó

`code/main.py`thực hiện một máy lọc thông tin PII đồ chơi với các mã thông báo nhất quán và một nhật ký kiểm toán chỉ phụ lục.

> `code/main.py`thực hiện một máy lọc thông tin PII đồ chơi với các mã thông báo nhất quán và một nhật ký kiểm toán chỉ phụ lục.

> `code/main.py`thực hiện một máy lọc thông tin PII đồ chơi với các mã thông báo nhất quán và một nhật ký kiểm toán chỉ phụ lục.

## Chuyển nó đi.

Bài học này sẽ mang lại kết quả `outputs/skill-llm-security-plan.md`Với phạm vi quy định và tình trạng hiện tại, kế hoạch di chuyển kho, scrubber, thoát, sổ kiểm toán.

> 本课产 出 `outputs/skill-llm-security-plan.md`Với phạm vi quy định và tình trạng hiện tại, kế hoạch di chuyển kho, scrubber, thoát, sổ kiểm toán.

## Tập luyện bài tập

1. Đi chạy`code/main.py`- Đưa hai lời nhắc về cùng một SSN.
   Trung ngữ翻译:运行 `code/main.py` gửi hai trích dẫn của SSN  xác nhận hai nhận được vị trí chiếm cùng 
2. Thiết kế chính sách thoát mạng cho việc triển khai vLLM-on-EKS gọi OpenAI + Anthropic + Weaviate.
   Trung文翻译:为调用 OpenAI 和 Anthropic 的 vLLM-on-EKS 部署设计网络出口策略──
3. Bạn phát hiện ra một khóa trong lịch sử git (2 năm tuổi). Câu trả lời chính xác là gì  xoay khóa, xóa lịch sử, hoặc cả hai?
   Trung ngữ翻译:你在 git 历史中发现一个密钥(2年前) ―― 正确响应流程是什么?
4. Quý liệu kiểm toán của bạn tăng lên 10 GB/ngày.
   Trung ngữ翻译:你的审计日志每天增长10GB──设计保留层级(热 30 天、温 12 月、冷 6年)──
5. Vấn đề xem việc đảo ngược token hóa (đổi lại các giá trị thực trở lại vào phản ứng LLM) có đáng sự phức tạp so với việc giữ các người nắm giữ vị trí hiển thị không.

## Từ khóa  Từ khóa nhanh chóng

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

## Xem thêm 延伸阅读

- [Doppler — Advanced LLM Security](https://www.doppler.com/blog/advanced-llm-security)
- [Portkey — Manage LLM API keys with secret references](https://portkey.ai/blog/secret-references-ai-api-key-management/)
- [Datadog — LLM Guardrails Best Practices](https://www.datadoghq.com/blog/llm-guardrails-best-practices/)
- [JumpServer — Secrets Management Best Practices 2026](https://www.jumpserver.com/blog/secret-management-best-practices-2026)
- [Microsoft Presidio](https://github.com/microsoft/presidio) Khám phá và ẩn danh thông tin thông tin cá nhân.
- [HashiCorp Vault docs](https://developer.hashicorp.com/vault/docs)
