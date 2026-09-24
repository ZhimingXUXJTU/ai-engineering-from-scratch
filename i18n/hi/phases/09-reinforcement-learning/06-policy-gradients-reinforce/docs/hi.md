# नीति ग्रेडिएंट  स्क्रैच से पुनर्मूल्यांकन  रणनीति梯度  शून्य से पुनर्मूल्यांकन 

> मूल्य अनुमान करना बंद करें। नीति को सीधे पैरामीटर करें, अपेक्षित रिटर्न की ग्रेडिएंट की गणना करें, ऊपर की ओर कदम रखें। विलियम्स (1992) ने इसे एक प्रमेय में लिखा। यही कारण है कि पीपीओ, जीआरपीओ और हर एलएलएम आरएल लूप मौजूद हैं।

> **【中文解读】**️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️`∇J(θ) = E[G · ∇log π_θ(a|s)]` यह पीपीओ GRPO  तथा सभी बड़े मॉडल आरएल प्रशिक्षण चक्रों के अस्तित्व का कारण है

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 3 · 03 (Backpropagation), Phase 9 · 03 (Monte Carlo), Phase 9 · 04 (TD Learning) | **前置知识:** Phase 3 · 03 (反向传播), Phase 9 · 03 (蒙特卡洛), Phase 9 · 04 (TD 学习)
**Time:** ~75 minutes | **时间:** ~75 分钟

## समस्या  समस्या परिचय

Q-learning और DQN *value* फ़ंक्शन को पैरामीटर करते हैं। आप क्रियाओं को `argmax Q`. यह अलग क्रियाओं और अलग राज्यों के लिए ठीक है. यह टूट जाता है जब क्रियाएं निरंतर हैं (जो`argmax`10 आयामी टोक़ पर? या जब आप स्टोकास्टिक नीति चाहते हैं (`argmax`संरचना द्वारा निर्धारक है) ।

> Q-learning 和 DQN 参数化* मूल्य* फ़ंक्शन──通过 `argmax Q`选择动作── यह अलग-अलग गति और अलग-अलग स्थिति के लिए कोई समस्या नहीं है── लेकिन जब गति निरंतर होती है तो 10 维力矩上取哪个?`argmax`?) या आवश्यकता के साथ रणनीति`argmax`स्वाभाविक रूप से निश्चित है), तो हम टूट गए हैं.

नीति ग्रेडिएंट्स इसके बजाय नीति को पैरामीटर करते हैं। `π_θ(a | s)`एक तंत्रिका नेटवर्क है जो कार्यों पर वितरण आउटपुट करता है. कार्रवाई करने के लिए नमूना से. अपेक्षाकृत रिटर्न के संबंध में ग्रेडिएंट की गणना करें`θ`. . कदम ऊपर चढ़ना.`argmax`कोई बेलमैन पुनरावृत्ति नहीं है, बस ग्रेडिएंट वृद्धि पर`J(θ) = E_{π_θ}[G]`. .

> 策略梯度改为参数化*策略*`π_θ(a | s)`                                                                                                                                                                                                                                                              `θ`                                                                                                                                                                                                                                                              `argmax`                                                                                                                                                                                                                                                              `J(θ) = E_{π_θ}[G]`ऊपर से ऊपर की तरफ़ बढ़ना

REINFORCE प्रमेय (विलियम्स 1992) आपको बताता है कि यह ग्रेडिएंट गणना योग्य हैः `∇J(θ) = E_π[ G · ∇_θ log π_θ(a | s) ]`एक एपिसोड चलाओ, रिटर्न की गणना करें, गुणा करें`∇ log π_θ(a | s)`हर कदम पर औसत, ग्रेडिएंट-आसेंट, किया गया।

> विल्यम्स 1992) हमें बताएं कि यह डिग्री गणना योग्य हैः`∇J(θ) = E_π[ G · ∇_θ log π_θ(a | s) ]`◊运行一个回合――计算回报――每步乘以 `∇ log π_θ(a | s)`取平均──梯度上升──完成──

2026 में LLM-RL के प्रत्येक एल्गोरिथ्म PPO, DPO, GRPO  में REINFORCE का एक परिष्करण है। इसे अपनी उंगलियों में समझना इस चरण के बाकी हिस्सों के लिए और चरण 10 · 07 (RLHF कार्यान्वयन) और चरण 10 · 08 (DPO) के लिए एक पूर्व शर्त है।

> 2026 के प्रत्येक LLM-RL 算法PPO、DPO、GRPO सभी REINFORCE के परिष्कृत हैं। इसे इस चरण के अवशिष्ट भाग तथा चरण 10 · 07 RLHF 实现) और चरण 10 · 08 DPO) के पूर्वानुमानों तक पहुंचाने के लिए।

> **【中文解读】**策略梯度 के मूल विचार: प्रत्यक्ष अनुकूलन रणनीति तत्व θ, 让高回报的动作概率增加大、低回报的动作概率减少──`∇log π`यानि "क्रांति के दिशा निर्देश" से गुणा करके "अच्छा दिशा में चलना"

> **【拓展：PPO→ChatGPT对齐】**ChatGPT के RLHF  प्रशिक्षण का उपयोग करने वाले पीपीओ 算法, असल में है REINFORCE + क्रिटिकल 基线 + विश्वास域剪──`loss = -advantage * log_prob`यह कोड लाइन, लगभग सभी 2026 साल के बड़े मॉडल आरएल प्रशिक्षण स्क्रिप्ट में दिखाई देती है।

## अवधारणा का मूल अवधारणा

![Policy gradient: softmax policy, log-π gradient, return-weighted update](../assets/policy-gradient.svg)

**The policy gradient theorem.**किसी भी नीति के लिए `π_θ` द्वारा पैरामीटर`θ`:

`∇J(θ) = E_{τ ~ π_θ}[ Σ_{t=0}^{T} G_t · ∇_θ log π_θ(a_t | s_t) ]`

कहाँ`G_t = Σ_{k=t}^{T} γ^{k-t} r_{k+1}` से छूट प्राप्त रिटर्न है`t`. उम्मीद पूरी पगड़ी से आगे है `τ``π_θ`. .

> **策略梯度定理。**किसी भी चीज़ के लिए`θ`参数化策略 `π_θ`, रिटर्न की उम्मीद की तरक्की के बराबर हैः रिटर्न की छूट और संख्यात्मक रणनीति की तरक्की की उम्मीद को गुणा करना।`π_θ`采样完整轨迹上取──

**The proof is short.**अंतर करें `J(θ) = Σ_τ P(τ; θ) G(τ)`उपयोग `∇P(τ; θ) = P(τ; θ) ∇ log P(τ; θ)`(लॉग-उत्पादक चाल) कारक `log P(τ; θ) = Σ log π_θ(a_t | s_t) + environment terms that do not depend on θ`पर्यावरण शब्द गायब हो जाते हैं बीजगणित की दो पंक्तियों आपको प्रमेय देते हैं।

> **证明很短。**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `J(θ)`求导──使用对数导数技巧──将 `log P(τ; θ)`इस पर दो सूत्रों का निर्धारण किया गया है।

**Variance reduction tricks.**वैनिला रिइनफोर्स में हत्यारा विसंगति है  रिटर्न शोर है, `∇ log π`दो मानक फिक्सः

> **方差降低技巧。**मूल पुनर्जागरण में भारी अंतर है,`∇ log π`शोर है, उनकी संख्या शोर से अधिक है।

1. **Baseline subtraction.**प्रतिस्थापन`G_t`के साथ`G_t - b(s_t)`किसी भी आधार रेखा के लिए `b(s_t)`जो निर्भर नहीं करता है `a_t`. निष्पक्ष क्योंकि`E[b(s_t) · ∇ log π(a_t | s_t)] = 0`. विशिष्ट विकल्प: `b(s_t) = V̂(s_t)`एक आलोचक द्वारा सीखा गया → अभिनेता- आलोचक (लक्षण 07) ।
   **基线减法。**उपयोग `G_t - b(s_t)`替换 `G_t`典型选择:`b(s_t) = V̂(s_t)`द्वारा आलोचक 学习 → अभिनेता-आलोचक
2. **Reward-to-go.**प्रतिस्थापन`Σ_t G_t · ∇ log π_θ(a_t | s_t)`के साथ`Σ_t G_t^{from t} · ∇ log π_θ(a_t | s_t)`. केवल भविष्य के रिटर्न ही किसी दिए गए कार्य के लिए मायने रखते हैं  पिछले पुरस्कार शून्य-मध्यम शोर में योगदान देते हैं।
   **未来回报。** केवल भविष्य के प्रतिफल के लिए ही किसी निश्चित गतिविधि में अर्थपूर्ण  अतीत के पुरस्कार योगदान शून्य औसत मूल्य शोर

संयुक्त रूप से, आप प्राप्त करते हैंः

`∇J ≈ (1/N) Σ_{i=1}^{N} Σ_{t=0}^{T_i} [ G_t^{(i)} - V̂(s_t^{(i)}) ] · ∇_θ log π_θ(a_t^{(i)} | s_t^{(i)})`

जो कि एक बेसलाइन के साथ REINFORCE है  A2C (लक्ष्य 07) और PPO (लक्ष्य 08) का प्रत्यक्ष पूर्वज।

**Softmax policy parameterization.**अलग-अलग कार्यों के लिए, मानक विकल्पः

`π_θ(a | s) = exp(f_θ(s, a)) / Σ_{a'} exp(f_θ(s, a'))`

कहाँ`f_θ`किसी भी तंत्रिका जाल है जो प्रति क्रिया एक स्कोर आउटपुट करता है। ग्रेडिएंट का एक साफ रूप हैः

`∇_θ log π_θ(a | s) = ∇_θ f_θ(s, a) - Σ_{a'} π_θ(a' | s) ∇_θ f_θ(s, a')`

यानी, किए गए कार्य के स्कोर को पॉलिसी के अंतर्गत इसके अपेक्षित मूल्य के घटाकर।

> **Softmax 策略参数化。**                                                                                                                                                                                                                                                              

**Gaussian policy for continuous actions.** `π_θ(a | s) = N(μ_θ(s), σ_θ(s))`. .`∇ log N(a; μ, σ)`चरण 9 · 07 के एसएसी की जरूरतें हैं।

> **连续动作的高斯策略。** `∇ log N(a; μ, σ)`वहाँ एक बंद समाधान है। यह सब चरण 9 · 07 के एसएसी की आवश्यकता है।

## इसे बनाओ, इसे पूरा करो।
```figure
policy-gradient-landscape
```

## इसे बनाओ

### चरण 1: softmax नीति नेटवर्क

```python
def policy_logits(theta, state_features):
    return [dot(theta[a], state_features) for a in range(N_ACTIONS)]

def softmax(logits):
    m = max(logits)
    exps = [exp(l - m) for l in logits]
    Z = sum(exps)
    return [e / Z for e in exps]
```

एक तालिकात्मक परिवेश के लिए एक रैखिक नीति (प्रति क्रिया एक वजन वेक्टर) का उपयोग करें। एटारी के लिए, सीएनएन में स्विप करें और सॉफ्टमैक्स सिर रखें।

> 表格环境使用线性策略( प्रत्येक动作一个权重向量) ⋅ ATARI के लिए, CNN में स्विच करें और सॉफ्टमैक्स ⋅ को बनाए रखें

### चरण 2: नमूनाकरण और लॉग-प्रभाव्यता

```python
def sample_action(probs, rng):
    x = rng.random()
    cum = 0
    for a, p in enumerate(probs):
        cum += p
        if x <= cum:
            return a
    return len(probs) - 1

def log_prob(probs, a):
    return log(probs[a] + 1e-12)
```

### चरण 3: लॉग-प्रोब्स कैप्चर के साथ रोलआउट

```python
def rollout(theta, env, rng, gamma):
    trajectory = []
    s = env.reset()
    while not done:
        logits = policy_logits(theta, s)
        probs = softmax(logits)
        a = sample_action(probs, rng)
        s_next, r, done = env.step(s, a)
        trajectory.append((s, a, r, probs))
        s = s_next
    return trajectory
```

### चरण 4: REINFORCE अद्यतन

```python
def reinforce_step(theta, trajectory, gamma, lr, baseline=0.0):
    returns = compute_returns(trajectory, gamma)
    for (s, a, _, probs), G in zip(trajectory, returns):
        advantage = G - baseline
        grad_log_pi_a = [-p for p in probs]
        grad_log_pi_a[a] += 1.0
        for i in range(N_ACTIONS):
            for j in range(len(s)):
                theta[i][j] += lr * advantage * grad_log_pi_a[i] * s[j]
```

ग्रेडिएंट `∇ log π(a|s) = e_a - π(·|s)`(केवल `a`-संभावनाओं) softmax नीति gradients का दिल है. मांसपेशियों स्मृति में जला.

> 梯度 `∇ log π(a|s) = e_a - π(·|s)`(`a`                                                                                                                                                                                                                                                              

### चरण 5: आधार रेखाएँ

`G`हाल के एपिसोड पर 4 × 4 ग्रिडवर्ल्ड चलाने के लिए पर्याप्त भिन्नता में कमी है; यह करीब 500 एपिसोड को एक साथ लाने के लिए लेता है। मूल रेखा को एक सीखा गया तक अपग्रेड करें `V̂(s)`और आप अभिनेता-आलोचक प्राप्त करते हैं।

> हाल ही में`G`के परिचालन औसत मूल्य पर्याप्त है 4×4 ग्रिडवर्ल्ड 工作; लगभग 500 回合收──将基线升级为学习的 `V̂(s)`मुझे अभिनेता-आलोचना मिली।

## फंदे

- **Exploding gradients.**रिटर्न बहुत बड़ा हो सकता है. हमेशा सामान्य हो जाओ.`G``~N(0, 1)``∇ log π`. .
  **梯度爆炸。** 回报可能很大──在乘以 `∇ log π`之前始终将 `G`归一化到 `~N(0, 1)`
- **Entropy collapse.**नीति बहुत जल्दी एक लगभग निर्धारक कार्रवाई के लिए अभिसरण, खोज बंद कर देता है, फिक्स्ड हो जाता है: जोड़ें एंट्रोपी बोनस`β · H(π(·|s))`लक्ष्य के लिए।
  **熵坍缩。**策略过早收到近确定性动作,停止探索,陷入困境──修复:向目标添加奖励 `β · H(π(·|s))`
- **High variance.**वैनिला रीइनफोर्स को हजारों एपिसोड की आवश्यकता होती है। एक आलोचक बेसलाइन (पढ़ें 07) या TRPO/PPO का ट्रस्ट क्षेत्र (पढ़ें 08) मानक फिक्स है।
  **高方差。**️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️
- **Sample inefficiency.**नीति पर एक अपडेट के बाद आप हर संक्रमण को फेंक देते हैं। महत्व के नमूने के माध्यम से नीति के बाहर सुधार डेटा को वापस लाता है, भिन्नता की लागत पर (पीपीओ का अनुपात एक कटौती आईएस वजन है) ।
  **样本效率低。**ऑनलाइन रणनीति का अर्थ है प्रत्येक अपडेट के बाद सभी स्थानांतरणों को त्याग देना।
- **Non-stationary gradients.**100 एपिसोड पहले से ही ग्रेडिएंट पुराने का उपयोग करता है `π`नीतिगत तरीकों को हर कुछ रोलआउट के लिए अद्यतन किया जाता है इस कारण से।
  **非平稳梯度。**100 回合前的梯度使用旧的 `π`                                                                                                                                                                                                                                                              
- **Credit assignment.**बिना इनाम-टू-गो के, पिछले इनामों शोर का योगदान देते हैं। हमेशा इनाम-टू-गो का उपयोग करें।
  **信用分配。**没有未来回报,过去的奖励贡献噪声──始终使用未来回报──

## इसे फ्रेमवर्क के साथ लागू करें

2026 में, REINFORCE को शायद ही कभी सीधे चलाया जाता है लेकिन इसका ग्रेडिएंट सूत्र हर जगह हैः

> 2026 साल,REINFORCE  बहुत कम सीधे संचालन, लेकिन इसकी तरक्की सूत्र मौजूद नहीं हैः

| Use case | Derived method |
|----------|---------------|
| Use case / 用例 | Derived method / 派生方法 |
| Continuous control / 连续控制 | PPO / SAC with Gaussian policy / 高斯策略的 PPO/SAC |
| LLM RLHF / LLM RLHF | PPO with KL penalty, running on token-level policy / 带 KL 惩罚的 PPO，token 级策略 |
| LLM reasoning (DeepSeek) / LLM 推理 | GRPO — REINFORCE with group-relative baseline, no critic / 组相对基线的 REINFORCE，无 critic |
| Multi-agent / 多智能体 | Centralized-critic REINFORCE (MADDPG, COMA) / 集中 critic 的 REINFORCE |
| Discrete action robotics / 离散动作机器人 | A2C, A3C, PPO |
| Preference-only settings / 仅偏好设置 | DPO — REINFORCE rewritten as a preference-likelihood loss, no sampling / 重写为偏好似然损失的 REINFORCE |

जब आप पढ़ते हैं`loss = -advantage * log_prob`एक 2026 प्रशिक्षण स्क्रिप्ट में, जो एक बेसलाइन के साथ REINFORCE है। पूरे पेपर (DPO, GRPO, RLOO) इस एक पंक्ति के शीर्ष पर भिन्नता-संकलन ट्रिक्स हैं।

> जब आप 2026 के प्रशिक्षण के लिए स्क्रिप्ट में पढ़ते हैं`loss = -advantage * log_prob`,that's带基线的 REINFORCE──整篇论文(DPO、GRPO、RLOO) सभी इस कोड पर अंतर कम करने की तकनीक में हैं──

## इसे भेजें उत्पाद

`outputs/skill-policy-gradient-trainer.md`:

```markdown
---
name: policy-gradient-trainer
description: Produce a REINFORCE / actor-critic / PPO training config for a given task and diagnose variance issues.
version: 1.0.0
phase: 9
lesson: 6
tags: [rl, policy-gradient, reinforce]
---

Given an environment (discrete / continuous actions, horizon, reward stats), output:

1. Policy head. Softmax (discrete) or Gaussian (continuous) with parameter counts.
2. Baseline. None (vanilla), running mean, learned `V̂(s)`, or A2C critic.
3. Variance controls. Reward-to-go on by default, return normalization, gradient clip value.
4. Entropy bonus. Coefficient β and decay schedule.
5. Batch size. Episodes per update; on-policy data freshness contract.

Refuse REINFORCE-no-baseline on horizons > 500 steps. Refuse continuous-action control with a softmax head. Flag any run with `β = 0` and observed policy entropy < 0.1 as entropy-collapsed.
```

## अभ्यास विषय

1. **Easy.**रैखिक सॉफ्टमैक्स नीति के साथ 4 × 4 ग्रिडवर्ल्ड पर REINFORCE लागू करें। बिना बेसलाइन के 1,000 एपिसोड के लिए प्रशिक्षित करें। सीखने की वक्र का पता लगाएं; भिन्नता (प्रतिफल का एसटीडी) मापें।
2. **Medium.**एक रन-मीडियन बेसलाइन जोड़ें. फिर से ट्रेन करें. वैनिला रन के साथ नमूना दक्षता और भिन्नता की तुलना करें. बेसलाइन अभिसरण के चरणों को कितना कम करती है?
3. **Hard.**एक एंट्रोपी बोनस जोड़ें `β · H(π)`. . .`β ∈ {0, 0.01, 0.1, 1.0}`इस कार्य में सबसे अच्छा स्थान कहाँ है?

## कीवर्ड्स  शब्द खोज तालिका

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Policy gradient | "Train the policy directly" / 策略梯度 | `∇J(θ) = E[G · ∇ log π_θ(a\|s)]`; derived from the log-derivative trick. |
| REINFORCE | "The original PG algorithm" / REINFORCE算法 | Williams (1992); Monte Carlo returns multiplied by log-policy gradient. |
| Log-derivative trick | "Score function estimator" / 对数导数技巧 | `∇P(τ;θ) = P(τ;θ) · ∇ log P(τ;θ)`; makes gradients of expectations tractable. |
| Baseline | "Variance reduction" / 基线 | Any `b(s)` subtracted from `G`; unbiased because `E[b · ∇ log π] = 0`. |
| Reward-to-go | "Only future returns count" / 未来回报 | `G_t^{from t}` instead of the full `G_0`; correct and lower-variance. |
| Entropy bonus | "Encourage exploration" / 熵正则化 | `+β · H(π(·\|s))` term keeps the policy from collapsing. |
| On-policy | "Train on what you just saw" / 在线策略 | Gradient expectation is w.r.t. the current policy — cannot reuse old data directly. |
| Advantage | "How much better than average" / 优势函数 | `A(s, a) = G(s, a) - V(s)`; the signed quantity REINFORCE-with-baseline multiplies. |

## आगे पढ़ना 延伸閱讀

- [Williams (1992). Simple Statistical Gradient-Following Algorithms for Connectionist Reinforcement Learning](https://link.springer.com/article/10.1007/BF00992696) मूल REINFORCE पेपर।
- [Sutton et al. (2000). Policy Gradient Methods for Reinforcement Learning with Function Approximation](https://papers.nips.cc/paper_files/paper/1999/hash/464d828b85b0bed98e80ade0a5c43b0f-Abstract.html) फंक्शन अप्रोक्सिमेशन के साथ आधुनिक नीति-ग्रेडिएंट प्रमेय।
- [Sutton & Barto (2018). Ch. 13 — Policy Gradient Methods](http://incompleteideas.net/book/RLbook2020.pdf) पाठ्यपुस्तक प्रस्तुत करना।
- [OpenAI Spinning Up — VPG / REINFORCE](https://spinningup.openai.com/en/latest/algorithms/vpg.html) PyTorch कोड के साथ स्पष्ट शैक्षणिक व्याख्या।
- [Peters & Schaal (2008). Reinforcement Learning of Motor Skills with Policy Gradients](https://homes.cs.washington.edu/~todorov/courses/amath579/reading/PolicyGradient.pdf) भिन्नता-संशोधन और प्राकृतिक-ग्रिडिएंट दृष्टिकोण जो REINFORCE को ट्रस्ट-क्षेत्र परिवार (TRPO, PPO) से जोड़ता है।
