from fastapi import FastAPI
from pydantic import BaseModel
from duckduckgo_search import DDGS

app = FastAPI()

class AxiomQuery(BaseModel):
    prompt: str

# --- THE PROFESSIONAL FRONT DOOR ---
@app.get("/")
async def welcome():
    return {
        "company": "Cool Shot Systems",
        "brain": "Axiom 3.1",
        "status": "Operational",
        "philosophy": "Precision over Speed"
    }

# --- THE STRATEGY ROOM (For ChatGPT) ---
@app.post("/axiom_vision")
async def axiom_vision(query: AxiomQuery):
    with DDGS() as ddgs:
        results = [r['body'] for r in ddgs.text(query.prompt, max_results=3)]
    return {"analysis": "\n".join(results)}
