import uvicorn
from fastapi import FastAPI, Request
from src.graphs.Graph_builder import GraphBuilder
from src.llms.Groqllm import GroqLLM

import os
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

@app.post("/blogs")
async def create_blogs(request: Request):
    data = await request.json()
    topic = data.get("topic", "")
    language = data.get("language", "")
    
    groqllm = GroqLLM()
    llm = groqllm.get_llm()
    
    graph = GraphBuilder(llm)
    if topic and language:
        graph = graph.setup_graph(usecase="language")
        state=graph.invoke({"topic":topic, "current_language":language.lower()})
        return {"data": state}
    if topic:
        graph = graph.setup_graph(usecase="topic")
        state=graph.invoke({"topic":topic})
        return {"data": state}
    
    
if __name__=="__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
