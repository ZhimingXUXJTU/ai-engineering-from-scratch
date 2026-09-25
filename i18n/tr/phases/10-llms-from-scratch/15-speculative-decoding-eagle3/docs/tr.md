# İsteğe bağlı Çözüm ve EAGLE-3

> Fase 7 · Ders 16 matematik kanıtladı: Leviathan reddetme kuralı doğrulayıcının dağılımını tam olarak korur. Bu ders 2026 üretim spekülasyonu çözme eğitim-stack görüşüdür. EAGLE-3 taslak modelini ucuz bir yaklaşımdan verifikatörün kendi gizli durumlarında eğitilmiş özel olarak inşa edilmiş küçük bir ağ haline getirmiş ve ardından tren ve sonuç dağılımlarını uyumlu hale getiren bir eğitim zamanı test döngüsü ekledi. Sonuç: 3x'ten 6.5x'e kadar hızlandırma, sohbette 0.9'dan fazla kabul edilen token oranları, dağıtımsal bir ödeme yok. 2026'da her üretim sonuç kümesi varsayılan olarak gönderir.

> **【中文解读】**投机解码: 小模型猜测接下来 3-5 代币,大模型只需验证――猜对就就就 5 代币算一个的价――EAGLE-3 用目标模型的隐藏状态训练草稿网络,接受率 90%+,3-6.5 倍加速,输出分布不变――

> **【拓展：投机解码→生产推理】**2026 yılında tüm ana düşünce çerçevesinde (vLLM、TensorRT-LLM) tüm yatırımlar için bir çözüm oluşturuldu.

>  **【前置】**学本节前 Lütfen önce öğrenin:Fase 07·16(Spekülatör Deçifreleme 数学証明);Fase 10·12(Inference Optimization);Transformer 隐藏状态概念──本节是生产部署投机解码的工程视角──

>  **【类比】**投机解码 = 老板让实习生先起草邮件。实习生(草案模型) 秒写 5 段草稿,老板(大模型) 校对一次一次。校对一段比从头写一段快得多。校对时如果某段错了,从那段开始重写。EAGLE-3'ün anahtarı:实习生看过老板以前写的邮件隐藏思考(隐藏状态),起草更像老板风格,接受率90%+。

**Type:** Build
**Languages:** Python (stdlib)
**Prerequisites:** Phase 7 · 16 (speculative decoding math), Phase 10 · 12 (inference optimization)
**Time:** ~75 minutes

## Öğrenme hedefleri

- Leviathan teoremiyi bir cümleyle belirtin ve spekülatif döngünün doğrulayıcıya eşit şekilde dağıtılmış örnekler ürettiğini kanıtlayın.
  Bir cümleyle ifade et Leviathan teorisi, proje döngüsü oluşturan örnekle testçi doğrudan örnek dağılımı aynı
- Vanilya spesifikasyonları çözme (Leviathan 2023) ile EAGLE, EAGLE-2, ve EAGLE-3 arasında iki yıllık ilerlemeyi izleyin ve her adımda ayrılmış tam sınırlamaları belirleyin.
  理 from朴素投机解码(Leviathan 2023) to EAGLE、EAGLE-2、EAGLE-3'ün iki yıllık gelişimi, her adımın taşındığı belirli sınırları belirle
- Kabul oranından beklenen hızlandırmayı hesaplayın `α`ve taslak ve denetçi maliyet oranı `c`, ve en uygun taslak uzunluğunu seçin `N`Her rejim için.
  Kabul oranı`α`和草稿-验证成本比 `c`計算预期加速,                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        `N`
- Tam spekülatör döngüsünü sıfırdan uygulayın: geri kalanı çiz, doğrulay, reddet-anlamayı, reddedildiğinde KV önbelleğini geri çevir, tam kabul olduğunda bonus tokenini yayınlayın.
  0'dan tam bir proje döngüsünü gerçekleştirmek: taslak, denetim, geri kalanı reddetmek, örnekleme reddetmek, geri dönmek KV  depolama, tüm kabul edilmek, ödül belirtilerini göndermek

## Sorunlar. Sorunlar.

H100'de otomatik olarak geriye dönük kodlama, saniyede 35 token hızında çalışır. GPU hiçbir yere doymuş değildir. Hatırlama bant genişliği tavan: her token HBM'den 70B ağırlık yükler, bir adım aritmetik yapar ve bir akış üretir. Hesaplama birimleri çoğunlukla hareketsiz oturuyor.

> 70B modelinin kendi kendine dönüşüm çözümü kodu H100'de yukarı yaklaşık olarak her saniye 35 token。GPU 远未和。显存带宽是上限: Her token HBM'den yüklenir 70B 权重, bir adım işlem yaparak, bir浮点数··计算单元大部分时间在置──

Bu, aslında çözebileceğiniz bir çıkış gücü sorunu haline getirir.`N`Tokenler `N`Verifiyeci bir kez önbellekle eklenir.`N`Eğer doğrulayıcı'nın konumdaki dağılım `i`Eğer bir projeyi kabul edersek (istatistik anlamda kesinleşeceğiz), kabul edersek; eğer kabul etmezsek, geri kalan dağılımdan bir düzeltme reddeder ve örnek alırız.`N+1`Bir tane yerine simgeler kabul etti.

> 投机解码 bunu pratik olarak çözebileceğiniz bir toplama sorunu olarak dönüştürür. N 次小前向传播 ile ucuz bir taslak modeli N 个符号を提出します. Taslaklayıcı, tüm N 个草稿 üzerinde bir kez çalışmaktadır. Eğer taslaklayıcı, i konumundaki dağılımıyla taslakla uyumludursa, kabul ederiz. Aksi takdirde, bir düzeltmeyi reddeder ve bir kez büyük bir modelin ön yönünde yayılmaya en fazla N + 1 kabul edilen bir tane ortaya çıkarır.

Önemli olan teorem Leviathan, Kalman, Matias (ICML 2023): çıkış dağılımı doğrulayıcıdan doğrudan üretilen örnekle aynıdır. Yaklaşık olarak değil. Aynı şekilde. Bu tüm neden spekülasyonsal dekodlama üretimde kabul edilebilir.

> 关键定理来自Leviathan、Kalman、Matias(ICML 2023): 输出分布与直接从验证器采样中产生的分布相同──不近似──是相同──这是投机解码在生产环境中可接受的全部原因它是纯粹的延迟优化,没有质量折衷──

Bu ders size eğitim yığını veriyor. İyi bir taslak ucuz bir taslaktan 2 kat daha fazla hızlandırmaya değer. EAGLE, EAGLE-2, ve EAGLE-3 (Li et al., 20242025) "taslak = aynı modelin daha küçük versiyonunu" kesin bir mühendislik disipline dönüştürdü. 2026 üretim sonuç sunucuları EAGLE-3'e varsayılan olarak varsayılır.

## Konsepten bir şey.

> **【中文解读】**投机解码(Spekülatör Dekoding) 小模型快速猜测多个代币,再用大模型并行验证接受代币 直接保留,被拒绝从拒绝点重新生成──EAGLE 系列方法在特征层而不是代币层进行投机,接受率更高──

> **【拓展：投机解码的加速效果】**标准投机解码: 2-3x 推理加速无损输出质量──EAGLE-2 和 Medusa 等等方法通过多头并行预测达到3-4x 加速──关键技术指标是接受率(接受率) 小模型与大模型的分布越接近,接受率越高,加速效越好──


### Değişmeyen: Leviathan reddetme örneği

- Bırak .`p(t)`Bir ön işaret verildiğinde, bir sonraki simge için taslakın dağıtımı olmalıdır ve `q(t)`Verifikatörün bir taslak simgesi.`d ~ p`- Muhtemelen kabul et .`min(1, q(d) / p(d))`.Yıkıtıldığında, kalan dağıtımdan örnek`(q - p)_+ / ||(q - p)_+||_1`. Sonuçta elde edilen örnekler `q`Bu ne kadar kötü olursa olsun doğru .`p`Ne kadar kötü olursa, o kadar sık reddedilir, ama sonuç tam kalır.

Yumruk .`N`Bu çağrıların bir verifikatörle geri dönüş yapılması için bir verifikatör kullanın.`prefix + d_1 + ... + d_N`- Verifiyeci geri dönüyor .`q_1, q_2, ..., q_{N+1}`Birinci reddedilme sırasında, pozisyonda sola doğru yürüyün.`j`, `residual(q_j, p_j)`Tam kabul edildiğinde, bir bonus token örneği alın.`q_{N+1}`- Evet .

### Hızlandırmayı belirleyenler

- Bırak .`α`Bu, bir taslak çekilen token için beklenen kabul oranı olacaktır.`c = cost(draft) / cost(verifier)`Geçmiş doğrulayıcı başına kabul edilen tokenlerin beklenen sayısı:

```
E[accepted] = (1 - α^(N+1)) / (1 - α)
```

Kabul edilen bir token için beklenen toplam duvar süresi `(N * c + 1) / E[accepted]`- Bunu en az `N`Ve sen de tatlı noktayı alırsın.`α = 0.8, c = 0.05`: en iyi `N`5 7 civarında, hızlanma 3.2 x.`α = 0.95, c = 0.02`: en iyi `N`810 civarında, hızlanma 5×'ye doğru ilerliyor.

En büyük tek kaldıraç `α`- Bırakın .`α = 0.6`(vanilya taslak) `α = 0.9`(Eagle-3) sabit `N = 5`2.2, verifiyeci başına kabul edilen belirtilerden 4.1'e doğru ilerler.

### İki yıllık ilerleme

**Vanilla speculative (Leviathan, 2023).**Draft modelinde aynı aileden bağımsız olarak eğitimli küçük bir LLM vardır.`α ≈ 0.6`En iyi şekilde 2 kat hızlandır.

**EAGLE-1 (Li et al., 2024).**Draft, verifiyecinin son katman gizli durumunu giriş olarak alan ve bir sonraki jetonu doğrudan tahmin eden küçük bir transformatördür.`α`0.70.8'e kadar yükselir.

**EAGLE-2 (Li et al., 2024).**Dinamik bir çizgi ağacı ekler: tek bir dizi önermek yerine `N`Tokenler, küçük bir aday ağacı önerir, her birini bir ileri geçiş (ağaç dikkat) ile doğrulayıcı ile puanlar ve en yüksek olasılık yolu ile yürürler.`α`kabul edilen yol için token 0.85'in üzerinde yükselir.

**EAGLE-3 (Li et al., 2025, NeurIPS).**İki değişiklik daha. Öncelikle, özellik tahmin kaybını tamamen bırakın  EAGLE-1/2 taslakı doğrulayıcının gizli durumlarına eşleştirmek için eğitti, bu da ne kadar veri yardımı sağladığını sınırlıyor. Eagle-3 doğrudan simge tahminleri üzerine trenler. İkinci olarak, eğitim zaman testi (TTT): taslak eğitim sırasında, taslakın kendi önceki tahminlerini bir çok aşamada giriş olarak geri vererek, sonuçlandırma sırasında aynı şekilde çalışır. Bu, tren ve test dağılımlarını birleştirir ve hata birikimini durdurur. Ölçülen hızlandırma: sohbette 6,5x'e kadar, H100'deki SGLang'da 64 seriyle 38% oranında hızlandırma.

### KV önbelleği geri dönüşü

Verifikasyon, verifikatörün KV önbelleğini `N`Bir geçitle girişler.`j`, önbelleğin içeriği geçmiş konumdadır `j-1`İki yaygın uygulama: bir çizim tamponu yazın ve kabul üzerine commit (vLLM, TensorRT-LLM), veya fiziksel KV önbelleği ek olarak mantıklı bir uzunluk ve reddetme üzerine keskinleştirin.

EAGLE-2 ağaç arayışı için, injeneri zor ama hesaplama standart bir flaş dikkat çağrısı özel bir maska ile.

### 2026 yılında mimarlık projeleri

| Strategy | Draft type | `α` | Speedup | Training cost |
|----------|-----------|-----|---------|---------------|
| Vanilla | Separate small LLM | 0.55-0.70 | 1.8-2.3× | None (reuse existing small model) |
| Medusa | Extra LM heads on verifier | 0.65-0.75 | 2-3× | ~1B SFT tokens |
| EAGLE-1 | 1-layer transformer on hidden states | 0.70-0.80 | 2.5-3× | ~60B tokens |
| EAGLE-2 | EAGLE-1 + dynamic draft tree | 0.80-0.88 | 3-4× | ~60B tokens |
| EAGLE-3 | Multi-layer feature fusion + TTT | 0.88-0.92 | 3.5-6.5× | ~60-200B tokens |
| Lookahead | No draft (Jacobi iteration) | N/A | 1.3-1.6× | None |

2026'da üretimi: vLLM ve SGLang varsayılan EAGLE-3 mevcut olduğunda, EAGLE-2 aksi takdirde. TensorRT-LLM Meta ve NVIDIA kamu modelleri için en hızlı Medusa yolu var. llama.cpp CPU dağıtımları için vanilla taslak gemileri.


> **【拓展：EAGLE 的创新点】**EAGLE, belirti alanında değil, özellik alanında yatırım yaparak, önde gelen birkaç katın özelliklerini kullanarak gelecekteki özellikleri tahmin eder, tekrar belirti belirti çözme belirtilerinden alınır.


## Yapın.
```figure
l5-spec-decode-eagle
```

## Yapın

Bakın .`code/main.py`Bu, tüm parçaları içeren Leviathan spekülatör döngüsü: N'in taslakı, doğrulayıcı paralel geçiş, pozisyon başına reddedilme, kalan örnekleme, bonus jetonu, KV geri dönüşü ve çıkış dağıtımının doğrudan örnekleme ile eşleştiğini deneysel olarak doğrulama `q`- Evet .

### Adım 1: reddetme kuralı

```python
def accept(q_prob, p_prob, u):
    if p_prob <= 0:
        return True
    return u < min(1.0, q_prob / p_prob)
```

### Adım 2: Geri kalan dağılım

```python
def residual(q, p):
    raw = [max(0.0, qi - pi) for qi, pi in zip(q, p)]
    s = sum(raw)
    if s == 0:
        return list(q)
    return [r / s for r in raw]
```

### Adım 3: Tam bir spekülasyonsal adım

- Evet .`spec_step`fonksiyon taslakları `N``p`, sonra hepsini bir paralelde doğruluyor .`q`değerlendirme. her taslağa hazırlanmış token için reddetme kuralını uyguluyor ve ilk reddetmede geri kalanın düzeltmesini örnekler.`q_{N+1}`- Evet .

### 4. Adım: KV'nin geri dönüşü muhasebeciliği

Simülatör mantıklı bir şekilde izliyor .`kv_length`İşçi başına.`k`Özetleme`kv_length += k`- Bir pozisyonda reddedildiği için .`j`, önbelleği zaten geçmişte yazılmış .`j`, ama mantıksal uzunluk `prefix_length + j + 1` bir düzeltme işaretinin ötesinde. Sonraki okurlar mantıksal uzunlukta kesik.

### 5. Adım: Leviathan kontrolü

50.000 spekülatör adım atın. Kabul edilen tokenların empiri dağılımını sayın.`q`Chi-square istatistikleri kritik değerden çok daha az olmalıdır.

### Adım 6: hızlandırma vs. α

Çelişkiyi rahatsız ederek taslak kalitesini tarayın .`p`- Kaldır .`q`Farklı amplitudlarda ölçülür.`α`, sonra verifikatör çağrısı başına beklenen tokenları  fonksiyonu olarak çiz .`α`ve `N`. Kod EAGLE-3 sınıfı taslak kalitesinin nasıl gösterildiğini gösteren bir tablo basıyor (`α ≈ 0.9`) verifiyeci çağrısı başına 45 tokeni açar.

## Çerçeveyi kullanın.

Üretim seviyesi `vllm serve`EAGLE-3 ile:

```bash
vllm serve meta-llama/Llama-3.3-70B-Instruct \
  --speculative-config '{
    "model": "yuhuili/EAGLE3-LLaMA3.3-Instruct-70B",
    "num_speculative_tokens": 5,
    "method": "eagle3"
  }'
```

H100'deki 64 partide EAGLE-3 ile SGLang: EAGLE-3 kağıdı için, batch-64 vanilya çözümü oranında yaklaşık 1,38 x daha fazla geçiş gücü.

Tahmin edici şifreleme için ne zaman ulaşabilirsiniz:

- P50 gecikme, en yüksek geçişten daha önemli olan herhangi bir etkileşimli sohbet iş yükü.
- Kod üretimi ve yapılandırılmış çıkış (JSON, SQL). `α`hedef dağılımının çok öngörülebilir olduğu için 0.9'dan fazla.
- Uzun süreli jenerasyon (binlerce token).

Ne zaman yapmamak:

- Çok küçük modeller (< 3B). taslak, doğrulayıcıdan çok daha ucuz değildir.
- Küçük bir seri 1 CPU dağıtımları.
- Çok yüksek sıcaklıklı yaratıcı örnekleme`α`- Düşüyor.

## İndirin . Ürünler .

Bu ders bize çok yararlı .`outputs/skill-eagle3-tuner.md`. Bir sonucu iş yükü (model, seri boyutu, hedef gecikme, görev profili) göz önüne alındığında, spekülatör bir çözme stratejisi ve ayarlama parametreleri (çeftel ailesi, `N`, ağaç derinliği, sıcaklık bilinciyle geçiş).

> 本课产 出 `outputs/skill-eagle3-tuner.md`◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊                                                                                                                                                                                                                                        `N`、树深度、温度感知切换) ⋅

## Egzersizler.

1. Çık .`code/main.py`Leviathan dağıtım kontrolü için chi-square istatistiklerini onaylayın.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`code/main.py`❖ Leviathan dağıtım kontrolü için kargoların sayısal oranının %95'ten daha düşük olduğunu belirlemek.

2. Tarama`N`1 ila 10 arasında `α`0.9 ve `c`Verifier çağrısı başına beklenen tokenleri ve token başına gerçek duvar zamanını hesaplayın.`N`Bu, duvar zamanını en aza indirerek eğriğin şeklini açıklar.
   Çeviri:`N`1'den 10'a kadar.`α`保持 0.9,`c`保持 0.04── draw per test调用期望符号 数和每符号 实际挂钟时间──找到最小化挂钟时间的 `N`❖ açıklama ❖

3. EAGLE-2 ağacı arama simülasyonu için kod değiştirin: her adımda, taslak bir ağaç şekli önerir `[2, 2, 2]`Verifiyeci bir kez çalışır ve en büyük olasılıkla kabul edilen yol kazanır.`α`Verifiye çağrısı başına bir yaprak ve toplam token.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`[2, 2, 2]`形形的树(8 条候选路径) ▽验证器运行一次,最高概率的接受路径胜出──计算每叶 ▽`α`Yörüngede kullanılan toplam token sayısı.

4. İki eşzamanlı dizide bir KV geri dönüş simülatörü uygulayın. A dizide tüm taslaklar kabul edildi; B dizide 2. pozisyonda reddetmelerini göster.`kv_length`Bu, bir dizi olarak güncellenir ve hiçbir çalışma boşa harcanmaz.
   Çinçe Çevirim: gerçekleştirmek iki并发序列の批量 KV 回滚模拟器──序列 A 所有草稿接受;序列 B 在位置 2 被拒绝──展示正确的`kv_length`按序列更新且无浪费──

5. EAGLE-3 makalesinin 4. bölümünü okuyun.TTT'si olmayan saf bir taslak eğitimi neden maruz kalma önyargısı altındadır ve taslak eğitimi sırasında kendi tahminlerini beslemek neden onu düzeltir.
   Çinçe çevirisi: READ EAGLE-3 论文第 4 节(тренинг时测试) 』

## Anahtar Şartlar .

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|------------------------|---------|
| Leviathan rule | "min(1, q over p)" | Bernoulli accept/reject with probability `min(1, q(d)/p(d))`, preserves the verifier distribution exactly when you sample from the residual on rejection | Leviathan 规则，精确保持验证器分布的接受/拒绝规则 |
| Residual distribution | "(q minus p) plus, normalized" | `(q - p)_+` clamped at zero and renormalized — the correct distribution to sample from on rejection | 残差分布，拒绝时从中采样的正确分布 |
| Acceptance rate α | "how often the draft is right" | Expected per-token Bernoulli-success probability under the rejection rule; governs all speedup math | 接受率，草稿每 token 的期望成功概率 |
| EAGLE-1 | "hidden-state draft" | Tiny transformer draft conditioned on the verifier's last-layer hidden state (Li et al., 2024) | EAGLE-1，基于验证器隐藏状态的小型草稿 |
| EAGLE-2 | "dynamic draft tree" | EAGLE-1 plus a tree of candidate continuations scored with tree attention in one verifier pass | EAGLE-2，动态草稿树+树注意力 |
| EAGLE-3 | "training-time test" | Drops the feature-prediction loss, trains on direct token prediction with the draft fed its own outputs during training | EAGLE-3，训练时让草稿自回归生成以匹配推理分布 |
| Training-time test (TTT) | "exposure bias fix" | Run the draft autoregressively during training so train and test input distributions match — the direct analog of scheduled sampling | 训练时测试，解决曝光偏差 |
| KV rollback | "undo rejected drafts" | Bookkeeping that resets the verifier's KV cache to the accepted-prefix length after a rejection | KV 回滚，拒绝后重置 KV 缓存到已接受前缀长度 |
| Bonus token | "the free one" | When all `N` drafts accept, sample one extra from `q_{N+1}` at no additional verifier cost | 奖励 token，全部接受时免费多生成一个 |
| Tree attention | "verify many candidates at once" | Attention with a non-causal mask that respects the topology of a draft tree; computes `q_i` for every node in the tree in one forward pass | 树注意力，一次前向传播验证多个候选 |

## Daha fazla okumak

- [Leviathan, Kalman, Matias — Fast Inference from Transformers via Speculative Decoding (arXiv:2211.17192, ICML 2023)](https://arxiv.org/abs/2211.17192) Temel Kağıt ve Dönüşüm Teoremi
- [Chen et al. — Accelerating Large Language Model Decoding with Speculative Sampling (arXiv:2302.01318)](https://arxiv.org/abs/2302.01318) Temiz bir kanıt ile eş zamanlı bağımsız giriş
- [Li et al. — EAGLE: Speculative Sampling Requires Rethinking Feature Uncertainty (arXiv:2401.15077)](https://arxiv.org/abs/2401.15077) EAGLE-1, gizli devlet koşullu taslak
- [Li et al. — EAGLE-2: Faster Inference of Language Models with Dynamic Draft Trees (arXiv:2406.16858)](https://arxiv.org/abs/2406.16858) dinamik ağaç arama
- [Li et al. — EAGLE-3: Scaling up Inference Acceleration via Training-Time Test (arXiv:2503.01840, NeurIPS 2025)](https://arxiv.org/abs/2503.01840) 2026 üretim default
- [Cai et al. — Medusa: Multiple Decoding Heads (arXiv:2401.10774)](https://arxiv.org/abs/2401.10774) Alternatif taslaksız yaklaşım
- [vLLM Speculative Decoding documentation](https://docs.vllm.ai/en/latest/features/spec_decode.html) Tüm stratejilerle bağlantılı olarak kanonik üretim referansı
