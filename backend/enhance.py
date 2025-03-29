import os
import glob
import shutil
import subprocess
from preprocess import preprocess_images
from ocr import extract_text

# Directories
PREPROCESS_DIR = "preprocess/"
LR_DIR = "ESRGAN/LR/"
RESULTS_DIR = "ESRGAN/results/"
ENHANCED_DIR = "enhanced/"
OUTPUT_TEXT_DIR = "output_texts/"

# Ensure necessary directories exist
os.makedirs(LR_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)
os.makedirs(ENHANCED_DIR, exist_ok=True)
os.makedirs(OUTPUT_TEXT_DIR, exist_ok=True)

# Step 1: Move preprocessed images to ESRGAN/LR/
for image_path in glob.glob(os.path.join(PREPROCESS_DIR, "*.png")):
    shutil.move(image_path, LR_DIR)
    print(f"Moved {image_path} to {LR_DIR}")

# Step 2: Run ESRGAN (test.py)
print("Running ESRGAN...")
subprocess.run(["python", "ESRGAN/test.py"], check=True)
print("ESRGAN enhancement completed.")

# Step 3: Move enhanced images to enhanced/
for enhanced_image in glob.glob(os.path.join(RESULTS_DIR, "*.png")):
    shutil.move(enhanced_image, ENHANCED_DIR)
    print(f"Moved {enhanced_image} to {ENHANCED_DIR}")

# Step 4: Clear ESRGAN/LR/ and ESRGAN/results/
for file in glob.glob(os.path.join(LR_DIR, "*.png")):
    os.remove(file)
for file in glob.glob(os.path.join(RESULTS_DIR, "*.png")):
    os.remove(file)
print("Cleared ESRGAN temporary files.")

# Step 5: Extract text from enhanced images
for enhanced_image in glob.glob(os.path.join(ENHANCED_DIR, "*.png")):
    text = extract_text(enhanced_image)
    output_text_file = os.path.join(OUTPUT_TEXT_DIR, os.path.basename(enhanced_image).replace(".png", ".txt"))
    
    with open(output_text_file, "w") as f:
        f.write(text)
    print(f"Extracted text saved: {output_text_file}")

print("Enhancement and OCR process completed!")