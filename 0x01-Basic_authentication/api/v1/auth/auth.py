#!/usr/bin/env python3
"""
auth.py
"""
from flask import request
from typing import *
from typing import TypeVar


class Auth:
    """ Auth class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ require_auth
        """
        if path is None:
            return True
        if excluded_paths is None or excluded_paths == []:
            return True
        if path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """ authorization_header
        """
        if request is None:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """ current_user
        """
        return None
