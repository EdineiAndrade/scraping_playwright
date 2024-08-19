from datetime import datetime
import pandas as pd
import requests
import time
import uuid
import os

def baixar_imagem(lista_imagens,id_produto):
    print(f"====>> Baixando imagens")
    data_hora_atual = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    caminho_pasta = r'C:\Users\inec\Edinei\freelas\site_02_atacadum\arquivos'
    
    for index,imagem in enumerate(lista_imagens):
        time.sleep(.1)
        image_id = str(uuid.uuid4())
        limited_image_id = image_id[:12]
        image_name = f"{limited_image_id}.jpg"  
        
        if index == 0:
            image_name = f'{id_produto}_capa_{data_hora_atual}_{image_name}'
            caminho_arquivo = f'{caminho_pasta}\\imagens_capa\\{image_name}'
            imagem_capa = image_name
        else:    
            image_name = f'{id_produto}_produto_{data_hora_atual}_{image_name}'
            caminho_arquivo = f'{caminho_pasta}\\imagens_produtos\\{image_name}'
        try:
            resposta = requests.get(imagem)
            if resposta.status_code == 200:
                with open(caminho_arquivo, 'wb') as arquivo:
                    arquivo.write(resposta.content)
                print(f"Imagem baixada com sucesso: {image_name}")
                salvar_xlsx = salvar_arquivo_excel(id_produto,image_name,caminho_arquivo,imagem,caminho_pasta)
            else:
                print(f"Falha ao baixar a imagem. Status code: {resposta.status_code}")
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
    return imagem_capa
def salvar_arquivo_excel(id_produto,image_name,caminho_arquivo,imagem,caminho_pasta):
        time.sleep(.1)
        nome_arquivo_excel = "lista_imagens.xlsx"
        nome_arquivo_completo = f'{caminho_pasta}\\{nome_arquivo_excel}'        
        if os.path.exists(nome_arquivo_completo):
            df = pd.read_excel(nome_arquivo_completo)
        else:
            df = pd.DataFrame(columns=["id", "foto", "caminho_imagem","link_magem","STATUS"])
        if os.path.exists(caminho_arquivo):
            status = "BAIXADA"
        else:
            status = "NÃO BAIXADA"
        nova_linha = pd.DataFrame([{"id": int(id_produto), "foto": image_name, "caminho_imagem":caminho_arquivo, "link_magem": imagem, "STATUS": status}])
        df = pd.concat([df, nova_linha], ignore_index=True)
        # Salvar o DataFrame em um arquivo Excel (sobrescrever o arquivo existente)
        df.to_excel(nome_arquivo_completo, index=False)
        print(f"Arquivo Excel atualizado e salvo como {nome_arquivo_completo}")
        