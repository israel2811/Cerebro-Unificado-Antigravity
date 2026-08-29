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
    # ⚡ Bolt: Optimización de limpieza. BeautifulSoup es lento para archivos de 17MB+
    # Intentamos primero una limpieza por Regex para reducir el volumen antes de BS4 si es necesario.
    print("[*] Aplicando expresiones regulares para limpieza profunda...")
    text = re.sub(r'\{.*?\}', '', raw_text, flags=re.DOTALL) # Quitar brackets JSON grandes

    print("[*] Ejecutando destilación por BeautifulSoup...")
    # ⚡ Bolt: Usar 'lxml' si está disponible es más rápido, si no html.parser
    try:
        soup = BeautifulSoup(text, "lxml")
    except:
        soup = BeautifulSoup(text, "html.parser")

    text = soup.get_text(separator="\n")
    text = re.sub(r'\n+', '\n', text)
    return text

def semantic_chunking(clean_text):
    """Divide el texto en bloques seguros basados en el límite de palabras sin romper oraciones."""
    print("[*] Iniciando Chunking Semántico...")
    # ⚡ Bolt: Usar generador para ahorrar memoria en lugar de crear una lista gigante de palabras
    
    current_chunk = []
    current_word_count = 0
    
    # ⚡ Bolt: split() sin argumentos ya es eficiente, pero iteramos para no duplicar memoria
    for word in clean_text.split():
        current_chunk.append(word)
        current_word_count += 1
        
        if current_word_count >= MAX_WORDS_PER_CHUNK:
            # Terminar en un punto final si es posible para no cortar ideas en seco
            if word.endswith('.') or word.endswith('\n'):
                yield " ".join(current_chunk)
                current_chunk = []
                current_word_count = 0
                
    if current_chunk:
         yield " ".join(current_chunk)

def upload_to_google_docs(chunks):
    """Inyector automatizado hacia la Nube de Google."""
    print(f"[*] Preparando inyección de volúmenes a Google Docs...")
    
    # Simulación de la conexión a API (Armadura lista para inyectar token oauth)
    # creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # docs_service = build('docs', 'v1', credentials=creds)
    # drive_service = build('drive', 'v3', credentials=creds)
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    for i, chunk in enumerate(chunks, 1):
        doc_title = f"CORPUS_TESIS_VOL_{i}"
        file_path = os.path.join(OUTPUT_DIR, f"{doc_title}.txt")
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(chunk)
            
        print(f"[+] {doc_title} generado localmente ({len(chunk.split())} palabras).")
        # Aquí iría el código de google doc insertText
        # document = docs_service.documents().create(body={'title': doc_title}).execute()
        # docs_service.documents().batchUpdate(documentId=document.get('documentId'), body={'requests': [{'insertText': {'location': {'index': 1}, 'text': chunk}}]}).execute()
        
        if not IS_CLOUD_VM:
            gc.collect() # Prevenir OOM en iteraciones grandes sólo en Windows Local

if __name__ == "__main__":
    print("[*] Iniciando PROTOCOLO 2: DOCTOR INJECTOR")
    if not os.path.exists(INPUT_FILE):
        print(f"[!] Archivo {INPUT_FILE} no encontrado. Ejecuta Protocolo 1 primero.")
        exit(1)
        
    print("[*] Cargando corpus...")
    # ⚡ Bolt: Para 2GB de RAM, 17MB es manejable, pero implementamos limpieza secuencial.
    with open(INPUT_FILE, "r", encoding="utf-8", errors="ignore") as f:
        raw_data = f.read()
        
    cleaned = clean_html_noise(raw_data)
    del raw_data
    if not IS_CLOUD_VM:
        gc.collect()
    
    # ⚡ Bolt: Usar el generador directamente para evitar duplicar el texto limpio en una lista
    upload_to_google_docs(semantic_chunking(cleaned))

    del cleaned
    if not IS_CLOUD_VM:
        gc.collect()
    
    print("[+] Protocolo 2 Finalizado. Data Lake preparado.")
