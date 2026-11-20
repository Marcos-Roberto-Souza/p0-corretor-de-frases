"""
    Projeto de um corretor de frases (português e inglês)
    pelo terminal, usando uma LLM via Ollama.
"""
import os
import ollama

# O endereço do servidor e o modelo vêm de variáveis de ambiente.
# Se elas não existirem, usa o Ollama instalado no próprio computador.
HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
MODELO = os.environ.get("OLLAMA_MODEL", "llama3.2")

# Instruções de sistema: que define o papel da LLM e o formato de resposta.
INSTRUCAO = (
    "Você é um corretor de textos. A frase do usuário pode estar em "
    "português do Brasil ou em inglês. Corrija ortografia, gramática, "
    "pontuação e acentuação NO MESMO IDIOMA da frase. "
    "NUNCA traduza a frase. Mantenha todas as palavras, sem remover nem "
    "acrescentar nada além das correções. "
    "Responda em texto simples, sem Markdown, neste formato:\n"
    "Frase corrigida: <a frase corrigida completa>\n"
    "O que mudou: <liste só as correções que você de fato fez, em português "
    "do Brasil. Não invente mudanças.>\n"
    "Se a frase corrigida for idêntica à original, escreva em 'O que mudou': "
    "Nada mudou.\n"
    "Exemplos:\n"
    "Entrada: ela nao gosta de cafe\n"
    "Frase corrigida: Ela não gosta de café.\n"
    "O que mudou: Acentos em 'não' e 'café', maiúscula inicial e ponto final.\n"
    "Entrada: they was happy yesterday\n"
    "Frase corrigida: They were happy yesterday.\n"
    "O que mudou: 'was' virou 'were' (concordância com 'they'), maiúscula "
    "inicial e ponto final."
)

# Função da correção do texto do usuário
def corrigir(frase: str) -> str:
    # Envia a frase para o LLM e devolve a resposta correta.
    cliente = ollama.Client(host=HOST)
    resposta = cliente.chat(
        model=MODELO,
        messages=[
            {"role": "system", "content": INSTRUCAO},
            {"role": "user", "content": frase},
        ],
        # Temperatura baixa: respostas mais previsíveis, boas para correção.
        options={"temperature": 0},
    )
    return resposta["message"]["content"]

# Função que recebe a frase do usuário e depois retorna a correção.
def main() -> None:
    """Lê uma frase do terminal e mostra a correção."""
    frase = input("Digite uma frase: ")
    print()
    print(corrigir(frase))
    
if __name__ == "__main__":
    main()
else:
    print("problema na saida main")

    