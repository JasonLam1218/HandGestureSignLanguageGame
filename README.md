# Hand Gesture Sign Language Game

An interactive game that helps users learn sign language through hand gesture recognition. Players can defeat monsters by performing correct sign language gestures captured through their webcam.

## Features

- Real-time hand gesture recognition
- Multiple sign language categories/zones
- Interactive monster battles
- Progress tracking
- Web-based interface

## Prerequisites

- Unity 2022.3 LTS or later
- Node.js 18.x or later
- Python 3.8 or later
- Webcam
- Modern web browser with WebGL support

## Project Structure

```
HandGestureSignLanguageGame/
├── UnityProject/          # Unity game project
├── WebServer/            # Web server for hosting
└── ML_Model/            # Hand gesture recognition model
```

## Setup Instructions

This project involves three main components: the ML Model (Python), the Web Server (Node.js), and the Unity Game (WebGL). To run the complete project, you will need three separate terminal windows.

Before you start, ensure you have granted camera access to your terminal application in macOS System Settings. Go to `System Settings > Privacy & Security > Camera` and toggle the switch for your terminal (e.g., "Terminal", "iTerm2", or "Cursor").

### Terminal 1: ML Model Server

This terminal will run your hand gesture recognition backend.

1.  **Navigate to the `ML_Model` directory:**
    ```bash
    cd ML_Model
    ```
2.  **Ensure compatible Python version (Python 3.10.x or 3.11.x recommended):**
    If you are using Python 3.12 or later, you may encounter compatibility issues with `mediapipe` and `tensorflow`. It's recommended to use `pyenv` to install and set a compatible Python version locally.
    *   **Install pyenv (if not already installed via Homebrew):**
        ```bash
        brew install pyenv
        ```
    *   **Configure your shell for pyenv (add to `~/.zshrc` and then close/reopen terminal):**
        ```bash
        echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
        echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
        echo 'eval "$(pyenv init -)"' >> ~/.zshrc
        echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.zshrc
        ```
    *   **Install Python 3.10 (or 3.11) using pyenv:**
        ```bash
        pyenv install 3.10.12 # Or 3.11.x, e.g., 3.11.8
        ```
    *   **Set the local Python version for this directory:**
        ```bash
        pyenv local 3.10.12 # Or the version you installed
        ```
3.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```
    *(You should see `(venv)` at the beginning of your terminal prompt.)*
4.  **Install the required Python packages:**
    ```bash
    pip install -r requirements.txt
    ```
    *This will install all necessary libraries like TensorFlow, MediaPipe, and OpenCV.*
5.  **Collect Hand Gesture Data:**
    Before training your model, you need to collect data for each gesture. The `data_collection.py` script will guide you through this process.
    *   **Ensure Iriun Webcam (or your preferred camera) is running and accessible.**
    *   Run the data collection script from the `ML_Model` directory:
        ```bash
        python data_collection.py
        ```
    *   Follow the on-screen prompts to perform each gesture (e.g., "Thumbs Up", "One Finger", "Two Fingers"). Make sure to allow the script to collect the specified number of samples for *each* gesture. The data will be saved in the `ML_Model/data/` directory.
6.  **Train the ML Model:**
    Once you have collected the data, train your model using the `model.py` script. This will create or update the `trained_gesture_model.h5` and `label_map.txt` files.
    ```bash
    python train/model.py
    ```
    *This process might take a few minutes depending on your system and dataset size.*
7.  **Run the Hand Gesture Detection Script (Inference):**
    After training, you can run the `gesture_detector.py` script to see real-time hand gesture recognition. This script will open your webcam feed and display the detected gestures, indicating whether it's a 'Left Hand' or 'Right Hand' gesture.
    *   **Ensure Iriun Webcam (or your preferred camera) is running and accessible.**
    ```bash
    python inference/gesture_detector.py
    ```
    *You should see a window with your webcam feed and recognized gestures. Keep this terminal running in the background for the game to interact with it.*

### Terminal 2: Web Server

This terminal will host your game's web page and handle API/WebSocket communication.

1.  **Navigate to the `WebServer` directory:**
    ```bash
    cd WebServer
    ```
2.  **Create a `.env` file** in this directory with your MongoDB URI (replace with your actual URI):
    ```
    MONGO_URI=mongodb://localhost:27017/sign_language_game
    PORT=3000
    ```
3.  **Install Node.js dependencies:**
    ```bash
    npm install
    ```
4.  **Start the web server:**
    ```bash
    npm start
    ```
    *You should see a message like `Server running on port 3000`. Keep this terminal running in the background.*

### Terminal 3: Unity Game (One-Time Setup & Build)

This is the Unity Editor, used for building the game. This needs to be done **once** or whenever you make changes to the Unity project that require a new WebGL build.

1.  **Open Unity Hub.**
2.  **Add your `UnityProject` folder:** Click "Add" and select the `UnityProject` folder (the one containing `Assets`, `ProjectSettings`, etc.).
3.  **Open the project in Unity** (ensure Unity 2022.3 LTS or later).
4.  **Create Missing Unity Scenes:**
    *   In your Unity Project window, navigate to `Assets/Scenes`.
    *   Right-click `Create > Scene` and name them:
        *   `MainMenu.unity`
        *   `ZoneSelection.unity`
        *   `GameLevel.unity`
        *   `LevelComplete.unity`
5.  **Add Scenes to Build Settings:**
    *   Go to `File > Build Settings...`.
    *   Drag and drop the newly created scenes from your `Assets/Scenes` folder into the "Scenes In Build" list, in this exact order:
        1.  `MainMenu`
        2.  `ZoneSelection`
        3.  `GameLevel`
        4.  `LevelComplete`
6.  **Select WebGL Platform:** Choose "WebGL" from the platform list and click "Switch Platform".
7.  **Configure Player Settings:**
    *   Click "Player Settings..." at the bottom-left of the Build Settings window.
    *   Under "Player > WebGL", ensure:
        *   `Compression Format` is set to `Disabled` (for faster iteration during development).
        *   `WebGL Template` is set to `Default`.
        *   Optionally, enable `Development Build` for debugging.
        *   Optionally, enable `Run in Background` if you want the game to continue running when the browser tab is not active.
8.  **Build the WebGL Game:**
    *   Go back to the `Build Settings` window.
    *   Click the "Build" button.
    *   When prompted to select a folder, navigate to your project's `WebServer/public` directory and select it. Unity will build the game files directly into your web server's public folder.

### Playing the Game

Once all the above steps are completed (ML Model Server and Web Server running, Unity game built to `WebServer/public`):

#### Real-time Gesture Recognition Data Flow

This diagram illustrates the comprehensive data flow across the various components of the Hand Gesture Sign Language Game, from real-time gesture detection to game interaction and data persistence.

```
+--------------------------+
| Python ML Model Server   |
| (Gesture Detection)      |
+--------------------------+
           |
           | 1. Webcam Video Feed (Input)
           |    - MediaPipe: Hand Landmarks & Handedness
           |    - TensorFlow: Gesture Prediction
           |
           v
+--------------------------+  2. Gesture Data (JSON)  +------------------------+
|   WebSocket Client       |------------------------->|   WebSocket Server     |
+--------------------------+   (ws://localhost:3000)  +------------------------+
                                                        |                        |
                                                        |  Node.js Web Server    |
                                                        |     (Central Hub)      |
                                                        |                        | 6. Save/Load Game State
+------------------------+  5. Game State Data        +------------------------+  (e.g., Score, Progress)
|     HTTP Server        |<---------------------------|  Database Interaction  |<----------------->+---------------------+
| (Serves Game Files)    |  (HTTP POST or WebSocket)  |      (Mongoose)        |                   |      Database       |
+------------------------+                            +------------------------+                   |      (MongoDB)      |
           ^                                                        |                              +---------------------+
           | 4. GET / (Initial Load)                                | 3. Relay Gesture Data (JSON)
           |                                                        |
           |                                                        v
+--------------------------+                            +------------------------+
|      Unity Game          |<---------------------------|   WebSocket Server     |
|    (Running in Browser)  |   (ws://localhost:3000)     +------------------------+
+--------------------------+
           |
           | 7. Apply Gesture to Game Logic
           |    - e.g., "Thumbs Up" -> "Good!"
           v
+--------------------------+
|      In-Game Action      |
+--------------------------+
```

---

1.  Ensure both your **ML Model Server** (Terminal 1) and **Web Server** (Terminal 2) are actively running.
2.  Open your web browser (Chrome, Firefox, or Edge are recommended).
3.  Navigate to: `http://localhost:3000`
4.  Your browser will likely ask for permission to access your webcam. **Grant permission** for the game to function.
5.  The game should now load and display the main menu.

Good luck with your project! Let me know if you need any more assistance.

## Development

- Unity scripts are in `UnityProject/Assets/Scripts`
- Web server code is in `WebServer/src`
- ML model code is in `ML_Model`

## License

MIT License 