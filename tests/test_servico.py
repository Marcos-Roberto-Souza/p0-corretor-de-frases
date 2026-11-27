"""
    Testes do fluxo completo, do texto digitado até a correção final.
"""
import pytest

from corretor.erros import EntradaInvalida, RespostaInvalida
from corretor.servico import corrigir_frase
from tests.falsos import ClienteFalso, resposta_com



def test_fluxo_completo(config):
    cliente = ClienteFalso(
        resposta=resposta_com(
            "Frase corrigida: Hello, how are you?\nO que mudou: Pontuação."
        )
    )
    correcao = corrigir_frase("hello how are you", "en", config, cliente)
    assert correcao.frase_corrigida == "Hello, how are you?"
    assert cliente.chamadas == 1
    

def test_entrada_vazia_nao_chama_o_modelo(config):
    cliente = ClienteFalso(resposta=resposta_com("x"))
    with pytest.raises(EntradaInvalida):
        corrigir_frase("  ", "pt", config, cliente)
    assert cliente.chamadas == 0
    

def test_resposta_vazia_vira_erro_claro(config):
    cliente = ClienteFalso(resposta=resposta_com(""))
    with pytest.raises(RespostaInvalida):
        corrigir_frase("oi", "pt", config, cliente)