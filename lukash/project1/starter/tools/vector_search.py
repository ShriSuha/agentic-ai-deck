from pathlib import Path
from typing import Any

from chromadb import PersistentClient
from crewai.tools import BaseTool


class VectorSearchTool(BaseTool):
    name: str = "vector_search"
    description: str = "Find model-card text semantically related to a natural-language query using vector search."
    client: Any = None

    def __init__(self):
        super().__init__()
        self.client = PersistentClient(path=Path(__file__).parent.parent.parent / "assets" / "chromadb")

    def _run(self, query: str) -> str:
        collection = self.client.get_or_create_collection("model_descriptions")
        result = collection.query(query_texts=[query])
        metadatas = result["metadatas"][0]
        documents = result["documents"][0]
        return "\n\n".join(
            f"# {meta['document_id']} ({meta['block_id']}):\n\n{document}"
            for meta, document in zip(metadatas, documents)
        ) or "No matching model cards found."
