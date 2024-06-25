import secrets
import string
import gspread
from controllers.usuario.models.tokenUsuario import Token
from utils.criptografar import criptografar


class TokenService:
    @staticmethod
    def createToken(worksheet: gspread.Worksheet, idUsuario: str):
        caracteres = string.ascii_letters + string.digits + string.punctuation
        tokenCriptografado = criptografar(''.join(secrets.choice(caracteres) for _ in range(12)))
        
        token = Token.create(dict(idUsuario=idUsuario, token=tokenCriptografado))
        return token