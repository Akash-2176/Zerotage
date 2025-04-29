import cv2
import os

def preprocess_images(image_paths, output_dir):
    """Lightweight preprocessing for license plate images."""
    os.makedirs(output_dir, exist_ok=True)

    for image_path in image_paths:
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        if img is None:
            print(f"❌ Could not read {image_path}, skipping...")
            continue

        
        height, width = img.shape
        new_width = int((100 / height) * width)
        img = cv2.resize(img, (new_width, 50))

        _, processed_img = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY)

        
        filename = os.path.basename(image_path)
        save_path = os.path.join(output_dir, f"processed_{filename}")
        cv2.imwrite(save_path, processed_img)
        print(f"✅ Preprocessed and saved: {save_path}")

    print("🎉 Preprocessing complete!")

if __name__ == "__main__":
    print("Run this script from `main.py` for batch processing.")
