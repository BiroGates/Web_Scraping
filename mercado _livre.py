import time
import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver


class Mercadolivre:

    def __init__(self, nome_produto, url_base):

        # Pegando as variaveis nescessarias pra rodar o codigo
        self.navegador = webdriver.Chrome()
        self.url_base = url_base
        self.nome_produto = nome_produto
        self.lista_produto = []

    def scraping(self):
        # Iniciando a variavel pra passar as paginas
        paginas = np.arange(1, 151, 50)

        # Passando de pagina
        for pagina in paginas:

            # Abrindo o navegador pra debug
            self.navegador.get(self.url_base + self.nome_produto + f'_Desde_{pagina}')

            # Passando pelas paginas e pegando informações
            response = requests.get(self.url_base + self.nome_produto + f'_Desde_{pagina}')
            site = BeautifulSoup(response.text, 'html.parser')
            produtos = site.findAll('div', attrs={'class': 'ui-search-result__wrapper'})

            # Pegando os valores da pagina
            for produto in produtos:
                titulo = produto.find('h2', attrs={'ui-search-item__title'})
                real = produto.find('span', attrs={'class': 'price-tag-fraction'})

                print(titulo.text)
                print(f'R${real.text}')
                print()
                self.lista_produto.append([titulo.text, real.text])
            time.sleep(5)

    def to_planinha(self):
        # Transformando a lista em um planinha
        if not self.lista_produto:
            print('Não é possivel gerar um planinha vazia!')
        else:
            planinha = pd.DataFrame(self.lista_produto, columns=['Nome', 'Preços'])
            planinha.to_excel('Relogio.xlsx', index=False)


produto = input('Digite o nome do produto: ')

Mercadolivre(produto, 'https://lista.mercadolivre.com.br/').scraping()