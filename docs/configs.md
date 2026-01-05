# 配置清单

- `configs/trait_schema.yaml`：定义原始性状字段类型与约束。
- `configs/vector_schema.yaml`：定义向量维度、编码方式及 vocab。
- `configs/weights_default.yaml`：默认权重与约束，支持归一化策略。
- `configs/similarity.yaml`：相似度度量、融合策略与解释参数。
- `configs/profile_rules.yaml`：画像版块字段与叙述阈值。

## 配置驱动要点
1. 所有流程依赖配置而非硬编码，可在不改代码的情况下调整字段与权重。
2. 向量维度与编码方式由 schema 控制，避免手写索引。
3. 权重约束用于守护上下界并统一归一化策略。
4. 画像规则可增加新的版块与阈值，驱动 narrative 输出。
