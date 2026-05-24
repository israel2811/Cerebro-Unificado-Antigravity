import os
import json
import gc
import re
import platform
from bs4 import BeautifulSoup

# Detección de VM en Nube (Codespaces/Gitpod)
IS_CLOUD_VM = platform.system().lower() == "linux"

# Rutas adaptadas al entorno actual
BASE_DIR = os.getcwd()
INPUT_FILE = os.path.join(BASE_DIR, "scripts_leviathan/raw_corpus_extraction.txt")
OUTPUT_DIR = os.path.join(BASE_DIR, "scripts_leviathan/clean_chunks")
MAX_WORDS_PER_CHUNK = 100000 if IS_CLOUD_VM else 30000

def clean_html_noise(raw_text):
    """Filtra y purifica el texto, quitando HTML, JSON y ruido sintáctico."""
    # BOLT OPTIMIZATION: Processed in smaller chunks via streaming to avoid massive string allocations
    soup = BeautifulSoup(raw_text, "html.parser")
    text = soup.get_text(separator="\n")
    
    # Limpieza básica de caracteres nulos, múltiples saltos de línea y ruido de JSON/código.
    text = re.sub(r'\{.*?\}', '', text, flags=re.DOTALL) # Quitar brackets JSON grandes
    text = re.sub(r'\n+', '\n', text)
    return text

def stream_corpus(input_file):
    """Generator that yields documents separated by ORIGEN markers."""
    with open(input_file, "r", encoding="utf-8", errors="ignore") as f:
        current_doc = []
        for line in f:
            if line.startswith("--- ORIGEN: ") and current_doc:
                yield "".join(current_doc)
                current_doc = [line]
            else:
                current_doc.append(line)
        if current_doc:
            yield "".join(current_doc)

def stream_semantic_chunking(input_file):
    """Divide el texto en bloques seguros basados en el límite de palabras sin romper oraciones, usando streaming."""
    print("[*] Iniciando Chunking Semántico por Streaming...")
    
    current_chunk_words = []
    current_word_count = 0
    
    for raw_doc in stream_corpus(input_file):
        cleaned_text = clean_html_noise(raw_doc)
        words = cleaned_text.split()
        
        for word in words:
            current_chunk_words.append(word)
            current_word_count += 1

            if current_word_count >= MAX_WORDS_PER_CHUNK:
                # Terminar en un punto final si es posible para no cortar ideas en seco
                if word.endswith('.') or word.endswith('\n'):
                    yield " ".join(current_chunk_words)
                    current_chunk_words = []
                    current_word_count = 0

    if current_chunk_words:
         yield " ".join(current_chunk_words)

def process_and_upload(input_file):
    """Inyector automatizado hacia la Nube de Google con procesamiento en streaming."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print(f"[*] Procesando corpus en streaming desde {input_file}...")

    count = 0
    for i, chunk in enumerate(stream_semantic_chunking(input_file), 1):
        doc_title = f"CORPUS_TESIS_VOL_{i}"
        file_path = os.path.join(OUTPUT_DIR, f"{doc_title}.txt")
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(chunk)
            
        # Optimization: Use maxsplit to check for overflow, but here we just count for logging
        word_count = len(chunk.split())
        print(f"[+] {doc_title} generado localmente ({word_count} palabras).")
        count = i
        
        if not IS_CLOUD_VM:
            gc.collect()

    print(f"[*] Finalizada la inyección de {count} volúmenes.")

if __name__ == "__main__":
    print("[*] Iniciando PROTOCOLO 2: DOCTOR INJECTOR (STREAMING EDITION ⚡)")
    if not os.path.exists(INPUT_FILE):
        print(f"[!] Archivo {INPUT_FILE} no encontrado. Ejecuta Protocolo 1 primero.")
        exit(1)
    
    process_and_upload(INPUT_FILE)
    print("[+] Protocolo 2 Finalizado. Data Lake preparado.")
