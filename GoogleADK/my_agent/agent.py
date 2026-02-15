from google.adk.agents.llm_agent import Agent
from google.adk.tools import google_search

root_agent = Agent(
    name="root_agent",
    model="gemini-3-flash-preview",
    description="Recommends various dishes and foods when user feels hungry and confused, on basis of their mood and interests.",
    instruction="You are a helpful assistant that recommends various dishes and foods when user feels hungry and confused, on basis of their mood and interests.",
    tools=[google_search],
)