# Eagle-3 - Khóa mã dự đoán trong sản xuất

> Việc giải mã giả định kết hợp mô hình dự thảo nhanh với mô hình mục tiêu. Dự thảo đề xuất các token K; mục tiêu xác minh bằng một forward duy nhất; các token được chấp nhận là miễn phí. Năm 2026, EAGLE-3 là biến thể cấp sản xuất  nó đào tạo một đầu dự thảo trên các trạng thái ẩn của mô hình mục tiêu thay vì trên mã thông báo thô, đẩy tỷ lệ chấp nhận alpha vào băng thông 0.6-0.8 trên trò chuyện chung. Câu hỏi đúng không phải là "mặt hước nhanh như thế nào" mà là " alpha là gì trên lưu lượng truy cập của tôi?" Nếu alpha giảm xuống dưới ~ 0.55, việc giải mã giả định là âm tính tại đồng thời cao bởi vì mỗi dự thảo bị từ chối chi phí một mục tiêu tiếp theo thứ hai. Bài học này dạy bạn phải đo alpha trước và xoay cờ sau.

> **【中文解读】**Bài viết này giới thiệu về các kỹ thuật phân tích suy đoán với mô hình nhỏ dự đoán mô hình lớn xuất hiện để tăng tốc suy đoán.
**Type:** Learn
**Languages:** Python (stdlib, toy acceptance-rate simulator)
**Prerequisites:** Phase 17 · 04 (Serving Engine Internals), Phase 10 · 18 (Multi-Token Prediction)
**Time:** ~60 minutes


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy acceptance-rate simulator) | **语言:** Python（标准库，接受率模拟器）
**Prerequisites:** Phase 17 · 04 (vLLM Serving Internals), Phase 10 · 18 (Multi-Token Prediction) | **前置知识:** Phase 17 · 04（vLLM 服务内部）, Phase 10 · 18（多 Token 预测）

>  **【前置】**学本节前请先掌握:Phase 17·04(vLLM) 、Phase 10·18(MTP 多 token 预测) 、Phase 10·25(投机解码原理) ⋅本节是生产版 EAGLE-3。
>  **【类比】**EAGLE-3 = "翻译员打草稿"──草稿模型(草案) 快速猜 K 个代币,目标模型一次验证──猜对=免费,猜错=多一次验证开销──EAGLE-3 创新:用目标模型隐藏状态训练草案(而不是原始代币), 接受率 α 提到 0.6-0.8──生产关键问题:α 在你的流量上多少?<0.55 时反而拖慢(拒绝的草案 浪费计算力) 必须先测α 再开旗――
**Time:** ~60 minutes | **时间:** ~60 分钟

## Mục tiêu học tập

- Hãy nêu tên ba thế hệ giải mã giả định và giải thích những gì EAGLE-3 thay đổi từ EAGLE-2 và từ mô hình dự thảo cổ điển.
  Trung ngữ翻译:说出推测解码的三代,并解释 EAGLE-3 相比EAGLE-2 和经典草案 模型改变了什么──
- Định nghĩa tỷ lệ chấp nhận alpha, tính toán tốc độ dự kiến từ alpha và K (giờ dài), và xác định alpha chia bằng cho đồng thời mục tiêu của bạn.
  Trung文翻译:定义接受率 alpha, từ alpha 和 K(草案 长度) tính toán dự kiến tăng tốc tỷ lệ,并确定目标并发下亏平衡 alpha。
- Giải thích tại sao việc giải mã giả định là chọn lựa (không phải mặc định) trong vLLM 2026 và tại sao bật nó mà không đo alpha là một mẫu chống sản xuất.
  Trung ngữ翻译:解释为什么推测解码在2026年 vLLM 中是选择-in (非默认),以及为什么不测量alpha 就开启它是生产反模式――
- Viết một kế hoạch đo lường: điểm chuẩn nào, phân phối nào, điểm đồng thời nào, số liệu nào để nhập vào.
  Trung ngữ翻译:写出测量计划:哪个基准测试、哪个快点 分布、哪个并发点、哪个指标作为门控──

## Vấn đề  vấn đề giới thiệu

> **【中文解读】**Ưu điểm giải mã giai đoạn là trong bộ nhớ có giới hạn rộng  mỗi giải mã một mã  cần phải đọc khoảng 140 GB / s trọng lượng, GPU  tính toán gần như trống ;; Ưu điểm giải mã sử dụng trống : sử dụng mô hình nhỏ giá rẻ để tạo ra K 个候选 mã, sau đó để mô hình mục tiêu trong một lần phát tán trước   ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ 

> **【拓展：推测解码的产业应用】**Google sẽ đưa ra dự án triển khai mã hóa AI vào năm 2025 (được xem xét kỹ thuật số của mình), trong trường hợp không mất chất lượng, đã tăng tốc độ phản ứng đáng kể.`speculative_config`作为官方接口──在生产中,推测解码特别适合实时对话(TTFT 敏感) 和代码补充全(延迟敏感)场景──但需要注意:高并发(256+)

Decode là kết nối bộ nhớ. trên một H100 chạy Llama 3.3 70B FP8, mỗi token được giải mã đọc ~ 140 GB / s trọng lượng và phát ra một token.

> Trong H100 trên chạy Llama 3.3 70B FP8, mỗi mã hóa mã hóa 读取约140 GB/s权重并输出一个 mã hóa。GPU 计算在解码期间几乎空瓶是HBM 带宽,而不是矩阵乘吞吐量。

Việc giải mã giả định khai thác khoảng cách. Tạo các mã thông báo ứng cử viên K với mô hình dự thảo rẻ tiền, sau đó yêu cầu mô hình mục tiêu xác minh tất cả K trong một lần đi trước. Mỗi mã thông báo được xác minh thực sự miễn phí (được rút tiền thành một loạt các mã thông báo K mà mục tiêu đã phải làm bất cứ lúc nào).

> 推测解码利用这个差距――使用廉价的草案 模型生成K个候选标记,然后让目标模型在一次前向传播中验证所有K个――每个验证通过的标记实际上是免费的(分摊到目标模型应该做的K批前向中) ――

Phương pháp mô hình dự thảo cổ điển sử dụng mô hình nhỏ hơn của cùng một gia đình (Llama 3.2 1B dự thảo cho Llama 3.3 70B). Nó hoạt động nhưng tỷ lệ chấp nhận là trung bình  phân phối mô hình nhỏ hơn khác với mục tiêu. Eagle, sau đó là Eagle-2, sau đó là Eagle-3 tập trung một đầu dự án nhẹ trực tiếp vào trạng thái bên trong của mô hình mục tiêu, do đó phân phối dự án theo dõi mục tiêu nhiều hơn. Đó là lý do tại sao alpha đi từ 0,4 với mô hình dự thảo đến 0,6-0,8 với EAGLE-3.

> 经典的草案 模型方法使用同系列的更小模型(Llama 3.2 1B 为 Llama 3.3 70B做草案) ―― nó có thể nhưng chấp nhận tỷ lệ phân bố nhỏ hơn của mô hình đơn giản偏离目标──EAGLE、EAGLE-2、EAGLE-3 直接在目标模型内部状态上训练轻量草案头,所以草案的分布更接近目标──这就是为什么 Alpha từ草案 模型的 0.4 升至EAGLE-3 的 0.6-0.8──

Vận động: EAGLE-3 sẽ chọn tham gia vào vLLM 2026. `speculative_config`Đội ngũ chuyển đổi nó mà không đo alpha trên lưu lượng truy cập thực của họ thường thấy độ trễ đuôi trở nên tồi tệ hơn, không tốt hơn.

> 关键点:EAGLE-3 trong năm 2026 VLLM Trung là chọn vào.`speculative_config`Không có dấu hiệu, không có tăng tốc, không đo lượng lưu lượng thực tế alpha, nhóm mở ra thường thấy sự chậm trễ thay đổi thay vì cải thiện.

## Khái niệm cốt lõi

### Điều gì tính toán giải mã thực sự mua

> **【中文解读】**推测解码的加速比公式为 `S = (1 + K*alpha) / (1 + verify_overhead)`Đối với K=5, alpha=0.7, tăng tốc lý thuyết là 4.1x. Nhưng trong sản xuất thực tế thường chỉ đạt 2-3x, vì alpha trong lưu lượng thực ít đạt 0,7 trên, và chứng minh việc bán hàng ở kích thước lô cao tăng lớn.

Nếu không có mã hóa đặc điểm, chi phí mỗi token là một mục tiêu tiến. Với mã hóa đặc điểm ở chiều dài dự thảo K và chấp nhận alpha, dự kiến các token cho mỗi mục tiêu tiến là `1 + K * alpha`- Tốc độ tăng tốc là`(1 + K * alpha) / (1 + epsilon)`nơi epsilon là draft-plus-verify overhead. cho K=5, alpha=0.7: `(1 + 5*0.7) / (1 + 0.1) = 4.5 / 1.1 = 4.1x`Số lượng trong thế giới thực tập hợp khoảng 2-3 lần vì alpha hiếm khi cao như vậy trên lưu lượng sản xuất và epsilon phát triển ở kích thước lô cao.

> Không có dự đoán giải mã, mỗi token thành phần của một mục tiêu trước tiên tiến truyền tải.`1 + K * alpha`◊ tăng tốc hơn`(1 + K * alpha) / (1 + epsilon)`, trong đó epsilon là dự thảo + 验证开销.`(1 + 5*0.7) / (1 + 0.1) = 4.5 / 1.1 = 4.1x`◊ tập trung dữ liệu thực tế là 2-3x, vì alpha trong dòng sản xuất rất ít, và epsilon trong kích thước lô cao tăng lớn ◊

### Tại sao alpha là chỉ số duy nhất quan trọng

Các token bị từ chối không biến mất  họ buộc một mục tiêu thứ hai đi về phía trước cho token bị từ chối đầu tiên. Với khối lượng làm việc mà alpha giảm xuống 0,4, bạn phải trả chi phí tổng hợp cộng với xác minh cộng với việc tái đóng. Ở đồng thời cao (chẳng hạn 256 đồng thời), lô decode đã đủ lớn để khoảng cách băng thông bộ nhớ giữa "chỉ mục tiêu" và "chỉ mục tiêu với xác minh" giảm đi. Dưới alpha 0.55 trên hầu hết phần cứng 2026, mã giải mã đặc điểm là âm tính.

> Các token bị từ chối sẽ không biến mất chúng buộc phải đối mặt với token bị từ chối đầu tiên  tiến hành mục tiêu tiếp theo tiếp tục lan truyền. Trong alpha  giảm xuống 0.4 tải trọng làm việc, bạn trả dự thảo 开销 + 验证 + 重新生成. Trong 256 lần phát triển, số lượng giải mã đã đủ lớn, khoảng cách dung lượng trong bộ nhớ giữa "单独目标" và "带验证目标" giảm đi.

Alpha thay đổi theo khối lượng công việc. Trong cuộc trò chuyện chung kiểu ShareGPT, EAGLE-3 được đào tạo trên ShareGPT đạt 0,6-0,8. Trên lưu lượng truy cập cụ thể về miền (điều mã, y tế, pháp lý) đầu dự thảo được đào tạo về dữ liệu chung giảm xuống 0,4-0,6.

> Alpha vì tải trọng làm việc khác. Trong các cuộc trò chuyện chung của ShareGPT 风格, sử dụng EAGLE-3 训练 của ShareGPT đạt 0.6-0.8  trên một dòng chảy cụ thể trong lĩnh vực:

### Những thế hệ của đại bàng một lần

> **【中文解读】**推测解码经历了三代演进:(1) Mô hình dự thảo cổ điển(同一系列小模型,alpha 0.3-0.5) đơn giản nhưng tỷ lệ chấp nhận thấp;(2) EAGLE-1/2(train draft head on the target model hidden state,alpha 0.5-0.7) Higher acceptance rate;(3) EAGLE-3(train on multilayer hidden state,alpha 0.6-0.8)2025-2026 năm sản xuất cấp cứu.

> **【拓展：推测解码 vs 其他加速技术】**LLM 推理加速技术对比:(1) 推测解码(EAGLE-3) 2-3x 加速, cần thêm đầu dự thảo;(2) 量化(INT8/FP8) 推理加速 1.5-2x, có chút chất lượng mất;(3) 分块预填降低ITL đuôi nhưng không trực tiếp nâng cỡ;(4) 分分式预填/解码消除资源浪费,30-40% 成本节省;(5) 自研芯片(Groq/Cerebras) 5-10x 解码速度但单价更高──这些技术可叠加使用:EAGLE-3 + FP8 + 分分式部署的综合效果可达10x──

- **Classic draft model**: mô hình nhỏ cùng gia đình. Alpha 0.3-0.5. cơ sở hạ tầng đơn giản  hai mô hình tải, dự thảo chạy K về phía trước cho mỗi mục tiêu về phía trước.
  Trung ngữ翻译:**经典 draft 模型**:同系列的小模型──Alpha 0.3-0.5──基础设施简单加载两个模型,草案 每次目标前向运行 K 次前向──
- **EAGLE-1 (2024)**: đầu đầu một đầu được huấn luyện trên các trạng thái ẩn mục tiêu (phần cuối). Alpha ~ 0,5-0,6.
  Trung ngữ翻译:**EAGLE-1 (2024)**Trong mục tiêu ẩn trạng thái () trên tập luyện đơn draft head.
- **EAGLE-2 (2025)**: chiều dài bản thảo thích ứng và bản thảo dựa trên cây (thêm vào nhiều nhánh trong một mục tiêu vượt qua). Alpha ~ 0,6-0,7.
  Trung ngữ翻译:**EAGLE-2 (2025)**: tự thích ứng dự thảo 长度和基于树的草案(一次目标前向验证多个分支) ・Alpha 约 0.6-0.7──更复杂的草案 调度器──
- **EAGLE-3 (2025-2026)**: đầu dự án được đào tạo trên nhiều lớp mục tiêu (không chỉ là cuối cùng), sắp xếp tốt hơn. Alpha ~ 0,6-0,8 trên trò chuyện chung.
  Trung ngữ翻译:**EAGLE-3 (2025-2026)**Trong nhiều mục tiêu, không chỉ là lớp cuối cùng, nhưng còn tốt hơn là tập luyện.

### Công thức sản xuất năm 2026

> **【中文解读】**生产环境 EAGLE-3 部署的五步流程:(1) 先以基础模型上线,建立 TTFT/ITL/吞吐量基线;(2) 启动 EAGLE-3 dự thảo 配置;(3) 监控接受率 alphavLLM V1 通过`spec_decode_metrics.accepted_tokens_per_request`暴露此指标;(4) Nếu alpha < 0.55,禁用推测解码或训练领域特定的草案头;(5) 在生产并发水平重新测试, xác nhận P99 ITL 没有恶化──

1. Mô hình mục tiêu tàu đơn giản. đo TTFT cơ sở, ITL, thông qua tại đồng thời mục tiêu.
   Trung ngữ翻译:先以基础模型上线──在目标并发下测量基线 TTFT、ITL、吞吐量──
2. Khả năng dự thảo EAGLE-3 thông qua vLLM `speculative_config`- Đổi lại điểm chuẩn.
   中文翻译: qua vLLM `speculative_config`启动 EAGLE-3 dự thảo.
3. Tỷ lệ chấp nhận nhật ký alpha. vLLM V1 báo cáo điều này như `spec_decode_metrics.accepted_tokens_per_request`Chia theo chiều dài dự thảo yêu cầu để có được alpha.
   中文翻译:记录接受率 alpha──vLLM V1 通过 `spec_decode_metrics.accepted_tokens_per_request`報告──除以要求草案 长度得到 alpha──
4. Nếu alpha < 0,55 về phân phối lưu lượng sản xuất, vô hiệu hóa mã thông số kỹ thuật hoặc đào tạo một bản thảo EAGLE-3 cụ thể cho lĩnh vực.
   Trung ngữ翻译: Nếu phân bố lưu lượng sản xuất trên alpha < 0.55,禁用推测解码或训练领域特定的EAGLE-3草案──
5. Khi đồng thời sản xuất, chạy lại.
   Trung文翻译:在生产并发下重新测试──确认 P99 ITL 没有恶化──

### Hỗn hẹp sản xuất: đuôi P99

Phân tích thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin thông tin

> 平均 ITL 随推测解码下降──如果不调优,P99可能恶化──被拒绝的草案 触发两次传递序列(草案 + 验证失败 + 重新生成)──在满批次下,这两次传递串行化──关注 P99 ITL,而不是 P50──

### Khi EAGLE-3 đã được triển khai

Google triển khai mã hóa giả định trong AI Overviews vào năm 2025 (các chất lượng tương tự, phản ứng nhanh hơn). vLLM V1 tàu `speculative_config`như giao diện được ghi chép; N-gram GPU decoding speculative trong V1 là biến thể tương thích với prefill chunked. SGLang hỗ trợ EAGLE-3 như là con đường dự thảo được khuyến cáo cho tải trọng công việc nặng tiền tố.

> Google sẽ đưa ra các dự án giải mã vào năm 2025 để triển khai AI Overviews.`speculative_config`作为档档化接口;V1 中的N-gram GPU 推测解码是与分块预填兼容的变体──SGLang 支持EAGLE-3 作为前密集工作负载的推草案路径──

### Phá toán bằng nhau trong một dòng

Tốc độ tăng tốc dự kiến: `S(alpha, K) = (1 + K*alpha) / (1 + verify_overhead)`- Đặt`S = 1`giải quyết cho alpha: `alpha_breakeven = verify_overhead / K`. Đối với tiêu chuẩn xác minh_overhead ~0.15 và K=5: `alpha_breakeven = 0.03`Nhưng đó là toán học giải mã nguyên thô. Khi đồng thời cao chi phí kiểm tra tăng lên và lô giải mã đã giảm giá đọc bộ nhớ qua các chuỗi, do đó hiệu quả alpha_breakeven leo lên ~ 0,45-0,55 trong thực tế.

> 预期加速比:`S(alpha, K) = (1 + K*alpha) / (1 + verify_overhead)`设 `S = 1`求解 alpha:`alpha_breakeven = verify_overhead / K`❖ điển hình xác minh_overhead 约 0.15,K=5:`alpha_breakeven = 0.03`Nhưng đó là nguyên thủy giải mã toán học. Trong cao并发下, xác nhận chi phí bán hàng tăng lên, giải mã số lượng đã được đọc trong chuỗi chia sẻ trong lưu trữ, vì vậy thực tế hiệu quả alpha_breakeven tăng lên khoảng 0,45-0,55。

### Khi nào không nên sử dụng mã hóa giả định

> **【拓展：推测解码的适用场景】**推测解码在以下场景有效:(1) 实时对话(TTFT < 200ms 要求) 2-3x 加速显著改善用户体验;(2) 代码补充(实时性要求高);(3) 低并发场景(< 50 concurrent) 内存带宽差距大,收益明显。 在以下场景应避免:(1) 批量离线生成延迟不重要,使用平面目标;(2) 短输出< 50 token) 草案 开销和验证成本主导;(3) 专业领域无领域训练的草案) alpha 太;(4) vLLM v0.18.0 + 草案-model + 零零-pre-model + 组合 零-低容容

> **【拓展：vLLM 推测解码配置】**vLLM V1 支持三种推测解码模式:(1) Dự thảo mô hình传统小模型作为草案,与零碎预填不兼容;(2) EAGLE在隐状态训练的草案头,推用于通用场景;(3) N-gram GPU基于提示 中 N-gram 查找的 GPU端草案,是唯一与零碎预填兼容的模式──`speculative_config`必须显式设置,vLLM默认不开任何推测解码──

- Lập 1 offline generation mà thời gian trễ không quan trọng.
  Trung ngữ翻译:延迟无关紧要的批量为 1 的离线生成――使用普通目标模型――
- Các sản phẩm đầu ra rất ngắn (dưới 50 token).
  Trung文翻译:非常短的输出(50 token 以下) ・ dự thảo 开销和验证成本占主导──
- Các tên miền chuyên nghiệp không có người huấn luyện tên miền.
  Trung文翻译:没有领域训练草案负责人的专业领域──Alpha 太低──
- vLLM v0.18.0 cộng với mã hóa mô hình dự thảo đặc điểm cộng với `--enable-chunked-prefill`Sự kết hợp này không biên soạn. ngoại lệ được ghi chép là mã hóa kỹ thuật định dạng GPU N-gram trong V1.
  中文翻译:vLLM v0.18.0 + mô hình dự thảo 推测解码 + `--enable-chunked-prefill` Bộ phận này không thể biên dịch được.

## Hãy sử dụng nó để thực hiện
```figure
mx-speculative-tree
```

## Sử dụng nó

`code/main.py`mô phỏng một vòng giải mã với và không có giải mã đầu cơ trên một loạt các giá trị alpha và chiều dài dự thảo K. Nó in alpha break-even, đo tốc độ lên, và hành vi đuôi.

> `code/main.py`模拟有/无推测解码的解码循环,覆盖一系列 alpha 值和草案 长度 K――它印印亏平衡 alpha、测量加速比和尾部行为──在多个 (alpha, K) 组合上运行,精确看推测解码在哪里停止收益──

## Chuyển nó đi.

Bài học này sẽ mang lại kết quả `outputs/skill-eagle3-rollout.md`. Với mô hình mục tiêu, mô tả phân phối lưu lượng và mục tiêu đồng thời, nó tạo ra một kế hoạch triển khai EAGLE-3 từng giai đoạn  đường cơ sở tham chiếu, cho phép cấu hình, đo alpha, cổng trên alpha >= 0.55, xem P99 ITL.

> 本课产 出 `outputs/skill-eagle3-rollout.md` Được định mục tiêu mô hình  lưu lượng phân bố mô tả và phát triển mục tiêu, nó tạo ra giai đoạn phân đoạn EAGLE-3  đưa ra kế hoạch 基准基线  kích hoạt cấu hình  đo alpha  alpha >= 0.55  như là kiểm soát 关注 P99 ITL 

## Tập luyện bài tập

1. Đi chạy`code/main.py`Ở K=5, bạn cần alpha nào để tăng tốc 2x? 3x?
   Trung ngữ翻译:运行 `code/main.py`K=5 时,2x 加速需要多少 alpha?3x 加速呢?
2. Hãy tưởng tượng lưu lượng sản xuất chia sẻ 70% chat chung, 30% mã. chat chung đạt alpha 0.7 với EAGLE-3 được đào tạo trên ShareGPT; mã đạt alpha 0.4.
   Trung ngữ翻译:假设生产流量 70% 通用聊天,30% 代码──通用聊天 alfa 0.7,代码 alfa 0.4──混合 alfa 是多少,推测解码是否净正向?
3. Đọc vLLM `speculative_config`Các mô hình (mô hình bản, EAGLE, N-gram) và mô hình nào tương thích với việc điền trước từng mảnh.
   中文翻译:阅读 vLLM `speculative_config`文档──说出三种模式(Mô hình bản EAGLE、N-gram)及哪个与分块预填兼容──
4. Bạn thấy mức ITL giảm 25% sau khi kích hoạt EAGLE-3 nhưng P99 ITL tăng 15%. Chẩn đoán và đề xuất giảm thiểu.
   Trung ngữ翻译:启用EAGLE-3 后平均ITL 下降25%,但P99 ITL上升15%──诊断并提出缓解方案──
5. Xét chi phí bộ nhớ của đầu dự thảo EAGLE-3 cho Llama 3.3 70B. Nó so sánh như thế nào với chạy Llama 3.2 1B như một dự thảo cổ điển?
   Trung文翻译:计算 Llama 3.3 70B 的 EAGLE-3 dự thảo đầu 内存成本──与运行 Llama 3.2 1B 作为经典草案 相比怎么?

## Từ khóa  Từ khóa nhanh chóng

| Term / 术语 | What people say / 通俗说法 | What it actually means / 实际含义 |
|------|----------------|------------------------|
| Speculative decoding | "draft plus verify" / "draft 加验证" | Propose K tokens with a cheap model, verify all K in one target forward / 用廉价模型提议 K 个 token，一次目标前向验证所有 K 个 |
| Acceptance rate alpha | "spec accept rate" / "推测接受率" | Fraction of draft tokens accepted by the target; the only metric that matters / 被 target 接受的 draft token 比例；唯一重要的指标 |
| Draft length K | "spec k" / "推测 K" | How many tokens the draft proposes per target forward; typical 4-8 / 每次 target 前向 draft 提议多少 token；通常 4-8 |
| Verify overhead epsilon | "spec overhead" / "推测开销" | Extra cost to verify-and-reroll vs a plain target forward; grows with batch / 验证+重新生成 vs 普通 target 前向的额外成本；随 batch 增长 |
| EAGLE-3 | "latest EAGLE" / "最新 EAGLE" | 2025-2026 variant; trains draft head on multiple target layers; alpha 0.6-0.8 / 2025-2026 变体；在多个 target 层上训练 draft head |
| `speculative_config` | "vLLM spec config" / "vLLM 推测配置" | The explicit opt-in in vLLM V1; no default means no acceleration / vLLM V1 中的显式 opt-in；无默认即无加速 |
| N-gram spec decode | "N-gram draft" / "N-gram draft" | GPU-side draft using N-gram lookups in the prompt; chunked-prefill-compatible / GPU 端使用 prompt 中 N-gram 查找的 draft；与分块预填充兼容 |
| Break-even alpha | "no-op alpha" / "无效果 alpha" | Alpha at which spec decode gives zero speedup; watch this at production concurrency / 推测解码零加速的 alpha；在生产并发下关注 |
| Rejected-draft two-pass | "reroll cost" / "重新生成成本" | Two target forwards when drafts reject; drives P99 tail / draft 被拒绝时的两次 target 前向；驱动 P99 尾部 |

## Xem thêm 延伸阅读

- [vLLM — Speculative Decoding docs](https://docs.vllm.ai/en/latest/features/spec_decode/) nguồn tin có thẩm quyền trên `speculative_config`và tương thích với các bộ phận trước lấp trong V1.
- [vLLM Speculative Config API](https://docs.vllm.ai/en/latest/api/vllm/config/speculative/) bộ trường chính xác.
- [EAGLE paper (arXiv:2401.15077)](https://arxiv.org/abs/2401.15077) Nữ bản của đầu dự thảo của Eagle.
- [EAGLE-2 paper (arXiv:2406.16858)](https://arxiv.org/abs/2406.16858) Dự thảo và cây thích ứng.
- [UC Berkeley EECS-2025-224](https://www2.eecs.berkeley.edu/Pubs/TechRpts/2025/EECS-2025-224.html) Hệ thống LLM hiệu quả với việc giải mã đầu cơ.
- [BentoML — Speculative Decoding](https://bentoml.com/llm/inference-optimization/speculative-decoding) Danh sách kiểm tra triển khai sản xuất.
