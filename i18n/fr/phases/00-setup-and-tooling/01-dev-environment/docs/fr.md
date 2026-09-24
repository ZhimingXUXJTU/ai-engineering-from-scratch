# Développer l'environnement développer l'environnement construire

> Vos outils façonnent votre pensée.

> **【中文解读】**Votre outil forme votre pensée  Une fois pour toutes, une fois pour toutes. Le chapitre est le point de départ de tout le cours: vous construirez un ensemble complet d'environnement de développement d'IA (Python, Node.js, Rust 工具链), et vérifiez si la GPU accélère ou non la possibilité de l'utiliser.

**Type:** Build | **类型:** 构建
**Languages:** Python, Node.js, Rust | **语言:** Python, Node.js, Rust
**Prerequisites:** None | **前置知识:** 无
**Time:** ~45 minutes | **时间:** ~45 分钟

## Objectifs d'apprentissage

- Configurez Python 3.11+, Node.js 20+ et Rust à partir de zéro
  Le code de Python 3.11+
- Configurer des environnements virtuels et des gestionnaires de paquets pour les constructions reproducibles
  Traduction anglaise: configuration d'environnement virtuel et de pack manager, assurer la construction réalisable
- Vérifiez l'accès à la GPU avec CUDA/MPS et effectuez une opération de test tenseur
  Le nombre de personnes concernées par la procédure de transfert est supérieur à celui de la personne concernée par la procédure de transfert.
- Comprendre la pile à quatre couches: système, paquets, temps d'exécution, bibliothèques d'IA
  Le langage est le langage de la langue, le langage de la langue, le langage de la langue.

## Le problème .

Vous allez apprendre l'ingénierie de l'IA sur plus de 500 leçons en utilisant Python, TypeScript, Rust et Julia. Si votre environnement est cassé, chaque leçon devient une lutte contre l'outillage au lieu d'apprendre.

> Vous allez passer 500 cours sur l'apprentissage de l'ingénierie de l'IA, en Python, TypeScript, Rust et Julia. Si votre environnement a des problèmes, chaque cours deviendra un outil de lutte intellectuelle, et non un outil d'apprentissage.

La plupart des gens sautent la configuration de l'environnement, puis passent des heures à déboguer les erreurs d'importation, les conflits de version et les pilotes CUDA manquants.

> La plupart des gens ont sauté sur l'environnement construit. Ils ont passé quelques heures à tester l'importation de l'erreur.

> **【中文解读】**
> 环境问题是你遇到"import error""",版本冲突""",找不到 CUDA"等报错的根本原因──与其每次上课都修环境,不如一次性搭好──

## Le concept de base.

Un environnement d'ingénierie AI a quatre couches:

> L'environnement de l'IA est divisé en quatre niveaux:

```mermaid
graph TD
    A["4. AI/ML Libraries\nPyTorch, JAX, transformers, etc."] --> B["3. Language Runtimes\nPython 3.11+, Node 20+, Rust, Julia"]
    B --> C["2. Package Managers\nuv, pnpm, cargo, juliaup"]
    C --> D["1. System Foundation\nOS, shell, git, editor, GPU drivers"]
```

Nous installons en bas vers le haut. Chaque couche dépend de celle qui est sous elle.

> Nous sommes installés en bas. Chaque étage dépend de la couche inférieure.

> **【中文解读】**
> L'environnement d'ingénierie de l'IA est un cadre de quatre niveaux: le plus bas est le système d'exploitation et le pilotage, le plus haut est le gestionnaire de paquets, le plus haut est le langage, le plus haut est le pyTorch, les transformateurs, etc.

> **【拓展：为什么需要 uv 而不是 pip？】**
> uv est un Python pack manager écrit par Rust, qui peut gérer automatiquement l'environnement virtuel. Dans les projets d'IA réels, vous pouvez également maintenir plusieurs projets en fonction de la dépendance.
```figure
s0-env-stack
```

## Construisez-le à la main.

> **【中文解读】**Vous pouvez utiliser les outils de mise en place de quatre niveaux. Chaque étape peut être directement copiée et collationnée jusqu'au terminal. Si vous utilisez Windows, vous pouvez utiliser WSL2 (Windows Subsystem for Linux) pour obtenir Linux.

### Étape 1: Fondation du système.

Vérifiez votre système et installez les bases.

> 检查你的系统并安装基础工具──

```bash
# macOS
xcode-select --install
brew install git curl wget

# Ubuntu/Debian
sudo apt update && sudo apt install -y build-essential git curl wget

# Windows (use WSL2)
wsl --install -d Ubuntu-24.04
```

### Étape 2: Python avec UV.

On utilise`uv`Il est 10 à 100 fois plus rapide que le pip et gère automatiquement les environnements virtuels.

> Nous utilisons`uv`Il est 10 à 100 fois plus rapide que le pip, et peut gérer automatiquement l'environnement virtuel.

> **【拓展：Python 版本选择】** Python 3.12                                                                                                                                                                                                                                                             `python install`会自动下载和管理 Python 版本, plus besoin de pyenv.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh

uv python install 3.12

uv venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

uv pip install numpy matplotlib jupyter
```

Vérifiez:

> 验证安装:

```python
import sys
print(f"Python {sys.version}")

import numpy as np
print(f"NumPy {np.__version__}")
a = np.array([1, 2, 3])
print(f"Vector: {a}, dot product with itself: {np.dot(a, a)}")
```

### Étape 3: Node.js avec pnpm

> **【中文解读】**Node.js est le type de type script.

Pour les leçons de typeScript (agents, serveurs MCP, applications Web).

> Utilisé dans le typeScript  cours(Agent、MCP  serveur、Web 应用)

```bash
curl -fsSL https://fnm.vercel.app/install | bash
fnm install 22
fnm use 22

npm install -g pnpm

node -e "console.log('Node', process.version)"
```

**macOS / Apple Silicon (M1/M2/M3/M4):**Si l' installateur arrête de`Error: Cannot install under Rosetta 2 in ARM default prefix (/opt/homebrew)`Votre terminal est sous Rosetta 2 (`arch`des empreintes`i386`Installez l'arm64 à force de fnm, branchez-le dans votre coquille, puis réalisez les commandes ci-dessus à partir de`fnm install 22`- Le numéro de la liste:

> **苹果芯片 Mac 用户注意**Si l' on trouve un autre type de réception`Error: Cannot install under Rosetta 2 in ARM default prefix (/opt/homebrew)`Je vais vous dire que votre terminal fonctionne sur Rosetta 2.`arch`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `i386`), alors que Homebrew est un modèle original de l'arm64  版本──`fnm install 22`Retourner à la ligne de commande:

```bash
arch -arm64 brew install fnm
echo 'eval "$(fnm env --use-on-cd)"' >> ~/.zshrc
source ~/.zshrc
```

### Étape 4: Rust

Pour les leçons critiques de performance (inférence, systèmes).

> Il est utilisé pour des cours sensibles aux performances (optimisation des systèmes).

> **【中文解读】**La rouille utilise des éléments sensibles aux performances de ce cours, tels que la mise en œuvre de la méthode d'optimisation (Phase 12) et le système autonome (Phase 15-17): la rouille est un appareil de rouille, la charge est un outil de construction (PIP+Make) de la version de rouille.

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

rustc --version
cargo --version
```

### Je suis en train de faire une petite photo de la photo.

Pour des cours de mathématiques où Julia brille.

> Il est utilisé pour Julia pour des cours de mathématiques très intenses.

```bash
curl -fsSL https://install.julialang.org | sh

julia -e 'println("Julia ", VERSION)'
```

### Étape 6: Configuration de la GPU (si vous en avez une)

**NVIDIA (Linux / Windows):**

> **【中文解读】**NVIDIA 显卡先用 `nvidia-smi`确认驱动正常,再安装 CUDA 版 PyTorch; 果芯片 Mac 没有 CUDA 属正常现象直接装默认版 PyTorch(内置 MPS/Metal 后端)即可,不要传 `--index-url .../cuXXX`(Ces roues ne supportent que Linux/Windows, elles ont été ratées)

```bash
nvidia-smi

# Install PyTorch with CUDA
uv pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
```

**macOS / Apple Silicon (M1/M2/M3/M4):**Il n'y a pas de CUDA sur un Mac qui soit attendu, pas un échec.**not**Passer .`--index-url .../cuXXX`Installez la construction simple, qui comprend le backend de la GPU MPS (Metal) d'Apple:

> **macOS / 苹果芯片（M1/M2/M3/M4）**C'est un comportement prévu, pas un problème.`--index-url .../cuXXX`(ceux roues  Linux/Windows seulement,传传传了安装会失败)

```bash
uv pip install torch torchvision torchaudio
```

Vérifiez (fonctionne sur n'importe quelle plateforme):

> 验证(任意平台通用):

```python
import torch
print(f"CUDA available: {torch.cuda.is_available()}")           # False on macOS — expected
print(f"MPS available:  {torch.backends.mps.is_available()}")   # True on Apple Silicon
if torch.cuda.is_available():
    print(f"GPU: {torch.cuda.get_device_name(0)}")
```

La plupart des leçons fonctionnent sur le processeur. Pour les leçons lourdes, utilisez Google Colab ou des GPU en nuage.

> 没有GPU?没关系── La plupart des cours peuvent être effectués sur le CPU── Les cours de grande taille peuvent être utilisés avec Google Colab ou GPU cloud-end──

> **【拓展：GPU vs CPU 性能对比】**訓練 GPT-2 small(117M 参数):CPU 约 7 天,单块 RTX 3090 约 3 小时,A100 约 40 分钟──推理阶段差距略小但仍然显著──本课程大部分课程可用CPU 跑,只有10期(从零训练LLM)等少数课程建议使用GPU──

> **【拓展：GPU 在 AI 中的作用】**
> GPU (graphique processor) est indispensable dans l'IA, car il peut exécuter simultanément des milliers de simples calculs.

### Étape 7: Vérifiez la route que vous voulez commencer.

Exécutez chaque commande dans cette leçon à partir de la racine du référentiel, le répertoire qui
contient `README.md`et `phases/`Le pré-vol ne vérifie que ce dont vous avez besoin .
Il saute les outils ultérieurs par défaut afin qu'un nouvel apprenant voit
une réponse claire au lieu d'un mur d'avertissements.

> Toutes les commandes de ce cours sont contenues dans le répertoire de stockage.`README.md`et `phases/`Le programme de formation est basé sur le programme de formation et de formation.

Commencez la séquence complète des débutants:

> Initialement complet de la séquence des débutants:

```bash
python3 phases/00-setup-and-tooling/01-dev-environment/code/verify.py --route beginner
```

Ou vérifier seulement la route que vous voulez:

> Ou alors, regardez ce que vous voulez apprendre.

```bash
python3 phases/00-setup-and-tooling/01-dev-environment/code/verify.py --route ml-foundations
python3 phases/00-setup-and-tooling/01-dev-environment/code/verify.py --route llm-engineering
python3 phases/00-setup-and-tooling/01-dev-environment/code/verify.py --route agents
python3 phases/00-setup-and-tooling/01-dev-environment/code/verify.py --route mcp
python3 phases/00-setup-and-tooling/01-dev-environment/code/verify.py --route agent-skills
python3 phases/00-setup-and-tooling/01-dev-environment/code/verify.py --route certification
```

Ajouter `--show-later`lorsque vous voulez le même pré-vol pour inspecter des outils optionnels
Les outils de formation sont utilisés dans les cours suivants.
route sélectionnée.

>  faire des examens préalables et des examens ultérieurs  utiliser des outils et des dépendances, en plus `--show-later` Les outils de suite de la défaillance ne vous bloqueront jamais sur le chemin que vous choisissez.

Chaque vérification requise ayant échoué comprend le chemin détecté ou l'erreur d'importation et un
Les compétences des agents et les routes de certification montrent également que les commandes correctives sont exactes.
Les contrôles manuels de l'hôte parce qu'un script Python ne peut pas prouver qu'un hôte AI a
Vous avez découvert une compétence ou que votre domaine d'expertise est réalisable.

> Chaque programme d'inspection indispensable échoué est accompagné d'un chemin ou d'une erreur d'importation, ainsi qu'un ordre de réparation précis.

Quand le pré-vol débutant passe, il imprime la première leçon exécutive:

> Lorsque les étudiants débutants passent le test, le script imprime le premier cours pratique:

```text
Ready to start Beginner course.
Next: python3 phases/01-math-foundations/01-linear-algebra-intuition/code/vectors.py
```

> **【中文解读】**预检脚本是"按路线最小环境"落地:beginner只需要Python和Git,ml-foundations 再加 NumPy,agents/mcp 路线连 Node 都可以先不装用到再装Windows User把命令里 `python3`- Je suis là !`python`Je suis là.

## Utilisez-le avec un guide.

> **【中文解读】**La première édition de la série est consacrée à la conception de la méthode de calcul. La première édition est consacrée à la conception de la méthode de calcul.

Votre environnement est prêt à démarrer le parcours que vous avez vérifié.
quand une leçon demande pour eux au lieu de bloquer votre première leçon dans son ensemble
Voici ce que vous utiliserez dans le programme:

> Votre environnement peut déjà commencer à vous inscrire sur le même chemin. Les outils suivants, etc., jusqu'à ce que le cours soit rechargé, ne laissez pas toute la technologie vous bloquer.

| Language | Used In | Package Manager |
|----------|---------|-----------------|
| Python | Phases 1-12 (ML, DL, NLP, Vision, Audio, LLMs) | uv |
| TypeScript | Phases 13-17 (Tools, Agents, Swarms, Infra) | pnpm |
| Rust | Phases 12, 15-17 (Performance-critical systems) | cargo |
| Julia | Phase 1 (Math foundations) | Pkg |

| 语言 | 用在哪些阶段 | 包管理器 |
|------|------------|---------|
| Python | 阶段 1-12（ML、DL、NLP、视觉、音频、LLM） | uv |
| TypeScript | 阶段 13-17（工具、Agent、集群、基础设施） | pnpm |
| Rust | 阶段 12, 15-17（高性能系统） | cargo |
| Julia | 阶段 1（数学基础） | Pkg |

## Envoyez-le . Produit .

> **【拓展：环境检查 Prompt】** `outputs/prompt-env-check.md`C'est un prompt qui peut être directement donné à l'aide de l'IA, pour vous aider à diagnostiquer les problèmes environnementaux.

Cette leçon produit un script de vérification que tout le monde peut exécuter pour vérifier leur configuration.

> Ce cours est un ouvrage de test, que tout le monde peut utiliser pour vérifier sa propre configuration environnementale.

Regardez !`outputs/prompt-env-check.md`pour une demande qui aide les assistants d'IA à diagnostiquer les problèmes environnementaux.

> 参见 `outputs/prompt-env-check.md`, qui contient une réponse rapide aux problèmes environnementaux de diagnostic d'aide à l'IA.

## Les exercices

1. Exécutez le script de vérification et corrigez les pannes
   运行验证脚本并修复 tous les contrôles ratés
2. Créez un environnement virtuel Python pour ce cours et installez PyTorch
   Pour ce cours Créer Python  Environnement virtuel et installer PyTorch
3. Écrivez un "bonjour au monde" dans les quatre langues et faites fonctionner chacune d'elles.
   En quatre langues, il écrit un "bonjour au monde" et fonctionne.
