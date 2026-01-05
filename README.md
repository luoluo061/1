# 鲜花品种性状参数建模系统（flower_trait_modeling）

本项目是一个围绕鲜花品种的性状参数建模、相似检索与画像输出的示例性代码库，强调配置驱动与模块化设计。系统聚焦于：
- 建立品种基础数据结构与数据质量控制；
- 采集并标准化花型、花径、颜色、茎长、瓶插期等性状参数；
- 基于 schema 的多维特征向量构建与编码；
- 支持性状权重配置与约束；
- 提供相似度计算、可解释性说明与品种画像输出。

## 目录与模块
- `configs/`：trait schema、vector schema、默认权重、相似度与画像规则配置。
- `docs/`：软著写作辅助文档（接口、配置、数据结构、流程与算法大纲）。
- `examples/`：示例数据与输出，包括演示数据、权重方案和画像样例。
- `scripts/`：工具脚本，包含自动文档生成。
- `src/flower_trait_modeling/`：核心代码，按 domain/ingestion/normalization/feature_engineering/weighting/similarity/profiling/storage/evaluation/utils 分层。
- `tests/`：覆盖标准化、向量维度、权重约束、相似度一致性、画像字段完整等的测试模块。

## 使用提示
项目以配置驱动设计，可通过修改 `configs/` 下的 YAML 文件调整 schema、向量映射、权重、相似度策略与画像规则。示例 CLI 提供参数入口，`scripts/gen_docs.py` 会读取配置并输出 Markdown 文档草稿，便于软著编写。

## 注意
代码为参数建模与检索示例，不包含生产级持久化或训练流水线，仅用于展示设计与接口。
