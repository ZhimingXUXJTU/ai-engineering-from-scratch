# T5, BART  Kodlayıcı-Küçükleme Modelleri  T5 BART  Kodlayıcı-Kodlayıcı Modelleri

> Kodlayıcılar anlıyor. Dekoderler oluşturur. Onları bir araya getirir ve giriş → çıkış görevleri için bir model oluşturulur: çevir, özetle, yeniden yaz, transkripte et.

> **【中文解读】**T5 Tüm NLP  görevlerini teksten metne biçimine birleştirmek.

**Type:** Study | **类型:** 学习
**Language:**Python .**语言:**Python
**Prerequisites:** Phase 7 · 05 (Full Transformer), Phase 7 · 06 (BERT), Phase 7 · 07 (GPT) | **前置知识:** Phase 7 · 05 (Full Transformer), Phase 7 · 06 (BERT), Phase 7 · 07 (GPT)
**Time:** ~45 minutes | **时间:** ~45 分钟

## Sorunlar. Sorunlar.

Sadece dekodörlü GPT ve sadece kodlayıcı BERT her biri farklı bir amaç için 2017 mimarisini çizer.

> 解码器专用 GPT 和编码器专用 BERT, 2017 yılının yapısını farklı amaçlarla daha iyi tanımladı.

- Çevirim: İngilizce → Fransızca.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri
- Toplam: 5.000 tokenlik makale → 200 tokenlik toplam.
  Çinli Türkçe Çeviri: 5000 Token 文章 → 200 Token 摘要。
- Konuşma tanımı: ses simgeler → metin simgeler.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri
- Yapılandırılmış çıkarma: proza → JSON.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri

Bu özellikler için, kodlayıcı-dekoder en temiz uyum sağlar. Kodlayıcı kaynağın yoğun bir temsilini üretir. Dekoder çıkış üretir, her adımda bu temsiline çapraz olarak katılır. Eğitim çıkış tarafında bir-bir değişimdir. GPT ile aynı kaybı, sadece kodlayıcı çıkışına bağlıdır.

> Bu görevler için, kodlayıcı- çözücü en uygun seçenektir. Kodlayıcı üretimi kaynaklarının yoğun göstergesi.

Modern oyun kitabı iki makalede tanımlandı:

> 两篇论文定义了现代范式:

1. **T5**"Teks-yazı transfer transformer". Her NLP görevi metin-a, metin-a. tek mimarlık, tek kelime birikimi, tek kayıp olarak yeniden çerçevelidir. Gizli uzantı tahmininde önceden eğitilmiştir (girideki yozlaşmış uzantılar, çıkışta onları çözünür).
   Çeviri:**T5**(Raffel 等人,2019) ・・・"文本到文本迁移 Transformer" ・・・ her NLP görevi yeniden tanımlanmıştır:文本输入文本输出 ・・・单一架构、单一词表、单一损失 ・・・ using掩码片段预测 to carry out pre-training ((破坏输入中的片段,在输出中解码它们) ・・・
2. **BART**(Lewis et al. 2019). "İki yönlü ve Otomatik Geri Dönüştürücü Transformer. " Otomatik kodlayıcıyı reddetmek: çok yönlü olarak bozuk giriş (karıştırmak, maske, silmek, döndürmek), dekodörden orijinalini yeniden oluşturmasını isteyin.
   Çeviri:**BART**(Lewis 等人,2019) ――"双向自归转变器"──去噪自编码器:用多种方式破坏输入(打乱、掩码、删除、旋转),要求解码器重建原始文本。

2026 yılında kodlayıcı-dekoder biçimi giriş yapısının önemli olduğu yerlerde yaşar:

> 2026 yılında, kodlayıcı- çözücü biçimi giriş yapısı önemli olaylarda var olmaya devam ediyor:

- Şapşır (söz → metin).
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çov Çov Çov Çov Çov Çov Çov Çov Çov Çov Çov Çov Çov Çov Çov Çov
- Google'ın çeviri yığını.
  Çeviri:Google'ın çevirme sistemi
- Bazı kod tamamlama / onarım modelleri farklı bağlam ve düzenleme yapıları vardır.
  Çinçe Çevirimiçi: bazı belirgin bir aşağıdaki metin-edited structure'nın kodları tamamlanmış/düzeltilmiş modelleri vardır.
- Flan-T5 ve yapılandırılmış mantıklama görevleri için değişkenler.
  Çeviri:Flan-T5 ve onun değişikleri, yapısal düşünme görevleri için kullanılır.

Sadece dekoder odak noktasını kazandı, ama kodlayıcı dekoder asla gitmedi.

> 解码器专用模型聚光灯'ı kazanmış, ancak kodlayıcı-解码器 asla yok olmadı.

> **【中文解读】**编码器-解码器架构在"输入→输出" yapılandırma görevlerinde hala avantajlar vardır. T5 tüm NLP 任务统一为文本格式,BART用去噪编码训练――Tamasahi tek metin üretimi alanında sadece Decoder tarafından değiştirilmiş olsa da,语音识别(Whisper) 翻译、摘要等 görevler arasında en iyi seçim olarak kalmaktadır.

## Konsepten bir şey.

![Encoder-decoder with cross-attention](../assets/encoder-decoder.svg)

### Önceki döngü

```
source tokens ─▶ encoder ─▶ (N_src, d_model)  ──┐
                                                 │
target tokens ─▶ decoder block                   │
                 ├─▶ masked self-attention       │
                 ├─▶ cross-attention ◀───────────┘
                 └─▶ FFN
                ↓
              next-token logits
```

Önemli olan, kodlayıcı giriş başına bir kez çalışır. Dekoder otomatik olarak çalışır ancak her adımda * aynı * kodlayıcı çıkışına karşı çalışır. Kodlayıcı çıkışını önbelleğe koymak uzun girişler için ücretsiz bir hızlandırmadır.

> Önemli olan, kodlayıcı her girişe sadece bir kez çalışır. Kodlayıcı kendi kendine geri döner, ancak her adımda aynı kodlayıcı çıkışını paylaşır.

> **【中文解读】**交叉注意力 is编码器-解码器架构的信息桥梁:Q 来自编码器,K/V 来自编码器输出;;编码器只运行一次(高效),解码器每步都通过交叉注意力访问编码器的完整输出;;

> **【拓展：Whisper 的编码器-解码器设计】**OpenAI'nin Whisper 语音识别模型ı, kodlayıcı- çözücü yapı kullanır, çünkü ses频 (Mel频谱图) ve metin tamamen farklı bir modoldur.

### T5 Eğitim öncesi  Uçuş süresinin bozulması

Girişlerin rastgele uzantıları seçin (ortalama uzunluğu 3 token, toplam %15). Her uzantıyı benzersiz bir sentinel ile değiştirin: `<extra_id_0>`- Evet .`<extra_id_1>`, vb. Dekodör sadece bozuk olan alanları bekçi önlüğü ile çıkardı:

> 随机选择输入中的片段(平均长度 3 个标志,总计 15%) △ her bir bölüm için tek görevli işaretle değiştir:`<extra_id_0>`- Evet.`<extra_id_1>`...bkz: ...bu yüzden sadece parçalanmış parçalar ve görevlileri çıkarıyor:

```
source: The quick <extra_id_0> fox jumps <extra_id_1> dog
target: <extra_id_0> brown <extra_id_1> over the lazy
```

T5 kağıtının ablasyonunda MLM (BERT) ve prefiks-LM (UniLM) ile rekabetçi.

> T5 makalesindeki giderme deneyinde, MLM (BERT) ve önceki LM (UniLM) ile rekabet gücü eşit olarak görülmektedir.

### BART öncesi eğitim  Çok gürültü denetimi

BART beş gürültü fonksiyonunu dener:

> BART 尝试五种噪声函数:

1. İşaret maskeli.
   Çıkışlı bir ses.
2. İşaret silinmesi.
   Çıkışlar: Çıkışlar: Çıkışlar: Çıkışlar: Çıkışlar: Çıkışlar: Çıkışlar: Çıkışlar: Çıkışlar: Çıkışlar: Çıkışlar: Çıkışlar: Çıkışlar: Çıkışlar: Çıkışlar: Çıkışlar: Çıkışlar: Çıkışlar: Çıkışlar: Çıkışlar: Çıkışlar: Çıkışlar: Çıkışlar: Çıkışlar: Çıkışlar: Çıkışlar: Çıkışlar: Çıkışlar: Çıkışlar: Çıkışlar: Çıkışlar: Çıkışlar: Çıkışlar: Çıkışlar: Çıkışlar: Çıkışlar: Çıkışlar: Çıkışlar: Çıkışlar: Çıkışlar: Çıkışlar: Çıkışlar: Çıkışlar: Çıkışlar: Çıkışlar: Çıkışlar: Çıkışlar: Çıkışlar: Çıkışlar: Çıkışlar: Çıkışlar: Çıkışlar: Çıkışlar: Çıkışlar: Çıkışlar: Çıkışlar: Çıkışlar: Çıkışlar: Çıkışlar: Çıkışlar: Çıkışlar: Çıkışlar: Çıkışlar: Çıkışlar: Çıkışlar: Çıkışlar: Çıkışlar: Çıkış Çıkış Çıkış Çıkış Çıkış Çıkış Çıkış Çıkış Çıkış Çıkış Çıkış Çıkış Çıkış Çıkış Çıkış Çıkış Çıkış Çıkış Çıkış Çıkış Çıkış Çıkış Çıkış Çıkış Çıkış Çıkış Çıkış Çıkış Çıkış Çıkış Çıkış Çıkış Çıkış Çıkış Çık Çık Çıkış Çıkış Çık Çıkış Çık Çık Çıkış Çık Çık Çık Çık Çık Çık Çık Çık Çık Çık Çık Çık Çık Çık Çık Çık Çık Çık Çık Çık Çık Çık Çık Çık Çık Ç
3. Metin doldurma (bir uzayı maske, dekodör doğru uzunluğu ekler).
   Çine dilinde:文本填充, 解码器插入正确长度, 解码器插入正确长度, 解码器插入正确长度, 解码器插入正确长度, 解码器插入正确长度, 解码器插入正确长度, 掩码一个片段, 解码器插入正确长度, 掩码一个片段, 解码器插入正确长度, 掩码器插入正确长度, 掩码器插入正确长度, 掩码器插入正确长度, 掩码器插入正确长度, 掩码器插入正确长度, 掩码器插入正确长度, 掩码器插入正确长度, 掩码器插入正确长度, 掩码器插入正确长度, 掩码器插入正确长度, 掩码器插入正长度, 掩码器插入正长度, 掩码器插入正长度, 掩码器
4. Cevabı değiştirmek.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri
5. Belge dönüşümü.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri

Metin doldurma + cümle permutasyonu kombinasyonu en iyi aşağı akıntılı sayıları üretti. Dekodör her zaman orijinalini yeniden oluşturur. BART'in çıkışı sadece bozuk süreler değil, tüm dizidir  bu nedenle önceden hesaplama T5'ten daha yüksektür.

> 组合文本填充 + 句子排列产生最佳下游效果──解码器总是重建原始文本──BART'ın çıkışı sadece yıkılmış parçalar değil, tam bir dizi olarak oluşur.

> **【中文解读】**T5 ve BART'ın önceden eğitim stratejisi farklıdır:T5'in uzantısı yozlaşır sadece tahmin ediliyor yıkılmış parçalar(高效),BART'ın giderek kaydedilmesi tüm dizini yeniden oluşturmak için daha kapsamlı ama daha pahalı bir şekilde seçilir.

### İndirim

GPT ile aynı autoregressive nesil. Açgözlülük / ışın / üst-p örnekleme uygulanır. Çatlama oranından daha dar çıkış dağılımı olduğundan, ışın araması (genişliği 45) çevirme ve özetleme için standarttır.

> 推理与 GPT的自归生成相同──贪心/束搜索/top-p 采样都适用──束搜索(宽度 4-5) 推理与 GPT 的自归生成相同──贪心/束搜索/top-p 采样都适用──束搜索(宽度 4-5) 推理与 GPT 的自归生成相同──贪心/束搜索/top-p 采样都适用──束搜索(宽度 4-5) 推理与 GPT 的自归生成相同── 推理与 GPT 的自归生成的标准策略,因为输出分布比对话较较窄──

> **【拓展：Beam Search 在翻译中的重要性】**编码器-解码器模型在翻译和摘要任务中常用束搜索(宽度 4-5), çünkü çıktıların dağılımları daha darıktır.

### 2026'da her variansı ne zaman seçmeliyiz?

| Task | Encoder-decoder? | Why |
|------|------------------|-----|
| 任务 | 是否用编码器-解码器？ | 原因 |
| Translation | Yes, usually | Clear source sequence; fixed output distribution; beam search works |
| 翻译 | 通常是 | 明确的源序列；固定的输出分布；束搜索有效 |
| Speech-to-text | Yes (Whisper) | Input modality differs from output; encoder shapes audio features |
| 语音转文本 | 是（Whisper） | 输入模态与输出不同；编码器处理音频特征 |
| Chat / reasoning | No, decoder-only | No persistent "input" — the conversation is the sequence |
| 对话/推理 | 否，解码器专用 | 没有持久的"输入"——对话本身就是序列 |
| Code completion | Usually no | Decoder-only with long context wins; code models like Qwen 2.5 Coder are decoder-only |
| 代码补全 | 通常否 | 带长上下文的解码器专用胜出；Qwen 2.5 Coder 等代码模型是解码器专用 |
| Summarization | Either works | BART, PEGASUS beat earlier decoder-only baselines; modern decoder-only LLMs match them |
| 摘要 | 都可以 | BART、PEGASUS 超越早期解码器专用基线；现代解码器专用 LLM 能匹配它们 |
| Structured extraction | Either | T5 is clean because "text → text" absorbs any output format |
| 结构化提取 | 都可以 | T5 很干净，因为"文本 → 文本"可以吸收任何输出格式 |

~2022'den bu yana tendensi: sadece dekodör, kodlayıcı-dekodör sahip olduğu görevleri üstlenir çünkü (a) talimat ayarlı dekodör-tek LLM'ler istekle herhangi bir şeye genel hale gelir, (b) bir mimarinin iki taneye oranla daha kolay ölçeklenmesi, (c) RLHF bir dekodörü varsayır.

> 2022 yılından bu yana, Trend: Çözücü özel bir şekilde kodlayıcı- Çözücü önceden sahip olduğu görevleri üstlendi, çünkü (a) Kurallar küçük bir şekilde kodlayıcı özel bir şekilde herhangi bir görev için genel hale getirebilir, (b) tek bir yapı iki daha kolay genişletebilir, (c) RLHF ı kullanmak için kurgulama Çözücü.

> **【拓展：T5 的 text-to-text 统一范式】**T5'in çekirdek psikolojik düşüncesi tüm NLP 任务统一为"文本输入→文本输出"格式──翻译:" İngilizce'ye çevirin: Hello → Bonjour";分类:"Sentiment: Bu film harika → olumlu"──这种统一简化了架构和训练流程,也后来指示调和快速工程的思想源头──Flan-T5 更是通过指示微调大幅提升了零样本能力──

## Yapın.
```figure
encoder-decoder
```

## Yapın

Bakın .`code/main.py`Oyuncak korpusu için T5 tarzı tarzı korumayı uyguluyoruz bu dersin en faydalı tek parçası çünkü o zamandan beri her kodlayıcı-dekoder öncesi eğitim tarifi içinde görünebilir.

> 参见 `code/main.py`Oyuncak dilini kullanmak için T5 biçiminin parçalarını yıkıyoruz Bu dersin en yararlı parçasıdır çünkü bu, sonraki her kodlayıcı- çözücü önceden eğitim programında yer alır.

### Adım 1: Uzay yolsuzluğu

```python
def corrupt_spans(tokens, mask_rate=0.15, mean_span=3.0, rng=None):
    """Pick spans summing to ~mask_rate of tokens. Return (corrupted_input, target)."""
    n = len(tokens)
    n_mask = max(1, int(n * mask_rate))
    n_spans = max(1, int(round(n_mask / mean_span)))
    ...
```

Hedef biçimi T5 sözleşmesi: `<sent0> span0 <sent1> span1 ...`. Bozuk giriş, değişmeyen tokenleri, bekçi tokenleriyle, uzanan yerlerde birbirine bırakır.

> 目標格式 T5 约定'e göre:`<sent0> span0 <sent1> span1 ...`△ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △

### Adım 2: Geri dönüş kontrolü

Bu, bir akıl kontrolüdür. Gerçek eğitim bunu asla yapmaz, ancak test ucuz ve zaman hesaplama işleminizde birer hata yakalar.

> 给定被破坏的输入和目标,重建原始句子──如果破坏是可逆的,前向传播就是良定义的──这是一个合理性检查真实训练从不这样做,但测试成本低且能发现片段簿记中的差一错──

### Adım 3: BART gürültüsü

Beş fonksiyon: `token_mask`- Evet .`token_delete`- Evet .`text_infill`- Evet .`sentence_permute`- Evet .`document_rotate`İki tane yapıp sonuçları göster.

> 五个函数:`token_mask`- Evet.`token_delete`- Evet.`text_infill`- Evet.`sentence_permute`- Evet.`document_rotate`◊ 组合其中2并显示结果──

## Çerçeveyi kullanın.

HuggingFace referansı:

> Öğütleme Yüzü 参考:

```python
from transformers import T5ForConditionalGeneration, T5Tokenizer
tok = T5Tokenizer.from_pretrained("google/flan-t5-base")
model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-base")

inputs = tok("translate English to French: Attention is all you need.", return_tensors="pt")
out = model.generate(**inputs, max_new_tokens=32)
print(tok.decode(out[0], skip_special_tokens=True))
```

T5 numarası: görev adı giriş metine girer. Aynı model onlarca görevi ele alır çünkü her görev metin-in, metin-out. 2026 yılında bu örnektir talimat ayarlı dekodör-tek modeller tarafından genelleştirildi, ancak T5 önce kodifiye edildi.

> T5'in teknikleri: görev adı giriş metinde yazılır. Aynı model onlarca görevi işleyebilir, çünkü her görevi metin giriş-metin çıkışıdır. 2026 yılında bu model, özel kodlama modelinin yaygınlaştırılması için talimat verilmiştir. Ancak T5 ilk olarak düzenlenmiştir.

## İndirin . Ürünler .

Bakın .`outputs/skill-seq2seq-picker.md`. Yetenek, giriş-çıktı yapısı, gecikme ve kalite hedefleri verildiği için yeni bir görev için sadece kodlayıcı-dekoder ve dekoder arasında seçim yapar.

> 参见 `outputs/skill-seq2seq-picker.md` Bu beceri  Yeni görev için giriş-çıçıktı yapı  gecikme ve kalite hedefine göre kodlayıcı- çözücü veya çözücü özel yapı seçmek 

## Egzersizler.

1. **Easy.**Çık .`code/main.py`, 30 token cümleye uzanma bozukluğu uygula, sentinel olmayan kaynak tokenlerini çözülmüş hedef uzanmalarla bağlamanın orijinalini yeniden ürettiğini doğrula.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`code/main.py`, 30 token için cümle uygulama bölümü yıkım, verification will non-sentral source token with the unlocked target fragment İleştirilir yeniden orijinal metin için kullanılabilir.
2. **Medium.**BART'ın uygulanması `text_infill`gürültü: rastgele süreleri tek birer ile değiştirin `<mask>`Bu, bir simgeyi gösterir ve dekodör doğru uzantı uzunluğu artı içeriği çıkarmalıdır.
   Çeviri: BART'ın gerçekleşmesi`text_infill`噪声: 用单个 `<mask>`Token 代引随机片段,解码器 doğru video uzunluğu ve içeriğini belirlemek gerekir.
3. **Hard.**- Güzel sesli .`flan-t5-small`Küçük bir İngilizce → Domuz-Latin corpus (200 çift) üzerinde.`Llama-3.2-1B`Aynı hesaplama ile aynı veriler üzerinde.
   Çevre dilinde dil değiştirme: 中文翻译:在小型英语 → Pig Latin 语料库(200对) 上微调 `flan-t5-small`◊ 50'den fazla test kümesi üzerinde ölçüm BLEU % sayı ◊ aynı verilerde ◊ aynı hesaplama miktarında küçük bir düzenleme `Llama-3.2-1B`- Karşılaştırmak için.

## Anahtar Şartlar .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Encoder-decoder | "Seq2seq transformer" | Two stacks: bidirectional encoder for input, causal decoder with cross-attention for output. |
| 编码器-解码器 | "Seq2seq Transformer" | 两个堆栈：双向编码器处理输入，带交叉注意力的因果解码器生成输出。 |
| Cross-attention | "Where source talks to target" | Decoder's Q × encoder's K/V. The only place encoder information enters the decoder. |
| 交叉注意力 | "源与目标对话的地方" | 解码器的 Q × 编码器的 K/V。编码器信息进入解码器的唯一通道。 |
| Span corruption | "T5's pretraining trick" | Replace random spans with sentinel tokens; decoder outputs the spans. |
| 片段破坏 | "T5 的预训练技巧" | 用哨兵 token 替换随机片段；解码器输出这些片段。 |
| Denoising objective | "BART's game" | Apply a noise function to the input, train the decoder to reconstruct the clean sequence. |
| 去噪目标 | "BART 的游戏" | 对输入应用噪声函数，训练解码器重建干净序列。 |
| Sentinel token | "The `<extra_id_N>` placeholder" | Special tokens that tag corrupted spans in the source and re-tag them in the target. |
| 哨兵 token | "`<extra_id_N>` 占位符" | 在源端标记被破坏片段、在目标端重新标记的特殊 token。 |
| Flan | "Instruction-tuned T5" | T5 fine-tuned on >1,800 tasks; made encoder-decoder competitive at instruction-following. |
| Flan | "指令微调的 T5" | 在 1,800+ 任务上微调的 T5；使编码器-解码器在指令遵循方面具有竞争力。 |
| Beam search | "Decoding strategy" | Keep top-k partial sequences at each step; standard for translation/summarization. |
| 束搜索 | "解码策略" | 每步保留得分最高的 k 个部分序列；翻译/摘要的标准策略。 |
| Teacher forcing | "Training-time input" | During training, feed the true previous output token to the decoder, not the sampled one. |
| Teacher forcing | "训练时输入" | 训练时向解码器输入真实的上一个输出 token，而非采样的 token。 |

## Daha fazla okumak

- [Raffel et al. (2019). Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer](https://arxiv.org/abs/1910.10683)T5.
  Çeviri:T5
- [Lewis et al. (2019). BART: Denoising Sequence-to-Sequence Pre-training for Natural Language Generation, Translation, and Comprehension](https://arxiv.org/abs/1910.13461)- BART.
  Çeviri:BART
- [Chung et al. (2022). Scaling Instruction-Finetuned Language Models](https://arxiv.org/abs/2210.11416) Flan-T5.
  Çeviri:Flan-T5
- [Radford et al. (2022). Robust Speech Recognition via Large-Scale Weak Supervision](https://arxiv.org/abs/2212.04356) Fısıltı, 2026'da kullanılan kodlayıcı-dekoder.
  Çinçe Çevirim:Sipper 论文,2026 yıl tipik kodlayıcı-解码器模型──
- [HuggingFace `modeling_t5.py`](https://github.com/huggingface/transformers/blob/main/src/transformers/models/t5/modeling_t5.py) referans uygulanması.
  Çeviri:T5 参考实现。
