# Belge ve Şekil Anlayışı

> Belgeler fotoğraf değil. PDF, bilimsel makale, fatura veya el yazılı bir form, basit bir görüntü anlayışının yakalayamayacağı bir düzen, tablolar, şkaflar, ayaknotlar, başlıklar ve anlamlı bir yapıya sahiptir. VLM öncesi yığın bir boru hattıydı: Tesseract OCR + LayoutLMv3 + masa çıkarma heuristikleri. VLM dalgası, doğrudan yapılandırılmış işaretleme yaydığı OCR-sizdir modelleri  Donut (2022), Nougat (2023), DocLLM (2023)  ile değiştirdi. 2026 yılına kadar sınır sadece "sayfa görüntüsünü Claude Opus 4.7'e 2576px doğal olarak besle" ve yapılandırılmış işaretleme çıkışı ücretsiz olarak gelir. Bu ders, belgeler AI'nin üç çağlı yayını okuyor.

> **【中文解读】**文档不是照片──PDF、论文、发票、手写表单有布局、表格、图表、脚注、标题等语义结构,普通图像理解无法捕捉──文档 AI 经历了三个时代:(1) OCR 管道(Tesseract + LayoutLMv3);(2) OCR-free(Donut、Nougat 直接从图像生成结构化输出);(3) VLM 原生(2026 yılında doğrudan sayfa görüntüleri 给Claude Opus 4.7 即可)

> **【拓展：文档理解在金融领域的应用】**Finansal sahne, AI'nin en önemli uygulama alanlarından biridir: E-Boksat Çözümü:  Automatic提取供应商、金额、税率) 合同审查条款比对、风险标记) 财务报表提取 资产负债表、利表的结构化数据抽取)  KYC 文档处理身份证、营业执照的自动识别)  2026 yılının önerisi: 纯印发票用 LayoutLMv3 低成本),混合文档用手写VLM 原生 PaliGemma 2 或 Qwen2.5-VL),监管场景用OCR + VLM 交叉验证

**Type:** Build
**Languages:** Python (stdlib, layout-aware document parser skeleton)
**Prerequisites:** Phase 12 · 05 (LLaVA), Phase 5 (NLP)
**Time:** ~180 minutes

>  **【前置】**Önemli olan, herhangi bir yüksek çözünürlük, dosya için önemlidir) 5.08-Fase LayoutLM 系列文档布局模型) ・・・文档 AI VLM'in yüksek değerli uygulamaları, finansal durum özellikle önemlidir。
>  **【类比】**文档理解三时代 = "Hesaba raporunun gelişi"。OCR 管道 = 人工核对+表格软件(先识别文字再解析布局);OCR-free(Donut) =統合化软件(看图直接生成结构化数据);VLM 原生(Claude) = 全能AI(看图就能理解、回答、推理,无需专门训练)。
> ️ **【易错点】**简单 OCR 任务用VLM = 杀用牛刀(成本 10倍) 例如纯文本发票用Tesseract + LayoutLMv3 只需几分钱, GPT-4V 要几毛钱──修复:先评估任务复杂度,简单的OCR管道,复杂的(手写、混合布局、多语言)才上VLM──

## Öğrenme Hedefleri

- Belge AI'nin üç çağını açıklayın: OCR boru hattı, OCR-sizgisel, VLM-dev.
  Çine dilinde: Çine dilinde: Çine dilinde: Çine dilinde: Çine dilinde: Çine dilinde: Çine dilinde: Çine dilinde: Çine dilinde: Çine dilinde: Çine dilinde: Çine dilinde: Çine dilinde: Çine dilinde: Çine dilinde: Çine dilinde: Çine dilinde: Çine dilinde: Çine dilinde: Çine dilinde: Çine dilinde: Çine dilinde: Çine dilinde: Çine dilinde: Çine dilinde: Çine dilinde: Çine dilinde: Çine dilinde: Çine dilinde: Çine dilinde: Çine dilinde: Çine dilde: Çine dilde: Çine dilde: Çine dilde: Çine dilde: Çine dilde: Çine dilde: Çine dilde: Çine dilde: Çine dilde: Çine dilde: Çine dilde: Çine dilde: Çine dilde: Çine dilde: Çine dilde: Çine dilde: Çine dilde: Çine dilde: Çine dilde: Çine dilde: Çine dilde: Çine dilde: Çine dilde: Çine dilde: Çine dilde: Çine dilde: Çine dilde: Çine dilde: Çine Çine dilde: Çine Çine Çine Çine Çine Çine Çine Çine Çine Çine Çine Çine Çine Çine Çine Çine Çine Çine Çine Çine Çine Çine Çine Çine Çine Çine Çine Çine Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç
- LayoutLMv3'ün üç giriş akışını açıklayın: metin, düzen (bbox), görüntü yamaları, birleşik maskelendirme ile.
  Çeviri: LayoutLMv3'ün üç giriş akışı:文本、布局(bbox)、图像补丁,配合统一掩码──
- Donut (OCR-free, image → markup), Nougat (bilimsel makale → LaTeX), DocLLM (layout-aware generative), PaliGemma 2 (VLM-native) ile karşılaştırın.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Ç Ç Ç Ç Çeviri: Çeviri: Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç
- Yeni bir görev için bir belge modeli seçin (faktürler, bilimsel makaleler, el yazılı formlar, Çin kviteleri).
  Çin Çeviri: Çin Çeviri: Çin Çeviri: Çin Çeviri: Çin Çeviri: Çin Çeviri: Çin Çeviri: Çin Çeviri: Çin Çeviri: Çin Çeviri: Çin Çeviri: Çin Çeviri: Çin Çeviri: Çin Çeviri: Çin Çeviri: Çin Çeviri: Çin Çeviri: Çin Çeviri: Çin Çeviri: Çin Çeviri: Çin Çeviri: Çin Çeviri: Çin Çeviri: Çin Çeviri: Çin Çeviri: Çin Çeviri: Çin Çeviri: Çin Çeviri: Çeviri: Çin Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri Çeviri: Çeviri Çeviri: Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Ç Ç Çeviri Çeviri Çeviri Ç Ç Çeviri Çeviri Ç Ç Ç Ç Çeviri Ç Ç Ç Ç Ç Ç Ç Ç Çeviri Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç

## Sorunlar. Sorunlar.

"Bu PDF'yi anlamak" aldatıcı bir şekilde zor.

> "Bu PDF'i anlamak" sanki basit bir gerçekte zor.

- Metin içeriği (sinyalın %90'ı).
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri Çeviri Çeviri Çeviri Çeviri: Ç Ç Ç Ç Çeviri Çeviri Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç
- Düzenleme (başlıklar, ayaknotlar, yan çubuqlar, iki sütun biçimi).
  Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çev
- Tablolar (sır, sütunlar, birleşik hücreler).
  Çine dilinde:表格(行、列、合并单元格)
- Resimler ve şablonlar.
  Çeviri ve resim.
- El yazılı notlar.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri
- Yazı tipi ve tipografi (başlık vs. vücut).
  Çine dilinde:字体和排版

Faturayı önemseyen bir sistem, alt sağdan değil, alt sağdan "Total: $1,245" geldiğini bilmelidir.

> OCR sadece metni çekip, kalan bilgiyi kaybeder.

## Konsepten bir şey.

> **【中文解读】**文档和图表理解是多模态 AI'nin önemli uygulama sahnesini:OCR、表格提取、流程图解读、公式识别等──关键技术:高分辨率输入 (高分辨率输入) 保存文字清晰度 (文字清晰度) 版面分析 (版面分析) 文档结构 (文档结构) 文档结构 (文档结构) 文档结构 (文档结构) 文档结构 (文档结构) 图解读 (图解读) 图解读 (图解读) 公式识别等──关键技术:高分辨率输入 (高分辨率输入) 文档与图表理解是多模态 AI'nin önemli uygulama场景:OCR、表格提取、流程图解读、公式识别等──关键技术:高分辨率输入 (文字清晰度保留) 版面分析 (文档结构理解) 文档结构 (文档结构化输出) 视觉信息将视觉信息转换为可处理的格式) ⋅

> **【拓展：文档 AI 的工业应用**文档 AI 市場巨型:合同审核、发票处理、学术论文分析等──GPT-4o DocVQA'da 92.8%'e ulaştı,InternVL2-26B'de 92.7%'e ulaştı.


> **【拓展：文档理解的技术路线】**文档理解有两条路线:(1) OCR-first(先用 OCR 提取文本,再用 LLM 处理) 适合纯文本文档;(2) Vision-first(直接用 VLM 处理文档图像)适合包含图表、表格的复杂版面── GPT-4o 和 InternVL2 走 Vision-first 路线,在复杂文档理解上表现更好──


### 1. dönem  OCR boru hattı (2021 yılına kadar)

Klasik bir yığın:

> 经典技术:

1. PDF → resim sayfası başına.
   Çeviri:PDF → Her sayfa görüntü
2. Tesseract (veya ticari OCR) kelimenin bir harfi sınırlama kutuları ile metni çıkarır.
   Çine dilinde:Tesseract (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tesseract) (Tessera) (Tessera) (Tessera) (Tesseract) (Tessera) (Tessera) (Tessera) (Tessera) (Tessera) (Tessera) (Tessera) (Tessera) (Tessera) (Tessera) (Tessera) (Tessera) (Tessera) (Tessera) (T
3. Layout analizitörü blokları tanımlar (başlık, tablo, paragraf).
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri
4. Masa yapısı tanıtıcısı masaları analiz eder.
   Çinçe Çevirisi:表格结构识别器解析表格。
5. Alan kuralları + regex çekim alanları.
   Çinçe Çevirimiçi: 领域规则 + 正则表达式提取字段。

Temiz basılı metin için çalışır. El yazısı, eğri tarama, karmaşık tablolar, İngilizce olmayan senaryolar için. Her başarısızlık modunda özel bir istisna yolu gerekir.

> 适用于清洁印刷文本──在手写、倾斜扫描、复杂表格、非英文文字上失败──每种失败模式都需要自定义异常处理──

### TrOCR (2021)

TROCR (Li et al., arXiv:2109.10282) Tesseract'in klasik CNN-CTC'ini sentetik + gerçek metin görüntülerinde eğitilmiş bir transformatör kodlayıcı-dekoderle değiştirdi. El yazılı ve çok dilli metin üzerinde temiz kazanç. Hala bir boru hattı (detektor sonra TrOCR sonra düzen), ancak OCR adımları çarpıcı bir şekilde iyileşti.

> TESERACT'in klasik CNN-CTC'ini değiştiren Transformer 编码器-解码器, TESERACT'in el yazısı ve çok dilli metinlerinde belirgin bir avantaj elde etti.

### 2. Çağ  OCR-den uzak (2022-2023)

İlk OCR-siz modeller şöyle dedi: tespit tamamen atlatın, görüntü piksellerini doğrudan yapılandırılmış çıkışa haritasın.

> İlk nesil OCR 模型 önerilen: tamamen atladı test, doğrudan görüntü görüntülerini yapısal olarak görüntüleyecektir

Donut (Kim et al., arXiv:2111.15664):
- Kodlayıcı-dekoder transformatörü, kodlayıcı Swin-B.
- Çıktı, form anlayışı için JSON, özetleme için markdown veya herhangi bir görev-özel şema.
- OCR yok, düzen yok, tespit yok.

> Donut:编码器-解码器 Transformer,编码器为 Swin-B──输出是 JSON(表单理解)、标记down(摘要) 或任务特定方案──无需 OCR、无需布局、无需检测──

Nougat (Blecher et al., arXiv:2308.13418):
- Özellikle bilimsel makaleler üzerine eğitim almış.
- Çıktım, LaTeX / markdown.
- Eklentiler, çok sütunlu düzen, rakamlar.
- Arxiv-parser'ın her çağrısı olan model.

> Nougat:专门在科学论文上训练──输出 LaTeX/markdown──处理公式、多布局、图表──每个 arXiv 解析器都调用此模型──

Bunlar uzmanlar, genelciler değil. Bilimsel bir makalede çörek başarısız olur.

> Bunlar uzman modeller, yetenekler değil.

### LayoutLMv3 (2022)

LayoutLMv3 (Huang et al., arXiv:2204.08387) OCR'yi korur ancak düzen anlayışını ekler:

> Yol değişikliği. Lv3'ün düzeni OCR'yi koruyor.

- Üç giriş akışı: OCR metin işaretleri, her işaret için 2D sınırlama kutuları, görüntü yamaları.
  中文翻译:三个输入流:OCR 文本代币、每个代币的2D 边界框、图像补丁──
- Üç modalitede de maskeli eğitim amacı (maskeli metin, maskeli yamalar, maskeli düzen).
  Çinçe Çevirimiçi:跨三个模态的掩码训练目标(掩码文本、掩码补丁、掩码布局)
- Aşağı akıntı: sınıflandırma, kurum çıkarımı, tablo QA.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri Çeviri: Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Ç Ç Çeviri Çeviri Çeviri Ç Ç Ç Ç Ç Çeviri Ç Ç Ç Ç Ç Ç Ç Çeviri Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç

LayoutLMv3 OCR tabanlı belge anlayışının zirvesidir. Formlar ve faturalarda güçlü. OCR'yi akıntılı bir şekilde gerektirir. Standartlaştırılmış belge referansları üzerinde en iyi VLM öncesi doğruluk.

> LayoutLMv3 OCR'e dayalı dosya anlayışının zirvesidir.

### Doküman (2023)

DocLLM (Wang et al., arXiv:2401.00908) LayoutLM'in doğuşcu kardeşidir.

> DokLLM LayoutLM'in oluşturma biçimidir.

### 3. dönem  VLM-devli (2024+)

2024'te VLM'ler tüm boru hattını değiştirmek için yeterince iyi hale geldi.

> 2024 yılında VLM  yeterince iyi hale geldi, tümüyle tüpü değiştirebilir.

- LLaVA-NeXT 336-til AnyRes küçük belgeler için çalışır.
  中文翻译:LLaVA-NeXT 336-tile AnyRes 适用于小文档。
- Qwen2.5VL dinamik çözünürlük 2048+ piksel doğuştan ele alıyor.
  Çine Çeviri:Qwen2.5VL 动态分辨率原生处理 2048+ 像素。
- Claude Opus 4.7 2576px belgeleri destekler.
  中文翻译:Claude Opus 4.7 支持 2576px 文档。
- PaliGemma 2 (April 2025) özel olarak belgelere + el yazısına yönelik eğitimler sunar.
  Çeviri:PaliGemma 2(2025 yıl 4 月) özel olarak文档+手写训练。

VLM-native ve OCR-pipeline arasındaki boşluk hızla kapatıldı. 2026 yılına kadar VLM-native:

> VLM 原生 ve OCR 管leri arasındaki fark hızla azalmıştır. 2026 yılına kadar, VLM 原生 şu yönlerden üstün çıkmıştır:

- Sahne metni (el yazısı + basılı, karıştırılmış senaryolar).
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri
- Birleştirilmiş hücrelerle karmaşık tablolar.
  Çin Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri
- Metinlere gömülü matematik denklemleri.
  Çin Çeviri: 嵌入文本的数学公式──
- Metin notları olan figürler.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri

OCR boru hattı hala kazanıyor:

> OCR 管道 hala aşağıdaki yönlerden başarısız:

- Sayfa başına gecikme önemli olduğu büyük ölçekte saf tarama iş yükleri.
  Çinçe Çevirisi: Büyük çaplı saf tarama çalışma yükü, her sayfa geç çok önemlidir.
- Pipeline güvenilirliği (deterministik başarısızlıklar vs. VLM halüsinasyonları).
  Çine dilinde: 管道可靠性 (BİLM)
- Denetim edilebilir OCR çıkışı gerektiren düzenlenmiş ortamlar.
  Çinçe Çevirisi: needs可审计 OCR 输出监管环境。

### Claude 4.7 / GPT-5 sınır

2576 piksellik yerel giriş ile sınır VLM'leri, insan doğruluğuna yakın bir anlayışla belgeler yapmaktadır. 2026 yılının başından itibaren referans rakamları:

> 2576 像素原生输入下,前沿 VLM, insan doğruluğuna yaklaşmak için dosya anlayışı yapmaktadır.

- DocVQA: Claude 4.7 ~ 95.1, PaliGemma 2 ~ 88.4, Nougat ~ 77.3, boru hattı LayoutLMv3 ~ 83.
  Çeviri:DocVQA:Claude 4.7 约 95.1,PaliGemma 2 约 88.4,Nougat 约 77.3,管道式 LayoutLMv3 约 83。
- ÇartQA: Claude 4.7 ~ 92,2, GPT-4V ~ 78.
  ÇartQA:Claude 4.7 约 92.2,GPT-4V 约 78。
- VisualMRC: Claude 4.7 ~ 94.
  Çeviri:VisualMRC:Claude 4.7 约 94。

Kapalı modelde boşluk çoğunlukla çözünürlük ve temel LLM ölçeğindedir. 7B'deki açık modeller birkaç puan geride ama yetişmektedir.

> Kapalı kaynak modeli arasındaki fark, çözünürlük ve temel LLM'nin büyüklüğünde.

### Matematik denklemler ve LaTeX çıkışı

Bilimsel makaleler denklemler için tam LaTeX çıkışına ihtiyaç duyar. Nougat bu konuda eğitildi. LaTeX hedefleri ile eğitilmiş VLM'ler (Qwen2.5-VL-Math, Nougat türevleri) kullanılabilir LaTeX üretir. Açık bir LaTeX eğitimi olmadan, VLM'ler okuyabilir ancak net olmayan transkripsiyonlar üretir.

> 科学论文需要精确的 LaTeX 公式输出──Nougat 在此上训练──使用 LaTeX 目标训练的 VLM(Qwen2.5-VL-Math、Nougat 衍生物) kullanılabilir LaTeX──产生可用的 LaTeX──没有明显的 LaTeX 训练的 VLM 产生可读但不精确的转录──

2026'da bilimsel kağıt boru hattı için: Nougat zinciri PDF'de, sonra da karmaşık sayfalarda VLM.

> 2026 yıl bilim makalesi 管道建议:先用 Nougat 处理 PDF,再用 VLM 处理棘手页面──

### El yazısı

Yine de en zor alt görev. Karışık basılı + el yazılı (doktor notları, doldurulmuş formlar) OCR boru hattının hala maliyet için VLM'leri yendiği yerdir. Sadece el yazılı VLM'ler iyileşmektedir (Klavü 4.7, PaliGemma 2).

> 仍然是最难的子任务──印刷+手写混合(医生笔记、填写的表单) 仍然是最难的子任务──印刷+手写混合(医生笔记、填写的表单) 仍然是 OCR管道在成本上胜过VLM的场景──纯手写VLM正在改进(Claude 4.7、PaliGemma 2)──

### 2026 tarifi

Yeni bir belge-İS projesi için:

> Yeni AI projeleri için:

- Temiz basılmış faturalar ölçeğinde: LayoutLMv3 + kuralları, maliyet-efikas.
  Çeviri: Lv3 + 规则,成本高效──
- Karışık belgeler (bilimsel + el yazılı + formlar): VLM-devde (PaliGemma 2 veya Qwen2.5-VL).
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Ç Ç Ç Ç Ç Ç Ç Ç Çeviri: Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç
- Matematik için Nougat, rakamlar için VLM.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri
- Yönetimsel: OCR borusu + çapraz kontrol için VLM onaylayıcı.
  Çinçe Çevirimiçi:监管场景:OCR 管道 + VLM 验证器交叉检查。

## Çerçeveyi kullanın.
```figure
mm-doc-layout
```

## Kullan

`code/main.py`- ...

- Oyuncak düzenini bilen bir tokenizer: verilen (metin, bbox) çiftler, LayoutLMv3 tarzında giriş üretir.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri Çeviri: Çeviri Çeviri: Çeviri: Çeviri Çeviri: Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri: Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Ç Ç Çeviri Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç
- Donut tarzı görev şeması jeneratörü: Formlar için JSON şablonu.
  Çeviri:JSON 模板.
- OCR-pipeline, Donut, Nougat ve VLM-native üzerinden sayfa başına token bütçelerinin bir karşılaştırması.
  Çinçe Çevirimiçi:OCR 管道、Donut、Nougat 和 VLM 原生之间每页代币 预算的比较。

## İndirin . Ürünler .

Bu ders bize çok yararlı .`outputs/skill-document-ai-stack-picker.md`. Bir belge-AI projesi (domain, ölçek, kalite, düzenlemeler) göz önüne alındığında, OCR boru hattı, OCR-den uzak uzman ve VLM-native arasında seçim yapılır.

> 本课产 出 `outputs/skill-document-ai-stack-picker.md`◊ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒    ⇒ ⇒ ⇒ ⇒ ⇒ ⇒    ⇒ ⇒ ⇒     ⇒ ⇒    ⇒ ⇒      ⇒                                                                                                                                                                                                          

## Egzersizler.

1. Projenin gününde 10 milyon faturası var. Hangi yığın sayfada maliyeti haksızlık olmadan en aza indirir? Projenin günde 1000 milyon teshkiyi işliyor.

2. LayoutLMv3 neden saf CLIP-VLM'leri karşılaştırırken sahne metni için daha düşük performans gösterir?

3. Nougat LaTeX üretir. VLM-mülki çıkışının Nougat'ı LaTeX sadakatinde yendiği bir test vakaını ve Nougat'ın kazandığı bir vaka önerin. Nougat 生成 LaTeX。 Design a VLM 原生输出在 LaTeX 保真度上胜胜胜胜胜 Nougat'ın test üyeleri,以及 a Nougat 胜出的用例。

4. PaliGemma 2 makalesini okuyun (Google, 2024). Hangi temel eğitim verileri eklenmesi belgelerin doğruluğunu PaliGemma 1 ile karşılaştırdı?

5. Bir düzenleyici güvenli hibrit tasarlayın: Birincil olarak OCR boru hattı, ikincil olarak VLM çapraz kontrol.

## Anahtar Şartlar .

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|------------------------|---------|
| OCR pipeline | "Tesseract-style" OCR 管道 | Stage-wise stack: detect -> OCR -> layout -> rules; deterministic, fragile 分阶段栈：检测→OCR→布局→规则；确定但脆弱 | |
| OCR-free | "Donut-style" 无 OCR | Image-to-output transformer that skips explicit OCR; single model 图像到输出的 Transformer，跳过显式 OCR；单一模型 | |
| Layout-aware | "LayoutLM" 布局感知 | Input includes per-token bbox coordinates; unified masking across modalities 输入包含逐 token 的 bbox 坐标；跨模态统一掩码 | |
| VLM-native | "Frontier VLM" VLM 原生 | Feed page image directly to Claude/GPT/Qwen VLM at high resolution; no pipeline 直接将页面图像输入高分辨率 VLM；无需管道 | |
| DocVQA | "Doc benchmark" 文档 VQA 基准 | Document VQA standard; most-cited score 文档 VQA 标准评测；被引用最多的评分 | |
| Markup output | "LaTeX / MD" 标记输出 | Structured output format instead of free-form text; enables downstream automation 结构化输出格式而非自由文本；支撑下游自动化 | |

## Daha fazla okumak

- [Li et al. — TrOCR (arXiv:2109.10282)](https://arxiv.org/abs/2109.10282)
- [Blecher et al. — Nougat (arXiv:2308.13418)](https://arxiv.org/abs/2308.13418)
- [Huang et al. — LayoutLMv3 (arXiv:2204.08387)](https://arxiv.org/abs/2204.08387)
- [Kim et al. — Donut (arXiv:2111.15664)](https://arxiv.org/abs/2111.15664)
- [Wang et al. — DocLLM (arXiv:2401.00908)](https://arxiv.org/abs/2401.00908)
