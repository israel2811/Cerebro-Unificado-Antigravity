import os
import json
import gc
import re
import platform
from bs4 import BeautifulSoup

# Detección de VM en Nube (Codespaces/Gitpod)
IS_CLOUD_VM = platform.system().lower() == "linux"

# NOTA: En un entorno real, descomentar y usar google-api-python-client
# from google.oauth2.credentials import Credentials
# from googleapiclient.discovery import build

INPUT_FILE = "/workspaces/Antigravity_Cloud_Project/scripts_leviathan/raw_corpus_extraction.txt" if IS_CLOUD_VM else r"C:\Users\Lenovo\Antigravity_Cloud_Project\scripts_leviathan\raw_corpus_extraction.txt"
OUTPUT_DIR = "/workspaces/Antigravity_Cloud_Project/scripts_leviathan/clean_chunks" if IS_CLOUD_VM else r"C:\Users\Lenovo\Antigravity_Cloud_Project\scripts_leviathan\clean_chunks"
MAX_WORDS_PER_CHUNK = 100000 if IS_CLOUD_VM else 30000

def clean_html_noise(raw_text):
    """Filtra y purifica el texto, quitando HTML, JSON y ruido sintáctico."""
    soup = BeautifulSoup(raw_text, "html.parser")
    text = soup.get_text(separator="\n")
    
    # Limpieza básica de caracteres nulos, múltiples saltos de línea y ruido de JSON/código.
    text = re.sub(r'\{.*?\}', '', text, flags=re.DOTALL) # Quitar brackets JSON grandes
    text = re.sub(r'\n+', '\n', text)
    return text

def stream_corpus(filepath):
    """Generador que lee el corpus y devuelve documentos individuales basados en el delimitador de ORIGEN."""
    current_doc = []
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if line.startswith("--- ORIGEN:"):
                if current_doc:
                    yield "".join(current_doc)
                    current_doc = []
                current_doc.append(line)
                continue
            current_doc.append(line)
        if current_doc:
            yield "".join(current_doc)

def upload_to_google_docs(word_list, index):
    """Inyector automatizado hacia la Nube de Google. (Optimizado para streaming)"""
    doc_title = f"CORPUS_TESIS_VOL_{index}"
    file_path = os.path.join(OUTPUT_DIR, f"{doc_title}.txt")
    
    # 1. Persistencia Local
    chunk_text = " ".join(word_list)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(chunk_text)

    print(f"[+] {doc_title} generado localmente ({len(word_list)} palabras).")

    # 2. Inyección Cloud (Placeholder para futuras implementaciones)
    # Simulación de la conexión a API (Armadura lista para inyectar token oauth)
    # creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # docs_service = build('docs', 'v1', credentials=creds)
    # drive_service = build('drive', 'v3', credentials=creds)
    
    # Aquí iría el código de google doc insertText
    # document = docs_service.documents().create(body={'title': doc_title}).execute()
    # docs_service.documents().batchUpdate(documentId=document.get('documentId'), body={'requests': [{'insertText': {'location': {'index': 1}, 'text': chunk_text}}]}).execute()

def process_and_inject_streaming(input_file):
    """Versión optimizada que procesa el corpus en streaming para minimizar el uso de RAM."""
    print("[*] Iniciando Inyección por Streaming (Optimización Bolt ⚡)")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    current_chunk_words = []
    current_word_count = 0
    volume_count = 1

    for raw_doc in stream_corpus(input_file):
        cleaned_doc = clean_html_noise(raw_doc)
        # bolt: preserve punctuation for boundary check but split by space
        words = cleaned_doc.split()
        
        for word in words:
            current_chunk_words.append(word)
            current_word_count += 1
            
            if current_word_count >= MAX_WORDS_PER_CHUNK:
                # Terminar en un punto final para no cortar ideas en seco
                # Nota: words de .split() no tienen \n, pero sí conservan el punto final.
                if word.endswith('.'):
                    upload_to_google_docs(current_chunk_words, volume_count)
                    volume_count += 1
                    current_chunk_words = []
                    current_word_count = 0

        if not IS_CLOUD_VM:
            gc.collect()

    # Flush final
    if current_chunk_words:
        upload_to_google_docs(current_chunk_words, volume_count)

if __name__ == "__main__":
    print("[*] Iniciando PROTOCOLO 2: DOCTOR INJECTOR (STREAMING EDITION)")
    if not os.path.exists(INPUT_FILE):
        print(f"[!] Archivo {INPUT_FILE} no encontrado. Ejecuta Protocolo 1 primero.")
        exit(1)
        
    process_and_inject_streaming(INPUT_FILE)
    print("[+] Protocolo 2 Finalizado. Data Lake preparado con mínima huella de RAM.")
