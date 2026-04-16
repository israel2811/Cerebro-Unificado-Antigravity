import os
import json
import gc
import re
import platform
from bs4 import BeautifulSoup

# Detección de VM en Nube (Codespaces/Gitpod)
IS_CLOUD_VM = platform.system().lower() == "linux"

INPUT_FILE = "/workspaces/Antigravity_Cloud_Project/scripts_leviathan/raw_corpus_extraction.txt" if IS_CLOUD_VM else r"C:\Users\Lenovo\Antigravity_Cloud_Project\scripts_leviathan\raw_corpus_extraction.txt"
OUTPUT_DIR = "/workspaces/Antigravity_Cloud_Project/scripts_leviathan/clean_chunks" if IS_CLOUD_VM else r"C:\Users\Lenovo\Antigravity_Cloud_Project\scripts_leviathan\clean_chunks"
MAX_WORDS_PER_CHUNK = 100000 if IS_CLOUD_VM else 30000

def clean_html_noise(raw_text):
    """Filtra y purifica el texto, quitando HTML, JSON y ruido sintáctico."""
    # Optimization: Process text in smaller segments via BeautifulSoup to keep RAM usage low
    soup = BeautifulSoup(raw_text, "html.parser")
    text = soup.get_text(separator="\n")
    
    # Limpieza básica de caracteres nulos, múltiples saltos de línea y ruido de JSON/código.
    text = re.sub(r'\{.*?\}', '', text, flags=re.DOTALL) # Quitar brackets JSON grandes
    text = re.sub(r'\n+', '\n', text)
    return text

def stream_documents(filepath):
    """Lee el archivo y cede fragmentos delimitados por ORIGEN."""
    # Performance Win: Streaming generator prevents loading 17MB+ files entirely into RAM
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        current_doc = []
        for line in f:
            if line.startswith("--- ORIGEN: ") and " ---" in line:
                if current_doc:
                    yield "".join(current_doc)
                    current_doc = []
            current_doc.append(line)
        if current_doc:
            yield "".join(current_doc)

def save_chunk(chunk_words, index):
    """Guarda un chunk de texto en el disco."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    doc_title = f"CORPUS_TESIS_VOL_{index}"
    file_path = os.path.join(OUTPUT_DIR, f"{doc_title}.txt")
    
    chunk_text = " ".join(chunk_words)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(chunk_text)

    print(f"[+] {doc_title} generado localmente ({len(chunk_words)} palabras).")

if __name__ == "__main__":
    print("[*] Iniciando PROTOCOLO 2: DOCTOR INJECTOR (Optimizado)")
    if not os.path.exists(INPUT_FILE):
        print(f"[!] Archivo {INPUT_FILE} no encontrado. Ejecuta Protocolo 1 primero.")
        exit(1)
        
    print("[*] Procesamiento en streaming activado para ahorro de RAM...")
    
    current_chunk_words = []
    chunk_index = 1
    
    # Process documents one-by-one to minimize peak RAM (OOM protection for 2GB systems)
    for doc_content in stream_documents(INPUT_FILE):
        cleaned = clean_html_noise(doc_content)
        words = cleaned.split()

        for word in words:
            current_chunk_words.append(word)
            if len(current_chunk_words) >= MAX_WORDS_PER_CHUNK:
                # Terminar en un punto final si es posible para no cortar ideas en seco
                if word.endswith('.') or word.endswith('\n'):
                    save_chunk(current_chunk_words, chunk_index)
                    chunk_index += 1
                    current_chunk_words = []

        if not IS_CLOUD_VM:
            gc.collect()

    # Guardar el residuo final
    if current_chunk_words:
        save_chunk(current_chunk_words, chunk_index)

    print("[+] Protocolo 2 Finalizado. Data Lake preparado.")
