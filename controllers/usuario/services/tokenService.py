import secrets
import string
import gspread
from controllers.usuario.models.tokenUsuario import Token
from controllers.usuario.persist.tokenPersist import TokenPersist
from utils.criptografar import criptografar
from functools import cache

@cache
def buscarIndexToken(spreadsheet: gspread.Spreadsheet, token: str):
    worksheet = spreadsheet.worksheet('tokens')
    tokens = worksheet.get_all_records()
    
    index = next((i for i, tok in enumerate(tokens) if tok['token'] == token), None)
    if index is None:
        raise Exception('Não foi possível localizar o index do token')
    
    return index

class TokenService:
    @staticmethod
    def createToken(spreadsheet: gspread.Spreadsheet, idUsuario: str):
        caracteres = string.ascii_letters + string.digits + string.punctuation
        tokenCriptografado = criptografar(''.join(secrets.choice(caracteres) for _ in range(12)))
        
        token = Token.create(dict(idUsuario=idUsuario, token=tokenCriptografado))
        return token
    
    @staticmethod
    @cache
    def verificarTokenValido(spreadsheet: gspread.Spreadsheet, idUsuario: str, token: str):
        worksheet = spreadsheet.worksheet('tokens')
        tokens = worksheet.get_all_records()
        tokenExiste = next((i for i in tokens if i.get('token') == token), None)
        if tokenExiste is None or tokenExiste.get('idUsuario') != idUsuario:
            raise Exception('nao foi possivel localizar o token')
    
    @staticmethod
    @cache
    def buscarToken(spreadsheet: gspread.Spreadsheet, idUsuario):
        """busca o token do usuário, caso não existir, tentará criar um novo"""
        
        worksheet = spreadsheet.worksheet('tokens')
        tokens = worksheet.get_all_records()
        token = next((i for i in tokens if i.get('idUsuario') == idUsuario), None)
        
        if token is None:
            tokenValidado = TokenService.createToken(worksheet, idUsuario)
            tokenCriado = TokenPersist.create(worksheet, tokenValidado.idUsuario, tokenValidado.token)
            return tokenCriado
        
        return token
    
    @staticmethod
    def deleteToken(spreadsheet: gspread.Spreadsheet, idUsuario: str):
        
        token = TokenService.buscarToken(spreadsheet, idUsuario)
        
        index = buscarIndexToken(spreadsheet, token.get('token'))
        
        token['index'] = index + 2
        
        TokenPersist.delete(spreadsheet, token)