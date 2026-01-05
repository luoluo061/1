"""Service orchestration for the flower trait modeling system."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

from ..ingestion.importers import read_csv
from ..ingestion.validators import batch_validate
from ..normalization.pipeline import NormalizationPipeline
from ..feature_engineering.vector_schema import VectorSchema
from ..feature_engineering.vector_builder import VectorBuilder
from ..weighting.constraints import WeightConstraints
from ..weighting.manager import WeightManager
from ..similarity.engine import SimilarityEngine
from ..similarity.retrieval import RetrievalEngine
from ..similarity.explain import ExplanationBuilder
from ..profiling.generator import ProfileGenerator
from ..profiling.rules import ProfileRules
from ..profiling.templates import NarrativeTemplates
from ..storage.repo_file import FileRepository
from ..utils.logging import get_logger

logger = get_logger(__name__)


@dataclass
class ModelingService:
    trait_schema_path: str
    vector_schema_path: str
    weights_path: str
    profile_rules_path: str
    storage_dir: str

    def _setup(self) -> None:
        self.pipeline = NormalizationPipeline.default()
        self.vector_schema = VectorSchema.from_file(self.vector_schema_path)
        self.vector_builder = VectorBuilder(self.vector_schema)
        constraint = WeightConstraints(min_weight=0.0, max_weight=1.0, normalization="l1")
        self.weight_manager = WeightManager(constraint)
        self.weight_scheme = self.weight_manager.load(self.weights_path)
        self.similarity_engine = SimilarityEngine({"vector": 1.0})
        self.retrieval_engine = RetrievalEngine(self.similarity_engine)
        self.profile_generator = ProfileGenerator(ProfileRules.from_file(self.profile_rules_path), NarrativeTemplates())
        self.repository = FileRepository(self.storage_dir)
        self.explainer = ExplanationBuilder()
        logger.info("Service setup complete")

    def ingest(self, csv_path: str) -> List[Dict[str, str | float]]:
        varieties = read_csv(csv_path)
        validated = batch_validate([v.to_record() for v in varieties])
        logger.info("Ingested varieties", extra={"count": len(validated)})
        return [v.to_record() for v in varieties]

    def normalize_and_vectorize(self, records: List[Dict[str, str | float]]) -> List[Dict[str, object]]:
        normalized_records: List[Dict[str, object]] = []
        for record in records:
            normalized = self.pipeline.run(dict(record))
            vector = self.vector_builder.build(normalized)
            self.repository.save_vector(vector)
            normalized_records.append({"record": normalized, "vector": vector})
        return normalized_records

    def search(self, query_vector: Dict[str, object], candidate_vectors: List[Dict[str, object]]) -> List[Dict[str, object]]:
        query = query_vector["vector"]
        candidates = [item["vector"] for item in candidate_vectors]
        results = self.retrieval_engine.search(query, candidates, top_k=5)
        packaged: List[Dict[str, object]] = []
        for res in results:
            reasons = self.similarity_engine.explain(query, candidates[0])
            explanation = self.explainer.build(res, reasons)
            packaged.append({"result": res, "explanation": explanation})
        return packaged

    def profile(self, normalized: List[Dict[str, object]]) -> List[Dict[str, object]]:
        outputs: List[Dict[str, object]] = []
        for item in normalized:
            record = item["record"]
            vector = item["vector"]
            profile = self.profile_generator.generate(record, vector)
            self.repository.save_profile(profile)
            outputs.append({"profile": profile})
        return outputs


__all__ = ["ModelingService"]
