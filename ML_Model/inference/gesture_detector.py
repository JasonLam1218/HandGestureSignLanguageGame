import cv2
import mediapipe as mp
import numpy as np

class HandGestureDetector:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils

    def detect_gesture(self, frame):
        """
        Detect hand gesture in the given frame
        Returns: (landmarks, processed_frame)
        """
        # Convert the BGR image to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process the frame and detect hands
        results = self.hands.process(rgb_frame)
        
        # Draw hand landmarks on the frame
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS
                )
                
                # Convert landmarks to numpy array
                landmarks = np.array([[lm.x, lm.y, lm.z] for lm in hand_landmarks.landmark])
                return landmarks, frame
        
        return None, frame

    def process_landmarks(self, landmarks):
        """
        Process landmarks to identify the gesture
        Returns: gesture_name
        """
        if landmarks is None:
            return None
            
        # TODO: Implement gesture classification logic
        # This will be implemented based on your specific sign language requirements
        
        return "unknown"

    def release(self):
        """
        Release resources
        """
        self.hands.close()

if __name__ == '__main__':
    detector = HandGestureDetector()
    
    cap = None
    # Prioritize camera index 1 first, as it's likely the built-in Mac camera.
    print(f"Attempting to open camera at index 1 (prioritized)...")
    cap = cv2.VideoCapture(1)
    if cap.isOpened():
        print(f"Successfully opened camera at index 1")
    else:
        print(f"Failed to open camera at index 1. Falling back to other indices...")
        cap = None # Reset cap if 1 fails

        # Then try other common indices if the prioritized one failed
        for i in range(5): # Try indices from 0 to 4
            if i == 1: continue # Skip index 1 as we already tried it
            print(f"Attempting to open camera at index {i}...")
            cap = cv2.VideoCapture(i) 
            if cap.isOpened():
                print(f"Successfully opened camera at index {i}")
                break
            else:
                print(f"Failed to open camera at index {i}")
                cap = None

    if cap is None:
        print("Error: Could not open any webcam. Please ensure a webcam is connected and accessible.")
        exit()

    print("Webcam opened. Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        landmarks, processed_frame = detector.detect_gesture(frame)
        gesture = detector.process_landmarks(landmarks)

        if gesture:
            cv2.putText(processed_frame, f'Gesture: {gesture}', (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        cv2.imshow('Hand Gesture Recognition', processed_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    detector.release() 