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

    archivos = [f for f in os.listdir(CLEAN_CHUNKS_DIR) if f.endswith(".txt")]
    
    if not archivos:
        print("[!] No hay chunks de texto para procesar.")
        return

    print(f"[*] Transformando {len(archivos)} chunks de texto en Embeddings Vectoriales...")

    BATCH_SIZE = 50
    batch_docs = []
    batch_metadatas = []
    batch_ids = []

    def flush_batch(docs, metas, ids, current_idx, total):
        """Helper to flush accumulated batches to ChromaDB."""
        if not ids:
            return
        try:
            print(f"  -> [{current_idx}/{total}] Inyectando lote de {len(ids)} documentos...")
            collection.add(documents=docs, metadatas=metas, ids=ids)
        except Exception as e:
            # Reportar el rango de archivos si falla el lote
            print(f"  [X] Error vectorizando lote finalizado en {ids[-1]}: {e}")
        finally:
            # Limpiar el lote para evitar 'poisoned batches' en caso de error
            docs.clear()
            metas.clear()
            ids.clear()

    for i, archivo in enumerate(archivos, 1):
        ruta = os.path.join(CLEAN_CHUNKS_DIR, archivo)

        try:
            with open(ruta, "r", encoding="utf-8") as f:
                contenido = f.read()

            # OPTIMIZACIÓN BOLT: Filtro heurístico por longitud de caracteres antes del split (ahorra CPU)
            # 150,000 caracteres es un umbral seguro antes de validar las 40,000 palabras de Chroma.
            if len(contenido) > 150000:
                words = contenido.split()
                if len(words) > 40000:
                    print(f"  [!] Advertencia: {archivo} es enorme. Cortando por limite interno de Chroma.")
                    contenido = " ".join(words[:40000])

            doc_id = f"chunk_{i}_{archivo}"
            batch_docs.append(contenido)
            batch_metadatas.append({"source": archivo, "type": "nexus_chunk"})
            batch_ids.append(doc_id)

            # Inyectar en bloques para optimizar latencia de red/IPC y permitir paralelismo interno
            if len(batch_ids) >= BATCH_SIZE:
                flush_batch(batch_docs, batch_metadatas, batch_ids, i, len(archivos))

        except Exception as e:
            print(f"  [X] Error procesando {archivo}: {e}")

    # Flush final para cualquier remanente
    flush_batch(batch_docs, batch_metadatas, batch_ids, len(archivos), len(archivos))

    print("\n✅ [CHROMADB RAG] Inyección Completada.")
    print(f"📂 Los archivos matriciales se guardaron en: {DB_PATH}")
    print("🎯 Ahora puedes consultar a Claude o ChatGPT usando búsqueda de similitud por cosenos local.")

if __name__ == "__main__":
    local_chroma_rag_inject()
