from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os
from dotenv import load_dotenv
load_dotenv()

tavily=TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


@tool
def web_search(query:str):
    """Search the web for recent and reliable information on a topic. Return Titles, URLs and snippets"""
    results=tavily.search(query=query,max_results=5)

    web_output=[]

    for res in results['results']:
        web_output.append(
            f"Title: {res['title']}\nURL: {res['url']}\nSnippet: {res['content'][:300]}\n" 
        )
    return "\n----\n".join(web_output)


@tool
def scrape_url_bs(url : str) -> str:
    """ Scrape and return clean text content from a given URL for deeper reading."""
    try:
        res = requests.get(url, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(res.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()
        return soup.get_text(separator=" ", strip=True)[:3000]
    except Exception as e:
        return f"Could not scrape URL: {str(e)}"
    