import os
import shutil
from uuid import uuid4
from fastapi import UploadFile



def save_image_file(image: UploadFile) -> str:
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    ext = image.filename.split(".")[-1]
    filename = f"{uuid4().hex}.{ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    return f"/static/uploads/{filename}"
