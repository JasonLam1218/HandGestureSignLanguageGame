// This file would contain client-side WebSocket specific logic for the Unity WebGL build
// (e.g., establishing WebSocket connection, sending/receiving messages).

const socket = new WebSocket('ws://localhost:3000'); // Ensure this matches your server's WebSocket URL

socket.onopen = (event) => {
    console.log('WebSocket connected:', event);
    // You might send an initial message to the server here, e.g., to register the client
};

socket.onmessage = (event) => {
    console.log('Message from server:', event.data);
    // Handle incoming messages from the server here
    // If the server sends data intended for Unity, you'd forward it:
    // Example: If message is JSON and has a 'unityMessage' field
    try {
        const data = JSON.parse(event.data);
        if (data.unityMessage) {
            if (unityInstance && unityInstance.SendMessage) {
                // Example: unityInstance.SendMessage("GameManager", "OnServerMessage", data.unityMessage);
                console.log("Would send message to Unity:", data.unityMessage);
            }
        }
    } catch (e) {
        console.warn("Received non-JSON message or message without 'unityMessage' field:", event.data);
    }
};

socket.onclose = (event) => {
    console.log('WebSocket disconnected:', event);
};

socket.onerror = (error) => {
    console.error('WebSocket error:', error);
};

// This function will be called by main.js (which gets data from Unity)
function sendGestureDataToWebsocket(gestureData) {
    if (socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify({ type: "gestureData", data: gestureData }));
        console.log('Sent gesture data to server:', gestureData);
    } else {
        console.warn('WebSocket not open. Gesture data not sent:', gestureData);
    }
}

// Example function to send data to the server
function sendToServer(data) {
    if (socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify(data));
        console.log('Sent to server:', data);
    } else {
        console.warn('WebSocket not open. Message not sent:', data);
    }
} 