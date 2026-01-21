from dotenv import load_dotenv
import os
from typing import TypedDict, Annotated, Sequence
from operator import add as add_messages
import json
from langgraph.graph import StateGraph, END
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, ToolMessage, AIMessage
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.tools import tool

# Load environment variables: API keys, etc.
load_dotenv(".env")

# ************************************** Build Translation Workflow **************************************
# Create a one big function to build the workflow for Livekit use
def create_workflow():

    class AgentState(TypedDict):
        messages: Annotated[Sequence[BaseMessage], add_messages]
    
    # Set up global variables for types of language
    lang_a = ""
    lang_b = ""



    # ------------------------------------ Set up tools ------------------------------------
    # Set up two languages that are going to be translated bidirectionally
    @tool
    def language_setup(language_A: str, language_B: str) -> str:
        """Set up language_A and language_B as the languages that are going to be translated bidirectionally according to the user's request"""
        global lang_a, lang_b
        lang_a = language_A
        lang_b = language_B
        return lang_a, lang_b

    # Retrieve the supported languages from the Chroma database and check if the lang_a and lang_b are listed in the document
    @tool
    def retrieve_supported_languages(query: str) -> str:
        """Retrieve the supported languages from the Chroma database and check if the lang_a and lang_b are listed in the document"""
        global lang_a, lang_b
        languages = retriever.invoke(query)
        for language in languages:
            if lang_a in language.page_content and lang_b in language.page_content: # Check if the lang_a and lang_b are bothlisted in the document
                return f"We support translation between {lang_a} and {lang_b}"
            # If either lang_a or lang_b is not listed in the document, return that we do not support translation between them
            elif lang_a not in language.page_content and lang_b in language.page_content:
                return f"We do not support {lang_a}, please select a different language"
            elif lang_b not in language.page_content and lang_a in language.page_content:
                return f"We do not support {lang_b}, please select a different language"
            # If neither lang_a nor lang_b is listed in the document, return that we do not support translation between them
            else:
                return f"We do not support {lang_a} and {lang_b}, please select different languages"

    # Record the conversation between the user and the agent during the translation process to a text file for later review.
    @tool
    def record_tool(conversation: str) -> str:
        """Records the conversation between the user and the agent during the translation process to a text file for later review."""
        
        # Parse messages from JSON
        messages_data = json.loads(conversation)

        # "a" — append mode; writes append to the end if the file exists, creates it if it doesn’t. (Other modes: "r" read, "w" write/overwrite, "x" exclusive create.)
        with open("intertranslation_conversation.txt", "a", encoding="utf-8") as f:
            global lang_a, lang_b
            f.write("\n" + "=" * 60 + "\n")
            f.write("CONVERSATION LOG for translation between {lang_a} and {lang_b}\n\n")
            
            for msg_data in messages_data:
                msg_type = msg_data.get("type", "unknown")
                content = msg_data.get("content", "")
                
                if msg_type == "human":
                    f.write(f"👤 User: {content}\n\n")
                elif msg_type == "ai":
                    f.write(f"🤖 Translator: {content}\n\n")
            f.write("-" * 60 + "\n\n")
        
        print(f"Recorded conversation with {len(messages_data)} messages")
        return "Conversation recorded successfully!"


    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.0)
    
    # RAG: Create a vector database to store the list of the languages that are supported for translation
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004"), # Embedding model must match the LLM
    pdf_path = os.getenv("Languages_PDF_PATH", "./Languages_supported.pdf")
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"Sorry, we do not support translation for {lang_a} and {lang_b}")
    
    pages = PyPDFLoader(pdf_path).load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    pages_split = text_splitter.split_documents(pages)

    persist_directory = os.getenv("CHROMA_DIR", "./chroma_store") # CHROMA_DIR is the environment variable that stores the path to the Chroma database. Reads the CHROMA_DIR environment variable for the directory path. If not set, defaults to "./chroma_store" (current directory).
    os.makedirs(persist_directory, exist_ok=True) # Creates the directory if it doesn't exist. exist_ok=True means that if the directory already exists, it won't raise an error.

    # Creates a Chroma vectorstore from the documents.
    # Chroma is an open-source vector database. It’s used for storing and searching data by semantic similarity, which fits retrieval-augmented generation (RAG).
    vectorstore = Chroma.from_documents(
        documents=pages_split,
        embedding=embeddings,
        persist_directory=persist_directory, # Persist directory is the path to the directory where the Chroma database will be stored.
        collection_name="company_info", # Collection name is the name of the collection in the Chroma database.
    )

    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 2}) # Creates a retriever object from the vectorstore. search_type="similarity" means that the retriever will use semantic similarity to find the most relevant documents. search_kwargs={"k": 2} means that the retriever will return the 2 most relevant documents.


