import pandas as pd

from pipeline.agregacoes_delivery import AgregacoesDelivery
from pipeline.transformacoes_trusted import TransformacoesTrusted


def trusted_sem_banco():
    return TransformacoesTrusted.__new__(TransformacoesTrusted)


def test_normaliza_nome_para_chave_de_juncao():
    trusted = trusted_sem_banco()

    assert trusted._criar_chave_nome("Banco Itaú S.A. - Prudencial") == "ITAU"
    assert trusted._criar_chave_nome(None) == ""


def test_transformacao_de_bancos_cria_chave_e_preserva_cnpj_como_texto():
    trusted = trusted_sem_banco()
    bancos = pd.DataFrame({"Nome": ["Banco Itaú S.A."], "CNPJ": [123]})

    resultado = trusted._transformar_bancos(bancos)

    assert resultado.loc[0, "Nome_processed"] == "ITAU"
    assert resultado.loc[0, "CNPJ"] == "123"


class BancoEmMemoria:
    def __init__(self, tabelas):
        self.tabelas = tabelas
        self.envios = []

    def read_table(self, schema, table_name):
        return self.tabelas[(schema, table_name)].copy()

    def upload_df(self, dataframe, schema, table_name):
        self.envios.append((schema, table_name, dataframe.copy()))


def test_delivery_une_apenas_chaves_validas_e_publica_resultado():
    banco = BancoEmMemoria(
        {
            ("trusted", "bancos"): pd.DataFrame(
                {"CNPJ": ["1", "0"], "Nome_processed": ["ALFA", "IGNORAR"]}
            ),
            ("trusted", "reclamacoes"): pd.DataFrame(
                {"CNPJ IF": ["1", "0"], "valor": [10, 20]}
            ),
            ("trusted", "empregados"): pd.DataFrame(
                {"Nome_processed": ["ALFA"], "avaliacao": [5]}
            ),
        }
    )
    delivery = AgregacoesDelivery.__new__(AgregacoesDelivery)
    delivery.db = banco
    delivery.trusted_schema = "trusted"
    delivery.delivery_schema = "delivery"

    delivery.executar()

    assert len(banco.envios) == 1
    schema, tabela, resultado = banco.envios[0]
    assert (schema, tabela) == ("delivery", "bancos_unificados")
    assert resultado["CNPJ"].tolist() == ["1"]
    assert resultado["avaliacao"].tolist() == [5]
