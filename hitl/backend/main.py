from fastapi import FastAPI
from pydantic import BaseModel
from agent import worflow,OrderProcessState
from fastapi.middleware.cors import CORSMiddleware
from langgraph.types import interrupt,Command

class Req(BaseModel):
    id:int = None
    items:str=None
    price:str=None
    processed:bool=False
    final_msg:str=None
    o_type:str=None
   
class Decison(BaseModel):
    decison:str

app = FastAPI()

origins = [
    "http://localhost:3000",  # Default React development port (CRA)
    "http://localhost:5173",  # Default Vite + React development port
    "https://yourproductiondomain.com"  # Your production frontend domain
]

# 2. Add the CORS middleware to your FastAPI application
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # Allows requests from specified domains
    allow_credentials=True,         # Allows cookies and headers like Authorization
    allow_methods=["GET","POST","OPTIONS","PUT"],            # Allows all standard HTTP methods (GET, POST, etc.)
# Allows all request headers
)


@app.get("/")
def root():
    return {"message":"Hello world"}

@app.post("/ai/start")
def agentStart(datas:Req):
    print("START")
    print(datas)
    initialState=datas.model_dump()
    res = worflow.invoke(initialState,{"configurable":{"thread_id":"th1"}})
    print("a",res)

    if "__interrupt__" in res and res["__interrupt__"]:
    # 2. Extract the interrupt structure cleanly 
        val = res["__interrupt__"][0]
    
    # 3. Print the underlying data or message payload
        thread_id = val.id
        return {"thread_id":thread_id,"message":val.value}

        

    print(res)
    return {"message":"Order processed","data":res} 
    

@app.post("/ai/approve/{thread_id}")
def userDecsion(thread_id:str,decison:Decison):
    res = worflow.invoke(Command(
        resume=decison,

    ),{"configurable":{"thread_id":thread_id}})

    print(res)
    return res 

