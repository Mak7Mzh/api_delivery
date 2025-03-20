from pydantic import BaseModel

class ReqCreate(BaseModel):
    description: str
    sender_name: str
    sender_phone: int
    sender_address: str
    recipient_name: str
    recipient_phone: int
    recipient_address: str