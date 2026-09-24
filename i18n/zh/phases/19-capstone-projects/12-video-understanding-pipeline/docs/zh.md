# 视频理解管道 (场景,问答,搜索)

> 十二个实验室生产了马伦戈+佩加索. 视频DB发送了CRUD为视频API. 艾尔2的Molmo2公布了开放的VLM检查站. 双胞胎长文本处理数小时的视频. 时间镜头-100K定义了时间定位. 2026年管道已经解决了:场景分区,每场景标题+嵌入,转录对齐,多向量索引,以及一个用 (开始,结束) 时间标签和框架预览来回答的问题. 终点石正在摄入100小时, 达到公共标准,

> **【中文解读】**本节是综合项目构建视频理解流水线,处理视频内容的AI分析.


**Type:** Capstone | **类型:** Capstone
**Languages:** Python (pipeline), TypeScript (UI) | **语言:** Python (pipeline), TypeScript (UI)
**Prerequisites:** Phase 4 (CV), Phase 6 (speech), Phase 7 (transformers), Phase 11 (LLM engineering), Phase 12 (multimodal), Phase 17 (infrastructure)

>  **【前置】**顶点项目 12 = 综合阶段 4/6/7/11/12/17──视频理解流水线 = 12个实验室(马伦戈+佩加索) +视频DB + AI2 Molmo 2 + 双胞胎长上下文 + TimeLens-100K──
>  **【类比】**视频理解 = "AI 视频助理"──2026 标准:场景分割→每场幕 字幕+嵌入→转录对齐→多向量索引→查询 返回 (开始,结束) 时间+预览──目标:100 小时长+公开基准+计数/动作幻觉测量──**前置知识:**阶段4 (CV),阶段6 (演讲),阶段7 (变革机),阶段11 (LLM工程),阶段12 (多元),阶段17 (基础设施)
**Phases exercised:**现在,我们在这个世界里,**涉及阶段:**子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子子
**Time:** 30 hours | **时间:** 30 hours

## 问题 问题引入

> **【中文解读】**本节描述视频理解管道的核心挑战――长视频QA是2026年带宽需求最大的多模态问题――虽然Gemini 2.5 Pro可以原生读取2小时视频,但将100小时视频索引为可查询语料库仍然需要场景级索引――生产级管道结合场景分区(TransNetV2/PySceneDetect)、每场景VLM 描述、ASR 转录对齐和多导向索引――已知难题是数量和动作类别问题幻觉本课程专门测量这种类别的失败――

> **【拓展：视频 AI 产品生态】**2026年视频理解主要产品:十二个实验室(马伦戈+佩加索斯 商业化) ‧视频DB(CRUD-for-video API) ‧AI2 Molmo 2(开源VLM) ‧Gemini 长上下文模型原生支持小时级视频‧TimeLens-100K 定义了大规模时间定位基准‧评估使用 ActivityNet-QA 和 NeXT-GQA 公开基准‧场景分区通常出于60-80场景/小时视频,每场景三种景向量‧描述/关键/转录),存储在Qdrant多向量集合中──

长频视频QA是2026年规模最需要带宽的多模式问题. 双子球 2.5 Pro 可以本地读取2小时的视频, 但在可查询的体内摄入100小时的视频仍然需要一个场景级索引. 制作形状结合了场景细分 (TransNetV2或PySceneDetect),每场景标题与VLM (Gemini 2.5,Qwen3-VL-Max或Molmo 2),转录对齐 (Whisper-v3-turbo与词时刻标签),以及多向量索引,存储标题,框架嵌入和转录一边. 查询管道的答案是 (开始,结束) 时间标签以及框架预览.

> 长频视频QA是2026年规模最需要带宽的多模式问题.


测量标准是公开的 (ActivityNet-QA,NeXT-GQA) 加上你自己的100个查询定制集.计算和行动类型的问题上的幻觉是已知的硬失败类;终点石显然测量它.

> 标准标志是公开的 (ActivityNet-QA, NeXT-GQA) 加上你自己的100个查询定制集.


## 概念的核心概念

> **【中文解读】**摄取时三条管道并行运行:场景分割(切分为场景)、VLM 描述(每场景生成描述+关键嵌)、ASR对齐(语-v3-turbo词级时间)。三条流按场景ID 和时间范围合并,每场景三种向量存入Qdrant多向量索引──查询时自然语言问题同时检索三种向量,RRF 合并后使用TimeLens 定位适配器精炼窗口,VLM 合成机生成带时间引用答案──

> **【拓展：视频 VLM 幻觉问题】**计算问题:"有多少人进入房间?") 和动作顺序问题("厨师在前倒吗?") 上幻觉率极高,这是已知的硬性限制.

入时,三个管道并行.**Scene segmentation**剪辑视频成场景.**VLM captioning**通过键盘生成一个字幕,**ASR alignment**制作字面级时间标签.三个流由 (scene_id,时间范围) 连接.每个场景在多向量索引 (Qdrant) 中得到三个向量类型:标题嵌入,键盘嵌入,转录嵌入.

> 道的三条管道在入时并行.


在查询时,自然语言问题针对三个向量;结果与RRF合并;一个时间定位适配器 (TimeLens式) 精炼了顶部场景内的 (开始,结束) 窗口.VLM合成器 (Gemini 2.5 Pro或Qwen3-VL-Max) 采用引用的时间标签和框架预览来查询+顶部场景+截截图框架和答案.

> 在查询时,自然语言问题针对三个向量;结果与RRF合并;一个时间定位适配器 (TimeLens式) 在顶部场景内精细化了 (开始,结束) 窗口.


测量幻觉是重要的.计算 ("房间里有多少人进来?") 和行动类型 ("厨师在之前倒水吗?") 的问题是不值得信赖的.

> 计算 ("房间里有多少人进来?") 和行动类型 ("厨师在之前倒水吗?") 的问题是不值得信赖的. 报告准确性与描述性问题分开.


## 建筑,建筑

```
video file / URL
      |
      v
PySceneDetect / TransNetV2  (scene segmentation)
      |
      +--- per-scene keyframe --- VLM caption + frame embedding
      |                            (Gemini 2.5 Pro / Qwen3-VL-Max / Molmo 2)
      |
      +--- audio channel --- Whisper-v3-turbo ASR + word timestamps
      |
      v
multi-vector Qdrant: {caption_emb, keyframe_emb, transcript_emb}
      |
query:
  dense queries against all three -> RRF merge -> top-k scenes
      |
      v
TimeLens / VideoITG temporal grounding (refine start/end within scene)
      |
      v
VLM synth: query + top scenes + frame previews
      |
      v
answer + (start, end) timestamps + frame thumbs + citations
```

##  技术

- 场景细分:TransNetV2 (最先进的2024-26) 或PySceneDetect
  中文翻译:场景细分:TransNetV2 (最先进的2024-26) 或PySceneDetect
- 通过快速的语,使用词语时刻标签.
  中文翻译:ASR:通过快速的语,使用语音时刻标签的Whisper-v3-turbo
- 维LM子+答案机:双子 2.5 专业或Qwen3-VL-Max或Molmo 2
  中文翻译:VLM 猎人 + 答案机:双子 2.5 专业或Qwen3-VL-Max或Molmo 2
- 时间定位:TimeLens-100K训练式适配器或视频ITG
  中文翻译:时间接地:TimeLens-100K训练适配器或VideoITG
- 索引:多向量支持的Qdrant (标题/框架/转录)
  中文翻译:索引:多向量支持的Qdrant (标题 / 框架 / 转录)
- 接口:下一个.js 15 带HTML5视频播放器和场景缩影
  中文翻译:UI:Next.js 15 带HTML5视频播放器和场景缩影
- 标准:ActivityNet-QA,NeXT-GQA,定制100个问题手动标记的套件
  中文翻译:Eval:活动网QA,下一个GQA,定制100个问题手动标签的套件
- 幻觉基准:手标的计数和行动类型子组
  中文翻译:幻觉基准:手标签的计算和行动类型子组

## 动手构建

> **【中文解读】**构建视频理解流水线的 8个阶段:视频摄入 Youtube/MP4 降采样到 720p) 关键提取(每秒 1  + 场景变化检测) 声频转录(语大-v3)  OCR(PaddleOCR) 描述(视觉语言模型) 时序对齐(将转录/OCR/描述对齐到时间轴) 多模态融合检索和幻觉基准测试――

> **【拓展：视频理解在 2026 年的前沿进展】**谷歌的双子 2.5 程序原生支持 1 小时视频输入,Claude 的视频模式支持截图分析.Twelve Labs 的Pegasus API 提供专用视频嵌入.关键挑战是时间序列理解.
```figure
cf-scene-index
```

## 建立它

1. **Ingest walker.**接受YouTubeURL或本地MP4文件. 如果需要,下调到720p.坚持`{video_id, file_path}`现在,我们要去.
   中文翻译:1. **Ingest walker.**接受YouTubeURL或本地MP4文件. 如果需要,下调到720p.坚持`{video_id, file_path}`现在,我们要去.

2. **Scene segmentation.**运行TransNetV2或PySceneDetect以生成`[{scene_id, start_ms, end_ms, keyframe_path}]`目标100小时: ~6K-8K场景.
   翻译: 翻译:**Scene segmentation.**运行TransNetV2或PySceneDetect以生成`[{scene_id, start_ms, end_ms, keyframe_path}]`目标100小时: ~6K-8K场景.

3. **ASR pass.**运行Whisper-v3turbo在音频上; 导出文字级别的时间; 分成每场景的转录片.
   翻译: 翻译:**ASR pass.**运行Whisper-v3turbo在音频上; 导出文字级别的时间; 分成每场景的转录片.

4. **VLM captioning.**每场景,用键盘和短标题模板拨打双子座2.5 Pro (或Qwen3-VL-Max).生成标题+框架嵌入.
   翻译: 翻译:**VLM captioning.**每场景,用键盘和短标题模板拨打双子座2.5 Pro (或Qwen3-VL-Max).生成标题+框架嵌入.

5. **Multi-vector index.**源集有三个命名的向量.`{video_id, scene_id, start_ms, end_ms, keyframe_url}`现在,我们要去.
   翻译: 五.**Multi-vector index.**源集有三个命名的向量.`{video_id, scene_id, start_ms, end_ms, keyframe_url}`现在,我们要去.

6. **Query.**自然语言问题引发了三个密集的查询;与相互的排列融合融合融合;顶级k=5场景.
   翻译: 七个字**Query.**自然语言问题引发了三个密集的查询;与相互的排列融合融合融合;顶级k=5场景.

7. **Temporal grounding.**在上方场景上运行TimeLens式适配器,以精细化场景内的 (开始,结束) 窗口.
   翻译:7.**Temporal grounding.**在上方场景上运行TimeLens式适配器,以精细化场景内的 (开始,结束) 窗口.

8. **VLM synth.**通过查询+前三场景剪辑 (作为图像或短片) +转录来调用双子 2.5 Pro. 要求 `(video_id, start_ms, end_ms)`引用.
   翻译:8.**VLM synth.**通过查询+前三场景剪辑 (作为图像或短片) +转录来调用双子 2.5 Pro. 要求 `(video_id, start_ms, end_ms)`引用.

9. **Eval.**运行 ActivityNet-QA 和 NeXT-GQA. 建立一个100个查询的自定义集. 报告总体准确性+每个类的分类 (计数,操作,描述).
   翻译:9.**Eval.**运行 ActivityNet-QA 和 NeXT-GQA. 建立一个100个查询的自定义集. 报告总体准确性+每个类的分类 (计数,操作,描述).

## 用它使用方法

```
$ video-qa ask --url=https://youtube.com/watch?v=X "how many cars pass the intersection in the first minute?"
[scene]    23 scenes detected
[asr]      transcript complete, 4m12s
[index]    69 vectors written (23 scenes x 3)
[query]    top scene: scene 3 [01:32-01:54], confidence 0.84
[ground]   refined window: [00:12-00:58]
[synth]    gemini 2.5 pro, 1.4s
answer:    5 cars pass the intersection between 00:12 and 00:58.
citations: [scene 3: 00:12-00:58]
          [frame preview at 00:14, 00:27, 00:44, 00:51, 00:57]
```

## 发射上线

`outputs/skill-video-qa.md`提供YouTubeURL或上传的视频,该管道将场景索引,并以时间标记引用来回答问题.

> `outputs/skill-video-qa.md`是交付物. 给定YouTubeURL或上传的视频,管道索引场景,并以时间标记引用回答问题.


| Weight | Criterion | How it is measured |
|:-:|---|---|
| 25 | Temporal grounding IoU | Intersection-over-union on held-out grounding set |
| 20 | QA accuracy | NeXT-GQA and custom 100-query |
| 20 | Ingest throughput | Hours of video per dollar spent |
| 20 | UI and citation UX | Timestamp links, thumbnail strip, jump-to-frame |
| 15 | Hallucination rate | Counting and action-type accuracy separately |
| **100** | | |

## 练习题

1. 报道标题质量达尔塔在人类评级的50场景样本上.

2. 减少每场景的框架嵌入到一个聚合向量而不是多向量.

3. 建立"严格计数"模式:合成器将每次计数的实例都以时间印取出来,用户点击验证. 测量用户验证是否减少幻觉.

4. 根据标准摄入成本:每美元的视频时间,在三个VLM选择中.

5. 添加扬声器日记转录:在音频中运行pyannote扬声器日记转录,并嵌入每个扬声器的转录. 展示"爱丽丝对X说什么?"的查询.

## 关键词 关键词

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| Scene segmentation | "Shot detection" | Cutting video into scenes at shot boundaries |
| Multi-vector index | "Caption + frame + transcript" | Qdrant collection with named vectors per representation |
| Temporal grounding | "When exactly did it happen" | Refining the (start, end) window for a query answer |
| Frame embedding | "Visual representation" | A vector embedding of a keyframe; used for scene-visual similarity |
| RRF fusion | "Reciprocal rank fusion" | Merge strategy across multiple ranked lists; a classic hybrid-retrieval trick |
| Counting hallucination | "Miscount" | Known failure mode of VLMs on "how many X" questions |
| ActivityNet-QA | "Video-QA benchmark" | Long-form video QA accuracy benchmark |

## 继续阅读 继续阅读

- [AI2 Molmo 2](https://allenai.org/blog/molmo2)开放VLM检查站
- [TimeLens (CVPR 2026)](https://github.com/TencentARC/TimeLens)时间定位
- [Gemini Video long-context](https://deepmind.google/technologies/gemini) 托管的参考
- [VideoDB](https://videodb.io)CRUD为视频API参考
- [Twelve Labs Marengo + Pegasus](https://www.twelvelabs.io)商业参考
- [TransNetV2](https://github.com/soCzech/TransNetV2)场景分区模型
- [PySceneDetect](https://github.com/Breakthrough/PySceneDetect)经典的开放替代品
- [ActivityNet-QA](https://arxiv.org/abs/1906.02467)参考评价基准
