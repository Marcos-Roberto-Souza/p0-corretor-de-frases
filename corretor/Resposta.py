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
    
    def separar_campos(texto: str) -> Correcao:
        """
        --- Separa a frase corrigida da explicação do Modelo.
        
        O modelo ás vezes esquece o rótulo "Frase corrigida:".
        Por isso o que vale é o rótulo "O que mudou: ": o texto antes dele é a frase corrigida.
        """
        partes = re.split(r"O que mudou: ", texto, maxsplit=1, flags=re.IGNORECASE)
        if len(partes) != 2:
            raise RespostaInvalida(
                "A resposta do modelo veio fora do formato esperado. Tente novamente. partes"
            )
        frase = re.sub(r"^\s*Frase corrigida: ", "", parte[0], flags=re.IGNORECASE).strip()
        explicacao = partes[1].strip()
        if not frase or not explicacao:
            raise RespostaInvalida(
                "A resposta do modelo veio incompleta. Tente novamente. explicacao"
            )
        return Correcao(frase_corrigida=frase, explicacao=explicacao)
        
        
    def tratar_resposta(resposta) -> Correcao:
        """
            Faz o camino completo: extraindo, limpando, confere se não é vazia a menssagem e separa.
        """
        texto = limpar_texto(extrair_texto(resposta))
        if not texto:
            raise RespostaInvalida(
                "O modelo devolveu uma resposta vazia. Tente novamente. tratar_resposta"
            )
        return separar_campos(texto)