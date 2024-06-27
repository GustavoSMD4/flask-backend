import gspread
from functools import cache

@cache
def verificarTokenExiste(worksheet: gspread.Worksheet, idUsuario: str):
    tokens = worksheet.get_all_records()
    tokenExiste = next((i for i in tokens if i.get('idUsuario') == idUsuario), None)
    return tokenExiste.get('token') if tokenExiste is not None else None
    
    return index

class TokenPersist:
    @staticmethod
    def create(spreadsheeet: gspread.Spreadsheet, idUsuario: str, tokenUsuario: str):
        worksheet = spreadsheeet.worksheet('tokens')
        tokenExiste = verificarTokenExiste(worksheet, idUsuario)
        
        if tokenExiste is not None:
            return tokenExiste
        
        worksheet.append_row([idUsuario, tokenUsuario])
        
        return tokenUsuario
    
    @staticmethod
    def delete(spreadsheeet: gspread.Spreadsheet, token: dict):
        worksheet = spreadsheeet.worksheet('tokens')
        
        index = token.get('index')
        
        worksheet.delete_rows(index, index)
        