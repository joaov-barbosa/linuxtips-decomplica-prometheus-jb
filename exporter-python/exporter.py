import random
import time
import requests
from prometheus_client import Gauge, start_http_server
url_numero_pessoas = 'http://api.open-notify.org/astros.json'  # URL para pegar o número de astronautas
url_local_ISS = 'http://api.open-notify.org/iss-now.json'  # URL para pegar a localização do ISS

# Função para pegar o número de astronautas
def pega_numero_astronautas():
    try:
        response = requests.get(url_numero_pessoas)  # Faz a requisição HTTP
        data = response.json()  # Converte o resultado em JSON
        return data['number']  # Retorna o número de astronautas
    except Exception as e:
        #print("Não foi possível acessar a url!")
        return random.randint(1, 100)  # Retorna um número aleatório entre 1 e 100

# Função para pegar a latitude (com valor aleatório em caso de erro)
def pega_latitude():
    try:
        response = requests.get(url_local_ISS)  # Faz a requisição HTTP
        data = response.json()  # Converte o resultado em JSON
        return data['latitude']  # Retorna a latitude
    except Exception as e:
        
        #print("Não foi possível acessar a url da latitude!")
        return random.uniform(-90, 90)  # Retorna um valor aleatório de latitude entre -90 e 90

# Função para pegar a longitude (com valor aleatório em caso de erro)
def pega_longitude():
    try:
        response = requests.get(url_local_ISS)  # Faz a requisição HTTP
        data = response.json()  # Converte o resultado em JSON
        return data['longitude']  # Retorna a longitude
    except Exception as e:
        #print("Não foi possível acessar a url da longitude!")
        return random.uniform(-180, 180)  # Retorna um valor aleatório de longitude entre -180 e 180

# Função para atualizar as métricas
def atualiza_metricas():
    try:
        """
        Atualiza as métricas com o número de astronautas e local da estação espacial internacional
        """
        numero_pessoas = Gauge('numero_de_astronautas', 'Número de astronautas no espaço')  # Cria a métrica
        latitude = Gauge('latitude_estacao', 'Latitude da estação espacial internacional')  # Cria a métrica para latitude
        longitude = Gauge('longitude_estacao', 'Longitude da estação espacial internacional')  # Cria a métrica para longitude

        while True:
            # Atualiza as métricas com os valores
            numero_atual = pega_numero_astronautas()
            latitude_atual = pega_latitude()
            longitude_atual = pega_longitude()

            numero_pessoas.set(numero_atual)  # Atualiza a métrica do número de astronautas
            latitude.set(latitude_atual)  # Atualiza a métrica de latitude
            longitude.set(longitude_atual)  # Atualiza a métrica de longitude

            time.sleep(10)  # Faz o sleep de 10 segundos
            print("Número de astronautas: %s, Latitude: %s, Longitude: %s" % (numero_atual, latitude_atual, longitude_atual))  # Imprime os valores
    except Exception as e:
        print("A quantidade de astronautas e/ou as coordenadas não podem ser atualizadas!")
        raise e  # Lança a exceção

def inicia_exporter(): # Função para iniciar o exporter
    try:
        """
        Iniciar o exporter
        """
        start_http_server(8899) # Inicia o servidor do Prometheus na porta 8899
        return True # Retorna True
    except Exception as e: # Se der algum erro
        print("O Servidor não pode ser iniciado!") # Imprime que não foi possível iniciar o servidor
        raise e # Lança a exceção

def main(): # Função principal
    try:
        inicia_exporter() # Inicia o exporter
        print('Exporter Iniciado') # Imprime que o exporter foi iniciado
        atualiza_metricas() # Atualiza as métricas
    except Exception as e: # Se der algum erro
        print('\nExporter Falhou e Foi Finalizado! \n\n======> %s\n' % e) # Imprime que o exporter falhou e foi finalizado
        exit(1) # Finaliza o programa com erro


if __name__ == '__main__': # Se o programa for executado diretamente
    main() # Executa o main
    exit(0) # Finaliza o programa
    