const express = require('express');
const http = require('http');
const WebSocket = require('ws');
const path = require('path');

const app = express();
const port = process.env.PORT || 3000;

// Serve static files from the 'public' directory
app.use(express.static(path.join(__dirname, '../public')));

// Create an HTTP server
const server = http.createServer(app);

// Create a WebSocket server attached to the HTTP server
const wss = new WebSocket.Server({ server });

wss.on('connection', ws => {
    console.log('Client connected to WebSocket');

    ws.on('message', message => {
        console.log(`Received message from client: ${message}`);
        // Echo message back to the client
        ws.send(`Server received: ${message}`);
    });

    ws.on('close', () => {
        console.log('Client disconnected from WebSocket');
    });

    ws.on('error', error => {
        console.error('WebSocket error:', error);
    });
});

// Basic route for the root URL, serving intro.html
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, '../public', 'intro.html'));
});

// Route for the game page
app.get('/game', (req, res) => {
    res.sendFile(path.join(__dirname, '../public', 'game.html'));
});

// Start the server
server.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
    console.log(`WebSocket server is running on ws://localhost:${port}`);
}); 