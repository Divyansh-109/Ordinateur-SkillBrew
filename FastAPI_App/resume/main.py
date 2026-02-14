import requests 

from fastapi import FastAPI
from pydantic import BaseModel

SYSTEM_PROMPT = """
You are a helpful assistant for Python only
- You will solve Python and it's framewrok related problems onlt.
- when ever youll give code output, you will explain that code as well.
- **Other than any python thing you will not answer or help**
"""

GROQ_API_KEY = "Your_Groq_API_Key"  


app = FastAPI(title="Grok Chat", version="0.1.0", description="API for Grok platform communication and LLM responses")

GROQ_BASE_URL = "https://api.groq.com/openai/v1"

class ChatRequestSchema(BaseModel):
    user_input: str
    model: str = "llama-3.3-70b-versatile" 
    max_tokens: int = 1000


@app.get("/")
def read_root():
    return {"message": "Welcome to Grok Chat API"}



@app.post("/chat")
def chat_with_grok_api(req: ChatRequestSchema):
    
    TOP_K = 10  
    TEMPERATURE = 0.7  
    
    api_key = GROQ_API_KEY 
    
    if not api_key:
        print("Groq API key not found. Please set the GROQ_API_KEY environment variable.")
        return {"error": "Internal server error"}
    
    print("Received request:")
    print(req)
    print("------------------")
    
    chat_completion_endpoint = f"{GROQ_BASE_URL}/chat/completions"
    
    auth_headers = f"Bearer {api_key}"  # Authorization header value / auth bearer token
    
    data = {
        "model": req.model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},  # System message
            {"role": "user", "content": req.user_input}
        ],
        "max_tokens": req.max_tokens,
    }
    
    """in request function we pass params as:
    - endpoint URL: where you have to send/hit the request
    - headers: authorization headers like API key or bearer token to verify Identity of the user
    - json: data/payload in JSON(in python its in dictionary format) format to be sent in the request body
    """
    
    resp = requests.post(
        chat_completion_endpoint,
        headers={"Authorization": auth_headers},
        json=data
    )
    """
    
    params = {"key1": "value1", "key2": "value2"}
    reesp = requests.get(
        <endpoint URL>,
        headers={<authorization headers>},
        params=params  # for GET requests
    )
    
    
    """
    
    response = {"response": resp.json()}
    return response
