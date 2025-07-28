import os, base64
from fastapi import FastAPI
from pydantic import BaseModel
from openai import AsyncOpenAI

client = AsyncOpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta",
    api_key=os.getenv("GEMINI_API_KEY")
)

app = FastAPI()

class ImagePayload(BaseModel):
    image: str   # base64 string

@app.post("/solve")
async def solve(payload: ImagePayload):
    data_uri = f"data:image/jpeg;base64,{payload.image}"
    resp = await client.chat.completions.create(
        model="models/gemini-2.0-flash-exp",
        messages=[
            {"role": "user", "content": [
                {"type": "image_url", "image_url": {"url": data_uri}},
                {"type": "text", "text": "Solve this."}
            ]}
        ],
        max_tokens=200,
        temperature=0.2
    )
    return {"answer": resp.choices[0].message.content.strip()}