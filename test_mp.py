import mediapipe as mp
import cv2
import numpy as np

def test_mp():
    print("Initializing MediaPipe Hands...")
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )
    print("MediaPipe Hands initialized.")
    
    # Create black image
    img = np.zeros((480, 640, 3), dtype=np.uint8)
    
    print("Processing dummy image...")
    results = hands.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    print("Processing complete.")
    
    hands.close()
    print("Test complete.")

if __name__ == "__main__":
    test_mp()
