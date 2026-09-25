# Çoklu Token Tahmin (MTP)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    

> GPT-2'den Llama 3'e kadar her bir gerileme derecesinde olan LLM, pozisyon başına bir kayıp kazanır. DeepSeek-V3 pozisyon başına ikinci bir kayıp ekledi. Bundan sonra token'ı tahmin et. Ekstra 14B parametreleri (671B modelinde) gradient akışı yoluyla ana modele geri distillendi ve eğitilmiş MTP başları, %80+ kabul ile spekülasyonsal dekodlama taslakçıları olarak sonuçta yeniden kullanıldı. 1.8x jenerasyon geçiş ücretsiz geldi. Bu ders, DeepSeek teknik raporundan sıralı MTP modülü oluşturur, kayıp ve paylaşılan baş parametresi düzenini hesaplar ve neden MTP nedensel zinciri koruduğunu açıklarken Gloeckle et al'ın orijinal paralel MTP'si onu kırdı.

> **【中文解读】**传统 LLM Her pozisyon sadece bir sonraki noktayı öngörüyor。DeepSeek-V3 her pozisyonda ikinci bir kaybı artırıyor: öngörüyor aşağıdaki noktayı。 Ekstra 14B 参数 梯度流蒸回主模型, eğitimli MTP 头在推理中被用投机解码的草稿器(80%+ 接受率),1.8倍吞吐提升免费获得。

> **【拓展：MTP→DeepSeek-V3创新】**MTP, DeepSeek-V3'in dört büyük yapısal yeniliklerinden biridir. Aynı zamanda eğitimde gelişmeler yapmıştır.

>  **【前置】**Öğrenci bölümünün önüne geçmek için öncelikle öğrenin:Dava 10·04(Pre-Training GPT);Dava 10·15(Spekülatör Çözümleme)MTP 在推理时变成草稿器;因果链(causal chain) konsept。本节是Dava 10·20(DeepSeek-V3 Walkthrough) 的前置。
>  **【类比】**传统下语标记 = 学英语时一次记一个单词──MTP = 同时记"这个单词"和"下一个常用搭配"训练时学更多结构(梯度信号丰富),推理时把"搭配预测器"当草稿器免费加速(80% 接受率)

**Type:** Build
**Languages:** Python (stdlib)
**Prerequisites:** Phase 10 · 04 (pre-training a mini GPT), Phase 10 · 15 (speculative decoding)
**Time:** ~60 minutes

## Öğrenme hedefleri

- MTP eğitim hedefini belirtin ve tahmin derinliklerinde ortak kayıptan çıkarın.
  Açıklama MTP                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
- Gloeckle et al.'ın paralel MTP başlıkları (2024) ile DeepSeek-V3'ün sıralı MTP modülleri arasındaki farkı ve sıralı tasarının nedensel zinciri neden koruduğunu açıklayın.
  解释 Gloeckle'ın MTP 头条与 DeepSeek-V3 模块的区别,以及为什么顺序设计保持因果链
- Bir önceden eğitim koşusuna MTP modüllerini eklemek için parametreleri ve hafıza geçişlerini hesaplayın.
  计算预训中添加MTP 模块的参数和内存开销
- Bir MTP modülü sıfırdan uygulayın: paylaşılan gömülme, derinlik dönüştürücü bloğu, projeksiyon ve paylaşılan çıkış başlığı.
  Bir MTP modülü: ortak yerleşim, her derinlik transformatör blokları, projekssiyon ve ortak çıkış başları

## Sorunlar. Sorunlar.

Sonraki belirti tahminleri standart LLM eğitim hedefi. Her gizli durum tam olarak bir şeyi tahmin etmek için denetlenir: hemen sonraki simge. Bu şaşırtıcı derecede zayıf bir sinyal. Bir dizi içinde bulunan bilgilerin çoğu bir simge  yapısı, tutarlılık, gerçeklik, aritmetik akıştan daha öte uzanır. Modelle, bunları, bir bilyon simgelerin üzerinde bir tek sinyal sinyallerini biriktirerek öğrenmek zorundadır.

> Aşağılık token 预测是标准 LLM 训练目标──每个隐藏状态被监督预测恰好一个事:紧接下来的下一个 token──这是一个惊人的弱信号──序列中的大部分信息延伸到单个 token 之外结构、连贯性、事实性、算术流程──模型必须通过在亿个 token 上积累许多单个 token 信号来学习这些──

MTP soruyor: Ya her gizli durum birden fazla gelecekteki token tahmin etmek için denetlenirse? Gloeckle et al. (Meta, 2024) bunun yardımcı olduğunu gösterdi. Uygulamaları, her biri farklı bir ofset öngörerek omurganın üzerine birkaç bağımsız çıkış başını koydu. Paralel, basit, ama başlar herhangi bir hiyerarşik gelişme olmadan aynı gizli durumu gördü  ve tahminler nedensel olarak zincirlenmedi, bu yüzden spekülasyonsal dekodlama için kullanılamadı.

> MTP 问: Eğer her gizli durum aynı zamanda izlenirse, nasıl bir gelecek belirtiyi öngörür?Gloeckle 等人(Meta,2024) bunun yardımcı olduğunu göstermektedir.

DeepSeek-V3 (Aralık 2024) MTP'yi, her tahmin derinliğinde nedenci zinciri tutan ardıcıl modüller olarak yeniden tasarladı.`t+1`-`h_i^(0)`Sonra tahmin eder .`t+2`Yeni bir gizli durumdan.`h_i^(1)`Bu da bir arada.`h_i^(0)`- ... ...`E(t+1)`DeepSeek-V3'ün ölçeğinde, 671B ana model ağırlıklarının üzerinde MTP modüllerindeki 14B ekstra parametreler. Bu% 2 overhead daha yoğun eğitim sinyalleri satın aldı ve sonuçta hazır bir spekülasyonsal dekodeleme taslakı aldı.

Bu ders tek bir MTP modülü oluşturur ve sıfırdan D derinliği kaybı.

## Konsepten bir şey.

> **【中文解读】**Çoklu token  tahmin etmek için bir model aynı zamanda çoklu gelecek tokenlerini tahmin etmesi için, daha zengin bir eğitim sinyalini sağlamak için kullanılır.

> **【拓展：Meta 的多 token 预测研究】**Meta'nın 2024 yılında yayınladığı bir makalede, 4-token  öngörüsü, kod üretimi ve düşünme görevlerinde standartın bir sonraki token'dan önemli ölçüde daha iyi olduğunu göstermiştir. DeepSeek-V3 ayrıca yardımcı çoklu token kullanmıştır.


### Sıradan MTP tarifi

DeepSeek-V3 ekliyor `D`Ana modelin üzerinde MTP modüller.`k`(çünkü)`k = 1..D`) simgeyi derinlikten tahmin eder .`k` yani, `t_{i+k}`konumdan önce bir önbellek verilmiştir.`i`- Evet .

Modül`k`aşağıdakilerden oluşur:

- Bir transformatör bloğu .`T_k`Kendi dikkatini ve MLP'yi.
- Bir projeksiyon matrisi `M_k`Önceki derinlik gizli durumunu birleştiren ve bir sonraki derinlik temel gerçeği simgesi yerleştiren.
- Paylaşılan yerleşim `E`(Ana modelle aynı).
- Paylaşılan çıkış başlığı `Out`(Ana modelle aynı).

Eğitim sırasında, pozisyon üzerinden bir önbellek için `i`, derinliklere göre gizli durum:

```
h_i^(0) = main model backbone at position i
h_i^(k) = T_k( M_k * concat(RMSNorm(h_i^(k-1)), RMSNorm(E(t_{i+k}))) )   for k >= 1
```

Derinlik tahminleri:

```
logits_{i+k} = Out(h_i^(k-1))   for k = 1..D
```

Derinlik kaybı , temel gerçeğe karşı çapraz entropi .`t_{i+k}`- ...

```
L_k = CE(logits_{i+k}, t_{i+k})
```

Derinlikler boyunca eklem kaybı:

```
L_MTP = (lambda / D) * sum_{k=1..D} L_k
```

`lambda`DeepSeek-V3'de ilk %10 eğitim için 0.3 kullanılır ve sonrasında 0.1 kullanılır.`L_main + L_MTP`- Evet .

### Neden paralel değil, sıralı?

Gloeckle'nin orijinal paralel MTP'sinde D çıkış başları vardı, her biri doğrudan `h_i^(0)`Her baş tahmin ediyor .`t_{i+k}`Bu trenler iyi, ama tahminler birbirine bağlı değil.`head_1`Yardımcı çıkış .`head_2` kafalar paralel ateş eder.

DeepSeek-V3'ün dizaynı devamlı inşa ediliyor.`h_i^(k)`-`h_i^(k-1)`artı gerçek bir sonraki simge yerleştirme `E(t_{i+k})`Bu sebepli zinciri korur: tahmin etmek .`t_{i+k+1}`, derinlik modülü `k+1`Ne olduğunu görüyor.`t_{i+k}`Bu, yapısal olarak bir autoregressive dekoder'in kendi çıkışını tüketmesine benzer.

Sonuç: besin `h_i^(k-1)`ve taslağı`t_{i+k}`modülüne`k+1`, bir tahmin edin .`t_{i+k+1}`Tekrarlıyorum. Bu tam olarak EAGLE tarzı bir taslak, eğitimli MTP modülü kullanarak taslak ağ. DeepSeek-V3 ilk MTP modülü üzerinde %80+ kabul ve ~1.8x hızlanma rapor ediyor.

### Parametre muhasebe

Gizli bir model için .`h`ve kelime hazinesi `V`- ...

- Ana model: milyarlarca parametre, artı bir çıkış başlığı boyutu `V * h`- Evet .
- Paylaşılan çıkış başı: Ana modelin başını tekrar kullanın.
- Paylaşılan yerleştirme: Ana modelin yerleştirmesini yeniden kullan.
- MTP modülü başına:
  - Proje `M_k`- Evet .`(2h) * h = 2h^2`- Evet .
  - Transformer blokları `T_k`: dikkat (`4h^2`MHA için) artı MLP (genellikle `8h^2`SwiGLU için 8/3 oranı ile.`12h^2`- Bir blok için.

Modül başına toplam ekme: `~14h^2`DeepSeek-V3 için.`h = 7168`, D = 1 modül: `~14 * 7168^2 = ~720M`DeepSeek-V3 raporları 14B  fark çoğunlukla uzman katmanları MTP modülünde de MoE olmak.

### Spekülatör çözme ödülü

Ön eğitim sırasında, MTP modülleri eğitimini yaklaşık %10 yavaşlatır (daha ileri hesaplama, ekstra kayb).

1. Denser eğitim sinyali. Her gizli durum D+1 denetim hedeflerini görür. MMLU, GSM8K, MATH, HumanEval üzerindeki ölçülmüş etki: DeepSeek-V3'ün ablasiyonlarında tutarlı birkaç yüzde puan iyileştirmeler.

2. MTP modülü, önümüzdeki birkaç token'ı tahmin etmek için zaten eğitilmiştir. Bir proje ağı olarak yeniden tasarlanmıştır, %80+ kabul oranları sunar. Bu seviyede, N=3 veya N=5 spesifik çözme 1.8x throughput verir. İlk kez sonuçlar çıkarırken %10 eğitim süresi maliyeti ödenir.

### KİÇİN ile ilişki

EAGLE, küçük bir taslak modeli önceden eğitimden sonra SEPARATEL olarak eğitir. MTP taslakı önceden eğitim içine pişirir.

| Dimension | EAGLE-3 | MTP (DeepSeek-V3) |
|-----------|---------|------------------|
| When trained | Post-pre-training | During pre-training |
| Backward-compatible with existing weights | Yes | No (need to re-train) |
| Draft params | 1-2 transformer layers | 1 transformer block + projection |
| Acceptance rate | 0.88-0.92 | 0.80+ at depth 1 |
| Benefit beyond speedup | Speculative decoding only | Denser training signal + speedup |


> **【拓展：多 token 预测与推理加速的联系】**Çok token  öngörü eğitiminin modeli doğal olarak uygundur投机解码 çünkü gelecekteki çok token tahmin etmeyi öğrenmiştir──Meta'nın araştırması, 4-token  öngörü eğitiminin modeli kod üretimi standard eğitimden %5-10 oranında yükseldiğini göstermektedir──


## Yapın.
```figure
multi-token-predict
```

## Yapın

`code/main.py`MTP modülü bir son son oluşturur: paylaşılan gömülme, projeksiyon, transformatör bloğu, paylaşılan çıkış başlığı. Daha sonra kısa bir sentetik dizide derinlik çapraz entropi kaybını hesaplar ve bileşenler tarafından parametrelerin sayısını yazdırır. 32 jetonlu bir oyuncak sözlük sayısı okunur.

### Adım 1: Paylaşılan yerleştirme masası

Tek bir tane .`vocab_size x hidden`Tablo, her derinlikte ana model ve her MTP modülü tarafından kullanılır.

### Adım 2: derinlik kombinasyonu

```python
def combine(prev_hidden, next_token_embed, M_k):
    # concat along feature dim, then project down to hidden
    concat = rms_norm(prev_hidden) + rms_norm(next_token_embed)  # vector addition stand-in
    projected = matvec(M_k, concat)
    return projected
```

Gerçek DeepSeek-V3 iki RMSNormed vektörünü birleştirir .`[2h]`ve bir `h x 2h`Oyuncak stdlib kısaltması için vektör eklemesini kullanıyor.

### Adım 3: K derinliğinde transformatör blok

Kendi dikkatini artı MLP. Oyuncakta, bir katmanlı bir çizgiden dikkat bloğu ve SwiGLU MLP yapıyı numpy olmadan görünür tutmaktadır.

### 4. adım: Paylaşılan çıkış başlığı

Ana modelin çıkış projesi tekrar kullanın.

### Adım 5: Derinlik kaybı

Softmax'ın (logits) karşı karşıya geçiş sırasında yeraltı gerçeği simgesi karşı karşıya geçmesi`k`- Deniz derinliklerinde toplanıp `lambda / D`Ölçekleme faktörü.

### Adım 6: Parametre muhasebe

Toplam parametreler sayısını, paylaşılan (eğlenme, baş) sayısını ve modül başına ek sayıyı basın.

## Çerçeveyi kullanın.

MTP, DeepSeek-V3 (Aralık 2024) ve DeepSeek-R1 serisine entegre edilmiştir.

- DeepSeek'in kendi servis yığını, MTP modülleri kasadan çıkmış spekülatör kodlayıcılar olarak tüketir.
- vLLM ve SGLang'ın Nisan 2026'dan itibaren DeepSeek-V3 MTP için entegrasyon yolları vardır.
- AMD'nin ROCm SGLang öğretim kitabı, V3 kontrol noktasında ölçülen 1.8× hızlandırma ile belirli bir MTP spekülasyonsal dekodlama yapılandırmasını gösterir.

Yeni bir eğitim öncesi koşuda MTP'yi ne zaman kullanmalısınız:

- Bütün antrenman öncesi boru hattını kontrol ediyorsun ve daha yoğun bir antrenman sinyali bankalamak istiyorsun.
- Model'e ölçekte hizmet vereceğini ve spekülasyonu ücretsiz olarak çözmek istediğini biliyorsun.
- Gizli boyutunuz en az 4096'dır. 1B ölçekinde, üst maliyet kazançtan daha fazla zarar verir.

Ne zaman yapmamak:

- MTP modülü eğitilmemiş.
- Temel bir temel çizgiyi karşılaştırmak için araştırma modelleri.

## İndirin . Ürünler .

Bu ders bize çok yararlı .`outputs/skill-mtp-planner.md`. Eğitim öncesi bir çalışma özellikini (model boyutu, veriler, hesaplama) göz önüne alarak, MTP'yi entegre etme planını gönderir: derinlik sayısı D, `lambda`Zamanlama, hafıza yükleme ve sonucu zaman spekülasyonu çözme kabloları.

> 本课产 出 `outputs/skill-mtp-planner.md`△ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △                                                                                  `lambda`调度、内存开销和推理时投机解码连线──

## Egzersizler.

1. Çık .`code/main.py`.Sintez sinyali güçlendikçe derinlik kaybının monoton olarak azalmasını göster.Sintezi sabit bir kalıp kullanmak için değiştirin ve hem derinlik-1 hem de derinlik-2 kaybının birleştiğini doğrulayın.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`code/main.py` her derinlik kaybını göstermek, sendikat sinyallerini güçlendirmek, tek düzenlemeyi azaltmak, sendikat verilerini sabit bir modülün kullanımı ile değiştirmek ve derinlik 1 ve derinlik 2'nin kaybını doğrulamak.

2. D = 1 MTP modülü olan yoğun 70B modeli için (goyduğu 8192, 80 katman) parametreler üstünü hesaplayın. DeepSeek-V3 rapor ettiği 14B üstünü karşılaştırın. DeepSeek'in sayısının neden daha yüksek olduğunu açıklayın: MTP transformatör bloku aynı MoE yapısını miras alır ve modül başına parametreler sayısını yükseltir.
   Çin dilinde:计算密集 70B 模型(hidden 8192,80 层)加 D=1 MTP 模块的参数开销。与DeepSeek-V3 报告的 14B 开销比较。解释为什么DeepSeek 的数字更高:MTP 变压器块继承了相同的MoE 结构,膨胀了每块参数──

3. Oyuncakta D=2 uygulamak: h^(1) alan ve tahmin eden ikinci bir MTP modülü ekle`t_{i+2}`- Ortak kayıp ve parametreler hesaplamaları DeepSeek kağıdının 19-21 denklemlerine uygun olduğunu kontrol edin.
   Çinçe Çevirim: Oyuncu Modülünde D=2 gerçekleştirmek: ikinci MTP 模块 ekle, h^(1) 并预测 `t_{i+2}` Testing Joint Loss and Parameter Clearance with DeepSeek 论文公式 19-21 匹配──

4. Oyuncakları paralel MTP'ye (Gloeckle tarzı) değiştirin: D çıkış başlıklarını ana gizli durumun üstüne ekleyin, her biri farklı bir sıyrıtı öngörür.
   Çinçe çevirisi:将玩具模型切换为并行 MTP(Gloeckle风格): Hedef gizli durumunda D 个输出头, her tahmin farklı yönlü bir hareketle eklenir.

5. Eğlence tarzında bir taslak olarak eğitimli MTP modülü kullanın: önermek için k modülünü çağırın `t_{i+k}`Bu taslak tokenlerinin kabul oranını, baş modelin beklenen bir dizi üzerinde tahminlerine göre ölçün. Oyuncak üzerinde %50+'e ulaşırsanız, empiri MTP-as-draft özelliğini yeniden üretmiş olursunuz.
   Çin Çeviri:                                                                                                                                                                                                                                                            `t_{i+k}` Bu taslakları, saklama sırasında ölçerek ana model tahminlerinin kabul oranına karşı kullanılır. Eğer oyuncak modeli üzerinde %50'e ulaşırsanız, MTP-as-draft deneyimi özelliklerini yeniden elde etmiş olursunuz.

## Anahtar Şartlar .

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|------------------------|---------|
| MTP module | "Extra loss block" | A small transformer block plus projection that predicts a token `k` positions ahead of the main model | MTP 模块，预测主模型后方第 k 个 token |
| Prediction depth | "Which offset" | The integer `k` such that module `k` predicts `t_{i+k}` from prefix through position `i` | 预测深度，模块 k 预测第 i+k 个 token |
| Parallel MTP | "Gloeckle-style" | D independent heads on the same backbone hidden state, no conditional chain | 并行 MTP，D 个独立头共享隐状态 |
| Sequential MTP | "DeepSeek-V3 style" | Each module conditions on the previous depth's hidden state plus the next token's embedding; preserves causal chain | 顺序 MTP，每层依赖前一层隐状态，保持因果链 |
| Shared output head | "Reuse the main head" | The MTP modules call the main model's LM head, not a separate output projection | 共享输出头，MTP 模块复用主模型的语言模型头 |
| Shared embedding | "Reuse the main table" | Same vocabulary embedding table is used everywhere; no duplicate parameters | 共享嵌入，复用词表嵌入表 |
| Projection matrix M_k | "Combine hidden + next-token" | An `h x 2h` linear层 that folds the previous hidden state and the target-token embedding into the next depth's input | 投影矩阵，组合隐状态与下一 token 嵌入 |
| Joint loss L_MTP | "Averaged extra losses" | Arithmetic mean of per-depth cross-entropy losses, scaled by `lambda` | 联合损失，各深度交叉熵损失的算术均值 |
| Acceptance rate at depth 1 | "How often MTP draft is right" | The rate at which the D=1 MTP module's top-1 prediction equals the main model's top-1 prediction; 80%+ on DeepSeek-V3 | 深度 1 的接受率，MTP 草稿与主模型一致的概率 |
| Lambda weighting | "Extra-loss importance" | Per-depth scaling factor; 0.3 at start of training, 0.1 later on DeepSeek-V3 | Lambda 权重，每深度损失的缩放因子 |

## Daha fazla okumak

- [DeepSeek-AI — DeepSeek-V3 Technical Report (arXiv:2412.19437)](https://arxiv.org/abs/2412.19437) toplam bir dizi MTP açıklaması (Bölüm 2.2), ortak kayıp denklemleri ve sonuçta 1.8× hızlandırma dahil
- [Gloeckle et al. — Better & Faster Large Language Models via Multi-token Prediction (arXiv:2404.19737)](https://arxiv.org/abs/2404.19737) paralel MTP temel hattı DeepSeek'in tasarımı
- [DeepSeek-V3 model card on Hugging Face](https://huggingface.co/deepseek-ai/DeepSeek-V3) 685B toplam (671B ana + 14B MTP), yerleştirme notları
- [Leviathan et al. — Fast Inference from Transformers via Speculative Decoding (arXiv:2211.17192)](https://arxiv.org/abs/2211.17192) spekülatör kodlama çerçevesinin MTP'si
- [Li et al. — EAGLE-3 (arXiv:2503.01840)](https://arxiv.org/abs/2503.01840) EAGLE'nin 2025 tarihli tasarımı, karşılığı MTP ile rekabet ediyor
