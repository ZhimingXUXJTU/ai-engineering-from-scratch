# النماذج المتسلسلة إلى المتسلسلة 序列 إلى序列模型 (seq2Seq)

> اثنان من المترجمين الراغبين في التظاهر بأنّهم مترجمون، والعقدة التي يواجههم هي السبب في وجود الاهتمام.
> اثنين من الـ RNN يظلون مترجمين.

> **【中文解读】**التركيز هو الجهاز الذي تم اختراعه لحل عبوة

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 08 (CNNs + RNNs for Text), Phase 3 · 11 (PyTorch Intro) | **前置知识:** Phase 5 · 08（CNN 和 RNN 文本处理），Phase 3 · 11（PyTorch 入门）
**Time:** ~75 minutes | **时间:** ~75 分钟

## المشكلة المشكلة المشكلة

تصنيف يخطط تسلسل طول متغير إلى علامة واحدة. الترجمة يخطط تسلسل طول متغير إلى تسلسل آخر طول متغير. المدخل والخروج يعيشون في مفردات مختلفة، وربما لغات مختلفة، دون ضمان لموازاة الطول.

> 分类将变长序列映射为单标签──翻译将变长序列映射为另一个变长序列──输入和输出在不同的词表中,可能是不同的语言,长度无法保证一致──

تمكن معماري seq2seq (Sutskever, Vinyals, Le, 2014) من كسر هذا الأمر مع وصفة بسيطة عمداً. اثنين من RNNs. يقرأ أحد الجملة المصدرة ويولد متجهًا سياقيًا ثابتًا. يقرأ الآخر ذلك المتجه ويولد رمز الجملة المستهدفة بواسطة رمز. نفس الرمز الذي كتبته للدرس 08, تم لصقها معاً بشكل مختلف.

> seq2seq 架构(Sutskever, Vinyals, Le, 2014) مع حل حلول بسيطة قصة.

يستحق هذا الدراسة لسببين. أولاً، فإن عنق الزجاجة المتعلقة بالسياق والمتجه هو الفشل الأكثر فائدة من الناحية التربوية في النمط النووي. إنه يحفز كل شيء من الاهتمام والتحولات جيدة في. ثانياً، وصفة التدريب (إجبار المعلم، أخذ العينات المجدولة، البحث عن شعاع عند الاستنتاج) لا تزال تطبق على كل نظام توليد حديث بما في ذلك LLMs.

> هذا يستحق التعلم لهما سببان. أولا، فإن إنجازات الاختبار هي الفشل الأكثر قيمة للتدريس في النمط النووي.

## المفهوم الأساسي

> **【中文解读】**هذا المقطع يعرض المفاهيم والنظريات الأساسية. فهم هذه المفاهيم هو شرط لتحقيق التنفيذ التالي، وكذلك النقاط المعرفة في المقابلة والممارسة التجريبية.

**Encoder.**الـ RNN الذي يقرأ الجملة المصدرة**context vector** ملخص في الحجم الثابت للمدخول بأكمله لا تفقد شيئاً سوى المصدر، على ما يفترض.

> **编码器（Encoder）。**إكتشاف: إكتشاف: إكتشاف: إكتشاف: إكتشاف: إكتشاف: إكتشاف: إكتشاف: إكتشاف: إكتشاف: إكتشاف: إكتشاف: إكتشاف: إكتشاف: إكتشاف: إكتشاف: إكتشاف: إكتشاف: إكتشاف: إكتشاف: إكتشاف: إكتشاف: إكتشاف: إكتشاف: إكتشاف: إكتشاف: إكتشاف: إكتشاف: إكتشاف: إكتشاف: إكتشاف: إكتشاف: إكتشاف: إكتشاف: إكتشاف: إكتشاف: إكتشاف: إكتشاف: إكتشاف: إكتشاف: إكتشاف: إكتشاف: إكتشاف: إكتشاف: إكتشاف: إكتشاف: إكتشاف: إكتشاف: إكتشاف: إكتشاف: إكتشاف: إكتشاف: إكتشاف: إكتشاف: إكتشاف: إكتشاف: إكتشاف: إكتشاف: إكتشاف: إكتشاف: إكتشاف: إكت: إكتشاف: إكت: إكتشاف: إكت: إكت: إكت: إكت: إكت: إكت: إكت: إكت: إكت: إ إكت: إكت: إكت: إ إ إ إكت: إكت: إ إ إكت: إ إ إكت: إكت: إ إ إ إ إ إ إ إ إ إكت: إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ إ**上下文向量**                                                

**Decoder.**يتم تشغيل RNN آخر من متجه السياق. في كل خطوة يأخذ رمزًا تم إنشاؤه مسبقاً كمدخول وينتج توزيعًا على المفردات المستهدفة. عينة أو argmax لتحديد رمز التالي. إعادة إدخاله. كرر حتى `<EOS>`يتم إنتاج الرمز أو يتم ضرب طول أقصى.

> **解码器（Decoder）。**另一个从上下文向量初始化 RNN──在每一步,它将先生成的代币 作为输入,产生目标词表上的分布──采样或取 argmax 选择下一个代币──将其反进进──重复直到产生`<EOS>`أوتو يصل إلى أقصى طول

**Training:**فقدان الإنتروبي المتقاطع في كل خطوة من مراحل إعادة التشغيل، يتم جمعها على التسلسل.

> **训练：**كل خطوة من الخطوات المفصلة، تخسر، في الترتيبات على طلب و.

**Teacher forcing.**أثناء التدريب، مدخلات المقرر في خطوة `t`هو رمز * الحقيقة القاعدية * في الموقف`t-1`لا يتوقع أن يكون هناك أي خطوة أخرى في التنبؤات، وليس التنبؤ السابق للكشف. هذا يثبّت التدريب، وبدون ذلك، تتسلل الأخطاء المبكرة والنموذج لا يتعلم أبداً. عند الاستنتاج، يجب عليك استخدام التنبؤات الخاصة بالنموذج، لذلك هناك دائماً فجوة توزيع القطار/الاضرار.**exposure bias**. . .

> **教师强制（Teacher Forcing）。**التدريبات، والفحوصات في خطوات`t`                                                  `t-1`من* الحقيقي* رمز، وليس المفسر نفسه سابقة التنبؤات. هذا استقر التدريب. بدونها، في مرحلة الخطأ المبكرة، النموذج لا يتعلم أبدا.**暴露偏差（Exposure Bias）**.

**The bottleneck.**كل ما تعلمه المبرمج عن المصدر يجب أن يتم ضغطه في متجه سياق واحد. الجمل الطويلة تفاصيل تفقد. تصبح الكلمات النادرة ضبابية. يجب حفظ إعادة ترتيب (الرداء السوداء مقابل القط الأسود) ، وليس الحساب.

> **瓶颈。**كل ما تعلمته عن المصدر يجب أن يتم ضغطه إلى ذلك على النحو التالي.

الاهتمام (المدرس 10) يصلح هذا عن طريق السماح للكشف للنظر في * كل * كشف مخفي حالة، وليس فقط الأخيرة. وهذا هو الصوت بأكمله.

> الانتباه (١٠) من خلال جعل المُحرّر يشاهد كلّ مُحرّر مخفيّة (١٠) ليس فقط الأخير (١٠) لتحلّل هذه المشكلة.

> **【拓展：大语言模型的工程实践】**من GPT إلى ChatGPT، تمر NLP من "كل مهمة تدريب نموذج" إلى "نموذج حل جميع المهام" التحول النموذجية. في المشاريع العملية، تحتاج نشر LLM إلى النظر في إيقاع الاختيارات التوقيتية التأخير التكلفة والتحقق الأمني وغيرها من المشاكل.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) هي الهيكل الأكثر شعبية في التطبيقات التجارية للذكاء الاصطناعي: سوف يطلب المستخدم أولاً الاختبار المستندات ذات الصلة، ثم يبحث عن نتائج الاختبار كإجابة على الجامعة.

> **【拓展：NLP 的多语言挑战】**في جميع أنحاء العالم هناك 7000 + من اللغات، ولكن دراسة اللغة غير اللغوية تركز بشكل رئيسي على اللغة الإنجليزية وغيرها من اللغات.

## بناء ذلك تحرك لتحقيق

> **【中文解读】**هذا المقطع من خلال الكود من الصفر لتحقيق الخوارزمية النووية. هذا النوع من "من الصفر" يمكن أن يساعد على فهم المبدأ الخلفي للإطار، عندما يواجهون مشكلة لن يتم تعقلها في الصندوق الأسود.
```figure
lstm-gates
```

## بناءها

### الخطوة الأولى: مُشفّر

```python
import torch
import torch.nn as nn


class Encoder(nn.Module):
    def __init__(self, src_vocab_size, embed_dim, hidden_dim):
        super().__init__()
        self.embed = nn.Embedding(src_vocab_size, embed_dim, padding_idx=0)
        self.gru = nn.GRU(embed_dim, hidden_dim, batch_first=True)

    def forward(self, src):
        e = self.embed(src)
        outputs, hidden = self.gru(e)
        return outputs, hidden
```

`outputs`لديه شكل`[batch, seq_len, hidden_dim]` حالة مخفية واحدة لكل موقف مدخل. `hidden`لديه شكل`[1, batch, hidden_dim]` الخطوة الأخيرة. الدروس 08 قالت "مجموعة فوق المخرجات للتصنيف". هنا نحتفظ بالحالة الأخيرة المخفية كمتجه السياق، وتجاهل المخرجات لكل خطوة.

> `outputs`形状为 `[batch, seq_len, hidden_dim]`كل مدخل يحتوي على حالة مخفية`hidden`形状为 `[1, batch, hidden_dim]` 最终步 第08 课说 "في النتائج 上池化做分类"── هنا نحتفظ بالوضع الخفي الأخير كحجم النتائج، ونجاهل الخروج التدريجي.

### الخطوة الثانية: جهاز تشكيل

```python
class Decoder(nn.Module):
    def __init__(self, tgt_vocab_size, embed_dim, hidden_dim):
        super().__init__()
        self.embed = nn.Embedding(tgt_vocab_size, embed_dim, padding_idx=0)
        self.gru = nn.GRU(embed_dim, hidden_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim, tgt_vocab_size)

    def forward(self, token, hidden):
        e = self.embed(token)
        out, hidden = self.gru(e, hidden)
        logits = self.fc(out)
        return logits, hidden
```

يُطلق على المُفكّر خطوة واحدة في كل مرة. المدخل: مجموعة من الرموز الفردية والحالة الخفية الحالية. الخروج: تسجيلات المفردات للرمز التالي والحالة الخفية المحدثة.

> 解码器每次调用步骤──输入:一批单个代币 和当前隐藏状态──输出: 下一个代币的词表 logits 和更新后的隐藏状态──

### الخطوة الثالثة: حلقة تدريبية مع إجبار المعلم

```python
def train_batch(encoder, decoder, src, tgt, bos_id, optimizer, teacher_forcing_ratio=0.9):
    optimizer.zero_grad()
    _, hidden = encoder(src)
    batch_size, tgt_len = tgt.shape
    input_token = torch.full((batch_size, 1), bos_id, dtype=torch.long)
    loss = 0.0
    loss_fn = nn.CrossEntropyLoss(ignore_index=0)

    for t in range(tgt_len):
        logits, hidden = decoder(input_token, hidden)
        step_loss = loss_fn(logits.squeeze(1), tgt[:, t])
        loss += step_loss
        use_teacher = torch.rand(1).item() < teacher_forcing_ratio
        if use_teacher:
            input_token = tgt[:, t].unsqueeze(1)
        else:
            input_token = logits.argmax(dim=-1)

    loss.backward()
    optimizer.step()
    return loss.item() / tgt_len
```

-كلافتان تستحق الإسم`ignore_index=0`يفرط في الخسارة على رموز التشغيل`teacher_forcing_ratio`هو احتمال استخدام الرمز الحقيقي مقابل توقعات النموذج في كل خطوة. تبدأ عند 1.0 (إجبار المعلم الكامل) وتحلل إلى ~ 0.5 على التدريب لتغلق فجوة التحيز التعرض.

> اثنين من العناصر التي تستحق الاهتمام`ignore_index=0`跳过填充代币 上的损失──`teacher_forcing_ratio`يبدأ في كل خطوة من استخدام الرمز الحقيقي مع احتمالية توقعات النموذج.

### الخطوة الرابعة: حلقة الاستنتاج (الحشوة)

```python
@torch.no_grad()
def greedy_decode(encoder, decoder, src, bos_id, eos_id, max_len=50):
    _, hidden = encoder(src)
    batch_size = src.shape[0]
    input_token = torch.full((batch_size, 1), bos_id, dtype=torch.long)
    output_ids = []
    for _ in range(max_len):
        logits, hidden = decoder(input_token, hidden)
        next_token = logits.argmax(dim=-1)
        output_ids.append(next_token)
        input_token = next_token
        if (next_token == eos_id).all():
            break
    return torch.cat(output_ids, dim=1)
```

إنّ التشفير البشع يختار رمزًا ذو أعلى احتمالية في كل خطوة، ويمكن أن يزول بعيداً، بمجرد أن تتعهد بشخصية، لا يمكنك إلغاء إرسالها. **Beam search**يحتفظ بالعلى`k`تسلسل جزئي حي و يختار أعلى نقطة كاملة في النهاية. عرض الشعاع 3-5 هو القياسية.

> 贪心解码 في كل خطوة اختيار أعلى احتمالات رمزية.**束搜索（Beam Search）**保持排名前 `k`في نهاية المجموعة الكاملة من المجموعة المختارة أعلى النقاط.

### الخطوة 5: عقد الزجاجة، تم إثباتها

تدريب النموذج على مهمة نسخ اللعبة: المصدر `[a, b, c, d, e]`، الهدف`[a, b, c, d, e]`. زيد طول التسلسل . لاحظ الدقة

> في تعليميات تعليميات`[a, b, c, d, e]`، هدف `[a, b, c, d, e]` زيادة طول المجموعة  مشاهدة

```
seq_len=5   copy accuracy: 98%
seq_len=10  copy accuracy: 91%
seq_len=20  copy accuracy: 62%
seq_len=40  copy accuracy: 23%
```

ولا يمكن لأحدى الحالات الخفية لـ GRU حفظ مدخل 40 رمزًا دون خسارة. المعلومات موجودة في كل خطوة من مراحل تشفير البرمجة، ولكن المفكّر يرى الحالة الأخيرة فقط.

> 单个GRU 隐藏状态无法无损记忆 40 代币的输入――信息存在在每个编码器步骤中,但解码器只看到最后状态――注意力直接修复了这个问题――

> **【中文解读】**هذا المقال يوضح كيفية استخدام إطار متقدم مثل PyTorch、HuggingFace وغيرها) سريعة تطبيق هذه التقنية.

> **【拓展：Prompt Engineering 与 LLM 应用】**أصبحت الهندسة السريعة مهارات أساسية لمهندسين النمط النووي. من الصفر إلى القليل من الأسلحة، من سلسلة التفكير إلى رد الفعل، تطبق استراتيجيات التفاصيل المختلفة على مختلف المواقف.

## استخدمها في إطار التنفيذ

(بيتورش) لديه`nn.Transformer`و`nn.LSTM`-بناء على نماذج "تقبيل"`transformers`السفن المكتبة كاملة نموذجات تشفير-تشفير (BART، T5، mBART، NLLB) تدرب على مليارات الرموز.

> هناك مشعل`nn.Transformer`و على أساس`nn.LSTM`模板──Hugging Face 的 `transformers`المجموعة المقدمة على مليارات الارقام

```python
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tok = AutoTokenizer.from_pretrained("facebook/bart-base")
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-base")

src = tok("Translate this to French: Hello, how are you?", return_tensors="pt")
out = model.generate(**src, max_new_tokens=50, num_beams=4)
print(tok.decode(out[0], skip_special_tokens=True))
```

أضع المرقم الرقمية الحديثة لتحويلات. الشكل رفيع المستوى (مرقم، مقطع، توليد رموز-ب-رموز) هو نفسه من ورقة 2014 seq2seq. الآلية داخل كل كتلة مختلفة.

> 现代编码器-解码器用变压器 替代了RNN──高层结构(编码器、解码器、个代币 生成) مع 2014seq2seq 论文 تماما نفسها── كل بلاك الجهاز الداخلي مختلفة──

### متى لا يزال هناك متابعة لـ RNN

تقريباً أبداً، بالنسبة للمشاريع الجديدة

> لا يوجد استثناءات محددة للبرامج الجديدة:

- ترجمة التدفق حيث تستهلك إدخال رمز واحد في وقت واحد مع ذاكرة محدودة.
  流式翻译, كل رمز 消耗输入,内存有界──
- إنتاج نص على الجهاز حيث تكلفة ذاكرة المحولات هي مكافئة.
  设备端文本生成,Transformer 内存成本过高──
- التعليم فهم عقدة الرمز التشفير هو أسرع طريق لفهم سبب فوز المحولات
  تعلم. فهم الكودر-فيكورات الكودر.

### تحيز التعرض وتخفيفه

- **Scheduled sampling.**نسبة الإجبار المعلمية خلال التدريب حتى يتعلم النموذج التعافي من أخطائه
  **计划采样（Scheduled Sampling）。** تعويض المعلمين خلال التدريب، دع المعلمين يتعافون من أخطائهم‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬
- **Minimum risk training.**تدرب على درجة الجملة بليو بدلا من التقاطع على مستوى الرمز. أقرب إلى ما تريد حقا.
  **最小风险训练（Minimum Risk Training）。**في الحرفات درجة BLEU 分数 وليس رمزية درجة交叉上训练──更接近你真正想要──
- **Reinforcement learning fine-tuning.**مكافأة مولد التسلسل مع مقياس يستخدم في القانون الحديث RLHF.
  **强化学习微调。**استخدام العلامات التجارية المهنية المهنية

كل هذه الثلاثة لا تزال تنطبق على توليد محول

> هذا ما زال مُطبقًا على إنتاج المحولات القائمة على المحولات

> **【中文解读】**هذا المادة يركز على كيفية نشر النموذج كمنتج متاح. من النموذج الأصلي إلى النظام في مرحلة الإنتاج، تحتاج إلى النظر في العديد من الخصائص في تحسين الأداء والتعامل الخاطئ والتحكم.

## أرسلها .

إبقوا`outputs/prompt-seq2seq-design.md`:

> 保存为 `outputs/prompt-seq2seq-design.md`:

```markdown
---
name: seq2seq-design
description: Design a sequence-to-sequence pipeline for a given task.
phase: 5
lesson: 09
---

Given a task (translation, summarization, paraphrase, question rewrite), output:

1. Architecture. Pretrained transformer encoder-decoder (BART, T5, mBART, NLLB) is the default. RNN-based seq2seq only for specific constraints.
2. Starting checkpoint. Name it (`facebook/bart-base`, `google/flan-t5-base`, `facebook/nllb-200-distilled-600M`). Match the checkpoint to task and language coverage.
3. Decoding strategy. Greedy for deterministic output, beam search (width 4-5) for quality, sampling with temperature for diversity. One sentence justification.
4. One failure mode to verify before shipping. Exposure bias manifests as generation drift on longer outputs; sample 20 outputs at the 90th-percentile length and eyeball.

Refuse to recommend training a seq2seq from scratch for under a million parallel examples. Flag any pipeline that uses greedy decoding for user-facing content as fragile (greedy repeats and loops).
```

> **【中文解读】**练题按照易/中级/Hard 三个难度递进──建议至少完成 级级中级的题目,Hard 级适合深入研究或面试准备──

## تمارين التدريب

1. **Easy.**تنفيذ مهمة نسخ اللعبة. قم بتدريب GRU seq2seq على أزواج المدخلات والخروج حيث يكون الهدف مساوياً للمصدر. قم بتقييم الدقة في أطوال 5, 10, 20. قم بتكرار ضغوط الزجاجة.
   **简单。**实现玩具复制任务──训练 GRU seq2seq 在目标等于源的输入输出对上──测量长度 5、10、20 的准确率──复现瓶──
2. **Medium.**إضافة تشفير البحث عن الشعاع مع عرض الشعاع 3. قياس اللون الأبيض على جسم متوازي صغير ضد الفلسفة. وثيقة تفوز فيها البحث عن الشعاع (عادةً آخر رموز) وأين لا يحدث أي فرق.
   **中等。**添加束宽度为 3的束搜索解码──在小平行语料上测量对贪心的蓝色──记录束搜索在哪里胜出(通常是最后几个代币)以及在哪里没有区别──
3. **Hard.**-حسناً`facebook/bart-base`على مجموعة بيانات تشكيل 10K. مقارنة النموذج المنسق بشكل دقيق مع النموذج الأساسي على المدخلات المحفوظة. تقرير BLEU واختيار 10 أمثلة نوعية.
   **困难。**في 10 000 على المجموعة البيانية`facebook/bart-base`◊ في تركيه إدخال على مقارنة النموذج التغيرات الصغيرة 4  الخروج مع النموذج الأساسي ◊ تقرير BLEU ومجموعة 10 أمثلة ذاتية ◊

> **【中文解读】**في لغة "ما يقوله الناس" مقابل "ما يعنيه في الواقع" تم التمييز بين لغة اليومية والتقنية المحددة.

## شروط الرئيسية

| Term / 术语 | What people say / 人们常说的 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| Encoder（编码器） | Input RNN / 输入 RNN | Reads source. Produces per-step hidden states and a final context vector. / 读取源。产生逐步隐藏状态和最终上下文向量。 |
| Decoder（解码器） | Output RNN / 输出 RNN | Initialized from context vector. Generates target tokens one at a time. / 从上下文向量初始化。逐个生成目标 token。 |
| Context vector（上下文向量） | The summary / 摘要 | Final encoder hidden state. Fixed size. The bottleneck attention solves. / 最终编码器隐藏状态。固定大小。注意力解决的瓶颈。 |
| Teacher forcing（教师强制） | Use true tokens / 使用真实 token | Feed the ground-truth previous token at training time. Stabilizes learning. / 训练时馈入真实的前一个 token。稳定学习。 |
| Exposure bias（暴露偏差） | Train/test gap / 训练/测试差距 | Model trained on true tokens never practiced recovering from its own mistakes. / 在真实 token 上训练的模型从未练习从自己的错误中恢复。 |
| Beam search（束搜索） | Better decoding / 更好的解码 | Keep top-k partial sequences alive at each step instead of committing greedily. / 每步保持排名前 k 的部分序列存活，而非贪心提交。 |

> **【中文解读】**延伸阅读 يوفر موارد عالية الجودة للتعلم المتعمق.

## المزيد من القراءة

- [Sutskever, Vinyals, Le (2014). Sequence to Sequence Learning with Neural Networks](https://arxiv.org/abs/1409.3215) ورقة الساق الثانية الأصلية. أربعة صفحات. / 原始 seq2seq 论文──四页──
- [Cho et al. (2014). Learning Phrase Representations using RNN Encoder-Decoder for Statistical Machine Translation](https://arxiv.org/abs/1406.1078) أدخل GRU والإطار المُشفّر-المُفَكّر. / 引入 GRU 和编码器-解码器框架──
- [Bahdanau, Cho, Bengio (2014). Neural Machine Translation by Jointly Learning to Align and Translate](https://arxiv.org/abs/1409.0473) ورقة الاهتمام. اقرأ فورا بعد هذا الدروس. / 注意力论文──在本课后立即阅读──
- [PyTorch NLP from Scratch tutorial](https://pytorch.org/tutorials/intermediate/seq2seq_translation_tutorial.html) بناء seq2seq + الرمز الاهتمام. / 可构建的 seq2seq + 注意力代码。
