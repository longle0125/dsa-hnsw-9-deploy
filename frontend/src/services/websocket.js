// src/services/websocket.js
export function initWebSocket(onMessage) {
    const ws = new WebSocket("ws://localhost:8000/ws");

    ws.onopen = () => console.log("WebSocket connected");
    ws.onmessage = (evt) => {
        const data = JSON.parse(evt.data);
        onMessage(data);
    };
    ws.onerror = (err) => console.error("WS error:", err);
    ws.onclose = () => console.log("WebSocket closed");

    return ws;
}
