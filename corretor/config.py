"""Carregamento da configuração a partir de variáveis de ambiente ( e do .env)."""

import os
from dataclasses import dataclass, field
from dotenv import load_dotenv
from corretor.erros import ConfiguracaoInvalida

HOST_PADRAO = "http://localhost:11434"  # Definindo o host padrão
MODELO_PADRAO = "llama3.2"  # Definindo um modelo local padrão se a conexão falhar
TIMEOUT_PADRAO = 60.0  # Definindo um tempo máximo para resposta
TEMPERATURA_PADRAO = 0.0
MAX_TOKENS_PADRAO = 1024
LOG_NIVEL_PADRAO = "INFO"
LOG_ARQUIVO_PADRAO = "logs/corretor.log"
NIVEIS_LOG("DEBUG", "INFO", "WARNING", "ERROR")

@dataclass(frozen=True)
class Configuracao:
    """Valores de configuração já validados."""

    host: str
    modelo: str
    timeout: float
    verificar_ssl: bool
    api_key: str = field (default="", repr=False)  # repr=False: se o objeto for impresso, a chave não aparece.
    temperatura: float = TEMPERATURA_PADRAO
    max_tokens: int = MAX_TOKENS_PADRAO
    log_nivel: str = LOG_NIVEL_PADRAO
    log_arquivo: str = LOG_ARQUIVO_PADRAO

    # Função para lê uma variável de ambiente, tirando espaços e aspas das pontas.
def _ler(nome: str, padrao: str = "") -> str:
    valor = os.environ.get(nome, "").strip().strip('"').strip("'")
    return valor or padrao

    # Funçãopara lê uma variável 'verdadeiro ou falso'.
def _ler_booleano(nome: str, padrao: bool) -> bool:
    valor = _ler(nome).lower()
    if not valor:
        return padrao
    if valor in ("1", "true", "sim", "yes"):
        return True
    if valor in ("0", "false", "nao", "não", "no"):
        return False
    raise ConfiguracaoInvalida(f"A variável {nome} deve ser 'true' ou 'false'.")

    # Função que lê o tempo limite em segundos e confere se é um número positivo.
def _ler_timeout() -> float:
    texto = _ler("OLLAMA_TIMEOUT", str(TIMEOUT_PADRAO))
    try:
        timeout = float(texto)
    except ValueError:
        raise ConfiguracaoInvalida(
            "A variável OLLAMA_TIMEOUT deve ser um número, em segundos."
        ) from None
    if timeout <= 0:
        raise ConfiguracaoInvalida(
            "A variável OLLAMA_TIMEOUT deve ser maior que zero."
        )
    return timeout


""" Função que lê a temperatura do modelo (de 0 a 2)."""
def _ler_temperatura() -> float:
    texto = _ler("OLLAMA_TEMPERATURE", str(TEMPERATURA_PADRAO))
    try:
        valor = float(texto)
    except ValueError:
        raise ConfiguracaoInvalida(
            "A variável OLLAMA_TEMPERATURE deve ser um número entre 0 e 2."
        ) from None
    if not 0 <= valor <=2:
        raise ConfiguracaoInvalida(
            "A variável OLLAMA_TEMPERATURE deve ser um número entre 0 e 2."
        )
    return valor



"""Funçaõ que lê o limite de tokens da resposta (número inteiro maior que zero)."""
def _ler_max_tokens() -> int:
    texto = _ler("OLLAMA_MAX_TOKENS", str(MAX_TOKENS_PADRAO))
    try:
        valor = int(texto)
    except ValueError:
        raise ConfiguracaoInvalida(
            "A variável OLLAMA_MAX_TOKENS deve ser um número inteiro."
        ) from None
    if valor <= 0:
        raise ConfiguracaoInvalida("A variável OLLAMA_MAX_TOKENS deve ser maior que zero.")
    return valor



# Função que lê o nivel dos logs (DEBUG, INFO, WARNING ou ERROR).
def _ler_nivel_log() -> str:
    nivel = _ler("LOG_LEVEL", LOG_NIVEL_PADRAO).upper()
    if nivel not in NIVEIS_LOG:
        raise ConfiguracaoInvalida(
            "A variável LOG_LEVEL deve ser DEBUG, INFO, WARNING ou ERROR."
        )
    return nivel


# Função descreve a configuração para os logs, sem o endereço nem a chave.
def resumo_seguro(config: Configuracao) -> str:
    return(
        f"modelo={config.modelo} timeout={config.timeout:g}s "
        f"verificar_ssl={config.verificar_ssl} temperatura={config.temperatura:g} "
        f"max_tokens={config.max_tokens} "
        f"credencial_configurada={bool(config.api_key)}"
    )


    # Função que lê e valida e devolve a configuração do programa.
def carregar_configuracao() -> Configuracao:
    # Se existir arquivo .env carrega as variáveis dele.
    # Variáveis já definidas no sistema têm prioridade.
    load_dotenv()
    host = _ler("OLLAMA_HOST", HOST_PADRAO)
    if not host.startswith(("http://", "https://")):
        # A mensagem não mostra o valo, para não expor endereços privados.
        raise ConfiguracaoInvalida(
            "A variável OLLAMA_HOST deve começar com http:// ou https://."
        )

    return Configuracao(
        host=host,
        modelo=_ler("OLLAMA_MODEL", MODELO_PADRAO),
        timeout=_ler_timeout(),
        verificar_ssl=_ler_booleano("OLLAMA_VERIFY_SSL", True),
        api_key=_ler("OLLAMA_API_KEY"),
        temperatura=_ler_temperatura(),
        max_tokens=_ler_max_tokens(),
        log_nivel = _ler_nivel_log(),
        log_arquivo=_ler("LOG_FILE", LOG_ARQUIVO_PADRAO),
    )
