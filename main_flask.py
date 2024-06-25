from flask import Flask
from controllers.usuario.usuarioApi import usuarioApi
import gspread
import os

current_directory = os.path.dirname(os.path.abspath(__file__))

creds_path = os.path.join(current_directory, 'creds.json')

gc = gspread.service_account(filename=creds_path)

spreadsheet = gc.open('gestão_interna_flask')

app = Flask(__name__)

usuarioApi(app, spreadsheet)

if __name__ == '__main__':
    app.run(debug=True)