#!/usr/bin/env python3
""" filtered logger """
import re


def filter_datum(fields: list, redaction: str, message: str, separator: str) -> str:
    """ filter datum """
    for field in fields:
        message = re.sub(f"{field}=.*?{separator}", f"{field}={redaction}{separator}", message)
    return message
