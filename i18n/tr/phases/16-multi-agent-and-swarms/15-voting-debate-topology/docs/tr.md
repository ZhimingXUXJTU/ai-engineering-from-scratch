# Oylama, Kendi Katkı ve Tartışma Topolojisi

> En ucuz birleştirme: örnek N bağımsız ajanlar, çoğunluk oyları. Wang et al. 2022 kendi kendine tutarlılık bunu bir model örnek N kez yaptı. Multi-agent onu genişletiyor **heterogeneous**Monoculture'den kaçmak için farklı modeller, farklı uyarılar, farklı sıcaklıklar, farklı bağlamlar. Çoğunluk oyundan öte, topoloji meseleleri tartışılır: MultiAgentBench (arXiv:2503.01935, ACL 2025) yıldız / zincir / ağaç / grafik koordinasyonu değerlendirdi ve buldu **graph best for research**AgentVerse (ICLR 2024) iki yenilikçi örneği belgelendirir  gönüllü davranışlar ve uyum davranışları  ve uyum hem bir özellik (tümleşme bulmak) hem de bir risk (grup düşüncesi, Ders 24). Bu ders topoloji alanını haritalar, her variansı inşa eder ve koordinasyon vergisini ölçer.

> **【中文解读】**Bu bölüm oylama ve tartışmanın çok sayıda ajanın oylama veya tartışmanın yoluyla karar vermesi için yapılan örgütsel yapısını tanıttı.

> **【拓展：voting debate topology→具体应用】**投票和辩論拓 形形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形 形     形     形                   形                                                                                                                            


**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib) | **语言:** Python（标准库）
**Prerequisites:** Phase 16 · 07 (Society of Mind and Debate), Phase 16 · 14 (Consensus and BFT) | **前置知识:** Phase 16 · 07（心智社会与辩论），Phase 16 · 14（共识与 BFT）

>  **【前置】**Öğrenci bölümünün ilk aşaması: 16·07 (debat)  16·14 (BFT 共识)  13·03 (Self-Consistency CoT)  Voti拓 = 多 Agent 决策的几何形状──
>  **【类比】**投票拓 = "konference table摆放方式"──星形 = 圆桌投票(独立);链形 = 接力修改(前面 代理的输出传给下一个);图形 = 圆桌讨论(多轮交互)──MultiAgentBench 结论:图形适合研究任务但有"协调税"──>4 个 代理 性价比下降)──异质性是关键不同模型/温度/快速 防单一文化错误──
**Time:** ~75 minutes | **时间:** ~75 分钟

## Sorunlar sorunun giriş

Tartışma doğruluğunu artırabilir (Du et al., arXiv:2305.14325).

> 辩论可以提高准确性 (Dü 等人,arXiv:2305.14325),也可能降低准确性 (Dü)

1. Kim kime konuşuyor (topoloji).
   Çevre dilinde:谁和谁对话 (谁和谁对话)
2. Kaç tur (Du 2023: hem turlar hem de ajanlar bağımsız olarak önemlidir).
   Çine Çevirimi: How many times (How many times)
3. Ajanların heterogen olup olmadığını (farklı temel modeller mono kültürü kırar).
   Çinçe Çevirimi:Agent 是否异构(不同基础模型打破单一文化)
4. Bir düşman sesinin var olup olmadığını (Çeliç-maning vs. Çöp-maning).
   Çinçe Çevirisi: Çinçe Çevirisi: Çinçe Çevirisi: Çinçe Çevirisi: Çinçe Çevirisi: Çinçe Çevirisi: Çinçe Çevirisi: Çinçe Çevirisi: Çinçe Çevirisi: Çinçe Çevirisi: Çinçe Çevirisi: Çinçe Çevirisi: Çinçe Çevirisi: Çinçe Çevirisi: Çinçe Çevirisi: Çinçe Çevirisi: Çinçe Çevirisi: Çinçe Çevirisi: Çinçe Çevirisi: Çinçe Çevirisi: Çinçe Çevirisi: Çinçe Çevirisi: Çinçe Çevirisi: Çinçe Çevirisi: Çinçe Çevirisi: Çinçe Çevirisi: Çinçe Çevirisi: Çinçeçeçe Çevirisi: Çinçeçeçe Çevirisi: Çinçeçeçeçe Çevirisi: Çinçeçeçeçeçe Çevirisi: Çinçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçeçe

Bir göreve "beş ajanı çalıştırıp oy veren" takımlar genellikle tek bir ajanla karşılaştırılır. Başarısızlıklar rastgele değildir. Topoloji ve heterogenliği izlerler. Bu ders topoloji haritasıdır.

> チーム" 5 Ajanı çalıştırır ve oy verir" görevlerine sert katılır, genellikle tek Ajanın performansından daha kötü olur. Başarısızlık tesadüfen değildir.

## Konsept merkezi konsept

### Kendi kendine uyumlulık, tek model temel çizgi

Wang et al. 2022 ("Öz tutarlılığı Düşünce Dönüşüm zincirini geliştirir") aynı model N defaları sıcaklık > 0 ve akıl yolu cevaplarında çoğunlukla oy kullanan örnekler aldı. GSM8K'da sonuç: tek açgözlülükle çözülen bir örnekle N=40'lık önemli kazançlar.Öz tutarlılık, birden fazla ajan oy kullanmasının öncüdür.

> Wang 等人 2022 yıl ((("Öz uyumluluk geliştirme düşünce zinciri düşünce") sıcaklık > 0 koşullarında aynı modelden alınan örneklere N kez, ve önerme yolunun cevaplarına çoğunlukla oy verilmiştir.

Sınır: kendi kendine tutarlılık bir temel model kullanır. Hatalar yapı ile ilişkilendirilir. Eğer model sistematik bir önyargıya sahipse, tüm N örnekleri bunu paylaşıyor.

>  sınırlama: öz uyumluluk bir temel model kullanır. Yapımdaki hatalar ilişkidir. Eğer model sistematik bir önyargıya sahipse, tüm N örnekleri paylaşıyor.

### Çoklu temsilci oylaması, heterogen genişleme

N örneklerini N * farklı* ajanlarla değiştirin. Farklı temel modeller (Claude, GPT, Llama), farklı istekler, farklı araç erişimleri. Fayda: ilişkisiz hatalar. Maliyet: farklı ajanlar farklı miktarlarda maliyetler öder; koordinasyonları genel maliyetler ekler.

> N 个样本的替代为 N 个*不同*的代理――不同的基础模型(Claude、GPT、Llama),不同的提示,不同的工具访问──好处:不相关的错误──代价:不同代理的成本不同;协调它们增加开销──

Heterogene tartışma için 2026 tarihli isim **A-HMAD** Düşmanlı Heterogene Multi-Agent Tartışma. Evrensel olarak kabul edilmedi, ancak makaleler "mono kültür çöküşünden kaynaklanan ilişkili hataları azaltan farklı modeller tartışmaları" için terimi kullanıyor.

> 2026 yılının farklı yapı tartışması için düzenleme adı:**A-HMAD**对抗性异构多 辩论──并非普遍采用,但论文使用这个词指"不同模型辩论,减少单一文化崩的相关错误"──

### Dört topoloji

```
star                chain               tree                graph

    ┌─A─┐           A─B─C─D         ┌──A──┐              A───B
    │   │                           │     │              │ × │
    B   C                           B     C              D───C
    │   │                          / \   / \
    D   E                         D   E F   G           (fully connected)
```

Yıldız: bir merkezi, diğerleri sadece merkeze konuşuyor.
Zincir: doğrusal, her ajan önceki birinin çıkışını görür.
Ağaç: hiyerarşik, hiyerarşik ajan sistemleri tarafından kullanılır (Deneyim 06).
Grafik: herhangi biri-herhangi biri. Tamamen bağlantılı kliş ve keyfi DAG'lar içerir.

> 星形: 一中心,所有其他 Agent 只与中心对话──等于没有反通道的监督者-工作者──
> 链形:线性, her Ajan 看到前一个 Ajan的输出──类似流水线──
> 树形:层次化,用于层次化 Agent 系统 (第 06 课)
> 图形:任意到任意──包括完全连接的团和任意 DAG──

### Koordinasyon vergisi (MultiAgentBench)

MultiAgentBench (MARBLE, ACL 2025, arXiv:2503.01935) araştırma, kodlama ve planlama dahil bir görev kümesinde yıldız, zincir, ağaç, grafikle benchmarked. Anahtar ölçüm sonuçları:

> MultiAgentBench ((MARBLE,ACL 2025,arXiv:2503.01935) araştırma, kodlama ve planlama dahil görev kitlerinde yıldız şekli, zincir şekli, ağaç şekli, tablo için基准测试──关键测量结果:

- **Graph**Topoloji araştırma görevlerinde kazanır. Bilgi her yere akıyor; ajanlar birbirlerini eleştirebilir.
  Çeviri:**图形**Araştırma görevlerinde kazanç elde etmek; bilgi her türlü şekilde akışır; ajanlar birbirlerini eleştirir.
- **Star**HAB filtreliyor ve konsolidasyon yapılıyor.
  Çeviri:**星形**Hızlı cevaplı gerçek görevler üzerinde kazançlılık.
- **Chain**adım adım boru hattlarında kazançlar (adrenal rafine).
  Çeviri:**链形**Bu da bir başarıdır.
- **Coordination tax**Grafik topolojisinde 4 ajanın ötesinde görünmektedir.
  Çeviri:**协调税**Çizgilik yapısında yaklaşık 4 ajan ortaya çıktı.

4 ajan tavanı temel değil, empiriyeldir. 2026 LLM bağlam kapasitesini yansıtır: her ajanın bağlamı eşdeğerlerin çıkışlarıyla dolur ve herkes herkesi görebildikten sonra eklemci N + 1'nin sınır değerinin düşmesi.

> 4 Ajanın Yukarı Sınırı, temel değil deneysel bir şeydir. Bu, 2026 LLM'nin üst üstelik kapsamını yansıtır: Her Ajanın üst üstelik kapsamı eşinin çıkışını doldurdu, bir kez herkes herkesi görebildiğinde, Ajanın kenar değerinin artımı N+1'e düşüyor.

### Çoklu ajan tartışması stratejileri ("Çılgınlık yapmalı mıyız?")

ArXiv:2311.17371 MAD stratejilerinin 2023 son araştırmasıdır. Diğerleri tarafından tekrarlanan ana bulgu: * yapısal olarak benzer* olan MAD varianları (bağımsız örnekleme + toplama) genellikle aynı bütçeyi kullanırken kendi tutarlılığını daha düşük performans gösterir. MAD, ajanlar gerçekten heterogen olduğunda ve tartışmaların karşıtlık yapısı olduğunda (bir ajan karşı çıkıyor).

> arXiv:2311.17371 is 2023 MAD 策略综述──关键发现已被他人复现: 结构上与自一致相似的 MAD 变体(独立采样 + 聚合) 结构上与自一致相似的 MAD 变体──通常不如自一致的MAD 在使用相同预算时往往不如自一致的MAD 在 Agent 真正异构和辩论对抗结构时最大的帮助──

### AgentVerse ortaya çıkan kalıplar

AgentVerse (ICLR 2024, https://proceedings.iclr.cc/paper_files/paper/2024/file/578e65cdee35d00c708d4c64bce32971-Paper-Conference.pdf) açık bir tasarım olmadan bile çoklu ajan tartışmasından ortaya çıkan iki davranışın belgelenmesini sağlar:

- **Volunteer.**Bir ajan, yardım teklif eder ("Bir sonraki adımı atabilirim") isteksiz.
  Çeviri:**自愿者。**Ajan 主动提供帮助 (("köste bir adım atabilirim") ◦有用: İşleri en yetkin görevleri olan Ajan'a dağıtacak.
- **Conformity.**Bir ajan, eleştirmen yanlış olduğunda bile, bir eleştirmenle uyumlu bir tutum geliştirir.
  Çeviri:**从众。**Agent 调整立场以匹配批评者,即使批评者是错的────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

Uygunluk, anlaşmaya kadar tartışmaların zorbaları ödüllendirdiği neden.

> "Debateye Rağmen" Neden?

### Heterogenite: doğruluk hareket eden gerçek düğme

Uygulama literatüründeki 2024-2026 model: N ajanlarından birini farklı bir temel model için değiştirmek, N'yi 1 ile artırmaktan daha büyük bir doğruluk artışı verir.

> 2024-2026 yılları için pratik literatürün bir modeli: N 个代理 中的一个换成不同基础模型而不是增加N + 1 个代理 带来更大的准确率提升──直觉是单一文化 每个新的独立错误源比额外相关样本更有价值──

Üç farklı model, temiz bir temel gerçeği olan çoğu görevde bir modelin beş kopyasını yener.

> En az bir durumda, farklı yapıların sayılarını kazanır. Çoğu açık standart cevap görevinde, üç farklı model aynı modelin beş kopyasını kazanır.

### Jüri yöntemleri

Sibyl çerçevesinde (Minsky-LLM literatüründe alıntılanan) bir " jüri " resmileştirir. Bu, her aşamada oy kullanarak cevapları düzelten küçük bir dizi uzman ajanın oluşturduğu bir gruptur.

> Sibyl framework (Minski-LLM metinde alıntı) formelleştirmiş "jury"一小组专业化 Agent 通过每阶段投票来改进答案──与简单多数投票不同,陪审团的角色:一个 Agent 交叉质询,一个提供上下文,一个评分合理性──陪审团的方法介于简单投票(便宜,易单一文化) 和完整的MAD(昂贵,易从众) 之间──

### Oylama ve tartışma baskısı olduğunda

- Bu sorunun temel gerçeği vardır (gerçek, matematik, kod davranış).
  Çinçe çevirisi: soru has standard answer ((facts、math、code behavior) ⋅ voting ⋅ is meaningful ⋅
- Ajanlar farklı kaynaklara veya araçlara erişebilir (heterogenlik mevcuttur).
  Çinçe Çevirimi:Agent farklı kaynaklara veya araçlara ulaşabilir.
- Rondlar sınırlıdır (2-3 tipik) ve ayrı bir yargıç veya doğrulayıcı vardır.
  Çinçe çevirisi:轮次有界 (genellikle 2-3 轮),有独立的评委或验证器──
- Bütçe 3-5 ajanı sağlar. 5-7'in dışında grafik topolojisi, koordinasyon vergisi hakimdir.
  Çinçe Çevirisi: Bütçe 3-5 Ajanı İzin Verir.

### Eğer tartışmalar ile oy kullanmak acı verirse

- Sorular, fikir şeklinde, ajanlar en güvenilir, en doğru olmayan yanıtlara birleşiyor.
  Çinçe Çevirisi: sorular, fikir biçimindedir.
- Bütün ajanlar bir temel model paylaşır.
  Çinçe çevirisi:所有 共同共享基础模型──单一文化使共识无意义──
- Rondlar sınırsızdır.
  Çin Çeviri: 轮次无界──从众每次都赢──
- Görev basit. N=5'te kendi kendine tutarlı bir ajan daha ucuz ve aynı derecede doğru.
  Çinçe Çevirimi: görev basit. Tek Ajan, N=5'de kendi kendine uyumlu daha uygun ve aynı şekilde doğru.

## Yapın.
```figure
sw-debate-topology
```

## Yapın

`code/main.py`Uygulamaları:

- `run_star(agents, hub, question)` Her çalışanın merkezi anketleri, toplamlar.
  Çeviri:`run_star` Central rotquery her işçi birleşmiş.
- `run_chain(agents, question)` sıradan gelişme.
  Çeviri:`run_chain` 顺序改进──
- `run_tree(root, children, question)` derinlik-2 toplama ile hiyerarşik.
  Çeviri:`run_tree` 层次化,深度 2 聚合──
- `run_graph(agents, question, rounds)`- Tümüne açık tartışma, sınırlı döngüler.
  Çeviri:`run_graph` 全对全辩,有界轮次──
- Bir senaryolu heterogenlik diyalog: her ajanın bir `error_bias`sistematik yanlışlığını göstermektedir.
  Çeviri: Her ajanın bir tane var.`error_bias`Sistemik hatalarını göstermek.
- Her topolojinin N=3, 5, 7'de çalıştırılan ve raporlar (düzgünlik, total_tokens, wallclock_simulated) yapan bir ölçüm harnesini.
  Çinçe Çevirimi: ölçüm araçları N=3, 5, 7 时运行每个拓并报告(准确率,总代币,模拟挂钟时间)

Çık:

```
python3 code/main.py
```

Beklenen çıkış: topoloji bir tablo × N → (doğrulık, tokenler, gecikme). Araştırma tarzı görevlerde grafik N=3-5'te kazanır; hızlı gerçeklik görevlerinde yıldız kazanır; N=7'deki grafik koordinasyon vergisini gösterir (gecikme doğruluğundan daha hızlı şişer).

> 预期输出:拓 × N →(准确率,token,延迟)表格。图形在 N=3-5 的研究风格任务上获胜;星形在快速事实性任务上获胜;图形在 N=7 时显示协调税(延迟膨胀快于准确率) 』

## Kullanın Kullanın

`outputs/skill-topology-picker.md`Bir görev açıklamasını okuyan ve topoloji (yıldız / zincir / ağaç / grafik), bir N (ajan sayısı), bir heterogenite profili (kullanılacak temel modeller) ve yuvarlak bir çizgi öneren bir beceri.

> `outputs/skill-topology-picker.md`Bu, bir beceri, read取任务描述并推拓(星形/链形/树形/图形) 、N(Agent 数量) 、异构配置(使用的基础模型) 和轮次上限──

## Gönderin.

Herhangi bir grup için:

- Başlayın .**self-consistency at N=5**Bu ucuz bir temel model.
  Çin Çeviri: From a strong basic model of**N=5 自一致性**Bu ucuz bir yol.
-  yükselt**heterogeneous voting at N=3**Eğer doğruluk önemlise, delta'yı ölç.
  Çinçe Çevirimi: Eğer doğru oran önemli ise, yükseltme **N=3 异构投票**                                                                                                                                                                                                                                                              
- Sadece **debate topology**Eğer görev yapılandırılmışsa ( Araştırma, çok adımlı) ve sınırlı döngüler mümkünse.
  Çinçe çevirisi: Sadece görevlerin yapısı vardır (şehir üzerinde çalışmak, daha fazla adım atmak) ve sıra sıraları vardır.**辩论拓扑**- Evet.
- Küçük bir azınlık sürekli haklı olduğunda, bir çeşitlilik sinyali var.
  Çinçe Çevirisi:始终记录少数派──当少数派持续正确时,你就有多样性信号──
- "10 kat daha iyi bir fiyatla daha iyi bir doğruluk" bir iş kararıdır.
  Çin dilinde:基准测试挂钟时间和代币以及准确率──"10倍成本的更好的准确率" (Böyük doğrulama oranı) ticari kararlardır──

## Egzersizler.

1. Çık .`code/main.py`Graf topolojisi için koordinasyon-davranış eğriyi çiz: doğruluk vs N, simgeler vs N.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`code/main.py`◊ çizim şekli                                                                                                                                                                                                                                                            
2. A-HMAD uygulaması: kasıtlı olarak farklı önyargılar olan üç ajan.
   Çinçe Çevirimi: A-HMAD: üç amaçlı farklı farklılıklara sahip Agent──全同偏差基线 A-HMAD ile 14. sınıfın tek kültür saldırısı üzerinde nasıl karşılaştırılır?
3. Grafik topolojisine oy kullanmayan, sadece son konsensüs oranını belirleyen bir "hakim" rolü ekleyin.
   Çinçe Çevirimiçi: Çizgi Toplamalarda bir "komisyon" rolü eklemek, sadece oy kullanmak değil, son bir fikir birliği belirlemek.
4. AgentVerse makalesini okuyun (ICLR 2024). Uygulamalarınızın en güçlü şekilde hangi yeni davranışları gösterdiğini belirleyin.
   ÇINCE TRIBULATION: READ AgentVerse 论文(ICLR 2024) ―― Identify your realization most strongly show现现的行为──你能通过提示变更激发相反的行为吗?
5. MultiAgentBench (arXiv:2503.01935) Bölüm 4 (topoloji deneyleri).
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri Çeviri Çeviri: Çeviri Çeviri: Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Ç Çeviri Çeviri Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç

## Anahtar Terimler

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Self-consistency / 自一致性 | "Sample N times, vote" / "采样 N 次，投票" | Wang 2022. Single model, N temperature>0 samples, majority vote on reasoning paths. / Wang 2022。单模型，N 次 temperature>0 采样，推理路径多数投票。 |
| Heterogeneity / 异构性 | "Different models" / "不同模型" | Ensemble of different base models or prompt families. Breaks monoculture. / 不同基础模型或提示族的集成。打破单一文化。 |
| MAD / 多 Agent 辩论 | "Multi-agent debate" / "多 Agent 辩论" | Generic term for agents exchanging critiques over rounds. See Du 2023. / Agent 跨轮次交换批评的通用术语。见 Du 2023。 |
| A-HMAD / 对抗性异构 MAD | "Adversarial Heterogeneous MAD" / "对抗性异构 MAD" | MAD variant emphasizing different models + adversarial structure. / 强调不同模型 + 对抗结构的 MAD 变体。 |
| Topology / 拓扑 | "Who talks to whom" / "谁和谁对话" | Star, chain, tree, graph. Determines information flow. / 星形、链形、树形、图形。决定信息流。 |
| Coordination tax / 协调税 | "Diminishing returns" / "边际收益递减" | Above ~4 agents on graph, cost grows faster than quality. / 图形拓扑约 4 个 Agent 后，成本增长快于质量。 |
| Volunteer behavior / 自愿者行为 | "Unprompted help" / "主动帮助" | AgentVerse emergent pattern: an agent offers to take a step. / AgentVerse 涌现模式：Agent 主动提出执行步骤。 |
| Conformity behavior / 从众行为 | "Agreement under pressure" / "压力下的同意" | AgentVerse emergent pattern: an agent aligns with a critic. / AgentVerse 涌现模式：Agent 与批评者对齐。 |
| Jury / 陪审团 | "Small specialized panel" / "小型专业小组" | Sibyl-style ensemble with roles (examiner, context, scorer). / Sibyl 风格的带角色集成（质询者、上下文、评分者）。 |

## Daha fazla okumak

- [Wang et al. — Self-Consistency Improves Chain of Thought Reasoning](https://arxiv.org/abs/2203.11171) Tek model için başlangıç
- [Du et al. — Improving Factuality and Reasoning via Multiagent Debate](https://arxiv.org/abs/2305.14325) Her iki ajan da ve atış da bağımsız olarak önemlidir.
- [MultiAgentBench / MARBLE](https://arxiv.org/abs/2503.01935) Topoloji referans gösterme grafik araştırma için en iyi, boru hattları için zincir
- [Should we be going MAD?](https://arxiv.org/abs/2311.17371) MAD stratejisi araştırması; MAD'nin genellikle eşit bütçeye sahipken kendi kendine uyumsuzluktan dolayı kaybediyor olduğunu buldu
- [AgentVerse (ICLR 2024)](https://proceedings.iclr.cc/paper_files/paper/2024/file/578e65cdee35d00c708d4c64bce32971-Paper-Conference.pdf) Gönüllülik ve uyumlulık belirgin modelleri
- [MARBLE repo](https://github.com/ulab-uiuc/MARBLE) Referans referans değerinin uygulanması
