from flask import Flask, request, jsonify
import gspread
from controllers.usuario.services.tokenService import TokenService
from controllers.usuario.services.usuarioService import UsuarioService

def usuarioApi(app: Flask, spreadsheet: gspread.Spreadsheet):
    
    worksheetUsuario = spreadsheet.worksheet('usuario')
    
    @app.route('/usuario/login', methods=['POST'])
    def login():
        usuario: dict = request.json
        
        try:
            
            if request.method != 'POST':
                raise Exception('o method usado não foi POST')

            usuarioLogado = UsuarioService.login(spreadsheet, usuario)
            
            return jsonify({'content': usuarioLogado}), 200
            
        except Exception as e:
            response = jsonify({'error': str(e)})
            response.status_code = 400
            return response
    
    @app.route('/usuario/consulta', methods=['POST'])
    def consulta():
        
        try:
            
            if request.method != 'POST':
                raise Exception('o method usado não foi POST')
            
            req: dict = request.json
            idUsuario = req.get('idUsuario')
            token = req.get('token')
        
            TokenService.verificarTokenValido(spreadsheet, idUsuario, token)
            
            usuarios = worksheetUsuario.get_all_records()
            return jsonify({'content': usuarios}), 200
        
        except Exception as e:
            return jsonify({'error': str(e)}), 400
          
    @app.route('/usuario/create', methods=['POST'])
    def create():
        usuario = request.json
        
        try:
            if request.method != 'POST':
                raise Exception('o method usado não foi POST')
            
            usuarioCriado = UsuarioService.createUsuario(spreadsheet, usuario)
        
            return jsonify({'content': usuarioCriado}), 200
           
        except Exception as e:
            response = jsonify({'error': str(e)})
            response.status_code = 400
            return response
    
    @app.route('/usuario/update', methods=['POST'])
    def update():
        try:
            
            if request.method != 'POST':
                raise Exception('o method usado não foi POST')
            
            usuario: dict = request.json
            token = usuario.get('token')
            idUsuario = usuario.get('id')
            
            TokenService.verificarTokenValido(spreadsheet, idUsuario, token)
            
            usuarioModificado = UsuarioService.updateUsuario(spreadsheet, usuario)
            
            return jsonify({'content': usuarioModificado}), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    
    @app.route('/usuario/delete', methods=['POST'])
    def delete():
        try:
            req: dict = request.json
            
            TokenService.verificarTokenValido(spreadsheet, req.get('idUsuario'), req.get('token'))
            
            usuarioDeletado = UsuarioService.deleteUsuario(spreadsheet, req)
            
            return jsonify({'content': usuarioDeletado}), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    
    
if __name__ == '__main__':
    usuarioApi()