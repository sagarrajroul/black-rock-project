from fastapi import FastAPI

app = FastAPI(app_name="FastAPI app for Black Rock", version="1.0.0")


@app.get("/")
def root():
    return {"message": "Hello, World!"}