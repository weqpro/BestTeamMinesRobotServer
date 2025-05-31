from fastapi.routing import APIRouter
from fastapi import WebSocket, WebSocketDisconnect
import json
import asyncio

router = APIRouter(prefix="/drone_data")

# Store active WebSocket connections
active_connections: list[WebSocket] = []


async def broadcast_metal_detection():
    """Broadcast metal detection to all connected clients"""
    if active_connections:
        message = json.dumps({"type": "metal_detected"})
        # Send to all connected clients
        disconnected = []
        for connection in active_connections:
            try:
                await connection.send_text(message)
            except:
                disconnected.append(connection)

        # Remove disconnected clients
        for connection in disconnected:
            active_connections.remove(connection)


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            # Keep connection alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        active_connections.remove(websocket)


@router.post("/detect_metal")
async def detect_metal():
    print("METAL DETECTED!")
    # Broadcast to all connected WebSocket clients
    await broadcast_metal_detection()
    return {"status": "metal_detected"}
