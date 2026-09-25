# Uzmanların Karışığı (MoE) 混合专家模型 (MoE)

> Dense 70B transformatörü her token için her parametreyi etkinleştirir. 671B MoE, her token için sadece 37B'yi etkinleştirir ve her referans markasında onu yenir.

> **【中文解读】**MoE sadece uzman ağının her token'ı işleme bölümünü aktifleştirir, büyük ölçüde işlem miktarını artırır ve hesaplama miktarını artırmaz.

**Type:** Hands-on | **类型:** 动手
**Language:**Python .**语言:**Python
**Prerequisites:** Phase 7 · 05 (Full Transformer), Phase 7 · 07 (GPT) | **前置知识:** Phase 7 · 05 (Full Transformer), Phase 7 · 07 (GPT)
**Time:** ~45 minutes | **时间:** ~45 分钟

## Sorunlar. Sorunlar.

Dense bir transformatörün FLOP'leri, parametre sayısının (geri geçiş için 2 kat) eşit olduğu sonucunda. Dense bir modeli ölçeklendirir ve her token tüm faturayı öder. 2024 yılına gelindiğinde sınır bir hesaplama duvarına çarpardı: anlamlı olarak daha akıllı olmak için, bir token için eksponensel olarak daha fazla FLOP'ye ihtiyacınız vardı.

> 密 推理时的FLOPs等于其参数(前向传播乘以2);;扩大密模型意味着每个代币都应支付全部代价;; 2024 yılına kadar,前沿模型遇到了计算墙:变得更聪明,需要指数级增长的每代币FLOPs;;

Uzmanlar karışımı bu bağlantıyı kırar.`E`bağımsız uzmanlar + seçen bir yönlendiricisi `k`Teknes başına uzmanlar.`E × FFN_size`. Token başına aktif parametreler = `k × FFN_size`.2026 tipi yapılandırma: `E=256`- Evet .`k=8`. depolama ölçekleri `E`, hesaplama ölçekleri ile `k`- Evet .

> Bu bağlantıyı kopardık. Her FFN'i değiştireceğiz.`E`个独立专家 + 一个路由器,每个代币 选择 `k`个专家──总参数 = `E × FFN_size`◊ Her bir simge'nin aktif parameter sayısı = `k × FFN_size`❖2026 yılının tipik konumu:`E=256`- Evet.`k=8`❖ Depolama`E`扩展,计算随 `k`扩展──

2026 sınır neredeyse tamamen MoE: DeepSeek-V3 (671B toplam / 37B aktif), Mixtral 8×22B, Qwen2.5-MoE, Llama 4, Kimi K2, gpt-oss. Yapay Analiz'in bağımsız liderlik tablosunda, en iyi 10 açık kaynaklı model tüm MoE.

> 2026 yılının ön kenarı neredeyse tamamen MoE:DeepSeek-V3(671B 总参数 / 37B 活跃) 、Mixtral 8×22B、Qwen2.5-MoE、Llama 4、Kimi K2、gpt-oss──

> **【中文解读】**MoE                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            

> **【拓展：DeepSeek-V3 的 MoE 创新】**DeepSeek-V3  671B  toplam parametreye sahip ama her token sadece 37B  256 路由专家 + 1 共享专家 aracılığıyla etkinleştirilmiştir. Ayrıca yardımcı kaybı olmayan yük denge stratejisini de tanıttı, geleneksel MoE'nin yol çöküşünün sorunlarını önledi.

## Konsepten bir şey.

![MoE layer: router selects k of E experts per token](../assets/moe.svg)

### FFN değişimi

Sıkı transformatör blokları:

> 密 Transformer 块:

```
h = x + attn(norm(x))
h = h + FFN(norm(h))
```

MoE blok:

```
h = x + attn(norm(x))
scores = router(norm(h))              # (N_tokens, E)
top_k = argmax_k(scores)              # pick k of E per token
h = h + sum_{e in top_k}(
        gate(scores[e]) * Expert_e(norm(h))
    )
```

Her uzman bağımsız bir FFN (genellikle SwiGLU) dir. yönlendiricisi tek bir doğrusal katman. Her token kendi seçer.`k`uzmanları ve çıkışlarını kapalı bir karışım alır.

> Her uzman bağımsız bir FFN (genellikle SwiGLU) ⋅ yönlendiricisi tek bir hattlı katman ⋅ her token  kendi seçimini yapmaktadır.`k`个专家, get them output control mix.

### Yük denge problemi

Eğer yönlendiriciler, %90'ı uzman 3'ün üzerinden gönderirse diğer uzmanlar aç kalır.

> Eğer router, %90'ı uzmanlara dağıtırsa diğer uzmanlar aç kalırsa, üç farklı çözüm programı denedi:

1. **Auxiliary load-balancing loss**(Switch Transformer, Mixtral). Uzman kullanımdaki değişikliğe göre bir ceza ekleyin. Çalışır, ancak bir hiperparametre ve ikinci bir gradient sinyali ekler.
   Çeviri:**辅助负载均衡损失**(Switch Transformer、Mixtral) ❖ Ek olarak uzmanların kullanım oranı oranında ❖ geçerli, ancak süper parametre ve ikinci derecede sinyaller ❖ artmıştır.
2. **Expert capacity + token dropping**(Erken Switch) Her uzman en fazla işlem yapar.`C × N/E`Tokenler, aşırı akış tokenleri katmanı atlar.
   Çeviri:**专家容量 + token 丢弃**(早期 Switch) ◊ her uzmanın en çok işlediği`C × N/E`个标志;溢出的标志 跳过该层――损害质量――
3. **Auxiliary-loss-free balancing**(DeepSeek-V3). Router'ın üst-k seçimini değiştiren bir uzman başına öğrenilen önyargıyı ekleyin.
   Çeviri:**辅助损失无关均衡**(DeepSeek-V3)──Add a learning to of the individual specialists biased, adjusting the top-k of the router 选择── biased in training loss beyond update──not against the main goal施加惩罚──2024 yılının büyük başarıları──

DeepSeek-V3'ün yaklaşımı: her eğitim aşamasından sonra, her uzman için, kullanımının hedefin üzerinde veya altında olup olmadığını kontrol edin.`±γ`Seçim kullanımı`scores + bias`- Kaplama için kullanılan uzman olasılıkları ,`scores`- Yollama ifadelerinden koparılmasını.

> DeepSeek-V3'ün yöntemi: Her antrenman aşamasından sonra, her uzmanın kullanımının hedefinden yüksek veya düşük olup olmadığını kontrol etmesi.`±γ`△ △ △ △ △ △ △ △`scores + bias`◊ Giriş kontrolü için kullanılan uzmanların olasılığı değişmemiş bir başlangıçtır.`scores`将路由与表达解──

### Ortak uzmanlar

DeepSeek-V2/V3 ayrıca uzmanları *shared* ve *routed* olarak bölüyor. Her token tüm ortak uzmanlardan geçer. Routed uzmanlar üst-k üzerinden seçilir. Ortak uzmanlar ortak bilgiyi yakalar; yönlendirilmiş uzmanlar uzmanlaşır. V3 1 ortak uzman artı 256 yönlendirilmiş üst-8'i çalışır.

> DeepSeek-V2/V3 ayrıca uzmanları* paylaşım* ve* yollardan* iki sınıf olarak bölüyor. Her bir token tüm paylaşım uzmanları tarafından geçer.

### Güzel tahıllardaki uzmanlar

Klasik MoE (GShard, Switch): her uzman, tam bir FFN kadar geniş. `E`küçük (864), `k`küçüktür (12).

> 经典 MoE(GShard、Switch):每个专家与完整FFN 一样宽──`E`较小(8-64),`k`较小(1-2)。

Modern ince tanelerli MoE (DeepSeek-V3, Qwen-MoE): her uzman daha dar (1/8 FFN boyut). `E`büyüktür (256+), `k`Aynı toplam parametreler, ancak kombinasyonlar daha hızlı ölçeklendirilir. `C(256, 8) = 400 trillion`- Kalite artıyor, gecikme sabit kalıyor.

> 现代细粒度 MoE(DeepSeek-V3、Qwen-MoE):每个专家更狭(1/8 FFN 大小) ⋅`E`较大(256+),`k`Aynı miktarda bile daha büyük, fakat daha hızlı bir şekilde büyüyor.`C(256, 8) = 400 万亿`种可能的专家组合──质量提升,延迟不变──

> **【拓展：MoE 的路由崩塌问题】**MoE  eğitiminin temel zorluğu ise yol yol çöküşüdür (router çöküşü) 路由器可能将大部分代币分配给少数专家,导致其他专家得不到训练――解决方案包括:辅助损失 (辅助损失) 辅助损失 (辅助损失) 鼓励均分配、噪声注入 (路由决策前加随机扰动) DeepSeek-V3 辅助损失无关负载均衡策略──

### Maliyet profili

Bir token, bir katman:

> Her bir simge, her bir kat:

| Config | Active params / token | Total params |
|--------|-----------------------|--------------|
| 配置 | 每个 token 活跃参数 | 总参数量 |
| Mixtral 8×22B | ~39B | 141B |
| Llama 3 70B (dense) | 70B | 70B |
| DeepSeek-V3 | 37B | 671B |
| Kimi K2 (MoE) | ~32B | 1T |

DeepSeek-V3 neredeyse her referans değerinde Llama 3 70B ' yi yener .**fewer active FLOPs per token**Daha fazla parametre = daha fazla bilgi. Daha aktif FLOPs = daha fazla hesaplama.

> DeepSeek-V3 neredeyse tüm testlerde Llama 3'yi 70B'ye yendi.**每个 token 的活跃 FLOPs 更少**△更多参数 = 更多知识──更多活跃 FLOPs = 更多计算── MoE 将两者解──

### Anlık: hafıza

Tüm uzmanlar, hangi birinden ateşlenmesine bakmaksızın GPU'da yaşarlar. 671B modeli fp16 ağırlıkları için ~ 1.3 TB VRAM gerektirir. Frontier MoE dağıtımı uzman paralellik gerektirir.

> Tüm uzmanlar, aktif olup olmadığına bakılmaksızın GPU'da bulunuyor. Bir 671B modeli yaklaşık 1.3TB'lik fp16 权重显存储ı gerektirir. Ön kenarında MoE'nin dağıtımında uzmanların bir çok GPU'ya bölünmesi gerekir.

> **【中文解读】**MoE'nin çekirdek ağırlığı:内存换计算──DeepSeek-V3 以 37B 活跃参数以70B 密模型性能超越的性能达到,但需要1.3TB 显存储所有专家──这推动专家并行(专家平行) 技术的发展专家将分散到多个GPU 上,通过网络路由代币──

> **【拓展：细粒度专家 vs 粗粒度专家】**传统 MoE(Switch Transformer) 少量大型专家 (E=8-64)。现代细粒度 MoE(DeepSeek-V3) 大量小型专家 (E=256+), her uzman sadece 1/8 FFN 宽度──组合数 C(256,8) 约为40000000000种,远超粗粒度的组合空间──质量提升显著,延迟基本不变──

## Yapın.
```figure
expert-routing
```

## Yapın

Bakın .`code/main.py`. Temiz bir stdlib'de kompakt bir MoE katmanı:

> 参见 `code/main.py`❖ Bir tek standartla gerçekleştirilen sıkı MoE katmanı, içerir:

- `n_experts=8`SwiGLU uzmanları (her biri çizgici, örneğe göre)
  Çeviri:`n_experts=8`个类 SwiGLU 专家( her bir 条线性层, gösterim için)
- üst k=2 yönlendirme
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Ç Çeviri Çeviri Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç
- Softmax normalleştirilmiş kaplama ağırlıkları
  Çinçe Çevirimi:softmax 归一化门控权重
- Uzmanlık önyargısı yoluyla yardımcı kayıpsız dengeleme
  Çinçe Çevirisi: Aşırı bir uzmanlık ayırma sonucu destek kaybı eşitsizliği

### Adım 1: Router

```python
def route(hidden, W_router, top_k, bias):
    scores = [sum(h * w for h, w in zip(hidden, W_router[e])) for e in range(len(W_router))]
    biased = [s + b for s, b in zip(scores, bias)]
    top_idx = sorted(range(len(biased)), key=lambda i: -biased[i])[:top_k]
    # softmax over ORIGINAL scores of the chosen experts
    chosen = [scores[i] for i in top_idx]
    m = max(chosen)
    exps = [math.exp(c - m) for c in chosen]
    s = sum(exps)
    gates = [e / s for e in exps]
    return top_idx, gates
```

Bu, DeepSeek-V3 numarasının  bias modeli tahminlerini yönlendirmeden yük dengesizliğini düzeltiyor.

> 偏置影响选择,不影响门控制权重――这是DeepSeek-V3'ün teknikleri偏置纠正负载不平衡,但不干预模型的预测──

### Adım 2: 100 tokeni yönlendiriciden çalıştır

Bilgi alanları hangi uzmanların ne sıklıkla ateş ettiğini takip et.`-γ`Aşırı kullanılmış uzmanlar için, `+γ`(ki) kullanımı birkaç tekrarla aynı bir dağılım halinde dönüşür.

> Follow hangi uzmanlar kaç kez aktifleştirildi.`-γ`, util insuficient of experts `+γ`), kullanım miktarı birkaç nesilde ortalama dağılımlara ulaşmıştır.

### Adım 3: Param sayı karşılaştırması

Bir MoE yapılandırmasının "sık eşdeğerini" yazdır. DeepSeek-V3- şeklinde: 256 yönlendirilmiş + 1 paylaşılan, 8 aktif, d_model=7168. Toplam parametreler sayısı gözleri aydınlatır.

> 印 MOE 配置的"密等价"──DeepSeek-V3 形:256 个路由 + 1 个共享,8 个活跃,d_model=7168──总参数令人惊叹──活跃参数数只有密 Llama 3 70B 的七分之一──

## Çerçeveyi kullanın.

HuggingFace yüklenmesi:

> Kucaklanmak Yüzü Üstü:

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
model = AutoModelForCausalLM.from_pretrained("mistralai/Mixtral-8x22B-v0.1")
```

2026 üretim sonucu: vLLM MoE yönlendirmeyi doğal olarak destekler. SGLang en hızlı uzman paralel yolu vardır.

> 2026 yıl üretim önerisi: vLLM 原生支持 MoE 路由──SGLang 拥有最快的专家并行路径──都自动处理 top-k 选择和专家并行──

**When to pick MoE:**
- Bir token için daha düşük bir sonuç fiyatı ile sınır kalitesi istiyorsunuz.
  Çin Çeviri:  You Wanna                                                                                                                                                                                                                                                          
- VRAM / uzman paralel altyapınız var.
  Çinçe Çevirisi:You have sufficient manifest survivor/专家并行基础设施──
- İş yükünüz token ağır (çat, kod) bağlam ağır (uzun belgeleri) değil.
  Çinçe Çevirimi: Senin iş yükümlülüğü, aşağıdaki yazıların yoğunluğunu değil, simgesel 密集型 (密集型) 长文档) ▽

**When NOT to pick MoE:**
- Kenar dağıtım  aktif FLOP için tam depolama ödüllendiriyorsunuz.
  Çin Çeviri: 边缘部署 支付全部储备
- Latency-critical single-user servis  uzman yönlendirme genel maliyet ekler.
  Çinçe Çevirisi:延迟敏感的单用户服务专家路由增加开销──
- Küçük modeller (<7B)  MoE'nin kalite avantajı sadece hesaplama eşiğinden (~6B aktif parametreler) ötesinde görülür.
  Çin dilinde:小模型 ((<7B) MoE'nin質量優勢僅在計算值以上 (約6B 活跃参数) 才出現──)

## İndirin . Ürünler .

Bakın .`outputs/skill-moe-configurator.md`. Yetenek yeni bir MOE için E, k ve ortak uzman düzenini seçer.

> 参见 `outputs/skill-moe-configurator.md` Bu beceri △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △             

## Egzersizler.

1. **Easy.**Çık .`code/main.py`Yardımcı kayıpsız önyargı güncelleme 50'den fazla iterasyonda uzman kullanımını nasıl düzeltiyor.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`code/main.py`◊ Observer yardımcı kaybı ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒     ⇒ ⇒   ⇒ ⇒ ⇒    ⇒       ⇒    ⇒               ⇒  ⇒                                                                                                                              
2. **Medium.**Öğrenilen yönlendiricini hash tabanlı yönlendiricilerle değiştirin (deterministik, öğrenme yok). Kaliteli ve dengeyi karşılaştırın. Öğrenilen yönlendiriciler neden daha iyidir?
   Çinçe çevirisi: Hashi'ye dayalı bir yolcu ile öğrenme biçimini değiştirmek için.
3. **Hard.**GRPO tarzında "rollout-matched routing" uygulamak (DeepSeek-V3.2 hilesi): akıl yürütme sırasında uzmanların ateşlediği kayıtları, gradient hesaplama sırasında aynı yönlendirmeyi zorlamak. Oyuncak politika-gradient ayarlama üzerindeki etkisini ölçmek.
   Çinçe çevirisi: GRPO 风格的实现"推演匹配路由" (GROPO 风格的推演匹配路由)  DeepSeek-V3.2 技巧): kaydet öneriler sırasında hangi uzmanlar aktif hale getirilmiş, 梯度計算時強制相同路由──; 梯度設定上測量效果──; 梯度計算時強制相同路由──; 梯度設定上測量效果──; 梯度計算時強制相同路由──; 梯度計算時強制相同路由──; 梯度設定時強制的過程──; 梯度計算時強制的過程──; 梯度計算時的過程──; 梯度計算時的過程──; 梯度計算時; 梯度計算時; 梯度計算時; 梯度設定時時時; 梯度設定時; 梯度設定時; 梯度設定時; 梯度設定時; 梯度設定時; 梯度設定時; 梯度設定時; 梯度設定時; 計算時; 計算時時; 計算時; 計算時時; 計算時; 計算時; 計算時; 計算時; 計算時; 計算時; 計算時; 計算時; 計算; 計算時; 計算; 計算; 計算; 計算; 計算; 計算; 計算; 計算; 計算; 計算; 計算; 計算; 計算; 計算; 計算; 計算; 計算; 計算; 計算; 計算; 計算; 計算; 計算; 計算; 計算;

## Anahtar Şartlar .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Expert | "One FFN among many" | An independent feed-forward network; parameters dedicated to a sparse slice of the FFN computation. |
| 专家 | "众多 FFN 之一" | 独立的前馈网络；专用于 FFN 计算的稀疏切片的参数。 |
| Router | "The gate" | A tiny linear layer that scores each token against each expert; top-k selection. |
| 路由器 | "门控" | 一个小线性层，对每个 token 与每个专家打分；top-k 选择。 |
| Top-k routing | "k active experts per token" | Each token's FFN computation goes through exactly k experts, weighted by gate. |
| Top-k 路由 | "每个 token 激活 k 个专家" | 每个 token 的 FFN 计算经过恰好 k 个专家，按门控加权。 |
| Auxiliary loss | "Load-balance penalty" | Extra loss term that penalizes skewed expert usage. |
| 辅助损失 | "负载均衡惩罚" | 惩罚专家使用不均衡的额外损失项。 |
| Auxiliary-loss-free | "DeepSeek-V3's trick" | Balance via per-expert bias on the router's selection only; no extra gradient. |
| 辅助损失无关 | "DeepSeek-V3 的技巧" | 仅通过路由器选择上的逐专家偏置实现均衡；无额外梯度。 |
| Shared expert | "Always on" | Extra expert through which every token passes; captures common knowledge. |
| 共享专家 | "始终开启" | 每个 token 都通过的额外专家；捕获通用知识。 |
| Expert parallelism | "Shard by expert" | Distribute different experts to different GPUs; route tokens across the network. |
| 专家并行 | "按专家分片" | 将不同专家分配到不同 GPU；通过网络路由 token。 |
| Sparsity | "Active params < total params" | The ratio `k × expert_size / (E × expert_size)`; 37/671 ≈ 5.5% for DeepSeek-V3. |
| 稀疏性 | "活跃参数 < 总参数" | 比率 `k × expert_size / (E × expert_size)`；DeepSeek-V3 为 37/671 ≈ 5.5%。 |

## Daha fazla okumak

- [Shazeer et al. (2017). Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer](https://arxiv.org/abs/1701.06538)- İdeya.
  Çeviri:Moz.
- [Fedus, Zoph, Shazeer (2022). Switch Transformer: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity](https://arxiv.org/abs/2101.03961) Switch, klasik MoE.
  Çıkış Transformer, klasik MoE 论文。
- [Jiang et al. (2024). Mixtral of Experts](https://arxiv.org/abs/2401.04088) Mixtral 8×7B.
  Çıkarıcı 8×7B 论文。
- [DeepSeek-AI (2024). DeepSeek-V3 Technical Report](https://arxiv.org/abs/2412.19437) MLA + yardımcı kayıpsız MoE + MTP.
  Çeviri:DeepSeek-V3 技术报告,MLA + 辅助损失无关 MoE + MTP。
- [Wang et al. (2024). Auxiliary-Loss-Free Load Balancing Strategy for Mixture-of-Experts](https://arxiv.org/abs/2408.15664) önyargılı dengeleme kağıdı.
  Çinçe Çevirisi: Değişikliklere dayalı dengeleme stratejisi
- [Dai et al. (2024). DeepSeekMoE: Towards Ultimate Expert Specialization in Mixture-of-Experts Language Models](https://arxiv.org/abs/2401.06066) ince taneler + paylaşım uzmanı bu ders için yönlendirme kullanımı bölüştürdü.
  Çeviri:DepSeekMoE 论文,细粒度 + 共享专家拆分──
- [Kim et al. (2022). DeepSpeed-MoE: Advancing Mixture-of-Experts Inference and Training](https://arxiv.org/abs/2201.05596) orijinal ortak uzman makalesi.
  Çeviri:DepSpeed-MoE
