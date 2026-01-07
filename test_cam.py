import cv2

def test_cam():
    print("Attempting to open camera...")
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Failed to open camera.")
        return

    print("Camera opened successfully. Reading 10 frames...")
    for i in range(10):
        ret, frame = cap.read()
        if not ret:
            print("Failed to read frame")
            break
        print(f"Read frame {i+1}")
    
    cap.release()
    print("Camera test complete.")

if __name__ == "__main__":
    test_cam()
