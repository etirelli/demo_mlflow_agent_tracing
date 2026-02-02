import logging
from typing import Literal

from fastmcp import FastMCP
from langchain_core.documents import Document
from pydantic import BaseModel

from demo_mlflow_agent_tracing.db import get_db
from demo_mlflow_agent_tracing.settings import Settings

logger = logging.getLogger(__name__)

mcp = FastMCP("Knowledge Base")


class SearchResult(BaseModel):
    """Search result class."""

    result: Literal["success", "error"]
    message: str
    documents: list[Document] = []


@mcp.tool
def search(query: str, k: int = 3):
    """
    Search the knowledge base using semantic search.

    Args:
        query (str): A natural language query to search the knowledge base.
        k (int, optional): Number of search results to return. Defaults to 3.

    """
    logger.info(f"Search requested. {query=}")
    settings = Settings()
    try:
        # Get database
        db = get_db()

        # Conduct search
        if settings.EMBEDDING_SEARCH_PREFIX is not None:
            query = settings.EMBEDDING_SEARCH_PREFIX + query
        documents = db.similarity_search(query=query, k=k)
        logger.info(f"Found {len(documents)} results")

        # Return results
        return SearchResult(result="success", message=f"Found {len(documents)} results", documents=documents)

    except Exception as e:
        logger.error(e, exc_info=True)
        return SearchResult(result="error", message=f"Search failed with error: {str(e)}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")
    mcp.run(show_banner=False)
