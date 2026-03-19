#analise considerando o ano de 2024 e 2025
import pandas as pd
import requests
import zipfile
import io
import time
import os

start_time = time.time()

# Definir o caminho onde os arquivos serão salvos
caminho_salvar = r'C:\temp\itr'

# Criar o diretório se não existir
os.makedirs(caminho_salvar, exist_ok=True)

lista_cnpjs = [
'92.702.067/0001-96',
'00.000.000/0001-91',
'60.872.504/0001-23',
'60.746.948/0001-12',
'90.400.888/0001-42',
'33.453.598/0001-23',
'34.274.233/0001-02',
'33.256.439/0001-39',
'28.594.234/0001-23',
'07.859.971/0001-30',
'00.001.180/0001-26',
'02.474.103/0001-19',
'02.429.144/0001-93',
'08.294.224/0001-65',
'73.178.600/0001-18',
'08.343.492/0001-20',
'08.312.229/0001-73',
'76.484.013/0001-45',
'43.776.517/0001-80',
'17.281.106/0001-03',
'17.344.597/0001-94',
'22.543.331/0001-00',
'02.149.205/0001-69',
'33.376.989/0001-91',
'53.113.791/0001-22',
'02.351.877/0001-52',
'81.243.735/0001-48',
'47.960.950/0001-21',
'92.754.738/0001-62',
'33.041.260/0652-90',
'33.592.510/0001-54',
'33.611.500/0001-19',
'08.902.291/0001-15',
'02.916.265/0001-60',
'03.853.896/0001-40',
'01.838.723/0001-27'
]

demonstrativos = ['BPA', 'BPP', 'DRE']

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

r = requests.get('https://dados.cvm.gov.br/dados/CIA_ABERTA/CAD/DADOS/cad_cia_aberta.csv')
lines = [i.strip().split(';') for i in r.text.split('\n')]
df = pd.DataFrame(lines[1:], columns = lines[0])
acoes_setor_imobiliario  = df[df['CNPJ_CIA'].isin(lista_cnpjs)]
lista_listas = []
a = 0
for j in empresas:
  lista_df = []
  for k in demonstrativos:
    link = 'https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/ITR/DADOS/itr_cia_aberta_2025.zip'
    r = requests.get(link)
    zf = zipfile.ZipFile(io.BytesIO(r.content))
    arquivo = 'itr_cia_aberta_' + str(k) + '_con_2025.csv'
    dados = zf.open(arquivo)
    linhas = dados.readlines()
    lines = [i.strip().decode('ISO-8859-1') for i in linhas]
    lines = [i.split(';') for i in lines]
    df = pd.DataFrame(lines[1:], columns = lines[0])
    df['VL_AJUSTADO'] = pd.to_numeric(df['VL_CONTA'])
    filtro = df[df['CD_CVM']== str(j).zfill(6)]
    lista_df.append(filtro)
    print(f'Trabalhando com a empresa {j} e sua demonstração {k}. As dimensões são {filtro.shape} ')
  lista_listas.append(lista_df)
  
  # MODIFICAÇÃO AQUI: Adicionar o caminho completo ao nome do arquivo
  caminho_completo = os.path.join(caminho_salvar, f'Demonstrativos ITR Empresa {str(j)}.xlsx')
  writer = pd.ExcelWriter(caminho_completo, engine='xlsxwriter')
  
  lista_listas[a][0].to_excel(writer, sheet_name='BPA')
  lista_listas[a][1].to_excel(writer, sheet_name='BPP')
  lista_listas[a][2].to_excel(writer, sheet_name='DRE')
  a += 1
  print(f'Arquivo excel com os demonstrativos da empresa {j} já exportado. \n')
  writer.close()
print("O tempo de execução desse programa foi de %s segundos ---" % (time.time() - start_time))