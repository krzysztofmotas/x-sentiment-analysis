# Example used: https://github.com/xdevplatform/Twitter-API-v2-sample-code/blob/main/Recent-Search/recent_search.py

import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
BEARER_TOKEN = os.getenv("BEARER_TOKEN")

search_url = "https://api.twitter.com/2/tweets/search/recent"

# Optional parameters: start_time,end_time,since_id,until_id,max_results,next_token,
# expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields
query_params = {
    'query': (
        '(#RealMadrid OR "Real Madrid") '
        '(transfer OR transfers OR sign OR signing OR signed OR deal OR bid OR '
        'rumor OR rumours OR target OR "Huijsen" OR "Trent Alexander-Arnold" OR "Carreras") '
        'lang:en -is:retweet'
    ),
    'max_results': '100',
    'tweet.fields': 'created_at,text,lang,author_id'
}

# Adds authorization headers (Bearer Token and User-Agent) to the HTTP request
def bearer_oauth(r):
    r.headers["Authorization"] = f"Bearer {BEARER_TOKEN}"
    r.headers["User-Agent"] = "x-sentiment-analysis"
    return r

# Connects to the X API endpoint and returns the response in JSON format
def connect_to_endpoint(url, params):
    response = requests.get(url, auth=bearer_oauth, params=params)
    if response.status_code != 200:
        raise Exception(f"Error: {response.status_code} {response.text}")
    return response.json()

def main():
    json_response = connect_to_endpoint(search_url, query_params)
    print(json_response)

    filename = "tweets.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(json_response, f, ensure_ascii=False, indent=4)

    print(f"Data saved to file: {filename}")

if __name__ == "__main__":
    main()
