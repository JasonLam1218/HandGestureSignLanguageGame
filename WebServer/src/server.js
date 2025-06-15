require('dotenv').config();
const express = require('express');
const http = require('http');
const WebSocket = require('ws');
const path = require('path');
const connectDB = require('./config/database');

// Connect to database
connectDB();

const app = express();
const port = process.env.PORT || 3000;

// Middleware for parsing JSON and urlencoded data
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Serve static files from the 'public' directory
app.use(express.static(path.join(__dirname, '../public')));

// Create an HTTP server
const server = http.createServer(app);

// Create a WebSocket server attached to the HTTP server
const wss = new WebSocket.Server({ server });

// Import WebSocket handler
const setupWebSocket = require('./websocketHandler');
setupWebSocket(wss);

// Import API routes
const authRoutes = require('./routes/auth');
const gameRoutes = require('./routes/game');

app.use('/api/auth', authRoutes);
app.use('/api/game', gameRoutes);

// Basic route for the root URL, serving intro.html
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, '../public', 'intro.html'));
});

// Route for the game page
app.get('/game', (req, res) => {
    res.sendFile(path.join(__dirname, '../public', 'game.html'));
});

// Basic error handling middleware
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).send('Something broke!');
});

// Start the server
server.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
    console.log(`WebSocket server is running on ws://localhost:${port}`);
}); 