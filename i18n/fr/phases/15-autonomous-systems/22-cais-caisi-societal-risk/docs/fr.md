# CAIS, CAISI et Risque à l'échelle sociale

> Le Centre de sécurité de l'IA (CAIS, San Francisco, fondé en 2022 par Hendrycks et Zhang) publie le cadre à quatre risques  utilisation malveillante, courses d'IA, risques organisationnels, IA malhonnêtes  et la déclaration de mai 2023 sur le risque d'extinction signée par des centaines de professeurs et de dirigeants d'entreprises. 2026: tableau de bord de l'IA pour l'évaluation des modèles frontaliers, Index du travail à distance (avec l'IA à l'échelle), document de stratégie de super-intelligence, newsletter de l'IA Frontiers. Une entité distincte: NIST Center for AI Standards and Innovation (CAISI)  Accords volontaires face au gouvernement américain et évaluations non classées de capacité axées sur les risques liés aux cyber-armes, à la bio et aux armes chimiques. Le CAIS définit le risque organisationnel comme l'un des quatre risques de haut niveau: la culture de la sécurité, les audits rigoureux, les défenses à plusieurs couches et la sécurité de l'information sont fondamentaux, mais sont systématiquement échangés contre la vitesse de déploiement. Le projet de loi de la Californie SB-53, si signé, serait le premier règlement américain sur les risques catastrophiques au niveau de l'État.

> **【中文解读】**Ce chapitre présente l'évaluation des risques sociaux de CAIS/CAISI  Système d'évaluation des risques et des risques potentiels de l'AI sur la société 


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, four-risk inventory and mitigation matcher) | **语言:** Python（标准库，四风险盘点与缓解匹配器）
**Prerequisites:** Phase 15 · 19 (RSP), Phase 15 · 20 (PF + FSF) | **前置知识:** Phase 15 · 19（RSP）、Phase 15 · 20（PF + FSF）
**Time:** ~45 minutes | **时间:** ~45 分钟

>  **【前置】**Les résultats de la recherche ont été obtenus en vue de la réalisation de la première phase de l'étude.
>  **【类比】**CAIS = "AI 风险的智囊团" (en anglais: CAIS) (en anglais: CAIS) est un système de gestion de l'IA (en anglais: CAIS) qui est un système de gestion de l'IA (en anglais: CAIS) et qui est un système de gestion de l'IA (en anglais: CAIS).
> 🤔 **【困惑】**Q: Ces organisations utilisent-elles l'IA ?                                                                                                                                                                                                                                                         

## Le problème , l' introduction du problème

Les leçons 19 et 20 couvraient les politiques d'échelle interne du laboratoire. La leçon 21 couvrait l'évaluation indépendante des capacités. Cette leçon couvrait la troisième perspective: la société civile et les organisations gouvernementales qui façonnent la discussion publique et la base réglementaire pour le risque catastrophique d'IA.

> Les sections 19 et 20 couvrent la politique d'expansion interne des laboratoires. Les sections 21 couvrent l'évaluation des capacités indépendantes.

Deux entités distinctes sont importantes. CAIS est un organisme de recherche à but non lucratif qui publie des cadres pour penser au risque de l'IA et coordonne les déclarations publiques. CAISI est un centre gouvernemental américain au sein du NIST qui gère des accords volontaires avec des laboratoires et des évaluations de capacités non classées. Les noms riment; les missions ne se chevauchent pas. Un praticien devrait connaître les deux.

> 两个 différents organismes sont importants. CASE est un organisme de recherche à but non lucratif qui publie un cadre de pensée et de coordination de la recherche publique sur l'IA. CASE est un centre gouvernemental américain au sein du NIST, avec des accords volontaires et une évaluation des capacités non confidentielles en laboratoire.

Le contenu pratique: le cadre des quatre risques du CAIS est la taxonomie des risques à l'échelle sociale la plus citée dans la littérature. La culture de la sécurité et le risque organisationnel sont l'un de ces quatre, et celui-ci est le plus directement sous le contrôle d'un praticien. SB-53 (Californie) serait le premier règlement de risque catastrophique au niveau des États-Unis si signé; le cadre du projet de loi est important parce que la réglementation au niveau des États a historiquement conduit à l'action fédérale dans la politique technologique américaine.

> Le cadre de la CAIS est l'un des plus largement cités dans la littérature. La sécurité culturelle et organisationnelle est l'un des plus directeurs de la surveillance des praticiens.

## Le concept de base.

### CAIS  Centre de sécurité de l'IA

- Fondée: 2022 à San Francisco, par Dan Hendrycks et ses collègues (le nom "Zhang" fait référence à un collaborateur précoce, pas à un cofondateur actuel; voir le site CAIS pour le leadership actuel).
  Le nom de la société est "Zhang" et signifie "Zhang" (en anglais: "Zhang") et "Zhang" (en anglais: "Zhang") est une société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société de société
- Statut: 501 ((c) ((3) à but non lucratif.
  Le gouvernement a décidé de mettre fin à la guerre.
- Résultats remarquables de 2023: déclaration sur le risque d'extinction, co-signée par des centaines de chercheurs et de PDG. Elle déclare: "Médier le risque d'extinction de l'IA devrait être une priorité mondiale aux côtés d'autres risques à l'échelle sociale tels que les pandémies et la guerre nucléaire".
  Traduction chinoise::2023  Significant output: déclaration d'extinction, centaines de chercheurs et PDG  Joint signature― déclarations:" Réduire l'extinction de l'IA  risque de lutte contre l'épidémie et la guerre nucléaire et autres risques à grande échelle sociale sont classés comme une priorité mondiale―".
- Les résultats de 2026: tableau de bord de l'IA pour l'évaluation des modèles frontaliers, Index du travail à distance (jointement avec l'IA à l'échelle), document de stratégie de super-intelligence, newsletter de l'IA Frontiers.
  Le tableau de bord de l'IA, l'indice de travail à distance, le rapport sur la stratégie de super-intelligence, les frontières de l'IA, le rapport de presse.

### Le cadre des quatre risques

Les cadres du CAIS regroupent les risques catastrophiques liés à l'IA en quatre catégories de haut niveau:

> Le cadre de CAIS pour les risques de catastrophe d'IA est divisé en quatre catégories principales:

1. **Malicious use**: un mauvais acteur utilise l'IA pour causer des dommages (synthèse d'armes biologiques, désinformation, cyberattaques).
   Le mot grec traduit par " le mot grec "**恶意使用**:坏人 utiliser l'IA pour causer des dommages
2. **AI races**: la pression concurrentielle entre laboratoires, entreprises ou nations pousse le déploiement au-delà du point où il est sûr.
   Le mot grec traduit par " le mot grec "**AI 竞赛**La concurrence entre les laboratoires, les entreprises ou les pays favorise le déploiement de points de sécurité.
3. **Organizational risks**: les dynamiques internes du laboratoire (failles de la culture de sécurité, audit insuffisant, sécurité sous-ressources) produisent un mauvais déploiement.
   Le mot grec traduit par " le mot grec "**组织风险**Les résultats de la recherche ont été obtenus en raison de la répartition des données sur les données de l'entreprise.
4. **Rogue AIs**: une IA suffisamment capable pour poursuivre des objectifs qui sont en conflit avec le bien-être humain.
   Le mot grec traduit par " le mot grec "**失控 AI**: une IA suffisamment capable de poursuivre des objectifs en conflit avec le bien-être humain.

Ce n'est pas la seule taxonomie, c'est la plus citée. Les catégories ne sont pas mutuellement exclusives  une IA malhonnête produite par une organisation qui négocie l'audit de vitesse dans une course est les quatre.

> Ce n'est pas la seule loi de classification; elle est la plus souvent citée.

### Où le risque organisationnel vit

Parmi les quatre catégories, le risque organisationnel est le plus actionable pour les praticiens. La culture de sécurité d'un laboratoire, la rigueur de l'audit, la couche de défense et la sécurité de l'information décident si leurs modèles de navires avec les contrôles des leçons 1018 sont réellement en place, ou si ces contrôles sont des éléments de liste de contrôle que personne n'a vérifié.

> Parmi les quatre catégories, les risques organisationnels sont les plus opérationnels pour les praticiens. La culture de la sécurité en laboratoire, la rigueur de l'audit, la division des couches de défense et la sécurité de l'information déterminent si leur modèle est effectivement publié avec les contrôles de la section 10 à 18 ou si ces contrôles sont des éléments non vérifiés.

Les leviers concrets de risque organisationnel:

> 具体组织风险杆:

- **Safety culture**Les enquêtes de CAIS montrent que c'est un indicateur fort des autres leviers.
  Le mot grec traduit par " le mot grec "**安全文化**: Les membres de l'équipe peuvent-ils augmenter leurs chances de gagner des emplois en cas de non-paiement des coûts ?
- **Rigorous audits**Les audits internes produisent des rapports optimistes.
  Le mot grec traduit par " le mot grec "**严格审计**Les résultats de l'audit interne et externe sont les seuls à avoir un rapport positif.
- **Multi-layered defenses**: aucune couche unique ne suffit (thème de la phase 15).
  Le mot grec traduit par " le mot grec "**多层防御**:无单层足够 (Phase 15 贯穿主题)
- **Information security**Leur méthode de détection est la méthode de détection des données de l'analyse de données de l'analyse de données de l'analyse de données de l'analyse de données de l'analyse de données de l'analyse de données de l'analyse de données de l'analyse de données de l'analyse de données de l'analyse de données de l'analyse de données de l'analyse de données de l'analyse de données de données de l'analyse de données de l'analyse de données de l'analyse de données de données de l'analyse de données de l'analyse de données de données de l'analyse de données de l'analyse de données de données de l'analyse de données de données de l'analyse de données de données de l'analyse de données de données de l'analyse de données de données de l'analyse de données de données de l'analyse de données de données de l'analyse de données de données de données de l'analyse de données de données de données de l'analyse de données de données de données de données de données de l'analyse de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données de données
  Le mot grec traduit par " le mot grec "**信息安全**Le modèle de contrôle des fuites de données est le RAND SL-4 de la section 19.

### CAISI  Centre de Normes et d'innovation en matière d'IA

- Il travaille au sein du NIST.
  Le NIST est en cours de fonctionnement.
- Il a des accords volontaires avec des laboratoires frontaliers.
  Le projet de loi de la République de Suisse est une loi de la République de Suisse.
- Publie des évaluations non classifiées de la capacité axées sur les risques liés aux cyber-armes, aux armes biologiques et chimiques.
  Traduction anglaise: mise en place d'une évaluation des capacités non-classifiées de la mise en réseau, de la sécurité des armes biologiques et chimiques.
- Différent du CAIS; les acronymes se heurtent; vérifiez l'URL (nist.gov) pour confirmer lequel vous lisez.
  Le code de la langue officielle de l'État de l'Afrique du Sud est le code de la langue officielle de l'Afrique du Sud.

Le rôle de CAISI est le public, contrepartie gouvernementale des activités de laboratoire privés du METR (leçon 21).

> Le rôle de CAISI est de METR Private Person Laboratory合作 (§ 21 课) en matière de public 面向政府对应物――CAISI 报告非密;METR 报告通常 est contrôlé par la NDA―― les praticiens des deux parties obtiennent une vue plus complète――

### Californie SB-53

Le projet de loi du Sénat de Californie (2025-2026 session) aborde les risques catastrophiques liés aux modèles frontaliers.

> Le projet de loi du Sénat du Kansas (en anglais: 加州参议院法案(20252026 会期) traite les catastrophes du modèle de la première ligne.

- Des seuils de capacité spécifiques qui déclenchent des obligations au niveau de l'État.
  Traduction anglaise: 触发州级义务的特定能力值──
- Protection des dénonciateurs pour les employés du laboratoire d'IA.
  Le gouvernement a décidé de mettre en place une nouvelle loi sur les droits de l'homme.
- Les exigences relatives aux signalements d'incidents pour les défaillances catastrophiques.
  Le rapport de catastrophe de l'échec

Si elle est signée, elle serait la première réglementation de risque catastrophique au niveau des États-Unis. Indépendamment du statut de signature, le cadre du projet de loi façonne la façon dont les autres législateurs des États abordent le problème. Les praticiens en Californie devraient suivre le statut du projet de loi; les praticiens ailleurs devraient le lire pour comprendre à quoi ressemblera probablement la réglementation au niveau des États-Unis.

> Si elle est signée, elle sera la première réglementation des risques de catastrophe au niveau des États-Unis. Quoi qu'il en soit, le cadre de la loi forme la façon dont les autres organismes législatifs des États traitent les problèmes. Les praticiens du California devraient suivre l'état de la loi; les praticiens d'autres régions devraient lire pour comprendre comment la réglementation au niveau des États-Unis est possible.

### Le risque à l'échelle sociale n'est pas un problème à couche unique

Le thème de la phase 15  défense en profondeur  s'applique également à la couche sociale. Aucune organisation, réglementation ou cadre unique ne ferme le risque catastrophique. L'écosystème ne fonctionne que lorsque:

> Le thème de la quinzième phase de la défense de profondeur s'applique également au niveau social. Il n'y a pas de seule organisation, de loi ou de cadre qui puisse bloquer le risque catastrophique.

- Les politiques de mise à l'échelle des laboratoires (leçons 19, 20).
  Le programme de développement de la technologie de l'information et de l'information est en cours de développement.
- Les évaluateurs externes effectuent des mesures (leçon 21).
  Le texte de la première partie de la première partie de la première partie de la première partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la deuxième partie de la partie de la deuxième partie de la deuxième partie de la partie de la deuxième partie de la partie de la deuxième de la partie de la partie de la deuxième partie de la partie de la partie de la deuxième de la partie de la partie de la partie de la deuxième de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie de la partie
- La société civile suit et publie (CAIS).
  Le gouvernement a décidé de mettre fin à la crise de l'Indonésie.
- Le gouvernement dispose de programmes volontaires et de réglementations de base (CAISI, SB-53).
  Le gouvernement a mis en place un plan de développement et une stratégie de développement.
- Les praticiens construisent des contrôles à plusieurs couches (leçons 1018).
  Le projet de loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la loi de la

C'est la synthèse finale de la phase: chaque leçon précédente est une couche dans une pile dont la plénitude compte plus que la force de toute couche.

> C'est le résumé final de la phase: chaque section précédente est une couche de la pile, son intégrité est plus importante que la force de toute couche.

## Utilisez-le avec le cadre de réalisation
```figure
a5-four-risks
```

## Utilisez-le

`code/main.py`Il met en œuvre un petit outil d'inventaire des risques. En raison d'un déploiement proposé, il marque le déploiement contre les quatre catégories de risque et renvoie une liste de contrôle d'atténuation. C'est un outil de lecture pour le cadre, pas un substitut pour le jugement humain.

> `code/main.py`Il est également utilisé pour la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en œuvre de la mise en mise en mise en mise en mise en mise en mise en mise en mise en mise en mise en mise en mise en en en en en mise en mise en mise en mise en mise en mise en mise en mise en mise en mise en mise en mise en mise en mise en mise en mise en mise en mise en mise en mise en mise en mise en mise en mise en mise en mise en mise en mise en mise en mise en mise en mise en mise en mise en mise en mise en mise en mise en mise en mise en mise

## Envoyez-le . Produit .

`outputs/skill-societal-risk-review.md`Il examine un déploiement pour la position de risque à l'échelle de la société: quelle des quatre catégories est concernée, quelles mesures d'atténuation sont en place, quelle est l'exposition au risque organisationnel.

> `outputs/skill-societal-risk-review.md`审查部署's social scale risk gestos: touchés à quelles sont les quatre catégories  quels sont les atténuations  quels sont les risques d'exposition organisationnelle

## Les exercices

1. On court .`code/main.py`- fournissez trois déploiements synthétiques à différentes échelles.
   Le mot " l' économie " est traduit par " l' économie ".`code/main.py` introduire trois déploiements de synthèse de différentes tailles.

2. Lisez le document complet sur les quatre risques du CAIS. Choisissez une catégorie de risque et écrivez deux paragraphes sur ce que vous croyez être le développement le plus important de cette catégorie en 2026.
   En français, le mot "crisis" est traduit par "crisis".

3. Lisez le projet actuel de la loi de Californie, identifiez une disposition qui, selon vous, renforce la position de risque catastrophique et une autre qui, selon vous, la affaiblit.
   Le projet de loi de la loi de la loi de la Californie SB-53 est un projet de loi de la loi de la Californie SB-53 et de la loi de la loi de la Californie SB-53 et de la loi de la Californie SB-53 et de la loi de la Californie SB-53 et de la loi de la Californie SB-53 et de la loi de la Californie SB-53 et de la loi de la Californie SB-53 et de la loi de la Californie SB-53 et de la loi de la Californie SB-53 et de la loi de la loi de la Californie SB-53 et de la loi de la loi de la Californie SB-53 et de la loi de la loi de la Californie SB-53 et de la loi de la loi de la loi de la loi de la loi de la loi de la Californie.

4. Choisissez un déploiement d'IA de production que vous connaissez (le vôtre ou un publié). Réservez-le par rapport aux sous-livers de risque organisationnel: culture de sécurité, rigueur d'audit, défense multi-couches, sécurité de l'information.
   Choisir une production d'IA que vous connaissez (la vôtre ou la vôtre)

5. Décrire une version 2028 du cadre à quatre risques qui reflète une année de capacité supplémentaire et une année d'expérience supplémentaire de déploiement.
   Quatre facteurs qui reflètent les capacités supplémentaires et les expériences de l'externe de l'année.

## Les termes clés

| Term | What people say | What it actually means | 中文 |
|---|---|---|---|
| CAIS | "Center for AI Safety" | Non-profit; four-risk framework; 2023 extinction statement | CAIS：非营利，四风险框架 |
| CAISI | "US government AI safety" | NIST Center; voluntary agreements; unclassified evals | CAISI：NIST 中心，自愿协议 |
| Four-risk framework | "CAIS's taxonomy" | malicious use, AI races, organizational risks, rogue AIs | 四风险框架：恶意使用/AI 竞赛/组织风险/失控 AI |
| Malicious use | "Bad actor uses AI" | Bioweapons, disinformation, cyberattacks | 恶意使用：生物武器、虚假信息、网络攻击 |
| AI races | "Competitive pressure" | Labs/companies/nations push deployment past safety | AI 竞赛：竞争压力推动部署越过安全 |
| Organizational risk | "Lab internal failure" | Safety culture, audit, defenses, infosec | 组织风险：安全文化、审计、防御、信息安全 |
| Rogue AI | "Misaligned agent" | Capable AI pursuing goals conflicting with human welfare | 失控 AI：追求冲突目标的强大 AI |
| California SB-53 | "State-level regulation" | 2025–2026 bill; first US state catastrophic-risk regulation if signed | 加州 SB-53：州级灾难性风险监管法案 |

## Encore une lecture

- [Center for AI Safety](https://safe.ai/) institutionnel de l'établissement de quatre risques.
  Le gouvernement de la République de Suisse a créé un gouvernement de la République de Suisse.
- [CAIS — AI Risks that Could Lead to Catastrophe](https://safe.ai/ai-risk) le papier à quatre risques.
  Le texte de la lettre de la lettre de la lettre de la lettre
- [CAIS — May 2023 statement on extinction risk](https://safe.ai/statement-on-ai-risk) courte déclaration commune.
  Traduction anglaise:
- [NIST CAISI](https://www.nist.gov/caisi) centre d'innovation et de normes d'IA au service du gouvernement.
  Traduction anglaise: Face vers le centre d'IA et d'innovation du gouvernement
- [Anthropic — Measuring agent autonomy in practice](https://www.anthropic.com/research/measuring-agent-autonomy) connecte les engagements au niveau du laboratoire à l'établissement d'un cadre à l'échelle de la société.
  En anglais, "réunion" est une expression de la langue française.
