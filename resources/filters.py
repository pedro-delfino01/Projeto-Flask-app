from database.sessao import db
from model.pagamentos import Pagamentos

class Filters():

    def listar_todos_pagamentos(self):
        items = Pagamentos.query.all()
        return {
            "items": items
        }

    def filtrar_processo(processo):
        if processo is not None:
            items = Pagamentos.query.filter('Rrocesso' == processo)
        return {
            "items": items
        }

    def filtrar_orgao(orgao):
        if orgao is not None:
            items = Pagamentos.query.filter('Órgão' == orgao)
        return {
            "items": items
        }