from pydantic import BaseModel


class Email(BaseModel):
    subject_line : str
    body : str
    cta : str

class DM(BaseModel):
    message : str


class Outreach_Message(BaseModel):
    channel : str
    outreach_msg : DM



class Email_Outreach(BaseModel):
    channel : str
    outreach_msg : Email




