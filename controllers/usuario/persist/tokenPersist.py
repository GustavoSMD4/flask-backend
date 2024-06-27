import gspread

def verificarTokenExiste(worksheet: gspread.Worksheet, idUsuario: str):
    tokens = worksheet.get_all_records()
    tokenExiste = next((i for i in tokens if i.get('idUsuario') == idUsuario), None)
    return tokenExiste.get('token') if tokenExiste is not None else None

class TokenPersist:
    @staticmethod
    def create(spreadsheeet: gspread.Spreadsheet, idUsuario: str, tokenUsuario: str):
        worksheet = spreadsheeet.worksheet('tokens')
        tokenExiste = verificarTokenExiste(worksheet, idUsuario)
        
        if tokenExiste is not None:
            return tokenExiste
        
        worksheet.append_row([idUsuario, tokenUsuario])
        
        return tokenUsuario