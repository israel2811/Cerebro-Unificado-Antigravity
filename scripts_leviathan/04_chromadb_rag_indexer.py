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
BATCH_SIZE = 20

def local_chroma_rag_inject():
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

    # Sorteo de archivos para orden determinista
    archivos = sorted([f for f in os.listdir(CLEAN_CHUNKS_DIR) if f.endswith(".txt")])
    
    if not archivos:
        print("[!] No hay chunks de texto para procesar.")
        return

    print(f"[*] Transformando {len(archivos)} chunks de texto en Embeddings Vectoriales (Batch Size: {BATCH_SIZE})...")
    
    # State management for batching
    batch_state = {
        'documents': [],
        'metadatas': [],
        'ids': []
    }

    def flush_batch():
        if not batch_state['ids']:
            return
        try:
            collection.add(
                documents=batch_state['documents'],
                metadatas=batch_state['metadatas'],
                ids=batch_state['ids']
            )
            print(f"  [+] Lote inyectado con éxito ({len(batch_state['ids'])} documentos).")
        except Exception as e:
            print(f"  [X] Error inyectando lote: {e}")
        finally:
            # Reset state even on failure to prevent poisoned batches
            batch_state['documents'] = []
            batch_state['metadatas'] = []
            batch_state['ids'] = []

    for i, archivo in enumerate(archivos, 1):
        ruta = os.path.join(CLEAN_CHUNKS_DIR, archivo)
        
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                contenido = f.read()

            # OPTIMIZACIÓN: Truncamiento eficiente usando maxsplit para evitar particionado total de memoria
            # split(None, 40001) genera máximo 40001 elementos, evitando procesar el resto de un archivo gigante.
            words = contenido.split(None, 40001)
            if len(words) > 40000:
                print(f"  [!] Advertencia: {archivo} es enorme. Cortando por limite interno de Chroma.")
                contenido = " ".join(words[:40000])

            doc_id = f"chunk_{i}_{archivo}"

            batch_state['documents'].append(contenido)
            batch_state['metadatas'].append({"source": archivo, "type": "nexus_chunk"})
            batch_state['ids'].append(doc_id)
            
            if len(batch_state['ids']) >= BATCH_SIZE:
                print(f"  -> Procesando lote hasta documento {i}/{len(archivos)}...")
                flush_batch()

        except Exception as e:
            print(f"  [X] Error procesando {archivo}: {e}")

    # Inyectar lote final restante
    flush_batch()

    print("\n✅ [CHROMADB RAG] Inyección Completada.")
    print(f"📂 Los archivos matriciales se guardaron en: {DB_PATH}")
    print("🎯 Ahora puedes consultar a Claude o ChatGPT usando búsqueda de similitud por cosenos local.")

if __name__ == "__main__":
    local_chroma_rag_inject()
