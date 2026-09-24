# LLaVA-OneVision: imagen única, imagen múltiple, video en un modelo

> Antes de LLaVA-OneVision (Li et al., agosto 2024) el mundo de VLM abierto tenía linajes separados: LLaVA-1.5 para imágenes individuales, modelos de imágenes múltiples como Mantis y VILA, modelos de video como Video-LLaVA y Video-LLaMA. Cada uno ganó su punto de referencia y falló en los otros. LLaVA-OneVision argumentó que un solo plan de estudios podría capacitar a un modelo para dominar los tres escenarios, y que los efectos emergentes de transferencia de tareas (habilidades de imagen única exportadas al video, razonamiento de imágenes múltiples exportados a imagen única) superan a la suma de especialistas. La receta es engañosamente simple: un presupuesto de fichaje visual que se mantiene constante en todos los escenarios, además de un plan de estudios explícito que pasa de una sola imagen a OneVision (multi-imagen) a video. Esta lección lee el presupuesto, el programa de estudios y los comportamientos emergentes.

> **【中文解读】**La contribución central de LLaVA-OneVision: con un token visual unificado  presupuesto                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         

> **【拓展：统一多模态模型的产业价值】**En los productos reales, el usuario puede subir simultáneamente imágenes, imágenes y vídeos.

**Type:** Build  | **类型：构建**
**Languages:** Python (stdlib, token budget solver + curriculum planner)  | **语言：Python（标准库，token预算求解器 + 课程规划器）**
**Prerequisites:** Phase 12 · 05 (LLaVA), Phase 12 · 06 (any-resolution)  | **前置：阶段12第05课（LLaVA）、阶段12第06课（任意分辨率）**
**Time:** ~180 minutes  | **时长：约180分钟**

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 12·05(LLaVA 投影器) 、Fase 12·06(AnyRes/NaFlex 分辨率调度) 、Fase 11·07(Curriculum Learning 课程学习) ⋅本节是LLaVA 系列的集大成一个模型干三件事──
> ¿ Qué es esto ?**【类比】**LLaVA-OneVision = "Old power Swiss Army Knife"―Otros VLM = 专门的单功能刀单图刀、多图刀、视频刀)― Swiss Army Knife cada uno de sus funciones no es como un especialista, pero puede hacer frente a un escenario desconocido; mantenimiento de un token único 预算3000-4000)= 子和刀片的总长度恒定, dependiendo del escenario de la función principal―

## Objetivos de aprendizaje

- Diseñar un presupuesto de tokens visuales que mantenga constante en entradas de una sola imagen, múltiples imágenes y videos.
- Ordenar un plan de entrenamiento que transfiera habilidades de una sola imagen al video sin olvidar catastróficamente.
- Explica por qué un modelo único supera a los especialistas en el mismo parámetro de conteo cuando el plan de estudios se hace correctamente.
- Nombre de las tres capacidades emergentes reportadas por LLaVA-OneVision: razonamiento multi-cámara, set-of-mark, agente de capturas de pantalla del iPhone.

## El problema es el contexto del problema

La imagen, la imagen múltiple y el video enfatizan cada modelo de manera diferente.

Una sola imagen necesita tokens de alta resolución (AnyRes, ~ 2880 tokens visuales) para capturar OCR y detalles finos. Presupuesto por muestra: una imagen, 2880 tokens.

Multi-imagen quiere varias imágenes con resolución moderada (~ 576 tokens cada uno) por lo que el razonamiento entre las imágenes encaja en el contexto. Presupuesto por muestra: 4-8 imágenes, 576 cada, 2300-4600 tokens.

El video necesita muchos cuadros con baja resolución (~ 196 tokens por cuadro después de la agrupación) para capturar la dinámica temporal. Presupuesto por muestra: 8-32 cuadros, 196 cada, 1600-6200 tokens.

> **【中文解读】**Tres escenarios para el token  Presupuesto de necesidades diferentes: un solo gráfico con alta resolución (~2880 tokens), un gráfico con media resolución (~576 tokens), un video con baja resolución (~196 tokens) ⋅ El reto es: Cómo cumplir con un presupuesto fijo al mismo tiempo con tres escenarios.

Si entrenas modelos separados, escoges un presupuesto. Si entrenas un modelo, necesitas el presupuesto para escalar sensatamente entre escenarios sin explotar el contexto.

Pre-OneVision, la respuesta predeterminada era "entrenar un escenario, ignorar los otros". Video-LLaVA adaptó el video a un modelo de imagen con etapas de entrenamiento adicionales. LLaVA-NeXT agregó soporte para múltiples imágenes con mosaicos. Ninguno manejó las tres limpiamente.

## El concepto central.

### El presupuesto de los tokens de OneVision.

LLaVA-OneVision elige un presupuesto unificado de tokens visuales de aproximadamente 3000-4000 tokens por muestra, asignados de manera diferente por escenario:

- Una sola imagen / 单图: AnyRes-9 (3x3 azulejos + miniatura), cada azulejo en 384 con 729 parches, bilinear agresivo de 2x2 → 182 por azulejo. Total: 9 * 182 + 182 = 1820 tokens.
- Multi-imagen / 多图: cada imagen en resolución moderada (384, sin azulejos), 729 tokens sin pooling. Presupuesto 6 imágenes → 4374 tokens.
- Video / 视频: 32 cuadros con 384 resoluciones con un pool bilinear agresivo 3x3 → 81 tokens por cuadro.

La asignación mantiene tokens totales aproximadamente constantes. El LLM nunca ve un lote que sopla su contexto. El codificador produce una geometría diferente por escenario, pero el LLM consume el mismo presupuesto.

> **【中文解读】**核心思想:总代币 预算保持恒定(约3000-4000), pero el modo de distribución es diferente en función de la escena.

### El plan de estudios de tres etapas.

Los trenes LLaVA-OneVision se dividen en tres etapas:

1. Una sola imagen SFT (estadio SI) / 单图指令微调. Todos los datos son una sola imagen más texto. Entrenamiento en entrada de alta resolución AnyRes. Esto enseña la percepción, OCR y la comprensión de granos finos. Utiliza datos LLaVA-NeXT más datos de una imagen específica de OneVision.
2. OneVision SFT (estadio OV) / 统一指令微调. Mezcla una imagen + una imagen + un video (marcos de muestra uniforme). Entrena en el presupuesto de token unificado. Esto enseña al modelo a manejar formas de lotes heterogéneas.
3. Transferencia de tareas (fase TT) / 任务迁移. Continúa con una mezcla de tareas objetivo, generalmente más pesada en imágenes o videos múltiples dependiendo del producto. Opcional para la implementación.

El programa de formación de video-primero o de imágenes múltiples-primero produce un rendimiento de imagen peor que de imagen única-primero, incluso con los mismos datos.

> ️ **【易错点】**Se autoentrenó a la vez en VLM 时课程顺序搞反了(先训视频再训单图)→ 单图性能大幅下降──原因:视频低分辨率输入让模型先学到"模糊是正常的",再训高分辨率单图时模型适应不过来──修复:必须单图 → 多图 → 视频的顺序,先学精细再学粗──
> ¿ Qué es esto ?**【困惑】**P: ¿Por qué es tan importante el presupuesto fijo? Porque la ventana de la LLM es fija, la única imagen de repente ocupa 5000 tokens、 vídeo 10000 tokens, destruirá el lote y el presupuesto de cálculo── presupuesto fijo = costo de cálculo predecible, es la clave de la implementación de productos──

> **【中文解读】** secuencia de curso es esencial: primero un dibujo, luego un dibujo + vídeo, luego una misión se desplaza. Si primero se entrenan videos o más dibujos, el rendimiento de los dibujos se reduce. Esto se debe a que el entrenamiento de los dibujos uniformes establece la base de la percepción, y la secuencia y el espacio de los videos se necesitan basar en esto.

### ¿Por qué el plan de estudios funciona ?

La formación de una sola imagen construye la base perceptiva. Los tokens de parche tienen características visuales de granos finos; el LLM aprende a integrarlas con el texto.

Si entrenamos todos los escenarios desde cero juntos, el modelo se adapta a la percepción (datos de una sola imagen por lote limitado) y a la estructura de sobrepeso (muchos datos de imágenes / videos múltiples).

El orden del currículo le da fuerza de percepción desde la etapa SI, luego el razonamiento compositivo/temporal desde la etapa OV, sin perder ninguna.

> **【中文解读】**Si al mismo tiempo se entrenan todos los escenarios, el modelo se quedará sin capacidad de percepción adecuada (con un gran número de imágenes/vidéos), lo que puede llevar a que el modelo pueda hacer una teoría transversal, pero la comprensión visual sea escasa.

### Habilidades emergentes de escenario transversal

El documento LLaVA-OneVision informa de tres capacidades emergentes:

1. El modelo integra correctamente las vistas a pesar de que nunca vio ese formato exacto en el entrenamiento.
2. Instrucción de marcas de conjunto / 标记提示. El usuario anota objetos en una imagen con marcas numeradas; el modelo razona sobre "qué hace la marca 3 en relación con la marca 7." Entrenado ni en marcas ni en anotaciones; aprendido a partir de la combinación de tierra espacial + referencia de imagen múltiple.
3. El usuario proporciona una captura de pantalla de una pantalla del iPhone y le pide que planifique el siguiente clic.

Estas no son tareas formadas; surgen de la estructura de composición del plan de estudios.

> **【拓展：涌现能力的工程启示】**涌现能力 significa que el valor del modelo unificado supera los diferentes expertos. La capacidad de razonamiento de varias cámaras puede ser utilizada para la seguridad de control, la conducción automática; la señal de señal puede ser utilizada para la marca de imágenes; el agente de la interceptación puede ser utilizado para la prueba de automatización de la interfaz de usuario.

### Comunización de tokens visuales

El presupuesto de tokens requiere un pooling. OneVision utiliza interpolación bilinear en la red de parches 2D: 24x24 = 576 parches se convierte en 12x12 = 144 (2x factor) o 8x8 = 64 (3x factor).

La elección de un factor de agrupación por escenario es en sí misma un hiperparámetro. Menos agrupación = más tokens = representación más rica.

> **【中文解读】**池化在2D 补丁网格空间进行(而不是 token 空间), para conservar el espacio local性──池化因子是每个场景的超参数:少池化=更多 token=更丰富表示;多池化=更少 token=可容纳更多/图像──

### LLaVA-OneVision-1.5

El seguimiento de 2025 (LLaVA-OneVision-1.5, arXiv 2509.23661) es "totalmente abierto" en datos de capacitación, pesos de modelos y código.

### Contraste con Qwen2.5VL en comparación con Qwen2.5VL

Qwen2.5-VL (Lección 12.09) hace diferentes opciones. Utiliza M-RoPE y FPS dinámico en lugar de un pooling fijo. Su balance de presupuesto con entrada  un video de 1 minuto utiliza más tokens que un video de 5 segundos. LLaVA-OneVision fija el presupuesto y escala el pooling. Ambos trabajan; intercambian configurabilidad por predictibilidad.

> **【中文解读】**Qwen2.5VL utiliza M-RoPE y el índice de movimiento,token  presupuesto con la entrada y la reducción;LLaVA-OneVision  presupuesto fijo 调整池化── dos estrategias tienen sus ventajas: las primeras son fáciles de calcular pero el coste es imprevisible, las últimas son controlables pero pueden perderse o quedar en desventaja──
```figure
l5-onevision-budget
```

## Usalo

## Usalo en práctica.

`code/main.py`Se trata de un plan de estudios y un planificador de presupuesto para un VLM de estilo OneVision.

- Alocar resolución, factor de agrupación y marcos por escenario.
- Verifica que cada escenario encaja dentro del presupuesto compartido.
- Informes del número de tokens esperados, los FLOPs de LLM, y qué escenarios están sub-tokenizados.
- Imprime un programa de entrenamiento paso a paso.

## Envíalo .

Esta lección produce`outputs/skill-onevision-budget-planner.md`. Dado una distribución de tareas objetivo y un presupuesto por muestra, emite el factor AnyRes, el conjunto por fotograma, el recuento de fotogramas de vídeo y los pesos de las etapas del currículo.

> **【中文解读】**Este curso se produce en OneVision  presupuesto de planificación de herramientas.

## Los ejercicios.

1. Su producto admite el 80% de imágenes individuales, el 10% de imágenes múltiples (2-4 imágenes), el 10% de vídeo (8-16 cuadros). Diseñe el presupuesto de token. ¿Dónde pondría el presupuesto adicional que ahorra sin hacer imágenes múltiples pesadas?
   | 产品支持 80% 单图、10% 多图（2-4张）、10% 视频（8-16帧）。设计 token 预算。从轻量多图中省下的预算放在哪？

2. Leer la sección 4.3 de LLaVA-OneVision (capacidades emergentes). Proponer una cuarta habilidad emergente que el plan de estudios probablemente desbloquearía pero el documento no informó.
   | 阅读 LLaVA-OneVision 第 4.3 节（涌现能力）。提出课程学习可能解锁但论文未报告的第四种涌现技能。

3. Cambiar el orden del currículo  tren de imágenes múltiples primero, luego de imágenes únicas, luego de video.
   | 交换课程顺序——先多图，再单图，最后视频。预测哪些基准会下降以及原因。

4. El artículo informa de los puntos de referencia de vídeo entrenados en sólo 8 cuadros por muestra. ¿Se generaliza eso a videos de 30 segundos en la inferencia? ¿Qué rompe primero  el presupuesto de token o el razonamiento temporal?
   | 论文报告视频基准只用每样本8帧训练。这对推理时的30秒视频泛化吗？先崩溃的是 token 预算还是时序推理？

5. La combinación bilinear de parches 24x24 a 12x12 es una reducción de 4x por dim. Implemente la combinación en stdlib Python y verifique que la media sobre cada bloque 2x2 coincida con la salida bilinear.
   | 将 24x24 补丁双线性池化为 12x12 是每维 4 倍缩减。用标准库 Python 实现池化，验证每个 2x2 块的均值与双线性输出一致。

## Términos clave .

| Term | What people say | What it actually means | 中文含义 | 中文释义 |
|------|-----------------|------------------------|----------|---------|
| OneVision scenario | "Single-image, multi-image, or video" | One of three input shapes the unified VLM handles; the budget stays constant across | 统一 VLM 处理的三种输入形态之一，预算在场景间保持恒定 | |
| Token budget | "How many tokens per sample" | Total visual tokens the LLM sees per training / inference sample, typically 3000-4000 | LLM 每样本看到的总视觉 token 数，通常 3000-4000 | |
| Curriculum | "Training order" | Stage ordering (single-image → multi-image → video) chosen for emergent transfer | 课程学习：按单图→多图→视频顺序训练，促进技能迁移 | |
| Bilinear pooling | "Token shrink" | Applying bilinear interpolation to the patch grid (2D) to reduce token count while preserving locality | 在补丁网格上做双线性插值，减少 token 数并保留空间局部性 | |
| Emergent skill | "Not trained, still works" | Capability that appears at inference without matching training data, due to curriculum composition | 课程学习组合带来的未训练即涌现的能力 | |
| AnyRes-k | "k-tile setup" | k sub-tiles of fixed resolution plus one thumbnail, typical k ∈ {4, 9} | k 个固定分辨率子切片加一个缩略图 | |
| Task transfer | "Cross-scenario generalization" | Skills learned on single-image that apply to video (and vice versa) via shared backbone | 通过共享骨干网络，单图技能迁移到视频（反之亦然） | |

## Más Leer más Leer más

- [Li et al. — LLaVA-OneVision (arXiv:2408.03326)](https://arxiv.org/abs/2408.03326)♬ Lava-OneVision original artículo
- [LLaVA-OneVision-1.5: Fully Open Framework (arXiv:2509.23661)](https://arxiv.org/abs/2509.23661)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
- [Lin et al. — Video-LLaVA (arXiv:2311.10122)](https://arxiv.org/abs/2311.10122)♬ Video-LLAVA                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       
- [Lin et al. — VILA (arXiv:2312.07533)](https://arxiv.org/abs/2312.07533)¿Qué es esto?
- [Wang et al. — Qwen2-VL (arXiv:2409.12191)](https://arxiv.org/abs/2409.12191) Qwen2-VL en comparación con Referencia
