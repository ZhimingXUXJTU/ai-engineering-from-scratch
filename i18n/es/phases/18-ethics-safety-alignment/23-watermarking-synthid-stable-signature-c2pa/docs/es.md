# Marca de agua  SynthID, firma estable, C2PA 稳定签名 水印 SynthID C2PA

> Tres tecnologías estructuran 2026 procedencia de contenido generado por IA. SynthID (Google DeepMind)  marcado de agua de imágenes lanzado en agosto de 2023, texto + video mayo de 2024 (Gemini + Veo), texto de código abierto octubre de 2024 a través de Responsible GenAI Toolkit, detector multimedia unificado noviembre de 2025 junto con Gemini 3 Pro. El marcado de agua de texto ajusta las probabilidades de muestreo de los tokens siguientes de manera imperceptible; las marcas de agua de imagen / video sobreviven a la compresión, recorte, filtros, cambios en la velocidad de fotogramas. Firma estable (Fernandez et al., ICCV 2023, arXiv:2303.15435)  sintoniza el decodificador de difusión latente para que cada salida contenga un mensaje fijo; las imágenes recortadas (10% del contenido) generadas detectadas >90% en FPR<1e-6. Seguimiento "La firma estable es inestable" (arXiv:2405.07145, mayo 2024)  ajuste fino elimina la marca de agua mientras se conserva la calidad. C2PA  estándar de metadatos firmado criptográficamente, que es evidente que se han manipulado (C2PA 2.2 Explicador 2025). El marcado de agua y el C2PA son complementarios: los metadatos pueden ser eliminados pero tienen una procedencia más rica; las marcas de agua persisten a través del transcodificación pero llevan menos información.

> **【中文解读】**Este capítulo presenta la tecnología de impresión de agua de IA SynthID、C2PA等 Identificación de contenido de IA SynthID(Google DeepMind) ajuste el siguiente token 采样概率 hace que la generación contenga más "verdes" de las señales Invisible pero verificable。Stable Signature 微调潜在扩散解码器 hace que cada salida contenga mensajes fijos de forma secundaria。C2PA es un código de cifrado Custom de cambios en los valores de datos 

> **【拓展：水印 → Deepfake 检测】**El agua se puede leer de texto, imágenes, sonidos y videos. Pero la limitación es evidente: el modelo específico (no tiene sinthid) no es igual a la verdad) no se puede resistir a la liberación (no se puede eliminar) de la información.

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, token-watermark embed + detect) | **语言:** Python（标准库，token 水印嵌入 + 检测）
**Prerequisites:** Phase 10 · 04 (sampling), Phase 01 · 09 (information theory) | **前置知识:** Phase 10 · 04 (采样), Phase 01 · 09 (信息论)
**Time:** ~75 minutes | **时间:** ~75 分钟

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 10·04(采样) 、Fase 01·09(信息论) ∼三大水印技术 + 内容追溯标准。
> ¿ Qué es esto ?**【类比】**水印 = "AI 内容的隐形身份证"──SynthID(Google) = 调整下面的代码采样偏好"绿色"代码,不可察知但可检测;Stable Signature = 微调解码器让每张图都含固定二进制消息(剪裁 10% 仍 >90% 检出);C2PA = 加密签名元数据──互补:元数据可剥取但信息丰富;水抗印转码但信息少──
> ️ "Signatura estable no está estable"2024.5:

## Objetivos de aprendizaje

- Describa el marcado de agua a nivel de token (estilo de texto SynthID) y el mecanismo por el cual se puede detectar.
- Describa la firma estable y el ataque de eliminación de 2024 que la rompió.
- El papel del C2PA estatal y por qué es complementario al marcado acuático.
- Describa las limitaciones clave: señal específica del modelo, robustez bajo parafraza y ataques que preservan el significado (arXiv:2508.20228).

> 描述令牌级水印(SynthID-text 风格) y su mecanismo de detección──描述 Stable Signature 和 2024 Year破坏 its removal attack──说明 C2PA's role as well as why it interacts with waterprint──描述关键局限性:模型特定信号、释义下鲁棒性和意义保持攻击──

## El problema es el problema .

2023-2024 vio que las falsificaciones profundas y el contenido generado por IA entraron en contextos políticos y de consumo a escala. El Watermarking es la señal de procedencia técnica propuesta: marcar generaciones en el momento de la creación, detectarlas más tarde. Prueba de 2025: ninguna marca de agua es incondicionalmente robusta, pero en capas con metadatos C2PA la combinación proporciona una historia de procedencia utilizable.

> 2023-2024 años de falsificación profunda y AI Produce contenido en gran escala en el escenario político y de consumo.

## El concepto.

> **【中文解读】**文本水印机(Kirchenbauer 等人 2023, by Google 产品化): cada paso de código se producirá un falso "verde" y "rojo" en la sección de los logitos de la palabra, hacia los logitos de color verde 添加 delta 偏置采样――生成包含比随机更多的绿色令牌──检测:重新哈希每前,计量生成中的绿色令牌,计算 z 分数──水印文本 z > 0,人类文本 z ~ 0──

### Marcación de agua de texto (estilo de texto SynthID)

El mecanismo de Kirchenbauer et al. 2023, producido por Google:

1. En cada paso de decodificación, hash los tokens K anteriores para producir una partición pseudorandomaria del vocabulario en conjuntos "verde" y "rojo".
2. Muestreo de sesgos hacia el conjunto verde añadiendo δ a los logitos verdes.
3. La generación contiene más tokens verdes de lo que producirían los hechos.

Detección: replantear cada prefijo, contar los tokens verdes en la generación, calcular un z-score. El z-score es >0 para texto marcado por agua, ~0 para texto humano.

Propiedades:
- Inperceptible para los lectores (δ es lo suficientemente pequeño como para que la pérdida de calidad sea menor).
- Detectable con acceso a la función de partición de vocabulario.
- No es robusto para parafrasear. Reescribir el texto destruye la señal.

SynthID-text es de código abierto en octubre de 2024 a través del Toolkit GenAI Responsable de Google.

> **【中文解读】**Firmas estables (Fernandez 等人, ICCV 2023) Micro调潜在扩散解码器使每个生成图像包含固定二进制消息──剪切到原始内容10%的图像在 FPR<1e-6 下检测率>90%──但2024 年 5 月"Stable Signature is Unstable"证明微调解码器可以在保持图像质量同时移除水印对抗性生成后微调成本低──

### Firma estable (imagen)

Fernandez et al. ICCV 2023. Fine-tune el decodificador de difusión latente para que cada imagen generada contenga un mensaje binario fijo incrustado en la representación latente. La detección se decodifica desde el latente con un decodificador neuronal.

> Firma estable 微调潜在扩散解码器 hace que cada imagen generada contenga mensajes fijos de segunda forma.

mayo 2024 "La firma estable es inestable" (arXiv:2405.07145): ajuste fino del decodificador elimina la marca de agua mientras se conserva la calidad de la imagen.

> 2024 5 月 "La firma estable es inestable" prueba que el micro-modulación de código puede mantener la calidad de la imagen al mismo tiempo que se elimina el agua de la impresión.

### Detector unificado SynthID (novembre 2025)

Junto con Gemini 3 Pro: un detector multimedia que lee señales SynthID de texto, imagen, audio y video en una API. Unifica la pila de procedencia de Google.

> 伴随 Gemini 3 Pro: un transmodelo tester, puede leerse en texto, imágenes, audio y vídeo en SynthID 信号──统一 Google Source技术──

> **【拓展：C2PA + 水印互补 → EU AI Act Article 50】**C2PA y agua imprenta: datos de la UE se pueden extraer pero con una cadena de fuentes abundante; agua imprenta mediante la transferencia de código persistente pero con una pequeña cantidad de bits. Google integra dos de ellos en búsqueda, publicidad y "sobre esta imagen".

### C2PA

Coalición para la procedencia y autenticidad del contenido. estándar de metadatos de prueba de manipulación firmado criptográficamente. C2PA 2.2 Explicador (2025).

> C2PA es un código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código de código

Complementario de la marca de agua:
- Los metadatos pueden ser despojados; las marcas de agua no pueden ser (fácilmente).
- Los metadatos son ricos (cadena de procedencia completa); las marcas de agua llevan bits.
- C2PA depende de la adopción de la plataforma; las marcas de agua se incorporan automáticamente.

> Consiguiendo una nueva versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la versión de la

Google integra tanto en la búsqueda, anuncios, y "Acerca de esta imagen".

> Google se ha integrado en la búsqueda, la publicidad y la "Acerca de esta imagen".

> **【拓展：水印局限性 → 模型特定信号问题】**关键局限性:SynthID 水印仅来自启用SynthID的模型──"无SynthID 信号"不等于真实性证明未启用SynthID的模型生成的任何内容都不会有水印──此外,arXiv:2508.20228(2025) demostró el significado de mantener el ataque puede destruir al mismo tiempo el texto de la impresión y las diversas imágenes de la impresión de agua──

### Las limitaciones

- **Model-specific.**Una generación de un modelo sin SynthID no está marcada por agua, por lo que "ningún señal SynthID" no es prueba de autenticidad.
- **Paraphrase.**Las marcas de agua del texto no sobreviven a la paráfrase que preserva el significado.
- **Transformation attacks.**arXiv:2508.20228 (2025) muestra ataques de preservación del significado que destruyen tanto las marcas de agua de texto como muchas marcas de agua de imagen.
- **Fine-tune removal.**Por "Signature stable is unstable", el ajuste fino de post-generación elimina las marcas de agua incrustadas.

### Artículo 50 de la Ley de IA de la UE

Código de transparencia para el etiquetado de contenidos generados por IA (primer proyecto de diciembre de 2025, segundo proyecto de marzo de 2026, previsto final de junio de 2026 por el año)[European Commission status page](https://digital-strategy.ec.europa.eu/en/policies/code-practice-ai-generated-content)El código permanece en redacción a partir de abril de 2026 y el calendario está sujeto a cambios. La capa regulatoria que requiere la capa técnica.

### Donde esto encaja en la Fase 18

Las lecciones 22-23 se refieren a lo que emite el modelo (datos privados, señal de procedencia). La lección 27 abarca la gobernanza de los datos de formación. La lección 24 es el marco regulatorio que requiere estas medidas técnicas.

> Lecciones 22-23  Sobre el modelo de emisión de datos privados  Source signal)  Lección 27   Cubriendo el entrenamiento en gestión de datos  Lección 24  Requiere un marco de supervisión de estas medidas técnicas 

## Usalo.
```figure
an-watermark-greenlist
```

## Usalo

`code/main.py`construye una marca de agua de texto de juguete. Las fichas son números enteros 0..N-1; los parámetros de muestreo marcados con agua hacia el conjunto verde definido por hash. Un detector calcula el puntaje z del token verde. Puedes observar la detección en generaciones de 1000 fichas, ver la paráfrase destruir la señal y medir la tasa de falsos positivos en el texto humano.

> `code/main.py`构建玩具文本水印──令牌是整数 0.N-1;水印采样偏向哈希定义的绿色集──检测器计算绿色令牌 z 分数── puedes observar 1000 令牌生成的检测、释义破坏信号以及人类文本上的误报率──

## Envíalo .

Esta lección produce`outputs/skill-provenance-audit.md`. Dado que se ha implementado un contenido con una declaración de procedencia, se realiza una auditoría: el mecanismo de marca de agua (si lo hay), la cadena de firma de la C2PA (si lo hay), la robustez adversaria de cada uno y la cobertura por modalidad.

> 本课产 出  `outputs/skill-provenance-audit.md` Encargar los contenidos de las declaraciones de origen determinado, auditoría: mecanismo de impresión del agua, cadena de firmas de la C2PA, su propia resistencia a la contaminación y su cobertura de cada tipo de información.

## Los ejercicios.

1. - ¿ Qué ?`code/main.py`.Informe los resultados z para la generación de 1000 tokens con marca de agua frente al texto escrito por el hombre.Identifique la tasa de falsos positivos en el umbral de confianza del 95%.

2. Implemente un ataque parafrase que reemplace el 30% de los tokens con sinónimos.

3. Leer Kirchenbauer et al. 2023 Sección 6 sobre robustez. ¿Por qué las marcas de agua de texto fallan bajo la paráfrasis pero las marcas de agua de imagen sobreviven al recortar?

4. Diseñar una implementación que utilice SynthID-text + C2PA metadatos. Describir la cadena de procedencia que un consumidor ve. Identificar un modo de falla de cada componente.

5. El resultado de 2024 "Signature stable is unstable" muestra que el ajuste fino elimina la marca de agua de la imagen. Diseñar un control de despliegue que limite este ataque  por ejemplo, requiere liberaciones firmadas de puntos de control ajustados.

## Términos clave .

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| SynthID | "Google's watermark" | Cross-modal provenance signal; text, image, audio, video |
| Token watermark | "Kirchenbauer-style" | Biased-sampling text watermark detectable via green-token z-score |
| Stable Signature | "image watermark" | Fine-tuned-decoder watermark; ICCV 2023 |
| C2PA | "the metadata standard" | Cryptographically signed tamper-evident provenance metadata |
| Paraphrase robustness | "does rewording break it" | Text watermark property; currently limited |
| Fine-tune removal | "adversarial unwatermark" | Attack that removes image watermark via decoder fine-tuning |
| Cross-modal detector | "unified SynthID" | November 2025 unified API across modalities |

## Más Leer más Leer más

- [Kirchenbauer et al. — A Watermark for Large Language Models (ICML 2023, arXiv:2301.10226)](https://arxiv.org/abs/2301.10226) el mecanismo de marcas de agua de los tokens
- [Fernandez et al. — Stable Signature (ICCV 2023, arXiv:2303.15435)](https://arxiv.org/abs/2303.15435) papel de marcas de agua de imagen
- ["Stable Signature is Unstable" (arXiv:2405.07145)](https://arxiv.org/abs/2405.07145) el ataque de eliminación
- [Google DeepMind — SynthID](https://deepmind.google/models/synthid/) la marca de agua transmódica
- [C2PA 2.2 Explainer (2025)](https://c2pa.org/specifications/specifications/2.2/explainer/Explainer.html) Norma de metadatos
