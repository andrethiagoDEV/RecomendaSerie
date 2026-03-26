from flask import Flask, request, jsonify, render_template
from recomendador import recomendar_series

app = Flask(__name__)

# Página principal
@app.route("/")
def home():
    return render_template("index.html")

# API de recomendação
@app.route("/recomendar", methods=["POST"])
def recomendar():
    data = request.get_json()
    favoritas = data.get("favoritas")

    resultado = recomendar_series(favoritas)

    return jsonify(resultado)

@app.route("/top2025")
def top_2025():

    import pandas as pd

    df = pd.read_csv("https://raw.githubusercontent.com/andrethiagoDEV/RecomendaSerie/refs/heads/main/series_tvmaze2.csv")

    df["ano"] = pd.to_datetime(df["ano"], errors="coerce")

    # 🔥 filtra séries mais recentes
    df_2025 = df[df["ano"].dt.year == 2025]

    # 🔥 ordena por rating
    df_2025 = df_2025.sort_values(by="rating", ascending=False).head(15)

    resultado = []

    for _, linha in df_2025.iterrows():
        resultado.append({
            "titulo": linha["titulo"],
            "rating": float(linha["rating"]),
            "imagem": linha["imagem"] if pd.notnull(linha["imagem"]) else "",
            "ano": int(linha["ano"].year) if pd.notnull(linha["ano"]) else ""
        })

    print("TOP 2025:", resultado)  # 👈 DEBUG

    return jsonify(resultado)

@app.route("/horror")
def horror():

    import pandas as pd

    df = pd.read_csv("https://raw.githubusercontent.com/andrethiagoDEV/RecomendaSerie/refs/heads/main/series_tvmaze2.csv")

    # 👇 aqui depende do nome da coluna (provavelmente "genero" ou "genres")
    # ajuste se necessário
    df_terror = df[df["genero"].str.contains("Horror", case=False, na=False)]

    # ordena pelos melhores
    df_terror = df_terror.sort_values(by="rating", ascending=False).head(15)

    resultado = []

    for _, linha in df_terror.iterrows():
        resultado.append({
            "titulo": linha["titulo"],
            "rating": float(linha["rating"]),
            "imagem": linha["imagem"] if pd.notnull(linha["imagem"]) else ""
        })

    print("HORROR:", resultado)

    return jsonify(resultado)

@app.route("/action")
def action():
    import pandas as pd

    df = pd.read_csv("https://raw.githubusercontent.com/andrethiagoDEV/RecomendaSerie/refs/heads/main/series_tvmaze2.csv")

    df_acao = df[df["genero"].str.contains("Action", case=False, na=False)]

    df_acao = df_acao.sort_values(by="rating", ascending=False).head(15)

    resultado = []

    for _, linha in df_acao.iterrows():
        resultado.append({
            "titulo": linha["titulo"],
            "rating": float(linha["rating"]),
            "imagem": linha["imagem"] if pd.notnull(linha["imagem"]) else ""
        })

    print("ACTION:", resultado)  

    return jsonify(resultado)
# Rodar servidor
app.run(debug=True)