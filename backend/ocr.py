import os
import cv2
import pytesseract
import numpy as np
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Set Tesseract path if needed
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

PREPROCESS_DIR = "preprocess"
OCR_RESULTS_DIR = "ocr_results"
os.makedirs(OCR_RESULTS_DIR, exist_ok=True)

def enhance_image(img):
    """Enhance image for better OCR results."""
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Resize image for better OCR accuracy
    scale_factor = 400 / gray.shape[1]
    gray = cv2.resize(gray, (400, int(gray.shape[0] * scale_factor)))

    # Apply GaussianBlur for noise reduction
    gray = cv2.GaussianBlur(gray, (3, 3), 0)

    # Apply adaptive thresholding
    processed_img = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )

    # Sharpening for better OCR
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    processed_img = cv2.filter2D(processed_img, -1, kernel)

    return processed_img

def extract_text(image_path):
    """Perform OCR on the enhanced image to extract text."""
    img = cv2.imread(image_path)

    if img is None:
        print(f"❌ Error: Could not load {image_path}")
        return ""

    processed_img = enhance_image(img)

    # Extract text using Tesseract OCR
    text = pytesseract.image_to_string(processed_img, config="--psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")

    return text.strip()

def process_ocr():
    """Process all images in the preprocess directory after preprocessing is done."""
    print("📄 Waiting for preprocessing to complete...")

    # Ensure preprocessing is completed
    while not os.listdir(PREPROCESS_DIR):  # Wait until files exist in preprocess dir
        pass

    print("✅ Preprocessing done! Starting OCR...")

    ocr_results = {}

    for filename in os.listdir(PREPROCESS_DIR):
        file_path = os.path.join(PREPROCESS_DIR, filename)

        if os.path.isfile(file_path) and filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            print(f"🔍 Processing OCR for {filename}...")
            extracted_text = extract_text(file_path)
            ocr_results[filename] = extracted_text

            # Save OCR result to a file
            result_path = os.path.join(OCR_RESULTS_DIR, f"{filename}.txt")
            with open(result_path, "w") as f:
                f.write(extracted_text)

            print(f"✅ Extracted: {extracted_text}")

    print("🎉 OCR processing complete!")

if __name__ == "__main__":
    process_ocr()
