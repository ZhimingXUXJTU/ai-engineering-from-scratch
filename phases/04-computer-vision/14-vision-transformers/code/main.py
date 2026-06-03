"""
视觉 Transformer (Vision Transformers — ViT)

核心概念：
- ViT：将图像切成 patch，每个 patch 作为一个 token，用标准 Transformer 处理
- Patch 嵌入：线性投影将 patch 展平并映射到嵌入维度
- 位置编码：为每个 patch 添加位置信息（Transformer 本身没有位置概念）
- [CLS] token：全局分类 token，用于图像级预测

AI 对应：
- ViT 是 GPT-4V、Claude Vision、LLaVA 的视觉编码器
- ViT 取代 CNN 成为计算机视觉的基础架构（2021 年至今）
- DINO、DINOv2、SAM、CLIP 等核心模型都基于 ViT
"""

import torch
import torch.nn as nn

class PatchEmbedding(nn.Module):
    def __init__(self, in_channels=3, patch_size=16, dim=192, image_size=64):
        super().__init__()
        assert image_size % patch_size == 0
        self.proj = nn.Conv2d(in_channels, dim, kernel_size=patch_size, stride=patch_size)
        self.num_patches = (image_size // patch_size) ** 2

    def forward(self, x):
        x = self.proj(x)
        return x.flatten(2).transpose(1, 2)


class Block(nn.Module):
    def __init__(self, dim, num_heads, mlp_ratio=4, dropout=0.0):
        super().__init__()
        self.ln1 = nn.LayerNorm(dim)
        self.attn = nn.MultiheadAttention(dim, num_heads, dropout=dropout, batch_first=True)
        self.ln2 = nn.LayerNorm(dim)
        self.mlp = nn.Sequential(
            nn.Linear(dim, dim * mlp_ratio),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(dim * mlp_ratio, dim),
            nn.Dropout(dropout),
        )

    def forward(self, x):
        normed = self.ln1(x)
        a, _ = self.attn(normed, normed, normed, need_weights=False)
        x = x + a
        x = x + self.mlp(self.ln2(x))
        return x


class ViT(nn.Module):
    def __init__(self, image_size=64, patch_size=16, in_channels=3,
                 num_classes=10, dim=192, depth=6, num_heads=3, mlp_ratio=4):
        super().__init__()
        self.patch = PatchEmbedding(in_channels, patch_size, dim, image_size)
        num_patches = self.patch.num_patches
        self.cls_token = nn.Parameter(torch.zeros(1, 1, dim))
        self.pos_embed = nn.Parameter(torch.zeros(1, num_patches + 1, dim))
        self.blocks = nn.ModuleList([Block(dim, num_heads, mlp_ratio) for _ in range(depth)])
        self.ln = nn.LayerNorm(dim)
        self.head = nn.Linear(dim, num_classes)
        nn.init.trunc_normal_(self.pos_embed, std=0.02)
        nn.init.trunc_normal_(self.cls_token, std=0.02)

    def forward(self, x):
        x = self.patch(x)
        cls = self.cls_token.expand(x.size(0), -1, -1)
        x = torch.cat([cls, x], dim=1)
        x = x + self.pos_embed
        for blk in self.blocks:
            x = blk(x)
        return self.head(self.ln(x[:, 0]))


def main():
    torch.manual_seed(0)
    vit = ViT(image_size=64, patch_size=16, num_classes=10, dim=192, depth=6, num_heads=3)
    x = torch.randn(2, 3, 64, 64)

    patches = vit.patch(x)
    print(f"[shapes] input {tuple(x.shape)} -> patches {tuple(patches.shape)}")
    cls = vit.cls_token.expand(x.size(0), -1, -1)
    tokens = torch.cat([cls, patches], dim=1)
    print(f"[shapes] tokens with CLS: {tuple(tokens.shape)}")
    tokens = tokens + vit.pos_embed
    print(f"[shapes] after pos embed: {tuple(tokens.shape)}")
    logits = vit(x)
    print(f"[shapes] output logits:   {tuple(logits.shape)}")
    print(f"[params] total: {sum(p.numel() for p in vit.parameters()):,}")

    with torch.no_grad():
        probs = logits.softmax(-1)
    print(f"[probs row 0 sum]: {probs[0].sum().item():.4f}")


if __name__ == "__main__":
    main()
