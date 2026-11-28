"""
    Testes com integração simulada: erros do servidor viram mensagens claras.
"""
import dataclasses
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
    cliente = ClienteFalso(resposta=resposta_com("ok"))
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
    assert "O modelo 'modelo-de-teste' não foi encontrado" in str(info.value)
    

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
    with pytest.raises(TempoEsgotado) as info:
        chamar_modelo(config, MENSAGENS, cliente)
    assert "5 segundos. Tente de novo" in str(info.value)
    
    
        
def test_falha_de_conexao(config):
    cliente = ClienteFalso(erro=ConnectionError("Falha de conexão or Failed to connect"))
    with pytest.raises(FalhaDeComunicacao) as info:
        chamar_modelo(config, MENSAGENS, cliente)
    assert "Confira OLLAMA_HOST, a rede e se o servidor está rodando." in str(info.value)
    
    
def test_envia_os_parametro_configurados(config):
    config = dataclasses.replace(config, temperatura=0.5, max_tokens=100)
    cliente = ClienteFalso(resposta=resposta_com("ok"))
    chamar_modelo(config, MENSAGENS, cliente)
    assert cliente.ultimos_argumentos["options"] == {
        "temperature": 0.5,
        "num_predict": 100,
    }