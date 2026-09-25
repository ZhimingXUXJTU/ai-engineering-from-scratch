# Modelos mundiais e difusão de vídeo

> Um modelo de vídeo que prevê os próximos segundos de uma cena é um simulador de mundo, condição que previsão sobre ações e você tem um motor de jogo aprendido.

> **【中文解读】**能够预测场景接下来的几秒的视频模型就是一个世界模拟器――将预测条件化为动作,就得到了一个学习的游戏引擎――世界模型是AI的前沿方向让AI理解物理世界的动态规律――

> **【拓展：世界模型的前沿】**Sora(OpenAI) e Genie(DeepMind) é o representante do modelo mundial. O modelo mundial pode ser usado para auto-conduir em simulação.

**Type:** Learn + Build | **类型:** 学习 + 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 4 Lesson 10 (Diffusion), Phase 4 Lesson 12 (Video Understanding), Phase 4 Lesson 23 (DiT + Rectified Flow) | **前置知识:** Phase 4 Lesson 10（扩散模型），Phase 4 Lesson 12（视频理解），Phase 4 Lesson 23（DiT + 整流流）
**Time:** ~75 minutes | **时间:** ~75 分钟

## Objetivos de aprendizagem

- Explique a diferença entre um modelo de geração de vídeo puro (Sora 2) e um modelo de mundo com condição de ação (Genie 3, DreamerV3)
- Descreva um vídeo DiT: patches espaciotemporais, codificação de posição 3D, atenção conjunta em tokens (T, H, W)
- Rastrear como um modelo mundial se conecta à robótica: planos VLM → modelo de vídeo simula → dinâmica inversa emite ações
- Escolha entre Sora 2, Genie 3, Runway GWM-1 Worlds, Wan-Video e HunyuanVideo para um determinado caso de uso (vídeo criativo, sim interativo, síntese de condução autônoma)

> **【中文解读】**O objetivo do aprendizado é listar as capacidades centrais que devem ser adquiridas após a conclusão do curso.


## O problema é o problema da introdução

A geração de vídeo e a modelagem mundial convergem em 2026. Um modelo que pode gerar um minuto de vídeo coerente, tem, em certo sentido, aprendido como o mundo se move: permanência de objetos, gravidade, causalidade, estilo. Se você condicionar essa previsão sobre ações (andar à esquerda, abrir a porta), o modelo de vídeo se torna um simulador aprenhável que pode substituir um motor de jogo, um simulador de condução ou um ambiente robótico.

> 视频生成和世界建模于 2026年融合了── um modelo que pode gerar um minuto连贯视频, em certo sentido, aprendeu como o mundo se move: durabilidade de objetos, força, relação de consequências, estilo── se você estiver em pronóstico para mover como condição (((para a esquerda, para o lado esquerdo, para o lado esquerdo), o modelo de vídeo se torna um simulador aprendiz, pode substituir um motor de jogo, um simulador de condução ou um ambiente de máquina──

As apostas são concretas. Genie 3 gera ambientes jogáveis a partir de uma única imagem. A pista GWM-1 Worlds sintetiza infinitas cenas exploráveis. A Sora 2 produz vídeos de minutos com áudio sincronizado e física modelada. NVIDIA Cosmos-Drive, Wayve Gaia-2 e Tesla DrivingWorld geram vídeos de condução realistas para dados de treinamento de veículos autônomos. O paradigma do modelo mundial está silenciosamente a assumir o sim-to-real para a robótica.

> Genie 3 de um único quadro gerar ambiente jogável. Runway GWM-1 Worlds  Sintetizado ilimitado explorar cenário. Sora 2 生成带同步音频和物理建模的分钟级视频. NVIDIA Cosmos-Drive、Wayve Gaia-2 和 Tesla DrivingWorld 为自动驾驶训练数据生成真实驾驶视频.

Esta lição é a lição "pintura geral" para a Fase 4. Ela conecta geração de imagens, compreensão de vídeo e raciocínio agente no padrão de arquitetura para o qual a pesquisa dominante está se movendo.

> Este curso é um curso de "todo o cenário" da quarta fase. Ele irá gerar imagens, vídeo compreensão e inteligência de pensamento conectados a um modelo de arquitetura em curso de estudo.

## O conceito central.

> **【中文解读】**Este capítulo apresenta os conceitos e teorias fundamentais.


### Três famílias de modelos mundiais

```mermaid
flowchart LR
    subgraph GEN["Pure video generation"]
        G1["Text / image prompt"] --> G2["Video DiT"] --> G3["Video frames"]
    end
    subgraph ACTION["Action-conditioned world model"]
        A1["Past frames + action"] --> A2["Latent-action video DiT"] --> A3["Next frames"]
        A3 --> A1
    end
    subgraph RL["World models for RL (DreamerV3)"]
        R1["State + action"] --> R2["Latent transition model"] --> R3["Next latent + reward"]
        R3 --> R1
    end

    style GEN fill:#dbeafe,stroke:#2563eb
    style ACTION fill:#fef3c7,stroke:#d97706
    style RL fill:#dcfce7,stroke:#16a34a
```

- **Sora 2**É uma geração de vídeo pura condicionada a pedidos.
  Tradução:**Sora 2**É puro vídeo gerado, condicionado a um argumento. Não há nenhuma interação de movimento.
- **Genie 3**- Não .**GWM-1 Worlds**- Não .**Mirage / Magica**Os modelos de mundo condicionados à ação são: Infere ações latentes a partir de vídeo observado, e depois condicione as previsões de quadros futuros sobre ações.
  Tradução:**Genie 3**- Não.**GWM-1 Worlds**- Não.**Mirage / Magica**É um modelo mundial de condicionamento de movimento. De um vídeo observado, o potencial de movimento é deduzido, e depois, o futuro é condicionado por um movimento.
- **DreamerV3**A família de modelos mundiais RL clássicos prevêem em um espaço latente com condicionamento de ação explícito, treinado em um sinal de recompensa.
  Tradução:**DreamerV3**O RL mundial modelo familiar em espaço intimo prevê, com condicionamento de movimento manifesto, treinamento em sinal de recompensa.

### Arquitetura de vídeo

```
Video latent:          (C, T, H, W)
Patchify (spatial):    grid of P_h x P_w patches per frame
Patchify (temporal):   group P_t frames into a temporal patch
Resulting tokens:      (T / P_t) * (H / P_h) * (W / P_w) tokens
```

A codificação posicional é 3D: uma rotativa ou aprendizagem de inserção por coordenada (t, h, w).

- **Full joint** todos os tokens atendem a todos os tokens. O ((N^2) com tokens N. Proibido para vídeos longos.
  Tradução:**全联合** todos os tokens  todos os tokens  O  N^2) 对长视频不可行──
- **Divided** atenção temporal alternada (a mesma posição espacial, através do tempo: `(H*W) * T^2`) e atenção espacial (seme passo de tempo, através do espaço: `T * (H*W)^2`Usado pelo TimeSformer e pela maioria dos DiTs de vídeo.
  Tradução:**分离**交替时间注意力(同空间位置,跨时间) 和空间注意力(同时间步,跨空间) ――TimeSformer 和大多数视频 DiT 使用──
- **Window** janelas locais em (t, h, w). Usado por Video Swin.
  Tradução:**窗口**(t, h, w) 中的局部窗口──Video Swin 使用──

Cada modelo de difusão de vídeo de 2026 usa um destes três padrões, além de condicionamento AdaLN (Lessão 23) e fluxo rectificado.

> Cada modelo de expansão de vídeo de 2026 utiliza um destes três modelos, adicionado à AdaLN  condicionamento (§ 23 课) e ao total 流――.

### Condicionamento das acções: modelos de acção latentes

O génio aprende uma .**latent action**O decodificador do modelo então condiciona a ação latente inferida  não em teclas de teclado explícitas. Na inferência, um usuário pode especificar uma ação latente (ou amostar uma a partir de um anterior novo) e o modelo gera a próxima ação consistente com essa ação.

Sora salta a interface de ação inteiramente. Seu decodificador prevê os próximos tokens do espaço-tempo dos tokens do espaço-tempo passado.

### Plausível física

A versão 2026 da Sora 2 foi anunciada explicitamente.**physical plausibility**O modelo melhora visível em objetos caídos, personagens em colisão e falhas no propósito (um salto perdido) contra Sora 1.

A plausibilidade continua a ser o modo de falha dominante. Vídeos de 2024-2025 de pessoas comendo espaguetes ou bebendo de copos revelaram a falta de representação de objetos persistente do modelo. Modelos de 2026 (Sora 2, Runway Gen-5, HunyuanVideo) reduzem, mas não eliminam estes.

### Modelos mundiais de condução autônoma

Os modelos de mundo de condução geram cenas de estrada realistas condicionadas a trajetórias, caixas de limite ou mapas de navegação.

- **Cosmos-Drive-Dreams**(NVIDIA)  gera minutos de vídeo de condução para treinamento RL.
- **Gaia-2**(Wayve)  Sintese de cenários condicionada por trajetória para avaliação de políticas.
- **DrivingWorld**Simula o tempo variado, a hora do dia, as condições do trânsito.
- **Vista**(ByteDance)  Síntese de cenas de condução reativa.

Eles substituem a coleta de dados reais caros para casos de canto  caminhadas de pedestres à noite, interseções geladas, tipos de veículos incomuns  que de outra forma exigiriam milhões de quilômetros de condução.

> Eles substituíram a coleta de dados do mundo real caro para lidar com situações de borda: caminhantes de noite deslocados por estradas, passagens de gelo, tipos de veículos estranhos, ou precisam de milhões de milhas de condução.

### Estaca de robótica: VLM + modelo de vídeo + dinâmica inversa

O novo ciclo de robótica de três componentes:

> O novo ciclo de máquinas:

1. **VLM**analisa o objetivo ("colher o copo vermelho"), planeja uma sequência de ação de alto nível.
   Tradução:**VLM**解析目标 (("拿起红色杯子"),规划高层动作序列──
2. **Video generation model**Simula o que executar cada ação seria como  prevê observações N quadros para frente.
   Tradução:**视频生成模型**模拟执行每个动作后样子预测 N 后的观测──
3. **Inverse dynamics model**extrai os comandos motores concretos que produziriam essas observações.
   Tradução:**逆动力学模型**提取产生这些观测的具体电机指令──

O modelo mundial faz a imaginação; a dinâmica inversa fecha o ciclo de ativação. Genie Envisioner é uma instância; muitos grupos de pesquisa estão convergindo nessa estrutura.

> Isto substituiu o RL de forma e padrão de recompensa intenso. O modelo mundial é responsável pela imaginação; inversamente, a dinamica é fechada para a execução.

### Avaliação

- **Visual quality** FVD (Fréchet Video Distance), estudos de utilizadores.
  Tradução:**视觉质量**FVD(Fréchet 视频距离) 、 usuário研究。
- **Prompt alignment** CLIPS score por quadro, avaliação ao estilo VQA.
  Tradução:**提示对齐** Cada  CLIPScore、VQA 风格评估──
- **Physical plausibility** classificação manual num conjunto de índices de referência (indice de referência interno da Sora 2, VBench).
  Tradução:**物理合理性**                                                                                                                                                                                                                                                              
- **Controllability**(para modelos interativos do mundo)  ação → consistência de observação; pode voltar a um estado anterior?
  Tradução:**可控性**(交互式世界模型) 动作→观测一致性;能否回到前前的状态?

### Paisagem modelo em 2026

| Model | Use | Parameters | Output | License |
|-------|-----|------------|--------|---------|
| Sora 2 | text-to-video, audio | — | 1-min 1080p + audio | API only |
| Runway Gen-5 | text/image-to-video | — | 10s clips | API |
| Runway GWM-1 Worlds | interactive world | — | infinite 3D rollout | API |
| Genie 3 | interactive world from image | 11B+ | playable frames | research preview |
| Wan-Video 2.1 | open text-to-video | 14B | high-quality clips | non-commercial |
| HunyuanVideo | open text-to-video | 13B | 10s clips | permissive |
| Cosmos / Cosmos-Drive | autonomous driving sim | 7-14B | driving scenes | NVIDIA open |
| Magica / Mirage 2 | AI-native game engine | — | modifiable worlds | product |

> **【中文解读】**Este é um método de "desde zero" que ajuda a entender o princípio da estrutura, não é um problema que se encontra em uma caixa negra.

> **【拓展：工业部署中的视觉系统】**No implementar industrial real, o modelo visual precisa considerar a possibilidade de atrasos, modelos de tamanho, dispositivos de margem, etc. TensorRT, ONNX Runtime, OpenVINO são ferramentas de aceleração de cálculo de uso comum.

> **【拓展：数据标注与质量】** Visual task's effect highly depends on label data quality──Label Studio、CVAT is the mainstream marking tool──In industrial scenarios, proactive learning(Active Learning) pode reduzir o custo de marcação: modelo contra um pedido de amostra não definido marcação artificial, identidade de amostra auto-marcação──




## Construí-lo e realizei-o.
```figure
v4-world-rollout
```

## Construí-lo

### Passo 1: 3D patch para vídeo

```python
import torch
import torch.nn as nn


class VideoPatch3D(nn.Module):
    def __init__(self, in_channels=4, dim=64, patch_t=2, patch_h=2, patch_w=2):
        super().__init__()
        self.proj = nn.Conv3d(
            in_channels, dim,
            kernel_size=(patch_t, patch_h, patch_w),
            stride=(patch_t, patch_h, patch_w),
        )
        self.patch_t = patch_t
        self.patch_h = patch_h
        self.patch_w = patch_w

    def forward(self, x):
        # x: (N, C, T, H, W)
        x = self.proj(x)
        n, c, t, h, w = x.shape
        tokens = x.reshape(n, c, t * h * w).transpose(1, 2)
        return tokens, (t, h, w)
```

Um conv 3D com passo igual ao núcleo atua como o patchador espaciotemporal. `(T, H, W) -> (T/2, H/2, W/2)`Grade de tokens.

### Passo 2: codificação de posição rotativa em 3D

Embedings rotativos de posição (RoPE) aplicados separadamente ao longo `t`- Não .`h`- Não .`w`Ácidos graxos:

```python
def rope_3d(tokens, t_dim, h_dim, w_dim, grid):
    """
    tokens: (N, T*H*W, D)
    grid: (T, H, W) sizes
    t_dim + h_dim + w_dim == D
    """
    T, H, W = grid
    n, seq, d = tokens.shape
    if t_dim + h_dim + w_dim != d:
        raise ValueError(f"t_dim+h_dim+w_dim ({t_dim}+{h_dim}+{w_dim}) must equal D={d}")
    assert seq == T * H * W
    t_idx = torch.arange(T, device=tokens.device).repeat_interleave(H * W)
    h_idx = torch.arange(H, device=tokens.device).repeat_interleave(W).repeat(T)
    w_idx = torch.arange(W, device=tokens.device).repeat(T * H)
    # Simplified: just scale channels by frequencies. Real RoPE rotates pairs.
    freqs_t = torch.exp(-torch.log(torch.tensor(10000.0)) * torch.arange(t_dim // 2, device=tokens.device) / (t_dim // 2))
    freqs_h = torch.exp(-torch.log(torch.tensor(10000.0)) * torch.arange(h_dim // 2, device=tokens.device) / (h_dim // 2))
    freqs_w = torch.exp(-torch.log(torch.tensor(10000.0)) * torch.arange(w_dim // 2, device=tokens.device) / (w_dim // 2))
    emb_t = torch.cat([torch.sin(t_idx[:, None] * freqs_t), torch.cos(t_idx[:, None] * freqs_t)], dim=-1)
    emb_h = torch.cat([torch.sin(h_idx[:, None] * freqs_h), torch.cos(h_idx[:, None] * freqs_h)], dim=-1)
    emb_w = torch.cat([torch.sin(w_idx[:, None] * freqs_w), torch.cos(w_idx[:, None] * freqs_w)], dim=-1)
    return tokens + torch.cat([emb_t, emb_h, emb_w], dim=-1)
```

Forma aditiva simplificada. RoPE real gira canais emparelhados em frequências; as informações de posição são as mesmas.

### Passo 3: Bloco de atenção dividido

```python
class DividedAttentionBlock(nn.Module):
    def __init__(self, dim=64, heads=2):
        super().__init__()
        self.time_attn = nn.MultiheadAttention(dim, heads, batch_first=True)
        self.space_attn = nn.MultiheadAttention(dim, heads, batch_first=True)
        self.ln1 = nn.LayerNorm(dim)
        self.ln2 = nn.LayerNorm(dim)
        self.ln3 = nn.LayerNorm(dim)
        self.mlp = nn.Sequential(nn.Linear(dim, 4 * dim), nn.GELU(), nn.Linear(4 * dim, dim))

    def forward(self, x, grid):
        T, H, W = grid
        n, seq, d = x.shape
        # time attention: same (h, w), across t
        xt = x.view(n, T, H * W, d).permute(0, 2, 1, 3).reshape(n * H * W, T, d)
        a, _ = self.time_attn(self.ln1(xt), self.ln1(xt), self.ln1(xt), need_weights=False)
        xt = (xt + a).reshape(n, H * W, T, d).permute(0, 2, 1, 3).reshape(n, seq, d)
        # space attention: same t, across (h, w)
        xs = xt.view(n, T, H * W, d).reshape(n * T, H * W, d)
        a, _ = self.space_attn(self.ln2(xs), self.ln2(xs), self.ln2(xs), need_weights=False)
        xs = (xs + a).reshape(n, T, H * W, d).reshape(n, seq, d)
        xs = xs + self.mlp(self.ln3(xs))
        return xs
```

A atenção temporal atende dentro de cada posição espacial ao longo do tempo; a atenção espacial atende dentro de cada quadro através de posições. Duas operações O(T^2 + (HW) ^ 2) em vez de um O((THW) ^ 2).

### Passo 4: Compõem um pequeno vídeo

```python
class TinyVideoDiT(nn.Module):
    def __init__(self, in_channels=4, dim=64, depth=2, heads=2):
        super().__init__()
        self.patch = VideoPatch3D(in_channels=in_channels, dim=dim, patch_t=2, patch_h=2, patch_w=2)
        self.blocks = nn.ModuleList([DividedAttentionBlock(dim, heads) for _ in range(depth)])
        self.out = nn.Linear(dim, in_channels * 2 * 2 * 2)

    def forward(self, x):
        tokens, grid = self.patch(x)
        for blk in self.blocks:
            tokens = blk(tokens, grid)
        return self.out(tokens), grid
```

Não é um gerador de vídeo que funciona; é uma demonstração estrutural que forma cada peça corretamente.

### Passo 5: Verifique as formas

```python
vid = torch.randn(1, 4, 8, 16, 16)  # (N, C, T, H, W)
model = TinyVideoDiT()
out, grid = model(vid)
print(f"input  {tuple(vid.shape)}")
print(f"tokens grid {grid}")
print(f"output {tuple(out.shape)}")
```

Esperem .`grid = (4, 8, 8)`E ...`out = (1, 256, 32)`Depois de parchear, a cabeça projeta para parches espaciotemporais por token, prontos para ser desparcheado de volta para um vídeo.

> **【中文解读】**Este capítulo mostra como usar um framework maduro (como PyTorch、HuggingFace etc) rápida aplicação desta tecnologia.





> **【拓展：视觉模型的持续学习】**Em um ambiente de produção, o modelo visual precisa se adaptar constantemente a novos dados. Isto é especialmente importante na condução automática e no controle de qualidade industrial.

## Use-o com o framework implementado.

Padrões de acesso à produção para 2026:

- **Sora 2 API**- Text-to-video, áudio sincronizado.
- **Runway Gen-5 / GWM-1**(Runway)  Imagem a vídeo, mundos interativos.
- **Wan-Video 2.1 / HunyuanVideo** auto-host de código aberto.
- **Cosmos / Cosmos-Drive**Simulação de condução de pesos abertos.
- **Genie 3** visualização da investigação, solicitação de acesso.

Para construir uma demonstração interativa de modelo mundial: comece com o Wan-Video para qualidade, capa em um adaptador de ação latente para interatividade. Para simulação de condução autônoma: Cosmos-Drive é a referência aberta de 2026.

Para a robótica, a pilha na natureza:

> **【中文解读】**Este capítulo se concentra em como o modelo será implantado como produto disponível. De modelo original a nível de produção, os sistemas precisam considerar várias dimensões de otimização de desempenho, tratamento de erros, controle, etc.


1. Objetivo de língua -> VLM (Qwen3-VL) -> plano de alto nível.
2. Plano -> Modelo de vídeo latente -> implantação imaginária.
3. Rollout -> modelo de dinâmica inversa -> ações de baixo nível.
4. Ações executadas -> observação reintegrada para o passo 1.



## Envia-o . Produto .

> **【中文解读】**Practicação de temas de fácil/médio/difícil  3o dificuldade de passagem  Recomendação de completar pelo menos Praça de nível médio Classe difícil  Adaptação a pesquisa profunda ou preparação para o encontro 


Esta lição produz:

- `outputs/prompt-video-model-picker.md` escolha entre Sora 2 / Runway / Wan / HunyuanVideo / Cosmos dada tarefa, licença e latência.
- `outputs/skill-physical-plausibility-checks.md` uma habilidade que define os controles automatizados (permanência do objeto, gravidade, continuidade) para executar em qualquer vídeo gerado antes do envio.

## Exercícios.

1. **(Easy)**Calcule a contagem de tokens para um vídeo de 5 segundos em 360p em patch-t=2, patch-h=8, patch-w=8. Razão sobre memória para atenção neste tamanho.
2. **(Medium)**Troque o bloco de atenção dividido acima para um bloco de atenção conjunto completo e mida a forma e a contagem de parâmetros. Explique por que a atenção dividida é necessária para modelos de vídeo reais.
3. **(Hard)**Construa um modelo de vídeo de ação latente mínimo: tome um conjunto de dados de (frame_t, action_t, frame_{t+1}) triples (qualquer jogo 2D simples), treine um pequeno vídeo DiT condicionado a embebimentos de ação, e mostre que diferentes ações produzem diferentes quadros próximos.

> **【中文解读】**No 术语表中的"O que as pessoas dizem" vs "O que realmente significa" 区分日常口语和精确技术含义── em equipe,统一术语定义可以避免大量沟通误解──


## Termos-chave .

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| World model | "Learned simulator" | A model that predicts future observations given state and action |
| Video DiT | "Spacetime transformer" | Diffusion transformer with 3D patchification and divided attention |
| Latent action | "Inferred control" | Discrete or continuous action latent inferred from frame pairs; used to condition next-frame generation |
| Divided attention | "Time then space" | Two attention operations per block — across time then across space — to keep O(N^2) manageable |
| Object permanence | "Things stay real" | Scene property that video models must learn; classic failure mode on food, glassware |
| FVD | "Fréchet Video Distance" | Video equivalent of FID; primary visual quality metric |
| Inverse dynamics model | "Observations to actions" | Given (state, next state), output the action that connects them; closes robotics loop |
| Cosmos-Drive | "NVIDIA driving sim" | Open-weights autonomous-driving world model for RL and evaluation |

> **【中文解读】**延伸阅读 fornece recursos de alta qualidade para a aprendizagem profunda.


## Mais leitura 延伸阅读

- [Sora technical report (OpenAI)](https://openai.com/index/video-generation-models-as-world-simulators/)
- [Genie: Generative Interactive Environments (Bruce et al., 2024)](https://arxiv.org/abs/2402.15391) Modelos latentes de mundo de ação
- [TimeSformer (Bertasius et al., 2021)](https://arxiv.org/abs/2102.05095) atenção dividida para os transformadores de vídeo
- [DreamerV3 (Hafner et al., 2023)](https://arxiv.org/abs/2301.04104) Modelos mundiais para RL
- [Cosmos-Drive-Dreams (NVIDIA, 2025)](https://research.nvidia.com/labs/toronto-ai/cosmos-drive-dreams/) Modelo mundial de condução
- [Top 10 Video Generation Models 2026 (DataCamp)](https://www.datacamp.com/blog/top-video-generation-models)
- [From Video Generation to World Model — survey repo](https://github.com/ziqihuangg/Awesome-From-Video-Generation-to-World-Model/)
