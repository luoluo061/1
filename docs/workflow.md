# 运行流程说明

1. **导入**：`ModelingService.ingest` 读取 CSV，通过 `batch_validate` 校验字段。
2. **标准化**：`NormalizationPipeline.default` 按 trait schema 对数值、类别、颜色进行标准化。
3. **向量化**：`VectorBuilder` 依据 `VectorSchema` 将标准化结果编码为多维向量。
4. **权重应用**：`WeightManager.load` 载入权重方案，在相似度计算时用于加权。
5. **相似检索**：`RetrievalEngine.search` 采用余弦与融合策略返回 Top-K 候选。
6. **解释生成**：`SimilarityEngine.explain` 计算特征差异，`ExplanationBuilder` 生成解释文本。
7. **画像输出**：`ProfileGenerator.generate` 按规则组装版块并输出 narrative，`FileRepository` 持久化。
