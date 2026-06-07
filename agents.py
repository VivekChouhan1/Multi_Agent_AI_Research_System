from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search, scrape_url_bs
from dotenv import load_dotenv
load_dotenv()

# Model Setup
llm_gemini = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", temperature=0)

# 1-st agent
def build_search_agent():
    return create_agent(
        model=llm_gemini,
        tools=[web_search]
    )

# 2-nd agent
def build_reader_agent():
    return create_agent(
        model=llm_gemini,
        tools=[scrape_url_bs]
    )