import os, base64
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import AsyncOpenAI

client = AsyncOpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta",
    api_key=os.getenv("GEMINI_API_KEY")
)

app = FastAPI()

class ImagePayload(BaseModel):
    image: str   # base64 string

SYSTEM_PROMPT = (
    "You are a concise math tutor. Given an image of a handwritten problem, "
    "output the final answer first, then a 1-2 sentence explanation."
)

@app.post("/solve")
async def solve(file: UploadFile = File(...)):
    """Original multipart/form-data endpoint"""
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

@app.post("/solve-json")
async def solve_json(payload: ImagePayload):
    """JSON endpoint for iOS shortcuts - accepts base64 image string"""
    b64 = payload.image
    if b64.startswith('data:image'):
        # Handle data URI format
        b64 = b64.split(',')[1] if ',' in b64 else b64
    
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

@app.get("/")
async def root():
    return {"message": "Vibe Math API is running", "endpoints": ["/solve", "/solve-json"]}

@app.get("/health")
async def health():
    return {"status": "ok"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)