const express = require('express');
const router = express.Router();
const auth = require('../middleware/auth');
const Progress = require('../models/progress');

// Dummy game data for demonstration
const gameChallenges = [
    { id: 1, gesture: "Hello", monster: "Goblin" },
    { id: 2, gesture: "Goodbye", monster: "Ogre" },
    { id: 3, gesture: "Yes", monster: "Dragon" }
];

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

// Get player progress (protected route)
router.get('/progress', auth, async (req, res) => {
    try {
        const progress = await Progress.findOne({ userId: req.user.id });
        if (!progress) {
            // Create a default progress if not found for new users
            const newProgress = new Progress({
                userId: req.user.id,
                level: 1,
                zone: 0,
                score: 0,
                completedLevels: []
            });
            await newProgress.save();
            return res.json(newProgress);
        }
        res.json(progress);
    } catch (err) {
        console.error(err.message);
        res.status(500).send('Server Error');
    }
});

// Update player progress (protected route)
router.post('/progress', auth, async (req, res) => {
    const { level, zone, score, completedLevels } = req.body;

    const progressFields = {};
    if (level) progressFields.level = level;
    if (zone) progressFields.zone = zone;
    if (score) progressFields.score = score;
    if (completedLevels) progressFields.completedLevels = completedLevels;
    progressFields.lastUpdated = Date.now();

    try {
        let progress = await Progress.findOne({ userId: req.user.id });

        if (progress) {
            // Update
            progress = await Progress.findOneAndUpdate(
                { userId: req.user.id },
                { $set: progressFields },
                { new: true }
            );
            return res.json(progress);
        } else {
            // Create if not found (shouldn't happen if progress is fetched first)
            progress = new Progress({
                userId: req.user.id,
                level,
                zone,
                score,
                completedLevels
            });
            await progress.save();
            return res.json(progress);
        }

    } catch (err) {
        console.error(err.message);
        res.status(500).send('Server Error');
    }
});

// Get current game challenge (e.g., monster and required gesture)
router.get('/challenge', auth, async (req, res) => {
    try {
        // In a real game, you'd determine the current challenge based on user progress
        // For this demo, we'll just send the first challenge.
        const currentChallenge = gameChallenges[0]; 
        res.json(currentChallenge);
    } catch (err) {
        console.error(err.message);
        res.status(500).send('Server Error');
    }
});

// Gesture matching endpoint (protected route)
router.post('/match-gesture', auth, (req, res) => {
    const { recognizedGesture, requiredGesture } = req.body;

    console.log(`Received gesture: "${recognizedGesture}", Required: "${requiredGesture}"`);

    // Simplified gesture matching logic for demonstration:
    // In a real application, this would involve a complex ML model inference.
    const isMatch = recognizedGesture && requiredGesture && 
                    recognizedGesture.toLowerCase() === requiredGesture.toLowerCase();

    if (isMatch) {
        res.json({ success: true, message: 'Gesture matched! Monster defeated!', recognizedGesture, requiredGesture });
    } else {
        res.json({ success: false, message: 'Gesture did not match. Try again!', recognizedGesture, requiredGesture });
    }
});

module.exports = router; 