from agents import build_reader_agent,build_search_agent,writer_Chain,critic_chain
from rich import print


def run_research_pipeline(topic : str) -> dict:
    
    state={}

    # step -1: search agent working
    print("\n"+" ="*50)
    print("Step 1 - search agent is working ...")
    print("="*50)


    search_agent=build_search_agent()
    search_result=search_agent.invoke({
        "messages" : [("user", f"Find recent, reliable and detailed information about: {topic}")]
    })

    state["search_result"]=search_result['messages'][-1].content

    print("\n search result \n",state["search_result"])


    #step -2: Reader agent working
    print("\n"+" ="*50)
    print("Step 2 - Reader agent is scraping top resources ...")
    print("="*50)

    reader_agent=build_reader_agent()
    reader_result=reader_agent.invoke({
        "messages": [( "user",
                      f"Based on the following search results about '{topic}', "
                      f"pick the most relevant URLs and scrape their content for deeper insights."
                      f"Search Results:\n{state['search_result'][:800]}"
        )] 
    })
    state['Scraped_content']=reader_result['messages'][-1].content

    print(" \n Scraped content \n",state["Scraped_content"])


    # step 3 - writer chain
    print("\n"+" ="*50)
    print("Step 3 - writer chain is drafting the report ...")
    print("="*50)

    research_combined=(
        f"SEARCH RESULTS : \n {state['search_result']} \n\n"
        f"DETAILED SCRAPED CONTENT : \n {state['Scraped_content']} \n\n"
    )

    state['Report']=writer_Chain.invoke({
        "topic" :topic,
        "research": research_combined
    })

    print("\n Final Report\n", state["Report"])


    # step 4 : critic report
    print("\n"+" ="*50)
    print("Step 4 - Critic chian is reviewing the report ...")
    print("="*50)

    state['Feedback']=critic_chain.invoke({
        "report":state["Report"]
    })

    print("\n Critic Report \n", state['Feedback'])

    return state


if __name__ == "__main__":
    topic=input("\n Enter research topic : ")
    run_research_pipeline(topic)


