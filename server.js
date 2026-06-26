const express = require('express');
const path = require('path');

const app = express();

// Serve everything in /public (index.html, Video.mp4, fonts, etc.)
app.use(express.static(path.join(__dirname, 'public')));

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.listen(3000, () => {
  console.log('BISCUIT & BREW running at http://localhost:3000');
});
