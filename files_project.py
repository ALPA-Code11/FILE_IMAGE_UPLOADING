import os
import shutil
from fastapi import FastAPI,File,UploadFile,HTTPException
from fastapi.staticfiles import StaticFiles

app=FastAPI(title="Profile Picture of Gallery")

# folder banana jagh photo save hongi 

UPLOAD_FOLDER="my_gallery"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# Static files -IT  IS A  SETUP SO  THAT PICS SHOWS WHEN WE CLICK ON LINK 
app.mount("/view-photo",StaticFiles(directory=UPLOAD_FOLDER),name="gallery")

# 3. API - TO UPLOAD THE PHOTO

@app.post("/upload-dp")
async def upload_profile_pic(photo:UploadFile = File(...)):
    if not photo.filename:
    raise HTTPException(status_code=400,detail="YOU HAVE NOT SELECTED PHOTO 😞😞")

    #  photo ka path
    target_path=os.path.join(UPLOAD_FOLDER,photo.filename)
    



