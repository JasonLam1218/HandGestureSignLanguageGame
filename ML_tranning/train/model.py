import tensorflow as tf
from tensorflow.keras import layers, models
import numpy as np
import os

def create_gesture_model(input_shape=(21, 3), num_classes=4):
    """
    Creates a simple Keras model for gesture recognition.
    Input shape (21, 3) for 21 hand landmarks (x, y, z).
    """
    if num_classes < 2:
        raise ValueError("Number of classes must be at least 2 for classification")
    
    model = models.Sequential([
        layers.Input(shape=input_shape),
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.3),
        layers.Dense(64, activation='relu'),
        layers.Dropout(0.3),
        layers.Dense(num_classes, activation='softmax')
    ])
    
    model.compile(optimizer='adam', 
                  loss='sparse_categorical_crossentropy', 
                  metrics=['accuracy'])
    return model

def load_data(data_dir='./data'):
    """
    Loads actual data for training.
    Assumes data is structured: data_dir/gesture_name/sample.npy
    """
    print(f"Loading data from {data_dir}...")
    X = [] # Features (landmark data)
    y = [] # Labels (gesture class index)
    label_map = {}
    current_label = 0

    gesture_names = sorted([d for d in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, d))])
    if not gesture_names:
        print(f"No gesture directories found in {data_dir}. Please run data_collection.py first.")
        return np.array([]), np.array([]), {}

    for gesture_name in gesture_names:
        label_map[gesture_name] = current_label
        gesture_path = os.path.join(data_dir, gesture_name)
        for sample_file in os.listdir(gesture_path):
            if sample_file.endswith('.npy'):
                sample_path = os.path.join(gesture_path, sample_file)
                try:
                    landmarks = np.load(sample_path)
                    X.append(landmarks)
                    y.append(current_label)
                except Exception as e:
                    print(f"Error loading {sample_path}: {e}")
        current_label += 1
    
    print(f"Loaded {len(X)} samples with {len(label_map)} classes.")
    print(f"Generated label map: {label_map}")
    return np.array(X), np.array(y), label_map


if __name__ == '__main__':
    # Load data first to determine the correct number of classes
    X_train, y_train, label_map = load_data(data_dir='./data')
    
    if len(X_train) == 0:
        print("No training data found. Please run data_collection.py first.")
        exit(1)
    
    num_classes = len(label_map)
    if num_classes < 2:
        print(f"Error: Only {num_classes} class(es) found. Need at least 2 classes for classification.")
        print("Please collect data for multiple gesture classes using data_collection.py")
        exit(1)
    
    input_shape = X_train.shape[1:]
    print(f"Creating model with {num_classes} classes and input shape {input_shape}")

    model = create_gesture_model(input_shape=input_shape, num_classes=num_classes)
    model.summary()

    # Train the model
    print(f"\nStarting model training with {len(X_train)} samples...")
    if len(X_train) < 10:
        print("Warning: Very few training samples. Consider collecting more data for better performance.")
    
    # Use validation split only if we have enough data
    validation_split = 0.2 if len(X_train) >= 10 else 0.0
    
    model.fit(X_train, y_train, epochs=10, batch_size=min(32, len(X_train)), 
              validation_split=validation_split)

    # Save the trained model
    os.makedirs('ML_Model', exist_ok=True)
    model_save_path = 'ML_Model/trained_gesture_model.h5'
    model.save(model_save_path)
    print(f"Model saved to {model_save_path}")

    # Save label map for inference
    label_map_path = 'ML_Model/label_map.txt'
    with open(label_map_path, 'w') as f:
        for gesture, label_id in label_map.items():
            f.write(f'{gesture}:{label_id}\n')
    print(f"Label map saved to {label_map_path}")

    print("\nTraining process complete.") 