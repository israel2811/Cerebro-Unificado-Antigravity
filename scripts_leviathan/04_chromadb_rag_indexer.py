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

# Resolución dinámica de rutas relativas al script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CLEAN_CHUNKS_DIR = os.path.join(SCRIPT_DIR, "clean_chunks")
DB_PATH = os.path.join(os.path.dirname(SCRIPT_DIR), "nexus_vector_db")

# Lote de inserción vectorial para reducir transacciones en SQLite/ChromaDB
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

    # Ordenamiento alfabético determinista para indexación consistente
    archivos = sorted([f for f in os.listdir(CLEAN_CHUNKS_DIR) if f.endswith(".txt")])
    
    if not archivos:
        print("[!] No hay chunks de texto para procesar.")
        return

    print(f"[*] Transformando {len(archivos)} chunks de texto en Embeddings Vectoriales...")
    
    batch_docs = []
    batch_metadatas = []
    batch_ids = []

    def flush_batch():
        if batch_docs:
            try:
                collection.add(
                    documents=list(batch_docs),
                    metadatas=list(batch_metadatas),
                    ids=list(batch_ids)
                )
            except Exception as e:
                print(f"  [X] Error en inyección por lote de vectorización: {e}")
            finally:
                batch_docs.clear()
                batch_metadatas.clear()
                batch_ids.clear()

    for i, archivo in enumerate(archivos, 1):
        ruta = os.path.join(CLEAN_CHUNKS_DIR, archivo)
        
        with open(ruta, "r", encoding="utf-8") as f:
            contenido = f.read()
            
        # Segmentación preventiva eficiente utilizando maxsplit=40001 para evitar split masivo
        words = contenido.split(None, 40001)
        if len(words) > 40000:
            print(f"  [!] Advertencia: {archivo} es enorme. Cortando por limite interno de Chroma.")
            contenido = " ".join(words[:40000])

        doc_id = f"chunk_{i}_{archivo}"
        
        print(f"  -> [{i}/{len(archivos)}] Procesando: {archivo}...")
        batch_docs.append(contenido)
        batch_metadatas.append({"source": archivo, "type": "nexus_chunk"})
        batch_ids.append(doc_id)

        if len(batch_docs) >= BATCH_SIZE:
            flush_batch()

    # Flush final para chunks restantes menores al tamaño de lote BATCH_SIZE
    flush_batch()

    print("\n✅ [CHROMADB RAG] Inyección Completada.")
    print(f"📂 Los archivos matriciales se guardaron en: {DB_PATH}")
    print("🎯 Ahora puedes consultar a Claude o ChatGPT usando búsqueda de similitud por cosenos local.")

if __name__ == "__main__":
    local_chroma_rag_inject()
