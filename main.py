from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_agent
from tools import search_tool, math_tool

load_dotenv()


class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]

model = ChatOllama(model='gpt-oss:latest', streaming=True)

parser = PydanticOutputParser(pydantic_object=ResearchResponse)

tools = [search_tool, math_tool]
agent = create_agent(
    model,
    tools,
    system_prompt='''
    You are a helpful assistant that can perform research and answer questions using the provided tools. 
    Use the tools to gather information and perform calculations as needed to provide accurate and comprehensive
    responses to user queries. Always include the tools you used in your response.''',
    response_format=ResearchResponse,
    debug=False
)

def stream_response(query):
    result = agent.stream(
    {"messages": [{"role": "user", "content": f"{query}"}]}
    )

    for chunk in result:
        yield chunk

if __name__ == "__main__":
    
    query = "What day is Christmas this year? And what is the summary of the Wikipedia page for Christmas? And what is 45 mutiplied by 45?"

    for chunk in stream_response(query):
        print("\n==================================\n", end='', flush=True)
        if 'model' in chunk:
            print(f'AI: {chunk['model']['messages'][0].content}', end='', flush=True)
        if 'tools' in chunk:
            print(f'TOOL: {chunk['tools']['messages'][0].content}', end='', flush=True)