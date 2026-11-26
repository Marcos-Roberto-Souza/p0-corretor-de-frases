"""
    Terminal: captura da entrada e apresentação do resultado.
"""
import sys

from corretor.config import carregar_configuracao
from corretor.erros import ErroCorretor
from corretor.prompt import IDIOMAS
from corretor.resposta import Correcao
from corretor.servico import corrigir_frase

""" Função Pergunta o idioma da frase até receber uma opção válida do usuário."""
def perguntar_idioma() -> str:
    while True:
        escolha = input("Idioma da frase(pt = português, en = inglês): ")
        escolha = escolha.strip().lower()
        if escolha in IDIOMAS:
            return escolha
        print("Opção inválida. Digite 'pt' ou 'en'. ")


