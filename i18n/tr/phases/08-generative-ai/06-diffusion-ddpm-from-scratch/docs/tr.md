# Değişiklik Modeller  DDPM sıfırdan  Genişleme Modeller  DDPM'yi sıfırdan gerçekleştirmek

> Ho, Jain, Abbeel (2020) alanı durduramadığı bir tarif verdi. Bir bin küçük adım üzerinde gürültü ile verileri yok edin. Gürültüyü tahmin etmek için bir sinir ağı eğit. Süresini çıkarma esnasında tersine çevirin. Bugün her ana akım görüntü, video, 3D ve müzik modeli bu döngü üzerinde çalışır, muhtemelen akış eşleşmesi veya tutarlılık hilelerle üstü.

> **【中文解读】**DDPM'nin temel süreci: 1000 adım adım veri artırmak, gürültü bozan veriyi kullanarak, bir sinir ağı tahmin gürültüsü eğitmek, gürültü çıkarma yönünde bir düşünce yapmak.

> **【拓展：扩散模型是当前 AI 生成的核心】**DDPM, basit bir ses çıkarma hedefi ile şaşırtıcı bir üretim kapasitesini ortaya çıkarabilir.

**Type:** Build / 构建型
**Languages:** Python
**Prerequisites:** Phase 3 · 02 (Backprop / 反向传播), Phase 8 · 02 (VAE)
**Time:** ~75 minutes

## Sorunlar. Sorunlar.

Örnek almak ister misin ?`p_data(x)`GAN'lar genellikle farklı bir minimum oyun oynar. VAE'ler Gaussian dekodöründen bulanık örnekler üretir. Gerçekten istediğiniz şey (a) tek sabit bir kayıp (saddle point, no minimax) olan bir eğitim hedefi.`log p(x)`(böylelikle olasılığınız var) ve (c) SOTA kalitesine uyan örnekler.

> - Ne istiyorsun?`p_data(x)`Bu nedenle, bu durumun bir sonucu olarak, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir sürececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececece`log p(x)`Çıktı.

Sohl-Dickstein et al. (2015) teorik bir cevabı vardı: Markov zinciri tanımlamak `q(x_t | x_{t-1})`Bu da yavaş yavaş Gaussian gürültüsünü ekler ve ters bir zincir oluşturur.`p_θ(x_{t-1} | x_t)`Bu, bir kayıpın bir satır olarak basitleştirilebileceğini gösterdi. 2020 yılında bu bir meraklılıktu. 2021 yılında en son örnekler üretti. 2022 yılında Stable Diffusion oldu. 2026 yılında altyapı.

> Sohl-Dickstein (2015) teorik bir cevap verdi: yavaş yavaş yükselen gürültü Markova zinciri tanımlamak, gürültüye karşı zincir eğitimi. Ho 等人 (2020) kayıpları bir satır  tahmin gürültü olarak basitleştirecektir.

> **【中文解读】**DDPM'nin üç adımlı süreci: 1) Ön yön süreci yavaş yavaş yüksek sesli sesli sesli sesli sesler oluşturana kadar; 2) 訓練 öğrenmek bir ağ tahmin her adım eklenen sesli; 3) ters yön süreci saf sesli sesli seslerden yavaş yavaş gürültüye başlamak, gerçek veriyi geri kazanmak için.

> **【拓展：从 DDPM 到实用扩散模型】**DDPM 原始论文在像素空间操作,速度慢(需要1000步去噪) ;;三个关键改进使它成为实用工具:(1) DDIM(2020) 采样步数将从1000 降至20-50;(2) 潜在扩散(2021,Rombach) 在 VAE 潜在空间中操作,大幅降低计算量;(3) CFG(Classifier-Free Guidance,2022) 通过条件/无条件预测的差提升生成质量;;

## Konsepten bir şey.

![DDPM: forward noise, reverse denoise](../assets/ddpm.svg)

**Forward process `q`.**Gaussian gürültüsünü ekleyin .`T`Kapalı form  matematikin ele alınması 'nin nedeni kumületif adımın da Gaussian olmasıdır:

> **前向过程 `q`。**- Evet .`T`Küçük adımlar arasında yavaş yavaş yüksek ses artışı.

```
q(x_t | x_0) = N( sqrt(α̅_t) · x_0,  (1 - α̅_t) · I )
```

nerede`α̅_t = ∏_{s=1..t} (1 - β_s)``β_t`- Seç .`β_t`1e-4'den 0.02'e kadar lineer olarak T=1000 adım üzerinde ve `x_T`Yaklaşık olarak `N(0, I)`- Evet .

> İçlerinden `α̅_t = ∏_{s=1..t} (1 - β_s)`- Ben de.`β_t`1e-4'den 0.02 线性排列 T=1000 步,`x_T`Yakınlık`N(0, I)`- Evet.

**Reverse process `p_θ`.**Bir sinir ağını öğrenin .`ε_θ(x_t, t)`Bu da eklenen gürültüyü tahmin eder.`x_t`, aşağıdakilerle tanımlanır:

> **反向过程 `p_θ`。**Bir sinir ağı öğrenin .`ε_θ(x_t, t)`预测添加的噪音──给定 `x_t`,去噪方式为:

```
x_{t-1} = (1 / sqrt(α_t)) · ( x_t - (β_t / sqrt(1 - α̅_t)) · ε_θ(x_t, t) )  +  σ_t · z
```

nerede`σ_t`Ya da`sqrt(β_t)`Bu ifade çirkin ama sadece cebir  çözmek için `x_{t-1}`Arka tarafı verildiği için`q(x_{t-1} | x_t, x_0)`ve yerine getirmek`x_0`gürültü tahminleri ile.

> İçlerinden `σ_t`Evet .`sqrt(β_t)`Ya da öğrenmek için farklılıklar. Bu ifade karmaşık görünüyor ama sadece bir sayı.`q(x_{t-1} | x_t, x_0)`Çözüm arayın .`x_{t-1}`- Evet.

**Training loss.**

```
L_simple = E_{x_0, t, ε} [ || ε - ε_θ( sqrt(α̅_t) · x_0 + sqrt(1 - α̅_t) · ε,  t ) ||² ]
```

Örnek`x_0`Verilerden, rastgele bir seçin.`t`, örnek`ε ~ N(0, I)`, gürültülü hesaplayın .`x_t`Bir atışta kapalı formda, gürültüye geri döner.

> Verilerden alıntı`x_0`, her zaman seçilir`t`- Evet .`ε ~ N(0, I)`, bir kez kalıp ses içeren bir hesaplama yoluyla`x_t`, sesle ilgili bir kayıp, minimum bir miktar, KL, ağırlıklı bir parametreleme becerisi yok.

**Sampling.**Başlayın .`x_T ~ N(0, I)`- Geri adımını tekrarla .`t = T`- ...`1`- Tamam.

> **采样。**- Evet .`x_T ~ N(0, I)`开始,从 `t = T`- Ne ?`1`代反向步骤──完成──

## Neden işe yarıyor ?

Üç içgüdü:

> Üçüncü görüş:

1. **Denoising is easy; generating is hard.**- Evet .`t=T`, veriler saf gürültü  ağ küçük bir sorunu çözmek zorunda.`t=0`... ağ sadece birkaç piksel temizlemek zorunda.`t`Bu sorun zor ama ağın her gürültü seviyesinden aynı ağırlıklardan akıp giden birçok gradiyenti var.
   **去噪容易，生成难。**- Evet .`t=T`时,数据是纯噪音网络只需要解决简单的问题.`t=0`时, net sadece küçük miktarda görüntü temizlemek gerekir.

2. **Score matching in disguise.**Vincent (2011) gürültü tahmininin tahminle eşdeğer olduğunu kanıtladı `∇_x log q(x_t | x_0)`Bu puanı kullanan geri SDE, yoğunluk gradiyenti 'nin yukarısına doğru yüksek olasılık bölgelerine doğru yönlendirilmiş rastgele bir yürüyüş yapar.
   **伪装的分数匹配。**预测                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           `∇_x log q(x_t | x_0)`❖ SDE'ye karşı bu oranın yoğunluk derecesi yükselmesine izin vererek kullanmak.

3. **The ELBO reduces to simple MSE.**DDPM'nin parametreleştirmesiyle bu KL terimleri, belirli koeficientlerle gürültü öngörüsü üzerinde MSE'ye basitleştirilmiştir; Ho koeficientleri düşürmüştür (sadece kayıp olarak adlandırılır) ve kalitesi * iyileştirilmiştir*.
   **ELBO 简化为简单 MSE。**完整的变分下界 每个时间步骤都有 KL 项──何 抛弃系数后质量反而*提升*了──

## Yapın.
```figure
diffusion-denoise
```

## Yapın

`code/main.py`1 boyutlu DDPM uygulamasını uyguluyor. Veriler iki modlu bir karışım. "net" ise küçük bir MLP'dir.`(x_t, t)`Bu, bir çizgi kaybı, örneği alınarak geri zincir tekrarlanır.

> `code/main.py`实现一维 DDPM──数据是双峰混合──"网络" (bir biçimli MLP)`(x_t, t)`输出预测噪音──训练就是那一行损失──采样代反向链──

### Adım 1: Önceki program (kapalı form)

```python
betas = [1e-4 + (0.02 - 1e-4) * t / (T - 1) for t in range(T)]
alphas = [1 - b for b in betas]
alpha_bars = []
cum = 1.0
for a in alphas:
    cum *= a
    alpha_bars.append(cum)
```

### İkinci adım: örnek`x_t`Tek bir atışta

```python
def forward_sample(x0, t, alpha_bars, rng):
    a_bar = alpha_bars[t]
    eps = rng.gauss(0, 1)
    x_t = math.sqrt(a_bar) * x0 + math.sqrt(1 - a_bar) * eps
    return x_t, eps
```

### Adım 3: Tek eğitim adımı

```python
def train_step(x0, model, alpha_bars, rng):
    t = rng.randrange(T)
    x_t, eps = forward_sample(x0, t, alpha_bars, rng)
    eps_hat = model_forward(model, x_t, t)
    loss = (eps - eps_hat) ** 2
    return loss, gradient_step(model, ...)
```

### 4. adım: ters örnekleme

```python
def sample(model, alpha_bars, T, rng):
    x = rng.gauss(0, 1)
    for t in range(T - 1, -1, -1):
        eps_hat = model_forward(model, x, t)
        beta_t = 1 - alphas[t]
        x = (x - beta_t / math.sqrt(1 - alpha_bars[t]) * eps_hat) / math.sqrt(alphas[t])
        if t > 0:
            x += math.sqrt(beta_t) * rng.gauss(0, 1)
    return x
```

40 zaman aşamasıyla ve 24 birim MLP ile 1 boyutlu bir sorun için, bu, iki mod karışımını ~ 200 dönemde öğrenir.

> 40 个时间步和 24 单元 MLP 的一维问题, yaklaşık 200 轮即可学会双峰混合──

## Zaman şartlandırması .

Ağ hangi zaman aşamasını tanımladığını bilmesi gerekiyor.

> 网络需要知道它在哪个时间步骤中.

- **Sinusoidal embedding.**Transformer pozisyon kodlaması gibi.`embed(t) = [sin(t/ω_0), cos(t/ω_0), sin(t/ω_1), ...]`Bir MLP'yi geçiyor ve ağda yayınlanıyor.
  **正弦嵌入。**类似变压器 位置编码──
- **Film / group-norm conditioning.**Proje, her blokta kanal ölçeğine/kıskançlığa (FiLM) yerleştirilmektedir.
  **FiLM / 组归一化条件化。**Projectio'yu her kanal için yerleştirir.

Oyuncak kodumuz sinusoidal → concat kullanıyor.

> Bizim oyuncak kodumuz, tam bir string ile.

## Tuzaklar.

- **Schedule matters a lot.**Düzsel `β`DDPM'nin varsayılan, ancak cosine şeması (Nichol & Dhariwal, 2021) aynı hesaplama için daha iyi FID verir.
  **调度很重要。**线性 `β`DDPM 默认但余弦调度在相同计算量下 FID 更好──
- **Timestep embedding is fragile.**Çürük geçiyor .`t`bir yüzerken oyuncak 1-D için çalışır ama görüntüler için başarısız olur; her zaman uygun bir yerleştirme kullanın.
  **时间步嵌入脆弱。**Önemli`t`Oyuncaklar 1D'de var ama resim gitmiyor.
- **V-prediction vs ε-prediction.**Sık rejimler için (çok küçük veya çok büyük t), `ε`Sinyal-gürültü zayıflığı.`v = α·ε - σ·x`) daha istikrarlıdır; SDXL, SD3 ve Flux kullanırlar.
  **V 预测 vs ε 预测。**Son zamanlarda daha da sabit bir şekilde kullanılıyor.
- **Classifier-free guidance.**Sonuçta, hem koşullu hem de koşulsuz hesaplayın.`ε`O zaman ...`ε_cfg = (1 + w) · ε_cond - w · ε_uncond`- Evet .`w ≈ 3-7`8. derste ele alındı.
  **无分类器引导。**推理时计算条件和无条件预测的差值──第 08 课详述──
- **1000 steps is a lot.**Üretim DDIM (20-50 adım), DPM-Solver (10-20 adım) veya destillasyon (1-4 adım) kullanır.
  **1000 步太多了。**Üretim için DDIM ((20-50 步) 、DPM-Solver ((10-20 步) 蒸(1-4 步) 

## Çerçeveyi kullanın.

| Role / 角色 | Typical stack in 2026 / 2026 典型技术栈 |
|------|-----------------------|
| Image pixel-space diffusion (small, toy) / 像素空间扩散 | DDPM + U-Net |
| Image latent diffusion / 潜在扩散 | VAE encoder + U-Net or DiT (Lesson 07) |
| Video latent diffusion / 视频潜在扩散 | Spatiotemporal DiT (Sora, Veo, WAN) |
| Audio latent diffusion / 音频潜在扩散 | Encodec + diffusion transformer |
| Science (molecules, proteins, physics) / 科学 | Equivariant diffusion (EDM, RFdiffusion, AlphaFold3) |

Diffusion, evrensel üreticiden oluşan omurgasıdır. Akış eşleşimi (Desin 13) genellikle aynı kalite için çıkarım hızı üzerinde kazanan 2024-2026 rakipidir.

> 扩散是通用生成骨干;;Flow Matching (第 13 课)  2024-2026'ın rakipleri, genellikle aynı kalite altında daha hızlı olarak düşünülür.

## İndirin . Ürünler .

- Kaydet .`outputs/skill-diffusion-trainer.md`. Yetenek bir veri kümesi + hesaplama bütçesi ve çıkışları alır: program (lineer/kosin/sigmoid), tahmin hedefi (ε/v/x), adım sayısı, rehberlik ölçeği, örnekleme ailesi ve değerlendirme protokolü.

> 保存 `outputs/skill-diffusion-trainer.md` Yetenekler                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        

## Egzersizler.

1. **Easy / 简单.**T' yi 40 ' dan 10 ' a değiştirin `code/main.py`- Örnek kalitesi (işlemlerin görsel histogramı) nasıl bozulur?
   T'yi 40'dan 10'a dönüştürmek.
2. **Medium / 中等.**E-büyüklüğünden V-büyüklüğüne geçin. Geri adımları tekrar alın. Son örnek kalitesini karşılaştırın.
   E 预测切换到 v 预测。重新推导反向步骤──比较最终样本质量──
3. **Hard / 困难.**Sınıf etiketi üzerinde koşul `c ∈ {0, 1}`, eğitim sırasında ve örnekleme zamanında kullanımı %10 düşürmek `ε = (1+w)·ε_cond - w·ε_uncond`Şartlı modda vurma oranını ölçmek`w = 0, 1, 3, 7`- Evet .
   添加无分类器引导──测量 `w = 0, 1, 3, 7`时的条件模式命中率──

## Anahtar Şartlar .

| Term / 术语 | What people say / 俗称 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| Forward process | "Adding noise" / "加噪" | Fixed Markov chain `q(x_t \| x_{t-1})` that destroys the data. / 破坏数据的固定马尔可夫链。 |
| Reverse process | "Denoising" / "去噪" | Learned chain `p_θ(x_{t-1} \| x_t)` that reconstructs the data. / 重建数据的学习链。 |
| β schedule | "The noise ladder" / "噪声阶梯" | Per-step variance; linear, cosine, or sigmoid. / 每步方差；线性、余弦或 S 形。 |
| α̅ | "Alpha bar" | Cumulative product `∏(1 - β)`; gives closed-form `x_t` from `x_0`. / 累积乘积，给出闭式 `x_t`。 |
| Simple loss | "MSE on noise" / "噪声 MSE" | `\|\|ε - ε_θ(x_t, t)\|\|²`; all variational derivations collapse to this. / 所有变分推导最终坍塌为此。 |
| ε-prediction | "Predict noise" / "预测噪声" | Output is the noise added; standard DDPM. / 输出是添加的噪声。 |
| V-prediction | "Predict velocity" / "预测速度" | Output is `α·ε - σ·x`; better conditioning across t. / 跨时间步条件化更好。 |
| DDPM | "The paper" / "那篇论文" | Ho et al. 2020; linear β, 1000 steps, U-Net. |
| DDIM | "Deterministic sampler" / "确定性采样器" | Non-Markov sampler, 20-50 steps, same training objective. / 非马尔可夫采样器。 |
| Classifier-free guidance | "CFG" | Mix conditional and unconditional noise predictions to amplify conditioning. / 混合条件和无条件预测以放大条件化。 |

## Üretim Not: Yayılma sonucu bir adım sayım sorunu.

DDPM kağıdı T=1000 ters adımları çalışır. Kimse üretimde bu gemi. Her gerçek sonuç yığın üç stratejiden birini seçer  ve her haritada temiz bir şekilde üretim çerçevesinde "kenden gecikme geliyor"

> DDPM 论文 T=1000反向步──生产中没有人这样做──每种策略对应生产中"延迟来自哪里":

1. **Faster sampler, same model.**DDIM (20-50 adım), DPM-Solver++ (10-20), UniPC (8-16).`ε_θ`Ağırlıklar dokunulmamış.
   **更快的采样器，相同模型。**DDIM、DPM-Solver++、UniPC──即插即用替换反向循环,降低延迟 20-50 倍──
2. **Distillation.**Öğrenciyi daha az adımla öğretmenine eşleştirmek için eğit: Gelişmiş Destillation (2 → 1), Düzgünlik Modeller (Özbürekli → 1-4), LCM, SDXL-Turbo, SD3-Turbo. Gecikme 5-10 x daha azaltır, yeniden eğitime ihtiyaç duyar.
   **蒸馏。**訓練学生模型在更少步数匹配教师──再降延迟 5-10 倍,重训需要──
3. **Caching and compilation.** `torch.compile(unet, mode="reduce-overhead")`TensorRT-LLM'in yayılma arka planları.`xformers`/SDPA dikkat, bf16 ağırlıkları. Adımlık gecikme ~ 2 ×. (1) ve (2) ile yığılır.
   **缓存和编译。**Torch.compile、TensorRT、xformers、bf16──降低每步延迟约2倍──

Bir üretim dağıtım sunucu için bütçe konuşması, LLM için üretim literatüründe tarif edilen gibi: gecikme `num_steps × step_cost + VAE_decode`, geçiş `batch_size × (num_steps × step_cost)^-1`TTFT küçüktür (bir adım); TPOT eşdeğeri tam yanıt süresi, çünkü görüntü oluşturma kullanıcı açısından "her zaman"dır.

> Üretim ve eğitim programı`num_steps × step_cost + VAE_decode`△TTFT 很小(一步);TPOT 等价物是完整响应时间──

## Daha fazla okumak

- [Sohl-Dickstein et al. (2015). Deep Unsupervised Learning using Nonequilibrium Thermodynamics](https://arxiv.org/abs/1503.03585) yayılma kağıdı, zamanından önce.
- [Ho, Jain, Abbeel (2020). Denoising Diffusion Probabilistic Models](https://arxiv.org/abs/2006.11239) DDPM.
- [Song, Meng, Ermon (2021). Denoising Diffusion Implicit Models](https://arxiv.org/abs/2010.02502) DDIM, daha az adım.
- [Nichol & Dhariwal (2021). Improved DDPM](https://arxiv.org/abs/2102.09672)- Kosinus programı, öğrenilmiş değişim.
- [Dhariwal & Nichol (2021). Diffusion Models Beat GANs on Image Synthesis](https://arxiv.org/abs/2105.05233) sınıflandırıcı rehberliği.
- [Ho & Salimans (2022). Classifier-Free Diffusion Guidance](https://arxiv.org/abs/2207.12598)CFG.
- [Karras et al. (2022). Elucidating the Design Space of Diffusion-Based Generative Models (EDM)](https://arxiv.org/abs/2206.00364) Tek bir notasyon, en temiz tarif.
