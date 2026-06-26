const express = require('express');
const path = require('path');
const os = require('os');

const app = express();
const PORT = process.env.PORT || 3000;
const HOST = '0.0.0.0'; // listen on every network interface so other devices (e.g. an iPad) on the same Wi-Fi can connect

// Serve everything in /public (index.html, Video.mp4, data/products.json, etc.)
app.use(express.static(path.join(__dirname, 'public')));

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Collect this machine's LAN IPv4 addresses to print on startup.
function lanAddresses() {
  const out = [];
  const nets = os.networkInterfaces();
  for (const name of Object.keys(nets)) {
    for (const net of nets[name] || []) {
      if (net.family === 'IPv4' && !net.internal) out.push(net.address);
    }
  }
  return out;
}

app.listen(PORT, HOST, () => {
  const ips = lanAddresses();
  console.log('\nBISCUIT & BREW running at http://localhost:' + PORT);
  console.log('  On this computer:      http://localhost:' + PORT);
  if (ips.length) {
    console.log('  On your iPad / Wi-Fi:  ' + ips.map(ip => 'http://' + ip + ':' + PORT).join('\n                         '));
    console.log('\n  (Make sure the iPad is on the same Wi-Fi network. If it cannot connect,');
    console.log('   allow Node.js through your computer\'s firewall for port ' + PORT + '.)');
  } else {
    console.log('  (No LAN address detected — connect to Wi-Fi, then restart to see your iPad URL.)');
  }
  console.log('');
});
