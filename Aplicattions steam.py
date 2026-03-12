import requests
from bs4 import BeautifulSoup
import os

def extract_exe(url):
    """Extrai o arquivo .exe do produto da Steam"""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Encontra o link do .exe na página
    exe_link = None
    for link in soup.find_all('a'):
        if '.exe' in link.get('href', ''):
            exe_link = link['href']
            break
    
    if not exe_link:
        raise ValueError("Nenhum link .exe encontrado.")
    
    return exe_link

def upload_to_mediafire(file_path):
    """Envia o arquivo para o MediaFire e retorna o link de download"""
    # Exemplo usando MediaFire API
    mediafire_api_url = "https://www.mediafire.com/api/upload.php"
    
    files = {'file': open(file_path, 'rb')}
    data = {
        'upload_type': 'file',
        'session_id': 'your_session_id',
        'api_key': 'your_api_key'
    }
    
    response = requests.post(mediafire_api_url, files=files, data=data)
    return response.json().get('link')

def main():
    steam_url = input("Digite o URL da Steam do produto: ")
    try:
        exe_url = extract_exe(steam_url)
        print(f"Arquivo .exe encontrado em: {exe_url}")
        
        # Baixa o arquivo localmente
        file_name = exe_url.split('/')[-1]
        response = requests.get(exe_url)
        with open(file_name, 'wb') as f:
            f.write(response.content)
        
        # Envia para o MediaFire
        mediafire_link = upload_to_mediafire(file_name)
        print(f"Link para download: {mediafire_link}")
    except Exception as e:
        print(f"Erro: {str(e)}")

if __name__ == "__main__":
    main()
    