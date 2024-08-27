from dotenv import load_dotenv
from fastapi import FastAPI
from langchain.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langserve import add_routes

load_dotenv()
app = FastAPI()

# LangChain setup
llm = ChatOllama(
    model="llama3.1:8b",
    temperature=0,
)

prompt1 = ChatPromptTemplate.from_template(
    "Write me an essay about {topic} with 100 words"
)

prompt2 = ChatPromptTemplate.from_template(
    "Write me an poem about {topic} for a 5 years child with 100 words"
)

add_routes(app, prompt1 | llm, path="/essay")

add_routes(app, prompt2 | llm, path="/poem")
