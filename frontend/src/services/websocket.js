// src/services/websocket.js
// get from .env file
const WS_BASE = process.env.BACKEND_WS_URL || "ws://localhost:8000";

export function initWebSocket(onMessage) {
    // Use secure websocket for the deployed backend
    const ws = new WebSocket(`${WS_BASE}/ws_recognize_frame`);

    ws.onopen = () => console.log("WebSocket connected");
    ws.onmessage = (evt) => {
        const data = JSON.parse(evt.data);
        onMessage(data);
    };
    ws.onerror = (err) => console.error("WS error:", err);
    ws.onclose = () => console.log("WebSocket closed");

    return ws;
}
