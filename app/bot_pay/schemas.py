from ninja import Schema
from ninja.orm import create_schema
from pydantic import Field
from . import models


class PatchUser(Schema):
    """Схема изменения любого параметра пользователя"""
    user_language: str = None
    hash: str = None
    last_trans: str = None
    last_wallet: str = None
    limits: int = None
    completed: int = None
    from_refer: int = None


class Message(Schema):
    """Сообщение"""
    detail: str


ReferOut = create_schema(models.Refer, depth=1)  ## расширенная схема рефера
ReferOutPartial = create_schema(models.Refer)  ## схема рефера
UserOut = create_schema(models.TableUsers)  ## схема пользователя
