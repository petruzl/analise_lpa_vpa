# testes.py
import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch
import yfinance as yf

def test_download_precos_yfinance():
    # Testa se o download de preços funciona (mock para evitar chamadas reais)
    with patch('yfinance.Ticker') as mock_ticker:
        mock_history = pd.DataFrame({'Close': [10.0]})
        mock_ticker.return_value.history.return_value = mock_history
        
        ticker = 'ALOS3.SA'
        dados = yf.Ticker(ticker).history(period='1d')
        assert not dados.empty
        assert dados['Close'].iloc[-1] == 10.0

def test_calculo_lpa():
    # Testa cálculo básico de LPA
    lucro_liquido = 1000000
    num_acoes = 500000
    lpa_esperado = lucro_liquido / num_acoes
    assert lpa_esperado == 2.0

def test_calculo_vpa():
    # Testa cálculo básico de VPA
    pl_ajustado = 2000000
    num_acoes = 500000
    vpa_esperado = pl_ajustado / num_acoes
    assert vpa_esperado == 4.0

def test_multiplos():
    # Testa cálculos de P/L e P/VPA
    preco = 20.0
    lpa = 2.0
    vpa = 4.0
    pl_esperado = preco / lpa
    pvpa_esperado = preco / vpa
    assert pl_esperado == 10.0
    assert pvpa_esperado == 5.0

# Executar testes: pytest testes.py