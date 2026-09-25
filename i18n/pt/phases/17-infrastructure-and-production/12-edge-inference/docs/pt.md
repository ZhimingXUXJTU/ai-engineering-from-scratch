# Edge Inference  Apple Neural Engine, Qualcomm Hexagon, WebGPU/WebLLM, Jetson 推理 边缘 LLM GPU 欧盟

> A restrição de borda do núcleo é a largura de banda da memória, não o computação. A DRAM móvel fica a 50-90 GB/s; o datacenter HBM3 limpa 2-3 TB/s  uma lacuna de 30-50x. A decodificação é limitada à memória, por isso a lacuna é decisiva. Em 2026, a paisagem divide-se em quatro partes. O Apple M4/A18 Neural Engine chega a 38 TOPS com memória unificada (sem cópia CPUNPU). Qualcomm Snapdragon X Elite / 8 Gen 4 Hexagon chega a 45 TOPS. WebGPU + WebLLM executa Llama 3.1 8B (Q4) a ~ 41 tok/s no M3 Max (cerca de 70-80% nativo); 17,6k estrelas GitHub, API compatível com OpenAI, ~ 70-75% cobertura móvel. NVIDIA Jetson Orin Nano Super (8GB) combina com Llama 3.2 3B / Phi-3; AGX Orin corre gpt-oss-20b via vLLM a ~ 40 tok/s; Jetson T4000 (JetPack 7.1) é 2x AGX Orin. TensorRT Edge-LLM suporta EAGLE-3, NVFP4, preenchimento em pedaços mostrado no CES 2026 pela Bosch, ThunderSoft, MediaTek.

> **【中文解读】**Esta secção apresenta os desafios e soluções do LLM em implementação em dispositivos de margem.
**Type:** Learn
**Languages:** Python (stdlib, toy bandwidth-bound decode simulator)
**Prerequisites:** Phase 17 · 04 (Serving Engine Internals), Phase 17 · 09 (Production Quantization)
**Time:** ~60 minutes


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy bandwidth-bound decode simulator) | **语言:** Python
**Prerequisites:** Phase 17 · 04 (vLLM Serving Internals), Phase 17 · 09 (Production Quantization) | **前置知识:** Phase 17 · 04 (vLLM Serving Internals), Phase 17 · 09 (Production Quantization)

> - Não .**【前置】**Há um período de tempo de tempo de transição entre os dois grupos de dados.
> - Não .**【类比】**边缘 vs 数据中心 = "手机 vs 超算"――手机 DRAM 50-90 GB/s, datacenter HBM3 2-3 TB/s30-50 倍差,解码(内存绑定) 下决定性。2026 四大平台:Apple NE(38 TOPS 统一内存)、Qualcomm Hexagon(45 TOPS)、WebGPU+WebLLM(M3 Max 跑 Llama 3.1 8B 41 tok/s)、Jetson(Orin AGX 跑 gpt-oss-20b 40 tok/s)。TensorRT Edge-LLM 支持 EAGLE-3 + NVFP4 + chunked prefill。
**Time:** ~60 minutes | **时间:** ~60 minutes

## Objetivos de aprendizagem

- Explique porque a inferência de LLM móvel é limitada à largura de banda de memória e a computação é secundária.
  Tradução do inglês para tradução do inglês: Explain why moving LLM 推理 is in-memory带宽有限, while computing ability is secondary.
- Enumere os quatro alvos de borda (Apple ANE, Qualcomm Hexagon, WebGPU/WebLLM, NVIDIA Jetson) e ajuste cada um a um caso de uso.
  Chinese: 列举四个边缘目标 (果 ANE, Qualcomm Hexagon, WebGPU, WebLLM, NVIDIA Jetson)并匹配每个用例,
- Nomear a lacuna de cobertura WebGPU 2026 (Firefox Android alcançando) e o Safari iOS 26 pouso.
  No entanto, o que não é o que eu quero dizer é que o que eu quero dizer é que eu quero que você me diga que eu quero que você me diga que eu quero que você me diga que eu quero que você me diga que eu quero que eu me diga que eu quero que você me diga que eu me diga que eu quero que você me diga que eu me diga que eu quero que eu me diga que eu me diga que eu sou um homem.
- Escolha um formato de quantização por alvo (Core ML INT4 + FP16 para ANE, QNN INT8/INT4 para Hexagon, WebGPU Q4 para navegador, NVFP4 para Jetson Thor).
  Por exemplo, o sistema de controle de dados de um computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de computador de comput

## O problema é o problema da introdução

> **【中文解读】**O limite central da lógica de margem é a capacidade de memória e não de cálculo. O DRAM móvel é de 50-90 GB/s, o centro de dados HBM3 é de 2-3 TB/s30-50x. A diferença é decisiva.

> **【拓展：边缘 AI 芯片市场】**2026 ano margem AI 芯片的竞争格局:(1) Apple Neural Engine (M4/A18) 38 TOPS,统一内存架构,无需CPUNPU 数据拷贝;(2) Qualcomm Hexagon (Snapdragon X Elite / 8 Gen 4) 45 TOPS,QNN SDK 提供转换链路;(3) Intel Lunar Lake / AMD Ryzen AI 30040-50 TOPS, software生态落后于 Apple/Qualcomm;((4) NVIDIA Jetson Orin/Thor边缘 GPU 方案,支持vLLM 和 TensorRT Edge-LLM──语音代理是边缘推杀手级应用本地推理完全消除网络延迟──

Um cliente quer um chatbot no dispositivo: voz-primeira, privada por padrão, funciona offline. Em um MacBook Pro M3 Max, Llama 3.1 8B Q4 funciona a ~55 tok/s  bem. Em um iPhone 16 Pro, o mesmo modelo funciona a 3 tok/s  não bem. Em um Android de gama média com Snapdragon 8 Gen 3, 7 tok/s. No navegador através de WebGPU no Chrome Android v121+, 4-8 tok/s dependendo do dispositivo.

A variação de throughput não é um problema de porting. É a diferença de largura de banda vezes o formato de quantização vezes se o NPU é acessível a partir do espaço do usuário.

## O conceito central.

### O largura de banda é o verdadeiro teto

> **【中文解读】**边缘推理的真正天花板是内存带宽――Decode 阶段每生成一个代币 需要读取全部权重――7B Q4 模型 3.5GB,在 50 GB/s 带宽下读取需要 70ms理论上限约14 tok/s――在 90 GB/s(高端移动DRAM) 下上限升至约25 tok/s――数据中心 HBM3在不同 3 TB/s读取同一模型只需1.2ms上限830 tok/s――同样模型 下同权重、内存子系统――

O decode lê o conjunto completo de pesos para cada token. Um modelo 7B no Q4 é de 3,5 GB. Ler 3,5 GB a 50 GB / s leva 70 ms  um limite teórico de ~ 14 tok / s. A 90 GB / s (high-end DRAM móvel) o limite se move para ~ 25 tok / s. Nenhuma quantidade de computação ajuda abaixo deste número.

Datacenter HBM3 a 3 TB/s limpa o mesmo 3,5 GB em 1,2 ms  teto é 830 tok/s. O mesmo modelo, os mesmos pesos.

### Motor Neural da Apple (M4 / A18)

- Até 38 TOPS. Memória unificada (CPU e ANE compartilham o mesmo pool)  sem custo superior de cópia.
- Acesso através do Core ML + `.mlmodel`Modelos compilados, ou através de Shaders de desempenho de metal (MPS) através de PyTorch.
- Llama.cpp Metal backend usa MPS, não ANE diretamente; ANE nativo requer conversão Core ML.
- Melhor caminho prático para aplicativos iOS em 2026: Core ML com pesos INT4 + ativações FP16.

### Qualcomm Hexagon (Snapdragon X Elite / 8 Gen 4)

- Integra com CPU e GPU no SoC, mas com domínio de memória separado.
- QNN (Qualcomm Neural Network) SDK e AI Hub fornecem conversão a partir de PyTorch / ONNX.
- Modelos de chat, Llama 3.2, Phi-3 todos enviados como artefatos de primeira classe no AI Hub.

### Intel / AMD NPUs (Lunar Lake, Ryzen AI 300)

- O software está atrasado pela Apple/Qualcomm; o OpenVINO está melhorando, mas é um nicho.
- Melhor para aplicativos de copiloto ARM do Windows; nativo em desktops AMD/Intel para local-primeiro.

### WebGPU + WebLLM

> **【中文解读】**WebGPU + WebLLM é um programa de análise de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software

- Execute modelos no navegador através de shaders de computação WebGPU; nenhuma instalação.
- Llama 3.1 8B Q4 a ~ 41 tok/s em M3 Max  aproximadamente 70-80% nativo através do mesmo backend.
- 17,6k GitHub estrelas em WebLLM; OpenAI-compatível JS API; Apache 2.0.
- 2026 cobertura: Chrome Android v121+, Safari iOS 26 GA, Firefox Android ainda alcançando.

### NVIDIA Família Jetson

- Orin Nano Super (8GB): combina com Llama 3.2 3B, Phi-3 a bons tok/s.
- AGX Orin: corre gpt-oss-20b via vLLM a ~ 40 tok/s.
- Thor / T4000 (JetPack 7.1): 2x desempenho AGX Orin, EAGLE-3 e NVFP4 suportados.
- TensorRT Edge-LLM (2026) suporta a decodificação especulativa EAGLE-3, pesos NVFP4, preenchimento em pedaços  as otimizações do datacenter portadas para a borda.

### A escolha de quantificação por alvo

| Target | Format | Notes |
|--------|--------|-------|
| Apple ANE | INT4 weights + FP16 activations | Core ML conversion path |
| Qualcomm Hexagon | QNN INT8 / INT4 | AI Hub converters |
| WebGPU / WebLLM | Q4 MLC (q4f16_1) | Use `mlc_llm convert_weight` + compiled `.wasm`; GGUF is not supported |
| Jetson Orin Nano | Q4 GGUF or TRT-LLM INT4 | Memory-bound |
| Jetson AGX / Thor | NVFP4 + FP8 KV | Edge-LLM path |

### A armadilha de longo contexto está a ponta

> **【中文解读】**边缘设备上长上下文陷:Llama 3.1 de 128K 上下文是数据中心特性. Em 8GB RAM, 4GB 模型 + 2GB KV Cache (tokoens 32K) + sistema开销 = OOM.

> **【拓展：边缘推理的隐私优势】**边缘推理在隐私敏感场景有独特优势: 1) 医疗患者数据不离开设备; 2) 金融交易分析在本地完成; 3) 法律律师-客户通信不上传云端; 4) 军事/政府完全离线运行.

O contexto 128K do Llama 3.1 é um recurso do datacenter. Em um telefone com 8 GB de RAM, modelo de 4 GB + 2 GB de cache KV para tokens 32K + OS overhead = OOM. As implementações de Edge mantêm o contexto em 4K-8K a menos que a quantização KV agressiva (Q4 KV) seja aceita.

### A voz é o aplicativo assassino

> **【拓展：边缘推理的应用场景】**边缘推理的杀手级应用是语音代理语音代理对延迟极度敏感(首代币 < 500ms) ――本地推理完全消除网络延迟――结合语音转文字(Whisper Turbo 变体在边缘运行),边缘推理成为生产质量的语音环路――其他场景包括:隐私优先医疗/金融分析、离线代码补充、实时翻译――Apple's"Private Cloud Compute" é uma forma de descontinuar o simples computador de missões, complexo de missões na Apple 专用云处理但承诺不存储数据――

Os agentes de voz são sensíveis à latência (primeiro token < 500 ms). A inferência local elimina completamente a latência da rede. Combinado com fala-a-texto (variantes de Whisper Turbo executadas em borda) e inferência de borda se torna o loop de voz de qualidade de produção.

### Números que você deve lembrar

- Apple M4 / A18 ANE: 38 TOPS.
- Qualcomm Hexagon SD X Elite: 45 TOPS.
- WebLLM M3 Max: ~ 41 tok/s no Llama 3.1 8B Q4.
- AGX Orin: ~ 40 tok/s em gpt-oss-20b via vLLM.
- O espaço de largura de banda do datacenter é de 30 a 50 vezes maior.
- Cobertura móvel WebGPU: ~ 70-75% (Lacagem do Firefox Android).

## Use-o com o framework implementado.
```figure
edge-bandwidth-pipe
```

## Usá-lo

`code/main.py`Comparar com benchmarks observados e destaques onde a largura de banda, não a computação, é o gargalo de engarrafamento.

> `code/main.py`A partir da banda larga limitada matemática de cálculo de todos os objetivos de bordas de teoria de solução de código de transmissão de limite. Comparado com a observação de base, enfatizar o teorema de banda larga e não de cálculo.

## Envia-o . Produto .

Esta lição produz`outputs/skill-edge-target-picker.md`. Dada a plataforma (iOS/Android/browser/Jetson), modelo e orçamento de latência/memória, escolhe um formato de quantização e um pipeline de conversão.

> 本课产 出 `outputs/skill-edge-target-picker.md` fornecer uma plataforma de desenvolvimento de sistemas operativos (iOS/Android/Jetson)  modelos e atrasos/presença de armazenamento, opções de armazenamento e de transferência de dados

## Exercícios.

1. Corra .`code/main.py`Para um modelo 7B no Q4 em um Snapdragon 8 Gen 3 (~ 77 GB / s largura de banda), calcular o teto de decodificação. Comparar com 6-8 tok / s observados  é o tempo de execução eficiente?
   Tradução: 运行`code/main.py` calcular Snapdragon 8 Gen 3 ((cerca de 77 GB/s 带宽) no Q4 7B 模型的解码上限──与观察到的 6-8 tok/s比较运行时是否高效?
2. WebGPU no Android requer Chrome v121+. Projeto de um fallback para navegadores mais antigos  lado do servidor através da mesma API compatível com OpenAI.
   O Android 需要 Chrome v121+── para o antigo navegador design 返回方案通过相同的 OpenAI 兼容 API 实现服务端推理──
3. O seu aplicativo iOS precisa de streaming de conteúdo 4K. Que combinação de modelo/formato permite que você fique com menos de 4 GB de memória ativa em um iPhone 16?
   Chinese Translation: Seu aplicativo iOS precisa de 4K.
4. Jetson AGX Orin executa gpt-oss-20b a 40 tok/s. Jetson Nano cabe apenas a 3B. Se o seu produto alveja ambos, como você unificar a pilha de inferência?
   Por exemplo, a empresa Jetson AGX Orin tem 40 tok/s 运行 gpt-oss-20b。Jetson Nano apenas pode operar 3B 模型。
5. Argumente se "WebLLM está pronto para produção em 2026". Cite a cobertura, desempenho e a lacuna do Firefox Android.
   O desenvolvimento de um sistema operacional de segurança e segurança em dispositivos móveis e dispositivos móveis em uso em todo o mundo.

## Termos-chave .

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

## Mais leitura 延伸阅读

- [On-Device LLMs State of the Union 2026](https://v-chandra.github.io/on-device-llms/) paisagem e referências.
- [NVIDIA Jetson Edge AI](https://developer.nvidia.com/blog/getting-started-with-edge-ai-on-nvidia-jetson-llms-vlms-and-foundation-models-for-robotics/)Orin / AGX / Thor.
- [NVIDIA TensorRT Edge-LLM](https://developer.nvidia.com/blog/accelerating-llm-and-vlm-inference-for-automotive-and-robotics-with-nvidia-tensorrt-edge-llm/) Anúncio de portos de bordo de 2026.
- [WebLLM (arXiv:2412.15803)](https://arxiv.org/html/2412.15803v2) design e valores de referência.
- [Apple Core ML](https://developer.apple.com/documentation/coreml) Conversion nativa.
- [Qualcomm AI Hub](https://aihub.qualcomm.com/) Modelos pré-convertidos para Hexagon.
