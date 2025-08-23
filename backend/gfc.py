import requests

def fact_check_claim(claim_text):
    api_key = "GOOGLE_API_KEY"  # Replace with your Google Fact Check API key
    url = f"https://factchecktools.googleapis.com/v1alpha1/claims:search?key={api_key}"
    params = {
        "query": claim_text
    }
    response = requests.get(url, params=params)
    sentence = ""
    if response.status_code == 200:
        data = response.json()
        # Extract relevant information from the response
        if "claims" in data:
            for claim in data["claims"]:
                sentence += claim["claimReview"][0]["publisher"]["site"] + " answered this claim as \"" + claim["claimReview"][0]["textualRating"] + "\". "
    else:
        print("Failed to fetch data:", response.status_code)
        print(response.json())
    print("this is sentence: ", sentence)
    return sentence
