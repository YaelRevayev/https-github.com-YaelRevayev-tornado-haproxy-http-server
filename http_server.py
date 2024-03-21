from fastapi import FastAPI, File, UploadFile
import os
import logging
from typing import List
from datetime import datetime

app = FastAPI()

UPLOAD_DIR = "./received-images"

log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)


error_logger = logging.getLogger("error_logger")
error_logger.setLevel(logging.ERROR)
error_handler = logging.FileHandler(os.path.join(log_dir, "error_logs.txt"))
error_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
error_handler.setFormatter(error_formatter)
error_logger.addHandler(error_handler)


info_logger = logging.getLogger("info_logger")
info_logger.setLevel(logging.INFO)
info_handler = logging.FileHandler(
    os.path.join(log_dir, f"server_logs_{datetime.now().strftime('%Y-%m-%d')}.txt")
)
info_formatter = logging.Formatter(
    "%(asctime)s - %(filename)s - %(levelname)s - %(message)s"
)
info_handler.setFormatter(info_formatter)
info_logger.addHandler(info_handler)


@app.post("/upload/")
async def upload_files(files: List[UploadFile] = File(...)):
    if not files:
        error_logger.error("No files received")
    for uploaded_file in files:
        file_path = os.path.join(UPLOAD_DIR, uploaded_file.filename)
        with open(file_path, "wb") as file_object:
            file_object.write(await uploaded_file.read())
            info_logger.info("A file is created.")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
