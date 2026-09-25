# Doğal Çekilme Dikkat (DeepSeek NSA)

> 64k tokenlerde dikkat, çözme gecikme sürecinin %70-80'ini tüketir. Her açık model laboratuvarın bunu düzeltmek için bir planı var. DeepSeek'in NSA (ACL 2025 en iyi kağıdı) sıkıştığı bir şey: üç paralel dikkat dalı  sıkıştırılmış kaba tanelerli jetonlar, seçici olarak saklanan ince tanelerli jetonlar ve yerel bağlam için kaydırıcı pencereler  öğrenilmiş bir kapıdan birleştirilmiştir. Hardware-ağır (kernel dostu), doğuştan eğitimlenebilir (doğrudan eğitimde çalışır, çıkarma sırasında bağlanmaz) ve 64k dekodlarda tam dikkat kalitesini eşleştirirken veya yenirken FlashAttention'dan daha hızlı çalışır. Bu ders üç dalı sonundan sonuna kadar inşa eder ve neden kısıtlılığın sonundan sonuna kadar farklılaştırılabileceğini gösterir.

> **【中文解读】**64K token 时注意耗 70-80%解码延迟──DeepSeek NSA(ACL 2025 最佳论文) သုံး条并行注意力分支解决:压缩粗粒度 token、选择保留细粒度 token、滑窗局部上下文,通过可学习门控组合──硬件友好、可预训、比FlashAttention更快──

> **【拓展：稀疏注意力→长上下文】**长上下文(64K-128K token) 2025-2026 yıllarındaki büyük modelin çekirdek kapasitesidir. NSA, MHA, GQA, dikkat hesaplama karmaşıklığını azaltma için bir çözümdür.

>  **【前置】**Öğrenci bölümünün ilk aşaması: 10·16                                                                                                                                                                                                                                                         
>  **【类比】**NSA = 看长文档的三种策略同时进行:**压缩分支**= 看目录摘要(粗粒度);(2) **选择分支**= 重点看自己感兴趣的章节 (seçimsellik)**滑动窗口**= 当前页前后 5 页仔细看(局部上下文) ・・・门控(gate) = Her pozisyonun hangi stratejiyi kullanması gerektiğini, otomatik olarak en iyi kombinasyonu öğrenmesini kararlaştırmak

**Type:** Build
**Languages:** Python (stdlib)
**Prerequisites:** Phase 7 · 12 (KV cache, flash-attention), Phase 7 · 15 (attention variants), Phase 10 · 16 (differential attention)
**Time:** ~60 minutes

## Öğrenme hedefleri

- NSA'nın üç dikkat şubesini ve her birinin ne yakaladığını anlat.
  NSA'nın üç dikkat bölümü ve onların yakaladığı bilgiler
- NSA'nın neden "doğal olarak eğitimlenebilir" olduğunu açıklayın, daha önce sadece sonuçlandırma yöntemleri kullanılmışken.
  NSA'nın neden "doğru eğitimli" olduğunu ve önceki nadir dikkat yöntemi sadece düşünce için kullanılabileceğini açıklayın.
- NSA'nın 64k bağlamında tam dikkat karşısında dikkat hesaplama tasarrufini, sıkıştırma blok boyutu ve seçim üst-k fonksiyonu olarak hesaplayın.
  計算在 64K 上下文中 NSA 相对全注意的计算节省量 (Bölümleme bloklarının büyüklüğü ve seçme üst-k'ın işlevi olarak)
- stdlib Python'da üç dallı kombinasyonu kısa bir sentetik dizide uygulayın ve kaplama ağırlıklarının davranışlarını doğrulayın.
  Python'un kısa bir yapım dizisinde üç parça birleştirme, test ve kontrol etmesi için kullanılır.

## Sorunlar. Sorunlar.

Dönem uzunluğunda tam dikkat N maliyetleri `O(N^2)`Zaman ve `O(N)`KV kasesi katman başına. 64k tokenlerde, hesaplama ve bellek bant genişliği rakamları felaketlidir. NSA kağıdından ölçülen teorik tahmin: dikkat toplam dekodlama gecikme sürecinin 70-80%'ini 64k'de oluşturur. Her şey aşağı akıntıda  TTFT, token / saniye, milyon token başına maliyet  dikkat maliyetinin baskısıdır.

> 序列长度 N'in tüm dikkat maliyeti `O(N^2)`Zaman ve her kat`O(N)`KV 缓存── 64k token 时,计算和显存带宽的数字是灾难性的──NSA 论文的测量理论估计:64k 时注意占据总解码延迟的70-80%──所有下游指标TTFT、代币/秒、每百万代币 成本都由注意成本主导──

Dikkatin az olması açık bir yanıt. Önceki girişimler iki kovaya düştü. Sıkıntılı kalıcı (slip-fenestesi, adımlı, blok-yalı) bilgiyi atıyor ve uzun mesafeli hatırlama görevlerinde başarısız oluyor. İnferans-zaman kısıtlılığı (KV cache pruning, H2O, StreamingLLM) yoğun dikkat üzerinde önceden eğitilmiş bir modele uygulanır ve modelden kısıtlı örneğin yoluyla bilgiyi yönlendirmesi istenmediğinden potansiyel hızlandırmanın sadece bir kısmını geri kazanır.

> 稀疏注意力 (稀疏注意力) iki sınıfta ayrılmıştır. 稀疏注意力 (Fixed Mode) 稀疏性 (sızdırıcı pencereler, geçişler, bloklar) bilgiyi bırakır ve uzun süreli hatırlama görevinde başarısız olur. 推理时稀疏性 (KV) 缓存剪枝、H2O、StreamingLLM) yoğun dikkat üzerinde yapılan eğitim modellerinde kullanılır.

Native Sparse Attention (Yuan et al., DeepSeek + PKU + UW, ACL 2025 best paper, arXiv:2502.11089) her ikisini de yapar: modelin önceden eğitim sırasında öğrendiği bir arzanlık kalıbı, aslında hesaplama tasarrufu sağlayan bir çekirdek-ağır algoritma olarak uygulanır.

> İlk kez, yeni bir model geliştirildi ve yeni bir model oluşturuldu. İlk olarak, yeni bir model geliştirildi ve yeni bir model geliştirildi.

## Konsepten bir şey.

> **【中文解读】**O'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'n'

> **【拓展：长上下文的稀疏注意力方案】**稀疏注意力工程实现包括:滑动窗口(Mistral'ın 32K 窗口) + 全局 token([CLS]) + 选择性关注。Google'ın Ring Attention 和 Block-Sparse Attention 将上下文扩展到百万 token──DeepSeek'in NSA(Native Sparse Attention) 在训练中直接学习稀疏模式──


### Üç paralel dal

Her sorgu için NSA, KV önbellekinin üç farklı görünümüne karşı dikkatini üç kez çalıştırır:

1. **Compressed branch.**Tokenler büyüklükte bloklara gruplandırılır `l`Her blok küçük bir öğrenilmiş MLP aracılığıyla tek bir özetleme tokene sıkıştırılır. sorgu, tüm dizinin kaba bir görünümünü elde ederek bu sıkıştırılmış tokenlere katılır.

2. **Selected branch.**Sıkıştırılmış daldan dikkat puanlarını kullanarak, mevcut sorgu için en uygun üst-k blokları belirlenir. Bu bloklardan ince tohumlu (sıkıştırılmamış) işaretler okunuyor ve sorgu hepsinin üzerinde çalışır. Seçim için yönlendirme sinyali olarak sıkıştırılmış dal dikkatini düşünün.

3. **Sliding-window branch.**Sorgu son soruları cevaplıyor `W`Bu dal diğer iki kişinin kaybedebildiği yapı ağır kısa aralık kalıpları (sintaks, yerel çekirdek referansı) yakalar.

Üç dal çıkışı, öğrenilen bir pozisyon kapısı üzerinden birleştirilir:

```
out = g_cmp * out_cmp + g_sel * out_sel + g_win * out_win
```

`g_cmp, g_sel, g_win`Sorguda küçük bir MLP'den geçit ağırlıkları bulunmaktadır. 1 'ye toplamına gerek yoktur.

### Neden bu "doğal olarak eğitilebilir"

Seçim adımları (top-k blokları) ayrıdır. Diskret işlemler gradient akışını kırar. Önceki nadir dikkat çalışmaları ya seçimi (yasaklama eğitimi) üzerinden geriye atladı veya sonuçta gerçek nadirlik vermeyen sürekli gevşeklemeler kullanıldı.

NSA bunu atlıyor: sıkıştırılmış dal dikkat tüm dizide farklılaştırılabilir kaba tohumlu bir dikkat. Top-k işlevi, baskı dalının en yüksek dikkat puanlarını kullanarak hangi ince tohumlu blokları yüklemek istediğini seçer. Gradiyentler sıkıştırılmış dal puanları (bütün sıkıştırılmış çıkış ve seçim mantığı etki eden) üzerinden akıyor ve seçilen blokların nihai çıkışa katkısı da farklılaştırılabilir. Farklı olmayan `top_k`İşlem ileri hesaplama grafikinde bir işlemi yok. Sadece hangi blokların hafızadan yüklendiğini kontrol eder.

Bu nedenle NSA'nın eğitim öncesi end-to-end kullanılabilmesi için kullanılabilir. Model, üç dalın üzerinden bilgiyi birlikte yönlendirmeyi öğrenir ve sonuçta söz verilen hızlandırmayı gerçekleştirecek nadir bir kalıp üretir.

### Hardware-ağırlaştırılmış çekirdek

NSA çekirdeği modern GPU bellek hiyerarşileri için tasarlanmıştır. çekirdeği GQA grupları (dış döngü) tarafından sorguları yükler, grup başına karşılık gelen nadir KV bloklarını (dahalik döngü) alır ve SRAM'a dikkat çeker. Her sorgu grubu aynı seçilen blokları gördüğü için (seçim sorgu grubu, sorgu başı değil) KV yükleri grubun her yerinde amortize edilir.

Kağıt, 64k dekodlarda Triton çekirdeklerinin FlashAttention'dan 9 kat daha hızlı çalıştığını, hızlandırma oranının dizi uzunluğu ile artışla artışla rapor ediyor.

### Bilgisayar bütçesi

- Bırak .`N`Dönem uzunluğu, `l`Sıkıştırma blok boyutu, `k`en üst k seçimi sayısı, `w`kaydırıcı penceresi,`b`Seçilen blok boyutu (genellikle `l`)

- Sıkıştırılmış dal: `O(N/l)`sorguya göre anahtarlar, yani `O(N * N / l)`- Toplam.
- Seçili dal: `O(k * b)`sorguya göre anahtarlar, yani `O(N * k * b)`- Evet .
- Çekilen dal: `O(w)`sorguya göre anahtarlar, yani `O(N * w)`- Evet .

Toplam: `O(N * (N/l + k*b + w))`- Evet .

- Evet .`N = 64k, l = 64, k = 16, b = 64, w = 512`: sorguya göre maliyet `1000 + 1024 + 512 = 2536 keys`Tam dikkat .`64000 keys`25 kat daha az hesaplama.

- Evet .`N = 128k, l = 64, k = 16, b = 64, w = 512`: sorguya göre maliyet `2000 + 1024 + 512 = 3536 keys`Tam dikkat .`128000 keys`36x azaltma. Fayda dizi uzunluğu ile büyür, bu da tüm noktayı.

### Nasıl karşılaştırılır?

| Method | Differentiable | Real inference speedup | Long-range recall |
|--------|---------------|----------------------|-------------------|
| Sliding window only | yes | yes | fails |
| Strided / block-sparse | yes | yes | partial |
| KV pruning (H2O, StreamingLLM) | N/A (inference-time) | yes | partial |
| MoBA (Moonshot) | partial | yes | good |
| NSA | yes (natively) | yes (9x at 64k) | matches full attention |

MoBA (Moonshot, arXiv:2502.13189) aynı anda yayınlandı ve dikkat bloklarına MoE ilkesini uygulayan benzer bir üç-birden daha iyi bir yaklaşım kullanıyor. NSA ve MoBA 2026 uzun bağlamlı önceden eğitim için bilinen iki mimaridir.


> **【拓展：稀疏注意力在长上下文中的应用】**密集注意力 O(n^2) 计算量使 128K 上下文的预填充阶段需要约30秒──稀疏方法(如 NSA、Ring Attention) 将其降至可接受范围──Gemini 1.5 Pro'nun 1M token 上下文依赖于稀疏注意力──


## Yapın.
```figure
sliding-window-attention
```

## Yapın

`code/main.py`Üç dalı kısa bir sentetik sıraya uyguluyor ve gösterir:

- Sıkıştırma MLP (pedagojik açıklık için basit bir ortalama havuz tabanı kullanılır; gerçek NSA öğrenilmiş bir MLP kullanır).
- Top-k blok seçimi, sıkıştırılmış dal puanları ile yönlendirilir.
- Sonuncuda kaydırıcı pencerenin dikkatini çek .`w`- Tokenler.
- Kapalı kombinasyon.
- Tam dikkatle karşılaştırılan bir hesap sayımı baskı.

### Adım 1: Token'leri bloklara sıkıştır

```python
def compress(K, l):
    n = len(K)
    n_blocks = (n + l - 1) // l
    out = []
    for b in range(n_blocks):
        start, end = b * l, min((b + 1) * l, n)
        block = K[start:end]
        summary = [sum(row[d] for row in block) / len(block) for d in range(len(K[0]))]
        out.append(summary)
    return out
```

### Adım 2: Sıkıştırılmış dal dikkat

Sıkıştırılmış anahtarlara karşı sorunun softmax dikkatini çalıştırın.

### Adım 3: Üst k blok seçimi

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `k`En yüksek puan veren sıkıştırılmış bloklar.

### 4. adım: Çekilme penceresi dikkat

Sonuncusu al .`w`Tokenleri kullanın ve standart dikkatle onlara karşı çalışın.

### Adım 5: kapı + kombinasyon

Sorgu üzerinde küçük bir MLP, üç kapı ağırlığını üretir. Nihai çıkış, üç dal çıkışının ağırlıklı toplamıdır.

### Adım 6: Hesaplama sayımı

Her dal için sorgulama başına katılan anahtar sayısını ve toplamı basın.`N`1024 simgesel bir sentetik üzerinde.`l = 32, k = 4, w = 128`NSA ' nin gördüğü gibi .`32 + 128 + 128 = 288`Tam dikkat için sorgu başına anahtarlar karşılaştırıldığında 1024  3,5 kat daha az.

## Çerçeveyi kullanın.

NSA, DeepSeek'in kendi uzun bağlamlı önceden eğitim hattında yayınlıyor.

- **DeepSeek internal**: yerel, yayınlanan ağırlıklar NSA veya onun halefi DSA (Deepseek Sparse Attention) kullanır.
- **vLLM**: DeepSeek-V3.x ağırlıkları için NSA deneysel desteği geliştirilmektedir.
- **SGLang**: NSA referans değerleri yayınlandı; üretim yolu vLLM'yi takip ediyor.
- **llama.cpp / CPU**: desteklenmiyor; çekirdek parçalanmasının genel maliyeti CPU geçişinde değmez.

NSA'ya ne zaman ulaşmak:

- Ciddi bir hesaplama bütçesi olan 64k'dan fazla konuya yönelik bir önceden eğitim veya devamlı eğitim çalışması.
- DeepSeek'in kendi uzun bağlamlı kontrol noktalarının tespit edilmesi.

Ne zaman yapmamak:

- NSA'yı eğitimsiz bir şekilde yeniden yapılandıramazsın.
- 16k'ın altında. 3 şubenin üst düzey maliyeti tasarrufları ele geçirir.
- Batch-1 interaktif sohbet, gecikme hassaslığı faydalanacak, ancak sadece uzun bağlamlarda.

## İndirin . Ürünler .

Bu ders bize çok yararlı .`outputs/skill-nsa-integrator.md`. Uzun bağlamlı bir önceden eğitim çalışması özellikleri göz önüne alındığında, NSA entegrasyon planı üretir: sıkıştırma blok boyutu, üst-k, kaydırma penceresi, kapı MLP genişliği, çekirdeğin seçimi ve mimarlık değişikliğini haklı çıkaracak belirli uzun bağlamlı değerlendirmeler.

> 本课产 出 `outputs/skill-nsa-integrator.md`◊ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒      ⇒                                                                                                                                                                           

## Egzersizler.

1. Çık .`code/main.py`1024 simgesel bir sentetik üzerinde.`(l, k, w)`Üç ön ayar ve baskı hesap sayımında. İğne-haystack testinde tam dikkat karşısında 95% hatırlama yaparken, sorgu başına en düşük anahtar sayısını elde eden ön ayarı tanımlayın.
   Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Çın Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç`code/main.py`◊ üç ön planda tarama`(l, k, w)`Ve basın hesaplama miktarı. Haystack testinde toplam dikkatini 95%  çağırma oranı ile aynı zamanda en düşük her sorgu anahtarı hesaplama öngörüsü gerçekleştirmek için bulunmaktadır.

2. Ortalama havuz kompresörü küçük bir öğrenilmiş MLP (2 katman, gizli 32) ile değiştirin. Sinyalın bir blokun ortalaması olduğu sentetik bir görev üzerinde çalıştırın.
   Çinçe çevirisi: Küçük öğrenme MLP ile değiştirmek için iki katlı, gizli 32) ortalama değerli bir kemikli basınç makinesi.

3. Kapı MLP uygulamasını uygulayın. Sorgu giriş olarak alır ve üç ölçekçi çıkardı. Kapının akıllıca davrandığını gösterin: rastgele sorgularda neredeyse birerli ağırlık, sorgu uzak arka bloklara çarpınca seçilen dal üzerinde ağırlık.
   Çinçe çevirisi: gerçekleştirmek için giriş kontrolü MLP── sorgu ile giriş için çıkış üç ölçüm¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬

4. NSA tarafından etkinleştirilen 70B modeli için KV önbelleği hafıza bütçesini 128k bağlamda hesaplayın. KV başları 8, başı 128, BF16. Tam dikkatle ve MLA ile karşılaştırın (Fase 10 · 14 MLA'nın numaralarını gösterdi). NSA'nın ince taneleri olan dal KV önbelleğinin tam dikkatle eşit olduğu sekans uzunluğunu belirleyin.
   Çin dilinde çevirme: hesaplama NSA  başlatılan 70B  model  KV 缓存内存预算在 128K 上下文下面 KV 缓存内存预算。KV 头 8 个,头维度 128,BF16。与全注意力和MLA比较。找到 NSA 细粒度分支 KV 缓存等于全注意序列长度。

5. NSA kağıdı'nın 4. bölümünü okuyun (arXiv:2502.11089) ve sıkıştırılmış dalın dikkat puanlarının neden ayrı bir yönlendirme puanı hesaplamaktan ziyade üst-k seçimi için tekrar kullanıldığını üç cümleyle açıklayın. Cevabı gradient akışına bağlayın.
   Çinçe çevirisi: NSA'nin 4. bölümünü okuyun, neden basınçlı bölgelerin dikkat oranı top-k  seçimi yerine hesaplama ayrı yolların oranını kullanmak için üç cümle ile açıklayın.

## Anahtar Şartlar .

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|------------------------|---------|
| Compressed branch | "Coarse view" | Attention over block-averaged keys that provides global context in O(N/l) keys per query | 压缩分支，块平均键上的注意力 |
| Selected branch | "Top-k blocks" | Fine-grained attention over the `k` blocks with highest compressed-branch scores | 选择分支，对 top-k 块做细粒度注意力 |
| Sliding window | "Local context" | Attention over the last `W` tokens for short-range patterns | 滑动窗口，最近 W 个 token 的局部上下文 |
| Native trainability | "Pre-train with the sparsity on" | The sparsity pattern is learned during pre-training, not bolted on at inference | 原生可训练，预训练时就使用稀疏模式 |
| Compression block size l | "Group size for coarse view" | How many tokens get merged into one summary; 32-64 typical | 压缩块大小，每组合并多少 token |
| Top-k | "Blocks to keep" | Number of compressed blocks whose uncompressed tokens get read; 16 typical | Top-k，保留的压缩块数量 |
| Sliding window W | "Local attention radius" | Typically 512; shorter hurts local coherence, longer wastes compute | 滑动窗口大小，典型值 512 |
| Branch gate | "How to mix the three" | Per-position MLP output that weights the three branches' contributions | 分支门控，MLP 输出加权三分支贡献 |
| Hardware alignment | "Kernel-friendly sparsity" | Sparse pattern chosen so that the actual GPU kernel achieves the theoretical speedup | 硬件对齐，稀疏模式适配 GPU 核函数 |
| DSA | "NSA's successor" | Deepseek Sparse Attention, the architecture that followed NSA in DeepSeek's lineage | DSA，DeepSeek 稀疏注意力，NSA 的后继架构 |

## Daha fazla okumak

- [Yuan et al. — Native Sparse Attention: Hardware-Aligned and Natively Trainable Sparse Attention (arXiv:2502.11089, ACL 2025 Best Paper)](https://arxiv.org/abs/2502.11089)- Kağıt
- [DeepSeek-V3 Technical Report (arXiv:2412.19437)](https://arxiv.org/abs/2412.19437) NSA'nın mimari ailesinin hedefleri
- [Moonshot AI — MoBA: Mixture of Block Attention for Long-Context LLMs (arXiv:2502.13189)](https://arxiv.org/abs/2502.13189) eş zamanlı çalışma, bloklar üzerinde MoE tarzı dikkat
- [Beltagy et al. — Longformer: The Long-Document Transformer (arXiv:2004.05150)](https://arxiv.org/abs/2004.05150) kaydırıcı pencerelerin kökeni
- [Xiao et al. — StreamingLLM: Efficient Streaming Language Models with Attention Sinks (arXiv:2309.17453)](https://arxiv.org/abs/2309.17453) İhtiyaçlı bir süreli kısıtlılık başlangıç çizgisi NSA'nın
- [Dao et al. — FlashAttention-2 (arXiv:2307.08691)](https://arxiv.org/abs/2307.08691) NSA çekirdekleri 64k'te çarpıyor .
