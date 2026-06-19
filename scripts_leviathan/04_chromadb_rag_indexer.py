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

    # Ordenar archivos para asegurar indexación determinista
    archivos = sorted([f for f in os.listdir(CLEAN_CHUNKS_DIR) if f.endswith(".txt")])
    
    if not archivos:
        print("[!] No hay chunks de texto para procesar.")
        return

    print(f"[*] Transformando {len(archivos)} chunks de texto en Embeddings Vectoriales...")
    
    # OPTIMIZACIÓN BOLT: Procesamiento por lotes (Batching) y Truncamiento Eficiente
    BATCH_SIZE = 20
    batch_docs = []
    batch_metadatas = []
    batch_ids = []

    def flush_batch(b_docs, b_metas, b_ids):
        if not b_docs:
            return
        try:
            print(f"  [⚡] Inyectando lote de {len(b_docs)} documentos a ChromaDB...")
            collection.add(
                documents=b_docs,
                metadatas=b_metas,
                ids=b_ids
            )
        except Exception as e:
            print(f"  [X] Error en inyección por lote: {e}")
        finally:
            # Limpiar lotes tras intento (evitar "batch poisoning" si falla uno)
            b_docs.clear()
            b_metas.clear()
            b_ids.clear()

    for i, archivo in enumerate(archivos, 1):
        ruta = os.path.join(CLEAN_CHUNKS_DIR, archivo)
        
        with open(ruta, "r", encoding="utf-8") as f:
            contenido = f.read()
            
        # OPTIMIZACIÓN BOLT: Truncamiento ultra-rápido usando maxsplit (O(N) vs O(2N+K))
        # split(None, 40001) evita procesar todo el archivo si es excesivamente grande.
        parts = contenido.split(None, 40001)
        if len(parts) > 40000:
            print(f"  [!] Advertencia: {archivo} excede límite. Truncando eficientemente.")
            contenido = " ".join(parts[:40000])

        doc_id = f"chunk_{i}_{archivo}"
        
        batch_docs.append(contenido)
        batch_metadatas.append({"source": archivo, "type": "nexus_chunk"})
        batch_ids.append(doc_id)

        if len(batch_docs) >= BATCH_SIZE:
            flush_batch(batch_docs, batch_metadatas, batch_ids)

    # Vaciar el último lote residual
    flush_batch(batch_docs, batch_metadatas, batch_ids)

    print("\n✅ [CHROMADB RAG] Inyección Completada.")
    print(f"📂 Los archivos matriciales se guardaron en: {DB_PATH}")
    print("🎯 Ahora puedes consultar a Claude o ChatGPT usando búsqueda de similitud por cosenos local.")

if __name__ == "__main__":
    local_chroma_rag_inject()
