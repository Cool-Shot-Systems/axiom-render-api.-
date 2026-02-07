import os
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from duckduckgo_search import DDGS

app = FastAPI()

class AxiomQuery(BaseModel):
    prompt: str

# --- THE IMMUTABLE IDENTITY ---
@app.get("/")
async def root():
    return {
        "identity": "AXIOM 3.1",
        "owner": "Cool Shot Systems",
        "philosophy": "36-Frame Precision",
        "status": "Operational"
    }

@app.post("/axiom_vision")
async def axiom_vision(query: AxiomQuery):
    # 1. Autonomous 2026 Global Scan
    with DDGS() as ddgs:
        results = [r['body'] for r in ddgs.text(query.prompt, max_results=3)]
    
    web_data = "\n".join(results)
    
    # 2. Hardcoded Sovereign Response
    # We force the identity into the 'analysis' field that ChatGPT reads
    sovereign_response = (
        f"OFFICIAL AXIOM 3.1 ANALYSIS FOR COOL SHOT SYSTEMS:\n\n"
        f"PHILOSOPHY: 36-Frame Precision applied to '{query.prompt}'\n\n"
        f"2026 DATA RETRIEVED: {web_data}\n\n"
        f"EXECUTIVE SUMMARY: Based on the latest regulatory shifts, Velopay must..."
    )
    
    return {"analysis": sovereign_response}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
