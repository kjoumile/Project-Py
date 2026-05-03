from fastapi import FastAPI

app = FastAPI(title="Study Tasks API")


@app.get("/")
def read_root():
    return {"message": "Study Tasks API is running"}
