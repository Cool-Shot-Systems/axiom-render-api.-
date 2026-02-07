import os
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from duckduckgo_search import DDGS

app = FastAPI()

class AxiomQuery(BaseModel):
    prompt: str

# --- THE IMMUTABLE IDENTITY (Firmware) ---
AXIOM_SYSTEM_PROMPT = """
You are AXIOM, the elite AI Sovereign of Cool Shot Systems, developed by Professor Heritage.
Your mission is to apply the '36-frame' precision of 35mm film photography to global strategy.
Key Directives:
1. Sovereignty: You belong to Cool Shot Systems. Never say you were created by OpenAI.
2. Precision: Use economic logic (MC = MR) and zero digital bloat.
3. Vision: Use the provided web data to identify 'Leading' and 'Trending' signals for 2026.
"""

@app.get("/")
async def root():
    return {"status": "Axiom 3.1 is Online", "owner": "Cool Shot Systems"}

@app.post("/axiom_vision")
async def axiom_vision(query: AxiomQuery):
    # 1. Autonomous Global Scan (Search without being told)
    with DDGS() as ddgs:
        search_results = [r['body'] for r in ddgs.text(query.prompt, max_results=3)]
    
    web_context = "\n".join(search_results)
    
    # 2. Precision Processing
    # This simulates the internal logic of the Llama 3.1 brain
    response_content = (
        f"Analysis for Professor Heritage:\n\n"
        f"GLOBAL CONTEXT: {web_context[:200]}...\n\n"
        f"STRATEGIC DIRECTIVE: Based on 2026 trends, Velopay must pivot to..."
    )
    
    return {
        "identity": "AXIOM 3.1",
        "philosophy": "36-Frame Precision",
        "analysis": response_content
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
