# 数据结构清单

## Domain
- `FlowerVariety`：核心品种实体，含形态、色彩、瓶插期等字段。
- `TraitValue`：单个性状值及其元数据。
- `FeatureVector`：向量值、映射关系与 schema ID。
- `SimilarityResult`：相似度分数与亮点。
- `Profile`：画像版块、摘要与向量快照。

## Normalization
- `NormalizationStep`：字段与对应 Normalizer 绑定。
- `NormalizationPipeline`：标准化步骤列表。

## Feature Engineering
- `Dimension`：向量维度描述，含类型与配置。
- `VectorSchema`：全量维度列表与总宽度计算。

## Weighting
- `WeightScheme`：命名权重集。
- `WeightConstraints`：权重上下界与归一化策略。

## Similarity
- `SimilarityEngine`：向量级相似度计算与解释。
- `RetrievalEngine`：检索流程与归一化。
- `ExplanationBuilder`：文本解释构建。

## Profiling
- `ProfileRules`：画像字段规则。
- `NarrativeTemplates`：叙述模板。
- `ProfileGenerator`：画像生成器。
