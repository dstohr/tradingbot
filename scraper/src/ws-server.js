const WebSocket = require('ws');
const wss = new WebSocket.Server({ port: process.env.SCRAPER_WS_PORT });


wss.on('connection', function connection(ws) {
    ws.on('message', function incoming(message) {
        console.log('received: %s', message);
    });

    ws.send('something');
});

wss.broadcast = function (data) {
    wss.clients.forEach(function (client) {
        if (client.readyState === WebSocket.OPEN) {
            client.send(data);
        }
    });
};

module.exports = wss;