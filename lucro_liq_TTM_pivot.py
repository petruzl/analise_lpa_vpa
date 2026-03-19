# Versão usando pivot tables (se você já tem dre_pivot)
lucro_liq_TTM_pivot = pd.DataFrame()

for empresa in lista_de_empresas:
    try:
        # Verificar se a empresa existe na pivot table
        if empresa in dre_pivot.index.get_level_values('DENOM_CIA'):
            # Pegar os valores do Lucro Líquido
            ll_valores = dre_pivot.loc[(empresa, 'Lucro/Prejuízo Consolidado do Período')]
            
            # Remover valores NaN e pegar os últimos 4 trimestres
            ll_valores_validos = ll_valores.dropna()
            
            if len(ll_valores_validos) >= 4:
                ll_ttm = ll_valores_validos.tail(4).sum()
            else:
                ll_ttm = ll_valores_validos.sum()  # Se não tem 4, soma todos disponíveis
                
            lucro_liq_TTM_pivot.loc[empresa, 'Lucro_Liquido_TTM'] = ll_ttm
            
            print(f"{empresa}: R$ {ll_ttm:,.2f}")
            
    except Exception as e:
        print(f"Erro em {empresa}: {e}")

print("\nLucro Líquido TTM calculado via pivot tables:")
print(lucro_liq_TTM_pivot.sort_values('Lucro_Liquido_TTM', ascending=False))