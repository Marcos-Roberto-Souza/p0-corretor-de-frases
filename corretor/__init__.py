"""Corretor de frases (PT/EN) com LLM via Ollama."""
import logging

# Sem configuração, os logs do programa ficam em silêncio (em vez de
# aparecerem soltos no terminal). A cli.py configura a gravação em arquivo.
logging.getLogger(__name__).addHandler(logging.NullHandler())
