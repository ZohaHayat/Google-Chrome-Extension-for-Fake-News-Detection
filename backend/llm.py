import os
from gfc import fact_check_claim
import re
import requests
import time
from langchain.tools import DuckDuckGoSearchRun
from langchain.utilities import GoogleSerperAPIWrapper

os.environ["FIREWORKS_API_KEY"] = "1yR1x6rnM2AfusPPmHLHGrw40xMujZZbVGj5vzGzGyx1VHAj"
os.environ["SERPER_API_KEY"] = "71dec5a8911e77cf4b02622b06f25e2d3661f1f9"

google_search = GoogleSerperAPIWrapper()

def get_response(text):
    
    API_URL = "https://api-inference.huggingface.co/models/SeemalT/gemma2b-finetuned-v2"
    headers = {"Authorization": "Bearer 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"}

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()
    
    def get_duckduckgo_results(query):
        ddg_search = DuckDuckGoSearchRun()  # Initialize the DuckDuckGo search class
        results = ddg_search.run(query)  # Run the search with the provided query
        return results
    
    def get_google_results(query):
        results = google_search.run(query)  # Get results from Google Serper API
        return results
    
    google_results = get_google_results(text)
    search_result = get_duckduckgo_results(text)
    fact = fact_check_claim(text)
    combined_text = " ".join(search_result + google_results + fact)
    
    # if fact != "":
    # prompt = f"Here is a statement: {text}. Classify the statement as true or false and provide factual explanations to prove your claim. Give it a rating according to this: 0: Completely True, 1: Mostly True, 2: Somewhat True, 3: uncertain, 4: Somewhat False, 5: Mostly False, 6: Completely False. Here is some supplementary information: {fact} & {combined_text}. The format for assigning rating should be the following: Rating: <rating_value>."
    # prompt = f"Here is a statement: {text}. Here is some supplementary information about the statement: {combined_text}. Classify the statement as one of the following: Completely True (Rating: 1.), Somewhat True (Rating: 2.), Uncertain (Rating: 3.), Somewhat False (Rating: 4.) or Completely False (Rating: 5.). Provide factual explanations to prove your claim. Only assign the relevant rating to a particular classification. The format for assigning rating should be the following: Rating: <rating_value>. The answer sequence should be: Rating, Classification, Explanation."
    prompt = f"Here is a statement: {text}. Here is some supplementary information about the statement: {combined_text}. Classify the statement as one of the following: True (the assigned rating should be 1.), Uncertain (the assigned rating should be 2.), or False (the assigned rating should be 3.). Provide factual explanations to prove your claim. Only assign the relevant rating to a particular classification. The format for assigning rating should be the following: Rating: <rating_value>. The answer sequence should be: Classification, Explanation."
    # else:
        # prompt = f"Here is a statement: {text}. Classify the statement as true or false and provide factual explanations to prove your claim. Give it a rating according to this - 0: Completely True, 1: Mostly True, 2: Somewhat True, 3: uncertain, 4: Somewhat False, 5: Mostly False, 6: Completely False. Here is some supplementary information: {combined_text}. The format for assigning rating should be the following: Rating: <rating_value>."

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
    
    prompt2 = f"Only extract and return the rating number given to the text: {x}. Just give me the number as an answer and don't write an entire sentence."
    
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
        elif output2[0]['generated_text'] == None:
            print(output2[0]['generated_text'])
            print("Retrying in 2 seconds...")
            time.sleep(2)  # Wait for 2 seconds before retrying
        elif len(output2[0]['generated_text']) > 1:
            print(output2[0]['generated_text'])
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
    
    # def replace_rating(input_str):
    #     # Replace "Rating: 9" with "Rating: 0" in the given string
    #     updated_str = input_str.replace("Rating: 9", "Rating: 0")
    #     return updated_str

    rating = extract_rating(clean_text(rating))
    
    # Replace the matching pattern with an empty string to remove it
    x = re.sub(r"Rating: \d+\.", "", x)
    
    # if rating == 9:
    #     x = replace_rating(x)
    #     rating = 0
    # print(rating)
    
    return x + "." + str(rating) + "."