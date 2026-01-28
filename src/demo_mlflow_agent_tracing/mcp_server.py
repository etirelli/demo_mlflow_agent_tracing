from fastmcp import FastMCP

from demo_mlflow_agent_tracing.db import get_db

mcp = FastMCP("Knowledge Base")


@mcp.tool
def search(query: str):
    """
    Search the knowledge base using semantic search.

    Args:
        query (str): A natural language query to search the knowledge base.

    """
    try:
        db = get_db()
        documents = db.search(query=query, search_type="similarity")
        return {
            "result": "success",
            "documents": documents,
        }

    except Exception as e:
        return {
            "result": "error",
            "message": f"Search failed with error: {str(e)}",
        }


if __name__ == "__main__":
    mcp.run(show_banner=False)
