import warnings
# Silence deprecation warnings so your terminal stays clean
warnings.filterwarnings("ignore", category=DeprecationWarning)

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings,ChatGoogleGenerativeAI
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from dotenv import load_dotenv
load_dotenv()
# 1. Initialize your Gemini Embeddings
embeder = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-2",
    
)

# 2. Connect to your LOCAL Docker Qdrant instead of temporary in-memory
# Change back to ":memory:" if you don't want to use Docker
client = QdrantClient(url="http://localhost:6333")

# 3. Create collection if it doesn't exist
collection_name = "demo_collection"
if not client.collection_exists(collection_name):
    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=3072, distance=Distance.COSINE),
    )

# 4. Bind Qdrant with LangChain
vector_store = QdrantVectorStore(
    client=client,
    collection_name=collection_name,
    embedding=embeder,
)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

print("hi")

# Load and split your PDF
loader = PyPDFLoader(file_path="./doc.pdf")
docs = loader.load()
print(f"Loaded {len(docs)} pages.")

texts = text_splitter.split_documents(docs)

# FIX: Changed from 'aadd_documents' (async) to 'add_documents' (sync)
vector_store.add_documents(texts)
print(f"Successfully added {len(texts)} chunks to Qdrant!")

query = "What is factory attern in smart contract"
result =vector_store.similarity_search(query,k=4)

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

prompt = f"This is users query : {query} and this is the relevant vector db results for the user queris : {result} \n \n based on this gove th eresponse  "

res = model.invoke(prompt)

print(res.content)

