import tensorflow as tf
from tensorflow.keras import layers, models
import numpy as np
import os

def create_gesture_model(input_shape=(21, 3), num_classes=1):
    """
    Creates a simple Keras model for gesture recognition.
    Input shape (21, 3) for 21 hand landmarks (x, y, z).
    """
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
    Loads dummy data for training. Replace with actual data loading.
    Assumes data is structured: data_dir/gesture_name/sample.npy
    """
    print(f"Loading data from {data_dir}...")
    X = [] # Features (landmark data)
    y = [] # Labels (gesture class index)
    label_map = {}
    current_label = 0

    # Dummy data generation
    num_samples_per_class = 100
    num_landmarks = 21
    num_dimensions = 3
    # Only train for "Thumbs Up"
    gesture_names = ["Thumbs Up"]

    for i, gesture_name in enumerate(gesture_names):
        label_map[gesture_name] = current_label
        # In a real scenario, you would load actual landmark data here.
        # For demonstration, we continue with dummy data generation.
        for _ in range(num_samples_per_class):
            # Replace this with loading actual landmark data for 'gesture_name'
            # For example: np.load(f'{data_dir}/{gesture_name}/sample_{_}.npy')
            dummy_landmarks = np.random.rand(num_landmarks, num_dimensions).astype(np.float32)
            X.append(dummy_landmarks)
            y.append(current_label)
        current_label += 1
    
    print(f"Loaded {len(X)} samples with {len(label_map)} classes.")
    # Ensure the label map includes all defined gesture names
    print(f"Generated label map: {label_map}")
    return np.array(X), np.array(y), label_map


if __name__ == '__main__':
    # TODO: Replace with your actual dataset loading and preprocessing
    X_train, y_train, label_map = load_data()
    num_classes = len(label_map) # This will now be 1
    input_shape = X_train.shape[1:]

    model = create_gesture_model(input_shape=input_shape, num_classes=num_classes)
    model.summary()

    # Train the model (dummy training)
    print("\nStarting dummy model training...")
    model.fit(X_train, y_train, epochs=10, batch_size=32, validation_split=0.2)

    # Save the trained model
    model_save_path = 'trained_gesture_model.h5'
    model.save(model_save_path)
    print(f"Model saved to {model_save_path}")

    # Save label map for inference
    label_map_path = 'label_map.txt'
    with open(label_map_path, 'w') as f:
        for gesture, label_id in label_map.items():
            f.write(f'{gesture}:{label_id}\n')
    print(f"Label map saved to {label_map_path}")

    print("\nTraining process complete.") 