# coding: utf-8

import os
from scrapy.crawler import CrawlerProcess
import sqlite3


def main():
    
    while(True):
        os.system('clear')
        print("--------------------- BUSCADOR DE CELULARES ---------------------")
        print("Digite uma opção:")
        print("1 - Atualizar banco de dados")
        print("2 - Pesquisar no banco de dados")
        print("0 - Sair")
        op = input(">>> ")

        if op == '1':
            profundidade = input("Digite quantas páginas deseja pesquisar: ")
            atualizar(profundidade)
            print()
            input("Pesquisa realizada com sucesso! Pressione enter para continuar....")
            main()

        elif op == '2':    
            palavra_chave = input("Digite uma palavra-chave para o celular: ")
            preco = input("Digite um preco base (Digite 'n' para mostrar todos os resultados): ")
            if preco == 'n':
                conecta_bd2('lista_celulares.db', palavra_chave)
                print()
                input("Pressione enter para continuar....")
            else:
                conecta_bd('lista_celulares.db', palavra_chave, preco)
                print()
                input("Pressione enter para continuar....")
            main()
        
        elif op == '0':
            exit()
        
        else:
            print()
            input("Opção inválida, tecle Enter para tentar novamente.")
            main()



def preco_minimo(preco):
    preco_min = 0.5 * float(preco)
    
    return str(preco_min)


def preco_maximo(preco):
    preco_max = float(preco) * 1.3

    return str(preco_max)
    

def atualizar(profundidade):
    profundidade = int(profundidade) - 1
    os.system("scrapy runspider -s DEPTH_LIMIT=" + str(profundidade) + " scraper.py")
    # c = CrawlerProcess({
    #     'DEPTH_LIMIT': profundidade
    # })
    # c.crawl(scraper.SpiderBuscape)
    # c.start()


def conecta_bd(nome, palavra, preco):
    bd = sqlite3.connect(nome)
    palavra = '"' + '%' + palavra + '%' + '"'
    preco_max = preco_maximo(preco)
    preco_min = preco_minimo(preco)

    bd.row_factory = sqlite3.Row
    cursor = bd.cursor()
    cursor.execute("SELECT nome,preco,tags,link FROM lista_celulares where nome in (SELECT nome from lista_celulares where (nome like " + palavra + " or tags like " + palavra + ") and qtde_tags > 0 and (preco BETWEEN " + preco_min + " and " + preco_max + ")) order by preco asc")
    resultado = [dict(row) for row in cursor.fetchall()]
    
    print('------------------------------------------------------------')
    print('CELULARES ENCONTRADOS:')
    print('------------------------------------------------------------')
    for i in resultado:
        print(i['Nome'] + ': R$ ' + str(i['Preco']) + ', link: ' + i['Link'])
        print('------------------------------------------------------------')


def conecta_bd2(nome, palavra):
    bd = sqlite3.connect(nome)
    palavra = '"' + '%' + palavra + '%' + '"'


    bd.row_factory = sqlite3.Row
    cursor = bd.cursor()
    cursor.execute("SELECT nome,preco,tags,link FROM lista_celulares where nome in (SELECT nome from lista_celulares where (nome like " + palavra + " or tags like " + palavra + ") and qtde_tags > 0) order by preco asc")
    resultado = [dict(row) for row in cursor.fetchall()]
    
    print('------------------------------------------------------------')
    print('CELULARES ENCONTRADOS:')
    print('------------------------------------------------------------')
    for i in resultado:
        print(i['Nome'] + ': R$ ' + str(i['Preco']) + ', link: ' + i['Link'])
        print('------------------------------------------------------------')

if __name__ == "__main__":
    main()