# import os
# from langchain.embeddings.openai import OpenAIEmbeddings
# from langchain.text_splitter import CharacterTextSplitter
# from langchain_community.chat_models import AzureChatOpenAI
# from langchain.embeddings.openai import OpenAIEmbeddings
# from langchain_community.vectorstores import FAISS
# from langchain.chains import RetrievalQA
# from langchain_core.prompts import ChatPromptTemplate
# from langchain.chains import ConversationalRetrievalChain
# # from dotenv import load_dotenv
# from langchain_community.embeddings import HuggingFaceEmbeddings
# from langchain_community.document_loaders import TextLoader, PyPDFLoader, DirectoryLoader, JSONLoader
# from langchain.prompts import PromptTemplate
# from langchain.chains.conversation.memory import ConversationBufferMemory
# from openai import OpenAI
# from langchain.chains import RetrievalQA
# from langchain_openai import OpenAIEmbeddings
# from langchain.agents import initialize_agent, Tool
# from langchain.agents import AgentType
# from langchain.tools import BaseTool
# from langchain_community.llms import OpenAI
# from langchain.tools.retriever import create_retriever_tool
# from langchain.chains.combine_documents import create_stuff_documents_chain
# from langchain.chains import create_retrieval_chain
# from langchain.chains import create_history_aware_retriever
# from langchain_core.prompts import MessagesPlaceholder
# from langchain_core.messages import AIMessage, HumanMessage, get_buffer_string
# from langchain_core.prompts import format_document
# from langchain_core.runnables import RunnableParallel
# import os
# from langchain_community.vectorstores import FAISS
# from langchain_openai import OpenAIEmbeddings
# from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain

# from langchain.text_splitter import CharacterTextSplitter
# from langchain_openai import ChatOpenAI
# from langchain.memory import ConversationBufferMemory
# from langchain.chains import ConversationalRetrievalChain

# from langchain_community.document_loaders import JSONLoader
# from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
# from langchain_community.vectorstores import Chroma
# import json
# from pathlib import Path
# from pprint import pprint

# class chat_gen():
#     def __init__(self):  # Corrected the constructor name
#         self.chat_history = []
#         # Assuming 'Anshul_Mallick.pdf' is a default or example PDF. Adjust as necessary.
#         self.pdf_file_path = './data/Anshul_Mallick.pdf'  # Set a default path relative to the project directory
    
#     def update_pdf_file_path(self, new_path: str):
#         """Update the PDF file path to a new file."""
#         full_path = Path(new_path)
#         if full_path.exists() and full_path.is_file():
#             self.pdf_file_path = new_path
#         else:
#             raise ValueError(f"File path {new_path} is not a valid file")


#     def load_doc(self):
#         """Loads, splits, and processes a PDF document specified by self.pdf_file_path."""
#         if not Path(self.pdf_file_path).is_file():
#             raise FileNotFoundError(f"{self.pdf_file_path} does not exist")

#         # Load the PDF document
#         loader = PyPDFLoader(self.pdf_file_path)
#         documents = loader.load()

#         # Split the document into chunks
#         text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=30, separator="\n")
#         docs = text_splitter.split_documents(documents=documents)

#         # Process the chunks with embeddings
#         embeddings = OpenAIEmbeddings(openai_api_key=self.openai_api_key)
#         vectorstore = FAISS.from_documents(docs, embeddings)

#         # For this example, we're just saving and loading the vectorstore locally
#         vectorstore_path = "./data/faiss_index_datamodel"
#         vectorstore.save_local(vectorstore_path)
#         persisted_vectorstore = FAISS.load_local(vectorstore_path, embeddings, allow_dangerous_deserialization=True)

#         return persisted_vectorstore
    

#     def load_model(self,):
#         llm = ChatOpenAI(model_name = 'gpt-4', openai_api_key=MY_ENV_VAR)
#         memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
#         conversation_chain = ConversationalRetrievalChain.from_llm(
#             llm=llm,
#             retriever=self.load_doc().as_retriever(),
#             memory=memory
#         )
#         return llm
    
#     def ask_pdf(self, question):
#         # result = self.load_model().invoke({"question":question })
#         # llm = ChatOpenAI(model_name = 'gpt-4', openai_api_key=MY_ENV_VAR)
        
#         text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=30, separator="\n")
        
#         kb_docs = PyPDFLoader('json.pdf').load()
#         kb_docs = text_splitter.split_documents(documents=kb_docs)
        
        
#         docs = PyPDFLoader(self.pdf_file_path).load() 
#         docs = text_splitter.split_documents(documents=docs)
        
#         a = ''
        
#         for kb_doc in kb_docs:
#             a += str(kb_doc.metadata["page"]) + ":" + kb_doc.page_content
        
#         a += 'Below is my resume, I am applying to various job postings to secure employement, you are an expert career advisor, Based on my resume, suggest me the most suitable jobs and rank them in order with percentiles in accordance with the job postings available above.'
#         for doc in docs:
#             a += str(doc.metadata["page"]) + ":" + doc.page_content



#         result = self.load_model().invoke(a)
#         return result
        
# if __name__ == '_main_':
#     chat = chat_gen()
#     print(chat.ask_pdf('what are p-values?'))
#     # print(chat.ask_pdf('what are few of its applications?'))




# # response = conversation_chain.invoke({'question': ""})
# # print('question: what are p-values?')
# # print(response['answer'])
# # print('===============================')
# # # print(chat_history)

# # print('what are few of its applications?')
# # response = conversation_chain.invoke({'question': ""})
# # chat_history = response['chat_history']
# # print(response['answer'])
# # print('==============================')
# # # print(chat_history)






































































































































# # OPENAI_API_KEY = os.environ['OPENAI_API_KEY']


# # loader = DirectoryLoader('C:/Users/gunda/Downloads/AI_Buddy/data', glob="*/.pdf",loader_cls = PyPDFLoader)
# # documents = loader.load()
# # # Split document in chunks
# # text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=30, separator="\n")
# # docs = text_splitter.split_documents(documents=documents)
# # embeddings = OpenAIEmbeddings()
# # # Create vectors
# # vectorstore = FAISS.from_documents(docs, embeddings)
# # # Persist the vectors locally on disk


# # vectorstore.save_local("faiss_index_datamodel")

# # # Load from local storage
# # persisted_vectorstore = FAISS.load_local("faiss_index_datamodel", embeddings, allow_dangerous_deserialization=True)




# # llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")


# # prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context:

# # <context>
# # {context}
# # </context>

# # Question: {input}""")

# # document_chain = create_stuff_documents_chain(llm, prompt)


# # retriever = vectorstore.as_retriever()
# # retrieval_chain = create_retrieval_chain(retriever, document_chain)

# # chat_history = []

# # prompt = ChatPromptTemplate.from_messages([
# #     MessagesPlaceholder(variable_name="chat_history"),
# #     ("user", "{input}"),
# #     ("user", "Given the above conversation, generate a search query to look up to get information relevant to the conversation")
# # ])
# # retriever_chain = create_history_aware_retriever(llm, retriever, prompt)


# # prompt = ChatPromptTemplate.from_messages([
# #     ("system", "Answer the user's questions based on the below context:\n\n{context}"),
# #     MessagesPlaceholder(variable_name="chat_history"),
# #     ("user", "{input}"),
# # ])
# # document_chain = create_stuff_documents_chain(llm, prompt)

# # retrieval_chain = create_retrieval_chain(retriever_chain, document_chain)


# # response1 = retrieval_chain.invoke({
# #     "chat_history": chat_history,
# #     "input": "What are p-values?"
# # })
# # response2 = retrieval_chain.invoke({
# #     "chat_history": chat_history,
# #     "input": "What are its applications?"
# # })
# # response3 = retrieval_chain.invoke({
# #     "chat_history": chat_history,
# #     "input": "What are few real world examples applications?"
# # })
# # response4 = retrieval_chain.invoke({
# #     "chat_history": chat_history,
# #     "input": "What is the full form of DNA?"
# # })

# # print(response1)
# # print('-------------------')
# # print(response2)
# # print('-------------------')
# # print(response3["answer"])
# # print('-------------------')
# # print(response4)

# # Import necessary libraries
# # from flask import Flask, render_template, request, redirect
# # from PyPDF2 import PdfReader

# #Please install PdfReader

# # OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
# # from langchain.text_splitter import CharacterTextSplitter
# # from langchain_openai import ChatOpenAI
# # from langchain.memory import ConversationBufferMemory
# # from langchain.chains import ConversationalRetrievalChain


# # chat_history = []


# # loader = DirectoryLoader('C:/Users/gunda/Downloads/AI_Buddy/data', glob="*/.pdf",loader_cls = PyPDFLoader)
# # documents = loader.load()
# # # Split document in chunks
# # text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=30, separator="\n")
# # docs = text_splitter.split_documents(documents=documents)
# # embeddings = OpenAIEmbeddings()
# # # Create vectors
# # vectorstore = FAISS.from_documents(docs, embeddings)
# # # Persist the vectors locally on disk


# # vectorstore.save_local("faiss_index_datamodel")

# # # Load from local storage
# # persisted_vectorstore = FAISS.load_local("faiss_index_datamodel", embeddings, allow_dangerous_deserialization=True)


# # llm = ChatOpenAI()
# # memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
# # conversation_chain = ConversationalRetrievalChain.from_llm(
# #     llm=llm,
# #     retriever=vectorstore.as_retriever(),
# #     memory=memory
# # )

# # response = conversation_chain.invoke({'question': "what are p-values?"})
# # print('question: what are p-values?')
# # print(response['answer'])
# # print('===============================')
# # # print(chat_history)

# # print('what are few of its applications?')
# # response = conversation_chain.invoke({'question': "what are few of its applications?"})
# # chat_history = response['chat_history']
# # print(response['answer'])
# # print('==============================')
# # # print(chat_history)


# # # print('======----------------------------=====')

# # # response = conversation_chain.invoke({'question': "what is the full form of DNA?"})
# # # chat_history = response['chat_history']
# # # print(response)
# # # print('==============================')
# # # print(chat_history)




# # @app.route('/')
# # def index():
# #     return render_template('index.html')

# # @app.route('/process', methods=['POST'])
# # def process_documents():
# #     global vectorstore, conversation_chain
# #     pdf_docs = request.files.getlist('pdf_docs')
# #     raw_text = get_pdf_text(pdf_docs)
# #     text_chunks = get_text_chunks(raw_text)
# #     vectorstore = get_vectorstore(text_chunks)
# #     conversation_chain = get_conversation_chain(vectorstore)
# #     return redirect('/chat')

# # @app.route('/chat', methods=['GET', 'POST'])
# # def chat():
# #     global vectorstore, conversation_chain, chat_history

# #     if request.method == 'POST':
# #         user_question = request.form['user_question']
# #         response = conversation_chain({'question': user_question})
# #         chat_history = response['chat_history']

# #     return render_template('chat.html', chat_history=chat_history)


# # if _name_ == '_main_':
# #     app.run(debug=True)























import os
from dotenv import load_dotenv
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.chat_models import AzureChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import ConversationalRetrievalChain
# from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import TextLoader, PyPDFLoader, DirectoryLoader, JSONLoader
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


from langchain.output_parsers.openai_tools import JsonOutputToolsParser



from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field, validator
from langchain_openai import ChatOpenAI




load_dotenv()  # Take environment variables from .env.

MY_ENV_VAR = os.getenv('OPENAI_API_KEY')

# class jd_match(BaseModel):

#     job_title: str = Field(description="Contains the job title of the job posting")
#     score: str = Field(description="The model evaluates the resume and provides a matching score")
#     reasoning: str = Field(description="The model evaluates why provides reasoning")

class chat_gen:
    def _init_(self):
        self.chat_history = []
        self.OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', MY_ENV_VAR)

    def load_doc(self):

        pass
    

    def load_model(self,):
        embeddings = OpenAIEmbeddings()
        vectorstore = FAISS.load_local("jd_vector", embeddings, allow_dangerous_deserialization=True)
        retriever = vectorstore.as_retriever()
        llm = ChatOpenAI(openai_api_key=MY_ENV_VAR, model_name = 'gpt-4')
        # chain = load_qa_chain(llm, chain_type="stuff",verbose=True)
        retrieval_chain = RetrievalQA.from_chain_type(llm, chain_type="stuff", retriever=retriever)
        return retrieval_chain
    
    def update_pdf_file_path(self, attachedFile):
        docs = PyPDFLoader(attachedFile).load() 
        a = ''
        docs = CharacterTextSplitter(chunk_size=1025, chunk_overlap=30, separator="\n").split_documents(documents=docs)
        for doc in docs:
            a += str(doc.metadata["page"]) + ":" + doc.page_content
        llm = self.load_model()
        b = llm.run('Given my resume below, generate my top 5 skills in just 5 words: ' + a)
        c = llm.run('Note: Only suggest two unique job postings in your context, do not generate random and generic job postings (such as data analyst , software engineer) of what you feel would be better to my skills, I want you to match already exsisting postings in your context with my skills, Make sure to print the exact Job names, and Job Id, from the context, I am a computer science major' + b)

        return c


