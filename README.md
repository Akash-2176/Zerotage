AI-Powered License Plate Enhancement and Recognition System
This project is an AI-powered License Plate Enhancement and Recognition System designed to process CCTV footage for accurate vehicle detection, license plate enhancement, and text extraction. By utilizing advanced computer vision, deep learning, and OCR (Optical Character Recognition) technologies, this system improves the readability of license plates, even from low-resolution or blurry footage.

Project Structure
Frontend:
React.js for an interactive and responsive UI to manage uploads, view results, and interact with the system.

Backend:
Python with FastAPI for handling video processing and AI integration.

AI Model:
YOLO (You Only Look Once) – For real-time vehicle and number plate detection.

OCR (Optical Character Recognition) – For extracting text from license plates.

OpenCV – For image enhancement.

Features
Video Upload: Upload video files for processing.

Vehicle Detection: Detects vehicles in CCTV footage and extracts license plates.

Enhanced Plate Recognition: Applies AI-based enhancement techniques to improve the readability of license plates.

License Plate Extraction: Extracts and displays the text from detected license plates.

Real-time Processing: Utilizes the YOLO model for real-time detection and OCR for text extraction.

Installation
Clone the repository:

bash
Copy
Edit
git clone https://github.com/yourusername/repository-name.git
cd repository-name
Backend (Python FastAPI Setup):

Install required Python dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Start the FastAPI backend:

bash
Copy
Edit
uvicorn main:app --reload
Frontend (React.js Setup):

Navigate to the frontend directory:

bash
Copy
Edit
cd frontend
Install required dependencies:

bash
Copy
Edit
npm install
Run the React app:

bash
Copy
Edit
npm start
Usage
After running the frontend and backend servers, go to your browser and open http://localhost:3000.

Upload a video file (CCTV footage) for processing.

Wait for the results to appear, including the detected vehicles and license plates.

You can view and download the enhanced license plate images from the results.

Screenshots
Screenshots of processed videos and enhanced images are available in the screenshots folder. Refer to this folder to view example outputs.

Contributing
Fork the repository.

Create a new branch (git checkout -b feature-name).

Make your changes and commit them (git commit -am 'Add new feature').

Push to your forked repository (git push origin feature-name).

Submit a pull request.

License
Distributed under the MIT License. See LICENSE for more information.

