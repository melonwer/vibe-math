import base64, os, json, httpx
from fastapi import FastAPI, UploadFile, File
from openai import AsyncOpenAI
from fastapi.middleware.cors import CORSMiddleware


client = AsyncOpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta",
    api_key="GEMINI_API_KEY" 
)

app = FastAPI()

SYSTEM_PROMPT = (
    "You are a concise math tutor. Given an image of a handwritten problem, "
    "output the final answer first, then a 1-2 sentence explanation."
)

@app.post("/solve")
async def solve(file: UploadFile = File(...)):
    img_bytes = await file.read()
    b64 = base64.b64encode(img_bytes).decode()
    data_uri = f"data:image/png;base64,{b64}"
    resp = await client.chat.completions.create(
        model="models/gemini-2.0-flash-exp",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": [
                {"type": "image_url", "image_url": {"url": data_uri}},
                {"type": "text", "text": "Solve this."}
            ]}
        ],
        max_tokens=200,
        temperature=0.2
    )
    answer = resp.choices[0].message.content.strip()
    return {"answer": answer}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)