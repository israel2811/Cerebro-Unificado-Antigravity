import os
import json
import gc

# CONFIGURACIÓN LEVIATÁN
SEARCH_DIRS = [
    r"C:\Users\Lenovo\.gemini\antigravity\brain",
    r"C:\Users\Lenovo\.codex",
    r"C:\Users\Lenovo\Antigravity_Cloud_Project"
]
ALLOWED_EXTENSIONS = {".json", ".md", ".html", ".txt"} # Evitar leer binarios directamente en utf-8 sin librería
OUTPUT_FILE = r"C:\Users\Lenovo\Antigravity_Cloud_Project\scripts_leviathan\raw_corpus_extraction.txt"
CHUNK_SIZE_BYTES = 1048576 * 5 # 5 MB por bloque de lectura para proteger la RAM de 2GB

def scan_and_extract():
    print("[*] Iniciando OMNI-PARSER. Escaneo profundo de memoria local (Tolerancia OOM: Activa)...")
    
    total_files_scanned = 0
    total_bytes_extracted = 0
    
    # Modo 'w' para reiniciar el corpus, o 'a' si queremos reanudar
    with open(OUTPUT_FILE, "w", encoding="utf-8") as outfile:
        for search_dir in SEARCH_DIRS:
            if not os.path.exists(search_dir):
                print(f"[!] Directorio no encontrado, omitiendo: {search_dir}")
                continue
                
            print(f"[*] Explorando nodo: {search_dir}")
            for root, _, files in os.walk(search_dir):
                for filename in files:
                    ext = os.path.splitext(filename)[1].lower()
                    
                    # Filtro preliminar de extensiones
                    if ext in ALLOWED_EXTENSIONS or ".pb" in ext:
                        filepath = os.path.join(root, filename)
                        total_files_scanned += 1
                        
                        try:
                            # LECTURA POR BLOQUES (Armadura Anti-Colapso de RAM)
                            with open(filepath, "r", encoding="utf-8", errors="ignore") as infile:
                                file_header_written = False
                                
                                while True:
                                    chunk = infile.read(CHUNK_SIZE_BYTES)
                                    if not chunk:
                                        break
                                    
                                    if not file_header_written:
                                        outfile.write(f"\n\n--- ORIGEN: {filepath} ---\n\n")
                                        file_header_written = True
                                        
                                    outfile.write(chunk)
                                    total_bytes_extracted += len(chunk.encode('utf-8'))
                                    
                            # Liberación de memoria tras cada archivo procesado
                            gc.collect()
                            
                        except Exception as e:
                            print(f"[!] Error extrayendo {filepath}: {e}")
                            
    print(f"[+] Extracción completada. Archivos escaneados: {total_files_scanned}")
    print(f"[+] Tamaño del Data Lake Bruto: {total_bytes_extracted / (1024*1024):.2f} MB")
    print(f"[+] Output salvado en: {OUTPUT_FILE}")

if __name__ == "__main__":
    scan_and_extract()
