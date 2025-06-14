import cv2
import mediapipe as mp
import numpy as np
import tensorflow as tf
import os

class HandGestureDetector:
    def __init__(self, model_path='ML_Model/trained_gesture_model.h5', label_map_path='ML_Model/label_map.txt'):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils

        self.model = None
        self.label_map = {}
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
                
                # Convert landmarks to numpy array (x, y, z for 21 points)
                landmarks = np.array([[lm.x, lm.y, lm.z] for lm in hand_landmarks.landmark])
                return landmarks, frame
        
        return None, frame

    def process_landmarks(self, landmarks):
        """
        Process landmarks to identify the gesture using the loaded ML model.
        Returns: gesture_name (str) or None if no valid gesture detected.
        """
        if landmarks is None or self.model is None:
            return None

        try:
            print(f"Shape of landmarks before reshape: {landmarks.shape}")
            # Reshape keypoints to (1, 21, 3) for model prediction
            keypoints = landmarks.reshape(1, 21, 3)
            print(f"Shape of keypoints after reshape: {keypoints.shape}")
            
            # Predict gesture
            predictions = self.model.predict(keypoints, verbose=0)
            predicted_class_index = np.argmax(predictions)
            confidence = predictions[0][predicted_class_index]

            print(f"Raw predictions: {predictions}")
            print(f"Predicted class index: {predicted_class_index}, Confidence: {confidence:.2f}")

            # Optional: Set a confidence threshold
            if confidence < 0.7:
                return "Unknown"

            predicted_gesture = self.label_map.get(predicted_class_index, "Unknown")

            return predicted_gesture
        except Exception as e:
            print(f"Error during landmark processing: {e}")
            return None

    def release(self):
        """
        Release resources
        """
        self.hands.close()

if __name__ == '__main__':
    # The model and label map are expected in the current working directory (ML_Model/)
    detector = HandGestureDetector(
        model_path='ML_Model/trained_gesture_model.h5',
        label_map_path='ML_Model/label_map.txt'
    )
    
    cap = None
    
    # Attempt to open the built-in camera by trying common indices
    # for i in range(5): # Try camera indices from 0 to 4
    #     print(f"Attempting to open camera at index {i} with AVFoundation backend...")
    #     cap = cv2.VideoCapture(2, cv2.CAP_AVFOUNDATION) 
    #     if cap.isOpened():
    #         print(f"Successfully opened camera at index {i}.")
    #         break
    #     else:
    #         print(f"Could not open camera at index {i}.")

    cap = cv2.VideoCapture(2, cv2.CAP_AVFOUNDATION) 

    if not cap or not cap.isOpened():
        print("Error: Could not open any camera. Please ensure your camera is connected and accessible,")
        print("and check your operating system's camera permissions for the application running this script.")
        exit()

    print("Webcam opened. Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame from camera. It might have disconnected or is in use by another application.")
            break

        landmarks, processed_frame = detector.detect_gesture(frame)
        gesture = detector.process_landmarks(landmarks)

        if gesture:
            display_text = f'Gesture: {gesture}'
            if gesture == "Thumbs Up":
                display_text = "Good!"
            elif gesture == "One Finger":
                display_text = "1"
            elif gesture == "Two Fingers":
                display_text = "2"
            cv2.putText(processed_frame, display_text, (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        cv2.imshow('Hand Gesture Recognition', processed_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    detector.release() 