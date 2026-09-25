# Llama Guard ve Giriş/Içeri Sınıflandırma

> Llama Guard 3 (Meta, Llama-3.1-8B tabanı, içeriğin güvenliği için ince ayarlanmıştır) 8 dilde MLCommons 13 tehlikesi taksonomisine göre hem LLM girişlerini hem de çıkışlarını sınıflandırır. 1B-INT4 kuantistik bir varianti mobil CPU'larda 30'dan fazla token/sekunde çalışır. Llama Guard 4 multimodal (resim + metin), S1S14 kategorisi setiyle genişletilmektedir (S14 Kod Anlatıcı İstifadesi dahil), ve Llama Guard 3 8B/11B'nin bir düşüş değiştiricisidir. NVIDIA NeMo Guardrails v0.20.0 (Ocak 2026) giriş ve çıkış raylarının üstüne Colang iletişim akışı raylarını ekler. Dürüst not: "LLM Guardrails'te Anında Enjeksiyon ve Ceza Eğitimi Algılamaları'nı Uzaklaştırmak" (Huang et al., arXiv:2504.11168) Emoji kaçakçılığı altı tanınmış güvenlik sisteminde %100 saldırı başarısı oranını gösterdi; NeMo Guard Detect, ceza eğitimi sırasında %72.54% ASR kaydetti. Sınıflayıcılar bir katman, bir çözüm değil.

> **【中文解读】**Llama Guard 3(Meta,Llama-3.1-8B 基础,为内容安全微调)对照 MLCommons 13 危害分类法在 8种语言上分类 LLM 输入和输出。1B-INT4 量化变体在移动CPU 上以30+代币/s 运行。Llama Guard 4 是多模态(图像+文本), S1-S14 类集集 (S14 Code Interpreter Abuse dahil),是Llama Guard 3 8B/11B 直接替代──NVIDIA NeMo Guard v0.20.0(2026年01月) 输出护之上添加对话实流护通过提示:"Huggling Injection and Jailbreak Detection in LLM Guard"方案, Huang Guard等等等等 系统, ️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️

> **【拓展：分类器是 Agent 栈最窄点】**LLM 输入输出分类器位于 Agent 最窄的点:每个请求通过、每个响应通过──好分类器层快速、基于分类法、小计算成本捕获大部分明显误用;坏分类器层是虚假安全感──文档记录的攻击面:字符级攻击(emoji 走私、同形字替换) 上下文重定向("忽略前面回答")、语义改写器产生可测量的分类精度下降──Llama Guard 4'in S14 Code Interpreter Abuse 类别特别针对阶段 15代码代理的

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, category-tagged classifier simulator) | **语言:** Python（标准库，分类标记分类器模拟器）
**Prerequisites:** Phase 15 · 10 (Permission modes), Phase 15 · 17 (Constitution) | **前置知识:** Phase 15 · 10（权限模式），Phase 15 · 17（宪法）
**Time:** ~45 minutes | **时间:** ~45 分钟

>  **【前置】**Önemli bir şekilde, bu süreçte, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir sürece bir sürece, bir sürece bir sürece bir sürece, bir sürece bir sürece bir sürece, bir sürececececece, bir sürececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececece
>  **【类比】**Llama Guard = "机场安检"。 her giriş istasyonu yolcu(输入) ve her çıkış istasyonu行李(输出) 都过一遍。优点:快速分类) 移动端可跑(INT4 30+ token/s) ・缺点:可被绕过Emoji kaçakçılığı %100 突破率,越狱 %72 başarısı oranı。
> ️ **【易错点】**Sadece Llama Guard 加其他防御 = 虚假安全感──攻击者使用emoji/同形字/语义改写就能绕过──修复:分类器 + 规则硬禁令 + 行为监控(Kill Switch) + HITL 多层防御──

## Sorunlar. Sorunlar.

> **【中文解读】**Llama Guard (Meta) içeriğin güvenlik sınıfına özel bir LLM'dir. İçeriye giriş ve çıkışın güvenlik stratejilerine aykırı olup olmadığını kontrol eder.

> **【拓展：llama guard】**Llama Guard, açık kaynaklı AI güvenlik araç zincirinin önemli bir parçasıdır.

LLM giriş ve çıkışları için sınıflandırıcılar ajan yığınının en dar noktasında yer almaktadır: her talep geçer, her cevap geçer.

> LLM 输入输出分类器位于 Agent 最狭的点:每个请求通过、每个响应通过──

İyi bir sınıflandırıcı katmanı hızlı, taksonomya tabanlı ve küçük bir hesaplama maliyeti için açıkça yanlış kullanımın büyük bir kısmını yakalar.

> İyi sınıflandırma düzeni hızlı, sınıflandırma kurallarına dayalı, küçük hesaplama maliyetinin büyük kısmını yakalamak için belirgin yanlış kullanımı vardır.

20242026 sınıflandırıcı yığın, küçük bir üretim hazır seçenekler kümesine üye oldu. Llama Guard (Meta) Meta'nın Topluluk Lisansı altında açık ağırlıklar gemileri. NeMo Guardrails (NVIDIA) izinli lisanslı raylar ve iletişim akışı kuralları için Colang gemileri. Her ikisi de bir temel modeli ile eşleştirmek için tasarlanmıştır, güvenlik davranışını değiştirmez.

> 2024-2026 分类器收到一小组成产就绪选项──Llama Guard(Meta) Meta Community License ile açıklama hakkı yayınlamak──NeMo Guardrails(NVIDIA) yayımlamak 宽松许可护加 Colang Dialog流规则──两者设计为基础模型的配对而非替代其安全行为──

> **【中文解读】**Bu bölümde AI Ajanının temel kavramı ve gerçekleştirme yöntemleri ele alınıyor. Ajan, çevreyi gözlemleyebilen, kararlar verebilen, eylemleri gerçekleştiren ve hedefleri gerçekleştirene kadar döngülenebilen LLM tarafından yönlendirilmiş bir otonom sistemdir.

Belgelemiş başarısızlık yüzeyi de aynı derecede iyi haritalanmıştır. Karakter düzeyde saldırılar (emoji kaçakçılığı, homoglif değiştirme), bağlamda yönlendirme ("öncekiyi görmezden gelme ve cevapla"), ve semantik parafrase hepsi sınıflandırıcı doğruluğunda ölçülebilir düşüşler üretmektedir. Huang et al. 2025'te belirli bir Emoji kaçakçılığı saldırısı gösterildi.

> 文档记录的失败面同样映射良好──字符级攻击(emoji 走私、同形字替换)、上下文重定向("忽略前面回答") 和语义改写都产生分类器精度的可测量下降──黄等 2025 特定的Emoji 走私 攻击在六个命名护系统上达到100% ASR──

## Konsepten bir şey.

### Llama Gardiyan 3 bir bakışta

- Üssü model: Llama-3.1-8B
  Çeviri: Llama-3.1-8B
- İçerik güvenliği için iyi ayarlanmış; genel bir sohbet modeli değil
  Çinçe Çevirimiçi:
- Giriş ve çıkışları sınıflandırır
  Çin Çeviri:分类输入和输出
- MLCommons 13- Tehlike taksonomisi
  Çeviri:MLCommons 13 危害分类法
- 8 dil
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri Çeviri: Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Ç Çeviri Çeviri Ç Çeviri
- 1B-INT4 kuantistik varianti mobil CPU'larda > 30 tok/s'de çalışır
  ÇINCE TRANSLATION: 1B-INT4 量化变体在移动 CPU 上 >30 tok/s 运行

Taksonomi üründür. "S1 Şiddetli Suçlar" "S13 Seçimler" yoluyla modelin eğitildiği ortak bir kelimeforuna hariteler. Aşağı akım sistemleri kategorilere özel eylemleri telsize edebilir: S1'i doğrudan engelleyin, insan gözden geçirme için S6 bayrağı, S12'yi not edin ancak izin verin.

> S1 S6 标志人类审查、标志 S12 标志 S12 标志 S12 标志 S12 标志 S12 标志 S12 标志 S12 标志 S12 标志 S1 标志 S1 标志 S1 标志 S1 标志 S1 标志 S1 标志 S1 标志 S1 标志 S1 标志 S1 标志 S1 标志 S1 标志 S1 标志 S1 标志 S1 标志 S1 标志 S12 标志 S12 标志 S12 标志 S12 标志 S12 标志 S12 标志 S12 标志 S12 标志 S12 标志 S12 标志 S12 标志 S12 标志 S12 标志 S12 标志 S12 标志 S12 标志 S12 标志 S12 标志 S12 标志 S12 标志 S12 标志 S12 标志 S12 标志 S12 标志 S12 标志 S12 标志 S12 标志 S12 标志 S12 标志 S12 标志 S12 标志 S12 标志 S12 标志 S12 标志 S12 标志 S12 标志 S12 标志 S12 标志 S12 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标 标     标 标 标   标                             标 标  

### Llama Gardi 4 ekleme Llama Gardi 4 ekleme

- Multimodal: görüntü + metin girişi
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri
- Genişletilmiş taksonomi: S1S14 (S14 Kod Anlatıcı İstifadesi ekliyor)
  Çeviri: S1-S14 (S14 Kodu Anlatıcı İstifadesi)
- Llama Guard 3 8B/11B'nin yer değiştirmesi
  Çeviri:Llama Gardiyan 3 8B/11B 的直接替换

S14 bu aşamada önemlidir. Otonom kodlama ajanları (Daa 9) kum kutularında kod uyguluyor (Daa 11); özel olarak kod yorumcularının kötüye kullanımı için sınıflandırıcı kategorisi daha önceki taksonomide adı verilmemiş bir saldırı sınıfını yakalar.

> S14 için bu aşama önemli. Özgür kodlama ajanı (第 9 课) 沙箱 (第 11 课) içinde kod uygulamak; özel olarak kod açıklayıcılarının kötüye kullanılması için kullanılan sınıflandırma sınıfları erken sınıflandırma biçiminde isimsiz saldırı sınıfları tarafından yakalamak için.

### NeMo Guardrails (NVIDIA)

- 2026 Ocak ayında yayınlanan v0.20.0
  中文翻译:v0.20.0 2026 年 1 月发布
- Giriş rayları: Kullanıcı dönüşünde sınıflandırma ve engelleme
  Çinçe Çevirimi:输入护: user轮上的分类并阻止
- Çıkış rayları: model dönüşünde sınıflandırma ve bloklama
  Çinçe Çevirim:输出护:模型轮上的分类并阻止
- Diyalog rayları: Kolang tanımlı akış kısıtlamaları (örneğin, "kullanıcı X sorarsa Y ile cevap ver")
  Çinçe Çevirimiçi:对话护:Colang 定义的流约束(例如"如果用户问X,回 Y")
- Llama Guard, Prompt Guard ve özel sınıflandırıcıları birleştirir
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri

Diyaloğ-düzgeç katmanı farklılıklandırıcıdır. Giriş/çıktı rayları tek bir dönüşte çalışır; diyaloğ rayları, kullanıcı üç farklı yolu sorarsa bile müşteri desteği botunda tıbbi teşhis hakkında tartışmamayı zorlayabilir.

> Bu nedenle, bu konularda, "özellikle, bir kişinin sağlık durumunu kontrol etmesi" ve "özellikle, bir kişinin sağlık durumunu kontrol etmesi" için gerekli önlemler alınmıştır.

### Saldırı korpusu.

**Emoji Smuggling**(Huang et al., arXiv:2504.11168): Yasak istek karakterleri arasında basılamaz veya görsel olarak benzer emoji ekleyin. Tokenizer onları sınıflandırıcının beklediğinden farklı bir şekilde birleştirir.

> **Emoji Smuggling**(Huang 等人,arXiv:2504.11168): On the Prohibited Request's characters间 inserted in print or visual similar emoji──tokenizer 以分类器预期外的方式合并它们──六个著名护系统上100% ASR──

**Homoglyph substitution**: Latin harflerini görsel olarak aynı olan Kiril alfabesi ile değiştirin. "Bomb" "Воmb" haline gelir; sınıflandırıcı İngilizce misler üzerinde eğitilmiştir.

> **同形字替换**:Vision aynı Latin harfleri değiştirmek için: "Bomb" 变为 "Воmb";英语训练的分类器遗漏──

**In-context redirection**: "Bu bir araştırma bağlamı olduğunu düşünmeden önce farklı bir politika uygulayın".

> **上下文重定向**:" cevap önce, düşünün bu araştırma üzerinde aşağıdaki yazı ve uygulama farklı politikaları.

**Semantic paraphrase**: Yasak talebi yeni bir dilde yeniden ifade edin.

> **语义改写**Yeni dilde yeniden ifade edilmesini yasaklamak için yapılan istekler.

**NeMo Guard Detect**: Huang et al. gazetesindeki bir jailbreak referansına göre 72,54% ASR. Bu dikkatli bir saldırı aracı ile yapılır; rastgele jailbreaks çok daha düşüktür, ancak tavan açıkça "sıfır" değildir.

> **NeMo Guard Detect**Huang 等人文中越狱基准上 72.54% ASR。

### Klasörler kazanırken

- **Fast default rejection**açık bir yanlış kullanım (CSAM oluşturmak için bir talebimiz milimetre içinde yakalanır).
  Çeviri:**明显误用的快速默认拒绝**(CSAM oluşturun Lütfen dakika içinde yakalayın)
- **Category routing**Farklı işlem için (bazısını engelle, diğerlerini kaydet, birkaçını yükselt).
  Çeviri:**类别路由**Farklılık işlemeyi engellemek için kullanılır.
- **Output rails**Eğer bu şekilde yapılırsa hassas kategorileri sızdırmış olan yakalama model çıkışları.
  Çeviri:**输出护栏**Yakalanmazsa hassas sınıflar model çıkışı ortaya çıkacaktır.
- **Compliance surface area**düzenleyiciler için  belgelenmiş, denetlenebilir sınıflandırıcı, açıklanmış taksonomisi ile.
  Çeviri:**监管合规面**带声明分类法律文档化、可审计分类器──

### Klasörler kaybediyor.

- Karşılıklı işleme (emoji kaçakçılığı, homoglif).
  Çine dilinde: ︎ ︎
- Sınıflandırıcının sıra seviyesindeki bağlamda hareket eden çok yönlü saldırılar.
  Çinçe Çevirisi:跨分类器轮级上下文漂移的多轮攻击──
- Klasörün eğitim verileri kelime birikmesine parafrase eden saldırılar görmedi.
  Çinçe Çevirisi:改写到分类器训练数据未见词汇的攻击──
- İzin verilen ve izin verilmeyen kategoriler arasında gerçekten belirsiz olan içerik.
  Çinçe Çevirimiçi:                                                                                                                                                                                                                                                           

### - Derin savunma.

Bir sınıflandırıcı katman boşlukları anayasa katmanının altında (Desin 17), çalıştırma katmanının üzerinde (Desin 10, 13, 14). Kompozisyon:

> 分类器层位于宪法层(第 17 课) 下、运行时层(第 10、13、14 课) 上──组合:

- **Weights**Bu, bir temel temel olarak, bir temel olarak, bir temel olarak, bir temel olarak, bir temel olarak, bir temel olarak, bir temel olarak, bir temel olarak, bir temel olarak, bir temel olarak, bir temel olarak, bir temel olarak, bir temel olarak, bir temel olarak, bir temel olarak, bir temel olarak, bir temel olarak, bir temel olarak, bir temel olarak, bir temel olarak, bir temel olarak, bir temel olarak, bir temel olarak, bir temel olarak, bir temel olarak, bir temel olarak, bir temel olarak, bir temel olarak, bir temel olarak, bir temel olarak, bir temel olarak, bir temel olarak, bir temel olarak, bir temel olarak, bir temel olarak, bir temel olarak, bir temel olarak, bir temel olarak, bir temel olarak, bir temel olarak, bir temel olarak, bir temel olarak, bir temel olarak, bir temel olarak, bir temel olarak, bir temel olarak, bir temel olarak, bir temel olarak, bir temel olarak, bir temel olarak, bir temel olarak, bir temel olarak, bir anlamıyla, bir anlamıyla, bir olarak, bir anlamıyla, bir anlamıyla, bir anlamıyla, bir olarak, bir anlamıyla, bir olarak, bir anlamıyla, bir anlamıyla, bir olarak, bir anlamıyla, bir olarak, bir anlamıyla, bir olarak, bir anlamıyla, bir olarak, bir anlamıyla, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak, bir olarak,
  Çeviri:**权重**:Divanyacılık Yapay zeka eğitimi modeli:默认拒绝公开误用:
- **Classifier**Llama Guard / NeMo Guardrails. Açık yanlış kullanım için hızlı reddedilme; kategori yönlendirme.
  Çeviri:**分类器**:Llama Guard / NeMo Guardrails。 açık yanlış kullanımı 快速拒绝;类别路由。
- **Runtime**: izin modları, bütçeler, öldürme anahtarları, kanaryalar.
  Çeviri:**运行时**: Hakkın Önerisi, Bütçe, Öneriler, Öneriler
- **Review**: HITL'e sonuçlı eylemler konusunda önerme-sonra karar verme.
  Çeviri:**审查**Bu yüzden, bu konuda bir şey yapmamalıyız.

Tek bir katman yeterli değil. Katmanlar farklı saldırı sınıflarını kapsar.

> 没有单一层是足够的―― her katılımcı farklı saldırı sınıflarını kapsar.

## Çerçeveyi kullanın.
```figure
a5-guard-sieve
```

## Kullan

`code/main.py`Bu metin, aynı metinle çiğ, emoji kaçakçılığı ve homoglif değiştirilmesi ile geçer; sınıflandırıcının hit oranı Huang et al. kağıt belgeleri şekillerinde düşer. Sürücü ayrıca çıkış raylarının giriş kabul edildiğinde bile bir çıkışı nasıl reddedeceğini gösterir.

> `code/main.py`模拟带 6 类分类法玩具 分类器对输入轮文本──相同文本通过原始、emoji 走私和同形字替换;分类器命中率 Huang 等人文记录的方式下降──驱动器还展示出口护输入被接受时仍拒绝出口──

## İndirin . Ürünler .

`outputs/skill-classifier-stack-audit.md`Bir dağıtımın sınıflandırıcı katmanını (model, taksonomi, giriş/çıktı rayları, iletişim rayları) denetlemektedir ve boşlukları işaretler.

> `outputs/skill-classifier-stack-audit.md`审计部署的分类器层(模型、分类法、输入/输出护、对话护)并标记缺口──

## Egzersizler.

1. Çık .`code/main.py`Sınıflandırıcının çiğ zararlı girişleri yakaladığını doğrulayın ama emoji kaçak versiyonunu kaçırır.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`code/main.py`▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ 

2. MLCommons 13-tehlik taksonomisi ve Llama Guard 4 S1S14 listesini okuyun. S1S14'teki orijinal 13-tehlik seti içinde doğrudan haritalama olmayan kategorileri tanımlayın; S14 Kod Anlatıcı İstifadesi'nin S1S14 aşamasında neden özel olarak ilgili olduğunu açıklayın.
   中文翻译:阅读 MLCommons 13 危害分类法和 Llama Guard 4 S1-S14 列表。识别 S1-S14 中原始 13 危害集无直接映射的类别;解释为什么 S14 Code Interpreter Abuse对阶段 15 特别相关。

3. NeMo Guardrails iletişim rayını, asla teşhis tartışmasına izin vermeyen bir müşteri desteği botu için tasarlayın.
   Çinçe Çevirimi: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çzzüm: Çzzzüm:

4. Huang et al. (arXiv:2504.11168). Bir saldırı kategorisini seçin (emoji kaçakçılığı, homoglif, parafrase) ve bir azaltma önerisini yapın.
   Çinli dilde: 阅读 Huang 等人(arXiv:2504.11168)。选一个攻击类别(emoji 走私、同形字、改写)并提出缓解──命名缓解自己的失败模式──

5. NeMo Guard Detect'in 72,54% ASR'i, jailbreak referans değerlerinde adversarial craft altında ölçülür.
   Çinçe çevirisi:NeMo Guard Detect, 72,54% ASR'i, bir süre içinde yapılan ölçümlere karşı tasarlanmıştır.

## Anahtar Şartlar .

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| Llama Guard | "Meta's safety classifier" | Llama-3.1-8B fine-tuned for input/output classification |
| Llama Guard | "Meta 的安全分类器" | 为输入/输出分类微调的 Llama-3.1-8B |
| MLCommons taxonomy | "13-hazard list" | Shared vocabulary for content-safety categories |
| MLCommons 分类法 | "13 危害列表" | 内容安全类别的共享词汇 |
| S1–S14 | "Llama Guard 4 categories" | Expanded taxonomy; S14 is Code Interpreter Abuse |
| S1-S14 | "Llama Guard 4 类别" | 扩展分类法；S14 是 Code Interpreter Abuse |
| NeMo Guardrails | "NVIDIA's rails" | Input + output + dialog rails; Colang for flows |
| NeMo Guardrails | "NVIDIA 的护栏" | 输入 + 输出 + 对话护栏；Colang 用于流 |
| Emoji Smuggling | "Tokenizer trick" | Non-printable emoji between chars; 100% ASR on six guards |
| Emoji Smuggling | "tokenizer 技巧" | 字符间不可打印 emoji；六个护栏上 100% ASR |
| Homoglyph | "Lookalike letters" | Cyrillic for Latin; classifier trained on English misses |
| 同形字 | "相似字母" | 西里尔代拉丁；英语训练的分类器遗漏 |
| ASR | "Attack success rate" | Fraction of attacks that bypass the classifier |
| ASR | "攻击成功率" | 绕过分类器的攻击比例 |
| Dialog rail | "Flow constraint" | Conversation-level rule that persists across turns |
| 对话护栏 | "流约束" | 跨轮持续的对话级规则 |

## Daha fazla okumak

- [Inan et al. — Llama Guard: LLM-based Input-Output Safeguard](https://ai.meta.com/research/publications/llama-guard-llm-based-input-output-safeguard-for-human-ai-conversations/)- Orijinal kağıt.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri
- [Meta — Llama Guard 4 model card](https://www.llama.com/docs/model-cards-and-prompt-formats/llama-guard-4/) multimodal, S1S14 taksonomisi.
  Çinçe Çevirim:多模态、S1-S14 分类法。
- [NVIDIA NeMo Guardrails (GitHub)](https://github.com/NVIDIA-NeMo/Guardrails) v0.20.0 Ocak 2026.
  中文翻译:v0.20.0 2026 年 1 月。
- [Huang et al. — Bypassing Prompt Injection and Jailbreak Detection in LLM Guardrails](https://arxiv.org/abs/2504.11168) Koruma sistemlerinde ASR numaraları.
  Çinçe Çevirimiçi:跨护系统的 ASR 数字──
- [Anthropic — Measuring agent autonomy in practice](https://www.anthropic.com/research/measuring-agent-autonomy) sınıflandırıcı-daha çalışma zamanı çerçevesini oluşturmak.
  Çinçe Çevirisi:分类器加运行时框架
