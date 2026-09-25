# Flamingo ve Gated Cross-Attention birkaç VLM için .

> DeepMind's Flamingo (2022) herkesten önce iki şey yaptı. Tek bir modelin, resimlerin, videoların ve metinlerin kendiliğinden birbirine karışmış dizilerini işleyebileceğini gösterdi. Ve VLM'lerin bağlamda öğrendiğini gösterdi  üç örnek (resim, başlık) çiftle birkaç çekim sorgulaması vererek ve model herhangi bir gradient adım olmadan yeni bir resim başlıklı. Mekanizm: donmuş LLM'nin mevcut katmanları arasında yerleştirilen kapalı çapraz dikkat katmanları, sıfırdan başlayan öğrenilmiş bir tanh kapısı ile LLM'nin metin yeteneği başlangıçta korunmaktadır. Bu ders Flamingo'nun Perceiver resampler ve kapalı çapraz dikkat mimarisini izler. Gemini'nin birbirine karışmış girişlerinin ve Idefics2'nin görsel jetonlarının ataları.

> **【中文解读】**Flamingo  İlk kez uygulama grafik                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       

> **【拓展：Flamingo→Gemini交织输入】**Flamingo'nun resim yapısı işleme modeli, Gemini 交织输入和 Idefics2 视觉代币'in orijinal biçimidir.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, gated cross-attention + Perceiver resampler demo) | **语言:** Python（标准库，门控交叉注意力 + Perceiver resampler 演示）
**Prerequisites:** Phase 12 · 03 (BLIP-2 Q-Former) | **前置知识:** Phase 12 · 03（BLIP-2 Q-Former）
**Time:** ~120 minutes | **时间:** ~120 分钟

>  **【前置】**学本节前 Lütfen önce öğrenin:Bölüm 12·03(BLIP-2 Q-Former,理解交叉注意力和可学习查询);Bölüm 7(Transformer残差结构);Bölüm 11·05(Kontext İçin Öğrenme 概念)。Flamingo 和 BLIP-2 最大不同:BLIP-2 在 LLM 输入端桥接一次;Flamingo 在 LLM 每隔几层插入门控制层──
>  **【类比】**Flamingo'nun kapı kontrolü çapraz dikkat = "外科手术式の微创改造"。BLIP-2 = "LLM'de büyük kapı açıp bir çevirmen"(输入端桥接一次);Flamingo = "LLM'nin her katındaki ofisler içinde bir pencere yerleştir"( her 4 katı kapı kontrolü çapraz dikkat)。门控初始为0 = 窗一开始关闭,模型行为与原始LLM 完全一样;训练慢慢开窗 = 视觉信息逐渐注入但不会破坏原始文本能力──

## Öğrenme hedefleri

- Kapalı çapraz dikkatin, donmuş bir LLM'nin tanh(gate) = 0 üzerinden başlangıçta metin yeteneğini nasıl koruduğunu açıklayın.
  Çinçe Çevirimi: açıklama 门控交叉注意力如何通过 tanh(gate) = 0 在初始化时保持结 LLM 的文本能力──
- Bir Perceiver resampler üzerinden yürüyün: N görüntü yamaları → K sabit "latent" sorular aracılığıyla çapraz dikkat.
  Çıktı. Çıktı. Çıktı. Çıktı. Çıktı. Çıktı. Çıktı. Çıktı. Çıktı. Çıktı. Çıktı. Çıktı. Çıktı. Çıktı. Çıktı. Çıktı. Çıktı. Çıktı. Çıktı. Çıktı. Çıktı. Çıktı. Çıktı. Çıktı. Çıktı. Çıktı. Çıktı. Çıktı. Çıktı. Çıktı. Çıktı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Ç. Çı
- Flamingo'nun, görüntü yerleştirilmesine saygı gösteren sebep maskeli olarak birbirine karışmış görüntü-metin dizilerini nasıl ele aldığını açıklayın.
  Çinçe Çevirimi: Flamingo'nun resimleri nasıl değerlendirilir
- Birkaç çekimden oluşan bir multimodal istek yapısını yeniden üretin (3 resim başlık örneği ve ardından bir sorgu görüntüsü).
  Çinçe Çevirimi:复现少样本多模态提示结构(3 个图文示例后跟一个查询图像) 』

## Sorunlar. Sorunlar.

BLIP-2, 32 görsel tokeni dondurulmuş bir LLM'nin giriş katmanına ekler. Tek istek için bir görüntü için çalışır. Ama ne olacak eğer "böyle bir resim A, başlıklı olsun; işte bir resim B, başlıklı olsun; şimdi bir resim C, başlıklı olsun" gibi metinlerle birbirine karışmış *çok* resimleri beslemek istiyorsanız? LLM'nin kendine özgü dikkatini tek bir akışta görüntü simgelerini ve metin simgelerini ele alması gerekecek ve hangi pozisyonların hangi görüntülere katılabileceği sorusu kargaşa olur.

> BLIP-2 32 görsel simgeyi LLM'nin giriş katmanına uygulayacaktır. Ancak eğer "Bu A'nın resmini anlatın, bunu anlatın; Bu B'nin resmini anlatın; Bu şimdi C'nin resmini anlatın" gibi metinlerle bağlantılı bir* çok* resim için kullanılırsa, LLM'nin kendi kendine dikkat etmesi tek bir akışta görüntü simgesini ve metin simgesini işleme ihtiyacı vardır.

Flamingo'nun cevabı: LLM'nin giriş akışını hiç değiştirmeyin. Mevcut LLM blokları arasında ek çapraz dikkat katmanları ekleyin. Metin işaretleri her zamanki gibi LLM'nin sebepli öz dikkatini akıttır. LLM blokları arasında, metin tokenleri de yeni kapalı bir katman üzerinden görüntü özelliklerine karşı karşıya gelir. Geçit (sıfır olarak başlangıç yapılır) sıfır adımda yeni katmanların hiç çalışmadığını gösterir. Eğitim ilerledikçe kapı açılır ve görsel bilgi akmaya başlar.

> Flamingo'nun cevabı: LLM'nin giriş akışını tamamen değiştirmez. mevcut LLM blokları arasında ek ekstra geçiş dikkat katmanı yerleştirilmektedir.

Flamingo ikinci soruya cevap verdi: bir istekle değişken bir görüntü sayısını (0, 1 veya çok) nasıl işletiyorsunuz? Bir Perceiver resampler  herhangi bir sayıda yama almayı ve sabit bir sayıda görsel gizli jeton ürettiği küçük çapraz dikkat modülü. LLM çapraz dikkat katmanı, istekle kaç görüntü varsa da aynı şekli görür.

> Flamingo 回答的第二个问题:如何处理每个提示中可变数量的图像(0、1或多张)?Perceiver resampler一个小型交叉注意力模块,任意数量的补丁接收并产生固定数量的视觉潜在代币──无论提示中多少图像,LLM 交叉注意力层看到的形状都相同──

## Konsepten bir şey.

> **【中文解读】**Flamingo(DeepMind) giriş kontrolü geçici dikkat(Gated Cross-Attention), 结 LLM katmanları arasında ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ 

> **【拓展：Flamingo 的高效适配】**Flamingo  sadece %1                                                                                                                                                                                                                                                            


> **【拓展：门控机制的数学原理】**门控交叉注意的门控值初始化为0, yani eğitim başladığında görsel bilgi tamamen LLM'ye akmayacaktır. 门控随着训练进行,门控逐渐开放了.


### Dondurulmuş LLM

Flamingo, dondurulmuş bir Chinchilla 70B LLM ile başlar. Tüm 70B ağırlıkları dokunmamıştır.

> Flamingo'nun Chinchilla 70B LLM'si başlatıldı.

### Algılayıcı resampler

ViT, isteklendirme içindeki her görüntü için N patch tokenleri üretir. Perceiver resamplerinde K sabit öğrenilebilir latenlar vardır (Flamingo K=64 kullanır).

> 对于提示中的每张图像,ViT 产生 N 个补丁符号──Perceiver resampler has K 个固定的可学习潜在向量(Flamingo 使用 K=64)──每个 resampler 块 has two two two steps:

> 🤔 **【困惑】**S: Farkçı resampler 和 BLIP-2'nin Q-Former'ı var mı?A: 思想 hampir identic(patch 提取信息) öğrenilme sorusu), ama Flamingo'nun Farkçı resampler sadece görsel özellikler sıkıştırmak、 kaybı karşısında katılmak; Q-Former transformör 结构且有 ITC/ITM/ITG 三个损失──

1. Çelişkili dikkat: K latentleri N patch tokens'e karşı katılır (Q latentlerden, K/V patchlerden).
   Çıktı. Çıktı. Çıktı. Çıktı. Çıktı. Çıktı. Çıktı. Çıktı. Çıktı. Çıktı. Çıktı. Çıktı. Çıktı. Çıktı. Çıktı. Çıktı. Çıktı. Çıktı. Çıktı. Çıktı. Çıktı. Çıktı. Çıktı. Çıktı. Çıktı. Çıktı. Çıktı. Çıktı. Çıktı. Çıktı. Çıktı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı Çı Çı. Çı. Çı Çı. Çı Çı Çı Çı Çı Çı Çı Çı Çı Çı Çı Çı Çı Çı Çı Çı Çı Çı Çı Çı
2. Kendine dikkat + FFN gizlilerde.
   Çinçe Çevirimi: potansiyel 量内部的自注意力 + FFN。

6 resampler blokundan sonra, ViT'nin ürettiği kaç yama olursa olsun, çıkış K=64 görsel token, 64 resampler tokeni olarak çıkar.

> 6 resampler bloktan sonra, çıkış K=64 个维度为 1024 视频代币, ne olursa olsun ViT 产生多少补丁;; 224x224 图像;; 196 补丁) 图像; 480x480 图像;; 900 补丁) 都输出为 64 个 resampler 图标;;

Video için resampler zamanlı olarak uygulanır: her çerçevenin yamaları 64 laten üretir ve zamanlı konum kodlaması modeli t=0 ile t=N arasında ayırt etmesine izin verir. Tam video T * 64 görsel jetonlar haline gelir.

> 对于视频,resampler 按时间维度应用:每的补丁 产生 64 潜在向量,时间位置编码让模型区分 t=0 和 t=N──完整视频变成T * 64 视频代币──

### Çaplaklı dikkat

Dondurulmuş LLM'nin her M katmanının arasına (Flamingo M=4 kullanıyor), yeni kapalı çapraz dikkat blokunu yerleştirin:

> Bu nedenle, bu programın tüm yönlerini ve yönlerini değiştirmek için, bir yeni giriş yapın.

```
x_after_llm_block = llm_block(x_before)
cross = cross_attn(x_after, resampler_output)
gated = tanh(alpha) * cross + x_after
x_before_next_block = gated
```

- `alpha`0'ya initialize edilen öğrenilebilir bir skalar.
  Çeviri:`alpha`Bu, öğrenilme yeteneği, başlangıçta sıfır.
- `tanh(0) = 0`, yani init'te kapalı dal sıfır katkı sağlar.
  Çeviri:`tanh(0) = 0`Bu yüzden başlangıç zamanında kontrol bölümü katkı sıfır.
- - Evet .`alpha`sıfırdan uzaklaşırsa, dikkat katkı sorunsuz bir şekilde büyür.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`alpha`远离零,交叉注意力贡献平滑增长──
- Geri kalan bağlantı, tamamen açık bir kapının bile LLM'nin metin temsilini üstü yazmaması anlamına gelir; sadece yukarıda görsel bilgi eklenir.
  Çinçe Çevirimiçi:残差连接 (残差连接) kapsamlı bir şekilde açılmış olsa bile, LLM'nin metnini kapsamıyor demektir; sadece üzerinde görsel bilgi ekliyor.

Flamingo'da en önemli tasarım seçeneği bu: görsel kondisyona sahip olmak, başlangıçta eklenir, kapalıdır ve sıfırdır.

> Flamingo'nun en önemli tasarım seçeneği: Görüş koşulları eklenmiş, kontrolü olan, başlangıç olarak sıfırlanmıştır.

> ️ **【易错点】**Özü realizasyon zaman unutma başlangıç alfa=0, direkt随机初始化 → 訓練前几步 LLM 文本能力就会崩塌──原因:未训练的交叉注意力输出是噪音,混入 LLM 内部表示会破坏文本知识──修复:alpha 必须初始化为0,让模型从"完美 LLM"出发,缓慢学习──
>  **【类比】**零初始化门控 = "新员工入职模式"──新员工 (新员工) 视觉层) 第一周只观察、不说话(gate=0);熟悉业务后逐渐发言(gate 慢慢打开)──直接让新员工主导决策(gate≠0初始化) 会扰乱团队原奏(破坏 LLM 文本能力)──

### Çelişkili girişler için maskeli çapraz dikkat

"<image A> caption A <image B> caption B <image C> ?" gibi bir istekle, her metin simgesi sırada sadece ondan önce gelen resimleri görmelidir.`t`Sadece görüntü indeksini oluşturan resampler tokenlerine katılır `i < i_t`nerede`i_t`konumdan önce en son görüntüdür `t`"Sadece son önceki görüntüyü görür" veya "sonraki tüm görüntüleri görür" her ikisi de geçerli seçimlerdir; Flamingo ilkini seçti.

> Bu nedenle, bu çizgiyi oluşturan bir metin simgesi olarak, bir metin simgesi olarak, bir metin simgesi olarak, bir metin simgesi olarak, bir metin simgesi olarak, bir metin simgesi olarak, bir metin simgesi olarak, bir metin simgesi olarak, bir metin simgesi olarak, bir metin simgesi olarak, bir metin simgesi olarak, bir metin simgesi olarak, bir metin simgesi olarak, bir metin simgesi olarak, bir metin simgesi olarak, bir metin olarak, bir metin olarak, bir metin olarak, bir metin olarak, bir metin olarak, bir metin olarak, bir metin olarak, bir metin olarak, bir metin olarak, bir metin olarak, bir metin olarak, bir metin olarak, bir metin olarak, bir metin olarak, bir metin olarak, bir metin olarak, bir metin olarak, bir metin olarak, bir metin olarak, bir metin olarak, bir metin olarak, bir metin olarak, bir metin olarak, bir metin olarak, bir metin olarak, bir metin olarak, bir metin olarak, bir metin olarak, bir metin olarak, bir metin olarak, bir metin olarak, bir metin olarak, bir metin olarak, bir metin olarak, bir metin olarak, bir metin olarak, bir metin olarak, bir metin olarak, bir metin olarak, bir metin olarak, bir metin olarak, bir metin olarak, bir metin olarak, bir metin olarak, bir metin olarak, bir metin olarak, bir metin olarak, bir metin olarak, bir metin olarak, bir metin olarak, bir metin olarak, bir metin olarak, bir metin olarak, bir metin olarak, bir metin olarak, bir metin olarak, bir metin olarak, bir metin olarak, bir metin olarak, bir metin olarak, bir metin olarak, bir metin olarak, bir metin olarak, bir metin olarak, metin olarak, bir metin olarak, bir metin olarak, metin olarak, metin olarak, metin olarak, metin olarak, metin olarak, metin olarak, metin olarak, metin olarak, metin olarak, metin olarak, metin olarak, metin olarak, metin olarak, metin olarak, metin olarak, metin`t`Yazı simgesi sadece resim göstergesini izle`i < i_t`Fotoğraf resampler simgesi, içinde `i_t`Yerinde`t`之前最近的图像──"Only look at the latest image" veya "See all previous images" hepsi geçerli seçimdir; Flamingo 选择了前者──

### Konekst içi az çekimli öğrenme

Flamingo'nun bir mesajı şöyle görünüyor:

> Flamingo 提示 şöyle görünüyor:

```
<image1> A photo of a cat. <image2> A photo of a dog. <image3> A photo of a
```

Model tamamlama kalıbını görür ve "kuş" (veya görüntü 3 gösterdiği her neyse) çıkışları yapar. Gradient adımları yoktur. Dondurulmuş LLM'nin bağlam içi öğrenme yeteneği kapalı çapraz dikkatin üzerinden taşır.

> Bu, makaleyi oluşturan önemli bir noktadır ve bunun önemli bir nedeni de budur.

> 🤔 **【困惑】**S: Neden Flamingo 能在背景学习而 BLIP-2 不能?A: Flamingo LLM'de Her 4 aşama içine video bilgileri,LLM 内部的视频信息注入中文学习的️在阶段11·05学习过) 仍完整工作;BLIP-2 32 视频代码 直接拼到即时前面,LLM 它们当普通代码 处理,但训练目标里没有显式的少数射击模式,所以能力弱――

### Eğitim verileri

Flamingo üç veri kümesi üzerine eğitilmiştir:

> Flamingo üç veri kitlesinde eğitim:

1. MultiModal MassiveWeb (M3W): 43M web sayfası, birbirine karışmış görüntüler ve metinlerle okuma sırasını yeniden yapılandırır.
   Çinçe Çevirimiçi:多模态 MassiveWeb(M3W) 43 milyon sayfa içeren 交织图像和文本的网页,重建阅读顺序──
2. Resim-Messim Çiftleri (ALIGN + LTIP): 4.4B Çiftler.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çev: Çev: Çeviri: Çev: Çev: Çev: Çev: Çev: Çev: Çev: Çev Çev: Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Ç Ç Ç Ç Ç Ç Ç Ç Ç Çev Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç
3. Video-Text Çiftleri (VTP): 27M kısa video klipi.
   Çin Çeviri: Video-文本对(VTP)

OBELICS (2023), Idefics, Idefics2 ve en açık "Flamingo benzeri" modellerin eğitildiği birbirine yapışmış web corpusunun açık bir çoğaltmasıdır.

> OBELICS(2023) ise, "Flamingo sınıfı" modelinin çoğunun üzerinde eğitimlenmesi,

### OpenFlamingo ve Otter

OpenFlamingo (2023) açık yeniden üretimdir. Arsitektur aynı (Perceiver resampler + donmuş LLaMA veya MPT'de kapalı çapraz dikkat). 3B, 4B, 9B'deki kontrol noktaları. Kalite daha küçük taban LLM ve daha az veri nedeniyle Flamingo'nun geride kalır.

> OpenFlamingo(2023) is open复现──架构相同(Perceiver resampler + 结 LLaMA veya MPT 上的门控交叉注意力)──3B、4B、9B 检查点──由于基础 LLM 更小和数据更少,质量落后于 Flamingo──

Otter (2023) OpenFlamingo'yu MIMIC-IT'de (mültimodaal talimatların bir veri kümesi) talimat ayarlaması ile inşa eder.

> Otter(2023) OpenFlamingo  temelinde MIMIC-IT (MIMIC-IT) ile talimatları küçültmek için, kanıtlama kontrolü için de dikkatli olmak için uygulanabilir.

### Soyları

- Idefics / Idefics2 / Idefics3: Hugging Face'ın kapalı çapraz dikkat soyundan, giderek daha basit (Idefics2 uyarlayıcı birleştirme ile doğrudan yama tokenlerinin lehine resampler düşürdü).
  Çeviri:İdefics / Idefics2 / Idefics3:Hugging Face'ın门控交叉注意力谱系,逐步简化(Idefics2 去掉了 resampler,改用自适应池化的直接补丁代币)
- Flamingo-Chameleon geçimi: 2024 yılına kadar birçok ekip erken birleştirmeye (Düşünme 12.11) geçti; omurgan donması gerektiğinde Flamingo tarzı kapalı çapraz dikkat üretiminde kalıyor.
  Çince çevirisi: Flamingo to Chameleon'ın geçişi: 2024 yılına kadar birçok takım erken birleşmeye yöneldi.
- İkizlerin birbirine karışmış girişleri: kavramsal olarak Flamingo'nun birbirine karışmış biçim esnekliğini miras alır, ancak tam mekanizma mülkiyetlidir.
  Çin dili:Gemini'nin 交织输入:概念上继承了 Flamingo'nun 交织形式灵活性,尽管具体机制是专有的──

### BLIP-2 ile karşılaştırma

| | BLIP-2 | Flamingo |
|---|---|---|
| / | BLIP-2 | Flamingo |
| Visual bridge | Q-Former once at input | Gated cross-attention at every M layers |
| 视觉桥接 | 输入层一次 Q-Former | 每 M 层一次门控交叉注意力 |
| Visual tokens | 32 per image | 64 per image per cross-attn layer |
| 视觉 token | 每图 32 个 | 每个交叉注意力层每图 64 个 |
| Frozen LLM | Yes | Yes |
| 冻结 LLM | 是 | 是 |
| Few-shot in-context | Weak | Strong — the paper's centerpiece |
| 少样本上下文学习 | 弱 | 强——论文的核心亮点 |
| Interleaved inputs | No native support | Yes, the design target |
| 交织输入 | 无原生支持 | 是，设计目标 |
| Training data | 130M pairs | 1.3B pairs + 43M interleaved pages |
| 训练数据 | 1.3 亿对 | 13 亿对 + 4300 万交织网页 |
| Parameter count | 188M trained | ~10B trained (cross-attn layers) |
| 参数量 | 训练 1.88 亿 | 训练约 100 亿（交叉注意力层） |
| Compute | Days on 8 A100s | Weeks on thousands of TPUv4 |
| 计算量 | 8 块 A100 数天 | 数千块 TPUv4 数周 |

Bütçeye göre tek görüntü VQA için BLIP-2'yi seçin.

> 预算有限的单图像 VQA 选 BLIP-2──交织、少样本或多图像推理选 Flamingo/Idefics2──

## Çerçeveyi kullanın.
```figure
cross-attention-fusion
```

## Kullan

`code/main.py`gösterir:

> `code/main.py`Gösterdi:

1. 36 sahte patch token'da 8 öğrenilebilir latente (temiz Python çapraz dikkat) bir Perceiver resampler.
   Çin Çeviri: 36 个假补丁代币的 Perceiver resampler,使用 8 个可学习潜在向量(纯 Python 交叉注意力)
2. Kapalı bir çapraz dikkat adımı ile .`alpha = 0`→ çıkış giriş eşit (LLM değişmedi), o zaman `alpha = 2.0`→ görsel katkıda bulunur.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri Çeviri: Çeviri: Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çov Çov Çov Çov Çov Ç`alpha = 0`→ 输出等于输入(LLM 不变), sonra `alpha = 2.0`→ 视觉贡献混入──
3. "(İs) 1) (metin 1) (İs) 2) (metin 2)" dizisi için 2D dikkat maskasını üreten bir yapışkanlık maskesi yapıştırıcı.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri Çeviri: Çeviri Çeviri: Çeviri: Çeviri Çeviri: Çeviri Çeviri Çeviri Çeviri Çeviri: Çeviri Çeviri Çeviri Çeviri Çeviri Ç Çeviri Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç

## İndirin . Ürünler .

Bu ders bize çok yararlı .`outputs/skill-gated-bridge-diagnostic.md`Açık bir VLM'nin yapılandırmasını (resampler Y/N, çapraz atn frekansı, kapı şeması) göz önüne alındığında, Flamingo soy unsurlarını tanımlar ve dondurma stratejisini açıklar.

> 本课产 出 `outputs/skill-gated-bridge-diagnostic.md`◊ VLM'nin yapılandırmasını belirlemek için, bir örnekleme yapımı yapılması için, bir kontrol sistemi oluşturur.

## Egzersizler.

1. Flamingo-9B'nin görsel parametrelerinin sayısını hesaplayın: 9B LLM + 1.4B kapalı çapraz dikkat katmanları + 64M resampler.
   Çinçe çevirisi: hesaplama Flamingo-9B'nin görsel parametreleri:9B LLM + 14 milyar门控交叉注意力层 + 64 milyon resampler。 eğitimin parametreleri toplam parametrelerin oranını ne kadar kapsar?

2. Kapalı kalanı uygula `y = tanh(alpha) * cross + x`PyTorch'de deneysel olarak bunu göster.`alpha=0`- Evet .`y==x`Tam olarak başlangıçta.
   Çeviri: PyTorch                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      `y = tanh(alpha) * cross + x`❖ Deneyim kanıtları`alpha=0`时  `y==x`- Evet.

3. OpenFlamingo Bölümü 3.2 (arXiv:2308.01390) her sorunun farklı bir görüntü sayısına sahip olduğu bir partide birden fazla görüntüyi nasıl işlediği hakkında bilgi ver.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri Çeviri: Çeviri: Çeviri

4. Flamingo'nun dikkat çekici maskası neden bir metin simgesini, önceki tüm görüntülerden ziyade * sadece en son* önceki görüntüyü kullanmasına izin verir?
   Çinçe Çevirimi: neden Flamingo'nun geçiş dikkatini gizlemek için tek bir resim çekmek için?

5. Konekst içi birkaç çekim: yeni Flamingo variansı için "image → color of main object" adlı 4 örnekle bir istekle oluşturun. Örnek sayısını 0'dan 8'e kadar değiştirip beklenen doğruluk örneğini açıklayın.
   Çineşince: 0 变化到 8 时预期的准确率模式──

## Anahtar Şartlar .

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|------------------------|---------|
| 术语 | 通俗说法 | 实际含义 | |
| Perceiver resampler | "Fixed-latent cross-attention" | Module that produces K fixed tokens from a variable number of input patches | 从可变数量输入 patch 产生 K 个固定 token 的模块 |
| Gated cross-attention | "Tanh-gated bridge" | Residual layer `y = tanh(alpha)*cross + x`, learnable alpha, init 0 | 残差层 `y = tanh(alpha)*cross + x`，可学习 alpha，初始化为 0 |
| Interleaved input | "Mixed sequence" | Prompt format with images and text mixed freely in reading order | 图像和文本按阅读顺序自由混合的提示格式 |
| Frozen LLM | "No LLM gradients" | The text LLM's weights do not update; only resampler + cross-attn layers train | 文本 LLM 权重不更新；仅 resampler + 交叉注意力层训练 |
| Few-shot | "In-context examples" | Give a few (image, answer) pairs in the prompt; model generalizes without finetuning | 在提示中给几个（图像，答案）对；模型无需微调即可泛化 |
| OBELICS | "Interleaved web corpus" | Open dataset of 141M web pages with images and text in reading order | 1.41 亿网页的开放数据集，包含按阅读顺序排列的图像和文本 |
| Chinchilla | "70B frozen base" | Flamingo's frozen text LLM, from DeepMind's Chinchilla paper | Flamingo 的冻结文本 LLM，来自 DeepMind 的 Chinchilla 论文 |
| Gate schedule | "How alpha moves" | The rate at which the cross-attention gate opens during training | 训练过程中交叉注意力门控打开的速率 |
| Cross-attn frequency | "Every M layers" | How often a gated cross-attention block is inserted; Flamingo uses M=4 | 门控交叉注意力块插入的频率；Flamingo 使用 M=4 |
| OpenFlamingo | "Open reproduction" | MosaicML/LAION open checkpoint at 3-9B; architecture-identical to Flamingo | MosaicML/LAION 的 3-9B 开放检查点；架构与 Flamingo 相同 |

## Daha fazla okumak

- [Alayrac et al. — Flamingo (arXiv:2204.14198)](https://arxiv.org/abs/2204.14198)- Orijinal kağıt.
  Çeviri:Flamingo
- [Awadalla et al. — OpenFlamingo (arXiv:2308.01390)](https://arxiv.org/abs/2308.01390) açık üreme.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri
- [Laurençon et al. — OBELICS (arXiv:2306.16527)](https://arxiv.org/abs/2306.16527) birbirine karışmış web corpus.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri
- [Jaegle et al. — Perceiver IO (arXiv:2107.14795)](https://arxiv.org/abs/2107.14795) genel algılayıcı mimarisi.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri
- [Li et al. — Otter (arXiv:2305.03726)](https://arxiv.org/abs/2305.03726) talimat ayarlanmış Flamingo soylu.
  Çeviri:                                                                                                                                                                                                                                                             
- [Laurençon et al. — Idefics2 (arXiv:2405.02246)](https://arxiv.org/abs/2405.02246) Flamingo yaklaşımının modern basitleştirilmesi.
  Çeviri:Flamingo 方法的现代化简化.
