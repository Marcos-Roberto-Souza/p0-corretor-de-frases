"""
    Teste do carregamento da configuração.
"""
import pytest

from corretor.config import carregar_configuracao
from corretor.erros import ConfiguracaoInvalida


def test_usa_os_valores_padrao():
    config = carregar_configuracao()
    assert config.host == "http://localhost:11434"
    assert config.modelo == "llama3.2"
    assert config.timeout == 60.0
    assert config.verificar_ssl is True
    assert config.api_key == ""
    assert config.temperatura == 0.0
    assert config.max_tokens == 1024
    
    
def test_limpa_espaco_e_aspas(monkeypatch):
    monkeypatch.setenv("OLLAMA_HOST", ' "https://servidor:9001" ')
    assert carregar_configuracao().host == "https://servidor:9001"
    
    
def test_host_sem_protocolo_e_recusado(monkeypatch):
    monkeypatch.setenv("OLLAMA_HOST", "servidor:9001")
    with pytest.raises(ConfiguracaoInvalida):
        carregar_configuracao()
        
        
def test_erro_de_host_nao_mostra_o_endereco(monkeypatch):
    monkeypatch.setenv("OLLAMA_HOST", "endereco-privado:9001")
    with pytest.raises(ConfiguracaoInvalida) as info:
        carregar_configuracao()
    assert "endereco-privado" not in str(info.value)
    

@pytest.mark.parametrize("valor", ["abc", "0", "-5"])
def test_timeout_invalido_e_recusado(monkeypatch, valor):
    monkeypatch.setenv("OLLAMA_TIMEOUT", valor)
    with pytest.raises(ConfiguracaoInvalida):
        carregar_configuracao()
        
def test_verificar_ssl_aceita_false(monkeypatch):
    monkeypatch.setenv("OLLAMA_VERIFY_SSL", "false")
    assert carregar_configuracao().verificar_ssl is False
    
def test_verificar_ssl_invalido_e_recusado(monkeypatch):
    monkeypatch.setenv("OLLAMA_VERIFY_SSL", "talvez")
    with pytest.raises(ConfiguracaoInvalida):
        carregar_configuracao()


def test_a_chave_nao_aparece_ao_imprimir_a_configuracao(monkeypatch):
    monkeypatch.setenv("OLLAMA_API_KEY", "chave-secreta-de-teste")
    config = carregar_configuracao()
    assert config.api_key == "chave-secreta-de-teste"
    assert "chave-secreta-de-teste" not in repr(config)
    


def test_le_os_parametros_do_modelo(monkeypatch):
    monkeypatch.setenv("OLLAMA_TEMPERATURE", "0.7")
    monkeypatch.setenv("OLLAMA_MAX_TOKENS", "256")
    config = carregar_configuracao()
    assert config.temperatura == 0.7
    assert config.max_tokens == 256
    
    
    
    
@pytest.mark.parametrize("valor", ["abc", "-1", "3"])
def test_temperatura_invalida_e_recusada(monkeypatch, valor):
    monkeypatch.setenv("OLLAMA_TEMPERATURE", valor)
    with pytest.raises(ConfiguracaoInvalida):
        carregar_configuracao()
        


@pytest.mark.parametrize("valor", ["abc", "0", "-5", "1.5"])
def test_max_tokens_invalido_e_recusado(monkeypatch, valor):
    monkeypatch.setenv("OLLAMA_MAX_TOKENS", valor)
    with pytest.raises(ConfiguracaoInvalida):
        carregar_configuracao()