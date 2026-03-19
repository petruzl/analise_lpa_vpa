# main.py - Versão 100% Dinâmica
import pandas as pd
import yfinance as yf
import os
import numpy as np

print("=== INICIANDO PROCESSAMENTO DINÂMICO ===")

# 1. CONFIGURAÇÃO DE CAMINHOS
caminho_arquivos = r'C:\Users\leandro.petruz\selects_novo\tcc\itr'
arquivos_xls = [os.path.join(caminho_arquivos, f) for f in os.listdir(caminho_arquivos) if f.endswith(('.xls', '.xlsx'))]

# 2. CARREGAMENTO DE DADOS (BPP e DRE)
bpp_consolidado = pd.DataFrame()
dre_consolidado = pd.DataFrame()

for f in arquivos_xls:
    try:
        bpp_consolidado = pd.concat([bpp_consolidado, pd.read_excel(f, sheet_name='BPP')])
        dre_consolidado = pd.concat([dre_consolidado, pd.read_excel(f, sheet_name='DRE')])
        print(f"✓ Carregado: {os.path.basename(f)}")
    except Exception as e:
        print(f"✗ Erro em {os.path.basename(f)}: {e}")

# 3. CRIAÇÃO DAS PIVOT TABLES
bpp_pivot = pd.pivot_table(bpp_consolidado, index=['DENOM_CIA', 'DS_CONTA'], columns=['DT_FIM_EXERC'], values='VL_AJUSTADO')
dre_pivot = pd.pivot_table(dre_consolidado, index=['DENOM_CIA', 'DS_CONTA'], columns=['DT_FIM_EXERC'], values='VL_AJUSTADO')

# 4. CÁLCULO DO LUCRO LÍQUIDO TTM E PATRIMÔNIO LÍQUIDO
lucro_liq_TTM = pd.DataFrame()
patrimonio_liq = pd.DataFrame()

empresas = bpp_pivot.index.get_level_values('DENOM_CIA').unique()

for emp in empresas:
    # TTM
    try:
        ll_valores = dre_pivot.loc[(emp, 'Lucro/Prejuízo Consolidado do Período')].dropna()
        lucro_liq_TTM.loc[emp, 'Lucro_TTM'] = ll_valores.tail(4).sum()
    except: pass
    
    # PL Ajustado
    contas_pl = ['Patrimônio Líquido Consolidado', 'Patrimônio Líquido', 'Patrimônio Líquido Atribuído à Controladora']
    for c in contas_pl:
        try:
            if (emp, c) in bpp_pivot.index:
                patrimonio_liq.loc[emp, 'PL_Ajustado'] = bpp_pivot.loc[(emp, c)].dropna().iloc[-1]
                break
        except: continue

# 5. DOWNLOAD DINÂMICO DE PREÇOS E NÚMERO DE AÇÕES (YFINANCE)
tickers = [
    'BRSR3.SA',
    'BBAS3.SA',
    'ITUB3.SA',
    'BBDC3.SA',
    'SANB3.SA',
    'RAIZ4.SA',
    'VBBR3.SA',
    'UGPA3.SA',
    'AURE3.SA',
    'TAEE3.SA',
    'AXIA3.SA',
    'EGIE3.SA',
    'CPFE3.SA',
    'JHSF3.SA',
    'CYRE3.SA',
    'MRVE3.SA',
    'EZTC3.SA',
    'SAPR3.SA',
    'SBSP3.SA',
    'CSMG3.SA',
    'BBSE3.SA',
    'CXSE3.SA',
    'PSSA3.SA',
    'IRBR3.SA',
    'TOTS3.SA',
    'LWSA3.SA',
    'POSI3.SA',
    'MGLU3.SA',
    'LREN3.SA',
    'BHIA3.SA',
    'VALE3.SA',
    'GGBR4.SA',
    'CSNA3.SA',
    'JBSS3.SA',
    'MRFG3.SA',
    'BRFS3.SA'
]

ticker_para_empresa = {
    'BRSR3.SA': 'BCO ESTADO DO RIO GRANDE DO SUL S.A.',
    'BBAS3.SA': 'BCO BRASIL S.A.',
    'ITUB3.SA': 'ITAU UNIBANCO HOLDING S.A.',
    'BBDC3.SA': 'BCO BRADESCO S.A.',
    'SANB3.SA': 'BCO SANTANDER (BRASIL) S.A.',
    'RAIZ4.SA': 'RAÍZEN S.A.',
    'VBBR3.SA': 'VIBRA ENERGIA S/A',
    'UGPA3.SA': 'ULTRAPAR PARTICIPACOES S.A.',
    'AURE3.SA': 'AUREN ENERGIA S.A.',
    'TAEE3.SA': 'TRANSMISSORA ALIANÇA DE ENERGIA ELÉTRICA S.A.',
    'AXIA3.SA': 'CENTRAIS ELET BRAS S.A. - ELETROBRAS',
    'EGIE3.SA': 'ENGIE BRASIL ENERGIA S.A.',
    'CPFE3.SA': 'CPFL ENERGIA S.A.',
    'JHSF3.SA': 'JHSF PARTICIPACOES S.A.',
    'CYRE3.SA': 'CYRELA BRAZIL REALTY S.A.EMPREEND E PART',
    'MRVE3.SA': 'MRV ENGENHARIA E PARTICIPACOES S.A.',
    'EZTC3.SA': 'EZ TEC EMPREEND. E PARTICIPACOES S.A.',
    'SAPR3.SA': 'CIA. DE SANEAMENTO DO PARANÁ - SANEPAR',
    'SBSP3.SA': 'CIA SANEAMENTO BASICO EST SAO PAULO',
    'CSMG3.SA': 'CIA SANEAMENTO DE MINAS GERAIS-COPASA MG',
    'BBSE3.SA': 'BB SEGURIDADE PARTICIPAÇÕES S.A.',
    'CXSE3.SA': 'CAIXA SEGURIDADE PARTICIPAÇÕES S.A.',
    'PSSA3.SA': 'PORTO SEGURO S.A.',
    'IRBR3.SA': 'IRB - BRASIL RESSEGUROS S.A.',
    'TOTS3.SA': 'TOTVS S.A.',
    'LWSA3.SA': 'LWSA S/A',
    'POSI3.SA': 'POSITIVO TECNOLOGIA S.A.',
    'MGLU3.SA': 'MAGAZINE LUIZA S.A.',
    'LREN3.SA': 'LOJAS RENNER S.A.',
    'BHIA3.SA': 'GRUPO CASAS BAHIA S.A.',
    'VALE3.SA': 'VALE S.A.',
    'GGBR4.SA': 'GERDAU S.A.',
    'CSNA3.SA': 'CSN MINERAÇÃO S.A.',
    'JBSS3.SA': 'JBS S.A.',
    'MRFG3.SA': 'MARFRIG GLOBAL FOODS S.A.',
    'BRFS3.SA': 'BRF S.A.'
}

print("\n=== CONSULTANDO MERCADO (PREÇO + NÚMERO DE AÇÕES) ===")
resultados_finais = pd.DataFrame()

for tkt in tickers:
    try:
        obj = yf.Ticker(tkt)
        info = obj.info
        
        # Preço Atual
        hist = obj.history(period='1d')
        preco = hist['Close'].iloc[-1] if not hist.empty else np.nan
        
        # Número de Ações (DINÂMICO)
        n_acoes = info.get('sharesOutstanding', np.nan)
        
        # Nome da empresa para buscar nos dados CVM
        emp_nome = ticker_para_empresa.get(tkt)
        
        if emp_nome and pd.notna(n_acoes):
            # Os dados da CVM vêm em MILHARES (R$ 1.000), então multiplicamos o PL/Lucro por 1000
            # para igualar à unidade do número de ações do yfinance
            lucro = lucro_liq_TTM.loc[emp_nome, 'Lucro_TTM'] * 1000 if emp_nome in lucro_liq_TTM.index else np.nan
            pl = patrimonio_liq.loc[emp_nome, 'PL_Ajustado'] * 1000 if emp_nome in patrimonio_liq.index else np.nan
            
            lpa = lucro / n_acoes if pd.notna(lucro) else np.nan
            vpa = pl / n_acoes if pd.notna(pl) else np.nan
            
            resultados_finais.loc[tkt, 'Empresa'] = emp_nome
            resultados_finais.loc[tkt, 'Preco'] = preco
            resultados_finais.loc[tkt, 'LPA_TTM'] = lpa # Lucro por Ação TTM
            resultados_finais.loc[tkt, 'VPA'] = vpa
            resultados_finais.loc[tkt, 'P_L'] = preco / lpa #if lpa > 0 else np.nan
            resultados_finais.loc[tkt, 'P_VPA'] = preco / vpa #if vpa > 0 else np.nan
            resultados_finais.loc[tkt, 'N_Acoes_Yahoo'] = n_acoes
            
            print(f"✓ {tkt}: Preço {preco:.2f} | Ações: {n_acoes:,.0f}")
    except Exception as e:
        print(f"✗ Erro ao processar {tkt}: {e}")

# 6. SALVAR RESULTADOS
caminho_res = r'C:\Users\leandro.petruz\selects_novo\tcc\resultados'
os.makedirs(caminho_res, exist_ok=True)
resultados_finais.to_excel(os.path.join(caminho_res, 'LPA_VPA_Dinamico.xlsx'))

print(f"\n✅ Concluído! Arquivo salvo em: {caminho_res}")