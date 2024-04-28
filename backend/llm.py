import os
from langchain_fireworks import Fireworks
from langchain.tools import DuckDuckGoSearchRun
from langchain.agents import Tool
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain.agents import initialize_agent


os.environ["FIREWORKS_API_KEY"] = "1yR1x6rnM2AfusPPmHLHGrw40xMujZZbVGj5vzGzGyx1VHAj"
os.environ["SERPER_API_KEY"] = "71dec5a8911e77cf4b02622b06f25e2d3661f1f9"




def get_response(text):
    
    llm = Fireworks(
        model="accounts/fireworks/models/llama-v3-70b-instruct",
        max_tokens=256)




    ddg_search = DuckDuckGoSearchRun()
    google_search = GoogleSerperAPIWrapper()

    tools = [
    Tool(
        name="DuckDuckGo Search",
        func=ddg_search.run,
        description="Useful to browse information from the Internet.",
    ),
        Tool(
        name="Google Search",
        func=google_search.run,
        description="Useful to search in Google. Use by default.",
    )
    ]

    agent = initialize_agent(
    tools, llm, agent="zero-shot-react-description", verbose=True
    )

    prompt = f"Here is a statement: {text}. Make a list of assumptions you made when given the above statement and classify it as true or fake news."
    x = agent.invoke(prompt)
    print(x)

    return x['output']