from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from app.model import segment_image, __version__ as model_version

app = FastAPI()

class SegmentationResult(BaseModel):
    mask: str  # Base64 encoded mask image

@app.get("/")
def home():
    return {"health_check": "OK", "model_version": model_version}

@app.post("/segment", response_model=SegmentationResult)
async def segment(file: UploadFile = File(...)):
    mask_base64 = await segment_image(file)
    return {"mask": mask_base64}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
