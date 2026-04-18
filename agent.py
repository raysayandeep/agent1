from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
from pydantic import BaseModel
from langgraph_supervisor import create_supervisor
from langchain_ollama import ChatOllama
import os
from tools import search_tool, custom_math_tool, wiki_tool
from pritty_print_msg import pretty_print_messages

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    print("Error: GROQ_API_KEY environment variable not set.")
    exit(1)

# llm1 = ChatGroq(model='meta-llama/llama-4-scout-17b-16e-instruct',
                # api_key=groq_api_key)

llm2 = ChatOllama(model='mistral:latest')

llm = llm2


class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]


search_agent = create_react_agent(
    llm,
    tools=[search_tool, wiki_tool],
    name="search_agent",
    description="A research assistant that helps generate answer based on search."
)

math_agent = create_react_agent(
    llm,
    tools=[custom_math_tool],
    name="math_agent",
    description="A Math assistant that performs basic math operations."
)

supervisor_worlflow = create_supervisor(
    [math_agent, search_agent],
    model=llm,
    prompt=(
        "You are a assistant that will help user query. "
        "Answer the user query with clear explanation only by using available tools."
        "do not try to generate answer without using tools."
    ),
    add_handoff_back_messages=True,
    output_mode="full_history"
)

app = supervisor_worlflow.compile()


if __name__ == "__main__":
    print("Welcome to the Research Assistant!")
    print("You can ask about any topic, and I will search for information.")
    print("You can also perform basic math operations.")
    print("Type 'exit' to quit.")
    try:
        while True:
            try:
                query = input("Enter your query: ")
            except (KeyboardInterrupt, EOFError):
                print("\nGoodbye!")
                break
            if query.lower() == "exit":
                print("Goodbye!")
                break
            try:
                for chunk in app.stream(
                    {
                        "messages": [
                            {
                                "role": "user",
                                "content": query,
                            }
                        ]
                    },
                ):
                    pretty_print_messages(chunk, last_message=True)
            except Exception as e:
                print(f"Error during processing: {e}")
    except Exception as main_e:
        print(f"Unexpected error: {main_e}")
