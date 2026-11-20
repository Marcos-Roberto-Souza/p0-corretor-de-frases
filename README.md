<!-- fullWidth: true tocVisible: false tableWrap: true -->
# Corretor de Frases (Português e Inglês) com LLM

programa de terminal que recebe uma frase em português ou inglês e a envia a uma LLM (via Ollama)

para corrigir a Ortografia, gramática e pontuação, sem mudar o sentido da frase.

## Requisitos

- python 3.13
- Ollama instalado e rodando, comum modelo baixado ( por exemplo, 'ollama pull llama3.2 )

## Instalação

```bash
python -m venv .venv
```

```bash
source .venv/Scripts/activate.bat  #Git Bash;
#no PowerShell: .venv\Scripts\Activate.ps1
#no VsCode: .venv\Scripts\activate.bat
```

```bash
pip install -r requirements.txt # para instalar o ollama direto do terminal
```

## Configuração

O programa lê duas variáveis de ambiente. Ambas são opcionais.

| Variável       | Para que serve               | Padrão                   |
| -------------- | ---------------------------- | ------------------------ |
| "OLLAMA_HOST"  | Endereço do servidor Ollama  | "http://localhost:11434" |
| "OLLAMA_MODEL  | Modelo usado                 | "llama3.2                |

## Execução

```bash
python main.py
```

## Exemplo

Digite uma frase: hello how are you

Retorno: Hello, how are you?

O que mudou: Pontuação

### Limitações conhecidas

- Modelos pequenos podem inventar explicações ou ignorar o formato pedido.