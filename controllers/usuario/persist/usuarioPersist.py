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
        
        usuarioSalvar = list(usuario.values())
        worksheet.append_row(usuarioSalvar)
        
        usuario['token'] = tokenUsuario
        return usuario
        