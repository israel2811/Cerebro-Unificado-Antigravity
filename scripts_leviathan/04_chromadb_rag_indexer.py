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

# Bolt optimization: Using dynamic relative path calculations via os.path.dirname
# and os.path.abspath to ensure the script can run in any environment seamlessly.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CLEAN_CHUNKS_DIR = os.path.join(SCRIPT_DIR, "clean_chunks")
DB_PATH = os.path.join(os.path.dirname(SCRIPT_DIR), "nexus_vector_db")

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

    # Bolt optimization: Deterministic alphabetical sorting for stable builds.
    archivos = sorted([f for f in os.listdir(CLEAN_CHUNKS_DIR) if f.endswith(".txt")])
    
    if not archivos:
        print("[!] No hay chunks de texto para procesar.")
        return

    print(f"[*] Transformando {len(archivos)} chunks de texto en Embeddings Vectoriales...")
    
    # Bolt optimization: Implement batch processing (BATCH_SIZE = 20) with robust
    # state cleanup inside a finally clause to prevent 'batch poisoning' where failed entries
    # cause subsequent batch failures. Nested try-except-finally blocks handle exceptions per batch.
    batch_docs = []
    batch_metadatas = []
    batch_ids = []
    BATCH_SIZE = 20

    def flush_batch():
        if not batch_docs:
            return
        try:
            print(f"  -> Enviando lote de {len(batch_docs)} documentos a ChromaDB...")
            collection.add(
                documents=batch_docs,
                metadatas=batch_metadatas,
                ids=batch_ids
            )
            print("  ✅ [Lote Embebido]")
        except Exception as ex:
            print(f"  [X] Error vectorizando lote: {ex}")
        finally:
            # Clear mutable buffers to prevent batch poisoning
            batch_docs.clear()
            batch_metadatas.clear()
            batch_ids.clear()

    for i, archivo in enumerate(archivos, 1):
        ruta = os.path.join(CLEAN_CHUNKS_DIR, archivo)
        
        with open(ruta, "r", encoding="utf-8") as f:
            contenido = f.read()
            
        # Bolt optimization: Optimizing word-count truncation using maxsplit (40001)
        # to avoid splitting the entire massive string multiple times, preventing performance drops.
        words = contenido.split(None, 40001)
        if len(words) > 40000:
            print(f"  [!] Advertencia: {archivo} es enorme. Cortando por limite interno de Chroma.")
            contenido = " ".join(words[:40000])

        doc_id = f"chunk_{i}_{archivo}"
        
        batch_docs.append(contenido)
        batch_metadatas.append({"source": archivo, "type": "nexus_chunk"})
        batch_ids.append(doc_id)

        if len(batch_docs) >= BATCH_SIZE:
            flush_batch()

    # Bolt optimization: Explicit flush to ensure any remaining documents are indexed.
    flush_batch()

    print("\n✅ [CHROMADB RAG] Inyección Completada.")
    print(f"📂 Los archivos matriciales se guardaron en: {DB_PATH}")
    print("🎯 Ahora puedes consultar a Claude o ChatGPT usando búsqueda de similitud por cosenos local.")

if __name__ == "__main__":
    local_chroma_rag_inject()
