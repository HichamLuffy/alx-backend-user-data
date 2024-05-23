#!/usr/bin/env python3
"""
auth.py
"""
from typing import List, TypeVar
from flask import request
import os


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

        if path[-1] != "/":
            path += "/"

        for excluded_path in excluded_paths:
            if excluded_path.endswith('*'):
                if path.startswith(excluded_path[:-1]):
                    return False
            else:
                if path == excluded_path:
                    return False

        return True

    def authorization_header(self, request=None) -> str:
        """ authorization_header
        """
        if request is None:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar("User"):
        """ current_user
        """
        return None

    def session_cookie(self, request=None):
        """ Returns the value of the cookie named _my_session_id from request
        """
        if request is None:
            return None
        session_name = os.getenv("SESSION_NAME")
        if session_name is None:
            return None
        return request.cookies.get(session_name)

    def destroy_session(self, request=None):
        """ Destroy the user session / logout """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        if self.user_id_for_session_id(session_id) is None:
            return False
        del self.user_id_by_session_id[session_id]
        return True
