"""Policy Q&A MCP tools."""

import logging
from typing import Optional

import chromadb

from src.rag.vectorstore import get_collection, index_policies

logger = logging.getLogger(__name__)

TOP_K = 3


def search_policies(
    query: str, collection: Optional[chromadb.Collection] = None
) -> dict:
    """Search HR policies for relevant information.

    Args:
        query: Natural language question about HR policies.
        collection: Optional ChromaDB collection for testing.

    Returns:
        MCP response dict with matching policy chunks and citations.
    """
    try:
        if collection is None:
            collection = get_collection()
            index_policies(collection)

        results = collection.query(
            query_texts=[query],
            n_results=min(TOP_K, collection.count()),
        )

        formatted = []
        for i, doc in enumerate(results["documents"][0]):
            metadata = results["metadatas"][0][i]
            formatted.append({
                "text": doc,
                "source": f"{metadata['source']}, {metadata['section']}",
            })

        return {
            "success": True,
            "data": {
                "query": query,
                "results": formatted,
            },
        }
    except Exception:
        logger.exception("Unexpected error in search_policies")
        return {"success": False, "error": "Internal error", "code": "INTERNAL"}
