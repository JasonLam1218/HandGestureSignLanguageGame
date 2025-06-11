const express = require('express');
const router = express.Router();

// Route to get game data (e.g., list of zones, levels)
router.get('/data', (req, res) => {
  // TODO: Implement logic to fetch game configuration data
  res.json({
    zones: [
      { id: 1, name: "Letters", description: "Learn ASL Alphabet" },
      { id: 2, name: "Numbers", description: "Learn ASL Numbers" },
      { id: 3, name: "Greetings", description: "Learn Common Greetings" }
    ]
  });
});

// Route to start a new game session or level
router.post('/start', (req, res) => {
  // TODO: Implement game session initialization logic
  res.status(200).send('Game session started');
});

module.exports = router; 