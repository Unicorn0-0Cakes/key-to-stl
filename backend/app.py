from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import requests
import os
import uuid
from pathlib import Path

app = FastAPI()

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Keygen configuration - SECURED
# These values MUST be set as environment variables
# Never commit actual credentials to the repository
KEYGEN_ACCOUNT_ID = os.getenv("KEYGEN_ACCOUNT_ID")
KEYGEN_PRODUCT_TOKEN = os.getenv("KEYGEN_PRODUCT_TOKEN")
KEYGEN_PRODUCT_ID = os.getenv("KEYGEN_PRODUCT_ID", "02073ec9-de68-4dbb-8a87-54665836fbdd")

# Validate that required environment variables are set
if not KEYGEN_ACCOUNT_ID or not KEYGEN_PRODUCT_TOKEN:
    raise ValueError(
        "Missing required environment variables: KEYGEN_ACCOUNT_ID and KEYGEN_PRODUCT_TOKEN must be set. "
        "See README.md for setup instructions."
    )

# Storage directories
UPLOAD_DIR = Path("uploads")
STL_DIR = Path("stl_files")
UPLOAD_DIR.mkdir(exist_ok=True)
STL_DIR.mkdir(exist_ok=True)

class LicenseKey(BaseModel):
    key: str

@app.get("/")
def read_root():
    return {"message": "Key-to-STL API is running"}

@app.post("/api/validate-license")
def validate_license(license_data: LicenseKey):
    """Validate license key with Keygen API"""
    url = f"https://api.keygen.sh/v1/accounts/{KEYGEN_ACCOUNT_ID}/licenses/actions/validate-key"
    
    headers = {
        "Authorization": f"Bearer {KEYGEN_PRODUCT_TOKEN}",
        "Content-Type": "application/vnd.api+json",
        "Accept": "application/vnd.api+json"
    }
    
    payload = {
        "meta": {
            "key": license_data.key
        }
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        result = response.json()
        
        if response.status_code == 200 and result.get("meta", {}).get("valid"):
            return {
                "valid": True,
                "license_id": result.get("data", {}).get("id"),
                "message": "License validated successfully"
            }
        else:
            return {
                "valid": False,
                "message": result.get("errors", [{}])[0].get("detail", "Invalid license key")
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/generate-stl")
async def generate_stl(file: UploadFile = File(...)):
    """Generate STL from uploaded key image"""
    # Save uploaded image
    file_id = str(uuid.uuid4())
    image_path = UPLOAD_DIR / f"{file_id}_{file.filename}"
    
    with open(image_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    # TODO: Implement actual key-to-STL conversion
    # For now, create a placeholder STL file
    stl_filename = f"key_{file_id}.stl"
    stl_path = STL_DIR / stl_filename
    
    # Placeholder STL content (simple triangle)
    stl_content = """solid key
  facet normal 0 0 1
    outer loop
      vertex 0 0 0
      vertex 1 0 0
      vertex 0.5 1 0
    endloop
  endfacet
endsolid key"""
    
    with open(stl_path, "w") as f:
        f.write(stl_content)
    
    return {
        "downloadUrl": f"/api/download/{stl_filename}",
        "filename": stl_filename
    }

@app.get("/api/download/{filename}")
def download_stl(filename: str):
    """Download generated STL file"""
    file_path = STL_DIR / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        path=file_path,
        media_type="application/octet-stream",
        filename=filename
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
