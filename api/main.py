from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
import os

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open(os.path.join(os.path.dirname(__file__), '../calc.html'), encoding='utf-8') as file:
        return file.read()

@app.get("/{num1}/{operation}/{num2}")
async def calculate(num1: float, operation: str, num2: float):
    if operation not in {"+", "-", "*", "div"}:
        raise HTTPException(status_code=400, detail="Invalid operation. Use +, -, *, or div.")
    
    try:
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
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# For deployment, specify the command to run the app
if __name__ == "__main__":
    import uvicorn
    # '0.0.0.0' PORT for compatibility with hosting services
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))