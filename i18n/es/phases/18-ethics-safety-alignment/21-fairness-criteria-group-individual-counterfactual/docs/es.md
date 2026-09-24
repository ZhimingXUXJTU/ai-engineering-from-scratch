# Criterios de equidad  Grupo, Individual, Counterfactual  Contras hechos  imparcial 准则

> Tres familias estructuran la literatura de la justicia. Equidad de grupo: paridad demográfica, probabilidades igualadas, igualdad de precisión de uso condicional  tasas iguales entre los grupos protegidos en promedio. La equidad individual (Dwork et al. 2012): personas similares reciben decisiones similares; condición de Lipschitz en el mapa de decisiones. La equidad contrafactual (Kusner et al. 2017): una decisión es justa para un individuo si no se cambia cuando los atributos sensibles se alteran de manera contrafactual. Resultado teórico 2024 (NeurIPS 2024): existe un trade-off inherente entre CF y precisión; un método modelo-agnóstico convierte un predictor óptimo pero injusto en un predictor CF con pérdida limitada de precisión. Contrafactualidades de retroceso (arXiv:2401.13935, enero 2024): un nuevo paradigma que evita requerir intervenciones sobre atributos legalmente protegidos. Conciliación filosófica (ICLR Blogposts 2024): con gráficos causales, satisfacer ciertas medidas de equidad de grupo implica equidad contrafactual.

> **【中文解读】**Este capítulo presenta los principios de equidad: equidad de grupo, equidad de individuo y equidad de hecho. Tres familias dan diferentes estándares estructurales. Un modelo puede ser equitativo de grupo, pero no equitativo de individuo, equitativo de grupo, pero no equitativo de hecho.

> **【拓展：不可能定理 → 公平性冲突】**Chouldechova / Kleinberg-Mullainathan-Raghavan (en inglés) (2017): no se puede establecer que la igualdad de la población, la tasa de igualdad y la tasa de precisión de uso de las condiciones de igualdad no pueden ser satisfechas simultáneamente bajo la tasa de base de desigualdad.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, three-criteria comparison) | **语言:** Python（标准库，三标准比较）
**Prerequisites:** Phase 18 · 20 (bias), Phase 02 (classical ML) | **前置知识:** Phase 18 · 20 (偏见), Phase 02 (经典 ML)
**Time:** ~60 minutes | **时间:** ~60 分钟

> ¿ Qué es esto ?**【前置】**学本节前请先掌握:Fase 18·20(偏见) 、Fase 02(clásico ML) 、因果推断基础──公平性三大家族──
> ¿ Qué es esto ?**【类比】**公平 = "AI de la justicia天平"──群体公平(paridad demográfica/cuotas igualadas) = 平均上各组别结果相等;个体公平(Durado 2012) = 相似个体得相似决策;反事实公平(Kusner 2017) = 改变敏感属性决策不变──三者不能同时满足选择是政策决定──
> 🤔 NeurIPS 2024:CF-vs-acurate tiene un peso interno, pero hay un método de cambio de límite.

## Objetivos de aprendizaje

- En el artículo 1, apartado 1, del Reglamento (UE) n.o 1095/2013 se establece que los Estados miembros deben adoptar medidas de seguridad y seguridad en el caso de los grupos de trabajo.

> Explicar tres grupos de normas equitativas:

- Describa la equidad individual a través de la fórmula de Dwork et al. 2012 Lipschitz.

> 描述通过 Dwork 等人 2012年 Lipschitz 公式定义的个体公平──

- Describa la equidad contrafactual y su dependencia del gráfico causal.

> 描述反事实公平及其因果图依赖──

- Explica las contrafactualidades de retroceso y por qué evitan el problema de la intervención en el atributo protegido.

> Explicar los hechos y por qué se han evitado las intervenciones en las propiedades protegidas.

## El problema es el problema .

La lección 20 se trataba de medir el sesgo. La lección 21 se trata de definir el estándar de equidad que la medición debe servir. Las tres familias dan estándares estructuralmente diferentes  un modelo puede ser justo en grupo y injusto en individuo, justo en contrafacto y injusto en grupo. Elegir un estándar es una decisión política; ningún estándar es universalmente óptimo.

> La lección 20 es sobre la medición prejuicio. La lección 21 es sobre la definición de la medición y el servicio de los estándares equitativos.

## El concepto.

> **【中文解读】**群体公平三大标准: población平权P(Y=1 dondeA=a) = P(Y=1 dondeA=a'),各组接受率相等;均等化赔率P(Y=1在Y*=y,A=a) = P(Y=1在Y*=y,A=a'),各组真阳性率和假阳性率相等;条件使用准准率均等P Y*=yY=y,A=a) = P各Y(*=yY=y,A=a'),

### Equidad en grupo

- **Demographic parity.**P\Y=1\A=a=P\Y=1\A=a') para todos los grupos. tasas de aceptación iguales.
- **Equalized odds.**P  Y = 1  Y * y = a) = P  Y = 1  Y * y = a)  = a)  = igual TPR y FPR en todos los grupos.
- **Conditional use accuracy equality.**P * Y = y , Y = y, A = a) = P * Y * y , Y = y, A = a') Valor predictivo igual entre los grupos.

> La tasa de aceptación de los grupos de población es igual; la tasa de compensación es igual a la tasa de efectividad y la tasa de falsidad de los grupos de población; la tasa de precisión es igual a la tasa de efectividad y la tasa de efectividad es igual a la tasa de previsión de los grupos de población es igual o igual.

Impossibilidad (Chouldechova, Kleinberg-Mullainathan-Raghavan 2017): estos tres no pueden satisfacerse simultáneamente bajo tasas de base desiguales.

> No es posible resolver: en una tasa de desigualdad de base, estos tres no pueden cumplirse simultáneamente.

### La equidad individual

Dwork et al. 2012. Un mapa de decisión f es individualmente justo con respecto a una métrica de similitud específica de la tarea d si f(x) - f(x') <= L * d(x, x') para alguna constante Lipschitz.

> Dwork 等人 2012──decisión mapuche f Si se trata de un número regular de Lipschitz 满足 L  f                                                                                                                                                                                                                                                 

Requiere definir d. Cuestión política, no estadística.

> 需要定义 d.Este es un problema de política, no de estadística.

> **【拓展：反事实公平 → 因果图依赖】**Kusner 等人(2017) de la razón de hecho: bajo el modelo de causa, si la decisión posterior al cambio de la propiedad sensible del individuo contra la realidad no cambia, entonces la decisión es justa para el individuo.

### La equidad contrafactual

Una decisión es contrafactualmente justa para el individuo i si, bajo un modelo causal de la población, la decisión no cambia cuando los atributos sensibles i son alterados contrafactualmente.

> Kusner 等人 2017 ⋅ En el modelo de causa, si la decisión no cambia después de que el individuo tenga propiedades sensibles al contrario de los hechos, entonces la decisión es justa contra los hechos para ese individuo.

Requiere un DAG causal. El DAG es una elección de modelado. La equidad contrafactual es tan justificada como el DAG.

> 需要因果 DAG──DAG 是建模选择──反事实公平的合理性取决于DAG的合理性──

### El cambio entre CF y precisión

NeurIPS 2024 teórico: existe un compromiso inherente entre la equidad contrafactual y la precisión predictiva. Un método modelo-agnóstico puede convertir un predictor óptimo pero injusto en un predictor CF, a un costo de precisión limitado. El costo de precisión depende de la magnitud del coeficiente de atributos sensibles en el predictor injusto óptimo.

> NeurIPS 2024  Teoría Resultados: Existe un peso firme entre la realidad y la precisión de la predicción.

### Contrarreloj de retroceso

ArXiv:2401.13935 (enero 2024). Las contrafacturas tradicionales requieren intervenciones en el atributo sensible  "la decisión cambiaría si esta persona hubiera sido de un género diferente".

> La ley tiene problemas en la que se trata de la intervención de la naturaleza sensible.

Las contrafactualidades de retroceso cambian de dirección: en lugar de intervenir en el atributo, pregunte qué combinación de las características reales del individuo habría producido el resultado contrafactual.

> El retroceso contra los hechos no es una característica de intervención, sino que se pregunta qué combinación de las características reales de un individuo producirá los resultados contra los hechos.

> **【中文解读】**哲学调和(ICLR Blogposts 2024): después de tener una gráfica de factores, satisfacer la medida de equidad de ciertos grupos implica un equilibrio de factores de hecho.

### Reconciliación filosófica

ICLR Blogposts 2024. Con un gráfico causal en la mano, satisfacer ciertas medidas de equidad de grupo implica equidad contrafactual. Las tres familias no son ortogonales; son diferentes facetas de la misma estructura causal subyacente.

> ICLR 2024: después de la figura de la causa, satisfacer la equidad de ciertos grupos implica la equidad de los hechos.

Esto no resuelve los teoremas de imposibilidad (tasas de base desiguales aún impiden la equidad simultánea de grupo). Pero muestra que la aparente oposición entre "grupos" y "individuales / contrafactos" es parcialmente un artefacto de no ser explícito sobre el modelo causal.

> No hay solución imposible de teorizar, pero se muestra que la parte superficial de la oposición entre "grupos" y "individuo/contrarechos" es porque no hay hipótesis claras causadas por el modelo de causa.

### Donde esto encaja en la Fase 18

La lección 20 es la medición de sesgos. La lección 21 es la definición de equidad. La lección 22 es privacidad (privalidad diferencial). La lección 23 es marcado de agua. Estas son las lecciones adyacentes a la asignación que complementan las lecciones 7-11 adyacentes al engaño.

> Lección 20 es prejuicio de la medida. Lección 21 es definición equitativa. Lección 22 es privacidad. Lección 23 es agua.

> **【拓展：CF vs 准确性权衡 → 实际影响】**NeurIPS 2024  Resultados teóricos: Existe un peso firme entre el antifacto público y la precisión de la predicción. Un método de modelo inconcebible puede convertir el predicador óptimo pero injusto en CF justo, pero la pérdida de precisión tiene límites dependiendo del tamaño de los factores de propiedades sensibles en el predicador injusto. Esto significa que elegir un estándar justo tiene un costo real.

## Usalo.
```figure
an-fairness-trilemma
```

## Usalo

`code/main.py`construye un conjunto de datos de clasificación binaria de juguete con un atributo sensible y tasas de base desiguales. Computa la paridad demográfica, las probabilidades igualadas y la igualdad de precisión de uso condicional en un clasificador simple. Observa las tres métricas que no coinciden. Aplique una nueva ponderación para la paridad demográfica y observa su costo en los otros dos.

> `code/main.py` Construir un conjunto de datos de juguetes de tipo II con características sensibles y tasas de base de desigualdad.  Calcular tres grupos de índices de equidad, observar sus discrepancias.  Aplicar el equilibrio de peso y el peso de la población y observar los precios de los otros dos.

## Envíalo .

Esta lección produce`outputs/skill-fairness-criterion.md`. Dado un reclamo o una política de equidad, se identifica el criterio que se está reclamando, si el modelo puede satisfacer los criterios restantes en virtud de las tasas de base desiguales reclamadas y de qué DAG causal depende el reclamo.

> 本课产 出  `outputs/skill-fairness-criterion.md` Dado un declarativo o política de equidad, la declaración de identidad es el criterio de satisfacción de los demás criterios en base a la tasa de desigualdad, así como el DAG de la declaración de la dependencia de la causa.

## Los ejercicios.

1. - ¿ Qué ?`code/main.py`.Informe las tres métricas de grupo en los datos predeterminados.Aplicar la reponderación y reinforme dirigida a la paridad demográfica.

2. Implemente la métrica de equidad individual de Dwork et al. 2012 utilizando L2 en características no sensibles.

3. Lea Kusner et al. 2017. Construye un simple DAG causal de dos características para la puntuación de resumen e identifique la condición de equidad contrafactual que implica.

4. El documento de contrafactos de retroceso de 2024 evita la intervención en los atributos protegidos.

5. La reconciliación del ICLR 2024 argumenta que la equidad de grupo y contrafactual son facetas de la misma estructura.`code/main.py`y indicar la suposición causal que los haga equivalentes.

## Términos clave .

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| Demographic parity | "equal rates" | P(Y=1 | A=a) equal across groups |
| Equalized odds | "equal TPR/FPR" | Equal true-positive and false-positive rates across groups |
| Conditional use accuracy | "equal PPV/NPV" | Equal predictive values across groups |
| Individual fairness | "Lipschitz condition" | Similar individuals get similar decisions |
| Counterfactual fairness | "causal alteration invariance" | Decision unchanged under counterfactual attribute alteration |
| Backtracking counterfactual | "explain via actuals" | Counterfactual reasoned backward from outcome, not forward from attribute |
| Impossibility theorem | "the three conflict" | Chouldechova / KMR 2017: group criteria mutually exclusive under unequal base rates |

## Más Leer más Leer más

- [Dwork et al. — Fairness through Awareness (arXiv:1104.3913)](https://arxiv.org/abs/1104.3913) equidad individual
- [Kusner, Loftus, Russell, Silva — Counterfactual Fairness (arXiv:1703.06856)](https://arxiv.org/abs/1703.06856) equidad contrafactual
- [Chouldechova — Fair prediction with disparate impact (arXiv:1703.00056)](https://arxiv.org/abs/1703.00056) Imposible
- [Backtracking Counterfactuals (arXiv:2401.13935)](https://arxiv.org/abs/2401.13935) Nuevo paradigma para las intervenciones de atributos protegidos
