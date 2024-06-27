import secrets
import string
import gspread
from controllers.usuario.models.tokenUsuario import Token
from controllers.usuario.persist.tokenPersist import TokenPersist
from utils.criptografar import criptografar


class TokenService:
    @staticmethod
    def createToken(spreadsheet: gspread.Spreadsheet, idUsuario: str):
        caracteres = string.ascii_letters + string.digits + string.punctuation
        tokenCriptografado = criptografar(''.join(secrets.choice(caracteres) for _ in range(12)))
        
        token = Token.create(dict(idUsuario=idUsuario, token=tokenCriptografado))
        return token
    
    @staticmethod
    def verificarTokenValido(spreadsheet: gspread.Spreadsheet, idUsuario: str, token: str):
        worksheet = spreadsheet.worksheet('tokens')
        tokens = worksheet.get_all_records()
        tokenExiste = next((i for i in tokens if i.get('token') == token), None)
        if tokenExiste is None or tokenExiste.get('idUsuario') != idUsuario:
            raise Exception('nao foi possivel localizar o token')
        
    @staticmethod
    def buscarToken(spreadsheet: gspread.Spreadsheet, idUsuario):
        """busca o token do usuário, caso não existir, tentará criar um novo"""
        
        worksheet = spreadsheet.worksheet('tokens')
        tokens = worksheet.get_all_records()
        token = next((i for i in tokens if i.get('idUsuario') == idUsuario), None)
        
        if token is None:
            tokenValidado = TokenService.createToken(worksheet, idUsuario)
            tokenCriado = TokenPersist.create(worksheet, tokenValidado.idUsuario, tokenValidado.token)
            return tokenCriado
        
        return token.get('token')