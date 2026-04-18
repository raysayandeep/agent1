from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from ddgs import DDGS
from langchain.tools import tool
from datetime import datetime

# search = DuckDuckGoSearchRun()

def duckduckgosearch(query):
    '''Search the Web with Duckduckgo for information'''
    ddgs = DDGS()
    results = ddgs.text(query, region='wt-wt',
                        safesearch='off', max_results=10)
    return results

@tool
def search_tool(query):
    '''Search the Web with Duckduckgo for information.
    use this tool to get any information which can not be answered by simple math operations.
    '''
    results = duckduckgosearch(query)
    return results

# search_tool = tool(
#     name="search",
#     func=duckduckgosearch,
#     description="Search the Web with Duckduckgo for information"
# )

# api_wrapper = WikipediaAPIWrapper(
#     top_k_results=1,
#     doc_content_chars_max=1000
# )

# wiki = WikipediaQueryRun(api_wrapper=api_wrapper)
# wiki_tool = tool(
#     name="wiki",
#     func=wiki.run,
#     description="Search Wikipedia for information"
# )

@tool
def math_tool(num1, num2, operator):
    '''Perform basic math operations
    valid operators are +, -, *, /
    valid inputs are num1, num2, operator
    '''
    if operator == '+':
        return num1 + num2
    elif operator == '-':
        return num1 - num2
    elif operator == '*':
        return num1 * num2
    elif operator == '/':
        return num1 / num2
    else:
        return "Invalid operator"


# custom_math_tool = tool(
#     name="simple_math",
#     func=math_tool,
#     description="Perform basic math operations"
# )

if __name__ == "__main__":
    print(duckduckgosearch("Current weather in Darjeeling"))
