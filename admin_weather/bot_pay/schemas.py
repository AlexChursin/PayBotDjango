from ninja import Schema


class PatchUser(Schema):
    user_language: str = None
    hash: str = None
    last_trans: str = None
    last_wallet: str = None
    limits: int = None
    completed: int = None
    from_refer: int = None


class Message(Schema):
    detail: str

