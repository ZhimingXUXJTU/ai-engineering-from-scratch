# L'inference de bord  moteur neuronal Apple, Qualcomm Hexagon, WebGPU/WebLLM, Jetson 推理 边缘 LLM GPU 欧盟

> La contrainte de bord de base est la bande passante de la mémoire, pas le calcul. La DRAM mobile est à 50 à 90 Go/s; le centre de données HBM3 élimine 2-3 TB/s  un écart de 30 à 50 fois. Le décodeur est lié à la mémoire, donc l'écart est décisif. En 2026, le paysage est divisé en quatre parties. Le moteur neural Apple M4/A18 atteint 38 TOPS avec mémoire unifiée (pas de copie CPUNPU). Qualcomm Snapdragon X Elite / 8 Gen 4 Hexagon atteint 45 TOPS. WebGPU + WebLLM exécute Llama 3.1 8B (Q4) à ~ 41 tok/s sur M3 Max (environ 70-80% de natifs); 17,6k étoiles GitHub, API compatible avec OpenAI, ~70-75% de couverture mobile. NVIDIA Jetson Orin Nano Super (8GB) est compatible avec Llama 3.2 3B / Phi-3; AGX Orin fonctionne gpt-oss-20b via vLLM à ~40 tok/s; Jetson T4000 (JetPack 7.1) est 2x AGX Orin. TensorRT Edge-LLM prend en charge EAGLE-3, NVFP4, pré-remplissage en morceaux  présenté au CES 2026 par Bosch, ThunderSoft, MediaTek.

> **【中文解读】**Ce chapitre présente les défis et les solutions du MLL déployé sur des appareils de bordure.
**Type:** Learn
**Languages:** Python (stdlib, toy bandwidth-bound decode simulator)
**Prerequisites:** Phase 17 · 04 (Serving Engine Internals), Phase 17 · 09 (Production Quantization)
**Time:** ~60 minutes


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy bandwidth-bound decode simulator) | **语言:** Python
**Prerequisites:** Phase 17 · 04 (vLLM Serving Internals), Phase 17 · 09 (Production Quantization) | **前置知识:** Phase 17 · 04 (vLLM Serving Internals), Phase 17 · 09 (Production Quantization)

>  **【前置】**Je suis en train de faire une étude sur la capacité de calcul.
>  **【类比】**边缘 vs 数据中心 = "手机 vs 超算"――手机 DRAM 50-90 GB/s, données centre HBM3 2-3 TB/s30-50 倍差,解码(内存绑定) 下决定性。2026 四大平台:Apple NE(38 TOPS 统一内存)、Qualcomm Hexagon(45 TOPS)、WebGPU+WebLLM(M3 Max 跑 Llama 3.1 8B 41 tok/s)、Jetson(Orin AGX 跑 gpt-oss-20b 40 tok/s)。TensorRT Edge-LLM 支持 EAGLE-3 + NVFP4 + chunked prefill。
**Time:** ~60 minutes | **时间:** ~60 minutes

## Objectifs d'apprentissage

- Expliquez pourquoi l'inférence mobile LLM est liée à la mémoire et à la bande passante et le calcul est secondaire.
  Expliquer pourquoi le calcul est une compétence limitée et la mémoire est une compétence limitée.
- Enumérez les quatre cibles de bord (Apple ANE, Qualcomm Hexagon, WebGPU/WebLLM, NVIDIA Jetson) et correspondrez chacune à un cas d'utilisation.
  Le nom de la société est le nom de la société de l'entreprise.
- Nombre de la lacune de couverture WebGPU 2026 (Firefox Android pour rattraper) et le débarquement Safari iOS 26.
  Le site Web de l'application est en cours de développement en 2026.
- Choisissez un format de quantification par cible (Core ML INT4 + FP16 pour ANE, QNN INT8/INT4 pour Hexagon, WebGPU Q4 pour navigateur, NVFP4 pour Jetson Thor).
  Pour chaque objectif, sélectionnez la taille du format: [EN] Utilisez le Core ML INT4 + FP16, l'héxagon Utilisez le QNN INT8/INT4, le navigateur Utilisez le WebGPU Q4, le Jetson Thor Utilisez le NVFP4)

## Le problème , l' introduction du problème

> **【中文解读】**La limite centrale de la logique de bord est la capacité de calcul et non la capacité de bande passante de 50 à 90 Go/s. Le DRAM mobile est de 50 à 90 Go/s. Le centre de données HBM3 atteint 2-3 TB/s.30 à 50 X. La différence est décisive.

> **【拓展：边缘 AI 芯片市场】**Le système de gestion de la technologie numérique (SNAPDRACON X Elite / 8 Gen 4) est un logiciel de gestion de la technologie numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique numérique num

Un client veut un chatbot sur un appareil: voix-première, privé par défaut, fonctionne hors ligne. Sur un MacBook Pro M3 Max, Llama 3.1 8B Q4 fonctionne à ~55 tok/s  fine. Sur un iPhone 16 Pro, le même modèle fonctionne à 3 tok/s  non bien. Sur un Android de milieu de gamme avec Snapdragon 8 Gen 3, 7 tok/s. Dans le navigateur via WebGPU sur Chrome Android v121+, 4-8 tok/s selon l'appareil.

La variance de débit n'est pas un problème de port. C'est l'écart de bande passante fois le format de quantification fois si le NPU est accessible depuis l'espace utilisateur.

## Le concept de base.

### La bande passante est le vrai plafond

> **【中文解读】**边缘推理的真正天花板是内存带宽――Decode 阶段每生成一个代币 需要读取全部权重――7B Q4 模型 3.5GB,在50GB/s 带宽下读取需要70ms理论上限约14 tok/s――在90GB/s(高端移动DRAM) 下上限升至约25 tok/s――数据中心 HBM3在不同3TB/s读取同一模型只需1.2ms上限830 tok/s――同样模型 下同权重、内存子系统――

Le décode lit l'ensemble complet des poids pour chaque jeton. Un modèle 7B dans le Q4 est de 3,5 Go. La lecture de 3,5 Go à 50 Go / s prend 70 ms  un plafond théorique de ~ 14 Tok / s. À 90 Go / s (DRAM mobile haut de gamme) le plafond se déplace à ~ 25 Tok / s. Aucune quantité de calcul ne permet de dépasser ce nombre.

Le centre de données HBM3 à 3 TB/s nettoie les mêmes 3,5 GB en 1,2 ms  le plafond est de 830 tok/s. Le même modèle, les mêmes poids.

### Moteur neuronal d'Apple (M4 / A18)

- Jusqu'à 38 TOPS. mémoire unifiée (CPU et ANE partagent le même pool)  Aucun coût de copie.
- Accès par le système de base ML + `.mlmodel`modèles compilés, ou par des métal-shaders (MPS) par PyTorch.
- Llama.cpp Metal backend utilise MPS, pas ANE directement; ANE natif nécessite la conversion de Core ML.
- Le meilleur chemin pratique pour les applications iOS en 2026: ML de base avec des poids INT4 + activations FP16.

### Qualcomm Hexagon (Snapdragon X Elite / 8 Gen 4)

- Intégré avec le processeur et la GPU dans le SoC mais séparé domaine de mémoire.
- Le SDK QNN (Qualcomm Neural Network) et l'AI Hub fournissent la conversion à partir de PyTorch/ONNX.
- Les modèles de chat, Llama 3.2, Phi-3 sont tous envoyés comme des objets de première classe sur l'AI Hub.

### Les NPU Intel / AMD (Lunar Lake, Ryzen AI 300)

- 40-50 TOPS. Le logiciel est en retard sur Apple/Qualcomm; OpenVINO s'améliore mais est un niche.
- Meilleur pour les applications de copilote ARM Windows; natif sur les ordinateurs de bureau AMD/Intel pour la première fois locale.

### L'utilisation de l'appareil

> **【中文解读】**Le WebGPU + WebLLM est un logiciel de recherche en ligne qui est disponible en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en ligne en

- Exécuter des modèles dans le navigateur via des shaders de calcul WebGPU; aucune installation.
- Llama 3.1 8B Q4 à ~41 tok/s sur M3 Max  environ 70-80% de natifs via le même backend.
- 17,6k GitHub étoiles sur WebLLM; API JS compatible avec OpenAI; Apache 2.0.
- Couverture 2026: Chrome Android v121+, Safari iOS 26 GA, Firefox Android toujours à la traîne. Couverture mobile globale ~ 70-75%.

### La famille Jetson

- Orin Nano Super (8 Go): s'adapte à Llama 3.2 3B, Phi-3 à bon taux de partage.
- AGX Orin: fonctionne gpt-oss-20b via vLLM à ~40 tok/s.
- Thor / T4000 (JetPack 7.1): 2x de performance AGX Orin, EAGLE-3 et NVFP4 pris en charge.
- TensorRT Edge-LLM (2026) prend en charge le décoding spéculatif EAGLE-3, les poids NVFP4, le pré-remplissage en morceaux  les optimisations du centre de données portées à bord.

### Choix de quantification par cible

| Target | Format | Notes |
|--------|--------|-------|
| Apple ANE | INT4 weights + FP16 activations | Core ML conversion path |
| Qualcomm Hexagon | QNN INT8 / INT4 | AI Hub converters |
| WebGPU / WebLLM | Q4 MLC (q4f16_1) | Use `mlc_llm convert_weight` + compiled `.wasm`; GGUF is not supported |
| Jetson Orin Nano | Q4 GGUF or TRT-LLM INT4 | Memory-bound |
| Jetson AGX / Thor | NVFP4 + FP8 KV | Edge-LLM path |

### Le piège du long contexte sur le bord

> **【中文解读】**Le système de distribution est généralement limité à 4K-8K, sauf en utilisant une quantité KV activée.

> **【拓展：边缘推理的隐私优势】**La logique de la confidentialité présente des avantages uniques: 1) les données des patients ne quittent pas les appareils; 2) l'analyse des transactions financières est effectuée sur place; 3) la loi et les services de communication client ne sont pas transmis sur le cloud; 4) la fonctionnement en ligne et entièrement hors ligne de l'armée et du gouvernement.

Le contexte 128K de Llama 3.1 est une fonctionnalité de centre de données. Sur un téléphone avec 8 Go de RAM, modèle 4 Go + 2 Go de cache KV pour les jetons 32 Go + OS overhead = OOM. Les déploiements Edge gardent le contexte à 4 K-8 Go à moins que la quantification KV agressive (Q4 KV) ne soit acceptée.

### La voix est l'application tueur

> **【拓展：边缘推理的应用场景】**边缘推理的杀手级应用是语音代理语音代理对延迟极度敏感(首代币 < 500ms) ――本地推理完全消除网络延迟――结合语音转文字(Whisper Turbo 变体在边缘运行),边缘推理成为生产质量的语音环路――其他场景包括:隐私优先医疗/金融分析、离线代码补充、实时翻译――Apple's "Private Cloud Compute" est une détente de simple tâche terminée, complexe tâche à effectuer chez Apple 专业云处理但承诺不存储数据――

Les agents vocaux sont sensibles à la latence (premier jeton < 500 ms). L'inférence locale élimine complètement la latence du réseau.

### Les chiffres que vous devriez vous rappeler

- Apple M4 / A18 ANE: 38 survols.
- Qualcomm Hexagon SD X Elite: 45 TOPS.
- WebLLM M3 Max: ~41 tocs/s sur Llama 3.1 8B Q4.
- AGX Orin: ~ 40 tok/s sur gpt-oss-20b par vLLM.
- L'écart de bande passante entre le centre de données et le bord: 30 à 50 fois.
- Couverture mobile WebGPU: ~ 70-75% (décalage de Firefox Android).

## Utilisez-le avec le cadre de réalisation
```figure
edge-bandwidth-pipe
```

## Utilisez-le

`code/main.py`Comparé aux points de référence observés et aux points marqués où la bande passante, et non le calcul, est le goulot d'étranglement.

> `code/main.py`En ce qui concerne la largeur limitée, le calcul des objectifs de chaque côté du calcul des théories de résolution du débit de la limite.

## Envoyez-le . Produit .

Cette leçon produit `outputs/skill-edge-target-picker.md`. En fonction de la plateforme (iOS/Android/browser/Jetson), du modèle et du budget de latence/mémoire, choisit un format de quantification et un pipeline de conversion.

> 本课产 出 `outputs/skill-edge-target-picker.md` donner une plateforme de mise à jour (iOS/Android/Browser/Jetson)  modèle et retard/budget de stockage, sélectionnement de format et de transformation de la ligne de stockage.

## Les exercices

1. On court .`code/main.py`Pour un modèle 7B au Q4 sur un Snapdragon 8 Gen 3 (~77 Go/s de bande passante), calculer le plafond de décode.
   Le mot " l' économie " est traduit par " l' économie ".`code/main.py` calculer Snapdragon 8 Gen 3 ((environ 77 Go/s 带宽) sur Q4 7B 模型的解码上限──与观察到的 6-8 tok/s
2. Le WebGPU sur Android nécessite Chrome v121+. Concevoir un back-up pour les navigateurs plus anciens  côté serveur via la même API OpenAI compatible.
   Le système d'exploitation WebGPU d'Android a besoin de Chrome v121+.
3. Votre application iOS a besoin de streaming de contexte 4K. Quelle combinaison de modèle/format vous permet de rester sous 4 Go de mémoire active sur un iPhone 16 ?
   Quel type de modèle/configuration peut être conservé dans l'iPhone 16 en 4 Go de mémoire active ?
4. Jetson AGX Orin fonctionne gpt-oss-20b à 40 tok/s. Jetson Nano ne correspond qu'à un 3B. Si votre produit cible les deux, comment unifier la pile d'inférence?
   Je ne peux pas faire de commande de 3B. Si vos produits sont ciblés simultanément, comment pouvez-vous les utiliser ?
5. Débattrez si "WebLLM est prêt à la production en 2026". Citez la couverture, les performances et le fossé entre Firefox et Android.
   Le projet WebLLM est en cours de production en 2026.

## Les termes clés

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

## Encore une lecture

- [On-Device LLMs State of the Union 2026](https://v-chandra.github.io/on-device-llms/) paysage et critères de référence.
- [NVIDIA Jetson Edge AI](https://developer.nvidia.com/blog/getting-started-with-edge-ai-on-nvidia-jetson-llms-vlms-and-foundation-models-for-robotics/) Orin / AGX / Thor.
- [NVIDIA TensorRT Edge-LLM](https://developer.nvidia.com/blog/accelerating-llm-and-vlm-inference-for-automotive-and-robotics-with-nvidia-tensorrt-edge-llm/) Annonce de port de bord de 2026.
- [WebLLM (arXiv:2412.15803)](https://arxiv.org/html/2412.15803v2) conception et critères de référence.
- [Apple Core ML](https://developer.apple.com/documentation/coreml) Conversion en ANE-native.
- [Qualcomm AI Hub](https://aihub.qualcomm.com/) Modèles préconvertis pour Hexagon.
