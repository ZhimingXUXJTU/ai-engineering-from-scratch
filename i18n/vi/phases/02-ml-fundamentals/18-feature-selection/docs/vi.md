# Chọn tính năng
# Đặc điểm chọn


> Nhiều tính năng không tốt hơn, nhưng những tính năng đúng hơn.

> Đặc điểm không phải là càng nhiều càng tốt.

**Type:** Build | **类型：** 构建
**Language:**Python**语言：**Python
**Prerequisites:** Phase 2, Lessons 01-09, 08 (feature engineering) | **前置知识：** Phase 2 第 1-9 课、第 8 课（特征工程）
**Time:** ~75 minutes | **时间：** 约 75 分钟

## Mục tiêu học tập

- Thực hiện các phương pháp lọc (nới hạn biến thể, thông tin lẫn nhau, chi-quad) và phương pháp bao bì (RFE, lựa chọn phía trước) từ đầu
  Từ zero thực hiện quá法 (RFE                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
- Giải thích tại sao thông tin lẫn nhau nắm bắt các mối quan hệ không tuyến tính tính- mục tiêu mà mối tương quan không có
  Giải thích tại sao thông tin lẫn nhau có thể nắm bắt liên quan của các tính năng không liên quan đến mục tiêu liên quan
- So sánh L1 regularization (đánh chọn tích hợp) với RFE (đánh chọn bao bì) và đánh giá các tradeoff tính toán của chúng
  So sánh L1 正则化 (嵌入选择) với RFE (包装选择), đánh giá số lượng cân nặng của chúng
- Xây dựng một đường ống chọn tính năng kết hợp nhiều phương pháp và chứng minh tổng quát hóa tốt hơn trên dữ liệu được giữ
  Xây dựng kết hợp nhiều phương pháp đặc điểm chọn đường, hiển thị sự cải tiến toàn diện trên dữ liệu để lại


> **【中文解读】**
> Trẻ chọn chọn trong nhiều đặc điểm chọn ra các bộ phận hữu ích nhất. Trẻ chọn chọn trong nhiều đặc điểm chọn ra các bộ phận hữu ích nhất. Trẻ chọn trong nhiều đặc điểm chọn ra các bộ phận hữu ích nhất. Trẻ chọn trong nhiều đặc điểm chọn ra các bộ phận hữu ích nhất. Trẻ chọn trong nhiều đặc điểm chọn ra các bộ phận hữu ích nhất. Trẻ chọn trong nhiều đặc điểm chọn ra các bộ phận hữu ích nhất. Trẻ chọn trong nhiều đặc điểm chọn ra các bộ phận hữu ích nhất. Trẻ chọn trong nhiều đặc điểm chọn ra các bộ phận hữu ích nhất. Trẻ chọn trong nhiều đặc điểm chọn ra các bộ phận hữu ích nhất. Trẻ chọn trong nhiều đặc điểm khác nhau. Trẻ chọn trong nhiều đặc điểm khác nhau. Trẻ chọn trong nhiều đặc điểm khác nhau. Trẻ chọn trong nhiều đặc điểm khác nhau. Trẻ chọn trong nhiều đặc điểm khác nhau. Trẻ chọn trong nhiều đặc điểm có thể làm tăng tốc độ và khả năng phổ biến mô hình.

> **【拓展：特征选择在工业界的重要性】**
> Trong mô hình kiểm soát tài chính, mô hình quản lý yêu cầu có thể giải thích phải có thể giải thích mỗi đặc điểm tại sao được chọn. L1 chính thức hóa. Lasso) tự động sẽ giảm trọng lượng của các đặc điểm không quan trọng thành 0, đồng thời thực hiện lựa chọn đặc điểm và đào tạo mô hình. Trong phân tích biểu hiện gen, trong phân tích 20.000 gen, được chọn 50 yếu tố quan trọng từ 50 gen không chỉ nâng cao hiệu suất mô hình, mà còn cung cấp đường dẫn cho nghiên cứu cơ chế bệnh. Trong chương trình chiến thắng giải thưởng Netflix, lựa chọn đặc điểm sẽ giảm xuống hàng trăm triệu đặc điểm.

## Vấn đề  vấn đề giới thiệu

Bạn có 500 tính năng. mô hình của bạn đào tạo chậm, quá tải liên tục, và không ai có thể giải thích những gì nó đã học được. Bạn thêm thêm nhiều tính năng hy vọng để cải thiện hiệu suất. Nó trở nên tồi tệ hơn.

> Bạn có 500 đặc điểm. Mô hình luyện tập chậm, không ai giải thích được điều gì. Bạn thêm nhiều đặc điểm để cải thiện hiệu suất. Kết quả là kém hơn.

Đây là lời nguyền của tính chiều trong hành động. Khi số lượng các tính năng tăng lên, khối lượng không gian tính năng nổ ra. Điểm dữ liệu trở nên hẹp. Khoảng cách giữa các điểm hội tụ. Mô hình cần nhiều dữ liệu hơn để tìm các mẫu thực tế. Các tính năng tiếng ồn nhấn chìm các tính năng tín hiệu.

> Đây là hoạt động thực tế của chiều kích nguyền rủa. Với sự gia tăng số lượng đặc điểm, kích thước của đặc điểm không gian nổ. Điểm dữ liệu trở nên hiếm. Khoảng cách giữa các điểm trở nên giống nhau.

Sự lựa chọn tính năng là thuốc chống thuốc. Giảm tiếng ồn. Giữ lại các tính năng mang lại thông tin thực tế về mục tiêu. Kết quả: đào tạo nhanh hơn, tổng quát tốt hơn, và các mô hình bạn có thể thực sự giải thích.

> Trẻ chọn là giải pháp. Trẻ bỏ tiếng ồn. Trẻ bỏ dư thừa. Giữ lại những đặc điểm mang thông tin đích thực. Kết quả là: đào tạo nhanh hơn.

Mục tiêu không phải là sử dụng tất cả thông tin có sẵn mà là sử dụng thông tin đúng.

> Ưu điểm không phải là sử dụng tất cả thông tin có sẵn.

> **【中文解读】**
> Trẻ chọn ba loại phương pháp có những ưu điểm: qua法 (quá khác nhau)  giá trị, thông tin lẫn nhau  kiểm tra) nhanh nhất nhưng bỏ qua giao tiếp giữa các đặc điểm; gói thức (quá kết kết hợp các đặc điểm loại bỏ RFE; chọn trước) xem xét các kết hợp đặc điểm nhưng tính toán chi phí cao; nhập pháp (L1 正则化、树模型特征的重要性) trong quá trình đào tạo tự động chọn các đặc điểm, là sự cân bằng tốt nhất về hiệu quả và hiệu quả.

## Khái niệm cốt lõi

### Ba loại lựa chọn tính năng

Mỗi phương pháp lựa chọn tính năng rơi vào một trong ba loại:

> Mỗi phương pháp lựa chọn đặc điểm thuộc một trong ba loại sau:

```mermaid
flowchart TD
    A[Feature Selection Methods] --> B[Filter Methods]
    A --> C[Wrapper Methods]
    A --> D[Embedded Methods]

    B --> B1["Variance Threshold"]
    B --> B2["Mutual Information"]
    B --> B3["Chi-squared Test"]
    B --> B4["Correlation Filtering"]

    C --> C1["Recursive Feature Elimination"]
    C --> C2["Forward Selection"]
    C --> C3["Backward Elimination"]

    D --> D1["L1 / Lasso Regularization"]
    D --> D2["Tree-based Importance"]
    D --> D3["Elastic Net"]
```

**Filter methods**và chỉ số mỗi tính năng một cách độc lập bằng cách sử dụng một thước đo thống kê. Họ không sử dụng mô hình.

> **过滤法**Sử dụng thống kê đo độc lập với mỗi đặc điểm đánh giá. Không sử dụng mô hình.

**Wrapper methods**- tập hợp các mô hình để đánh giá các bộ phụ tính năng. Họ sử dụng hiệu suất mô hình như điểm số. Kết quả tốt hơn, nhưng tốn kém bởi vì họ tập lại mô hình nhiều lần.

> **包装法**Mô hình đào tạo để đánh giá các đặc điểm của tập hợp. Sử dụng hiệu suất mô hình như phần tử. Kết quả tốt hơn, nhưng chi phí cao, vì cần nhiều lần tái đào tạo mô hình.

**Embedded methods**chọn các tính năng như một phần của đào tạo mô hình. L1 điều chỉnh đẩy trọng lượng lên không. Cây quyết định chia thành các tính năng hữu ích nhất. Việc lựa chọn xảy ra trong quá trình lắp ráp, không phải là một bước riêng biệt.

> **嵌入法**Trong quá trình đào tạo mô hình, chọn tính năng. L1 chính thức hóa sẽ được chuyển hóa thành không. Cây quyết định phân chia trên các tính năng hữu ích nhất.

### Tỉ lệ biến động

Nếu một tính năng hầu như không khác nhau giữa các mẫu, nó sẽ không mang lại thông tin.

> Trình lình đơn giản nhất. Nếu một đặc điểm trong mẫu hầu như không thay đổi, nó hầu như không mang thông tin.

Hãy xem xét một tính năng là 0,0 cho 999 trong 1000 mẫu. sự khác biệt của nó gần bằng không. Không mô hình nào có thể sử dụng nó để phân biệt giữa các lớp.

> 考虑一个1000样本中999 值为0.0的特征――它的方差接近零――没有模型能用它来区分类――移除它――

```
variance(x) = mean((x - mean(x))^2)
```

Đặt ngưỡng (ví dụ: 0.01). Thả mọi tính năng với sự biến đổi dưới đó. Điều này loại bỏ các tính năng liên tục hoặc gần liên tục mà không cần nhìn vào biến mục tiêu.

> 设置 một 值(ví dụ như 0.01)。 loại bỏ khác biệt thấp hơn mỗi đặc điểm của giá trị này。

Khi nào sử dụng nó: như một bước xử lý trước các phương pháp khác. Nó bắt được các tính năng rõ ràng vô dụng với chi phí gần bằng không.

> 何時使用: như các bước xử lý trước các phương pháp khác.

Giới hạn: một tính năng có thể có sự khác biệt cao và vẫn là tiếng ồn thuần túy.

>  giới hạn: một đặc điểm có thể có độ khác biệt cao nhưng vẫn là âm thanh thanh.

### Thông tin lẫn nhau

Thông tin lẫn nhau đo lường mức độ biết giá trị của tính năng X làm giảm sự không chắc chắn về mục tiêu Y.

> 互信息衡知道特征 X có thể giảm đáng kể sự không chắc chắn đối với mục tiêu Y.

```
I(X; Y) = sum_x sum_y p(x, y) * log(p(x, y) / (p(x) * p(y)))
```

Nếu X và Y là độc lập, p(x, y) = p(x) * p(y), do đó thuật ngữ log là 0 và I(X; Y) = 0.

> Nếu X và Y 独立,p(x,y) = p(x) * p(y), do đó đối với số lượng các mục为零,I(X;Y) = 0。X 告诉你关于Y的信息越多,互信息越高。

Lợi thế chính so với tương quan: thông tin lẫn nhau nắm bắt các mối quan hệ phi tuyến tính. Một tính năng có thể có không tương quan với mục tiêu nhưng thông tin lẫn nhau cao vì mối quan hệ là vuông hoặc định kỳ.

> Đối với mối quan hệ quan trọng: nhận thức về mối quan hệ không tuyến tính. Một đặc điểm có thể liên quan đến mục tiêu là không, nhưng vì mối quan hệ là hai lần hoặc chu kỳ, thông tin lẫn nhau rất cao.

Đối với các tính năng liên tục, phân định thành thùng trước tiên (sự ước tính dựa trên histogram). Số lượng thùng ảnh hưởng đến ước tính - quá ít thùng mất thông tin, quá nhiều thùng thêm tiếng ồn. Một lựa chọn phổ biến: thùng vuông hoặc quy tắc Sturges (1 + log2(n)).

> Đối với các đặc điểm liên tục, phân bố trước thành hộp (xác định dựa trên hình dạng hình chữ nhật) ⋅ số hộp ảnh hưởng đến ước tính ⋅ quá ít hộp bị mất thông tin, quá nhiều hộp tăng tiếng ⋅ thường见选择:sqrt(n) 个分箱或 Sturges 规则 (1 + log2(n)) ⋅

```mermaid
flowchart LR
    A[Feature X] --> B[Discretize into Bins]
    B --> C["Compute Joint Distribution p(x,y)"]
    C --> D["Compute MI = sum p(x,y) * log(p(x,y) / p(x)p(y))"]
    D --> E["Rank Features by MI Score"]
    E --> F[Select Top K]
```

### Phục tiêu tính năng tái phát (RFE)

RFE là một phương pháp bao bì. Nó sử dụng tính năng quan trọng của mô hình để cắt lặp đi lặp lại:

> RFE là một phương pháp đóng gói. Nó sử dụng các đặc điểm của mô hình để tạo ra các loại hình:

1. Trình hình với tất cả các tính năng
   Sử dụng tất cả các đặc điểm
2. Các tính năng cấp độ theo tầm quan trọng (tỷ lệ đối với các mô hình tuyến tính, giảm tạp chất đối với cây)
   按重要性排列特征 (nếu có một mô hình có tính chất như vậy, thì có thể dùng mô hình có tính chất như vậy)
3. Xóa các tính năng ít quan trọng nhất
                                                                                                                                                                                                                                                                 
4. Lặp lại cho đến khi số lượng các tính năng mong muốn vẫn còn
   重复 cho đến số lượng các đặc điểm cần thiết còn sót lại

```mermaid
flowchart TD
    A["Start: All N Features"] --> B["Train Model"]
    B --> C["Rank Feature Importances"]
    C --> D["Remove Least Important"]
    D --> E{"Features == Target Count?"}
    E -->|No| B
    E -->|Yes| F["Return Selected Features"]
```

RFE xem xét các tương tác tính năng vì mô hình nhìn thấy tất cả các tính năng còn lại cùng nhau.

> RFE  cân nhắc tính cách giao tiếp, vì mô hình nhìn thấy tất cả các tính năng còn lại cùng nhau.

Chi phí: bạn đào tạo mô hình N - thời gian mục tiêu. Với 500 tính năng và mục tiêu 10, đó là 490 lần đào tạo. Đối với các mô hình đắt tiền, điều này chậm. Bạn có thể tăng tốc bằng cách loại bỏ nhiều tính năng mỗi bước (ví dụ, loại bỏ 10% dưới mỗi vòng).

> 代价:你需要训练模型 N - 目标 次数──500 个特征和目标 10 个,就是490 个训练──对于昂贵的模型,这很慢──你可以通过每步移动多个特征来加速──如每轮移动底部10%)──

### L1 (Lasso) Chuẩn bị

L1 quy định thêm giá trị tuyệt đối của trọng lượng vào hàm mất:

```
loss = prediction_error + alpha * sum(|w_i|)
```

Các tham số alpha kiểm soát cách tích cực các tính năng được cắt.

> Alpha 参数 kiểm soát đặc điểm được cắt thành cấp độ kích thích.

Tại sao chính xác là không? L1 hình phạt tạo ra một khu vực hạn chế hình kim cương trong không gian trọng lượng. Giải pháp tối ưu có xu hướng hạ cánh ở một góc của kim cương này, nơi một hoặc nhiều trọng lượng là không. L2 điều chỉnh (cột) tạo ra một hạn chế chu kỳ nơi trọng lượng thu nhỏ nhưng hiếm khi đạt đến không.

> Tại sao chính xác là không?L1 惩罚 trong không gian trọng lượng tạo ra 形约束区域──最优解倾向于落在形角上,在那里 một hoặc nhiều trọng lượng là không──L2 正则化(Ridge) tạo ra 圆形约束, trọng lượng giảm nhỏ nhưng ít thay đổi thành không──

Đây là sự lựa chọn tính năng nhúng: mô hình học được trong quá trình đào tạo những tính năng mà phải bỏ qua.

> Đây là lựa chọn đặc điểm được nhúng: mô hình trong quá trình tập luyện học để bỏ qua những đặc điểm nào.

Lợi ích: chạy đào tạo đơn, xử lý các tính năng tương quan (chọn một và không những người khác), được xây dựng trong hầu hết các triển khai mô hình tuyến tính.

> 优势: đơn次训练运行, xử lý các đặc điểm liên quan

Khác giới hạn: chỉ hoạt động cho các mô hình tuyến tính. Không thể nắm bắt tầm quan trọng của tính năng phi tuyến tính.

> 限性: chỉ áp dụng cho mô hình tuyến tính. Không thể nắm bắt được tầm quan trọng của các đặc điểm không tuyến tính.

### Sự quan trọng của tính năng cây

Cây quyết định và các tập hợp của chúng (hàng rừng ngẫu nhiên, tăng độ nghiêng) tự nhiên xếp hạng các tính năng. Mỗi phân chia làm giảm tạp chất (Gini hoặc entropy để phân loại, biến thể để lùi lại).

> 决策树及其集成 (随机森林,梯度升级) tự nhiên đối với các đặc điểm xếp hạng.

Đối với một khu rừng ngẫu nhiên với cây T:

```
importance(feature_j) = (1/T) * sum over all trees of
    sum over all nodes splitting on feature_j of
        (n_samples * impurity_decrease)
```

Điều này cung cấp một điểm số tầm quan trọng bình thường cho mỗi tính năng. Nó xử lý các mối quan hệ phi tuyến tính và tương tác tính năng tự động.

> Nó cho ra các điểm quan trọng của sự hợp nhất của mỗi đặc điểm. Nó tự động xử lý các mối quan hệ không tuyến tính và giao tiếp đặc điểm.

Cảnh sát: tầm quan trọng dựa trên cây bị thiên vị về các tính năng có nhiều giá trị độc đáo (đồng tính cao). Một cột ID ngẫu nhiên sẽ xuất hiện quan trọng vì nó chia sẻ hoàn hảo mọi mẫu. Sử dụng tầm quan trọng permutation như một kiểm tra trí tuệ.

> Lưu ý: Sự quan trọng của mô hình cây có nhiều tính năng có giá trị duy nhất. Một tự nhiên ID 列会显得 quan trọng, vì nó phân chia hoàn hảo mỗi mẫu.

### Tầm quan trọng của sự chuyển đổi

Một phương pháp mô hình-những người:

> Một cách không liên quan đến mô hình:

1. Cử lý mô hình và ghi lại hiệu suất cơ sở trên dữ liệu xác thực
   训练模型并记录 trên dữ liệu chứng minh hiệu suất cơ bản
2. Đối với mỗi tính năng: trộn các giá trị của nó ngẫu nhiên, đo đạc giảm hiệu suất
   Đối với mỗi đặc điểm:随机打乱其值, hiệu suất đo giảm
3. Thêm vào đó, tính năng này càng lớn
   Nhanh xuống càng lớn, đặc điểm càng quan trọng

Nếu sự trộn lẫn của một tính năng không làm tổn hại hiệu suất, mô hình không phụ thuộc vào nó.

> Nếu một tính năng không ảnh hưởng đến hiệu suất, mô hình không phụ thuộc vào nó. Nếu hiệu suất sụp đổ, tính năng này là quan trọng.

Tầm quan trọng của sự chuyển đổi tránh sự thiên vị về tính chất của sự quan trọng dựa trên cây. Nhưng nó chậm: một đánh giá đầy đủ cho mỗi tính năng, lặp lại nhiều lần để ổn định.

> Sự quan trọng của việc thay thế tránh sự phân biệt số lượng cơ bản của mô hình cây. Nhưng nó rất chậm: mỗi đặc điểm được đánh giá một lần đầy đủ, để ổn định cần phải lặp lại nhiều lần.

### Bảng so sánh

| Method | Type | Speed | Nonlinear | Feature Interactions |
|--------|------|-------|-----------|---------------------|
| Variance threshold | Filter | Very fast | No | No |
| Mutual information | Filter | Fast | Yes | No |
| Correlation filter | Filter | Fast | No | No |
| RFE | Wrapper | Slow | Depends on model | Yes |
| L1 / Lasso | Embedded | Fast | No (linear) | No |
| Tree importance | Embedded | Medium | Yes | Yes |
| Permutation importance | Model-agnostic | Slow | Yes | Yes |

### Hình ảnh dòng chảy quyết định

```mermaid
flowchart TD
    A[Start: Feature Selection] --> B{How many features?}
    B -->|"< 50"| C["Start with variance threshold + mutual information"]
    B -->|"50-500"| D["Variance threshold, then L1 or tree importance"]
    B -->|"> 500"| E["Variance threshold, then mutual info filter, then RFE on survivors"]

    C --> F{Using linear model?}
    D --> F
    E --> F

    F -->|Yes| G["L1 regularization for final selection"]
    F -->|No - trees| H["Tree importance + permutation importance"]
    F -->|No - other| I["RFE with your model"]

    G --> J[Validate: compare selected vs all features]
    H --> J
    I --> J

    J --> K{Performance improved?}
    K -->|Yes| L["Ship with selected features"]
    K -->|No| M["Try different method or keep all features"]
```

## Hãy xây dựng nó.

> **【中文解读】**
> Từ thực hiện零三类特征选择方法:过法(方差值、互信息、卡方检查独立评估每个特征) 、包装法(递归特征消除RFE反复训练模型消除最不重要特征) 、嵌入法(L1 正规化 Lasso训练时自动将不重要特征权重压缩为零) ⋅通过合成数据(已知哪些特征有用) 验证各方法的效果──

> **【拓展：特征选择在 LLM 时代的新意义】**
> Mặc dù số lượng đào tạo sâu được gọi là "hình thức học tự động", nhưng các đặc điểm chọn lựa trong các trường hợp sau đây vẫn quan trọng: 1) biểu đồ dữ liệu đặc điểm chọn lựa có thể nâng cao hiệu suất và tốc độ đào tạo của XGBoost / LightGBM; 2) yêu cầu giải thích được  lĩnh vực y tế và tài chính cần giải thích những đặc điểm được sử dụng; 3) 嵌入空间 Ngay cả Transformer, cũng cần phải nhúng 维度上做"特征选择" (tự chọn đặc điểm)  Cơ chế chú ý bản chất là một loại chọn tính năng động)  GPT-4 của OpenAI 技术报告提到, trong đào tạo đã sử dụng chiến lược chọn dữ liệu dựa trên tầm quan trọng.
```figure
f3-feature-prune
```

## Hãy xây dựng nó

### Bước 1: Tạo dữ liệu tổng hợp với cấu trúc tính năng được biết đến

```python
import numpy as np


def make_feature_selection_data(n_samples=500, seed=42):
    rng = np.random.RandomState(seed)

    x1 = rng.randn(n_samples)
    x2 = rng.randn(n_samples)
    x3 = rng.randn(n_samples)
    x4 = x1 + 0.1 * rng.randn(n_samples)
    x5 = x2 + 0.1 * rng.randn(n_samples)

    informative = np.column_stack([x1, x2, x3, x4, x5])

    correlated = np.column_stack([
        x1 * 0.9 + 0.1 * rng.randn(n_samples),
        x2 * 0.8 + 0.2 * rng.randn(n_samples),
        x3 * 0.7 + 0.3 * rng.randn(n_samples),
        x1 * 0.5 + x2 * 0.5 + 0.1 * rng.randn(n_samples),
        x2 * 0.6 + x3 * 0.4 + 0.1 * rng.randn(n_samples),
    ])

    noise = rng.randn(n_samples, 10) * 0.5

    X = np.hstack([informative, correlated, noise])
    y = (2 * x1 - 1.5 * x2 + x3 + 0.5 * rng.randn(n_samples) > 0).astype(int)

    feature_names = (
        [f"info_{i}" for i in range(5)]
        + [f"corr_{i}" for i in range(5)]
        + [f"noise_{i}" for i in range(10)]
    )

    return X, y, feature_names
```

Chúng ta biết sự thật cơ bản: các tính năng 0-4 là thông tin (cả 3 và 4 là bản sao tương quan của 0 và 1), các tính năng 5-9 tương quan với các tính năng thông tin, các tính năng 10-19 là tiếng ồn thuần túy.

> Chúng ta biết tình huống thực tế: đặc điểm 0-4 là có thông tin của mình (trong số 3 và 4 là 0 và 1), đặc điểm 5-9 là có thông tin liên quan đến đặc điểm, đặc điểm 10-19 là âm thanh thanh thanh thanh thanh.

### Bước 2: Khoảng hạn biến động

```python
def variance_threshold(X, threshold=0.01):
    variances = np.var(X, axis=0)
    mask = variances > threshold
    return mask, variances
```

### Bước 3: Thông tin lẫn nhau (tự riêng tư)

```python
def discretize(x, n_bins=10):
    min_val, max_val = x.min(), x.max()
    if max_val == min_val:
        return np.zeros_like(x, dtype=int)
    bin_edges = np.linspace(min_val, max_val, n_bins + 1)
    binned = np.digitize(x, bin_edges[1:-1])
    return binned


def mutual_information(X, y, n_bins=10):
    n_samples, n_features = X.shape
    mi_scores = np.zeros(n_features)

    y_vals, y_counts = np.unique(y, return_counts=True)
    p_y = y_counts / n_samples

    for f in range(n_features):
        x_binned = discretize(X[:, f], n_bins)
        x_vals, x_counts = np.unique(x_binned, return_counts=True)
        p_x = dict(zip(x_vals, x_counts / n_samples))

        mi = 0.0
        for xv in x_vals:
            for yi, yv in enumerate(y_vals):
                joint_mask = (x_binned == xv) & (y == yv)
                p_xy = np.sum(joint_mask) / n_samples
                if p_xy > 0:
                    mi += p_xy * np.log(p_xy / (p_x[xv] * p_y[yi]))
        mi_scores[f] = mi

    return mi_scores
```

### Bước 4: Phục tiêu tính năng tái phát

```python
def simple_logistic_importance(X, y, lr=0.1, epochs=100):
    n_samples, n_features = X.shape
    w = np.zeros(n_features)
    b = 0.0

    for _ in range(epochs):
        z = X @ w + b
        pred = 1.0 / (1.0 + np.exp(-np.clip(z, -500, 500)))
        error = pred - y
        w -= lr * (X.T @ error) / n_samples
        b -= lr * np.mean(error)

    return w, b


def rfe(X, y, n_features_to_select=5, lr=0.1, epochs=100):
    n_total = X.shape[1]
    remaining = list(range(n_total))
    rankings = np.ones(n_total, dtype=int)
    rank = n_total

    while len(remaining) > n_features_to_select:
        X_subset = X[:, remaining]
        w, _ = simple_logistic_importance(X_subset, y, lr, epochs)
        importances = np.abs(w)

        least_idx = np.argmin(importances)
        original_idx = remaining[least_idx]
        rankings[original_idx] = rank
        rank -= 1
        remaining.pop(least_idx)

    for idx in remaining:
        rankings[idx] = 1

    selected_mask = rankings == 1
    return selected_mask, rankings
```

### Bước 5: Chọn tính năng L1

```python
def soft_threshold(w, alpha):
    return np.sign(w) * np.maximum(np.abs(w) - alpha, 0)


def l1_feature_selection(X, y, alpha=0.1, lr=0.01, epochs=500):
    n_samples, n_features = X.shape
    w = np.zeros(n_features)
    b = 0.0

    for _ in range(epochs):
        z = X @ w + b
        pred = 1.0 / (1.0 + np.exp(-np.clip(z, -500, 500)))
        error = pred - y

        gradient_w = (X.T @ error) / n_samples
        gradient_b = np.mean(error)

        w -= lr * gradient_w
        w = soft_threshold(w, lr * alpha)
        b -= lr * gradient_b

    selected_mask = np.abs(w) > 1e-6
    return selected_mask, w
```

### Bước 6: Tầm quan trọng dựa trên cây (trái quyết định đơn giản)

```python
def gini_impurity(y):
    if len(y) == 0:
        return 0.0
    classes, counts = np.unique(y, return_counts=True)
    probs = counts / len(y)
    return 1.0 - np.sum(probs ** 2)


def best_split(X, y, feature_idx):
    values = np.unique(X[:, feature_idx])
    if len(values) <= 1:
        return None, -1.0

    best_threshold = None
    best_gain = -1.0
    parent_gini = gini_impurity(y)
    n = len(y)

    for i in range(len(values) - 1):
        threshold = (values[i] + values[i + 1]) / 2.0
        left_mask = X[:, feature_idx] <= threshold
        right_mask = ~left_mask

        n_left = np.sum(left_mask)
        n_right = np.sum(right_mask)

        if n_left == 0 or n_right == 0:
            continue

        gain = parent_gini - (n_left / n) * gini_impurity(y[left_mask]) - (n_right / n) * gini_impurity(y[right_mask])

        if gain > best_gain:
            best_gain = gain
            best_threshold = threshold

    return best_threshold, best_gain


def tree_importance(X, y, n_trees=50, max_depth=5, seed=42):
    rng = np.random.RandomState(seed)
    n_samples, n_features = X.shape
    importances = np.zeros(n_features)

    for _ in range(n_trees):
        sample_idx = rng.choice(n_samples, size=n_samples, replace=True)
        feature_subset = rng.choice(n_features, size=max(1, int(np.sqrt(n_features))), replace=False)

        X_boot = X[sample_idx]
        y_boot = y[sample_idx]

        tree_imp = _build_tree_importance(X_boot, y_boot, feature_subset, max_depth)
        importances += tree_imp

    total = importances.sum()
    if total > 0:
        importances /= total

    return importances


def _build_tree_importance(X, y, feature_subset, max_depth, depth=0):
    n_features = X.shape[1]
    importances = np.zeros(n_features)

    if depth >= max_depth or len(np.unique(y)) <= 1 or len(y) < 4:
        return importances

    best_feature = None
    best_threshold = None
    best_gain = -1.0

    for f in feature_subset:
        threshold, gain = best_split(X, y, f)
        if gain > best_gain:
            best_gain = gain
            best_feature = f
            best_threshold = threshold

    if best_feature is None or best_gain <= 0:
        return importances

    importances[best_feature] += best_gain * len(y)

    left_mask = X[:, best_feature] <= best_threshold
    right_mask = ~left_mask

    importances += _build_tree_importance(X[left_mask], y[left_mask], feature_subset, max_depth, depth + 1)
    importances += _build_tree_importance(X[right_mask], y[right_mask], feature_subset, max_depth, depth + 1)

    return importances
```

### Bước 7: Thực hiện tất cả các phương pháp và so sánh

Các tập tin mã chạy tất cả năm phương pháp trên cùng một tập dữ liệu tổng hợp và in một bảng so sánh cho thấy các tính năng mà mỗi phương pháp chọn.

> Các tập tin mã chạy trên cùng một tập dữ liệu tổng hợp tất cả năm phương pháp, và in bảng so sánh cho thấy mỗi phương pháp đã chọn những đặc điểm nào.

## Hãy sử dụng nó để thực hiện

Với scikit-learn, lựa chọn tính năng được xây dựng vào đường ống dẫn:

> Sử dụng các mô hình học tập, đặc điểm chọn nội dung trong đường ống:

```python
from sklearn.feature_selection import (
    VarianceThreshold,
    mutual_info_classif,
    RFE,
    SelectFromModel,
)
from sklearn.linear_model import Lasso, LogisticRegression
from sklearn.ensemble import RandomForestClassifier

vt = VarianceThreshold(threshold=0.01)
X_filtered = vt.fit_transform(X)

mi_scores = mutual_info_classif(X, y)
top_k = np.argsort(mi_scores)[-10:]

rfe_selector = RFE(LogisticRegression(), n_features_to_select=10)
rfe_selector.fit(X, y)
X_rfe = rfe_selector.transform(X)

lasso_selector = SelectFromModel(Lasso(alpha=0.01))
lasso_selector.fit(X, y)
X_lasso = lasso_selector.transform(X)

rf = RandomForestClassifier(n_estimators=100)
rf.fit(X, y)
importances = rf.feature_importances_
```

Các thực hiện từ đầu cho thấy chính xác những gì xảy ra bên trong mỗi phương pháp.`var(X, axis=0)`và áp dụng một mặt nạ. thông tin chung là đếm tần số khớp và biên trong một bảng tình huống. RFE là một vòng tròn tập luyện, xếp hạng và cỏ. L1 là giảm độ nghiêng với một bước ngập ngập mềm.

> Từ thực hiện bằng cách hiển thị chính xác những gì đã xảy ra trong mỗi phương pháp.`var(X, axis=0)`Và áp dụng ẩn dụ. Thông tin lẫn nhau là tần số kết hợp và tần số biên trong bảng tính liên kết. RFE là một vòng tròn tập luyện, sắp xếp, cắt ránh. L1 là một bước giảm thang của các bước mềm.

Các phiên bản sklearn thêm độ bền (ví dụ, mutual_info_classif sử dụng ước tính mật độ k-NN thay vì binning), tốc độ (c thực hiện C) và tích hợp đường ống.

> Kế hoạch  phiên bản tăng 鲁棒性(如互通_info_classif 使用 k-NN 密度估计而非分箱) 速度(C 实现) 和管线集成──

## Chuyển nó đi.

Bài học này mang lại:
- `outputs/skill-feature-selector.md`-- một cây quyết định tham chiếu nhanh để chọn phương pháp lựa chọn tính năng đúng

## Tập luyện bài tập

1. **Forward selection**: thực hiện ngược lại của RFE. Bắt đầu với không tính năng. Ở mỗi bước, thêm tính năng cải thiện hiệu suất mô hình nhiều nhất. dừng khi thêm tính năng không còn giúp ích. So sánh các tính năng được chọn với kết quả RFE. Which is faster? Which gives better results?
   1. Sinh ra 100 bộ dữ liệu về các đặc điểm, trong đó 10 liên quan đến mục tiêu, 90 là tiếng ồn.

2. **Stability selection**: chạy L1 tính năng lựa chọn 50 lần, mỗi lần trên một mẫu phụ ngẫu nhiên 80% của dữ liệu, với giá trị alpha khác nhau một chút. đếm bao nhiêu lần mỗi tính năng được chọn. Các tính năng được chọn trong > 80% các chạy là " ổn định. " So sánh tính năng ổn định với lựa chọn L1 một lần chạy.
   2. 实现后向消除 (~)  从所有特征开始,逐个移除)  与前向选择比较效率和结果

3. **Multicollinearity detection**: tính toán các matrix tương quan cho tất cả các tính năng. Thực hiện một hàm, với một ngưỡng tương quan (ví dụ 0,9), loại bỏ một tính năng từ mỗi cặp có tương quan cao (giữ một với thông tin lẫn nhau cao hơn với mục tiêu).
   3. Kết quả lựa chọn của L1 và RFE trên cùng một tập dữ liệu. Chúng chọn cùng một đặc điểm?

4. **Feature selection pipeline**: ngưỡng biến số chuỗi, bộ lọc thông tin lẫn nhau và RFE vào một đường ống dẫn. Trước tiên loại bỏ các tính năng biến số gần bằng không, sau đó giữ 50% trên bằng thông tin lẫn nhau, sau đó chạy RFE trên những người sống sót. So sánh đường ống này với chạy RFE một mình trên tất cả các tính năng. đường ống dẫn nhanh hơn không? Nó cũng chính xác không?
   4. 构建完整的特征选择管线:方差值 -> 相关性过 -> 互信息 -> L1――展示每步移除多少特征以及模型性能的变化――

5. **Permutation importance from scratch**: thực hiện tầm quan trọng của sự thay đổi. Đối với mỗi tính năng, trộn các giá trị của nó 10 lần, đo lường sự sụt giảm trung bình trong điểm số F1. So sánh xếp hạng với tầm quan trọng dựa trên cây. Tìm những trường hợp họ không đồng ý và giải thích lý do tại sao (khung: các tính năng tương quan).

> **【中文解读】**
> Chiến lược thực tế của tính năng chọn: 1) sử dụng phương cách khác nhau để loại bỏ các đặc điểm thường xuyên (quả phương cách gần không có thông tin); 2) sử dụng thông tin lẫn nhau để chọn các đặc điểm liên quan đến mục tiêu (đối với các đặc điểm liên quan), hơn toàn diện hơn; 3) sử dụng RFE hoặc L1 để xem xét sự tương tác giữa các đặc điểm (đối với các phương pháp khác nhau)  nhiều phương pháp kết hợp hơn một phương pháp ổn định hơn.

> **【拓展：递归特征消除（RFE）的工业应用】**
> RFE được sử dụng rộng rãi trong sinh vật học để chọn ra 50-100 gen có khả năng dự đoán cao nhất từ 20.000 biểu hiện gen, không chỉ nâng cao hiệu suất mô hình, mà còn cung cấp ứng cử viên cho các dấu hiệu bệnh tật. Trong lĩnh vực kiểm soát tài chính, RFE giúp chọn ra các dấu hiệu nhập cuối cùng từ hàng trăm đặc điểm ứng cử viên.

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Filter method | "Score features independently" | A feature selection approach that ranks features using a statistical measure without training a model, evaluating each feature in isolation |
| Wrapper method | "Use the model to pick features" | A feature selection approach that evaluates feature subsets by training a model and using its performance as the selection criterion |
| Embedded method | "The model selects features during training" | Feature selection that happens as part of model fitting, such as L1 regularization driving weights to zero |
| Mutual information | "How much one variable tells you about another" | A measure of the reduction in uncertainty about Y given knowledge of X, capturing both linear and nonlinear dependencies |
| Recursive Feature Elimination | "Train, rank, prune, repeat" | An iterative wrapper method that trains a model, removes the least important feature(s), and repeats until a target count is reached |
| L1 / Lasso regularization | "Penalty that kills features" | Adding the sum of absolute weight values to the loss function, which drives unimportant feature weights to exactly zero |
| Variance threshold | "Remove constant features" | Dropping features whose variance across samples falls below a specified threshold, filtering out features that carry no information |
| Feature importance | "Which features matter most" | A score indicating how much each feature contributes to model predictions, computed from split gains (trees) or coefficient magnitudes (linear) |
| Permutation importance | "Shuffle and measure the damage" | Evaluating feature importance by randomly shuffling each feature's values and measuring the resulting drop in model performance |
| Curse of dimensionality | "Too many features, not enough data" | The phenomenon where adding features increases the volume of the feature space exponentially, making data sparse and distances meaningless |

## Xem thêm 延伸阅读

- [An Introduction to Variable and Feature Selection (Guyon & Elisseeff, 2003)](https://jmlr.org/papers/v3/guyon03a.html)-- cuộc khảo sát cơ bản về các phương pháp lựa chọn tính năng, vẫn được tham khảo rộng rãi
  [Guyon & Elisseeff: An Introduction to Variable and Feature Selection (2003)](https://jmlr.org/papers/v3/guyon03a.html)- đặc trưng chọn tổng quát
- [scikit-learn Feature Selection Guide](https://scikit-learn.org/stable/modules/feature_selection.html)-- tham khảo thực tế cho các phương pháp lọc, bao bì và nhúng với các ví dụ mã
  [scikit-learn 特征选择文档](https://scikit-learn.org/stable/modules/feature_selection.html)
- [Stability Selection (Meinshausen & Buhlmann, 2010)](https://arxiv.org/abs/0809.2932)-- kết hợp mẫu phụ với lựa chọn tính năng cho kết quả mạnh mẽ, có thể tái tạo
  [Feature Engineering and Selection](http://www.feat.engineering/)- 免费在线书籍
- [Beware Default Random Forest Importances (Strobl et al., 2007)](https://bmcbioinformatics.biomedcentral.com/articles/10.1186/1471-2105-8-25)-- chứng minh sự thiên vị về tính trọng tâm dựa trên cây và đề xuất tầm quan trọng có điều kiện như là một lựa chọn thay thế
