import requests
import pandas as pd

print("Iniciando download das séries...")

series = []
pagina = 0

while True:

    print(f"Baixando página {pagina}...")

    url = f"https://api.tvmaze.com/shows?page={pagina}"
    dados = requests.get(url).json()

    if not dados:
        print("Nenhuma página nova encontrada. Finalizando download.")
        break

    for s in dados:

        series.append({
            "titulo": s["name"],
            "genero": ",".join(s["genres"]),
            "rating": s["rating"]["average"] if s["rating"]["average"] else 0,
            "ano": s["premiered"]
        })

    print(f"Página {pagina} concluída. Total parcial de séries: {len(series)}")

    pagina += 1


print("\nCriando DataFrame...")
df = pd.DataFrame(series)

print("Convertendo datas...")
df["ano"] = pd.to_datetime(df["ano"], errors="coerce")

print("Filtrando séries a partir do ano 2000...")
df = df[df["ano"].dt.year >= 2000]

print("Total de séries após filtro:", len(df))

print("Salvando dataset em CSV...")
df.to_csv("series_tvmaze.csv", index=False)

print("Arquivo salvo com sucesso!")
print("Nome do arquivo: series_tvmaze.csv")
