# Değerlendirme ve Koordinasyon Benchmarks .

> Beş 2025-2026 referans noktası, çoklu ajan değerlendirme alanını kapsar. **MultiAgentBench / MARBLE**(ACL 2025, arXiv:2503.01935) yıldız/ zincir/ ağaç/graf topolojilerini, önemli nokta KPI'leri ile değerlendirir. **graph is best for research**, bilişsel planlama %3'lik bir dönüm noktası elde eder. **COMMA**GPT-4o'nun rastgele bir başlangıç çizgisini yenmek için mücadeleyi içeren en son modeller;**MedAgentBoard**(arXiv:2505.12371) dört tıbbi görev kategorisini kapsar ve genellikle çoklu ajanın tek LLM'de baskın olmadığını bulur. **AgentArch**(arXiv:2509.10769) araç kullanımı + bellek + orkestrasyonu birleştiren kurumsal ajan mimarlıklarını referanslandırır. **SWE-bench Pro**([arXiv:2509.16941](https://arxiv.org/abs/2509.16941)) iş uygulamaları, B2B hizmetleri ve geliştiriciler aracılığıyla 41 repo'da 1865 sorun yaşanıyor; sınır modelleri Pro'da %23 oranında %70'e karşı verified'de %70'e karşı  kirliliğin gerçeklik kontrolü. Claude Opus 4.7 (Epril 2026)**64.3%**Pro'da açık bir ajan-eşikler koordinasyonu ile (Antropik ilk kaynak henüz yayınlanmamış  ön raporu olarak ele alınmıştır); Verdent (ajan asfalt) vurgular **76.1% pass@1**Verified ([Verdent technical report](https://www.verdent.ai/blog/swe-bench-verified-technical-report) ).**AAAI 2026 Bridge Program WMAC**(https://multiagents.org/2026/Bu ders MARBLE'nin ölçümlerine dayanıyor, topoloji karşı ölçüm tarama yapılıyor ve "SWE-benç Verified'in sadece geçmesi genelleşmenin kanıtı değildir" kuralını sıkıştırıyor.

> **【中文解读】**Bu bölüm koordinasyon temel değerlendirmeyi  çoklu ajanları ölçmek  sistem koordinasyon yeteneğini değerlendirme yöntemlerini tanıttı.

> **【拓展：evaluation coordination benchmarks→具体应用】**Çoğu Ajan  koordinate evaluate基准:(1) AgentBench 多 Ajan  görev tamamlanması değerlendirmesi;(2) CLEVALLM Ajan 评估框架;(3) SWE-bench 多 Ajan 协作修复 bug。关键评估维度: görev tamamlanması oranı、协调效率(步数/成本)、鲁棒性(Agent故障时的表现) 和可扩展性(Agent 数量增加时的性能变化)。


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib) | **语言:** Python（标准库）
**Prerequisites:** Phase 16 · 15 (Voting and Debate Topology), Phase 16 · 23 (Failure Modes) | **前置知识:** Phase 16 · 15（投票与辩论拓扑），Phase 16 · 23（失败模式）

>  **【前置】**Öğrenci bölümün önüne geçmek için öncelikle öğrenin: 16·15(voting拓)  16·23(失败模式) SWE-bench 概念──5 个 2026 主流多 基准横向对比──
>  **【类比】**Çoğu Agent 基准 = "AI 团队的标准化考试"──MARBLE 测拓(图最佳做研究);COMMA 测多模态不对称信息协调(GPT-4o 都难超随机基线);MedAgentBoard 测医疗(多 Agent 常不胜单 LLM);SWE-bench Pro 测真码(1865 题/41 仓库,前沿模型仅23%,对比 Verified 70%+,揭露污染问题) ─Claude Opus 4.7 多 Agent 协调达 64.3%──
**Time:** ~75 minutes | **时间:** ~75 分钟

## Sorunlar sorunun giriş

Bir makalede "çok ajanlı sistemimiz daha iyidir" denildiğinde, soru şu: ne, ne üzerinde, nasıl ölçüldü? 2023-2024 yılları arasında çok ajanlı değerlendirme çağında kaos vardı.

> "Bizim çoklu ajanımız  sistemimiz daha iyi" dendiğinde, soru şuydu: Neye göre daha iyi, neye göre daha iyi, neyi ölçmek için? 2023-2024 yıllarındaki çoklu ajan değerlendirmesi  kaoslu bir değerlendirme Herkes kendi göstergelerini, temel lini ve görev kümelerini seçti.

Paylaşılan referanslar olmadan iki çoklu ajan sistemini anlamlı bir şekilde karşılaştıramazsınız. Daha da kötüsü, beklenmedik referanslar olmadan, sınır modelleri kirleştirebilir. SWE-benç Verified 2025 ortalarına kadar eğitim korpuslarında kısmen kirlendi; sınır puanları şişmişti; Pro kirlenmemiş bir gerçeklik kontrolü olarak tasarlandı.

> 没有共享基准,你不能有意地比较两个多代理系统――更糟的是,没有保留基准,前沿模型可能会受到污染――SWE-bench Verified in mid-2025 期部分污染了训练语料;前沿分数膨胀;Pro 设计为无污染的现实检验――

Bu ders, 2026'daki beş kanonik referans değerini sıralar, her birinin ölçümlerini belirler ve referans iddialarını şüpheci bir şekilde okumayı öğretir.

> Bu ders, 5 kuralları listede 2026 yılının temel testi, her bir ölçüm nedir, ve size şüphe tutumunu öğretir temel açıklama okuyun.

## Konsept merkezi konsept

### MultiAgentBench (MARBLE)  ACL 2025

arXiv:2503.01935. Araştırma, kodlama ve planlama görevleri üzerinde dört koordinasyon topolojisini (yıldız, zincir, ağaç, grafik) değerlendirir.

Ölçüm sonuçları:

- **Graph**Topoloji araştırma senaryoları için en iyi; herhangi bir eleştirileri destekler.
- **Chain**Adımlı rafine kodlama için en iyi.
- **Star**Hızlı bir gerçekleşme için en iyi.
- **Coordination tax**Graf üzerinde ~4 ajanın geçtiği görünür.
- **Cognitive planning**Topolojiler arasında %3'lik bir kilometrelik başarıyı ekler.

Kolportasyon topolojilerini elma-elme karşılaştırmak istediğinizde kullanın.https://github.com/ulab-uiuc/MARBLE) değerlendirici tarafından sağlanır.

### COMMA  Multimodal asimetrik bilgi

Görevler, ajanların farklı gözlem yöntemleri olan ve tam bilgi paylaşımı olmadan koordinasyon yapmaları gereken görevleri kapsar.**random baseline**COMMA'da ajan-ajen işbirliği konusunda.Signal, çoklu ajan modalitelerinin yetersiz eğitilmiş ve değerlendirilmemiş olduğu  LLM'ler tek modalitelerle işbirliği makul bir şekilde yönetmektedir.

Sisteminizin multimodal veya asimetrik bilgi koordinasyonu olduğunda kullanın. COMMA'dan gelen sıfır sonuç, talep etmeden önce ölçmek için bir uyarıdır.

### MedAgentBoard  alan stres testi

ArXiv:2505.12371. Dört tıbbi görev kategorisi: teşhis, tedavi planlaması, rapor oluşturma, hasta iletişim.

Bulma: çoklu ajan çoğu kategoride tek-LLM'de egemenlik göstermiyor. Çoklu ajan avantajı dar  alt görevlerin açıkça ayrılabilir olduğunda görev parçalanması yardımcı olur (diagnostik + tedavi); koordinasyon genel maliyeti uzmanlık kazancını (raport oluşturma) aşırırken zarar görür.

MedAgentBoard'un dersi genelleştirirse, önerilen birçok multi-agent sistemi aşırı tasarlanmıştır.

### AgentArch  Girişimci mimarlıklar

ArXiv:2509.10769. Kullanım, bellek ve orkestrasyonla birlikte katlanmış işletme ayarları. Benchmark her katmanın katkılarını izole eder: araç eklemenin ne kadar yardımı var? bellek eklemek? çoklu ajan orkestrasyonu eklemek?

Bir kurumsal ajan yığınını tasarladığınızda ve her katmanı haklı çıkarmanız gerektiğinde kullanın. AgentArch, değerini ölçemediğiniz özellikleri satın almaktan kaçınmanıza yardımcı olur.

### SWE-bench Pro  gerçeklik kontrolü

ArXiv:2509.16941. İşletme uygulamaları, B2B hizmetleri ve geliştiriciler aracı kapsamında 41 deposu üzerinde 1865 sorun.**uncontaminated**Frontier modelleri Pro'da %23 oranında verified'de %70 oranında puan alıyor.

Nisan 2026 notları:
- Claude Opus 4.7 Pro: **64.3%**(Agent-team koordinasyonu ile bildirildi; henüz Anthropic ilk kaynağı yayınlanmadı  ön raporu olarak ele alınmıştır).
- Verdent (Agent Eklenti) Verified: **76.1% pass@1**([technical report](https://www.verdent.ai/blog/swe-bench-verified-technical-report))
- Pro'da ajan asfaltlaması olmayan sınırlı ham puanlar: ~23-35% ([SWE-bench Pro paper](https://arxiv.org/abs/2509.16941))

"SWE-bench Verified'i yenmiştik" artık yetenek kanıtı değildir. Pro, mevcut geçit testidir. Ajan-eğitim asfaltlaması, 2026'da çoklu ajan koordinasyonu için en güçlü empirici argümanlardan biri olan Pro'da ölçülebilir kazançlar üretir (~30-40 puan delta).

### AAAI 2026 WMAC

AAAI 2026 Köprü Programı  Çoklu Ajan Koordinasyonu Atölyesinde (https://multiagents.org/2026/) 2026'da çoklu ajanlı AI araştırmaları için topluluk odak noktası. Kabul edilen makaleler ve atölye işlevleri yeni yöntemlerin değerlendirilmesi için kanonik bir yerlerdir.

### Referans iddialarını şüpheci bir şekilde okuyun  2026 kontrol listesini

Birisi çoklu ajanlı bir sonuç talep ettiğinde:

1. **Which benchmark, which split?**SWE-benç Verified vs Pro çok önemli. Yanlış bölünme ile rapor edilen bir sayı değersiz.
   Çeviri:**哪个基准，哪个分割？**SWE-bench Verified vs Pro 差 çok büyük.
2. **Contamination check.**Eğer modelin eğitim kesiminden sonra verildiyse dikkatli olun.
   Çeviri:**污染检查。**基准是否在模型训练截止日期后发布? yoksa, dikkatli olarak muamele yapın.
3. **Baseline comparison.**Tek bir LLM başlangıç noktası vs rastgele vs önceki çoklu ajan çalışmaları.
   Çeviri:**基线比较。**Tek bir LLM'de çalışmak için, "bir sistemle karşılaştırıldığında daha iyi bir sürüm değil".
4. **Statistical significance.**N testleri, p değeri, güven aralığı.
   Çeviri:**统计显著性。**N 次试验、p 值、置信区间──前沿模型是高方差的;单次运行误导──
5. **Task diversity.**Genelleştirme üretim için önemli.
   Çeviri:**任务多样性。**Bir görev mi yoksa çok mu? Üretim için genelleşme önemlidir.
6. **Cost disclosure.**%90'lık bir çözüm 20 kat daha pahalı bir iş kararı, yetenek iddiası değil.
   Çeviri:**成本披露。**Her görev için belirti  20 % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %

### Benchmarkların hiçbiri neyi iyi ölçmedi

- **Long-horizon coordination.**Günlerce divar saatleri ile etkileşim.
- **Adversarial resilience.**Bir ajan kötü niyetli veya tehlikeli olduğunda ne olur?
- **Drift under deployment.**Benchmarks statik; üretim dağılımları değişir.
- **Cost-normalized performance.**Çoğu referans, dolar başına doğru değil, çıplak doğruluk rapor ediyor.

Aslında önem verdiğiniz bir eksenizin kendi iç standartınızı oluşturmak genellikle doğru bir adımdır.

## Yapın.
```figure
a5-bench-gap
```

## Yapın

`code/main.py`etkileşimsiz bir geçiş yolu:

- Oyuncak görevinde 3 çoklu ajan sistemi simüle eder.
- Her biri için MARBLE tarzı kilometrelik metrikleri hesaplar.
- "Eğitim" setinden görevleri gizleyerek kirliliği kontrol eder.
- Açıkça rastgele bir başlangıç çizgisi ile karşılaştırılır.
- Referans talepleri puan kartı basar.

Çık:

```bash
python3 code/main.py
```

Beklenen çıkış: çürük doğrulukla sistem puan kartı, ana nokta başarısı, görev başına maliyet, rastgele başlangıç çizgisi delta ile kirlilik kontrol notu.

## Kullanın Kullanın

`outputs/skill-benchmark-reader.md`Birçok ajanla ilgili referans değerini okumak ve kontrol kontrol listesini uygulamak.

## Gönderin.

Üretim değerlendirme disiplini:

- **Build an internal benchmark**Halkın referans değerleri, bilgi verir, fakat değiştirmez.
  Çeviri:**构建内部基准** reflects your actual production distribution― public basis provides information but cannot be substituted―
- **Include a random baseline**Eğer koordinasyon görevinde rastgele bir oranla büyük bir farkla yenemezseniz, görev yanlış bir şekilde ayarlanabilir.
  Çeviri:**在每个比较中包含随机基线。**Eğer koordinasyon görevinde büyük ölçüde geçemezsen, görev tanımlanamaz.
- **Report cost alongside accuracy.**Token fiyatı ve duvar saati.
  Çeviri:**同时报告成本和准确率。**İşaret 成本和挂钟时间──运维团队都需要──
- **Rebuild the benchmark quarterly.**Üretim dağılımında değişiklikler; eski referans değerleri yanıltıcı.
  Çeviri:**每季度重建基准。**Üretim dağılımı yön değiştirdi; geçmişte temel kuruluşlar yanlış yönlendirilmiştir.
- **Avoid published-benchmark overfitting.**Takımınız özel olarak SWE-bench Pro numaraları için optimize ediyorsa, üretime geri döneceksiniz.
  Çeviri:**避免公开基准过拟合。**Eğer takımınız özel olarak SWE-bench Pro numarasını optimize ederse, siz de üretim üzerinde geri dönersiniz.

## Egzersizler.

1. Çık .`code/main.py`Üç simülasyon sistemden hangisinin en iyi maliyetleri olduğu belirlenir.
2. MultiAgentBench'i okuyun (arXiv:2503.01935). Kendi görev alanınız için, MARBLE'nin önerdiği dört topolojiden hangisini seçin.
3. SWE-bench Pro kağıdı okuyun.
4. COMMA'nın multimodal koordinasyonla ilgili bulgularını okuyun. İç standart değerinize ekleyebileceğiniz basit bir multimodal koordinasyon görevi tasarlayın.
5. Benchmark-davayeleri kontrol listesini son bir çok ajan gazetesinin başlık sonuçlarına uygulayın.

## Anahtar Terimler

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| MARBLE | "MultiAgentBench" / "多 Agent 基准" | ACL 2025; star/chain/tree/graph topologies with milestone KPIs. / ACL 2025；星形/链形/树形/图形拓扑，带里程碑 KPI。 |
| COMMA | "Multimodal benchmark" / "多模态基准" | Multimodal asymmetric-info coordination; frontier models struggle vs random. / 多模态不对称信息协调；前沿模型难以超越随机基线。 |
| MedAgentBoard | "Domain stress test" / "领域压力测试" | Four medical categories; often finds multi-agent does not dominate single-LLM. / 四个医疗类别；常发现多 Agent 不优于单 LLM。 |
| AgentArch | "Enterprise benchmark" / "企业基准" | Tools + memory + orchestration layered. / 工具 + 记忆 + 编排分层。 |
| SWE-bench Pro | "Contamination-resistant" / "抗污染" | 1865 problems, 41 repos; ~23% vs 70%+ on Verified (the contamination signal). / 1865 个问题，41 个仓库；~23% vs Verified 上 70%+（污染信号）。 |
| Milestone achievement / 里程碑达成 | "Partial credit" / "部分积分" | Benchmarks that reward progress, not only final success. / 奖励进展而非仅最终成功的基准。 |
| Contamination / 污染 | "Benchmark leaked into training" / "基准泄露到训练" | Post-release, benchmarks drift into training corpora; scores inflate. / 发布后，基准渗入训练语料；分数膨胀。 |
| WMAC | "AAAI 2026 Bridge Program" / "AAAI 2026 桥接项目" | Workshop on Multi-Agent Coordination; community focal point. / 多 Agent 协调研讨会；社区焦点。 |

## Daha fazla okumak

- [MultiAgentBench / MARBLE](https://arxiv.org/abs/2503.01935) MİLİK'ler ile topoloji referans göstergesi
- [MARBLE repository](https://github.com/ulab-uiuc/MARBLE) Referans uygulanması
- [MedAgentBoard](https://arxiv.org/abs/2505.12371) alan stres testi; çoklu ajan genellikle baskın değildir
- [AgentArch](https://arxiv.org/abs/2509.10769) Girişimci ajan mimarisi
- [SWE-bench leaderboards](https://www.swebench.com/) Sınır modelleri için doğrulanmış ve pro puanları
- [AAAI 2026 WMAC](https://multiagents.org/2026/) 2026 yılındaki topluluk odak noktası
