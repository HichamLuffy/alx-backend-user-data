#!/usr/bin/env python3
"""" encrypt password """
import bcrypt


def hash_password(password) -> bytes:
    """ hash password """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())