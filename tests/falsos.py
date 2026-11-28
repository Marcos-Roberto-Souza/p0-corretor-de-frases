""" Peças falsas para simular o servidor da LLM nos testes.
"""
import contextlib
import logging

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


# Função para Juntar as mensagens de log do programa numa lista para os testes poder ler.
@contextlib.contextmanager
def coletar_logs():
    registros = []
    
    class Coletor(logging.Handler):
        def emit(self, record):
            registros.append(record.getMessage())
            
    logger = logging.getLogger("corretor")
    coletor = Coletor()
    nivel_antigo = logger.level
    logger.addHandler(coletor)
    logger.setLevel(logging.DEBUG)
    
    try:
        yield registros
    
    finally:
        logger.removeHandler(coletor)
        logger.setLevel(nivel_antigo)