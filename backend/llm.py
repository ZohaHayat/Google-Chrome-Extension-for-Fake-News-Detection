import os
from langchain_fireworks import Fireworks
from langchain.tools import DuckDuckGoSearchRun
from langchain.agents import Tool
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain.agents import initialize_agent
from gfc import fact_check_claim
import re

os.environ["FIREWORKS_API_KEY"] = "ylT5fkGfTQpTSnoq57gQOYtmgYcUsLHrxunYpPBUk5aTAqGE"
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

    fact = fact_check_claim(text)
    prompt = f"Here is a news statement: {text}. Classify the news statement as one of the following: True News (the assigned rating should be 1.), Uncertain News (the assigned rating should be 2.), or False News (the assigned rating should be 3.). Provide factual explanations to prove your claim. Only assign the relevant rating to a particular classification. If the news is fake, further classify it as misinformation, propaganda or misleading. Here is some supplementary information about the statement: {fact}. The format for assigning rating should be the following: Rating: <rating_value>. The answer sequence should be: Classification, Explanation."

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
    
    rating = None
    while rating == None:
        x = agent.invoke(prompt)
        print(x)
        
        cleaned_data = remove_after(x['output'], '<|eot_id|>')
        cleaned_data = clean_text(cleaned_data)
        
        prompt2 = f"Only extract and return the rating number given to the text: {x}. Just give me the number as an answer and don't write an entire sentence."
        
        rating = clean_text(remove_after((agent.invoke(prompt2))['output'], '<|eot_id|>'))
        rating = extract_rating(rating)
        # while (rating==None):
        #     rating = clean_text(remove_after((agent.invoke(prompt2))['output'], '<|eot_id|>'))
        
        cleaned_data = re.sub(r"Rating: \d+\.", "", cleaned_data)
    

    
    # rating = extract_rating(rating)
        
    print(cleaned_data + "." + str(rating) + ".")
    return cleaned_data + "." + str(rating) + "."