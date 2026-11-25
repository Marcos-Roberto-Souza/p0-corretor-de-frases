""" ---- Tratamento da resposta: extrai o texto, limpa e separa os campos. -----
"""
import re
from dataclasses import dataclass
from corretor.erros import RespostaInvalida

@dataclass(frozen=True)
class Correcao:
    """Resultado de uma correção, já separado em dois campos."""
    frase_corrigida: str
    explicacao: str
    
    def extrair_texto(resposta) -> str:
        """ Pega o texto dentro da resposta bruta do LLM."""
        try:
            texto = resposta["message"]["content"]
        except (KeyError, TypeError):
            raise RespostaInvalida(
                "A resposta do modelo veio em um formato inesperado."
            ) from None
        if not isinstance(texto, str):
            raise RespostaInvalida(
                "A resposta do modelo veio em um formato inesperado. 'isinstance'"
            )
        return texto
    
    def limpar_texto(texto: str) -> str:
        """Remove o bloco <think> ..... </think> e os asteriscos do Markdown da pagina."""
        texto = re.sub(r"<think>.*?</think>", "", texto, flags=re.DOTALL)
        return texto.replace("**", "").strip()