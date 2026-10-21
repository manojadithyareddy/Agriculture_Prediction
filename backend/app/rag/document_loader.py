"""
document_loader.py — Intelligent Document Ingestion Pipeline
==============================================================
Phase 2: Recursive semantic chunking with metadata extraction.

Improvements over the original:
- Recursive text splitting: paragraph → sentence → word (never mid-sentence)
- Automatic metadata extraction (crop, disease, category) from content
- Support for PDF, TXT, and Markdown files
- Deduplication by content hash
- Wired into startup auto-ingestion
"""
from __future__ import annotations

import glob
import hashlib
import logging
import os
import re
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

# ────────────────────────────────────────────────────────────
# Crop & Condition Auto-Detection
# ────────────────────────────────────────────────────────────
KNOWN_CROPS = [
    "rice", "maize", "corn", "wheat", "banana", "mango", "citrus", "orange",
    "lemon", "lime", "watermelon", "grapes", "grape", "beans", "soybean",
    "pomegranate", "cotton", "groundnut", "peanut", "tomato", "potato",
    "onion", "chili", "pepper", "sugarcane", "coffee", "tea", "coconut",
    "sunflower", "mustard", "sesame", "jute", "millets", "sorghum",
    "pigeonpea", "chickpea", "lentil", "cowpea",
]

KNOWN_CONDITIONS = [
    "blast", "blight", "wilt", "rust", "mildew", "canker", "anthracnose",
    "sigatoka", "mosaic", "leaf spot", "rot", "smut", "scab", "damping off",
    "armyworm", "bollworm", "hopper", "aphid", "whitefly", "thrips",
    "borer", "mite", "nematode", "leaf miner", "fruit fly",
    "nitrogen", "phosphorus", "potassium", "zinc", "iron", "boron",
    "deficiency", "toxicity",
]

CATEGORY_KEYWORDS = {
    "Disease": ["fungal", "bacterial", "viral", "disease", "pathogen", "infection",
                "blight", "blast", "wilt", "rust", "mildew", "canker", "rot",
                "anthracnose", "sigatoka", "mosaic", "smut", "scab"],
    "Pest": ["pest", "insect", "larva", "larvae", "moth", "caterpillar",
             "armyworm", "bollworm", "hopper", "aphid", "whitefly", "thrips",
             "borer", "mite", "nematode", "weevil", "beetle"],
    "Fertilizer": ["fertilizer", "nutrient", "npk", "nitrogen", "phosphorus",
                   "potassium", "zinc", "iron", "boron", "deficiency",
                   "manure", "compost", "urea", "dap"],
    "Irrigation": ["irrigation", "watering", "drip", "sprinkler", "moisture",
                   "water management", "drought", "waterlogging"],
}


def _detect_crop(text: str) -> str:
    """Auto-detect crop name from content."""
    text_lower = text.lower()
    for crop in KNOWN_CROPS:
        if crop in text_lower:
            return crop.capitalize()
    return "General"


def _detect_condition(text: str) -> str:
    """Auto-detect disease/pest/condition from content."""
    text_lower = text.lower()
    for condition in KNOWN_CONDITIONS:
        if condition in text_lower:
            return condition.title()
    return "Agronomy Guide"


def _detect_category(text: str) -> str:
    """Auto-detect category (Disease, Pest, Fertilizer, Irrigation)."""
    text_lower = text.lower()
    scores = {}
    for category, keywords in CATEGORY_KEYWORDS.items():
        scores[category] = sum(1 for kw in keywords if kw in text_lower)
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "General"


# ────────────────────────────────────────────────────────────
# Recursive Semantic Text Splitter
# ────────────────────────────────────────────────────────────
class RecursiveSemanticSplitter:
    """
    Splits text into chunks that respect semantic boundaries:
    1. Try splitting by double newline (paragraphs)
    2. Then by single newline
    3. Then by sentence boundaries (. ! ?)
    4. Finally by word boundaries

    Each chunk maintains overlap with neighbors for context continuity.
    """

    def __init__(
        self,
        chunk_size: int = 800,
        chunk_overlap: int = 150,
        min_chunk_size: int = 80,
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.min_chunk_size = min_chunk_size
        self._separators = [
            "\n\n",           # paragraph
            "\n",             # line break
            r"(?<=[.!?])\s+", # sentence boundary (regex)
            " ",              # word boundary
        ]

    def split_text(self, text: str) -> List[str]:
        """Split text into semantically coherent chunks with overlap."""
        text = text.strip()
        if len(text) <= self.chunk_size:
            return [text] if len(text) >= self.min_chunk_size else []

        chunks = self._recursive_split(text, 0)

        # Apply overlap by prepending end of previous chunk
        if self.chunk_overlap > 0 and len(chunks) > 1:
            overlapped = [chunks[0]]
            for i in range(1, len(chunks)):
                prev_tail = chunks[i - 1][-self.chunk_overlap:]
                # Find a clean word boundary for the overlap
                space_idx = prev_tail.find(" ")
                if space_idx > 0:
                    prev_tail = prev_tail[space_idx + 1:]
                overlapped.append(prev_tail + " " + chunks[i])
            chunks = overlapped

        return [c.strip() for c in chunks if len(c.strip()) >= self.min_chunk_size]

    def _recursive_split(self, text: str, sep_idx: int) -> List[str]:
        """Recursively split text using progressively finer separators."""
        if len(text) <= self.chunk_size:
            return [text]

        if sep_idx >= len(self._separators):
            # Hard split at chunk_size as last resort
            return [text[i:i + self.chunk_size]
                    for i in range(0, len(text), self.chunk_size)]

        separator = self._separators[sep_idx]

        # Use regex split for sentence boundaries
        if separator.startswith(r"(?"):
            parts = re.split(separator, text)
        else:
            parts = text.split(separator)

        # Merge small parts into chunks
        chunks = []
        current = ""
        for part in parts:
            candidate = (current + separator + part) if current else part
            if len(candidate) <= self.chunk_size:
                current = candidate
            else:
                if current:
                    chunks.append(current)
                # If a single part is too large, split it with the next separator
                if len(part) > self.chunk_size:
                    sub_chunks = self._recursive_split(part, sep_idx + 1)
                    chunks.extend(sub_chunks)
                    current = ""
                else:
                    current = part

        if current:
            chunks.append(current)

        return chunks


# ────────────────────────────────────────────────────────────
# File Loaders
# ────────────────────────────────────────────────────────────
def _extract_text_from_pdf(filepath: str) -> str:
    """Extract text from a PDF file."""
    try:
        import pypdf
        reader = pypdf.PdfReader(filepath)
        pages = []
        for page_idx, page in enumerate(reader.pages):
            text = page.extract_text() or ""
            if text.strip():
                pages.append(f"[Page {page_idx + 1}]\n{text}")
        return "\n\n".join(pages)
    except Exception as e:
        logger.warning(f"Failed to extract PDF text from {filepath}: {e}")
        return ""


def _extract_text_from_file(filepath: str) -> str:
    """Extract text from a file based on its extension."""
    ext = os.path.splitext(filepath)[1].lower()
    if ext == ".pdf":
        return _extract_text_from_pdf(filepath)
    elif ext in (".txt", ".md", ".csv", ".rst"):
        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()
        except Exception as e:
            logger.warning(f"Failed to read {filepath}: {e}")
            return ""
    else:
        logger.debug(f"Unsupported file type: {ext}")
        return ""


def _content_hash(text: str) -> str:
    """Generate a short hash for deduplication."""
    return hashlib.md5(text.encode("utf-8")).hexdigest()[:12]


# ────────────────────────────────────────────────────────────
# Public API
# ────────────────────────────────────────────────────────────
_splitter = RecursiveSemanticSplitter(chunk_size=800, chunk_overlap=150, min_chunk_size=80)


def load_documents_from_directory(
    directory: str,
    extensions: Optional[List[str]] = None,
) -> List[Dict[str, Any]]:
    """
    Scan a directory for documents, extract text, intelligently chunk,
    and auto-tag with crop/condition/category metadata.

    Args:
        directory: Path to scan for documents.
        extensions: File extensions to include (default: pdf, txt, md).

    Returns:
        List of document chunks ready for vector store ingestion.
    """
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
        logger.info(f"Created document directory: {directory}")
        return []

    if extensions is None:
        extensions = [".pdf", ".txt", ".md"]

    # Gather all matching files
    all_files: List[str] = []
    for ext in extensions:
        pattern = os.path.join(directory, f"**/*{ext}")
        all_files.extend(glob.glob(pattern, recursive=True))
        # Also check non-recursive
        pattern_flat = os.path.join(directory, f"*{ext}")
        all_files.extend(glob.glob(pattern_flat))

    all_files = list(set(all_files))  # Deduplicate paths
    if not all_files:
        logger.info(f"No documents found in {directory}.")
        return []

    chunks: List[Dict[str, Any]] = []
    seen_hashes: set = set()

    for filepath in sorted(all_files):
        filename = os.path.basename(filepath)
        full_text = _extract_text_from_file(filepath)
        if not full_text or len(full_text.strip()) < 50:
            continue

        # Split into semantic chunks
        text_chunks = _splitter.split_text(full_text)

        for chunk_idx, chunk_content in enumerate(text_chunks):
            # Deduplication
            h = _content_hash(chunk_content)
            if h in seen_hashes:
                continue
            seen_hashes.add(h)

            # Auto-detect metadata
            crop = _detect_crop(chunk_content)
            condition = _detect_condition(chunk_content)
            category = _detect_category(chunk_content)

            chunks.append({
                "id": f"{filename}_{chunk_idx}_{h}",
                "title": f"{filename} (Section {chunk_idx + 1})",
                "content": chunk_content.strip(),
                "source": f"Document: {filename}",
                "crop": crop,
                "condition": condition,
                "category": category,
            })

    logger.info(
        f"Loaded {len(chunks)} chunks from {len(all_files)} files in '{directory}'."
    )
    return chunks


# Backward-compatible alias
def load_pdfs_from_directory(directory: str) -> List[Dict[str, Any]]:
    """Legacy alias for load_documents_from_directory (PDF only)."""
    return load_documents_from_directory(directory, extensions=[".pdf"])
