"""
RAG (Retrieval-Augmented Generation) Module
=============================================
Hybrid semantic + keyword agricultural knowledge retrieval system.

Components:
- vector_store: HybridAgronomyVectorStore with ChromaDB + BM25 fusion
- query_engine: Context-aware synthesis with LLM + template fallback
- document_loader: Recursive semantic chunking with metadata extraction
- knowledge_base: Curated agronomic knowledge entries
"""
from app.rag.query_engine import query_rag
from app.rag.vector_store import vector_store
from app.rag.document_loader import load_documents_from_directory, load_pdfs_from_directory

__all__ = [
    "query_rag",
    "vector_store",
    "load_documents_from_directory",
    "load_pdfs_from_directory",
]
