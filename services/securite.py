# app/services/security.py
import hashlib

def hashPwd(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()
