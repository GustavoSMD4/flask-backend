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
                
        tokenUsuario = TokenPersist.create(spreadsheet.worksheet('tokens'),
                                            usuario.get('id'),
                                            usuario.get('token'))
        
        del usuario['token']
        usuarioSalvar = list(usuario.values())
        worksheet.append_row(usuarioSalvar)
        
        del usuario['senha']
        del usuario['id']
        return usuario
        
    @staticmethod
    def update(spreadsheet: gspread.Spreadsheet, usuario: dict):
        worksheetUsuario = spreadsheet.worksheet('usuario')
        
        index = usuario.get('index')
        
        numeroNaPlanilha = index + 2
        
        del usuario['index']
        usuarioUpdate = [[usuario.values()]]
        
        worksheetUsuario.update(usuarioUpdate, range_name=F"A{numeroNaPlanilha}:E{numeroNaPlanilha}")
        
        return usuario
        
        