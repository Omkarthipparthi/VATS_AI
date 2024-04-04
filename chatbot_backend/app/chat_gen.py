import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.chat_models import AzureChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import ConversationalRetrievalChain
from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import TextLoader, PyPDFLoader, DirectoryLoader
from langchain.prompts import PromptTemplate
from langchain.chains.conversation.memory import ConversationBufferMemory
from openai import OpenAI
from langchain.chains import RetrievalQA
from langchain_openai import OpenAIEmbeddings
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.tools import BaseTool
from langchain_community.llms import OpenAI
from langchain.tools.retriever import create_retriever_tool
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain.chains import create_history_aware_retriever
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.messages import AIMessage, HumanMessage, get_buffer_string
from langchain_core.prompts import format_document
from langchain_core.runnables import RunnableParallel
import os
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain

from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain




load_dotenv()  # Take environment variables from .env.

MY_ENV_VAR = os.getenv('OPENAI_API_KEY')

class chat_gen:
    def __init__(self):
        self.chat_history = []
        self.OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', MY_ENV_VAR)

    def load_doc(self):

        loader = DirectoryLoader('./data', glob="**/*.pdf",loader_cls = PyPDFLoader)
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=30, separator="\n")
        docs = text_splitter.split_documents(documents=documents)
        embeddings = OpenAIEmbeddings(openai_api_key=MY_ENV_VAR)
        vectorstore = FAISS.from_documents(docs, embeddings)
        vectorstore.save_local("faiss_index_datamodel")
        persisted_vectorstore = FAISS.load_local("faiss_index_datamodel", embeddings, allow_dangerous_deserialization=True)
        return persisted_vectorstore
    

    def load_model(self,):
        llm = ChatOpenAI(openai_api_key=MY_ENV_VAR)
        memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
        conversation_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=self.load_doc().as_retriever(),
            memory=memory
        )

        return conversation_chain
    
    def ask_pdf(self, question):
        print(question)
        result = self.load_model().invoke({"question":question })
        return result['answer']