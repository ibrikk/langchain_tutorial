import os
from dotenv import load_dotenv
from langchain_ollama import OllamaLLM
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.tracers import LangChainTracer

load_dotenv()

# Langsmith Tracking
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
# Langsmith tracing
os.environ["LANGCHAIN_PROJECT_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT")

## Prompt Template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Please respond to the question asked"),
        ("user", "Question {question}"),
    ]
)

## streamlit framework
st.title("LangChain Demo With Gemma model")
input_text = st.text_input("What question you have in mind?")

## Ollama Llama2 model
llm = OllamaLLM(model="gemma:2b")
output_parser = StrOutputParser()
tracer = LangChainTracer()
chain = prompt | llm | output_parser

if input_text:
    try:
        with st.spinner("Thinking..."):
            response = chain.invoke({"question": input_text}, config={"callbacks": [tracer]})
            st.write(response)
    except Exception as e:
                st.error(f"Something went wrong: {e}")


