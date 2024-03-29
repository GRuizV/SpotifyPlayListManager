const mongoose = require('mongoose');

const { Schema } = mongoose;

const userSchema = new Schema({
  userId: { type: String, required: true, unique: true },
  refreshToken: { type: String, required: true, unique: true },
  playlistId: { type: String },
  lastUpdated: { type: Date },
  playlistOptions: {
    seeds: { type: [String], default: ['ST', 'ST', 'MT', 'MT', 'MT'] },
    acousticness: { type: [Number, Number], default: [10, 90] },
    danceability: { type: [Number, Number], default: [10, 90] },
    energy: { type: [Number, Number], default: [10, 90] },
    instrumentalness: { type: [Number, Number], default: [10, 90] },
    popularity: { type: [Number, Number], default: [50, 100] },
    valence: { type: [Number, Number], default: [10, 90] },
  },
  stripeId: { type: String, required: false },
  grandmothered: { type: Boolean, default: false },
});

const userModel = mongoose.model('users', userSchema, 'users');

module.exports = userModel;
