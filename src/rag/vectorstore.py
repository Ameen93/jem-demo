"""ChromaDB vectorstore for policy RAG."""

import logging
import re
from pathlib import Path
from typing import Optional

import chromadb

logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).parent.parent.parent / "data"
POLICY_DIR = DATA_DIR / "policies"
DEFAULT_PERSIST_DIR = str(DATA_DIR / "chroma")
COLLECTION_NAME = "hr_policies"


def get_collection(
    persist_dir: Optional[str] = None,
) -> chromadb.Collection:
    """Get or create the ChromaDB collection.

    Args:
        persist_dir: Directory for ChromaDB persistence. Defaults to data/chroma/.

    Returns:
        ChromaDB Collection instance.
    """
    if persist_dir is None:
        persist_dir = DEFAULT_PERSIST_DIR

    client = chromadb.PersistentClient(path=persist_dir)
    collection = client.get_or_create_collection(name=COLLECTION_NAME)
    logger.info("ChromaDB collection '%s' ready (%d docs)", COLLECTION_NAME, collection.count())
    return collection


def _split_by_sections(content: str, source: str) -> list[dict]:
    """Split markdown content into sections by ## headers.

    Args:
        content: Markdown text.
        source: Source filename.

    Returns:
        List of dicts with keys: text, source, section.
    """
    chunks = []
    sections = re.split(r"(?=^## )", content, flags=re.MULTILINE)

    for section in sections:
        section = section.strip()
        if not section:
            continue

        # Extract section name from header
        lines = section.split("\n", 1)
        header = lines[0].lstrip("#").strip()
        text = section

        chunks.append({
            "text": text,
            "source": source,
            "section": header,
        })

    return chunks


def index_policies(collection: chromadb.Collection) -> None:
    """Index policy documents into ChromaDB.

    Idempotent: skips if documents already indexed.

    Args:
        collection: ChromaDB collection to index into.
    """
    if collection.count() > 0:
        logger.info("Policies already indexed (%d docs). Skipping.", collection.count())
        return

    logger.info("Indexing policy documents...")

    all_chunks = []
    for policy_file in sorted(POLICY_DIR.glob("*.md")):
        content = policy_file.read_text()
        chunks = _split_by_sections(content, policy_file.name)
        all_chunks.extend(chunks)

    if not all_chunks:
        logger.warning("No policy documents found in %s", POLICY_DIR)
        return

    collection.add(
        ids=[f"policy-{i}" for i in range(len(all_chunks))],
        documents=[c["text"] for c in all_chunks],
        metadatas=[{"source": c["source"], "section": c["section"]} for c in all_chunks],
    )

    logger.info("Indexed %d policy chunks", len(all_chunks))
