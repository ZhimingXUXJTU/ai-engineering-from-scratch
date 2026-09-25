# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

> Ders 01 sana bir oyuncak verdi.

> **【中文解读】**İlk sınıf BPE oyuncak,本课构建生产级分词器:处理 Unicode、空白归归一化、特殊代币、字节级回退(让任何输入都能编码,包括emoji 和中文) ⋅

> **【拓展：tiktoken/HuggingFace】**GPT-4'in tiktokenleri ve Llama cümle parçaları üretim sınıfı sözcük makinelerinin gerçekleşmesidir.

>  **【前置】**学本节前 Lütfen önce bil:(1) Fase 10·01(Tokenizers: BPE/WordPiece/SentencePiece) BPE 合并循环和合并表的概念;(2) Unicode ve UTF-8 编码codepoint、字节、NFC/NFKC 归一化的区别;(3) 正则表达式特别是`\p{L}`- Evet.`\p{N}`、负向先行断言 `(?!\S)`;(4) Python `regex`库(standard değil `re`Çünkü ...`re`(→ Unicode özelliğini desteklemiyor)

**Type:** Build
**Languages:** Python
**Prerequisites:** Phase 10, Lesson 01 (Tokenizers: BPE, WordPiece, SentencePiece)
**Time:** ~90 minutes

## Öğrenme hedefleri

- Unicode, beyaz alan normallaştırımı ve özel tokenleri işleyen bir üretim derecesi BPE tokenizeri oluşturun
  构建处理 Unicode、空白归归归化和特殊代币的生产级 BPE 分词器
- Bayt seviyesindeki geri dönüşü uygulayın, böylece tokenizer bilinmeyen tokenler olmadan herhangi bir giriş (emoji, CJK ve kod da dahil) kodlayabilir
  实现字节级回退,分词器能编码任何输入(包括emoji、CJK、代码) 未知代码生成不
- BPE birleşmelerini uygulamadan önce kelime sınırlarında metni bölünen pre-tokenization regex modellerini ekle
  添加预分词正则模式, bpe 合并前按词边界 分分文本
- Bir corpus üzerinde özel bir tokenizer eğitmek ve çok dilli metinde tiktoken ile sıkıştırma oranını değerlendirmek
  Sözcükler üzerinde kendi kendini tanımlayan bir kelime makinesi eğitmek ve çok dilli metinlerde tiktoken ile sıkıştırma oranını değerlendirmek

> **【中文解读】**Bu dersin amacı, ilk sınıf oyuncakları BPE'yi üretim sınıfı 分词器 olarak yükseltmek. Önemli gelişmeler şunları içerir: Unicode 归一化(NFKC) 预分词正则(跨词边界的合并) 字节级回退 (零未知代币) 零特币 管理(BOS/EOS/聊天模板标记器) ⋅ bunlar "bütün internet"in 分词处理 için gerekli mekanizmalardır.

## Sorunlar. Sorunlar.

Ders 01'den gelen BPE işaretleyiciniz İngilizce metinde çalışıyor. Şimdi Japonca atın. Ya da emoji. Ya da Python kodu karışık sekmeleri ve boşluklarla.

> İlk sınıfınızdaki BPE 分词器能处理英文文本──现在给它日文──或是emoji──或混合制表符和空格的Python代码──

- Kırırıyor.

> Boşa gidecek.

BPE'nin yanlış olduğu için değil, uygulamanın tamamlanmamış olması için. Bir üretim tokenizerinin herhangi bir kodlama içindeki çiğ baytları işlediği için değil, bölmeden önce Unicode'u normalleştirdiği için, asla birleşmeyen özel tokenleri yönettiği için değil, alt sözcük bölüşmesi ile zincir öncesi tokenize edilmesi için ve tüm bunları 15 trilyon token işleme eğitimi borusunu boğazlamayacak kadar hızlı bir şekilde yapması için.

> Bu, BPE'nin sorunları olduğu için değil, tamamlanmamış olması için değil. Üretim sınıfı sözcüğü, herhangi bir kodun orijinal şablonunu işlemeyi, bölünmeden önce birleştirilmesini, düzenlemeyi, özel birleştirme, 串联预分词与子词分割, tüm işlemleri yeterince hızlı olduğu için, 15 milyar token'ın eğitim boru hattının şişesinin işlenmesine izin vermeyecek.

GPT-2'nin tokenizerinde 50.257 token var. Llama 3'ün sayısı 128.256'dır. GPT-4'de yaklaşık 100.000 tane var. Bunlar oyuncak numaraları değil. Bu sözlüklerin arkasındaki birleşme tabloları yüzlerce gigabayt metinde eğitilmiştir ve çevredeki makine - normallaşma, pre-tokenizasyon, özel token enjeksiyonu, sohbet şablon biçimlendirme - "hello world" ile tüm internetle ilgilenen bir tokenizeri ayırır.

> GPT-2'nin ayırt edici makinesi 50,257 tane tokeni var. Llama 3'nin 128,256 tane var. GPT-4'ün yaklaşık 100.000 tane var. Bunlar oyuncak sayıları değil. Bu kelimelerin arkasındaki birleşim makinesi, yüzlerce GB metinde eğitim alıyor. Çevresi  birleştirme, ön ayırt edici kelimeler, özel tokenler, giriş, sohbet biçimleri  tam olarak "selam dünya" ve tüm İnternet'in ayırt edici biçimlerini işleyebilen ayırt edici bir yapı.

Bu makineyi sen yapacaksın.

> Bu mekanizmayı inşa edeceksin.

> **【中文解读】**生产级分词器不是单一算法,而是一个五阶段管线:归一化 → 预分词 → BPE 合并 → 特殊代币注入 → ID 映射──每个阶段解决不同的问题──例如 NFKC 归一化把 "fi" 连字(U+FB01) "fi" 两个字符,预分词防止 "cat" 被合并出 "e c" 这样代币──

>  **【类比】**Ürün: Ü+FB01 "fi" → "fi",全角字母 → 半角),预分词是"按目的先分堆"(按词边界、数字、标点切,避免跨城市混装),BPE 合并是"高频包裹自动拼箱"(常见词直接整箱),特殊 token 是"挂号信标签"(BOS/EOS/PAD 最后永远不参与拼箱),才是"贴条形码"(ID 映射) ∼任何套漏掉,邮件就乱.

> **【拓展：Llama 3 的分词器升级】**Meta 在 Llama 3 中将词表从 32K (Llama 2'nin cümlesi) Piece BPE) yükseltme 128K (tiktoken 风格字节级 BPE), özel olarak non-Ingilizce yazılı belirtiler bölünmesi arttırmıştır. Bu değişiklik, çok dilli sıkıştırma verimliliğini yaklaşık 2 kat arttı, ancak yerleşim matriksinin parametreleri sayısı da 4 kat arttı.

## Konsepten bir şey.

### Tam Boru hattı

Bir üretim tokenizer bir algoritma değil, her biri farklı bir sorunu çözmek için beş aşamalı bir boru hattıdır.

> 生产级分词器 tek bir algoritma değildir.

```mermaid
graph LR
    A[Raw Text] --> B[Normalize]
    B --> C[Pre-Tokenize]
    C --> D[BPE Merge]
    D --> E[Special Tokens]
    E --> F[Token IDs]

    style A fill:#1a1a2e,stroke:#e94560,color:#fff
    style B fill:#1a1a2e,stroke:#e94560,color:#fff
    style C fill:#1a1a2e,stroke:#e94560,color:#fff
    style D fill:#1a1a2e,stroke:#e94560,color:#fff
    style E fill:#1a1a2e,stroke:#e94560,color:#fff
    style F fill:#1a1a2e,stroke:#e94560,color:#fff
```

Her aşamanın özel bir işi vardır:

> Her aşamada belirli bir görev vardır:

| Stage | What It Does | Why It Matters |
|-------|-------------|----------------|
| Normalize | NFKC Unicode, lowercase optional, strip accents optional | "fi" ligature (U+FB01) becomes "fi" (two chars). Without this, same word gets different tokens. |
| Pre-Tokenize | Split text into chunks before BPE | Prevents BPE from merging across word boundaries. "the cat" should never produce a token "e c". |
| BPE Merge | Apply learned merge rules to byte sequences | The core compression. Turns raw bytes into subword tokens. |
| Special Tokens | Inject [BOS], [EOS], [PAD], chat template markers | These tokens have fixed IDs. They never participate in BPE merges. The model needs them for structure. |
| ID Mapping | Convert token strings to integer IDs | The model sees integers, not strings. |

### BPE byte seviyesinde

Ders 01'nin tokenizer'i UTF-8 baytlarında çalıştı. Doğru bir çağrıydı. Ama önemli bir şeyi atladık: bu baytlar geçerli olmayan UTF-8'de ne olur?

> İlk sınıfın ayırt edici kelimeleri UTF-8'de kullanılıyor. Bu doğru bir seçim. Ama önemli bir şeyi atladık: Bu karakterler geçerli olmadığında ne olur?

BPE byte seviyesinde, her mümkün byte değeri (0-255) geçerli bir token olarak ele alarak çözülür. Temel sözlükleriniz tam olarak 256 girişi. Her dosya - metin, ikili, bozuk - bilinmeyen bir token üretmeden tokenlendirilebilir.

> 字节级 BPE 通过将每个可能的字节值(0-255)视为有效代币来解决这个问题――你的基础词表恰好 256条条点――任何文件文本、二进制、损坏的都可以被分词而产生未知代币──

GPT-2 bir numara ekledi: her baytı bir basınabilir Unicode karakterine harcama yapın, böylece kelime birikimi insan tarafından okunur. 0x20 bayt (uzay) harcamalarında "G" karakterine dönüşür. Bu tamamen kozmetik. Algoritm umurunda değil.

> GPT-2 bir sürümle: her bir karakterin bir yazılabilir Unicode karakterine yerleştirilmesi, sözcüklerin okunurlu kalmasını sağlamak.

Gerçek güç: BPE'nin byte seviyesinde dünya üzerindeki her dili ele alır. Çinli karakterler her biri 3 UTF-8 bytes. Japonca 3-4 byte olabilir. Arapça, Devanagari, emoji - hepsi sadece byte dizisi. BPE algoritması bu byte dizisinde kalıpları İngilizce ASCII byte'lerde bulduğu gibi bulur.

> Gerçek güç: BPE sınıfı  dünyadaki her dilde işlem yapar. Orta harf karakterleri her bir 3 UTF-8 karakterini oluşturur. Japonca 3-4 karakter oluşturur. Arapça, Türkçe, Türkçe ve Türkçe.

> **【中文解读】**字节级 BPE'nin çekirdek avantajları:基础词表恰好 256 字节值,任何输入都能编码;;GPT-2 ayrıca bir "花招" yaptı. Her字节ü bir yazılabilir Unicode karakterine harekete geçirdi, böylece söz表 daha kolay okunurdu;.

### Tokenizasyon öncesi

BPE metnize dokunmadan önce, onu parçalara ayırmanız gerekir. Bu, birleşme algoritmasının kelimeler sınırlarını uzanan jetonlar oluşturmasını engeller.

> BPE'de metnizi işlemeyince, onu parçalara ayırmanız gerekir. Bu, birleştirilmiş algoritmanın sözcük sınırı üzerinde bir işaret oluşturmasını engeller.

GPT-2 metni bölmek için regex örneğini kullanır:

> GPT-2: Yazıyı ayırmak için resmi ifade kullanmak:

```
'(?:[sdmt]|ll|ve|re)| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+
```

Bu kalıp kısaltmalara ("don't" "don" + "'t" haline gelir), seçmeli ön alanlı, sayısal, noktalama ve beyaz alanlı kelimelere ayrılır. Ön alan sözcüğüne bağlanır - bu nedenle " kedi" [", " kedi" "), değil [", " ", " kedi" "].

> Bu model kısaltma biçiminde ayrıştırılmıştır. Bu nedenle " kedi " " " kedi " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " "

Llama, regex'i tamamen atlayan SentencePiece'yi kullanır. Çiğ bayt akışını uzun bir dizi olarak ele alır ve BPE algoritmasının sınırları bulmasına izin verir. Bu daha basit ama BPE'ye çapraz sözcük jetonları oluşturmak için daha fazla özgürlük verir.

> Llama kullanın SentencePiece, tamamen gerçek ifadeyi atladı. Bu, BPE algoritmasının kendiliğinden sınırları belirlemesine izin verir. Bu daha basit ama BPE'ye daha fazla oluşturma özgürlüğünü verir.

Seçim önemlidir. GPT-2'nin regex'i, tokenizer'in bir kelimenin sonunda "in" ve bir sonraki kelimenin başında "in" birleşmesi gerektiğini öğrenmesini engeller. SentencePiece buna izin verir, bu da bazen daha verimli sıkıştırma üretir ancak daha az yorumlanabilir tokens.

> Bu seçim çok önemlidir. GPT-2'nin kuralları bir kelimenin sonunun "di" ve sonuncu kelimenin başındaki "di" 合并──SentencePiece bunu yapmayı sağlar.

### Özel Tokenler

Her üretim tokenizer, yapısal işaretçiler için token kimliklerini saklar:

> Her üretim sınıfı分词器都为结构标记保留代币 ID:

| Token | Purpose | Used By |
|-------|---------|---------|
| `[BOS]` / `<s>` | Beginning of sequence | Llama 3, GPT |
| `[EOS]` / `</s>` | End of sequence | All models |
| `[PAD]` | Padding for batch alignment | BERT, T5 |
| `[UNK]` | Unknown token (byte-level BPE eliminates this) | BERT, WordPiece |
| `<\|im_start\|>` | Chat message boundary start | ChatGPT, Qwen |
| `<\|im_end\|>` | Chat message boundary end | ChatGPT, Qwen |
| `<\|user\|>` | User turn marker | Llama 3 |
| `<\|assistant\|>` | Assistant turn marker | Llama 3 |

Özel tokenler hiçbir zaman BPE tarafından bölünmez. Birleştirme algoritması çalışmadan önce tam olarak eşlenir, sabit kimliği ile değiştirilir ve çevredeki metin normal olarak tokenized edilir.

> Özel simgeler, BPE tarafından asla ayrılmaz. Bunlar, algoritma işleminden önce doğru bir şekilde uyumlu hale getirilmiş, sabit bir kimlik olarak değiştirilmiştir.

> **【中文解读】**Özel işaret, 分词器中"不可触"ın saklanma işaretidir:`[BOS]`(序列开始)`[EOS]`(序列结束)`[PAD]`(批次填充) 聊天模板标记等──它们有固定的ID,永远不参与BPE 合并,而在合并之前通过精确匹配被提取出来──Llama 3 使用 `<|start_header_id|>`- Evet.`<|end_header_id|>`- Evet.`<|eot_id|>`Çanaklama yapısı, Çanaklama GPT kullanımı `<|im_start|>`和 `<|im_end|>`- Evet.

> **【拓展：聊天模板的工程陷阱】**聊天模板, gerçekte yapılan uygulamaların en kolay yanıltıcı yeridir. Her model, eğitim sırasında belirli biçimlerde özel bir belirti kullanır.`chat_template`Jinja2 模板机制就是为了标准化这个过程――

> ️ **【易错点】**实现特殊 token 的三个陷:(1) **特殊 token 内含正则元字符**如 `<|im_start|>`Orta `|`- İhtiyacım var .`re.escape()`转义,否则在 GPT-2 预分词的正则上会被解析成选择符;(2) **未从 BPE 词表中排除特殊 token**若 `<|im_end|>`Bölülmeden önce çıkarılır, karakter sırası BPE tarafından 8 simgeye ayrılır, model her zaman tam yapı belirtilmesine bakmaz;**`add_special_tokens=False` 漏配**调用 `tokenizer.encode(text)`默认会自动加 BOS/EOS,做拼接时会出现 BOS BOS EOS EOS 序列,破坏注意面具对齐──修复:编码时显式传 `add_special_tokens=False`Sonunda da bir teklifin içinde.

### Çat Şablonları

Bu insanların çoğu karışıklık ve çoğu uygulamanın kırıldığı yer.

> Bu çoğu insanın şaşkın olduğu ve çoğu insanın yanlış bir şekilde başardığı yer.

Bir sohbet modeline mesaj gönderdiğinizde, API bir mesaj listesini kabul eder:

> Çatın modelinde mesaj gönderdiğinde API bir mesaj listesi kabul eder:

```
[
  {"role": "system", "content": "You are helpful."},
  {"role": "user", "content": "Hello"},
  {"role": "assistant", "content": "Hi there!"}
]
```

Modeldeki JSON görünmüyor. Düz bir token dizini görüyor. Çat şablonu, mesajları özel tokenler kullanarak bu düz dizine dönüştürüyor. Her model bunu farklı yapar:

> Model JSON'a bakmıyor. Bu model bir 平的符号序列 (seyrek) görür.

```
Llama 3:
<|begin_of_text|><|start_header_id|>system<|end_header_id|>

You are helpful.<|eot_id|><|start_header_id|>user<|end_header_id|>

Hello<|eot_id|><|start_header_id|>assistant<|end_header_id|>

Hi there!<|eot_id|>

ChatGPT:
<|im_start|>system
You are helpful.<|im_end|>
<|im_start|>user
Hello<|im_end|>
<|im_start|>assistant
Hi there!<|im_end|>
```

Şablonun yanlış yapılması ve modelin çöp üretmesi. Tam bir biçim üzerinde eğitildi. Her türlü sapma - kayıp bir yeni çizgi, değiştirilmiş bir token, ekstra bir alan - girişleri eğitim dağılımının dışında yerleştirir.

> 模板搞错了模型就会产生垃圾输出――它在一个精确形式上训练的――任何偏差缺少换行、交换代币、多一个空格都会使输入偏离训练分布──

> 🤔 **【困惑】**S: Llama 3 neden vazgeçti SentencePiece 改用tiktoken?字节级 BPE 比原版强在哪? A: 两点关键优势:(1) **SentencePiece 用 ⊗（U+2581）代替空格**, ASCII 字符和原始空格的混在聊天场下导致代币序列对快速微小变变过于敏感;tiktoken 直接保留前导空格,"hello"和"hello"是不同代币,更稳定;**字节级 BPE 词表恰好 256 个基础 token**, teorik olarak herhangi bir karakter sırasını kodlayabilir, emoji 、 özel bölge karakterleri dahil), belirli bir语料ye bağlı değildir;SentencePiece 词表若未训练到某字符直接 [UNK]。Llama 3 词表从32K 扩至128K,多语言压缩比升升 ~2x,这是推理成本买单的工程决策──

### Hızlılık

Python üretim tokenizasyonu için çok yavaş.

> Python 对于生产级分词太慢了──

tiktoken (OpenAI) Python bağlamaları ile Rust'de yazılmıştır. HuggingFace tokenizeri de Rust. SentencePiece C++. Bunlar saf Python'a göre 10-100x hızlandırma sağlar.

> tiktoken(OpenAI) Rust ile 编写并提供 Python 绑定──HuggingFace tokenizers 也是 Rust──SentencePiece 是 C++──这些比纯Python 快 10-100倍──

Perspektif için: Llama 3 için 15 trilyon token'i 1 saniyelik 1 milyon token'a (hızlı Python) tokenize etmek 174 gün sürecek.

> Örnek: Llama 3 için hızlandırılan hız: saniyede 100 milyon token (Hızlı Python) için hızlandırılan hız: 15 milyar token (Hızlı Python) için 174 gün gerekir.

Algoritmi anlamak için Python'da inşa ediyorsunuz. Üretim sırasında, bir oluşturulmuş uygulamayı kullanır ve sadece Python kapakına dokunursunuz.

> Python'la yapılandırmak için algoritmaları anlamak için kullanıyorsun.

## Yapın.
```figure
weight-tying
```

## Yapın

### Adım 1: Byte-Level Kodlama

Temel. Her bir ipçeyi bir bayt dizisine dönüştürün, her baytı görüntülemek için basılabilir bir karakterle haritasın ve süreci tersine çevirin.

> 基础── herhangi bir karakteryi bir karakter dizisi olarak dönüştürür, her bir karakteryi görüntülemek için yazdırılabilir karakterlere haritalar,并反转该过程──

```python
def bytes_to_tokens(text):
    return list(text.encode("utf-8"))

def tokens_to_text(token_bytes):
    return bytes(token_bytes).decode("utf-8", errors="replace")
```

Bayt sayısını görmek için çok dilli metinde test:

```python
texts = [
    ("English", "hello"),
    ("Chinese", "你好"),
    ("Emoji", "🔥"),
    ("Mixed", "hello你好🔥"),
]

for label, text in texts:
    b = bytes_to_tokens(text)
    print(f"{label}: {len(text)} chars -> {len(b)} bytes -> {b}")
```

"hello" 5 byte. "你好" 6 byte (3 karakter başına). Ateş emoji 4 byte. Byte seviyesindeki tokenizer hangi dilden ibaret olduğu umurumda değil. Byte byte.

> "hello" 5 字节──"你好" 6 字节──每个字符 3 字节)──火焰 emoji 4 字节──字节级分词器不关心它是什么语言──字节就是字节──

### Adım 2: Regex ile Pre- Tokenizer

GPT-2 regex modelini kullanarak metni parçalara ayırın.

> GPT-2 resmi biçimi kullanılarak metni parçalara ayırır.

```python
import re

try:
    import regex
    GPT2_PATTERN = regex.compile(
        r"""'(?:[sdmt]|ll|ve|re)| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+"""
    )
except ImportError:
    GPT2_PATTERN = re.compile(
        r"""'(?:[sdmt]|ll|ve|re)| ?[a-zA-Z]+| ?[0-9]+| ?[^\s\w]+|\s+(?!\S)|\s+"""
    )

def pre_tokenize(text):
    return [match.group() for match in GPT2_PATTERN.finditer(text)]
```

- Evet .`regex`modül Unicode özelliği kaçışlarını destekler (`\p{L}`Mektuplar için,`\p{N}`Standart kütüphanede.`re`Modülde değil, bu yüzden ASCII karakter sınıflarına geri dönelim.`regex`- Evet .

> `regex`模块支持 Unicode 属性转义(`\p{L}`Gösterme`\p{N}`☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐`re`模块不支持,所以我们回归 ASCII 字符类──对于生产级多语言分词器,请安装 `regex`- Evet.

Denemeyin.

```python
print(pre_tokenize("Hello, world! Don't stop."))
# [' Hello', ',', ' world', '!', " Don", "'t", ' stop', '.']
```

Önceki boşluk kelimenin yanında kalır. Kısalamalar apostropda bölünür. Noktalama kendi parçası haline gelir. BPE bu sınırları asla birleştirmez.

> Ön导空格保持在词上. 缩写在撇号处分分. 标点成为独立块. BPE 永远不会跨越这些边界合并代币.

### Adım 3: Byte Sequences'te BPE

01-ci dersden gelen temel algoritma, ama şimdi önceden tokenize edilmiş parçalarda bağımsız olarak çalışıyor.

> Birinci sınıfın temel algoritması, ama şimdi bağımsız olarak önbölümün bir parçasıyla işlem yapmaktadır.

```python
from collections import Counter

def get_byte_pairs(chunks):
    pairs = Counter()
    for chunk in chunks:
        byte_seq = list(chunk.encode("utf-8"))
        for i in range(len(byte_seq) - 1):
            pairs[(byte_seq[i], byte_seq[i + 1])] += 1
    return pairs

def apply_merge(byte_seq, pair, new_id):
    merged = []
    i = 0
    while i < len(byte_seq):
        if i < len(byte_seq) - 1 and byte_seq[i] == pair[0] and byte_seq[i + 1] == pair[1]:
            merged.append(new_id)
            i += 2
        else:
            merged.append(byte_seq[i])
            i += 1
    return merged
```

### Dördüncü Adım: Özel İşaret İşlemi

Özel tokenler tam eşleşme ve sabit kimliklere ihtiyaç duyar.

> Özel simgeler, BPE'yi tamamen atlatmaktadır.

```python
class SpecialTokenHandler:
    def __init__(self):
        self.special_tokens = {}
        self.pattern = None

    def add_token(self, token_str, token_id):
        self.special_tokens[token_str] = token_id
        escaped = [re.escape(t) for t in sorted(self.special_tokens.keys(), key=len, reverse=True)]
        self.pattern = re.compile("|".join(escaped))

    def split_with_specials(self, text):
        if not self.pattern:
            return [(text, False)]
        parts = []
        last_end = 0
        for match in self.pattern.finditer(text):
            if match.start() > last_end:
                parts.append((text[last_end:match.start()], False))
            parts.append((match.group(), True))
            last_end = match.end()
        if last_end < len(text):
            parts.append((text[last_end:], False))
        return parts
```

### Adım 5: Tam Tokenizer Sınıfı

Her şeyi bir araya getir: normalleştir, özel tokenlere böl, önceden tokenleştir, BPE birleşmesi, harita ile kimlikler.

> Tüm adımları birleştirmek için özel bir işaretle ayırmak için birleştirmek için birleştirmek için birleştirmek için birleştirmek için birleştirmek için birleştirmek için birleştirmek için birleştirmek için birleştirmek için birleştirmek için birleştirmek için birleştirmek için birleştirmek için birleştirmek için birleştirmek için birleştirmek için birleştirmek için birleştirmek için birleştirmek için birleştirmek için birleştirmek için birleştirmek için birleştirmek için birleştirmek için birleştirmek için birleştirmek için birleştirmek için birleştirmek için birleştirmek için birleştirmek için birleştirmek için birleştirmek için birleştirmek için birleştirmek için birleştirmek için birleştirmek için birleştirmek için birleştirmek için birleştirmek için birleştirmek için birleştirmek için birleştirmek için birleştirmek için birleştirmek için birleştirmek için birleştirmek için birleştirmek için birleştirmek için birleştirmek için birleştirmek için birleştirmek için birleştirmek için birleştirmek için birleştirmek için birleştirmek için

```python
import unicodedata

class ProductionTokenizer:
    def __init__(self):
        self.merges = {}
        self.vocab = {i: bytes([i]) for i in range(256)}
        self.special_handler = SpecialTokenHandler()
        self.next_id = 256

    def normalize(self, text):
        return unicodedata.normalize("NFKC", text)

    def train(self, text, num_merges):
        text = self.normalize(text)
        chunks = pre_tokenize(text)
        chunk_bytes = [list(chunk.encode("utf-8")) for chunk in chunks]

        for i in range(num_merges):
            pairs = Counter()
            for seq in chunk_bytes:
                for j in range(len(seq) - 1):
                    pairs[(seq[j], seq[j + 1])] += 1
            if not pairs:
                break
            best = max(pairs, key=pairs.get)
            new_id = self.next_id
            self.next_id += 1
            self.merges[best] = new_id
            self.vocab[new_id] = self.vocab[best[0]] + self.vocab[best[1]]
            chunk_bytes = [apply_merge(seq, best, new_id) for seq in chunk_bytes]

    def add_special_token(self, token_str):
        token_id = self.next_id
        self.next_id += 1
        self.special_handler.add_token(token_str, token_id)
        self.vocab[token_id] = token_str.encode("utf-8")
        return token_id

    def encode(self, text):
        text = self.normalize(text)
        parts = self.special_handler.split_with_specials(text)
        all_ids = []
        for part_text, is_special in parts:
            if is_special:
                all_ids.append(self.special_handler.special_tokens[part_text])
            else:
                for chunk in pre_tokenize(part_text):
                    byte_seq = list(chunk.encode("utf-8"))
                    for pair, new_id in self.merges.items():
                        byte_seq = apply_merge(byte_seq, pair, new_id)
                    all_ids.extend(byte_seq)
        return all_ids

    def decode(self, ids):
        byte_parts = []
        for token_id in ids:
            if token_id in self.vocab:
                byte_parts.append(self.vocab[token_id])
        return b"".join(byte_parts).decode("utf-8", errors="replace")

    def vocab_size(self):
        return len(self.vocab)
```

### Adım 6: Çok Dilli Sınav

Gerçek test İngilizce, Çin, emoji ve kod at.

> Gerçek test. İngilizce, Çince, Emoji ve kod da bırakıldı.

```python
corpus = (
    "The quick brown fox jumps over the lazy dog. "
    "The quick brown fox runs through the forest. "
    "Machine learning models process natural language. "
    "Deep learning transforms how we build software. "
    "def train(model, data): return model.fit(data) "
    "def predict(model, x): return model(x) "
)

tok = ProductionTokenizer()
tok.train(corpus, num_merges=50)

bos = tok.add_special_token("<|begin|>")
eos = tok.add_special_token("<|end|>")

test_texts = [
    "The quick brown fox.",
    "你好世界",
    "Hello 🌍 World",
    "def foo(x): return x + 1",
    f"<|begin|>Hello<|end|>",
]

for text in test_texts:
    ids = tok.encode(text)
    decoded = tok.decode(ids)
    print(f"Input:   {text}")
    print(f"Tokens:  {len(ids)} ids")
    print(f"Decoded: {decoded}")
    print()
```

Çinli karakterler her biri 3 byte üretir. emoji 4 byte üretir. Bunların hiçbiri tokenizer'i çarpmaz. Hiçbiri bilinmeyen tokenler üretmez. Bu byte seviyesindeki BPE'nin gücü.

> 中文字符每个产生 3 字节──emoji 产生 4 字节──这些都不会使分词器崩──都不会产生未知代币──这是字节级 BPE 的力量──

> **【中文解读】**Yukarıdaki kod tüm bileşenleri birbirine bağlayacaktır:归归化 → 特殊代币 分割 → 预分词 → BPE 合并 → ID 映射。测试覆盖英文、中文、emoji、代码和特殊代币的混合场景──字节级 BPE garanti herhangi bir giriş bilinmeyen bir token üretmez işte bu, endüstriyel standartların temel nedenidir。

> **【拓展：分词速度的工程意义】**Pure Python 分词器每秒处理约1M tokens,Llama 3'ün预训语料有15亿亿代币,Python 需要174 天――tiktoken(Rust 实现)每秒100M代币,只需要1.7 天――这就是为什么生产级分词器都用编译语言:tiktoken 用Rust,HuggingFace tokeners 用Rust,SentencePiece 用C++──

## Çerçeveyi kullanın.

### Gerçek Tokenizers'i karşılaştırmak

Llama 3, GPT-4 ve Mistral'ın gerçek işaretleyicilerini yükle ve her birinin aynı çok dilli paragrafı nasıl ele aldığını gör.

> Ünlü dillerde kullanılan kelimelerden oluşan bir dizi metin nasıl işlenir?

```python
import tiktoken

gpt4_enc = tiktoken.get_encoding("cl100k_base")

test_paragraph = "Machine learning is powerful. 机器学习很强大。 L'apprentissage automatique est puissant. 🤖💪"

tokens = gpt4_enc.encode(test_paragraph)
pieces = [gpt4_enc.decode([t]) for t in tokens]
print(f"GPT-4 ({len(tokens)} tokens): {pieces}")
```

```python
from transformers import AutoTokenizer

llama_tok = AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-3-8B")
mistral_tok = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-v0.1")

for name, tok in [("Llama 3", llama_tok), ("Mistral", mistral_tok)]:
    tokens = tok.encode(test_paragraph)
    pieces = tok.convert_ids_to_tokens(tokens)
    print(f"{name} ({len(tokens)} tokens): {pieces[:20]}...")
```

Aynı metin için farklı token sayısını göreceksiniz. 128K sözlüklü Llama 3 ortak desenleri birleştirmede daha agresif. 100K ile GPT-4 ortada oturur. 32K ile Mistral daha fazla token üretir ancak daha küçük bir yerleştirme katmanı vardır.

> Aynı metnin farklı simgelerinin sayısı göreceksiniz. Llama 3'ün 128K 词表在合并常见模式上更积极──GPT-4'ün 100K 中间──Mistral'ın 32K 更多的代币产生,但嵌层更小──

Bu anlaşma her zaman aynıdır: Daha büyük kelime kümesi daha kısa sıralamalar ama daha fazla parametre anlamına gelir.

> 权衡始终相同: Büyük kelime listesi daha kısa bir dizi anlamına gelir, ancak daha fazla parametre vardır。

## İndirin . Ürünler .

Bu ders, üretim tokenizörlerini oluşturmak ve düzeltmek için bir ipucu üretir.`outputs/prompt-tokenizer-builder.md`- Evet .

> Bu ders, yapılandırma ve üretim sınıfı sözcük makinesi için kullanılır.`outputs/prompt-tokenizer-builder.md`- Evet.

## Egzersizler.

1. **Easy:**Bir ekle`get_token_bytes(id)`Bu yöntem, herhangi bir token kimliği için çiğ baytları gösterir. En yaygın birleşik tokenlarınızın aslında neyi temsil ettiğini incelemek için kullanın.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`get_token_bytes(id)`方法,显示任意 token ID 的原始字节──用它检查您最常用的合并代码 实际代表什么──
2. **Medium:**Beyaz alan ve rakamlara bölünen, ama önde gelen alanları koruyan Llama tarzı pre-tokenizer'i uygulayın.
   Çinçe Çevirimi: gerçekleştirmek Llama 风格的预分词器,按空格和数字分分但保留前导空格──在相同语料上比较其词表与GPT-2 正则方法──
3. **Hard:** Listesi alan bir sohbet şablonu yöntemi ekle`{"role": ..., "content": ...}`mesajlar ve Llama 3 sohbet biçimi için doğru belirti sırasını üretir.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`{"role": ..., "content": ...}`消息列表并生成 Llama 3 聊天格式的正确代币序列──对照 HuggingFace 实现进行测试──

## Anahtar Şartlar .

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|----------------------|---------|
| Byte-level BPE | "Tokenizer that works on bytes" | BPE with a base vocabulary of 256 byte values -- handles any input without unknown tokens | 字节级 BPE，基础词表 256 个字节值 |
| Pre-tokenization | "Splitting before BPE" | Regex or rule-based splitting that prevents BPE from merging across word boundaries | 预分词，防止跨词边界的 token 合并 |
| NFKC normalization | "Unicode cleanup" | Canonical decomposition followed by compatibility composition -- "fi" ligature becomes "fi", fullwidth "A" becomes "A" | NFKC 归一化，统一 Unicode 表示 |
| Chat template | "How messages become tokens" | The exact format for converting a list of role/content messages into a flat token sequence -- model-specific and must match training format | 聊天模板，消息转 token 的格式规则 |
| Special tokens | "Control tokens" | Reserved token IDs that bypass BPE -- [BOS], [EOS], [PAD], chat markers -- matched exactly before merge | 特殊 token，绕过 BPE 的控制标记 |
| Fertility | "Tokens per word" | Ratio of output tokens to input words -- 1.3 for English in GPT-4, 2-3 for Korean, higher means wasted context | 生育率，每词 token 数 |
| tiktoken | "OpenAI tokenizer" | Rust BPE implementation with Python bindings -- 10-100x faster than pure Python | OpenAI 的 Rust 分词器实现 |
| Merge table | "The vocabulary" | Ordered list of byte-pair merges learned during training -- this IS the tokenizer's learned knowledge | 合并表，分词器的核心知识 |

## Daha fazla okumak

- [OpenAI tiktoken source](https://github.com/openai/tiktoken)-- GPT-3.5/4 tarafından kullanılan Rust BPE uygulaması
- [HuggingFace tokenizers](https://github.com/huggingface/tokenizers)-- Rust Tokenizer kütüphanesi BPE, WordPiece, Unigram'ı destekler
- [Llama 3 paper (Meta, 2024)](https://arxiv.org/abs/2407.21783)-- 128K kelime birikimi ve tokenizer eğitimi hakkında detaylar
- [SentencePiece (Kudo & Richardson, 2018)](https://arxiv.org/abs/1808.06226)-- dil-agnostik simgelendirme
- [GPT-2 tokenizer source](https://github.com/openai/gpt-2/blob/master/src/encoder.py)-- orijinal bayt-Unicode haritası
