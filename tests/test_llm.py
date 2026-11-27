"""
    Testes com integração simulada: erros do servidor viram mensagens claras.
"""
import httpx
import ollama
import pytest

from corretor.erros import(
    ConfiguracaoInvalida,
    CredencialAusente,
    CredencialInvalida,
    FalhaDeComunicacao,
    ServidorIndisponivel,
    TempoEsgotado,
)
from corretor.llm import chamar_modelo
from tests.falsos import ClienteFalso, resposta_com

MENSAGENS = [{"role": "user", "content": "oi"}]


def test_devolve_a_resposta_do_modelo(config):
    cliente = ClienteFalso(reposta=resposta_com("ok"))
    assert chamar_modelo(config, MENSAGENS, cliente) == resposta_com("ok")
    
    
@pytest.mark.parametrize("status", [401, 403])
def test_credencial_ausente(config, status):
    cliente = ClienteFalso(erro=ollama.ResponseError("nao autorizado", status))
    with pytest.raises(CredencialAusente):
        chamar_modelo(config, MENSAGENS, cliente)
        
        

@pytest.mark.parametrize("status", [401, 403])
def test_credencial_invalida(config_com_chave, status):
    cliente = ClienteFalso(erro=ollama.ResponseError("nao autorizado", status))
    with pytest.raises(CredencialInvalida) as info:
        chamar_modelo(config_com_chave, MENSAGENS, cliente)
    # A mensagem nunca pode conter a chave
    assert "chave-secreta-de-teste" not in str(info.value)
    
    
def test_modelo_inexistente(config):
    cliente = ClienteFalso(erro=ollama.ResponseError("not found", 404))
    with pytest.raises(ConfiguracaoInvalida) as info:
        chamar_modelo(config, MENSAGENS, cliente)
    assert "modelo-de-teste" in str(info.value)
    

@pytest.mark.parametrize("status", [502, 503, 504])
def test_servidor_indisponivel(config, status):
    cliente = ClienteFalso(erro=ollama.ResponseError("<html>página enorme</html>", status))
    with pytest.raises(ServidorIndisponivel) as info:
        chamar_modelo(config, MENSAGENS, cliente)
    assert "<html>" not in str(info.value)
    
    
def test_outro_codigo_mostra_so_o_numero(config):
    cliente = ClienteFalso(erro=ollama.ResponseError("<html>corpo</html>", 500))
    with pytest.raises(FalhaDeComunicacao) as info:
        chamar_modelo(config, MENSAGENS, cliente)
    assert "500" in str(info.value)
    assert "<html>" not in str(info.value)
    
def test_timeout(config):
    cliente = ClienteFalso(erro=httpx.TimeoutException("demorou muito"))
    with pytest.raises(TempoEsgotado):
        chamar_modelo(config, MENSAGENS, cliente)
        
        
def test_falha_de_conexao(config):
    cliente = ClienteFalso(erro=ConnectionError("Falha de conexão or Failed to connect"))
    with pytest.raises(FalhaDeComunicacao):
        chamar_modelo(config, MENSAGENS, cliente)
