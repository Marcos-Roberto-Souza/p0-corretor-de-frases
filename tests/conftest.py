"""
    Configuração compartilhadas pelo testes.
"""
import pytest

from corretor.config import Configuracao

VARIAVEIS = (
    "OLLAMA_HOST",
    "OLLAMA_MODEL",
    "OLLAMA_TIMEOUT",
    "OLLAMA_VERIFY_SSL",
    "OLLAMA_API_KEY",
    "OLLAMA_TEMPERATURE",
    "OLLAMA_MAX_TOKENS",
    "LOG_LEVEL",
    "LOG_FILE",
)

@pytest.fixture(autouse=True)
def ambiente_limpo(monkeypatch):
    """ Isola os testes: sem variáveis OLLAMA_* e sem ler o .env real."""
    for nome in VARIAVEIS:
        monkeypatch.delenv(nome, raising=False)
    monkeypatch.setattr("corretor.config.load_dotenv", lambda *a, **k: False)
    

@pytest.fixture
def config():
    """ Configuração de teste, sem credencial."""
    return Configuracao(
        host="http://servidor-de-teste:11434",
        modelo="modelo-de-teste",
        timeout=5.0,
        verificar_ssl=True,
    )
    
    
@pytest.fixture
def config_com_chave():
    """ Configuração de teste, com uma credencial falsa."""
    return Configuracao(
        host="http://servidor-de-teste:11434",
        modelo="modelo-de-teste",
        timeout=5.0,
        verificar_ssl=True,
        api_key="chave-secreta-de-teste",
    )