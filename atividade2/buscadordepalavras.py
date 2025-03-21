import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import threading
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict

def buscar_palavra_na_pagina(url_atual, url_inicial, palavra, profundidade_maxima, profundidade_atual, urls_visitados, resultados, lock):
    if profundidade_atual > profundidade_maxima or url_atual in urls_visitados:
        return
    
    with lock:
        urls_visitados.add(url_atual)
    
    try:
        print(f"Buscando em: {url_atual} (Profundidade: {profundidade_atual})")
        response = requests.get(url_atual, timeout=10)
        response.raise_for_status()  #

        soup = BeautifulSoup(response.text, 'html.parser')

        conteudo = soup.get_text().lower()
        palavra_encontrada = palavra.lower() in conteudo
        with lock:
            resultados[url_atual] = palavra_encontrada

        links = soup.find_all('a', href=True)
        for link in links:
            url_completa = urljoin(url_inicial, link['href'])

            if url_completa.startswith(url_inicial):
                buscar_palavra_na_pagina(url_completa, url_inicial, palavra, profundidade_maxima, profundidade_atual + 1, urls_visitados, resultados, lock)

    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar {url_atual}: {e}")

def buscar_palavra_no_site(url_inicial, palavra, profundidade_maxima=3):
    urls_visitados = set()
    resultados = defaultdict(bool)  
    lock = threading.Lock()  

    with ThreadPoolExecutor() as executor:
        executor.submit(buscar_palavra_na_pagina, url_inicial, url_inicial, palavra, profundidade_maxima, 1, urls_visitados, resultados, lock)

    return resultados

if __name__ == "__main__":
    url_inicial = input("Digite a URL inicial do site (ex.: https://www.exemplo.com): ")
    palavra = input("Digite a palavra a ser buscada: ")
    
    import time
    start_time = time.time()

    resultados = buscar_palavra_no_site(url_inicial, palavra)

    print("\nResultados da busca:")
    for url, encontrada in resultados.items():
        status = "Encontrada" if encontrada else "Não encontrada"
        print(f"{url}: Palavra '{palavra}' {status}")

    print(f"\nTempo de execução: {time.time() - start_time:.2f} segundos")
