import getpass
import os
from dotenv import load_dotenv

load_dotenv()
if not os.environ.get("TAVILY_API_KEY"):
    os.environ["TAVILY_API_KEY"] = getpass.getpass("Tavily API key:\n")

from langchain_tavily import TavilySearch

search = TavilySearch(max_results=2)