"""
实例分割 — Mask R-CNN (Instance Segmentation — Mask R-CNN)

核心概念：
- 实例分割 = 目标检测 + 像素级分割（区分同类不同个体）
- RoIAlign：将不同大小的候选区域精确对齐到固定尺寸特征图
- Mask R-CNN = Faster R-CNN + 掩码分支（并行预测类别、框、掩码）
- 三阶段：RPN 生成候选区域 → RoIAlign 提取特征 → 多头预测

AI 对应：
- Mask R-CNN 广泛用于自动驾驶（区分不同车辆）、机器人抓取、视频抠图
- RoIAlign 技术被 ViT 适配器等方法借鉴
- 实例分割是 COCO 数据集上最全面的视觉任务
"""

import torch
import torch.nn.functional as F
from torchvision.ops import roi_align


def roi_align_single(feature, box, output_size=7, spatial_scale=1 / 16.0):
    C, H, W = feature.shape
    x1, y1, x2, y2 = [c * spatial_scale - 0.5 for c in box]
    bin_w = (x2 - x1) / output_size
    bin_h = (y2 - y1) / output_size

    grid_y = torch.linspace(y1 + bin_h / 2, y2 - bin_h / 2, output_size, device=feature.device)
    grid_x = torch.linspace(x1 + bin_w / 2, x2 - bin_w / 2, output_size, device=feature.device)
    yy, xx = torch.meshgrid(grid_y, grid_x, indexing="ij")

    gx = 2 * (xx + 0.5) / W - 1
    gy = 2 * (yy + 0.5) / H - 1
    grid = torch.stack([gx, gy], dim=-1).unsqueeze(0)
    sampled = F.grid_sample(feature.unsqueeze(0), grid, mode="bilinear",
                            align_corners=False)
    return sampled.squeeze(0)


def compare_with_torchvision_roi_align():
    torch.manual_seed(0)
    feature = torch.randn(1, 16, 50, 50)
    boxes = torch.tensor([[0, 10, 20, 100, 90],
                          [0, 5, 5, 80, 80],
                          [0, 30, 10, 120, 110]], dtype=torch.float32)

    diffs = []
    for b in boxes:
        ours = roi_align_single(feature[0], b[1:].tolist(), output_size=7, spatial_scale=1 / 4)
        theirs = roi_align(
            feature, b.unsqueeze(0),
            output_size=(7, 7),
            spatial_scale=1 / 4,
            sampling_ratio=1,
            aligned=True,
        )[0]
        diffs.append((ours - theirs).abs().max().item())
    return diffs


def load_pretrained_maskrcnn():
    from torchvision.models.detection import (
        maskrcnn_resnet50_fpn_v2, MaskRCNN_ResNet50_FPN_V2_Weights,
    )
    model = maskrcnn_resnet50_fpn_v2(weights=MaskRCNN_ResNet50_FPN_V2_Weights.DEFAULT)
    model.eval()
    return model


def build_custom_maskrcnn(num_classes):
    from torchvision.models.detection import (
        maskrcnn_resnet50_fpn_v2, MaskRCNN_ResNet50_FPN_V2_Weights,
    )
    from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
    from torchvision.models.detection.mask_rcnn import MaskRCNNPredictor

    model = maskrcnn_resnet50_fpn_v2(weights=MaskRCNN_ResNet50_FPN_V2_Weights.DEFAULT)
    in_features = model.roi_heads.box_predictor.cls_score.in_features
    model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)
    in_features_mask = model.roi_heads.mask_predictor.conv5_mask.in_channels
    model.roi_heads.mask_predictor = MaskRCNNPredictor(in_features_mask, 256, num_classes)
    return model


def freeze_backbone(model):
    # torchvision Mask R-CNN's backbone includes the FPN (model.backbone.fpn),
    # so freezing model.backbone.parameters() also freezes the FPN parameters.
    for p in model.backbone.parameters():
        p.requires_grad = False
    return model


def main():
    print("[roi_align] comparing ours vs torchvision.ops.roi_align")
    diffs = compare_with_torchvision_roi_align()
    for i, d in enumerate(diffs):
        print(f"  box {i}: max|diff|={d:.2e}")

    try:
        print("\n[pretrained] loading maskrcnn_resnet50_fpn_v2 (downloads on first run)")
        model = load_pretrained_maskrcnn()
        with torch.no_grad():
            p = model([torch.randn(3, 200, 300)])[0]
        print(f"  boxes:  {tuple(p['boxes'].shape)}")
        print(f"  labels: {tuple(p['labels'].shape)}")
        print(f"  masks:  {tuple(p['masks'].shape)}")

        print("\n[fine-tune setup] swap heads for 5-class dataset, freeze backbone")
        custom = build_custom_maskrcnn(num_classes=5)
        custom = freeze_backbone(custom)
        trainable = sum(p.numel() for p in custom.parameters() if p.requires_grad)
        total = sum(p.numel() for p in custom.parameters())
        print(f"  trainable: {trainable:,}   total: {total:,}")
    except Exception as e:
        print(f"[pretrained] skipped: {e}")


if __name__ == "__main__":
    main()
