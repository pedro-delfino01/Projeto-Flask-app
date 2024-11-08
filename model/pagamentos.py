from database.sessao import db


class Pagamentos(db.Model):
    __tablename__ = 'pagamentos'
    processo = db.Column(db.String(), primary_key=True, nullable=False)
    orgao = db.Column(db.String(), nullable=False)
    unidade = db.Column(db.String(), nullable=False)
    data = db.Column(db.String(), nullable=False)
    empenho = db.Column(db.String(10), nullable=False)
    credor =db.Column(db.String(), nullable=False)
    pago = db.Column(db.String(), nullable=False)
    retido = db.Column(db.String(), nullable=False)
    anulacao = db.Column(db.String(), nullable=False)
    nota = db.Column(db.String(), nullable=True)
    cnpj = db.Column(db.String(), nullable=False)
    ds_empenho = db.Column(db.String(), nullable=False)
    ds_item_despesa = db.Column(db.String(), nullable=False)
    is_deleted = db.Column(db.Boolean, default=False)