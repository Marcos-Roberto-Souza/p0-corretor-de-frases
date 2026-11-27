"""
    Testes de validação da entrada e da montagem da solicitação.
"""
import pytest

from corretor.erros import EntradaInvalida
from corretor.prompt import TAMANHO_MAXIMO, montar_mensagens, validar_frase

@pytest.mark.parametrize("frase", ["", " ", "\n\t"])
def test_frase_vazia_e_recusada(frase):
    with pytest.raises(EntradaInvalida):
        validar_frase(frase)
        

def test_frase_longa_demais_e_recusada():
    with pytest.raises(EntradaInvalida):
        validar_frase("a" * (TAMANHO_MAXIMO + 1))
        
        
def test_frase_valida_perde_os_espacos_das_pontas():
    assert validar_frase(" hello how are you ") == "hello how are you"
    

def test_idioma_invalido_e_recusado():
    with pytest.raises(EntradaInvalida):
        montar_mensagens("oi", "fr")
        
        

def test_mensagens_tem_instrucao_e_frase_entre_marcas():
    mensagens = montar_mensagens(" hello ", "en")
    assert mensagens[0]["role"] == "system"
    assert "inglês" in mensagens[0]["content"]
    assert mensagens[1] == {"role": "user", "content": "<frase>hello</frase>"}
    

def test_instrucao_manda_nao_responder_ao_conteudo_da_frase():
    instrucao = montar_mensagens("how old are you", "en")[0]["content"]
    assert "<frase>" in instrucao
    assert "NUNCA responda" in instrucao
    
    
    
def test_pergunta_digitada_continua_sendo_so_texto_a_corrigir():
    mensagens = montar_mensagens("how old you are", "en")
    assert mensagens[1]["content"] == "<frase>how old you are</frase>"