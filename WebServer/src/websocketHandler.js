const WebSocket = require('ws');

const setupWebSocket = (wss) => {
    wss.on('connection', ws => {
        console.log('Client connected to WebSocket');

        ws.on('message', message => {
            console.log(`Received message from client: ${message}`);
            // In a real game, process the message based on a defined protocol
            // For example, if message is a JSON string:
            try {
                const parsedMessage = JSON.parse(message);
                console.log('Parsed WebSocket message:', parsedMessage);

                // Example: Handle different message types
                if (parsedMessage.type === 'gesture_data') {
                    console.log('Gesture Data Received via WebSocket:', parsedMessage.gesture);
                    // For real-time feedback or small updates that don't require full API call
                    // For actual game logic (like defeating a monster), use the HTTP API endpoint.
                    ws.send(JSON.stringify({ type: 'ws_gesture_ack', message: `WebSocket received gesture: ${parsedMessage.gesture}` }));
                } else if (parsedMessage.type === 'player_action') {
                    console.log('Player Action Received:', parsedMessage.action);
                    // TODO: Implement specific player actions (e.g., pause, resume)
                    ws.send(JSON.stringify({ type: 'action_ack', success: true, message: 'Action acknowledged!' }));
                }
                // Add more WebSocket message types as needed

            } catch (error) {
                console.error('Failed to parse WebSocket message:', message, error);
                ws.send(JSON.stringify({ type: 'error', message: 'Invalid message format' }));
            }
        });

        ws.on('close', () => {
            console.log('Client disconnected from WebSocket');
        });

        ws.on('error', error => {
            console.error('WebSocket error:', error);
        });
    });
};

module.exports = setupWebSocket; 