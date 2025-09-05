const express = require('express');
const cors = require('cors');
const fetch = require('node-fetch');

const app = express();
const PORT = process.env.PORT || 3001;

// Middleware
app.use(cors());
app.use(express.json());

// API endpoint for news
app.get('/api/news', async (req, res) => {
  const {
    country = 'us',
    category = 'general',
    page = 1,
    pageSize = 8,
  } = req.query;

  const apiKey = '11e2c80f95584684a9a6f1849b8c4c48'; // NewsAPI key

  const url = `https://newsapi.org/v2/top-headlines?country=${country}&category=${category}&apiKey=${apiKey}&page=${page}&pageSize=${pageSize}`;

  try {
    const response = await fetch(url);
    const data = await response.json();
    
    if (data.status === 'error') {
      return res.status(400).json({ error: data.message });
    }
    
    res.status(200).json(data);
  } catch (error) {
    console.error('Error fetching news:', error);
    res.status(500).json({ error: 'Failed to fetch news' });
  }
});

// Health check endpoint
app.get('/health', (req, res) => {
  res.status(200).json({ status: 'OK', message: 'Server is running' });
});

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});