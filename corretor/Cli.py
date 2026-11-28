"""
    Terminal: captura da entrada e apresentação do resultado.
"""
import logging
import sys

from corretor.config import carregar_configuracao, resumo_seguro
from corretor.erros import ErroCorretor
from corretor.logs import configurar_logs
from corretor.prompt import IDIOMAS
from corretor.resposta import Correcao
from corretor.servico import corrigir_frase


logger = logging.getLogger(__name__)


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
        configurar_logs(config.log_nivel, config.log_arquivo)
        logger.info("execução iniciada: %s", resumo_seguro(config))
        idioma = perguntar_idioma()
        frase = input("Digite uma frase para corrigir: ")
        correcao = corrigir_frase(frase, idioma, config)
    except ErroCorretor as erro:
        print(f"\nErro: {erro}", file=sys.stderr)
        return 1
    except(KeyboardInterrupt, EOFError):
        print("\nEncerrado.")
        return 130
    except Exception as erro:
        # Último recurso: só o tipo do erro vai para o log e para a tela.
        logger.error("erro inesperado: %s", type(erro).__name__)
        print(
            f"\nErro inesperado ({type(erro).__name__}). Consulte o arquivo de logs. ", file=sys.stderr,
        )
        return 1
    apresentar(correcao)
    return 0
    

