import pandas as pd

# ==============================
# CARREGAR CSV
# ==============================

df = pd.read_csv("series_tvmaze.csv")

print("Dataset carregado!")
print("Total de séries:", len(df))

# Padronizar colunas
df.columns = df.columns.str.strip().str.lower()

# Padronizar dados
df["titulo"] = df["titulo"].fillna("").str.strip().str.lower()
df["genero"] = df["genero"].fillna("")
df["rating"] = pd.to_numeric(df["rating"], errors="coerce")

# Converter data
df["ano"] = pd.to_datetime(df["ano"], errors="coerce")

# ==============================
# TOP SÉRIES DE 2025
# ==============================

print("\nRecomendador para usuários novos / Séries mais populares\n")

series_2025 = df[df["ano"].dt.year == 2025]
series_2025 = series_2025.sort_values(by="rating", ascending=False)

top_2025 = series_2025.head(10)

print("\nSéries mais populares de 2025:\n")

for _, linha in top_2025.iterrows():
    print(f"{linha['titulo']} | Nota: {linha['rating']} | Ano: {linha['ano'].year}")

# ==============================
# INPUT DO USUÁRIO
# ==============================

favoritas = input("\nDigite algumas séries que você gosta (separadas por vírgula): ")
favoritas = favoritas.split(",")

# ==============================
# CRIAR SIMILARIDADE
# ==============================

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Reduzir dataset (performance)
df = df.sort_values(by="rating", ascending=False).head(3000)
df = df.reset_index(drop=True)

vectorizer = CountVectorizer()
matriz = vectorizer.fit_transform(df["genero"])

similaridade = cosine_similarity(matriz)

# ==============================
# FUNÇÃO DE RECOMENDAÇÃO
# ==============================

def recomendar(titulo):

    titulo = titulo.strip().lower()

    filtro = df["titulo"].str.contains(titulo, na=False)

    if not filtro.any():
        print(f"\nSérie '{titulo}' não encontrada.")
        return None

    indice = df[filtro].index[0]

    scores = list(enumerate(similaridade[indice]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)

    recomendacoes = scores[1:6]

    return df.iloc[[i[0] for i in recomendacoes]][["titulo", "rating", "ano"]]

# ==============================
# MOSTRAR RECOMENDAÇÕES
# ==============================

for serie in favoritas:

    serie = serie.strip()

    rec = recomendar(serie)

    if rec is not None:

        print(f"\n🔎 Recomendações baseadas em: {serie}\n")

        for _, linha in rec.iterrows():
            ano = linha["ano"].year if pd.notnull(linha["ano"]) else "N/A"
            print(f"- {linha['titulo']} | Nota: {linha['rating']} | Ano: {ano}")

# ==============================
# EXTRA (MULTIPLAS FAVORITAS)
# ==============================

def recomendar_por_favoritas(lista):

    recomendacoes = []

    for serie in lista:

        rec = recomendar(serie.strip())

        if rec is not None:
            recomendacoes.extend(rec["titulo"].tolist())

    return list(set(recomendacoes))

#Janela Final

#IDEIA GERAL (só quis colocar mesmo)

#fazer um sistema/programa(ou sei lá qual o nome certo), aonde quando inicia o codigo ele vai primeiramente listar as 5 melhores series -> feito
#(precisa ver se tem como deixar as 5 melhores atualmente e não as 5 melhores com avaliação embora não sei se é possivel fazer isso) -> 
# Depois de aparecer as 5 melhores dai então aparece a seguinte pergunta "Digite algumas séries que você gosta (separadas por vírgula): " ->
#dai então pegar um certo numero de series parecidas com aquelas que ele digitou e colocar em ordem de avaliação ou algo do tipo

#IDEIAS LOUCAS QUE EU ESTOU PENSANDO 
#Ao invés da mensagem sair do terminar <- sotaque até na digitação kkkkk erre, faz alguma coisa para abrir uma pagina separa quase igual ao negocio do olho do peixe dai nessa janela ->
#aparece as 5 melhores series e depois faz as perguntas e traz as melhores series baseadas na escolha do usuario

#Comandos aleatorios que talvez vai precisar usar kkkkkk

#serie = input("Digite o nome da série: ") - Um exemplo de pergunta aonde a pessoa -
#vai precisar digitar o nome das series (precisa ver como vai fazer para colocar varios nomes)



#janela = tk.Tk()

#janela.title("Recomendador de Séries")
#janela.geometry("500x400")

#texto = tk.Label(janela, text="Sistema de Recomendação de Séries", font=("Arial", 16))
#texto.pack(pady=20)

#janela.mainloop()

#COISAS QUE ESTAVAM SENDO USADA E AGORA ESTÃO COMENTADAS


#series = []

#for s in dados:
    #series.append({
        #"titulo": s["name"],
        #"genero": ",".join(s["genres"]),
        #"rating": s["rating"]["average"] if s["rating"]["average"] else 0,
        #"ano":s["premiered"]
    #})

#df = pd.DataFrame(series)

#def recomendar_populares_recentes(df, n=10):

    #df["ano"] = pd.to_datetime(df["ano"], errors="coerce")

    #recentes = df[df["ano"].dt.year >= 2023]

    #populares = recentes.sort_values(
        #by="rating",
        #ascending=False
    #)

    #return populares.head(n)
#print("")
#print("Séries mais populares recentes")
#print("")

#print(recomendar_populares_recentes(df)[["titulo","rating","ano"]])

#print(recomendar_populares(df))

#print("Top séries de 2025:")
#print(top_2025[["titulo", "rating", "ano"]])