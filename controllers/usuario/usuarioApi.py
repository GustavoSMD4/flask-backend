from flask import Flask, request, jsonify
import gspread
from controllers.usuario.services.usuarioService import UsuarioService
from controllers.usuario.persist.usuarioPersist import UsuarioPersist

def usuarioApi(app: Flask, spreadsheet: gspread.Spreadsheet):
    
    worksheetUsuario = spreadsheet.worksheet('usuario')
    
    @app.route('/usuario/login', methods=['POST'])
    def login():
        usuario: dict = request.json
        
        try:
            if not usuario or type(usuario) != dict:
                raise Exception('usuario nao foi enviado')

            usuarioLogado = UsuarioService.login(worksheetUsuario, usuario)
            
            response = jsonify({'body': usuarioLogado})
            response.status_code = 200
            return response
            
        except Exception as e:
            response = jsonify({'error': str(e)})
            response.status_code = 400
            return response
    
    @app.route('/usuario/consulta')
    def consulta():
        usuarios = worksheetUsuario.get_all_records()
        return jsonify({'body': usuarios}), 200
    
    @app.route('/usuario/create', methods=['POST'])
    def create():
        usuario = request.json
        
        if not usuario:
            response = jsonify({'error': 'usuario não foi enviado'})
            response.status = 400
            return response
        
        try:
            usuarioCriado = UsuarioService.createUsuario(spreadsheet, usuario)
            UsuarioPersist.create(spreadsheet, usuarioCriado.copy())
           
            response = jsonify({'body': usuarioCriado})
            response.status_code = 200
            return response
           
        except Exception as e:
            response = jsonify({'error': str(e)})
            response.status_code = 400
            return response
    
if __name__ == '__main__':
    usuarioApi()