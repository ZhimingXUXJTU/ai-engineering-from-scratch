# श्रृंखला नियम और स्वचालित अंतरण

> चेन नियम प्रत्येक तंत्रिका नेटवर्क के पीछे इंजन है जो सीखता है।

**Type:** Build | **类型:** 动手
**Language:**पायथन**语言:**पायथन
**Prerequisites:** Phase 1, Lesson 04 (Derivatives & Gradients) | **前置知识:** Phase 1, Lesson 04（导数与梯度）
**Time:** ~90 minutes | **时间:** ~90 分钟

## सीखने के लक्ष्य

- एक न्यूनतम ऑटोग्रेड इंजन (मूल्य वर्ग) का निर्माण करें जो ऑपरेशन रिकॉर्ड करता है और रिवर्स मोड ऑटोडिफ के माध्यम से ग्रेडिएंट्स की गणना करता है
  构建最小化 autograd 引擎(Value 类),记录运算并通过反向模式自动微分计算梯度
- टॉपॉलॉजिकल सॉर्ट का उपयोग करके गणना ग्राफ के माध्यम से आगे और पीछे की ओर गुजरना
  पूर्ववर्ती और विपरीतवर्ती संचरण को प्राप्त करने के लिए
- केवल स्क्रैच से ऑटोग्रेड इंजन का उपयोग करके XOR पर एक बहु-परत perceptron का निर्माण और प्रशिक्षण
   केवल शून्य से प्राप्त ऑटोग्रेड इंजन का उपयोग करके निर्माण और XOR पर प्रशिक्षण बहुस्तरीय संवेदक मशीन
- संख्यात्मक अंतहीन अंतरों के खिलाफ ग्रेडिएंट जांच का उपयोग करके ऑटोडिफ़ सटीकता की जांच करें
  सीमित मूल्य अंतर के साथ स्तर की जांच, सत्यापन ऑटोडिफ की सत्यता

> **【中文解读】**
> 链式法则是"函数套函数的导数怎么算"──神经网络就是几百个函数嵌套在一起:矩阵乘法→加偏置→激活函数→再矩阵乘法→Softmax→交叉──链式法则让你从最后层开始,阶层往返计算每个参数的梯度

> **【拓展：链式法则 → 反向传播 → PyTorch autograd】**
> 链式法则是反向传播 (反向传播)                                                                                                                                                                                                                                                        `autograd`、टेन्सरफ्लो के `GradientTape` ये स्वचालित रूप से अनुवर्ती मॉडल के साथ स्वचालित रूप से घटता है  ये स्वचालित रूप से गणना के नक्शे का पता लगाते हैं, फिर श्रृंखला विधि के साथ सभी तरंगों की गणना करते हैं  आप इस अध्याय में शून्य से अपने स्वयं के ऑटोग्रेड इंजन का निर्माण करेंगे 

## समस्या  समस्या परिचय

आप सरल कार्यों के व्युत्पन्नों की गणना कर सकते हैं। लेकिन एक तंत्रिका नेटवर्क एक सरल कार्य नहीं है। यह एक साथ मिलकर बने सैकड़ों कार्यों का है: मैट्रिक्स गुणा, पूर्वाग्रह जोड़ें, सक्रियण लागू करें, मैट्रिक्स फिर से गुणा करें, सॉफ्टमैक्स, क्रॉस-एंट्रोपी हानि। आउटपुट एक फ़ंक्शन का एक फ़ंक्शन है।

> आप सरल फ़ंक्शन के निर्देशांक की गणना कर सकते हैं। लेकिन तंत्रिका नेटवर्क सरल फ़ंक्शन नहीं है। यह सैकड़ों फ़ंक्शंस का एक जटिल हैः रैंक गुणाकार, अतिरिक्त विकृति, सक्रिय फ़ंक्शन, पुनः रैंक गुणाकार, सॉफ्टमैक्स,交叉 हानि।

नेटवर्क को प्रशिक्षित करने के लिए, आपको प्रत्येक वजन के संबंध में हानि के ग्रेडिएंट की आवश्यकता होती है। लाखों मापदंडों के लिए इसे हाथ से करना असंभव है। इसे संख्यात्मक रूप से करना (सीमित अंतर) बहुत धीमा है।

> नेट को प्रशिक्षित करने के लिए, आपको प्रत्येक वजन के स्तर पर हानि की आवश्यकता है।

श्रृंखला नियम आपको गणित देता है। स्वचालित विभेदन आपको एल्गोरिथ्म देता है। साथ में वे आपको एक एकल आगे के पास के समान समय में कार्यों की मनमाने रचनाओं के माध्यम से सटीक ग्रेडिएंट की गणना करने की अनुमति देते हैं।

> 链式法则 gives mathematics, automatically minuscule gives algorithm── दोनों का संयोजन, आपको एक ही समय में एक ही समय के साथ आगे-आगे प्रसार करने के लिए, किसी भी जटिल फ़ंक्शन की सटीक डिग्री की गणना करने देता है──

यह है कि कैसे PyTorch, TensorFlow, और JAX काम करते हैं. आप खरोंच से एक लघु संस्करण का निर्माण करेंगे.

> यह है PyTorch, TensorFlow और JAX का काम करने का तरीका. आप शून्य से एक माइक्रोटाइप संस्करण का निर्माण करेंगे.

> **【中文解读】**神经网络 = 函数的函数的函数──链式法则让你逐层解解复合函数的导数:dL/dw = dL/d_out × d_out/d_hidden × d_hidden/d_w──自动求导把这个过程自动化PyTorch的`backward()`एक पंक्ति कोड को निर्धारित करो मिलियन पैरामीटर की डिग्री गणना

## अवधारणा का मूल अवधारणा

> **【拓展：自动求导是深度学习的引擎】**पिटॉर्च की `loss.backward()`उपयोग करें विपरीत मोड स्वचालित अनुरोध मार्गदर्शनः से आउटपुट से वापस, चरणबद्ध अनुप्रयोग श्रृंखला विधि।`backward()`एक बार सभी तत्वों के स्तर की गणना कर सकता है। बिना स्वचालित मार्गदर्शन, गहन सीखने के साथ इतने बड़े मॉडल को संसाधित करना असंभव है।

### श्रृंखला नियम

यदि`y = f(g(x))`,  के व्युत्पन्न`y`के संबंध में `x`है:

> यदि `y = f(g(x))`,y से x के लिए निर्देशांक हैः

```
dy/dx = dy/dg * dg/dx = f'(g(x)) * g'(x)
```

श्रृंखला के साथ व्युत्पन्न को गुणा करें। प्रत्येक लिंक अपने स्थानीय व्युत्पन्न में योगदान देता है।

> 沿链路乘导数―― प्रत्येक चरण में योगदान अपनी स्थानीय दिशा-निर्देश संख्या――

उदाहरण: `y = sin(x^2)`

```
g(x) = x^2       g'(x) = 2x
f(g) = sin(g)     f'(g) = cos(g)

dy/dx = cos(x^2) * 2x
```

> उदाहरण: y = sin(x2);;内层 g(x) = x2 的导数是2x,外层 f(g) = sin(g) 的导数是 cos(g),链式相乘:dy/dx = cos(x2) × 2x。

गहरी रचनाओं के लिए, श्रृंखला विस्तारित हैः

```
y = f(g(h(x)))

dy/dx = f'(g(h(x))) * g'(h(x)) * h'(x)
```

> 更深的复合:y = f(g(h(x))),导数为 f'(g(h(x))) × g'(h(x)) × h'(x),每多一层就多乘一项。

न्यूरल नेटवर्क में हर परत इस श्रृंखला में एक कड़ी है।

> तंत्रिका नेटवर्क की प्रत्येक परत इस कड़ी का एक अंग है।

### कम्प्यूटेशनल ग्राफ

एक कम्प्यूटेशनल ग्राफ श्रृंखला नियम को दृश्य बनाता है. प्रत्येक ऑपरेशन नोड बन जाता है. डेटा ग्राफ के माध्यम से आगे बहता है. ग्रेडिएंट पीछे की ओर बहते हैं.

> 計算圖讓链式法则可視化── प्रत्येक क्रिया एक नोड में बदल जाती है, डेटा आगे-पीछे, तरंग-पीछे-पीछे प्रवाह

> 计算图是 PyTorch autograd के निचले स्तर के सारः节点是运算,前向时存储中值,反向时计算局部梯度──

**Forward pass (compute values):**

```mermaid
graph TD
    x1["x1 = 2"] --> mul["* (multiply)"]
    x2["x2 = 3"] --> mul
    mul -->|"a = 6"| add["+ (add)"]
    b["b = 1"] --> add
    add -->|"c = 7"| relu["relu"]
    relu -->|"y = 7"| y["output y"]
```

**Backward pass (compute gradients):**

```mermaid
graph TD
    dy["dy/dy = 1"] -->|"relu'(c)=1 since c>0"| dc["dy/dc = 1"]
    dc -->|"dc/da = 1"| da["dy/da = 1"]
    dc -->|"dc/db = 1"| db["dy/db = 1"]
    da -->|"da/dx1 = x2 = 3"| dx1["dy/dx1 = 3"]
    da -->|"da/dx2 = x1 = 2"| dx2["dy/dx2 = 2"]
```

पिछड़े पास प्रत्येक नोड पर श्रृंखला नियम लागू करता है, आउटपुट से इनपुट तक ग्रेडिएंट को प्रसारित करता है।

> प्रतिवर्ती प्रसार प्रत्येक खंड में प्रयुक्त श्रृंखला विधि के अनुसार, आउटपुट से प्रसारण तक प्रविष्टि तक की तरक्की करेगा।

### आगे की मोड बनाम रिवर्स मोड

एक ग्राफ के माध्यम से श्रृंखला नियम लागू करने के दो तरीके हैं।

> 通过计算图应用链式法则有两种方式──

**Forward mode**इनपुट पर शुरू होता है और डेरिवेटिव आगे धकेलता है। यह गणना करता है`dx/dx = 1`अच्छा है जब आप कम इनपुट और कई आउटपुट है।

> **前向模式**से输入开始向前推进导数―― यह गणना `dx/dx = 1`और प्रत्येक ऑपरेशन के माध्यम से प्रसारित होते हैं।

```
Forward mode: seed dx/dx = 1, propagate forward

  x = 2       (dx/dx = 1)
  a = x^2     (da/dx = 2x = 4)
  y = sin(a)  (dy/dx = cos(a) * da/dx = cos(4) * 4 = -2.615)
```

**Reverse mode**आउटपुट पर शुरू होता है और पीछे की ओर gradients खींचता है. यह गणना करता है`dy/dy = 1`और प्रत्येक ऑपरेशन के माध्यम से विपरीत में प्रसारित. अच्छा जब आप कई इनपुट और कुछ आउटपुट है.

> **反向模式**से आउटपुट शुरू से पीछे पीछे पीछे पीछे की तरफ़।`dy/dy = 1`और प्रत्येक ऑपरेशन के विपरीत, जब अधिक इनपुट होता है, तो कम आउटपुट होता है।

```
Reverse mode: seed dy/dy = 1, propagate backward

  y = sin(a)  (dy/dy = 1)
  a = x^2     (dy/da = cos(a) = cos(4) = -0.654)
  x = 2       (dy/dx = dy/da * da/dx = -0.654 * 4 = -2.615)
```

न्यूरल नेटवर्क में लाखों इनपुट (वेट) और एक आउटपुट (लॉस) होते हैं। रिवर्स मोड एक बैकवर्ड पास में सभी ग्रेडिएंट की गणना करता है। यही कारण है कि बैकप्रॉपेगेशन रिवर्स मोड का उपयोग करता है।

> तंत्रिका नेटवर्क में एक मिलियन इनपुट हैं और एक आउटपुट है। एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार में एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार में एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार में एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार में एक बार एक बार एक बार एक बार एक बार एक बार एक बार एक बार में एक बार एक बार एक बार एक बार एक बार

| Mode | Seed | Direction | Best when |
|------|------|-----------|-----------|
| Forward | `dx_i/dx_i = 1` | Input to output | Few inputs, many outputs |
| Reverse | `dy/dy = 1` | Output to input | Many inputs, few outputs (neural nets) |

> 两种模式对比:前向模式种子 dx/dx = 1,输入到输出,适合少输入多输出;反向模式种子 dy/dy = 1,输出到输入,适合多输入少输出(神经网络)

### आगे के मोड के लिए दोहरे संख्याएँ

आगे के मोड को डबल नंबरों के साथ सुरुचिपूर्ण रूप से लागू किया जा सकता है।`a + b*epsilon`कहाँ`epsilon^2 = 0`. .

> पूर्ववर्ती मोड को प्रतिपद संख्या के रूप में उपयोग किया जा सकता है।`a + b*ε`, उनमें से `ε² = 0`

```
Dual number: (value, derivative)

(2, 1) means: value is 2, derivative w.r.t. x is 1

Arithmetic rules:
  (a, a') + (b, b') = (a+b, a'+b')
  (a, a') * (b, b') = (a*b, a'*b + a*b')
  sin(a, a')         = (sin(a), cos(a)*a')
```

> 导数: 值 导数)  गणितीय नियम:加法对应分量相加;乘法用积的求导法则;sin 用链式法则──把输入的导数种子设为1,导数会自动通过每个运算传播──

इनपुट चर को व्युत्पन्न 1 के साथ बीज करें। प्रत्येक ऑपरेशन के माध्यम से व्युत्पन्न स्वचालित रूप से संवर्धित होता है।

> 1. इनपुट चर के निर्देशांक को प्रत्येक संचरण के माध्यम से स्वचालित रूप से प्रसारित किया जाएगा।

### ऑटोग्राड इंजन बनाना

एक ऑटोग्रेड इंजन तीन चीजों की जरूरत हैः

1. **Value wrapping.**किसी वस्तु में प्रत्येक संख्या को लपेटें जो उसका मूल्य और ग्रेडिएंट संग्रहीत करे।
2. **Graph recording.**प्रत्येक ऑपरेशन में इनपुट और स्थानीय ग्रेडिएंट फ़ंक्शन दर्ज होते हैं।
3. **Backward pass.**ग्राफ को टोपोलॉजिकल क्रमबद्ध करें, फिर इसे उल्टा करें, प्रत्येक नोड पर श्रृंखला नियम लागू करें।

> ऑटोग्राड इंजन को तीन चीजों की आवश्यकता हैः**数值包装**: प्रत्येक संख्या को भंडारण मूल्य और स्तर के वस्तुओं में पैक करें;**图记录**: प्रत्येक ऑपरेशन अपने इनपुट और स्थानीय स्तर फ़ंक्शन को रिकॉर्ड करता है;**反向传播**:拓排序图,反向遍历, प्रत्येक节点应用链式法则──

यह ठीक यही है कि PyTorch है `autograd`है।`torch.Tensor`वर्ग मानों को लपेटता है, जब ऑपरेशन रिकॉर्ड करता है `requires_grad=True`, और गणना gradients जब आप कॉल`.backward()`. .

> यह ठीक है PyTorch की `autograd`कुछ करना है`torch.Tensor`包装数值,当 `requires_grad=True`时记录操作,调用 `.backward()`时计算梯度――

### कैसे PyTorch Autograd हुड के नीचे काम करता है

जब आप PyTorch कोड लिखते हैंः

```python
x = torch.tensor(2.0, requires_grad=True)
y = x ** 2 + 3 * x + 1
y.backward()
print(x.grad)  # 7.0 = 2*x + 3 = 2*2 + 3
```

> जब आप लिखते हैं PyTorch 代码时:x 设 requires_grad=True,运算自动记录,调用倒向() 后 x.grad 自动算出梯度 7.0──

PyTorch आंतरिक रूप सेः

1. एक `Tensor` के लिए नोड`x`के साथ`requires_grad=True`
2. प्रत्येक कार्य (`**`,`*`,`+`) एक नया नोड बनाता है और पीछे की फ़ंक्शन रिकॉर्ड करता है
3. `y.backward()`रिकॉर्ड किए गए ग्राफ के माध्यम से रिवर्स मोड ऑटोडिफ को ट्रिगर करता है
4. प्रत्येक नोड के `grad_fn`स्थानीय ग्रेडिएंट की गणना करता है और उन्हें माता-पिता नोड्स में पारित करता है
5. ग्रेडिएंट्स में जमा होते हैं `.grad`अतिरिक्त (बदला नहीं) के माध्यम से विशेषताएं

> PyTorch 内部:1) 为 x 创建紧张节点;2) 每运算(**、*、+) 创建新节点并记录反向函数;3) y.backward() 触发反向自动微分;4) प्रत्येक节点的 grad_fn 计算局部梯度并传给父节点;5) 梯度通过加法累积到 .grad 属性(不是替代) ]]

ग्राफ गतिशील है (रनिंग-दर-रनिंग) । प्रत्येक आगे के पास पर एक नया ग्राफ बनाया जाता है। यही कारण है कि PyTorch मॉडल के अंदर नियंत्रण प्रवाह (यदि / अन्यथा, लूप) का समर्थन करता है।

> 計算圖是動态的 (~)                                                                                                                                                                                                                                                          

## इसे बनाओ, इसे पूरा करो।
```figure
chain-rule
```

## इसे बनाओ

### चरण 1: मूल्य वर्ग

```python
class Value:
    def __init__(self, data, children=(), op=''):
        self.data = data
        self.grad = 0.0
        self._backward = lambda: None
        self._prev = set(children)
        self._op = op

    def __repr__(self):
        return f"Value(data={self.data:.4f}, grad={self.grad:.4f})"
```

> मूल्य 类是自格的核心数据结构── प्रत्येक मूल्य 存储数值、梯度、反向函数闭包和子节点指针──

हर `Value`यह अपने संख्यात्मक डेटा, उसके ग्रेडिएंट (शुरुआती शून्य), एक पिछड़े फ़ंक्शन को संग्रहीत करता है, और इसे उत्पन्न करने वाले बाल नोड्स को इंगित करता है।

> प्रत्येक `Value` भंडारण संख्या मूल्य、梯度(初始为零)、反向函数和产生它的子节点指针──

### चरण 2: ग्रेडिएंट ट्रैकिंग के साथ अंकगणितीय संचालन

```python
    def __add__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data + other.data, (self, other), '+')
        def _backward():
            self.grad += out.grad
            other.grad += out.grad
        out._backward = _backward
        return out

    def __mul__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data * other.data, (self, other), '*')
        def _backward():
            self.grad += other.data * out.grad
            other.grad += self.data * out.grad
        out._backward = _backward
        return out

    def relu(self):
        out = Value(max(0, self.data), (self,), 'relu')
        def _backward():
            self.grad += (1.0 if out.data > 0 else 0.0) * out.grad
        out._backward = _backward
        return out
```

प्रत्येक ऑपरेशन एक बंद बनाता है जो जानता है कि स्थानीय ग्रेडिएंट की गणना कैसे की जाए और अपस्ट्रीम ग्रेडिएंट से गुणा किया जाए (`out.grad`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `+=`ऐसे मामले को संभालता है जहां एक मान का उपयोग कई ऑपरेशन में किया जाता है।

> प्रत्येक ऑपरेशन एक बंद सेट बनाता है, जानता है कि कैसे गणना करने के लिए स्थानीय स्तर और ऊपर या नीचे की तरफ़।`+=`处理一个值被多个操作使用的情况 (बहुक्रियाओं द्वारा एक मूल्य का उपयोग किया गया)

> 关键设计:加法的反向是1(梯度直接传给两个输入),乘法的反向是另一个操作数(链式法则:d(a*b)/da = b)。relu का反向是0或1(取决于前向是否激活)。

### चरण 3: पीछे की ओर जाने का रास्ता

```python
    def backward(self):
        topo = []
        visited = set()
        def build_topo(v):
            if v not in visited:
                visited.add(v)
                for child in v._prev:
                    build_topo(child)
                topo.append(v)
        build_topo(self)

        self.grad = 1.0
        for v in reversed(topo):
            v._backward()
```

टोपोलॉजिकल सॉर्ट सुनिश्चित करता है कि प्रत्येक नोड का ग्रेडिएंट अपने बच्चों में फैलने से पहले पूरी तरह से गणना की जाए। बीज ग्रेडिएंट 1.0 (डी / डी = 1) है।

> 拓排序 सुनिश्चित करें कि प्रत्येक节 के gradient का प्रसारण से पहले पूर्ण गणना की जाए।

> पीछे की ओर) 算法: पहले पुनः निर्माण करने की प्रक्रिया में शामिल हों, प्रत्येक खंड सभी निर्भरता के बाद दिखाई देता है, फिर प्रत्येक खंड के _पश्चिम में _पश्चिम में_अनुकूलित करें।

### चरण 4: पूर्ण इंजन के लिए अधिक संचालन

मूल मूल्य वर्ग जोड़, गुणा और रील्यू को संभालता है। एक वास्तविक ऑटोग्रेड इंजन को अधिक की आवश्यकता होती है। यहां तंत्रिका नेटवर्क बनाने के लिए आपको जिन कार्यों की आवश्यकता होती है वे हैंः

> 基础 मूल्य वर्ग केवल समर्थन加加、乘、relu── एक वास्तविक ऑटोग्रेड  इंजन को अधिक संचालन की आवश्यकता होती हैः घटा法、、除法、exp、log、tanh──

```python
    def __neg__(self):
        return self * -1

    def __sub__(self, other):
        return self + (-other)

    def __radd__(self, other):
        return self + other

    def __rmul__(self, other):
        return self * other

    def __rsub__(self, other):
        return other + (-self)

    def __pow__(self, n):
        out = Value(self.data ** n, (self,), f'**{n}')
        def _backward():
            self.grad += n * (self.data ** (n - 1)) * out.grad
        out._backward = _backward
        return out

    def __truediv__(self, other):
        return self * (other ** -1) if isinstance(other, Value) else self * (Value(other) ** -1)

    def exp(self):
        import math
        e = math.exp(self.data)
        out = Value(e, (self,), 'exp')
        def _backward():
            self.grad += e * out.grad
        out._backward = _backward
        return out

    def log(self):
        import math
        out = Value(math.log(self.data), (self,), 'log')
        def _backward():
            self.grad += (1.0 / self.data) * out.grad
        out._backward = _backward
        return out

    def tanh(self):
        import math
        t = math.tanh(self.data)
        out = Value(t, (self,), 'tanh')
        def _backward():
            self.grad += (1 - t ** 2) * out.grad
        out._backward = _backward
        return out
```

**Why each operation matters:**

| Operation | Backward rule | Used in |
|-----------|--------------|---------|
| `__sub__` | Reuses add + neg | Loss computation (pred - target) |
| `__pow__` | n * x^(n-1) | Polynomial activations, MSE (error^2) |
| `__truediv__` | Reuses mul + pow(-1) | Normalization, learning rate scaling |
| `exp` | exp(x) * upstream | Softmax, log-likelihood |
| `log` | (1/x) * upstream | Cross-entropy loss, log probabilities |
| `tanh` | (1 - tanh^2) * upstream | Classic activation function |

> विभिन्न संचालन के विपरीत नियम: घटा法 दोहरा उपयोग加法+取负; उपयोग n*x^(n-1);除法 दोहरा उपयोग乘法+(-1);exp उपयोग exp(x) ×上游;log उपयोग (1/x) ×上游;tanh उपयोग (1-tanh2) ×上游。

चतुर भागः `__sub__`और `__truediv__`वे सही ग्रेडिएंट मुफ्त में प्राप्त करते हैं क्योंकि श्रृंखला नियम अंतर्निहित जोड़/मल/पू ऑपरेशन के माध्यम से बना होता है।

> 巧妙之处:`__sub__`和 `__truediv__`                                                                                                                                                                                                                                                              

### चरण 5: स्क्रैच से मिनी एमएलपी

एक पूर्ण मूल्य वर्ग के साथ, आप एक तंत्रिका नेटवर्क का निर्माण कर सकते हैं कोई PyTorch नहीं, कोई NumPy नहीं, केवल मूल्यों और श्रृंखला नियम।

> पूर्ण मूल्य वर्ग के साथ, आप तंत्रिका नेटवर्क का निर्माण कर सकते हैं।

```python
import random

class Neuron:
    def __init__(self, n_inputs):
        self.w = [Value(random.uniform(-1, 1)) for _ in range(n_inputs)]
        self.b = Value(0.0)

    def __call__(self, x):
        act = sum((wi * xi for wi, xi in zip(self.w, x)), self.b)
        return act.tanh()

    def parameters(self):
        return self.w + [self.b]

class Layer:
    def __init__(self, n_inputs, n_outputs):
        self.neurons = [Neuron(n_inputs) for _ in range(n_outputs)]

    def __call__(self, x):
        return [n(x) for n in self.neurons]

    def parameters(self):
        return [p for n in self.neurons for p in n.parameters()]

class MLP:
    def __init__(self, sizes):
        self.layers = [Layer(sizes[i], sizes[i+1]) for i in range(len(sizes)-1)]

    def __call__(self, x):
        for layer in self.layers:
            x = layer(x)
        return x[0] if len(x) == 1 else x

    def parameters(self):
        return [p for layer in self.layers for p in layer.parameters()]
```

ए `Neuron`गणना `tanh(w1*x1 + w2*x2 + ... + b)`.`Layer`न्यूरॉन्स की सूची है।`MLP`प्रत्येक भार एक है`Value`, तो बुला रहा है`loss.backward()`प्रत्येक पैरामीटर के लिए gradients प्रचारित करता है।

> एक `Neuron`计算 `tanh(w1*x1 + w2*x2 + ... + b)` एक `Layer`                                                                                                                                                                                                                                                              `MLP`堆叠多层── प्रत्येक का भार है `Value`, तो调用 `loss.backward()`प्रत्येक तत्व तक तरंग फैल जाएगी।

**Training on XOR:**

> **在 XOR 上训练**:XOR क्लासिक गैर-रेखीय समस्या है, एक स्तरीय संज्ञानात्मक मशीन को हल नहीं किया जा सकता है, कम से कम एक स्तरीय छिपी हुई स्तरीय के साथ करना चाहिए।

```python
random.seed(42)
model = MLP([2, 4, 1])  # 2 inputs, 4 hidden neurons, 1 output

xs = [[0, 0], [0, 1], [1, 0], [1, 1]]
ys = [-1, 1, 1, -1]  # XOR pattern (using -1/1 for tanh)

for step in range(100):
    preds = [model(x) for x in xs]
    loss = sum((p - y) ** 2 for p, y in zip(preds, ys))

    for p in model.parameters():
        p.grad = 0.0
    loss.backward()

    lr = 0.05
    for p in model.parameters():
        p.data -= lr * p.grad

    if step % 20 == 0:
        print(f"step {step:3d}  loss = {loss.data:.4f}")

print("\nPredictions after training:")
for x, y in zip(xs, ys):
    print(f"  input={x}  target={y:2d}  pred={model(x).data:6.3f}")
```

यह माइक्रोग्रेड है. शुद्ध पायथन में पूर्ण तंत्रिका नेटवर्क प्रशिक्षण लूप स्वचालित विभेदन के साथ. हर वाणिज्यिक गहरे सीखने फ्रेमवर्क बड़े पैमाने पर एक ही काम करता है.

> यह है माइक्रोग्रेड। शुद्ध पायथन के साथ पूर्ण तंत्रिका नेटवर्क प्रशिक्षण चक्र और स्वचालित लघु भागों को लागू किया गया है। प्रत्येक व्यावसायिक गहन सीखने के ढांचे ने बड़े पैमाने पर ऐसा ही किया है।

>  प्रशिक्षण चक्र 5 步骤:1) 前向预测;2) 计算损失(MSE);3) 清零所有参数梯度;4) 反向传播;5) 沿梯度负方向更新参数── यही है PyTorch  प्रशिक्षण चक्र का केंद्र──

### चरण 6: ग्रेडिएंट जांच

आप कैसे जानते हैं कि आपका ऑटोडिफ़ सही है? इसे संख्यात्मक व्युत्पन्न के साथ तुलना करें. यह ग्रेडिएंट जांच है।

> 如何知道你的自动驾驶是正确的?

```python
def gradient_check(build_expr, x_val, h=1e-7):
    x = Value(x_val)
    y = build_expr(x)
    y.backward()
    autodiff_grad = x.grad

    y_plus = build_expr(Value(x_val + h)).data
    y_minus = build_expr(Value(x_val - h)).data
    numerical_grad = (y_plus - y_minus) / (2 * h)

    diff = abs(autodiff_grad - numerical_grad)
    return autodiff_grad, numerical_grad, diff
```

इसे एक जटिल अभिव्यक्ति पर परीक्षण करेंः

```python
def expr(x):
    return (x ** 3 + x * 2 + 1).tanh()

ad, num, diff = gradient_check(expr, 0.5)
print(f"Autodiff:  {ad:.8f}")
print(f"Numerical: {num:.8f}")
print(f"Difference: {diff:.2e}")
# Difference should be < 1e-5
```

> 测试复杂表达式:(x3 + 2x + 1) के तन्ह 在 x=0.5 处的梯度── ऑटोडिफ़ 和数值导数的差异应 < 1e-5,验证反向传播实现正确──

नए ऑपरेशन को लागू करते समय ग्रेडिएंट जांच आवश्यक है। यदि आपके बैकवर्ड पास में बग है, तो संख्यात्मक जांच इसे पकड़ती है। विकास के दौरान हर गंभीर गहन सीखने के कार्यान्वयन ग्रेडिएंट जांच चलाता है।

> 梯度检查 नई ऑपरेशन को लागू करने में आवश्यक है। यदि विपरीत दिशा में प्रसारण में कोई बग है, तो संख्यात्मक मूल्य जांच की जा सकती है। प्रत्येक गंभीर गहन सीखने को विकास चरण में सभी चरणों में चलाया जाता है।

**When to use gradient checking:**

| Situation | Do gradient check? |
|-----------|-------------------|
| Adding a new operation to your autograd | Yes, always |
| Debugging a training loop that won't converge | Yes, check gradients first |
| Production training | No, too slow (2x forward passes per parameter) |
| Unit tests for autograd code | Yes, automate it |

> 何時使用梯度检查:给自升加新操作(永远要);调试不收的训练循环(先查梯度);生产训练(不要,太慢);自升单元测试(自动化)

### चरण 7: मैनुअल गणना के खिलाफ सत्यापित करें

```python
x1 = Value(2.0)
x2 = Value(3.0)
a = x1 * x2          # a = 6.0
b = a + Value(1.0)    # b = 7.0
y = b.relu()          # y = 7.0

y.backward()

print(f"y = {y.data}")          # 7.0
print(f"dy/dx1 = {x1.grad}")   # 3.0 (= x2)
print(f"dy/dx2 = {x2.grad}")   # 2.0 (= x1)
```

> 手动验证:y = relu(x1*x2 + 1), चूंकि x1*x2 + 1 = 7 > 0,relu 是恒等映射──dy/dx1 = x2 = 3,dy/dx2 = x1 = 2──引擎计算结果完全匹配──

मैनुअल जांच: `y = relu(x1*x2 + 1)`. . .`x1*x2 + 1 = 7 > 0`, रीलू पहचान है।
`dy/dx1 = x2 = 3`. .`dy/dx2 = x1 = 2`इंजन मेल खाता है.

## इसे फ्रेमवर्क के साथ लागू करें

### PyTorch के खिलाफ जांचें

> तुलना परीक्षण: टर्च के साथ दोहराएँ

```python
import torch

x1 = torch.tensor(2.0, requires_grad=True)
x2 = torch.tensor(3.0, requires_grad=True)
a = x1 * x2
b = a + 1.0
y = torch.relu(b)
y.backward()

print(f"PyTorch dy/dx1 = {x1.grad.item()}")  # 3.0
print(f"PyTorch dy/dx2 = {x2.grad.item()}")  # 2.0
```

आपके इंजन PyTorch के समान परिणाम की गणना करता है क्योंकि गणित एक ही हैः रिवर्स मोड ऑटोडिफ के माध्यम से श्रृंखला नियम.

> समान स्तरों में। आपका इंजन और पाइटॉर्च  ने एक ही परिणाम का अनुमान लगाया है, क्योंकि गणित एक ही हैः श्रृंखला के नियम के माध्यम से विपरीत मोड स्वचालित रूप से सूक्ष्म है।

## इसे भेजें उत्पाद

इस पाठ से उत्पन्न होता हैः
- `outputs/skill-autodiff.md`-- ऑटोग्रेड सिस्टम बनाने और डिबग करने की क्षमता
- `code/autodiff.py`-- एक न्यूनतम ऑटोग्रेड इंजन आप विस्तार कर सकते हैं

> 本课产出: निर्माण एवं调试 ऑटोग्रेड 系统的技能文档 +可扩展的最小 ऑटोग्रेड 引擎代码──

यहाँ निर्मित मूल्य वर्ग चरण 3 में तंत्रिका नेटवर्क प्रशिक्षण लूप के लिए आधार है।

> इस में निर्मित मूल्य वर्ग चरण 3 तंत्रिका नेटवर्क प्रशिक्षण चक्र का आधार है।

### अधिक जटिल अभिव्यक्ति

```python
a = Value(2.0)
b = Value(-3.0)
c = Value(10.0)
f = (a * b + c).relu()  # relu(2*(-3) + 10) = relu(4) = 4

f.backward()
print(f"df/da = {a.grad}")  # -3.0 (= b)
print(f"df/db = {b.grad}")  #  2.0 (= a)
print(f"df/dc = {c.grad}")  #  1.0
```

> 更复杂的表达式:relu(a*b + c) 在 a=2, b=-3, c=10 处, परिणाम है relu(4) = 4──df/da = b = -3,df/db = a = 2,df/dc = 1──

## अभ्यास विषय

1. जोड़ें `__pow__`मान वर्ग में आप गणना कर सकते हैं`x ** n`. . यह सत्यापित करें .`d/dx(x^3)`पर`x=2`बराबर `12.0`. .
   给 मूल्य 类添加 `__pow__`, तुम गणना कर सकते हैं`x ** n`验证 `d/dx(x^3)``x=2`处等于 `12.0`

2. जोड़ें `tanh`एक सक्रियण समारोह के रूप में. यह सत्यापित करें कि`tanh'(0) = 1`और `tanh'(2) = 0.0707`(अंदाजी)
   添加 `tanh`激活函数──验证 `tanh'(0) = 1`,`tanh'(2) ≈ 0.0707`

3. एक ही न्यूरॉन के लिए एक गणना ग्राफ बनाएंः `y = relu(w1*x1 + w2*x2 + b)`सभी पांच ग्रेडिएंट की गणना करें और PyTorch के खिलाफ सत्यापित करें।
   एकल तंत्रिकाओं के लिए गणना का चित्रण`y = relu(w1*x1 + w2*x2 + b)`计算所有五个梯度并与 PyTorch 验证

4. दोहरे संख्याओं का उपयोग करके आगे मोड ऑटोडिफ्लिकेशन लागू करें।`Dual`वर्ग और यह सत्यापित है कि यह आपके रिवर्स मोड इंजन के रूप में एक ही व्युत्पन्न देता है.
   उपयोग करके आंशिक संख्या को प्राप्त करने के लिए पूर्ववर्ती मोड स्वचालित रूप से लघु . . .`Dual`类并验证 यह आपके विपरीत मोड इंजन के समान निर्देशन देता है।

## कीवर्ड्स  शब्द खोज तालिका

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Chain rule | "Multiply the derivatives" | The derivative of composed functions equals the product of each function's local derivative, evaluated at the right point |
| Computational graph | "The network diagram" | A directed acyclic graph where nodes are operations and edges carry values (forward) or gradients (backward) |
| Forward mode | "Push derivatives forward" | Autodiff that propagates derivatives from inputs to outputs. One pass per input variable. |
| Reverse mode | "Backpropagation" | Autodiff that propagates gradients from outputs to inputs. One pass per output variable. |
| Autograd | "Automatic gradients" | A system that records operations on values, builds a graph, and computes exact gradients via the chain rule |
| Dual numbers | "Value plus derivative" | Numbers of the form a + b*epsilon (epsilon^2 = 0) that carry derivative information through arithmetic |
| Topological sort | "Dependency order" | Ordering graph nodes so every node comes after all its dependencies. Required for correct gradient propagation. |
| Gradient accumulation | "Add, don't replace" | When a value feeds into multiple operations, its gradient is the sum of all incoming gradient contributions |
| Dynamic graph | "Define by run" | A computation graph rebuilt on every forward pass, allowing Python control flow inside models (PyTorch style) |
| Gradient checking | "Numerical verification" | Comparing autodiff gradients against numerical finite-difference gradients to verify correctness. Essential for debugging. |
| MLP | "Multi-layer perceptron" | A neural network with one or more hidden layers of neurons. Each neuron computes a weighted sum plus bias, then applies an activation function. |
| Neuron | "Weighted sum + activation" | The basic unit: output = activation(w1*x1 + w2*x2 + ... + b). The weights and bias are learnable parameters. |

> 术语速查:链条 (链式法则) 复合函数导数=各局部导数之积) 计算图,运算为节点的有向无环图) 前行模式 (前向模式,输入到输出传播导数) 逆向模式 (反向模式,输出到输入传播梯度,即反向传播) 自动分系统) 自动微分系统 (PyTorch) 双数 (对偶数 a+bε,前向模式实现) 拓拓拓拓排序,依赖排序排序点) 梯度节积累积,加法不是替代) 动态下行图,前行图 (前行) 梯度检查,激化值与重建机 (前行) 梯度测量,激化值与重建机 (前行) 梯度积累积,加法不是替代) 梯度节积累积,加法证 (前行图) 梯度检查,激化值与重建机 (前行图) 梯度测量和重建机 (前行图) 梯度测量

## आगे पढ़ना 延伸閱讀

- [3Blue1Brown: Backpropagation calculus](https://www.youtube.com/watch?v=tIeHLnjs5U8)-- तंत्रिका नेटवर्क में श्रृंखला नियम की दृश्य व्याख्या
- [PyTorch Autograd mechanics](https://pytorch.org/docs/stable/notes/autograd.html)-- वास्तविक प्रणाली कैसे काम करती है
- [Baydin et al., Automatic Differentiation in Machine Learning: a Survey](https://arxiv.org/abs/1502.05767)-- व्यापक संदर्भ
