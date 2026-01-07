import mediapipe as mp
import numpy as np

def test_mp_pure():
    print("Initializing MediaPipe Hands (Pure)...")
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )
    print("MediaPipe Hands initialized.")
    
    # Create black image (height, width, 3)
    img = np.zeros((480, 640, 3), dtype=np.uint8)
    
    print("Processing dummy image...")
    # MediaPipe expects RGB, but we just pass zeros
    results = hands.process(img)
    print("Processing complete.")
    
    hands.close()
    print("Test complete.")

if __name__ == "__main__":
    test_mp_pure()
