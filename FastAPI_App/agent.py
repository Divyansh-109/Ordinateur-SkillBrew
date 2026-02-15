import requests
import os

SYSTEM_PROMPT = """
** You are a 'Search-First' recomendation agent for Food and Dishes (Eated in India) **.
Your Goal is to find the most delicious and trending dishes and foods for the user based on their mood and interests.

Process:
1. Identify the user's mood or request.
2. Determine if you need fresh data (e.g., "what's trending now?" or "what's popular in India?").
3. if you need data, output only a SEARCH_QUERY in the format: "SEARCH_QUERY: <query>".
4. once you have search results, provide 3 recomendations in JSON format:

"title": "Name of the dish or food",
"type": "food",
"platform": "Where to find or prepare it",
"reason": "A brief reason for the recommendation",
"rating": "A rating out of 10 based on popularity and user reviews",
"link": "A direct link to the dish or food on the recommended platform and to order them (e.g., Zomato, Swiggy etc.)",
"rating_link": "A direct link to the rating source (e.g., Yelp, Allrecipes, etc.)"
"""

GROQ_BASE_URL = "https://api.groq.com/openai/v1"
GROQ_API_KEY = os.getenv("GROK_API_KEY")

class SearchFirstAgent:
    def __init__(self):
        self.llm_url = f"{GROQ_BASE_URL}/chat/completions"
        self.llm_key = GROQ_API_KEY
        self.search_key = os.getenv("SERPER_API_KEY")
        self.search_url = "https://google.serper.dev/search"

    def converToJSON(self, text):
        try:
            print("LLM Response:", text) 
            json_data = text.strip()
            if json_data.startswith("```json"):
                json_data = json_data[len("```json"):].strip()
            if json_data.endswith("```"):
                json_data = json_data[:-len("```")].strip()
            return eval(json_data)
        except Exception as e:
            print("Error parsing JSON:", e)
            return None
    def call_llm(self, messages: list):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.llm_key}"
        }
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": messages,
            "response_format": {
                "type": "json_object"
            }
        }
        response = requests.post(self.llm_url, json=payload, headers=headers)
        return response.json()["choices"][0]["message"]["content"]
    
    def web_search(self, query: str):
        headers = {
            "X-API-KEY": self.search_key,
            "Content-Type": "application/json"
        }
        payload = {
            "q": query,
        }
        response = requests.post(self.search_url, json=payload, headers=headers)
        print(f"Web Search Query: {query}")
        print(f"Web search status code: {response.status_code}")
        print(f"Web Search Response: {response.text}")
        result = response.json().get("organic", [])
        print(f"Web Search Result: {result}")
        return result
    
    def run(self, user_input: str):
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ]
        llm_response = self.call_llm(messages)
        
        if "SEARCH_QUERY:" in llm_response:
            search_query = llm_response.split("SEARCH_QUERY:")[1].strip().replace('"', '')

            search_results = self.web_search(search_query)

            messages.append({"role": "assistant", "content": llm_response})
            messages.append({"role": "user", "content": f"Here are the search results: {search_results}. Based on these, provide 3 food recommendations in the specified JSON format."})
            
            final_response = self.call_llm(messages)
            return self.converToJSON(final_response)
        return self.converToJSON(llm_response)