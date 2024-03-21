from fastapi import FastAPI, File, UploadFile
import os
import logging
from typing import List

app = FastAPI()

UPLOAD_DIR = "./received-images"

log_file = "http_server_log.txt"
logging.basicConfig(filename=log_file, level=logging.INFO)


@app.post("/upload/")
async def upload_files(files: List[UploadFile] = File(...)):
    if not files:
        logging.error("No files received")
    for uploaded_file in files:
        file_path = os.path.join(UPLOAD_DIR, uploaded_file.filename)
        with open(file_path, "wb") as file_object:
            file_object.write(await uploaded_file.read())
            logging.info("A file is created.")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
