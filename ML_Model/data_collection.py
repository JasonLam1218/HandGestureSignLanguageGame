import cv2
import mediapipe as mp
import numpy as np
import os
import time

# --- Configuration ---
DATA_DIR = './data' # Directory to save collected data
GESTURE_NAMES = ["Thumbs Up", "Peace Sign", "One Finger", "Two Fingers"] # Add more gestures here
NUM_SAMPLES_PER_GESTURE = 100 # Number of samples to collect for each gesture
DELAY_BEFORE_START = 3 # Seconds to wait before starting collection for a gesture
SAMPLE_INTERVAL = 0.1 # Seconds between capturing each sample

# --- MediaPipe Setup ---
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)
mp_draw = mp.solutions.drawing_utils

def collect_data():
    cap = None
    # Attempt to open the built-in camera by trying common indices
    for i in range(5): # Try camera indices from 0 to 4
        print(f"Attempting to open camera at index {i} with AVFoundation backend...")
        cap = cv2.VideoCapture(i, cv2.CAP_AVFOUNDATION)
        if cap.isOpened():
            print(f"Successfully opened camera at index {i}.")
            break
        else:
            print(f"Could not open camera at index {i}.")

    if not cap or not cap.isOpened():
        print("Error: Could not open any camera. Please ensure your camera is connected and accessible,")
        print("and check your operating system's camera permissions for the application running this script.")
        return

    print("Camera opened. Follow instructions to collect data. Press 'q' to quit at any time.")

    for gesture_name in GESTURE_NAMES:
        os.makedirs(os.path.join(DATA_DIR, gesture_name), exist_ok=True)
        print(f"\nPreparing to collect data for: {gesture_name}")
        print(f"Please show the '{gesture_name}' gesture to the camera.")
        
        # Countdown before starting
        for i in range(DELAY_BEFORE_START, 0, -1):
            print(f"Starting in {i}...")
            time.sleep(1)
        print("Go!")

        samples_collected = 0
        while samples_collected < NUM_SAMPLES_PER_GESTURE:
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame from camera.")
                break

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb_frame)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    
                    landmarks = np.array([[lm.x, lm.y, lm.z] for lm in hand_landmarks.landmark])
                    
                    # Save the landmark data
                    sample_path = os.path.join(DATA_DIR, gesture_name, f"sample_{samples_collected}.npy")
                    np.save(sample_path, landmarks)
                    samples_collected += 1
                    print(f"Collected {samples_collected}/{NUM_SAMPLES_PER_GESTURE} for {gesture_name}")

            cv2.putText(frame, f'Collecting: {gesture_name} ({samples_collected}/{NUM_SAMPLES_PER_GESTURE})', (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.imshow('Data Collection', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Data collection interrupted by user.")
                break
            time.sleep(SAMPLE_INTERVAL) # Control the sampling rate

        if samples_collected < NUM_SAMPLES_PER_GESTURE: # If interrupted
            break

    cap.release()
    cv2.destroyAllWindows()
    hands.close()
    print("Data collection complete.")

if __name__ == '__main__':
    collect_data() 