from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json

load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = f"{client_id}:{client_secret}"
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = base64.b64encode(auth_bytes).decode('utf-8')

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "client_credentials"
    }
    response = post(url, headers=headers, data=data)
    json_response = json.loads(response.content)
    token = json_response.get("access_token")  
    if not token:
        raise Exception("Failed to retrieve access token")
    print("Access token retrieved successfully.")
    return token

def get_auth_header(token):
    """Returns the authorization header for API requests."""
    return {"Authorization": f"Bearer {token}"} 



def search_artist(token, artist_name):
    #Buscar por um artista e retorna o ID do artista
    
    # Endpoint da API do Spotify para fazer buscas
    url = "https://api.spotify.com/v1/search"

    # Cabeçalho de autenticação com o token recebido
    headers = get_auth_header(token)

    # Parâmetros da requisição: nome do artista, tipo (artista), e limite de 1 resultado
    params = {
        "q": artist_name,      # Termo de busca (nome do artista)
        "type": "artist",      # Tipo de busca (nesse caso, artista)
        "limit": 1             # Traz só o primeiro resultado encontrado
    }

    # Faz a requisição GET à API do Spotify
    response = get(url, headers=headers, params=params)

    # Converte a resposta da API de JSON para dicionário Python
    json_response = json.loads(response.content)
    print(json_response)

    # Verifica se a resposta contém artistas e se há ao menos um item
    if 'artists' in json_response and json_response['artists']['items']:
        # Pega o ID do primeiro artista da lista
        artist_id = json_response['artists']['items'][0]['id']
        print(f"Artist ID for '{artist_name}': {artist_id}")
        return artist_id
    else:
        # Se não encontrou nenhum artista, levanta um erro
        raise Exception(f"Artist '{artist_name}' not found.")


token = get_token()

search_artist(token, "Taylor Swift")
