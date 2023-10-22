from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import json
from cmd.main import run_conversation

app = FastAPI()

class EvaluationInput(BaseModel):
    user_input: str

class EvaluationOutput(BaseModel):
    evaluation_results: list

@app.post("/evaluate/", response_model=EvaluationOutput)
async def evaluate_claims(data: EvaluationInput):
    user_input = data.user_input
    evaluation_results = run_conversation(user_input)
    return {"evaluation_results": evaluation_results}