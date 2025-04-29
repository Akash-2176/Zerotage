import os
import cv2
import numpy as np
import argparse
import subprocess
import sys
from ultralytics import YOLO
from inference_sdk import InferenceHTTPClient
from preprocess import preprocess_images  # Import preprocessing function

# Roboflow API Client
CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="MdJE2LoFn7C7dozwvfkA"
)

# Load YOLO model for vehicle detection
vehicle_model = YOLO("models/yolov8n.pt")

# Directories
UPLOAD_DIR = "uploads"
OUTPUT_DIR = "results"
PREPROCESS_DIR = "preprocess"
OCR_RESULTS_DIR = "ocr_results"
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(PREPROCESS_DIR, exist_ok=True)
os.makedirs(OCR_RESULTS_DIR, exist_ok=True)

CAR_CLASS_ID = 2  # COCO class ID for "car"
detected_plates = set()
detected_vehicles = []

DISTANCE_THRESHOLD = 50  # Pixels

def is_duplicate_plate(plate_crop):
    """Check if the plate is already detected using hashing."""
    plate_hash = hash(plate_crop.tobytes())
    if plate_hash in detected_plates:
        return True
    detected_plates.add(plate_hash)
    return False

def is_new_vehicle(center_x, center_y):
    """Check if the detected vehicle is significantly different from previous ones."""
    for prev_x, prev_y in detected_vehicles:
        if np.sqrt((center_x - prev_x) ** 2 + (center_y - prev_y) ** 2) < DISTANCE_THRESHOLD:
            return False
    detected_vehicles.append((center_x, center_y))
    return True

def process_video(video_path):
    print(f"📂 Processing video: {video_path}")

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("❌ Error: Could not open video.")
        return

    frame_rate = int(cap.get(cv2.CAP_PROP_FPS))
    frames_to_skip = frame_rate
    frame_count = 0

    plate_filenames = []  # Store detected plate file paths for batch processing
    vehicle_plate_mapping = []  # List to store vehicle and plate mapping

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        if frame_count % frames_to_skip != 0:
            continue

        print(f"✅ Processing frame {frame_count}")

        # Detect vehicles
        vehicle_results = vehicle_model(frame)
        vehicle_boxes = [
            box for box, cls in zip(vehicle_results[0].boxes.xyxy.cpu().numpy(), 
                                    vehicle_results[0].boxes.cls.cpu().numpy())
            if int(cls) == CAR_CLASS_ID
        ]

        if not vehicle_boxes:
            continue

        print(f"🚗 {len(vehicle_boxes)} car(s) detected, checking for plates...")

        for i, box in enumerate(vehicle_boxes):
            x1, y1, x2, y2 = map(int, box[:4])
            center_x, center_y = (x1 + x2) // 2, (y1 + y2) // 2

            if not is_new_vehicle(center_x, center_y):
                continue

            vehicle_crop = frame[y1:y2, x1:x2]
            vehicle_path = f"{OUTPUT_DIR}/vehicle_{frame_count}_{i}.jpg"
            cv2.imwrite(vehicle_path, vehicle_crop)

            try:
                result = CLIENT.infer(vehicle_path, model_id="license-plate-recognition-rxg4e/6")
            except Exception as e:
                print(f"⚠️ Roboflow API error: {e}")
                continue

            if not result['predictions']:
                os.remove(vehicle_path)
                continue

            for j, plate in enumerate(result['predictions']):
                px1, py1, px2, py2 = map(int, [plate['x'] - plate['width'] // 2, 
                                               plate['y'] - plate['height'] // 2, 
                                               plate['x'] + plate['width'] // 2, 
                                               plate['y'] + plate['height'] // 2])
                
                px1, py1 = max(px1, 0), max(py1, 0)
                px2, py2 = min(px2, vehicle_crop.shape[1]), min(py2, vehicle_crop.shape[0])

                plate_crop = vehicle_crop[py1:py2, px1:px2]

                if plate_crop.size == 0 or is_duplicate_plate(plate_crop):
                    continue

                plate_filename = f"{OUTPUT_DIR}/plate_{frame_count}_{i}_{j}.png"
                cv2.imwrite(plate_filename, plate_crop)
                plate_filenames.append(plate_filename)

                # Map the vehicle to the detected plate
                vehicle_plate_mapping.append({
                    "vehicle_id": f"vehicle_{frame_count}_{i}",
                    "plate_filename": plate_filename,
                    "vehicle_coordinates": (x1, y1, x2, y2),
                    "plate_coordinates": (px1, py1, px2, py2),
                    "frame_number": frame_count,
                    "plate_text": plate.get("label", "Unknown")  # Assuming OCR result returns label
                })

                print(f"✅ Saved plate: {plate_filename} for vehicle {frame_count}_{i}")

    cap.release()

    # Process detected plates
    if plate_filenames:
        print("🔄 Preprocessing detected license plates...")
        preprocess_images(plate_filenames, PREPROCESS_DIR)

        print("🚀 Running OCR on preprocessed images...")
        subprocess.run([sys.executable, "ocr.py"])  # Automatically executes OCR

    print("🎉 Detection & OCR process complete!")

    # Optionally save the vehicle-plate mapping for later use
    with open(f"{OUTPUT_DIR}/vehicle_plate_mapping.json", "w") as f:
        import json
        json.dump(vehicle_plate_mapping, f, indent=4)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="License Plate Detection from Video")
    parser.add_argument("video_path", type=str, help="Path to the video file")
    args = parser.parse_args()

    process_video(args.video_path)
