# Thỏa thuận và thương lượng

> Các đại lý đàm phán tài nguyên, giá cả, phân bổ nhiệm vụ và các điều khoản. Mức chuẩn 2026 rõ ràng: NegotiationArena (arXiv:2402.05863) cho thấy LLM có thể cải thiện lợi nhuận ~ 20% thông qua thao túng cá nhân ("sự tuyệt vọng"); "Mắt khả năng đàm phán" (arXiv:2402.15813) cho thấy người mua khó hơn người bán và quy mô không giúp  họ **OG-Narrator**(tạo sản xuất đề nghị quyết định + người kể về LLM) đẩy tỷ lệ giao dịch từ 26,67% lên 88.88%; Cuộc thi đàm phán tự trị quy mô lớn (arXiv:2503.06416) đã tiến hành khoảng 180k đàm phán và phát hiện ra rằng**chain-of-thought-concealing**Bhattacharya et al. 2025 trên Harvard Negotiation Project metrics xếp hạng Llama-3 hiệu quả nhất, Claude-3 hung hăng nhất, GPT-4 công bằng nhất. Bài học này thực hiện Công ước Net Protocol (đạo của FIPA, Bài học 02), dây một người mua / bán theo kiểu LLM, chạy phân hủy theo kiểu OG-Narrator, và đo lường tỷ lệ giao dịch thay đổi như thế nào với mỗi lựa chọn cấu trúc.

> **【中文解读】**Phần này giới thiệu các chiến lược đàm phán trong phân phối nguồn lực và phân phối nhiệm vụ.

> **【拓展：negotiation bargaining→具体应用】**协商和讨价还价 là cơ chế cốt lõi của phân phối nguồn lực của nhiều đại lý.


**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib) | **语言:** Python（标准库）
**Prerequisites:** Phase 16 · 02 (FIPA-ACL Heritage), Phase 16 · 09 (Parallel Swarm Networks) | **前置知识:** Phase 16 · 02（FIPA-ACL 遗产），Phase 16 · 09（并行群体网络）

>  **【前置】**Học本节前请先掌握:Phase 16·02(FIPA Contract Net) Phase 16·09(Swarm) 、博论基础(纳什均衡) Công viên 协商 = 资源/价格/任务分配的讨价还价──
>  **【类比】**Agent 协商 = "二手市场砍价"──LLM 通过人操操(装穷)能多 20%;隐藏推理过程的 Agent 赢对手看不到你的底线──OG-Narrator 把协商拆为"确定性提议生成"+"LLM 叙述",交易率 26%→89%──模型差异:Llama-3 最有效、Claude-3 强势、GPT-4公平 最选即选择风格──
**Time:** ~75 minutes | **时间:** ~75 分钟

##                                                                                                                                                                                                                                                               

Hai đại lý cần phải đồng ý về một mức giá. Được để lại cho chính họ với các lời khuyên ngôn ngữ thuần túy, LLM 2024-2026 sẽ kết thúc các giao dịch với tỷ lệ đáng ngạc nhiên thấp (~ 27% trên các giao dịch có tham số chặt chẽ trong arXiv:2402.15813).

> Trong năm 2024-2026 tỷ lệ giao dịch LLM của năm 2024-2026 là rất thấp.

Vấn đề gốc là LLM kết hợp hai công việc  quyết định đề nghị và kể lại đề nghị. OG-Narrator tách ra những điều này: một nhà sản xuất đề nghị xác định tính toán các chuyển động số; LLM chỉ kể lại. tỷ lệ giao dịch nhảy lên ~ 89%.

> 根本问题是LLM 混了两个任务决定报价和叙述报价――OG-Narrator 将两者分开:确定性报价生成器计算数字变动;LLM chỉ chịu trách nhiệm về叙述――成交率跃升至约89%――

Điều này phản ánh một phát hiện đa đại lý cổ điển: giải quyết cơ chế từ lớp truyền thông thắng. Phương pháp giao dịch mạng (FIPA, 1996; Smith, 1980) là cơ chế thị trường nhiệm vụ tham chiếu.

> Điều này phản ánh một cơ chế đa tác giả cổ điển: sẽ cơ chế và giao tiếp tầng giải là con đường chiến thắng.

## Khái niệm cốt lõi

### Hợp đồng Net, trong một đoạn

Nghị định thư lưới hợp đồng năm 1980 của Smith: a **manager**phát sóng một **call for proposals (cfp)****bidders**trả lời với **propose**tin nhắn chứa các đề nghị của họ; người quản lý chọn một người chiến thắng và gửi **accept-proposal**cho người chiến thắng và **reject-proposal**Người thắng sẽ làm công việc.**refuse**FIPA đã hợp pháp hóa điều này như:`fipa-contract-net`giao thức tương tác.

> Hiệp định hợp đồng của Smith năm 1980:**管理者**广播**提案请求（cfp）**-**投标人**回复包含其报价的**提案**消息; quản trị viên chọn người chiến thắng并向 người chiến thắng发送**接受提案**,向落选者发送**拒绝提案**❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖**拒绝**(投标人拒绝提案)  FIPA 将其编码为`fipa-contract-net`交互协议――

### Tại sao OG-Narrator thắng

"Thử nghiệm khả năng thương lượng của các mô hình ngôn ngữ" (arXiv:2402.15813) lưu ý rằng:

> "衡量语言模型的议价能力" (ArXiv:2402.15813) quan sát:

- LLM thường vi phạm các quy tắc thương lượng (sự cung cấp với giá vô nghĩa, phớt lờ ZOPA của bên kia).
  Trung ngữ翻译:LLM 经常违反议价规则 ((以无意义的价格报价,忽略对方的ZOPA) 
- Họ được neo kém (tự chấp nhận các đề nghị đầu tiên xấu; phản đề nghị với số tiền biểu tượng thay vì chiến lược).
  Trung ngữ翻译:定效差 ((( chấp nhận giá đầu vòng tồi tệ; 定效差; 定效差; 定效差; 定效差; 定效差; 定效差; 定效差; 定效差; 定效差; 定效差; 定效差; 定效差; 定效差; 定效差; 定效差; 定效差; 定效差; 定效差; 定效差; 定效差; 定效差; 定效差; 定效差; 定效差; 定价; 定价; 定价; 定价; 定价; 定价; 定价; 定价; 定价; 定价; 定价; 定价; 定价; 定价; 定价; 定价; 定价; 定价; 定价; 定价; 定价; 定价; 定价; 定价;
- Chỉ riêng quy mô không khắc phục được những điều này. Các mô hình lớn hơn làm cho ngôn ngữ có khả năng tin cậy hơn với sai lầm chiến lược tương tự.
  Trung ngữ: Chỉ bằng quy mô không thể giải quyết được những vấn đề này.

Sự phân hủy của OG-Narrator:

```
           ┌──────────────────┐        ┌──────────────────┐
  state  → │ offer generator  │ price → │  LLM narrator    │ → message
           │  (deterministic) │        │  (writes the     │
           │                  │        │   human-style    │
           └──────────────────┘        │   accompaniment) │
                                       └──────────────────┘
```

Các nhà sản xuất giá cả là một chiến lược đàm phán cổ điển: một mô hình thương lượng Rubinstein, một chiến lược Zeuthen, hoặc một cái nhìn đơn giản về giá. LLM kể lại. Thông điệp chứa giá xác định và khung ngôn ngữ tự nhiên.

Giá giao dịch tăng vì:
- Giá vẫn ở trong khu vực thương lượng.
- Cây neo là chiến lược, không phải cảm xúc.
- LLM làm những gì nó giỏi: viết.

> 成交率 tăng vì:
> - Giá duy trì trong khu vực giá议间.
> - 点是战略性的,而不是情绪化的.
> - LLM làm nó tốt: viết作.

### Các kết quả đàm phán

ArXiv:2402.05863 cung cấp điểm chuẩn theo luật.

> ArXiv:2402.05863  cung cấp quy tắc cơ sở:

- LLM có thể cải thiện lợi nhuận ~ 20% bằng cách áp dụng personas ("Tôi tuyệt vọng bán điều này vào thứ Sáu")  thao túng cá nhân là một chiến thuật thực sự.
  Trung ngữ:LLM có thể tăng lợi nhuận bằng cách sử dụng nhân vật khoảng 20% (I urgent need to sell this on this周五前).
- Các nhân viên công bằng/ hợp tác được khai thác bởi những người đối kháng; quốc phòng đòi hỏi phải có sự phản đối rõ ràng.
  Trung ngữ翻译:公平/合作的代理被对抗性代理利用;防御需要显然的反向姿态──
- Các cặp đối xứng hội tụ với kết quả không công bằng trên khoảng 40% các kịch bản chuẩn.
  Trung ngữ:  đối với đối với được nhận được kết quả không công bằng trên cơ sở của khoảng 40% trường hợp.

Đây không phải là "LLC là những người đàm phán xấu". Đó là "LLC đàm phán quá nhiều như con người, bao gồm cả các phần khai thác".

> Đây không phải là "LLM là một nhà đàm phán tồi tệ" mà là "hình thức đàm phán của LLM quá giống con người, bao gồm cả những phần có thể được sử dụng".

### Sự che giấu chuỗi suy nghĩ

Cuộc thi đàm phán tự trị quy mô lớn (arXiv:2503.06416) đã tiến hành khoảng 180k đàm phán trên nhiều chiến lược LLM. Những người chiến thắng che giấu lý luận của họ từ đối tác:

> Cuộc thi tự trị lớn được tổ chức trên nhiều chiến lược LLM đã được tổ chức khoảng 180.000 lần.

- Nếu một đại lý in "Tôi chỉ đi đến$75; my reservation price is $70" vào một tấm cọp được nhìn thấy công khai, đối thủ đọc nó.
  Nếu đại lý sẽ "Tôi chỉ đi đến"$75；我的保留价是 $70" in lên bản thảo có thể nhìn thấy công khai, đối thủ sẽ đọc nó.
- Người chiến thắng tính toán chiến lược riêng tư; kênh xuất phát chỉ chứa lời đề nghị và câu chuyện tối thiểu cần thiết.
  Trung ngữ翻译:获胜者私下计算策略;输出通道只包含报价和最低限的叙述──

Đây là một hồi âm 2026 của lý thuyết trò chơi cổ điển (Aumann 1976 về tính hợp lý và thông tin): tiết lộ chi phí định giá cá nhân của bạn trả tiền. LLM không trực giác điều này và vui vẻ gõ những dự bị của họ trong các dấu vết lý luận trở nên hiển thị cho đối tác.

> Đây là bài viết kinh điển của Aumann 1976  Về lý thuyết và thông tin) vào năm 2026 phản hồi: Khám phá giá trị cá nhân sẽ mất lợi nhuận. LLM không nhận ra điều này trực tiếp, vui lòng trong dấu vết của suy luận nhập vào giá lưu giữ, những dấu vết này đối với đối thủ có thể thấy.

Công nghệ lấy đi: tách ngữ cảnh riêng của scratchpad từ ngữ cảnh thông điệp công cộng. Không tùy chọn.

> 工程要点:将私人草稿本上下文与公开消息上下文分离──

### Bhattacharya et al. 2025  bảng xếp hạng mô hình

Về các chỉ số của Dự án đàm phán Harvard (chủ nghĩa đàm phán, tôn trọng BATNA, tương ứng lợi ích):

> Trong chương trình đàm phán Harvard, các mục tiêu trên:

- **Llama-3**là hiệu quả nhất trong việc đánh giá thương mại (transaction rate + payoff).
  Trung ngữ翻译:**Llama-3**Trong lĩnh vực giao dịch đạt được hiệu quả nhất (%)
- **Claude-3**là nhà đàm phán hung hăng nhất (những chiếc neo cao, những nhượng bộ muộn).
  Trung ngữ翻译:**Claude-3**Là người đàm phán có tính tấn công nhất.
- **GPT-4**là công bằng nhất (sự khác biệt nhỏ nhất trong thanh toán giữa các cặp).
  Trung ngữ翻译:**GPT-4**最公平 (最公平) 跨配对的收益方差最小)

Đây là một bức ảnh chụp năm 2025. Điểm không phải là mô hình nào thắng trong tháng 4 năm 2026  đó là các mô hình cơ sở khác nhau có phong cách đàm phán bền vững.

> Đây là một sự thay đổi nhanh chóng vào năm 2025. Điểm nhấn không phải là mô hình nào sẽ giành chiến thắng vào tháng 4 năm 2026.

### Việc phân bổ nhiệm vụ thông qua hợp đồng Net + LLM

Việc tái sử dụng hợp đồng hiện đại cho LLM đa đại lý:

> 合同网在现代 LLM 多 Agent 中中重用:

1. Trưởng phòng phân hủy nhiệm vụ thành đơn vị.
   Trung ngữ翻译:管理者 代理 将任务分解为单元――
2. Truyền hình `cfp`Với mô tả nhiệm vụ cho nhân viên.
   Trung文翻译:向工作者 Agent 广播带任务描述的`cfp`
3. Mỗi công nhân trả lại một đề nghị: `(price, eta, confidence)`Giá có thể là token, đơn vị tính toán, hoặc đô la.
   Trung ngữ翻译:每个工作者返回一个报价:`(price, eta, confidence)`, trong đó giá có thể là token ⋅ tính đơn vị hoặc USD⋅
4. Người quản lý chọn người chiến thắng (một hoặc nhiều, tùy thuộc vào nhiệm vụ) và giải thưởng.
   Trung ngữ翻译:管理者选择获胜者 (单个或多个,取决于任务)并授标──
5. Những công nhân bị từ chối có thể tự do thầu cho các nhiệm vụ khác.
   Trung ngữ翻译:被拒的工作者可以竞标其他任务──

Điều này vượt quá 100 nhân viên bởi vì sự phối hợp là phát sóng và trả lời, không phải trò chuyện đồng bộ. được sử dụng trong sản xuất: mô hình dàn xếp của Microsoft Agent Framework, một số triển khai LangGraph.

> Điều này có thể được mở rộng tốt đến hơn 100 nhân viên, bởi vì phối hợp là mô hình phát thanh-đáp ứng, chứ không phải là cùng chia sẻ.

### Các bên liên quan của LLM

NeurIPS 2024 (https://proceedings.neurips.cc/paper_files/paper/2024/file/984dd3db213db2d1454a163b65b84d08-Paper-Datasets_and_Benchmarks_Track.pdf) giới thiệu các trò chơi có thể ghi bàn nhiều bên với **secret scores**và **minimum-acceptance thresholds**. Mỗi bên liên quan có các công ty tiện ích tư nhân; LLM phải suy luận chúng từ các thông điệp. Đây là sự phổ biến của thương lượng hai bên đến hình thành liên minh N-party.

> NeurIPS 2024  đã đưa ra các**秘密分数**和**最低接受阈值**Các công ty có thể đánh giá cao các vấn đề này. Mỗi người có lợi ích có lợi ích riêng; LLM phải được đưa ra từ thông tin.

### Quy tắc kể chuyện chống lại cơ chế

Trong tất cả các tiêu chuẩn đàm phán 2024-2026, quy tắc kỹ thuật nhất quán là:

> Hãy để LLM kể lại. Đừng để LLM tính toán đề nghị.

> 让LLM 叙述──不要让LLM 计算报价──

Nếu đề nghị cần phải là một số (giá, ETA, số lượng), tạo ra nó theo cách xác định từ trạng thái đàm phán và có LLM sản xuất khung. Nếu đề nghị cần phải là một cấu trúc đề xuất (phân giải nhiệm vụ, giao vai trò), hãy để LLM biên soạn nó, nhưng xác nhận nó dựa trên một sơ đồ và kiểm tra hạn chế trước khi gửi.

> Nếu giá cả cần phải là số (đơn giá, số lượng), từ trạng thái đàm phán xác định tạo ra nó, để LLM tạo ra một khuôn khổ. Nếu giá cả cần là cấu trúc đề xuất, để LLM xây dựng nó, nhưng phải được gửi trước khi được xác định về mô hình và quy mô kiểm tra.

## Hãy xây dựng nó.
```figure
a5-og-narrator
```

## Hãy xây dựng nó

`code/main.py`thực hiện:

- `ContractNetManager`- `ContractNetTask`- `Bid` quản lý + người đề nghị, phát sóng cfp, thu thập đề xuất, trao giải.
  Trung ngữ翻译:`ContractNetManager``ContractNetTask``Bid` 管理者 + 投标人,广播 cfp,收集提案,授标──
- `og_narrator_bargain(state, rng)` OG-Nau người mua: quyết định phong cách Zeuthen nhượng bộ về điểm trung.
  Trung ngữ翻译:`og_narrator_bargain` OG-Narrator 买方:确定性 Zeuthen 风格向中间点让步──
- `seller_response(state, rng)` chính sách đối phó của người bán xác định (sự thật cơ bản cấu trúc cho cả hai phong cách).
  Trung ngữ翻译:`seller_response` 确定性卖方还价策略 ( 确定性卖方还价策略)
- `naive_llm_bargain(state, rng)` mô phỏng một thương lượng toàn LLM: chọn giá với sự khác biệt cao, thường là bên ngoài ZOPA.
  Trung ngữ翻译:`naive_llm_bargain` 模拟全 LLM 议价者:以高方差选价,经常超出 ZOPA。
- Đo: tỷ lệ giao dịch trên 1000 thử nghiệm với giá đặt phòng mới được lấy mẫu cho mỗi thử nghiệm.
  Trung ngữ翻译:测量:1000 lần thử nghiệm tỷ lệ hoàn thành, mỗi lần thử nghiệm tái采样保留价格──

Đi chạy:

```
python3 code/main.py
```

Tạo ra dự kiến: tỷ lệ giao dịch LLM ngây thơ ~ 65-75%; tỷ lệ giao dịch OG-Narrator ~ 85-95%; khoảng cách 15-25 điểm là lợi thế cấu trúc của việc phân hủy sản xuất đề xuất từ câu chuyện.

> 预期输出:朴素 LLM 成交率约65-75%;OG-Narrator 成交率约85-95%;15-25 个百分点差距是将报价生成与叙述解的结构优势――加上一个三个投标者和一个任务的合同网任务市场分配示例――

## Sử dụng nó.

`outputs/skill-bargainer-designer.md`thiết kế một giao thức thương lượng: ai tạo ra các đề nghị (định nghĩa hoặc LLM), ai kể lại, cách các scratchpad riêng biệt tách biệt với các thông điệp công cộng, và cách theo dõi tỷ lệ giao dịch.

> `outputs/skill-bargainer-designer.md`设计一个议价协议:谁生成报价 (谁生成报价) (确定性或 LLM),谁叙述,谁描述,谁描述,谁描述,谁描述,谁描述,谁描述,谁描述,谁描述,谁描述,谁描述,谁描述,谁描述,谁描述,谁描述,谁描述,谁描述,谁描述,谁描述,谁描述,谁描述,谁描述,谁描述,谁描述,谁描述,谁描述,谁描述,谁描述,谁描述,谁描述,谁描述,谁描述,谁描述,谁描述,谁描述,谁描述,谁描述,谁描述,谁描述,谁描述,谁描述,谁描述,谁监督,以及如何监督成交率.

## Đưa nó lên mạng

Danh sách kiểm tra thương lượng sản xuất:

- **Separate scratchpad.**Nhà nước tư nhân không bao giờ đạt đến ngữ cảnh của đối tác.
  Trung ngữ翻译:**分离草稿本。**Tình trạng cá nhân sẽ không bao giờ đạt được đối thủ trên...
- **Deterministic offer generation.**Giá, số lượng, thời gian đến: tính toán, không yêu cầu.
  Trung ngữ翻译:**确定性报价生成。**价格、数量、ETA:计算, đừng gợi ý.
- **Validate all incoming offers**Thử từ chối các đề nghị ngoài của Zopa ở biên giới giao thức.
  Trung ngữ翻译:**验证所有传入报价**根据模式――在协议边界拒绝 ZOPA 外的报价――
- **Bound rounds.**3-5 lần bắn tối đa; tăng lên trung gian khi bị tắc nghẽn.
  Trung ngữ翻译:**限制轮次。**Trận tối đa 3-5 vòng; chết khóa khi nâng cấp đến điều giải.
- **Measure deal rate and payoff variance**Một tỷ lệ giao dịch giảm là một triệu chứng  thường là một sự lở hở nhanh chóng hoặc một cuộc tấn công bên đối tác.
  Trung ngữ翻译:**持续测量成交率和收益方差。**Tỷ lệ giao dịch giảm là triệu chứng thường là sự chuyển động hoặc tấn công đối phương.
- **Log all rejected proposals**Đối với các nhà quản lý mạng hợp đồng, những người đấu thầu thua cuộc cần hiểu lý do tại sao.
  Trung ngữ翻译:**记录所有被拒绝的提案**及确定性理由── đối với người quản lý hợp đồng, người nộp đơn cần hiểu lý do──

## Tập luyện bài tập

1. Đi chạy`code/main.py`- Confirm OG-Narrator vượt qua naive-LLM với tỷ lệ giao dịch.
   Trung ngữ翻译:运行 `code/main.py`❖ xác nhận OG-Narrator trong tỷ lệ thành công tốt hơn LLM đơn giản ❖
2. Thực hiện**persona-based payoff improvement**(arXiv:2402.05863)  người mua chỉ chấp nhận một "sự tuyệt vọng mua tuần này" nhân vật trong câu chuyện, cung cấp máy phát động không thay đổi.
   Trung ngữ翻译:实现**基于人格的收益改进**(arXiv:2402.05863)  người mua chỉ sử dụng trong câu chuyện "本周急需购" nhân cách, giá cả tạo không thay đổi.
3. Thực hiện chuỗi suy nghĩ **concealment**: giữ một chuỗi scratchpad riêng mà không được chuyển đến đối tác.
   Trung ngữ翻译:实现思维链**隐藏**:维护一个不传递给对手的私人草稿本字符串. Nếu không cố gắng tiết lộ (通过交换通道模拟) sẽ xảy ra gì?
4. Có thể mở rộng hợp đồng Net cho đấu giá N-thầu với giá dự trữ. Khi tất cả các giá thầu vượt quá dự trữ, làm thế nào người quản lý quyết định giữa giá thấp nhất và chất lượng cao nhất?
   Trung ngữ翻译:将合同网扩展以保留价格的 N 投标人拍卖. Khi tất cả các cổ phiếu được đặt ra vượt quá giá lưu giữ, quản lý làm thế nào để chọn giữa giá thấp nhất và chất lượng cao nhất?
5. Đọc Bhattacharya et al. 2025 trên Harvard Negotiation Project metrics. Thực hiện hai thương lượng với các phong cách khác nhau (cực kỳ hung hăng vs. công bằng). đo sự khác biệt thanh toán dưới sự đối xứng và không đối xứng.
   Bài viết của Bhattacharya 等人 về mục tiêu của dự án đàm phán của Harvard năm 2025 ⋅ thực hiện hai kiểu khác nhau của các nhà đàm phán ⋅ tấn công đối với công bằng ⋅ đo lường đối xứng và không đối xứng đối xứng.

## Từ khóa  Keyword

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Contract Net / 合同网 | "Task market" / "任务市场" | Smith 1980, FIPA 1996. cfp + propose + accept/reject. The canonical task-market. / Smith 1980, FIPA 1996。cfp + propose + accept/reject。规范的任务市场。 |
| ZOPA / 可能协议区 | "Zone of possible agreement" / "可能协议区域" | Overlap between buyer's max and seller's min. Offers outside it cannot close. / 买方最大值和卖方最小值的重叠。超出此范围的报价无法成交。 |
| BATNA / 最佳替代方案 | "Best alternative to a negotiated agreement" / "谈判协议的最佳替代方案" | Your fallback if this deal fails. Sets your reservation price. / 如果交易失败的后备方案。设定你的保留价。 |
| OG-Narrator / OG-叙述者 | "Offer generator + narrator" / "报价生成器 + 叙述者" | Decomposition: deterministic offer, LLM narration. / 分解：确定性报价，LLM 叙述。 |
| Zeuthen strategy / Zeuthen 策略 | "Risk-minimizing concession" / "风险最小化让步" | Classical offer-generator that concedes based on risk limits. / 基于风险限制让步的经典报价生成器。 |
| Rubinstein bargaining / Rubinstein 议价 | "Alternating-offer equilibrium" / "交替报价均衡" | Game-theoretic model for infinite-horizon bargaining with discounting. / 带折现的无限期议价博弈论模型。 |
| CoT concealment / CoT 隐藏 | "Hide your reasoning" / "隐藏推理" | Winners in arXiv:2503.06416 kept private scratchpads; public channel shows offer only. / arXiv:2503.06416 的获胜者保持私人草稿本；公开通道只显示报价。 |
| Persona manipulation / 人格操纵 | "Emotional posturing" / "情绪姿态" | arXiv:2402.05863: ~20% payoff gain from desperation/urgency personas. / arXiv:2402.05863：绝望/紧迫人格带来约 20% 的收益增益。 |

## Xem thêm 延伸阅读

- [NegotiationArena](https://arxiv.org/abs/2402.05863) chỉ số chuẩn; kết quả thao túng cá nhân và khai thác
- [Measuring Bargaining Abilities of Language Models](https://arxiv.org/abs/2402.15813) OG-Narrator và kết quả người mua khó hơn người bán
- [Large-Scale Autonomous Negotiation Competition](https://arxiv.org/abs/2503.06416) ~ 180k đàm phán; chuỗi của suy nghĩ che giấu thắng
- [LLM-Stakeholders Interactive Negotiation (NeurIPS 2024)](https://proceedings.neurips.cc/paper_files/paper/2024/file/984dd3db213db2d1454a163b65b84d08-Paper-Datasets_and_Benchmarks_Track.pdf) trò chơi có thể ghi bàn nhiều bên với các tiện ích bí mật
- [Smith 1980 — The Contract Net Protocol](https://ieeexplore.ieee.org/document/1675516) Cơ chế cổ điển, IEEE Transactions on Computers
