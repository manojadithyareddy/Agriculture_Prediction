"""
vector_store.py — Hybrid Semantic + Keyword Agricultural RAG Vector Store
==========================================================================
Phase 1: ChromaDB + sentence-transformer embeddings for real semantic search.
Phase 3: Hybrid retrieval with Reciprocal Rank Fusion (BM25 + vector).
Phase 4: Agricultural synonym query expansion.

Architecture:
    User Query
        ├─► ChromaDB cosine similarity  (semantic)   ──┐
        │                                               ├─► RRF Fusion ─► Top-k
        └─► BM25 keyword scoring        (lexical)   ──┘

Falls back to enhanced BM25-only if ChromaDB / sentence-transformers
are not installed, so the app never crashes.
"""
from __future__ import annotations

import logging
import math
import re
import time
from typing import List, Dict, Any, Optional, Tuple

from app.rag.knowledge_base import AGRICULTURE_KNOWLEDGE

logger = logging.getLogger(__name__)

# ────────────────────────────────────────────────────────────
# Phase 4: Agricultural Synonym Map for Query Expansion
# ────────────────────────────────────────────────────────────
AGRI_SYNONYMS: Dict[str, List[str]] = {
    "blast": ["magnaporthe", "pyricularia", "leaf blast", "neck blast", "panicle blast"],
    "sigatoka": ["black sigatoka", "yellow sigatoka", "leaf spot", "mycosphaerella"],
    "leaf spot": ["sigatoka", "cercospora", "alternaria", "foliar lesion"],
    "wilt": ["fusarium wilt", "verticillium wilt", "bacterial wilt", "wilting"],
    "blight": ["bacterial blight", "late blight", "early blight", "leaf blight", "turcicum"],
    "rust": ["stem rust", "leaf rust", "stripe rust", "puccinia"],
    "mildew": ["powdery mildew", "downy mildew", "erysiphe", "pseudoperonospora"],
    "canker": ["citrus canker", "xanthomonas", "bacterial canker"],
    "anthracnose": ["colletotrichum", "fruit rot", "blossom blight"],
    "armyworm": ["fall armyworm", "spodoptera", "faw", "army worm"],
    "bollworm": ["pink bollworm", "pectinophora", "helicoverpa", "boll worm"],
    "hopper": ["brown plant hopper", "bph", "mango hopper", "leafhopper", "jassid"],
    "aphid": ["aphids", "plant lice", "greenfly", "blackfly"],
    "whitefly": ["white fly", "bemisia", "trialeurodes"],
    "thrips": ["thrip", "scirtothrips", "frankliniella"],
    "fertilizer": ["nutrient", "npk", "urea", "dap", "potash", "manure", "compost"],
    "nitrogen": ["urea", "ammonium", "nitrate", "n deficiency"],
    "phosphorus": ["phosphate", "dap", "ssp", "p deficiency"],
    "potassium": ["potash", "mop", "k deficiency", "k2o"],
    "irrigation": ["watering", "drip", "sprinkler", "water management", "moisture"],
    "organic": ["bio", "biological", "neem", "trichoderma", "pseudomonas"],
    # Hindi / Telugu regional terms
    "khaira": ["zinc deficiency", "rice khaira"],
    "telya": ["bacterial blight", "pomegranate oily spot"],
    "tikka": ["leaf spot", "groundnut tikka"],
    "karpa": ["blast", "rice blast"],
}


def expand_query(query: str) -> str:
    """
    Expand user query with agricultural synonyms to improve recall.
    Only adds terms not already present in the query.
    """
    query_lower = query.lower()
    expansions: List[str] = []

    for trigger, synonyms in AGRI_SYNONYMS.items():
        if trigger in query_lower:
            for syn in synonyms:
                if syn not in query_lower:
                    expansions.append(syn)

    if expansions:
        # Limit expansion to avoid noise — take top 6 most relevant
        expanded = query + " " + " ".join(expansions[:6])
        logger.debug(f"Query expanded: '{query}' → '{expanded}'")
        return expanded
    return query


# ────────────────────────────────────────────────────────────
# Embedding Model Loader (lazy, cached)
# ────────────────────────────────────────────────────────────
_embedding_model = None
_embedding_attempted = False
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_DIMENSION = 384


def _get_embedding_model():
    """Lazy-load the sentence-transformer embedding model."""
    global _embedding_model, _embedding_attempted
    if _embedding_model is not None or _embedding_attempted:
        return _embedding_model
    _embedding_attempted = True
    try:
        from sentence_transformers import SentenceTransformer
        logger.info(f"Loading embedding model: {EMBEDDING_MODEL_NAME}...")
        _embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)
        logger.info("Embedding model loaded successfully.")
    except Exception as e:
        logger.warning(f"sentence-transformers not available ({e}); using BM25-only mode.")
        _embedding_model = None
    return _embedding_model


def _encode_texts(texts: List[str]) -> Optional[List[List[float]]]:
    """Encode texts into dense vectors. Returns None if model unavailable."""
    model = _get_embedding_model()
    if model is None:
        return None
    embeddings = model.encode(texts, show_progress_bar=False, normalize_embeddings=True)
    return embeddings.tolist()


# ────────────────────────────────────────────────────────────
# ChromaDB Client (lazy, persistent)
# ────────────────────────────────────────────────────────────
_chroma_collection = None
_chroma_attempted = False
CHROMA_COLLECTION_NAME = "agriculture_knowledge"


def _get_chroma_collection(persist_dir: str):
    """Lazy-load ChromaDB persistent client and collection."""
    global _chroma_collection, _chroma_attempted
    if _chroma_collection is not None or _chroma_attempted:
        return _chroma_collection
    _chroma_attempted = True
    try:
        import chromadb
        from chromadb.config import Settings as ChromaSettings

        client = chromadb.Client(ChromaSettings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=persist_dir,
            anonymized_telemetry=False,
        ))
        _chroma_collection = client.get_or_create_collection(
            name=CHROMA_COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"},
        )
        logger.info(
            f"ChromaDB collection '{CHROMA_COLLECTION_NAME}' ready "
            f"({_chroma_collection.count()} documents)."
        )
    except Exception as e:
        logger.warning(f"ChromaDB not available ({e}); using BM25-only mode.")
        _chroma_collection = None
    return _chroma_collection


# ────────────────────────────────────────────────────────────
# Main Hybrid Vector Store
# ────────────────────────────────────────────────────────────
class HybridAgronomyVectorStore:
    """
    Production-grade hybrid retrieval store combining:
    - ChromaDB dense vector search (semantic similarity)
    - BM25 sparse keyword scoring (lexical matching)
    - Reciprocal Rank Fusion to merge both ranked lists
    - Domain-specific filter boosting for crop/condition metadata

    Gracefully falls back to BM25-only when ChromaDB or
    sentence-transformers are unavailable.
    """

    def __init__(
        self,
        documents: Optional[List[Dict[str, Any]]] = None,
        chroma_persist_dir: Optional[str] = None,
    ):
        self.documents: List[Dict[str, Any]] = (
            documents if documents is not None else list(AGRICULTURE_KNOWLEDGE)
        )
        self._chroma_dir = chroma_persist_dir
        self._chroma_populated = False

        # Build the BM25 inverted index
        self._build_bm25_index()

        # Stats
        self._query_count = 0
        self._total_latency_ms = 0.0

    # ── Document Management ──────────────────────────────────

    def add_documents(self, docs: List[Dict[str, Any]]):
        """Add new documents to both BM25 index and ChromaDB."""
        new_count = 0
        existing_ids = {d.get("id") for d in self.documents}

        for doc in docs:
            doc_id = doc.get("id", f"doc_{len(self.documents)}")
            if doc_id in existing_ids:
                continue
            doc["id"] = doc_id
            self.documents.append(doc)
            existing_ids.add(doc_id)
            new_count += 1

        if new_count > 0:
            self._build_bm25_index()
            self._chroma_populated = False  # Force re-population
            logger.info(f"Added {new_count} new documents (total: {len(self.documents)}).")

    def add_document(self, doc: Dict[str, Any]):
        """Add a single document."""
        self.add_documents([doc])

    @property
    def document_count(self) -> int:
        return len(self.documents)

    # ── BM25 Index ───────────────────────────────────────────

    def _tokenize(self, text: str) -> List[str]:
        """Tokenize text for BM25 scoring."""
        cleaned = re.sub(r"[^a-zA-Z0-9\s]", " ", text.lower())
        return [w for w in cleaned.split() if len(w) > 2]

    def _build_bm25_index(self):
        """Build inverted index for BM25 scoring."""
        self.vocab = set()
        self.doc_freq: Dict[str, int] = {}
        self.doc_tokens: List[List[str]] = []
        self.avg_doc_len = 0.0

        total_tokens = 0
        for doc in self.documents:
            full_text = " ".join([
                doc.get("crop", ""),
                doc.get("condition", ""),
                doc.get("category", ""),
                doc.get("title", ""),
                doc.get("content", ""),
            ])
            tokens = self._tokenize(full_text)
            self.doc_tokens.append(tokens)
            total_tokens += len(tokens)

            for t in set(tokens):
                self.vocab.add(t)
                self.doc_freq[t] = self.doc_freq.get(t, 0) + 1

        self.total_docs = len(self.documents)
        self.avg_doc_len = total_tokens / max(self.total_docs, 1)

    def _bm25_score(self, query_tokens: List[str], doc_idx: int) -> float:
        """Compute BM25 score for a single document."""
        tokens = self.doc_tokens[doc_idx]
        doc_len = len(tokens)
        if doc_len == 0:
            return 0.0

        k1, b = 1.5, 0.75
        score = 0.0

        for qt in query_tokens:
            tf = tokens.count(qt)
            if tf == 0:
                continue
            df = self.doc_freq.get(qt, 0)
            idf = math.log(1.0 + (self.total_docs - df + 0.5) / (df + 0.5))
            norm_tf = (tf * (k1 + 1)) / (tf + k1 * (1 - b + b * (doc_len / self.avg_doc_len)))
            score += idf * norm_tf

        return score

    def _bm25_search(
        self,
        query: str,
        k: int,
        crop_filter: Optional[str] = None,
        condition_filter: Optional[str] = None,
    ) -> List[Tuple[int, float]]:
        """Run BM25 search, return list of (doc_index, score) pairs."""
        query_tokens = self._tokenize(query)
        if not query_tokens:
            return [(i, 0.0) for i in range(min(k, self.total_docs))]

        scored: List[Tuple[int, float]] = []
        for idx in range(self.total_docs):
            doc = self.documents[idx]
            score = self._bm25_score(query_tokens, idx)

            # Domain metadata boosting
            doc_crop = doc.get("crop", "").lower()
            doc_cond = doc.get("condition", "").lower()

            if crop_filter and crop_filter.lower() in doc_crop:
                score += 5.0
            if condition_filter and condition_filter.lower() in doc_cond:
                score += 8.0

            # Bonus for query terms appearing in metadata fields
            for qt in query_tokens:
                if qt in doc_crop:
                    score += 3.0
                if qt in doc_cond:
                    score += 5.0

            scored.append((idx, score))

        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:k]

    # ── ChromaDB Vector Search ───────────────────────────────

    def _ensure_chroma_populated(self):
        """Populate ChromaDB with embeddings if not done yet."""
        if self._chroma_populated:
            return

        collection = _get_chroma_collection(self._chroma_dir or ".")
        if collection is None:
            return

        # Check if collection already has documents
        if collection.count() >= len(self.documents):
            self._chroma_populated = True
            return

        # Encode all documents
        texts = []
        ids = []
        metadatas = []
        for doc in self.documents:
            text = " ".join([
                doc.get("title", ""),
                doc.get("crop", ""),
                doc.get("condition", ""),
                doc.get("content", ""),
            ])
            texts.append(text)
            ids.append(doc.get("id", f"doc_{len(ids)}"))
            metadatas.append({
                "crop": doc.get("crop", ""),
                "condition": doc.get("condition", ""),
                "category": doc.get("category", ""),
                "source": doc.get("source", ""),
            })

        embeddings = _encode_texts(texts)
        if embeddings is None:
            return

        # Batch upsert into ChromaDB
        batch_size = 100
        for i in range(0, len(texts), batch_size):
            batch_end = min(i + batch_size, len(texts))
            collection.upsert(
                ids=ids[i:batch_end],
                embeddings=embeddings[i:batch_end],
                documents=texts[i:batch_end],
                metadatas=metadatas[i:batch_end],
            )

        self._chroma_populated = True
        logger.info(f"ChromaDB populated with {len(texts)} document embeddings.")

    def _vector_search(
        self,
        query: str,
        k: int,
        crop_filter: Optional[str] = None,
    ) -> Optional[List[Tuple[int, float]]]:
        """
        Run ChromaDB vector similarity search.
        Returns list of (doc_index, similarity_score) or None if unavailable.
        """
        self._ensure_chroma_populated()

        collection = _get_chroma_collection(self._chroma_dir or ".")
        if collection is None:
            return None

        query_embedding = _encode_texts([query])
        if query_embedding is None:
            return None

        # Build ChromaDB where filter
        where_filter = None
        if crop_filter:
            where_filter = {"crop": {"$eq": crop_filter}}

        try:
            results = collection.query(
                query_embeddings=query_embedding,
                n_results=min(k, collection.count()),
                where=where_filter if where_filter else None,
                include=["distances"],
            )
        except Exception as e:
            logger.warning(f"ChromaDB query failed ({e}); falling back to BM25.")
            return None

        if not results or not results.get("ids"):
            return None

        # Map ChromaDB IDs back to document indices
        id_to_idx = {doc.get("id", f"doc_{i}"): i for i, doc in enumerate(self.documents)}
        scored = []
        for doc_id, distance in zip(results["ids"][0], results["distances"][0]):
            idx = id_to_idx.get(doc_id)
            if idx is not None:
                # ChromaDB returns cosine distance; convert to similarity
                similarity = max(0.0, 1.0 - distance)
                scored.append((idx, similarity))

        return scored

    # ── Phase 3: Reciprocal Rank Fusion ──────────────────────

    @staticmethod
    def _reciprocal_rank_fusion(
        ranked_lists: List[List[Tuple[int, float]]],
        k_rrf: int = 60,
    ) -> List[Tuple[int, float]]:
        """
        Reciprocal Rank Fusion merges multiple ranked lists.
        RRF_score(d) = Σ 1 / (k + rank_i(d))
        """
        fused_scores: Dict[int, float] = {}

        for ranked_list in ranked_lists:
            for rank, (doc_idx, _original_score) in enumerate(ranked_list):
                if doc_idx not in fused_scores:
                    fused_scores[doc_idx] = 0.0
                fused_scores[doc_idx] += 1.0 / (k_rrf + rank + 1)

        # Sort by fused score descending
        fused = sorted(fused_scores.items(), key=lambda x: x[1], reverse=True)
        return fused

    # ── Main Search Interface ────────────────────────────────

    def similarity_search(
        self,
        query: str,
        k: int = 4,
        crop_filter: Optional[str] = None,
        condition_filter: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Hybrid retrieval pipeline:
        1. Expand query with agricultural synonyms
        2. Run BM25 keyword search (top-20 candidates)
        3. Run ChromaDB vector search (top-20 candidates) if available
        4. Fuse results with Reciprocal Rank Fusion
        5. Return top-k with relevance scores
        """
        t_start = time.perf_counter()
        self._query_count += 1

        # Phase 4: Expand query with synonyms
        expanded_query = expand_query(query)

        # Candidate pool size — retrieve more than k for re-ranking
        candidate_k = min(max(k * 5, 20), self.total_docs)

        # Stage 1: BM25 keyword search
        bm25_results = self._bm25_search(
            expanded_query, candidate_k, crop_filter, condition_filter
        )

        # Stage 2: Vector search (if available)
        vector_results = self._vector_search(expanded_query, candidate_k, crop_filter)

        # Stage 3: Fuse results
        if vector_results:
            fused = self._reciprocal_rank_fusion(
                [bm25_results, vector_results]
            )
        else:
            # BM25-only mode
            fused = [(idx, score) for idx, score in bm25_results]

        # Build response
        results: List[Dict[str, Any]] = []
        for doc_idx, fused_score in fused[:k]:
            res = dict(self.documents[doc_idx])
            res["relevance_score"] = round(fused_score, 4)
            res["retrieval_method"] = "hybrid" if vector_results else "bm25"
            results.append(res)

        # Observability logging
        elapsed_ms = (time.perf_counter() - t_start) * 1000
        self._total_latency_ms += elapsed_ms
        logger.info(
            f"RAG search [{self._query_count}]: "
            f"query='{query[:60]}...' | "
            f"method={'hybrid' if vector_results else 'bm25'} | "
            f"results={len(results)} | "
            f"latency={elapsed_ms:.1f}ms"
        )

        return results

    # ── Observability / Stats ────────────────────────────────

    def get_stats(self) -> Dict[str, Any]:
        """Return store statistics for the health endpoint."""
        collection = _get_chroma_collection(self._chroma_dir or ".")
        return {
            "total_documents": len(self.documents),
            "chroma_available": collection is not None,
            "chroma_count": collection.count() if collection else 0,
            "embeddings_available": _get_embedding_model() is not None,
            "embedding_model": EMBEDDING_MODEL_NAME,
            "bm25_vocab_size": len(self.vocab),
            "queries_served": self._query_count,
            "avg_latency_ms": round(
                self._total_latency_ms / max(self._query_count, 1), 1
            ),
        }


# ────────────────────────────────────────────────────────────
# Global singleton store instance
# ────────────────────────────────────────────────────────────
def _get_chroma_dir() -> str:
    """Resolve ChromaDB persist directory from config."""
    try:
        from app.config import settings
        return settings.CHROMA_DB_DIR
    except Exception:
        return "agriculture_db"


vector_store = HybridAgronomyVectorStore(chroma_persist_dir=_get_chroma_dir())
