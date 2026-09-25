# Sıradan sıraya Modeller.

> İki RNN tercüman numarası yapıyor.
> İki RNN 假装是翻译器──它们遇到的瓶正是注意力机的存在的原因──

> **【中文解读】**编码器-解码器架构──注意力机制就是为了解决它的瓶而发明的──

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 08 (CNNs + RNNs for Text), Phase 3 · 11 (PyTorch Intro) | **前置知识:** Phase 5 · 08（CNN 和 RNN 文本处理），Phase 3 · 11（PyTorch 入门）
**Time:** ~75 minutes | **时间:** ~75 分钟

## Sorunlar. Sorunlar.

Sınıflandırma, değişken uzunluklı bir diziyi tek bir etiketle haritası yapar. Çevirme, değişken uzunluklı bir diziyi başka değişken uzunluklı bir diziye haritası yapar. Giriş ve çıkış, uzunluk paritesi garantisi olmadan farklı kelime kitaplarında, muhtemelen farklı dillerde yaşar.

> 分类将变长序列映射为单标. 译文将变长序列映射为另一个变长序列. 译文将变长序列映射为另一个变长序列. 译文将变长序列映射为另一个变长序列. 译文将变长序列映射为另一个变长序列. 译文将变长序列映射为另一个变长序列. 译文将变长序列映射为另一个变长序列. 译文: 译文: 译文: 译文: 译文: 译文: 译文: 译文: 译文: 译文: 译文: 译文: 译文: 译文: 译文: 译文: 译文: 译文: 译文: 译文: 译文: 译文: 译文: 译文: 译文: 译文: 译文: 译文: 译文: 译文: 译: 译: 译: 译: 译: 译: 译: 译: 译: 译: 译: 译: 译: 译: 译: 译: 译: 译: 译: 译: 译: 译: 译: 译: 译: 译: 译: 译: 译: 译: 译: 译: 译: 译: 译: 译: 译: 译: 译: 译: 译: 译: 译: 译: 译: 译: 译: 译: 译: 译: 译: 译: 译: 译: 译: 译: 译: 译: 译: 译: 译: 译: 译: 译: 译: 译: 译: 译: 译: 译: 译: 译: 译: 译: 译: 译: 译: 译: 译: 译: 译: 译: 译: 译: 译: 译: 译: 译: 译: 译

Seq2seq mimarisi (Sutskever, Vinyals, Le, 2014) bunu kasıtlı bir basit bir tarifle çözdü. İki RNN. Biri kaynak cümleyi okuyor ve sabit boyutlu bir bağlam vektörü üretir. Diğeri bu vektörü okuyor ve hedef cümle tokeni tokeni oluşturur. Ders 08, farklı bir şekilde yapıştırılmış olarak yazdığınız aynı kod.

> Seq2seq 架构(Sutskever, Vinyals, Le, 2014) bir tasarlanmış basit çözümle bu sorunu çözdü.

Bu iki nedenden ötürü çalışmaya değer. Birincisi, bağlam vektör boğazı NLP'de en pedağolojik açıdan yararlı başarısızlıktır. Dikkat ve transformatörlerin iyi olduğu her şeyi motive eder. İkincisi, eğitim tarifi (öğretmen zorlaması, planlı örnekleme, sonucu üzerinde ışın araştırması) LLM'ler dahil olmak üzere tüm modern nesil sistemlerine hala uygulanır.

> Bu öğrenmeye değer iki nedenle. Birincisi, NLP'de en çok öğretim değerinin başarısız olmasıdır.

## Konsepten bir şey.

> **【中文解读】**Bu bölümde temel kavramlar ve teoriler hakkında konuşuluyor. Bu kavramları öğrenmek, sonradan gerçekleştirilme önemi, aynı zamanda, görüşmeler ve mühendislik uygulamalarında yüksek sıklıkta yapılan incelemelerin bilgi noktasıdır.

**Encoder.**Kaynak cümlesini okuyan bir RNN. Son gizli durumunda**context vector** tüm girişlerin sabit boyutlu bir özet. Kaynaktan başka bir şey kaybetme.

> **编码器（Encoder）。**Bir okuyucu cümleyi RNN---sonunda gizli durum**上下文向量**                                                                                                                                                                                                                                                              

**Decoder.**Diğer bir RNN bağlam vektöründen başlatılır. Her adımda daha önce üretilen token'ı giriş olarak alır ve hedef sözlük üzerinde bir dağılım üretir.`<EOS>`Token üretilir veya maksimum uzunluk vurulur.

> **解码器（Decoder）。**另一个从上下文向量初始化的 RNN──在每一步,它将先生成的代币 作为输入,产生目标词表上的分布──采样或取 argmax 选择下一个代币──将其反进进──重复直到产生`<EOS>`Token veya maksimum uzunluğa ulaşmak için.

**Training:**Her dekoder adımında çapraz entropi kaybı, sırada toplamda.

> **训练：**Her çözücü adımın geçiş kaybı, iki ağın standart zamanın karşı yönünde yayılması.

**Teacher forcing.**Eğitim sırasında, dekodörün girişleri adım adım `t`konumdaki * temel gerçeklik* simgesi`t-1`Bu eğitimleri istikrarlandırır; bu olmadan erken hatalar kaskadaya düşer ve model asla öğrenmez.**exposure bias**- Evet .

> **教师强制（Teacher Forcing）。**訓練時,解码器在步骤 `t`Yerin girişidir.`t-1`Bu, eğitimden önce de sabitleştirilmiştir. Bu olmadan, erken hatalar sınıfı, model asla öğrenmez.**暴露偏差（Exposure Bias）**- Evet.

**The bottleneck.**Kodlayıcı, kaynak hakkında öğrendiği her şeyi bu tek bağlam vektörüne sıkıştırmalı. Uzun cümleler ayrıntıları kaybeder. Nadir kelimeler bulanıklaşır. Yeniden düzenleme (chat noir vs. siyah kedi) hesaplama değil, ezberlenmelidir.

> **瓶颈。**编码器学到的关于源的一切都必须缩小到那一个上下文向量中──长句子丢失细节──罕见词被模糊──重排序(chat noir vs. black cat) 计算 değil, hatırlamak gerekir──

Dikkat (dokuzuncu ders) bunu çözüyor. * her * kodlayıcıyı saklı durumlara bakmak için izin veriyor.

> Dikkatli olmamıza yardım eder. Bu, tüm önemli noktalardır.

> **【拓展：大语言模型的工程实践】**GPT'den ChatGPT'e kadar, NLP alanında "her görev bir model eğitimi" ile "her görevyi çözmek için bir model" biçiminin değişiminden geçti.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) şu anki işletme AI 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用  应用 应用 应用    应用     应用   应用        应用    应用       应用          应用        应用      应用          应用                                                                                                       

> **【拓展：NLP 的多语言挑战】**Küresel olarak 7000'den fazla dil vardır, ancak NLP çalışmaları çoğunlukla İngilizce ve az sayıda dil üzerinde yoğunlaşmaktadır.

## Yapın.

> **【中文解读】**Bu bölüm kodla sıfırdan gerçekleştirilen çekirdek algoritmasıdır. Bu "sıfırdan" yöntem çerçevenin arkasındaki prensipleri anlama yardımcı olur.
```figure
lstm-gates
```

## Yapın

### Adım 1: Kodlayıcı

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

`outputs`şekli var .`[batch, seq_len, hidden_dim]` giriş pozisyonu başına bir gizli durum. `hidden`şekli var .`[1, batch, hidden_dim]` son adım. Ders 08 "sınıflandırma için çıkışları topluyoruz". Burada son gizli durumu bağlam vektörü olarak tuturuz ve adımlardaki çıkışları görmezden geliriz.

> `outputs`形状为 `[batch, seq_len, hidden_dim]` Her giriş yeri gizli bir durumdur.`hidden`形状为 `[1, batch, hidden_dim]` 最终步 第08 课说 "在输出上池化做分类"──这里我们保留最后隐藏状态作为上下文向量,忽略逐步输出──

### İkinci adım: Bir dekodör

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

Decooder bir adım adım olarak adlandırılır. Giriş: tek bir token ve mevcut gizli durum. Çıktı: sözlük kaynağı logitleri bir sonraki token ve güncellenmiş gizli durum.

> 解码器每次调用一步──输入: 一批单个代币 和当前隐藏状态──输出: 下一个代币的词表 logits 和更新后的隐藏状态──

### Adım 3: Öğretmen zorla eğitim döngüsü

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

İki düğme isim vermeye değer.`ignore_index=0`Yükleme tokenlerinde kayıp atlar.`teacher_forcing_ratio`Bu, gerçek simgeyi her adımda modelin tahminine karşı kullanma olasılığının birincil değeri.

> Dikkat edilmesi gereken iki parametreden oluşuyor.`ignore_index=0`跳过填充代币 上的损失──`teacher_forcing_ratio`Bu, gerçek simgelerle model tahmininin olasılıklarını belirler. 1.0'dan başlayarak eğitim süreci boyunca yaklaşık 0.5'e geri döner.

### Adım 4: İfade döngüsü (cinsel açgözlülük)

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

Açgözlü kodlama her adımda en büyük olasılıkla belirtiyi seçer.**Beam search**- Üstünü tutar.`k`Parsiyel dizi canlı ve en yüksek puan alan tamamlayıcıyı seçer.

> 贪心解码每步选择最高概率的代币――它可能走偏: bir kez bir token gönderdiğinde, geri çekilemez――**束搜索（Beam Search）**保持排名前 `k`Son seçimde en yüksek bölümün tamamı var.

### Adım 5: Boş boğazı, gösterildi

Modelleri oyuncak kopyası görevinde eğit: Kaynak `[a, b, c, d, e]`, hedef`[a, b, c, d, e]`- Seans uzunluğunu artırın.

> Oyuncak kopyalama görevinde eğitim modeli: kaynağı`[a, b, c, d, e]`, hedef `[a, b, c, d, e]`❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖

```
seq_len=5   copy accuracy: 98%
seq_len=10  copy accuracy: 91%
seq_len=20  copy accuracy: 62%
seq_len=40  copy accuracy: 23%
```

Tek bir GRU gizli durumu, 40 token girisini kayıpsız bir şekilde hatırlayamaz. Bilgi her kodlama adımında orada, ancak dekodör yalnızca son durumu görür. Dikkat bunu doğrudan düzeltir.

> 单个GRU 隐藏状态无法无损记忆 40 代币的输入──信息在每个编码器步骤中都存在,但解码器只看到最后的状态──注意直接修复了这个问题──

> **【中文解读】**Bu bölümde, PyTorch, HuggingFace gibi olgun çerçeveler nasıl kullanılacağını gösterir.

> **【拓展：Prompt Engineering 与 LLM 应用】**Hızlı Mühendislik NLP mühendislerinin temel beceri haline geldi. Zero-shot'tan birkaç-shot'a, Chain-of-Thought'tan ReAct'e kadar, farklı fikir stratejileri farklı durumlarda uygulanmaktadır.

## Çerçeveyi kullanın.

PyTorch ' un varlığı .`nn.Transformer`ve `nn.LSTM`-Sek2sek şablonları tabanlı.`transformers`kütüphane gemileri milyarlarca token üzerinde eğitilmiş tam kodlayıcı-dekoder modelleri (BART, T5, mBART, NLLB).

> - PyTorch var .`nn.Transformer`Ve temelinde`nn.LSTM`模板──Hugging Face 的 `transformers`Binlerce milyarlık tokenle birlikte, tüm programları oluşturan bir kodlama makinesi oluşturdu.

```python
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tok = AutoTokenizer.from_pretrained("facebook/bart-base")
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-base")

src = tok("Translate this to French: Hello, how are you?", return_tensors="pt")
out = model.generate(**src, max_new_tokens=50, num_beams=4)
print(tok.decode(out[0], skip_special_tokens=True))
```

Modern kodlayıcı-dekodörler transformatörler için RNN'leri düşürdü. Yüksek düzeyde şekil (kodlayıcı, dekodör, generate-token-by-token) 2014 seq2seq kağıdı ile aynıdır. Her blok içindeki mekanizma farklıdır.

> Modern kodlayıcı- çözücü cihaz kullanımı Transformer RNN                                                                                                                                                                                                                                                        

### RNN tabanlı seq2seq'e ne zaman ulaşmak gerekiyor?

Yeni projeler için neredeyse hiç.

> Yeni projeler için neredeyse hiç gerek yok.

- Akışlı çeviriler, bir kez bir token'ı kullanırken sınırlı hafıza ile.
  流式翻译,逐代币 消耗输入,内存有界──
- Transformer belleği maliyetinin yasak olduğu cihaz içi metin üretimi.
  设备端文本生成,Transformer 内存成本过高──
- Kodlayıcı-dekoder boğazını anlamak, neden transformatörler kazanmış olduğunu anlamanın en hızlı yolu.
  Öğrenmek. Anlamak. Transformer'in neden en hızlı yol olduğunu anlamak.

### Ekspozisyon önyargısı ve azaltmaları

- **Scheduled sampling.**Eğitim sırasında öğretmen zorlama oranı, böylece model kendi hatalarından kurtulmayı öğrenir.
  **计划采样（Scheduled Sampling）。**訓練 sırasında geri dönmüş öğretmen zorlayıcı oranı, model öğrencilerin kendi hatalarından kurtulmasını sağlar.
- **Minimum risk training.**Cümle seviyesindeki BLEU puanına göre çalış, token seviyesindeki çapraz entropi yerine.
  **最小风险训练（Minimum Risk Training）。**Sıfırdan daha yakın olan şey, senin istediğin şey.
- **Reinforcement learning fine-tuning.**Sequence jeneratörünü modern LLM RLHF'de kullanılan bir metrikle ödüllendirin.
  **强化学习微调。**Üzn index ödül sırası üreticisi。用于现代 LLM 的 RLHF。

Üçü de hala transformatör tabanlı jenerasyona uygundur.

> Bu üç kişi hala Transformer tabanlı üretim için geçerlidir.

> **【中文解读】**Bu bölümde modellerin kullanılabilir ürünler için nasıl dağıtılacağı üzerinde yoğunlaşmaktadır.

## İndirin . Ürünler .

- Kaydet .`outputs/prompt-seq2seq-design.md`- ...

> 保存为 `outputs/prompt-seq2seq-design.md`- ...

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

> **【中文解读】**练习题按照易/中级/难三度递进;;建议至少完成中级题,Hard级适合深入研究或面试准备;;

## Egzersizler.

1. **Easy.**Oyuncak kopyası görevini uygulayın. Hedef kaynağa eşit olduğu giriş-çıktı çiftlerinde GRU seq2seq eğit. 5, 10, 20 uzunluklarında doğruluk ölçün.
   **简单。**实现玩具复制任务──训练 GRU seq2seq 在目标等于源的输入输出对上──测量长度 5、10、20 的准确率──复现瓶──
2. **Medium.**3 . Küçük paralel bir korpus üzerinde BLEU ölçerek açgözlülük karşılığını alın.
   **中等。**添加束宽度为 3 的束搜索解码──在小平行语料上测量对贪心的蓝色──记录束搜索在哪里胜出(通常是最后几个代币) 以及在哪里没有区别──
3. **Hard.**- Güzel sesli .`facebook/bart-base`10k çift parafrase verisi kümesi üzerinde. ince ayarlanmış modelin ışın-4 çıkışını, tutulan girişlerde bulunan temel modelin çıkışına karşılaştırın. BLEU raporunu yapın ve 10 kalite örneği seçin.
   **困难。**10.000'e göre bir veri kümesi üzerinde küçük bir düzenleme .`facebook/bart-base`◊ Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bilanı: Bedi: Bedi: Bedi: Bedi: B.

> **【中文解读】**术语表中的"İnsanların ne dediği" vs "Gerçekten ne anlama geldiği" 区分日常口语和精确技术含义──在团队协作中,统一术语定义可以避免大量沟通误解──

## Anahtar Şartlar .

| Term / 术语 | What people say / 人们常说的 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| Encoder（编码器） | Input RNN / 输入 RNN | Reads source. Produces per-step hidden states and a final context vector. / 读取源。产生逐步隐藏状态和最终上下文向量。 |
| Decoder（解码器） | Output RNN / 输出 RNN | Initialized from context vector. Generates target tokens one at a time. / 从上下文向量初始化。逐个生成目标 token。 |
| Context vector（上下文向量） | The summary / 摘要 | Final encoder hidden state. Fixed size. The bottleneck attention solves. / 最终编码器隐藏状态。固定大小。注意力解决的瓶颈。 |
| Teacher forcing（教师强制） | Use true tokens / 使用真实 token | Feed the ground-truth previous token at training time. Stabilizes learning. / 训练时馈入真实的前一个 token。稳定学习。 |
| Exposure bias（暴露偏差） | Train/test gap / 训练/测试差距 | Model trained on true tokens never practiced recovering from its own mistakes. / 在真实 token 上训练的模型从未练习从自己的错误中恢复。 |
| Beam search（束搜索） | Better decoding / 更好的解码 | Keep top-k partial sequences alive at each step instead of committing greedily. / 每步保持排名前 k 的部分序列存活，而非贪心提交。 |

> **【中文解读】**延伸阅读, derinlemesine öğrenme için yüksek kaliteli kaynaklar sağladı. Bu makaleler ve dersler, derinlemesine anlama ihtiyacı olan okuyuculara uygun olarak bu alanın klasik referanslarıdır.

## Daha fazla okumak

- [Sutskever, Vinyals, Le (2014). Sequence to Sequence Learning with Neural Networks](https://arxiv.org/abs/1409.3215) orijinal sek2seq kağıdı. 4 sayfa. / 原始 sek2seq 论文──四页──
- [Cho et al. (2014). Learning Phrase Representations using RNN Encoder-Decoder for Statistical Machine Translation](https://arxiv.org/abs/1406.1078) GRU ve kodlayıcı-dekoder çerçevesini tanıttı. / 引入了 GRU 和编码器-解码器框架──
- [Bahdanau, Cho, Bengio (2014). Neural Machine Translation by Jointly Learning to Align and Translate](https://arxiv.org/abs/1409.0473) dikkat kağıdı. Bu dersden hemen sonra okuyun. / 注意力论文──在本课后立即阅读──
- [PyTorch NLP from Scratch tutorial](https://pytorch.org/tutorials/intermediate/seq2seq_translation_tutorial.html) yapılandırılabilir sek2sek + dikkat kodu. / 可构建的 sek2seq + 注意力代码──
