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

1. **Unity Setup**
   - Open Unity Hub
   - Add the UnityProject folder
   - Install required Unity packages

2. **Web Server Setup**
   ```bash
   cd WebServer
   npm install
   npm start
   ```

3. **ML Model Setup**
   ```bash
   cd ML_Model
   pip install -r requirements.txt
   ```

## Development

- Unity scripts are in `UnityProject/Assets/Scripts`
- Web server code is in `WebServer/src`
- ML model code is in `ML_Model`

## License

MIT License 