# Genreatif Modeller  Taksonomi ve Tarih  生成模型  分类与历史

> Her görüntü modeli, metin modeli, video modeli ve 3 boyutlu modeli beş kova içinden birine sığar. Yanlış kova seçin ve haftalarca matematikle mücadele edeceksiniz. Doğru olanı seçin ve alanın son on iki yıllık ilerlemesi kafanızda temiz bir şekilde toplanır.

> **【中文解读】**Tüm resim, metin, video ve 3D üretim modelleri beş kategoriye ayrılır: VAE、GAN、 yayılma modeli、 akış modeli ve kendi kendine dönüş modeli。 seçilebilir sınıflar sizi matematikle 斗数周; seçilebilir, son 12 yıllık ilerlemeler aklınızda net bir şekilde toplanmaktadır。

> **【拓展：生成式 AI 的五大路线】**(1) VAE变分自编码器,Stable Diffusion 的编码器;(2) GAN生成对抗网络,StyleGAN 的核心;(3) 扩散模型DDPM/DDIM,当前图像生成主流;(4) 流模型Flow Matching,SD3/FLUX 的新方向;(5) 自归归GPT 模式,VAR 应用于图像──

**Type:** Learn / 学习型
**Languages:** Python
**Prerequisites:** Phase 2 (ML Fundamentals / 机器学习基础), Phase 3 (Deep Learning Core / 深度学习核心), Phase 7 · 14 (Transformers / Transformer)
**Time:** ~45 minutes

## Sorunlar. Sorunlar.

Bir üreticik model bir iş yapar: Bilinmeyen bir dağıtımdan alınan eğitim örnekleri.`p_data(x)`Yüzler, cümleler, MIDI dosyaları, protein yapıları  göz kırpırsanız hepsi aynı sorun.

> Bir model sadece bir şey yapar: Bilinmeyen bir dağılımdan belirlenir.`p_data(x)`İçinden alınan eğitim örneği, çıkış aynı dağılımdaki yeni örneğinden geliyor.

- Sorun şu ki .`p_data`Bu örnekler, milyonlarca boyutlu bir alanda yaşıyor (bir 512x512 RGB görüntü yaklaşık 786k boyutlu), ve bu alanın içinde ince bir çeşitlilik üzerinde oturur ve sadece 10M örnekler vardır.

> Sorun şu:`p_data`Bir 512x512 RGB görüntü yaklaşık 78.60.000 dimensi), örnekler sadece bu alanın zayıf bir akışını oluşturuyor, siz ise sadece 10 milyon örnekler varsınız.

Son on iki yılda beş aile hayatta kaldı. Her aile hangi ödüller verdiğini bilmek, bazı görevlerde neden kazanıyor ve diğerlerinde neden çöküyor, anlatabilir.

> Son 12 yılda beş model aile hayatta kaldı. Her aile neyi anlaşmaya girdiğini öğrenmek, bazı görevlerde neden başarılı olduğunu ve diğer görevlerde neden çöktüğünü anlamak.

> **【中文解读】**生成模型の核心任务: 訓練模型中学習未知分布 p_data(x), sonra üretmek aynı dağılımlı yeni örneklerden görünmek için. 課題は高维空间にあります. 512x512 画像約786K 维) 画像内の稀疏データです.

> **【拓展：从扩散模型到 Flow Matching 的范式转移】**2024-2026 yıllarında en önemli eğilim, yayılma modeliden DDPM'ye akış eşleşmesine doğru akış eşleşmesine doğru ilerlemektir. Akış eşleşmesi daha basit bir eğitimdir.

## Konsepten bir şey.

![Five families of generative models — taxonomy by what they model](../assets/taxonomy.svg)

**1. Explicit density, tractable.**Yazmın .`log p(x)`Bu, bir değerlendirme yapabilmek için bir toplam olarak kullanılır.`p(x) = ∏ p(x_i | x_<i)`Normalleşen akışlar (RealNVP, Glow) oluşturulur.`p(x)`Pro: tam olasılık, temiz eğitim kaybı. Con: autoregressive sonuçlandırma sıralı (uzun sırada yavaş), akışlar dönüştürülebilir mimarlıklara ihtiyaç duyar (memarlık açısından kısıtlayıcı).

> **1. 显式密度，可处理。**- Ben de .`log p(x)`写成可以实际求值的求和──自归归模型(PixelCNN、WaveNet、GPT) 联合分布分解为条件分布的乘积──标准化流(RealNVP、Glow) 简单分布的可逆变换构建 `p(x)`△优点:精确似然,训练损失清晰──缺点:自归推理是顺序的(长序列慢),流需要可逆架构(架构受限)

**2. Explicit density, approximate.**Bağlı`log p(x)`VAE'ler (Kingma 2013) bir varyasyon arka taraflı bir kodlayıcı-dekodör kullanır. Diffusion modelleri (DDPM, Ho 2020) bir denoiser eğitmek ve dolaylı olarak ağırlanmış ELBO'yu optimize eder.

> **2. 显式密度，近似。**Aşağıdan bağlanın`log p(x)`(ELBO)并优化该下界──VAE Kullanım kodlayıcı-解码器和变分后验──扩散模型训练去噪器,隐式优化加权 ELBO──扩散模型是2026年图像、视频和3D 的主导骨干──

**3. Implicit density.**Denetliği tamamen atlayın; bir jeneratör öğrenin `G(z)`Örnekler üreten ve ayrımcı olan bir grup.`D(x)`Bu, gerçekten sahteye anlatır. GAN'lar (Goodfellow 2014). Tahminde hızlı (bir ileri geçiş) ancak eğitim sırasında belirsiz olarak dengesiz. StyleGAN 1/2/3 2026'da bile sabit alan fotorealizmi için sanatın en son durumunu sürdürüyor.

> **3. 隐式密度。** tamamen sıvıtan fazla tahmin; öğrenmek bir jeneratör `G(z)`产生样本,一个判别器 `D(x)`区分真假──GAN 推理快(单次前向传播), fakat eğitim极不稳定──StyleGAN 1/2/3 hatta 2026 yılında sabit alan fotoğraf derecesinde gerçek duyunun en ileri modeli olarak kalmaktadır──

**4. Score-based / continuous-time.**Çubuk yoğunluğunun eğilimi öğrenin `∇_x log p(x)`(score) doğrudan. Song & Ermon (2019) skor eşleşmesi, SDE'ye yayılmayı genelleştirdiğini gösterdi. Akış eşleşmesi (Lipman 2023) 2024-2026 sıcaklığıdır: simülasyonsuz eğitim, daha düz yollar, DDPM'den 4-10 kat daha hızlı örnekleme.

> **4. 基于分数/连续时间。**直接学习对数密度的梯度 (数密度的梯度) 分数函数) Song & Ermon (2019) 证明分数匹配将扩散推广到 SDE──Flow Matching(2023) is 2024-2026 热门:免模拟训练,更直的路径,比DDPM 快 4-10 倍──Stable Diffusion 3、Flux、AudioCraft 2 都使用Flow Matching──

> **【中文解读】**Bölümsel uyum ve akış eşleşmesi, genişleme modelinin genelleşmesi ve gelişmesidir. Bölümsel uyum doğrudan öğrenme logı  yoğunluk derecesi, Akış eşleşmesi, eğitim sürecini daha da basitleştirdi.

**5. Token-based autoregressive over discrete codes.**Yüksek-dim verileri bir VQ-VAE veya kalan kuantitör ile kısa bir ayrı jeton sekansına sıkıştırın, sonra jeton sekansını modellemek için bir Transformer kullanın. Parti, MuseNet, AudioLM, VALL-E, Sora'nın yama jetonçısı hepsinin bunu kullanması. Bu sep 1 artı öğrenilmiş jetonçudur.

> **5. 基于离散 token 的自回归。**VQ-VAE veya残差量化器 ile yüksek düzeyde veri sıkıştırılır ve kısa bir dizi boş token olarak oluşturulur. Transformer ile birlikte, 建模 token 序列──Parti、MuseNet、AudioLM、VALL-E、Sora'nın tokenize cihazı da bu şekilde kullanılır.

## Kısa bir tarih. Kısa bir tarih.

| Year / 年份 | Model / 模型 | Why it mattered / 重要意义 |
|------|-------|-----------------|
| 2013 | VAE (Kingma) | First deep generative model with a usable training loss. / 首个具有可用训练损失的深度生成模型。 |
| 2014 | GAN (Goodfellow) | Implicit density, no likelihood — shockingly sharp samples. / 隐式密度，无需似然——惊人的锐利样本。 |
| 2015 | DRAW, PixelCNN | Sequential image generation. / 顺序图像生成。 |
| 2017 | Glow, RealNVP | Invertible flows; exact likelihood with depth. / 可逆流；深度带来精确似然。 |
| 2017 | Progressive GAN | First megapixel faces. / 首个百万像素人脸。 |
| 2019 | StyleGAN / StyleGAN2 | Photorealistic faces still hard to beat for that one domain. / 照片级真实人脸，该领域至今难以超越。 |
| 2020 | DDPM (Ho) | Diffusion becomes practical. / 扩散模型变得实用。 |
| 2021 | CLIP, DALL-E 1, VQGAN | Text-to-image goes mainstream. / 文本生成图像走向主流。 |
| 2022 | Imagen, Stable Diffusion 1, DALL-E 2 | Latent diffusion + text conditioning = commodity. / 潜在扩散 + 文本条件 = 大众化。 |
| 2022 | ControlNet, LoRA | Fine control over pretrained diffusion. / 对预训练扩散模型的精细控制。 |
| 2023 | SDXL, Midjourney v5, Flow matching | Scale + better training dynamics. / 规模化 + 更好的训练动态。 |
| 2024 | Sora, Stable Diffusion 3, Flux.1 | Video diffusion; flow matching wins. / 视频扩散；Flow Matching 胜出。 |
| 2025 | Veo 2, Kling 1.5, Runway Gen-3, Nano Banana | Production-grade video. / 生产级视频。 |
| 2026 | Consistency + Rectified Flow | One-step sampling from diffusion backbones. / 从扩散骨干实现单步采样。 |

## Beş sorudan oluşan seçim.

Yeni bir üreticik model kağıdı düştüğünde, yöntem bölümünü okumadan önce bu beş soruya cevap verin.

> Yeni bir üretim modeli makalesi yayınlandığında, okuduktan önce bu beş soruya cevap verin.

1. **What is being modeled?**Pikseller, gizli, ayrı simgeler, 3 boyutlu Gaussians, ağlar, dalga şekilleri?
   **正在建模什么？**像素、潜在表示、离散符号、3D 高斯、网格、波形?
2. **Is the density explicit or implicit?**- Yazdılar mı ?`log p(x)`- Ne ?
   **密度是显式还是隐式的？**Yazdılar mı ?`log p(x)`- Ne ?
3. **Sampling: one-shot or iterative?**İteratif, daha yavaş bir sonucu çıkarmak anlamına gelir; tek atış genellikle karşıtlık veya destilli anlamına gelir.
   **采样：单次还是迭代？**代, daha yavaş düşünmeyi,单次 genellikle karşı veya bozulmayı ifade eder.
4. **Conditioning: unconditional, class, text, image, pose?**Bu, kayıp ve mimarlık asfaltlamasını belirler.
   **条件：无条件、类别、文本、图像、姿态？**Bu, kayıp fonksiyon ve yapı çerçevesini belirler.
5. **Evaluation: FID, CLIP score, IS, human preference, task accuracy?**Her biri başarısızlık modlarını biliyor (Düşünme 14).
   **评估：FID、CLIP Score、IS、人类偏好、任务准确率？**Her birinin bilgili bir başarısızlık modeli vardır.

Bu aşamada her ders için bu beşin cevabını tekrar vereceksin.

> Bu aşamada her dersinde bu beş soruya yeniden cevap vereceksin. Sonunda, senin içgüdülerine dönüşecek.

> **【中文解读】**Bu beş soru (Bu beş soru) herhangi bir üretilen modelin genel çerçevesini analiz etmek için bir çerçeve oluşturur. Bu beş soruya sonraki her bölümde tekrar tekrar cevap vererek, yeni makalelerin temel katkılarını ve teknik seçimlerini hızlı bir şekilde anlamanıza yardımcı olabilir.

## Yapın.
```figure
autoencoder-bottleneck
```

## Yapın

Bu dersin kodu hafif bir vizüalizasyon: üç oyuncak yaklaşımı (yürekli yoğunluk, ayrı histogram ve en yakın örnek "GAN-ish" jeneratörü) kullanarak örneklerden 1 boyutlu Gaussian karışımı uygulayın, böylece bir ekranda yazdırabileceğiniz bir sorunda açık vs. içeren yoğunluk arasındaki farkı görebilirsiniz.

> Bu dersin kodu hafif bir derecede görülebilir: üç basit yöntem kullanmak: nükleer yoğunluk tahminleri, ayrıntılı düz çizim, yakın komşu "GAN 风格" üreticisi) bir ekran içinde açık yoğunluk ve gizli yoğunluk arasındaki farkı netleştirmek için örnekler arasında uygun bir boyutlu karışık dağılım sağlar.

Çık .`code/main.py`İki modlu Gaussian karışımından 2000 numune çıkarır ve sonra yazdırır:

> 运行  İşlem`code/main.py`İki peşelik bir karışımdan 2000 numune çıkarıp yazdırır:

```
explicit density (histogram): p(x in [-0.5, 0.5]) ≈ 0.38
approximate density (KDE):     p(x in [-0.5, 0.5]) ≈ 0.41
implicit (nearest-sample gen): 20 new samples printed, no p(x)
```

Dikkat edin: İlk iki bölümde "Bu nokta ne kadar olası?" diye sormak için izin verilir. Üçüncü bölümde "Bu nokta ne kadar olası?" diye sormak için izin verilir.

> Dikkat: İlk iki yöntem "Bu noktada büyük olasılıkla ne var?" diye cevaplayabilir. Üçüncü olarak, mümkün değil.

## Çerçeveyi kullanın.

Hangi aile, 2026'da hangi görev için?

> 2026 yılında hangi aile hangi göreve uygun olacak?

| Task / 任务 | Best family / 最佳家族 | Why / 原因 |
|------|-------------|-----|
| Photoreal faces, narrow domain / 照片级人脸，窄域 | StyleGAN 2/3 | Still sharpest, fastest inference. / 仍然最锐利，推理最快。 |
| General text-to-image / 通用文本生成图像 | Latent diffusion + flow matching | SD3, Flux.1, DALL-E 3. |
| Fast text-to-image / 快速文本生成图像 | Rectified flow + distillation | SDXL-Turbo, SD3-Turbo, LCM. |
| Text-to-video / 文本生成视频 | Diffusion Transformer + flow matching | Sora, Veo 2, Kling. |
| Speech + music / 语音+音乐 | Token-based AR (AudioLM, VALL-E, MusicGen) or flow matching (AudioCraft 2) | Discrete tokens scale cheaply. / 离散 token 扩展成本低。 |
| 3D scenes / 3D 场景 | Gaussian Splatting fit, diffusion prior | 3D-GS for reconstruction, diffusion for novel-view. / 3D-GS 用于重建，扩散用于新视角。 |
| Density estimation (no sampling) / 密度估计（不采样） | Flows | Only family with exact `log p(x)`. / 唯一有精确 `log p(x)` 的家族。 |
| Simulation / physics / 模拟/物理 | Flow matching, score SDE | Straight-line paths, smooth vector fields. / 直线路径，平滑向量场。 |

## İndirin . Ürünler .

- Kaydet .`outputs/skill-model-chooser.md`- Evet .

> 保存为 `outputs/skill-model-chooser.md`- Evet.

Bu beceride görevlerin tanımlanması ve çıkışları bulunur: (1) hangi aileyi kullanmak, (2) üç açık ve üç barındırılmış seçeneklerin sıralamalı bir listesi, (3) dikkat etmeniz gereken olası başarısızlık modu ve (4) hesaplama/zaman bütçesi.

> Bu beceride 接收任务描述,输出:(1) 应使用哪个家族,(2) 三个开源和三个托管选项的排列列表,(3) 应注意的可能失效模式,(4) 计算/时间预算。

## Egzersizler.

1. **Easy / 简单.**Bu beş ürün için, aile ve omurganı belirleyin: ChatGPT görüntü, Midjourney v7, Sora, Runway Gen-3, ElevenLabs. Kanıtlar kamu teknik raporlarından olmalıdır.
   Bu beş ürün için, tanımlama ve yapılandırma: ChatGPT görüntü、Midjourney v7、Sora、Runway Gen-3、ElevenLabs。 kanıtlar açık teknoloji raporundan alınmalıdır。
2. **Medium / 中等.**Yarın okuyacağınız makale, yayılmaktan 100 kat daha hızlı örnek almayı iddia ediyor.
   Yarın okumak zorunda olduğumuz makale, yayılmaya oranla 100 kat daha fazla örnek aldığını iddia ediyor.
3. **Hard / 困难.**İlgilendiğiniz bir alanı alın (örneğin protein yapısı, CAD, moleküller, yoldurma). Şu anki SOTA modeli için beş sorunun seçimini yanıtlayın ve daha iyi bir modelin neyi değiştirdiğini çizin.
   選一你關心的領域 (如蛋白質结构、CAD、分子、轨迹) 〜 ♂️Bu alan için mevcut SOTA 模型回答五问分类法,并勾画更好的模型会改变什么──

## Anahtar Şartlar .

| Term / 术语 | What people say / 俗称 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| Generative model | "It makes new stuff" / "它生成新东西" | Learns a sampler for `p_data(x)`, optionally exposes `log p(x)`. / 学习 `p_data(x)` 的采样器，可选暴露 `log p(x)`。 |
| Explicit density | "You can evaluate it" / "可以计算" | Model provides a closed-form or tractable `log p(x)`. / 模型提供闭式或可处理的 `log p(x)`。 |
| Implicit density | "GAN-style" / "GAN 风格" | Only a sampler — no way to evaluate `p(x)` of a given point. / 只有采样器——无法计算给定点的 `p(x)`。 |
| ELBO | "Evidence lower bound" / "证据下界" | A tractable lower bound on `log p(x)`; VAEs and diffusion optimize it. / `log p(x)` 的可处理下界；VAE 和扩散模型优化它。 |
| Score | "Gradient of log-density" / "对数密度梯度" | `∇_x log p(x)`; diffusion and SDE models learn this field. / 扩散和 SDE 模型学习这个场。 |
| Manifold hypothesis | "Data lives on a surface" / "数据在曲面上" | High-dim data concentrates on a low-dim manifold; why dimensionality reduction works. / 高维数据集中在低维流形上；降维有效的原因。 |
| Autoregressive | "Predict the next piece" / "预测下一个" | Factorize joint as product of conditionals. / 将联合分布分解为条件分布的乘积。 |
| Latent | "Compressed code" / "压缩编码" | Low-dim representation from which a decoder can reconstruct the input. / 解码器可从中重建输入的低维表示。 |

## Üretim notu: beş aile, beş sonucu şekli

Her aile farklı bir sonuç-server maliyet eğriyi haritası yapar. üretim-sonuculu literatür LLM sonuçlarını önceden doldur + çözme olarak çerçevelemektedir; aynı parçalanma burada geçerlidir:

> Her aile farklı hesaplama hizmetleri maliyet eğilimi için çalışır.

- **Autoregressive (bucket 1 and 5).**Sequential decoding latency'yi yönetiyor; KV-cache, sürekli serileme ve spekülasyonsal dekodlama hepsi doğrudan uygulanmaktadır.
  **自回归（第 1 和 5 类）。**顺序解码主导延迟;KV 缓存、连续批处理和推测解码直接适用──
- **VAE / diffusion / flow-matching (buckets 2 and 4).**LLM anlamında bir dekod yok.`num_steps × step_cost`, ve `step_cost`Üretim düğmeleri adım sayımı (DDIM / DPM-Solver / destillasyon), parti boyutu ve hassaslığı (bf16 / fp8 / int4) ile oluşur.
  **VAE / 扩散 / Flow Matching（第 2 和 4 类）。**LLM anlamında çözülmez.`num_steps × step_cost`, üretim düzenlemesi döngüsü, adım sayısı, büyüklük ve hassasiyetidir.
- **GAN (bucket 3).**Bir ileri geçiş, program yok, KV-cache yok, TTFT ≈ toplam gecikme. Bu yüzden StyleGAN hala dar alan UX'de kazanıyor.
  **GAN（第 3 类）。**单次前向传播──调度なし, KV 缓存なし──TTFT ≈ 总延迟── işte bu yüzden StyleGAN 狭域 UX 上仍然胜出的原因──

Kağıt özetinde "aşırı yayılmaktan daha hızlı" gördüğünüzde, "çık adımlar × aynı adım maliyeti" veya "aynı adımlar × daha ucuz adım maliyeti" olarak çevirin.

> "Biraz daha hızlı yayılmak" olarak çevrildiğinde, "sadece daha az adım sayısı × aynı adım maliyeti" veya "eşit adım sayısı × daha ucuz adım maliyeti" olarak çevrildiğinde, kalanı da satışdır.

## Daha fazla okumak

- [Goodfellow et al. (2014). Generative Adversarial Nets](https://arxiv.org/abs/1406.2661) GAN kağıdı.
- [Kingma & Welling (2013). Auto-Encoding Variational Bayes](https://arxiv.org/abs/1312.6114) VAE kağıdı.
- [Ho, Jain, Abbeel (2020). Denoising Diffusion Probabilistic Models](https://arxiv.org/abs/2006.11239) DDPM makalesi.
- [Song et al. (2021). Score-Based Generative Modeling through SDEs](https://arxiv.org/abs/2011.13456) SDE olarak yayılma.
- [Lipman et al. (2023). Flow Matching for Generative Modeling](https://arxiv.org/abs/2210.02747) akış eşleşen kağıt.
- [Esser et al. (2024). Scaling Rectified Flow Transformers for High-Resolution Image Synthesis](https://arxiv.org/abs/2403.03206) Dönüştürülme 3.
