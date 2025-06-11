const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const ProgressSchema = new Schema({
  userId: {
    type: Schema.Types.ObjectId,
    ref: 'User',
    required: true
  },
  level: {
    type: Number,
    default: 1
  },
  zone: {
    type: Number,
    default: 0
  },
  score: {
    type: Number,
    default: 0
  },
  completedLevels: [
    {
      levelNumber: Number,
      zoneIndex: Number,
      score: Number,
      completedAt: { type: Date, default: Date.now }
    }
  ],
  lastUpdated: {
    type: Date,
    default: Date.now
  }
});

module.exports = mongoose.model('Progress', ProgressSchema); 