# Yerarşik Mimarlık ve Başarısızlık Modu

> Yerarşik, yöneticilerden yöneticilerden yöneticilerden çalışanlardan daha fazla yöneticilerden daha fazla yöneticilerden daha fazla yöneticilerden daha fazla yöneticilerden daha fazla yöneticilerden daha fazla yöneticilerden daha fazla yöneticilerden daha fazla yöneticilerden daha fazla yöneticilerden daha fazla yöneticilerden daha fazla yöneticilerden daha fazla yöneticilerden daha fazla yöneticilerden daha fazla yöneticilerden daha fazla yöneticilerden daha fazla yöneticilerden daha fazla yöneticilerden daha fazla yöneticilerden daha fazla yöneticilerden daha fazla yöneticilerden daha fazla yöneticilerden daha fazla yöneticilerden daha fazla yöneticilerden daha fazla yöneticilerden daha fazla yöneticilerden daha fazla yöneticilerden daha fazla yöneticilerden daha fazla yöneticilerden daha fazla yöneticilerden daha fazla yöneticilerden daha fazla yöneticilerden daha fazla yöneticilerden daha fazla yöneticilerden daha fazla yöneticilerden daha fazla yöneticilerden daha fazla yöneticilerden daha fazla yöneticilerden daha fazla yöneticilerden daha fazla yöneticilerden daha fazla yöneticilerden daha fazla yöneticilerden daha fazla yöneticilerden daha fazla yöneticilerden daha fazla yöneticilerden daha fazla yöneticilerden daha fazla`Process.hierarchical`ders kitabı versiyonu: a `manager_llm`LangGraph eşdeğeri `create_supervisor(create_supervisor(...))`Bu, iş gerçek bir org çizelgesinde olduğu zaman doğal bir kalıptır. Aynı zamanda yönetimsel döngüye düşeceği en olası kalıptır.

> **【中文解读】**Bu bölüm karmaşık görevlerin geri dönüşümlü çözülmesi için uygulanabilen çok katlı düzenleyici yapılarının birleştirilmiş örgüt yapısını tanıttı.

> **【拓展：hierarchical architecture→具体应用】**Bölümsel yapı, gözetmen modeline geri döner 嵌套 üst düzey yöneticiler orta düzey yöneticilere, orta düzey yöneticiler alt düzey işçilere yeniden dağıtılar  Bu, insan örgütünün düzey yapılarına benzer 2026 yılının pratik gösterdiği gibi,2-3 düzey seviyelerinin en iyisi  çok az 1 düzey) yöneticilerin yüklenmesine, çok derin  4+ düzeylerine yol açar  bilgi kaybına ve gecikme artışına yol açar 


**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 16 · 05 (Supervisor Pattern) | **前置知识:** Phase 16 · 05 (监督者模式)
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**Öğrenci bölümünün ilk aşaması: 16·05(Sövizör 模式)。本节 = Sövizör 嵌套 Sövizör多层管理。失败模式 = "menerileri açıp oturup iş yapmıyor"。
>  **【类比】**Bölümsel yapı = "Şirket seviyesinde"──1 seviyede = 创业公司;;CEO 直接带工程师);2-3 seviyede = 中型公司;;最优;4+层 = 大企业病(信息失真、决策缓慢、经理们皮)──Agent也一样2-3 seviyede 优,多了就"管理循环":经理 代理相互指派却不真事──
> ️ **【易错点】**看到"任务复杂"就加层级 → 管理开销压系统──修复:先用序列或监督者单层跑,确认不够再分层;2-3层是上限──

## Sorunlar sorunun giriş

Bir kez yönetici örneği tıklandığında, doğal bir sonraki adım "işçilerin kendileri yönetici ise ne olacak?"

> Bir gözlemci modeli anladıktan sonra, doğal bir sonraki adım "Eğer iş makinesi kendisi de gözlemci mi?" bir ekip vardır; şirketin bir bölümü vardır.

Bu nedenle insan kuruluşları bu şekilde çalışırken, ayartma güçlüdür. Ancak LLM hiyerarşileri insan hiyerarşilerinin tüm patolojilerini (bilgi kaybı, yanlış iletişim, yavaş iterasyon) insan ilişkilerinin ve ortak kültürün istikrarlı etkilerinin olmadan miras alır.

> 诱惑很强,因为人类组织这样工作──但LLM seviyesi tüm insan seviyesi hastalıklarını miras aldı, ancak insan ilişkileri ve ortak kültürünün sabit etkileri yok──

Sorun: LLM yöneticileri insan yöneticileriyle aynı değildir. Bir insan yöneticisi raporlarının bildikleri konusunda sabit geçmişlere sahiptir. LLM yöneticisi her dönüşü, org'u bağlamında olan her şeyden yeniden akla getirir. Bu bağlamda küçük bir sürükleme ve tüm ağaç işyi yanlış yerleştirir.

> 问题在:LLM 管理者与人类管理者不同.人类管理者对其下属知道有稳定的先验.LLM 管理者每轮从其上下文中的内容重新推论组织──上下文中的微小漂移,整个树就会错分配工作──

Bu, hiyerarşik LLM sistemlerinin temel başarısızlık modudur: her yönetim düzeyi önceki düzeyin hatalarını artırır. En üstteki %5 yanlış tahsis, her düzeyinde (hepsi yanlış) delegasyonu yeniden yorumladığı için, 3. düzeyde %25 olur.

> Bu, bölgelik LLM sisteminin temel başarısızlık modudur: Her yöneticinin üst düzey hatası arttırılır. Üst düzey 5%'in hataları üçüncü düzeylere 25%'e dönüşür. Çünkü her düzey yeniden açıklanır.

## Konsept merkezi konsept

### Şekil

```
                 Manager
                 ┌─────┐
                 └──┬──┘
           ┌────────┴────────┐
           ▼                 ▼
       Sub-Mgr A         Sub-Mgr B
       ┌─────┐           ┌─────┐
       └──┬──┘           └──┬──┘
         ┌┴──┬──┐          ┌┴──┐
         ▼   ▼  ▼          ▼   ▼
       W1  W2  W3         W4  W5
```

Her iç düğüm planlar, delegeler ve sentezler.

> Her iç nokta planlama, görev ve genel birleştirme. Sadece yapay noktalar gerçek iş yapmaktadır.

Bu, hem güçlü (aile zihinsel model) hem de zayıflık (insan organlarının LLM'lerin eksik olduğu istikrarlı geçmişleri vardır) olan bir insan organ tablosunu yansıtır.

> Bu, insan örgütlerinin yapısını yansıtır, bu da onun avantajlarıdır.

### # Parladığı yerde #

- **Clear org mapping.**Eğer gerçek görev bölümselse ("dokümanı yasal olarak incelemek, finansal olarak incelemek, mühendislik olarak incelemek, sonra exec için özetlemek") hiyerarşi açıkça görülür.
  Çeviri:**清晰的组织映射。**Eğer gerçek görev departmansal ise, "Fakistik inceleme dosyası, Mali inceleme dosyası, İnjenerasyon inceleme dosyası, sonra da yönetim kurulu genel sonucu için"), düzey yapı belirgin olacaktır.
- **Local summarization.**Her alt yöneticiler, üst yöneticiler tarafından görmeden önce takımlarının çıkışını sentezler.
  Çeviri:**局部摘要。**Her bir yöneticinin üst düzey yöneticinin görmesi, önce ekiplerinin çıkışlarını birleştirir.

### Kırık olduğu yerlerde

2026'da yapılan ölüm sonrası testler üç başarısızlık modunu bulmaya devam ediyor:

> 2026 yılının son analizinde sürekli olarak üç başarısızlık modeli bulunmaktadır:

Cemri et al. (MAST, arXiv:2503.13657) bunları "spesifikasyon başarısızlığı" ve "insanlararası yanlış uyum" alt aile olarak belgelendirir.

> Cemri 等人(MAST,arXiv:2503.13657) bu sorunları "规范失败" ve "人际不对齐"子家族──分层系统 平系统 平系统 比较容易出现这些问题,因为每个层添加重新解释步骤──

1. **Task assignment error.**Yöneticisi hedefi okuyor, bir parçalanmayı halüsinasyonlar yapar ve yanlış alt yöneticisine delegasyon yapar. Alt yöneticinin verilen şeyi itaatle çalıştığı için hata sadece en üst sentezde ortaya çıkar.
   Çeviri:**任务分配错误。**Yöneticiler hedefleri okuyor, hayallerini çözer, hataları yanlış yöneticilere gönderir. Çünkü çocuk yöneticiler belirli görevleri yerine getirmeye itaat eder. Hatalar sadece en üst düzey genel zamanlarda ortaya çıkar.
2. **Output misinterpretation.**Alt yöneticisi "X iddiasını doğrulayamıyor". Top yöneticisi "X iddiası onaylanmamış" olarak özetler.
   Çeviri:**输出误解。**Sonraki makale: "Yönetici" dönemi, "Yönetici" dönemi, "Yönetici" dönemi, "Yönetici" dönemi, "Yönetici" dönemi, "Yönetici" dönemi, "Yönetici" dönemi, "Yönetici" dönemi, "Yönetici" dönemi, "Yönetici" dönemi, "Yönetici" dönemi, "Yönetici" dönemi, "Yönetici" dönemi, "Yönetici" dönemi, "Yönetici" dönemi, "Yönetici" dönemi, "Yönetici" dönemi, "Yönetici" dönemi, "Yönetici" dönemi, "Yönetici" dönemi, "Yönetici" dönemi, "Yönetici" dönemi, "Yönetici" dönemi, "Yönetici" dönemi, "Yönetici" dönemi" dönemi, "Yönetici" dönemi, "Yönetici" dönemi" dönemi, "Yönetici" dönemi" dönemi, "Yönetici" dönemi" dönemi" ifadesi, "Yönetici" ifadesi, "Yönetici" ifadesi, "Yönetici" ifadesi" ifadesi, "Yönetici" ifadesi, "Yönetici" ifadesi" ifadesi, "Yönetici" ifadesi, "Yönetici" ifadesi, "Yönetici" ifad" ifad" ifad "Yönemi, ifad, ifad, ifad, ifad, ifad, ifad, ifad, ifad, ifad, ifad, ifad, ifad, ifad, ifad, ifad, ifad, ifad, ifad, ifad, ifad, ifad, ifad, ifad, ifad, ifad, ifad, ifad, ifad, ifad, ifad, ifad, ifad, ifad, ifad, ifad, ifad, ifad, ifad, ifad, ifad, ifad, ifad, ifad, ifad, ifad, is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is is
3. **Consensus loops.**İki alt yöneticinin görüşleri farklıdır; üst yöneticiler onları uzlaşmaları için çağırır; onlar yeniden görevlendirilir; işçiler yeniden çalışırlar; alt yöneticiler biraz farklı cevaplar verir; döngü. CrewAI'nin `Process.hierarchical`Bu konuda adım sınırları ile korunmak gerekir, ama sınırın kendisi artık bir hiperparametre.
   Çeviri:**共识循环。**İki çocuk yöneticisi anlaşmaz; üst düzey yöneticisi onları koordine etmek istiyor; aşağıya doğru yeniden görevlendirildi; çalışma makinesi yeniden çalıştırıldı; çocuk yöneticisi geri döndü; farklı cevaplar vardı; döngü-¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬`Process.hierarchical`通过步骤限制来保护,但限制本身现在是一个超参数――

### Önemli soru

Sıralı (lineer boru hattı) vs hiyerarşik: göreviniz aslında bağımsız alt takımlara sahip mi, yoksa bir ağaç gibi davranan bir çizgi akış mıdır?

> 顺序(线性流水线) vs 分层: Senin görevin gerçekten bağımsız bir alt takım var, aynı zamanda bir ağaç gibi sahte bir 线性流? Eğer sonrakilerse, 顺序 kullanın.

Bu, çoğu takım atlayan test. Yüksek derecede hiyerarşik olanlara ulaşırlar çünkü karmaşık görünüyor, sonra haftalarca parçalanma sürüşünü düzeltirler.

> Bu, çoğu takımın atladığı testlerdir. Yüksek gibi görünen için sınıflandırmayı seçerler, sonra birkaç hafta boyunca bu bölümde çalışıp, bu bölümde hareket ederler.

### CrewAI'nin uygulanması
### Rol çerçevesinin uygulanması

CrewAI'nin `Process.hierarchical`Müdür, uzman ekipler üzerinden bir yöneticinin LLM'sini bağlar.

> `Process.hierarchical`Bu nedenle, bu konuda bir araştırma yaparak, bir araştırma yaparak, bir araştırma yaparak, bir araştırma yaparak, bir araştırma yaparak, bir araştırma yaparak, bir araştırma yaparak, bir araştırma yaparak, bir araştırma yaparak, bir araştırma yaparak, bir araştırma yaparak, bir araştırma yaparak, bir araştırma yaparak, bir araştırma yaparak, bir araştırma yaparak, bir araştırma yaparak, bir araştırma yaparak, bir araştırma yaparak, bir araştırma yaparak, bir araştırma yaparak, bir araştırma yaparak, bir araştırma yaparak, bir araştırma yaparak, bir araştırma yaparak, bir araştırma yaparak, bir araştırma yaparak, bir araştırma yaparak, bir araştırma yaparak, bir araştırma yaparak, bir araştırma yaparak, bir araştırma yaparak, bir araştırma yaparak, bir araştırma yaparak, bir araştırma yaparak, bir araştırma yaparak, bir araştırma yaparak, bir araştırma yaparak, bir araştırma yaparak, bir çalışma yaparak, bir çalışma yaparak, bir çalışma yaparak, bir çalışma yaparak, bir çalışma yaparak, bir çalışma yaparak, bir çalışma yaparak, bir çalışma yaparak, bir çalışma yaparak, bir çalışma yaparak, bir çalışma yaparak, bir çalışma yaparak, bir çalışma yaparak, bir çalışma yaparak, bir çalışma yaparak, bir etkileşmek üzere, bir etkileşmek üzere, bir etkileşmek üzere,

Yöneticisi LLM kendi bağlamı, tescil ve araçları ile tam bir ajandır. Deterministik bir dispatcher değildir.

> 管理者 LLM kendisi bir kendi kendine aşağıya 提示和工具の完全なエージェントである.  Bu bir kararlılık düzenleyicisi değildir.

- En üst düzey görev alır,
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri
- mürettebatlara alt görevler verir,
  Çıktı.
- mürettebatın çıkışlarını değerlendirir,
  Çeviri: değerlendirme ekip,
- kabul, yeniden devretme veya tekrarlama karar verir.
  Çinçe Çevirisi: karar kabul edilmek, yeniden görevlendirmek veya verilmek.

Belge: https://docs.crewai.com/en/introduction(Közel kavramlar altında "Hiyerarşik süreç" için bakınız).

> 文档:https://docs.crewai.com/en/introduction（在核心概念中查找"Hierarchicalİşlem")

### LangGraph'in uygulanması
### Grafik çerçevesinin uygulanması

LangGraph , yuva yapılmış kullanıyor .`create_supervisor`İç yöneticinin kendi grafikleri vardır; dış yöneticisi iç grafikleri açık olmayan bir düğüm olarak değerlendirir. Bu, debugging için CrewAI'den daha temizdir (her grafikleri ayrı ayrı geçebilirsiniz), ancak ağacın dinamik yeniden şekillendirilmesini ifade etmek daha zordur.

> LangGraph kullanın `create_supervisor`调用──内部监督者有自己的图;外部监督者将内部图视为不透明节点──调试方面比 CrewAI更清晰(各图中分步进可以分别进进),但更难表达树的动态重塑──

Çözümleme kazancı gerçek: 3 seviye LangGraph hiyerarşisinde bir şey ters gittiğinde, her grafikten bağımsız olarak geçerek hangi seviyenin başarısız olduğunu izole edebilirsiniz. CrewAI'de, yöneticisi LLM yanlış devredilen bir açık olmayan çağrıdır.

> 调试优势真实: 3 kat LangGraph seviyesi hatalı olduğunda, her bir çizimden bağımsız bir adım atarak hangi seviyeden başarısız olduğunu ayırıp ayırt edebilirsiniz.

İpucu: https://reference.langchain.com/python/langgraph-supervisor.

> Referans:https://reference.langchain.com/python/langgraph-supervisor。

## Yapın.
```figure
swarm-hierarchy-token
```

## Yapın

`code/main.py`3 seviye hiyerarşi vardır:

> `code/main.py`3 katlı bir işlev:

- üst düzey yöneticisi: bir görevi "muhendislik" ve " hukuki" bölümlere ayırır.
  Çin Çeviri: Top层管理者:将任务分分为工程和法务分支,
- Mühendislik alt yöneticisi: "frontend" ve "backend" işçilere ayrılır,
  Çeviri: "İşcilik"
- Yasal alt yöneticisi: bir işçi.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri

Demo mutlu yolla karşıtlık gösterir (herkes aynı fikirde)**perturbed path**Yöneticinin ayrıştırılması "yasal" olarak "maliye" olarak yanlış etiketlediği ve hata kaskasasını izlediği yerde  alt yöneticinin itaatli bir şekilde finans işi yapması, üst sentezörün finans bulgularını rapor etmesi, orijinal yasal sorunun cevabı kalmamış kalması.

> 演示对比了正常路径 (düşünme)**扰动路径**, üst düzey yöneticilerin ayrıntıları "Financial" olarak yanlış işaretlenmiş ve yanlış gözlemlenmiş; üst düzey yöneticilerin raporları finansal olarak ortaya çıkmıştır; orijinal yasal sorunlar cevaplanmamıştır;;

Çelişkili yol uyarıdır: hiyerarşik sistemler hataları sessizce artırır. Alt yöneticisi geri çekilmez ("finans dediysiniz, ama görev yasal dedi").

>  perturbatory route is warning:分层系统静默放大错误──子管理者不反驳("Söylediğin finansal, fakat görevin söylediği法务")──它假设管理者更了解──当任何人注意到时,原始意图已丢失──

Çık:

```
python3 code/main.py
```

Çıktım, her iki yolun da açık bir yan yana "ne istendi" vs. "ne teslim edildi" gösterir.

> 输出显示两条路径的清晰并排对比:"要求什么"与"交付了什么"──

## Çerçeveyi kullanın.

`outputs/skill-hierarchy-fitness.md`Görevlerin hiyerarşik, sıradan veya düz yönetici kullanılması gerektiğini değerlendirir. Girişler: görev açıklaması, org yapısı, uzlaşma bütçesi. Çıktı: belirli başarısızlık modlarına karşı korunmak için bir model önerisi.

> `outputs/skill-hierarchy-fitness.md`评估给定任务应使用分层、顺序还是平监督者──输入:任务描述、组织结构、协调预算──输出:模式建议及需要防护的特定失败模式──输入: görev tanımlaması、 örgüt yapısı、 koordinasyon bütçesi、输出:模式建议及需要防护的特定失败模式──

## İndirin . Ürünler .

Eğer hiyerarşik bir gemi varsa:

> Eğer deployment aşama yapı:

- **Cap tree depth at 2.**Üç seviyede zaten çoğu hata gözlemlenebilirlikten gizlenir.
  Çeviri:**将树深度限制在 2。**Üç kat daha fazla hata gözlemlenme dışındadır.
- **Explicit reconciliation budget.**Yöneticinin en üst düzey görevlerini yapmadan önce en fazla bir sayı ayarlayın.
  Çeviri:**明确的协调预算。**Üst düzey yöneticisi göndermeden önce en büyük sıra sayısını ayarlamalıdır.
- **Provenance on every synthesis.**Her düğümün özetinde hangi yaprak çıkışı üretildiğini belirtmek gerekir.
  Çeviri:**每次综合的来源追溯。**Her noktunun özetleri, yaprak çıkışını oluşturmak için alıntı yapmalıdır.
- **Alert on decomposition drift.**Yöneticinin parçalanmasını adım adım kaydet; kullanıcı sorguyla karşılaştırın.
  Çeviri:**分解漂移告警。**Kayıt yöneticisi'nin her adımı ayrıştırılması; kullanıcı sorgularına karşı.

## Egzersizler.

1. Çık .`code/main.py`Yukarı çıkışın kullanıcı sorusundan tamamen farklı olması için kaç düzeyde yöneticinin teslim olması gerekir?
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`code/main.py`Normal yollarla rahatsızlık yolları arasında bir kıyaslama yok. Üst düzey çıkışını tamamen kullanıcılardan uzaklaştırmak için kaç düzey yöneticinin iletişim kurması gerekir?
2. Üçüncü bir seviye ekleyin (yukarı -> alt -> alt -> alt -> işçi). Bozuklu yolun derinlik büyüdükçe ne sıklıkla kendisini düzelttiğini ölçün.
   Çine çevirisi: ek üçüncü katı (solu katı)
3. Her alt yöneticide, orijinal kullanıcı sorusu her zaman değişmeden sorulan bir "kanar" işçisi uygulayın.
   Çinçe çevirisi: Bir "Kins雀" çalışma makinesi gerçekleştirmek için her bir çocuk yöneticisi, genellikle orijinal kullanıcı sorusu sorulur.
4. CrewAI'nin yazısını okuyun.`Process.hierarchical`CrewAI'nin uyguladığı bir beton koruma rayı (adım sınırı, manager_llm kısıtlaması) tanımlayın ve hangi başarısızlık modunu hedeflemesini açıklayın.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`Process.hierarchical`文档──识别 CrewAI 应用一个具体防护措施(步骤限制、管理者_llm 约束)并描述它针对的失败模式──
5. Yatağındaki LangGraph denetleyicilerini CrewAI hiyerarşikleriyle karşılaştırın.
   Çinçe Çevirimi: LangGraph 监督者与 CrewAI 分层── hangi koordinasyon döngüsünü daha kolay kontrol eder?

## Anahtar Şartlar .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Hierarchical / 分层 | "Org chart pattern" / "组织架构模式" | Supervisors over supervisors; only leaves do work. / 监督者之上还有监督者；只有叶子节点做实际工作。 |
| Manager LLM / 管理者 LLM | "The boss" / "老板" | The LLM that decomposes, assigns, and validates at an internal node. / 在内部节点进行分解、分配和验证的 LLM。 |
| Decomposition drift / 分解漂移 | "The boss lost the plot" / "老板偏离了主题" | Top manager's split no longer covers the original question. / 顶层管理者的拆分不再覆盖原始问题。 |
| Reconciliation loop / 协调循环 | "Endless meetings" / "无尽会议" | Sub-managers disagree; top re-delegates; workers re-run; loop until budget exhausted. / 子管理者不一致；顶层重新委派；工作器重新运行；循环直到预算耗尽。 |
| Depth-2 ceiling / 深度-2 上限 | "Don't go deeper than 2 levels" / "不要超过 2 层" | Empirical guardrail: 3+ levels collapses observability. / 经验防护：3+ 层使可观测性崩溃。 |
| Canary question / 金丝雀问题 | "Ground truth at every level" / "每层的基准真相" | A worker that is always asked the original query unchanged, to detect drift. / 一个总是被问及原始查询不变的工作器，用于检测漂移。 |
| Provenance chain / 来源链 | "Who said what" / "谁说了什么" | Trace from each synthesis back to the leaf outputs that produced it. / 从每个综合追溯到产生它的叶子输出。 |

## Daha fazla okumak

- [CrewAI introduction — Process.hierarchical](https://docs.crewai.com/en/introduction) Yöneticisi ile ders kitabı hiyerarşik LLM
  Çeviri:CrewAI 介绍  Process.hierarşik  带管理者 LLM 的教科书式分层
- [LangGraph supervisor reference](https://reference.langchain.com/python/langgraph-supervisor) Yörüngede bulunan bir gözetmen tarafından`create_supervisor`
  中文翻译:LangGraph 监督者参考  通过 `create_supervisor`Bu yüzden de bu konuda bir şey yapmamalıyız.
- [Anthropic engineering — Research system](https://www.anthropic.com/engineering/multi-agent-research-system) Antropic neden hiyerarşikten daha fazla flat supervisor seçti
  Çinçe Çevirimi:Antropik 工程  研究系统  Neden Antropik                                                                                                                                                                                                                                                    
- [Cemri et al. — Why Do Multi-Agent LLM Systems Fail?](https://arxiv.org/abs/2503.13657) MAST taksonomisi; koordinasyon hataları bölümü
  Çinçe Çevirimi:Cemri  et al  Neden çok ajan LLM 系统会失败?  MAST 分类法;协调失败部分记录了分解漂移
