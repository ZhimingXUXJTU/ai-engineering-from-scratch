# Gradyent Kontrol Noktası ve Aktifleştirme Rekomülasyonu .

> Backprop, her geçici etkinleştirmeyi tutar. 70B parametreleri ve 128K bağlamında bu, her sıra başına 3 TB etkinleştirme demektir. Kontrol noktası hafıza için FLOPs işlemleri: kaydetmek yerine yeniden hesaplamak. Sorun hangisi bölgeleri düşürmek ve cevap "bütünü" değil.

> **【中文解读】**Bu nedenle, bu konuyla ilgili olarak, bu konuyla ilgili olarak, bu konuyla ilgili olarak, bu konuyla ilgili olarak, bu konuyla ilgili olarak, bu konuyla ilgili olarak, bu konuyla ilgili olarak, bu konuyla ilgili olarak, bu konuyla ilgili olarak, bu konuyla ilgili olarak, bu konuyla ilgili olarak, bu konuyla ilgili olarak, bu konuyla ilgili olarak, bu konuyla ilgili olarak, bu konuyla ilgili olarak, bu konuyla ilgili olarak, bu konuyla ilgili olarak, bu konuyla ilgili olarak, bu konuyla ilgili olarak, bu konuyla ilgili olarak, bu konuyla ilgili olarak, bu konuyla ilgili olarak, bu konuyla ilgili olarak, bu konuyla ilgili olarak, bu konuyla ilgili olarak, bu konuyla ilgili olarak, bu konuyla ilgili olarak, bu konuyla ilgili olarak, bu konuyla ilgili olarak, bu konuyla ilgili olarak, bu konuyla ilgili olarak, bu konuyla ilgili olarak, bu konuyla ilgili olarak, bu konuyla ilgili olarak, bu konuyla ilgili olarak, bu konuyla ilgili olarak, bu konuyla ilgili olarak, bu konuyla ilgili olarak, bu konuyla ilgili olarak, "bir konuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyuyu

> **【拓展：梯度检查点→大模型训练】**梯度检查点是训练大模型的标配技术──PyTorch'ın meşale.kullanımları. kontrol noktası、DeepSpeed'in etkinleştirme kontrol noktası bu düşüncenin gerçekleşmesidir──128K 上下文训练中, selektivity检查点 60%+'ın kaydedilmesi için tasarruf sağlar──

>  **【前置】**Önemli bir eğitim programı yaparak, eğitim programının başlatılması ve hazırlanması için gerekli teknikleri öğrenmek için, eğitim programının başlatılması için, eğitim programının başlatılması için, eğitim programının başlatılması için, eğitim programının başlatılması için, eğitim programının başlatılması için, eğitim programının başlatılması için, eğitim programının başlatılması için, eğitim programının başlatılması için, eğitim programının başlatılması için, eğitim programının başlatılması için, eğitim programının başlatılması için, eğitim programının başlatılması için, eğitim programının başlatılması için, eğitim programının başlatılması için, eğitim programının başlatılması için, eğitim programının başlatılması için, eğitim programının başlatılması için, eğitim programının başlatılması için, eğitim programının başlatılması için, eğitim programın başlatılması için, eğitim programın başlatılması için, eğitim programın başlatılması için, eğitim programın başlatılması için, eğitim programın başlatılması için, eğitim programın başlatılması için, eğitim programın başlatılması için, eğitim programın başlatılması için, eğitim ve eğitim programın başlatılması için, eğitim için, eğitim planın başlatılması için, eğitim ve eğitim için, eğitim için, eğitim için, eğitim ve eğitim için, eğitim için, eğitim için, eğitim için, eğitim için, eğitim için, eğitim için, eğitim için, eğitim için, eğitim için, başlatmak için, başlatmak için, başlatmak için, başlatmak için, başlatmak için, başlatmak için, başlatmak için, başlatmak için,
>  **【类比】**梯度检查点 = 出差只带必要文件──反向传播──工作完成后回顾所有材料;不检查点 = 出差路上所有材料都背着(占满行李箱);全检查点 = 只带护照,需要时再印(重算成本高);选择性检查点──只扔可重算的(草稿) 保留难重建的(合同) 平衡存储和速度显――

**Type:** Build
**Languages:** Python (with numpy, optional torch)
**Prerequisites:** Phase 10 Lesson 04 (Pre-Training Mini-GPT), Phase 10 Lesson 05 (Scaling & Distributed)
**Time:** ~70 minutes

## Sorunlar. Sorunlar.

Bir transformatör eğitimi, her katman için geriye ayrılmış her operasyonun girişlerini saklar: dikkat girişleri, Q/K/V projeksiyonları, softmax çıkışı, FFN girişleri, norm çıkışları ve kalan akım. Gizli boyutlu bir katman için `d`, dizi uzunluğu `L`, parti`B`Bu , emir üzerine .`12 * B * L * d`katman başına yüzen.

>                                                                                                                                                                                                                                                               `d`、序列长度 `L`、Bölüm`B`Bu her katın bir kısmı.`12 * B * L * d`- Evet.

- Evet .`d=8192, L=8192, B=1`Bu, BF16'da katman başına 800 MB'dir. 64 katlı bir model 51 GB aktivasyonlara sahiptir.`L^2`(bkz: baş başına) ve tensor paralel kısmi kopyaları oluşturmadan önce.

> - Evet .`d=8192, L=8192, B=1`BF16 Aşağı kat 800 MB¬64 kat modelinin aktivasyon değeri 51 GB bu da küçük bitki büyüklüğü, daha fazla dikkat çekilmez softmax orta değer( başına`L^2`), aynı zamanda 张量并行的部分副本に

İki taraflı fatur: BF16 ağırlıkları artı optimizer durumu 80GB'ye uygun olabilir, ancak etkinleştirmeler sizi öteye itebilir. Gradient kontrol noktası (aka activation recalculation) standart düzeltme. Çoğu etkinleştirmeyi bırakın; geriye dönerken ileriyi tekrar yapın.

> 双面账单:BF16 权重加优化器状态可能放入80GB,但激活值让你超出──梯度检查点(又称激活重计算) 标准修复方案──丢弃大部分激活值;反向传播期间重复前向传播以恢复它们──代价:额外FLOPs──收益:显存按检查段段数与总层数的比例下降──

Naifce yapıldığında, kontrol noktası, adım başına yaklaşık %33 daha fazla ileri geçiş FLOP maliyetindedir. İyi yapıldı  Korthikanti et al.'ın "akıllı seçimi" başına seçici kontrol noktası  5x hafıza tasarruf edersiniz.

## Konsepten bir şey.

> **【中文解读】**梯度检查点(Gradient Checkpointing) hesaplama değişimi: önde yayılma zamanında orta aktiv değer saklanmaz, karşıda yayılma zamanında yeniden hesaplama gereksiniminin aktivasyonu── bu, ek hesaplama açıklama fiyatına yaklaşık %30'a düşecek, aktiv değerin açıklama kullanımını yaklaşık %70'e düşürecek──

> **【拓展：梯度检查点在训练中的关键作用】**梯度检查点是训练大模型的标志技术──Llama 3 70B için, hiçbir kontrol noktası yoktur, her örnek yaklaşık 16GB 激活值显存, açıldıktan sonra yaklaşık 5GB 降低──FSDP ve混合精度 ile birlikte, 梯度检查点 sınırlı GPU 显存内训练大模型成为可能──


### Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geriye Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri Geri

`output = layer(input)`Geriye dönmek istiyor .`grad_input`ve `grad_params`Onları hesaplamak için:

- `input`(Bilgilemek için `grad_params = input.T @ grad_output`Düzsel katmanlar için)
- bazı aktive derivatifler arası (ReLU/GELU/softmax'ın derivatifleri aktive değerine bağlıdır)

Ön geçit otomatik olarak otograd grafikinde depolanır.`tensor.retain_grad()`ve girişine ihtiyacı olan her operasyon bir referans tutar.

### Tam Kontrol Noktası Saçma

Ağı ikiye böl .`N`Önceki bölümler. Önceki bölümler sırasında, her bölüm için sadece * giriş * depolayın. Geriye geçişler gerektiğinde, segmentin önceki geçişini yeniden çalıştırın, sonra farklılaştırın.

Örnek: 32 katmanlı transformatör, her katman 1 katmanlı 32 bölüme ayrılmıştır.

- Hatıra: 32 katman giriş (küçük) vs 32 * (katman başına etkinleştirme hacmi) (çok büyük).
- Ekstra hesaplama: Segmente başına 1 ekstra ileri, yani %33 daha fazla ileri FLOP toplamı (geriye doğru 2x ileri olduğu için, tam adım 1 + 1 + 2 = 4 birim yerine 1 + 2 = 3 olur).

Bu Chen et al. 2016 tarihli orijinal tarifi: her bir kontrol noktası `sqrt(L)`L=64, 8 kontrol noktası.

### Seçimsel Kontrol Noktası (Korthikanti 2022)

Tüm etkinleştirmeler aynı maliyetli değil.`B*L*L*heads`FFN gizli etkinliği `B*L*4d`Uzun sekanslarda softmax hakimdir.

Seçimsel kontrol noktası, ucuz depolama aktivasyonlarını (lineer projeksiyonlar, kalıntılar) tutar ve sadece pahalı olanları (özen) yeniden hesaplar.

Megatron-Core bunu "seçici" etkinleştirme yeniden hesaplama olarak uyguluyor.

### Çıkarım

Yeniden hesaplama alternatifleri: ileri ve geriye doğru CPU RAM'a devreye aktarma. PCIe bant genişliği gerektirir; boş bant genişliği yeniden maddeleşme maliyetinden fazla olduğunda yararlıdır. Karışık stratejiler yaygın: bazı katmanları kontrol et, diğerlerini boşalt.

FSDP2 birinci sınıf bir seçenek olarak yükten çıkartır. GPU hafıza boğazında bulunduklarında yükten çıkartır.

### Ücret Modelini Yeniden Hesapla

Her adımda saf bir kontrol noktası ile FLOPs .`k`katmanları `L`- ...

```
flops_fwd_normal = L * f_layer
flops_bwd_normal = 2 * L * f_layer
flops_total_normal = 3 * L * f_layer

flops_fwd_ckpt = L * f_layer
flops_recompute = L * f_layer  # one extra forward per layer in the segment
flops_bwd_ckpt = 2 * L * f_layer
flops_total_ckpt = 4 * L * f_layer
overhead = 4 / 3 - 1 = 0.33 = 33%
```

Seçimsel kontrol noktası ile sadece dikkat çekirdeğini yeniden hesaplarsınız, tüm katmanı değil:

```
flops_recompute_selective = L * f_attention ~= L * f_layer * 0.15
overhead_selective = (3 + 0.15) / 3 - 1 = 0.05 = 5%
```

### Hatıra Kaydetme Modülü

Katman başına etkinleştirme hacmi: `A`- Evet .`L`katmanlar, toplam aktivasyon hafızası: `L * A`- Evet .

Tam kontrol noktası (sektör boyutu 1): sadece depolama `L * input_volume`(~`L * 1/10 A`Standart bir transformatör için).`9 * L * A * 1/10`- Evet .

Kontrol noktası her zaman .`k`katmanlar: depolama `L/k * A`Ek olarak .`k-1`aktif segment içindeki katmanların değeri.

- Evet .`k = sqrt(L)`, bellek ve yeniden hesaplama maliyeti hem ölçekle `sqrt(L)` En iyi fiyat değişikliği.

### Kontrol Noktasına Ne Zaman Gitmemek

- Bir boru hattının en iç katmanları uçuşta zaten.
- Eğlence hesabına hükmeden ilk ve son katmanlar (transformatörlerde nadirdir).
- FlashAttention'ı kullanan dikkat çekirdekleri  Flash zaten softmax hızını yeniden hesaplar, bu yüzden ek katman seviyesindeki kontrol işaretlemeyi üstte biraz ekler.

### Uygulama Şekilleri

1. **Function wrapper:**Bir bölümü içine sarın `torch.utils.checkpoint.checkpoint(fn, input)`Sadece PyTorch mağazaları .`input`, geriye dönüp her şeyi yeniden hesaplar.

2. **Decorator-based:**Etiketlemenin kontrol noktası olarak yapılması gereken katmanlar; eğitmen, hangi bölümlerin toplanıp sarılacağına konfigürasyon zamanında karar verir.

3. **Manual explicit recompute:**Sıradan bir alışkanlık olarak geriye geçmeyi kendin yaz.`recompute_forward`Öncekiyi depolanan giriş ile çiftleştirir.

Üçü de aynı fonksiyonel sonuç verir.

### TP / PP / FP8 ile etkileşim

- **Tensor parallel:**Kontrol noktası girişleri yeniden hesaplama sırasında toplanmalı veya yeniden dağıtılmalıdır; iletişim maliyetini karşılamak.
- **Pipeline parallel:**Tipik bir örnektir. Her boru hattının aşamasının ileriye doğru kontrol edilmesi böylece geri sıra mikrobatçlar aktifleşme belleğini yeniden kullanabilmektedir.
- **FP8 recompute:**amax tarihleri yeniden hesaplama sırasında güncellenmiş orijinal ileri veya FP8 ölçek sürüşleri ile eşleşmelidir.


> **【拓展：梯度检查点与 FSDP 的配合】**梯度 kontrol noktası genellikle FSDP/ZeRO ile birlikte kullanılır. 梯度 kontrol noktası, aktif değerlerin azalması, ikili birbiriyle tamamlanır. 70B seviyesindeki modeller için, FSDP + 梯度 kontrol noktası + 混合精度 8xA100'de üst eğitim mümkün hale getirir.


## Yapın.
```figure
activation-recompute
```

## Yapın

### Adım 1: Bölümlerle Oyuncak Model

```python
import numpy as np


def linear_forward(x, w, b):
    return x @ w + b


def relu(x):
    return np.maximum(x, 0)


def layer_forward(x, w1, b1, w2, b2):
    h = relu(linear_forward(x, w1, b1))
    return linear_forward(h, w2, b2)


def model_forward(x, params):
    activations = [x]
    h = x
    for w1, b1, w2, b2 in params:
        h = layer_forward(h, w1, b1, w2, b2)
        activations.append(h)
    return h, activations
```

### İkinci Adım: Geriye Alışmak İçin Tüm Aktivasyonlara İhtiyaç Var

```python
def model_backward(grad_output, activations, params):
    grads = [None] * len(params)
    g = grad_output
    for i in range(len(params) - 1, -1, -1):
        w1, b1, w2, b2 = params[i]
        x_in = activations[i]
        h_pre = linear_forward(x_in, w1, b1)
        h = relu(h_pre)
        gh = g @ w2.T
        gw2 = h.T @ g
        gb2 = g.sum(axis=0)
        g_pre = gh * (h_pre > 0)
        gx = g_pre @ w1.T
        gw1 = x_in.T @ g_pre
        gb1 = g_pre.sum(axis=0)
        grads[i] = (gw1, gb1, gw2, gb2)
        g = gx
    return g, grads
```

### Adım 3: Kontrol Noktası-Her-k hafıza

```python
def model_forward_checkpointed(x, params, k=4):
    saved_inputs = [x]
    h = x
    for i, (w1, b1, w2, b2) in enumerate(params):
        h = layer_forward(h, w1, b1, w2, b2)
        if (i + 1) % k == 0:
            saved_inputs.append(h)
    return h, saved_inputs


def model_backward_checkpointed(grad_output, saved_inputs, params, k=4):
    grads = [None] * len(params)
    g = grad_output
    segments = [(j * k, min((j + 1) * k, len(params))) for j in range(len(saved_inputs))]
    for seg_idx in range(len(saved_inputs) - 1, -1, -1):
        start, end = segments[seg_idx]
        if start >= end:
            continue
        x_in = saved_inputs[seg_idx]
        _, seg_acts = model_forward(x_in, params[start:end])
        g, seg_grads = model_backward(g, seg_acts, params[start:end])
        for j, gr in enumerate(seg_grads):
            grads[start + j] = gr
    return g, grads
```

### Dördüncü Adım: Maliyet modeli

```python
def checkpoint_cost(n_layers, segment_size, flops_per_layer=1.0):
    fwd = n_layers * flops_per_layer
    recompute = n_layers * flops_per_layer
    bwd = 2 * n_layers * flops_per_layer
    return {
        "fwd": fwd,
        "recompute": recompute,
        "bwd": bwd,
        "total": fwd + recompute + bwd,
        "overhead_vs_no_ckpt": (fwd + recompute + bwd) / (fwd + bwd) - 1.0,
    }


def selective_checkpoint_cost(n_layers, attention_fraction=0.15,
                              flops_per_layer=1.0):
    fwd = n_layers * flops_per_layer
    recompute = n_layers * attention_fraction * flops_per_layer
    bwd = 2 * n_layers * flops_per_layer
    return {
        "fwd": fwd,
        "recompute": recompute,
        "bwd": bwd,
        "total": fwd + recompute + bwd,
        "overhead_vs_no_ckpt": (fwd + recompute + bwd) / (fwd + bwd) - 1.0,
    }
```

### Adım 5: Hatıra Tahminici

```python
def activation_memory_mb(n_layers, hidden=8192, seq=8192,
                        batch=1, bytes_per_value=2):
    per_layer = 12 * batch * seq * hidden * bytes_per_value
    return n_layers * per_layer / 1e6


def memory_after_checkpoint(n_layers, segment_size, hidden=8192,
                           seq=8192, batch=1, bytes_per_value=2):
    n_seg = max(1, n_layers // segment_size)
    saved = (n_seg + segment_size) * 1 * batch * seq * hidden * bytes_per_value
    return saved / 1e6
```

### Adım 6: Optimal Bölüm Boyutu

```python
def optimal_segment(n_layers):
    return int(round(np.sqrt(n_layers)))
```

### Adım 7: Seçimçi Kontrol Noktası Kararı

```python
def should_recompute(layer_type, activation_bytes, recompute_flops_ratio):
    if layer_type == "attention" and activation_bytes > 100 * 1e6:
        return True
    if layer_type == "ffn" and activation_bytes > 500 * 1e6:
        return recompute_flops_ratio < 0.1
    return False
```

## Çerçeveyi kullanın.

- **torch.utils.checkpoint**- Evet .`from torch.utils.checkpoint import checkpoint`PyTorch'daki kanonik ambalaj. Bir fonksiyonu sarar; sadece girişleri saklar, geriye doğru yeniden hesaplar.
- **Megatron-Core activation recomputation**: destekler `selective`- Evet .`full`ve`block`2024+ sınır eğitiminde standart.
- **FSDP2 offload**- Evet .`module.to_empty(device="cpu")`- Evet .`offload_policy`FSDP2'de yeniden hesaplama yerine CPU'ya etkinleştirmelerini kısaltır.
- **DeepSpeed ZeRO-Offload**: Optimizer durumları ve etkinleştirmeleri için CPU yükü çıkartmak, kontrol noktasını tamamlamak.

## İndirin . Ürünler .

Bu ders bize çok yararlı .`outputs/prompt-activation-recompute-policy.md` model yapılandırmasını (katmanlar, gizli, seq, parti) ve mevcut GPU belleğini alan ve katman başına yeniden hesaplama politikasını (hiçbir / seçici / tam / yüklenme) yayınlayan bir istek.

> 本课产 出 `outputs/prompt-activation-recompute-policy.md` bir kabul model konfigürasyonu (Level Numbers, Hidden Dimensions, Process Length, Batch) ve kullanılabilir GPU'lar içinde depolama ve çıkış için her aşamalı yeniden hesaplama stratejisi (No / Selectionary / 完全 / 卸载) 

## Egzersizler.

1. Doğru olduğunu kontrol et.`model_forward`+ `model_backward`(tam aktivasyon) vs `model_forward_checkpointed`+ `model_backward_checkpointed`Parametre gradiyenti makinenin hassasiyetine eşit olmalıdır.
   Çinçe Çevirimi:验证正确性──运行 `model_forward`+ `model_backward`(完整激活)  ile`model_forward_checkpointed`+ `model_backward_checkpointed`(分段) ◊ Parametral ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊ ̊   ̊ ̊                                                                                                                                                                                                                                         

2. Tarama bölümü boyutu `k`1 ' den `L`- FLOP'u ve hafızayı çiz.
   Çeviri: 将段大小`k`1 扫到`L`◊ FLOP çizmek 开销和内存──找到曲线的拐点──

3. Seçimsel kontrol işaretlemeyi uygulayın: dikkat modülünün girişini, ancak aralarını değil saklayın. 32 katlı bir model için FLOP üst üstlük vs tam katman kontrol işaretlemesini seq=8192'de ölçün.
   Çinçe Çevirimi: implement selektive checkpoint: depolama dikkatlilik modülü giriş ama yok orta sonuçları。 ölçüm 32 kat model seq=8192 下 seq=8192 下 seq=8192 下 seq=8192 下 seq=8192 下 seq=8192 下 seq=8192 下 seq=8192 下 seq=8192 下 seq=8192 下 seq=8192 下 seq=8192 下 seq=8192 下 seq=8192 下 seq=8192 下 seq=8192 下 seq=819

4. Çıkarma ekleyin. Segment girişlerini simülasyonlu bir "CPU tamponu"na (ayrı bir liste) kaydetin. "PCIe bant genişliği" byte/zaman olarak ölçün ve çıkarma ve yeniden hesaplama arasındaki kesinti noktasını bulun.
   Çinçe Çevirim: 添加卸载. 将段输入保存到模拟的"CPU缓冲区" (CPU 缓冲区) 单独的列表)  设节/时间测量 (PCIe 带宽) 并找到卸载与重计算之间的平衡点.

5. Gerçek PyTorch transformatörünü , içinde ve dışında bir referans göster .`torch.utils.checkpoint`. hafıza ölçümleri (den`torch.cuda.max_memory_allocated`) ve adım zaman.
   Çin Çeviri:对真实 PyTorch transformer 分别使用和不使用 `torch.utils.checkpoint`基准测试──测量内存(通过 `torch.cuda.max_memory_allocated`) ve步长时间。

## Anahtar Şartlar .

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|----------------------|---------|
| Gradient checkpointing | "Save memory by redoing forward" | Store segment inputs only; recompute intermediates during backward to get gradient-support tensors | 梯度检查点，仅保存段输入，反向时重算中间值 |
| Activation recomputation | "Same as checkpointing" | The HPC-flavored name for the same technique | 激活重计算，梯度检查点的 HPC 叫法 |
| Segment size (k) | "How many layers per checkpoint" | Number of layers whose intermediates are dropped and rematerialized together | 段大小，每个检查点包含的层数 |
| Selective checkpointing | "Korthikanti's trick" | Recompute only expensive-to-store activations (attention softmax); keep cheap ones | 选择性检查点，只重算存储昂贵的激活 |
| Full checkpointing | "The naive version" | Recompute every layer's intermediates in every segment | 全量检查点，朴素版本重算所有中间值 |
| Block checkpointing | "Coarse-grained" | Checkpoint whole transformer blocks; largest granularity | 块级检查点，以 Transformer 块为粒度 |
| FLOP overhead | "The compute tax" | Extra FLOPs per step = (recompute FLOPs) / (fwd + bwd FLOPs); 33% naive, 5% selective | FLOP 开销，朴素版 33%，选择性版 5% |
| Activation offload | "Ship to CPU" | Move activations to CPU RAM across forward->backward; alternative to recompute | 激活卸载，将激活移到 CPU 内存 |
| sqrt-L rule | "The classical optimum" | For uniform-cost layers, optimal checkpoint spacing is sqrt(L) layers | sqrt-L 规则，均匀层代价的最优检查点间隔 |
| Attention-softmax volume | "The O(L^2) problem" | L^2 * heads * batch floats; dominates activation memory at long contexts | 注意力 softmax 体积，O(L^2) 的显存问题 |

## Daha fazla okumak

- [Chen et al., 2016 -- "Training Deep Nets with Sublinear Memory Cost"](https://arxiv.org/abs/1604.06174)- ...diğerleri kontrol etmek için resmileştirilen orijinal kağıt.
- [Korthikanti et al., 2022 -- "Reducing Activation Recomputation in Large Transformer Models"](https://arxiv.org/abs/2205.05198)-- Seçkin etkinleştirme yeniden hesaplama ve resmi maliyet analizi
- [Pudipeddi et al., 2020 -- "Training Large Neural Networks with Constant Memory using a New Execution Algorithm"](https://arxiv.org/abs/2002.05645)-- ters modunda yeniden maddeleşme yoluyla alternatif sabit hafıza yaklaşımı
- [Ren et al., 2021 -- "ZeRO-Offload: Democratizing Billion-Scale Model Training"](https://arxiv.org/abs/2101.06840)-- Ölçüsünde aktifleştirme yükü
- [PyTorch torch.utils.checkpoint docs](https://pytorch.org/docs/stable/checkpoint.html)-- Standart API
- [Megatron-Core activation recomputation documentation](https://docs.nvidia.com/nemo-framework/user-guide/latest/nemotoolkit/features/memory_optimizations.html)-- Seçkin, tam ve blok modları
