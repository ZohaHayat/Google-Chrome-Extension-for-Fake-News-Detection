import os
from gfc import fact_check_claim
import re
import requests
import time
from langchain.tools import DuckDuckGoSearchRun

os.environ["FIREWORKS_API_KEY"] = "1yR1x6rnM2AfusPPmHLHGrw40xMujZZbVGj5vzGzGyx1VHAj"
os.environ["SERPER_API_KEY"] = "71dec5a8911e77cf4b02622b06f25e2d3661f1f9"

def get_response(text):
    
    API_URL = "https://api-inference.huggingface.co/models/SeemalT/gemma2b-finetuned"
    headers = {"Authorization": "Bearer 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"}

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()
    
    def get_duckduckgo_results(query):
        ddg_search = DuckDuckGoSearchRun()  # Initialize the DuckDuckGo search class
        results = ddg_search.run(query)  # Run the search with the provided query
        return results
    
    search_result = get_duckduckgo_results(text)
    combined_text = " ".join(search_result)
    
    fact = fact_check_claim(text)
    if fact != "":
        prompt = f"Here is a statement: {text}. Classify the statement as true (give it a rating of 1) or false (give it a rating of 5) and provide factual explanations to prove your claim. Here is some supplementary information: {fact} & {combined_text}. The format for assigning rating should be the following: Rating: <rating_value>."
    else:
        prompt = f"Here is a statement: {text}. Classify the statement as true (give it a rating of 1) or false (give it a rating of 5) and provide factual explanations to prove your claim. Here is some supplementary information: {combined_text}. The format for assigning rating should be the following: Rating: <rating_value>."

    inputs = f"""<bos>
    <start_of_turn>user
    {prompt}<end_of_turn>
    <start_of_turn>model
    """
    
    while True:
        output = query({
            "inputs": inputs,
        "parameters": {"max_new_tokens": 150, "return_full_text": False},
        })

        if "error" in output:
            print(output["error"])
            print("Retrying in 2 seconds...")
            time.sleep(2)  # Wait for 2 seconds before retrying
        else:
            print(output[0]['generated_text'])
            break  # Exit the loop if successful
    
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
    
    while True:
        output2 = query({
            "inputs": inputs2,
        "parameters": {"max_new_tokens": 150, "return_full_text": False},
        })

        if "error" in output2:
            print(output2["error"])
            print("Retrying in 2 seconds...")
            time.sleep(2)  # Wait for 2 seconds before retrying
        else:
            print(output2[0]['generated_text'])
            break  # Exit the loop if successful
    
    rating = output2[0]['generated_text']
    while (rating==None):
        rating = output2[0]['generated_text']
    
    def extract_rating(sentence):
        pattern = r'\d+'
        match = re.search(pattern, sentence)
        if match:
            return int(match.group())
        else:
            return None
        
    rating = extract_rating(clean_text(rating))
    
    print(rating)
    
    return x + "." + str(rating) + "."