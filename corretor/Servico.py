"""Fluxo completo de correção, compartilhado pelo terminal e depois pelo Streamlit.
"""
import logging
import time

from corretor.config import Configuracao
from corretor.llm import chamar_modelo
from corretor.prompt import montar_mensagens
from corretor.resposta import Correcao, tratar_resposta

logger = logging.getLogger(__name__)


def corrigir_frase(frase: str,
                idioma: str,
                config: Configuracao,
                cliente=None
                ) -> Correcao:
    """ 
        Valida a entrada, chama a LLM e devolve a correção já tratada.
    
    Os logs registram só o idioma, o tamanho da frase, a duração e o tipo de erro.
    A frase e a resposta nunca vão para o log.

    """
    inicio = time.perf_counter()
    logger.info(
        "correção inicianda: idioma=%s tamanho_da_frase=%d", idioma, len(frase.strip())
    )
    try:
        mensagens = montar_mensagens(frase, idioma)
        resposta = chamar_modelo(config, mensagens, cliente)
        correcao = tratar_resposta(resposta)
    except ErroCorretor as erro:
        logger.warning(
            "correção falhou: erro=%s duracao=%.2fs",
            type(erro).__name__,
            time.perf_counter() - inicio,
        )
        raise logger.info(
            "correção concluida: duracao=%2fs", time.perf_counter() - inicio
        )
    return correcao