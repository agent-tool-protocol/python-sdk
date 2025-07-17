import os
from dotenv import load_dotenv
from atp_sdk.clients import ToolKitClient
from tavily import TavilyClient


load_dotenv()  # 🔥 Load variables from .env file

# Init ToolKitClient
client = ToolKitClient(
    api_key="",   # Replace with your real ToolKit API key
    app_name=""
)

# Tool 1: Search
@client.register_tool(
    function_name="tavily_search",
    params=["query", "max_results", "topic"],
    required_params=["query"],
    description="Search the web using Tavily. Optional: max_results, topic.",
    auth_provider="tavily",
    auth_type="api_key",
    auth_with="api_key"
)
def tavily_search(**kwargs):
    try:
        client = TavilyClient(api_key=kwargs.get("auth_token"))
        return client.search(
            query=kwargs["query"],
            max_results=int(kwargs.get("max_results", 3)),
            topic=kwargs.get("topic", "general"),
            search_depth="basic",
            include_answer=False,
            include_raw_content=False,
            include_images=False
        )
    except Exception as e:
        return {"error": str(e)}

# Tool 2: Crawl
@client.register_tool(
    function_name="tavily_crawl",
    params=["url", "urls", "max_depth", "max_breadth", "limit", "instructions"],
    required_params=[],
    description="Crawl one or more websites using Tavily's Crawl API. Provide 'url' for a single site or 'urls' as a list.",
    auth_provider="tavily",
    auth_type="api_key",
    auth_with="api_key"
)
def tavily_crawl(**kwargs):
    """
    Crawl one or more websites using Tavily's Crawl API.

    Args:
        url (str, optional): Single URL to crawl.
        urls (list, optional): List of URLs to crawl.
        max_depth (int, optional): Maximum crawl depth.
        max_breadth (int, optional): Maximum crawl breadth.
        limit (int, optional): Maximum number of pages to crawl.
        instructions (str, optional): Additional crawl instructions.

    Returns:
        dict: Crawl results for each URL.
    """
    try:
        client = TavilyClient(api_key=kwargs.get("auth_token"))
        results = []
        urls = kwargs.get("urls")
        if urls:
            for url in urls:
                result = client.crawl(
                    url=url,
                    max_depth=int(kwargs.get("max_depth", 1)),
                    max_breadth=int(kwargs.get("max_breadth", 20)),
                    limit=int(kwargs.get("limit", 50)),
                    instructions=kwargs.get("instructions"),
                    extract_depth="basic",
                    format="markdown"
                )
                results.append({"url": url, "result": result})
            return results
        elif "url" in kwargs:
            return client.crawl(
                url=kwargs["url"],
                max_depth=int(kwargs.get("max_depth", 1)),
                max_breadth=int(kwargs.get("max_breadth", 20)),
                limit=int(kwargs.get("limit", 50)),
                instructions=kwargs.get("instructions"),
                extract_depth="basic",
                format="markdown"
            )
        else:
            return {"error": "No url or urls provided."}
    except Exception as e:
        return {"error": str(e)}

# Tool 3: Map
@client.register_tool(
    function_name="tavily_map",
    params=["url", "max_depth", "max_breadth", "limit", "instructions"],
    required_params=["url"],
    description="Map a website's structure using Tavily's Map API.",
    auth_provider="tavily",
    auth_type="api_key",
    auth_with="api_key"
)
def tavily_map(**kwargs):
    try:
        client = TavilyClient(api_key=kwargs.get("auth_token"))
        return client.map(
            url=kwargs["url"],
            max_depth=int(kwargs.get("max_depth", 2)),
            max_breadth=int(kwargs.get("max_breadth", 20)),
            limit=int(kwargs.get("limit", 50)),
            instructions=kwargs.get("instructions")
        )
    except Exception as e:
        return {"error": str(e)}

# Start ToolKit
client.start()
