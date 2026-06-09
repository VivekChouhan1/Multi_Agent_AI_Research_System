from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search, scrape_url_bs
from dotenv import load_dotenv
load_dotenv()
import os

MISTRAL_API_KEY = os.environ.get("MISTRAL_API_KEY")
GOOGLE_API_KEY  = os.environ.get("GOOGLE_API_KEY")


# Model Setup
llm_gemini = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", temperature=0)
llm_mistral = ChatMistralAI(model="mistral-small-2506", temperature=0)



# 1-st agent
def build_search_agent():
    return create_agent(
        model=llm_mistral,
        tools=[web_search]
    )



# 2-nd agent
def build_reader_agent():
    return create_agent(
        model=llm_mistral,
        tools=[scrape_url_bs]
    )



# Writter Chain
writer_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a senior research analyst and professional report writer with expertise across multiple domains.

    Your writing is:
    - Factual, precise, and evidence-based
    - Well-structured with smooth transitions between sections
    - Free of filler phrases like "it is important to note" or "in conclusion, we can see"
    - Rich with specific data points, statistics, and named examples when available
    - Written in an active, authoritative voice

    Never hallucinate facts. If the research is insufficient for a section, say so explicitly."""),

        ("human", """Write a comprehensive research report on the topic below using ONLY the provided research.

    ━━━━━━━━━━━━━━━━━━━━━━
    TOPIC: {topic}
    ━━━━━━━━━━━━━━━━━━━━━━

    RESEARCH INPUT:
    {research}

    ━━━━━━━━━━━━━━━━━━━━━━
    REPORT STRUCTURE (follow strictly):
    ━━━━━━━━━━━━━━━━━━━━━━

    ## Executive Summary
    2–3 sentence overview of the entire report. What is the topic, why does it matter, and what is the key takeaway?

    ## Introduction
    - Background and context of the topic
    - Why this topic is relevant right now
    - Scope of this report (what it covers and what it doesn't)

    ## Key Findings
    Present a minimum of 4 distinct, well-explained findings. For each finding:
    - Use a descriptive subheading (not just "Finding 1")
    - Explain the finding in depth (3–5 sentences minimum)
    - Include supporting data, statistics, or examples from the research
    - Explain the implication or significance of this finding

    ## Analysis & Insights
    - Identify patterns or connections across the findings
    - Highlight any contradictions or gaps in the current research
    - Provide context: how do these findings compare to prior knowledge or expectations?

    ## Conclusion
    - Summarize the core message of the report in 3–5 sentences
    - Avoid repeating bullet points from Key Findings — synthesize them
    - End with a forward-looking statement or open question

    ## Recommendations *(if applicable)*
    - Actionable steps for practitioners, policymakers, or researchers based on the findings
    - Keep each recommendation specific and grounded in the research

    ## Sources
    - List every URL found in the research, one per line
    - Format: [Source Title or Domain] — URL
    - Do not fabricate sources

    ━━━━━━━━━━━━━━━━━━━━━━
    QUALITY CHECKLIST (self-verify before outputting):
    □ No fabricated facts beyond what the research provides
    □ Every Key Finding has a subheading and supporting evidence
    □ Sources section lists all URLs from the research
    □ Report flows logically from section to section
    □ Language is professional, specific, and avoids vague generalizations
    ━━━━━━━━━━━━━━━━━━━━━━
    """),
])

writer_Chain= writer_prompt | llm_mistral | StrOutputParser()



# Critic Chain
critic_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a senior peer reviewer and research quality evaluator with decades of experience 
    reviewing academic papers, industry reports, and investigative journalism.

    Your reviews are:
    - Brutally honest but always constructive — you critique the work, not the author
    - Specific: you always cite exact sections, sentences, or claims when pointing out issues
    - Balanced: you acknowledge genuine strengths before dissecting weaknesses
    - Actionable: every criticism comes with a clear suggestion for improvement

    You evaluate reports on FIVE dimensions:
    1. ACCURACY      — Are claims factual, grounded, and properly sourced?
    2. DEPTH         — Does the report go beyond surface-level observations?
    3. STRUCTURE     — Is the report logically organized with smooth flow?
    4. CLARITY       — Is the language precise, concise, and jargon-free?
    5. USEFULNESS    — Does the report deliver real insight or actionable value?

    Never give inflated scores. A 9–10 is reserved for near-perfect work.
    A 5 means mediocre — average is NOT good."""),

        ("human", """Conduct a rigorous peer review of the research report below.

    ━━━━━━━━━━━━━━━━━━━━━━
    REPORT TO REVIEW:
    ━━━━━━━━━━━━━━━━━━━━━━
    {report}
    ━━━━━━━━━━━━━━━━━━━━━━

    Respond in EXACTLY this format — do not skip or rename any section:

    ## Dimension Scores
    | Dimension   | Score (1–10) | One-line Reason                         |
    |-------------|-------------|------------------------------------------|
    | Accuracy    | X/10        | ...                                      |
    | Depth       | X/10        | ...                                      |
    | Structure   | X/10        | ...                                      |
    | Clarity     | X/10        | ...                                      |
    | Usefulness  | X/10        | ...                                      |

    ## Overall Score: X/10
    *(Weighted average — penalize heavily for factual issues or missing sources)*

    ---

    ## Strengths  
    *(Minimum 3 — be specific, cite the exact part of the report you're praising)*
    - **[Strength label]:** ...
    - **[Strength label]:** ...
    - **[Strength label]:** ...

    ---

    ## Critical Issues  
    *(Minimum 3 — cite exact section/claim, explain the problem, then give a fix)*
    - **[Issue label] → Section: "..."]**  
    Problem: ...  
    Fix: ...

    - **[Issue label] → Section: "..."]**  
    Problem: ...  
    Fix: ...

    - **[Issue label] → Section: "..."]**  
    Problem: ...  
    Fix: ...

    ---

    ## Quick Wins  
    *(2–3 small, fast improvements that would immediately raise the score)*
    - ...
    - ...

    ---

    ## Verdict  
    **One sentence:** ...  
    **Should this report be revised or published as-is?** Revised / Conditionally Accepted / Accepted  
    **Priority fix before next revision:** ...

    ━━━━━━━━━━━━━━━━━━━━━━
    REVIEWER SELF-CHECK (verify before outputting):
    □ Every Critical Issue cites a specific section or claim
    □ Every weakness has an actionable Fix
    □ Scores reflect genuine quality — no grade inflation
    □ Verdict is decisive, not vague
    ━━━━━━━━━━━━━━━━━━━━━━
    """),
])

critic_chain = critic_prompt | llm_mistral | StrOutputParser()