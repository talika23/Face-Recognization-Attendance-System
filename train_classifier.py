import cv2
import numpy as np
import os

def train_classifier():
    # Path to your training images (format: user.id.number.jpg)
    dataset_path = "data"
    
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    detector = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    
    faces = []
    ids = []
    
    for root, _, files in os.walk(dataset_path):
        for file in files:
            if file.lower().endswith((".jpg", ".png")):
                try:
                    # Extract ID from filename (user.id.number.jpg)
                    id = int(file.split(".")[1])
                    img_path = os.path.join(root, file)
                    
                    # Read and convert to grayscale
                    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                    
                    # Detect faces
                    faces_detected = detector.detectMultiScale(img)
                    
                    for (x, y, w, h) in faces_detected:
                        faces.append(img[y:y+h, x:x+w])
                        ids.append(id)
                except Exception as e:
                    print(f"Error processing {file}: {str(e)}")
    
    # Train and save the model
    recognizer.train(faces, np.array(ids))
    recognizer.save("classifier.xml")
    print(f"Training complete. {len(np.unique(ids))} faces trained.")

if __name__ == "__main__":
    train_classifier()