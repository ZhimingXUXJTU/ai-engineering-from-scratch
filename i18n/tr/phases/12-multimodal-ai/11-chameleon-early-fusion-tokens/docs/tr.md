# Chameleon ve erken füzyon simgesi-tek çok model modeller

> Şimdiye kadar gördüğümüz her VLM'de görüntü ve metin ayrı kalıyor. Görsel tokenler bir görme kodlayıcısından gelir, bir projektorun içine akıyor, sonra LLM içinde metin buluyorlar. Görme ve metin sözlükleri asla üst üste geçmez. Chameleon (Meta, Mayıs 2024) sordu: Ya yaparlarsa? Bir resmini paylaşılmış bir kelime kaynağından ayrı bir token dizisine dönüştüren bir VQ-VAE eğit. Her multimodal belge şimdi tek bir dizi  metin işaretleri ve görüntü işaretleri birbirine karışmış, tek bir autoregressive kaybı. Yan etkisi: model, tek bir sonuç çağrısında değişen metin ve görüntü belirtilerini  karışık modalite çıkışları oluşturabilir. Bu ders erken bir birleşme tezini okuyor ve bir oyuncak versiyonu sonuna kadar inşa ediyor.

> **【中文解读】**Chameleon (Meta,2024年5月) bir çeşit yoğun bir çok biçimli yöntem önerdi: VQ-VAE ile görüntüyi dağıltılı bir token olarak dönüştürmek, metin token ile bir kelime metni paylaşmak, tek bir kendi kendine dönüş kaybı eğitimi kullanarak. Bu şekilde model hem anlayabilir hem de karışık biçimli içeriği oluşturabilir.

> **【拓展：早期融合 vs 后期融合】**之前所有 VLM(LLaVA、BLIP-2、Qwen-VL)都保持图像和文本分离──Chameleon'un " erken birleşimi" anlamı, ilk baştan beri aynı uzayda işlenmiş olan resim ve metinlerdir.

**Type:** Build  | **类型:** 构建
**Languages:** Python (stdlib, VQ-VAE tokenizer + interleaved decoder) | **语言:** Python（标准库，VQ-VAE tokenizer + 交织解码器）
**Prerequisites:** Phase 12 · 05, Phase 8 (Generative AI) | **前置知识:** Phase 12 · 05，Phase 8（生成式 AI）
**Time:** ~180 minutes | **时间:** ~180 分钟

>  **【前置】**Önemli bir şekilde, bu süreçte, "Lavya karşıtı" olan bir diğer uçta olan "Chameleon" da "Lavya karşıtı" olan bir diğer uçta olan "Lavya karşıtı" olan bir diğer uçta olan "Chameleon" da "Lavya karşıtı" olan bir diğer uçta olan "Lavya karşıtı" olan bir diğer uçta olan "Lavya karşıtı" olan bir diğer uçta olan "Lavya karşıtı" olan bir diğer uçta olan "Chameleon" da vardır.
>  **【类比】**Chameleon = "welt语"──LLaVA = 翻译机(视觉编码器把图片翻译成 LLM 能懂的语言);Chameleon = 世界语(图片和文本都用同一种人造语言,模型不用翻译)──世界语'in faydaları,

## Öğrenme hedefleri

- Paylaşılan kelime birikimi + tek kayıpın neden modelin yapabileceği şeyi değiştirdiğini açıklayın.
  > 解释为什么共享词汇表 + 单一损失能改变模型能力──
- Bir VQ-VAE'nin bir transformerin bir sonraki belirtilmiş hedefiyle uyumlu bir ayrı bir dizine bir görüntüyi nasıl işaretlediğini açıklayın.
  > 描述 VQ-VAE 如何将图像分词为与变压器 下一代标志 目标兼容的离散序列──
- Chameleon'un eğitim ve istikrar hilelerini isimlendirin: QK-Norm, bırakma yerleştirme, LayerNorm siparişleri.
  > 列举 Chameleon's training稳定性技巧:QK-Norm、Dropout 位置、LayerNorm 顺序。
- Chameleon vs BLIP-2'in Q-Former yaklaşımını karşılaştırın ve her biri doğru seçim olduğunda açıklayın.
  > Şemalı ile BLIP-2'nin Q-Former 方案ini karşılaştırın, kendi uygunluklarını anlatın.

## Sorun  sorun arka planı

Adaptör tabanlı VLM'ler (LLaVA, BLIP-2, Qwen-VL) metin ve görüntüyi iki farklı şey olarak değerlendirir.`embed(text_token)`Bir görüntü geçer .`visual_encoder(image) → projector → ... pseudo_tokens`Modelin iki giriş yolu var.

> 适配器式 VLM(LLaVA、BLIP-2、Qwen-VL) 文本と图像视为两种不同的东西──文本代号 通过 通过 通过`embed(text_token)`Çizgilik yoluyla`visual_encoder(image) → projector → ... pseudo_tokens`◊ Modelle iki bölüm vardır.

Üç sonuç:

> Üç sonuç:

1. LLM sadece görüntü tüketir, yayınlamaz.
   ÇINCE TRÜBLÜK:LLM Sadece resim tüketir, resim üretemez.
2. Karışık modalite belgeleri (bir makalede olduğu gibi alternatif paragraflar ve görüntüler) garip  ya model dışında ya da zincir nesillerinde multimodal girişleri analiz edersiniz.
   Çinçe Çevirim:混合模态文档 (Hikstraz)
3. Distribüsiyonal eşleşme eksikliği. Görsel jetonlar ve metin jetonları gizli alanın farklı bölgelerinde yaşar ve ince bir uyum sorunları yaratır.
   Çin Çeviri: dağılmamış. Görüş simgesi ve metin simgesi  gizli alanın farklı bölgelerinde bulunur.

Chameleon, bu önyargıyı reddediyor: görüntüler, paylaşılmış bir sözlükten ayrı bir token sekanslarıdır. Modelli birbirine karışmış belgelere uygulayın, bir kayıp, bir autoregressive decoder ve karışık modalite üretimini ücretsiz olarak açarsınız.

> Chameleon  reddetti bu varsayım: görüntü sadece paylaşım sözcükleri ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒  ⇒ ⇒ ⇒     ⇒ ⇒ ⇒  ⇒            ⇒ ⇒ ⇒              ⇒                                                                                                               

## Konsepten bir şey.

> **【中文解读】**Chameleon(Meta) erken bir birleşim stratejisini benimsedi: görüntü ve metin tümü bir token 序列 olarak dağıtıldı, aynı Transformer ile 处理。 görüntü VQGAN üzerinden 编码为离散 token,与文本 token 在同一词表中──这是统一多模态理解的极致实现──

> **【拓展：早期融合 vs 晚期融合】**早期融合 (Chameleon) 多模态统一到同一代号空间,理论上优雅但训练成本高──晚期融合 (LLaVA) 保持视觉和语言模型独立性通过桥接层连接,训练更高效──


### VQ-VAE görüntü simgeselcisi olarak

Tokenizer, vektörlü kuantitasyonlu bir otomatik kodlayıcıdır.

> 分词器 bir 量化变分自编码器──架构如下:

- Kodlayıcı: CNN + ViT görüntüyi bir uzay özellik haritasına haritası yapan, dim 256'nin 32x32 özelliklerini söyleyin.
  Çinçe Çevirisi:编码器:CNN + ViT resimleri 32x32 个维度为 256 个特征为空间特征图 olarak görüntüleyecektir.
- Kod kitabı: K vektörlerinin öğrenilmiş bir kelime kaynağı (Chameleon 8192 kullanır), aynı zamanda 256'yi de zayıflatır.
  Çine dilinde: 个学习向量的词汇表 (Chameleon 使用 8192 个), ayrıca 256 维──
- Kvantisa: her alan özelliği için, L2 mesafe ile en yakın kod defteri girişini arayın. Sürekli özelliği tam sayı endeksi ile değiştirin.
  Çinçe Çevirimiçi: 量化: L2 ile tüm uzay özelliklerini değiştirmek için en son kod kod bu 条目ı bulmak için.
- Çözücü: CNN'de kuantistik özellikler pixel olarak geri götürülür.
  Çinçe Çevirisi: CNN Resim için yeniden inşa edilmek için özellikleri ölçecek.

Eğitim: VAE yeniden yapılandırma kaybı + bağlılık kaybı + kod defteri kaybı.

> 訓練:VAE 重建损失 + 承诺损失 + 码本损失──码本索引构成图像的离散字母表──

Şameleon için: bir görüntü 32*32 = 1024 token oluşturuyor. 8192 kelimeden alınmıştır. Metin tokenleriyle (LLM'nin BPE kelimelerinden, 32000 diyoruz) birleştirilmiştir. Son kelime: 40192. Transformatör bir dizi, bir kayıp görür.

> 对于 Chameleon:一张图像变成32*32 = 1024 个标记, 来自8192 的词汇表――与文本标记( 来自LLM 的 BPE 词汇表,如32000) 拼接──最终词汇表:40192──Transformer 见一个序列,一个损失──

### Paylaşılan kelime birikimi

Chameleon'un kelime birikimi metin jetonları, görüntü jetonları ve modalite ayırıcılarını birleştirir. Her jeton tek bir kimliğe sahiptir. Giriş yerleştirme katmanı her kimliği bir D-dim gizli vektörüne haritası yapar. Çıkış projeksiyonu sözcük logitlerine geri gizlenir. Softmax, bir sonraki jetonu seçer.

> Chameleon'un kelime çizelgesi metin belirtilerini, resim belirtilerini ve biçim ayrımlarını birleştirir. Her bir belirtiye eşsiz bir ID vardır. Giriş yerleşim katmanı her bir ID'yi D 维隐藏向量に映射する.

Ayrıcılar önemli: `<image>`ve `</image>`Etiketler görüntü belirtilen dizini destekler.`<image>`, aşağı akımlı yazılım, önümüzdeki 1024 tokeni pixel gösterimi için dekodere göndermek için VQ indeksleri olduğunu biliyor.

> Bölünme çok önemli:`<image>`和 `</image>`Etiket paketleme resim simgesi 序列──生成时,如果模型输出 `<image>`Sonraki 1024 token VQ indeks olduğunu biliyordu.

### Karışık modalite üretim

İndirim, paylaşılmış kelimeforumunda bir sonraki belirti tahminidir. Örnek istek: "Bir kedi çiz ve onu tanımla".

> 推理是共享词汇表中的下一代币 预测。 örnek提示:"画一只猫并描述它──"Chameleon 输出:

```
<image> 4821 1029 2891 ... (1024 image tokens) </image>
The cat is orange, sitting on a windowsill...
```

Model, sırayı kendiliğinden seçer.  görüntü, sonra metin, metin, sonra görüntü veya ara bırakma üretebilir. Aynı dekodör, aynı kaybı.

> Model kendi kendine seçimi sırası  önce resim  önce resim  önce resim  veya aynı çözücü, aynı kaybı 

Sadece metin üretilen adapter VLM'lerle karşılaştırın.

> Cameleon yeniden açtı Modell Output Modem sorunu

### Eğitim istikrarı  QK-Norm, bırakma, LayerNorm sipariş

Erken füzyon eğitimi ölçeğinde dengesiz.

> 早期融合 eğitimi büyük ölçekte belirsizliğe neden olmuştur.

- QK-Norm. LayerNorm'u nokta ürünü öncesinde dikkat içindeki sorgu ve anahtar projeksiyonlarına uygulayın.
  Çinçe Çevirimiçi:QK-Norma.                                                                                                                                                                                                                                                        
- Arıza ve MLP'den sonra değil, her kalan eklemeden sonra bırakın.
  Çinçe Çevirimi:Droput 位置──在每次残差加法后放 Dropout,不仅是注意和MLP 后──当图像代币的梯度可能主导时需要更多正则化──
- LayerNorm düzenleme. Geri kalan dalda (standard) öncesi LN, son blokun atış bağlantısında ek bir LN. Son katman gradient akışını istikrarlı kılar.
  Çinçe Çevirimiçi:LayerNorm 顺序──残差分支上的 Pre-LN(standard做法),加上最后一块跳跃连接上的额外LN──稳定最后一层的梯度流──

Bu hileler olmadan 34B-param kameleon eğitimi birden fazla kontrol noktasında farklılaşmış ve onlarla birleşti.

> Bu teknikler olmadan 340 milyarlık parametre sahip olan Kameleon, birçok kontrol noktasında eğitim görüyor.

### Tokenizer'in yeniden inşaat tavanı

VQ-VAE kayblıdır. 8192 kod defteri girişinde ve 512x512 görüntü başına 1024 token'de, yeniden yapılandırma PSNR kaplamaları 26-28 dB civarında. Bu tanınabilir görüntü gen için yeterli ama sürekli uzay difüzyonundan görünüşe göre daha kötüdür (Stable Diffusion 3 32+ dB'ye ulaşır).

> VQ-VAE 已损失的──8192 个码本条目和每张 512x512 图像 1024 个代币, yeniden inşa PSNR 上限约26-28 dB──足以生成可识别的图像,但明显差于连续空间扩散(Stable Diffusion 3 达到32+ dB)──

Tokenizer, şişe boğazıdır. Daha iyi tokenizerler (MAGVIT-v2, IBQ, SBER-MoVQGAN) tavanı kaldırır. Emu3 (Desin 12.12) yalnızca daha iyi tokenizer aracılığıyla SDXL kalitesi üretimini sağlar.

> 分词器是瓶──更好的分词器(MAGVIT-v2、IBQ、SBER-MoVQGAN) 能提高上限──Emu3(第 12.12 课) Sadece daha iyi分词器 ئارقىلىق SDXL kalitesi üretimi gerçekleştirilmiştir──

### Kameleon vs BLIP-2 / LLaVA

Kameleon (erken birleşme, ortak kelime):
- Bir kayıp, bir dekoder.
  Çıktı.
- Karışık modalite çıkışı üretir.
  Çeviri:                                                                                                                                                                                                                                                             
- Tokenizer kalite tavanıdır.
  Çınca sözcükler: 分词器是质量上限.
- Pahalı: VQ-VAE dekodörü, sonuç yolu üzerinde üretilen görüntü başına.
  Çin Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Ç Ç Çev Çev Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç

BLIP-2 / LLaVA (son birleştirme, ayrı kuleler):
- Görüş içeri, mesaj sadece.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri
- Ön eğitimli LLM'yi tekrar kullanıyor.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri
- Anlamak için tokenizer boğazı yok.
  Çeviri: anlamı var.
- Ucuz: tek ileri geçiş.
  Çeviri: 便宜:单次前向传播。

Eğer görüntü üretimi, Chameleon ailesine ihtiyacınız varsa, sadece anlayış istiyorsanız, adapter-VLM daha basit ve daha önceden eğitilmiş hesaplama kullanır.

> 按任务选择──如果需要图像生成,选择Cameleon 系列──如果只需要理解,适配器 VLM 更简单且复用更多预训计算──

### Fuyu ve AnyGPT

Fuyu (Adept, 2023) ilgili bir yaklaşımdır: ayrı görme kodlayıcısını tamamen atlayın, LLM'nin giriş projesi yoluyla ham görüntü yamalarını tıkınlar gibi besleyin, tıkınlayıcı yok.

> Fuyu(Adept,2023) bir ilgili yöntemdir: tamamen bağımsız bir görsel kodlayıcı üzerinden atlamak, LLM'nin giriş projesi yoluyla orijinal görüntü yamacını, sanki onlar bir jeton gibi, hiçbir分词器──kameleon daha basit, ama kaybetti ortak sözcük 词汇表的输出成──

AnyGPT (Zhan et al., 2024) Cameleon'u dört modaya genişletiyor: metin, görüntü, konuşma, müzik. Her biri için aynı VQ-VAE hilesi, paylaşılan dönüştürücü. Herhangi bir nesle.

> AnyGPT(Zhan 等人,2024) Camelion'u dört modola yayılacak:文本、图像、语音、音乐──每种模态相同的VQ-VAE 技巧,共享 Transformer──任意到任意生成──第 12.16 课详细介绍──


> **【拓展：早期融合的训练挑战】**早期融合 gerektirir görüntü ve metin birleştirilmesine, görüntü tokenizatörünün kalite gereksinimleri çok yüksek. Meta'nın Kameleon 8192 kodlı VQGAN kullanılarak ImageNet'te yeniden yapılandırma kalitesi (rFID yaklaşık 5.0) ve metin uyumluluğu arasında dikkat çekildi.


## Kullanın.
```figure
vq-codebook
```

## Kullan

`code/main.py`Oyuncakların sonundan sonuna erken bir birleşim modeli oluşturur:

> `code/main.py`Bir son son oyuncak erken birleşim modeli oluşturmak:

- 8x8 patchleri kod defteri indekslerine (K=16) haritası yapan küçük bir VQ-VAE tarzı kuantitör.
  Çine dilinde: 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書 図書
- Paylaşılan bir kelime birikimi (metin kimlikleri 0..31) + (resim kimlikleri 32..47) + (paylayıcılar 48, 49).
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Ç Ç Çeviri: Ç Ç Ç Ç Ç Ç Ç Çeviri: Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç
- Sintez başlık + görüntü-töken diziler üzerinde eğitilmiş bir oyuncak autoregressive decoder (bigram tablosu).
  Çinçe Çevirimi: bir oyuncak kendi kendine çözücü ()
- Bir istek verildiğinde alternatif metin + görüntü belirtilerini yayılan örnekleme döngüsü.
  Çeviri: Çeviri, Çeviri, Çeviri, Çeviri, Çeviri, Çeviri, Çeviri, Çeviri, Çeviri, Çeviri, Çeviri, Çeviri, Çeviri, Çeviri, Çeviri, Çeviri, Çeviri, Çeviri, Çeviri, Çeviri, Çeviri, Çeviri, Çeviri, Çeviri, Çeviri, Çeviri, Çeviri, Çeviri, Çeviri, Çeviri, Çeviri, Çeviri, Çeviri, Çeviri, Çeviri, Çeviri, Çeviri, Çeviri, Çeviri, Çeviri, Çeviri, Çeviri, Çeviri, Çeviri, Çeviri, Çeviri, Çeviri, Çeviri, Çeviri, Çeviri, Çeviri, Çeviri, Çeviri, Çeviri, Çeviri, Çeviri, Çeviri, Çeviri, Çeviri, Çeviri, Çeviri, Çeviri, Çeviri, Çeviri, Çeviri, Çeviri, Çeviri, Çeviri, Çeviri, Çeviri, Çeviri, Çeviri, Çeviri, Çeviri, Çeviri, Çeviri, Çeviri, Çeviri, Çeviri, Çeviri, Çeviri, Çeviri, Çeviri, Çev, Çev, Çev, Çev, Çev, Çev, Çev, Çev, Çev, Çev, Çev, Çev, Çev, Çev, Çev, Çev, Çev, Çev, Çev, Çev, Çev, Çev, Çev, Çev, Çev, Çev, Çev, Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çek Çek Çek Çek Çek Ç

Kod kasıtlı olarak transformatörü küçük tutar (bigramlar) böylece sinyal akışını sonundan sonuna kadar takip edebilirsiniz.

> Transformer'ı çok küçük tutun. Böylece sinyal akımını takip edebilirsiniz.

## Gönderin.

Bu ders bize çok yararlı .`outputs/skill-tokenizer-vs-adapter-picker.md`. Ürün özelliklerini göz önüne alarak (tek anlamak vs. anlamak + oluşturmak, gerekli görüntü kalitesi, maliyet bütçesi) Chameleon-familie (erkek füzyon) ve LLaVA-familie (kenak füzyon) arasında seçim yaparak, kuantitatif kurallarla haklı çıkar.

> 本课产 出 `outputs/skill-tokenizer-vs-adapter-picker.md`◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊                                                                                                                                                                                                                            

## Egzersizler.

1. Chameleon, 512x512 görüntü başına K=8192 kod defteri girişlerini ve 1024 jetonu kullanır.
   Çinçe Çevirimi:Chameleon Kullanım K=8192 个码本条目和每张 512x512 图像 1024 个代币。

2. Aynı VQ-VAE yoğunluğundaki 4K görüntü (3840x2160) kaç görüntü belirti üretir? Bir Chameleon tarzı modeli bir sonuç çağrısında 4K görüntü oluşturabilir mi?
   Çine çevirisi:4K 图像(3840x2160) aynı VQ-VAE 密度 altında kaç resim simgesi üretilir?Chameleon 风格的模型能一次推理调用生成4K 图像吗?

3. Temiz Python'da QK-Norm uygulamak. 64 boyutlu bir sorgu ve anahtar verildiğinde, LayerNorm'den önce ve sonra nokta ürünü göster. Büyüklük kontrolü derinliklerde neden önemlidir?
   Çinçe çeviri: saf Python ile QK-Normayı gerçekleştirmek için.

4. "Chameleon" Bölümü 2.3'i okuyun. 34B'de QK-Norm olmadan gözlemlenen kağıtın tam başarısızlık modunu açıklayın. "Norma patlaması" imzası neydi?
   Çinçe çevirisi: Çameleon bölüm 2.3. eğitim sabitliği hakkında.

5. Oyuncak dekodörünü sadece metin istekleri verildiğinde karışık bir modaliyetli bir yanıt yayınlamak için genişlet. Modelin önce görüntü vs. önce metin seçtiğini ölçün.
   Çinçe Çevirisi: Genişle oyuncak çözücü, belirli saf metin önerisi sırasında karışık bir modem yanıt göndermesini sağlar.

## Anahtar Terimler

| Term | What people say | What it actually means | 中文含义 | 中文释义 |
|------|-----------------|------------------------|---------|
| Early fusion | "Unified tokens" | Images converted to discrete tokens sharing the transformer's vocabulary from step one | 图像从第一步就转换为与 Transformer 共享词汇表的离散 token |
| VQ-VAE | "Image tokenizer" | CNN + ViT + codebook that maps images to integer indices the transformer can predict | CNN + ViT + 码本，将图像映射为 Transformer 可预测的整数索引 |
| Shared vocabulary | "One dictionary" | A single token ID space covering text + image + modality separators | 覆盖文本 + 图像 + 模态分隔符的单一 token ID 空间 |
| QK-Norm | "Attention stabilizer" | LayerNorm applied to query and key before their dot product, prevents norm blowup | 在 query 和 key 点积前应用 LayerNorm，防止范数爆炸 |
| Mixed-modality generation | "Text + image output" | Inference that autonomously produces interleaved text and image tokens in one pass | 推理时自主产生交替的文本和图像 token |
| Codebook size | "K entries" | Number of discrete vectors the VQ-VAE can quantize to; trades compression for fidelity | VQ-VAE 可量化到的离散向量数；压缩与保真度的权衡 |
| Tokenizer ceiling | "Reconstruction limit" | Best PSNR achievable by decoding VQ tokens; bounds the model's image quality | 解码 VQ token 可达到的最佳 PSNR；限制模型的图像质量上限 |

## Daha fazla okumak

- [Chameleon Team — Chameleon: Mixed-Modal Early-Fusion Foundation Models (arXiv:2405.09818)](https://arxiv.org/abs/2405.09818)
  Çine çevirisi:Chameleon 混合模态早期融合基础模型。
- [Aghajanyan et al. — CM3 (arXiv:2201.07520)](https://arxiv.org/abs/2201.07520)
  Çeviri:Chameleon'un önümüzdeki yaşamı
- [Yu et al. — CM3Leon (arXiv:2309.02591)](https://arxiv.org/abs/2309.02591)
  Çine çevirisi:CM3Leon,Chameleon'un yakın yakınları
- [Zhan et al. — AnyGPT (arXiv:2402.12226)](https://arxiv.org/abs/2402.12226)
  Çinçe Çevirim:AnyGPT, genişletilmiş dört mod mod mod modolu
- [Adept — Fuyu-8B blog (adept.ai)](https://www.adept.ai/blog/fuyu-8b)
  Çeviri:Fuyu-8B 博客,跳过视觉编码器的方案.
