# Các chế độ thất bại  MAST, Groupthink, Monoculture, Cascading Errors 失败模式 群体思维 MAST

> Định dạng phân loại tham chiếu cho năm 2026 là **MAST**(Cemri et al., NeurIPS 2025, arXiv:2503.13657), được lấy từ 1642 dấu vết thực hiện trên 7 MAS mã nguồn mở hiện đại cho thấy **41–86.7% failure rate**. Ba loại gốc: **Specification Problems**(41,77%)  vai trò không rõ ràng, định nghĩa nhiệm vụ không rõ ràng; **Coordination Failures**(36,94%)  sự cố liên lạc, sự mất đồng bộ trạng thái; **Verification Gaps**(21.30%)  thiếu xác nhận, không có kiểm tra chất lượng.**Groupthink**gia đình (arXiv:2508.05687) thêm: sự sụp đổ của đơn văn hóa (những mô hình cơ bản tương tự → thất bại tương quan), sự thiên vị về sự phù hợp (những đại lý tăng cường các lỗi của nhau), lý thuyết suy nghĩ thiếu sót, động cơ hỗn hợp, thất bại độ tin cậy hàng loạt. Ví dụ: bão thử lại khi một lỗi thanh toán kích hoạt các lần thử lại đơn đặt hàng, gây ra các lần thử lại hàng tồn kho, khiến dịch vụ hàng tồn kho bị áp đảo (10 lần tải trong giây  cần máy cắt mạch). Mùi độc trí nhớ: ảo giác của một nhân vật vào bộ nhớ chia sẻ, nhân vật tiếp theo xử lý nó như là sự thật; độ chính xác dần suy giảm, làm cho chẩn đoán gốc rễ đau đớn.**STRATUS**(NeurIPS 2025) báo cáo cải thiện thành công giảm nhẹ 1,5 lần thông qua các đại lý phát hiện / chẩn đoán / xác thực chuyên dụng. Bài học này xử lý các chế độ thất bại như các mục tiêu kỹ thuật hạng nhất.

> **【中文解读】**Bài viết này giới thiệu về mô hình thất bại của nhiều đại lý và nhóm suy nghĩ về các mô hình thất bại đặc biệt của nhiều đại lý.

> **【拓展：failure modes mast groupthink→具体应用】**Nhiều Agent  hệ thống đặc biệt có thất bại mô hình:(1) 群体思维(Groupthink) Agent 过度趋同,失去多样性;(2) 信息级联一个 Agent 的错误被后续 Agent 放大;(3) 死锁Agent 相互等待无法继续;(4) 活锁Agent 不断改变策略但无法接受──防范措施包括:注入异见 Agent、随机化发言顺序、设置超时──


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib) | **语言:** Python（标准库）
**Prerequisites:** Phase 16 · 13 (Shared Memory), Phase 16 · 14 (Consensus and BFT), Phase 16 · 15 (Voting and Debate Topology) | **前置知识:** Phase 16 · 13（共享内存），Phase 16 · 14（共识与 BFT），Phase 16 · 15（投票与辩论拓扑）

>  **【前置】**Học本节前请先掌握:Phase 16·13-15(共享内存/BFT/投票) ・MAST = 2026 多 Agent 失败模式的标准分类法。
>  **【类比】**MAST 失败分类 = "医院急诊分诊"──三类根因:规格问题(42%角色不清)、协调失败(37%通信失灵)、验证缺失(21%无质检)──MAST 1642 条 痕迹 显示 41-87% 失败率多 Agent 不是银弹──Groupthink 家族:单一文化崩(同基模型 全错)、群体盲从级付联错支(修失触发重试风暴,10秒 10倍负载)──重复:异见 Agent + 随机化发言顺序 + 断路器──
**Time:** ~75 minutes | **时间:** ~75 分钟

##                                                                                                                                                                                                                                                               

Các hệ thống đa đại lý thất bại trong 41-86,7% thời gian trên các nhiệm vụ thực (Cemri et al. 2025 đo này trên 7 MAS nguồn mở). Điều đó không thể gỡ lỗi bằng cách "chỉ thêm thêm thêm các đại lý. " Các thất bại có nguyên nhân cấu trúc.

> Nhiều đại lý hệ thống trong nhiệm vụ thực sự sẽ thất bại trong 41-86,7% thời gian của các nhiệm vụ thực sự. Cemri 等人 năm 2025 trong 7 个开源 MAS 上测量) ⋅This is not "Add More Agent" on the ability to be调试的.

Thực hành sản xuất năm 2026 là đối xử với các chế độ thất bại như là đầu vào thiết kế. Kiến trúc của bạn không đủ tốt cho đến khi bạn có thể chỉ ra từng loại MAST và đặt tên cho sự giảm thiểu mà bạn triển khai.

> Thực hành sản xuất năm 2026 là một mô hình thất bại trong việc xem xét các thiết kế nhập khẩu.

## Khái niệm cốt lõi

### Các loại MAST

**Specification Problems (41.77% of failures).**Nhiệm vụ của đại lý không được định nghĩa đủ chặt chẽ.

> **规范问题（41.77% 的失败）。**Nhiệm vụ của đại lý được định nghĩa không đủ chặt chẽ. Ví dụ:

- Sự mơ hồ về vai trò: hai đại lý đều nghĩ rằng họ là nhà phê bình.
  Trung văn翻译:角色模糊: Hai đại lý đều nghĩ mình là người xem xét.
- Nhiệm vụ được xác định rõ ràng: "đánh summarize this" khi người dùng muốn một góc độ cụ thể.
  Trung ngữ翻译:任务规格不足:"总结这个",但用户想要特定角度──
- Các tiêu chí thành công ngầm: đại lý không thể nói liệu nó có thành công hay không.
  Trung文翻译:成功标准隐含:Công ty không thể phán xét liệu thành công hay không.

Giảm thiểu:

> 缓解措施:

- Viết hợp đồng vai trò rõ ràng.
  Trung ngữ翻译:编写显式角色契约──每个代理的提示声明它做什么*和不做什么*──
- Trước khi bắt đầu, hãy xác định "được hoàn thành giống như X".
  Trung ngữ翻译:每个任务的验收测试――在 Agent 开始前,定义"完成的样子是 X"――
- Kiểm tra kỹ thuật trước chuyến bay: một nhân viên riêng xem xét định nghĩa nhiệm vụ trước khi vận chuyển.
  Trung ngữ翻译:预检规范检查: đơn độc đặc vụ trong phân发前审查任务定义──

**Coordination Failures (36.94%).**Truyền thông hoặc tình trạng suy giảm.

> **协调失败（36.94%）。**通信或状态故障──

Ví dụ:

> Ví dụ:

- Hai đại lý cập nhật trạng thái chia sẻ mà không đồng bộ.
  Trung ngữ翻译:两个代理 不同步地更新共享状态──
- Thông điệp bị mất giữa các đại lý (trận xếp hàng không, thời gian nghỉ).
  Trung文翻译:Agent 间消息丢失(队列故障、超时)
- State drift: Agent A nghĩ rằng nhiệm vụ đã hoàn thành; Agent B vẫn đang thực hiện.
  中文翻译:状态漂移:Công viên A 认为任务完成;Công viên B còn đang thực hiện。

Giảm thiểu:

> 缓解措施:

- Phiên bản chia sẻ trạng thái với đồng thời lạc quan.
  Trung ngữ翻译:带乐观并发的版本化共享状态──
- Sự thừa nhận rõ ràng cho các thông điệp quan trọng (được thử lại cho đến khi được bấm).
  Trung文翻译:关键消息的显式确认 (重试直到确认)
- Các điểm kiểm soát đồng bộ định kỳ; phát hiện sự lở hở sớm.
  Trung文翻译:定期状态同步检查点;早期检测漂移。

**Verification Gaps (21.30%).**Không kiểm tra độc lập về các kết quả.

> **验证缺口（21.30%）。**Không có kiểm tra độc lập về sản xuất.

Ví dụ:

> Ví dụ:

- Một nhân viên tuyên bố thành công; không ai xác minh.
  Trung文翻译:一个代理声称成功;没人验证──
- Dòng đại lý đều tin vào sự ra đi của tiền nhiệm.
  Trung ngữ翻译:Công viên 链中每个都信任前一个的输出。
- Các bài kiểm tra không có trong hành vi hợp tác mới nổi.
  Trung文翻译:涌现组合行为缺少测试覆盖──

Giảm thiểu:

> 缓解措施:

- Trình kiểm tra độc lập (Học 13). Chỉ đọc, truy cập nguồn độc lập.
  Trung文翻译:独立验证 Agent (第13 课) ∼只读,独立源访问──
- Hợp đồng giao dịch rõ ràng: "Sản lượng của A phải vượt qua kiểm tra C trước khi B bắt đầu".
  Trung ngữ翻译:显式交接契约:"A của输出 phải được B bắt đầu trước qua kiểm tra C".""
- Lập nhật kết quả cho phân tích hậu hoc.
  Trung ngữ翻译:结果日志用于事后分析。

### Gia đình tư duy nhóm (arXiv:2508.05687)

Năm thất bại liên quan khi các chất homogenize hoặc bắt chước nhau:

**Monoculture collapse.**Một mô hình cơ bản hoặc dữ liệu đào tạo tương quan. khi ba đại lý chia sẻ một LLM, họ chia sẻ ảo giác của nó.

**Conformity bias.**Các đại lý thích nghi với người đồng nghiệp lớn tiếng nhất hoặc tự tin nhất, ngay cả khi sai.

**Deficient ToM.**Các đại lý không thể mô hình hóa niềm tin của nhau; sự phối hợp bị phá vỡ (Dạy học 18).

**Mixed-motive dynamics.**Các đại lý có những động lực tương thích một phần sẽ hướng về trung tâm thỏa hiệp, điều này không thỏa mãn ai.

**Cascading reliability failures.**Mô hình lỗi của một thành phần kích hoạt mô hình lỗi trong các thành phần phụ thuộc.

### Ví dụ:  cơn bão tái thử

Một mô hình tai nạn cổ điển năm 2026:

```
payment service fails 10% of requests
   ↓
order agent retries payment (exponential backoff but naive)
   ↓
each retry is a new order-inventory check
   ↓
inventory service sees 2x normal load
   ↓
inventory service starts timing out
   ↓
every order retries inventory check
   ↓
inventory service sees 10x normal load
   ↓
cluster goes down
```

Phong cách là cổ điển:**circuit breakers**Khi tỷ lệ lỗi dòng chảy sau vượt quá ngưỡng, mạch ngắn với kết quả được lưu trữ trong cache hoặc mặc định.

Các bộ cắt mạch là một trong số ít các biện pháp giảm lỗi đa tác nhân mà bạn vay trực tiếp từ các hệ thống phân tán mà không cần sửa đổi.

### Mùi độc trí nhớ (được xem xét lại)

Từ Bài học 13: ảo giác của một nhân viên trở thành thực tế ký ức chung; các nhân viên dòng chảy sau suy luận về thực tế độc.

Sự suy giảm độ chính xác dần dần là triệu chứng: bạn không bị tai nạn; bạn bị lôi kéo chậm mà khó để bắt nguồn.

Giảm thiểu: chỉ có bản ghi, nguồn gốc, xác minh không thể viết.

### STRATUS  Các chất đặc biệt cho việc phát hiện lỗi

STRATUS (NeurIPS 2025) báo cáo cải thiện hiệu quả giảm nhẹ 1,5 lần khi bạn triển khai:

- **Detection agent.**Đồng hồ cho các mô hình triệu chứng (sự bất đồng cao, thử lại, độ phân trần chính xác).
- **Diagnosis agent.**Với các triệu chứng, suy luận nguyên nhân gốc có thể từ phân loại MAST.
- **Validation agent.**Sau khi áp dụng thuốc giảm bớt, kiểm tra các triệu chứng rõ ràng.

Đây là phản ứng tai nạn kiểu SRE, được áp dụng cho các hệ thống đại lý. Ba vai trò đều có thể là đại lý LLM với các lời nhắc chuyên môn.

### Việc kiểm toán trong chế độ thất bại

Một thực tiễn tốt nhất năm 2026 là một kiểm toán về chế độ thất bại hàng năm (hoặc mỗi bản phát hành lớn):

1. **Trace sample.**Thu thập khoảng 1000 dấu vết thực hành.
2. **Categorize.**Đối với các lỗi của mỗi dấu vết, hãy lập bản đồ đến các danh mục MAST + Groupthink.
3. **Compute failure-by-category rate.**Những loại nào thống trị hệ thống của bạn?
4. **Rank mitigations.**Phong cách nào sẽ loại bỏ nhiều thất bại nhất?
5. **Pick 2-3 mitigations.**Thực hiện; kiểm toán lại quý tới.

Sự kỷ luật quan trọng hơn những lựa chọn cụ thể.

### Khi hệ thống thất bại lặng lẽ

Loại lỗi nguy hiểm nhất là lỗi chính xác im lặng. Một hệ thống thất bại lớn (sự cố, ngoại lệ, cảnh báo) có thể được giám sát. Một hệ thống tạo ra các kết quả có thể chấp nhận được nhưng không đúng không thể được phát hiện bằng nhật ký ngoại lệ. Đây là lý do tại sao lỗ hổng xác minh là loại lỗi đắt nhất mặc dù chỉ là 21,30% theo số.

Đầu tư vào:
- Phân tích con người dựa trên mẫu.
- Các xét nghiệm hồi quy của bộ dữ liệu vàng.
- Các nhân viên liên quan kiểm tra các kết quả quan trọng.

### Thất bại so với thất bại chậm

Một số thất bại là ngay lập tức; một số là chậm. Các thất bại ngay lập tức (sự mất thời gian, không phù hợp với schema, lỗi tác giả) là rẻ để phát hiện.

Động thái kỹ thuật năm 2026: các trình thay thế thất bại chậm của công cụ để bạn có thể bắt kịp khi nó trở thành một lỗi hiển thị. Tốc độ thỏa thuận, tốc độ thử lại, phân phối chiều dài đầu ra và khoảng cách chỉnh sửa giữa các phiên bản đại lý liên tiếp đều là các trình thay thế hữu ích.

## Hãy xây dựng nó.
```figure
a5-retry-cascade
```

## Hãy xây dựng nó

`code/main.py`thực hiện:

- `FailureTaxonomy` phân loại các sự cố mô phỏng thành các loại MAST + Groupthink.
- `CircuitBreaker` mô hình cổ điển; mở khi tỷ lệ lỗi vượt quá ngưỡng.
- `RetryStormSimulator` cho thấy sự cố hàng loạt; bật / tắt bộ cắt mạch.
- `DetectionAgent` Scripts STRATUS kiểu phù hợp triệu chứng.

Đi chạy:

```
python3 code/main.py
```

Tạo sản lượng dự kiến:
- thử lại bão không có bộ cắt mạch: lỗi hàng tồn kho nổ (được mô phỏng).
- Với bộ cắt mạch: nắp ở ngưỡng; phản ứng chế độ suy giảm được phục vụ.
- Máy phát hiện đánh dấu mô hình và đặt tên cho danh mục MAST.

## Sử dụng nó.

`outputs/skill-mast-auditor.md`thực hiện một kiểm toán chế độ thất bại theo kiểu MAST trên một hệ thống đa đại lý.

## Đưa nó lên mạng

Phân tích chế độ thất bại trong sản xuất:

- **MAST audit per quarter.**Không phải là hàng năm, các loại thay đổi khi hệ thống của bạn phát triển.
  Trung ngữ翻译:**每季度 MAST 审计。**Không phải là hàng năm.
- **Circuit breakers everywhere.**Mỗi cuộc gọi ra ngoài đến bất kỳ dịch vụ phụ thuộc nào.
  Trung ngữ翻译:**到处都是熔断器。**Mỗi nhà hàng phụ thuộc dịch vụ được sử dụng                                                                                                                                                                                                                                                          
- **Golden datasets.**Kiểu, chất lượng cao, kiểm tra tay, kiểm tra hồi phục với chúng hàng tuần.
  Trung ngữ翻译:**黄金数据集。**Kiểu, chất lượng cao, kiểm tra nhân tạo, mỗi tuần kiểm tra trở lại.
- **STRATUS trio.**Các chất phát hiện + Chẩn đoán + Thiết lập kiểm tra sản xuất. Bắt đầu với chất phát hiện chỉ; thêm chẩn đoán khi các triệu chứng ồn ào.
  Trung ngữ翻译:**STRATUS 三重奏。**检测 + 诊断 + 验证代理 监控生产――从检测代理 开始;当症状杂时添加诊断――
- **Failure budget.**SLO rõ ràng cho tỷ lệ thất bại theo hạng mục.
  Trung ngữ翻译:**失败预算。**按类别失败率显然SLO──超出预算触发停止发言──

## Tập luyện bài tập

1. Đi chạy`code/main.py`- Đảm bảo máy cắt mạch đóng cửa cơn bão, thay đổi ngưỡng thất bại và quan sát sự đổi giá.
2. Thực hiện một**slow-failure proxy**: tỷ lệ đồng thuận trên 3 đại lý song song. Khi nó giảm mạnh, kích hoạt một cảnh báo. Chơi mô phỏng một trôi động monoculture bằng cách liên kết dần các sản lượng đại lý.
3. Xem Cemri et al. (arXiv:2503.13657). Chọn một trong 7 hệ thống MAS của họ và lập bản đồ 3 loại thất bại hàng đầu của nó.
4. Đọc bài báo Groupthink (arXiv:2508.05687). xác định ra mô hình nào trong năm mô hình khó phát hiện nhất trong sản xuất.
5. Thiết kế một bộ ba phát hiện-hình dung-tính xác định kiểu STRATUS cho một hệ thống đa tác nhân cụ thể mà bạn biết. Các triệu chứng nào mà phát hiện theo dõi?

## Từ khóa  Keyword

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| MAST / MAST 分类法 | "The 2026 taxonomy" / "2026 年分类法" | Cemri 2025; 3 root categories + 14 sub-types of failures. / Cemri 2025；3 个根类别 + 14 个失败子类型。 |
| Specification Problem / 规范问题 | "Role ambiguity" / "角色模糊" | Task or role under-defined; agents do not know what to do. / 任务或角色定义不足；Agent 不知道做什么。 |
| Coordination Failure / 协调失败 | "State drift" / "状态漂移" | Communication or sync breakdown between agents. / Agent 之间的通信或同步故障。 |
| Verification Gap / 验证缺口 | "No one checked" / "没人检查" | Outputs accepted without independent validation. / 输出未经独立验证即接受。 |
| Groupthink family / 群体思维族 | "Homogeneity failures" / "同质性失败" | Monoculture, conformity, deficient ToM, mixed-motive, cascading. / 单一文化、从众、ToM 不足、混合动机、级联。 |
| Monoculture collapse / 单一文化崩溃 | "Same model, same hallucinations" / "相同模型，相同幻觉" | Correlated errors from shared base model or training data. / 共享基础模型或训练数据的相关错误。 |
| Retry storm / 重试风暴 | "Cascading error amplification" / "级联错误放大" | One failure triggers retries which amplify load downstream. / 一次失败触发重试，放大下游负载。 |
| Circuit breaker / 熔断器 | "Fail fast on error rate" / "错误率快速失败" | Open when error rate exceeds threshold; short-circuit with default. / 错误率超阈值时断开；用默认值短路。 |
| STRATUS | "Incident response trio" / "事件响应三重奏" | Detection + diagnosis + validation agents. 1.5x mitigation success. / 检测 + 诊断 + 验证 Agent。1.5 倍缓解成功。 |
| Memory poisoning / 记忆投毒 | "Hallucinations propagate" / "幻觉传播" | Shared-memory fact tainted; downstream agents reason on poison. / 共享记忆事实被污染；下游 Agent 在毒化数据上推理。 |

## Xem thêm 延伸阅读

- [Cemri et al. — Why Do Multi-Agent LLM Systems Fail?](https://arxiv.org/abs/2503.13657) Định dạng phân loại MAST, NeurIPS 2025
- [Groupthink failures in multi-agent LLMs](https://arxiv.org/abs/2508.05687) Monoculture, conformity, và phân loại năm gia đình
- [STRATUS — specialized agents for MAS incident response](https://neurips.cc/) Việc đăng nhập thủ tục NeurIPS 2025 (phát hiện + chẩn đoán + xác nhận)
- [Release It! — stability patterns (Nygard)](https://pragprog.com/titles/mnee2/release-it-second-edition/) tham chiếu mạch cắt đường truyền
- [Anthropic — Multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) ghi chú về chế độ thất bại sản xuất
