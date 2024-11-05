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

    @app.route('/pagamentos/filtro', methods=['GET'])
    def listar_pagamentos_com_filtros():
        processo = request.args.get('processo')
        orgao = request.args.get('orgao')
        query = Pagamentos.query

        if processo:
            query = query.filter_by(processo=processo)
        if orgao:
            query = query.filter_by(orgao=orgao)

        resultados = []
        pagamentos_filtrados = query.all()
        for pagamento in pagamentos_filtrados:
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

    @app.route('/transacao/<int:processo>/editar', methods=['PUT'])
    def atualizar_pagamento(processo):
        data = request.get_json()
        pagamento = Pagamentos.query.get_or_404(processo)

        pagamento.orgao = data.get('orgao', pagamento.orgao)
        pagamento.unidade = data.get('unidade', pagamento.unidade)
        pagamento.data = data.get('data', pagamento.data)
        pagamento.empenho = data.get('empenho', pagamento.empenho)
        pagamento.processo = data.get('processo', pagamento.processo)
        pagamento.credor = data.get('credor', pagamento.credor)
        pagamento.pago = data.get('pago', pagamento.pago)
        pagamento.retido = data.get('retido', pagamento.retido)
        pagamento.anulacao = data.get('anulacao', pagamento.anulacao)
        pagamento.nota = data.get('nota', pagamento.nota)
        pagamento.cnpj = data.get('cnpj', pagamento.cnpj)
        pagamento.ds_empenho = data.get('ds_empenho', pagamento.ds_empenho)
        pagamento.ds_item_despesa = data.get('ds_item_despesa', pagamento.ds_item_despesa)

        db.session.commit()

        return jsonify({'message': 'Pagamento atualizado com sucesso!'}), 200

    @app.route('/pagamentos/<processo>/remover/', methods=['DELETE'])
    def deletar_transacao(processo):
        pagamento = Pagamentos.query.get_or_404(processo)

        db.session.delete(pagamento)
        db.session.commit()

        return jsonify({'message': 'Pagamento deletado com sucesso!'}), 200