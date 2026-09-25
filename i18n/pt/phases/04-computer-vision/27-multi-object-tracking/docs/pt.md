# Multi-Object Tracking & Video Memory  Multi-Objecto Tracking e memória de vídeo

> Detectar cada quadro, combinar as detecções deste quadro com as pistas do último quadro por identificação.

> **【中文解读】**Seguir = 检测 + 关联── cada 检测目标, em seguida, irá os resultados do atual 检测与上一的跟踪轨迹通过 ID 匹配──多目标跟踪(MOT) é a técnica central do vídeo entendimento, precisa de lidar com a ocultação, desaparecimento, reaparição e outras situações complexas──

> **【拓展：MOT 的应用】**Dois objetivos de acompanhamento em segurança ([[ByteTrack]], [[SORT]]/DeepSORT]] é um método clássico.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 4 Lesson 06 (YOLO Detection), Phase 4 Lesson 08 (Mask R-CNN), Phase 4 Lesson 24 (SAM 3) | **前置知识:** Phase 4 Lesson 06（YOLO 检测），Phase 4 Lesson 08（Mask R-CNN），Phase 4 Lesson 24（SAM 3）
**Time:** ~60 minutes | **时间:** ~60 分钟

## Objetivos de aprendizagem

- Distinguir o rastreamento por detecção do rastreamento baseado em consulta e nomear as famílias de algoritmos (SORT, DeepSORT, ByteTrack, BoT-SORT, SAM 2 tracker de memória, SAM 3.1 Object Multiplex)
- Implementar a missão IoU + Hungria desde zero para o rastreamento por detecção clássico
- Explique o banco de memória do SAM 2 e por que trata melhor a oclusão do que a associação baseada em IoU
- Leia as três métricas de rastreamento (MOTA, IDF1, HOTA) e escolha qual delas é importante para um determinado caso de uso

> **【中文解读】**O objetivo do aprendizado é listar as capacidades centrais que devem ser adquiridas após a conclusão do curso.


## O problema é o problema da introdução

Um detector diz-lhe onde os objetos estão num único quadro.`t`é o mesmo objeto que uma detecção em quadro `t-1`Sem isso, não se pode contar objetos que atravessam uma linha, seguir uma bola através de uma oclusão, ou saber "o carro #4 está na faixa há 8 segundos".

> O testeiro diz-te a posição do objeto no solo. O rastreador diz-te a posição.`t`中哪个检测与第 `t-1`Se não houver, não se pode calcular o número de objetos que atravessam a linha, ou saber que o carro número 4 já está nesta estrada há 8 segundos.

O rastreamento é essencial para todos os produtos que se encontram em vias de vídeo: análise esportiva, vigilância, condução autônoma, análise de vídeo médico, monitoramento da vida selvagem, contagem de marcas. Os blocos de construção principais são compartilhados: um detector por quadro, um modelo de movimento (filtro Kalman ou algo mais rico), um passo de associação (algoritmo húngaro sobre IoU / cosino / características aprendidas) e um ciclo de vida da pista (nascimento, atualização, morte).

> Seguir para cada produto em cada fase de vídeo são essenciais: análise de esportes, controle, auto-condução, análise de vídeo médico, monitoramento de animais selvagens, marcação comercial.

O ano 2026 trouxe dois novos padrões: **SAM 2 memory-based tracking**(factor-memory em vez de associação de modelo de movimento) e **SAM 3.1 Object Multiplex**Esta lição segue a pilha clássica primeiro, depois a abordagem baseada na memória.

> O ano 2026 traz dois novos modelos:**SAM 2 基于记忆的跟踪**(特征记忆替代运动模型关联) e **SAM 3.1 Object Multiplex**(Multiple examples of the same concept sharing memory) ∼ 本课先走经典,然后走基于记忆的方法──

## O conceito central.

> **【中文解读】**Este capítulo apresenta os conceitos e teorias fundamentais.


### Seguimento por detecção

```mermaid
flowchart LR
    F1["Frame t"] --> DET["Detector"] --> D1["Detections at t"]
    PREV["Tracks up to t-1"] --> PREDICT["Motion predict<br/>(Kalman)"]
    PREDICT --> PRED["Predicted tracks at t"]
    D1 --> ASSOC["Hungarian assignment<br/>(IoU / cosine / motion)"]
    PRED --> ASSOC
    ASSOC --> UPDATE["Update matched tracks"]
    ASSOC --> NEW["Birth new tracks"]
    ASSOC --> DEAD["Age unmatched tracks; delete after N"]
    UPDATE --> NEXT["Tracks at t"]
    NEW --> NEXT
    DEAD --> NEXT

    style DET fill:#dbeafe,stroke:#2563eb
    style ASSOC fill:#fef3c7,stroke:#d97706
    style NEXT fill:#dcfce7,stroke:#16a34a
```

Cada rastreador que encontraremos em 2026 é uma variação deste ciclo.

> Cada rastreador que encontrar em 2026 é uma variação deste ciclo.

- **SORT**(2016): Filtro Kalman + IoU húngaro. Modelo simples, rápido, sem aparência.
  Tradução:**SORT**(2016):Karlmann 波器 + IoU 匈牙利算法──简单、快速、无外观模型──
- **DeepSORT**(2017): SORT + um recurso de aparência baseado na CNN por faixa (embedding ReID).
  Tradução:**DeepSORT**(2017):SORT + Cada trajeto de CNN 外观特征(ReID 嵌入)
- **ByteTrack**(2021): associa as detecções de baixa confiança como uma segunda fase; não são necessárias características de aparência, mas o melhor desempenho no MOT17.
  Tradução:**ByteTrack**(2021):将低信度检测作为第二阶段关联; não necessária característica externa, mas melhor desempenho no MOT17
- **BoT-SORT**(2022): Byte + compensação de movimento da câmera + ReID.
  Tradução:**BoT-SORT**(2022):Byte + 相机运动补偿 + ReID。
- **StrongSORT / OC-SORT**Descendentes de ByteTrack com melhor movimento e aparência.
  Tradução:**StrongSORT / OC-SORT**ByteTrack 后代,改进了运动和外观模型──

### Filtro de Kalman num parágrafo

Um filtro Kalman mantém um estado por trilha .`(x, y, w, h, dx, dy, dw, dh)`com uma covariância.**predict**O estado usando um modelo de velocidade constante, então **update**A atualização confía mais na detecção quando a incerteza de previsão é alta. Isto dá trajetórias suaves e a capacidade de continuar uma pista através de uma oclusão curta (1-5 quadros).

> O Carman é um aparelho que mantém cada trajeto.`(x, y, w, h, dx, dy, dw, dh)`和协方差──每先用恒速模型**预测**status, reutilizar correspondentes de inspecção**更新**△ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △                                                                         

Todos os rastreadores clássicos usam um filtro Kalman no passo de previsão de movimento.

> Cada rastreador clássico usa o "Carlman" em cada fase do movimento.

### O algoritmo húngaro

Dado um `M x N`A partir da data de execução, a matriz de custos (tracks x detections), encontrar a atribuição individual que minimiza o custo total.`1 - IoU(track_bbox, detection_bbox)`O tempo de execução é O(((M+N) ^3); para M, N até ~1000 é rápido o suficiente em Python via `scipy.optimize.linear_sum_assignment`- Não .

> - Não .`M x N`de preços em linha ([[轨迹 x 检测]]), encontrar a minimização total do preço de um par de uma distribuição.`1 - IoU(轨迹框, 检测框)`Ou exterioridade das características de um só campo de observação.`scipy.optimize.linear_sum_assignment`- É muito rápido.

### A ideia chave do ByteTrack

Os rastreadores padrão deixam de detectar detecções de baixa confiança (< 0, 5).**second-stage candidates**A partir de agora, a rede de dados da rede de dados da rede de dados da rede de dados da rede de dados da rede de dados da rede de dados da rede de dados da rede de dados da rede de dados da rede de dados da rede de dados da rede de dados da rede de dados da rede de dados da rede de dados da rede de dados da rede de dados da rede de dados da rede de dados da rede de dados da rede de dados da rede de dados da rede de dados da rede de dados da rede de dados da rede de dados da rede de dados da rede de dados da rede de dados da rede de dados da rede de dados da rede de dados da rede de dados da rede de dados da rede de dados da rede de dados da rede de dados da rede de dados da rede de dados da rede de dados da rede de dados da rede de dados da rede de dados da rede de dados da rede de dados da rede de dados da rede de dados da rede de dados da rede de dados da rede de dados da rede de dados da rede de dados da rede de dados da rede de dados da rede de dados da rede de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de

> 标准跟踪器丢弃低置信度检测(< 0.5)。ByteTrack irá mantê-los para**第二阶段候选**A partir de agora, o sistema de verificação de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados de dados

### SAM 2 rastreamento baseado em memória

SAM 2 lida com vídeo mantendo um **memory bank**Em um quadro, um prompt (clique, caixa, texto) codifica a instância na memória. Em quadros subsequentes, a memória é atendida contra as características do novo quadro, e o decodificador produz uma máscara para a mesma instância no novo quadro.

Não há filtro Kalman, não há tarefa húngara, a associação está implícita na operação de atenção-memória.

Pros:
- Robusto para grandes oclusões (memória carrega identidade de instância em muitos quadros).
- Vocabulário aberto quando combinado com as instruções de texto do SAM 3.
- Funciona sem um modelo de movimento separado.

Cons:
- Mais lento do que o ByteTrack para rastrear muitos objetos.
- O banco de memória cresce; limita a janela de contexto.

### SAM 3.1 Objeto Multiplex

O rastreamento anterior SAM 2 / SAM 3 mantém um banco de memória separado por instância. Para 50 objetos, 50 bancos de memória. Object Multiplex (março 2026) os colapsou em uma memória compartilhada com **per-instance query tokens**- As escalas de custos sublineares em número de casos.

O Multiplex é o novo padrão para o seguimento da multidão em 2026: multidões de concertos, trabalhadores de armazém, interseções de trânsito.

### Três métricas a saber

- **MOTA (Multi-Object Tracking Accuracy)** 1 - (FN + FP + ID switches) / GT. Pesado por tipo de erro; uma única métrica que confunde falhas de detecção e associação.
  Tradução:**MOTA（多目标跟踪精度）**1 - (FN + FP + ID 切换) / GT──按错误类型加权;将检测和关联失败混混的单一标标──
- **IDF1 (ID F1)** média harmonica de precisão e recall de ID. Focaliza especificamente em como cada trilha de verdade de terra mantém a sua ID ao longo do tempo.
  Tradução:**IDF1（ID F1）**Id 精度率和召回率调和平均――专注衡量每个真实轨迹随时间保持 ID 的一致性――对 ID 切换敏感任务优于MOTA――
- **HOTA (Higher Order Tracking Accuracy)** se decompõe em precisão de detecção (DetA) e precisão de associação (AssA).
  Tradução:**HOTA（高阶跟踪精度）**分解为检测精度(DetA) 和关联精度(AssA) ・2020年以来的社区标准;最全面──

Para vigilância (quem é quem): IDF1 é o que você relata. Para análise esportiva (passos de contagem): HOTA. Para comparação acadêmica geral: HOTA.

> 监控(谁是谁): relatório IDF1──运动分析(计数传球):HOTA──一般学术比较:HOTA──

> **【拓展：工业部署中的视觉系统】**No implementar industrial real, o modelo visual precisa considerar a possibilidade de atrasos, modelos de tamanho, dispositivos de margem, etc. TensorRT, ONNX Runtime, OpenVINO são ferramentas de aceleração de cálculo de uso comum.

> **【拓展：数据标注与质量】** Visual task's effect highly depends on label data quality──Label Studio、CVAT is the mainstream marking tool──In industrial scenarios, proactive learning(Active Learning) pode reduzir o custo de marcação: modelo contra um pedido de amostra não definido marcação artificial, identidade de amostra auto-marcação──



## Construí-lo e realizei-o.

> **【中文解读】**Este é um método de "desde zero" que ajuda a entender o princípio da estrutura, não é um problema que se encontra em uma caixa negra.

```figure
cv3-track-assoc
```

## Construí-lo

### Passo 1: Matriz de custos baseada em UIO

```python
import numpy as np


def bbox_iou(a, b):
    """
    a, b: (N, 4) arrays of [x1, y1, x2, y2].
    Returns (N_a, N_b) IoU matrix.
    """
    ax1, ay1, ax2, ay2 = a[:, 0], a[:, 1], a[:, 2], a[:, 3]
    bx1, by1, bx2, by2 = b[:, 0], b[:, 1], b[:, 2], b[:, 3]
    inter_x1 = np.maximum(ax1[:, None], bx1[None, :])
    inter_y1 = np.maximum(ay1[:, None], by1[None, :])
    inter_x2 = np.minimum(ax2[:, None], bx2[None, :])
    inter_y2 = np.minimum(ay2[:, None], by2[None, :])
    inter = np.clip(inter_x2 - inter_x1, 0, None) * np.clip(inter_y2 - inter_y1, 0, None)
    area_a = (ax2 - ax1) * (ay2 - ay1)
    area_b = (bx2 - bx1) * (by2 - by1)
    union = area_a[:, None] + area_b[None, :] - inter
    return inter / np.clip(union, 1e-8, None)
```

### Passo 2: Tracker de estilo SORT mínimo

Calman constante-velocidade fixa omitido para brevidade  utilizamos uma associação simples IoU aqui; na produção a previsão Kalman é essencial.`sort`O pacote Python fornece a versão completa.

```python
from scipy.optimize import linear_sum_assignment


class Track:
    def __init__(self, tid, bbox, frame):
        self.id = tid
        self.bbox = bbox
        self.last_frame = frame
        self.hits = 1

    def update(self, bbox, frame):
        self.bbox = bbox
        self.last_frame = frame
        self.hits += 1


class SimpleTracker:
    def __init__(self, iou_threshold=0.3, max_age=5):
        self.tracks = []
        self.next_id = 1
        self.iou_threshold = iou_threshold
        self.max_age = max_age

    def step(self, detections, frame):
        if not self.tracks:
            for d in detections:
                self.tracks.append(Track(self.next_id, d, frame))
                self.next_id += 1
            return [(t.id, t.bbox) for t in self.tracks]

        track_boxes = np.array([t.bbox for t in self.tracks])
        det_boxes = np.array(detections) if len(detections) else np.empty((0, 4))

        iou = bbox_iou(track_boxes, det_boxes) if len(det_boxes) else np.zeros((len(track_boxes), 0))
        cost = 1 - iou
        cost[iou < self.iou_threshold] = 1e6

        matched_track = set()
        matched_det = set()
        if cost.size > 0:
            row, col = linear_sum_assignment(cost)
            for r, c in zip(row, col):
                if cost[r, c] < 1.0:
                    self.tracks[r].update(det_boxes[c], frame)
                    matched_track.add(r); matched_det.add(c)

        for i, d in enumerate(det_boxes):
            if i not in matched_det:
                self.tracks.append(Track(self.next_id, d, frame))
                self.next_id += 1

        self.tracks = [t for t in self.tracks if frame - t.last_frame <= self.max_age]
        return [(t.id, t.bbox) for t in self.tracks]
```

60 linhas. Tome detecções por quadro, retorna IDs de pista por quadro. Sistemas reais adicionam a previsão de Kalman, a re-match do segundo estágio do ByteTrack e recursos de aparência.

### Passo 3: Teste de trajetória sintética

```python
def synthetic_frames(num_frames=20, num_objects=3, H=240, W=320, seed=0):
    rng = np.random.default_rng(seed)
    starts = rng.uniform(20, 200, size=(num_objects, 2))
    velocities = rng.uniform(-5, 5, size=(num_objects, 2))
    frames = []
    for f in range(num_frames):
        dets = []
        for i in range(num_objects):
            cx, cy = starts[i] + f * velocities[i]
            dets.append([cx - 10, cy - 10, cx + 10, cy + 10])
        frames.append(dets)
    return frames


tracker = SimpleTracker()
for f, dets in enumerate(synthetic_frames()):
    tracks = tracker.step(dets, f)
```

Três objetos que se movem em linhas retas devem manter os seus identificadores em todos os 20 quadros.

### Passo 4: Metrica de interruptor de identificação

```python
def count_id_switches(tracks_per_frame, gt_per_frame):
    """
    tracks_per_frame:  list of list of (track_id, bbox)
    gt_per_frame:      list of list of (gt_id, bbox)
    Returns number of ID switches.
    """
    prev_assignment = {}
    switches = 0
    for tracks, gts in zip(tracks_per_frame, gt_per_frame):
        if not tracks or not gts:
            continue
        t_boxes = np.array([b for _, b in tracks])
        g_boxes = np.array([b for _, b in gts])
        iou = bbox_iou(g_boxes, t_boxes)
        for g_idx, (gt_id, _) in enumerate(gts):
            j = iou[g_idx].argmax()
            if iou[g_idx, j] > 0.5:
                t_id = tracks[j][0]
                if gt_id in prev_assignment and prev_assignment[gt_id] != t_id:
                    switches += 1
                prev_assignment[gt_id] = t_id
    return switches
```

Esta é uma métrica simplificada IDF1 adjacente: contar quantas vezes um objeto de verdade de terra muda sua identificação de pista prevista atribuída.`py-motmetrics`E ...`TrackEval`- Não .

> **【中文解读】**Este capítulo mostra como usar um framework maduro (como PyTorch、HuggingFace etc) rápida aplicação desta tecnologia.





> **【拓展：视觉模型的持续学习】**Em um ambiente de produção, o modelo visual precisa se adaptar constantemente a novos dados. Isto é especialmente importante na condução automática e no controle de qualidade industrial.

## Use-o com o framework implementado.

Traqueadores de produção em 2026:

- `ultralytics` YOLOv8 + ByteTrack / BoT-SORT incorporado. `results = model.track(source, tracker="bytetrack.yaml")`- O padrão.
- `supervision`(Roboflow)  Envolvedores ByteTrack mais utilitários de anotação.
- SAM 2 / SAM 3.1  rastreamento baseado em memória via `processor.track()`- Não .
- Estaca personalizada: detector (YOLOv8 / RT-DETR) + `sort-tracker`- Não .`OC-SORT`- Não .`StrongSORT`- Não .

- A escolha:

- Pedestres / carros / caixas a 30+ fps: **ByteTrack with ultralytics**- Não .
- Muitas instâncias de uma classe numa multidão:**SAM 3.1 Object Multiplex**- Não .
- Oclusões pesadas com aparência identificável: **DeepSORT / StrongSORT**(Figurações de ReID).
- Esportes / interações complexas: **BoT-SORT**ou rastreadores aprendidos (MOTRv3).

> **【中文解读】**Este capítulo se concentra em como o modelo será implantado como produto disponível. De modelo original a nível de produção, os sistemas precisam considerar várias dimensões de otimização de desempenho, tratamento de erros, controle, etc.




## Envia-o . Produto .

> **【中文解读】**Practicação de temas de fácil/médio/difícil  3o dificuldade de passagem  Recomendação de completar pelo menos Praça de nível médio Classe difícil  Adaptação a pesquisa profunda ou preparação para o encontro 


Esta lição produz:

- `outputs/prompt-tracker-picker.md` escolhe SORT / ByteTrack / BoT-SORT / SAM 2 / SAM 3.1 dado tipo de cena, padrões de oclusão e orçamento de latência.
- `outputs/skill-mot-evaluator.md` escreve um arnes completo de avaliação para MOTA / IDF1 / HOTA contra trilhas de verdade no solo.

## Exercícios.

1. **(Easy)**Execute o rastreador sintético acima com 3, 10 e 30 objetos. Relate a contagem de interruptores de ID em cada caso. Identifique onde a associação simples apenas com IoU começa a falhar.
2. **(Medium)**Adicione um passo de previsão de Kalman de velocidade constante antes da associação. Mostre que as oclusões curtas (2-3 quadros) não causam mais interruptores de ID.
3. **(Hard)**Integrar o rastreador baseado em memória do SAM 2 (via `transformers`Execute o SimpleTracker e o SAM 2 em um clipe de 30 segundos de uma multidão e compare as contagens de interruptores de identificação, rotulado manualmente os identificadores de verdade para 5 pessoas salientes.

> **【中文解读】**No 术语表中的"O que as pessoas dizem" vs "O que realmente significa" 区分日常口语和精确技术含义── em equipe,统一术语定义可以避免大量沟通误解──


## Termos-chave .

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Tracking-by-detection | "Detect then associate" | Per-frame detector + Hungarian assignment on IoU / appearance |
| Kalman filter | "Motion predict" | Linear dynamics + covariance for smooth track predictions and occlusion handling |
| Hungarian algorithm | "Optimal assignment" | Solves the minimum-cost bipartite matching problem; `scipy.optimize.linear_sum_assignment` |
| ByteTrack | "Low-confidence second pass" | Re-match unmatched tracks to low-confidence detections to recover short occlusions |
| DeepSORT | "SORT + appearance" | Adds a ReID feature for cross-frame matching; better for ID preservation |
| Memory bank | "SAM 2 trick" | Per-instance spatio-temporal features stored across frames; cross-attention replaces explicit association |
| Object Multiplex | "SAM 3.1 shared memory" | Single shared memory with per-instance queries for fast many-object tracking |
| HOTA | "Modern tracking metric" | Decomposes into detection and association accuracy; community standard |

> **【中文解读】**延伸阅读 fornece recursos de alta qualidade para a aprendizagem profunda.


## Mais leitura 延伸阅读

- [SORT (Bewley et al., 2016)](https://arxiv.org/abs/1602.00763) o papel mínimo de rastreamento por detecção
- [DeepSORT (Wojke et al., 2017)](https://arxiv.org/abs/1703.07402) adiciona recurso de aparência
- [ByteTrack (Zhang et al., 2022)](https://arxiv.org/abs/2110.06864) Baixa confiança em segundo passo
- [BoT-SORT (Aharon et al., 2022)](https://arxiv.org/abs/2206.14651) Compensamento de movimento da câmera
- [HOTA (Luiten et al., 2020)](https://arxiv.org/abs/2009.07736) Metrica de rastreamento decomposta
- [SAM 2 video segmentation (Meta, 2024)](https://ai.meta.com/sam2/) Tracker baseado em memória
- [SAM 3.1 Object Multiplex (Meta, March 2026)](https://ai.meta.com/blog/segment-anything-model-3/)
