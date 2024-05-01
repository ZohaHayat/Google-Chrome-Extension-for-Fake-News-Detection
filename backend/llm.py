# import os
# from langchain_fireworks import Fireworks
# from langchain.tools import DuckDuckGoSearchRun
# from langchain.agents import Tool
# from langchain_community.utilities import GoogleSerperAPIWrapper
# from langchain.agents import initialize_agent
# from gfc import fact_check_claim
# import re

# os.environ["FIREWORKS_API_KEY"] = "1yR1x6rnM2AfusPPmHLHGrw40xMujZZbVGj5vzGzGyx1VHAj"
# os.environ["SERPER_API_KEY"] = "71dec5a8911e77cf4b02622b06f25e2d3661f1f9"

# def get_response(text):
    
#     llm = Fireworks(
#         model="accounts/fireworks/models/llama-v3-70b-instruct",
#         max_tokens=256)

#     ddg_search = DuckDuckGoSearchRun()
#     google_search = GoogleSerperAPIWrapper()

#     tools = [
#     Tool(
#         name="DuckDuckGo Search",
#         func=ddg_search.run,
#         description="Useful to browse information from the Internet.",
#     ),
#         Tool(
#         name="Google Search",
#         func=google_search.run,
#         description="Useful to search in Google. Use by default.",
#     )
#     ]

#     agent = initialize_agent(
#     tools, llm, agent="zero-shot-react-description", verbose=True
#     )

#     # prompt = f"Here is a statement: {text}. Make a list of assumptions you made when given the above statement and classify it as true or fake news."
#     fact = fact_check_claim(text)
#     print("fact ", fact)
#     if fact != "":
#         prompt = f"Here is a statement: {text}. We asked Google Fact Check API to verify our claim. Here's what it said: {fact}. Make a list of assumptions you made when given the above statement and classify it as true or fake news. If the news is fake, further classify it as misinformation, propaganda or misleading content as done by Google Fact Check API. Also you must assign a numerical rating to the claim on a scale of 0 to 5 where 0 means completely true and 5 means completely false. The format for assigning rating should be the following: \"Rating: <rating_value>\"."
#         #prompt2 = f"Extract and return the integer rating from the following text: {prompt} "
#         #prompt2 = f"Here is a piece of text: {prompt} Extract the rating being assigned and give it as your response. Note: you must only return the rating as your reponse and no other character value."
#     else:
#         #prompt = f"Here is a statement: {text}. Make a list of assumptions you made when given the above statement and classify it as true or fake news. If the news is fake, further classify it as misinformation, propaganda or misleading content as done by Google Fact Check API. Also assign a numerical rating to the claim on a scale of 1 to 5 where 1 means completely true and 5 means completely false. The format for assigning rating should be the following: \"Rating: <rating_value>\"'
#         prompt = prompt = f"Here is a statement: {text}. Make a list of assumptions you made when given the above statement and classify it as true or fake news. If the news is fake, further classify it as misinformation, propaganda or misleading content as done by Google Fact Check API. Also assign a numerical rating to the claim on a scale of 0 to 5 where 0 means completely true and 5 means completely false. The format for assigning rating should be the following: \"Rating: <rating_value>\"."
#         #prompt2 = f"Extract and return the integer rating from the following text: {prompt} "

    
#     # removing tokens
#     def remove_after(text, delimiter):
#         return text.split(delimiter)[0].strip()

    
#     # removing special characters
#     def clean_text(text):
#         text = text.replace('\\n', ' ').replace('\\', '')
#         text = re.sub(r'\s+', ' ', text)
#         return text.strip()
    
#     x = agent.invoke(prompt)
#     print(x)
#     cleaned_data = remove_after(x['output'], '<|eot_id|>')
#     cleaned_data = clean_text(cleaned_data)
    

#     #rating = extract_rating(cleaned_data)
#     prompt2 = f"Extract and return the only integer rating (no other character) from the following text: {cleaned_data} "
    
#     rating = clean_text(remove_after((agent.invoke(prompt2))['output'], '<|eot_id|>'))
#     while (rating==None):
#         rating = clean_text(remove_after((agent.invoke(prompt2))['output'], '<|eot_id|>'))
        
        
    
#     return cleaned_data + "." + rating + "."
#     # return cleaned_data,rating
 
#     # def extract_rating(sentence):
#     # # Define the pattern to match "Rating: " followed by a single character
#     #     pattern = r'Rating:\s*(\S)'
#     #     match = re.search(pattern, sentence)
#     #     if match:
#     #         return match.group(1)
#     #     else:
#     #         return None
    







import os
from gfc import fact_check_claim
import re
import requests

os.environ["FIREWORKS_API_KEY"] = "1yR1x6rnM2AfusPPmHLHGrw40xMujZZbVGj5vzGzGyx1VHAj"
os.environ["SERPER_API_KEY"] = "71dec5a8911e77cf4b02622b06f25e2d3661f1f9"

def get_response(text):
    
    API_URL = "https://api-inference.huggingface.co/models/SeemalT/gemma2b-finetuned"
    headers = {"Authorization": "Bearer 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"}


    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()
    
    fact = fact_check_claim(text)
    if fact != "":
        prompt = f"Here is a statement: {text}. We asked Google Fact Check API to verify our claim. Here's what it said: {fact}. Make a bullet point list of assumptions you made when given the above statement and explain whether statement is true new or fake news. If the news is fake, further classify it as misinformation, propaganda or misleading content as done by Google Fact Check API. Also you must assign a numerical rating to the claim on a scale of 0 to 5 where 0 means completely true and 5 means completely false. The format for assigning rating should be the following: Rating: <rating_value>."
    else:
        prompt = f"Here is a statement: {text}. Make a list of assumptions you made when given the above statement and classify it as true or fake news. If the news is fake, further classify it as misinformation, propaganda or misleading content. Also assign a numerical rating to the claim on a scale of 0 to 5 where 0 means completely true and 5 means completely false. The format for assigning rating should be the following: Rating: <rating_value>."

    inputs = f"""<bos>
    <start_of_turn>user
    {prompt}<end_of_turn>
    <start_of_turn>model

    """

    output = query({
        "inputs": inputs,
    "parameters": {"max_new_tokens": 150, "return_full_text": False},
    })
    
    x = output[0]['generated_text']
    
    def clean_text(text):
        text = text.replace('\\n', ' ').replace('\\', '')
        text = text.replace('*', '')
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    x = clean_text(x)
    print(x)
    
    prompt2 = f"Only extract and return the rating number (this will be a number from 0 to 5) given to the text: {x}. Just give me the number as an answer and don't write an entire sentence."
    
    inputs2 = f"""<bos>
    <start_of_turn>user
    {prompt2}<end_of_turn>
    <start_of_turn>model

    """

    output2 = query({
        "inputs": inputs2,
    "parameters": {"max_new_tokens": 150, "return_full_text": False},
    })
    
    rating = output2[0]['generated_text']
    while (rating==None):
        rating = output2[0]['generated_text']
    
    rating = clean_text(rating)
    
    print(rating)
    
    return x + "." + rating + "."