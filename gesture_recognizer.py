import math

class GestureRecognizer:
    def __init__(self, mirrored=False):
        self.tip_ids = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky
        self.mirrored = mirrored

    def recognize_gesture(self, lm_list):
        """
        Analyzes landmarks to determine the gesture.
        Returns:
            gesture_name (str): 'OPEN_PALM', 'CLOSED_FIST', 'VOLUME_MODE', 'UNKNOWN'
            fingers_up (list): Binary list of fingers up [Thumb, Index, Middle, Ring, Pinky]
            metadata (dict): Extra data like 'pinch_distance'
        """
        if not lm_list:
            return "UNKNOWN", [], {}

    def recognize_gesture(self, lm_list, handedness="Right"):
        """
        Analyzes landmarks to determine the gesture.
        handedness: 'Right' or 'Left' (from MediaPipe, based on the image passed)
        """
        if not lm_list:
            return "UNKNOWN", [], {}

        fingers = []

        # Thumb Logic
        # Handedness comes from MediaPipe analyzing the frame.
        # Since we flip the frame BEFORE MediaPipe, MP sees the "Mirrored" version.
        # - User's Left Hand -> Looks like Left Hand on screen -> MP says "Left"
        # - User's Right Hand -> Looks like Right Hand on screen -> MP says "Right"
        
        # Geometry:
        # Left Hand (Palm facing cam): Thumb is on the RIGHT side of the hand (Tip X > IP X)
        # Right Hand (Palm facing cam): Thumb is on the LEFT side of the hand (Tip X < IP X)

        thumb_tip_x = lm_list[self.tip_ids[0]][1]
        thumb_ip_x = lm_list[self.tip_ids[0] - 1][1]
        
        thumb_is_open = False
        
        if handedness == "Left":
            # Thumb Open if Tip is to the RIGHT (Greater X)
            if thumb_tip_x > thumb_ip_x:
                thumb_is_open = True
        else: # "Right" or fallback
            # Thumb Open if Tip is to the LEFT (Smaller X)
            if thumb_tip_x < thumb_ip_x:
                thumb_is_open = True
                
        if thumb_is_open: 
             fingers.append(1)
        else:
             fingers.append(0)

        # 4 Fingers
        for id in self.tip_ids[1:]:
            if lm_list[id][2] < lm_list[id - 2][2]: # Tip y < Pip y
                fingers.append(1)
            else:
                fingers.append(0)

        total_fingers = fingers.count(1)

        # Classify Gesture
        gesture = "UNKNOWN"
        metadata = {}

        # Mode: Volume Control (Thumb and Index only)
        if fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 0:
            gesture = "VOLUME_MODE"
            # Calculate distance between Thumb Tip (4) and Index Tip (8)
            x1, y1 = lm_list[4][1], lm_list[4][2]
            x2, y2 = lm_list[8][1], lm_list[8][2]
            length = math.hypot(x2 - x1, y2 - y1)
            metadata['pinch_distance'] = length
            metadata['pinch_coords'] = ((x1+x2)//2, (y1+y2)//2)

        elif total_fingers == 5:
            gesture = "OPEN_PALM"
        elif total_fingers == 0:
            gesture = "CLOSED_FIST"
        
        return gesture, fingers, metadata
