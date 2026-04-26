"""SpreadX Python SDK reference implementation."""

from .client import Client
from .errors import APIError

__all__ = ["APIError", "Client"]

