const socket = io('http://localhost:3000'); // Connect to your web server

socket.on('connect', () => {
    console.log('Connected to WebSocket server');
});

socket.on('disconnect', () => {
    console.log('Disconnected from WebSocket server');
});

socket.on('gestureResult', (data) => {
    console.log('Received gesture result from server:', data);
    // TODO: Send this result to Unity (e.g., call a Unity function)
    if (unityInstance) {
        // Example: unityInstance.SendMessage("GameManager", "OnGestureRecognized", data.gesture);
        console.log("Would send gesture result to Unity:", data.gesture);
    }
});

function sendGestureDataToWebsocket(gestureData) {
    if (socket.connected) {
        socket.emit('gestureData', { data: gestureData });
        console.log('Sent gesture data to server:', gestureData);
    } else {
        console.warn('WebSocket not connected. Cannot send gesture data.');
    }
} 