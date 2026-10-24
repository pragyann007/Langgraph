import warnings
# Silence deprecation warnings so your terminal stays clean
warnings.filterwarnings("ignore", category=DeprecationWarning)

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from dotenv import load_dotenv
from langgraph.graph import START, END, StateGraph
load_dotenv()
from typing import TypedDict, Literal
from pydantic import BaseModel

# 1. Initialize your Gemini Embeddings
embeder = GoogleGenerativeAIEmbeddings(model="gemini-embedding-2")

class EnhacedPrompts(BaseModel):
    prompts: list[str]

class Router(BaseModel):
    needRag: bool

# 2. Connect to your LOCAL Docker Qdrant
client = QdrantClient(url="http://localhost:6333")

collection_name = "demo_collection"
if not client.collection_exists(collection_name):
    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=3072, distance=Distance.COSINE),
    )

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
prompt_enhance_model = model.with_structured_output(EnhacedPrompts)
router__model = model.with_structured_output(Router)

# 4. Bind Qdrant with LangChain
vector_store = QdrantVectorStore(
    client=client,
    collection_name=collection_name,
    embedding=embeder,
)

class ChatStates(TypedDict):
    initialPrompt: str 
    needRag: bool
    promptLists: list[str]
    final_messages: str

def routerAgent(state: ChatStates) -> ChatStates:
    iMsg = state["initialPrompt"]
    prompt = f"Look at this user prompt and if you know the answer give it but if you dont know like the user query is some document based or internal data then return needRag:True note if you know the answer then return needRag:False but if you dont know users answer like users internal data or you dont have any idea of that then you should return needRag True so that the vector searching can occur.. for ex if user ask info about them their company and in your message history or context you dont have any knowledge of it then simply return True but if the user query is general like pm of nepal write blogs etc etc then it dont need internal data then that time do False users query = {iMsg}"

    res = router__model.invoke(prompt)
    state["needRag"] = res.needRag
    return state 

def rawPromptChat(state: ChatStates) -> ChatStates:
    initial = state["initialPrompt"]
    prompt = f"This user has a raw prompt i want you to make this highly specialised one so convert this user query into 3 extra more query so that the retrieving from db is smooth and does thing super nicely.. raw prompt : {initial} give response in this format give only 3 enhanced prompt in array form"

    res = prompt_enhance_model.invoke(prompt)
    state["promptLists"] = res.prompts 
    return state 

def ragNode(state: ChatStates):
    origPrompt = state["initialPrompt"]
    # Provide a fallback fallback list if promptLists somehow wasn't generated
    prompts = state.get("promptLists", [])
    
    extracted_docs = []

    # Run the Multi-Query retrieval loop
    for query in prompts:
        search_results = vector_store.similarity_search_with_score(query, k=2)
        for doc, score in search_results:
            # Gather page content text cleanly
            extracted_docs.append(doc.page_content)

    # Search using original prompt as well
    orig_result = vector_store.similarity_search_with_score(origPrompt, k=2)
    for doc, score in orig_result:
        extracted_docs.append(doc.page_content)

    # Deduplicate the context strings to save token space
    unique_context = list(set(extracted_docs))
    context_str = "\n---\n".join(unique_context)

    aiPrompt = f"You are a helpful AI assistant. This is the user's primary prompt, accompanied by text fragments retrieved from our vector database. Based on this information and your intelligence, answer the question accurately.\n\nUser prompt: {origPrompt}\n\nRetrieved Context:\n{context_str}"

    response = model.invoke(aiPrompt)
    state["final_messages"] = response.content 
    return state 

def generalNode(state: ChatStates):
    # FIXED: Swapped out nested double-quotes to avoid syntax errors
    prompt = f"Answer the users query accurately , userPrompt : {state['initialPrompt']}"
    res = model.invoke(prompt)
    state["final_messages"] = res.content 
    return state 

def router_conditional(state: ChatStates) -> Literal["prompt", "generalNode"]:
    if state["needRag"]:
        return "prompt"
    else:
        return "generalNode"

graph = StateGraph(ChatStates)

graph.add_node("prompt", rawPromptChat)
graph.add_node("router", routerAgent)
graph.add_node("ragNode", ragNode)
graph.add_node("generalNode", generalNode)

graph.add_edge(START, "router")
graph.add_conditional_edges("router", router_conditional)
graph.add_edge("prompt", "ragNode")
graph.add_edge("ragNode", END)
graph.add_edge("generalNode", END)

workflow = graph.compile()

res = workflow.invoke({"initialPrompt": "what is withdrawal pattern written in the document"})
print("\n--- Final Agent Output ---")
print(res["final_messages"])



# text_splitter = RecursiveCharacterTextSplitter(
#     chunk_size=1000,
#     chunk_overlap=200
# )

# print("hi")

# # Load and split your PDF
# loader = PyPDFLoader(file_path="./doc.pdf")
# docs = loader.load()
# print(f"Loaded {len(docs)} pages.")

# texts = text_splitter.split_documents(docs)

# # FIX: Changed from 'aadd_documents' (async) to 'add_documents' (sync)
# vector_store.add_documents(texts)
# print(f"Successfully added {len(texts)} chunks to Qdrant!")

