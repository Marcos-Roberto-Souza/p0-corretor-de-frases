""" Peças falsas para simular o servidor da LLM nos testes.
"""

class ClienteFalso:
    """ Imita o cliente do Ollama: devolve uma resposta ou levanta um erro."""
    
    def __init__(self, resposta=None, erro=None):
        self.resposta = resposta
        self.erro = erro
        self.chamadas = 0
        self.ultimos_argumentos = None

    def chat(self, **kwargs):
        self.chamadas += 1
        self.ultimos_argumentos = kwargs
        if self.erro:
            raise self.erro
        return self.resposta
    
def resposta_com(texto: str) -> dict:
    """ Monta uma resposta no mesmo formato da LLM. """
    return {"message": {"content": texto}}