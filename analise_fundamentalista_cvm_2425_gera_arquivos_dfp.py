import pandas as pd
import requests
import zipfile
import io
import time
import os

# Definir o caminho onde os arquivos serão salvos
caminho_salvar = r'C:\Users\leandro.petruz\selects_novo\tcc\dfp'

# Criar o diretório se não existir
os.makedirs(caminho_salvar, exist_ok=True)

# Suas listas de empresas (coloque aqui as listas do seu código original)
empresas = [
'001210',
'001023',
'019348',
'000906',
'020532',
'025917',
'024295',
'018465',
'026620',
'020257',
'002437',
'017329',
'018660',
'020605',
'014460',
'020915',
'020770',
'018627',
'014443',
'019445',
'023159',
'023795',
'016659',
'024180',
'019992',
'024910',
'020362',
'022470',
'008133',
'006505',
'004170',
'003980',
'025585',
'020575',
'020788',
'016292'   
]

start_time = time.time()
demonstrativos = ['DRE']
lista_listas = []
a = 0

for j in empresas: 
    c = 0
    lista_df = []
    for k in demonstrativos:
        link = 'https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/DFP/DADOS/dfp_cia_aberta_2024.zip' 
        r = requests.get(link)
        zf = zipfile.ZipFile(io.BytesIO(r.content))
        arquivo = 'dfp_cia_aberta_' + str(k) + '_con_2024.csv' 
        zf = zf.open(arquivo)
        lines = zf.readlines()
        lines = [i.strip().decode('ISO-8859-1') for i in lines]
        lines = [i.split(';') for i in lines]
        c += 1
        df = pd.DataFrame(lines[1:], columns = lines[0])
        df['VL_AJUSTADO'] = pd.to_numeric(df['VL_CONTA'])
        filtro = df[df['CD_CVM'] == j] 
        lista_df.append(filtro)
        print(f'Trabalhando com a empresa {j} e sua demonstração {k}. As dimensões são {filtro.shape} ')
    
    lista_listas.append(lista_df)
    
    # MODIFICAÇÃO AQUI: Adicionar o caminho completo ao nome do arquivo
    caminho_completo = os.path.join(caminho_salvar, f'Demonstrativos DFP Empresa {str(j)}.xlsx')
    writer = pd.ExcelWriter(caminho_completo, engine='xlsxwriter')
    
    lista_listas[a][0].to_excel(writer, sheet_name='DRE')
    a += 1
    print(f'Arquivo excel com os demonstrativos da empresa {j} já exportado. \n')
    writer.close()

print("O tempo de execução desse programa foi de %s segundos ---" % (time.time() - start_time))