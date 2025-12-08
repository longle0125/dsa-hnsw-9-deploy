// src/services/websocket.js
export function initWebSocket(onMessage) {
    // Use secure websocket for the deployed backend
    const ws = new WebSocket("wss://face-reco-api-2sjf.onrender.com/ws");

    ws.onopen = () => console.log("WebSocket connected");
    ws.onmessage = (evt) => {
        const data = JSON.parse(evt.data);
        onMessage(data);
    };
    ws.onerror = (err) => console.error("WS error:", err);
    ws.onclose = () => console.log("WebSocket closed");

    return ws;
}
