from playwright.sync_api import Playwright, sync_playwright, expect
from baixar_imagem import baixar_imagem
from termcolor import colored
import pandas as pd
import time
import os

def run(playwright: Playwright) -> None:
                  
    browser = playwright.chromium.launch(args=["--window-position=380,0"],headless=False)
    context = browser.new_context()
    context.set_default_timeout(20000)
    page = context.new_page()    
    base_url = "https://www.atacadum.com.br/"
    page.goto(base_url)
    categorias = page.locator('//*[@class="categorias_desk"]/li/a').all()               
    for categoria in categorias:
        time.sleep(1)
        try:
            try:    
                categoria_nome = categoria.locator("span").inner_text()
                print(colored(f"====>> Informações do produto: Categoria --> {categoria_nome}",'green'))
                link_categoria = categoria.get_attribute("href")            
                if link_categoria == 'ofertas/':
                    continue
                n = 1
                url_categoria = f"{base_url}{link_categoria}?page={n}"
                page.goto(url_categoria)
                paginas = page.locator('//*[@class="col text-center"]/select/option').all()
                total_paginas = len(paginas)
                for n in range(1,int(total_paginas)+1):
                    url_categoria = f"{base_url}{link_categoria}?page={n}"
                    if n > 1:
                        page.goto(url_categoria)  
                    produtos = page.locator('//*[@class="produtos"]/div/div/div').all()
                    for produto in produtos:
                        time.sleep(1)
                        id_produto = produto.first.get_attribute('data-id')
                        link_produto = produto.locator("a").first.get_attribute('href')
                        page.goto(f"{base_url}{link_produto}")
                        nome_produto = page.locator('//*[@class="detalhes"]/h3').inner_text()
                        valor_custo = page.locator('(//*[@class="valor"])[1]/span[1]').inner_text()
                        valor_custo = valor_custo.replace('R$', '').replace('.', '').replace(',', '.').strip()
                        valor_custo = float(valor_custo)
                        valor_corrigido = round(valor_custo * 2 * 1.2,2)
                        print(colored(f"====>> Informações do produto: Nome: {nome_produto}",'green'))
                        cores = page.locator('(//*[@class="list"])[1]/div').all()
                        lista_cores = []
                        for cor in cores:
                            cor_nome = cor.get_attribute('data-original-title')
                            lista_cores.append(cor_nome)
                        lista_cor =', '.join(str(lista_cores) for cor in lista_cores if cor is not None)
                        descricao = page.locator('(//*[@class="texto"])[1]/p').all()
                        todas_descricoes = []
                        for p in descricao:
                            texto_descricao = p.inner_text()
                            todas_descricoes.append(texto_descricao)
                        descricao_completa = " ".join(todas_descricoes)
                        imagens = page.locator('(//*[@class="slick-track"])[1]/div/img').all()
                        lista_imagens = []
                        for imagem in imagens:
                            link_imagem = imagem.get_attribute('src')
                            lista_imagens.append(link_imagem)
                        #link_video = page.locator('(//*[@class="item video slick-slide"])[1]/iframe').get_attribute('src')
                        iframe = page.locator('(//*[@class="item video slick-slide"])[1]/iframe').first
                        # Verifique se o iframe foi encontrado e tente pegar o atributo 'src'
                        link_video = iframe.get_attribute('src') if iframe.count() > 0 else None
                        if link_video:
                            print(f"Link do vídeo: {link_video}")
                        else:
                            print("Elemento não encontrado.")
                        imagem_capa = baixar_imagem(lista_imagens,id_produto)
                        product_info = {
                                        'nome': nome_produto,
                                        'valor': valor_corrigido,
                                        'valor_promo': 0.00,
                                        'estoque': 100,
                                        'nivel': 10,
                                        'categoria': categoria_nome,
                                        'subcategoria': 0,
                                        'envio': 'Melhor Envio',
                                        'frete': 0.00,
                                        'promocao': 'Não',
                                        'imagem': imagem_capa,
                                        'marca':"",
                                        'modelo':"",
                                        'peso': 'peso_decimal',
                                        'largura':0,
                                        'altura':0,
                                        'comprimento':0,
                                        'palavras':"",
                                        'descricao':descricao_completa,
                                        'nome_url':"",
                                        'ativo':"Sim",
                                        'vendas':0,
                                        'loja':79,
                                        'carac':'<br>',
                                        'nota':0,
                                        'video':link_video,
                                        'nome_frete':"",
                                        'id_fornecedor':0,
                                        'id_produto':id_produto,
                                        'valor_custo':valor_custo,
                                        'lista_cores': lista_cor
                                    }
                        page.go_back()
                        df_produto = pd.DataFrame([product_info])            
                        update_excel_file(df_produto)
            except Exception as e:
                        print(f"Erro {e}")
        except Exception as e:
            print(f"Erro {e}")
            continue 
    print(colored(f"====>> Informações buscadas: categoria: {categoria} Produto: {nome_produto}",'green'))
       
def update_excel_file(df_produto):
    nome_arquivo_excel = r"C:\Users\inec\Edinei\freelas\site_02_atacadum\arquivos\lista_produtos.xlsx"
    if os.path.exists(nome_arquivo_excel):    
        df = pd.read_excel(nome_arquivo_excel)
    else:
        df = pd.DataFrame(columns=df_produto.keys())
        df.to_excel(nome_arquivo_excel, index=False)
        print(colored(f"====>> Criando arquivo excel {nome_arquivo_excel}",'green'))
    # Carregar o arquivo existente
    print(colored("====>> Inserindo as informações do arqiovo Excel",'green'))
    # Adicionar a nova linha de informações
    df = pd.concat([df, df_produto], ignore_index=True)    
    # Salvar as atualizações
    df.to_excel(nome_arquivo_excel, index=False)
    print(colored("====>> Informações inseridas!!",'green'))  
    
def buscar_dados():
    with sync_playwright() as playwright:
        run(playwright)
        
buscar_dados()

