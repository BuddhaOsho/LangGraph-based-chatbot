from dotenv import load_dotenv
from typing_extensions import  TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.mongodb import MongoDBSaver

load_dotenv()
llm = ChatOpenAI(model="gpt-4o-mini")


class State(TypedDict):
    messages: Annotated[list, add_messages]

def chatbot(state:State):
    response = llm.invoke(state.get("messages"))
    print("\n\nwe are inside chatbot node",state)
    return {"messages": [response] }



graph_builder = StateGraph(State)

graph_builder.add_node("chatbot",chatbot)


graph_builder.add_edge(START,"chatbot")
graph_builder.add_edge("chatbot", END)


graph = graph_builder.compile()

def compile_graph_with_checkpointer(checkpointer):
    return  graph_builder.compile(checkpointer=checkpointer)

DB_URI = "mongodb://admin:admin@localhost:27017"
with MongoDBSaver.from_conn_string(DB_URI) as checkpointer:
    graph_with_checkpointer = compile_graph_with_checkpointer(checkpointer=checkpointer)
    config = {
            "configurable":{
                "thread_id":"BuddhaOsho"
            }
                }
    for chunk in graph_with_checkpointer.stream(State(
        {"messages":["my name is buddha"]}),
        config,
        stream_mode="values"
        ):
            chunk["messages"][-1].pretty_print()
   







# START > chatbot > samplenode > END
