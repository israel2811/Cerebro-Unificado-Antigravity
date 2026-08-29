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

def stream_documents(filepath):
    """Generador que lee el corpus por bloques delimitados por el marcador de ORIGEN."""
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        current_doc = []
        for line in f:
            if line.startswith("--- ORIGEN:"):
                if current_doc:
                    yield "".join(current_doc)
                current_doc = [line]
            else:
                current_doc.append(line)
        if current_doc:
            yield "".join(current_doc)

def clean_html_noise(raw_text):
    """Filtra y purifica el texto, quitando HTML, JSON y ruido sintáctico."""
    soup = BeautifulSoup(raw_text, "html.parser")
    text = soup.get_text(separator="\n")
    
    # Limpieza básica de caracteres nulos, múltiples saltos de línea y ruido de JSON/código.
    text = re.sub(r'\{.*?\}', '', text, flags=re.DOTALL) # Quitar brackets JSON grandes
    text = re.sub(r'\n+', '\n', text)
    return text

def save_volume(volume_text, volume_index, word_count):
    """Guarda un volumen procesado en el sistema de archivos."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    doc_title = f"CORPUS_TESIS_VOL_{volume_index}"
    file_path = os.path.join(OUTPUT_DIR, f"{doc_title}.txt")
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(volume_text)
        
    print(f"[+] {doc_title} generado localmente ({word_count} palabras).")

    if not IS_CLOUD_VM:
        gc.collect()
    return volume_index + 1

if __name__ == "__main__":
    print("[*] Iniciando PROTOCOLO 2: DOCTOR INJECTOR (Versión Streaming Optimizada)")
    if not os.path.exists(INPUT_FILE):
        print(f"[!] Archivo {INPUT_FILE} no encontrado. Ejecuta Protocolo 1 primero.")
        exit(1)
        
    print("[*] Procesando corpus en streaming para optimizar RAM...")
    
    current_volume_words = []
    current_word_count = 0
    volume_idx = 1

    for raw_doc in stream_documents(INPUT_FILE):
        # Limpiar documento individualmente
        cleaned_doc = clean_html_noise(raw_doc)
        doc_words = cleaned_doc.split()

        for word in doc_words:
            current_volume_words.append(word)
            current_word_count += 1

            # Si alcanzamos el límite y es un buen punto de corte
            if current_word_count >= MAX_WORDS_PER_CHUNK:
                if word.endswith('.') or word.endswith('\n'):
                    volume_text = " ".join(current_volume_words)
                    volume_idx = save_volume(volume_text, volume_idx, current_word_count)
                    current_volume_words = []
                    current_word_count = 0

        # Liberar memoria después de cada documento
        del cleaned_doc
        del doc_words
        if not IS_CLOUD_VM:
            gc.collect()

    # Guardar el residuo final
    if current_volume_words:
        volume_text = " ".join(current_volume_words)
        save_volume(volume_text, volume_idx, current_word_count)
    
    print("[+] Protocolo 2 Finalizado. Data Lake preparado con balanceo de carga en RAM.")
