# Thiết kế tự cải thiện giới hạn

> Nghiên cứu đã hội tụ về bốn nguyên thủy để giới hạn vòng tự cải thiện. Các biến số chính thức phải được giữ qua mọi chỉnh sửa. Các neo sắp xếp không thể thay đổi. Các hạn chế đa mục tiêu mà mọi chiều kích (sự an toàn, công bằng, độ bền) phải có, không chỉ hiệu suất. Khám phá sự lùi lại làm dừng vòng lặp khi các số liệu lịch sử cho thấy mất khả năng. Không một trong số đó là bằng chứng về an toàn  kết quả lý thuyết thông tin (độ phức tạp Kolmogorov, định lý Lob) ràng buộc những gì bất kỳ hệ thống nào có thể chứng minh về những người kế nhiệm của nó. Chúng là những biện pháp giảm thiểu làm tăng chi phí thất bại im lặng.

> **【中文解读】**Nghiên cứu đã nhận được bốn ràng buộc tự cải tiến vòng lặp nguyên ngữ. Mỗi lần chỉnh sửa phải được thành lập hình thức không thay đổi. Không thể thay đổi đối với các điểm. Mỗi chiều kích (trang tính) an toàn, công bằng, và không chỉ có hiệu suất. Khi các chỉ số lịch sử cho thấy mất năng lực, chúng không phải là kết quả của chứng minh an toàn.

> **【拓展：四个原语 → 一个守门栈】**Trong thực tế, mỗi lần tự sửa đổi phải được thực hiện theo: không biến số kiểm tra:模块哈希、工具权限清单、宪法头)→ 对齐点检查:目标陈述匹配批准版)→ 多目标评估:性能安全、公平、鲁棒)→ 回归检测:无轴下降超值:─任一失败暂停循环:

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, bounded-loop with invariant check) | **语言:** Python（标准库，带不变量检查的有界循环）
**Prerequisites:** Phase 15 · 07 (RSI), Phase 15 · 04 (DGM) | **前置知识:** Phase 15 · 07（RSI），Phase 15 · 04（DGM）
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**学本节前请先掌握:Phase 15·07(RSI 风险) 、Phase 15·04(DGM 自修) 、Phase 15·14(kill-switches) 、形式化方法概念(不变量、定理证明) ⋅RSI bị ràng buộc = 把RSI 装进子。
>  **【类比】**RSI bị ràng buộc = "AI tự tôi cải tiến护"。四个原语 = 四道门:(1) 不变量检查(哈希签名,不能改变);(2) 对齐点(价值观不能改变);(3) 多目标评估(性能但安全不能掉);(4) 回归检测(任何轴下降就停)。 Mỗi lần tự sửa đổi phải được bốn道门全过──但理论上:Lob 定理 + Kolmogorov 复杂性 = 系统永远无法完全证明自己的后继者 这些只是缓解,不是保证──
> 🤔 **【困惑】**Q: 既然不能保证安全,为什么还要研究? Vì" nâng cao chi phí thất bại" cũng có giá trị.  Người tấn công phải chi nhiều nguồn lực hơn để vượt qua bốn cánh cửa.

## Vấn đề  vấn đề giới thiệu

Máy mô phỏng đua của bài học 7 cho thấy sự khác biệt tỷ lệ nhỏ kết hợp thành khoảng cách lớn. Nghiên cứu trường hợp DGM của bài học 4 cho thấy các vòng lặp có thể tích cực chơi các nhà đánh giá của riêng họ.

> Chương 7 mô phỏng đua xe hiển thị sự khác biệt tốc độ nhỏ phức hợp sự khác biệt lớn. Chương 4 ví dụ về DGM cho thấy vòng lặp có thể chủ động hóa các thiết bị đánh giá của riêng mình.

Cả hai kết quả đều chỉ ra cùng một câu hỏi kỹ thuật: bạn có thể đặt ra những hạn chế nào trên một vòng tự cải thiện để các hạn chế không thể bị làm suy yếu lặng lẽ bởi vòng tự nó?

> 2 kết quả chỉ ra vấn đề cùng một công trình: Bạn có thể áp dụng những ràng buộc gì trên vòng tự cải tiến tự, để các ràng buộc này không thể bị vòng tự bị suy yếu?

ICLR 2026 RSI Workshop summary (openreview.net/pdf?id=OsPQ6zTQXV) xác định bốn nguyên thủy như vậy. RSP v3.0 (Dạy 19) của Anthropic và FSF v3 (Dạy 20) của DeepMind đều đề cập đến chúng trong ngưỡng khả năng.

> ICLR 2026 RSI 工作坊摘要(openreview.net/pdf?id=OsPQ6zTQXV)识别四个此类原语──Anthropic 的 RSP v3.0(第 19 课) 和 DeepMind 的 FSF v3(第 20 课) 都在能力值中引用它们──Meta HyperAgents 工作和 SAHOO(2026 年 3 月) 等社区框架在生产中实现子集──

> **【中文解读】**Có giới tự cải tiến khám phá khả năng và giới hạn của AI  hệ thống cải tiến khả năng của mình trong ranh giới an ninh. Câu hỏi cốt lõi: 1) Chuyển đổi có thể xác minh được  hệ thống có thể chứng minh được phiên bản sau cải tiến bằng giá hoặc tốt hơn không? 2) Ranh giới cách xác định được  những khía cạnh nào được phép cải tiến? 3) Có sự cải tiến có được  bảo đảm  liệu cải tiến sẽ đạt được một giới hạn nào đó không?

Các kết quả lý thuyết thông tin kết nối những gì bất kỳ hệ thống nào có thể chứng minh về người kế nhiệm của nó, và không có thiết kế hiện tại nào đóng cửa vấn đề một cách chính thức.

> Các khung thực tế: những điều này là các biện pháp giảm thiểu. Kết quả nghiên cứu thông tin hạn chế nội dung của bất kỳ hệ thống nào đối với những người kế nhiệm của nó.

Một vòng lặp có giới hạn tốt là an toàn hơn một vòng lặp không giới hạn, không an toàn trong các thuật ngữ tuyệt đối.

> Một vòng lặp tốt hơn không có giới hạn là an toàn hơn, không phải là an toàn tuyệt đối.

## Khái niệm cốt lõi

### Primitive 1: các bất biến chính thức

Một tính không biến đổi là một thuộc tính phải giữ trước và sau mỗi tự sửa đổi.

> Không biến đổi là thuộc tính phải được thành lập sau mỗi lần tự sửa đổi trước.

Ví dụ:

> Ví dụ:

- Phân phối sản lượng được điều kiện theo một tiêu đề cấu trúc cố định (Học 17).
  Trung ngữ翻译:输出分布以固定宪法头为条件 (第 17 课)
- Không có cuộc gọi công cụ nào đến một điểm cuối không được phép.
  Trung ngữ翻译:没有工具调用到达未授权端点──
- Tưởng thức viết đi qua một con đường được ghi chép, ký kết.
  Trung文翻译:内存写入通过记录、签名路径。
- Hash module của người đánh giá phù hợp với phiên bản được phê duyệt.
  Trung ngữ翻译:评估器的模块哈希匹配批准版本──

Các biến thể được kiểm tra bởi mã bên ngoài vòng lặp không thể chỉnh sửa. Nếu một sửa đổi được đề xuất vi phạm một biến thể, nó sẽ bị từ chối. Điều này bắt được chế độ đánh giá-phản trị kiểu DGM (Dạy học 4).

> Không biến số bởi vòng không thể chỉnh sửa kiểm tra mã bên ngoài. Nếu đề xuất sửa đổi trái ngược không biến số, được từ chối.

Phần khó khăn là chọn các biến số cần thiết cho an toàn và tính toán trong thời gian hợp lý.

> Phần khó khăn là lựa chọn cho sự an toàn cần thiết và có thể tính toán trong thời gian hợp lý không thay đổi.

### Primitive 2: Anchor alignment 😁

Một neo sắp xếp là một sự đại diện không thay đổi của mục tiêu cốt lõi của vòng lặp, được gắn bên ngoài bề mặt chỉnh sửa của vòng lặp.

> Đối với các điểm là biểu hiện không thể thay đổi của mục tiêu trung tâm vòng, cố định bên ngoài mặt biên tập vòng.

Ví dụ:

> Ví dụ:

- Một văn bản hiến pháp (Dạy 17) được tải từ một vị trí chỉ đọc trên mỗi lời kêu gọi.
  Trung ngữ翻译:每次调用从只读位置加载的宪法文本 ((第 17 课) 〕
- Một nhà đánh giá trong một kho lưu trữ riêng với kiểm soát truy cập độc lập.
  Trung ngữ翻译: 在独立访问控制的独立仓库中的评估器.
- Một bản ghi giấy phép công cụ được ký bởi con người và được xác minh lại mỗi chu kỳ.
  Trung ngữ翻译:由人类签名每周期重新验证的工具权限清单──

Vai trò của neo là ngăn chặn sự trôi dạt khách quan.

>  điểm có tác dụng là ngăn chặn mục tiêu di chuyển.

Chế độ thất bại tinh tế: một vòng xoắn mà vòng lặp không thể chỉnh sửa vẫn có thể được giải thích lại bởi một vòng xoắn mà di chuyển theo cách nó đọc bộ xoắn. AI hiến pháp (Dạy học 17) được dựa trên lý do rõ ràng để xử lý các tình huống mới; lớp lý luận đó là nơi mà sự dẫn dắt giải thích sống.

> 微妙的失败模式: vòng lặp không thể chỉnh sửa được 点 vẫn có thể được giải thích lại trong cách đọc 点 trên vòng lặp di chuyển.

### Primitive 3: Multi-Objective constraints

Một vòng lặp tối ưu hóa một điểm số scalar duy nhất sẽ tìm ra các đường tắt.

> 优化单标量分数循环会找到捷径――必须同时满足多个硬束循环可用捷径较少――

Vốn mô hình:

> 典型轴:

- Hiệu suất (chỉ số chuẩn cấp nhiệm vụ)
  Trung ngữ翻译:性能(任务级基准)
- An toàn (bản đánh giá nhóm đỏ, tỷ lệ từ chối trên xấu được biết đến)
  Trung ngữ翻译:安全(红队评估、已知坏例的拒绝率)
- Sự công bằng (chỉ giới tác động khác nhau đối với các nhóm phụ nhạy cảm)
  Trung ngữ翻译:公平(敏感子群体上的差异影响边界)
- Độ bền (các bộ thử OOD, xử lý đầu vào đối kháng)
  Trung文翻译:鲁棒性(OOD 测试集、对抗输入处理)

Một sửa đổi chỉ được chấp nhận nếu mọi hạn chế vẫn tồn tại. Thống đốc chi phí của Bài 13 xếp lại với các hạn chế tài chính. Llama Guard của Bài 18 được kết nối với như một trục an toàn.

>  sửa đổi chỉ được chấp nhận khi tất cả các ràng buộc được thành lập.                                                                                                                                                                                                                                                       

### Primitive 4: Khám phá sự lùi lại

Điểm số của mỗi chu kỳ được so sánh với phân phối lịch sử. Một sự sụt giảm vượt qua dung lượng được cấu hình dừng vòng lặp. Điều này bắt mất khả năng im lặng mà nếu không sẽ được hấp thụ vào trung bình chạy khi vòng lặp "bắt đầu" nó.

> Phân tích phân tích của mỗi chu kỳ với phân bố lịch sử: giảm chu kỳ tạm dừng của sự dung nạp vượt quá quy trình.

Một thực tế thực hiện: lưu trữ điểm số mỗi nhiệm vụ của các chu kỳ N cuối cùng. Mỗi chu kỳ mới tính toán một delta mỗi nhiệm vụ. Nếu bất kỳ delta nào giảm xuống dưới ngưỡng, chu kỳ bị từ chối và một cuộc đánh giá của con người.

> Thực tế thực hiện: lưu trữ số lượng mỗi nhiệm vụ trong N 个周期 gần đây ⋅ mỗi chu kỳ mới tính toán mỗi nhiệm vụ tăng ⋅ Nếu bất kỳ tăng nào giảm xuống dưới  giá trị, chu kỳ sẽ bị từ chối và được kiểm tra bởi con người ⋅

### Biên giới lý thuyết thông tin 信息论极限

Sự phức tạp của Kolmogorov và định lý Lob đặt ra ranh giới trên những gì một hệ thống có thể chứng minh về bản thân. Máy Godel chính thức của Schmidhuber (Dạy học 4) nhắm đến giới hạn cao nhất như vậy; không ai đã hoàn thành một bằng chứng không tầm thường. Kết quả của Lob nói: nếu một hệ thống có thể chứng minh rằng "Tôi sẽ làm X nếu tôi chứng minh tôi nên làm X", nó sẽ làm X mà không chứng minh nó nên, một thất bại tham chiếu tự thân nổi tiếng.

> Kolmogorov 复杂性和 Lob 定理为系统能对自己证明的内容设置上限──Schmidhuber's形式 Godel Machine (第4 课) 准最高此类边界;没人完成过非凡证明──Lob 结果说: Nếu hệ thống có thể chứng minh rằng "Nếu chứng minh tôi nên làm X, tôi sẽ làm X", nó sẽ làm X và không chứng minh nên, một tự trích dẫn đã được biết đã thất bại──

Điều này có nghĩa là chúng ta không thể giải quyết được vấn đề an toàn, chúng làm cho sự thất bại im lặng trở nên tốn kém hơn, một vòng lặp độc hại hoặc bị trôi qua để tránh một kiểm tra bị mất đi, giờ đây sẽ làm suy yếu một cái rõ ràng, đó là một chữ ký dễ phát hiện hơn.

> Đối với ý nghĩa của ngôn ngữ gốc của chúng ta: chúng không thể đóng các vấn đề an ninh. Chúng làm cho sự yên tĩnh thất bại đắt tiền hơn.

### Một ví dụ đã làm việc.

Giả sử một đại lý đề xuất một chỉnh sửa.

> 假设 Agent 提议一个编辑──守门:

1. Kiểm tra không thay đổi: module hashes, biểu đồ giấy phép công cụ, tiêu đề hiến pháp.
   Trung ngữ翻译:不变量检查:模块哈希、工具权限清单、宪法头──
2. Kiểm tra neo: tuyên bố khách quan phù hợp với phiên bản được phê duyệt (từ về cácbyte hoặc ngữ nghĩa).
   Trung ngữ翻译:点检查:目标陈述匹配批准版本(字节或语义) 』
3. Đánh giá đa mục tiêu: hiệu suất, an toàn, công bằng, độ bền.
   Trung文翻译:多目标评估: hiệu suất, an toàn, công bằng, có tính chất tốt.
4. Khám phá sự lùi: không có trục giảm nhiều hơn dung nạp.
   Trung文翻译:回归检测:无轴下降超容忍度.

Tất cả bốn phải vượt qua để chỉnh sửa hạ cánh.

> Tất cả bốn phải qua biên tập để rơi xuống.

## Hãy sử dụng nó để thực hiện
```figure
bounded-gates
```

## Sử dụng nó

`code/main.py`chạy một vòng lặp tự cải thiện được giới hạn trên đồ chơi kiểu DGM từ Bài học 4, nhưng với bốn nguyên thủy được xếp lớp trên. Mỗi nguyên thủy có thể được bật hoặc vô hiệu hóa riêng biệt.

> `code/main.py`Trong lớp 4, DGM 式 đồ chơi hoạt động có vòng tự cải tiến, nhưng trên đó được lắp đặt bốn ngôn ngữ nguyên bản. Mỗi ngôn ngữ nguyên bản có thể được bật hoặc tắt độc lập.

## Chuyển nó đi.

`outputs/skill-bounded-loop-review.md`kiểm tra một vòng lặp giới hạn được đề xuất và ghi điểm nào trong bốn nguyên thủy thực sự thực hiện so với yêu cầu.

> `outputs/skill-bounded-loop-review.md`审计提议 có giới hạn vòng lặp và đánh giá nó thực sự thực hiện trong bốn ngôn ngữ gốc nào so với 声称的──

## Tập luyện bài tập

1. Đi chạy`code/main.py`xác nhận vòng lặp vẫn cải thiện trên số liệu chính mà không để hack thắng.
   中文翻译:启用所有原语运行 `code/main.py`                                                                                                                                                                                                                                                              

2. Thiết lập đầu vào khi điều này dẫn đến việc mất khả năng im lặng được chấp nhận.
   Trung ngữ翻译:禁用回归检测──构建一个导致接受静默能力损失的输入──

3. Thiết lập giới hạn đa mục tiêu. Hình bày vòng lặp hội tụ trên trục hiệu suất trong khi trục an toàn giảm.
   Trung ngữ翻译:禁用多目标约束──展示循环在性能轴收而安全轴下降──

4. Thiết kế một bộ neo sắp xếp cho một nhân viên mã hóa.
   Trung ngữ翻译:为编码代理 设计对齐点──什么文本、存储何处、如何检查?

5. Đọc bản tóm tắt của Hội thảo RSI ICLR 2026 chọn một trong bốn nguyên thủy và đề xuất một cải tiến cụ thể cho hiện tại của nghệ thuật.
   Trung ngữ翻译:阅读 ICLR 2026 RSI 工作坊摘要──选四个原语之一并提出具体改进对当前技术水平──

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| Invariant | "Always-true property" | A property checked by external code before and after every edit |
| 不变量 | "始终成立的属性" | 每次编辑前后由外部代码检查的属性 |
| Alignment anchor | "Pinned objective" | Immutable core-goal representation outside the loop's edit surface |
| 对齐锚点 | "固定的目标" | 循环编辑面之外的不可变核心目标表示 |
| Multi-objective constraint | "All axes must hold" | Performance, safety, fairness, robustness — all required |
| 多目标约束 | "所有轴必须成立" | 性能、安全、公平、鲁棒——全部要求 |
| Regression detection | "Pause on drop" | Pause the loop when historical metric deltas suggest capability loss |
| 回归检测 | "下降时暂停" | 当历史指标增量表明能力损失时暂停循环 |
| Kolmogorov bound | "Information-theoretic limit" | Limits what a system can prove about its own successor |
| Kolmogorov 边界 | "信息论极限" | 限制系统能对其后继者证明的内容 |
| Lob's theorem | "Self-reference trap" | System can act on "I should" without proving it should |
| Lob 定理 | "自引用陷阱" | 系统可在不证明应该的情况下按"我应该"行动 |
| Gate stack | "Layered check" | Multiple primitives combined; any failure rejects the edit |
| 守门栈 | "分层检查" | 多个原语组合；任一失败拒绝编辑 |
| Bounded improvement | "Mitigation, not proof" | Raises silent-failure cost; does not close the safety problem |
| 有界改进 | "缓解，非证明" | 提高静默失败成本；不闭合安全问题 |

## Xem thêm 延伸阅读

- [ICLR 2026 RSI Workshop summary (OpenReview)](https://openreview.net/pdf?id=OsPQ6zTQXV) sự hội tụ bốn nguyên thủy.
  Trung ngữ翻译:四原语收──
- [Anthropic Responsible Scaling Policy v3.0](https://anthropic.com/responsible-scaling-policy/rsp-v3-0) Các ngưỡng khả năng đa mục tiêu.
  Trung文翻译:多目标能力值──
- [DeepMind Frontier Safety Framework v3](https://deepmind.google/blog/strengthening-our-frontier-safety-framework/) giám sát sự sắp xếp lừa đảo như một nguyên thủy không thay đổi.
  Trung ngữ翻译:作为不变量原语的欺骗性对齐监控──
- [Schmidhuber (2003). Godel Machines](https://people.idsia.ch/~juergen/goedelmachine.html) tổ tiên chính thức-bằng chứng của những nguyên thủy này.
  Trung ngữ翻译:这些原语的形式证明祖先──
- [Anthropic — Claude's Constitution (January 2026)](https://www.anthropic.com/news/claudes-constitution) cơ sở lập trình dựa trên lý do.
  Trung ngữ翻译: dựa trên lý thuyết đối với các điểm 点.
