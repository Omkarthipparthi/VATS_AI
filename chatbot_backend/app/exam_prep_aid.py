from dotenv import load_dotenv
from langchain import hub
from langchain import hub
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
import os
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

from langchain.prompts import FewShotPromptTemplate, PromptTemplate
from langchain_core.pydantic_v1 import BaseModel
from langchain_experimental.tabular_synthetic_data.openai import (
    OPENAI_TEMPLATE,
    create_openai_data_generator,
)
from langchain_experimental.tabular_synthetic_data.prompts import (
    SYNTHETIC_FEW_SHOT_PREFIX,
    SYNTHETIC_FEW_SHOT_SUFFIX,
)
from langchain_openai import ChatOpenAI

load_dotenv()  # Take environment variables from .env.

MY_ENV_VAR = os.getenv('OPENAI_API_KEY')

class MCQ(BaseModel):
    id: int
    wholeQuestion: str
    allOptions: list[str]
    correctOption: str
    
    
examples = [
    {
        "example": 
        """
        id: 1, 
        wholeQuestion: What is the measure of variability that represents the average distance between each data point and the mean of the data set?, 
        allOptions Code: Standard Deviation, Mean, Variance, Range, 
        correctOption Code:  Standard Deviation, 
        """
    },
    {
        "example": 
        """
        id: 2, 
        wholeQuestion: Which of the following is a measure of central tendency?, 
        allOptions Code: Variance, Standard Deviation, Median, Range, 
        correctOption Code:  Median, 
        """
    },
    {
        "example": 
        """
        id: 3, 
        wholeQuestion: What does the p-value in hypothesis testing represent?, 
        allOptions Code: Level of significance, Probability of observing the data given that the null hypothesis is true, Type I error rate, Type II error rate, 
        correctOption Code:  Level of significance, 
        """
    },
        {
        "example": 
        """
        id: 4, 
        wholeQuestion: Which statistical test is used to determine the relationship between two categorical variables?, 
        allOptions Code: ANOVA, T-test, Chi-square test, Regression analysis,
        correctOption Code:  Chi-square test, 
        """
    },
        
]

OPENAI_TEMPLATE = PromptTemplate(input_variables=["example"], template="{example}")

prompt_template = FewShotPromptTemplate(
    prefix=SYNTHETIC_FEW_SHOT_PREFIX,
    examples=examples,
    suffix=SYNTHETIC_FEW_SHOT_SUFFIX,
    input_variables=["subject", "extra"],
    example_prompt=OPENAI_TEMPLATE,
)


synthetic_data_generator = create_openai_data_generator(
    output_schema=MCQ,
    llm=ChatOpenAI(temperature=1, openai_api_key = MY_ENV_VAR, model_name = 'gpt-4'), 
    prompt=prompt_template,
)


synthetic_results = synthetic_data_generator.generate(
    subject="fundamental_statistics",
    extra="Generate similar multiple-choice question (MCQ) on fundamental statistics, Ensure it reflects our examples, and every question you generate must be unique, Ensure the question is clear, with one correct answer and three plausible distractors., Focus on core concepts and common pitfalls.",
    runs=10, 
)


print(synthetic_results)











# client = OpenAI(api_key = MY_ENV_VAR)

# response = client.chat.completions.create(
#   model="gpt-3.5-turbo-0125",
#   response_format={ "type": "json_object" },
#   messages=[
#     {"role": "system", "content": "You are a helpful assistant designed to output JSON, make sure while generating the json, it contains 3 keys per example, they 3 keys are - Question, Options, and Correct Option, also ensure that there are 4 options and 1 correct option."},
#     {"role": "user", "content": "Generate 5 questions on fundamental statistics"}
#   ]
# )
# print(response.choices[0].message.content)