import json
from pathlib import Path

import numpy as np

from app.config import get_settings

settings = get_settings()


class FaissVectorStore:
    def __init__(self) -> None:
        self.vector_dir = Path(settings.vector_dir)
        self.vector_dir.mkdir(parents=True, exist_ok=True)
        self.meta_path = self.vector_dir / "faiss_metadata.json"
        self.index_path = self.vector_dir / "financial_docs.faiss"
        self.ids: list[str] = []
        self.index = None
        self.dimension = None
        self._load()

    def _load(self) -> None:
        try:
            import faiss
        except ImportError:
            return
        if self.meta_path.exists():
            self.ids = json.loads(self.meta_path.read_text())
        if self.index_path.exists():
            self.index = faiss.read_index(str(self.index_path))
            self.dimension = self.index.d

    def _ensure_index(self, dimension: int) -> None:
        import faiss

        if self.index is None:
            self.dimension = dimension
            self.index = faiss.IndexFlatIP(dimension)

    def add(self, vector_ids: list[str], vectors: np.ndarray) -> None:
        vectors = self._normalize(vectors.astype("float32"))
        self._ensure_index(vectors.shape[1])
        self.index.add(vectors)
        self.ids.extend(vector_ids)
        self._persist()

    def search(self, query_vector: np.ndarray, limit: int = 20) -> list[tuple[str, float]]:
        if self.index is None or not self.ids:
            return []
        query_vector = self._normalize(query_vector.astype("float32").reshape(1, -1))
        scores, positions = self.index.search(query_vector, min(limit, len(self.ids)))
        return [(self.ids[pos], float(score)) for pos, score in zip(positions[0], scores[0]) if pos >= 0]

    def _persist(self) -> None:
        import faiss

        faiss.write_index(self.index, str(self.index_path))
        self.meta_path.write_text(json.dumps(self.ids, indent=2))

    @staticmethod
    def _normalize(vectors: np.ndarray) -> np.ndarray:
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        norms[norms == 0] = 1
        return vectors / norms
