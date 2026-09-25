# ASCII Sanat ve Görsel Hapishane Çıkışları

> Jiang, Xu, Niu, Xiang, Ramasubramanian, Li, Poovendran, "ArtPrompt: ASCII Art tabanlı Ceilbreak Attacks against Alligned LLMs" (ACL 2024, arXiv:2402.11753). Güvenlik ile ilgili belirtileri zararlı bir talepte gizleyin, aynı harflerin ASCII sanatı gösterileri ile değiştirin ve gizlenmiş bir istek gönderin. GPT-3.5, GPT-4, Gemini, Claude, Llama-2 hepsi ASCII sanatı simgelerini güçlü bir şekilde tanımamaktadır. Saldırı PPL (kafas karışıklığı filtreleri), Parafraze savunmaları ve Retokenizasyon'u atlıyor. İlgili: ViTC referans ölçüsü semantik olmayan görsel isteklerin tanınmasını ölçer; StructuralSleight, kodlama saldırıları ailesi olarak Usual Metin Kodlanmış Yapılara (ağaçlar, grafikler, yuvalanmış JSON) genelleştirir.

> **【中文解读】**Bu bölüm ASCII 艺术视觉越狱文本图形绕过安全过器的攻击技术──ArtPrompt(ACL 2024) iki adımlı saldırı:识别安全相关词, ASCII 艺术染替换──安全过器看无害的标点符号网格,模型看一个词──GPT-4、Gemini、Claude、Llama-2 全部失败,攻击成功率超过75%──

> **【拓展：ArtPrompt → 编码攻击家族】**标准防御 (困惑度过、释义、重新分词) ArtPrompt'te tamamen başarısız oldu, çünkü güvenlik 过器在令牌/语义级操作中, ArtPrompt ise görsel tanımlama seviyesi operasyonlarında.

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, ArtPrompt token-masking harness) | **语言:** Python（标准库，ArtPrompt token 掩码框架）
**Prerequisites:** Phase 18 · 12 (PAIR), Phase 18 · 13 (MSJ) | **前置知识:** Phase 18 · 12 (PAIR), Phase 18 · 13 (MSJ)
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**Öğrenci bölümün önüne:Fase 18·12-13──视觉越狱 = 用 ASCII 艺术/树状图/JSON 等编码攻击绕过文本过器──
>  **【类比】**ASCII 越狱 = "隐形墨水"。安全过器看无害的标点网格,模型视觉理解为一个词。ArtPrompt ACL 2024:GPT-4/Gemini/Claude/Llama-2 全失败,>75% 攻击成功率──绕过PPL 过、改写、重代币 化防御──结构性变种(StructuralSleight) 扩展到树/图/嵌套 JSON所有非语义视觉提示都是攻击面──

## Öğrenme hedefleri

- ArtPrompt saldırısını açıklayın: kelime tanımlama adım, ASCII-art değiştirme, son gizlenmiş istek.

> 描述 ArtPrompt 攻击:词识别步骤、ASCII 艺术替换、最终伪装提示──

- Standart savunmaların (PPL, Parafraze, Retokenization) ArtPrompt'te neden başarısız olduğunu açıklayın.

> 解释为什么标准防御 (困惑度过、释义、重新分词) 在 ArtPrompt 上失败──

- ViTC'yi tanımlayın ve ölçümlerini açıklayın.

> 定義 ViTC并描述其衡量的内容──

- StructuralSleight'ı keyfi olmayan Uygulanabilir Metin Kodlanmış Yapılara genelleştirme olarak tanımlayın.

> 描述 StructuralSleight 作为任意罕见文本编码结构的推广──

## Sorun . Sorun .

Parafrase ve rol oynaması (Daahi 12) ve uzun bağlam (Daahi 13) yoluyla saldırılar metin düzeyde bir patern üzerinde çalışır. ArtPrompt tanıma düzeyinde çalışır: model yasaklı jetonu analiz etmez.

> 通过释义和角色扮演(Lesson 12) 和长上下文(Lesson 13) 的攻击在文本级模式上操作──ArtPrompt在识别级操作:模型不解析禁止令牌,而是解析以字符染的图像──安全过器看无害的标点符号──模型看一个词──

## Konsep kavramı.

> **【中文解读】**ArtPrompt 两步攻击的细节:第一步给定有害请求,使用LLM 识别安全相关词(如"bomba"在"如何做炸弹"中);第二步将每个识别的词替换为其ASCII 艺术染(7x5 或 7x7 字符块形成字母形) ;;模型收到的是标点和空格网格,足够强大的模型可以识别为词;安全过器只看网格;;

### ArtPrompt, iki adım

Adım 1. Sözcük Tanımlama. Zararlı bir talebe göre saldırgan, güvenlikle ilgili kelimeleri tanımlamak için bir LLM kullanır (örneğin, "bomba nasıl yapılır"daki "bomba"). 

Adım 2. Gizli Çözüm Yükleme. Her tanımlanan kelimeyi ASCII sanatı gösterimiyle değiştirin (harf şeklini oluşturan 7x5 veya 7x7 karakter blokları). Modelle yeterli derecede yetenekli bir modelin kelime olarak tanıyabileceği noktalama ve boşluklar bir şebekesi gelir; güvenlik filtre sadece şebekesi görür.

Sonuç: GPT-4, Gemini, Claude, Llama-2, GPT-3.5 hepsi başarısız oldu.

> Sonuç:GPT-4、Gemini、Claude、Llama-2、GPT-3.5 全部失败──基准子集上攻击成功率75%以上──

> **【拓展：防御失败 → 多层安全启示】**困惑度过器失败是因为合法结构化输入也得分高;释义失败是因为释义 LLM 常保留或重建 ASCII 艺术;重新分词失败是因为识别是视觉的而不是令牌级的──安全必须泛化到模型能解析的所有结构化表示

### Standart savunma neden başarısız oluyor

- **PPL (perplexity filter).**ASCII sanatı yüksek karmaşıklığa sahiptir  ama tüm yeni girişler de aynıdır. ArtPrompt'i engelleyen eşiği seçimler de meşru yapılandırılmış girişleri engeller.

> **困惑度过滤。**ASCII 艺术 has high confusion  but all new 输入 is also the same                                                                                                                                                                                                                                                     

- **Paraphrase.**Promptu'nun parafrase edilmesi ASCII sanatını yok eder.

> **释义。**释义提示会破坏 ASCII 艺术── aslında, 释义 LLM 常常保留或重建艺术──

- **Retokenization.**Tokenleri farklı bir şekilde bölmek, modelin görmesinin harf şekillerini tanıdığını değiştirmez.

> **重新分词。**Bölümler birbiriyle bölünmez.

Temel sorun, güvenlik filtrelerinin token veya semantik düzeyde olmasıdır; ArtPrompt görsel tanıma düzeyinde çalışır.

> 根本问题是安全过器在令牌或语义级操作中;ArtPrompt在视觉识别级操作中.

> **【中文解读】**ViTC 基准:ArtPrompt'in etkinliği ile modelin görsel metin okuyabilme yeteneği ilişkili ViTC 准确率越高,ArtPrompt 越有效。

### ViTC referans değerini

Semantik olmayan görsel isteklerin tanınması. Modelin ASCII-art, wingdings ve diğer metin-semantik olmayan görsel içeriği okumayı ölçer. ArtPrompt'in etkinliği ViTC doğruluğu ile ilişkilidir: model görsel metni ne kadar iyi okursa ArtPrompt üzerinde o kadar iyi çalışır. Bu bir yetenek-güvenlik pazarlamasıdır.

> Non-selimice görsel önerilerinin tanımlanması. Ölçüm modeli okuma ASCII 艺术、Wingdings 和其他非文本语义视觉内容的能力──ArtPrompt'in etkinliği ViTC 准确率 ile ilişkili:模型读取视觉文本越好,ArtPrompt 效果越好──这是能力-安全权衡──

### YapısalSleight

ArtPrompt: Usual Metin Kodlanmış Yapılar (UTES) Genelleştirir. Ağaclar, grafikler, yuvalanmış JSON, CSV-in-JSON, farklı stil kod blokları.

> 推广 ArtPrompt:罕见文本编码结构(UTES) ――树、图、嵌套 JSON、JSON içindeki CSV、diff 风格代码块── Eğer bir yapı eğitim güvenlik verileri arasında nadir görülür ama çözülebilirse, zararlı içeriği gizleyebilir──

Savunma anlamı: modelin analiz edebileceği yapılandırılmış temsiller boyunca güvenlik genelleşmelidir.

> 防御启示: güvenlik tüm yapısal gösterilere genel hale gelmelidir.

### Görüntü-modallik analog

Görsel LLM'ler (GPT-5.2, Gemini 3 Pro, Claude Opus 4.5, Grok 4.1) saldırı yüzeyini genişletiyor.

> 视觉 LLM  saldırı yüzünü genişletti. Gerçek görüntülerin ArtPrompt 式 saldırısı ASCII 艺术 daha güçlüdür, çünkü görüntü kodlayıcıları daha zengin sinyaller üretir.

### Bu 18 fazaya uygun.

Ders 12-14 üç ortogonal saldırı vektörünü tanımlar: İteratif Düzeltme (PAIR), Konekst Uzunluğu (MSJ) ve Kodlama (ArtPrompt/StructuralSleight).15 ders model merkezli saldırılardan sistem sınırlı saldırılara (indirekt acil enjeksiyon) geçiyor.16 ders savunma araç tepkisini tanımlar.

> Ders 12-14  Three Right-Based Attacks 代改进 (PAR) 、上下文长度 (MSJ) 和编码 (Közet)  ArtPrompt/StructuralSleight (Sektör)  Ders 15

> **【拓展：视觉 LLM → 攻击面扩展】**视觉 LLM(GPT-5.2, Gemini 3 Pro, Claude Opus 4.5, Grok 4.1) saldırı yüzünü genişletti.

## Kullanın Kullanın
```figure
al-ascii-cloak
```

## Kullan

`code/main.py`ASCII-art gliflerle zararlı bir sorguda belirli kelimeleri gizleyebilir, gizlenmiş dizinin anahtar kelime filtresi geçmesini doğrulayabilir ve (veya seçeneği olarak) gizlenmiş dizinin basit bir tanıtıcı kullanarak tekrar şifreleyebilirsiniz.

> `code/main.py`构建一个玩具 ArtPrompt──你可以使用ASCII 艺术字形伪装有害查询中的特定词,验证伪装字符串通过关键词过,并(可选地)简单识别器解码──

## Gönderin.

Bu ders bize çok yararlı .`outputs/skill-encoding-audit.md`. Bir jailbreak savunma raporu göz önüne alındığında, kapsamlı kodlama saldırı aileleri (ASCII sanatı, base64, leet-speak, UTF-8 homoglif, UTES) ve her birini yakalayan savunma katmanı sayılır.

> 本课产 出 `outputs/skill-encoding-audit.md`❖ Hapishanenin savunma raporlarını, saldırı ailesinin kodlama ve her bir karşıtı savunma katmanının kapsamını listeler.

## Egzersizler.

1. Çık .`code/main.py`Gizli dizinin basit bir anahtar kelime filtreyi geçtiğini kontrol edin.

2. İkinci bir kodlama uygulayın: base64 aynı hedef kelime için. ArtPrompt ile filtre-önleme oranını ve kurtarma zorluğunu karşılaştırın.

3. Jiang et al. 2024 Bölüm 4.3 (beş model sonuçları) okuyun.

4. ASCII sanat şeklinde bölgeleri anında algılayan bir ön nesil savunma tasarlayın. Kanunlu kod, tablolar ve matematiksel notasyonda yanlış pozitif oranı ölçün.

5. StructuralSleight 10 kodlama yapısını listeler. 10'u ele alan genel bir savunma çizin ve savunulan bir istek için hesaplama maliyetini tahmin edin.

## Anahtar Terimler

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| ArtPrompt | "the ASCII-art attack" | Two-step jailbreak that masks safety words with ASCII-art renderings |
| Cloaking | "hide the word" | Replace a forbidden token with a visual representation the model reads but the filter does not |
| UTES | "uncommon structure" | Uncommon Text-Encoded Structure — tree, graph, nested JSON, etc. used to smuggle content |
| ViTC | "visual-text capability" | Benchmark for model's ability to read non-semantic visual encoding |
| Perplexity filter | "PPL defense" | Reject prompts with high perplexity; fails because legitimate structured input also scores high |
| Retokenization | "tokenizer shift defense" | Pre-process the prompt with a different tokenizer; fails because recognition is visual |
| Homoglyph | "lookalike characters" | Unicode characters that look identical to Latin letters; bypass substring checks |

## Daha fazla okumak

- [Jiang et al. — ArtPrompt (ACL 2024, arXiv:2402.11753)](https://arxiv.org/abs/2402.11753) ASCII-art jailbreak kağıdı
- [Li et al. — StructuralSleight (arXiv:2406.08754)](https://arxiv.org/abs/2406.08754) UTES genelleşimi
- [Chao et al. — PAIR (Lesson 12, arXiv:2310.08419)](https://arxiv.org/abs/2310.08419) Ek iteratif saldırı
- [Anil et al. — Many-shot Jailbreaking (Lesson 13)](https://www.anthropic.com/research/many-shot-jailbreaking) Ek uzunluk saldırısı
