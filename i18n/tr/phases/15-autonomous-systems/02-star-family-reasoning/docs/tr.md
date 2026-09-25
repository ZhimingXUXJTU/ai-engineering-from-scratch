# STAR, V-STAR, Silenç STAR  Kendine Öğretilmiş Dönüşüm

> En küçük kendi kendini geliştirme döngüsü mantık içinde yer alır. Bir model bir düşünce zinciri oluşturur, doğru cevaplara ulaşanları tutar ve bu cevaplara ince ayarlar verir. Bu STAR. V-STaR bir doğrulama ekler, böylece sonuçlama zaman seçimi daha iyidir. Sessiz-STAR mantıkları her noktaya doğru yönlendirir. Üçü de çalışıyor. Bunlardan hiçbiri sihirli değil. Bu sarmalık doğru cevaba ulaşmak için herhangi bir kısayolunu korur.

> **【中文解读】**En küçük kendi kendini geliştirme döngüsü düşünme sürecinde gizlenir: model oluşturur düşünce zinciri, doğru cevapların düşünme sürecini korur, bu veriler üzerinde küçük düzenler yapar. İşte STaR。V-STaR 添加验证器改善推理时选择。Stille-STaR, düşünceyi her bir noktaya kadar çözecek。

> **【拓展：STaR → OpenAI o1/o3 的自我改进】**STaR 系列, "Özünü Boşaltma" eğitimin temel düşünce biçimidir. Bu, kendi düşüncelerini kullanarak kendini eğitmek için kullanılan bir yöntemdir. Bu, AI'nin kendi kendini geliştirme anahtar teknolojisidir.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, bootstrap-loop simulator) | **语言:** Python (标准库，bootstrap 循环模拟器)
**Prerequisites:** Phase 13 · 01-03 (Reasoning and CoT), Phase 15 · 01 (long-horizon framing) | **前置知识:** Phase 13 · 01-03（推理与 CoT），Phase 15 · 01（长程框架）
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**Öğrenci bölümünün ilk aşamasında:Fase 13·01-03(CoT 思维链)、Fase 11·08(SFT 监督微调)、Fase 15·01(长程 代理框架)。STaR "自蒸 + 推理增强"ın en küçük kapalı döngüsüdür。
>  **【类比】**STaR = "öğrenci kendi kendini eleştirir"──普通学习 = 老师改作业学生订正(人工标注推理过程);STaR = 学生写推理→对答案→对对的推理保留并自我再练一遍(自我生成训练数据)──问题是:有时推理过程是错误的但答案巧合对对对对对对对对对对对,STaR 会强化这种"蒙对"的推理V-STaR 加一个法官验证器) 掉错推理
> ️ **【易错点】**STaR  eğitim zamanı sadece " cevap doğru mu " olacak mı " güçlendirilmesi " yolculuk düşüncesi "                                                                                                                                                                                                                                                  

## Sorunlar, sorunlar, sorunlar, sorunlar.

Bir modelin akıl yürütmesini öğretmenin en kolay yolu, insan tarafından yazılmış akıl yürütme izlerini toplamak.

> Model düşüncesinin doğrudan yolu, insan yazısının düşünce tarzı toplamak. Bu hem pahalı hem de yavaş, aynı zamanda insanların yazma isteğiyle sınırlıdır.

STaR (Self-Teught Reasoner, Zelikman et al., 2022) soruyor: model kendi mantıklılıklarını yazarsa ve bilinen cevaplara göre sınıflandırırsa ne olur?

> STaR(self teaching推理器,Zelikman 等人,2022) önerdi: Eğer model kendi kendini yazarsa推理 süreci并与已知答案对照评分会怎么样?


> **【中文解读】**Star 家族推理技術 (STAR、Quiet-STaR、ReST、ReST-EM) 代式自我训练提升 LLM 推理能力──核心思想:让模型生成推理轨迹,过高质量轨迹,用这些轨迹微调模型,循环代── bu OpenAI o1/o3 系列和人类扩展思想的技术基础──

1. Bir mantık izini ve yanıtını örnekleyin.
2. Son cevabı doğruysa, izini tut.
3. - Saklı izleri inceleme.
4. Tekrar ediyorum.

GSM8K ve CommonsenseQA her ikisi de yeni insan notasyonu olmadan iyileşti. Ancak döngüde yerleşik bir önyargı vardır: doğru cevabı üreten herhangi bir mantık, mantıkın kendisinin sağlam olup olmadığından bağımsız olarak korunur. V-STaR (Hosseini et al., 2024) bunu öğrenilmiş bir doğrulayıcı ile düzeltir; Quiet-STaR (Zelikman et al., 2024) fikri iç mantıkları belirleyen genelleştirir.

> Bu, geçerlidir. GSM8K ve CommonsenseQA'nın yeni insan işaretleri olmadığı durumlarda yükseltilmesi vardır. Ancak döngüde bir içsel bir kayıp vardır: doğru cevaplar üreten herhangi bir düşünce süreci, düşünce kendiliğinden mantıklı olup olmadığından bağımsız olarak korunur.

## Konsepten bir şey.

### STaR: işe yarayanları başlat

Her eğitim sorunu üzerinde bir mantık artı cevap örnekleyin. Eğer cevap etiketle eşleşirse, (problemi, mantık, cevap) üçlü tutun. Modelli tutulan seti ince ayarlayın. Tekrarlayın.

> Her bir eğitim sorusunda, bir düşünce süreci örneği olarak bir düşünce süreci eklenmesi için bir temel modelden başlayarak, bir düşünce süreci ile bir cevap oluşturmak için bir eğitim süreci oluşturmak gerekir.

Bir dönüş önemli. Eğer model bir sorunu asla düzeltemezse, döngü üzerinde öğrenemez.**rationalization**Bu nedenle, modelin başarısız olduğu sorunlarda, doğru cevabı bir ipucu olarak enjekte edin ve modelin buna yol açan bir mantık oluşturması için tekrar teşvik edin.

> Bir anahtar dönüştürü. Eğer model bir soruya doğru cevap veremezse, döngü ondan öğrenemez.**合理化**Model başarısızlığı sorusu için, doğru cevaplar bir ipucu olarak enjekte edilir, yeniden ipucular modelin ortaya çıkmasına yönlendirilir. Bu cevapların düşünce süreci.

Başlangıç kağıdında (Zelikman et al., 2022) sonuç: GSM8K'de tekrarlanan STaR turları ile 5.8%'den 10.7%'ye kadar gelişmiş bir GPT-J temel modeli  yaklaşık 5 yüzde puan mutlak olarak                                                                                                                                                                                                                                   

> İlk makale sonuçları: Zelikman 等人,2022):GPT-J 基础模型通过合理化重复 STaR 轮次, GSM8K'de 5.8% 升升至10.7%约5个百分点的绝对升升.

### V-STaR: DPO ile bir doğrulayıcı eğit

STaR yanlış mantıklılıkları atıyor. Hosseini et al. (2024) bunları da veriler olarak gözlemledi: her çift (rational, "bu doğru mu") bir doğrulayıcıyı eğitebilir. Bir sıralamacı oluşturmak için hem doğru hem de yanlış çözümler üzerinde doğrudan tercih optimizasyonu kullanırlar.

> STaR                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           

Raporlanan delta: GSM8K ve MATH'de önceki kendi kendini geliştirme temellerinden +4 ila +17 yüzde puan, kazancın büyük kısmı, ek jeneratör ince ayarlamaları yerine sonuçlama zaman seçimi için doğrulayıcı kullanmaktan kaynaklanır.

> Rapor'un yükseltilmesi: GSM8K ve MATH'de öncekilerden +4 ila +17% oranında yükseltilmesi, büyük kısmı, ek üreticinin küçük düzeltmelerinden değil, önerilerde seçilen test cihazlarından gelir.

### Quiet-STaR: iç mantıklar per token

Zelikman et al. (2024) sordu: model sadece sorun ve cevap arasında değil, her simge pozisyonunda kısa bir iç mantık oluşturmayı öğrenirse ne olacak? Sessiz-STaR, bir modelin her tahmin edilen simge öncesi gizli bir "düşünce" yaymasını eğitir, sonra düşünce bilincinde tahminleri öğrenilmiş bir ağırlık aracılığıyla temel tahminle karıştırır.

> Zelikman 等人 2024) önerdi: Eğer model öğrenci her bir belirti konumunda sadece soru ve cevap arasında değil, kısa bir iç düşünce üretirse?Sisice-STAR  eğitim modeli her bir belirti belirti önceden gizli bir "düşünme" gönderir, sonra öğrenme gücü ile düşünme hakkı algılama tahmin ile temel çizgi tahmin karışımı olacaktır.

Sonuç: Mistral 7B GSM8K'de 5.9%'den 10.9%'a ve CommonsenseQA'da görev-özel ince ayarlama olmadan 36.3%'den 47.2%'e mutlak sıfır çekim iyileştirmeler elde etti.

> Sonuç: GSM8K'de Mistral 7B'nin sıfırdan sıfırdan sıfırdan sıfırdan sıfırdan sıfırdan sıfır yükseldi, %5.9'dan %10.9'a yükseldi, CommonsenseQA'da %36.3'den %47.2'ye yükseldi, görevlerin belirli bir şekilde düzenlenmesi gerekmedi.

### Üçü de neden güvenlik konusunda endişeli?

Üç yöntem de son cevabı gradient sinyali olarak kullanır. Kusurlu bir mantıklama yoluyla doğru cevaba ulaşan bir mantık  bir kısayol kullanmak, tahmin etmek veya genelleştirme olmayan bir kalıp kullanmak  olumlu bir şekilde güçlendirilir. Dağıtım içindeki sorunlarda kısayol çalışır. Dağıtım dışındaki sorunlarda sessizce kırılır.

> Üç yöntem son cevabı bir dereceli sinyal olarak kullanır. Kusurlu bir düşünce yoluyla doğru cevabı elde etme düşünce süreci.

V-STaR'in doğrulayıcısı, mantıklıları sıralamayı öğrenerek hafifletiyor, ancak doğrulayıcı aynı etiket seti üzerinde eğitilmiştir. Dürüst belirsizlikten çok iyi biçimlendirilmiş yanlış bir mantıklamayı tercih etmeyi öğrenebilir. Daha güvenli tasarım, (a) süreç denetimli ödül modelleri (sadece cevaplar değil, ödüller veren ara adımlar) ve (b) basit kısayolları kıran uzun süren OOD değerlendirme ile STaR tarzındaki verileri birleştirmektir.

> V-STaR'in onaylayıcıları, değerlendirmeyi sınıflandırmayı öğrenerek hafifletir, ancak onaylayıcılar aynı etiket kitlesinde eğitimlidir. İyi ama yanlış değerlendirme biçiminde tercih edilen belirsizlikleri öğrenir. Daha güvenli bir tasarım olarak STaR tarzı verilerini birleştirmek için tasarlanmıştır.

### Karşılaştırma

| Method | Training signal | Inference cost | Data waste | Known failure mode |
|---|---|---|---|---|
| 方法 | 训练信号 | 推理成本 | 数据浪费 | 已知失败模式 |
| STaR | keep (rationale, answer) if correct | 1x | discards all incorrect rationales | shortcut rationales |
| STaR | 正确时保留（推理，答案） | 1x | 丢弃所有不正确的推理 | 捷径推理 |
| STaR + rationalization | above + correct-answer hinted retries | 1x | less | rationalized rationales may be implausible |
| STaR + 合理化 | 上述 + 正确答案提示重试 | 1x | 较少 | 合理化的推理可能不可信 |
| V-STaR | STaR + DPO verifier from both classes | Nx (best-of-N) | minimal | verifier can reinforce confident wrongness |
| V-STaR | STaR + 两类 DPO 验证器 | Nx（N 中选优） | 最少 | 验证器可能强化自信的错误 |
| Quiet-STaR | per-token rationale + mixing weight | 1.5-3x | minimal | still answer-conditioned gradient |
| Quiet-STaR | 每 token 推理 + 混合权重 | 1.5-3x | 最少 | 仍是答案条件梯度 |

### 2026'da bu yerle bir olur.

STAR eski. Ama 2025-2026 yıllarında bu model her yerde tekrar ortaya çıkıyor. Denebilir matematik problemlerinde RL (DeepSeek-R1, Kimi-k1.5, o1) STaR'in cevap koşullu gradient sinyali, ölçeklendirilmiştir. İşlem ödül modelleri (Lightman et al., 2023; OpenAI'nin "Hatır adım doğrulayalım") süreç denetim altyapıdır. AlphaEvolve (Learning 3) bir etiket yerine bir program değerlendirici ile kod için STaR. Darwin Godel Makinesi (Denevi 4) ajan asfaltı için STaR'dir.

> STaR  çok eskiydi. Fakat bu model 2025-2026 yıllarında ortaya çıktı. RL ((DeepSeek-R1、Kimi-k1.5、o1) STaR'ın cevap koşul 梯度信号の拡大版──プロセス奖励モデル──Lightman 等人,2023;OpenAI'nin " adım adım denetimi") süreç denetimi için bir alternatif.

STaR'i anlamak tüm bu tıklamaları yapar. Bu en az yaşanabilir kendi kendini geliştirme döngüsü.

> Bu, en az yapılabilecek bir kendiliğinden gelişme döngüsü.

## Çerçeveyi kullanın.
```figure
reflection-loop
```

## Kullan

`code/main.py`Oyuncak bir aritmetik görevde simülasyonlu bir STaR döngüsü çalıştırır.

- Ne kadar doğru bir şekilde atışın üstündeki atışları aşırıyor.
  Çinçe Çevirisi: 准确率如何在bootstrap 轮次中升──
- Kısa yolu nasıl gizlice girer: Simülatörde doğru cevabı %40'da doğru bulur ama kötü bir şekilde genelleştirir.
  Çinçe çevirisi: 模拟器 nasıl 潜入 模拟器 模拟器 模拟器 模拟器 模拟器 模拟器 模拟器 模拟器 模拟器 模拟器 模拟器 模拟器 模拟器 模拟器 模拟器 模拟器 模拟器 模拟器 模拟器 模拟器 模拟器 模拟器 模拟器 模拟器 模拟器 模拟器 模拟器 模拟器 模拟器 模拟器 模拟器 模拟器 模拟器 模拟器 模拟器 模拟器 模拟器 模拟器 模拟器 模拟器 模拟器 模拟器 模拟器 模拟器 模拟器 模拟器 模拟器 模拟器 模拟器 模拟器 模拟器 模拟器 模拟器 模拟器 模拟器 模拟器 模拟器 器 器 器 器 器 器 器 器 器 器 器 器 器 器 器 器 器 器 器 器 器 器 器 器 器 器 器 器 器 器 器 器 器 器 器 器 器 器 器 器 器 器 器 器 器 器 器 器 器 器 器 器 器 器 器 器 器 器 器 器 器 器 器 器 器 器 器 器 器 
- Bir doğrulayıcı (V-STaR tarzı) sonuca çıkarmaya nasıl yardımcı olur, ancak eğitim sırasında kurulan kısayolları tam olarak kesemez.
  Çinçe Çevirimiçi:验证器 (V-STaR 风格) nasıl bir şekilde eğitim sırasında nasıl bir şekilde kurulabilir, ancak tam olarak kurulamaz.

## İndirin . Ürünler .

`outputs/skill-star-loop-reviewer.md`Bu, eğitimden önce önerilen kendi kendine akıl yürütme borusunu denetlemenize yardımcı olur.

> `outputs/skill-star-loop-reviewer.md` eğitimden önce kendi kendine öğretim önerisi için bir inceleme yapmanıza yardımcı olmak.

## Egzersizler.

1. Simülatörü çalıştırın. Kısa yolu frekansını sıfır, sonra da 0.4'e ayarlayın.
   Çinçe Çevirisi: İki çalışma arasında, iki çalışma arasında dahi bir ayrım oranı %90'a ulaşsa bile, ne kadar ayrım oranı vardır?

2. Simülatörde bir OOD testi ekleyin. Farklı bir dağılımdan sorunlar çizin ve hem dağılım içindeki hem de OOD setlerinde başlatılmış modeli değerlendirin. Boşluğu ölçün.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri

3. Sessiz-STaR kağıdı'nı okuyun (arXiv:2403.09629) Bölüm 3. "Düşünme sonu" simgesini ve karışım ağırlığı başını her biri üç cümle ile açıklayın.
   Çine dilinde: using 三句话分别解释"思考结束"token 和混合权重头──

4. STaR'ın doğru tutmak filtresini her mantıklı adımı bağımsız olarak ödüllendiren, süreçle denetlenen bir alternatifle karşılaştırın.
   Çinçe Çevirimiçi: 识别标注成本差异和质量差异──

5. Uygulan bir modelde kısayolların rasyonalleri yakalayacağı bir değerlendirme tasarlayın.
   Çinçe Çevirisi: STAR döngüsünü güçlendirmenin en basit yolunu kırmak gerekir.

## Anahtar Şartlar .

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| STaR | "Self-Taught Reasoner" | Fine-tune on model-generated rationales that land correct answers; repeat |
| STaR | "自我教学推理器" | 在模型生成的正确推理上微调；重复 |
| Rationalization | "Hinted retry" | Inject the correct answer and re-prompt for a rationale |
| 合理化 | "提示重试" | 注入正确答案重新提示推理 |
| V-STaR | "Verifier STaR" | DPO-train a verifier on both correct and incorrect rationales |
| V-STaR | "验证器 STaR" | DPO 训练验证器用于推理时选择 |
| Quiet-STaR | "Per-token rationales" | Generate hidden thoughts at every token position; mix with baseline |
| Quiet-STaR | "每 token 推理" | 在每个 token 位置生成隐藏思考；与基线预测混合 |
| Answer-conditioned gradient | "Outcome-based signal" | The training loop rewards final answers, not reasoning steps |
| 答案条件梯度 | "基于结果的信号" | 训练循环奖励最终答案，而非推理步骤 |
| Process reward model | "Step-level verifier" | Reward model trained on per-step correctness, not outcome |
| 过程奖励模型 | "步骤级验证器" | 在每步正确性上训练的奖励模型 |
| Shortcut rationale | "Right answer, wrong reasoning" | A rationale that reaches the label via a non-generalizing pattern |
| 捷径推理 | "正确答案，错误推理" | 通过不可泛化模式达到标签的推理 |

## Daha fazla okumak

- [Zelikman et al. (2022). STaR: Bootstrapping Reasoning With Reasoning](https://arxiv.org/abs/2203.14465)- Orijinal kağıt.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri
- [Hosseini et al. (2024). V-STaR: Training Verifiers for Self-Taught Reasoners](https://arxiv.org/abs/2402.06457) sonuç zaman seçimi için bir DPO doğrulayıcısı eklenir.
  Çinçe Çevirimi: 添加 DPO 验证器用于推理时选择。
- [Zelikman et al. (2024). Quiet-STaR: Language Models Can Teach Themselves to Think Before Speaking](https://arxiv.org/abs/2403.09629) iç ratsiyonlar.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Ç Ç Çev
- [Lightman et al. (2023). Let's Verify Step by Step](https://arxiv.org/abs/2305.20050) işlem ödül modelleri, alternatif gradient sinyali.
  Çinçe Çevirisi: süreç ödül modeli,替代梯度信号。
- [DeepSeek-R1 paper (arXiv:2501.12948)](https://arxiv.org/abs/2501.12948) Kontrol edilebilir görevler için RL, STaR sınır eğitimine kadar uzanmıştır.
  Çinçe Çevirisi: RL,STaR                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
