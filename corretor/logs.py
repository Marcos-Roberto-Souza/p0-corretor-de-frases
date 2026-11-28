""" Registros simples da execução.

Os logs mostram o que aconteceu (etapas, duração, tipo de erro), mas nunca a frase digitada,
a resposta do modelo, a chave de acesso nem o endereço do servidor.

"""
import logging
from pathlib import Path

NOME = "corretor"
FORMATO = "%(asctime)s %(levelname)s %(name)s: %(menssage)s"


""" Função que configura o logger do programa para gravar em um arquivo."""
def configurar_logs(nivel: str, arquivo: str) -> None:
    logger = logging.getLogger(NOME)
    logger.setLevel(nivel)
    logger.propagate = False
    # Remove handlers antigos, para não duplicar linhas se for chamado de novo.
    for antigo in list(logger.handlers):
        logger.removeHandler(antigo)
        antigo.close()
        
    try:
        caminho = Path(arquivo)
        caminho.parent.mkdir(parents=True, exist_ok=True)
        handler = logging.FileHandler(caminho, encoding="utf-8")
    except OSError:
        # Se não der para gravar o arquivo o programa segue sem registrar.
        handler = logging.NullHandler()
    handler.setFormatter(logging.Formatter(FORMATO))
    logger.addHandler(handler)