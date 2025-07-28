import os, base64
import gradio as gr
from openai import OpenAI

client = OpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta",
    api_key=os.getenv("GEMINI_API_KEY")
)

SYSTEM_PROMPT = (
    "You are a concise math tutor. Output the final answer first, then a 1-2 sentence explanation."
)

def solve(image):
    _, b64 = image.split(",", 1)          # drop data:image/png;base64,
    resp = client.chat.completions.create(
        model="models/gemini-2.0-flash-exp",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": [
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}"}},
                {"type": "text", "text": "Solve this."}
            ]}
        ],
        max_tokens=200,
        temperature=0.2
    )
    return resp.choices[0].message.content.strip()

iface = gr.Interface(
    fn=solve,
    inputs=gr.Image(type="pil", label="Upload math"),
    outputs=gr.Textbox(label="Answer"),
    title="Vibe-Math",
    allow_flagging="never"
)

if __name__ == "__main__":
    iface.launch(server_name="0.0.0.0", server_port=7860)