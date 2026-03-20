import csv
import json
import random
import os
import time

import requests
from bs4 import BeautifulSoup

genero_map = {
    "ACTION": "ACAO",
    "ADVENTURE": "AVENTURA",
    "FANTASY": "FICCAO",
    "FICTION": "FICCAO",
    "ANIMATION": "INFANTIL",
    "FAMILY": "INFANTIL",
    "MYSTERY": "SUSPENSE",
    "THRILLER": "SUSPENSE",
    "SUSPENSE": "SUSPENSE",
    "COMEDY": "COMEDIA",
    "DRAMA": "DRAMA",
    "DOCUMENTARY": "DOCUMENTARIO",
    "HISTORY": "DOCUMENTARIO",
    "ROMANCE": "ROMANCE",
    "TERROR": "TERROR",
    "MUSICAL": "MUSICAL"
}

def download_cover(filme: str, ano: str):
    nome_arquivo = f"covers/{filme.replace(':', '_').replace('\'', '')}-{ano}.jpg"
    url_pesquisa = f"https://www.cinematerial.com/search?q={filme.replace(' ', '+')}"

    if os.path.isfile(nome_arquivo):
        return
    
    print(f"Baixando capa do filme: {filme} ({ano})...")

    res = requests.get(
        url_pesquisa,
        timeout=200
    )
    res.raise_for_status()

    html_reader = BeautifulSoup(res.text, "html.parser")
    img_cover = html_reader.find(class_="object-cover")

    if img_cover:
        url_cover = img_cover.get("src")
        if url_cover:
            url_cover = str(url_cover).replace("/60x/", "/297x/").replace("-xs.jpg", "-md.jpg")
            res = requests.get(
                url_cover,
                timeout=200
            )
            res.raise_for_status()

            if not os.path.isdir("covers"):
                os.mkdir("covers")
            
            with open(nome_arquivo, "wb") as f:
                f.write(res.content)
            
            time.sleep(2)
    else:
        raise Exception("Capa não encontrada!")

def extrair_filmes_e_capas ():
    filmes = []
    with open("movies.csv", "r", encoding="utf-8") as f:
        dados = csv.DictReader(f)

        for row in dados:
            generos = row["genres"].upper().split(" ")
            genero = "{" + list(filter(lambda x:x in genero_map, generos))[0] + "}"
            genero = genero.format_map(genero_map)

            filme = {
                "dt_lancamento": row["release_date"],
                "nome": row["title"],
                "descricao": row["overview"],
                "idade_min": random.randint(0, 18),
                "genero": genero,
            }

            try:
                download_cover(filme["nome"], str(filme["dt_lancamento"]).split("-")[0])
            except:
                print(f"Ocorreu um erro ao obter a capa do filme {filme['nome']}!")

            filmes.append(filme)

            if len(filmes) == 400:
                break

    with open("movies.json", "w", encoding="utf-8") as f:
        json.dump(filmes, f, indent=4)

if __name__ == "__main__":
    extrair_filmes_e_capas()