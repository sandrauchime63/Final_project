from langchain_openai import ChatOpenAI 
from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory
from langchain_community.document_loaders import JSONLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.tools import tool
import requests
from bs4 import BeautifulSoup



llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key="***", # type: ignore
    temperature=0,

)

loader = JSONLoader(
    file_path="Final_files/school_file.json",
    jq_schema=".faqs[] | .answer"
)
documents = loader.load()


text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200,add_start_index=True)
allsplit=text_splitter.split_documents(documents)




embed = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


vectorstore = Chroma.from_documents(
    documents=allsplit,
    embedding=embed,
    persist_directory="new_db"
)

vectorstore.persist()



url="https://unilag.edu.ng/"

@tool
def search_school_website(user_input: str) :
    """Fetch and extract text from a school website."""

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    text = soup.get_text()
    return text[:2000]

@tool
def chooser(user_input):
    """Search FAQ vector database"""
    result=vectorstore.similarity_search(user_input, k=1)

    doc=result[0].page_content



tools=[search_school_website, chooser]
def agent_executor():
    agent = initialize_agent(
    tools, # type: ignore
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    handle_parsing_errors=True,
    verbose=True,
    max_iteration=3,
    memory = ConversationBufferMemory()
)
    return agent







