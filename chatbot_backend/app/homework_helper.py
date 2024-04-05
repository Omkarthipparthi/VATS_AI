from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain.chains import create_history_aware_retriever
from langchain_core.prompts import MessagesPlaceholder
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import create_history_aware_retriever
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.messages import AIMessage, HumanMessage, get_buffer_string

loader = DirectoryLoader('textbook_data/', glob="*.pdf",loader_cls = PyPDFLoader)

documents = loader.load()
# Split document in chunks
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=30, separator="\n")
docs = text_splitter.split_documents(documents=documents)
embeddings = OpenAIEmbeddings(openai_api_key="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")
# Create vectors
vectorstore = FAISS.from_documents(docs, embeddings)
# Persist the vectors locally on disk
vectorstore.save_local("faiss_index_datamodel")

vectorstore = FAISS.load_local("faiss_index_datamodel", embeddings, allow_dangerous_deserialization=True)

# Retrieve and generate using the relevant snippets of the blog.
retriever = vectorstore.as_retriever()
llm = ChatOpenAI(openai_api_key="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")


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

chat_history = []

question = "What are P-values?"
ai_msg_1 = rag_chain.invoke({"input": question, "chat_history": chat_history})
chat_history.extend([HumanMessage(content=question), ai_msg_1["answer"]])

print(ai_msg_1["answer"])
print("----------------------------------")

second_question = "What are few of it's applications"
ai_msg_2 = rag_chain.invoke({"input": second_question, "chat_history": chat_history})
chat_history.extend([HumanMessage(content=second_question), ai_msg_2["answer"]])

print(ai_msg_2["answer"])
