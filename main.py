import asyncio

import ollama
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 요청 데이터 모델
class QueryRequest(BaseModel):
    prompt: str
    max_tokens: int = 512


async def generate_response(prompt: str, max_tokens: int):
    response = await asyncio.to_thread(
        ollama.chat,
        model="llama3.2:1b",
        messages=[{"role": "user", "content": prompt}],
    )
    return response["message"]["content"]


@app.post("/generate/")
async def generate_text(request: QueryRequest):
    try:
        response = await generate_response(request.prompt, request.max_tokens)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
