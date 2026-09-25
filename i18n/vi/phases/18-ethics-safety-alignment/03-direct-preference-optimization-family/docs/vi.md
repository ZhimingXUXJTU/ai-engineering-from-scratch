# Gia đình Optimize Preferences Direct                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      

> Rafailov et al. (2023) cho thấy tối ưu của RLHF có hình thức đóng về dữ liệu ưu tiên, vì vậy bạn có thể bỏ qua mô hình phần thưởng rõ ràng và tối ưu hóa chính sách trực tiếp. Sự hiểu biết đó đã sinh ra một gia đình  IPO, KTO, SimPO, ORPO, BPO  mỗi người sửa chữa một chế độ thất bại của DPO. Năm 2026, các thuật toán sắp xếp trực tiếp sẽ vận chuyển nhiều chuyến chạy sau đào tạo hơn PPO. Nhưng đường cong tối ưu hóa quá mức từ Bài học 2 vẫn áp dụng: DAA không thoát khỏi Goodhart, họ chỉ di chuyển đến nơi nó cắn.

> **【中文解读】**Trong phần này, tôi giới thiệu về mô hình ưu đãi trực tiếp của DPO (Refilov et al.) (Rafailov et al.) (Rafailov et al.) (Rafailov et al.) (Rafailov et al.) (Rafailov et al.) (Rafailov et al.) (Rafailov et al.) (Rafailov et al.) (Rafailov et al.) (Rafailov et al.) (Rafailov et al.) (Rafailov et al.) (Rafailov et al.) (Rafailov et al.) (Rafailov et al.) (Rafailov et al.) (Rafailov et al.) (Rafailov et al.) (Rafailov et al.) (Rafailov et al.) (Rafailov et al.) (Rafailov et al.) (Rafailov et al.) (Rafailov et al.) (Rafailov et al.) (Rafailov et al.) (Rafailov et al.) (Rafail et al.) (Rafail et al.) (Rafail et al.) (Rafail) (Rafail) (Rafail) (Rafail) (Rafail) (Rafail) (Rafail) (Rafail) (Rafail) (Rafail) (Rafail) (Rafail) (Rafail) (Rafail) (Rafail) (Rafail) (Rafail) (Rafail) (Rafail) (Rafail) (Rafail) (Rafail) (Rafail) (Rafail) (Rafail) (Rafail) (Rafail) (Rafail) (Rafail) (Rafail) (Rafail) (Rafail) (Rafail) (Rafail) (Rafail) (Rafail) (Rafail) (Rafail) (Rafail) (Rafail) (Rafail) (Rafail) (Rafail) (Rafail) (Rafail) (Rafail) (Rafail) (Rafail) (Rafail) (R

> **【拓展：DPO 家族 → 现代 AI 训练】**Năm 2026, trực tiếp đối với các thuật toán chuẩn bị (DAA) hơn PPO trong nhiều đào tạo phía trước sau triển khai. Nhưng đường cong quá ưu đãi của Bài học 2 vẫn áp dụng.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, six-variant preference-loss comparator) | **语言:** Python（标准库，六种变体偏好损失比较器）
**Prerequisites:** Phase 18 · 01 (InstructGPT), Phase 18 · 02 (Reward hacking), Phase 10 · 08 (DPO basics) | **前置知识:** Phase 18 · 01 (InstructGPT), Phase 18 · 02 (奖励黑客), Phase 10 · 08 (DPO 基础)

>  **【前置】**学本节前请先掌握:Phase 18·01-02(InstructGPT+古德哈特) 、Phase 10·08(DPO 基础) DPO 家族 = 绕过显式奖励模型直接从偏好数据训练──
>  **【类比】**DPO = " bỏ cuộc thi trọng tài "。RLHF = 训练裁判(奖励模型) + 训练选手优化裁判评分;DPO = 直接用比赛结果;;DPO = 直接用比赛结果;;偏好对) 训练选手;;家族变体 IPO/KTO/SimPO/ORPO/BPO 都在修 DPO 不同缺陷;;2026 DAA(直接对齐算法) 比 PPO 部署更多;;但古德特定法不变只是从"奖励模型过优化"挪到"参考策略比率过度优化"──
**Time:** ~75 minutes | **时间:** ~75 分钟

## Mục tiêu học tập

- Thuộc dẫn hình thức DPO đóng từ RLHF-with-KL tối ưu.
  Trung文翻译:从带 KL 的 RLHF 最优解推导 DPO 闭式解。
- Cụ thể chế độ thất bại của mỗi sửa chữa IPO, KTO, SimPO, ORPO, BPO trong DPO.
  Trung文翻译:说明 IPO、KTO、SimPO、ORPO、BPO 分别修复了 DPO's哪个失败模式──
- Hóa ra sự khác biệt giữa "sự chênh lệch phần thưởng ngầm" và "sức mạnh ưu tiên" và giải thích lý do tại sao việc lập bản đồ danh tính của IPO là quan trọng.
  Trung ngữ翻译:区分"隐式奖励差距"和"偏好强度", giải thích tại sao việc phân tích các khoản đầu tư của IPO là rất quan trọng.
- Giải thích lý do tại sao Rafailov et al. (NeurIPS 2024) chứng minh DAAs quá tối ưu hóa mặc dù không có RM rõ ràng.
  Trung ngữ翻译:解释为什么 Rafailov 等人(NeurIPS 2024) chứng minh DAA 尽管没有显式 RM 仍然会过度优化──

## Vấn đề  vấn đề giới thiệu

Mục tiêu RLHF (Lớp 1):

> RLHF 目标(Dạy 1):

```
max_pi E_{x,y~pi} [ r(x, y) ] - beta * KL(pi || pi_ref)
```

có một tối ưu được biết đến:

> Có những giải pháp tốt nhất:

```
pi*(y|x) = (1/Z(x)) * pi_ref(y|x) * exp(r(x, y) / beta)
```

Vì vậy, phần thưởng được xác định ngầm bởi tỷ lệ chính sách tối ưu với tham chiếu:

> Do đó, tỷ lệ phần thưởng được xác định bởi các chiến lược tốt nhất và các chiến lược tham khảo:

```
r(x, y) = beta * log(pi*(y|x) / pi_ref(y|x)) + beta * log Z(x)
```

Thay thế nó vào khả năng ưu tiên Bradley-Terry và chức năng phân vùng `Z(x)`hủy vì nó chỉ phụ thuộc vào `x`. Điều còn lại là một sự mất mát trong các tham số chính sách một mình không cần mô hình thưởng. Đó là DPO.

> Để chuyển thành Bradley-Terry                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       `Z(x)`Vì chỉ phụ thuộc vào`x`Và抵消── còn lại là hàm mất của các yếu tố chiến lược đơn giản không cần mô hình thưởng── đây là DPO──

Sự nếp nhăn: dẫn xuất giả định tối ưu có thể đạt được, dữ liệu ưu tiên là trong phân phối, và chính sách tham chiếu là neo chế độ thực.

> 问题在于:推导假设最优可达,偏好数据分布内,参考策略是真正点.

## Khái niệm cốt lõi

> **【中文解读】**Ưu điểm của PO:RLF  mục tiêu có được biết là ưu điểm nhất pi*((y DH khix) = (1(x)) * pi_ref(y khix) * exp((r(x,y) /beta)  sẽ được báo hiệu phần thưởng cho số lượng đối số tỷ lệ chiến lược tốt nhất và tỷ lệ tham khảo chiến lược, thay vào Bradley-Terry 偏似然, phân phối hàm Z(x) vì chỉ phụ thuộc vào x và抵消 còn lại là hàm mất mát của các tham số chiến lược, không cần mô hình thưởng.

### DPO (Rafailov et al., 2023)

```
L_DPO = -log sigmoid(
  beta * log(pi(y_w | x) / pi_ref(y_w | x))
  - beta * log(pi(y_l | x) / pi_ref(y_l | x))
)
```

Có thể sai gì?

> Có thể có vấn đề gì:

- Sự chênh lệch phần thưởng ngầm `beta * (log(pi/pi_ref)_w - log(pi/pi_ref)_l)`Một sự ưu tiên nhỏ có thể tạo ra một khoảng cách lớn tùy tiện.
  Trung文翻译:隐式奖励差距无限──微小偏好可以产生任意大的差距──
- Các ổ đĩa mất chọn và từ chối log-prob trong các hướng đối lập. nó có thể đẩy được chọn log-prob tuyệt đối xuống miễn là bị từ chối rơi nhanh hơn.
  Trung ngữ翻译:损失驱动选择和拒绝对数概率朝相反方向――只要拒绝的下降更快,它可以推低选择的绝对对数概率――这是"退化选择响应"现象――
- Tích thích ngoài phân phối (cặp hiếm hiếm so với cặp hiếm hiếm) tạo ra những phần thưởng ngầm tùy ý.
  Trung文翻译: phân tán ngoài ưu tiên tạo ra bất kỳ phần thưởng ẩn hình.

> **【拓展：IPO → DPO 的边界控制】**IPO(Tích ưu điểm danh tính Optimization) thay thế log-sigmoid bằng các bản đồ như恒等, khoảng cách ưu điểm được 1/(2*beta) 封顶.

### IPO (Azar et al., 2024)

Identity Preference Optimization thay thế log-sigmoid bằng một bản đồ danh tính trên xác suất ưu tiên.

> IPO sử dụng các loại hình hình ảnh thay thế log-sigmoid, sự khác biệt ưu điểm được 1/(2 *beta) 封顶.

```
L_IPO = (log(pi(y_w | x) / pi_ref(y_w | x)) - log(pi(y_l | x) / pi_ref(y_l | x)) - 1/(2 beta))^2
```

Lợi nhuận được giới hạn bởi `1/(2 beta)`- Tăng cường ưu tiên và khoảng cách phần thưởng ngầm là tương xứng.

> 边界被 `1/(2 beta)`封顶── ưu tiên mạnh và ẩn hình sự khác biệt phần thưởng thành chính xác── sẽ không nổ──

> **【拓展：KTO → 无配对数据训练】**KTO (Kahneman-Tversky Optimization) là một sáng tạo quan trọng là hoàn toàn từ bỏ các cấu trúc, chỉ cần một nhãn đơn lẻ để sản xuất "hiện" hoặc "không lý tưởng".

### KTO (Ethayarajh et al., 2024)

Kahneman-Tversky Optimization giảm cấu trúc đôi hoàn toàn. Với một đầu ra được dán nhãn duy nhất và một tín hiệu "thích" hoặc "không mong muốn" nhị phân, nó được lập bản đồ cho một tiện ích lý thuyết triển vọng:

> KTO hoàn toàn từ bỏ sự phối hợp với cấu trúc. cho một dấu hiệu đầu ra và tín hiệu "hiện tượng" hoặc "không lý tưởng" hai dạng, nó được mô tả cho hiệu ứng lý thuyết viễn cảnh:

```
v(x, y) = sigma(beta * log(pi(y|x) / pi_ref(y|x)) - z_ref)
```

lợi ích: bạn có thể sử dụng dữ liệu không cặp, đó là nhiều hơn nhiều.

> Đối với lợi nhuận và lỗ sử dụng khác nhau trọng lượng: bạn có thể sử dụng không đối xứng dữ liệu, nó là xa hơn so với đối xứng dữ liệu phong phú.

> **【中文解读】**SimPO  đã loại bỏ các chiến lược tham chiếu, thay thế với các đối số giống như của tính cách thống nhất độ dài, cộng với các bài tập ổn định gamma 边际. Điều này trực tiếp giải quyết được các vấn đề về sự cố định độ dài của DPO.

### SimPO (Meng et al., 2024)

Simple Preference Optimization phù hợp tín hiệu đào tạo với hệ thống.

> SimPO sẽ tập trung tín hiệu và tạo ra đối với nhau.

```
L_SimPO = -log sigmoid(
  (beta / |y_w|) * log pi(y_w | x)
  - (beta / |y_l|) * log pi(y_l | x)
  - gamma
)
```

với một biên giới`gamma`Việc bình thường hóa chiều dài loại bỏ động lực để khai thác chế độ thất bại về chiều dài của DPO (longer `y_w`cho một khoảng cách lớn hơn log-prob theo xây dựng).

> Lên bên cạnh`gamma`稳定训练―― 长度归结消除了利用 DPO 长度偏见失败模式的激励`y_w`构造性地产生较大的对数概率差距)

### ORPO (Hong et al., 2024)

Optimization Preference Ratio Optimization thêm một thuật ngữ ưu tiên cho SFT tiêu chuẩn khả năng log âm:

> ORPO sẽ tăng các ưu tiên lên tiêu chuẩn SFT 负 đối với số lượng giống như:

```
L_ORPO = L_NLL(y_w) + lambda * L_OR
L_OR = -log sigmoid(log(odds(y_w) / odds(y_l)))
```

Không có chính sách tham chiếu  thuật ngữ SFT là điều chỉnh. Đường bộ trong một giai đoạn từ mô hình cơ sở đến mô hình được sắp xếp. Không có điểm kiểm soát SFT riêng biệt.

> 无参考策略SFT 项就是正则化器──单阶段从基础模型训练到对齐模型──无需单独的SFT 检查点──

### BPO (ICLR 2026 đệ trình, OpenReview id=b97EwMUWu7)

Xác định vấn đề Phản ứng được chọn xuống cấp: DPO giữ xếp hạng `y_w > y_l`Nhưng sự kiểm tra toàn diện của `y_w`BPO thêm một sửa đổi một dòng phạt chuyển động xuống trên câu trả lời được chọn. báo cáo chính xác +10.1% trên Llama-3.1-8B-Instruct về lý luận toán học trên DPO.

> BPO 识别了"退化选择响应" vấn đề:DPO 保持 `y_w > y_l`排序但 `y_w` Phân tích về các phương pháp học của Llama-3.1-8B-Instruct

> **【拓展：DAA 过度优化 → 通用防御】**Rafailov 等人(NeurIPS 2024) trong nhiều tập hợp dữ liệu và KL  ngân sách đào tạo DPO、IPO、SLiC 策略。 thực thưởng với đường cong của KL xuất hiện giống như Gao 等人。 phần thưởng ẩn của DAA trong quá trình đào tạo tìm kiếm phân bố ngoài mẫu, KL 正则化无法稳定这一点──

### Kết quả phổ biến: DAAs vẫn tối ưu hóa quá mức

Rafailov et al. "Các quy luật về tối ưu hóa quá mức mô hình phần thưởng trong thuật toán sắp xếp trực tiếp" (NeurIPS 2024) đào tạo các chính sách với DPO, IPO, SLiC về nhiều bộ dữ liệu trên các ngân sách KL. Các đường cong vàng-mức thưởng-về-KL có hình dạng cao điểm và sụp đổ Gao et al. Các câu hỏi phần thưởng ngầm ngoài phân phối mẫu trong quá trình đào tạo; điều chỉnh KL không ổn định điều này.

> Rafailov ỹng trong nhiều tập dữ liệu và KL ỹng ngân sách đào tạo DPO、IPO、SLiC ỹ thuật。 Giải thưởng thực sự xuất hiện với đường cong của KL với hình dạng tăng và giảm giống như Gao ỹng。 Giải thưởng ẩn của DAA trong quá trình đào tạo tìm kiếm phân tán mẫu, KL chính thức không thể ổn định điều này。

DAAs không thoát khỏi Goodhart. Chúng thay đổi bề mặt nơi nó cắn từ "mô hình phần thưởng được tối ưu hóa quá mức" đến "tỷ lệ chính sách tham chiếu được tối ưu hóa quá mức".

> DAA không thoát khỏi luật cũ. Chúng chỉ đơn giản là sẽ tấn công bề mặt từ "tự ưu đãi quá mức mô hình thưởng" thành "tự ưu đãi quá mức tỷ lệ tỷ lệ chiến lược tham khảo".

> **【中文解读】**2026 năm phương pháp lựa chọn chỉ dẫn: có rất nhiều tỷ lệ chọn lựa chọn lựa chọn lựa chọn chọn lựa chọn lựa chọn lựa chọn chọn lựa chọn chọn lựa chọn lựa chọn chọn lựa chọn lựa chọn lựa chọn chọn lựa chọn lựa chọn chọn lựa chọn chọn lựa chọn chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn chọn lựa chọn lựa chọn chọn lựa chọn lựa chọn lựa chọn lựa chọn chọn lựa chọn chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa chọn lựa

### Chọn trong số họ (2026)

- Nếu bạn có dữ liệu ưu tiên cặp lớn: DPO với beta bảo thủ, SimPO nếu sự thiên vị chiều dài rõ ràng.
  Trung文翻译: có rất nhiều phụ đối với sự lựa chọn dữ liệu → DPO(保守 beta),如有长度偏见使用 SimPO。
- Nếu bạn có phản hồi nhị phân không cặp: KTO.
  Trung文翻译:有非配对二元反 → KTO。
- Nếu bạn muốn một đường ống một giai đoạn từ một mô hình cơ bản: ORPO.
  Trung ngữ翻译: muốn từ nền mô hình đơn giai đoạn管线 → ORPO。
- Nếu bạn thấy các bản kiểm tra hồ sơ được chọn bị suy giảm trong hồ sơ DPO: BPO.
  Trung文翻译:DPO 日志中看选择概率下降 → BPO。
- Nếu ưu tiên mạnh khác nhau rất nhiều và DPO là bão hòa: IPO.
  Trung文翻译:偏好强度变化大且 DPO 和 → IPO。

Mỗi phòng thí nghiệm chạy tất cả năm trên một pin và chọn người chiến thắng cho mỗi nhiệm vụ.

> Mỗi phòng thí nghiệm chạy hoàn thành trên tất cả các phương pháp và không có lý do để cho rằng phương pháp tốt nhất cho lý luận toán học và an toàn là một.

> **【拓展：DPO 家族实践 → 方法选择】**2026 mỗi phòng thí nghiệm tiên phong chạy trên tất cả các phương pháp theo các nhiệm vụ khác nhau. Không có lý do để cho rằng phương pháp tốt nhất cho lý luận và an toàn toán học là một.

## Hãy sử dụng nó để thực hiện
```figure
dpo-margin
```

## Sử dụng nó

`code/main.py`so sánh sáu lỗ (DPO, IPO, KTO, SimPO, ORPO, BPO) trên một bộ dữ liệu ưu tiên đồ chơi nơi sức mạnh ưu tiên thực sự thay đổi theo cặp. Mỗi lỗ được tối ưu hóa so với mẫu 500 cặp cùng với chính sách softmax nhỏ.

> `code/main.py`Trong tập dữ liệu về các loại đồ chơi thay đổi cường độ ưu tiên so sánh 6 loại lỗ hổng (DPO,IPO,KTO,SimPO,ORPO,BPO)  Mỗi loại lỗ hổng trong cùng 500 mẫu sử dụng tối ưu hóa chiến lược softmax nhỏ trên mẫu  vẽ tỷ lệ chiến thắng cuối cùng của mỗi phương pháp  chọn tỷ lệ di chuyển và phân phối phần thưởng ẩn 

## Chuyển nó đi.

Bài học này sẽ mang lại kết quả `outputs/skill-preference-loss-selector.md`. Với số liệu thống kê của bộ dữ liệu (cặp với không cặp, biến với sức mạnh ưu tiên đồng nhất, phân phối chiều dài) và mục tiêu (một giai đoạn hoặc SFT-then-preference), đề nghị mất ưu tiên và báo cáo chế độ thất bại mà nó bảo vệ chống lại.

> 本课产 出 `outputs/skill-preference-loss-selector.md` Định nghĩa dữ liệu tập thống kê ()                                                                                                                                                                                                                                                         

## Tập luyện bài tập

1. Đi chạy`code/main.py`. báo cáo sự sụt giảm cuối cùng của các hồ sơ kiểm tra được chọn cho DPO và BPO. BPO nên giữ cho xác suất tuyệt đối được chọn cao hơn
   Trung ngữ翻译:运行 `code/main.py` BPO 应保持更高的选择绝对概率 证实这一点──

2. Thay đổi dữ liệu ưu tiên để tất cả các cặp có sức mạnh bằng nhau.
   Trung ngữ翻译: sửa đổi ưu tiên dữ liệu làm cho tất cả các đối tác cường độ tương tự.

3. Làm cho các phản ứng bị từ chối trung bình dài hơn 2 lần so với lựa chọn.
   Trung ngữ翻译:使拒响应平均比选择响应长 2倍──不改变其他东西, số lượng cho thấy DPO 的长度利用和 SimPO 的修复──

4. Rafailov et al. (NeurIPS 2024) tuyên bố DAAs tối ưu hóa quá mức. Tạo lại một phiên bản điểm duy nhất: biểu đồ chọn-minus-đánh chối sự khác biệt KL và quan sát tối ưu hóa quá mức trong DPO ở beta lớn.
   Trung文翻译:Rafailov 等人(NeurIPS 2024) tuyên bố DAA 过度优化──复现单点版本:绘制选择减拒的 KL 散度,观察 DPO 在大beta 时的过度优化──

5. Đọc bản tóm tắt của BPO (OpenReview b97EwMUWu7).`code/main.py`- Tôi không biết.
   Trung văn翻译:阅读 BPO 论文摘要(OpenReview b97EwMUWu7)。写下 BPO đối với DPO 添加的单行修正──对照`code/main.py`Trung thực hiện xác nhận.

## Từ khóa  Keyword

| Term | What people say | What it actually means |
| 术语 | 人们怎么说 | 实际含义 |
|------|-----------------|------------------------|
| DPO | "RLHF without a reward model" / "没有奖励模型的 RLHF" | Loss derived from the closed-form RLHF optimum; policy parameters only / 从闭式 RLHF 最优解推导的损失；仅策略参数 |
| Implicit reward | "the log-ratio" / "对数比率" | `beta * log(pi(y\|x) / pi_ref(y\|x))` — the DPO-implied reward / DPO 隐含的奖励 |
| IPO | "bounded DPO" / "有界 DPO" | Replaces log-sigmoid with identity; implicit reward gap capped by `1/(2 beta)` / 用恒等映射替换 log-sigmoid；隐式奖励差距被 `1/(2 beta)` 封顶 |
| KTO | "unpaired DPO" / "非配对 DPO" | Prospect-theory utility over single labels with loss aversion / 带损失厌恶的单标签前景理论效用 |
| SimPO | "reference-free DPO" / "无参考 DPO" | Length-normalized log-likelihood + margin; no reference policy / 长度归一化对数似然 + 边际；无参考策略 |
| ORPO | "one-stage DPO" / "单阶段 DPO" | NLL + odds-ratio preference term; trains from base model in one pass / NLL + 胜率比偏好项；单阶段从基础模型训练 |
| BPO | "chosen-preserving DPO" / "保留选择的 DPO" | DPO plus a penalty for decreasing the chosen response's absolute log-prob / DPO 加上降低选择响应绝对对数概率的惩罚 |
| Degraded Chosen | "chosen goes down" / "选择概率下降" | DPO decreases chosen log-prob so long as rejected falls faster / DPO 降低选择对数概率只要拒绝下降更快 |
| DAA | "direct alignment algorithm" / "直接对齐算法" | Any preference-loss method that skips an explicit RM / 任何跳过显式 RM 的偏好损失方法 |

## Xem thêm 延伸阅读

- [Rafailov et al. — Direct Preference Optimization (NeurIPS 2023, arXiv:2305.18290)](https://arxiv.org/abs/2305.18290)
  中文翻译:Rafailov 等人DPO 原始论文
- [Azar et al. — A General Theoretical Paradigm to Understand Learning from Human Preferences (AISTATS 2024, arXiv:2310.12036)](https://arxiv.org/abs/2310.12036) IPO
  Trung ngữ翻译:Azar 等人IPO 论文
- [Ethayarajh et al. — KTO: Model Alignment as Prospect Theoretic Optimization (arXiv:2402.01306)](https://arxiv.org/abs/2402.01306)
  中文翻译:Ethayarajh 等人KTO 论文
- [Meng, Xia, Chen — SimPO (NeurIPS 2024, arXiv:2405.14734)](https://arxiv.org/abs/2405.14734)
  Trung văn翻译:Meng 等人SimPO 论文
- [Hong, Lee, Thorne — ORPO (EMNLP 2024, arXiv:2403.07691)](https://arxiv.org/abs/2403.07691)
  Trung ngữ翻译:Hong 等人ORPO 论文
- [BPO — Behavior Preservation Optimization (ICLR 2026 OpenReview b97EwMUWu7)](https://openreview.net/forum?id=b97EwMUWu7)
  Trung文翻译:BPO行为保持优化
- [Rafailov et al. — Scaling Laws for RM Overoptimization in DAAs (NeurIPS 2024, arXiv:2406.02900)](https://arxiv.org/abs/2406.02900)
  Trung文翻译:Rafailov 等人DAA 过度优化缩放定律
