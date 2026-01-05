# 接口清单

## CLI
- `flower_trait_modeling.cli:main(argv=None)`：加载配置、运行导入与画像流程。

## Service 层
- `ModelingService.ingest(csv_path)`：读取 CSV 并验证字段。
- `ModelingService.normalize_and_vectorize(records)`：执行标准化与向量构建。
- `ModelingService.search(query_vector, candidate_vectors)`：相似检索并生成解释。
- `ModelingService.profile(normalized)`：生成画像并持久化。

## Normalization
- `NormalizationPipeline.run(payload)`：按序应用标准化步骤。
- `MinMaxNormalizer.normalize(value)`：区间缩放。
- `CategoricalNormalizer.normalize(value)`：类别映射校验。

## Feature Engineering
- `VectorSchema.from_file(path)`：解析向量 schema。
- `VectorBuilder.build(payload)`：生成 `FeatureVector`。
- `VectorScaler.scale(values)`：向量缩放。

## Weighting
- `WeightManager.load(path)`：加载权重方案。
- `WeightManager.apply(values, scheme)`：应用权重。

## Similarity
- `SimilarityEngine.compare(query, candidate)`：计算相似度。
- `RetrievalEngine.search(query, candidates, top_k)`：检索最相似品种。
- `ExplanationBuilder.build(result, reasons)`：构建可解释输出。

## Profiling
- `ProfileGenerator.generate(record, vector)`：生成画像。
- `ProfileRules.extract_sections(record)`：按规则抽取字段。

## Storage
- `FileRepository.save_vector(vector)`、`load_profiles()`：文件存储示例。
- `SQLiteRepository.save_vector(vector)`：SQLite 存储示例。
