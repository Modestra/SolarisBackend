from typing import Any
from django.core.serializers.json import DjangoJSONEncoder

class Message:
    """Основная форма реализации сообщения запроса"""
    def __init__(self, type, text):
        self.type = type
        self.text = text

class MessageEncoder(DjangoJSONEncoder):
    """Создание JSON формы сообщения об успешном запросе"""
    def default(self, o):
        if isinstance(o, Message):
            return {"type": o.type, "text": o.text}
        return super().default()