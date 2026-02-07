import os
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from huggingface_hub import hf_hub_download
from llama_cpp import Llama
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="Axiom 3.1 Sovereign API")

# --- CONFIGURATION ---
REPO_ID = "CoolShotSystems/Axiom-3.1-Sovereign"
FILENAME = "Meta-Llama-3.1-8B.Q4_K_M.gguf"

# Global variable for the model
axiom_model = None

@app.on_event("startup")
def load_brain():
    """Downloads and loads the AI model when the server starts."""
    global axiom_model
    print("📡 CONNECTING TO VAULT... Downloading Sovereign Model...")
    
    try:
        # Download the model from Hugging Face
        model_path = hf_hub_download(
            repo_id=REPO_ID,
            filename=FILENAME,
            token=os.environ.get("HF_TOKEN")
        )
        print(f"✅ DOWNLOAD COMPLETE. Path: {model_path}")
        
        print("🧠 WAKING UP AXIOM (Loading into RAM)...")
        # Load the model into memory
        axiom_model = Llama(
            model_path=model_path,
            n_ctx=2048,
            n_threads=4, 
            verbose=False
        )
        print("🚀 AXIOM 3.1 IS ONLINE AND READY.")
        
    except Exception as e:
        print(f"❌ CRITICAL FAILURE: {e}")

# --- DATA MODELS ---
class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: list[Message]

# --- ENDPOINTS ---
@app.get("/")
def home():
    if axiom_model:
        return {"status": "Axiom 3.1 Online", "message": "System Operational"}
    return {"status": "Loading...", "message": "Brain is still waking up"}

@app.post("/v1/chat/completions")
async def chat(request: ChatRequest):
    if not axiom_model:
        raise HTTPException(status_code=503, detail="Axiom is still waking up.")

    # Format the prompt for Llama 3
    prompt = "<|begin_of_text|>"
    for msg in request.messages:
        prompt += f"<|start_header_id|>{msg.role}<|end_header_id|>\n\n{msg.content}<|eot_id|>"
    prompt += "<|start_header_id|>assistant<|end_header_id|>\n\n"

    # Generate response
    output = axiom_model(
        prompt,
        max_tokens=512,
        stop=["<|eot_id|>", "<|end_of_text|>"],
        echo=False,
        temperature=0.7
    )

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
