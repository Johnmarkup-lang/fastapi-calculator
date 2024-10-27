from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
import os
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open(os.path.join(os.path.dirname(__file__), 'calc.html'), encoding='utf-8') as file:
        return file.read()

@app.get("/{num1}/{operation}/{num2}")
async def calculate(num1: float, operation: str, num2: float):
    if operation not in {"+", "-", "*", "div"}:  # Use 'div' instead of '/'
        raise HTTPException(status_code=400, detail="Invalid operation. Use +, -, *, or div.")
    
    if operation == "+":
        result = num1 + num2
    elif operation == "-":
        result = num1 - num2
    elif operation == "*":
        result = num1 * num2
    elif operation == "div":
        if num2 == 0:
            raise HTTPException(status_code=400, detail="Division by zero is not allowed.")
        result = num1 / num2

    return {"result": result}
