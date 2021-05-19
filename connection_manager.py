from typing import List

from pydantic import UUID4
from starlette.websockets import WebSocket

from models.message import Message


class ConnectionManager:
    def __init__(self):
        from typing import Dict
        self.active_connections: Dict[str, List[WebSocket]] = {}

    @staticmethod
    def get_chat_id(client_id: UUID4, target_id: UUID4):
        return ':'.join([str(client_id), str(target_id)])

    async def connect(self, websocket: WebSocket, client_id: UUID4):
        await websocket.accept()
        chat_id = str(client_id)
        if chat_id in self.active_connections:
            self.active_connections[chat_id].append(websocket)
        else:
            self.active_connections[chat_id] = [websocket]

    def disconnect(self, websocket: WebSocket, client_id: UUID4):
        chat_id = str(client_id)
        self.active_connections[chat_id].remove(websocket)

    async def send_personal_message(self, message: Message):
        client_id = message.sender_id
        chat_id = str(client_id)
        websockets = self.active_connections[chat_id]
        for websocket in websockets:
            await websocket.send_text(f"You wrote to {message.receiver_id}: {message.text}")

    async def send_message_to_target(self, message: Message):
        client_id = message.sender_id
        target_id = message.receiver_id
        chat_id = str(target_id)
        websockets = self.active_connections[chat_id]
        for websocket in websockets:
            await websocket.send_text(f"Client #{client_id} says: {message.text}")
