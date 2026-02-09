import pandas as pd
import random
from datetime import datetime, timedelta
import os

class GerandoDados:
    """
    Classe responsável por gerar uma base de dados
    simulando operações logísticas.
    """

    def __init__(self, qtd_linhas=5000, caminho_saida="dados"):
        self.total_linhas = qtd_linhas
        self.caminho_saida = caminho_saida
        self.nome_arquivo = "base_entregas_brutas.xlsx"

        os.makedirs(self.caminho_saida, exist_ok=True)

        self.filiais = ["SP", "RJ", "MG", "PR", "RS", "SC", None]

        self.clientes = [
            "Magazine Luiza", "Americanas",
            "Mercado Livre", "Shopee",
            "Amazon", None
        ]

        self.status_entrega = [
            "ENTREGUE", "entregue", "Entregue ", "ATRASADO",
            "Atrasado", " atrasado", "EM TRANSITO", "Em trânsito",
            None
        ]

        self.descricoes = [
            "Entrega realizada no prazo", "Entrega com atraso por chuva",
            "Cliente ausente no local", "Problema operacional na rota",
            "Entrega reagendada", "Extravio temporário", "Entrega EXPRESSA",
            "Entrega normal", None
        ]

        self.tipos_servico = ["EXPRESS", "Normal", "econômico", "EXPRESSA", None]


    def gerar_data_postagem(self):
        """
        Gera uma data aleatória nos últimos 30 dias.
        """
        hoje = datetime.today()
        dias_atras = random.randint(0, 30)
        return hoje - timedelta(days=dias_atras)


    def gerar_registro(self):
        """
        Gera um único registro de entrega.
        """
        return {
            # ID repetido propositalmente para gerar duplicatas
            "id_entrega": random.randint(1, 4000),

            # Filial com valores ausentes
            "filial": random.choice(self.filiais),

            # Cliente com valores nulos
            "cliente": random.choice(self.clientes),

            # Status propositalmente despadronizado
            "status": random.choice(self.status_entrega),

            # Texto livre para análise de palavras-chave
            "descricao_entrega": random.choice(self.descricoes),

            # Tipo de serviço sem padrão
            "tipo_servico": random.choice(self.tipos_servico),

            "valor_frete": round(random.uniform(15, 350), 2),
            "data_postagem": self.gerar_data_postagem(),

            # Prazo previsto (em dias)
            "prazo_previsto": random.choice([1, 2, 3, 5, 7, None]),

            "dias_atraso": random.choice([0, 0, 0, 1, 2, 3, None])
        }


    def gerar_dataframe(self):
        """
        Gera o DataFrame principal com dados brutos.
        """

        df = pd.DataFrame(
            self.gerar_registro() for _ in range
            (self.total_linhas)
        )

        return df


    def inserir_duplicatas(self, df, quantidade=200):
        """
        Insere linhas duplicadas propositalmente.
        """
        duplicatas = df.sample(quantidade)
        df_final = pd.concat([df, duplicatas], ignore_index=True)
        df_final = df_final.sample(frac=1).reset_index(drop=True)

        return df_final


    def salvar_excel(self, df):
        """
        Salva o DataFrame em um arquivo Excel.
        """
        caminho_completo = os.path.join(self.caminho_saida, self.nome_arquivo)
        df.to_excel(caminho_completo, index=False)

        print("Arquivo criado com sucesso!")
        

    def executar(self):
        df = self.gerar_dataframe()
        df = self.inserir_duplicatas(df)
        self.salvar_excel(df)


if __name__ == "__main__":
    gerador = GerandoDados(qtd_linhas=5000)
    gerador.executar()
