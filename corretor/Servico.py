"""Fluxo completo de correção, compartilhado pelo terminal e depois pelo Streamlit.
"""
from corretor.config import Configuração
from corretor.Llm import chamar_modelo
from corretor.prompt import montar_mensagens
from corretor.Resposta import Correcao, tratar_resposta

def corrigir_frase(frase: str,
                idioma: str,
                config: Configuração,
                cliente=None
                ) -> Correcao:
    """ Valida a entrada, chama a LLM e devolve a correção já tratada."""
    mensagens = montar_mensagens(frase, idioma)
    reposta = chamar_modelo(config, mensagens, cliente)
    return tratar_resposta(reposta)