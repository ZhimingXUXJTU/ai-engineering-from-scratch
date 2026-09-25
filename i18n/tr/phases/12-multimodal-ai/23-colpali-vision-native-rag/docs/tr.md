# ColPali ve Vision-Native Doküman RAG

> Geleneksel RAG PDF'leri metneye ayırır, parçalara ayırır, parçaları yerleştirir, vektörleri saklar. Her adım sinyal kaybeder: OCR tablo verilerini düşürür, parçalanma tablo satırlarını kırar, metin yerleştirmeleri rakamları görmezden gelir. ColPali (Faysse et al., Temmuz 2024) daha basit bir soru sordu: Neden metni çıkarmak? Sayfa resmini doğrudan PaliGemma üzerinden yerleştirin, arama için ColBERT tarzı geç etkileşimi kullanın ve belgenin taşıdığı tüm düzen, rakamlar, şifre ve biçimlendirme sinyalini koruyun. Yayınlanan referans değerleri: Görsel açıdan zengin belgelerdeki metin-RAG'den yüzde 20-40 daha iyi bir son-son doğruluk. ColQwen2, ColSmol ve VisRAG bu kalıpı genişletti. Bu ders, görme doğası RAG tezini okuyor ve küçük bir ColPali benzeri bir indeks oluşturur.

> **【中文解读】**传统RAG PDF'de performansı kötüdür, çünkü her adım kayıp sinyallerde bulunur:OCR 丢图表、分块破坏表格行、文本嵌入忽略图片。ColPali 问了一个更简单的问题: neden文本提取?

> **【拓展：ColPali 在金融 RAG 中的应用】**Finansal raporlar en tipik görsel zenginlik belgesi Q3  Gelir artışı genellikle grafiklerde, sözleşme imzası blokları düzen gerçekleri değil metin gerçekleri olacaktır. ColPali  doğrudan sayfa görüntüsüne yerleştirilmiş, tam görsel sinyalleri koruyan, finansal raporlara çok uygun  sözleşme  gönderme ve benzeri durumlara ️ depo açılış satışları metin RAG'nin 5-10 katı olacaktır ️ PQ sıkıştırılmasından sonra), ancak doğru değer oranında yükselme genellikle bu maliyeti kazanır.

**Type:** Build
**Languages:** Python (stdlib, multi-vector indexer + MaxSim scorer)
**Prerequisites:** Phase 11 (LLM Engineering — RAG basics), Phase 12 · 05 (LLaVA)
**Time:** ~180 minutes

>  **【前置】**Önemli bir şekilde, bu süreçte, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir sürece, bir sürece, bir sürece, bir sürece, bir sürece, bir sürecececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececece
>  **【类比】**传统 RAG vs ColPali = "看书先扫描成纯文本" vs "直接看图找答案"──传统 = OCR 提取文字→分块→embedding(图表数据全部丢失);ColPali = 直接对页面图像做补丁嵌入(图表、表格、布局全保留)──

## Öğrenme Hedefleri

- İki kodlayıcı çekim (her belgeye bir vektör) ve geç etkileşim çekim (her belgeye birçok vektör) arasındaki farkı açıklayın.
  Çinçe Çevirimi: açıklama iki kodlayıcı çekim (per dosya bir sekme) ve geç geçiş tartışma çekim (per dosya bir çok sekme) arasındaki farkı.
- ColBERT'in MaxSim işlevi ve ColPali'nin onu metin jetonlarından görüntü yamalarına nasıl genelleştirdiğini açıklayın.
  中文翻译:描述 ColBERT'in MaxSim 操作以及 ColPali 如何将其从文本代币 推广到图像补丁──
- Küçük bir ColPali benzeri indeksi oluşturun: sayfa → patch yerleştirmeler → MaxSim sorgu terimi yerleştirmeler → top-k sayfalar.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri Çeviri Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri Çeviri Çeviri: Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Ç Ç Çeviri Çeviri Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç
- Faturayı / finansal raporları kullanma durumunda ColPali + Qwen2.5 VL jeneratörü vs. metin-RAG + GPT-4 ile karşılaştırın.
  Çinçe Çevirimiçi: 在发票/金融报告用例上比较 ColPali + Qwen2.5-VL 生成器 vs 文本 RAG + GPT-4──

## Sorunlar. Sorunlar.

PDF'lerde metin-RAG, belgenin büyük kısmını atıyor. Mali raporun üçüncü çeyreklik gelir artışı genellikle bir tabloda bulunur; bir tıbbi raporun bulguları notlı görüntülerde bulunur; yasal sözleşmenin imza bloğu bir metin faktörü değil, bir düzen faktörüdür.

> PDF'deki metin RAG, belge bilgilerini terk etti. Mali Raporların 3. çeyrekinde gelir artışı genellikle tablolarda görülür.

Metin-RAG boru hattı:

> 文本 RAG 管道:

1. PDF → OCR / pdftotext yoluyla metin.
   中文翻译:PDF → 通过 OCR/pdftotext 提取文本。
2. Metin → 300-500 token parçası.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Ç Ç Ç Ç Ç Çeviri Çeviri Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Çeviri Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç
3. Chunk → bi-encoder yerleştirme (bir vektör).
   Çinçe Çevirim:块 → 双编码器嵌入(一个向量)
4. Kullanıcı sorusu → yerleştirme → cosine benzerliği → üst-k parçalar.
   中文翻译: user quer quer query → 嵌入 → 余弦相似度 → top-k 块──
5. Çünks + sorgu → LLM.
   中文翻译:块 + 查询 → LLM。

Beş kayıp adım, grafiği yakalamamış, tablolar parçalara ayrılmış, sütun düzeni düzeni, resim notları kaybolmuş.

> 5 五有损步骤──图表未捕获──图表被块截截断──多布局被展平──图表注释消失──

ColPali'nin düzeni: OCR'yi atlayın, sayfa resmini doğrudan yerleştirin. Arama sırasında model ince tanelerli yamalara bakabilmesi için ColBERT tarzı geç etkileşimi kullanın.

> ColPali'nin düzeni: OCR'den atlayın, doğrudan sayfa görüntüsüne yerleştirin.

## Konsepten bir şey.

> **【中文解读】**ColPali, RAG'yi saf görsel yöntemle gerçekleştirir: OCR üzerinden geçmeden, doğrudan dosya sayfasını görüntü kodlaması olarak, görsel benzerlik araması ile oluşturur. ColPali'nin temel yeniliği MaxSim 模式query'in her token'i dosya sayfasının her patch'ına en fazla benzerlik uyumluluğu için yerleştirir ve ardından da aramak için birlikte oluşturur.

> **【拓展：视觉原生 RAG 的优势**传统RAG管线(OCR -> 文本 -> 嵌入 -> 检索) on复杂版面(表格、图表、公式) on frequently fail;;ColPali 直接在视觉层次匹配,无需OCR,在包含图表和表格的文档检索上上传统方法提升 30-50%──缺点是需要更多存储(每页一个向量)


> **【拓展：ColPali 的效率分析】**ColPali, arama gecikmesiyle geleneksel yöntemle eşdeğerdir (yaklaşık 50 ms/sorgusu), ancak tablo ve tablo içeren dosyalarda doğruluk oranı %30-50 arttı.


### Colbert (2020)

ColBERT (Khattab & Zaharia, arXiv:2004.12832) bir metin kurtarma yöntemi.

> ColBERT bir metin kontrol yöntemidir.

- Sorgu simgelerinin kendi gömülmeleri (N_q vektörleri) vardır.
  Çinçe Çevirim:K sorgu simgesi  get your own嵌入
- Belge simgelerinin gömülmeleri (N_d vektörleri, tipik olarak önbelleğe alınır).
  Çinçe Çevirimiçi:文档代币 获得嵌入
- Not = cosine benzerliği olan dosya tokenlerine karşı maksimum sorgu tokenlerinin toplamı: Σ_i max_j cos(q_i, d_j).
  Çine çevirisi:分数 = 求和,每个查询代币 取文档代币 中最大余弦相似度:Σ_i max_j cos(q_i, d_j) 』

Bu MaxSim işlevi. Her sorgu simgesi en uygun belge simgesini "seçiyor". Son puan toplamdır.

> İşte MaxSim'in işlevi. Her sorgu simgesi en uygun dosya simgesi seçilir.

Avantajlar: güçlü hatırlama, terim seviyesindeki semantikleri ele alır. Eksileri: Doküman başına N_d vektörleri, depolama pahalı.

> 优势:强召回率,处理词级语义――劣势: 每文档 N_d 个向量,储存昂贵――

### KolPali

ColPali (Faysse et al., arXiv:2407.01449) ColBERT örneğini görüntülere uyguluyor.

> ColPali, ColBERT'in resimlere uygulanacağı bir model oluşturdu.

- Her sayfa PaliGemma (ViT + dili) tarafından patch yerleştirmelerine kodlanır: Sayfa başına N_p vektörleri.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri Çeviri: Çeviri Çeviri: Çeviri Çeviri: Çeviri Çeviri: Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri: Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Çeviri Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç
- Her kullanıcı sorgu (metin) sorgu-tökeni yerleştirmelerinde kodlanır: N_q vektörleri.
  Çine çevirisi: her kullanıcı sorusu (文本) 编码为查询代币 嵌入:N_q 个向量。
- Skor = Σ_i max_j cos(q_i, p_j), yani, MaxSim sorgu metin-token ve sayfa-resim-patçlar üzerinde.
  Çine çevirisi:分数 = Σ_i max_j cos(q_i, p_j),即查询文本代币 和页面图像补丁的 MaxSim。
- Top-k sayfaları toplam puanla alın.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri

Belgeyi yedikten sonra: her sayfayı PaliGemma ile yerleştirin, tüm patch yerleştirmelerini saklayın. Sorgu zamanı: sorgu simgelerini yerleştirin, MaxSim'i tüm kaydedilen sayfa yerleştirmelerine karşı hesaplayın, üst-k sayfaları geri gönderin.

> 文档摄取时: PaliGemma kullanılarak 嵌入每页,存储所有补丁 嵌入──查询时:嵌入查询代币,对所有存储的页面嵌入计算MaxSim,返回顶-k页面──

Avantajlar: görsel açıdan zengin belgelerde son-sonun RAK metnini %20-40'a geçiyor. Her patch-vector yerel düzen ve içeriği yakalar.

> 优势:端到端在视觉丰富文档上文RAG Yüksek %20-40── her yama 向量捕获局部布局和内容──

Eksiler: N_p yamalar × 4 bayt yüzen × D-dim vektörleri sayfaya = depolama hızla büyüyor.

> 劣势:N_p 个补丁 × 4 字节浮点 × D 维向量每页 = 储存快速增长──可通过 PQ/OPQ 量化缓解──

### ColQwen2 ve ColSmol

ColQwen2 (illuin-tech, 2024-2025) PaliGemma'yı Qwen2-VL'ye değiştirir. Daha iyi temel kodlayıcı, daha iyi geri alınma.

> ColQwen2 PaliGemma'yı Qwen2-VL'ye değiştirecek. Daha iyi bir temel kodlayıcı, daha iyi bir kontrol.

ColSmol, yerel / kenar kullanım için daha küçük ölçekli bir varyandır. ~ 1B parametreleri olan bir ColSmol retriever tüketici GPU'da çalışır.

> ColSmol, yerel/ sınır kullanımına yönelik daha küçük bir değişimdir.

### VisRAG

VisRAG (Yu et al., arXiv:2410.10594) farklı bir variandır: MaxSim yerine, her sayfayı VLM ile tek bir vektöre birleştirin ve sonra iki kodlayıcıyı geri alın.

> VisRAG farklı bir varyasyon: bir patch üzerinde MaxSim yapmak değil, VLM ile her sayfayı tek bir yönlü yeniden ikili kodlayıcı olarak kontrol eder.

Kalite karşı maliyet karşılığı: Kalite için ColPali, ölçek için VisRAG.

> 质量与成本的权衡:ColPali 追求质量,VisRAG 追求规模──

### M3DocRAG

M3DocRAG (Cho et al., arXiv:2411.04952) çok sayfalık çok belge akıl yürütmesine çok modal geri almayı genişletiyor.

> M3DocRAG, çoklu bir arşiv araştırmasını çoklu bir arşiv araştırmasına yayımlayacak.

### ViDoRe  referans değer

ColPali'nin eş göstergesi. Görsel Belge İzleme Değerlendirme. Görevler finansal raporlar, bilimsel makaleler, idari belgeler, tıbbi kayıtlar, el kitabları içerir.

> ColPali'nin配套基准──视觉文档检索评估──任务包括金融报告、科学论文、行政文件、医疗记录、手册──标签:nDCG@5──

ColPali-v1 ViDoRe'de %80 nDCG@5 puanı verir; aynı belgelerdeki metin-RAG %50-60 puanı verir.

> ColPali-v1 on ViDoRe 上約80% nDCG@5;文本 RAG on the same文档上約50%-60%──

### Sonundan sonuna kadar olan RAG boru hattı

Görme doğası olan bir RAG için:

> 视觉原生 RAG 管道:

1. İçecek: PDF → sayfa görüntüleri → PaliGemma kodlama → tüm yama gömülmeleri saklamak.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç
2. Sorgu: Kullanıcı metni → sorgu-token yerleştirmeleri → Tüm indekslenmiş sayfalara karşı MaxSim → üst-k sayfalar.
   Çeviri: Çeviri: User文本 → Çeviri simgesi 嵌入 → Tüm indeks sayfaları için yap MaxSim → üst-k ページ。
3. Yarat: üst-k sayfa görüntüleri + sorgu → VLM (Qwen2.5-VL veya Claude) → cevap.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Ç Ç Ç Çeviri: Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç

Şekiller, tablolar, şifre, düzen tümü cevapta akıyor.

> Tüm yollar OCR'si yok.

### Kaydetme matematikleri

Sayfa başına 729 patch ve 128 boyutlu yerleştirmeler ile 50 sayfalık bir finansal rapor:

> 50 sayfa finans rapor, her sayfa 729 个补丁,128 维嵌:

- ColPali: 50 * 729 * 128 * 4 byte = ~18 MB çiğ, ~4 MB PQ'den sonra.
  中文翻译:ColPali:50 * 729 * 128 * 4 字节 = 约18 MB 原始,PQ 后约4 MB。
- Metin-RAG: 50 parça * 768-dim * 4 byte = ~ 150 kB.
  中文翻译:文本 RAG:50 块 * 768 维 * 4 字节 = yaklaşık 150 kB。

ColPali, bir belge için ~ 30 kat daha fazla depolama alanı içerir. Ölçüsünde, OPQ / PQ genellikle tolere edilebilir olan ~ 5-10 katı azaltır.

> ColPali Her dosya depolama alanı yaklaşık 30 倍 ⋅ Büyük boyutta, OPQ/PQ genellikle 5-10 ⋅ kadar düşer.

### SMS-RAG hala kazanırken

- Çatlama sinyali olmayan saf metin belgeler (wiki makaleler, sohbet güncellemeleri).
  Çinçe Çevirimiçi:无布局信号的纯文本文档(维基文章、聊天记录) 』文本 RAG 更简单且存储更便宜──
- Milyonlarca sayfalık arşivler, depolama maliyetleri üzerinde baskın.
  Çinçe Çevirisi:数百万页档案, depolama maliyeti
- Çıkarılabilir OCR metnini geri almakla birlikte talep eden sıkı düzenlemel gereksinimler.
  Çinçe Çevirisi:严格要求可提取 OCR 文本与检索并存的监管要求.

2026'da her şey için  finansal raporlar, bilimsel makaleler, yasal sözleşmeler, tıbbi kayıtlar, UX belgeleri  vizyon doğası RAG kazanır.

> 2026 yılının diğer tüm olayları  Finansal rapor  科学论文 法律合同 医疗记录  UX 文档 视觉原生 RAG 胜出──

## Çerçeveyi kullanın.
```figure
mm-maxsim
```

## Kullan

`code/main.py`- ...

- Oyuncak yama kodlayıcı: bir "sayfa" (karakter vektörlerinin küçük bir şebekesi) bir dizi yama gömülmesine haritası yapar.
  Çinçe Çevirimi: oyuncak yama 编码器:将"页面" ({{lang-en}})
- MaxSim puanlayıcı: sorgu simgesi yerleştirme seti ile bir sayfa yama seti arasında ColBERT tarzı puanı hesaplar.
  Çeviri: MaxSim 评分器:计算查询代币 嵌入集和页面补丁集 集之间 ColBERT 风格分数──
- 5 oyuncak sayfasını indeksiyor, 3 sorgu yapıyor, puanlarla en üst düzeyde.
  Çin Çeviri: 5 oyuncak sayfa, 3 sorgu, geri dönüm

## İndirin . Ürünler .

Bu ders bize çok yararlı .`outputs/skill-vision-rag-designer.md`. Bir belge-RAG projesini göz önüne alarak ColPali / ColQwen2 / VisRAG / text-RAG'i seçer ve depolama alanını boyutlandırır.

> 本课产 出 `outputs/skill-vision-rag-designer.md`△给定文档 RAG 项目,选择 ColPali / ColQwen2 / VisRAG / 文本 RAG 并估算存储──

## Egzersizler.

1. 200 sayfalık yıllık rapor, sayfada 729 patch, 128 boyutlu emb, 4 baytlı yüzer. Çiğ depolama ve PQ sıkıştırılmış (8x) depolama hesaplama. 200 sayfa yıllık haber, 729 patch/page,128 维嵌入,4 字节浮点──计算原始储和 PQ 压缩(8 倍) 後的储──

2. MaxSim = Σ_i max_j cos(q_i, p_j). Bu toplam basit bir benzerlik anlamı olmayan neyi yakalar? MaxSim = Σ_i max_j cos(q_i, p_j) ・・・

3. ColPali sayfaları birleştirme seti olarak indeksiyor. Eğer sözcük düzeyinde indeksi yaparsak ne değişir (ColBERT yapar)?

4. 1M sayfalık bir korpus için son-son boru hattını tasarlayın ve her soruya 500 ms gecikme bütçesi ile. ColQwen2 / VisRAG'i seçin ve haklı çıkarın.

5. M3DocRAG'ı okuyun (arXiv:2411.04952). Çok sayfalık dikkat kalıbını ve tek sayfalık ColPali'den nasıl farklı olduğunu açıklayın.

## Anahtar Şartlar .

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|------------------------|---------|
| Late interaction | "ColBERT-style" 延迟交互 | Retrieval using per-token or per-patch embeddings + MaxSim, not a single doc vector 使用逐 token/patch 嵌入 + MaxSim 的检索，非单向量 | |
| MaxSim | "Max-over-patches" 最大相似度 | For each query token, pick the highest-similarity document token; sum across query 对每个查询 token 选最高相似度的文档 token；跨查询求和 | |
| Bi-encoder | "Single-vector" 双编码器 | One vector per document; faster but loses granularity 每文档一个向量；更快但丢失粒度 | |
| Multi-vector | "Many-vectors-per-doc" 多向量索引 | Store N_p vectors per document / page; storage cost grows but recall improves 每文档/页存储 N_p 个向量；存储增长但召回提升 | |
| Patch embedding | "Page feature" 图像块嵌入 | One vector per image patch from a VLM encoder, cached per page VLM 编码器输出的每 patch 一个向量，按页缓存 | |
| ViDoRe | "Vision doc bench" 视觉文档检索基准 | ColPali's benchmark suite for visual document retrieval ColPali 的视觉文档检索基准套件 | |
| PQ quantization | "Product quantization" 乘积量化 | Compression that maintains vector similarity while shrinking storage ~8x 保持向量相似度的同时压缩存储约 8 倍 | |

## Daha fazla okumak

- [Faysse et al. — ColPali (arXiv:2407.01449)](https://arxiv.org/abs/2407.01449)
- [Khattab & Zaharia — ColBERT (arXiv:2004.12832)](https://arxiv.org/abs/2004.12832)
- [Yu et al. — VisRAG (arXiv:2410.10594)](https://arxiv.org/abs/2410.10594)
- [Cho et al. — M3DocRAG (arXiv:2411.04952)](https://arxiv.org/abs/2411.04952)
- [illuin-tech/colpali GitHub](https://github.com/illuin-tech/colpali)
