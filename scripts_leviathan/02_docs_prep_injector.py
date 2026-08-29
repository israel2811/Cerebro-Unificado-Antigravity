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
    print("[*] Ejecutando destilación por BeautifulSoup...")
    soup = BeautifulSoup(raw_text, "html.parser")
    text = soup.get_text(separator="\n")
    
    # Limpieza básica de caracteres nulos, múltiples saltos de línea y ruido de JSON/código.
    print("[*] Aplicando expresiones regulares para limpieza profunda...")
    text = re.sub(r'\{.*?\}', '', text, flags=re.DOTALL) # Quitar brackets JSON grandes
    text = re.sub(r'\n+', '\n', text)
    return text

def semantic_chunking(clean_text):
    """Divide el texto en bloques seguros basados en el límite de palabras sin romper oraciones."""
    print("[*] Iniciando Chunking Semántico...")
    words = clean_text.split()
    chunks = []
    
    current_chunk = []
    current_word_count = 0
    
    for word in words:
        current_chunk.append(word)
        current_word_count += 1
        
        if current_word_count >= MAX_WORDS_PER_CHUNK:
            # Terminar en un punto final si es posible para no cortar ideas en seco
            if word.endswith('.') or word.endswith('\n'):
                chunks.append(" ".join(current_chunk))
                current_chunk = []
                current_word_count = 0
                
    if current_chunk:
         chunks.append(" ".join(current_chunk))
         
    return chunks

def stream_corpus_documents(filepath):
    """Generador que lee el corpus línea a línea y entrega documentos por separado."""
    current_doc = []
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if line.startswith("--- ORIGEN:"):
                if current_doc:
                    yield "".join(current_doc)
                    current_doc = []
            current_doc.append(line)
        if current_doc:
            yield "".join(current_doc)

def upload_to_google_docs(chunks, global_counter):
    """Inyector automatizado hacia la Nube de Google."""
    print(f"[*] Preparando inyección de {len(chunks)} volúmenes a Google Docs...")
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    for chunk in chunks:
        global_counter += 1
        doc_title = f"CORPUS_TESIS_VOL_{global_counter}"
        file_path = os.path.join(OUTPUT_DIR, f"{doc_title}.txt")
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(chunk)
            
        print(f"[+] {doc_title} generado localmente ({len(chunk.split())} palabras).")
        
        if not IS_CLOUD_VM:
            gc.collect()

    return global_counter

if __name__ == "__main__":
    print("[*] Iniciando PROTOCOLO 2: DOCTOR INJECTOR (STREAMING MODE)")
    if not os.path.exists(INPUT_FILE):
        print(f"[!] Archivo {INPUT_FILE} no encontrado. Ejecuta Protocolo 1 primero.")
        exit(1)
        
    print("[*] Procesando corpus en streaming para optimizar RAM...")

    global_chunk_count = 0
    
    for doc_content in stream_corpus_documents(INPUT_FILE):
        # Procesar cada documento de forma independiente para mantener baja la RAM
        cleaned = clean_html_noise(doc_content)
        del doc_content

        volumenes = semantic_chunking(cleaned)
        del cleaned

        global_chunk_count = upload_to_google_docs(volumenes, global_chunk_count)
        del volumenes

        if not IS_CLOUD_VM:
            gc.collect()
    
    print("[+] Protocolo 2 Finalizado. Data Lake preparado.")
