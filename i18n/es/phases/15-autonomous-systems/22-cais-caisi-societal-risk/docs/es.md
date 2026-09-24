# CAIS, CAISI y riesgo a escala social

> El Centro para la Seguridad de la IA (CAIS, San Francisco, fundado en 2022 por Hendrycks y Zhang) publica el marco de cuatro riesgos  uso malicioso, carreras de IA, riesgos organizacionales, IA deshonestas  y la declaración de mayo de 2023 sobre el riesgo de extinción firmada por cientos de profesores y líderes de empresas. 2026 lanzamientos de CAIS: AI Dashboard para la evaluación de modelos fronterizos, Índice de Trabajo Remoto (con IA de escala), Superinteligencia Estrategia de Papel, AI Frontiers boletín de noticias. Una entidad distinta: NIST Center for AI Standards and Innovation (CAISI)  Acuerdos voluntarios dirigidos al gobierno de Estados Unidos y evaluaciones de capacidad no clasificadas enfocadas en riesgos de ciber, bio y armas químicas. El CAIS señala el riesgo organizacional como uno de los cuatro riesgos de alto nivel: la cultura de seguridad, las auditorías rigurosas, las defensas de múltiples capas y la seguridad de la información son fundamentales pero se intercambian rutinariamente contra la velocidad de despliegue. El SB-53 de California, si se firma, sería la primera regulación de riesgo catastrófico a nivel estatal de los Estados Unidos.

> **【中文解读】**Este apartado presenta la evaluación de riesgos sociales de CAIS/CAISI AI 系统对社会潜在影响和风险分析


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, four-risk inventory and mitigation matcher) | **语言:** Python（标准库，四风险盘点与缓解匹配器）
**Prerequisites:** Phase 15 · 19 (RSP), Phase 15 · 20 (PF + FSF) | **前置知识:** Phase 15 · 19（RSP）、Phase 15 · 20（PF + FSF）
**Time:** ~45 minutes | **时间:** ~45 分钟

> ¿ Qué es esto ?**【前置】**El estudio de la tecnología de la inteligencia artificial (AI) se desarrolló en el período de investigación de la Universidad de Nueva York (U.S.) en el año 2000.
> ¿ Qué es esto ?**【类比】**CAIS = "AI 风险的智囊团" (Miércoles de investigación, declaraciones, propuestas); CAISI = "AI 风险的政府办公室" (NIST, coordinación voluntaria) (NIST, coordinación voluntaria) (B) (NIST, coordinación voluntaria) (B) (NIST, coordinación voluntaria) (B) (B) (NIST, coordinación voluntaria) (B) (B) (NIST, coordinación voluntaria) (B) (B) (NIST, coordinación voluntaria) (B) (NIST, coordinación voluntaria) (B) (NIST, coordinación voluntaria) (B) (B) (NIST, coordinación voluntaria) (B) (B) (B) (NIST, coordinación voluntaria).
> ¿ Qué es esto ?**【困惑】**P: ¿Qué usan estas organizaciones para hacer ingeniería de IA?   uso directo es conforme a la normativa: si sus productos involucran escenarios de alto riesgo (medicina, finanzas, contratación), necesitan consultar el marco CAIS para hacer una evaluación de riesgos, puede necesitar cumplir con la Ley de IA de la UE, la ley SB-53 de California, etc.

## El problema es la introducción del problema

Las lecciones 19 y 20 abarcaron políticas de escalación interna del laboratorio. La lección 21 abarcó la evaluación de capacidad independiente. Esta lección cubre la tercera perspectiva: la sociedad civil y las organizaciones gubernamentales que dan forma a la discusión pública y la base regulatoria para el riesgo de IA catastrófica.

> Se trata de un programa de investigación y desarrollo de la tecnología de la información y de la información, que se desarrolla en el ámbito de la investigación y la investigación.

CAIS es una organización de investigación sin fines de lucro que publica marcos para pensar sobre el riesgo de IA y coordina declaraciones públicas. CAISI es un centro del gobierno de Estados Unidos dentro del NIST que ejecuta acuerdos voluntarios con laboratorios y evaluaciones de capacidad no clasificadas. Los nombres rimen; las misiones no se superponen. Un practicante debe saber ambos.

> 两个 entidades diferentes son importantes. CAIS es la organización de investigación sin fines de lucro que publica un marco de pensamiento y coordinación de declaraciones públicas sobre IA. CAISI es el centro del gobierno de los Estados Unidos dentro del NIST, con el acuerdo voluntario de operación de laboratorios y evaluación de la capacidad de no secreto.

El contenido práctico: el marco de cuatro riesgos del CAIS es la taxonomía de riesgo a escala social más citada en la literatura. La cultura de seguridad y el riesgo organizacional son uno de esos cuatro, y éste es el más directamente bajo el control de un profesional. SB-53 (California) sería la primera regulación de riesgo catastrófico a nivel estatal de los Estados Unidos si se firma; el marco del proyecto de ley es importante porque la regulación a nivel estatal ha liderado históricamente la acción federal en la política tecnológica de los Estados Unidos.

>  Contenido práctico:El Cuatro Arándares de riesgo de CAIS es uno de los más ampliamente citados en la literatura. El riesgo de seguridad cultural y organizativo es uno de los más directos bajo el control de los profesionales.

## El concepto central.

### CAIS  Centro de Seguridad de la IA

- Fundado: 2022 en San Francisco, por Dan Hendrycks y colegas (el nombre "Zhang" se refiere a un colaborador temprano, no a un cofundador actual; vea el sitio web de CAIS para el liderazgo actual).
  China:成立:2022年在旧金山, por Dan Hendrycks 和同事创立("Zhang" significa colaborador temprano, no actual联合创始人; actual领导见 CAIS 网站) ]]
- Estatus: 501 ((c) ((3) sin ánimo de lucro.
  En el caso de los niños, el estado de la familia de los niños es el de la familia de los niños.
- Resultados notables de 2023: declaración sobre el riesgo de extinción, co-firmada por cientos de investigadores y CEOs.
  China 显著产出:灭绝风险声明, cientos de investigadores y CEO 联合签署――声明:"Minimalizar el riesgo de extinción de IA se asocia con otras amenazas a escala social como la epidemia y la guerra nuclear como prioridad mundial".""
- Resultados de 2026: Tabla de control de IA para la evaluación de modelos fronterizos, Índice de trabajo remoto (junto con AI de escala), documento de estrategia de superinteligencia, boletín informativo de AI Frontiers.
  En el libro de trabajo, el artículo se publica en el periódico de la revista "La inteligencia artificial".

### El marco de los cuatro riesgos

Los marcos de CAIS agrupan el riesgo de IA catastrófica en cuatro categorías de alto nivel:

> El marco de CAIS se divide en cuatro categorías principales:

1. **Malicious use**: un mal actor utiliza la IA para causar daño (sintesis de armas biológicas, desinformación, ciberataques).
   En inglés:**恶意使用**:坏人 usar IA  causar daño 生物武器合成、虚假信息、网络攻击)
2. **AI races**: la presión competitiva entre laboratorios, empresas o naciones empuja el despliegue más allá del punto en que es seguro.
   En inglés:**AI 竞赛**Las empresas o los países tienen un mayor riesgo de desarrollar un sistema de seguridad.
3. **Organizational risks**En el caso de los laboratorios, la utilización de los recursos de seguridad es insuficiente.
   En inglés:**组织风险**El proyecto de investigación de la Comisión de Investigación y Tecnología (CIP) se ha desarrollado en el marco de la investigación de la investigación y de la investigación de la tecnología de la información.
4. **Rogue AIs**: una IA suficientemente capaz persigue objetivos que entran en conflicto con el bienestar humano.
   En inglés:**失控 AI**: la capacidad suficiente de la IA para alcanzar los objetivos de conflicto con el bienestar humano.

Esta no es la única taxonomía; es la más citada. Las categorías no se excluyen mutuamente  una IA deshonesta producida por una organización que negoció auditoría de velocidad en una carrera es las cuatro.

> Esta no es la única ley de clasificación; es la más frecuentemente citada. La IA sin control producida por una organización que utiliza la velocidad de auditoría en la competencia es la de las cuatro clases.

### Donde el riesgo organizacional vive

De las cuatro categorías, el riesgo organizacional es el más accionable para los profesionales. La cultura de seguridad de un laboratorio, el rigor de auditoría, la capa de defensa y la seguridad de la información deciden si sus modelos de buques con los controles de las lecciones 1018 están realmente en su lugar, o si esos controles son elementos de la lista de verificación que nadie verificó.

> Entre las cuatro categorías, el riesgo organizacional es el más operable para los profesionales. La cultura de seguridad de los laboratorios, la rigor de auditoría, la división de la defensa y la seguridad de la información determinan si sus modelos se ejecutan con los controles de la clase 10 a 18 en el lugar real, o si estos controles son listados sin verificación humana.

Las palancas de riesgo organizacional concretas:

> 具体组织风险杆:

- **Safety culture**Las encuestas de CAIS muestran que esto es un fuerte predictor de las otras palancas.
  En inglés:**安全文化**¿Pueden los miembros del equipo aumentar sus preocupaciones en caso de no pagar el costo de su trabajo?
- **Rigorous audits**Las auditorías internas producen informes optimistas.
  En inglés:**严格审计**Exterior y interno: sólo la auditoría interna produce un informe de opinión.
- **Multi-layered defenses**: no es suficiente una sola capa (el tema de la fase 15).
  En inglés:**多层防御**No hay un solo nivel suficiente.
- **Information security**El RAND SL-4 en la Lección 19 es una norma específica.
  En inglés:**信息安全**El modelo de la RAND SL-4 es un estándar específico.

### CAISI  Centro de Normas e Innovación de Inteligencia Artificial

- Opera dentro del NIST.
  En inglés, "NIST" es un programa de investigación y desarrollo de la ciencia.
- Se ejecuta acuerdos voluntarios con laboratorios fronterizos.
  Traducción:With前沿实验室运行自愿协议.
- Publica evaluaciones de capacidad no clasificadas centradas en los riesgos de las armas cibernéticas, biológicas y químicas.
  China: Publicar la evaluación de la capacidad de no secreto de la red de focalización de la seguridad de las armas biológicas y químicas.
- Diferente de CAIS; los acrónimos chocan; compruebe la URL (nist.gov) para confirmar cuál está leyendo.
  La traducción de la palabra en inglés es:

El papel de CAISI es el público, frente al gobierno contraparte de los compromisos de laboratorio privados de METR (lección 21). Los informes de CAISI no son clasificados; los informes de METR a menudo están cerrados por la NDA.

> El papel de CAISI es el de METR Private Person Laboratory合作 (§ 21 课) en el ámbito público, orientado al gobierno, a la interacción con los objetos.

### California SB-53

El proyecto de ley del Senado de California (20252026 sesión) aborda el riesgo catastrófico de los modelos fronterizos.

> La ley del Senado de la República de la República de la República de la República de la República de la República de la República de la República de la República de la República de la República de la República de la República de la República de la República de la República de la República de la República de la República de la República de la República de la República de la República de la República de la República de la República de la República de la República de la República de la República de la República de la República de la República de la República de la República de la República de la República de la República de la República de la República de la República de la República de la República de la República de la República de la República de la República de la República de la República de la República de la República de la República de la República de la República de la República de la República de la República de la República de la República de la República de la República de la República de la República de la República de la República de la República de la República de la República de la República de la República de la República de la República de la República de la República de la República de la República de la República de la República de la República de la República de la República de la República de la República de China de la República de la República de la República de la República de la República de la República de la República de la República de la República de la República de la República de la República de la República de la República de la República de la República de China de la República de la República de la República de la República de China de la República de la República de China de la República de China de la República de la República de China de China de la República de la República de China de China de China de la República de China de China de China de China de China de China de China de China de China de China de China de China de China de China de China de China de China de China de China de China de China de China de China de China de China de China de China de China de China de China de China de China de China de China de China de China de China de China de China de China de China de China de China de China de China de China de China de China de China de China de China de China de China de China de China de China de China de China de China de China de China de China de China de China de China de China de China de China de China de China de China de China de China de China de China de China

- Los límites de capacidad específicos que activan obligaciones a nivel estatal.
  Capacidad específica de la obligación estatal 值.
- Protecciones de denunciantes para empleados de laboratorio de IA.
  China: AI 实验室员工举报人保护.
- Requisitos para la notificación de incidentes en caso de fallas catastróficas.
  China: Catastrophe: los problemas de la vida

Si se firma, sería la primera regulación de riesgo catastrófico a nivel estatal de los Estados Unidos. Independientemente del estado de firma, el marco del proyecto de ley da forma a cómo otras legislaturas estatales se acercan al problema. Los practicantes en California deben rastrear el estado del proyecto de ley; los practicantes en otros lugares deben leerlo para entender cómo probablemente se verá la regulación a nivel estatal de los Estados Unidos.

> Si se firma, será la primera regulación de riesgos de catástrofes a nivel estatal de los Estados Unidos. Independientemente del estado de firma, el marco de la ley moldea cómo los legisladores de otros estados tratan los problemas.

### El riesgo a escala social no es un problema de una sola capa

El tema de la fase 15  defensa en profundidad  también se aplica a la capa social. Ninguna organización, regulación o marco único cierra el riesgo catastrófico. El ecosistema solo funciona cuando:

> La definición de la protección de los ecosistemas se aplica también a la sociedad. No hay una sola organización, normativas o marco que pueda cerrar el riesgo de catástrofe.

- Las políticas de escalación de los barcos de los laboratorios (lecciones 19, 20).
  En el caso de la investigación, el estudio de la investigación de la ciencia y el desarrollo de la ciencia y la tecnología, se ha desarrollado una serie de estudios de la ciencia y la tecnología.
- Los evaluadores externos producen mediciones (lección 21).
  La evaluación externa de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad de la calidad.
- La sociedad civil realiza seguimientos y publicaciones (CAIS).
  En el caso de los medios de comunicación, el gobierno de la República de China ha adoptado una política de seguimiento y difusión de la sociedad civil.
- El gobierno ejecuta programas voluntarios y regulación de referencia (CAISI, SB-53).
  El gobierno de la República de China ha adoptado una nueva política de control de la población.
- Los profesionales construyen controles de múltiples capas (lecciones 1018).
  La práctica de la construcción de un sistema de control de múltiples niveles (第 1018 课)

Esta es la síntesis final de la fase: cada lección anterior es una capa en una pila cuya integridad importa más que la fuerza de cualquier capa.

> Es el compendio final de la etapa: cada sección anterior es una capa de la pila, su integridad es más importante que la intensidad de cualquier sola capa.

## Usalo con el marco de ejecución
```figure
a5-four-risks
```

## Usalo

`code/main.py`En el caso de un proyecto de implementación, marca el despliegue en las cuatro categorías de riesgo y devuelve una lista de control de mitigación. Es una ayuda para leer el marco, no un sustituto del juicio humano.

> `code/main.py` Implementar un pequeño riesgo de mercado.  Implementar un pequeño riesgo de mercado.  Implementar un pequeño riesgo de mercado.  Implementar un pequeño riesgo de mercado.  Implementar un pequeño riesgo de mercado.  Implementar un pequeño riesgo de mercado.  Implementar un pequeño riesgo de mercado.  Implementar un pequeño riesgo de mercado.  Implementar un pequeño riesgo de mercado.  Implementar un pequeño riesgo de mercado.  Implementar un pequeño riesgo de mercado.  Implementar un pequeño riesgo de mercado.  Implementar un pequeño riesgo de mercado.  Implementar un pequeño riesgo de mercado.  Implementar un pequeño riesgo de mercado.  Implementar un pequeño riesgo de mercado.  Implementar un sistema de mercado.  Implementar un sistema de mercado.  Implementar un sistema de mercado.  Implementar un sistema de mercado.  Implementar un sistema de mercado.

## Envíe el producto .

`outputs/skill-societal-risk-review.md`Revisa una implementación para la postura de riesgo a escala social: cuáles de las cuatro categorías se refieren, cuáles son las medidas de mitigación, cuál es la exposición al riesgo organizacional.

> `outputs/skill-societal-risk-review.md`审查部署的社会规模风险姿态:触及四类中哪些有哪些缓解,组织风险暴露是什么, 审查部署的社会规模风险姿态:触及四类中哪些有哪些缓解, 审查部署的社会规模风险姿态:触及四类中哪些有哪些缓解, 审查部署的社会规模风险姿态:触及四类中哪些已有哪些缓解, 组织风险暴露是什么, 审查部署的社会规模风险姿态:触及四类中哪些已有哪些缓解, 审查部署的组织风险暴露是什么, 触及四类中哪些已有哪些缓解, 审查部署的组织风险暴露是什么, 触及四类中哪些已有哪些缓解

## Los ejercicios.

1. - ¿ Qué ?`code/main.py`. Introducir tres implementaciones sintéticas en diferentes escalas.
   Traducción:运行`code/main.py` introducir tres diferentes tipos de instalaciones de sintéticos.

2. Lea el documento completo sobre los cuatro riesgos del CAIS. Elige una categoría de riesgo y escriba dos párrafos sobre lo que cree que es el desarrollo más importante de 2026 en esa categoría.
   China: Completo lectura CAIS 四风险论文──select a风险类别, write two段关于你认为该类别 2026 最重要发展──

3. Lea el borrador actual del SB-53 de California. Identifique una disposición que cree fortalece la postura de riesgo catastrófico y una que cree que la debilita.
   La ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de la ley de

4. Seleccione una implementación de IA en producción que conozca (la suya o una publicada). Ponga en cuenta los subimpulsos de riesgo organizacional: cultura de seguridad, rigor de auditoría, defensas de múltiples capas, seguridad de la información. ¿Cuál es el más débil? ¿Cuánto costaría ponerlo a la par?
   ChinaXiv:select a uno que sabe de la producción de AI 部署(tuos o abiertos) ⋅对组织风险子杆打分:安全文化、审计严格性、多层防信息安全──cuál es el más débil? ¿cuál es el costo de alcanzar los estándares?

5. Esbozar una versión 2028 del marco de cuatro riesgos que refleje un año de capacidad adicional y un año de experiencia adicional en la implementación. ¿Qué agregaría, eliminaría o reagruparía?
   China 译文:勾勒反映一年额外能力和一年额外外署经验的四风险框架 2028 版本──你会添加、移除或重组什么?

## Términos clave .

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

## Más Leer más Leer más

- [Center for AI Safety](https://safe.ai/) el hogar institucional del marco de cuatro riesgos.
  Traducción:Cuatro instituciones del marco de la economía
- [CAIS — AI Risks that Could Lead to Catastrophe](https://safe.ai/ai-risk) el papel de cuatro riesgos.
  Traducción:El libro de la historia
- [CAIS — May 2023 statement on extinction risk](https://safe.ai/statement-on-ai-risk) Breve declaración conjunta.
  Traducción:简短联合声明
- [NIST CAISI](https://www.nist.gov/caisi) Centro de innovación y estándares de IA dirigidos al gobierno.
  China 翻译: Façã向政府的 AI 标准和创新中心
- [Anthropic — Measuring agent autonomy in practice](https://www.anthropic.com/research/measuring-agent-autonomy) conecta los compromisos de laboratorio con el marco a escala social.
  Enlace a la estructura de compromiso de la escala social
