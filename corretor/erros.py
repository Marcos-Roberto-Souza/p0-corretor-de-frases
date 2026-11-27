""" ----- Erros esperados do corretor -----
    
    Cada erro carrega uma mensagem que o usuário consegue entender.
    A tela (terminal ou Streamlit) só precisa capturar ErroCorretor e mostrar a mensagem.
"""

class ErroCorretor(Exception):
    """ Base de todos os erros esperados do programa. """
    
class ConfiguracaoInvalida(ErroCorretor):
    """ Uma variável de ambiente está com valor inválido. """
    
class EntradaInvalida(ErroCorretor):
    """ A frase ou o idioma informado não pode ser enviado. """
    
class CredencialAusente(ErroCorretor):
    """ O seu servidor exige uma credencial e nenhuma foi configurada. """
    
class CredencialInvalida(ErroCorretor):
    """ O servidor recusou a credencial configurada. """
    
class ServidorIndisponivel(ErroCorretor):
    """ O servidor da LLM está fora do ar ou sobrecarregado. """
    
class FalhaDeComunicacao(ErroCorretor):
    """ Não foi possível chegar ao servidor (rede, endereço, certificado). """
    
class TempoEsgotado(ErroCorretor):
    """ O servidor demorou mais do que o tempo limite para responder. """
    
class RespostaInvalida(ErroCorretor):
    """ A resposta veio vazia ou fora do formato esperado. """