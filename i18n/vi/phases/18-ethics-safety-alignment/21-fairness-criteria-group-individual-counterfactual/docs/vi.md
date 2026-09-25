# Các tiêu chí công bằng  Nhóm, cá nhân, giả mạo 

> Ba gia đình cấu trúc văn học công bằng. Sự công bằng trong nhóm: sự bình đẳng nhân khẩu học, tỷ lệ tỷ lệ cân bằng, sự chính xác sử dụng điều kiện bình đẳng  tỷ lệ bình đẳng giữa các nhóm được bảo vệ trung bình. Sự công bằng cá nhân (Dwork et al. 2012): những cá nhân tương tự nhận được các quyết định tương tự; Lipschitz điều kiện trên bản đồ quyết định. Sự công bằng đối lập (Kusner et al. 2017): một quyết định là công bằng với một cá nhân nếu nó không thay đổi khi các thuộc tính nhạy cảm bị thay đổi ngược lại. Kết quả lý thuyết 2024 (NeurIPS 2024): có một trade-off CF-vs-sự chính xác vốn có; một phương pháp không hiểu mô hình chuyển đổi một dự báo tối ưu nhưng không công bằng thành một dự báo CF với sự mất chính xác hạn chế. Phản ứng ngược (arXiv:2401.13935, tháng 1 năm 2024): mô hình mới tránh yêu cầu can thiệp vào các thuộc tính được bảo vệ pháp lý. Sự hòa giải triết học (ICLR Blogposts 2024): với biểu đồ nguyên nhân, thỏa mãn một số biện pháp công bằng nhóm đòi hỏi sự công bằng đối lập.

> **【中文解读】**Phần này giới thiệu các nguyên tắc công bằng  nhóm công bằng  cá nhân công bằng và chống thực tế công bằng định nghĩa và thước đo  ba gia đình đưa ra các tiêu chuẩn cấu trúc khác nhau mô hình có thể nhóm công bằng nhưng cá nhân không công bằng, chống thực tế công bằng nhưng nhóm không công bằng  chọn tiêu chuẩn là quyết định chính sách, không có tiêu chuẩn là phổ biến nhất.

> **【拓展：不可能定理 → 公平性冲突】**Chouldechova / Kleinberg-Mullainathan-Raghavan (tiếng Anh: Kleinberg-Mullainathan-Raghavan, 2017) không thể định lý: quyền bình đẳng dân số, tỷ lệ bình đẳng và điều kiện sử dụng tỷ lệ chính xác bình đẳng dưới tỷ lệ cơ bản bất bình đẳng không thể đáp ứng cùng một lúc.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, three-criteria comparison) | **语言:** Python（标准库，三标准比较）
**Prerequisites:** Phase 18 · 20 (bias), Phase 02 (classical ML) | **前置知识:** Phase 18 · 20 (偏见), Phase 02 (经典 ML)
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**学本节前请先掌握:Phase 18·20(偏见) 、Phase 02(经典 ML) 、因果推断基础──公平性三大家族──
>  **【类比】**公平 = "AI của chính义天平"──群体公平(demographic parity/equalized odds) = 平均上各组别结果相等;个体公平(Dawk 2012) = 相似个体得相似决策;反事实公平(Kusner 2017) = 改变敏感属性决策不变──三者不能同时满足选择是政策决定──
> 🤔 NeurIPS 2024:CF-vs-sự chính xác Có trong cân nặng, nhưng có một phương pháp chuyển đổi bị mất giới hạn tồn tại.

## Mục tiêu học tập

- Cụ thể ba tiêu chí công bằng nhóm (sự bình đẳng dân số, tỷ lệ tỷ lệ bình đẳng, sự bình đẳng chính xác sử dụng điều kiện) và một kết quả không thể.

> Nói rõ ba nhóm bình đẳng tiêu chuẩn:

- Mô tả tính công bằng cá nhân thông qua công thức Dwork et al. 2012 Lipschitz.

> Mô tả thông qua Dwork 等人 2012 năm Lipschitz 公式定义的个体公平──

- Mô tả tính công bằng đối lập và sự phụ thuộc của nó vào biểu đồ nguyên nhân.

> Mô tả phản thực tế công bằng và phụ thuộc vào kết quả của nó.

- Giải thích các đối chứng ngược lại và lý do tại sao chúng tránh được vấn đề can thiệp vào thuộc tính bảo vệ.

> Giải thích những sự thật ngược lại và lý do tại sao chúng tránh được sự can thiệp vào các thuộc tính được bảo vệ.

## Vấn đề  vấn đề

Bài học 20 là về việc đo lường thiên vị. Bài học 21 là về việc xác định tiêu chuẩn công bằng mà phép đo nên phục vụ. Ba gia đình cung cấp các tiêu chuẩn khác nhau về cấu trúc. Một mô hình có thể là công bằng nhóm và không công bằng cá nhân, công bằng đối lập và không công bằng nhóm. Việc chọn một tiêu chuẩn là một quyết định chính sách; không có tiêu chuẩn nào là tối ưu phổ biến.

> Bài học 20 là về sự thiên vị về đo lường. Bài học 21 là về việc xác định các tiêu chuẩn công bằng về việc đo lường nên phục vụ.

## Khái niệm

> **【中文解读】**群体公平三大标准:人口平权P(Y=1 ởA=a) = P(Y=1 ởA=a'),各组接受率相等;均等化赔率P(Y=1 ởY*=y,A=a) = P(Y=1 ởY*=y,A=a'),各组真阳性率和假阳性率相等;条件使用准准率均等P Y*=yY=y,A=a) = P各Y(*=yY=y,A=a'),

### Sự công bằng trong nhóm

- **Demographic parity.**P (Y=1) A=a = P (Y=1) A=a') cho tất cả các nhóm. Tỷ lệ chấp nhận bằng nhau.
- **Equalized odds.**P (Y=1), Y=y, A=a) = P (Y=1), Y=y, A=a'). TPR và FPR trên các nhóm.
- **Conditional use accuracy equality.**P (Y*y=y, A=a) = P (Y*y, Y=y, A=a) = P (Y*y, A=a) = Y=y, Y=y, A=a') = Y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=y=

> Nhân dân quyền từng nhóm chấp nhận tỷ lệ tương đương; tỷ lệ đồng hóa  từng nhóm tỷ lệ thực và tỷ lệ giả; tỷ lệ sử dụng chính xác  từng nhóm dự đoán giá trị tương đương.

Không thể (Chouldechova, Kleinberg-Mullainathan-Raghavan 2017): ba điều này không thể được đáp ứng cùng một lúc với tỷ lệ cơ sở không bình đẳng.

> Không thể định lý: dưới tỷ lệ cơ sở bất bình đẳng, ba điều này không thể được đáp ứng cùng một lúc.

### Sự công bằng cá nhân

Dwork et al. 2012. Một bản đồ quyết định f là cá nhân công bằng đối với một métric tương đồng cụ thể đối với nhiệm vụ d nếu f(x) - f(x') <= L * d(x, x') cho một số liên tục Lipschitz. Những cá nhân tương tự nhận được các quyết định tương tự.

> Dwork 等人 2012──决策映射 f Nếu đối với một số thường Lipschitz 满足 L  f x) - f x') là <= L * d x, x'), thì đối với nhiệm vụ cụ thể tương tự mực d là cá nhân công bằng── cá nhân tương tự nhận được quyết định tương tự──

Cần xác định d. Câu hỏi chính sách, không phải thống kê.

> 需要定义 d. Đó là vấn đề chính sách, không phải là vấn đề thống kê.

> **【拓展：反事实公平 → 因果图依赖】**Kusner 等人(2017) của phản thực tế công bằng: dưới mô hình nhân quả, nếu các quyết định sau khi thay đổi thuộc tính nhạy cảm của cá nhân phản thực tế, thì quyết định đó đối với cá nhân đó là công bằng.

### Sự công bằng trái ngược thực tế

Kusner et al. 2017. Một quyết định là đối lập công bằng với cá nhân i nếu, theo mô hình nhân quả của dân số, quyết định không thay đổi khi các thuộc tính nhạy cảm i được thay đổi đối lập.

> Kusner 等人 2017: Trong mô hình nhân quả, nếu một cá nhân có tính chất nhạy cảm đối với sự thật thay đổi sau khi quyết định không thay đổi, thì quyết định đó đối với cá nhân đó là công bằng đối với sự thật.

đòi hỏi một DAG nguyên nhân. DAG là một lựa chọn mô hình hóa. Sự công bằng đối lập chỉ là hợp lý như DAG.

> 需要因果 DAG──DAG 是建模选择──反事实公平的合理性取决于DAG的合理性──

### Sự đổi giá CF/sự chính xác

NeurIPS 2024 lý thuyết: có một sự thỏa hiệp vốn có giữa tính công bằng đối lập và độ chính xác dự đoán. Một phương pháp mô hình-nhận thức có thể chuyển đổi một dự đoán tối ưu nhưng không công bằng thành một CF, với chi phí chính xác giới hạn. Chi phí chính xác phụ thuộc vào quy mô của hệ số thuộc tính nhạy cảm trong dự đoán không công bằng tối ưu.

> NeurIPS 2024  Kết quả lý thuyết: Có một cân bằng vững chắc giữa sự công khai thực tế và sự chính xác dự đoán.

### Các đối số ngược

ArXiv:2401.13935 (từ tháng 1 năm 2024). Các đối nghịch truyền thống đòi hỏi sự can thiệp vào thuộc tính nhạy cảm  "có thay đổi quyết định nếu người này là một giới tính khác". Về mặt pháp lý, điều này là vấn đề: thuộc tính được bảo vệ không thể can thiệp vào luật phân loại.

> 传统反事实需要在敏感属性上干预法律上有问题──反事实反转方向: không phải từ属性干预, mà từ kết quả ngược lại lý luận──这避免法律异议──

Các đối chứng ngược lại đảo ngược hướng: thay vì can thiệp vào thuộc tính, hãy hỏi kết hợp của các tính năng thực tế của cá nhân sẽ tạo ra kết quả đối lập. Điều này tránh sự phản đối pháp lý.

> Trở lại phản thực không phải thuộc tính dự đoán, mà hỏi những kết hợp của các đặc điểm thực tế cá nhân sẽ tạo ra phản thực kết quả.

> **【中文解读】**哲学调和(ICLR Blogposts 2024): có biểu đồ nhân tố, đáp ứng một số nhóm công bằng là một số lượng có chứa phản thực tế công bằng.

### Sự hòa giải triết học

ICLR Blogposts 2024. Với biểu đồ nguyên nhân trong tay, thỏa mãn một số biện pháp công bằng nhóm đòi hỏi sự công bằng đối lập. Ba gia đình không phải là chân chính; chúng là những khía cạnh khác nhau của cấu trúc nguyên nhân cơ bản.

> ICLR 2024: Với biểu đồ nguyên nhân, đáp ứng một số nhóm bằng cách có tính cách có liên quan đến sự đối xử với thực tế.

Điều này không giải quyết các lý thuyết bất khả thi (tỷ lệ cơ sở không bình đẳng vẫn ngăn cản sự công bằng đồng thời của nhóm).

> Không có giải pháp lý thuyết không thể, nhưng cho thấy phần đối diện bề mặt giữa "nhóm" và "nhân/người/người phản thực" là vì không có giả thuyết được tạo ra bởi mô hình nguyên nhân rõ ràng.

### Khi điều này phù hợp với giai đoạn 18

Bài học 20 là đo lường thiên vị. Bài học 21 là định nghĩa công bằng. Bài học 22 là quyền riêng tư (tự riêng tư khác biệt). Bài học 23 là đánh dấu nước. Đây là những bài học phụ thuộc vào phân bổ bổ bổ sung cho bài học 7-11.

> Bài học 20 là định kiến định đoan. Bài học 21 là định nghĩa công bằng. Bài học 22 là sự bí mật. Bài học 23 là sự ấn tượng.

> **【拓展：CF vs 准确性权衡 → 实际影响】**NeurIPS 2024  Kết quả lý thuyết: Có một cân bằng cố định giữa sự công khai thực tế và sự chính xác dự đoán. Phương pháp không thể hiểu được mô hình có thể chuyển đổi các dự đoán tốt nhất nhưng không công bằng thành CF.

## Sử dụng nó.
```figure
an-fairness-trilemma
```

## Sử dụng nó

`code/main.py`xây dựng một bộ dữ liệu phân loại nhị phân đồ chơi với một thuộc tính nhạy cảm và tỷ lệ cơ sở không bình đẳng. Xét số tỷ lệ dân số, tỷ lệ tỷ lệ cược bình đẳng và tỷ lệ sử dụng điều kiện trên một phân loại đơn giản. Quan sát ba métrics không đồng ý. Sử dụng cân nặng lại cho tỷ lệ dân số và quan sát chi phí của nó trên hai người khác.

> `code/main.py` xây dựng bộ dữ liệu phân loại thứ hai về tỷ lệ cơ sở có tính chất nhạy cảm và bất bình đẳng.

## Đưa nó lên mạng

Bài học này sẽ mang lại kết quả `outputs/skill-fairness-criterion.md`. Với một tuyên bố hoặc chính sách công bằng, xác định được tiêu chí nào được yêu cầu, liệu mô hình có thể đáp ứng các tiêu chí còn lại theo các mức cơ sở không bình đẳng được yêu cầu hay không, và DAG nguyên nhân nào mà tuyên bố phụ thuộc vào.

> 本课产 出 `outputs/skill-fairness-criterion.md` Đưa ra tuyên bố về công bằng hoặc chính sách, nhận thức tuyên bố là những tiêu chuẩn nào, đáp ứng các tiêu chuẩn còn lại dưới mức độ cơ sở bất bình đẳng hay không, cũng như tuyên bố dựa trên các nguyên nhân DAG.

## Tập luyện bài tập

1. Đi chạy`code/main.py`. báo cáo ba số liệu nhóm trên dữ liệu mặc định. Sử dụng cân nhắc lại đối số nhân khẩu học và báo cáo lại.

2. Thực hiện Dwork et al. 2012 chỉ số công bằng cá nhân bằng cách sử dụng L2 đối với các tính năng không nhạy cảm.

3. Đọc Kusner et al. 2017. Xây dựng DAG nguyên nhân hai tính năng đơn giản để ghi điểm tiếp tục và xác định điều kiện công bằng đối lập nó hàm ý.

4. Báo cáo phản thực tế ngược năm 2024 tránh can thiệp vào các thuộc tính được bảo vệ.

5. Sự hòa giải ICLR 2024 cho rằng sự công bằng nhóm và đối thực là những khía cạnh của cùng một cấu trúc.`code/main.py`và đưa ra giả định nguyên nhân làm cho chúng tương đương.

## Từ khóa  Keyword

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| Demographic parity | "equal rates" | P(Y=1 | A=a) equal across groups |
| Equalized odds | "equal TPR/FPR" | Equal true-positive and false-positive rates across groups |
| Conditional use accuracy | "equal PPV/NPV" | Equal predictive values across groups |
| Individual fairness | "Lipschitz condition" | Similar individuals get similar decisions |
| Counterfactual fairness | "causal alteration invariance" | Decision unchanged under counterfactual attribute alteration |
| Backtracking counterfactual | "explain via actuals" | Counterfactual reasoned backward from outcome, not forward from attribute |
| Impossibility theorem | "the three conflict" | Chouldechova / KMR 2017: group criteria mutually exclusive under unequal base rates |

## Xem thêm 延伸阅读

- [Dwork et al. — Fairness through Awareness (arXiv:1104.3913)](https://arxiv.org/abs/1104.3913) Công bằng cá nhân
- [Kusner, Loftus, Russell, Silva — Counterfactual Fairness (arXiv:1703.06856)](https://arxiv.org/abs/1703.06856) tính công bằng đối với thực tế
- [Chouldechova — Fair prediction with disparate impact (arXiv:1703.00056)](https://arxiv.org/abs/1703.00056) không thể
- [Backtracking Counterfactuals (arXiv:2401.13935)](https://arxiv.org/abs/2401.13935) mô hình mới cho các can thiệp thuộc tính bảo vệ
