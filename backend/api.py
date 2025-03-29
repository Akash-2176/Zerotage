import os
import shutil
import subprocess
import logging
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from fastapi.responses import JSONResponse

# Initialize FastAPI app
app = FastAPI()

# Allow all origins for CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Setup logging
logging.basicConfig(level=logging.INFO)

# Define directories
BASE_DIR = Path(__file__).parent
UPLOAD_DIR = BASE_DIR / "uploads"
OUTPUT_DIR = BASE_DIR / "results"
PREPROCESS_DIR = BASE_DIR / "preprocess"
OCR_RESULTS_DIR = BASE_DIR / "ocr_results"

# Create directories if not exist
for directory in [UPLOAD_DIR, OUTPUT_DIR, PREPROCESS_DIR, OCR_RESULTS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Mount static directories
app.mount("/static/results", StaticFiles(directory=OUTPUT_DIR, html=False), name="results")
app.mount("/static/preprocess", StaticFiles(directory=PREPROCESS_DIR, html=False), name="preprocess")

@app.post("/process_video/")
async def process_video(video: UploadFile = File(...)):
    """Upload video and process it through detect.py and ocr.py"""
    
    video_path = UPLOAD_DIR / video.filename
    try:
        # Save uploaded video
        with video_path.open("wb") as buffer:
            shutil.copyfileobj(video.file, buffer)
        logging.info(f"Saved video to {video_path}")

        # Run detect.py inside virtual environment
        detect_command = ["venv/Scripts/python", "detect.py", str(video_path)]
        detect_result = subprocess.run(detect_command, capture_output=True, text=True)

        if detect_result.returncode != 0:
            logging.error(f"detect.py failed: {detect_result.stderr}")
            raise HTTPException(status_code=500, detail={"error": "Error running detect.py", "details": detect_result.stderr})

        # Run ocr.py inside virtual environment
        ocr_command = ["venv/Scripts/python", "ocr.py"]
        ocr_result = subprocess.run(ocr_command, capture_output=True, text=True)

        if ocr_result.returncode != 0:
            logging.error(f"ocr.py failed: {ocr_result.stderr}")
            raise HTTPException(status_code=500, detail={"error": "Error running ocr.py", "details": ocr_result.stderr})

        # Base URL for serving static files
        BASE_URL = "http://127.0.0.1:8000"

        # Collect results
        vehicle_images = [f"{BASE_URL}/static/results/{f.name}" for f in OUTPUT_DIR.iterdir() if f.name.startswith("vehicle")]
        plate_images = [f"{BASE_URL}/static/results/{f.name}" for f in OUTPUT_DIR.iterdir() if f.name.startswith("plate")]
        preprocessed_images = [f"{BASE_URL}/static/preprocess/{f.name}" for f in PREPROCESS_DIR.iterdir()]
        ocr_texts = {}

        for filename in OCR_RESULTS_DIR.iterdir():
            with filename.open("r") as f:
                ocr_texts[str(filename.name)] = f.read().strip()

        # Prepare response
        response_data = {
            "vehicles": vehicle_images,
            "plates": plate_images,
            "preprocessed_plates": preprocessed_images,
            "ocr_results": ocr_texts
        }

        response = JSONResponse(content=response_data)
        response.headers["Access-Control-Allow-Origin"] = "*"
        return response

    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
