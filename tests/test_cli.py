""" 
    Testes do terminal: códigos de saída e mensagens, sem rede e sem traceback.
"""
import contextlib
import io

from corretor.cli import main
from corretor.erros import EntradaInvalida
from corretor.resposta import Correcao


# Função simula o que o usuário digita e a correção, e evita gravar logs de verdade.
def _preparar(monkeypatch, entradas, corrigir):
    digitado = iter(entradas)
    monkeypatch.setattr("builtins.input", lambda *args, **kwargs: next(digitado))
    monkeypatch.setattr("corretor.cli.corrigir_frase", corrigir)
    monkeypatch.setattr("corretor.cli.configurar_logs", lambda *args, **kwargs: None)
    
def _rodar():
    saida, erro = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(saida), contextlib.redirect_stderr(erro):
        codigo = main()
    return codigo, saida.getvalue(), erro.getvalue()
    



def test_sucesso_mostra_a_correcao_e_sai_com_zero(monkeypatch):
    correcao = Correcao("Hello, how are you?", "Pontuação.")
    _preparar(monkeypatch,["en", "hello how are you"], lambda *a, **k: correcao)
    codigo, saida, _ = _rodar()
    assert codigo == 0
    assert "Frase corrigida: Hello, how are you?" in saida
    assert "O que mudou: Pontuação." in saida
    
    
def test_erro_esperado_mostra_a_mensagem_e_sai_com_um(monkeypatch):
    def recusa(*args, **kwargs):
        raise EntradaInvalida("Digite uma frase antes de enviar.")
    
    _preparar(monkeypatch, ["pt", ""], recusa)
    codigo, _, erro = _rodar()
    assert "Erro: Digite uma frase antes de enviar." in erro
    assert "Traceback" not in erro
    
    
    

def test_erro_inesperado_vira_mensagem_curta_sem_traceback(monkeypatch):
    def quebra(*args, **kwargs):
        raise RuntimeError("falha interna")
    
    _preparar(monkeypatch, ["pt", "oi"], quebra)
    codigo, _, erro = _rodar()
    assert codigo == 1
    assert "Erro inesperado (RuntimeError)" in erro
    assert "Traceback" not in erro
    assert "falha interna" not in erro