from fastapi import FastAPI
from pydantic import BaseModel
from Services.final_Project import agent_executor

app = FastAPI()

agent = agent_executor()


@app.get("/chat")
async def chat(query: str):
    return {"response": agent.run(query)}



