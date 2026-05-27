from hashlib import sha256
from uuid import uuid4

import numpy as np
from sqlalchemy.orm import Session

from app.config import get_settings
from app.models.entities import Document, EmbeddingMetadata, SearchLog
from app.rag.vector_store import FaissVectorStore
from app.schemas.domain import SearchResult

settings = get_settings()


class RagPipeline:
    def __init__(self) -> None:
        self.vector_store = FaissVectorStore()
        self.embedder = None
        self.reranker = None

    def _embedder(self):
        if self.embedder is None:
            from sentence_transformers import SentenceTransformer

            self.embedder = SentenceTransformer(settings.embedding_model)
        return self.embedder

    def _reranker(self):
        if self.reranker is None:
            try:
                from sentence_transformers import CrossEncoder

                self.reranker = CrossEncoder(settings.reranker_model)
            except Exception:
                self.reranker = False
        return self.reranker

    def chunk_text(self, text: str) -> list[str]:
        try:
            from langchain_text_splitters import RecursiveCharacterTextSplitter
        except Exception:
            from langchain.text_splitter import RecursiveCharacterTextSplitter

        splitter = RecursiveCharacterTextSplitter(chunk_size=900, chunk_overlap=150)
        return [chunk for chunk in splitter.split_text(text) if chunk.strip()]

    def embed(self, texts: list[str]) -> np.ndarray:
        if not texts:
            return np.empty((0, 384), dtype="float32")
        return np.asarray(self._embedder().encode(texts, show_progress_bar=False), dtype="float32")

    def index_document(self, db: Session, document: Document) -> int:
        chunks = self.chunk_text(document.content_text)
        if not chunks:
            return 0
        vectors = self.embed(chunks)
        vector_ids = [f"doc-{document.id}-{idx}-{uuid4().hex[:8]}" for idx in range(len(chunks))]
        self.vector_store.add(vector_ids, vectors)
        for idx, (vector_id, chunk) in enumerate(zip(vector_ids, chunks)):
            db.add(EmbeddingMetadata(document_id=document.id, chunk_index=idx, vector_id=vector_id, chunk_text=chunk))
        db.commit()
        return len(chunks)

    def search(self, db: Session, query: str, user_id: int | None = None, top_k: int = 5) -> tuple[str, list[SearchResult]]:
        query_vector = self.embed([query])[0]
        raw_hits = self.vector_store.search(query_vector, limit=20)
        metadata = []
        for vector_id, score in raw_hits:
            row = db.query(EmbeddingMetadata).filter_by(vector_id=vector_id).first()
            if row:
                metadata.append((row, score))

        ranked = self.rerank(query, metadata)[:top_k]
        results = [
            SearchResult(
                document_id=row.document.id,
                title=row.document.title,
                company_name=row.document.company_name,
                document_type=row.document.document_type,
                chunk=row.chunk_text,
                score=score,
            )
            for row, score in ranked
        ]
        db.add(SearchLog(user_id=user_id, query=query, results_count=len(results)))
        db.commit()
        return self.generate_insights(query, results), results

    def rerank(self, query: str, hits: list[tuple[EmbeddingMetadata, float]]) -> list[tuple[EmbeddingMetadata, float]]:
        reranker = self._reranker()
        if reranker:
            pairs = [(query, row.chunk_text) for row, _ in hits]
            scores = reranker.predict(pairs).tolist() if pairs else []
            return sorted([(row, float(score)) for (row, _), score in zip(hits, scores)], key=lambda item: item[1], reverse=True)
        query_terms = set(query.lower().split())
        return sorted(
            hits,
            key=lambda item: item[1] + len(query_terms.intersection(item[0].chunk_text.lower().split())) / 20,
            reverse=True,
        )

    def generate_insights(self, query: str, results: list[SearchResult]) -> str:
        if not results:
            return "No relevant financial context was found for this query."
        companies = sorted({result.company_name for result in results})
        doc_types = sorted({result.document_type for result in results})
        evidence_hash = sha256("".join(result.chunk[:200] for result in results).encode()).hexdigest()[:8]
        return (
            f"Found {len(results)} high-relevance passages for '{query}'. "
            f"The evidence spans {', '.join(doc_types)} for {', '.join(companies)}. "
            f"Review the matched excerpts before making audit or credit decisions. Evidence ref: {evidence_hash}."
        )


rag_pipeline = RagPipeline()
