import pandas as pd
def executar_analise():
    print("=== Iniciando Processamento Automatizado de Dados ===\n")
    try:
        df = pd.read_csv("dados_vendas.csv")
        print("[SUCESSO] Arquivo "dados_vendas.csv" carregado corretamente.")
    except FileNotFoundError:
        print("[ERRO] Arquivo de dados nao encontrado.")
        return

        df["Faturamento_Total"] = df["Quantidade"] * df["Preco_Unitario"]

        faturamento_total = df["Faturamento_Total"].sum()
        produtos_mais_vendidos = df.groupby("Produto")["Quantidade"].sum().sort_values(ascending=False)
        faturamento_por_regiao = df.groupby("regiao")["faturamento_total"].sum()

        print("\n" + "="*40)
        print("       RELATORIO DE PERFORMANCE DIGITAL")
        print("="*40)
        print(f"Faturamento Bruto Total: R$ {faturamento_total:,.2f")

        print("\nVolume de Vendas por Produto:")
        for prod, qtd in produtos_mais_vendidos.items():
            print(f" - {prod}: {qtd} unidades")

        print("\nFaturamento por Regiao Geografica:")
        for reg, fat in faturamento_por_regiao.items():
            print(f" - Regiao {reg}: R$ {fat:,.2f}")
        print("="*40)
        print("\n[SUCESSO] Processamento concluído com êxito.")

    if __name__ == "__main__":
        executar_analise()
