import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

class DataAnalyticsPipeline:
    def __init__(self, input_path):
        self.input_path = input_path
        self.df = None
    def carregar_e_limpar_dados(self):
        print("[INFO] Iniciando pipeline de extração e tratamento...")

        if not os.path.exists(self.input_path):
            raise FileNotFoundError(f"Base de dados {self.input_path} não encontrada.")

        self.df = pd.read_csv(self.input_path)

        duplicados = self.df.duplicated().sum()
        self.df.drop_duplicates(inplace=True)
        print(f"[Tratamento] {duplicados} linhas duplicadas removidas.")

        self.df["Preco_Unitario"] = self.df["Preco_Unitario"].fillna(2500.0)
        print("[Tratamento] Valores ausentes em "Preco_Unitario" preenchidos com sucesso.")

        self.df["Data"] = pd.to_datetime(self.df["Data"])
        self.df["Faturamento_Bruto"] = self.df["Quantidade"] * self.df["Preco_Unitario"]

        self.df_validos = self.df[self.df["Status"] == "Concluido"].copy()
        print("[INFO] Fase de tratamento concluída com êxito.")

    def calcular_metricas_negocio(self):
        print("\n" + "="*50)
        print("         KPIs EXECUTIVOS DE PERFORMANCE")
        print("="*50)

        faturamento_total = self.df_validos["Faturamento_Bruto"].sum()
        ticket_medio = self.df_validos["Faturamento_Bruto"].mean()
        total_pedidos = self.df_validos["ID_Pedido"].nunique()
        taxa_conversao = (len(self.df_validos) / len(self.df)) * 100

        print(f"  Faturamento Líquido Total : R$ {faturamento_total:,.2f}")
        print(f"  Ticket Médio por Contrato : R$ {ticket_medio:,.2f}")
        print(f"  Total de Contratos Fechados : {total_pedidos}")
        print(f"  Taxa de Conversão de Leads : {taxa_conversao:.2f}%")
        print("="*50)

   def gerar_insights_visuais(self):
       print("\n[Visual Renderizando gráficos de performance corporativa...")

       fat_produto = self.df_validos.groupby("Produto")["Faturamento_Bruto"].sum().reset_index()
       fig_prod = px.bar(
           fat_produto,
           x="Produto",
           y="Faturamento_Bruto",
           title="Faturamento Total por Solução Digital",
           labels={"Faturamento_Bruto": "Faturamento (R$)"},
           text_auto=" .2s",
           template="plotly_dark"
       )

       fat_regiao = self.df_validos.groupby("Regiao")["Faturamento_Bruto"].sum().reset_index()
       fig_reg = px.pie(
           fat_regiao,
           values="Faturamento_Bruto",
           names="Regiao",
           title="Market Share de Faturamento por Regiao",
           hole=0.4"
           template="plotly_dark"
       )

       os.makedirs("output", exist_ok=True)

       fig_prod.write_html("output/faturamento_produtos.html")
       fig_reg.write_html("output/share_regioes.html")

       print("[SUCESSO] Dashboards dinâmicos exportados na pasta "output/".")

       if __name__ == "__main__":
           pipeline = DataAnalyticsPipeline(input_path="dados_comerciais.csv")
           try:
               pipeline.carregar_e_limpar_dados()
               pipeline.calcular_metricas_negocio()
               pipeline.gerar_insights_visuais()
           except Exception as e:
               print(f"[ERRO NO PIPELINE]: {e}")
  
