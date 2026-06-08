# ❓ 常见问题 (FAQ)

> 学习过程中遇到问题？先看这里。

---

## 环境问题

### Q: Python 装不上怎么办？

**推荐**：使用 [Miniconda](https://docs.conda.io/en/latest/miniconda.html)，比 Anaconda 轻量很多。

```bash
# 安装 Miniconda 后
conda create -n ai-learning python=3.11
conda activate ai-learning
```

**替代方案**：直接用 [Google Colab](https://colab.research.google.com/)（免费在线 Python 环境，免安装）。

### Q: pip install 报错怎么办？

```bash
# 常见原因1：网络问题（国内用户）
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple <包名>

# 常见原因2：版本冲突
pip install --upgrade pip
pip install <包名> --no-deps  # 不装依赖，单独装

# 常见原因3：权限问题（Windows）
pip install <包名> --user
```

### Q: 没有 GPU 能学吗？

**完全可以。** Phase 0-3 的所有代码都不需要 GPU，普通笔记本就行。

需要 GPU 的阶段（Phase 4+），可以使用：
- **Google Colab**（免费 GPU）
- **Kaggle Notebooks**（免费 GPU，每周 30 小时）
- **AutoDL / 矩池云**（国内 GPU 租赁，几毛钱一小时）

### Q: Windows 上运行报错怎么办？

常见问题及解决方案：

| 错误 | 原因 | 解决 |
|------|------|------|
| `ModuleNotFoundError` | 没装这个包 | `pip install <模块名>` |
| `SyntaxError` | Python 版本太低 | 需要 Python 3.10+ |
| 路径中有中文 | 部分库不支持中文路径 | 把项目放到纯英文路径下 |
| `Permission denied` | 权限不足 | 用管理员权限运行，或 `--user` 安装 |

### Q: Jupyter Notebook 打不开？

```bash
# 方法1：命令行启动
jupyter notebook

# 方法2：用 VS Code 打开 .ipynb 文件（推荐）

# 方法3：用 Google Colab 替代
```

---

## 学习问题

### Q: 数学公式看不懂怎么办？

1. **先看代码**：Phase 1 的每节数学课都有对应的 Python 代码。数学公式和代码是一一对应的
2. **看中文解读**：每个英文段落后都有灰色块（`>`）的中文翻译
3. **用 AI 辅助**：把公式粘贴到 ChatGPT/Claude，让它用中文解释
4. **跳过再回来**：暂时跳过，学完后面回来再看会更容易理解

### Q: 代码跑不通怎么办？

1. **检查依赖**：`pip install -r requirements.txt`
2. **看错误信息**：最后一行通常告诉了你问题所在
3. **搜索错误**：把错误信息复制到 Google/百度搜索
4. **问 AI**：把错误信息和代码一起发给 ChatGPT/Claude
5. **跳过**：某些代码可能需要特定硬件/数据，跳过不影响理解

### Q: 应该按什么顺序学？

参考 [学习路线图](学习路线图.md)，一般按 Phase 0 → 1 → 2 → 3 的顺序。

如果你有特定目标（比如只想学 LLM 应用），路线图里有"特殊学习路径"推荐。

### Q: 每天学多少合适？

- **推荐**：每天 1-2 小时，每周 5-7 天
- **不建议**：周末突击 10 小时（效果差，容易放弃）
- **节奏**：每节课 45-75 分钟，正好是一天的量

### Q: 需要看完每一节课吗？

**不需要。** 根据你的目标选择：
- 只想了解 AI 原理 → Phase 0-3 足够
- 想做 LLM 应用 → Phase 0-3 + 7 + 11
- 想做 AI Agent → 再加上 Phase 13-14

### Q: 英文不好能学吗？

**完全可以。** 本仓库提供了：
- 每个英文段落后的中文翻译（灰色块）
- 双语标题和元数据
- 代码文件的中文注释
- 【中文解读】深入解释
- 【拓展】补充知识点

---

## 工具问题

### Q: Git 怎么用？

```bash
# 克隆仓库
git clone https://github.com/rohitg00/ai-engineering-from-scratch.git

# 更新到最新
cd ai-engineering-from-scratch
git pull

# 如果你想用中文翻译版
git clone -b main-zh https://github.com/ZhimingXUXJTU/ai-engineering-from-scratch.git
```

### Q: VS Code 怎么配置？

推荐安装以下插件：
- **Python**（Microsoft）— Python 语言支持
- **Jupyter**（Microsoft）— 在 VS Code 中运行 Notebook
- **Markdown All in One** — 预览 Markdown 课程文档
- **Chinese Language Pack** — 中文界面

### Q: 怎么阅读 en.md 文件？

en.md 是 Markdown 格式的文本文件。你可以：
1. 在 GitHub 上直接浏览（自动渲染）
2. 用 VS Code 打开（右键 → "打开预览"）
3. 用 Typora 等 Markdown 编辑器打开
4. 在线浏览：[aiengineeringfromscratch.com](https://aiengineeringfromscratch.com)

### Q: 怎么运行 .py 代码文件？

```bash
# 进入代码目录
cd phases/01-math-foundations/01-linear-algebra-intuition/code/

# 运行
python vectors.py

# 如果有依赖问题
pip install numpy matplotlib
python vectors.py
```

---

## 内容问题

### Q: 术语表在哪里？

→ [glossary/terms.md](glossary/terms.md)，包含 83 个 AI 核心术语的通俗解释（英文原文，需要一定英文基础）。

### Q: 每节课的代码在哪里？

```
phases/<阶段号>-<阶段名>/<课程号>-<课程名>/code/
```

例如 Phase 1 第 1 课的代码：
```
phases/01-math-foundations/01-linear-algebra-intuition/code/vectors.py
```

### Q: 练习题有答案吗？

课程中的 Exercises 是开放式练习，没有标准答案。建议：
1. 先自己尝试
2. 参考同目录下 `code/` 中的实现
3. 不确定的话，把你的解答发给 AI 助手帮你检查

### Q: Further Reading 的资源都是英文的，怎么办？

1. 用浏览器翻译插件（推荐：沉浸式翻译）
2. 搜索中文替代资源（知乎、CSDN、B站）
3. 优先理解课程本身的内容，延伸阅读是可选的

---

## 仍然无法解决？

1. 在 GitHub 上提 [Issue](https://github.com/rohitg00/ai-engineering-from-scratch/issues)
2. 把你的问题 + 错误信息发给 ChatGPT/Claude
3. 搜索相关技术社区（Stack Overflow、知乎、V2EX）
