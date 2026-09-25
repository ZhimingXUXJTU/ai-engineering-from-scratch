# Thế hệ 3D

> 3D là phương thức mà đòn bẩy 2D đến 3D mạnh nhất. Sự đột phá năm 2023 là 3D Gaussian Splating. 2024-2026 tạo ra các lớp đẩy đa dạng phân phối + tái tạo 3D trên cùng để tạo ra các đối tượng và cảnh từ một lời nhắc hoặc ảnh duy nhất.

> **【中文解读】**3D là mô hình nối nối 2D đến 3D mạnh nhất. Năm 2023 là đột phá của 3D Gaussian Splating. Xu hướng sản xuất năm 2024-2026 là sẽ có nhiều góc nhìn mở rộng + 3D tái tạo chồng lên, từ một lời chỉ dẫn hoặc hình ảnh tạo ra vật thể và cảnh 3D.

> **【拓展：3D 生成的应用】**3D 生成 được sử dụng cho game tài sản tạo ra VR / AR 内容、建筑设计、电商产品展示──DreamGaussian、TripoSR 等模型可以在秒级从文字/图片生成 3D模型──

**Type:** Learn / 学习型
**Languages:** Python
**Prerequisites:** Phase 4 (Vision / 视觉), Phase 8 · 07 (Latent Diffusion / 潜在扩散)
**Time:** ~45 minutes

## Vấn đề  vấn đề giới thiệu

Nội dung 3D là đau đớn:

> 3D 内容很困难:

- **Representation.**Các lưới, đám mây điểm, lưới voxel, trường đường cách (SDF), trường tia sáng thần kinh (NeRF), Gaussians 3D. Mỗi một trong số đó có trade-off.
  **表示方式。**网格、点云、体素、SDF、NeRF、3D 高斯──各有权衡──
- **Data scarcity.**ImageNet có 14 triệu hình ảnh. Bộ dữ liệu 3D sạch lớn nhất (Objaverse-XL, 2023) có ~ 10 triệu vật thể, chất lượng thấp nhất.
  **数据稀缺。**ImageNet có 140.000 hình ảnh.
- **Memory.**Một lưới 5123 voxel là 128M voxel; một cảnh hữu ích NeRF cần 1M mẫu / tia.
  **内存。**5123 体素网格 là 1.28 tỷ体素.
- **Supervision.**Đối với hình ảnh 2D bạn có các pixel. Đối với 3D bạn thường có một số lượng lớn các hình ảnh 2D và phải nâng lên 3D.
  **监督。**2D hình ảnh có hình ảnh. 3D thường chỉ có một lượng nhỏ hình ảnh 2D.

Các khối 2026 tách hai vấn đề. Thứ nhất, tạo ra hình ảnh đa hình ảnh 2D với mô hình phân tán. thứ hai, phù hợp với hình ảnh đó một đại diện 3D (thường là Gaussian splating).

> Chương trình năm 2026 chia làm hai bước: đầu tiên sử dụng mô hình mở rộng tạo ra * 2D 多视角图像*, tái sử dụng * 3D biểu hiện *( thường là cao 射) 拟合──

> **【中文解读】**Thách thức cốt lõi của 3D sinh sản: biểu hiện nhiều cách: trước sử dụng mô hình mở rộng để tạo ra nhiều góc nhìn 2D hình ảnh, tái sử dụng 3D cao cấp chiếu xạ (Gaussian Splating) phù hợp với biểu hiện 3D.

> **【拓展：3D Gaussian Splatting 的革命性影响】**3DGS(2023) thay thế NeRF  trở thành phương pháp xây dựng 3D 重重的主流. Nó sử dụng hàng triệu cảnh 3D 高斯球体表示场景,染速度快 100 倍以上,质量相当或更优.

## Khái niệm cốt lõi

![3D generation: multi-view diffusion + 3D reconstruction](../assets/3d-generation.svg)

### Tương tự: 3D Gaussian Splatting (Kerbl et al., 2023)

Tụt họa một cảnh như một đám mây của Gaussia 3D ~ 1M. Mỗi một trong số đó có 59 tham số: vị trí (3), tính hợp (6, hoặc quaternion 4 + thang 3), độ không sáng (1), màu sắc hòa âm hình cầu (48 ở độ 3, 3 ở độ 0).

Đưa ra = chiếu + alpha-composing. Nhanh (~ 100 fps ở 1080p trên 4090). Có thể phân biệt. phù hợp bằng độ giảm theo độ so với ảnh thực tại mặt đất. Một cảnh phù hợp trong 5-30 phút trên GPU tiêu dùng.

Hai đổi mới 2023-2024 trên cùng:
- **Generative Gaussian splats.**Các mô hình như LGM, LRM, InstantMesh dự đoán một đám mây Gaussian trực tiếp từ một hoặc vài hình ảnh.
- **4D Gaussian Splatting.**Gaussians với các bộ chuyển đổi mỗi khung hình cho các cảnh động.

### Phân phối nhiều hình ảnh

Hoạt động tinh chỉnh mô hình phân tán hình ảnh được đào tạo trước để tạo nhiều lượt xem nhất quán của cùng một đối tượng từ một hình ảnh văn bản nhanh chóng hoặc đơn lẻ. Zero123 (Liu et al., 2023), MVDream (Shi et al., 2023), SV3D (Tình ổn định, 2024), CAT3D (Google, 2024). Thông thường phát ra 4-16 lượt xem xung quanh đối tượng, nâng lên 3D thông qua Gaussian splating hoặc NeRF.

### Các đường ống dẫn văn bản đến 3D

| Model | Input | Output | Time |
|-------|-------|--------|------|
| DreamFusion (2022) | text | NeRF via SDS | ~1 hour per asset |
| Magic3D | text | mesh + texture | ~40 min |
| Shap-E (OpenAI, 2023) | text | implicit 3D | ~1 min |
| SJC / ProlificDreamer | text | NeRF / mesh | ~30 min |
| LRM (Meta, 2023) | image | triplane | ~5 s |
| InstantMesh (2024) | image | mesh | ~10 s |
| SV3D (Stability, 2024) | image | novel views | ~2 min |
| CAT3D (Google, 2024) | 1-64 images | 3D NeRF | ~1 min |
| TripoSR (2024) | image | mesh | ~1 s |
| Meshy 4 (2025) | text + image | PBR mesh | ~30 s |
| Rodin Gen-1.5 (2025) | text + image | PBR mesh | ~60 s |
| Tencent Hunyuan3D 2.0 (2025) | image | mesh | ~30 s |

2025-2026 hướng: mô hình văn bản trực tiếp với các vật liệu PBR phù hợp với các động cơ trò chơi.

### NeRF (đối với ngữ cảnh)

Phân xạ thần kinh (Mildenhall et al., 2020).`(x, y, z, view direction)`và sản lượng`(color, density)`. Đưa bằng cách tích hợp dọc theo tia. Thất lượng tổng hợp nhìn mới dựa trên lưới nhưng chậm hơn 100-1000 lần. Được thay thế bởi Gaussian splatting cho hầu hết sử dụng thời gian thực nhưng vẫn chiếm ưu thế trong nghiên cứu.

## Hãy xây dựng nó.
```figure
v4-3d-multiview
```

## Hãy xây dựng nó

`code/main.py`thực hiện một đồ chơi 2D "Gaussian splating" fit: đại diện cho một hình ảnh mục tiêu tổng hợp (một gradient mịn) như là tổng số các điểm Gaussian 2D. Tối ưu hóa vị trí, màu sắc và sự đồng hóa bằng sự giảm gradient để phù hợp với mục tiêu. Bạn thấy hai hoạt động cốt lõi: chuyển tiếp về phía trước (splat + alpha-composite) và phù hợp bằng sự giảm gradient.

### Bước 1: 2D Gaussian splat

```python
def gaussian_at(x, y, gaussian):
    px, py = gaussian["pos"]
    sigma = gaussian["sigma"]
    d2 = (x - px) ** 2 + (y - py) ** 2
    return math.exp(-d2 / (2 * sigma * sigma))
```

### Bước 2: trình bày bằng cách tổng hợp các điểm

```python
def render(image_size, gaussians):
    img = [[0.0] * image_size for _ in range(image_size)]
    for g in gaussians:
        for y in range(image_size):
            for x in range(image_size):
                img[y][x] += g["color"] * gaussian_at(x, y, g)
    return img
```

Trò chơi Gaussian 3D thực sự phân loại Gaussian theo độ sâu và alpha-composites theo thứ tự.

### Bước 3: phù hợp theo độ giảm gradient

```python
for step in range(steps):
    pred = render(size, gaussians)
    loss = mse(pred, target)
    gradients = compute_grads(pred, target, gaussians)
    update(gaussians, gradients, lr)
```

## # Thói bẫy #

- **View inconsistency.**Nếu bạn tạo ra 4 lượt xem độc lập và họ không đồng ý về cấu trúc đối tượng, sự phù hợp 3D là mờ.
- **Back-side hallucination.**Hình ảnh đơn → 3D phải phát minh ra mặt không thấy.
- **Gaussian splat explosion.**Việc đào tạo không hạn chế tăng lên đến 10M chỗ và quá trình.
- **Topology issues.**Các lưới từ các trường ngầm (SDF) thường có lỗ hoặc giao lộ tự.
- **License of training data.**Objaverse có giấy phép hỗn hợp; sử dụng thương mại khác nhau theo mô hình.

## Hãy sử dụng nó để thực hiện

| Task / 任务 | 2026 pick / 2026 选择 |
|------|-----------|
| Scene reconstruction from photos / 照片场景重建 | Gaussian splatting (3DGS, Gsplat, Scaniverse) |
| Text-to-3D object for games / 文本生成游戏 3D | Meshy 4 or Rodin Gen-1.5 (PBR output) |
| Image-to-3D / 图像生成 3D | Hunyuan3D 2.0, TripoSR, InstantMesh |
| Novel-view synthesis from few images / 少样本新视角 | CAT3D, SV3D |
| Dynamic scene reconstruction / 动态场景重建 | 4D Gaussian Splatting |
| Avatar / clothed human / 虚拟人/穿衣人体 | Gaussian Avatar, HUGS |
| Research / SOTA / 研究 | Whatever dropped last week / 上周发布的任何模型 |

Đối với sản xuất hàng hóa 3D trong một trò chơi hoặc đường ống thương mại điện tử: Mesh 4 hoặc Rodin Gen-1.5 đầu ra lưới PBR đi thẳng vào Unity / Unreal.

> Trong game hoặc điện thương mại流水线中部署 3D:Meshy 4 hoặc Rodin Gen-1.5 输出可直接用于 Unity/Unreal 的 PBR 网格──

## Chuyển nó đi.

- Cứu lại`outputs/skill-3d-pipeline.md`. Skill lấy một bản tóm tắt 3D (input: text / one image / few images; output: mesh / splat / NeRF; usage: render / game / VR) và đầu ra: pipeline (multi-view diffusion + fit, hoặc direct mesh model), model cơ sở, ngân sách lặp lại, topology post-processing, các kênh vật liệu cần thiết.

## Tập luyện bài tập

1. **Easy.**Đi chạy`code/main.py`với 4, 16, 64 Gaussians.
2. **Medium.**Tăng đến màu Gaussians (RGB). xác nhận tái tạo phù hợp với mô hình màu mục tiêu.
3. **Hard.**Sử dụng gsplat hoặc Nerfstudio, tái tạo một đối tượng thực tế từ 50 bức ảnh chụp.

## Từ khóa  Từ khóa nhanh chóng

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 3D Gaussian Splatting | "3DGS" | Scene as a cloud of 3D Gaussians; differentiable alpha-composite render. |
| NeRF | "Neural radiance field" | MLP that outputs color + density at a 3D point; render by ray integration. |
| Triplane | "Three 2-D planes" | Factor 3D into three 2-D axis-aligned feature grids; cheaper than volumetric. |
| SDS | "Score distillation sampling" | Train 3D model by using 2D-diffusion score as pseudo-gradient. |
| Multi-view diffusion | "Many views at once" | Diffusion model that outputs a batch of consistent camera views. |
| PBR | "Physically-based rendering" | Material with albedo, roughness, metallic, normal channels. |
| Densification | "Grow splats" | 3DGS training heuristic: split / clone splats in high-gradient regions. |

## Lưu ý sản xuất: 3D chưa có nền chia sẻ nào

Không giống như hình ảnh (sự phân tán laten + DiT) và video (spaceotemporal DiT), 3D không có thời gian chạy thống trị duy nhất vào năm 2026.

- **NeRF / triplane.**Inference là ray-marking + một MLP về phía trước cho mỗi mẫu. Một render 5122 đòi hỏi hàng triệu MLP về phía trước.
- **Multi-view diffusion + LRM reconstruction.**Lớp 2 (LRM biến đổi) là một bước đi một bước về phía trước qua các khung cảnh.
- **SDS / DreamFusion.**Tăng cường cho mỗi tài sản, không phải suy luận, xây dựng công việc, không yêu cầu người xử lý.

Đối với hầu hết các sản phẩm 2026, câu trả lời chính xác là "để chạy mô hình phân phối đa dạng xem theo yêu cầu, tái cấu trúc thành 3DGS không đồng bộ, phục vụ 3DGS cho xem thời gian thực". Điều này chia sẻ tải trọng công việc giữa một máy chủ GPU-inference (quá) và một máy tối ưu hóa ngoại tuyến (rút).

## Xem thêm 延伸阅读

- [Mildenhall et al. (2020). NeRF: Representing Scenes as Neural Radiance Fields](https://arxiv.org/abs/2003.08934) NeRF.
- [Kerbl et al. (2023). 3D Gaussian Splatting for Real-Time Radiance Field Rendering](https://arxiv.org/abs/2308.04079)3DGS.
- [Poole et al. (2022). DreamFusion: Text-to-3D using 2D Diffusion](https://arxiv.org/abs/2209.14988) SDS.
- [Liu et al. (2023). Zero-1-to-3: Zero-shot One Image to 3D Object](https://arxiv.org/abs/2303.11328) Zero123.
- [Shi et al. (2023). MVDream](https://arxiv.org/abs/2308.16512) Phân phối nhiều hình ảnh.
- [Hong et al. (2023). LRM: Large Reconstruction Model for Single Image to 3D](https://arxiv.org/abs/2311.04400) LRM.
- [Gao et al. (2024). CAT3D: Create Anything in 3D with Multi-View Diffusion Models](https://arxiv.org/abs/2405.10314) CAT3D.
- [Stability AI (2024). Stable Video 3D (SV3D)](https://stability.ai/research/sv3d) SV3D.
