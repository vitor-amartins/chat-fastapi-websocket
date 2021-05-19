import json

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import UUID4

from connection_manager import ConnectionManager
from models.message import Message


def main():
    main_app = FastAPI()

    manager = ConnectionManager()

    @main_app.websocket("/ws/{client_id}")
    async def websocket_endpoint(websocket: WebSocket, client_id: UUID4):
        await manager.connect(websocket, client_id)
        try:
            while True:
                ws_data = await websocket.receive_text()
                message = Message(sender_id=client_id, **json.loads(ws_data))
                print(f'User {message.sender_id} sends to user {message.receiver_id} the message {message.text}')
                await manager.send_personal_message(message)
                await manager.send_message_to_target(message)
        except WebSocketDisconnect:
            manager.disconnect(websocket, client_id)

    return main_app


app = main()
