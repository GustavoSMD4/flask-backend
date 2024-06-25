class Token:
    def __init__(self, idUsuario: str, token: str) -> None:
        self.idUsuario = idUsuario
        self.token = token
        
    @classmethod
    def create(cls, token: dict):
        idUsuario = token.get('idUsuario')
        token = token.get('token')
        
        tokenUsuario = cls(idUsuario, token)
        return tokenUsuario