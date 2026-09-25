# BERT  Maskeli Dil Modelleştirme  BERT  掩码语言模型

> GPT bir sonraki kelimeyi tahmin ediyor. BERT bir eksik kelimeyi tahmin ediyor.

> **【中文解读】**BERT sadece kodlayıcı Transformer, use掩码预测训练──理解BERT =理解双上下文建模──用于文本分类、NER、问答等──

**Type:** Hands-on | **类型:** 动手
**Language:**Python .**语言:**Python
**Prerequisites:** Phase 7 · 05 (Full Transformer), Phase 5 · 02 (Text Representation) | **前置知识:** Phase 7 · 05 (Full Transformer), Phase 5 · 02 (Text Representation)
**Time:** ~45 minutes | **时间:** ~45 分钟

## Sorunlar. Sorunlar.

2018 yılında her NLP görevi  duygu, NER, QA, entailment  kendi etiketlenmiş verilerinde sıfırdan kendi modelini eğitmiş. Düzeltirilebilecek önceden eğitilmiş "İngilizce anlama" kontrol noktası yoktu. ELMo (2018) iki yönlü LSTM ile bağlamlı yerleşimleri önceden eğitilebileceğini göstermiştir; yardımcı oldu ancak genelleştirmedi.

> 2018 yılında, her NLP  görev duygusal analiz、 isimli varlık tanımlama、 sorular、文本含都需要在自己的标签数据上从零训练模型──当时没有预训的"理解英语"检查点可供微调──ELMo(2018) kanıtı iki yönlü LSTM 预训上下文嵌入,但泛化能力有限──

BERT (Devlin et al. 2018) sordu: Bir transformatör kodlayıcıyı alıp internet'teki her cümle üzerinde eğitirsek ve iki taraftan da bağlamdan kayıp kelimeleri tahmin etmeye zorlasak ne olur?

> BERT(Devlin  et al., 2018) bir anahtar sorunu ortaya koydu: Eğer Transformer 编码器 ile, internet'teki tüm cümleler üzerinde eğitim, zorla iki tarafta aşağıdaki tahminlerin altında örtülü kelimeler, nasıl olacak?

Sonuç: 18 ay içinde BERT ve onun çeşitleri (RoBERTa, ALBERT, ELECTRA) var olan her NLP liderliğindeki her bir kişiye hakim oldu. 2020 yılına kadar dünyanın her arama motoru, içerik moderasyon boru hattı ve semantik arama sistemi içinde bir BERT vardı.

> Sonuç: 18 个月内,BERT 及其变体 (Robert ̇ Albert ̇ Electra) tüm NLP 排行榜ını yönetti. 2020 yılına kadar, dünyanın her arama motoru, içerik denetleme hattı ve dil arama sisteminde bir BERT vardır.

2026'da sadece kodlayıcı modeller sınıflandırma, geri çekim ve yapılandırılmış çıkarma için hala doğru araçtır.

> 2026 yılına kadar, kodlayıcı özel modeli hala sınıflandırma, arama ve yapılandırma çekimlerinin doğru seçimi olarak kalır. Her token'un çalışma hızı, kodlayıcıya göre hızlı 5-10 kat daha hızlıdır.

> **【中文解读】**BERT'in devrimciliği "pre-training+micro-modulation" biçiminde bulunmaktadır: Büyük ölçekte işaretsiz语料 üzerinde maskode dil modeli (MLM) pre-training, sonra belirli görevlerde küçük miktarda parametre azaltmak için.

## Konsepten bir şey.

![Masked language modeling: pick tokens, mask them, predict originals](../assets/bert-mlm.svg)

### Eğitim sinyali

Bir cümle alın:`the quick brown fox jumps over the lazy dog`- Evet .

> Bir cümle:`the quick brown fox jumps over the lazy dog`- Evet.

Tokenlerin % 15'ini rastgele maske edin:

> % 15'in belirtilerini:

```
input:  the [MASK] brown fox jumps [MASK] the lazy dog
target: the quick brown fox jumps over the lazy dog
```

Modelle, maskeli pozisyonlarda orijinal jetonları tahmin etmeyi eğit. Çünkü kodlayıcı iki yönlüdür, tahmin eder `[MASK]`1 pozisyonda kullanabilirsiniz `brown fox jumps`GPT'nin yapamayacağı şey bu.

> 訓練模型在被掩藏位置预测 原始代币──因为编码器是双向的,预测位置1 的 `[MASK]`2 ve sonrası konumları kullanılabilir.`brown fox jumps`Bu GPT'nin yapmadığı bir şey.

### BERT maskası kuralları

Tahmin için seçilen tokenlerin %15'inden:

> Seçilen %15 belirtiler arasında:

- % 80 ' i `[MASK]`- Evet .
  Çeviri: % 80`[MASK]`- Evet.
- %10'u rastgele bir token ile değiştirilir.
  Çin Çeviri: %10
- %10 değişmez kalır.
  Çinçe Çevirim: %10 保持不变──

Neden her zaman değil ?`[MASK]`- Çünkü ...`[MASK]`Bu modelin tahminini öğrenmek için çalıştırmak.`[MASK]`Bu, maskeli pozisyonların %100'inde, antrenman öncesi ve ince ayarlama arasında bir dağılım değişikliğini yaratır.

> Neden her zaman kullanılmaz ?`[MASK]`? Çünkü`[MASK]`Eğer bir eğitim modeli %100'lik bir gizlenme pozisyonunda ise, bunu görmek için beklenir.`[MASK]`, ön eğitim ve küçük düzenler arasında dağılım kayıpları meydana gelir. %10 随机替换 + 10% 保持不变让模型保持"诚实"──

> **【中文解读】**BERT 掩码的三条规则 ((80% [MASK]、10% 随机替换、10% 保持不变) ön eğitim ve微调 arasındaki dağılım farkını azaltmak için 推理时不会出现 [MASK] token,所以需要让模型在训练时也见到正常和随机替换的 token──

> **【拓展：BERT 在 RAG 系统中的角色】**Modern RAG (Çekim Artarma) sisteminde, BERT 变体 hala检索阶段in merkezi olarak kalıyor. Tüm MiniLM-L6-v2 gibi cümle-transformers 模型

### Sonraki Ceza Tahmini (NSP)  ve neden düşürüldü

Orijinal BERT ayrıca NSP üzerinde eğitim aldı: A ve B cümlelerini vererek, B'nin A'yı takip ettiğini tahmin edin. RoBERTa (2019) onu kaldırdı ve NSP'nin zarar verdiğini gösterdi, yardımcı olmadı.

> İlk BERT'in NSP'de de olduğu belirlenmiştir.

### 2026'da Ne Değişti: ModernBERT

2024 ModernBERT kağıdı, blokları 2026 ilkelerle yeniden inşa etti:

> ModernBERT 2024 yılında Modern Komponents ile kodlama makinesi bloklarını yeniden inşa etti:

| Component | Original BERT (2018) | ModernBERT (2024) |
|-----------|----------------------|-------------------|
| 组件 | 原始 BERT (2018) | ModernBERT (2024) |
| Positional | Learned absolute | RoPE |
| 位置编码 | 学习式绝对位置 | RoPE |
| Activation | GELU | GeGLU |
| 激活函数 | GELU | GeGLU |
| Normalization | LayerNorm | Pre-norm RMSNorm |
| 归一化 | LayerNorm | 前归一化 RMSNorm |
| Attention | Full dense | Alternating local (128) + global |
| 注意力 | 全密集 | 交替局部 (128) + 全局 |
| Context length | 512 | 8192 |
| 上下文长度 | 512 | 8192 |
| Tokenizer | WordPiece | BPE |
| 分词器 | WordPiece | BPE |

2018 pilinden farklı olarak, Flash-Attention-native. Inference daha iyi GLUE puanları ile DeBERTa-v3'den 8K dizide 23x daha hızlıdır.

> ModernBERT'in 2018 teknolojisinden farklı olarak, Flash Dikkatini desteklemektedir.

### 2026'da hala bir kodlayıcı seçen kullanım durumları

| Task | Why encoder beats decoder |
|------|---------------------------|
| 任务 | 为什么编码器优于解码器 |
| Retrieval / semantic search embeddings | Bidirectional context = better embedding quality per token |
| 检索/语义搜索嵌入 | 双向上下文 = 每个 token 更好的嵌入质量 |
| Classification (sentiment, intent, toxicity) | One forward pass; no generation overhead |
| 分类（情感、意图、毒性） | 一次前向传播；无生成开销 |
| NER / token labeling | Per-position output, natively bidirectional |
| NER/token 标注 | 逐位置输出，天然双向 |
| Zero-shot entailment (NLI) | Classifier head on top of encoder |
| 零样本蕴含 (NLI) | 编码器之上的分类器头 |
| Reranker for RAG | Cross-encoder scoring, 10x faster than LLM rerankers |
| RAG 重排序器 | 交叉编码器评分，比 LLM 重排序器快 10 倍 |

## Yapın.
```figure
transformer-residual
```

## Yapın

### Adım 1: Gizli mantık

Bakın .`code/main.py`- Fonksiyon`create_mlm_batch`Token ID'lerinin, bir sözcük boyutunun ve bir mask olasılık listesini alır. Giriş ID'lerini (mask uygulanan) ve etiketleri (sadece maskeli pozisyonlarda, -100 başka yerlerde  PyTorch'in indeksi kabulü görmezden gelme kuralı) gönderir.

> 参见 `code/main.py`。函数 `create_mlm_batch` accept token ID 列表、词表大小和掩码概率,返回输入 ID(已应用掩码) 和标签(仅在掩码位置有价值,其余为 -100PyTorch的忽略索引约定)

```python
def create_mlm_batch(tokens, vocab_size, mask_prob=0.15, rng=None):
    input_ids = list(tokens)
    labels = [-100] * len(tokens)
    for i, t in enumerate(tokens):
        if rng.random() < mask_prob:
            labels[i] = t
            r = rng.random()
            if r < 0.8:
                input_ids[i] = MASK_ID
            elif r < 0.9:
                input_ids[i] = rng.randrange(vocab_size)
            # else: keep original
    return input_ids, labels
```

### Adım 2: Küçük bir korpus üzerinde MLM tahminini çalıştır

2 katlı bir kodlayıcı + MLM başını 20 kelime, 200 cümle kelime birikimi üzerinde eğit.

> 20 kelime kelime çizelgesinde ve 200 cümle üzerinde 2 katlı bir kodlayıcı + MLM başlığı eğitmek.

### Adım 3: Maske türlerini karşılaştırın

Üç yönlü kuralın modelin nasıl kullanılabilir hale geldiğini göster .`[MASK]`- Maskeli cümle ve maskeli cümle üzerine tahmin yapın. Her ikisi de makul bir simge dağıtımları üretmelidir çünkü model eğitimde her iki örneği de görmüştür.

> 展示三路规则  nasıl modellerin yokluğunda `[MASK]`Bu iki model de eğitim sırasında görülmüştür.

### Dördüncü adım: ince ayarlı baş

Bir oyuncak duygu verisi kümesindeki sınıflandırma başlığı ile değiştirin. Sadece baş trenleri; kodlayıcı donmuştur. Bu her BERT uygulamasının takip ettiği bir kalıp.

> Bir oyuncak duygusu verisi üzerinde eğitim, başı eğitimi, kodlama 结── bu her BERT  uygulamasının standart modeli

> **【拓展：BERT 微调的实践技巧】**BERT 微调'un en iyi uygulamaları şunları içerir: 1) Daha küçük öğrenme oranını kullanmak; 2) ön eğitim ağırlığını bozmaktan kaçınmak; 2) bölük sınıfı görevleri için [CLS] token kullanımı için bir cümle ifade etmesi; 3) NER için ve diğer tokenlerden  görevler için, her konumdan çıkış kullanmak; 4) adım adım çözmek (sıralamalı çözmek)

## Çerçeveyi kullanın.

```python
from transformers import AutoModel, AutoTokenizer

tok = AutoTokenizer.from_pretrained("answerdotai/ModernBERT-base")
model = AutoModel.from_pretrained("answerdotai/ModernBERT-base")

text = "Attention is all you need."
inputs = tok(text, return_tensors="pt")
out = model(**inputs).last_hidden_state   # (1, N, 768)
```

**Embedding models are fine-tuned BERT.** `sentence-transformers``all-MiniLM-L6-v2`Bu, bir diğer tür devirde, bir diğer tür devirde, bir diğer tür devirde, bir diğer tür devirde, bir diğer tür devirde, bir diğer tür devirde, bir diğer tür devirde, bir diğer tür devirde, bir diğer tür devirde, bir diğer tür devirde, bir diğer tür devirde, bir diğer tür devirde, bir diğer tür devirde, bir diğer tür devirde, bir diğer tür devirde, bir diğer tür devirde, bir diğer tür devirde, bir diğer tür devirde, bir diğer bir devirde, bir devirde, bir devirde, bir devirde, bir devirde, bir devirde, bir devirde, bir devirde, bir devirde, bir devirde, bir devirde, bir devirde, bir devirde, bir devirde, bir devirde, bir devirde, bir devirde, bir devirde, bir devirde, bir devirde, bir devirde, bir devirde, bir devirde, bir devirde, bir devirde, bir devirde, bir devirde, bir devirde, bir devirde, bir devirde, bir devirde, bir devirde, bir devirde, bir devirde, bir devirde, bir devirde, bir devirde, bir devirde, bir devirde, bir devirde, bir devirde, bir devirde, bir devirde, bir devirde, bir devirde, bir devirde, bir devirde, birde, bir devirde, bir devirde, bir devirde, bir de, bir devirde,

> **嵌入模型是微调后的 BERT。** `sentence-transformers`Modeller`all-MiniLM-L6-v2`Aslında, BERT'nin kayıp antrenmanına karşı aynı kodlama yapıları vardır, sadece kayıp işlevi değişmiştir.

**Cross-encoder rerankers are also fine-tuned BERT.**Çift sınıflandırma `[CLS] query [SEP] doc [SEP]`Arama ve belge arasındaki iki yönlü dikkat, çapraz kodlayıcılara iki yönlü kodlayıcılara karşı kalite kenarlarını veren tam olarak budur.

> **交叉编码器重排序器也是微调后的 BERT。**- Evet .`[CLS] query [SEP] doc [SEP]`Sorgu ve dosya arasındaki iki yönlü dikkat, iki yönlü kodlayıcıların kalitesi iki yönlü kodlayıcılardan daha iyi olmasının nedeni olarak görülmektedir.

**When not to pick BERT in 2026.**Genereatif bir şey. Kodlayıcı, jetonları otomatik olarak üretmek için mantıklı bir yolun bulunmuyor. Ayrıca: küçük bir dekoderin daha esnek bir şekilde kalitesi eşleştirebileceği 1B parametrelerinin altında olan herhangi bir şey (Phi-3-Mini, Qwen2-1.5B).

> **2026 年何时不选 BERT。**任何生成式任务──编码器, kendi kendine dönüştürme tokeni gerçekleştirmek için mantıklı bir yol bulunmamaktadır.  生成──此外, 1B 参数下面的场景中,小型解码器 ((如 Phi-3-Mini、Qwen2-1.5B) daha az参数 ile oldukça esneklik elde edebilir.

> **【拓展：ModernBERT 的现代化改进】**ModernBERT(2024) 2018 yılına gelmektedir BERT yapısı Tam olarak yükseltilmesi:RoPE 替代学习式位置编码、GeGLU 替代 GELU、前归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归归

## İndirin . Ürünler .

Bakın .`outputs/skill-bert-finetuner.md`. Yetenek alanı yeni bir sınıflandırma veya çıkarma görevi için BERT ince ayarlamaları (yöntemlilik seçimi, baş özellikleri, veriler, değerlendirme, durma) yapar.

> 参见 `outputs/skill-bert-finetuner.md`Bu beceriler yeni bir sınıflandırma veya görev planlaması için kullanılır.

## Egzersizler.

1. **Easy.**Çık .`code/main.py`Bu sayede %15'i onaylayıp %80'i de onaylayıp %10'a dağıtılır.`[MASK]`- Evet .
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`code/main.py`Bu sayede %15'i seçilmiştir.`[MASK]`- Evet.
2. **Medium.**Tam kelime maskesini uygulayın: bir kelime alt kelimelere simgelik yapılırsa, tüm alt kelimeleri bir araya getir veya hiç bir şey maske edin. Bu 500 cümlelik bir korpusta MLM doğruluğunu arttırır mı ölçün.
   Çinçe Çevirimi: implement全词掩码: Bir kelime bir çok kelime için ayrılmışsa, ya da tüm掩码 ya da tüm掩码 değil.
3. **Hard.**Halkın bir veri kümesinden 10.000 cümle üzerine küçük bir (2 katman, d=64) BERT eğit.`[CLS]`- Dönüştürücü-tek bir başlangıç çizgisi ile karşılaştırın.
   Çinçe Çevirimiçi: WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB WEB`[CLS]`SST-2 情感分类. Aynı parametre ile karşılaştırıldığında hangisi daha iyi?

## Anahtar Şartlar .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| MLM | "Masked language modeling" | Training signal: randomly replace 15% of tokens with `[MASK]`, predict the originals. |
| MLM | "掩码语言建模" | 训练信号：随机将 15% 的 token 替换为 `[MASK]`，预测原始 token。 |
| Bidirectional | "Looks both ways" | Encoder attention has no causal mask — every position sees every other position. |
| 双向 | "看两边" | 编码器注意力没有因果掩码——每个位置都能看到其他所有位置。 |
| `[CLS]` | "The pooler token" | A special token prepended to every sequence; its final embedding is used as the sentence-level representation. |
| `[CLS]` | "池化 token" | 一个特殊 token，添加到每个序列开头；其最终嵌入用作句子级表示。 |
| `[SEP]` | "Segment separator" | Separates paired sequences (e.g. query/doc, sentence A/B). |
| `[SEP]` | "片段分隔符" | 分隔成对序列（如查询/文档、句子 A/B）。 |
| NSP | "Next sentence prediction" | BERT's second pretraining task; shown to be useless in RoBERTa, dropped after 2019. |
| NSP | "下一句预测" | BERT 的第二个预训练任务；RoBERTa 证明其无用，2019 年后弃用。 |
| Fine-tuning | "Adapt to a task" | Keep the encoder mostly frozen; train a small head on top for the downstream task. |
| 微调 | "适应任务" | 保持编码器基本冻结；在顶部训练一个小头用于下游任务。 |
| Cross-encoder | "A reranker" | A BERT that takes both query and doc as input, outputs a relevance score. |
| 交叉编码器 | "重排序器" | 同时接收查询和文档作为输入的 BERT，输出相关性分数。 |
| ModernBERT | "2024 refresh" | Encoder rebuilt with RoPE, RMSNorm, GeGLU, alternating local/global attention, 8K context. |
| ModernBERT | "2024 刷新版" | 用 RoPE、RMSNorm、GeGLU、交替局部/全局注意力重建的编码器，8K 上下文。 |

## Daha fazla okumak

- [Devlin et al. (2018). BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding](https://arxiv.org/abs/1810.04805) orijinal kağıt.
  Çeviri:Bert
- [Liu et al. (2019). RoBERTa: A Robustly Optimized BERT Pretraining Approach](https://arxiv.org/abs/1907.11692)BERT'i nasıl doğru şekilde eğitilir?
  Çeviri: nasıl doğru eğitim BERT; kanıtladı NSP 无用──
- [Clark et al. (2020). ELECTRA: Pre-training Text Encoders as Discriminators Rather Than Generators](https://arxiv.org/abs/2003.10555) değiştirilmiş belirti tespitleri eşleşen hesaplamalarda MLM'yi yener.
  Çinçe Çevirimiçi: 检测在相同计算量下优于 MLM。
- [Warner et al. (2024). Smarter, Better, Faster, Longer: A Modern Bidirectional Encoder](https://arxiv.org/abs/2412.13663)ModernBERT kağıdı.
  Çeviri: ModernBERT
- [HuggingFace `modeling_bert.py`](https://github.com/huggingface/transformers/blob/main/src/transformers/models/bert/modeling_bert.py) Kanonik kodlayıcı referansı.
  Çeviri:HuggingFace BERT 模型实现参考代码──
