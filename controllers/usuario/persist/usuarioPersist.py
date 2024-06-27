import gspread
from controllers.usuario.persist.tokenPersist import TokenPersist
from controllers.usuario.services.tokenService import TokenService

def verificarUsuarioExiste(worksheet: gspread.Worksheet, usuario: str):
    usuarios = worksheet.get_all_records()
    usuarioExiste = next((i for i in usuarios if i.get('usuario') == usuario), None)
    if usuarioExiste is not None:
        raise Exception('Nome de usuario ja existe')


class UsuarioPersist:
    @staticmethod
    def create(spreadsheet: gspread.Spreadsheet, usuario: dict):
        worksheet = spreadsheet.worksheet('usuario')
        
        verificarUsuarioExiste(worksheet, usuario.get('usuario'))
                
        TokenPersist.create(spreadsheet, usuario.get('id'), usuario.get('token'))
        
        del usuario['token']
        usuarioSalvar = list(usuario.values())
        worksheet.append_row(usuarioSalvar)
        
        del usuario['senha']
        del usuario['id']
        return usuario
        
    @staticmethod
    def update(spreadsheet: gspread.Spreadsheet, usuarioEditar: dict):
        worksheetUsuario = spreadsheet.worksheet('usuario')
        
        index = usuarioEditar.get('index')
        
        numeroNaPlanilha = index + 2
        
        del usuarioEditar['index']
        del usuarioEditar['token']

        usuarioUpdate = [[
            usuarioEditar.get('id'),
            usuarioEditar.get('nome'),
            usuarioEditar.get('usuario'),
            usuarioEditar.get('senha'),
            usuarioEditar.get('role'),
        ]]
        
        worksheetUsuario.update(usuarioUpdate, range_name=F"A{numeroNaPlanilha}:E{numeroNaPlanilha}")
        
        return usuarioEditar
        
        