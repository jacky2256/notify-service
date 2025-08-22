from enum import Enum
from pydantic import BaseModel, EmailStr, HttpUrl, ConfigDict


class NotifyEmailEventType(str, Enum):
    USER_REGISTERED = "notify.user.registered.email"
    USER_PASS_RESET = "notify.user.pass.reset.email"
    USER_PASS_CHANGED = "notify.pass.changed.email"


class Recipient(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    language: str = "en"


class RegisteredPayload(Recipient):
    login: str
    password: str
    confirm_url: HttpUrl


class PassResetPayload(Recipient):
    confirm_url: HttpUrl


class PassChangedPayload(Recipient):
    pass


class NotifyEmailEvent(BaseModel):
    payload: RegisteredPayload | PassResetPayload | PassChangedPayload

    model_config = ConfigDict(populate_by_name=True, extra="ignore")
