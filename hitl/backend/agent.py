from langgraph.types import interrupt,Command
from dotenv import load_dotenv
load_dotenv()
from langgraph.graph import START,END,StateGraph
from langchain.tools import tool
from typing import TypedDict,Literal
from langgraph.checkpoint.memory import InMemorySaver
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

class OrderProcessState(TypedDict):
    id:int
    items:str
    price:str
    processed:bool=False
    final_msg:str
    o_type:str

graph = StateGraph(OrderProcessState)



def order_process(state:OrderProcessState)->OrderProcessState:

    if state.get("o_type") == "pay":
        decison = interrupt(f"Do you wnat to pay for {state["items"]} at {state["price"]} ??")

        if(decison=="yes"):
            state["processed"]=True
            state["final_msg"]="Successfully processed payment"
            print("Succesfully paid")
            return state
        else:
            print("this order cant be processed ")
            

    else:
        print( "sucesfully viwed ")
        return state
    
graph.add_node("order",order_process)

graph.add_edge(START,"order")
graph.add_edge("order",END)

worflow = graph.compile(checkpointer=InMemorySaver())










# r = worflow.invoke(Command(
#     resume="yes"
# ), config={"configurable":{"thread_id":"th9"}})
