"""
    Testes do tratamento da resposta da LLM.
"""
import pytest

from corretor.erros import RespostaInvalida
from corretor.resposta import tratar_resposta
from tests.falsos import resposta_com

def test_resposta_normal():
    resposta = resposta_com(
        "Frase corrigida: Hello, how are you?\nO que mudou: Pontuação."
    )
    correcao = tratar_resposta(resposta)
    assert correcao.frase_corrigida == "Hello, how are you?"
    assert correcao.explicacao == "Pontuação."
    
    
def test_resposta_sem_o_rotulo_frase_corrigida():
    resposta = resposta_com("Hello, how are you?\nO que mudou: Pontuação.")
    assert tratar_resposta(resposta).frase_corrigida == "Hello, how are you?"
    

def test_remove_markdown_e_bloco_think():
    resposta = resposta_com(
        "<think>pensando</think>**Frase corrigida:** Hello.\n**O que mudou:** Nada mudou."
    )
    correcao = tratar_resposta(resposta)
    assert correcao.frase_corrigida == "Hello."
    assert correcao.explicacao == "Nada mudou."
    
    
@pytest.mark.parametrize(
    "resposta",
    [
        resposta_com(""),
        resposta_com("  "),
        resposta_com("<think>só pensamento</think>"),
        resposta_com("Hello, how are you?"),
        resposta_com("Frase corrigida: \nO que mudou: Pontuação."),
        {"outra_coisa": 1},
        {"message": {}},
        None,
    ],
)
def test_resposta_vazia_ou_fora_do_formato_e_recusada(resposta):
    with pytest.raises(RespostaInvalida):
        tratar_resposta(resposta)