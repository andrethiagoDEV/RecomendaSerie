import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter

# Carrega o dataset de séries de TV do GitHub

df = pd.read_csv("https://raw.githubusercontent.com/andrethiagoDEV/RecomendaSerie/main/series_tvmaze.csv")

print("Dataset carregado")
print("Total de séries:", len(df))

# Limpeza dos dados

df.columns = df.columns.str.strip().str.lower()

df["titulo"] = df["titulo"].fillna("").str.strip()
df["genero"] = df["genero"].fillna("")
df["rating"] = pd.to_numeric(df["rating"], errors="coerce").fillna(0)

df["ano"] = pd.to_datetime(df["ano"], errors="coerce")

# Faz as 10 melhores séries de 2025

print("\n Recomendador para usuários novos / Séries mais populares\n")

series_2025 = df[df["ano"].dt.year == 2025]
series_2025 = series_2025.sort_values(by="rating", ascending=False)

top_2025 = series_2025.head(10)

print(" Séries mais populares de 2025:\n")

for _, linha in top_2025.iterrows():
    print(f"{linha['titulo']} | Nota: {linha['rating']} | Ano: {linha['ano'].year}")

# Digite as séries favoritas do usuário

print("")
favoritas = input("Digite algumas séries que você gosta (separadas por vírgula): ")
favoritas = favoritas.split(",")


# dodos modo (TF-IDF)

df = df.sort_values(by="rating", ascending=False).head(3000)
df = df.reset_index(drop=True)

df["conteudo"] = df["genero"] + " " + df["titulo"]

vectorizer = TfidfVectorizer(stop_words="english")
matriz = vectorizer.fit_transform(df["conteudo"])

similaridade = cosine_similarity(matriz)

# faz uma busca mais flexível, ignorando maiúsculas, espaços e acentos

def buscar_titulo(titulo):
    titulo = titulo.strip().lower()

    resultados = df[df["titulo"].str.lower().str.contains(titulo, na=False)]

    if len(resultados) == 0:
        return None

    return resultados.iloc[0]["titulo"]

# Faz a recomendação indibidual

def recomendar(titulo):

    titulo_original = titulo
    titulo = buscar_titulo(titulo)

    if titulo is None:
        print(f"\n Série '{titulo_original}' não encontrada.")
        return None

    indice = df[df["titulo"] == titulo].index[0]

    scores = list(enumerate(similaridade[indice]))

    # ranking híbrido (similaridade + nota)
    scores = [
        (i, s * 0.7 + df.iloc[i]["rating"] * 0.3)
        for i, s in scores
    ]

    scores = sorted(scores, key=lambda x: x[1], reverse=True)

    recomendacoes = scores[1:6]

    resultado = df.iloc[[i[0] for i in recomendacoes]][["titulo", "rating", "ano"]]

    return resultado

# Recomendações por série favorita do usuário

favoritas_validas = [f.strip() for f in favoritas if f.strip() != ""]

contador = Counter()

for serie in favoritas_validas:

    rec = recomendar(serie)

    if rec is not None:

        print(f"\n Recomendações baseadas em '{serie}':\n")

        for _, linha in rec.iterrows():
            print(f"- {linha['titulo']} | Nota: {linha['rating']} | Ano: {linha['ano'].year}")
            contador.update([linha["titulo"]])

# Resultado Final

if len(favoritas_validas) > 1:

    print("\n Recomendações finais (mais relevantes):\n")

    for serie, freq in contador.most_common(5):
        print(f"- {serie}")
