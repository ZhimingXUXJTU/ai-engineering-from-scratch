# Multimodal RAG và Cross-Modal Retrieval 

> Tài liệu RAG của thị giác là một mảnh. RAG đa phương pháp sản xuất mở rộng hơn  thu thập thông qua văn bản, hình ảnh, âm thanh và video cho các dòng công việc như lập kế hoạch chuyến đi ("đặt cho tôi một bữa ăn uống vegan yên tĩnh với ánh sáng tự nhiên"), phân loại y tế ("những vết thương nào phù hợp với bức ảnh này + những ghi chú này"), thương mại điện tử ("những trang phục tương tự như selfie này, kích thước của tôi"), và dịch vụ thực địa ("chẩn đoán âm thanh động cơ này cộng với ảnh của bộ phận"). Ba cuộc khảo sát năm 2025  Abootorabi et al., Mei et al., Zhao et al.  hợp pháp hóa các phụ vấn đề: thu hồi đa phương thức, hợp nhất thu hồi, hạ tầng sản xuất, đánh giá đa phương thức. Bài học này đọc các cuộc khảo sát và thiết kế một đường ống sản xuất.

> **【中文解读】**Các RAG sản xuất nhiều mô hình vượt qua một hồ sơ kiểm tra đơn ỏi cần phải trải qua văn bản, hình ảnh, âm thanh, video kiểm tra, sử dụng trong quy hoạch du lịch, y tế phân诊, điện thương mại khuyến cáo, dịch vụ thực địa, vv.

**Type:** Build
**Languages:** Python (stdlib, cross-modal retriever with fusion + grounded generator)
**Prerequisites:** Phase 12 · 23 (ColPali), Phase 11 (RAG basics)
**Time:** ~180 minutes

>  **【前置】**学本节前请先掌握:Phase 12·23(ColPali 视觉文档 RAG) 、Phase 11·14-17(RAG 检索/融合/重排) 、Phase 12·02(CLIP 跨模态对齐) ⋅本节是ColPali 扩展多种模态一起检索+融合──
>  **【类比】**多模态 RAG = "全科医生诊断"―― bệnh nhân nói"我胸痛" (文本) + 给你看心电图 (图像) + 让你听心跳录音 (录音) 音频) ∼医生要同时检索医学文献 (图文) ∼心电图案库 (图像) ∼心跳声纹库 (音频) ∼融合多源信息后给出诊断――融合策略:分数融合 = 让各源分分加权;注意力融合 = 专业融合 = 让 LLM 自己决定哪源重要;MoE 融合 = 不同专家处理不同模态。

## Mục tiêu học tập

- Thiết kế truy xuất đa phương thức: văn bản → hình ảnh, hình ảnh → văn bản, âm thanh → video, vv
  中文翻译:设计跨模态检索:文本→图像、图像→文本、音频→视频等──
- So sánh ba chiến lược hợp nhất: hợp nhất điểm, hợp nhất dựa trên sự chú ý, hợp nhất MoE.
  Trung ngữ翻译:比较三种融合策略:分数融合、注意力融合、MoE 融合──
- Giải thích việc đặt nền thế hệ: "đọc nguồn của bạn" trông như thế nào khi các nguồn là một sự pha trộn của các phương pháp.
  Trung文翻译:解释生成接地:当来源是多种模态混合时,"引用来源"是什么样子──
- Tên gọi ba cuộc khảo sát RAG đa phương pháp theo quy định năm 2025 và phân loại phân loại phụ của họ.
  Trung ngữ翻译:列举 2025 年三篇经典多模态 RAG 综述及其子问题分类──

## Vấn đề  vấn đề giới thiệu

RAG một cách đơn phương là một mô hình được giải quyết: đặt truy vấn, đặt các khối, lấy lại, mọi thứ vào LLM. RAG đa phương pháp đòi hỏi:

> 单模态 RAG 是已解决的模式:嵌入查询,,嵌入块、检索、塞入 LLM──多模态 RAG 需要:

1. Nhiều đầu lấy (mỗi phương thức cần được nhúng vào một không gian tương thích).
   Trung ngữ翻译:多个检索头 (多个检索头)
2. Kết quả thu hồi kết hợp trên các phương pháp.
   Trung ngữ翻译:跨模态检索结果的融合──
3. Việc tạo ra đất mà trích dẫn các nguồn qua các phương thức.
   Trung文翻译:跨模态引用来源的生成接地──
4. Các số liệu đánh giá bao gồm tín hiệu qua phương tiện.
   Trung ngữ翻译:覆盖跨模态信号的评估指标.

Các cuộc khảo sát năm 2025 đều đến với cùng một phân loại.

> Năm 2025 tổng thể đều có được các phân loại giống nhau.

## Khái niệm cốt lõi

> **【中文解读】**跨模态 RAG  mở rộng văn bản truyền thống RAG, hỗ trợ nhiều mô hình tìm kiếm và tạo: có thể sử dụng văn bản tìm kiếm hình ảnh, sử dụng hình ảnh tìm kiếm văn bản, hoặc hỗn hợp tìm kiếm nhiều mô hình tài liệu.

> **【拓展：多模态 RAG 的应用**Nhiều mô hình RAG trong lĩnh vực y tế, kinh doanh, kinh doanh, và các lĩnh vực khác có giá trị rất lớn.


### Khám phá liên hợp

Nhận lại các tài liệu của chế độ B khi đưa ra truy vấn của chế độ A. Ba mô hình:

> 给定模态 A 的查询,检索模态 B 的文档──三种模式:

1. Không gian nhúng chung. CLIP và CLAP tạo ra văn bản + hình ảnh / văn bản + âm thanh nhúng trong không gian chung. Sự tương đồng của cosine trên các phương pháp hoạt động trực tiếp.
   Trung ngữ翻译:共享嵌入空间──CLIP 和 CLAP 在共享空间产生文本+图像/文本+音频嵌入──跨模态余弦相似度直接有效──限于CLIP 训练过的配对──

2. Bộ mã hóa tính năng tính năng (per-modality encoder + translation). Bộ mã hóa văn bản + bộ mã hóa hình ảnh + mô-đun dịch thuật nhỏ lập bản đồ giữa không gian. Sen2Sen của Gupta et al. và các thiết kế khác năm 2024.
   Trung ngữ翻译:每模态独立编码器 + 翻译――文本编码器 + 图像编码器 + 在空间间映射的小翻译模块──Sen2Sen等 2024年设计──灵活但增加复杂度──

3. VLM làm mã hóa. sử dụng các trạng thái ẩn của VLM như đại diện lấy lại. bất kỳ phương thức nào mà VLM hỗ trợ hoạt động. chất lượng cao hơn, đắt hơn.
   Trung文翻译:VLM 作为编码器──使用VLM 隐藏状态作为检索表示──VLM 支持的任何模态都可用──质量更高,成本更高──

Tùy chọn: CLIP / SigLIP 2 cho văn bản + hình ảnh; CLAP cho văn bản + âm thanh; VLM-họa-thường cho cross-modal ở chất lượng biên giới.

> 选择建议:文本+图像用 CLIP/SigLIP 2;文本+音频用 CLAP;前沿质量跨模态用 VLM 隐藏状态──

### Chiến lược sáp nhập

Bạn đã lấy lại 10 kết quả: 5 hình ảnh, 3 đoạn văn bản, 2 đoạn âm thanh. Làm thế nào để sáp nhập?

> Bạn đã tìm kiếm 10 kết quả: 5 张图像, 3 段文本, 2 段音频片段.

Kết hợp điểm số (tô nhất). Mỗi phương thức có bộ thu hồi riêng của mình, mỗi phương thức trả lại điểm số.

> 分数融合 (最便宜) ⋅ Mỗi mô hình có bộ kiểm tra riêng, mỗi mô hình trả lại分数──

Phối hợp dựa trên sự chú ý, kết hợp tất cả các mục được lấy lại, để một mạng lưới chú ý nhỏ cân nặng chúng.

> 注意力融合──拼接所有检索项,让小型注意力网络加权──需要训练──

Phối hợp MoE. Gating mạng đường đến các chuyên gia cụ thể về phương pháp. Các loại truy vấn khác nhau đường khác nhau  một câu hỏi trực quan cân nặng hình ảnh cao hơn.

> MoE 融合──门控网络路由到模态特定专家──不同查询类型路由不同视觉问题给图像更高权重──

Tiêu chuẩn sản xuất: kết hợp điểm số với một sự thiên vị nhẹ đối với phương thức thống trị của truy vấn. Tăng lên MoE nếu A / B cho thấy chiến thắng rõ ràng trên miền của bạn.

> 生产默认:分数融合 + nhẹ định vị đối với các mô hình quản lý truy vấn. Nếu A/B 测试 trong lĩnh vực của bạn cho thấy ưu điểm rõ ràng, nâng cấp lên MoE.

> **【中文解读】**三种融合策略:(1) 分数融合各模态检索器分别归归化分数后加权求和,最简单;(2) 注意力融合小网络学习权重,需要训练;(3) MoE 融合门控网络按查询类型路由到不同专家──生产默认是分数融合 + 微偏置对查询主导模态的微偏置──

> **【拓展：多模态 RAG 的跨模态检索基础】**跨模态检索有三种模式:(1) 共享嵌入空间(CLIP/SigLIP 2 用图文,CLAP 用文本-音频);(2) 每模态独立编码器 + 翻译模块;(3) 用 VLM 隐藏状态作为检索表示;;选择建议:文本+图像用 CLIP/SigLIP 2,文本+音频用 CLAP,跨模态前沿质量用 VLM 隐藏状态;;

### Địa đất thế hệ

LLM nên nêu ra mục nào được thu hồi đã thúc đẩy mỗi yêu cầu.

> LLM 应引用哪个检索项驱动了每个声明. Đối với nhiều mô hình:

- Nguồn văn bản: trích dẫn tiêu chuẩn `[1]`- Tôi không biết.
  Trung ngữ翻译:文本来源:标准引用 `[1]`
- Nguồn hình ảnh: `[img 3]`với một đoạn văn ngắn.
  Trung ngữ翻译:图像来源:`[img 3]`附简短描述──
- Âm thanh: `[audio 2 at 0:34]`- Tôi không biết.
  Trung ngữ翻译:音频来源:`[audio 2 at 0:34]`

Trình tạo với dữ liệu có ý thức về nền tảng: mỗi tuyên bố trong mục tiêu đào tạo được dán nhãn với chỉ số nguồn.

> Sử dụng máy tạo dữ liệu cảm nhận: mỗi tuyên bố trong mục tiêu đào tạo đều được đánh dấu nguồn chỉ dẫn.

### Các cuộc khảo sát năm 2025

Abootorabi et al. (arXiv:2502.08826, "Hãy hỏi trong bất kỳ modality"): phân loại cho RAG đa phương thức. Bao gồm thu hồi, hợp nhất, sản xuất.

> Abootorabi 等人:多模态 RAG 分类法──覆盖检索、融合、生成──覆盖最广──

Mei et al. (arXiv:2504.08748, "A Survey of Multimodal RAG"): tập trung vào các tiêu chuẩn phụ nhiệm vụ và chế độ thất bại. hữu ích cho thiết kế đánh giá.

> Mei 等人: tập trung nhiệm vụ基准和失败模式――对评估设计有用――

Zhao et al. (arXiv:2503.18016): khảo sát tập trung vào tầm nhìn.

> Zhao 等人:聚焦视觉的综述──对 ColPali 系列工作覆盖深入──

Đọc cả ba sẽ cho bạn những thông tin mới nhất vào mùa xuân năm 2025.

> 阅读全部三篇 可获得2025年春最前沿状态――大多数子问题仍开放――

### MuRAG  bài báo cơ bản

MuRAG (Chen et al., 2022) là RAG đa phương thức đầu tiên. lấy hình ảnh + văn bản từ KB đa phương thức, tạo ra câu trả lời.

> MuRAG là RAG đa hình thức đầu tiên. Từ nhiều hình thức kiến thức kiểm tra hình ảnh + văn bản, tạo câu trả lời.

### Ví dụ về kế hoạch hành trình sản xuất

Câu hỏi: "Hãy tìm cho tôi một bữa ăn sáng vegan yên tĩnh với ánh sáng tự nhiên".

>  Thắc mắc: "Hãy cho tôi tìm một bữa sáng bình tĩnh, có ánh sáng tự nhiên".

Đường ống:

> 管道:

1. Tháo gỡ truy vấn. "quiet" → từ khóa âm thanh / đánh giá; "vegan brunch" → mục menu; "natural light" → tính năng hình ảnh.
   中文翻译:分解查询──"安静"→音频/评论关键词;"纯素早午餐"→菜单项;"自然光"→图像特征──
2. Thu thập theo phương thức:
   Trung文翻译:按模态检索:
   - Tìm kiếm văn bản trong đánh giá: "Bunch vegan, bầu không khí yên tĩnh".
     Trung ngữ翻译:评论文本检索:"纯素早午餐,安静氛围"。
   - Khám ảnh trên ảnh nhà hàng: "Ánh sáng tự nhiên, không khí".
     Trung ngữ翻译:餐厅照片图像检索:"自然光,通风"──
   - Khám phá âm thanh trên các đoạn âm thanh xung quanh: "Nuyết decibel thấp, không có âm nhạc".
     Trung ngữ翻译:环境声音频检索:"低分贝,无音乐"──
3. Mỗi nhà hàng đều có điểm số hỗn hợp.
   Trung ngữ翻译:融合分数──每个餐厅有综合分数──
4. Top-k nhà hàng → VLM máy phát điện với tất cả các bằng chứng → trả lời với trích dẫn.
   Trung文翻译:Top-k 餐厅 → VLM 生成器(附所有证据)→ 带引用的回答──

Điều này vượt xa text-RAG. Mỗi phương thức thêm tín hiệu mà văn bản một mình bỏ lỡ.

> Đây là một cách khác biệt với các RAG văn bản. Mỗi mô hình được thêm vào chỉ dựa trên các tín hiệu của các bài viết đã bị bỏ qua.

### Máy vận hành đa phương tiện RAG

Multi-hop: nếu lần tìm kiếm đầu tiên không trả lời tự tin cao, LLM lại định dạng lại và lấy lại một lần nữa.

> 多跳: Nếu lần đầu tiên kiểm tra không trả lại trả lời,LLM 重新表述并再次检索──Phase 14 của Agent RAG 模式在此适用── ví dụ:

- Khôi phục top-10 đầu tiên → LLM yêu cầu "quá tiếng ồn, lọc cho <40 dB" → khôi phục lại.
  Trung文翻译:检索初始 top-10 → LLM 提问"太杂,过 <40 分贝" → 重新检索。
- Khôi phục hình ảnh → LLM thấy một có một menu → lấy lại văn bản menu → trả lời.
  Trung văn翻译:检索图像 → LLM 看到一张有菜单 → 检索菜单文本 → 回答。

Thêm sự phức tạp nhưng xử lý các truy vấn mà chỉ lấy lại một lần không thể.

> 增加复杂性但能处理单次检查无法处理的查询――

### Đánh giá

Việc đánh giá qua phương thức vẫn chưa trưởng thành.

> 跨模态评估 vẫn chưa trưởng thành.

- Recall@k theo từng phương pháp.
  Trung ngữ翻译:每模态的 Recall@k。
- Độ chính xác top-k hợp nhất.
  Trung ngữ翻译:融合后的顶-k准确率──
- Sự hài lòng của người.
  Trung ngữ翻译:人工评判的端到端满意度.
- Đặc biệt về nhiệm vụ (bản đặt phòng hoàn thành, mua hàng được thực hiện).
  Trung ngữ翻译:任务特定指标(完成的预订、达成的购买)

Không có điểm chuẩn tiêu chuẩn nào bao gồm tất cả các phương pháp.

> Không có tiêu chuẩn về các mô hình.

## Hãy sử dụng nó để thực hiện
```figure
contrastive-matrix
```

## Sử dụng nó

`code/main.py`- Có thể là:

- Ba máy lấy lại giả (text, image, audio) hoạt động trên một tập hợp chung của các nhà hàng.
  Trung ngữ翻译:三个模拟检索器 (三模拟检索器)
- Kết hợp điểm số kết hợp điểm số modality với trọng lượng có thể cấu hình.
  Trung ngữ翻译:用可配置权重组合模态分数的分数融合──
- Một cái cột máy phát ra câu trả lời cuối cùng với các trích dẫn.
  Trung文翻译:输出带引用最终回答的生成器──
- Một vòng lặp đơn giản của các nhà quản lý để định dạng lại câu hỏi nếu sự tin tưởng thấp.
  Trung ngữ翻译:置信度低时重新表述查询的简单代理循环──

## Chuyển nó đi.

Bài học này sẽ mang lại kết quả `outputs/skill-multimodal-rag-designer.md`Với một đặc điểm sản phẩm với một dòng truy vấn đa phương thức, thiết kế máy thu hồi, hợp nhất, máy phát và đánh giá.

> 本课产 出 `outputs/skill-multimodal-rag-designer.md` Định dạng các quy định sản phẩm, thiết kế các bộ kiểm tra, chiến lược kết hợp, máy phát triển và các quy trình đánh giá của dòng truy vấn.

## Tập luyện bài tập

1. Đề xuất một RAG đa phương pháp y tế-triang: truy vấn = ảnh chấn thương + triệu chứng văn bản.

2. Phối hợp điểm là một số tiền cân nặng đơn giản. Nó có chế độ thất bại nào mà Phối hợp MoE tránh? 分数融合是简单的加权求和.

3. Đọc phân loại của Abootorabi et al. (Gụ phần 3). Ba phụ vấn đề hợp pháp là gì và làm thế nào để họ được lập bản đồ cho sản phẩm bạn chọn?

4. Thiết kế một mô hình đánh giá cho một RAG đa phương thức du lịch. Những số liệu nào bao gồm thu hồi hình ảnh, thu hồi âm thanh và tính chính xác hợp nhất?

5. Agentic multi-hop RAG có một thuế độ trễ mỗi chuyến đi về lại. Tại khó khăn truy vấn nào tăng độ chính xác biện minh cho độ trễ? Agent 多跳 RAG 每轮有延迟开销――在什么查询复杂度下,准确率提升值得延迟代价?

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|------------------------|---------|
| Cross-modal retrieval | "Query one modality, retrieve another" 跨模态检索 | Text query retrieves images; image query retrieves text; requires a shared space or translator 文本查询检索图像；图像查询检索文本；需要共享空间或翻译器 | |
| Score fusion | "Combine scores" 分数融合 | Weighted sum of per-modality retrieval scores; simplest fusion 各模态检索分数的加权和；最简单的融合方式 | |
| MoE fusion | "Modality-routed experts" 混合专家融合 | Gating network picks which modality's scores to trust per query 门控网络按查询选择信任哪个模态的分数 | |
| Grounded generation | "Cite your sources" 接地生成 | Each claim in the answer tagged with the source index 回答中的每个声明都标注来源索引 | |
| MuRAG | "First multimodal RAG" 首个多模态 RAG | 2022 paper that established the multimodal RAG pattern 2022 年建立多模态 RAG 模式的论文 | |
| Agentic multi-hop | "Reformulate and retry" Agent 多跳 | LLM re-queries retrievers when first-pass confidence is low 首次检索置信度低时 LLM 重新查询检索器 | |

## Xem thêm 延伸阅读

- [Abootorabi et al. — Ask in Any Modality (arXiv:2502.08826)](https://arxiv.org/abs/2502.08826)
- [Mei et al. — A Survey of Multimodal RAG (arXiv:2504.08748)](https://arxiv.org/abs/2504.08748)
- [Zhao et al. — Vision RAG Survey (arXiv:2503.18016)](https://arxiv.org/abs/2503.18016)
- [Chen et al. — MuRAG (arXiv:2210.02928)](https://arxiv.org/abs/2210.02928)
- [Liu et al. — REACT (arXiv:2301.10382)](https://arxiv.org/abs/2301.10382)
