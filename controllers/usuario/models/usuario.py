import uuid
import gspread
from controllers.usuario.services.tokenService import TokenService

class User:
    def __init__(self, id: str, nome: str, usuario: str, senha: str, role: str, token: str):
        self.id = id
        self.nome = nome
        self.usuario = usuario
        self.senha = senha
        self.role = role
        self.token = token
        
    @classmethod
    def create(cls, spreadsheet: gspread.Spreadsheet, user: dict):
        id = str(uuid.uuid4())
        nome = user.get('nome')
        usuario = user.get('usuario')
        senha = user.get('senha')
        role = user.get('role')
        token = TokenService.createToken(spreadsheet.worksheet('tokens'), id)
        
        usuarioCriado = cls(id, nome, usuario, senha, role, token.token)
        
        return usuarioCriado
    