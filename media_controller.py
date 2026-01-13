import pyautogui
import time

class MediaController:
    def __init__(self, control_mode='youtube'):
        self.last_action_time = 0
        self.debounce_delay = 1.0 # 1 second delay for Play/Pause
        self.vol_delay = 0.1 # Faster for volume
        self.control_mode = control_mode

    def play_pause(self):
        """Toggles Play/Pause if debounce time has passed."""
        if time.time() - self.last_action_time > self.debounce_delay:
            print(f"Action: Play/Pause Triggered! (Mode: {self.control_mode})") # Debug Log
            
            if self.control_mode == 'youtube':
                # YouTube uses 'k' for reliable play/pause
                pyautogui.press('k')
            else:
                # Default system media key
                pyautogui.press('playpause')
                
            self.last_action_time = time.time()
            return True
        return False

    def set_volume(self, direction):
        """
        Adjusts volume. 
        direction: 'up' or 'down'
        """
        if self.control_mode == 'youtube':
            # YouTube Player Volume: Up/Down Arrows
            if direction == 'up':
                print(f"Action: Volume UP (YouTube Mode)") 
                pyautogui.press('up')
            elif direction == 'down':
                print(f"Action: Volume DOWN (YouTube Mode)")
                pyautogui.press('down')
        else:
            # System Volume
            if direction == 'up':
                print("Action: Volume UP (System)")
                pyautogui.press('volumeup')
            elif direction == 'down':
                print("Action: Volume DOWN (System)")
                pyautogui.press('volumedown')
        
    def toggle_mute(self):
        """Toggles Mute (sending 'm' for YouTube or 'volumemute' for system)."""
        print(f"Action: Mute Toggled (Mode: {self.control_mode})")
        if self.control_mode == 'youtube':
            pyautogui.press('m')
        else:
            pyautogui.press('volumemute')

    def set_volume_by_percentage(self, percentage):
        """
        Advanced: Set volume based on a mapped percentage (0-100).
        Since we can't 'set' absolute volume easily cross-platform with just pyautogui,
        we might stick to relative up/down for this prototype.
        """
        pass

    def seek_forward(self):
        """Seeks forward 10 seconds."""
        if time.time() - self.last_action_time > self.debounce_delay:
            print(f"Action: Seek Forward (Mode: {self.control_mode})")
            if self.control_mode == 'youtube':
                pyautogui.press('l') # +10s
            else:
                pyautogui.press('right') # Usually +5s or +10s depending on app
            self.last_action_time = time.time()
            return True
        return False

    def seek_backward(self):
        """Seeks backward 10 seconds."""
        if time.time() - self.last_action_time > self.debounce_delay:
            print(f"Action: Seek Backward (Mode: {self.control_mode})")
            if self.control_mode == 'youtube':
                pyautogui.press('j') # -10s
            else:
                pyautogui.press('left') # Usually -5s or -10s depending on app
            self.last_action_time = time.time()
            return True
        return False
