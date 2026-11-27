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

""" Função que mostra o resultado no terminal. """
def apresentar(correcao: Correcao) -> None:
    print()
    print(f"Frase corrigida: {correcao.frase_corrigida}")
    print(f"O que mudou: {correcao.explicacao}")

""" Função que Roda o programa e Devolve 0 se tudo deu certo e 1 se houve erro esperado. """
def main() -> int:
    try:
        config = carregar_configuracao()
        idioma = perguntar_idioma()
        frase = input("Digite uma frase para corrigir: ")
        correcao = corrigir_frase(frase, idioma, config)
    except ErroCorretor as erro:
        print(f"\nErro: {erro}", file=sys.stderr)
        return 1
    except(KeyboardInterrupt, EOFError):
        print("\nEncerrado.")
        return 130
    apresentar(correcao)
    return 0
    

