# Edge Inference  Apple Neural Engine, Qualcomm Hexagon, WebGPU/WebLLM, Jetson 推理 边缘 LLM GPU 欧盟

> Temel kenar kısıtlaması, hesaplama değil hafıza bant genişliği. Mobil DRAM, 50-90 GB/s'de oturuyor; HBM3 veri merkezi 2-3 TB/s  30-50x boşluğu temizliyor. Deşifreleme hafıza bağlanmış, bu yüzden boşluk belirleyici. 2026'da manzara dört bölüme ayrılır. Apple M4/A18 Neural Engine, birleşik bellek (CPU NPU kopyası) ile 38 TOPS'e ulaştı. Qualcomm Snapdragon X Elite / 8 Gen 4 Hexagon 45 TOPS'e ulaştı. WebGPU + WebLLM, M3 Max'te Llama 3.1 8B (Q4) ile ~41 tok/s ile çalışır (doğuştan yaklaşık %70-80%); 17.6k GitHub yıldızları, OpenAI uyumlu API, ~70-75% mobil kapsama. NVIDIA Jetson Orin Nano Super (8GB) Llama 3.2 3B / Phi-3'ye uyar; AGX Orin vLLM üzerinden gpt-oss-20b'yi ~40 tok/s'de çalışır; Jetson T4000 (JetPack 7.1) 2x AGX Orin. TensorRT Edge-LLM EAGLE-3, NVFP4, parçalanmış prefill  tarafından CES 2026'da gösterilen EAGLE-3, NVFP4 desteğini sağlar.

> **【中文解读】**Bu bölüm, sınırlı bir ekipman üzerinde yerleştirilen LLM'nin zorlukları ve çözümlerini anlatıyor.
**Type:** Learn
**Languages:** Python (stdlib, toy bandwidth-bound decode simulator)
**Prerequisites:** Phase 17 · 04 (Serving Engine Internals), Phase 17 · 09 (Production Quantization)
**Time:** ~60 minutes


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy bandwidth-bound decode simulator) | **语言:** Python
**Prerequisites:** Phase 17 · 04 (vLLM Serving Internals), Phase 17 · 09 (Production Quantization) | **前置知识:** Phase 17 · 04 (vLLM Serving Internals), Phase 17 · 09 (Production Quantization)

>  **【前置】**Önemli bir şekilde, bu süreçte, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir sürece bir sürececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececece
>  **【类比】**边缘 vs 数据中心 = "手机 vs 超算"。手机 DRAM 50-90 GB/s,数据中心 HBM3 2-3 TB/s30-50 倍差,解码(内存绑定) 下决定性。2026 四大平台:Apple NE(38 TOPS 统一内存)、Qualcomm Hexagon(45 TOPS)、WebGPU+WebLLM(M3 Max 跑 Llama 3.1 8B 41 tok/s)、Jetson(Orin AGX 跑 gpt-oss-20b 40 tok/s)。TensorRT Edge-LLM 支持 EAGLE-3 + NVFP4 + chunked prefill。
**Time:** ~60 minutes | **时间:** ~60 minutes

## Öğrenme hedefleri

- Mobil LLM sonuçlarının neden hafıza bant genişliği ile sınırlı olduğunu ve hesaplamaların neden ikinci sırada olduğunu açıklayın.
  Çinçe Çevirimi: Neden hareket LLM 推理 内存带宽限定的, hesaplama yeteneği ise sıradan 
- Dört kenar hedefi (Apple ANE, Qualcomm Hexagon, WebGPU/WebLLM, NVIDIA Jetson) listeleyin ve her birini bir kullanım durumuna eşleştirin.
  Çinçe Çevirimi Çevirisi:列举四个边缘目标(Apple ANE、Qualcomm Hexagon、WebGPU/WebLLM、NVIDIA Jetson)并匹配每个用例──
- 2026 WebGPU kapsamı boşluğu (Firefox Android yakalama) ve Safari iOS 26 inişini isimlendirin.
  ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇXV ÇX ÇX ÇX ÇX ÇX ÇX ÇX ÇX ÇX ÇX ÇX ÇX ÇX ÇX ÇX ÇX Ç Ç Ç ÇX Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç
- Hedef başına bir kuantitasyon biçimi seçin (Core ML INT4 + FP16 için ANE, QNN INT8/INT4 için Hexagon, WebGPU Q4 için tarayıcı, NVFP4 için Jetson Thor).
  Çinçe Çevirimi: için her hedef seçimi ölçüm biçimi(ANE kullanmak Core ML INT4 + FP16, Hexagon kullanmak QNN INT8/INT4, Browser器用 WebGPU Q4,Jetson Thor kullanmak NVFP4)。

## Sorunlar. Sorunlar.

> **【中文解读】**边缘推理'nin çekirdek kısıtlaması, hesaplama kapasitesi değil, 内存带宽dır. 移动DRAM 带宽 50-90 GB/s,数据中心 HBM3 达2-3 TB/s30-50x 差距. 边缘推理'nin çekirdek kısıtlamasıdır. 边缘推理'nin çekirdek kısıtlaması belirgin bir fark. 边缘推理'nin çekirdek kısmı 边缘推理'nin 边缘推理'i. 边缘推理'nin çözümüdür. 边缘推理'nin 边缘推理'i. 边缘推理'nin 边缘推理'i. 边缘推理'nin 边缘推理'i. 边缘推理'nin 边缘推理'i. 边缘推理'i. 边缘推理'in 边缘推理'i. 边缘推理'i. 边缘推理'in 边缘推理'i. 边缘推理'i. 边缘推理'in 边缘推理'i. 边缘推理'i. 边缘推理'in 边缘推理'i. 边缘推理's 边缘推理's 边缘推理's 边缘推理's 边缘推理's 边缘推理's 边缘推理's 边缘推理's 边缘推理's 边缘推理's 边缘推理's 边缘推理's 边缘推理's 边缘推理's 边缘推理's 边缘推理's 边缘推理's 边缘推理's 边缘推理's 边缘推理's 边缘推理's 边缘推理's 边缘推理's 边缘推理's 边缘推理's 边缘推理's 边缘推理's 边缘推理's 边缘推理's 边缘推理's 边缘推理's 边缘推理's 边缘推

> **【拓展：边缘 AI 芯片市场】**2026 yılının kenarında AI 芯片 竞争格局:(1) Apple Neural Engine (M4/A18) 38 TOPS,统一内存架构,无需 CPUNPU 数据拷贝;(2) Qualcomm Hexagon (Snapdragon X Elite / 8 Gen 4) 45 TOPS,QNN SDK 提供转换链路;(3) Intel Lunar Lake / AMD Ryzen AI 30040-50 TOPS,软件生态落后于 Apple/Qualcomm;(((VIDIA Jetson Orin/Thor边缘 GPU 方案,支持vLLM 和 TensorRT Edge-LLM──语音代理是边缘推杀手级应用本地推理完全消除网络延迟──

Bir müşteri bir cihaz üzerinde bir chatbot istiyor: sesli önce, özel öntanımlı olarak, çevrimdışı çalışır. Bir MacBook Pro M3 Max'te, Llama 3.1 8B Q4 ~55 tok/s  ile çalışır. Bir iPhone 16 Pro'da, aynı model 3 tok/s  ile çalışır.

Geçerlilik varyansi bir portleme sorunu değildir. NPU'nun kullanıcı alanından erişilebilir olup olmadığı için bant genişliği farkı çarpı olarak kuantitasyon biçimi çarpı olarak kullanılır. 2026'da kenar çıkarım dört farklı çözüm ile dört farklı sorundur.

## Konsepten bir şey.

### Çubuğun genişliği gerçek tavan

> **【中文解读】**边缘推理的真正天花板是内存带宽――Decode 阶段每生成一个代币 需要读取全部权重──7B Q4 模型 3.5GB,在 50 GB/s 带宽下读取需要 70ms理论上限约14 tok/s──在 90 GB/s 高端移动 DRAM) 下上限升至25 tok/s──数据中心 HBM3在不同 3 TB/s 读取同一模型只需1.2ms上限830 tok/s──同样模型 下同权重、内存子系统──

Dekode, her token için tüm ağırlıkları okuyor. Q4'te bir 7B modeli 3.5 GB'dır. 50 GB / s'de 3.5 GB okuyarak 70 ms  ~ 14 tok / s teorik bir tavan alır. 90 GB / s (yüksek sonlu mobil DRAM) da tavan ~ 25 tok / s'ye taşınır.

Datacenter HBM3 3 TB/s'de aynı 3.5 GB'yi 1.2 ms'de temizler  tavan 830 tok/s'dir. Aynı model, aynı ağırlıklar. Farklı bellek alt sistemi.

### Apple Sinir Motoru (M4 / A18)

- 38 TOPS'e kadar. Birleştirilmiş bellek (CPU ve ANE aynı havuzyu paylaşıyor)  Kopya üstü maliyeti yoktur.
- Core ML +  üzerinden erişim`.mlmodel`Dökülen modeller veya PyTorch üzerinden Metal Performance Shaders (MPS) aracılığıyla.
- Llama.cpp Metal backend doğrudan ANE değil MPS kullanır; yerel ANE Core ML dönüşümünü gerektirir.
- 2026'da iOS uygulamaları için en iyi pratik yol: INT4 ağırlıkları + FP16 etkinleştirmeleri ile Core ML.

### Qualcomm Hexagon (Snapdragon X Elite / 8 Gen 4)

- 45 TOPS'e kadar. SoC'de CPU ve GPU ile entegre ama ayrı hafıza alanı.
- QNN (Qualcomm Neural Network) SDK ve AI Hub PyTorch/ONNX'den dönüşüm sağlar.
- Çat şablonları, Llama 3.2, Phi-3 hepsi AI Hub'da birinci sınıf eserler olarak gönderiliyor.

### Intel / AMD NPU'ları (Lunar Lake, Ryzen AI 300)

- 40-50 TOPS. Yazılım Apple/Qualcomm'dan geride kalıyor; OpenVINO gelişmekte ama niş.
- Windows ARM yardımcı pilot uygulamaları için en iyisi; yerel olarak ilk olarak AMD/Intel masaüstülerinde doğuştur.

### WebGPU + WebLLM

> **【中文解读】**WebGPU + WebLLM is browser内 LLM 推理的方案无需安装,通过 WebGPU compute shader 运行模型──在M3 Max 上 Llama 3.1 8B Q4 达到 ~41 tok/s,约为原生性能的70-80%──2026年覆盖率:Chrome Android v121+、Safari iOS 26 GA、Firefox Android 仍追赶,总体约70-75% 移动浏览器覆盖──17.6k GitHub yıldızları,OpenAI 兼容的 JavaScript API──

- WebGPU hesaplama şaderleri üzerinden tarayıcıda modeller çalıştırın; kurulmaz.
- Llama 3.1 8B Q4 M3 Max'de ~41 tok/s'de yaklaşık olarak aynı arka uç üzerinden yerli %70-80%'i.
- 17.6k GitHub yıldızları WebLLM; OpenAI uyumlu JS API; Apache 2.0.
- 2026 kapsamı: Chrome Android v121+, Safari iOS 26 GA, Firefox Android hala yakalamak. Genel olarak ~ 70-75% mobil kapsam.

### NVIDIA Jetson ailesi

- Orin Nano Super (8GB): Llama 3.2 3B, Phi-3'e iyi noktada uyar.
- AGX Orin: gpt-oss-20b'yi vLLM üzerinden ~40 tok/s ile çalışır.
- Thor / T4000 (JetPack 7.1): 2x AGX Orin performans, EAGLE-3 ve NVFP4 desteklenir.
- TensorRT Edge-LLM (2026) EAGLE-3 spekülatör çözümü, NVFP4 ağırlıklarını, parçalanmış prefill  edge'ye aktarılan veri merkezi optimizasyonlarını destekler.

### Hedef başına miktar seçimi

| Target | Format | Notes |
|--------|--------|-------|
| Apple ANE | INT4 weights + FP16 activations | Core ML conversion path |
| Qualcomm Hexagon | QNN INT8 / INT4 | AI Hub converters |
| WebGPU / WebLLM | Q4 MLC (q4f16_1) | Use `mlc_llm convert_weight` + compiled `.wasm`; GGUF is not supported |
| Jetson Orin Nano | Q4 GGUF or TRT-LLM INT4 | Memory-bound |
| Jetson AGX / Thor | NVFP4 + FP8 KV | Edge-LLM path |

### Uzun bağlamlı bir tuzak kenarında

> **【中文解读】**边缘设备上长上下文陷:Llama 3.1'in 128K 上下文是数据中心特性. 8GB RAM'ın cep telefonlarında,4GB 模型 + 2GB KV Cache(32K token) + 系统开销 = OOM。边缘部署 genellikle 4K-8K'de sınırlanır, ancak aktif KV 量化 kullanılırsa başka.

> **【拓展：边缘推理的隐私优势】**边缘推理在隐私敏感场景中有独特优势: 1) 医疗患者数据不离开设备; 2) 金融交易分析在本地完成; 3) 法律律师-客户通信不上传云端; 4) 军事/政府完全离线运行.

Llama 3.1'ün 128K bağlamı bir veri merkezi özelliğidir. 8 GB RAM, 4 GB model + 2 GB KV önbelleği 32K jetonları + OS overhead = OOM için bir telefonda.

### Ses , katil uygulamadır .

> **【拓展：边缘推理的应用场景】**边缘推理的杀手级应用是语音代理语音代理对延迟极度敏感(首代币 <500ms) ――本地推理完全消除网络延迟――结合语音转文字――语音结合语音语音变体在边缘运行),边缘推理成为生产质量的语音环路――其他场景包括:隐私优先医疗/金融分析、离线代码补充、实时翻译――Apple'ın "Private Cloud Compute" bir kesintisi简单任务设备端完成,杂任务在 Apple 专有云处理但承诺不存储数据――

Ses ajanları gecikme hassasıdır (birinci token < 500 ms). Yerel sonuçlama ağ gecikmesini tamamen ortadan kaldırır. Konuşma-sözle (Whisper Turbo çeşitleri kenarda çalışır) birleştirilince kenar sonuçlandırması üretim kalitesi ses döngüsü haline gelir.

### Hatırlamalısın numaralar

- Apple M4 / A18 ANE: 38 TOPS.
- Qualcomm Hexagon SD X Elite: 45 TOPS.
- WebLLM M3 Max: Llama 3.1 8B Q4'te ~41 tok/s.
- AGX Orin: ~ 40 tok/s gpt-oss-20b üzerinden vLLM.
- Veri merkezi kenarında bant genişliği boşluğu: 30-50x.
- WebGPU mobil kapsamı: ~ 70-75% (Firefox Android geride kaldı).

## Çerçeveyi kullanın.
```figure
edge-bandwidth-pipe
```

## Kullan

`code/main.py`Kısayolu hedefler üzerinden bant genişliği sınırlı matematikten teorik dekod geçiş tavanlarını hesaplar.

> `code/main.py`Genişlik sınırlı matematik hesaplamalarının her bir kenarındaki hedeflerin teorik çözümü, ölçüm ve nüfuz sınırları ile karşılaştırıldığında, genişlik üzerinde değil, hesaplama üzerinde yoğunlaşmaktadır.

## İndirin . Ürünler .

Bu ders bize çok yararlı .`outputs/skill-edge-target-picker.md`. Verilen platform (iOS/Android/browser/Jetson), model ve gecikme/hüzdedecek bütçe, bir kuantitasyon biçimi ve dönüşüm borusunu seçer.

> 本课产 出 `outputs/skill-edge-target-picker.md`△给定平台(iOS/Android/浏览器/Jetson) 模型和延迟/内存预算,选择量化格式和转换管线

## Egzersizler.

1. Çık .`code/main.py`. Snapdragon 8 Gen 3 (~ 77 GB / s bant genişliği) ile Q4'te 7B model için, dekodlama tavanını hesaplayın.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`code/main.py` hesaplama Snapdragon 8 Gen 3 ((77 GB/s 带宽)  Q4 7B 模型的解码上限──与观察到的 6-8 tok/s
2. Android'deki WebGPU, Chrome v121+ gerektiriyor. Aynı OpenAI uyumlu API üzerinden eski tarayıcılar için  sunucu tarafında bir geri dönüş tasarlayın.
   Çinçe çevirisi:Android'ın üstündeki WebGPU'yu Chrome v121+ gerektirir.
3. iOS uygulamanız 4K bağlam akışı gerektirir. Hangi model/format kombinasyonu iPhone 16'da 4 GB aktif bellek altında kalmanıza izin verir?
   Çinçe Çevirimi: iOS uygulamanız 4K'ye ihtiyaç duyar. iPhone 16'da hangi model/format kompleksi 4GB aktif bellekte kalabilir?
4. Jetson AGX Orin 40 tok/s hızıyla gpt-oss-20b çalıştırır. Jetson Nano sadece 3B'ye uyar.
   C.A.T.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.C.
5. "WebLLM 2026'da üretime hazır mı" tartışın.
   Çinçe Çevirimi:论证WebLLM 在 2026年是否生产就绪──引用覆盖率、性能和 Firefox Android 缺口──

## Anahtar Şartlar .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| ANE | "Apple neural engine" | On-device NPU in M-series and A-series; unified memory |
| Hexagon | "Qualcomm NPU" | Snapdragon NPU; QNN SDK for access |
| WebGPU | "browser GPU" | W3C-standardized browser GPU API; Chrome/Safari 2026 |
| WebLLM | "browser LLM runtime" | MLC-LLM project; Apache 2.0; OpenAI-compatible JS |
| Jetson | "NVIDIA edge" | Orin Nano / AGX / Thor / T4000 family |
| TRT Edge-LLM | "edge TensorRT" | 2026 edge port of TensorRT-LLM; EAGLE-3 + NVFP4 |
| Unified memory | "shared pool" | CPU and NPU see same RAM; no copy overhead |
| Bandwidth-bound | "memory limited" | Decode gated by bytes/sec reading weights |
| Core ML | "Apple conversion" | Apple framework for ANE-native models |
| QNN | "Qualcomm stack" | Qualcomm Neural Network SDK |

## Daha fazla okumak

- [On-Device LLMs State of the Union 2026](https://v-chandra.github.io/on-device-llms/) manzara ve referans değerleri.
- [NVIDIA Jetson Edge AI](https://developer.nvidia.com/blog/getting-started-with-edge-ai-on-nvidia-jetson-llms-vlms-and-foundation-models-for-robotics/) Orin / AGX / Thor.
- [NVIDIA TensorRT Edge-LLM](https://developer.nvidia.com/blog/accelerating-llm-and-vlm-inference-for-automotive-and-robotics-with-nvidia-tensorrt-edge-llm/)2026 kenar liman ilanı.
- [WebLLM (arXiv:2412.15803)](https://arxiv.org/html/2412.15803v2) tasarım ve referans değerleri.
- [Apple Core ML](https://developer.apple.com/documentation/coreml) ANE-devli dönüşüm.
- [Qualcomm AI Hub](https://aihub.qualcomm.com/) Hexagon için önceden dönüştürülen modeller.
