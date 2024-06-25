import hashlib

def criptografar(valor:str):
    valor = hashlib.sha256(valor.encode()).hexdigest()
    return valor