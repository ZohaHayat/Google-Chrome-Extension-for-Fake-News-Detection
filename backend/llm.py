import os
from langchain_fireworks import Fireworks
from langchain.tools import DuckDuckGoSearchRun
from langchain.agents import Tool
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain.agents import initialize_agent
from gfc import fact_check_claim
from langchain.agents import AgentExecutor, create_react_agent
from langchain import hub
import re

os.environ["FIREWORKS_API_KEY"] = "FIREWORKS_API_KEY"
os.environ["SERPER_API_KEY"] = "SERPER_API_KEY"

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

    # agent = initialize_agent(
    # tools, llm, agent="zero-shot-react-description", verbose=True
    # )
    
    fact = fact_check_claim(text)
    prompt = f"Here is a news statement: {text}. Classify the news statement as one of the following: True News (the assigned rating should be 1.), Uncertain News (the assigned rating should be 2.), or False News (the assigned rating should be 3.). Provide factual explanations to prove your claim. If the news is false, further classify it as misinformation, propaganda or misleading. Only assign the relevant rating to a particular classification. Here is some supplementary information about the statement: {fact}. The format for assigning rating should be the following: Rating: <rating_value>. The answer sequence should be: Classification, Explanation."
    agent = create_react_agent(llm, tools, hub.pull("hwchase17/react"))
    agent_ex = AgentExecutor(
    agent=agent, tools=tools, verbose=True, handle_parsing_errors=True
)

    

    # removing tokens
    def remove_after(text, delimiter):
        return text.split(delimiter)[0].strip()

    def clean_text(text):
        text = text.replace('\\n', ' ').replace('\\', '')
        text = text.replace('*', '')
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def extract_rating(sentence):
        pattern = r'\d+'
        match = re.search(pattern, sentence)
        if match:
            return int(match.group())
        else:
            return None
        
    x = agent_ex.invoke({"input":prompt})
    print(x,"Model's new output")
    
    cleaned_data = remove_after(x['output'], '<|eot_id|>')
    cleaned_data = clean_text(cleaned_data)
    
    prompt2 = f"Only extract and return the rating number given to the text: {x}. Just give me the number as an answer and don't write an entire sentence."
    
    rating = clean_text(remove_after((agent_ex.invoke({"input":prompt2}))['output'], '<|eot_id|>'))
    rating = extract_rating(rating)
    while (rating==None):
        x = agent_ex.invoke({"input":prompt})
        cleaned_data = clean_text(remove_after(x['output'], '<|eot_id|>'))
        prompt2 = f"Only extract and return the rating number given to the text: {x}. Just give me the number as an answer and don't write an entire sentence."
        rating = extract_rating(clean_text(remove_after((agent_ex.invoke({"input":prompt2}))['output'], '<|eot_id|>')))
            
    print(rating)
    
    cleaned_data = re.sub(r"Rating: \d+\.", "", cleaned_data)
        
    print(cleaned_data + "." + str(rating) + ".")
    return cleaned_data + "." + str(rating) + "."
