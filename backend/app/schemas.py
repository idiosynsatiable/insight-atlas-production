from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any, List

class RegisterIn(BaseModel):
    email: EmailStr
    password: str

class LoginIn(BaseModel):
    email: EmailStr
    password: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"

class IntakeIn(BaseModel):
    consent: bool
    survey: Dict[str, Any] = {}
    free_text: str = ""

class IntakeOut(BaseModel):
    session_id: int

class ReportOut(BaseModel):
    report_id: int
    session_id: int
    result: Dict[str, Any]

class MeOut(BaseModel):
    email: EmailStr
    plan: str
    status: str
