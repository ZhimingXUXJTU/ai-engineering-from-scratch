# CNN ve RNN'ler için metin

> Değişiklikler n-gram öğrenir. Tekrarlıklar hatırlanır. İkisi de dikkatle değiştirilmiştir. İkisi de sınırlı donanımlarda hala önemlidir.
> 卷积学习 n-gram。循环负责记忆──都被注意力机取代──但在限硬件上仍然重要──

> **【中文解读】**CNN 捕捉局部 n-gram 特征,RNN 处理长程依赖──Transformer 之前的主流架构──

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 3 · 11 (PyTorch Intro), Phase 5 · 03 (Word Embeddings), Phase 4 · 02 (Convolutions from Scratch) | **前置知识:** Phase 3 · 11（PyTorch 入门），Phase 5 · 03（词嵌入），Phase 4 · 02（从零实现卷积）
**Time:** ~75 minutes | **时间:** ~75 分钟

## Sorunlar. Sorunlar.

TF-IDF ve Word2Vec, kelime sırasını görmezden gelen düz vektörler üretti.`dog bites man`-`man bites dog`Bazen kelime sırası sinyal taşır.

> TF-IDF ve Word2Vec                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     `dog bites man`和 `man bites dog`                                                                                                                                                                                                                                                              

Transformatörler gelmeden önce iki mimarlık ailesi bu boşluğu doldurdu.

> Transformer ortaya çıkmadan önce iki ırkın yapıları boşluğu doldurdu.

**Convolutional nets for text (TextCNN).**1D sarmalamaları kelimelerinin sekanslarına uygulayın. Genişliği 3 olan bir filtre öğrenilebilir bir trigram algılayıcısıdır: üç kelimeyi kapsar ve bir puan çıkarır. Çok ölçekli desenleri algılamak için farklı genişlikler (2, 3, 4, 5) yığın. Max-pool sabit boyutlu bir temsil. Düz, paralel, hızlı.

> **文本卷积网络（TextCNN）。**Bir kelimenin yerleştirilmesi dizisinde uygulanır bir boyut yuvarlaklıklı. 波器 for 3'lik boyutlu bir 波器 is a learning trio group tester: it crosses three words and outputs fractional numbers.

**Recurrent nets (RNN, LSTM, GRU).**İşlem simgelerini bir seferde, bilgiyi ileriye taşıyan gizli bir durum koruyarak. Sequential, bellek taşıyan, esnek giriş uzunlukları. 2014'ten 2017'ye kadar baskın sıra modeliştirme, sonra dikkat oldu.

> **循环网络（RNN、LSTM、GRU）。**个个处理 token,维护向前传递信息的隐藏状态――顺序、有记忆、灵活输入长度── 2014-2017 yılları arasında yönetici dizi oluşturuldu, sonra dikkat mekanizması ortaya çıktı──

Bu ders her ikisini de geliştirir, sonra dikkat çeken başarısızlığı isimlendirir.

> Bu ders, iki yönü oluşturur ve dikkatli hareketlerin başarısız olduğunu belirtir.

## Konsepten bir şey.

> **【中文解读】**Bu bölümde temel kavramlar ve teoriler hakkında konuşuluyor. Bu kavramları öğrenmek, sonradan gerçekleştirilme önemi, aynı zamanda, görüşmeler ve mühendislik uygulamalarında yüksek sıklıkta yapılan incelemelerin bilgi noktasıdır.

**TextCNN**Tokenler yerleştirilmiştir.`k`1D kıvrım bir filtreyi ardıcıl olarak kaydırır `k`-gramlar yerleştirilmiş, özellik haritası üreten. bu haritada global maksimum birleştirme en güçlü etkinliği seçer.

> **TextCNN**(Kim, 2014) ◊ Token ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅                                                                                                                                                                                                                                                             `k`Bir de devamlı bir süreç.`k`-gram 嵌入上滑波器,产生特征图――对该特征图做全局最大池化选择最强的激活――多个波器宽度最大池化输出拼接――送入分类器头――

Filtrenin çalışması neden önemlidir. Bir filtre öğrenilebilir bir n-gramdır. Maksimum birleştirme pozisyon değişikliğidir, bu nedenle "iyi değil" bir incelemenin başında veya ortasında aynı özelliği ateşler. Her biri 100 filtre ile üç filtre genişliği size 300 öğrenilmiş n-gram detektörü verir. Eğitim paraleldir; sıralı bağımlılık yoktur.

> Neden geçerli? 波器 is learning n-gramı。 en büyük miktarı konum değişmez, bu yüzden "iyi değil" olarak yorumlarda ilk veya orta 触发 aynı özellikleri。 üç 波器 genişliği her 100 波器 size 300 波器 检测器  波器  波器  波器  波器  波器  波器  波器  波器  波器  波器  波器  波器  波器  波器  波器  波器  波器  波器  波器  波器  波器 波器 波器 波器 波器 波器 波器 波器 波器 波器 波器 波器 波器 波器 波器 波器 波器 波器 波器 波器 波器 波器 波器 波器 波器 波器 波器 波器 波器 波器 波器 波器 波器 波器 波器 波器 波器 波器 波器 波器 波器 波器 波器 波器 波器 波器 波器 波器 波器 波器 波器 波器 波器 波器 波器 波器 波器 波器 波器 波器 波器 波器 波器 波器 波器 波器 波器 波器 波器 波器 波器 波器 波器 波器 波器 波器 波器 波器 波 波 波器 波 波 波器 波器 波器 波 波 波 器 波 波器 波器 波 波器 器 波 波 器 波 波 器 器 器 器 器 器 器 器 器 器 器 器 器 器 器 器 器 器 器 器 器 器 器 器 器 器 器 器 

**RNN.**Her adımda .`t`, gizli durum .`h_t = f(W * x_t + U * h_{t-1} + b)`Paylaşın .`W`- Evet .`U`- Evet .`b`Zamanın içinde gizli bir durum.`T`sınıflandırma için, bir araya getirmek `h_1 ... h_T`(maksimum, ortalama veya son).

> **RNN。**Her zamanki adım.`t`Gizli durum .`h_t = f(W * x_t + U * h_{t-1} + b)`- Evet.`W`- Evet.`U`- Evet.`b`跨时间共享──时间 `T`Bu, tüm bölümlerin özetini oluşturur.`h_1 ... h_T`Ü池化 (最大、平均值, or final)

Basit RNN'ler kaybolan eğriliklere sahiptir.**LSTM**Neyi unutmaya, neyi saklamaya ve neyi çıkaracak karar veren kapılar ekler.**GRU**LSTM'yi iki kapıya basitleştirir; daha az parametrelerle benzer şekilde çalışır.

> Normal RNN                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          **LSTM**添加决定忘了什么,储存什么,输出什么的门,稳定长序列的梯度.**GRU**LSTM'yi iki kapıya basitleştirmek; parametreler daha az ama sonuçlar benzer.

**Bidirectional RNNs**RNN'nin birini ileriye, birini geriye, gizli durumları birleştirerek çalıştırın.

> **双向 RNN**运行一个RNN向前、另一个向后,拼接隐藏状态──每个代币的表示看左右两侧的上下文──对标注任务必不可少──

> **【拓展：大语言模型的工程实践】**GPT'den ChatGPT'e kadar, NLP alanında "her görev bir model eğitimi" ile "her görevyi çözmek için bir model" biçiminin değişiminden geçti.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) şu anki işletme AI 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用  应用 应用 应用    应用     应用   应用        应用    应用       应用          应用        应用      应用          应用                                                                                                       

> **【拓展：NLP 的多语言挑战】**Küresel olarak 7000'den fazla dil vardır, ancak NLP çalışmaları çoğunlukla İngilizce ve az sayıda dil üzerinde yoğunlaşmaktadır.

## Yapın.

> **【中文解读】**Bu bölüm kodla sıfırdan gerçekleştirilen çekirdek algoritmasıdır. Bu "sıfırdan" yöntem çerçevenin arkasındaki prensipleri anlama yardımcı olur.
```figure
rnn-unroll
```

## Yapın

### Adım 1: PyTorch'te TextCNN

```python
import torch
import torch.nn as nn
import torch.nn.functional as F


class TextCNN(nn.Module):
    def __init__(self, vocab_size, embed_dim, n_classes, filter_widths=(2, 3, 4), n_filters=64, dropout=0.3):
        super().__init__()
        self.embed = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
        self.convs = nn.ModuleList([
            nn.Conv1d(embed_dim, n_filters, kernel_size=k)
            for k in filter_widths
        ])
        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(n_filters * len(filter_widths), n_classes)

    def forward(self, token_ids):
        x = self.embed(token_ids).transpose(1, 2)
        pooled = []
        for conv in self.convs:
            c = F.relu(conv(x))
            p = F.max_pool1d(c, c.size(2)).squeeze(2)
            pooled.append(p)
        h = torch.cat(pooled, dim=1)
        return self.fc(self.dropout(h))
```

- Evet .`transpose(1, 2)`yeniden şekillendirilmesi`[batch, seq_len, embed_dim]`- ...`[batch, embed_dim, seq_len]`Çünkü ...`nn.Conv1d`Orta ekseni kanal olarak değerlendirir.

> `transpose(1, 2)`- Ben de .`[batch, seq_len, embed_dim]`Şıklık`[batch, embed_dim, seq_len]`Çünkü ...`nn.Conv1d`Orta aksellerin geçiş yolu olarak görüldüğü için, giriş uzunluğunun ne olursa olsun, bir yığının ardından çıkışlar sabit büyüklükte olacaktır.

### Adım 2: LSTM sınıflandırıcısı

```python
class LSTMClassifier(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_dim, n_classes, bidirectional=True, dropout=0.3):
        super().__init__()
        self.embed = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
        self.lstm = nn.LSTM(embed_dim, hidden_dim, batch_first=True, bidirectional=bidirectional)
        factor = 2 if bidirectional else 1
        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(hidden_dim * factor, n_classes)

    def forward(self, token_ids):
        x = self.embed(token_ids)
        out, _ = self.lstm(x)
        pooled = out.max(dim=1).values
        return self.fc(self.dropout(pooled))
```

Klassifleştirme için, maksimum birleştirme genellikle son gizli durumu almayı yener çünkü uzun bir dizi sonunda bilgi son durumu ele geçirmektedir.

> Sıralarda son durumun bir araya gelmesi yerine, dizi üzerinde en büyük bir bir araya gelme yapılır.

### Adım 3: kaybolan gradient demo (intuition)

Kapalı olmayan basit bir RNN uzun mesafeli bağımlılıkları öğrenemez.`A`Bir dizi içinde herhangi bir yerde ortaya çıktı.`A`Eğer 1 pozisyonunda ve dizisi 100 token uzunluğunda ise kayıptan gelen gradient tekrarlayan ağırlığın 99 katından geri akmalı. Eğer ağırlık 1'den azsa, gradient ortadan kaybolur. 1'den fazlasa patlar.

> 没有门控的普通 RNN 无法学习长程依赖――考虑一个玩具任务:预测 token `A`Eğer bu sırada herhangi bir yerde bulunmuyorsa.`A`1, dizinin uzunluğu 100'e kadar ise, kayıp derecesi 99 kez döngülürken ağırlığın çarpı geri akışı geçmelidir. Eğer ağırlık 1'den küçükse, derecesi kaybolur.

```python
def vanishing_gradient_sim(seq_len, recurrent_weight=0.9):
    import math
    return math.pow(recurrent_weight, seq_len)


# At weight=0.9 over 100 steps:
#   0.9 ^ 100 ≈ 2.7e-5
# The gradient from step 100 to step 1 is effectively zero.
```

LSTM'ler bunu bir **cell state**Bu, sadece katılımlı etkileşimlerle ağın üzerinden geçer (gözgeçit onu çoğaltır, ancak gradientler hala "yolu" boyunca akıyor).

> LSTM                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            **细胞状态**Bu sorunu düzeltti, bu durum sadece ağın üzerinden geçen iletişimlerin artması ile gerçekleşmiştir. Bu da bir hızla hızla hızla hızla hızla hızla hızla hızla hızla hızla hızla hızla hızla hızla hızla hızla hızla hızla hızla hızla hızla hızla hızla hızla hızla hızla hızla hızla hızla hızla hızla hızla hızla hızla hızla hızla hızla hızla hızla hızla hızla hızla hızla hızla hızla hızla hızla hızla hızla hızla hızla hızla hızla hızla hızla hızla hızla hızla hızla hızla hızla hızla hızla hızla hızla hızla hızla hızla hızla hızla hızla hızla hızla hızla hızla hızlandırıyor.

### Dördüncü adım: Neden bu yeterli değildi?

LSTM'ler ile bile üç sorun devam etti.

> LSTM bile olsa, üç sorun devam ediyor.

1. **Sequential bottleneck.**1000 uzunluklı bir dizide bir RNN'yi eğitmek 1000 seri ileri/geri adım gerektirir.
   **顺序瓶颈。**1000'e kadar uzun bir dizi üzerinde eğitim almak için RNN'ye 1000'den fazla doğru/karşı yönlü adım gerekmektedir.
2. **Fixed-size context vector in encoder-decoder setups.**Dekoder, tüm giriş üzerinde sıkıştırılmış, sadece enkoderin son gizli durumunu görür. Uzun girişler ayrıntıları kaybeder. 09 ders bunu doğrudan kapsar.
   **编码器-解码器中的固定大小上下文向量。**解码器 yalnızca 编码器'ın son gizli durumunu görür, tüm girişleri sıkıştırır.
3. **Distant-dependency accuracy ceiling.**LSTM'ler sıradan RNN'lerden daha iyi performans gösterir, ancak hala 200'den fazla aşamada belirli bilgileri yaymak için mücadele ederler.
   **远距离依赖准确率天花板。**LSTM                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            

Dikkat üçünü de çözdü. Transformatörler tekrarlanmayı tamamen düşürdü.

> Dikkat, tüm üç sorunu çözdü. Transformer tamamen döngüden vazgeçti.

> **【中文解读】**Bu bölümde, PyTorch, HuggingFace gibi olgun çerçeveler nasıl kullanılacağını gösterir.

> **【拓展：Prompt Engineering 与 LLM 应用】**Hızlı Mühendislik NLP mühendislerinin temel beceri haline geldi. Zero-shot'tan birkaç-shot'a, Chain-of-Thought'tan ReAct'e kadar, farklı fikir stratejileri farklı durumlarda uygulanmaktadır.

## Çerçeveyi kullanın.

PyTorch'in `nn.LSTM`- Evet .`nn.GRU`ve`nn.Conv1d`Eğitim kodu standart.

> PyTorch'in `nn.LSTM`- Evet.`nn.GRU`和 `nn.Conv1d`Bu, bir eğitim kuralıdır.

Yüz gemileri, giriş katmanı olarak bağladığınız önceden eğitilmiş yerleşimler:

> Öğünmüş Yüz 提供预训嵌入作为输入层插入:

```python
from transformers import AutoModel

encoder = AutoModel.from_pretrained("bert-base-uncased")
for param in encoder.parameters():
    param.requires_grad = False


class BertCNN(nn.Module):
    def __init__(self, n_classes, filter_widths=(2, 3, 4), n_filters=64):
        super().__init__()
        self.encoder = encoder
        self.convs = nn.ModuleList([nn.Conv1d(768, n_filters, kernel_size=k) for k in filter_widths])
        self.fc = nn.Linear(n_filters * len(filter_widths), n_classes)

    def forward(self, input_ids, attention_mask):
        with torch.no_grad():
            out = self.encoder(input_ids=input_ids, attention_mask=attention_mask).last_hidden_state
        x = out.transpose(1, 2)
        pooled = [F.max_pool1d(F.relu(conv(x)), kernel_size=conv(x).size(2)).squeeze(2) for conv in self.convs]
        return self.fc(torch.cat(pooled, dim=1))
```

Kullanım-ne zaman-it-fits-the-restriction kontrol listesi.

> 适用约束检查清单──

- **Edge / on-device inference.**TextCNN'in GloVe yerleştirmeleri bir transformatörden 10-100 kat daha küçüktür.
  **边缘/设备端推理。**带 GloVe 嵌入的 TextCNN 比 Transformer 小 10-100 倍──如果部署目标是手机,这就是你的技术──
- **Streaming / online classification.**RNN bir seferde bir token işliyor; transformörlerin tam sıraya ihtiyacı var. Gerçek zamanlı gelen metin için LSTM'ler hala kazanıyor.
  **流式/在线分类。**RNN Her kez bir token işlenmesi;Transformer  needs complete序列──
- **Tiny models for baselines.**Yeni bir görev için hızlı tekrarlama.
  **用于基线的微型模型。**Yeni görevlerde hızlı bir şekilde çalışmak.
- **Sequence labeling with limited data.**BiLSTM-CRF (dersi 06) hala 1k-10k etiketli cümleler için üretim derecesi NER mimarisi.
  **数据有限的序列标注。**BiLSTM-CRF (第 06 课) 1k-10k için 标注句子仍然是生产级 NER 架构──

Diğer her şey bir transformatöre gidiyor.

> Diğer her şey Transformer'la.

> **【中文解读】**Bu bölümde modellerin kullanılabilir ürünler için nasıl dağıtılacağı üzerinde yoğunlaşmaktadır.

## İndirin . Ürünler .

- Kaydet .`outputs/prompt-text-encoder-picker.md`- ...

> 保存为 `outputs/prompt-text-encoder-picker.md`- ...

```markdown
---
name: text-encoder-picker
description: Pick a text encoder architecture for a given constraint set.
phase: 5
lesson: 08
---

Given constraints (task, data volume, latency budget, deploy target, compute budget), output:

1. Encoder architecture: TextCNN, BiLSTM, BiLSTM-CRF, transformer fine-tune, or "use a pretrained transformer as a frozen encoder + small head".
2. Embedding input: random init, GloVe / fastText frozen, or contextualized transformer embeddings.
3. Training recipe in 5 lines: optimizer, learning rate, batch size, epochs, regularization.
4. One monitoring signal. For RNN/CNN models: attention mechanism absence means they miss long-range deps; check per-length accuracy. For transformers: fine-tuning collapse if LR too high; check train loss.

Refuse to recommend fine-tuning a transformer when data is under ~500 labeled examples without showing that a TextCNN / BiLSTM baseline has plateaued. Flag edge deployment as needing architecture-before-everything.
```

> **【中文解读】**练习题按照易/中级/难三度递进;;建议至少完成中级题,Hard级适合深入研究或面试准备;;

## Egzersizler.

1. **Easy.**Bir TextCNN'i 3 sınıf oyuncak verisi kümesi üzerinde eğit (verileri icat ettin). Filtr genişliğinin (2, 3, 4) ortalama F1'den tek bir genişliğe (3) daha yüksek olduğunu kontrol edin.
   **简单。**Bir 3 sınıf oyuncak verileri üzerinde eğitim TextCNN((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((
2. **Medium.**LSTM sınıflandırıcısı için maksimum, ortalama ve son durum birleştirmesini uygulayın. Küçük bir veri kümesi üzerinde karşılaştırın; birleştirmenin hangi belgeyi kazanmış olduğunu ve neden olduğunu varsayın.
   **中等。**LSTM sınıflandırma makinesi en büyük bir birleştirme ̇ ortalama birleştirme ve son birleştirme yapmaktadır.
3. **Hard.**BiLSTM-CRF NER etiketini oluşturun (bütün ders 06 ve bu birleştirin). CoNLL-2003'te eğitim alın.
   **困难。**BiLSTM-CRF NER 标志器ı oluşturmak için.

> **【中文解读】**术语表中的"İnsanların ne dediği" vs "Gerçekten ne anlama geldiği" 区分日常口语和精确技术含义──在团队协作中,统一术语定义可以避免大量沟通误解──

## Anahtar Şartlar .

| Term / 术语 | What people say / 人们常说的 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| TextCNN | CNN for text / 文本 CNN | Stack of 1D convolutions over word embeddings with global max-pool. Kim (2014). / 在词嵌入上堆叠一维卷积加全局最大池化。Kim (2014)。 |
| RNN（循环神经网络） | Recurrent net / 循环网络 | Hidden state updated at each time step: `h_t = f(W x_t + U h_{t-1})`. / 每个时间步更新隐藏状态：`h_t = f(W x_t + U h_{t-1})`。 |
| LSTM | Gated RNN / 门控 RNN | Adds input / forget / output gates + a cell state. Trains stably through long sequences. / 添加输入/遗忘/输出门 + 细胞状态。在长序列上稳定训练。 |
| GRU | Simpler LSTM / 更简单的 LSTM | Two gates instead of three. Similar accuracy, fewer parameters. / 两个门代替三个。类似准确率，更少参数。 |
| Bidirectional（双向） | Both directions / 两个方向 | Forward + backward RNN concatenated. Every token sees both sides of its context. / 前向 + 后向 RNN 拼接。每个 token 看到其上下文两侧。 |
| Vanishing gradient（梯度消失） | Training signal dies / 训练信号消失 | Repeated multiplication by <1 weights in plain RNNs makes early-step gradients effectively zero. / 普通 RNN 中对小于 1 的权重反复乘法使早期步骤的梯度实际上为零。 |

> **【中文解读】**延伸阅读, derinlemesine öğrenme için yüksek kaliteli kaynaklar sağladı. Bu makaleler ve dersler, derinlemesine anlama ihtiyacı olan okuyuculara uygun olarak bu alanın klasik referanslarıdır.

## Daha fazla okumak

- [Kim, Y. (2014). Convolutional Neural Networks for Sentence Classification](https://arxiv.org/abs/1408.5882) TextCNN makalesi. Sekiz sayfa. Okuyabilir. / TextCNN 论文──八页──易读──
- [Hochreiter, S. and Schmidhuber, J. (1997). Long Short-Term Memory](https://www.bioinf.jku.at/publications/older/2604.pdf) LSTM kağıdı. Beklenmedik derecede açık. / LSTM 论文──出乎意料地清晰──
- [Olah, C. (2015). Understanding LSTM Networks](https://colah.github.io/posts/2015-08-Understanding-LSTMs/) LSTM'leri herkese erişilebilir kılan şablonlar. /  LSTM'yi herkese anlaşılabilir bir şekilde oluşturun.
