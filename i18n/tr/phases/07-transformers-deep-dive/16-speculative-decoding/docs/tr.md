# Tahmin edici çözme  Özetleme, doğrulama, tekrarlama  Tahmin çözme  Tasarım 验证 重复

> Autoregressive dekodlama serilidir. Her token önceki birini bekler. Speküel dekodlama zinciri kırar: ucuz model N tokens taslaklar, pahalı model tüm N bir ileri geçiş doğruluyor.

> **【中文解读】**Küçük model hızlı bir şekilde seçkin belirtiler üretir, büyük model toplu verifikasyonu.

**Type:** Hands-on | **类型:** 动手
**Language:**Python .**语言:**Python
**Prerequisites:** Phase 7 · 07 (GPT Causal LM), Phase 7 · 12 (KV Cache & Flash Attention) | **前置知识:** Phase 7 · 07 (GPT Causal LM), Phase 7 · 12 (KV Cache & Flash Attention)
**Time:** ~60 minutes | **时间:** ~60 分钟

## Sorunlar. Sorunlar.

Bir H100'de bir 70B LLM örneği örneği ~30 ms alır. Bir 3B taslak modeli ~3 ms alır. 3B taslak 5 tokeni ileri bırakırsak, tüm 5'i doğrulamak için 70B * bir kez * çalıştırın.`5×3 + 30 = 45 ms`5 tane kadar kabul edilen token için  vs `5×30 = 150 ms`Bu tam spekülasyonsal dekodlama alanı: 24x daha düşük dekod gecikmesi için küçük miktarda ekstra GPU belleği (yazar model) değiştirin.

> Bir 70B LLM Şablon bir token H100'de yaklaşık 30 ms gerekir。 bir 3B taslak modeli yaklaşık 3 ms gerekir。 eğer 3B'ye 5 token üretmesini önersek, sonra 70B * bir kez * test ederek hepsini 5 tane, total time for `5×3 + 30 = 45 ms`En fazla 5 tane kabul edilen token elde etmek için doğrudan üretilmelidir.`5×30 = 150 ms`︎ Bu, tüm satış noktasıdır: az miktarda ek GPU 内存 ile değiştirmek için 2-4 倍 daha düşük çözümü geciktirmek için.

Leviathan et al. (2023) ve Chen et al. tarafından aynı anda getirilen spekülasyonlu örnekleme, çıkış sırasının **identically distributed**Bu büyük model kendi başına üretebildiği şey için.

> Bu teknik değişmez bir dağılım sürdürmelidir. Leviathan  et al. 2023) ve Chen  et al. tarafından aynı anda başlatılmış, çıkış dizisi ile büyük modelin kendi kendine üretilen dağılımını garanti eden bir teknik olarak kullanılmaktadır.**完全相同**                                                                                                                                                                                                                                                              

4 çift çiftin ailesi 2026 sonucu üzerinde egemenlik göstermektedir:

> 4 sınıf taslak-temizleme cihazları 2026 yılının önerilerinde baskın konumlara sahip:

1. **Vanilla speculative (Leviathan 2023).**Ayrı taslak modeli (örneğin Llama 3 1B) + doğrulayıcı (örneğin Llama 3 70B).
   Çeviri:**朴素推测（Leviathan 2023）。**独立的草案模型(如 Llama 3 1B) + 验证器(如 Llama 3 70B) ⋅
2. **Medusa (Cai 2024).**Verifikatörde birden fazla dekodlama başlığı , tahmin pozisyonları `t+1..t+k`- Ayrı bir taslak modeli yok.
   Çeviri:**Medusa（Cai 2024）。**验证器 üzerinde bir çok çözünürlük ve tahmin konumları `t+1..t+k`无需独立草案模型──
3. **EAGLE family (Li 2024, 2025).**Verifikatörün gizli durumlarını tekrar kullanan hafif bir taslak; vanilya'dan daha yakın kabul oranı; tipik 34×.
   Çeviri:**EAGLE 系列（Li 2024, 2025）。**复用验证器隐藏状态的轻量草案; kabul oranı basit bir programdan daha yüksek; tipik hızlandırma 3-4 倍──
4. **Lookahead decoding (Fu 2024).**Jacobi iterasyonu, hiç bir taslak modeli gerekmiyor, kendi kendine spekülasyon yapılıyor, niş ama bağımlılıktan uzak.
   Çeviri:**前瞻解码（Fu 2024）。**Yacobi 代;完全不需要草案模型──自推测──小众但无依赖──

2026'da her üretim sonuçları varsayılan olarak spekülasyonsal çözümü gönderir. vLLM, TensorRT-LLM, SGLang ve llama.cpp hepsi en az vanilya + EAGLE-2 desteğini sağlar.

> 2026 yılının her üretim önerisi 都默认搭载推测解码──vLLM、TensorRT-LLM、SGLang 和 llama.cpp 都至少支持朴素 + EAGLE-2──

> **【中文解读】**推测解码的核心洞察:自归生成是串行瓶──用小模型(3B)快速生成 N 个候选符号,大模型(70B)一次前向传播验证所有 N 个──总时间从 N×30ms 降至 5×3+30=45ms,加速 2-4 倍──关键:推测采样保证输出分布与大模型完全一致,无质量损失──

> **【拓展：EAGLE 与 Medusa 的自推测策略】**EAGLE(2024) Büyük modelin gizli durumunu tekrar kullanarak taslak üretmek, kabul oranı bağımsız küçük modelden daha yüksek, tipik olarak 3-4 kat hızlandırılır. Medusa, büyük model üzerinde birden fazla çözünürlük ekliyor, aynı zamanda daha fazla gelecek konumunu tahmin ediyor, ek model gerekmiyor. Bu iki "kendini tahmin" stratejisi, bağımsız taslak modelinin satışını önledi ve 2026'da ana akım seçeneği haline geldi.

## Konsepten bir şey.

### Temel algoritma

Bir doğrulayıcı veriliyor `M_q`ve daha ucuz bir taslak .`M_p`- ...

> 给定验证器 `M_q`Daha ucuz bir taslak modeli`M_p`- ...

1. - Bırak .`x_1..x_k`- Bu, zaten çözülmüş bir önlemdir.
   Çeviri: 设`x_1..x_k`Çözülmüş bir öykü.
2. **Draft**: kullanımı `M_p`- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -`d_{k+1}, d_{k+2}, ..., d_{k+N}`- Evet .`p_1..p_N`- Evet .
   Çeviri:**草案**:用 `M_p`Özgürlük önerildi`d_{k+1}, d_{k+2}, ..., d_{k+N}`, 附带草案概率 `p_1..p_N`- Evet.
3. **Verify in parallel**Çıkış`M_q`Bir kere .`x_1..x_k, d_{k+1}, ..., d_{k+N}`, verifier olasılıklarını almak `q_1..q_{N+1}`pozisyonlar için `k+1..k+N+1`- Evet .
   Çeviri:**并行验证**:对 `x_1..x_k, d_{k+1}, ..., d_{k+N}`Bir kerelik .`M_q`, pozisyon almak`k+1..k+N+1`Testörlerin `q_1..q_{N+1}`- Evet.
4. **Accept/reject each draft token left to right**: her biri için`i`, olasılıklarla kabul et .`min(1, q_i(d_i) / p_i(d_i))`- Evet .
   Çeviri:**从左到右接受/拒绝每个草案 token**Herkese:`i`,                `min(1, q_i(d_i) / p_i(d_i))`Kabul ediyorum.
5. İlk reddedilme konusunda pozisyon .`j`Örnek:`t_j`"Kalan" dağıtımından `(q_j - p_j)_+`Tüm taslaklar normalleştirildi.`j`Atılır.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`j`İlk kez reddedildiğinde: "Şeyriyet" dağıtımından`(q_j - p_j)_+`归一化后采样 `t_j`- Evet.`j`Sonra tüm taslaklar atıldı.
6. Her şeyi kabul etmekle .`N`: örnek bir ekstra token `t_{N+1}`-`q_{N+1}`(Buna karşılık bonus simgesi)
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`N`个都被接受时: 个`q_{N+1}`采样一个额外的标志 `t_{N+1}`(gratis ödül simgesi)

Geri kalan dağılım hilesi , çıkışın tam olarak dağılmasını sağlayan matematiksel bir anlayıştır .`M_q`- İlk defa örnek almıştım.

> Geride kalan fark dağılım teknikleri, çıkış dağılımını ve `M_q`Bu da bir matematik açısından tamamen aynı.

### Hızlandırmayı belirleyenler

- Bırak .`α`= proje token başına beklenen kabul oranı.`c`= taslak ve denetleyiciler arasındaki maliyet oranı.

> 设 `α`= Her taslak simgesi'nin öngörülen kabul oranı¬¬`c`= Draft ve verifiyeci maliyet oranı:

- Saçma nesil, her token için bir büyük model çağrısı yapar.
  Çinçe Çevirim: 朴素生成每个代币 调用一次大模型──
- Spekülatör , her gün 1 büyük model çağrısı yapıyor .`(1 - α^{N+1}) / (1 - α) ≈ 1/(1-α)`Tokenler ne zaman`α`- Yüksek.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`α`较高时,每 `(1 - α^{N+1}) / (1 - α) ≈ 1/(1-α)`Bir tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane tane

Tipik bir kural .`α = 0.75`ve `N = 5`Bu yüzden, bu bir şey değil.

> `α = 0.75`和 `N = 5`时的典型经验法则:大模型调用减少3倍――草案成本是5倍便宜――实际总时间下降约2.5倍――

> **【中文解读】**加速效果取決於接受率 alpha──当 alpha=0.75、草案长度 N=5 时,大模型调用──残差分布──残差分布──残差分布──残差分布──残差分布──残差分布──残差分布──残差分布──残差分布──残差分布──残差分布──残差分布──残差分布──残差分布──残差分布──残差分布──残差分布──残差分布──残差分布──残差分布──残差分布──残差分布──残差分布──残差分布──残差分布──残差分布──残差分布──残差分布──残差分布──残差分布──残差分布──残差分布──残差分布──残差分布──残差分布──残差分布──残差分布──残差分布──残差分布──残差分布──残差分布──残差分布──残差分布──残差分布──残差−残差−残差−残差−残差−残差−残差−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−

**α depends on:**

> **α 取决于：**

- Aynı aile / aynı eğitim verileri α önemli ölçüde artırır.
  Çinçe Çevirimiçi:Drafta test cihazı yakınlık derecesi
- Açgözlü verifikatör karşısında açgözlü taslak: yüksek α. Temperatür örneği: eşleşmesi zor; kabul düşüyor.
  Çinçe Çevirimiçi:解码策略──贪心草案对贪心验证器:高 α──温度采样:更难匹配;接受率下降──
- Görev türü: Kod ve yapılandırılmış çıkış daha fazla (görünülebilir) kabul eder; serbest biçimdeki yaratıcı yazım daha az kabul eder.
  Çinçe çevirisi: görev tipi──代码和结构化输出接受更多(可预测);自由形式创意写作接受更少──

### Medusa  bir taslak modeli olmayan taslaklar

Medusa, taslak modelini verifikatörde ekstra çıkış başlıklarıyla değiştirir.`t`- ...

> Medusa, test cihazındaki ekstra çıkış başı değiştirme tasarılarını kullanıyor.`t`- ...

```
shared trunk → hidden h_t
    ├── head_0: predict token at t+1  (standard LM head)
    ├── head_1: predict token at t+2
    ├── head_2: predict token at t+3
    ├── head_3: predict token at t+4
```

Her baş kendi logitlerini çıkarır. Sonuç olarak, aday dizisini almak için her baştan örnek alırsınız, sonra tüm aday devamlarını bir anda göz önünde bulundurarak bir ağaç dikkat skeması kullanarak bir ileri geçişle doğrulayın.

> Her baş kendi loglarını çıkarır. Öneriler, her baştan örnek alınarak aday serisi elde eder, sonra da tüm adayları ele alırken, bir kez daha bir kez önde yayılma programı kullanır.

Avantajlar: ikinci bir model yok. Eksiler: eğitimli parametreler ekler; denetimli ince ayarlama aşamasına ihtiyaç duyar (~ 1B jetonlar); kabul oranı iyi bir taslakla vanilya spekülasyonundan biraz daha düşüktür.

> 优点:无需第二模型──缺点:增加可训练参数;需要监督微调阶段(约1B token);接受率比好的草案模型的朴素推测略低──

> **【拓展：推测解码在 vLLM 中的实现】**vLLM 2026 yılının en popüler LLM 推理框架,原生支持推测解码──它使用连续批处理(连续批处理) + PagedAttention + 推测解码的组合优化──在生产部署中,推测解码通常带来2-3倍的延迟降低,对于聊天场景的用户感知延迟敏感)尤为关键──结合量化(AWQ/GPTQ),单张GPU 上实现高性能推推──

### KİÇİN  gizli durumları yeniden kullanarak daha iyi bir çizim

EAGLE-1/2/3 (Li et al., 20242025) taslak modelini, doğrulayıcının son katman gizli durumlarını yudumlayan küçük bir transformatör (genellikle 1 katman) yapar.

> EAGLE-1/2/3 ((Li 等人,2024-2025) bir taslak modeli, genellikle 1 katlı) küçük bir transformatör olarak yapılır, test cihazının son katındaki gizli durum.

EAGLE-3 (2025) aday devamları üzerinde ağaç arama ekledi. vLLM ve SGLang gemisi EAGLE-2/3 Llama 3/4 ve Qwen 3 için varsayılan özellik yolu olarak.

> EAGLE-3(2025) için bir seçim yapma tarzı oluşturuldu.

### KV'nin dansı

Verifikasyon kaynakları `N`Tek ileri geçişle verifikatörün giriş simgelerini çiz. Bu verifikatörün KV önbelleğini `N`Bazı taslaklar reddedildiğinde, önbelleği kabul edilen önbellek uzunluğuna geri çevirmelisiniz.

> 验证在一次前向传播中将 `N`个草案代号 输入验证器──                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  `N`个条目── Eğer bazı taslağın reddedilmesi halinde, kabul edilen önce alınan süreye kadar kaydını geri çevirmelisin.

Üretim uygulamalar (vLLM'ler) `--speculative-model`Bu, ilk önce yaz, kabul üzerine karar ver.

> 生产实现(vLLM 的 `--speculative-model`、TensorRT-LLM'nin LookaheadDecoder) kullanmak için geçici KV 缓冲区

## Yapın.
```figure
draft-verify-tokens
```

## Yapın

Bakın .`code/main.py`Temel spekülatör örneği algoritmi (reddedme adım + kalan dağılım) uygulamamız:

> 参见 `code/main.py`△ Biz aşağıdaki bileşenlerle çekirdek önerme biçimlerini gerçekleştirdik:

- El kodlanmış bir dağılım üzerinde deterministik-yumuşak maksimum olan "büyük bir model" (böylelikle kabul matematikini analitik olarak doğrulayabiliriz).
  Çinçe Çevirimi: bir "büyük model",                                                                                                                                                                                                                                                        
- Büyük modelin bir rahatsızlığı olan bir "öntem modeli".
  Çinçe Çevirisi: bir "草案模型", is büyük模型的扰动版本──
- Doğrudan örnekleme ile aynı sınırlı dağılım üreten kabul / reddetme döngüsü.
  Çinçe Çevirisi: bir kabul/reddet döngüsü, doğrudan örnekle aynı kenar dağılım oluşur.

### Adım 1: reddetme adımı

```python
def accept_or_reject(q_prob, p_prob, draft_token, u):
    ratio = q_prob / p_prob if p_prob > 0 else float("inf")
    return u < min(1.0, ratio)
```

`u`- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ...`q_prob`verifiyeci tarafından hazırlanmış token için olasılık. `p_prob`Leviathan teoremi, Bernoulli'nin bu kararının ardından geri kalanı reddettikten sonra örnekleme yapılması, doğrulayıcının dağılımını tam olarak koruduğudur.

> `u`Evet, bu kadar.`q_prob`Yöntemli bir tasarı için bir tescilci.`p_prob`Leviathan teorisi, bu değerli kararın, bir delil örneğinden reddedilmesinin yanı sıra, tescilciye sahiplerin dağılmasını kesin olarak sağlayabileceğini göstermektedir.

### Adım 2: Geri kalan dağılım

```python
def residual_dist(q, p):
    raw = [max(0.0, qi - pi) for qi, pi in zip(q, p)]
    s = sum(raw)
    return [r / s for r in raw]
```

Kısalt `p`-`q`Bu değerleri sıfıra sıkıştırıp yeniden normalleştirir.

>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              `q`- Yeter .`p`, sıfır olarak kesilecek, yeniden birleştirilecektir.

### Adım 3: Bir spekülasyonsal adım

```python
def spec_step(prefix, q_model, p_model, N, rng):
    drafts = []
    p_probs = []
    ctx = list(prefix)
    for _ in range(N):
        p_dist = p_model(ctx)
        d = sample(p_dist, rng)
        drafts.append(d)
        p_probs.append(p_dist[d])
        ctx.append(d)

    q_dists = [q_model(prefix + drafts[:i]) for i in range(N + 1)]

    for i, d in enumerate(drafts):
        u = rng.random()
        q_prob = q_dists[i][d]
        p_prob = p_probs[i]
        if u < min(1.0, q_prob / p_prob if p_prob > 0 else float("inf")):
            prefix = prefix + [d]
        else:
            res = residual_dist(q_dists[i], p_model(prefix))
            prefix = prefix + [sample(res, rng)]
            return prefix
    prefix = prefix + [sample(q_dists[N], rng)]
    return prefix
```

Beş kabul edilmiş → bir bonus → altı token bir doğrulayıcı geçişinde üretilmiştir.

> 五个被接受 → 一个奖励 → 一次验证器通行产生六个代币──

### Adım 4: Kabul oranını ölç

10 bin spekülatör adım atmak, farklı tasamlı tasamlı tasamlı tasamlı tasamlı tasamlı tasamlı tasamlı tasamlı tasamlı tasamlı tasamlı tasamlı tasamlı tasamlı tasamlı tasamlı tasamlı tasamlı tasamlı tasamlı tasamlı tasamlı tasamlı tasamlı tasamlı tasamlı tasamlı tasamlı tasamlı tasamlı tasamlı tasamlı tasamlı tasamlı tasamlı tasamlı tasamlı tasamlı tasamlı tasamlı tasamlı tasamlı tasamlı tasamlı tasamlı tasamlı tasamlı tasamlı tasamlı tasamlı tasamlı tasamlı tasamlı tasamlı tasamlı tasamlı tasamlı tasamlı tasamlı tasamlı tasamlı tasamlı tasamlı tasamlı tasamlı tasamlı tasamlı tasamlı tasamlı tasamlı tasamlı tasamlı tasamlı tasamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlıamlı

> farklı taslak kalitesi seviyesinde çalıştırılır 10.000 kez önerme adımları.

### Adım 5: dağıtım eşdeğerliğini kontrol edin

Empirik olarak: spekülatör döngü tarafından üretilen simgelerin histogramı, doğrudan doğrulayıcıdan örnekleme ile üretilen histogramla eşleşmelidir. Bu pratikte Leviathan teoremi.

> 経験上: 推测循环'dan kaynaklanan simge doğrudan test cihazından alınmış gibi doğrudan doğru bir şekilde uyumlu olmalıdır.

## Çerçeveyi kullanın.

Üretim:

> 生产部署:

```bash
# vLLM with EAGLE
vllm serve meta-llama/Llama-3.1-70B-Instruct \
    --speculative-model /models/llama-3.1-eagle-70b \
    --speculative-draft-tensor-parallel-size 1 \
    --num-speculative-tokens 5

# vLLM with vanilla draft model
vllm serve meta-llama/Llama-3.1-70B-Instruct \
    --speculative-model meta-llama/Llama-3.2-1B-Instruct \
    --num-speculative-tokens 5
```

TensorRT-LLM'de 2026 ortalarında en hızlı Medusa yolu var.`faster-whisper`Whisper-large için spekülatörlü bir kodlama yaparak küçük bir taslakla kaplıyor.

> TensorRT-LLM 2026 yılının orta döneminde en hızlı Medusa 路径 sahip olacaktır.`faster-whisper`Şapşır-büyük 封装了推测解码,使用小草案模型──

**Picking a draft:**

> **选择草案策略：**

| Strategy | When to pick | Speedup |
|----------|--------------|---------|
| 策略 | 何时选择 | 加速比 |
| Vanilla draft (1B/3B Llama family) | Fast prototype, no training | 1.8–2.3× |
| 朴素草案（1B/3B Llama 系列） | 快速原型，无需训练 | 1.8–2.3× |
| Medusa heads | You can fine-tune the verifier | 2–3× |
| Medusa 头 | 可以微调验证器 | 2–3× |
| EAGLE-2 / 3 | Production, max speed | 3–4× |
| EAGLE-2 / 3 | 生产环境，最大速度 | 3–4× |
| Lookahead | No draft, no training, no extra params | 1.3–1.6× |
| 前瞻 | 无草案，无训练，无额外参数 | 1.3–1.6× |

**When NOT to spec-decode:**

> **何时不使用推测解码：**

- Tek sıralama jenerasyonu 15 token.
  Çin Çeviri: 1-5 simge
- Çok yaratıcı / yüksek sıcaklık örneklemesi (α damlaları).
  Çinçe Çevirimi: Yüksek sıcaklıklı ︎
- Hatıra sınırlı dağıtımlar (önzet modeli VRAM ekler).
  Çinçe Çevirimiçi:内存受限的部署 (内存受限的部署)

## İndirin . Ürünler .

Bakın .`outputs/skill-spec-decode-picker.md`. Yetenek yeni bir sonucu oluşturmak için spekülatör bir çözme stratejisi (vanil / Medusa / EAGLE / lookahead) ve ayarlama parametreleri (N, taslak sıcaklık) seçer.

> 参见 `outputs/skill-spec-decode-picker.md`△ Bu beceri yeni bir önerme için △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △    △ △                       

## Egzersizler.

1. **Easy.**Çık .`code/main.py`. Spekülatör token dağıtımının, verifikatörün p = 0.05 çerez içinde 50.000 token üzerinde doğrudan örnek dağıtımına uygun olduğunu onaylayın.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`code/main.py`❖ 50.000 token üzerinde doğrulanır, tescil token dağıtımı ve tescilere doğrudan örnek verileyici tarafından test edilen kartlarda paylaşılan p > 0.05 içinde uyumlu olarak
2. **Medium.** fonksiyonu olarak plan hızlandırılması (büyük model için tokens)`N`için`α = 0.5, 0.7, 0.85`- En iyi olanı belirle`N`(Tip: Verify call başına beklenen token = `(1 - α^{N+1}) / (1 - α)`.)
   Çizgi dilinde`α = 0.5, 0.7, 0.85`时加速比(每次大模型前向的符号数) 与`N`                                                                                                                                                                                                                                                              `N`△                                                                                                                                                                                                                                                              `(1 - α^{N+1}) / (1 - α)`◊)
3. **Hard.**Küçük bir Medusa uygulayın: 14. dersten alın GPT, t+2, t+3, t+4 pozisyonlarını tahmin eden 3 ekstra LM başını ekleyin.
   Çin dilinde: implement a小型 Medusa:取第14 课的 GPT毕业项目,添加3 额外的 LM 头预测位置 t+2、t+3、t+4──用联合多头损失在小小小小小小小小小小小中学上训练──与截断相同模型得到的简单草案的接受率──
4. **Hard.**Geri dönüşü uygulayın: 10 token ön harf KV ön harfinden başlayarak, 5 taslak belirticiyi besleyin, 3. pozisyonda bir reddedmeyi simüle edin. Ön harfinizin okumalarının bir sonraki iterasyonda "ön harf + ilk 2 kabul edilen taslak" ile doğru eşleştiklerini kontrol edin.
   Çinçe Çevirimi:实现回滚:从 10 token 的前 KV 缓存开始,输入 5 个草案代币,模拟位置 3 的拒绝――验证你的缓存读取在下次代时正确匹配"前 + 前 2 个已接受草案"――

## Anahtar Şartlar .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Draft model | "The cheap one" | A smaller model that proposes candidate tokens; usually 10–50× cheaper than the verifier. |
| 草案模型 | "便宜的那个" | 提出候选 token 的较小模型；通常比验证器便宜 10-50 倍。 |
| Verifier | "The big one" | The target model whose distribution we preserve; runs once per speculative step. |
| 验证器 | "大的那个" | 我们要保持其分布的目标模型；每次推测步骤运行一次。 |
| Acceptance rate (α) | "How often the draft is right" | Per-token probability that the verifier accepts the draft. 0.7–0.9 typical. |
| 接受率 (α) | "草案正确的频率" | 验证器接受草案的每 token 概率。典型值 0.7-0.9。 |
| Residual distribution | "The rejection fallback" | `(q - p)_+` normalized; sampling from this on rejection preserves the verifier's distribution. |
| 残差分布 | "拒绝时的后备方案" | `(q - p)_+` 归一化；拒绝时从中采样保持验证器的分布。 |
| Bonus token | "The free one" | When all N drafts accepted, sample one more from the verifier's next-step distribution. |
| 奖励 token | "免费的那个" | 当所有 N 个草案被接受时，从验证器的下一步分布中多采样一个。 |
| Medusa | "Draft-less speculative" | Multiple LM heads on the verifier predict positions t+1..t+k in parallel. |
| Medusa | "无草案推测" | 验证器上的多个 LM 头并行预测位置 t+1..t+k。 |
| EAGLE | "Hidden-state draft" | Tiny transformer draft conditioned on the verifier's last-layer hidden states. |
| EAGLE | "隐藏状态草案" | 以验证器最后一层隐藏状态为条件的小型 Transformer 草案。 |
| Lookahead decoding | "Jacobi iteration" | Self-speculation using a fixed-point iteration; no draft model. |
| 前瞻解码 | "Jacobi 迭代" | 使用不动点迭代的自推测；无需草案模型。 |
| Tree attention | "Verify many candidates at once" | Branching verification that considers several draft continuations simultaneously. |
| 树注意力 | "同时验证多个候选" | 同时考虑多个草案续写的分支验证。 |
| KV rollback | "Undo rejected drafts" | Scratch KV buffer; commit on acceptance, discard on reject. |
| KV 回滚 | "撤销被拒绝的草案" | 临时 KV 缓冲区；接受时提交，拒绝时丢弃。 |

## Daha fazla okumak

- [Leviathan, Kalman, Matias (2023). Fast Inference from Transformers via Speculative Decoding](https://arxiv.org/abs/2211.17192) çekirdek algoritması ve eşdeğerlik teoremi.
  Çinçe çevirisi:推测解码的核心算法和等价定理论文──
- [Chen et al. (2023). Accelerating Large Language Model Decoding with Speculative Sampling](https://arxiv.org/abs/2302.01318) eş zamanlı giriş; Bernoulli reddetme kanıtı temiz.
  Çin Çeviri: Şimdiki Zamanda Yayımlanan Tahminler; Açıkça Görüldü
- [Cai et al. (2024). Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads](https://arxiv.org/abs/2401.10774) Medusa kağıdı; ağaçlara dikkatle bakım.
  Çeviri: Medusa 论文;树注意力验证。
- [Li et al. (2024). EAGLE: Speculative Sampling Requires Rethinking Feature Uncertainty](https://arxiv.org/abs/2401.15077) EAGLE-1; gizli devlet koşullu taslak.
  Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Ç Ç Ç Ç Ç Ç Ç Ç Ç Çov
- [Li et al. (2024). EAGLE-2: Faster Inference of Language Models with Dynamic Draft Trees](https://arxiv.org/abs/2406.16858) Eagle-2; dinamik ağaç derinliği.
  Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri Çeviri:Çeviri Çeviri:Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çov Çov Çov Çov Çov Çoviki Çoviki Çoviki Çoviki Çoviki Çoviki Çoviki Çoviki Çoviki Çoviki Çoviki Çoviki Çoviki Çoviki Çoviki Çoviki Çoviki Çoviki Çoviki Çoviki Çoviki Çoviki Çoviki Çoviki Çoviki Çov
- [Li et al. (2025). EAGLE-3: Scaling up Inference Acceleration of Large Language Models via Training-Time Test](https://arxiv.org/abs/2503.01840)- Eagle-3.
  Çeviri:Çevre 3
- [Fu et al. (2024). Break the Sequential Dependency of LLM Inference Using Lookahead Decoding](https://arxiv.org/abs/2402.02057)- Göz önüne bak, taslaksız yaklaşım.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri
- [vLLM docs — Speculative Decoding](https://docs.vllm.ai/en/latest/features/spec_decode.html) dört stratejinin de bağlantılı olarak kanonik üretim referansı.
  Çinçe Çevirimiçi:vLLM 推测解码文档,四种策略的生产参考──
- [SafeAILab / EAGLE reference implementation](https://github.com/SafeAILab/EAGLE) EAGLE-1/2/3 için referans kodu.
  Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:Çeviri:ÇÇÇÇÇÇÇÇÇÇÇÇÇirÇirÇirÇirÇirÇirÇirÇirÇirÇirÇirÇirÇirÇirÇirÇirÇirÇirÇirÇirÇirÇirÇirÇirÇirÇirÇirÇirÇirÇirÇirÇirÇirÇirÇirÇirÇ ki ki ki ki ki ki ki ki ki ki ki ki ki ki ki ki ki ki ki ki ki ki ki ki ki ki ki ki ki ki ki ki ki ki ki ki ki ki ki ki ki ki ki ki ki ki ki ki ki ki ki ki ki ki ki ki ki ki ki ki ki ki ki ki ki ki ki ki ki ki ki ki ki ki ki ki ki ki ki ki ki ki ki ki ki
