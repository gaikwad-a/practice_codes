import requests
from typing import List, Dict, Union

class NewsClient:
    

    def __init__(self, api_key: str, base_url: str = "https://newsapi.org/v2/top-headlines"):
       
        self.api_key = api_key
        self.base_url = base_url

    def get_headlines_by_keyword(self, keyword: str, country: str = 'us') -> Union[List[Dict], Dict]:
       
        params = {
            'q': keyword,
            'country': country,
            'apiKey': self.api_key,
        }

        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            print(data)

            if data.get('status') != 'ok':
                return {"error": "Unexpected response format."}

            return data.get('articles', [])
        
        except requests.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}


if __name__ == "__main__":
    API_KEY = "63c91e2383be43919b01745d8b68a289" 
    client = NewsClient(api_key=API_KEY)
    
    
    articles = client.get_headlines_by_keyword("stocks")

    if isinstance(articles, list):
        for i, article in enumerate(articles[:5], start=1):
            print(f"{i}. {article['title']} - {article['source']['name']}")
    else:
        print(articles) 