#!/usr/bin/env python3
"""
auth.py
"""
from typing import List, TypeVar
from flask import request
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """ BasicAuth class
    """
    pass