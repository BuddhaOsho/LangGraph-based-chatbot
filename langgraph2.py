from dotenv import load_dotenv
from typing_extensions import  TypedDict
from typing import Optional,Literal
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from openai import OpenAI
load_dotenv()

client = OpenAI(
    api_key="AIzaSyAVjGIOmRdMGCgIogLAHrMjHDn35rfsZhI",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
class State(TypedDict):
    user_query: str
    llm_output : Optional[str]
    is_good: Optional[bool]

graph_loader = StateGraph(State)

def chatbot(state:State):
    print("chatbot",state)
    response= client.chat.completions.create(
        model= "gemini-2.5-flash",
        messages=[
            {"role": "user", "content":state.get("user_query")}
        ]
    
    )
    state["llm_output"]= response.choices[0].message.content
    return state 

def evaluate_response(state:State)-> Literal["chatbot_gemini","endnode"]:
    print("evaluate_response",state)
    if True:
        return "endnode"
    return "chatbot_gemini"

def chatbot_gemini(state:State):
    print("chatbot_gemini",state)
    response= client.chat.completions.create(
        model = "gemini-2.5-flash",
        messages=[
            {"role":"user","content":state.get("user_query")}
        ]
        
    )
    return state
def endnode(state:State):
    print("endnode",state)
    return state

graph_builder = StateGraph(State)

graph_builder.add_node("chatbot",chatbot)
graph_builder.add_node("chatbot_gemini",chatbot_gemini)
graph_builder.add_node("endnode",endnode)

# START>chatbot>evaluate_response>chatbot_gemini|endnode>END

graph_builder.add_edge(START,"chatbot")
graph_builder.add_conditional_edges("chatbot",evaluate_response)
graph_builder.add_edge("chatbot_gemini","endnode")
graph_builder.add_edge("endnode",END)

graph = graph_builder.compile()

graph.invoke({"user_query": "Hey what is 2+2"})



