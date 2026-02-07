import os
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from huggingface_hub import hf_hub_download
from llama_cpp import Llama
from dotenv import load_dotenv

# Load environment variables (HF_TOKEN)
load_dotenv()

app = FastAPI(title="Axiom 3.1 Sovereign API")

# --- CONFIGURATION ---
REPO_ID = "CoolShotSystems/Axiom-3.1-Sovereign"
FILENAME = "Meta-Llama-3.1-8B.Q4_K_M.gguf"

# Global variable to hold the model in RAM
axiom_model = None

@app.on_event("startup")
def load_brain():
    """Downloads and loads the AI model when the server starts."""
    global axiom_model
    print("📡 CONNECTING TO VAULT... Downloading Sovereign Model...")
    
    try:
        model_path = hf_hub_download(
            repo_id=REPO_ID,
            filename=FILENAME,
            token=os.environ.get("HF_TOKEN") # Pulls from Render Env Vars
        )
        print(f"✅ DOWNLOAD COMPLETE. Path: {model_path}")
        
        print("🧠 WAKING UP AXIOM (Loading into RAM)...")
        # n_ctx=2048 matches your training. n_threads=4 for speed.
        axiom_model = Llama(
            model_path=model_path,
            n_ctx=2048,
            n_threads=4, 
            verbose=False
        )
        print("🚀 AXIOM 3.1 IS ONLINE AND READY.")
        
    except Exception as e:
        print(f"❌ CRITICAL FAILURE: {e}")
        # We don't raise error here so the server can still start and show logs

# --- DATA MODELS ---
class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: list[Message]

# --- ENDPOINTS ---
@app.get("/")
def health_check():
    if axiom_model:
        return {"status": "online", "model": "Axiom 3.1 Sovereign"}
    return {"status": "offline", "error": "Model failed to load"}

@app.post("/v1/chat/completions")
async def chat(request: ChatRequest):
    """The OpenAI-compatible endpoint for your Custom GPT."""
    if not axiom_model:
        raise HTTPException(status_code=503, detail="Axiom is still waking up.")

    # 1. Format the Prompt (Llama 3 Style)
    prompt = "<|begin_of_text|>"
    for msg in request.messages:
        prompt += f"<|start_header_id|>{msg.role}<|end_header_id|>\n\n{msg.content}<|eot_id|>"
    prompt += "<|start_header_id|>assistant<|end_header_id|>\n\n"

    # 2. Generate Response
    output = axiom_model(
        prompt,
        max_tokens=512,
        stop=["<|eot_id|>", "<|end_of_text|>"],
        echo=False,
        temperature=0.7
    )

    # 3. Return JSON
    return {
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": output['choices'][0]['text']
                }
            }
        ]
        }
