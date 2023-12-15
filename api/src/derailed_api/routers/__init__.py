"""
derailed_api.routers
~~~~~~~~~~~~~~~~~~~~
Routing inside of the Derailed API
"""

__all__ = ("users", "messages")

from .message import router as messages
from .user import router as users
