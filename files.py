import os
import shutil
from typing import List
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="My File Upload API")

# ==========================================================
# STEP 1: Ensure Uploads Folder Exists
# ==========================================================
UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# ==========================================================
# STEP 2: Static Files Setup
# Isse hum browser mein direct file access kar payenge
# URL: http://127.0.0.1:8000/files/your_file_name.png
# ==========================================================
app.mount("/files", StaticFiles(directory=UPLOAD_DIR), name="files")


# ==========================================================
# STEP 3: Home Route (Just to check if server is running)
# ==========================================================
@app.get("/")
def home():
    return {"message": "File Upload API is Running Successfully!"}


# ==========================================================
# STEP 4: Single File Upload API
# ==========================================================
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    filename = file.filename
    
    # Check agar user ne bina file select kiye send kar diya
    if not filename:
        raise HTTPException(status_code=400, detail="File not selected. Please upload a file.")
    
    # File ka poora path banana (e.g., uploads/photo.jpg)
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    # File ko read karke server par save karna
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # File ka size nikalna (Optional - dekhne mein accha lagta hai)
    file_size_kb = os.path.getsize(file_path) / 1024
    
    return {
        "message": "File Uploaded successfully",
        "fileName": filename,
        "fileSize": f"{round(file_size_kb, 2)} KB",
        "file_url": f"http://127.0.0.1:8000/files/{filename}"
    }


# ==========================================================
# STEP 5: Multiple Files Upload API (Bonus)
# ==========================================================
# @app.post("/upload-multiple")
# async def upload_multiple_files(files: List[UploadFile] = File(...)):
#     uploaded_filenames = []
    
#     for file in files:
#         if file.filename:
#             file_path = os.path.join(UPLOAD_DIR, file.filename)
#             with open(file_path, "wb") as buffer:
#                 shutil.copyfileobj(file.file, buffer)
#             uploaded_filenames.append(file.filename)
            
#     return {
#         "message": f"Successfully uploaded {len(uploaded_filenames)} files",
#         "fileNames": uploaded_filenames
#     }


# ==========================================================
# STEP 6: Get File URL API
# ==========================================================
@app.get("/get-file/{filename}")
def get_file(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    # Check karna ki file folder mein hai ya nahi
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found in the server")
        
    return {"file_url": f"http://127.0.0.1:8000/files/{filename}"}