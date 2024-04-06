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
        pass

        
        # print("load doc")
        # loader = DirectoryLoader('data/', glob="*.pdf",loader_cls = PyPDFLoader)

        # documents = loader.load()
        # text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=30, separator="\n")
        # docs = text_splitter.split_documents(documents=documents)
        # embeddings = OpenAIEmbeddings(openai_api_key=MY_ENV_VAR)
        # vectorstore = FAISS.from_documents(docs, embeddings)
        # vectorstore.save_local("faiss_index_datamodel")
        # vectorstore = FAISS.load_local("faiss_index_datamodel", embeddings, allow_dangerous_deserialization=True)
        # return vectorstore
    

    def load_model(self,):
        embeddings = OpenAIEmbeddings(openai_api_key=MY_ENV_VAR)
        vectorstore = FAISS.load_local("faiss_index_datamodel", embeddings, allow_dangerous_deserialization=True)
        retriever = vectorstore.as_retriever()
        llm = ChatOpenAI(openai_api_key=MY_ENV_VAR)
        print("load model")
        contextualize_q_system_prompt = """Given a chat history and the latest user question \
        which might reference context in the chat history, formulate a standalone question \
        which can be understood without the chat history. Do NOT answer the question, \
        just reformulate it if needed and otherwise return it as is."""
        contextualize_q_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", contextualize_q_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )
        history_aware_retriever = create_history_aware_retriever(
            llm, retriever, contextualize_q_prompt
        )


        qa_system_prompt = """You are an assistant for question-answering tasks. \
        Use the following pieces of retrieved context to answer the question. \
        If you don't know the answer, just say I don't know. \
        Use three sentences maximum and keep the answer concise.\

        {context}"""
        qa_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", qa_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )

        question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

        rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

        print("rag_chain")  
        return rag_chain
    
    def ask_pdf(self, question):
        print(question)
        result = self.load_model().invoke({"input":question, "chat_history": self.chat_history })
        print(result['answer'])
        self.chat_history.extend([HumanMessage(content=question), result["answer"]])

        return result['answer']
