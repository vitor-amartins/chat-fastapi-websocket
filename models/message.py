from datetime import datetime

from pydantic import BaseModel, UUID4


class Message(BaseModel):
    sender_id: UUID4
    receiver_id: UUID4
    sent_on: datetime = datetime.now()
    text: str
