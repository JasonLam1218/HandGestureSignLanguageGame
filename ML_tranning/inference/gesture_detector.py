import cv2
import mediapipe as mp
import numpy as np
import tensorflow as tf
import os
import asyncio
import json
import websockets
import time
from concurrent.futures import ThreadPoolExecutor

# WebSocket server URL
WEBSOCKET_SERVER_URL = "ws://localhost:3000"

class HandGestureDetector:
    def __init__(self, model_path='ML_Model/trained_gesture_model.h5', label_map_path='ML_Model/label_map.txt'):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils

        self.model = None
        self.label_map = {}
        self.websocket = None
        self.last_gesture_time = 0
        self.gesture_cooldown = 1.0  # Prevent spam sending
        self.load_model_and_labels(model_path, label_map_path)

    def load_model_and_labels(self, model_path, label_map_path):
        # Load the trained Keras model
        if os.path.exists(model_path):
            print(f"Loading gesture classification model from {model_path}...")
            try:
                self.model = tf.keras.models.load_model(model_path)
                print("Model loaded successfully.")
                if self.model:
                    print(f"Model expected input shape: {self.model.input_shape}")
            except Exception as e:
                print(f"Error loading model: {e}")
                self.model = None
        else:
            print(f"Warning: Model file not found at {model_path}. Gesture classification will not work.")

        # Load the label map
        if os.path.exists(label_map_path):
            print(f"Loading label map from {label_map_path}...")
            try:
                with open(label_map_path, 'r') as f:
                    for line in f:
                        if ':' in line:
                            gesture, label_id = line.strip().split(':')
                            self.label_map[int(label_id)] = gesture
                print(f"Label map loaded: {self.label_map}")
            except Exception as e:
                print(f"Error loading label map: {e}")
                self.label_map = {}
        else:
            print(f"Warning: Label map file not found at {label_map_path}. Gesture classification will return numerical IDs.")

    def detect_gesture(self, frame):
        """
        Detect hand gesture in the given frame
        Returns: (landmarks, processed_frame)
        """
        try:
            # Convert the BGR image to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Process the frame and detect hands
            results = self.hands.process(rgb_frame)
            
            # Draw hand landmarks on the frame
            if results.multi_hand_landmarks:
                all_hand_data = []
                for i, hand_landmarks in enumerate(results.multi_hand_landmarks):
                    self.mp_draw.draw_landmarks(
                        frame,
                        hand_landmarks,
                        self.mp_hands.HAND_CONNECTIONS
                    )
                    
                    # Convert landmarks to numpy array (x, y, z for 21 points)
                    landmarks = np.array([[lm.x, lm.y, lm.z] for lm in hand_landmarks.landmark])
                    
                    # Get handedness (left/right hand) - with safety check
                    handedness = "Unknown"
                    if results.multi_handedness and i < len(results.multi_handedness):
                        handedness_classification = results.multi_handedness[i].classification[0]
                        handedness = handedness_classification.label
                    
                    all_hand_data.append({'landmarks': landmarks, 'handedness': handedness})
                return all_hand_data, frame
            
            return None, frame
        except Exception as e:
            print(f"Error in gesture detection: {e}")
            return None, frame

    def process_landmarks(self, landmarks):
        """
        Process landmarks to identify the gesture using the loaded ML model.
        Returns: gesture_name (str) or None if no valid gesture detected.
        """
        if landmarks is None or self.model is None:
            return None

        try:
            # Reshape keypoints to (1, 21, 3) for model prediction
            keypoints = landmarks.reshape(1, 21, 3)
            
            # Predict gesture
            predictions = self.model.predict(keypoints, verbose=0)
            predicted_class_index = np.argmax(predictions)
            confidence = predictions[0][predicted_class_index]

            # Optional: Set a confidence threshold
            if confidence < 0.7:
                return "Unknown"

            predicted_gesture = self.label_map.get(predicted_class_index, f"Class_{predicted_class_index}")

            return predicted_gesture
        except Exception as e:
            print(f"Error during landmark processing: {e}")
            return None

    async def send_gesture_to_websocket(self, data):
        """Send gesture data to WebSocket server with proper error handling"""
        current_time = time.time()
        if current_time - self.last_gesture_time < self.gesture_cooldown:
            return  # Rate limiting
        
        try:
            async with websockets.connect(WEBSOCKET_SERVER_URL, timeout=1) as websocket:
                message = json.dumps({
                    "type": "gesture_data",
                    "gesture": data["gesture"],
                    "handedness": data["handedness"],
                    "timestamp": current_time
                })
                await websocket.send(message)
                self.last_gesture_time = current_time
        except Exception as e:
            # Silently fail to avoid spam in console when server is down
            pass

    def release(self):
        """
        Release resources properly
        """
        try:
            if self.hands:
                self.hands.close()
        except Exception as e:
            print(f"Error releasing MediaPipe hands: {e}")

def main():
    detector = None
    cap = None
    
    try:
        # Initialize detector
        detector = HandGestureDetector(
            model_path='ML_Model/trained_gesture_model.h5',
            label_map_path='ML_Model/label_map.txt'
        )
        
        # Initialize camera with better error handling
        cap = cv2.VideoCapture(2, cv2.CAP_AVFOUNDATION) 
        
        if not cap or not cap.isOpened():
            print("Error: Could not open camera. Please ensure your camera is connected and accessible.")
            return
            
        print("Webcam opened. Press 'q' to quit.")
        
        # Main processing loop
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame from camera.")
                break

            all_hand_data, processed_frame = detector.detect_gesture(frame)

            if all_hand_data:
                for i, hand_data in enumerate(all_hand_data):
                    landmarks = hand_data['landmarks']
                    handedness = hand_data['handedness']
                    gesture = detector.process_landmarks(landmarks)

                    if gesture and gesture != "Unknown":
                        display_text = f'{handedness} Hand Gesture: {gesture}'
                        if gesture == "Thumbs Up":
                            display_text = f'{handedness} Hand: Good!'
                        elif gesture == "One Finger":
                            display_text = f'{handedness} Hand: 1'
                        elif gesture == "Two Fingers":
                            display_text = f'{handedness} Hand: 2'
                        
                        cv2.putText(processed_frame, display_text, (10, 30 + i * 40), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

                        # Send gesture data over WebSocket (async)
                        asyncio.create_task(detector.send_gesture_to_websocket({
                            "gesture": gesture,
                            "handedness": handedness
                        }))

            cv2.imshow('Hand Gesture Recognition', processed_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
    except KeyboardInterrupt:
        print("\nShutting down gracefully...")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        # Cleanup resources
        if cap:
            cap.release()
        cv2.destroyAllWindows()
        if detector:
            detector.release()
        print("Resources cleaned up successfully.")

if __name__ == '__main__':
    # Run the main function with proper async handling
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nApplication terminated by user.")
    except Exception as e:
        print(f"Application error: {e}") 