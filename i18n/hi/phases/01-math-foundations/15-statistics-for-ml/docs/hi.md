# मशीन लर्निंग के लिए सांख्यिकी

> सांख्यिकी यह है कि आप कैसे जानते हैं कि आपका मॉडल वास्तव में काम करता है या सिर्फ भाग्यशाली था।
> 统计学告诉你模型是真的有效还是只是运气好――

**Type:** Build | **类型:** 动手
**Language:**पायथन**语言:**पायथन
**Prerequisites:** Phase 1, Lessons 06 (Probability and Distributions), 07 (Bayes' Theorem) | **前置知识:** Phase 1, 第 06 课（概率与分布）、第 07 课（贝叶斯定理）
**Time:** ~120 minutes | **时间:** ~120 分钟

## सीखने के लक्ष्य

- गणना विवरणात्मक सांख्यिकी, पीयरसन/स्पीयरमैन सहसंबंध और सह-भेरिएंस मैट्रिक्स को खरोंच से
  शून्य गणना से वर्णनात्मक सांख्यिकीय पियरसन/स्पीयरमैन  相关系数和协方差矩阵

- परिकल्पना परीक्षण (टी-टेस्ट, चि-क्वायर) करें और p-मूल्यों और विश्वास अंतराल को सही ढंग से व्याख्या करें
  执行假设检验(t 检验、卡方检验),正确解释 p 值和置信区间

- वितरण परिकल्पनाओं के बिना किसी भी मीट्रिक के लिए विश्वास अंतराल बनाने के लिए बूटस्ट्रैप पुनः नमूनाकरण का उपयोग करें
  उपयोग Bootstrap 重采样为任意标标构建置信区间,无需分布假设

- प्रभाव आकार माप का उपयोग करके सांख्यिकीय महत्व को व्यावहारिक महत्व से अलग करना
  उपयोग प्रभाव मात्रा अंतर सांख्यिकीय उल्लेखनीयता और वास्तविक उल्लेखनीयता

> **【中文解读】**
> 统计学告诉你模型是真的有效还是运气好――A/B 测试评估新模型、Bootstrap 构建置信区间、假设检查判断差异显著性 ये एमएल 实验评估的基础──

## समस्या  समस्या परिचय

> **【中文解读】**模型 A 准确率 0.87,模型 B 准确率 0.89,你部署了B──三周后线上效果反而变差因为 0.02 का अंतर है शोर नहीं है वास्तविक वृद्धि──统计学回答:差异是显著吗?置信区间多宽?样本量不够?没有统计学ML 实验 = अंधा摸象──

## अवधारणा का मूल अवधारणा

> **【拓展：AI 工程中的统计学实战】**(1) **A/B 测试**:推/搜索模型上线前必须做,统计显著(p<0.05) 才发布;(2) **Bootstrap 置信区间**: बिना किसी परिकल्पना के डेटा वितरण के, किसी भी संकेत के लिए किसी भी प्रकार का निर्माण करने के लिए पुनः प्रयोग किया जाता है।**效应量**:p मूल्य केवल आपको "किसी अंतर के बारे में" बताता है, प्रभाव मात्रा आपको "किसी अंतर के बारे में" बताती है।**多重比较校正**: 20 सुपर सेमेन्टर लिए सबसे अच्छा, अनिवार्य रूप से "多碰运气"

यह लगातार होता है. कैगलबर्ड में बदलाव. कागजात जो पुनः पेश नहीं होते. ए / बी परीक्षण जो कुछ सौ नमूनों के आधार पर विजेताओं की घोषणा करते हैं. मूल कारण हमेशा एक ही हैः कोई आंकड़े छोड़ देता है।

> यह अक्सर होता है। यह एक ही कारण है कि किसी ने सांख्यिकीय परीक्षा से चूक कर कुछ सौ नमुने दिए हैं।

सांख्यिकी आपको संकेत और शोर को अलग करने के लिए उपकरण देती है। यह आपको बताती है कि अंतर कब वास्तविक है, आपको कितना आश्वस्त होना चाहिए, और परिणाम पर भरोसा करने से पहले आपको कितने डेटा की आवश्यकता है। हर एमएल पाइपलाइन, हर मॉडल तुलना, हर प्रयोग को सांख्यिकी की आवश्यकता होती है। इसके बिना, आप अनुमान लगा रहे हैं।

> 统计学 ने आपको संकेत और शोर को अलग करने का एक उपकरण प्रदान किया है  यह आपको बताता है कि अंतर कब वास्तविक है, आपको कितना विश्वास होना चाहिए, और आपको एक परिणाम पर विश्वास करने के लिए कितने डेटा की आवश्यकता है  प्रत्येक एमएल ट्यूब, प्रत्येक मॉडल की तुलना, प्रत्येक प्रयोग को सांख्यिकी की आवश्यकता है  इसके बिना, आप केवल अनुमान लगा रहे हैं

## अवधारणा का मूल अवधारणा

### वर्णनात्मक सांख्यिकीः अपने डेटा का सारांश

इससे पहले कि आप कुछ भी मॉडल करें, आपको यह जानना होगा कि आपके डेटा कैसा दिखते हैं। वर्णनात्मक सांख्यिकी डेटा सेट को कुछ संख्याओं में संपीड़ित करती है जो इसके आकार को कैप्चर करती है।

> किसी भी मॉडल के निर्माण से पहले, आपको डेटा के पैटर्न को समझने की आवश्यकता है।

**Measures of central tendency**जवाब "कहाँ है बीच में?

> **集中趋势度量** उत्तर " मध्य में कहाँ है? "

```
Mean:   sum of all values / count
        mu = (1/n) * sum(x_i)

Median: middle value when sorted
        Robust to outliers. If you have [1, 2, 3, 4, 1000], the mean is 202
        but the median is 3.

Mode:   most frequent value
        Useful for categorical data. For continuous data, rarely informative.
```

औसत संतुलन बिंदु है। मध्यवर्ती मध्यवर्ती अंक है। जब वे विचलित होते हैं, तो आपका वितरण विकृत होता है। आय वितरण का औसत >> मध्यवर्ती (अरबपति से दाएं विकृत) होता है। प्रशिक्षण के दौरान हानि वितरण में अक्सर औसत << मध्यवर्ती (आसान नमूनों से बाएं विकृत) होता है।

> 平均值 = संतुलन बिंदु। 平均值 = मध्य अंक। 平均值 = मध्य अंक। 平均值 = मध्य अंक। 平均值 = मध्य अंक। 平均值 = मध्य अंक। 平均值 = मध्य अंक। 平均值 = मध्य अंक। 平均值 = मध्य अंक। 平均值 = मध्य अंक। 平均值 = मध्य अंक। 平均值 = मध्य अंक। 平均值 = मध्य अंक। 平均值 = मध्य अंक। 平均值 = मध्य अंक। 平均值 = मध्य अंक। 平均值 = मध्य अंक। 平均值 = मध्य अंक। 平均值 = मध्य अंक। 平均值 = मध्य अंक। 平均值 = मध्य अंक। 平均值 = मध्य अंक। 平均值 = मध्य अंक। 平均值 = मध्य अंक। 平均值 = मध्य अंक। 平均值 = मध्य अंक। 平均值 = मध्य अंक। 平均值 = मध्य अंक। 平均值 = मध्य अंक = मध्य अंक। 平均值 = मध्य अंक = मध्य अंक। 平均值 = मध्य अंक = मध्य अंक = मध्य अंक। 平均值 = मध्य अंक = मध्य अंक = मध्य अंक = मध्य अंक = मध्य अंक = मध्य अंक = मध्य अंक = मध्य अंक = बाईं ओर = साधारण नमूना = साधारण नमूना = साधारण = साधारण = साधारण = साधारण = साधारण = साधारण = साधारण = साधारण = साधारण = साधारण = साधारण = साधारण = = साधारण = = साधारण = साधारण = साधारण = = = साधारण = साधारण = साधारण = = = साधारण = = = साधारण = = = साधारण = = = = = साधारण = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

**Measures of spread**जवाब "कई बार डेटा कैसे फैला हुआ है?

> **离散程度度量** जवाब" डेटा शायद फैल गया है?

```
Variance:   average squared deviation from the mean
            sigma^2 = (1/n) * sum((x_i - mu)^2)

Standard deviation:  square root of variance
                     sigma = sqrt(sigma^2)
                     Same units as the data, so more interpretable.

Range:      max - min
            Sensitive to outliers. Almost never useful alone.

IQR:        Q3 - Q1 (interquartile range)
            The range of the middle 50% of the data.
            Robust to outliers. Used for box plots and outlier detection.
```

**Percentiles**क्रमबद्ध डेटा को 100 समान भागों में विभाजित करें। 25वें पर्सेंटाइल (Q1) का मतलब है कि 25% मान इस बिंदु से नीचे गिरते हैं। 50वें पर्सेंटाइल का अर्थ है मध्यवर्ती। 75वें पर्सेंटाइल का अर्थ है Q3.

> **百分位数**क्रमबद्ध होने के बाद डेटा को 100 等份子 में विभाजित करना होगा। 25 百分位数 ((Q1) का अर्थ है कि 25% का मूल्य इस बिंदु से कम है। 50 百分位数就是中位数── 75 百分位数是Q3──

```
For latency monitoring:
  P50 = median latency        (typical user experience)
  P95 = 95th percentile       (bad but not worst case)
  P99 = 99th percentile       (tail latency, often 10x the median)
```

एमएल में, आप अनुमानित विलंबता, भविष्यवाणी विश्वास वितरण और त्रुटि वितरण को समझने के लिए प्रतिशत के बारे में परवाह करते हैं। कम औसत त्रुटि के साथ एक मॉडल लेकिन भयानक पी 99 त्रुटि सुरक्षा-महत्वपूर्ण अनुप्रयोगों के लिए बेकार हो सकती है।

> एमएल में, आप देरी के तर्क पर ध्यान देते हैं, अनुमानित विश्वास वितरण और त्रुटि वितरण के प्रतिशत की संख्या में ध्यान देते हैं। एक औसत त्रुटि कम है, लेकिन P99 त्रुटि बहुत खराब है, सुरक्षा कुंजी अनुप्रयोगों के लिए अप्रयुक्त हो सकता है।

**Sample vs population statistics.**जब किसी नमूना से भिन्नता का गणना करते हैं, तो n के बजाय (n-1) से विभाजित करें। यह बेसल की सुधार है। यह इस तथ्य की भरपाई करता है कि आपका नमूना औसत वास्तविक जनसंख्या औसत नहीं है। नामक में n के साथ, आप व्यवस्थित रूप से वास्तविक भिन्नता का मूल्यांकन करते हैं। (n-1) के साथ, अनुमान निष्पक्ष है।

> **样本统计 vs 总体统计。**नमूना गणना में अंतर के समय, (n-1) के बजाय n से अलग करना n है। यह बेसल की सही है।

```
Population variance: sigma^2 = (1/N) * sum((x_i - mu)^2)
Sample variance:     s^2     = (1/(n-1)) * sum((x_i - x_bar)^2)
```

व्यवहार में: यदि n बड़ा है (हजारों नमूने), तो अंतर नगण्य है। यदि n छोटा है (दसों नमूने), तो यह मायने रखता है।

> 实践中: यदि n 很大(数千个样本),差异可以忽略──如果 n 很小(几十个样本),差异很重要──

### संयोगः कैसे चर एक साथ चलें 相关性: कैसे चर एक साथ बदलते हैं

सहसंबंध दो चर के बीच रैखिक संबंध की ताकत और दिशा को मापता है।

> संबंध दो चर के बीच संबंध की तीव्रता और दिशा को मापता है।

**Pearson correlation coefficient**रैखिक संघनित उपाय:

> **Pearson 相关系数**衡量线性关联:

```
r = sum((x_i - x_bar)(y_i - y_bar)) / (n * s_x * s_y)

r = +1:  perfect positive linear relationship
r = -1:  perfect negative linear relationship
r =  0:  no linear relationship (but there might be a nonlinear one!)

Range: [-1, 1]
```

पियरसन का मानना है कि संबंध रैखिक है और दोनों चर लगभग सामान्य रूप से वितरित हैं। यह असाधारण के प्रति संवेदनशील है। एक एकल चरम बिंदु r को 0.1 से 0.9 तक खींच सकता है।

> पियरसन  परिकल्पना है कि संबंध रैखिक है, और दो चर बड़े पैमाने पर सामान्य वितरण से अनुपालन करते हैं। यह असामान्य मूल्य के प्रति संवेदनशील है।

**Spearman rank correlation**एकतरफा संबंध उपायः

> **Spearman 秩相关**衡量单调关联:

```
1. Replace each value with its rank (1, 2, 3, ...)
2. Compute Pearson correlation on the ranks

Spearman catches any monotonic relationship, not just linear.
If y = x^3, Pearson gives r < 1 but Spearman gives rho = 1.
```

**When to use each:**

> **何时使用哪个：**

```
Pearson:    Both variables are continuous and roughly normal.
            You care about the linear relationship specifically.
            No extreme outliers.

Spearman:   Ordinal data (rankings, ratings).
            Data is not normally distributed.
            You suspect a monotonic but not linear relationship.
            Outliers are present.
```

**The golden rule:**संयोग का अर्थ है कारणों का संबंध नहीं है। आइसक्रीम की बिक्री और डूबने से होने वाली मौतों का संबंध है क्योंकि दोनों गर्मियों में बढ़ते हैं। आपके मॉडल की सटीकता और पैरामीटर की संख्या संबद्ध हैं, लेकिन पैरामीटर जोड़ने से सटीकता में स्वचालित रूप से सुधार नहीं होता है (देखेंः ओवरफिट) ।

> **黄金法则：**相关不意味因果──冰淋销量和溺水死亡是相关的,因为它们都在夏季增加──你的模型精度和参数数数量是相关的,但增加参数并非自动提高精度

### सह-अंतर मैट्रिक्स

दो चर के बीच सह-परिवर्तन यह मापता है कि वे कैसे भिन्न होते हैंः

>  दो चर के बीच अंतर यह मापता है कि वे कैसे एक साथ बदलते हैंः

```
Cov(X, Y) = (1/n) * sum((x_i - x_bar)(y_i - y_bar))

Cov(X, Y) > 0:  X and Y tend to increase together
Cov(X, Y) < 0:  when X increases, Y tends to decrease
Cov(X, Y) = 0:  no linear co-movement
```

d सुविधाओं के लिए, सह-विवर्तन मैट्रिक्स C एक d x d मैट्रिक्स है जहां C[i][j] = Cov(feature_i, feature_j। विकर्ण प्रविष्टियाँ C[i][i] प्रत्येक सुविधा के भिन्नताएं हैं।

> 对于d 个特征,协方差矩阵 C एक d x d矩阵 है, जिसमें C[i][j] = Cov(feature_i, feature_j) ――对角线元素 C[i][i] 是每个特征的方差──

```
C = | Var(x1)      Cov(x1,x2)  Cov(x1,x3) |
    | Cov(x2,x1)  Var(x2)      Cov(x2,x3) |
    | Cov(x3,x1)  Cov(x3,x2)  Var(x3)     |

Properties:
  - Symmetric: C[i][j] = C[j][i]
  - Positive semi-definite: all eigenvalues >= 0
  - Diagonal = variances
  - Off-diagonal = covariances
```

**Connection to PCA.**PCA स्वयं कोविरेन्स मैट्रिक्स को संकलित करता है। स्ववेक्टर मुख्य घटक (अधिकतम भिन्नता के दिशाएं) हैं। स्वमूल्य आपको बताते हैं कि प्रत्येक घटक कितना भिन्नता कैप्चर करता है। यह ठीक यही है कि पाठ 10 का कवर किया गया है, लेकिन अब आप देखते हैं कि क्यों कोविरेन्स मैट्रिक्स को विघटित करने के लिए सही चीज हैः यह आपके डेटा में सभी जोड़ेदार रैखिक संबंधों को एन्कोड करता है।

> **与 PCA 的联系。**PCA ने एक सह-समय भिन्नता रक्छा के लिए विशेषता विघटन किया है। विशेषता द्रव्यमान मुख्य घटक है। यह आपको बताता है कि प्रत्येक घटक ने कितने वर्ग विघटनों को कैप्चर किया है। यह 10 वीं कक्षा में बताया गया है, लेकिन अब आप समझ गए हैं कि क्यों एक सह-समय भिन्नता रक्छा सही विघटन वस्तु हैः यह डेटा में सभी के लिए रैखिक संबंध को कोड करता है।

**Connection to correlation.**सहसंबंध मैट्रिक्स मानकीकृत चर (प्रत्येक अपने मानक विचलन से विभाजित) की सहसंबंध मैट्रिक्स है। सहसंबंध सहसंबंध को सामान्य बनाता है इसलिए सभी मान [-1, 1 में गिरते हैं।

> **与相关性的联系。**相关矩阵是标准化变量 (), प्रत्येक के बराबर भिन्नता के बराबर भिन्नता矩阵 (), सभी मानों को [-1, 1] में समेकित करने के लिए।

### परिकल्पना परीक्षण

परिकल्पना परीक्षण अनिश्चितता के तहत निर्णय लेने के लिए एक ढांचा है। आप एक दावे से शुरू करते हैं, डेटा एकत्र करते हैं, और यह निर्धारित करते हैं कि क्या डेटा दावे के साथ संगत है।

> 假设检查在不确定性下做决策的框架中──आप एक प्रस्ताव से शुरू करते हैं, डेटा एकत्र करते हैं, फिर यह तय करते हैं कि क्या डेटा प्रस्ताव के अनुरूप है──

**The setup:**

> **基本设置：**

```
Null hypothesis (H0):        the default assumption, usually "no effect"
Alternative hypothesis (H1): what you are trying to show

Example:
  H0: Model A and Model B have the same accuracy
  H1: Model B has higher accuracy than Model A
```

**The p-value**यह अनुमान है कि H0 सच है, यह अनुमान है कि H0 सच है, यह आंकड़ों में सबसे आम गलतफहमी है।

> **p 值**यह H0 के लिए वास्तविक संभावना नहीं है। यह सांख्यिकी में सबसे आम गलतफहमी है।

```
p-value = P(data this extreme | H0 is true)

If p-value < alpha (typically 0.05):
    Reject H0. The result is "statistically significant."
If p-value >= alpha:
    Fail to reject H0. You do not have enough evidence.
    This does NOT mean H0 is true.
```

**Confidence intervals**किसी पैरामीटर के लिए मान्य मानों की सीमा देंः

> **置信区间**दिलों की एक उचित मूल्य सीमाः

```
95% confidence interval for the mean:
    x_bar +/- z * (s / sqrt(n))

where z = 1.96 for 95% confidence

Interpretation: if you repeated this experiment many times, 95% of the
computed intervals would contain the true mean. It does NOT mean there
is a 95% probability the true mean is in this specific interval.
```

विश्वास अंतराल की चौड़ाई आपको सटीकता के बारे में बताती है। व्यापक अंतराल का अर्थ है उच्च अनिश्चितता। संकीर्ण अंतराल का अर्थ है कि आपका अनुमान सटीक है (लेकिन जरूरी नहीं कि सटीक हो, यदि आपके डेटा पक्षपातपूर्ण हैं) ।

> 置信区间的宽度告诉你精度──宽区间的意思是高不确定性──狭区间的意思是你的估计是精确的(但如果数据有偏见,不一定准确) 

### टी-टेस्ट टी-टेस्ट

टी-टेस्ट तुलना के माध्यम से है. कई स्वाद हैं.

> 检测比较平均值──有几种变化──

**One-sample t-test:**क्या जनसंख्या का औसत परिकल्पना मूल्य से भिन्न है?

> **单样本 t 检验：** सकल औसत मूल्य का मानदंड से क्या अंतर है?

```
t = (x_bar - mu_0) / (s / sqrt(n))

degrees of freedom = n - 1
```

**Two-sample t-test (independent):**क्या दो समूहों का अर्थ अलग है?

> **两样本 t 检验（独立）：**क्या दोनों समूहों का औसत मूल्य भिन्न है?

```
t = (x_bar_1 - x_bar_2) / sqrt(s1^2/n1 + s2^2/n2)

This is Welch's t-test, which does not assume equal variances.
Always use Welch's unless you have a specific reason for equal variances.
```

**Paired t-test:**जब माप जोड़े में होते हैं (एक ही मॉडल के साथ आंकड़ों के समान विभाजन पर मूल्यांकन किया जाता है):

> **配对 t 检验：**जब माप एक ही डेटा विभाजन पर मूल्यांकन किया गया थाः

```
Compute d_i = x_i - y_i for each pair
Then run a one-sample t-test on the d_i values against mu_0 = 0
```

एमएल में, जोड़ी t-परीक्षण आम हैः आप दोनों मॉडल को एक ही 10 क्रॉस-वैलिडेशन फोल्ड पर चलाते हैं और उनके स्कोर की तुलना जोड़ी के रूप में करते हैं।

> एमएल में, परीक्षणों के लिए एक साथ जाना आम हैः आप एक ही 10 पारस्परिक परीक्षणों के लिए दो मॉडल चलाने, और फिर उनकी तुलना करने के लिए।

### चि-क्वाड टेस्ट कार्टून टेस्ट

चि-क्वायर परीक्षण जांचता है कि क्या देखे गए आवृत्तियों अपेक्षित आवृत्तियों से मेल खाते हैं।

> 卡方检查检查观测频率是否匹配期望频率──适用于分类数据──

```
chi^2 = sum((observed - expected)^2 / expected)

Example: does a language model's output distribution match the
training distribution across categories?

Category    Observed   Expected
Positive       120        100
Negative        80        100
chi^2 = (120-100)^2/100 + (80-100)^2/100 = 4 + 4 = 8

With 1 degree of freedom, chi^2 = 8 gives p < 0.005.
The difference is significant.
```

### एमएल मॉडल के लिए ए / बी परीक्षण

एमएल में ए/बी परीक्षण वेब ए/बी परीक्षण के समान नहीं है। मॉडल तुलना में विशिष्ट चुनौतियां हैंः

> एमएल में ए/बी 测试与网页 ए/बी 测试不同──模型比较有特定挑战:

```
1. Same test set:    Both models must be evaluated on identical data.
                     Different test sets make comparison meaningless.

2. Multiple metrics: Accuracy alone is not enough. You need precision,
                     recall, F1, latency, and fairness metrics.

3. Variance:         Use cross-validation or bootstrap to estimate
                     the variance of each metric, not just point estimates.

4. Data leakage:     If the test set was used during model selection,
                     your comparison is biased. Hold out a final test set.
```

**The procedure:**

> **操作步骤：**

```
1. Define your metric and significance level (alpha = 0.05)
2. Run both models on the same k-fold cross-validation splits
3. Collect paired scores: [(a1, b1), (a2, b2), ..., (ak, bk)]
4. Compute differences: d_i = b_i - a_i
5. Run a paired t-test on the differences
6. Check: is the mean difference significantly different from 0?
7. Compute a confidence interval for the mean difference
8. Compute effect size (Cohen's d) to judge practical significance
```

### सांख्यिकीय महत्व बनाम व्यावहारिक महत्व

परिणाम सांख्यिकीय रूप से महत्वपूर्ण हो सकता है लेकिन व्यावहारिक रूप से कोई अर्थ नहीं है। पर्याप्त डेटा के साथ, यहां तक कि एक मामूली अंतर सांख्यिकीय रूप से महत्वपूर्ण हो जाता है।

> एक परिणाम सांख्यिकीय रूप से महत्वपूर्ण हो सकता है, लेकिन वास्तव में इसका कोई अर्थ नहीं है। जब पर्याप्त डेटा होता है, तो यहां तक कि मामूली अंतर भी सांख्यिकीय रूप से महत्वपूर्ण हो जाता है।

```
Example:
  Model A accuracy: 0.9234
  Model B accuracy: 0.9237
  n = 1,000,000 test samples
  p-value = 0.001

Statistically significant? Yes.
Practically significant? A 0.03% improvement is not worth the
engineering cost of deploying a new model.
```

**Effect size**नमूना आकार के बावजूद अंतर कितना बड़ा है, यह quantifies:

> **效应量** मात्रा में अंतर बहुत अधिक है, नमूना मात्रा से कोई संबंध नहीं हैः

```
Cohen's d = (mean_1 - mean_2) / pooled_std

d = 0.2:  small effect
d = 0.5:  medium effect
d = 0.8:  large effect
```

हमेशा p-मूल्य और प्रभाव आकार दोनों की रिपोर्ट करें. p-मूल्य आपको बताता है कि क्या अंतर वास्तविक है. प्रभाव आकार आपको बताता है कि क्या यह मायने रखता है.

> 始终同时报告 p 值和效应量──p 值告诉你差异是否真实──效应量告诉你差异是否有意义──

### बहु तुलना समस्या बहु तुलना समस्या

यदि आप 20 चीजों का परीक्षण अल्फा = 0.05 पर करते हैं, तो आप 1 झूठी सकारात्मक की उम्मीद करते हैं, भले ही कुछ भी वास्तविक नहीं हो।

> जब आप कई परिकल्पनाओं का परीक्षण करते हैं, तो कुछ "अतिशय" होते हैं। यदि आप अल्फा = 0.05 पर 20 चीजों का परीक्षण करते हैं, भले ही कोई वास्तविक प्रभाव न हो, तो आप भी 1 झूठी सकारात्मकता की अपेक्षा करते हैं।

```
P(at least one false positive) = 1 - (1 - alpha)^m

m = 20 tests, alpha = 0.05:
P(false positive) = 1 - 0.95^20 = 0.64

You have a 64% chance of at least one false positive.
```

**Bonferroni correction:**परीक्षणों की संख्या के अनुसार अल्फा विभाजित करें।

> **Bonferroni 校正：**अल्फा को परीक्षण की संख्या के अलावा

```
Adjusted alpha = alpha / m = 0.05 / 20 = 0.0025

Only reject H0 if p-value < 0.0025.
Conservative but simple. Works when tests are independent.
```

एमएल में, यह तब मायने रखता है जब आप कई मापों के बीच एक मॉडल की तुलना करते हैं, कई हाइपरपरमैटर कॉन्फ़िगरेशन का परीक्षण करते हैं, या कई डेटासेट पर मूल्यांकन करते हैं।

> एमएल में, जब आप कई सूचकों पर मॉडल की तुलना करते हैं, कई सुपरपरमाइंडरों के विन्यास का परीक्षण करते हैं या कई डेटासेट पर मूल्यांकन करते हैं, तो यह महत्वपूर्ण है।

### बूटस्ट्रैप विधिएँ

बूटस्ट्रैपिंग आपके डेटा को प्रतिस्थापन के साथ पुनः नमूना करके एक आंकड़े के नमूने वितरण का अनुमान लगाता है। अंतर्निहित वितरण के बारे में कोई धारणा आवश्यक नहीं है।

> बूटस्ट्रैप ️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️

**The algorithm:**

> **算法：**

```
1. You have n data points
2. Draw n samples WITH replacement (some points appear multiple times,
   some not at all)
3. Compute your statistic on this bootstrap sample
4. Repeat B times (typically B = 1000 to 10000)
5. The distribution of bootstrap statistics approximates the
   sampling distribution
```

**Bootstrap confidence interval (percentile method):**

> **Bootstrap 置信区间（百分位数法）：**

```
Sort the B bootstrap statistics
95% CI = [2.5th percentile, 97.5th percentile]
```

**Why bootstrap matters for ML:**

> **Bootstrap 对 ML 为什么重要：**

```
- Test set accuracy is a point estimate. Bootstrap gives you
  confidence intervals.
- You cannot assume metric distributions are normal (especially
  for AUC, F1, precision at k).
- Bootstrap works for ANY statistic: median, ratio of two means,
  difference in AUC between two models.
- No closed-form formula needed.
```

**Bootstrap for model comparison:**

> **Bootstrap 用于模型比较：**

```
1. You have predictions from Model A and Model B on the same test set
2. For each bootstrap iteration:
   a. Resample test indices with replacement
   b. Compute metric_A and metric_B on the resampled set
   c. Store diff = metric_B - metric_A
3. 95% CI for the difference:
   [2.5th percentile of diffs, 97.5th percentile of diffs]
4. If the CI does not contain 0, the difference is significant
```

यह जोड़ी t-परीक्षण से अधिक मजबूत है क्योंकि यह कोई वितरण परिकल्पना नहीं करता है।

> यह परीक्षण के मुकाबले अधिक स्थिर है, क्योंकि यह वितरण परिकल्पना नहीं करता है।

### पैरामीटर बनाम गैर-परमामीटर परीक्षण

**Parametric tests**एक विशिष्ट वितरण (आमतौर पर सामान्य) का अनुमान लगाएंः

> **参数检验**假设特定分布 (आमतौर पर सही स्थिति में):

```
t-test:         assumes normally distributed data (or large n by CLT)
ANOVA:          assumes normality and equal variances
Pearson r:      assumes bivariate normality
```

**Non-parametric tests**वितरण परिकल्पना नहीं करेंः

> **非参数检验**不做分布假设:

```
Mann-Whitney U:     compares two groups (replaces independent t-test)
Wilcoxon signed-rank: compares paired data (replaces paired t-test)
Spearman rho:       correlation on ranks (replaces Pearson)
Kruskal-Wallis:     compares multiple groups (replaces ANOVA)
```

**When to use non-parametric:**

> **何时使用非参数检验：**

```
- Small sample size (n < 30) and data is clearly non-normal
- Ordinal data (ratings, rankings)
- Heavy outliers you cannot remove
- Skewed distributions
```

**When to use parametric:**

> **何时使用参数检验：**

```
- Large sample size (CLT makes the test statistic approximately normal)
- Data is roughly symmetric without extreme outliers
- More statistical power (better at detecting real differences)
```

एमएल प्रयोगों में, आप आमतौर पर छोटे n (5 या 10 क्रॉस-वैलिडेशन फोल्ड) है, इसलिए Wilcoxon हस्ताक्षरित-रैंक जैसे गैर-परिमेट्रिक परीक्षण अक्सर टी-टेस्ट की तुलना में अधिक उपयुक्त हैं।

> एमएल प्रयोगों में, आपके पास आमतौर पर 5 या 10 से अधिक पारस्परिक परीक्षण होते हैं, इसलिए विल्कोक्सन के समान अभूतपूर्व परीक्षण आमतौर पर टी से अधिक उपयुक्त होते हैं।

### केंद्रीय सीमा प्रमेय: व्यावहारिक प्रभाव

सीएलटी का कहना है कि नमूना का वितरण सामान्य वितरण के करीब आता है जैसे-जैसे n बढ़ता है, चाहे जनसंख्या का आधार आधार क्या हो।

> सीएलटी का कहना है कि, जैसे-जैसे n  वृद्धि होती है, नमूना औसत मूल्य का वितरण सामान्य वितरण के करीब आता है, चाहे निचले स्तर का समग्र वितरण कैसा भी हो।

```
If X_1, X_2, ..., X_n are iid with mean mu and variance sigma^2:

    X_bar ~ Normal(mu, sigma^2 / n)    as n -> infinity

Works for n >= 30 in most cases.
For highly skewed distributions, you might need n >= 100.
```

**Why this matters for ML:**

> **这对 ML 为什么重要：**

```
1. Justifies confidence intervals and t-tests on aggregated metrics
2. Explains why averaging over cross-validation folds gives stable
   estimates even when individual folds vary wildly
3. Mini-batch gradient descent works because the average gradient
   over a batch approximates the true gradient (CLT in action)
4. Ensemble methods: averaging predictions from many models gives
   more stable output than any single model
```

**What CLT does NOT do:**

> **CLT 不能做什么：**

```
- Does NOT make your data normal. It makes the MEAN of samples normal.
- Does NOT work for heavy-tailed distributions with infinite variance
  (Cauchy distribution).
- Does NOT apply to dependent data (time series without correction).
```

### एमएल पेपर में आम सांख्यिकीय त्रुटियां

1. **Testing on the training set.**हमेशा मॉडल प्रशिक्षण के दौरान कभी नहीं देखता डेटा बाहर रखें।

> 1. **在训练集上测试。**सुनिश्चित करें कि यह अनुकूलित है।

2. **No confidence intervals.**अनिश्चितता के बिना एक ही सटीकता संख्या की रिपोर्ट करना परिणामों को प्रतिकृति और सत्यापन योग्य नहीं बनाता है।

> 2. **没有置信区间。**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             

3. **Ignoring multiple comparisons.**50 कॉन्फ़िगरेशन का परीक्षण करना और बिना सुधार के सर्वश्रेष्ठ की रिपोर्ट करना गलत सकारात्मक दरों को बढ़ाता है।

> 3. **忽略多重比较。**测试 50 配置并报告  सर्वश्रेष्ठ एक बिना सुधार, झूठी सकारात्मकता दर में वृद्धि होगी

4. **Confusing statistical and practical significance.**0.01% सटीकता में सुधार पर 0.001 का p-मूल्य सार्थक नहीं है।

> 4. **混淆统计显著性和实际显著性。**0.01% 精度提升上 p 值 0.001 没有意义──

5. **Using accuracy on imbalanced data.**99% नकारात्मक वर्ग के साथ डेटा सेट पर 99% सटीकता का मतलब है कि मॉडल कुछ भी नहीं सीखा। सटीकता का उपयोग करें, याद, F1, या AUC।

> 5. **在不平衡数据上使用精度。**99% नकारात्मक डेटाबेस पर 99% सटीकता का अर्थ है कि मॉडल ने कुछ भी नहीं सीखा है।

6. **Cherry-picking metrics.**केवल उस मेट्रिक की रिपोर्ट करना जहां आपका मॉडल जीतता है। ईमानदार मूल्यांकन सभी प्रासंगिक मेट्रिक्स की रिपोर्ट करता है।

> 6. **挑选指标。**केवल अपने मॉडल के विजेता के संकेतकों को रिपोर्ट करें।

7. **Leaking information across train/test splits.**विभाजन से पहले सामान्यीकरण, या अतीत की भविष्यवाणी करने के लिए भविष्य के डेटा का उपयोग करना।

> 7. **在训练/测试划分之间泄露信息。**̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇  ̇ ̇ ̇ ̇ ̇   ̇ ̇    ̇ ̇    ̇ ̇          ̇      ̇     ̇ ̇                                                                                                                                                                                                         

8. **Small test sets with no variance estimates.**100 नमूनों पर मूल्यांकन करना और 2% सुधार का दावा करना शोर है, सिग्नल नहीं।

> 8. **小测试集没有方差估计。**100 नमूनों पर मूल्यांकन करते हुए दावा किया गया कि 2% की वृद्धि शोर है, न कि संकेत।

9. **Assuming independence when data is not independent.**एक ही रोगी की चिकित्सा छवियां, एक ही दस्तावेज से कई वाक्य। एक समूह के भीतर अवलोकन सहसंबंधित हैं।

> 9. **数据不独立时假设独立。**एक ही रोगी की चिकित्सा छवि से, एक ही दस्तावेज से कई वाक्य से।

10. **P-hacking.**विभिन्न परीक्षणों, उपसमूहों, या बहिष्करण मानदंडों का परीक्षण जब तक आप पी < 0.05 प्राप्त नहीं करते। परिणाम खोज का एक कलाकृत्य है।

> 10. **P 值操纵（P-hacking）。**尝试不同的检查、子集或排除标准,直到得到p <0.05── परिणाम खोज प्रक्रिया का छद्म छाया है──

## इसे बनाने के लिए कदम उठाओ

आप लागू करेंगेः

> आप को पूरा होगाः

1. **Descriptive statistics from scratch**(औसत, मध्य, मोड, मानक विचलन, प्रतिशत, IQR)
   **从零实现描述性统计**(औसत मूल्य, मध्यबिग्यान, संख्या, मानक अंतर, प्रतिशतबिग्यान, आईक्यूआर)
2. **Correlation functions**(पीयरसन और स्पीयरमैन, सह-विवर्तन मैट्रिक्स के साथ)
   **相关函数**(पीयरसन और स्पीयरमैन, तथा संगत अनुपात रक्शन्स)
3. **Hypothesis tests**(एक नमूना टी-टेस्ट, दो नमूना टी-टेस्ट, चि-क्वाड टेस्ट)
   **假设检验**(单样本 t 检验、两样本 t 检验、卡方检验)
4. **Bootstrap confidence intervals**(किसी भी सांख्यिकीय के लिए कोई अनुमान की आवश्यकता नहीं है)
   **Bootstrap 置信区间**(आच्छिक आंकड़ा, बिना किसी परिकल्पना की आवश्यकता)
5. **A/B test simulator**(डेटा उत्पन्न करना, परीक्षण करना, प्रकार I और प्रकार II की त्रुटियों की जांच करना)
   **A/B 测试模拟器**(जनरेट डेटा, परीक्षण, जांच प्रथम श्रेणी और द्वितीय श्रेणी की त्रुटि)
6. **Statistical vs practical significance demo**(यह दिखाता है कि बड़े n सब कुछ "महत्वपूर्ण" बनाता है)
   **统计 vs 实际显著性演示**(प्रदर्शन करना बड़ा n 使一切都"显著")

सब कुछ खरोंच से, केवल उपयोग करते हुए `math`और `random`कोई नंगा, कोई नंगा।

>  全部从零实现, केवल उपयोग `math`和 `random`不使用numpy、scipy。

## कीवर्ड्स  शब्द खोज तालिका
```figure
f3-bootstrap-resample
```

## प्रमुख शर्तें

| Term / 术语 | Definition / 定义 |
|---|---|
| Mean / 均值 | Sum of values divided by count. Sensitive to outliers. / 值的总和除以个数。对异常值敏感。 |
| Median / 中位数 | Middle value of sorted data. Robust to outliers. / 排序后数据的中间值。对异常值稳健。 |
| Standard deviation / 标准差 | Square root of variance. Measures spread in original units. / 方差的平方根。用原始单位衡量离散程度。 |
| Percentile / 百分位数 | Value below which a given percentage of data falls. / 给定百分比的数据低于此值。 |
| IQR / 四分位距 | Interquartile range. Q3 minus Q1. The spread of the middle 50%. / 四分位距。Q3 减 Q1。中间 50% 的展幅。 |
| Pearson correlation / Pearson 相关系数 | Measures linear association between two variables. Range [-1, 1]. / 衡量两个变量间的线性关联。范围 [-1, 1]。 |
| Spearman correlation / Spearman 相关系数 | Measures monotonic association using ranks. / 用排名衡量单调关联。 |
| Covariance matrix / 协方差矩阵 | Matrix of pairwise covariances between all features. / 所有特征间成对协方差的矩阵。 |
| Null hypothesis / 零假设 | Default assumption of no effect or no difference. / 无效应或无差异的默认假设。 |
| p-value / p 值 | Probability of data this extreme given the null hypothesis is true. / 在零假设为真的条件下观察到如此极端数据的概率。 |
| Confidence interval / 置信区间 | Range of plausible values for a parameter at a given confidence level. / 给定置信水平下参数的合理值范围。 |
| t-test / t 检验 | Tests whether means differ significantly. Uses the t-distribution. / 检验均值是否有显著差异。使用 t 分布。 |
| Chi-squared test / 卡方检验 | Tests whether observed frequencies differ from expected frequencies. / 检验观测频率是否与期望频率不同。 |
| Effect size / 效应量 | Magnitude of a difference, independent of sample size. Cohen's d is common. / 差异的大小，与样本量无关。常用 Cohen's d。 |
| Bonferroni correction / Bonferroni 校正 | Divides significance threshold by number of tests to control false positives. / 将显著性阈值除以检验次数以控制假阳性。 |
| Bootstrap / Bootstrap | Resampling with replacement to estimate sampling distributions. / 有放回重采样以估计抽样分布。 |
| Type I error / 第一类错误 | False positive. Rejecting H0 when it is true. / 假阳性。H0 为真时拒绝 H0。 |
| Type II error / 第二类错误 | False negative. Failing to reject H0 when it is false. / 假阴性。H0 为假时未能拒绝 H0。 |
| Statistical power / 统计功效 | Probability of correctly rejecting a false H0. Power = 1 minus Type II error rate. / 正确拒绝假 H0 的概率。功效 = 1 减第二类错误率。 |
| Central limit theorem / 中心极限定理 | Sample means converge to a normal distribution as sample size grows. / 样本均值随样本量增大趋近于正态分布。 |
| Parametric test / 参数检验 | Assumes a specific distribution for the data (usually normal). / 假设数据服从特定分布（通常是正态分布）。 |
| Non-parametric test / 非参数检验 | Makes no distributional assumptions. Works on ranks or signs. / 不做分布假设。基于排名或符号工作。 |
