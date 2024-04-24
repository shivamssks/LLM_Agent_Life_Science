from langchain_community.utilities import SerpAPIWrapper
from langchain.tools import BaseTool
import os
os.environ["SERPAPI_API_KEY"] = ""


def web_search(keyword,search_engine = "google"):
    """
    Perform a web search using the specified search engine.

    Args:
        keyword (str): The keyword to search for.
        search_engine (str, optional): The search engine to use. Defaults to "google".

    Returns:
        str: The search results returned by the search engine.
    """
    try:
        search_progress = SerpAPIWrapper(search_engine=search_engine)
        result = search_progress.run(keyword)
        return result
    except Exception as e:
        # print(e)
        return "No results found"


class websearch(BaseTool):
    """Search for keywords in the web."""

    name = "websearch"
    description = """Useful for when you need to answer questions about current events.
    Input should be a search query.
    """
    def _run(self,query):
        return web_search(query)

if __name__ == "__main__":
    print(web_search("What is the capital of India?"))

