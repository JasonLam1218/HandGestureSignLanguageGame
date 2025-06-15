const authSection = document.getElementById('auth-section');
const gameControls = document.getElementById('game-controls');
const gameArea = document.getElementById('game-area');
const authMessage = document.getElementById('auth-message');
const gameMessage = document.getElementById('game-message');
const welcomeUsername = document.getElementById('welcome-username');
const currentLevel = document.getElementById('current-level');
const currentZone = document.getElementById('current-zone');
const currentScore = document.getElementById('current-score');
const monsterName = document.getElementById('monster-name');
const requiredGestureSpan = document.getElementById('required-gesture');
const simulatedGestureInput = document.getElementById('simulated-gesture-input');
const websocketConnectBtn = document.getElementById('websocket-connect-btn');
const websocketDisconnectBtn = document.getElementById('websocket-disconnect-btn');

let token = localStorage.getItem('token');
let ws = null;
let currentChallengeRequiredGesture = null; // Store the required gesture

const API_URL = ''; // Relative path, handled by browser

// --- UI State Management ---
function updateUI() {
    if (token) {
        authSection.classList.add('hidden');
        gameControls.classList.remove('hidden');
        gameArea.classList.remove('hidden');
        // You would typically decode the JWT to get username, but for simplicity, we'll leave it for now
        welcomeUsername.textContent = localStorage.getItem('username') || 'User';
    } else {
        authSection.classList.remove('hidden');
        gameControls.classList.add('hidden');
        gameArea.classList.add('hidden');
        clearGameInfo();
    }
}

function clearGameInfo() {
    currentLevel.textContent = 'N/A';
    currentZone.textContent = 'N/A';
    currentScore.textContent = 'N/A';
    monsterName.textContent = 'N/A';
    requiredGestureSpan.textContent = 'N/A';
    gameMessage.textContent = '';
}

function showAuthMessage(msg, isError = false) {
    authMessage.textContent = msg;
    authMessage.style.color = isError ? 'red' : 'green';
}

function showGameMessage(msg, isError = false) {
    gameMessage.textContent = msg;
    gameMessage.style.color = isError ? 'red' : 'green';
}

// --- API Calls ---
async function callApi(endpoint, method = 'GET', data = null, needsAuth = true) {
    const headers = { 'Content-Type': 'application/json' };
    if (needsAuth && token) {
        headers['x-auth-token'] = token;
    }

    const options = {
        method,
        headers,
    };
    if (data) {
        options.body = JSON.stringify(data);
    }

    try {
        const response = await fetch(`${API_URL}${endpoint}`, options);
        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.msg || 'Something went wrong');
        }
        return result;
    } catch (error) {
        console.error('API Call Error:', error);
        throw error;
    }
}

// --- Authentication Functions ---
document.getElementById('register-btn').addEventListener('click', async () => {
    const username = document.getElementById('register-username').value;
    const email = document.getElementById('register-email').value;
    const password = document.getElementById('register-password').value;
    try {
        const data = await callApi('/api/auth/register', 'POST', { username, email, password }, false);
        showAuthMessage('Registration successful!', false);
        // Optionally, log in user immediately after registration
        document.getElementById('login-email').value = email;
        document.getElementById('login-password').value = password;
    } catch (error) {
        showAuthMessage(error.message, true);
    }
});

document.getElementById('login-btn').addEventListener('click', async () => {
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;
    try {
        const data = await callApi('/api/auth/login', 'POST', { email, password }, false);
        token = data.token;
        localStorage.setItem('token', token);
        localStorage.setItem('username', email); // Store email as username for display
        showAuthMessage('Login successful!', false);
        updateUI();
        fetchProgress();
        fetchChallenge();
    } catch (error) {
        showAuthMessage(error.message, true);
    }
});

document.getElementById('logout-btn').addEventListener('click', () => {
    token = null;
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    if (ws) ws.close();
    updateUI();
    showAuthMessage('Logged out.');
});

// --- Game Functions ---
async function fetchProgress() {
    try {
        const progress = await callApi('/api/game/progress');
        currentLevel.textContent = progress.level;
        currentZone.textContent = progress.zone;
        currentScore.textContent = progress.score;
        showGameMessage('Progress fetched!');
    } catch (error) {
        showGameMessage(`Failed to fetch progress: ${error.message}`, true);
    }
}

async function fetchChallenge() {
    try {
        const challenge = await callApi('/api/game/challenge');
        monsterName.textContent = challenge.monster;
        requiredGestureSpan.textContent = challenge.gesture;
        currentChallengeRequiredGesture = challenge.gesture; // Store for matching
        showGameMessage('Challenge fetched!');
    } catch (error) {
        showGameMessage(`Failed to fetch challenge: ${error.message}`, true);
    }
}

async function sendGestureViaApi() {
    const recognizedGesture = simulatedGestureInput.value;
    if (!recognizedGesture) {
        showGameMessage('Please type a gesture to send.', true);
        return;
    }
    if (!currentChallengeRequiredGesture) {
        showGameMessage('No challenge loaded. Fetch a challenge first.', true);
        return;
    }

    try {
        const result = await callApi('/api/game/match-gesture', 'POST', {
            recognizedGesture,
            requiredGesture: currentChallengeRequiredGesture
        });
        showGameMessage(result.message, !result.success);
        if (result.success) {
            fetchProgress(); // Update progress after a successful match
            fetchChallenge(); // Get next challenge (or same if not level up logic)
        }
    } catch (error) {
        showGameMessage(`Error matching gesture: ${error.message}`, true);
    }
    simulatedGestureInput.value = ''; // Clear input
}

// --- WebSocket Functions ---
function connectWebSocket() {
    if (ws && ws.readyState === WebSocket.OPEN) {
        showGameMessage('WebSocket already connected.');
        return;
    }
    if (!token) {
        showGameMessage('Please log in to connect to WebSocket.', true);
        return;
    }

    // Append token to WebSocket URL for server-side authentication (simplified)
    ws = new WebSocket(`ws://localhost:3000?token=${token}`);

    ws.onopen = () => {
        showGameMessage('WebSocket connected.');
        websocketConnectBtn.classList.add('hidden');
        websocketDisconnectBtn.classList.remove('hidden');
    };

    ws.onmessage = (event) => {
        try {
            const data = JSON.parse(event.data);
            showGameMessage(`WebSocket Message: ${data.message}`);
            console.log('WebSocket Data:', data);
        } catch (e) {
            showGameMessage(`WebSocket Raw: ${event.data}`);
            console.log('WebSocket Raw:', event.data);
        }
    };

    ws.onclose = () => {
        showGameMessage('WebSocket disconnected.', true);
        websocketConnectBtn.classList.remove('hidden');
        websocketDisconnectBtn.classList.add('hidden');
        ws = null;
    };

    ws.onerror = (error) => {
        showGameMessage('WebSocket error!', true);
        console.error('WebSocket Error:', error);
    };
}

function disconnectWebSocket() {
    if (ws) {
        ws.close();
    }
}

function sendGestureViaWs() {
    if (!ws || ws.readyState !== WebSocket.OPEN) {
        showGameMessage('WebSocket not connected.', true);
        return;
    }
    const recognizedGesture = simulatedGestureInput.value;
    if (!recognizedGesture) {
        showGameMessage('Please type a gesture to send via WebSocket.', true);
        return;
    }

    const message = { type: 'gesture_data', gesture: recognizedGesture };
    ws.send(JSON.stringify(message));
    showGameMessage('Gesture sent via WebSocket!');
    simulatedGestureInput.value = ''; // Clear input
}

// --- Event Listeners ---
document.getElementById('fetch-progress-btn').addEventListener('click', fetchProgress);
document.getElementById('fetch-challenge-btn').addEventListener('click', fetchChallenge);
document.getElementById('send-gesture-btn').addEventListener('click', sendGestureViaApi);
document.getElementById('send-gesture-ws-btn').addEventListener('click', sendGestureViaWs);
websocketConnectBtn.addEventListener('click', connectWebSocket);
websocketDisconnectBtn.addEventListener('click', disconnectWebSocket);

// Initial UI update on page load
updateUI(); 