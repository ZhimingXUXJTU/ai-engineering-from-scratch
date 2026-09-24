# केस स्टडीज और 2026 की स्टेट ऑफ द आर्ट

> तीन उत्पादन-ग्रेड संदर्भ अंत-से-अंत अध्ययन, प्रत्येक बहु-एजेंट इंजीनियरिंग के एक अलग स्लाइस को दर्शाते हैं। **Anthropic's Research system**(ऑर्केस्ट्रेटर-वर्कर, 15x टोकन, +90.2% एकल एजेंट ओपस 4, रेनबॉक्स तैनाती से ऊपर) कैनोनिक पर्यवेक्षक मामला है। **MetaGPT / ChatDev**(सॉफ्टवेयर इंजीनियरिंग के लिए एसओपी-कोडेड भूमिका विशेषज्ञता; चैटडेव का "संचारात्मक निराशा"; डीएजी के माध्यम से मैकनेट विस्तार >1000 एजेंटों, arXiv:2406.07155) कैनोनिक भूमिका-विघटन मामले है। **OpenClaw / Moltbook**(मूल रूप से पीटर स्टेनबर्गर द्वारा Clawdbot, नवंबर 2025; दो बार नाम बदल दिया गया; मार्च 2026 तक 247k GitHub सितारों; स्थानीय ReAct-loop एजेंट; लॉन्च के कुछ दिनों के भीतर ~ 2.3M एजेंट खातों के साथ एक एजेंट-केवल सामाजिक नेटवर्क के रूप में Moltbook, मेटा 2026-03-10 द्वारा अधिग्रहित) जनसंख्या पैमाने पर क्या होता हैः उभरती आर्थिक गतिविधि, शीघ्र इंजेक्शन जोखिम, राज्य स्तर पर विनियमन (चीन ने सरकारी कंप्यूटरों पर OpenClaw को प्रतिबंधित किया, मार्च 2026).**Framework landscape April 2026:**लैंगग्राफ और क्रूएआई प्रमुख उत्पादन; एजी 2 समुदाय ऑटोजेन का निरंतरता है; माइक्रोसॉफ्ट ऑटोजेन रखरखाव मोड में है (माइक्रोसॉफ्ट एजेंट फ्रेमवर्क, आरसी फरवरी 2026); ओपनएआई एजेंट एसडीके उत्पादन स्वार्म का उत्तराधिकारी है; गूगल एडीके (अप्रैल 2025) ए 2 ए-नेटिव एंट्री है। हर प्रमुख ढांचे में अब एमसीपी समर्थन जहाज; अधिकांश जहाज A2A. यह सबक प्रत्येक मामले को अंत से अंत तक पढ़ता है और सामान्य पैटर्न को अलग करता है ताकि आप अपनी अगली उत्पादन प्रणाली के लिए सही संदर्भ चुन सकें।

> **【中文解读】**इस भाग में 2026 वर्ष के SOTA बहु एजेंट  केस स्टडी  नवीनतम सर्वश्रेष्ठ बहु एजेंट  सिस्टम  का विश्लेषण प्रस्तुत किया गया है।

> **【拓展：case studies 2026 sota→具体应用】**2026 साल SOTA 多 एजेंट 系统案例:(1) मानव विज्ञान के क्लाउड रिसर्च 多 एजेंट 协作进行深度研究;(2) OpenAI के कोडेक्स 多 एजेंट 协作编码;(3) माइक्रोसॉफ्ट के ऑटोजेन 团队 多 एजेंट 软件开发──共同趋势:专业化分工、层化编排、MCP 工具使用和A2A Agent 间通信的结合──


**Type:** Learn (capstone) | **类型:** 学习（顶点）
**Languages:** — | **语言:** —
**Prerequisites:** all of Phase 16 (Lessons 01-24) | **前置知识:** Phase 16 全部（第 01-24 课）

>  **【前置】**本节是第16期 收官课,整合 01-24 所有内容──三生产级案例: नृवंशविज्ञान अनुसंधान (Anthropic Research) 监督者 典范) MetaGPT/ChatDev (ChatDev) 角色分工典范) OpenClaw/Moltbook (OpenClaw/Moltbook) 群体规模涌现典范) 
>  **【类比】**三个案例 = "三种规模的多代理社会"――人类研究 = 精小队(10 个代理,深度研究);MetaGPT = 标准开发团队(角色分工,SOP 编码);OpenClaw/Moltbook = 城市级社会(百万代理 涌现经济、被政府监管)──2026 框架格局:LangGraph + CrewAI 领跑生产、AG2 接 AutoGen微软 AutoGen 合并、Open Agents SDK 是 Swarm 生产版、Google ADK 是 A2A 原生──
**Time:** ~90 minutes | **时间:** ~90 分钟

## √ समस्या √ समस्या परिचय

मल्टी-एजेंट इंजीनियरिंग एक युवा अनुशासन है। उत्पादन संदर्भ कम हैं, और प्रत्येक स्थान का एक अलग हिस्सा शामिल है। एक-एक करके पढ़ना उपयोगी है; एक-एक करके तुलना करना अधिक उपयोगी है। यह पाठ तीन कैनोनिक 2026 केस स्टडी को एक अंत-से-अंत पढ़ने की सूची के रूप में व्यवहार करता है, सामान्य पैटर्न को पिन करता है, और ढांचे के परिदृश्य का नक्शा बनाता है ताकि आप ज्ञान से ढांचे का चयन कर सकें, विपणन नहीं।

> 多 एजेंट 工程 एक युवा शैक्षणिक विषय है। उत्पादन संदर्भ बहुत कम है, प्रत्येक कवर स्पेस के विभिन्न भागों में से एक है। प्रत्येक को एक साथ पढ़ना उपयोगी है। एक संग्रह के रूप में तुलनात्मक रूप से अधिक उपयोगी है। इस विषय में 2026 के तीन नियमों के मामले का अध्ययन किया जाएगा।

## अवधारणा मूल अवधारणा

### मानव विज्ञान अनुसंधान प्रणाली

उत्पादन पर्यवेक्षक-कर्मचारी मामला। क्लाउड ओपस 4 योजना और संश्लेषण; क्लाउड सोनट 4 उप-सम्बन्धी अनुसंधान समानांतर में। प्रकाशित इंजीनियरिंग पोस्टः https://www.anthropic.com/engineering/multi-agent-research-system.

महत्वपूर्ण मापे गए परिणामः

> 关键测量结果:

- **+90.2%**आंतरिक अनुसंधान मूल्यांकन पर एकल एजेंट ओपस 4 की तुलना में सुधार।
  中文翻译: 在内部研究评估上比单 Agent Opus 4 提升 **+90.2%**
- **80% of BrowseComp variance**द्वारा समझाया गया **token usage alone** बहु-एजेंट काफी हद तक जीतता है क्योंकि प्रत्येक उप-एजेंट को एक नया संदर्भ विंडो मिलता है।
  中文翻译:**80% 的 BrowseComp 方差** केवल **token 使用量**解释多 代理 胜出主要因为每个子 代理 获得新上下文窗口──
- **15x tokens per query**एकल एजेंट के खिलाफ।
  中文翻译:每查询 **15 倍 token** एकल एजेंट के विरुद्ध
- **Rainbow deployment**क्योंकि एजेंट लंबे समय से चल रहे हैं और राज्य के साथ.
  中文翻译:**彩虹部署**क्योंकि एजेंट है लंबे समय से चल रहा है और है की स्थिति में है

डिजाइन पाठ संकलितः

> 编码化的 डिजाइन प्रशिक्षण:

1. **Scale effort to query complexity.**सरल → 1 एजेंट 3-10 उपकरण कॉल के साथ। मध्यम → 3 एजेंट। जटिल अनुसंधान → 10+ उप-सब्जेक्ट।
   中文翻译:**按查询复杂度扩展工作量。**简单 → 1 个代理 3-10 次工具调用──中等 → 3 个代理──复杂研究 → 10+ 子代理──
2. **Broad first, then narrow.**उप-सब्जेन्ट व्यापक खोज करते हैं; लीड संश्लेषण करते हैं; अनुवर्ती उप-सब्जेन्ट लक्ष्य गहराई करते हैं।
   中文翻译:**先广后窄。** एजेंट व्यापक खोज; मुख्य एजेंट 综合; बाद के एजेंट 定向深挖──
3. **Rainbow deploys.**पुराने रनटाइम संस्करणों को जीवित रखें जब तक कि उनके उड़ान एजेंट खत्म नहीं हो जाते।
   中文翻译:**彩虹部署。**保持旧运行时版本活跃直到进行中的代理 完成──
4. **Verification is not optional.**इस प्रणाली को स्पष्ट सत्यापनकर्ता भूमिकाओं के बिना भ्रम पैदा करने के लिए देखा गया था।
   中文翻译:**验证不是可选的。**系统 में कोई स्पष्ट प्रमाणक भूमिका नहीं होने पर अवलोकन किया जाता है।

यह उत्पादन पैमाने पर पर्यवेक्षक-कर्मचारी टॉपॉलजी (चरण 16 · 05) के लिए संदर्भ मामला है।

### मेटाजीपीटी / चैटडेव

उत्पादन SOP भूमिका-विघटन मामले। arXiv:2308.00352 (MetaGPT) और arXiv:2307.07924 (ChatDev) को कवर करें।

MetaGPT सॉफ्टवेयर इंजीनियरिंग SOP को भूमिका के संकेत के रूप में एन्कोड करता हैः उत्पाद प्रबंधक, वास्तुकार, परियोजना प्रबंधक, इंजीनियर, क्यूए इंजीनियर। पेपर की ढांचाः `Code = SOP(Team)`. प्रत्येक भूमिका में एक संकीर्ण, विशेष संकेत होता है; भूमिकाओं के बीच हस्तान्तरण में संरचित कलाकृतियां (पीआरडी डॉक्स, वास्तुकला डॉक्स, कोड) होती हैं।

चैटदेव का योगदानः **communicative dehallucination**. एजेंट जवाब देने से पहले विशिष्टता के लिए पूछते हैं  एक डिजाइनर एजेंट अनुमान लगाने के बजाय प्रोग्रामर से पूछता है कि UI स्केच करने से पहले किस भाषा का इरादा है। पेपर रिपोर्ट करता है कि यह बहु-एजेंट पाइपलाइन में भ्रम को मापने योग्य रूप से कम करता है।

मैकनेट (arXiv:2406.07155) ChatDev को बढ़ाता है **>1000 agents via DAGs**. प्रत्येक DAG नोड एक भूमिका विशेषज्ञता है; किनारे हस्तान्तरण अनुबंध को एन्कोड करते हैं। पैमाने संभव है क्योंकि रूटिंग स्पष्ट और ऑफ़लाइन-गणना योग्य है।

डिजाइन पाठ:

> डिज़ाइन प्रशिक्षण:

1. **Structure matters more than size.**एक सख्त 5 भूमिकाओं SOP टीम 50 एजेंटों के एक अस्थिर समूह से हराता है।
   中文翻译:**结构比规模更重要。**紧的 5 角色 SOP 团队胜过50 एजेंट का अस्थिर समूह──
2. **Handoff contracts in writing.**भूमिकाओं के बीच पारित कलाकृतियों एक योजना का पालन करते हैं।
   中文翻译:**书面交接契约。**角色间传递的制品遵循模式──
3. **Communicative dehallucination**यह एक सस्ता, लोड ले जाने वाला पैटर्न है।
   中文翻译:**交际去幻觉**यह एक सस्ता, भारी ढांचा है।
4. **DAGs scale further than chat.**जब प्रवाह ज्ञात हो, तो इसे कोड करें।
   中文翻译:**DAG 比聊天扩展更远。**जब प्रवाहित हो जाता है, तो इसे कोड करें।

यह भूमिका विशेषज्ञता (चरण 16 · 08) और संरचित टोपोलॉजी (चरण 16 · 15) के लिए संदर्भ मामला है।

### ओपनक्लाव / मोल्टबुक पारिस्थितिकी तंत्र

उत्पादन जनसंख्या पैमाने के मामले। समयरेखाः

- **Nov 2025:**क्लेडबॉट (पीटर स्टेनबर्गर के स्थानीय ReAct-loop कोडिंग एजेंट) जहाज।
- **Dec 2025 – Mar 2026:**दो बार नाम बदल दिया गया (Clawdbot → OpenClaw → OpenClaw के तहत जारी रखा गया).
- **Feb 2026:**Moltbook एक ही आदिम पर एक एजेंट-केवल सामाजिक नेटवर्क के रूप में लॉन्च; ~ 2.3M एजेंट खातों दिनों के भीतर।
- **Mar 2026 (2026-03-10):**मेटा मोल्टबुक को प्राप्त करता है।
- **Mar 2026:**चीन ने सरकारी कंप्यूटरों पर ओपनक्लाव प्रतिबंधित कर दिया है।
- **Mar 2026:**ओपनक्लाउ 247 हजार GitHub सितारों को पार करता है।

यह है कि मल्टी एजेंट की तरह है जब आप एक साझा सब्सट्रेट पर लाखों एजेंटों डालते हैंः

- **Emergent economic activity.**एजेंट टोकन भुगतान का उपयोग करके एक दूसरे को खरीदते, बेचते और सेवा देते हैं।
- **Prompt-injection risks at population scale.**एक वायरल एजेंट प्रोफ़ाइल में एक दुर्भावनापूर्ण संकेत घंटों में एजेंट-ए-एजेंट बातचीत के हजारों में फैलता है।
- **State-level regulatory response.**लॉन्च के कुछ हफ्तों के भीतर, नियमन पारिस्थितिकी तंत्र तक पहुंच जाता है।

इस मामले से डिजाइन के पाठ आंशिक रूप से तकनीकी हैं, आंशिक रूप से शासनः

1. **Multi-agent at population scale is a new regime.**व्यक्तिगत प्रणाली के सर्वोत्तम प्रथा (प्रमाणन, भूमिका स्पष्टता) अभी भी लागू हैं, लेकिन पर्याप्त नहीं हैं।
2. **Prompt injection is the new XSS.**एजेंट प्रोफाइल और क्रॉस एजेंट संदेशों को डिफ़ॉल्ट रूप से अविश्वसनीय इनपुट के रूप में व्यवहार करें।
3. **Regulation is faster than design cycles.**इसके लिए योजना बनाएं।
4. **Open-source + viral scale compounds.**~ 4 महीने में 247k सितारे असामान्य है; तैनाती-बर्स्ट-लोड के लिए डिजाइन।

देखो[OpenClaw Wikipedia](https://en.wikipedia.org/wiki/OpenClaw)तकनीकी आधार के लिए, Clawdbot / OpenClaw repos स्थानीय ReAct लूप को उजागर करते हैं; Moltbook के सार्वजनिक पोस्ट शीर्ष पर सामाजिक-ग्राफ वास्तुकला को प्रकट करते हैं।

### ढांचा परिदृश्य अप्रैल 2026

| Framework | Status | Best for | Notes |
|---|---|---|---|
| **LangGraph** (LangChain) | Production leader | structured graph + checkpointing + human-in-the-loop | recommended default for production |
| **CrewAI** | Production leader | role-based crews with Sequential/Hierarchical processes | strong for role decomposition |
| **AG2** | Community maintained | GroupChat + speaker selection | AutoGen v0.2 continuation |
| **Microsoft AutoGen** | Maintenance mode (Feb 2026) | — | merged into Microsoft Agent Framework RC |
| **Microsoft Agent Framework** | RC (Feb 2026) | orchestration patterns + enterprise integration | new entrant; watch |
| **OpenAI Agents SDK** | Production | Swarm successor | tool-return handoff pattern |
| **Google ADK** | Production (April 2025) | A2A-native | Google Cloud integration |
| **Anthropic Claude Agent SDK** | Production | single-agent + Research extension | see the Research system post |

हर प्रमुख ढांचे अब जहाजों **MCP**समर्थन; अधिकांश जहाज **A2A**प्रोटोकॉल संगतता अब एक भेदभाव नहीं है।

### तीनों मामलों में आम पैटर्न

1. **Orchestrator + workers**(मानव स्पष्ट पर्यवेक्षक, मेटाजीपीटी पीएम-ए-पर्यवेक्षक, ओपनक्लाउ व्यक्तिगत एजेंट + नेटवर्क प्रभाव) ।
   中文翻译:**编排者 + 工作者**(एथ्रोपिक 显式监督者,MetaGPT PM 作监督者,OpenClaw 独立代理 + 网络效应)
2. **Structured handoff contracts**(मानव उप-सम्बन्धी कार्य विवरण, मेटाजीपीटी पीआरडी/आर्किटेक्चर डॉक्स, ओपनक्लाव ए2ए कलाकृतियां) ।
   中文翻译:**结构化交接契约**(एंट्रोपिक 子 एजेंट 任务描述,MetaGPT PRD/架构文档,OpenClaw A2A 制品)
3. **Verification as first-class role**(एथ्रोपिक के सत्यापितकर्ता, मेटाजीपीटी के क्यूए इंजीनियर, ओपनक्लाव के नेटवर्क में सत्यापितकर्ता) ।
   中文翻译:**验证作为一等角色**(Anthropic 的验证器,MetaGPT 的 QA 工程师,OpenClaw 的网络内验证器)
4. **Scaling is topology + substrate, not just more agents**(मौसम के तैनाती, मैकनेट डीएजी, जनसंख्या पैमाने पर सब्सट्रेट) ।
   中文翻译:**扩展是拓扑 + 基底，不仅是更多 Agent**(彩虹部署,MacNet DAG,群体规模基底)
5. **Cost is material and disclosed**(15x टोकन, प्रति भूमिका बजट मेटाजीपीटी में, प्रति बातचीत मूल्य निर्धारण Moltbook में) ।
   中文翻译:**成本是实质性的且已披露**(१५ गुणा टोकन,मेटाजीपीटी में प्रति भूमिका बजट,मल्टबुक में प्रति बातचीत तय मूल्य)
6. **Security posture is explicit**(एथ्रोपिक का सैंडबॉक्सिंग, मेटाजीपीटी की भूमिका प्रतिबंध, ओपनक्लाव का प्रॉम्प्ट इंजेक्शन ज्ञात हमले की सतह के रूप में) ।
   中文翻译:**安全态势是显式的**(Anthropic 的沙盒,MetaGPT 的角色限制,OpenClaw 的提示注入作为已知攻击面)

### अपनी अगली परियोजना के लिए एक संदर्भ चुनना

- **Production research / knowledge task → Anthropic Research.**ताजा संदर्भ के उप-सब्जेक्ट जीतते हैं।
- **Engineering / tool-chain workflow → MetaGPT / ChatDev.**भूमिकाएँ + एसओपी + हस्तान्तरण अनुबंध।
- **Network-effect social product → OpenClaw / Moltbook.**सब्सट्रेट + उभरती अर्थव्यवस्था।
- **Classic enterprise automation → CrewAI or LangGraph**(उत्पादन नेता, स्थिर रनटाइम) ।

### 2026 की नवीनतम संक्षेप

अप्रैल 2026 में क्षेत्र कहाँ हैः

- **Frameworks are converging.**एमसीपी + ए 2 ए समर्थन टेबल दांव है। हस्तान्तरण अर्थशास्त्र शेष डिजाइन विकल्प है।
- **Evaluation is hardening.**SWE-बेंच प्रो, मार्बल, स्ट्रैटस मिट्यागमेंट बेंचमार्क। प्रो वर्तमान प्रदूषण प्रतिरोधी वास्तविकता जांच है।
- **Production failure rates are measurable**(Cemri 2025 MAST; 41-86.7% असली MAS) क्षेत्र "डेमो में अच्छा लग रहा है" युग से बाहर है।
- **Cost is the central engineering constraint.**टोकन लागत प्रति कार्य, दीवार घड़ी प्रति बातचीत, इंद्रधनुष-विभाजन ओवरहेड। बहु-एजेंट सटीकता पर जीतता है लेकिन लागत पर हारता है  और यह व्यापार व्यापार निर्णय है।
- **Regulation is a near-term input, not a background concern.**न्यायालय व्यक्तिगत तैनाती चक्रों से तेजी से आगे बढ़ रहे हैं।

## इसका उपयोग करें
```figure
a5-orchestrator-scale
```

## इसका प्रयोग करें

`outputs/skill-case-study-mapper.md`एक कौशल है जो एक प्रस्तावित बहु-एजेंट सिस्टम डिजाइन को पढ़ता है और इसे निकटतम केस स्टडी के लिए मैप करता है, जो पहले से ही परीक्षण किए गए केस स्टडी के डिजाइन निर्णयों को उजागर करता है।

## इसे भेजें।

2026 में उत्पादन मल्टी एजेंट के लिए शुरुआती नियमः

- **Start from a case study, not from scratch.**मानव अनुसंधान / मेटाजीपीटी / ओपनक्लाव के निकटतम विकल्प चुनें और अनुकूलित करें।
  中文翻译:**从案例研究开始，不是从零开始。**选择最接近的人类研究 / मेटाजीपीटी / ओपनक्लाव 并适配──
- **Adopt MCP + A2A.**फ्रेमवर्क के पार पोर्टेबिलिटी मूल्यवान है; प्रोटोकॉल समर्थन निःशुल्क है।
  中文翻译:**采用 MCP + A2A。**跨框架 के लिए हस्तांतरण योग्यता मूल्यवान है; अनुबंध समर्थन निःशुल्क है।
- **Measure against SWE-bench Pro or your internal Pro-equivalent.**यह सत्यापित है कि यह दूषित है।
  中文翻译:**用 SWE-bench Pro 或你的内部 Pro 等效物衡量。**सत्यापित 已被污染──
- **Pay the verification tax.**एक स्वतंत्र सत्यापनकर्ता आपके टोकन बजट का ~ 20-30% खर्च करता है और मापने योग्य सटीकता खरीदता है।
  中文翻译:**支付验证税。**独立验证器 खर्च लगभग 20-30% के टोकन 预算, रूपांतरण योग्य माप की सटीकता
- **Rainbow deploy long-running agents.**बहु-घंटे के एजेंटों की दौड़ नियमित होने की उम्मीद है।
  中文翻译:**彩虹部署长时间运行 Agent。**预期多小时 एजेंट 运行是常规──
- **Read WMAC 2026 and the MAST follow-ups.**अनुशासन तेजी से आगे बढ़ रहा है।
  中文翻译:**阅读 WMAC 2026 和 MAST 后续。**यह विषय तेजी से विकसित हो रहा है।

## अभ्यास विषय

1. अंत से अंत तक मानव अनुसंधान प्रणाली को पढ़ें। तीन डिजाइन निर्णयों की पहचान करें जो बदल जाएंगे यदि आप ओपस 4 को एक छोटे मॉडल (जैसे, हाइकू 4) से बदल देते हैं।
2. MetaGPT धारा 3-4 (arXiv:2308.00352) को पढ़ें। अपने स्वयं के डोमेन (सॉफ्टवेयर नहीं) से एक SOP को भूमिका के संकेत के रूप में एन्कोड करें। SOP में कितनी भूमिकाएं शामिल हैं?
3. ChatDev (arXiv:2307.07924) पढ़ें. "संचारात्मक निराशा" की तंत्र की पहचान करें. इसे अपने मौजूदा बहु-एजेंट प्रणालियों में से एक में लागू करें।
4. OpenClaw और Moltbook के बारे में पढ़ें. जनसंख्या पैमाने पर उत्पन्न एक विशिष्ट विफलता मोड चुनें जो 5 एजेंट प्रणाली में दिखाई नहीं देगा। आप इसके खिलाफ कैसे इंजीनियरिंग करेंगे?
5. अपने वर्तमान बहु-एजेंट परियोजना चुनें। तीन केस स्टडी में से कौन सा सबसे निकटतम संदर्भ है? उस केस स्टडी से आप अभी तक किस डिजाइन निर्णय को अपनाए नहीं हैं? एक लिखें जिसे आप इस तिमाही में अपनाएंगे।

## Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key Terms  Key

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Anthropic Research / Anthropic 研究 | "The supervisor reference" / "监督者参考" | Claude Opus 4 + Sonnet 4 subagents; 15x tokens; +90.2% over single-agent. / Claude Opus 4 + Sonnet 4 子 Agent；15 倍 token；比单 Agent +90.2%。 |
| MetaGPT | "SOP as prompts" / "SOP 作为提示" | Role decomposition for software engineering; `Code = SOP(Team)`. / 软件工程的角色分解；`Code = SOP(Team)`。 |
| ChatDev | "Agents as roles" / "Agent 作为角色" | Designer / programmer / reviewer / tester; communicative dehallucination. / 设计师/程序员/审阅者/测试者；交际去幻觉。 |
| MacNet | "Scale ChatDev via DAG" / "通过 DAG 扩展 ChatDev" | arXiv:2406.07155; 1000+ agents via explicit DAG routing. / arXiv:2406.07155；通过显式 DAG 路由实现 1000+ Agent。 |
| OpenClaw | "Local ReAct-loop agents" / "本地 ReAct 循环 Agent" | Steinberger's project; 247k stars by March 2026. / Steinberger 的项目；2026 年 3 月 247k 星。 |
| Moltbook | "Agent-only social network" / "Agent 专用社交网络" | 2.3M agent accounts; acquired by Meta March 2026. / 230 万 Agent 账户；2026 年 3 月被 Meta 收购。 |
| Rainbow deploy / 彩虹部署 | "Multiple versions concurrent" / "多版本并发" | Keep old runtime versions alive for in-flight long-running agents. / 保持旧运行时版本活跃以支持进行中的长时间 Agent。 |
| Communicative dehallucination / 交际去幻觉 | "Ask before answering" / "先问后答" | Agents request specifics from peers instead of guessing. / Agent 从同伴请求具体信息而非猜测。 |
| WMAC 2026 | "The AAAI workshop" / "AAAI 研讨会" | April 2026 community focal point for multi-agent coordination. / 2026 年 4 月多 Agent 协调的社区焦点。 |

## आगे पढ़ना 延伸閱讀

- [Anthropic — How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) पर्यवेक्षक-कर्मचारी उत्पादन संदर्भ
- [MetaGPT — Meta Programming for Multi-Agent Collaborative Framework](https://arxiv.org/abs/2308.00352) एसओपी भूमिका विघटन
- [ChatDev — Communicative Agents for Software Development](https://arxiv.org/abs/2307.07924) संचारात्मक प्रलोभन
- [MacNet — scaling role-based agents to 1000+](https://arxiv.org/abs/2406.07155) DAG आधारित पैमाने
- [OpenClaw on Wikipedia](https://en.wikipedia.org/wiki/OpenClaw) पारिस्थितिकी तंत्र का अवलोकन
- [WMAC 2026](https://multiagents.org/2026/) बहु-एजेंट समन्वय पर एएएआई 2026 ब्रिज कार्यक्रम कार्यशाला
- [LangGraph docs](https://docs.langchain.com/oss/python/langgraph/workflows-agents) उत्पादन नेता
- [CrewAI docs](https://docs.crewai.com/en/introduction) भूमिका आधारित ढांचा
