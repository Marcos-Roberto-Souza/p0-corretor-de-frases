"""
   ****** Chamada ao modelo  *******
   
   Cria o cliente e traduz os erros do Ollama em erros do programa.
"""
import httpx
import ollama

from corretor.config import Configuracao
from corretor.erros import(
    ConfiguracaoInvalida,
    CredencialAusente,
    CredencialInvalida,
    FalhaDeComunicacao,
    ServidorIndisponivel,
    TempoEsgotado,
)

# Se manter a ** Temperatura baixa ** , terá respostas mais previsíveis, adequadas para correção de texto.
TEMPERATURA = 0 # Temperatura ajustada para 0

""" Função Cria o cliente do Ollama a partir da configuração."""
def criar_cliente(config: Configuracao) -> ollama.Client:
    
    cabecalhos = {}
    
    if config.api_key:
        cabecalhos["Authorization"] = f"Bearer {config.api_key}"
    
    return ollama.Client(
        
        host=config.host,
        verify=config.verificar_ssl,
        timeout=config.timeout,
        headers=cabecalhos,
    )
    
    
def _erro_para_status(status: int, config: Configuracao) -> Exception:
    # Função que define um código de erro HTTP do servidor e converte para um erro compreensível
    if status in (401, 403):
        if not config.api_key:
            return CredencialAusente(
                "O servidor exige credencial e nenhuma foi configurada. "
                "Defina a variável OLLAMA_API_KEY."
            )
        return CredencialInvalida(
            "O servidor recusou a credencial. Confira o valor de OLLAMA_API_KEY."
        )
    if status == 404:
        return ConfiguracaoInvalida(
            f"Omodelo '{config.modelo}' não foi encontrado no servidor. "
            "Confira a variável OLLAMA_MODEL."
        )
    if status in (502, 503, 504):
        return ServidorIndisponivel(
            "O servidor da LLM está indisponível ou sobrecarregado. "
            "Tente de novo em alguns minutos."
        )
    # Só o código aparece: o corpo da resposta pode ser uma página HTML enorme.
    return FalhaDeComunicacao(
        f"O servidor respondeu com um erro (código {status})."
        )
    
def chamar_modelo(config: Configuracao, mensagens: list[dict], cliente=None):
    """ Envia as mensagens ao modelo e devolve a resposta bruta. 
        O parâmetro 'cliente' existe para os testes: dá para passar um cliente falso e simular
        as respostas e erros sem usar a rede.
    """
        
    cliente = cliente or criar_cliente(config)
    try:
        return cliente.chat(
            model=config.modelo,
            messages=mensagens,
            options={"temperature": TEMPERATURA},
        )
    except ollama.ResponseError as erro:
        raise _erro_para_status(erro.status_code, config) from None
    except httpx.TimeoutException:
        raise TempoEsgotado(
            f"O servidor não respondeu em {config.timeout:g} segundos."
            "Tente de novo ou aumente OLLAMA_TIMEOUT."
        ) from None
    except(ConnectionError, httpx.HTTPError):
        raise FalhaDeComunicacao(
            "Não foi possível conectar ao servidor. Confira OLLAMA_HOST, "
            " e a rede e  se o servidor está rodando."
        ) from None
        
        
