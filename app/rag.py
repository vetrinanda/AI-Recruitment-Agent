import os
from dotenv import load_dotenv

load_dotenv()

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_chroma import Chroma
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# --- 1. Initialize Models ---
# Ensure GOOGLE_API_KEY is set in .env
if not os.getenv("GOOGLE_API_KEY"):
    print("Warning: GOOGLE_API_KEY not found in environment variables.")

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.7)
embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")

# --- 2. Load and Store Document ---
file_path = "Think-And-Grow-Rich_2011-06.pdf"
persist_dir = "./chroma_db"
collection_name = "example_collection"

# Initialize vector_store (will load/create if needed)
vector_store = Chroma(
    collection_name=collection_name,
    embedding_function=embeddings,
    persist_directory=persist_dir,
)

# Only load and add documents if the collection is empty or usually we might check logic here
# For the script purporse, we try to load if file exists
if os.path.exists(file_path):
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    print(f"Loaded {len(docs)} pages.")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=200, add_start_index=True
    )
    all_splits = text_splitter.split_documents(docs)
    print(f"Created {len(all_splits)} splits.")

    # Add to vector store
    # Note: This might duplicate docs if run multiple times without checking. 
    # For a simple script, we assume user manages state or clears DB.
    # To check if empty:
    if vector_store._collection.count() == 0:
         vector_store.add_documents(documents=all_splits)
         print("Documents added to vector store.")
    else:
         print("Vector store already populated. Skipping ingestion.")
else:
    print(f"File {file_path} not found. Ensure it exists or vector store is already populated.")

# --- 3. Define Tool ---
@tool(response_format="content_and_artifact")
def retrieve_context(query: str):
    """Retrieve information to help answer a query."""
    retrieved_docs = vector_store.similarity_search(query, k=2)
    serialized = "\n\n".join(
        (f"Source: {doc.metadata}\nContent: {doc.page_content}")
        for doc in retrieved_docs
    )
    return serialized, retrieved_docs

# --- 4. Agentic RAG (LangGraph) ---
tools = [retrieve_context]
system_prompt = (
    "You have access to a tool that retrieves context from a book. "
    "Use the tool to help answer user queries."
)

# Using LangGraph's prebuilt ReAct agent
agent = create_react_agent(llm, tools, state_modifier=system_prompt)

query = "burning desire as a driving force"

print("--- Agentic RAG Stream ---")
try:
    for event in agent.stream(
        {"messages": [{"role": "user", "content": query}]},
        stream_mode="values",
    ):
        event["messages"][-1].pretty_print()
except Exception as e:
    print(f"Error running agent: {e}")


# --- 5. Traditional RAG Chain ---
print("\n--- Traditional RAG Chain ---")
retriever = vector_store.as_retriever(search_kwargs={"k": 2})

template = """
Answer the question based on the context provided.
Context: {context}
Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)

rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

try:
    response = rag_chain.invoke("What is the main idea of the book?")
    print(response)
except Exception as e:
    print(f"Error running chain: {e}")