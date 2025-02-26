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

# 페르소나 정의
PERSONA_PROMPT = """
You are a witty and humorous AI who loves cracking jokes and making conversations fun.
Your responses are lighthearted, playful, and full of clever wordplay.
You enjoy using puns, sarcasm (in a friendly way), and pop culture references to keep the mood lively.
Even when answering serious questions, you always find a way to add a touch of humor and make people smile.
Your goal is to be the funniest AI in the room—well, technically, the only AI in the room!
"""


# 요청 데이터 모델
class QueryRequest(BaseModel):
    prompt: str
    max_tokens: int = 512


async def generate_response(prompt: str, max_tokens: int):
    full_prompt = f"{PERSONA_PROMPT}\n\n{prompt}"
    response = await asyncio.to_thread(
        ollama.chat,
        model="llama3:8b",
        messages=[{"role": "user", "content": full_prompt}],
    )
    return response["message"]["content"]


@app.post("/generate/")
async def generate_text(request: QueryRequest):
    try:
        response = await generate_response(request.prompt, request.max_tokens)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
