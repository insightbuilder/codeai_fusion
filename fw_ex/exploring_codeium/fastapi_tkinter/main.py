import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import os

app = FastAPI()

# Load problems from JSON
def load_problems():
    with open('problems.json', 'r') as f:
        return json.load(f)

class Solution(BaseModel):
    problem_id: int
    code: str

@app.get("/problems")
async def get_problems():
    return load_problems()

@app.get("/problem/{problem_id}")
async def get_problem(problem_id: int):
    problems = load_problems()
    problem = next((p for p in problems if p['id'] == problem_id), None)
    if problem is None:
        raise HTTPException(status_code=404, detail="Problem not found")
    return problem

@app.post("/save_solution")
async def save_solution(solution: Solution):
    # Ensure solutions directory exists
    os.makedirs('solutions', exist_ok=True)
    
    # Save solution to a file
    filename = f"solutions/problem_{solution.problem_id}_solution.py"
    with open(filename, 'w') as f:
        f.write(solution.code)
    
    return {"message": "Solution saved successfully", "filename": filename}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
