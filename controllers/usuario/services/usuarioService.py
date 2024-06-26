from controllers.usuario.models.usuario import User
from controllers.usuario.persist.usuarioPersist import UsuarioPersist
from controllers.usuario.services.tokenService import TokenService
from utils.criptografar import criptografar
from functools import cache
import gspread

def validarCampos(nome: str, usuario:str, senha: str, role: str):
    if type(nome) != str or not nome or nome == '':
        raise ValueError('Campo nome vazio ou não é string')
    if type(usuario) != str or not usuario or usuario == '':
        raise ValueError('Campo usuario vazio ou não é string')
    if type(senha) != str or not senha or senha == '':
        raise ValueError('Campo senha vazio ou não é string')
    if type(role) != str or not role or role == '':
        raise ValueError('Campo role vazio ou não é string')

@cache
def verificarUsuarioExiste(worksheetUsuario: gspread.Worksheet, nomeCampoComparar: str, valorComparar, retornarIndex: bool):
    usuarios = worksheetUsuario.get_all_records()
    usuarioExiste = next((i for i in usuarios if i[nomeCampoComparar] == valorComparar), None)
    if usuarioExiste is None:
        raise Exception('Usuário não localizado')
    if retornarIndex:
        indexUsuario = next((index for index, user in enumerate(usuarios) if user['id'] == usuarioExiste['id']), None)
        if indexUsuario is None:
            raise Exception('Não foi possível localizar o index do usuário')

        usuarioExiste['index'] = indexUsuario
        return usuarioExiste
    
    return usuarioExiste

def verificarLogin(worsheet: gspread.Worksheet, nomeUsuario: str, senha: str):
    usuarioExiste = verificarUsuarioExiste(worsheet, 'usuario', nomeUsuario, False)
    if usuarioExiste.get('senha') != senha:
        raise Exception('senha incorreta')
    
    return usuarioExiste

class UsuarioService:
    @staticmethod
    def createUsuario(spreadsheet: gspread.Spreadsheet, user: dict):
        nome = user.get('nome')
        usuario = user.get('usuario')
        senha = user.get('senha')
        role = user.get('role')
        
        validarCampos(nome, usuario, senha, role)
        
        senhaCriptografada = criptografar(senha)
        
        usuario = User.create(spreadsheet, dict(nome=nome, usuario=usuario, senha=senhaCriptografada, role=role))
        usuarioCriado = UsuarioPersist.create(spreadsheet, usuario.__dict__)
        
        return usuarioCriado
    
    @staticmethod
    def login(spreadsheet: gspread.Spreadsheet, user: dict):
        worksheet = spreadsheet.worksheet('usuario')
        
        usuario = user.get('usuario')
        senha = user.get('senha')
        
        senhaCriptografada = criptografar(senha)
        
        usuarioLogado = verificarLogin(worksheet, usuario, senhaCriptografada)
        token = TokenService.buscarToken(spreadsheet, usuarioLogado.get('id'))
        
        usuarioLogado['token'] = token.get('token')
        del usuarioLogado['senha']
        
        return usuarioLogado
    
    @staticmethod
    def updateUsuario(spreadsheet: gspread.Spreadsheet, user: dict):
        id = user.get('id')
        nome = user.get('nome')
        usuario = user.get('usuario')
        senha = user.get('senha')
        role = user.get('role')
        
        validarCampos(nome, usuario, senha, role)
        
        worksheetUsuario = spreadsheet.worksheet('usuario')
        
        senhaCriptografada = criptografar(senha)
        
        usuarioExiste = verificarUsuarioExiste(worksheetUsuario, 'id', id, True)
        
        user['index'] = usuarioExiste.get('index')
        user['senha'] = senhaCriptografada
        
        usuarioModificado = UsuarioPersist.update(spreadsheet, user)
        
        return usuarioModificado
        
    @staticmethod
    def deleteUsuario(spreadsheet: gspread.Spreadsheet, req: dict):
        worksheetUsuario = spreadsheet.worksheet('usuario')
        
        idUsuarioDelete: str = req.get('id')
        idUsuario: str = req.get('idUsuario')
        token: str = req.get('token')
        
        usuario = verificarUsuarioExiste(worksheetUsuario, 'id', idUsuarioDelete, True)

        usuarioDeletado = UsuarioPersist.delete(spreadsheet, usuario)
        
        return usuarioDeletado

    
    
    
    
    