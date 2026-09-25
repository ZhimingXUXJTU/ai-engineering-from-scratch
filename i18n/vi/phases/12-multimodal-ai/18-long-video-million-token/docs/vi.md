# Video dài hiểu tại Million-Token Context 百万Token 上下文的长视频理解

> Một video 4K 1 giờ với tốc độ 24 FPS, được dán và nhúng, tạo ra khoảng 60 triệu token. Một tập podcast 2 giờ được sao chép là 30.000 token. Một bộ phim đầy đủ Blu-ray, thậm chí được nén với sự tập hợp dữ dội, là hàng trăm ngàn token. Google's Gemini 1.5 (Tháng 3 năm 2024) mở ra thời đại này với một ngữ cảnh 10 triệu token, thực hiện thu hồi kim cáp trong một đống cỏ đáng tin cậy trong các video dài một giờ. LWM (Liu et al., tháng 2 năm 2024) cho thấy con đường quy mô của sự chú ý vòng. LongVILA và Video- XL đã tăng cường lượng tiêu thụ. VideoAgent đã đổi ngữ cảnh nguyên liệu cho thu hồi của đại lý. Mỗi cách tiếp cận là một sự đổi mới khác nhau về tính toán, nhớ lại và phức tạp kỹ thuật. Bài học này đọc cho chúng một bên nhau.

> **【中文解读】**1 小时 4K 视频可产生约6000.000 token,远超任何模型的上下文窗口──处理长视频有三条路径:(1) 暴力上下文(Gemini 1.5 的千万 token 上下文);(2) Ring Attention 跨设备分布式注意力;(3) Token 压缩(Video-XL 摘要);(4) 代码检查器 视频Agent 将视频在数据库查询) ⋅ Mỗi路径在计算量,召回率和工程复杂度上有不同取量.

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, needle-in-haystack simulator + agentic-retrieval router) | **语言:** Python（标准库，大海捞针模拟器 + Agent 检索路由器）
**Prerequisites:** Phase 12 · 17 (video temporal tokens) | **前置知识:** Phase 12 · 17（视频时间 token）
**Time:** ~180 minutes | **时间:** ~180 分钟

>  **【前置】**Học本节前请先掌握:Phase 12·17(视频时间代币与采样);Phase 10·34(Công tâm phân bố式注意力);Phase 14(Agent 检索,VideoAgent 思路)。本节是长视频理解的极限挑战:百万代币 上下文。
>  **【类比】**长视频理解 = "看完整部电影后能回答细节"──三种策略:(1) Gemini 1.5 路线 = 把整部电影硬塞进脑子(10M token 上下文,硬件怪兽);(2) Video-XL 路线 = 看完写摘要+检索原始片段(token 压缩);(3) VideoAgent 路线 = 当数据库查看,问题导向地拉取相关段段(Agent 检索) ~~

## Mục tiêu học tập

- Xét tổng số mã thông báo thị giác cho video hình dạng dài với FPS và tích hợp khác nhau.
  Trung ngữ翻译:计算不同 FPS 和池化配置 下长视频的视觉代币 总数──
- Giải thích ba con đường quy mô: bối cảnh thô (Gemini 1.5), chú ý vòng (LWM), nén token (LongVILA / Video-XL).
  Trung文翻译:解释三条扩展路径:暴力上下文(Gemini 1.5)、环形注意力(LWM)、token 压缩(LongVILA / Video-XL)。
- So sánh VLMs video trong bối cảnh nguyên liệu với VLMs video thu hồi bằng máy chủ (VideoAgent) về độ chính xác và độ trễ.
  Trung ngữ翻译:比较原始上下文视频 VLM 和 Agent 检索视频 VLM(VideoAgent) 在准确率和延迟上的表现──
- Thiết kế một thử nghiệm kim trong một đống cỏ cho một video 30 phút và đo lường hồi tưởng vào một phút cụ thể.
  Trung ngữ翻译:为30分钟视频设计大海捞针测试并测量特定分钟的召回率──

## Vấn đề  vấn đề giới thiệu

Một khung hình đơn của các bản vá kích thước Qwen2.5VL với độ phân giải bản địa là ~ 729 token. Với 3x3 tích hợp đó là 81 token mỗi khung hình. Một clip 30 phút với 1 FPS = 1800 khung hình = 145.800 token. Có thể thực hiện vào năm 2025 mở VLM, chặt chẽ. Ở 2 FPS, 291.600 token chỉ phù hợp với các bối cảnh lớn nhất.

> Qwen2.5-VL                                                                                                                                                                                                                                                            

Một bộ phim 2 giờ với 1 FPS là 583k token. Ngoài hầu hết các mô hình mở 2026; yêu cầu Gemini 2.5 Pro hoặc hợp tác mạnh mẽ hơn.

> 2 小时电影 1 FPS là 583k token── vượt quá khả năng mở rộng của hầu hết các mô hình năm 2026; cần Gemini 2.5 Pro hoặc tăng cường hơn.

Ba con đường leo lên đã xuất hiện.

> 出现了三条扩展路径──

## Khái niệm cốt lõi

> **【中文解读】**长视频理解(百万代币 级别) là thách thức phía trước của AI đa dạng.

> **【拓展：Gemini 1.5 Pro 的百万 token 上下文**Gemini 1.5 Pro  hỗ trợ 1M token 输入, có thể xử lý khoảng 1 giờ của video hoặc 1000+ trang tài liệu.


### Chặng đường 1: Bối cảnh thô (Gemini 1.5, Claude Opus)

Thả phần cứng vào vấn đề, mở rộng ngữ cảnh lên hàng triệu token, xử lý mọi thứ trong một lần đi trước.

> Sử dụng phần cứng khắc phục vấn đề bạo lực.

Gemini 1.5 Pro được tung ra với 1M token; Gemini 1.5 Ultra đến 10M; Gemini 2.5 Pro vào năm 2026 thực hiện nhiều giờ video đáng tin cậy.

> Gemini 1.5 Pro với token 1M  phát hành; Gemini 1.5 Ultra  mở rộng đến 10M; Gemini 2.5 Pro vào năm 2026 có thể xử lý đáng tin cậy số giờ video.

Kỹ thuật: một ứng dụng chú ý tùy chỉnh với hệ thống phân cấp bộ nhớ (đại địa phương + toàn cầu + hiếm) cộng với định tuyến chuyên gia MoE cho hiệu quả trong bối cảnh dài. Không được công bố chi tiết đầy đủ. Không nguồn mở.

> 工程实现: tự xác định cơ chế chú ý,带有内存层次(局部+全局+稀疏),加上 MoE 专家路由提升长上下文效率──未完整公开──非开源──

### Đường 2: Cảnh sát vòng (LWM, LongVILA)

Sự chú ý vòng phân phối các chuỗi dài giữa các thiết bị trong một "phòng" nơi mỗi thiết bị giữ một phần. Sự chú ý trên toàn bộ chuỗi xảy ra bởi mỗi thiết bị gửi phần của nó đến thứ tiếp theo trong một mô hình vòng, tính toán sự chú ý một phần, và tổng hợp.

> **【中文解读】**Ring Attention sẽ phân phối chuỗi dài trên nhiều thiết bị, mỗi thiết bị có một khối chuỗi, thông qua vòng hình giao thông tính toán toàn bộ chú ý.

LWM (Liu et al., 2024) đã đào tạo một mô hình ngữ cảnh 1M-token theo cách này. đào tạo tính toán các quy mô theo đường thẳng với ngữ cảnh, không phải hình vuông.

> LWM(Liu 等人,2024) sử dụng cách này đào tạo 1M token 上下文模型── đào tạo tính toán lượng theo dõi tăng trưởng tuyến tính dưới đây thay vì phân bổ chi phí chú ý thứ hai vào các thiết bị vòng hình──

LongVILA (arXiv:2408.10188) đã điều chỉnh mô hình cho VLMs. 1400-phần video với 192 token mỗi khung = 268k ngữ cảnh, được đào tạo với sự chú ý vòng qua song song đường 8-way.

> LongVILA sẽ điều chỉnh mô hình này để phù hợp với VLM──1400 视频, mỗi 192 token = 268k 上下文, thông qua 8 路并行环形注意力训练──

### Path 3: Compression token (Video-XL, LongVA)

Giá rẻ hơn so với bối cảnh thô: nén mạnh mẽ trước khi LLM thấy chuỗi.

> 比暴力上下文更便宜: trong LLM  xem trình tự trước khi tiến hành tăng cường nén.

Video-XL (arXiv:2409.14485) sử dụng một token tóm tắt trực quan: mỗi clip của các khung N tạo ra một token "tóm tắt" duy nhất tham gia trên N. Khi suy luận, LLM thấy một token tóm tắt mỗi clip, làm giảm đáng kể bối cảnh.

> Video-XL 使用视觉摘要代号: mỗi N 片段生成一个"摘要代号", để N 做注意.

LongVA mở rộng ngữ cảnh LLM từ 200k đến 2M với kỹ thuật "transai ngữ cảnh dài".

> LongVA sử dụng "长上下文迁移" kỹ thuật sẽ LLM 上下文 từ 200k 扩展到2M。

Việc nén token không được thu hồi tại các dấu thời gian cụ thể để có thể mở rộng. mô hình thường biết những gì đã xảy ra nhưng đôi khi bỏ lỡ khung chính xác.

> Các mã thông báo đánh áp để hy sinh thời gian cụ thể  tỷ lệ quay lại để đổi lấy khả năng mở rộng . mô hình thường biết điều gì đã xảy ra nhưng đôi khi sẽ sai quá chính xác .

### Path 4: Nhận lại đại lý (VideoAgent)

Đừng cung cấp toàn bộ video cho LLM. Thay vào đó, coi video như một cơ sở dữ liệu và sử dụng LLM để truy vấn nó.

> Đừng đưa toàn bộ video vào LLM. Thay vào đó, hãy đưa video vào cơ sở dữ liệu, sử dụng LLM để hỏi nó.

VideoAgent (arXiv:2403.10517):

> VideoAgent ((arXiv:2403.10517):

1. LLM đọc câu hỏi.
   > LLM 读取问题──
2. LLM yêu cầu một công cụ lấy lại các clip liên quan ("mở tôi các phân đoạn với một con mèo").
   > LLM 调用检索工具获取相关片段("给我看有猫的片段")
3. Công cụ trả lại phù hợp với các dấu thời gian clip.
   > 工具返回匹配的片段时间──
4. LLM đọc những đoạn băng đó qua VLM.
   > LLM 通过VLM 读取这些片段──
5. LLM soạn thảo câu trả lời hoặc hỏi các câu hỏi tiếp theo.
   > LLM 生成回答或发起后续查询.

Đây là mô hình LLM-as-agent được áp dụng cho video dài. Kết luận rẻ hơn (chỉ có đoạn clip có liên quan được mã hóa), kỹ thuật khó khăn hơn (huyết điểm về chất lượng truy xuất trở thành nút thắt).

> Đây là cách để LLM như một đại lý 模式 áp dụng đến dài video.

### Chỉ số chuẩn kim cương

Thử nghiệm ngữ cảnh dài tiêu chuẩn: chèn một dấu hiệu thị giác hoặc văn bản độc đáo tại một điểm ngẫu nhiên trong video, sau đó hỏi một câu hỏi đòi hỏi phải nhớ lại nó.

> 标准长上下文测试: Đưa vào vị trí video bất cứ hình ảnh hoặc văn bản nào, sau đó đưa ra yêu cầu nhớ lại các câu hỏi về nhãn hiệu này.

Metric: Recall@k qua chiều dài video và vị trí đánh dấu.

> Chỉ số:跨视频长度和标记位置的 Recall@k。

Gemini 2.5 Pro ghi điểm >99% nhớ lại trong video tối đa 90 phút. Các mô hình mở 72B (Qwen2.5-VL-72B, InternVL3-78B) ghi điểm ~85-90% sau 30 phút và giảm xuống hơn 60.

> Gemini 2.5 Pro trong 90 phút video trên tỷ lệ triệu hồi >99%── mở 72B 模型(Qwen2.5-VL-72B、InternVL3-78B) trong 30 phút khoảng 85-90%,60 phút sau khi trở lại──

VideoAgent có thể phù hợp hoặc đánh bại các mô hình trong bối cảnh nguyên liệu trong 2 giờ hoặc hơn vì việc lấy lại chạm vào kim cáp nếu công cụ tốt.

> VideoAgent có thể phù hợp hoặc vượt quá mô hình video gốc trong 2 giờ hoặc hơn, vì miễn là công cụ tốt, kiểm tra sẽ có thể đạt được mục tiêu.

### Đường nào để chọn

Để xem đoạn clip 15 phút ở độ chính xác biên giới: mở 72B + ngữ cảnh bản địa thường hoạt động. Chọn Qwen2.5-VL-72B.

> 15 分片段追求前沿准确率: 开放 72B + 原生上下文通常可行──选 Qwen2.5-VL-72B──

Đối với nội dung từ 30 phút đến 1 giờ: LongVILA hoặc Video-XL mở; Gemini 2.5 Pro đóng.

> 30 phút đến 1 giờ nội dung: mở nguồn với LongVILA hoặc Video-XL; đóng nguồn với Gemini 2.5 Pro。 chất lượng cửa rất quan trọng tiền tuyến cấp cần đóng nguồn。

Đối với nội dung 2 giờ trở lên: VideoAgent hoặc các mô hình tìm kiếm tương tự. Ngoài ra, tóm tắt thành các đoạn nhỏ hơn và cung cấp tóm tắt hàng đầu.

> 2 小时以上内容:VideoAgent hoặc kiểu tìm kiếm tương tự.

### Mô hình sản xuất năm 2026

Trong thực tế, các đường ống sản xuất video dài là lai:

> Trong thực tế, sản xuất cấp长视频管道 là một phương pháp hỗn hợp:

1. Thực hiện lấy mẫu FPS động + tích hợp dữ liệu tích cực trên toàn bộ video (được đại diện toàn cầu 100k token).
   Trung ngữ翻译:对整个视频运行动态 FPS 采样 + 激进池化(得到约100k token 的全局表示) ⋅
2. Nhận được một VLM 72B để xem tổng kết toàn cầu.
   Trung ngữ翻译:传入 72B VLM 生成全局摘要──
3. Nếu người dùng hỏi các câu hỏi chi tiết, hãy chạy tìm kiếm bằng cách sử dụng bản tóm tắt như một chỉ mục.
   Trung文翻译: Nếu người dùng hỏi chi tiết, sử dụng trích dẫn như một chỉ số vận hành Trưởng 检索。

Điều này kết hợp bối cảnh thô cho sự hiểu biết toàn cầu và tìm kiếm chi tiết địa phương.

> Điều này kết hợp với khả năng hiểu toàn diện và tìm kiếm chi tiết địa phương về bạo lực.

## Hãy sử dụng nó để thực hiện
```figure
mm-video-token-budget
```

## Sử dụng nó

`code/main.py`- Có thể là:

- Xét ngân sách token cho video từ 1 phút đến 3 giờ với FPS + hợp nhất khác nhau.
  Trung ngữ翻译:计算 1 分钟到 3 小时视频在不同 FPS + 池化下的代币 预算。
- Mô phỏng một cuộc chạy kim trong một đống cỏ: tiêm một dấu hiệu vào một dấu thời gian ngẫu nhiên, hỏi một câu hỏi, ghi lại.
  Trung文翻译:模拟大海捞针测试: 在随机时间注入标记,提问,评分召回率──
- Bao gồm một bộ mô phỏng bộ định tuyến lấy lại cơ quan chọn các clip cụ thể để cung cấp cho một VLM dòng chảy xuống.
  Trung文翻译:包含一个代理 检索路由模拟器, chọn cụ thể片段给下游 VLM。

Hãy kiểm tra bảng ngân sách và cảm nhận được khoảng cách ở quy mô.

> 运行预算表, cảm nhận sự khác biệt về quy mô.

## Chuyển nó đi.

Bài học này sẽ mang lại kết quả `outputs/skill-long-video-strategy-planner.md`. Với thời gian video và độ phức tạp của truy vấn, nó chọn giữa ngữ cảnh thô, nén và tìm kiếm cơ quan, và tính toán kỳ vọng độ trễ + chất lượng.

> 本课产 出 `outputs/skill-long-video-strategy-planner.md`❖ cho thời gian video và độ phức tạp của truy vấn, nó là trong bạo lực ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞

## Tập luyện bài tập

1. Một bài giảng 45 phút với 1 FPS, 81 token mỗi khung. Tổng số token? phù hợp với các ngữ cảnh của mô hình nào? 45 分钟讲座,1 FPS, mỗi 81 token。 tổng số token?

2. Thiết kế một con kim trong một đống cỏ: vào phút nào bạn tiêm dấu hiệu, và định dạng truy vấn chính xác là gì?

3. So sánh ngữ cảnh thô Qwen2.5-VL-72B (80k ngữ cảnh) với VideoAgent (Claude 3.5 + lấy lại) trên một video 1 giờ.

4. Tự động của sự chú ý nhớ cân bằng đường thẳng theo chiều dài chuỗi và đường thẳng trong số lượng thiết bị. Giải thích tại sao và những gì thất bại nếu bạn bỏ ra giai đoạn quay vòng.

5. Đọc Gemini 1.5 Phần 5 về kim cáp trong một đống cỏ. Bài báo tìm thấy gì về việc thu hồi ở giới hạn mã thông báo 1M vs 10M?

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|------------------------|---------|
| Brute context | "Just more tokens" 暴力上下文 | Scale LLM context to millions of tokens; process everything in one pass 将 LLM 上下文扩展到百万 token，一次前向传播处理全部内容 | |
| Ring attention | "LWM-style parallel" 环形注意力 | Distributed attention pattern where each device holds a chunk and rotates 分布式注意力模式，每个设备持有一块并在环中轮转 | |
| Token compression | "Summary tokens" 摘要 token | Reduce per-clip tokens via a learned compressor before the LLM LLM 前通过学习型压缩器减少每片段 token 数 | |
| Needle-in-haystack | "NIH test" 大海捞针测试 | Insert a unique marker at a random point, ask model to recall it at test time 在随机位置插入唯一标记，测试时要求模型回忆 | |
| Agentic retrieval | "LLM as query planner" Agent 检索 | LLM asks a retrieval tool for relevant clips, reads them via a VLM, composes answer LLM 调用检索工具获取相关片段，通过 VLM 阅读并生成回答 | |
| VideoAgent | "Retrieval pattern for video" 视频检索模式 | Canonical agentic-retrieval design: question -> tool -> clip -> answer 经典 Agent 检索设计：问题→工具→片段→回答 | |

## Xem thêm 延伸阅读

- [Gemini Team — Gemini 1.5 (arXiv:2403.05530)](https://arxiv.org/abs/2403.05530)
- [Liu et al. — LWM / RingAttention (arXiv:2402.08268)](https://arxiv.org/abs/2402.08268)
- [Xue et al. — LongVILA (arXiv:2408.10188)](https://arxiv.org/abs/2408.10188)
- [Shu et al. — Video-XL (arXiv:2409.14485)](https://arxiv.org/abs/2409.14485)
- [Wang et al. — VideoAgent (arXiv:2403.10517)](https://arxiv.org/abs/2403.10517)
