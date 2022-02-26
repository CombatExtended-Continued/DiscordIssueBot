#!/usr/bin/python3
import os
import sys
from dataclasses import dataclass
from typing import BinaryIO
from math import log


from functools import wraps

from nacl.exceptions import BadSignatureError
from nacl.signing import VerifyKey

def verify_key(raw_body: bytes, signature: str, timestamp: str, client_public_key: str) -> bool:
    message = timestamp.encode() + raw_body
    try:
        vk = VerifyKey(bytes.fromhex(client_public_key))
        vk.verify(message, bytes.fromhex(signature))
        return True
    except Exception as ex:
        print(ex)
    return False




@dataclass(init=False)
class Verify(object):
    public_key: str
    def __init__(self, pk):
        self.public_key = pk

    def verify(self, body: bytes, signature: str, timestamp: str):
        if (not body or not signature or not timestamp):
            return False
        return verify_key(body, signature, timestamp, self.public_key)
