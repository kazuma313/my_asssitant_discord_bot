from langchain_tavily import TavilySearch
from typing import List
import tiktoken
import logging


def many_search_formatted(
    search_query_list: List[str],
    include_raw_content: bool = True,
    max_search_results: int = 5,
    max_tokens: int = 1000,
    search_depth: str = "advanced",
    topic: str = "general",
    model_name: str = "gpt-4",
) -> str:
    """
    Melakukan multiple search queries dan menformat hasilnya.

    Args:
        search_query_list: List of search queries
        include_raw_content: Whether to include raw content
        max_search_results: Maximum number of results per query
        max_tokens: Maximum tokens for raw content
        search_depth: Search depth ('basic' or 'advanced')
        topic: Search topic
        model_name: Model name for token encoding

    Returns:
        Formatted search results as string
    """
    if not search_query_list:
        return "No search queries provided."

    def _format_single_search(
        search_query: str, include_raw: bool, encoding: tiktoken.Encoding
    ) -> str:
        """Helper function to format single search result."""
        try:
            logging.info("--- Searching to internet ---")
            tavily_search = TavilySearch(
                max_results=max_search_results,
                topic=topic,
                include_raw_content=include_raw,
                search_depth=search_depth,
            )
            result_search = tavily_search.invoke(search_query)

            formatted_parts = []
            for source in result_search.get("results", []):
                parts = [
                    f"Score relevancy: {source.get('score', 'none')}",
                    f"Source/Title: {source.get('title', 'Untitled')}",
                    f"URL: {source.get('url', '')}",
                    f"Most relevant content: {source.get('content', 'No content available')}",
                ]

                if include_raw and "raw_content" in source:
                    raw_content = str(source["raw_content"])
                    tokens = encoding.encode(raw_content)
                    truncated_tokens = tokens[:max_tokens]
                    truncated_content = encoding.decode(truncated_tokens)
                    parts.append(f"Full content:\n {truncated_content}")

                formatted_parts.append("\n---\n".join(parts))
                logging.info(
                    f"--- got sources from internet: {len(formatted_parts)} ---"
                )

            return "\n\n".join(formatted_parts)

        except Exception as e:
            return f"Error searching '{search_query}': {str(e)}"

    # Initialize encoding once
    try:
        encoding = tiktoken.encoding_for_model(model_name)
    except Exception:
        encoding = tiktoken.get_encoding("cl100k_base")  # Fallback

    results = ["Content from web search:\n"]
    for query in search_query_list:
        results.append(f"\n{'='*60}")
        results.append(f"Query: {query}")
        results.append("=" * 60)
        results.append(_format_single_search(query, include_raw_content, encoding))

    return "\n".join(results)
