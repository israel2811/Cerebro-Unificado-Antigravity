#!/usr/bin/env python3
# ==============================================================================
# 🧠 PILAR 2: WEAPONIZACIÓN VECTORIAL - RAG LOCAL CON CHROMADB
# ==============================================================================
# Rediseñado para ignorar Supabase/Pinecone. Esto corre 100% gratis en tu PC
# o en la Máquina Virtual de Codespaces, insertando la tesis en SQLite local.
# ==============================================================================

import os
import time

try:
    import chromadb
    from chromadb.utils import embedding_functions
except ImportError:
    print("[!] Dependencias faltantes. Instalando en background...")
    print("Corre: pip install chromadb sentence-transformers")
    exit(1)

CLEAN_CHUNKS_DIR = r"/workspaces/Antigravity_Cloud_Project/scripts_leviathan/clean_chunks" if os.name == 'posix' else r"C:\Users\Lenovo\Antigravity_Cloud_Project\scripts_leviathan\clean_chunks"
DB_PATH = r"/workspaces/Antigravity_Cloud_Project/nexus_vector_db" if os.name == 'posix' else r"C:\Users\Lenovo\Antigravity_Cloud_Project\nexus_vector_db"

# CONFIGURACIÓN DE RENDIMIENTO (BOLT ⚡)
BATCH_SIZE = 50  # Optimiza el IOPS y la latencia de transacciones en SQLite
WORD_LIMIT = 40000
CHAR_HEURISTIC = 200000 # ~5 caracteres por palabra, evita split() costoso en archivos pequeños

def local_chroma_rag_inject():
    start_time = time.time()
    print("🚀 [CHROMADB RAG] Base Vectorial 100% Autónoma y Gratuita Iniciada...")
    
    # 1. Inicializar Cliente Chroma (Sin API Keys, guardado en disco duro)
    chroma_client = chromadb.PersistentClient(path=DB_PATH)
    
    # 2. Usar modelo de Embeddings Ligero (MiniLM) para no ahogar la RAM de 2GB
    sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    
    # 3. Crear / Cargar Colección
    collection = chroma_client.get_or_create_collection(name="tesis_cca", embedding_function=sentence_transformer_ef)
    
    if not os.path.exists(CLEAN_CHUNKS_DIR):
        print(f"[!] Directorio {CLEAN_CHUNKS_DIR} vacío. Corre el 02_docs_prep_injector primero.")
        return

    archivos = [f for f in os.listdir(CLEAN_CHUNKS_DIR) if f.endswith(".txt")]
    
    if not archivos:
        print("[!] No hay chunks de texto para procesar.")
        return

    print(f"[*] Transformando {len(archivos)} chunks de texto en Embeddings Vectoriales (Lote: {BATCH_SIZE})...")

    batch_docs = []
    batch_metadatas = []
    batch_ids = []
    
    for i, archivo in enumerate(archivos, 1):
        ruta = os.path.join(CLEAN_CHUNKS_DIR, archivo)
        
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                contenido = f.read()

            # Optimización Bolt: Heurística de caracteres antes de split() costoso
            if len(contenido) > CHAR_HEURISTIC:
                palabras = contenido.split()
                if len(palabras) > WORD_LIMIT:
                    print(f"  [!] Advertencia: {archivo} excede límite. Truncando a {WORD_LIMIT} palabras.")
                    contenido = " ".join(palabras[:WORD_LIMIT])

            doc_id = f"chunk_{i}_{archivo}"
            batch_docs.append(contenido)
            batch_metadatas.append({"source": archivo, "type": "nexus_chunk"})
            batch_ids.append(doc_id)
            
            # Inyectar lote si alcanzamos BATCH_SIZE
            if len(batch_docs) >= BATCH_SIZE:
                print(f"  [⚡] Inyectando lote de {len(batch_docs)} documentos...")
                try:
                    collection.add(
                        documents=batch_docs,
                        metadatas=batch_metadatas,
                        ids=batch_ids
                    )
                except Exception as batch_err:
                    first_file = batch_metadatas[0]['source']
                    last_file = batch_metadatas[-1]['source']
                    print(f"  [X] Error en lote ({first_file} -> {last_file}): {batch_err}")
                finally:
                    # Bolt: Siempre resetear el lote para evitar "poisoned batches"
                    batch_docs, batch_metadatas, batch_ids = [], [], []

        except Exception as e:
            # Errores de lectura o procesamiento individual
            print(f"  [X] Error procesando {archivo}: {e}")

    # Flush final (Último lote parcial)
    if batch_docs:
        print(f"  [⚡] Inyectando lote final de {len(batch_docs)} documentos...")
        try:
            collection.add(
                documents=batch_docs,
                metadatas=batch_metadatas,
                ids=batch_ids
            )
        except Exception as e:
            print(f"  [X] Error en lote final: {e}")

    duration = time.time() - start_time
    print(f"\n✅ [CHROMADB RAG] Inyección Completada en {duration:.2f}s.")
    print(f"📂 Los archivos matriciales se guardaron en: {DB_PATH}")
    print("🎯 Ahora puedes consultar a Claude o ChatGPT usando búsqueda de similitud por cosenos local.")

if __name__ == "__main__":
    local_chroma_rag_inject()
