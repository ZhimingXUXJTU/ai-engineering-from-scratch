# Qwen-VL Aile ve Dinamik-FPS Videoları

> Qwen-VL ailesi  Qwen-VL (2023), Qwen2-VL (2024), Qwen2.5-VL (2025), Qwen3-VL (2025)  2026'da en etkili açık görüş dil model soyundadır. Her nesil, açık ekosistemin geri kalanının on iki ay içinde kopyaladığı tek bir kararlı mimari bahis yaptı: M-RoPE üzerinden yerel dinamik çözünürlük, mutlak zaman ayarıyla dinamik-FPS örnekleme, ViT'deki pencerelerin dikkatini ve yapılandırılmış ajan çıkış biçimlerini. Qwen3-VL tarafından, reçete istikrarlı hale geldi: 2D-RoPE-ViT kodlayıcı, yerel açı oranı girişleri, büyük bir Qwen3 dil tabanına bir MLP projeksiyonu ve birinci sınıf hedefler olarak OCR, yerleştirme ve ajan davranışını vurgulayan eğitim aşamaları. Bu ders aileyi kronolojik olarak okuyor, böylece her düğmenin neden olduğu yeri anlayabiliyorsun.

> **【中文解读】**Qwen-VL シリーズ 2026 yılının en etkili açık kaynak görsel dil model ailesidir. Her nesil 12 ay içinde açık kaynak topluluğu tarafından 12 önemli yapısal kararlar verildi.

> **【拓展：Qwen-VL 的产业生态位】**Qwen-VL 系列, Çin dilinde iki dilli ortamlarda, GUI 代理、OCR ve video anlama açısından önemli avantajlara sahiptir.

**Type:** Learn  | **类型：学习**
**Languages:** Python (stdlib, M-RoPE encoder + dynamic-FPS sampler)  | **语言：Python（标准库，M-RoPE 编码器 + 动态帧率采样器）**
**Prerequisites:** Phase 12 · 06 (patch-n'-pack)  | **前置：阶段12第06课（补丁打包）**
**Time:** ~120 minutes  | **时长：约120分钟**

>  **【前置】**学本节前 Lütfen önce bil:Fase 12·06(patch-n'-pack 任意分辨率);Fase 7·04(RoPE 旋转位置编码,本节升级为 3D M-RoPE);Fase 14·04(Agent 工具调用,本节讲解 VLM 如何输出 JSON)
>  **【类比】**Qwen-VL 系列 = "中文 VLM 旗舰"──和 LLaVA 系列的区别:LLaVA 主打英文 + 简单架构;Qwen-VL 主打中英双语 + 高分辨率 + 结构化输出──如果你做中文场景(财报、合同、票据),Qwen-VL 是默认选择──
> ️ **【易错点】**Qwen-VL 输出边界框坐标时混"绝对像素 vs相对比例"不同代次用不同约定──Qwen2-VL绝对像素(0-1000 范围),Qwen2.5-VL 改用归一化比例(0-1)──修复:使用前查文档,按代次正确解析坐标──

## Öğrenme hedefleri

- M-RoPE'nin üç eksel dönümlerini hesaplayın (zaman, yüksekliği, genişliği) ve neden bunların hepsine ihtiyaç duyduğunu açıklayın.
- Video için dinamik bir FPS örnekleme stratejisi seçin ve bir saniyelik simgeler vs olay tespit doğruluğu hakkında düşünün.
- Dört Qwen-VL nesil yükseltme sırasıyla ve her birinin neyi etkinleştirdiğini söyleyin.
- Qwen2.5 VL tarzı JSON ajanı çıkış biçimini bağlayın ve VLM yanıtından yapılandırılmış araç çağrılarını analiz edin.

## Sorun  sorun arka planı

Qwen-VL, Ağustos 2023'te LLaVA-1.5 ve BLIP-2'ye doğrudan bir cevap olarak gönderildi. Qwen ekibi hedef alan boşluk üçtür: çözünürlük, video ve yapılandırılmış çıkış.

Çözüm: LLaVA-1.5 336x336'da çalıştı. Fotoğraflar için iyi, Çin dilindeki bir fatura veya yoğun bir kalıplama ekran görüntüsü için işe yaramaz. Qwen-VL'nin ilk yeniliği 448x448 ve sınırlama kutusunun çıkışı ile yerleştirilmişti.

Video: Video-LLaMA, çerçeve başına kodlayıcıları yığarak LLM'ye gönderdi. Kısa klipler için çalışıyordu, zaman ekseni sinyal olduğu çok dakikalık videolar için değil. Qwen ekibi zamanı anlayan tek bir kodlayıcı istiyordu.

Yapılandırılmış çıkış: LLaVA serbest biçimli metin yayımladı. Bir ajan JSON'a ihtiyaç duyar. Qwen-VL açık JSON çıkış biçimlerinde eğitim almıştır.

Her Qwen-VL nesli bu üç ekseden birini uzattı.

> **【中文解读】**Qwen-VL  LLaVA-1.5'in üç büyük eksikliği başlatıyor: 1) çözünürlük 336x336 処理できない中文发票或密集表格截图; 2) 视频Video-LLaMA sadece kısa片段leri işleyebilir; 3) 構造化输出LLaVA 输出自由文本,代理需要 JSON──每一代 Qwen-VL 都在三轴上延伸──

## Konsepten bir şey.

### Qwen-VL (Avgust 2023)

İlk nesil: OpenCLIP ViT-bigG/14 kodlayıcı olarak (2.5B param), LLama uyumlu Q-Former (1-adım 256 sorgu ile), Qwen-7B tabanı. Katkılar:

- 448x448 çözünürlük (O zaman açık bir VLM için SOTA).
- Yerleşim / 定位: açık koordinat-tıkınası çıkışı ile görüntü-metin çiftlerinde eğitilmiştir. "Kedi <box>112, 204), (280, 344)</box>".
- Çin + İngilizce çok dilli eğitim başlangıçtan beri.

O zamanlar standartlar: İngilizce'de GPT-4V ile rekabetçi, Çin'de dominançlı.

> **【中文解读】**Qwen-VL birinci nesil kırılganı:448x448 çözünürlük(超越 LLaVA'nın 336x336) 定位能力(输出边界框坐标) ✓中英双语──中文基准上显著领先──

### Qwen2-VL (Eylül 2024)  M-RoPE ve yerli çözünürlük

Qwen2-VL sabit çözünürlüklü + Q-Former yığınını doğuştan dinamik çözünürlüklü ViT kodlayıcısı ile değiştirdi. Ana değişiklikler:

- Doğal dinamik çözünürlük / 原生动态分辨率. ViT 28 ile bölünebilir herhangi bir HxW kabul eder (2x uzaylı birleşim ile patch 14). 1120x672 (40x24 birleşmiş patches) bir görüntü 960 görsel jeton üretir. boyut yok, bez, küçük resim yok.
- M-RoPE (Multimodal RoPE) / 多模态旋转位置编码. Her token 1D yerine 3D pozisyonu (t, h, w) taşır. Resimler için t = 0, video için t = frame_index. RoPE, sorgu / anahtar vektörlerini bir eksesi başına bir frekansla döndürür.
- MLP projector / MLP 投影器. Q-Former'ı bırakın; birleşik yama tokenlerinde 2 kat MLP kullanın.
- Video dinamik FPS / 动态率视频. Video örnekleri varsayılan olarak 1-2 FPS, ama model keyfi çerçeve sayıları kabul.

Sonuç: Qwen2-VL-7B, birkaç multimodal referans değerinde GPT-4o ile eşleşti ve DocVQA (94.5 vs 88.4) üzerinde yendi.

> **【中文解读】**Qwen2-VL'nin çekirdek yapısı değişmiştir: sabit çözünürlük + Q-Former'i kaldırmak, orijinal canlı ortam çözünürlüğü ViT + M-RoPE + MLP 投影器──M-RoPE için her bir token için 3D konumlandırmak, zaman, yükseklik, genişlik), aynı konum kodlama işlemini tek bir şekilde yapabilmek için GPT-4o'nun çoklu biçim temelini oluşturmak.

### Qwen2.5VL (Şubat 2025)  dinamik FPS + mutlak zaman

Qwen2.5 VL'nin büyük değişikliği videoydu. Dinamik FPS sadece "gerekirse daha fazla çerçeve örneklemek" değil.

- Absolute time tokens / 绝对时间 token. konum göstergeleri yerine (cadı 0, 1, 2...), gerçek zaman damgaları kullanın. "0:04'te kedi atlar".`<time>0.04</time>`- Ben de. - Ben de.
- Dinamik FPS / 动态率. 1 FPS'de yavaş görüntü için örnek, 4+ FPS'de eylem için. Kullanıcı veya eğitmen seçer; M-RoPE uyarlanır.
- Pencere dikkat / ViT fencere dikkat. Yerel dikkat (blükler içinde yerel) geçiş için pencere; küresel dikkat birkaç katman.
- Açık JSON çıkış biçimi / 显式 JSON 输出格式. Araç- çağrı verileri üzerinde eğitilmiş: `{"tool": "click", "coords": [380, 220]}`- Ajan hazır. - Bilgi kullanma yeteneği.
- MRoPE-v2 ölçeklendirme / MRoPE-v2 缩放. Motular maksimum giriş boyutu ile ölçeklendirilsin böylece 10 dakikalık bir video frekans aralığı bitmez.

Benchmarks: Qwen2.5-VL-72B çoğu video benchmark'da GPT-4o'yu yener, belgelerde Gemini 2.0'ya eşleşir ve GUI yerleştirimi için açık model SOTA'yı ayarlar (ScreenSpot: 84% doğruluk vs. GPT-4o için 38%).

> **【中文解读】**Qwen2.5 VL'nin başarısı video anlayışında:绝对时间代币 让模型知道"第4秒猫跳了",动态率让模型在动作密集时自动提高采样率,窗口注意力提升 ViT 吞吐量──72B 版本在视频基准上超越GPT-4o,GUI 定位精度(ScreenSpot 84%)远超GPT-4o(38%)──

> **【拓展：结构化输出对 Agent 工程的意义】**Qwen2.5-VL'nin yapılandırılmış JSON 输出ı doğrudan bilgisayar kullanım temsilcisi olarak kullanılabilir.

### Qwen3-VL (Kasım 2025)

Qwen3-VL, yeniden icat etmek yerine birleştirilen bir artış yükseltmesidir: daha büyük LLM omurgası (Qwen3-72B), genişletilmiş eğitim verileri, geliştirilmiş OCR, Qwen3 "düşünme modu" aracılığıyla daha güçlü bir mantıklama.

Soy alınması: 2025 yılına kadar Qwen-VL mimarisi istikrarlı hale geldi.

> **【中文解读】**Qwen3-VL, yeniden ortaya çıkmak yerine artışlı bir yükseltme: daha büyük LLM 骨干、更多的训练数据、更好的 OCR、更强的推理(Qwen3 "思考模式")。ViT 和 M-RoPE 保持不变──2025 yılına kadar, Qwen-VL 架构已经稳定,后版本主要通过扩大规模和优化数据来升升────

### Matematik olarak M-RoPE Matematik prensipleri

Klasik RoPE bir sorguyu döndürür `q`boyutlu `d`Konumlara göre`m`Çift koordinatları kullanılarak:

```
q_rot[2i]   = q[2i]   * cos(m * theta_i) - q[2i+1] * sin(m * theta_i)   # 经典 RoPE 旋转
q_rot[2i+1] = q[2i]   * sin(m * theta_i) + q[2i+1] * cos(m * theta_i)
theta_i     = 10000^(-2i/d)                                                 # 频率基
```

M-RoPE gizli karanlığı üç gruba ayırır.`d = 96`. 32 dims'i temporal, 32'i yükseklik ve 32'i genişlik olarak belirleyin. Her bant kendi eksesi pozisyonu ile döner.`R_t(5)`- Evet .`R_h(10)`- Evet .`R_w(20)`Üç bandına uygulanır.

Metin işaretleri kullanımı `t = text_index, h = 0, w = 0`(veya normal bir seçim) uyumluluğu korumak için.`t = frame_time, h = row, w = col`Tek görüntü kullanımı`t = 0`- Evet .

Avantaj: Bir pozisyon kodlaması, farklı pozisyon tabloları veya şubeler kodları olmadan metin, resim ve videoyu işliyor.

> **【中文解读】**M-RoPE gizli boyutları üç frekanslara ayrıştırır: zaman, yükseklik, genişlik, her frekans kendi aksel konumlarına göre döner, metin belirtileri kullanılır (text_index, 0, 0), video  kullanılır (frame_time, row, col), single图用 (0, row, col) .

### Dinamik-FPS örnekleme mantığı

Videoyu gösterdiğimizde .`T`saniye ve hedef token bütçesi `B`- ...

1. Yapabileceğiniz maksimum FPS'i hesaplayın: `fps_max = B / (T * tokens_per_frame)`. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
2. Hedef FPS ' den birini seç .`{1, 2, 4, 8}`Bu tatmin eder.`fps <= fps_max`Seçim oranından seçim.
3. Hareket yüksekse (optik akış heuristik veya açık kullanıcı istekleri), daha yüksek FPS seçin. Hareket düşükse, daha düşük seçin.
4. Seçilen FPS'de örnekler aynı şekilde; ekle `<time>t</time>`Çerçeve arasındaki simgeler.

Qwen2.5-VL bu mantığı içeren bir şekilde eğitir; sonuçta kullanıcı `fps`Parametre. 4 FPS'de 60 saniyelik bir eylem dizisi, çerçeve başına 81 token = 19440 token ile, 32k bağlamda yönetilebilir.

> **【中文解读】**动态率的核心思想:根据视频时长、代币 预算和运动量,自动选择最佳率──60秒动作场景在4FPS下产生19440代币,可在32k上下文中处理──

### Yapılandırılmış ajan çıkışı yapılandırılmış ajan çıkışı

Qwen2.5 - VL'nin ajan eğitiminde açıkça yapılandırılmış araç çağrıları hedefliyor:

```
{
  "tool": "mouse_click",          # 工具名称
  "coords": [1024, 512],          # 点击坐标
  "button": "left",               # 鼠标按钮
  "modifier": null                # 修饰键
}
```

Parsing deterministiktir: JSON.parse modelin çıkışını karşılaştırın. Regex ve belirsizlik işlemeyi gerektiren serbest biçim " (1024, 512) " ile karşılaştırın.

> **【中文解读】**结构化输出让VLM直接发发出可解析的工具调用 (如点击坐标),无需正则表达式──这是ScreenSpot 精度的关键原因―― 55% 跳到 84%
```figure
mm-mrope-axes
```

## Kullan

## Kullanın.

`code/main.py`Uygulamaları:

- M-RoPE konum hesaplama paketlenmiş bir dizi metin, görüntü yamaları ve video çerçeveleri karıştırmak için.
- Dinamik-FPS örnekleme: verilen (durum, bütçe, hareket_ seviyesi), FPS seçin ve çerçeve zaman damgaları gönderin.
- Oyuncak bir Qwen2.5VL JSON çıkış analizörü, koordinat alanları ile araç çağrıları yanıtları işliyor.

## Gönderin.

Bu ders bize çok yararlı .`outputs/skill-qwen-vl-pipeline-designer.md`. Bir video görevi (önetici, ajan, eylem tanıma, erişilebilirlik) verildiğinde, Qwen2.5 VL yapılandırmasını (cadre bütçesi, FPS stratejisi, pencere dikkatliliği bayrağı, ajan çıkış modunu) ve gecikme tahminini yayar.

> **【中文解读】**Bu dersden çıkıyor Qwen-VL borusu  tasarım araçları 给定视频任务(监控、代理、动作识别、无障碍),输出 Qwen2.5VL 配置(预算、FPS 策略、窗户注意力标志、代理输出模式)

## Egzersizler.

1. Bir yama için M-RoPE dönüşümlerini (t=3, h=5, w=7) gizli 48 (16 per bant, temel theta 10000) ile hesaplayın.
   | 计算 (t=3, h=5, w=7) 补丁的 M-RoPE 旋转，隐藏维度48（每频段16），基数10000。展示每频段前三对的旋转角度。

2. 10 dakikalık güvenlik kamerası 1 FPS'de kaydetmek kaç çorap üretir? 3x havuzlu 384 çözünürlükte toplam kaç token? Qwen2.5 -VL'nin varsayılan 32k bağlamı bunu işliyor mu?
   | 10分钟安防摄像头录像在 1FPS 下产生多少帧？384分辨率+3x池化后多少 token？Qwen2.5-VL 默认 32k 上下文能处理吗？

3. 30 saniyelik tenis rallisi için FPS'i 30 saniyelik tarif demo ile 30 saniyelik UI ajanı kayıtları karşılaştırın.
   | 为 30 秒网球比赛、30 秒食谱演示、30 秒 UI 代理录像选择帧率。用动态帧率逻辑论证每个选择。

4. Qwen2.5VL, Q-Former'ı tamamen düşürüyor. Neden basit bir MLP 2025'te çalışacak ama 2023'te çalışmayacak?
   | Qwen2.5-VL 完全去掉了 Q-Former。为什么 MLP 在 2025 年可行但 2023 年不行？（提示：数据规模和编码器质量。）

5. Üç Qwen2.5-VL JSON araç çağrı çıkışlarını Python diktlerine ayırın. Yanlış biçimlendirilmiş JSON'da ne eksikliği var ve Qwen yemek kitabı hangi kurtarma stratejisini önerir?
   | 将三个 Qwen2.5-VL JSON 工具调用输出解析为 Python 字典。畸形 JSON 会出什么问题？Qwen 食谱推荐的恢复策略是什么？

## Anahtar Terimler

| Term | What people say | What it actually means | 中文含义 | 中文释义 |
|------|-----------------|------------------------|----------|---------|
| M-RoPE | "Multimodal RoPE" | 3D rotary position embedding with temporal, height, and width bands in the hidden dim | 三维旋转位置编码，隐藏维度分时间、高度、宽度三个频段 | |
| Dynamic FPS | "Smart sampling" | Frame sampling rate chosen per video based on motion, duration, and token budget | 根据运动量、时长和 token 预算动态选择帧率 | |
| Absolute time token | "Timestamp token" | `<time>t</time>` interleaved in the sequence so the model sees actual seconds not frame index | 在序列中插入真实时间戳 token | |
| Window attention | "Local attention" | Spatial self-attention restricted to small windows for speed; global attention added periodically | 空间自注意力限制在小窗口内加速，周期性加入全局注意力 | |
| Structured agent output | "JSON mode" | Training data supervision teaching the VLM to emit parseable JSON with coords and tool names | 训练 VLM 输出可解析的 JSON（含坐标和工具名） | |
| min_pixels / max_pixels | "Resolution bounds" | Per-request Qwen2.5-VL controls bounding total pixel count and therefore token count | 按请求控制最小/最大像素数从而控制 token 数 | |
| Grounding | "Point-at-it" | Outputting bounding-box coordinates as text tokens; used since Qwen-VL v1 | 输出边界框坐标作为文本 token，从 Qwen-VL v1 开始支持 | |

## Daha fazla okumak

- [Bai et al. — Qwen-VL (arXiv:2308.12966)](https://arxiv.org/abs/2308.12966)# Qwen-VL # İlk Nesil
- [Wang et al. — Qwen2-VL (arXiv:2409.12191)](https://arxiv.org/abs/2409.12191)# Qwen2-VL M-RoPE
- [Qwen Team — Qwen2.5-VL Technical Report (arXiv:2502.13923)](https://arxiv.org/abs/2502.13923) Qwen2.5VL  动态率
- [Qwen Team — Qwen3-VL (arXiv:2511.21631)](https://arxiv.org/abs/2511.21631) Qwen3-VL                                                                                                                                                                                                                                                            
- [Zhu et al. — InternVL3 (arXiv:2504.10479)](https://arxiv.org/abs/2504.10479) InternVL3  Referans
