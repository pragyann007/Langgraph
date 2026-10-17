from langgraph.graph import START,END,StateGraph
from typing import TypedDict

class MyState(TypedDict):
    vala:str
    valb:str

def nodeA(state:MyState):
    state["vala"]="a"
    return {"vala":"a"}

def nodeB(state:MyState):
    state["valb"]="b"
    return {"valb":"b"}

graph = StateGraph(MyState)

graph.add_node("nodea",nodeA)
graph.add_node("nodeb",nodeB)

graph.add_edge(START,"nodea")
graph.add_edge("nodea","nodeb")
graph.add_edge("nodeb",END)


workflow = graph.compile()

reuslt = workflow.invoke({"vala":"","valb":""})

print(result)


