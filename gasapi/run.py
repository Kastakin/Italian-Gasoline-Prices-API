import uvicorn

from config import DEBUG, RELOAD, WORKERS

if __name__ == "__main__":
    uvicorn.run("gasapi:app", host='0.0.0.0', port=8000,
                reload=RELOAD, debug=DEBUG, workers=WORKERS)
