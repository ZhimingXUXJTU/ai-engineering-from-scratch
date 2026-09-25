# Görme Transformerleri (ViT)

> Bir resim bir yama şebekesi, bir cümle bir simge şebekesi, aynı transformatör her ikisini de yiyor.

> **【中文解读】**ViT Yapıştırma, resim kesme, işleme, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem ve işlem, işlem, işlem, işlem, işlem, işlem, işlem ve işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem ve işlem, işlem, işlem, işlem, işlem, işlem, işlem ve işlem, işlem, işlem, işlem, işlem, işlem ve işlem, işlem, işlem, işlem, işlem, işlem, işlem ve işlem, işlem, işlem, işlem ve işlem, işlem, işlem, işlem, işlem, işlem, işlem ve işlem, işlem, işlem, işlem, işlem, işlem, işlem ve işlem, işlem, işlem, işlem ve işlem, işlem, işlem, işlem, işlem, işlem ve işlem, işlem, işlem, işlem, işlem, işlem ve işlem, işlem, işlem, işlem, işlem ve işlem, işlem, işlem, işlem, işlem, işlem, işlem ve işlem, işlem, işlem, işlem, işlem, işlem, işlem ve işlem, işlem, işlem, işlem, işlem, işlem, işlem, işlem ve işlem, işlem, işlem, işlem, işlem, işlem, işlem ve işlem, işlem, işlem, işlem, işlem, işlem ve işlem, işlem, işlem.

**Type:** Hands-on | **类型:** 动手
**Language:**Python .**语言:**Python
**Prerequisites:** Phase 7 · 05 (Full Transformer), Phase 4 · 03 (CNNs), Phase 4 · 14 (Vision Transformers intro) | **前置知识:** Phase 7 · 05 (Full Transformer), Phase 4 · 03 (CNNs), Phase 4 · 14 (Vision Transformers intro)
**Time:** ~45 minutes | **时间:** ~45 分钟

## Sorunlar. Sorunlar.

2020'den önce bilgisayar görme dönüşümleri anlamına geliyordu. ImageNet'teki her SOTA, COCO ve tespit referansları CNN'in omurgasını kullanıyordu. Transformerler dil içinydi.

> 2020 yılına kadar, bilgisayar görme, bir dizi oluşturmak anlamına geliyordu. ImageNet、COCO 和检测基准 üzerindeki her SOTA CNN 骨干网络──Transformer is used for language processing──

Dosovitskiy et al. (2020)  "Bir Resim 16x16 Kelimaya Değer"  gösterdi ki, dönüşümleri tamamen bırakabilirsiniz. Bir resimi sabit boyutlu yamalara kesin, her yamayı bir gömleğe lineer olarak projekte edin, dizini bir vanilya transformatör kodleyicisine besleyin. Yeterli ölçekte (ImageNet-21k öncesi eğitim veya daha büyük), ViT ResNet tabanlı modellerle eşleşiyor veya yener.

> Dosovitskiy 等人(2020) "一张图像值 16x16 个词"证明可以完全放弃卷积──将图像切成固定大小的补丁,线性投影每补丁为嵌入,将序列送入标准变压器编码器──在足够大的下规模(ImageNet-21k 预训或更大),ViT 可以匹配或超越基于ResNet 的模型──

ViT 2026'da daha geniş bir modelin başlangıcıydı: tek bir mimarlık, birçok modaliteler. Sıfırlatmak ses simgelendirir. ViT görüntü simgelendirir. Robotik için eylem simgeleri. Video için piksel simgeleri. Transformatör umurunda değil  ona bir dizi besler ve öğrenir.

> ViT 2026 yılının daha geniş bir eğiliminin başlangıcıdır: bir yapı, çok çeşitli biçimlerdir.

2026 yılına kadar, ViT ve soyundan gelenleri (DeiT, Swin, DINOv2, ViT-22B, SAM 3) görselliğin büyük kısmına sahip. CNN'ler hala kenar cihazlar ve gecikme hassas görevlerde kazanır.

> 2026 yılına kadar, Vietnamlılar ve onların sonraki halefi (DeiT, Swin, DINOv2, Vietnamlılar ve Vietnamlılar) görsel alanda büyük bir payı ele geçirdi.

> **【中文解读】**ViT'in temel anlayışı: Resimler metin gibi "token" dizisi olarak kesilebilir. 224x224 resim 14x14 个 16x16 çubuk olarak kesilecek. Her çubuk 展平后线性投影为嵌入向量,然后送入标准变压器编码器. Bu, Transformer'ın genel kullanımının NLP ile sınırlı olmadığını kanıtlıyor.

## Konsepten bir şey.

![Image → patches → tokens → transformer](../assets/vit.svg)

### Adım 1  Yapıştır

A bölün .`H × W × C`bir görüntüye dönüştürülür.`N × (P·P·C)`Düzlemli yamalar sırası.`224 × 224`görüntü, `16 × 16`patches → 196 patches, her biri 768 değer.

> - Ben de .`H × W × C`图像分为 `N × (P·P·C)`序列──典型设置:`224 × 224`Resimler,`16 × 16`Patch → 196 个 768 值的补丁──

```
image (224, 224, 3) → 14 × 14 grid of 16x16x3 patches → 196 vectors of length 768
```

Patch boyutu kaldıraçtır. Küçük patches = daha fazla token, daha iyi çözünürlük, kare dikkat maliyeti. Büyük patches = daha kaba, daha ucuz.

> Patch büyüklükte kontrol parametrelidir. Daha küçük patch = daha fazla token, daha iyi çözünürlük, ikinci dikkat maliyeti. Daha büyük patch = daha kaba, daha ucuz.

### Adım 2  Düzsel yerleştirme

Tek öğrenilen bir matris , her düz yamacı `d_model`. Yükleme büyüklüğü bir kıvrımla eşdeğer `P`ve adım at `P`PyTorch ' da bu kelimenin tam anlamıyla`nn.Conv2d(C, d_model, kernel_size=P, stride=P)` 2 satırlı bir uygulama.

> Bir öğrenmek için matron her 平 yama 投影 `d_model`◊ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ `P`、步长为 `P`Çekilmecikler içinde.`nn.Conv2d(C, d_model, kernel_size=P, stride=P)`两行实现──

> **【拓展：Swin Transformer 的层级设计】**標準 ViT 固定 patch 大小和全局注意力,计算量 O(N^2)。Swin Transformer  引入层级结构:在小 patch 上做局部窗口注意力,逐层合并 patch 扩大感受野。 bu da hesaplama karmaşıklığını O(N'e dönüştürürken, aynı zamanda seviye özelliklerini çıkarma yeteneğini korur。Swin, kontrol ve bölme görevlerinde standart ViTden daha iyidir。

### Adım 3  hazırlık `[CLS]`Token, pozisyonsal yerleşim ekle

- Öğrenilenecek bir şey hazırla .`[CLS]`Son gizli durum, sınıflandırma için kullanılan görüntü temsilidir.
  Çin Çeviri:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        `[CLS]`token── son gizli durumunu görüntü gösterimleri için kullanılır──
- Öğrenilebilir pozisyonsal yerleşimler (ViT-orjinal) veya sinusoidal 2D (sonraki çeşitler) eklenir.
  Çinçe Çevirimi: Add Add Add可学习的位置嵌入 (ViT) veya正弦 2D 嵌入 (后续变体)
- 2024+ RoPE pozisyon için 2D'ye genişletildi, bazen açıkça yerleştirilmeden.
  Çinçe Çevirimi::2024 yıl sonra, RoPE  genişletildi 2D  konum kodlaması, bazen açık bir yerleşim gerektirmez.

### Adım 4  Standart transformer kodlayıcı

L blokları yığılsın`LayerNorm → Self-Attention → + → LayerNorm → MLP → +`- BERT'ye benzer. Görüş özel katman yok. Bu makaleyin pedagojik çizgisi.

> Bir sürü şey .`LayerNorm → Self-Attention → + → LayerNorm → MLP → +`Bu makaleyi okuduktan sonra, bu makaleyi okuduktan sonra, bu makaleyi okuduktan sonra, bu makaleyi okuduktan sonra, bu makaleyi okuduktan sonra, bu makaleyi okuduktan sonra, bu makaleyi okuduktan sonra, bu makaleyi okuduktan sonra, bu makaleyi okuduktan sonra, bu makaleyi okuduktan sonra, bu makaleyi okuduktan sonra, bu makaleyi okuduktan sonra, bu makaleyi okuduktan sonra, bu makaleyi okuduktan sonra, bu makaleyi okuduktan sonra, bu makaleyiyi okuduktan sonra, bu makaleyiye devam etti.

### Adım 5  baş

Sınıflandırma için: alın `[CLS]`Gizli durum → doğrusal → yumuşak maksimum.`[CLS]`, patch yerleştirmelerini doğrudan kullanın.

>  分类:取 `[CLS]`隐藏状态 → 线性层 → softmax── DINOv2 veya SAM için, terk edilmiş `[CLS]`, doğrudan kullanım patch 嵌入──

### Önemli olan çeşitler

| Model | Year | Change |
|-------|------|--------|
| 模型 | 年份 | 变化 |
| ViT | 2020 | The original. Fixed patch size, full global attention. |
| ViT | 2020 | 原始版本。固定 patch 大小，全局注意力。 |
| DeiT | 2021 | Distillation; trainable on ImageNet-1k only. |
| DeiT | 2021 | 蒸馏；仅在 ImageNet-1k 上可训练。 |
| Swin | 2021 | Hierarchical with shifted windows. Fixed sub-quadratic cost. |
| Swin | 2021 | 层级结构，移位窗口。固定的亚二次成本。 |
| DINOv2 | 2023 | Self-supervised (no labels). Best general vision features. |
| DINOv2 | 2023 | 自监督（无标签）。最佳通用视觉特征。 |
| ViT-22B | 2023 | 22B params; scaling laws apply. |
| ViT-22B | 2023 | 22B 参数；缩放定律适用。 |
| SigLIP | 2023 | ViT + language pair, sigmoid contrastive loss. |
| SigLIP | 2023 | ViT + 语言配对，sigmoid 对比损失。 |
| SAM 3 | 2025 | Segment anything; ViT-Large + promptable mask decoder. |
| SAM 3 | 2025 | 分割一切；ViT-Large + 可提示的掩码解码器。 |

### Neden biraz zaman aldı?

ViT, CNN'e eşleşmek için *çok sayıda* veriye ihtiyaç duyar çünkü CNN'in induktif önyargıları (çevirim değişikliği, yerleşim) yoktur. > 100M etiketli görüntü veya güçlü kendiliğinden denetimli önceden eğitim olmadan, CNN'ler hala eşleşen hesaplamalarda kazanır. DeiT bunu 2021'de destilasyon hileleriyle düzeltti; DINOv2 bunu 2023'te kendiliğinden denetimle kalıcı olarak düzeltti.

> ViT, CNN'in performansına uymak için büyük miktarda veri gerektirir, çünkü CNN'in özelliği yoktur.

> **【中文解读】**ViT'nin zayıf özelleştirme tercihleri iki kılıçlı bir kılıçtır: CNN'in performansına uymak için daha fazla veri gerekmektedir, çünkü CNN'in doğal olarak sabit ve yerel özelleştirme tercihleri vardır. Ancak veri miktarı yeterince büyük olduğunda, ViT'in genişleme kapasitesi CNN'den çok daha fazladır.

> **【拓展：ViT 在多模态系统中的角色】**CLIP kullanarak ViT 编码图像、Transformer 编码文本,通过对比学习对齐两个模态──DALL-E 和 Sora kullanarak ViT 理解图像/视频,再生成新内容──SAM(Segment Anything) kullanarak ViT 作为主干网络实现通用图像分割──ViT 已成为多模态 AI's视觉基础模块──

## Yapın.
```figure
n5-patch-stream
```

## Yapın

Bakın .`code/main.py`- Pure-stdlib patchify + linear yerleştirme + akıl sağlığı kontrolü.

> 参见 `code/main.py`◊ Pure Standard Library patchify + 线性嵌入 + 合理性检查──无训 任何实际规模的 ViT 都需要 PyTorch 和数小时的GPU 时间──

### Adım 1: Sahte görüntü

24 × 24 RGB görüntü , `(R, G, B)`6×6 patches → 16 patches, her biri 108D gömleyici vektör kullanıyoruz.

> Bir 24 × 24 RGB görüntü,`(R, G, B)`元组的行列表形式表示──使用 6×6 patch → 16 个 patch,每个108 维嵌入向量──

### Adım 2: Yapıştır

```python
def patchify(image, P):
    H = len(image)
    W = len(image[0])
    patches = []
    for i in range(0, H, P):
        for j in range(0, W, P):
            patch = []
            for di in range(P):
                for dj in range(P):
                    patch.extend(image[i + di][j + dj])
            patches.append(patch)
    return patches
```

Raster sıralaması: ağ üzerinde büyük satır.

> 光顺序:网格上按行优先遍历──每个 ViT 都使用这种排序──

### Adım 3: Düzsel yerleştirme

Her düz parçanı rastgele çarpın .`(patch_flat_size, d_model)`Çıktı biçiminin doğru olduğunu kontrol edin.`(N_patches + 1, d_model)`Önceden `[CLS]`- Evet .

> Her düzlemeyi bir anda bir kez daha yapalım.`(patch_flat_size, d_model)`矩阵──验证在添加 `[CLS]`后输出形为 `(N_patches + 1, d_model)`- Evet.

### Adım 4: Gerçekçi bir ViT için sayım parametreleri

ViT-Base için parametre sayısını basın: 12 katman, 12 baş, d = 768, yama = 16. ResNet-50 (~ 25M) ile karşılaştırın. ViT-Base ~ 86M'ye ulaşır. ViT-Large ~ 307M. ViT-Huge ~ 632M.

> 打印 ViT-Base 参数:12 层、12 头、d=768、patch=16──与ResNet-50(約25M)对比──ViT-Base 约86M──ViT-Large 约307M──ViT-Huge 约632M──

## Çerçeveyi kullanın.

```python
from transformers import ViTImageProcessor, ViTModel
import torch
from PIL import Image

processor = ViTImageProcessor.from_pretrained("google/vit-base-patch16-224-in21k")
model = ViTModel.from_pretrained("google/vit-base-patch16-224-in21k")

img = Image.open("cat.jpg")
inputs = processor(img, return_tensors="pt")
out = model(**inputs).last_hidden_state   # (1, 197, 768): [CLS] + 196 patches
cls_emb = out[:, 0]                       # image representation
```

**DINOv2 embeddings are the 2026 default for image features.**Meta'nın DINOv2 kontrol noktaları, metin dışı görme görevleri için CLIP'den daha iyi performans gösteriyor.

> **DINOv2 嵌入是 2026 年图像特征的默认选择。**结骨干网络,训练一个小头──适用于分类,检查,检测,图像描述──Meta'nın DINOv2 检查点在每个非文本视觉任务上都优于CLIP──

**Patch-size picking.**Küçük modeller 16×16 (ViT-B/16) kullanır. Sıklık öngörü (segmentasyon) 8×8 veya 14×14 (SAM, DINOv2) kullanır. Çok büyük modeller 14×14 kullanır.

> **Patch 大小选择。**小模型使用 16×16(ViT-B/16)。密集预测(分割) 8×8 veya 14×14(SAM、DINOv2)。 çok büyük modelleri 14×14。

## İndirin . Ürünler .

Bakın .`outputs/skill-vit-configurator.md`. Bilgi kümesi boyutu, çözünürlük ve hesaplama bütçesi göz önüne alındığında, yeni bir görme görevi için ViT varianti ve patch boyutu seçilir.

> 参见 `outputs/skill-vit-configurator.md`◊ Bu beceri DATABET'in büyüklüğüne göre Razon ve hesaplama bütçesine göre, yeni görüntü görevleri için ViT 变体和补丁を選択 大小──

## Egzersizler.

1. **Easy.**Çık .`code/main.py`- Patch sayısını kontrol edin .`(H/P) * (W/P)`ve düz yama boyutu eşit `P*P*C`- Evet .
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`code/main.py`△ Test patch 数量等于 `(H/P) * (W/P)`,平 yama 维度等于 `P*P*C`- Evet.
2. **Medium.**2D sinusoidal pozisyon yerleşimleri uygulayın  iki bağımsız sinusoidal kod için `row`ve `col`Her yama, zincirlenmiş. Onları küçük bir PyTorch ViT'ye besleyin ve CIFAR-10'da doğrulık ile öğrenilebilir konum yerleşimlerini karşılaştırın.
   Çin Çeviri: 2D 正弦位置嵌入每个补丁的实现`row`和 `col`独立编码后拼接──在小型 PyTorch ViT 上使用,与可学习位置嵌入在CIFAR-10 上对比准确率──
3. **Hard.**3 katmanlı bir ViT (PyTorch) oluşturun, 4×4 yamalarla 1000 MNIST görüntüde çalıştırın. Test doğruluğunu ölçün. Şimdi aynı 1.000 görüntüde DINOv2 önceden çalıştırmayı ekleyin (sederleştirilmiş: sadece kodlayıcıyı maskeli yamalardan yama yerleştirmelerini tahmin etmek için çalıştırın).
   Çin dili: yapılandırma 3 katlı ViT(PyTorch), 4×4 patçla 1.000 张 MNIST 图像上训练。测量测试准确率。然后添加 DINOv2 预训练(简化版:训练编码器从掩码 patch 预测 patch 嵌入)。准确率是否提升?

## Anahtar Şartlar .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Patch | "The vision-transformer token" | Flat vector of pixel values for a `P × P × C` region of the image. |
| Patch | "视觉 Transformer 的 token" | 图像中 `P × P × C` 区域的像素值扁平向量。 |
| Patchify | "Chop + flatten" | Slice image into non-overlapping patches, flatten each to a vector. |
| Patchify | "切分 + 展平" | 将图像切成不重叠的 patch，每个展平为向量。 |
| `[CLS]` token | "The image summary" | Prepended learnable token; its final embedding is the image representation. |
| `[CLS]` token | "图像摘要" | 预置的可学习 token；其最终嵌入是图像表示。 |
| Inductive bias | "What the model assumes" | ViT has fewer priors than CNNs; needs more data to make up the gap. |
| 归纳偏好 | "模型假设了什么" | ViT 的先验比 CNN 少；需要更多数据来弥补差距。 |
| DINOv2 | "Self-supervised ViT" | Trained without labels using image augmentation + momentum teacher. Best general image features in 2026. |
| DINOv2 | "自监督 ViT" | 使用图像增强 + 动量教师无标签训练。2026 年最佳通用图像特征。 |
| SigLIP | "CLIP's successor" | ViT + text encoder trained with sigmoid contrastive loss; better than CLIP on matched compute. |
| SigLIP | "CLIP 的继承者" | 用 sigmoid 对比损失训练的 ViT + 文本编码器；相同计算量下优于 CLIP。 |
| Swin | "Windowed ViT" | Hierarchical ViT with local attention + shifted windows; sub-quadratic. |
| Swin | "窗口 ViT" | 带局部注意力 + 移位窗口的层级 ViT；亚二次复杂度。 |
| Register tokens | "2023 trick" | A few extra learnable tokens that soak up attention sinks; improves DINOv2 features. |
| Register tokens | "2023 技巧" | 几个额外的可学习 token，吸收注意力汇聚；改善 DINOv2 特征。 |

## Daha fazla okumak

- [Dosovitskiy et al. (2020). An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale](https://arxiv.org/abs/2010.11929)- ViT kağıdı.
  Çeviri:VİT
- [Touvron et al. (2021). Training data-efficient image transformers & distillation through attention](https://arxiv.org/abs/2012.12877)- Dönüşüm.
  Çeviri:DeiT 论文。
- [Liu et al. (2021). Swin Transformer: Hierarchical Vision Transformer using Shifted Windows](https://arxiv.org/abs/2103.14030)- Swin.
  Çeviri:Swin Transformer
- [Oquab et al. (2023). DINOv2: Learning Robust Visual Features without Supervision](https://arxiv.org/abs/2304.07193)DINOv2.
  Çeviri:DINOv2
- [Darcet et al. (2023). Vision Transformers Need Registers](https://arxiv.org/abs/2309.16588)DINOv2 için kayıt simgesi ayarlaması.
  Çeviri:DINOv2'in kayıt simgesi
