import express from 'express';
import mongoose from 'mongoose';
import cors from 'cors';
import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';

const app = express();
const PORT = 5000;
const JWT_SECRET = 'your_jwt_secret_key';

app.use(cors());
app.use(express.json());

// MongoDB connection
mongoose.connect('mongodb://localhost:27017/expensetracker', {
  useNewUrlParser: true,
  useUnifiedTopology: true
}).then(() => console.log('✅ MongoDB Connected'))
  .catch(err => console.error('❌ MongoDB Connection Error:', err));

// User schema
const userSchema = new mongoose.Schema({
  first_name: String,
  last_name: String,
  email: { type: String, unique: true },
  password: String
});
const User = mongoose.model('User', userSchema);

// Signup Route
app.post('/api/auth/signup', async (req, res) => {
  const { first_name, last_name, email, password } = req.body;

  try {
    const existing = await User.findOne({ email });
    if (existing) return res.status(400).json({ success: false, message: 'User already exists' });

    const hashed = await bcrypt.hash(password, 10);
    const newUser = new User({ first_name, last_name, email, password: hashed });
    await newUser.save();

    const token = jwt.sign({ userId: newUser._id }, JWT_SECRET, { expiresIn: '1h' });

    res.json({
      success: true,
      access_token: token,
      user: {
        first_name: newUser.first_name,
        last_name: newUser.last_name,
        email: newUser.email
      }
    });
  } catch (err) {
    console.error('Signup error:', err);
    res.status(500).json({ success: false, message: 'Signup error' });
  }
});

// Login Route
app.post('/api/auth/login', async (req, res) => {
  const { email, password } = req.body;

  try {
    const user = await User.findOne({ email });
    if (!user) return res.status(401).json({ success: false, message: 'User not found' });

    const isMatch = await bcrypt.compare(password, user.password);
    if (!isMatch) return res.status(401).json({ success: false, message: 'Incorrect password' });

    const token = jwt.sign({ userId: user._id }, JWT_SECRET, { expiresIn: '1h' });

    res.json({
      success: true,
      access_token: token,
      user: {
        first_name: user.first_name,
        last_name: user.last_name,
        email: user.email
      }
    });
  } catch (err) {
    console.error('Login error:', err);
    res.status(500).json({ success: false, message: 'Login failed' });
  }
});
// Dummy route: /api/summary
app.get('/api/summary', (req, res) => {
  const category = req.query.category || 'all';
  res.json({
    success: true,
    stats: {
      total: 4567.89,
      avg_daily: 123.45,
    },
    weekly_data: {
      'Week 1': 100,
      'Week 2': 200,
      'Week 3': 150,
      'Week 4': 175,
    },
    categories: {
      Food: 1200,
      Transport: 800,
      Entertainment: 600
    },
    recommendations: [
      { message: "Reduce entertainment spending", priority: "high" },
      { message: "Consider cooking at home more", priority: "medium" }
    ],
    plot: '', // optionally return base64 image if needed
  });
});

// Dummy route: /api/expenses
app.get('/api/expenses', (req, res) => {
  const period = req.query.period || 'monthly';
  const category = req.query.category || 'all';
  res.json({
    success: true,
    data: {
      'Week 1': 200,
      'Week 2': 250,
      'Week 3': 300,
      'Week 4': 180,
    }
  });
});


// Start server
app.listen(PORT, () => console.log(`🚀 Server running at http://localhost:${PORT}`));
