# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3


class SpidapehPipeline(object):

    def __init__(self):
        self.criar_conexao()
        self.criar_tabela()

    def criar_conexao(self):
        self.con = sqlite3.connect("lista_celulares.db")
        self.cursor = self.con.cursor()

    def criar_tabela(self):
        self.cursor.execute("""DROP TABLE IF EXISTS lista_celulares""")
        self.cursor.execute("""create table lista_celulares(
            Nome text,
            Preco double,
            Tags text,
	    Qtde_tags int,
	    Link text
        )
        """)

    def process_item(self, item, spider):
        self.guardar_db(item)
        return item

    def guardar_db(self, item):
        if item['Tags'] == None:
            self.cursor.execute("""insert into lista_celulares values(
            ?, ?, ?, ?, ?
        )""",
        (
            item['Nome'],
            item['Preco'],
	    "null",
            0,
	    item['Link']
        ))
        else:
            tags = ''
            qtd_tags = 0
            for i in item['Tags']:
                if i == item['Tags'][-1]:
                    tags += i
                else:
                    tags += i + ', '
                qtd_tags += 1
            self.cursor.execute("""insert into lista_celulares values(
                ?, ?, ?, ?, ?
            )""",
            (
		item['Nome'],
		item['Preco'],
		tags,
		qtd_tags,
		item['Link']
            ))

        self.con.commit()
