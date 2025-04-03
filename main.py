from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_tool_calling_agent, AgentExecutor
from tools import search_tool,save_tool  

load_dotenv()

llm = ChatGroq(temperature=0, 
    model_name="llama3-70b-8192"  
)


prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a research assistant. Answer the user's query using the necessary tools."),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}")
    ]
)



tools = [search_tool,save_tool]

agent = create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=tools
)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

query = input("What can I help you research? ")

raw_response = agent_executor.invoke({"query": query})

try:
    structured_response = parser.parse(raw_response.get("output")[0]["text"])
    print(structured_response)
except Exception as e:
    print("Error parsing response:", e, "Raw Response -", raw_response)
