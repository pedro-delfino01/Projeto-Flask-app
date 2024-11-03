from sqlite3 import IntegrityError

from flask import request, jsonify

from database.sessao import db
from model.pagamentos import Pagamentos

def register_routes(app):
    @app.route("/importar-pagamentos/", methods=['POST'])
    def enviar_pagamentos():
        file_data = request.get_json()
        print(file_data)

        novo_pagamento = Pagamentos(
            processo=file_data.get('Processo'),
            orgao=file_data.get('Órgão'),
            unidade=file_data.get('Unidade'),
            data=file_data.get('Data'),
            empenho=file_data.get('Empenho'),
            credor=file_data.get('Credor'),
            pago=file_data.get('Pago'),
            retido=file_data.get('Retido'),
            anulacao=file_data.get('Anulação'),
            nota=file_data.get('Nota de Pagamento'),
            cnpj=file_data.get('CNPJ', None),
            ds_empenho=file_data.get('DsEmpenho'),
            ds_item_despesa=file_data.get('DsItemDespesa')
        )

        try:
            db.session.add(novo_pagamento)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return jsonify({'error': 'Erro de integridade ao inserir pagamento.'}), 400

        return jsonify({'mensagem': 'Transacao realizada'}), 200


    @app.route("/pagamentos/", methods=['GET'])
    def listar_pagamentos():

        pagamentos = Pagamentos.query.all()

        resultados = []
        for pagamento in pagamentos:
            result = {
                'orgao': pagamento.orgao,
                'unidade': pagamento.unidade,
                'data': pagamento.data,
                'empenho': pagamento.empenho,
                'processo': pagamento.processo,
                'credor': pagamento.credor,
                'pago': pagamento.pago,
                'retido': pagamento.retido,
                'anulacao': pagamento.anulacao,
                'nota': pagamento.nota,
                'cnpj': pagamento.cnpj,
                'ds_empenho': pagamento.ds_empenho,
                'ds_item_despesa': pagamento.ds_item_despesa
            }
            resultados.append(result)

        return jsonify(resultados), 200
