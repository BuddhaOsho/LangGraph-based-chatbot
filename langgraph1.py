from dotenv import load_dotenv
from typing_extensions import  TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI

load_dotenv()
llm = ChatOpenAI(model="gpt-4o-mini")


class State(TypedDict):
    messages: Annotated[list, add_messages]

def chatbot(state:State):
    response = llm.invoke(state.get("messages"))
    print("\n\nwe are inside chatbot node",state)
    return {"messages": [response] }

def samplenode(state:State):
    print("\n\nwe are inside samplenode", state)
    return{"messages":["Sample Message appended"]}

graph_builder = StateGraph(State)

graph_builder.add_node("chatbot",chatbot)
graph_builder.add_node("samplenode",samplenode)

graph_builder.add_edge(START,"chatbot")
graph_builder.add_edge("chatbot","samplenode")
graph_builder.add_edge("samplenode",END)

graph = graph_builder.compile()

updated_state= graph.invoke(State({"messages": ["Hii, my name is pritesh "]}))

print("\n\nupdated_state", updated_state)
# START > chatbot > samplenode > END
