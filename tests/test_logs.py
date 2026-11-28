""" 
    Testes do resgistros: úteis para entender a execução, sem vazar dados.
"""
import logging
import os
import tempfile
import ollama
import pytest

from corretor.config import resumo_seguro
from corretor.erros import ServidorIndisponivel
from corretor.logs import configurar_logs
from corretor.servico import corrigir_frase
from tests.falsos import ClienteFalso, coletar_logs, resposta_com


def test_log_nao_contem_a_frase_a_resposta_nem_dados_de_acesso(config_com_chave):
    frase = "frase-secreta-do-usuario"
    cliente = ClienteFalso(
        resposta=resposta_com(
            "Frase corrigida: Texto corrigido secreto.\nO que mudou: Pontuação."
        )
    )
    with coletar_logs() as registros:
        corrigir_frase(frase, "pt", config_com_chave, cliente)
    texto = "\n".join(registros)
    assert "correção iniciada" in texto
    assert "correção concluida" in texto
    assert frase not in texto
    assert "Texto corrigido secreto" not in texto
    assert "chave-secreta-de-teste" not in texto
    assert "servidor-de-teste" not in texto
    
    
    def test_log_registra_o_tipo_do_erro_sem_o_corpo_da_resposta(config):
        cliente = ClienteFalso(erro=ollama.ResponseError("<html>corpo</html>", 504))
        with pytest.raises(ServidorIndisponivel):
            corrigir_frase("oi", "pt", config, cliente)
        texto = "\n".join(registros)
        assert "ServidorIndisponivel" in texto
        assert "<html>" not in texto
        
        
def test_resumo_da_configuracao_nao_mostra_endereco_nem_chave(config_com_chave):
    resumo = resumo_seguro(config_com_chave)
    assert "chave-secreta-de-teste" not in resumo
    assert "servidor-de-teste" not in resumo
    assert "credencial_configurada=True" in resumo
    

def test_configurar_logs_grava_no_arquivo():
    logger = logging.getLogger("corretor")
    with tempfile.TemporaryDirectory() as pasta:
        caminho = os.path.join(pasta, "subpasta", "corretor.log")
        try:
            configurar_logs("INFO", caminho)
            logging.getLogger("corretor.teste").info("mensagem de teste")
            for handler in logger.handlers:
                handler.flush()
            with open(caminho, encoding="utf-8") as arquivo:
                conteudo = arquivo.read()
        finally:
            # Fecha o arquivo antes da pasta temporária ser apagada no sistema --> (windows)
            for handler in list(logger.handlers):
                logger.removeHandler(handler)
                handler.close()
            # Devolve o handler silenciosamente, como o corretor/__init__.py deixa.
            logger.addHandler(logging.NullHandler())
    assert "mensagem de teste" in conteudo