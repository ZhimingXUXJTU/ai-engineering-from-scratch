# Herhangi bir çözünürlük vizyonu: Patch-n'-Pack ve NaFlex 任意分辨率

> Gerçek görüntüler 224x224 kare değil. Bir makbuz 9:16, bir tablo 16:9, bir tıbbi tarama 4096x4096, bir mobil ekran görüntüsü 9:19.5. 2024'ten önceki VLM cevabı  her şeyi sabit bir kareye boyutlandır  OCR, belge anlayışı ve yüksek çözünürlüklü sahne analizini yapan sinyali atıyor. NaViT (Google, 2023) değişken çözünürlüklü yamaları blok diyagonal maske ile tek bir transformatör partiye paketleyebileceğinizi gösterdi. Qwen2-VL'nin M-RoPE (2024) mutlak pozisyon tablolarını tamamen düşürdü. LLaVA-NeXT'in AnyRes yüksek çözünürlüklü görüntülerini bir taban + alt görüntülere kaydırdı. SigLIP 2'nin NaFlex variansı (2025) artık her yön oranına hizmet vermek için tek bir kontrol noktası isteyen açık VLM'ler için varsayılan kodlayıcıdır. Bu ders, bir parça parça yaptırır.

> **【中文解读】**Gerçek dünya görüntüleri 224x224'in düz şekli değil  Rue de 9:16, tablo da 16:9, medikal görüntüler 4096x4096 olabilir  2024 yıl önce VLM 统一将图像缩小为固定正形, this will lose OCR、文档理解和高分辨率场景解析的关键信息──本课讲解如何让变压器以原始分辨率处理任意宽高比的图像──

> **【拓展：金融文档场景的分辨率挑战】**Finansal sahnelerde, raporlar, göndermeler, sözleşmeler ve diğer dosyaların genişliği binlerce farklılıktan çok daha yüksektir. Sıkı düz şekil kısaltılması, metin değişimlerine yol açar. OCR'nin hassaslığı düşer.

**Type:** Build  | **类型:** 构建
**Languages:** Python (stdlib, patch packer + block-diagonal mask)  | **语言:** Python（标准库，补丁打包器 + 块对角掩码）
**Prerequisites:** Phase 12 · 01 (ViT patches), Phase 12 · 05 (LLaVA)  | **前置知识:** Phase 12 · 01（ViT补丁）、Phase 12 · 05（LLaVA）
**Time:** ~120 minutes  | **时间:** ~120 分钟

>  **【前置】**Öğrenci bölümünün önüne geçin:Fase 12.01;;ViT Get图切成补丁;;Fase 12.05;;LLaVA 投影器);Fase 7.04;;RoPE 位置编码,本节用2D-RoPE)
>  **【类比】**NaViT'in yamac-n'-paketi = " taşımacılık 打包 ";; geleneksel ViT = her şeyi bir kutuya bir kutuya koymak;
> ️ **【易错点】**实现 NaViT 时忘记块对角掩码 → 三张图的补丁 会相互做注意,模型训练完全失败──修复:必须构建 (N,N) 的注意矩阵,只在每张图对应的补丁中允许注意,块外为 -inf──

## Öğrenme hedefleri

- Değişken çözünürlüklü görüntüler bir seriye paketle ve blok diyagonal dikkat maskesini oluştur.
  > Farklı çözünürlüklü görüntülerin düzeltmelerini bir diziye bağlayarak, köşelere karşı dikkatli bir yapı oluşturmak için bir yapı oluşturun.
- Verilmiş bir görev için AnyRes kapaklama (LLaVA-NeXT), NaFlex (SigLIP 2) ve M-RoPE (Qwen2-VL) arasında seçim yapın.
  > Görevlerine göre seç AnyRes 切片(LLaVA-NeXT)、NaFlex(SigLIP 2) veya M-RoPE(Qwen2-VL)。
- OCR, tablolar ve fotoğraflar için token bütçelerini boyutlarını değiştirmeden hesaplayın.
  > 計算無縮的情況下 OCR、圖表和攝影的代號 預算──
- Çekirde boyutlandırmanın üç başarısız modunun adını verin: sıkıştırılmış metin, kesilmiş içerik, dolguda harcadığı jetonlar.
  > 列举正方形缩放的三种失败模式:文字压缩、内容裁剪、padding 浪费──

## Sorun  sorun arka planı

Transformatörler bir dizi bekler. Bir parti aynı uzunlukta bir dizi yığınıdır. Eğer resimleriniz 224x224 ise, her seferinde 196 patch tokeni alırsınız, doldurma gerekmez, iş tamamlanmıştır. 224'e tren, 224'e çıkar, çözünürlüğü asla düşünmeyin.

> Transformer 期望固定长度序列──一批就是一堆等长序列──如果图像都是224x224,每次都产生196补丁代币,无需填充,问题解决──训练和推理都用224,永远不用考虑分辨率──

Dünya işbirliği yapmaz. Belgeler portredir (8.5x11 inç, 2:3-ish). Çart ekran görüntüleri manzara (16:9). Kitseler uzun ve ince (1:3). 2048x2048 veya daha büyük tıbbi görüntüleme gemileri. Mobil cihaz ekran görüntüleri 1170x2532 (0.46:1).

> 现实世界不配──文档是向的(8.5x11 英寸,约 2:3)──图表截图是横向的(16:9)──收据又高又窄(1:3)──医疗影像动 2048x2048或更大──移动设备截图是1170x2532(0.46:1)──

2024'e kadar üç seçenek ve bunların her birinin neden başarısız olduğu:

> 2024'ten önce üç seçim ve kendi başlarına başarısız olma nedenleri:

1. Sıkıntılı bir düzene göre şekil değiştirmek için, bir düzene göre şekil değiştirmek gerekir.
   > 缩放为固定正方形(224x224 或 336x336) ―― 缩放会扭曲文字和人脸──下采样会破坏图表标签和OCR 内容──LLaVA-1.5 之前的标准做法──
2. Resimlerin çoğunu atarsın ve biçim yeri seçmek kendi görüş sorunu.
   > 剪裁定宽高比──将丢弃大部分图像,而选择剪裁位置本身就是一个视觉问题──
3. En uzun tarafına kapatır. Bozukluğu düzeltir ama portre görüntülerine kapatmak için tokenlerin %50'ini harcıyor.
   > 填充至最长边──扭曲修复但对屏图像浪费50%+的代币 在填充上──所有填充代币的注意成本是二次的──

> **【中文解读】**Transformer 期望固定长度的序列──真世界图像宽高比各异,2024年前有三种做法:(1) 缩写为正方形文字变形、OCR 内容丢失;(2) 剪丢弃大量内容;(3) 填屏图像浪费 50%+ 的代币 在填充上,注意计算成本第二次增──

2024-2025'te cevap: transformatörün resmin doğuştan çözünürlüğünde parşömenler yemeye izin vermesi ve heterogen bir partiyi bir diziye nasıl paketleyeceğini bulması gerek.

> 2024-2025 yılları için cevap: Transformer'ı doğrudan orijinal çözünürlükte "eçi" eklemle, sonra da tasarlanmış bir diziye dönüştürmek için bir yöntem bulmaya çalışın.

## Konsepten bir şey.

### NaViT ve patch-n'-pack

NaViT (Dehghani et al., 2023) bu çalışmaları ölçekte gösteren makaledir.

> NaViT ((Dehghani  et al., 2023) bu düşünceyi büyük çapta kullanılabilir olarak kanıtladı.

1. Parçadaki her görüntü için, kendi yerel parçet çubuğunu seçilen bir parçet boyutunda hesaplayın (deyelim ki 14).
   > Satır içindeki her resim için, belirtilen ekleme büyüklüğü için, tıpkı 14) hesaplanmaktadır.
2. Her resmin yamalarını kendi değişken uzunluklı dizisine düzelt.
   > Her resim için değişen boyut serisi için düzeltme.
3. Tüm resimlerin parşlarını seri için uzun bir dizide birleştirin.
   > Tüm resimlerin düzeltmelerini bir dizi olarak birleştirir.
4. Bir blok diyagonal dikkat maskası yapın böylece A resminin yamaları sadece A resmin içinde yer alır.
   >  yapı blokları açılara dikkat çekmek için, A resminin düzeltmelerini sadece A resminin içindeki dikkat çekmek için 
5. Her patç için konum bilgileri taşın (2D RoPE veya bölümlü konum yerleşimleri).
   > Her bir eklemde yer bilgisi taşınır.

336x336 (576 jeton), 224x224 (256 jeton) ve 448x336 (768 jeton) ile üç görüntüden oluşan bir parti, 1600x1600 blok-diyagonal maskesi ile 1600 jeton dizisi haline gelir.

> Üç张不同分辨率图像(336x336=576 token、224x224=256 token、448x336=768 token)

NaViT ayrıca eğitim sırasında bölümsel yama düşüşünü de tanıttı.  İşi düzenleyen ve hızlandırıcı eğitim yapan parti boyunca %50'lik yama rastgele düşüş. SigLIP 2 buna mirasçı oldu.

> NaViT ayrıca eğitim zaman oranı %50'lik bir miktarı atıfta bırakıldı.

> **【中文解读】**NaViT'in çekirdeği: 三张不同分辨率的图像(576 + 256 + 768 = 1600 个代币) bir dizi olarak toplanmış, bloklara karşı köşeleri örtüştürerek resim üzerinde dikkat çekmesini önlemek için.

### AnyRes (LLaVA-NEXT)

LLaVA-NeXT'in AnyRes pragmatik bir alternatiftir. Yüksek çözünürlüklü bir görüntü ve sabit bir kodlayıcı (CLIP veya SigLIP 336) verildiği için, görüntüyi çiz:

1. Resimdeki boyut oranına en uygun bir çubuğun düzenini önceden tanımlanmış bir setten seçin  (1x1), (1x2), (2x1), (1x3), (3x1), (2x2), vb. .
2. Tüm resmini şebekeye kaydırın; her kaydırma 336x336 biçimine dönüşür.
3. Ayrıca küçük bir resim oluşturun: Tüm görüntü küresel bağlamlı bir simge olarak 336x336'a boyutlandırıldı.
4. Her tekelyi donmuş 336 kodlayıcıyla kodlayın. Tekel simgeleri + küçük resim simgeleri ile bağlayın.

2x2 grid ve miniatürde 672x672 görüntü için: 4 * 576 + 576 = 2880 görsel jeton. Pahalı ama etkili  LLM hem yerel ayrıntıları hem de küresel bağlamı görür.

AnyRes, kodlamanız dondurulduğunda ve yalnızca bir çözünürlüğü desteklediğinde seçilen yoldur. Büyük görüntüler için token sayısını patlatır (4x4 şeritte bir 1344x1344 görüntü 9216 + 576 ≈ 9800 token, 8k LLM bağlamının çoğunu doldurur).

> **【中文解读】**AnyRes  kodlayıcı için uygundur 结并支持单一分辨率的情况──代价是大图像的代码数增长(1344x1344 在4x4 网格下约9800 代码,几乎填满8k LLM 上下文)──它的优点是LLM 同时看局部细节和全局上下文──

### M-RoPE (Qwen2-VL)

Qwen2-VL, Multimodal Rotary Position Embedding'i tanıttı. NaViT'in kıramlı pozisyonları veya AnyRes'in kapak ve miniatür yerine, her yama 3 boyutlu bir konum (zamanlı, yükseklik, genişlik) taşıyor. Sorgu / anahtar dönümleri keyfi H, W ve zamanlı uzunluğu ele alıyor.

M-RoPE, yeniden eğitim almadan yerel dinamik çözünürlük gönderir. Herhangi bir HxW görüntüsünü beslediğinizde, yama ekleyici H/14 x W/14 jetonları üretir, her jeton (t=0, r=sır, c=col) konumunu alır, RoPE dikkatini doğru frekanslarla döndürür, yapılır. Qwen2.5-VL ve Qwen3-VL bunu sürdürür. InternVL3'in V2PE'si değişken kodlama ile aynı fikirdir.

AnyRes'den farklı olarak, M-RoPE, doğuşsal çözünürlükte O(H x W / P^2) tokensidir  çarpıcı bir plitel overhead yoktur. NaViT'den farklı olarak, hala ileriye bir görüntü bekler.

> **【中文解读】**M-RoPE her ekleme için üç boyutlu konumlandırır, herhangi bir H、W 和时间长度── herhangi bir HxW 图像, H/14 x W/14 个代币 üretmek için doğrudan girişi yapar.

### NaFlex (SigLIP 2) NaFlex 灵活分辨率

NaFlex, SigLIP 2 kontrol noktasının doğuştan hareket eden modudur. Tek bir model, sonuçta birden fazla dizi uzunluğu (256, 729, 1024 token) hizmet eder. İçeriden eğitim sırasında NaViT tarzı patch-n'-pack ve her patch için mutlak bölümsel pozisyonlar kullanır. Satış noktası: bir kontrol noktası, görev temelinde sonuçta token bütçenizi seçin.

Bir semantik görev için (sınıflama, geri alım), 256 token. OCR veya tablo anlayışı için, 1024 token.

> **【中文解读】**NaFlex'in çekirdek satışı noktası: bir kontrol noktası, tasarruflı görev seçimi token  bütçe 语义任务用256 token,OCR或图表理解用1024 token,无需重训练──

### Çanta maskası.

Bir blok diyagonal maskası, çoğu uygulamanın çarpışmasıdır.`N_total`Görüntüleri kapsar `i=0..B-1`uzunlukları ile `n_i`, maskeyi`M`şekli ile`(N_total, N_total)`Eğer her iki indeks aynı görüntü blokuna düşerse, 0'dur.

```
offsets = [0, n_0, n_0+n_1, ..., N_total]                         # 累积偏移量
M[i, j] = 1 iff there exists b where offsets[b] <= i < offsets[b+1] # 同一图像块内为1
                        and offsets[b] <= j < offsets[b+1]
```

Bu PyTorch'de bir satır.`torch.block_diag`FlashAttention'un değişken uzunluklu yolu (`cu_seqlens`) maskeyi tamamen atlar ve kumülatîf uzunluk tenzorunu kullanarak sırada bir şekilde düzenler.

> **【中文解读】**Blok karşı köşede gizlenir, her resim için düzenleme kendi kendine odaklanır, diğer resimlerin düzenlemelerini görmez.`cu_seqlens`) doğrudan toplama uzunluğu 张量 ile dikkat, sıfırlı gömülü atladı, hız yaklaşık 10 倍.

### - Bütçe belirtiler.

Görevlere göre stratejinizi seçin:

- OCR / belgeleri: 1024-4096 token. SigLIP 2 NaFlex 1024, veya AnyRes 3x3 + miniatür.
- Çarşivler ve kullanıcı arayüzü: 729-1024 token 384-448 native. Qwen2.5VL dinamik çözünürlük maksimum piksel kapalı.
- Doğal fotoğraflar: 256-576 token iyi. Aşağıdaki LLM yeterince görür. İçerik yoğunluğu yüksek olan tokenler için ödeme.
- Video: Yerel birleştirme sonrası çerçeve başına 64-128 token, 2-8 FPS. 12.17 ders bunu kapsar.

2026 üretim kuralı: her göreve maksimum piksel kapalı bir şey seçin, bu kapalı doğal boyut oranında kodlayın, partiyi paketleyin ve doldurmayı atlayın.`min_pixels`ve `max_pixels`Tam olarak bu düğmeye.

> **【拓展：Token 预算与成本优化】**Üretim ortamında, token  bütçesi doğrudan API'yi etkilemektedir 成本和延迟──OCR 任务 için 1024+ token dağıtılması gereklidir(文字 yoğunluğu yüksek), ancak doğal fotoğraflar ile 256 token yeterli olacaktır── görev hareketli ayarlama çözünürlüğü 2026 yılında VLM 部署ının en iyi uygulamasıdır──

> 🤔 **【困惑】**Öğrenme bölümünde de sorulur:1) OCR  sistemi, min_pixels 和 max_pixels Deployment için ne kadar ayarlanabilir? 文档类 min=28*28*4、max=28*28*2560(Qwen2-VL 默认); 过高会爆显存,过低会丢失小字──2) Neden doğrudan 2k×2k kullanmıyorsunuz? token ikinci patlama,长文档一张图就吃掉整个LLM 上下文──3) NaFlex vs AnyRes 哪个更通用? NaFlex(SigLIP 2) 更现代,单一点检查 适应所有分辨率;AnyRes 是过渡方案──

## Kullanın.
```figure
mm-patch-n-pack
```

## Kullan

`code/main.py`tam pixel koordinatları olan heterogen bir görüntü parti için patch-n'-pack uygulamaktadır.

> `code/main.py`Tüm sayısal görüntü sitatölyesi ile farklı görüntüler paketini gerçekleştirilmiştir.

- (H, W) görüntü boyutlarının bir listesini alır.
  > 接收 (H, W) 图像尺寸列表──
- Her resmin patch dizisi uzunluğunu patch boyutu 14'te hesaplar.
  > 計算每张图像在补丁大小 14 下的序列长度──
- Toplam uzunluğunda bir diziye paketler .`sum(n_i)`- Evet .
  > 打包为总长度 `sum(n_i)`Tek bir dizi.
- Blok diyagonal dikkat maskesini (yaklaşıklık için yoğun) oluşturur.
  > 构建块对角注意力掩码 (Köşeye dikkat çekmek için çok kolay)
- Paketlenmiş maliyet ile kare boyut ve AnyRes kapak karşılaştırır.
  > Çekim ve kesim için yapılan bir kısım karşılaştırıldığında.
- Karışık bir parti için bir belirti bütçe tablosunu basar (girdi, tablo, ekran görüntüsü, fotoğraf).
  > 打印混合批次(收据、图表、截图、照片) 预算表

Çıkış sayıları 2026'da açılan her VLM'nin patch-n'-pack'i kullanmasının nedeni.

> Çaplanan rakam her 2026'da patch-n'-pack kullanma nedenidir.

## Gönderin.

Bu ders bize çok yararlı .`outputs/skill-resolution-budget-planner.md`. Karışık bir yön oranlı iş yükü (OCR, tablolar, fotoğraflar, video çerçeveleri) ve toplam bir token bütçesi göz önüne alındığında, doğru stratejiyi (NaFlex, AnyRes, M-RoPE veya sabit kare) seçer ve istek başına bir yapılandırma yayar.

> 本课产 出 `outputs/skill-resolution-budget-planner.md` Önemli bir karıştırma genişliği ile çalışma yükü  OCR ✓ tablo ✓ fotoğraf ✓ video ) ve toplam token  bütçe, doğru strateji seçer  NaFlex ✓ AnyRes ✓ M-RoPE veya sabit düz şekil) ve istedikleri şekilde oluşturur  Ürünler için VLM ölçekleri seçerken bu beceri kullanmak  Bu beceri  Bu                                                                                                                                                                                                              

> **【中文解读】**Bu ders çıkış çözünürlük bütçe planlama aracı.

## Egzersizler.

1. Bir makbuz 600x1500 (1:2.5) olarak 14 boyutlu bir yama ile, kaç tane yerel çözünürlüklü token? 336'ya kare boyutundan sonra kaç tane?
   | 一张收据 600x1500（1:2.5）。补丁大小14下，原始分辨率多少 token？缩放到336正方形后多少？实际中哪种 OCR 精度损失更大？

2. 256, 576, 729, 1024 uzunlukları olan dört görüntü için blok diyagonal maskesini yapın. dikkat matrisinin 2585x2585 olduğunu ve tam olarak `256^2 + 576^2 + 729^2 + 1024^2`sıfır dışı girişler.
   | 为四张长度分别为 256、576、729、1024 的图像构建块对角掩码。验证注意力矩阵为 2585x2585 且非零元素数精确为 `256^2 + 576^2 + 729^2 + 1024^2`。

3. Patch 14'te 1792x896 görüntü için: (a) kare boyutunu 336'a çevirin ve sonra kodlayın, (b) AnyRes 2x1 + miniatür, (c) M-RoPE'de yerel olarak. Hangi token en az kullanılır?
   | 对于 1792x896 的图像（补丁14），对比：(a) 缩放到336正方形，(b) AnyRes 2x1+缩略图，(c) M-RoPE 原始分辨率。哪种 token 最少？哪种保留最多细节？

4. Fraksiyonel patch düşüşü uygulayın: paketlenmiş bir dizi verildiğinde, simgelerin %50'ini rastgele olarak düşürün ve blok-diyagonal maskanı buna göre güncelleyin. Maskenin kısıtlılık değişikliğini ölçün.
   | 实现分数补丁丢弃：给定打包序列，随机均匀丢弃50%的token，更新块对角掩码，测量掩码稀疏度变化。

5. Qwen2-VL makalesinin 3.2 bölümünü okuyun (arXiv:2409.12191).`min_pixels`ve `max_pixels`kontrol ve neden her iki sınır da önemli.
   | 阅读 Qwen2-VL 论文第 3.2 节（arXiv:2409.12191）。用两句话描述 `min_pixels` 和 `max_pixels` 控制什么，为什么两个边界都很重要。

## Anahtar Terimler

| Term | What people say | What it actually means | 中文含义 | 中文释义 |
|------|-----------------|------------------------|----------|---------|
| Patch-n'-pack | "NaViT-style packing" | Concatenate variable-length patch sequences from different images into one batch dimension | 将不同图像的可变长度补丁序列拼接到一个批次维度 | |
| Block-diagonal mask | "Packing mask" | Attention mask that confines each image's patches to attend only to themselves, not neighbors in the pack | 块对角掩码：限制每张图像的补丁只关注自身 | |
| AnyRes | "LLaVA-NeXT tiling" | Split a high-res image into a grid of fixed-size tiles plus a global thumbnail; encode every tile with a fixed encoder | 将高分辨率图像切分为固定大小网格+全局缩略图 | |
| NaFlex | "SigLIP 2 native-flex" | Single SigLIP 2 checkpoint that serves 256/729/1024-token budgets at inference without retraining | 单一 SigLIP 2 checkpoint 推理时支持多种 token 预算 | |
| M-RoPE | "Multimodal RoPE" | 3D rotary position encoding (time, row, column) that handles arbitrary H, W, T without position tables | 三维旋转位置编码（时间、行、列），处理任意宽高和时间长度 | |
| cu_seqlens | "FlashAttention packing" | Cumulative-length tensor the FlashAttention varlen path uses instead of a dense block-diagonal mask | FlashAttention 可变长度路径使用的累积长度张量 | |
| min_pixels / max_pixels | "Resolution bounds" | Qwen2.5-VL per-request knobs capping token count on very small or very large inputs | Qwen2.5-VL 按请求控制最小/最大像素数的参数 | |
| Visual token budget | "How many tokens per image" | Rough count of patch tokens emitted per image; sets the LLM's prompt budget and attention cost | 每张图像产生的补丁 token 数，决定 LLM 的提示预算和注意力成本 | |

## Daha fazla okumak

- [Dehghani et al. — Patch n' Pack: NaViT (arXiv:2307.06304)](https://arxiv.org/abs/2307.06304)NaViT'in istedikleri çözünürlük eğitimi
- [Wang et al. — Qwen2-VL (arXiv:2409.12191)](https://arxiv.org/abs/2409.12191)# Qwen2-VL çok modoldur dönüm pozisyon kodlama
- [Laurençon et al. — What matters when building vision-language models? (Idefics2, arXiv:2405.02246)](https://arxiv.org/abs/2405.02246)VLM'i oluşturmanın anahtar faktörleri
- [Tschannen et al. — SigLIP 2 (arXiv:2502.14786)](https://arxiv.org/abs/2502.14786)# Siglip 2 NaFlex
- [Qwen Team — Qwen2.5-VL Technical Report (arXiv:2502.13923)](https://arxiv.org/abs/2502.13923) Qwen2.5VL  Teknik rapor
