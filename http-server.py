from fastapi import FastAPI, File, UploadFile
import os
import logging
from typing import List

app = FastAPI()

UPLOAD_DIR = "/home/haproxy-backend1/received-images" 

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.post("/upload/")
async def upload_files(files: List[UploadFile] = File(...)):
    if not files:
        logger.error("No files received")
        return {"message": "No files received"}

    for uploaded_file in files:
        file_path = os.path.join(UPLOAD_DIR, uploaded_file.filename)
        with open(file_path, "wb") as file_object:
            file_object.write(await uploaded_file.read())
            logger.info(f"Received file: {uploaded_file.filename}")

    return {"message": "Files uploaded successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
