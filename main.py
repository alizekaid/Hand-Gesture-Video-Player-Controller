import cv2
import time
import numpy as np
from hand_tracker import HandTracker
from gesture_recognizer import GestureRecognizer
from media_controller import MediaController

def main():
    # Camera Setup
    wCam, hCam = 640, 480
    cap = cv2.VideoCapture(0)
    
    # Check if camera opened successfully
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    cap.set(3, wCam)
    cap.set(4, hCam)

    # Initialize Modules
    tracker = HandTracker(detection_con=0.7)
    recognizer = GestureRecognizer(mirrored=True) # Enable mirrored mode
    # Defaulting to 'youtube' mode as per user request
    controller = MediaController(control_mode='youtube') 

    pTime = 0
    
    # Volume Control Variables
    volBar = 400
    volPer = 0
    prev_vol_y = None # Track previous Y position for volume control
    pinch_active = False # Track pinch state for mute
    
    last_gesture = "None" # Track previous gesture to prevent bouncing

    print("Starting Gesture Control Interface... Press 'q' to exit.")
    print("NOTE: For YouTube control, click on the video window first to ensure it's focused.")
    print("NOTE: Camera is MIRRORED.")

    while True:
        success, img = cap.read()
        if not success:
            print("Failed to read frame.")
            break

        # 0. Mirror the Frame
        img = cv2.flip(img, 1)

        # 1. Find Hands
        img = tracker.find_hands(img)
        lm_list, handedness = tracker.get_landmark_positions(img)

        gesture = "None"
        
        if len(lm_list) != 0:
            # 2. Recognize Gesture
            gesture, fingers, meta = recognizer.recognize_gesture(lm_list, handedness)
            
            # 3. Action based on Gesture
            if gesture == "OPEN_PALM":
                # Only trigger if the previous gesture was NOT Open Palm (Rising Edge)
                if last_gesture != "OPEN_PALM":
                    print(f"Gesture Detected: {gesture}") # Debug Log
                    controller.play_pause()
                
                # Visual Feedback always shows while gesture is held
                cv2.putText(img, "PLAY/PAUSE", (50, 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3)

            elif gesture == "CLOSED_FIST":
                # Same logic for Fist if used
                if last_gesture != "CLOSED_FIST":
                    print(f"Gesture Detected: {gesture}") # Debug Log
                    controller.play_pause()
                    
                cv2.putText(img, "PAUSE (Toggle)", (50, 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 3)

            elif gesture == "VOLUME_MODE":
                cx, cy = meta.get('pinch_coords', (0,0))
                
                # Visual Feedback for Volume Mode
                cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
                cv2.putText(img, "Volume Mode: Move Up/Down | Pinch to Mute", (50, 450), cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 0, 255), 2)
                
                # --- Mute Logic (Pinch to Toggle) ---
                length = meta.get('pinch_distance', 100)
                mute_threshold = 30 # Distance pixels to consider a "Pinch"
                
                if length < mute_threshold:
                    if not pinch_active: # Only trigger on initial pinch (falling edge of distance)
                        controller.toggle_mute()
                        pinch_active = True
                        cv2.putText(img, "MUTE TOGGLED", (cx, cy - 60), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
                else:
                    pinch_active = False # Reset when fingers open
                
                # --- Dynamic Volume Control (Movement based) ---
                # Only adjust volume if NOT pinching (to avoid conflicting actions)
                if not pinch_active:
                    if prev_vol_y is None:
                        prev_vol_y = cy
                    
                    # Threshold for movement detection (pixels)
                    movement_threshold = 20
                    
                    # Check displacement
                    # cy increases downwards (0 at top)
                    # Move UP (cy decreases) -> Volume UP
                    if cy < prev_vol_y - movement_threshold:
                        controller.set_volume('up')
                        cv2.putText(img, "VOL UP", (cx, cy - 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
                        prev_vol_y = cy # Update anchor to current position for continuous scrolling
                        
                    # Move DOWN (cy increases) -> Volume DOWN
                    elif cy > prev_vol_y + movement_threshold:
                        controller.set_volume('down')
                        cv2.putText(img, "VOL DOWN", (cx, cy + 40), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
                        prev_vol_y = cy
                
        # Reset volume anchor if not in volume mode
        if gesture != "VOLUME_MODE":
            prev_vol_y = None

        # 4. Display Info
        cTime = time.time()
        fps = 1 / (cTime - pTime) if (cTime - pTime) > 0 else 0
        pTime = cTime
        
        # Update last_gesture for next frame
        last_gesture = gesture

        cv2.putText(img, f'FPS: {int(fps)}', (10, 450), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), 2)
        cv2.putText(img, f'Mode: {gesture}', (10, 420), cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 255, 255), 2)

        cv2.imshow("HCI Gesture Control", img)
        
        # Exit on 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
