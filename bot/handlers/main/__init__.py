from .errors import dp
from .bot_start import dp
from .bot_commands import dp
from .settings import dp
from .inline_handlers import dp  # Присутсвует блокировка команд
from .ttc import dp

__all__ = ['dp']
