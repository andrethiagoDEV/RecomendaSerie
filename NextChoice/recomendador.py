import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter

# =========================
# 📥 CARREGAR DATASET
# =========================
df = pd.read_csv("https://raw.githubusercontent.com/andrethiagoDEV/RecomendaSerie/refs/heads/main/series_tvmaze2.csv")

# =========================
# 🧹 LIMPEZA DOS DADOS
# =========================
df.columns = df.columns.str.strip().str.lower()

df["titulo"] = df["titulo"].fillna("").str.strip()
df["genero"] = df["genero"].fillna("")
df["rating"] = pd.to_numeric(df["rating"], errors="coerce").fillna(0)
df["ano"] = pd.to_datetime(df["ano"], errors="coerce")

# 🔥 garante que coluna imagem existe
if "imagem" not in df.columns:
    df["imagem"] = ""

# =========================
# ⚡ OTIMIZAÇÃO (performance)
# =========================
df = df.sort_values(by="rating", ascending=False).head(3000).reset_index(drop=True)

# =========================
# 🧠 CRIA TEXTO PARA IA
# =========================
df["conteudo"] = df["genero"] + " " + df["titulo"]

# =========================
# 🤖 VETORIZAÇÃO (TF-IDF)
# =========================
vectorizer = TfidfVectorizer(stop_words="english")
matriz = vectorizer.fit_transform(df["conteudo"])

# =========================
# 🔗 MATRIZ DE SIMILARIDADE
# =========================
similaridade = cosine_similarity(matriz)

# =========================
# 🔍 BUSCA FLEXÍVEL
# =========================
def buscar_titulo(titulo):
    titulo = titulo.strip().lower()

    resultados = df[df["titulo"].str.lower().str.contains(titulo, na=False)]

    if len(resultados) == 0:
        return None

    return resultados.iloc[0]["titulo"]

# =========================
# 🎬 FUNÇÃO PRINCIPAL
# =========================
def recomendar_series(favoritas):

    favoritas = favoritas.split(",")
    favoritas_validas = [f.strip() for f in favoritas if f.strip() != ""]

    contador = Counter()
    resultados_finais = []

    # 🔄 PARA CADA SÉRIE
    for serie in favoritas_validas:

        titulo = buscar_titulo(serie)

        if titulo is None:
            continue

        indice = df[df["titulo"] == titulo].index[0]

        scores = list(enumerate(similaridade[indice]))

        # 🔥 ranking híbrido (similaridade + nota)
        scores = [
            (i, s * 0.7 + df.iloc[i]["rating"] * 0.3)
            for i, s in scores
        ]

        scores = sorted(scores, key=lambda x: x[1], reverse=True)

        recomendacoes = scores[1:11]

        for i in recomendacoes:
            contador.update([df.iloc[i[0]]["titulo"]])

    # =========================
    # 🏆 RESULTADO FINAL
    # =========================
    for serie, _ in contador.most_common(10):

        linha = df[df["titulo"] == serie].iloc[0]

        resultados_finais.append({
            "titulo": linha["titulo"],
            "rating": float(linha["rating"]),
            "imagem": linha["imagem"] if pd.notnull(linha["imagem"]) else "",
            "ano": int(linha["ano"].year) if pd.notnull(linha["ano"]) else "N/A"
        })

    # 🔥 evita retorno vazio
    if not resultados_finais:
        return [{
            "titulo": "Nenhuma recomendação encontrada",
            "rating": 0,
            "imagem": "",
            "ano": ""
        }]

    return resultados_finais