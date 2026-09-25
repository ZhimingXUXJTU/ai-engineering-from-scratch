# Emu3: Next-Token Tahmin Görüntü ve Video Yükleme için Emu3: aşağıdaki token kullanın 预测生成图像与视频

> BAAI'nin Emu3 (Wang et al., Eylül 2024) yayılma karşı-autoregressive tartışmayı bitirecek olan 2024 sonucu. Tek bir Llama tarzı dekoder-tek dönüştürücü, sadece bir sonraki belirti-bunu tahmin amacıyla eğitilmiş, tek bir kelime birikimi üzerinden metin + VQ görüntü belirtiler + 3D VQ video belirtiler, görüntü üretimi SDXL ve algılama LLaVA-1.6 yener. Klip kaybı yok. Yayılma programı yok. Kalite için sonuca çıkarma için sınıflandırıcı dışı rehberlik kullanılır, ancak temel eğitim amacı öğretmen zorlama ile bir sonraki belirti tahminidir. Nature dergisinde yayınlandı. Bu ders Emu3 tezini okuyor  neden daha iyi bir tokenizer artı ölçek tüm ihtiyacınız  ve difüzyon yaklaşımlarıyla karşıt.

> **【中文解读】**Emu3(BAAI,2024 yıl Eylül) tek bir kendi kendine geri dönüşün bir teker tokeni kullanarak 预测目标,统一文本+图像+视频词汇表上训练,图像生成上击败SDXL,视觉理解上击败LLaVA-1.6──没有CLIP 损失,没有扩散调度,核心训练目标就是下一 token 预测──发表在自然上──

> **【拓展：自回归 vs 扩散的争论】**Emu3'ün temel katkıları kavramsaldır: Eğer aşağıdaki token 预测 图像生成上匹敌扩散模型, 统一模型路径 (one loss, one bone干, any mode) ⇒可行──后续的 Show-o、Janus-Pro、InternVL-U ⇒ 统一模型路径 (one loss, one bone干, any mode) ⇒ 统一模型路径 (one loss, one bone干, any mode) ⇒ 统一模型路径 (one loss, one bone, any mode) ⇒ 统一模型路径 (one loss, one bone, any mode) ⇒ 统一模型路径 (one loss, one bone, one structure) ⇒ 统一模型路径 (one loss, one structure, one structure, one structure, one structure, one structure) ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒  ⇒ ⇒ ⇒  ⇒         ⇒        ⇒                                                                                                                             

**Type:** Learn  | **类型:** 学习
**Languages:** Python (stdlib, 3D video tokenizer math + autoregressive sampler skeleton) | **语言:** Python（标准库，3D 视频分词器数学 + 自回归采样器骨架）
**Prerequisites:** Phase 12 · 11 (Chameleon) | **前置知识:** Phase 12 · 11（Chameleon）
**Time:** ~120 minutes | **时间:** ~120 分钟

>  **【前置】**学本节前 Lütfen önce bil:Fase 12·11(Chameleon 早期融合 token)、Fase 8·01-03(扩散模型基础,对照学习)、Fase 7(自归下回 टोकन 训练)。Emu3 =Chameleon 思路 + 更好的VQ 分词器 + 大规模训练。
>  **【类比】**扩散模型 vs Emu3 = "画油画" vs "拼乐高"。扩散 = 噪音开始一步精修(连续去噪),每步都重新画整张图;Emu3 = 一个标记 往下拼拼;;离散乐高块),图片拼出序列──乐高看粗,但块足够小+种类足够多时也能拼出逼真画面,而且和文本生成同一套机制(都是下图片的标记)。
> 🤔 **【困惑】**S: 既然 Emu3 这么强,为什么稳定扩散 仍然主流? 推理成本!扩散模型 50 步去噪就能出图,Emu3 自回归需要产生上千代币才能出图,慢 20 倍――生成质量 Emu3 接近 SDXL 但是推理慢,所以生产仍然偏爱扩散――统一一生成的价值在"一个模型干所有事",不是"每个任务都最快"――

## Öğrenme hedefleri

- Emu3'ün tek kayıp bir sonraki belirti hedefi, görüntü kalitesi için yayılma gerekli olduğu uzun zamandır kabul edilen varsayıma rağmen neden işe yaradığını açıklayın.
  > 解释为什么Emu3 单一损失的下一代币 目标在长期假设"图像生成必须扩散"的情况下仍然有效──
- 3D video tokenizer'i açıklayın: uzay-zamanlı VQ kod defteri nasıl görünüyor, neden yamalar zaman geçirir.
  > 描述 3D 视频分词器:时空 VQ 码本长什么样、为什么补丁 要跨时间维度──
- Emu3 vs. Stable Diffusion XL ile karşılaştırın (öğrenme hesaplama, sonucu çıkarma maliyeti, kalite tavanı).
  > Emu3 ile Stable Diffusion XL'yi karşılaştırın, eğitim güçindeki farkı, maliyet ve kalite sınırlarını tahmin edin.
- Aynı Emu3 modeli oynayan üç rolü isimlendirin: Emu3-Gen (resim gen), Emu3-Chat (görüş), Emu3-Stage2 (video gen).
  > 列举同一 Emu3 模型扮演的三种角色:Emu3-Gen(图像生成)、Emu3-Chat(感知)、Emu3-Stage2(视频生成)。

## Sorun  sorun arka planı

2024 yılına kadar geleneksel bilgelik: görüntü üretimi yayılmaya ihtiyaç duyar. Dövüş: ayrı görüntü belirtileri ayrıntıları yeniden yapılandırmak için çok fazla bilgi kaybeder ve autoregressive örnekleme binlerce belirti boyunca hata biriktirir. Dall-E 3, Imagen, Midjourney, her biri bir çeşit difüzyon kullanıyor. Chameleon (Düşünme 12.11) bunu küçük ölçekte kısmen reddetti ancak kalitede SDXL ile eşleşmedi.

> 2024 yıl öncesinde bir ortak fikir: görüntü üretimi yayılma ihtiyacı modelilerdir. Sonucunda: ayrılmış görüntü simgesi  kaybı çok fazla bilgi yeniden inşa edilemez ayrıntılar, kendi kendine geri dönüşü örneği binlerce simgesi üzerinde toplanmış hatalar. Staj Distribution、DALL-E 3、Imagen、Midjourney hepsi yayılma biçiminde bir şekilde kullanıyor.

Emu3, argümanın önüne saldırdı. İddia: daha iyi görsel tokenizer + yeterli ölçek + sonraki token kaybı = algılama yapan aynı modelde difüzyon-beating görüntü üretimi.

> Emu3 正面攻击这个论点──声称:更好的视觉分词器 + 足够的规模 + 下一代币 损失 = aynı modelde aşırı yayılmış görüntü üretimi, aynı zamanda 感知也能做──

Bahis yayınlandığında tartışmalıydı. İki yıl sonra, açık kaynaklı tek nesil ailesi (Emu3, Show-o, Janus-Pro, Transfusion) araştırma için varsayılan yoldur; üretim sınır modelleri bazı variantları kullanıyor gibi görünüyor.

> Bu yayın sırasında tartışmalar var. İki yıl sonra, bu çalışma bir çalışma standardı haline geldi.

## Konsepten bir şey.

> **【中文解读】**EMU3 Pure Auto-Return Next Token  Prediction unified multi-modelous understanding and generation── görüntüler token 序列 olarak ayrıştırıldı 序列 sonrasında, model gibi bir proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje proje

> **【拓展：自回归图像生成的挑战】**EMU3'ün saf kendi kendine dönüşüm yöntemi, görüntü üretimi sırasında yayılma modelinden geride kalıyor, çünkü görsel jetonların uzunluğu metinden daha öğrenmek zorlaştırmaktadır.


### Emu3 Tokenizer

Ana bileşen görsel tokenizer. Emu3 bir token başına 8x8 çözünürlük azaltma ile özel IBQ sınıfı tokenizer (Inverse Bottleneck Quantizer, SBER-MoVQGAN ailesi) eğitir. 512x512 bir görüntü 64x64 = 4096 token kod defteri büyüklüğünde 32768 olur.

> 关键成分是视觉分词器──Emu3 训练了自定义的 IBQ 类分词器(逆瓶量化器,SBER-MoVQGAN 家族), her token 8x8 分辨率缩减──一张 512x512 图像变成64x64 = 4096 代币,码本大小 32768──

Bu, Chameleon'un 512x512 başına 1024 tokenden daha büyüktür, ancak her token için daha ucuz (kodu defteri araması, daha basit kodek). Ana metrik: 30,5 dB'de PSNR yeniden inşa edilmesi, Stable Diffusion'ın 32 dB'de sürekli gizli alanıyla rekabetçi.

> Bu, Kameleon'un her bir çekiminden 512x512 图像 1024 个标志(K=8192) Daha büyük, ancak her bir token daha ucuz(更小的码本查找、更简单的编解码器) 

Video için: 3D VQ tokenizer bir uzay-zaman yama (4x4x4 piksel) bir tamsayı kodlar. 8 FPS'de 4s klipi 32 çerçeveye sahiptir; 4x uzay ve 4x zamanlı azaltma ile 256x256'da, token sayısı (256/4) * (256/4) * (32/4) = 64 * 64 * 8 = 32,768 token.

> 对于视频:3D VQ 分词器将时空补丁(4x4x4 像素)编码为整数──4秒片段在 8 FPS 下有 32 ;256x256 分辨率下 4x 空间和 4x 时间缩减,代码数字为 32768──

Tokenizer kalitesi tavan. Emu3'ün katkı kısmen "çok iyi bir tokenizer eğittik".

> 分词器质量是上限──Emu3'ün katkısı kısmen "Biz çok iyi bir分词器 eğitmişiz"──

### Tek Kayıp Eğitim

Emu3 bir hedef kullanır: metin jetonları, 2D görüntü jetonları ve 3D video jetonları arasında paylaşılan bir kelime birikimine bağlı bir sonraki jeton öngörümü.

> Emu3 Using a goal: in common words 预测, covers text token、2D 图像 token 和 3D 视频 token── eğitim sırasında ağırlık ağırlığı belirli faktörlerin ödenmesi için bir ölçüde çarpılır, ancak kayıp işlevi aynı──

Tren, bir karışım üzerinde:
- Resim gen: `<text caption> <image> image_tokens </image>`
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri
- Resim algısı: `<image> image_tokens </image> <question> text_tokens`
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri
- Video Gen: `<text caption> <video> video_tokens </video>`
  Çeviri: video
- Video algısı: Analog.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri
- Tekst: Standart NTP.
  Çöntem: 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0

Model, verilerin dağıtımından görüntü jetonları vs metin jetonları ne zaman yayılacağını öğrenir.`<image>`- Etiket.

> 模型从数据分布中学习何时输出图像代币与文本代币――生成能力来自模型在 `<image>`标签后预测 Görüntü simgesi

### Sınıflandırıcı olmayan yönlendirme ve sıcaklık

Autoregressive görüntü oluşturma, sınıflandırıcısız rehberlik (CFG) ile sonuçlandırma sırasında çok daha iyi hale gelir. Emu3 onu kullanır: iki kez, bir kez tam başlık ile, bir kez boş başlık ile oluşturun, logitleri rehberlik ağırlığıyla karıştırın (tipik 3.0-7.0). Bu aynı CFG numara yayılması kullanımıdır, autoregressive ayarına ödünç alınmıştır.

> Kendi dönüşümlü görüntü üretimi düşünce sırasında kullanılırken kullanılırken kullanılırken kullanılırken kullanılırken kullanılırken kullanılırken kullanılırken kullanılırken kullanılırken kullanılırken kullanılırken kullanılırken kullanılırken kullanılırken kullanılırken kullanılırken kullanılırken kullanılırken kullanılırken kullanılırken kullanılırken kullanılırken kullanılırken kullanılırken kullanılırken kullanılırken kullanılırken kullanılırken kullanılırken kullanılırken kullanılırken kullanılırken kullanılırken kullanılırken kullanılırken kullanılırken kullanılırken kullanılırken kullanılırken kullanılırken kullanılırken kullanılırken kullanılırken kullanılırken kullanılırken kullanılırken kullanılırken kullanılırken kullanılırken kullanılırken kullanılırken kullanılırken kullanılırken kullanılırken kullanılırken kullanılırken kullanılırken kullanılırken kullanılırken kullanılırken kullanılırken kullanılırken kullanılırken kullanılırken kullanılırken kullanılırken kullanılırken kullanılırken kullanılırken kullanılırken kullanılırken kullanılırken kullanılır.

Sıcaklık önemli: çok yüksek, eserler; çok düşük, mod çöküşü.

> 温度 çok önemlidir: 太高会有伪影; 太低会导致模式崩──Emu3 推的温度是感知用 1.0,图像生成用 0.8──

### Üç rol, bir model.

Emu3 gemileri, üç işlevsel olarak farklı API'de, ancak bir temel ağırlık seti olarak:

> Emu3 以三个功能不同 API 发货,但使用相同权重:

- Emu3-Gen. Resim oluşturma. Giriş metni, çıkış resim belirtileri.
  Çeviri:Emu3-Gen──图像生成──输入文本,输出图像代码──
- Emu3-Chat. VQA ve başlıklama. Giriş görüntü (token), çıkış metni.
  Çeviri:Emu3-Chat──视觉问答和描述──输入图像(token),输出文本──
- Emu3-Stage2. Video oluşturma ve video VQA. Giriş metni veya video, çıkış metni veya video.
  Çinçe Çevirimiçi:Emu3-Stage2── video üretim ve video sorusu──输入文本或视频,输出文本或视频──

Görev özel başlık yok, farklı istek şablonları, aynı kontrol noktası.

> 没有任务特定头──只是不同的提示模板──同一个检查点──

### Önyargılar

Emu3 makalesinden (Ecuba 2024):

> Emu3 论文(2024年 9月):

- Resim üretimi: MJHQ-30K FID (5.4 vs 5.6) üzerinde SDXL'i yener, GenEval genel olarak (0.54 vs 0.55  istatistiksel denge) ve Deep-Eval'in bileşik eşdeğerini.
  Çine çevirisi:图像生成: 在 MJHQ-30K FID 上击败 SDXL(5.4 vs 5.6),GenEval 总体(0.54 vs 0.55统计上打平)
- Görüntü algısı: VQAv2'de LLaVA-1.6'u (75.1 vs. 72.4) yener ve MMMU'da yaklaşık olarak eşleşir.
  Çinçe Çevirimiçi: 图像感知: 在 VQAv2 上击败 LLaVA-1.6(75.1 vs 72.4), 在 MMMU 上大致持平──
- Video üretimi: 4 saniyelik video kalitesi, Sora çağının kamuoyuna göre standartlaştırılmış modelleri ile rekabetçi FVD'de.
  Çinçe Çevirimiçi: Video Generi:4 秒片段质量 Sora 时代的公开基准模型竞争力相当──

Sayılar her zaman kazanmıyor  Emu3 burada bir noktayı bir noktaya karşı tutar  ama "sonraki jeton tahmininin tek ihtiyacı olan şey" iddiası, modaliteler arasında savunulabilir.

> Sayılar her zaman kazanmaz. Bir noktada diğer noktada değişir. Ama "Sonraki işaret, tahminin senin ihtiyacın olan her şey" ifadesinin tüm biçimlerde kalıcıdır.

### Hesaplama maliyeti

Emu3 yaklaşık 300 milyar multimodal jeton üzerinde 7B parametre modeli ile eğitilmiştir. GPU saatleri Llama-2-7B öncesi eğitimiyle (A100 sınıfı silikon üzerinde 2k-4k GPU yılları) yaklaşık olarak karşılaştırılabilir. Stable Diffusion 3 gibi difüzyon modelleri benzer bütçelerde trenler ancak ayrı metin kodlayıcılara ve daha karmaşık boru hattlarına ihtiyaç duyar.

> Emu3 yaklaşık 3000 milyar fazla modem token üzerinde 70 milyar parametre modeli eğitimi kullanıyor. GPU küçük sayı büyük ölçüde Llama-2-7B 预训相当(A100 sınıfı 片上 2k-4k GPU 年) ⋅ Stabil Diffusion 3 等 扩散模型在类似预算下训练,但需要独立文本编码器和更复杂的管线──

Sonuç olarak, Emu3 görüntü başına SDXL'den daha yavaş: 30 tok/s'de 4096 görüntü jetonu, 512x512 görüntü başına ~ 2 dakika, SDXL için 2-5 saniye. Speküel çözme ve KV-cache optimizasyonu boşluğu daraltır, ancak kapatmaz. Autoregressive görüntü gen hesaplama ağırdır; bu daimi pazarlama.

> 推理时,Emu3 张图像比 SDXL 慢:4096 个图像代币 以 30 tok/s 生成,每张 512x512 图像约2分钟,而 SDXL只需2-5秒――投机解码和KV 缓存优化缩小了差距但没有关闭它――自归图像生成密度计算;这是持续存在的权衡――

### Neden önemli?

Emu3'ün derin katkı konseptaldir. Eğer bir sonraki belirti tahmininin görüntü üretimi üzerinde yayılma ile eşleşmesi için ölçekleri varsa, tek bir model yolu (bir kayb, bir omurgan, herhangi bir modalik) uygulanabilirdir. Gelecek modeller ayrı metin kodlayıcılarına, ayrı yayılma programcılarına, ayrı VAE'lere ihtiyaç duymaz.

> Emu3'ün derin katkıları kavramsaldır. Eğer bir token 预测能扩展到在图像生成上匹敌扩散,统一模型路径 ((一个损失,一个骨干,任何模态) 是可行的──未来模型不需要独立文编码器、独立扩散调度器、独立 VAE──一个变压器,每个模态一个分词器,然后扩展规模──

Show-o, Janus-Pro ve InternVL-U, tümü bu tez üzerinde inşa ediyor veya meydan okuyor. Çin laboratuvarları (BAAI, DeepSeek) 2025 yılına kadar ABD laboratuvarlarından daha agresif bir şekilde bu yönde yayın yapıyor.

> Show-o、Janus-Pro 和 InternVL-U bu noktada kurulmuştur veya bu noktada meydan okudu.


> **【拓展：EMU3 的统一训练策略】**EMU3'ün temel katkıları, saf kendiliğinden geri dönüş yönteminin aynı anda anlaşılmasını ve üretimini sağlayabileceğini kanıtlamakta.


## Kullanın.
```figure
l5-emu3-next-token
```

## Kullan

`code/main.py`İki oyuncak parça yapar:

> `code/main.py`İki oyuncak bileşeni inşa ettin:

- 2D vs 3D VQ tokenizer sayım hesaplayıcı: verilen ( çözünürlük, yama, clip_length, FPS), hesaplama simgelerinin görüntü vs. video sayıları.
  ÇINCE TRANSLATION: 2D vs 3D VQ 分词器计数计算器:给定(分辨率、补丁、片段长度、FPS),计算图像与视频的代号 数――
- Sınıflandırıcı olmayan sıcaklık yönlendirici bir autoregressive image-token sampleler.
  Çinçe çevirisi:带温度和无分类器引导的自归图像代号采样器

CFG uygulaması Emu3'ün reçetesine  şartlı ve koşulsuz logitleri bir rehberlik ağırlığı ile karıştırır.

> CFG                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            

## Gönderin.

Bu ders bize çok yararlı .`outputs/skill-token-gen-cost-analyzer.md`. Bir jenerasyon ürün özellikini (resim veya video, hedef çözünürlük, kalite seviyesini, gecikme bütçesini) göz önüne alarak, token sayısını, sonuç maliyetini hesaplar ve Emu3 ailesini yayılma karşısında seçer.

> 本课产 出 `outputs/skill-token-gen-cost-analyzer.md`◊ belirlenmiş üretim ürün kuralları, hedef çözünürlük, kalite derecesi, gecikme bütçesi, belirtilen miktarı hesaplar, tahmin maliyetlerini hesaplar ve Emu3 serisi ile yayılma modeli arasında seçim yapar.

## Egzersizler.

1. Emu3 512x512 görüntü başına 4096 token üretir. 8x8 azaltımıyla. 1024x1024 ve 2048x2048 için eşdeğer hesaplayın.
   Çinçe Çevirimi:Emu3 在 8x8 缩减下每张 512x512 图像产生 4096 个代币──计算 1024x1024 和 2048x2048 的等效值──推理延迟会怎样?

2. Emu3'ü video tokenizer'deki 3.3 bölümde okuyun. 3D VQ yama şeklini ve neden 8x8x1 değil 4x4x4 olduğunu açıklayın.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri Çeviri Çeviri: Çeviri Çeviri: Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Ç Ç Ç Çeviri Çeviri Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç

3. Sınıflandırıcısız rehberlik ağırlığı 5.0 vs 3.0: hangi görsel etki? Matematikleri izleyin `code/main.py`- Evet .
   Çin Çeviri:                                                                                                                                                                                                                                                            `code/main.py`Orta matematik.

4. Emu3-7B için FLOP'leri hesaplayın ve Stable Diffusion 3 ile karşılaştırın.
   Çinçe Çevirim: hesap Emu3-7B , 300B token 上的训练 FLOPs,并与稳定扩散3比较──哪个训练更贵?

5. Emu3 FID'de SDXL'yi yener, ancak VQAv2 vs. uzmanlaşmış VLM'lerde değil.
   Çinçe Çevirisi:Emu3 FID'de SDXL'yi yendi, ama VQAv2'de profesyonel VLM gibi değildi.

## Anahtar Terimler

| Term | What people say | What it actually means | 中文含义 | 中文释义 |
|------|-----------------|------------------------|---------|
| Next-token prediction | "NTP" | Standard autoregressive loss: predict token[i+1] given token[0..i]; works for every modality when tokenized | 标准自回归损失：给定 token[0..i] 预测 token[i+1]；分词后适用于所有模态 |
| IBQ tokenizer | "Inverse bottleneck quantizer" | A class of VQ-VAE with larger codebooks (32768+) and better reconstruction than Chameleon's | 一类更大码本（32768+）和更好重建质量的 VQ-VAE |
| 3D VQ | "Spatiotemporal quantizer" | Codebook indexed by (time, row, col); one token covers a 4x4x4 pixel cube | 按（时间、行、列）索引的码本；一个 token 覆盖 4x4x4 像素立方体 |
| Classifier-free guidance | "CFG" | Mix conditional and unconditional logits with weight gamma; boosts image quality at inference | 用权重 gamma 混合条件和无条件 logits；提升推理图像质量 |
| Unified vocabulary | "Shared tokens" | Text + image + video all draw from the same integer space; model predicts whichever modality comes next | 文本+图像+视频共享同一整数空间；模型预测下一个模态 |
| MJHQ-30K | "Image gen benchmark" | Midjourney-quality benchmark with 30k prompts; Emu3 reports FID here | 30k 提示的 Midjourney 质量基准；Emu3 报告 FID |

## Daha fazla okumak

- [Wang et al. — Emu3: Next-Token Prediction is All You Need (arXiv:2409.18869)](https://arxiv.org/abs/2409.18869)
  Çeviri:Emu3 论文下一符号 预测就是你需要的一切──
- [Sun et al. — Emu: Generative Pretraining in Multimodality (arXiv:2307.05222)](https://arxiv.org/abs/2307.05222)
  Çinçe Çevirimi:Emu 多模态生成预训练。
- [Liu et al. — LWM (arXiv:2402.08268)](https://arxiv.org/abs/2402.08268)
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri
- [Yu et al. — MAGVIT-v2 (arXiv:2310.05737)](https://arxiv.org/abs/2310.05737)
  Çeviri:MGVIT-v2
- [Tian et al. — VAR (arXiv:2404.02905)](https://arxiv.org/abs/2404.02905)
  Çeviri:VAR 视觉自归模型──
